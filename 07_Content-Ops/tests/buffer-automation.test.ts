import { describe, expect, it, vi } from "vitest";
import { createBufferApiClient, type BufferClient } from "../src/lib/publishing/buffer-api";
import fs from "fs";
import os from "os";
import path from "path";
import { createFileBufferStore, type BufferStore } from "../src/lib/publishing/buffer-store";
import { mirrorVideo, runBufferCheck, type MirrorDeps } from "../src/lib/publishing/buffer-runner";
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
      };
    },
  };
  return { store, get: () => ledger };
}

function fakeClient(failOn?: string) {
  let n = 0;
  const client = {
    createPost: vi.fn(async (input: Record<string, unknown>) => {
      if (failOn && input.channelId === failOn) throw new Error("Buffer InvalidInputError: bad video");
      n += 1;
      return { id: `post${n}`, dueAt: (input.dueAt as string) ?? null, status: "scheduled" };
    }),
    editPost: vi.fn(async ({ postId, dueAt }: { postId: string; mode: string; dueAt: string }) => ({ id: postId, dueAt, status: "scheduled" })),
    deletePost: vi.fn(async () => undefined),
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
    expect((d.client as ReturnType<typeof fakeClient>).createPost).not.toHaveBeenCalled();
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
    expect(d.host).toHaveBeenCalledWith("/tmp/thumb.jpg", "social/long0000002.jpg");
    expect(d.checkUrl).toHaveBeenCalledWith(expect.any(String), "image");
    expect(out.results.every((r) => r.ok && r.action === "create_post")).toBe(true);
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
