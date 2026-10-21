/**
 * Orbit With Ben's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but keeping
 * their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts, youtube-package-upload.ts) import
 * these hooks; each repo keeps its own copy of this file, so how a channel signs in, guards its desk, files its uploads
 * and mirrors to social stays the channel's own.
 */
import type { ResolvedYouTubePackage } from "../src/lib/publishing/youtube-package";
import type { ChannelUpload } from "../src/lib/youtube/upload";

export { ensureDeskLock as beforeRun } from "./with-desk-lock";
export { getYouTubeAccessToken as youtubeAccessToken } from "../src/lib/youtube/data-api";

export async function afterRun(): Promise<void> {}

/** Science & Technology; no language set (unchanged from before the core). */
export const UPLOAD: ChannelUpload = { categoryId: "28" };

/** The upload flags only Orbit has, for the usage line. */
export const UPLOAD_FLAGS = "[--no-buffer] [--standalone] [--force-new]";

type UploadHookInput = { resolved: ResolvedYouTubePackage; flag: (name: string) => boolean; repoRoot: string };

/** Refuses a second upload of the same film (uploads.json + earlier results); `--force-new` skips it. */
export async function beforeUpload(input: UploadHookInput): Promise<Record<string, unknown>> {
  const { checkPackageDuplicate } = await import("../src/lib/publishing/package-duplicate");
  const { UPLOADS_FILE } = await import("../src/lib/publishing/buffer-deps");
  return checkPackageDuplicate({
    packageDir: input.resolved.packageDir, videoPath: input.resolved.videoPath,
    uploadsFile: UPLOADS_FILE, repoRoot: input.repoRoot, forceNew: input.flag("force-new"),
  });
}

/**
 * After a live upload: record which files it came from (so the daily check can always find them), then mirror it to
 * Instagram, Facebook and Threads through Buffer for the YouTube go-public time (STUDIO_PLAYBOOK.md §12). A Buffer
 * problem never fails the upload; it's reported, and `--no-buffer` skips the mirror.
 */
export async function afterUpload(
  input: UploadHookInput & { videoId: string; identity: Record<string, unknown> },
): Promise<{ buffer: Record<string, unknown> | null }> {
  const { resolved, flag, videoId } = input;
  const { UPLOADS_FILE, createMirrorDeps } = await import("../src/lib/publishing/buffer-deps");
  const { registerUpload } = await import("../src/lib/publishing/media-finder");
  const { mirrorVideo } = await import("../src/lib/publishing/buffer-runner");
  const isShort = resolved.format === "shorts";

  registerUpload(UPLOADS_FILE, input.repoRoot, videoId, {
    ...input.identity,
    kind: isShort ? "short" : "long",
    file: resolved.videoPath,
    thumb: resolved.thumbnailPath ?? undefined,
    trailer: resolved.trailerPath ?? undefined,
    long: isShort ? resolved.relatedVideoId ?? undefined : undefined,
    standalone: (isShort && flag("standalone")) || undefined,
    social: resolved.social ?? undefined,
  });
  if (flag("no-buffer")) return { buffer: null };

  let buffer: Record<string, unknown>;
  try {
    const deps = createMirrorDeps();
    const outcome = await mirrorVideo(
      {
        videoId,
        kind: isShort ? "short" : "long",
        longId: isShort ? resolved.relatedVideoId : null,
        standalone: isShort && flag("standalone"),
        mediaPath: isShort ? resolved.videoPath : null,
        thumbPath: isShort ? null : resolved.thumbnailPath,
        trailerPath: isShort ? null : resolved.trailerPath,
        social: resolved.social ?? undefined,
      },
      deps,
    );
    buffer = {
      sent: outcome.sent,
      deferred: outcome.deferred,
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
  if (buffer.deferred) console.log(`Buffer mirror for ${videoId}: ${buffer.deferred}.`);
  else if (!buffer.sent || errs.length || failed.length) {
    console.error(
      `Buffer mirror incomplete for ${videoId}: ${[...errs, ...failed.map((f) => JSON.stringify(f))].join("; ") || "planning only (no BUFFER_API_KEY)"}. ` +
        "Fix it, then run scripts/buffer-mirror.ts mirror (STUDIO_PLAYBOOK.md §12).",
    );
  }
  return { buffer };
}
