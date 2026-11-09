import concurrent.futures as cf,json,pathlib,subprocess,datetime
O=pathlib.Path(__file__).parent;D=O/'extra_tabs';D.mkdir(exist_ok=True)
j=json.loads((O/'search.json').read_text());channels={}
for q in j['queries']:
 own=next((r['rank'] for r in q['results'] if r['channel']=='Orbit With Ben'),11)
 for r in q['results']:
  if r['rank']<own and r['channel']!='Kurzgesagt – In a Nutshell':channels[r['channel_id']]=r

def run(item):
 cid,r,tab=item;dest=D/f'{cid}_{tab}.json'
 try:
  p=subprocess.run(['yt-dlp','--no-warnings','--flat-playlist','--extractor-args','youtubetab:approximate_date','--playlist-end','200','--dump-single-json',f'https://www.youtube.com/channel/{cid}/{tab}'],capture_output=True,text=True,timeout=120)
  if p.returncode:raise RuntimeError(p.stderr[-400:])
  j=json.loads(p.stdout);dest.write_text(json.dumps(j));es=j.get('entries',[])
  out={'channel':r['channel'],'channel_id':cid,'tab':tab,'path':str(dest),'entries':len(es),'listing_capped':len(es)==200,'dates':'approximate screen only; exact 90-day cohort and rank still pending'}
 except Exception as e:out={'channel':r['channel'],'channel_id':cid,'tab':tab,'error':str(e)}
 print(json.dumps(out),flush=True);return out
with cf.ThreadPoolExecutor(max_workers=3) as ex:out=list(ex.map(run,[(cid,r,t) for cid,r in channels.items() for t in ['videos','shorts']]))
(O/'extra_catalog.json').write_text(json.dumps({'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':out},indent=2))
