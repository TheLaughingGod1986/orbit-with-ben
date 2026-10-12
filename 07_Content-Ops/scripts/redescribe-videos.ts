#!/usr/bin/env tsx
/**
 * Replace one exact passage in the description of listed YouTube ids.
 * Reads the live snippet first and sends it back with only that passage
 * changed, so title, tags, category and languages stay as they are. Does not
 * send status, so privacy and publishAt stay untouched.
 *
 *   npx tsx --env-file=.env scripts/redescribe-videos.ts --file ../05_Analytics/live_fixes/<date>_descriptions.json --dry-run
 *   npx tsx --env-file=.env scripts/redescribe-videos.ts --file ../05_Analytics/live_fixes/<date>_descriptions.json
 *
 * File: { "redescribe": [ { "id": "...", "find": "old passage", "replace": "new passage" } ] }
 */
import { ensureDeskLock } from "./with-desk-lock";
import fs from "fs";
import path from "path";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

type RedescribeRow = {
  id: string;
  find: string;
  replace: string;
};

const WRITABLE_SNIPPET_KEYS = [
  "title",
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

function countOf(haystack: string, needle: string): number {
  return needle ? haystack.split(needle).length - 1 : 0;
}

async function main() {
  const file = arg("file");
  if (!file) {
    console.error("Usage: redescribe-videos.ts --file <json> [--dry-run]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const pack = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  const rows: RedescribeRow[] = pack.redescribe;
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
    const current: string = item.snippet?.description || "";
    const before = {
      title: item.snippet?.title,
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt || null,
    };
    if (countOf(current, row.replace) > 0 && countOf(current, row.find) === 0) {
      results.push({ id: row.id, skipped: "already_fixed", before });
      continue;
    }
    // The passage must appear exactly once, or the description changed since the fix list was written.
    const n = countOf(current, row.find);
    if (n !== 1) {
      results.push({ id: row.id, skipped: n === 0 ? "passage_not_found" : "passage_not_unique", matches: n, before });
      continue;
    }
    const description = current.replace(row.find, row.replace);
    const snippet: Record<string, unknown> = { description };
    for (const key of WRITABLE_SNIPPET_KEYS) {
      if (item.snippet?.[key] !== undefined) snippet[key] = item.snippet[key];
    }
    if (dry) {
      results.push({ id: row.id, dryRun: true, before, find: row.find, replace: row.replace });
      console.log(JSON.stringify({ id: row.id, from: row.find, to: row.replace, dryRun: true }));
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
    const afterDesc: string = a?.snippet?.description || "";
    results.push({
      id: row.id,
      updated: true,
      before,
      after: {
        title: a?.snippet?.title,
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
        hasReplace: afterDesc.includes(row.replace),
        hasFind: afterDesc.includes(row.find),
      },
    });
    console.log(JSON.stringify({ id: row.id, title: a?.snippet?.title, fixed: afterDesc.includes(row.replace) }));
  }

  const out = path.resolve(file.replace(/\.json$/, "") + "_RESULT.json");
  fs.writeFileSync(out, JSON.stringify({ dry, finishedAt: new Date().toISOString(), results }, null, 2) + "\n");
  console.log(JSON.stringify({ wrote: out, n: results.length, dry }, null, 2));
}

ensureDeskLock();

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
