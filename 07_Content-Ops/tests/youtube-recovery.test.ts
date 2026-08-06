import { describe, expect, it } from "vitest";
import fs from "fs";
import path from "path";
import {
  classifyOAuthHttpError,
  hasForceSslScope,
  missingRequiredScopes,
  parseGrantedScopes,
  scopesFromTokenResponse,
} from "../src/lib/publishing/youtube-oauth";
import {
  calendarDayKey,
  evaluateRecoveryGate,
  findScheduleCollision,
  isRecoveryActive,
  recoveryWindowEnd,
  shouldRetryUncertainUpload,
  type YouTubeRecoveryConfig,
} from "../src/lib/publishing/youtube-recovery";
import {
  lookupCanonicalConflicts,
  seedOrbitCanonicalRecords,
  upsertCanonicalRecord,
  type CanonicalRegistryFile,
} from "../src/lib/publishing/youtube-registry";
import { assertYouTubeVideoState } from "../src/lib/publishing/adapters/youtube";

const recoveryBase: YouTubeRecoveryConfig = {
  recoveryMode: true,
  startedAt: "2026-08-07T00:00:00+02:00",
  timezone: "Europe/Paris",
  durationDays: 7,
  maxShortsPerDay: 1,
  maxLongsDuringRecovery: 0,
  replacementUploadsAllowed: false,
  duplicateUploadsAllowed: false,
  bulkMetadataUpdatesAllowed: false,
  deleteAndReuploadAllowed: false,
  minimumEvaluationWindowHours: 72,
  heldVideoIds: ["2C-eiSMsBLc"],
  canonicalPublicIds: ["3xrxdmaOwJI"],
};

describe("youtube oauth scopes", () => {
  it("detects force-ssl presence and gaps", () => {
    expect(hasForceSslScope(["https://www.googleapis.com/auth/youtube.upload"])).toBe(false);
    expect(
      hasForceSslScope([
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
      ]),
    ).toBe(true);
    expect(
      missingRequiredScopes(["https://www.googleapis.com/auth/youtube.upload"]).length,
    ).toBeGreaterThan(0);
  });

  it("parses granted scopes from JSON or space lists", () => {
    expect(parseGrantedScopes(JSON.stringify(["a", "b"]))).toEqual(["a", "b"]);
    expect(parseGrantedScopes("a b c")).toEqual(["a", "b", "c"]);
    expect(scopesFromTokenResponse("x y")).toEqual(["x", "y"]);
  });

  it("classifies oauth http failures", () => {
    expect(classifyOAuthHttpError(403, "ACCESS_TOKEN_SCOPE_INSUFFICIENT")).toBe("missing_scope");
    expect(classifyOAuthHttpError(401, "invalid_grant revoked")).toBe("revoked_token");
    expect(classifyOAuthHttpError(401, "token expired")).toBe("expired_token");
    expect(classifyOAuthHttpError(400, "invalid_client")).toBe("invalid_client");
  });
});

describe("youtube recovery gates", () => {
  it("blocks more than one Short per day", () => {
    const r = evaluateRecoveryGate({
      config: recoveryBase,
      now: new Date("2026-08-08T12:00:00+02:00"),
      format: "shorts",
      shortsPublishedOrScheduledToday: 1,
      longsUploadedDuringRecovery: 0,
      isReplacementUpload: false,
      isDuplicateFingerprint: false,
      alreadyHasCanonicalVideoId: false,
    });
    expect(r.blocked).toBe(true);
    expect(r.errors[0]).toContain("maximum of 1 Short per day");
  });

  it("blocks replacement uploads and held mutations", () => {
    const r = evaluateRecoveryGate({
      config: recoveryBase,
      now: new Date("2026-08-08T12:00:00+02:00"),
      format: "shorts",
      shortsPublishedOrScheduledToday: 0,
      longsUploadedDuringRecovery: 0,
      isReplacementUpload: true,
      isDuplicateFingerprint: true,
      alreadyHasCanonicalVideoId: true,
      canonicalVideoId: "JRfhE6yWom4",
      wouldMutateHeldVideo: true,
      targetVideoId: "2C-eiSMsBLc",
    });
    expect(r.blocked).toBe(true);
    expect(r.errors.some((e) => e.includes("Replacement"))).toBe(true);
    expect(r.errors.some((e) => e.includes("already mapped"))).toBe(true);
    expect(r.errors.some((e) => e.includes("held"))).toBe(true);
  });

  it("allows inactive recovery mode", () => {
    const r = evaluateRecoveryGate({
      config: { ...recoveryBase, recoveryMode: false },
      format: "shorts",
      shortsPublishedOrScheduledToday: 5,
      longsUploadedDuringRecovery: 5,
      isReplacementUpload: true,
      isDuplicateFingerprint: true,
      alreadyHasCanonicalVideoId: true,
    });
    expect(r.ok).toBe(true);
    expect(r.recoveryActive).toBe(false);
  });

  it("computes recovery window end", () => {
    const end = recoveryWindowEnd(recoveryBase);
    expect(isRecoveryActive(recoveryBase, new Date("2026-08-08T00:00:00+02:00"))).toBe(true);
    expect(isRecoveryActive(recoveryBase, new Date(end.getTime() + 1000))).toBe(false);
  });

  it("formats calendar day keys", () => {
    expect(calendarDayKey(new Date("2026-08-07T10:30:00Z"), "Europe/Paris")).toMatch(/2026-08-07/);
  });

  it("blocks schedule collisions in the same UTC minute", () => {
    const hit = findScheduleCollision({
      proposedPublishAt: "2026-08-07T10:30:00Z",
      existing: [
        { youtubeVideoId: "tUAdhOnMW2g", scheduledPublishTimestamp: "2026-08-07T10:30:00.000Z" },
      ],
    });
    expect(hit.collision).toBe(true);
    expect(hit.withVideoId).toBe("tUAdhOnMW2g");

    const r = evaluateRecoveryGate({
      config: recoveryBase,
      now: new Date("2026-08-08T12:00:00+02:00"),
      format: "shorts",
      shortsPublishedOrScheduledToday: 0,
      longsUploadedDuringRecovery: 0,
      isReplacementUpload: false,
      isDuplicateFingerprint: false,
      alreadyHasCanonicalVideoId: false,
      scheduleCollision: true,
      scheduleCollisionWith: "tUAdhOnMW2g",
    });
    expect(r.blocked).toBe(true);
    expect(r.errors[0]).toContain("Schedule collision");
  });

  it("never retries after a video ID is confirmed or search finds a match", () => {
    expect(
      shouldRetryUncertainUpload({
        confirmedVideoId: "JRfhE6yWom4",
        searchHitsMatchingTitle: [],
      }).retryAllowed,
    ).toBe(false);
    expect(
      shouldRetryUncertainUpload({
        confirmedVideoId: null,
        searchHitsMatchingTitle: [{ id: "abc" }],
      }).retryAllowed,
    ).toBe(false);
    expect(
      shouldRetryUncertainUpload({
        confirmedVideoId: null,
        searchHitsMatchingTitle: [],
      }).retryAllowed,
    ).toBe(true);
  });
});

describe("canonical registry", () => {
  it("blocks duplicate internal id / fingerprint / video id", () => {
    const registry: CanonicalRegistryFile = {
      version: 1,
      updatedAt: new Date().toISOString(),
      records: seedOrbitCanonicalRecords(),
    };
    expect(
      lookupCanonicalConflicts({ registry, internalContentId: "v002-bh-short-01" }).blocked,
    ).toBe(true);
    expect(
      lookupCanonicalConflicts({ registry, sourceFileFingerprint: "seed:JRfhE6yWom4" }).reason,
    ).toContain("JRfhE6yWom4");
    expect(lookupCanonicalConflicts({ registry, youtubeVideoId: "3xrxdmaOwJI" }).blocked).toBe(
      true,
    );
  });

  it("refuses silent canonical id replacement", () => {
    const registry: CanonicalRegistryFile = {
      version: 1,
      updatedAt: new Date().toISOString(),
      records: seedOrbitCanonicalRecords(),
    };
    expect(() =>
      upsertCanonicalRecord(registry, {
        ...seedOrbitCanonicalRecords()[4],
        youtubeVideoId: "NEWID12345",
      }),
    ).toThrow(/Refusing to replace canonical YouTube ID/);
  });
});

describe("assertYouTubeVideoState (mocked)", () => {
  it("fails closed when privacy mismatches", async () => {
    const original = global.fetch;
    global.fetch = (async () =>
      ({
        ok: true,
        json: async () => ({
          items: [
            {
              id: "abc",
              status: { privacyStatus: "private", uploadStatus: "processed" },
              snippet: { tags: ["a", "b", "c", "d", "e", "f"], description: "x".repeat(100) },
              processingDetails: { processingStatus: "succeeded" },
            },
          ],
        }),
      }) as Response) as typeof fetch;
    try {
      const r = await assertYouTubeVideoState({
        accessToken: "x",
        videoId: "abc",
        expectPrivacy: "public",
      });
      expect(r.ok).toBe(false);
      expect(r.errors.some((e) => e.includes("privacyStatus"))).toBe(true);
    } finally {
      global.fetch = original;
    }
  });
});

describe("quarantined CDP scripts", () => {
  const scheduleDir = path.resolve(
    process.cwd(),
    "../02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/11_Upload-Package/Schedule",
  );

  const names = [
    "DISABLED__upload_smooth_cfr_v01.py",
    "DISABLED__upload_smooth_cfr_continue_v01.py",
    "DISABLED__replace_smooth_cfr_v01.py",
    "DISABLED__replace_smooth_cfr_v02.py",
  ];

  it("keeps DISABLED__ scripts present with immediate SystemExit", () => {
    for (const name of names) {
      const p = path.join(scheduleDir, name);
      expect(fs.existsSync(p)).toBe(true);
      const text = fs.readFileSync(p, "utf8");
      expect(text).toContain("SystemExit");
      expect(text).toContain("DISABLED");
      // Must exit before any playwright import executes meaningfully — guard is at top
      const exitIdx = text.indexOf("SystemExit");
      const playwrightIdx = text.indexOf("from playwright");
      expect(exitIdx).toBeGreaterThan(-1);
      if (playwrightIdx >= 0) expect(exitIdx).toBeLessThan(playwrightIdx);
    }
  });

  it("is not referenced by package.json scripts", () => {
    const pkg = JSON.parse(
      fs.readFileSync(path.resolve(process.cwd(), "package.json"), "utf8"),
    ) as { scripts: Record<string, string> };
    const joined = Object.values(pkg.scripts || {}).join("\n");
    for (const name of names) {
      expect(joined.includes(name)).toBe(false);
      expect(joined.includes(name.replace("DISABLED__", ""))).toBe(false);
    }
    expect(joined.includes("smooth_cfr")).toBe(false);
  });

  it("fails if an enabled non-DISABLED smooth_cfr upload script reappears", () => {
    const enabled = fs
      .readdirSync(scheduleDir)
      .filter(
        (f) =>
          /smooth_cfr/.test(f) &&
          f.endsWith(".py") &&
          !f.startsWith("DISABLED__") &&
          !f.startsWith("_studio_audit"),
      );
    expect(enabled).toEqual([]);
  });
});

describe("shelf expectation fixture", () => {
  it("matches approved canonical public set", () => {
    const verify = JSON.parse(
      fs.readFileSync(
        path.resolve(
          process.cwd(),
          "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/FINAL_SHELF_VERIFY.json",
        ),
        "utf8",
      ),
    ) as { items: { id: string; privacy: string }[] };
    const publicIds = verify.items.filter((i) => i.privacy === "public").map((i) => i.id).sort();
    expect(publicIds).toEqual(
      ["1HuV8o3gOss", "3xrxdmaOwJI", "JRfhE6yWom4", "KcKBixwmcV4", "L2OFjL4neOo", "Mo93x0fxB1Q"].sort(),
    );
  });
});
