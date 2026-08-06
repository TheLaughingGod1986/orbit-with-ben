#!/usr/bin/env tsx
/**
 * Orbit YouTube package upload — Data API for everything it can do,
 * plus a Studio finish checklist for ABC / pin / Related / end screens.
 *
 * Hardened for recovery mode + canonical registry (ONE package = ONE video ID).
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
import { createHash } from "crypto";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv, isDryRun } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import {
  addVideoToYouTubePlaylist,
  buildStudioFinishChecklist,
  fetchMineYouTubeChannelId,
  loadYouTubePackage,
  postYouTubeTopLevelComment,
} from "../src/lib/publishing/youtube-package";
import {
  evaluateRecoveryGate,
  loadYouTubeRecoveryConfig,
  calendarDayKey,
  findScheduleCollision,
} from "../src/lib/publishing/youtube-recovery";
import {
  fingerprintSourceFile,
  loadCanonicalRegistry,
  lookupCanonicalConflicts,
  saveCanonicalRegistry,
  upsertCanonicalRecord,
} from "../src/lib/publishing/youtube-registry";
import { hasForceSslScope, parseGrantedScopes } from "../src/lib/publishing/youtube-oauth";

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

function packageContentId(packageDir: string, format: string, title: string): string {
  const base = path.basename(path.resolve(packageDir, ".."));
  const slug = createHash("sha1").update(`${base}|${format}|${title}`).digest("hex").slice(0, 10);
  return `${base}:${format}:${slug}`;
}

/** Ambiguous upload resolution — never blind-retry. */
export async function findExistingUploadByTitle(input: {
  accessToken: string;
  title: string;
  maxResults?: number;
}): Promise<{ id: string; title: string; publishedAt: string }[]> {
  const q = encodeURIComponent(input.title.slice(0, 80));
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/search?part=snippet&forMine=true&type=video&maxResults=${input.maxResults || 10}&q=${q}`,
    { headers: { Authorization: `Bearer ${input.accessToken}` } },
  );
  const body = await res.json();
  return (body.items || []).map((it: any) => ({
    id: it.id?.videoId as string,
    title: it.snippet?.title as string,
    publishedAt: it.snippet?.publishedAt as string,
  }));
}

async function main() {
  getEnv();
  const packageDir = arg("package");
  if (!packageDir) {
    console.error(
      "Usage: youtube-package-upload.ts --package <11_Upload-Package> --video <mp4> [--manifest path] [--schedule ISO] [--thumbnail path] [--playlist-id ID] [--related-video-id ID] [--format longform|shorts] [--privacy private] [--made-for-kids false] [--content-id ID] [--allow-recovery-exception] [--skip-comment] [--dry-run]",
    );
    process.exit(1);
  }

  if (flag("replace") || flag("reupload") || flag("delete-and-reupload")) {
    console.error(
      "UPLOAD BLOCKED: Replacement / reupload flags are forbidden. ONE CONTENT PACKAGE = ONE YOUTUBE VIDEO ID.",
    );
    process.exit(20);
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

  if (!fs.existsSync(resolved.videoPath)) {
    console.error(`UPLOAD BLOCKED: video file missing: ${resolved.videoPath}`);
    process.exit(21);
  }

  const fingerprint = fingerprintSourceFile(resolved.videoPath);
  const internalContentId =
    arg("content-id") || packageContentId(resolved.packageDir, resolved.format, resolved.title);

  const registry = loadCanonicalRegistry();
  const conflict = lookupCanonicalConflicts({
    registry,
    internalContentId,
    sourceFileFingerprint: fingerprint,
  });
  if (conflict.blocked) {
    console.error(conflict.reason);
    console.error(
      JSON.stringify(
        {
          matched: {
            internalContentId: conflict.matched?.internalContentId,
            youtubeVideoId: conflict.matched?.youtubeVideoId,
          },
        },
        null,
        2,
      ),
    );
    process.exit(22);
  }

  const recovery = loadYouTubeRecoveryConfig();
  const dayKey = calendarDayKey(new Date(), recovery.timezone);
  // Count registry shorts with upload/schedule on this calendar day (best-effort)
  const shortsToday = registry.records.filter((r) => {
    if (r.contentType !== "shorts") return false;
    const ts = r.scheduledPublishTimestamp || r.uploadTimestamp;
    if (!ts) return false;
    return calendarDayKey(new Date(ts), recovery.timezone) === dayKey;
  }).length;
  const longsDuring = registry.records.filter((r) => {
    if (r.contentType !== "longform" || !r.uploadTimestamp) return false;
    const t = new Date(r.uploadTimestamp).getTime();
    const start = new Date(recovery.startedAt).getTime();
    return t >= start;
  }).length;

  const collision = findScheduleCollision({
    proposedPublishAt: resolved.scheduledAt,
    existing: registry.records.map((r) => ({
      youtubeVideoId: r.youtubeVideoId,
      scheduledPublishTimestamp: r.scheduledPublishTimestamp,
    })),
  });

  const gate = evaluateRecoveryGate({
    config: recovery,
    format: resolved.format,
    shortsPublishedOrScheduledToday: shortsToday,
    longsUploadedDuringRecovery: longsDuring,
    isReplacementUpload: false,
    isDuplicateFingerprint: false,
    alreadyHasCanonicalVideoId: false,
    scheduleCollision: collision.collision,
    scheduleCollisionWith: collision.withVideoId,
  });
  if (gate.blocked && !flag("allow-recovery-exception")) {
    console.error(gate.errors.join("\n"));
    process.exit(23);
  }

  const connection = await prisma.platformConnection.findFirst({
    where: {
      platform: "youtube_shorts",
      connectionStatus: "connected",
      disconnectedAt: null,
    },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) {
    console.error(
      "No connected YouTube account. Connect Google OAuth on /settings/connections (reconnect after scope updates).",
    );
    process.exit(1);
  }

  const scopes = parseGrantedScopes(connection.grantedScopes);
  if (!hasForceSslScope(scopes)) {
    const msg =
      "youtube.force-ssl not granted. Run: npm run youtube:verify-oauth -- --print-auth-url";
    if (dryRun) {
      console.error(`WARNING: ${msg}`);
    } else {
      console.error(`UPLOAD BLOCKED: ${msg}`);
      process.exit(24);
    }
  }

  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    const refreshed = await adapter.refreshConnection(connection);
    if (!refreshed.ok) {
      console.error(`Token refresh failed: ${refreshed.message}`);
      process.exit(1);
    }
  }

  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  if (!fresh?.accessTokenEncrypted) {
    console.error("Missing access token");
    process.exit(1);
  }
  const accessToken = decryptSecret(fresh.accessTokenEncrypted);

  const hashtagsJson = JSON.stringify(resolved.tags);

  let upload;
  try {
    upload = await adapter.publish(
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
      fresh,
      {
        dryRun,
        workerId: "youtube-package-upload-cli",
        jobId: `pkg-${Date.now()}`,
        attemptNumber: 1,
        accessToken,
      },
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(
      "UPLOAD UNCERTAIN: request failed before a confirmed video ID. Do NOT retry blindly.",
    );
    console.error(message);
    if (!dryRun) {
      const existing = await findExistingUploadByTitle({
        accessToken,
        title: resolved.title,
      });
      console.error(
        JSON.stringify(
          {
            remediation:
              "Compare search hits below with duration/title. Retry only if no matching upload exists.",
            searchHits: existing.slice(0, 5),
          },
          null,
          2,
        ),
      );
    }
    process.exit(25);
  }

  // Persist canonical ID immediately on success
  if (!dryRun && upload.success && upload.platformPostId) {
    const next = upsertCanonicalRecord(registry, {
      internalContentId,
      contentType: resolved.format,
      sourceFileFingerprint: fingerprint,
      title: resolved.title,
      youtubeVideoId: upload.platformPostId,
      uploadTimestamp: new Date().toISOString(),
      scheduledPublishTimestamp: resolved.scheduledAt?.toISOString() || null,
      privacyStatus: resolved.privacy,
      packageVersion: "package-cli",
      metadataVersion: "v1",
      relatedLongFormVideoId: resolved.relatedVideoId,
      lastVerificationTimestamp: new Date().toISOString(),
      lastApiResponseStatus: "uploaded",
      packagePath: resolved.packageDir,
    });
    saveCanonicalRegistry(next);
  }

  let firstCommentPosted = false;
  let commentMessage: string | null = null;
  let playlistAdded = false;
  let playlistMessage: string | null = null;

  if (!dryRun && upload.success && upload.platformPostId) {
    if (resolved.pinnedComment && !skipComment) {
      const channelId =
        fresh.channelId ||
        fresh.accountUsername ||
        (await fetchMineYouTubeChannelId(accessToken));
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
    recovery: {
      active: gate.recoveryActive,
      blocked: gate.blocked,
      endsAt: gate.endsAt,
    },
    registry: {
      internalContentId,
      sourceFileFingerprint: fingerprint,
      youtubeVideoId: upload.platformPostId || null,
    },
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

  if (!upload.success) {
    // If a video ID somehow exists in the message/summary, do not advise retry
    if (upload.platformPostId) {
      console.error(
        `UPLOAD FAILED AFTER VIDEO ID ${upload.platformPostId} — do not create a replacement. Inspect/update that ID.`,
      );
    }
    process.exit(1);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
