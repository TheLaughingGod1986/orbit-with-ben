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
    // YouTube has no thumbnail for a private or scheduled video (404): ask only for public ones.
    const id = isLive(v) && v.youtube.videoId;
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
  function jobGroups(vs) {
    const groups = new Map();
    for (const v of vs) { const id = activeJob(v).id || v.key; groups.set(id, (groups.get(id) || []).concat([v])); }
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
    return `<a class="row" href="#agents"><div class="thumb job">${esc(j.id)}</div><div class="body"><b>${esc(clip(j.remaining_action || j.title, 90))}</b>
      <span class="meta">Studio job · not one video</span><span class="doing">${esc(AGENTS[j.by] || j.by || "An agent")} · ${esc(j.id)}</span>
      ${p ? bar(p, left) : left ? `<span class="meta">${esc(left)}</span>` : ""}</div><span class="chev">›</span></a>`;
  }
  const uatLink = v => `#uat=${encodeURIComponent(v.key)}`;

  function stage(v) {
    if (isLive(v)) return "Published";
    if ((v.youtube || {}).state === "scheduled") return "Scheduled";
    if (v.lane === "ready") return v.readyFor === "Ben" ? "Ready for you" : `Waiting on ${v.readyFor || "a check"}`;
    if (v.lane === "changes") return "Fixing your changes";
    if (v.lane === "approved") return "Approved, on its way";
    if (v.lane === "done") return v.youtube && v.youtube.state === "scheduled" ? "Scheduled" : "On YouTube";
    const live = (v.jobs || []).find(j => j.status === "claimed");
    if (live) return "Working now";
    if ((v.jobs || []).some(j => j.status === "blocked")) return "On hold";
    return v.lane === "upcoming" ? "Planned" : "In progress";
  }

  const forBen = vs => uniqueVideos(vs).filter(v => !isLive(v) && v.lane === "ready" && v.readyFor === "Ben" && !sent[v.checkId]);
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
  const inProgress = vs => vs.filter(v => ["progress", "changes", "ready", "approved"].includes(v.lane) && !isLive(v) && !forBen([v]).length);

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
    const week = scheduledThisWeek(vs, now);
    return {
      health, ready: forBen(vs), working: vs.filter(isWorking),
      progress: inProgress(vs), week, chief: m.chief || {}, runner: m.runner || {},
      jobs: { working: jobs.filter(j => j.status === "claimed").length, queued: jobs.filter(j => j.status === "open").length,
              held: jobs.filter(j => j.status === "blocked").length, doneToday: ((b.owb || {}).day || {}).doneToday || 0 },
    };
  }

  function row(v, extra, href) {
    return `<a class="row" href="${href || detailLink(v)}">${thumb(v)}<div class="body"><b>${esc(v.title)}</b>
      <span class="meta">${ch(v)} · ${kind(v)}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}</span>${extra || (isLive(v) ? "" : bar(progressOf(v)))}</div><span class="chev">›</span></a>`;
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

  // Milestone progress is independent of job step progress. Older board data stays readable.
  function uatOutlook(v, now) {
    if (v.lane === "ready" && v.readyFor === "Ben") return {label: "Ready for UAT", detail: "Your review can start now", tone: "green"};
    if (["approved", "done"].includes(v.lane)) return {label: "UAT handoff passed", detail: "Follow-up work is shown below", tone: "green"};
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
    if (state === 'blocked') return {text:'Blocked',tone:'held',icon:'!'};
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
      return {job:j,scope:best.scope,why:blockerReason(hold.reason||hold.condition||j.result)||'The job is blocked, but its reason has not been recorded.',
        action:blockerAction(hold.action||j.remaining_action||'')||(stageApproval?nextAction(m):'No unblock action is recorded. The job owner needs to add the missing next step.'),
        owner:AGENTS[hold.owner||j.by]||hold.owner||j.by||'Not recorded',checkAt:hold.check_at||'',checkedAt:hold.checked_at||'',dependency:j.after||'',others:entries.filter(x=>x.job.id!==j.id)};
    }
    const evidence=String(source.note||source.proof||m.evidence||'');
    const meaningful=evidence.length>10 && /\s/.test(evidence) && !/^[a-f0-9]+$/i.test(evidence);
    return {scope:'stage',why:stageApproval?`Awaiting ${reviewer||'the recorded reviewer’s'} approval.`:meaningful?blockerReason(evidence):`${m.label} is marked blocked, but no stage-specific reason is recorded.`,
      action:stageApproval?nextAction(m):m.nextAction||'No unblock action is recorded. A responsible owner and a specific next step need to be recorded.',
      owner:stageApproval?(reviewer||'Not recorded'):ownerName(m)==='Unassigned'?'Not recorded':ownerName(m),others:entries};
  }
  function reviewQueueInfo(b,j,now,mb=null) {
    if(!j) return null;
    const jobs=((b.owb||{}).jobs)||[], state=(b.workflow||{}).states||{};
    const task=jobs.find(x=>x.recheck_of===j.id&&['open','claimed'].includes(x.status));
    const needsReview=/(?:parked|awaiting|waiting) for (?:the )?Chief.*(?:review|approval)/i.test(String((j.hold||{}).condition||j.result||''));
    if(!task||!needsReview) return null;
    const fresh=stamp=>{const age=now-Date.parse(stamp||'');return Number.isFinite(age)&&age>=0&&age<=5*MIN;};
    const models=b.models||{}, chief=(models.chief||{}).agent, reviewer=AGENTS[chief]||chief||'Elected Chief';
    const ownState=state[task.id]||{}, predecessor=((b.owb||{}).jobStates||{})[task.after]||{};
    const ready=fresh((b.workflow||{}).at)?['queued','review'].includes(ownState.state):task.status==='open'&&!task.hold&&(!task.after||predecessor.status==='done')&&(!task.notBefore||Date.parse(task.notBefore)<=now);
    const active=jobs.find(x=>x.status==='claimed'&&x.by===chief);
    const next=(b.workflow||{}).next||{}, runner=models.runner||{};
    const starting=runner.state==='working'&&fresh(runner.at)&&next.id===runner.job&&next.worker===chief?jobs.find(x=>x.id===runner.job):null;
    const busy=fresh(models.checkedAt)?active||starting:null;
    const estimate=busy&&recordedTaskProgress(busy), started=busy&&Date.parse(busy.claimedAt||'');
    const eta=estimate&&estimate.step>0&&estimate.step<estimate.of&&Number.isFinite(started)&&started<=now?etaOf(busy,now):null;
    const availability=eta&&!eta.over?`Current task estimate: about ${durationText(eta.min)} remaining. A review start time is not reserved.`:'No reliable reviewer-free time is recorded.';
    const mbAge=mb?now-Date.parse(mb.at||''):NaN;
    const macbookText=Number.isFinite(mbAge)&&mbAge>=0&&mbAge<=20*MIN?`MacBook worker: ${mb.state||'state unreported'}${mb.job?' on '+mb.job:''}${(mb.why||[]).length?' · '+mb.why.join('; '):''}.`:'MacBook availability report is stale or missing.';
    return {task,reviewer,ready,busy,availability,macbookText};
  }
  function blockerGuide(v,m,now=Date.now()) {
    const model=blockerModel(v,m), j=model.job, review=reviewQueueInfo(board||{},j,now,macbook);
    const due=Date.parse(model.checkAt||''), checked=Date.parse(model.checkedAt||'');
    const states=((board||{}).owb||{}).jobStates||{}, dependency=states[model.dependency]||{};
    const dependencyStatus={done:'Completed',blocked:'Blocked',claimed:'In progress',open:'Queued',cancelled:'Cancelled'}[dependency.status]||'Status unreported';
    const check=Number.isFinite(due)?`${due<now?'Check overdue: ':'Next recorded check: '}${recordedTime(model.checkAt)}`:'No next check recorded';
    return `<div class="blocker-guide" data-blocker-scope="${model.scope}"><p class="blocker-scope">${model.scope==='reference'?'Related recorded hold':model.scope==='video'?'Video-level hold · stage link unconfirmed':'Recorded stage hold'}</p>
      <h3>${review?'Awaiting Chief review':'Why blocked'}</h3><p class="blocker-reason">${esc(model.why)}</p>
      <h3>How to unblock</h3><p class="blocker-action">${esc(model.action)}</p>
      <dl class="blocker-facts"><div><dt>${j?(review?'Previous worker':'Recorded job owner'):'Reviewer / owner'}</dt><dd>${esc(model.owner)}</dd></div><div><dt>Follow-up</dt><dd>${esc(check)}</dd></div>${Number.isFinite(checked)?`<div><dt>Last checked</dt><dd>${esc(recordedTime(model.checkedAt))}</dd></div>`:''}${model.dependency?`<div><dt>Recorded dependency</dt><dd>${esc(model.dependency)} · ${esc(dependencyStatus)}</dd></div>`:''}</dl>
      ${review?`<div class="review-handoff"><p><b>${esc(review.reviewer)} · ${review.ready?'review queued and eligible now':review.task.status==='claimed'?'review job claimed':'review queue state needs confirmation'}</b></p><a class="blocker-job-link" href="${jobRoute(review.task.id)}">Open review job ${esc(review.task.id)} →</a>${review.busy?`<p>${esc(review.reviewer)} is ${review.busy.status==='claimed'?'working on':'starting'} ${esc(review.busy.id)}: ${esc(clip(review.busy.remaining_action||review.busy.title,140))}</p>`:''}<details class="technical"><summary>Reviewer availability and MacBook</summary><p>${esc(review.availability)}</p><p>${esc(review.macbookText)}</p><p>Device availability does not establish media-review capability or Chief approval authority.</p></details></div>`:''}
      ${Number.isFinite(due)?`<p class="blocker-caption">${review?'The follow-up time does not schedule or delay the queued review.':'The check time is a follow-up, not a promise that the video will be unblocked.'}</p>`:''}
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
    if (v.lane === 'ready' && v.readyFor === 'Ben') return {value:'Ready now',reason:'Your review can start',confidence:'Ready',credible:false};
    if (['approved','done'].includes(v.lane) || isLive(v)) return {value:'Handoff complete',reason:'Production countdown ended',confidence:'Complete',credible:false};
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
    if(isLive(v)) return section('Published on YouTube',null,
      '<p class="muted">This video is published. Production progress and UAT forecasts no longer apply.</p>'
      + `<details class="technical" data-disclosure="${esc(v.key)}-history"><summary>Recorded production history</summary><p class="muted">Unconfirmed milestones mean historical records are missing, not that the published video is unfinished.</p>${milestones(v).map(m=>milestoneCard(v,m,null)).join('')}</details>`);

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
  function videoProductionRow(v, now) {
    if (isLive(v)) return row(v, "");
    const current=currentProduction(v)[0], f=forecastView(v,now);
    return row(v, `<span class="meta current-label">${esc(current?current.label:stage(v))}${blockedVideo(v)?' · <span class="blocked-word">Blocked / approval pending</span>':''}</span>${milestoneProgress(v)}<span class="meta outlook-line">UAT: ${esc(f.value)}</span>`);
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
    return uniqueVideos(vs).filter(v=>!isLive(v) && (v.youtube||{}).state!=='scheduled' && v.lane!=='done'
      && !(v.lane==='ready' && v.readyFor==='Ben')
      && ['progress','changes','ready','approved'].includes(v.lane));
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
      if(!id || (states[id]||{}).state!=='running') continue;
      const index=all.findIndex(j=>j.id===id), recorded=index>=0?all[index]:{};
      const current={...recorded,id,title:recorded.title||active.title,by:active.worker||active.agent||recorded.by,progress:active.progress||recorded.progress};
      if(index>=0) all[index]=current; else all.push(current);
    }
    const jobState=j=>(states[j.id]||{}).state;
    const running=all.filter(j=>jobState(j)?jobState(j)==='running':j.status==='claimed'),
      queued=all.filter(j=>jobState(j)?['queued','review'].includes(jobState(j)):j.status==='open'),
      held=all.filter(j=>jobState(j)?['waiting','stalled'].includes(jobState(j)):j.status==='blocked');
    const freshRunning=running.filter(j=>{
      const at=Math.max(...[j.claimedAt,(j.progress||{}).at,(j.last||{}).at].map(d=>Date.parse(d||'')).filter(Number.isFinite));
      return Number.isFinite(at) && now>=at && now-at<=QUIET_MIN*MIN;
    });
    const activeRunning=fresh?running:freshRunning, operationalFresh=fresh || freshRunning.length>0;
    const degraded=!fresh || (models.models||[]).some(m=>['red','amber'].includes(m.status));
    const agents=(models.models||[]).filter(m=>AGENTS[m.id] && m.id!=='macbook');
    const noCapacity=queued.length>0 && agents.length>0 && agents.every(m=>m.status==='red');
    const status=!operationalFresh ? {text:'Attention needed',tone:'red'} : activeRunning.length ? {text:degraded?'Running · Limited':'Running',tone:degraded?'amber':'green'}
      : {text:noCapacity || held.length && !queued.length?'Attention needed':'Waiting',tone:noCapacity || held.length && !queued.length?'red':'amber'};
    return {vs,ready,producing,jobs:all,week:scheduledThisWeek(vs,now),fresh:operationalFresh,running:activeRunning,queued,held,status};
  }
  function featureVideo(b, now) {
    const s=overviewModel(b,now), focus=(((b.owb||{}).focus)||[]).map(x=>String(x).includes(':')?String(x):'OWB:'+x);
    const rank=v=>{
      const ready=forBen([v]).length>0, blocked=blockedVideo(v), f=forecastView(v,now), p=progressStats(v), active=currentProduction(v);
      const finalQA=active.some(m=>m.id==='qa') || p.rows.filter(m=>m.id!=='qa').every(completeStage);
      const unresolved=p.rows.filter(m=>!completeStage(m) && (stageView(m).tone==='held' || m.state==='unknown')).length;
      const priority=Number(v.productionPriority ?? v.priority);
      return [ready?0:1,blocked?1:0,f.credible?0:1,f.credible?f.minutes:Infinity,finalQA?0:1,unresolved,
        focus.includes(v.key)?0:1,Number.isFinite(priority)?priority:Infinity,-videoUpdated(v),v.key];
    };
    const candidates=uniqueVideos([...s.ready,...s.producing.filter(v=>v.lane!=='approved')]);
    return candidates.sort((a,b)=>{
      const ar=rank(a),br=rank(b);for(let i=0;i<ar.length;i++){if(ar[i]<br[i])return -1;if(ar[i]>br[i])return 1;}return 0;
    })[0]||null;
  }
  function featuredOutlook(v,now) {
    if(forBen([v]).length) return 'Ready for UAT';
    if(blockedVideo(v)) return 'Blocked';
    const f=forecastView(v,now);
    return f.credible ? `Approximately ${durationText(f.minutes)}` : 'Estimate pending';
  }
  function featuredCard(v,now,producingCount=0) {
    if(!v) return `<p class="overview-empty">${producingCount?'UAT handoffs are complete. Approved videos are moving toward publishing.':'No videos are in production right now. Explore the backlog in Videos.'}</p><a class="overview-empty-link" href="#videos">Open Videos <span aria-hidden="true">›</span></a>`;
    const p=progressStats(v), m=currentProduction(v)[0], ready=forBen([v]).length>0;
    const stageLabel=ready?'Ready for your UAT':m ? m.label+(stageView(m).text==='Awaiting approval'?' approval':'') : 'Unconfirmed';
    const action=ready?((v.watch||{}).url?'Use Watch & review below to open this cut.':'Review delivery incomplete: no watch link is recorded.') : m ? stageView(m).tone==='held'?blockerModel(v,m).action:nextAction(m) : 'The next production step has not been confirmed.';
    return `<a class="featured-video" href="${detailLink(v)}" aria-label="Open ${esc(v.title||'video')} production details">
      <div class="featured-heading">${thumb(v)}<div><h3>${esc(v.title||'Untitled video')}</h3><p>${v.channel==='HOS'?'History of Science':'Orbit With Ben'} · ${kind(v)}</p></div><span class="chev" aria-hidden="true">›</span></div>
      <div class="featured-progress-heading"><span>Milestones completed</span><b>${p.percent}%</b></div>
      <div class="hero-track" role="progressbar" aria-label="Milestones completed, not production time" aria-valuenow="${p.done}" aria-valuemin="0" aria-valuemax="9"><i style="width:${p.percent}%"></i></div>
      <p class="featured-count">${p.done} of 9 milestones complete${p.unknown?` · ${p.unknown} unconfirmed`:''}</p>
      <dl class="featured-facts"><div><dt>Current stage</dt><dd>${esc(stageLabel)}</dd></div><div><dt>Estimated UAT</dt><dd class="${ready?'ready-text':blockedVideo(v)?'held-text':''}">${esc(featuredOutlook(v,now))}</dd></div></dl>
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
      if(/^\d+$/.test(String(job.film||''))) keys.add((job.repo==='hos'?'HOS':'OWB')+':'+String(job.film).padStart(3,'0'));
      for(const v of videos) if(v.key&&(v.jobs||[]).some(x=>x.id===job.id)) keys.add(v.key);
    };
    add(j);
    if(j.recheck_of) {
      const parent=(((b.owb||{}).jobs)||[]).find(x=>x.id===j.recheck_of);
      if(parent) add(parent);
    }
    const rows=[...keys].map(key=>({key,video:videos.find(v=>v.key===key)}));
    const label=row=>{
      const channel=row.key.startsWith('HOS:')?'History of Science':'Orbit With Ben';
      return row.video?`${row.video.title||row.key} · ${channel} · ${kind(row.video)}`:`${channel} · ${row.key.split(':')[1]} · title not recorded`;
    };
    return rows.length?{label:rows.slice(0,2).map(label).join(' / ')+(rows.length>2?` · +${rows.length-2} more videos`:''),count:rows.length}
      :{label:'Studio task · no video linked in the job record',count:0};
  }
  function activityCard(b,now) {
    const s=overviewModel(b,now), jobs=s.running.slice().sort((a,b)=>Number(!!b.urgent)-Number(!!a.urgent));
    // Otherwise retain the publisher's active-job order; a shared job has already been deduplicated.
    const j=jobs[0], footer=`<p class="activity-footer">${s.queued.length} queued · ${s.held.length} on hold</p>`;
    if(!j) return `<section class="overview-activity"><h2>Studio activity</h2><a href="#agents"><div><b>${s.queued.length?'Ready work waiting for dispatch':s.held.length?'No job running · work is on hold':'Studio waiting for next job'}</b>${!s.fresh?'<span>Activity report is stale or missing</span>':''}</div><span class="chev" aria-hidden="true">›</span>${footer}</a></section>`;
    const videoContext=activityVideoContext(b,j);
    const p=recordedTaskProgress(j), start=Date.parse(j.claimedAt||'');
    // Reuse the existing task estimator only with a valid recorded start and valid inputs.
    const e=(!p || p.step<p.of) && Number.isFinite(start) && start<=now && (p && p.step>0 && p.step<p.of || Number.isFinite(+j.estMin) && +j.estMin>0)
      ? etaOf({...j,progress:p || {step:0,of:0}},now) : null;
    const eta=e ? e.over?'Task estimate exceeded':`Task ETA: ~${durationText(e.min)} remaining (estimate)` : 'Task ETA unavailable';
    return `<section class="overview-activity"><h2>Studio activity</h2><a class="active-job-card" href="${jobRoute(j.id)}" aria-label="Open job ${esc(j.id)} in Agents">
      <div><b>${esc(AGENTS[j.by]||j.by||'Unassigned agent')} is working</b><span class="activity-job-id">${esc(j.id)}${jobs.length>1?` · +${jobs.length-1} other active job${jobs.length>2?'s':''}`:''}</span></div><span class="chev" aria-hidden="true">›</span>
      <p class="activity-video"><span>${videoContext.count>1?'Videos':videoContext.count?'Video':'Scope'}</span>${esc(videoContext.label)}</p>
      <p class="activity-action">${esc(clip(j.remaining_action||j.title||'Current action not recorded',160))}</p>
      ${p?`<div class="activity-progress"><div class="hero-track" role="progressbar" aria-label="Recorded task steps, not video completion" aria-valuemin="0" aria-valuemax="${p.of}" aria-valuenow="${p.step}"><i style="width:${pct(p)}%"></i></div><span>${p.step} of ${p.of} steps · ${pct(p)}%</span></div>`:'<p class="activity-progress-missing">Task progress not recorded</p>'}
      <p class="activity-eta">${esc(eta)}</p>${footer}</a></section>`;
  }
  function overview(b, now) {
    const s=overviewModel(b,now), candidate=featureVideo(b,now);
    return `<div class="overview-home"><header class="overview-header"><div><h1>Studio</h1><p>Orbit With Ben · History of Science</p></div><a class="operation-status ${s.status.tone}" href="#agents" aria-label="Studio status: ${s.status.text}. Open Agents"><i aria-hidden="true"></i>${s.status.text}</a></header>
      <div class="overview-stats" aria-label="Studio video counts"><a href="#review"><b>${s.ready.length}</b><span>To review</span></a><a href="#videos&view=producing"><b>${s.producing.length}</b><span>Producing</span></a><a href="#schedule&view=week"><b>${s.week.length}</b><span>This week</span></a></div>
      <section class="overview-feature"><h2>${s.ready.length?'Ready for your review':'Next in production'}</h2>${!s.ready.length?'<p class="muted">Nothing is ready for your review yet.</p>':''}${featuredCard(candidate,now,s.producing.length)}</section>
      ${activityCard(b,now)}</div>`;
  }

  // Working / Queued / Backlog (Ben, 28 Oct): active work is one tap away; All keeps everything with On YouTube.
  function videoGroups(vs) {
    const active = ["progress", "changes", "ready", "approved"];
    return {
      working: vs.filter(v => active.includes(v.lane) && !isLive(v) && isWorking(v)),
      queued: vs.filter(v => active.includes(v.lane) && !isLive(v) && !isWorking(v)),
      backlog: vs.filter(v => v.lane === "upcoming" && !isLive(v)),
      done: vs.filter(v => (v.lane === "done" || isLive(v)) && !v.collapsed && (isLive(v) || !isWorking(v))),
    };
  }

  function videos(b) {
    const vs = (routeView()==='producing' ? producingVideos(((b.tracker||{}).videos)||[]) : uniqueVideos(((b.tracker||{}).videos)||[])).filter(v =>
      (filterCh === "all" || v.channel === filterCh) && (filterType === "all" || v.type === filterType));
    const g = videoGroups(vs);
    for (const key of Object.keys(g)) g[key] = sortVideos(g[key], videoSort, Date.now());
    // Ben, 29 Oct: "Home page saying working on 1, the video page says 0": studio jobs count here too.
    const studio = routeView()!=='producing' && filterType === "all" ? studioJobs(b).filter(j => filterCh === "all" || (j.repo || "owb") === filterCh.toLowerCase()) : [];
    g.working.extra = studio.length;
    const segs = [["all", "All"], ["working", "Working"], ["queued", "Waiting"], ["backlog", "Backlog"]]
      .map(([id, label]) => `<button type="button" data-seg="${id}" class="${seg === id ? "on" : ""}">${label}${id === "all" ? "" : ` <small>${g[id].length + (g[id].extra || 0)}</small>`}</button>`).join("");
    const chips = [["ch", "all", "Both"], ["ch", "OWB", "Orbit"], ["ch", "HOS", "HOS"], ["ty", "long", "Longs"], ["ty", "short", "Shorts"]]
      .map(([k, val, label]) => `<button type="button" data-f="${k}" data-v="${val}" class="${(k === "ch" ? filterCh : filterType) === val ? "on" : ""}">${label}</button>`).join("");
    const list = (items, limit) => items.slice(0, limit).map(v => videoProductionRow(v, Date.now())).join("")
      + (items.length > limit ? `<p class="meta">${items.length - limit} more: pick Orbit or HOS, Longs or Shorts to narrow the list.</p>` : "");
    // A batch job on several videos: the first card carries the job, the others say whose job they share.
    const jobList = items => jobGroups(items).map(([first, ...rest]) => videoProductionRow(first, Date.now())
      + rest.map(v => videoProductionRow(v, Date.now())).join('')).join('');
    const show = id => routeView()==='producing' || seg === "all" || seg === id;
    return `<header class="top"><h1>Videos</h1></header>
      ${routeView()==='producing'?`<p class="list-scope">Producing · ${vs.length} unique videos <a href="#videos">Show all</a></p>`:''}
      <div class="seg">${segs}</div><div class="chips">${chips}</div>
      <label class="sort-control">Sort videos<select id="video-sort"><option value="uat" ${videoSort==='uat'?'selected':''}>Nearest credible UAT</option><option value="updated" ${videoSort==='updated'?'selected':''}>Recently updated</option><option value="stage" ${videoSort==='stage'?'selected':''}>Production stage</option><option value="blocked" ${videoSort==='blocked'?'selected':''}>Blocked first</option></select></label>
      ${show("working") ? section("An agent is on it now", g.working.length + studio.length, (jobList(g.working) + studio.map(jobCard).join("")) || empty("No agent is working this minute.")) : ""}
      ${show("queued") ? section("In production, waiting for its next step", g.queued.length, list(g.queued, 30) || empty("Nothing waiting.")) : ""}
      ${show("backlog") ? section("Backlog", g.backlog.length, list(g.backlog, seg === "backlog" ? 60 : 10) || empty("Backlog is empty.")) : ""}
      ${seg === "all" ? section("On YouTube", g.done.length, list(g.done, 10)) : ""}`;
  }

  // One video, in the hub: where it is, who is on it, what is left, your notes, and its links.
  const JOB_WORD = { claimed: ["green", "Working"], open: ["", "Queued"], blocked: ["amber", "On hold"], done: ["", "Done"] };
  function detail(b, key) {
    const v = ((((b.tracker || {}).videos) || []).find(x => x.key === key));
    const back = `<header class="top"><a class="more back" href="#videos">‹ Back to Videos</a></header>`;
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
    return `${back}<div class="video-heading">${thumb(v)}<div><h1 class="uat-title">${esc(v.title)}</h1>
      <p class="meta">${v.channel==='HOS'?'History of Science':'Orbit With Ben'} · ${kind(v)} ${esc(v.number || "")}${v.version ? " · " + esc(v.version) : ""} · ${esc(stage(v))}${v.airText ? " · " + (yt.state === "live" && yt.privacy === "public" ? "published " : "airs ") + esc(v.airText) : ""}</p>
      </div></div>
      ${links.length ? `<div class="btns">${links.join("")}</div>` : ""}
      ${productionDetail(v, Date.now())}
      <details class="technical video-technical" data-disclosure="${esc(v.key)}-jobs"><summary>Agent work &amp; technical details <span>${jobs.length} jobs</span></summary><div class="technical-body">${v.line?`<p>${esc(v.line)}</p>`:''}${flags}${jobRows}${jobs.map(j=>technicalFields(j)).join('')}</div></details>
      ${notes ? section("Your notes", null, `<ul class="notes">${notes}</ul>`) : ""}`;
  }

  function review(b) {
    const vs = uniqueVideos(((b.tracker || {}).videos) || []);
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

  function agentQueue(b,now) {
    const s=overviewModel(b,now), jobs=s.jobs.filter(j=>['claimed','open','blocked'].includes(j.status)).sort((a,b)=>['claimed','open','blocked'].indexOf(a.status)-['claimed','open','blocked'].indexOf(b.status));
    return `<details class="technical video-technical" data-disclosure="agent-queue" ${selectedJob()?'open':''}><summary>Job queue · ${jobs.length} job${jobs.length===1?'':'s'}</summary><div class="technical-body">${jobs.length?jobs.map(j=>`<article id="job-${esc(j.id)}" class="job ${selectedJob()===j.id?'selected-job':''}" tabindex="-1"><b>${esc(j.id)} · ${esc(j.title || 'Untitled job')}</b><p>Recorded status: ${esc(j.status)}${j.by?' · '+esc(AGENTS[j.by]||j.by):''}</p>${j.remaining_action?`<p>${esc(j.remaining_action)}</p>`:''}${technicalFields(j.hold)}${j.result?`<p>${esc(j.result)}</p>`:''}<details class="technical"><summary>Recorded job metadata</summary>${technicalFields(j)}</details></article>`).join(''):'No queued or active jobs recorded.'}</div></details>`;
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
      <div class="chief-card"><span class="dot ${c.agent ? "green" : "red"}"></span><div><b>Chief: ${esc(c.name || "nobody")}</b>
        <span class="meta">${c.agent ? "Online · coordinating production" : "No Chief up: jobs wait"}</span></div></div>
      ${jobTiles(s.jobs)}
      ${section("Agent team", null, team + '<p class="meta">Green: working now. Amber: online but idle, or not checked in lately. Red: out of usage or failing; its jobs go to the next agent.</p>')}
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
    return `<header class="top"><h1>Schedule</h1></header><p class="meta">Calendar weeks · Monday–Sunday · London time</p>
      ${section("This week · scheduled",actualWeek.length,byDay(actualWeek)||empty("Nothing scheduled this week."))}
      ${routeView()==='week'?'<a class="more" href="#schedule">Full schedule</a>':`${planned.length?section("This week · planned",planned.length,byDay(planned)):''}${section("Next week",next.length,byDay(next)||empty("Nothing yet."))}${section("Later",later.length,byDay(later.slice(0,12))||empty("Nothing yet."))}`}`;
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
      if (sha) lastSha = sha;
      try { const mb = await fetch(MACBOOK + "?t=" + Date.now(), { cache: "no-store" }); macbook = mb.ok ? await mb.json() : null; } catch (e) {}
      if (!uatKey() || !document.getElementById("uat-notes")) render();  // never wipe notes or the player mid-review
    } catch (e) {
      if (!board) { renderedView=""; document.getElementById("view").innerHTML = '<p class="empty" role="status">Could not load the studio data. Retrying automatically.</p>'; }
    }
  }

  // STUDIO_APP_TEST_HOOK
  window.addEventListener("hashchange", () => {
    if(location.hash==="#videos&view=producing") {filterCh="all";filterType="all";seg="all";}
    render(); window.scrollTo(0, 0);
  });
  render();
  poll();
  setInterval(poll, 60 * 1000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) poll(); });
})();
