from pathlib import Path
import subprocess,json,hashlib,io,math,shutil
from PIL import Image,ImageDraw
repo=Path('/private/tmp/owb-J1321')
audit=repo/'00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10'
evidence=audit/'j1321_evidence';evidence.mkdir(exist_ok=True)
for which in ('ar2','ar3'):
 version='v05' if which=='ar2' else 'v09'
 work=Path('/private/tmp/J1321-render')/('assembly_'+version)/which
 master=work/f'owb_apophis_{which}_{version}.mp4'
 info=json.loads((work/'measure.json').read_text())
 assert info['loop_ok'] and all(info[k]==0 for k in ('picture_qa_exit','polish_exit','sfx_level_exit')), info
 n=math.ceil(info['total']*2)
 sheet=Image.new('RGB',(1008,math.ceil(n/4)*448))
 for i in range(n):
  t=i*.5
  r=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(master),'-frames:v','1','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True,check=True)
  im=Image.open(io.BytesIO(r.stdout))
  if i==0:im.save(evidence/f'{which}_{version}_frame0.jpg',quality=85)
  sheet.paste(im.resize((252,448)),((i%4)*252,(i//4)*448))
  ImageDraw.Draw(sheet).text(((i%4)*252+8,(i//4)*448+426),f'{t:.1f}s',fill='white')
 sheet.save(evidence/f'{which}_{version}_contact_0.5s.jpg',quality=80)
 for name in ('cuts.json','pool.json','measure.json','sfx_level.txt'):
  shutil.copy2(work/name,evidence/f'{which}_{name}')
 for name in ('picture_qa_stdout.txt','polish_stdout.txt','polish_gate.json'):
  shutil.copy2(work/'qa'/name,evidence/f'{which}_{name}')
 shutil.copy2(work/'qa/picture/PICTURE_QA.md',evidence/f'{which}_PICTURE_QA.md')
 # Exact compressed audio and decoded audio must match the original.
 old=Path('/Users/benjaminoats/YouTube/orbit-with-ben')/audit.relative_to(repo)/f'07_Edit-Project/assembly_j1308_v02/{which}/owb_apophis_{which}_v02.mp4'
 hashes=[]
 for f in (old,master):
  b=subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-c:a','copy','-f','adts','-'])
  hashes.append(hashlib.sha256(b).hexdigest())
 assert hashes[0]==hashes[1],hashes
 (evidence/f'{which}_audio_identity.json').write_text(json.dumps({'old':str(old),'new':str(master),'aac_payload_sha256':hashes[0],'identical':True},indent=2)+'\n')
print('evidence exported')
for which in ('ar2','ar3'):
 version='v05' if which=='ar2' else 'v09'
 work=Path('/private/tmp/J1321-render')/('assembly_'+version)/which
 master=work/f'owb_apophis_{which}_{version}.mp4'
 code="import sys;from pathlib import Path;sys.path.insert(0,'/Users/benjaminoats/YouTube/orbit-with-ben/scripts');from short_c37 import loop_metrics,finish_scan;m=finish_scan(Path(sys.argv[1]),loop_metrics(Path(sys.argv[1])));print({k:v for k,v in m.items() if k not in ('steps','frames_arr')})"
 r=subprocess.run(['/Users/benjaminoats/_desk/venv-graphics/bin/python','-c',code,str(master)],capture_output=True,text=True)
 (evidence/f'{which}_loop_stdout.txt').write_text(r.stdout+r.stderr)
 assert r.returncode==0,r.stderr
for version in ('v03','v04','v05','v06','v07','v08'):
 for which in ('ar2','ar3'):
  work=Path('/private/tmp/J1321-render')/('assembly_'+version)/which
  if not (work/'measure.json').exists():continue
  dest=evidence/'trials'/version/which;dest.mkdir(parents=True,exist_ok=True)
  for name in ('measure.json','qa/picture_qa_stdout.txt','qa/polish_stdout.txt'):
   shutil.copy2(work/name,dest/Path(name).name)
