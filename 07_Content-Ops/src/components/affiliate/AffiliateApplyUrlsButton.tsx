"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export function AffiliateApplyUrlsButton() {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function apply() {
    setBusy(true);
    setMessage(null);
    try {
      const res = await fetch("/api/affiliate/go-live", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "apply-urls", dryRun: false }),
      });
      const data = await res.json();
      if (!res.ok) {
        setMessage(data.error || "Apply failed");
        return;
      }
      const n = (data.updated || []).length;
      setMessage(
        n
          ? `Updated ${n} product URL(s). Swap search pages for exact ASINs when you lock the product.`
          : "No URL changes needed.",
      );
      router.refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <button
        type="button"
        disabled={busy}
        onClick={() => void apply()}
        className="rounded-full border border-white/15 px-4 py-2 text-sm disabled:opacity-50"
      >
        {busy ? "Applying…" : "Apply live destination URLs"}
      </button>
      {message ? <span className="text-xs text-[#FFC85A]">{message}</span> : null}
    </div>
  );
}
