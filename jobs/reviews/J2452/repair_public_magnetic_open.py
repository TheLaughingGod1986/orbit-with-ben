#!/usr/bin/env python3
"""Reframe only the opening field-line shot to remove a detected left gutter."""
import json
from pathlib import Path
import build_public_magnetic as b
SRC=b.OUT
OUT=SRC.with_name('public_magnetic_v05')
def main():
 OUT.mkdir(exist_ok=False)
 build=json.loads((SRC/'BUILD.json').read_text())
 from PIL import Image,ImageDraw,ImageFont
 credit=Image.new('RGBA',(1920,1080));ImageDraw.Draw(credit).text((30,1030),'NASA',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24),fill=(235,235,235,255));credit.save(OUT/'credit.png')
 # Only the opening field-line shot is cropped; title is laid after reframing.
 graph="[0:v]trim=end=4.6,setpts=PTS-STARTPTS,crop=1760:990:160:45,scale=1920:1080,setsar=1,fps=30[a];[0:v]trim=start=4.6:end=26.9,setpts=PTS-STARTPTS,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[base];[1:v]format=rgba,fade=t=in:st=0:d=1.5:alpha=1,fade=t=out:st=4.5:d=1.5:alpha=1[t];[base][t]overlay=0:0:enable=lt(t\\,6)[titled];[titled][2:v]overlay=0:0:enable=lt(t\\,4.6),format=yuv420p[v]"
 first=OUT/'interior_00.mp4'
 b.run(['-i',str(b.MASTER),'-loop','1','-i',str(SRC/'title.png'),'-loop','1','-i',str(OUT/'credit.png'),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v','807',*b.enc(),str(first)])
 listing=(SRC/'concat.txt').read_text().replace(str(SRC/'interior_00.mp4'),str(first));(OUT/'concat.txt').write_text(listing)
 video=OUT/'031_magnetic_undarkened_v05.mp4'
 b.run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(b.NARR),'-map','0:v','-map','1:a','-af','volume=-0.5dB','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(build['duration_s']),str(video)])
 for name in ['full_pixel_cuts.json','changed_cuts.json','source_cuts.json']:(OUT/name).write_bytes((SRC/name).read_bytes())
 build.update(output=str(video),sha256=b.sha(video),repair='Opening 0–4.6s cropped 1760x990 at x160 y45, scaled to 1920x1080 (1.091x); title laid after reframe. NASA source credit restored after crop. Removes the detected left gutter; all narration and later picture unchanged. Requires fresh gates.')
 (OUT/'BUILD.json').write_text(json.dumps(build,indent=2)+'\n')
if __name__=='__main__':main()
