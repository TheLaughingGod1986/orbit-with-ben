#!/usr/bin/env python3
"""Collect completed J1321 renders without overwriting any prior delivery."""
import hashlib,json,subprocess,shutil
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
REL=Path('00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10')
AUDIT=ROOT/REL
HERE=Path(__file__).resolve().parent
DEST=AUDIT/'07_Edit-Project/assembly_j1321_delivery_v02'
EVIDENCE=HERE/'J1321_evidence'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def run(args): return subprocess.check_output([str(x) for x in args])
def audio_sha(p): return hashlib.sha256(run(['ffmpeg','-v','error','-i',p,'-map','0:a','-c','copy','-f','adts','-'])).hexdigest()
old={'ar1':('v01','49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07'),'ar2':('v02','73cbb7c0174fcbdf774a059f189ac5ce5b8f3e1274291bbb8e2f4fd47b023405'),'ar3':('v02','cfcb23508be4c66bbb3ced01ab656512e1feb0b209fddd7a4f22f88da6ca5dad')}
for k,(v,h) in old.items():
 p=AUDIT/f'07_Edit-Project/assembly_j1308_{v}'/k/f'owb_apophis_{k}_{v}.mp4'
 assert sha(p)==h,(k,'old master changed')
assert not DEST.exists(),'Delivery exists; refusing overwrite'
DEST.mkdir(parents=True)
summary={}
for k,v in [('ar2','v06'),('ar3','v03')]:
 src=Path(f'/private/tmp/J1321-render-{v}')/k
 info=json.loads((src/'measure.json').read_text())
 assert info['loop_ok'] and all(info[x]==0 for x in ['picture_qa_exit','polish_exit','sfx_level_exit']), info
 out=DEST/k; out.mkdir()
 for p in src.iterdir():
  if p.name=='picture.mp4': continue
  if p.is_dir(): shutil.copytree(p,out/p.name)
  else: shutil.copy2(p,out/p.name)
 master=out/f'owb_apophis_{k}_{v}.mp4'
 assert sha(master)==info['sha256']
 prior=AUDIT/'07_Edit-Project/assembly_j1308_v02'/k/f'owb_apophis_{k}_v02.mp4'
 assert audio_sha(master)==audio_sha(prior),'AAC changed'
 info['master']=str(master);info['audio_sha256']=audio_sha(master)
 (out/'measure.json').write_text(json.dumps(info,indent=2)+'\n')
 ev=EVIDENCE/k;ev.mkdir(parents=True,exist_ok=True)
 for name in ['measure.json','cuts.json','pool.json','sfx_level.txt']:
  shutil.copy2(out/name,ev/name)
 for name in ['picture_qa_stdout.txt','polish_stdout.txt','polish_gate.json']:
  shutil.copy2(out/'qa'/name,ev/name)
 shutil.copy2(out/'qa/picture/picture_qa.json',ev/'picture_qa.json')
 imgs=out/'review_frames';imgs.mkdir()
 raw=run(['ffmpeg','-v','error','-i',master,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
 Image.frombytes('RGB',(1080,1920),raw).save(imgs/f'{k}_{v}_frame0.jpg',quality=85)
 raw=run(['ffmpeg','-v','error','-i',master,'-vf',r'select=not(mod(n\,15)),scale=252:448','-fps_mode','vfr','-f','rawvideo','-pix_fmt','rgb24','-'])
 size=252*448*3;n=len(raw)//size
 sheet=Image.new('RGB',(1008,((n+3)//4)*448));d=ImageDraw.Draw(sheet)
 for i in range(n):
  tile=Image.frombytes('RGB',(252,448),raw[i*size:(i+1)*size]);sheet.paste(tile,((i%4)*252,(i//4)*448));d.text(((i%4)*252+4,(i//4)*448+4),f'{i/2:.1f}s',fill='white',stroke_width=1,stroke_fill='black')
 sheet.save(imgs/f'{k}_{v}_contact_0.5s.jpg',quality=80)
 info['review_frames']=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in imgs.iterdir()]
 summary[k]=info
(EVIDENCE/'DELIVERY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
