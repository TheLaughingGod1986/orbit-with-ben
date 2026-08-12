/**
 * User-approved 2026-08-12: fill remaining 19 Aug gap before JWST long.
 * Schedule Zoo Hypothesis (rFJoOdQAc9c) at 11:30 UK.
 *
 * Requires: --execute --allow-emergency-unfreeze --approved-by-user
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/schedule_aug19_zoo_2026-08-12");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

const TARGET = {
  id: "rFJoOdQAc9c",
  publishAt: "2026-08-19T10:30:00Z", // 11:30 UK BST
  title: "Don't Look Up: The Zoo Hypothesis",
} as const;

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

function baseWritable(prior: any) {
  return {
    privacyStatus: "private" as string,
    license: prior?.license || "youtube",
    embeddable: prior?.embeddable !== false,
    publicStatsViewable: prior?.publicStatsViewable !== false,
    selfDeclaredMadeForKids: prior?.selfDeclaredMadeForKids === true,
  };
}

async function updateStatus(access: string, id: string, status: Record<string, unknown>) {
  const res = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${access}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id, status }),
  });
  const body = await res.json().catch(() => ({}));
  return { ok: res.ok, statusCode: res.status, body };
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
      throw new Error(
        `PROTECTED SCHEDULE DRIFT ${id}: before=${before.scheduled[id]} after=${after.scheduled[id]}`,
      );
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
    console.log(JSON.stringify({ ok: true, dryRun: true, target: TARGET }, null, 2));
    return;
  }
  if (!approved) throw new Error("Execution requires --approved-by-user");
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "schedule-aug19-zoo-2026-08-12",
  });

  const prisma = new PrismaClient();
  try {
    const access = await getAccess(prisma);
    const watchIds = [TARGET.id, ...PROTECTED_SCHEDULE_IDS, ...PROTECTED_PUBLIC_IDS];
    let map = await getVideos(access, watchIds);
    const baseline = snapProtected(map);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );

    const occupied = new Set(Object.values(baseline.scheduled).filter(Boolean));
    if (occupied.has(TARGET.publishAt)) throw new Error(`collision ${TARGET.publishAt}`);

    const before = map.get(TARGET.id);
    if (!before) throw new Error(`missing ${TARGET.id}`);
    if (before.status?.privacyStatus !== "private") {
      throw new Error(`expected private, got ${before.status?.privacyStatus}`);
    }

    writeFileSync(
      resolve(AUD, "PRE_STATE.json"),
      JSON.stringify(
        {
          at: new Date().toISOString(),
          id: TARGET.id,
          title: before.snippet?.title,
          privacy: before.status?.privacyStatus,
          publishAt: before.status?.publishAt || null,
          targetPublishAt: TARGET.publishAt,
        },
        null,
        2,
      ) + "\n",
    );

    console.log(`\n>>> SCHEDULE ${TARGET.id} → ${TARGET.publishAt}`);
    const result = await updateStatus(access, TARGET.id, {
      ...baseWritable(before.status),
      privacyStatus: "private",
      publishAt: TARGET.publishAt,
    });
    if (!result.ok) throw new Error(`schedule failed: ${JSON.stringify(result.body)}`);
    await sleep(2000);
    map = await getVideos(access, watchIds);
    const after = map.get(TARGET.id);
    const ok =
      after?.status?.privacyStatus === "private" &&
      after?.status?.publishAt === TARGET.publishAt;
    const entry = {
      action: "schedule",
      id: TARGET.id,
      title: TARGET.title,
      before: {
        privacy: before.status?.privacyStatus,
        publishAt: before.status?.publishAt || null,
      },
      after: {
        privacy: after?.status?.privacyStatus,
        publishAt: after?.status?.publishAt || null,
      },
      ok,
      at: new Date().toISOString(),
    };
    writeFileSync(resolve(AUD, "journal", `${Date.now()}_${TARGET.id}.json`), JSON.stringify(entry, null, 2));
    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify([entry], null, 2) + "\n");
    console.log(JSON.stringify(entry, null, 2));
    if (!ok) throw new Error("verify failed");
    assertProtectedUnchanged(baseline, snapProtected(map));
    writeFileSync(
      resolve(AUD, "POST_STATE.json"),
      JSON.stringify({ at: new Date().toISOString(), entry, protected: snapProtected(map) }, null, 2) +
        "\n",
    );
    console.log("\n=== AUG 19 SCHEDULED ===");
    console.log(
      JSON.stringify(
        {
          id: TARGET.id,
          publishAt: TARGET.publishAt,
          uk: "Wed 19 Aug 2026 11:30",
          studioEdit: `https://studio.youtube.com/video/${TARGET.id}/edit`,
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
