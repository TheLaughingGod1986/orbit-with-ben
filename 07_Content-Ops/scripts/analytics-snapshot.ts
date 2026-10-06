#!/usr/bin/env tsx
/**
 * Daily channel snapshot for Orbit With Ben and History of Science (read only, no spend).
 *
 *   cd 07_Content-Ops && npm run analytics:snapshot                # both channels, today (London)
 *   cd 07_Content-Ops && npm run analytics:snapshot -- --channel hos --date 2026-10-06
 *
 * Writes 05_Analytics/<channel>/snapshots/<date>.json (every video's views, likes, comments and
 * the channel totals) and, once the channel has signed in for YouTube Analytics,
 * 05_Analytics/<channel>/channel_daily.json (views, watch time and subscribers for every day
 * since launch) plus each video's last 7 / 28 days. Then run `npm run analytics:report`.
 *
 * Tokens (07_Content-Ops/.env, never printed):
 *   YT_ANALYTICS_REFRESH_TOKEN_OWB / _HOS  read-only sign-in per channel (scripts/youtube-auth.ts --analytics owb|hos)
 *   YOUTUBE_REFRESH_TOKEN                  fallback for the public numbers only
 */
import fs from "fs";
import path from "path";
import { refreshAccessToken } from "../src/lib/youtube/data-api";
import {
  CHANNELS,
  addDays,
  londonDate,
  toDailyRows,
  toVideoStat,
  toVideoWindows,
  type ChannelDaily,
  type ChannelKey,
  type Snapshot,
} from "../src/lib/analytics/channel-tracker";

const API = "https://www.googleapis.com/youtube/v3";
const ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports";
export const ANALYTICS_ROOT = path.resolve(__dirname, "../../05_Analytics");
/** YouTube Analytics is about two days behind; asking for later days returns nothing for them. */
const ANALYTICS_LAG_DAYS = 2;

async function get(token: string, url: string) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(`${url.split("?")[0]} ${res.status} ${JSON.stringify(body?.error?.message ?? body).slice(0, 200)}`);
    (err as Error & { status?: number }).status = res.status;
    throw err;
  }
  return body;
}

function args() {
  const a = process.argv.slice(2);
  const val = (k: string) => (a.includes(k) ? a[a.indexOf(k) + 1] : undefined);
  const ch = val("--channel") ?? "all";
  if (ch !== "all" && !(ch in CHANNELS)) throw new Error(`--channel must be owb, hos or all (got ${ch})`);
  return { channels: (ch === "all" ? Object.keys(CHANNELS) : [ch]) as ChannelKey[], date: val("--date") ?? londonDate() };
}

async function snapshot(key: ChannelKey, date: string): Promise<string> {
  const meta = CHANNELS[key];
  const own = process.env[meta.tokenKey];
  const fallback = process.env.YOUTUBE_REFRESH_TOKEN;
  if (!own && !fallback) throw new Error(`no token (${meta.tokenKey} or YOUTUBE_REFRESH_TOKEN) in .env`);
  const token = (await refreshAccessToken((own ?? fallback)!)).token;

  // Public numbers: channel totals and every upload. Read by channel id, so any token works.
  const ch = await get(token, `${API}/channels?part=snippet,statistics,contentDetails&id=${meta.id}`);
  const item = ch.items?.[0];
  if (!item) throw new Error(`${key}: channel ${meta.id} not found`);
  const uploads: string = item.contentDetails.relatedPlaylists.uploads;
  const ids: string[] = [];
  let page = "";
  do {
    const pl = await get(token, `${API}/playlistItems?part=contentDetails&maxResults=50&playlistId=${uploads}${page ? `&pageToken=${page}` : ""}`);
    for (const i of pl.items ?? []) if (i.contentDetails?.videoId) ids.push(i.contentDetails.videoId);
    page = pl.nextPageToken ?? "";
  } while (page);
  const videos = [];
  for (let i = 0; i < ids.length; i += 50) {
    const body = await get(token, `${API}/videos?part=snippet,statistics,contentDetails,status&id=${ids.slice(i, i + 50).join(",")}`);
    videos.push(...(body.items ?? []).map(toVideoStat));
  }
  const s = item.statistics ?? {};
  const snap: Snapshot = {
    channel: key,
    channelId: meta.id,
    date,
    takenAt: new Date().toISOString(),
    totals: {
      subscribers: s.hiddenSubscriberCount ? null : Number(s.subscriberCount ?? 0),
      views: Number(s.viewCount ?? 0),
      videos: Number(s.videoCount ?? videos.length),
    },
    videos: videos.sort((a, b) => (b.publishedAt ?? "").localeCompare(a.publishedAt ?? "")),
    analytics: null,
  };

  // Private numbers: only with this channel's own read-only Analytics sign-in.
  const dir = path.join(ANALYTICS_ROOT, key);
  let analyticsLine = "YouTube Analytics: not connected";
  if (!own) {
    snap.note = `YouTube Analytics isn't connected for ${meta.name} yet (run "npx tsx --env-file=.env scripts/youtube-auth.ts --analytics ${key}" once).`;
  } else {
    try {
      const mine = await get(token, `${API}/channels?part=id&mine=true`);
      if (mine.items?.[0]?.id !== meta.id) throw new Error(`the ${meta.tokenKey} sign-in is not ${meta.name}`);
      const through = addDays(date, -ANALYTICS_LAG_DAYS);
      const start = item.snippet.publishedAt.slice(0, 10);
      const q = (p: Record<string, string>) => `${ANALYTICS}?${new URLSearchParams({ ids: "channel==MINE", endDate: through, ...p })}`;
      const daily = await get(
        token,
        q({ startDate: start, dimensions: "day", sort: "day", metrics: "views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments,shares" }),
      );
      const top = (from: string) =>
        get(token, q({ startDate: from, dimensions: "video", sort: "-views", maxResults: "200", metrics: "views,estimatedMinutesWatched,subscribersGained,averageViewDuration,averageViewPercentage" }));
      const [last7, last28, lifetime] = await Promise.all([top(addDays(through, -6)), top(addDays(through, -27)), top(start)]);
      snap.analytics = { through, last7: toVideoWindows(last7), last28: toVideoWindows(last28), lifetime: toVideoWindows(lifetime) };
      const file: ChannelDaily = { channel: key, through, rows: toDailyRows(daily) };
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, "channel_daily.json"), JSON.stringify(file, null, 0).replace(/},{/g, "},\n{") + "\n");
      analyticsLine = `YouTube Analytics through ${through}: ${file.rows.length} days`;
    } catch (e) {
      const status = (e as Error & { status?: number }).status;
      const why = status === 403 ? "the sign-in lacks yt-analytics.readonly, or the YouTube Analytics API isn't enabled on the Google Cloud project" : (e as Error).message;
      snap.note = `YouTube Analytics failed for ${meta.name}: ${why}.`;
      analyticsLine = `YouTube Analytics FAILED: ${why}`;
    }
  }

  const out = path.join(dir, "snapshots", `${date}.json`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, serialiseSnapshot(snap));
  return `${meta.name}: ${snap.totals.subscribers ?? "hidden"} subs, ${snap.totals.views} views, ${videos.length} videos → ${path.relative(process.cwd(), out)}. ${analyticsLine}`;
}

/** One video per line and the Analytics block on one line, so the daily git diff stays readable. */
export function serialiseSnapshot(snap: Snapshot): string {
  const { videos, analytics, ...head } = snap;
  return (
    JSON.stringify({ ...head, analytics: "__A__", videos: "__V__" }, null, 1)
      .replace('"__A__"', () => JSON.stringify(analytics))
      .replace('"__V__"', () => `[\n${videos.map((v) => JSON.stringify(v)).join(",\n")}\n]`) + "\n"
  );
}

async function main() {
  const { channels, date } = args();
  let failed = 0;
  for (const key of channels) {
    try {
      console.log(await snapshot(key, date));
    } catch (e) {
      failed++;
      console.error(`${key}: ${(e as Error).message}`);
    }
  }
  if (failed) process.exit(1);
}

if (require.main === module) main();
