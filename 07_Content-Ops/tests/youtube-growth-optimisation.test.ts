import { describe, expect, it } from "vitest";
import {
  APPROVED_SCHEDULE,
  CHANNEL_KEYWORDS,
  PLAYLIST_SPECS,
  assertNoScheduleFieldsInSnippetUpdate,
  buildRegistryRelationFixes,
  buildShortDescriptionPlans,
  classifyTitle,
  descriptionAlreadyOptimised,
  formatChannelKeywordsForApi,
  playlistTitleCollisionKey,
  scoreGrowthReadiness,
} from "../src/lib/publishing/youtube-growth-optimisation";

describe("youtube-growth-optimisation", () => {
  it("builds unique playlist titles (idempotency collision keys)", () => {
    const keys = PLAYLIST_SPECS.map((p) => playlistTitleCollisionKey(p.title));
    expect(new Set(keys).size).toBe(keys.length);
  });

  it("playlist video memberships stay within approved public+scheduled set", () => {
    const allowed = new Set([
      "Mo93x0fxB1Q",
      "1HuV8o3gOss",
      "KcKBixwmcV4",
      "3xrxdmaOwJI",
      "JRfhE6yWom4",
      "L2OFjL4neOo",
      ...Object.keys(APPROVED_SCHEDULE),
    ]);
    for (const p of PLAYLIST_SPECS) {
      for (const id of p.videoIds) {
        expect(allowed.has(id)).toBe(true);
      }
    }
  });

  it("short description plans are idempotent and fix JWST parent links", () => {
    const plans = buildShortDescriptionPlans();
    expect(plans.length).toBeGreaterThanOrEqual(13);
    for (const p of plans) {
      expect(descriptionAlreadyOptimised(p.description, p.description)).toBe(true);
      expect(p.description).toContain(`youtu.be/${p.parentLongId}`);
      expect(p.description).not.toContain("1wxUhF3XnwI");
      expect((p.description.match(/#/g) || []).length).toBeLessThanOrEqual(6);
    }
    const jwst = plans.filter((p) => p.family === "JWST");
    expect(jwst.every((p) => p.parentLongId === "tfTkMdE7qqw")).toBe(true);
  });

  it("does not allow status fields on snippet updates", () => {
    expect(() => assertNoScheduleFieldsInSnippetUpdate({ status: { privacyStatus: "public" } })).toThrow(
      /status must not/,
    );
    expect(() => assertNoScheduleFieldsInSnippetUpdate({} as any)).not.toThrow();
  });

  it("registry relation fixes fill exo/jwst orphans without guessing unknowns", () => {
    const fixes = buildRegistryRelationFixes([
      {
        youtubeVideoId: "ho9VJxp7f3A",
        contentType: "shorts",
        contentFamily: "EXOPLANETS",
        relatedLongFormVideoId: null,
      },
      {
        youtubeVideoId: "bLv0RfidjSg",
        contentType: "shorts",
        contentFamily: "JWST",
        relatedLongFormVideoId: null,
      },
      {
        youtubeVideoId: "1HuV8o3gOss",
        contentType: "shorts",
        contentFamily: "FERMI",
        relatedLongFormVideoId: "Mo93x0fxB1Q",
      },
      {
        youtubeVideoId: "mystery",
        contentType: "shorts",
        contentFamily: "UNKNOWN",
        relatedLongFormVideoId: null,
      },
    ]);
    expect(fixes.map((f) => f.youtubeVideoId).sort()).toEqual(["bLv0RfidjSg", "ho9VJxp7f3A"]);
    expect(fixes.find((f) => f.youtubeVideoId === "ho9VJxp7f3A")?.relatedLongFormVideoId).toBe(
      "b8-X_FyJnHM",
    );
    expect(fixes.find((f) => f.youtubeVideoId === "bLv0RfidjSg")?.relatedLongFormVideoId).toBe(
      "tfTkMdE7qqw",
    );
  });

  it("sanitises channel keywords and keeps list compact", () => {
    const k = formatChannelKeywordsForApi(CHANNEL_KEYWORDS);
    expect(k.includes("Orbit With Ben")).toBe(true);
    expect(k.includes("JWST")).toBe(true);
    expect(k.length).toBeLessThan(500);
  });

  it("title classifier preserves healthy titles (no speculative FIX NOW)", () => {
    expect(
      classifyTitle({
        youtubeId: "3xrxdmaOwJI",
        title: "What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey",
      }).verdict,
    ).toBe("KEEP");
    expect(
      classifyTitle({ youtubeId: "x", title: "UNTITLED PLACEHOLDER" }).verdict,
    ).toBe("FIX NOW");
  });

  it("growth scores rise when playlists/keywords/funnels are healthy", () => {
    const before = scoreGrowthReadiness({
      playlists: 0,
      keywordsSet: false,
      channelDescMentionsJwst: false,
      thinShortDescriptionsRemaining: 10,
      wrongParentLinksRemaining: 4,
      orphanShortsInRegistry: 8,
      studioManualRemaining: 8,
    });
    const after = scoreGrowthReadiness({
      playlists: 5,
      keywordsSet: true,
      channelDescMentionsJwst: true,
      thinShortDescriptionsRemaining: 0,
      wrongParentLinksRemaining: 0,
      orphanShortsInRegistry: 0,
      studioManualRemaining: 5,
    });
    expect(after.channelHealth).toBeGreaterThan(before.channelHealth);
    expect(after.growthReadiness).toBeGreaterThan(before.growthReadiness);
    expect(after.channelHealth).toBeGreaterThanOrEqual(75);
    expect(after.growthReadiness).toBeGreaterThanOrEqual(70);
  });

  it("approved schedule map remains 13 slots with no Dec-31 placeholders", () => {
    expect(Object.keys(APPROVED_SCHEDULE)).toHaveLength(13);
    expect(Object.values(APPROVED_SCHEDULE).some((v) => v.startsWith("2026-12-31"))).toBe(false);
  });
});
