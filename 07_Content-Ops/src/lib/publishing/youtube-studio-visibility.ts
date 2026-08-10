/**
 * Studio visibility taxonomy for YouTube catalogue audits.
 * Distinguishes PUBLIC / SCHEDULED / PRIVATE / DRAFT / PROCESSING / FAILED / UNKNOWN.
 *
 * Studio "Draft" Shorts may lack a normal /video/{id} link in the list row but
 * expose an underlying video id via edit URL query `udvid=`.
 * Drafts live under Content → Shorts (/videos/short), NOT Content → Videos (/videos/upload).
 */
export type StudioVisibilityClass =
  | "PUBLIC"
  | "SCHEDULED"
  | "PRIVATE"
  | "DRAFT"
  | "PROCESSING"
  | "FAILED_UPLOAD"
  | "UNKNOWN";

export type StudioRowLike = {
  title?: string | null;
  visibilityText?: string | null;
  dateText?: string | null;
  rawText?: string | null;
  videoId?: string | null;
  /** Underlying id from Studio draft edit URL (?udvid=) */
  udvid?: string | null;
  href?: string | null;
  uploadStatus?: string | null;
  privacyStatus?: string | null;
  publishAt?: string | null;
};

const HAS = (hay: string, re: RegExp) => re.test(hay);

/** Extract udvid from a Studio edit/list URL if present. */
export function extractStudioUdvid(url: string | null | undefined): string | null {
  if (!url) return null;
  const m = url.match(/[?&]udvid=([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

/** Extract /video/{id} from a Studio URL. */
export function extractStudioVideoId(url: string | null | undefined): string | null {
  if (!url) return null;
  const m = url.match(/\/video\/([A-Za-z0-9_-]{11})/);
  return m ? m[1] : null;
}

/**
 * Classify a Studio content row using UI labels + optional API fields.
 * Priority: DRAFT label > SCHEDULED > PUBLIC > PRIVATE > PROCESSING/FAILED > UNKNOWN.
 */
export function classifyStudioVisibility(row: StudioRowLike): StudioVisibilityClass {
  const blob = [row.visibilityText, row.dateText, row.rawText].filter(Boolean).join("\n");

  if (HAS(blob, /\bDraft\b/i) || HAS(row.visibilityText || "", /^draft$/i)) {
    return "DRAFT";
  }
  if (
    HAS(blob, /\bScheduled\b/i) ||
    (row.publishAt != null && row.publishAt !== "" && (row.privacyStatus === "private" || !row.privacyStatus))
  ) {
    // API scheduled holds are private+publishAt; UI shows Scheduled
    if (row.publishAt) return "SCHEDULED";
    if (HAS(blob, /\bScheduled\b/i)) return "SCHEDULED";
  }
  if (row.privacyStatus === "public" || HAS(blob, /\bPublic\b/i)) {
    // Avoid "Public" false positive inside other words — UI uses word boundary
    if (row.privacyStatus === "public") return "PUBLIC";
    if (HAS(blob, /\bPublic\b/i) && !HAS(blob, /\bPrivate\b/i)) return "PUBLIC";
  }
  if (row.privacyStatus === "private" || HAS(blob, /\bPrivate\b/i)) {
    if (row.publishAt) return "SCHEDULED";
    return "PRIVATE";
  }
  if (row.privacyStatus === "unlisted" || HAS(blob, /\bUnlisted\b/i)) {
    return "PRIVATE"; // treat unlisted as non-public protected bucket for this taxonomy
  }
  if (
    row.uploadStatus === "uploaded" ||
    row.uploadStatus === "processed" ||
    HAS(blob, /\bProcessing\b/i)
  ) {
    if (HAS(blob, /\bProcessing\b/i) || row.uploadStatus === "uploaded") return "PROCESSING";
  }
  if (row.uploadStatus === "failed" || HAS(blob, /\bFailed\b/i) || HAS(blob, /upload failed/i)) {
    return "FAILED_UPLOAD";
  }
  return "UNKNOWN";
}

/**
 * Resolve the best catalogue id for a Studio row.
 * Prefer explicit videoId, then udvid from draft edit URL, then href path id.
 */
export function resolveStudioCatalogueId(row: StudioRowLike): string | null {
  if (row.videoId) return row.videoId;
  if (row.udvid) return row.udvid;
  const fromHref = extractStudioVideoId(row.href || null) || extractStudioUdvid(row.href || null);
  return fromHref;
}

export type DraftEnumerationPaths = {
  /** Content → Videos draft filter results */
  videosUploadTabDraftCount: number;
  /** Content → Shorts draft filter results */
  shortsTabDraftCount: number;
};

/**
 * Explain / detect the Aug-2026 audit failure mode:
 * counting drafts only on /videos/upload yields 0 while Shorts drafts exist.
 */
export function diagnoseDraftAuditGap(paths: DraftEnumerationPaths): {
  previousAuditWouldReportZero: boolean;
  rootCause: "WRONG_STUDIO_TAB_FILTER" | "NO_DRAFTS" | "UNKNOWN";
  message: string;
} {
  if (paths.shortsTabDraftCount > 0 && paths.videosUploadTabDraftCount === 0) {
    return {
      previousAuditWouldReportZero: true,
      rootCause: "WRONG_STUDIO_TAB_FILTER",
      message:
        "Draft filter on Content → Videos (/videos/upload) is empty, but Content → Shorts (/videos/short) has Draft rows. Shorts drafts are tab-scoped.",
    };
  }
  if (paths.shortsTabDraftCount === 0 && paths.videosUploadTabDraftCount === 0) {
    return {
      previousAuditWouldReportZero: true,
      rootCause: "NO_DRAFTS",
      message: "Both Videos and Shorts Draft filters are empty.",
    };
  }
  return {
    previousAuditWouldReportZero: paths.videosUploadTabDraftCount === 0 && paths.shortsTabDraftCount === 0,
    rootCause: "UNKNOWN",
    message: "Draft counts present on one or both tabs.",
  };
}

/** Studio Private filter includes scheduled holds (privacyStatus=private). */
export function studioPrivateFilterIncludesScheduled(): boolean {
  return true;
}

export type CleanupGateInput = {
  classification:
    | "CANONICAL_SCHEDULED"
    | "CANONICAL_PUBLIC"
    | "HISTORICAL_DUPLICATE"
    | "SUPERSEDED_UPLOAD"
    | "TRUE_STUDIO_DRAFT"
    | "ORPHAN"
    | "PROTECTED_PRIVATE"
    | "UNKNOWN";
  confidence: "HIGH" | "MEDIUM" | "LOW";
  isPublic: boolean;
  isScheduled: boolean;
  inApproved13: boolean;
  isCanonicalId: boolean;
  hasConfirmedReplacement: boolean;
};

export function mayProposeHighConfidenceDelete(input: CleanupGateInput): boolean {
  if (input.confidence !== "HIGH") return false;
  if (input.isPublic || input.isScheduled || input.inApproved13 || input.isCanonicalId) return false;
  if (
    input.classification === "CANONICAL_PUBLIC" ||
    input.classification === "CANONICAL_SCHEDULED" ||
    input.classification === "PROTECTED_PRIVATE" ||
    input.classification === "UNKNOWN"
  ) {
    return false;
  }
  if (input.classification === "HISTORICAL_DUPLICATE" || input.classification === "SUPERSEDED_UPLOAD") {
    return input.hasConfirmedReplacement;
  }
  if (input.classification === "TRUE_STUDIO_DRAFT" || input.classification === "ORPHAN") {
    return true;
  }
  return false;
}

export function defaultProtectWhenUnknown(classification: string): boolean {
  return classification === "UNKNOWN" || classification === "ORPHAN";
}
