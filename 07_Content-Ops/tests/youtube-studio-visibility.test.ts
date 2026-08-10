import { describe, expect, it } from "vitest";
import {
  classifyStudioVisibility,
  diagnoseDraftAuditGap,
  extractStudioUdvid,
  extractStudioVideoId,
  mayProposeHighConfidenceDelete,
  resolveStudioCatalogueId,
  studioPrivateFilterIncludesScheduled,
  defaultProtectWhenUnknown,
  expectedStateFromIntent,
  isOverdueCanonicalPublishCandidate,
  defaultMutationMode,
  isNaturalSchedulePublication,
  schedulePublishAtProtected,
  reconstructPublicationIntent,
  classifyContentIdentity,
  resolveAuthoritativeVisibility,
  mayDemotePublicShort,
  proposedVisibilityMutationAllowed,
  studioShortsPaginationComplete,
} from "../src/lib/publishing/youtube-studio-visibility";

describe("youtube-studio-visibility", () => {
  it("classifies Draft from Studio label even without videoId", () => {
    expect(
      classifyStudioVisibility({
        title: "Cross This Line and You Never Come Back",
        visibilityText: "Draft",
        rawText: "0:45\nCross This Line\nDraft\nEdit draft",
        videoId: null,
      }),
    ).toBe("DRAFT");
  });

  it("classifies Scheduled from date text or publishAt", () => {
    expect(
      classifyStudioVisibility({
        title: "Would You Look Back?",
        dateText: "Scheduled for 11 Aug 2026",
        rawText: "Would You Look Back?\nScheduled",
        privacyStatus: "private",
        publishAt: "2026-08-11T10:30:00Z",
      }),
    ).toBe("SCHEDULED");
  });

  it("classifies Public and Private", () => {
    expect(
      classifyStudioVisibility({
        privacyStatus: "public",
        visibilityText: "Public",
      }),
    ).toBe("PUBLIC");
    expect(
      classifyStudioVisibility({
        privacyStatus: "private",
        publishAt: null,
        visibilityText: "Private",
      }),
    ).toBe("PRIVATE");
  });

  it("extracts udvid from draft edit URLs", () => {
    const url =
      "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short?filter=%5B%5D&udvid=z-kgwJaz5pY";
    expect(extractStudioUdvid(url)).toBe("z-kgwJaz5pY");
    expect(extractStudioVideoId("https://studio.youtube.com/video/3xrxdmaOwJI/edit")).toBe(
      "3xrxdmaOwJI",
    );
  });

  it("resolves catalogue id preferring videoId then udvid", () => {
    expect(resolveStudioCatalogueId({ videoId: "abcABCabcAB", udvid: "xyzXYZxyzXY" })).toBe(
      "abcABCabcAB",
    );
    expect(
      resolveStudioCatalogueId({
        videoId: null,
        href: "https://studio.youtube.com/...?udvid=z8-haBeF6mI",
      }),
    ).toBe("z8-haBeF6mI");
  });

  it("diagnoses previous Drafts=0 as wrong Studio tab filter", () => {
    const d = diagnoseDraftAuditGap({
      videosUploadTabDraftCount: 0,
      shortsTabDraftCount: 15,
    });
    expect(d.previousAuditWouldReportZero).toBe(true);
    expect(d.rootCause).toBe("WRONG_STUDIO_TAB_FILTER");
  });

  it("documents that Studio Private filter includes scheduled holds", () => {
    expect(studioPrivateFilterIncludesScheduled()).toBe(true);
  });

  it("unknown defaults to protect", () => {
    expect(defaultProtectWhenUnknown("UNKNOWN")).toBe(true);
    expect(defaultProtectWhenUnknown("ORPHAN")).toBe(true);
    expect(defaultProtectWhenUnknown("TRUE_STUDIO_DRAFT")).toBe(false);
  });

  it("gates SAFE_TO_DELETE_HIGH_CONFIDENCE proposals", () => {
    expect(
      mayProposeHighConfidenceDelete({
        classification: "HISTORICAL_DUPLICATE",
        confidence: "HIGH",
        isPublic: false,
        isScheduled: false,
        inApproved13: false,
        isCanonicalId: false,
        hasConfirmedReplacement: true,
      }),
    ).toBe(true);

    expect(
      mayProposeHighConfidenceDelete({
        classification: "HISTORICAL_DUPLICATE",
        confidence: "MEDIUM",
        isPublic: false,
        isScheduled: false,
        inApproved13: false,
        isCanonicalId: false,
        hasConfirmedReplacement: true,
      }),
    ).toBe(false);

    expect(
      mayProposeHighConfidenceDelete({
        classification: "CANONICAL_SCHEDULED",
        confidence: "HIGH",
        isPublic: false,
        isScheduled: true,
        inApproved13: true,
        isCanonicalId: true,
        hasConfirmedReplacement: false,
      }),
    ).toBe(false);

    expect(
      mayProposeHighConfidenceDelete({
        classification: "UNKNOWN",
        confidence: "HIGH",
        isPublic: false,
        isScheduled: false,
        inApproved13: false,
        isCanonicalId: false,
        hasConfirmedReplacement: false,
      }),
    ).toBe(false);
  });

  it("classifies PROCESSING and FAILED_UPLOAD", () => {
    expect(
      classifyStudioVisibility({
        rawText: "Processing",
        uploadStatus: "uploaded",
      }),
    ).toBe("PROCESSING");
    expect(
      classifyStudioVisibility({
        uploadStatus: "failed",
        rawText: "Failed",
      }),
    ).toBe("FAILED_UPLOAD");
  });

  it("computes expected PUBLIC vs SCHEDULED from intendedPublishAt", () => {
    const now = new Date("2026-08-10T12:00:00Z");
    expect(expectedStateFromIntent("2026-08-10T10:30:00Z", now)).toBe("PUBLIC");
    expect(expectedStateFromIntent("2026-08-11T10:30:00Z", now)).toBe("SCHEDULED");
    expect(expectedStateFromIntent("2026-08-01T00:00:00Z", now, true)).toBe("PRIVATE_INTENTIONAL");
  });

  it("flags overdue canonical private and blocks duplicates / future", () => {
    const now = new Date("2026-08-10T12:00:00Z");
    const slot = { canonicalShortId: "tUAdhOnMW2g", intendedPublishAt: "2026-08-10T10:30:00Z" };
    expect(
      isOverdueCanonicalPublishCandidate(slot, {
        videoId: "tUAdhOnMW2g",
        privacyStatus: "private",
        publishAt: null,
      }, now),
    ).toBe(true);
    expect(
      isOverdueCanonicalPublishCandidate(slot, {
        videoId: "tUAdhOnMW2g",
        privacyStatus: "public",
        publishAt: null,
      }, now),
    ).toBe(false);
    expect(
      isOverdueCanonicalPublishCandidate(
        { canonicalShortId: "svYOx07OrIM", intendedPublishAt: "2026-08-11T10:30:00Z" },
        { videoId: "svYOx07OrIM", privacyStatus: "private", publishAt: "2026-08-11T10:30:00Z" },
        now,
      ),
    ).toBe(false);
    expect(
      isOverdueCanonicalPublishCandidate(slot, {
        videoId: "tUAdhOnMW2g",
        privacyStatus: "private",
        publishAt: null,
        isHistoricalDuplicate: true,
      }, now),
    ).toBe(false);
  });

  it("defaults cleanup to NO_MUTATION and protects future publishAt", () => {
    expect(defaultMutationMode()).toBe("NO_MUTATION");
    expect(
      schedulePublishAtProtected("2026-08-11T10:30:00Z", "2026-08-11T10:30:00Z", true),
    ).toBe(true);
    expect(schedulePublishAtProtected("2026-08-11T10:30:00Z", null, true)).toBe(false);
  });

  it("treats natural schedule fire as healthy, not schedule damage", () => {
    expect(
      isNaturalSchedulePublication({
        videoId: "tUAdhOnMW2g",
        expectedPublishAt: "2026-08-10T10:30:00Z",
        nowPrivacy: "public",
        nowPublishAt: null,
        now: new Date("2026-08-10T12:00:00Z"),
      }),
    ).toBe(true);
  });

  it("private does not mean intentional private", () => {
    const result = reconstructPublicationIntent(
      "dPMJQp2gMNc",
      [{ source: "CURRENT_AUDIT", videoId: "dPMJQp2gMNc", intentionalPrivate: true }],
      new Date("2026-08-10T12:00:00Z"),
    );
    expect(result.state).toBe("UNKNOWN");
    expect(result.confidence).toBe("LOW");
  });

  it("similar title does not prove duplicate", () => {
    expect(
      classifyContentIdentity({
        leftVideoId: "w1ej9u0rPTA",
        rightVideoId: "JRfhE6yWom4",
        similarTitle: true,
      }),
    ).toBe("UNPROVEN");
  });

  it("same parent does not prove duplicate", () => {
    expect(
      classifyContentIdentity({
        leftVideoId: "w1ej9u0rPTA",
        rightVideoId: "JRfhE6yWom4",
        sameParentLong: true,
      }),
    ).toBe("UNPROVEN");
  });

  it("current registry cannot override stronger independent publication evidence", () => {
    const result = reconstructPublicationIntent(
      "dPMJQp2gMNc",
      [
        {
          source: "ORIGINAL_PUBLISHING_PLAN",
          videoId: "dPMJQp2gMNc",
          intendedPublishAt: "2026-08-01T11:30:00Z",
        },
        { source: "UPLOAD_LOG", videoId: "dPMJQp2gMNc", observedPublic: true },
        { source: "CURRENT_REGISTRY", videoId: "dPMJQp2gMNc", intentionalPrivate: true },
      ],
      new Date("2026-08-10T12:00:00Z"),
    );
    expect(result.state).toBe("PUBLIC_BY_NOW");
    expect(result.confidence).toBe("HIGH");
    expect(result.decisiveSources).toEqual(["ORIGINAL_PUBLISHING_PLAN"]);
  });

  it("accepts only fingerprint identity or explicit replacement evidence", () => {
    expect(
      classifyContentIdentity({
        leftVideoId: "old",
        rightVideoId: "new",
        exactSourceAssetFingerprintMatch: true,
      }),
    ).toBe("EXACT_DUPLICATE");
    expect(
      classifyContentIdentity({
        leftVideoId: "old",
        rightVideoId: "new",
        explicitReplacementMapping: true,
      }),
    ).toBe("SUPERSEDED_RENDER");
  });

  it("prefers API over conflicting Studio list Private label", () => {
    expect(
      resolveAuthoritativeVisibility({
        studioListLabel: "Private",
        apiPrivacyStatus: "public",
        apiPublishAt: null,
      }),
    ).toBe("PUBLIC");
    expect(
      resolveAuthoritativeVisibility({
        studioListLabel: "Private",
        apiPrivacyStatus: "private",
        apiPublishAt: "2026-08-11T10:30:00Z",
      }),
    ).toBe("SCHEDULED");
  });

  it("never demotes public Shorts and only allows overdue Private→Public", () => {
    expect(mayDemotePublicShort()).toBe(false);
    expect(
      proposedVisibilityMutationAllowed({
        from: "PUBLIC",
        to: "PRIVATE",
        overdueCanonicalHighConfidence: true,
      }),
    ).toBe(false);
    expect(
      proposedVisibilityMutationAllowed({
        from: "SCHEDULED",
        to: "PUBLIC",
        overdueCanonicalHighConfidence: true,
      }),
    ).toBe(false);
    expect(
      proposedVisibilityMutationAllowed({
        from: "PRIVATE",
        to: "PUBLIC",
        overdueCanonicalHighConfidence: false,
      }),
    ).toBe(false);
    expect(
      proposedVisibilityMutationAllowed({
        from: "PRIVATE",
        to: "PUBLIC",
        overdueCanonicalHighConfidence: true,
      }),
    ).toBe(true);
  });

  it("requires full Shorts pagination without hardcoding 62", () => {
    expect(
      studioShortsPaginationComplete({
        enumeratedRowCount: 62,
        studioReportedTotal: 62,
        pagesVisited: 3,
      }),
    ).toBe(true);
    expect(
      studioShortsPaginationComplete({
        enumeratedRowCount: 30,
        studioReportedTotal: 62,
        pagesVisited: 1,
      }),
    ).toBe(false);
    expect(
      studioShortsPaginationComplete({
        enumeratedRowCount: 70,
        studioReportedTotal: 70,
        pagesVisited: 3,
      }),
    ).toBe(true);
  });

  it("leaves ambiguous private untouched (no overdue gate)", () => {
    const now = new Date("2026-08-10T12:00:00Z");
    // Private with no independent intended publish → reconstruct UNKNOWN → not overdue
    const intent = reconstructPublicationIntent(
      "IsPLdq0oSe8",
      [{ source: "CURRENT_REGISTRY", videoId: "IsPLdq0oSe8", intentionalPrivate: true }],
      now,
    );
    expect(intent.state).toBe("UNKNOWN");
    expect(
      isOverdueCanonicalPublishCandidate(
        { canonicalShortId: "IsPLdq0oSe8", intendedPublishAt: "2026-08-01T00:00:00Z" },
        {
          videoId: "IsPLdq0oSe8",
          privacyStatus: "private",
          publishAt: null,
          isSuperseded: true,
        },
        now,
      ),
    ).toBe(false);
  });
});
