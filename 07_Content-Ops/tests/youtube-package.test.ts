import { describe, expect, it } from "vitest";
import fs from "fs";
import os from "os";
import path from "path";
import {
  buildStudioFinishChecklist,
  loadYouTubePackage,
  mergeDescriptionWithChapters,
  parseTagsFile,
  parseTitleAbcSheet,
} from "../src/lib/publishing/youtube-package";

describe("youtube package parsers", () => {
  it("parses title ABC sheet with recommended A", () => {
    const text = `A — RECOMMENDED
JWST Found Galaxies That Shouldn't Exist Yet | Orbit's Cosmic Journey

B — ALT
The Early Universe Was Busier Than It Should Have Been | Orbit's Cosmic Journey

C — FALLBACK
Why Did the Early Universe Look Too Busy for JWST? | Orbit's Cosmic Journey
`;
    const parsed = parseTitleAbcSheet(text);
    expect(parsed.titles).toHaveLength(3);
    expect(parsed.recommended).toContain("Shouldn't Exist");
  });

  it("parses comma tags and merges chapters when missing", () => {
    expect(parseTagsFile("jwst, early universe, orbit")).toEqual([
      "jwst",
      "early universe",
      "orbit",
    ]);
    const merged = mergeDescriptionWithChapters("Hook line", "0:00 — Open\n1:00 — Dawn");
    expect(merged).toContain("Chapters");
    expect(merged).toContain("0:00 — Open");
    const already = mergeDescriptionWithChapters("Chapters\n0:00 — X", "1:00 — Y");
    expect(already).not.toContain("1:00 — Y");
  });
});

describe("studio finish checklist", () => {
  it("marks API steps done and Studio pin/ABC/related pending", () => {
    const checklist = buildStudioFinishChecklist({
      videoId: "abc123",
      format: "longform",
      titleAbc: ["T1", "T2", "T3"],
      thumbnailAbc: ["/a.png", "/b.png"],
      pinnedComment: "Pin me",
      relatedVideoId: null,
      firstCommentPosted: true,
      thumbnailSet: true,
      playlistAdded: false,
      playlistId: "PLtest",
    });
    expect(checklist.studioEditUrl).toContain("abc123");
    expect(checklist.items.find((i) => i.id === "api_metadata")?.status).toBe("api_done");
    expect(checklist.items.find((i) => i.id === "title_thumb_abc")?.status).toBe(
      "pending_studio",
    );
    expect(checklist.items.find((i) => i.id === "pin_comment")?.status).toBe("pending_studio");
    expect(checklist.items.find((i) => i.id === "related_watch_next")?.status).toBe("n/a");
    expect(checklist.summary).toMatch(/Studio finish/);
  });

  it("requires Related for Shorts", () => {
    const checklist = buildStudioFinishChecklist({
      videoId: "short1",
      format: "shorts",
      titleAbc: [],
      thumbnailAbc: [],
      pinnedComment: null,
      relatedVideoId: "long1",
      firstCommentPosted: false,
      thumbnailSet: false,
      playlistAdded: false,
      playlistId: null,
    });
    expect(checklist.items.find((i) => i.id === "related_watch_next")?.required).toBe(true);
    expect(checklist.items.find((i) => i.id === "title_thumb_abc")?.status).toBe("n/a");
  });
});

describe("loadYouTubePackage", () => {
  it("loads package dirs with Titles/Descriptions/Tags", () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "yt-pkg-"));
    const video = path.join(root, "video.mp4");
    fs.writeFileSync(video, "fake");
    fs.mkdirSync(path.join(root, "Titles"));
    fs.mkdirSync(path.join(root, "Descriptions"));
    fs.mkdirSync(path.join(root, "Tags"));
    fs.mkdirSync(path.join(root, "Pinned-Comments"));
    fs.writeFileSync(
      path.join(root, "Titles", "title_abc_v01.txt"),
      "A — RECOMMENDED\nHello Space | Orbit's Cosmic Journey\n\nB — ALT\nAlt Title | Orbit's Cosmic Journey\n",
    );
    fs.writeFileSync(path.join(root, "Descriptions", "long_description_v01.txt"), "Desc body");
    fs.writeFileSync(path.join(root, "Tags", "tags_v01.txt"), "space,orbit,jwst");
    fs.writeFileSync(path.join(root, "Pinned-Comments", "pin_v01.txt"), "Please pin");

    const pkg = loadYouTubePackage({
      packageDir: root,
      videoPath: video,
      overrides: { format: "longform", schedule: "2026-08-20T18:00:00.000Z" },
    });
    expect(pkg.title).toContain("Hello Space");
    expect(pkg.tags).toContain("jwst");
    expect(pkg.pinnedComment).toBe("Please pin");
    expect(pkg.scheduledAt?.toISOString()).toBe("2026-08-20T18:00:00.000Z");
  });
  it("keeps manifest values when CLI flags are unset (undefined)", () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "yt-pkg-"));
    const video = path.join(root, "short.mp4");
    fs.writeFileSync(video, "fake");
    fs.writeFileSync(
      path.join(root, "PACKAGE_MANIFEST.json"),
      JSON.stringify({
        format: "shorts",
        title: "Could a Robot Survive Touching the Sun?",
        description: "Is the Sun Getting Brighter?",
        tags: ["sun"],
        schedule: "2026-10-21T10:30:00.000Z",
      }),
    );
    const pkg = loadYouTubePackage({
      packageDir: root,
      videoPath: video,
      overrides: { title: undefined, format: undefined, schedule: undefined },
    });
    expect(pkg.title).toBe("Could a Robot Survive Touching the Sun?");
    expect(pkg.format).toBe("shorts");
    expect(pkg.scheduledAt?.toISOString()).toBe("2026-10-21T10:30:00.000Z");
  });
});
