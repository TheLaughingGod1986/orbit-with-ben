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
    ["approved", "Approved, on its way"],   // Ben, 25 Oct 14:13: what he OK'd, until YouTube has it (video_tracker.py)
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
  let view = "work", workFilter = "all", approvalFilter = "needs", youtubeFilter = "scheduled", completedFilter = "today", search = "";

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
    // Keep the server's decision when an uploaded video has actionable work.
    if (v.working && v.lane === "progress") return "progress";
    if ((v.youtube && v.youtube.videoId) || v.lane === "done") return "done";
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

  // Ben's OK on a card in Ready for OK: straight into "Approved, on its way" (the next board publish fills in the job).
  function approvedStub(v, c, job) {
    const at = c && c.at ? new Date(c.at) : null;
    const on = at && !isNaN(at) ? " on " + at.toLocaleString("en-GB", { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit", timeZone: "Europe/London" }).replace(",", "") : "";
    const version = (c && c.version) || v.version || "";
    const status = job ? `Waiting for the Chief to start ${job}.` : "Waiting for the Chief to queue it.";
    return Object.assign({}, v, { lane: "approved", readyFor: "", waitingOn: "Chief", okNote: "", notes: [],
      line: `You OK'd ${version || "it"}${on}. ${status}`,
      flags: (v.flags || []).filter(f => f.audience !== "chief" && f.kind !== "chief" && f.kind !== "stale" && f.kind !== "deadline" && f.kind !== "stuck" && f.kind !== "nofile"),
      approved: Object.assign({ job: job || "", state: "waiting", status, warn: "", version, okAt: (c && c.at) || "" }, v.approved || {}, { state: "waiting", status }),
      check: c ? { verdict: c.verdict, version: c.version, at: c.at, handled: !!c.handled } : v.check });
  }

  // A card for a job waiting on Ben (awaits_ben in the queue; video_tracker.py apply_ask): always Ready for OK with its
  // own ask line and deadline, Short or long, uploaded or not. A tick on an older version doesn't count against it.
  function applyAsk(v, m) {
    const a = v.ask;
    let c = m[v.checkId] || null;
    if (c && a.version && c.version && c.version !== a.version) c = null;
    const open = c && !c.handled;
    let lane = "ready", readyFor = "Ben", line = a.line || v.line;
    if (open && c.verdict === "change") { lane = "changes"; readyFor = ""; line = `You asked for changes on ${a.version || "this cut"}; ${a.job} is held.`; }
    else if (open && c.verdict === "ok") return approvedStub(v, c, a.job);
    const notes = (c && c.verdict === "change" && Array.isArray(c.fixes)) ? c.fixes.map(f => ({ t: f.t || "", text: f.text || "", done: false })) : [];
    const flags = (v.flags || []).filter(f => f.audience !== "chief" && f.kind !== "chief" && f.kind !== "stale" && (readyFor === "Ben" || f.kind !== "deadline"));
    return Object.assign({}, v, { lane, readyFor, waitingOn: readyFor || "worker", line, notes, flags, okNote: "",
      check: c ? { verdict: c.verdict, version: c.version, at: c.at, handled: !!c.handled } : null });
  }

  function applyChecks(videos) {
    const m = checksMerged();
    return videos.map(v => {
      // On its way (approved_from on the delivering job): the server knows the job's state; show it as published.
      if (v.lane === "approved" && v.approved) return Object.assign({}, v, { flags: (v.flags || []).filter(f => f.audience !== "chief" && f.kind !== "chief") });
      if (v.ask) return applyAsk(v, m);
      const c = m[v.checkId] || null;
      let lane = deriveLane(v, c);
      // Ready for OK only with a cut to play (Ben, 25 Oct 00:03); otherwise it's still being made.
      if (lane === "ready" && !(v.watch && v.watch.url)) lane = v.lane !== "ready" ? v.lane : ((v.jobs || []).length ? "progress" : "upcoming");
      const notes = (c && c.verdict === "change" && Array.isArray(c.fixes) && c.fixes.length)
        ? c.fixes.map(f => ({ t: f.t || "", text: f.text || "", done: false }))
        : (v.notes || []);
      // Chief-only flags (and the old "Brief still asks for your OK" text) never reach Ben's board: on a card he has
      // already OK'd it read as an ask (Ben, 25 Oct 01:00). The Chief still has them in tracker.json.
      const flags = (v.flags || []).filter(f => f.audience !== "chief" && f.kind !== "chief" && f.kind !== "stale");
      if (c && !c.handled && (c.verdict === "ok" || c.verdict === "change") && !(v.jobs || []).length) {
        if (!flags.some(f => f.kind === "stuck")) flags.push({ kind: "stuck", text: "No job queued" });
      }
      // One field drives both the "Waits on" badge and the "Waiting on" line (Ben's 009 screenshot, 25 Oct 00:03).
      const okd = !!(c && c.verdict === "ok" && !c.handled);
      // Ready for OK holds only what waits on Ben (video_tracker.settle_ready).
      if (lane === "ready" && okd) return approvedStub(Object.assign({}, v, { flags }), c, ((v.jobs || [])[0] || {}).id || "");
      if (lane === "ready" && v.lane === "ready" && v.readyFor && v.readyFor !== "Ben") lane = "progress";
      let readyFor = "", waitingOn = v.waitingOn || "", line = v.line;
      if (lane === "ready") {
        readyFor = okd ? "Chief" : (v.lane === "ready" && v.readyFor ? v.readyFor : "Ben");
        waitingOn = readyFor;
        if (readyFor === "Ben") line = "Waiting on your OK.";
        else if (okd) line = "You OK'd it — waiting on Chief PASS.";
        else if (!/chief/i.test(line || "")) line = "Waiting on Chief PASS.";
      }
      if (lane === "changes" && notes.length) line = `${notes.length} change${notes.length === 1 ? "" : "s"} to make.`;
      // Outside Ready for OK / Changes nothing asks Ben (older data said "No cut to watch yet — your final OK Sun 15 Nov").
      if (lane !== "ready" && lane !== "changes" && /\byour (?:final )?OK\b|needs your OK|asks for your OK/i.test(line || "")) {
        const d = (line.match(/\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\s+\d{1,2}\s+[A-Z][a-z]{2}/) || [""])[0];
        const held = (line.match(/ Held up: .*$/) || [""])[0];
        line = "No cut to watch yet. Nothing needed from you now" + (d ? `; review planned ${d}` : "") + "." + held;
      }
      // OK'd and back in the works: say so calmly, ask nothing.
      let okNote = "";
      if (okd && lane !== "ready" && lane !== "changes" && lane !== "done") {
        const at = c.at ? new Date(c.at) : null;
        const on = at && !isNaN(at) ? " on " + at.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: "Europe/London" }).replace(",", "") : "";
        okNote = `You OK'd ${c.version || "this"}${on}. Nothing needed from you.`;
      }
      return Object.assign({}, v, { lane, notes, flags, okNote, readyFor, waitingOn, line, check: c ? { verdict: c.verdict, version: c.version, at: c.at, handled: !!c.handled } : v.check });
    });
  }

  function passFilter(v) {
    if (filterCh !== "all" && v.channel !== filterCh) return false;
    if (filterType === "long" && v.type !== "long") return false;
    if (filterType === "short" && v.type !== "short") return false;
    return true;
  }

  // Ben, 25 Oct 2026: "Just need to approve no need for code", and 13:34: no linking step, no confirmation. Taps just
  // go: a browser without the studio_ben cookie is accepted and given it on that tap (open taps, ../benauth.js).
  // Brief inline note instead of a dialog (Ben, 25 Oct 13:34: no confirmations): "Sent ✓", or what went wrong.
  const toast = (msg, bad) => { try {
    let t = document.getElementById("studio-toast");
    if (!t) { t = document.createElement("div"); t.id = "studio-toast"; t.setAttribute("role", "status");
      t.style.cssText = "position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 18px);transform:translateX(-50%);z-index:9999;padding:10px 18px;border-radius:12px;font:600 15px -apple-system,system-ui,sans-serif;color:#fff;box-shadow:0 4px 18px rgba(0,0,0,.35);max-width:90vw;text-align:center;transition:opacity .25s;pointer-events:none;opacity:0";
      document.body.appendChild(t); }
    t.style.background = bad ? "#b3261e" : "#1f7a3a"; t.textContent = msg; t.style.opacity = "1";
    clearTimeout(t._h); t._h = setTimeout(() => { t.style.opacity = "0"; }, bad ? 6000 : 1800);
  } catch (e) {} };
  window.__studioToast = toast;
  const authHeaders = () => (key ? { "x-board-key": key } : {});

  async function postCheck(id, doc) {
    const r = await fetch(API, {
      method: "POST",
      credentials: "same-origin",
      headers: Object.assign({ "content-type": "application/json" }, authHeaders()),
      body: JSON.stringify({ id, doc }),
    });
    if (!r.ok) { const j = await r.json().catch(() => ({})); throw new Error((j && j.error) || ("save failed " + r.status)); }
    const j = await r.json();
    if (j && j.checks) checks = j.checks;
    if (j && /^not posted/.test(j.chief || "")) toast("Saved, but it didn't reach the Chief's thread. Tell the Chief in chat too.", true);
    else toast("Sent ✓");
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
      if (v.ask) Object.assign(doc, { job: v.ask.job, what: v.ask.what });
      local[v.checkId] = doc;
      bg.remove();
      render();
      try { await postCheck(v.checkId, doc); }
      catch (e) { delete local[v.checkId]; render(); toast("Not sent: " + String(e.message || e), true); }
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
    if (v.ask) Object.assign(doc, { job: v.ask.job, what: v.ask.what });
    local[v.checkId] = doc;
    render();
    try { await postCheck(v.checkId, doc); }
    catch (e) { delete local[v.checkId]; render(); toast("Not sent: " + String(e.message || e), true); }
  }

  // "Approved, on its way": what Ben OK'd, the job carrying it, and that job's live state.
  function approvedHtml(a) {
    const label = { waiting: "Waiting on Chief", queued: "Queued", working: "Working", blocked: "Blocked", uploaded: "Uploaded", cancelled: "Cancelled" }[a.state] || a.state || "";
    const pct = a.state === "working" && a.of ? Math.max(5, Math.min(100, Math.round(100 * (a.step || 0) / a.of))) : 0;
    return `<div class="appr ${esc(a.state || "")}${a.warn ? " warn" : ""}">
      <div class="appr-top"><span class="appr-state">${esc(label)}</span>${a.job ? `<span class="mono">${esc(a.job)}</span>` : ""}${a.version ? `<span>· OK'd ${esc(a.version)}</span>` : ""}</div>
      <div class="appr-line">${esc(a.status || "")}</div>
      ${pct ? `<div class="appr-bar"><span style="width:${pct}%"></span></div>` : ""}
      ${a.airsText ? `<div class="appr-line">Airs ${esc(a.airsText)} London</div>` : ""}
    </div>`;
  }

  function cardHtml(v) {
    const flagged = (v.flags || []).length;
    const chClass = v.channel === "HOS" ? "hos" : "orbit";
    const chLabel = v.channel === "HOS" ? "HOS" : "Orbit";
    const notes = (v.notes || []).map(n =>
      `<li class="${n.done ? "done" : ""}"><span class="box" aria-hidden="true"></span><span>${n.t ? `<span class="t">${esc(n.t)}</span>` : ""}${esc(n.text)}</span></li>`
    ).join("");
    const flagHtml = (v.flags || []).map(f => `<div class="flag">${esc(f.text)}</div>`).join("");
    const showActions = v.lane === "ready" && v.readyFor === "Ben" && (v.type === "long" || !!v.ask);
    // Big Play button for UAT (Ben, 25 Oct 00:03): the exact cut under review via the board's /api/watch link (plays in
    // the browser), YouTube for Done. Review lanes without a link say so instead of hiding the button.
    const review = v.lane === "ready" || v.lane === "changes" || v.lane === "approved";
    const watch = v.watch && v.watch.url
      ? `<a class="btn ${review ? "play" : "watch"}" href="${esc(v.watch.url)}" target="_blank" rel="noopener">▶ Play ${esc(v.watch.version || v.version || "cut")}</a>`
      : (review ? `<span class="btn play none" aria-disabled="true">No preview link yet</span>` : "");
    const yt = v.youtube && v.youtube.url
      ? `<a class="btn ${v.lane === "done" ? "play yt" : "yt"}" href="${esc(v.youtube.url)}" target="_blank" rel="noopener">▶ Play on YouTube</a>`
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
      <p class="line">${esc(cardHeadline(v))}</p>
      ${cardWorkHtml(v)}
      ${v.ask && v.ask.dueText && v.lane === "ready" && v.readyFor === "Ben" ? `<p class="meta"><b>OK by ${esc(v.ask.dueText)} London</b> · ${esc(v.ask.job)}</p>` : ""}
      <p class="meta">Waiting on: ${esc(cardWaiting(v))}</p>
      ${flagHtml ? `<div class="flags">${flagHtml}</div>` : ""}
      ${v.okNote ? `<div class="okline">✓ ${esc(v.okNote)}</div>` : ""}
      ${v.lane === "approved" && v.approved ? approvedHtml(v.approved) : ""}
      ${notes ? `<ul class="notes">${notes}</ul>` : ""}
      ${review ? `<div class="actions">${watch}</div>` : ""}
      <div class="actions">
        ${showActions ? `<button type="button" class="ok" data-ok="${esc(v.key)}">Approve</button>
          <button type="button" class="chg" data-chg="${esc(v.key)}">Request changes</button>` : ""}
        ${review ? "" : watch}${yt}
      </div>
    </article>`;
  }


  // ---- Top strip: Models traffic lights, acting Chief, Now working + Next (Ben, 24 Oct 2026 23:39/23:40) ----
  const MIN = 60 * 1000;
  const tsOf = x => { const t = Date.parse(x || ""); return isNaN(t) ? NaN : t; };
  const hm = t => new Date(t).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/London" });
  const dur = ms => { const m = Math.max(0, Math.round(ms / MIN)); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h${m % 60 ? ` ${m % 60} min` : ""}`; };
  const agentName = by => {
    const b = String(by || "").toLowerCase(), last = b.split("/").pop();
    if (last === "codex-dashboard") return "Codex";
    if (last === "gemini" || last === "agy") return "Gemini";
    if (b === "chief" || b.startsWith("chief/")) return "Grok";
    return last ? last[0].toUpperCase() + last.slice(1) : "";
  };
  // Percent is confirmed steps, never elapsed time presented as completed work.
  function jobProgress(j) {
    const p = j.progress || {}, s = tsOf(j.workStart || j.claimedAt);
    const est = (+j.estMin || +j.typMin || 25) * MIN;
    const elapsed = isNaN(s) ? 0 : Math.max(0, Date.now() - s);
    const reported = Number.isInteger(p.step) && Number.isInteger(p.of) && p.of > 0 && p.step >= 0 && p.step <= p.of;
    return { pct: reported ? Math.round(100 * p.step / p.of) : null,
      left: Math.max(0, est - elapsed), over: elapsed > est, start: s, total: est };
  }
  function jobState(j) {
    if (j.status === "claimed") return j.eta && tsOf(j.eta) < Date.now() - 45 * MIN ? "stalled" : "running";
    if (j.status === "blocked" && /reset|renewal|waits? (?:for |until ).*public|date gate|test.*(?:running|ends?)/i.test(j.result || "")) return "waiting";
    if (j.status === "blocked") return /parked for (?:the )?chief|chief (?:review|pass|ruling)/i.test(j.result || "") ? "review" : "waiting";
    const states = ((board || {}).owb || {}).jobStates || {};
    if (tsOf(j.notBefore) > Date.now() || (j.after && states[j.after]?.status !== "done")) return "waiting";
    return "queued";
  }
  function blockReason(j) {
    if (j.status === "blocked") return j.result || j.last?.what || "No blocker reason recorded.";
    if (j.after) return `Waiting for ${j.after}.`;
    if (j.notBefore) return `Starts after ${new Date(j.notBefore).toLocaleString("en-GB", { timeZone: "Europe/London" })} London.`;
    return "Claim is overdue; waiting for the relay to check or reassign it.";
  }
  function supportingJob(j) {
    return /\bBacklog\b|Weekly .*audit|Daily Studio read|QA sweep|listing check.*(?:live videos|last \d+)/i.test(j.title || "");
  }
  function matchesVideo(j, v) {
    if (supportingJob(j)) return false;
    if ((v.jobs || []).some(x => x.id === j.id)) return true;
    const vid = v.shortId || v.youtube?.videoId;
    if (vid && String(j.title || "").includes(vid)) return true;
    // Parent-film completions are not completions of every Short.
    if (v.type === "short") return false;
    if ((j.taskKeys || []).includes(v.key) || j.film === v.key) return true;
    const f = filmOf(j);
    return f.key === v.key;
  }
  function cardWork(v) {
    const owb = (board || {}).owb || {};
    const live = (owb.jobs || []).filter(j => matchesVideo(j, v));
    // Baked data still supplies live ids before the full queue arrives.
    for (const j of v.jobs || []) if (!supportingJob(j) && !live.some(x => x.id === j.id)) live.push(j);
    const done = (owb.done || []).filter(j => matchesVideo(j, v)).sort((a,b) => tsOf(b.at)-tsOf(a.at));
    return { live, done };
  }
  function cardWaiting(v) {
    if (!["progress","changes"].includes(v.lane)) return v.waitingOn || "—";
    const live=cardWork(v).live;
    const running=live.find(j=>jobState(j)==="running");
    if(running) return agentName(running.by);
    if(live.some(j=>jobState(j)==="queued")) return "next available worker";
    if(live.length) return [...new Set(live.map(j=>jobState(j)==="review"?"Chief review":/ElevenLabs|Flow.*credit|credit.*renew/i.test(j.result||"")?"credit reset":"input / date"))].join(" · ");
    return v.waitingOn || "—";
  }
  function cardHeadline(v) {
    if (!["progress", "changes"].includes(v.lane)) return v.line;
    const live=cardWork(v).live;
    const running=live.find(j=>jobState(j)==="running");
    if(running) return `${agentName(running.by)} is working on ${running.id}: ${taskOf(running)}`;
    const queued=live.find(j=>jobState(j)==="queued");
    if(queued) return `Next: ${queued.id} — ${taskOf(queued)}`;
    if(live.length) return `Work is paused — ${live.some(j=>jobState(j)==="review")?"awaiting Chief review":"waiting on inputs, a release date or credits"}.`;
    return v.line;
  }
  function cardWorkHtml(v) {
    const w = cardWork(v);
    if (!w.live.length && !w.done.length) return "";
    const counts = w.live.reduce((a,j) => { const k=jobState(j); a[k]=(a[k]||0)+1; return a; }, {});
    const summary = [["running","running"],["queued","queued"],["waiting","waiting"],["review","awaiting Chief"],["stalled","stalled"]]
      .filter(([k])=>counts[k]).map(([k,label])=>`${counts[k]} ${label}`).join(" · ");
    const running = w.live.filter(j=>jobState(j)==="running");
    const latest = w.done[0];
    return `<div class="card-work"><b>${w.live.length} ${w.live.length===1?"job":"jobs"} remaining</b>${summary?`<p class="meta">${esc(summary)}</p>`:""}
      ${running.map(j=>jobHtml(j,"now")).join("")}
      ${w.live.length?`<details id="remaining-${esc(v.key)}"><summary>Remaining tasks and blockers</summary>${w.live.filter(j=>jobState(j)!=="running").map(waitingJobHtml).join("")}</details>`:""}
      ${latest?`<div class="last-result">✓ Last completed: ${esc(latest.id)} · ${esc(agentName(latest.by))} · ${esc(new Date(latest.at).toLocaleString("en-GB",{timeZone:"Europe/London"}))} London<br>${esc(taskOf(latest))}</div>`:""}
      ${w.done.length?`<details id="completed-${esc(v.key)}"><summary>Recent completed jobs (${w.done.length})</summary>${w.done.slice(0,8).map(doneJobHtml).join("")}</details>`:""}
    </div>`;
  }
  function waitingJobHtml(j) {
    const state=jobState(j), labels={queued:"Queued",waiting:"Waiting on input/date",review:"Awaiting Chief review",stalled:"Stalled claim",running:"Running"};
    return `<div class="task-row"><b>${esc(j.id)} · ${labels[state]}</b><div>${esc(taskOf(j))}</div>
      ${state!=="queued"?`<p class="block-reason">${esc(blockReason(j))}</p>`:""}
      ${j.progress?.of?`<div class="meta">${j.progress.step} of ${j.progress.of} steps recorded complete${j.progress.note?` · ${esc(j.progress.note)}`:""}</div>`:""}
      ${j.last?.at?`<div class="meta">Updated ${esc(new Date(j.last.at).toLocaleString("en-GB",{timeZone:"Europe/London"}))} London · ${esc(agentName(j.last.by || j.by))}</div>`:""}</div>`;
  }
  function doneJobHtml(j) {
    return `<div class="task-row"><b>✓ ${esc(j.id)} · ${esc(agentName(j.by))} · ${esc(new Date(j.at).toLocaleString("en-GB",{timeZone:"Europe/London"}))} London</b><div>${esc(taskOf(j))}</div>${j.result?`<p class="meta">${esc(j.result)}</p>`:""}</div>`;
  }
  function renderActivity() {
    const el=document.getElementById("activity"), owb=(board||{}).owb;
    if (!el || !owb) return;
    const opened=[...el.querySelectorAll("details[open]")].map(x=>x.id);
    const jobs=owb.jobs||[], counts=jobs.reduce((a,j)=>{const k=jobState(j);a[k]=(a[k]||0)+1;return a;},{});
    const today=new Date().toLocaleDateString("en-CA",{timeZone:"Europe/London"});
    const done=(owb.done||[]).filter(j=>new Date(j.at).toLocaleDateString("en-CA",{timeZone:"Europe/London"})===today).sort((a,b)=>tsOf(b.at)-tsOf(a.at));
    const waiting=jobs.filter(j=>["waiting","review","stalled"].includes(jobState(j)));
    el.innerHTML=`<h2>Studio job activity <span class="meta">Both channels · all jobs</span></h2>
      <div class="activity-counts"><span><b>${counts.running||0}</b> running</span><span><b>${counts.queued||0}</b> queued</span><span><b>${waiting.length}</b> waiting / review</span><span><b>${owb.day?.doneToday ?? done.length}</b> completed today</span></div>
      <p class="meta">Lane numbers count videos. These numbers count jobs; one video can need several jobs.</p>
      <details id="activity-done"><summary>Completed today · ${owb.day?.doneToday ?? done.length}</summary>${done.map(doneJobHtml).join("")||'<p class="meta">No completion records available yet.</p>'}</details>
      <details id="activity-waiting"><summary>Waiting and blockers · ${waiting.length}</summary>${waiting.map(waitingJobHtml).join("")}</details>`;
    opened.forEach(id=>{const d=document.getElementById(id);if(d)d.open=true;});
  }
  function filmOf(j) {
    const t = String(j.title || "").replace(/^URGENT:?\s*/i, "");
    let m = /\bHOS\s*(\d{3})\b/i.exec(t), key = "";
    if (m) key = `HOS:${m[1]}`;
    else if ((m = /^(?:OWB\s*)?(\d{3})\b/.exec(t)) || (m = /\b(?:OWB\s*)(\d{3})\b/.exec(t))) key = `${j.repo === "hos" ? "HOS" : "OWB"}:${m[1]}`;
    else if (j.film && /^\d{3}$/.test(String(j.film))) key = `${j.repo === "hos" ? "HOS" : "OWB"}:${j.film}`;
    const vids = ((board && board.tracker) || {}).videos || [];
    const v = key ? vids.find(x => x.key === key) : null;
    return { key, label: key ? `${key.split(":")[0] === "HOS" ? "HOS" : "Orbit"} ${key.split(":")[1]}` : "", title: v ? v.title : "" };
  }
  function taskOf(j) {
    let t = String(j.title || "").replace(/^URGENT:?\s*/i, "");
    const c = t.indexOf(": ");
    if (c > 0 && c < 48 && /\d{3}|HOS|OWB|Backlog/i.test(t.slice(0, c))) t = t.slice(c + 2);
    t = t.replace(/\s*->\s*/g, " → ").replace(/,?\s*park(ed)? for Chief\.?$/i, "").trim();
    return t.length > 150 ? t.slice(0, 148) + "…" : t;
  }
  function jobHtml(j, kind) {
    const f = filmOf(j);
    let who = j.status === "claimed" ? agentName(j.by) : (j.routedTo || agentName(j.by) || (j.needs === "mini" ? "Mac mini worker" : j.needs || ""));
    // The queue's planned worker may be out of usage: say the relay will fall back rather than show a red worker as next.
    const out = (((board && board.models) || {}).models || []).find(m => m.status === "red" && m.name.toLowerCase() === String(who).toLowerCase());
    if (out && j.status !== "claimed") who = `${who} is out → next worker in its chain`;
    const model = j.model ? ` · ${esc(j.model)}` : "";
    let bar = "", note = "";
    if (kind === "now") {
      const pr = jobProgress(j), p = j.progress || {}, step = p.of ? `${p.step || 0} of ${p.of} steps complete` : (j.stage ? `Stage: ${j.stage}` : "");
      const since = isNaN(pr.start) ? "" : `started ${hm(pr.start)} · ${dur(Date.now() - pr.start)} so far`;
      const tail = pr.over ? "running over" : `~${dur(pr.left)} left`;
      // Colour moves with progress (Ben, 25 Oct 00:03): red-orange < 34, amber 34-66, green > 66; running over is purple.
      const band = pr.over ? "over" : pr.pct < 34 ? "low" : pr.pct <= 66 ? "mid" : "high";
      bar = pr.pct === null ? "" : `<div class="bar ${band}" role="progressbar" aria-label="Confirmed job steps" aria-valuenow="${pr.pct}" aria-valuemin="0" aria-valuemax="100"><i style="width:${pr.pct}%"></i></div>`;
      note = `<b style="color:var(--ink)">${pr.pct === null ? "Progress not reported" : `${pr.pct}% confirmed`} · ${tail} (estimate)</b> · ${[step, since, `usually ~${dur(pr.total)}`].filter(Boolean).join(" · ")}`;
      if (p.note) note += `<br>Latest update${p.at ? ` at ${hm(tsOf(p.at))}` : ""}: ${esc(String(p.note).slice(0, 240))}`;
    } else {
      note = j.urgent ? "Urgent — goes first" : (j.after ? `after ${esc(j.after)}` : "");
    }
    return `<div class="job ${kind}">
      <div class="jtop"><span class="jid">${esc(j.id)}</span>${j.urgent ? '<span class="badge type" style="color:var(--flag)">URGENT</span>' : ""}<span>${esc(who)}${model}</span></div>
      ${f.label ? `<div class="jfilm"><span class="num">${esc(f.label)}</span> ${esc(f.title)}</div>` : ""}
      <div class="jtask">${esc(taskOf(j))}</div>
      ${bar}${note ? `<div class="jnote">${note}</div>` : ""}
    </div>`;
  }
  function nextJobs(owb) {
    const jobs = owb.jobs || [], byId = Object.fromEntries(jobs.map(j => [j.id, j])), now = Date.now();
    const order = ((owb.runOrder || {}).mini) || jobs.filter(j => (j.line || j.needs) === "mini" && j.status === "open")
      .sort((a, b) => (b.urgent ? 1 : 0) - (a.urgent ? 1 : 0) || (a.pos ?? 9e9) - (b.pos ?? 9e9)).map(j => j.id);
    return order.map(id => byId[id]).filter(j => j && j.status === "open" && jobState(j) === "queued").slice(0, 2);
  }
  function renderStrip() {
    const el = document.getElementById("strip");
    if (!el) return;
    const owb = (board && board.owb) || null, M = (board && board.models) || null;
    if (!owb && !M) { el.innerHTML = `<h2>Now working</h2><p class="mmeta">Waiting for the Mac mini's next publish…</p>`; return; }
    let models = "";
    if (M) {
      const chk = tsOf(M.checkedAt), stale = isNaN(chk) || Date.now() - chk > 60 * MIN;
      const chips = (M.models || []).map(m => {
        const st = stale && m.status !== "red" ? "amber" : m.status;
        const icon = st === "green" ? "✓" : st === "red" ? "✗" : "?";
        return `<span class="mchip ${st}" title="${esc(m.why)}"><span class="dot">${icon}</span>${esc(m.name)}</span>`;
      }).join("");
      const ch = M.chief || {};
      const chief = ch.name ? `Chief: <b>${esc(ch.name)}${ch.acting ? " (acting)" : ""}</b>` : `<b style="color:var(--flag)">No Chief</b>`;
      const why = (M.models || []).filter(m => m.status !== "green").map(m =>
        `<li><b>${esc(m.name)}</b>: ${esc(String(m.why).slice(0, 140))}${m.until ? ` (back ${esc(new Date(m.until).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: "Europe/London" }))})` : ""}</li>`).join("");
      models = `<div class="row"><h2>Models</h2><div class="models">${chips}</div>
        <div class="mmeta">${chief} · ${stale ? '<b style="color:var(--ready)">stale</b> — ' : ""}checked ${isNaN(chk) ? "—" : hm(chk) + " London"}</div>
        ${why ? `<details class="mmeta"><summary>Why</summary><ul style="margin:4px 0 0;padding-left:18px">${why}</ul></details>` : ""}</div>`;
    }
    if(M?.chiefChain?.length) models += `<p class="mmeta">Chief order: ${M.chiefChain.map(c=>esc(c.name)).join(" → ")}. The first available takes the role.</p>`;
    let jobsHtml = "";
    if (owb) {
      const now = (owb.jobs || []).filter(j => jobState(j) === "running")
        .sort((a, b) => (b.urgent ? 1 : 0) - (a.urgent ? 1 : 0) || tsOf(a.claimedAt) - tsOf(b.claimedAt));
      const next = nextJobs(owb);
      jobsHtml = `<div class="row jobs">
        <div class="row"><h2>Now working</h2>${now.length ? now.map(j => jobHtml(j, "now")).join("") : '<p class="mmeta">No job is currently claimed. See queued work and waiting reasons below.</p>'}</div>
        <div class="row"><h2>Next</h2><div class="nextlist">${next.length ? next.map(j => jobHtml(j, "next")).join("") : '<p class="mmeta">Nothing else queued.</p>'}</div></div>
      </div>`;
    }
    const opened=el.querySelector("details")?.open;
    el.innerHTML = `<details ${opened?"open":""}><summary>Agents & services · ${esc((M?.chief?.name)||"Chief unknown")}${M?.chief?.acting?" acting Chief":""}</summary>${models}</details>`;
  }

  function jobChannel(j) {
    const title=String(j.title||"");
    if(/both channels|OWB.*HOS|HOS.*OWB/i.test(title)) return "both";
    return j.repo==="hos" || /\bHOS\b/.test(title) ? "HOS" : "OWB";
  }
  function jobBucket(j) {
    // Raw blocked jobs stay countable even when the cut is approved or awaits Chief.
    if(j.status==="blocked") return "blocked";
    const state=jobState(j);
    return state==="running"?"working":state==="stalled"?"stalled":state==="waiting"?"waiting":"todo";
  }
  function nextAction(j) {
    const state=jobState(j), reason=blockReason(j);
    if(state==="running") return j.progress?.note ? `Continue from: ${j.progress.note}` : "Worker to report the next completed step.";
    if(state==="stalled") return "Relay to check the overdue claim and reassign or renew it.";
    if(j.after && (((board||{}).owb||{}).jobStates||{})[j.after]?.status!=="done") return `Finish ${j.after}, then resume this job.`;
    if(j.kind==="chief" && j.status==="open" && state==="queued") return `${board?.models?.chief?.name || "The elected Chief"} to claim and review this job.`;
    if(j.status==="open" && state==="queued") return `${j.routedTo || "Next eligible worker"} to claim and start this job.`;
    if(/ElevenLabs|Flow.*credit|credit.*renewal/i.test(reason)) return "Verify the recorded credit reset or renewal, then resume within the available balance.";
    if(/public|publishAt|date gate|Test & Compare|test.*(?:running|end)/i.test(reason) && !/gate.*fail/i.test(reason)) return "Check the recorded release or test date; resume the unfinished step when its input is ready.";
    if(state==="review") return /FAIL|fails|gate|limiter/i.test(reason) ? "Chief to decide the correction and approval path; the upload remains held." : "Chief to review the recorded result and release, revise or close the job.";
    return "Resolve the recorded blocker, then return this job to the queue.";
  }
  function fmtDate(at) {
    return Number.isFinite(tsOf(at)) ? new Date(at).toLocaleString("en-GB",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit",timeZone:"Europe/London"})+" London" : "Not recorded";
  }
  function approvedRecords(videos) {
    const rows=new Map();
    for(const e of (board?.briefs?.approved || [])) {
      const state=board?.owb?.jobStates?.[e.job]?.status || e.jobStatus || "unknown";
      rows.set(e.job+":"+e.version,{...e,jobStatus:state,at:e.okAt,title:e.title||e.what||e.job});
    }
    for(const v of videos.filter(v=>v.lane==="approved")) {
      const e=v.approved||{}, id=e.job||v.ask?.job||v.key, k=id+":"+(e.version||v.version||"");
      if(!rows.has(k)) rows.set(k,{...e,job:id,version:e.version||v.version,at:e.okAt||v.check?.at,title:v.title,channel:v.channel,jobStatus:e.state||"waiting"});
    }
    return [...rows.values()].sort((a,b)=>(tsOf(b.at)||0)-(tsOf(a.at)||0));
  }
  function pipelineVideos(videos) {
    const seen=new Set();
    return videos.filter(v=>{
      // Delivery receipts also create approval placeholders with no YouTube id.
      // They are approval history, not additional planned or scheduled videos.
      if(/:(?:OK|ASK):/.test(v.key||"")) return false;
      const key=v.youtube?.videoId || v.key;
      if(seen.has(key))return false;
      seen.add(key);return true;
    });
  }
  function workflowCounts(videos, channel="all") {
    const pass=ch=>channel==="all"||ch===channel||ch==="both";
    const pipeline=pipelineVideos(videos).filter(v=>pass(v.channel));
    const jobs=(board?.owb?.jobs||[]).filter(j=>pass(jobChannel(j))), counts={all:jobs.length,working:0,todo:0,blocked:0,waiting:0,stalled:0};
    jobs.forEach(j=>counts[jobBucket(j)]++);
    return {...counts,needs:videos.filter(v=>pass(v.channel)&&v.lane==="ready"&&v.readyFor==="Ben").length,
      approved:approvedRecords(videos).filter(e=>pass(e.channel)).length,changes:videos.filter(v=>pass(v.channel)&&v.lane==="changes").length,
      scheduled:pipeline.filter(v=>v.youtube?.videoId&&v.youtube.state==="scheduled").length,
      live:pipeline.filter(v=>v.youtube?.videoId&&v.youtube.state==="live").length,
      planned:pipeline.filter(v=>!v.youtube?.videoId).length,
      uploaded:pipeline.filter(v=>v.youtube?.videoId && !["live","scheduled"].includes(v.youtube.state)).length};
  }
  function workflowJobHtml(j) {
    const bucket=jobBucket(j), labels={working:"Working now",todo:"To do",blocked:"Blocked",waiting:"Waiting on dependency",stalled:"Stalled claim"};
    const approvals=board?.briefs?.approved||[], approval=approvals.find(e=>e.job===j.id);
    const who=agentName(j.by || j.last?.by), updated=j.last?.at||j.progress?.at||j.claimedAt;
    const p=j.progress, pr=jobProgress(j);
    const liveProgress=`<div class="step-count"><b>${pr.pct===null?"Progress not reported":`${pr.pct}% confirmed · ${p.step} of ${p.of} steps complete`}</b>${pr.pct===null?"":`<div class="bar" role="progressbar" aria-label="Confirmed job steps" aria-valuenow="${pr.pct}" aria-valuemin="0" aria-valuemax="100"><i style="width:${pr.pct}%"></i></div>`}<p class="meta">${pr.over?"Running past estimate":`About ${dur(pr.left)} left (estimate)`}${p?.note?` · ${esc(p.note)}`:""}</p></div>`;
    return `<article class="work-card" data-job="${esc(j.id)}"><div class="top"><span class="badge ${jobChannel(j)==="HOS"?"hos":"orbit"}">${esc(jobChannel(j)==="OWB"?"Orbit":jobChannel(j))}</span>
      <span class="status-chip ${bucket}">${labels[bucket]}</span>${approval?'<span class="status-chip approved">You approved</span>':""}${jobState(j)==="review"?'<span class="status-chip review">Chief decision</span>':""}<b class="job-id">${esc(j.id)}</b></div>
      <h3>${esc(j.title||j.id)}</h3>
      <p class="meta">${bucket==="working"?"Working":"Last worked"} by ${esc(who||"not recorded")} · Updated ${esc(fmtDate(updated))}</p>
      ${bucket==="working"?liveProgress:(p?.of?`<p class="step-count"><b>${p.step} of ${p.of} steps complete</b>${p.note?` · ${esc(p.note)}`:""}</p>`:"")}
      ${["blocked","waiting","stalled"].includes(bucket)?`<div class="why"><b>${bucket==="blocked"?"Blocked because":"Waiting because"}</b><p>${esc(blockReason(j))}</p></div>`:""}
      <div class="next-action"><b>Next step</b><p>${esc(nextAction(j))}</p></div>
      ${j.last?.what?`<details id="history-${esc(j.id)}"><summary>Latest recorded activity</summary><p>${esc(j.last.what)}</p></details>`:""}
    </article>`;
  }
  function approvalRecordHtml(e) {
    const labels={done:"Delivery job complete",blocked:"Approved, but blocked",claimed:"Delivery in progress",open:"Approved, queued",cancelled:"Cancelled after approval",waiting:"Approved, awaiting delivery"};
    const j=(board?.owb?.jobs||[]).find(j=>j.id===e.job);
    return `<article class="work-card"><div class="top"><span class="status-chip approved">You approved ${esc(e.version||"")}</span><b>${esc(e.job)}</b><span class="status-chip ${e.jobStatus==="blocked"?"blocked":""}">${esc(labels[e.jobStatus]||e.jobStatus)}</span></div>
      <h3>${esc(e.title)}</h3><p>${esc(e.what||"")}</p><p class="meta">Approved ${esc(fmtDate(e.at))}${e.doneAt?` · Job completed ${esc(fmtDate(e.doneAt))}`:""}</p>
      ${j?`${["blocked","waiting","stalled"].includes(jobBucket(j))?`<div class="why"><p>${esc(blockReason(j))}</p></div>`:""}<div class="next-action"><b>Next step</b><p>${esc(nextAction(j))}</p></div>`:e.result?`<p class="meta">Result: ${esc(e.result)}</p>`:""}
      ${e.watch?.url?`<a class="record-link" href="${esc(e.watch.url)}" target="_blank" rel="noopener">▶ Play approved cut</a>`:""}</article>`;
  }
  function render() {
    const searchFocused=document.activeElement?.id==="work-search", searchPosition=searchFocused?document.activeElement.selectionStart:null;
    renderStrip();
    const root=board?.tracker, boardEl=document.getElementById("board");
    if(!root || !Array.isArray(root.videos) || !board.owb) {boardEl.innerHTML='<p class="empty">Loading the current studio queue…</p>';return;}
    const videos=applyChecks(root.videos), c=workflowCounts(videos,filterCh);
    const when=window.__boardData?.dataChangedAt||root.updatedAt;
    document.getElementById("asof").textContent=when?`Updated ${fmtDate(when)} · refreshes every minute`:"Waiting for a current snapshot";
    document.getElementById("activity").innerHTML=`<nav class="view-tabs" aria-label="Studio views">${[["work","Work & blockers",c.all],["approvals","Your approvals",c.needs+c.approved+c.changes],["youtube","Video pipeline",c.planned+c.scheduled+c.live+c.uploaded],["completed","Completed today",filterCh==="all"?(board.owb?.day?.doneToday||0):(board.owb?.done||[]).filter(j=>jobChannel(j)===filterCh&&tsOf(j.at)>=tsOf(board.owb?.day?.since)).length]].map(([id,label,n])=>`<button type="button" class="${view===id?"on":""}" data-view="${id}">${label} <b>${n}</b></button>`).join("")}</nav>
      <p class="process">To do → Working → Review / your OK → Approved → Scheduled → Live</p>`;
    document.querySelectorAll("[data-view]").forEach(b=>b.onclick=()=>{view=b.dataset.view;search="";render();});
    const chips=[["all","All channels"],["OWB","Orbit"],["HOS","HOS"]];
    document.getElementById("filters").innerHTML=chips.map(([id,label])=>`<button type="button" class="${filterCh===id?"on":""}" data-channel="${id}">${label}</button>`).join("");
    document.querySelectorAll("[data-channel]").forEach(b=>b.onclick=()=>{filterCh=b.dataset.channel;render();});
    const opened=[...boardEl.querySelectorAll("details[open]")].map(x=>x.id);
    const channelPass=ch=>filterCh==="all"||ch===filterCh||ch==="both";
    let heading="",intro="", tabs=[],body="", matches=0, total=0;
    if(view==="work") {
      heading=({all:"All current jobs",working:"Working now",todo:"To do",blocked:"Blocked jobs",waiting:"Waiting on dependencies",stalled:"Stalled claims"})[workFilter];
      intro=`${c.all} current jobs · ${c.working} working · ${c.todo} to do · ${c.blocked} blocked · ${c.waiting} waiting${c.stalled?` · ${c.stalled} stalled`:""}.`;
      tabs=[["all",`All current ${c.all}`],["working",`Working ${c.working}`],["todo",`To do ${c.todo}`],["blocked",`Blocked ${c.blocked}`],["waiting",`Waiting ${c.waiting}`],...(c.stalled?[["stalled",`Stalled ${c.stalled}`]]:[])];
      let jobs=(board.owb?.jobs||[]).filter(j=>(workFilter==="all"||jobBucket(j)===workFilter)&&channelPass(jobChannel(j)));
      total=jobs.length;jobs=jobs.filter(j=>(j.id+" "+j.title+" "+(j.result||"")).toLowerCase().includes(search.toLowerCase()));
      const rank={working:0,stalled:1,todo:2,blocked:3,waiting:4};jobs.sort((a,b)=>rank[jobBucket(a)]-rank[jobBucket(b)]||Number(!!b.urgent)-Number(!!a.urgent)||(tsOf(b.last?.at)||0)-(tsOf(a.last?.at)||0));
      matches=jobs.length;body=jobs.map(workflowJobHtml).join("");
    } else if(view==="approvals") {
      heading="Your approvals";intro="Your decisions are separate from Chief reviews. An approved cut can still be blocked; its approval stays visible here.";
      tabs=[["needs",`Needs your OK ${c.needs}`],["approved",`You approved ${c.approved}`],["changes",`Changes requested ${c.changes}`]];
      if(approvalFilter==="approved") {
        let rows=approvedRecords(videos).filter(e=>channelPass(e.channel));total=rows.length;rows=rows.filter(e=>(e.job+" "+e.title+" "+e.what).toLowerCase().includes(search.toLowerCase()));matches=rows.length;body=rows.map(approvalRecordHtml).join("");
      } else {
        let rows=videos.filter(v=>channelPass(v.channel)&&(approvalFilter==="needs"?v.lane==="ready"&&v.readyFor==="Ben":v.lane==="changes"));total=rows.length;rows=rows.filter(v=>(v.title+" "+v.key).toLowerCase().includes(search.toLowerCase()));matches=rows.length;body=rows.map(cardHtml).join("");
      }
    } else if(view==="youtube") {
      heading="Video pipeline";intro="Scheduled means uploaded and waiting for its air time. Live means recorded as public by the tracker. Video publication is separate from unfinished follow-up jobs.";
      tabs=[["planned",`Planned / in production ${c.planned}`],["scheduled",`Scheduled ${c.scheduled}`],["live",`Live ${c.live}`],["uploaded",`Uploaded, no schedule ${c.uploaded}`]];
      let rows=pipelineVideos(videos).filter(v=>channelPass(v.channel)&&(youtubeFilter==="planned"?!v.youtube?.videoId:v.youtube?.videoId&&(youtubeFilter==="uploaded"?!["live","scheduled"].includes(v.youtube.state):v.youtube.state===youtubeFilter)));
      total=rows.length;rows=rows.filter(v=>(v.title+" "+v.key+" "+(v.youtube?.videoId||"")).toLowerCase().includes(search.toLowerCase()));rows.sort((a,b)=>(youtubeFilter==="live"?-1:1)*((tsOf(a.youtube?.publishAt)||0)-(tsOf(b.youtube?.publishAt)||0)));matches=rows.length;
      body=rows.map(v=>`<div class="publication"><div class="publication-state ${youtubeFilter}">${youtubeFilter==="live"?"● Live on YouTube":youtubeFilter==="scheduled"?"◷ Scheduled":youtubeFilter==="planned"?"Planned / in production":"Uploaded · no schedule recorded"}${v.youtube?.publishAt?` · ${esc(fmtDate(v.youtube.publishAt))}`:""}</div>${youtubeFilter==="scheduled"&&tsOf(v.youtube?.publishAt)<Date.now()-15*MIN?`<p class="flag">Past the recorded air time — YouTube status needs a fresh check.</p>`:""}${cardHtml(v)}</div>`).join("");
    } else {
      heading="Completed jobs";intro="Completed jobs have a recorded result. Completing one job does not necessarily finish its video. Review handoffs remain in the blocked queue until accepted.";
      const history=board.owb?.done||[], since=tsOf(board.owb?.day?.since);
      const today=history.filter(j=>Number.isFinite(since)&&tsOf(j.at)>=since);
      tabs=[["today",`Today ${board.owb?.day?.doneToday ?? today.length}`],["history",`Recent results ${history.length}`]];
      const rows=(completedFilter==="today"?today:history).filter(j=>channelPass(jobChannel(j))&&(j.id+" "+j.title+" "+j.result).toLowerCase().includes(search.toLowerCase()));total=matches=rows.length;
      if(completedFilter==="today" && today.length<(board.owb?.day?.doneToday||0)) intro+=` Showing ${today.length} retained records of ${board.owb.day.doneToday} completions today.`;
      body=rows.map(j=>`<article class="work-card">${doneJobHtml(j)}</article>`).join("");
    }
    boardEl.className="workflow";
    const selected=view==="work"?workFilter:view==="approvals"?approvalFilter:view==="completed"?completedFilter:youtubeFilter;
    const empty=view==="approvals"&&approvalFilter==="needs"?"Nothing needs your approval right now. Chief review items are in Work & blockers.":"No items match this view.";
    boardEl.innerHTML=`<div class="workflow-heading"><h2>${heading}</h2><p>${esc(intro)}</p></div><div class="status-tabs">${tabs.map(([id,label])=>`<button type="button" class="${selected===id?"on":""}" data-status="${id}">${label}</button>`).join("")}</div>
      <label class="search-label">Find a job or video<input id="work-search" type="search" placeholder="Search title, job ID or blocker" value="${esc(search)}"></label><p class="result-count">Showing ${matches}${total!==matches?` of ${total}`:""} ${view==="youtube"?"videos":view==="approvals"?"approval items":"jobs"}${filterCh!=="all"?` · ${filterCh}`:""}${view==="completed"?" · recent retained history":""}</p>
      <div class="work-grid">${body||`<p class="empty">${empty}</p>`}</div>`;
    document.querySelectorAll("[data-status]").forEach(b=>b.onclick=()=>{if(view==="work")workFilter=b.dataset.status;else if(view==="approvals")approvalFilter=b.dataset.status;else if(view==="completed")completedFilter=b.dataset.status;else youtubeFilter=b.dataset.status;search="";render();});
    document.getElementById("work-search").oninput=e=>{const value=e.target.value,pos=e.target.selectionStart;search=value;render();const input=document.getElementById("work-search");input.focus();try{input.setSelectionRange(pos,pos);}catch{}};
    opened.forEach(id=>{const d=document.getElementById(id);if(d)d.open=true;});
    if(searchFocused){const input=document.getElementById("work-search");input.focus();try{input.setSelectionRange(searchPosition,searchPosition);}catch{}}
    boardEl.querySelectorAll("[data-ok]").forEach(b=>b.onclick=()=>{const v=videos.find(v=>v.key===b.dataset.ok);if(v)approve(v);});
    boardEl.querySelectorAll("[data-chg]").forEach(b=>b.onclick=()=>{const v=videos.find(v=>v.key===b.dataset.chg);if(v)openChangesModal(v);});
  }

  async function pollChecks() {
    try {
      const r = await fetch(API + "?t=" + Date.now(), { cache: "no-store", credentials: "same-origin", headers: authHeaders() });
      if (!r.ok) return;
      const j = await r.json();
      window.__benLinked = !!(j && j.ben);
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
  setInterval(() => { if(!document.querySelector("#work-search:focus")) render(); }, 30 * 1000);  // progress bar and 'so far' times move between data refreshes
  document.addEventListener("visibilitychange", () => { if (!document.hidden) { pollData(); pollChecks(); } });
})();
