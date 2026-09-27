/**
 * Commission, RPM, and revenue helpers.
 * Pure functions — no DB access.
 */

export function estimateCommission(args: {
  saleAmount?: number | null;
  price?: number | null;
  commissionType?: string | null;
  commissionValue?: number | null;
  estimatedCommission?: number | null;
}): number {
  if (args.estimatedCommission != null && args.estimatedCommission >= 0) {
    return roundMoney(args.estimatedCommission);
  }
  const base = args.saleAmount ?? args.price ?? 0;
  const value = args.commissionValue ?? 0;
  if (!value) return 0;
  if ((args.commissionType || "PERCENTAGE") === "FIXED") {
    return roundMoney(value);
  }
  return roundMoney((base * value) / 100);
}

export function roundMoney(n: number): number {
  return Math.round(n * 100) / 100;
}

/** Affiliate RPM = (affiliate revenue / views) * 1000 */
export function affiliateRpm(revenue: number, views: number): number | null {
  if (!views || views <= 0) return null;
  return roundMoney((revenue / views) * 1000);
}

/** Revenue per click (EPC) */
export function earningsPerClick(revenue: number, clicks: number): number | null {
  if (!clicks || clicks <= 0) return null;
  return roundMoney(revenue / clicks);
}

export function conversionRate(conversions: number, clicks: number): number | null {
  if (!clicks || clicks <= 0) return null;
  return roundMoney((conversions / clicks) * 100);
}

export function clickThroughRate(clicks: number, views: number): number | null {
  if (!views || views <= 0) return null;
  return roundMoney((clicks / views) * 100);
}

export function revenuePerThousandViews(revenue: number, views: number): number | null {
  return affiliateRpm(revenue, views);
}

/**
 * Total Content RPM foundation: (ads + affiliate + sponsorship) / views * 1000.
 * Sponsorship optional for future.
 */
export function totalContentRpm(args: {
  views: number;
  adsenseRevenue?: number;
  affiliateRevenue?: number;
  sponsorshipRevenue?: number;
}): number | null {
  if (!args.views || args.views <= 0) return null;
  const total =
    (args.adsenseRevenue ?? 0) +
    (args.affiliateRevenue ?? 0) +
    (args.sponsorshipRevenue ?? 0);
  return roundMoney((total / args.views) * 1000);
}

export type ProgrammeRevenueRow = {
  programmeId: string;
  programmeName: string;
  clicks: number;
  conversions: number;
  revenue: number;
  epc: number | null;
  conversionRate: number | null;
};

export function summariseProgrammePerformance(
  rows: Array<{
    programmeId: string;
    programmeName: string;
    clicks: number;
    conversions: number;
    revenue: number;
  }>,
): ProgrammeRevenueRow[] {
  return rows.map((r) => ({
    ...r,
    revenue: roundMoney(r.revenue),
    epc: earningsPerClick(r.revenue, r.clicks),
    conversionRate: conversionRate(r.conversions, r.clicks),
  }));
}
