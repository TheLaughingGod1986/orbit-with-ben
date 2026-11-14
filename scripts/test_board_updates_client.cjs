const assert = require('node:assert/strict');
const fs = require('node:fs');
global.window = {};
const source = fs.readFileSync(__dirname + '/../05_Analytics/kanban/board_site/board_updates.js', 'utf8');
const sha = 'a'.repeat(40);
async function run() {
  eval(source);
  let snapshot = { tracker: { videos: [{ key: 'OWB:032', lane: 'progress' }] }, heartbeat: 1 };
  let update = {schema:1, revision:'first', snapshotEtag:'snapshot-one', edits:[]}, reads=0;
  const own = async (query) => { assert.equal(query,'f=updates'); return new Response(JSON.stringify(update), {headers:{'X-Board-Sha':sha}}); };
  const full = async (commit) => {assert.equal(commit,''); reads++; return new Response(JSON.stringify(snapshot), {headers:{'ETag':'"snapshot-one"'}});};
  const initial = await (await window.__boardUpdates(sha, own, full)).json();
  initial.tracker.videos[0].lane='mutated by UI';
  update={schema:1,revision:'second',edits:[{from:'first',to:'second',ops:[['set',['heartbeat'],2]]}]};
  const next=await (await window.__boardUpdates(sha,own,full)).json();
  assert.equal(reads,1);
  assert.equal(next.heartbeat,2);
  assert.equal(next.tracker.videos[0].lane,'progress');
  snapshot={...snapshot,heartbeat:3};
  update={schema:1,revision:'third',edits:[]};
  assert.equal((await (await window.__boardUpdates(sha,own,full)).json()).heartbeat,3);
  assert.equal(reads,2,'missed edit must fetch complete file');
  await assert.rejects(window.__boardUpdates(sha,async()=>{throw Object.assign(new Error('sign in'),{signIn:true});},full),/sign in/);
  assert.equal(reads,2,'401 must not try full data or public fallback');
  // An unmatched branch snapshot must not be assigned the update revision.
  eval(source); reads=0;
  update={schema:1,revision:'r1',snapshotEtag:'different',edits:[]};
  await window.__boardUpdates('',own,full);
  update={schema:1,revision:'r2',snapshotEtag:'snapshot-one',edits:[{from:'r1',to:'r2',ops:[['set',['heartbeat'],99]]}]};
  const recovered=await (await window.__boardUpdates('',own,full)).json();
  assert.equal(reads,2,'mismatched snapshot requires a fresh full read');
  assert.equal(recovered.heartbeat,3,'never apply edits to a different snapshot');
  assert.throws(()=>window.__applyBoardEdits({},[['set',['__proto__','polluted'],true]]),/Unsafe/);
  console.log('Board update chain, UI isolation, missed-window fallback and sign-in checks OK');
}
run().catch(e=>{console.error(e);process.exit(1);});
