// One-time "link this phone" for Ben's board buttons (see ../benauth.js). GET shows a tiny page whose script POSTs the
// same query back, so a chat app's link preview (which doesn't run script) can't use the link up. POST checks the
// signature and expiry, records the nonce in the #219 store so the link works once, sets the studio_ben cookie and
// answers {ok}. Nothing is approved here; it only lets this phone's Approve / Request changes buttons post.
import { benAuth, pairOk, makeSession, cookieHeader, renewCookie } from "../benauth.js";
import { loadStore, saveStore } from "./checks.js";

const page = (title, body, script = "") => `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>${title}</title><style>body{font:17px -apple-system,system-ui,sans-serif;background:#0f1218;color:#e8e8ea;
margin:0;display:grid;place-items:center;min-height:100vh;text-align:center;padding:24px}a{color:#7cc4ff}</style></head>
<body><div><h2 id="h">${title}</h2><p id="p">${body}</p></div>${script}</body></html>`;

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Referrer-Policy", "no-referrer");
  const q = req.query || {};
  try {
    if (req.method === "GET") {
      res.setHeader("Content-Type", "text/html; charset=utf-8");
      const script = `<script>
fetch(location.pathname + location.search, { method: "POST", credentials: "same-origin" })
  .then(r => r.json().then(j => ({ r, j })))
  .then(({ r, j }) => {
    if (r.ok && j.ok) { document.getElementById("h").textContent = "This phone is linked";
      document.getElementById("p").textContent = "Approve and Request changes now work with one tap. Opening the board…";
      history.replaceState(null, "", "/api/pair"); setTimeout(() => location.replace("/"), 1200); }
    else { document.getElementById("h").textContent = "Link not used";
      document.getElementById("p").textContent = (j && j.error) || "Something went wrong."; }
  }).catch(() => { document.getElementById("p").textContent = "No connection. Open the link again."; });
</script>`;
      return res.status(200).send(page("Linking this phone…", "One moment.", script));
    }
    if (req.method !== "POST") return res.status(405).json({ error: "GET or POST" });
    if (!process.env.BOARD_KEY || !process.env.WATCH_LINK_SECRET) return res.status(500).json({ error: "board isn't set up for linking" });
    // Already linked (e.g. tapped twice): fine, nothing to use up.
    const how = benAuth(req);
    if (how) { renewCookie(res, req, how); return res.status(200).json({ ok: true, already: true }); }
    const n = String(q.n || ""), e = String(q.e || "");
    if (!pairOk(n, e, q.s, process.env.WATCH_LINK_SECRET))
      return res.status(401).json({ error: "This link has expired or isn't valid. Ask Grok Bot for a new one." });
    const { state } = await loadStore();
    const now = Math.floor(Date.now() / 1000);
    state.pairs = (state.pairs || []).filter(p => p && Number(p.e) > now);
    if (state.pairs.some(p => p.n === n)) return res.status(401).json({ error: "This link was already used. Ask Grok Bot for a new one." });
    state.pairs.push({ n, e: Number(e), at: new Date().toISOString() });
    await saveStore(state);
    res.setHeader("Set-Cookie", cookieHeader(makeSession(process.env.BOARD_KEY)));
    console.log("pair: linked a phone");
    return res.status(200).json({ ok: true });
  } catch (err) {
    return res.status(500).json({ error: String(err && err.message || err).slice(0, 200) });
  }
}
