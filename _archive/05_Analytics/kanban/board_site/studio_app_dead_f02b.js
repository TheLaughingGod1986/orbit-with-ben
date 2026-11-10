// Archived from 05_Analytics/kanban/board_site/studio_app.js under J2464 (row F-02b: 15 dead functions).
  function miniLine(s, b) {
    const jobs = ((b.owb || {}).jobs) || [], r = s.runner || {};
    const live = jobs.find(j => j.status === "claimed");
    const left = live ? etaText(etaOf(live, Date.now())) : "";
    const text = live ? `Mac mini working: ${AGENTS[live.by] || live.by} on ${live.id} · ${clip(live.remaining_action || live.title, 60)}${left ? " · " + left : ""}`
      : s.jobs.queued ? `Mac mini between jobs · ${s.jobs.queued} queued, the next starts within minutes`
      : r.state ? "Mac mini idle · nothing queued" : "";
    return text ? `<p class="mini ${live ? "on" : ""}"><i></i>${esc(text)}</p>` : "";
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
  function nextVideoTask(b,v,now) {
    if(!v || forBen([v]).length || isLive(v) || (v.youtube||{}).state==='scheduled' || unconfirmedCut(v) || ['approved','done'].includes(v.lane)) return null;
    const s=overviewModel(b,now), workflow=b.workflow||{}, fresh=t=>Number.isFinite(Date.parse(t||''))&&now>=Date.parse(t)&&now-Date.parse(t)<=10*MIN;
    const reportFresh=[b.publishedAt,workflow.at,(b.models||{}).checkedAt].some(fresh), dispatchFresh=fresh(workflow.at);
    const m=unconfirmedCut(v)?relatedStage(v):currentProduction(v)[0], stage=id=>({facts:'sources',thumbnails:'thumbs'}[id]||id);
    const all=new Map(s.jobs.map(j=>[j.id,j]));
    for(const j of [...(v.jobs||[]),...((m||{}).jobs||[])]) if(j.id&&!all.has(j.id)) all.set(j.id,j);
    const own=new Set(((m||{}).jobs||[]).map(j=>j.id));
    const linked=[...all.values()].filter(j=>activityVideoContext(b,j).keys.includes(v.key)||own.has(j.id));
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
    if(!ctx||!ctx.count) return {compact:true, text:(ctx&&ctx.label)||'Studio task · no video linked in the job record'};
    if(ctx.count===1) return {compact:false, text:ctx.label};
    return {compact:true, text:`${ctx.count} videos linked`};
  }
  function p24BlockedWhy(f) {
    if(f.blockedWhy) return f.blockedWhy;
    const items=f.items||[];
    const wait=items.find(j=>j.waitKind==='after')||items.find(j=>j.waitKind||j.status==='blocked'||(j.after&&j.status!=='done'));
    return (wait&&wait.why)||'';
  }
  function p24FocusFilms(b) {
    const p=b&&b.progress24h; if(!p) return [];
    return p24MergeFilms(p.films,p.moved).filter(f=>p24InFocus(f.film, p24FocusSet(b)));
  }
  function p24NextLive(p) {
    const next=((p&&p.glance)||{}).nextLive||[];
    const rows=next.slice(0,4);
    if(!rows.length) return '';
    return `<section class="overview-next-live" aria-label="Next to go live"><h2>Next to go live</h2><div class="ov-card p24-next"><ol class="p24-next-list">${rows.map(v=>{
      const when=v.atLondon||v.at||'';
      return `<li><span class="p24-next-when">${esc(when)}</span><span class="p24-title wrap">${esc(v.title||'')}</span></li>`;
    }).join('')}</ol></div></section>`;
  }
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
    return s.replace(/\s*\([^)]*heartbeat[^)]*\)/gi,'').replace(/\bheartbeat\b/gi,'check-in').replace(/\s{2,}/g,' ').trim()||'down';
  }
  function agentLines(b) {
    const q=(b&&b.queueForecast)||{};
    const rows=(q.agents||[]).filter(a=>!a.up||a.now||a.queued).map(a=>{
      const name=AGENTS[a.agent]||a.agent;
      if(!a.up) return `<li><span class="p24-film">${esc(name)}</span> <span class="p24-title wrap muted">Not available · ${esc(plainWhy(a.why))}</span></li>`;
      const on=a.now?`on ${esc(a.now)} · free about ${esc(qWhen(a.freeAt))}`:'free now';
      const line=a.queued?` · ${a.queued} in line, clear about ${esc(qWhen(a.clearAt))}`:'';
      return `<li><span class="p24-film">${esc(name)}</span> <span class="p24-title wrap">${on}${line}</span></li>`;
    }).join('');
    return rows?`<section class="overview-agents" aria-label="Agents and their lines"><h2>Agents and their lines</h2><div class="ov-card mc-agents"><ul class="p24-list mc-agent-list">${rows}</ul>${q.note?`<p class="muted p24-note">${esc(q.note)}</p>`:''}</div></section>`:'';
  }
  function agentTraffic(a, modelStatus) {
    const ms=(modelStatus&&modelStatus[a.agent])||{};
    if(!a.up||ms.status==='red') return {light:'red', word:'Down'};
    if(a.now) return {light:'green', word:'Working'};
    if((a.queued||0)>0) return {light:'amber', word:'Waiting'};
    return {light:'red', word:'Idle'};
  }
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
