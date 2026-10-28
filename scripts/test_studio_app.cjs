// Studio app (05_Analytics/kanban/board_site/studio_app.js): Ben's review queue is finished videos only, progress is
// reported steps only, the schedule has one row per slot, and every tab renders from a real board.json.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/studio_app.js'), 'utf8');
const hook = '  // STUDIO_APP_TEST_HOOK';
assert(source.includes(hook), 'studio_app.js keeps its test hook');
const context = {Date, console, location: {hash: ''}, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {renderTab, summary, schedule, progressOf, forBen, stage, tickDoc, canTick};
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
assert(review.includes('Watch v06') && review.includes('/board#v=OWB%3A019'), 'Watch plays the file; OK or changes opens the card on /board');
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
assert(review.includes('data-ok="OWB:019"') && review.includes('data-chg="OWB:019"'), 'OK and Changes are on the review card');
console.log('studio app OK');
