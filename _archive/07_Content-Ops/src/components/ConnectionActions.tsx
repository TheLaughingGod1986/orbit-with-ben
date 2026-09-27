"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export function ConnectionActions(props: {
  platform: string;
  connectionId?: string;
  connectPath?: string;
  canConnect: boolean;
}) {
  const router = useRouter();
  const [msg, setMsg] = useState<string | null>(null);

  async function validate() {
    if (!props.connectionId) return;
    const res = await fetch(`/api/connections/${props.connectionId}/validate`, { method: "POST" });
    const data = await res.json();
    setMsg(data.message || (res.ok ? "Validated" : data.error));
    router.refresh();
  }

  async function disconnect() {
    if (!props.connectionId) return;
    if (!confirm("Disconnect this account and remove stored credentials?")) return;
    const res = await fetch(`/api/connections/${props.connectionId}/disconnect`, { method: "POST" });
    const data = await res.json();
    setMsg(data.message || data.error);
    router.refresh();
  }

  return (
    <div className="flex flex-col gap-2 text-sm">
      {props.connectPath && props.canConnect ? (
        <a
          href={props.connectPath}
          className="rounded-full bg-[#FF7A24] px-4 py-2 text-center text-[#0A0C12]"
        >
          {props.connectionId ? "Reconnect" : "Connect"}
        </a>
      ) : (
        <span className="rounded-full border border-white/10 px-4 py-2 text-center text-[#5A6E82]">
          Setup required
        </span>
      )}
      {props.connectionId ? (
        <>
          <button onClick={validate} className="rounded-full border border-white/15 px-4 py-2">
            Validate
          </button>
          <button onClick={disconnect} className="rounded-full border border-white/15 px-4 py-2">
            Disconnect
          </button>
        </>
      ) : null}
      {msg ? <span className="max-w-[220px] text-xs text-[#FFC85A]">{msg}</span> : null}
    </div>
  );
}
