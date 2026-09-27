import Link from "next/link";
import { listPrograms, getProgramPerformance } from "@/lib/affiliate/programs";

export const dynamic = "force-dynamic";

export default async function AffiliateProgramsPage() {
  const programs = await listPrograms();
  const rows = await Promise.all(
    programs.map(async (p) => ({
      program: p,
      perf: await getProgramPerformance(p.id),
      categories: p.categoriesJson
        ? (JSON.parse(p.categoriesJson) as string[])
        : [],
    })),
  );

  return (
    <div className="space-y-8">
      <div>
        <Link href="/affiliate" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
          ← Affiliate
        </Link>
        <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl">
          Programmes
        </h1>
        <p className="mt-2 text-sm text-[#F5E8D2]/55">
          Affiliate IDs come from env / admin config — never hard-coded in seed.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {rows.map(({ program, perf, categories }) => (
          <div key={program.id} className="card-panel space-y-3 p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
                  {program.name}
                </h2>
                <p className="mt-1 text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
                  {program.status} · {program.slug}
                </p>
              </div>
              <div className="text-right text-xs text-[#5A6E82]">
                {program._count.products} products
              </div>
            </div>
            <p className="text-sm text-[#F5E8D2]/65">{program.description}</p>
            <div className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
              <div>
                <div className="text-xs text-[#5A6E82]">Placements</div>
                <div>{perf.placements}</div>
              </div>
              <div>
                <div className="text-xs text-[#5A6E82]">Clicks</div>
                <div>{perf.clicks}</div>
              </div>
              <div>
                <div className="text-xs text-[#5A6E82]">Conv. rate</div>
                <div>{perf.conversionRate != null ? `${perf.conversionRate}%` : "—"}</div>
              </div>
              <div>
                <div className="text-xs text-[#5A6E82]">Avg EPC</div>
                <div>{perf.epc != null ? `£${perf.epc.toFixed(2)}` : "—"}</div>
              </div>
            </div>
            <div className="text-sm text-[#F5E8D2]/7">
              Est. revenue: £{perf.revenue.toFixed(2)}
            </div>
            {categories.length ? (
              <p className="text-xs text-[#5A6E82]">{categories.join(" · ")}</p>
            ) : null}
            {program.affiliateIdEnvKey ? (
              <p className="text-xs text-[#FFC85A]/80">
                ID env key: {program.affiliateIdEnvKey}
              </p>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}
