"""Recover explicit video-ID/tag pairs from historical upload indexes, read-only."""
import json,pathlib,subprocess,datetime
HERE=pathlib.Path(__file__).parent
ROOTS={'owb':pathlib.Path('/Users/benjaminoats/YouTube/orbit-with-ben'),'hos':pathlib.Path('/Users/benjaminoats/YouTube/History Of Science')}
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True,stderr=subprocess.DEVNULL)
def records(data):
 if isinstance(data,dict):
  tags=data.get('tags')
  if isinstance(tags,str):tags=[x.strip() for x in tags.split(',') if x.strip()]
  if isinstance(tags,list) and tags and all(isinstance(x,str) for x in tags):
   for key in ['video_id','youtube_video_id','videoId','youtubeId']:
    vid=data.get(key)
    if isinstance(vid,str) and len(vid)==11:yield vid,tags
  for value in data.values():yield from records(value)
 elif isinstance(data,list):
  for value in data:yield from records(value)
def main():
 comparison=json.loads((HERE/'current_comparison.json').read_text());out={}
 for channel,root in ROOTS.items():
  missing={r['id'] for r in comparison[channel]['rows'] if not r['baselineTags']}
  history=git(root,'log','--all','--format=%H','--name-only','--','02_Video-Projects/**/SHORTS_UPLOAD_INDEX.json','02_Video-Projects/**/UPLOAD_INDEX.json')
  rev=None;pairs=[]
  for line in history.splitlines():
   if len(line)==40 and all(c in '0123456789abcdef' for c in line):rev=line
   elif line.endswith('.json') and rev:pairs.append((rev,line))
  found={};scanned=0
  for rev,path in dict.fromkeys(pairs):
   try:data=json.loads(git(root,'show',rev+':'+path))
   except (subprocess.CalledProcessError,ValueError):continue
   scanned+=1
   for vid,tags in records(data):
    if vid not in missing:continue
    row=found.setdefault(vid,{'id':vid,'candidates':[]})
    if not any(x['tags']==tags for x in row['candidates']):row['candidates'].append({'revision':rev,'path':path,'tags':tags})
  out[channel]={'indexVersionsScanned':scanned,'recovered':list(found.values()),'unavailableIds':sorted(missing-set(found))}
  print(channel,'versions',scanned,'recovered',len(found),'unavailable',len(missing-set(found)),flush=True)
 (HERE/'historical_index_recovery.json').write_text(json.dumps({'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':out},indent=2)+'\n')
if __name__=='__main__':main()
