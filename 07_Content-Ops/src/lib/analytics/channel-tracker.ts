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
  /** When a private video is scheduled to go public (the gate checks every Short scheduled in the next 14 days). */
  publishAt?: string | null;
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
  analytics: null | {
    through: string;
    last7: Record<string, VideoWindow>;
    last28: Record<string, VideoWindow>;
    lifetime: Record<string, VideoWindow>;
    /** Views by traffic source, per video: the last 28 days, and a Short's first two days (lesson R1). */
    sources?: Record<string, VideoSources>;
    /** Audience retention per public long over its lifetime (where viewers leave; Ben, 8 Oct 2026). */
    retention?: Record<string, RetentionPoint[]>;
  };
  note?: string;
};

export type VideoSources = { last28: Record<string, number>; day1: Record<string, number> | null };

/** One point of a retention curve: how far into the video (0-1), the share of viewers still watching (can start
 * above 1 with rewatches), and how that compares with videos of similar length (0-1, 0.5 = typical). */
export type RetentionPoint = { at: number; watching: number; relative: number | null };

/** Where viewers are at fixed moments of a long, as % still watching, and the first 30 s against similar videos. */
export type LongRetention = {
  points: { label: string; seconds: number; pct: number | null }[];
  relative30s: "lower" | "typical" | "higher" | null;
};

export function toRetention(t: AnalyticsTable): RetentionPoint[] {
  return tableRows(t)
    .map((r) => ({
      at: Number(r.elapsedVideoTimeRatio),
      watching: Number(r.audienceWatchRatio ?? 0),
      relative: r.relativeRetentionPerformance == null ? null : Number(r.relativeRetentionPerformance),
    }))
    .sort((a, b) => a.at - b.at);
}

/** Linear interpolation of a curve at a ratio (0-1); null outside the curve or for an empty one. */
export function curveAt(points: RetentionPoint[], at: number, key: "watching" | "relative" = "watching"): number | null {
  const pts = points.filter((p) => p[key] != null);
  if (!pts.length || at < pts[0].at - 1e-9 || at > pts[pts.length - 1].at + 1e-9) return null;
  for (let i = 0; i < pts.length; i++) {
    const b = pts[i];
    if (b.at >= at - 1e-9) {
      const a = pts[Math.max(i - 1, 0)];
      if (b.at === a.at) return b[key] as number;
      const f = (at - a.at) / (b.at - a.at);
      return (a[key] as number) + f * ((b[key] as number) - (a[key] as number));
    }
  }
  return null;
}

export const RETENTION_MARKS: { label: string; seconds: number | "half" | "end" }[] = [
  { label: "0:15", seconds: 15 },
  { label: "0:30", seconds: 30 },
  { label: "1:00", seconds: 60 },
  { label: "2:00", seconds: 120 },
  { label: "Halfway", seconds: "half" },
  { label: "End", seconds: "end" },
];

export function longRetention(points: RetentionPoint[] | undefined, seconds: number): LongRetention | null {
  if (!points?.length || !seconds) return null;
  const marks = RETENTION_MARKS.map((m) => {
    const sec = m.seconds === "half" ? seconds / 2 : m.seconds === "end" ? seconds : m.seconds;
    // The curve's last point is just short of the end (YouTube buckets 0.01-1.0), so "End" reads the last bucket.
    const ratio = m.seconds === "end" ? points[points.length - 1].at : sec / seconds;
    const w = sec > seconds ? null : curveAt(points, ratio);
    return { label: m.label, seconds: Math.round(sec), pct: w == null ? null : Math.round(w * 100) };
  });
  const rel = curveAt(points, Math.min(30 / seconds, 1), "relative");
  return { points: marks, relative30s: rel == null ? null : rel < 0.4 ? "lower" : rel > 0.6 ? "higher" : "typical" };
}

/** YouTube's traffic source codes in plain words. */
export const SOURCE_NAMES: Record<string, string> = {
  SHORTS: "Shorts feed",
  YT_SEARCH: "YouTube search",
  RELATED_VIDEO: "Suggested",
  BROWSE: "Browse / home",
  SUBSCRIBER: "Subscriptions",
  YT_CHANNEL: "Channel page",
  PLAYLIST: "Playlists",
  NOTIFICATION: "Notifications",
  END_SCREEN: "End screens",
  EXT_URL: "Other sites",
  NO_LINK_OTHER: "Direct / unknown",
  YT_OTHER_PAGE: "Other YouTube pages",
  HASHTAGS: "Hashtags",
  SOUND_PAGE: "Sound page",
  ANNOTATION: "Cards",
  CAMPAIGN_CARD: "Campaign cards",
  SHORTS_CONTENT_LINKS: "Related video link (Shorts)",
  VIDEO_REMIXES: "Remixes",
  LIVE_REDIRECT: "Live redirect",
  ADVERTISING: "Ads",
};

export function toSourceViews(t: AnalyticsTable): Record<string, number> {
  const out: Record<string, number> = {};
  for (const r of tableRows(t)) out[String(r.insightTrafficSourceType)] = Number(r.views ?? 0);
  return out;
}

/** Share of views (0-100) from one source, or null when there are no views to share out. */
export function sourceShare(views: Record<string, number> | null | undefined, source: string): number | null {
  if (!views) return null;
  const total = Object.values(views).reduce((a, b) => a + b, 0);
  return total > 0 ? Math.round(((views[source] ?? 0) / total) * 1000) / 10 : null;
}

/** The biggest source by views, in plain words. */
export function topSource(views: Record<string, number> | null | undefined): string | null {
  if (!views) return null;
  const best = Object.entries(views).sort((a, b) => b[1] - a[1])[0];
  return best && best[1] > 0 ? (SOURCE_NAMES[best[0]] ?? best[0]) : null;
}

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
  status?: { privacyStatus?: string; publishAt?: string };
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
    publishAt: item.status?.publishAt ?? null,
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

export type PeriodTotals = { views: number; minutes: number | null; subsNet: number | null };

/** One week (Monday start) or calendar month. `from`/`to` are the days that have data. A period still running, or
 * the launch period, is `partial`; a running period is compared like for like with the same number of days at the
 * start of the previous one (`likeForLike`). `prev` is null when there is no fair comparison. */
export type PeriodRow = PeriodTotals & {
  period: string;
  from: string;
  to: string;
  partial: boolean;
  uploads: number;
  source: "analytics" | "snapshots";
  prev: PeriodTotals | null;
  likeForLike: boolean;
  viewsPct: number | null;
  hoursPct: number | null;
};

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
  /** A Short's Shorts-feed share of views over its first two days (R1: 50% or more means it was fed). */
  feedShareDay1: number | null;
  /** Where the last 28 days of views came from (source code to views), and the biggest one in words. */
  sources28: Record<string, number> | null;
  topSource28: string | null;
  /** Longs only: % still watching at fixed moments, lifetime (null until collected, or when YouTube has too few views). */
  retention: LongRetention | null;
};

/** How many videos the last-24-hours list names before the rest are summed into one row. */
export const TOP_DAY_VIDEOS = 10;

export type DayGainRow = {
  id: string;
  title: string;
  format: "short" | "long";
  url: string;
  /** Views gained in the window, or null when the two snapshots can't be compared for this video. */
  gain: number | null;
  share: number | null;
};

/** Which videos brought in the last 24 hours' views. Every number here comes from the same two snapshots as the
 * tile, so `rows` + `other` + `unaccounted` add up to `total` exactly; nothing is estimated or clamped. */
export type DayGains = {
  /** The tile's figure, which the rows add up to. */
  total: number | null;
  source: "snapshots" | "analytics" | null;
  /** The two snapshots compared (`from` is null when there is no second one). */
  from: string | null;
  to: string;
  rows: DayGainRow[];
  /** Everything outside `rows` that could be compared: mostly videos that gained nothing. */
  other: { videos: number; gain: number; share: number | null } | null;
  /** Public videos the two snapshots can't compare. Counted, never guessed, and left out of the sums. */
  unknown: { videos: number } | null;
  /** The tile's figure less every video's gain: views YouTube counts on the channel but not on a listed video
   * (a video made private or deleted since, or the channel total refreshing ahead of the per-video counts). */
  unaccounted: number | null;
  /** Why there is no list, when there isn't one. */
  note: string | null;
};

export const videoUrl = (v: { id: string; format: "short" | "long" }): string =>
  v.format === "short" ? `https://www.youtube.com/shorts/${v.id}` : `https://www.youtube.com/watch?v=${v.id}`;

/** A gain as a share of the day's total, to one decimal place. Null when there's nothing to share out. */
export function gainShare(gain: number | null, total: number | null): number | null {
  if (gain == null || total == null || total <= 0) return null;
  return Math.round((gain / total) * 1000) / 10;
}

/** The last-24-hours list: the biggest gains first, the rest summed, and whatever the videos don't account for. */
export function dayGains(change: Change, videos: VideoRow[], window: { from: string | null; to: string }): DayGains {
  const base: DayGains = { total: change?.views ?? null, source: change?.source ?? null, ...window, rows: [], other: null, unknown: null, unaccounted: null, note: null };
  if (!change) return { ...base, note: "Which videos brought the views in starts with the second daily snapshot." };
  if (change.source !== "snapshots" || !window.from) {
    return { ...base, note: "This figure comes from YouTube Analytics, which doesn't break the last day down by video. The list returns once there are two daily snapshots." };
  }
  const known = videos.filter((v) => v.d1 != null);
  const movers = known.filter((v) => v.d1 !== 0).sort((a, b) => (b.d1 as number) - (a.d1 as number));
  // The top gains, plus every drop: a video losing views is never hidden inside the remainder row.
  const shown = [...movers.slice(0, TOP_DAY_VIDEOS), ...movers.slice(TOP_DAY_VIDEOS).filter((v) => (v.d1 as number) < 0)];
  const rest = known.filter((v) => !shown.includes(v));
  const total = change.views;
  const restGain = sum(rest.map((v) => v.d1 as number));
  const unknown = videos.length - known.length;
  return {
    ...base,
    total,
    rows: shown.map((v) => ({ id: v.id, title: v.title, format: v.format, url: videoUrl(v), gain: v.d1, share: gainShare(v.d1, total) })),
    other: rest.length ? { videos: rest.length, gain: restGain, share: gainShare(restGain, total) } : null,
    unknown: unknown ? { videos: unknown } : null,
    unaccounted: total - sum(known.map((v) => v.d1 as number)),
  };
}

export type ChannelReport = {
  channel: ChannelKey;
  name: string;
  handle: string;
  date: string;
  firstSnapshot: string;
  analyticsThrough: string | null;
  totals: Snapshot["totals"];
  change: { d1: Change; d7: Change; d30: Change };
  /** Which videos the 'Last 24 hours' tile's views came from. */
  day1: DayGains;
  windowSource: { d7: "snapshots" | "analytics" | null; d30: "snapshots" | "analytics" | null };
  daily: { day: string; views: number; minutes: number | null; subsNet: number | null }[];
  weekly: PeriodRow[];
  monthly: PeriodRow[];
  videos: VideoRow[];
  /** Last 28 days of views by source, summed over Shorts and over longs (null until traffic sources are collected). */
  sourceMix: { short: Record<string, number>; long: Record<string, number> } | null;
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

/** Below these, a percentage change is noise (0.06 h to 0.6 h reads as +900%), so none is shown. */
export const MIN_BASE_VIEWS = 20;
export const MIN_BASE_MINUTES = 30;

type DayPoint = { day: string; views: number; minutes: number | null; subsNet: number | null };

export function pct(now: number | null, before: number | null): number | null {
  if (now == null || before == null || before <= 0) return null;
  return Math.round(((now - before) / before) * 1000) / 10;
}

function addTotals(a: PeriodTotals, d: DayPoint): void {
  a.views += d.views;
  a.minutes = a.minutes == null || d.minutes == null ? null : a.minutes + d.minutes;
  a.subsNet = a.subsNet == null || d.subsNet == null ? null : a.subsNet + d.subsNet;
}

/** Weeks or months from a per-day series, each with its change against the period before. */
export function periods(unit: "week" | "month", series: DayPoint[], uploads: Map<string, number>, source: PeriodRow["source"]): PeriodRow[] {
  const startOf = (day: string) => (unit === "week" ? weekStart(day) : `${day.slice(0, 7)}-01`);
  const endOf = (start: string) => {
    if (unit === "week") return addDays(start, 6);
    const [y, m] = start.split("-").map(Number);
    return new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10);
  };
  const label = (start: string) => (unit === "week" ? start : start.slice(0, 7));
  const days = [...series].sort((a, b) => a.day.localeCompare(b.day));
  const byStart = new Map<string, DayPoint[]>();
  for (const d of days) {
    const k = startOf(d.day);
    if (!byStart.has(k)) byStart.set(k, []);
    byStart.get(k)!.push(d);
  }
  const blank = (): PeriodTotals => ({ views: 0, minutes: source === "analytics" ? 0 : null, subsNet: 0 });
  const rows: PeriodRow[] = [];
  let before: { start: string; total: PeriodTotals; full: boolean; points: DayPoint[] } | null = null;
  for (const [start, points] of [...byStart.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    const total = blank();
    for (const d of points) addTotals(total, d);
    const from = points[0].day;
    const to = points[points.length - 1].day;
    const end = endOf(start);
    const startsOnTime = from === start;
    const full = startsOnTime && to === end;
    let prev: PeriodTotals | null = null;
    let likeForLike = false;
    // Only compare with the period directly before, and only when that one has data from its first day.
    if (before && addDays(endOf(before.start), 1) === start && before.points[0].day === before.start && startsOnTime) {
      if (full && before.full) prev = before.total;
      else if (!full) {
        const n = daysBetween(start, to);
        const cut = addDays(before.start, n);
        const same = before.points.filter((d) => d.day <= cut);
        if (same.length === n + 1) {
          prev = blank();
          for (const d of same) addTotals(prev, d);
          likeForLike = true;
        }
      }
    }
    rows.push({
      period: label(start),
      from,
      to,
      partial: !full,
      uploads: uploads.get(label(start)) ?? 0,
      source,
      ...total,
      prev,
      likeForLike,
      viewsPct: prev && prev.views >= MIN_BASE_VIEWS ? pct(total.views, prev.views) : null,
      hoursPct: prev && (prev.minutes ?? 0) >= MIN_BASE_MINUTES ? pct(total.minutes, prev.minutes) : null,
    });
    before = { start, total, full, points };
  }
  return rows;
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

  // Once per id: snapshots from before 7 Oct can hold a video twice (the uploads playlist repeats some).
  const publicVideos = [...new Map(now.videos.filter((v) => v.privacy === "public").map((v) => [v.id, v])).values()];
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
        feedShareDay1: v.format === "short" ? sourceShare(a?.sources?.[v.id]?.day1, "SHORTS") : null,
        sources28: a?.sources?.[v.id]?.last28 ?? null,
        topSource28: topSource(a?.sources?.[v.id]?.last28),
        retention: v.format === "long" ? longRetention(a?.retention?.[v.id], v.seconds) : null,
      };
    })
    .sort((x, y) => (y.publishedAt ?? "").localeCompare(x.publishedAt ?? ""));

  if (!a) notes.push(now.note ?? "YouTube Analytics isn't connected for this channel yet, so watch time, average % viewed and history before the first snapshot are missing.");
  if (snaps.length < 2) notes.push("Day-on-day growth starts with the second daily snapshot.");
  if (!d7Snap && a) notes.push("7-day video growth comes from YouTube Analytics (it runs about 2 days behind) until there are 7 days of snapshots.");
  if (!d30Snap && a) notes.push("30-day video growth is YouTube Analytics' last 28 days until there are 30 days of snapshots.");
  if (now.totals.subscribers != null) notes.push("YouTube rounds the public subscriber total to 3 significant figures; subscriber gains from YouTube Analytics are exact.");

  // One per-day series for the period tables: YouTube Analytics when connected, else snapshot differences.
  const source: PeriodRow["source"] = daily.length ? "analytics" : "snapshots";
  const series: DayPoint[] = daily.length
    ? daily.map((r) => ({ day: r.day, views: r.views, minutes: r.minutes, subsNet: r.subsGained - r.subsLost }))
    : derived.map((r) => ({ day: r.day, views: r.views, minutes: null, subsNet: r.subsNet }));

  const dailyOut = daily.length
    ? daily.slice(-120).map((r) => ({ day: r.day, views: r.views, minutes: r.minutes, subsNet: r.subsGained - r.subsLost }))
    : derived.slice(-120).map((r) => ({ day: r.day, views: r.views, minutes: null, subsNet: r.subsNet }));

  let sourceMix: ChannelReport["sourceMix"] = null;
  if (a?.sources) {
    sourceMix = { short: {}, long: {} };
    for (const v of videos) {
      for (const [k, n] of Object.entries(v.sources28 ?? {})) {
        const name = SOURCE_NAMES[k] ?? k;
        sourceMix[v.format][name] = (sourceMix[v.format][name] ?? 0) + n;
      }
    }
  }

  const change = {
    d1: channelChange(now, old(t1, 1), daily, 1),
    d7: channelChange(now, d7Snap, daily, 7),
    d30: channelChange(now, d30Snap, daily, 30),
  };

  return {
    channel,
    name: meta.name,
    handle: meta.handle,
    date: now.date,
    firstSnapshot: snaps[0].date,
    analyticsThrough: dailyFile?.through ?? null,
    totals: now.totals,
    change,
    day1: dayGains(change.d1, videos, { from: old(t1, 1)?.date ?? null, to: now.date }),
    windowSource: { d7: d7Snap ? "snapshots" : a ? "analytics" : null, d30: d30Snap ? "snapshots" : a ? "analytics" : null },
    daily: dailyOut,
    weekly: periods("week", series, uploadsBy(weekStart), source).slice(-26),
    monthly: periods("month", series, uploadsBy((d) => d.slice(0, 7)), source),
    videos,
    sourceMix,
    notes,
  };
}

// ----------------------------------------------------------------------------- markdown
const n0 = (x: number | null | undefined) => (x == null ? "–" : Math.round(x).toLocaleString("en-GB"));
const signed = (x: number | null | undefined) => (x == null ? "–" : `${x > 0 ? "+" : ""}${Math.round(x).toLocaleString("en-GB")}`);
const hours = (minutes: number | null | undefined) => (minutes == null ? "–" : (minutes / 60).toLocaleString("en-GB", { maximumFractionDigits: 1 }));
const cell = (s: string) => s.replace(/\|/g, "\\|");

/** 'Top videos, last 24 hours': the same rows the dashboard shows, adding up to the growth table's first row. */
export function renderDayGains(d: DayGains): string[] {
  const L = ["## Top videos, last 24 hours", ""];
  const share = (x: number | null) => (x == null ? "–" : `${x.toFixed(1)}%`);
  if (d.note) return [...L, d.note, ""];
  L.push(`Public view-count change, snapshot ${d.from} to ${d.to}.`, "");
  L.push("| Video | Format | Views | Share |", "|---|---|---:|---:|");
  for (const v of d.rows) L.push(`| [${cell(v.title)}](${v.url}) | ${v.format} | ${signed(v.gain)} | ${share(v.share)} |`);
  if (d.other) L.push(`| Other videos (${d.other.videos}) | | ${signed(d.other.gain)} | ${share(d.other.share)} |`);
  if (d.unknown) L.push(`| Can't be compared (${d.unknown.videos}) | | unknown | – |`);
  if (d.unaccounted) L.push(`| Not matched to a listed video | | ${signed(d.unaccounted)} | ${share(gainShare(d.unaccounted, d.total))} |`);
  L.push(`| **Channel total, last 24 hours** | | **${signed(d.total)}** | **${d.total != null && d.total > 0 ? "100.0%" : "–"}** |`, "");
  if (d.unknown) L.push(`${d.unknown.videos} public video${d.unknown.videos === 1 ? " is" : "s are"} missing from the ${d.from} snapshot, so the change can't be worked out and is left out of the sum.`, "");
  if (d.unaccounted) L.push("YouTube's channel view total and its per-video counts refresh at different times, and a video made private or removed since keeps its views in the channel total. That difference is the unmatched row; nothing here is estimated.", "");
  return L;
}

export function renderMarkdown(r: ChannelReport): string {
  const L: string[] = [];
  L.push(`# ${r.name}: channel tracker`, "");
  L.push(`Generated from the ${r.date} snapshot by \`npm run analytics:report\`. Don't edit by hand.`, "");
  L.push(`**${n0(r.totals.subscribers)} ${r.totals.subscribers === 1 ? "subscriber" : "subscribers"} · ${n0(r.totals.views)} views · ${r.totals.videos} videos**`, "");
  L.push("| Growth | Views | Subscribers |", "|---|---:|---:|");
  for (const [label, c] of [["Last 24 hours", r.change.d1], ["Last 7 days", r.change.d7], ["Last 30 days", r.change.d30]] as const) {
    L.push(`| ${label}${c?.source === "analytics" ? " (YouTube Analytics)" : ""} | ${signed(c?.views)} | ${signed(c?.subscribers)} |`);
  }
  L.push("");
  L.push(...renderDayGains(r.day1));
  const change = (x: number | null) => {
    if (x == null) return "–";
    const v = Math.round(x) || 0; // never "-0%"
    return `${v > 0 ? "+" : ""}${v.toLocaleString("en-GB")}%`;
  };
  const table = (title: string, rows: PeriodRow[], unit: string) => {
    L.push(`## ${title}`, "", `| ${unit} | Views | vs previous | Watch hours | vs previous | Subscribers | Uploads |`, "|---|---:|---:|---:|---:|---:|---:|");
    for (const p of [...rows].reverse()) {
      const name = `${p.period}${p.partial ? (p.likeForLike ? ` (so far, to ${p.to.slice(5)})` : " (part)") : ""}`;
      L.push(`| ${name} | ${n0(p.views)} | ${change(p.viewsPct)} | ${hours(p.minutes)} | ${change(p.hoursPct)} | ${signed(p.subsNet)} | ${p.uploads} |`);
    }
    L.push("");
  };
  table("Week on week (weeks start Monday)", r.weekly.slice(-12), "Week of");
  table("Month on month", r.monthly, "Month");
  L.push(`A period still running is compared with the same number of days at the start of the one before. A part period at launch isn't compared, and no change is shown on a base under ${MIN_BASE_VIEWS} views or ${MIN_BASE_MINUTES} minutes.`, "");
  if (r.sourceMix) {
    const fmtMix = (m: Record<string, number>) => {
      const total = Object.values(m).reduce((x, y) => x + y, 0);
      return total ? Object.entries(m).sort((x, y) => y[1] - x[1]).slice(0, 4).map(([k, n]) => `${k} ${Math.round((n / total) * 100)}%`).join(" · ") + ` (${n0(total)} views)` : "no views";
    };
    L.push("## Where views come from (last 28 days)", "", `- **Shorts:** ${fmtMix(r.sourceMix.short)}`, `- **Longs:** ${fmtMix(r.sourceMix.long)}`, "");
  }
  if (r.videos.some((v) => v.format === "long") && r.videos.some((v) => v.retention)) {
    L.push("## Where viewers leave (longs, lifetime)", "");
    L.push("% of viewers still watching at each point (rewatches can push the start above 100%). The last column compares the first 30 s with videos of similar length on YouTube.", "");
    L.push(`| Long | Views | ${RETENTION_MARKS.map((m) => m.label).join(" | ")} | First 30 s vs similar videos |`);
    L.push(`|---|---:|${RETENTION_MARKS.map(() => "---:").join("|")}|---|`);
    for (const v of r.videos.filter((x) => x.format === "long")) {
      const ret = v.retention;
      const cells = ret ? ret.points.map((p) => (p.pct == null ? "–" : `${p.pct}%`)) : RETENTION_MARKS.map(() => "–");
      const rel = ret ? (ret.relative30s ?? "–") : "too few views";
      L.push(`| [${cell(v.title)}](https://youtu.be/${v.id}) | ${n0(v.views)} | ${cells.join(" | ")} | ${rel} |`);
    }
    L.push("");
  }
  L.push("## Every video (newest first)", "");
  L.push(`| Published | Title | Format | Views | +1 day | +7 days | +30 days | Views/day | Avg % viewed (28 d) | Feed share, day 1 | Top source (28 d) |`);
  L.push("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|");
  for (const v of r.videos) {
    const pct = v.last28?.avgViewPct == null ? "–" : `${v.last28.avgViewPct.toFixed(0)}%`;
    L.push(
      `| ${v.publishedAt?.slice(0, 10) ?? "–"} | [${cell(v.title)}](https://youtu.be/${v.id}) | ${v.format} | ${n0(v.views)} | ${signed(v.d1)} | ${signed(v.d7)} | ${signed(v.d30)} | ${v.perDay ?? "–"} | ${pct} | ${v.feedShareDay1 == null ? "–" : `${v.feedShareDay1.toFixed(0)}%`} | ${v.topSource28 ?? "–"} |`,
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
