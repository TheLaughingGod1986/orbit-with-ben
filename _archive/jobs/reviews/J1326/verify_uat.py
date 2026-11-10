from pathlib import Path
import json,hashlib,os,subprocess
O=Path(__file__).parent; root=Path('/Users/benjaminoats/YouTube/orbit-with-ben'); uat=root/'OWB UAT'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
# Exact existing NAS archive subtrees only. Never writes to NAS.
nasroots=[Path('/Volumes/data/mac-mini-archive/youtube-staging/029'),Path('/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/029_shorts_v04'),Path('/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-31/owb/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts')]
idx={}
for nr in nasroots:
 for dp,ds,fs in os.walk(nr):
  for f in fs:idx.setdefault(f,[]).append(Path(dp)/f)
rows=[]
for p in sorted(uat.glob('*.mp4')):
 h=sha(p); matches=[]
 canonical=list((root/'02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts').glob('*/06_Final-Exports/'+p.name))
 for dest in canonical+idx.get(p.name,[]):
  if dest.stat().st_size==p.stat().st_size:
   dh=sha(dest)
   matches.append({'path':str(dest),'sha256':dh,'match':h==dh})
 rows.append({'source':str(p),'allocated_bytes':p.stat().st_blocks*512,'bytes':p.stat().st_size,'sha256':h,'copies':matches,'decision':'KEEP','reason':'Do not remove current/previous or uploaded version duplicates without exact watch-path disambiguation; bare OWB UAT watch links do not prove which physical directory serves the card.'})
O.joinpath('uat_hash_proof.json').write_text(json.dumps({'mount':subprocess.run(['df','-k','/Volumes/data'],capture_output=True,text=True).stdout,'nas_roots':list(map(str,nasroots)),'files':rows},indent=2))
print(len(rows),'UAT media hashed;',sum(any(c['match'] for c in r['copies']) for r in rows),'have verified copies')
