// AI & credits page (05_Analytics/kanban/board_site/ai_app.js): traffic lights, stale and low pools, burn rate, Chief.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/ai_app.js'), 'utf8');
const hook = '  // AI_APP_TEST_HOOK';
assert(source.includes(hook), 'ai_app.js keeps its test hook');
const context = {Date, console, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {parseWeeklyReset,renderAI, poolState, burnPerDay, poolTotal};
})();`, context);
const t = context.test;
const NOW = Date.parse('2026-10-28T20:00:00Z');
const day = n => new Date(NOW - n * 864e5).toISOString();

// Burn: credit used per day since the last refill only.
assert.equal(t.burnPerDay([[day(4), 1000], [day(2), 800], [day(0), 600]], NOW), 100);
assert.equal(t.burnPerDay([[day(4), 100], [day(3), 25000], [day(1), 24000]], NOW), 500, 'a refill restarts the count');
assert.equal(t.burnPerDay([[day(1), 5]], NOW), null);

const credits = {tiers: {flow: [{name: 'Ultra', allow: 25000, current: true}]}, pools: {}};
// Low pool reads red; a missed daily reading reads amber; a fresh healthy one green.
let s = t.poolState('elevenlabs', {unit: 'credits', latest: {left: 119, total: 209536, at: day(0.5)}, series: []}, credits, NOW);
assert.equal(s.status, 'red'); assert.equal(s.why, 'almost out');
s = t.poolState('vertex', {unit: 'GBP', latest: {left: 71.02, at: day(6)}, series: []}, credits, NOW);
assert.equal(s.status, 'amber'); assert(s.why.startsWith('no reading for 6 days'));
s = t.poolState('flow', {unit: 'credits', latest: {left: 20870, at: day(0.2)}, series: []}, credits, NOW);
assert.equal(s.status, 'green'); assert.equal(s.total, 25000, "Flow's size comes from the current plan tier");
assert.equal(t.poolTotal('codex', {unit: '%', latest: {left: 93}}, credits), 100);

// The whole page renders from a real board.json, escapes text, and names the Chief.
const board = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'ai_board.json'), 'utf8'));
const html = t.renderAI(board, NOW);
for (const want of ['Acting Chief', 'Grok', 'Agents & models', 'Credit left &amp; pace', 'ElevenLabs', 'almost out', 'Cursor &amp; Grok', '<strong>Used</strong>', 'Plans', 'Where it went'])
  assert(html.includes(want), `page shows ${want}`);
assert(!html.includes('<script>'), 'text from the data is escaped');
assert(t.renderAI({}, NOW).includes('No data yet'));
console.log('ai page OK');

// J3024 regressions run against each independently rendered page.
{
 const now = Date.parse('2026-11-17T13:00Z');
 const plan = {tiers: {claude: [{name:'Current', quotaId:'q1', current:true, allow:100, gbp:180}, {name:'Cheaper', allow:50, gbp:90}]}};
 const week = (peak, inCycle) => ({firstAt:'2026-11-01T00:00Z',peakUsed:peak,hitLimit:peak>=100,inCycle,quotaId:'q1',partial:false});
 const pool = {unit:'%',since:'2026-11-01',renews:'2026-12-01',latest:{at:'2026-11-17T12:00Z',left:80,total:100,note:'weekly resets Wednesday 10:00 AM'},weeklyHistory:[week(90,false),week(20,true),week(20,true)]};
 const meter = p => t.poolState('claude', p, plan, now);
 assert(!meter(pool).verdict.includes('Could drop'), 'prior comparable high week vetoes unsafe downgrade');
 pool.weeklyHistory[0].peakUsed=20;
 assert(meter(pool).verdict.includes('Could drop'), 'verified comparable low complete history can support advice');
 pool.weeklyHistory[0].quotaId='old-plan';
 assert(meter(pool).verdict.includes('plan/allowance changed'), 'changed quota cannot be compared as the same percentage');
 delete pool.weeklyHistory[0].quotaId;
 assert(meter(pool).verdict.includes('unknown'), 'unidentified quota withholds advice');
 const expired = t.poolState('codex',{unit:'%',latest:{at:'2026-11-17T12:00Z',left:0,total:100,note:'weekly resets Tue 17 Nov 23:22Z'}},{},Date.parse('2026-11-18T01:00Z'));
 assert.equal(expired.timeShare,null);
 assert.equal(expired.verdict,'');
 assert(/historical.*awaiting refreshed/.test(expired.why));
 const near = t.poolState('claude',{unit:'%',latest:{at:'2026-11-17T12:00Z',left:6,total:100,note:'weekly resets Wednesday 10:00 AM'}},{},now);
 assert(!near.why.includes('at limit'), '94% is near limit, never exhaustion');
}

// J3024 follow-up: reset parsing agrees with explicit provider clocks and years.
{
 const cases = [
  ['weekly resets 18 Nov 2026 10:00Z','2026-11-18T08:00Z','2026-11-18T10:00Z'],
  ['weekly resets Wednesday 10:00 UTC','2026-07-07T12:00Z','2026-07-08T10:00Z'],
  ['weekly resets Wednesday 10:00 GMT','2026-07-07T12:00Z','2026-07-08T10:00Z'],
  ['weekly resets Wednesday 10:00 AM','2026-07-07T12:00Z','2026-07-08T09:00Z'],
  ['weekly resets 2 Jan 2027 10:00Z','2026-12-31T12:00Z','2027-01-02T10:00Z'],
  ['weekly resets Jan 2 2027 10:00 UTC','2026-12-31T12:00Z','2027-01-02T10:00Z'],
  ['weekly resets 2 Jan 2026 10:00Z','2026-12-31T12:00Z','2026-01-02T10:00Z'],
 ];
 for (const [note,at,end] of cases) assert.equal(t.parseWeeklyReset(note,Date.parse(at)).endMs,Date.parse(end),note);
 const p={unit:'%',latest:{at:'2026-11-18T08:00Z',left:0,total:100,note:cases[0][0]}};
 assert(t.poolState('codex',p,{},Date.parse('2026-11-18T09:00Z')).timeShare>0,'before actual reset is current');
 assert.equal(t.poolState('codex',p,{},Date.parse('2026-11-18T10:01Z')).timeShare,null,'after actual reset is historical');
 // Actual unverified subscription metadata must neither hide Time nor the recorded decision.
 const plans=JSON.parse(fs.readFileSync(path.join(__dirname,'../05_Analytics/ai_spend/plans.json'))).subscriptions;
 const now=Date.parse('2026-11-18T09:00Z');
 const flow={unit:'credits',latest:{at:'2026-11-18T08:00Z',left:24500,total:25000},series:[]};
 const c={plans,pools:{flow},tiers:{flow:[{current:true,allow:25000,gbp:189.99,verified:false}]}};
 assert.equal(t.poolState('flow',flow,c,now).timeShare,null,'unknown allowance start cannot borrow unverified billing');
 let html=t.renderAI({credits:c,models:{models:[]},owb:{jobs:[]}},now);
 assert(html.includes('Time unavailable'),'explicit unavailable Time row');
 assert(html.includes('keep Ultra') && html.includes('then review'),'Ben decision visible without computed verdict');
 const known={...flow,allowanceWindow:{verified:true,start:'2026-11-12T00:00Z',end:'2026-12-12T00:00Z'}};
 const state=t.poolState('flow',known,c,now);
 assert(state.timeShare>0 && state.timeShare<1,'verified allowance independent of unverified billing');
 assert(!state.verdict.includes('Could drop'),'allowance evidence does not verify billing or tiers');
 const el={unit:'credits',latest:{at:'2026-11-18T08:00Z',left:67893,total:121114},series:[]};
 const e=t.poolState('elevenlabs',el,{plans},now);
 assert.equal(e.timeShare,null,'reset end alone does not establish duration');
 const ehtml=t.renderAI({credits:{plans,pools:{elevenlabs:el}},models:{models:[]},owb:{jobs:[]}},now);
 assert(ehtml.includes('start unread'),'verified reset date survives unknown billing');
}
