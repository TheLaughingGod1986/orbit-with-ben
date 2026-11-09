// Read-only resolution. Never print or persist credentials, signed URLs or random object keys.
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { r2Config, newestWatchUrl } from '/Users/benjaminoats/YouTube/orbit-with-ben/05_Analytics/kanban/board_site/r2sign.js';
const root='/Users/benjaminoats/YouTube/orbit-with-ben';
const env={};
for(const line of readFileSync(root+'/07_Content-Ops/.env','utf8').split(/\r?\n/)){
  const m=/^\s*(?:export\s+)?(R2_[A-Z_]+)\s*=\s*(.*?)\s*$/.exec(line);
  if(m) env[m[1]]=m[2].replace(/^(['"])(.*)\1$/,'$2');
}
const cfg=r2Config({...env,...process.env});
if(!cfg) throw new Error('R2 configuration unavailable');
const regs=JSON.parse(readFileSync(new URL('watch_registers.json',import.meta.url)));
const ids=[...new Set(Object.values(regs).flatMap(x=>Object.values(x)))];
const rows=[];
for(const id of ids){
  try{
    const url=await newestWatchUrl(cfg,id);
    if(!url){rows.push({id,status:'no object'});continue;}
    const res=await fetch(url);
    if(!res.ok){rows.push({id,status:res.status});continue;}
    const h=createHash('sha256');let size=0;
    for await(const chunk of res.body){h.update(chunk);size+=chunk.length;}
    rows.push({id,store:'R2 owb-media',prefix:`watch/${id}/`,filename:decodeURIComponent(new URL(url).pathname.split('/').pop()).replace(/^[a-f0-9]{16}-/,''),bytes:size,sha256:h.digest('hex'),status:res.status});
  }catch(e){rows.push({id,error:'read failed; credential and URL detail suppressed'});}
}
writeFileSync(new URL('r2_resolution.json',import.meta.url),JSON.stringify({at:new Date().toISOString(),objects:rows},null,2)+'\n');
console.log(JSON.stringify({ids:ids.length,read:rows.filter(r=>r.status===200).length}));
