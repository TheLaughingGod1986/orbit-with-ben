/**
 * YouTube schedule safety guards.
 * Placeholder holding dates (2026-12-31) are forbidden.
 */
export const PLACEHOLDER_HOLD_DATE_PREFIX = "2026-12-31";

export function isPlaceholderHoldPublishAt(publishAt: string | null | undefined): boolean {
  if (!publishAt) return false;
  return String(publishAt).startsWith(PLACEHOLDER_HOLD_DATE_PREFIX);
}

export function assertNotPlaceholderHoldPublishAt(publishAt: string | null | undefined): void {
  if (isPlaceholderHoldPublishAt(publishAt)) {
    throw new Error(
      "SCHEDULE BLOCKED:\n31 Dec placeholder holding dates are no longer permitted.\n" +
        `Received publishAt=${publishAt}\nUse PRIVATE + unscheduled instead of a fake publishAt.`,
    );
  }
}

export type ScheduleCadenceInput = {
  format: "longform" | "shorts";
  publishAtIso: string;
  /** Shorts already scheduled/public on this calendar day (recovery timezone). */
  shortsOnSameDay: number;
  /** Longs already scheduled that same ISO week (optional). */
  longsInSameWeek?: number;
  maxShortsPerDay?: number;
  maxLongsPerWeek?: number;
  isHistoricalDuplicate?: boolean;
  isCanonical?: boolean;
  contentId?: string | null;
  collidingContentId?: string | null;
  sameMinuteCollision?: boolean;
};

export type ScheduleCadenceResult = {
  ok: boolean;
  errors: string[];
};

export function assertScheduleCadence(input: ScheduleCadenceInput): ScheduleCadenceResult {
  const errors: string[] = [];
  if (isPlaceholderHoldPublishAt(input.publishAtIso)) {
    errors.push(
      "SCHEDULE BLOCKED: 31 Dec placeholder holding dates are no longer permitted",
    );
  }
  const t = Date.parse(input.publishAtIso);
  if (Number.isNaN(t)) errors.push("publishAt is not a valid ISO timestamp");
  else if (t <= Date.now()) errors.push("publishAt must be in the future");

  if (input.isHistoricalDuplicate) {
    errors.push("SCHEDULE BLOCKED: historical duplicate IDs cannot be scheduled");
  }
  if (input.sameMinuteCollision) {
    errors.push("SCHEDULE BLOCKED: another upload shares the same publish minute");
  }
  if (input.collidingContentId && input.contentId && input.collidingContentId === input.contentId) {
    errors.push("SCHEDULE BLOCKED: duplicate contentId already scheduled");
  }

  const maxShorts = input.maxShortsPerDay ?? 1;
  const maxLongs = input.maxLongsPerWeek ?? 1;
  if (input.format === "shorts" && input.shortsOnSameDay >= maxShorts) {
    errors.push(`SCHEDULE BLOCKED: max ${maxShorts} Short/day exceeded`);
  }
  if (input.format === "longform" && (input.longsInSameWeek ?? 0) >= maxLongs) {
    errors.push(`SCHEDULE BLOCKED: max ${maxLongs} long/week exceeded`);
  }

  return { ok: errors.length === 0, errors };
}
