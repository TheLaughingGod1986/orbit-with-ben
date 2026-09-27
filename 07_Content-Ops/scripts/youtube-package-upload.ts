#!/usr/bin/env tsx
/**
 * Orbit YouTube package upload — Data API for everything it can do,
 * plus a Studio finish checklist for ABC / pin / Related / end screens.
 *
 * Usage:
 *   npm run youtube:package -- \
 *     --package ../../02_Video-Projects/004_.../11_Upload-Package \
 *     --video ../../02_Video-Projects/004_.../09_Final-Export/master.mp4 \
 *     --dry-run
 *
 * Optional: PACKAGE_MANIFEST.json inside the package dir, or --manifest path.
 * After a live upload, writes *_PACKAGE_UPLOAD_RESULT.json into Schedule/ (or package root).
 */
import fs from "fs";
import path from "path";
import { isDryRun } from "../src/lib/env";
import { uploadToYouTube } from "../src/lib/youtube/upload";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";
import {
  addVideoToYouTubePlaylist,
  buildStudioFinishChecklist,
  fetchMineYouTubeChannelId,
  loadYouTubePackage,
  postYouTubeTopLevelComment,
} from "../src/lib/publishing/youtube-package";
import { REPO_ROOT, UPLOADS_FILE, createMirrorDeps } from "../src/lib/publishing/buffer-deps";
import { registerUpload } from "../src/lib/publishing/media-finder";
import { mirrorVideo } from "../src/lib/publishing/buffer-runner";

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function parseBool(v: string | undefined, fallback: boolean): boolean {
  if (v == null) return fallback;
  const s = v.toLowerCase();
  if (["1", "true", "yes"].includes(s)) return true;
  if (["0", "false", "no"].includes(s)) return false;
  throw new Error(`Invalid boolean: ${v}`);
}

async function main() {
  const packageDir = arg("package");
  if (!packageDir) {
    console.error(
      "Usage: youtube-package-upload.ts --package <11_Upload-Package> --video <mp4> [--manifest path] [--schedule ISO] [--thumbnail path] [--playlist-id ID] [--related-video-id ID] [--format longform|shorts] [--privacy private] [--made-for-kids false] [--skip-comment] [--no-buffer] [--standalone] [--dry-run]",
    );
    process.exit(1);
  }

  const dryRun = flag("dry-run") || isDryRun();
  const skipComment = flag("skip-comment");

  const resolved = loadYouTubePackage({
    packageDir,
    videoPath: arg("video"),
    manifestPath: arg("manifest"),
    overrides: {
      schedule: arg("schedule"),
      thumbnail: arg("thumbnail"),
      playlistId: arg("playlist-id"),
      relatedVideoId: arg("related-video-id"),
      title: arg("title"),
      format: (arg("format") as "longform" | "shorts" | undefined) || undefined,
      privacy: (arg("privacy") as "private" | "public" | "unlisted" | undefined) || undefined,
      madeForKids:
        arg("made-for-kids") != null ? parseBool(arg("made-for-kids"), false) : undefined,
    },
  });

  // Dry runs never need the YouTube login.
  const accessToken = dryRun ? "" : await getYouTubeAccessToken();

  const hashtagsJson = JSON.stringify(resolved.tags);

  const upload = await uploadToYouTube(
    {
      id: `pkg-${Date.now()}`,
      platform: "youtube_shorts",
      title: resolved.title,
      caption: resolved.description,
      hashtags: hashtagsJson,
      uploadStatus: "ready",
      privacyStatus: resolved.privacy,
      madeForKids: resolved.madeForKids,
      mediaFilePath: resolved.videoPath,
      scheduledAt: resolved.scheduledAt,
      thumbnailPath: resolved.thumbnailPath,
      contentFormat: resolved.format,
    },
    { dryRun, accessToken },
  );


  let firstCommentPosted = false;
  let commentMessage: string | null = null;
  let playlistAdded = false;
  let playlistMessage: string | null = null;

  if (!dryRun && upload.success && upload.platformPostId) {
    if (resolved.pinnedComment && !skipComment) {
      const channelId = await fetchMineYouTubeChannelId(accessToken);
      if (channelId) {
        const comment = await postYouTubeTopLevelComment({
          accessToken,
          channelId,
          videoId: upload.platformPostId,
          text: resolved.pinnedComment,
        });
        firstCommentPosted = comment.ok;
        commentMessage = comment.message;
      } else {
        commentMessage = "No channel id — skip comment insert";
      }
    }

    if (resolved.playlistId) {
      const pl = await addVideoToYouTubePlaylist({
        accessToken,
        playlistId: resolved.playlistId,
        videoId: upload.platformPostId,
      });
      playlistAdded = pl.ok;
      playlistMessage = pl.message;
    }
  }

  // Mirror to Instagram, Facebook and Threads through Buffer, for the YouTube go-public
  // time (STUDIO_PLAYBOOK.md §12). A Buffer problem never fails the upload; it's reported.
  let buffer: Record<string, unknown> | null = null;
  if (!dryRun && upload.success && upload.platformPostId) {
    // Record which files this upload came from, so the daily check can always find them.
    registerUpload(UPLOADS_FILE, REPO_ROOT, upload.platformPostId, {
      kind: resolved.format === "shorts" ? "short" : "long",
      file: resolved.videoPath,
      thumb: resolved.thumbnailPath ?? undefined,
      long: resolved.format === "shorts" ? resolved.relatedVideoId ?? undefined : undefined,
      standalone: (resolved.format === "shorts" && flag("standalone")) || undefined,
    });
  }
  if (!dryRun && upload.success && upload.platformPostId && !flag("no-buffer")) {
    const isShortUpload = resolved.format === "shorts";
    try {
      const deps = createMirrorDeps();
      const outcome = await mirrorVideo(
        {
          videoId: upload.platformPostId,
          kind: isShortUpload ? "short" : "long",
          longId: isShortUpload ? resolved.relatedVideoId : null,
          standalone: isShortUpload && flag("standalone"),
          mediaPath: isShortUpload ? resolved.videoPath : null,
          thumbPath: isShortUpload ? null : resolved.thumbnailPath,
        },
        deps,
      );
      buffer = {
        sent: outcome.sent,
        planOnly: !deps.client,
        errors: outcome.plan.errors,
        warnings: outcome.plan.warnings,
        results: outcome.results,
      };
    } catch (e) {
      buffer = { sent: false, errors: [(e as Error).message] };
    }
    const errs = (buffer.errors as string[]) ?? [];
    const failed = ((buffer.results as { ok: boolean }[]) ?? []).filter((r) => !r.ok);
    if (!buffer.sent || errs.length || failed.length) {
      console.error(
        `Buffer mirror incomplete for ${upload.platformPostId}: ${[...errs, ...failed.map((f) => JSON.stringify(f))].join("; ") || "planning only (no BUFFER_API_KEY)"}. ` +
          "Fix it, then run scripts/buffer-mirror.ts mirror (STUDIO_PLAYBOOK.md §12).",
      );
    }
  }

  const checklist = buildStudioFinishChecklist({
    videoId: upload.platformPostId || null,
    format: resolved.format,
    titleAbc: resolved.titleAbc,
    thumbnailAbc: resolved.thumbnailAbc,
    pinnedComment: resolved.pinnedComment,
    relatedVideoId: resolved.relatedVideoId,
    firstCommentPosted,
    thumbnailSet: Boolean(resolved.thumbnailPath) && (dryRun || upload.success),
    playlistAdded,
    playlistId: resolved.playlistId,
  });

  const result = {
    ok: upload.success,
    dryRun,
    method: "youtube_data_api_package",
    upload: {
      published: upload.published,
      scheduledOnPlatform: upload.scheduledOnPlatform || false,
      scheduledFor: upload.scheduledFor || null,
      platformPostId: upload.platformPostId || null,
      platformUrl: upload.platformUrl || null,
      message: upload.message,
      responseSummary: upload.responseSummary || null,
    },
    package: {
      title: resolved.title,
      format: resolved.format,
      privacy: resolved.privacy,
      tagCount: resolved.tags.length,
      hasPinnedComment: Boolean(resolved.pinnedComment),
      thumbnailPath: resolved.thumbnailPath,
      scheduledAt: resolved.scheduledAt?.toISOString() || null,
      sources: resolved.sources,
    },
    postUpload: {
      firstCommentPosted,
      commentMessage,
      playlistAdded,
      playlistMessage,
    },
    buffer,
    studioFinish: checklist,
  };

  console.log(JSON.stringify(result, null, 2));

  const outDir = fs.existsSync(path.join(resolved.packageDir, "Schedule"))
    ? path.join(resolved.packageDir, "Schedule")
    : resolved.packageDir;
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const outPath = path.join(outDir, `PACKAGE_UPLOAD_RESULT_${stamp}.json`);
  fs.writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.error(`Wrote ${outPath}`);

  if (!upload.success) process.exit(1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
