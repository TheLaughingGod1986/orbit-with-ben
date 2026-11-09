// AI & credits page (05_Analytics/kanban/board_site/ai_app.js): traffic lights, stale and low pools, burn rate, Chief.
const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/ai_app.js'), 'utf8');
const hook = '  // AI_APP_TEST_HOOK';
assert(source.includes(hook), 'ai_app.js keeps its test hook');
const context = {Date, console, document: {getElementById: () => ({})}, window: {}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf(hook)) + `
  globalThis.test = {renderAI, poolState, burnPerDay, poolTotal};
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
for (const want of ['Acting Chief', 'Grok', 'Agents & models', 'Credit left', 'ElevenLabs', 'almost out', 'Plans', 'Where it went'])
  assert(html.includes(want), `page shows ${want}`);
assert(!html.includes('<script>'), 'text from the data is escaped');
assert(t.renderAI({}, NOW).includes('No data yet'));
console.log('ai page OK');
