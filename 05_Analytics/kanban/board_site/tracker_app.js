// Per-video Studio tracker UI (Ben, 24 Oct 2026). Reads board.json `tracker` (+ live /api/checks),
// re-applies lane rules when Ben taps Approve / Request changes, posts via the same /api/checks path
// as the classic board (OWB → issue #264, HOS → #180).
(function () {
  const DATA_REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  const DATA_AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const API = "/api/checks";
  const LANES = [
    ["upcoming", "Upcoming"],
    ["progress", "In progress"],
    ["changes", "Changes requested"],
    ["ready", "Ready for OK"],
    ["done", "Done on YouTube"],
  ];

  let key = null;
  try {
    const m = location.hash.match(/(?:^#|&)k=([A-Za-z0-9_-]{8,})/);
    if (m) { localStorage.setItem("studio-board-key", m[1]); history.replaceState(null, "", location.pathname + location.search); }
    key = localStorage.getItem("studio-board-key");
  } catch (e) {}

  let board = null, checks = {}, local = {}, showOldDone = false;
  let filterCh = "all", filterType = "all";
  let lastSha = "";

  const checksMerged = () => {
    const m = Object.assign({}, checks);
    for (const [id, v] of Object.entries(local)) { if (v === null) delete m[id]; else m[id] = v; }
    return m;
  };

  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  // Mirror of scripts/video_tracker.py derive_lane (keep in sync for instant taps).
  function deriveLane(v, check) {
    if (v.youtube && v.youtube.videoId) return "done";
    const jobs = v.jobs || [];
    const unhandled = check && !check.handled;
    const changeCheck = unhandled && check.verdict === "change";
    const okCheck = unhandled && check.verdict === "ok";
    const isChangesJob = j => /Ben'?s?\s+\d+\s+changes|changes?\s+on\s+master|change tick/i.test((j.title || "") + " " + (j.body || ""));
    const changeJobs = jobs.filter(isChangesJob);
    const otherJobs = jobs.filter(j => !isChangesJob(j));
    if (changeCheck || changeJobs.length) {
      if (changeCheck && !changeJobs.length && (v._you || "") && !otherJobs.length) return "ready";
      return "changes";
    }
    if (okCheck) return (otherJobs.length || changeJobs.length) ? "progress" : "ready";
    if ((v._you || "") && !okCheck) {
      if (otherJobs.some(j => j.status === "claimed")) return "progress";
      return "ready";
    }
    if (jobs.some(j => j.status === "blocked" && /parked for Chief/i.test(j.title || ""))) return "ready";
    if (jobs.length) return "progress";
    return "upcoming";
  }

  function applyChecks(videos) {
    const m = checksMerged();
    return videos.map(v => {
      const c = m[v.checkId] || null;
      const lane = deriveLane(v, c);
      const notes = (c && c.verdict === "change" && Array.isArray(c.fixes) && c.fixes.length)
        ? c.fixes.map(f => ({ t: f.t || "", text: f.text || "", done: false }))
        : (v.notes || []);
      const flags = [...(v.flags || [])];
      if (c && !c.handled && (c.verdict === "ok" || c.verdict === "change") && !(v.jobs || []).length) {
        if (!flags.some(f => f.kind === "stuck")) flags.push({ kind: "stuck", text: "No job queued" });
      }
      let readyFor = v.readyFor || "";
      if (lane === "ready") {
        readyFor = (c && c.verdict === "ok" && !c.handled) ? "Chief" : "Ben";
      }
      let line = v.line;
      if (lane === "ready" && readyFor === "Ben") line = "Waiting on your OK.";
      if (lane === "ready" && readyFor === "Chief") line = "You OK'd it — waiting on Chief PASS.";
      if (lane === "changes" && notes.length) line = `${notes.length} change${notes.length === 1 ? "" : "s"} to make.`;
      return Object.assign({}, v, { lane, notes, flags, readyFor, line, check: c ? { verdict: c.verdict, version: c.version, at: c.at, handled: !!c.handled } : v.check });
    });
  }

  function passFilter(v) {
    if (filterCh !== "all" && v.channel !== filterCh) return false;
    if (filterType === "long" && v.type !== "long") return false;
    if (filterType === "short" && v.type !== "short") return false;
    return true;
  }

  async function ensureKey() {
    if (key) return key;
    const k = (window.prompt("One-time setup on this phone: paste the board code from your board link (the part after #k=).") || "").trim().replace(/^.*#k=/, "");
    if (!k) throw new Error("no board code");
    key = k;
    try { localStorage.setItem("studio-board-key", k); } catch (e) {}
    return key;
  }

  async function postCheck(id, doc) {
    await ensureKey();
    const r = await fetch(API, {
      method: "POST",
      headers: { "content-type": "application/json", "x-board-key": key },
      body: JSON.stringify({ id, doc }),
    });
    if (r.status === 401) { key = null; try { localStorage.removeItem("studio-board-key"); } catch (e) {} throw new Error("bad board code"); }
    if (!r.ok) throw new Error("save failed " + r.status);
    const j = await r.json();
    if (j && j.checks) checks = j.checks;
    if (j && /^not posted/.test(j.chief || "")) alert("Saved, but it didn't reach the Chief's thread. Tell the Chief in chat too.");
    delete local[id];
    render();
  }

  function openChangesModal(v) {
    const bg = document.createElement("div");
    bg.className = "modal-bg";
    bg.innerHTML = `<div class="modal" role="dialog" aria-label="Request changes">
      <h3>Changes for ${esc(v.number)} ${esc(v.title)}</h3>
      <p class="meta">One note per line. Start with a timecode when you can (e.g. 0:38 figures fall through shelf).</p>
      <textarea id="chg-text" placeholder="0:38 figures falling through shelf&#10;2:40 needle not scratch&#10;4:22 arm artefact"></textarea>
      <div class="row">
        <button type="button" class="chg" id="chg-save">Send changes</button>
        <button type="button" class="watch" id="chg-cancel">Cancel</button>
      </div>
    </div>`;
    document.body.appendChild(bg);
    bg.querySelector("#chg-cancel").onclick = () => bg.remove();
    bg.onclick = e => { if (e.target === bg) bg.remove(); };
    bg.querySelector("#chg-save").onclick = async () => {
      const raw = bg.querySelector("#chg-text").value.trim();
      if (!raw) return;
      const fixes = raw.split(/\n+/).map(line => {
        const m = line.match(/^\s*(\d{1,2}:\d{2})\s*[:\-]?\s*(.+)$/);
        return m ? { t: m[1], text: m[2].trim() } : { t: "", text: line.trim() };
      }).filter(f => f.text);
      const doc = {
        film: v.key.split(":S:")[0],
        version: v.version || "",
        verdict: "change",
        fixes,
        note: raw,
        at: new Date().toISOString(),
      };
      local[v.checkId] = doc;
      bg.remove();
      render();
      try { await postCheck(v.checkId, doc); }
      catch (e) { delete local[v.checkId]; render(); alert(String(e.message || e)); }
    };
  }

  async function approve(v) {
    const doc = {
      film: v.key.split(":S:")[0],
      version: v.version || "",
      verdict: "ok",
      fixes: [],
      note: "",
      at: new Date().toISOString(),
    };
    local[v.checkId] = doc;
    render();
    try { await postCheck(v.checkId, doc); }
    catch (e) { delete local[v.checkId]; render(); alert(String(e.message || e)); }
  }

  function cardHtml(v) {
    const flagged = (v.flags || []).length;
    const chClass = v.channel === "HOS" ? "hos" : "orbit";
    const chLabel = v.channel === "HOS" ? "HOS" : "Orbit";
    const notes = (v.notes || []).map(n =>
      `<li class="${n.done ? "done" : ""}"><span class="box" aria-hidden="true"></span><span>${n.t ? `<span class="t">${esc(n.t)}</span>` : ""}${esc(n.text)}</span></li>`
    ).join("");
    const flagHtml = (v.flags || []).map(f => `<div class="flag">${esc(f.text)}</div>`).join("");
    const showActions = v.lane === "ready" && v.readyFor === "Ben" && v.type === "long";
    const watch = v.watch && v.watch.url
      ? `<a class="btn watch" href="${esc(v.watch.url)}" target="_blank" rel="noopener">▶ Watch ${esc(v.watch.version || v.version || "")}</a>`
      : "";
    const yt = v.youtube && v.youtube.url
      ? `<a class="btn yt" href="${esc(v.youtube.url)}" target="_blank" rel="noopener">YouTube</a>`
      : "";
    return `<article class="card${flagged ? " flagged" : ""}" data-key="${esc(v.key)}">
      <div class="top">
        <span class="badge ${chClass}">${chLabel}</span>
        <span class="badge type">${esc(v.type === "short" ? "Short" : "Long")}</span>
        ${v.version ? `<span class="badge ver">${esc(v.version)}</span>` : ""}
        ${v.lane === "ready" && v.readyFor ? `<span class="ready-tag">Waits on ${esc(v.readyFor)}</span>` : ""}
      </div>
      <h3 class="title"><span class="num">${esc(v.number)}</span>${esc(v.title)}</h3>
      ${v.airText ? `<p class="meta">${v.lane === "done" ? esc(v.airText) : "Airs " + esc(v.airText)}</p>` : ""}
      <p class="line">${esc(v.line)}</p>
      <p class="meta">Waiting on: ${esc(v.waitingOn || "—")}</p>
      ${flagHtml ? `<div class="flags">${flagHtml}</div>` : ""}
      ${notes ? `<ul class="notes">${notes}</ul>` : ""}
      <div class="actions">
        ${showActions ? `<button type="button" class="ok" data-ok="${esc(v.key)}">Approve</button>
          <button type="button" class="chg" data-chg="${esc(v.key)}">Request changes</button>` : ""}
        ${watch}${yt}
      </div>
    </article>`;
  }

  function render() {
    const root = board && board.tracker;
    if (!root || !Array.isArray(root.videos)) {
      document.getElementById("board").innerHTML = `<p class="empty">No tracker data yet. The Mini publishes it on the next board-data push.</p>`;
      return;
    }
    const videos = applyChecks(root.videos).filter(passFilter);
    const asof = document.getElementById("asof");
    const when = (window.__boardData && window.__boardData.dataChangedAt) || root.updatedAt || "";
    asof.textContent = when ? `Updated ${new Date(when).toLocaleString("en-GB", { timeZone: "Europe/London" })} London` : "Live";

    const fil = document.getElementById("filters");
    const chips = [
      ["ch", "all", "All"], ["ch", "OWB", "Orbit"], ["ch", "HOS", "HOS"],
      ["ty", "all", "Long + Shorts"], ["ty", "long", "Longs"], ["ty", "short", "Shorts"],
    ];
    fil.innerHTML = chips.map(([kind, val, label]) => {
      const on = kind === "ch" ? filterCh === val : filterType === val;
      return `<button type="button" class="${on ? "on" : ""}" data-f="${kind}" data-v="${val}">${label}</button>`;
    }).join("");
    fil.querySelectorAll("button").forEach(b => b.onclick = () => {
      if (b.dataset.f === "ch") filterCh = b.dataset.v;
      else filterType = b.dataset.v;
      render();
    });

    const boardEl = document.getElementById("board");
    boardEl.innerHTML = LANES.map(([id, label]) => {
      const all = videos.filter(v => v.lane === id);
      const shown = id === "done" && !showOldDone ? all.filter(v => !v.collapsed) : all;
      const hidden = id === "done" ? all.filter(v => v.collapsed).length : 0;
      const body = shown.length ? shown.map(cardHtml).join("") : `<p class="empty">Nothing here</p>`;
      const more = hidden
        ? `<button type="button" class="collapsed-toggle" data-old="1">Show ${hidden} older public</button>`
        : (id === "done" && showOldDone
          ? `<button type="button" class="collapsed-toggle" data-old="0">Hide older public</button>` : "");
      return `<section class="lane" data-lane="${id}"><h2>${label}<span class="n">${shown.length}</span></h2><div class="cards">${body}${more}</div></section>`;
    }).join("");

    boardEl.querySelectorAll("[data-ok]").forEach(b => b.onclick = () => {
      const v = videos.find(x => x.key === b.dataset.ok);
      if (v) approve(v);
    });
    boardEl.querySelectorAll("[data-chg]").forEach(b => b.onclick = () => {
      const v = videos.find(x => x.key === b.dataset.chg);
      if (v) openChangesModal(v);
    });
    boardEl.querySelectorAll("[data-old]").forEach(b => b.onclick = () => {
      showOldDone = b.dataset.old === "1";
      render();
    });

    document.querySelectorAll("a[href*='/api/watch?']").forEach(a => {
      a.addEventListener("click", ev => {
        if (!key) {
          const k = (window.prompt("Paste the board code from your board link (#k=…).") || "").trim().replace(/^.*#k=/, "");
          if (!k) { ev.preventDefault(); return; }
          key = k; try { localStorage.setItem("studio-board-key", k); } catch (e) {}
        }
        const u = new URL(a.href, location.href); u.searchParams.set("k", key); a.href = u.toString();
      }, true);
    });
  }

  async function pollChecks() {
    try {
      const r = await fetch(API + "?t=" + Date.now(), { cache: "no-store" });
      if (!r.ok) return;
      const j = await r.json();
      if (j && typeof j.checks === "object") { checks = j.checks; render(); }
    } catch (e) {}
  }

  async function pollData() {
    try {
      let url = DATA + "?t=" + Date.now(), sha = "";
      try {
        const g = await fetch(DATA_REF, { cache: "no-cache" });
        if (g.ok) {
          sha = ((await g.json()).object || {}).sha || "";
          if (sha && sha === lastSha && board) return;
          if (sha) url = DATA_AT(sha);
        }
      } catch (e) {}
      const r = await fetch(url, { cache: sha ? "force-cache" : "no-store" });
      if (!r.ok) return;
      const j = await r.json();
      if (sha) lastSha = sha;
      window.__boardData = { dataChangedAt: j.dataChangedAt, publishedAt: j.publishedAt };
      if (j.checks && typeof j.checks === "object" && !Object.keys(checks).length) checks = j.checks;
      // Prefer live tracker; keep the baked offline copy until board-data carries the new section.
      const briefs = ((j.briefs || {}).films) || {};
      if (j.tracker && Array.isArray(j.tracker.videos)) {
        j.tracker.videos.forEach(v => { v._you = (briefs[v.key] || {}).you || ""; });
        board = j;
      } else if (!board || !board.tracker) {
        board = j;
      } else {
        board = Object.assign({}, j, { tracker: board.tracker });
      }
      render();
    } catch (e) {
      document.getElementById("asof").textContent = "Could not load board data";
    }
  }

  // Boot with any baked tracker (offline), then refresh.
  try {
    const baked = document.getElementById("baked-tracker");
    if (baked) {
      board = { tracker: JSON.parse(baked.textContent) };
      render();
    }
  } catch (e) {}

  pollData();
  pollChecks();
  setInterval(() => { pollData(); pollChecks(); }, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) { pollData(); pollChecks(); } });
})();
