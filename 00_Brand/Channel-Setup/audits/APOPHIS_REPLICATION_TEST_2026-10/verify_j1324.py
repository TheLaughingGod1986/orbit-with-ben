from pathlib import Path
import subprocess,json,hashlib,shutil,sys,io,math
from PIL import Image,ImageDraw
R=Path('/Users/benjaminoats/YouTube/orbit-with-ben');O=Path('/private/tmp/J1324-render');E=Path(__file__).parent/'j1324_evidence';M=O/'owb_apophis_ar2_v08.mp4';OLD=Path('/private/tmp/J1321-render/assembly_v05/ar2')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def run(name,cmd):
 p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);(E/name).write_text(p.stdout+p.stderr);return p.returncode
cuts=json.loads((OLD/'cuts.json').read_text());cuts[5]['framing']['offset']=468.0
for c in cuts:
 if c['source'].startswith('Crew2'):c['upscale']=1.46 if c['timeline_in']==14.767 else .96
(E/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
pool=json.loads((OLD/'pool.json').read_text())
for p in pool:
 if p['id'].startswith('Crew2'):p['title']='NASA Crew-2 ISS footage, native sharp view with same-source blurred fill'
(E/'pool.json').write_text(json.dumps(pool,indent=2)+'\n')
results={}
results['picture']=run('picture_stdout.txt',[sys.executable,R/'scripts/picture_qa.py',M,'--cuts',E/'cuts.json','--pool',E/'pool.json','--out-dir',O/'picture_qa'])
results['polish']=run('polish_stdout.txt',[sys.executable,R/'scripts/polish_gate.py',M,'--cuts',E/'cuts.json','--out',E/'polish_gate.json'])
code="import sys;from pathlib import Path;sys.path.insert(0,str(Path(sys.argv[1])/'scripts'));from short_c37 import loop_metrics,finish_scan;m=finish_scan(Path(sys.argv[2]),loop_metrics(Path(sys.argv[2])));print({k:v for k,v in m.items() if k not in ('steps','frames_arr')})"
results['loop']=run('loop_stdout.txt',[sys.executable,'-c',code,R,M])
results['sfx']=run('sfx_stdout.txt',[sys.executable,R/'scripts/sfx_kit.py','level','--vo',OLD/'stem_vo.wav','--sfx',OLD/'stem_sfx.wav','--minutes',19.4/60])
for name in ['PICTURE_QA.md','picture_qa.json']:
 if (O/'picture_qa'/name).exists():shutil.copy2(O/'picture_qa'/name,E/name)
hashes=[]
for p in [Path('/Volumes/data/mac-mini-archive/jobs/J1321/masters/owb_apophis_ar2_v05.mp4'),M]:
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-']);hashes.append(hashlib.sha256(b).hexdigest())
(E/'audio_identity.json').write_text(json.dumps({'aac_sha256':hashes,'identical':hashes[0]==hashes[1]},indent=2)+'\n');assert hashes[0]==hashes[1]
sheet=Image.new('RGB',(1008,448*10))
for i in range(39):
 t=i*.5
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(M),'-frames:v','1','-f','image2pipe','-vcodec','mjpeg','-'])
 im=Image.open(io.BytesIO(b))
 if i in [0,32]:im.save(E/('frame0.jpg' if i==0 else 'late_16s.jpg'),quality=95)
 sheet.paste(im.resize((252,448)),((i%4)*252,(i//4)*448));ImageDraw.Draw(sheet).text(((i%4)*252+8,(i//4)*448+426),f'{t:.1f}s',fill='white')
sheet.save(E/'contact_0.5s.jpg',quality=80)
(E/'gates.json').write_text(json.dumps(results,indent=2)+'\n')
print(results,flush=True)
# Archive candidate regardless of gate result; a gate FAIL remains a FAIL.
D=Path('/Volumes/data/mac-mini-archive/jobs/J1324/masters');assert Path('/Volumes/data').is_mount();D.mkdir(parents=True,exist_ok=True)
dest=D/M.name;assert not dest.exists();shutil.copy2(M,dest);assert sha(M)==sha(dest)
(E/'master.json').write_text(json.dumps({'master':str(dest),'sha256':sha(dest),'bytes':dest.stat().st_size,'gates':results},indent=2)+'\n')
