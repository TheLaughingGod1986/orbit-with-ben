"use client";

import { useState } from "react";

/** Film-only caption for social: wonder one-liner + YouTube watch URL. */
export function CopyFilmCaptionButton({
  oneLiner,
  youtubeUrl,
}: {
  oneLiner: string;
  youtubeUrl: string;
}) {
  const [copied, setCopied] = useState(false);
  const caption = `${oneLiner.trim()}\n\n${youtubeUrl.trim()}`;

  async function copy() {
    try {
      await navigator.clipboard.writeText(caption);
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
      className="inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-4 py-2 text-sm text-[#F5E8D2] transition hover:bg-white/5"
    >
      {copied ? "Copied" : "Copy film caption"}
    </button>
  );
}
