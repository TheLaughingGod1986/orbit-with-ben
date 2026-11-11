#!/usr/bin/env python3
"""Prepare a six-second clean starfield; v04 donor accidentally includes a card."""
import json,subprocess as sp
from pathlib import Path
import build_public_light as b
OUT=Path('/Users/ben/_desk/J2452-sleep-scratch/light_clean_starfield_v01')
def main():
 OUT.mkdir(exist_ok=False)
 dest=OUT/'starfield_221_224_slow_v01.mp4'
 b.run(['-ss','221','-i',str(b.MASTER),'-vf','trim=duration=3,setpts=2*(PTS-STARTPTS),fps=30,format=yuv420p','-frames:v','180',*b.enc(),str(dest)])
 cuts=[dict(row=f'clean-{i}',timeline_in=i*.5,timeline_out=(i+1)*.5,source='clean-starfield',framing=dict(offset=i*.5),src_w=1920,upscale=1) for i in range(12)]
 (OUT/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
 (OUT/'BUILD.json').write_text(json.dumps(dict(output=str(dest),sha256=b.sha(dest),master=str(b.MASTER),source_range_s=[221,224],speed=.5,frames=180,chapter_target_s=[196,202],reason='v04 donor 221-227 includes the source chapter card starting 224.44s. This donor ends before it. Requires inspection and integration into a new chapter, then fresh full gates before grading.'),indent=2)+'\n')
 for i,t in enumerate([0,2.9,5.9]):sp.run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',str(dest),'-frames:v','1',str(OUT/f'frame_{i}.jpg')],check=True)
if __name__=='__main__':main()
