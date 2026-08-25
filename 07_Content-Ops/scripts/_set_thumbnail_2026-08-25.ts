#!/usr/bin/env tsx
/**
 * Set a video thumbnail via the Data API.
 *   npx tsx scripts/_set_thumbnail_2026-08-25.ts <videoId> <imagePath> [<videoId> <imagePath> ...]
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
  const args = process.argv.slice(2);
  if (args.length < 2 || args.length % 2 !== 0) {
    throw new Error("usage: <videoId> <imagePath> [pairs...]");
  }
  const t = await token();
  for (let i = 0; i < args.length; i += 2) {
    const [id, img] = [args[i], args[i + 1]];
    const bytes = fs.readFileSync(img);
    if (bytes.length > 2 * 1024 * 1024) throw new Error(`${img} over 2MB`);
    const mime = img.endsWith(".png") ? "image/png" : "image/jpeg";
    const res = await fetch(
      `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${id}`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${t}`, "Content-Type": mime },
        body: bytes,
      },
    );
    const body = await res.json();
    console.log(id, res.ok ? "THUMB SET ok" : `ERROR: ${JSON.stringify(body).slice(0, 200)}`);
    await new Promise((r) => setTimeout(r, 500));
  }
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
