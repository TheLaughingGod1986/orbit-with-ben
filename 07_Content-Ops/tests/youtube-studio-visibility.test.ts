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
});
