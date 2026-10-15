// Upload a cut so Ben's Watch button plays it in the phone's browser (Studio Kanban /api/watch).
//   WATCH_UPLOAD_KEY=... node scripts/watch_upload.mjs <id> <file.mp4>
// Prints the watch URL to put in film_briefs.json (extraWatch[].url or watch[...].url). Never deletes anything.
// Needs @vercel/blob (npm i --no-save @vercel/blob in 05_Analytics/kanban/board_site, or anywhere on NODE_PATH).
import { upload } from "@vercel/blob/client";
import { readFile } from "node:fs/promises";
import path from "node:path";

const [id, file] = process.argv.slice(2);
const SITE = process.env.BOARD_SITE || "https://studio-kanban.vercel.app";
if (!/^[a-z0-9][a-z0-9_-]{0,63}$/.test(id || "") || !file) { console.error("usage: watch_upload.mjs <id> <file.mp4>"); process.exit(2); }
const key = process.env.WATCH_UPLOAD_KEY; if (!key) { console.error("WATCH_UPLOAD_KEY not set"); process.exit(2); }
const data = await readFile(file);
const b = await upload(`watch/${id}/${path.basename(file)}`, data, { access: "public", contentType: "video/mp4", multipart: data.length > 20e6,
  handleUploadUrl: `${SITE}/api/watch?v=${id}`, headers: { "x-watch-key": key } });
console.error(`uploaded ${b.pathname} (${data.length} bytes)`);
console.log(`${SITE}/api/watch?v=${id}`);
