#!/usr/bin/env tsx
/** READ-ONLY: fresh title + desc snippet for scheduled Shorts (title audit). */
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

const IDS = [
  "68uTDP2esso",
  "QptlHs1HuYI",
  "Q16DKNvq2OY",
  "oN_jm9PTDOQ",
  "0j_pgYbCe5E",
  "FbRFvSApfOQ",
  "0eqTVgrlU-s",
  "Fv-lSwB_Z-o",
  "TE_HDKAnqms",
  "Rp_8J6_6IIk",
];

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
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${IDS.join(",")}`,
    { headers: { Authorization: `Bearer ${t}` } },
  );
  const body = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(body).slice(0, 300));
  for (const v of body.items || []) {
    console.log(`=== ${v.id} · publishAt=${v.status.publishAt || "?"}`);
    console.log(`TITLE: ${v.snippet.title}`);
    console.log(`DESC: ${(v.snippet.description || "").split("\n").slice(0, 2).join(" ¶ ").slice(0, 180)}`);
  }
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
