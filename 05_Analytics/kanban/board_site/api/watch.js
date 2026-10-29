// Watch links that play in the phone's browser (Ben, 15 Oct: "Clicking watch does not play the film"). The old links were
// Files-app links (shareddocuments://...) into iCloud Drive: Safari hands them to Files, which can't play a folder, and the
// standalone Shorts' folder was never copied into iCloud Drive at all, so nothing played.
//
// Now a cut for Ben lives in the Cloudflare R2 bucket under watch/<id>/<random>-<file>.mp4 (it was the Vercel Blob store
// until 23 Oct). The random part is only known to the bucket (it's never in board.json, which is public on GitHub), so the
// file can't be found from the board data.
//   GET /api/watch?v=<id>&k=<board code>  -> 302 to the R2 file (public r2.dev URL: video/mp4, Range/206, plays inline).
//     The board code is Ben's (env BOARD_KEY, saved on his phone from the board link); the page adds it when he taps.
//   (The POST client-upload handshake to Blob was removed on 29 Oct 2026.) Nothing is ever deleted here.
//
// 23 Oct 2026: the Blob store was suspended (15 Oct, Hobby limits), so new cuts go to the Cloudflare R2 bucket instead
// (watch/<id>/<random>-<file>.mp4, uploaded straight from the Mini by watch_upload.mjs with its own R2 keys). GET looks in
// R2 first when this project has R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL set, and falls
// back to Blob for older cuts. 29 Oct 2026: the Blob fallback is gone; R2 is the only store. Without the R2_* env vars
// GET answers 500 naming them, rather than looking anywhere else.
// The random part keeps a cut's URL unguessable; board.json only ever holds the id.
// 25 Oct 2026 (Ben: Play should just open the video, no board code): board.json now carries per-cut signed links,
//   GET /api/watch?v=<id>&e=<unix expiry>&s=<HMAC-SHA256(WATCH_LINK_SECRET, "<id>.<e>"), base64url>
// minted by scripts/kanban_snapshot.py on the Mini on every publish (12-15 h ahead). A link stops working at its expiry,
// so a copy from the public board-data branch can't be reused later, and the id alone still opens nothing. The
// board code (k=) keeps working as before for older links.
import { newestWatchUrl, r2Config } from "../r2sign.js";
import { signedOk } from "../watchsign.js";
import { benAuth } from "../benauth.js";

const ID = /^[a-z0-9][a-z0-9_-]{0,63}$/;

export function keyOk(given, ...keys) {
  return !!given && keys.some(k => !!k && given === k);
}


export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  const v = String((req.query || {}).v || "");
  try {
    if (req.method === "GET") {
      if (!ID.test(v)) return res.status(400).send("bad id");
      const q = req.query || {};
      const k = String(q.k || "");
      if (!signedOk(v, q.e, q.s, process.env.WATCH_LINK_SECRET) && !keyOk(k, process.env.BOARD_KEY, process.env.WATCH_UPLOAD_KEY)
          && !benAuth(req))   // Ben's linked phone (studio_ben cookie) plays any cut, even an expired link
        return res.status(401).send(q.s ? "This Play link has expired. Reload the board and tap Play again."
          : "Reload the board and tap Play again.");
      const r2 = r2Config();
      if (!r2) return res.status(500).send("Watch store not configured: set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY and R2_PUBLIC_URL.");
      const url = await newestWatchUrl(r2, v);
      if (!url) return res.status(404).send("That cut isn't uploaded yet.");
      res.setHeader("Location", url);
      return res.status(302).send("");
    }
    return res.status(405).send("GET only");
  } catch (e) {
    return res.status(500).send(String(e && e.message || e).slice(0, 300));
  }
}
