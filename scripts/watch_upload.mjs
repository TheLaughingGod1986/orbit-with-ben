// Upload a cut so Ben's Watch button plays it in the phone's browser (Studio Kanban /api/watch).
//   node scripts/watch_upload.mjs <id> <file.mp4>
// R2 first (23 Oct 2026: the Vercel Blob store was suspended on 15 Oct): with R2_ACCOUNT_ID, R2_ACCESS_KEY_ID,
// R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL in the environment or in 07_Content-Ops/.env (the Buffer mirror's keys), the file
// goes to watch/<id>/<random>-<file>.mp4 in the R2 bucket, and /api/watch?v=<id> redirects to it. Without R2 it falls back
// to the old Blob upload (needs WATCH_UPLOAD_KEY and @vercel/blob on NODE_PATH). Prints the watch URL. Never deletes.
import { randomBytes } from "node:crypto";
import { readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { putWatchFile, r2Config } from "../05_Analytics/kanban/board_site/r2sign.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [id, file] = process.argv.slice(2);
const SITE = process.env.BOARD_SITE || "https://studio-kanban.vercel.app";
if (!/^[a-z0-9][a-z0-9_-]{0,63}$/.test(id || "") || !file) { console.error("usage: watch_upload.mjs <id> <file.mp4>"); process.exit(2); }

/** R2_* values from 07_Content-Ops/.env, without overriding the environment. Values are never printed. */
function envFileR2(text) {
  const out = {};
  for (const line of text.split(/\r?\n/)) {
    const m = /^\s*(?:export\s+)?(R2_[A-Z_]+)\s*=\s*(.*?)\s*$/.exec(line);
    if (m) out[m[1]] = m[2].replace(/^(['"])(.*)\1$/, "$2");
  }
  return out;
}

// Same places as kanban_snapshot.env_files(): this checkout, $ORBIT_REPO, then ~/YouTube/orbit-with-ben (board_publish.py
// runs from a sparse worktree that has no .env of its own, J0888).
let fromFile = {};
for (const root of [ROOT, process.env.ORBIT_REPO, path.join(os.homedir(), "YouTube", "orbit-with-ben")].filter(Boolean)) {
  try { fromFile = envFileR2(readFileSync(path.join(root, "07_Content-Ops", ".env"), "utf8")); break; } catch { /* next */ }
}
const r2 = r2Config({ ...fromFile, ...process.env });
const data = await readFile(file);

if (r2) {
  const key = await putWatchFile(r2, id, path.basename(file), data, randomBytes(8).toString("hex"));
  console.error(`uploaded ${key} (${data.length} bytes) to R2`);
} else {
  const key = process.env.WATCH_UPLOAD_KEY; if (!key) { console.error("no R2 keys and WATCH_UPLOAD_KEY not set"); process.exit(2); }
  const { upload } = await import("@vercel/blob/client");
  const b = await upload(`watch/${id}/${path.basename(file)}`, data, { access: "public", contentType: "video/mp4", multipart: data.length > 20e6,
    handleUploadUrl: `${SITE}/api/watch?v=${id}`, headers: { "x-watch-key": key } });
  console.error(`uploaded ${b.pathname} (${data.length} bytes) to Blob`);
}
console.log(`${SITE}/api/watch?v=${id}`);
