/**
 * User-approved 2026-08-12: fill exo→JWST gap (16→20 Aug) using existing
 * retention-v2 exo reserves (no new builds needed).
 *
 * 17 Aug 11:30 UK → OlwENQcY-jg (Giant Eye)
 * 18 Aug 11:30 UK → QRi6Dxq0hz0 (Host Life)
 * 19 Aug left empty as buffer before JWST long (20 Aug).
 *
 * ONE VIDEO AT A TIME. Requires: --execute --allow-emergency-unfreeze --approved-by-user
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/schedule_exo_gap_17_18_2026-08-12");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

/** 12:30 Europe/London BST = 11:30Z */
const PLAN = [
  {
    id: "OlwENQcY-jg",
    publishAt: "2026-08-17T10:30:00Z",
    title: "Giant Eye / Eyeball Planets",
  },
  {
    id: "QRi6Dxq0hz0",
    publishAt: "2026-08-18T10:30:00Z",
    title: "Could Any of These Alien Worlds Host Life?",
  },
] as const;

const PROTECTED_SCHEDULE_IDS = [
  "SC2WGTl_V5Q",
  "M-VN84HCNls",
  "nAZRIBm5wJw",
  "tEOHYQbcgOw",
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

async function setScheduled(access: string, id: string, prior: any, publishAt: string) {
  const result = await updateStatus(access, id, {
    ...baseWritable(prior),
    privacyStatus: "private",
    publishAt,
  });
  if (!result.ok) return { ok: false as const, result, after: null };
  await sleep(2000);
  const live = (await getVideos(access, [id])).get(id);
  return {
    ok: live?.status?.privacyStatus === "private" && live?.status?.publishAt === publishAt,
    result,
    after: {
      privacy: live?.status?.privacyStatus || null,
      publishAt: live?.status?.publishAt || null,
    },
  };
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
      throw new Error(
        `PROTECTED PUBLIC DRIFT ${id}: before=${before.publicState[id]} after=${after.publicState[id]}`,
      );
    }
  }
}

async function main() {
  mkdirSync(resolve(AUD, "journal"), { recursive: true });
  const execute = flag("execute");
  const allow = flag("allow-emergency-unfreeze");
  const approved = flag("approved-by-user");
  if (!execute) {
    console.log(
      JSON.stringify(
        { ok: true, dryRun: true, plan: PLAN, note: "Pass --execute --allow-emergency-unfreeze --approved-by-user" },
        null,
        2,
      ),
    );
    return;
  }
  if (!approved) throw new Error("Execution requires --approved-by-user");
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "schedule-exo-gap-17-18-2026-08-12",
  });

  const prisma = new PrismaClient();
  const journal: unknown[] = [];
  try {
    const access = await getAccess(prisma);
    const watchIds = [
      ...PLAN.map((x) => x.id),
      ...PROTECTED_SCHEDULE_IDS,
      ...PROTECTED_PUBLIC_IDS,
    ];
    let map = await getVideos(access, watchIds);
    const baseline = snapProtected(map);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );

    // collision check vs existing protected publishAts
    const occupied = new Set(Object.values(baseline.scheduled).filter(Boolean));
    for (const t of PLAN) {
      if (occupied.has(t.publishAt)) throw new Error(`schedule collision ${t.publishAt}`);
    }

    const preRows = PLAN.map((t) => {
      const it = map.get(t.id);
      return {
        id: t.id,
        title: it?.snippet?.title || null,
        privacy: it?.status?.privacyStatus || null,
        publishAt: it?.status?.publishAt || null,
        targetPublishAt: t.publishAt,
      };
    });
    writeFileSync(
      resolve(AUD, "PRE_STATE.json"),
      JSON.stringify({ at: new Date().toISOString(), rows: preRows }, null, 2) + "\n",
    );

    for (const t of PLAN) {
      const before = map.get(t.id);
      if (!before) throw new Error(`missing ${t.id}`);
      console.log(`\n>>> SCHEDULE ${t.id} → ${t.publishAt} (${t.title})`);
      if (before.status?.privacyStatus !== "private") {
        throw new Error(`expected private ${t.id}, got ${before.status?.privacyStatus}`);
      }
      if (before.status?.publishAt === t.publishAt) {
        journal.push({ action: "schedule", id: t.id, skipped: true, reason: "already at target" });
        console.log("already scheduled — skip");
        continue;
      }
      const set = await setScheduled(access, t.id, before.status, t.publishAt);
      if (!set.ok) throw new Error(`schedule failed ${t.id}: ${JSON.stringify(set)}`);
      await sleep(1500);
      map = await getVideos(access, watchIds);
      const after = map.get(t.id);
      const ok =
        after?.status?.privacyStatus === "private" && after?.status?.publishAt === t.publishAt;
      const entry = {
        action: "schedule",
        id: t.id,
        title: t.title,
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
      journal.push(entry);
      writeFileSync(
        resolve(AUD, "journal", `${Date.now()}_${t.id}.json`),
        JSON.stringify(entry, null, 2),
      );
      console.log(JSON.stringify(entry, null, 2));
      if (!ok) throw new Error(`verify failed schedule ${t.id}`);
      assertProtectedUnchanged(baseline, snapProtected(map));
      console.log("protected schedule/public OK");
    }

    const post = {
      at: new Date().toISOString(),
      targets: PLAN.map((t) => {
        const it = map.get(t.id);
        return {
          id: t.id,
          privacy: it?.status?.privacyStatus,
          publishAt: it?.status?.publishAt || null,
        };
      }),
      protected: snapProtected(map),
      journal,
      note: "Aug 19 left empty as buffer before JWST long 20 Aug",
    };
    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify(journal, null, 2) + "\n");
    writeFileSync(resolve(AUD, "POST_STATE.json"), JSON.stringify(post, null, 2) + "\n");
    console.log("\n=== GAP FILL SCHEDULED ===");
    console.log(JSON.stringify({ targets: post.targets, note: post.note }, null, 2));
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
