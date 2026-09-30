/**
 * YouTube Data API for the local scripts: the channel token, video records and the
 * channel's scheduled uploads. The login is YOUTUBE_REFRESH_TOKEN in 07_Content-Ops/.env
 * (made once by scripts/youtube-auth.ts) with GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET.
 * No database: the hosted ops app was retired on 27 Sep 2026.
 */
import { parseIsoDuration, type YouTubeVideo } from "@/lib/publishing/buffer-mirror";

const API = "https://www.googleapis.com/youtube/v3";

let cached: { token: string; expiresAt: number } | null = null;

/** A fresh access token from the stored refresh token. Never logs either. */
export async function getYouTubeAccessToken(): Promise<string> {
  if (cached && cached.expiresAt > Date.now() + 60_000) return cached.token;
  const { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN } = process.env;
  if (!GOOGLE_CLIENT_ID || !GOOGLE_CLIENT_SECRET) throw new Error("GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET missing from .env");
  if (!YOUTUBE_REFRESH_TOKEN) throw new Error("YOUTUBE_REFRESH_TOKEN missing from .env: run `npx tsx --env-file=.env scripts/youtube-auth.ts` once");
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      refresh_token: YOUTUBE_REFRESH_TOKEN,
      grant_type: "refresh_token",
    }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.access_token) {
    const reason = body.error === "invalid_grant" ? "the YouTube login expired or was revoked; run scripts/youtube-auth.ts again" : body.error || res.status;
    throw new Error(`YouTube token refresh failed: ${reason}`);
  }
  cached = { token: body.access_token as string, expiresAt: Date.now() + Number(body.expires_in || 3600) * 1000 };
  return cached.token;
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

/** The channel's most recent uploads (newest first in the uploads playlist). */
async function listRecentUploads(token: string, recent = 50): Promise<YouTubeVideo[]> {
  const ch = await get(token, `${API}/channels?part=contentDetails&mine=true`);
  const uploads: string | undefined = ch.items?.[0]?.contentDetails?.relatedPlaylists?.uploads;
  if (!uploads) return [];
  const pl = await get(token, `${API}/playlistItems?part=contentDetails&maxResults=${recent}&playlistId=${encodeURIComponent(uploads)}`);
  const ids: string[] = (pl.items ?? []).map((i: { contentDetails?: { videoId?: string } }) => i.contentDetails?.videoId).filter(Boolean);
  return [...(await fetchYouTubeVideos(token, ids)).values()];
}

/** The channel's most recent uploads that are private with a future go-public time. */
export async function listScheduledUploads(token: string, now = new Date(), recent = 50): Promise<YouTubeVideo[]> {
  return (await listRecentUploads(token, recent))
    .filter((v) => v.privacyStatus === "private" && v.publishAt && Date.parse(v.publishAt) > now.getTime())
    .sort((a, b) => Date.parse(a.publishAt!) - Date.parse(b.publishAt!));
}

/** Uploads that went public within `withinMs` (default 24 h): published straight away, or after the last check. */
export async function listRecentlyPublic(token: string, now = new Date(), withinMs = 24 * 60 * 60 * 1000, recent = 50): Promise<YouTubeVideo[]> {
  return (await listRecentUploads(token, recent)).filter(
    (v) => v.privacyStatus === "public" && v.publishedAt && now.getTime() - Date.parse(v.publishedAt) <= withinMs,
  );
}
