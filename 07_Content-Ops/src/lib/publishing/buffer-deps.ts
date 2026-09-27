/**
 * Real dependencies for the Buffer mirror (Node only): YouTube via the saved channel
 * token, Buffer via BUFFER_API_KEY, media via the public Vercel Blob store, and the
 * BufferMirrorPost table. Missing keys degrade to plan-only rather than failing.
 */
import fs from "fs";
import { prisma } from "@/lib/storage/prisma";
import { BUFFER_CHANNELS, type ChannelIds } from "@/lib/publishing/buffer-mirror";
import { createBufferApiClient } from "@/lib/publishing/buffer-api";
import { createPrismaBufferStore } from "@/lib/publishing/buffer-store";
import { checkMediaUrl, hostOnVercelBlob } from "@/lib/publishing/media-host";
import type { MirrorDeps } from "@/lib/publishing/buffer-runner";
import { fetchYouTubeVideos, getYouTubeAccessToken, listScheduledUploads } from "@/lib/youtube/data-api";

/** Channel ids from 00_Brand/Channel-Setup/social/BUFFER_CHANNELS.json. */
export function loadChannelIds(file: string): ChannelIds {
  if (!fs.existsSync(file)) return {};
  const cfg = JSON.parse(fs.readFileSync(file, "utf8")) as { channels?: Record<string, { id?: string }> };
  const ids: ChannelIds = {};
  for (const c of BUFFER_CHANNELS) {
    const id = cfg.channels?.[c]?.id;
    if (id) ids[c] = id;
  }
  return ids;
}

export function createMirrorDeps(opts: { channelIds?: ChannelIds } = {}): MirrorDeps {
  const key = process.env.BUFFER_API_KEY;
  return {
    youtubeToken: getYouTubeAccessToken,
    fetchVideos: fetchYouTubeVideos,
    listScheduled: listScheduledUploads,
    client: key ? createBufferApiClient(key) : null,
    store: createPrismaBufferStore(prisma),
    host: process.env.BLOB_READ_WRITE_TOKEN ? hostOnVercelBlob : null,
    checkUrl: (url, want) => checkMediaUrl(url, want),
    channelIds: opts.channelIds ?? {},
    now: () => new Date(),
  };
}
