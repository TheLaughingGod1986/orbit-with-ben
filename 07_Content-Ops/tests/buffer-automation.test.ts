import { describe, expect, it, vi } from "vitest";
import { createBufferApiClient, type BufferClient } from "../src/lib/publishing/buffer-api";
import fs from "fs";
import os from "os";
import path from "path";
import { createFileBufferStore, type BufferStore } from "../src/lib/publishing/buffer-store";
import { mirrorVideo, runBufferCheck, videoIdFromBlobPath, type MirrorDeps } from "../src/lib/publishing/buffer-runner";
import type { Ledger, Plan, YouTubeVideo, BufferChannel } from "../src/lib/publishing/buffer-mirror";

const NOW = new Date("2026-10-01T09:00:00Z");
const CHANNELS = { instagram: "ig1", facebook: "fb1", threads: "th1" };

function video(over: Partial<YouTubeVideo> = {}): YouTubeVideo {
  return {
    id: "short0000001",
    title: "Why You Can't Stand on a Neutron Star",
    description: "One teaspoon weighs as much as a mountain.",
    tags: ["neutron star", "space"],
    durationSeconds: 27,
    privacyStatus: "private",
    publishAt: "2026-10-05T10:30:00Z",
    publishedAt: null,
    containsSyntheticMedia: true,
    ...over,
  };
}
const LONG = video({ id: "long0000001", durationSeconds: 600, privacyStatus: "public", publishAt: null, publishedAt: "2026-09-20T17:00:00Z" });

function memoryStore(initial: Ledger = { version: 1, videos: {} }) {
  const ledger: Ledger = JSON.parse(JSON.stringify(initial));
  const store: BufferStore = {
    async load() {
      return JSON.parse(JSON.stringify(ledger));
    },
    async record(plan: Pick<Plan, "videoId" | "kind" | "title" | "timing">, channel: BufferChannel, postId: string | null) {
      const prev = ledger.videos[plan.videoId];
      const channels = { ...(prev?.channels ?? {}) };
      if (postId) channels[channel] = { postId, recordedAt: NOW.toISOString() };
      else delete channels[channel];
      if (!Object.keys(channels).length) {
        delete ledger.videos[plan.videoId];
        return;
      }
      ledger.videos[plan.videoId] = {
        kind: plan.kind,
        title: plan.title,
        dueAt: plan.timing.mode === "customScheduled" ? plan.timing.dueAt : prev?.dueAt ?? null,
        mode: plan.timing.mode === "shareNow" ? "shareNow" : "customScheduled",
        channels,
        ...(prev?.media ? { media: prev.media } : {}),
      };
    },
    async setMedia(videoId: string, urls: string[]) {
      const e = ledger.videos[videoId];
      if (!e) return;
      if (urls.length === 1) e.media = urls[0];
      else if (urls.length) e.media = urls;
      else delete e.media;
    },
  };
  return { store, get: () => ledger };
}

function fakeClient(failOn?: string, statuses: Record<string, string | null> = {}) {
  let n = 0;
  const client = {
    createPost: vi.fn(async (input: Record<string, unknown>) => {
      if (failOn && input.channelId === failOn) throw new Error("Buffer InvalidInputError: bad video");
      n += 1;
      return { id: `post${n}`, dueAt: (input.dueAt as string) ?? null, status: "scheduled" };
    }),
    editPost: vi.fn(async ({ postId, dueAt }: { postId: string; mode: string; dueAt: string }) => ({ id: postId, dueAt, status: "scheduled" })),
    deletePost: vi.fn(async () => undefined),
    getPostStatus: vi.fn(async (postId: string) => (postId in statuses ? statuses[postId] : "scheduled")),
  };
  return client satisfies BufferClient;
}

function deps(over: Partial<MirrorDeps> & { videos?: YouTubeVideo[]; scheduled?: YouTubeVideo[] } = {}): MirrorDeps {
  const all = new Map((over.videos ?? [video(), LONG]).map((v) => [v.id, v]));
  return {
    youtubeToken: async () => "token",
    fetchVideos: async (_t, ids) => new Map(ids.filter((id) => all.has(id)).map((id) => [id, all.get(id)!])),
    listScheduled: async () => over.scheduled ?? [],
    client: fakeClient(),
    store: memoryStore().store,
    host: vi.fn(async (_p: string, pathname: string) => `https://abc.public.blob.vercel-storage.com/${pathname}`),
    checkUrl: vi.fn(async () => null),
    channelIds: CHANNELS,
    now: () => NOW,
    ...over,
  };
}

describe("Buffer API client", () => {
  it("sends createPost with the key, the MCP-shaped input and needsApproval false", async () => {
    const fetchImpl = vi.fn(async (_url: string, init: RequestInit) => {
      const body = JSON.parse(String(init.body));
      expect(body.query).toContain("createPost(input: $input)");
      expect(body.variables.input).toMatchObject({ channelId: "ig1", mode: "customScheduled", needsApproval: false, assets: [] });
      expect((init.headers as Record<string, string>).Authorization).toBe("Bearer k");
      return new Response(JSON.stringify({ data: { createPost: { __typename: "PostActionSuccess", post: { id: "p1", dueAt: "x", status: "scheduled" } } } }));
    });
    const client = createBufferApiClient("k", fetchImpl as unknown as typeof fetch);
    await expect(client.createPost({ channelId: "ig1", mode: "customScheduled" })).resolves.toEqual({ id: "p1", dueAt: "x", status: "scheduled" });
  });

  it("throws Buffer's typed errors and GraphQL errors", async () => {
    const typed = createBufferApiClient("k", (async () =>
      new Response(JSON.stringify({ data: { createPost: { __typename: "InvalidInputError", message: "dueAt must be in the future" } } }))) as unknown as typeof fetch);
    await expect(typed.createPost({})).rejects.toThrow(/InvalidInputError: dueAt must be in the future/);
    const gql = createBufferApiClient("k", (async () => new Response(JSON.stringify({ errors: [{ message: "Unauthorized" }] }), { status: 401 })) as unknown as typeof fetch);
    await expect(gql.deletePost("p1")).rejects.toThrow(/401: Unauthorized/);
  });

  it("refuses to start without a key", () => {
    expect(() => createBufferApiClient("")).toThrow(/BUFFER_API_KEY/);
  });
});

describe("Buffer store (BUFFER_POSTS.json)", () => {
  it("records, updates and removes posts in the file", async () => {
    const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "orbit-buffer-")), "BUFFER_POSTS.json");
    const store = createFileBufferStore(file, () => NOW);
    expect(await store.load()).toEqual({ version: 1, videos: {} });
    const plan = { videoId: "v1", kind: "short" as const, title: "T", timing: { mode: "customScheduled" as const, dueAt: "2026-10-05T10:30:00.000Z" } };
    await store.record(plan, "instagram", "a");
    await store.record(plan, "threads", "b");
    const saved = JSON.parse(fs.readFileSync(file, "utf8"));
    expect(Object.keys(saved.videos.v1.channels)).toEqual(["instagram", "threads"]);
    expect(saved.videos.v1.dueAt).toBe("2026-10-05T10:30:00.000Z");
    await store.record({ ...plan, timing: { mode: "customScheduled", dueAt: "2026-10-07T10:30:00.000Z" } }, "instagram", "a");
    expect((await store.load()).videos.v1.dueAt).toBe("2026-10-07T10:30:00.000Z");
    await store.record(plan, "instagram", null);
    await store.record(plan, "threads", null);
    expect((await store.load()).videos).toEqual({});
  });
});

describe("mirrorVideo (after an upload)", () => {
  it("hosts the Short, checks the URL, schedules all three posts and records them", async () => {
    const mem = memoryStore();
    const d = deps({ store: mem.store });
    const out = await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, d);
    expect(out.plan.errors).toEqual([]);
    expect(d.host).toHaveBeenCalledWith("/tmp/short.mp4", "social/short0000001.mp4");
    expect(d.checkUrl).toHaveBeenCalledWith("https://abc.public.blob.vercel-storage.com/social/short0000001.mp4", "video");
    expect(out.sent).toBe(true);
    expect(out.results.map((r) => `${r.channel}:${r.ok}`)).toEqual(["instagram:true", "facebook:true", "threads:true"]);
    expect(Object.keys(mem.get().videos.short0000001.channels)).toEqual(["instagram", "facebook", "threads"]);
    expect(mem.get().videos.short0000001.dueAt).toBe("2026-10-05T10:30:00.000Z");
  });

  it("never uploads the file for a Short it refuses", async () => {
    const d = deps({ videos: [video({ publishAt: "2026-10-03T10:30:00Z" }), video({ id: "long0000001", durationSeconds: 600, publishAt: "2026-10-04T17:00:00Z" })] });
    const out = await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, d);
    expect(out.plan.errors.join()).toMatch(/before its long/);
    expect(d.host).not.toHaveBeenCalled();
    expect(out.sent).toBe(false);
  });

  it("dry run hosts and posts nothing", async () => {
    const d = deps();
    const out = await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4", dryRun: true }, d);
    expect(out.plan.actions.filter((a) => a.action === "create_post")).toHaveLength(3);
    expect(d.host).not.toHaveBeenCalled();
    expect((d.client as unknown as ReturnType<typeof fakeClient>).createPost).not.toHaveBeenCalled();
  });

  it("plans only without a Buffer key, and stops without a Blob token", async () => {
    const noKey = await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ client: null }));
    expect(noKey.sent).toBe(false);
    expect(noKey.plan.errors).toEqual([]);
    const noBlob = await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ host: null }));
    expect(noBlob.plan.errors.join()).toMatch(/BLOB_READ_WRITE_TOKEN/);
  });

  it("keeps going when one channel fails, and records the others", async () => {
    const mem = memoryStore();
    const out = await mirrorVideo(
      { videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" },
      deps({ store: mem.store, client: fakeClient("ig1") }),
    );
    expect(out.results.map((r) => `${r.channel}:${r.ok}`)).toEqual(["instagram:false", "facebook:true", "threads:true"]);
    expect(Object.keys(mem.get().videos.short0000001.channels)).toEqual(["facebook", "threads"]);
  });

  it("mirrors a long with its thumbnail and link cards", async () => {
    const long = video({ id: "long0000002", durationSeconds: 594, publishAt: "2026-10-04T17:00:00Z" });
    const d = deps({ videos: [long] });
    const out = await mirrorVideo({ videoId: "long0000002", thumbPath: "/tmp/thumb.jpg" }, d);
    expect(d.host).toHaveBeenCalledWith("/tmp/thumb.jpg", "social/long0000002-thumb.jpg");
    expect(d.host).toHaveBeenCalledTimes(1);
    expect(d.checkUrl).toHaveBeenCalledWith(expect.any(String), "image");
    expect(out.results.every((r) => r.ok && r.action === "create_post")).toBe(true);
  });

  it("mirrors a long with a trailer: hosts both files, Reels on Instagram and Facebook, and remembers both", async () => {
    const long = video({ id: "long0000002", durationSeconds: 594, publishAt: "2026-10-04T17:00:00Z" });
    const mem = memoryStore();
    const client = fakeClient();
    const d = deps({ videos: [long], store: mem.store, client });
    const social = { hook: "There's no ground on Jupiter.", question: "Would you go in?" };
    const out = await mirrorVideo({ videoId: "long0000002", thumbPath: "/tmp/thumb.jpg", trailerPath: "/tmp/trailer.mp4", social }, d);
    expect(out.plan.errors).toEqual([]);
    const thumb = "https://abc.public.blob.vercel-storage.com/social/long0000002-thumb.jpg";
    const trailer = "https://abc.public.blob.vercel-storage.com/social/long0000002-trailer.mp4";
    expect(out.hosted).toEqual([thumb, trailer]);
    expect(d.checkUrl).toHaveBeenCalledWith(trailer, "video");
    expect(d.checkUrl).toHaveBeenCalledWith(thumb, "image");
    const inputs = client.createPost.mock.calls.map((c) => c[0] as { channelId: string; text: string; assets: unknown[] });
    expect(inputs.map((i) => JSON.stringify(i.assets).includes("trailer"))).toEqual([true, true, false]);
    expect(inputs.every((i) => i.text.startsWith("There's no ground on Jupiter.") && i.text.includes("Would you go in?"))).toBe(true);
    expect(mem.get().videos.long0000002.media).toEqual([thumb, trailer]);
  });

  it("hosts only the files a new post will use", async () => {
    const long = video({ id: "long0000002", durationSeconds: 594, publishAt: "2026-10-04T17:00:00Z" });
    const plan = { videoId: "long0000002", kind: "long" as const, title: long.title, timing: { mode: "customScheduled" as const, dueAt: "2026-10-04T17:00:00.000Z" } };
    const mem = memoryStore();
    for (const [c, id] of [["instagram", "p1"], ["threads", "p3"]] as const) await mem.store.record(plan, c, id);
    const d = deps({ videos: [long], store: mem.store });
    // Only Facebook is missing: the trailer is needed, the thumbnail isn't.
    await mirrorVideo({ videoId: "long0000002", thumbPath: "/tmp/thumb.jpg", trailerPath: "/tmp/trailer.mp4" }, d);
    expect(d.host).toHaveBeenCalledTimes(1);
    expect(d.host).toHaveBeenCalledWith("/tmp/trailer.mp4", "social/long0000002-trailer.mp4");
  });

  it("re-running a mirrored video posts nothing new and needs no file", async () => {
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ store: mem.store }));
    const d = deps({ store: mem.store });
    const again = await mirrorVideo({ videoId: "short0000001", longId: "long0000001" }, d);
    expect(again.plan.errors).toEqual([]);
    expect(again.results.every((r) => r.action === "skip")).toBe(true);
    expect(d.host).not.toHaveBeenCalled();
  });
});

describe("runBufferCheck (daily)", () => {
  async function mirrored() {
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ store: mem.store }));
    return mem;
  }

  it("moves the Buffer posts when the YouTube time moves", async () => {
    const mem = await mirrored();
    const client = fakeClient();
    const out = await runBufferCheck(deps({ store: mem.store, client, videos: [video({ publishAt: "2026-10-07T10:30:00Z" })] }));
    expect(client.editPost).toHaveBeenCalledTimes(3);
    expect(out.changes[0].actions.every((a) => a.action === "edit_post")).toBe(true);
    expect(mem.get().videos.short0000001.dueAt).toBe("2026-10-07T10:30:00.000Z");
  });

  it("takes the posts down when the video no longer goes public", async () => {
    const mem = await mirrored();
    const client = fakeClient();
    await runBufferCheck(deps({ store: mem.store, client, videos: [video({ publishAt: null })] }));
    expect(client.deletePost).toHaveBeenCalledTimes(3);
    expect(mem.get().videos.short0000001).toBeUndefined();
  });

  it("reports only, when dry, and lists scheduled uploads never mirrored", async () => {
    const mem = await mirrored();
    const client = fakeClient();
    const other = video({ id: "new00000001", title: "New Short" });
    const out = await runBufferCheck(
      deps({ store: mem.store, client, videos: [video({ publishAt: null })], scheduled: [video(), other] }),
      { dryRun: true },
    );
    expect(out.sent).toBe(false);
    expect(client.deletePost).not.toHaveBeenCalled();
    expect(out.changes[0].actions).toHaveLength(3);
    expect(out.unmirrored).toEqual([
      { videoId: "new00000001", title: "New Short", publishAt: "2026-10-05T10:30:00Z", reason: expect.stringMatching(/register --video new00000001/) },
    ]);
  });
});

describe("runBufferCheck auto-mirrors uploads made outside youtube:package", () => {
  const handShort = video({ id: "hand0000001", title: "Hand-uploaded Short" });
  const hint = { videoId: "hand0000001", mediaPath: "/tmp/hand.mp4", thumbPath: null, longId: "long0000001", standalone: false, source: "social/UPLOADS.json" };

  it("finds the file, hosts it and schedules all three posts", async () => {
    const mem = memoryStore();
    const client = fakeClient();
    const d = deps({ store: mem.store, client, videos: [handShort, LONG], scheduled: [handShort], findMedia: () => hint });
    const out = await runBufferCheck(d);
    expect(out.unmirrored).toEqual([]);
    expect(out.autoMirrored).toEqual([expect.objectContaining({ videoId: "hand0000001", sent: true, source: "social/UPLOADS.json" })]);
    expect(d.host).toHaveBeenCalledWith("/tmp/hand.mp4", "social/hand0000001.mp4");
    expect(client.createPost).toHaveBeenCalledTimes(3);
    expect(Object.keys(mem.get().videos.hand0000001.channels)).toEqual(["instagram", "facebook", "threads"]);
  });

  it("dry run plans it but hosts and posts nothing", async () => {
    const client = fakeClient();
    const d = deps({ client, videos: [handShort, LONG], scheduled: [handShort], findMedia: () => hint });
    const out = await runBufferCheck(d, { dryRun: true });
    expect(out.autoMirrored).toEqual([expect.objectContaining({ videoId: "hand0000001", sent: false })]);
    expect(d.host).not.toHaveBeenCalled();
    expect(client.createPost).not.toHaveBeenCalled();
  });

  it("reports, and never guesses, when the Short has no long or no file", async () => {
    const noLong = await runBufferCheck(deps({ videos: [handShort], scheduled: [handShort], findMedia: () => ({ ...hint, longId: null }) }));
    expect(noLong.unmirrored[0].reason).toMatch(/needs --long/);
    const noFile = await runBufferCheck(deps({ videos: [handShort], scheduled: [handShort], findMedia: () => null }));
    expect(noFile.unmirrored[0].reason).toMatch(/no local file recorded/);
    expect(noFile.autoMirrored).toEqual([]);
  });

  it("leaves videos already in Buffer alone", async () => {
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ store: mem.store }));
    const findMedia = vi.fn(() => hint);
    const out = await runBufferCheck(deps({ store: mem.store, scheduled: [video()], findMedia }));
    expect(findMedia).not.toHaveBeenCalled();
    expect(out.autoMirrored).toEqual([]);
    expect(out.unmirrored).toEqual([]);
  });
});

describe("Blob clean-up", () => {
  const BLOB = "https://abc.public.blob.vercel-storage.com/social/short0000001.mp4";
  // After the Short (5 Oct 10:30) and the long (4 Oct 17:00) are due; within the 14 days.
  const AFTER = new Date("2026-10-06T09:00:00Z");

  async function mirroredWith(client: ReturnType<typeof fakeClient>, deleteMedia = vi.fn(async () => undefined)) {
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ store: mem.store, client, deleteMedia }));
    return { mem, deleteMedia };
  }

  it("remembers the Blob copy after posting", async () => {
    const { mem, deleteMedia } = await mirroredWith(fakeClient());
    expect(mem.get().videos.short0000001.media).toBe(BLOB);
    expect(deleteMedia).not.toHaveBeenCalled();
  });

  it("deletes it once every Buffer post has been sent", async () => {
    const { mem } = await mirroredWith(fakeClient());
    const deleteMedia = vi.fn(async () => undefined);
    const sent = fakeClient(undefined, { post1: "sent", post2: "sent", post3: "sent" });
    const out = await runBufferCheck(deps({ store: mem.store, client: sent, deleteMedia, now: () => AFTER }));
    expect(deleteMedia).toHaveBeenCalledWith(BLOB);
    expect(out.mediaCleaned).toEqual([{ videoId: "short0000001", url: BLOB, reason: "every Buffer post has been sent", deleted: true }]);
    expect(mem.get().videos.short0000001.media).toBeUndefined();
    expect(Object.keys(mem.get().videos.short0000001.channels)).toHaveLength(3);
  });

  it("keeps it while a post is still scheduled or errored, and when dry", async () => {
    const { mem } = await mirroredWith(fakeClient());
    const deleteMedia = vi.fn(async () => undefined);
    const at = { now: () => AFTER };
    await runBufferCheck(deps({ store: mem.store, client: fakeClient(undefined, { post1: "sent", post2: "error", post3: "sent" }), deleteMedia, ...at }));
    await runBufferCheck(deps({ store: mem.store, client: fakeClient(undefined, { post1: "sent", post2: "scheduled", post3: "sent" }), deleteMedia, ...at }));
    const dry = await runBufferCheck(deps({ store: mem.store, client: fakeClient(undefined, { post1: "sent", post2: "sent", post3: "sent" }), deleteMedia, ...at }), { dryRun: true });
    expect(deleteMedia).not.toHaveBeenCalled();
    expect(dry.mediaCleaned).toEqual([expect.objectContaining({ deleted: false })]);
    expect(mem.get().videos.short0000001.media).toBe(BLOB);
  });

  it("doesn't ask Buffer about posts that aren't due yet", async () => {
    const { mem } = await mirroredWith(fakeClient());
    const client = fakeClient(undefined, { post1: "sent", post2: "sent", post3: "sent" });
    const deleteMedia = vi.fn(async () => undefined);
    const out = await runBufferCheck(deps({ store: mem.store, client, deleteMedia }));
    expect(client.getPostStatus).not.toHaveBeenCalled();
    expect(out.mediaCleaned).toEqual([]);
  });

  it("deletes it 14 days after go-public, even if a post errored", async () => {
    const { mem } = await mirroredWith(fakeClient());
    const deleteMedia = vi.fn(async () => undefined);
    const later = new Date(Date.parse("2026-10-05T10:30:00Z") + 15 * 24 * 3600 * 1000);
    const out = await runBufferCheck(deps({ store: mem.store, client: fakeClient(undefined, { post2: "error" }), deleteMedia, now: () => later }));
    expect(out.mediaCleaned[0].reason).toMatch(/14 days/);
    expect(deleteMedia).toHaveBeenCalledWith(BLOB);
  });

  it("deletes every copy of a long with a trailer once its posts have been sent", async () => {
    const long = video({ id: "long0000002", durationSeconds: 594, publishAt: "2026-10-04T17:00:00Z" });
    const mem = memoryStore();
    await mirrorVideo({ videoId: "long0000002", thumbPath: "/tmp/thumb.jpg", trailerPath: "/tmp/trailer.mp4" }, deps({ videos: [long], store: mem.store }));
    const deleteMedia = vi.fn(async () => undefined);
    const sent = fakeClient(undefined, { post1: "sent", post2: "sent", post3: "sent" });
    const out = await runBufferCheck(deps({ videos: [long], store: mem.store, client: sent, deleteMedia, now: () => AFTER }));
    expect(deleteMedia).toHaveBeenCalledTimes(2);
    expect(out.mediaCleaned.map((m) => m.deleted)).toEqual([true, true]);
    expect(mem.get().videos.long0000002.media).toBeUndefined();
  });

  it("keeps a second copy uploaded for a video in Buffer with that video", async () => {
    // Real 11-character id: Blob paths are matched to videos by it.
    const mem = memoryStore();
    const plan = { videoId: "xQlV9G9lqLI", kind: "long" as const, title: "T", timing: { mode: "customScheduled" as const, dueAt: "2026-10-05T10:30:00.000Z" } };
    for (const [c, id] of [["instagram", "p1"], ["facebook", "p2"], ["threads", "p3"]] as const) await mem.store.record(plan, c, id);
    const thumb = "https://abc.public.blob.vercel-storage.com/social/xQlV9G9lqLI-thumb-a1.jpg";
    const trailer = "https://abc.public.blob.vercel-storage.com/social/xQlV9G9lqLI-trailer-b2.mp4";
    await mem.store.setMedia("xQlV9G9lqLI", [thumb]);
    const listMedia = vi.fn(async () => [
      { url: thumb, pathname: "social/xQlV9G9lqLI-thumb-a1.jpg", uploadedAt: new Date("2026-09-20T09:00:00Z") },
      { url: trailer, pathname: "social/xQlV9G9lqLI-trailer-b2.mp4", uploadedAt: new Date("2026-09-20T09:00:00Z") },
    ]);
    const deleteMedia = vi.fn(async () => undefined);
    const out = await runBufferCheck(
      deps({ store: mem.store, client: fakeClient(), deleteMedia, listMedia, videos: [video({ id: "xQlV9G9lqLI", durationSeconds: 600 })] }),
    );
    expect(out.mediaCleaned).toEqual([]);
    expect(deleteMedia).not.toHaveBeenCalled();
    expect(mem.get().videos.xQlV9G9lqLI.media).toEqual([thumb, trailer]);
  });

  it("deletes it when the video is pulled and its posts removed", async () => {
    const { mem } = await mirroredWith(fakeClient());
    const deleteMedia = vi.fn(async () => undefined);
    const out = await runBufferCheck(deps({ store: mem.store, client: fakeClient(), deleteMedia, videos: [video({ publishAt: null })] }));
    expect(out.mediaCleaned).toEqual([expect.objectContaining({ reason: "its Buffer posts were removed", deleted: true })]);
    expect(mem.get().videos.short0000001).toBeUndefined();
  });

  it("deletes an uploaded file straight away when no post was created", async () => {
    const deleteMedia = vi.fn(async () => undefined);
    const failAll = {
      ...fakeClient(),
      createPost: vi.fn(async () => {
        throw new Error("Buffer InvalidInputError: bad video");
      }),
    };
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, deps({ store: mem.store, client: failAll, deleteMedia }));
    expect(deleteMedia).toHaveBeenCalledWith(BLOB);
    // Without a Buffer key it only plans, so nothing is uploaded (or deleted).
    const noKey = deps({ client: null, deleteMedia: vi.fn(async () => undefined) });
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaPath: "/tmp/short.mp4" }, noKey);
    expect(noKey.host).not.toHaveBeenCalled();
    expect(noKey.deleteMedia).not.toHaveBeenCalled();
  });

  it("never touches files that aren't the mirror's own Blob copies", async () => {
    const mem = memoryStore();
    await mirrorVideo({ videoId: "short0000001", longId: "long0000001", mediaUrl: "https://cdn.example.com/social/short.mp4" }, deps({ store: mem.store }));
    expect(mem.get().videos.short0000001.media).toBeUndefined();
  });

  it("adopts an untracked copy by its YouTube id, and sweeps old orphans", async () => {
    expect(videoIdFromBlobPath("social/xQlV9G9lqLI-a1B2c3.mp4")).toBe("xQlV9G9lqLI");
    expect(videoIdFromBlobPath("other/file.mp4")).toBeNull();
    // A video posted before clean-up existed (real 11-character id): its record has no media yet.
    const mem = memoryStore();
    const plan = { videoId: "xQlV9G9lqLI", kind: "short" as const, title: "T", timing: { mode: "customScheduled" as const, dueAt: "2026-10-05T10:30:00.000Z" } };
    for (const [c, id] of [["instagram", "p1"], ["facebook", "p2"], ["threads", "p3"]] as const) await mem.store.record(plan, c, id);
    const adopted = "https://abc.public.blob.vercel-storage.com/social/xQlV9G9lqLI-a1B2c3.mp4";
    const deleteMedia = vi.fn(async () => undefined);
    const listMedia = vi.fn(async () => [
      { url: adopted, pathname: "social/xQlV9G9lqLI-a1B2c3.mp4", uploadedAt: new Date("2026-09-28T09:00:00Z") },
      { url: "https://abc.public.blob.vercel-storage.com/social/gone0000001-x.mp4", pathname: "social/gone0000001-x.mp4", uploadedAt: new Date("2026-09-20T09:00:00Z") },
      { url: "https://abc.public.blob.vercel-storage.com/social/newx0000001-y.mp4", pathname: "social/newx0000001-y.mp4", uploadedAt: new Date("2026-10-01T08:30:00Z") },
    ]);
    const out = await runBufferCheck(
      deps({ store: mem.store, client: fakeClient(), deleteMedia, listMedia, videos: [video({ id: "xQlV9G9lqLI" })] }),
    );
    expect(mem.get().videos.xQlV9G9lqLI.media).toBe(adopted);
    expect(out.mediaCleaned).toEqual([expect.objectContaining({ videoId: "gone0000001", reason: expect.stringMatching(/orphaned/), deleted: true })]);
    expect(deleteMedia).toHaveBeenCalledTimes(1);
  });
});
