import {afterEach,describe,expect,it,vi} from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {scheduledWithRegistry} from '../src/lib/publishing/buffer-deps';
import {listScheduledUploads} from '../src/lib/youtube/data-api';
import {findMedia,validateShortSource} from '../src/lib/publishing/media-finder';
import {mirrorVideo,runBufferCheck,type MirrorDeps} from '../src/lib/publishing/buffer-runner';
import type {YouTubeVideo} from '../src/lib/publishing/buffer-mirror';
const now=new Date('2026-11-03T07:05:00Z');
const video=(id:string):YouTubeVideo=>({id,title:id,description:'',tags:[],durationSeconds:25,privacyStatus:'private',publishAt:'2026-11-08T11:30:00Z',publishedAt:null,containsSyntheticMedia:false});
const dirs:string[]=[];
afterEach(()=>{vi.unstubAllGlobals();for(const d of dirs.splice(0))fs.rmSync(d,{recursive:true,force:true});});
function source(){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'buffer-source-'));dirs.push(dir);const file=path.join(dir,'approved.mp4');fs.writeFileSync(file,'approved social source');return {dir,file,sha256:createHash('sha256').update('approved social source').digest('hex')};}
describe('Buffer recovery regressions',()=>{
 it('finds registered schedules absent from the entire playlist and deduplicates',async()=>{
  const a=video('marslong001'),b=video('marsnight01');
  const byId=vi.fn(async()=>new Map([[a.id,a],[b.id,b]]));
  const out=await scheduledWithRegistry('test',now,[a.id,b.id],async()=>[a],byId);
  expect(out.map(v=>v.id)).toEqual([a.id,b.id]);expect(byId).toHaveBeenCalledWith('test',[a.id,b.id]);
 });
 it('uses direct-id state to remove an obsolete playlist schedule',async()=>{
  const a=video('marslong001');
  const out=await scheduledWithRegistry('test',now,[a.id],async()=>[a],async()=>new Map([[a.id,{...a,privacyStatus:'public',publishAt:null}]]));
  expect(out).toEqual([]);
 });
 it('reads page two rather than losing an older scheduled upload',async()=>{
  const requests:string[]=[];
  vi.stubGlobal('fetch',vi.fn(async(url:string)=>{requests.push(url);const u=new URL(url);let body;
   if(u.pathname.endsWith('/channels'))body={items:[{contentDetails:{relatedPlaylists:{uploads:'ours'}}}]};
   else if(u.pathname.endsWith('/playlistItems'))body=u.searchParams.has('pageToken')?{items:[{contentDetails:{videoId:'olderMars01'}}]}:{items:[{contentDetails:{videoId:'first000001'}}],nextPageToken:'second'};
   else body={items:(u.searchParams.get('id')||'').split(',').map(id=>({id,status:{privacyStatus:'private',publishAt:'2026-11-08T11:30Z'},snippet:{title:id},contentDetails:{duration:'PT25S'}}))};
   return new Response(JSON.stringify(body),{status:200});
  }));
  expect((await listScheduledUploads('test',now)).map(v=>v.id)).toContain('olderMars01');
  expect(requests.filter(s=>s.includes('/playlistItems'))).toHaveLength(2);
 });
 it('holds mismatched Titan bytes, unavailable originals, and unreadable sources',()=>{
  const {dir,file,sha256}=source();
  expect(validateShortSource({sha256},file)).toBeNull();
  fs.writeFileSync(file,'a newer unapproved render');
  expect(validateShortSource({sha256},file)).toMatch(/mismatch/i);
  expect(validateShortSource({sha256},null)).toMatch(/unavailable/i);
  expect(validateShortSource({sha256},path.join(dir,'missing.mp4'))).toMatch(/cannot be read/i);
  expect(validateShortSource({sha256,knownNoFile:'overwritten original'},file)).toMatch(/original unavailable/i);
 });
 it('validates the approved HOS social source instead of its different YouTube copy',()=>{
  const {file,sha256}=source();
  expect(validateShortSource({sha256,youtubeUploadSha256:'a'.repeat(64),sourceNote:'Approved different social source'},file)).toBeNull();
 });
 it('surfaces the source hold through the automatic finder',()=>{
  const {dir,file}=source();
  const hint=findMedia('titan000001',{repoRoot:dir,registryFile:path.join(dir,'UPLOADS.json'),scanned:new Map(),registry:{version:1,videos:{titan000001:{kind:'short',file,sha256:'a'.repeat(64)}}}});
  expect(hint?.sourceError).toMatch(/mismatch/i);
 });
 it.each([true,false])('rejects a source before any hosting or create (dryRun=%s)',async(dryRun)=>{
  const {file}=source(),v=video('titan000001');
  const host=vi.fn(),create=vi.fn();
  const deps:MirrorDeps={youtubeToken:async()=> 'test',fetchVideos:async()=>new Map([[v.id,v]]),listScheduled:async()=>[],now:()=>now,
   store:{load:async()=>({version:1,videos:{}}),record:vi.fn(),setMedia:vi.fn()},host,checkUrl:async()=>null,
   client:{createPost:create,editPost:vi.fn(),deletePost:vi.fn(),getPostStatus:vi.fn()},channelIds:{instagram:'ig',facebook:'fb',threads:'th'},
   validateSource:(_id,p)=>validateShortSource({sha256:'a'.repeat(64)},p)};
  const out=await mirrorVideo({videoId:v.id,mediaPath:file,standalone:true,dryRun},deps);
  expect(out.plan.errors.join(' ')).toMatch(/mismatch/i);expect(out.plan.actions).toEqual([]);expect(host).not.toHaveBeenCalled();expect(create).not.toHaveBeenCalled();
 });
});

it('does not take down an existing queued post when the replacement source is unverified',async()=>{
 const v=video('titan000001'),remove=vi.fn();
 const ledger={version:1 as const,videos:{[v.id]:{kind:'short' as const,title:v.title,dueAt:v.publishAt,mode:'customScheduled' as const,channels:{instagram:{postId:'existing',recordedAt:now.toISOString()}},media:'https://external.invalid/short.mp4'}}};
 const deps:MirrorDeps={youtubeToken:async()=> 'test',fetchVideos:async()=>new Map([[v.id,v]]),listScheduled:async()=>[v],now:()=>now,
  store:{load:async()=>ledger,record:vi.fn(),setMedia:vi.fn()},host:vi.fn(),checkUrl:async()=> 'expired asset',
  client:{createPost:vi.fn(),editPost:vi.fn(),deletePost:remove,getPostStatus:async()=> 'scheduled'},channelIds:{instagram:'ig'},
  findMedia:()=>({videoId:v.id,mediaPath:'/unapproved.mp4',thumbPath:null,longId:null,standalone:true,source:'registry',registered:true,sourceError:'Social source SHA256 mismatch'})};
 const out=await runBufferCheck(deps);
 expect(out.rehosted[0]).toMatchObject({removed:false,error:'Social source SHA256 mismatch'});expect(remove).not.toHaveBeenCalled();
});

it('defers beyond-window registrations without reading unavailable source files',async()=>{
 const v={...video('later000001'),publishAt:'2026-12-08T11:30Z'},find=vi.fn();
 const deps:MirrorDeps={youtubeToken:async()=> 'test',fetchVideos:async()=>new Map(),listScheduled:async()=>[v],now:()=>now,
  store:{load:async()=>({version:1,videos:{}}),record:vi.fn(),setMedia:vi.fn()},host:null,checkUrl:async()=>null,client:null,channelIds:{},findMedia:find};
 const out=await runBufferCheck(deps,{dryRun:true});expect(out.deferred).toHaveLength(1);expect(out.unmirrored).toEqual([]);expect(find).not.toHaveBeenCalled();
});
