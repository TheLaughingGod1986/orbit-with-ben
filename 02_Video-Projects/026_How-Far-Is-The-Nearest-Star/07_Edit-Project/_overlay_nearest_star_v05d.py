#!/usr/bin/env python3
"""J0148 Chief correction: sourced Bessel WHO card over unchanged v05c/audio."""
from pathlib import Path
import json, subprocess as sp, hashlib
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
PACK=HERE/'rough_v05d_pack'
SRC=Path('/private/tmp/026_NearestStar_v05c_PHONE.mp4')
OUT=Path('/private/tmp/026_NearestStar_v05d_PHONE.mp4')
START,END=185.28,188.88
NAME='code_graphic_026_row14_bessel_who_v05d.png'
# Lower right clear area, beside the existing lower-left 1838 date.
X,Y=790,840
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
img=Image.new('RGBA',(1040,180));d=ImageDraw.Draw(img)
d.rounded_rectangle((0,0,1039,179),radius=24,fill=(23,36,55,220))
d.text((30,13),'Friedrich Bessel',font=ImageFont.truetype(FONT,72),fill='white')
d.text((30,99),'1784–1846 · Astronomer',font=ImageFont.truetype(FONT,56),fill='white')
img.save(PACK/NAME)
meta=dict(file=NAME,row='14',start=START,end=END,x=X,y=Y,size=[1040,180],text='Friedrich Bessel / 1784–1846 · Astronomer',source='SOURCES.md: J0148 Bessel card source rows',fade_in=0.35,fade_out=0.3,rise=22)
cuts=json.loads((PACK/'cuts_v05c.json').read_text())
for c in cuts:
 if c['timeline_in']<END and c['timeline_out']>START:c.setdefault('overlays',[]).append(NAME)
(PACK/'cuts_v05d.json').write_text(json.dumps(cuts,indent=2)+'\n')
ov=json.loads((PACK/'overlays_v05c.json').read_text());ov['labels'].append(meta)
(PACK/'overlays_v05d.json').write_text(json.dumps(ov,indent=2)+'\n')
fc=(f'[1:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={END-START-0.3:.3f}:d=0.3:alpha=1,setpts=PTS-STARTPTS+{START}/TB[card];'
 f"[0:v][card]overlay=x={X}:y='{Y}+22*max(0\\,1-(t-{START})/0.35)':eval=frame:eof_action=pass,format=yuv420p[v]")
sp.run(['ffmpeg','-y','-v','error','-i',str(SRC),'-loop','1','-framerate','30','-t',str(END-START),'-i',str(PACK/NAME),'-filter_complex',fc,'-map','[v]','-map','0:a','-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','copy','-movflags','+faststart',str(OUT)],check=True)
for t in (185.5,186.2,187.5,188.7):
 sp.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(OUT),'-frames:v','1',str(PACK/f'bessel_{t}.jpg')],check=True)
def audio(p):return sp.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a','-c','copy','-f','md5','-'],text=True).strip()
a,b=audio(SRC),audio(OUT)
(PACK/'audio_v05d.json').write_text(json.dumps(dict(v05c=a,v05d=b,identical=a==b),indent=2)+'\n')
assert a==b
h=hashlib.file_digest(OUT.open('rb'),'sha256').hexdigest()
(PACK/'SHA256.txt').write_text(f'{h}  {OUT}\n')
print('Rendered',OUT,flush=True)
