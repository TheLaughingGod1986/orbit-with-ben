// Ben's ticks on the Studio Kanban's "Ready for you to check" card (OK / needs a change), replacing the claude.ai
// artifact's checks/* store. GET returns them all; POST {id, doc} or {id, delete:true} with header x-board-key
// (env BOARD_KEY; Ben's board link carries it as #k=...) writes one. The Mac mini's scripts/board_publish.py copies
// them into board.json, so the Chief sees them on the board-data branch too.
//
// Storage: this project's Vercel Blob store (env BLOB_READ_WRITE_TOKEN). Blob URLs are CDN-cached for at least 60 s and
// ignore query strings, so a file overwritten in place reads stale. Each write therefore saves a new immutable
// snapshot board/checks/state-<time>.json and a read lists the prefix and takes the newest (one list call per read;
// the Hobby plan allows 2,000 a month, so the page reads on load and on return to the tab, and the Mini hourly).
import { put, list, del } from "@vercel/blob";

const PREFIX = "board/checks/state-";
const ID = /^[A-Za-z0-9_.-]{1,48}$/;
const KEEP = 20;

async function snapshots() {
  const { blobs } = await list({ prefix: PREFIX, limit: 1000 });
  return blobs.sort((a, b) => (a.pathname < b.pathname ? 1 : -1));   // newest first (ISO time in the name)
}

async function load() {
  const all = await snapshots();
  if (!all.length) return { all, state: { checks: {}, history: [] } };
  const r = await fetch(all[0].url, { cache: "no-store" });
  if (!r.ok) throw new Error(`blob read ${r.status}`);
  const j = await r.json();
  return { all, state: { checks: j.checks || {}, history: Array.isArray(j.history) ? j.history : [] } };
}

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") return JSON.parse(req.body || "{}");
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString() || "{}");
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Access-Control-Allow-Origin", "*");
  try {
    if (req.method === "GET") {
      const { state } = await load();
      return res.status(200).json({ checks: state.checks, at: new Date().toISOString() });
    }
    if (req.method !== "POST") return res.status(405).json({ error: "GET or POST" });
    const key = process.env.BOARD_KEY;
    if (!key || req.headers["x-board-key"] !== key) return res.status(401).json({ error: "this link can't save ticks" });
    const b = await readBody(req);
    if (!ID.test(String(b.id || ""))) return res.status(400).json({ error: "bad id" });
    const { all, state } = await load();
    if (b.delete) {
      delete state.checks[b.id];
    } else {
      const doc = b.doc && typeof b.doc === "object" ? b.doc : null;
      if (!doc || JSON.stringify(doc).length > 16000) return res.status(400).json({ error: "bad doc" });
      state.checks[b.id] = doc;
    }
    const at = new Date().toISOString();
    state.history = [...state.history, { id: b.id, op: b.delete ? "delete" : "set", at, verdict: b.doc?.verdict || "" }].slice(-300);
    await put(`${PREFIX}${at.replace(/[:.]/g, "-")}.json`, JSON.stringify(state), { access: "public", addRandomSuffix: true,
      contentType: "application/json", cacheControlMaxAge: 31536000 });
    const old = all.slice(KEEP - 1).map(x => x.url);
    if (old.length) await del(old).catch(() => {});
    return res.status(200).json({ ok: true, checks: state.checks });
  } catch (e) {
    return res.status(500).json({ error: String(e && e.message || e).slice(0, 300) });
  }
}
