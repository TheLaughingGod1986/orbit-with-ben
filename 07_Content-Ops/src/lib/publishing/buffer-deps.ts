/**
 * Real dependencies for the Buffer mirror, per channel profile (buffer-profile.ts): YouTube via the profile's
 * refresh token, Buffer via its key (BUFFER_API_KEY for Orbit, BUFFER_HOS_API_KEY for History of Science), media
 * via the public Cloudflare R2 bucket (R2_* keys; the Vercel Blob store, BLOB_READ_WRITE_TOKEN, only for Orbit when
 * R2 isn't set up), and the profile's BUFFER_POSTS.json record. Missing keys degrade to plan-only rather than failing.
 */
import fs from "fs";
import path from "path";
import { type ChannelIds } from "@/lib/publishing/buffer-mirror";
import { createBufferApiClient } from "@/lib/publishing/buffer-api";
import { checkChannelsFile, getProfile, ownedByOtherProfile, profileFiles, refuseChannel, type BufferProfile } from "@/lib/publishing/buffer-profile";
import { createFileBufferStore } from "@/lib/publishing/buffer-store";
import { checkMediaUrl, deleteFromVercelBlob, hostOnVercelBlob, listVercelBlobMedia } from "@/lib/publishing/media-host";
import { createR2Host, r2Config } from "@/lib/publishing/media-host-r2";
import { findMedia, loadRegistry, scanProjectRecords } from "@/lib/publishing/media-finder";
import type { MirrorDeps } from "@/lib/publishing/buffer-runner";
import {
  fetchYouTubeVideos,
  getChannelAccessToken,
  getYouTubeAccessToken,
  listRecentlyPublic,
  listScheduledUploads,
} from "@/lib/youtube/data-api";

export const REPO_ROOT = path.resolve(__dirname, "../../../..");
export const SOCIAL_DIR = path.join(REPO_ROOT, "00_Brand/Channel-Setup/social");
export const CHANNELS_FILE = path.join(SOCIAL_DIR, "BUFFER_CHANNELS.json");
export const LEDGER_FILE = path.join(SOCIAL_DIR, "BUFFER_POSTS.json");
export const UPLOADS_FILE = path.join(SOCIAL_DIR, "UPLOADS.json");

/** Channel ids from the profile's BUFFER_CHANNELS.json, refused if any isn't the profile's own. */
export function loadChannelIds(file = CHANNELS_FILE, profile: BufferProfile = getProfile("owb")): ChannelIds {
  if (!fs.existsSync(file)) return {};
  return checkChannelsFile(profile, JSON.parse(fs.readFileSync(file, "utf8")));
}

export function createMirrorDeps(opts: { channelIds?: ChannelIds; ledgerFile?: string; profile?: BufferProfile } = {}): MirrorDeps {
  const profile = opts.profile ?? getProfile("owb");
  const files = profileFiles(profile, REPO_ROOT);
  const key = process.env[profile.keyEnv];
  // Old project records are scanned once per run, only if something needs them.
  let scanned: ReturnType<typeof scanProjectRecords> | null = null;
  // R2 first (Ben, 21 Oct 2026: the Vercel Hobby Blob store was suspended over its limits). HOS uses R2 only.
  const r2 = r2Config();
  const r2Host = r2 ? createR2Host(r2) : null;
  const blob = !r2Host && profile.id === "owb" && process.env.BLOB_READ_WRITE_TOKEN;
  return {
    youtubeToken: profile.id === "owb" ? getYouTubeAccessToken : () => getChannelAccessToken(profile.youtubeTokenEnv, profile.youtubeChannelId),
    fetchVideos: fetchYouTubeVideos,
    listScheduled: listScheduledUploads,
    listRecentlyPublic: (token, now) => listRecentlyPublic(token, now),
    client: key ? createBufferApiClient(key) : null,
    store: createFileBufferStore(opts.ledgerFile ?? files.ledger),
    host: r2Host?.host ?? (blob ? hostOnVercelBlob : null),
    deleteMedia: r2Host?.deleteMedia ?? (blob ? deleteFromVercelBlob : undefined),
    listMedia: r2Host?.listMedia ?? (blob ? listVercelBlobMedia : undefined),
    checkUrl: (url, want) => checkMediaUrl(url, want),
    channelIds: opts.channelIds ?? loadChannelIds(files.channels, profile),
    now: () => new Date(),
    networks: profile.networks,
    shortsOnly: profile.shortsOnly,
    mediaPrefix: profile.mediaPrefix,
    foreignMedia: (pathname) => ownedByOtherProfile(pathname, profile),
    refuseChannel: (id) => refuseChannel(profile, id),
    findMedia: (videoId) =>
      findMedia(videoId, {
        registry: loadRegistry(files.uploads),
        scanned: profile.scanProjects ? (scanned ??= scanProjectRecords(REPO_ROOT)) : new Map(),
        repoRoot: REPO_ROOT,
        registryFile: files.uploads,
      }),
  };
}
