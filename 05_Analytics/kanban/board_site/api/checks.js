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
// Ben's buttons go straight to the Chief (Ben, 10 Oct): every Approve / Request changes / Undo is also posted on the
// Chief's thread, OWB on orbit-with-ben #99 and HOS on history-of-science #180, with env BOARD_GH_TOKEN (a fine-grained
// GitHub token that can comment on those two repos; never in the page or the repo). Prefix: "[Ben] " then OK / changes /
// undo, so the Chief's thread watch takes it as Ben's word. Without the token the tick still saves; the reply says so.
const THREADS = { OWB: ["TheLaughingGod1986/orbit-with-ben", 99], HOS: ["TheLaughingGod1986/history-of-science", 180] };

function londonTime(iso) {
  try { return new Date(iso).toLocaleString("en-GB", { timeZone: "Europe/London", weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); }
  catch (e) { return iso; }
}

export function benLine(id, doc, prev) {
  const [ch, film] = String(id).split("-");
  if (!THREADS[ch] || !/^\d{3}$/.test(film || "")) return null;
  const what = `${film}${(doc || prev || {}).version ? " " + (doc || prev).version : ""}`;
  const tail = `\n\n(Studio Kanban button, ${londonTime((doc && doc.at) || new Date().toISOString())} London)`;
  if (!doc) return prev && !prev.handled ? `[Ben] undo ${what}: ignore my ${prev.verdict === "ok" ? "OK" : "change request"} from the board.${tail}` : null;
  if (doc.handled) return null;
  if (doc.verdict === "ok") return `[Ben] OK ${what}: watched it, looks good.${tail}`;
  const fx = Array.isArray(doc.fixes) ? doc.fixes : [];
  const list = fx.map((f, i) => `${i + 1}. ${f.t ? f.t + " " : ""}${String(f.text || "").slice(0, 1000)}`).join("\n") || String(doc.note || "").slice(0, 4000);
  return `[Ben] changes ${what}:\n${list}${tail}`;
}

async function postToChief(id, body) {
  const token = process.env.BOARD_GH_TOKEN;
  if (!token) return "not posted: BOARD_GH_TOKEN isn't set";
  const [repo, n] = THREADS[String(id).split("-")[0]];
  const r = await fetch(`https://api.github.com/repos/${repo}/issues/${n}/comments`, { method: "POST",
    headers: { authorization: `Bearer ${token}`, accept: "application/vnd.github+json", "user-agent": "studio-kanban", "content-type": "application/json" },
    body: JSON.stringify({ body }) });
  return r.ok ? `posted on ${repo.split("/")[1]} #${n}` : `not posted: GitHub ${r.status}`;
}
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
    const prev = state.checks[b.id] || null;
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
    // Post once per real change (a re-save of the same tick has the same `at`).
    const doc = b.delete ? null : state.checks[b.id];
    const line = doc && prev && prev.at === doc.at && prev.verdict === doc.verdict ? null : benLine(b.id, doc, prev);
    let chief = "";
    if (line) chief = await postToChief(b.id, line).catch(e => `not posted: ${String(e && e.message || e).slice(0, 100)}`);
    return res.status(200).json({ ok: true, checks: state.checks, chief });
  } catch (e) {
    return res.status(500).json({ error: String(e && e.message || e).slice(0, 300) });
  }
}
