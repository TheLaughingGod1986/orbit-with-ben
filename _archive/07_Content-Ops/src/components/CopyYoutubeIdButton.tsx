"use client";

import { useState, type MouseEvent } from "react";

/** One-tap copy of a stored YouTube id for Auditor pass/fail. */
export function CopyYoutubeIdButton({ youtubeId }: { youtubeId: string }) {
  const [copied, setCopied] = useState(false);

  async function copy(e: MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    try {
      await navigator.clipboard.writeText(youtubeId);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  }

  return (
    <button
      type="button"
      onClick={copy}
      title="Copy YouTube id"
      className="inline-flex min-h-11 max-w-full items-center gap-2 rounded-full border border-white/10 bg-[#0A0C12]/60 px-3 py-2 font-mono text-sm text-[#FFC85A] transition hover:bg-white/5"
    >
      <span className="truncate">{copied ? "Copied" : youtubeId}</span>
    </button>
  );
}
