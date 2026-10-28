// Studio app (05_Analytics/kanban/board_site/studio_app.js): Ben's review queue is finished videos only, progress is
// reported steps only, the schedule has one row per slot, and every tab renders from a real board.json.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/studio_app.js'), 'utf8');
const hook = '  // STUDIO_APP_TEST_HOOK';
assert(source.includes(hook), 'studio_app.js keeps its test hook');
const context = {Date, console, location: {hash: ''}, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {renderTab, summary, schedule, progressOf, forBen, stage, tickDoc, canTick, uat, agentLight, readiness, videoGroups, doing, detail, miniLine};
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
assert(t.doing(g.working[0]).includes('Codex · cut · Step 3 of 5'), 'the working card says who, what and which step');

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
assert(ov.includes('Plus 1 studio job not tied to one video') && ov.includes('Jobs running'));
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
console.log('studio app OK');
