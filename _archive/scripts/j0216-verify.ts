import fs from 'node:fs';
import path from 'node:path';
import {getYouTubeAccessToken} from '../07_Content-Ops/src/lib/youtube/data-api';
async function main(){
 const base=path.resolve('00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10');
 const m=JSON.parse(fs.readFileSync(path.join(base,'08_Covers/MANIFEST.json'),'utf8'));
 const rows=m.shorts.map((s:any)=>{const p=path.join(base,'11_Upload-Package',s.id);const r=fs.readdirSync(p).filter(f=>f.startsWith('PACKAGE_UPLOAD_RESULT_')).map(f=>JSON.parse(fs.readFileSync(path.join(p,f),'utf8'))).find(r=>!r.dryRun&&r.ok);return {slug:s.id,title:s.title,expected:s.uk,id:r?.upload.platformPostId};});
 if(rows.some((r:any)=>!r.id))throw Error('Missing upload');
 const token=await getYouTubeAccessToken();
 const res=await fetch('https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id='+rows.map((r:any)=>r.id).join(','),{headers:{Authorization:'Bearer '+token}});
 if(!res.ok)throw Error('Readback HTTP '+res.status);
 const data:any=await res.json();
 const result=rows.map((r:any)=>{const v=data.items.find((v:any)=>v.id===r.id);return {...r,status:v?.status,title:v?.snippet.title,verified:!!v&&v.status.privacyStatus==='private'&&Date.parse(v.status.publishAt)===Date.parse(r.expected)&&v.status.selfDeclaredMadeForKids===false&&v.status.containsSyntheticMedia===true&&v.snippet.title===r.title};});
 fs.writeFileSync(path.join(base,'J0216_YOUTUBE_READBACK.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result,null,2));
 if(result.some((r:any)=>!r.verified))process.exitCode=1;
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
