#!/usr/bin/env python3
"""Sample cover centres and edges, retaining a local visual review sheet."""
import json,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path('/Users/ben/_desk/J2452-sleep-scratch/public_light_v04'));OUT=parser.parse_args().out
b=json.loads((OUT/'BUILD.json').read_text());changes=json.loads((OUT/'changed_cuts.json').read_text())
times=sorted(set(round(max(0,min(b['duration_s']-.1,t)),3) for c in changes for t in [c['timeline_in'],(c['timeline_in']+c['timeline_out'])/2,c['timeline_out']]))
sheet=Image.new('RGB',(1280,((len(times)+3)//4)*205));d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 f=OUT/f'review_{i:03}.jpg';sp.run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',b['output'],'-frames:v','1','-vf','scale=320:180',str(f)],check=True)
 sheet.paste(Image.open(f),((i%4)*320,(i//4)*205));d.text(((i%4)*320,(i//4)*205+182),str(t),fill='white')
sheet.save(OUT/'EDIT_REVIEW.jpg',quality=90)
(OUT/'EDIT_REVIEW_TIMES.json').write_text(json.dumps(times,indent=2)+'\n')
