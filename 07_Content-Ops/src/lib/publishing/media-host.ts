/**
 * Public, permanent URLs for the Buffer mirror's media. Buffer takes no uploads and
 * fetches each file when the post goes out, so the Short's mp4 (or the long's
 * thumbnail) goes to the public Vercel Blob store first. Needs BLOB_READ_WRITE_TOKEN.
 */
import fs from "fs";
import path from "path";
import { put } from "@vercel/blob";

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
  if (!token) throw new Error("BLOB_READ_WRITE_TOKEN is not set (connect a public Blob store to orbit-content-ops)");
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
