/**
 * Set custom thumbnails for Shorts that show blank/grey covers in Studio.
 * Scoped: thumbnails.set only — no title/desc/visibility/schedule changes.
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const ENV = resolve(__dirname, "../.env");
const AUD =
  process.argv.find((a) => a.startsWith("--aud="))?.slice("--aud=".length) ||
  resolve(ROOT, "00_Brand/Channel-Setup/audits/shorts_blank_thumbs_reapply_2026-08-12");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

const TARGETS = [
  {
    id: "nAZRIBm5wJw",
    title: "Three Suns in the Sky — Real Alien Worlds",
    thumb: resolve(
      ROOT,
      "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/08_Covers/exoplanets_short-03_three-suns_cover_v02.jpg",
    ),
  },
  {
    id: "KcKBixwmcV4",
    title: "Why the First Alien Clue Might Be a Pattern, Not a Signal",
    thumb: resolve(
      ROOT,
      "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/08_Covers/aliens_short-04_hidden-clues_cover_v02.jpg",
    ),
  },
];

async function getAccess(): Promise<string> {
  const prisma = new PrismaClient();
  try {
    const conn = await prisma.platformConnection.findFirst({
      where: {
        platform: "youtube_shorts",
        channelId: "UC_esArsDKd3GJvOkeO0DUog",
        connectionStatus: "connected",
      },
    });
    if (!conn?.accessTokenEncrypted) throw new Error("no token");
    let access = decryptSecret(conn.accessTokenEncrypted);
    const refresh = conn.refreshTokenEncrypted
      ? decryptSecret(conn.refreshTokenEncrypted)
      : null;
    const exp = conn.accessTokenExpiresAt ? new Date(conn.accessTokenExpiresAt).getTime() : 0;
    if (Date.now() >= exp - 60_000) {
      if (!refresh) throw new Error("expired");
      const body = new URLSearchParams({
        client_id: process.env.GOOGLE_CLIENT_ID!,
        client_secret: process.env.GOOGLE_CLIENT_SECRET!,
        refresh_token: refresh,
        grant_type: "refresh_token",
      });
      const res = await fetch("https://oauth2.googleapis.com/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });
      const json = (await res.json()) as { access_token?: string };
      if (!res.ok || !json.access_token) throw new Error(JSON.stringify(json));
      access = json.access_token;
    }
    return access;
  } finally {
    await prisma.$disconnect();
  }
}

async function setThumbnail(access: string, videoId: string, filePath: string) {
  const buf = readFileSync(filePath);
  const res = await fetch(
    `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${encodeURIComponent(videoId)}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${access}`,
        "Content-Type": "image/jpeg",
        "Content-Length": String(buf.length),
      },
      body: buf,
    },
  );
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`thumbnails.set ${res.status}: ${JSON.stringify(body)}`);
  return body;
}

async function main() {
  mkdirSync(AUD, { recursive: true });
  const access = await getAccess();
  const results: unknown[] = [];
  for (const t of TARGETS) {
    if (!existsSync(t.thumb)) throw new Error(`missing thumb ${t.thumb}`);
    console.log(`Setting thumb for ${t.id} …`);
    const body = await setThumbnail(access, t.id, t.thumb);
    results.push({ id: t.id, title: t.title, thumbPath: t.thumb, response: body });
    console.log(`OK ${t.id}`);
  }
  writeFileSync(
    resolve(AUD, "THUMB_SET_RESULT.json"),
    JSON.stringify({ at: new Date().toISOString(), results }, null, 2) + "\n",
  );
  console.log(JSON.stringify(results, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
