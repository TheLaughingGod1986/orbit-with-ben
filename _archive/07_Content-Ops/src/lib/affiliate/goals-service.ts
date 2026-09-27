import { prisma } from "@/lib/storage/prisma";
import {
  buildAffiliateGoalsSnapshot,
  resolveGoalsClockStart,
  goalsMonthRange,
  goalsMonthNumber,
  type AffiliateGoalsSnapshot,
} from "./goals";

/**
 * Load goals panel data for the internal /affiliate dashboard.
 * Reporting only — does not mutate placements or bypass the editorial gate.
 */
export async function getAffiliateGoalsPanel(
  now: Date = new Date(),
): Promise<AffiliateGoalsSnapshot> {
  const [earliestApproved, firstClick, conversions, brokenLinks, activeProducts] =
    await Promise.all([
      prisma.affiliatePlacement.findFirst({
        where: { status: { in: ["APPROVED", "ACTIVE"] } },
        orderBy: { updatedAt: "asc" },
        select: { updatedAt: true },
      }),
      prisma.affiliateClick.findFirst({
        orderBy: { timestamp: "asc" },
        select: { timestamp: true },
      }),
      prisma.affiliateConversion.findMany({
        select: { conversionDate: true, commissionAmount: true },
      }),
      prisma.affiliateProduct.count({
        where: { active: true, urlHealthStatus: "BROKEN" },
      }),
      prisma.affiliateProduct.count({
        where: { active: true },
      }),
    ]);

  const clockStart = resolveGoalsClockStart({
    firstApprovedPlacementAt: earliestApproved?.updatedAt ?? null,
    firstClickAt: firstClick?.timestamp ?? null,
  });

  const workingLinks = Math.max(0, activeProducts - brokenLinks);

  let clicksThisMonth = 0;
  if (clockStart) {
    const monthNumber = goalsMonthNumber(clockStart, now);
    const range = goalsMonthRange(clockStart, monthNumber);
    clicksThisMonth = await prisma.affiliateClick.count({
      where: {
        timestamp: {
          gte: range.start,
          lte: now < range.end ? now : range.end,
        },
      },
    });
  }

  return buildAffiliateGoalsSnapshot({
    now,
    clockStart,
    commissions: conversions.map((c) => ({
      date: c.conversionDate,
      commissionAmount: c.commissionAmount,
    })),
    clicksThisMonth,
    workingLinks,
    brokenLinks,
  });
}
