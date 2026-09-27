#!/usr/bin/env tsx
/**
 * Fresh-id supersede for stale scheduled Orbit Shorts (15 Aug re-upload batch).
 *
 * Default is dry-run. Live writes require --live.
 *
 *   cd 07_Content-Ops
 *   npx tsx scripts/supersede-stale-scheduled-shorts.ts
 *   npx tsx scripts/supersede-stale-scheduled-shorts.ts --live --only eVp9a7f4rWg
 *
 * Does not remint FbRFvSApfOQ or 0j_pgYbCe5E.
 * Related video pill is Studio-only — printed in studioFinish after each upload.
 */
import { execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv, isDryRun } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";

type Job = {
  priority: string;
  old_id: string;
  title: string;
  schedule_utc?: string;
  schedule_uk?: string;
  related: string;
  mp4?: string;
  cover?: string;
  action: string;
};

type Listing = {
  id: string;
  title: string;
  description: string;
  tags: string[];
};

const REPO = path.resolve(__dirname, "../..");
const JOBS_PATH = path.join(
  REPO,
  "00_Brand/Channel-Setup/audits/scheduled_shorts_distribution_audit_2026-09-03/SUPERSEDE_JOBS.json",
);
const LISTINGS_PATH = path.join(
  REPO,
  "00_Brand/Channel-Setup/audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json",
);
const OUT_PATH = path.join(
  REPO,
  "00_Brand/Channel-Setup/audits/scheduled_shorts_distribution_audit_2026-09-03/EXECUTION_RESULT.json",
);
const NEVER = new Set(["FbRFvSApfOQ", "0j_pgYbCe5E"]);

function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function probeDuration(file: string): number {
  const out = execFileSync(
    "ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file],
    { encoding: "utf8" },
  ).trim();
  return Number.parseFloat(out);
}

async function accessToken(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn) throw new Error("No connected YouTube account (Content Ops Settings → Google OAuth)");
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
  const text = await res.text();
  let body: unknown = text;
  try {
    body = JSON.parse(text);
  } catch {
    /* keep text */
  }
  if (!res.ok) throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 400)}`);
  return body as Record<string, unknown>;
}

async function privatizeOld(token: string, videoId: string): Promise<unknown> {
  const got = (await yt(
    token,
    `https://www.googleapis.com/youtube/v3/videos?part=status&id=${encodeURIComponent(videoId)}`,
  )) as { items?: Array<{ status?: Record<string, unknown> }> };
  const status = { ...(got.items?.[0]?.status || {}) };
  delete status.publishAt;
  status.privacyStatus = "private";
  status.selfDeclaredMadeForKids = false;
  return yt(token, "https://www.googleapis.com/youtube/v3/videos?part=status", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: videoId, status }),
  });
}

async function main() {
  getEnv();
  const live = flag("live") && !isDryRun();
  const only = arg("only");
  const jobsFile = JSON.parse(fs.readFileSync(JOBS_PATH, "utf8")) as { jobs: Job[] };
  const listingsFile = JSON.parse(fs.readFileSync(LISTINGS_PATH, "utf8")) as { shorts: Listing[] };
  const listings = new Map(listingsFile.shorts.map((s) => [s.id, s]));

  const adapter = new YouTubePublishingAdapter();
  let token: string | null = null;
  const results: unknown[] = [];

  for (const job of jobsFile.jobs) {
    if (NEVER.has(job.old_id)) {
      results.push({ old_id: job.old_id, skipped: true, reason: "house_lock" });
      continue;
    }
    if (only && job.old_id !== only) continue;

    const row: Record<string, unknown> = {
      old_id: job.old_id,
      priority: job.priority,
      action: job.action,
      live,
    };

    try {
      if (job.action.startsWith("unschedule")) {
        if (!live) {
          row.dryRun = true;
          row.would = "privatize_unschedule";
          results.push(row);
          console.log(JSON.stringify(row));
          continue;
        }
        token = token || (await accessToken());
        row.privatize = await privatizeOld(token, job.old_id);
        row.ok = true;
        results.push(row);
        console.log(JSON.stringify({ old_id: job.old_id, privatized: true }));
        continue;
      }

      if (job.action.includes("verify_upload_date") || job.action.startsWith("move_or_fresh")) {
        row.ok = false;
        row.needs_human = true;
        row.note =
          "Neutron: on Mac mini, check Studio upload date. Fresh-id supersede if before 2026-09-01. Rp_8J6_6IIk → Thu 10 Sep 20:00 launch after Premiere.";
        results.push(row);
        continue;
      }

      if (job.action !== "fresh_id_supersede") {
        row.skipped = true;
        row.reason = "action_not_auto";
        results.push(row);
        continue;
      }

      if (!job.mp4) throw new Error("missing mp4 path");
      const mp4 = path.join(REPO, job.mp4);
      if (!fs.existsSync(mp4)) throw new Error(`mp4 missing: ${mp4}`);
      const duration = probeDuration(mp4);
      row.duration_s = duration;
      if (duration >= 40) throw new Error(`duration ${duration}s >= 40 — abort`);
      if (duration < 20 || duration > 28) {
        row.duration_warn = "outside_22_27_sweet_spot";
      }

      const listing = listings.get(job.old_id);
      if (!listing) throw new Error("no listing pack for old id");
      const thumb = job.cover ? path.join(REPO, job.cover) : null;
      if (thumb && !fs.existsSync(thumb)) throw new Error(`cover missing: ${thumb}`);
      const scheduledAt = job.schedule_utc ? new Date(job.schedule_utc) : null;

      if (!live) {
        row.dryRun = true;
        row.would_upload = {
          title: listing.title,
          schedule: job.schedule_utc,
          related: job.related,
          mp4,
          thumb,
        };
        results.push(row);
        console.log(JSON.stringify({ old_id: job.old_id, dryRun: true, duration_s: duration }));
        continue;
      }

      const connection = await prisma.platformConnection.findFirst({
        where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
        orderBy: { updatedAt: "desc" },
      });
      if (!connection?.accessTokenEncrypted) throw new Error("No connected YouTube account");
      token = token || (await accessToken());
      const fresh = await prisma.platformConnection.findUnique({ where: { id: connection.id } });
      if (!fresh) throw new Error("connection vanished");

      const result = await adapter.publish(
        {
          id: `supersede-${job.old_id}-${Date.now()}`,
          platform: "youtube_shorts",
          title: listing.title,
          caption: listing.description,
          uploadStatus: "ready",
          privacyStatus: "private",
          madeForKids: false,
          mediaFilePath: mp4,
          scheduledAt,
          thumbnailPath: thumb,
          contentFormat: "shorts",
        },
        fresh,
        {
          dryRun: false,
          workerId: "supersede-stale-scheduled-shorts",
          jobId: `supersede-${job.old_id}`,
          attemptNumber: 1,
          accessToken: token,
        },
      );
      row.upload = {
        ok: result.success,
        platformPostId: result.platformPostId,
        platformUrl: result.platformUrl,
        message: result.message,
        scheduledFor: result.scheduledFor,
      };
      if (!result.success || !result.platformPostId) {
        throw new Error(result.message || "upload failed");
      }
      row.new_id = result.platformPostId;
      row.studio_related = {
        required: true,
        target: job.related,
        url: `https://studio.youtube.com/video/${result.platformPostId}/edit`,
        note: "Data API cannot set Related. Desktop Studio only. Then apply 9:16 cover in Studio (API thumbs letterbox Shorts).",
      };
      row.privatize_old = await privatizeOld(token, job.old_id);
      row.ok = true;
      results.push(row);
      console.log(
        JSON.stringify({
          old_id: job.old_id,
          new_id: result.platformPostId,
          schedule: job.schedule_uk,
          related_pending_studio: job.related,
        }),
      );
    } catch (err) {
      row.ok = false;
      row.error = err instanceof Error ? err.message : String(err);
      results.push(row);
      console.error(JSON.stringify({ old_id: job.old_id, error: row.error }));
    }
  }

  const report = {
    started_note: live ? "LIVE" : "DRY_RUN",
    finished_at: new Date().toISOString(),
    live,
    results,
  };
  fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  fs.writeFileSync(OUT_PATH, JSON.stringify(report, null, 2) + "\n");
  console.log(`wrote ${OUT_PATH}`);
  const failed = results.filter((r) => (r as { ok?: boolean }).ok === false);
  process.exit(failed.length ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
