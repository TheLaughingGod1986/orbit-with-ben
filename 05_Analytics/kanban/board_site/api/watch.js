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
import { list } from "@vercel/blob";
import { handleUpload } from "@vercel/blob/client";

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
      const k = String((req.query || {}).k || "");
      if (!keyOk(k, process.env.BOARD_KEY, process.env.WATCH_UPLOAD_KEY))
        return res.status(401).send("Open the board from your board link once on this phone, then tap Watch again.");
      const { blobs } = await list({ prefix: `watch/${v}/`, limit: 20 });
      const mp4 = blobs.filter(b => /\.mp4$/i.test(b.pathname)).sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt))[0];
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
