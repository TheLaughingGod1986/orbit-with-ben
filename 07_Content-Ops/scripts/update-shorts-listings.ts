#!/usr/bin/env tsx
/**
 * Update scheduled Shorts title/description/tags via YouTube Data API.
 * Does NOT send status — privacy and publishAt stay untouched.
 *
 *   npx tsx scripts/update-shorts-listings.ts --file ../00_Brand/Channel-Setup/audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json
 *   npx tsx scripts/update-shorts-listings.ts --file ... --dry-run
 */
import { ensureDeskLock } from "./with-desk-lock";
import fs from "fs";
import path from "path";
import { getYouTubeAccessToken } from "../src/lib/youtube/data-api";

type ShortRow = {
  id: string;
  title: string;
  description: string;
  tags: string[];
};

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function packTags(tags: string[], limit = 490): string[] {
  const out: string[] = [];
  let used = 0;
  const seen = new Set<string>();
  for (const raw of tags) {
    const t = raw.trim().replace(/\s+/g, " ");
    if (!t || seen.has(t.toLowerCase())) continue;
    const extra = t.length + (out.length ? 1 : 0);
    if (used + extra > limit) continue;
    seen.add(t.toLowerCase());
    out.push(t);
    used += extra;
  }
  return out;
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
    console.error("Usage: update-shorts-listings.ts --file <json> [--dry-run]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const pack = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  const shorts: ShortRow[] = pack.shorts;
  const token = await getYouTubeAccessToken();
  const results: unknown[] = [];

  for (const row of shorts) {
    const got = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const item = got.items?.[0];
    if (!item) {
      results.push({ id: row.id, error: "not_found" });
      continue;
    }
    const before = {
      title: item.snippet?.title,
      description: (item.snippet?.description || "").slice(0, 180),
      tags: item.snippet?.tags || [],
      tagChars: (item.snippet?.tags || []).join(",").length,
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt || null,
    };
    const tags = packTags(row.tags);
    const snippet = {
      title: row.title,
      description: row.description,
      tags,
      categoryId: item.snippet?.categoryId || "28",
      defaultLanguage: item.snippet?.defaultLanguage || "en-GB",
    };
    if (item.snippet?.defaultAudioLanguage) {
      (snippet as { defaultAudioLanguage?: string }).defaultAudioLanguage = item.snippet.defaultAudioLanguage;
    }
    const payload = { id: row.id, snippet };
    if (dry) {
      results.push({ id: row.id, dryRun: true, before, nextTitle: row.title, nextTagChars: tags.join(",").length });
      continue;
    }
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
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
        tagChars: (a?.snippet?.tags || []).join(",").length,
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
      },
    });
    console.log(JSON.stringify({ id: row.id, title: a?.snippet?.title, publishAt: a?.status?.publishAt || null }, null, 0));
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
