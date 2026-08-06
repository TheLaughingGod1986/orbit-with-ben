/**
 * Orbit YouTube recovery-mode enforcement (7-day stabilization).
 */
import fs from "fs";
import path from "path";

export type YouTubeRecoveryConfig = {
  recoveryMode: boolean;
  startedAt: string;
  timezone: string;
  durationDays: number;
  maxShortsPerDay: number;
  maxLongsDuringRecovery: number;
  replacementUploadsAllowed: boolean;
  duplicateUploadsAllowed: boolean;
  bulkMetadataUpdatesAllowed: boolean;
  deleteAndReuploadAllowed: boolean;
  minimumEvaluationWindowHours: number;
  heldVideoIds: string[];
  canonicalPublicIds: string[];
  notes?: string;
};

export type RecoveryGateInput = {
  config: YouTubeRecoveryConfig;
  now?: Date;
  format: "longform" | "shorts";
  /** Count of Shorts that already went public (or will go public) on this calendar day in the recovery timezone. */
  shortsPublishedOrScheduledToday: number;
  /** Count of new long-form uploads created during the recovery window (API inserts). */
  longsUploadedDuringRecovery: number;
  isReplacementUpload: boolean;
  isDuplicateFingerprint: boolean;
  alreadyHasCanonicalVideoId: boolean;
  canonicalVideoId?: string | null;
  targetVideoId?: string | null;
  wouldMutateHeldVideo?: boolean;
  /** True when another scheduled upload shares the same publish minute. */
  scheduleCollision?: boolean;
  scheduleCollisionWith?: string | null;
};

export type RecoveryGateResult = {
  ok: boolean;
  blocked: boolean;
  errors: string[];
  warnings: string[];
  recoveryActive: boolean;
  endsAt: string | null;
};

const DEFAULT_RELATIVE = path.join(
  "..",
  "00_Brand",
  "Channel-Setup",
  "YOUTUBE_RECOVERY_MODE.json",
);

export function resolveRecoveryConfigPath(fromCwd = process.cwd()): string {
  const candidates = [
    path.resolve(fromCwd, DEFAULT_RELATIVE),
    path.resolve(fromCwd, "00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json"),
    path.resolve(fromCwd, "../00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json"),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return candidates[0];
}

export function loadYouTubeRecoveryConfig(configPath?: string): YouTubeRecoveryConfig {
  const p = configPath || resolveRecoveryConfigPath();
  if (!fs.existsSync(p)) {
    throw new Error(`Recovery config not found: ${p}`);
  }
  return JSON.parse(fs.readFileSync(p, "utf8")) as YouTubeRecoveryConfig;
}

export function recoveryWindowEnd(config: YouTubeRecoveryConfig): Date {
  const start = new Date(config.startedAt);
  return new Date(start.getTime() + config.durationDays * 24 * 60 * 60 * 1000);
}

export function isRecoveryActive(config: YouTubeRecoveryConfig, now = new Date()): boolean {
  if (!config.recoveryMode) return false;
  return now.getTime() < recoveryWindowEnd(config).getTime();
}

/** Calendar day key in a fixed offset approximation for Europe/Paris (UTC+1/+2). Uses Intl when available. */
export function calendarDayKey(now: Date, timeZone: string): string {
  try {
    return new Intl.DateTimeFormat("en-CA", {
      timeZone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).format(now);
  } catch {
    return now.toISOString().slice(0, 10);
  }
}

export function evaluateRecoveryGate(input: RecoveryGateInput): RecoveryGateResult {
  const now = input.now || new Date();
  const errors: string[] = [];
  const warnings: string[] = [];
  const active = isRecoveryActive(input.config, now);
  const endsAt = active ? recoveryWindowEnd(input.config).toISOString() : null;

  if (!active) {
    return { ok: true, blocked: false, errors, warnings, recoveryActive: false, endsAt: null };
  }

  if (input.wouldMutateHeldVideo) {
    errors.push(
      "UPLOAD BLOCKED: Held recovery videos (31 Dec holds) must not be altered by automation.",
    );
  }

  if (!input.config.replacementUploadsAllowed && input.isReplacementUpload) {
    errors.push("UPLOAD BLOCKED: Replacement uploads are forbidden during recovery mode.");
  }

  if (!input.config.duplicateUploadsAllowed && input.isDuplicateFingerprint) {
    errors.push(
      "UPLOAD BLOCKED: Duplicate source fingerprint detected during recovery mode.",
    );
  }

  if (!input.config.deleteAndReuploadAllowed && input.isReplacementUpload) {
    errors.push("UPLOAD BLOCKED: Delete-and-reupload is forbidden during recovery mode.");
  }

  if (input.alreadyHasCanonicalVideoId) {
    errors.push(
      `UPLOAD BLOCKED: This content package is already mapped to YouTube video ${input.canonicalVideoId || "(unknown)"}. Use the canonical update workflow instead.`,
    );
  }

  if (input.format === "shorts") {
    if (input.shortsPublishedOrScheduledToday >= input.config.maxShortsPerDay) {
      errors.push(
        `UPLOAD BLOCKED: Recovery mode permits a maximum of ${input.config.maxShortsPerDay} Short per day.`,
      );
    }
  }

  if (input.format === "longform") {
    if (input.longsUploadedDuringRecovery >= input.config.maxLongsDuringRecovery) {
      errors.push(
        `UPLOAD BLOCKED: Recovery mode permits at most ${input.config.maxLongsDuringRecovery} new long-form upload(s).`,
      );
    }
  }

  if (input.targetVideoId && input.config.heldVideoIds.includes(input.targetVideoId)) {
    errors.push(
      `UPLOAD BLOCKED: Video ${input.targetVideoId} is on the held list until recovery ends.`,
    );
  }

  if (input.scheduleCollision) {
    errors.push(
      `UPLOAD BLOCKED: Schedule collision with ${input.scheduleCollisionWith || "an existing upload"} — choose a different publishAt.`,
    );
  }

  return {
    ok: errors.length === 0,
    blocked: errors.length > 0,
    errors,
    warnings,
    recoveryActive: true,
    endsAt,
  };
}

/** Same UTC minute = collision (duplicate slot risk). */
export function findScheduleCollision(input: {
  proposedPublishAt: Date | string | null | undefined;
  existing: { youtubeVideoId: string; scheduledPublishTimestamp: string | null }[];
}): { collision: boolean; withVideoId: string | null } {
  if (!input.proposedPublishAt) return { collision: false, withVideoId: null };
  const proposed = new Date(input.proposedPublishAt).getTime();
  if (!Number.isFinite(proposed)) return { collision: false, withVideoId: null };
  const proposedMinute = Math.floor(proposed / 60_000);
  for (const row of input.existing) {
    if (!row.scheduledPublishTimestamp) continue;
    const t = new Date(row.scheduledPublishTimestamp).getTime();
    if (!Number.isFinite(t)) continue;
    if (Math.floor(t / 60_000) === proposedMinute) {
      return { collision: true, withVideoId: row.youtubeVideoId };
    }
  }
  return { collision: false, withVideoId: null };
}

/**
 * Ambiguous upload handling: never blind-retry when a video ID may already exist.
 * Returns whether a retry is allowed.
 */
export function shouldRetryUncertainUpload(input: {
  confirmedVideoId: string | null | undefined;
  searchHitsMatchingTitle: { id: string }[];
}): { retryAllowed: boolean; reason: string } {
  if (input.confirmedVideoId) {
    return {
      retryAllowed: false,
      reason: `UPLOAD BLOCKED: Video ID ${input.confirmedVideoId} already exists — do not create a replacement.`,
    };
  }
  if (input.searchHitsMatchingTitle.length > 0) {
    return {
      retryAllowed: false,
      reason: `UPLOAD BLOCKED: Channel search found ${input.searchHitsMatchingTitle.length} possible match(es). Inspect before any retry.`,
    };
  }
  return {
    retryAllowed: true,
    reason: "No confirmed video ID and no search matches — cautious single retry may proceed.",
  };
}
