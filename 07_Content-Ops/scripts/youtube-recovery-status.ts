#!/usr/bin/env tsx
/**
 * Non-destructive recovery monitoring.
 *
 *   npm run youtube:recovery-status
 *   npm run youtube:recovery-status -- --checkpoint 72h
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import {
  isRecoveryActive,
  loadYouTubeRecoveryConfig,
  recoveryWindowEnd,
} from "../src/lib/publishing/youtube-recovery";
import { loadCanonicalRegistry } from "../src/lib/publishing/youtube-registry";

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

const CANONICAL = [
  { id: "Mo93x0fxB1Q", type: "longform" as const },
  { id: "1HuV8o3gOss", type: "shorts" as const },
  { id: "KcKBixwmcV4", type: "shorts" as const },
  { id: "3xrxdmaOwJI", type: "longform" as const },
  { id: "JRfhE6yWom4", type: "shorts" as const },
  { id: "L2OFjL4neOo", type: "shorts" as const },
];

async function main() {
  getEnv();
  const checkpoint = arg("checkpoint") || "live";
  const recovery = loadYouTubeRecoveryConfig();
  const registry = loadCanonicalRegistry();
  const active = isRecoveryActive(recovery);

  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) {
    console.error("No YouTube connection");
    process.exit(2);
  }
  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    await adapter.refreshConnection(connection);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  const token = decryptSecret(fresh!.accessTokenEncrypted!);

  const ids = CANONICAL.map((c) => c.id);
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,statistics,contentDetails&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${token}` } },
  );
  const body = await res.json();
  const now = Date.now();

  const assets = (body.items || []).map((it: any) => {
    const meta = CANONICAL.find((c) => c.id === it.id)!;
    const publishedAt = new Date(it.snippet?.publishedAt || 0).getTime();
    const publishAgeHours = publishedAt ? Math.round((now - publishedAt) / 3600000) : null;
    const base = {
      id: it.id,
      type: meta.type,
      title: it.snippet?.title,
      privacy: it.status?.privacyStatus,
      views: it.statistics?.viewCount != null ? Number(it.statistics.viewCount) : null,
      likes: it.statistics?.likeCount != null ? Number(it.statistics.likeCount) : null,
      comments: it.statistics?.commentCount != null ? Number(it.statistics.commentCount) : null,
      publishAgeHours,
      impressions: "MANUAL STUDIO CHECK REQUIRED",
      impressionCtr: "MANUAL STUDIO CHECK REQUIRED",
      averageViewDuration: "MANUAL STUDIO CHECK REQUIRED",
      averagePercentageViewed: "MANUAL STUDIO CHECK REQUIRED",
      trafficSources: "MANUAL STUDIO CHECK REQUIRED",
    };
    if (meta.type === "shorts") {
      return {
        ...base,
        shortsFeedTraffic: "MANUAL STUDIO CHECK REQUIRED",
        shownInFeed: "MANUAL STUDIO CHECK REQUIRED",
        engagedViews: "MANUAL STUDIO CHECK REQUIRED",
        subscribersGained: "MANUAL STUDIO CHECK REQUIRED",
      };
    }
    return base;
  });

  const views = assets.map((a: any) => a.views).filter((v: any) => typeof v === "number") as number[];
  const anyNonZero = views.some((v) => v > 0);
  const bhShorts = assets.filter((a: any) => ["JRfhE6yWom4", "L2OFjL4neOo"].includes(a.id));
  const bhLong = assets.find((a: any) => a.id === "3xrxdmaOwJI");

  const decision = {
    initialSuccessSignals: {
      anyCanonicalViews: anyNonZero,
      bhShortHasViews: bhShorts.some((a: any) => (a.views || 0) > 0),
      bhLongHasViews: (bhLong?.views || 0) > 0,
      note: "Impressions/CTR require Studio or YouTube Analytics API — not inferred as zero.",
    },
    doNotInterveneSolelyBecause: [
      "low views in first 24h",
      "small impressions",
      "CTR unavailable",
      "Shorts distribution delayed",
      "no subscriber conversion yet",
    ],
    escalateWhen: [
      "clean public long remains 0 impressions after 72h (Studio)",
      "two consecutive clean longs get no recommendation testing",
      "Shorts stay at 0 Shorts-feed exposure across several clean uploads",
      "API reports restrictions/processing failures",
      "public shelf changes unexpectedly",
      "duplicate video ID appears",
    ],
    escalateNow: false,
  };

  // Soft escalate flag only if BH long age >= 72h AND views still 0 — impressions still MANUAL
  if (bhLong && (bhLong.publishAgeHours || 0) >= 72 && (bhLong.views || 0) === 0) {
    decision.escalateNow = false; // cannot confirm impressions via Data API
    (decision as any).note72h =
      "BH long is >=72h old with 0 public views — check Studio impressions manually before escalating.";
  }

  const report = {
    checkpoint,
    generatedAt: new Date().toISOString(),
    recovery: {
      active,
      startedAt: recovery.startedAt,
      endsAt: recoveryWindowEnd(recovery).toISOString(),
      maxShortsPerDay: recovery.maxShortsPerDay,
      replacementUploadsAllowed: recovery.replacementUploadsAllowed,
    },
    registryRecordCount: registry.records.length,
    assets,
    decision,
  };

  const outDir = path.resolve(
    process.cwd(),
    "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07",
  );
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `RECOVERY_STATUS_${checkpoint}.json`);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report, null, 2));
  console.error(`Wrote ${outPath}`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
