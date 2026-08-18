import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import {
  DEFAULT_MAPPINGS,
  parseMetricsCsv,
  previewCsv,
  withEngagement,
} from "@/lib/analytics/csv-import";
import { generateInsights } from "@/lib/analytics/insights";
import { requireOperatorApi } from "@/lib/security/operator-auth";

export async function POST(req: Request) {
  const denied = await requireOperatorApi();
  if (denied) return denied;

  const body = await req.json();
  const platformKey = String(body.platform || "youtube") as keyof typeof DEFAULT_MAPPINGS;
  const mapping = {
    ...DEFAULT_MAPPINGS[platformKey],
    ...(body.mapping || {}),
  };
  const csv = String(body.csv || "");
  if (!csv.trim()) {
    return NextResponse.json({ error: "CSV text is required" }, { status: 400 });
  }

  const preview = previewCsv(csv, mapping);
  if (body.dryRun) {
    return NextResponse.json({ preview });
  }

  const parsed = parseMetricsCsv(csv, mapping);
  let successCount = 0;
  const errors = [...parsed.errors];

  for (const row of parsed.rows) {
    try {
      const post = await prisma.platformPost.findFirst({
        where: {
          OR: [
            row.platformPostId ? { platformPostId: row.platformPostId } : undefined,
            row.platformUrl ? { platformUrl: row.platformUrl } : undefined,
          ].filter(Boolean) as { platformPostId?: string; platformUrl?: string }[],
        },
      });
      if (!post) {
        errors.push(`No PlatformPost match for ${row.platformUrl || row.platformPostId}`);
        continue;
      }
      const enriched = withEngagement(row);
      await prisma.performanceMetric.create({
        data: {
          platformPostId: post.id,
          views: enriched.views,
          impressions: enriched.impressions,
          likes: enriched.likes,
          comments: enriched.comments,
          shares: enriched.shares,
          saves: enriched.saves,
          averageWatchTime: enriched.averageWatchTime,
          averagePercentageViewed: enriched.averagePercentageViewed,
          completionRate: enriched.completionRate,
          profileVisits: enriched.profileVisits,
          linkClicks: enriched.linkClicks,
          subscribersGained: enriched.subscribersGained,
          followersGained: enriched.followersGained,
          engagementRate: enriched.engagementRate,
          clickThroughRate: enriched.clickThroughRate,
          retention30s: enriched.retention30s,
          retentionDropAtSeconds: enriched.retentionDropAtSeconds,
          retentionDropDepth: enriched.retentionDropDepth,
          returningViewers: enriched.returningViewers,
          newViewers: enriched.newViewers,
          browsePercent: enriched.browsePercent,
          suggestedPercent: enriched.suggestedPercent,
          searchPercent: enriched.searchPercent,
          endScreenCtr: enriched.endScreenCtr,
          cardsCtr: enriched.cardsCtr,
          averageSessionSeconds: enriched.averageSessionSeconds,
          importSource: platformKey,
          importBatchId: body.batchId || new Date().toISOString(),
        },
      });
      successCount += 1;
    } catch (err) {
      errors.push(err instanceof Error ? err.message : "Import row failed");
    }
  }

  await prisma.analyticsImport.create({
    data: {
      platform: platformKey,
      filename: body.filename || "paste.csv",
      rowCount: parsed.rows.length,
      successCount,
      errorCount: errors.length,
      errorsJson: JSON.stringify(errors.slice(0, 50)),
    },
  });

  // Refresh insights from all metrics
  const posts = await prisma.platformPost.findMany({
    include: {
      metrics: { orderBy: { recordedAt: "desc" }, take: 1 },
      shortClip: { include: { longFormVideo: true } },
    },
  });
  const insightRows = posts
    .filter((p) => p.metrics[0])
    .map((p) => ({
      platform: p.platform,
      topic: p.shortClip.longFormVideo.topic,
      hookCategory: p.shortClip.hookCategory,
      durationSeconds: p.shortClip.targetDurationSeconds,
      scheduledHour: p.scheduledAt?.getHours() ?? null,
      metrics: p.metrics[0],
    }));
  const { insights, lowDataMessage } = generateInsights(insightRows);
  await prisma.contentInsight.deleteMany({ where: { type: { not: "system" } } });
  for (const insight of insights) {
    await prisma.contentInsight.create({
      data: {
        type: insight.type,
        topic: insight.topic,
        platform: insight.platform,
        finding: insight.finding,
        evidence: insight.evidence,
        confidence: insight.confidence,
        recommendedAction: insight.recommendedAction,
        sampleSize: insight.sampleSize,
      },
    });
  }
  if (lowDataMessage) {
    await prisma.contentInsight.create({
      data: {
        type: "low_data",
        finding: lowDataMessage,
        evidence: `Metric-bearing posts: ${insightRows.length}`,
        confidence: 0,
        recommendedAction: "Keep importing weekly analytics.",
        sampleSize: insightRows.length,
      },
    });
  }

  return NextResponse.json({
    rowCount: parsed.rows.length,
    successCount,
    duplicatesSkipped: parsed.duplicatesSkipped,
    errors,
    preview,
  });
}
