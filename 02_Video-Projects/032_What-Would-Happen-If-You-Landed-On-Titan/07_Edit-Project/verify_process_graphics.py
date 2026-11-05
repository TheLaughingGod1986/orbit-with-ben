"""Measure J2089 process preview layout at every planned frame; no review verdict."""
import sys,json,hashlib,subprocess
from pathlib import Path
from PIL import ImageChops
here=Path(__file__).resolve().parent
sys.path.insert(0,str(here))
import process_graphics as g
out=Path('/Users/benjaminoats/_desk/cache/J2089/process_previews_v02')
subprocess.run([sys.executable,str(here/'process_graphics.py'),'--out',str(out)],check=True)
records=[]
for spec in g.SPECS:
 bounds=[]
 for n in range(109):
  b=g.frame(spec,n/30).getchannel('A').getbbox()
  if b:
   assert b[0]>=96 and b[1]>=54 and b[2]<=1824 and b[3]<=1026,(spec['id'],n,b)
   bounds.append(b)
 assert g.frame(spec,0).getbbox() is None
 assert g.frame(spec,3.6).getbbox() is None
 assert ImageChops.difference(g.frame(spec,.8),g.frame(spec,1.5)).getbbox() is not None
 records.append(dict(id=spec['id'],checked_frames=109,all_frame_bounds_inside_5_percent=True,entry_exit_alpha_zero=True,changing_frames=True))
manifest=json.loads((out/'PROCESS_MANIFEST_v01.json').read_text())
for clip in manifest['clips']:
 assert hashlib.sha256(Path(clip['preview']).read_bytes()).hexdigest()==clip['preview_sha256']
for extra in [[],['--approved','invalid','--review-ref','TEST']]:
 r=subprocess.run([sys.executable,str(here/'process_graphics.py'),'--out',str(out/'guard_probe'),'--render',*extra],capture_output=True,text=True)
 assert r.returncode==2
assert not (out/'guard_probe').exists()
result=dict(job='J2089',status='MEASUREMENTS_ONLY_NO_APPROVAL',drafts=records,preview_hashes='MATCH',render_guard='MISSING_APPROVAL_AND_UNKNOWN_ID_REJECTED_EXIT_2',visual_still_inspection='Codex inspected all seven full-size stills; not motion or composite review',rain_scale=dict(diameter_ratio=9.5/6.5,fall_speed_ratio=9.2/1.6,spatial_speed_scale='10 pixels per second per m/s, same for both; linear; no wrap within 3.6s'),not_verified=['Source/label review decision','Actual moving-plate contrast and placement','Native motion perception','Final picture, music and polish gates'])
(here/'PROCESS_VERIFICATION_v02.json').write_text(json.dumps(result,indent=2)+'\n')
for name in ['PROCESS_MANIFEST_v01.json','PROCESS_CHECKS_v01.json']:(here/name.replace('_v01','_v02')).write_bytes((out/name).read_bytes())
print('7 preview hashes match; 763 sampled frames within safe area; entry/exit transparency and changing frames checked; both render guards exit 2; no media rendered.')
