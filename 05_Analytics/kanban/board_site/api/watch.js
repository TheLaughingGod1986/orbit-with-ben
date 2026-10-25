// Watch links that play in the phone's browser (Ben, 15 Oct: "Clicking watch does not play the film"). The old links were
// Files-app links (shareddocuments://...) into iCloud Drive: Safari hands them to Files, which can't play a folder, and the
// standalone Shorts' folder was never copied into iCloud Drive at all, so nothing played.
//
// Now a cut for Ben lives in this project's Vercel Blob store under watch/<id>/<random>.mp4. The random part is only known
// to the store (it's never in board.json, which is public on GitHub), so the file can't be found from the board data.
//   GET /api/watch?v=<id>&k=<board code>  -> 302 to the Blob file (served by the CDN: video/mp4, Range/206, plays inline).
//     The board code is Ben's (env BOARD_KEY, saved on his phone from the board link); the page adds it when he taps.
//   POST /api/watch?v=<id>  header x-watch-key (env WATCH_UPLOAD_KEY): client-upload token handshake for
//     scripts/watch_upload.mjs, so a file of any size goes straight to Blob. Nothing is ever deleted here.
//
// 23 Oct 2026: the Blob store was suspended (15 Oct, Hobby limits), so new cuts go to the Cloudflare R2 bucket instead
// (watch/<id>/<random>-<file>.mp4, uploaded straight from the Mini by watch_upload.mjs with its own R2 keys). GET looks in
// R2 first when this project has R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL set, and falls
// back to Blob for older cuts. The random part keeps a cut's URL unguessable; board.json only ever holds the id.
// 25 Oct 2026 (Ben: Play should just open the video, no board code): board.json now carries per-cut signed links,
//   GET /api/watch?v=<id>&e=<unix expiry>&s=<HMAC-SHA256(WATCH_LINK_SECRET, "<id>.<e>"), base64url>
// minted by scripts/kanban_snapshot.py on the Mini on every publish (12-15 h ahead). A link stops working at its expiry,
// so a copy from the public board-data branch can't be reused later, and the id alone still opens nothing. The
// board code (k=) keeps working as before for older links.
import { list } from "@vercel/blob";
import { handleUpload } from "@vercel/blob/client";
import { newestWatchUrl, r2Config } from "../r2sign.js";
import { signedOk } from "../watchsign.js";

const ID = /^[a-z0-9][a-z0-9_-]{0,63}$/;

export function keyOk(given, ...keys) {
  return !!given && keys.some(k => !!k && given === k);
}


async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = []; for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  const v = String((req.query || {}).v || "");
  try {
    if (req.method === "GET") {
      if (!ID.test(v)) return res.status(400).send("bad id");
      const q = req.query || {};
      const k = String(q.k || "");
      if (!signedOk(v, q.e, q.s, process.env.WATCH_LINK_SECRET) && !keyOk(k, process.env.BOARD_KEY, process.env.WATCH_UPLOAD_KEY))
        return res.status(401).send(q.s ? "This Play link has expired. Reload the board and tap Play again."
          : "Open the board from your board link once on this phone, then tap Watch again.");
      const r2 = r2Config();
      const fromR2 = r2 ? await newestWatchUrl(r2, v) : null;
      if (fromR2) {
        res.setHeader("Location", fromR2);
        return res.status(302).send("");
      }
      let mp4 = null;
      try {
        const { blobs } = await list({ prefix: `watch/${v}/`, limit: 20 });
        mp4 = blobs.filter(b => /\.mp4$/i.test(b.pathname)).sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt))[0];
      } catch (e) {
        if (!r2) throw e;  // the suspended Blob store: with R2 set up, a cut that isn't there is simply not uploaded yet
      }
      if (!mp4) return res.status(404).send("That cut isn't uploaded yet.");
      res.setHeader("Location", mp4.url);
      return res.status(302).send("");
    }
    if (req.method === "POST") {
      // Blob's completion callback also lands here (signed by Blob itself; handleUpload checks it).
      const body = await readBody(req);
      const isCallback = body && body.type === "blob.upload-completed";
      if (!isCallback && !keyOk(req.headers["x-watch-key"], process.env.WATCH_UPLOAD_KEY)) return res.status(401).json({ error: "no upload key" });
      const out = await handleUpload({ body, request: req,
        onBeforeGenerateToken: async (pathname) => {
          if (!/^watch\/[a-z0-9][a-z0-9_-]{0,63}\/[A-Za-z0-9_.-]+\.mp4$/.test(pathname)) throw new Error("bad pathname");
          return { allowedContentTypes: ["video/mp4"], addRandomSuffix: true, maximumSizeInBytes: 500 * 1024 * 1024 };
        },
        onUploadCompleted: async () => {} });
      return res.status(200).json(out);
    }
    return res.status(405).send("GET or POST");
  } catch (e) {
    return res.status(500).send(String(e && e.message || e).slice(0, 300));
  }
}
