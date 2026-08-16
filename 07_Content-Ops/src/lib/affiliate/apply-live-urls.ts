/**
 * Additive apply of LIVE_PRODUCT_URLS onto AffiliateProduct rows.
 * Updates existing rows; creates missing topic-book products.
 * Does not reset the database. Never invents or commits affiliate tags.
 */

import { prisma } from "@/lib/storage/prisma";
import { upsertProductTags } from "./products";
import {
  LIVE_PRODUCT_URLS,
  isPlaceholderAffiliateUrl,
  type LiveProductUrlSpec,
} from "./live-product-urls";

export type ApplyLiveUrlsResult = {
  updated: string[];
  created: string[];
  skipped: string[];
  missing: string[];
};

/**
 * Apply confirmed live destination URLs onto matching products.
 * Creates rows for new verified slugs when absent (additive — no DB reset).
 * Leaves affiliateUrl empty — tag stamped at /go from AMAZON_ASSOCIATE_TAG.
 */
export async function applyLiveProductUrls(opts?: {
  dryRun?: boolean;
}): Promise<ApplyLiveUrlsResult> {
  const updated: string[] = [];
  const created: string[] = [];
  const skipped: string[] = [];
  const missing: string[] = [];

  for (const spec of LIVE_PRODUCT_URLS) {
    const product = await prisma.affiliateProduct.findUnique({
      where: { slug: spec.slug },
    });

    if (!product) {
      const createdOk = await createMissingLiveProduct(spec, opts?.dryRun);
      if (createdOk) {
        created.push(spec.slug);
      } else {
        missing.push(spec.slug);
      }
      continue;
    }

    const affiliateUrl = resolveStoredAffiliateUrl(spec);
    const programmeId = await resolveProgrammeId(spec, product.affiliateProgramId);

    const needsUpdate =
      product.destinationUrl !== spec.destinationUrl ||
      product.affiliateUrl !== affiliateUrl ||
      (spec.active !== undefined && product.active !== spec.active) ||
      (spec.name !== undefined && product.name !== spec.name) ||
      (spec.description !== undefined && product.description !== spec.description) ||
      programmeId !== null;

    if (!needsUpdate) {
      if (!opts?.dryRun && spec.tags?.length) {
        await upsertProductTags(product.id, spec.tags);
      }
      skipped.push(spec.slug);
      continue;
    }

    if (!opts?.dryRun) {
      await prisma.affiliateProduct.update({
        where: { id: product.id },
        data: {
          destinationUrl: spec.destinationUrl,
          affiliateUrl,
          notes: spec.notes,
          urlHealthStatus: "UNKNOWN",
          ...(spec.name ? { name: spec.name } : {}),
          ...(spec.description ? { description: spec.description } : {}),
          ...(spec.active !== undefined ? { active: spec.active } : {}),
          ...(programmeId ? { affiliateProgramId: programmeId } : {}),
        },
      });
      if (spec.tags?.length) {
        await upsertProductTags(product.id, spec.tags);
      }
    }
    updated.push(spec.slug);
  }

  return { updated, created, skipped, missing };
}

async function createMissingLiveProduct(
  spec: LiveProductUrlSpec,
  dryRun?: boolean,
): Promise<boolean> {
  // Inactive placeholder stubs (e.g. LEGO) should already exist from seed — skip inventing junk.
  if (isPlaceholderAffiliateUrl(spec.destinationUrl) && spec.active === false) {
    return false;
  }
  if (!spec.name || !spec.category || !spec.programmeSlug) {
    return false;
  }

  if (dryRun) return true;

  const programme = await prisma.affiliateProgram.findUnique({
    where: { slug: spec.programmeSlug },
    select: { id: true },
  });
  if (!programme) return false;

  const product = await prisma.affiliateProduct.create({
    data: {
      affiliateProgramId: programme.id,
      name: spec.name,
      slug: spec.slug,
      description: spec.description || null,
      destinationUrl: spec.destinationUrl,
      affiliateUrl: resolveStoredAffiliateUrl(spec),
      category: spec.category,
      price: spec.price ?? null,
      currency: "GBP",
      estimatedCommission: spec.estimatedCommission ?? null,
      commissionType: "PERCENTAGE",
      active: spec.active ?? true,
      featured: spec.featured ?? false,
      evergreen: spec.evergreen ?? false,
      priority: spec.priority ?? 0,
      notes: spec.notes,
      urlHealthStatus: "UNKNOWN",
    },
  });

  if (spec.tags?.length) {
    await upsertProductTags(product.id, spec.tags);
  }
  return true;
}

function resolveStoredAffiliateUrl(spec: LiveProductUrlSpec): string {
  if (spec.affiliateUrl === undefined || spec.affiliateUrl === "") {
    return "";
  }
  return spec.affiliateUrl;
}

async function resolveProgrammeId(
  spec: LiveProductUrlSpec,
  currentProgrammeId: string,
): Promise<string | null> {
  if (!spec.programmeSlug) return null;
  const programme = await prisma.affiliateProgram.findUnique({
    where: { slug: spec.programmeSlug },
    select: { id: true },
  });
  if (!programme || programme.id === currentProgrammeId) return null;
  return programme.id;
}
