/**
 * Public, permanent URLs for the Buffer mirror's media. Buffer takes no uploads and
 * fetches each file when the post goes out, so the Short's mp4 (or the long's
 * thumbnail) goes to the public Vercel Blob store first. Needs BLOB_READ_WRITE_TOKEN.
 */
import fs from "fs";
import path from "path";
import { del, list, put } from "@vercel/blob";

const TYPES: Record<string, string> = {
  ".mp4": "video/mp4",
  ".mov": "video/quicktime",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
};

export type HostFile = (localPath: string, pathname: string) => Promise<string>;

export const hostOnVercelBlob: HostFile = async (localPath, pathname) => {
  const token = process.env.BLOB_READ_WRITE_TOKEN;
  if (!token) throw new Error("BLOB_READ_WRITE_TOKEN is not set (create a public Vercel Blob store and put its token in .env)");
  const ext = path.extname(localPath).toLowerCase();
  const contentType = TYPES[ext];
  if (!contentType) throw new Error(`Unsupported media type ${ext}`);
  const size = fs.statSync(localPath).size;
  const blob = await put(pathname, fs.createReadStream(localPath), {
    access: "public",
    token,
    contentType,
    // A random suffix keeps an unreleased Short's URL unguessable.
    addRandomSuffix: true,
    multipart: size > 50 * 1024 * 1024,
  });
  return blob.url;
};

/** Only files this mirror put on a Vercel Blob store are ever deleted by it. */
export function isOwnBlobUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return u.protocol === "https:" && /\.public\.blob\.vercel-storage\.com$/i.test(u.hostname) && u.pathname.startsWith("/social/");
  } catch {
    return false;
  }
}

export async function deleteFromVercelBlob(url: string): Promise<void> {
  const token = process.env.BLOB_READ_WRITE_TOKEN;
  if (!token) throw new Error("BLOB_READ_WRITE_TOKEN is not set");
  if (!isOwnBlobUrl(url)) throw new Error(`refusing to delete ${url}: not a mirror file on the Blob store`);
  await del(url, { token });
}

export type StoredMedia = { url: string; pathname: string; uploadedAt: Date };

/** Every mirror file on the Blob store (pathnames under social/). */
export async function listVercelBlobMedia(): Promise<StoredMedia[]> {
  const token = process.env.BLOB_READ_WRITE_TOKEN;
  if (!token) throw new Error("BLOB_READ_WRITE_TOKEN is not set");
  const out: StoredMedia[] = [];
  let cursor: string | undefined;
  do {
    const page = await list({ prefix: "social/", token, cursor, limit: 1000 });
    out.push(...page.blobs.map((b) => ({ url: b.url, pathname: b.pathname, uploadedAt: new Date(b.uploadedAt) })));
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);
  return out;
}

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
