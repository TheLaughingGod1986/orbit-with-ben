// Ben's ticks on the Studio Kanban's "Ready for you to check" card (OK / needs a change), replacing the claude.ai
// artifact's checks/* store. GET returns them all; POST {id, doc} or {id, delete:true} with header x-board-key
// (env BOARD_KEY; Ben's board link carries it as #k=...) writes one. Stored as one JSON file in this project's
// Vercel Blob store (env BLOB_READ_WRITE_TOKEN, injected when the store is connected). The Mac mini's
// scripts/board_publish.py copies them into board.json so the Chief sees them on the board-data branch too.
import { put } from "@vercel/blob";

const PATH = "board/checks.json";
const ID = /^[A-Za-z0-9_.-]{1,48}$/;

function blobUrl() {
  const t = process.env.BLOB_READ_WRITE_TOKEN || "";
  const store = t.split("_")[3];
  return store ? `https://${store.toLowerCase()}.public.blob.vercel-storage.com/${PATH}` : null;
}

async function load() {
  const url = blobUrl();
  if (!url) return { checks: {}, history: [] };
  const r = await fetch(`${url}?v=${Date.now()}`, { cache: "no-store" });
  if (r.status === 404 || r.status === 403) return { checks: {}, history: [] };
  if (!r.ok) throw new Error(`blob read ${r.status}`);
  const j = await r.json();
  return { checks: j.checks || {}, history: Array.isArray(j.history) ? j.history : [] };
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
      const { checks } = await load();
      return res.status(200).json({ checks, at: new Date().toISOString() });
    }
    if (req.method !== "POST") return res.status(405).json({ error: "GET or POST" });
    const key = process.env.BOARD_KEY;
    if (!key || req.headers["x-board-key"] !== key) return res.status(401).json({ error: "this link can't save ticks" });
    const b = await readBody(req);
    if (!ID.test(String(b.id || ""))) return res.status(400).json({ error: "bad id" });
    const store = await load();
    if (b.delete) {
      delete store.checks[b.id];
    } else {
      const doc = b.doc && typeof b.doc === "object" ? b.doc : null;
      if (!doc || JSON.stringify(doc).length > 16000) return res.status(400).json({ error: "bad doc" });
      store.checks[b.id] = doc;
    }
    store.history = [...store.history, { id: b.id, op: b.delete ? "delete" : "set", at: new Date().toISOString(),
      verdict: b.doc?.verdict || "" }].slice(-300);
    await put(PATH, JSON.stringify(store), { access: "public", addRandomSuffix: false, allowOverwrite: true,
      contentType: "application/json", cacheControlMaxAge: 60 });
    return res.status(200).json({ ok: true, checks: store.checks });
  } catch (e) {
    return res.status(500).json({ error: String(e && e.message || e).slice(0, 300) });
  }
}
