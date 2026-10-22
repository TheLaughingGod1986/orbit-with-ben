import { describe, expect, it, vi } from "vitest";
import fs from "fs";
import path from "path";
import type { BufferClient } from "../src/lib/publishing/buffer-api";
import type { BufferStore } from "../src/lib/publishing/buffer-store";
import { executeActions, runBufferCheck, type MirrorDeps } from "../src/lib/publishing/buffer-runner";
import { planBufferMirror, type BufferChannel, type Ledger, type Plan, type YouTubeVideo } from "../src/lib/publishing/buffer-mirror";
import {
  PROFILES,
  checkChannelsFile,
  getProfile,
  ownedByOtherProfile,
  profileFiles,
  refuseChannel,
  videoIdFromMediaPath,
} from "../src/lib/publishing/buffer-profile";

const NOW = new Date("2026-10-26T07:05:00Z");
const HOS = PROFILES.hos;
const OWB = PROFILES.owb;
const REPO = path.resolve(__dirname, "../..");

function video(over: Partial<YouTubeVideo> = {}): YouTubeVideo {
  return {
    id: "5n7xFQRBUvI",
    title: "Galen Thought Your Heart Was a Stove",
    description: "For 1,400 years doctors believed the heart warmed the blood.",
    tags: ["history of science", "galen", "william harvey"],
    durationSeconds: 24,
    privacyStatus: "private",
    publishAt: "2026-10-31T11:30:00Z",
    publishedAt: null,
    containsSyntheticMedia: true,
    ...over,
  };
}
const LONG = video({ id: "wwcjcFfC-5M", title: "How Harvey Proved Blood Circulates", durationSeconds: 540, publishAt: "2026-10-29T18:00:00Z" });
const SOCIAL = { hook: "Galen taught that the heart's job was to heat the blood, not to pump it.", question: "What did you think the heart did?" };

function memoryStore() {
  const ledger: Ledger = { version: 1, videos: {} };
  const store: BufferStore = {
    async load() {
      return JSON.parse(JSON.stringify(ledger));
    },
    async record(plan: Pick<Plan, "videoId" | "kind" | "title" | "timing">, channel: BufferChannel, postId: string | null) {
      const prev = ledger.videos[plan.videoId];
      const channels = { ...(prev?.channels ?? {}) };
      if (postId) channels[channel] = { postId, recordedAt: NOW.toISOString() };
      else delete channels[channel];
      ledger.videos[plan.videoId] = {
        kind: plan.kind,
        title: plan.title,
        dueAt: plan.timing.mode === "customScheduled" ? plan.timing.dueAt : null,
        mode: "customScheduled",
        channels,
        ...(prev?.media ? { media: prev.media } : {}),
      };
    },
    async setMedia(videoId: string, urls: string[]) {
      if (ledger.videos[videoId]) ledger.videos[videoId].media = urls.length === 1 ? urls[0] : urls;
    },
  };
  return { store, get: () => ledger };
}

function fakeClient() {
  let n = 0;
  return {
    createPost: vi.fn(async (input: Record<string, unknown>) => ({ id: `post${++n}`, dueAt: (input.dueAt as string) ?? null, status: "scheduled" })),
    editPost: vi.fn(async ({ postId, dueAt }: { postId: string; mode: string; dueAt: string }) => ({ id: postId, dueAt, status: "scheduled" })),
    deletePost: vi.fn(async () => undefined),
    getPostStatus: vi.fn(async () => "scheduled"),
  } satisfies BufferClient;
}

function hosDeps(over: Partial<MirrorDeps> = {}): MirrorDeps {
  const all = new Map([video(), LONG].map((v) => [v.id, v]));
  return {
    youtubeToken: async () => "token",
    fetchVideos: async (_t, ids) => new Map(ids.filter((id) => all.has(id)).map((id) => [id, all.get(id)!])),
    listScheduled: async () => [video(), LONG],
    client: fakeClient(),
    store: memoryStore().store,
    host: vi.fn(async (_p: string, pathname: string) => `https://pub.r2.dev/${pathname}`),
    checkUrl: vi.fn(async () => null),
    channelIds: HOS.channelIds,
    now: () => NOW,
    networks: HOS.networks,
    shortsOnly: true,
    mediaPrefix: HOS.mediaPrefix,
    foreignMedia: (p) => ownedByOtherProfile(p, HOS),
    refuseChannel: (id) => refuseChannel(HOS, id),
    findMedia: (id) =>
      id === "5n7xFQRBUvI"
        ? { videoId: id, mediaPath: "/uat/galen.mp4", thumbPath: null, longId: "wwcjcFfC-5M", standalone: false, social: SOCIAL, source: "social/hos/UPLOADS.json", registered: true }
        : null,
    ...over,
  };
}

describe("History of Science profile (J0817)", () => {
  it("plans a Short to HOS's Instagram, Facebook and TikTok, never Threads", () => {
    const plan = planBufferMirror({
      video: video(),
      channelIds: HOS.channelIds,
      ledger: { version: 1, videos: {} },
      now: NOW,
      mediaUrl: "https://pub.r2.dev/social/hos/5n7xFQRBUvI-ab.mp4",
      social: SOCIAL,
      parentLong: { id: LONG.id, goesPublicAt: LONG.publishAt },
      channels: HOS.networks,
      shortsOnly: true,
    });
    expect(plan.errors).toEqual([]);
    expect(plan.actions.map((a) => a.channel)).toEqual(["instagram", "facebook", "tiktok"]);
    const tiktok = plan.actions.find((a) => a.channel === "tiktok")!;
    if (tiktok.action !== "create_post") throw new Error("expected a create");
    expect(tiktok.input).toMatchObject({
      channelId: "6ac381bc6a5c39ccb61dd8aa",
      mode: "customScheduled",
      dueAt: "2026-10-31T11:30:00.000Z",
      assets: [{ video: { url: "https://pub.r2.dev/social/hos/5n7xFQRBUvI-ab.mp4", metadata: { thumbnailOffset: 1000 } } }],
      metadata: { tiktok: { isAiGenerated: true } },
    });
    const text = tiktok.input.text as string;
    expect(text.startsWith(SOCIAL.hook)).toBe(true);
    expect(text).toContain("Full film on YouTube. Link in bio.");
    expect(text).not.toContain("http");
    expect(text.length).toBeLessThanOrEqual(2200);
  });

  it("refuses a long film: HOS mirrors Shorts only", () => {
    const plan = planBufferMirror({ video: LONG, channelIds: HOS.channelIds, ledger: { version: 1, videos: {} }, now: NOW, channels: HOS.networks, shortsOnly: true });
    expect(plan.actions).toEqual([]);
    expect(plan.errors.join()).toMatch(/Shorts only/);
  });

  it("Orbit's default networks are unchanged and TikTok never takes a long", () => {
    const plan = planBufferMirror({
      video: video({ id: "long0000001", durationSeconds: 600, privacyStatus: "public", publishAt: null, publishedAt: NOW.toISOString() }),
      channelIds: { ...OWB.channelIds, tiktok: "tt" },
      ledger: { version: 1, videos: {} },
      now: NOW,
      thumbUrl: "https://pub.r2.dev/social/long0000001-thumb.jpg",
      channels: ["instagram", "facebook", "threads", "tiktok"],
    });
    expect(plan.actions.find((a) => a.channel === "tiktok")).toMatchObject({ action: "skip", reason: "TikTok takes Shorts only" });
    const owb = planBufferMirror({ video: video(), channelIds: OWB.channelIds, ledger: { version: 1, videos: {} }, now: NOW, mediaUrl: "https://x.r2.dev/a.mp4", standalone: true });
    expect(owb.actions.map((a) => a.channel)).toEqual(["instagram", "facebook", "threads"]);
  });
});

describe("org guard: an Orbit post never reaches HOS, or the reverse", () => {
  it("names the other channel's id, refuses unknown ids and passes the profile's own", () => {
    expect(refuseChannel(HOS, OWB.channelIds.instagram)).toMatch(/History of Science post to Orbit With Ben's Buffer channel/);
    expect(refuseChannel(OWB, HOS.channelIds.tiktok)).toMatch(/Orbit With Ben post to History of Science's/);
    expect(refuseChannel(HOS, "someoneelse")).toMatch(/not one of History of Science's channels in org 6431f03385378b838b780157/);
    expect(refuseChannel(HOS, undefined)).toMatch(/\(none\)/);
    for (const id of Object.values(HOS.channelIds)) expect(refuseChannel(HOS, id)).toBeNull();
  });

  it("executeActions refuses the create before Buffer is called, and records nothing", async () => {
    const client = fakeClient();
    const { store, get } = memoryStore();
    const plan = {
      videoId: "5n7xFQRBUvI",
      kind: "short" as const,
      title: "t",
      timing: { mode: "customScheduled" as const, dueAt: "2026-10-31T11:30:00.000Z" },
      actions: [
        { action: "create_post" as const, channel: "instagram" as const, input: { channelId: OWB.channelIds.instagram } },
        { action: "create_post" as const, channel: "facebook" as const, input: { channelId: HOS.channelIds.facebook } },
      ],
    };
    const results = await executeActions(plan, client, store, (id) => refuseChannel(HOS, id));
    expect(results[0]).toMatchObject({ ok: false, error: expect.stringMatching(/Refusing/) });
    expect(results[1]).toMatchObject({ ok: true });
    expect(client.createPost).toHaveBeenCalledTimes(1);
    expect(Object.keys(get().videos["5n7xFQRBUvI"].channels)).toEqual(["facebook"]);
  });

  it("a channels file with the wrong org or another profile's id is refused", () => {
    expect(() => checkChannelsFile(HOS, { organizationId: OWB.organizationId, channels: {} })).toThrow(/names org/);
    expect(() => checkChannelsFile(HOS, { channels: { instagram: { id: OWB.channelIds.instagram } } })).toThrow(/Orbit With Ben's Buffer channel/);
    // A network the profile doesn't post to (Threads for HOS) is never read.
    expect(checkChannelsFile(HOS, { channels: { threads: { id: "anything" }, tiktok: { id: HOS.channelIds.tiktok } } })).toEqual({ tiktok: HOS.channelIds.tiktok });
  });

  it("the repo's own channel files match their profiles", () => {
    for (const p of [OWB, HOS]) {
      const cfg = JSON.parse(fs.readFileSync(profileFiles(p, REPO).channels, "utf8"));
      expect(checkChannelsFile(p, cfg)).toEqual(p.channelIds);
    }
    expect(getProfile(undefined)).toBe(OWB);
    expect(getProfile("HOS")).toBe(HOS);
    expect(() => getProfile("threads")).toThrow(/use owb or hos/);
  });
});

describe("HOS daily check", () => {
  it("mirrors the scheduled Short under social/hos/ and leaves the long alone (not even reported)", async () => {
    const d = hosDeps();
    const out = await runBufferCheck(d);
    expect(out.unmirrored).toEqual([]);
    expect(out.autoMirrored.map((m) => m.videoId)).toEqual(["5n7xFQRBUvI"]);
    expect(out.autoMirrored[0].results.map((r) => [r.channel, r.ok])).toEqual([
      ["instagram", true],
      ["facebook", true],
      ["tiktok", true],
    ]);
    expect(d.host).toHaveBeenCalledWith("/uat/galen.mp4", "social/hos/5n7xFQRBUvI.mp4");
    const ids = (d.client!.createPost as ReturnType<typeof vi.fn>).mock.calls.map((c) => (c[0] as { channelId: string }).channelId);
    expect(ids.sort()).toEqual(Object.values(HOS.channelIds).sort());
  });
});

describe("hosted media stays with its profile", () => {
  it("reads the YouTube id only inside the profile's prefix", () => {
    expect(videoIdFromMediaPath("social/hos/5n7xFQRBUvI-1a2b.mp4", "social/hos/")).toBe("5n7xFQRBUvI");
    expect(videoIdFromMediaPath("social/5n7xFQRBUvI-1a2b.mp4", "social/hos/")).toBeNull();
    expect(ownedByOtherProfile("social/hos/5n7xFQRBUvI-1a2b.mp4", OWB)).toBe(true);
    expect(ownedByOtherProfile("social/abcdefghijk.mp4", OWB)).toBe(false);
    expect(ownedByOtherProfile("social/hos/x.mp4", HOS)).toBe(false);
  });

  it("Orbit's sweep never deletes an old HOS file, and HOS's never deletes Orbit's", async () => {
    const old = new Date("2026-10-01T00:00:00Z");
    const files = [
      { url: "https://pub.r2.dev/social/hos/5n7xFQRBUvI-aa.mp4", pathname: "social/hos/5n7xFQRBUvI-aa.mp4", uploadedAt: old },
      { url: "https://pub.r2.dev/social/zzzzzzzzzzz-bb.mp4", pathname: "social/zzzzzzzzzzz-bb.mp4", uploadedAt: old },
    ];
    const env = process.env.R2_PUBLIC_URL;
    process.env.R2_PUBLIC_URL = "https://pub.r2.dev";
    try {
      for (const [profile, kept, swept] of [
        [OWB, files[0].url, files[1].url],
        [HOS, files[1].url, files[0].url],
      ] as const) {
        const deleteMedia = vi.fn(async () => undefined);
        await runBufferCheck(
          hosDeps({
            listScheduled: async () => [],
            listMedia: async () => files,
            deleteMedia,
            mediaPrefix: profile.mediaPrefix,
            foreignMedia: (p) => ownedByOtherProfile(p, profile),
          }),
        );
        const deleted = deleteMedia.mock.calls.map((c) => (c as unknown[])[0]);
        expect(deleted).toContain(swept);
        expect(deleted).not.toContain(kept);
      }
    } finally {
      process.env.R2_PUBLIC_URL = env;
    }
  });
});
