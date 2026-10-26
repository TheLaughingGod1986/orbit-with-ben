#!/usr/bin/env tsx
/**
 * Read-only check that closes a Short swap job: the old copy must be Private with NO publishAt and the new copy
 * Private + scheduled. Writes jobs/readbacks/<job>.json, which `scripts/jobs.py done` requires for swap jobs.
 * Exits 1 when the old copy is still scheduled (26 Oct 2026: four swaps closed with both copies on one slot).
 *
 *   npx tsx --env-file=.env scripts/verify-swap.ts --job J0940 --old dM1OgGPAYvw --new OVLv9dxTcpE
 */
import fs from "fs";
import path from "path";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

const ORBIT_CHANNEL_ID = "UC_esArsDKd3GJvOkeO0DUog";

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  return idx === -1 ? undefined : process.argv[idx + 1];
}

type Item = { id: string; snippet?: Record<string, unknown>; status?: Record<string, unknown> };

export type CopyState = {
  id: string;
  found: boolean;
  title: string | null;
  channelId: string | null;
  privacyStatus: string | null;
  publishAt: string | null;
};

function state(item: Item | undefined, id: string): CopyState {
  if (!item) return { id, found: false, privacyStatus: null, publishAt: null, title: null, channelId: null };
  return {
    id,
    found: true,
    title: (item.snippet?.title as string) ?? null,
    channelId: (item.snippet?.channelId as string) ?? null,
    privacyStatus: (item.status?.privacyStatus as string) ?? null,
    publishAt: (item.status?.publishAt as string) ?? null,
  };
}

export function verdict(old: CopyState, neu: CopyState): string[] {
  const problems: string[] = [];
  for (const v of [old, neu]) {
    if (!v.found) problems.push(`${v.id}: not found`);
    else if (v.channelId !== ORBIT_CHANNEL_ID) problems.push(`${v.id}: not on the Orbit channel`);
  }
  if (old.privacyStatus !== "private" || old.publishAt) {
    problems.push(`old ${old.id}: ${old.privacyStatus} publishAt ${old.publishAt}; must be private and unscheduled`);
  }
  if (neu.privacyStatus !== "private" || !neu.publishAt) {
    problems.push(`new ${neu.id}: ${neu.privacyStatus} publishAt ${neu.publishAt}; must be private and scheduled`);
  }
  return problems;
}

async function main() {
  const job = arg("job");
  const oldId = arg("old");
  const newId = arg("new");
  if (!job || !oldId || !newId) {
    console.error("Usage: verify-swap.ts --job J0940 --old <old id> --new <new id>");
    process.exit(2);
  }
  const token = await getYouTubeAccessToken();
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(`${oldId},${newId}`)}`,
    { headers: { Authorization: `Bearer ${token}` } },
  );
  const body = (await res.json()) as { items?: Item[] };
  if (!res.ok) throw new Error(`${res.status} ${JSON.stringify(body).slice(0, 300)}`);
  const byId = new Map((body.items || []).map((i) => [i.id, i]));
  const old = state(byId.get(oldId), oldId);
  const neu = state(byId.get(newId), newId);
  const problems = verdict(old, neu);
  const report = { job, at: new Date().toISOString(), ok: problems.length === 0, old, new: neu, problems };
  if (report.ok) {
    const dir = path.resolve(process.cwd(), "../jobs/readbacks"); // run from 07_Content-Ops
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, `${job}.json`), JSON.stringify(report, null, 2) + "\n");
  }
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.ok ? 0 : 1);
}

if (process.argv[1]?.endsWith("verify-swap.ts")) {
  main().catch((err) => {
    console.error(err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
}
