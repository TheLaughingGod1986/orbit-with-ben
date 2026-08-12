/**
 * Aug 19 gap: formerly-public Zoo Short (rFJoOdQAc9c) cannot take publishAt
 * via API. Re-upload v02 as a NEW private+scheduled video for 19 Aug 11:30 UK.
 *
 * Requires: --execute --allow-emergency-unfreeze --approved-by-user
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync, statSync, existsSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/schedule_aug19_zoo_2026-08-12");
const ENV = resolve(__dirname, "../.env");
const FILE = resolve(
  ROOT,
  "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-03_zoo-hypothesis_v02.mp4",
);

const PUBLISH_AT = "2026-08-19T10:30:00Z"; // 11:30 UK BST
const OLD_ID = "rFJoOdQAc9c";
const PARENT_LONG = "Mo93x0fxB1Q";

const META = {
  title: "Don't Look Up: The Zoo Hypothesis #Shorts #Aliens #Science",
  description:
    "The zoo hypothesis imagines advanced civilisations observing younger worlds while deliberately avoiding contact — science, not fearbait.\n\nThis is one moment from the full documentary.\nWatch the full film:\nhttps://youtu.be/Mo93x0fxB1Q\n\n#Aliens #SpaceMystery #FermiParadox #Shorts #OrbitWithBen",
  tags: [
    "zoo hypothesis",
    "what if aliens are watching us",
    "alien life",
    "extraterrestrial life",
    "fermi paradox",
    "space shorts",
    "orbit with ben",
    "astronomy shorts",
    "are we alone",
    "SETI",
    "will we ever meet aliens",
    "space documentary",
    "zoo hypothesis explained",
    "fermi paradox explained",
  ],
};

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

const PROTECTED_SCHEDULE_IDS = [
  "SC2WGTl_V5Q",
  "M-VN84HCNls",
  "nAZRIBm5wJw",
  "tEOHYQbcgOw",
  "OlwENQcY-jg",
  "QRi6Dxq0hz0",
  "b8-X_FyJnHM",
  "tfTkMdE7qqw",
  "bLv0RfidjSg",
  "PcP64way3xA",
  "pjIevt27Svo",
  "AeFm7gWyWik",
];

const PROTECTED_PUBLIC_IDS = [
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
  "tUAdhOnMW2g",
  "svYOx07OrIM",
  "B2STcIAF1lY",
];

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
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
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${access}` } },
    );
    const json = await res.json();
    if (!res.ok) throw new Error(JSON.stringify(json));
    for (const it of json.items || []) map.set(it.id, it);
  }
  return map;
}

async function uploadScheduledPrivate(access: string) {
  if (!existsSync(FILE)) throw new Error(`missing ${FILE}`);
  const size = statSync(FILE).size;
  const initUrl = new URL("https://www.googleapis.com/upload/youtube/v3/videos");
  initUrl.searchParams.set("uploadType", "resumable");
  initUrl.searchParams.set("part", "snippet,status");
  initUrl.searchParams.set("notifySubscribers", "false");
  const metaRes = await fetch(initUrl.toString(), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${access}`,
      "Content-Type": "application/json; charset=UTF-8",
      "X-Upload-Content-Type": "video/mp4",
      "X-Upload-Content-Length": String(size),
    },
    body: JSON.stringify({
      snippet: {
        title: META.title.slice(0, 100),
        description: META.description,
        categoryId: "27",
        tags: META.tags,
        defaultLanguage: "en",
        defaultAudioLanguage: "en-GB",
      },
      status: {
        privacyStatus: "private",
        publishAt: PUBLISH_AT,
        selfDeclaredMadeForKids: false,
      },
    }),
  });
  if (!metaRes.ok) throw new Error(`upload init ${metaRes.status}: ${await metaRes.text()}`);
  const uploadUrl = metaRes.headers.get("location");
  if (!uploadUrl) throw new Error("No resumable upload URL");
  console.log(`Uploading ${(size / 1e6).toFixed(1)} MB…`);
  const fileBuf = readFileSync(FILE);
  const uploadRes = await fetch(uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": "video/mp4", "Content-Length": String(fileBuf.length) },
    body: fileBuf,
  });
  const uploadBody = await uploadRes.json().catch(() => ({}));
  if (!uploadRes.ok || !uploadBody.id) {
    throw new Error(`upload put ${uploadRes.status}: ${JSON.stringify(uploadBody)}`);
  }
  return uploadBody as { id: string; status?: any; snippet?: any };
}

function snapProtected(map: Map<string, any>) {
  const scheduled: Record<string, string | null> = {};
  const publicState: Record<string, string | null> = {};
  for (const id of PROTECTED_SCHEDULE_IDS) {
    scheduled[id] = map.get(id)?.status?.publishAt || null;
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    publicState[id] = map.get(id)?.status?.privacyStatus || null;
  }
  return { scheduled, publicState };
}

function assertProtectedUnchanged(
  before: ReturnType<typeof snapProtected>,
  after: ReturnType<typeof snapProtected>,
) {
  for (const id of PROTECTED_SCHEDULE_IDS) {
    if (before.scheduled[id] !== after.scheduled[id]) {
      throw new Error(`PROTECTED SCHEDULE DRIFT ${id}`);
    }
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    if (after.publicState[id] !== "public") {
      throw new Error(`PROTECTED PUBLIC DRIFT ${id}: ${after.publicState[id]}`);
    }
  }
}

async function main() {
  mkdirSync(resolve(AUD, "journal"), { recursive: true });
  const execute = flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  const approved = flag("approved-by-user");
  if (!execute) {
    console.log(JSON.stringify({ ok: true, dryRun: true, publishAt: PUBLISH_AT, file: FILE }, null, 2));
    return;
  }
  if (!approved) throw new Error("Execution requires --approved-by-user");
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "reupload-schedule-aug19-zoo-2026-08-12",
  });

  const prisma = new PrismaClient();
  try {
    const access = await getAccess(prisma);
    const watchIds = [...PROTECTED_SCHEDULE_IDS, ...PROTECTED_PUBLIC_IDS, OLD_ID];
    const beforeMap = await getVideos(access, watchIds);
    const baseline = snapProtected(beforeMap);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );
    const occupied = new Set(Object.values(baseline.scheduled).filter(Boolean));
    if (occupied.has(PUBLISH_AT)) throw new Error(`collision ${PUBLISH_AT}`);

    console.log("\n>>> REUPLOAD + SCHEDULE Zoo for", PUBLISH_AT);
    const uploaded = await uploadScheduledPrivate(access);
    const newId = uploaded.id;
    console.log("new id", newId);

    // verify schedule sticks (processing may delay status)
    let live: any = null;
    for (let attempt = 1; attempt <= 12; attempt++) {
      await sleep(2000);
      live = (await getVideos(access, [newId])).get(newId);
      if (
        live?.status?.privacyStatus === "private" &&
        live?.status?.publishAt === PUBLISH_AT
      ) {
        break;
      }
    }
    const ok =
      live?.status?.privacyStatus === "private" && live?.status?.publishAt === PUBLISH_AT;
    const entry = {
      action: "reupload_schedule",
      oldId: OLD_ID,
      newId,
      publishAt: PUBLISH_AT,
      parentLong: PARENT_LONG,
      file: FILE,
      after: {
        privacy: live?.status?.privacyStatus || null,
        publishAt: live?.status?.publishAt || null,
        title: live?.snippet?.title || null,
      },
      ok,
      at: new Date().toISOString(),
      studioEdit: `https://studio.youtube.com/video/${newId}/edit`,
    };
    writeFileSync(resolve(AUD, "journal", `${Date.now()}_${newId}.json`), JSON.stringify(entry, null, 2));
    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify([entry], null, 2) + "\n");
    console.log(JSON.stringify(entry, null, 2));
    if (!ok) throw new Error(`schedule verify failed for ${newId}: ${JSON.stringify(entry.after)}`);

    const afterMap = await getVideos(access, [...watchIds, newId]);
    assertProtectedUnchanged(baseline, snapProtected(afterMap));
    // old Zoo must remain private unscheduled
    const old = afterMap.get(OLD_ID);
    if (old?.status?.privacyStatus !== "private" || old?.status?.publishAt) {
      throw new Error(`old Zoo drifted: ${JSON.stringify(old?.status)}`);
    }

    writeFileSync(
      resolve(AUD, "POST_STATE.json"),
      JSON.stringify(
        {
          at: new Date().toISOString(),
          entry,
          protected: snapProtected(afterMap),
          oldZoo: {
            id: OLD_ID,
            privacy: old?.status?.privacyStatus,
            publishAt: old?.status?.publishAt || null,
          },
        },
        null,
        2,
      ) + "\n",
    );
    console.log("\n=== AUG 19 ZOO REUPLOAD SCHEDULED ===");
    console.log(
      JSON.stringify(
        {
          newId,
          publishAt: PUBLISH_AT,
          uk: "Wed 19 Aug 2026 11:30",
          studioEdit: entry.studioEdit,
        },
        null,
        2,
      ),
    );
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
