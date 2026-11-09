#!/usr/bin/env python3
"""R52 generation scale: existing SOURCES row 18 arithmetic, no new claim.

Two bars share zero and scale. Units are 25-year generations, not individual
reversal events. Transparent component requires a graded moving real plate.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W,H,BLUE,GOLD,WHITE,ease
from evidence_graphics import caption,main as render
SPECS=[dict(row=52,mode='generations',start_s=534.68,duration_s=3.24,
           source_rows=[18],alpha=True,
           geometry='Common-zero bars: 40 and 400 generations; 25 years per generation; 1000 and 10000 years. Existing source-row arithmetic, not measured reversal chronology.')]

def frame(s,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    x,width=1060,620
    for y,n,c in [(480,40,BLUE),(730,400,GOLD)]:
        p=ease((t-(0 if n==40 else .84))/.72)
        d.line((x,y+55,x+width,y+55),fill=(140,160,180,110),width=3)
        if p>0:
            d.rounded_rectangle((x,y-15,x+max(1,round(width*n/400*p)),y+15),radius=7,fill=c)
        caption(d,(1370,y-90),f'{n} GENERATIONS',48,c,t,0 if n==40 else .84,3.24)
    caption(d,(1370,890),'25 YEARS EACH',40,WHITE,t,.1,3.24)
    a=max(0,min(1,t/.4,(s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v:round(v*a)))
    return im

def main(argv=None):return render(argv,specs=SPECS,render_frame=frame)
if __name__=='__main__':main()
