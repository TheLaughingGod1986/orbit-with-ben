import { describe, expect, it, vi, afterEach } from "vitest";
import { resolveYouTubeSchedule, uploadToYouTube, YOUTUBE_SCOPES } from "../src/lib/youtube/upload";
import { upsertEnvLine } from "../scripts/youtube-auth";

describe("YouTube upload (local, no database)", () => {
  it("schedules with publishAt only when far enough ahead", () => {
    const now = new Date("2026-10-01T09:00:00Z");
    expect(resolveYouTubeSchedule(new Date("2026-10-04T17:00:00Z"), now)).toEqual({ usePublishAt: true, publishAtIso: "2026-10-04T17:00:00.000Z" });
    expect(resolveYouTubeSchedule(new Date("2026-10-01T09:05:00Z"), now)).toEqual({ usePublishAt: false });
    expect(resolveYouTubeSchedule(null, now)).toEqual({ usePublishAt: false });
  });

  it("dry run prepares the upload without touching the network", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const result = await uploadToYouTube(
      { id: "x", platform: "youtube_shorts", title: "T", caption: "D", uploadStatus: "ready", privacyStatus: "private", madeForKids: false, scheduledAt: new Date(Date.now() + 86_400_000) },
      { accessToken: "", dryRun: true },
    );
    expect(result.success).toBe(true);
    expect(result.scheduledOnPlatform).toBe(true);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("refuses a dry run without the kids flag", async () => {
    const result = await uploadToYouTube({ id: "x", platform: "youtube_shorts", title: "T", uploadStatus: "ready", privacyStatus: "private" }, { accessToken: "", dryRun: true });
    expect(result.success).toBe(false);
    expect(result.message).toMatch(/madeForKids/);
  });

  it("asks for upload, read and comment scopes", () => {
    expect(YOUTUBE_SCOPES.join(" ")).toMatch(/youtube\.upload.*youtube\.readonly.*youtube\.force-ssl/);
  });
});

describe("youtube-auth .env write", () => {
  afterEach(() => vi.restoreAllMocks());
  it("replaces the token line and leaves every other line alone", () => {
    const before = "GOOGLE_CLIENT_ID=abc\nYOUTUBE_REFRESH_TOKEN=old\nBUFFER_API_KEY=k\n";
    expect(upsertEnvLine(before, "YOUTUBE_REFRESH_TOKEN", "new")).toBe("GOOGLE_CLIENT_ID=abc\nYOUTUBE_REFRESH_TOKEN=new\nBUFFER_API_KEY=k\n");
  });
  it("adds the line when missing, with a newline before it", () => {
    expect(upsertEnvLine("GOOGLE_CLIENT_ID=abc", "YOUTUBE_REFRESH_TOKEN", "t")).toBe("GOOGLE_CLIENT_ID=abc\nYOUTUBE_REFRESH_TOKEN=t\n");
    expect(upsertEnvLine("", "YOUTUBE_REFRESH_TOKEN", "t")).toBe("\nYOUTUBE_REFRESH_TOKEN=t\n");
  });
});
