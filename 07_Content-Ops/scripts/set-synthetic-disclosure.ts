#!/usr/bin/env tsx
/**
 * Set YouTube status.containsSyntheticMedia=true on listed video ids.
 * Sends part=status only. Copies the writable status fields already on
 * the video (privacy, publishAt, kids flag, embed, license) and does not
 * send snippet, so title, description, and schedule stay as they are.
 *
 *   npx tsx scripts/set-synthetic-disclosure.ts --ids id1,id2
 */
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

const IDS = [
  "_WQLVnLETYA",
  "4P9v_2jx7Yo",
  "i6KGk9Z3pIE",
  "G8DiaNjD2WE",
  "Ih2zhZTbIR0",
  "pL339HhjDwo",
];

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
  if (!res.ok) {
    throw new Error(`${res.status} ${JSON.stringify(body).slice(0, 500)}`);
  }
  return body as { items?: Array<Record<string, unknown>> };
}

function snapshot(item: Record<string, unknown>) {
  const snippet = (item.snippet || {}) as Record<string, unknown>;
  const status = (item.status || {}) as Record<string, unknown>;
  return {
    title: snippet.title ?? null,
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

function writableStatus(status: Record<string, unknown>) {
  const out: Record<string, unknown> = {
    containsSyntheticMedia: true,
  };
  if (typeof status.privacyStatus === "string") out.privacyStatus = status.privacyStatus;
  if (typeof status.publishAt === "string" && status.publishAt) out.publishAt = status.publishAt;
  if (typeof status.license === "string") out.license = status.license;
  if (typeof status.embeddable === "boolean") out.embeddable = status.embeddable;
  if (typeof status.publicStatsViewable === "boolean") {
    out.publicStatsViewable = status.publicStatsViewable;
  }
  if (typeof status.selfDeclaredMadeForKids === "boolean") {
    out.selfDeclaredMadeForKids = status.selfDeclaredMadeForKids;
  } else if (typeof status.madeForKids === "boolean") {
    out.selfDeclaredMadeForKids = status.madeForKids;
  }
  return out;
}

async function main() {
  const ids = (arg("ids") || IDS.join(","))
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const token = await getYouTubeAccessToken();
  const results: unknown[] = [];

  for (const id of ids) {
    const got = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(id)}`,
    );
    const item = got.items?.[0];
    if (!item) {
      results.push({ id, error: "not_found" });
      continue;
    }
    const before = snapshot(item);
    const status = (item.status || {}) as Record<string, unknown>;
    if (status.containsSyntheticMedia === true) {
      results.push({ id, action: "already_true", before });
      continue;
    }
    const nextStatus = writableStatus(status);
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=status", {
      method: "PUT",
      body: JSON.stringify({ id, status: nextStatus }),
    });
    const again = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(id)}`,
    );
    const afterItem = again.items?.[0];
    const after = afterItem ? snapshot(afterItem) : null;
    const unchanged =
      after &&
      after.title === before.title &&
      after.privacyStatus === before.privacyStatus &&
      after.publishAt === before.publishAt;
    results.push({
      id,
      action: "set_true",
      sent: nextStatus,
      before,
      after,
      titlePrivacyScheduleUnchanged: unchanged,
    });
  }

  console.log(JSON.stringify(results, null, 2));
}

main().catch(async (err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
