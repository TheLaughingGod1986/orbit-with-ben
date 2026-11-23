import { describe,it,expect } from 'vitest';
import { buildFieldOrder, collectFieldOrder, triggers, projection, renderReads, type Detail } from '../src/lib/analytics/field-order';
import type { Snapshot } from '../src/lib/analytics/channel-tracker';
import { authTarget } from '../scripts/youtube-auth';
const snapFixture=():Snapshot=>({channel:'ww2',channelId:'fixture',date:'2026-11-17',takenAt:'2026-11-18T00:00:00Z',totals:{subscribers:0,views:0,videos:0},analytics:null,videos:[]});
const fixture=():Detail=>({channelId:'fixture',through:'2026-11-17',subscribers:100,failures:[],channel:{publicLongHoursEstimate:200,daily:Array.from({length:7},(_,i)=>({day:`2026-11-${11+i}`,estimatedMinutesWatched:600,subscribersGained:10,subscribersLost:0}))},videos:{one:{title:'A | film',seconds:600,retention:[{at:0,watching:1,relative:null},{at:1,watching:0,relative:null}],windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',metrics:{views:100,estimatedMinutesWatched:200,averageViewDuration:120,averageViewPercentage:20,subscribersGained:2}}}}}});
const studio=()=>({channelId:'fixture',readAt:'2026-11-18T00:00:00Z',videos:{one:{chapters:[180],windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',impressions:1001,ctr:2}}}}});
describe('Field Order History learning loop',()=>{
 it('matches Studio date ranges, flags thresholds and retains chapter checkpoints',()=>{
  const r=buildFieldOrder(fixture(),studio());
  expect(r.films[0].flags).toHaveLength(2);
  expect(r.films[0].checkpoints.map(x=>x.seconds)).toEqual([30,60,120,180]);
  expect(r.films[0].checkpoints[0].ratio).toBeCloseTo(.95);
  expect(r.films[0].medianCtr).toBe(2);
  expect(renderReads(r)).toContain('A   film');
 });
 it('does not invent reach, eligible hours or growth when unavailable',()=>{
  const d=fixture();d.channel.daily=[];
  const r=buildFieldOrder(d,null);
  expect(r.films[0].ctr).toBeNull();expect(r.eligibleWatchHours).toBeNull();
  expect(r.targets[0].eta).toBeNull();
 });
 it('rejects another channel or mismatched period without losing API metrics',()=>{
  const st=studio();st.channelId='other';expect(buildFieldOrder(fixture(),st).films[0].ctr).toBeNull();
  st.channelId='fixture';st.videos.one.windows['48h'].endDate='2026-11-03';
  expect(buildFieldOrder(fixture(),st).films[0].ctr).toBeNull();
 });
 it('uses strict triggers and seven complete days for forecasts',()=>{
  expect(triggers(1000,2,25)).toEqual([]);expect(triggers(1001,3,25)).toEqual([]);
  const r=buildFieldOrder(fixture(),studio());expect(r.targets[0].eta).toBe('2027-02-15');
  expect(projection('2026-11-17',100,1000,0)).toBeNull();
  expect(projection('2026-11-17',1000,1000,0)).toBe('2026-11-17');
 });
 it('does not compare 7-day reads with 48-hour medians',()=>{
  const d=fixture();d.videos.two={...d.videos.one,windows:{'7d':{startDate:'2026-11-01',endDate:'2026-11-07',metrics:{averageViewPercentage:80}}}};
  const r=buildFieldOrder(d,null);expect(r.films.map(f=>f.medianViewed)).toEqual([20,80]);
 });
 it('isolates failed optional reports and waits for complete API dates',async()=>{
  const calls:Record<string,string>[]=[];
  const snap:Snapshot={channel:'ww2',date:'2026-11-02',takenAt:'2026-11-03T00:00:00Z',channelId:'fixture',totals:{subscribers:0,views:0,videos:1},analytics:{through:'2026-11-02',retention:{},last7:{},last28:{},lifetime:{}},videos:[{id:'one',privacy:'public',format:'long',publishedAt:'2026-11-01T18:00:00Z',seconds:600,title:'Film',views:0,likes:0,comments:0}]};
  const d=await collectFieldOrder(snap,async p=>{calls.push(p);if(p.dimensions==='ageGroup')throw Error('unavailable');return {columnHeaders:[],rows:[]};});
  expect(d.failures).toContain('ageGroups');expect(d.videos.one.windows['48h']).toBeDefined();expect(d.videos.one.windows['7d']).toBeUndefined();
  expect(calls.every(p=>!p.endDate||p.endDate<='2026-11-02')).toBe(true);
 });
 it('prefers a newer dated Studio read of channel totals and says where each figure came from',()=>{
  const d=fixture();d.takenAt='2026-11-18T06:40:00Z';
  const st={...studio(),readAt:'2026-11-19T12:41:00Z',channelTotals:{subscribers:101,watchHours:250},channelTotalsReadAt:'2026-11-19T12:41:00Z'};
  const r=buildFieldOrder(d,st);
  expect(r.targets[0]).toMatchObject({current:101,source:'Studio',asOf:'2026-11-19T12:41:00Z'});
  expect(r.targets[1]).toMatchObject({current:250,source:'Studio, all watch time',asOf:'2026-11-19T12:41:00Z'});
  // Older than the snapshot and the API's last complete date: the API figures stand.
  const old={...st,channelTotalsReadAt:'2026-11-17T12:00:00Z'};
  const r2=buildFieldOrder(d,old);
  expect(r2.targets[0]).toMatchObject({current:100,source:'YouTube API',asOf:'2026-11-18T06:40:00Z'});
  expect(r2.targets[1]).toMatchObject({current:200,source:'API estimate',asOf:'data through 2026-11-17'});
  // A hidden Studio figure never replaces a real one, and another channel's read is ignored.
  expect(buildFieldOrder(d,{...st,channelTotals:{subscribers:null,watchHours:250}}).targets[0].current).toBe(100);
  expect(buildFieldOrder(d,{...st,channelId:'other'}).targets[0].current).toBe(100);
 });
 it('uses only read-only scopes for the third channel',()=>{
  expect(()=>authTarget(['--analytics','ww2'])).toThrow('Set YT_CHANNEL_ID_WW2');
 });
});

describe('Studio import contract',()=>{
 it('rejects credentials and malformed reach data',async()=>{
  const {studioSchema}=await import('../scripts/field-order-studio-import');
  const valid={channelId:'UC'+'a'.repeat(22),readAt:'2026-11-18T00:00:00Z',videos:{abcdefghijk:{windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',impressions:1001,ctr:2}}}}};
  expect(studioSchema.safeParse(valid).success).toBe(true);
  expect(studioSchema.safeParse({...valid,token:'never-store'}).success).toBe(false);
  expect(studioSchema.safeParse({...valid,videos:{abcdefghijk:{windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',impressions:1,ctr:101}}}}}).success).toBe(false);
  expect(studioSchema.safeParse({...valid,channelTotals:{subscribers:1,watchHours:1.36}}).success).toBe(true);
  expect(studioSchema.safeParse({...valid,channelTotals:{subscribers:-1,watchHours:1}}).success).toBe(false);
  expect(studioSchema.safeParse({...valid,channelTotals:{subscribers:1,watchHours:1,email:'x'}}).success).toBe(false);
 });
 it('stamps channel totals with their own read time and keeps them across later reads',async()=>{
  const {mergeStudio}=await import('../scripts/field-order-studio-import');
  const id='UC'+'a'.repeat(22);
  const first=mergeStudio(null,{channelId:id,readAt:'2026-11-23T12:41:00Z',videos:{},channelTotals:{subscribers:1,watchHours:1.36}});
  expect(first.channelTotalsReadAt).toBe('2026-11-23T12:41:00Z');
  const later=mergeStudio(first,{channelId:id,readAt:'2026-11-24T09:00:00Z',videos:{},eligibleWatchHours:2});
  expect(later.channelTotals).toEqual({subscribers:1,watchHours:1.36});expect(later.channelTotalsReadAt).toBe('2026-11-23T12:41:00Z');
 });
});

describe('Unattended Studio dispatch and merging',()=>{
 it('dispatches windows only once due, including Pacific date boundary cases',async()=>{
  const {planReads}=await import('../scripts/field-order-dispatch');
  const s:Snapshot={...snapFixture(),videos:[{id:'abcdefghijk',title:'A film',format:'long',privacy:'public',publishedAt:'2026-11-01T01:00:00Z',seconds:600,views:0,likes:0,comments:0}],channelId:'UC'+'a'.repeat(22)};
  // Each day with a public film also gets one channel totals read (weekly audience read + daily totals),
  // and every film read is followed by a rules review.
  expect(planReads(s,new Date('2026-11-03T00:59:59Z'))).toHaveLength(2);
  const jobs=planReads(s,new Date('2026-11-03T01:00:00Z'));
  expect(jobs).toHaveLength(4);expect(jobs[0].due).toBe('2026-11-03T01:00:00.000Z');expect(jobs[0].body).toContain('2026-10-31 through 2026-11-01');
  expect(jobs[1]).toMatchObject({title:'Field Order History rules review abcdefghijk 48h',kind:'review',needs:'any',due:'2026-11-03T13:00:00.000Z'});
  expect(jobs[1].body).toContain('LEARNINGS.md');expect(jobs[1].body).toContain('strangers only');
  expect(planReads(s,new Date('2026-11-08T01:00:00Z'))).toHaveLength(6);
  s.videos[0].privacy='private';expect(planReads(s,new Date('2026-12-01'))).toHaveLength(1);
 });
 it('queues one channel totals read per day once a film is public',async()=>{
  const {planReads}=await import('../scripts/field-order-dispatch');
  const s:Snapshot={...snapFixture(),videos:[{id:'abcdefghijk',title:'A film',format:'long',privacy:'public',publishedAt:'2026-11-22T17:00:31Z',seconds:600,views:0,likes:0,comments:0}],channelId:'UC'+'a'.repeat(22)};
  expect(planReads(s,new Date('2026-11-22T16:59:00Z')).map(j=>j.title)).toEqual(['Field Order History channel audience read 2026-11-16']);
  const titles=planReads(s,new Date('2026-11-23T06:40:00Z')).map(j=>j.title);
  expect(titles).toContain('Field Order History channel totals read 2026-11-23');
  expect(planReads(s,new Date('2026-11-24T06:40:00Z')).map(j=>j.title)).toContain('Field Order History channel totals read 2026-11-24');
 });
 it('preserves earlier films and windows on import',async()=>{
  const {mergeStudio}=await import('../scripts/field-order-studio-import');
  const after=mergeStudio(studio(),{channelId:'fixture',readAt:'2026-11-19T00:00:00Z',videos:{two:{windows:{'7d':{startDate:'2026-11-01',endDate:'2026-11-07',impressions:null,ctr:null,missing:{reach:'Insufficient audience'}}}}}});
  expect(after.videos.one.windows?.['48h']?.impressions).toBe(1001);
  expect(after.videos.two.windows?.['7d']?.missing?.reach).toBe('Insufficient audience');
 });
 it('requires a timezone with viewer activity',async()=>{
  const {studioSchema}=await import('../scripts/field-order-studio-import');
  const s={channelId:'UC'+'a'.repeat(22),readAt:'2026-11-18T00:00:00Z',videos:{},whenViewers:[]};
  expect(studioSchema.safeParse(s).success).toBe(false);
  expect(studioSchema.safeParse({...s,whenViewersTimezone:'UTC'}).success).toBe(true);
 });
});

describe('Queue and import integration with disk fixtures',()=>{
 it('is idempotent across completed and claimed reads',async()=>{
  const fs=await import('fs'),os=await import('os'),path=await import('path');
  const {dispatchReads}=await import('../scripts/field-order-dispatch');
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'ww2-dispatch-test-'));
  try {
   fs.mkdirSync(path.join(root,'jobs'));
   const file=path.join(root,'jobs/queue.json');fs.writeFileSync(file,JSON.stringify({jobs:[]}));
   const snapshot:Snapshot={...snapFixture(),channel:'ww2',channelId:'UC'+'a'.repeat(22),videos:[{id:'abcdefghijk',title:'Film',privacy:'public',format:'long',publishedAt:'2026-11-01T18:00:00Z',seconds:600,views:0,likes:0,comments:0}]};
   const calls:string[][]=[];
   const run=(args:string[])=>{calls.push(args);const queue=JSON.parse(fs.readFileSync(file,'utf8'));queue.jobs.push({title:args[args.indexOf('--title')+1],status:'done'});fs.writeFileSync(file,JSON.stringify(queue));return Buffer.from('');};
   expect(dispatchReads(snapshot,root,new Date('2026-11-09'),run)).toHaveLength(6);
   expect(dispatchReads(snapshot,root,new Date('2026-11-09'),run)).toEqual([]);
   expect(calls.every(a=>a.includes('--git')&&a.includes('ww2')&&!a.includes('--body'))).toBe(true);
   const review=calls.find(a=>a.includes('Field Order History rules review abcdefghijk 7d'))!;
   expect(review[review.indexOf('--kind')+1]).toBe('review');expect(review[review.indexOf('--needs')+1]).toBe('any');
   const read=calls.find(a=>a.includes('Field Order History analytics read abcdefghijk 7d'))!;
   expect(read[read.indexOf('--kind')+1]).toBe('studio');expect(read[read.indexOf('--needs')+1]).toBe('mini');
  } finally {fs.rmSync(root,{recursive:true,force:true});}
 });
 it('validates before writing and merges earlier reads on disk',async()=>{
  const fs=await import('fs'),os=await import('os'),path=await import('path');
  const {importStudio}=await import('../scripts/field-order-studio-import');
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'ww2-import-test-'));
  try {
   const d=fixture();d.channelId='UC'+'a'.repeat(22);d.videos.abcdefghijk=d.videos.one;delete d.videos.one;
   fs.writeFileSync(path.join(root,'detail.json'),JSON.stringify(d));
   const file=path.join(root,'incoming.json');
   const read={channelId:d.channelId,readAt:'2026-11-18T00:00:00Z',videos:{abcdefghijk:{windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',impressions:1001,ctr:2}}}}};
   fs.writeFileSync(file,JSON.stringify(read));importStudio(file,root);
   const before=fs.readFileSync(path.join(root,'board.json'),'utf8');
   read.videos.abcdefghijk.windows['48h'].endDate='2026-11-03';
   fs.writeFileSync(file,JSON.stringify(read));expect(()=>importStudio(file,root)).toThrow('does not match');
   expect(fs.readFileSync(path.join(root,'board.json'),'utf8')).toBe(before);
   fs.writeFileSync(file,JSON.stringify({channelId:d.channelId,readAt:'2026-11-18T01:00:00Z',videos:{},eligibleWatchHours:300}));importStudio(file,root);
   const board=JSON.parse(fs.readFileSync(path.join(root,'board.json'),'utf8'));
   expect(board.films[0].impressions).toBe(1001);expect(board.eligibleWatchHours).toBe(300);
  } finally {fs.rmSync(root,{recursive:true,force:true});}
 });
 it('does not forecast watch hours from private or unlisted channel watch time',()=>{
  const d=fixture();d.channel.publicLongDaily={'2026-11-17':60};
  const r=buildFieldOrder(d,null);
  expect(r.targets[1].eta).toBe(projection(d.through,200,4000,1/7));
 });
});
