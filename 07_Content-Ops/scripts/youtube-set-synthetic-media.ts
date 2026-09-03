#!/usr/bin/env tsx
/**
 * Set status.containsSyntheticMedia=true on Orbit YouTube videos
 * (Studio "Altered or synthetic content" / Made with AI disclosure).
 *
 * Usage:
 *   cd 07_Content-Ops && npx tsx scripts/youtube-set-synthetic-media.ts
 *   cd 07_Content-Ops && npx tsx scripts/youtube-set-synthetic-media.ts --dry-run
 *   cd 07_Content-Ops && npx tsx scripts/youtube-set-synthetic-media.ts --ids a,b,c
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";

const OUT_DIR = path.resolve(
  __dirname,
  "../../00_Brand/Channel-Setup/audits/ai_synthetic_disclosure_2026-08-26",
);

async function accessToken(): Promise<string> {
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected" },
  });
  if (!conn) throw new Error("No YouTube connection");
  const env = getEnv();
  if (conn.refreshTokenEncrypted && env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET) {
    const refreshToken = decryptSecret(conn.refreshTokenEncrypted);
    const res = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: env.GOOGLE_CLIENT_ID,
        client_secret: env.GOOGLE_CLIENT_SECRET,
        refresh_token: refreshToken,
        grant_type: "refresh_token",
      }),
    });
    const body = await res.json();
    if (!res.ok || !body.access_token) {
      throw new Error(`refresh failed: ${JSON.stringify(body).slice(0, 240)}`);
    }
    await prisma.platformConnection.update({
      where: { id: conn.id },
      data: {
        accessTokenEncrypted: encryptSecret(body.access_token),
        accessTokenExpiresAt: new Date(Date.now() + Number(body.expires_in || 3600) * 1000),
        lastRefreshAt: new Date(),
      },
    });
    return body.access_token as string;
  }
  if (!conn.accessTokenEncrypted) throw new Error("No access token");
  return decryptSecret(conn.accessTokenEncrypted);
}

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(init?.headers || {}),
    },
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 400)}`);
  }
  return body;
}

async function listAllVideoIds(token: string): Promise<string[]> {
  const ch = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true",
  );
  const uploads = ch.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
  const ids: string[] = [];
  let page: string | undefined;
  if (uploads) {
    do {
      const q = new URLSearchParams({
        part: "contentDetails",
        playlistId: uploads,
        maxResults: "50",
      });
      if (page) q.set("pageToken", page);
      const s = await yt(token, `https://www.googleapis.com/youtube/v3/playlistItems?${q}`);
      for (const it of s.items || []) {
        const id = it.contentDetails?.videoId;
        if (id) ids.push(id);
      }
      page = s.nextPageToken;
    } while (page);
  }
  // Also mine=search for scheduled / private that may not be in uploads yet
  page = undefined;
  do {
    const q = new URLSearchParams({
      part: "id",
      forMine: "true",
      type: "video",
      maxResults: "50",
    });
    if (page) q.set("pageToken", page);
    const s = await yt(token, `https://www.googleapis.com/youtube/v3/search?${q}`);
    for (const it of s.items || []) if (it.id?.videoId) ids.push(it.id.videoId);
    page = s.nextPageToken;
  } while (page);
  return [...new Set(ids)];
}

type VideoRow = {
  id: string;
  title: string;
  privacyStatus?: string;
  containsSyntheticMedia?: boolean | null;
};

async function fetchStatuses(token: string, ids: string[]): Promise<VideoRow[]> {
  const rows: VideoRow[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const q = new URLSearchParams({
      part: "snippet,status",
      id: chunk.join(","),
    });
    const v = await yt(token, `https://www.googleapis.com/youtube/v3/videos?${q}`);
    for (const it of v.items || []) {
      rows.push({
        id: it.id,
        title: it.snippet?.title || "",
        privacyStatus: it.status?.privacyStatus,
        containsSyntheticMedia: it.status?.containsSyntheticMedia ?? null,
      });
    }
  }
  return rows;
}

async function setSynthetic(token: string, id: string): Promise<VideoRow> {
  // videos.update with part=status; only send fields we intend to change.
  // Privacy must be re-sent or API may reject; read current first.
  const cur = await yt(
    token,
    `https://www.googleapis.com/youtube/v3/videos?part=status&id=${encodeURIComponent(id)}`,
  );
  const status = cur.items?.[0]?.status || {};
  const body = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/videos?part=status",
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id,
        status: {
          privacyStatus: status.privacyStatus,
          selfDeclaredMadeForKids: status.selfDeclaredMadeForKids ?? status.madeForKids ?? false,
          embeddable: status.embeddable,
          publicStatsViewable: status.publicStatsViewable,
          license: status.license,
          ...(status.publishAt ? { publishAt: status.publishAt } : {}),
          containsSyntheticMedia: true,
        },
      }),
    },
  );
  const st = body.items?.[0]?.status || body.status || {};
  return {
    id,
    title: body.items?.[0]?.snippet?.title || id,
    privacyStatus: st.privacyStatus,
    containsSyntheticMedia: st.containsSyntheticMedia ?? true,
  };
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const idsArg = args.find((a) => a.startsWith("--ids="))?.slice(6);
  const onlyIds = idsArg
    ? idsArg.split(",").map((s) => s.trim()).filter(Boolean)
    : null;

  const token = await accessToken();
  const ids = onlyIds || (await listAllVideoIds(token));
  console.log(`videos=${ids.length} dryRun=${dryRun}`);

  const before = await fetchStatuses(token, ids);
  const already = before.filter((v) => v.containsSyntheticMedia === true);
  const need = before.filter((v) => v.containsSyntheticMedia !== true);
  console.log(`already=${already.length} need=${need.length}`);

  const results: Array<Record<string, unknown>> = [];
  for (const v of need) {
    if (dryRun) {
      console.log(`dry-run would set ${v.id} · ${v.title}`);
      results.push({ ...v, action: "dry_run" });
      continue;
    }
    try {
      const updated = await setSynthetic(token, v.id);
      console.log(`SET ${v.id} · ${v.title} → containsSyntheticMedia=${updated.containsSyntheticMedia}`);
      results.push({ ...v, action: "set", after: updated.containsSyntheticMedia });
      // gentle pacing
      await new Promise((r) => setTimeout(r, 200));
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      console.error(`FAIL ${v.id} · ${msg}`);
      results.push({ ...v, action: "error", error: msg.slice(0, 400) });
    }
  }

  // verify pass
  const after = dryRun ? before : await fetchStatuses(token, ids);
  const stillMissing = after.filter((v) => v.containsSyntheticMedia !== true);

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const report = {
    when: new Date().toISOString(),
    dryRun,
    total: ids.length,
    already: already.length,
    attempted: need.length,
    stillMissing: stillMissing.map((v) => ({ id: v.id, title: v.title, privacy: v.privacyStatus })),
    results,
    after: after.map((v) => ({
      id: v.id,
      title: v.title,
      privacy: v.privacyStatus,
      containsSyntheticMedia: v.containsSyntheticMedia,
    })),
  };
  const outFile = path.join(OUT_DIR, dryRun ? "DRY_RUN.json" : "RESULT.json");
  fs.writeFileSync(outFile, JSON.stringify(report, null, 2) + "\n");
  console.log(`wrote ${outFile}`);
  console.log(`stillMissing=${stillMissing.length}`);
  if (stillMissing.length && !dryRun) process.exitCode = 1;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
