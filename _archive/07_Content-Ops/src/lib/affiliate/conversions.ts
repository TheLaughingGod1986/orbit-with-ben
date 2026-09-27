import { prisma } from "@/lib/storage/prisma";
import {
  AFFILIATE_CSV_DEFAULT_MAPPINGS,
  parseAffiliateCsv,
  previewAffiliateCsv,
  rowsToConversions,
  type AffiliateColumnMapping,
} from "./csv-import";
import { roundMoney } from "./revenue";

export async function previewConversionImport(args: {
  csvText: string;
  source?: string;
  mapping?: Partial<AffiliateColumnMapping>;
}) {
  const source = args.source || "generic";
  const mapping =
    args.mapping ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS[source] ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS.generic;
  const preview = previewAffiliateCsv(args.csvText, mapping);

  const existing = preview.contentHash
    ? await prisma.affiliateImportBatch.findUnique({
        where: { contentHash: preview.contentHash },
      })
    : null;

  return {
    preview,
    alreadyImported: Boolean(existing),
    existingBatchId: existing?.id ?? null,
  };
}

export async function commitConversionImport(args: {
  csvText: string;
  source?: string;
  programmeSlug: string;
  filename?: string;
  mapping?: Partial<AffiliateColumnMapping>;
  dryRun?: boolean;
}) {
  const source = args.source || "generic";
  const mapping =
    args.mapping ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS[source] ||
    AFFILIATE_CSV_DEFAULT_MAPPINGS.generic;

  const { rows, contentHash } = parseAffiliateCsv(args.csvText, mapping);

  const existing = await prisma.affiliateImportBatch.findUnique({
    where: { contentHash },
  });
  if (existing) {
    return {
      ok: false as const,
      duplicate: true,
      batchId: existing.id,
      message: "This CSV was already imported (duplicate content hash).",
    };
  }

  const programme = await prisma.affiliateProgram.findUnique({
    where: { slug: args.programmeSlug },
  });
  if (!programme) {
    throw new Error(`Programme not found: ${args.programmeSlug}`);
  }

  const { conversions, errors } = rowsToConversions(rows);

  if (args.dryRun) {
    return {
      ok: true as const,
      dryRun: true,
      rowCount: rows.length,
      successCount: conversions.length,
      errorCount: errors.length,
      errors,
      sample: conversions.slice(0, 5),
    };
  }

  const batch = await prisma.affiliateImportBatch.create({
    data: {
      programmeSlug: args.programmeSlug,
      filename: args.filename || null,
      source,
      rowCount: rows.length,
      successCount: 0,
      errorCount: errors.length,
      skippedCount: 0,
      errorsJson: errors.length ? JSON.stringify(errors) : null,
      contentHash,
    },
  });

  let successCount = 0;
  let skippedCount = 0;
  const commitErrors = [...errors];

  for (const row of conversions) {
    let productId: string | null = null;
    if (row.productSlug) {
      const p = await prisma.affiliateProduct.findUnique({
        where: { slug: row.productSlug },
      });
      productId = p?.id ?? null;
    } else if (row.productName) {
      const p = await prisma.affiliateProduct.findFirst({
        where: {
          affiliateProgramId: programme.id,
          name: { contains: row.productName },
        },
      });
      productId = p?.id ?? null;
    }

    const orderReference =
      row.orderReference || `auto-${contentHash.slice(0, 8)}-${successCount}`;

    try {
      await prisma.affiliateConversion.create({
        data: {
          affiliateProgramId: programme.id,
          affiliateProductId: productId,
          orderReference,
          saleAmount: roundMoney(row.saleAmount),
          commissionAmount: roundMoney(row.commissionAmount),
          currency: row.currency,
          conversionDate: row.conversionDate,
          imported: true,
          importBatchId: batch.id,
          source,
        },
      });
      successCount += 1;

      if (productId && row.orders > 0) {
        const placement = await prisma.affiliatePlacement.findFirst({
          where: {
            affiliateProductId: productId,
            status: { in: ["APPROVED", "ACTIVE"] },
          },
          orderBy: { updatedAt: "desc" },
        });
        if (placement) {
          await prisma.affiliatePlacement.update({
            where: { id: placement.id },
            data: {
              conversions: { increment: row.orders || 1 },
              estimatedRevenue: { increment: row.commissionAmount },
            },
          });
        }
      }
    } catch (err) {
      skippedCount += 1;
      commitErrors.push(
        err instanceof Error ? err.message : `Failed to import ${orderReference}`,
      );
    }
  }

  await prisma.affiliateImportBatch.update({
    where: { id: batch.id },
    data: {
      successCount,
      skippedCount,
      errorCount: commitErrors.length,
      errorsJson: commitErrors.length ? JSON.stringify(commitErrors.slice(0, 50)) : null,
    },
  });

  return {
    ok: true as const,
    dryRun: false,
    batchId: batch.id,
    rowCount: rows.length,
    successCount,
    skippedCount,
    errorCount: commitErrors.length,
    errors: commitErrors.slice(0, 20),
  };
}
