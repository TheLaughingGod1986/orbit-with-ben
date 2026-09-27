/**
 * Affiliate goals ladder — reporting only.
 * Never auto-inserts placements or bypasses the editorial trust gate.
 *
 * Clock starts on first approved AffiliatePlacement (or first click if earlier).
 * Month 1: floor £10, target £20.
 * Month N: target = 2 × previous month’s actual commission.
 */

import { addMonths, differenceInCalendarDays, min as minDate } from "date-fns";

export const GOALS_MONTH_1_FLOOR_GBP = 10;
export const GOALS_MONTH_1_TARGET_GBP = 20;

export type GoalsPaceStatus = "on_track" | "behind" | "ahead" | "not_started";

export type GoalsMonthRange = {
  monthNumber: number;
  start: Date;
  end: Date;
};

export type AffiliateGoalsSnapshot = {
  /** null when no approved placement and no clicks yet */
  clockStarted: boolean;
  clockStartDate: string | null;
  monthNumber: number | null;
  monthStart: string | null;
  monthEnd: string | null;
  targetGbp: number | null;
  floorGbp: number | null;
  revenueSoFarGbp: number;
  clicksThisMonth: number;
  workingLinks: number;
  brokenLinks: number;
  status: GoalsPaceStatus;
  /** Pace target at “now” (linear toward month target). */
  pacedTargetGbp: number | null;
  lastMonthActualGbp: number | null;
  lastMonthNumber: number | null;
  /** Explicit: goals never drive placement auto-insert. */
  reportingOnly: true;
};

export type CommissionPoint = {
  date: Date;
  commissionAmount: number;
};

/** Start of local calendar day for stable month boundaries. */
export function startOfLocalDay(d: Date): Date {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0, 0);
}

/**
 * Resolve goals clock: earliest of first approved placement vs first click.
 */
export function resolveGoalsClockStart(args: {
  firstApprovedPlacementAt: Date | null;
  firstClickAt: Date | null;
}): Date | null {
  const dates = [args.firstApprovedPlacementAt, args.firstClickAt].filter(
    (d): d is Date => d != null && !Number.isNaN(d.getTime()),
  );
  if (!dates.length) return null;
  return startOfLocalDay(minDate(dates));
}

/**
 * 1-based goals month index from clock start (anniversary months).
 */
export function goalsMonthNumber(clockStart: Date, now: Date): number {
  const start = startOfLocalDay(clockStart);
  const current = startOfLocalDay(now);
  if (current < start) return 1;

  let months =
    (current.getFullYear() - start.getFullYear()) * 12 +
    (current.getMonth() - start.getMonth());
  if (current.getDate() < start.getDate()) months -= 1;
  return Math.max(1, months + 1);
}

export function goalsMonthRange(clockStart: Date, monthNumber: number): GoalsMonthRange {
  const start = addMonths(startOfLocalDay(clockStart), monthNumber - 1);
  const endExclusive = addMonths(start, 1);
  const end = new Date(endExclusive.getTime() - 1);
  return { monthNumber, start, end };
}

export function sumCommissionInRange(
  points: CommissionPoint[],
  start: Date,
  end: Date,
): number {
  let sum = 0;
  for (const p of points) {
    const t = p.date.getTime();
    if (t >= start.getTime() && t <= end.getTime()) {
      sum += p.commissionAmount;
    }
  }
  return Math.round(sum * 100) / 100;
}

/**
 * Month 1 target = £20. Month N = 2 × previous month actual.
 */
export function computeMonthTargetGbp(args: {
  monthNumber: number;
  previousMonthActualGbp: number;
}): { targetGbp: number; floorGbp: number | null } {
  if (args.monthNumber <= 1) {
    return {
      targetGbp: GOALS_MONTH_1_TARGET_GBP,
      floorGbp: GOALS_MONTH_1_FLOOR_GBP,
    };
  }
  return {
    targetGbp: Math.round(args.previousMonthActualGbp * 2 * 100) / 100,
    floorGbp: null,
  };
}

export function computePaceStatus(args: {
  revenueSoFarGbp: number;
  targetGbp: number;
  pacedTargetGbp: number;
  floorGbp: number | null;
}): GoalsPaceStatus {
  if (args.revenueSoFarGbp >= args.targetGbp) return "ahead";
  if (args.revenueSoFarGbp + 1e-9 >= args.pacedTargetGbp) return "on_track";
  // Month 1: still “on track” if at/above floor pace toward floor when early — else behind
  if (args.floorGbp != null && args.revenueSoFarGbp >= args.floorGbp) {
    // Hit floor but behind target pace
    return "on_track";
  }
  return "behind";
}

export function linearPacedTarget(args: {
  targetGbp: number;
  monthStart: Date;
  monthEnd: Date;
  now: Date;
}): number {
  const start = args.monthStart.getTime();
  const end = args.monthEnd.getTime();
  const now = Math.min(Math.max(args.now.getTime(), start), end);
  const totalMs = Math.max(end - start, 1);
  const elapsed = now - start;
  return Math.round(args.targetGbp * (elapsed / totalMs) * 100) / 100;
}

/**
 * Pure snapshot builder — inject clock + commissions (no DB).
 */
export function buildAffiliateGoalsSnapshot(args: {
  now: Date;
  clockStart: Date | null;
  commissions: CommissionPoint[];
  clicksThisMonth: number;
  workingLinks: number;
  brokenLinks: number;
}): AffiliateGoalsSnapshot {
  const base = {
    clicksThisMonth: args.clicksThisMonth,
    workingLinks: args.workingLinks,
    brokenLinks: args.brokenLinks,
    reportingOnly: true as const,
  };

  if (!args.clockStart) {
    return {
      ...base,
      clockStarted: false,
      clockStartDate: null,
      monthNumber: null,
      monthStart: null,
      monthEnd: null,
      targetGbp: null,
      floorGbp: null,
      revenueSoFarGbp: 0,
      status: "not_started",
      pacedTargetGbp: null,
      lastMonthActualGbp: null,
      lastMonthNumber: null,
    };
  }

  const monthNumber = goalsMonthNumber(args.clockStart, args.now);
  const range = goalsMonthRange(args.clockStart, monthNumber);
  const revenueSoFarGbp = sumCommissionInRange(
    args.commissions,
    range.start,
    // Cap “so far” at now within the month
    args.now < range.end ? args.now : range.end,
  );

  let lastMonthActualGbp: number | null = null;
  let lastMonthNumber: number | null = null;
  if (monthNumber >= 2) {
    lastMonthNumber = monthNumber - 1;
    const prev = goalsMonthRange(args.clockStart, lastMonthNumber);
    lastMonthActualGbp = sumCommissionInRange(
      args.commissions,
      prev.start,
      prev.end,
    );
  }

  const { targetGbp, floorGbp } = computeMonthTargetGbp({
    monthNumber,
    previousMonthActualGbp: lastMonthActualGbp ?? 0,
  });

  const pacedTargetGbp = linearPacedTarget({
    targetGbp,
    monthStart: range.start,
    monthEnd: range.end,
    now: args.now,
  });

  const status = computePaceStatus({
    revenueSoFarGbp,
    targetGbp,
    pacedTargetGbp,
    floorGbp,
  });

  return {
    ...base,
    clockStarted: true,
    clockStartDate: startOfLocalDay(args.clockStart).toISOString(),
    monthNumber,
    monthStart: range.start.toISOString(),
    monthEnd: range.end.toISOString(),
    targetGbp,
    floorGbp,
    revenueSoFarGbp,
    status,
    pacedTargetGbp,
    lastMonthActualGbp,
    lastMonthNumber,
  };
}

/** Days remaining in the current goals month (inclusive of today). */
export function daysRemainingInGoalsMonth(
  monthEnd: Date,
  now: Date,
): number {
  return Math.max(0, differenceInCalendarDays(monthEnd, now));
}
