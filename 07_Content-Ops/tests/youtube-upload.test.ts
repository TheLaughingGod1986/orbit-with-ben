// Studio core (15 Oct 2026): the shared uploader, as both channels use it.
import fs from "fs";
import os from "os";
import path from "path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { retryOn403, uploadToYouTube } from "../src/lib/youtube/upload";

vi.mock("../src/lib/publishing/media/ffprobe", () => ({
  probeVideo: async () => ({}),
  validateForPlatform: () => ({ errors: [], warnings: [] }),
}));

describe("thumbnails.set retry", () => {
  it("retries a 403 up to 3 tries, 60 s apart", async () => {
    const results = [
      { ok: false, message: "processing", status: 403 },
      { ok: false, message: "processing", status: 403 },
      { ok: true, message: "ok", status: 200 },
    ];
    let calls = 0;
    const sleeps: number[] = [];
    const res = await retryOn403(async () => results[calls++], {
      sleep: async (ms) => {
        sleeps.push(ms);
      },
    });
    expect(res.ok).toBe(true);
    expect(calls).toBe(3);
    expect(sleeps).toEqual([60_000, 60_000]);
  });

  it("gives up after 3 tries of 403", async () => {
    let calls = 0;
    const res = await retryOn403(
      async () => {
        calls++;
        return { ok: false, message: "processing", status: 403 };
      },
      { sleep: async () => {} },
    );
    expect(res.ok).toBe(false);
    expect(calls).toBe(3);
  });

  it("does not retry other errors", async () => {
    let calls = 0;
    const res = await retryOn403(
      async () => {
        calls++;
        return { ok: false, message: "bad image", status: 400 };
      },
      { sleep: async () => {} },
    );
    expect(res.status).toBe(400);
    expect(calls).toBe(1);
  });
});

describe("channel settings reach the upload request", () => {
  afterEach(() => vi.restoreAllMocks());

  async function snippetFor(channel: { categoryId: string; defaultLanguage?: string }) {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "yt-up-"));
    const video = path.join(dir, "v.mp4");
    fs.writeFileSync(video, "x");
    const bodies: string[] = [];
    vi.spyOn(globalThis, "fetch").mockImplementation(async (_url, init) => {
      if (init?.method === "POST") {
        bodies.push(String(init.body));
        return new Response("{}", { status: 200, headers: { location: "https://upload.example/x" } });
      }
      return new Response(JSON.stringify({ id: "vid123" }), { status: 200 });
    });
    const res = await uploadToYouTube(
      {
        id: "x", platform: "youtube_shorts", title: "T", caption: "D", uploadStatus: "ready",
        privacyStatus: "private", madeForKids: false, mediaFilePath: video,
      },
      { accessToken: "tok", dryRun: false, channel },
    );
    expect(res.success).toBe(true);
    return JSON.parse(bodies[0]).snippet;
  }

  it("Orbit With Ben: Science & Technology, no language set", async () => {
    const snippet = await snippetFor({ categoryId: "28" });
    expect(snippet.categoryId).toBe("28");
    expect(snippet.defaultLanguage).toBeUndefined();
  });

  it("History of Science: Education, en-GB title and audio", async () => {
    const snippet = await snippetFor({ categoryId: "27", defaultLanguage: "en-GB" });
    expect(snippet.categoryId).toBe("27");
    expect(snippet.defaultLanguage).toBe("en-GB");
    expect(snippet.defaultAudioLanguage).toBe("en-GB");
  });
});
