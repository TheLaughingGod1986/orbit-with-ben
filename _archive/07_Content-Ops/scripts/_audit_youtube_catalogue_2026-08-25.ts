#!/usr/bin/env tsx
import fs from "fs";
import path from "path";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";

const OUT = path.resolve(
  __dirname,
  "../../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-08-25/youtube_catalogue.json",
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

async function yt(token: string, url: string) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

function parseIsoDuration(iso?: string): number | null {
  if (!iso) return null;
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!m) return null;
  return Number(m[1] || 0) * 3600 + Number(m[2] || 0) * 60 + Number(m[3] || 0);
}

async function main() {
  const token = await accessToken();
  const ch = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails,brandingSettings&mine=true",
  );
  const channel = ch.items?.[0];
  const uploads = channel?.contentDetails?.relatedPlaylists?.uploads;

  const searchIds: string[] = [];
  let page: string | undefined;
  do {
    const q = new URLSearchParams({
      part: "id",
      forMine: "true",
      type: "video",
      maxResults: "50",
    });
    if (page) q.set("pageToken", page);
    const s = await yt(token, `https://www.googleapis.com/youtube/v3/search?${q}`);
    for (const it of s.items || []) if (it.id?.videoId) searchIds.push(it.id.videoId);
    page = s.nextPageToken;
  } while (page);

  const uploadIds: string[] = [];
  page = undefined;
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
        if (id) uploadIds.push(id);
      }
      page = s.nextPageToken;
    } while (page);
  }

  const allIds = [...new Set([...searchIds, ...uploadIds])];
  const videos: Record<string, unknown>[] = [];
  for (let i = 0; i < allIds.length; i += 50) {
    const chunk = allIds.slice(i, i + 50);
    const q = new URLSearchParams({
      part: "snippet,contentDetails,statistics,status",
      id: chunk.join(","),
      maxResults: "50",
    });
    const v = await yt(token, `https://www.googleapis.com/youtube/v3/videos?${q}`);
    for (const it of v.items || []) {
      const dur = parseIsoDuration(it.contentDetails?.duration);
      videos.push({
        id: it.id,
        title: it.snippet?.title,
        publishedAt: it.snippet?.publishedAt,
        privacy: it.status?.privacyStatus,
        publishAt: it.status?.publishAt || null,
        madeForKids: it.status?.madeForKids,
        duration: it.contentDetails?.duration,
        duration_s: dur,
        isShort: dur != null && dur > 0 && dur <= 61,
        views: Number(it.statistics?.viewCount || 0),
        likes: Number(it.statistics?.likeCount || 0),
        comments: Number(it.statistics?.commentCount || 0),
        inUploadsPlaylist: uploadIds.includes(it.id),
        inSearchForMine: searchIds.includes(it.id),
      });
    }
  }

  videos.sort((a, b) => String(b.publishedAt || "").localeCompare(String(a.publishedAt || "")));
  const payload = {
    pulled_at: new Date().toISOString(),
    channel: {
      id: channel?.id,
      title: channel?.snippet?.title,
      customUrl: channel?.snippet?.customUrl,
      subs: Number(channel?.statistics?.subscriberCount || 0),
      hiddenSubs: channel?.statistics?.hiddenSubscriberCount,
      views: Number(channel?.statistics?.viewCount || 0),
      videoCount: Number(channel?.statistics?.videoCount || 0),
    },
    counts: {
      searchForMine: searchIds.length,
      uploadsPlaylist: uploadIds.length,
      unique: videos.length,
      missingFromUploads: videos.filter((v) => !v.inUploadsPlaylist).map((v) => v.id),
    },
    videos,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(payload, null, 2));
  console.log("WROTE", OUT, "videos", videos.length);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
