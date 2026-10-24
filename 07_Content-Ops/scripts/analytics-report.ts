#!/usr/bin/env tsx
/**
 * Builds the channel tracker from the daily snapshots (no network, no tokens).
 *
 *   cd 07_Content-Ops && npm run analytics:report
 *
 * Writes, for each channel with at least one snapshot:
 *   05_Analytics/<channel>/REPORT.md        readable on GitHub
 * and for both channels together:
 *   05_Analytics/dashboard/data.json        what the dashboard shows
 *   05_Analytics/dashboard/dashboard.html   template.html with the data built in (open it in a browser)
 */
import fs from "fs";
import path from "path";
import { ANALYTICS_ROOT } from "./analytics-snapshot";
import { CHANNELS, buildReport, renderMarkdown, type ChannelDaily, type ChannelKey, type ChannelReport, type Snapshot } from "../src/lib/analytics/channel-tracker";

/** Impressions, impressions CTR, views and average % viewed come from a daily read-only Studio read (the Analytics API has no CTR), written to
 *  05_Analytics/<key>/studio_ctr.json by the `studio-ctr-daily` job (Ben, 12 Oct 22:19). Merged onto each video. */
export function mergeStudioCtr(root: string, key: string, r: ChannelReport): void {
  const f = path.join(root, key, "studio_ctr.json");
  if (!fs.existsSync(f)) return;
  try {
    const s = JSON.parse(fs.readFileSync(f, "utf8")) as { readAt?: string; videos?: Record<string, { impressions?: number; impressionsCtr?: number; views?: number; avgViewPct?: number; avgViewSeconds?: number; stayedToWatch?: number }> };
    for (const v of r.videos as Array<ChannelReport["videos"][number] & { impressions?: number; impressionsCtr?: number; ctrReadAt?: string; studioViews?: number; studioAvgViewPct?: number; studioAvgViewSeconds?: number; studioStayedPct?: number }>) {
      const m = s.videos?.[v.id];
      if (!m) continue;
      // Studio is live; the Analytics API lags 2-3 days (Saturn 021 read 99.7% from 1 view when Studio had 63 views
      // at 6.8%, Ben 12 Oct 22:33). Studio's views and average % viewed take priority on the tracker.
      if (typeof m.views === "number") v.studioViews = m.views;
      if (typeof m.avgViewPct === "number") v.studioAvgViewPct = m.avgViewPct;
      if (typeof m.avgViewSeconds === "number") v.studioAvgViewSeconds = m.avgViewSeconds;
      if (typeof m.impressionsCtr === "number") v.impressionsCtr = m.impressionsCtr;
      if (typeof m.stayedToWatch === "number") v.studioStayedPct = m.stayedToWatch;   // Shorts: "Stayed to watch" %
      if (typeof m.impressions === "number") v.impressions = m.impressions;
      if (s.readAt) v.ctrReadAt = s.readAt;
    }
  } catch {
    /* a broken sidecar never breaks the report */
  }
}

/** Ben's Shorts target (24 Oct 2026): Studio "Stayed to watch" 60% or more at the 48 h read, on both channels.
 *  Rules for hitting it: .cursor/rules/orbit-build-shorts.mdc -> "60% stayed-to-watch". */
export const STAYED_TARGET = 60;
export const STAYED_WATCH = 45;
export const STAYED_MIN_VIEWS = 100;

type StayedRow = ChannelReport["videos"][number] & { studioStayedPct?: number; studioViews?: number };

/** The verdict for one Short's Studio read: too few views to judge, PASS (>= 60%), WATCH (45-59.9%) or MISS (< 45%). */
export function stayedVerdict(stayed: number, views: number | undefined): string {
  if ((views ?? 0) < STAYED_MIN_VIEWS) return "too few to judge";
  if (stayed >= STAYED_TARGET) return "PASS";
  return stayed >= STAYED_WATCH ? "WATCH" : "MISS";
}

/** Every Short aired in the last `days` days that has a Studio stayed-to-watch read, checked against the 60% target. */
export function renderStayedCheck(r: ChannelReport, now = Date.now(), days = 14): string {
  const rows = (r.videos as StayedRow[])
    .filter((v) => v.format === "short" && typeof v.studioStayedPct === "number" && v.publishedAt)
    .map((v) => ({ v, ageH: (now - Date.parse(v.publishedAt!)) / 3_600_000 }))
    .filter(({ ageH }) => ageH >= 0 && ageH <= days * 24)
    .sort((a, b) => a.ageH - b.ageH);
  const lines = [
    "",
    `## Shorts: stayed-to-watch vs the ${STAYED_TARGET}% target`,
    "",
    `Studio "Stayed to watch" for Shorts aired in the last ${days} days. PASS ${STAYED_TARGET}%+, WATCH ${STAYED_WATCH}-${STAYED_TARGET}%, MISS under ${STAYED_WATCH}%; under ${STAYED_MIN_VIEWS} Studio views is too few to judge. Reads before 48 h are early. Rules: .cursor/rules/orbit-build-shorts.mdc -> "60% stayed-to-watch".`,
    "",
  ];
  if (!rows.length) return [...lines, "No Short aired in this window has a Studio read yet.", ""].join("\n");
  lines.push("| Short | Age | Studio views | Stayed | Verdict |", "|---|---:|---:|---:|---|");
  let pass = 0, judged = 0;
  for (const { v, ageH } of rows) {
    const verdict = stayedVerdict(v.studioStayedPct!, v.studioViews ?? v.views);
    if (verdict !== "too few to judge") { judged++; if (verdict === "PASS") pass++; }
    const age = ageH < 48 ? `${Math.round(ageH)} h (early)` : `${Math.floor(ageH / 24)} d`;
    lines.push(`| [${v.title.replace(/\|/g, "/")}](https://youtu.be/${v.id}) | ${age} | ${v.studioViews ?? v.views} | ${v.studioStayedPct!.toFixed(1)}% | ${verdict} |`);
  }
  lines.push("", `${pass} of ${judged} judged Shorts at ${STAYED_TARGET}%+.`, "");
  return lines.join("\n");
}

/** Embed the data in the page. `<` is escaped so a title can never close the script tag. */
export function injectData(template: string, data: unknown): string {
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  if (!template.includes("__TRACKER_DATA__")) throw new Error("template.html has no __TRACKER_DATA__ placeholder");
  return template.replace("__TRACKER_DATA__", () => json);
}

/** Apply a dated public-catalog repair without rewriting raw historical snapshots. */
export function mergeCatalogRecovery(root: string, key: ChannelKey, snaps: Snapshot[]): void {
  const file = path.join(root, key, "catalog_recovery.json");
  if (!snaps.length || !fs.existsSync(file)) return;
  const doc = JSON.parse(fs.readFileSync(file, "utf8")) as { channelId: string; observedAt: string; source: string; videos: Snapshot["videos"] };
  const latest = snaps[snaps.length - 1], observed = Date.parse(doc.observedAt), taken = Date.parse(latest.takenAt);
  if (doc.channelId !== CHANNELS[key].id || !Array.isArray(doc.videos) || !Number.isFinite(observed) || observed < taken || observed-taken > 86400000) return;
  const known = new Set(latest.videos.map(v=>v.id));
  const added = doc.videos.filter(v=>v.privacy === "public" && /^[A-Za-z0-9_-]{11}$/.test(v.id) && !known.has(v.id) && (known.add(v.id), true));
  if (added.length) {
    latest.videos = latest.videos.concat(added);
    latest.catalogRecovery = { observedAt: doc.observedAt, source: doc.source, addedIds: added.map(v=>v.id) };
  }
}

export function loadChannel(root: string, key: ChannelKey): { snaps: Snapshot[]; daily: ChannelDaily | null } {
  const dir = path.join(root, key, "snapshots");
  const snaps = fs.existsSync(dir)
    ? fs
        .readdirSync(dir)
        .filter((f) => /^\d{4}-\d{2}-\d{2}\.json$/.test(f))
        .sort()
        .map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")) as Snapshot)
    : [];
  mergeCatalogRecovery(root, key, snaps);
  const dailyPath = path.join(root, key, "channel_daily.json");
  const daily = fs.existsSync(dailyPath) ? (JSON.parse(fs.readFileSync(dailyPath, "utf8")) as ChannelDaily) : null;
  return { snaps, daily };
}

export function run(root = ANALYTICS_ROOT): string[] {
  const out: string[] = [];
  const reports: ChannelReport[] = [];
  for (const key of Object.keys(CHANNELS) as ChannelKey[]) {
    const { snaps, daily } = loadChannel(root, key);
    if (!snaps.length) {
      out.push(`${key}: no snapshots yet`);
      continue;
    }
    const r = buildReport(key, snaps, daily);
    mergeStudioCtr(root, key, r);
    reports.push(r);
    fs.writeFileSync(path.join(root, key, "REPORT.md"), renderMarkdown(r) + renderStayedCheck(r));
    out.push(`${key}: REPORT.md from ${snaps.length} snapshot(s), latest ${r.date}`);
  }
  if (!reports.length) return out;
  const dash = path.join(root, "dashboard");
  fs.mkdirSync(dash, { recursive: true });
  const data = { generatedAt: new Date().toISOString(), channels: reports };
  fs.writeFileSync(path.join(dash, "data.json"), JSON.stringify(data) + "\n");
  const template = path.join(dash, "template.html");
  if (fs.existsSync(template)) {
    fs.writeFileSync(path.join(dash, "dashboard.html"), injectData(fs.readFileSync(template, "utf8"), data));
    out.push("dashboard.html rebuilt");
  }
  return out;
}

if (require.main === module) {
  try {
    for (const line of run()) console.log(line);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
