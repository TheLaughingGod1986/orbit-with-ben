/**
 * Read-only: decrypt Orbit YouTube OAuth and fetch video status for Studio Shorts IDs.
 * Writes API_LIVE_STATE.json under the forensic audit folder — no mutations.
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { readFileSync, writeFileSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(
  ROOT,
  "00_Brand/Channel-Setup/audits/shorts_visibility_forensic_repair_2026-08-10",
);
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

async function main() {
  const prisma = new PrismaClient();
  try {
    const conn = await prisma.platformConnection.findFirst({
      where: {
        platform: "youtube_shorts",
        channelId: "UC_esArsDKd3GJvOkeO0DUog",
        connectionStatus: "connected",
      },
    });
    if (!conn?.accessTokenEncrypted) throw new Error("no Orbit With Ben youtube token");

    let access = decryptSecret(conn.accessTokenEncrypted);
    const refresh = conn.refreshTokenEncrypted
      ? decryptSecret(conn.refreshTokenEncrypted)
      : null;
    const exp = conn.accessTokenExpiresAt ? new Date(conn.accessTokenExpiresAt).getTime() : 0;
    if (Date.now() >= exp - 60_000) {
      if (!refresh) throw new Error("token expired and no refresh");
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
      const json = (await res.json()) as { access_token?: string; error?: string };
      if (!res.ok || !json.access_token) throw new Error(JSON.stringify(json));
      access = json.access_token;
    }

    const studio = JSON.parse(
      readFileSync(resolve(AUD, "STUDIO_SHORTS_COMPLETE_INVENTORY.json"), "utf8"),
    ) as { rows: { videoId: string }[] };
    const registry = JSON.parse(
      readFileSync(resolve(ROOT, "00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json"), "utf8"),
    );

    const ids = new Set<string>();
    for (const r of studio.rows) if (r.videoId) ids.add(r.videoId);
    const addId = (x: unknown) => {
      if (!x) return;
      if (typeof x === "string" && /^[A-Za-z0-9_-]{11}$/.test(x)) ids.add(x);
      if (typeof x === "object" && x && "id" in x && typeof (x as { id: string }).id === "string") {
        ids.add((x as { id: string }).id);
      }
      if (
        typeof x === "object" &&
        x &&
        "youtubeVideoId" in x &&
        typeof (x as { youtubeVideoId: string }).youtubeVideoId === "string"
      ) {
        ids.add((x as { youtubeVideoId: string }).youtubeVideoId);
      }
    };
    for (const key of [
      "canonicalPublicLongform",
      "canonicalPublicShorts",
      "scheduledFuture",
      "intentionalPrivateHolds",
      "historicalDuplicatePrivate",
      "records",
      "deletedHistoricalDuplicateIds",
    ]) {
      const arr = (registry as Record<string, unknown>)[key];
      if (Array.isArray(arr)) arr.forEach(addId);
    }
    ["Mo93x0fxB1Q", "3xrxdmaOwJI", "b8-X_FyJnHM", "tfTkMdE7qqw", "1wxUhF3XnwI"].forEach((id) =>
      ids.add(id),
    );

    const idList = [...ids];
    const byId: Record<string, unknown> = {};
    for (let i = 0; i < idList.length; i += 50) {
      const chunk = idList.slice(i, i + 50);
      const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics&id=${chunk.join(",")}`;
      const res = await fetch(url, { headers: { Authorization: `Bearer ${access}` } });
      const json = (await res.json()) as { items?: unknown[]; error?: unknown };
      if (!res.ok) throw new Error(JSON.stringify(json.error || json));
      for (const it of json.items || []) {
        const item = it as { id: string };
        byId[item.id] = it;
      }
    }

    const out = {
      capturedAt: new Date().toISOString(),
      channelId: "UC_esArsDKd3GJvOkeO0DUog",
      requestedIds: idList.length,
      returnedIds: Object.keys(byId).length,
      missingIds: idList.filter((id) => !byId[id]),
      videos: byId,
    };
    writeFileSync(resolve(AUD, "API_LIVE_STATE.json"), JSON.stringify(out, null, 2) + "\n");
    console.log(
      JSON.stringify(
        {
          ok: true,
          requested: idList.length,
          returned: Object.keys(byId).length,
          missing: out.missingIds.length,
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
