#!/usr/bin/env python3
"""Create labelled master contact sheets for cover review, never a QA PASS."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image, ImageDraw
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--film');p.add_argument('--skip-film',default='');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
inputs=json.loads(Path('jobs/reviews/J2452/alignment_v02/inputs_v01.json').read_text());reports=[]
for c in inputs:
    if a.film and c['film']!=a.film:continue
    if c['film'] in a.skip_film.split(','):continue
    frames=a.out/c['film'];frames.mkdir();out=a.out/f"{c['film']}_master_every_5s.jpg"
    # Do not put tile inside ffmpeg: a source format change flushes a partial tile.
    # Emit samples first; frame_pts filenames retain the five-second timeline slots.
    r=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-loglevel','error','-n','-i',c['master'],'-vf','fps=1/5,scale=320:180','-fps_mode','vfr','-frame_pts','1',str(frames/'%04d.jpg')],capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr[-2000:])
    files=sorted(frames.glob('*.jpg'));assert files
    maxslot=max(int(f.stem) for f in files);img=Image.new('RGB',(2560,180*((maxslot//8)+1)))
    for f in files:
        n=int(f.stem);x=n%8*320;y=n//8*180;img.paste(Image.open(f),(x,y));draw=ImageDraw.Draw(img);sec=n*5
        draw.rectangle((x,y,x+115,y+19),fill='black');draw.text((x+3,y+2),f"slot {sec//60}:{sec%60:02d}-{(sec+5)//60}:{(sec+5)%60:02d}",fill='white')
    img.save(out,quality=92)
    reports.append(dict(film=c['film'],master=c['master'],sheet=str(out),samples=len(files),first_slot=int(files[0].stem),last_slot=maxslot,sampling='Five-second fps slots, nominal labels; inspect exact frames before replacement boundaries',status='REVIEW_AID_ONLY_NOT_EVERY_FRAME_QA'))
    print(c['film'],flush=True)
(a.out/'INDEX.json').write_text(json.dumps(reports,indent=2)+'\n')
