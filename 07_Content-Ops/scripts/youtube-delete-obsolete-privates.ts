/**
 * User-approved 2026-08-12: permanently delete 13 obsolete/superseded private Shorts.
 * Leave usable reserves private (OlwENQcY-jg, QRi6Dxq0hz0, rFJoOdQAc9c, dPMJQp2gMNc).
 *
 * ONE VIDEO AT A TIME. Abort if protected public/schedule drifts.
 * Requires: --execute --allow-emergency-unfreeze --approved-by-user
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { assertYouTubeMutationAllowed } from "../src/lib/publishing/youtube-freeze";
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/delete_obsolete_privates_2026-08-12");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

const DELETE = [
  { id: "ho9VJxp7f3A", reason: "Superseded by SC2WGTl_V5Q (glass rain)" },
  { id: "aoR-dA_g7eI", reason: "Superseded by M-VN84HCNls (diamond)" },
  { id: "6QFGAFZk264", reason: "Superseded by nAZRIBm5wJw (three suns)" },
  { id: "eOOFVrJ2Ojc", reason: "Superseded by tEOHYQbcgOw (hottest nights)" },
  { id: "Web2otrTcT0", reason: "Superseded by OlwENQcY-jg (giant eye old)" },
  { id: "1qts3tIsg9c", reason: "Superseded by QRi6Dxq0hz0 (host life old)" },
  { id: "mGwSCdgxQO4", reason: "Extra glass-rain hold; scheduled copy exists" },
  { id: "w1ej9u0rPTA", reason: "Duplicate of public JRfhE6yWom4; blank thumb" },
  { id: "HvAKGjx4lv0", reason: "Duplicate of public tUAdhOnMW2g" },
  { id: "icedH_gK8JE", reason: "BH legacy hold; public B2STcIAF1lY covers beat" },
  { id: "8DxCTXUlw74", reason: "20s Fermi historical dup; public 1HuV8o3gOss" },
  { id: "gPCpMsB0w2E", reason: "16→13 obsolete" },
  { id: "YsyPMhNmHMk", reason: "16→13 obsolete" },
] as const;

/** Must NEVER be deleted in this run */
const NEVER_DELETE = new Set([
  // usable reserves / later schedule
  "OlwENQcY-jg",
  "QRi6Dxq0hz0",
  "rFJoOdQAc9c",
  "dPMJQp2gMNc",
  // scheduled
  "b8-X_FyJnHM",
  "SC2WGTl_V5Q",
  "M-VN84HCNls",
  "nAZRIBm5wJw",
  "tEOHYQbcgOw",
  "tfTkMdE7qqw",
  "bLv0RfidjSg",
  "PcP64way3xA",
  "pjIevt27Svo",
  "AeFm7gWyWik",
  // public shorts
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
  "tUAdhOnMW2g",
  "svYOx07OrIM",
  "B2STcIAF1lY",
]);

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

const KEEP_PRIVATE_IDS = ["OlwENQcY-jg", "QRi6Dxq0hz0", "rFJoOdQAc9c", "dPMJQp2gMNc"];

function flag(name: string) {
  return process.argv.includes(`--${name}`);
}

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

function parseDur(iso: string): number {
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!m) return 0;
  return (
    parseInt(m[1] || "0", 10) * 3600 +
    parseInt(m[2] || "0", 10) * 60 +
    parseInt(m[3] || "0", 10)
  );
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
  const res = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?id=${encodeURIComponent(id)}`,
    { method: "DELETE", headers: { Authorization: `Bearer ${access}` } },
  );
  if (!res.ok && res.status !== 204) {
    const body = await res.text();
    throw new Error(`videos.delete ${id} ${res.status}: ${body}`);
  }
}

function snapProtected(map: Map<string, any>) {
  const scheduled: Record<string, string | null> = {};
  const publicState: Record<string, string | null> = {};
  const keepPrivate: Record<string, string | null> = {};
  for (const id of PROTECTED_SCHEDULE_IDS) {
    scheduled[id] = map.get(id)?.status?.publishAt || null;
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    publicState[id] = map.get(id)?.status?.privacyStatus || null;
  }
  for (const id of KEEP_PRIVATE_IDS) {
    const it = map.get(id);
    keepPrivate[id] = it
      ? `${it.status?.privacyStatus}|${it.status?.publishAt || ""}`
      : "MISSING";
  }
  return { scheduled, publicState, keepPrivate };
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
    if (!after.scheduled[id]) {
      throw new Error(`PROTECTED SCHEDULE LOST ${id}`);
    }
  }
  for (const id of PROTECTED_PUBLIC_IDS) {
    if (after.publicState[id] !== "public") {
      throw new Error(
        `PROTECTED PUBLIC DRIFT ${id}: before=${before.publicState[id]} after=${after.publicState[id]}`,
      );
    }
  }
  for (const id of KEEP_PRIVATE_IDS) {
    if (after.keepPrivate[id] === "MISSING") throw new Error(`KEEP-PRIVATE MISSING ${id}`);
    if (!after.keepPrivate[id]?.startsWith("private|")) {
      throw new Error(`KEEP-PRIVATE DRIFT ${id}: ${after.keepPrivate[id]}`);
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
        { ok: true, dryRun: true, deleteCount: DELETE.length, note: "Pass --execute --allow-emergency-unfreeze --approved-by-user" },
        null,
        2,
      ),
    );
    return;
  }
  if (!approved) throw new Error("Execution requires --approved-by-user");
  assertYouTubeMutationAllowed({
    allowEmergencyUnfreeze: allow,
    operation: "delete-obsolete-privates-2026-08-12",
  });

  for (const t of DELETE) {
    if (NEVER_DELETE.has(t.id)) throw new Error(`REFUSING delete of protected id ${t.id}`);
  }

  const prisma = new PrismaClient();
  const journal: unknown[] = [];
  try {
    const access = await getAccess(prisma);
    const watchIds = [
      ...DELETE.map((x) => x.id),
      ...PROTECTED_SCHEDULE_IDS,
      ...PROTECTED_PUBLIC_IDS,
      ...KEEP_PRIVATE_IDS,
    ];
    let map = await getVideos(access, watchIds);
    const baseline = snapProtected(map);
    writeFileSync(
      resolve(AUD, "PROTECTED_BASELINE.json"),
      JSON.stringify({ at: new Date().toISOString(), baseline }, null, 2) + "\n",
    );

    const preRows = DELETE.map((t) => {
      const it = map.get(t.id);
      return {
        id: t.id,
        reason: t.reason,
        present: Boolean(it),
        title: it?.snippet?.title || null,
        privacy: it?.status?.privacyStatus || null,
        publishAt: it?.status?.publishAt || null,
        durationS: it ? parseDur(it.contentDetails?.duration || "") : null,
        views: it ? Number(it.statistics?.viewCount || 0) : null,
      };
    });
    writeFileSync(
      resolve(AUD, "PRE_STATE.json"),
      JSON.stringify({ at: new Date().toISOString(), rows: preRows }, null, 2) + "\n",
    );

    for (const t of DELETE) {
      console.log(`\n>>> DELETE ${t.id} (${t.reason})`);
      if (NEVER_DELETE.has(t.id)) throw new Error(`REFUSING ${t.id}`);
      const before = map.get(t.id);
      if (!before) {
        const entry = { action: "delete", id: t.id, skipped: true, reason: "already missing" };
        journal.push(entry);
        console.log("already missing — skip");
        continue;
      }
      const privacy = before.status?.privacyStatus;
      const publishAt = before.status?.publishAt || null;
      const dur = parseDur(before.contentDetails?.duration || "");
      if (privacy !== "private" || publishAt) {
        throw new Error(`gate fail ${t.id}: privacy=${privacy} publishAt=${publishAt}`);
      }
      if (dur <= 0 || dur > 60) {
        throw new Error(`duration gate fail ${t.id}: ${dur}s`);
      }

      await deleteVideo(access, t.id);
      let missing = false;
      for (let attempt = 1; attempt <= 8; attempt++) {
        await sleep(750);
        const check = await getVideos(access, [t.id]);
        if (!check.has(t.id)) {
          missing = true;
          break;
        }
      }
      if (!missing) throw new Error(`delete verify failed — still present ${t.id}`);

      map = await getVideos(access, watchIds.filter((id) => id !== t.id || NEVER_DELETE.has(id)));
      // refresh full watch set except deleted
      map = await getVideos(
        access,
        watchIds.filter((id) => id !== t.id),
      );
      // re-add deleted as absent
      const entry = {
        action: "delete",
        id: t.id,
        reason: t.reason,
        before: {
          title: before.snippet?.title || null,
          privacy,
          publishAt,
          durationS: dur,
          views: Number(before.statistics?.viewCount || 0),
        },
        deleted: true,
        at: new Date().toISOString(),
      };
      journal.push(entry);
      writeFileSync(
        resolve(AUD, "journal", `${Date.now()}_${t.id}.json`),
        JSON.stringify(entry, null, 2),
      );
      console.log(JSON.stringify(entry, null, 2));

      // rebuild map including confirming deleted gone
      const afterMap = await getVideos(access, [
        ...PROTECTED_SCHEDULE_IDS,
        ...PROTECTED_PUBLIC_IDS,
        ...KEEP_PRIVATE_IDS,
        ...DELETE.map((x) => x.id),
      ]);
      if (afterMap.has(t.id)) throw new Error(`still listed after delete ${t.id}`);
      assertProtectedUnchanged(baseline, snapProtected(afterMap));
      console.log("protected schedule/public/reserves OK");
      map = afterMap;
    }

    const stillPresent = DELETE.map((t) => t.id).filter((id) => map.has(id));
    const post = {
      at: new Date().toISOString(),
      deleted: DELETE.map((t) => t.id).filter((id) => !map.has(id)),
      stillPresent,
      protected: snapProtected(map),
      journal,
    };
    writeFileSync(resolve(AUD, "MUTATION_JOURNAL.json"), JSON.stringify(journal, null, 2) + "\n");
    writeFileSync(resolve(AUD, "POST_STATE.json"), JSON.stringify(post, null, 2) + "\n");
    if (stillPresent.length) throw new Error(`still present: ${stillPresent.join(",")}`);
    console.log("\n=== DELETE COMPLETE ===");
    console.log(JSON.stringify({ deleted: post.deleted.length, protectedPublic: post.protected.publicState }, null, 2));
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
