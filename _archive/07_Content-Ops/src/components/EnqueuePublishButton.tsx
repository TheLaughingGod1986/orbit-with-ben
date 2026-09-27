"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function EnqueuePublishButton({
  postId,
  label = "Enqueue publish",
}: {
  postId: string;
  label?: string;
}) {
  const router = useRouter();
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function run(publishNow: boolean) {
    setBusy(true);
    setMsg(null);
    const res = await fetch(`/api/posts/${postId}/enqueue`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ publishNow }),
    });
    const data = await res.json();
    setBusy(false);
    if (!res.ok) {
      setMsg(data.error || "Failed to enqueue");
      return;
    }
    setMsg(data.duplicate ? "Existing job reused" : "Job enqueued");
    if (data.jobId) router.push(`/publishing/${data.jobId}`);
    else router.refresh();
  }

  return (
    <div className="flex flex-col gap-2 text-xs">
      <button
        disabled={busy}
        onClick={() => run(false)}
        className="rounded-full bg-[#FF7A24] px-3 py-1.5 font-medium text-[#0A0C12] disabled:opacity-50"
      >
        {label}
      </button>
      <button
        disabled={busy}
        onClick={() => run(true)}
        className="rounded-full border border-white/15 px-3 py-1.5 disabled:opacity-50"
      >
        Publish now (queue)
      </button>
      {msg ? <span className="text-[#FFC85A]">{msg}</span> : null}
    </div>
  );
}
