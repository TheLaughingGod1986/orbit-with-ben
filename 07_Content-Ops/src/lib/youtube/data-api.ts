/**
 * YouTube Data API reads for the Buffer mirror: the saved channel token, video
 * records, and the channel's scheduled uploads. Used by scripts/buffer-mirror.ts,
 * the package upload and the daily /api/cron/buffer-check job.
 */
import { prisma } from "@/lib/storage/prisma";
import { getEnv } from "@/lib/env";
import { decryptSecret, encryptSecret } from "@/lib/security/token-crypto";
import { parseIsoDuration, type YouTubeVideo } from "@/lib/publishing/buffer-mirror";

const API = "https://www.googleapis.com/youtube/v3";

/** Access token for the connected channel, refreshed (and saved) when a refresh token exists. */
export async function getYouTubeAccessToken(): Promise<string> {
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
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  });
  const body = await res.json();
  if (!res.ok || !body.access_token) throw new Error(`YouTube token refresh failed (${res.status})`);
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

async function get(token: string, url: string) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url.split("?")[0]} ${res.status} ${JSON.stringify(body).slice(0, 300)}`);
  return body;
}

type ApiVideo = {
  id: string;
  snippet?: { title?: string; description?: string; tags?: string[]; publishedAt?: string };
  status?: { privacyStatus?: string; publishAt?: string; containsSyntheticMedia?: boolean };
  contentDetails?: { duration?: string };
};

export function toYouTubeVideo(item: ApiVideo): YouTubeVideo {
  return {
    id: item.id,
    title: item.snippet?.title ?? "",
    description: item.snippet?.description ?? "",
    tags: item.snippet?.tags ?? [],
    durationSeconds: parseIsoDuration(item.contentDetails?.duration),
    privacyStatus: item.status?.privacyStatus ?? "unknown",
    publishAt: item.status?.publishAt ?? null,
    publishedAt: item.snippet?.publishedAt ?? null,
    containsSyntheticMedia: Boolean(item.status?.containsSyntheticMedia),
  };
}

/** Videos by id. Ids YouTube doesn't return (deleted, not ours) are absent from the map. */
export async function fetchYouTubeVideos(token: string, ids: string[]): Promise<Map<string, YouTubeVideo>> {
  const out = new Map<string, YouTubeVideo>();
  const unique = [...new Set(ids)];
  for (let i = 0; i < unique.length; i += 50) {
    const batch = unique.slice(i, i + 50).map(encodeURIComponent).join(",");
    const body = await get(token, `${API}/videos?part=snippet,status,contentDetails&id=${batch}`);
    for (const item of (body.items ?? []) as ApiVideo[]) out.set(item.id, toYouTubeVideo(item));
  }
  return out;
}

/** The channel's most recent uploads that are private with a future go-public time. */
export async function listScheduledUploads(token: string, now = new Date(), recent = 50): Promise<YouTubeVideo[]> {
  const ch = await get(token, `${API}/channels?part=contentDetails&mine=true`);
  const uploads: string | undefined = ch.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
  if (!uploads) return [];
  const pl = await get(token, `${API}/playlistItems?part=contentDetails&maxResults=${recent}&playlistId=${encodeURIComponent(uploads)}`);
  const ids: string[] = (pl.items ?? []).map((i: { contentDetails?: { videoId?: string } }) => i.contentDetails?.videoId).filter(Boolean);
  const videos = await fetchYouTubeVideos(token, ids);
  return [...videos.values()]
    .filter((v) => v.privacyStatus === "private" && v.publishAt && Date.parse(v.publishAt) > now.getTime())
    .sort((a, b) => Date.parse(a.publishAt!) - Date.parse(b.publishAt!));
}
