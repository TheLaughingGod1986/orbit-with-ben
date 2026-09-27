"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function DistributionPackButton({ videoId }: { videoId: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function run() {
    setLoading(true);
    setMessage(null);
    try {
      const res = await fetch(`/api/videos/${videoId}/distribution-pack`, {
        method: "POST",
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      setMessage(`Proposed ${data.created} clip(s). ${data.warnings?.join(" ") || ""}`);
      router.refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="text-right">
      <button
        onClick={run}
        disabled={loading}
        className="rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12] disabled:opacity-60"
      >
        {loading ? "Generating…" : "Create Distribution Pack"}
      </button>
      {message ? <p className="mt-2 max-w-xs text-xs text-[#F5E8D2]/60">{message}</p> : null}
    </div>
  );
}
