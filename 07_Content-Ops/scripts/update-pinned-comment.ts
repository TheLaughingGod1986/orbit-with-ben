#!/usr/bin/env tsx
/**
 * Keep the pinned comment on each long current (STUDIO_PLAYBOOK.md §9).
 * Text = the film's open question + a thank-you with the last subscriber milestone
 * (no number under 10). Only the comment text changes; pinning stays a Studio step
 * because the YouTube API cannot pin.
 *
 *   # post the first comment on a new long, then pin it by hand in Studio
 *   npx tsx --env-file=.env scripts/update-pinned-comment.ts --create --video <id> --question "…?"
 *   # weekly (after the Monday report): refresh every listed comment
 *   npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run
 *   npx tsx --env-file=.env scripts/update-pinned-comment.ts
 *
 * Config: 00_Brand/Channel-Setup/PINNED_COMMENTS.json
 */
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";
import { buildPinnedCommentText, DEFAULT_MILESTONES } from "../src/lib/publishing/pinned-comment";

const CONFIG = path.resolve(__dirname, "../../00_Brand/Channel-Setup/PINNED_COMMENTS.json");

type Entry = { videoId: string; title?: string; commentId: string; question: string };
type Config = { note?: string; milestones?: number[]; cadence?: string; comments: Entry[] };

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
  const dry = process.argv.includes("--dry-run");
  const config: Config = JSON.parse(fs.readFileSync(CONFIG, "utf8"));
  const token = await accessToken();
  const channel = await yt(token, "https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true");
  const subscribers = Number(channel.items?.[0]?.statistics?.subscriberCount ?? 0);
  const textFor = (question: string) =>
    buildPinnedCommentText({
      question,
      subscribers,
      milestones: config.milestones ?? DEFAULT_MILESTONES,
      cadence: config.cadence,
    });

  if (process.argv.includes("--create")) {
    const videoId = arg("video");
    const question = arg("question");
    if (!videoId || !question) throw new Error("--create needs --video <id> and --question \"…\"");
    if (config.comments.some((c) => c.videoId === videoId && c.commentId)) {
      throw new Error(`${videoId} already has a comment in PINNED_COMMENTS.json — refresh it instead of posting twice.`);
    }
    const text = textFor(question);
    if (dry) {
      console.log(JSON.stringify({ videoId, dryRun: true, text }, null, 2));
      return;
    }
    const thread = await yt(token, "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ snippet: { videoId, topLevelComment: { snippet: { textOriginal: text } } } }),
    });
    const commentId = thread.snippet?.topLevelComment?.id as string;
    config.comments = config.comments.filter((c) => c.videoId !== videoId);
    config.comments.push({ videoId, commentId, question });
    fs.writeFileSync(CONFIG, JSON.stringify(config, null, 2) + "\n");
    console.log(JSON.stringify({ videoId, commentId, next: "Pin this comment in Studio (the API cannot pin)." }, null, 2));
    return;
  }

  const results: unknown[] = [];
  for (const entry of config.comments) {
    if (!entry.commentId) {
      results.push({ videoId: entry.videoId, skipped: "no commentId yet — run --create first" });
      continue;
    }
    const got = await yt(token, `https://www.googleapis.com/youtube/v3/comments?part=snippet&id=${entry.commentId}`);
    const current: string | undefined = got.items?.[0]?.snippet?.textOriginal;
    if (current === undefined) {
      results.push({ videoId: entry.videoId, error: "comment not found" });
      continue;
    }
    const next = textFor(entry.question);
    if (current === next) {
      results.push({ videoId: entry.videoId, unchanged: true });
      continue;
    }
    if (!dry) {
      await yt(token, "https://www.googleapis.com/youtube/v3/comments?part=snippet", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: entry.commentId, snippet: { textOriginal: next } }),
      });
    }
    results.push({ videoId: entry.videoId, updated: !dry, dryRun: dry, from: current, to: next });
  }
  console.log(JSON.stringify({ subscribers, dry, results }, null, 2));
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
