#!/usr/bin/env tsx
/** Accept a dated, read-only Studio collection. Never reads OAuth tokens or changes YouTube. */
import fs from 'fs';
import path from 'path';
import { z } from 'zod';
import { buildFieldOrder, renderReads, type Detail } from '../src/lib/analytics/field-order';
const count=z.number().finite().nonnegative();
const date=z.iso.date();
export const studioSchema=z.object({
  channelId:z.string().regex(/^UC[\w-]{22}$/),readAt:z.iso.datetime(),eligibleWatchHours:count.optional(),
  whenViewers:z.array(z.object({day:z.number().int().min(0).max(6),hour:z.number().int().min(0).max(23),viewers:count}).strict()).optional(),
  videos:z.record(z.string().regex(/^[\w-]{11}$/),z.object({
    chapters:z.array(count).optional(),
    windows:z.partialRecord(z.enum(['48h','7d']),z.object({startDate:date,endDate:date,impressions:count,ctr:count.max(100),newViewers:count.optional(),returningViewers:count.optional(),
      testCompare:z.object({status:z.enum(['running','complete','unavailable']),variants:z.array(z.object({label:z.string().max(30),watchTimeShare:count.max(100)}).strict())}).strict().optional()
    }).strict()).optional()
  }).strict())
}).strict();
export function importStudio(file:string,dir:string) {
  const studio=studioSchema.parse(JSON.parse(fs.readFileSync(file,'utf8')));
  const detail=JSON.parse(fs.readFileSync(path.join(dir,'detail.json'),'utf8')) as Detail;
  if(studio.channelId!==detail.channelId)throw Error('Studio read belongs to another channel; nothing written');
  if(Date.parse(studio.readAt)>Date.now()+300000)throw Error('Studio read is in the future; nothing written');
  for(const v of Object.values(studio.videos))for(const w of Object.values(v.windows??{})) {
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
