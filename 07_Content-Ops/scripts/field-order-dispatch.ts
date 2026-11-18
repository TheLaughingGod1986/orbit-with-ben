#!/usr/bin/env tsx
/** Dispatch Studio-only reads through the existing unattended queue. Never changes YouTube. */
import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFileSync } from 'child_process';
import type { Snapshot } from '../src/lib/analytics/channel-tracker';

type ReadJob = { title:string; plain:string; body:string };
export function planReads(s:Snapshot, now:Date):ReadJob[] {
  const jobs:ReadJob[]=[];
  for(const v of s.videos.filter(v=>v.privacy==='public' && v.format==='long' && v.publishedAt)) {
    for(const [label,hours,days] of [['48h',48,2],['7d',168,7]] as const) {
      if(now.getTime()<Date.parse(v.publishedAt!)+hours*3600000)continue;
      const startDate=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(v.publishedAt!));
      const endDate=new Date(Date.parse(startDate)+86400000*(days-1)).toISOString().slice(0,10);
      jobs.push({title:`Field Order History analytics read ${v.id} ${label}`,
        plain:`Read how ${v.title} performed in its first ${days===2?'two':'seven'} days`,
        body:`J3006 automatic read-only learning loop. Channel ${s.channelId}; video ${v.id}; ${label} read due after ${hours} elapsed hours. This is the first daily dispatch after the deadline, not a claim of an exact live 48-hour capture.\nRead this channel's own channels/ww2/studio/RULES.md and 00_Brand/PLAYBOOK.md. Use the configured Studio browser and reuse_page; verify CHANNEL_ID before reading. No saves, account switching, publishing, title or thumbnail changes, spend or sign-in.\nCollect impressions, CTR percent, new and returning viewers and Test & Compare status/variant watch-time shares. Analytics period must be ${startDate} through ${endDate}, inclusive (Pacific dates matching the API); wait for reporting lag rather than substituting lifetime. Keep API views, hours, average seconds/percentage, subscribers, sources and retention/checkpoints.\nImport a strict dated read using 07_Content-Ops/scripts/field-order-studio-import.ts, merging with earlier windows. For suppressed or unavailable fields, use null and a missing reason, never zero. Record the video/window as attempted. Do not persist raw browser responses, credentials or account identity. Commit generated analytics from a clean worktree and report collection evidence. READS.md and board.json rebuild automatically. If there are triggers, recommend thumbnail first, then title, or tightening the next opening; never change packaging in this read job.\n`});
    }
  }
  // One channel read per reporting week, including the first week before any film is public.
  const monday=new Date(now);monday.setUTCHours(0,0,0,0);monday.setUTCDate(monday.getUTCDate()-(monday.getUTCDay()+6)%7);
  jobs.push({title:`Field Order History channel audience read ${monday.toISOString().slice(0,10)}`,
    plain:'Read Field Order History’s audience and progress towards monetisation',
    body:`J3006 automatic weekly read. Read-only, £0; channel ${s.channelId}. Reuse its configured Studio tab and verify channel identity. Never switch accounts, save settings or start a sign-in. Read qualified public watch hours (trailing 365 days) from Earn and when viewers are on YouTube from Audience (weekday, hour, relative activity and displayed timezone). Record Test & Compare results on public films if present. Never invent numbers if hidden or unavailable.\nUse the strict dated importer 07_Content-Ops/scripts/field-order-studio-import.ts; eligibleWatchHours is separate from the API estimate. whenViewers must carry its timezone. Use missing reasons for unavailable channel fields. Merge without replacing previous video windows, commit generated analytics in a clean worktree and report evidence. No public changes.\n`});
  return jobs;
}
export function dispatchReads(s:Snapshot, queueRepo:string, now=new Date(), run=(args:string[])=>execFileSync('python3',args,{cwd:queueRepo,stdio:'pipe',timeout:120000})) {
  if(!/^UC[\w-]{22}$/.test(s.channelId) || s.channel!=='ww2')throw Error('Invalid Field Order History snapshot');
  const queue=()=>JSON.parse(fs.readFileSync(path.join(queueRepo,'jobs/queue.json'),'utf8')).jobs as {title:string}[];
  const created:string[]=[];
  for(const job of planReads(s,now)) {
    // All statuses count: completed/suppressed reads must not regenerate every morning.
    if(queue().some(j=>j.title===job.title))continue;
    const dir=fs.mkdtempSync(path.join(os.tmpdir(),'field-order-read-'));
    try {
      const file=path.join(dir,'brief.md');fs.writeFileSync(file,job.body);
      run([path.join(queueRepo,'scripts/jobs.py'),'add','--needs','mini','--kind','studio','--repo','ww2','--title',job.title,'--plain',job.plain,'--action',job.plain,'--body-file',file,'--by','codex','--git']);
      created.push(job.title);
    } finally {fs.rmSync(dir,{recursive:true,force:true});}
  }
  return created;
}
if(require.main===module) {
  if(!process.env.YT_CHANNEL_ID_WW2 || !process.env.YT_ANALYTICS_REFRESH_TOKEN_WW2) {
    console.log('Field Order History Studio dispatch disabled until own read-only sign-in');
  } else {
    const dir=path.resolve(__dirname,'../../channels/ww2/05_Analytics/snapshots');
    const files=fs.readdirSync(dir).filter(f=>/^\d{4}-\d{2}-\d{2}\.json$/.test(f)).sort();
    const s=JSON.parse(fs.readFileSync(path.join(dir,files.at(-1)!), 'utf8')) as Snapshot;
    if(s.channelId!==process.env.YT_CHANNEL_ID_WW2 || Date.now()-Date.parse(s.takenAt)>86400000)throw Error('Missing fresh own-channel snapshot; no Studio jobs dispatched');
    const repo=process.env.FIELD_ORDER_QUEUE_REPO ?? path.resolve(__dirname,'../..');
    console.log(`Field Order History: ${dispatchReads(s,repo).length} Studio read jobs queued`);
  }
}
