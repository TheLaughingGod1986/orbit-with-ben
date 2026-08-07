#!/usr/bin/env tsx
/**
 * Apply en-GB language fields on approved canonical IDs (requires force-ssl).
 *
 *   npx tsx scripts/youtube-apply-en-gb.ts
 *   npx tsx scripts/youtube-apply-en-gb.ts --dry-run
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { hasForceSslScope, parseGrantedScopes } from "../src/lib/publishing/youtube-oauth";

const IDS = [
  "Mo93x0fxB1Q",
  "1HuV8o3gOss",
  "KcKBixwmcV4",
  "3xrxdmaOwJI",
  "JRfhE6yWom4",
  "L2OFjL4neOo",
];

const OUT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/EN_GB_METADATA_APPLY.json",
);

async function main() {
  getEnv();
  const dry = process.argv.includes("--dry-run");
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) throw new Error("No YouTube connection");
  const scopes = parseGrantedScopes(connection.grantedScopes);
  if (!hasForceSslScope(scopes)) {
    console.error("UPLOAD BLOCKED: youtube.force-ssl missing — reconnect first");
    process.exit(3);
  }
  const adapter = new YouTubePublishingAdapter();
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    await adapter.refreshConnection(connection);
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  const token = decryptSecret(fresh!.accessTokenEncrypted!);

  const results: any[] = [];
  for (const id of IDS) {
    const getRes = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`,
      { headers: { Authorization: `Bearer ${token}` } },
    );
    const getBody = await getRes.json();
    const item = getBody.items?.[0];
    if (!item) {
      results.push({ id, ok: false, error: "not_found" });
      continue;
    }
    const before = {
      defaultLanguage: item.snippet?.defaultLanguage || null,
      defaultAudioLanguage: item.snippet?.defaultAudioLanguage || null,
      categoryId: item.snippet?.categoryId || null,
    };
    const after = {
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
      categoryId: before.categoryId,
    };
    if (dry) {
      results.push({ id, dryRun: true, before, after, ok: true });
      continue;
    }
    const updateRes = await fetch(
      "https://www.googleapis.com/youtube/v3/videos?part=snippet",
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id,
          snippet: {
            title: item.snippet.title,
            description: item.snippet.description,
            categoryId: item.snippet.categoryId,
            tags: item.snippet.tags || [],
            defaultLanguage: "en-GB",
            defaultAudioLanguage: "en-GB",
          },
        }),
      },
    );
    const updateBody = await updateRes.json().catch(() => ({}));
    results.push({
      id,
      ok: updateRes.ok,
      before,
      after,
      status: updateRes.status,
      error: updateRes.ok ? null : JSON.stringify(updateBody).slice(0, 300),
    });
  }

  const payload = { ok: results.every((r) => r.ok), dry, results, at: new Date().toISOString() };
  fs.writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n");
  console.log(JSON.stringify(payload, null, 2));
  process.exit(payload.ok ? 0 : 1);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
