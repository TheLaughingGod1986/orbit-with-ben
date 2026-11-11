#!/usr/bin/env python3
"""Retain dense still evidence at the title-cover fade edges; no playback claim."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--out',type=Path,required=True)
 out=parser.parse_args().out
 build=json.loads((out/'BUILD.json').read_text())
 times=[195.9,196,196.2,196.4,197,198,199,199.5,200,200.5,201,201.5,201.8,202,202.2,202.4,202.6,202.8]
 sheet=Image.new('RGB',(1280,((len(times)+3)//4)*205));draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  frame=out/f'patch_edge_{i:02}.jpg'
  subprocess.run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',build['output'],'-frames:v','1','-vf','scale=320:180',str(frame)],check=True,timeout=30)
  sheet.paste(Image.open(frame),((i%4)*320,(i//4)*205))
  draw.text(((i%4)*320,(i//4)*205+183),str(t),fill='white')
 sheet.save(out/'PATCH_EDGE_REVIEW.jpg')
 (out/'PATCH_EDGE_TIMES.json').write_text(json.dumps(times,indent=2)+'\n')
if __name__=='__main__':main()
