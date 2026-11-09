// Upload a cut so Ben's Watch button plays it in the phone's browser (Studio Kanban /api/watch).
//   node scripts/watch_upload.mjs <id> <file.mp4>
// R2 only (23 Oct 2026: the Vercel Blob store was suspended on 15 Oct; the Blob fallback was removed on 29 Oct): with
// R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL in the environment or in 07_Content-Ops/.env (the
// Buffer mirror's keys), the file goes to watch/<id>/<random>-<file>.mp4 in the R2 bucket, and /api/watch?v=<id> redirects
// to it. Without all four R2 keys it exits 2 with an error naming them; it never uploads anywhere else. Prints the watch
// URL. Never deletes.
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
if (!r2) {
  console.error("no R2 keys: set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL (env or 07_Content-Ops/.env); "
    + "there is no Vercel Blob fallback");
  process.exit(2);
}
const data = await readFile(file);
const key = await putWatchFile(r2, id, path.basename(file), data, randomBytes(8).toString("hex"));
console.error(`uploaded ${key} (${data.length} bytes) to R2`);
console.log(`${SITE}/api/watch?v=${id}`);
