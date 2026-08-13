/**
 * 2026-08-13: rebuild brighter Short covers + re-set via API (Studio mobile grey list).
 * Targets: Three Suns, Fermi punch, Giant Eye.
 * Requires: --execute [--allow-emergency-unfreeze]
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync } from "fs";
import { resolve, basename } from "path";
import { execFileSync } from "child_process";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/grey_studio_thumbs_2026-08-13");
const ENV = resolve(__dirname, "../.env");

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
    mp4: resolve(
      ROOT,
      "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/06_Final-Exports/exoplanets_short-03_three-suns_retention_v2.mp4",
    ),
    ss: "4.0",
    coverName: "nAZRIBm5wJw_cover_v03.jpg",
    alsoCopyTo: resolve(
      ROOT,
      "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/08_Covers/exoplanets_short-03_three-suns_cover_v03.jpg",
    ),
  },
  {
    id: "f8V6wCjWwHA",
    title: "Why Haven't We Found Aliens Yet?",
    mp4: resolve(
      ROOT,
      "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_punch-p01_where-is-everybody_v03.mp4",
    ),
    ss: "10.0",
    coverName: "f8V6wCjWwHA_cover_v03.jpg",
  },
  {
    id: "OlwENQcY-jg",
    title: "Why This Alien World Looks Like a Giant Eye",
    mp4: resolve(
      ROOT,
      "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/06_Final-Exports/exoplanets_short-05_eyeball_retention_v2.mp4",
    ),
    ss: "10.0",
    coverName: "OlwENQcY-jg_cover_v03.jpg",
  },
] as const;

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}

async function getAccess(prisma: PrismaClient): Promise<string> {
  const conn = await prisma.platformConnection.findFirst({
    where: {
      platform: "youtube_shorts",
      channelId: "UC_esArsDKd3GJvOkeO0DUog",
      connectionStatus: "connected",
    },
  });
  if (!conn?.accessTokenEncrypted) throw new Error("no token");
  let access = decryptSecret(conn.accessTokenEncrypted);
  const refresh = conn.refreshTokenEncrypted ? decryptSecret(conn.refreshTokenEncrypted) : null;
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
}

/** 9:16 frame → bright 1280×720 with colour-matched blur wings (no flat grey pillarbox). */
function buildCover(mp4: string, ss: string, outJpg: string) {
  mkdirSync(resolve(AUD, "covers"), { recursive: true });
  const frame = outJpg.replace(/\.jpg$/i, "_frame.png");
  execFileSync(
    "ffmpeg",
    ["-y", "-ss", ss, "-i", mp4, "-frames:v", "1", "-update", "1", frame],
    { stdio: "pipe" },
  );
  // brighter / more saturated fill so Studio list cells don't read as solid grey
  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-i",
      frame,
      "-filter_complex",
      [
        "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,",
        "gblur=sigma=32,eq=brightness=0.18:saturation=1.35:contrast=1.08[bg];",
        "[0:v]scale=-2:720,eq=brightness=0.08:saturation=1.2:contrast=1.05[fg];",
        "[bg][fg]overlay=(W-w)/2:(H-h)/2",
      ].join(""),
      "-frames:v",
      "1",
      "-q:v",
      "2",
      outJpg,
    ],
    { stdio: "pipe" },
  );
}

async function setThumbMultipart(access: string, videoId: string, filePath: string) {
  const buf = readFileSync(filePath);
  const boundary = `orbit_thumb_${Date.now()}`;
  const name = basename(filePath);
  const preamble =
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="media"; filename="${name}"\r\n` +
    `Content-Type: image/jpeg\r\n\r\n`;
  const epilogue = `\r\n--${boundary}--\r\n`;
  const body = Buffer.concat([Buffer.from(preamble, "utf8"), buf, Buffer.from(epilogue, "utf8")]);

  const res = await fetch(
    `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${encodeURIComponent(videoId)}&uploadType=multipart`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${access}`,
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
        "Content-Length": String(body.length),
      },
      body,
    },
  );
  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const res2 = await fetch(
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
    const json2 = await res2.json().catch(() => ({}));
    if (!res2.ok) {
      throw new Error(
        `thumbnails.set ${res.status}/${res2.status}: ${JSON.stringify(json)} / ${JSON.stringify(json2)}`,
      );
    }
    return { via: "simple", body: json2, bytes: buf.length };
  }
  return { via: "multipart", body: json, bytes: buf.length };
}

async function getVideo(access: string, id: string) {
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id=${id}`,
    { headers: { Authorization: `Bearer ${access}` } },
  );
  const json = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(json));
  return (json.items || [])[0] || null;
}

async function main() {
  mkdirSync(resolve(AUD, "covers"), { recursive: true });
  mkdirSync(resolve(AUD, "journal"), { recursive: true });
  const execute = flag("execute");
  const allow = flag("allow-emergency-unfreeze");

  // Always build covers (local only) so Studio CDP can use them even on dry-run preview
  const built: { id: string; cover: string; title: string }[] = [];
  for (const t of TARGETS) {
    if (!existsSync(t.mp4)) throw new Error(`missing mp4 ${t.mp4}`);
    const cover = resolve(AUD, "covers", t.coverName);
    console.log(`BUILD ${t.id} ss=${t.ss}`);
    buildCover(t.mp4, t.ss, cover);
    if ("alsoCopyTo" in t && t.alsoCopyTo) {
      mkdirSync(resolve(t.alsoCopyTo, ".."), { recursive: true });
      copyFileSync(cover, t.alsoCopyTo);
    }
    built.push({ id: t.id, cover, title: t.title });
  }
  writeFileSync(
    resolve(AUD, "COVERS_BUILT.json"),
    JSON.stringify({ at: new Date().toISOString(), built }, null, 2) + "\n",
  );

  if (!execute) {
    console.log(JSON.stringify({ ok: true, dryRun: true, built }, null, 2));
    return;
  }

  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "fix-grey-studio-thumbs-2026-08-13",
  });

  const prisma = new PrismaClient();
  const journal: unknown[] = [];
  try {
    const access = await getAccess(prisma);
    for (const t of built) {
      console.log(`\n>>> THUMB ${t.id}`);
      const before = await getVideo(access, t.id);
      const out = await setThumbMultipart(access, t.id, t.cover);
      await new Promise((r) => setTimeout(r, 800));
      const after = await getVideo(access, t.id);
      const entry = {
        action: "thumbnails.set",
        id: t.id,
        title: t.title,
        cover: t.cover,
        via: out.via,
        bytes: out.bytes,
        etag: (out.body as any)?.etag || null,
        beforeMaxres: before?.snippet?.thumbnails?.maxres?.url || null,
        afterMaxres: after?.snippet?.thumbnails?.maxres?.url || null,
        privacy: after?.status?.privacyStatus || null,
        publishAt: after?.status?.publishAt || null,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(
        resolve(AUD, "journal", `${Date.now()}_${t.id}.json`),
        JSON.stringify(entry, null, 2) + "\n",
      );
      console.log(JSON.stringify(entry, null, 2));
    }
    writeFileSync(
      resolve(AUD, "MUTATION_JOURNAL.json"),
      JSON.stringify(journal, null, 2) + "\n",
    );
    console.log("\n=== API DONE ===");
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
