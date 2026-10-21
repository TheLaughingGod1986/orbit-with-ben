/**
 * Cloudflare R2 host for the Buffer mirror's media (Ben, 21 Oct 2026). Replaces the Vercel
 * Blob store, which went over its Hobby limits and was suspended on 15 Oct. The bucket
 * (owb-media) is public through its r2.dev address; uploads go through R2's S3 API.
 * Needs R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL.
 */
import crypto from "crypto";
import fs from "fs";
import path from "path";
import { AwsClient } from "aws4fetch";
import { MEDIA_TYPES, type HostFile, type StoredMedia } from "@/lib/publishing/media-host";

export type R2Config = { accountId: string; accessKeyId: string; secretAccessKey: string; publicUrl: string; bucket: string };

/** The R2 settings from .env, or null when any is missing (the mirror then plans only). */
export function r2Config(env: NodeJS.ProcessEnv = process.env): R2Config | null {
  const { R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_PUBLIC_URL } = env;
  if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY || !R2_PUBLIC_URL) return null;
  return {
    accountId: R2_ACCOUNT_ID,
    accessKeyId: R2_ACCESS_KEY_ID,
    secretAccessKey: R2_SECRET_ACCESS_KEY,
    publicUrl: R2_PUBLIC_URL.replace(/\/+$/, ""),
    bucket: env.R2_BUCKET || "owb-media",
  };
}

/** Object key for a mirror file: a random tag keeps an unreleased Short's URL unguessable. */
export function r2Key(pathname: string, rand: () => string = () => crypto.randomBytes(8).toString("hex")): string {
  const ext = path.extname(pathname);
  const base = pathname.slice(0, pathname.length - ext.length).replace(/^\/+/, "");
  return `${base}-${rand()}${ext}`;
}

/** Only files this mirror put in the bucket (under social/) are ever deleted by it. */
export function isOwnR2Url(url: string, publicUrl: string | undefined): boolean {
  if (!publicUrl) return false;
  try {
    const u = new URL(url);
    const base = new URL(publicUrl);
    return u.protocol === "https:" && u.hostname === base.hostname && u.pathname.startsWith("/social/");
  } catch {
    return false;
  }
}

export function createR2Host(cfg: R2Config, fetchImpl: typeof fetch = fetch) {
  const aws = new AwsClient({ accessKeyId: cfg.accessKeyId, secretAccessKey: cfg.secretAccessKey, service: "s3", region: "auto" });
  const endpoint = `https://${cfg.accountId}.r2.cloudflarestorage.com/${cfg.bucket}`;
  const call = async (url: string, init: RequestInit) => {
    const signed = await aws.sign(url, init);
    return fetchImpl(signed);
  };

  const host: HostFile = async (localPath, pathname) => {
    const ext = path.extname(localPath).toLowerCase();
    const contentType = MEDIA_TYPES[ext];
    if (!contentType) throw new Error(`Unsupported media type ${ext}`);
    const key = r2Key(pathname);
    const body = fs.readFileSync(localPath);
    const res = await call(`${endpoint}/${key}`, { method: "PUT", body, headers: { "content-type": contentType } });
    if (!res.ok) throw new Error(`R2 upload of ${key} failed: ${res.status} ${(await res.text()).slice(0, 200)}`);
    return `${cfg.publicUrl}/${key}`;
  };

  const deleteMedia = async (url: string) => {
    if (!isOwnR2Url(url, cfg.publicUrl)) throw new Error(`refusing to delete ${url}: not a mirror file in the R2 bucket`);
    const key = new URL(url).pathname.replace(/^\//, "");
    const res = await call(`${endpoint}/${key}`, { method: "DELETE" });
    if (!res.ok && res.status !== 404) throw new Error(`R2 delete of ${key} failed: ${res.status}`);
  };

  const listMedia = async (): Promise<StoredMedia[]> => {
    const out: StoredMedia[] = [];
    let token: string | undefined;
    do {
      const q = new URLSearchParams({ "list-type": "2", prefix: "social/", "max-keys": "1000" });
      if (token) q.set("continuation-token", token);
      const res = await call(`${endpoint}?${q}`, { method: "GET" });
      if (!res.ok) throw new Error(`R2 list failed: ${res.status}`);
      const xml = await res.text();
      out.push(...parseListObjects(xml, cfg.publicUrl));
      token = /<IsTruncated>true<\/IsTruncated>/.test(xml) ? xml.match(/<NextContinuationToken>([^<]+)<\/NextContinuationToken>/)?.[1] : undefined;
    } while (token);
    return out;
  };

  return { host, deleteMedia, listMedia };
}

/** Keys and upload times from an S3 ListObjectsV2 reply. */
export function parseListObjects(xml: string, publicUrl: string): StoredMedia[] {
  const out: StoredMedia[] = [];
  for (const m of xml.matchAll(/<Contents>([\s\S]*?)<\/Contents>/g)) {
    const key = m[1].match(/<Key>([^<]+)<\/Key>/)?.[1];
    const modified = m[1].match(/<LastModified>([^<]+)<\/LastModified>/)?.[1];
    if (!key) continue;
    out.push({ url: `${publicUrl.replace(/\/+$/, "")}/${key}`, pathname: key, uploadedAt: new Date(modified || 0) });
  }
  return out;
}
