#!/usr/bin/env python3
"""Source-linked WHEN overlays. Alpha only; moving plates required. £0."""
from PIL import Image, ImageDraw
from mechanism_graphics import W,H,GOLD,WHITE,BLUE,ease
from evidence_graphics import caption,main as render
SPECS=[
 dict(row=19,mode='era83m',start_s=197.0,duration_s=3.6,source_rows=[7],alpha=True,labels=['83 MILLION YEARS']),
 dict(row=24,mode='swarm2013',start_s=234.58,duration_s=3.6,source_rows=[9],alpha=True,labels=['2013','3 SPACECRAFT']),
 dict(row=33,mode='laschamp',start_s=341.38,duration_s=3.6,source_rows=[14],alpha=True,labels=['41,000 YEARS AGO','LASCHAMP EVENT'])]
def frame(s,t):
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 # Upper-right placement leaves the existing WHO/FACT lower thirds clear.
 # Line is an entrance accent, not a quantitative time axis.
 p=ease(t/.5);x=1400;y=200
 d.line((1080,y,1080+round(640*p),y),fill=BLUE,width=5)
 for i,txt in enumerate(s['labels']):
  caption(d,(x,280+i*95),txt,54 if i==0 else 44,GOLD if i==0 else WHITE,t,.12+i*.35,3.6)
 a=max(0,min(1,t/.4,(3.6-t)/.4));im.putalpha(im.getchannel('A').point(lambda v:round(v*a)))
 return im
def main(argv=None):return render(argv,specs=SPECS,render_frame=frame)
if __name__=='__main__':main()
