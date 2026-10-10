#!/usr/bin/env tsx
/**
 * Make listed Orbit video ids Private. Never deletes.
 * Sends part=status only, copying the writable status fields already on the
 * video (kids flag, embed, license, synthetic media) so only privacy changes.
 * Refuses any id that isn't on the Orbit channel.
 *
 *   npx tsx --env-file=.env scripts/set-private.ts --ids id1,id2 --dry-run
 *   npx tsx --env-file=.env scripts/set-private.ts --ids id1,id2 --out <result.json>
 */
import fs from "fs";
import path from "path";
import { ensureDeskLock } from "./with-desk-lock";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

const ORBIT_CHANNEL_ID = "UC_esArsDKd3GJvOkeO0DUog";

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  const text = await res.text();
  let body: unknown = text;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text.slice(0, 400) };
  }
  if (!res.ok) throw new Error(`${res.status} ${JSON.stringify(body).slice(0, 500)}`);
  return body as { items?: Array<Record<string, unknown>> };
}

function snapshot(item: Record<string, unknown>) {
  const snippet = (item.snippet || {}) as Record<string, unknown>;
  const status = (item.status || {}) as Record<string, unknown>;
  return {
    title: snippet.title ?? null,
    channelId: snippet.channelId ?? null,
    channelTitle: snippet.channelTitle ?? null,
    privacyStatus: status.privacyStatus ?? null,
    publishAt: status.publishAt ?? null,
    selfDeclaredMadeForKids: status.selfDeclaredMadeForKids ?? null,
    madeForKids: status.madeForKids ?? null,
    containsSyntheticMedia: status.containsSyntheticMedia ?? null,
    embeddable: status.embeddable ?? null,
    license: status.license ?? null,
    publicStatsViewable: status.publicStatsViewable ?? null,
  };
}

function privateStatus(status: Record<string, unknown>) {
  const out: Record<string, unknown> = { privacyStatus: "private" };
  if (typeof status.license === "string") out.license = status.license;
  if (typeof status.embeddable === "boolean") out.embeddable = status.embeddable;
  if (typeof status.publicStatsViewable === "boolean") out.publicStatsViewable = status.publicStatsViewable;
  if (typeof status.containsSyntheticMedia === "boolean") out.containsSyntheticMedia = status.containsSyntheticMedia;
  if (typeof status.selfDeclaredMadeForKids === "boolean") {
    out.selfDeclaredMadeForKids = status.selfDeclaredMadeForKids;
  } else if (typeof status.madeForKids === "boolean") {
    out.selfDeclaredMadeForKids = status.madeForKids;
  }
  return out;
}

async function main() {
  const ids = (arg("ids") || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  if (!ids.length) {
    console.error("Usage: set-private.ts --ids id1,id2 [--dry-run] [--out result.json]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const token = await getYouTubeAccessToken();
  const results: unknown[] = [];
  const get = async (id: string) =>
    (await yt(token, `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(id)}`))
      .items?.[0];

  for (const id of ids) {
    const item = await get(id);
    if (!item) {
      results.push({ id, error: "not_found" });
      continue;
    }
    const before = snapshot(item);
    if (before.channelId !== ORBIT_CHANNEL_ID) {
      results.push({ id, error: "not_orbit_channel", before });
      continue;
    }
    if (before.privacyStatus === "private") {
      results.push({ id, action: "already_private", before });
      continue;
    }
    const sent = privateStatus((item.status || {}) as Record<string, unknown>);
    if (dry) {
      results.push({ id, action: "dry_run", before, wouldSend: sent });
      continue;
    }
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=status", {
      method: "PUT",
      body: JSON.stringify({ id, status: sent }),
    });
    const afterItem = await get(id);
    const after = afterItem ? snapshot(afterItem) : null;
    results.push({ id, action: "set_private", sent, before, after, titleUnchanged: after?.title === before.title });
  }

  const report = { dry, finishedAt: new Date().toISOString(), results };
  const out = arg("out");
  if (out) fs.writeFileSync(path.resolve(out), JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report, null, 2));
}

ensureDeskLock();

main().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
