#!/usr/bin/env tsx
/**
 * Post full-film CTA comments on BH Shorts via Data API.
 * Pinning still requires Studio CDP afterward.
 *
 *   cd 07_Content-Ops && npx tsx scripts/youtube-post-bh-short-comments.ts
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
import { postYouTubeTopLevelComment } from "../src/lib/publishing/youtube-package";

const CHANNEL = "UC_esArsDKd3GJvOkeO0DUog";
const LONG_ID = "3xrxdmaOwJI";
const COMMENT =
  "Want to see the full journey into a black hole? Watch the complete episode using the related video link 👇\n" +
  `https://youtu.be/${LONG_ID}`;
const DEFAULT = ["tUAdhOnMW2g", "svYOx07OrIM"];
const OUT = path.resolve(
  process.cwd(),
  "../00_Brand/Channel-Setup/audits/punch_first_shorts_sprint_2026-08-11/API_COMMENT_POST_RESULT.json",
);

async function refreshIfNeeded(connectionId: string) {
  const adapter = new YouTubePublishingAdapter();
  const connection = await prisma.platformConnection.findUnique({ where: { id: connectionId } });
  if (!connection) throw new Error("connection missing");
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    const refreshed = await adapter.refreshConnection(connection);
    if (!refreshed.ok) throw new Error(refreshed.message || "refresh failed");
  }
  const fresh = await prisma.platformConnection.findUnique({ where: { id: connectionId } });
  if (!fresh?.accessTokenEncrypted) throw new Error("No access token");
  return decryptSecret(fresh.accessTokenEncrypted);
}

async function main() {
  getEnv();
  const connection = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection) {
    console.log(JSON.stringify({ ok: false, error: "no_connection" }));
    process.exit(2);
  }
  const accessToken = await refreshIfNeeded(connection.id);
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : DEFAULT;
  const results = [];
  for (const videoId of ids) {
    const posted = await postYouTubeTopLevelComment({
      accessToken,
      channelId: CHANNEL,
      videoId,
      text: COMMENT,
    });
    results.push({ videoId, ...posted });
    console.log(
      JSON.stringify({
        videoId,
        ok: posted.ok,
        message: posted.message,
        commentId: posted.commentId,
      }),
    );
  }
  const out = {
    ok: results.every((r) => r.ok),
    executedAt: new Date().toISOString(),
    parentLongId: LONG_ID,
    results,
  };
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + "\n");
  console.log(JSON.stringify({ ok: out.ok, out: OUT }));
  process.exit(out.ok ? 0 : 1);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
