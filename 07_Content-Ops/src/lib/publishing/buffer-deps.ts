/**
 * Real dependencies for the Buffer mirror, per channel profile (buffer-profile.ts): YouTube via the profile's
 * refresh token, Buffer via its key (BUFFER_API_KEY for Orbit, BUFFER_HOS_API_KEY for History of Science), media
 * via the public Cloudflare R2 bucket (R2_* keys; the only media host since the Vercel Blob fallback was removed on
 * 29 Oct 2026), and the profile's BUFFER_POSTS.json record. Missing keys degrade to plan-only rather than failing.
 */
import fs from "fs";
import path from "path";
import { parseTagsFile } from "@/lib/publishing/youtube-package";
import { type ChannelIds } from "@/lib/publishing/buffer-mirror";
import { createBufferApiClient } from "@/lib/publishing/buffer-api";
import { checkChannelsFile, getProfile, ownedByOtherProfile, profileFiles, refuseChannel, type BufferProfile } from "@/lib/publishing/buffer-profile";
import { createFileBufferStore } from "@/lib/publishing/buffer-store";
import { checkMediaUrl } from "@/lib/publishing/media-host";
import { createR2Host, r2Config } from "@/lib/publishing/media-host-r2";
import { findMedia, loadRegistry, scanProjectRecords, validateShortSource } from "@/lib/publishing/media-finder";
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

/** Registered uploads may be absent from the uploads playlist entirely. */
export async function scheduledWithRegistry(token: string, now: Date, ids: string[], list = listScheduledUploads, byId = fetchYouTubeVideos) {
  const merged = new Map((await list(token, now)).map(v => [v.id,v]));
  for (const [id,video] of await byId(token, ids)) merged.set(id,video);
  return [...merged.values()].filter(v => v.privacyStatus === "private" && v.publishAt && Date.parse(v.publishAt) > now.getTime())
    .sort((a,b) => Date.parse(a.publishAt!) - Date.parse(b.publishAt!));
}

export function createMirrorDeps(opts: { channelIds?: ChannelIds; ledgerFile?: string; profile?: BufferProfile } = {}): MirrorDeps {
  const profile = opts.profile ?? getProfile("owb");
  const files = profileFiles(profile, REPO_ROOT);
  const key = process.env[profile.keyEnv];
  // Old project records are scanned once per run, only if something needs them.
  let scanned: ReturnType<typeof scanProjectRecords> | null = null;
  // R2 only (Ben, 21 Oct 2026: the Vercel Hobby Blob store was suspended over its limits; the Blob fallback was
  // removed on 29 Oct). Without the R2_* keys nothing can be hosted and the mirror stops with an error naming them.
  const r2 = r2Config();
  const r2Host = r2 ? createR2Host(r2) : null;
  return {
    youtubeToken: profile.id === "owb" ? getYouTubeAccessToken : () => getChannelAccessToken(profile.youtubeTokenEnv, profile.youtubeChannelId),
    fetchVideos: async (token, ids) => {
      const videos = await fetchYouTubeVideos(token, ids);
      const registry = loadRegistry(files.uploads);
      for (const [id, video] of videos) {
        // Immediately after upload, the live read can be missing tags. Only use
        // this video's registered package; never borrow its parent's metadata.
        if (profile.id === "owb" && !video.tags.length) video.tags = registeredPackageTags(REPO_ROOT, registry.videos[id]?.packageDir);
      }
      return videos;
    },
    listScheduled: (token, now) => scheduledWithRegistry(token, now, Object.keys(loadRegistry(files.uploads).videos)),
    listRecentlyPublic: (token, now) => listRecentlyPublic(token, now),
    client: key ? createBufferApiClient(key) : null,
    store: createFileBufferStore(opts.ledgerFile ?? files.ledger),
    host: r2Host?.host ?? null,
    deleteMedia: r2Host?.deleteMedia,
    listMedia: r2Host?.listMedia,
    checkUrl: (url, want) => checkMediaUrl(url, want),
    validateSource: (videoId, mediaPath, kind) => kind === "short" ? validateShortSource(loadRegistry(files.uploads).videos[videoId], mediaPath) : null,
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

/** Tags from the exact registered package, used only when the live record has none. */
export function registeredPackageTags(root: string, packageDir: unknown): string[] {
  if (typeof packageDir !== "string") return [];
  const dir = path.resolve(root, packageDir);
  if (!dir.startsWith(path.resolve(root) + path.sep)) return [];
  const manifest = path.join(dir, "PACKAGE_MANIFEST.json");
  if (!fs.existsSync(manifest)) return [];
  try {
    const data = JSON.parse(fs.readFileSync(manifest, "utf8"));
    if (Array.isArray(data.tags)) return data.tags.filter((t: unknown): t is string => typeof t === "string" && Boolean(t.trim()));
    const tagsFile = typeof data.tagsFile === "string" ? path.resolve(dir, data.tagsFile) :
      fs.existsSync(path.join(dir, "Tags")) ? fs.readdirSync(path.join(dir, "Tags")).filter(n => n.endsWith(".txt")).sort().map(n => path.join(dir, "Tags", n)).at(-1) : undefined;
    return tagsFile && tagsFile.startsWith(dir + path.sep) && fs.existsSync(tagsFile) ? parseTagsFile(fs.readFileSync(tagsFile, "utf8")) : [];
  } catch { return []; }
}
