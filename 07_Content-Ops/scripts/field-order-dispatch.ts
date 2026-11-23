#!/usr/bin/env tsx
/** Dispatch Studio-only reads through the existing unattended queue. Never changes YouTube. */
import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFileSync } from 'child_process';
import type { Snapshot } from '../src/lib/analytics/channel-tracker';
import { channelRoot, ENGINE_ROOT, assertAnalyticsEngine } from './analytics-paths';

type ReadJob = { title:string; plain:string; body:string; due:string };
export function planReads(s:Snapshot, now:Date):ReadJob[] {
  const jobs:ReadJob[]=[];
  for(const v of s.videos.filter(v=>v.privacy==='public' && v.format==='long' && v.publishedAt)) {
    for(const [label,hours,days] of [['48h',48,2],['7d',168,7]] as const) {
      if(now.getTime()<Date.parse(v.publishedAt!)+hours*3600000)continue;
      const startDate=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(v.publishedAt!));
      const endDate=new Date(Date.parse(startDate)+86400000*(days-1)).toISOString().slice(0,10);
      jobs.push({title:`Field Order History analytics read ${v.id} ${label}`,due:new Date(Date.parse(v.publishedAt!)+hours*3600000).toISOString(),
        plain:`Read how ${v.title} performed in its first ${days===2?'two':'seven'} days`,
        body:`J3006 automatic read-only learning loop. Channel ${s.channelId}; video ${v.id}; ${label} read due after ${hours} elapsed hours. This is the first daily dispatch after the deadline, not a claim of an exact live 48-hour capture.\nRead this channel's own channels/ww2/studio/RULES.md and 00_Brand/PLAYBOOK.md. Use the configured Studio browser and reuse_page; verify CHANNEL_ID before reading. No saves, account switching, publishing, title or thumbnail changes, spend or sign-in.\nCollect impressions, CTR percent, new and returning viewers and Test & Compare status/variant watch-time shares. Analytics period must be ${startDate} through ${endDate}, inclusive (Pacific dates matching the API); wait for reporting lag rather than substituting lifetime. Keep API views, hours, average seconds/percentage, subscribers, sources and retention/checkpoints.\nImport a strict dated read using 07_Content-Ops/scripts/field-order-studio-import.ts, merging with earlier windows. For suppressed or unavailable fields, use null and a missing reason, never zero. Record the video/window as attempted. Do not persist raw browser responses, credentials or account identity. Commit generated analytics from a clean worktree and report collection evidence. READS.md and board.json rebuild automatically. If there are triggers, recommend thumbnail first, then title, or tightening the next opening; never change packaging in this read job.\n`});
    }
  }
  // One channel read per reporting week, including the first week before any film is public.
  const monday=new Date(now);monday.setUTCHours(0,0,0,0);monday.setUTCDate(monday.getUTCDate()-(monday.getUTCDay()+6)%7);
  jobs.push({title:`Field Order History channel audience read ${monday.toISOString().slice(0,10)}`,due:now.toISOString(),
    plain:'Read Field Order History’s audience and progress towards monetisation',
    body:`J3006 automatic weekly read. Read-only, £0; channel ${s.channelId}. Reuse its configured Studio tab and verify channel identity. Never switch accounts, save settings or start a sign-in. Read qualified public watch hours (trailing 365 days) from Earn and when viewers are on YouTube from Audience (weekday, hour, relative activity and displayed timezone). Record Test & Compare results on public films if present. Never invent numbers if hidden or unavailable.\nUse the strict dated importer 07_Content-Ops/scripts/field-order-studio-import.ts; eligibleWatchHours is separate from the API estimate. whenViewers must carry its timezone. Use missing reasons for unavailable channel fields. Merge without replacing previous video windows, commit generated analytics in a clean worktree and report evidence. No public changes.\n`});
  // Daily totals keep the board's monetisation card current: the API's watch hours lag a day or two (Ben, 23 Nov 2026).
  if(s.videos.some(v=>v.privacy==='public' && v.publishedAt && Date.parse(v.publishedAt)<=now.getTime())) {
    const day=now.toISOString().slice(0,10);
    jobs.push({title:`Field Order History channel totals read ${day}`,due:now.toISOString(),
      plain:'Read Field Order History’s subscribers and watch hours so the board stays current',
      body:`J3006 automatic daily read, about five minutes. Read-only, £0; channel ${s.channelId}. Reuse its configured Studio tab and verify channel identity. Never switch accounts, save settings or start a sign-in. In Studio Analytics, Overview, period Lifetime, read the channel's total subscribers and total watch time in hours, exactly as Studio shows them. Never invent numbers; if one is hidden, use null and a missing reason.\nImport them with the strict dated importer 07_Content-Ops/scripts/field-order-studio-import.ts as channelTotals {subscribers, watchHours}, with readAt the time you read them and videos {}. Commit the generated analytics from a clean worktree and report the two numbers. No public changes.\n`});
  }
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
      run([path.join(queueRepo,'scripts/jobs.py'),'add','--needs','mini','--kind','studio','--repo','ww2','--title',job.title,'--plain',job.plain,'--action',job.plain,'--due',job.due,'--body-file',file,'--by','codex','--git']);
      created.push(job.title);
    } finally {fs.rmSync(dir,{recursive:true,force:true});}
  }
  return created;
}
/** The shared active engine owns queue writes; channel records never do. */
export function queueRoot(engine=ENGINE_ROOT, configured=process.env.FIELD_ORDER_QUEUE_REPO):string {
  const repo=configured ?? engine;
  if(!path.isAbsolute(repo))throw Error('Field Order queue checkout must be absolute');
  try {
    const identity=(root:string)=>JSON.parse(fs.readFileSync(path.join(root,'channels/channels.json'),'utf8')).studio.github;
    const expected=identity(engine);
    if(typeof expected!=='string' || !expected || identity(repo)!==expected ||
       !fs.statSync(path.join(repo,'scripts/jobs.py')).isFile() ||
       !Array.isArray(JSON.parse(fs.readFileSync(path.join(repo,'jobs/queue.json'),'utf8')).jobs)) {
      throw Error('wrong queue');
    }
  } catch {
    throw Error('Field Order queue checkout is missing or belongs to a different engine');
  }
  return path.resolve(repo);
}

export function latestSnapshot(dir=path.join(channelRoot('ww2'),'snapshots')):Snapshot {
  const files=fs.readdirSync(dir).filter(f=>/^\d{4}-\d{2}-\d{2}\.json$/.test(f)).sort();
  if(!files.length)throw Error('No Field Order History snapshot; no Studio jobs dispatched');
  return JSON.parse(fs.readFileSync(path.join(dir,files.at(-1)!), 'utf8')) as Snapshot;
}

if(require.main===module) {
  assertAnalyticsEngine();
  if(!process.env.YT_CHANNEL_ID_WW2 || !process.env.YT_ANALYTICS_REFRESH_TOKEN_WW2) {
    console.log('Field Order History Studio dispatch disabled until own read-only sign-in');
  } else {
    const s=latestSnapshot();
    if(s.channelId!==process.env.YT_CHANNEL_ID_WW2 || Date.now()-Date.parse(s.takenAt)>86400000)throw Error('Missing fresh own-channel snapshot; no Studio jobs dispatched');
    const repo=queueRoot();
    console.log(`Field Order History: ${dispatchReads(s,repo).length} Studio read jobs queued`);
  }
}
