"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { EnqueuePublishButton } from "@/components/EnqueuePublishButton";

export function PostStatusForm({
  postId,
  status,
  url,
  approvedForPublish = false,
  privacyStatus,
  madeForKids,
  platform,
}: {
  postId: string;
  status: string;
  url?: string | null;
  approvedForPublish?: boolean;
  privacyStatus?: string | null;
  madeForKids?: boolean | null;
  platform?: string;
}) {
  const router = useRouter();
  const [nextStatus, setNextStatus] = useState(status);
  const [platformUrl, setPlatformUrl] = useState(url || "");
  const [scheduledAt, setScheduledAt] = useState("");
  const [repostReason, setRepostReason] = useState("");
  const [approved, setApproved] = useState(approvedForPublish);
  const [privacy, setPrivacy] = useState(privacyStatus || (platform === "youtube_shorts" ? "private" : "public"));
  const [kids, setKids] = useState(madeForKids === null || madeForKids === undefined ? "" : madeForKids ? "yes" : "no");
  const [msg, setMsg] = useState<string | null>(null);

  async function save() {
    setMsg(null);
    const res = await fetch(`/api/posts/${postId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        uploadStatus: nextStatus,
        platformUrl: platformUrl || null,
        scheduledAt: scheduledAt || undefined,
        repostReason: repostReason || undefined,
        approvedForPublish: approved,
        privacyStatus: privacy || null,
        madeForKids: kids === "" ? null : kids === "yes",
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      setMsg(data.error || "Failed");
      if (data.warnings) {
        setMsg(
          (data.error || "Duplicate warning") +
            " — " +
            data.warnings.map((w: { reason: string }) => w.reason).join("; "),
        );
      }
      return;
    }
    setMsg("Saved");
    router.refresh();
  }

  return (
    <div className="flex min-w-[240px] flex-col gap-2 text-xs">
      <select
        value={nextStatus}
        onChange={(e) => setNextStatus(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        {["draft", "ready", "scheduled", "published", "failed", "skipped"].map((s) => (
          <option key={s} value={s}>
            {s}
          </option>
        ))}
      </select>
      <label className="flex items-center gap-2 text-[#F5E8D2]/7">
        <input type="checkbox" checked={approved} onChange={(e) => setApproved(e.target.checked)} />
        Approved for API publish
      </label>
      <select
        value={privacy}
        onChange={(e) => setPrivacy(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        <option value="private">privacy: private</option>
        <option value="unlisted">privacy: unlisted</option>
        <option value="public">privacy: public</option>
        <option value="SELF_ONLY">privacy: SELF_ONLY (TikTok test)</option>
      </select>
      {platform === "youtube_shorts" ? (
        <select
          value={kids}
          onChange={(e) => setKids(e.target.value)}
          className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
        >
          <option value="">madeForKids: unset</option>
          <option value="no">madeForKids: no</option>
          <option value="yes">madeForKids: yes</option>
        </select>
      ) : null}
      <input
        type="datetime-local"
        value={scheduledAt}
        onChange={(e) => setScheduledAt(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      />
      <input
        placeholder="Published URL"
        value={platformUrl}
        onChange={(e) => setPlatformUrl(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      />
      <select
        value={repostReason}
        onChange={(e) => setRepostReason(e.target.value)}
        className="rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5"
      >
        <option value="">Repost reason (if needed)</option>
        <option>New hook</option>
        <option>New edit</option>
        <option>Seasonal repost</option>
        <option>Performance retest</option>
        <option>Updated information</option>
      </select>
      <button onClick={save} className="rounded-full bg-white/10 px-3 py-1.5 hover:bg-white/15">
        Update
      </button>
      <EnqueuePublishButton postId={postId} />
      {msg ? <span className="text-[#FFC85A]">{msg}</span> : null}
    </div>
  );
}
