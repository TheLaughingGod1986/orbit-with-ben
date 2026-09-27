#!/usr/bin/env tsx
/**
 * Change only the title on listed YouTube ids.
 * Reads the live snippet first and sends it back with the new title, so
 * description, tags, category and languages stay as they are. Does not
 * send status, so privacy and publishAt stay untouched.
 *
 *   npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json --dry-run
 *   npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json
 */
import fs from "fs";
import path from "path";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

type RetitleRow = {
  id: string;
  expectCurrentTitle: string;
  title: string;
};

const WRITABLE_SNIPPET_KEYS = [
  "description",
  "tags",
  "categoryId",
  "defaultLanguage",
  "defaultAudioLanguage",
] as const;

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init?.headers || {}) },
  });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 400)}`);
  return body;
}

async function main() {
  const file = arg("file");
  if (!file) {
    console.error("Usage: retitle-videos.ts --file <json> [--dry-run]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const pack = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  const rows: RetitleRow[] = pack.retitle;
  const token = await getYouTubeAccessToken();
  const results: unknown[] = [];

  for (const row of rows) {
    const got = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const item = got.items?.[0];
    if (!item) {
      results.push({ id: row.id, error: "not_found" });
      continue;
    }
    const current: string = item.snippet?.title || "";
    const before = {
      title: current,
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt || null,
    };
    if (current === row.title) {
      results.push({ id: row.id, skipped: "already_titled", before });
      continue;
    }
    // Someone changed the title since the fix list was written — do not overwrite their choice.
    if (current !== row.expectCurrentTitle) {
      results.push({ id: row.id, skipped: "title_changed_since_audit", before, expected: row.expectCurrentTitle });
      continue;
    }
    const snippet: Record<string, unknown> = { title: row.title };
    for (const key of WRITABLE_SNIPPET_KEYS) {
      if (item.snippet?.[key] !== undefined) snippet[key] = item.snippet[key];
    }
    if (dry) {
      results.push({ id: row.id, dryRun: true, before, nextTitle: row.title });
      console.log(JSON.stringify({ id: row.id, from: current, to: row.title, dryRun: true }));
      continue;
    }
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: row.id, snippet }),
    });
    const after = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const a = after.items?.[0];
    results.push({
      id: row.id,
      updated: true,
      before,
      after: {
        title: a?.snippet?.title,
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
      },
    });
    console.log(JSON.stringify({ id: row.id, title: a?.snippet?.title, publishAt: a?.status?.publishAt || null }));
  }

  const out = path.resolve(file.replace(/\.json$/, "") + "_RESULT.json");
  fs.writeFileSync(out, JSON.stringify({ dry, finishedAt: new Date().toISOString(), results }, null, 2) + "\n");
  console.log(JSON.stringify({ wrote: out, n: results.length, dry }, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
