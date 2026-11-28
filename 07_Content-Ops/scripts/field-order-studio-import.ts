#!/usr/bin/env tsx
/** Accept a dated, read-only Studio collection. Never reads OAuth tokens or changes YouTube. */
import fs from 'fs';
import path from 'path';
import { z } from 'zod';
import { buildFieldOrder, renderReads, type Detail, type StudioRead } from '../src/lib/analytics/field-order';
const count=z.number().finite().nonnegative();
const date=z.iso.date();
const missing=z.record(z.string().max(60),z.string().min(1).max(240));
export const studioSchema=z.object({
  channelId:z.string().regex(/^UC[\w-]{22}$/),readAt:z.iso.datetime(),eligibleWatchHours:count.optional(),eligibleWatchHoursReadAt:z.iso.datetime().optional(),missing:missing.optional(),whenViewersTimezone:z.string().min(1).max(80).optional(),
  channelTotals:z.object({subscribers:count.nullable(),watchHours:count.nullable()}).strict().optional(),channelTotalsReadAt:z.iso.datetime().optional(),
  whenViewers:z.array(z.object({day:z.number().int().min(0).max(6),hour:z.number().int().min(0).max(23),viewers:count}).strict()).optional(),
  videos:z.record(z.string().regex(/^[\w-]{11}$/),z.object({
    chapters:z.array(count).optional(),
    windows:z.partialRecord(z.enum(['48h','7d']),z.object({startDate:date,endDate:date,impressions:count.nullable(),ctr:count.max(100).nullable(),newViewers:count.nullable().optional(),returningViewers:count.nullable().optional(),missing:missing.optional(),
      testCompare:z.object({status:z.enum(['running','complete','unavailable']),variants:z.array(z.object({label:z.string().max(30),watchTimeShare:count.max(100)}).strict())}).strict().optional()
    }).strict()).optional()
  }).strict())
}).strict().refine(v=>!v.whenViewers || !!v.whenViewersTimezone, 'Viewer activity needs its displayed timezone');
export function mergeStudio(old:StudioRead|null, fresh:StudioRead):StudioRead {
  if(fresh.eligibleWatchHours!==undefined)fresh={...fresh,eligibleWatchHoursReadAt:fresh.readAt};
  if(fresh.channelTotals!==undefined)fresh={...fresh,channelTotalsReadAt:fresh.readAt};
  if(!old || old.channelId!==fresh.channelId)return fresh;
  const merged={...old,...fresh,videos:{...old.videos},missing:{...old.missing,...fresh.missing}};
  for(const [id,v] of Object.entries(fresh.videos))merged.videos[id]={...old.videos[id],...v,windows:{...old.videos[id]?.windows,...v.windows}};
  return merged;
}
export function importStudio(file:string,dir:string) {
  const fresh=studioSchema.parse(JSON.parse(fs.readFileSync(file,'utf8')));
  let old:StudioRead|null=null;
  if(fs.existsSync(path.join(dir,'studio_read.json')))old=studioSchema.parse(JSON.parse(fs.readFileSync(path.join(dir,'studio_read.json'),'utf8')));
  if(old && Date.parse(fresh.readAt)<Date.parse(old.readAt))throw Error('Stale Studio read; nothing written');
  const studio=mergeStudio(old,fresh);
  const detail=JSON.parse(fs.readFileSync(path.join(dir,'detail.json'),'utf8')) as Detail;
  if(studio.channelId!==detail.channelId)throw Error('Studio read belongs to another channel; nothing written');
  if(Date.parse(studio.readAt)>Date.now()+300000)throw Error('Studio read is in the future; nothing written');
  for(const [id,v] of Object.entries(fresh.videos))for(const [label,w] of Object.entries(v.windows??{})) {
    const expected=detail.videos[id]?.windows?.[label];
    if(!expected || expected.startDate!==w.startDate || expected.endDate!==w.endDate)throw Error('Studio reporting period does not match API detail; nothing written');
    if(w.endDate<w.startDate || w.endDate>studio.readAt.slice(0,10))throw Error('Invalid Studio reporting period; nothing written');
  }
  const report=buildFieldOrder(detail,studio);
  fs.writeFileSync(path.join(dir,'studio_read.json'),JSON.stringify(studio,null,2)+'\n');
  fs.writeFileSync(path.join(dir,'board.json'),JSON.stringify(report,null,2)+'\n');
  fs.writeFileSync(path.join(dir,'READS.md'),renderReads(report));
}
if(require.main===module) {
  const file=process.argv[2];
  if(!file)throw Error('Usage: field-order-studio-import.ts <dated-read.json>');
  importStudio(file,path.resolve(__dirname,'../../channels/ww2/05_Analytics'));
  console.log('Field Order History: dated Studio read imported; reports rebuilt');
}
