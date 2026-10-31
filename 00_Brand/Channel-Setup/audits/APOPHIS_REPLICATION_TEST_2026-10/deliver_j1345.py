"""Persist J1345 evidence and review frames; never overwrite previous delivery."""
import hashlib,json,subprocess,shutil
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
REL=Path('00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10')
AUDIT=ROOT/REL
HERE=Path(__file__).resolve().parent
DEST=AUDIT/'07_Edit-Project/assembly_j1345_v05/ar3'
EV=HERE/'J1345_evidence'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def run(a):return subprocess.check_output([str(x) for x in a])
def audio(p):return hashlib.sha256(run(['ffmpeg','-v','error','-i',p,'-map','0:a','-c','copy','-f','adts','-'])).hexdigest()
src=Path('/private/tmp/J1345-render-v05/ar3')
info=json.loads((src/'measure.json').read_text())
assert info['loop_ok'] and all(info[x]==0 for x in ['picture_qa_exit','polish_exit','sfx_level_exit']),info
assert not DEST.exists(),'refuse overwrite'
DEST.mkdir(parents=True)
for p in src.iterdir():
 if p.name=='picture.mp4':continue
 if p.is_dir():shutil.copytree(p,DEST/p.name)
 else:shutil.copy2(p,DEST/p.name)
master=DEST/'owb_apophis_ar3_v05.mp4'
assert sha(master)==info['sha256']
prior=AUDIT/'07_Edit-Project/assembly_j1321_delivery_v02/ar3/owb_apophis_ar3_v03.mp4'
assert audio(master)==audio(prior)
protected={}
for name,p in {
 'ar1_v01':AUDIT/'07_Edit-Project/assembly_j1308_v01/ar1/owb_apophis_ar1_v01.mp4',
 'ar2_v06':AUDIT/'07_Edit-Project/assembly_j1321_delivery_v02/ar2/owb_apophis_ar2_v06.mp4',
 'ar3_v03':prior}.items():protected[name]={'path':str(p),'sha256':sha(p)}
assert protected['ar2_v06']['sha256']=='6d517aad6c61a0f12d67b4f2f7990f94ea165e17e01055b56873e89415bf8e67'
assert protected['ar3_v03']['sha256']=='caf3f3b0e2290c703d0cb4d33d587580eaaf43e8ef83ec87e258af1727474ea7'
imgs=DEST/'review_frames';imgs.mkdir()
for label,t in [('frame0',0),('duration_13.1',13.1),('totality_15.2',15.2)]:
 run(['ffmpeg','-v','error','-ss',t,'-i',master,'-frames:v',1,imgs/f'{label}.png'])
raw=run(['ffmpeg','-v','error','-i',master,'-vf',r'select=not(mod(n\,15)),scale=252:448','-fps_mode','vfr','-f','rawvideo','-pix_fmt','rgb24','-'])
size=252*448*3;n=len(raw)//size
sheet=Image.new('RGB',(1008,((n+3)//4)*448));d=ImageDraw.Draw(sheet)
for i in range(n):
 tile=Image.frombytes('RGB',(252,448),raw[i*size:(i+1)*size]);x,y=(i%4)*252,(i//4)*448;sheet.paste(tile,(x,y));d.text((x+4,y+4),f'{i/2:.1f}s',fill='white',stroke_width=1,stroke_fill='black')
sheet.save(imgs/'contact_0.5s.jpg',quality=85)
info.update(master=str(master),audio_sha256=audio(master),protected=protected,changed_intervals={'11.56-14.60':'unchanged duration graphic over moving Earth','14.60-VO end':'unobscured 2017 totality, archive credit retained'})
info['review_frames']=[{'path':str(p),'sha256':sha(p)}for p in sorted(imgs.iterdir())]
EV.mkdir(exist_ok=False)
for name in ['cuts.json','pool.json','sfx_level.txt']:shutil.copy2(DEST/name,EV/name)
for name in ['picture_qa_stdout.txt','polish_stdout.txt','polish_gate.json']:shutil.copy2(DEST/'qa'/name,EV/name)
shutil.copy2(DEST/'qa/picture/picture_qa.json',EV/'picture_qa.json')
(EV/'DELIVERY.json').write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps(info,indent=2))
