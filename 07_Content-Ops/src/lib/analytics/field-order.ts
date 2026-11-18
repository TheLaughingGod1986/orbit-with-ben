/** Field Order History's read-only learning loop. No publishing or account mutation. */
import fs from 'fs';
import path from 'path';
import { addDays, curveAt, type RetentionPoint, type Snapshot } from './channel-tracker';
type Table = { columnHeaders?: { name: string }[]; rows?: unknown[][] };
type Query = (params: Record<string,string>) => Promise<Table>;
export const rows = (t: Table) => (t.rows ?? []).map(row => Object.fromEntries((t.columnHeaders ?? []).map((h,i)=>[h.name,row[i]])));
const n = (v: unknown): number | null => typeof v === 'number' && Number.isFinite(v) ? v : null;
export type StudioRead = {
  readAt: string; channelId: string;
  videos: Record<string, { chapters?: number[]; windows?: Record<string, { startDate: string; endDate: string; impressions: number|null; ctr: number|null; newViewers?: number|null; returningViewers?: number|null; missing?: Record<string,string>; testCompare?: unknown }> }>;
  eligibleWatchHours?: number; eligibleWatchHoursReadAt?:string; whenViewers?: unknown; whenViewersTimezone?:string; missing?:Record<string,string>;
};
type Metrics = Record<string, number>;
type WindowRead = { startDate: string; endDate: string; metrics: Metrics | null; sources?: Record<string, unknown>[] | null };
type VideoDetail = { title: string; publishedAt?: string | null; seconds: number; chapters?: number[]; windows: Record<string, WindowRead>; suggested?: Record<string, unknown>[] | null; retention: RetentionPoint[] };
type FilmRead = { id: string; title: string; window: string; startDate: string; endDate: string; metrics: Metrics | null; impressions: number | null; ctr: number | null; viewed: number | null; watchHours: number | null; sources: WindowRead['sources']; suggested: VideoDetail['suggested']; retention: RetentionPoint[]; checkpoints: { seconds: number; ratio: number | null }[]; newViewers: number | null; returningViewers: number | null; studioMissing: Record<string, string>; testCompare: unknown; flags: string[]; medianAvgSeconds?: number | null; avgSecondsVsMedian?: number | null; medianCtr?: number | null; medianViewed?: number | null; ctrVsMedian?: number | null; viewedVsMedian?: number | null };
export type Detail = { through: string; channelId: string; subscribers: number | null; channel: Record<string,unknown>; videos: Record<string, VideoDetail>; failures: string[] };
export async function collectFieldOrder(s: Snapshot, q: Query): Promise<Detail> {
  const through = s.analytics!.through;
  const d: Detail = { through, channelId:s.channelId, subscribers:s.totals.subscribers, channel:{}, videos:{}, failures:[] };
  const safe = async (name:string, p:Record<string,string>) => {
    try { return rows(await q(p)); } catch { d.failures.push(name); return null; }
  };
  const start = addDays(through,-364);
  d.channel.countries = await safe('countries',{startDate:start,dimensions:'country',metrics:'views,estimatedMinutesWatched',sort:'-views',maxResults:'25'});
  d.channel.ageGroups = await safe('ageGroups',{startDate:start,dimensions:'ageGroup',metrics:'viewerPercentage'});
  const daily = await safe('daily',{startDate:start,dimensions:'day',metrics:'estimatedMinutesWatched,subscribersGained,subscribersLost',sort:'day'});
  d.channel.daily = daily;
  // Estimated public long-form hours; the Earn page alone supplies qualified YPP hours.
  let minutes = 0, complete = true;
  const longDaily:Record<string,number>={};
  const publicLongs = s.videos.filter(v=>v.privacy==='public' && v.format==='long' && v.publishedAt);
  for (const v of publicLongs) {
    const published = new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(v.publishedAt!));
    if (published > through) continue;
    const filters = `video==${v.id}`;
    const year = await safe(`${v.id}:year`,{startDate:published>start?published:start,filters,metrics:'estimatedMinutesWatched'});
    const pace=await safe(`${v.id}:daily`,{startDate:addDays(through,-6),filters,dimensions:'day',metrics:'estimatedMinutesWatched'});
    if(!pace)complete=false;
    for(const row of pace ?? [])longDaily[String(row.day)]=(longDaily[String(row.day)]??0)+Number(row.estimatedMinutesWatched);
    if (year) minutes += Number(year[0]?.estimatedMinutesWatched ?? 0); else complete=false;
    const suggested = await safe(`${v.id}:suggested`,{startDate:published,filters:`${filters};insightTrafficSourceType==RELATED_VIDEO`,dimensions:'insightTrafficSourceDetail',metrics:'views',sort:'-views',maxResults:'25'});
    const windows: Record<string,WindowRead> = {};
    for (const [label,days] of [['48h',2],['7d',7]] as const) {
      const endDate = addDays(published,days-1);
      if (endDate>through) continue;
      const metrics = await safe(`${v.id}:${label}`,{startDate:published,endDate,filters,metrics:'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained'});
      const sources = await safe(`${v.id}:${label}:sources`,{startDate:published,endDate,filters,dimensions:'insightTrafficSourceType',metrics:'views'});
      windows[label] = {startDate:published,endDate,metrics:metrics?.[0] as Metrics ?? null,sources};
    }
    d.videos[v.id] = { title:v.title, publishedAt:v.publishedAt, seconds:v.seconds, chapters:v.chapters ?? [], windows, suggested, retention:s.analytics?.retention?.[v.id] ?? [] };
  }
  d.channel.publicLongDaily = complete ? longDaily : null;
  d.channel.publicLongHoursEstimate = complete ? minutes/60 : null;
  return d;
}
export function median(values: (number|null)[]) {
  const a=values.filter((x):x is number=>x!=null).sort((a,b)=>a-b), m=Math.floor(a.length/2);
  return a.length ? a.length%2?a[m]:(a[m-1]+a[m])/2 : null;
}
export function triggers(impressions:number|null,ctr:number|null,viewed:number|null) {
  return [...(impressions!=null && impressions>1000 && ctr!=null && ctr<3 ? ['Change thumbnail first, then title; Chief reviews before any change.'] : []),...(viewed!=null && viewed<25 ? ["Tighten the next script's first two minutes."] : [])];
}
export function projection(date:string, current:number|null, target:number, perDay:number|null) {
  if(current==null) return null;
  if(current>=target) return date;
  return perDay!=null && perDay>0 ? addDays(date,Math.ceil((target-current)/perDay)) : null;
}
export function buildFieldOrder(d:Detail, studio:StudioRead|null) {
  const own=studio?.channelId===d.channelId ? studio : null;
  const films:FilmRead[]=[];
  for(const [id,v] of Object.entries(d.videos)) {
    for(const [window,w] of Object.entries(v.windows)) {
      const st=own?.videos[id]?.windows?.[window];
      const matched=!!st && !!own && st.startDate===w.startDate && st?.endDate===w.endDate && own!.readAt.slice(0,10)>=w.endDate;
      const impressions=matched?n(st!.impressions):null, ctr=matched?n(st!.ctr):null;
      const viewed=n(w.metrics?.averageViewPercentage);
      const marks=[30,60,120,...(v.chapters ?? []),...(own?.videos[id]?.chapters ?? [])].filter((x,i,a)=>x<=v.seconds && a.indexOf(x)===i);
      films.push({id,title:v.title,window,startDate:w.startDate,endDate:w.endDate,metrics:w.metrics,impressions,ctr,viewed,
        watchHours:n(w.metrics?.estimatedMinutesWatched)==null?null:w.metrics!.estimatedMinutesWatched/60,
        sources:w.sources,suggested:v.suggested,retention:v.retention,
        checkpoints:marks.map(seconds=>({seconds,ratio:curveAt(v.retention,seconds/v.seconds)})),
        newViewers:matched?n(st!.newViewers):null,returningViewers:matched?n(st!.returningViewers):null,
        studioMissing:matched?st!.missing??{}:{reach:"No matching dated Studio read"},testCompare:matched?st!.testCompare??null:null,flags:triggers(impressions,ctr,viewed)});
    }
  }
  // Compare like windows only, never a 48-hour result against a 7-day one.
  for(const window of ['48h','7d']) {
    const peers=films.filter(f=>f.window===window), ctr=median(peers.map(f=>f.ctr)), viewed=median(peers.map(f=>f.viewed));
    const seconds=median(peers.map(f=>n(f.metrics?.averageViewDuration)));
    for(const f of peers) {f.medianAvgSeconds=seconds;f.avgSecondsVsMedian=n(f.metrics?.averageViewDuration)==null||seconds==null?null:f.metrics!.averageViewDuration-seconds;f.medianCtr=ctr;f.medianViewed=viewed;f.ctrVsMedian=f.ctr==null||ctr==null?null:f.ctr-ctr;f.viewedVsMedian=f.viewed==null||viewed==null?null:f.viewed-viewed;}
  }
  const daily=(d.channel.daily as {day:string; subscribersGained:number; subscribersLost:number}[]|null) ?? [], week=daily.filter(r=>r.day>=addDays(d.through,-6) && r.day<=d.through);
  const complete=week.length===7 && new Set(week.map(r=>r.day)).size===7;
  const subPace=complete?week.reduce((a,r)=>a+Number(r.subscribersGained)-Number(r.subscribersLost),0)/7:null;
  // Channel hours pace is an estimate, not qualified Earn progress.
  const longDaily=d.channel.publicLongDaily as Record<string,number>|null;
  const hourPace=complete && longDaily ? Object.entries(longDaily).filter(([day])=>day>=addDays(d.through,-6)&&day<=d.through).reduce((a,[,minutes])=>a+minutes,0)/60/7:null;
  const hours=own?n(own.eligibleWatchHours):null, estimate=n(d.channel.publicLongHoursEstimate);
  const targets=[{name:'Subscribers',current:d.subscribers,target:1000,eta:projection(d.through,d.subscribers,1000,subPace)},
    ...[4000,8000].map(target=>({name:'Public watch hours (estimate)',current:estimate,target,eta:projection(d.through,estimate,target,hourPace)}))];
  return {name:'Field Order History',through:d.through,deadline:'2027-02-01',targets,eligibleWatchHours:hours,studioReadAt:own?.eligibleWatchHoursReadAt??own?.readAt??null,estimatedPublicLongHours:estimate,
    note:'Watch-hour forecasts are estimates, not YPP eligibility. Rolling 365-day hours can expire. February 1 is the studio planning line; confirm current policy before applying.',
    films,countries:d.channel.countries,ageGroups:d.channel.ageGroups,whenViewers:own?.whenViewers??null,whenViewersTimezone:own?.whenViewersTimezone??null,studioMissing:own?.missing??{},failures:d.failures};
}
export function renderReads(report:ReturnType<typeof buildFieldOrder>) {
  const fmt=(v:unknown)=>v==null?'pending':String(v);
  const lines=['# Field Order History: film reads','',`Analytics through ${report.through}. Generated automatically; do not edit.`,
    '', '48h uses the first two Pacific calendar dates; 7d uses the first seven. The API has daily granularity and a reporting lag, so these are not exact elapsed-hour windows. Studio reach reads must match these date ranges.', '',
    '| Film | Read | Impressions | CTR % | Views | Watch hours | Avg seconds | Avg viewed % | Subscribers gained | Action |',
    '|---|---|---:|---:|---:|---:|---:|---:|---:|---|'];
  for(const f of report.films) lines.push(`| ${f.title.replace(/[|\n]/g,' ')} | ${f.window} | ${fmt(f.impressions)} | ${fmt(f.ctr)} | ${fmt(f.metrics?.views)} | ${fmt(f.watchHours)} | ${fmt(f.metrics?.averageViewDuration)} | ${fmt(f.viewed)} | ${fmt(f.metrics?.subscribersGained)} | ${[...f.flags,...Object.values(f.studioMissing)].join(' ')||'No trigger from available data'} |`);
  lines.push('',report.note,'','Full retention curves, chapter checkpoints, traffic sources, suggested-from videos, demographics, medians and missing-field status are in board.json and detail.json. Studio-only fields remain pending until a dated read exists.');
  return lines.join('\n')+'\n';
}
export function writeFieldOrder(dir:string,_s:Snapshot,d:Detail) {
  fs.mkdirSync(dir,{recursive:true});
  let studio:StudioRead|null=null;
  try {studio=JSON.parse(fs.readFileSync(path.join(dir,'studio_read.json'),'utf8'));} catch { /* unavailable */ }
  const report=buildFieldOrder(d,studio);
  fs.writeFileSync(path.join(dir,'detail.json'),JSON.stringify(d,null,2)+'\n');
  fs.writeFileSync(path.join(dir,'board.json'),JSON.stringify(report,null,2)+'\n');
  fs.writeFileSync(path.join(dir,'READS.md'),renderReads(report));
}
