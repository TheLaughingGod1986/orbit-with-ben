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

export type IntendedShortSlot = {
  canonicalShortId: string;
  intendedPublishAt: string; // ISO UTC
  intentionallyCancelled?: boolean;
};

export type LiveShortState = {
  videoId: string;
  privacyStatus: string | null;
  publishAt: string | null;
  isHistoricalDuplicate?: boolean;
  isSuperseded?: boolean;
  hasPublicCanonicalEquivalent?: boolean;
};

export type IndependentEvidenceSource =
  | "ORIGINAL_PUBLISHING_PLAN"
  | "STUDIO_SCHEDULE_CAPTURE"
  | "UPLOAD_LOG"
  | "SOURCE_ASSET_MANIFEST"
  | "MUTATION_JOURNAL"
  | "GIT_HISTORY"
  | "CURRENT_REGISTRY"
  | "CURRENT_AUDIT";

export type PublicationIntentEvidence = {
  source: IndependentEvidenceSource;
  /** The video id directly supported by this evidence item. */
  videoId: string;
  intendedPublishAt?: string | null;
  observedPublic?: boolean;
  intentionalPrivate?: boolean;
  explicitReplacementVideoId?: string | null;
  sourceAssetFingerprint?: string | null;
};

const EVIDENCE_STRENGTH: Record<IndependentEvidenceSource, number> = {
  ORIGINAL_PUBLISHING_PLAN: 100,
  STUDIO_SCHEDULE_CAPTURE: 95,
  UPLOAD_LOG: 90,
  SOURCE_ASSET_MANIFEST: 85,
  MUTATION_JOURNAL: 80,
  GIT_HISTORY: 75,
  CURRENT_REGISTRY: 20,
  CURRENT_AUDIT: 10,
};

export type ReconstructedPublicationIntent = {
  state: "PUBLIC_BY_NOW" | "SCHEDULED_FUTURE" | "INTENTIONAL_PRIVATE" | "UNKNOWN";
  intendedPublishAt: string | null;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  decisiveSources: IndependentEvidenceSource[];
};

/**
 * Reconstruct intent without allowing a current registry/audit to validate itself.
 * Private is only intentional when independent, explicit evidence says so. A bare
 * private observation or KEEP_PRIVATE registry label is not publication intent.
 */
export function reconstructPublicationIntent(
  videoId: string,
  evidence: PublicationIntentEvidence[],
  now: Date = new Date(),
): ReconstructedPublicationIntent {
  const direct = evidence
    .filter((item) => item.videoId === videoId)
    .sort((a, b) => EVIDENCE_STRENGTH[b.source] - EVIDENCE_STRENGTH[a.source]);
  const independent = direct.filter(
    (item) => item.source !== "CURRENT_REGISTRY" && item.source !== "CURRENT_AUDIT",
  );

  const explicitPrivate = independent.find((item) => item.intentionalPrivate === true);
  const scheduled = independent.find((item) => Boolean(item.intendedPublishAt));
  const previouslyPublic = independent.find((item) => item.observedPublic === true);

  if (explicitPrivate && (!scheduled || EVIDENCE_STRENGTH[explicitPrivate.source] >= EVIDENCE_STRENGTH[scheduled.source])) {
    return {
      state: "INTENTIONAL_PRIVATE",
      intendedPublishAt: null,
      confidence: EVIDENCE_STRENGTH[explicitPrivate.source] >= 80 ? "HIGH" : "MEDIUM",
      decisiveSources: [explicitPrivate.source],
    };
  }

  if (scheduled?.intendedPublishAt) {
    const intended = scheduled.intendedPublishAt;
    return {
      state: new Date(intended) <= now ? "PUBLIC_BY_NOW" : "SCHEDULED_FUTURE",
      intendedPublishAt: intended,
      confidence: EVIDENCE_STRENGTH[scheduled.source] >= 85 ? "HIGH" : "MEDIUM",
      decisiveSources: [scheduled.source],
    };
  }

  if (previouslyPublic) {
    return {
      state: "PUBLIC_BY_NOW",
      intendedPublishAt: null,
      confidence: EVIDENCE_STRENGTH[previouslyPublic.source] >= 85 ? "HIGH" : "MEDIUM",
      decisiveSources: [previouslyPublic.source],
    };
  }

  return {
    state: "UNKNOWN",
    intendedPublishAt: null,
    confidence: "LOW",
    decisiveSources: direct.slice(0, 1).map((item) => item.source),
  };
}

export type ContentIdentityEvidence = {
  leftVideoId: string;
  rightVideoId: string;
  exactSourceAssetFingerprintMatch?: boolean;
  explicitReplacementMapping?: boolean;
  sameTitle?: boolean;
  similarTitle?: boolean;
  sameParentLong?: boolean;
};

/** Similar titles and a shared parent describe a topic, not an upload identity. */
export function classifyContentIdentity(
  evidence: ContentIdentityEvidence,
): "EXACT_DUPLICATE" | "SUPERSEDED_RENDER" | "UNPROVEN" {
  if (evidence.exactSourceAssetFingerprintMatch) return "EXACT_DUPLICATE";
  if (evidence.explicitReplacementMapping) return "SUPERSEDED_RENDER";
  return "UNPROVEN";
}

/**
 * Expected state from intended publish time vs now.
 * Cancelled slots stay private intentionally.
 */
export function expectedStateFromIntent(
  intendedPublishAt: string,
  now: Date = new Date(),
  intentionallyCancelled = false,
): "PUBLIC" | "SCHEDULED" | "PRIVATE_INTENTIONAL" {
  if (intentionallyCancelled) return "PRIVATE_INTENTIONAL";
  return new Date(intendedPublishAt) <= now ? "PUBLIC" : "SCHEDULED";
}

/**
 * HIGH-confidence overdue canonical publish candidate.
 * All gates must pass — title similarity is not an input here.
 */
export function isOverdueCanonicalPublishCandidate(
  slot: IntendedShortSlot,
  live: LiveShortState,
  now: Date = new Date(),
): boolean {
  if (slot.intentionallyCancelled) return false;
  if (slot.canonicalShortId !== live.videoId) return false;
  if (live.isHistoricalDuplicate || live.isSuperseded) return false;
  if (live.hasPublicCanonicalEquivalent) return false;
  if (new Date(slot.intendedPublishAt) > now) return false;
  if (live.privacyStatus === "public" && !live.publishAt) return false;
  // Stuck private with no future hold, or past-due publishAt still attached
  if (live.privacyStatus === "private" && !live.publishAt) return true;
  if (live.publishAt && new Date(live.publishAt) <= now) return true;
  return false;
}

/** Cleanup / repair scripts must default to no live mutation. */
export function defaultMutationMode(): "NO_MUTATION" {
  return "NO_MUTATION";
}

/** Natural publication of a scheduled ID must not be treated as schedule damage. */
export function isNaturalSchedulePublication(args: {
  videoId: string;
  expectedPublishAt: string;
  nowPrivacy: string | null;
  nowPublishAt: string | null;
  now: Date;
}): boolean {
  if (args.nowPrivacy !== "public") return false;
  if (args.nowPublishAt) return false;
  return new Date(args.expectedPublishAt) <= args.now;
}

/** Future scheduled rows must keep exact publishAt — cleanup must not clear it. */
export function schedulePublishAtProtected(
  beforePublishAt: string | null,
  afterPublishAt: string | null,
  intendedFuture: boolean,
): boolean {
  if (!intendedFuture) return true;
  return beforePublishAt === afterPublishAt && beforePublishAt != null;
}

/**
 * Studio Shorts list chips can disagree with the video edit page / Data API.
 * When API privacy is present, it wins over a conflicting list label.
 */
export function resolveAuthoritativeVisibility(input: {
  studioListLabel?: string | null;
  apiPrivacyStatus?: string | null;
  apiPublishAt?: string | null;
}): StudioVisibilityClass {
  const api = (input.apiPrivacyStatus || "").toLowerCase();
  if (api === "public") return "PUBLIC";
  if (api === "private" && input.apiPublishAt) return "SCHEDULED";
  if (api === "private") return "PRIVATE";
  if (api === "unlisted") return "PRIVATE";
  return classifyStudioVisibility({
    visibilityText: input.studioListLabel,
    privacyStatus: input.apiPrivacyStatus,
    publishAt: input.apiPublishAt,
  });
}

/** This forensic repair must never demote a live public Short. */
export function mayDemotePublicShort(): boolean {
  return false;
}

/**
 * Only HIGH-confidence overdue canonical PRIVATE→PUBLIC is auto-allowed.
 * Everything else (including unexpected public superseded) stays NO_MUTATION.
 */
export function proposedVisibilityMutationAllowed(input: {
  from: StudioVisibilityClass;
  to: StudioVisibilityClass;
  overdueCanonicalHighConfidence: boolean;
}): boolean {
  if (input.from === "PUBLIC") return false;
  if (input.from === "SCHEDULED") return false;
  if (input.from === "PRIVATE" && input.to === "PUBLIC") {
    return input.overdueCanonicalHighConfidence === true;
  }
  return false;
}

/**
 * Pagination completeness: discovered row count must equal reported total when known.
 * Do not hardcode 62 — Studio can grow/shrink.
 */
export function studioShortsPaginationComplete(input: {
  enumeratedRowCount: number;
  studioReportedTotal?: number | null;
  pagesVisited: number;
}): boolean {
  if (input.enumeratedRowCount <= 0) return false;
  if (input.pagesVisited < 1) return false;
  if (input.studioReportedTotal == null) return input.enumeratedRowCount > 0;
  return input.enumeratedRowCount === input.studioReportedTotal;
}
