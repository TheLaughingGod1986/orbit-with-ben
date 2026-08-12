/**
 * P0 repairs (user-approved 2026-08-12):
 * 1) Privatize accidental-early publics: dPMJQp2gMNc, rFJoOdQAc9c
 * 2) Unschedule hold/obsolete/duplicate: icedH_gK8JE, gPCpMsB0w2E, YsyPMhNmHMk, 8DxCTXUlw74
 *
 * ONE VIDEO AT A TIME. Verify after each. Abort if protected schedule drifts.
 * Requires: --execute --allow-emergency-unfreeze
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/p0_privatize_unschedule_2026-08-12");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

const PRIVATIZE = [
  { id: "dPMJQp2gMNc", reason: "ACCIDENTAL_EARLY_KEEP_PRIVATE — Space Is Rude About Distance" },
  { id: "rFJoOdQAc9c", reason: "ACCIDENTAL_EARLY_KEEP_PRIVATE — Zoo Hypothesis" },
];

const UNSCHEDULE = [
  { id: "icedH_gK8JE", reason: "BH reserve / legacy hold — must not air 19 Aug" },
  { id: "gPCpMsB0w2E", reason: "16→13 obsolete — must not air 28 Aug" },
  { id: "YsyPMhNmHMk", reason: "16→13 obsolete — must not air 1 Sep" },
  { id: "8DxCTXUlw74", reason: "20s Fermi historical duplicate — must not air 3 Sep" },
];

/** Canonical / approved schedule that must not change during this run */
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
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${access}` } },
    );
    const json = await res.json();
    if (!res.ok) throw new Error(JSON.stringify(json));
    for (const it of json.items || []) map.set(it.id, it);
  }
  return map;
}

async function updateStatus(
  access: string,
  id: string,
  status: Record<string, unknown>,
) {
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

function baseWritable(prior: any) {
  return {
    privacyStatus: "private" as string,
    license: prior?.license || "youtube",
    embeddable: prior?.embeddable !== false,
    publicStatsViewable: prior?.publicStatsViewable !== false,
    selfDeclaredMadeForKids: prior?.selfDeclaredMadeForKids === true,
  };
}

async function setPrivate(access: string, id: string, prior: any) {
  return updateStatus(access, id, baseWritable(prior));
}

/** Clear publishAt via private update; if stuck, unlisted hop then private (proven pattern). */
async function setPrivateUnscheduled(access: string, id: string, prior: any) {
  let result = await updateStatus(access, id, baseWritable(prior));
  if (!result.ok) return { ok: false as const, result, hopped: false, after: null };
  await sleep(2000);
  let live = (await getVideos(access, [id])).get(id);
  if (live?.status?.publishAt) {
    await updateStatus(access, id, { ...baseWritable(prior), privacyStatus: "unlisted" });
    await sleep(1500);
    result = await updateStatus(access, id, baseWritable(prior));
    await sleep(2000);
    live = (await getVideos(access, [id])).get(id);
    return {
      ok: live?.status?.privacyStatus === "private" && !live?.status?.publishAt,
      result,
      hopped: true,
      after: {
        privacy: live?.status?.privacyStatus || null,
        publishAt: live?.status?.publishAt || null,
      },
    };
  }
  return {
    ok: live?.status?.privacyStatus === "private" && !live?.status?.publishAt,
    result,
    hopped: false,
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
    const it = map.get(id);
    scheduled[id] = it?.status?.publishAt || null;
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    const it = map.get(id);
    publicState[id] = it?.status?.privacyStatus || null;
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
    if (before.publicState[id] !== "public" || after.publicState[id] !== "public") {
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
  if (!execute) {
    console.log(JSON.stringify({ ok: true, dryRun: true, note: "Pass --execute --allow-emergency-unfreeze" }, null, 2));
    return;
  }
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "p0-privatize-unschedule-2026-08-12",
  });

  const prisma = new PrismaClient();
  const journal: unknown[] = [];
  try {
    const access = await getAccess(prisma);
    const watchIds = [
      ...PRIVATIZE.map((x) => x.id),
      ...UNSCHEDULE.map((x) => x.id),
      ...PROTECTED_SCHEDULE_IDS,
      ...PROTECTED_PUBLIC_IDS,
    ];
    let map = await getVideos(access, watchIds);
    const baseline = snapProtected(map);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );

    // --- Privatize one-by-one ---
    for (const t of PRIVATIZE) {
      const before = map.get(t.id);
      if (!before) throw new Error(`missing ${t.id}`);
      console.log(`\n>>> PRIVATIZE ${t.id} (${t.reason})`);
      if (before.status?.privacyStatus === "private" && !before.status?.publishAt) {
        journal.push({ action: "privatize", id: t.id, skipped: true, reason: "already private" });
        console.log("already private — skip");
        continue;
      }
      const result = await setPrivate(access, t.id, before.status);
      if (!result.ok) throw new Error(`privatize failed ${t.id}: ${JSON.stringify(result.body)}`);
      await sleep(2000);
      map = await getVideos(access, watchIds);
      const after = map.get(t.id);
      const ok = after?.status?.privacyStatus === "private";
      const entry = {
        action: "privatize",
        id: t.id,
        reason: t.reason,
        before: { privacy: before.status?.privacyStatus, publishAt: before.status?.publishAt || null },
        after: { privacy: after?.status?.privacyStatus, publishAt: after?.status?.publishAt || null },
        ok,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(resolve(AUD, "journal", `${Date.now()}_${t.id}.json`), JSON.stringify(entry, null, 2));
      console.log(JSON.stringify(entry, null, 2));
      if (!ok) throw new Error(`verify failed privatize ${t.id}`);
      assertProtectedUnchanged(baseline, snapProtected(map));
      console.log("protected schedule/public OK");
    }

    // --- Unschedule one-by-one ---
    for (const t of UNSCHEDULE) {
      const before = map.get(t.id);
      if (!before) throw new Error(`missing ${t.id}`);
      console.log(`\n>>> UNSCHEDULE ${t.id} (${t.reason})`);
      if (before.status?.privacyStatus === "private" && !before.status?.publishAt) {
        journal.push({ action: "unschedule", id: t.id, skipped: true, reason: "already private+unscheduled" });
        console.log("already clear — skip");
        continue;
      }
      const cleared = await setPrivateUnscheduled(access, t.id, before.status);
      if (!cleared.ok) throw new Error(`unschedule failed ${t.id}: ${JSON.stringify(cleared)}`);
      await sleep(1500);
      map = await getVideos(access, watchIds);
      const after = map.get(t.id);
      const ok = after?.status?.privacyStatus === "private" && !after?.status?.publishAt;
      const entry = {
        action: "unschedule",
        id: t.id,
        reason: t.reason,
        before: { privacy: before.status?.privacyStatus, publishAt: before.status?.publishAt || null },
        after: { privacy: after?.status?.privacyStatus, publishAt: after?.status?.publishAt || null },
        hopped: cleared.hopped,
        ok,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(resolve(AUD, "journal", `${Date.now()}_${t.id}.json`), JSON.stringify(entry, null, 2));
      console.log(JSON.stringify(entry, null, 2));
      if (!ok) throw new Error(`verify failed unschedule ${t.id}`);
      assertProtectedUnchanged(baseline, snapProtected(map));
      console.log("protected schedule/public OK");
    }

    const finalSnap = snapProtected(map);
    const post = {
      at: new Date().toISOString(),
      targets: [...PRIVATIZE, ...UNSCHEDULE].map((t) => {
        const it = map.get(t.id);
        return {
          id: t.id,
          privacy: it?.status?.privacyStatus,
          publishAt: it?.status?.publishAt || null,
        };
      }),
      protected: finalSnap,
      journal,
    };
    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify(journal, null, 2) + "\n");
    writeFileSync(resolve(AUD, "POST_STATE.json"), JSON.stringify(post, null, 2) + "\n");
    console.log("\n=== P0 COMPLETE ===");
    console.log(JSON.stringify({ targets: post.targets, protectedPublic: finalSnap.publicState }, null, 2));
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
