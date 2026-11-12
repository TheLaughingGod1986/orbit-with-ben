/** J2711: offline preview from the saved live audit; does not publish. */
import fs from 'node:fs';
import path from 'node:path';
import {buildText, hashtags, HASHTAG_LIMIT} from '../../../07_Content-Ops/src/lib/publishing/buffer-mirror';
const root=path.resolve(__dirname,'../../..');
const dir=path.join(root,'jobs/reviews/J2711');
const audit=JSON.parse(fs.readFileSync(path.join(dir,'owb_tags_before.json'),'utf8'));
const registry=JSON.parse(fs.readFileSync(path.join(root,'00_Brand/Channel-Setup/social/UPLOADS.json'),'utf8')).videos;
const ledger=JSON.parse(fs.readFileSync(path.join(root,'00_Brand/Channel-Setup/social/BUFFER_POSTS.json'),'utf8')).videos;
const scheduled=JSON.parse(fs.readFileSync(path.join(dir,'owb_buffer_scheduled.json'),'utf8')).data.posts.edges;
const preview=[];
for(const {node:post} of scheduled){
 if(/#[\p{L}\p{N}]/u.test(post.text))continue;
 let match=Object.entries(ledger).find(([,e]:[string,any])=>Object.values(e.channels).some((p:any)=>p.postId===post.id));
 if(!match){
 const candidates=Object.entries(registry).filter(([,v]:[string,any])=>v.social?.hook && post.text.startsWith(v.social.hook) && !v.supersededBy);
 if(candidates.length!==1)throw new Error(`Ambiguous unregistered post ${post.id}`);
 const channel=({'6ab92127ea19ca0bde03aead':'threads','6ab92149ea19ca0bde03af77':'facebook','6ab920b2ea19ca0bde03abff':'instagram'} as Record<string,string>)[post.channelId];
 match=[candidates[0][0],{channels:{[channel]:{postId:post.id}}}];
 }
 const [id,entry]:[string,any]=match;
 const channel=Object.keys(entry.channels).find(c=>entry.channels[c].postId===post.id) as 'instagram'|'facebook'|'threads';
 const v=audit.videos.find((v:any)=>v.id===id);
 if(!v)throw new Error(`Unaudited video ${id}`);
 const video={id,title:v.title,description:v.snippet.description,tags:v.liveTags,durationSeconds:30,privacyStatus:v.status.privacyStatus,publishAt:v.status.publishAt,publishedAt:v.snippet.publishedAt,containsSyntheticMedia:true};
 const tags=hashtags(video.tags,HASHTAG_LIMIT[channel],[video.title,registry[id]?.social?.hook,video.description].join(' '));
 if(tags.length!==HASHTAG_LIMIT[channel])throw new Error(`Insufficient usable tags ${id} ${channel}`);
 const text=post.text.trimEnd()+'\n\n'+tags.join(' ');
 preview.push({id,postId:post.id,channel,before:post,text,hashtagCount:tags.length,nextBuild:buildText(video,channel,'short',{social:registry[id]?.social,filmUrl:'https://youtu.be/'+registry[id]?.long})});
}
fs.writeFileSync(path.join(dir,'scheduled_repairs_preview.json'),JSON.stringify(preview,null,2)+'\n');
console.log(preview.map(p=>({id:p.id,postId:p.postId,channel:p.channel,hashtagCount:p.hashtagCount,nextBuild:p.nextBuild})));
