import { describe, expect, it } from "vitest";
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";
import {
  londonDateTime,
  scheduleClipAcrossPlatforms,
  isValidScheduleDate,
  formatLondon,
} from "../src/lib/publishing/schedule";
import { detectDuplicates, canForceRepost } from "../src/lib/publishing/duplicates";
import { parseMetricsCsv, previewCsv, DEFAULT_MAPPINGS } from "../src/lib/analytics/csv-import";
import { exportCaptions, formatSrtTime } from "../src/lib/content/captions";
import { createExportPackage, slugify } from "../src/lib/content/export-package";
import { validateClipTimestamps, validateScriptPresent } from "../src/lib/validation/schemas";
import { canTransitionClip, canTransitionPost } from "../src/lib/publishing/status";
import { generateInsights, engagementRate } from "../src/lib/analytics/insights";
import { getAdapterForPlatform } from "../src/lib/publishing/adapters";
import { generateShortPlan } from "../src/lib/content/generate-short-plan";
import fs from "fs/promises";
import os from "os";
import path from "path";

describe("platform metadata generation", () => {
  it("creates customised copy per platform", () => {
    const copies = generatePlatformCopy({
      shortTitle: "The Great Filter",
      hook: "The universe may be hiding something from us.",
      topic: "Alien Civilisations",
      youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
    });
    expect(copies).toHaveLength(8);
    const yt = copies.find((c) => c.platform === "youtube_shorts")!;
    expect(yt.title!.length).toBeLessThanOrEqual(60);
    expect(yt.pinnedComment).toContain("youtu.be");
    const x = copies.find((c) => c.platform === "x")!;
    expect(x.caption.length).toBeLessThanOrEqual(280);
  });
});

describe("schedule creation", () => {
  it("staggers platforms within 24h", () => {
    const base = londonDateTime("2026-08-07", "21:00");
    const slots = scheduleClipAcrossPlatforms({ youtubeShortAt: base });
    expect(slots[0].platform).toBe("youtube_shorts");
    expect(slots.find((s) => s.platform === "tiktok")!.scheduledAt.getTime()).toBeGreaterThan(
      base.getTime(),
    );
    expect(formatLondon(base)).toContain("2026-08-07");
  });

  it("rejects invalid schedule dates", () => {
    expect(isValidScheduleDate("2026-08-07T21:00:00+01:00")).toBe(true);
    expect(isValidScheduleDate("not-a-date")).toBe(false);
  });
});

describe("duplicate detection", () => {
  it("blocks same clip on same platform", () => {
    const warnings = detectDuplicates({
      shortClipId: "c1",
      platform: "tiktok",
      title: "Hello",
      existing: [
        {
          id: "p1",
          shortClipId: "c1",
          platform: "tiktok",
          title: "Hello",
        },
      ],
    });
    expect(warnings.some((w) => w.level === "block")).toBe(true);
    expect(canForceRepost(warnings, undefined).ok).toBe(false);
    expect(canForceRepost(warnings, "New hook").ok).toBe(true);
  });
});

describe("csv analytics import", () => {
  const csv = `Video URL,Views,Likes,Comments,Shares,Average view duration,Average percentage viewed,Subscribers gained
https://youtu.be/a,100,10,1,2,12,40,3
https://youtu.be/a,100,10,1,2,12,40,3
`;

  it("previews and skips duplicate rows", () => {
    const preview = previewCsv(csv, DEFAULT_MAPPINGS.youtube);
    expect(preview.headers).toContain("Views");
    const parsed = parseMetricsCsv(csv, DEFAULT_MAPPINGS.youtube);
    expect(parsed.rows).toHaveLength(1);
    expect(parsed.duplicatesSkipped).toBe(1);
  });

  it("reports missing id/url", () => {
    const bad = `Views,Likes\n10,1\n`;
    const parsed = parseMetricsCsv(bad, { views: "Views", likes: "Likes" });
    expect(parsed.errors.length).toBeGreaterThan(0);
  });
});

describe("caption export", () => {
  it("builds srt/vtt", () => {
    const caps = exportCaptions({
      transcript: "The universe may be hiding something from us tonight.",
      startSeconds: 0,
      endSeconds: 20,
    });
    expect(caps.srt).toContain("-->");
    expect(caps.vtt.startsWith("WEBVTT")).toBe(true);
    expect(formatSrtTime(65.5)).toBe("00:01:05,500");
  });
});

describe("export manifest", () => {
  it("writes package files", async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), "orbit-export-"));
    const copies = generatePlatformCopy({
      shortTitle: "The Great Filter",
      hook: "The universe may be hiding something from us.",
      topic: "Alien Civilisations",
    });
    const captions = exportCaptions({
      transcript: "A short transcript for captions.",
      endSeconds: 30,
    });
    const { dir, manifest } = await createExportPackage({
      exportRoot: root,
      slug: "demo",
      clipId: "clip-1",
      clipNumber: 1,
      clipSlug: slugify("The Great Filter"),
      sourceVideoTitle: "Will We Ever Meet Aliens?",
      sourceStartTime: "03:20",
      sourceEndTime: "04:00",
      platforms: copies,
      captions,
    });
    const manifestRaw = await fs.readFile(path.join(dir, "manifest.json"), "utf8");
    expect(JSON.parse(manifestRaw).clipId).toBe("clip-1");
    expect(manifest.platforms).toContain("youtube_shorts");
  });
});

describe("validation rules", () => {
  it("flags empty script and bad timestamps", () => {
    expect(validateScriptPresent("")).toHaveLength(1);
    expect(validateClipTimestamps("01:00", "00:30").ok).toBe(false);
    expect(validateClipTimestamps("01:00", "02:10").errors.some((e) => e.includes("longer"))).toBe(
      true,
    );
  });
});

describe("status transitions", () => {
  it("allows and rejects transitions", () => {
    expect(canTransitionClip("proposed", "approved")).toBe(true);
    expect(canTransitionClip("proposed", "exported")).toBe(false);
    expect(canTransitionPost("draft", "ready")).toBe(true);
    expect(canTransitionPost("published", "draft")).toBe(false);
  });
});

describe("missing data handling", () => {
  it("handles blank analytics and low insight data", () => {
    expect(engagementRate({ views: 0, likes: 10 })).toBeNull();
    const { insights, lowDataMessage } = generateInsights([]);
    expect(insights).toHaveLength(0);
    expect(lowDataMessage).toMatch(/More performance data/);
  });
});

describe("publishing adapters", () => {
  it("keeps manual mode without fake success", async () => {
    const adapter = getAdapterForPlatform("tiktok");
    const result = await adapter.publish({
      id: "1",
      platform: "tiktok",
      caption: "Hello",
      uploadStatus: "ready",
    });
    expect(result.success).toBe(false);
    expect(result.message).toMatch(/connected account|Manual upload required/i);
  });

  it("reports unsupported platform via manual adapter", async () => {
    const adapter = getAdapterForPlatform("unknown_platform");
    const status = await adapter.getStatus();
    expect(status.connection).toBe("manual_upload_required");
  });
});

describe("short plan", () => {
  it("rejects empty script and proposes aliens clips", () => {
    expect(generateShortPlan({ title: "x", script: "" }).errors.length).toBeGreaterThan(0);
    const plan = generateShortPlan({
      title: "Will We Ever Meet Aliens?",
      script: `
Where is everybody? The Fermi paradox asks why a crowded galaxy can still sound empty.
The Great Filter may explain the silence — a barrier so hard almost no civilisation crosses it.
Light-years make contact slow; even Alpha Centauri is awkwardly far for any conversation.
First contact may arrive as data in an archive rather than a landing craft on a pad.
Astronomers keep listening with radio telescopes and searching atmospheres for biosignatures.
Orbit asks the question calmly: will we ever meet aliens, and what would meeting even mean?
`.repeat(2),
    });
    expect(plan.errors).toHaveLength(0);
    expect(plan.clips.length).toBeGreaterThanOrEqual(4);
  });
});
