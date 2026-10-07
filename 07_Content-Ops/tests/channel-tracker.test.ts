import { describe, expect, it } from "vitest";
import fs from "fs";
import os from "os";
import path from "path";
import {
  addDays,
  buildReport,
  periods,
  londonDate,
  renderMarkdown,
  snapshotAtOrBefore,
  toDailyRows,
  toVideoStat,
  toVideoWindows,
  weekStart,
  type ChannelDaily,
  type Snapshot,
  type VideoStat,
} from "@/lib/analytics/channel-tracker";
import { serialiseSnapshot } from "../scripts/analytics-snapshot";
import { injectData, run } from "../scripts/analytics-report";
import { authTarget } from "../scripts/youtube-auth";

const video = (id: string, views: number, publishedAt = "2026-09-01T10:30:00Z", format: "short" | "long" = "short"): VideoStat => ({
  id,
  title: `Video ${id}`,
  publishedAt,
  seconds: format === "short" ? 25 : 480,
  format,
  privacy: "public",
  views,
  likes: 0,
  comments: 0,
});

const snap = (date: string, views: number, subs: number, videos: VideoStat[], analytics: Snapshot["analytics"] = null): Snapshot => ({
  channel: "owb",
  channelId: "UC_esArsDKd3GJvOkeO0DUog",
  date,
  takenAt: `${date}T05:40:00Z`,
  totals: { subscribers: subs, views, videos: videos.length },
  videos,
  analytics,
});

describe("dates", () => {
  it("uses the London calendar date, including across midnight in summer time", () => {
    expect(londonDate(new Date("2026-10-05T23:30:00Z"))).toBe("2026-10-06");
    expect(londonDate(new Date("2026-12-05T23:30:00Z"))).toBe("2026-12-05");
  });
  it("finds the Monday of the week and steps days across month ends", () => {
    expect(weekStart("2026-10-06")).toBe("2026-10-05"); // Tuesday
    expect(weekStart("2026-10-11")).toBe("2026-10-05"); // Sunday
    expect(weekStart("2026-10-05")).toBe("2026-10-05"); // Monday
    expect(addDays("2026-10-01", -1)).toBe("2026-09-30");
  });
});

describe("API parsing", () => {
  it("tells Shorts from longs by length and reads the counts", () => {
    const s = toVideoStat({ id: "a", snippet: { title: "T", publishedAt: "2026-10-05T10:30:00Z" }, contentDetails: { duration: "PT26S" }, statistics: { viewCount: "88", likeCount: "3" }, status: { privacyStatus: "public" } });
    expect(s).toMatchObject({ format: "short", views: 88, likes: 3, comments: 0, privacy: "public", seconds: 26 });
    expect(toVideoStat({ id: "b", contentDetails: { duration: "PT7M41S" } }).format).toBe("long");
  });
  it("reads YouTube Analytics tables by column name", () => {
    const daily = toDailyRows({
      columnHeaders: [{ name: "day" }, { name: "views" }, { name: "estimatedMinutesWatched" }, { name: "subscribersGained" }, { name: "subscribersLost" }],
      rows: [["2026-10-01", 120, 300, 4, 1]],
    });
    expect(daily[0]).toEqual({ day: "2026-10-01", views: 120, minutes: 300, subsGained: 4, subsLost: 1, likes: 0, comments: 0, shares: 0 });
    const w = toVideoWindows({
      columnHeaders: [{ name: "video" }, { name: "views" }, { name: "estimatedMinutesWatched" }, { name: "subscribersGained" }, { name: "averageViewDuration" }, { name: "averageViewPercentage" }],
      rows: [["abc", 50, 20, 1, 18, 72.5]],
    });
    expect(w.abc).toEqual({ views: 50, minutes: 20, subs: 1, avgViewSeconds: 18, avgViewPct: 72.5 });
  });
});

describe("buildReport from snapshots only", () => {
  const snaps = [
    snap("2026-10-04", 1000, 100, [video("a", 600), video("b", 400)]),
    snap("2026-10-05", 1100, 102, [video("a", 650), video("b", 420), video("c", 30, "2026-10-05T10:30:00Z")]),
  ];
  const r = buildReport("owb", snaps, null);

  it("gives day-on-day growth for the channel and each video", () => {
    expect(r.change.d1).toEqual({ views: 100, subscribers: 2, source: "snapshots" });
    expect(r.videos.find((v) => v.id === "a")!.d1).toBe(50);
  });
  it("counts all views of a video published after the earlier snapshot", () => {
    expect(r.videos.find((v) => v.id === "c")!.d1).toBe(30);
  });
  it("leaves 7 and 30 days empty until those snapshots exist, and says why", () => {
    expect(r.change.d7).toBeNull();
    expect(r.videos[0].d7).toBeNull();
    expect(r.windowSource.d7).toBeNull();
    expect(r.notes.join(" ")).toMatch(/isn't connected/);
  });
  it("lists the newest video first and skips private ones", () => {
    const withPrivate = [...snaps];
    withPrivate[1] = { ...snaps[1], videos: [...snaps[1].videos, { ...video("p", 0, "2026-10-09T10:30:00Z"), privacy: "private" }] };
    const r2 = buildReport("owb", withPrivate, null);
    expect(r2.videos.map((v) => v.id)).toEqual(["c", "a", "b"]);
  });
  it("lists a video once even if the snapshot holds it twice", () => {
    const dup = [...snaps];
    dup[1] = { ...snaps[1], videos: [...snaps[1].videos, video("a", 650)] };
    expect(buildReport("owb", dup, null).videos.filter((v) => v.id === "a")).toHaveLength(1);
  });
  it("finds the snapshot on or before a day", () => {
    expect(snapshotAtOrBefore(snaps, "2026-10-04")!.date).toBe("2026-10-04");
    expect(snapshotAtOrBefore(snaps, "2026-10-03")).toBeNull();
  });
});

describe("buildReport with YouTube Analytics", () => {
  const rows = Array.from({ length: 40 }, (_, i) => {
    const day = addDays("2026-08-25", i);
    return { day, views: 10, minutes: 6, subsGained: 2, subsLost: 1, likes: 0, comments: 0, shares: 0 };
  });
  const daily: ChannelDaily = { channel: "owb", through: rows[rows.length - 1].day, rows };
  const w = (views: number) => ({ views, minutes: 1, subs: 0, avgViewSeconds: 15, avgViewPct: 60 });
  const analytics = { through: daily.through, last7: { a: w(70) }, last28: { a: w(280) }, lifetime: { a: w(600) } };
  const r = buildReport("owb", [snap("2026-10-05", 1100, 102, [video("a", 650), video("b", 420)], analytics)], daily);

  it("falls back to Analytics for 7 and 28 days before the snapshots are old enough", () => {
    expect(r.windowSource).toEqual({ d7: "analytics", d30: "analytics" });
    expect(r.videos.find((v) => v.id === "a")).toMatchObject({ d7: 70, d30: 280 });
    expect(r.videos.find((v) => v.id === "b")).toMatchObject({ d7: 0, d30: 0 }); // no views in the window
    expect(r.change.d7).toEqual({ views: 70, subscribers: 7, source: "analytics" });
  });
  it("sums weeks from Monday and months by calendar month, with watch hours and uploads", () => {
    const sep = r.monthly.find((m) => m.period === "2026-09")!;
    expect(sep).toMatchObject({ views: 300, minutes: 180, subsNet: 30, uploads: 2, source: "analytics" });
    const wk = r.weekly.find((p) => p.period === "2026-09-28")!;
    expect(wk.views).toBe(60); // Mon 28 Sep to Sat 3 Oct: the rows end on the 3rd
  });
  it("renders a markdown report with every video linked", () => {
    const md = renderMarkdown(r);
    expect(md).toContain("[Video a](https://youtu.be/a)");
    expect(md).toContain("| Last 7 days (YouTube Analytics) | +70 | +7 |");
    expect(md).toContain("60%");
  });
});

describe("week on week and month on month", () => {
  const day = (d: string, views: number, minutes = 60) => ({ day: d, views, minutes, subsNet: 1 });
  const run = (from: string, n: number, views: (i: number) => number) => Array.from({ length: n }, (_, i) => day(addDays(from, i), views(i)));

  it("compares each full week with the week before", () => {
    const series = [...run("2026-09-21", 7, () => 10), ...run("2026-09-28", 7, () => 15)];
    const w = periods("week", series, new Map(), "analytics");
    expect(w.map((r) => [r.period, r.views, r.viewsPct, r.partial])).toEqual([
      ["2026-09-21", 70, null, false],
      ["2026-09-28", 105, 50, false],
    ]);
  });
  it("compares a month still running with the same days of the month before", () => {
    const series = [...run("2026-09-01", 30, (i) => (i < 4 ? 50 : 1)), ...run("2026-10-01", 4, () => 25)];
    const m = periods("month", series, new Map(), "analytics");
    const oct = m.find((r) => r.period === "2026-10")!;
    expect(oct).toMatchObject({ partial: true, likeForLike: true, views: 100, viewsPct: -50 });
    expect(oct.prev!.views).toBe(200);
  });
  it("doesn't compare with a launch part-period, or on a tiny base", () => {
    const series = [...run("2026-07-27", 5, () => 1), ...run("2026-08-01", 31, () => 3)];
    const m = periods("month", series, new Map(), "analytics");
    expect(m[0]).toMatchObject({ period: "2026-07", partial: true, prev: null });
    expect(m[1]).toMatchObject({ period: "2026-08", prev: null, viewsPct: null });
    const tiny = periods("week", [...run("2026-09-21", 7, () => 2), ...run("2026-09-28", 7, () => 20)], new Map(), "analytics");
    expect(tiny[1].viewsPct).toBeNull(); // 14 views before: under the 20-view floor
  });
});

describe("files", () => {
  it("serialises a snapshot one video per line and round-trips titles with $ signs", () => {
    const s = snap("2026-10-05", 1, 1, [{ ...video("a", 5), title: "The $& Trick | $1" }, video("b", 6)]);
    const text = serialiseSnapshot(s);
    expect(JSON.parse(text)).toEqual(s);
    expect(text.split("\n").filter((l) => l.startsWith('{"id"')).length).toBe(2);
  });
  it("embeds the data without letting a title close the script tag", () => {
    const html = injectData("<script>const D = __TRACKER_DATA__;</script>", { t: "</script><b>$&" });
    expect(html).not.toContain("</script><b>");
    expect(html).toContain("$&");
  });
  it("builds REPORT.md and the dashboard from a folder of snapshots", () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "tracker-"));
    fs.mkdirSync(path.join(root, "owb", "snapshots"), { recursive: true });
    fs.mkdirSync(path.join(root, "dashboard"), { recursive: true });
    fs.writeFileSync(path.join(root, "owb", "snapshots", "2026-10-05.json"), serialiseSnapshot(snap("2026-10-05", 10, 1, [video("a", 10)])));
    fs.writeFileSync(path.join(root, "dashboard", "template.html"), "<script>window.D=__TRACKER_DATA__</script>");
    const log = run(root);
    expect(log).toContain("hos: no snapshots yet");
    expect(fs.readFileSync(path.join(root, "owb", "REPORT.md"), "utf8")).toContain("Orbit With Ben");
    expect(fs.readFileSync(path.join(root, "dashboard", "dashboard.html"), "utf8")).toContain('"channel":"owb"');
  });
});

describe("sign-in target", () => {
  it("keeps the upload login by default and asks read-only scopes for the tracker", () => {
    expect(authTarget([]).envKey).toBe("YOUTUBE_REFRESH_TOKEN");
    const t = authTarget(["--analytics", "hos"]);
    expect(t).toMatchObject({ envKey: "YT_ANALYTICS_REFRESH_TOKEN_HOS", channelId: "UCXp7HkBIl1LgaznXuZHJyRg" });
    expect(t.scopes).toEqual(["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"]);
    expect(() => authTarget(["--analytics", "x"])).toThrow();
  });
});
