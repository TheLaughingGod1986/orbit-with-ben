/**
 * YouTube Data API upload for `npm run youtube:package`: resumable upload, private +
 * publishAt scheduling, altered-content disclosure, custom thumbnail. Moved out of the
 * retired ops app (27 Sep 2026); the token comes from getYouTubeAccessToken().
 */
import fs from "fs";
import type { PlatformPostRecord, PublishResult } from "@/lib/publishing/types";
import { classifyHttpError, redactSummary } from "@/lib/publishing/errors";
import { probeVideo, validateForPlatform } from "@/lib/publishing/media/ffprobe";

const YT_UPLOAD = "https://www.googleapis.com/auth/youtube.upload";
const YT_READONLY = "https://www.googleapis.com/auth/youtube.readonly";
/** Needed for commentThreads.insert + playlistItems.insert after upload. */
const YT_FORCE_SSL = "https://www.googleapis.com/auth/youtube.force-ssl";

/** YouTube requires publishAt at least ~15 minutes in the future (API soft rule). */
const MIN_PUBLISH_AT_MS = 15 * 60 * 1000;

export function resolveYouTubeSchedule(scheduledAt?: Date | null, now = new Date()): {
  usePublishAt: boolean;
  publishAtIso?: string;
} {
  if (!scheduledAt || scheduledAt.getTime() <= now.getTime() + MIN_PUBLISH_AT_MS) {
    return { usePublishAt: false };
  }
  return {
    usePublishAt: true,
    publishAtIso: scheduledAt.toISOString(),
  };
}

export async function validateYouTubeUpload(post: PlatformPostRecord) {
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!post.title && !post.caption) errors.push("Title or caption required");
  if (post.privacyStatus == null) errors.push("privacyStatus is required (default tests to private)");
  if (post.madeForKids == null) errors.push("madeForKids must be set explicitly");
  const schedule = resolveYouTubeSchedule(post.scheduledAt ?? null);
  if (schedule.usePublishAt && post.privacyStatus && post.privacyStatus !== "private" && post.privacyStatus !== "unlisted") {
    errors.push("Native YouTube schedule requires privacyStatus private or unlisted (API publishAt rule)");
  }
  const file = post.mediaFilePath || post.exportPath;
  if (!file) errors.push("mediaFilePath / export video missing");
  else {
    const probe = await probeVideo(resolveVideoFile(file));
    const platformKey = post.contentFormat === "longform" ? "youtube_longform" : "youtube_shorts";
    const platformCheck = validateForPlatform(platformKey, probe);
    errors.push(...platformCheck.errors);
    warnings.push(...platformCheck.warnings);
  }
  if (post.thumbnailPath) {
    if (!fs.existsSync(post.thumbnailPath)) {
      warnings.push(`thumbnailPath not found: ${post.thumbnailPath}`);
    }
  }
  return { ok: errors.length === 0, errors, warnings };
}

export async function uploadToYouTube(
  post: PlatformPostRecord,
  context: { accessToken: string; dryRun: boolean },
): Promise<PublishResult> {
  const schedule = resolveYouTubeSchedule(post.scheduledAt ?? null);
  const requestedPrivacy = (post.privacyStatus || "private") as "private" | "public" | "unlisted";
  const privacyStatus = schedule.usePublishAt
    ? (requestedPrivacy === "unlisted" ? "unlisted" : "private")
    : requestedPrivacy;

  if (context.dryRun) {
    const errors: string[] = [];
    if (!post.title && !post.caption) errors.push("Title or caption required");
    if (post.privacyStatus == null) errors.push("privacyStatus is required");
    if (post.madeForKids == null) errors.push("madeForKids must be set explicitly");
    if (errors.length) {
      return {
        success: false,
        published: false,
        message: errors.join("; "),
        method: "dry_run",
        errorCategory: "validation",
        retryable: false,
      };
    }
    return {
      success: true,
      published: false,
      scheduledOnPlatform: schedule.usePublishAt,
      scheduledFor: schedule.publishAtIso,
      message: schedule.usePublishAt
        ? `Dry-run complete. Would upload now with publishAt=${schedule.publishAtIso}.`
        : "Dry-run complete. YouTube upload request prepared but not sent.",
      method: "dry_run",
      responseSummary: redactSummary({
        title: post.title,
        privacyStatus,
        publishAt: schedule.publishAtIso || null,
        madeForKids: post.madeForKids,
        containsSyntheticMedia: true,
        contentFormat: post.contentFormat || "shorts",
      }),
    };
  }

  const validation = await validateYouTubeUpload(post);
  if (!validation.ok) {
    return {
      success: false,
      published: false,
      message: validation.errors.join("; "),
      method: "api",
      errorCategory: "validation",
      retryable: false,
    };
  }

  const filePath = resolveVideoFile(post.mediaFilePath || post.exportPath!);
  const title = (post.title || post.caption || "Orbit Short").slice(0, 100);
  const description = post.caption || "";
  const madeForKids = Boolean(post.madeForKids);

  const statusPayload: Record<string, unknown> = {
    privacyStatus,
    selfDeclaredMadeForKids: madeForKids,
    // YouTube “altered or synthetic” disclosure. On for every new upload.
    containsSyntheticMedia: true,
  };
  if (schedule.usePublishAt && schedule.publishAtIso) {
    statusPayload.publishAt = schedule.publishAtIso;
  }

  try {
    const metaRes = await fetch(
      "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${context.accessToken}`,
          "Content-Type": "application/json; charset=UTF-8",
          "X-Upload-Content-Type": "video/mp4",
          "X-Upload-Content-Length": String(fs.statSync(filePath).size),
        },
        body: JSON.stringify({
          snippet: {
            title,
            description,
            categoryId: "28",
            tags: safeTags(post.hashtags),
          },
          status: statusPayload,
        }),
      },
    );

    if (!metaRes.ok) {
      const text = await metaRes.text();
      const classified = classifyHttpError(metaRes.status, text);
      return {
        success: false,
        published: false,
        message: `YouTube session init failed (${metaRes.status})`,
        method: "api",
        errorCategory: classified.category,
        retryable: classified.retryable,
        httpStatus: metaRes.status,
        responseSummary: redactSummary(text),
      };
    }

    const uploadUrl = metaRes.headers.get("location");
    if (!uploadUrl) {
      return {
        success: false,
        published: false,
        message: "YouTube did not return a resumable upload URL",
        method: "api",
        errorCategory: "temporary_platform",
        retryable: true,
      };
    }

    const fileBuf = fs.readFileSync(filePath);
    const uploadRes = await fetch(uploadUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "video/mp4",
        "Content-Length": String(fileBuf.length),
      },
      body: fileBuf,
    });
    const uploadBody = await uploadRes.json().catch(() => ({}));
    if (!uploadRes.ok || !uploadBody.id) {
      const classified = classifyHttpError(uploadRes.status, JSON.stringify(uploadBody));
      return {
        success: false,
        published: false,
        message: "YouTube upload failed",
        method: "api",
        errorCategory: classified.category,
        retryable: classified.retryable,
        httpStatus: uploadRes.status,
        responseSummary: redactSummary(uploadBody),
      };
    }

    const videoId = uploadBody.id as string;
    let thumbNote = "";
    if (post.thumbnailPath && fs.existsSync(post.thumbnailPath)) {
      const thumbOk = await setYouTubeThumbnail(context.accessToken, videoId, post.thumbnailPath);
      thumbNote = thumbOk.ok ? "; thumbnail set" : `; thumbnail skipped: ${thumbOk.message}`;
    }

    if (schedule.usePublishAt && schedule.publishAtIso) {
      return {
        success: true,
        published: true,
        scheduledOnPlatform: true,
        scheduledFor: schedule.publishAtIso,
        platformPostId: videoId,
        platformUrl: `https://youtu.be/${videoId}`,
        message: `Uploaded to YouTube; scheduled to go live at ${schedule.publishAtIso}${thumbNote}`,
        method: "api",
        responseSummary: redactSummary({
          id: videoId,
          privacyStatus,
          publishAt: schedule.publishAtIso,
        }),
      };
    }

    return {
      success: true,
      published: true,
      platformPostId: videoId,
      platformUrl: `https://youtu.be/${videoId}`,
      message: `Uploaded to YouTube as ${privacyStatus}${thumbNote}`,
      method: "api",
      responseSummary: redactSummary({ id: videoId, privacyStatus }),
    };
  } catch (err) {
    return {
      success: false,
      published: false,
      message: err instanceof Error ? err.message : "YouTube network error",
      method: "api",
      errorCategory: "network",
      retryable: true,
    };
  }
}

async function setYouTubeThumbnail(
  accessToken: string,
  videoId: string,
  thumbnailPath: string,
): Promise<{ ok: boolean; message: string }> {
  try {
    const buf = fs.readFileSync(thumbnailPath);
    const lower = thumbnailPath.toLowerCase();
    const contentType = lower.endsWith(".png")
      ? "image/png"
      : lower.endsWith(".gif")
        ? "image/gif"
        : "image/jpeg";
    const res = await fetch(
      `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${encodeURIComponent(videoId)}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": contentType,
          "Content-Length": String(buf.length),
        },
        body: buf,
      },
    );
    if (!res.ok) {
      const text = await res.text();
      return { ok: false, message: redactSummary(text) };
    }
    return { ok: true, message: "ok" };
  } catch (err) {
    return { ok: false, message: err instanceof Error ? err.message : "thumbnail upload failed" };
  }
}

function safeTags(hashtags?: string | null): string[] {
  if (!hashtags) return [];
  try {
    const parsed = JSON.parse(hashtags);
    if (Array.isArray(parsed)) return parsed.map(String).slice(0, 15);
  } catch {
    /* ignore */
  }
  return [];
}

function resolveVideoFile(fileOrDir: string): string {
  if (fs.existsSync(fileOrDir) && fs.statSync(fileOrDir).isFile()) return fileOrDir;
  // export package directory — look for mp4
  if (fs.existsSync(fileOrDir) && fs.statSync(fileOrDir).isDirectory()) {
    const videoDir = `${fileOrDir}/video`;
    if (fs.existsSync(videoDir)) {
      const mp4 = fs.readdirSync(videoDir).find((f) => f.endsWith(".mp4"));
      if (mp4) return `${videoDir}/${mp4}`;
    }
  }
  return fileOrDir;
}

export const YOUTUBE_SCOPES = [YT_UPLOAD, YT_READONLY, YT_FORCE_SSL];
export { YT_UPLOAD, YT_READONLY, YT_FORCE_SSL };
