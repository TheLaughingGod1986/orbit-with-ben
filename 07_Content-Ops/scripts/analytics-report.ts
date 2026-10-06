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

/** Embed the data in the page. `<` is escaped so a title can never close the script tag. */
export function injectData(template: string, data: unknown): string {
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  if (!template.includes("__TRACKER_DATA__")) throw new Error("template.html has no __TRACKER_DATA__ placeholder");
  return template.replace("__TRACKER_DATA__", () => json);
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
    reports.push(r);
    fs.writeFileSync(path.join(root, key, "REPORT.md"), renderMarkdown(r));
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
