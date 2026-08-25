#!/usr/bin/env tsx
/**
 * Retitle public Shorts failing the locked kill test (TITLE_THUMBNAIL_FORMULA.md).
 *   npx tsx scripts/_retitle_public_formula_2026-08-25.ts [--apply]
 */
import fs from "fs";
import path from "path";

function loadDotEnv(file: string) {
  if (!fs.existsSync(file)) return;
  for (const raw of fs.readFileSync(file, "utf8").split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const eq = line.indexOf("=");
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let val = line.slice(eq + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (process.env[key] == null) process.env[key] = val;
  }
  if (!process.env.DIRECT_URL && process.env.DATABASE_URL) {
    process.env.DIRECT_URL = process.env.DATABASE_URL;
  }
}
loadDotEnv(path.resolve(process.cwd(), ".env"));

import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

const APPLY = process.argv.includes("--apply");
const OUT = path.resolve(
  __dirname,
  "../../00_Brand/Channel-Setup/audits/channel_review_2026-08-24/RETITLE_PUBLIC_RESULT.json",
);

const UPDATES: Record<string, { title: string; why: string }> = {
  QRi6Dxq0hz0: {
    title: "We Could Smell Alien Life in a Spectrum",
    why: "S1 concrete-weird; was abstract question (26 views)",
  },
  SC2WGTl_V5Q: {
    title: "This Planet's Rain Is Molten Glass",
    why: "S1; strips hashtags; distinct from scheduled glass-rain punch Short",
  },
  ZnsJTCcrTlA: {
    title: "Black Holes Grew Too Big, Too Fast",
    why: "S1 wrongness stated; was abstract question (19 views)",
  },
  iQUbmlaj4vk: {
    title: "A Reply From the Stars Takes Generations",
    why: "S1 concrete; was cute abstraction (17 views)",
  },
  tEOHYQbcgOw: {
    title: "This Planet's Night Never Cools Down",
    why: "S1 drawable; was superlative without subject (16 views)",
  },
  f8V6wCjWwHA: {
    title: "Billions of Planets, Zero Signals",
    why: "S1; strips title hashtags (13 views)",
  },
  ykmoxRJ6BOI: {
    title: "We May Have Already Recorded Alien Life",
    why: "S1 matches desc (archive); strips hashtags (8 views)",
  },
  kBkWtBMKPqE: {
    title: "Falling Into a Black Hole Feels Like Nothing",
    why: "S1+S4 names subject; was subjectless (5 views)",
  },
  "9ez9BeqGBtE": {
    title: "The Event Horizon Is a One-Way Line",
    why: "S1 names subject; was orphan 'this line' + hashtags (4 views)",
  },
  "5-sofIhR0lI": {
    title: "What You'd See Looking Back From a Black Hole",
    why: "S4 experiential; was zero-context (3 views)",
  },
};

async function token() {
  getEnv();
  const c = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  const a = new YouTubePublishingAdapter();
  if (c!.accessTokenExpiresAt && c!.accessTokenExpiresAt.getTime() < Date.now() + 60000) {
    await a.refreshConnection!(c!);
  }
  const f = await prisma.platformConnection.findUnique({ where: { id: c!.id } });
  return decryptSecret(f!.accessTokenEncrypted!);
}

async function main() {
  const t = await token();
  const ids = Object.keys(UPDATES);
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${t}` } },
  );
  const body = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(body).slice(0, 300));
  const results: any[] = [];
  for (const v of body.items || []) {
    const u = UPDATES[v.id];
    console.log(`${APPLY ? "APPLY" : "DRY"} ${v.id}`);
    console.log(`  "${v.snippet.title}"`);
    console.log(`  → "${u.title}"  [${u.title.length}ch] · ${u.why}`);
    if (!APPLY) {
      results.push({ id: v.id, status: "dry", newTitle: u.title });
      continue;
    }
    const put = await fetch("https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
      body: JSON.stringify({ id: v.id, snippet: { ...v.snippet, title: u.title } }),
    });
    const pb = await put.json();
    results.push({
      id: v.id,
      status: put.ok ? "updated" : "error",
      newTitle: u.title,
      error: put.ok ? undefined : JSON.stringify(pb).slice(0, 150),
    });
    await new Promise((r) => setTimeout(r, 400));
  }
  fs.writeFileSync(
    OUT,
    JSON.stringify({ ranAt: new Date().toISOString(), apply: APPLY, results }, null, 2),
  );
  console.log(`\nwritten=${OUT}`);
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
