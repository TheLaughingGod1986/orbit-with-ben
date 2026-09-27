import Link from "next/link";
import { listVideoOpportunities } from "@/lib/affiliate/analytics";

export const dynamic = "force-dynamic";

export default async function AffiliateOpportunitiesPage() {
  const rows = await listVideoOpportunities();

  return (
    <div className="space-y-8">
      <div>
        <Link href="/affiliate" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
          ← Affiliate
        </Link>
        <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl">
          Opportunities
        </h1>
        <p className="mt-2 text-sm text-[#F5E8D2]/55">
          Videos sorted by affiliate opportunity. High views + no links = monetisation opportunity.
        </p>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-white/5">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-white/3 text-xs uppercase tracking-[0.12em] text-[#5A6E82]">
            <tr>
              <th className="px-4 py-3">Video</th>
              <th className="px-4 py-3">Views</th>
              <th className="px-4 py-3">Topic</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Products</th>
              <th className="px-4 py-3">Links</th>
              <th className="px-4 py-3">Clicks</th>
              <th className="px-4 py-3">Est. rev</th>
              <th className="px-4 py-3">Rev / 1k</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr
                key={r.videoId}
                className={`border-t border-white/5 ${
                  r.monetisationOpportunity ? "bg-[#FF7A24]/8" : ""
                }`}
              >
                <td className="px-4 py-3">
                  <Link href={`/videos/${r.videoId}`} className="text-[#FF7A24] hover:underline">
                    {r.workingTitle || r.title}
                  </Link>
                  {r.monetisationOpportunity ? (
                    <div className="mt-1 text-[10px] uppercase tracking-[0.16em] text-[#FFC85A]">
                      Monetisation opportunity
                    </div>
                  ) : null}
                </td>
                <td className="px-4 py-3">{r.views}</td>
                <td className="px-4 py-3">{r.topic}</td>
                <td className="px-4 py-3 font-medium">{r.affiliateScore}</td>
                <td className="px-4 py-3">{r.productsAvailable}</td>
                <td className="px-4 py-3">{r.linksInserted}</td>
                <td className="px-4 py-3">{r.clicks}</td>
                <td className="px-4 py-3">£{r.estimatedRevenue.toFixed(2)}</td>
                <td className="px-4 py-3">
                  {r.revenuePerThousandViews != null
                    ? `£${r.revenuePerThousandViews.toFixed(2)}`
                    : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
