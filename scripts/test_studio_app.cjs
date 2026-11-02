// Studio app (05_Analytics/kanban/board_site/studio_app.js): Ben's review queue is finished videos only, progress is
// reported steps only, the schedule has one row per slot, and every tab renders from a real board.json.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/studio_app.js'), 'utf8');
const hook = '  // STUDIO_APP_TEST_HOOK';
assert(source.includes(hook), 'studio_app.js keeps its test hook');
const context = {Date, Intl, URLSearchParams, console, location: {hash: ''}, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {overviewModel, featureVideo, scheduledThisWeek, uniqueVideos, producingVideos, featuredOutlook, weekDates, progressStats, currentProduction, stageView, forecastView, sortVideos, videoUpdated, conciseEvidence, uatOutlook, milestoneProgress, productionDetail, renderTab, summary, schedule, progressOf, forBen, stage, tickDoc, canTick, uat, agentLight, readiness, videoGroups, doing, detail, miniLine, etaOf, etaText, macbookState, meterless, poolMeter, jobGroups, inProgress, thumb, overview, setBoard: b => { board = b; }};
})();`, context);
const t = context.test;
const NOW = Date.parse('2026-10-28T20:00:00Z');
const v = (o) => Object.assign({key: 'OWB:001', channel: 'OWB', number: '001', title: 'T', type: 'long', lane: 'progress', jobs: [], youtube: null, air: ''}, o);

// Review is Ben's finished videos only.
const vs = [v({key: 'a', lane: 'ready', readyFor: 'Ben'}), v({key: 'b', lane: 'ready', readyFor: 'Chief'}), v({key: 'c'})];
assert.deepEqual(t.forBen(vs).map(x => x.key), ['a']);
assert.equal(t.stage(vs[1]), 'Waiting on Chief');

// Progress comes from a job working now, never a parked or estimated one.
assert.equal(t.progressOf(v({jobs: [{status: 'blocked', progress: {step: 3, of: 3}}]})), null);
assert.deepEqual(JSON.parse(JSON.stringify(t.progressOf(v({jobs: [{status: 'claimed', progress: {step: 2, of: 5}}]})))), {step: 2, of: 5});

// One row per slot: an approved swap record and the Short on YouTube share 11:30; the YouTube one stays.
const at = '2026-10-29T11:30:00Z';
const rows = t.schedule([v({key: 'OWB:OK:J1', type: 'short', youtube: {state: 'scheduled', publishAt: at}}),
  v({key: 'OWB:023:S', type: 'short', youtube: {state: 'scheduled', publishAt: at, videoId: 'abcdefghijk'}}),
  v({key: 'HOS:010', channel: 'HOS', air: '2026-12-03'}),
  v({key: 'old', youtube: {state: 'live', privacy: 'public', publishAt: '2026-10-01T11:30:00Z'}})], NOW);
assert.deepEqual(rows.map(r => r.v.key), ['OWB:023:S', 'HOS:010']);
assert.equal(rows[1].scheduled, false, 'a planned air date is not shown as scheduled');

// Health: the Mac mini quiet past 75 min reads red.
const quiet = t.summary({tracker: {videos: []}, models: {checkedAt: '2026-10-28T17:00:00Z', models: []}}, NOW);
assert.equal(quiet.health[0], 'red');

// Every tab renders from a real board.json and escapes the data.
const board = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'ai_board.json'), 'utf8'));
board.tracker = {videos: [v({key: 'OWB:019', title: 'Andromeda <script>', lane: 'ready', readyFor: 'Ben',
  watch: {url: 'https://example.com/w', version: 'v06'}})]};
board.owb = {jobs: [{id: 'J1', status: 'claimed', by: 'gemini', title: 'Credit readings'}], day: {doneToday: 4}};
for (const tab of ['overview', 'videos', 'review', 'agents', 'schedule']) {
  const html = t.renderTab(tab, board, NOW);
  assert(!html.includes('<script>'), `${tab} escapes text`);
  assert(html.length > 200, `${tab} renders`);
}
const review = t.renderTab('review', board, NOW);
assert(review.includes('#uat=OWB%3A019') && review.includes('Watch &amp; review v06') || review.includes('Watch & review v06'), 'a review card opens the UAT screen');
assert(t.renderTab('agents', board, NOW).includes('Working on J1: Credit readings'));
assert(t.renderTab('overview', null, NOW).includes('Loading'));
// Ben's tick from the hub is the same document /board sends (tracker_app.js approve / openChangesModal).
const ok = t.tickDoc(v({key: 'OWB:029:S:abc', version: 'v04', ask: {job: 'J0961', what: 'swap'}}), 'ok');
assert.deepEqual([ok.film, ok.version, ok.verdict, ok.fixes.length, ok.note, ok.job, ok.what], ['OWB:029', 'v04', 'ok', 0, '', 'J0961', 'swap']);
const chg = t.tickDoc(v({version: 'v06'}), 'change', '0:38 text does not match the VO\nending too quiet');
assert.deepEqual(JSON.parse(JSON.stringify(chg.fixes)), [{t: '0:38', text: 'text does not match the VO'}, {t: '', text: 'ending too quiet'}]);
assert.equal(chg.note, '0:38 text does not match the VO\nending too quiet');
// Buttons where /board shows them: a long, or a Short with an ask; other Shorts open on the board.
assert(t.canTick(v({})) && t.canTick(v({type: 'short', ask: {job: 'J1'}})) && !t.canTick(v({type: 'short'})));
// UAT screen: a streamable cut plays in the page with a timestamp button; Approve and Request changes are there.
const stream = t.uat(board, 'OWB:019');
assert(!stream.includes('<video'), 'an https link that is not a stream opens outside the page');
board.tracker.videos[0].watch = {url: 'https://studio-kanban.vercel.app/api/watch?v=x', version: 'v06', kind: 'stream'};
const play = t.uat(board, 'OWB:019');
assert(play.includes('<video id="uat-video"') && play.includes('data-stamp') && play.includes('data-ok="OWB:019"') && play.includes('data-chg="OWB:019"'));
board.tracker.videos[0].watch = {url: 'shareddocuments:///x.mp4', version: 'v06', kind: 'files', source: 'iCloud Drive'};
assert(t.uat(board, 'OWB:019').includes('Open v06 in iCloud Drive'), 'an iCloud file opens in Files');
assert(t.uat(board, 'nope').includes('waiting for review any more'));

// Agents: green means working (or the Chief coordinating), amber idle, red out.
assert.deepEqual([...t.agentLight('codex', 1, 'green', false)], ['green', 'Working']);
assert.deepEqual([...t.agentLight('claude', 0, 'green', false)], ['amber', 'Idle'], 'a ready agent with no job is not green');
assert.deepEqual([...t.agentLight('chief', 0, 'green', true)], ['green', 'Coordinating']);
assert.deepEqual([...t.agentLight('cursor', 1, 'red', false)], ['red', 'Out']);

// Videos: Working / Queued / Backlog.
const g = t.videoGroups([v({key: 'w', jobs: [{status: 'claimed', by: 'codex', title: 'cut', progress: {step: 3, of: 5}}]}), v({key: 'q'}), v({key: 'b', lane: 'upcoming'})]);
assert.deepEqual([g.working[0].key, g.queued[0].key, g.backlog[0].key], ['w', 'q', 'b']);
assert(t.doing(g.working[0]).includes('Codex · cut') && t.doing(g.working[0]).includes('<b>60%</b> · 3 of 5'), 'the working card says who, what, and the reported step as a percentage');

// Schedule: a warning only when readiness can't be verified.
assert.equal(t.readiness(v({youtube: {videoId: 'abcdefghijk', state: 'scheduled'}}), NOW + 864e5, NOW), '');
assert.equal(t.readiness(v({}), NOW + 2 * 864e5, NOW), 'Not uploaded to YouTube yet');
assert.equal(t.readiness(v({youtube: {state: 'scheduled', publishAt: 'x'}}), NOW + 864e5, NOW), '', 'a swap YouTube already has scheduled is not flagged');
assert.equal(t.readiness(v({flags: [{kind: 'approved', text: 'no read-back'}]}), NOW + 864e5, NOW), 'no read-back');
assert(t.renderTab('schedule', board, NOW).length > 100);
// One meaning of working: the video flag alone is not an agent working (11 / 1 / 0 no longer disagree).
const flagOnly = t.summary({tracker: {videos: [v({key: 'f', working: true})]}, models: {checkedAt: new Date(NOW).toISOString(), models: []}, owb: {jobs: []}}, NOW);
assert.equal(flagOnly.working.length, 0);
assert.equal(flagOnly.jobs.working, 0);
const ov = t.renderTab('overview', {tracker: {videos: []}, models: {checkedAt: new Date(NOW).toISOString()}, owb: {jobs: [{id: 'J1', status: 'claimed', by: 'gemini', title: 'x'}]}}, NOW);
assert(ov.includes('1 active job') && !ov.includes('J1') && !ov.includes('Agents working now'), 'studio jobs stay counted in compact activity without raw cards');
// Every video opens in the hub, never the old board; the detail shows the agent work and its reasons.
for (const tab of ['overview', 'videos', 'review', 'agents', 'schedule']) assert(!t.renderTab(tab, board, NOW).includes('/board'), `${tab} never links to /board`);
const det = t.detail({tracker: {videos: [v({key: 'OWB:005', line: 'Held up by the audit', jobs: [
  {id: 'J1', status: 'blocked', by: 'codex', title: 'audit', hold: {condition: 'after the Chief review'}},
  {id: 'J2', status: 'claimed', by: 'gemini', title: 'build', remaining_action: 'grade', progress: {step: 2, of: 4}}]})]}}, 'OWB:005');
assert(det.indexOf('J2') < det.indexOf('J1'), 'working job first');
assert(det.includes('after the Chief review') && det.includes('2 of 4') && det.includes('Held up by the audit'));
assert(t.detail({tracker: {videos: []}}, 'x').includes('on the board any more'));
// The Mac mini line: working, or between jobs with a queue, never a silent zero.
const s1 = t.summary({tracker: {videos: []}, models: {checkedAt: new Date(NOW).toISOString(), runner: {state: 'ready'}}, owb: {jobs: [{id: 'J9', status: 'open'}]}}, NOW);
assert(t.miniLine(s1, {owb: {jobs: [{id: 'J9', status: 'open'}]}}).includes('between jobs · 1 queued'));
assert(t.miniLine(s1, {owb: {jobs: [{id: 'J8', status: 'claimed', by: 'codex', title: 'disk'}]}}).includes('Mac mini working: Codex on J8'));
// ETA: the pace of reported steps, else the typical time for the kind; overruns say so.
const start = new Date(NOW - 30 * 6e4).toISOString();
t.setBoard({owb: {jobs: [{id: 'J7', claimedAt: start, estMin: 85}]}});
assert.equal(t.etaOf({id: 'J7', progress: {step: 1, of: 4}}, NOW).min, 90, '30 min for 1 of 4 steps -> about 90 min left');
assert.equal(t.etaOf({id: 'J7', progress: {step: 0, of: 4}}, NOW).min, 55, 'no step yet -> typical 85 min less 30 spent');
assert(t.etaText(t.etaOf({id: 'J7', progress: {step: 3, of: 4}}, NOW)).startsWith('about 10 min left (done ~'));
t.setBoard({owb: {jobs: [{id: 'J7', claimedAt: new Date(NOW - 200 * 6e4).toISOString(), estMin: 85}]}});
assert.equal(t.etaText(t.etaOf({id: 'J7'}, NOW)), 'taking longer than usual');
assert.equal(t.etaOf({id: 'J8'}, NOW), null, 'no start time, no ETA');
// MacBook: its own report says why it waits; silence reads as asleep, never as fine.
assert.equal(t.macbookState(null, NOW)[1], 'No report');
assert.deepEqual([...t.macbookState({at: new Date(NOW - 5 * 6e4).toISOString(), state: 'waiting', why: ['on battery']}, NOW)], ['amber', 'Waiting', 'on battery']);
assert.equal(t.macbookState({at: new Date(NOW - 5 * 6e4).toISOString(), state: 'working', job: 'J1122'}, NOW)[2], 'on J1122');
assert(t.macbookState({at: new Date(NOW - 90 * 6e4).toISOString(), state: 'idle'}, NOW)[2].includes('asleep, lid closed or off'));
// Credits: Grok, Claude and Gemini have no meter; the tile says up or out, and when a flagged one is back.
assert.deepEqual([...t.meterless({agent: 'chief', up: false, until: '2026-10-30T07:00:00Z'}, null, NOW)], ['red', 'Out', 'back Fri 07:00']);
assert.deepEqual([...t.meterless({agent: 'claude', up: true}, null, NOW)], ['green', 'Up', 'no meter published']);
assert(t.renderTab('agents', board, NOW).includes('Grok'));
// One job over several videos is one card on Overview, counted once.
const batch = {status: 'claimed', id: 'J1100', by: 'codex', title: 'batch C'};
const ovb = t.renderTab('overview', {tracker: {videos: [v({key: 'a', number: '027', jobs: [batch]}), v({key: 'b', number: '028', jobs: [batch]}),
  v({key: 'c', number: '027', type: 'short', jobs: [batch]})]}, models: {checkedAt: new Date(NOW).toISOString()}, owb: {jobs: [batch]}}, NOW);
assert(ovb.includes('1 active job') && !ovb.includes('J1100'), 'a shared job is counted once without exposing its title');
assert.equal(t.jobGroups([v({key: 'a', jobs: [batch]}), v({key: 'b', jobs: [batch]})]).length, 1);
// Videos: a batch job shows its progress once; the other videos say they share it.
const vb = {tracker: {videos: [v({key: 'a', number: '027', jobs: [batch]}), v({key: 'b', number: '028', jobs: [batch]})]}};
const vt = t.renderTab('videos', vb, NOW);
assert.equal((vt.match(/class="doing"/g) || []).length, 0, 'task percentages are kept in Agent work, not video milestone rows');
assert(vt.includes('027') && vt.includes('028') && vt.includes('milestones complete'));
// Videos counts a running studio job too, so it matches Overview's Agents working now.
const vsj = t.renderTab('videos', {tracker: {videos: []}, owb: {jobs: [{id: 'J1199', status: 'claimed', by: 'cursor', title: 'Shorts fix'}]}}, NOW);
assert(vsj.includes('Studio job · not one video') && vsj.includes('Working <small>1</small>'), 'Videos shows and counts the studio job');
// A public video is published, whatever follow-up jobs it has; private ones never ask YouTube for a thumbnail.
const pub = v({key: 'pub', lane: 'progress', youtube: {videoId: 'abcdefghijk', privacy: 'public', state: 'live'}, jobs: [{id: 'J9', status: 'open'}]});
const priv = v({key: 'priv', lane: 'progress', youtube: {videoId: 'bcdefghijkl', privacy: 'private', state: 'scheduled'}});
assert.deepEqual(t.inProgress([pub, priv]).map(x => x.key), ['priv']);
const gg = t.videoGroups([pub, priv]);
assert.deepEqual([gg.queued.map(x => x.key), gg.done.map(x => x.key)], [['priv'], ['pub']]);
assert(t.thumb(pub).includes('i.ytimg.com') && !t.thumb(priv).includes('i.ytimg.com'));
// Credit bars: a plan allowance or the month's refill makes a bar; a % pool keeps its reset date.
const flow = t.poolMeter('flow', {unit: 'credits', latest: {left: 20870, at: new Date(NOW).toISOString()}}, {tiers: {flow: [{name: 'Google AI Ultra $200 tier', allow: 25000, current: true}]}}, NOW);
assert.equal(flow.fig, '83%'); assert(flow.note.includes('of 25,000'));
const vx = t.poolMeter('vertex', {unit: 'GBP', latest: {left: 69.48, at: new Date(NOW).toISOString()}, series: [['2026-10-02T08:00Z', 100], ['2026-10-20T08:00Z', 80]]}, {}, NOW);
assert.equal(vx.fig, '69%'); assert(vx.note.includes('of £100 this month'));
const cx = t.poolMeter('codex', {unit: '%', latest: {left: 40, total: 100, at: new Date(NOW).toISOString(), note: 'weekly 60% used, resets Wed 04 Nov 06:36Z'}}, {}, NOW);
assert.equal(cx.fig, '40%'); assert(cx.note.includes('resets Wed 04 Nov 06:36Z'), cx.note);
assert.equal(t.poolMeter('claude', undefined, {}, NOW), null, 'no reading, no bar');
const ag = t.renderTab('agents', {tracker: {videos: []}, models: {chiefChain: [{agent: 'claude', up: true}]}, credits: {pools: {cursor: {unit: '%', latest: {left: 0, total: 100, at: new Date(NOW).toISOString(), note: 'weekly resets Oct 29'}}}}}, NOW);
assert((ag.match(/<span>Grok<\/span><b class="red">0%/) || []).length === 1, 'Grok shows the shared Cursor weekly pool');


// Milestones and ETA share the same producer evidence on Overview and video detail.
const tracked = v({production: {asOf: new Date(NOW).toISOString(), milestones: [{id:'edit', label: 'Edit <unsafe>', state: 'done'}, {id:'qa', label: 'Chief QA', state: 'doing'}],
  eta: {state: 'estimated', confidence: 'low', lowerMinutes: 15, upperMinutes: 25, criticalPath: ['qa'], basedOn: 'Git stage transitions'}}});
assert(t.milestoneProgress(tracked, true).includes('11%'));
assert(t.productionDetail(tracked, NOW).includes('~15m–25m'));
assert(t.productionDetail(tracked, NOW).includes('&lt;unsafe&gt;'));
assert(!t.productionDetail(tracked, NOW).includes('<unsafe>'));
assert(t.uatOutlook(v({}), NOW).detail.includes('not been published'));
const blockedProduction = v({production: {milestones: [], eta: {state: 'unavailable', reasons: ['Flow <manual>', 'credit reset']}}});
assert(t.productionDetail(blockedProduction, NOW).includes('Flow &lt;manual&gt;') && t.productionDetail(blockedProduction, NOW).includes('credit reset'));
assert(t.overview({tracker: {videos: [tracked]}}, NOW).includes('milestones complete'));
assert(!t.renderTab('review', {tracker: {videos: [tracked, blockedProduction]}}, NOW).includes('15–25 min'));

assert(t.uatOutlook(tracked, NOW + 80 * 6e4).detail.includes('fresh production'));
assert(t.uatOutlook(tracked, NOW + 26 * 6e4).detail.includes('range exceeded'));

// V2: nine unique milestones, independent from task progress and approval waits.
const nine = ['topic','script','sources','vo','shots','picture','edit','thumbs','qa'];
const v2 = v({jobs:[{id:'dup',status:'claimed',progress:{step:99,of:100}}],production:{asOf:new Date(NOW).toISOString(),
  milestones:nine.map((id,i)=>({id,label:id,state:i<3?'done':i===5?'review':'unknown',owner:id==='picture'?'chief':'',
    evidence:id==='picture'?'J1191 complete (parked for Chief picture PASS): all 101/101 Flow v03 rows minted and KEEP…':'',dependsOn:[]})),
  activeStages:['picture'],eta:{state:'unavailable',reasons:['Edit: fewer than 3 comparable historical stages','Chief QA: fewer than 3 comparable historical stages']}}});
assert.equal(t.progressStats(v2).percent,33);
assert.equal(t.progressStats(v2).done,3);
v2.production.milestones.push(v2.production.milestones[0]);
assert.equal(t.progressStats(v2).done,3,'duplicate milestones never inflate counts');
assert.equal(t.currentProduction(v2)[0].id,'picture');
assert.equal(t.stageView(t.currentProduction(v2)[0]).text,'Awaiting approval');
assert(t.productionDetail(v2,NOW).includes('101/101 Flow shots generated'));
assert(t.productionDetail(v2,NOW).includes('View technical details'));
assert(t.productionDetail(v2,NOW).includes('J1191 complete (parked for Chief picture PASS)'));
assert.equal((t.productionDetail(v2,NOW).match(/data-stage="[^"]+"[^>]* open/g)||[]).length,1,'only current stage expanded initially');
assert(t.forecastView(v2,NOW).value==='Pending');
const unassigned = v({production:{milestones:nine.map(id=>({id,state:'unknown'}))}});
assert.equal(t.currentProduction(unassigned).length,0,'unknown is not a current stage');
const approvalDone = v({production:{milestones:[{id:'picture',state:'done',awaitingApproval:true}]}});
assert.equal(t.progressStats(approvalDone).done,0);
const pending1=v({key:'pending1'}),pending2=v({key:'pending2'});
assert.deepEqual(t.sortVideos([pending1,pending2],'uat',NOW).map(x=>x.key),['pending1','pending2']);
assert.equal(t.videoUpdated(v({production:{asOf:new Date(NOW).toISOString()}})),0,'publisher time is not a production update');
assert.equal(t.forecastView(v({...tracked,lane:'done'}),NOW).value,'Handoff complete');
assert(t.detail({tracker:{videos:[v2]}},v2.key).includes('href="#videos"'));
console.log('Studio V2 unit checks OK');

const later = v({key:'later',production:{asOf:new Date(NOW).toISOString(),milestones:[],eta:{state:'estimated',confidence:'low',lowerMinutes:30,upperMinutes:60}}});
const sooner = v({key:'sooner',production:{asOf:new Date(NOW).toISOString(),milestones:[],eta:{state:'estimated',confidence:'low',lowerMinutes:10,upperMinutes:20}}});
assert.deepEqual(t.sortVideos([pending1,later,pending2,sooner],'uat',NOW).map(x=>x.key),['sooner','later','pending1','pending2']);
const updated = v({key:'updated',production:{milestones:[{id:'edit',state:'doing',source:{updatedAt:new Date(NOW).toISOString()}}]}});
assert.deepEqual(t.sortVideos([pending1,updated],'updated',NOW).map(x=>x.key),['updated','pending1']);
assert(t.forecastView(tracked,NOW+80*6e4).value==='Pending');
console.log('Studio app regression and V2 checks OK');

// V3 shared video selectors, calendar weeks, health and deterministic featured selection.
const freshModels={checkedAt:new Date(NOW).toISOString(),models:[]};
const makeBoard=videos=>({tracker:{videos},models:freshModels,owb:{jobs:[]}});
const shared={id:'Jshared',status:'claimed',by:'codex',claimedAt:new Date(NOW).toISOString()};
const producingA=v({key:'OWB:101',jobs:[shared]}), producingB=v({key:'HOS:101',channel:'HOS',jobs:[shared]});
const publicFollowup=v({key:'OWB:102',youtube:{videoId:'abcdefghijk',privacy:'public',state:'live'},jobs:[shared]});
const scheduled=v({key:'OWB:103',lane:'done',youtube:{videoId:'bcdefghijkl',state:'scheduled',publishAt:'2026-10-30T18:00:00Z'}});
const readyFilm=v({key:'OWB:104',lane:'ready',readyFor:'Ben'});
const db=makeBoard([producingA,producingA,producingB,publicFollowup,scheduled,readyFilm,readyFilm]);
const om=t.overviewModel(db,NOW);
assert.equal(om.ready.length,1);assert.equal(om.producing.length,2);assert.equal(om.running.length,1);assert.equal(om.week.length,1);
assert.equal(t.featureVideo(db,NOW).key,'OWB:104','finished Ben review comes first');
assert.equal(t.featureVideo(makeBoard([pending1,pending2,sooner,later]),NOW).key,'sooner','credible earliest UAT outranks pending');
const nearlyDone=v({key:'blocked',production:{milestones:nine.map((id,i)=>({id,state:i<8?'done':'review'})),activeStages:['qa']}});
assert.equal(t.featureVideo(makeBoard([nearlyDone,producingA]),NOW).key,producingA.key,'nominal progress does not promote a blocked film');
const focused=makeBoard([v({key:'OWB:202'}),v({key:'OWB:201'})]);focused.owb.focus=['202'];
assert.equal(t.featureVideo(focused,NOW).key,'OWB:202','recorded focus breaks readiness ties');
assert.equal(t.featureVideo(makeBoard([v({key:'z'}),v({key:'a'})]),NOW).key,'a','fallback has an explicit stable key');
assert.equal(t.featuredOutlook(pending1,NOW),'Estimate pending');
const staleBoard={...makeBoard([v({key:'stale',jobs:[{...shared,claimedAt:new Date(NOW-80*6e4).toISOString()}]})]),models:{checkedAt:new Date(NOW-80*6e4).toISOString()}};
assert.equal(t.overviewModel(staleBoard,NOW).status.text,'Attention needed');
assert(!t.overview(staleBoard,NOW).includes('Codex is working'));
assert.equal(t.overviewModel({...db,models:staleBoard.models},NOW).status.text,'Running · Limited','fresh job activity is independent of a stale relay report');
assert.equal(t.overviewModel({...db,models:{...freshModels,models:[{id:'claude',status:'red'}]}},NOW).status.text,'Running · Limited');
assert(t.overview(db,NOW).includes('Codex is working'));
assert.equal(t.overviewModel(makeBoard([]),NOW).status.text,'Waiting');
const weekNow=Date.parse('2026-11-02T12:00:00Z');
const slot=(key,at,state='scheduled')=>v({key,lane:'done',youtube:{state,publishAt:at}});
const weekVideos=[slot('start','2026-11-02T00:00:00Z'),slot('end','2026-11-08T23:59:00Z'),slot('next','2026-11-09T00:00:00Z'),
  slot('live','2026-11-04T18:00:00Z','live'),v({key:'planned',air:'2026-11-05'})];
assert.deepEqual(t.scheduledThisWeek(weekVideos,weekNow).map(r=>r.v.key),['start','end']);
assert.equal(t.weekDates(Date.parse('2026-07-05T23:30:00Z')).start,'2026-07-06','calendar uses London day across BST midnight');
context.location.hash='#videos&view=producing';
assert(t.renderTab('videos',db,NOW).includes('Producing · 2 unique videos'));
context.location.hash='#schedule&view=week';
assert(t.renderTab('schedule',db,NOW).includes('This week · scheduled <span class="n">1</span>'));
context.location.hash='';
assert.equal((t.overview(db,NOW).match(/class="featured-video"/g)||[]).length,1);
assert(!t.overview(db,NOW).includes('How this estimate works'));
console.log('Studio V3 selector and Overview checks OK');

const identicalSlot=[slot('OWB:s1','2026-11-04T18:00:00Z'),slot('OWB:s2','2026-11-04T18:00:00Z')];
identicalSlot[0].youtube.videoId='abcdefghijk';identicalSlot[1].youtube.videoId='bcdefghijkl';
assert.equal(t.scheduledThisWeek(identicalSlot,weekNow).length,2,'distinct videos sharing a slot are still two scheduled videos');
const ytReady=v({key:'physical',youtube:{videoId:'abcdefghijk',state:'private'}});
assert.equal(t.uniqueVideos([ytReady,{...ytReady,key:'alias'},ytReady]).length,1);
assert.equal(t.uniqueVideos([v({key:'same'}),v({key:'same',youtube:{videoId:'abcdefghijk'}})]).length,1);
assert.equal(t.producingVideos([v({key:'backlog',lane:'upcoming',production:nearlyDone.production})]).length,0,'backlog milestones do not silently promote a video into active production');
