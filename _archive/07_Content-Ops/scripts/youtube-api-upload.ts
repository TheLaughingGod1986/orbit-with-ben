#!/usr/bin/env tsx
/**
 * Orbit YouTube Data API upload (default path — prefer over Studio CDP).
 *
 * Usage:
 *   npx tsx scripts/youtube-api-upload.ts --file /path/to.mp4 --title "..." --dry-run
 *   npx tsx scripts/youtube-api-upload.ts --file /path/to.mp4 --title "..." \
 *     --description "..." --privacy private --made-for-kids false \
 *     --schedule 2026-08-10T18:00:00Z --thumbnail /path/to.jpg --format longform
 *
 * Requires: Google OAuth connected via /settings/connections (youtube_shorts),
 * ORBIT_TOKEN_ENCRYPTION_KEY + GOOGLE_CLIENT_* in .env.
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv, isDryRun } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function parseBool(v: string | undefined, fallback: boolean): boolean {
  if (v == null) return fallback;
  const s = v.toLowerCase();
  if (["1", "true", "yes"].includes(s)) return true;
  if (["0", "false", "no"].includes(s)) return false;
  throw new Error(`Invalid boolean for flag: ${v}`);
}

async function main() {
  getEnv();
  const file = arg("file");
  const title = arg("title");
  if (!file || !title) {
    console.error(
      "Usage: youtube-api-upload.ts --file <mp4> --title <title> [--description ...] [--privacy private|public|unlisted] [--made-for-kids false] [--schedule ISO] [--thumbnail path] [--format shorts|longform] [--dry-run]",
    );
    process.exit(1);
  }
  const abs = path.resolve(file);
  if (!fs.existsSync(abs)) {
    console.error(`File not found: ${abs}`);
    process.exit(1);
  }

  const description = arg("description") || "";
  const privacy = (arg("privacy") || "private") as "private" | "public" | "unlisted";
  const madeForKids = parseBool(arg("made-for-kids"), false);
  const scheduleRaw = arg("schedule");
  const scheduledAt = scheduleRaw ? new Date(scheduleRaw) : null;
  if (scheduleRaw && Number.isNaN(scheduledAt!.getTime())) {
    console.error(`Invalid --schedule ISO date: ${scheduleRaw}`);
    process.exit(1);
  }
  const thumbnail = arg("thumbnail");
  if (thumbnail && !fs.existsSync(path.resolve(thumbnail))) {
    console.error(`Thumbnail not found: ${thumbnail}`);
    process.exit(1);
  }
  const format = (arg("format") || "shorts") as "shorts" | "longform";
  const dryRun = flag("dry-run") || isDryRun();

  const connection = await prisma.platformConnection.findFirst({
    where: {
      platform: "youtube_shorts",
      connectionStatus: "connected",
      disconnectedAt: null,
    },
    orderBy: { updatedAt: "desc" },
  });
  if (!connection?.accessTokenEncrypted) {
    console.error(
      "No connected YouTube account. Open Content Ops → Settings → Connections and connect Google OAuth first.",
    );
    process.exit(1);
  }

  const adapter = new YouTubePublishingAdapter();

  // Refresh if near expiry
  if (
    connection.accessTokenExpiresAt &&
    connection.accessTokenExpiresAt.getTime() < Date.now() + 60_000 &&
    adapter.refreshConnection
  ) {
    const refreshed = await adapter.refreshConnection(connection);
    if (!refreshed.ok) {
      console.error(`Token refresh failed: ${refreshed.message}`);
      process.exit(1);
    }
  }

  const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
  if (!fresh?.accessTokenEncrypted) {
    console.error("Missing access token after refresh");
    process.exit(1);
  }
  const accessToken = decryptSecret(fresh.accessTokenEncrypted);

  const result = await adapter.publish(
    {
      id: `cli-${Date.now()}`,
      platform: "youtube_shorts",
      title,
      caption: description,
      uploadStatus: "ready",
      privacyStatus: privacy,
      madeForKids,
      mediaFilePath: abs,
      scheduledAt,
      thumbnailPath: thumbnail ? path.resolve(thumbnail) : null,
      contentFormat: format,
    },
    fresh,
    {
      dryRun,
      workerId: "youtube-api-upload-cli",
      jobId: `cli-${Date.now()}`,
      attemptNumber: 1,
      accessToken,
    },
  );

  console.log(
    JSON.stringify(
      {
        ok: result.success,
        published: result.published,
        scheduledOnPlatform: result.scheduledOnPlatform || false,
        scheduledFor: result.scheduledFor || null,
        platformPostId: result.platformPostId || null,
        platformUrl: result.platformUrl || null,
        message: result.message,
        method: result.method,
        dryRun,
        responseSummary: result.responseSummary || null,
      },
      null,
      2,
    ),
  );

  if (!result.success) process.exit(1);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => prisma.$disconnect());
