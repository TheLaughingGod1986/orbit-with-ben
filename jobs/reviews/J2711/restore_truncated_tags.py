"""Restore only a confirmed first-15 truncation; preserve live snippet and status."""
import json,urllib.request,time,pathlib
from audit_tags import token,req
HERE=pathlib.Path(__file__).parent
ID='c5AdqQsnnys'
KEYS=['title','description','categoryId','defaultLanguage','defaultAudioLanguage','tags']
def payload_for(live,tags):
 assert len(tags)>15 and set(live['tags'])==set(tags[:15]), 'Not a proven first-15 truncation'
 return {**{k:live[k] for k in KEYS if k in live},'tags':tags}
def main():
 audit=json.loads((HERE/'owb_tags_before.json').read_text());row=next(v for v in audit['videos'] if v['id']==ID)
 t=token('owb');url='https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id='+ID
 before=req(url,t)['items'][0];snippet=payload_for(before['snippet'],row['packageTags'])
 result=dict(id=ID,source=row['package'],before=before,payload=dict(id=ID,snippet=snippet))
 (HERE/'nearest_star_repair.json').write_text(json.dumps(result,indent=2)+'\n')
 r=urllib.request.Request('https://www.googleapis.com/youtube/v3/videos?part=snippet',data=json.dumps(result['payload']).encode(),method='PUT',headers={'Authorization':'Bearer '+t,'Content-Type':'application/json','If-Match':before['etag']})
 result['update']=json.load(urllib.request.urlopen(r,timeout=35))
 for i in range(8):
  after=next(v for v in req(url+',uhZSRcvngvE',t)['items'] if v['id']==ID)
  if set(after['snippet'].get('tags',[]))==set(row['packageTags']):break
  time.sleep(1)
 result['after']=after
 (HERE/'nearest_star_repair.json').write_text(json.dumps(result,indent=2)+'\n')
 assert set(after['snippet']['tags'])==set(row['packageTags'])
 assert before['status']==after['status']
 assert {k:before['snippet'].get(k) for k in KEYS if k!='tags'}=={k:after['snippet'].get(k) for k in KEYS if k!='tags'}
 print('Restored 19 tags; all other writable snippet fields and complete status unchanged')
if __name__=='__main__':main()
