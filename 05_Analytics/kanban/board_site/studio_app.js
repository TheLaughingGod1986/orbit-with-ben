(function () {
  // Studio app, the board's front page (Ben, 28 Oct 2026 mock-up): Overview, Videos, Review, Agents, Schedule.
  // Reads the same board.json as the video board (/board) and the AI page (/ai). Its only write is Ben's OK / changes
  // tick on the Review tab, sent to /api/checks exactly as /board sends it (same document, same key, no confirmation).
  const DATA_REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  const DATA_AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const TABS = [["overview", "Overview", "⌂"], ["videos", "Videos", "▤"], ["review", "Review", "▶"], ["agents", "Agents", "◉"], ["schedule", "Schedule", "▦"]];
  const QUIET_MIN = 75;  // the relay checks in every 10-20 min; this long without it, the Mac mini is quiet
  const AGENTS = { chief: "Grok", claude: "Claude", codex: "Codex", gemini: "Gemini", cursor: "Cursor", macbook: "MacBook" };
  const POOLS = { elevenlabs: "ElevenLabs", flow: "Flow", vertex: "Vertex", cursor: "Cursor", codex: "Codex · mini", "codex-macbook": "Codex · MacBook" };
  let board = null, lastSha = "", filterCh = "all", filterType = "all";
  const sent = {};  // checkId -> the tick just sent, until board.json shows it
  // Ben's board links carry his tick key (/#k=...); that page lives at /board now, so hand them over untouched.
  if (/(?:^#|&)k=/.test(location.hash)) { location.replace("/board" + location.hash); return; }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }
  const ch = v => v.channel === "HOS" ? "HOS" : "Orbit";
  const kind = v => v.type === "short" ? "Short" : "Long";
  const boardLink = v => `/board#v=${encodeURIComponent(v.key)}`;
  const LIVE = j => j && (j.status === "claimed" || j.status === "open" || j.status === "blocked");

  // A real picture only: the YouTube thumbnail when the video has an id, otherwise a channel tile with its number.
  function thumb(v) {
    const id = v.youtube && v.youtube.videoId;
    const fallback = `<span class="tile ${v.channel === "HOS" ? "hos" : "owb"}">${esc(v.number || "")}</span>`;
    return `<div class="thumb">${id ? `<img loading="lazy" alt="" src="https://i.ytimg.com/vi/${esc(id)}/mqdefault.jpg" onerror="this.remove()" onload="if(this.naturalWidth<=120)this.remove()">` : ""}${fallback}</div>`;
  }

  // Step progress the worker reported (never an estimate): the furthest-along live job on the video.
  function progressOf(v) {
    const p = (v.jobs || []).filter(j => j.status === "claimed").map(j => j.progress).filter(p => p && p.of > 0)
      .sort((a, b) => b.step / b.of - a.step / a.of)[0];
    return p ? { step: p.step, of: p.of } : null;
  }
  const bar = p => p ? `<div class="prog"><div class="bar"><i style="width:${Math.round(p.step / p.of * 100)}%"></i></div><span>${p.step} of ${p.of}</span></div>` : "";

  function stage(v) {
    if (v.lane === "ready") return v.readyFor === "Ben" ? "Ready for you" : `Waiting on ${v.readyFor || "a check"}`;
    if (v.lane === "changes") return "Fixing your changes";
    if (v.lane === "approved") return "Approved, on its way";
    if (v.lane === "done") return v.youtube && v.youtube.state === "scheduled" ? "Scheduled" : "On YouTube";
    const live = (v.jobs || []).find(j => j.status === "claimed");
    if (live) return "Working now";
    if ((v.jobs || []).some(j => j.status === "blocked")) return "On hold";
    return v.lane === "upcoming" ? "Planned" : "In progress";
  }

  const forBen = vs => vs.filter(v => v.lane === "ready" && v.readyFor === "Ben" && !sent[v.checkId]);
  // /board shows Approve / Changes for a long, or a Short with an ask (tracker_app.js showActions); the same here.
  const canTick = v => v.type === "long" || !!v.ask;

  // Ben's tick, as /board sends it (tracker_app.js approve / openChangesModal and postCheck).
  function boardKey() { try { return localStorage.getItem("studio-board-key") || ""; } catch (e) { return ""; } }
  function tickDoc(v, verdict, raw) {
    const fixes = verdict === "ok" ? [] : String(raw || "").split(/\n+/).map(line => {
      const m = line.match(/^\s*(\d{1,2}:\d{2})\s*[:\-]?\s*(.+)$/);
      return m ? { t: m[1], text: m[2].trim() } : { t: "", text: line.trim() };
    }).filter(f => f.text);
    const doc = { film: v.key.split(":S:")[0], version: v.version || "", verdict, fixes, note: verdict === "ok" ? "" : raw, at: new Date().toISOString() };
    if (v.ask) Object.assign(doc, { job: v.ask.job, what: v.ask.what });
    return doc;
  }
  function toast(msg, bad) {
    let t = document.getElementById("toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.className = bad ? "bad on" : "on"; t.textContent = msg;
    clearTimeout(t._h); t._h = setTimeout(() => { t.className = bad ? "bad" : ""; }, bad ? 6000 : 1800);
  }
  async function sendTick(v, verdict, raw) {
    const doc = tickDoc(v, verdict, raw), key = boardKey();
    sent[v.checkId] = Object.assign({ key: v.key }, doc);  // Shorts share their long's checkId: mark only this card
    render();
    try {
      const r = await fetch("/api/checks", { method: "POST", credentials: "same-origin",
        headers: Object.assign({ "content-type": "application/json" }, key ? { "x-board-key": key } : {}),
        body: JSON.stringify({ id: v.checkId, doc }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error((j && j.error) || "save failed " + r.status);
      if (/^not posted/.test(j.chief || "")) toast("Saved, but it didn't reach the Chief's thread. Tell the Chief in chat too.", true);
      else toast(verdict === "ok" ? "OK sent ✓" : "Changes sent ✓");
    } catch (e) {
      delete sent[v.checkId];
      render();
      toast("Not sent: " + String(e.message || e), true);
    }
  }
  function openChanges(v) {
    const bg = document.createElement("div");
    bg.className = "sheet-bg";
    bg.innerHTML = `<div class="sheet" role="dialog" aria-label="Changes"><h3>Changes for ${esc(v.title)}</h3>
      <p class="meta">One note per line. Start with a time when you can, e.g. 0:38 text doesn't match the voice.</p>
      <textarea id="chg" rows="5" placeholder="0:38 text doesn't match the voice&#10;2:40 shot too dark"></textarea>
      <div class="btns"><button type="button" class="btn" data-x>Cancel</button><button type="button" class="btn primary" data-send>Send changes</button></div></div>`;
    document.body.appendChild(bg);
    bg.querySelector("[data-x]").onclick = () => bg.remove();
    bg.onclick = e => { if (e.target === bg) bg.remove(); };
    bg.querySelector("[data-send]").onclick = () => {
      const raw = bg.querySelector("#chg").value.trim();
      if (!raw) return;
      bg.remove();
      sendTick(v, "change", raw);
    };
    bg.querySelector("#chg").focus();
  }
  const inProgress = vs => vs.filter(v => ["progress", "changes", "ready", "approved"].includes(v.lane) && !forBen([v]).length);

  // Publications from now on: YouTube's own schedule first, else the planned air date; one row per YouTube video.
  function schedule(vs, now) {
    const seen = new Set(), rows = [];
    for (const v of vs) {
      const yt = v.youtube || {}, at = Date.parse(yt.publishAt || "") || Date.parse(v.air ? v.air + "T18:00:00Z" : "");
      if (!at || at < now - 36e5 || (yt.state === "live" && yt.privacy === "public")) continue;
      const slot = `${v.channel}|${v.type}|${at}`, id = yt.videoId || "";
      if ((id && seen.has(id)) || seen.has(slot)) {
        const i = rows.findIndex(r => r.slot === slot);  // keep the row that has the YouTube video
        if (i >= 0 && id && !(rows[i].v.youtube || {}).videoId) rows[i] = { v, at, slot, scheduled: yt.state === "scheduled" };
        continue;
      }
      seen.add(slot); if (id) seen.add(id);
      rows.push({ v, at, slot, scheduled: yt.state === "scheduled" });
    }
    return rows.sort((a, b) => a.at - b.at);
  }

  function summary(b, now) {
    const vs = ((b.tracker || {}).videos) || [], m = b.models || {}, jobs = ((b.owb || {}).jobs) || [];
    const quietMin = (now - Date.parse(m.checkedAt || "")) / 6e4;
    const health = !m.checkedAt || isNaN(quietMin) ? ["amber", "No news yet"]
      : quietMin > QUIET_MIN ? ["red", `Mac mini quiet ${Math.round(quietMin / 60)} h`]
      : (m.models || []).some(x => x.status === "red") ? ["amber", "Running, some agents out"] : ["green", "Healthy"];
    const week = schedule(vs, now).filter(r => r.at - now < 7 * 864e5);
    return {
      health, ready: forBen(vs), working: vs.filter(v => v.working || (v.jobs || []).some(j => j.status === "claimed")),
      progress: inProgress(vs), week, chief: m.chief || {},
      jobs: { working: jobs.filter(j => j.status === "claimed").length, queued: jobs.filter(j => j.status === "open").length,
              held: jobs.filter(j => j.status === "blocked").length, doneToday: ((b.owb || {}).day || {}).doneToday || 0 },
    };
  }

  function row(v, extra) {
    return `<a class="row" href="${boardLink(v)}">${thumb(v)}<div class="body"><b>${esc(v.title)}</b>
      <span class="meta">${ch(v)} · ${kind(v)}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}</span>${extra || bar(progressOf(v))}</div><span class="chev">›</span></a>`;
  }
  const section = (title, n, body, more) => `<section><h2>${esc(title)}${n != null ? ` <span class="n">${n}</span>` : ""}${more || ""}</h2>${body}</section>`;
  const empty = text => `<p class="empty">${esc(text)}</p>`;

  function overview(b, now) {
    const s = summary(b, now);
    const tiles = `<div class="tiles">
      <a class="tile-stat" href="#review"><b class="${s.ready.length ? "amber" : ""}">${s.ready.length}</b><span>Ready for you</span></a>
      <a class="tile-stat" href="#videos"><b class="blue">${s.progress.length}</b><span>In progress</span></a>
      <a class="tile-stat" href="#schedule"><b>${s.week.length}</b><span>Going live this week</span></a>
      <a class="tile-stat" href="#agents"><b class="${s.chief.agent ? "green" : "red"}">${esc(s.chief.name || "None")}</b><span>Chief · ${s.chief.agent ? "online" : "nobody up"}</span></a></div>`;
    const working = s.working.slice(0, 3).map(v => row(v)).join("") || empty("Nothing running this minute.");
    const ready = s.ready.map(v => row(v, `<span class="meta">${esc(v.line || "")}</span>`)).join("") || empty("Nothing waiting for you.");
    const pipe = `<div class="tiles three"><div class="tile-stat"><b class="blue">${s.jobs.working}</b><span>Working</span></div>
      <div class="tile-stat"><b>${s.jobs.queued}</b><span>Queued</span></div><div class="tile-stat"><b>${s.jobs.held}</b><span>On hold</span></div></div>
      <p class="meta">${s.jobs.doneToday} jobs finished today.</p>`;
    return `<header class="top"><div><h1>Studio</h1><p class="meta">Orbit With Ben · History of Science</p></div>
      <span class="pill ${s.health[0]}"><i></i>${esc(s.health[1])}</span></header>${tiles}
      ${section("Ready for your review", s.ready.length, ready)}
      ${section("Working now", s.working.length, working, ' <a class="more" href="#videos">See all</a>')}
      ${section("Production pipeline", null, pipe, ' <a class="more" href="#agents">Agents</a>')}`;
  }

  function videos(b) {
    const vs = (((b.tracker || {}).videos) || []).filter(v =>
      (filterCh === "all" || v.channel === filterCh) && (filterType === "all" || v.type === filterType));
    const chips = [["ch", "all", "All"], ["ch", "OWB", "Orbit"], ["ch", "HOS", "HOS"], ["ty", "long", "Longs"], ["ty", "short", "Shorts"]]
      .map(([k, val, label]) => `<button type="button" data-f="${k}" data-v="${val}" class="${(k === "ch" ? filterCh : filterType) === val ? "on" : ""}">${label}</button>`).join("");
    const prog = vs.filter(v => ["progress", "changes", "ready", "approved"].includes(v.lane));
    const up = vs.filter(v => v.lane === "upcoming");
    const done = vs.filter(v => v.lane === "done" && !v.collapsed);
    return `<header class="top"><h1>Videos</h1><a class="more" href="/board">Full board ›</a></header><div class="chips">${chips}</div>
      ${section("In progress", prog.length, prog.map(v => row(v)).join("") || empty("Nothing in progress."))}
      ${section("Planned", up.length, up.slice(0, 15).map(v => row(v)).join("") + (up.length > 15 ? `<a class="more block" href="/board">${up.length - 15} more on the full board</a>` : ""))}
      ${section("On YouTube", done.length, done.slice(0, 10).map(v => row(v)).join(""))}`;
  }

  function review(b) {
    const vs = ((b.tracker || {}).videos) || [];
    const need = forBen(vs).map(v => `<div class="rcard">${row(v, `<span class="tag amber">Needs your review</span>`)}
      ${v.watch && v.watch.url ? `<a class="btn watch" href="${esc(v.watch.url)}" target="_blank" rel="noopener">▶ Watch ${esc(v.watch.version || "")}</a>` : `<span class="btn watch off">No file link yet</span>`}
      <div class="btns">${canTick(v) ? `<button type="button" class="btn ok" data-ok="${esc(v.key)}">✓ OK</button>
        <button type="button" class="btn chg" data-chg="${esc(v.key)}">Changes</button>`
        : `<a class="btn" href="${boardLink(v)}">Open on the board</a>`}</div></div>`).join("");
    const checked = vs.map(v => (sent[v.checkId] || {}).key === v.key ? Object.assign({}, v, { check: sent[v.checkId] }) : v);
    const done = checked.filter(v => v.check && v.check.at).sort((a, b) => Date.parse(b.check.at) - Date.parse(a.check.at)).slice(0, 8)
      .map(v => row(v, `<span class="tag ${v.check.verdict === "ok" ? "green" : "amber"}">${v.check.verdict === "ok" ? "You OK'd" : "You asked for changes"} ${esc(v.check.version || "")}</span>`)).join("");
    return `<header class="top"><h1>Review</h1></header><p class="meta">Finished videos only. Everything else is the agents' job.</p>
      ${section("Needs your review", forBen(vs).length, need || empty("Nothing to watch right now. You'll get a message when there is."))}
      ${section("Reviewed", null, done || empty("No reviews yet."))}`;
  }

  function agents(b, now) {
    const m = b.models || {}, jobs = ((b.owb || {}).jobs) || [], c = m.chief || {}, s = summary(b, now);
    const status = Object.fromEntries((m.models || []).map(x => [x.id, x]));
    const team = Object.entries(AGENTS).map(([id, name]) => {
      const mine = jobs.filter(j => j.by === id && j.status === "claimed");
      const st = id === "chief" ? (c.agent === "chief" ? "green" : "amber") : (status[id] || {}).status || (mine.length ? "green" : "amber");
      const chain = (m.chiefChain || []).find(r => r.agent === id) || {};
      const why = mine.length ? "Working on " + mine.map(j => `${j.id}: ${j.title}`).join(" · ")
        : (status[id] || {}).why || chain.why || (id === "macbook" ? "waits for a MacBook job, plugged in and idle" : "idle");
      return `<div class="row agent"><span class="dot ${esc(st)}"></span><div class="body"><b>${esc(name)}${c.agent === id ? ' <span class="tag green">Chief</span>' : ""}</b>
        <span class="meta">${esc(why.length > 110 ? why.slice(0, 108) + "…" : why)}</span></div></div>`;
    }).join("");
    const pools = (b.credits || {}).pools || {};
    const credit = Object.entries(POOLS).filter(([id]) => pools[id]).map(([id, name]) => {
      const lt = pools[id].latest || {}, unit = pools[id].unit, total = lt.total || (unit === "%" ? 100 : null);
      const share = total && lt.left != null ? lt.left / total : null;
      const stale = (now - Date.parse(lt.at || "")) / 36e5 > 30;
      const tone = share != null && share < 0.1 ? "red" : stale ? "amber" : "green";
      const fig = share != null ? Math.round(share * 100) + "%" : unit === "GBP" ? "£" + Number(lt.left).toFixed(0) : Number(lt.left || 0).toLocaleString("en-GB");
      return `<a class="credit" href="/ai"><span>${esc(name)}</span><b class="${tone}">${fig}</b>${share != null ? `<div class="bar"><i class="${tone}" style="width:${Math.max(3, share * 100).toFixed(0)}%"></i></div>` : `<small>${stale ? "reading stale" : "left"}</small>`}</a>`;
    }).join("");
    return `<header class="top"><h1>Agents</h1><a class="more" href="/ai">Details ›</a></header>
      <div class="chief-card"><span class="dot ${c.agent ? "green" : "red"}"></span><div><b>Chief: ${esc(c.name || "nobody")}</b>
        <span class="meta">${c.agent ? "Online · coordinating production" : "No Chief up: jobs wait"}</span></div></div>
      <div class="tiles three"><div class="tile-stat"><b class="blue">${s.jobs.working}</b><span>Working</span></div>
        <div class="tile-stat"><b>${s.jobs.queued}</b><span>Queued</span></div><div class="tile-stat"><b>${s.jobs.held}</b><span>On hold</span></div></div>
      ${section("Agent team", null, team)}
      ${section("Credits", null, `<div class="credits">${credit}</div>`, ' <a class="more" href="/ai">See all</a>')}`;
  }

  function scheduleTab(b, now) {
    const rows = schedule(((b.tracker || {}).videos) || [], now);
    const fmt = at => new Date(at).toLocaleString("en-GB", { timeZone: "Europe/London", weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
    const item = r => row(r.v, `<span class="meta when">${esc(fmt(r.at))}</span>${r.scheduled ? "" : '<span class="tag">Planned date, not on YouTube yet</span>'}`);
    const week = rows.filter(r => r.at - now < 7 * 864e5), next = rows.filter(r => r.at - now >= 7 * 864e5 && r.at - now < 14 * 864e5);
    const later = rows.filter(r => r.at - now >= 14 * 864e5);
    return `<header class="top"><h1>Schedule</h1></header>
      ${section("Going live this week", week.length, week.map(item).join("") || empty("Nothing scheduled this week."))}
      ${section("Next week", next.length, next.map(item).join("") || empty("Nothing yet."))}
      ${section("Later", later.length, later.slice(0, 12).map(item).join("") || empty("Nothing yet."))}`;
  }

  function renderTab(tab, b, now) {
    if (!b || !b.tracker) return '<p class="empty">Loading the studio…</p>';
    return ({ overview, videos, review, agents, schedule: scheduleTab }[tab] || overview)(b, now);
  }

  function current() {
    const t = (location.hash || "").replace("#", "");
    return TABS.some(([id]) => id === t) ? t : "overview";
  }

  function render() {
    const tab = current(), now = Date.now();
    document.getElementById("view").innerHTML = renderTab(tab, board, now);
    const ready = board ? forBen(((board.tracker || {}).videos) || []).length : 0;
    document.getElementById("nav").innerHTML = TABS.map(([id, label, icon]) =>
      `<a href="#${id}" class="${id === tab ? "on" : ""}"><span class="ic">${icon}</span>${label}${id === "review" && ready ? `<em>${ready}</em>` : ""}</a>`).join("");
    const byKey = k => (((board || {}).tracker || {}).videos || []).find(v => v.key === k);
    document.querySelectorAll("[data-ok]").forEach(btn => btn.onclick = () => { const v = byKey(btn.dataset.ok); if (v) sendTick(v, "ok"); });
    document.querySelectorAll("[data-chg]").forEach(btn => btn.onclick = () => { const v = byKey(btn.dataset.chg); if (v) openChanges(v); });
    document.querySelectorAll(".chips button").forEach(btn => btn.onclick = () => {
      if (btn.dataset.f === "ch") filterCh = btn.dataset.v;
      else filterType = filterType === btn.dataset.v ? "all" : btn.dataset.v;
      render();
    });
  }

  async function poll() {
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
      board = await r.json();
      if (sha) lastSha = sha;
      render();
    } catch (e) {
      document.getElementById("view").innerHTML = '<p class="empty">Could not load the studio data.</p>';
    }
  }

  // STUDIO_APP_TEST_HOOK
  window.addEventListener("hashchange", () => { render(); window.scrollTo(0, 0); });
  render();
  poll();
  setInterval(poll, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) poll(); });
})();
