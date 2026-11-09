/**
 * Shared types and checks for the Buffer mirror's media host. Buffer takes no uploads and fetches each file
 * when the post goes out, so the Short's mp4 (or the long's thumbnail) is put on a public host first.
 * The only host is the Cloudflare R2 bucket (media-host-r2.ts). The Vercel Blob fallback was removed on
 * 29 Oct 2026 (the Hobby store was suspended over its limits on 15 Oct). Without the R2_*
 * keys the mirror stops with an error rather than hosting anywhere else.
 */
export const MEDIA_TYPES: Record<string, string> = {
  ".mp4": "video/mp4",
  ".mov": "video/quicktime",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
};

export type HostFile = (localPath: string, pathname: string) => Promise<string>;

/** Only files this mirror put in the R2 bucket (under social/) are ever deleted by it. Old Vercel Blob URLs are not. */
export function isOwnMediaUrl(url: string, r2PublicUrl: string | undefined = process.env.R2_PUBLIC_URL): boolean {
  try {
    const u = new URL(url);
    if (u.protocol !== "https:" || !u.pathname.startsWith("/social/")) return false;
    return !!r2PublicUrl && u.hostname === new URL(r2PublicUrl).hostname;
  } catch {
    return false;
  }
}

export type StoredMedia = { url: string; pathname: string; uploadedAt: Date };

/** Buffer needs a direct 200 with the right type, now and when the post goes out. */
export async function checkMediaUrl(url: string, want: "video" | "image", fetchImpl: typeof fetch = fetch): Promise<string | null> {
  try {
    const res = await fetchImpl(url, { method: "HEAD", redirect: "manual" });
    if (res.status !== 200) return `${url} answered ${res.status} (Buffer needs a direct 200, no redirect or login)`;
    const type = res.headers.get("content-type") || "";
    if (!type.startsWith(`${want}/`)) return `${url} is ${type || "no content-type"}, not ${want}/*`;
    return null;
  } catch (e) {
    return `${url} unreachable: ${(e as Error).message}`;
  }
}
