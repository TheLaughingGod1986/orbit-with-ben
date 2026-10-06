/**
 * Channel tracker (6 Oct 2026): daily stats for every Orbit With Ben and History of Science
 * video, and the daily / weekly / monthly growth built from them.
 *
 * Two sources, both read only:
 *  - YouTube Data API: each video's total views, likes and comments, and the channel's
 *    subscriber and view totals, as they stand today. One file per channel per day, so the
 *    day-on-day difference is that day's growth. Public data, so any signed-in token reads it.
 *  - YouTube Analytics API (when the channel has signed in with yt-analytics.readonly): the
 *    channel's views, watch time and subscribers for every day since launch, and each video's
 *    views, watch time and average % viewed over the last 7 and 28 days. It runs about two
 *    days behind, so the newest days fill in later.
 *
 * Files (05_Analytics/<channel>/): snapshots/<date>.json, channel_daily.json, REPORT.md.
 * Everything here is pure, so it's unit tested; scripts/analytics-snapshot.ts does the fetching.
 */
import { parseIsoDuration } from "@/lib/publishing/buffer-mirror";

export type ChannelKey = "owb" | "hos";

export const CHANNELS: Record<ChannelKey, { id: string; name: string; handle: string; tokenKey: string }> = {
  owb: { id: "UC_esArsDKd3GJvOkeO0DUog", name: "Orbit With Ben", handle: "@OrbitWithBen", tokenKey: "YT_ANALYTICS_REFRESH_TOKEN_OWB" },
  hos: { id: "UCXp7HkBIl1LgaznXuZHJyRg", name: "History of Science", handle: "@HistoryOfScienceYT", tokenKey: "YT_ANALYTICS_REFRESH_TOKEN_HOS" },
};

/** A Short is at most 3 minutes; every long on both channels runs well past that. */
export const SHORT_MAX_SECONDS = 180;

export type VideoStat = {
  id: string;
  title: string;
  publishedAt: string | null;
  seconds: number;
  format: "short" | "long";
  privacy: string;
  views: number;
  likes: number;
  comments: number;
};

export type VideoWindow = { views: number; minutes: number; subs: number; avgViewSeconds: number | null; avgViewPct: number | null };

export type Snapshot = {
  channel: ChannelKey;
  channelId: string;
  date: string;
  takenAt: string;
  totals: { subscribers: number | null; views: number; videos: number };
  videos: VideoStat[];
  analytics: null | { through: string; last7: Record<string, VideoWindow>; last28: Record<string, VideoWindow>; lifetime: Record<string, VideoWindow> };
  note?: string;
};

export type DailyRow = { day: string; views: number; minutes: number; subsGained: number; subsLost: number; likes: number; comments: number; shares: number };

export type ChannelDaily = { channel: ChannelKey; through: string; rows: DailyRow[] };

// ----------------------------------------------------------------------------- dates
/** The calendar date in London for an instant, as YYYY-MM-DD. */
export function londonDate(at: Date = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/London", year: "numeric", month: "2-digit", day: "2-digit" }).format(at);
}

export function addDays(day: string, n: number): string {
  const d = new Date(`${day}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

export function daysBetween(from: string, to: string): number {
  return Math.round((Date.parse(`${to}T12:00:00Z`) - Date.parse(`${from}T12:00:00Z`)) / 86_400_000);
}

/** The Monday that starts the ISO week holding `day`. */
export function weekStart(day: string): string {
  const dow = new Date(`${day}T12:00:00Z`).getUTCDay(); // 0 = Sunday
  return addDays(day, -((dow + 6) % 7));
}

// ----------------------------------------------------------------------------- API parsing
type ApiVideo = {
  id: string;
  snippet?: { title?: string; publishedAt?: string };
  status?: { privacyStatus?: string };
  contentDetails?: { duration?: string };
  statistics?: { viewCount?: string; likeCount?: string; commentCount?: string };
};

export function toVideoStat(item: ApiVideo): VideoStat {
  const seconds = parseIsoDuration(item.contentDetails?.duration);
  return {
    id: item.id,
    title: item.snippet?.title ?? "",
    publishedAt: item.snippet?.publishedAt ?? null,
    seconds,
    format: seconds > 0 && seconds <= SHORT_MAX_SECONDS ? "short" : "long",
    privacy: item.status?.privacyStatus ?? "unknown",
    views: Number(item.statistics?.viewCount ?? 0),
    likes: Number(item.statistics?.likeCount ?? 0),
    comments: Number(item.statistics?.commentCount ?? 0),
  };
}

type AnalyticsTable = { columnHeaders?: { name: string }[]; rows?: (string | number)[][] };

/** A YouTube Analytics report as an array of objects keyed by column name. */
export function tableRows(t: AnalyticsTable): Record<string, string | number>[] {
  const names = (t.columnHeaders ?? []).map((c) => c.name);
  return (t.rows ?? []).map((r) => Object.fromEntries(names.map((n, i) => [n, r[i]])));
}

export function toDailyRows(t: AnalyticsTable): DailyRow[] {
  return tableRows(t).map((r) => ({
    day: String(r.day),
    views: Number(r.views ?? 0),
    minutes: Number(r.estimatedMinutesWatched ?? 0),
    subsGained: Number(r.subscribersGained ?? 0),
    subsLost: Number(r.subscribersLost ?? 0),
    likes: Number(r.likes ?? 0),
    comments: Number(r.comments ?? 0),
    shares: Number(r.shares ?? 0),
  }));
}

export function toVideoWindows(t: AnalyticsTable): Record<string, VideoWindow> {
  const out: Record<string, VideoWindow> = {};
  for (const r of tableRows(t)) {
    out[String(r.video)] = {
      views: Number(r.views ?? 0),
      minutes: Number(r.estimatedMinutesWatched ?? 0),
      subs: Number(r.subscribersGained ?? 0),
      avgViewSeconds: r.averageViewDuration == null ? null : Number(r.averageViewDuration),
      avgViewPct: r.averageViewPercentage == null ? null : Number(r.averageViewPercentage),
    };
  }
  return out;
}

// ----------------------------------------------------------------------------- report
export type Change = { views: number; subscribers: number | null; source: "snapshots" | "analytics" } | null;

export type PeriodRow = { period: string; views: number; minutes: number | null; subsNet: number | null; uploads: number; source: "analytics" | "snapshots" };

export type VideoRow = {
  id: string;
  title: string;
  format: "short" | "long";
  publishedAt: string | null;
  ageDays: number | null;
  views: number;
  likes: number;
  comments: number;
  d1: number | null;
  d7: number | null;
  d30: number | null;
  perDay: number | null;
  last28: VideoWindow | null;
  lifetime: VideoWindow | null;
};

export type ChannelReport = {
  channel: ChannelKey;
  name: string;
  handle: string;
  date: string;
  firstSnapshot: string;
  analyticsThrough: string | null;
  totals: Snapshot["totals"];
  change: { d1: Change; d7: Change; d30: Change };
  windowSource: { d7: "snapshots" | "analytics" | null; d30: "snapshots" | "analytics" | null };
  daily: { day: string; views: number; minutes: number | null; subsNet: number | null }[];
  weekly: PeriodRow[];
  monthly: PeriodRow[];
  videos: VideoRow[];
  notes: string[];
};

/** The newest snapshot taken on or before `day`. Snapshots must be sorted by date. */
export function snapshotAtOrBefore(snaps: Snapshot[], day: string): Snapshot | null {
  let best: Snapshot | null = null;
  for (const s of snaps) if (s.date <= day) best = s;
  return best;
}

/** Views a video gained since `then`. A video published after `then` gained all its views since. */
function videoDelta(v: VideoStat, then: Snapshot | null): number | null {
  if (!then) return null;
  const old = then.videos.find((o) => o.id === v.id);
  if (old) return v.views - old.views;
  if (v.publishedAt && v.publishedAt.slice(0, 10) > then.date) return v.views;
  return null;
}

function channelChange(now: Snapshot, then: Snapshot | null, daily: DailyRow[], days: number): Change {
  if (then && then.date < now.date) {
    const subs = now.totals.subscribers != null && then.totals.subscribers != null ? now.totals.subscribers - then.totals.subscribers : null;
    return { views: now.totals.views - then.totals.views, subscribers: subs, source: "snapshots" };
  }
  if (daily.length >= days) {
    const rows = daily.slice(-days);
    return { views: sum(rows.map((r) => r.views)), subscribers: sum(rows.map((r) => r.subsGained - r.subsLost)), source: "analytics" };
  }
  return null;
}

function sum(xs: number[]): number {
  return xs.reduce((a, b) => a + b, 0);
}

function periods(
  key: (day: string) => string,
  daily: DailyRow[],
  derived: { day: string; views: number; subsNet: number | null }[],
  uploads: Map<string, number>,
): PeriodRow[] {
  const out = new Map<string, PeriodRow>();
  const row = (p: string, source: PeriodRow["source"]) => {
    if (!out.has(p)) out.set(p, { period: p, views: 0, minutes: source === "analytics" ? 0 : null, subsNet: 0, uploads: uploads.get(p) ?? 0, source });
    return out.get(p)!;
  };
  if (daily.length) {
    for (const d of daily) {
      const r = row(key(d.day), "analytics");
      r.views += d.views;
      r.minutes = (r.minutes ?? 0) + d.minutes;
      r.subsNet = (r.subsNet ?? 0) + d.subsGained - d.subsLost;
    }
  } else {
    for (const d of derived) {
      const r = row(key(d.day), "snapshots");
      r.views += d.views;
      r.subsNet = d.subsNet == null || r.subsNet == null ? null : r.subsNet + d.subsNet;
    }
  }
  for (const [p, n] of uploads) if (out.has(p)) out.get(p)!.uploads = n;
  return [...out.values()].sort((a, b) => a.period.localeCompare(b.period));
}

/** Everything the dashboard and REPORT.md show for one channel. `snaps` in any order. */
export function buildReport(channel: ChannelKey, snapsIn: Snapshot[], dailyFile: ChannelDaily | null): ChannelReport {
  const snaps = [...snapsIn].sort((a, b) => a.date.localeCompare(b.date));
  if (!snaps.length) throw new Error(`no snapshots for ${channel}`);
  const now = snaps[snaps.length - 1];
  const daily = (dailyFile?.rows ?? []).filter((r) => r.day <= now.date).sort((a, b) => a.day.localeCompare(b.day));
  const meta = CHANNELS[channel];
  const notes: string[] = [];

  const then = (n: number) => snapshotAtOrBefore(snaps, addDays(now.date, -n));
  const t1 = then(1);
  const t7 = then(7);
  const t30 = then(30);
  const old = (s: Snapshot | null, n: number) => (s && daysBetween(s.date, now.date) >= n ? s : null);

  // Day-by-day from the snapshots (used when the Analytics API isn't connected yet).
  const derived: { day: string; views: number; subsNet: number | null }[] = [];
  for (let i = 1; i < snaps.length; i++) {
    const a = snaps[i - 1];
    const b = snaps[i];
    const subs = a.totals.subscribers != null && b.totals.subscribers != null ? b.totals.subscribers - a.totals.subscribers : null;
    derived.push({ day: b.date, views: b.totals.views - a.totals.views, subsNet: subs });
  }

  const publicVideos = now.videos.filter((v) => v.privacy === "public");
  const uploadsBy = (key: (d: string) => string) => {
    const m = new Map<string, number>();
    for (const v of publicVideos) if (v.publishedAt) m.set(key(v.publishedAt.slice(0, 10)), (m.get(key(v.publishedAt.slice(0, 10))) ?? 0) + 1);
    return m;
  };

  const a = now.analytics;
  const d7Snap = old(t7, 7);
  const d30Snap = old(t30, 30);
  const videos: VideoRow[] = publicVideos
    .map((v) => {
      const published = v.publishedAt?.slice(0, 10) ?? null;
      const ageDays = published ? Math.max(daysBetween(published, now.date), 0) : null;
      const d7 = d7Snap ? videoDelta(v, d7Snap) : (a?.last7[v.id]?.views ?? (a ? 0 : null));
      const d30 = d30Snap ? videoDelta(v, d30Snap) : (a?.last28[v.id]?.views ?? (a ? 0 : null));
      return {
        id: v.id,
        title: v.title,
        format: v.format,
        publishedAt: v.publishedAt,
        ageDays,
        views: v.views,
        likes: v.likes,
        comments: v.comments,
        d1: old(t1, 1) ? videoDelta(v, t1) : null,
        d7,
        d30,
        perDay: ageDays != null ? Math.round((v.views / Math.max(ageDays, 1)) * 10) / 10 : null,
        last28: a?.last28[v.id] ?? (a ? { views: 0, minutes: 0, subs: 0, avgViewSeconds: null, avgViewPct: null } : null),
        lifetime: a?.lifetime[v.id] ?? null,
      };
    })
    .sort((x, y) => (y.publishedAt ?? "").localeCompare(x.publishedAt ?? ""));

  if (!a) notes.push(now.note ?? "YouTube Analytics isn't connected for this channel yet, so watch time, average % viewed and history before the first snapshot are missing.");
  if (snaps.length < 2) notes.push("Day-on-day growth starts with the second daily snapshot.");
  if (!d7Snap && a) notes.push("7-day video growth comes from YouTube Analytics (it runs about 2 days behind) until there are 7 days of snapshots.");
  if (!d30Snap && a) notes.push("30-day video growth is YouTube Analytics' last 28 days until there are 30 days of snapshots.");
  if (now.totals.subscribers != null) notes.push("YouTube rounds the public subscriber total to 3 significant figures; subscriber gains from YouTube Analytics are exact.");

  const dailyOut = daily.length
    ? daily.slice(-120).map((r) => ({ day: r.day, views: r.views, minutes: r.minutes, subsNet: r.subsGained - r.subsLost }))
    : derived.slice(-120).map((r) => ({ day: r.day, views: r.views, minutes: null, subsNet: r.subsNet }));

  return {
    channel,
    name: meta.name,
    handle: meta.handle,
    date: now.date,
    firstSnapshot: snaps[0].date,
    analyticsThrough: dailyFile?.through ?? null,
    totals: now.totals,
    change: {
      d1: channelChange(now, old(t1, 1), daily, 1),
      d7: channelChange(now, d7Snap, daily, 7),
      d30: channelChange(now, d30Snap, daily, 30),
    },
    windowSource: { d7: d7Snap ? "snapshots" : a ? "analytics" : null, d30: d30Snap ? "snapshots" : a ? "analytics" : null },
    daily: dailyOut,
    weekly: periods(weekStart, daily, derived, uploadsBy(weekStart)).slice(-26),
    monthly: periods((d) => d.slice(0, 7), daily, derived, uploadsBy((d) => d.slice(0, 7))),
    videos,
    notes,
  };
}

// ----------------------------------------------------------------------------- markdown
const n0 = (x: number | null | undefined) => (x == null ? "–" : Math.round(x).toLocaleString("en-GB"));
const signed = (x: number | null | undefined) => (x == null ? "–" : `${x > 0 ? "+" : ""}${Math.round(x).toLocaleString("en-GB")}`);
const hours = (minutes: number | null | undefined) => (minutes == null ? "–" : (minutes / 60).toLocaleString("en-GB", { maximumFractionDigits: 1 }));
const cell = (s: string) => s.replace(/\|/g, "\\|");

export function renderMarkdown(r: ChannelReport): string {
  const L: string[] = [];
  L.push(`# ${r.name}: channel tracker`, "");
  L.push(`Generated from the ${r.date} snapshot by \`npm run analytics:report\`. Don't edit by hand.`, "");
  L.push(`**${n0(r.totals.subscribers)} subscribers · ${n0(r.totals.views)} views · ${r.totals.videos} videos**`, "");
  L.push("| Growth | Views | Subscribers |", "|---|---:|---:|");
  for (const [label, c] of [["Last day", r.change.d1], ["Last 7 days", r.change.d7], ["Last 30 days", r.change.d30]] as const) {
    L.push(`| ${label}${c?.source === "analytics" ? " (YouTube Analytics)" : ""} | ${signed(c?.views)} | ${signed(c?.subscribers)} |`);
  }
  L.push("");
  const table = (title: string, rows: PeriodRow[]) => {
    L.push(`## ${title}`, "", "| Period | Views | Watch hours | Subscribers | Uploads |", "|---|---:|---:|---:|---:|");
    for (const p of [...rows].reverse()) L.push(`| ${p.period} | ${n0(p.views)} | ${hours(p.minutes)} | ${signed(p.subsNet)} | ${p.uploads} |`);
    L.push("");
  };
  table("Weekly (week starting Monday)", r.weekly.slice(-12));
  table("Monthly", r.monthly);
  L.push("## Every video (newest first)", "");
  L.push(`| Published | Title | Format | Views | +1 day | +7 days | +30 days | Views/day | Avg % viewed (28 d) |`);
  L.push("|---|---|---|---:|---:|---:|---:|---:|---:|");
  for (const v of r.videos) {
    const pct = v.last28?.avgViewPct == null ? "–" : `${v.last28.avgViewPct.toFixed(0)}%`;
    L.push(
      `| ${v.publishedAt?.slice(0, 10) ?? "–"} | [${cell(v.title)}](https://youtu.be/${v.id}) | ${v.format} | ${n0(v.views)} | ${signed(v.d1)} | ${signed(v.d7)} | ${signed(v.d30)} | ${v.perDay ?? "–"} | ${pct} |`,
    );
  }
  L.push("");
  if (r.notes.length) {
    L.push("## Notes", "");
    for (const n of r.notes) L.push(`- ${n}`);
    L.push("");
  }
  return L.join("\n");
}
