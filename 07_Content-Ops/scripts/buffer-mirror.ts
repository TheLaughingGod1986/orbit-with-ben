#!/usr/bin/env tsx
/**
 * Mirror a YouTube upload to Instagram, Facebook and Threads through Buffer
 * (STUDIO_PLAYBOOK.md §12). Reads the live video from the YouTube API, so the
 * Buffer posts carry exactly what Studio has: title, description, tags and the
 * go-public time. This script never posts; the agent sends each create_post /
 * edit_post / delete_post in the plan through the Buffer MCP, then records the
 * Buffer post id here.
 *
 *   # Short (mp4 hosted at a permanent public URL first, e.g. `vercel blob put … --access public`)
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts plan --video <shortId> --long <longId> --media-url <https://…mp4>
 *   # Long (Instagram gets the thumbnail; Facebook and Threads get the YouTube link card)
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts plan --video <longId> --thumb-url <https://…jpg>
 *   # After each Buffer call
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts record --video <id> --channel instagram --post-id <bufferPostId>
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts record --video <id> --channel instagram --deleted
 *   # Monday, or after any change in Studio: moved times and pulled videos
 *   npx tsx --env-file=.env scripts/buffer-mirror.ts check
 *
 * Files: 00_Brand/Channel-Setup/social/BUFFER_CHANNELS.json (channel ids),
 *        00_Brand/Channel-Setup/social/BUFFER_POSTS.json (ledger),
 *        00_Brand/Channel-Setup/social/buffer-plans/<id>.json (last plan per video).
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";
import {
  BUFFER_CHANNELS,
  BufferChannel,
  ChannelIds,
  Ledger,
  Plan,
  YouTubeVideo,
  parseIsoDuration,
  planBufferMirror,
  reconcileEntry,
  recordPost,
} from "../src/lib/publishing/buffer-mirror";

const SOCIAL = path.resolve(__dirname, "../../00_Brand/Channel-Setup/social");
const CHANNELS_FILE = path.join(SOCIAL, "BUFFER_CHANNELS.json");
const LEDGER_FILE = path.join(SOCIAL, "BUFFER_POSTS.json");
const PLANS_DIR = path.join(SOCIAL, "buffer-plans");

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}
const flag = (name: string) => process.argv.includes(`--${name}`);

function readJson<T>(file: string, fallback: T): T {
  return fs.existsSync(file) ? (JSON.parse(fs.readFileSync(file, "utf8")) as T) : fallback;
}
function writeJson(file: string, data: unknown) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
}

async function accessToken(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn) throw new Error("No connected YouTube account");
  if (!conn.refreshTokenEncrypted || !env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    if (!conn.accessTokenEncrypted) throw new Error("No YouTube token");
    return decryptSecret(conn.accessTokenEncrypted);
  }
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  });
  const body = await res.json();
  if (!res.ok || !body.access_token) throw new Error(`refresh failed: ${JSON.stringify(body).slice(0, 240)}`);
  await prisma.platformConnection.update({
    where: { id: conn.id },
    data: {
      accessTokenEncrypted: encryptSecret(body.access_token),
      accessTokenExpiresAt: new Date(Date.now() + Number(body.expires_in || 3600) * 1000),
      lastRefreshAt: new Date(),
    },
  });
  return body.access_token as string;
}

async function fetchVideos(token: string, ids: string[]): Promise<Map<string, YouTubeVideo>> {
  const out = new Map<string, YouTubeVideo>();
  for (let i = 0; i < ids.length; i += 50) {
    const batch = ids.slice(i, i + 50);
    const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${batch
      .map(encodeURIComponent)
      .join(",")}`;
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    const body = await res.json();
    if (!res.ok) throw new Error(`videos.list ${res.status} ${JSON.stringify(body).slice(0, 300)}`);
    for (const item of body.items ?? []) {
      out.set(item.id, {
        id: item.id,
        title: item.snippet?.title ?? "",
        description: item.snippet?.description ?? "",
        tags: item.snippet?.tags ?? [],
        durationSeconds: parseIsoDuration(item.contentDetails?.duration),
        privacyStatus: item.status?.privacyStatus ?? "unknown",
        publishAt: item.status?.publishAt ?? null,
        publishedAt: item.snippet?.publishedAt ?? null,
        containsSyntheticMedia: Boolean(item.status?.containsSyntheticMedia),
      });
    }
  }
  return out;
}

/** Buffer fetches media when the post goes out, so the URL must load for anyone, now and later. */
async function headCheck(url: string | undefined, want: "video" | "image"): Promise<string | null> {
  if (!url) return null;
  try {
    const res = await fetch(url, { method: "HEAD", redirect: "manual" });
    if (res.status !== 200) return `${url} answered ${res.status} (Buffer needs a direct 200, no redirect or login)`;
    const type = res.headers.get("content-type") || "";
    if (!type.startsWith(`${want}/`)) return `${url} is ${type || "no content-type"}, not ${want}/*`;
    return null;
  } catch (e) {
    return `${url} unreachable: ${(e as Error).message}`;
  }
}

function loadChannels(): ChannelIds {
  const cfg = readJson<{ channels?: Record<string, { id?: string }> }>(CHANNELS_FILE, {});
  const ids: ChannelIds = {};
  for (const c of BUFFER_CHANNELS) {
    const id = cfg.channels?.[c]?.id;
    if (id) ids[c] = id;
  }
  return ids;
}

function loadLedger(): Ledger {
  return readJson<Ledger>(LEDGER_FILE, { version: 1, videos: {} });
}

async function plan() {
  const videoId = arg("video");
  if (!videoId) throw new Error("plan needs --video <youtube id>");
  const longId = arg("long");
  const token = await accessToken();
  const videos = await fetchVideos(token, longId ? [videoId, longId] : [videoId]);
  const video = videos.get(videoId);
  if (!video) throw new Error(`${videoId} not found on the channel`);
  const long = longId ? videos.get(longId) : undefined;
  if (longId && !long) throw new Error(`long ${longId} not found on the channel`);

  const kind = arg("kind") as "short" | "long" | undefined;
  const result: Plan = planBufferMirror({
    video,
    channelIds: loadChannels(),
    ledger: loadLedger(),
    now: new Date(),
    kind,
    mediaUrl: arg("media-url"),
    thumbUrl: arg("thumb-url"),
    parentLong: long
      ? { id: long.id, goesPublicAt: long.privacyStatus === "public" ? long.publishedAt : long.publishAt }
      : null,
    standalone: flag("standalone"),
    allowLate: flag("allow-late"),
  });

  const creates = result.actions.filter((a) => a.action === "create_post");
  if (creates.length) {
    const want = result.kind === "short" ? "video" : "image";
    const url = result.kind === "short" ? arg("media-url") : arg("thumb-url");
    const problem = await headCheck(url, want);
    if (problem) {
      result.errors.push(problem);
      result.actions = [];
    }
  }

  const out = path.join(PLANS_DIR, `${videoId}.json`);
  writeJson(out, { plannedAt: new Date().toISOString(), ...result });
  console.log(JSON.stringify(result, null, 2));
  console.log(JSON.stringify({ wrote: path.relative(process.cwd(), out) }));
  if (result.errors.length) process.exit(1);
}

function record() {
  const videoId = arg("video");
  const channel = arg("channel") as BufferChannel | undefined;
  const postId = arg("post-id");
  const deleted = flag("deleted");
  if (!videoId || !channel || !BUFFER_CHANNELS.includes(channel) || (!postId && !deleted)) {
    throw new Error("record needs --video <id> --channel instagram|facebook|threads and --post-id <id> or --deleted");
  }
  const planFile = path.join(PLANS_DIR, `${videoId}.json`);
  if (!fs.existsSync(planFile)) throw new Error(`No plan for ${videoId}; run plan (or check) first`);
  const saved = readJson<Plan>(planFile, null as unknown as Plan);
  const next = recordPost(loadLedger(), saved, channel, deleted ? null : postId!, new Date());
  writeJson(LEDGER_FILE, next);
  console.log(JSON.stringify({ recorded: videoId, channel, postId: deleted ? null : postId, entry: next.videos[videoId] ?? null }));
}

async function check() {
  const ledger = loadLedger();
  const ids = Object.keys(ledger.videos);
  if (!ids.length) {
    console.log(JSON.stringify({ ok: true, videos: 0 }));
    return;
  }
  const videos = await fetchVideos(await accessToken(), ids);
  const now = new Date();
  const todo = [];
  for (const id of ids) {
    const video = videos.get(id) ?? null;
    const actions = reconcileEntry(id, ledger.videos[id], video, now);
    if (!actions.length) continue;
    // Save a plan whose timing matches YouTube, so `record` writes the new time.
    const timing: Plan["timing"] =
      video?.privacyStatus === "private" && video.publishAt
        ? { mode: "customScheduled", dueAt: new Date(video.publishAt).toISOString() }
        : { mode: "none", reason: "no longer going public" };
    const plan = { videoId: id, kind: ledger.videos[id].kind, title: ledger.videos[id].title, timing, actions, errors: [], warnings: [] };
    writeJson(path.join(PLANS_DIR, `${id}.json`), { plannedAt: now.toISOString(), ...plan });
    todo.push(plan);
  }
  console.log(JSON.stringify({ ok: todo.length === 0, videos: ids.length, todo }, null, 2));
}

async function main() {
  const cmd = process.argv[2];
  if (cmd === "plan") await plan();
  else if (cmd === "record") record();
  else if (cmd === "check") await check();
  else {
    console.error("Usage: buffer-mirror.ts plan|record|check  (see the header of this file)");
    process.exit(1);
  }
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect().catch(() => undefined));
