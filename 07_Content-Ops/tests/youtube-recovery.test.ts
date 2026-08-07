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
import {
  assertYouTubeMutationAllowed,
  isYouTubePublishingFrozen,
  loadYouTubePublishingFreeze,
} from "../src/lib/publishing/youtube-freeze";
import {
  assertNotPlaceholderHoldPublishAt,
  assertScheduleCadence,
  isPlaceholderHoldPublishAt,
} from "../src/lib/publishing/youtube-schedule-guards";

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

  it("blocks historical duplicate IDs from becoming upload targets", () => {
    const registry: CanonicalRegistryFile = {
      version: 2,
      updatedAt: new Date().toISOString(),
      records: seedOrbitCanonicalRecords(),
      historicalDuplicateIdsGlobal: ["RCs6MMxF3ko", "IwpO33AJaPQ", "z-DLqoSoEBo"],
    };
    const r = lookupCanonicalConflicts({ registry, youtubeVideoId: "RCs6MMxF3ko" });
    expect(r.blocked).toBe(true);
    expect(r.reason).toContain("historical duplicate");
    expect(
      lookupCanonicalConflicts({ registry, youtubeVideoId: "IwpO33AJaPQ" }).blocked,
    ).toBe(true);
  });

  it("refuses silent canonical id replacement", () => {
    const registry: CanonicalRegistryFile = {
      version: 1,
      updatedAt: new Date().toISOString(),
      records: seedOrbitCanonicalRecords(),
    };
    const bhShort = seedOrbitCanonicalRecords().find(
      (r) => r.internalContentId === "v002-bh-short-01",
    )!;
    expect(() =>
      upsertCanonicalRecord(registry, {
        ...bhShort,
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

describe("emergency publishing freeze", () => {
  it("loads freeze config and fail-closes mutations", () => {
    const cfg = loadYouTubePublishingFreeze();
    expect(cfg.youtubePublishingFrozen).toBe(true);
    expect(isYouTubePublishingFrozen(cfg)).toBe(true);
    expect(() => assertYouTubeMutationAllowed({ operation: "test" })).toThrow(
      /YOUTUBE MUTATION BLOCKED/,
    );
    expect(() =>
      assertYouTubeMutationAllowed({ allowEmergencyUnfreeze: true, operation: "test" }),
    ).not.toThrow();
  });

  it("keeps youtube:upload as a hard-disabled stub", () => {
    const upload = fs.readFileSync(
      path.resolve(process.cwd(), "scripts/youtube-api-upload.ts"),
      "utf8",
    );
    expect(upload).toContain("DISABLED");
    expect(upload).toContain("youtube:package");
    expect(upload).not.toContain("YouTubePublishingAdapter");
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

  it("quarantines inverted cleanup and YouTube replace scripts", () => {
    const paths = [
      path.resolve(
        process.cwd(),
        "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/DISABLED___cleanup_visibility_cdp.py",
      ),
      path.resolve(
        process.cwd(),
        "../00_Brand/Channel-Setup/audits/DISABLED___replace_shorts_v02_youtube.py",
      ),
      path.resolve(
        process.cwd(),
        "../00_Brand/Channel-Setup/audits/youtube_smooth_canon_2026-08-07/DISABLED___canon_smooth_bh_v01.py",
      ),
    ];
    for (const p of paths) {
      // Accept either DISABLED__ rename or in-place SystemExit stub
      const alt = p
        .replace("/DISABLED___", "/")
        .replace("DISABLED___", "");
      const target = fs.existsSync(p) ? p : alt;
      expect(fs.existsSync(target)).toBe(true);
      const head = fs.readFileSync(target, "utf8").slice(0, 500);
      expect(head).toMatch(/SystemExit|DISABLED|permanently disabled/);
    }
  });
});

describe("ambiguous upload retry protection", () => {
  it("documents that blind --replace/--reupload flags are rejected by package CLI source", () => {
    const src = fs.readFileSync(
      path.resolve(process.cwd(), "scripts/youtube-package-upload.ts"),
      "utf8",
    );
    expect(src).toContain('flag("replace")');
    expect(src).toContain("UPLOAD BLOCKED: Replacement / reupload flags are forbidden");
    expect(src).toContain("findExistingUploadByTitle");
  });
});

describe("held-video and recovery config persistence", () => {
  it("keeps recovery mode with approved schedule and no Dec31 holds", () => {
    const cfg = JSON.parse(
      fs.readFileSync(
        path.resolve(process.cwd(), "../00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json"),
        "utf8",
      ),
    ) as {
      recoveryMode: boolean;
      maxShortsPerDay: number;
      heldVideoIds: string[];
      replacementUploadsAllowed: boolean;
      notes?: string;
      approvedScheduledIds?: string[];
    };
    expect(cfg.recoveryMode).toBe(true);
    expect(cfg.maxShortsPerDay).toBe(1);
    expect(cfg.replacementUploadsAllowed).toBe(false);
    expect(cfg.heldVideoIds).toEqual([]);
    expect(String(cfg.notes || "")).toMatch(/approved calendar applied/i);
    expect(cfg.approvedScheduledIds?.length || 0).toBeGreaterThanOrEqual(16);
  });
});

describe("registry persistence shape", () => {
  it("persists historicalDuplicateIds on disk registry", () => {
    const reg = JSON.parse(
      fs.readFileSync(
        path.resolve(process.cwd(), "../00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json"),
        "utf8",
      ),
    ) as {
      version: number;
      records: { youtubeVideoId: string; historicalDuplicateIds?: string[] }[];
      historicalDuplicateIdsGlobal?: string[];
    };
    expect(reg.version).toBeGreaterThanOrEqual(2);
    expect(reg.historicalDuplicateIdsGlobal?.length || 0).toBeGreaterThan(0);
    const bh = reg.records.find((r) => r.youtubeVideoId === "3xrxdmaOwJI");
    expect(bh?.historicalDuplicateIds).toEqual(expect.arrayContaining(["RCs6MMxF3ko"]));
  });
});

describe("placeholder hold date ban", () => {
  it("detects 31 Dec placeholder publishAt", () => {
    expect(isPlaceholderHoldPublishAt("2026-12-31T11:30:00Z")).toBe(true);
    expect(isPlaceholderHoldPublishAt("2026-12-31T12:30:00+01:00")).toBe(true);
    expect(isPlaceholderHoldPublishAt("2026-08-14T17:00:00Z")).toBe(false);
    expect(isPlaceholderHoldPublishAt(null)).toBe(false);
  });

  it("throws SCHEDULE BLOCKED for placeholder holds", () => {
    expect(() => assertNotPlaceholderHoldPublishAt("2026-12-31T11:30:00Z")).toThrow(
      /SCHEDULE BLOCKED/,
    );
  });

  it("blocks cadence when placeholder, historical duplicate, or short-day exceeded", () => {
    const future = new Date(Date.now() + 86_400_000).toISOString();
    expect(
      assertScheduleCadence({
        format: "shorts",
        publishAtIso: "2026-12-31T11:30:00Z",
        shortsOnSameDay: 0,
      }).ok,
    ).toBe(false);

    expect(() =>
      assertScheduleCadence({
        format: "shorts",
        publishAtIso: future,
        shortsOnSameDay: 0,
        isHistoricalDuplicate: true,
      }),
    ).not.toThrow();
    expect(
      assertScheduleCadence({
        format: "shorts",
        publishAtIso: future,
        shortsOnSameDay: 0,
        isHistoricalDuplicate: true,
      }).errors.some((e) => /historical duplicate/i.test(e)),
    ).toBe(true);

    expect(
      assertScheduleCadence({
        format: "shorts",
        publishAtIso: future,
        shortsOnSameDay: 1,
        maxShortsPerDay: 1,
      }).errors.some((e) => /Short\/day/i.test(e)),
    ).toBe(true);

    expect(
      assertScheduleCadence({
        format: "longform",
        publishAtIso: future,
        shortsOnSameDay: 0,
        longsInSameWeek: 1,
        maxLongsPerWeek: 1,
      }).errors.some((e) => /long\/week/i.test(e)),
    ).toBe(true);

    expect(
      assertScheduleCadence({
        format: "shorts",
        publishAtIso: future,
        shortsOnSameDay: 0,
        sameMinuteCollision: true,
      }).ok,
    ).toBe(false);
  });

  it("emergency-repair no longer assigns Dec 31 holds", () => {
    const src = fs.readFileSync(
      path.resolve(process.cwd(), "scripts/youtube-emergency-repair.ts"),
      "utf8",
    );
    expect(src).toContain("placeholder_holds_forbidden");
    expect(src).toContain("report_imminent_no_placeholder_hold");
    expect(src).not.toMatch(/action:\s*"hold_schedule_dec31"/);
  });

  it("shelf-verify expects NF01 scheduled and historical dupes unscheduled", () => {
    const src = fs.readFileSync(
      path.resolve(process.cwd(), "scripts/youtube-shelf-verify.ts"),
      "utf8",
    );
    expect(src).toContain('role: "canonical_nf01_scheduled"');
    expect(src).toContain('role: "historical_dupe_unscheduled"');
    expect(src).toContain('publishAt: "2026-08-08T10:30:00Z"');
    expect(src).not.toMatch(/publishAt:\s*"2026-12-31T11:30:00Z"/);
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

  it("post-repair shelf verify keeps approved BH+Fermi core public and dupes private", () => {
    const verifyPath = path.resolve(
      process.cwd(),
      "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/POST_REPAIR_SHELF_VERIFY.json",
    );
    expect(fs.existsSync(verifyPath)).toBe(true);
    const verify = JSON.parse(fs.readFileSync(verifyPath, "utf8")) as {
      ok: boolean;
      rows: { id: string; status: string; expect: string }[];
    };
    expect(verify.ok).toBe(true);
    for (const id of ["3xrxdmaOwJI", "JRfhE6yWom4", "L2OFjL4neOo", "Mo93x0fxB1Q"]) {
      expect(verify.rows.find((r) => r.id === id)?.status).toBe("PASS");
    }
    for (const id of ["RCs6MMxF3ko", "IwpO33AJaPQ", "z-DLqoSoEBo", "UWwNKYf_aU8"]) {
      expect(verify.rows.find((r) => r.id === id)?.status).toBe("PASS");
    }
  });
});
