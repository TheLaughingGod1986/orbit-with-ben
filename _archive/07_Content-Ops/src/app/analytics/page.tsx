import { prisma } from "@/lib/storage/prisma";
import { engagementRate, generateInsights, perThousand } from "@/lib/analytics/insights";
import {
  computeCtr,
  diagnoseCatalog,
  summarizeGrowthDashboard,
  type YouTubeGrowthMetrics,
} from "@/lib/analytics/youtube-growth";
import { AnalyticsImportForm } from "@/components/AnalyticsImportForm";
import { PLATFORMS } from "@/config/platforms";
import { isOperatorAuthenticated } from "@/lib/security/operator-auth";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  const canWrite = await isOperatorAuthenticated();
  const posts = await prisma.platformPost.findMany({
    include: {
      metrics: { orderBy: { recordedAt: "desc" }, take: 1 },
      shortClip: { include: { longFormVideo: true } },
    },
  });

  const rows = posts
    .filter((p) => p.metrics[0])
    .map((p) => {
      const m = p.metrics[0];
      return {
        platform: p.platform,
        topic: p.shortClip.longFormVideo.topic,
        hookCategory: p.shortClip.hookCategory,
        durationSeconds: p.shortClip.targetDurationSeconds,
        scheduledHour: p.scheduledAt ? p.scheduledAt.getHours() : null,
        scheduledDay: p.scheduledAt
          ? p.scheduledAt.toLocaleDateString("en-GB", { weekday: "long", timeZone: "Europe/London" })
          : null,
        metrics: m,
        title: p.shortClip.workingTitle,
        isShort: p.platform === "youtube_shorts" || p.platform === "youtube",
      };
    });

  const { insights, lowDataMessage } = generateInsights(
    rows.map((r) => ({
      platform: r.platform,
      topic: r.topic,
      hookCategory: r.hookCategory,
      durationSeconds: r.durationSeconds,
      scheduledHour: r.scheduledHour,
      scheduledDay: r.scheduledDay,
      metrics: r.metrics,
    })),
  );

  const growthRows: YouTubeGrowthMetrics[] = rows
    .filter((r) => r.platform === "youtube" || r.platform === "youtube_shorts")
    .map((r) => {
      const m = r.metrics;
      return {
        title: r.title,
        topic: r.topic,
        hookCategory: r.hookCategory,
        isShort: r.platform === "youtube_shorts",
        durationSeconds: r.durationSeconds,
        views: m.views,
        impressions: m.impressions,
        ctr: m.clickThroughRate ?? computeCtr(m.impressions, m.views),
        averageViewDurationSeconds: m.averageWatchTime,
        averagePercentageViewed: m.averagePercentageViewed,
        retention30s: m.retention30s,
        retentionDropAtSeconds: m.retentionDropAtSeconds,
        retentionDropDepth: m.retentionDropDepth,
        returningViewers: m.returningViewers,
        newViewers: m.newViewers,
        subscribersGained: m.subscribersGained,
        browsePercent: m.browsePercent,
        suggestedPercent: m.suggestedPercent,
        searchPercent: m.searchPercent,
        endScreenCtr: m.endScreenCtr,
        cardsCtr: m.cardsCtr,
        averageSessionSeconds: m.averageSessionSeconds,
      };
    });

  const growthSummary = summarizeGrowthDashboard(growthRows);
  const { recommendations: growthRecs, leaders } = diagnoseCatalog(growthRows);

  const byPlatform = Object.keys(PLATFORMS).map((platform) => {
    const list = rows.filter((r) => r.platform === platform);
    const views = list.reduce((s, r) => s + (r.metrics.views ?? 0), 0);
    const eng = list
      .map((r) => engagementRate(r.metrics))
      .filter((n): n is number => n != null);
    const avgEng = eng.length ? eng.reduce((a, b) => a + b, 0) / eng.length : null;
    const subs = list.reduce((s, r) => s + (r.metrics.subscribersGained ?? 0), 0);
    return { platform, views, avgEng, subs, n: list.length };
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">Performance</h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Growth System v2 — impressions, CTR, AVD, APV, traffic mix, and post-upload recommendations.
        </p>
      </div>

      {canWrite ? (
        <AnalyticsImportForm />
      ) : (
        <div className="card-panel space-y-3 p-5">
          <p className="text-sm text-[#F5E8D2]/65">
            Metrics import is operator-only. Sign in to upload CSV performance data.
          </p>
          <Link
            href="/login?next=/analytics"
            className="inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#FF7A24]"
          >
            Operator sign-in
          </Link>
        </div>
      )}

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card-panel p-4">
          <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Impressions</div>
          <div className="mt-3 text-2xl">{growthSummary.impressions || "—"}</div>
        </div>
        <div className="card-panel p-4">
          <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Avg CTR</div>
          <div className="mt-3 text-2xl">
            {growthSummary.avgCtr != null ? `${growthSummary.avgCtr.toFixed(2)}%` : "—"}
          </div>
        </div>
        <div className="card-panel p-4">
          <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Avg APV</div>
          <div className="mt-3 text-2xl">
            {growthSummary.avgApv != null ? `${growthSummary.avgApv.toFixed(1)}%` : "—"}
          </div>
        </div>
        <div className="card-panel p-4">
          <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Subs gained</div>
          <div className="mt-3 text-2xl">{growthSummary.subscribersGained || "—"}</div>
        </div>
      </section>

      <section className="card-panel p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">
          YouTube growth recommendations
        </h2>
        <p className="mt-2 text-sm text-[#F5E8D2]/55">
          Auto-flags weak openings, retention drops, poor titles/thumbnails, runtime, funnel gaps.
        </p>
        {!growthRecs.length ? (
          <p className="mt-4 rounded-xl border border-[#FFC85A]/30 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#FFC85A]">
            Import YouTube metrics (impressions, CTR, retention, traffic %) to generate recommendations.
          </p>
        ) : (
          <ul className="mt-4 space-y-3">
            {growthRecs.slice(0, 12).map((rec) => (
              <li key={`${rec.category}-${rec.finding}`} className="rounded-xl bg-white/3 p-4 text-sm">
                <div className="text-xs uppercase tracking-[0.12em] text-[#FF7A24]">{rec.category}</div>
                <div className="mt-1 text-[#F5E8D2]">{rec.finding}</div>
                <div className="mt-1 text-[#F5E8D2]/50">{rec.evidence}</div>
                <div className="mt-2 text-[#FF7A24]">{rec.recommendedAction}</div>
              </li>
            ))}
          </ul>
        )}
        {(leaders.topHooks.length > 0 || leaders.topTopics.length > 0 || leaders.topShorts.length > 0) && (
          <div className="mt-6 grid gap-4 sm:grid-cols-3 text-sm">
            <div>
              <div className="text-xs uppercase tracking-[0.12em] text-[#5A6E82]">Top hooks</div>
              <ul className="mt-2 space-y-1 text-[#F5E8D2]/80">
                {leaders.topHooks.map((h) => (
                  <li key={h.hook}>
                    {h.hook} · APV {h.avgApv.toFixed(1)}% (n={h.n})
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <div className="text-xs uppercase tracking-[0.12em] text-[#5A6E82]">Top topics</div>
              <ul className="mt-2 space-y-1 text-[#F5E8D2]/80">
                {leaders.topTopics.map((t) => (
                  <li key={t.topic}>
                    {t.topic} · CTR {t.avgCtr.toFixed(2)}% (n={t.n})
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <div className="text-xs uppercase tracking-[0.12em] text-[#5A6E82]">Top Shorts</div>
              <ul className="mt-2 space-y-1 text-[#F5E8D2]/80">
                {leaders.topShorts.map((s) => (
                  <li key={s.title}>
                    {s.title} · APV {s.apv.toFixed(1)}%
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </section>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {byPlatform.map((p) => (
          <div key={p.platform} className="card-panel p-4">
            <div
              className="text-xs uppercase tracking-[0.14em]"
              style={{ color: PLATFORMS[p.platform as keyof typeof PLATFORMS].color }}
            >
              {PLATFORMS[p.platform as keyof typeof PLATFORMS].label}
            </div>
            <div className="mt-3 text-2xl">{p.views} views</div>
            <div className="mt-1 text-sm text-[#F5E8D2]/55">
              n={p.n} · eng {p.avgEng != null ? (p.avgEng * 100).toFixed(1) + "%" : "—"} · subs{" "}
              {p.subs}
            </div>
          </div>
        ))}
      </section>

      <section className="card-panel p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Clip recommendations</h2>
        {lowDataMessage ? (
          <p className="mt-4 rounded-xl border border-[#FFC85A]/30 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#FFC85A]">
            {lowDataMessage}
          </p>
        ) : null}
        <ul className="mt-4 space-y-3">
          {insights.map((insight) => (
            <li key={insight.finding} className="rounded-xl bg-white/3 p-4 text-sm">
              <div className="text-[#F5E8D2]">{insight.finding}</div>
              <div className="mt-1 text-[#F5E8D2]/50">{insight.evidence}</div>
              <div className="mt-2 text-[#FF7A24]">{insight.recommendedAction}</div>
            </li>
          ))}
        </ul>
      </section>

      <section className="card-panel overflow-x-auto p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Clip comparison</h2>
        <table className="mt-4 w-full min-w-[920px] text-left text-sm">
          <thead className="text-xs uppercase tracking-[0.12em] text-[#5A6E82]">
            <tr>
              <th className="pb-2">Clip</th>
              <th className="pb-2">Platform</th>
              <th className="pb-2">Hook</th>
              <th className="pb-2">Views</th>
              <th className="pb-2">Impr.</th>
              <th className="pb-2">CTR</th>
              <th className="pb-2">Engagement</th>
              <th className="pb-2">Subs/1k</th>
              <th className="pb-2">APV</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => {
              const ctr =
                r.metrics.clickThroughRate ??
                computeCtr(r.metrics.impressions, r.metrics.views);
              return (
                <tr key={`${r.title}-${r.platform}-${i}`} className="border-t border-white/5">
                  <td className="py-2">{r.title}</td>
                  <td className="py-2">{r.platform}</td>
                  <td className="py-2">{r.hookCategory}</td>
                  <td className="py-2">{r.metrics.views ?? "—"}</td>
                  <td className="py-2">{r.metrics.impressions ?? "—"}</td>
                  <td className="py-2">{ctr != null ? `${ctr.toFixed(2)}%` : "—"}</td>
                  <td className="py-2">
                    {engagementRate(r.metrics) != null
                      ? `${((engagementRate(r.metrics) as number) * 100).toFixed(1)}%`
                      : "—"}
                  </td>
                  <td className="py-2">
                    {perThousand(r.metrics.subscribersGained, r.metrics.views)?.toFixed(2) ?? "—"}
                  </td>
                  <td className="py-2">
                    {r.metrics.averagePercentageViewed != null
                      ? `${r.metrics.averagePercentageViewed}%`
                      : r.metrics.completionRate != null
                        ? `${r.metrics.completionRate}%`
                        : "—"}
                  </td>
                </tr>
              );
            })}
            {!rows.length ? (
              <tr>
                <td colSpan={9} className="py-6 text-[#F5E8D2]/50">
                  No metrics imported yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </section>
    </div>
  );
}
