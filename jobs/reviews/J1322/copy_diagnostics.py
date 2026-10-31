import json,os,hashlib,subprocess
from pathlib import Path
OUT=Path('/Users/benjaminoats/_desk/jobs/J1322');NAS=Path('/Volumes/data/mac-mini-archive');H=Path('/Users/benjaminoats/YouTube/History Of Science');A=NAS/'J1322-20261031-0808-diagnostics'
assert (OUT/'recovery.done').read_text().strip()=='0'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
def st(p):
 s=p.stat();return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def mount():
 assert os.path.ismount('/Volumes/data')
 assert subprocess.check_output(['df','/Volumes/data'],text=True).splitlines()[-1].startswith('192.168.1.119:')
 assert os.statvfs(NAS).f_bavail*os.statvfs(NAS).f_frsize>5*2**30
mount();A.mkdir(exist_ok=False)
rows=[];before=subprocess.check_output(['df','-k',str(H)],text=True)
tracked=set(subprocess.check_output(['git','-C',str(H),'ls-files'],text=True).splitlines())
for r in json.load(open(OUT/'allowlist.json'))['excluded']:
 s=Path(r['source']);assert s.name in ['hos_008_master_v01_gain.mp4','hos_008_master_v01_park.mp4','hos_008_master_v01_rise.mp4']
 assert not s.is_symlink() and all(not p.is_symlink() for p in s.parents)
 assert str(s.relative_to(H)) not in tracked
 opened=subprocess.run(['lsof','-n','-F','n',str(s)],capture_output=True,text=True);assert opened.returncode==1 and not opened.stdout
 initial=st(s);h=sha(s);assert st(s)==initial
 d=A/str(s).lstrip('/');d.parent.mkdir(parents=True,exist_ok=True);assert not d.exists()
 mount();subprocess.run(['rsync','-a','--ignore-existing','--',str(s),str(d)],check=True)
 assert sha(d)==h and d.stat().st_size==s.stat().st_size
 rec={'source':str(s),'destination':str(d),'sha256':h,'bytes':s.stat().st_size,'allocated_local_bytes':s.stat().st_blocks*512,'allocated_nas_bytes':d.stat().st_blocks*512}
 rows.append(rec)
 for root in [OUT,A]:(root/'diagnostic_manifest.json').write_text(json.dumps({'before_df':before,'files':rows},indent=2)+'\n')
 assert sha(s)==h and st(s)==initial
 mount();pointer=s.parent/(s.name+'.MOVED_TO_NAS.txt');assert not pointer.exists();pointer.write_text(f"J1322\nNAS: {d}\nSHA256: {h}\nBytes: {rec['bytes']}\nManifest: {A}/diagnostic_manifest.json\n")
 assert st(s)==initial;s.unlink()
 for root in [OUT,A]:
  with (root/'diagnostic_removed.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n');f.flush();os.fsync(f.fileno())
 print('REMOVED VERIFIED DIAGNOSTIC',s,flush=True)
res={'before_df':before,'after_df':subprocess.check_output(['df','-k',str(H)],text=True),'files':rows,'unique_allocated_removed':sum(r['allocated_local_bytes'] for r in rows)}
for root in [OUT,A]:(root/'diagnostic_result.json').write_text(json.dumps(res,indent=2)+'\n')
print(res['after_df'],flush=True)
