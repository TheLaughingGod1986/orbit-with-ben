#!/usr/bin/env tsx
/**
 * READ-ONLY: per-video impressions + impressions CTR (packaging signal).
 *
 *   npx tsx scripts/_impressions_ctr_2026-08-25.ts
 */
import fs from "fs";
import path from "path";

function loadDotEnv(file: string) {
  if (!fs.existsSync(file)) return;
  for (const raw of fs.readFileSync(file, "utf8").split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const eq = line.indexOf("=");
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let val = line.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (process.env[key] == null) process.env[key] = val;
  }
  if (!process.env.DIRECT_URL && process.env.DATABASE_URL) {
    process.env.DIRECT_URL = process.env.DATABASE_URL;
  }
}
loadDotEnv(path.resolve(process.cwd(), ".env"));

import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

const OUT = path.resolve(
  __dirname,
  "../../00_Brand/Channel-Setup/audits/channel_review_2026-08-24/IMPRESSIONS_CTR.json",
);
const STATS = path.resolve(
  __dirname,
  "../../00_Brand/Channel-Setup/audits/channel_review_2026-08-24/CHANNEL_STATS.json",
);
const START = "2026-07-25";
const END = "2026-08-25";

async function token() {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) throw new Error("no token");
  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60000
  ) {
    await adapter.refreshConnection!(connection);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  return decryptSecret(fresh!.accessTokenEncrypted!);
}

async function query(t: string, params: Record<string, string>) {
  const qs = new URLSearchParams({
    ids: "channel==MINE",
    startDate: START,
    endDate: END,
    ...params,
  });
  const res = await fetch(`https://youtubeanalytics.googleapis.com/v2/reports?${qs}`, {
    headers: { Authorization: `Bearer ${t}` },
  });
  const body = await res.json();
  if (!res.ok) return { error: body?.error?.message || JSON.stringify(body).slice(0, 200) };
  return body;
}

async function main() {
  const t = await token();
  const titles: Record<string, { title: string; kind: string; views: number }> = {};
  if (fs.existsSync(STATS)) {
    const stats = JSON.parse(fs.readFileSync(STATS, "utf8"));
    for (const v of stats.videos || []) {
      titles[v.id] = { title: v.title, kind: v.kind, views: v.views };
    }
  }

  const channel = await query(t, {
    metrics: "videoThumbnailImpressions,videoThumbnailImpressionsClickRate",
  });
  const perVideo = await query(t, {
    dimensions: "video",
    metrics: "videoThumbnailImpressions,videoThumbnailImpressionsClickRate",
    sort: "-videoThumbnailImpressions",
    maxResults: "50",
  });

  const rows: any[] = [];
  if (perVideo.rows) {
    for (const r of perVideo.rows) {
      const [id, impressions, ctr] = r;
      rows.push({
        id,
        title: titles[id]?.title || "?",
        kind: titles[id]?.kind || "?",
        impressions,
        ctrPct: Number(ctr.toFixed(2)),
        views: titles[id]?.views ?? null,
      });
    }
  }

  const out = { ranAt: new Date().toISOString(), window: `${START}..${END}`, channel, rows };
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2));

  console.log("channel:", JSON.stringify(channel.rows?.[0] || channel.error));
  console.log("\nvideo | kind | impressions | CTR% | views | title");
  for (const r of rows) {
    console.log(
      `${r.id} | ${r.kind} | ${String(r.impressions).padStart(5)} | ${String(r.ctrPct).padStart(5)} | ${String(r.views ?? "?").padStart(4)} | ${r.title.slice(0, 55)}`,
    );
  }
  console.log(`\nwritten=${OUT}`);
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
