"""Continue J1106 search-neighbour study, public metadata only; resumable cache."""
import concurrent.futures as cf,datetime as dt,hashlib,json,pathlib,subprocess,time,requests
O=pathlib.Path(__file__).parent;NOW=dt.datetime.now(dt.timezone.utc);CUT=NOW-dt.timedelta(days=90)
INDEX=json.loads((O/'extra_catalog.json').read_text())['channels'];D=O/'extra_details';D.mkdir(exist_ok=True);T=O/'extra_thumbs';T.mkdir(exist_ok=True)
def compact_research(j):
 return {k:v for k,v in j.items() if k in ['age_limit', 'availability', 'categories', 'channel', 'channel_id', 'channel_url', 'comment_count', 'description', 'duration', 'id', 'like_count', 'live_status', 'release_timestamp', 'tags', 'thumbnail', 'thumbnails', 'timestamp', 'title', 'upload_date', 'view_count', 'webpage_url']}

def command(args):
 p=subprocess.run(['yt-dlp','--no-warnings',*args],capture_output=True,text=True,timeout=120)
 if p.returncode:raise RuntimeError(p.stderr[-450:])
 return json.loads(p.stdout)
def group(g):
 out={**g,'all_90d':[],'errors':[],'boundary':[],'sampled_at':NOW.isoformat()}
 try:
  if g.get('error'):return out
  path=pathlib.Path(g['path']);raw=json.loads(path.read_text())
  if g['listing_capped']:
   more=path.with_name(path.stem+'_1000.json')
   if more.exists():raw=json.loads(more.read_text())
   else:
    raw=command(['--flat-playlist','--extractor-args','youtubetab:approximate_date','--playlist-end','1000','--dump-single-json',f"https://www.youtube.com/channel/{g['channel_id']}/{g['tab']}"]);more.write_text(json.dumps(raw))
  old=0
  for e in raw.get('entries',[]):
   vid=e['id'];dest=D/f'{vid}.json'
   try:
    shared=O/'details'/f'{vid}.json'
    if dest.exists(): j=json.loads(dest.read_text())
    elif shared.exists():j=json.loads(shared.read_text())
    else:
     j=command(['--skip-download','--ignore-no-formats-error','--dump-single-json',f'https://www.youtube.com/watch?v={vid}']);j=compact_research(j);dest.write_text(json.dumps(j));time.sleep(.35)
    if j.get('availability') in ('subscriber_only','premium_only','needs_auth','private'):
     out['errors'].append({'id':vid,'reason':'excluded nonpublic '+j['availability']});continue
    pub=dt.datetime.fromtimestamp(j['timestamp'],dt.timezone.utc) if j.get('timestamp') else dt.datetime.strptime(j['upload_date'],'%Y%m%d').replace(tzinfo=dt.timezone.utc)
    if pub<CUT:
     old+=1;out['boundary'].append({'id':vid,'published':pub.isoformat()})
     if old>=2:break
     continue
    old=0
    if pub>NOW:continue
    age=(NOW-pub).total_seconds()/86400
    if j.get('view_count') is None:raise RuntimeError('View count missing')
    out['all_90d'].append({'id':vid,'title':j.get('title'),'published':pub.isoformat(),'age_days':age,'under_one_day':age<1,'views':j['view_count'],'views_per_day':j['view_count']/max(age,1/86400),'duration':j.get('duration'),'channel':j.get('channel'),'url':f'https://www.youtube.com/watch?v={vid}','thumbnails':j.get('thumbnails',[])})
   except Exception as ex:out['errors'].append({'id':vid,'reason':str(ex)});print('ERROR',g['channel'],vid,str(ex),flush=True)
  rows=sorted(out['all_90d'],key=lambda e:e['views_per_day'],reverse=True);out['all_90d']=rows
  out['fast_ids']=[e['id'] for e in rows[:10]];out['slow_ids']=[e['id'] for e in reversed(rows[-10:])];out['overlap_ids']=sorted(set(out['fast_ids'])&set(out['slow_ids']))
  out['coverage']='Stopped after two older uploads in newest-first tab; confirm chronological order and review errors. No minimum sample invented.'
  out['assets']=[]
  for e in rows:
   if e['id'] not in out['fast_ids']+out['slow_ids']:continue
   p=T/f"{e['id']}.jpg"
   try:
    if not p.exists():
     for th in sorted(e['thumbnails'],key=lambda t:t.get('width') or 0,reverse=True):
      r=requests.get(th['url'],timeout=30)
      if r.ok:p.write_bytes(r.content);break
    out['assets'].append({'id':e['id'],'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   except Exception as ex:out['errors'].append({'id':e['id'],'reason':'thumbnail '+str(ex)})
 except Exception as ex:out['group_error']=str(ex)
 (O/f"extra_{g['channel_id']}_{g['tab']}_study.json").write_text(json.dumps(out,indent=2));print('GROUP DONE',g['channel'],g['tab'],len(out['all_90d']),len(out['errors']),flush=True);return out
with cf.ThreadPoolExecutor(max_workers=2) as ex:groups=list(ex.map(group,INDEX))
(O/'extra_study.json').write_text(json.dumps({'collected':NOW.isoformat(),'cutoff':CUT.isoformat(),'groups':groups},indent=2));print('ALL DONE',len(groups),flush=True)
