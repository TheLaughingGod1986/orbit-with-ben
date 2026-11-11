#!/usr/bin/env python3
"""Render exact-time cover-edge stills for human review; never grants a gate pass."""
import argparse,json,subprocess as sp
from pathlib import Path
from PIL import Image,ImageDraw
from build_public_andromeda import OUT

def main():
 global OUT
 parser=argparse.ArgumentParser();parser.add_argument("--out",type=Path,default=OUT);OUT=parser.parse_args().out
 b=json.loads((OUT/'BUILD.json').read_text());rows=json.loads((OUT/'source_cuts.json').read_text())
 times={0,2,5,b['duration_s']-1}
 for r in rows:
  if r['label']!='public':
   for t in [r['timeline_in']-1.1,r['timeline_in']-.1,r['timeline_in']+.5,(r['timeline_in']+r['timeline_out'])/2,r['timeline_out']-.5,r['timeline_out']+.1,r['timeline_out']+1.1]:
    if 0<=t<b['duration_s']:times.add(round(t,3))
 times=sorted(times);sheet=Image.new('RGB',(1440,160*((len(times)+5)//6)));d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  p=OUT/f'edge_{i:03}.jpg';sp.run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',b['output'],'-frames:v','1','-vf','scale=240:135',str(p)],check=True,timeout=20)
  sheet.paste(Image.open(p),((i%6)*240,(i//6)*160));d.text(((i%6)*240,(i//6)*160+137),f'{t:.3f}s',fill='white')
 sheet.save(OUT/'COVER_EDGES.jpg');(OUT/'COVER_EDGE_TIMES.json').write_text(json.dumps(times,indent=2)+'\n')
if __name__=='__main__':main()
