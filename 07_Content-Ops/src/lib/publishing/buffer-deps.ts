/**
 * Real dependencies for the Buffer mirror: YouTube via YOUTUBE_REFRESH_TOKEN, Buffer via
 * BUFFER_API_KEY, media via the public Cloudflare R2 bucket (R2_* keys; the Vercel Blob
 * store, BLOB_READ_WRITE_TOKEN, only when R2 isn't set up), and the BUFFER_POSTS.json record. Missing keys degrade to plan-only rather than failing.
 */
import fs from "fs";
import path from "path";
import { BUFFER_CHANNELS, type ChannelIds } from "@/lib/publishing/buffer-mirror";
import { createBufferApiClient } from "@/lib/publishing/buffer-api";
import { createFileBufferStore } from "@/lib/publishing/buffer-store";
import { checkMediaUrl, deleteFromVercelBlob, hostOnVercelBlob, listVercelBlobMedia } from "@/lib/publishing/media-host";
import { createR2Host, r2Config } from "@/lib/publishing/media-host-r2";
import { findMedia, loadRegistry, scanProjectRecords } from "@/lib/publishing/media-finder";
import type { MirrorDeps } from "@/lib/publishing/buffer-runner";
import { fetchYouTubeVideos, getYouTubeAccessToken, listRecentlyPublic, listScheduledUploads } from "@/lib/youtube/data-api";

export const REPO_ROOT = path.resolve(__dirname, "../../../..");
export const SOCIAL_DIR = path.join(REPO_ROOT, "00_Brand/Channel-Setup/social");
export const CHANNELS_FILE = path.join(SOCIAL_DIR, "BUFFER_CHANNELS.json");
export const LEDGER_FILE = path.join(SOCIAL_DIR, "BUFFER_POSTS.json");
export const UPLOADS_FILE = path.join(SOCIAL_DIR, "UPLOADS.json");

/** Channel ids from social/BUFFER_CHANNELS.json. */
export function loadChannelIds(file = CHANNELS_FILE): ChannelIds {
  if (!fs.existsSync(file)) return {};
  const cfg = JSON.parse(fs.readFileSync(file, "utf8")) as { channels?: Record<string, { id?: string }> };
  const ids: ChannelIds = {};
  for (const c of BUFFER_CHANNELS) {
    const id = cfg.channels?.[c]?.id;
    if (id) ids[c] = id;
  }
  return ids;
}

export function createMirrorDeps(opts: { channelIds?: ChannelIds; ledgerFile?: string } = {}): MirrorDeps {
  const key = process.env.BUFFER_API_KEY;
  // Old project records are scanned once per run, only if something needs them.
  let scanned: ReturnType<typeof scanProjectRecords> | null = null;
  // R2 first (Ben, 21 Oct 2026: the Vercel Hobby Blob store was suspended over its limits).
  const r2 = r2Config();
  const r2Host = r2 ? createR2Host(r2) : null;
  const blob = !r2Host && process.env.BLOB_READ_WRITE_TOKEN;
  return {
    youtubeToken: getYouTubeAccessToken,
    fetchVideos: fetchYouTubeVideos,
    listScheduled: listScheduledUploads,
    listRecentlyPublic: (token, now) => listRecentlyPublic(token, now),
    client: key ? createBufferApiClient(key) : null,
    store: createFileBufferStore(opts.ledgerFile ?? LEDGER_FILE),
    host: r2Host?.host ?? (blob ? hostOnVercelBlob : null),
    deleteMedia: r2Host?.deleteMedia ?? (blob ? deleteFromVercelBlob : undefined),
    listMedia: r2Host?.listMedia ?? (blob ? listVercelBlobMedia : undefined),
    checkUrl: (url, want) => checkMediaUrl(url, want),
    channelIds: opts.channelIds ?? loadChannelIds(),
    now: () => new Date(),
    findMedia: (videoId) =>
      findMedia(videoId, {
        registry: loadRegistry(UPLOADS_FILE),
        scanned: (scanned ??= scanProjectRecords(REPO_ROOT)),
        repoRoot: REPO_ROOT,
        registryFile: UPLOADS_FILE,
      }),
  };
}
