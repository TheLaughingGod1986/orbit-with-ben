import { prisma } from "@/lib/storage/prisma";
import { CONTENT_RULES } from "@/config/content-rules";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import Link from "next/link";
import { startOfMonth, endOfMonth } from "date-fns";
import { isDryRun } from "@/lib/env";
import { getHomeMonetisationCard } from "@/lib/affiliate/analytics";

export const dynamic = "force-dynamic";

async function getOverview() {
  const now = new Date();
  const monthStart = startOfMonth(now);
  const monthEnd = endOfMonth(now);

  const [
    filmCount,
    longInProduction,
    longScheduled,
    longPublished,
    clipCount,
    postCount,
    shortsPlanned,
    shortsAwaitingEdit,
    shortsReady,
    postsScheduled,
    postsPublishedMonth,
    metrics,
    bestClip,
    pendingApprovals,
    missingAnalytics,
    heartbeat,
    nextJob,
    recentJobs,
    monetisation,
  ] = await Promise.all([
    prisma.longFormVideo.count(),
    prisma.longFormVideo.count({
      where: { status: { in: ["idea", "scripting", "production", "editing", "ready"] } },
    }),
    prisma.longFormVideo.count({
      where: {
        OR: [{ status: "scheduled" }, { publicationDate: { gt: now } }],
      },
    }),
    prisma.longFormVideo.count({
      where: { status: "published" },
    }),
    prisma.shortClip.count(),
    prisma.platformPost.count(),
    prisma.shortClip.count({ where: { status: { in: ["proposed", "approved"] } } }),
    prisma.shortClip.count({ where: { status: { in: ["approved", "editing"] } } }),
    prisma.shortClip.count({ where: { status: { in: ["exported", "scheduled"] } } }),
    prisma.platformPost.count({ where: { uploadStatus: "scheduled" } }),
    prisma.platformPost.count({
      where: {
        uploadStatus: "published",
        publishedAt: { gte: monthStart, lte: monthEnd },
      },
    }),
    prisma.performanceMetric.aggregate({
      _sum: { views: true, subscribersGained: true },
    }),
    prisma.shortClip.findFirst({
      orderBy: { qualityScore: "desc" },
      include: { longFormVideo: true },
    }),
    prisma.shortClip.count({ where: { status: "proposed" } }),
    prisma.platformPost.count({
      where: {
        uploadStatus: "published",
        metrics: { none: {} },
      },
    }),
    prisma.workerHeartbeat.findFirst({ orderBy: { lastHeartbeatAt: "desc" } }),
    prisma.publishingJob.findFirst({
      where: { status: { in: ["pending", "scheduled", "failed_retryable"] } },
      orderBy: { nextAttemptAt: "asc" },
    }),
    prisma.publishingJob.findMany({
      orderBy: { updatedAt: "desc" },
      take: 5,
      include: { platformPost: true },
    }),
    getHomeMonetisationCard(),
  ]);

  type NextAction = { label: string; href?: string };
  const nextActions: NextAction[] = [];

  if (filmCount === 0) {
    nextActions.push({
      label: "Add the known Thursday films",
      href: "/videos",
    });
  } else if (clipCount === 0 && postCount === 0) {
    // Films exist; Shorts/posts not built yet — do not nag schedule/worker.
    nextActions.push({
      label:
        longScheduled > 0
          ? "Open Thursday films — next scheduled long is on the list."
          : "Open Thursday films — review the catalogue.",
      href: "/videos",
    });
  } else {
    if (pendingApprovals > 0) {
      nextActions.push({
        label: `Approve ${pendingApprovals} proposed clip${pendingApprovals === 1 ? "" : "s"}.`,
        href: "/pipeline",
      });
    }
    if (shortsAwaitingEdit > 0) {
      nextActions.push({
        label: `Move ${shortsAwaitingEdit} clip(s) through editing / export.`,
        href: "/pipeline",
      });
    }
    if (postsScheduled === 0) {
      nextActions.push({
        label: "Schedule this week’s cross-platform posts.",
        href: "/calendar",
      });
    }
    if (missingAnalytics > 0) {
      nextActions.push({
        label: `Import analytics for ${missingAnalytics} published post(s).`,
        href: "/analytics",
      });
    }
    if (monetisation.videosMissingLinks > 0) {
      nextActions.push({
        label: `Review ${monetisation.videosMissingLinks} published/high-view video(s) with no affiliate placement.`,
        href: "/affiliate",
      });
    }
    if (!heartbeat || Date.now() - heartbeat.lastHeartbeatAt.getTime() > 30_000) {
      nextActions.push({
        label: "Start the publishing worker (`npm run worker`) for scheduled API posts.",
      });
    }
    if (!nextActions.length) {
      nextActions.push({
        label: "Pipeline looks clear — register the next long-form video.",
        href: "/videos",
      });
    }
  }

  return {
    filmCount,
    longInProduction,
    longScheduled,
    longPublished,
    shortsPlanned,
    shortsAwaitingEdit,
    shortsReady,
    postsScheduled,
    postsPublishedMonth,
    totalViews: metrics._sum.views ?? 0,
    subsGained: metrics._sum.subscribersGained ?? 0,
    bestClip,
    nextActions,
    cadence: PUBLISHING_SCHEDULE.cadenceMonthlyTargets,
    heartbeat,
    nextJob,
    recentJobs,
    dryRun: isDryRun(),
    monetisation,
  };
}

function StatCard({ label, value, hint }: { label: string; value: string | number; hint?: string }) {
  return (
    <div className="card-panel p-5">
      <div className="text-xs uppercase tracking-[0.18em] text-[#5A6E82]">{label}</div>
      <div className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
        {value}
      </div>
      {hint ? <div className="mt-2 text-xs text-[#F5E8D2]/45">{hint}</div> : null}
    </div>
  );
}

export default async function HomePage() {
  const data = await getOverview();
  const workerOnline =
    data.heartbeat && Date.now() - data.heartbeat.lastHeartbeatAt.getTime() < 30_000;

  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-3xl border border-white/5 bg-[#0d1018]/70 p-8 md:p-10">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(255,122,36,0.2),transparent_40%)]" />
        <p className="text-xs uppercase tracking-[0.28em] text-[#FF7A24]">Orbit with Ben</p>
        <h1 className="mt-3 max-w-2xl font-[family-name:var(--font-orbit-display)] text-4xl leading-tight text-[#F5E8D2] md:text-5xl">
          Content operations studio
        </h1>
        <p className="mt-4 max-w-xl text-[#F5E8D2]/70">
          One long-form pillar becomes a reusable short-form flywheel across YouTube,
          TikTok, Instagram, Facebook, X and Threads — without rebuilding the production system.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/videos"
            className="rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
          >
            Open long-form library
          </Link>
          <Link
            href="/settings/connections"
            className="rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2]"
          >
            Connect accounts
          </Link>
        </div>
      </section>

      <section className="card-panel p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
          Publishing worker
        </h2>
        <p className="mt-2 text-sm text-[#F5E8D2]/7">
          Status: {workerOnline ? "Worker online" : "Worker offline"}
          {data.heartbeat
            ? ` · last heartbeat ${data.heartbeat.lastHeartbeatAt.toISOString()}`
            : ""}
          {data.heartbeat?.lastJobId ? ` · last job ${data.heartbeat.lastJobId}` : ""}
        </p>
        <p className="mt-1 text-sm text-[#F5E8D2]/55">
          Next scheduled job:{" "}
          {data.nextJob
            ? `${data.nextJob.id} · ${data.nextJob.nextAttemptAt?.toISOString() || "due"}`
            : "none"}
        </p>
        <p className="mt-2 text-xs text-[#5A6E82]">
          Local scheduling is not cloud-reliable. Keep `npm run worker` running; laptop sleep stops
          publishes.
          {data.dryRun ? " Dry-run mode is active." : ""}
        </p>
        {data.recentJobs.length ? (
          <ul className="mt-3 space-y-1 text-xs text-[#F5E8D2]/6">
            {data.recentJobs.map((j) => (
              <li key={j.id}>
                <Link href={`/publishing/${j.id}`} className="text-[#FF7A24]">
                  {j.platformPost.platform}
                </Link>{" "}
                · {j.status}
              </li>
            ))}
          </ul>
        ) : null}
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <StatCard
          label="Films in catalogue"
          value={data.filmCount}
          hint={`${data.longInProduction} still in production stages`}
        />
        <StatCard
          label="Films scheduled"
          value={data.longScheduled}
          hint="status scheduled or air date ahead"
        />
        <StatCard
          label="Films published"
          value={data.longPublished}
          hint={`Catalogue · target ${data.cadence.longForm}/mo`}
        />
        <StatCard label="Shorts planned" value={data.shortsPlanned} />
        <StatCard label="Awaiting editing" value={data.shortsAwaitingEdit} />
        <StatCard label="Ready to publish" value={data.shortsReady} />
        <StatCard label="Posts scheduled" value={data.postsScheduled} />
        <StatCard label="Posts published (month)" value={data.postsPublishedMonth} />
        <StatCard label="Cross-platform views" value={data.totalViews} />
        <StatCard label="YT subs gained (tracked)" value={data.subsGained} />
        <StatCard
          label="Best-scoring clip"
          value={data.bestClip?.workingTitle ?? "—"}
          hint={data.bestClip ? `Score ${data.bestClip.qualityScore}/100` : undefined}
        />
      </section>

      <section className="card-panel p-6">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
              Monetisation
            </h2>
            <p className="mt-1 text-sm text-[#F5E8D2]/55">
              Affiliate revenue this month · relevance before commission
            </p>
          </div>
          <Link href="/affiliate/opportunities" className="text-sm text-[#FF7A24] hover:underline">
            Opportunities →
          </Link>
        </div>
        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <StatCard
            label="Affiliate revenue (month)"
            value={`£${data.monetisation.revenueMonth.toFixed(2)}`}
          />
          <StatCard label="Clicks (month)" value={data.monetisation.clicksMonth} />
          <StatCard
            label="Affiliate RPM"
            value={
              data.monetisation.affiliateRpm != null
                ? `£${data.monetisation.affiliateRpm.toFixed(2)}`
                : "—"
            }
          />
          <StatCard
            label="Videos without placements"
            value={data.monetisation.videosMissingLinks}
          />
          <StatCard
            label="Top affiliate video"
            value={data.monetisation.topAffiliateVideo || "—"}
          />
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="card-panel p-6">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
            Pipeline
          </h2>
          <div className="mt-5 flex flex-wrap gap-2">
            {CONTENT_RULES.pipelineStages.map((stage, i) => (
              <div key={stage} className="flex items-center gap-2">
                <span className="pipeline-step rounded-full px-3 py-1.5 text-xs text-[#F5E8D2]/80">
                  {stage}
                </span>
                {i < CONTENT_RULES.pipelineStages.length - 1 ? (
                  <span className="text-[#FF7A24]/60">→</span>
                ) : null}
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm text-[#F5E8D2]/55">
            Canonical schedule preserved: long-form Thursday 19:00 UK · Short #1 at 21:00 · Days 2–7
            at 12:30 · cross-platform staggered within 24 hours.
          </p>
        </div>

        <div className="card-panel p-6">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
            Next action
          </h2>
          <ul className="mt-4 space-y-3">
            {data.nextActions.map((action) => (
              <li
                key={action.label}
                className="rounded-xl border border-[#FF7A24]/25 bg-[#FF7A24]/10 px-4 py-3 text-sm text-[#F5E8D2]"
              >
                {action.href ? (
                  <Link href={action.href} className="font-medium text-[#FFC85A] hover:underline">
                    {action.label}
                  </Link>
                ) : (
                  action.label
                )}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
