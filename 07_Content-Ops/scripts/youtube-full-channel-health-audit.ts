/**
 * Full channel health audit (read-only): enumerate uploads playlist,
 * classify visibility, score thumbnails, compare to approved calendar.
 */
import { PrismaClient } from "@prisma/client";
import { decryptSecret } from "../src/lib/security/token-crypto";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve } from "path";

const ROOT = resolve(__dirname, "../..");
const AUD = resolve(ROOT, "00_Brand/Channel-Setup/audits/full_channel_health_audit_2026-08-12");
const ENV = resolve(__dirname, "../.env");

for (const line of readFileSync(ENV, "utf8").split("\n")) {
  const m = line.match(/^([^#=]+)=(.*)$/);
  if (m && !process.env[m[1].trim()]) {
    process.env[m[1].trim()] = m[2].trim().replace(/^"|"$/g, "");
  }
}

function parseDur(iso?: string | null): number | null {
  if (!iso) return null;
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!m) return null;
  return Number(m[1] || 0) * 3600 + Number(m[2] || 0) * 60 + Number(m[3] || 0);
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

async function yt(access: string, path: string) {
  const res = await fetch(`https://www.googleapis.com/youtube/v3/${path}`, {
    headers: { Authorization: `Bearer ${access}` },
  });
  const json = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(json));
  return json;
}

async function downloadThumb(url: string, dest: string): Promise<number> {
  const res = await fetch(url);
  if (!res.ok) return -1;
  const buf = Buffer.from(await res.arrayBuffer());
  writeFileSync(dest, buf);
  return buf.length;
}

/** Very small / near-uniform files often render as blank in Studio mobile. */
function thumbRisk(bytes: number): "LIKELY_BLANK" | "WEAK" | "OK" | "MISSING" {
  if (bytes < 0) return "MISSING";
  if (bytes < 8000) return "LIKELY_BLANK";
  if (bytes < 25000) return "WEAK";
  return "OK";
}

async function main() {
  mkdirSync(resolve(AUD, "thumbs"), { recursive: true });
  mkdirSync(resolve(AUD, "api"), { recursive: true });
  const prisma = new PrismaClient();
  try {
    const access = await getAccess(prisma);
    const now = new Date();

    const ch = await yt(access, "channels?part=snippet,contentDetails,statistics&mine=true");
    const channel = ch.items?.[0];
    const uploads = channel?.contentDetails?.relatedPlaylists?.uploads;
    if (!uploads) throw new Error("no uploads playlist");

    // Enumerate entire uploads playlist
    const playlistIds: string[] = [];
    let pageToken: string | undefined;
    do {
      const q = new URLSearchParams({
        part: "contentDetails,snippet",
        playlistId: uploads,
        maxResults: "50",
      });
      if (pageToken) q.set("pageToken", pageToken);
      const pl = await yt(access, `playlistItems?${q}`);
      for (const it of pl.items || []) {
        const id = it.contentDetails?.videoId;
        if (id) playlistIds.push(id);
      }
      pageToken = pl.nextPageToken;
    } while (pageToken);

    // Batch videos
    const videos: any[] = [];
    for (let i = 0; i < playlistIds.length; i += 50) {
      const chunk = playlistIds.slice(i, i + 50);
      const resp = await yt(
        access,
        `videos?part=snippet,status,contentDetails,statistics&id=${chunk.join(",")}`,
      );
      videos.push(...(resp.items || []));
    }

    // Intent sources
    const cal = JSON.parse(
      readFileSync(
        resolve(ROOT, "00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/FINAL_APPROVED_RELEASE_CALENDAR.json"),
        "utf8",
      ),
    );
    const recon = JSON.parse(
      readFileSync(
        resolve(ROOT, "00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/FINAL_16_TO_13_RECONCILIATION.json"),
        "utf8",
      ),
    );
    const registryPath = resolve(ROOT, "00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json");
    const registry = existsSync(registryPath) ? JSON.parse(readFileSync(registryPath, "utf8")) : {};

    const approvedById = new Map<string, any>();
    for (const item of cal.items || []) approvedById.set(item.youtubeId, item);
    const obsolete = new Set<string>(recon.obsoleteIds || []);

    // Production duplicate / hold maps
    const historicalDup = new Set<string>();
    const superseded = new Map<string, string>(); // old -> canonical
    const intentionalPrivate = new Set<string>([
      ...obsolete,
      "dPMJQp2gMNc",
      "rFJoOdQAc9c",
      "HvAKGjx4lv0",
      "icedH_gK8JE",
      "Web2otrTcT0",
      "1qts3tIsg9c",
      "mGwSCdgxQO4",
      "QW0cn-O9k5g",
      "yTljUMV5Gms",
      "5MysOlOqLDY",
      "Tw2OdQABU4E",
      "SGv-wH0XbtI",
      "oFzKgHbAw4M",
      "IsPLdq0oSe8",
    ]);
    const indexes = [
      "001_Will-We-Ever-Meet-Aliens",
      "002_What-Happens-If-You-Fall-Into-A-Black-Hole",
      "003_Exoplanets-Strangest-Alien-Worlds",
      "004_JWST-Discoveries-That-Change-Everything",
    ];
    for (const ep of indexes) {
      const p = resolve(ROOT, `02_Video-Projects/${ep}/10_Shorts/SHORTS_UPLOAD_INDEX.json`);
      if (!existsSync(p)) continue;
      const idx = JSON.parse(readFileSync(p, "utf8"));
      for (const s of idx.shorts || []) {
        const canon = s.youtube_video_id || s.video_id;
        for (const hid of s.historical_duplicate_ids || []) {
          historicalDup.add(hid);
          if (canon) superseded.set(hid, canon);
        }
        for (const key of ["old_video_id", "previous_video_id", "smooth_cfr_video_id"]) {
          if (s[key] && canon) {
            historicalDup.add(s[key]);
            superseded.set(s[key], canon);
          }
        }
        if (s.reserve || s.status === "reserve") {
          if (canon) intentionalPrivate.add(canon);
        }
      }
    }
    // Known unexpected public superseded from prior forensic
    for (const [old, canon] of Object.entries({
      "z-DLqoSoEBo": "1HuV8o3gOss",
      UWwNKYf_aU8: "dPMJQp2gMNc",
    })) {
      historicalDup.add(old);
      superseded.set(old, canon);
    }

    const rows = [];
    for (const it of videos) {
      const dur = parseDur(it.contentDetails?.duration);
      const isShort = dur != null && dur <= 180;
      const privacy = it.status?.privacyStatus;
      const publishAt = it.status?.publishAt || null;
      let state: string = privacy;
      if (privacy === "private" && publishAt) state = "scheduled";
      const thumbs = it.snippet?.thumbnails || {};
      const thumbUrl = thumbs.maxres?.url || thumbs.high?.url || thumbs.default?.url || null;
      let thumbBytes = -1;
      let thumbRiskLabel: ReturnType<typeof thumbRisk> = "MISSING";
      if (thumbUrl && isShort) {
        const dest = resolve(AUD, "thumbs", `${it.id}_hq.jpg`);
        // Prefer high for size signal (maxres can be large even when list shows blank)
        const probeUrl = thumbs.high?.url || thumbUrl;
        thumbBytes = await downloadThumb(probeUrl, dest);
        thumbRiskLabel = thumbRisk(thumbBytes);
      }

      const approved = approvedById.get(it.id);
      let intended: string | null = null;
      if (approved) {
        const dt = new Date(approved.proposedUTC || approved.livePublishAt);
        intended = dt <= now ? "PUBLIC_BY_NOW" : "SCHEDULED_FUTURE";
      } else if (intentionalPrivate.has(it.id)) {
        intended = "INTENTIONAL_PRIVATE";
      } else if (historicalDup.has(it.id) || superseded.has(it.id)) {
        intended = "SUPERSEDED_OR_DUPLICATE";
      }

      let issue: string | null = null;
      if (state === "public" && intended === "INTENTIONAL_PRIVATE") issue = "UNEXPECTED_PUBLIC_SHOULD_BE_PRIVATE";
      if (state === "public" && intended === "SUPERSEDED_OR_DUPLICATE") issue = "UNEXPECTED_PUBLIC_SUPERSEDED";
      if (state === "private" && !publishAt && intended === "PUBLIC_BY_NOW") issue = "OVERDUE_CANONICAL_PRIVATE";
      if (state === "scheduled" && intended === "PUBLIC_BY_NOW") {
        const dt = new Date(publishAt);
        if (dt <= now) issue = "SCHEDULE_PAST_DUE_STILL_PRIVATE";
      }
      if (isShort && (thumbRiskLabel === "LIKELY_BLANK" || thumbRiskLabel === "WEAK")) {
        issue = issue ? `${issue}+THUMB_${thumbRiskLabel}` : `THUMB_${thumbRiskLabel}`;
      }
      if (state === "public" && !intended && isShort) issue = issue || "PUBLIC_SHORT_NOT_IN_APPROVED_PLAN";

      rows.push({
        id: it.id,
        title: it.snippet?.title,
        isShort,
        durationSec: dur,
        state,
        privacy,
        publishAt,
        publishedAt: it.snippet?.publishedAt,
        views: Number(it.statistics?.viewCount || 0),
        likes: Number(it.statistics?.likeCount || 0),
        comments: Number(it.statistics?.commentCount || 0),
        intended,
        approvedSlot: approved
          ? { date: approved.date, timeLocal: approved.timeLocal, type: approved.type }
          : null,
        supersededBy: superseded.get(it.id) || null,
        thumbBytes,
        thumbRisk: isShort ? thumbRiskLabel : null,
        thumbUrl,
        issue,
      });
    }

    const shorts = rows.filter((r) => r.isShort);
    const longs = rows.filter((r) => !r.isShort);

    const summary = {
      capturedAt: now.toISOString(),
      channelId: channel.id,
      channelTitle: channel.snippet?.title,
      stats: channel.statistics,
      totals: {
        uploadsPlaylist: playlistIds.length,
        returned: videos.length,
        shorts: shorts.length,
        longs: longs.length,
        publicShorts: shorts.filter((r) => r.state === "public").length,
        scheduledShorts: shorts.filter((r) => r.state === "scheduled").length,
        privateShorts: shorts.filter((r) => r.state === "private").length,
        publicLongs: longs.filter((r) => r.state === "public").length,
        scheduledLongs: longs.filter((r) => r.state === "scheduled").length,
        privateLongs: longs.filter((r) => r.state === "private").length,
      },
      issues: rows.filter((r) => r.issue).map((r) => ({
        id: r.id,
        title: r.title,
        state: r.state,
        intended: r.intended,
        issue: r.issue,
        thumbRisk: r.thumbRisk,
        thumbBytes: r.thumbBytes,
        publishAt: r.publishAt,
        supersededBy: r.supersededBy,
      })),
      publicShorts: shorts.filter((r) => r.state === "public"),
      scheduled: rows
        .filter((r) => r.state === "scheduled")
        .sort((a, b) => String(a.publishAt).localeCompare(String(b.publishAt))),
      approvedCalendarCheck: {
        expectedPublicByNow: [...approvedById.entries()]
          .filter(([, v]) => v.type === "shorts" && new Date(v.proposedUTC || v.livePublishAt) <= now)
          .map(([id, v]) => ({ id, title: v.title, proposedUTC: v.proposedUTC || v.livePublishAt })),
        expectedStillScheduled: [...approvedById.entries()]
          .filter(([, v]) => new Date(v.proposedUTC || v.livePublishAt) > now)
          .map(([id, v]) => ({
            id,
            type: v.type,
            title: v.title,
            proposedUTC: v.proposedUTC || v.livePublishAt,
          })),
      },
    };

    // Mark missing expected public
    for (const exp of summary.approvedCalendarCheck.expectedPublicByNow) {
      const live = rows.find((r) => r.id === exp.id);
      if (!live || live.state !== "public") {
        summary.issues.push({
          id: exp.id,
          title: exp.title,
          state: live?.state || "MISSING",
          intended: "PUBLIC_BY_NOW",
          issue: "EXPECTED_PUBLIC_MISSING_OR_NOT_PUBLIC",
          thumbRisk: live?.thumbRisk,
          thumbBytes: live?.thumbBytes,
          publishAt: live?.publishAt,
          supersededBy: null,
        });
      }
    }
    // Mark missing/wrong schedule for future approved
    for (const exp of summary.approvedCalendarCheck.expectedStillScheduled) {
      const live = rows.find((r) => r.id === exp.id);
      if (!live) {
        summary.issues.push({
          id: exp.id,
          title: exp.title,
          state: "MISSING",
          intended: "SCHEDULED_FUTURE",
          issue: "APPROVED_SCHEDULE_ID_MISSING",
          thumbRisk: null,
          thumbBytes: -1,
          publishAt: null,
          supersededBy: null,
        });
      } else if (live.state === "public" && exp.type === "shorts") {
        // natural fire OK if past; if future date still public early:
        if (new Date(exp.proposedUTC) > now) {
          summary.issues.push({
            id: exp.id,
            title: exp.title,
            state: live.state,
            intended: "SCHEDULED_FUTURE",
            issue: "EARLY_PUBLIC_BEFORE_APPROVED_SLOT",
            thumbRisk: live.thumbRisk,
            thumbBytes: live.thumbBytes,
            publishAt: live.publishAt,
            supersededBy: null,
          });
        }
      } else if (live.state !== "scheduled" && new Date(exp.proposedUTC) > now) {
        summary.issues.push({
          id: exp.id,
          title: exp.title,
          state: live.state,
          intended: "SCHEDULED_FUTURE",
          issue: "APPROVED_FUTURE_NOT_SCHEDULED",
          thumbRisk: live.thumbRisk,
          thumbBytes: live.thumbBytes,
          publishAt: live.publishAt,
          supersededBy: null,
        });
      } else if (live.publishAt && live.publishAt !== exp.proposedUTC && new Date(exp.proposedUTC) > now) {
        // allow Z formatting differences
        const a = new Date(live.publishAt).toISOString();
        const b = new Date(exp.proposedUTC).toISOString();
        if (a !== b) {
          summary.issues.push({
            id: exp.id,
            title: exp.title,
            state: live.state,
            intended: "SCHEDULED_FUTURE",
            issue: `SCHEDULE_TIMESTAMP_MISMATCH live=${a} expected=${b}`,
            thumbRisk: live.thumbRisk,
            thumbBytes: live.thumbBytes,
            publishAt: live.publishAt,
            supersededBy: null,
          });
        }
      }
    }

    writeFileSync(resolve(AUD, "api/LIVE_CATALOGUE.json"), JSON.stringify({ rows, summary: summary.totals }, null, 2) + "\n");
    writeFileSync(resolve(AUD, "AUDIT_SUMMARY.json"), JSON.stringify(summary, null, 2) + "\n");
    console.log(
      JSON.stringify(
        {
          totals: summary.totals,
          issueCount: summary.issues.length,
          issues: summary.issues,
          publicShortIds: summary.publicShorts.map((s) => s.id),
          scheduled: summary.scheduled.map((s) => ({ id: s.id, at: s.publishAt, short: s.isShort })),
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
