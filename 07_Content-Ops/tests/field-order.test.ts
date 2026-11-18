import { describe,it,expect } from 'vitest';
import { buildFieldOrder, collectFieldOrder, triggers, projection, renderReads, type Detail } from '../src/lib/analytics/field-order';
import { authTarget } from '../scripts/youtube-auth';
const fixture=():Detail=>({channelId:'fixture',through:'2026-11-17',subscribers:100,failures:[],channel:{publicLongHoursEstimate:200,daily:Array.from({length:7},(_,i)=>({day:`2026-11-${11+i}`,estimatedMinutesWatched:600,subscribersGained:10,subscribersLost:0}))},videos:{one:{title:'A | film',seconds:600,retention:[{at:0,watching:1,relative:null},{at:1,watching:0,relative:null}],windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',metrics:{views:100,estimatedMinutesWatched:200,averageViewDuration:120,averageViewPercentage:20,subscribersGained:2}}}}}});
const studio=()=>({channelId:'fixture',readAt:'2026-11-18T00:00:00Z',videos:{one:{chapters:[180],windows:{'48h':{startDate:'2026-11-01',endDate:'2026-11-02',impressions:1001,ctr:2}}}}});
describe('Field Order History learning loop',()=>{
 it('matches Studio date ranges, flags thresholds and retains chapter checkpoints',()=>{
  const r=buildFieldOrder(fixture(),studio());
  expect(r.films[0].flags).toHaveLength(2);
  expect(r.films[0].checkpoints.map((x:any)=>x.seconds)).toEqual([30,60,120,180]);
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
  const d=fixture();d.videos.two={...d.videos.one,windows:{'7d':{metrics:{averageViewPercentage:80}}}};
  const r=buildFieldOrder(d,null);expect(r.films.map(f=>f.medianViewed)).toEqual([20,80]);
 });
 it('isolates failed optional reports and waits for complete API dates',async()=>{
  const calls:any[]=[];
  const snap:any={channelId:'fixture',totals:{subscribers:0},analytics:{through:'2026-11-02',retention:{}},videos:[{id:'one',privacy:'public',format:'long',publishedAt:'2026-11-01T18:00:00Z',seconds:600,title:'Film'}]};
  const d=await collectFieldOrder(snap,async p=>{calls.push(p);if(p.dimensions==='ageGroup')throw Error('unavailable');return {columnHeaders:[],rows:[]};});
  expect(d.failures).toContain('ageGroups');expect(d.videos.one.windows['48h']).toBeDefined();expect(d.videos.one.windows['7d']).toBeUndefined();
  expect(calls.every(p=>!p.endDate||p.endDate<='2026-11-02')).toBe(true);
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
 });
});
