// Studio Kanban, self-updating host (Ben, 9 Oct). Stands in for the claude.ai artifact runtime the page was written
// for: window.claude.use("db") serves board/hos, board/owb, board/briefs, board/credits and checks/* from
//   - board.json on the orbit-with-ben `board-data` branch (pushed by the Mac mini's scripts/board_publish.py
//     whenever a job moves or main changes), re-read every 60 s; and
//   - /api/checks (Ben's OK / needs-a-change ticks), re-read on load, after a tick and on return to the tab
//     (board.json also carries them, from the Mini's hourly read).
// use("mcp") returns null, so the page never asks for a GitHub connector.
(function () {
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const API = "/api/checks";
  let key = null;
  try {
    const m = location.hash.match(/(?:^#|&)k=([A-Za-z0-9_-]{8,})/);
    if (m) { localStorage.setItem("studio-board-key", m[1]); history.replaceState(null, "", location.pathname + location.search); }
    key = localStorage.getItem("studio-board-key");
  } catch (e) {}

  let board = null, lastHash = "", server = {}, local = {};   // local: ticks saved from this page, until the server echoes them
  const docSubs = {}, colSubs = [];
  const snap = d => ({ exists: d != null, data: () => d });
  const checks = () => {
    const m = Object.assign({}, server);
    for (const [id, v] of Object.entries(local)) { if (v === null) delete m[id]; else m[id] = v; }
    return m;
  };
  const docData = path => {
    const [c, n] = path.split("/");
    if (c === "board") return board ? board[n] || null : null;
    if (c === "checks") return checks()[n] || null;
    return null;
  };
  const emitDoc = path => (docSubs[path] || []).forEach(cb => { try { cb(snap(docData(path))); } catch (e) {} });
  const emitChecks = () => {
    const m = checks();
    const s = { docs: Object.keys(m).map(id => ({ id, exists: true, data: () => m[id] })) };
    colSubs.forEach(cb => { try { cb(s); } catch (e) {} });
    Object.keys(docSubs).filter(p => p.startsWith("checks/")).forEach(emitDoc);
  };
  const emitAll = () => { Object.keys(docSubs).forEach(emitDoc); emitChecks(); };
  const setServer = m => {
    server = m || {};
    for (const id of Object.keys(local)) {   // the server has caught up with a local tick: drop the local copy
      const s = server[id], l = local[id];
      if ((l === null && !s) || (l && s && s.at === l.at)) delete local[id];
    }
  };

  // raw.githubusercontent caches a branch URL for up to 5 min and ignores query strings, so ask the GitHub API which
  // commit board-data is on (cached 60 s; the browser revalidates with ETag, and 304s don't use the hourly limit) and
  // read that commit's file, which never goes stale. If the API says no (rate limit), fall back to the branch URL.
  const REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  const AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  let lastSha = "";
  async function pollData() {
    try {
      let url = DATA + "?t=" + Date.now(), sha = "";
      try {
        const g = await fetch(REF, { cache: "no-cache" });
        if (g.ok) { sha = ((await g.json()).object || {}).sha || ""; if (sha && sha === lastSha && board) return; if (sha) url = AT(sha); }
      } catch (e) {}
      const r = await fetch(url, { cache: sha ? "force-cache" : "no-store" });
      if (!r.ok) return;
      const text = await r.text();
      if (sha) lastSha = sha;
      if (text === lastHash) return;
      const j = JSON.parse(text);
      lastHash = text;
      board = { hos: j.hos, owb: j.owb, briefs: j.briefs, credits: j.credits };
      window.__boardData = { dataChangedAt: j.dataChangedAt, changedAt: j.changedAt };
      if (j.checks && typeof j.checks === "object" && !checksFresh) setServer(j.checks);
      emitAll();
    } catch (e) {}
  }
  let checksFresh = false;
  async function pollChecks() {
    try {
      const r = await fetch(API + "?t=" + Date.now(), { cache: "no-store" });
      if (!r.ok) return;
      const j = await r.json();
      if (j && typeof j.checks === "object") { checksFresh = true; setServer(j.checks); emitChecks(); }
    } catch (e) {}
  }
  // Ben, 10 Oct: "we used to have a button to add changes or approve". The buttons always show. Saving needs the board
  // code (env BOARD_KEY): opening the board link once (#k=...) stores it on that device; if it isn't stored (e.g. the
  // Home Screen copy keeps its own storage), the first tap asks for it once and keeps it.
  async function write(id, body) {
    if (!key) {
      const k = (window.prompt("One-time setup on this phone: paste the board code from your board link (the part after #k=).") || "").trim().replace(/^.*#k=/, "");
      if (!k) throw new Error("no board code");
      key = k; try { localStorage.setItem("studio-board-key", k); } catch (e) {}
    }
    const r = await fetch(API, { method: "POST", headers: { "content-type": "application/json", "x-board-key": key || "" },
      body: JSON.stringify(Object.assign({ id }, body)) });
    if (r.status === 401) { key = null; try { localStorage.removeItem("studio-board-key"); } catch (e) {} }
    if (!r.ok) throw new Error("save failed " + r.status);
    const j = await r.json();
    if (j && j.checks) { checksFresh = true; setServer(j.checks); emitChecks(); }
  }

  const db = {
    canWrite: true,
    doc(path) {
      return {
        onSnapshot(cb) {
          (docSubs[path] = docSubs[path] || []).push(cb);
          if (board) setTimeout(() => cb(snap(docData(path))), 0);
          return () => { docSubs[path] = (docSubs[path] || []).filter(x => x !== cb); };
        },
        async set(v) {
          const id = path.split("/")[1];
          local[id] = v; emitChecks();
          try { await write(id, { doc: v }); } catch (e) { delete local[id]; emitChecks(); alert("Couldn't save that tick. Try again in a minute."); }
        },
        async delete() {
          const id = path.split("/")[1];
          const before = local[id]; local[id] = null; emitChecks();
          try { await write(id, { delete: true }); } catch (e) { if (before === undefined) delete local[id]; else local[id] = before; emitChecks(); }
        },
      };
    },
    collection() {
      return { onSnapshot(cb) { colSubs.push(cb); if (board) setTimeout(emitChecks, 0); return () => {}; } };
    },
  };
  window.claude = { use: async what => (what === "db" ? db : null) };
  pollData(); pollChecks();
  setInterval(pollData, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) { pollData(); pollChecks(); } });
})();
