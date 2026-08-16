import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import {
  fetchUrlHealthChecker,
  shouldCheckUrl,
  stubUrlHealthChecker,
} from "@/lib/affiliate/health";
import { resolveAffiliateRedirectBase } from "@/lib/affiliate/urls";

export const dynamic = "force-dynamic";

/**
 * Manual / throttled health check. Does NOT hit every URL constantly.
 * Pass ?productId=… or ?due=true (only products due for recheck).
 * Pass ?dryRun=true to skip network.
 */
export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const sp = request.nextUrl.searchParams;
  const productId = (body.productId || sp.get("productId")) as string | null;
  const dueOnly = body.due === true || sp.get("due") === "true";
  const dryRun = body.dryRun === true || sp.get("dryRun") === "true";
  const limit = Math.min(Number(body.limit || sp.get("limit") || 10), 25);

  const checker = dryRun ? stubUrlHealthChecker() : fetchUrlHealthChecker;

  const candidates = productId
    ? await prisma.affiliateProduct.findMany({ where: { id: productId } })
    : await prisma.affiliateProduct.findMany({
        where: { active: true },
        orderBy: { urlLastCheckedAt: "asc" },
        take: limit * 3,
      });

  const toCheck = candidates
    .filter((p) => !dueOnly || shouldCheckUrl(p.urlLastCheckedAt))
    .slice(0, limit);

  const results = [];
  for (const product of toCheck) {
    const checkUrl = resolveAffiliateRedirectBase({
      destinationUrl: product.destinationUrl,
      affiliateUrl: product.affiliateUrl,
    });
    const result = await checker.check(checkUrl);
    await prisma.affiliateUrlHealthCheck.create({
      data: {
        affiliateProductId: product.id,
        status: result.status,
        httpStatus: result.httpStatus,
        finalUrl: result.finalUrl,
        notes: result.notes,
      },
    });
    await prisma.affiliateProduct.update({
      where: { id: product.id },
      data: {
        urlHealthStatus: result.status,
        urlLastCheckedAt: new Date(),
      },
    });
    results.push({ productId: product.id, slug: product.slug, ...result });
  }

  return NextResponse.json({ checked: results.length, results });
}
