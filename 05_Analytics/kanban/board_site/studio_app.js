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
  const POOLS = { elevenlabs: "ElevenLabs", flow: "Flow", vertex: "Vertex", cursor: "Cursor", codex: "Codex" };
  let board = null, lastSha = "", filterCh = "all", filterType = "all", seg = "all";
  const sent = {};  // checkId -> the tick just sent, until board.json shows it
  const MACBOOK = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/macbook-heartbeat/heartbeat.json";
  let macbook = null;  // the MacBook worker's own report (scripts/macbook_worker.py push_heartbeat), every 15 min
  // Ben's board links carry his tick key (/#k=...); that page lives at /board now, so hand them over untouched.
  if (/(?:^#|&)k=/.test(location.hash)) { location.replace("/board" + location.hash); return; }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }
  const ch = v => v.channel === "HOS" ? "HOS" : "Orbit";
  const kind = v => v.type === "short" ? "Short" : "Long";
  const detailLink = v => `#v=${encodeURIComponent(v.key)}`;  // every video opens in the hub (Ben, 28 Oct: not the old board)
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
  // Percent of the steps the agent reported done (Ben, 28 Oct: "add percentages"), never an estimate.
  const pct = p => Math.round(Math.min(1, Math.max(0, p.step / p.of)) * 100);
  const bar = (p, left) => p ? `<div class="prog"><div class="bar"><i style="width:${pct(p)}%"></i></div><span><b>${pct(p)}%</b> · ${p.step} of ${p.of}${left ? " · " + left : ""}</span></div>` : "";

  // ETA (Ben, 28 Oct): from when the job started and the steps it reported, else the typical time for that kind of
  // job (board owb estMin, from past runs). Always "about"; a job past its estimate says so instead of inventing one.
  const MIN = 6e4;
  function etaOf(j, now) {
    const full = ((((board || {}).owb || {}).jobs) || []).find(x => x.id === j.id) || {};
    const start = Date.parse(full.claimedAt || j.claimedAt || ""), est = +(full.estMin || j.estMin) || 0;
    if (!start || isNaN(start)) return null;
    const p = j.progress || full.progress || {}, done = +p.step || 0, of = +p.of || 0, spent = Math.max(0, now - start);
    let left = null;
    if (done > 0 && of > done) left = spent / done * (of - done);
    else if (est) left = est * MIN - spent;
    if (left == null) return null;
    if (left <= 0) return { over: true };
    return { min: Math.max(1, Math.round(left / MIN)), at: now + left };
  }
  const etaText = e => !e ? "" : e.over ? "taking longer than usual"
    : `about ${e.min < 60 ? e.min + " min" : Math.round(e.min / 6) / 10 + " h"} left (done ~${new Date(e.at).toLocaleTimeString("en-GB", { timeZone: "Europe/London", hour: "2-digit", minute: "2-digit" })})`;
  const clip = (s, n) => { s = String(s || ""); return s.length > n ? s.slice(0, n - 1) + "…" : s; };
  const activeJob = v => (v.jobs || []).find(j => j.status === "claimed");
  // One meaning of "working" everywhere (Ben, 28 Oct: 11 / 1 / 0 read as a contradiction): an agent has claimed a job
  // on it right now. The tracker's looser v.working flag is not used here.
  const isWorking = v => !!activeJob(v);

  // What the agents are doing on a video, in one line: who, the task, and the step they reported.
  function doing(v) {
    const j = activeJob(v);
    if (!j) return "";
    const left = etaText(etaOf(j, Date.now()));
    return `<span class="doing">${esc(AGENTS[j.by] || j.by || "An agent")} · ${esc(clip(j.remaining_action || j.title, 70))}</span>`
      + (progressOf(v) ? bar(progressOf(v), left) : left ? `<span class="meta">${esc(left)}</span>` : "");
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
      progress: inProgress(vs), week, chief: m.chief || {}, runner: m.runner || {},
      jobs: { working: jobs.filter(j => j.status === "claimed").length, queued: jobs.filter(j => j.status === "open").length,
              held: jobs.filter(j => j.status === "blocked").length, doneToday: ((b.owb || {}).day || {}).doneToday || 0 },
    };
  }

  function row(v, extra, href) {
    return `<a class="row" href="${href || detailLink(v)}">${thumb(v)}<div class="body"><b>${esc(v.title)}</b>
      <span class="meta">${ch(v)} · ${kind(v)}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}</span>${extra || bar(progressOf(v))}</div><span class="chev">›</span></a>`;
  }
  const jobTiles = j => `<div class="tiles three"><div class="tile-stat"><b class="blue">${j.working}</b><span>Jobs running</span></div>
      <div class="tile-stat"><b>${j.queued}</b><span>Jobs queued</span></div><div class="tile-stat"><b>${j.held}</b><span>Jobs on hold</span></div></div>`;
  const section = (title, n, body, more) => `<section><h2>${esc(title)}${n != null ? ` <span class="n">${n}</span>` : ""}${more || ""}</h2>${body}</section>`;
  const empty = text => `<p class="empty">${esc(text)}</p>`;

  // The Mac mini works one job at a time, round the clock: say so, so a gap between two jobs never reads as "stopped".
  function miniLine(s, b) {
    const jobs = ((b.owb || {}).jobs) || [], r = s.runner || {};
    const live = jobs.find(j => j.status === "claimed");
    const left = live ? etaText(etaOf(live, Date.now())) : "";
    const text = live ? `Mac mini working: ${AGENTS[live.by] || live.by} on ${live.id} · ${clip(live.remaining_action || live.title, 60)}${left ? " · " + left : ""}`
      : s.jobs.queued ? `Mac mini between jobs · ${s.jobs.queued} queued, the next starts within minutes`
      : r.state ? "Mac mini idle · nothing queued" : "";
    return text ? `<p class="mini ${live ? "on" : ""}"><i></i>${esc(text)}</p>` : "";
  }

  function overview(b, now) {
    const s = summary(b, now);
    const tiles = `<div class="tiles">
      <a class="tile-stat" href="#review"><b class="${s.ready.length ? "amber" : ""}">${s.ready.length}</b><span>Ready for you</span></a>
      <a class="tile-stat" href="#videos"><b class="blue">${s.progress.length}</b><span>Videos in production</span></a>
      <a class="tile-stat" href="#schedule"><b>${s.week.length}</b><span>Going live this week</span></a>
      <a class="tile-stat" href="#agents"><b class="${s.chief.agent ? "green" : "red"}">${esc(s.chief.name || "None")}</b><span>Chief · ${s.chief.agent ? "online" : "nobody up"}</span></a></div>`;
    const other = s.jobs.working - s.working.length;
    const working = (s.working.slice(0, 3).map(v => row(v, doing(v))).join("") || empty("No agent is on a video this minute."))
      + (other > 0 ? `<p class="meta">Plus ${other} studio job${other > 1 ? "s" : ""} not tied to one video (audits, credit readings, fixes). <a class="more" href="#agents">See Agents</a></p>` : "");
    const ready = s.ready.map(v => row(v, `<span class="meta">${esc(v.line || "")}</span>`, uatLink(v))).join("") || empty("Nothing waiting for you.");
    const pipe = `${jobTiles(s.jobs)}<p class="meta">Jobs are the agents' tasks across both channels. ${s.jobs.doneToday} finished today.</p>`;
    return `<header class="top"><div><h1>Studio</h1><p class="meta">Orbit With Ben · History of Science</p></div>
      <span class="pill ${s.health[0]}"><i></i>${esc(s.health[1])}</span></header>${miniLine(s, b)}${tiles}
      ${section("Ready for your review", s.ready.length, ready)}
      ${section("Videos an agent is on now", s.working.length, working, ' <a class="more" href="#videos">See all</a>')}
      ${section("Agent jobs", null, pipe, ' <a class="more" href="#agents">Agents</a>')}`;
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
    const segs = [["all", "All"], ["working", "Working"], ["queued", "Waiting"], ["backlog", "Backlog"]]
      .map(([id, label]) => `<button type="button" data-seg="${id}" class="${seg === id ? "on" : ""}">${label}${id === "all" ? "" : ` <small>${g[id].length}</small>`}</button>`).join("");
    const chips = [["ch", "all", "Both"], ["ch", "OWB", "Orbit"], ["ch", "HOS", "HOS"], ["ty", "long", "Longs"], ["ty", "short", "Shorts"]]
      .map(([k, val, label]) => `<button type="button" data-f="${k}" data-v="${val}" class="${(k === "ch" ? filterCh : filterType) === val ? "on" : ""}">${label}</button>`).join("");
    const list = (items, limit) => items.slice(0, limit).map(v => row(v, isWorking(v) ? doing(v) : "")).join("")
      + (items.length > limit ? `<p class="meta">${items.length - limit} more: pick Orbit or HOS, Longs or Shorts to narrow the list.</p>` : "");
    const show = id => seg === "all" || seg === id;
    return `<header class="top"><h1>Videos</h1></header>
      <div class="seg">${segs}</div><div class="chips">${chips}</div>
      ${show("working") ? section("An agent is on it now", g.working.length, list(g.working, 30) || empty("No agent is on a video this minute.")) : ""}
      ${show("queued") ? section("In production, waiting for its next step", g.queued.length, list(g.queued, 30) || empty("Nothing waiting.")) : ""}
      ${show("backlog") ? section("Backlog", g.backlog.length, list(g.backlog, seg === "backlog" ? 60 : 10) || empty("Backlog is empty.")) : ""}
      ${seg === "all" ? section("On YouTube", g.done.length, list(g.done, 10)) : ""}`;
  }

  // One video, in the hub: where it is, who is on it, what is left, your notes, and its links.
  const JOB_WORD = { claimed: ["green", "Working"], open: ["", "Queued"], blocked: ["amber", "On hold"], done: ["", "Done"] };
  function detail(b, key) {
    const v = ((((b.tracker || {}).videos) || []).find(x => x.key === key));
    const back = `<header class="top"><a class="more back" href="javascript:history.back()">‹ Back</a></header>`;
    if (!v) return back + empty("That video isn't on the board any more.");
    const yt = v.youtube || {}, w = v.watch || {};
    const links = [
      forBen([v]).length ? `<a class="btn primary" href="${uatLink(v)}">▶ Watch & review</a>` : w.url ? `<a class="btn" href="${esc(w.url)}" target="_blank" rel="noopener">▶ Watch ${esc(w.version || v.version || "")}</a>` : "",
      yt.url ? `<a class="btn" href="${esc(yt.url)}" target="_blank" rel="noopener">Open on YouTube</a>` : "",
    ].filter(Boolean);
    const jobs = (v.jobs || []).slice().sort((a, b) => ["claimed", "open", "blocked", "done"].indexOf(a.status) - ["claimed", "open", "blocked", "done"].indexOf(b.status));
    const jobRows = jobs.map(j => { const [tone, word] = JOB_WORD[j.status] || ["", j.status];
      const why = j.status === "blocked" ? (j.hold && j.hold.condition) || j.result : j.remaining_action;
      return `<div class="job"><div class="job-top"><span class="tag ${tone}">${word}</span><b>${esc(clip(j.title || j.id, 90))}</b></div>
        <span class="meta">${esc(j.id)}${j.by ? " · " + esc(AGENTS[j.by] || j.by) : ""}${why ? " · " + esc(clip(why, 160)) : ""}</span>
        ${j.status === "claimed" ? (j.progress && j.progress.of > 0 ? bar(j.progress, etaText(etaOf(j, Date.now()))) : `<span class="meta">${esc(etaText(etaOf(j, Date.now())))}</span>`) : ""}</div>`; }).join("");
    const notes = (v.notes || []).map(n => `<li class="${n.done ? "done" : ""}">${n.t ? `<b>${esc(n.t)}</b> ` : ""}${esc(n.text)}</li>`).join("");
    const flags = (v.flags || []).map(f => `<span class="tag amber">⚠ ${esc(clip(f.text, 120))}</span>`).join("");
    return `${back}<div class="hero">${thumb(v)}</div>
      <h1 class="uat-title">${esc(v.title)}</h1>
      <p class="meta">${ch(v)} · ${kind(v)} ${esc(v.number || "")}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}${v.airText ? " · " + (yt.state === "live" && yt.privacy === "public" ? "published " : "airs ") + esc(v.airText) : ""}</p>
      ${flags ? `<div class="flags">${flags}</div>` : ""}
      ${v.line ? `<p class="line">${esc(v.line)}</p>` : ""}
      ${links.length ? `<div class="btns">${links.join("")}</div>` : ""}
      ${section("Agent work on this video", jobs.length, jobRows || empty("No agent jobs on this video right now."))}
      ${notes ? section("Your notes", null, `<ul class="notes">${notes}</ul>`) : ""}`;
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
      : `<p class="line">This Short is reviewed with its long film: your OK or changes there cover it.</p>`;
    return `<header class="top"><a class="more back" href="#review">‹ Review</a></header>
      <h1 class="uat-title">${esc(v.title)}</h1><p class="meta">${ch(v)} · ${kind(v)} · ${esc(w.version || v.version || "")}${v.airText ? " · airs " + esc(v.airText) : ""}</p>
      <div class="player">${player}</div>${actions}`;
  }

  // Green only for real work (a claimed job, or the Chief coordinating on a fresh relay check); amber for online but
  // idle, or a stale check-in; red for out of usage or failing (Ben, 28 Oct: a green light must mean something).
  // The MacBook says why it is or isn't working; silence for 40 min means asleep, lid closed, off or not set up.
  function macbookState(mb, now) {
    if (!mb || !mb.at) return ["amber", "No report", "no status from the MacBook yet: asleep, lid closed, off, or its worker not running"];
    const age = Math.round((now - Date.parse(mb.at)) / 6e4);
    if (age > 40) return ["amber", "Silent", `no report for ${age < 120 ? age + " min" : Math.round(age / 60) + " h"}: asleep, lid closed or off`];
    const why = (mb.why || []).join("; ");
    if (mb.state === "working") return ["green", "Working", `on ${mb.job}`];
    if (mb.state === "error") return ["red", "Error", why];
    if (mb.state === "idle") return ["amber", "Idle", why || "no MacBook job waiting"];
    return ["amber", "Waiting", why];
  }

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
      let why = mine.length ? "Working on " + mine.map(j => `${j.id}: ${j.title}`).join(" · ")
        : (status[id] || {}).why || chain.why || (id === "macbook" ? "waits for a MacBook job, plugged in and idle" : "no job right now");
      let [st, word] = agentLight(id, mine.length, (status[id] || {}).status, c.agent === id && m.fresh !== false);
      if (id === "macbook" && !mine.length) { const mbs = macbookState(macbook, now); st = mbs[0]; word = mbs[1]; why = mbs[2]; }
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
      ${jobTiles(s.jobs)}
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
    if (t.startsWith("v=")) return "videos";
    return TABS.some(([id]) => id === t) ? t : "overview";
  }
  const uatKey = () => { const m = (location.hash || "").match(/^#uat=(.+)$/); return m ? decodeURIComponent(m[1]) : ""; };
  const videoKey = () => { const m = (location.hash || "").match(/^#v=(.+)$/); return m ? decodeURIComponent(m[1]) : ""; };

  function render() {
    const tab = current(), now = Date.now();
    const key = uatKey();
    const vk = videoKey(), ready = board && board.tracker;
    document.getElementById("view").innerHTML = key && ready ? uat(board, key) : vk && ready ? detail(board, vk) : renderTab(tab, board, now);
    const waiting = board ? forBen(((board.tracker || {}).videos) || []).length : 0;
    document.getElementById("nav").innerHTML = TABS.map(([id, label, icon]) =>
      `<a href="#${id}" class="${id === tab ? "on" : ""}"><span class="ic">${icon}</span>${label}${id === "review" && waiting ? `<em>${waiting}</em>` : ""}</a>`).join("");
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
      try { const mb = await fetch(MACBOOK + "?t=" + Date.now(), { cache: "no-store" }); macbook = mb.ok ? await mb.json() : null; } catch (e) {}
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
