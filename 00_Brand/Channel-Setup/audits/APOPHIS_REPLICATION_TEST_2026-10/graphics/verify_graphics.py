#!/usr/bin/env python3
"""Check delivery alpha/band/frame counts and build a diagnostic still reel for picture_qa.
The neutral navy is a QA display background, NOT an assembly plate or film approval.
"""
import argparse,hashlib,json,subprocess,itertools,sys
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np

def check_label_clearance(im,name,q):
 # Inspect actual stroked alpha pixels, not font metrics or intended baselines.
 if name not in ('ar1_size','ar2_station'): return None
 mask=np.asarray(im.getchannel('A'))>0
 cut=850 if name=='ar1_size' else 880
 rows=np.flatnonzero(mask[:cut].any(axis=1))
 if not len(rows): return None  # Fully transparent fade endpoint.
 runs=np.split(rows,np.flatnonzero(np.diff(rows)>1)+1)
 expected=(1 if q<.48 else 2) if name=='ar1_size' else (2 if mask[750:cut].any() else 1)
 assert len(runs)==expected,(name,q,'merged or missing label lines',len(runs),expected)
 gaps=[int(b[0]-a[-1]-1) for a,b in zip(runs,runs[1:])]
 assert all(g>=8 for g in gaps),(name,q,'stroked line gap <8px',gaps)
 art=np.flatnonzero(mask[cut:].any(axis=1))+cut
 clearance=int(art[0]-rows[-1]-1) if len(art) else None
 assert clearance is None or clearance>=12,(name,q,'art clearance <12px',clearance)
 for run in runs:
  cols=np.flatnonzero(mask[run].any(axis=0))
  assert cols[-1]-cols[0]+1<=980,(name,q,'stroked line width >980px')
 return {'line_gaps_px':gaps,'art_clearance_px':clearance}

p=argparse.ArgumentParser();p.add_argument('media',type=Path);p.add_argument('--qa-script',type=Path,required=True);a=p.parse_args()
from render_graphics import map_base
map_image,project=map_base((-48,45,12,55),'Morocco')
map_pixels=np.asarray(map_image)
tint=(map_pixels[:,:,:3]==[166,173,104]).all(axis=2)
assert not tint[int(project(0,27.67)[1]):].any(),'Morocco tint extends into Western Sahara'
assert tint.any(),'Morocco highlight missing'
m=json.loads((a.media/'manifest.json').read_text());out=a.media/'qa';out.mkdir(exist_ok=True)
checks=[];cuts=[];all_hashes={};sheet=Image.new('RGB',(1080,len(m['items'])*220),(30,45,65));draw=ImageDraw.Draw(sheet)
for i,item in enumerate(m['items']):
 folder=Path(item['sequence']).parent;frames=sorted(folder.glob('frame_*.png'))
 assert len(frames)==item['frames'],(item['name'],len(frames))
 hashes=[];layouts=[]
 for f in frames:
  im=Image.open(f);assert im.mode=='RGBA' and im.size==(1080,1920)
  box=im.getchannel('A').getbbox();assert box is None or (box[1]>=656 and box[3]<=1264),(f,box)
  if item['name']=='ar1_odds' and 0<int(f.stem.split('_')[-1])<item['frames']-1:
   assert im.crop((0,835,1080,910)).getchannel('A').getbbox(), (f,'first odds line disappeared')
  layout=check_label_clearance(im,item['name'],int(f.stem.split('_')[-1])/item['fps']/item['duration'])
  if layout: layouts.append(layout)
  hashes.append(hashlib.sha256(f.read_bytes()).hexdigest())
  all_hashes[str(f.relative_to(a.media))]=hashes[-1]
 assert len(set(hashes))>1,(item['name'],'no animation')
 assert max(sum(1 for _ in g) for _,g in itertools.groupby(hashes))<=4*item['fps'],(item['name'],'static hold exceeds 4 seconds')
 checks.append({'name':item['name'],'frames':len(frames),'unique_frames':len(set(hashes)),'sequence_sha256':hashlib.sha256(''.join(hashes).encode()).hexdigest(),'all_rgba_1080x1920_in_centre_band':True,'label_clearance_checks':layouts})
 for j,sample in enumerate(item['previews']):
  im=Image.open(sample['path']).crop((0,656,1080,1264));bg=Image.new('RGBA',im.size,(45,64,87,255));bg.alpha_composite(im)
  number=i*3+j;bg.convert('RGB').save(out/f'still_{number:03}.png')
  cuts.append({'row':f"{item['name']}_sample{j}",'source':sample['path'],'timeline_in':number,'timeline_out':number+1,'upscale':1.0,'framing':{}})
  thumb=bg.convert('RGB').resize((360,203));sheet.paste(thumb,(j*360,i*220+17));draw.text((j*360+5,i*220),f"{item['name']} / {j}",fill='white')
(out/'SHA256SUMS.txt').write_text(''.join(v+'  '+k+'\n' for k,v in all_hashes.items()))
(out/'delivery_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n');sheet.save(out/'all_stills.jpg')
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(out/'still_%03d.png'),'-c:v','libx264','-r','30','-pix_fmt','yuv420p',str(out/'still_review.mp4')],check=True)
r=subprocess.run([sys.executable,str(a.qa_script),str(out/'still_review.mp4'),'--cuts',str(out/'cuts.json'),'--out-dir',str(out/'picture'),'--no-jitter'],capture_output=True,text=True)
(out/'picture_qa_stdout.txt').write_text(r.stdout+r.stderr);print(r.stdout);print('picture_qa exit',r.returncode)
print('Delivery geometry/alpha/count checks succeeded:',len(checks),'sequences')

raise SystemExit(r.returncode)
