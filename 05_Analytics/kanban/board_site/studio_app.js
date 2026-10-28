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
  let board = null, lastSha = "", filterCh = "all", filterType = "all", seg = "all";
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
  const clip = (s, n) => { s = String(s || ""); return s.length > n ? s.slice(0, n - 1) + "…" : s; };
  const activeJob = v => (v.jobs || []).find(j => j.status === "claimed");
  const isWorking = v => !!activeJob(v) || !!v.working;

  // What the agents are doing on a video, in one line: who, the task, and the step they reported.
  function doing(v) {
    const j = activeJob(v);
    if (!j) return `<span class="doing">${esc(clip(v.line || "Being worked on", 90))}</span>`;
    const p = j.progress && j.progress.of > 0 ? ` · Step ${j.progress.step} of ${j.progress.of}` : "";
    return `<span class="doing">${esc(AGENTS[j.by] || j.by || "An agent")} · ${esc(clip(j.remaining_action || j.title, 70))}${p}</span>${bar(progressOf(v))}`;
  }
  const uatLink = v => `#uat=${encodeURIComponent(v.key)}`;

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
      health, ready: forBen(vs), working: vs.filter(isWorking),
      progress: inProgress(vs), week, chief: m.chief || {},
      jobs: { working: jobs.filter(j => j.status === "claimed").length, queued: jobs.filter(j => j.status === "open").length,
              held: jobs.filter(j => j.status === "blocked").length, doneToday: ((b.owb || {}).day || {}).doneToday || 0 },
    };
  }

  function row(v, extra, href) {
    return `<a class="row" href="${href || boardLink(v)}">${thumb(v)}<div class="body"><b>${esc(v.title)}</b>
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
    const working = s.working.slice(0, 3).map(v => row(v, doing(v))).join("") || empty("Nothing running this minute.");
    const ready = s.ready.map(v => row(v, `<span class="meta">${esc(v.line || "")}</span>`, uatLink(v))).join("") || empty("Nothing waiting for you.");
    const pipe = `<div class="tiles three"><div class="tile-stat"><b class="blue">${s.jobs.working}</b><span>Working</span></div>
      <div class="tile-stat"><b>${s.jobs.queued}</b><span>Queued</span></div><div class="tile-stat"><b>${s.jobs.held}</b><span>On hold</span></div></div>
      <p class="meta">${s.jobs.doneToday} jobs finished today.</p>`;
    return `<header class="top"><div><h1>Studio</h1><p class="meta">Orbit With Ben · History of Science</p></div>
      <span class="pill ${s.health[0]}"><i></i>${esc(s.health[1])}</span></header>${tiles}
      ${section("Ready for your review", s.ready.length, ready)}
      ${section("Working now", s.working.length, working, ' <a class="more" href="#videos">See all</a>')}
      ${section("Production pipeline", null, pipe, ' <a class="more" href="#agents">Agents</a>')}`;
  }

  // Working / Queued / Backlog (Ben, 28 Oct): active work is one tap away; All keeps everything with On YouTube.
  function videoGroups(vs) {
    const active = ["progress", "changes", "ready", "approved"];
    return {
      working: vs.filter(v => active.includes(v.lane) && isWorking(v)),
      queued: vs.filter(v => active.includes(v.lane) && !isWorking(v)),
      backlog: vs.filter(v => v.lane === "upcoming"),
      done: vs.filter(v => v.lane === "done" && !v.collapsed),
    };
  }

  function videos(b) {
    const vs = (((b.tracker || {}).videos) || []).filter(v =>
      (filterCh === "all" || v.channel === filterCh) && (filterType === "all" || v.type === filterType));
    const g = videoGroups(vs);
    const segs = [["all", "All"], ["working", "Working"], ["queued", "Queued"], ["backlog", "Backlog"]]
      .map(([id, label]) => `<button type="button" data-seg="${id}" class="${seg === id ? "on" : ""}">${label}${id === "all" ? "" : ` <small>${g[id].length}</small>`}</button>`).join("");
    const chips = [["ch", "all", "Both"], ["ch", "OWB", "Orbit"], ["ch", "HOS", "HOS"], ["ty", "long", "Longs"], ["ty", "short", "Shorts"]]
      .map(([k, val, label]) => `<button type="button" data-f="${k}" data-v="${val}" class="${(k === "ch" ? filterCh : filterType) === val ? "on" : ""}">${label}</button>`).join("");
    const list = (items, limit) => items.slice(0, limit).map(v => row(v, isWorking(v) ? doing(v) : "")).join("")
      + (items.length > limit ? `<a class="more block" href="/board">${items.length - limit} more on the full board</a>` : "");
    const show = id => seg === "all" || seg === id;
    return `<header class="top"><h1>Videos</h1><a class="more" href="/board">Full board ›</a></header>
      <div class="seg">${segs}</div><div class="chips">${chips}</div>
      ${show("working") ? section("Working", g.working.length, list(g.working, 30) || empty("No agent is on a video this minute.")) : ""}
      ${show("queued") ? section("Queued", g.queued.length, list(g.queued, 30) || empty("Nothing queued.")) : ""}
      ${show("backlog") ? section("Backlog", g.backlog.length, list(g.backlog, seg === "backlog" ? 60 : 10) || empty("Backlog is empty.")) : ""}
      ${seg === "all" ? section("On YouTube", g.done.length, list(g.done, 10)) : ""}`;
  }

  function review(b) {
    const vs = ((b.tracker || {}).videos) || [];
    const need = forBen(vs).map(v => `<div class="rcard">${row(v, `<span class="tag amber">Needs your review</span>`, uatLink(v))}
      <a class="btn watch" href="${uatLink(v)}">▶ Watch & review ${esc((v.watch || {}).version || v.version || "")}</a></div>`).join("");
    const checked = vs.map(v => (sent[v.checkId] || {}).key === v.key ? Object.assign({}, v, { check: sent[v.checkId] }) : v);
    const done = checked.filter(v => v.check && v.check.at).sort((a, b) => Date.parse(b.check.at) - Date.parse(a.check.at)).slice(0, 8)
      .map(v => row(v, `<span class="tag ${v.check.verdict === "ok" ? "green" : "amber"}">${v.check.verdict === "ok" ? "You OK'd" : "You asked for changes"} ${esc(v.check.version || "")}</span>`)).join("");
    return `<header class="top"><h1>Review</h1></header><p class="meta">Finished videos only. Everything else is the agents' job.</p>
      ${section("Needs your review", forBen(vs).length, need || empty("Nothing to watch right now. You'll get a message when there is."))}
      ${section("Reviewed", null, done || empty("No reviews yet."))}`;
  }

  // UAT screen (Ben, 28 Oct): the cut in a player, notes stamped with the playback time, Approve or Request changes.
  // Your notes go to the agents as the change list; they bring back the next version without you managing tasks.
  const stamp = sec => `${Math.floor(sec / 60)}:${String(Math.floor(sec % 60)).padStart(2, "0")}`;
  function uat(b, key) {
    const v = ((((b.tracker || {}).videos) || []).find(x => x.key === key));
    if (!v) return `<header class="top"><a class="more back" href="#review">‹ Review</a></header>${empty("That video isn't waiting for review any more.")}`;
    const w = v.watch || {}, inPage = w.url && /^https:\/\//.test(w.url) && w.kind === "stream";
    const player = inPage ? `<video id="uat-video" controls playsinline preload="metadata" src="${esc(w.url)}"></video>`
      : w.url ? `<a class="btn watch" href="${esc(w.url)}" target="_blank" rel="noopener">▶ Open ${esc(w.version || "the cut")} in ${esc(w.source || "Files")}</a>`
      : empty("No file link yet. The agents will add it.");
    const actions = canTick(v) ? `<textarea id="uat-notes" rows="5" placeholder="Notes for the agents, one per line.&#10;0:38 text doesn't match the voice"></textarea>
        ${inPage ? '<div class="btns one"><button type="button" class="btn" data-stamp>+ Note at the current time</button></div>' : ""}
        <div class="btns"><button type="button" class="btn ok" data-ok="${esc(v.key)}">✓ Approve</button>
        <button type="button" class="btn chg" data-chg="${esc(v.key)}">Request changes</button></div>
        <p class="meta">Approve sends your OK; Request changes sends the notes above. The agents make the next version and it comes back here.</p>`
      : `<a class="btn" href="${boardLink(v)}">Open on the board to OK or change</a>`;
    return `<header class="top"><a class="more back" href="#review">‹ Review</a></header>
      <h1 class="uat-title">${esc(v.title)}</h1><p class="meta">${ch(v)} · ${kind(v)} · ${esc(w.version || v.version || "")}${v.airText ? " · airs " + esc(v.airText) : ""}</p>
      <div class="player">${player}</div>${actions}`;
  }

  // Green only for real work (a claimed job, or the Chief coordinating on a fresh relay check); amber for online but
  // idle, or a stale check-in; red for out of usage or failing (Ben, 28 Oct: a green light must mean something).
  function agentLight(id, working, status, chiefNow) {
    if (status === "red") return ["red", "Out"];
    if (working) return ["green", "Working"];
    if (chiefNow) return ["green", "Coordinating"];
    return ["amber", "Idle"];
  }

  function agents(b, now) {
    const m = b.models || {}, jobs = ((b.owb || {}).jobs) || [], c = m.chief || {}, s = summary(b, now);
    const status = Object.fromEntries((m.models || []).map(x => [x.id, x]));
    const team = Object.entries(AGENTS).map(([id, name]) => {
      const mine = jobs.filter(j => j.by === id && j.status === "claimed");
      const chain = (m.chiefChain || []).find(r => r.agent === id) || {};
      const why = mine.length ? "Working on " + mine.map(j => `${j.id}: ${j.title}`).join(" · ")
        : (status[id] || {}).why || chain.why || (id === "macbook" ? "waits for a MacBook job, plugged in and idle" : "no job right now");
      const [st, word] = agentLight(id, mine.length, (status[id] || {}).status, c.agent === id && m.fresh !== false);
      return `<div class="row agent"><span class="dot ${esc(st)}"></span><div class="body"><b>${esc(name)} <span class="tag ${st}">${word}</span>${c.agent === id ? ' <span class="tag">Chief</span>' : ""}</b>
        <span class="meta">${esc(clip(why, 110))}</span></div></div>`;
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
      ${section("Agent team", null, team + '<p class="meta">Green: working now. Amber: online but idle, or not checked in lately. Red: out of usage or failing; its jobs go to the next agent.</p>')}
      ${section("Credits", null, `<div class="credits">${credit}</div>`, ' <a class="more" href="/ai">See all</a>')}`;
  }

  // A scheduled video we can't vouch for gets one small warning; everything verified stays quiet.
  function readiness(v, at, now) {
    const flag = (v.flags || []).find(f => f && f.text);
    if (flag) return flag.text;
    if (v.approved && v.approved.warn) return v.approved.warn;
    const yt = v.youtube || {};
    if (!yt.videoId && yt.state !== "scheduled" && at - now < 7 * 864e5) return "Not uploaded to YouTube yet";
    if (yt.videoId && yt.state !== "scheduled" && yt.state !== "live") return "YouTube shows it unscheduled";
    return "";
  }

  function scheduleTab(b, now) {
    const rows = schedule(((b.tracker || {}).videos) || [], now);
    const day = at => new Date(at).toLocaleDateString("en-GB", { timeZone: "Europe/London", weekday: "long", day: "numeric", month: "short" });
    const time = at => new Date(at).toLocaleTimeString("en-GB", { timeZone: "Europe/London", hour: "2-digit", minute: "2-digit" });
    const item = r => { const warn = readiness(r.v, r.at, now);
      return row(r.v, `<span class="meta when">${esc(time(r.at))}${r.scheduled ? "" : " · planned date"}</span>${warn ? `<span class="tag amber">⚠ ${esc(clip(warn, 80))}</span>` : ""}`); };
    const byDay = list => { let out = "", last = "";
      for (const r of list) { const d = day(r.at); if (d !== last) { out += `<h3 class="day">${esc(d)}</h3>`; last = d; } out += item(r); }
      return out; };
    const week = rows.filter(r => r.at - now < 7 * 864e5), next = rows.filter(r => r.at - now >= 7 * 864e5 && r.at - now < 14 * 864e5);
    const later = rows.filter(r => r.at - now >= 14 * 864e5);
    return `<header class="top"><h1>Schedule</h1></header>
      ${section("This week", week.length, byDay(week) || empty("Nothing scheduled this week."))}
      ${section("Next week", next.length, byDay(next) || empty("Nothing yet."))}
      ${section("Later", later.length, byDay(later.slice(0, 12)) || empty("Nothing yet."))}`;
  }

  function renderTab(tab, b, now) {
    if (!b || !b.tracker) return '<p class="empty">Loading the studio…</p>';
    return ({ overview, videos, review, agents, schedule: scheduleTab }[tab] || overview)(b, now);
  }

  function current() {
    const t = (location.hash || "").replace("#", "");
    if (t.startsWith("uat=")) return "review";
    return TABS.some(([id]) => id === t) ? t : "overview";
  }
  const uatKey = () => { const m = (location.hash || "").match(/^#uat=(.+)$/); return m ? decodeURIComponent(m[1]) : ""; };

  function render() {
    const tab = current(), now = Date.now();
    const key = uatKey();
    document.getElementById("view").innerHTML = key && board && board.tracker ? uat(board, key) : renderTab(tab, board, now);
    const ready = board ? forBen(((board.tracker || {}).videos) || []).length : 0;
    document.getElementById("nav").innerHTML = TABS.map(([id, label, icon]) =>
      `<a href="#${id}" class="${id === tab ? "on" : ""}"><span class="ic">${icon}</span>${label}${id === "review" && ready ? `<em>${ready}</em>` : ""}</a>`).join("");
    const byKey = k => (((board || {}).tracker || {}).videos || []).find(v => v.key === k);
    const notes = document.getElementById("uat-notes");
    document.querySelectorAll("[data-ok]").forEach(btn => btn.onclick = () => {
      const v = byKey(btn.dataset.ok); if (!v) return;
      sendTick(v, "ok"); location.hash = "#review";
    });
    document.querySelectorAll("[data-chg]").forEach(btn => btn.onclick = () => {
      const v = byKey(btn.dataset.chg); if (!v) return;
      const raw = notes ? notes.value.trim() : "";
      if (!raw) { if (notes) { notes.focus(); toast("Add a note first: what should change?", true); } else openChanges(v); return; }
      sendTick(v, "change", raw); location.hash = "#review";
    });
    document.querySelectorAll("[data-stamp]").forEach(btn => btn.onclick = () => {
      const vid = document.getElementById("uat-video"); if (!vid || !notes) return;
      vid.pause();
      notes.value = (notes.value && !notes.value.endsWith("\n") ? notes.value + "\n" : notes.value) + stamp(vid.currentTime) + " ";
      notes.focus();
    });
    document.querySelectorAll("[data-seg]").forEach(btn => btn.onclick = () => { seg = btn.dataset.seg; render(); });
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
      if (!uatKey() || !document.getElementById("uat-notes")) render();  // never wipe notes or the player mid-review
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
