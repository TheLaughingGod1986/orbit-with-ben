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
    let jobsHtml = "";
    if (owb) {
      const now = (owb.jobs || []).filter(j => jobState(j) === "running")
        .sort((a, b) => (b.urgent ? 1 : 0) - (a.urgent ? 1 : 0) || tsOf(a.claimedAt) - tsOf(b.claimedAt));
      const next = nextJobs(owb);
      const chiefWork = M?.chiefWork || {}, review = chiefWork.active;
      const reviewLive = review && tsOf(review.expiresAt) > Date.now();
      const reviewHtml = reviewLive ? `<div class="job now"><b>${esc(review.job)} · Chief review</b>
        <p>${esc(review.title)}</p><p class="mmeta">${esc(agentName(review.agent))} reviewing · started ${esc(hm(tsOf(review.startedAt)))} London. Production remains held until the decision is recorded.</p></div>` : "";
      const chiefNext = (chiefWork.next || []).filter(j => !reviewLive || j.id !== review.job);
      const chiefNextHtml = chiefNext.slice(0, 1).map(j => `<div class="job"><b>${esc(j.id)} · Next Chief task</b><p>${esc(j.title)}</p><p class="mmeta">Awaiting ${esc(M?.chief?.name || "the elected Chief")}</p></div>`).join("");
      jobsHtml = `<div class="row jobs">
        <div class="row"><h2>Now working</h2>${now.length ? jobHtml(now[0], "now") : reviewLive ? reviewHtml : '<p class="mmeta">No job is currently claimed. See queued work and waiting reasons below.</p>'}</div>
        <div class="row"><h2>Next</h2><div class="nextlist">${chiefNext.length ? chiefNextHtml : next.length ? jobHtml(next[0], "next") : '<p class="mmeta">Nothing else queued.</p>'}</div></div>
      </div>`;
    }
    el.innerHTML = models + jobsHtml;
  }

  function render() {
    renderStrip();
    renderActivity();
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
    const opened=[...boardEl.querySelectorAll("details[open]")].map(x=>x.id);
    boardEl.innerHTML = LANES.map(([id, label]) => {
      const all = videos.filter(v => v.lane === id);
      const shown = id === "done" && !showOldDone ? all.filter(v => !v.collapsed) : all;
      const hidden = id === "done" ? all.filter(v => v.collapsed).length : 0;
      const body = shown.length ? shown.map(cardHtml).join("") : `<p class="empty">Nothing here</p>`;
      const more = hidden
        ? `<button type="button" class="collapsed-toggle" data-old="1">Show ${hidden} older public</button>`
        : (id === "done" && showOldDone
          ? `<button type="button" class="collapsed-toggle" data-old="0">Hide older public</button>` : "");
      const running=all.filter(v=>cardWork(v).live.some(j=>jobState(j)==="running")).length;
      const sub=id==="progress"?`<p class="lane-summary">${running} being worked on · ${all.length-running} queued / waiting</p>`:"";
      return `<section class="lane" data-lane="${id}"><h2>${label}<span class="n">${shown.length} videos</span></h2>${sub}<div class="cards">${body}${more}</div></section>`;
    }).join("");

    opened.forEach(id=>{const d=document.getElementById(id);if(d)d.open=true;});
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

    // Play opens the signed link as is: no code prompt (Ben, 25 Oct). Older unsigned links get the code if the phone has it.
    document.querySelectorAll("a[href*='/api/watch?']").forEach(a => {
      a.addEventListener("click", () => {
        const u = new URL(a.href, location.href);
        if (u.searchParams.get("s") || !key) return;
        u.searchParams.set("k", key); a.href = u.toString();
      }, true);
    });
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
  setInterval(() => { renderStrip(); renderActivity(); }, 30 * 1000);  // progress bar and 'so far' times move between data refreshes
  document.addEventListener("visibilitychange", () => { if (!document.hidden) { pollData(); pollChecks(); } });
})();
