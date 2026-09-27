export type DuplicateCandidate = {
  id: string;
  shortClipId: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  platformUrl?: string | null;
  scheduledAt?: Date | null;
  publishedAt?: Date | null;
  fileChecksum?: string | null;
};

export type DuplicateCheckInput = {
  shortClipId: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  fileChecksum?: string | null;
  scheduledAt?: Date | null;
  existing: DuplicateCandidate[];
};

export type DuplicateWarning = {
  level: "block" | "warn";
  reason: string;
  matchedPostId: string;
};

const REPOST_REASONS = [
  "New hook",
  "New edit",
  "Seasonal repost",
  "Performance retest",
  "Updated information",
] as const;

export { REPOST_REASONS };

function normalize(s?: string | null): string {
  return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
}

export function detectDuplicates(input: DuplicateCheckInput): DuplicateWarning[] {
  const warnings: DuplicateWarning[] = [];
  for (const post of input.existing) {
    if (post.platform !== input.platform) continue;

    if (post.shortClipId === input.shortClipId) {
      warnings.push({
        level: "block",
        reason: "This clip is already tracked for this platform",
        matchedPostId: post.id,
      });
    }

    if (
      input.fileChecksum &&
      post.fileChecksum &&
      input.fileChecksum === post.fileChecksum
    ) {
      warnings.push({
        level: "block",
        reason: "Same video file checksum already used on this platform",
        matchedPostId: post.id,
      });
    }

    if (post.platformUrl) {
      warnings.push({
        level: "warn",
        reason: `Existing published URL on file: ${post.platformUrl}`,
        matchedPostId: post.id,
      });
    }

    const titleSame =
      normalize(input.title) &&
      normalize(input.title) === normalize(post.title);
    const captionSame =
      normalize(input.caption) &&
      normalize(input.caption) === normalize(post.caption);

    if (titleSame || captionSame) {
      warnings.push({
        level: "warn",
        reason: titleSame
          ? "Very similar title already exists for this platform"
          : "Very similar caption already exists for this platform",
        matchedPostId: post.id,
      });
    }

    if (input.scheduledAt && post.scheduledAt) {
      const diff = Math.abs(input.scheduledAt.getTime() - post.scheduledAt.getTime());
      if (diff < 60 * 60 * 1000 && (titleSame || captionSame || post.shortClipId === input.shortClipId)) {
        warnings.push({
          level: "warn",
          reason: "Similar post scheduled within one hour",
          matchedPostId: post.id,
        });
      }
    }
  }

  // de-dupe warnings by reason+id
  const seen = new Set<string>();
  return warnings.filter((w) => {
    const key = `${w.level}:${w.matchedPostId}:${w.reason}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export function canForceRepost(
  warnings: DuplicateWarning[],
  repostReason?: string | null,
): { ok: boolean; error?: string } {
  const blocking = warnings.some((w) => w.level === "block");
  if (!blocking) return { ok: true };
  if (!repostReason || !REPOST_REASONS.includes(repostReason as (typeof REPOST_REASONS)[number])) {
    return {
      ok: false,
      error: `Intentional repost requires a reason: ${REPOST_REASONS.join(", ")}`,
    };
  }
  return { ok: true };
}
