#!/usr/bin/env python3
"""Check delivery alpha/band/frame counts and build a diagnostic still reel for picture_qa.
The neutral navy is a QA display background, NOT an assembly plate or film approval.
"""
import argparse,hashlib,json,subprocess,itertools
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('media',type=Path);p.add_argument('--qa-script',type=Path,required=True);a=p.parse_args()
m=json.loads((a.media/'manifest.json').read_text());out=a.media/'qa';out.mkdir(exist_ok=True)
checks=[];cuts=[];all_hashes={};sheet=Image.new('RGB',(1080,len(m['items'])*220),(30,45,65));draw=ImageDraw.Draw(sheet)
for i,item in enumerate(m['items']):
 folder=Path(item['sequence']).parent;frames=sorted(folder.glob('frame_*.png'))
 assert len(frames)==item['frames'],(item['name'],len(frames))
 hashes=[]
 for f in frames:
  im=Image.open(f);assert im.mode=='RGBA' and im.size==(1080,1920)
  box=im.getchannel('A').getbbox();assert box is None or (box[1]>=656 and box[3]<=1264),(f,box)
  hashes.append(hashlib.sha256(f.read_bytes()).hexdigest())
  all_hashes[str(f.relative_to(a.media))]=hashes[-1]
 assert len(set(hashes))>1,(item['name'],'no animation')
 assert max(sum(1 for _ in g) for _,g in itertools.groupby(hashes))<=4*item['fps'],(item['name'],'static hold exceeds 4 seconds')
 checks.append({'name':item['name'],'frames':len(frames),'unique_frames':len(set(hashes)),'sequence_sha256':hashlib.sha256(''.join(hashes).encode()).hexdigest(),'all_rgba_1080x1920_in_centre_band':True})
 for j,sample in enumerate(item['previews']):
  im=Image.open(sample['path']).crop((0,656,1080,1264));bg=Image.new('RGBA',im.size,(45,64,87,255));bg.alpha_composite(im)
  number=i*3+j;bg.convert('RGB').save(out/f'still_{number:03}.png')
  cuts.append({'row':f"{item['name']}_sample{j}",'source':sample['path'],'timeline_in':number,'timeline_out':number+1,'upscale':1.0,'framing':{}})
  thumb=bg.convert('RGB').resize((360,203));sheet.paste(thumb,(j*360,i*220+17));draw.text((j*360+5,i*220),f"{item['name']} / {j}",fill='white')
(out/'SHA256SUMS.txt').write_text(''.join(v+'  '+k+'\n' for k,v in all_hashes.items()))
(out/'delivery_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(out/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n');sheet.save(out/'all_stills.jpg')
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(out/'still_%03d.png'),'-c:v','libx264','-r','30','-pix_fmt','yuv420p',str(out/'still_review.mp4')],check=True)
r=subprocess.run(['python3',str(a.qa_script),str(out/'still_review.mp4'),'--cuts',str(out/'cuts.json'),'--out-dir',str(out/'picture'),'--no-jitter'],capture_output=True,text=True)
(out/'picture_qa_stdout.txt').write_text(r.stdout+r.stderr);print(r.stdout);print('picture_qa exit',r.returncode)
print('Delivery geometry/alpha/count checks succeeded:',len(checks),'sequences')
