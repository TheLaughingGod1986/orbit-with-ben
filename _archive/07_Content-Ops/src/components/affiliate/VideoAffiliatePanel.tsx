"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type PlacementRow = {
  id: string;
  status: string;
  placementType: string;
  relevanceScore: number | null;
  affiliateProduct: {
    id: string;
    name: string;
    slug: string;
    category: string;
    estimatedCommission: number | null;
    affiliateProgram: { name: string };
  };
};

type SocialSnippet = {
  platform: string;
  label: string;
  caption: string;
  trackedUrl: string | null;
  clickSource: string;
  includeAffiliateMention: boolean;
  skipReason?: string;
  approvedForPublish: false;
  notes: string[];
};

export function VideoAffiliatePanel({
  videoId,
  placements: initial,
  opportunityScore,
}: {
  videoId: string;
  placements: PlacementRow[];
  opportunityScore: number;
}) {
  const router = useRouter();
  const [placements, setPlacements] = useState(initial);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [snippets, setSnippets] = useState<SocialSnippet[]>([]);
  const [snippetsMeta, setSnippetsMeta] = useState<{
    placementApproved: boolean;
    videoSlug: string;
  } | null>(null);

  const loadSnippets = useCallback(async () => {
    try {
      const res = await fetch(`/api/affiliate/social-snippets?videoId=${videoId}`);
      const data = await res.json();
      if (res.ok) {
        setSnippets(data.snippets || []);
        setSnippetsMeta({
          placementApproved: Boolean(data.placementApproved),
          videoSlug: data.videoSlug,
        });
      }
    } catch {
      /* non-blocking */
    }
  }, [videoId]);

  useEffect(() => {
    void loadSnippets();
  }, [loadSnippets]);

  async function call(body: Record<string, unknown>) {
    setBusy(true);
    setMessage(null);
    try {
      const res = await fetch("/api/affiliate/placements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) {
        setMessage(data.error || "Action failed");
        return;
      }
      if (data.placements) {
        setPlacements(
          data.placements.map(
            (p: PlacementRow & { affiliateProduct: PlacementRow["affiliateProduct"] }) => p,
          ),
        );
      }
      setMessage("Updated");
      router.refresh();
      await loadSnippets();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  async function refreshList() {
    const res = await fetch(`/api/affiliate/placements?videoId=${videoId}`);
    const data = await res.json();
    if (res.ok) setPlacements(data.placements);
  }

  async function copyCaption(caption: string) {
    try {
      await navigator.clipboard.writeText(caption);
      setMessage("Copied social caption");
    } catch {
      setMessage("Could not copy — select the text manually");
    }
  }

  return (
    <div className="card-panel space-y-4 p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Affiliate Monetisation
          </h2>
          <p className="mt-1 text-sm text-[#F5E8D2]/55">
            Opportunity score {opportunityScore}/100 · relevance before revenue
          </p>
        </div>
        <button
          disabled={busy}
          onClick={() =>
            call({ action: "regenerate", videoId, replaceAll: false }).then(refreshList)
          }
          className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12] disabled:opacity-50"
        >
          Regenerate recommendations
        </button>
      </div>

      {placements.length === 0 ? (
        <p className="text-sm text-[#F5E8D2]/55">
          No affiliate placements yet. Generate recommendations to match products to this episode.
        </p>
      ) : (
        <ul className="space-y-3">
          {placements.map((p) => (
            <li
              key={p.id}
              className="rounded-xl border border-white/5 bg-white/3 px-4 py-3 text-sm"
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <div className="text-[#F5E8D2]">{p.affiliateProduct.name}</div>
                  <div className="mt-1 text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                    {p.placementType} · {p.status} · score{" "}
                    {p.relevanceScore != null ? Math.round(p.relevanceScore) : "—"} ·{" "}
                    {p.affiliateProduct.affiliateProgram.name}
                    {p.affiliateProduct.estimatedCommission != null
                      ? ` · ~£${p.affiliateProduct.estimatedCommission.toFixed(2)} est.`
                      : ""}
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    disabled={busy}
                    onClick={async () => {
                      setBusy(true);
                      setMessage(null);
                      try {
                        const res = await fetch("/api/affiliate/placements", {
                          method: "POST",
                          headers: { "Content-Type": "application/json" },
                          body: JSON.stringify({
                            action: "status",
                            placementId: p.id,
                            status: "APPROVED",
                          }),
                        });
                        const data = await res.json();
                        if (!res.ok) {
                          setMessage(
                            data.trustGate
                              ? `Trust gate: ${data.error}`
                              : data.error || "Approve failed",
                          );
                          return;
                        }
                        setMessage("Approved");
                        router.refresh();
                        await loadSnippets();
                      } finally {
                        setBusy(false);
                      }
                    }}
                    className="rounded-full border border-white/15 px-3 py-1 text-xs"
                  >
                    Approve
                  </button>
                  <button
                    disabled={busy}
                    onClick={() => call({ action: "status", placementId: p.id, status: "REJECTED" })}
                    className="rounded-full border border-white/15 px-3 py-1 text-xs"
                  >
                    Reject
                  </button>
                  <button
                    disabled={busy}
                    onClick={() => call({ action: "remove", placementId: p.id })}
                    className="rounded-full border border-[#FF7A24]/40 px-3 py-1 text-xs text-[#FF7A24]"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}

      <section className="space-y-3 border-t border-white/10 pt-4">
        <div>
          <h3 className="font-[family-name:var(--font-orbit-display)] text-lg text-[#F5E8D2]">
            Live social snippets
          </h3>
          <p className="mt-1 text-xs text-[#F5E8D2]/55">
            Threads · Instagram Reels + feed · Facebook Page. Copy or send through the existing
            publishing pipeline — never auto-posted. Links are YouTube or /go/ only.
            {snippetsMeta && !snippetsMeta.placementApproved
              ? " Approve a description placement before soft mentions appear."
              : null}
          </p>
        </div>
        {snippets.length === 0 ? (
          <p className="text-sm text-[#F5E8D2]/45">
            No snippets yet — approve a relevant placement first.
          </p>
        ) : (
          <ul className="space-y-3">
            {snippets.map((s) => (
              <li
                key={s.platform}
                className="rounded-xl border border-white/5 bg-white/3 px-4 py-3 text-sm"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                    {s.label} · utm_source={s.clickSource}
                    {s.includeAffiliateMention ? "" : " · no soft mention"}
                  </div>
                  <button
                    type="button"
                    onClick={() => copyCaption(s.caption)}
                    className="rounded-full border border-white/15 px-3 py-1 text-xs"
                  >
                    Copy
                  </button>
                </div>
                <pre className="mt-2 whitespace-pre-wrap font-sans text-[#F5E8D2]/85">
                  {s.caption}
                </pre>
                {s.skipReason ? (
                  <p className="mt-2 text-xs text-[#FFC85A]/80">Skipped soft mention: {s.skipReason}</p>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      {message ? <p className="text-xs text-[#FFC85A]">{message}</p> : null}
    </div>
  );
}
