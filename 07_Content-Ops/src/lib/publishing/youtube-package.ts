import fs from "fs";
import path from "path";
import { redactSummary } from "@/lib/publishing/errors";
import {
  appendAffiliateSectionToDescription,
  type AffiliateDescriptionLink,
} from "@/lib/affiliate/description";

export type YouTubePackageManifest = {
  format?: "longform" | "shorts";
  video?: string;
  title?: string;
  /** Prefer A/B/C letter from Titles/*abc* when title omitted. Default A. */
  titleVariant?: "A" | "B" | "C";
  description?: string;
  descriptionFile?: string;
  tags?: string[];
  tagsFile?: string;
  chapters?: string;
  chaptersFile?: string;
  pinnedComment?: string;
  pinnedCommentFile?: string;
  thumbnail?: string;
  /** Primary + B/C paths for Studio ABC test (API only uploads primary). */
  thumbnailAbc?: string[];
  titleAbc?: string[];
  schedule?: string;
  playlistId?: string;
  /** Shorts Related / watch-next target (Studio-only). */
  relatedVideoId?: string;
  privacy?: "private" | "public" | "unlisted";
  madeForKids?: boolean;
  categoryId?: string;
};

export type ResolvedYouTubePackage = {
  packageDir: string;
  format: "longform" | "shorts";
  videoPath: string;
  title: string;
  titleAbc: string[];
  description: string;
  tags: string[];
  pinnedComment: string | null;
  thumbnailPath: string | null;
  thumbnailAbc: string[];
  scheduledAt: Date | null;
  playlistId: string | null;
  relatedVideoId: string | null;
  privacy: "private" | "public" | "unlisted";
  madeForKids: boolean;
  sources: Record<string, string>;
};

export type StudioFinishItem = {
  id: string;
  required: boolean;
  status: "api_done" | "pending_studio" | "skipped" | "n/a";
  title: string;
  detail: string;
  studioUrlHint?: string;
};

export type StudioFinishChecklist = {
  videoId: string | null;
  studioEditUrl: string | null;
  items: StudioFinishItem[];
  summary: string;
};

function readText(filePath: string): string {
  return fs.readFileSync(filePath, "utf8").replace(/^\uFEFF/, "").trim();
}

function firstExisting(dir: string, predicates: ((name: string) => boolean)[]): string | null {
  if (!fs.existsSync(dir)) return null;
  const names = fs.readdirSync(dir).filter((n) => !n.startsWith("."));
  for (const pred of predicates) {
    const hit = names.find(pred);
    if (hit) return path.join(dir, hit);
  }
  return null;
}

function findInSubdir(packageDir: string, sub: string, predicates: ((name: string) => boolean)[]): string | null {
  return firstExisting(path.join(packageDir, sub), predicates);
}

/** Parse Orbit title ABC sheets (A — RECOMMENDED / title on next line). */
export function parseTitleAbcSheet(text: string): { titles: string[]; recommended: string | null } {
  const lines = text.split(/\r?\n/).map((l) => l.trim());
  const titles: string[] = [];
  let recommended: string | null = null;
  let pendingVariant: "A" | "B" | "C" | null = null;
  let pendingRecommended = false;

  for (const line of lines) {
    if (!line || line.startsWith("#") || line.startsWith("##")) {
      if (line.startsWith("##")) pendingVariant = null;
      continue;
    }
    const header = line.match(/^([ABC])\s*[—\-–:]\s*(.*)$/i);
    if (header) {
      pendingVariant = header[1].toUpperCase() as "A" | "B" | "C";
      pendingRecommended = /recommend/i.test(header[2]);
      const inline = header[2].replace(/^(RECOMMENDED|ALT|FALLBACK)\s*/i, "").trim();
      if (inline && !/^(RECOMMENDED|ALT|FALLBACK)$/i.test(inline) && inline.length > 8) {
        titles.push(inline);
        if (pendingRecommended || pendingVariant === "A") recommended = recommended || inline;
        pendingVariant = null;
      }
      continue;
    }
    if (pendingVariant && line.length > 8 && !/^PRIMARY:|^Thumbnail/i.test(line)) {
      titles.push(line);
      if (pendingRecommended || pendingVariant === "A") recommended = recommended || line;
      pendingVariant = null;
    }
  }

  if (!recommended && titles.length) recommended = titles[0];
  return { titles: titles.slice(0, 3), recommended };
}

export function parseTagsFile(text: string): string[] {
  const raw = text.includes("\n") && !text.includes(",")
    ? text.split(/\r?\n/)
    : text.split(/,/);
  return raw
    .map((t) => t.trim())
    .filter(Boolean)
    .slice(0, 500);
}

export function mergeDescriptionWithChapters(description: string, chapters: string | null): string {
  if (!chapters) return description.trim();
  const desc = description.trim();
  const ch = chapters.trim();
  if (!ch) return desc;
  if (/chapters/i.test(desc) && /\d:\d{2}/.test(desc)) return desc;
  return `${desc}\n\nChapters\n${ch}`.trim();
}

/**
 * Optional affiliate block for YouTube long-form descriptions.
 * Pure merge — callers load placements via `@/lib/affiliate/description-service`.
 * Does not invent links; empty links leave the description unchanged.
 */
export function mergeDescriptionWithAffiliateLinks(
  description: string,
  links: AffiliateDescriptionLink[],
  templates?: Record<string, string>,
): string {
  return appendAffiliateSectionToDescription({
    description,
    links,
    templates,
    useRedirectUrls: true,
  });
}

export function buildStudioFinishChecklist(input: {
  videoId?: string | null;
  format: "longform" | "shorts";
  titleAbc: string[];
  thumbnailAbc: string[];
  pinnedComment: string | null;
  relatedVideoId: string | null;
  firstCommentPosted: boolean;
  thumbnailSet: boolean;
  playlistAdded: boolean;
  playlistId: string | null;
}): StudioFinishChecklist {
  const videoId = input.videoId || null;
  const studioEditUrl = videoId ? `https://studio.youtube.com/video/${videoId}/edit` : null;
  const items: StudioFinishItem[] = [];

  items.push({
    id: "api_metadata",
    required: true,
    status: videoId ? "api_done" : "pending_studio",
    title: "Title · description · tags · schedule · video",
    detail: videoId
      ? "Uploaded via YouTube Data API"
      : "Run package upload first",
  });

  items.push({
    id: "primary_thumbnail",
    required: true,
    status: input.thumbnailSet ? "api_done" : videoId ? "pending_studio" : "skipped",
    title: "Primary thumbnail",
    detail: input.thumbnailSet
      ? "Set via thumbnails.set"
      : "Upload primary thumb in Studio or re-run with --thumbnail",
    studioUrlHint: studioEditUrl || undefined,
  });

  const canAbc =
    input.format === "longform" &&
    (input.titleAbc.length >= 2 || input.thumbnailAbc.length >= 2);
  items.push({
    id: "title_thumb_abc",
    required: input.format === "longform",
    status: !canAbc ? "n/a" : "pending_studio",
    title: "Title + thumbnail ABC (Test & Compare)",
    detail: canAbc
      ? `Studio A/B Testing — titles (${input.titleAbc.length}) · thumbs (${input.thumbnailAbc.length}). Not available via Data API.`
      : input.format === "shorts"
        ? "A/B Testing not available for Shorts"
        : "Provide titleAbc / thumbnailAbc in manifest for Studio finish",
    studioUrlHint: studioEditUrl || undefined,
  });

  items.push({
    id: "first_comment",
    required: Boolean(input.pinnedComment),
    status: !input.pinnedComment
      ? "n/a"
      : input.firstCommentPosted
        ? "api_done"
        : "pending_studio",
    title: "First / pinned comment text",
    detail: !input.pinnedComment
      ? "No pinned comment file in package"
      : input.firstCommentPosted
        ? "commentThreads.insert posted — PIN it in Studio (API cannot pin)"
        : "Post + pin in Studio Comments (API post failed or scope missing)",
    studioUrlHint: videoId
      ? `https://studio.youtube.com/video/${videoId}/comments`
      : undefined,
  });

  items.push({
    id: "pin_comment",
    required: Boolean(input.pinnedComment),
    status: !input.pinnedComment ? "n/a" : "pending_studio",
    title: "Pin the comment",
    detail: "Studio only — no official Data API pin endpoint",
    studioUrlHint: videoId
      ? `https://studio.youtube.com/video/${videoId}/comments`
      : undefined,
  });

  items.push({
    id: "related_watch_next",
    required: input.format === "shorts",
    status:
      input.format !== "shorts"
        ? "n/a"
        : input.relatedVideoId
          ? "pending_studio"
          : "pending_studio",
    title: "Related video (full film)",
    detail: input.relatedVideoId
      ? `Desktop Studio: set Related video to ${input.relatedVideoId} (that Short’s Thursday long only). Pin optional if Related is set.`
      : "Desktop Studio: Content → Short → Related video → that Short’s Thursday long → Save. Required. Pin optional.",
    studioUrlHint: studioEditUrl || undefined,
  });

  items.push({
    id: "end_screens_cards",
    required: input.format === "longform",
    status: input.format === "longform" ? "pending_studio" : "n/a",
    title: "End screen + cards",
    detail: "Studio only — subscribe + best next video",
    studioUrlHint: videoId
      ? `https://studio.youtube.com/video/${videoId}/edit`
      : undefined,
  });

  items.push({
    id: "playlist",
    required: false,
    status: !input.playlistId
      ? "n/a"
      : input.playlistAdded
        ? "api_done"
        : "pending_studio",
    title: "Add to playlist",
    detail: !input.playlistId
      ? "No playlistId in manifest"
      : input.playlistAdded
        ? `Added to ${input.playlistId}`
        : `Add to playlist ${input.playlistId} in Studio`,
  });

  const pending = items.filter((i) => i.status === "pending_studio" && i.required);
  const summary = videoId
    ? pending.length
      ? `API upload done (${videoId}). ${pending.length} required Studio finish step(s) remain.`
      : `API upload done (${videoId}). No required Studio finish steps.`
    : "Package resolved; upload not run yet.";

  return { videoId, studioEditUrl, items, summary };
}

export function loadYouTubePackage(input: {
  packageDir: string;
  videoPath?: string;
  manifestPath?: string;
  overrides?: Partial<YouTubePackageManifest> & {
    schedule?: string;
    thumbnail?: string;
    relatedVideoId?: string;
    playlistId?: string;
    title?: string;
    privacy?: "private" | "public" | "unlisted";
    madeForKids?: boolean;
    format?: "longform" | "shorts";
  };
}): ResolvedYouTubePackage {
  const packageDir = path.resolve(input.packageDir);
  if (!fs.existsSync(packageDir) || !fs.statSync(packageDir).isDirectory()) {
    throw new Error(`Package dir not found: ${packageDir}`);
  }

  const sources: Record<string, string> = {};
  let manifest: YouTubePackageManifest = {};
  const defaultManifest = path.join(packageDir, "PACKAGE_MANIFEST.json");
  const manifestPath = input.manifestPath
    ? path.resolve(input.manifestPath)
    : fs.existsSync(defaultManifest)
      ? defaultManifest
      : null;
  if (manifestPath) {
    manifest = JSON.parse(readText(manifestPath)) as YouTubePackageManifest;
    sources.manifest = manifestPath;
  }
  const merged: YouTubePackageManifest = { ...manifest, ...input.overrides };

  const format = merged.format || "longform";
  const titleVariant = merged.titleVariant || "A";

  let titleAbc = merged.titleAbc?.filter(Boolean) || [];
  let title = merged.title?.trim() || "";
  if (!title || titleAbc.length < 2) {
    const titleFile =
      findInSubdir(packageDir, "Titles", [
        (n) => /title.*abc/i.test(n) && n.endsWith(".txt"),
        (n) => /abc/i.test(n) && n.endsWith(".txt"),
        (n) => n.endsWith(".txt"),
      ]) || null;
    if (titleFile) {
      const parsed = parseTitleAbcSheet(readText(titleFile));
      sources.titleFile = titleFile;
      if (!titleAbc.length) titleAbc = parsed.titles;
      if (!title) {
        if (titleVariant === "B" && parsed.titles[1]) title = parsed.titles[1];
        else if (titleVariant === "C" && parsed.titles[2]) title = parsed.titles[2];
        else title = parsed.recommended || parsed.titles[0] || "";
      }
    }
  }
  if (!title) throw new Error("No title found (manifest.title or Titles/*)");

  let description = merged.description?.trim() || "";
  if (!description) {
    const descFile = merged.descriptionFile
      ? path.resolve(packageDir, merged.descriptionFile)
      : findInSubdir(packageDir, "Descriptions", [
          (n) => /long|description/i.test(n) && n.endsWith(".txt"),
          (n) => n.endsWith(".txt"),
        ]);
    if (descFile && fs.existsSync(descFile)) {
      description = readText(descFile);
      sources.descriptionFile = descFile;
    }
  }

  let chapters: string | null = merged.chapters?.trim() || null;
  if (!chapters) {
    const chFile = merged.chaptersFile
      ? path.resolve(packageDir, merged.chaptersFile)
      : findInSubdir(packageDir, "Chapters", [(n) => n.endsWith(".txt")]);
    if (chFile && fs.existsSync(chFile)) {
      chapters = readText(chFile);
      sources.chaptersFile = chFile;
    }
  }
  description = mergeDescriptionWithChapters(description, chapters);
  if (!description) throw new Error("No description found (Descriptions/* or manifest)");

  let tags = merged.tags?.filter(Boolean) || [];
  if (!tags.length) {
    const tagsFile = merged.tagsFile
      ? path.resolve(packageDir, merged.tagsFile)
      : findInSubdir(packageDir, "Tags", [(n) => n.endsWith(".txt")]);
    if (tagsFile && fs.existsSync(tagsFile)) {
      tags = parseTagsFile(readText(tagsFile));
      sources.tagsFile = tagsFile;
    }
  }

  let pinnedComment = merged.pinnedComment?.trim() || null;
  if (!pinnedComment) {
    const pinFile = merged.pinnedCommentFile
      ? path.resolve(packageDir, merged.pinnedCommentFile)
      : findInSubdir(packageDir, "Pinned-Comments", [(n) => n.endsWith(".txt")]);
    if (pinFile && fs.existsSync(pinFile)) {
      pinnedComment = readText(pinFile);
      sources.pinnedCommentFile = pinFile;
    }
  }

  const videoRel = merged.video;
  const videoPath = path.resolve(
    input.videoPath
      ? input.videoPath
      : videoRel
        ? path.isAbsolute(videoRel)
          ? videoRel
          : path.resolve(packageDir, videoRel)
        : "",
  );
  if (!input.videoPath && !videoRel) {
    throw new Error("Provide --video or manifest.video");
  }
  if (!fs.existsSync(videoPath)) {
    throw new Error(`Video not found: ${videoPath}`);
  }
  sources.video = videoPath;

  let thumbnailPath: string | null = null;
  if (merged.thumbnail) {
    thumbnailPath = path.isAbsolute(merged.thumbnail)
      ? merged.thumbnail
      : path.resolve(packageDir, merged.thumbnail);
  }
  if (thumbnailPath && !fs.existsSync(thumbnailPath)) {
    throw new Error(`Thumbnail not found: ${thumbnailPath}`);
  }
  if (thumbnailPath) sources.thumbnail = thumbnailPath;

  const thumbnailAbc = (merged.thumbnailAbc || [])
    .map((p) => (path.isAbsolute(p) ? p : path.resolve(packageDir, p)))
    .filter((p) => fs.existsSync(p));

  let scheduledAt: Date | null = null;
  if (merged.schedule) {
    scheduledAt = new Date(merged.schedule);
    if (Number.isNaN(scheduledAt.getTime())) {
      throw new Error(`Invalid schedule ISO: ${merged.schedule}`);
    }
  }

  return {
    packageDir,
    format,
    videoPath,
    title,
    titleAbc,
    description,
    tags,
    pinnedComment,
    thumbnailPath,
    thumbnailAbc,
    scheduledAt,
    playlistId: merged.playlistId || null,
    relatedVideoId: merged.relatedVideoId || null,
    privacy: merged.privacy || "private",
    madeForKids: merged.madeForKids ?? false,
    sources,
  };
}

export async function postYouTubeTopLevelComment(input: {
  accessToken: string;
  channelId: string;
  videoId: string;
  text: string;
}): Promise<{ ok: boolean; commentId?: string; message: string }> {
  try {
    const res = await fetch(
      "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          snippet: {
            channelId: input.channelId,
            videoId: input.videoId,
            topLevelComment: {
              snippet: { textOriginal: input.text },
            },
          },
        }),
      },
    );
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      return { ok: false, message: redactSummary(body) };
    }
    const commentId = body?.id || body?.snippet?.topLevelComment?.id;
    return { ok: true, commentId, message: "comment posted (pin in Studio)" };
  } catch (err) {
    return {
      ok: false,
      message: err instanceof Error ? err.message : "comment insert failed",
    };
  }
}

export async function addVideoToYouTubePlaylist(input: {
  accessToken: string;
  playlistId: string;
  videoId: string;
}): Promise<{ ok: boolean; message: string }> {
  try {
    const res = await fetch(
      "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          snippet: {
            playlistId: input.playlistId,
            resourceId: {
              kind: "youtube#video",
              videoId: input.videoId,
            },
          },
        }),
      },
    );
    const body = await res.json().catch(() => ({}));
    if (!res.ok) return { ok: false, message: redactSummary(body) };
    return { ok: true, message: "added to playlist" };
  } catch (err) {
    return {
      ok: false,
      message: err instanceof Error ? err.message : "playlist insert failed",
    };
  }
}

export async function fetchMineYouTubeChannelId(accessToken: string): Promise<string | null> {
  const res = await fetch(
    "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
    { headers: { Authorization: `Bearer ${accessToken}` } },
  );
  const body = await res.json().catch(() => ({}));
  return body?.items?.[0]?.id || null;
}
