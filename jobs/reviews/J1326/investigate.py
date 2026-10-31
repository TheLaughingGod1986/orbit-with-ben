import os,json,subprocess,datetime,pwd,re,hashlib
from pathlib import Path
OUT=Path(__file__).parent
OWB=Path('/Users/benjaminoats/YouTube/orbit-with-ben'); HOS=Path('/Users/benjaminoats/YouTube/History Of Science')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def cmd(*args): return subprocess.run(args,capture_output=True,text=True).stdout
old=json.load(open('/private/tmp/J1322-records/jobs/reviews/J1322/deferred.json'))
roots=[Path('/private/tmp'),Path('/Users/benjaminoats/_desk/renders'),Path('/Users/benjaminoats/_desk/008'),OWB/'00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project']
roots += [Path(x['candidate']) for x in old]
roots += [next((OWB if film in ['031','032'] else HOS).glob('02_Video-Projects/'+film+'_*'))/'02_Voiceover' for film in ['031','032','013']]
# Bounded census only: listed scratch, exact deferred candidates and T2-C VO.
files={}; errors=[]
for root in roots:
 paths=[root] if root.is_file() else (Path(dp)/f for dp,ds,fs in os.walk(root,followlinks=False) for f in fs)
 for p in paths:
  try:
   if p.is_symlink(): continue
   s=p.stat(); files[str(p)]={'bytes':s.st_size,'allocated':s.st_blocks*512,'mtime_ns':s.st_mtime_ns,'dev':s.st_dev,'ino':s.st_ino,'owner':pwd.getpwuid(s.st_uid).pw_name}
  except OSError as e: errors.append({'path':str(p),'error':str(e)})
OUT.joinpath('census_first.json').write_text(json.dumps({'at':now(),'roots':list(map(str,roots)),'df':cmd('df','-k','/'),'files':files,'errors':errors},indent=2))
print('census',len(files),'files',len(errors),'errors')
print('largest exact files:')
for p,s in sorted(files.items(),key=lambda x:x[1]['allocated'],reverse=True)[:20]: print(round(s['allocated']/2**30,3),p)
# Reference corpus limited to production records/code; skip secret/cache/media.
texts=[]
for repo in [OWB,HOS]:
 for area in ['02_Video-Projects','00_Brand/Channel-Setup/social','05_Analytics/kanban','jobs']:
  for dp,ds,fs in os.walk(repo/area):
   ds[:]=[d for d in ds if d not in ['node_modules','.git','.secrets','_archive','__pycache__'] and not d.startswith('_work_')]
   for f in fs:
    p=Path(dp)/f
    if p.suffix.lower() not in ['.json','.md','.csv','.py','.txt','.jsonl'] or p.name=='queue.json' or 'deferred' in f: continue
    try:
     if p.stat().st_size>3_000_000: continue
     texts.append((str(p),p.read_text(errors='replace')))
    except OSError: pass
# Active queue only: historical jobs remain evidence but are not active references.
q=json.load(open(OWB/'jobs/queue.json'))['jobs']
for j in q:
 if j.get('status') not in ['done','cancelled']:
  texts.append(('queue:'+j['id'],json.dumps({k:j.get(k) for k in ['body','result','remaining_action','awaits','hold']})))
refs={}
for x in old:
 p=x['candidate']; name=Path(p).name
 hits=[]
 for src,t in texts:
  if '/jobs/reviews/J132' in src: continue
  if p in t or name in t:
   lines=[(i+1,line[:600]) for i,line in enumerate(t.splitlines()) if p in line or name in line]
   hits.append({'source':src,'lines':lines[:8]})
 refs[p]=hits
OUT.joinpath('references.json').write_text(json.dumps(refs,indent=2))
print('reference corpus',len(texts),'records;',sum(bool(v) for v in refs.values()),'candidate hits')
