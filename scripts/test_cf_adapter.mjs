import assert from 'node:assert/strict';
import { adapt } from '../05_Analytics/kanban/board_site/cf_adapter.js';
import checks from '../05_Analytics/kanban/board_site/api/checks.js';
import data, { forget } from '../05_Analytics/kanban/board_site/api/data.js';
import pair from '../05_Analytics/kanban/board_site/api/pair.js';
import ref from '../05_Analytics/kanban/board_site/api/ref.js';
import watch from '../05_Analytics/kanban/board_site/api/watch.js';
import { makeSession } from '../05_Analytics/kanban/board_site/benauth.js';
const RealDate = Date;
globalThis.Date = class extends RealDate { constructor(...a) { super(...(a.length ? a : [1800000000000])); } static now() { return 1800000000000; } };
Object.assign(process.env, { BOARD_KEY:'test-key', BOARD_GH_TOKEN:'test-token', WATCH_LINK_SECRET:'test-secret', BOARD_OPEN_TAPS:'0', R2_ACCOUNT_ID:'account', R2_ACCESS_KEY_ID:'key', R2_SECRET_ACCESS_KEY:'secret', R2_PUBLIC_URL:'https://media.example' });
globalThis.fetch = async (url) => {
  if (String(url).includes('.r2.cloudflarestorage.com')) return new Response('<ListBucketResult><Contents><Key>watch/test/clip.mp4</Key><LastModified>2026-11-12T00:00:00Z</LastModified></Contents></ListBucketResult>');
  if (String(url).includes('/git/ref/')) return Response.json({object:{sha:'a'.repeat(40)}});
  if (String(url).includes('/issues/')) return Response.json({updated_at:'now',body:'```json\n{"checks":{},"history":[],"pairs":[]}\n```'});
  return Response.json({hello:'world'});
};
async function direct(handler, request) {
 const headers = new Headers(); let status=200, body=null;
 const res={setHeader(k,v){headers.set(k,v);return this},status(n){status=n;return this},json(j){headers.set('Content-Type','application/json; charset=utf-8');body=JSON.stringify(j);return this},send(b){body=b;return this},end(){return this}};
 const u=new URL(request.url);
 const req={method:request.method,headers:{...Object.fromEntries(request.headers),host:u.host},query:Object.fromEntries(u.searchParams)};
 if(request.method==='POST')req.body=await request.text();
 await handler(req,res);
 return {status,headers:[...headers],body:body??''};
}
for(const [name,handler,query] of [['checks',checks,'?stamp=1'],['data',data,'?f=ref'],['pair',pair,''],['ref',ref,''],['watch',watch,'?v=test']]){
 const req=new Request('https://board.example/api/'+name+query,{headers:{'x-board-key':'test-key'}});
 forget();const expected=await direct(handler,req.clone());forget();const actual=await adapt(handler,req);
 assert.equal(actual.status,expected.status,name);assert.deepEqual([...actual.headers],expected.headers,name);assert.equal(await actual.text(),expected.body,name);
 if(name==='watch')assert.equal(actual.status,302);
}
const cookie='studio_ben='+makeSession('test-key');
const linked=await adapt(checks,new Request('https://board.example/api/checks?stamp=1',{headers:{cookie}}));
assert.equal(linked.status,200);assert.match(linked.headers.get('set-cookie'),/HttpOnly; Secure; SameSite=Lax/);
const post=await adapt(checks,new Request('https://board.example/api/checks',{method:'POST',headers:{cookie,'content-type':'application/json'},body:JSON.stringify({id:'migration-test',dryRun:true})}));
assert.equal((await post.json()).auth,'cookie');
console.log('PASS: five route contracts, watch 302, cookie renewal/readback and POST body');

const worker = (await import('../05_Analytics/kanban/board_site/cf_worker.js')).default;
for (const route of ['checks?stamp=1', 'missing']) {
  const response = await worker.fetch(new Request('https://board.example/api/' + route), {});
  assert.equal(response.headers.get('X-Robots-Tag'), 'noindex, nofollow');
}
console.log('PASS: API responses and errors excluded from search');
