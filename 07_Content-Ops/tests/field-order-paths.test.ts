import { afterEach, describe, expect, it } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { latestSnapshot, queueRoot } from '../scripts/field-order-dispatch';
const temporary:string[]=[];
afterEach(()=>{for(const dir of temporary.splice(0))fs.rmSync(dir,{recursive:true,force:true});});
function fixture(){
 const base=fs.mkdtempSync(path.join(os.tmpdir(),'field-order-paths-'));temporary.push(base);
 const engine=path.join(base,'engine');
 const queue=path.join(base,'shared-studio');
 for(const root of [engine,queue]){
  for(const dir of ['channels','scripts','jobs'])fs.mkdirSync(path.join(root,dir),{recursive:true});
  fs.writeFileSync(path.join(root,'channels/channels.json'),JSON.stringify({studio:{github:'fixture/studio'}}));
  fs.writeFileSync(path.join(root,'scripts/jobs.py'),'# fixture');
  fs.writeFileSync(path.join(root,'jobs/queue.json'),JSON.stringify({jobs:[]}));
 }
 return {base,engine,queue};
}
describe('Field Order detached record and queue paths',()=>{
 it('selects the latest dated snapshot from the supplied channel records, ignoring sidecars',()=>{
  const {base}=fixture();const dir=path.join(base,'ww2/05_Analytics/ww2/snapshots');fs.mkdirSync(dir,{recursive:true});
  for(const [file,date] of [['2026-11-18.json','2026-11-18'],['2026-11-19.json','2026-11-19'],['latest.tmp','bad']]){
   fs.writeFileSync(path.join(dir,file),JSON.stringify({channel:'ww2',date}));
  }
  expect(latestSnapshot(dir).date).toBe('2026-11-19');
 });
 it('refuses an empty snapshot folder without queue work',()=>{
  const {base}=fixture();const dir=path.join(base,'empty');fs.mkdirSync(dir);
  expect(()=>latestSnapshot(dir)).toThrow('No Field Order History snapshot');
 });
 it('uses a separate shared studio queue when its identity matches the executing engine',()=>{
  const {engine,queue}=fixture();expect(queueRoot(engine,queue)).toBe(queue);
 });
 it('refuses a retained channel engine even when it has a valid-looking queue',()=>{
  const {engine,queue}=fixture();
  fs.writeFileSync(path.join(queue,'channels/channels.json'),JSON.stringify({studio:{github:'fixture/old-channel'}}));
  expect(()=>queueRoot(engine,queue)).toThrow('different engine');
  expect(JSON.parse(fs.readFileSync(path.join(queue,'jobs/queue.json'),'utf8'))).toEqual({jobs:[]});
 });
 it('refuses relative, incomplete and corrupt queue checkouts',()=>{
  const {engine,queue}=fixture();
  expect(()=>queueRoot(engine,'relative')).toThrow('absolute');
  fs.writeFileSync(path.join(queue,'jobs/queue.json'),'broken');
  expect(()=>queueRoot(engine,queue)).toThrow('missing');
  fs.rmSync(path.join(queue,'scripts/jobs.py'));
  expect(()=>queueRoot(engine,queue)).toThrow('missing');
 });
});
