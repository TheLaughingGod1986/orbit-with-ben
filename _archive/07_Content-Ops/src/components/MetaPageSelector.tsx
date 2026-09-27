"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

type PageOption = {
  id: string;
  name?: string;
  instagram_business_account?: { id: string; username?: string; name?: string };
};

export function MetaPageSelector({
  connectionId,
  metadataJson,
}: {
  connectionId: string;
  metadataJson?: string | null;
}) {
  const router = useRouter();
  const pages = useMemo(() => {
    try {
      return (metadataJson ? JSON.parse(metadataJson).pages : []) as PageOption[];
    } catch {
      return [] as PageOption[];
    }
  }, [metadataJson]);
  const [pageId, setPageId] = useState(pages[0]?.id || "");
  const [igId, setIgId] = useState(pages[0]?.instagram_business_account?.id || "");
  const [msg, setMsg] = useState<string | null>(null);

  if (!pages.length) return null;

  async function save() {
    const res = await fetch(`/api/connections/${connectionId}/select-page`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pageId,
        instagramBusinessAccountId: igId || null,
      }),
    });
    const data = await res.json();
    setMsg(data.message || data.error);
    router.refresh();
  }

  const selected = pages.find((p) => p.id === pageId);

  return (
    <div className="mt-4 space-y-2 rounded-xl border border-white/10 bg-white/3 p-3 text-xs">
      <div className="uppercase tracking-[0.14em] text-[#5A6E82]">Select Facebook Page</div>
      <select
        value={pageId}
        onChange={(e) => {
          setPageId(e.target.value);
          const p = pages.find((x) => x.id === e.target.value);
          setIgId(p?.instagram_business_account?.id || "");
        }}
        className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        {pages.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name || p.id}
          </option>
        ))}
      </select>
      {selected?.instagram_business_account ? (
        <select
          value={igId}
          onChange={(e) => setIgId(e.target.value)}
          className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
        >
          <option value={selected.instagram_business_account.id}>
            IG @{selected.instagram_business_account.username || selected.instagram_business_account.id}
          </option>
        </select>
      ) : (
        <p className="text-[#FFC85A]">No Instagram professional account linked to this Page.</p>
      )}
      <button onClick={save} className="rounded-full bg-white/10 px-3 py-1.5 hover:bg-white/15">
        Save selection
      </button>
      {msg ? <div className="text-[#FFC85A]">{msg}</div> : null}
    </div>
  );
}
