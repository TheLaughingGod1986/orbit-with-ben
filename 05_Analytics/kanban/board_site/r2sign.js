// Cloudflare R2 (S3 API) request signing for the Watch button (Ben, 23 Oct 2026: "Still not opening when click the
// button"). The Vercel Blob store that held the phone copies was suspended on 15 Oct, so cuts now live in the R2 bucket
// the Buffer mirror already uses, under watch/<id>/<random>-<file>.mp4 (Buffer only ever touches social/).
// AWS Signature V4 with node:crypto, so neither the Vercel function nor the Mini needs a package for it.
// Shared by api/watch.js (lists a cut to redirect to it) and scripts/watch_upload.mjs (uploads from the Mini).
import { createHash, createHmac } from "node:crypto";

const hmac = (key, s) => createHmac("sha256", key).update(s, "utf8").digest();
const hex = s => createHash("sha256").update(s).digest("hex");
// RFC 3986 encoding, as SigV4 wants it (encodeURIComponent leaves !'()* alone).
const enc = s => encodeURIComponent(s).replace(/[!'()*]/g, c => "%" + c.charCodeAt(0).toString(16).toUpperCase());

/** R2 settings from the environment, or null when any is missing. */
export function r2Config(env = process.env) {
  const { R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_PUBLIC_URL } = env;
  if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY || !R2_PUBLIC_URL) return null;
  return { accountId: R2_ACCOUNT_ID, accessKeyId: R2_ACCESS_KEY_ID, secretAccessKey: R2_SECRET_ACCESS_KEY,
    publicUrl: R2_PUBLIC_URL.replace(/\/+$/, ""), bucket: env.R2_BUCKET || "owb-media" };
}

/**
 * Headers for a SigV4-signed request. `url` carries the query string; `payloadHash` is the body's SHA-256 hex, or
 * "UNSIGNED-PAYLOAD" for a large upload.
 */
export function signedHeaders({ method, url, accessKeyId, secretAccessKey, region = "auto", service = "s3",
  headers = {}, payloadHash = hex(""), date = new Date() }) {
  const u = new URL(url);
  const amzDate = date.toISOString().replace(/[:-]|\.\d{3}/g, "");
  const day = amzDate.slice(0, 8);
  const all = { ...Object.fromEntries(Object.entries(headers).map(([k, v]) => [k.toLowerCase(), String(v).trim()])),
    host: u.host, "x-amz-content-sha256": payloadHash, "x-amz-date": amzDate };
  const names = Object.keys(all).sort();
  const query = [...u.searchParams.entries()].map(([k, v]) => [enc(k), enc(v)])
    .sort(([a, x], [b, y]) => (a < b ? -1 : a > b ? 1 : x < y ? -1 : x > y ? 1 : 0)).map(([k, v]) => `${k}=${v}`).join("&");
  const path = u.pathname.split("/").map(p => enc(decodeURIComponent(p))).join("/");
  const canonical = [method, path, query, names.map(n => `${n}:${all[n]}\n`).join(""), names.join(";"), payloadHash].join("\n");
  const scope = `${day}/${region}/${service}/aws4_request`;
  const toSign = ["AWS4-HMAC-SHA256", amzDate, scope, hex(canonical)].join("\n");
  const key = ["aws4_request"].reduce((k, s) => hmac(k, s),
    hmac(hmac(hmac(`AWS4${secretAccessKey}`, day), region), service));
  const signature = createHmac("sha256", key).update(toSign, "utf8").digest("hex");
  const out = { ...all, authorization: `AWS4-HMAC-SHA256 Credential=${accessKeyId}/${scope}, SignedHeaders=${names.join(";")}, Signature=${signature}` };
  delete out.host;
  return out;
}

const endpoint = cfg => `https://${cfg.accountId}.r2.cloudflarestorage.com/${cfg.bucket}`;

/** The newest .mp4 under watch/<id>/, as its public URL, or null. */
export async function newestWatchUrl(cfg, id, fetchImpl = fetch) {
  const url = `${endpoint(cfg)}?list-type=2&prefix=${encodeURIComponent(`watch/${id}/`)}&max-keys=50`;
  const res = await fetchImpl(url, { headers: signedHeaders({ method: "GET", url, ...cfg }) });
  if (!res.ok) throw new Error(`R2 list ${res.status}`);
  const xml = await res.text();
  const items = [...xml.matchAll(/<Contents>([\s\S]*?)<\/Contents>/g)].map(m => ({
    key: (m[1].match(/<Key>([^<]+)<\/Key>/) || [])[1] || "",
    at: Date.parse((m[1].match(/<LastModified>([^<]+)<\/LastModified>/) || [])[1] || 0),
  })).filter(x => /\.mp4$/i.test(x.key)).sort((a, b) => b.at - a.at);
  return items.length ? `${cfg.publicUrl}/${items[0].key.split("/").map(encodeURIComponent).join("/")}` : null;
}

/** PUT a file's bytes to watch/<id>/<random>-<name>.mp4; returns the object key. */
export async function putWatchFile(cfg, id, name, body, rand, fetchImpl = fetch) {
  const safe = name.replace(/[^A-Za-z0-9_.-]/g, "_");
  const key = `watch/${id}/${rand}-${safe}`;
  const url = `${endpoint(cfg)}/${key}`;
  const headers = signedHeaders({ method: "PUT", url, ...cfg, payloadHash: "UNSIGNED-PAYLOAD",
    headers: { "content-type": "video/mp4" } });
  const res = await fetchImpl(url, { method: "PUT", headers, body });
  if (!res.ok) throw new Error(`R2 upload ${res.status}: ${(await res.text()).slice(0, 200)}`);
  return key;
}
