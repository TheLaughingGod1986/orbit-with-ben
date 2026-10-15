// Ben's ticks on the Studio Kanban's "Ready for you to check" card (OK / needs a change), replacing the claude.ai
// artifact's checks/* store. GET returns them all; POST {id, doc} or {id, delete:true} with header x-board-key
// (env BOARD_KEY; Ben's board link carries it as #k=...) writes one. The Mac mini's scripts/board_publish.py copies
// them into board.json, so the Chief sees them on the board-data branch too.
//
// Storage (15 Oct 2026): the body of one GitHub issue, orbit-with-ben #219, written with env BOARD_GH_TOKEN (the same
// token that posts Ben's taps to the Chief's thread). The Vercel Blob store used before was suspended on the Hobby plan
// (limits exceeded), so every tap failed with "blob read 403". The issue body holds one fenced JSON block,
// {checks, history}: a read is one GitHub call, a write one PATCH. Free, no new account, nothing to suspend.
//
// The change stamp: the issue's updated_at is the version. GET ?stamp=1 answers {version} only, and GET returns
// stampUrl pointing there, so the Mini's every-minute check stays one small read (scripts/board_publish.py).

const STORE = ["TheLaughingGod1986/orbit-with-ben", 219];
const HISTORY_KEEP = 150;
// Ben's buttons go straight to the Chief (Ben, 10 Oct): every Approve / Request changes / Undo is also posted on the
// Chief's thread, OWB on orbit-with-ben #99 and HOS on history-of-science #180, with env BOARD_GH_TOKEN (a fine-grained
// GitHub token that can comment on those two repos; never in the page or the repo). Prefix: "[Ben] " then OK / changes /
// undo, so the Chief's thread watch takes it as Ben's word.
const THREADS = { OWB: ["TheLaughingGod1986/orbit-with-ben", 99], HOS: ["TheLaughingGod1986/history-of-science", 180] };

function londonTime(iso) {
  try { return new Date(iso).toLocaleString("en-GB", { timeZone: "Europe/London", weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }); }
  catch (e) { return iso; }
}

export function benLine(id, doc, prev) {
  const [ch, film] = String(id).split("-");
  if (!THREADS[ch] || !/^(\d{3}|S\d{1,2})$/.test(film || "")) return null;   // S1..S8 = the standalone Shorts (Ben, 15 Oct)
  const what = `${film}${(doc || prev || {}).version ? " " + (doc || prev).version : ""}`;
  const tail = `\n\n(Studio Kanban button, ${londonTime((doc && doc.at) || new Date().toISOString())} London)`;
  if (!doc) return prev && !prev.handled ? `[Ben] undo ${what}: ignore my ${prev.verdict === "ok" ? "OK" : "change request"} from the board.${tail}` : null;
  if (doc.handled) return null;
  if (doc.verdict === "ok") return `[Ben] OK ${what}: watched it, looks good.${tail}`;
  const fx = Array.isArray(doc.fixes) ? doc.fixes : [];
  const list = fx.map((f, i) => `${i + 1}. ${f.t ? f.t + " " : ""}${String(f.text || "").slice(0, 1000)}`).join("\n") || String(doc.note || "").slice(0, 4000);
  return `[Ben] changes ${what}:\n${list}${tail}`;
}

function gh(path, init = {}) {
  const token = process.env.BOARD_GH_TOKEN;
  if (!token) throw new Error("BOARD_GH_TOKEN isn't set");
  return fetch(`https://api.github.com/${path}`, { ...init, headers: { authorization: `Bearer ${token}`,
    accept: "application/vnd.github+json", "user-agent": "studio-kanban", "content-type": "application/json" } });
}

async function postToChief(id, body) {
  const [repo, n] = THREADS[String(id).split("-")[0]];
  const r = await gh(`repos/${repo}/issues/${n}/comments`, { method: "POST", body: JSON.stringify({ body }) });
  if (r.ok) return `posted on ${repo.split("/")[1]} #${n}`;
  const why = await r.text().catch(() => "");
  return `not posted: GitHub ${r.status} ${why.slice(0, 160)}`;
}

const ID = /^[A-Za-z0-9_.-]{1,48}$/;

// The store issue's body: a note, then one ```json fenced block.
export function parseStore(body) {
  const m = String(body || "").match(/```json\s*([\s\S]*?)```/);
  const j = m ? JSON.parse(m[1]) : {};
  return { checks: j.checks && typeof j.checks === "object" ? j.checks : {}, history: Array.isArray(j.history) ? j.history : [] };
}

export function renderStore(state) {
  return "Studio Kanban stores Ben's OK / Request changes buttons in this issue's body (15 Oct 2026: replaces the " +
    "suspended Vercel Blob store). Only the board's `/api/checks` writes it. Don't edit by hand.\n\n```json\n" +
    JSON.stringify({ checks: state.checks, history: state.history.slice(-HISTORY_KEEP) }) + "\n```\n";
}

async function load() {
  const r = await gh(`repos/${STORE[0]}/issues/${STORE[1]}`);
  if (!r.ok) throw new Error(`store read ${r.status}`);
  const issue = await r.json();
  return { version: issue.updated_at || "", state: parseStore(issue.body) };
}

async function save(state) {
  const r = await gh(`repos/${STORE[0]}/issues/${STORE[1]}`, { method: "PATCH", body: JSON.stringify({ body: renderStore(state) }) });
  if (!r.ok) throw new Error(`store write ${r.status} ${(await r.text().catch(() => "")).slice(0, 120)}`);
  return (await r.json()).updated_at || "";
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
      const { version, state } = await load();
      if (req.query && req.query.stamp) return res.status(200).json({ version });
      const stampUrl = `https://${req.headers.host}/api/checks?stamp=1`;
      return res.status(200).json({ checks: state.checks, at: new Date().toISOString(), version, stampUrl });
    }
    if (req.method !== "POST") return res.status(405).json({ error: "GET or POST" });
    const key = process.env.BOARD_KEY;
    if (!key || req.headers["x-board-key"] !== key) return res.status(401).json({ error: "this link can't save ticks" });
    const b = await readBody(req);
    if (!ID.test(String(b.id || ""))) return res.status(400).json({ error: "bad id" });
    const { state } = await load();
    const prev = state.checks[b.id] || null;
    if (b.delete) {
      delete state.checks[b.id];
    } else {
      const doc = b.doc && typeof b.doc === "object" ? b.doc : null;
      if (!doc || JSON.stringify(doc).length > 16000) return res.status(400).json({ error: "bad doc" });
      state.checks[b.id] = doc;
    }
    const at = new Date().toISOString();
    state.history = [...state.history, { id: b.id, op: b.delete ? "delete" : "set", at, verdict: b.doc?.verdict || "" }];
    await save(state);
    // Post once per real change (a re-save of the same tick has the same `at`).
    const doc = b.delete ? null : state.checks[b.id];
    const line = doc && prev && prev.at === doc.at && prev.verdict === doc.verdict ? null : benLine(b.id, doc, prev);
    let chief = "";
    if (line) chief = await postToChief(b.id, line).catch(e => `not posted: ${String(e && e.message || e).slice(0, 100)}`);
    if (line) console.log(`checks ${b.id} ${b.delete ? "delete" : (doc || {}).verdict}: ${chief}`);   // shows in vercel logs
    return res.status(200).json({ ok: true, checks: state.checks, chief });
  } catch (e) {
    return res.status(500).json({ error: String(e && e.message || e).slice(0, 300) });
  }
}
