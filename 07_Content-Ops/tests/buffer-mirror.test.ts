import { describe, expect, it } from "vitest";
import {
  Ledger,
  YouTubeVideo,
  DEFAULT_COVER_MS,
  DEFAULT_QUESTION,
  buildText,
  hashtags,
  isBufferOnlyPlatform,
  openingParagraph,
  parseIsoDuration,
  planBufferMirror,
  reconcileEntry,
  recordPost,
} from "../src/lib/publishing/buffer-mirror";

const NOW = new Date("2026-10-01T09:00:00Z");
const CHANNELS = { instagram: "ig000000000000000000000a", facebook: "fb000000000000000000000b", threads: "th000000000000000000000c" };
const EMPTY: Ledger = { version: 1, videos: {} };
const MEDIA = "https://abc.public.blob.vercel-storage.com/social/short.mp4";
const THUMB = "https://abc.public.blob.vercel-storage.com/social/long.jpg";
const TRAILER = "https://abc.public.blob.vercel-storage.com/social/long-trailer.mp4";

function video(over: Partial<YouTubeVideo> = {}): YouTubeVideo {
  return {
    id: "short0000001",
    title: "Why You Can't Stand on a Neutron Star",
    description:
      "One teaspoon of it weighs as much as a mountain.\n\nFull film: https://youtu.be/Yk1tLh23rko\n\nSources:\nNASA https://nasa.gov",
    tags: ["neutron star", "space", "astronomy", "Orbit With Ben", "physics", "stars", "gravity"],
    durationSeconds: 27,
    privacyStatus: "private",
    publishAt: "2026-10-05T10:30:00Z",
    publishedAt: null,
    containsSyntheticMedia: true,
    ...over,
  };
}

const LONG_PUBLIC = { id: "long0000001", goesPublicAt: "2026-10-04T17:00:00Z" };

describe("buffer mirror: text", () => {
  it("takes the opening paragraph without links or sources", () => {
    expect(openingParagraph(video().description)).toBe("One teaspoon of it weighs as much as a mountain.");
    expect(openingParagraph("0:00 Intro\n0:40 Fall\n\nThe real hook.")).toBe("The real hook.");
  });

  it("turns tags into hashtags within each platform's limit", () => {
    expect(hashtags(video().tags, 5)).toEqual(["#NeutronStar", "#Space", "#Astronomy", "#OrbitWithBen", "#Physics"]);
    expect(hashtags(["Space", "space", "!!!"], 5)).toEqual(["#Space"]);
    expect(buildText(video(), "threads", "short").match(/#/g)).toHaveLength(1);
  });

  it("keeps Threads under 500 characters, shortening only the body", () => {
    const long = video({ description: "word ".repeat(300) });
    const text = buildText(long, "threads", "long", { youtubeUrl: "https://youtu.be/long0000001" });
    expect(text.length).toBeLessThanOrEqual(500);
    expect(text.startsWith("Why You Can't Stand")).toBe(true);
    expect(text).toContain(DEFAULT_QUESTION);
    expect(text).toContain("Watch the film: https://youtu.be/long0000001");
    expect(text).toMatch(/#NeutronStar$/);
  });

  it("opens with the social hook and ends the body with a question", () => {
    const plain = buildText(video(), "instagram", "short");
    expect(plain.split("\n\n")).toEqual([
      "Why You Can't Stand on a Neutron Star",
      "One teaspoon of it weighs as much as a mountain.",
      DEFAULT_QUESTION,
      "#NeutronStar #Stars #Space #Astronomy #OrbitWithBen",
    ]);
    const own = buildText(video(), "facebook", "short", { social: { hook: "A teaspoon of this star outweighs Everest.", question: "Would you pick it up?" } });
    expect(own.split("\n\n")[0]).toBe("A teaspoon of this star outweighs Everest.");
    expect(own).toContain("Would you pick it up?");
    expect(own).not.toContain(DEFAULT_QUESTION);
  });

  it("leads with the tag that names the subject, wherever it sits in the YouTube tags", () => {
    const v = video({
      title: "This Star Is 20 km Wide and Heavier Than the Sun",
      description: "Why You Can't Stand on a Neutron Star",
      tags: ["Orbit With Ben", "animated science", "astronomy", "astrophysics", "black holes", "neutron star", "pulsar"],
    });
    expect(buildText(v, "instagram", "short").split("\n\n").at(-1)).toBe("#NeutronStar #OrbitWithBen #AnimatedScience #Astronomy #Astrophysics");
    expect(buildText(v, "threads", "short").split("\n\n").at(-1)).toBe("#NeutronStar");
  });

  it("never prints the same line twice", () => {
    const v = video({ title: "How Long Until Andromeda Hits Us?", description: "How long until Andromeda hits us?\n\nFull film: https://youtu.be/x" });
    // No hook: the title would be printed twice, so the description line goes.
    expect(buildText(v, "instagram", "short").split("\n\n")[1]).toBe(DEFAULT_QUESTION);
    // With a hook, the title line gives it context, so it stays.
    const hooked = buildText(v, "instagram", "short", { social: { hook: "Andromeda is coming toward us at 110 km every second." } });
    expect(hooked.split("\n\n").slice(0, 2)).toEqual(["Andromeda is coming toward us at 110 km every second.", "How long until Andromeda hits us?"]);
    // Nor when the description line is the question itself.
    const asked = buildText(v, "instagram", "short", { social: { hook: "Andromeda is coming.", question: "How long until Andromeda hits us?" } });
    expect(asked.match(/How long until Andromeda hits us\?/gi)).toHaveLength(1);
  });

  it("points each platform to the full film its own way", () => {
    const long = video({ id: "long0000001", durationSeconds: 724 });
    expect(buildText(long, "instagram", "long")).toContain("New film on YouTube. Link in bio.");
    expect(buildText(long, "instagram", "long", { trailer: true })).toContain("Full film on YouTube. Link in bio.");
    expect(buildText(long, "facebook", "long", { trailer: true, youtubeUrl: "https://youtu.be/long0000001" })).toContain("Full film: https://youtu.be/long0000001");
    expect(buildText(long, "facebook", "long")).not.toContain("YouTube");
  });

  it("parses YouTube durations", () => {
    expect(parseIsoDuration("PT27S")).toBe(27);
    expect(parseIsoDuration("PT12M4S")).toBe(724);
    expect(parseIsoDuration("PT1H")).toBe(3600);
  });
});

describe("buffer mirror: plan", () => {
  it("schedules a Short on all three channels at the YouTube publish time", () => {
    const plan = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC });
    expect(plan.errors).toEqual([]);
    expect(plan.kind).toBe("short");
    const creates = plan.actions.filter((a) => a.action === "create_post");
    expect(creates.map((a) => a.channel)).toEqual(["instagram", "facebook", "threads"]);
    for (const a of creates) {
      if (a.action !== "create_post") continue;
      expect(a.input.mode).toBe("customScheduled");
      expect(a.input.dueAt).toBe("2026-10-05T10:30:00.000Z");
      expect(a.input.schedulingType).toBe("automatic");
      expect(a.input.assets).toEqual([expect.objectContaining({ video: expect.objectContaining({ url: MEDIA }) })]);
    }
    const ig = creates.find((a) => a.channel === "instagram");
    expect(ig?.action === "create_post" && ig.input.metadata).toEqual({
      instagram: { type: "reel", shouldShareToFeed: true, isAiGenerated: true },
    });
  });

  it("never plans a Short before its long is public", () => {
    const plan = planBufferMirror({
      video: video({ publishAt: "2026-10-03T10:30:00Z" }),
      channelIds: CHANNELS,
      ledger: EMPTY,
      now: NOW,
      mediaUrl: MEDIA,
      parentLong: LONG_PUBLIC,
    });
    expect(plan.actions).toEqual([]);
    expect(plan.errors.join()).toMatch(/before its long/);
  });

  it("needs a long (or --standalone) and a direct public media URL for a Short", () => {
    const noLong = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA });
    expect(noLong.errors.join()).toMatch(/--long/);
    const drive = planBufferMirror({
      video: video(),
      channelIds: CHANNELS,
      ledger: EMPTY,
      now: NOW,
      standalone: true,
      mediaUrl: "https://drive.google.com/file/d/abc/view",
    });
    expect(drive.errors.join()).toMatch(/share page/);
    expect(drive.actions).toEqual([]);
  });

  it("mirrors a long with no trailer: thumbnail on Instagram and Threads, link card on Facebook", () => {
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, thumbUrl: THUMB });
    expect(plan.errors).toEqual([]);
    const byChannel = Object.fromEntries(plan.actions.map((a) => [a.channel, a]));
    const alt = `Thumbnail for the Orbit With Ben film "${long.title}"`;
    expect(byChannel.facebook).toMatchObject({
      input: { assets: [], metadata: { facebook: { type: "post", linkAttachment: { url: "https://youtu.be/long0000001" } } } },
    });
    expect(byChannel.threads).toMatchObject({ input: { assets: [{ image: { url: THUMB, metadata: { altText: alt } } }] } });
    expect((byChannel.threads as unknown as { input: Record<string, unknown> }).input.metadata).toBeUndefined();
    expect((byChannel.threads as unknown as { input: { text: string } }).input.text).toContain("https://youtu.be/long0000001");
    expect(byChannel.instagram).toMatchObject({
      input: { assets: [{ image: { url: THUMB, metadata: { altText: alt } } }], metadata: { instagram: { type: "post" } } },
    });
  });

  it("uses the alt text given for the thumbnail", () => {
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const alt = "Jupiter's orange cloud bands, with the words NO FLOOR.";
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, thumbUrl: THUMB, social: { alt } });
    expect(plan.actions[0]).toMatchObject({ channel: "instagram", input: { assets: [{ image: { metadata: { altText: alt } } }] } });
  });

  it("posts a long's trailer as a Reel on Instagram and Facebook, with the film link in Facebook's text", () => {
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, thumbUrl: THUMB, trailerUrl: TRAILER });
    expect(plan.errors).toEqual([]);
    const byChannel = Object.fromEntries(plan.actions.map((a) => [a.channel, a]));
    expect(byChannel.instagram).toMatchObject({
      input: {
        assets: [{ video: { url: TRAILER, metadata: { thumbnailOffset: DEFAULT_COVER_MS } } }],
        metadata: { instagram: { type: "reel", shouldShareToFeed: true } },
      },
    });
    expect(byChannel.facebook).toMatchObject({
      input: {
        assets: [{ video: { url: TRAILER } }],
        metadata: { facebook: { type: "reel" } },
      },
    });
    expect((byChannel.facebook as unknown as { input: { text: string } }).input.text).toContain("Full film: https://youtu.be/long0000001");
    // Buffer's free plan rejects first comments.
    expect(JSON.stringify(plan.actions)).not.toContain("firstComment");
    expect(byChannel.threads).toMatchObject({ input: { assets: [{ image: { url: THUMB } }] } });
  });

  it("posts a long's trailer on Instagram even with no thumbnail", () => {
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, trailerUrl: TRAILER });
    expect(plan.actions.map((a) => `${a.channel}:${a.action}`)).toEqual(["instagram:create_post", "facebook:create_post", "threads:create_post"]);
    expect(plan.actions[2]).toMatchObject({ input: { metadata: { threads: { linkAttachment: { url: "https://youtu.be/long0000001" } } } } });
    const bad = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, trailerUrl: "https://drive.google.com/file/x" });
    expect(bad.errors.join()).toMatch(/--trailer-url/);
  });

  it("warns when a new post has no hook, no question, or (for a long) no trailer", () => {
    const base = { video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC };
    expect(planBufferMirror(base).warnings.join()).toMatch(/no social hook.*no social question/);
    expect(planBufferMirror({ ...base, social: { hook: "h", question: "q?" } }).warnings).toEqual([]);
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW, thumbUrl: THUMB, social: { hook: "h", question: "q?" } });
    expect(plan.warnings.join()).toMatch(/no trailer/);
    expect(plan.errors).toEqual([]);
  });

  it("points every Short post to its full film on YouTube", () => {
    const plan = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC });
    const by = Object.fromEntries(plan.actions.map((a) => [a.channel, a as unknown as { input: { text: string; metadata?: Record<string, Record<string, unknown>> } }]));
    expect(by.instagram.input.text).toContain("Full film on YouTube. Link in bio.");
    expect(by.facebook.input.text).toContain("Full film: https://youtu.be/long0000001");
    expect(by.facebook.input.metadata?.facebook.firstComment).toBeUndefined();
    expect(by.threads.input.text).toContain("Full film: https://youtu.be/long0000001");
    // A standalone Short has no film to point to.
    const alone = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true });
    expect(JSON.stringify(alone.actions)).not.toContain("youtu.be");
  });

  it("refuses the manifest template's placeholder copy", () => {
    const base = { video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC };
    const plan = planBufferMirror({ ...base, social: { hook: "REPLACE: one short line that stops the scroll" } });
    expect(plan.errors.join()).toMatch(/social.hook is still the template placeholder/);
    expect(plan.actions).toEqual([]);
  });

  it("sets the Reel cover a second in, or where the video says", () => {
    const base = { video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC };
    expect(planBufferMirror(base).actions[0]).toMatchObject({ input: { assets: [{ video: { metadata: { thumbnailOffset: 1000 } } }] } });
    expect(planBufferMirror({ ...base, social: { coverMs: 2500 } }).actions[0]).toMatchObject({
      input: { assets: [{ video: { metadata: { thumbnailOffset: 2500 } } }] },
    });
  });

  it("skips Instagram on a long without a thumbnail or trailer, but still posts the link cards", () => {
    const long = video({ id: "long0000001", durationSeconds: 724, publishAt: "2026-10-04T17:00:00Z" });
    const plan = planBufferMirror({ video: long, channelIds: CHANNELS, ledger: EMPTY, now: NOW });
    expect(plan.errors).toEqual([]);
    expect(plan.actions.map((a) => `${a.channel}:${a.action}`)).toEqual(["instagram:skip", "facebook:create_post", "threads:create_post"]);
    expect(plan.actions[2]).toMatchObject({ input: { metadata: { threads: { linkAttachment: { url: "https://youtu.be/long0000001" } } } } });
  });

  it("refuses back catalogue, too-close times and videos not going public", () => {
    const old = video({ privacyStatus: "public", publishAt: null, publishedAt: "2026-09-20T10:00:00Z" });
    expect(planBufferMirror({ video: old, channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true }).errors.join()).toMatch(
      /back catalogue/,
    );
    const soon = video({ publishAt: "2026-10-01T09:05:00Z" });
    expect(planBufferMirror({ video: soon, channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true }).errors.join()).toMatch(
      /under 10 minutes/,
    );
    const priv = video({ publishAt: null });
    expect(planBufferMirror({ video: priv, channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true }).errors.join()).toMatch(
      /nothing to mirror/,
    );
  });

  it("shares a just-published video now", () => {
    const fresh = video({ privacyStatus: "public", publishAt: null, publishedAt: "2026-10-01T08:30:00Z" });
    const plan = planBufferMirror({ video: fresh, channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true });
    expect(plan.errors).toEqual([]);
    expect(plan.actions.every((a) => a.action === "create_post" && a.input.mode === "shareNow" && !("dueAt" in a.input))).toBe(true);
  });

  it("errors when a Buffer channel id is missing", () => {
    const plan = planBufferMirror({ video: video(), channelIds: { instagram: CHANNELS.instagram }, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, standalone: true });
    expect(plan.errors.join()).toMatch(/facebook/);
    expect(plan.actions).toEqual([]);
  });
});

describe("buffer mirror: ledger", () => {
  const base = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger: EMPTY, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC });
  let ledger = EMPTY;
  ledger = recordPost(ledger, base, "instagram", "p-ig", NOW);
  ledger = recordPost(ledger, base, "facebook", "p-fb", NOW);
  ledger = recordPost(ledger, base, "threads", "p-th", NOW);

  it("never posts the same video twice", () => {
    const again = planBufferMirror({ video: video(), channelIds: CHANNELS, ledger, now: NOW, mediaUrl: MEDIA, parentLong: LONG_PUBLIC });
    expect(again.actions.every((a) => a.action === "skip")).toBe(true);
  });

  it("moves the Buffer posts when the YouTube time moves", () => {
    const moved = video({ publishAt: "2026-10-06T10:30:00Z" });
    const actions = reconcileEntry(moved.id, ledger.videos[moved.id], moved, NOW);
    expect(actions).toEqual([
      { action: "edit_post", channel: "instagram", input: { postId: "p-ig", mode: "customScheduled", dueAt: "2026-10-06T10:30:00.000Z" } },
      { action: "edit_post", channel: "facebook", input: { postId: "p-fb", mode: "customScheduled", dueAt: "2026-10-06T10:30:00.000Z" } },
      { action: "edit_post", channel: "threads", input: { postId: "p-th", mode: "customScheduled", dueAt: "2026-10-06T10:30:00.000Z" } },
    ]);
  });

  it("takes the Buffer posts down when the video no longer goes public", () => {
    const pulled = video({ publishAt: null });
    expect(reconcileEntry(pulled.id, ledger.videos[pulled.id], pulled, NOW).map((a) => a.action)).toEqual([
      "delete_post",
      "delete_post",
      "delete_post",
    ]);
    expect(reconcileEntry(pulled.id, ledger.videos[pulled.id], null, NOW)).toHaveLength(3);
  });

  it("leaves posts alone once they have gone out, or when nothing changed", () => {
    expect(reconcileEntry("short0000001", ledger.videos.short0000001, video(), NOW)).toEqual([]);
    const after = new Date("2026-10-05T11:00:00Z");
    expect(reconcileEntry("short0000001", ledger.videos.short0000001, video({ publishAt: null }), after)).toEqual([]);
  });

  it("drops the entry when every channel is deleted", () => {
    let l = recordPost(ledger, base, "instagram", null, NOW);
    l = recordPost(l, base, "facebook", null, NOW);
    l = recordPost(l, base, "threads", null, NOW);
    expect(l.videos).toEqual({});
  });
});

describe("buffer mirror: worker guard", () => {
  it("blocks every social platform in the app worker, but not YouTube", () => {
    for (const p of ["instagram_reels", "facebook_reels", "threads", "tiktok", "x", "meta"]) expect(isBufferOnlyPlatform(p)).toBe(true);
    expect(isBufferOnlyPlatform("youtube_shorts")).toBe(false);
  });
});
