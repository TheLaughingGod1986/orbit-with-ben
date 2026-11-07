// Studio app (05_Analytics/kanban/board_site/studio_app.js): Ben's review queue is finished videos only, progress is
// reported steps only, the schedule has one row per slot, and every tab renders from a real board.json.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/studio_app.js'), 'utf8');
const hook = '  // STUDIO_APP_TEST_HOOK';
assert(source.includes(hook), 'studio_app.js keeps its test hook');
const context = {Date, Intl, URLSearchParams, console, location: {hash: ''}, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {normalizeCut,kind,unconfirmedCut,reviewQueueInfo,activityVideoContext,stageExplanation, stageExplanationHtml, milestoneCard, blockerJobs, blockerModel, blockerGuide, blockerReason, currentStageCard, videoProductionRow, activityCard, recordedTaskProgress, overviewModel, featureVideo, featuredCard, scheduledThisWeek, uniqueVideos, producingVideos, featuredOutlook, weekDates, progressStats, currentProduction, stageView, forecastView, sortVideos, videoUpdated, conciseEvidence, uatOutlook, milestoneProgress, productionDetail, renderTab, summary, schedule, progressOf, forBen, stage, tickDoc, canTick, uat, agentLight, readiness, videoGroups, videoLane, listingLine, isScheduledNotPublic, isQa, needsBenWatch, doing, detail, miniLine, etaOf, etaText, macbookState, meterless, poolMeter, jobGroups, inProgress, thumb, overview, forecastLine, agentLines, agentsCards, machinesCard, plainWhy, qWhen, progressCard, p24FilmCard, p24FilmHasActiveWork, p24MergeFilms, p24NextLive, workingOnNow, p24Totals, p24HydrateFilmItems, p24SortFilmItems, setBoard: b => { board = b; }};
})();`, context);
const t = context.test;
const NOW = Date.parse('2026-10-28T20:00:00Z');
const v = (o) => Object.assign({key: 'OWB:001', channel: 'OWB', number: '001', title: 'T', type: 'long', lane: 'progress', jobs: [], youtube: null, air: ''}, o);

// Review is Ben's finished videos only.
const vs = [v({key: 'a', lane: 'ready', readyFor: 'Ben', watch: {url: 'https://x/api/watch?v=a'}}), v({key: 'b', lane: 'ready', readyFor: 'Chief'}), v({key: 'c'}),
  v({key: 'd', lane: 'ready', readyFor: 'Ben'})];  // d: no video attached yet, so not shown to Ben
assert.deepEqual(t.forBen(vs).map(x => x.key), ['a']);
assert.equal(t.videoLane(vs[1]), 'qa', 'Chief-ready is agent QA, not a Ben blocker');
assert.equal(t.stage(vs[1]), 'In review');

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

// Videos: nine exclusive lanes (Ben, 7 Nov 2026). Later stages win; only UAT needs Ben.
const g = t.videoGroups([v({key: 'w', jobs: [{status: 'claimed', by: 'codex', title: 'cut', progress: {step: 3, of: 5}}]}), v({key: 'q'}), v({key: 'b', lane: 'upcoming'})]);
assert.deepEqual([g.progress[0].key, g.todo[0].key, g.backlog[0].key], ['w', 'q', 'b']);
assert(t.doing(g.progress[0]).includes('Codex · cut') && t.doing(g.progress[0]).includes('<b>60%</b> · 3 of 5'), 'the working card says who, what, and the reported step as a percentage');
// UAT OK → Passed (ready to schedule); UAT notes → In progress (not UAT, not Passed).
const passedCut = v({key: 'ok', lane: 'approved', listing: {complete: true, missing: [], status: 'Ready to upload'}});
const uatCut = v({key: 'watch', lane: 'ready', readyFor: 'Ben', watch: {url: 'https://x/api/watch?v=watch', version: 'v02'}});
const notesCut = v({key: 'fix', lane: 'changes', version: 'v02', checkId: 'fix', check: {verdict: 'change', version: 'v02', handled: false}});
assert.equal(t.videoLane(passedCut), 'passed');
assert.equal(t.stage(passedCut), 'Ready to upload');
assert.equal(t.listingLine(passedCut) || t.stage(passedCut), 'Ready to upload');
assert.equal(t.videoLane(uatCut), 'uat');
assert.equal(t.stage(uatCut), 'Ready for you');
assert.equal(t.videoLane(notesCut), 'progress');
assert.equal(t.stage(notesCut), 'Fixing your changes');
assert.deepEqual(t.videoGroups([passedCut, uatCut, notesCut]).uat.map(x => x.key), ['watch']);
assert.deepEqual(t.videoGroups([passedCut, uatCut, notesCut]).passed.map(x => x.key), ['ok']);
assert.deepEqual(t.videoGroups([passedCut, uatCut, notesCut]).progress.map(x => x.key), ['fix']);
// Scheduled needs a real publishAt; approved without one stays Passed (never invent a date).
assert.equal(t.videoLane(v({key: 'sched-no-at', lane: 'approved', youtube: {state: 'scheduled'}})), 'passed');
assert.equal(t.videoLane(v({key: 'sched-at', lane: 'approved', youtube: {state: 'scheduled', publishAt: '2026-11-12T18:00:00Z'}})), 'scheduled');
assert.equal(t.stage(v({key: 'sched-at', lane: 'approved', youtube: {state: 'scheduled', publishAtLondon: 'Wed 12 Nov 18:00'}})), 'Scheduled for Wed 12 Nov 18:00 London');
// QA is agent-owned; Passed with a live upload job stays Passed (ready to schedule).
assert.equal(t.videoLane(v({key: 'chief-qa', lane: 'ready', readyFor: 'Chief'})), 'qa');
assert.equal(t.videoLane(v({key: 'pass-up', lane: 'approved', jobs: [{status: 'claimed', by: 'cursor', title: 'Upload 032', kind: 'studio'}]})), 'passed');
const videosHtml = t.renderTab('videos', {tracker: {videos: [passedCut, uatCut, notesCut]}}, NOW);
assert(videosHtml.includes('Only UAT needs you') && videosHtml.includes('Passed') && videosHtml.includes('ready to schedule'), 'Videos copy names the UAT → Passed loop');
assert(videosHtml.includes('Needs your review') && videosHtml.includes('Watch &amp; review') || videosHtml.includes('Watch & review'), 'UAT lane cards feel like they need Ben');
// Nine lane chips in locked 3×3 order (count above label); no wrapping "All" tile.
const laneChipOrder = [...videosHtml.matchAll(/data-seg="([^"]+)"/g)].map(m => m[1]);
assert.deepEqual(laneChipOrder, ['backlog', 'todo', 'progress', 'qa', 'uat', 'passed', 'scheduled', 'live', 'postlive'], 'Videos lane chips stay in locked 3×3 order');
assert(videosHtml.includes('<b>') && videosHtml.includes('<span>Backlog</span>'), 'lane chips keep big counts above labels');
assert(!/To do[\s\S]*Needs your review/.test(videosHtml) || videosHtml.includes('UAT'), 'Ben review CTA sits in UAT');

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
assert(ov.includes('J1') && ov.includes('active-job-card') && !ov.includes('Agents working now'), 'the compact activity card opens its actual job');
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
assert(ovb.includes('J1100') && !ovb.includes('other active job'), 'a shared job is shown once');
assert.equal(t.jobGroups([v({key: 'a', jobs: [batch]}), v({key: 'b', jobs: [batch]})]).length, 1);
// Videos: a batch job shows its progress once; the other videos say they share it.
const vb = {tracker: {videos: [v({key: 'a', number: '027', jobs: [batch]}), v({key: 'b', number: '028', jobs: [batch]})]}};
const vt = t.renderTab('videos', vb, NOW);
assert.equal((vt.match(/class="doing"/g) || []).length, 0, 'task percentages are kept in Agent work, not video milestone rows');
assert(vt.includes('027') && vt.includes('028') && vt.includes('milestones complete'));
// Videos counts a running studio job too, so it matches Overview's Agents working now.
const vsj = t.renderTab('videos', {tracker: {videos: []}, owb: {jobs: [{id: 'J1199', status: 'claimed', by: 'cursor', title: 'Shorts fix'}]}}, NOW);
assert(vsj.includes('Studio job · not one video') && vsj.includes('data-seg="progress"') && vsj.includes('<b>1</b><span>In progress</span>'), 'Videos shows and counts the studio job under In progress');
// A public video is published, whatever follow-up jobs it has; private ones never ask YouTube for a thumbnail.
const pub = v({key: 'pub', lane: 'progress', youtube: {videoId: 'abcdefghijk', privacy: 'public', state: 'live'}, jobs: [{id: 'J9', status: 'open'}]});
const priv = v({key: 'priv', lane: 'progress', youtube: {videoId: 'bcdefghijkl', privacy: 'private', state: 'scheduled', publishAt: '2026-11-12T18:00:00Z'}});
assert.deepEqual(t.inProgress([pub, priv]).map(x => x.key), [], 'Live and Scheduled are not overview in-progress');
const gg = t.videoGroups([pub, priv]);
assert.deepEqual([gg.scheduled.map(x => x.key), gg.live.map(x => x.key), gg.postlive.map(x => x.key)], [['priv'], [], ['pub']]);
// Post-live = public with open work; Live = public with nothing left; Scheduled needs publishAt (not Post-live).
const sched = v({key: 'sched', lane: 'done', youtube: {videoId: 'cdefghijklm', privacy: 'private', state: 'scheduled', publishAt: '2026-11-12T11:30:00Z'}, jobs: [{id: 'J8', status: 'blocked'}]});
const doneLive = v({key: 'quiet', lane: 'done', youtube: {videoId: 'defghijklmn', privacy: 'public', state: 'live'}, jobs: [{id: 'J7', status: 'done'}]});
const pl = t.videoGroups([sched, doneLive]);
assert.deepEqual([pl.scheduled.map(x => x.key), pl.live.map(x => x.key), pl.postlive.map(x => x.key)], [['sched'], ['quiet'], []]);
assert(t.renderTab('videos', {tracker: {videos: [sched, doneLive]}}, NOW).includes('On YouTube · waiting to go public'));
assert(t.renderTab('videos', {tracker: {videos: [pub]}}, NOW).includes('Public · improvements still open'));
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
const trackedBoard={tracker: {videos: [tracked]}};
assert(t.featuredCard(t.featureVideo(trackedBoard, NOW), NOW, 1).includes('milestones complete'));
assert(!t.overview(trackedBoard, NOW).includes('milestones complete'),'Overview home no longer embeds milestone feature copy');
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
const readyFilm=v({key:'OWB:104',lane:'ready',readyFor:'Ben',watch:{url:'https://x/api/watch?v=104'}});
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
assert.equal((t.overview(db,NOW).match(/class="featured-video"/g)||[]).length,0,'Overview home no longer carries the feature card');
assert(!t.overview(db,NOW).includes('How this estimate works'));
assert(!t.overview(db,NOW).includes('overview-feature')&&!t.overview(db,NOW).includes('Next in production')&&!t.overview(db,NOW).includes('Ready for your review'));
console.log('Studio V3 selector and Overview checks OK');

const identicalSlot=[slot('OWB:s1','2026-11-04T18:00:00Z'),slot('OWB:s2','2026-11-04T18:00:00Z')];
identicalSlot[0].youtube.videoId='abcdefghijk';identicalSlot[1].youtube.videoId='bcdefghijkl';
assert.equal(t.scheduledThisWeek(identicalSlot,weekNow).length,2,'distinct videos sharing a slot are still two scheduled videos');
const ytReady=v({key:'physical',youtube:{videoId:'abcdefghijk',state:'private'}});
assert.equal(t.uniqueVideos([ytReady,{...ytReady,key:'alias'},ytReady]).length,1);
assert.equal(t.uniqueVideos([v({key:'same'}),v({key:'same',youtube:{videoId:'abcdefghijk'}})]).length,1);
assert.equal(t.producingVideos([v({key:'backlog',lane:'upcoming',production:nearlyDone.production})]).length,0,'backlog milestones do not silently promote a video into active production');

const runningTask={id:'Jactual',status:'claimed',by:'codex',title:'Assemble the film',remaining_action:'Finish the recorded edit',claimedAt:new Date(NOW-10*6e4).toISOString(),progress:{step:2,of:5}};
const activityBoard={tracker:{videos:[]},models:freshModels,owb:{jobs:[runningTask,{id:'q',status:'open'},{id:'h',status:'blocked'}]}};
const activeHtml=t.activityCard(activityBoard,NOW);
assert(activeHtml.includes('Active jobs')&&activeHtml.includes('Running now'));
assert(activeHtml.includes('Codex is working')&&activeHtml.includes('Jactual'));
assert(activeHtml.includes('2 / 5 steps (40%)')&&activeHtml.includes('~15m ETA'));
assert(activeHtml.includes('#agents&job=Jactual')&&activeHtml.includes('aj-bar'));
assert.equal((activeHtml.match(/aj-bar/g)||[]).length,1,'one claimed job still shows one progress bar');
assert.equal((activeHtml.match(/is working/g)||[]).length,1);
// Two agents running → two cards / two bars (Ben, 6 Nov evening) — not "+N other active job".
const geminiTask={id:'Jgemini',status:'claimed',by:'gemini',title:'Check the sources',remaining_action:'Verify every MUST QUOTE row',
  claimedAt:new Date(NOW-8*6e4).toISOString(),progress:{step:1,of:3}};
const twoAgentsHtml=t.activityCard({...activityBoard,owb:{jobs:[runningTask,geminiTask,{id:'q',status:'open'},{id:'h',status:'blocked'}]}},NOW);
assert(twoAgentsHtml.includes('Codex is working')&&twoAgentsHtml.includes('Gemini is working'));
assert(twoAgentsHtml.includes('Jactual')&&twoAgentsHtml.includes('Jgemini'));
assert(twoAgentsHtml.includes('Active jobs (2)')&&twoAgentsHtml.includes('Running now'));
assert.equal((twoAgentsHtml.match(/aj-bar/g)||[]).length,2,'each running agent gets its own progress bar');
assert.equal((twoAgentsHtml.match(/is working/g)||[]).length,2);
assert(!twoAgentsHtml.includes('activity-footer')&&!twoAgentsHtml.includes('queued ·'),'compact Active jobs drops the queued/waiting footer');
assert(!twoAgentsHtml.includes('other active job'),'no collapsed "+N other" summary when multiple agents run');
const sameAgentTwo=t.activityCard({...activityBoard,owb:{jobs:[runningTask,{...runningTask,id:'Jsecond',remaining_action:'Second cut'}]}},NOW);
assert.equal((sameAgentTwo.match(/aj-bar/g)||[]).length,2);
assert(!sameAgentTwo.includes('+1 other active job'));
const missingHtml=t.activityCard({...activityBoard,owb:{jobs:[{...runningTask,progress:null,claimedAt:''}]}},NOW);
assert(!missingHtml.includes('aj-bar')&&missingHtml.includes('Progress n/a'));
const idleHtml=t.activityCard(makeBoard([]),NOW);
assert(idleHtml.includes('Studio waiting for next job')&&idleHtml.includes('Active jobs')&&!idleHtml.includes('Running now'));
for(const progress of [{step:-1,of:5},{step:6,of:5},{step:2,of:0},{step:1.5,of:5}, {step:'<img>',of:5}]) assert.equal(t.recordedTaskProgress({progress}),null);
assert(!t.activityCard({...activityBoard,owb:{jobs:[{...runningTask,progress:{step:5,of:5},estMin:100}]}},NOW).includes('~15m ETA'));
console.log('Studio active-job card checks OK');

// Published status overrides stale production lanes and follow-up jobs, without fabricating 100% history.
const publicMissing=v({key:'published',lane:'progress',youtube:{state:'live',privacy:'public',videoId:'abcdefghijk'},jobs:[{id:'followup',status:'claimed',progress:{step:1,of:2}}]});
assert.equal(t.stage(publicMissing),'Published');
const publishedRow=t.videoProductionRow(publicMissing,NOW);
assert(!publishedRow.includes('0%')&&!publishedRow.includes('UAT:')&&!publishedRow.includes('In progress'));
assert(!publishedRow.includes('50%'),'follow-up task progress is not published-video progress');
assert(publishedRow.includes('Published'));
const publishedDetail=t.productionDetail(publicMissing,NOW);
assert(publishedDetail.includes('Published on YouTube')&&publishedDetail.includes('Recorded production history'));
assert(!publishedDetail.includes('role="progressbar"')&&!publishedDetail.includes('progress-number'));
assert(publishedDetail.includes('Unconfirmed'),'unknown history stays unknown, not changed to complete');
assert(t.videoGroups([publicMissing]).postlive.some(x=>x.key==='published'));  // live with a follow-up job: Post-live lane
assert.equal(t.videoGroups([publicMissing]).progress.length,0);
assert.equal(t.videoGroups([publicMissing]).uat.length,0);
assert(t.videoProductionRow(v({key:'unfinished'}),NOW).includes('0%'),'active production still uses recorded milestone counts');
console.log('Published-video regression checks OK');

// Blocker guidance uses actual holds and explicit stage references, never a guessed owner or release time.
const blockedEdit={id:'edit',label:'Edit',state:'blocked',source:{ref:'d0b04b5e0'},evidence:'d0b04b5e0',jobs:[]};
const inputJob={id:'J1471',stage:'',status:'blocked',by:'codex',title:'Correct openings',remaining_action:'Identify approved moving ISS input, then correct and review the openings',after:'J1468',hold:{type:'input',condition:'Approved ISS interval for AR2 0-2.4s plus loop preroll remains missing. Correct masters and run the affected checks.',checked_at:new Date(NOW-10*6e4).toISOString(),check_at:new Date(NOW+30*6e4).toISOString()},result:'Inspection d0b04b5e0; no suitable approved input.'};
const blockedFilm=v({key:'OWB:030',jobs:[{id:'other',status:'blocked',by:'cursor',hold:{condition:'Unrelated video gate'}},inputJob],production:{milestones:[blockedEdit],activeStages:['edit'],eta:{state:'unavailable'}}});
const compactStage=t.currentStageCard(blockedFilm);
assert(compactStage.includes('data-open-stage="edit"')&&compactStage.includes('More information'));
assert(!compactStage.includes('blocker-guide')&&!compactStage.includes('Full recorded blocker'));
const guidance=t.blockerModel(blockedFilm,blockedEdit);
assert.equal(guidance.job.id,'J1471');assert.equal(guidance.scope,'reference');assert.equal(guidance.owner,'Codex');
assert(guidance.why.includes('International Space Station'));assert(guidance.action.includes('Identify approved'));
t.setBoard({owb:{jobStates:{J1468:{status:'done'}}}});
const guideHtml=t.blockerGuide(blockedFilm,blockedEdit,NOW);
assert(guideHtml.includes('What it is waiting for')&&guideHtml.includes('What moves it on')&&guideHtml.includes('#agents&job=J1471'));
assert(guideHtml.includes('J1468 · Completed')&&guideHtml.includes('Next recorded check'));
assert(guideHtml.includes('not a promise')&&guideHtml.includes('1 other recorded video hold'));
assert(guideHtml.includes(inputJob.hold.condition),'original condition is available unmodified');
assert(!guideHtml.includes('Resolve the recorded blocker'));
const missingGuide=t.blockerModel(v({jobs:[]}),blockedEdit);
assert(missingGuide.why.includes('no stage-specific reason'));assert.equal(missingGuide.owner,'Not recorded');assert(missingGuide.action.includes('No unblock action'));
const videoOnly=t.blockerModel(v({jobs:[{...inputJob,result:'No reference',hold:{condition:'Waiting for footage'}}]}),blockedEdit);
assert.equal(videoOnly.scope,'video');
const reviewStageFixture={id:'picture',label:'Picture',state:'review',reviewer:'claude',jobs:[]};
const reviewGuide=t.blockerModel(blockedFilm,reviewStageFixture);
assert.equal(reviewGuide.scope,'stage');assert(reviewGuide.why.includes('Claude'));assert(!reviewGuide.why.includes('ISS'));
const overdue=t.blockerGuide(v({jobs:[{...inputJob,stage:'edit',hold:{condition:'Waiting for <unsafe>',check_at:new Date(NOW-6e4).toISOString()}}]}),blockedEdit,NOW);
assert(overdue.includes('Check overdue')&&overdue.includes('&lt;unsafe&gt;')&&!overdue.includes('<unsafe>'));
assert(!t.blockerReason('Approved ISS input found; waiting for edit review.').includes('is missing'));
console.log('Studio blocker guidance checks OK');

const ownStageJob={...inputJob,id:'Jstage',stage:'edit',by:'gemini',hold:{condition:'Awaiting the recorded edit review'}};
assert.equal(t.blockerModel(v({jobs:[inputJob,ownStageJob]}),blockedEdit).job.id,'Jstage','explicit stage mapping outranks a reference match');
assert(!t.blockerModel(v({jobs:[{...inputJob,status:'done'}]}),blockedEdit).job,'completed records cannot become active blockers');

// Raw open is not ready: workflow dependencies/date gates control the activity footer.
const dispatchBoard={models:{checkedAt:new Date(NOW).toISOString()},tracker:{videos:[]},owb:{jobs:[{id:'future',status:'open'},{id:'dependent',status:'open'},{id:'ready',status:'open'}]},workflow:{at:new Date(NOW).toISOString(),states:{future:{state:'waiting'},dependent:{state:'waiting'},ready:{state:'queued'}}}};
assert.equal(t.overviewModel(dispatchBoard,NOW).queued.length,1);
assert.equal(t.overviewModel(dispatchBoard,NOW).held.length,2);
assert(t.activityCard(dispatchBoard,NOW).includes('Ready work waiting for dispatch'));
dispatchBoard.workflow.states.ready.state='waiting';
assert(t.activityCard(dispatchBoard,NOW).includes('No job running · work is waiting'));
assert(!t.activityCard(dispatchBoard,NOW).includes('0 queued · 3 waiting'),'queued/waiting footer is gone from Active jobs');
console.log('Dispatch visibility checks OK');

dispatchBoard.owb.jobs.push({id:'chiefReview',status:'blocked',by:'cursor',title:'Review the output'});
dispatchBoard.workflow.states.chiefReview={state:'running'};
dispatchBoard.workflow.active=[{id:'chiefReview',worker:'codex',progress:{step:1,of:3}}];
assert(t.activityCard(dispatchBoard,NOW).includes('Codex is working'));
assert(t.activityCard(dispatchBoard,NOW).includes('1 / 3 steps'));
assert.equal(t.overviewModel(dispatchBoard,NOW).running.length,1);
// Missing milestone data must explain the gap without inventing approval or linking unrelated jobs.
const unknownQA={id:'qa',label:'Chief QA',state:'unknown',dependsOn:['edit','thumbs']};
const completedPrereqs=[{id:'edit',label:'Edit',state:'done'},{id:'thumbs',label:'Packaging',state:'done'},unknownQA];
const qaVideo=v({production:{milestones:completedPrereqs},jobs:[{id:'unrelated',stage:'',status:'blocked',remaining_action:'Repair a Short'}]});
let qaContext=t.stageExplanation(qaVideo,unknownQA);
assert(qaContext.why.includes('no recorded review decision'));assert(!qaContext.job);
assert(qaContext.action.includes('queue its review'));assert(qaContext.owner.includes('Chief owns QA'));
const qaHtml=t.milestoneCard(qaVideo,unknownQA,'qa');
assert(qaHtml.includes('QA decision not recorded')&&!qaHtml.includes('Unassigned')&&!qaHtml.includes('Open stage details for'));
const scheduledQA=t.stageExplanation({...qaVideo,youtube:{state:'scheduled',publishAtLondon:'Sun 22 Nov 2026 18:00 GMT'}},unknownQA);
assert(scheduledQA.why.includes('already scheduled')&&scheduledQA.why.includes('22 Nov'));
assert(scheduledQA.action.includes('not a reason to restart production'));
const waitingQA=t.stageExplanation({...qaVideo,production:{milestones:[{id:'edit',label:'Edit',state:'blocked'},unknownQA]}},unknownQA);
assert(waitingQA.why.includes('Edit (Waiting)'));
const linkedQA=t.stageExplanation({...qaVideo,jobs:[{id:'Jreview',stage:'qa',status:'claimed',by:'codex',remaining_action:'Review the final cut'}]},unknownQA);
assert.equal(linkedQA.job.id,'Jreview');assert.equal(linkedQA.owner,'Codex');assert(linkedQA.why.includes('claimed'));
assert(t.stageExplanationHtml({...qaVideo,jobs:[{id:'Jreview',stage:'qa',status:'open',title:'<unsafe>'}]},unknownQA).includes('&lt;unsafe&gt;'));
console.log('Stage explanation checks OK');
// Overview home no longer shows Ready for review / Next in production (Review tab owns that).
const notReadyOverview=t.overview({tracker:{videos:[v({key:'blocked-example',lane:'progress'})]},owb:{jobs:[]}},NOW);
assert(!notReadyOverview.includes('Next in production')&&!notReadyOverview.includes('Ready for your review')&&!notReadyOverview.includes('overview-feature'));
assert(!notReadyOverview.includes('Next for your review')&&!notReadyOverview.includes('▶ Watch & review'));
const readyBoard={tracker:{videos:[v({key:'watch-now',lane:'ready',readyFor:'Ben',watch:{url:'https://example.com/cut.mp4',version:'v02'}})]},owb:{jobs:[]}};
const readyOverview=t.overview(readyBoard,NOW);
assert(!readyOverview.includes('Ready for your review')&&!readyOverview.includes('▶ Watch & review v02')&&!readyOverview.includes('overview-feature'));
assert.equal(t.overviewModel(readyBoard,NOW).ready.length,1,'ready cuts still count in To review');
const readyReview=t.renderTab('review',readyBoard,NOW);
assert(readyReview.includes('href="#uat=watch-now"')&&(readyReview.includes('▶ Watch & review v02')||readyReview.includes('Watch &amp; review v02')),
  'Watch CTA lives on the Review tab');
const featuredReady=t.featuredCard(t.featureVideo(readyBoard,NOW),NOW,0);
assert(featuredReady.includes('Ready for your review')||featuredReady.includes('Watch'),'featuredCard helper still renders ready cuts for Review');
const missingDelivery=t.overview({tracker:{videos:[v({key:'missing-watch',lane:'ready',readyFor:'Ben'})]},owb:{jobs:[]}},NOW);
assert(!missingDelivery.includes('▶ Watch & review')&&!missingDelivery.includes('overview-feature'));
console.log('Review readiness wording and Watch CTA checks OK');
// Activity video context comes from existing associations, never guessed from a job title.
const contextVideos=[v({key:'HOS:008',channel:'HOS',title:'How Franklin Tamed Lightning',jobs:[{id:'J1757'}]}),v({key:'OWB:030',channel:'OWB',title:'Apophis'})];
const contextBoard={tracker:{videos:contextVideos},owb:{jobs:[{id:'parent',repo:'hos',film:'008'}]}};
assert(t.activityVideoContext(contextBoard,{id:'J1757'}).label.includes('Franklin'));
assert(t.activityVideoContext(contextBoard,{id:'x',taskKeys:['HOS:008','HOS:008']}).count===1);
assert(t.activityVideoContext(contextBoard,{id:'x',repo:'hos',film:'008'}).label.includes('History of Science'));
assert(t.activityVideoContext(contextBoard,{id:'x',recheck_of:'parent'}).label.includes('Franklin'));
assert.equal(t.activityVideoContext(contextBoard,{id:'x',taskKeys:['HOS:008','OWB:030']}).count,2);
assert(t.activityVideoContext(contextBoard,{id:'x',taskKeys:['HOS:999']}).label.includes('title not recorded'));
assert(t.activityVideoContext(contextBoard,{id:'x',title:'HOS 008 mentioned in prose'}).label.includes('no video linked'));
console.log('Activity video context checks OK');

const escapedContext=t.activityCard({...activityBoard,tracker:{videos:[v({key:'HOS:008',channel:'HOS',title:'<svg onload=alert(1)>',jobs:[{id:'Jactual'}]})]}},NOW);
assert(!escapedContext.includes('<svg onload'), 'compact Active jobs does not dump a raw video title XSS payload');
assert(t.activityVideoContext({tracker:{videos:[v({key:'HOS:008',channel:'HOS',title:'<svg onload=alert(1)>',jobs:[{id:'Jactual'}]})]}},{id:'Jactual'}).label.includes('<svg onload'),
  'activityVideoContext still exposes the raw title for callers that escape it');

// A follow-up checkpoint is distinct from the ready review's start and from real device capacity.
const reviewParent={id:'J1834',status:'blocked',by:'codex',hold:{condition:'Parked for Chief approval of delivered candidate',check_at:new Date(NOW+60*6e4).toISOString()}};
const reviewTask={id:'J1841',recheck_of:'J1834',status:'open'};
const busyTask={id:'J1835',status:'claimed',by:'codex',title:'Check another film'};
const reviewBoard={owb:{jobs:[reviewParent,reviewTask,busyTask]},models:{checkedAt:new Date(NOW).toISOString(),chief:{agent:'codex'}},workflow:{at:new Date(NOW).toISOString(),states:{J1841:{state:'queued'}}}};
let reviewInfo=t.reviewQueueInfo(reviewBoard,reviewParent,NOW,{at:new Date(NOW).toISOString(),state:'waiting',why:['in use']});
assert(reviewInfo.ready&&reviewInfo.busy.id==='J1835');assert(reviewInfo.macbookText.includes('in use'));assert(reviewInfo.availability.includes('No reliable'));
assert(!t.reviewQueueInfo(reviewBoard,{...reviewParent,hold:{condition:'Missing footage'}},NOW));
reviewInfo=t.reviewQueueInfo({...reviewBoard,models:{...reviewBoard.models,checkedAt:new Date(NOW-10*6e4).toISOString()}},reviewParent,NOW);
assert(!reviewInfo.busy&&reviewInfo.macbookText.includes('stale or missing'));
t.setBoard(reviewBoard);
const reviewHtml=t.blockerGuide(v({jobs:[reviewParent]}),{id:'edit',label:'Edit',state:'review',jobs:[reviewParent]},NOW);
assert(reviewHtml.includes('Awaiting Chief review')&&reviewHtml.includes('review queued and eligible now')&&reviewHtml.includes('#agents&job=J1841'));
assert(reviewHtml.includes('Previous worker')&&reviewHtml.includes('does not schedule or delay'));
console.log('Review queue and capacity explanation checks OK');

reviewBoard.owb.jobs.push({id:'J1844',kind:'review',ref:'J1834',status:'open',for:'gemini'});
reviewBoard.workflow.states.J1844={state:'queued'};
const specialistInfo=t.reviewQueueInfo(reviewBoard,reviewParent,NOW);
assert.equal(specialistInfo.reviewer,'Gemini');assert.equal(specialistInfo.task.id,'J1844');assert(!specialistInfo.busy,'Codex work does not establish Gemini is busy');

assert.equal(t.stageView({id:'edit',state:'blocked',jobs:[reviewParent]}).text,'Awaiting review');

reviewBoard.workflow.states.J1835={state:'running'};
assert.equal(t.reviewQueueInfo(reviewBoard,reviewParent,NOW).miniBusy.id,'J1835');

assert(t.activityVideoContext(contextBoard,{id:'specialist',kind:'review',ref:'parent'}).label.includes('no video linked'));
contextBoard.owb.jobs.push({id:'J1834',repo:'hos',film:'008'});
assert(t.activityVideoContext(contextBoard,{id:'J1844',kind:'review',ref:'J1834'}).label.includes('Franklin'));

// Live execution lease reports startup without fabricating a claim, progress or task ETA.
const startupBoard={models:{checkedAt:new Date(NOW).toISOString(),models:[]},tracker:{videos:[]},owb:{jobs:[{id:'Jlaunch',status:'open',title:'Prepare the selected review',progress:{step:3,of:3}}]},workflow:{at:new Date(NOW).toISOString(),states:{Jlaunch:{state:'starting'}},active:[{id:'Jlaunch',worker:'gemini',mode:'starting',phase:'starting',startedAt:new Date(NOW-6e4).toISOString(),expiresAt:new Date(NOW+10*6e4).toISOString()}]}};
const startupHtml=t.activityCard(startupBoard,NOW), startupModel=t.overviewModel(startupBoard,NOW);
assert(startupHtml.includes('Gemini is starting')&&startupHtml.includes('Claim pending')&&startupHtml.includes('Starting…'));
assert(!startupHtml.includes('aj-bar')&&!startupHtml.includes('~15m ETA'));
assert.equal(startupModel.queued.length,0);assert.equal(startupModel.running.length,1);assert.equal(startupModel.status.text,'Starting');
const expiredStartup=t.overviewModel(startupBoard,NOW+11*6e4);assert.equal(expiredStartup.running.length,0);assert.equal(expiredStartup.status.text,'Attention needed');
const onlyHeartbeat={...startupBoard,workflow:{},owb:{jobs:[{id:'Jlaunch',status:'open'}]},models:{checkedAt:new Date(NOW).toISOString(),runner:{state:'working',job:'Jlaunch'}}};
assert.equal(t.overviewModel(onlyHeartbeat,NOW).running.length,0,'heartbeat alone never fabricates active work');
console.log('Starting-worker visibility checks OK');

// Delivered cuts retain missing historical stages without misleading completion percentages.
const readyHistory=v({key:'HOS:008',channel:'HOS',version:'v03',lane:'ready',readyFor:'Ben',watch:{url:'https://example.test/v03'},production:{milestones:[{id:'topic',state:'done'},{id:'script',state:'done'},{id:'vo',state:'done'},{id:'picture',state:'doing'}]}});
const readyHistoryHtml=t.productionDetail(readyHistory,NOW);
assert(readyHistoryHtml.includes('Ready for your review')&&readyHistoryHtml.includes('Recorded production history'));
assert(!readyHistoryHtml.includes('progress-number')&&!readyHistoryHtml.includes('role="progressbar"')&&!readyHistoryHtml.includes('Current stage'));
assert.equal(t.progressStats(readyHistory).done,3,'history is never silently promoted to 100%');
assert(!t.overview({tracker:{videos:[readyHistory]}},NOW).includes('33%'),'ready feature does not report historical coverage as production progress');
const reviewChanged={...readyHistory,check:{verdict:'change',version:'v03',handled:false}};
assert.equal(t.forBen([reviewChanged]).length,0,'unhandled same-version changes override a stale ready lane');
assert.equal(t.stage(reviewChanged),'Fixing your changes');
assert(t.productionDetail(reviewChanged,NOW).includes('Changes requested'));
assert(!t.forecastView(reviewChanged,NOW).reason.includes('Your review can start'));
assert.equal(t.forBen([{...reviewChanged,version:'v04'}]).length,1,'old-version feedback does not block a new cut');
assert.equal(t.forBen([{...reviewChanged,check:{...reviewChanged.check,handled:true}}]).length,1,'handled feedback does not suppress a fresh recorded handoff');
const postPublish=t.productionDetail({...publicMissing,jobs:[...publicMissing.jobs,...publicMissing.jobs]},NOW);
assert(postPublish.includes('Post-publication work')&&postPublish.includes('1 job'));
assert(postPublish.includes('#agents&job=followup'),'follow-up work is linked to its actual job');
assert(!postPublish.includes('progress-number'));
console.log('Delivered-cut historical coverage and post-publication work checks OK');

assert.equal(t.producingVideos([reviewChanged]).length,1,'stale ready lane plus current changes remains in producing count');
assert(!t.videoProductionRow(readyHistory,NOW).includes('33%'));
assert(!t.videoProductionRow(reviewChanged,NOW).includes('33%'));
assert.equal(t.forecastView({...publicMissing,version:'v03',check:{verdict:'change',version:'v03',handled:false}},NOW).value,'Handoff complete','publication overrides old review feedback');

assert(!t.detail({tracker:{videos:[{...publicMissing,jobs:[...publicMissing.jobs,...publicMissing.jobs]}]}},publicMissing.key).includes('2 jobs'),'technical linked-job count is also deduplicated');

const scheduledHistory=v({youtube:{state:'scheduled',privacy:'private'},production:readyHistory.production});
assert(!t.milestoneProgress(scheduledHistory).includes('UAT handoff complete'),'a schedule does not establish Ben approval');
assert(t.productionDetail(scheduledHistory,NOW).includes('Scheduled on YouTube'));
assert(!t.productionDetail(scheduledHistory,NOW).includes('progress-number'));

// Cut identity and aggregate history must stay separate, including cached board payloads.
const mixedCut=v({key:'OWB:030',version:'v13a',watch:{url:'https://example.test/watch',file:'OWB UAT/030_apophis_short_v13a_PHONE.mp4'},production:{milestones:['topic','script','sources','vo','shots','picture','edit','thumbs','qa'].map(id=>({id,state:id==='edit'?'blocked':id==='qa'?'unknown':'done',source:id==='edit'?{note:'AR cohort: separate replacement work'}:{}}))}});

// Stage row counts explain real sub-stage work without becoming video/time progress.
const hosRows=nine.map(id=>({id,label:id,state:['topic','script','sources','vo'].includes(id)?'done':id==='picture'?'doing':'unknown',
  summary:id==='picture'?'70/90 picture rows recorded':'',evidence:id==='picture'?'/private/internal-generation-log':''}));
const hosPicture=v({key:'HOS:009',channel:'HOS',production:{milestones:hosRows,activeStages:['picture'],eta:{state:'unavailable'}}});
const hosBoard={tracker:{videos:[hosPicture]}};
const hosFeatured=t.featuredCard(t.featureVideo(hosBoard,NOW),NOW,1);
assert(hosFeatured.includes('70/90 picture rows recorded'));
assert(hosFeatured.includes('4 of 9 milestones complete')&&hosFeatured.includes('44%'));
assert(!hosFeatured.includes('/private/internal-generation-log'));
assert(!t.overview(hosBoard,NOW).includes('70/90 picture rows recorded'),'Overview home no longer embeds the feature card');
const noRowSummary=t.featuredCard(t.featureVideo({tracker:{videos:[{...hosPicture,production:{...hosPicture.production,milestones:hosRows.map(m=>({...m,summary:''}))}}]}},NOW),NOW,1);
assert(!noRowSummary.includes('picture rows recorded'),'missing row counts never get invented');
const unknownCutRows=t.featuredCard(t.featureVideo({tracker:{videos:[{...hosPicture,production:{scope:'unconfirmed_cut',projectHistory:hosPicture.production}}]}},NOW),NOW,1);
assert(!unknownCutRows.includes('70/90 picture rows recorded'),'project row counts do not certify an unconfirmed cut');
const normalized=t.normalizeCut(mixedCut);
assert.equal(normalized.type,'short');assert.equal(normalized.key,'OWB:030');assert.equal(mixedCut.type,'long','source records are unchanged');
const mixedBoard={tracker:{videos:[mixedCut]}};
const mixedFeatured=t.featuredCard(t.featureVideo(mixedBoard,NOW),NOW,1);
assert(mixedFeatured.includes('Short')&&mixedFeatured.includes('Cut progress')&&mixedFeatured.includes('Unconfirmed'));
assert(!mixedFeatured.includes('78%')&&!mixedFeatured.includes('0%'));
assert(!t.overview(mixedBoard,NOW).includes('Cut progress'),'Overview home no longer embeds cut progress feature copy');
assert(!t.videoProductionRow(mixedCut,NOW).includes('78%'));
const mixedDetail=t.productionDetail(mixedCut,NOW);
assert(mixedDetail.includes('Progress for this cut unconfirmed')&&mixedDetail.includes('Related project history · 7 of 9'));
assert(!mixedDetail.includes('progress-number')&&!mixedDetail.includes('role="progressbar"'));
assert(!t.forecastView(mixedCut,NOW).credible);
assert.equal(t.progressStats(mixedCut).done,7,'original history is retained');
assert(t.productionDetail({...mixedCut,lane:'ready',readyFor:'Ben'},NOW).includes('Ready for your review'));
assert.equal(t.normalizeCut({...mixedCut,youtube:{videoId:'publishedLong',state:'live'}}).type,'long');
console.log('Exact-cut identity and mixed-scope progress checks OK');

const exactCut={...normalized,production:{...mixedCut.production,scope:'cut',scopeVersion:'v13a'}};
assert(!t.unconfirmedCut(exactCut));assert(t.milestoneProgress(exactCut).includes('78%'));
assert(t.unconfirmedCut({...exactCut,version:'v14'}),'a later cut cannot borrow an earlier version mapping');

assert(t.unconfirmedCut({...exactCut,watch:{...exactCut.watch,version:'v12'}}),'watch and card versions must agree');

// Queue forecast (Ben, 5 Nov 2026): each queued job says who it waits for, its place in line and when it starts.
// Overview tidy (Ben, 6 Nov 2026): hide idle empty agent rows, drop min/job, plain unavailable, wrap clear times.
{
  const qb = {queueForecast: {jobs: {J7: {agent: 'gemini', pos: 4, startAt: '2026-11-05T11:40:00Z'}},
    noAgent: {J8: 'waiting for codex: marked down'},
    agents: [{agent: 'gemini', up: true, now: 'J6', freeAt: '2026-11-05T10:40:00Z', queued: 4, clearAt: '2026-11-05T13:00:00Z', minutesPerJob: 48},
             {agent: 'cursor', up: false, why: 'out of credit until 2026-11-06'},
             {agent: 'macbook', up: true, now: '', queued: 0, freeAt: '2026-11-05T10:00:00Z', clearAt: '2026-11-05T10:00:00Z', minutesPerJob: 150},
             {agent: 'claude', up: false, why: 'no Claude run for 647 min (heartbeat stale)'}], note: 'Estimate'}};
  const line = t.forecastLine(qb, {id: 'J7'});
  assert(line.startsWith('Next for Gemini · #4 in line · starts about'), line);
  assert.equal(t.forecastLine(qb, {id: 'J8'}), 'Waiting for codex: marked down');
  assert.equal(t.forecastLine(qb, {id: 'J9'}), '');
  const lanes = t.agentLines(qb);
  assert(lanes.includes('on J6 · free about') && lanes.includes('4 in line') && lanes.includes('clear about'), lanes);
  assert(lanes.includes('Not available · out of credit'), lanes);
  assert(lanes.includes('Not available · last run about 11 hours ago'), lanes);
  assert(!/<span class="p24-film">MacBook(?: 2)?<\/span>/.test(lanes), 'idle MacBook with nothing waiting is hidden');
  assert(!lanes.includes('min/job'), 'per-row minutes-per-job is gone');
  assert(lanes.includes('p24-title wrap'), 'queue lines use the wrapping title class');
  assert.equal(t.agentLines({}), '');
  assert.equal(t.agentLines({queueForecast: {agents: [{agent: 'macbook', up: true, now: '', queued: 0}]}}), '',
    'Agents block hides when every row is idle and empty');
  assert.equal(t.plainWhy('no Claude run for 647 min (heartbeat…)'), 'last run about 11 hours ago');
  assert.equal(t.plainWhy('no MacBook heartbeat in 40 min'), "MacBook hasn't checked in for about 40 min");
}
{
  const now = Date.parse('2026-11-06T10:51:00Z');
  const qb = {machines: {machines: [
    {id: 'mini', name: 'Mac mini', done24: 45, now: [{id: 'J2276', title: 'Verify condition for J2033', agent: 'gemini'}],
      byAgent: {gemini: 28, cursor: 10, codex: 7}, seen: '2026-11-06T10:50:00Z'},
    {id: 'macbook', name: 'MacBook Pro', done24: 12, now: [], why: 'no MacBook job waiting',
      byAgent: {macbook: 7, 'macbook-2': 5}, agents: ['codex', 'gemini', 'claude', 'cursor'], seen: '2026-11-06T10:47:00Z'},
    {id: 'cloud', name: 'Claude (cloud)', done24: 5, now: [], byAgent: {claude: 5}, seen: '2026-11-05T22:51:00Z'},
  ]}, queueForecast: {agents: [
    {agent: 'gemini', up: true, now: 'J2276', freeAt: '2026-11-06T11:30:00Z', queued: 2, clearAt: '2026-11-06T14:00:00Z'},
    {agent: 'macbook', up: true, now: '', queued: 0},
  ], note: 'Estimate'}};
  const card = t.machinesCard(qb, now);
  assert(card.includes('Mini') && card.includes('45') && card.includes('mc-row'), card);
  assert(card.includes('mc-chip') && card.includes('light-green'), 'working machine gets a green traffic light');
  assert(card.includes('MacBook') && card.includes('Claude') && card.includes('Grok'), 'four machine chips stay in one row');
  assert(!card.includes('Verify condition for J2033'), 'long machine job titles are not dumped on Overview chips');
  assert(!card.includes('By gemini') && !card.includes('By macbook') && !/By claude/.test(card), 'per-machine By splits are gone');
  assert(!card.includes('Agents here'), 'Agents here CLI list is gone');
  assert(!card.includes('overview-agents'), 'Machines section does not swallow Agents');
  assert((card.match(/aria-label="Machines"/g)||[]).length===1, 'Machines is its own section');
  const agents = t.agentsCards(qb);
  assert(agents.includes('overview-agents') && agents.includes('aria-label="Agents"'), 'agentsCards helper still builds a separate Agents section');
  assert(agents.includes('mc-chip') && agents.includes('light-green') && agents.includes('J2276'), 'agent chips use traffic lights');
  assert(agents.includes('light-red') || agents.includes('Idle') || agents.includes('Down'), 'idle/down agents get a red light');
  const ov = t.overview({tracker:{videos:[]}, ...qb}, now);
  assert(ov.includes('overview-stats') && ov.includes('ov-stat'), 'Overview stacks simple stats');
  assert(ov.includes('4 total') && ov.includes('1 on · 45 done'), 'Machines header shows total and chip captions');
  assert(ov.indexOf('overview-machines') < ov.indexOf('overview-activity'), 'Machines sit above Active jobs');
  assert(ov.includes('Active jobs'), 'Active jobs section uses the cleaner label');
  assert(!ov.includes('overview-agents') && !ov.includes('Agents</h2>'), 'Overview home does not repeat the Agents tab');
  assert(!ov.includes('overview-next-live') && !ov.includes('Next to go live'), 'Overview home does not list Next to go live');
  assert(!ov.includes('overview-feature') && !ov.includes('Next in production') && !ov.includes('Ready for your review'),
    'Overview home drops Ready for review / Next in production');
}
console.log('Queue forecast checks OK');

// Last 24 hours: quiet film cards with remaining-to-go-live checklist behind a disclosure (Ben, 6 Nov 2026).
{
  const p24 = {
    hours: 24, jobsDone: 57, videoJobs: 30, otherJobs: 27, milestones: 3,
    byAgent: {gemini: 22, codex: 10},
    glance: {
      doneToday: 9, left: 4, blocked: 1,
      blockedJobs: [{id: 'J2142', film: 'OWB:032', title: '032 pebble ruler review', status: 'blocked',
        waitKind: 'after', why: 'Will run automatically after J2141 (032 picture harvest)'}],
      nextLive: [
        {key: 'OWB:025', title: 'Could a Robot Survive on Mars?', at: '2026-11-08T18:00:00.000Z', atLondon: 'Sun 8 Nov 2026 18:00 GMT', type: 'long'},
        {key: 'OWB:025:S:iyvWYFP_ETA', title: 'Could a Robot Survive a Night on Mars?', at: '2026-11-09T11:30:00.000Z', atLondon: 'Mon 9 Nov 2026 11:30 GMT', type: 'short'},
        {key: 'OWB:025:S:TtgHNLXfDSs', title: 'Why Did a 90-Day Mars Rover Last 14 Years?', at: '2026-11-11T11:30:00.000Z', atLondon: 'Wed 11 Nov 2026 11:30 GMT', type: 'short'},
        {key: 'HOS:007', title: 'Why Vaccines Are Named After a Cow', at: '2026-11-12T18:00:00Z', atLondon: 'Thu 12 Nov 2026 18:00 GMT', type: 'long'},
      ],
    },
    moved: [
      {key: 'OWB:031', title: 'What Happens When Earths Magnetic Field Flips', from: 56, to: 67, milestones: 1},
      {key: 'OWB:032', title: 'What Would Happen If You Landed On Titan', from: 56, to: 67, milestones: 1},
    ],
    films: [
      {film: 'OWB:031', title: 'What Happens When Earths Magnetic Field Flips', jobs: 2, closed: true,
        from: 56, to: 67, milestones: 1, status: '56% → 67%', pct: 67, stage: 'edit', stageLabel: 'edit',
        doneCount: 6, total: 9, pctReason: '6 of 9 stages · edit still open',
        doneToday: 1, left: 0, blocked: 0, earlierDone: 4,
        items: [{id: 'J2100', title: '031 edit polish', status: 'done', when: 'today', stage: 'edit'}]},
      {film: 'OWB:032', title: 'What Would Happen If You Landed On Titan', jobs: 4, closed: true,
        from: 56, to: 67, milestones: 1, status: '56% → 67%', pct: 67, stage: 'picture', stageLabel: 'picture',
        doneCount: 6, total: 9, pctReason: '6 of 9 stages · picture still open',
        doneToday: 1, left: 3, blocked: 1, earlierDone: 12,
        blockedWhy: 'Will run automatically after J2141 (032 picture harvest)',
        items: [
          {id: 'J2141', title: '032 picture harvest', status: 'claimed', stage: 'picture', progress: {step: 1, of: 3}},
          {id: 'J2142', title: '032 pebble ruler review', status: 'blocked', stage: 'picture', waitKind: 'after',
            after: 'J2141', why: 'Will run automatically after J2141 (032 picture harvest)'},
          {kind: 'stage', stage: 'qa', status: 'todo', title: 'Chief QA — not started', state: 'unknown'},
          {id: 'J2110', title: 'Titan Short v11 cover', status: 'done', when: 'today', stage: 'thumbs'},
          {id: 'J2109', title: '032 spectrum stills review', status: 'done', when: 'yesterday', stage: 'picture'},
        ]},
      // 033 had jobs but no stage closed — not in moved[].
      {film: 'OWB:033', title: 'Why Knocked-Sideways Uranus Has 21-Year Winters', jobs: 1, closed: false,
        status: 'worked on, no stage closed — still in picture (56%)', pct: 56, stage: 'picture', stageLabel: 'picture',
        doneCount: 5, total: 9, pctReason: '5 of 9 stages · picture still open',
        doneToday: 1, left: 0, blocked: 0, earlierDone: 2,
        items: [{id: 'J2200', title: 'Chief: resolve 033 picture orphan-review', status: 'done', when: 'today', stage: 'picture'}]},
    ],
    studio: [
      {id: 'J2290', title: 'Daily analytics capture', status: 'done', when: 'today', by: 'gemini'},
      {id: 'J2291', title: 'House rules condition check', status: 'done', when: 'today', by: 'codex'},
    ],
  };
  const card = t.progressCard({progress24h: p24});
  assert(card.includes('Video jobs finished') && card.includes('30 of 57 jobs were on videos'), 'headline stats stay');
  assert(card.includes('Videos that had work') && card.includes('p24-film-card'), 'films render as cards');
  assert(card.includes('OWB 031') && card.includes('56% → 67%'), 'moved films show the % change');
  assert(card.includes('J2141') && card.includes('1 of 3') && card.includes('in progress'), 'in-progress jobs stay visible');
  assert(!card.includes('>claimed<') && !card.includes('claimed</span>'), 'raw claimed status is not shown');
  assert(card.includes('J2200') && card.includes('OWB 033') && card.includes('56%'), 'no-stage-closed films still show their pct and id');
  assert(card.includes('Studio-wide') && card.includes('J2290') && card.includes('Daily analytics capture'), 'studio-wide jobs fold at the bottom');
  assert(!card.includes('Where the work went'), 'old count+last summary is gone');
  // Glance strip: numbers only — can't-run detail moved to Needs attention on Overview.
  assert(card.includes('p24-glance') && card.includes('Done today') && card.includes('Left to go live') && card.includes("Can't run yet"),
    'glance strip shows done today, left, and cannot-run counts');
  assert(!card.includes('p24-glance-fold') && !card.includes('overview-attention'),
    'progressCard glance stays numbers-only; Needs attention lives on Overview');
  assert(!card.includes('Next to go live') && !card.includes('overview-next-live'),
    'progressCard no longer mixes Next to go live into Last 24 hours');
  const nextLive = t.p24NextLive(p24);
  assert(nextLive.includes('Next to go live') && nextLive.includes('Could a Robot Survive on Mars?') && nextLive.includes('Why Vaccines Are Named After a Cow'),
    'p24NextLive helper still lists the next four from publish times');
  // Compact film row; full checklist expands from the row (Ben, 6 Nov ~23:07).
  // After-waits are not Ben-facing, so Can't run counts 0 even when Left still lists them.
  assert(card.includes('6 of 9 stages') && card.includes('Done 1') && card.includes('Left 3') && card.includes('Can&#39;t run 0'),
    'film cards show one-line stage / done / left / can\'t-run without opening anything');
  assert(card.includes('p24-film-bar') && card.includes('p24-film-meta') && card.includes('p24-film-summary'),
    'compact resting row keeps id, title, percent, progress bar, and meta');
  assert(card.includes('p24-check-fold') && card.includes('Jobs checklist') && card.includes('p24-film-expand'),
    'full checklist sits behind a row expand control');
  assert(!/<details[^>]*p24-check-fold[^>]*\sopen/i.test(card), 'film checklists stay closed by default');
  assert(card.includes('Will run automatically after J2141 (032 picture harvest)') && card.includes('p24-job-why'),
    "will-run-after explanation stays on the expanded checklist row");
  assert(card.includes('p24-job-spinner') && card.includes('is-done') && card.includes('is-progress') && card.includes('is-waiting'),
    'jobs render as a checklist with done, in-progress spinner and waiting marks');
  assert(card.includes('is-done-yesterday') && card.includes('data-job-state="done-yesterday"'),
    "yesterday's finished jobs use a gray tick, not today's green");
  assert(card.includes('Chief QA — not started') && card.includes('is-stage'),
    'leftover stages without a job show as unchecked rows with no invented job id');
  assert(card.includes('12 earlier jobs already done'), 'older finished jobs fold into a muted earlier note');
  assert(card.includes('data-job-state="done"') && card.includes('data-job-state="progress"') && card.includes('data-job-state="waiting"'),
    'checklist states are marked for done, in progress and waiting');
  assert(card.includes('J2142') && card.includes('after earlier work') && !card.includes('>blocked<'),
    'after-wait jobs stay unchecked with a workflow note, not raw blocked');
  assert(!/<input\b[^>]*type=["']?checkbox/i.test(card) && !/onclick=|role=["']checkbox["']/i.test(card),
    'checklist is display-only — no interactive checkbox or click handler');
  assert(card.includes('p24-job-stage') && card.includes('thumbs') && card.includes('picture'), 'stage labels stay on the right');
  assert(/p24-studio[\s\S]*p24-check[\s\S]*J2290/.test(card) || (card.includes('Studio-wide') && card.includes('is-done') && card.includes('J2290')),
    'studio-wide jobs use the same checklist treatment');
  // Older snapshots with only moved[] still render cards.
  const legacy = t.progressCard({progress24h: {hours: 24, jobsDone: 3, videoJobs: 2, milestones: 1, moved: p24.moved.slice(0, 1), films: []}});
  assert(legacy.includes('p24-film-card') && legacy.includes('OWB 031') && legacy.includes('56% → 67%'), 'legacy moved-only snapshots still show a film card');
  // Live board.json shape on 6 Nov: non-empty older films[] (count+last, no items/status) plus moved[] with 031 missing from films.
  const liveLegacy = t.progressCard({progress24h: {
    hours: 24, jobsDone: 57, videoJobs: 30, otherJobs: 27, milestones: 3,
    moved: [
      {key: 'OWB:031', title: 'What Happens When Earths Magnetic Field Flips', from: 56, to: 67, milestones: 1},
      {key: 'OWB:032', title: 'What Would Happen If You Landed On Titan', from: 56, to: 67, milestones: 1},
      {key: 'OWB:033', title: 'Why Knocked-Sideways Uranus Has 21-Year Winters', from: 44, to: 56, milestones: 1},
    ],
    films: [
      {film: 'OWB:032', title: 'What Would Happen If You Landed On Titan', jobs: 4, last: 'Titan Short v11 cover'},
      {film: 'OWB:033', title: 'Why Knocked-Sideways Uranus Has 21-Year Winters', jobs: 2, last: 'Chief: resolve 033 picture orphan-review'},
    ],
  }});
  assert(liveLegacy.includes('OWB 031') && liveLegacy.includes('OWB 032') && liveLegacy.includes('OWB 033'), 'moved films missing from films[] still appear');
  assert(liveLegacy.includes('56% → 67%') && liveLegacy.includes('44% → 56%'), 'moved % change is copied onto legacy film cards');
  assert(!liveLegacy.includes('worked on, no stage closed'), 'films that closed a stage do not say no stage closed');
  assert(liveLegacy.includes('Titan Short v11 cover') && liveLegacy.includes('Chief: resolve 033 picture orphan-review'),
    'until items[] exist, the last job title remains the fallback line');
  assert(liveLegacy.includes('p24-check') && liveLegacy.includes('is-open'),
    'legacy last-title fallback still shows as an open checklist row');
  const ov = t.overview({tracker: {videos: []}, progress24h: p24, machines: {machines: []}}, Date.parse('2026-11-06T19:41:00Z'));
  assert(ov.includes('p24-film-card') && ov.includes('Last 24 hours'), 'Overview includes the film job cards');
  assert(ov.includes('p24-check') && ov.includes('data-job-state="progress"'), 'Overview checklist marks survive the full overview render');
  assert(ov.includes('p24-glance') && !ov.includes('Next to go live') && !ov.includes('overview-next-live'),
    'Overview glance strip stays; Next to go live stays off home');
  // After-only boards must not raise Needs attention (Ben, 6 Nov ~23:20).
  assert(!ov.includes('overview-attention') && !ov.includes('Needs attention'),
    'pipeline after-waits alone do not open Needs attention');
  assert(ov.indexOf('overview-machines') < ov.indexOf('overview-activity'),
    'Machines sit above Active jobs');
  assert(ov.indexOf('overview-activity') < ov.indexOf('overview-working'),
    'Active jobs sit above Working on now');
  assert(ov.indexOf('overview-working') < ov.indexOf('overview-last24'),
    'Working on now sits above Last 24 hours');
  assert(ov.includes('overview-working') && ov.includes('overview-p24-stats'),
    'Working on now and studio totals are separate sections');
  assert(ov.indexOf('overview-last24') < ov.indexOf('overview-p24-stats'),
    'Last 24 hours sits above Studio totals');
  assert(!ov.includes('overview-agents') && !ov.includes('overview-feature'),
    'Overview home omits Agents cards and the Ready-for-review feature block');
  assert(!/<details[^>]*p24-check-fold[^>]*\sopen/i.test(ov),
    'film checklists stay closed by default');

  // Focus filter (Ben, 6 Nov evening): Overview film cards = studio focus (+ active work); glance matches those cards.
  const focusedBoard = {
    owb: {focus: ['032', 'OWB:032', '031', 'OWB:031', '033', 'OWB:033']},
    progress24h: {
      ...p24,
      moved: [
        ...p24.moved,
        {key: 'OWB:024', title: 'Old Venus film', from: 80, to: 89, milestones: 1},
        {key: 'HOS:006', title: 'Old HOS film', from: 70, to: 78, milestones: 1},
      ],
      films: [
        ...p24.films,
        {film: 'OWB:024', title: 'Old Venus film', jobs: 2, closed: true, from: 80, to: 89, milestones: 1,
          status: '80% → 89%', doneToday: 2, left: 9, blocked: 4, items: []},
        {film: 'HOS:006', title: 'Old HOS film', jobs: 1, closed: true, from: 70, to: 78, milestones: 1,
          status: '70% → 78%', doneToday: 1, left: 8, blocked: 3, items: []},
        {film: 'OWB:ASK:J1356.2', title: 'Housekeeping', jobs: 0, doneToday: 0, left: 9, blocked: 0,
          items: [{kind: 'stage', stage: 'topic', status: 'todo', title: 'topic — not started'}]},
      ],
      glance: {doneToday: 208, left: 208, blocked: 53, blockedJobs: [
        {id: 'J2142', film: 'OWB:032', title: '032 pebble ruler review', status: 'blocked', waitKind: 'after',
          why: 'Will run automatically after J2141 (032 picture harvest)'},
        {id: 'J024x', film: 'OWB:024', title: '024 leftover', status: 'blocked'},
      ], nextLive: p24.glance.nextLive},
    },
  };
  const focused = t.progressCard(focusedBoard);
  assert(focused.includes('Working on now'), 'focus mode labels the film stack as working on now');
  assert(focused.includes('OWB 031') && focused.includes('OWB 032') && focused.includes('OWB 033'), 'focus films stay on Overview');
  assert(!focused.includes('OWB 024') && !focused.includes('HOS 006') && !focused.includes('OWB ASK'),
    'non-focus films without claimed work and housekeeping keys are not shown as Overview cards');
  assert(!focused.includes('Old Venus film') && !focused.includes('Housekeeping'),
    'non-focus titles do not appear on Overview film cards');
  // Glance totals come from the three focus cards (1+1+1 done today, 0+3+0 left); after-waits are not Ben can't-run.
  assert(/<b>3<\/b><span>Done today<\/span>/.test(focused), 'glance done-today matches the focus films on screen');
  assert(/<b>3<\/b><span>Left to go live<\/span>/.test(focused), 'glance left matches the focus films on screen');
  assert(/<b>0<\/b><span>Can't run yet<\/span>/.test(focused), 'glance can\'t-run ignores pipeline after-waits');
  assert(!focused.includes('Could a Robot Survive on Mars?'), 'next-to-go-live titles are not mixed into Last 24 hours / Working on now');
  const focusedOv = t.overview({tracker: {videos: []}, machines: {machines: []}, ...focusedBoard}, Date.parse('2026-11-06T19:41:00Z'));
  assert(!focusedOv.includes('Needs attention') && !focusedOv.includes('overview-attention'),
    'after-wait glance jobs do not raise Needs attention');

  // Working-on-now active-work marker (Ben, 6 Nov ~22:58 / ~23:07): green pulse only when a film has a claimed job.
  const activeCard = t.p24FilmCard({
    film: 'OWB:032', title: 'What Would Happen If You Landed On Titan', status: '56% → 67%', from: 56, to: 67,
    items: [{id: 'J2141', title: '032 picture harvest', status: 'claimed', stage: 'picture'}],
  });
  assert(activeCard.includes('p24-working-dot') && activeCard.includes('is-working'),
    'claimed/in-progress film card shows the top-left working marker');
  assert(activeCard.includes('aria-label="A job is in progress on this film"'),
    'working marker has an accessible name');
  assert(activeCard.includes('p24-check-fold') && activeCard.includes('p24-film-summary') && activeCard.includes('Jobs checklist'),
    'working film row expands to the jobs checklist');
  assert(activeCard.includes('p24-job-spinner') && activeCard.includes('data-job-state="progress"'),
    'expanded in-progress checklist row shows a spinner mark');
  assert(t.p24FilmHasActiveWork({film: 'OWB:032', items: [{id: 'J2141', status: 'claimed'}]}),
    'helper treats claimed checklist jobs as active work');
  const waitingCard = t.p24FilmCard({
    film: 'OWB:032', title: 'Titan', status: '56% → 67%',
    items: [{id: 'J2142', title: '032 pebble ruler review', status: 'blocked', waitKind: 'after',
      why: 'Will run automatically after J2141 (032 picture harvest)'}],
  });
  assert(!waitingCard.includes('p24-working-dot') && !waitingCard.includes('is-working'),
    'will-run-after / waiting films do not get the working marker');
  assert(waitingCard.includes('p24-check-fold') && waitingCard.includes('Will run automatically after J2141'),
    'waiting films still expand to show will-run-after on the checklist');
  assert(waitingCard.includes('Can&#39;t run 0'), 'after-waits do not inflate the film Can\'t run count');
  const openCard = t.p24FilmCard({
    film: 'OWB:031', title: 'Magnetic Field',
    items: [{id: 'J1914', title: 'queued picture job', status: 'open', stage: 'picture'}],
  });
  assert(!openCard.includes('p24-working-dot') && !openCard.includes('is-working'),
    'open/queued jobs alone do not get the working marker');
  const doneCard = t.p24FilmCard({
    film: 'OWB:033', title: 'Uranus',
    items: [{id: 'J2200', title: 'done job', status: 'done', when: 'today'}],
  });
  assert(!doneCard.includes('p24-working-dot'), 'done-only films do not get the working marker');
  const emptyCard = t.p24FilmCard({film: 'OWB:034', title: 'Empty', items: []});
  assert(!emptyCard.includes('p24-check-fold') && emptyCard.includes('<article'),
    'films with no jobs stay a compact article with no expand control');
  // Live claimed job on the board still lights the card even if progress24 items lag.
  const liveBoard = {
    tracker: {videos: [v({key: 'OWB:032', title: 'Titan', jobs: [{id: 'Jlive', status: 'claimed', by: 'codex'}]})]},
    owb: {jobs: [{id: 'Jlive', status: 'claimed', by: 'codex', film: '032', repo: 'owb', title: '032 live claim'}]},
  };
  assert(t.p24FilmHasActiveWork({film: 'OWB:032', items: []}, liveBoard),
    'live claimed board job for the film counts as active work');
  assert(t.p24FilmCard({film: 'OWB:032', title: 'Titan', items: []}, liveBoard).includes('p24-working-dot'),
    'film card shows the marker from a live claimed board job');
  assert(card.includes('is-working') && card.includes('p24-working-dot') && card.includes('J2141'),
    'progressCard film with claimed J2141 carries the working marker');
  // CSS keeps the pulse for motion, static green for prefers-reduced-motion.
  const css = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/studio_app.html'), 'utf8');
  assert(css.includes('p24-working-pulse') && css.includes('prefers-reduced-motion: no-preference'),
    'working-dot pulses only when motion is preferred');
  assert(/prefers-reduced-motion:\s*reduce[\s\S]*p24-working-dot[\s\S]*animation:\s*none/.test(css),
    'prefers-reduced-motion keeps a static green working-dot');
  assert(css.includes('overview-spin') && /prefers-reduced-motion:\s*no-preference[\s\S]*aj-icon::before[\s\S]*overview-spin/.test(css),
    'Active jobs circle spins when motion is preferred');
  assert(/prefers-reduced-motion:\s*no-preference[\s\S]*p24-job-spinner[\s\S]*overview-spin/.test(css),
    'expanded in-progress checklist spinner animates when motion is preferred');
  assert(/prefers-reduced-motion:\s*reduce[\s\S]*aj-icon::before[\s\S]*animation:\s*none/.test(css)
    && /prefers-reduced-motion:\s*reduce[\s\S]*p24-job-spinner[\s\S]*animation:\s*none/.test(css),
    'prefers-reduced-motion keeps Active jobs and checklist spinners static');
  // Tab bar is a flex footer on the viewport, not position:fixed mid-document (Ben, 6 Nov ~23:55).
  assert(/html\s*\{[^}]*height:\s*100dvh/.test(css) && /body\s*\{[^}]*display:\s*flex[^}]*flex-direction:\s*column/.test(css),
    'html/body use a 100dvh flex column app shell');
  assert(/body\s*\{[^}]*overflow:\s*hidden/.test(css), 'body does not scroll — main#view does');
  assert(/main#view\s*\{[^}]*overflow-y:\s*auto/.test(css) && /main#view\s*\{[^}]*min-height:\s*0/.test(css),
    'main#view is the scrolling pane above the tab bar');
  assert(/nav#nav\s*\{[^}]*flex:\s*0\s+0\s+auto/.test(css), 'tab bar is a non-shrinking flex footer');
  assert(!/nav#nav\s*\{[^}]*position:\s*fixed/.test(css),
    'tab bar is not position:fixed (iOS left it between Working and Studio totals)');
  assert(/safe-area-inset-bottom/.test(css), 'tab bar padding includes iPhone safe-area');
  assert(source.includes('scrollAppTop') && source.includes('pane.scrollTo'),
    'hash changes scroll the app-shell main pane, not window');

  // Tonight's Needs attention shape (Ben, 6 Nov ~23:20): after + parked-for-Chief + Chief: leftover → hide banner.
  const tonightBoard = {
    owb: {focus: ['032', '031', '033']},
    progress24h: {
      hours: 24, jobsDone: 10, videoJobs: 8, milestones: 1,
      glance: {doneToday: 2, left: 5, blocked: 4, blockedJobs: [
        {id: 'J0979', film: 'OWB:032', status: 'blocked', waitKind: 'after',
          why: 'Will run automatically after J2089 (032 picture harvest)'},
        {id: 'J2299', film: 'OWB:033', status: 'blocked', waitKind: 'blocker',
          title: '033 picture: correct source identities',
          why: 'Needs: parked for Chief: approve a specific R01 fallback or genuinely new bounded source approach'},
        {id: 'J2300', film: 'OWB:033', status: 'open', waitKind: 'after',
          why: 'Will run automatically after J2299 (033 picture: correct source identities)'},
        {id: 'J1754', film: 'OWB:031', status: 'blocked', waitKind: 'blocker', kind: 'chief',
          title: 'Chief: review workflow handoff',
          why: 'Needs: J1914 directly observed installed AND loaded relay'},
      ]},
      films: [
        {film: 'OWB:032', title: 'Titan', doneToday: 1, left: 1, blocked: 1, items: [
          {id: 'J0979', title: '032 Shorts B+C', status: 'blocked', waitKind: 'after',
            why: 'Will run automatically after J2089 (032 picture harvest)'},
        ]},
        {film: 'OWB:031', title: 'Magnetic Field', doneToday: 0, left: 1, blocked: 1, items: [
          {id: 'J1754', title: 'Chief: review workflow handoff', status: 'blocked', waitKind: 'blocker', kind: 'chief',
            why: 'Needs: J1914 directly observed installed AND loaded relay'},
        ]},
        {film: 'OWB:033', title: 'Uranus', doneToday: 1, left: 2, blocked: 2, items: [
          {id: 'J2299', title: '033 picture: correct source identities', status: 'blocked', waitKind: 'blocker',
            why: 'Needs: parked for Chief: approve a specific R01 fallback'},
          {id: 'J2300', title: '033 follow-on', status: 'open', waitKind: 'after',
            why: 'Will run automatically after J2299'},
        ]},
      ],
      moved: [],
    },
  };
  const tonightOv = t.overview({tracker: {videos: []}, machines: {machines: []}, ...tonightBoard}, Date.parse('2026-11-06T23:20:00Z'));
  assert(!tonightOv.includes('overview-attention') && !tonightOv.includes('Needs attention'),
    'tonight\'s after/Chief leftovers do not raise Needs attention');
  assert(/<b>0<\/b><span>Can't run yet<\/span>/.test(tonightOv), 'glance Can\'t run is 0 for tonight\'s non-Ben waits');
  assert(tonightOv.includes('Will run automatically after J2089') && tonightOv.includes('Will run automatically after J2299'),
    'sequential waits remain visible in the expanded film checklist');
  assert(tonightOv.includes('Can&#39;t run 0'), 'film rows do not count after/Chief waits as Can\'t run');
  // A real Ben UAT wait still raises Needs attention.
  const benWaitBoard = {
    owb: {focus: ['032']},
    progress24h: {
      hours: 24, jobsDone: 1, videoJobs: 1, milestones: 0,
      glance: {doneToday: 0, left: 1, blocked: 1, blockedJobs: [
        {id: 'J0999', film: 'OWB:032', status: 'blocked', waitKind: 'blocker', awaits_ben: true,
          title: '032 Final OK watch', why: 'Needs Ben: watch the finished cut in UAT and Approve or Request changes'},
      ]},
      films: [{film: 'OWB:032', title: 'Titan', doneToday: 0, left: 1, blocked: 1, items: [
        {id: 'J0999', title: '032 Final OK watch', status: 'blocked', waitKind: 'blocker', awaits_ben: true,
          why: 'Needs Ben: watch the finished cut in UAT and Approve or Request changes'},
      ]}],
      moved: [],
    },
  };
  const benOv = t.overview({tracker: {videos: []}, machines: {machines: []}, ...benWaitBoard}, Date.parse('2026-11-06T23:20:00Z'));
  assert(benOv.includes('overview-attention') && benOv.includes('Needs attention') && benOv.includes('J0999'),
    'a Ben UAT wait still appears in Needs attention');
  assert(benOv.includes('Needs Ben: watch the finished cut') && benOv.indexOf('overview-attention') < benOv.indexOf('overview-machines'),
    'Ben-facing banner sits above Machines and names the watch reason');
  assert(/<b>1<\/b><span>Can't run yet<\/span>/.test(benOv) && benOv.includes('Can&#39;t run 1'),
    'Ben UAT wait counts in glance and the film Can\'t run line');

  // Active non-focus film appears with pulse; Active jobs names the video (Ben, 6 Nov ~23:21 / ~23:33).
  const betelgeuseShort = v({
    key: 'OWB:029:S:heiGCnGKTkE', channel: 'OWB', number: '029', type: 'short',
    title: 'How Bright Will Betelgeuse Get When It Explodes?',
    jobs: [{id: 'J2311', status: 'claimed', by: 'cursor', title: '029 Short Betelgeuse cut', progress: {step: 1, of: 5}}],
  });
  const betelgeuseLong = v({
    key: 'OWB:029', channel: 'OWB', number: '029', type: 'long',
    title: 'Is Betelgeuse About to Explode?',
    jobs: [], // progress24h items empty — checklist must hydrate from the claimed Short job
  });
  const activeOutsideFocus = {
    models: {checkedAt: new Date(Date.parse('2026-11-06T23:21:00Z')).toISOString()},
    tracker: {videos: [
      betelgeuseLong,
      betelgeuseShort,
      v({key: 'OWB:032', title: 'What Would Happen If You Landed On Titan'}),
      v({key: 'OWB:031', title: 'What Happens When Earths Magnetic Field Flips'}),
      v({key: 'OWB:033', title: 'Why Knocked-Sideways Uranus Has 21-Year Winters'}),
    ]},
    owb: {
      focus: ['032', '031', '033'],
      jobs: [{id: 'J2311', status: 'claimed', by: 'cursor', film: '029', repo: 'owb',
        title: '029 Short Betelgeuse cut', claimedAt: new Date(Date.parse('2026-11-06T23:21:00Z')-5*6e4).toISOString(),
        progress: {step: 1, of: 5}, taskKeys: ['OWB:029:S:heiGCnGKTkE']}],
    },
    progress24h: {
      hours: 24, jobsDone: 4, videoJobs: 3, milestones: 1,
      glance: {doneToday: 3, left: 4, blocked: 0, blockedJobs: []},
      films: [
        {film: 'OWB:032', title: 'What Would Happen If You Landed On Titan', doneToday: 1, left: 1, blocked: 0,
          from: 56, to: 67, items: [{id: 'J0979', title: '032 wait', status: 'blocked', waitKind: 'after',
            why: 'Will run automatically after J2089'}]},
        {film: 'OWB:031', title: 'What Happens When Earths Magnetic Field Flips', doneToday: 1, left: 1, blocked: 0, items: []},
        {film: 'OWB:033', title: 'Why Knocked-Sideways Uranus Has 21-Year Winters', doneToday: 1, left: 2, blocked: 0, items: []},
        // Parent long with empty items — the bug: pulsed as a bare article with Left 0.
        {film: 'OWB:029', title: 'Is Betelgeuse About to Explode?', doneToday: 0, left: 0, blocked: 0,
          from: 89, to: 78, items: []},
      ],
      moved: [
        {key: 'OWB:032', title: 'What Would Happen If You Landed On Titan', from: 56, to: 67, milestones: 1},
        {key: 'OWB:029', title: 'Is Betelgeuse About to Explode?', from: 89, to: 78, milestones: -1},
      ],
    },
    machines: {machines: []},
  };
  const nowActive = Date.parse('2026-11-06T23:21:00Z');
  const activeOv = t.overview(activeOutsideFocus, nowActive);
  assert(activeOv.includes('OWB 032') && activeOv.includes('OWB 031') && activeOv.includes('OWB 033'),
    'focus films without claimed work still appear');
  assert(activeOv.includes('Is Betelgeuse About to Explode?') && activeOv.includes('How Bright Will Betelgeuse Get When It Explodes?'),
    'claimed work on a non-focus film adds that film to Working on now');
  assert(!activeOv.includes('Old Venus film'), 'films with only recent work stay off Working on now');
  assert(activeOv.includes('OWB 029 Short') && !activeOv.includes('heiGCnGKTkE'),
    'Short heading uses a readable label, not the raw YouTube id');
  const workingHtml = t.workingOnNow(activeOutsideFocus);
  assert(workingHtml.includes('is-working') && workingHtml.includes('p24-working-dot') && workingHtml.includes('OWB 029'),
    'non-focus film with claimed work gets the green pulsing marker');
  assert(!t.p24FilmCard(activeOutsideFocus.progress24h.films[0], activeOutsideFocus).includes('is-working'),
    '032 without claimed work has no working marker');
  assert(!t.p24FilmCard(activeOutsideFocus.progress24h.films[1], activeOutsideFocus).includes('is-working'),
    '031 without claimed work has no working marker');
  assert(!t.p24FilmCard(activeOutsideFocus.progress24h.films[2], activeOutsideFocus).includes('is-working'),
    '033 without claimed work has no working marker');
  // Parent long with empty progress24h items must still expand (Ben, 6 Nov ~23:33).
  const long029 = t.p24FilmCard(activeOutsideFocus.progress24h.films[3], activeOutsideFocus);
  assert(long029.includes('is-working') && long029.includes('p24-working-dot'),
    'parent long with empty items still pulses from the claimed Short job');
  assert(long029.includes('p24-check-fold') && long029.includes('p24-film-expand') && !/^[\s\S]*<article class="[^"]*is-working/.test(long029),
    'pulsing parent long is a closed details checklist, not a bare article');
  assert(long029.includes('J2311') && long029.includes('p24-job-spinner') && long029.includes('data-job-state="progress"'),
    'hydrated long checklist shows the in-progress job with a spinner');
  assert(long029.includes('Left 1') && !long029.includes('Left 0'),
    'hydrated long meta Left counts the claimed job, not the empty progress24h left:0');
  const short029 = t.p24FilmCard({film: 'OWB:029:S:heiGCnGKTkE', title: 'How Bright Will Betelgeuse Get When It Explodes?', items: []}, activeOutsideFocus);
  assert(short029.includes('p24-check-fold') && short029.includes('is-working') && short029.includes('J2311') && short029.includes('p24-job-spinner'),
    'Short row also expands with the in-progress job spinner');
  assert(short029.includes('OWB 029 Short') && short029.includes('Left 1'),
    'Short row uses a readable id and Left reflects the claimed job');
  assert((workingHtml.match(/p24-check-fold/g)||[]).length >= 3,
    '032 checklist plus both pulsing Betelgeuse rows use expand checklists');
  const aj = t.activityCard(activeOutsideFocus, nowActive);
  assert(aj.includes('aj-icon') && aj.includes('Cursor is working') && aj.includes('J2311'),
    'Active jobs still shows the running agent and job id');
  assert(aj.includes('How Bright Will Betelgeuse Get When It Explodes?') && aj.includes('OWB 029'),
    'Active job card names the video id and title, not a generic Video production label');
  assert(!/J2311 · Video production/.test(aj), 'Active job subline is not the generic category when a video is linked');
}
console.log('Last-24-hours film cards OK');

// Working on now checklist = run / hierarchy order, not raw job-id order (Ben, 7 Nov ~00:26).
{
  // Titan: J0979 waits on J2089 — prerequisite stays above even when listed first by id.
  const titan = t.p24SortFilmItems([
    {id: 'J0979', title: '032 Shorts B+C', status: 'blocked', waitKind: 'after',
      after: 'J2089', why: 'Will run automatically after J2089 (032 picture harvest)'},
    {id: 'J2089', title: '032 picture harvest', status: 'claimed', progress: {step: 1, of: 5}},
  ]);
  assert.deepEqual(titan.map(j => j.id), ['J2089', 'J0979'],
    'Titan: J2089 (prerequisite) appears above J0979 (waits after it)');
  const titanCard = t.p24FilmCard({
    film: 'OWB:032', title: 'What Would Happen If You Landed On Titan',
    items: [
      {id: 'J0979', title: '032 Shorts B+C', status: 'blocked', waitKind: 'after',
        after: 'J2089', why: 'Will run automatically after J2089 (032 picture harvest)'},
      {id: 'J2089', title: '032 picture harvest', status: 'claimed', progress: {step: 1, of: 5}},
    ],
  });
  assert(titanCard.indexOf('J2089') < titanCard.indexOf('J0979'),
    'expanded Titan checklist HTML keeps J2089 above J0979');

  // HOS 009: newer "Verify condition for JX" ids sit below their targets by number — must render above.
  const hosItems = [
    {id: 'J1275', title: 'HOS 009/010: merge PR #389', status: 'blocked', waitKind: 'blocker',
      progress: {step: 2, of: 4}},
    {id: 'J2033', title: 'HOS 009: Mint the remaining 20 approved HOS009 Quality rows',
      status: 'blocked', waitKind: 'blocker', stage: 'picture', progress: {step: 0, of: 3}},
    {id: 'J2034', title: 'HOS 009: review Quality mint', status: 'open', progress: {step: 0, of: 3}},
    {id: 'J2200', title: 'HOS 009: build tested tranche-2 Flow mint runner',
      status: 'blocked', waitKind: 'blocker', stage: 'picture', progress: {step: 5, of: 5}},
    {id: 'J2281', title: 'Verify condition for J0862', status: 'blocked', waitKind: 'blocker',
      recheck_of: 'J0862', progress: {step: 3, of: 3}},
    {id: 'J2293', title: 'Verify condition for J2200', status: 'blocked', waitKind: 'blocker',
      recheck_of: 'J2200', progress: {step: 3, of: 3}},
    {id: 'J2322', title: 'Verify condition for J2033', status: 'claimed',
      recheck_of: 'J2033', progress: {step: 0, of: 3}},
  ];
  const hos = t.p24SortFilmItems(hosItems);
  const hosIds = hos.map(j => j.id);
  assert(hosIds.indexOf('J2322') < hosIds.indexOf('J2033'),
    'HOS 009: Verify condition for J2033 appears above J2033');
  assert(hosIds.indexOf('J2293') < hosIds.indexOf('J2200'),
    'HOS 009: Verify condition for J2200 appears above J2200');
  assert(hosIds.indexOf('J2322') < hosIds.indexOf('J1275'),
    'in-progress verify is preferred among ready roots over older blocked jobs');
  // Title-only signal (no recheck_of) still orders correctly.
  const byTitle = t.p24SortFilmItems([
    {id: 'J2033', title: 'Mint rows', status: 'blocked', waitKind: 'blocker'},
    {id: 'J2322', title: 'Verify condition for J2033', status: 'claimed'},
  ]);
  assert.deepEqual(byTitle.map(j => j.id), ['J2322', 'J2033'],
    'title "Verify condition for JX" alone places the verifier above JX');
  const hosCard = t.p24FilmCard({film: 'HOS:009', title: 'HOS 009', items: hosItems.slice().reverse()});
  assert(hosCard.indexOf('J2322') < hosCard.indexOf('J2033')
    && hosCard.indexOf('J2293') < hosCard.indexOf('J2200'),
    'expanded HOS 009 checklist HTML is hierarchy order, not reverse id order');
  // afterChain from progress24 also orders multi-step waits.
  const chain = t.p24SortFilmItems([
    {id: 'J2143', title: '032 package', status: 'open', waitKind: 'after',
      after: 'J2142', afterChain: [{id: 'J2141'}, {id: 'J2142'}],
      why: 'Will run automatically after J2141 and J2142'},
    {id: 'J2142', title: '032 Shorts edit', status: 'open', after: 'J2141'},
    {id: 'J2141', title: '032 picture harvest', status: 'claimed'},
  ]);
  assert.deepEqual(chain.map(j => j.id), ['J2141', 'J2142', 'J2143'],
    'afterChain / after pipeline keeps A → B → C top to bottom');
}
console.log('Working checklist hierarchy order OK');

// Jobs running counts the jobs on video cards too (5 Nov 2026: Mini + MacBook both working showed as 1).
{
  const sb = {tracker: {videos: [v({key: 'OWB:032', jobs: [{id: 'J2176', status: 'claimed', by: 'codex'}]})]},
    owb: {jobs: [{id: 'J2165', status: 'claimed', by: 'macbook'}, {id: 'J2176', status: 'claimed', by: 'codex'}]}, models: {}};
  assert.equal(t.summary(sb, NOW).jobs.working, 2);
  assert.equal(t.summary({...sb, owb: {jobs: [{id: 'J2165', status: 'claimed'}]}}, NOW).jobs.working, 2);
}
console.log('Jobs running count checks OK');
