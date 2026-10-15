#!/usr/bin/env tsx
/**
 * YouTube package upload, shared by Orbit With Ben and History of Science (studio core, 15 Oct 2026) — Data API
 * for everything it can do, plus a Studio finish checklist for ABC / pin / Related / end screens.
 *
 * What stays each channel's own lives in its scripts/channel-youtube.ts: the sign-in, the desk guard, the category
 * and language (UPLOAD), the duplicate check before the upload and what runs after it (Orbit: uploads.json and the
 * Buffer mirror). The Shorts ship gate is shared and has no override.
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
import * as channel from "./channel-youtube";
import { isDryRun } from "../src/lib/env";
import { uploadToYouTube } from "../src/lib/youtube/upload";
import {
  addVideoToYouTubePlaylist,
  buildStudioFinishChecklist,
  fetchMineYouTubeChannelId,
  loadYouTubePackage,
  postYouTubeTopLevelComment,
} from "../src/lib/publishing/youtube-package";
import { runShortsGate } from "../src/lib/publishing/shorts-gate";

const REPO_ROOT = path.resolve(__dirname, "..", "..");

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
      `Usage: youtube-package-upload.ts --package <11_Upload-Package> --video <mp4> [--manifest path] [--schedule ISO] [--thumbnail path] [--playlist-id ID] [--related-video-id ID] [--format longform|shorts] [--privacy private] [--made-for-kids false] [--skip-comment] [--dry-run] ${channel.UPLOAD_FLAGS}`,
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

  // The channel's own check before anything is sent (Orbit: refuses a second upload of the same film).
  const identity = await channel.beforeUpload({ resolved, flag, repoRoot: REPO_ROOT });

  // Shorts ship gate: a hard stop, dry run included, so the dry run shows the verdict. No override (Never list).
  if (resolved.format === "shorts") {
    const gate = runShortsGate({
      videoPath: resolved.videoPath, repoRoot: REPO_ROOT, scheduledAt: resolved.scheduledAt,
      lengthTest: resolved.lengthTest,
    });
    console.log(gate.output);
    if (!gate.ok) {
      console.error(`gate_shorts_open FAILED (exit ${gate.exitCode}, air date ${gate.airDate}): not uploading. Fix the cut.`);
      process.exit(1);
    }
  }

  // Dry runs never need the YouTube login.
  const accessToken = dryRun ? "" : await channel.youtubeAccessToken();

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
    { dryRun, accessToken, channel: channel.UPLOAD },
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

  // The channel's own steps after a live upload (Orbit: uploads.json and the Buffer mirror). Never fails the upload.
  const after =
    !dryRun && upload.success && upload.platformPostId
      ? await channel.afterUpload({ videoId: upload.platformPostId, resolved, identity, flag, repoRoot: REPO_ROOT })
      : {};

  // The upload succeeds even when YouTube refuses the thumbnail (403 on 022, 9 Oct): the reason is only in the message.
  const thumbnailSkipped = /thumbnail skipped/i.test(upload.message || "");
  if (!dryRun && resolved.thumbnailPath && thumbnailSkipped) {
    console.error(
      `THUMBNAIL NOT SET on ${upload.platformPostId}: ${upload.message}. Set it in Studio (or re-run the thumbnail) before go-live; the video shows an auto frame until then.`,
    );
  }

  const checklist = buildStudioFinishChecklist({
    videoId: upload.platformPostId || null,
    format: resolved.format,
    titleAbc: resolved.titleAbc,
    thumbnailAbc: resolved.thumbnailAbc,
    pinnedComment: resolved.pinnedComment,
    relatedVideoId: resolved.relatedVideoId,
    firstCommentPosted,
    thumbnailSet: Boolean(resolved.thumbnailPath) && (dryRun || (upload.success && !thumbnailSkipped)),
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
      ...identity,
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
    ...after,
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

channel.beforeRun();

main()
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(() => channel.afterRun());
