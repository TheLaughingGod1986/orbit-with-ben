"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ClipWorkspaceActions({
  clipId,
  status,
}: {
  clipId: string;
  status: string;
}) {
  const router = useRouter();
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function generateCopy() {
    setBusy(true);
    setMsg(null);
    try {
      const res = await fetch(`/api/clips/${clipId}/platform-copy`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      setMsg(`Generated copy for ${data.count} platforms.`);
      router.refresh();
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  async function exportPackage() {
    setBusy(true);
    setMsg(null);
    try {
      const res = await fetch(`/api/clips/${clipId}/export`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed");
      setMsg(`Export package written to ${data.dir}`);
      router.refresh();
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card-panel flex flex-wrap items-center gap-3 p-4">
      <span className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Status: {status}</span>
      <button
        disabled={busy || !["approved", "editing", "exported", "scheduled", "published"].includes(status)}
        onClick={generateCopy}
        className="rounded-full border border-white/15 px-4 py-2 text-sm disabled:opacity-40"
      >
        Generate platform copy
      </button>
      <button
        disabled={busy || !["approved", "editing", "exported", "scheduled", "published"].includes(status)}
        onClick={exportPackage}
        className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12] disabled:opacity-40"
      >
        Export upload package
      </button>
      {msg ? <span className="text-xs text-[#F5E8D2]/60">{msg}</span> : null}
    </div>
  );
}
