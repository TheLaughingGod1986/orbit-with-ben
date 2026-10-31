import os,json,hashlib,subprocess,time
from pathlib import Path
ROOT=Path('/Users/benjaminoats/YouTube'); H=ROOT/'History Of Science'; O=ROOT/'orbit-with-ben'
BASE=H/'02_Video-Projects/008_Lightning-Franklin/07_Edit-Project'
OUT=Path('/Users/benjaminoats/_desk/jobs/J1322')
NAS=Path('/Volumes/data/mac-mini-archive'); ARCH=NAS/'J1322-20261031-0808-bounded'

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def mount():
 assert os.path.ismount('/Volumes/data'), 'NAS unmounted'
 assert subprocess.check_output(['df','/Volumes/data'],text=True).splitlines()[-1].startswith('192.168.1.119:'),'Wrong mount'
 assert os.statvfs(NAS).f_bavail*os.statvfs(NAS).f_frsize>5*2**30

def stamp(p):
 s=p.stat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
q=json.load(open(O/'jobs/queue.json'))['jobs']
active=[j for j in q if j.get('status') not in ['done','cancelled'] and j['id']!='J1322']
references=[]
# Current builders and their cut/pool records; current/previous masters retained.
for folder in ['master_v03','master_v02','_desk/008/rough_v12','_desk/008/rough_v11']:
 for p in (BASE/folder).rglob('*'):
  if p.is_file() and p.suffix in ['.py','.json','.md','.csv']:references.append((str(p),p.read_text(errors='ignore')))
for root in [O,H]:
 for p in (root/'00_Brand/Channel-Setup').rglob('*.json'):
  if p.name in ['UPLOADS.json','BUFFER_POSTS.json'] or 'PACKAGE' in p.name: references.append((str(p),p.read_text(errors='ignore')))
references.extend((j['id'],json.dumps({k:j.get(k) for k in ['title','body','remaining_action','watch','awaits']})) for j in active)
tracked=set(subprocess.check_output(['git','-C',str(H),'ls-files'],text=True).splitlines())
openfiles=subprocess.run(['lsof','-n','-F','n'],capture_output=True,text=True).stdout
pairs=[]
for v in ['01','02']:
 s=BASE/f'_desk/008/rough_v{v}/hos_008_rough_v{v}.mp4'
 d=NAS/f'YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/rough_v{v}/hos_008_rough_v{v}.mp4'
 pairs.append((s,d))
# Diagnostic gain/park/rise outputs are not the current or previous master.
for name in ['gain','park','rise']:
 s=BASE/f'_precheck/master_v01/hos_008_master_v01_{name}.mp4'
 d=NAS/('YouTube/'+str(s.relative_to(ROOT)))
 pairs.append((s,d))
records=[];exclusions=[]
for s,d in pairs:
 assert s.is_file() and not s.is_symlink()
 assert all(not p.is_symlink() for p in s.parents)
 assert str(s.relative_to(H)) not in tracked
 assert '\nn'+str(s)+'\n' not in '\n'+openfiles
 hits=[label for label,t in references if str(s) in t or str(s.relative_to(H)) in t]
 if hits:
  exclusions.append({'source':str(s),'reason':'active/current reference','references':hits});continue
 if not d.is_file():
  exclusions.append({'source':str(s),'reason':'existing NAS duplicate unavailable; needs copy checkpoint'});continue
 state=stamp(s);sha=digest(s);assert stamp(s)==state
 assert d.stat().st_size==s.stat().st_size and digest(d)==sha, f'mismatch {s}'
 records.append({'source':str(s),'destination':str(d),'sha256':sha,'bytes':s.stat().st_size,'allocated_local_bytes':s.stat().st_blocks*512,'allocated_nas_bytes':d.stat().st_blocks*512,'source_state':state})
report={'job':'J1322','before_df':subprocess.check_output(['df','-k',str(H)],text=True),'allowlist':records,'excluded':exclusions,'preserved':'all current/previous masters and scratch, VO, graphics, source plates, worktrees, J1100/J1320/J1321 inputs; other candidates unproven and remain local'}
(OUT/'allowlist.json').write_text(json.dumps(report,indent=2)+'\n')
mount();ARCH.mkdir(exist_ok=False)
(ARCH/'allowlist.json').write_text(json.dumps(report,indent=2)+'\n')
for r in records:
 mount();s=Path(r['source']);d=Path(r['destination']);assert stamp(s)==r['source_state']
 assert digest(d)==r['sha256'] and digest(s)==r['sha256'] and stamp(s)==r['source_state']
 pointer=s.parent/(s.name+'.MOVED_TO_NAS.txt')
 assert not pointer.exists()
 pointer.write_text(f"J1322 verified duplicate offload\nNAS: {d}\nSHA256: {r['sha256']}\nBytes: {r['bytes']}\nManifest: {ARCH}/allowlist.json\n")
 # All records durable before unlink; no directory deletion.
 mount();assert stamp(s)==r['source_state'];s.unlink()
 with (OUT/'removed.jsonl').open('a') as f:f.write(json.dumps(r)+'\n');f.flush();os.fsync(f.fileno())
 with (ARCH/'removed.jsonl').open('a') as f:f.write(json.dumps(r)+'\n');f.flush();os.fsync(f.fileno())
 print('REMOVED VERIFIED LOCAL DUPLICATE',s,flush=True)
report['after_df']=subprocess.check_output(['df','-k',str(H)],text=True)
report['unique_allocated_removed']=sum(r['allocated_local_bytes'] for r in records)
(OUT/'result.json').write_text(json.dumps(report,indent=2)+'\n');(ARCH/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['after_df'],report['unique_allocated_removed'],flush=True)
