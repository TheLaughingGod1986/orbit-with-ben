"""J2711 exact-plan text-only repair. Run through the YouTube/Buffer desk lock."""
import json,datetime,pathlib,re,time
from buffer_read import gql
HERE=pathlib.Path(__file__).parent
FIELDS='id status text dueAt channelId assets{__typename ... on VideoAsset{id source thumbnail video{title thumbnailOffset}}} externalLink metadata{__typename ... on FacebookPostMetadata{type title firstComment annotations{content indices text url type displayValue serviceEntityId} linkAttachment{__typename}} ... on InstagramPostMetadata{type firstComment shouldShareToFeed isAiGenerated link geolocation{__typename} stickerFields{__typename}}}'
def allowed(before,current,now):
 return (current==before and current['status']=='scheduled' and datetime.datetime.fromisoformat(current['dueAt'].replace('Z','+00:00'))>now+datetime.timedelta(minutes=10) and not re.search(r'#[\w]+',current['text']))
def repair(apply=False):
 out=[]
 for row in json.loads((HERE/'scheduled_repairs_preview.json').read_text()):
  p=gql('query($input:PostInput!){post(input:$input){'+FIELDS+'}}',{'input':{'id':row['postId']}})
  current=p['data']['post']
  before={k:row['before'][k] for k in ['id','status','text','dueAt','channelId']}
  observed={k:current[k] for k in before}
  if current['text']==row['text']:
   assert {k:v for k,v in observed.items() if k!='text'}=={k:v for k,v in before.items() if k!='text'}
   out.append(dict(postId=row['postId'],videoId=row['id'],alreadyRepaired=True,after=current))
   (HERE/'scheduled_repairs_result.json').write_text(json.dumps(out,indent=2)+'\n')
   continue
  assert allowed(before,observed,datetime.datetime.now(datetime.timezone.utc)), 'Post changed or is no longer safely scheduled'
  limit={'instagram':2200,'facebook':5000,'threads':500}[row['channel']]
  assert len(row['text'])<=limit
  assert row['text'].startswith(current['text'].rstrip()+'\n\n')
  result=dict(postId=row['postId'],videoId=row['id'],before=current,text=row['text'],dryRun=not apply)
  if apply:
   payload={'id':row['postId'],'text':row['text']}
   assert len(current['assets'])==1 and current['assets'][0]['__typename']=='VideoAsset'
   asset=current['assets'][0]
   payload['assets']=[{'video':{'url':asset['source'],'metadata':{k:v for k,v in asset['video'].items() if v is not None}}}]
   if row['channel'] in ['facebook','instagram']:
    meta=current['metadata'].copy();meta.pop('__typename',None)
    if row['channel']=='facebook':
     assert meta.pop('title') is None
     assert meta['linkAttachment'] is None
     meta.pop('annotations') # Buffer parses URLs and new hashtags from the unchanged body.
    else:assert meta['geolocation'] is None and meta['stickerFields'] is None
    payload['metadata']={row['channel']:meta}
   result['mutation']=gql('mutation($input:EditPostInput!){editPost(input:$input){__typename ... on PostActionSuccess{post{id text dueAt status}} ... on MutationError{message}}}',{'input':payload})
   assert result['mutation'].get('data',{}).get('editPost',{}).get('__typename')=='PostActionSuccess', result['mutation']
   (HERE/'scheduled_repairs_pending.json').write_text(json.dumps(result,indent=2)+'\n')
   after=gql('query($input:PostInput!){post(input:$input){'+FIELDS+'}}',{'input':{'id':row['postId']}})['data']['post']
   for attempt in range(4):
    if after['text']==row['text']:break
    time.sleep(1)
    after=gql('query($input:PostInput!){post(input:$input){'+FIELDS+'}}',{'input':{'id':row['postId']}})['data']['post']
   result['after']=after
   (HERE/'scheduled_repairs_pending.json').write_text(json.dumps(result,indent=2)+'\n')
   assert after['text']==row['text']
   assert {k:v for k,v in after.items() if k not in ['text','metadata']}=={k:v for k,v in current.items() if k not in ['text','metadata']}
   am=(after.get('metadata') or {}).copy();bm=(current.get('metadata') or {}).copy()
   aa=am.pop('annotations',[]);ba=bm.pop('annotations',[])
   assert am==bm
   assert all(a in aa for a in ba), 'Existing link annotations changed' 
  out.append(result)
  (HERE/'scheduled_repairs_result.json').write_text(json.dumps(out,indent=2)+'\n')
 print('verified',len(out),'scheduled captions','applied' if apply else 'dry-run')
if __name__=='__main__':
 import sys
 repair('--apply' in sys.argv)
