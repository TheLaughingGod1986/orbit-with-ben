"""Read-only exhaustive upload/tag audit. Credentials stay in memory."""
import json, urllib.request, urllib.parse, pathlib, datetime, re
OWB=pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben')
HOS=pathlib.Path('/Users/benjaminoats/YouTube/History Of Science')
def envfile(p):
 out={}
 for line in p.read_text().splitlines():
  if '=' in line and not line.lstrip().startswith('#'):
   k,v=line.split('=',1);out[k.strip()]=v.strip().strip('\"\'')
 return out
def req(url,token=None,data=None,method=None):
 headers={'Authorization':'Bearer '+token} if token else {}
 if isinstance(data,dict):data=urllib.parse.urlencode(data).encode()
 r=urllib.request.Request(url,data=data,headers=headers,method=method)
 return json.load(urllib.request.urlopen(r,timeout=35))
def token(channel):
 e=envfile(OWB/'07_Content-Ops/.env')
 return req('https://oauth2.googleapis.com/token',data=dict(client_id=e['GOOGLE_CLIENT_ID'],client_secret=e['GOOGLE_CLIENT_SECRET'],refresh_token=e['YOUTUBE_REFRESH_TOKEN' if channel=='owb' else 'YT_ANALYTICS_REFRESH_TOKEN_HOS'],grant_type='refresh_token'))['access_token']
def audit(channel,root):
 t=token(channel); api='https://www.googleapis.com/youtube/v3/'
 ch=req(api+'channels?part=id,contentDetails&mine=true',t)['items'][0]
 pl=ch['contentDetails']['relatedPlaylists']['uploads'];ids=set();page=''
 while True:
  d=req(api+'playlistItems?part=contentDetails&maxResults=50&playlistId='+pl+'&pageToken='+page,t)
  ids.update(i['contentDetails']['videoId'] for i in d.get('items',[]));page=d.get('nextPageToken','')
  if not page:break
 reg=OWB/('00_Brand/Channel-Setup/social/'+('hos/' if channel=='hos' else '')+'UPLOADS.json')
 registry=json.loads(reg.read_text()).get('videos',{});ids.update(registry)
 packages={}
 for p in root.glob('02_Video-Projects/**/PACKAGE_UPLOAD_RESULT*.json'):
  try:
   d=json.loads(p.read_text());vid=d.get('upload',{}).get('platformPostId')
   if vid:packages.setdefault(vid,[]).append(p.parent)
  except (ValueError,OSError):pass
 videos=[]
 for start in range(0,len(ids),50):
  batch=sorted(ids)[start:start+50]
  for v in req(api+'videos?part=snippet,status,contentDetails&id='+','.join(batch),t).get('items',[]):
   s=v['snippet'];status=v['status']
   if status.get('privacyStatus')!='public' and not status.get('publishAt'):continue
   candidates=[]
   r=registry.get(v['id'],{})
   if r.get('packageDir'):candidates.append(root/r['packageDir'])
   candidates+=packages.get(v['id'],[])
   tags=[];source=None
   for p in candidates:
    try:
     manifest=json.loads((p/'PACKAGE_MANIFEST.json').read_text());tags=manifest.get('tags',[])
     if not tags and manifest.get('tagsFile'):
      raw=(p/manifest['tagsFile']).read_text();tags=[x.strip() for x in re.split('[,\n]',raw) if x.strip()]
     if tags:source=str(p/'PACKAGE_MANIFEST.json');break
    except (ValueError,OSError):pass
   videos.append(dict(id=v['id'],title=s['title'],status=status,liveTags=s.get('tags',[]),packageTags=tags,package=source,snippet=s,duration=v.get('contentDetails',{}).get('duration')))
 out=dict(channel=channel,channelId=ch['id'],checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),videos=videos)
 pathlib.Path(__file__).with_name(channel+'_tags_before.json').write_text(json.dumps(out,indent=2)+'\n')
 print(channel,'total',len(videos),'no tags',sum(not v['liveTags'] for v in videos),'package matched',sum(bool(v['package']) for v in videos),'missing with package',sum(not v['liveTags'] and bool(v['packageTags']) for v in videos),'different',sum(bool(v['packageTags']) and v['liveTags']!=v['packageTags'] for v in videos),flush=True)
if __name__=='__main__':
 audit('owb',OWB);audit('hos',HOS)
