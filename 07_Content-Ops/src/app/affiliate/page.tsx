import Link from "next/link";
import { format } from "date-fns";
import { getAffiliateDashboardSummary } from "@/lib/affiliate/analytics";
import { getAffiliateGoalsPanel } from "@/lib/affiliate/goals-service";
import { getAffiliateGoLiveReport } from "@/lib/affiliate/go-live-service";
import type { GoalsPaceStatus } from "@/lib/affiliate/goals";
import { AffiliateApplyUrlsButton } from "@/components/affiliate/AffiliateApplyUrlsButton";

export const dynamic = "force-dynamic";

function StatCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
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

function formatGbp(n: number): string {
  return `£${n.toFixed(2)}`;
}

function statusLabel(status: GoalsPaceStatus): string {
  switch (status) {
    case "ahead":
      return "Ahead";
    case "on_track":
      return "On track";
    case "behind":
      return "Behind";
    case "not_started":
      return "Not started";
    default:
      return status;
  }
}

function statusTone(status: GoalsPaceStatus): string {
  switch (status) {
    case "ahead":
      return "border-[#5AEE8A]/30 bg-[#5AEE8A]/10 text-[#5AEE8A]";
    case "on_track":
      return "border-[#FFC85A]/30 bg-[#FFC85A]/10 text-[#FFC85A]";
    case "behind":
      return "border-[#FF7A24]/35 bg-[#FF7A24]/10 text-[#FF7A24]";
    default:
      return "border-white/15 bg-white/5 text-[#F5E8D2]/70";
  }
}

function formatRange(startIso: string, endIso: string): string {
  const start = new Date(startIso);
  const end = new Date(endIso);
  return `${format(start, "d MMM yyyy")} – ${format(end, "d MMM yyyy")}`;
}

export default async function AffiliateDashboardPage() {
  const [data, goals, goLive] = await Promise.all([
    getAffiliateDashboardSummary(),
    getAffiliateGoalsPanel(),
    getAffiliateGoLiveReport(),
  ]);
  const warnings: string[] = [];
  if (data.warnings.videosMissingLinks > 0) {
    warnings.push(
      `${data.warnings.videosMissingLinks} published/high-view video(s) still missing affiliate links.`,
    );
  }
  if (data.warnings.inactiveProductInDescriptions > 0) {
    warnings.push(
      `${data.warnings.inactiveProductInDescriptions} inactive product(s) still appear in descriptions.`,
    );
  }
  if (data.warnings.brokenUrls > 0) {
    warnings.push(`${data.warnings.brokenUrls} broken affiliate URL(s) detected.`);
  }
  if (data.warnings.highClickZeroConversions > 0) {
    warnings.push(
      `${data.warnings.highClickZeroConversions} high-click product(s) with zero conversions.`,
    );
  }
  if (data.warnings.programmesNeedingReports > 0) {
    warnings.push(
      `${data.warnings.programmesNeedingReports} active programme(s) still need reporting data.`,
    );
  }

  const progressPct =
    goals.targetGbp && goals.targetGbp > 0
      ? Math.min(100, Math.round((goals.revenueSoFarGbp / goals.targetGbp) * 100))
      : goals.revenueSoFarGbp > 0
        ? 100
        : 0;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-[#FF7A24]">Monetisation</p>
          <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
            Affiliate
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-[#F5E8D2]/55">
            Relevance before revenue. Only recommend products Orbit would still endorse with no
            commission.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            href="/affiliate/products"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            Products
          </Link>
          <Link
            href="/affiliate/programs"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            Programmes
          </Link>
          <Link
            href="/affiliate/opportunities"
            className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]"
          >
            Opportunities
          </Link>
          <Link
            href="/affiliate/import"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            CSV import
          </Link>
        </div>
      </div>

      <section className="card-panel space-y-4 p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
              Go-live readiness
            </h2>
            <p className="mt-1 text-sm text-[#F5E8D2]/55">{goLive.summary}</p>
            <p className="mt-2 text-xs text-[#F5E8D2]/45">
              Tracked redirects:{" "}
              {goLive.readyForTrackedRedirects ? "ready" : "not ready"} · Paid traffic:{" "}
              {goLive.readyForPaidTraffic ? "ready" : "waiting on programme IDs"}
            </p>
          </div>
          <AffiliateApplyUrlsButton />
        </div>
        <ul className="space-y-2">
          {goLive.checks.map((c) => (
            <li
              key={c.id}
              className="flex flex-wrap items-start justify-between gap-2 rounded-xl border border-white/5 bg-white/3 px-4 py-3 text-sm"
            >
              <div>
                <div className="text-[#F5E8D2]">{c.label}</div>
                <div className="mt-1 text-xs text-[#F5E8D2]/55">{c.detail}</div>
              </div>
              <span
                className={`shrink-0 rounded-full border px-2.5 py-0.5 text-[10px] uppercase tracking-[0.14em] ${
                  c.status === "pass"
                    ? "border-[#5AEE8A]/30 text-[#5AEE8A]"
                    : c.status === "warn"
                      ? "border-[#FFC85A]/30 text-[#FFC85A]"
                      : c.status === "manual"
                        ? "border-white/20 text-[#F5E8D2]/60"
                        : "border-[#FF7A24]/35 text-[#FF7A24]"
                }`}
              >
                {c.status}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="card-panel space-y-5 p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
              Goals
            </h2>
            <p className="mt-1 text-xs text-[#F5E8D2]/55">
              Internal ladder only — reporting, not a reason to auto-insert links. Editorial gate
              still decides placements.
            </p>
          </div>
          <span
            className={`rounded-full border px-3 py-1 text-xs uppercase tracking-[0.14em] ${statusTone(goals.status)}`}
          >
            {statusLabel(goals.status)}
          </span>
        </div>

        {!goals.clockStarted ? (
          <p className="text-sm text-[#F5E8D2]/55">
            Clock starts on the first approved placement (or first click if earlier). No goals month
            yet.
          </p>
        ) : (
          <>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div>
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Month</div>
                <div className="mt-1 font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
                  {goals.monthNumber}
                </div>
                <div className="mt-1 text-xs text-[#F5E8D2]/45">
                  {goals.monthStart && goals.monthEnd
                    ? formatRange(goals.monthStart, goals.monthEnd)
                    : "—"}
                </div>
              </div>
              <div>
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                  Revenue vs target
                </div>
                <div className="mt-1 font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
                  {formatGbp(goals.revenueSoFarGbp)}
                  <span className="text-base text-[#F5E8D2]/45">
                    {" "}
                    / {goals.targetGbp != null ? formatGbp(goals.targetGbp) : "—"}
                  </span>
                </div>
                {goals.floorGbp != null ? (
                  <div className="mt-1 text-xs text-[#F5E8D2]/45">
                    Month 1 floor {formatGbp(goals.floorGbp)}
                  </div>
                ) : null}
              </div>
              <div>
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                  Clicks (this goals month)
                </div>
                <div className="mt-1 font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
                  {goals.clicksThisMonth}
                </div>
              </div>
              <div>
                <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                  Links working / broken
                </div>
                <div className="mt-1 font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
                  {goals.workingLinks}
                  <span className="text-base text-[#F5E8D2]/45"> / {goals.brokenLinks}</span>
                </div>
              </div>
            </div>

            <div>
              <div className="mb-1 flex justify-between text-xs text-[#F5E8D2]/45">
                <span>Progress to target</span>
                <span>{progressPct}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-white/10">
                <div
                  className="h-full rounded-full bg-[#FF7A24]"
                  style={{ width: `${progressPct}%` }}
                />
              </div>
              {goals.pacedTargetGbp != null ? (
                <p className="mt-2 text-xs text-[#F5E8D2]/45">
                  Pace line today: {formatGbp(goals.pacedTargetGbp)}
                </p>
              ) : null}
            </div>

            {goals.monthNumber != null && goals.monthNumber >= 2 ? (
              <p className="text-sm text-[#F5E8D2]/70">
                Last month (M{goals.lastMonthNumber}) actual:{" "}
                {goals.lastMonthActualGbp != null
                  ? formatGbp(goals.lastMonthActualGbp)
                  : "—"}
                . This month’s target is 2× that figure.
              </p>
            ) : (
              <p className="text-sm text-[#F5E8D2]/55">
                Month 1 ladder: floor {formatGbp(10)}, target {formatGbp(20)}. Later months: 2×
                previous actual commission.
              </p>
            )}
          </>
        )}
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Active programmes" value={data.activePrograms} />
        <StatCard label="Active products" value={data.activeProducts} />
        <StatCard label="Videos with links" value={data.videosWithLinks} />
        <StatCard label="Clicks (all time)" value={data.clicksTotal} />
        <StatCard label="Clicks (month)" value={data.clicksMonth} />
        <StatCard label="Est. conversions" value={data.conversionsEstimated} />
        <StatCard
          label="Revenue (month)"
          value={`£${data.revenueMonth.toFixed(2)}`}
        />
        <StatCard
          label="Revenue (all time)"
          value={`£${data.revenueTotal.toFixed(2)}`}
        />
        <StatCard
          label="Top product"
          value={data.highestPerformingProduct || "—"}
        />
        <StatCard
          label="Top affiliate video"
          value={data.highestPerformingVideo || "—"}
        />
      </section>

      <section className="card-panel space-y-4 p-5">
        <div>
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Clicks & revenue by source
          </h2>
          <p className="mt-1 text-sm text-[#F5E8D2]/55">
            youtube · threads · instagram · facebook (from /go/ utm_source). Revenue attributed by
            click share per product when CSV conversions have no click id.
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[420px] text-left text-sm">
            <thead>
              <tr className="border-b border-white/10 text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                <th className="py-2 pr-4 font-normal">Source</th>
                <th className="py-2 pr-4 font-normal">Clicks</th>
                <th className="py-2 font-normal">Est. revenue</th>
              </tr>
            </thead>
            <tbody>
              {data.bySource.map((row) => (
                <tr key={row.source} className="border-b border-white/5 text-[#F5E8D2]/85">
                  <td className="py-2.5 pr-4 capitalize">{row.source}</td>
                  <td className="py-2.5 pr-4">{row.clicks}</td>
                  <td className="py-2.5">£{row.revenue.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {warnings.length ? (
        <section className="card-panel space-y-3 p-5">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Warnings
          </h2>
          <ul className="space-y-2">
            {warnings.map((w) => (
              <li
                key={w}
                className="rounded-xl border border-[#FFC85A]/25 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#F5E8D2]"
              >
                {w}
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <section className="card-panel p-5 text-sm text-[#F5E8D2]/55">
          No monetisation warnings right now.
        </section>
      )}
    </div>
  );
}
