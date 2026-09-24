#!/usr/bin/env tsx
/**
 * Change only the title on listed YouTube ids.
 * Reads the live snippet first and sends it back with the new title, so
 * description, tags, category and languages stay as they are. Does not
 * send status, so privacy and publishAt stay untouched.
 *
 *   npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json --dry-run
 *   npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";

type RetitleRow = {
  id: string;
  expectCurrentTitle: string;
  title: string;
};

const WRITABLE_SNIPPET_KEYS = [
  "description",
  "tags",
  "categoryId",
  "defaultLanguage",
  "defaultAudioLanguage",
] as const;

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

async function accessToken(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn) throw new Error("No connected YouTube account");
  if (!conn.refreshTokenEncrypted || !env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    if (!conn.accessTokenEncrypted) throw new Error("No YouTube token");
    return decryptSecret(conn.accessTokenEncrypted);
  }
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

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init?.headers || {}) },
  });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 400)}`);
  return body;
}

async function main() {
  const file = arg("file");
  if (!file) {
    console.error("Usage: retitle-videos.ts --file <json> [--dry-run]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const pack = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  const rows: RetitleRow[] = pack.retitle;
  const token = await accessToken();
  const results: unknown[] = [];

  for (const row of rows) {
    const got = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const item = got.items?.[0];
    if (!item) {
      results.push({ id: row.id, error: "not_found" });
      continue;
    }
    const current: string = item.snippet?.title || "";
    const before = {
      title: current,
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt || null,
    };
    if (current === row.title) {
      results.push({ id: row.id, skipped: "already_titled", before });
      continue;
    }
    // Someone changed the title since the fix list was written — do not overwrite their choice.
    if (current !== row.expectCurrentTitle) {
      results.push({ id: row.id, skipped: "title_changed_since_audit", before, expected: row.expectCurrentTitle });
      continue;
    }
    const snippet: Record<string, unknown> = { title: row.title };
    for (const key of WRITABLE_SNIPPET_KEYS) {
      if (item.snippet?.[key] !== undefined) snippet[key] = item.snippet[key];
    }
    if (dry) {
      results.push({ id: row.id, dryRun: true, before, nextTitle: row.title });
      console.log(JSON.stringify({ id: row.id, from: current, to: row.title, dryRun: true }));
      continue;
    }
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: row.id, snippet }),
    });
    const after = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const a = after.items?.[0];
    results.push({
      id: row.id,
      updated: true,
      before,
      after: {
        title: a?.snippet?.title,
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
      },
    });
    console.log(JSON.stringify({ id: row.id, title: a?.snippet?.title, publishAt: a?.status?.publishAt || null }));
  }

  const out = path.resolve(file.replace(/\.json$/, "") + "_RESULT.json");
  fs.writeFileSync(out, JSON.stringify({ dry, finishedAt: new Date().toISOString(), results }, null, 2) + "\n");
  console.log(JSON.stringify({ wrote: out, n: results.length, dry }, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
