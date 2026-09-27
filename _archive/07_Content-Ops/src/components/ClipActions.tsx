"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ClipActions({ clipId, status }: { clipId: string; status: string }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);

  async function setStatus(next: string) {
    setBusy(true);
    try {
      const res = await fetch(`/api/clips/${clipId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: next }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      router.refresh();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-wrap gap-2">
      {status === "proposed" ? (
        <>
          <button
            disabled={busy}
            onClick={() => setStatus("approved")}
            className="rounded-full bg-[#FF7A24] px-3 py-1.5 text-xs text-[#0A0C12]"
          >
            Approve
          </button>
          <button
            disabled={busy}
            onClick={() => setStatus("rejected")}
            className="rounded-full border border-white/15 px-3 py-1.5 text-xs"
          >
            Reject
          </button>
        </>
      ) : null}
      {status === "approved" ? (
        <button
          disabled={busy}
          onClick={() => setStatus("editing")}
          className="rounded-full border border-white/15 px-3 py-1.5 text-xs"
        >
          Start editing
        </button>
      ) : null}
      {status === "editing" ? (
        <button
          disabled={busy}
          onClick={() => setStatus("exported")}
          className="rounded-full border border-white/15 px-3 py-1.5 text-xs"
        >
          Mark exported
        </button>
      ) : null}
    </div>
  );
}
