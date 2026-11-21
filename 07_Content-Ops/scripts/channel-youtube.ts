/**
 * Orbit With Ben's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but keeping
 * their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts, youtube-package-upload.ts) import
 * these hooks; each repo keeps its own copy of this file, so how a channel signs in, guards its desk, files its uploads
 * and mirrors to social stays the channel's own.
 */
import fs from "fs";
import path from "path";
import type { ResolvedYouTubePackage } from "../src/lib/publishing/youtube-package";
import type { ChannelUpload } from "../src/lib/youtube/upload";

export { ensureDeskLock as beforeRun } from "./with-desk-lock";

const FOH_ID = "UCu94mInMFosxu3W0H6jlI6Q";

/** The channel whose checkout holds this package, from the nearest studio/channel.json above it. */
export function packageOwner(packageDir: string): { slug: string; id: string } | null {
  let dir = path.resolve(packageDir);
  for (let i = 0; i < 8; i++) {
    const file = path.join(dir, "studio", "channel.json");
    if (fs.existsSync(file)) {
      try {
        const c = JSON.parse(fs.readFileSync(file, "utf8")) as { slug?: string; youtube?: { id?: string } };
        if (c.slug) return { slug: c.slug, id: c.youtube?.id || "" };
      } catch {
        return null;
      }
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

function fieldOrderUploadHold(packageDir: string): string | null {
  let names: string[] = [];
  try {
    names = fs.readdirSync(packageDir).filter((n) => /^metadata_v\d+\.json$/i.test(n));
  } catch {
    return null;
  }
  names.sort((a, b) => Number(a.match(/\d+/)?.[0] || 0) - Number(b.match(/\d+/)?.[0] || 0));
  const file = names.length ? path.join(packageDir, names[names.length - 1]) : "";
  if (!file) return null;
  try {
    const meta = JSON.parse(fs.readFileSync(file, "utf8")) as { upload_authorized?: boolean; hold_reason?: string };
    if (meta.upload_authorized === false) {
      return meta.hold_reason || "Field Order History package is not authorised for upload";
    }
  } catch {
    return null;
  }
  return null;
}

function isFieldOrder(packageDir: string): { slug: string; id: string } | null {
  const owner = packageOwner(packageDir);
  return owner?.slug === "ww2" ? owner : null;
}

/** Orbit's upload login, or Field Order History's own token when the package lives in that checkout. */
export async function youtubeAccessToken(packageDir?: string): Promise<string> {
  const foh = packageDir ? isFieldOrder(packageDir) : null;
  if (foh) {
    if (foh.id !== FOH_ID) {
      throw new Error(`Refusing a Field Order History upload: studio/channel.json id is ${foh.id || "(none)"}, not ${FOH_ID}`);
    }
    const { getChannelAccessToken } = await import("../src/lib/youtube/data-api");
    try {
      return await getChannelAccessToken("YOUTUBE_REFRESH_TOKEN_WW2", FOH_ID);
    } catch (e) {
      const msg = (e as Error).message;
      if (msg.includes("missing from .env")) {
        throw new Error("YOUTUBE_REFRESH_TOKEN_WW2 missing from .env: run `npx tsx --env-file=.env scripts/youtube-auth.ts --upload ww2` and choose the Field Order History Brand Account");
      }
      throw e;
    }
  }
  const { getYouTubeAccessToken } = await import("../src/lib/youtube/data-api");
  return getYouTubeAccessToken();
}

/** Education, British English, for a Field Order History package. Orbit stays Science & Technology. */
export function uploadFor(packageDir: string): ChannelUpload {
  return isFieldOrder(packageDir) ? { categoryId: "27", defaultLanguage: "en-GB" } : UPLOAD;
}

export async function afterRun(): Promise<void> {}

/** Science & Technology; no language set (unchanged from before the core). */
export const UPLOAD: ChannelUpload = { categoryId: "28" };

/** The upload flags only Orbit has, for the usage line. */
export const UPLOAD_FLAGS = "[--no-buffer] [--standalone] [--force-new]";

type UploadHookInput = { resolved: ResolvedYouTubePackage; flag: (name: string) => boolean; repoRoot: string };

/** Refuses a second upload of the same film (uploads.json + earlier results); `--force-new` skips it. */
export async function beforeUpload(input: UploadHookInput): Promise<Record<string, unknown>> {
  const foh = isFieldOrder(input.resolved.packageDir);
  if (foh) {
    if (foh.id !== FOH_ID) {
      throw new Error(`Refusing a Field Order History upload: studio/channel.json id is ${foh.id || "(none)"}, not ${FOH_ID}`);
    }
    if (!input.flag("dry-run")) {
      const { isDryRun } = await import("../src/lib/env");
      if (!isDryRun()) {
        const hold = fieldOrderUploadHold(input.resolved.packageDir);
        if (hold) throw new Error(hold);
      }
    }
    return { channel: "ww2", channelId: FOH_ID };
  }
  const { checkPackageDuplicate } = await import("../src/lib/publishing/package-duplicate");
  const { UPLOADS_FILE, REPO_ROOT } = await import("../src/lib/publishing/buffer-deps");
  return checkPackageDuplicate({
    packageDir: input.resolved.packageDir, videoPath: input.resolved.videoPath,
    uploadsFile: UPLOADS_FILE, repoRoot: REPO_ROOT, forceNew: input.flag("force-new"),
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
  if (isFieldOrder(input.resolved.packageDir)) {
    return { buffer: { skipped: true, reason: "Field Order History has no Buffer mirror" } };
  }
  const { resolved, flag, videoId } = input;
  const { UPLOADS_FILE, REPO_ROOT, createMirrorDeps } = await import("../src/lib/publishing/buffer-deps");
  const { registerUpload } = await import("../src/lib/publishing/media-finder");
  const { mirrorVideo } = await import("../src/lib/publishing/buffer-runner");
  const isShort = resolved.format === "shorts";

  registerUpload(UPLOADS_FILE, REPO_ROOT, videoId, {
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
