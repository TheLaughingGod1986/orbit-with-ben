#!/usr/bin/env python3
"""Source-linked alpha comparisons; no invented chronology or measured curves.

Requires graded moving plates. R40 is the strength component only, not the
unfinished multipole geometry. R44 uses words rather than unequal bars because
'billions' gives no exact duration. Every caption animates and lasts <4s.
"""
from PIL import Image,ImageDraw
from mechanism_graphics import W,H,GOLD,WHITE,BLUE,ease
from evidence_graphics import caption,main as render
SPECS=[
 dict(row=30,mode='recap',start_s=307.12,duration_s=5.76,source_rows=[1,8,12],alpha=True,
      geometry='Three sequential factual labels; no measured time-series'),
 dict(row=40,mode='dipole_strength',start_s=409.54,duration_s=4.92,source_rows=[15],alpha=True,
      geometry='Common zero, normal 1.00 to approximate 0.10 dipole strength; not total field'),
 dict(row=44,mode='duration_comparison',start_s=452.70,duration_s=5.52,source_rows=[17],alpha=True,
      geometry='Qualitative duration comparison, no invented exact value for billions')]

def recap(d,t):
 # Sequential columns follow each phrase; all earlier words fade before 4s.
 for x,start,end,head,value in [
  (1080,0,2.08,'GLOBAL FIELD','−9% STRENGTH'),
  (1360,2.08,3.52,'RACING POLE','55 KM/YR'),
  (1640,3.52,5.76,'ATLANTIC DENT','2 LOBES')]:
  if start<=t<end:
   d.line((x-110,430,x-110+round(220*ease((t-start)/.5)),430),fill=BLUE,width=5)
   caption(d,(x,525),head,36,WHITE,t,start,end)
   caption(d,(x,620),value,40,GOLD,t,start,end)

def dipole_strength(d,t):
 x,y,width=1090,650,620
 ratio=1-.9*ease((t-2.46)/.98)
 d.line((x,y,x+width,y),fill=(110,125,145,130),width=4)
 d.rounded_rectangle((x,y-20,x+max(1,round(width*ratio)),y+20),radius=9,fill=BLUE)
 caption(d,(1400,380),'MAIN DIPOLE',54,WHITE,t,0,2.46)
 caption(d,(1400,380),'ABOUT A TENTH',54,GOLD,t,2.46,4.92)
 caption(d,(1400,790),'NORMAL = 100%',44,WHITE,t,0,2.46)
 caption(d,(1400,790),'≈ 10% NORMAL',48,GOLD,t,2.46,4.92)

def duration_comparison(d,t):
 # These are separate quantities, not bars implying an unsupported numeric ratio.
 if t<2.68:
  caption(d,(1400,440),'MARS ATMOSPHERE LOSS',46,WHITE,t,0,2.68)
  caption(d,(1400,590),'BILLIONS OF YEARS',54,GOLD,t,1,2.68)
 else:
  caption(d,(1400,440),'EARTH FIELD FLIP',46,WHITE,t,2.68,5.52)
  caption(d,(1400,590),'A FEW THOUSAND YEARS',48,GOLD,t,4.2,5.52)
 start=0 if t<2.68 else 2.68
 d.line((1080,720,1080+round(640*ease((t-start)/.5)),720),fill=BLUE,width=5)

def frame(s,t):
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 globals()[s['mode']](d,t)
 a=max(0,min(1,t/.4,(s['duration_s']-t)/.4))
 im.putalpha(im.getchannel('A').point(lambda v:round(v*a)))
 return im

def main(argv=None):return render(argv,specs=SPECS,render_frame=frame)
if __name__=='__main__':main()
