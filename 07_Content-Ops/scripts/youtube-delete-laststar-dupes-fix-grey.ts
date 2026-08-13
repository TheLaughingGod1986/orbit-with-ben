/**
 * 2026-08-13: delete 4 Last-Star historical private dupes + refresh grey Short covers.
 * Requires: --execute --allow-emergency-unfreeze --approved-by-user
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve } from "path";
import { execSync } from "child_process";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/private_and_grey_thumbs_2026-08-13");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

/** historical_duplicate_ids from Last Star SHORTS_UPLOAD_INDEX (private holds only) */
const DELETE = [
  { id: "n0s2JzmN1u8", reason: "superseded by Uyi5WtL4GMY (star birth fail)" },
  { id: "arQcxdxTcTo", reason: "superseded by F4mN0abXfa8 (red dwarf)" },
  { id: "2uhUXTSBANw", reason: "superseded by KasDw7SY54M (last star dies)" },
  { id: "jqiZE25gBQc", reason: "superseded by a1O-nCrpbAI (what remains)" },
] as const;

const THUMBS = [
  {
    id: "nAZRIBm5wJw",
    title: "Three Suns",
    cover: resolve(
      ROOT,
      "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/08_Covers/exoplanets_short-03_three-suns_cover_v02.jpg",
    ),
  },
  {
    id: "f8V6wCjWwHA",
    title: "Why Haven't We Found Aliens Yet?",
    cover: resolve(AUD, "covers/f8V6wCjWwHA_cover_v01.jpg"),
    sourceMp4: resolve(
      ROOT,
      "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_punch-p01_where-is-everybody_v03.mp4",
    ),
  },
] as const;

const PROTECTED_SCHEDULE_IDS = [
  "SC2WGTl_V5Q",
  "M-VN84HCNls",
  "nAZRIBm5wJw",
  "tEOHYQbcgOw",
  "OlwENQcY-jg",
  "QRi6Dxq0hz0",
  "03v4f1hlvtQ",
  "b8-X_FyJnHM",
  "tfTkMdE7qqw",
  "bLv0RfidjSg",
  "PcP64way3xA",
  "pjIevt27Svo",
  "AeFm7gWyWik",
  "Uyi5WtL4GMY",
  "F4mN0abXfa8",
  "KasDw7SY54M",
  "a1O-nCrpbAI",
  "dbBojuwg4r8",
  "kFj3vx9WpIw",
];

const PROTECTED_PUBLIC_IDS = [
  "f8V6wCjWwHA",
  "ykmoxRJ6BOI",
  "iQUbmlaj4vk",
  "9ez9BeqGBtE",
  "kBkWtBMKPqE",
  "5-sofIhR0lI",
  "B2STcIAF1lY",
  "tUAdhOnMW2g",
];

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}
function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}
function parseDur(iso: string): number {
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!m) return 0;
  return +(m[1] || 0) * 3600 + +(m[2] || 0) * 60 + +(m[3] || 0);
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

async function getVideos(access: string, ids: string[]) {
  const map = new Map<string, any>();
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const res = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${access}` } },
    );
    const json = await res.json();
    if (!res.ok) throw new Error(JSON.stringify(json));
    for (const it of json.items || []) map.set(it.id, it);
  }
  return map;
}

async function deleteVideo(access: string, id: string) {
  const res = await fetch(`https://www.googleapis.com/youtube/v3/videos?id=${encodeURIComponent(id)}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${access}` },
  });
  if (!res.ok && res.status !== 204) {
    throw new Error(`delete ${id} ${res.status}: ${await res.text()}`);
  }
}

async function setThumb(access: string, id: string, filePath: string) {
  const buf = readFileSync(filePath);
  const res = await fetch(
    `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${encodeURIComponent(id)}`,
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
  if (!res.ok) throw new Error(`thumb ${id} ${res.status}: ${JSON.stringify(body)}`);
  return body;
}

function buildFermiCover(mp4: string, outJpg: string) {
  mkdirSync(resolve(AUD, "covers"), { recursive: true });
  const frame = resolve(AUD, "covers/_fermi_frame.png");
  execSync(
    `ffmpeg -y -ss 2.5 -i ${JSON.stringify(mp4)} -update 1 -frames:v 1 ${JSON.stringify(frame)}`,
    { stdio: "pipe" },
  );
  execSync(
    `ffmpeg -y -i ${JSON.stringify(frame)} -filter_complex "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,gblur=sigma=28,eq=brightness=0.1:saturation=1.25[bg];[0:v]scale=-1:720[fg];[bg][fg]overlay=(W-w)/2:0" -frames:v 1 -q:v 2 ${JSON.stringify(outJpg)}`,
    { stdio: "pipe" },
  );
}

function snapProtected(map: Map<string, any>) {
  const scheduled: Record<string, string | null> = {};
  const publicState: Record<string, string | null> = {};
  for (const id of PROTECTED_SCHEDULE_IDS) {
    const it = map.get(id);
    scheduled[id] = it?.status?.publishAt || (it ? "PRESENT_NO_PUBLISHAT" : null);
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    publicState[id] = map.get(id)?.status?.privacyStatus || null;
  }
  return { scheduled, publicState };
}

async function main() {
  mkdirSync(resolve(AUD, "journal"), { recursive: true });
  const execute = flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  const approved = flag("approved-by-user");
  if (!execute) {
    console.log(JSON.stringify({ ok: true, dryRun: true, delete: DELETE, thumbs: THUMBS.map((t) => t.id) }, null, 2));
    return;
  }
  if (!approved) throw new Error("--approved-by-user required");
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "delete-laststar-dupes-fix-grey-2026-08-13",
  });

  const prisma = new PrismaClient();
  const journal: unknown[] = [];
  try {
    const access = await getAccess(prisma);
    const watch = [
      ...DELETE.map((d) => d.id),
      ...PROTECTED_SCHEDULE_IDS,
      ...PROTECTED_PUBLIC_IDS,
      ...THUMBS.map((t) => t.id),
    ];
    let map = await getVideos(access, watch);
    const baseline = snapProtected(map);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );

    // --- deletes ---
    for (const t of DELETE) {
      console.log(`\n>>> DELETE ${t.id} (${t.reason})`);
      const before = map.get(t.id);
      if (!before) {
        journal.push({ action: "delete", id: t.id, skipped: true, reason: "already missing" });
        console.log("already missing — skip");
        continue;
      }
      if (before.status?.privacyStatus !== "private" || before.status?.publishAt) {
        throw new Error(`gate fail ${t.id}: ${before.status?.privacyStatus} ${before.status?.publishAt}`);
      }
      const dur = parseDur(before.contentDetails?.duration || "");
      if (dur <= 0 || dur > 60) throw new Error(`duration gate ${t.id}: ${dur}`);
      await deleteVideo(access, t.id);
      let gone = false;
      for (let i = 0; i < 8; i++) {
        await sleep(750);
        if (!(await getVideos(access, [t.id])).has(t.id)) {
          gone = true;
          break;
        }
      }
      if (!gone) throw new Error(`still present ${t.id}`);
      const entry = {
        action: "delete",
        id: t.id,
        reason: t.reason,
        title: before.snippet?.title,
        deleted: true,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(resolve(AUD, "journal", `${Date.now()}_${t.id}.json`), JSON.stringify(entry, null, 2));
      console.log(JSON.stringify(entry, null, 2));
      map = await getVideos(access, watch.filter((id) => id !== t.id));
      const afterSnap = snapProtected(map);
      for (const id of PROTECTED_PUBLIC_IDS) {
        if (afterSnap.publicState[id] !== "public") throw new Error(`public drift ${id}`);
      }
      for (const id of ["Uyi5WtL4GMY", "F4mN0abXfa8", "KasDw7SY54M", "a1O-nCrpbAI", "nAZRIBm5wJw"]) {
        if (baseline.scheduled[id] && afterSnap.scheduled[id] !== baseline.scheduled[id]) {
          throw new Error(`schedule drift ${id}`);
        }
      }
      console.log("protected OK");
    }

    // --- thumbs ---
    for (const t of THUMBS) {
      let cover = t.cover;
      if ("sourceMp4" in t && t.sourceMp4) {
        if (!existsSync(t.sourceMp4)) throw new Error(`missing mp4 ${t.sourceMp4}`);
        console.log(`\n>>> BUILD COVER ${t.id}`);
        buildFermiCover(t.sourceMp4, cover);
      }
      if (!existsSync(cover)) throw new Error(`missing cover ${cover}`);
      console.log(`\n>>> THUMB ${t.id}`);
      const body = await setThumb(access, t.id, cover);
      const entry = {
        action: "thumbnails.set",
        id: t.id,
        title: t.title,
        cover,
        etag: (body as any)?.etag || null,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(resolve(AUD, "journal", `${Date.now()}_thumb_${t.id}.json`), JSON.stringify(entry, null, 2));
      console.log(JSON.stringify(entry, null, 2));
    }

    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify(journal, null, 2) + "\n");
    writeFileSync(
      resolve(AUD, "POST_STATE.json"),
      JSON.stringify({ at: new Date().toISOString(), journal }, null, 2) + "\n",
    );
    console.log("\n=== DONE ===");
    console.log(JSON.stringify({ deleted: DELETE.map((d) => d.id), thumbs: THUMBS.map((t) => t.id) }, null, 2));
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
