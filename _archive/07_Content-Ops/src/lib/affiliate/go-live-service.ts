import { prisma } from "@/lib/storage/prisma";
import { getEnv } from "@/lib/env";
import {
  evaluateAffiliateGoLive,
  type GoLiveReport,
} from "./go-live";
import { isPlaceholderAffiliateUrl } from "./live-product-urls";
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

  // Empty affiliateUrl is intentional (tag stamped at /go). Only flag real placeholders.
  const placeholderUrlCount = activeProducts.filter((p) => {
    if (isPlaceholderAffiliateUrl(p.destinationUrl)) return true;
    const aff = p.affiliateUrl?.trim() || "";
    return aff.length > 0 && isPlaceholderAffiliateUrl(aff);
  }).length;

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
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 6_000);
    try {
      const res = await fetch(`${base}/__orbit_go_live_probe__`, {
        method: "GET",
        redirect: "manual",
        signal: controller.signal,
      });
      return res.status > 0;
    } finally {
      clearTimeout(timer);
    }
  } catch {
    return false;
  }
}
