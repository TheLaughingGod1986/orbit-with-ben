#!/usr/bin/env tsx
/**
 * Retitle scheduled Shorts that fail the locked title kill test
 * (TITLE_THUMBNAIL_FORMULA.md S1–S6). Titles only; descriptions untouched.
 *
 *   npx tsx scripts/_retitle_scheduled_formula_2026-08-25.ts          # dry run
 *   npx tsx scripts/_retitle_scheduled_formula_2026-08-25.ts --apply
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
  "../../00_Brand/Channel-Setup/audits/channel_review_2026-08-24/RETITLE_FORMULA_RESULT.json",
);

// old title → new title (formula S1–S6; ≤50 chars; named subject; no hashtags)
const UPDATES: Record<string, { old: string; title: string; why: string }> = {
  "68uTDP2esso": {
    old: "The Discovery That Doesn't Add Up",
    title: "JWST Keeps Finding Galaxies Too Big, Too Soon",
    why: "S1+S3 — named subject (JWST), wrongness stated; sibling of 89-view winner",
  },
  QptlHs1HuYI: {
    old: "Where Is Everybody? The Fermi Paradox",
    title: "The Galaxy Should Be Crowded — It's Silent",
    why: "S1 — wrongness stated as fact; search phrase stays in description",
  },
  "0j_pgYbCe5E": {
    old: "What Waits at the Far Edge?",
    title: "The Solar System Doesn't End Where You Think",
    why: "S1 — named subject, contradiction; was subjectless question",
  },
  FbRFvSApfOQ: {
    old: "The Ocean We Cannot See",
    title: "Europa Hides More Water Than Every Ocean on Earth",
    why: "S1 — Europa named + killer stat; was subjectless",
  },
  "0eqTVgrlU-s": {
    old: "Life With No Sunlight?",
    title: "Deep-Sea Vents Feed Life With No Sunlight",
    why: "S1 — concrete drawable subject (vents); was vague question",
  },
  "Fv-lSwB_Z-o": {
    old: "Sample an Ocean Without Drilling",
    title: "Europa Sprays Its Ocean Into Space",
    why: "S1 — iconic drawable image (plumes), Europa named",
  },
  TE_HDKAnqms: {
    old: "If Life Can Start Under Ice…",
    title: "If Life Starts Under Ice, It's Everywhere",
    why: "S5 — completes the thought; payoff inside the title",
  },
  Rp_8J6_6IIk: {
    old: "Would Crushing Feel Too Fast?",
    title: "A Neutron Star Crushes You Too Fast to Feel",
    why: "S1+S4 — neutron star named; was subjectless question",
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
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${t}` } },
  );
  const body = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(body).slice(0, 300));

  const results: any[] = [];
  for (const v of body.items || []) {
    const u = UPDATES[v.id];
    const cur = v.snippet.title;
    if (cur === u.title) {
      results.push({ id: v.id, status: "already_done" });
      continue;
    }
    if (cur !== u.old) {
      results.push({ id: v.id, status: "title_drifted_skip", current: cur, expectedOld: u.old });
      console.log(`SKIP ${v.id} — current title differs from expected: "${cur}"`);
      continue;
    }
    if (u.title.length > 100) throw new Error(`title too long ${v.id}`);
    console.log(`${APPLY ? "APPLY" : "DRY"} ${v.id} (${v.status.publishAt})`);
    console.log(`  "${cur}"`);
    console.log(`  → "${u.title}"  [${u.title.length}ch] · ${u.why}`);
    if (!APPLY) {
      results.push({ id: v.id, status: "dry_run", newTitle: u.title });
      continue;
    }
    const put = await fetch("https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
      body: JSON.stringify({ id: v.id, snippet: { ...v.snippet, title: u.title } }),
    });
    const putBody = await put.json();
    results.push({
      id: v.id,
      status: put.ok ? "updated" : "error",
      newTitle: u.title,
      error: put.ok ? undefined : JSON.stringify(putBody).slice(0, 200),
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
