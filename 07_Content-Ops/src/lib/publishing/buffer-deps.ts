/**
 * Real dependencies for the Buffer mirror: YouTube via YOUTUBE_REFRESH_TOKEN, Buffer via
 * BUFFER_API_KEY, media via the public Vercel Blob store (BLOB_READ_WRITE_TOKEN), and the
 * BUFFER_POSTS.json record. Missing keys degrade to plan-only rather than failing.
 */
import fs from "fs";
import path from "path";
import { BUFFER_CHANNELS, type ChannelIds } from "@/lib/publishing/buffer-mirror";
import { createBufferApiClient } from "@/lib/publishing/buffer-api";
import { createFileBufferStore } from "@/lib/publishing/buffer-store";
import { checkMediaUrl, deleteFromVercelBlob, hostOnVercelBlob, listVercelBlobMedia } from "@/lib/publishing/media-host";
import { findMedia, loadRegistry, scanProjectRecords } from "@/lib/publishing/media-finder";
import type { MirrorDeps } from "@/lib/publishing/buffer-runner";
import { fetchYouTubeVideos, getYouTubeAccessToken, listScheduledUploads } from "@/lib/youtube/data-api";

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
  return {
    youtubeToken: getYouTubeAccessToken,
    fetchVideos: fetchYouTubeVideos,
    listScheduled: listScheduledUploads,
    client: key ? createBufferApiClient(key) : null,
    store: createFileBufferStore(opts.ledgerFile ?? LEDGER_FILE),
    host: process.env.BLOB_READ_WRITE_TOKEN ? hostOnVercelBlob : null,
    deleteMedia: process.env.BLOB_READ_WRITE_TOKEN ? deleteFromVercelBlob : undefined,
    listMedia: process.env.BLOB_READ_WRITE_TOKEN ? listVercelBlobMedia : undefined,
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
