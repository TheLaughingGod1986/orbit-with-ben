(function () {
  // Studio app, the board's front page (Ben, 28 Oct 2026 mock-up): Overview, Videos, Review, Agents, Schedule.
  // Reads the same board.json as the video board (/board) and the AI page (/ai). Its only write is Ben's OK / changes
  // tick on the Review tab, sent to /api/checks exactly as /board sends it (same document, same key, no confirmation).
  const DATA_REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";
  // One cached read on our own site first (api/ref.js); GitHub directly only if that fails (29 Oct audit: the
  // unauthenticated GitHub limit, 60 an hour per IP, ran out with three pages open).
  const refFetch = () => fetch("/api/ref", { cache: "no-cache" }).then(r => r.ok ? r : fetch(DATA_REF, { cache: "no-cache" }))
    .catch(() => fetch(DATA_REF, { cache: "no-cache" }));
  const DATA_AT = sha => `https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/${sha}/board.json`;
  const DATA = "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/board-data/board.json";
  const TABS = [["overview", "Overview", "⌂"], ["videos", "Videos", "▤"], ["review", "Review", "▶︎"], ["agents", "Agents", "◉"], ["schedule", "Schedule", "▦"]];
  const QUIET_MIN = 75;  // the relay checks in every 10-20 min; this long without it, the Mac mini is quiet
  const AGENTS = { chief: "Grok", claude: "Claude", codex: "Codex", gemini: "Gemini", cursor: "Cursor", macbook: "MacBook", "macbook-2": "MacBook 2" };
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
  // Channels come from board.channels (channels/*/channel.json via board_publish); these two are the fallback for an
  // older board.json. A third channel shows up here, in the filters and on its tiles with no page change.
  const DEFAULT_CHANNELS = [{ slug: "owb", label: "OWB", name: "Orbit With Ben", short: "Orbit", home: true },
                            { slug: "hos", label: "HOS", name: "History of Science", short: "HOS" }];
  const channelList = () => ((board || {}).channels || []).length ? board.channels : DEFAULT_CHANNELS;
  const homeChannel = () => channelList().find(c => c.home) || channelList()[0];
  const chInfo = label => channelList().find(c => c.label === String(label || "").toUpperCase()) || homeChannel();
  const repoLabel = repo => (channelList().find(c => c.slug === repo) || homeChannel()).label;
  const chName = label => chInfo(label).name;
  const ch = v => chInfo(v.channel).short || chInfo(v.channel).label;
  function watchFormat(v) {
    const w=v.watch||{};
    if(['long','short'].includes(w.type)) return w.type;
    return /(?:^|\/)10_Shorts\/|(?:^|\/)[^/]*_short(?:_v\d+[a-z0-9-]*)?(?:_PHONE)?\.mp4$/i.test(String(w.file||'').replace(/\\/g,'/'))?'short':'';
  }
  function normalizeCut(v) {
    const format=watchFormat(v);
    return format && format!==v.type && !(v.youtube||{}).videoId ? {...v,type:format,cutFormatCorrected:true}:v;
  }
  const kind = v => normalizeCut(v).type === "short" ? "Short" : "Long";
  function unconfirmedCut(v) {
    if ((v.production||{}).scope==='cut' && (v.production||{}).scopeVersion===v.version && (!(v.watch||{}).version || v.watch.version===v.version)) return false;
    return (v.production||{}).scope==='unconfirmed_cut' || !!normalizeCut(v).cutFormatCorrected || !!(v.watch && ((v.production||{}).milestones||[]).some(m=>/^\s*AR cohort:/i.test((m.source||{}).note||m.evidence||'')));
  }
  const relatedProduction=v=>(v.production||{}).projectHistory||v.production||{};
  const relatedStage=v=>currentProduction({...v,production:relatedProduction(v)})[0];
  const detailLink = v => `#v=${encodeURIComponent(v.key)}`;  // every video opens in the hub (Ben, 28 Oct: not the old board)
  const LIVE = j => j && (j.status === "claimed" || j.status === "open" || j.status === "blocked");

  // A real picture only: the YouTube thumbnail when the video has an id, otherwise a channel tile with its number.
  function thumb(v) {
    // YouTube has no thumbnail for a private or scheduled video (404): ask only for public ones.
    const id = isLive(v) && v.youtube.videoId;
    const fallback = `<span class="tile ${esc(chInfo(v.channel).slug)}">${esc(v.number || "")}</span>`;
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
  function jobGroups(vs) {
    const groups = new Map();
    for (const v of vs) {
      const j = activeJob(v);
      const id = (j && j.id) || v.key;
      groups.set(id, (groups.get(id) || []).concat([v]));
    }
    return [...groups.values()];
  }
  const alsoOn = rest => !rest.length ? "" : `<span class="meta">Same job also covers ${rest.length} more: ${esc(rest.map(v =>
    `${v.number}${v.type === "short" ? " Short" : ""}`).join(", "))}</span>`;
  // Running jobs no video carries (audits, checks, batch fixes): the same set on Overview and Videos.
  function studioJobs(b) {
    const onVideo = new Set((((b.tracker || {}).videos) || []).filter(isWorking).map(v => activeJob(v).id));
    return (((b.owb || {}).jobs) || []).filter(j => j.status === "claimed" && !onVideo.has(j.id));
  }
  function jobCard(j) {
    const left = etaText(etaOf(j, Date.now())), p = j.progress && j.progress.of ? j.progress : null;
    const working = j && j.status === "claimed";
    const dot = working ? `<span class="p24-working-dot" role="img" aria-label="A job is in progress"></span>` : "";
    return `<a class="row${working ? " is-working" : ""}" href="#agents">${dot}<div class="thumb job">${esc(j.id)}</div><div class="body"><b>${esc(clip(j.remaining_action || j.title, 90))}</b>
      <span class="meta">${esc(j.plain || "Studio job · not one video")}</span><span class="doing">${esc(AGENTS[j.by] || j.by || "An agent")} · ${esc(j.id)}</span>
      ${p ? bar(p, left) : left ? `<span class="meta">${esc(left)}</span>` : ""}</div><span class="chev">›</span></a>`;
  }
  const uatLink = v => `#uat=${encodeURIComponent(v.key)}`;

  function pendingChanges(v) {
    if (isLive(v)) return false;
    const local=sent[v.checkId], c=local && local.key===v.key ? local : v.type==='long' ? v.check : null;
    return !!c && c.verdict==='change' && c.handled!==true && !!c.version && c.version===v.version;
  }
  // Passed / Scheduled status in plain words (Ben, 7 Nov 2026). Never invent a publishAt or YouTube id.
  function listingLine(v) {
    const L = v.listing || {}, yt = v.youtube || {};
    if (L.status) return L.status;
    if (yt.state === "scheduled" && (yt.publishAtLondon || yt.publishAt)) {
      const raw = String(yt.publishAtLondon || yt.publishAt).replace(/\s*(GMT|BST|UTC)\s*$/i, "").trim();
      return /London/i.test(raw) ? `Scheduled for ${raw}` : `Scheduled for ${raw} London`;
    }
    if (Array.isArray(L.missing) && L.missing.length) return "Needs " + L.missing.join(", ");
    if (L.complete) return L.destination === "social" ? "Ready to post" : "Ready to upload";
    return "";
  }
  // Scheduled on YouTube with a real publishAt only — never invent a slot (Ben, 7 Nov 2026).
  const isScheduledNotPublic = v => {
    const yt = v.youtube || {};
    return !isLive(v) && yt.state === "scheduled" && !!(yt.publishAt || yt.publishAtLondon);
  };
  // Specialist / Chief review — agent-owned QA, never a Ben blocker (Ben, 7 Nov 2026).
  function isQa(v) {
    if (v.lane === "ready" && v.readyFor && v.readyFor !== "Ben") return true;
    return (v.jobs || []).some(j => {
      if (!LIVE(j)) return false;
      const kind = String(j.kind || "").toLowerCase();
      if (kind === "review" || kind === "qa" || kind === "chief") return true;
      return !kind && /\b(review|KEEP|shot list|Chief QA|frame review)\b/i.test(j.title || "");
    });
  }
  // Waiting on Ben's watch only (same gate as Review / forBen, without the uniqueVideos pass).
  function needsBenWatch(v) {
    return !isLive(v) && v.lane === "ready" && v.readyFor === "Ben" && !sent[v.checkId] && !pendingChanges(v)
      && !!(v.watch || {}).url;
  }
  // Nine exclusive Videos swim lanes. Later stages win. Only UAT is Ben's; everything else is agent-run
  // (Ben, 7 Nov 2026). UAT OK → Passed; UAT notes/fixes → In progress (pendingChanges / changes).
  const VIDEO_LANE_ORDER = ["backlog", "todo", "progress", "qa", "uat", "passed", "scheduled", "live", "postlive"];
  const VIDEO_LANE_CHIPS = [
    ["backlog", "Backlog"], ["todo", "To do"], ["progress", "In progress"], ["qa", "QA"], ["uat", "UAT"],
    ["passed", "Passed"], ["scheduled", "Scheduled"], ["live", "Live"], ["postlive", "Post-live"],
  ];
  const VIDEO_LANE_COPY = {
    backlog: { title: "Backlog", blurb: "Planned, not started yet." },
    todo: { title: "To do", blurb: "In the work mix · waiting for its next step. Agents own this — nothing for Ben." },
    // Working-now vs waiting: claimed jobs surface first; open/blocked/queued stay in this lane (Ben, 7 Nov 2026).
    progress: { title: "In progress", blurb: "Working now first (green pulse = a claimed job). Waiting and queued cuts stay below. UAT notes land here too — not a Ben blocker." },
    qa: { title: "QA", blurb: "Specialist review · not for Ben." },
    uat: { title: "UAT", blurb: "Ready for your watch. Pass → Passed (ready to schedule). Notes → In progress for the agents." },
    passed: { title: "Passed", blurb: "You passed it · ready to schedule. Agents finish the listing package and upload handoff." },
    scheduled: { title: "Scheduled", blurb: "On YouTube · waiting to go public. Agents own the schedule — nothing for Ben." },
    live: { title: "Live", blurb: "Public." },
    postlive: { title: "Post-live", blurb: "Public · improvements still open (pins, Related, thumb tests). Agents own these." },
  };
  // Same signal Overview uses for the green pulse: a claimed job on this cut (not open/blocked/waiting).
  const videoHasActiveWork = v => isWorking(v);
  function partitionProgressVideos(items) {
    const working = [], waiting = [];
    for (const v of items || []) {
      if (videoHasActiveWork(v)) working.push(v);
      else waiting.push(v);
    }
    return { working, waiting };
  }
  // Parent film key for progress24h lookup (Shorts share the long's film progress; never invent a %).
  function videoFilmKey(v) {
    const key = String((v && v.key) || "");
    const m = /^([A-Z]+:\d{3})/.exec(key);
    return m ? m[1] : key;
  }
  function videoProgressDelta(v, b) {
    const p = b && b.progress24h;
    if (!p) return null;
    const filmKey = videoFilmKey(v);
    if (!filmKey) return null;
    const films = p24MergeFilms(p.films || [], p.moved || []);
    const f = films.find(x => x.film === filmKey || x.film === v.key
      || p24InFocus(v.key, new Set([x.film])) || p24InFocus(filmKey, new Set([x.film])));
    return f ? p24FilmPct(f) : null;
  }
  function videoLane(v) {
    if (v.collapsed && isLive(v)) return null;
    if (isLive(v) && (v.jobs || []).some(LIVE)) return "postlive";
    if (isLive(v)) return "live";
    if (isScheduledNotPublic(v)) return "scheduled";
    // Passed stays Passed even while an upload/social job runs — it is ready to schedule, not a Ben hold.
    if (v.lane === "approved") return "passed";
    if (needsBenWatch(v)) return "uat";
    // Ben's Request changes / notes return the film to In progress before QA.
    if (pendingChanges(v) || v.lane === "changes") return "progress";
    if (isQa(v)) return "qa";
    if (isWorking(v) || (v.jobs || []).some(LIVE)) return "progress";
    if (v.lane === "upcoming") return "backlog";
    if (["progress", "ready", "changes", "approved"].includes(v.lane)) return "todo";
    if (v.lane === "done") return "todo";
    return "todo";
  }
  function stage(v) {
    const lane = videoLane(v);
    if (lane === "live" || isLive(v)) return "Published";
    if (lane === "postlive") return "Post-live improvements";
    if (lane === "scheduled") return listingLine(v) || "Scheduled";
    if (lane === "passed") return listingLine(v) || "Ready to schedule";
    if (lane === "uat") return "Ready for you";
    if (lane === "qa") return "In review";
    if (pendingChanges(v) || v.lane === "changes") return "Fixing your changes";
    if ((v.youtube || {}).state === "scheduled") return listingLine(v) || "Scheduled";
    if (v.lane === "ready") return v.readyFor === "Ben" ? "Ready for you" : `Waiting on ${v.readyFor || "a check"}`;
    if (v.lane === "approved") return listingLine(v) || "Ready to schedule";
    if (v.lane === "done") return v.youtube && v.youtube.state === "scheduled" ? (listingLine(v) || "Scheduled") : "On YouTube";
    const live = (v.jobs || []).find(j => j.status === "claimed");
    if (live) return "Working now";
    if ((v.jobs || []).some(j => j.status === "blocked")) return "Waiting";
    return v.lane === "upcoming" ? "Planned" : "In progress";
  }

  // Only with its video attached (Ben, 5 Nov 2026: three Shorts showed at 12:49:43 and their links came 40 s later, so
  // Watch & review opened an empty page).
  const forBen = vs => uniqueVideos(vs).filter(v => !isLive(v) && v.lane === "ready" && v.readyFor === "Ben" && !sent[v.checkId] && !pendingChanges(v)
    && !!(v.watch || {}).url);
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
  // Public on YouTube is published, whatever follow-up jobs it still carries (29 Oct audit: Venus, the Earth and
  // Apophis Shorts sat in "in production" because of a title test or a Related-video step).
  const isLive = v => !!v.youtube && (v.youtube.privacy === "public" || v.youtube.state === "live");
  // Overview "in production": agent lanes only — never UAT / Passed / Scheduled / Live / Post-live (Ben, 7 Nov 2026).
  const inProgress = vs => vs.filter(v => ["todo", "progress", "qa"].includes(videoLane(v)));

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
    const vs = ((b.tracker || {}).videos) || [], m = b.models || {};
    // Every job once: the general list plus the jobs carried on video cards (5 Nov 2026: the Mini's J2176 lives on the
    // 032 card, so "Jobs running" said 1 while the Mini and the MacBook both worked).
    const byId = new Map();
    for (const j of [...(((b.owb || {}).jobs) || []), ...vs.flatMap(v => v.jobs || [])]) if (j && j.id && !byId.has(j.id)) byId.set(j.id, j);
    const jobs = [...byId.values()];
    const quietMin = (now - Date.parse(m.checkedAt || "")) / 6e4;
    const health = !m.checkedAt || isNaN(quietMin) ? ["amber", "No news yet"]
      : quietMin > QUIET_MIN ? ["red", `Mac mini quiet ${Math.round(quietMin / 60)} h`]
      : (m.models || []).some(x => x.status === "red") ? ["amber", "Running, some agents out"] : ["green", "Healthy"];
    const week = scheduledThisWeek(vs, now);
    return {
      health, ready: forBen(vs), working: vs.filter(isWorking),
      progress: inProgress(vs), week, chief: m.chief || {}, runner: m.runner || {},
      jobs: { working: jobs.filter(j => j.status === "claimed").length, queued: jobs.filter(j => j.status === "open").length,
              held: jobs.filter(j => j.status === "blocked").length, doneToday: ((b.owb || {}).day || {}).doneToday || 0 },
    };
  }

  function row(v, extra, href, opts) {
    const working = !!(opts && opts.working);
    const dot = working
      ? `<span class="p24-working-dot" role="img" aria-label="A job is in progress on this cut"></span>`
      : "";
    return `<a class="row${working ? " is-working" : ""}" href="${href || detailLink(v)}">${dot}${thumb(v)}<div class="body"><b>${esc(v.title)}</b>
      <span class="meta">${ch(v)} · ${kind(v)}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}</span>${extra || (isLive(v) ? "" : bar(progressOf(v)))}</div><span class="chev">›</span></a>`;
  }
  const jobTiles = j => `<div class="seg" aria-label="Job counts"><div><b>${j.working}</b><span>Running</span></div><div><b>${j.queued}</b><span>Queued</span></div><div><b>${j.held}</b><span>Waiting</span></div></div>`;
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

  // Milestone progress is independent of job step progress. Older board data stays readable.
  function uatOutlook(v, now) {
    if (pendingChanges(v)) return {label:"Changes requested",detail:"Your notes need correction and fresh QA before another review",tone:"amber"};
    if (v.lane === "ready" && v.readyFor === "Ben") return {label: "Ready for UAT", detail: "Your review can start now", tone: "green"};
    if (["approved", "done"].includes(v.lane)) return {label: "UAT handoff passed", detail: "Follow-up work is shown below", tone: "green"};
    if (unconfirmedCut(v)) return {label:'UAT ETA unavailable',detail:'Progress for this exact cut is unconfirmed',tone:'amber'};
    const p = v.production, e = p && p.eta;
    if (!e) return {label: "UAT ETA unavailable", detail: "Production milestones have not been published yet", tone: "amber"};
    if (e.state === "estimated") {
      const age = (now - Date.parse(p.asOf || "")) / MIN;
      if (!Number.isFinite(age) || age < 0 || age > QUIET_MIN) return {label: "UAT ETA unavailable", detail: "Forecast needs fresh production data", tone: "amber"};
      if (age >= e.upperMinutes) return {label: "UAT ETA unavailable", detail: "Historical range exceeded · waiting for a new production update", tone: "amber"};
      return {label: `UAT in about ${Math.max(0, Math.ceil(e.lowerMinutes - age))}–${Math.ceil(e.upperMinutes - age)} min`,
        detail: `${e.confidence} confidence · historical stage durations · estimate, not a deadline`, tone: "blue"};
    }
    return {label: "UAT ETA unavailable", detail: (e.reasons || []).join(" · ") || "Waiting for production evidence", tone: "amber"};
  }
  const MILESTONES = [['topic','Topic'],['script','Script'],['sources','Fact checks'],['vo','Voice'],['shots','Shot plan'],['picture','Picture'],['edit','Edit'],['thumbs','Packaging'],['qa','Chief QA']];
  const expandedStages = new Map();
  const disclosureState = new Map();
  let renderedView="", renderedNav="", focusedJobRoute="";
  let videoSort = 'uat';
  const completeStage = m => ['done','skip','passed'].includes(m.displayState || m.state) && !m.awaitingApproval;
  function milestones(v) {
    const recorded = new Map(((v.production || {}).milestones || []).map(m => [m.id, m]));
    return MILESTONES.map(([id,label]) => Object.assign({id,label,state:'unknown',dependsOn:[]}, recorded.get(id)));
  }
  function progressStats(v) {
    const rows = milestones(v), done = rows.filter(completeStage).length;
    return {rows, done, total:9, percent:Math.round(done / 9 * 100), unknown:rows.filter(m => m.state === 'unknown').length};
  }
  function stageView(m) {
    const state = m.awaitingApproval ? 'review' : m.displayState || m.state;
    if (completeStage(m)) return {text:state === 'skip' ? 'Not required · recorded' : 'Completed',tone:'complete',icon:'✓'};
    if (state === 'review') return {text:'Awaiting approval',tone:'held',icon:'!'};
    if (state === 'blocked' && (m.jobs||[]).some(j=>reviewQueueInfo(board||{},j,Date.now(),macbook))) return {text:'Awaiting review',tone:'held',icon:'!'};
    if (state === 'blocked') return {text:'Waiting',tone:'held',icon:'!'};
    if (['doing','in_progress'].includes(state)) return {text:'In progress',tone:'active',icon:'●'};
    return {text:['todo','pending','queued'].includes(state) ? 'Not started' : 'Unconfirmed',tone:'neutral',icon:'○'};
  }
  function currentProduction(v) {
    const rows = milestones(v), ids = (v.production || {}).activeStages || [];
    const recorded = ids.map(id => rows.find(m => m.id === id)).filter(Boolean).filter(m => !completeStage(m));
    if (recorded.length) return recorded;
    // Backward-compatible selection from explicit stage states, prioritising approval/blocking work.
    const path = (((v.production || {}).eta || {}).criticalPath || []);
    return rows.filter(m => ['held','active'].includes(stageView(m).tone)).sort((a,b) =>
      (stageView(a).tone === 'held' ? 0 : 1) - (stageView(b).tone === 'held' ? 0 : 1)
      || (path.includes(a.id) ? 0 : 1) - (path.includes(b.id) ? 0 : 1));
  }
  const ownerName = m => AGENTS[m.owner] || m.owner || 'Unassigned';
  function conciseEvidence(m) {
    if (m.summary) return m.summary;
    const text = String(m.evidence || ''), parts = [];
    const flow = text.match(/\b(\d+)\s*\/\s*(\d+)\s+Flow\b/i);
    if (m.id === 'picture' && flow && /minted|generated/i.test(text)) parts.push(`${flow[1]}/${flow[2]} Flow shots generated`);
    if (m.version) parts.push(m.version);
    const score = Number((m.source || {}).score);
    if ((m.source || {}).score != null && Number.isFinite(score)) parts.push(`Score ${score}`);
    if (m.id === 'vo' && /Claude\s+(?:QA\s+)?PASS(?:ED)?\b/i.test(text)) parts.push('Claude QA passed');
    return parts.join(' · ');
  }
  function nextAction(m) {
    if (stageView(m).text === 'Awaiting approval') {
      const reviewer = m.reviewer || (/\b(?:parked|awaiting|waiting).*Chief\b/i.test(String(m.evidence || '')) ? 'chief' : '');
      return reviewer === 'chief' ? 'Chief reviews and approves this stage.' : reviewer ? `${AGENTS[reviewer] || reviewer} reviews and approves this stage.` : 'The recorded reviewer needs to approve this stage.';
    }
    const jobs = m.jobs || [];
    const job = jobs.find(j => j.status === 'blocked') || jobs.find(j => j.status === 'claimed') || jobs.find(j => j.status === 'open');
    const raw = m.nextAction || (job || {}).remaining_action || '';
    // Long/internal logs stay intact in technical details; never rewrite them into invented facts.
    if (raw && raw.length <= 140 && !/\bJ\d{3,}|\/[\w.-]+\/|sha256|credits?\b/i.test(raw)) return raw;
    if (stageView(m).tone === 'held') return 'Resolve the recorded blocker before this stage can continue.';
    return job && job.status === 'open' ? 'Waiting for an agent to start; queue timing is unconfirmed.' : 'No next action is recorded. Chief needs to confirm the handoff and owner.';
  }
  function blockerJobs(v,m) {
    const own=new Set((m.jobs||[]).map(j=>j.id)), jobs=new Map();
    for(const j of [...(v.jobs||[]),...(m.jobs||[])]) if(j.id && !jobs.has(j.id)) jobs.set(j.id,j);
    const refs=String((m.source||{}).ref||m.evidence||'').match(/\b[a-f0-9]{7,40}\b/gi)||[];
    return [...jobs.values()].filter(j=>j.status==='blocked').map(j=>{
      const exact=own.has(j.id)||j.stage===m.id;
      const text=[(j.hold||{}).condition,j.result,(j.progress||{}).note].join(' ');
      const reference=refs.some(ref=>new RegExp('\\b'+ref+'\\b','i').test(text));
      return {job:j,scope:exact?'stage':reference?'reference':'video',rank:exact?0:reference?1:2};
    }).sort((a,b)=>a.rank-b.rank || (Date.parse((b.job.hold||{}).checked_at)||0)-(Date.parse((a.job.hold||{}).checked_at)||0) || a.job.id.localeCompare(b.job.id));
  }
  function blockerReason(raw) {
    const text=String(raw||'').replace(/\s+/g,' ').trim();
    if(!text) return '';
    // A narrow source-backed paraphrase for the actual ISS hold; no generated plan or approval inference.
    if(/(?:lacks|missing)[\s\S]{0,80}approved ISS|approved ISS[\s\S]{0,240}remains missing/i.test(text)) return 'Approved moving footage of the International Space Station (ISS) is missing.';
    const sentences=text.split(/(?<=[.!?])\s+/);
    const relevant=sentences.find(x=>/missing|await|blocked|require|need|waiting|reject/i.test(x) && !/^J\d+ verified/i.test(x));
    return clip(relevant||text,240);
  }
  function blockerAction(raw) {
    return clip(String(raw||'').replace(/\bIdentify approved moving ISS opening input, then correct and review AR cohort\b/i,
      'Find an approved moving ISS opening clip, then correct and review the affected cuts'),280);
  }
  function blockerModel(v,m) {
    const entries=blockerJobs(v,m), best=entries[0];
    const source=m.source||{}, reviewer=m.reviewer && (AGENTS[m.reviewer]||m.reviewer);
    const stageApproval=stageView(m).text==='Awaiting approval';
    // A known stage approval must not be explained using an unrelated video-level hold.
    const useJob=best && (best.scope!=='video' || !stageApproval);
    if(useJob) {
      const j=best.job, hold=j.hold||{};
      return {job:j,scope:best.scope,why:blockerReason(hold.reason||hold.condition||j.result)||'The job is waiting, but its reason has not been recorded.',
        action:blockerAction(hold.action||j.remaining_action||'')||(stageApproval?nextAction(m):'No unblock action is recorded. The job owner needs to add the missing next step.'),
        owner:AGENTS[hold.owner||j.by]||hold.owner||j.by||'Not recorded',checkAt:hold.check_at||'',checkedAt:hold.checked_at||'',dependency:j.after||'',others:entries.filter(x=>x.job.id!==j.id)};
    }
    const evidence=String(source.note||source.proof||m.evidence||'');
    const meaningful=evidence.length>10 && /\s/.test(evidence) && !/^[a-f0-9]+$/i.test(evidence);
    return {scope:'stage',why:stageApproval?`Awaiting ${reviewer||'the recorded reviewer’s'} approval.`:meaningful?blockerReason(evidence):`${m.label} is marked waiting, but no stage-specific reason is recorded.`,
      action:stageApproval?nextAction(m):m.nextAction||'No unblock action is recorded. A responsible owner and a specific next step need to be recorded.',
      owner:stageApproval?(reviewer||'Not recorded'):ownerName(m)==='Unassigned'?'Not recorded':ownerName(m),others:entries};
  }
  function reviewQueueInfo(b,j,now,mb=null) {
    if(!j) return null;
    const jobs=((b.owb||{}).jobs)||[], state=(b.workflow||{}).states||{};
    const task=jobs.find(x=>x.kind==='review'&&x.ref===j.id&&['open','claimed'].includes(x.status))||jobs.find(x=>x.recheck_of===j.id&&['open','claimed'].includes(x.status));
    const needsReview=task&&task.kind==='review'&&task.ref===j.id||/(?:parked|awaiting|waiting) for (?:the )?Chief.*(?:review|approval)/i.test(String((j.hold||{}).condition||j.result||''));
    if(!task||!needsReview) return null;
    const fresh=stamp=>{const age=now-Date.parse(stamp||'');return Number.isFinite(age)&&age>=0&&age<=5*MIN;};
    const models=b.models||{}, chief=task.kind==='review'?(task.by||task.for):(models.chief||{}).agent, reviewer=AGENTS[chief]||chief||'Elected Chief';
    const ownState=state[task.id]||{}, predecessor=((b.owb||{}).jobStates||{})[task.after]||{};
    const ready=fresh((b.workflow||{}).at)?['queued','review'].includes(ownState.state):task.status==='open'&&!task.hold&&(!task.after||predecessor.status==='done')&&(!task.notBefore||Date.parse(task.notBefore)<=now);
    const active=jobs.find(x=>x.status==='claimed'&&x.by===chief);
    const next=(b.workflow||{}).next||{}, runner=models.runner||{};
    const starting=runner.state==='working'&&fresh(runner.at)&&next.id===runner.job&&next.worker===chief?jobs.find(x=>x.id===runner.job):null;
    const busy=fresh(models.checkedAt)?active||starting:null;
    const miniBusy=fresh(models.checkedAt)?jobs.find(x=>x.status==='claimed'&&x.needs!=='macbook'&&(state[x.id]||{}).state==='running'):null;
    const estimate=busy&&recordedTaskProgress(busy), started=busy&&Date.parse(busy.claimedAt||'');
    const eta=estimate&&estimate.step>0&&estimate.step<estimate.of&&Number.isFinite(started)&&started<=now?etaOf(busy,now):null;
    const availability=eta&&!eta.over?`Current task estimate: about ${durationText(eta.min)} remaining. A review start time is not reserved.`:'No reliable reviewer-free time is recorded.';
    const mbAge=mb?now-Date.parse(mb.at||''):NaN;
    const macbookText=Number.isFinite(mbAge)&&mbAge>=0&&mbAge<=20*MIN?`MacBook worker: ${mb.state||'state unreported'}${mb.job?' on '+mb.job:''}${(mb.why||[]).length?' · '+mb.why.join('; '):''}.`:'MacBook availability report is stale or missing.';
    return {task,reviewer,ready,busy,miniBusy,availability,macbookText};
  }
  function blockerGuide(v,m,now=Date.now()) {
    const model=blockerModel(v,m), j=model.job, review=reviewQueueInfo(board||{},j,now,macbook);
    const due=Date.parse(model.checkAt||''), checked=Date.parse(model.checkedAt||'');
    const states=((board||{}).owb||{}).jobStates||{}, dependency=states[model.dependency]||{};
    const dependencyStatus={done:'Completed',blocked:'Waiting',claimed:'In progress',open:'Queued',cancelled:'Cancelled'}[dependency.status]||'Status unreported';
    const check=Number.isFinite(due)?`${due<now?'Check overdue: ':'Next recorded check: '}${recordedTime(model.checkAt)}`:'No next check recorded';
    return `<div class="blocker-guide" data-blocker-scope="${model.scope}"><p class="blocker-scope">${model.scope==='reference'?'Related recorded hold':model.scope==='video'?'Video-level hold · stage link unconfirmed':'Recorded stage hold'}</p>
      <h3>${review?(review.task.kind==='review'?'Awaiting specialist review':'Awaiting Chief review'):'What it is waiting for'}</h3><p class="blocker-reason">${esc(model.why)}</p>
      <h3>What moves it on</h3><p class="blocker-action">${esc(model.action)}</p>
      <dl class="blocker-facts"><div><dt>${j?(review?'Previous worker':'Recorded job owner'):'Reviewer / owner'}</dt><dd>${esc(model.owner)}</dd></div><div><dt>Follow-up</dt><dd>${esc(check)}</dd></div>${Number.isFinite(checked)?`<div><dt>Last checked</dt><dd>${esc(recordedTime(model.checkedAt))}</dd></div>`:''}${model.dependency?`<div><dt>Recorded dependency</dt><dd>${esc(model.dependency)} · ${esc(dependencyStatus)}</dd></div>`:''}</dl>
      ${review?`<div class="review-handoff"><p><b>${esc(review.reviewer)} · ${review.ready?'review queued and eligible now':review.task.status==='claimed'?'review job claimed':'review queue state needs confirmation'}</b></p><a class="blocker-job-link" href="${jobRoute(review.task.id)}">Open review job ${esc(review.task.id)} →</a>${review.busy?`<p>${esc(review.reviewer)} is ${review.busy.status==='claimed'?'working on':'starting'} ${esc(review.busy.id)}: ${esc(clip(review.busy.remaining_action||review.busy.title,140))}</p>`:''}${!review.busy&&review.miniBusy?`<p>Mini execution: ${esc(AGENTS[review.miniBusy.by]||review.miniBusy.by||'Worker')} on ${esc(review.miniBusy.id)} · ${esc(clip(review.miniBusy.remaining_action||review.miniBusy.title,140))}. An extra execution slot is not confirmed by this report.</p>`:''}<details class="technical"><summary>Reviewer availability and MacBook</summary><p>${esc(review.availability)}</p><p>${esc(review.macbookText)}</p><p>Device availability does not establish media-review capability or Chief approval authority.</p></details></div>`:''}
      ${Number.isFinite(due)?`<p class="blocker-caption">${review?'The follow-up time does not schedule or delay the queued review.':'The check time is a follow-up, not a promise that the video will move on by then.'}</p>`:''}
      ${j?`<a class="blocker-job-link" href="${jobRoute(j.id)}">Open blocking job ${esc(j.id)} <span aria-hidden="true">›</span></a><details class="technical" data-disclosure="${esc(v.key)}-${esc(m.id)}-hold"><summary>Full recorded blocker</summary><div class="technical-body">${(j.hold||{}).condition?`<p>${esc(j.hold.condition)}</p>`:''}${j.remaining_action?`<p>Recorded next action: ${esc(j.remaining_action)}</p>`:''}${j.result?`<p>${esc(j.result)}</p>`:''}</div></details>`:''}
      ${model.others.length?`<details class="technical" data-disclosure="${esc(v.key)}-${esc(m.id)}-other-holds"><summary>${model.others.length} other recorded video hold${model.others.length===1?'':'s'}</summary><div class="technical-body">${model.others.map(({job})=>`<article><b>${esc(job.title||job.id)}</b><p>${esc(blockerReason((job.hold||{}).condition||job.result)||'Reason not recorded')}</p><p>Next step: ${esc(job.remaining_action||'Not recorded')}</p><a class="blocker-job-link" href="${jobRoute(job.id)}">Open ${esc(job.id)}</a></article>`).join('')}</div></details>`:''}</div>`;
  }
  function durationText(minutes) {
    minutes = Math.max(0, Math.round(minutes));
    const days = Math.floor(minutes/1440), hours = Math.floor(minutes%1440/60), mins = minutes%60;
    return [days ? `${days}d` : '', hours ? `${hours}h` : '', !days && mins ? `${mins}m` : ''].filter(Boolean).join(' ') || 'under 1m';
  }
  function forecastView(v, now) {
    const p = v.production || {}, e = p.eta || {}, o = uatOutlook(v, now);
    if (pendingChanges(v)) return {value:'Pending',reason:'Your requested changes need correction and fresh QA',confidence:'Unavailable',credible:false};
    if (v.lane === 'ready' && v.readyFor === 'Ben') return {value:'Ready now',reason:'Your review can start',confidence:'Ready',credible:false};
    if (['approved','done'].includes(v.lane) || isLive(v)) return {value:'Handoff complete',reason:'Production countdown ended',confidence:'Complete',credible:false};
    if (unconfirmedCut(v)) return {value:'Unconfirmed',reason:'Related project milestones do not establish readiness for this exact cut',confidence:'Unavailable',credible:false};
    if (e.state === 'estimated' && o.tone === 'blue') {
      const age = (now-Date.parse(p.asOf))/MIN;
      return {value:`~${durationText(e.lowerMinutes-age)}–${durationText(e.upperMinutes-age)}`,reason:'Estimated calendar time to your review',confidence:`${e.confidence === 'medium' ? 'Medium' : e.confidence === 'high' ? 'High' : 'Low'} confidence`,credible:true,minutes:e.upperMinutes-age};
    }
    const reasons = (e.reasons || []).join(' ');
    const reason = /fresh production|range exceeded/.test(o.detail) ? o.detail : /manual Flow/.test(reasons) ? 'Manual production timing is unconfirmed'
      : /blocked|review timing|dependency|Requested changes/.test(reasons) ? 'A production dependency needs resolving'
      : /queue|worker/.test(reasons) ? 'Queue start or agent availability is unconfirmed' : 'Insufficient historical timing data';
    const held=currentProduction(v).find(m=>stageView(m).tone==='held');
    const hold=held?blockerModel(v,held):null;
    return {value:'Pending',reason:hold?(hold.scope==='video'?'Video-level hold (stage link unconfirmed): ':'')+hold.why:reason,confidence:'Unavailable',credible:false};
  }
  function milestoneProgress(v) {
    if (isLive(v)) return '<span class="meta">Published</span>';
    if (forBen([v]).length) return '<span class="meta">Finished cut awaiting your review</span>';
    if (v.lane==='changes'||pendingChanges(v)) return '<span class="meta">Changes requested · revision progress not recorded</span>';
    if (['approved','done'].includes(v.lane)) return '<span class="meta">UAT handoff complete</span>';
    if ((v.youtube||{}).state==='scheduled') return '<span class="meta">Scheduled · milestone history retained</span>';
    if (unconfirmedCut(v)) return '<span class="meta">Cut progress unconfirmed · related project work tracked separately</span>';
    const p = progressStats(v);
    return `<div class="milestone-mini" aria-label="${p.percent}% milestone completion; ${p.done} of 9 complete"><div class="track"><i style="width:${p.percent}%"></i></div><span>${p.percent}% <span class="muted">· ${p.done} of 9 milestones complete</span></span></div>`;
  }
  function recordedTime(value) {
    const at=Date.parse(value || '');
    return Number.isFinite(at) ? new Date(at).toLocaleString('en-GB',{timeZone:'Europe/London',day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}) + ' London' : String(value || '');
  }
  function technicalFields(value) {
    if (value == null || value === '') return '';
    if (typeof value !== 'object') return `<span>${esc(value)}</span>`;
    return `<dl class="tech-fields">${Object.entries(value).filter(([,x]) => x != null && x !== '').map(([key,x]) => `<div><dt>${esc(key)}</dt><dd>${technicalFields(x)}</dd></div>`).join('')}</dl>`;
  }
  function stageExplanation(v,m) {
    const rows=milestones(v), own=new Set((m.jobs||[]).map(j=>j.id));
    const linked=[...(v.jobs||[]),...(m.jobs||[])].filter((j,i,all)=>j.id&&all.findIndex(x=>x.id===j.id)===i&&(own.has(j.id)||j.stage===m.id));
    const live=linked.filter(j=>['claimed','open','blocked'].includes(j.status));
    const job=live.find(j=>j.status==='claimed')||live.find(j=>j.status==='blocked')||live[0];
    const missing=(m.displayState||m.state||'unknown')==='unknown'&&!m.awaitingApproval;
    const deps=(m.dependsOn||[]).map(id=>rows.find(x=>x.id===id)).filter(Boolean);
    const unfinished=deps.filter(x=>!completeStage(x)), confirmed=unfinished.filter(x=>stageView(x).text!=='Unconfirmed');
    const scheduled=(v.youtube||{}).state==='scheduled', published=isLive(v);
    let why,action,owner;
    if(job) {
      const state=(((board||{}).workflow||{}).states||{})[job.id]||{};
      const prerequisite=((((board||{}).owb||{}).jobStates||{})[job.after]||{}).status||'state not recorded';
      why=job.status==='claimed'?'A linked job is claimed; recorded activity is available below.':state.reason||(job.hold||{}).condition|| (job.after?`Linked prerequisite ${job.after}: ${prerequisite}. This job has not been claimed.`:'A linked job is queued; its start time is not recorded.');
      action=job.remaining_action||job.title||'Check the linked job for the next recorded action.';
      owner=job.by ? (AGENTS[job.by]||job.by) : 'The linked job has not been claimed.';
    } else if(missing&&(scheduled||published)) {
      why=scheduled?`This video is already scheduled${v.youtube.publishAtLondon?' for '+v.youtube.publishAtLondon:''}. Its ${m.label} decision is missing from the milestone records.`:`This video is already on YouTube. Its historical ${m.label} decision is missing from the milestone records.`;
      action='Reconcile the approval record for this version; this missing record alone is not a reason to restart production.';
      owner=m.id==='qa'?'Chief owns QA decisions; no stage-specific review job is recorded.':'No stage-specific job is recorded.';
    } else if(confirmed.length) {
      why='Recorded prerequisites are unfinished: '+confirmed.map(x=>`${x.label} (${stageView(x).text})`).join(', ')+'.';
      action='Complete or resolve those prerequisites, then record the handoff to this stage.';
      owner='No stage-specific job is recorded; Chief needs to confirm the next owner.';
    } else if(unfinished.length) {
      why='Prerequisite records need confirmation: '+unfinished.map(x=>x.label).join(', ')+'. No linked job establishes whether this stage is waiting or underway.';
      action='Chief needs to reconcile the prerequisite evidence and record the next action and owner.';
      owner='No stage-specific job is recorded.';
    } else {
      why=`${m.label} has no recorded ${m.id==='qa'?'review decision':'stage update'} or linked active job. The records do not establish why it has not moved.`;
      action=m.id==='qa'?'Chief needs to verify whether this version has already passed QA; otherwise queue its review with an eligible reviewer.':'Chief needs to confirm the stage state and queue the next action with an owner.';
      owner=m.id==='qa'?'Chief owns QA decisions; an individual reviewer has not been recorded.':'No stage-specific job is recorded.';
    }
    if(!job&&m.owner) owner='Recorded stage owner: '+(AGENTS[m.owner]||m.owner)+'. No stage-specific active job is recorded.';
    return {missing,why,action,owner,job};
  }
  function stageExplanationHtml(v,m) {
    const c=stageExplanation(v,m);
    return `<div class="next-action stage-explanation"><span>What is happening</span><p>${esc(c.why)}</p><span>Next action</span><p>${esc(c.action)}</p><span>Responsibility</span><p>${esc(c.owner)}</p>${c.job?`<a class="other-stage" href="${jobRoute(c.job.id)}">Open job ${esc(c.job.id)} →</a>`:''}</div>`;
  }
  function milestoneCard(v, m, current) {
    const state = stageView(m), context=stageExplanation(v,m), displayStatus=context.missing?(m.id==='qa'?'QA decision not recorded':'Stage update not recorded'):state.text, saved = expandedStages.get(v.key), open = saved ? saved.has(m.id) : m.id === current;
    const jobs = m.jobs || [], source = m.source || {};
    const times = [['Started',recordedTime(source.startedAt || source.since)],['Completed',recordedTime(source.completedAt)],['Duration',source.durationSeconds ? durationText(source.durationSeconds/60) : '']].filter(([,value])=>value);
    return `<details class="milestone-card ${state.tone}" data-stage="${esc(m.id)}" data-video="${esc(v.key)}" ${open?'open':''}>
      <summary aria-label="${esc(m.label)}: ${esc(displayStatus)}"><span class="stage-icon" aria-hidden="true">${state.icon}</span><span class="stage-copy"><b>${esc(m.label)}</b><small>${esc([displayStatus,conciseEvidence(m)].filter(Boolean).join(' · '))}</small></span><span class="expand-icon" aria-hidden="true">⌄</span></summary>
      <div class="stage-expanded"><dl class="stage-facts"><div><dt>Status</dt><dd>${esc(displayStatus)}</dd></div>${m.owner?`<div><dt>Assigned agent</dt><dd>${esc(ownerName(m))}</dd></div>`:''}${times.map(([label,value])=>`<div><dt>${label}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl>
      ${!completeStage(m)?(state.tone==='held' && !isLive(v)?blockerGuide(v,m):stageExplanationHtml(v,m)):''}
      <details class="technical" data-disclosure="${esc(v.key)}-${esc(m.id)}-tech"><summary>View technical details</summary><div class="technical-body">${m.evidence?`<p>${esc(m.evidence)}</p>`:''}${technicalFields(source)}${jobs.map(j=>technicalFields(j)).join('')}${m.sampleCount!=null?`<p>${esc(m.sampleCount)} comparable historical stage samples</p>`:''}</div></details></div></details>`;
  }
  function currentStageCard(v) {
    if (['approved','done'].includes(v.lane) || isLive(v) || forBen([v]).length) return '';
    const stages = currentProduction(v), m = stages[0];
    if (!m) return `<section class="current-stage"><p class="eyebrow">Current stage</p><h2>No current-stage handoff recorded</h2><p class="muted">The records do not identify an active stage. Chief needs to reconcile the production evidence and record the next job and owner.</p></section>`;
    const state = stageView(m);
    return `<section class="current-stage ${state.tone}"><p class="eyebrow">Current stage</p><h2>${esc(m.label)}${m.id==='picture'?' production':''}</h2>${conciseEvidence(m)?`<p>${esc(conciseEvidence(m))}</p>`:''}
      <p class="stage-status"><span class="status-dot ${state.tone}"></span>${esc(state.text)}</p>${state.tone==='held'?`<button type="button" class="stage-more" data-open-stage="${esc(m.id)}" aria-label="More information about ${esc(m.label)}: ${esc(state.text)}">More information <span aria-hidden="true">↓</span></button>`:`<p class="next-action"><span>Next action</span>${esc(nextAction(m))}</p>${m.owner?`<p class="muted">Assigned agent: <strong>${esc(ownerName(m))}</strong></p>`:'<p class="muted">Chief needs to record the next owner.</p>'}`}
      ${stages.length>1?`<details class="other-stages" data-disclosure="${esc(v.key)}-other"><summary>${stages.length-1} other active stage${stages.length>2?'s':''}</summary>${stages.slice(1).map(x=>`<a class="other-stage" href="#stage-${esc(x.id)}">${esc(x.label)} · ${esc(stageView(x).text)}</a>`).join('')}</details>`:''}</section>`;
  }
  function productionDetail(v, now) {
    const published=isLive(v), changes=!published&&(v.lane==='changes'||pendingChanges(v)), ready=!changes&&forBen([v]).length>0;
    const scheduled=(v.youtube||{}).state==='scheduled', approved=['approved','done'].includes(v.lane);
    if(published||changes||ready||scheduled||approved) {
      const title=published?'Published on YouTube':changes?'Changes requested':ready?'Ready for your review':scheduled?'Scheduled on YouTube':'UAT handoff complete';
      const explanation=published?'This video is published. Production progress and UAT forecasts no longer apply.':changes?'Your requested changes need correction and fresh QA before another review. The earlier milestone records do not measure progress on these revisions.':ready?'A finished cut has been handed over for your review. Incomplete historical milestone records do not describe how much of this cut remains to be made.':scheduled?'This video is scheduled. The publication date is separate from production milestone history.':'Your UAT handoff is complete. Delivery and any linked follow-up work are separate from historical milestone coverage.';
      const linked=[...new Map((v.jobs||[]).filter(LIVE).map(j=>[j.id,j])).values()];
      return section(title,null,`<p class="muted">${esc(explanation)}</p>${changes?'<p class="muted">Your timestamped notes are listed below. The records must identify the correction owner and next action.</p>':''}
        ${linked.length?`<div class="next-action"><span>${published?'Post-publication work':'Linked outstanding work'} · ${linked.length} job${linked.length===1?'':'s'}</span><p>${published?'These linked jobs do not make the published video unfinished. A shared job may also cover other videos.':'Job completion and recorded milestone history are separate from your review decision.'}</p>${linked.map(j=>`<a class="other-stage blocker-job-link" href="${jobRoute(j.id)}">${esc(j.id)} · ${esc(clip(j.remaining_action||j.title||'Action not recorded',160))} · ${esc((JOB_WORD[j.status]||['',j.status])[1])}</a>`).join('')}</div>`:''}
        <details class="technical" data-disclosure="${esc(v.key)}-history"><summary>${unconfirmedCut(v)?'Related project history':'Recorded production history'}</summary><p class="muted">Unconfirmed milestones mean historical records are missing, not that the delivered video is unfinished. Source records and approval requirements remain unchanged.</p>${milestones({...v,production:relatedProduction(v)}).map(m=>milestoneCard(v,m,null)).join('')}</details>`);
    }

    if(unconfirmedCut(v)) {
      const history=relatedProduction(v), rows=milestones({...v,production:history}), m=relatedStage(v), count=rows.filter(completeStage).length;
      const action=m?blockerModel(v,m):null;
      return section('Progress for this cut unconfirmed',null,`<p class="muted">The recorded watch cut${v.version?` (${esc(v.version)})`:''} and the related production work share a project record. Its milestone count does not measure completion of this exact cut. UAT readiness has not been confirmed.</p>
        ${m?`<div class="next-action"><span>Related production work · ${esc(m.label)}</span><p>${esc(stageView(m).text)}</p><p>${esc(action.action)}</p></div>`:''}
        <details class="technical" data-disclosure="${esc(v.key)}-project-history"><summary>Related project history · ${count} of 9 recorded milestones</summary><p class="muted">These are project records, not a cut-specific progress percentage. Original states, approvals and evidence are retained.</p>${rows.map(x=>milestoneCard(v,x,null)).join('')}</details>`);
    }
    const p=progressStats(v), f=forecastView(v,now), production=v.production || {}, e=production.eta || {}, current=(currentProduction(v)[0] || {}).id;
    const fresh = Number.isFinite(Date.parse(production.asOf)) && now-Date.parse(production.asOf)>=0 && now-Date.parse(production.asOf)<=QUIET_MIN*MIN;
    const partial = fresh && !['approved','done','ready'].includes(v.lane) ? (production.partialEstimates || []).filter(x=>x.upperMinutes>(now-Date.parse(production.asOf))/MIN) : [];
    return `<section class="progress-hero" aria-label="Production progress and UAT forecast"><div class="progress-head"><p class="eyebrow">Production progress</p><strong class="progress-number">${p.percent}<span>%</span></strong></div><p class="milestone-caption">${p.done} of 9 milestones complete</p><div class="hero-track" role="progressbar" aria-label="Milestone completion, not production time" aria-valuemin="0" aria-valuemax="9" aria-valuenow="${p.done}"><i style="width:${p.percent}%"></i></div>
      <p class="muted progress-note">Milestone completion · not time elapsed${p.unknown?` · ${p.unknown} unconfirmed`:''}</p><div class="forecast-block"><div><span class="eyebrow">Estimated UAT</span><b>${esc(f.value)}</b></div><span class="confidence">${esc(f.confidence)}</span></div><p class="muted">${esc(f.reason)}</p>
      ${partial.length?`<p class="partial-estimate">Stage estimate only: ${esc(partial[0].label)} · ~${durationText(Math.max(0,partial[0].lowerMinutes-(now-Date.parse(production.asOf))/MIN))}–${durationText(partial[0].upperMinutes-(now-Date.parse(production.asOf))/MIN)} remaining · low confidence. Full UAT estimate unavailable.</p>`:''}
      <details class="technical forecast-diagnostics" data-disclosure="${esc(v.key)}-forecast"><summary>How this estimate works</summary><div class="technical-body"><p>${esc(e.basedOn || 'Timing needs comparable completed stages and confirmed dependencies. Task completion does not imply video readiness.')}</p>${e.reasons && e.reasons.length?`<ul>${e.reasons.map(r=>`<li>${esc(r)}</li>`).join('')}</ul>`:''}${e.criticalPath && e.criticalPath.length?`<p>Critical path: ${esc(e.criticalPath.join(' → '))}</p>`:''}<p>Updated: ${esc(production.asOf || 'Not published')}. Publication dates and your watch time are separate from UAT readiness. Confidence is qualitative, not a calibrated probability.</p></div></details></section>
      ${currentStageCard(v)}<section class="milestone-timeline"><h2>Production milestones <span class="n">${p.done}/9</span></h2><div class="stage-strip" aria-hidden="true">${p.rows.map(m=>`<i class="${stageView(m).tone}"></i>`).join('')}</div>${p.rows.map(m=>`<div id="stage-${m.id}">${milestoneCard(v,m,current)}</div>`).join('')}</section>`;
  }
  function videoUpdated(v) {
    const dates=[v.updatedAt,(v.check||{}).at,...milestones(v).flatMap(m=>{const s=m.source||{};return [s.updatedAt,s.completedAt,s.startedAt,s.since,...(m.jobs||[]).map(j=>(j.progress||{}).at)]})];
    // production.asOf is the publisher clock, not a meaningful production update.
    return Math.max(0,...dates.map(d=>Date.parse(d||'')).filter(Number.isFinite));
  }
  const blockedVideo=v=>currentProduction(v).some(m=>stageView(m).tone==='held') || (v.jobs||[]).some(j=>j.status==='blocked');
  function sortVideos(vs, mode, now) {
    return vs.slice().sort((a,b)=>{
      if(mode==='updated') return videoUpdated(b)-videoUpdated(a);
      if(mode==='blocked') return Number(blockedVideo(b))-Number(blockedVideo(a));
      if(mode==='stage') {const ai=MILESTONES.findIndex(([id])=>id===(currentProduction(a)[0]||{}).id),bi=MILESTONES.findIndex(([id])=>id===(currentProduction(b)[0]||{}).id);return (ai<0?99:ai)-(bi<0?99:bi);}
      const af=forecastView(a,now),bf=forecastView(b,now);
      return Number(bf.credible)-Number(af.credible) || (af.credible && bf.credible ? af.minutes-bf.minutes : 0);
    });
  }
  function videoProductionRow(v, now, b) {
    if (isLive(v)) return row(v, "");
    const historyOnly=forBen([v]).length || pendingChanges(v) || ['approved','done','changes'].includes(v.lane) || (v.youtube||{}).state==='scheduled';
    const scoped=unconfirmedCut(v), current=historyOnly?null:scoped?relatedStage(v):currentProduction(v)[0], f=forecastView(v,now);
    const working = videoHasActiveWork(v);
    // Film-level live delta from Overview's progress24h when this cut's parent film moved; never invent cut %s.
    const pct = working ? videoProgressDelta(v, b || board) : null;
    const delta = pct && pct.label && pct.from != null && pct.to != null && pct.from !== pct.to
      ? `<span class="video-live-delta p24-delta${pct.down ? " down" : (pct.grew ? "" : " flat")}">${esc(pct.label)}</span>`
      : "";
    return row(v, `<span class="meta current-label">${scoped?'Related work: ':''}${esc(current?current.label:stage(v))}${blockedVideo(v)?' · <span class="blocked-word">Waiting for a step</span>':''}${working?' · <span class="working-word">Working now</span>':''}</span>${delta}${milestoneProgress(v)}<span class="meta outlook-line">UAT: ${esc(f.value)}</span>`, null, { working });
  }
  // One set of selectors feeds Overview and its linked lists. Jobs never stand in for videos.
  function uniqueVideos(vs) {
    const selected=new Map(), byKey=new Map();
    const score=v=>(isLive(v)?100:0)+(v.lane==='ready' && v.readyFor==='Ben'?20:0)+((v.youtube||{}).videoId?10:0)+(!/:OK:/.test(v.key||'')?2:0)+(v.production?1:0);
    for(const v of vs) if(v.key && (!byKey.has(v.key) || score(v)>score(byKey.get(v.key)))) byKey.set(v.key,v);
    for(const v of byKey.values()) {
      const id=(v.youtube||{}).videoId ? `yt:${v.youtube.videoId}` : v.key;
      if(!id) continue;
      if(!selected.has(id) || score(v)>score(selected.get(id))) selected.set(id,v);
    }
    return [...selected.values()];
  }
  function producingVideos(vs) {
    // Agent production only: To do / In progress / QA / Passed. UAT is Ben's; Backlog and YouTube lanes stay out.
    return uniqueVideos(vs).filter(v => ["todo", "progress", "qa", "passed"].includes(videoLane(v)));
  }
  function londonDay(at) {
    const p=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/London',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(at).map(x=>[x.type,x.value]));
    return `${p.year}-${p.month}-${p.day}`;
  }
  function weekDates(now) {
    const local=new Date(londonDay(now)+'T12:00:00Z');
    local.setUTCDate(local.getUTCDate()-((local.getUTCDay()+6)%7));
    const start=local.toISOString().slice(0,10);
    local.setUTCDate(local.getUTCDate()+7);const end=local.toISOString().slice(0,10);
    local.setUTCDate(local.getUTCDate()+7);return {start,end,nextEnd:local.toISOString().slice(0,10)};
  }
  function scheduledThisWeek(vs, now) {
    const {start,end}=weekDates(now);
    // Include a recorded overdue schedule until YouTube's readback says public; never include a mere air plan.
    const rows=uniqueVideos(vs).filter(v=>!isLive(v) && (v.youtube||{}).state==='scheduled')
      .flatMap(v=>schedule([v],-Infinity)).filter(r=>r.scheduled && !!(r.v.youtube||{}).publishAt);
    return rows.filter(r=>londonDay(r.at)>=start && londonDay(r.at)<end)
      .filter(r=>!/:OK:/.test(r.v.key) || (r.v.youtube||{}).videoId || !rows.some(other=>other!==r && (other.v.youtube||{}).videoId && other.at===r.at && other.v.channel===r.v.channel && other.v.type===r.v.type))
      .sort((a,b)=>a.at-b.at || a.v.key.localeCompare(b.v.key));
  }
  const routeView=()=>new URLSearchParams((location.hash||'').slice(1)).get('view')||'';
  function overviewModel(b, now) {
    const vs=uniqueVideos(((b.tracker||{}).videos)||[]), ready=forBen(vs), producing=producingVideos(vs);
    const jobs=new Map();
    for(const j of [...(((b.owb||{}).jobs)||[]),...vs.flatMap(v=>v.jobs||[])]) if(j.id && !jobs.has(j.id)) jobs.set(j.id,j);
    const all=[...jobs.values()], models=b.models||{};
    const age=(now-Date.parse(models.checkedAt||''))/MIN;
    const fresh=Number.isFinite(age) && age>=0 && age<=QUIET_MIN && models.fresh!==false;
    const workflow=b.workflow||{}, workflowAge=(now-Date.parse(workflow.at||''))/MIN;
    const states=Number.isFinite(workflowAge)&&workflowAge>=0&&workflowAge<=QUIET_MIN ? workflow.states||{} : {};
    for(const active of workflow.active||[]) {
      const id=active.id||active.job;
      if(!id || !['running','starting'].includes((states[id]||{}).state)) continue;
      const index=all.findIndex(j=>j.id===id), recorded=index>=0?all[index]:{};
      const current={...recorded,id,title:recorded.title||active.title,by:active.worker||active.agent||recorded.by,progress:active.progress||recorded.progress,phase:active.phase||active.mode,dispatchStartedAt:active.startedAt,dispatchExpiresAt:active.expiresAt};
      if(index>=0) all[index]=current; else all.push(current);
    }
    const jobState=j=>{const value=(states[j.id]||{}).state;return value==='starting'&&!(Date.parse(j.dispatchExpiresAt||'')>now)?'stalled':value;};
    const running=all.filter(j=>jobState(j)?['running','starting'].includes(jobState(j)):j.status==='claimed'),
      queued=all.filter(j=>jobState(j)?['queued','review'].includes(jobState(j)):j.status==='open'),
      held=all.filter(j=>jobState(j)?['waiting','stalled'].includes(jobState(j)):j.status==='blocked');
    const freshRunning=running.filter(j=>{
      const at=Math.max(...[j.claimedAt,j.dispatchStartedAt,(j.progress||{}).at,(j.last||{}).at].map(d=>Date.parse(d||'')).filter(Number.isFinite));
      return Number.isFinite(at) && now>=at && now-at<=QUIET_MIN*MIN;
    });
    const activeRunning=fresh?running:freshRunning, operationalFresh=fresh || freshRunning.length>0;
    const degraded=!fresh || (models.models||[]).some(m=>['red','amber'].includes(m.status));
    const agents=(models.models||[]).filter(m=>AGENTS[m.id] && !String(m.id).startsWith('macbook'));
    const noCapacity=queued.length>0 && agents.length>0 && agents.every(m=>m.status==='red');
    const startupUnconfirmed=all.some(j=>j.phase==='starting'&&jobState(j)==='stalled');
    const status=!operationalFresh || startupUnconfirmed ? {text:'Attention needed',tone:'red'} : activeRunning.length ? {text:activeRunning.every(j=>j.phase==='starting')?'Starting':degraded?'Running · Limited':'Running',tone:degraded?'amber':'green'}
      : {text:noCapacity || held.length && !queued.length?'Attention needed':'Waiting',tone:noCapacity || held.length && !queued.length?'red':'amber'};
    return {vs,ready,producing,jobs:all,week:scheduledThisWeek(vs,now),fresh:operationalFresh,running:activeRunning,queued,held,status,startupUnconfirmed};
  }
  function featureVideo(b, now) {
    const s=overviewModel(b,now), focus=(((b.owb||{}).focus)||[]).map(x=>String(x).includes(':')?String(x):homeChannel().label+':'+x);
    const rank=v=>{
      const ready=forBen([v]).length>0, blocked=blockedVideo(v), f=forecastView(v,now), p=progressStats(v), active=currentProduction(v);
      const scoped=unconfirmedCut(v), finalQA=!scoped&&(active.some(m=>m.id==='qa') || p.rows.filter(m=>m.id!=='qa').every(completeStage));
      const unresolved=scoped?9:p.rows.filter(m=>!completeStage(m) && (stageView(m).tone==='held' || m.state==='unknown')).length;
      const priority=Number(v.productionPriority ?? v.priority);
      return [ready?0:1,blocked?1:0,f.credible?0:1,f.credible?f.minutes:Infinity,finalQA?0:1,unresolved,
        focus.includes(v.key)?0:1,Number.isFinite(priority)?priority:Infinity,-videoUpdated(v),v.key];
    };
    const candidates=uniqueVideos([...s.ready,...s.producing.filter(v=>videoLane(v)!=='passed')]);
    return candidates.sort((a,b)=>{
      const ar=rank(a),br=rank(b);for(let i=0;i<ar.length;i++){if(ar[i]<br[i])return -1;if(ar[i]>br[i])return 1;}return 0;
    })[0]||null;
  }
  function featuredOutlook(v,now) {
    if(forBen([v]).length) return 'Ready for UAT';
    if(v.lane==='changes'||pendingChanges(v)) return 'Awaiting corrections';
    if(unconfirmedCut(v)) return 'Estimate pending';
    if(blockedVideo(v)) return 'Waiting';
    const f=forecastView(v,now);
    return f.credible ? `Approximately ${durationText(f.minutes)}` : 'Estimate pending';
  }
  function featuredCard(v,now,producingCount=0) {
    if(!v) return `<p class="overview-empty">${producingCount?'UAT handoffs are complete. Approved videos are moving toward publishing.':'No videos are in production right now. Explore the backlog in Videos.'}</p><a class="overview-empty-link" href="#videos">Open Videos <span aria-hidden="true">›</span></a>`;
    const scoped=unconfirmedCut(v), p=progressStats(v), m=scoped?relatedStage(v):currentProduction(v)[0], ready=forBen([v]).length>0, changes=v.lane==='changes'||pendingChanges(v);
    const stageLabel=ready?'Ready for your UAT':changes?'Requested corrections':m ? m.label+(stageView(m).text==='Awaiting approval'?' approval':'') : 'Unconfirmed';
    const action=ready?((v.watch||{}).url?'Use Watch & review below to open this cut.':'Review delivery incomplete: no watch link is recorded.') : changes?'Your notes need correction and fresh QA. Open the video for linked work and responsibility.':m ? stageView(m).tone==='held'?blockerModel(v,m).action:nextAction(m) : 'The next production step has not been confirmed.';
    return `<a class="featured-video" href="${detailLink(v)}" aria-label="Open ${esc(v.title||'video')} production details">
      <div class="featured-heading">${thumb(v)}<div><h3>${esc(v.title||'Untitled video')}</h3><p>${esc(chName(v.channel))} · ${kind(v)}</p></div><span class="chev" aria-hidden="true">›</span></div>
      ${ready?'<p class="featured-count">Finished cut awaiting your review</p>':changes?'<p class="featured-count">Changes requested · revision progress not recorded</p>':scoped?'<div class="featured-progress-heading"><span>Cut progress</span><b>Unconfirmed</b></div><p class="featured-count">Related project milestones do not measure this cut’s completion.</p>':`<div class="featured-progress-heading"><span>Milestones completed</span><b>${p.percent}%</b></div>
      <div class="hero-track" role="progressbar" aria-label="Milestones completed, not production time" aria-valuenow="${p.done}" aria-valuemin="0" aria-valuemax="9"><i style="width:${p.percent}%"></i></div>
      <p class="featured-count">${p.done} of 9 milestones complete${p.unknown?` · ${p.unknown} unconfirmed`:''}</p>`}
      <dl class="featured-facts"><div><dt>${scoped&&!ready?'Related work':'Current stage'}</dt><dd>${esc(stageLabel)}</dd></div><div><dt>Estimated UAT</dt><dd class="${ready?'ready-text':blockedVideo(v)?'held-text':''}">${esc(featuredOutlook(v,now))}</dd></div></dl>
      ${!scoped&&!ready&&!changes&&m&&m.id==='picture'&&m.summary?`<p class="featured-count">${esc(m.summary)}</p>`:''}
      <p class="featured-next"><span>${ready?'Ready for you':blockedVideo(v)?'Needs attention':'Next action'}</span>${esc(action)}</p></a>${ready&&(v.watch||{}).url?`<a class="btn primary" href="${uatLink(v)}">▶ Watch & review ${esc((v.watch||{}).version||v.version||'')}</a>`:''}`;
  }
  function recordedTaskProgress(j) {
    const p=j.progress || {}, step=Number(p.step), of=Number(p.of);
    return p.step!=null && p.of!=null && Number.isInteger(step) && Number.isInteger(of) && of>0 && step>=0 && step<=of ? {step,of} : null;
  }
  const jobRoute=id=>'#agents&job='+encodeURIComponent(id);
  const selectedJob=()=>new URLSearchParams((location.hash||'').slice(1)).get('job')||'';
  function activityVideoContext(b,j) {
    const videos=uniqueVideos(((b.tracker||{}).videos)||[]), keys=new Set();
    const add=job=>{
      for(const key of Array.isArray(job.taskKeys)?job.taskKeys:[]) if(typeof key==='string'&&/^(OWB|HOS):/.test(key)) keys.add(key);
      if(/^\d+$/.test(String(job.film||''))) keys.add(repoLabel(job.repo)+':'+String(job.film).padStart(3,'0'));
      for(const v of videos) if(v.key&&(v.jobs||[]).some(x=>x.id===job.id)) keys.add(v.key);
    };
    add(j);
    const parentId=j.recheck_of||(j.kind==='review'&&/^J\d{4}$/.test(j.ref||'')?j.ref:'');
    if(parentId) {
      const parent=(((b.owb||{}).jobs)||[]).find(x=>x.id===parentId);
      if(parent) add(parent);
    }
    const rows=[...keys].map(key=>({key,video:videos.find(v=>v.key===key)}));
    const label=row=>{
      const channel=chName(row.key.split(':')[0]);
      return row.video?`${row.video.title||row.key} · ${channel} · ${kind(row.video)}`:`${channel} · ${row.key.split(':')[1]} · title not recorded`;
    };
    return rows.length?{label:rows.slice(0,2).map(label).join(' / ')+(rows.length>2?` · +${rows.length-2} more videos`:''),count:rows.length,keys:rows.map(r=>r.key)}
      :{label:'Studio task · no video linked in the job record',count:0,keys:[]};
  }
  function activityCategory(b,j) {
    const text=String(j.title||'')+' '+String(j.remaining_action||'');
    if(/\b(?:dispatcher|frontend|schema|kanban|deployment|rollout|capacity|software|implementation|code patch|checker fix|worker repair|workflow (?:handoff )?(?:fixes?|repair|code))\b/i.test(text)) return {id:'engineering',label:'Engineering'};
    if(/\b(?:analytics|analytical|impressions|reach|CTR|retention|watch time|daily Studio read|collect(?:ed|ing)? metrics|rebuild the tracker|monthly (?:channel )?(?:improvement )?(?:report|review)|weekly .*audit)\b/i.test(text)) return {id:'analytics',label:'Analytics'};
    if(j.recheck_of || /\b(?:verify (?:the )?condition for|orphan-(?:review|blocked))\b/i.test(text)) return {id:'coordination',label:'Coordination'};
    if(activityVideoContext(b,j).count) return {id:'production',label:'Video production'};
    return {id:'operations',label:'Studio operations'};
  }
  function taskEstimate(j,now) {
    if(!j || j.phase==='starting') return null;
    const p=recordedTaskProgress(j), start=Date.parse(j.claimedAt||'');
    return (!p || p.step<p.of) && Number.isFinite(start) && start<=now && (p && p.step>0 && p.step<p.of || Number.isFinite(+j.estMin) && +j.estMin>0)
      ? etaOf({...j,progress:p || {step:0,of:0}},now) : null;
  }
  function activityEvidenceFresh(j,now) {
    return [j.claimedAt,j.dispatchStartedAt,(j.progress||{}).at,(j.last||{}).at].some(t=>{
      const at=Date.parse(t||'');return Number.isFinite(at)&&now>=at&&now-at<=10*MIN;
    }) || Date.parse(j.dispatchStartedAt||'')<=now && Date.parse(j.dispatchExpiresAt||'')>now;
  }
  function nextVideoTask(b,v,now) {
    if(!v || forBen([v]).length || isLive(v) || (v.youtube||{}).state==='scheduled' || unconfirmedCut(v) || ['approved','done'].includes(v.lane)) return null;
    const s=overviewModel(b,now), workflow=b.workflow||{}, fresh=t=>Number.isFinite(Date.parse(t||''))&&now>=Date.parse(t)&&now-Date.parse(t)<=10*MIN;
    const reportFresh=[b.publishedAt,workflow.at,(b.models||{}).checkedAt].some(fresh), dispatchFresh=fresh(workflow.at);
    const m=unconfirmedCut(v)?relatedStage(v):currentProduction(v)[0], stage=id=>({facts:'sources',thumbnails:'thumbs'}[id]||id);
    const all=new Map(s.jobs.map(j=>[j.id,j]));
    for(const j of [...(v.jobs||[]),...((m||{}).jobs||[])]) if(j.id&&!all.has(j.id)) all.set(j.id,j);
    const own=new Set(((m||{}).jobs||[]).map(j=>j.id));
    const linked=[...all.values()].filter(j=>activityVideoContext(b,j).keys.includes(v.key)||own.has(j.id));
    // A Shorts/packaging job is not automatically the next Picture task of a long.
    const relevant=linked.filter(j=>['open','claimed','blocked'].includes(j.status)||s.running.some(a=>a.id===j.id))
      .filter(j=>m ? own.has(j.id)||stage(j.stage)===m.id : activityCategory(b,j).id==='production');
    const running=s.running.find(a=>relevant.some(j=>j.id===a.id)&&activityEvidenceFresh(a,now)), next=dispatchFresh?workflow.next:null;
    const selected=next&&relevant.find(j=>j.id===next.id);
    const j=running||selected||relevant.find(j=>j.status==='blocked')||relevant.find(j=>j.status==='open')||relevant[0];
    if(!j) return {video:v,job:null,status:'Next task not recorded',responsibility:'Chief needs to record the handoff',timing:'Start time unknown',context:'',dispatchNote:''};
    const state=dispatchFresh?(workflow.states||{})[j.id]||{}:{};
    const hold=j.hold||{}, parent=j.after&&all.get(j.after), parentState=(parent||{}).status||((((b.owb||{}).jobStates)||{})[j.after]||{}).status;
    const dependency=j.after&&parentState!=='done';
    const chief=j.kind==='chief'||hold.type==='chief'||(m||{}).reviewer==='chief';
    const reviewWait=chief&&(state.state==='review'||['chief','approval'].includes(hold.type));
    const held=(j.status==='blocked'||state.state==='waiting')&&!reviewWait;
    const uncertainClaim=j.status==='claimed'&&!running;
    let status,timing,responsibility;
    if(running&&reportFresh) {
      status=running.phase==='starting'?'Worker starting · claim pending':'Working on this video';
      timing=running.phase==='starting'?'Launch recorded; task start is not confirmed':'Already started';
      responsibility=AGENTS[running.by]||running.by||'Agent not recorded';
    } else {
      status=j.awaits_ben||hold.type==='ben'?'Waiting for your approval':dependency?'Waiting for a prerequisite':held?'Waiting for '+(hold.type==='credits'?'credit':hold.type==='capability'?'a capable reviewer':'input'):uncertainClaim?'Claim recorded · activity unconfirmed':chief?'Chief decision queued':selected?'Selected next · not yet claimed':'Queued for this video';
      const fc=j.status==='open'&&!dependency&&!held?forecastLine(b,j):'';
      timing=fc?fc:!reportFresh?'Start time unknown · report stale or missing':dependency?(parent?'After '+clip(parent.title||parent.id,90):'Prerequisite status not confirmed'):held?'Start depends on resolving the recorded hold':uncertainClaim?'Task claim exists; live execution is not confirmed':'Start time not confirmed';
      const selectedWorker=selected&&(next.worker||next.agent), chiefName=fresh((b.models||{}).checkedAt)?((b.models||{}).chief||{}).agent:'';
      responsibility=uncertainClaim&&j.by?'Recorded owner · '+(AGENTS[j.by]||j.by):chief?'Chief'+(chiefName?' · '+(AGENTS[chiefName]||chiefName):''):selectedWorker?'Selected worker · '+(AGENTS[selectedWorker]||selectedWorker):j.for?'Eligible worker · '+(AGENTS[j.for]||j.for):'Waiting for an eligible agent';
    }
    const current=s.running.slice().sort((a,b)=>Number(!!b.urgent)-Number(!!a.urgent))[0], e=reportFresh&&current&&activityEvidenceFresh(current,now)?taskEstimate(current,now):null;
    const category=current&&activityCategory(b,current), scope=category&&category.id==='production'?(activityVideoContext(b,current).keys.includes(v.key)?' on this video':' on another video'):'';
    const context=!running&&current&&current.id!==j.id?`Current ${category.label.toLowerCase()} task${scope}${e&&!e.over?' estimates ~'+durationText(e.min)+' remaining':e&&e.over?' has exceeded its estimate':'; remaining time unavailable'}. This does not confirm when this video task starts.`:'';
    const dispatchNote=next&&next.id!==j.id?'Next recorded dispatch: '+activityCategory(b,next).label+'.':'';
    return {video:v,job:j,status,responsibility,timing,context,dispatchNote};
  }
  function nextVideoWorkCard(b,v,now) {
    const p=nextVideoTask(b,v,now);
    if(!p) return '';
    return `<aside class="video-next-work" aria-label="Next work on ${esc(v.title||'this video')}"><a href="${p.job?jobRoute(p.job.id):detailLink(v)}" aria-label="${esc(p.status)}. ${p.job?'Open job '+esc(p.job.id)+' in Agents':'Open video details'}"><div><span>Next work on this video</span><b>${esc(p.status)}</b><small>${esc(p.responsibility)}${p.job?' · '+esc(p.job.id):''}</small></div><span class="chev" aria-hidden="true">›</span></a><p class="video-next-timing">${esc(p.timing)}</p>${p.context?`<p>${esc(p.context)}</p>`:''}${p.dispatchNote?`<p>${esc(p.dispatchNote)}</p>`:''}</aside>`;
  }
  function activityVideoLine(ctx) {
    // One film: show its title. Many films: keep it compact — the job title/action is the headline (Ben, 6 Nov).
    if(!ctx||!ctx.count) return {compact:true, text:(ctx&&ctx.label)||'Studio task · no video linked in the job record'};
    if(ctx.count===1) return {compact:false, text:ctx.label};
    return {compact:true, text:`${ctx.count} videos linked`};
  }
  // Film id + title for Active jobs (Ben, 6 Nov ~23:21) — never hide behind "Video production".
  function activityJobVideoLabel(b,j) {
    const ctx=activityVideoContext(b,j);
    if(!ctx||!ctx.count) return '';
    const videos=uniqueVideos(((b.tracker||{}).videos)||[]);
    const key=ctx.keys[0], video=videos.find(v=>v.key===key);
    const long=(/^([A-Z]+:\d{3})/.exec(key)||[])[1];
    const idLabel=(long||key||'').replace(/:/g,' ');
    if(video&&video.title) return `${idLabel} · ${video.title}`;
    if(ctx.count===1&&ctx.label&&!/title not recorded/i.test(ctx.label)) {
      const title=String(ctx.label).split(' · ')[0];
      return title?`${idLabel} · ${title}`:idLabel;
    }
    return idLabel||ctx.label||'';
  }
  function activityJobCard(b,j,now) {
    const starting=j.phase==='starting', p=starting?null:recordedTaskProgress(j), category=activityCategory(b,j);
    const e=taskEstimate(j,now);
    const eta=starting?'Claim pending':e? (e.over?'Over ETA':`~${durationText(e.min)} ETA`) : '';
    const agent=AGENTS[j.by]||j.by||'Unassigned';
    const steps=p?`${p.step} / ${p.of} steps (${pct(p)}%)`:(starting?'Starting…':'Progress n/a');
    const videoLabel=activityJobVideoLabel(b,j);
    const sub=videoLabel?`${j.id} · ${videoLabel}`:`${j.id} · ${category.label}`;
    // Compact Active jobs row (Ben, 6 Nov ~23:05/23:21) — agent, id · video, steps/ETA, spinning icon, thin bar.
    return `<a class="ov-card active-job-card" href="${jobRoute(j.id)}" aria-label="Open job ${esc(j.id)} in Agents. ${esc(videoLabel||category.label)}">
      <span class="aj-icon" aria-hidden="true"></span>
      <div class="aj-main"><b>${esc(agent)} is ${starting?'starting':'working'}</b><span class="aj-sub">${esc(sub)}</span></div>
      <div class="aj-right"><span class="aj-steps">${esc(steps)}</span>${eta?`<span class="aj-eta">${esc(eta)}</span>`:''}</div>
      ${p?`<div class="aj-bar" role="progressbar" aria-label="Recorded task steps, not video completion" aria-valuemin="0" aria-valuemax="${p.of}" aria-valuenow="${p.step}"><i style="width:${pct(p)}%"></i></div>`:''}
    </a>`;
  }
  function activityCard(b,now) {
    const s=overviewModel(b,now), jobs=s.running.slice().sort((a,b)=>Number(!!b.urgent)-Number(!!a.urgent));
    const head=`<div class="ov-section-head"><h2>Active jobs${jobs.length?` (${jobs.length})`:''}</h2>${jobs.length?`<span class="ov-live"><i aria-hidden="true"></i>Running now</span>`:''}</div>`;
    if(!jobs.length) return `<section class="overview-activity" aria-label="Active jobs">${head}<a class="ov-card aj-empty" href="#agents"><div><b>${s.startupUnconfirmed?'Worker startup could not be confirmed':s.queued.length?'Ready work waiting for dispatch':s.held.length?'No job running · work is waiting':'Studio waiting for next job'}</b>${!s.fresh?'<span>Activity report is stale or missing</span>':''}</div><span class="chev" aria-hidden="true">›</span></a></section>`;
    // One compact card per running agent/job — never a single featured job + "+N others".
    return `<section class="overview-activity" aria-label="Active jobs">${head}<div class="ov-stack activity-stack">${jobs.map(j=>activityJobCard(b,j,now)).join('')}</div></section>`;
  }
  // Last 24 hours (Ben, 4 Nov 2026; film cards 6 Nov 2026): headline counts, then one quiet card per film.
  // Checklist (Ben, 6 Nov 2026): remaining-to-go-live + today green / yesterday gray; display-only. Review owns real ticks.
  // Glance strip (Ben, 6 Nov evening): done today, left, can't run, next four going live — checklist behind a disclosure.
  function p24JobLive(j) {
    const status=j&&j.status, wait=j&&j.waitKind;
    if(wait==='after') return 'after earlier work';
    if(wait==='blocker'||status==='blocked') return 'needs something';
    if(!status||status==='done'||status==='todo') return '';
    if(status==='claimed') return 'in progress';
    return status;
  }
  function p24JobMark(j) {
    const status=j&&j.status, when=j&&j.when, wait=j&&j.waitKind;
    if(status==='done'&&when==='yesterday') return {cls:'is-done-yesterday', label:'Done yesterday'};
    if(!status||status==='done') return {cls:'is-done', label:'Done today'};
    if(status==='claimed'&&wait!=='after') return {cls:'is-progress', label:'In progress'};
    if(wait==='after') return {cls:'is-waiting', label:'Waiting on earlier work'};
    if(wait==='blocker'||status==='blocked') return {cls:'is-waiting', label:'Needs something first'};
    return {cls:'is-open', label:'Open'};
  }
  function p24JobLine(j) {
    const mark=p24JobMark(j);
    const stage=j.stage&&j.kind!=='stage'?`<span class="p24-job-stage">${esc(j.stage)}</span>`:'';
    const prog=j.progress&&j.progress.of?`<span class="p24-job-prog">${j.progress.step||0} of ${j.progress.of}</span>`:'';
    const liveLabel=p24JobLive(j);
    const live=liveLabel?`<span class="p24-job-live">${esc(liveLabel)}</span>`:'';
    const why=j.why?`<span class="p24-job-why wrap">${esc(j.why)}</span>`:'';
    const id=j.id?`<b>${esc(j.id)}</b> `:'';
    const aria=`${mark.label}: ${[j.id,j.title,j.why].filter(Boolean).join(' ')}`.trim();
    // In-progress rows get a spinner so the expanded checklist names the live job (Ben, 6 Nov ~23:21).
    const markEl=mark.cls==='is-progress'
      ?`<span class="p24-job-spinner" role="img" aria-label="In progress"></span>`
      :`<span class="p24-check" aria-hidden="true"></span>`;
    return `<li class="p24-job ${mark.cls}${j.kind==='stage'?' is-stage':''}${j.waitKind?' is-'+esc(j.waitKind):''}" data-job-state="${esc(mark.cls.replace(/^is-/,''))}" aria-label="${esc(aria)}">
      ${markEl}
      <span class="p24-job-main">${id}<span class="p24-title wrap">${esc(j.title||'')}</span>${why}</span>${stage}${prog}${live}
    </li>`;
  }
  function p24MovedStatus(m) {
    if(m.milestones<0) return `↺ reopened · ${m.from}% → ${m.to}%`;
    return `${m.from}% → ${m.to}%`;
  }
  // Live boards may still have the older films[] shape (count + last, no items/status). Always merge moved[].
  function p24MergeFilms(films, moved) {
    const by=new Map();
    for(const f of films||[]){
      const key=f.film||f.key; if(!key) continue;
      by.set(key,{...f,film:key});
    }
    for(const m of moved||[]){
      if(!m.key) continue;
      const status=p24MovedStatus(m), closed=m.milestones>0;
      const cur=by.get(m.key);
      if(cur){
        by.set(m.key,{...cur,from:m.from,to:m.to,milestones:m.milestones,closed,status,title:cur.title||m.title});
      }else{
        by.set(m.key,{film:m.key,title:m.title,from:m.from,to:m.to,milestones:m.milestones,closed,status,items:[],jobs:0,last:''});
      }
    }
    return [...by.values()];
  }
  // Overview film cards follow studio focus (queue → board.owb.focus). Empty focus = no filter.
  function p24FocusSet(b) {
    const raw=((b&&b.owb)||{}).focus||[];
    const home=(typeof homeChannel==='function'&&homeChannel().label)||'OWB';
    const set=new Set();
    for(const x of raw){
      const s=String(x||'').trim(); if(!s) continue;
      set.add(s);
      if(/^\d{3}$/.test(s)) set.add(home+':'+s);
      const m=/^([A-Za-z]+):(\d{3})$/.exec(s);
      if(m){ set.add(m[1].toUpperCase()+':'+m[2]); set.add(m[2]); }
    }
    return set;
  }
  function p24InFocus(film, focus) {
    if(!focus||!focus.size) return true;
    const key=String(film||'');
    if(focus.has(key)) return true;
    const m=/^([A-Z]+):(\d{3})$/.exec(key);
    return !!(m&&(focus.has(m[2])||focus.has(m[1]+':'+m[2])));
  }
  // Can't-run that Ben himself must clear (UAT/watch, money, login/device). Pipeline "after" waits,
  // parked-for-Chief, and Chief: leftovers are studio work — not Needs attention (Ben, 6 Nov ~23:20).
  function p24NeedsBenAttention(j) {
    if(!j || j.kind==='stage' || j.status==='done' || j.status==='todo') return false;
    if(j.waitKind==='after') return false;
    const title=String(j.title||'');
    const hold=j.hold||{};
    const holdType=String(hold.type||'').toLowerCase();
    const why=String(j.why||'');
    const blob=[title, why, j.result, hold.condition, j.remaining_action].filter(Boolean).join(' ');
    if(j.awaits_ben || j.needs==='ben' || holdType==='ben') return true;
    if(/\bNeeds Ben\b/i.test(why) || /\bNeeds Ben\b/i.test(blob)) return true;
    if(/\bwaiting for (?:ben|you)(?:\s+to)?\b|\bben to (?:watch|uat|review|ok|approve)\b|\bfor (?:your|ben(?:'s)?) (?:watch|uat|review|approval)\b|\bready for (?:your )?(?:uat|watch|review)\b/i.test(blob)) return true;
    if(/\b(?:top-?ups?|buy credits|real money|enable (?:paid )?overage|charge (?:the )?card|spend(?:ing)? money)\b/i.test(blob)) return true;
    if(/\b(?:google )?password\b|\b2fa\b|\bsign[- ]?in\b|\bhis (?:voice|device|phone|login)\b|\bonly ben can\b/i.test(blob)) return true;
    if(String(j.kind||'').toLowerCase()==='chief' || /^Chief:/i.test(title)) return false;
    if(/parked for Chief/i.test(blob)) return false;
    if(/\bWill run automatically after\b/i.test(why||blob)) return false;
    return false;
  }
  function p24IsCantRunItem(j) {
    if(!j || j.kind==='stage' || j.status==='done') return false;
    return !!(j.waitKind || j.status==='blocked' || (j.after&&j.status!=='done')
      || j.awaits_ben || j.needs==='ben' || ((j.hold||{}).type&&String(j.hold.type).toLowerCase()==='ben'));
  }
  function p24FilmCounts(f, items) {
    const list=items!==undefined?items:(f.items||[]);
    const useItems=items!==undefined||!!(f.items&&f.items.length);
    const doneToday=useItems
      ? list.filter(j=>j&&j.status==='done'&&j.when==='today').length
      : (f.doneToday!=null?f.doneToday:0);
    const left=useItems
      ? list.filter(j=>j&&j.status!=='done').length
      : (f.left!=null?f.left:0);
    // Ben-facing can't-run only — server `blocked` still includes after/Chief waits.
    const blocked=list.filter(j=>p24IsCantRunItem(j)&&p24NeedsBenAttention(j)).length;
    return {doneToday, left, blocked};
  }
  function p24FilmLabel(film) {
    const key=String(film||'');
    const short=/^([A-Z]+):(\d{3}):S:/i.exec(key);
    if(short) return `${short[1].toUpperCase()} ${short[2]} Short`;
    const long=/^([A-Z]+):(\d{3})$/i.exec(key);
    if(long) return `${long[1].toUpperCase()} ${long[2]}`;
    return key.replace(/:/g,' ');
  }
  function p24FilmMatchesJob(filmKey, b, j) {
    if(!j||!filmKey) return false;
    const keys=(activityVideoContext(b,j).keys)||[];
    if(keys.includes(filmKey)) return true;
    const focus=new Set([filmKey]);
    if(keys.some(k=>k===filmKey||p24InFocus(k, focus))) return true;
    if(/^\d+$/.test(String(j.film||''))){
      const home=(typeof repoLabel==='function'?repoLabel(j.repo):'OWB')+':'+String(j.film).padStart(3,'0');
      if(home===filmKey||String(filmKey).startsWith(home+':')||String(filmKey)===home) return true;
    }
    return false;
  }
  function p24JobFromTracker(j) {
    if(!j) return null;
    return {
      id:j.id, title:j.title||j.remaining_action||'', status:j.status||'open',
      stage:j.stage||'', progress:j.progress||null, when:j.when,
      why:j.why, waitKind:j.waitKind, after:j.after, afterChain:j.afterChain,
      recheck_of:j.recheck_of, ref:j.ref, awaits_ben:j.awaits_ben,
      needs:j.needs, hold:j.hold, kind:j.kind,
    };
  }
  function p24NormJobId(id) {
    const m=/\b(J\d{3,5})\b/i.exec(String(id||''));
    return m?m[1].toUpperCase():'';
  }
  // Jobs that must finish before this one (appear above it): after / afterChain / "will run after JX".
  function p24JobDependsOn(j) {
    const out=[];
    const add=id=>{ const n=p24NormJobId(id); if(n&&!out.includes(n)) out.push(n); };
    const after=j&&j.after;
    if(Array.isArray(after)) after.forEach(add);
    else if(after) add(after);
    for(const p of (j&&j.afterChain)||[]){
      if(p&&typeof p==='object') add(p.id);
      else add(p);
    }
    const blob=[j&&j.why, j&&j.title].filter(Boolean).join(' ');
    // "Will run automatically after J2089 (…)" / "after J2141 and J2142"
    const chunk=/\bafter\s+([^.;\n]+)/i.exec(blob);
    if(chunk) for(const m of chunk[1].matchAll(/\b(J\d{3,5})\b/gi)) add(m[1]);
    return out;
  }
  // Jobs this one unblocks (this job appears above them): recheck_of / "Verify condition for JX".
  function p24JobPrecedesTargets(j) {
    const out=[];
    const add=id=>{ const n=p24NormJobId(id); if(n&&!out.includes(n)) out.push(n); };
    if(j&&j.recheck_of) add(j.recheck_of);
    const title=String((j&&j.title)||'');
    const m=/Verify(?:\s+the)?\s+condition\s+for\s+(J\d{3,5})/i.exec(title);
    if(m) add(m[1]);
    if(j&&j.kind==='review'&&/^J\d{3,5}$/i.test(String(j.ref||''))) add(j.ref);
    return out;
  }
  function p24ItemRank(j) {
    const cls=p24JobMark(j).cls;
    if(cls==='is-progress') return 0;
    if(cls==='is-open') return 1;
    if(cls==='is-waiting') return 2;
    if(cls==='is-done') return 3;
    if(cls==='is-done-yesterday') return 4;
    return 2;
  }
  // Top-to-bottom = run / hierarchy order, not raw job-id order (Ben, 6–7 Nov 2026).
  // A before B; "Verify condition for JX" above JX; waiting-after jobs stay visible below their named earlier jobs.
  function p24SortFilmItems(items) {
    const list=(items||[]).filter(Boolean);
    const stages=list.filter(j=>j.kind==='stage'||!j.id);
    const nodes=list.filter(j=>j.id&&j.kind!=='stage');
    const byId=new Map(nodes.map(j=>[String(j.id).toUpperCase(), j]));
    const ids=[...byId.keys()];
    const succ=new Map(ids.map(i=>[i, []]));
    const indeg=new Map(ids.map(i=>[i, 0]));
    const addEdge=(a,b)=>{
      a=String(a).toUpperCase(); b=String(b).toUpperCase();
      if(!byId.has(a)||!byId.has(b)||a===b) return;
      if((succ.get(a)||[]).includes(b)) return;
      succ.get(a).push(b);
      indeg.set(b,(indeg.get(b)||0)+1);
    };
    for(const j of nodes){
      const id=String(j.id).toUpperCase();
      for(const dep of p24JobDependsOn(j)) addEdge(dep, id);
      for(const tgt of p24JobPrecedesTargets(j)) addEdge(id, tgt);
    }
    const indexOf=new Map(nodes.map((j,i)=>[String(j.id).toUpperCase(), i]));
    const cmp=(a,b)=>p24ItemRank(byId.get(a))-p24ItemRank(byId.get(b))||indexOf.get(a)-indexOf.get(b);
    const ready=ids.filter(i=>(indeg.get(i)||0)===0).sort(cmp);
    const out=[], seen=new Set();
    while(ready.length){
      const i=ready.shift();
      if(seen.has(i)) continue;
      seen.add(i);
      out.push(byId.get(i));
      for(const s of succ.get(i)||[]){
        indeg.set(s,(indeg.get(s)||0)-1);
        if(indeg.get(s)===0){ ready.push(s); ready.sort(cmp); }
      }
    }
    for(const j of nodes){
      if(!seen.has(String(j.id).toUpperCase())) out.push(j);
    }
    return out.concat(stages);
  }
  // When progress24h items are empty on a pulsing film, fill from tracker + claimed owb jobs (Ben, 6 Nov ~23:33).
  function p24HydrateFilmItems(f, b) {
    const filmKey=String((f&&f.film)||'');
    const byId=new Map();
    const add=j=>{
      if(!j) return;
      const id=j.id?String(j.id):`__anon_${byId.size}`;
      const cur=byId.get(id);
      if(!cur) byId.set(id, j);
      else if(j.status==='claimed'&&cur.status!=='claimed') byId.set(id, {...cur, ...j, status:'claimed'});
    };
    for(const j of (f&&f.items)||[]) add(j);
    if(b&&filmKey){
      for(const v of uniqueVideos((((b.tracker)||{}).videos)||[])){
        if(v.key!==filmKey) continue;
        for(const j of v.jobs||[]) add(p24JobFromTracker(j));
      }
      for(const j of (((b.owb)||{}).jobs)||[]){
        if(!j||j.status!=='claimed') continue;
        if(!p24FilmMatchesJob(filmKey, b, j)) continue;
        add({id:j.id, title:j.title||j.remaining_action||'', status:'claimed', stage:j.stage||'',
          progress:j.progress||null, recheck_of:j.recheck_of, ref:j.ref, after:j.after, kind:j.kind});
      }
    }
    return p24SortFilmItems([...byId.values()]);
  }
  function p24BlockedWhy(f) {
    if(f.blockedWhy) return f.blockedWhy;
    const items=f.items||[];
    const wait=items.find(j=>j.waitKind==='after')||items.find(j=>j.waitKind||j.status==='blocked'||(j.after&&j.status!=='done'));
    return (wait&&wait.why)||'';
  }
  // True only when a job for this film is claimed / in progress (Ben, 6 Nov ~22:58).
  // Open, waiting, and "will run after …" do not count.
  function p24FilmHasActiveWork(f, b) {
    const items=f.items||[];
    if(items.some(j=>j&&j.kind!=='stage'&&p24JobMark(j).cls==='is-progress')) return true;
    if(!b) return false;
    const filmKey=String(f.film||'');
    if(!filmKey) return false;
    const focus=new Set([filmKey]);
    for(const v of ((b.tracker||{}).videos)||[]){
      if(!(v.key===filmKey||p24InFocus(v.key, focus))) continue;
      if((v.jobs||[]).some(j=>j&&j.status==='claimed')) return true;
    }
    for(const j of (((b.owb)||{}).jobs)||[]){
      if(!j||j.status!=='claimed') continue;
      const keys=(activityVideoContext(b,j).keys)||[];
      if(keys.some(k=>k===filmKey||p24InFocus(k, focus))) return true;
    }
    return false;
  }
  function p24FilmPct(f) {
    const from=f.from!=null?+f.from:null, to=f.to!=null?+f.to:(f.pct!=null?+f.pct:null);
    const grew=from!=null&&to!=null&&to>from;
    const down=from!=null&&to!=null&&to<from;
    let label='';
    if(from!=null&&to!=null&&from!==to) label=`${from}% → ${to}%`;
    else if(to!=null) label=`${to}%`;
    else if(f.status&&/\d+%/.test(f.status)&&!/worked on, no stage closed/i.test(f.status)) label=String(f.status).replace(/^↺ reopened · /,'');
    const bar=to!=null?Math.max(0,Math.min(100,to)):(from!=null?Math.max(0,Math.min(100,from)):0);
    return {from, to, grew, down, label, bar};
  }
  function p24FilmCard(f, b) {
    const items=p24HydrateFilmItems(f, b);
    const name=p24FilmLabel(f.film);
    const closed=f.closed||(f.milestones!=null&&f.milestones>0);
    const active=p24FilmHasActiveWork({...f, items}, b);
    const counts=p24FilmCounts(f, items);
    const pctInfo=p24FilmPct(f);
    const stages=((f.pctReason||'').split('·')[0]||'').trim()
      ||(f.doneCount!=null?`${f.doneCount} of ${f.total||9} stages`:'');
    const meta=[stages, `Done ${counts.doneToday}`, `Left ${counts.left}`, `Can't run ${counts.blocked}`].filter(Boolean).join(' · ');
    const deltaCls=pctInfo.down?' down':(pctInfo.grew?'':' flat');
    const delta=pctInfo.label||(closed?'':'—');
    const jobs=items.map(p24JobLine).join('')
      ||(f.last?`<li class="p24-job is-open" data-job-state="open" aria-label="Open: ${esc(f.last)}"><span class="p24-check" aria-hidden="true"></span><span class="p24-job-main"><span class="p24-title wrap">${esc(f.last)}</span></span></li>`:'');
    const earlier=f.earlierDone>0?`<p class="muted p24-earlier">${f.earlierDone} earlier job${f.earlierDone===1?'':'s'} already done</p>`:'';
    const n=items.length||(f.last?1:0)||(active&&jobs?1:0);
    const cls=`ov-card p24-film-card${active?' is-working':''}${pctInfo.grew?' is-grew':''}${!pctInfo.grew?' is-flat':''}`;
    const dot=active?`<span class="p24-working-dot" role="img" aria-label="A job is in progress on this film"></span>`:'';
    // Compact resting row (id, title, %, bar, one-line meta). Tap/expand opens the jobs checklist (Ben, 6 Nov ~23:07).
    const compact=`${dot}
      <div class="p24-film-top">
        <div class="p24-film-left"><b class="p24-film">${esc(name)}</b><p class="p24-film-title">${esc(f.title||'')}</p></div>
        <div class="p24-film-right"><span class="p24-delta${deltaCls}">${esc(delta)}</span>
          <div class="p24-film-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pctInfo.bar}" aria-label="Film stage progress ${pctInfo.bar}%"><i style="width:${pctInfo.bar}%"></i></div>
        </div>
      </div>
      <p class="p24-film-meta">${esc(meta)}</p>`;
    // Pulsing rows must always expand — never a bare article while work is in progress (Ben, 6 Nov ~23:33).
    if(!jobs && !active) return `<article class="${cls}">${compact}</article>`;
    const list=jobs||`<li class="p24-job is-progress" data-job-state="progress" aria-label="In progress"><span class="p24-job-spinner" role="img" aria-label="In progress"></span><span class="p24-job-main"><span class="p24-title wrap">Job in progress</span></span></li>`;
    return `<details class="${cls} p24-check-fold" aria-label="Jobs checklist (${n||1})">
      <summary class="p24-film-summary">${compact}<span class="p24-film-expand" aria-hidden="true">›</span></summary>
      <ul class="p24-job-list" role="list">${list}</ul>${earlier}
    </details>`;
  }
  function p24FocusFilms(b) {
    const p=b&&b.progress24h; if(!p) return [];
    return p24MergeFilms(p.films,p.moved).filter(f=>p24InFocus(f.film, p24FocusSet(b)));
  }
  // Keys for films that currently have claimed / in-progress work (live board + checklist).
  function p24ActiveFilmKeys(b) {
    const keys=new Set();
    const add=k=>{
      if(!k) return;
      keys.add(k);
      const m=/^([A-Z]+:\d{3})/.exec(String(k));
      if(m) keys.add(m[1]);
    };
    const p=b&&b.progress24h;
    for(const f of p24MergeFilms((p&&p.films)||[],(p&&p.moved)||[])){
      if(p24FilmHasActiveWork(f, b)) add(f.film);
    }
    for(const j of (((b&&b.owb)||{}).jobs)||[]){
      if(!j||j.status!=='claimed') continue;
      for(const k of (activityVideoContext(b,j).keys)||[]) add(k);
    }
    for(const v of (((b&&b.tracker)||{}).videos)||[]){
      if((v.jobs||[]).some(j=>j&&j.status==='claimed')) add(v.key);
    }
    return keys;
  }
  // Focus films first, then any film with claimed work even outside focus (Ben, 6 Nov ~23:21).
  // Does not dump every film that merely had recent work.
  function p24WorkingFilms(b) {
    const p=b&&b.progress24h; if(!p) return [];
    const focus=p24FocusSet(b);
    const merged=p24MergeFilms(p.films,p.moved);
    const by=new Map(merged.map(f=>[f.film,f]));
    const out=[], seen=new Set();
    for(const f of merged){
      if(focus.size&&!p24InFocus(f.film, focus)) continue;
      out.push(f); seen.add(f.film);
    }
    const videos=uniqueVideos((((b.tracker)||{}).videos)||[]);
    for(const key of p24ActiveFilmKeys(b)){
      if(seen.has(key)) continue;
      // Keep both the long and the Short when both are active — do not drop one (Ben, 6 Nov ~23:33).
      if(by.has(key)){ out.push(by.get(key)); seen.add(key); continue; }
      const video=videos.find(v=>v.key===key);
      if(!video) continue;
      const claimed=(video.jobs||[]).filter(j=>j&&j.status==='claimed').map(j=>({
        id:j.id, title:j.title||j.remaining_action||'', status:'claimed', stage:j.stage||'',
        progress:j.progress||null,
      }));
      out.push({film:key, title:video.title||'', items:claimed, doneToday:0, left:claimed.length, blocked:0, jobs:claimed.length});
      seen.add(key);
    }
    return out;
  }
  function p24BenBlockedJobs(p, films) {
    const g=(p&&p.glance)||{};
    const list=films||[];
    const filmKeys=new Set(list.map(f=>f.film).filter(Boolean));
    const fromGlance=(g.blockedJobs||[])
      .filter(j=>!filmKeys.size||filmKeys.has(j.film)||p24InFocus(j.film, filmKeys))
      .filter(p24NeedsBenAttention);
    if(fromGlance.length) return fromGlance;
    const out=[];
    for(const f of list){
      for(const j of f.items||[]){
        if(!(p24IsCantRunItem(j)&&p24NeedsBenAttention(j))) continue;
        out.push({id:j.id||'', film:f.film, title:j.title||'', status:j.status||'blocked', waitKind:j.waitKind, why:j.why||''});
      }
    }
    return out;
  }
  function p24GlanceCounts(p, films) {
    const list=films||p.films||[];
    // Prefer counts from the cards on screen so focus filtering never leaves glance inflated.
    const doneToday=list.reduce((n,f)=>n+(p24FilmCounts(f).doneToday||0),0);
    const left=list.reduce((n,f)=>n+(p24FilmCounts(f).left||0),0);
    const blockedJobs=p24BenBlockedJobs(p, list);
    const blockedFromFilms=list.reduce((n,f)=>n+(p24FilmCounts(f).blocked||0),0);
    const blocked=blockedFromFilms||blockedJobs.length;
    return {doneToday, left, blocked, blockedJobs};
  }
  // Last 24h headlines only — can't-run detail lives in Needs attention (Ben, 6 Nov ~23:05).
  function p24Glance(p, films) {
    const {doneToday, left, blocked}=p24GlanceCounts(p, films);
    return `<div class="ov-card p24-glance" aria-label="Studio glance">
      <div class="p24-glance-stats"><div><b>${doneToday}</b><span>Done today</span></div><div><b>${left}</b><span>Left to go live</span></div><div><b>${blocked}</b><span>Can't run yet</span></div></div>
    </div>`;
  }
  function needsAttentionBanner(b) {
    const p=b&&b.progress24h; if(!p) return '';
    const films=p24WorkingFilms(b);
    const {blockedJobs}=p24GlanceCounts(p, films);
    if(!blockedJobs.length) return '';
    const n=blockedJobs.length;
    const list=blockedJobs.map(j=>{
      const line=j.why||j.title||'';
      return `<li><b>${esc(j.id||'')}</b> <span class="p24-title wrap">${esc(line)}</span></li>`;
    }).join('');
    return `<details class="overview-attention" aria-label="Needs attention">
      <summary><span class="att-icon" aria-hidden="true"></span><span class="att-copy"><b>Needs attention</b><span>${n} job${n===1?'':'s'} can't run yet</span></span><span class="att-chev" aria-hidden="true">›</span></summary>
      <ul class="p24-glance-list att-list">${list}</ul>
    </details>`;
  }
  // Next publishes helper kept for tests / Schedule; not shown on Overview home.
  function p24NextLive(p) {
    const next=((p&&p.glance)||{}).nextLive||[];
    const rows=next.slice(0,4);
    if(!rows.length) return '';
    return `<section class="overview-next-live" aria-label="Next to go live"><h2>Next to go live</h2><div class="ov-card p24-next"><ol class="p24-next-list">${rows.map(v=>{
      const when=v.atLondon||v.at||'';
      return `<li><span class="p24-next-when">${esc(when)}</span><span class="p24-title wrap">${esc(v.title||'')}</span></li>`;
    }).join('')}</ol></div></section>`;
  }
  function workingOnNowBody(b) {
    const p=b.progress24h; if(!p) return '';
    const focus=p24FocusSet(b);
    const films=p24WorkingFilms(b);
    const filmCards=films.map(f=>p24FilmCard(f, b)).join('');
    const base=focus.size?'Working on now':'Videos that had work';
    const filmsH=films.length?`${base} (${films.length})`:base;
    if(!filmCards) return {h:filmsH, n:0, html:`<p class="muted p24-note">No video work in this window${p.hours?'':' yet (first reading)'}.</p>`};
    return {h:filmsH, n:films.length, html:`<div class="ov-stack p24-films">${filmCards}</div>`};
  }
  function workingOnNow(b) {
    const body=workingOnNowBody(b); if(!body) return '';
    return `<section class="overview-p24 overview-working" aria-label="Working on now"><div class="ov-section-head"><h2>${body.h}</h2></div>${body.html}</section>`;
  }
  function p24TotalsBody(b) {
    const p=b.progress24h; if(!p) return '';
    const studio=(p.studio||[]).map(p24JobLine).join('');
    const studioN=p.otherJobs!=null?p.otherJobs:(p.studio||[]).length;
    return `<div class="ov-card p24-head">
      <div class="p24-stats"><div><b>${p.videoJobs!=null?p.videoJobs:(p.jobsDone||0)}</b><span>Video jobs finished</span></div><div><b>${p.milestones||0}</b><span>Milestones done</span></div><div><b>${(p.moved||[]).filter(m=>m.milestones>0).length}</b><span>Videos moved forward</span></div></div>
      ${p.videoJobs!=null?`<p class="muted p24-agents${p.jobsDone&&p.videoJobs/p.jobsDone<0.3?' p24-warn':''}">${p.videoJobs} of ${p.jobsDone||0} jobs were on videos (${p.jobsDone?Math.round(p.videoJobs/p.jobsDone*100):0}%); the rest kept the studio running.</p>`:''}
      </div>
      ${studio||studioN?`<details class="p24-more p24-studio"><summary>Studio-wide (${studioN||(p.studio||[]).length} job${(studioN||(p.studio||[]).length)===1?'':'s'})</summary><ul class="p24-job-list" role="list">${studio||`<li class="muted">No job titles recorded.</li>`}</ul></details>`:''}`;
  }
  function p24Totals(b) {
    const body=p24TotalsBody(b); if(!body) return '';
    return `<section class="overview-p24 overview-p24-stats" aria-label="Studio totals"><div class="ov-section-head"><h2>Studio totals</h2></div>${body}</section>`;
  }
  // Composed for tests; Overview home restacks the pieces itself (Ben, 6 Nov ~23:05).
  function progressCard(b) {
    const p=b.progress24h; if(!p) return '';
    const films=p24WorkingFilms(b);
    const work=workingOnNowBody(b);
    return `<section class="overview-p24" aria-label="Progress in the last 24 hours"><h2>Last 24 hours</h2>
      ${p24Glance(p, films)}
      ${work?`<h3 class="p24-films-h">${work.h}</h3>${work.html}`:''}
      ${p24TotalsBody(b)}
    </section>`;
  }
  // Machines (Ben, 4 Nov 2026): what the Mini and the MacBook are on now, and jobs each finished in 24 h.
  // Queue forecast (Ben, 5 Nov 2026: "waiting for this particular agent to be free, number 4 in the queue ... a time").
  // Overview tidy (Ben, 6 Nov 2026): drop per-machine By splits / Agents here / min-per-job / idle empty agent rows;
  // show last-seen only when stale (~30+ min); wrap queue clear times; plain-English unavailable reasons.
  const SEEN_STALE_MIN = 30;
  function qWhen(t) {
    const d=Date.parse(t); if(!d) return '';
    const day=x=>new Date(x).toLocaleDateString('en-GB',{timeZone:'Europe/London',weekday:'long'});
    const hm=new Date(d).toLocaleTimeString('en-GB',{timeZone:'Europe/London',hour:'2-digit',minute:'2-digit'});
    return (day(d)===day(Date.now())?'':day(d)+' ')+hm;
  }
  function plainWhy(why) {
    const s=String(why||'').trim();
    if(!s) return 'down';
    let m=s.match(/no Claude run for (\d+)\s*min/i);
    if(m){
      const min=+m[1];
      if(min<60) return `last run about ${min} min ago`;
      const h=Math.round(min/60);
      return `last run about ${h} hour${h===1?'':'s'} ago`;
    }
    m=s.match(/no heartbeat from MacBook slot (\d+) in (\d+)\s*min/i);
    if(m) return `MacBook ${m[1]} hasn't checked in for about ${m[2]} min`;
    m=s.match(/no MacBook heartbeat in (\d+)\s*min/i);
    if(m) return `MacBook hasn't checked in for about ${m[1]} min`;
    m=s.match(/no heartbeat yet/i);
    if(m) return 'no check-in yet';
    // Strip heartbeat internals; keep the human meaning.
    return s.replace(/\s*\([^)]*heartbeat[^)]*\)/gi,'').replace(/\bheartbeat\b/gi,'check-in').replace(/\s{2,}/g,' ').trim()||'down';
  }
  function forecastLine(b, j) {
    const q=(b&&b.queueForecast)||{}, f=j&&(q.jobs||{})[j.id];
    if(f) return `Next for ${AGENTS[f.agent]||f.agent} · #${f.pos} in line · starts about ${qWhen(f.startAt)}`;
    const why=j&&(q.noAgent||{})[j.id];
    return why?why.charAt(0).toUpperCase()+why.slice(1):'';
  }
  // Compact agent rows (still used by tests / detail views). Overview home no longer lists Agents (Agents tab).
  function agentLines(b) {
    const q=(b&&b.queueForecast)||{};
    // Busy, queued, or unavailable only — hide idle agents with nothing waiting.
    const rows=(q.agents||[]).filter(a=>!a.up||a.now||a.queued).map(a=>{
      const name=AGENTS[a.agent]||a.agent;
      if(!a.up) return `<li><span class="p24-film">${esc(name)}</span> <span class="p24-title wrap muted">Not available · ${esc(plainWhy(a.why))}</span></li>`;
      const on=a.now?`on ${esc(a.now)} · free about ${esc(qWhen(a.freeAt))}`:'free now';
      const line=a.queued?` · ${a.queued} in line, clear about ${esc(qWhen(a.clearAt))}`:'';
      return `<li><span class="p24-film">${esc(name)}</span> <span class="p24-title wrap">${on}${line}</span></li>`;
    }).join('');
    return rows?`<section class="overview-agents" aria-label="Agents and their lines"><h2>Agents and their lines</h2><div class="ov-card mc-agents"><ul class="p24-list mc-agent-list">${rows}</ul>${q.note?`<p class="muted p24-note">${esc(q.note)}</p>`:''}</div></section>`:'';
  }
  // Traffic light: green = working, amber = waiting/available, red = idle / down / blocked (Ben, 6 Nov ~22:14).
  function machineTraffic(r) {
    const n=(r.now||[]).length;
    const st=String(r.state||'').toLowerCase();
    if(n>0||st==='running'||st==='working') return {light:'green', word:'Working', count:n||1};
    if(st==='error'||st==='down') return {light:'red', word:'Down', count:0};
    if(st==='busy'||st==='waiting') return {light:'amber', word:'Waiting', count:0};
    // Up with nothing on it → idle (red). Available-with-queue is rare on machines; keep amber for explicit waiting.
    return {light:'red', word:'Idle', count:0};
  }
  function agentTraffic(a, modelStatus) {
    const ms=(modelStatus&&modelStatus[a.agent])||{};
    if(!a.up||ms.status==='red') return {light:'red', word:'Down'};
    if(a.now) return {light:'green', word:'Working'};
    if((a.queued||0)>0) return {light:'amber', word:'Waiting'};
    return {light:'red', word:'Idle'};
  }
  const MACHINE_ORDER=[
    {id:'mini', short:'Mini', name:'Mac mini'},
    {id:'macbook', short:'MacBook', name:'MacBook Pro'},
    {id:'cloud', short:'Claude', name:'Claude (cloud)'},
    {id:'grok', short:'Grok', name:'Grok box'},
  ];
  function liveMachineRow(r, now) {
    if(r.id!=='macbook'||!macbook||!(Date.parse(macbook.at)>Date.parse(r.seen||0))) return r;
    const why=Array.isArray(macbook.why)?macbook.why.join('; '):(macbook.why||'');
    const now2=(r.now||[]).length||!macbook.job?r.now:[{id:macbook.job,title:'',agent:'macbook'}];
    return {...r,state:macbook.state||r.state,why,seen:macbook.at,agents:macbook.agents||r.agents,now:now2};
  }
  // Four compact traffic-light chips: "1 on · 41 done" / "Idle · 0 done" (Ben, 6 Nov ~23:05).
  function machinesCard(b, now) {
    const m=b.machines;
    const byId=Object.fromEntries(((m&&m.machines)||[]).map(r=>[r.id, liveMachineRow(r, now)]));
    const chips=MACHINE_ORDER.map(meta=>{
      const r=byId[meta.id]||{id:meta.id, name:meta.name, now:[], done24:0, state:''};
      const t=machineTraffic(r);
      const working=t.count>0?`${t.count} on`:`${t.word}`;
      const caption=`${working} · ${r.done24||0} done`;
      return `<a class="ov-card mc-chip light-${t.light}" href="#agents" aria-label="${esc(meta.name)}: ${t.word}">
        <i class="mc-light" aria-hidden="true"></i>
        <b class="mc-short">${esc(meta.short)}</b>
        <span class="mc-chip-state">${esc(caption)}</span>
      </a>`;
    }).join('');
    return `<section class="overview-machines" aria-label="Machines"><div class="ov-section-head"><h2>Machines</h2><span class="ov-count">${MACHINE_ORDER.length} total</span></div><div class="mc-row">${chips}</div></section>`;
  }
  // Kept for tests / reuse; Overview home no longer renders Agents (Agents tab owns that).
  function agentsCards(b) {
    const q=(b&&b.queueForecast)||{};
    const modelStatus=Object.fromEntries((((b.models)||{}).models||[]).map(x=>[x.id,x]));
    const rows=q.agents||[];
    if(!rows.length) return '';
    const chips=rows.map(a=>{
      const name=AGENTS[a.agent]||a.agent;
      const t=agentTraffic(a, modelStatus);
      const detail=a.now?esc(a.now):(a.queued?`${a.queued} waiting`:t.word);
      return `<div class="ov-card mc-chip ag-chip light-${t.light}" aria-label="${esc(name)}: ${t.word}">
        <i class="mc-light" aria-hidden="true"></i>
        <b class="mc-short">${esc(name)}</b>
        <span class="mc-chip-state">${detail}</span>
      </div>`;
    }).join('');
    return `<section class="overview-agents" aria-label="Agents"><h2>Agents</h2><div class="mc-row mc-row-wrap">${chips}</div></section>`;
  }
  function last24Section(b) {
    const p=b.progress24h; if(!p) return '';
    return `<section class="overview-p24 overview-last24" aria-label="Last 24 hours"><div class="ov-section-head"><h2>Last 24 hours</h2></div>${p24Glance(p, p24WorkingFilms(b))}</section>`;
  }
  // Cleaner dashboard (Ben, 6 Nov ~23:05): Header → stats → Needs attention → Machines →
  // Active jobs → Working on now → Last 24h → Totals. No Agents / Next live / feature card.
  function overview(b, now) {
    const s=overviewModel(b,now);
    return `<div class="overview-home"><header class="overview-header"><div><h1>Studio</h1><p>Orbit With Ben · History of Science</p></div><a class="operation-status ${s.status.tone}" href="#agents" aria-label="Studio status: ${s.status.text}. Open Agents"><i aria-hidden="true"></i>${s.status.text}</a></header>
      <div class="seg" aria-label="Studio video counts"><a href="#review"><b>${s.ready.length}</b><span>To review</span></a><a href="#videos&view=producing"><b>${s.producing.length}</b><span>Producing</span></a><a href="#schedule&view=week"><b>${s.week.length}</b><span>This week</span></a></div>
      ${needsAttentionBanner(b)}
      ${machinesCard(b,now)}
      ${activityCard(b,now)}
      ${workingOnNow(b)}
      ${last24Section(b)}
      ${p24Totals(b)}</div>`;
  }

  // Nine exclusive Videos swim lanes (Ben, 7 Nov 2026). Only UAT needs Ben; UAT OK → Passed, notes → In progress.
  function videoGroups(vs) {
    const g = Object.fromEntries(VIDEO_LANE_ORDER.map(id => [id, []]));
    for (const v of vs) {
      const lane = videoLane(v);
      if (lane && g[lane]) g[lane].push(v);
    }
    return g;
  }

  function videos(b) {
    const vs = (routeView()==='producing' ? producingVideos(((b.tracker||{}).videos)||[]) : uniqueVideos(((b.tracker||{}).videos)||[])).filter(v =>
      (filterCh === "all" || v.channel === filterCh) && (filterType === "all" || v.type === filterType));
    const g = videoGroups(vs);
    for (const key of Object.keys(g)) g[key] = sortVideos(g[key], videoSort, Date.now());
    // Studio-only jobs (no video card) still count under In progress, matching Overview.
    const studio = routeView()!=='producing' && filterType === "all" ? studioJobs(b).filter(j => filterCh === "all" || (j.repo || "owb") === filterCh.toLowerCase()) : [];
    g.progress.extra = studio.length;
    // Nine equal count chips in locked order (3×3). No "All" tile — tap the active lane again to clear.
    const segs = VIDEO_LANE_CHIPS
      .map(([id, label]) => {
        const n = g[id].length + (g[id].extra || 0);
        return `<button type="button" data-seg="${id}" class="${seg === id ? "on" : ""}" aria-pressed="${seg === id ? "true" : "false"}"><b>${n}</b><span>${esc(label)}</span></button>`;
      }).join("");
    const chs = channelList();
    const chips = [["ch", "all", chs.length === 2 ? "Both" : "All"], ...chs.map(c => ["ch", c.label, c.short || c.label]),
                   ["ty", "long", "Longs"], ["ty", "short", "Shorts"]]
      .map(([k, val, label]) => `<button type="button" data-f="${k}" data-v="${val}" class="${(k === "ch" ? filterCh : filterType) === val ? "on" : ""}">${label}</button>`).join("");
    const list = (items, limit) => items.slice(0, limit).map(v => videoProductionRow(v, Date.now(), b)).join("")
      + (items.length > limit ? `<p class="meta">${items.length - limit} more: pick Orbit or HOS, Longs or Shorts to narrow the list.</p>` : "");
    // A batch job on several videos: the first card carries the job, the others say whose job they share.
    const jobList = items => jobGroups(items).map(([first, ...rest]) => videoProductionRow(first, Date.now(), b)
      + rest.map(v => videoProductionRow(v, Date.now(), b)).join('')).join('');
    // In progress: claimed/working-now first, then waiting — never bury live work under UAT sort (Ben, 7 Nov 2026).
    const progressBody = (items) => {
      const { working, waiting } = partitionProgressVideos(items);
      const workingN = working.length + studio.length;
      const parts = [];
      if (workingN) {
        parts.push(`<h3 class="lane-sub">Working now <span class="n">${workingN}</span></h3>`);
        parts.push(jobList(working));
        parts.push(studio.map(jobCard).join(""));
      }
      if (waiting.length) {
        parts.push(`<h3 class="lane-sub">Waiting <span class="n">${waiting.length}</span></h3>`);
        parts.push(`<p class="meta lane-sub-blurb">Queued, blocked, or waiting for a step — still In progress, not live work.</p>`);
        parts.push(jobList(waiting));
      }
      return parts.join("") || empty("Nothing in progress.");
    };
    const show = id => routeView()==='producing' || seg === "all" || seg === id;
    const limitFor = id => (seg === id ? 60 : (id === "todo" || id === "progress" || id === "qa" || id === "uat" || id === "passed" ? 30 : 10));
    const laneSection = (id) => {
      if (!show(id)) return "";
      // Producing view hides YouTube / backlog noise.
      if (routeView() === "producing" && ["backlog", "scheduled", "live", "postlive", "uat"].includes(id)) return "";
      const copy = VIDEO_LANE_COPY[id] || { title: id, blurb: "" };
      const items = g[id] || [];
      const count = items.length + (items.extra || 0);
      const blurb = items.length || (id === "progress" && studio.length) ? `<p class="meta">${esc(copy.blurb)}</p>` : "";
      let body = "";
      if (id === "progress") body = progressBody(items);
      else if (id === "uat") body = (items.map(v => `<div class="rcard">${row(v, `<span class="tag amber">Needs your review</span>`, uatLink(v))}<a class="btn watch" href="${uatLink(v)}">▶ Watch & review ${esc((v.watch || {}).version || v.version || "")}</a></div>`).join("")) || empty("Nothing waiting for your watch.");
      else body = list(items, limitFor(id)) || empty(id === "backlog" ? "Backlog is empty." : "Nothing here.");
      // Collapsible lane sections (open when selected or when viewing all).
      const open = seg === "all" || seg === id ? " open" : "";
      return `<details class="lane-fold"${open}><summary>${esc(copy.title)} <span class="n">${count}</span></summary>${blurb}${body}</details>`;
    };
    return `<header class="top"><h1>Videos</h1></header>
      <p class="meta">Only UAT needs you. Pass a cut → Passed (ready to schedule). Leave notes → In progress for the agents.</p>
      ${routeView()==='producing'?`<p class="list-scope">Producing · ${vs.length} unique videos <a href="#videos">Show all</a></p>`:''}
      <div class="seg">${segs}</div><div class="chips">${chips}</div>
      <label class="sort-control">Sort videos<select id="video-sort"><option value="uat" ${videoSort==='uat'?'selected':''}>Nearest credible UAT</option><option value="updated" ${videoSort==='updated'?'selected':''}>Recently updated</option><option value="stage" ${videoSort==='stage'?'selected':''}>Production stage</option><option value="blocked" ${videoSort==='blocked'?'selected':''}>Waiting first</option></select></label>
      ${VIDEO_LANE_ORDER.map(laneSection).join("")}`;
  }

  // One video, in the hub: where it is, who is on it, what is left, your notes, and its links.
  // Ben, 5 Nov 2026: "the work block is telling me it's a hard stop ... it should not be blocked, we have all the tools".
  // A held job is waiting for something specific, so the page says what, never "Blocked".
  function waitWord(j) {
    const h=(j&&j.hold)||{}, t=String(h.type||''), r=String((j&&j.result)||'')+' '+String(h.condition||'');
    if (j && j.awaits_ben) return 'Waiting for Ben';
    if (t==='public') return 'Starts when the film goes public';
    if (t==='date') return 'Scheduled';
    if (t==='test') return 'Waiting for a YouTube test';
    if (t==='credits') return 'Waiting for credits';
    if (/parked for Chief|Chief review|for Chief/i.test(r) || (j&&j.kind==='chief')) return 'Waiting for review';
    if (t==='dependency' || (j&&j.after)) return 'Waiting for an earlier job';
    return 'Waiting';
  }
  const JOB_WORD = { claimed: ["green", "Working"], open: ["", "Queued"], blocked: ["amber", "Waiting"], done: ["", "Done"] };
  function detail(b, key) {
    const v = ((((b.tracker || {}).videos) || []).find(x => x.key === key));
    const back = `<header class="top"><a class="more back" href="#videos">‹ Back to Videos</a></header>`;
    if (!v) return back + empty("That video isn't on the board any more.");
    const yt = v.youtube || {}, w = v.watch || {};
    const links = [
      forBen([v]).length ? `<a class="btn primary" href="${uatLink(v)}">▶ Watch & review</a>` : w.url ? `<a class="btn" href="${esc(w.url)}" target="_blank" rel="noopener">▶ Watch ${esc(w.version || v.version || "")}</a>` : "",
      yt.url ? `<a class="btn" href="${esc(yt.url)}" target="_blank" rel="noopener">Open on YouTube</a>` : "",
    ].filter(Boolean);
    const jobs = [...new Map((v.jobs || []).map(j=>[j.id,j])).values()].sort((a, b) => ["claimed", "open", "blocked", "done"].indexOf(a.status) - ["claimed", "open", "blocked", "done"].indexOf(b.status));
    const jobRows = jobs.map(j => { const [tone, w0] = JOB_WORD[j.status] || ["", j.status]; const word = j.status === "blocked" ? waitWord(j) : w0;
      const why = j.status === "blocked" ? (j.hold && j.hold.condition) || j.result : j.status === "open" && forecastLine(b, j) || j.remaining_action;
      return `<div class="job"><div class="job-top"><span class="tag ${tone}">${word}</span><b>${esc(clip(j.title || j.id, 90))}</b></div>
        <span class="meta">${esc(j.id)}${j.by ? " · " + esc(AGENTS[j.by] || j.by) : ""}${why ? " · " + esc(clip(why, 160)) : ""}</span>
        ${j.status === "claimed" ? (j.progress && j.progress.of > 0 ? bar(j.progress, etaText(etaOf(j, Date.now()))) : `<span class="meta">${esc(etaText(etaOf(j, Date.now())))}</span>`) : ""}</div>`; }).join("");
    const notes = (v.notes || []).map(n => `<li class="${n.done ? "done" : ""}">${n.t ? `<b>${esc(n.t)}</b> ` : ""}${esc(n.text)}</li>`).join("");
    const flags = (v.flags || []).map(f => `<span class="tag amber">⚠ ${esc(clip(f.text, 120))}</span>`).join("");
    return `${back}<div class="video-heading">${thumb(v)}<div><h1 class="uat-title">${esc(v.title)}</h1>
      <p class="meta">${esc(chName(v.channel))} · ${kind(v)} ${esc(v.number || "")}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}${v.airText ? " · " + (yt.state === "live" && yt.privacy === "public" ? "published " : "airs ") + esc(v.airText) : ""}</p>
      </div></div>
      ${links.length ? `<div class="btns">${links.join("")}</div>` : ""}
      ${productionDetail(v, Date.now())}
      <details class="technical video-technical" data-disclosure="${esc(v.key)}-jobs"><summary>Agent work &amp; technical details <span>${jobs.length} jobs</span></summary><div class="technical-body">${v.line?`<p>${esc(v.line)}</p>`:''}${flags}${jobRows}${jobs.map(j=>technicalFields(j)).join('')}</div></details>
      ${notes ? section("Your notes", null, `<ul class="notes">${notes}</ul>`) : ""}`;
  }

  function review(b) {
    const vs = uniqueVideos(((b.tracker || {}).videos) || []);
    const needList = forBen(vs);
    const need = needList.map(v => `<div class="rcard">${row(v, `<span class="tag amber">Needs your review</span>`, uatLink(v))}
      <a class="btn watch" href="${uatLink(v)}">▶ Watch & review ${esc((v.watch || {}).version || v.version || "")}</a></div>`).join("");
    const checked = vs.map(v => (sent[v.checkId] || {}).key === v.key ? Object.assign({}, v, { check: sent[v.checkId] }) : v);
    const reviewed = checked.filter(v => v.check && v.check.at).sort((a, b) => Date.parse(b.check.at) - Date.parse(a.check.at));
    const done = reviewed.slice(0, 8)
      .map(v => row(v, `<span class="tag ${v.check.verdict === "ok" ? "green" : "amber"}">${v.check.verdict === "ok" ? "You OK'd" : "You asked for changes"} ${esc(v.check.version || "")}</span>`)).join("");
    // Two equal summary chips. Not filters — pending stays above; reviewed can collapse but starts open.
    const chips = `<div class="seg two" aria-label="Review counts"><div><b>${needList.length}</b><span>Needs your review</span></div><div><b>${reviewed.length}</b><span>Reviewed</span></div></div>`;
    return `<header class="top"><h1>Review</h1></header><p class="meta">Finished videos only. Everything else is the agents' job.</p>
      ${chips}
      ${section("Needs your review", needList.length, need || empty("Nothing to watch right now. You'll get a message when there is."))}
      <details class="reviewed-fold" open><summary>Reviewed <span class="n">${reviewed.length}</span></summary>${done || empty("No reviews yet.")}</details>`;
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
        <p class="meta">Approve moves it to Passed (ready to schedule). Request changes sends your notes to In progress — agents pick them up; it does not stay in UAT.</p>`
      : `<p class="line">This Short is reviewed with its long film: your OK or changes there cover it.</p>`;
    return `<header class="top"><a class="more back" href="#review">‹ Review</a></header>
      <h1 class="uat-title">${esc(v.title)}</h1><p class="meta">${ch(v)} · ${kind(v)} · ${esc(w.version || v.version || "")}${v.airText ? " · airs " + esc(v.airText) : ""} · your watch</p>
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

  function agentQueue(b,now) {
    const s=overviewModel(b,now), jobs=s.jobs.filter(j=>['claimed','open','blocked'].includes(j.status)).sort((a,b)=>['claimed','open','blocked'].indexOf(a.status)-['claimed','open','blocked'].indexOf(b.status));
    return `<details class="technical video-technical" data-disclosure="agent-queue" ${selectedJob()?'open':''}><summary>Job queue · ${jobs.length} job${jobs.length===1?'':'s'}</summary><div class="technical-body">${jobs.length?jobs.map(j=>`<article id="job-${esc(j.id)}" class="job ${selectedJob()===j.id?'selected-job':''}" tabindex="-1"><b>${esc(j.id)} · ${esc(j.title || 'Untitled job')}</b><p>Recorded status: ${esc(j.status)}${j.by?' · '+esc(AGENTS[j.by]||j.by):''}</p>${j.remaining_action?`<p>${esc(j.remaining_action)}</p>`:''}${technicalFields(j.hold)}${j.result?`<p>${esc(j.result)}</p>`:''}<details class="technical"><summary>Recorded job metadata</summary>${technicalFields(j)}</details></article>`).join(''):'No queued or active jobs recorded.'}</div></details>`;
  }

  function agents(b, now) {
    const m = b.models || {}, jobs = ((b.owb || {}).jobs) || [], c = m.chief || {}, s = summary(b, now);
    const status = Object.fromEntries((m.models || []).map(x => [x.id, x]));
    // Working first, then idle, then unavailable (red). Content of each row is unchanged.
    const rank = { green: 0, amber: 1, red: 2 };
    const teamRows = Object.entries(AGENTS).map(([id, name]) => {
      const mine = jobs.filter(j => j.by === id && j.status === "claimed");
      const chain = (m.chiefChain || []).find(r => r.agent === id) || {};
      let why = mine.length ? "Working on " + mine.map(j => `${j.id}: ${j.title}`).join(" · ")
        : (status[id] || {}).why || chain.why || (id === "macbook" ? "waits for a MacBook job, plugged in and idle" : "no job right now");
      let [st, word] = agentLight(id, mine.length, (status[id] || {}).status, c.agent === id && m.fresh !== false);
      if (id === "macbook" && !mine.length) { const mbs = macbookState(macbook, now); st = mbs[0]; word = mbs[1]; why = mbs[2]; }
      const href = mine[0] ? jobRoute(mine[0].id) : "#agents";
      return { st, html: `<a class="row agent" href="${href}"><span class="dot ${esc(st)}"></span><div class="body"><b>${esc(name)} <span class="tag ${st}">${word}</span>${c.agent === id ? ' <span class="tag">Chief</span>' : ""}</b>
        <span class="meta">${esc(clip(why, 110))}</span></div><span class="chev">›</span></a>` };
    }).sort((a, b) => (rank[a.st] ?? 9) - (rank[b.st] ?? 9));
    const team = teamRows.map(r => r.html).join("");
    const pools = (b.credits || {}).pools || {};
    // Every model gets a bar where a real reading exists (Ben, 29 Oct: "accurate progress for all the models").
    // Grok Bot has no meter of its own: it runs on the same weekly pool as Cursor (the Mini reads it from
    // grok.com/dashboard/billing), so its tile shows that reading. Claude and Gemini show one once the Mini records it.
    const chain = Object.fromEntries((m.chiefChain || []).map(r => [r.agent, r]));
    const tile = (name, id, alias) => {
      const pm = poolMeter(id, pools[id], (b.credits || {}), now);
      if (!pm) {
        const [tone, word, note] = meterless(chain[alias], status[alias], now);
        return `<a class="credit" href="/ai"><span>${esc(name)}</span><b class="${tone}">${word}</b><small>${esc(note)}</small></a>`;
      }
      return `<a class="credit" href="/ai"><span>${esc(name)}</span><b class="${pm.tone}">${pm.fig}</b>${pm.share != null
        ? `<div class="bar"><i class="${pm.tone}" style="width:${Math.max(3, pm.share * 100).toFixed(0)}%"></i></div>` : ""}<small>${esc(pm.note)}</small></a>`;
    };
    const credit = [["ElevenLabs", "elevenlabs"], ["Flow", "flow"], ["Vertex", "vertex"], ["Codex", "codex"], ["Cursor", "cursor"],
      ["Grok", "cursor", "chief"], ["Claude", "claude", "claude"], ["Gemini", "gemini", "gemini"]]
      .filter(([, id, alias]) => pools[id] || alias).map(([name, id, alias]) => tile(name, id, alias)).join("");
    return `<header class="top"><h1>Agents</h1><a class="more" href="/ai">Details ›</a></header>
      <p class="meta">AI agents, their status, and usage credits.</p>
      ${jobTiles(s.jobs)}
      <div class="chief-card"><span class="dot ${c.agent ? "green" : "red"}"></span><div class="body"><b>Chief: ${esc(c.name || "nobody")} <span class="tag ${c.agent ? "green" : "red"}">${c.agent ? "Coordinating" : "Down"}</span></b>
        <span class="meta">${c.agent ? "Online · coordinating production" : "No Chief up: jobs wait"}</span></div></div>
      ${section("Agent team", Object.keys(AGENTS).length, team + '<p class="meta">Green: working now. Amber: online but idle, or not checked in lately. Red: out of usage or failing; its jobs go to the next agent.</p>')}
      ${agentQueue(b,now)}
      ${section("Credits", null, `<div class="credits">${credit}</div>`, ' <a class="more" href="/ai">See all</a>')}`;
  }

  // A pool's reading as a bar: its own total, else 100 for a %, else the current plan's allowance (credits.tiers),
  // else for a monthly £ credit the highest reading this calendar month (the refill).
  function poolMeter(id, pool, credits, now) {
    if (!pool || !pool.latest) return null;
    const lt = pool.latest, unit = pool.unit;
    let total = lt.total || (unit === "%" ? 100 : null), of = "";
    const tier = ((credits.tiers || {})[id] || []).find(t => t.current);
    if (!total && tier) { total = tier.allow; of = `of ${Number(total).toLocaleString("en-GB")} (${tier.name.replace(/^Google /, "")})`; }
    if (!total && unit === "GBP") {
      const month = new Date(now).toISOString().slice(0, 7);
      const vals = (pool.series || []).filter(p => String(p[0]).slice(0, 7) === month && p[1] != null).map(p => p[1]);
      total = vals.length ? Math.max(...vals, lt.left) : null;
      if (total) of = `of £${Number(total).toFixed(0)} this month`;
    }
    const share = total && lt.left != null ? Math.max(0, Math.min(1, lt.left / total)) : null;
    const stale = (now - Date.parse(lt.at || "")) / 36e5 > 30;
    const tone = share != null && share < 0.1 ? "red" : stale ? "amber" : "green";
    const fig = share != null ? Math.round(share * 100) + "%" : unit === "GBP" ? "£" + Number(lt.left).toFixed(0) : Number(lt.left || 0).toLocaleString("en-GB");
    const reset = (String(lt.note || "").match(/resets? (?:on )?([A-Z][a-z]{2} \d{2} [A-Z][a-z]{2} [\d:]+Z?|[A-Z][a-z]{2} \d{1,2})/) || [])[1];
    const left = unit === "GBP" ? `£${Number(lt.left).toFixed(2)} left` : unit === "%" ? "" : `${Number(lt.left).toLocaleString("en-GB")} left`;
    const note = stale ? "reading stale" : [left, of, reset ? "resets " + reset.trim() : ""].filter(Boolean).join(" · ");
    return { share, fig, tone, note };
  }
  function meterless(row, st, now) {
    row = row || {}; st = st || {};
    const until = Date.parse(row.until || st.until || "");
    const back = until > now ? "back " + new Date(until).toLocaleString("en-GB", {weekday: "short", hour: "2-digit", minute: "2-digit", timeZone: "Europe/London"}) : "";
    const up = row.agent ? row.up : st.status === "green";
    if (!row.agent && !st.id) return ["amber", "—", "no reading"];
    return up ? ["green", "Up", "no meter published"] : ["red", "Out", back || "out of usage"];
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
    const vs=uniqueVideos(((b.tracker||{}).videos)||[]);
    const rows = schedule(vs, now), actualWeek=scheduledThisWeek(vs,now), bounds=weekDates(now);
    const day = at => new Date(at).toLocaleDateString("en-GB", { timeZone: "Europe/London", weekday: "long", day: "numeric", month: "short" });
    const time = at => new Date(at).toLocaleTimeString("en-GB", { timeZone: "Europe/London", hour: "2-digit", minute: "2-digit" });
    const item = r => { const warn = readiness(r.v, r.at, now);
      return row(r.v, `<span class="meta when">${esc(time(r.at))}${r.scheduled ? "" : " · planned date"}</span>${warn ? `<span class="tag amber">⚠ ${esc(clip(warn, 80))}</span>` : ""}`); };
    const byDay = list => { let out = "", last = "";
      for (const r of list) { const d = day(r.at); if (d !== last) { out += `<h3 class="day">${esc(d)}</h3>`; last = d; } out += item(r); }
      return out; };
    const planned=rows.filter(r=>!r.scheduled && londonDay(r.at)>=bounds.start && londonDay(r.at)<bounds.end);
    const next=rows.filter(r=>londonDay(r.at)>=bounds.end && londonDay(r.at)<bounds.nextEnd);
    const later=rows.filter(r=>londonDay(r.at)>=bounds.nextEnd);
    // Three matching summary chips (Videos/Review/Agents language). Not filters — week lists stay stacked below.
    // "Scheduled" = confirmed YouTube publishAt only; planned dates stay labelled in the list.
    const confirmed = rows.filter(r => r.scheduled).length;
    const chips = `<div class="seg" aria-label="Schedule counts"><div><b>${actualWeek.length}</b><span>This week</span></div><div><b>${next.length}</b><span>Next week</span></div><div><b>${confirmed}</b><span>Scheduled</span></div></div>`;
    // Always show This week then Next week (and Later). view=week is a deep-link only — never hides a week list.
    return `<header class="top"><h1>Schedule</h1></header><p class="meta">Calendar weeks · Monday–Sunday · London time</p>
      ${chips}
      ${section("This week · scheduled",actualWeek.length,byDay(actualWeek)||empty("Nothing scheduled this week."))}
      ${planned.length?section("This week · planned",planned.length,byDay(planned)):''}
      ${section("Next week",next.length,byDay(next)||empty("Nothing yet."))}
      ${section("Later",later.length,byDay(later.slice(0,12))||empty("Nothing yet."))}`;
  }

  function renderTab(tab, b, now) {
    if (!b || !b.tracker) return '<p class="empty">Loading the studio…</p>';
    return ({ overview, videos, review, agents, schedule: scheduleTab }[tab] || overview)(b, now);
  }

  function current() {
    const t = (location.hash || "").replace("#", "");
    if (t.startsWith("uat=")) return "review";
    if (t.startsWith("v=")) return "videos";
    const tab=t.split("&")[0];
    return TABS.some(([id]) => id === tab) ? tab : "overview";
  }
  const uatKey = () => { const m = (location.hash || "").match(/^#uat=(.+)$/); return m ? decodeURIComponent(m[1]) : ""; };
  const videoKey = () => { const m = (location.hash || "").match(/^#v=(.+)$/); return m ? decodeURIComponent(m[1]) : ""; };

  function render() {
    document.querySelectorAll('details[data-disclosure]').forEach(el => disclosureState.set(el.dataset.disclosure,el.open));
    const focused = document.activeElement;
    const focusStage = focused && focused.tagName === 'SUMMARY' && focused.parentElement.dataset.stage;
    const focusId = focused && focused.id;
    const tab = current(), now = Date.now();
    const key = uatKey();
    const vk = videoKey(), ready = board && board.tracker;
    const nextView=key && ready ? uat(board,key) : vk && ready ? detail(board,vk) : renderTab(tab,board,now);
    const view=document.getElementById("view");
    if (renderedView!==nextView) { view.innerHTML=nextView; renderedView=nextView; }
    const waiting = board ? forBen(((board.tracker || {}).videos) || []).length : 0;
    const nextNav = TABS.map(([id, label, icon]) =>
      `<a id="tab-${id}" href="#${id}" ${id===tab?'aria-current="page"':''} class="${id === tab ? "on" : ""}"><span class="ic">${icon}</span>${label}${id === "review" && waiting ? `<em>${waiting}</em>` : ""}</a>`).join("");
    if (nextNav!==renderedNav) { document.getElementById("nav").innerHTML=nextNav; renderedNav=nextNav; }
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
    document.querySelectorAll('details[data-disclosure]').forEach(el => {
      if (el.dataset.disclosure==='agent-queue' && selectedJob()) el.open=true;
      else if (disclosureState.has(el.dataset.disclosure)) el.open=disclosureState.get(el.dataset.disclosure);
    });
    if (focusId) document.getElementById(focusId)?.focus({preventScroll:true});
    else if (focusStage) document.querySelector(`details[data-stage="${focusStage}"]>summary`)?.focus({preventScroll:true});
    const target=tab==='agents' && selectedJob() ? document.getElementById('job-'+selectedJob()) : null;
    if(tab!=='agents' || !selectedJob()) focusedJobRoute="";
    if(target && focusedJobRoute!==location.hash) {focusedJobRoute=location.hash;requestAnimationFrame(()=>{target.scrollIntoView({block:'center',behavior:'instant'});target.focus({preventScroll:true});});}
    document.querySelectorAll('[data-open-stage]').forEach(button => button.onclick = () => {
      const card = [...document.querySelectorAll('details[data-stage]')].find(el => el.dataset.stage === button.dataset.openStage);
      if (!card) return;
      card.open = true;
      const saved = expandedStages.get(card.dataset.video) || new Set();
      saved.add(card.dataset.stage); expandedStages.set(card.dataset.video, saved);
      card.querySelector('summary')?.focus({preventScroll:true});
      card.scrollIntoView({block:'start', behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    });
    const sortControl = document.getElementById('video-sort');
    if (sortControl) sortControl.onchange = () => { videoSort=sortControl.value; render(); };
    document.querySelectorAll('details[data-stage]').forEach(el => el.addEventListener('toggle', () => {
      const key=el.dataset.video;
      if (!expandedStages.has(key)) expandedStages.set(key,new Set([...document.querySelectorAll('details[data-stage][open]')].map(x=>x.dataset.stage)));
      const saved=expandedStages.get(key); if(el.open) saved.add(el.dataset.stage); else saved.delete(el.dataset.stage);
    }));
    document.querySelectorAll("[data-seg]").forEach(btn => btn.onclick = () => {
      seg = seg === btn.dataset.seg ? "all" : btn.dataset.seg;
      render();
    });
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
        const g = await refFetch();
        if (g.ok) {
          sha = ((await g.json()).object || {}).sha || "";
          if (sha && sha === lastSha && board) {
            if (!uatKey() || !document.getElementById("uat-notes")) render();
            return;
          }
          if (sha) url = DATA_AT(sha);
        }
      } catch (e) {}
      const r = await fetch(url, { cache: sha ? "force-cache" : "no-store" });
      if (!r.ok) throw new Error("Board unavailable");
      const incoming=await r.json();
      if (!incoming || !incoming.tracker || !Array.isArray(incoming.tracker.videos)) throw new Error("Invalid board data");
      board = incoming;
      board.tracker.videos=board.tracker.videos.map(normalizeCut);
      if (sha) lastSha = sha;
      try { const mb = await fetch(MACBOOK + "?t=" + Date.now(), { cache: "no-store" }); macbook = mb.ok ? await mb.json() : null; } catch (e) {}
      if (!uatKey() || !document.getElementById("uat-notes")) render();  // never wipe notes or the player mid-review
    } catch (e) {
      if (!board) { renderedView=""; document.getElementById("view").innerHTML = '<p class="empty" role="status">Could not load the studio data. Retrying automatically.</p>'; }
    }
  }

  // STUDIO_APP_TEST_HOOK
  // Scroll the app-shell main pane (Ben, 6 Nov ~23:55: tab bar is a flex footer, not position:fixed).
  function scrollAppTop() {
    const pane=document.getElementById("view");
    if(pane&&typeof pane.scrollTo==="function") pane.scrollTo(0,0);
    else if(pane) pane.scrollTop=0;
    else window.scrollTo(0,0);
  }
  window.addEventListener("hashchange", () => {
    if(location.hash==="#videos&view=producing") {filterCh="all";filterType="all";seg="all";}
    render(); scrollAppTop();
  });
  render();
  poll();
  setInterval(poll, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) poll(); });
})();
