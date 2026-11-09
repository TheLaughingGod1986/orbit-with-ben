"""J1106 public metadata only. Resumable; no media download except thumbnails."""
import concurrent.futures as cf, datetime as dt, hashlib, json, pathlib, subprocess, requests
O=pathlib.Path(__file__).parent
NOW=dt.datetime.now(dt.timezone.utc); CUTOFF=NOW-dt.timedelta(days=90)
CHANNELS={'astrum':'astrumspace','hotu':'HistoryoftheUniverse','sea':'SEA','kurzgesagt':'kurzgesagt','melodysheep':'melodysheep'}
for d in ['tabs','details','thumbs']: (O/d).mkdir(exist_ok=True)
def compact_research(j):
 return {k:v for k,v in j.items() if k in ['age_limit', 'availability', 'categories', 'channel', 'channel_id', 'channel_url', 'comment_count', 'description', 'duration', 'id', 'like_count', 'live_status', 'release_timestamp', 'tags', 'thumbnail', 'thumbnails', 'timestamp', 'title', 'upload_date', 'view_count', 'webpage_url']}

def ytdlp(args,path):
 if path.exists(): return json.loads(path.read_text())
 p=subprocess.run(['yt-dlp','--no-warnings',*args],capture_output=True,text=True,timeout=180)
 if p.returncode: raise RuntimeError(p.stderr[-500:])
 j=json.loads(p.stdout);j=compact_research(j) if path.parent.name == 'details' else j;path.write_text(json.dumps(j));return j

def tab(item):
 name,handle,kind=item
 try:
  j=ytdlp(['--flat-playlist','--extractor-args','youtubetab:approximate_date','--playlist-end','200','--dump-single-json',f'https://www.youtube.com/@{handle}/{kind}'],O/'tabs'/f'{name}_{kind}.json')
  es=j.get('entries',[]); result={'name':name,'handle':handle,'kind':kind,'channel':j.get('channel'),'channel_id':j.get('channel_id'),'total_tab_entries':len(es),'capped':len(es)==200,'entries':es}
  print('TAB',name,kind,len(es),flush=True);return result
 except Exception as e: print('TAB ERROR',name,kind,str(e),flush=True);return {'name':name,'kind':kind,'error':str(e),'entries':[]}
with cf.ThreadPoolExecutor(max_workers=4) as ex: tabs=list(ex.map(tab,[(n,h,k) for n,h in CHANNELS.items() for k in ['videos','shorts']]))
(O/'tab_index.json').write_text(json.dumps(tabs,indent=2))
# Approximate channel-page dates are screening only. Keep 150 days to cover rounding.
candidates={e['id']:e for t in tabs for e in t['entries'] if e.get('id') and (not e.get('timestamp') or e['timestamp']>=(NOW-dt.timedelta(days=150)).timestamp())}
print('DETAIL CANDIDATES',len(candidates),flush=True)
def detail(vid):
 try:
  j=ytdlp(['--skip-download','--ignore-no-formats-error','--dump-single-json',f'https://www.youtube.com/watch?v={vid}'],O/'details'/f'{vid}.json')
  if j.get('availability') in ('subscriber_only','premium_only','needs_auth','private'): raise RuntimeError('Excluded nonpublic availability: '+str(j['availability']))
  published=dt.datetime.fromtimestamp(j['timestamp'],dt.timezone.utc) if j.get('timestamp') else dt.datetime.strptime(j['upload_date'],'%Y%m%d').replace(tzinfo=dt.timezone.utc)
  return {'id':vid,'title':j.get('title'),'published':published.isoformat(),'timestamp_precision':'seconds' if j.get('timestamp') else 'day','views':j.get('view_count'),'duration':j.get('duration'),'channel':j.get('channel'),'channel_id':j.get('channel_id'),'url':j.get('webpage_url'),'thumbnails':j.get('thumbnails',[])}
 except Exception as e: print('DETAIL ERROR',vid,str(e),flush=True);return {'id':vid,'error':str(e)}
with cf.ThreadPoolExecutor(max_workers=4) as ex: details=list(ex.map(detail,candidates))
byid={e['id']:e for e in details};groups=[]; selected={}
for t in tabs:
 rows=[]
 for e in t['entries']:
  d=byid.get(e.get('id'),{})
  if d.get('error') or not d.get('published'): continue
  pub=dt.datetime.fromisoformat(d['published']);age=(NOW-pub).total_seconds()/86400
  if not CUTOFF<=pub<=NOW or d.get('views') is None: continue
  rows.append({**d,'age_days':age,'views_per_day':d['views']/max(age,1),'under_one_day':age<1})
 rows.sort(key=lambda e:e['views_per_day'],reverse=True)
 fast=rows[:10];slow=list(reversed(rows[-10:]))
 for e in fast+slow: selected[e['id']]=e
 groups.append({'channel':t['name'],'tab':t['kind'],'count_90d':len(rows),'fast_ids':[e['id'] for e in fast],'slow_ids':[e['id'] for e in slow],'overlap_ids':sorted(set(e['id'] for e in fast)&set(e['id'] for e in slow)),'all_90d':rows,'tab_error':t.get('error'),'listing_capped':t.get('capped',False)})
def thumb(e):
 p=O/'thumbs'/f"{e['id']}.jpg"
 try:
  if not p.exists():
   for t in sorted(e['thumbnails'],key=lambda t:t.get('width') or 0,reverse=True):
    r=requests.get(t['url'],timeout=30)
    if r.ok: p.write_bytes(r.content);break
  return {'id':e['id'],'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 except Exception as x: return {'id':e['id'],'error':str(x)}
with cf.ThreadPoolExecutor(max_workers=6) as ex: assets=list(ex.map(thumb,selected.values()))
report={'collected':NOW.isoformat(),'cutoff':CUTOFF.isoformat(),'method':'Public yt-dlp tabs and watch metadata; views / max(age days,1); tabs separate Shorts from longs; approximate date only screens to 150d, exact watch date filters to 90d; groups <20 overlap, never independent fast/slow samples.','groups':groups,'errors':[d for d in details if d.get('error')],'assets':assets}
(O/'study.json').write_text(json.dumps(report,indent=2));print('DONE',len(selected),'selected',len(report['errors']),'errors',flush=True)
