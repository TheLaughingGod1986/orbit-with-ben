"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function PlatformSettingsForm(props: {
  id: string;
  enabled: boolean;
  accountDisplayName: string;
  profileUrl: string;
  defaultCallToAction: string;
  defaultHashtags: string;
  publishingMethod: string;
  defaultVisibility: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState(props);
  const [msg, setMsg] = useState<string | null>(null);

  async function save() {
    const res = await fetch(`/api/settings/platforms/${props.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    if (!res.ok) {
      setMsg(data.error || "Failed");
      return;
    }
    setMsg("Saved");
    router.refresh();
  }

  return (
    <div className="mt-4 grid gap-2 md:grid-cols-2">
      <label className="text-xs text-[#5A6E82]">
        Enabled
        <select
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm text-[#F5E8D2]"
          value={form.enabled ? "yes" : "no"}
          onChange={(e) => setForm({ ...form, enabled: e.target.value === "yes" })}
        >
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label className="text-xs text-[#5A6E82]">
        Display name
        <input
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm"
          value={form.accountDisplayName}
          onChange={(e) => setForm({ ...form, accountDisplayName: e.target.value })}
        />
      </label>
      <label className="text-xs text-[#5A6E82]">
        Profile URL
        <input
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm"
          value={form.profileUrl}
          onChange={(e) => setForm({ ...form, profileUrl: e.target.value })}
        />
      </label>
      <label className="text-xs text-[#5A6E82]">
        Default CTA
        <input
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm"
          value={form.defaultCallToAction}
          onChange={(e) => setForm({ ...form, defaultCallToAction: e.target.value })}
        />
      </label>
      <label className="text-xs text-[#5A6E82]">
        Publishing method
        <select
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm"
          value={form.publishingMethod}
          onChange={(e) => setForm({ ...form, publishingMethod: e.target.value })}
        >
          <option value="manual">manual</option>
          <option value="scheduled_export">scheduled_export</option>
          <option value="api">api</option>
          <option value="third_party">third_party</option>
        </select>
      </label>
      <label className="text-xs text-[#5A6E82]">
        Default visibility
        <input
          className="mt-1 w-full rounded-lg border border-white/10 bg-[#0A0C12] px-2 py-1.5 text-sm"
          value={form.defaultVisibility}
          onChange={(e) => setForm({ ...form, defaultVisibility: e.target.value })}
        />
      </label>
      <div className="md:col-span-2">
        <button onClick={save} className="rounded-full bg-white/10 px-4 py-2 text-sm">
          Save platform
        </button>
        {msg ? <span className="ml-3 text-xs text-[#FFC85A]">{msg}</span> : null}
      </div>
    </div>
  );
}
