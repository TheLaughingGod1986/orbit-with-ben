import { prisma } from "@/lib/storage/prisma";
import { getEnv } from "@/lib/env";
import {
  evaluateAffiliateGoLive,
  isPlaceholderAffiliateUrl,
  type GoLiveReport,
} from "./go-live";
import { LIVE_PRODUCT_URLS } from "./live-product-urls";
import { getAmazonAssociateTag, getBrilliantAffiliateId, getAffiliateRedirectBaseUrl } from "./urls";

export async function getAffiliateGoLiveReport(opts?: {
  probeGoRoute?: boolean;
}): Promise<GoLiveReport> {
  let appBaseUrl: string | null = null;
  try {
    appBaseUrl = getEnv().APP_BASE_URL;
  } catch {
    appBaseUrl = process.env.APP_BASE_URL?.trim() || null;
  }

  const [activeProducts, activePrograms, approvedPlacements, clickCount, brokenUrlCount] =
    await Promise.all([
      prisma.affiliateProduct.findMany({
        where: { active: true },
        select: { destinationUrl: true, affiliateUrl: true },
      }),
      prisma.affiliateProgram.count({ where: { status: "ACTIVE" } }),
      prisma.affiliatePlacement.count({
        where: { status: { in: ["APPROVED", "ACTIVE"] } },
      }),
      prisma.affiliateClick.count(),
      prisma.affiliateProduct.count({
        where: { active: true, urlHealthStatus: "BROKEN" },
      }),
    ]);

  const placeholderUrlCount = activeProducts.filter(
    (p) =>
      isPlaceholderAffiliateUrl(p.destinationUrl) ||
      isPlaceholderAffiliateUrl(p.affiliateUrl),
  ).length;

  let goRouteReachable: boolean | null = null;
  if (opts?.probeGoRoute) {
    goRouteReachable = await probeGoRedirectBase();
  }

  return evaluateAffiliateGoLive({
    amazonTag: getAmazonAssociateTag(),
    brilliantId: getBrilliantAffiliateId(),
    appBaseUrl,
    affiliateRedirectBaseUrl: process.env.AFFILIATE_REDIRECT_BASE_URL?.trim() || null,
    activeProductCount: activeProducts.length,
    placeholderUrlCount,
    brokenUrlCount,
    activeProgramCount: activePrograms,
    approvedPlacementCount: approvedPlacements,
    clickCount,
    goRouteReachable,
  });
}

async function probeGoRedirectBase(): Promise<boolean> {
  try {
    const base = getAffiliateRedirectBaseUrl().replace(/\/$/, "");
    // Probe without a product slug — expect 404 JSON from app, or any HTTP response from host
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 6_000);
    try {
      const res = await fetch(`${base}/__orbit_go_live_probe__`, {
        method: "GET",
        redirect: "manual",
        signal: controller.signal,
      });
      // Any response from our host counts (404 is fine — means /go is mounted)
      return res.status > 0;
    } finally {
      clearTimeout(timer);
    }
  } catch {
    return false;
  }
}

/**
 * Apply LIVE_PRODUCT_URLS onto matching AffiliateProduct rows.
 * Does not invent affiliate IDs — Amazon/Brilliant tags stay in env.
 */
export async function applyLiveProductUrls(opts?: {
  dryRun?: boolean;
}): Promise<{ updated: string[]; skipped: string[]; missing: string[] }> {
  const updated: string[] = [];
  const skipped: string[] = [];
  const missing: string[] = [];

  for (const spec of LIVE_PRODUCT_URLS) {
    const product = await prisma.affiliateProduct.findUnique({
      where: { slug: spec.slug },
    });
    if (!product) {
      missing.push(spec.slug);
      continue;
    }
    const affiliateUrl = spec.affiliateUrl || spec.destinationUrl;
    const already =
      product.destinationUrl === spec.destinationUrl &&
      product.affiliateUrl === affiliateUrl &&
      !isPlaceholderAffiliateUrl(product.destinationUrl);
    if (already) {
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
        },
      });
    }
    updated.push(spec.slug);
  }

  return { updated, skipped, missing };
}
