#!/usr/bin/env python3
"""031 £0 schematic overlays for locked satellite/grid lines; not engineering models.

Composite over graded moving plates. Icons illustrate the spoken action only:
no claimed orbit geometry, hazard boundary, protection efficiency or hardware design.
"""
import math
from PIL import Image, ImageDraw
from mechanism_graphics import W,H,BLUE,GOLD,WHITE,ease
from evidence_graphics import caption,main as render

SPECS=[
 dict(row=28,mode='sat_safe',start_s=295.34,duration_s=4.44,source_rows=[11],alpha=True,
      cue='satellite operators often shut down anything non-essential',
      geometry='Illustrative satellite icon; non-essential panels dim, core stays lit. No orbit or SAA contour.'),
 dict(row=46,mode='grid_shield',start_s=472.22,duration_s=3.28,source_rows=[],alpha=True,
      cue='hardening satellites and power grids against solar storms',
      source_note='Locked v02a VO action, SHOT_LIST_v02 row 46; conceptual resilience icons, no quantitative claim.',
      geometry='Illustrative shield outlines build around satellite and grid icons; no engineering efficacy claim.')]

def satellite(d,cx,cy,t,dim=False):
    level=round(255-165*ease((t-1.62)/.6)) if dim else 255
    panel=BLUE+(level,)
    for side in [-1,1]:
        x=cx+side*170
        d.rectangle((x-65,cy-70,x+65,cy+70),outline=panel,width=5)
        for dy in [-35,0,35]:d.line((x-65,cy+dy,x+65,cy+dy),fill=panel,width=2)
        d.line((cx+side*65,cy,x-side*65,cy),fill=WHITE,width=5)
    d.rounded_rectangle((cx-65,cy-65,cx+65,cy+65),radius=14,outline=WHITE,width=6)
    r=10+3*math.sin(t*3)
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=GOLD)
    d.line((cx,cy-65,cx+40,cy-110),fill=WHITE,width=5)

def grid(d,cx,cy):
    d.line((cx-65,cy+100,cx,cy-100,cx+65,cy+100),fill=WHITE,width=6)
    for dy,half in [(-55,85),(0,105),(55,125)]:
        d.line((cx-half,cy+dy,cx+half,cy+dy),fill=BLUE,width=6)
    d.line((cx-50,cy+50,cx+35,cy-25,cx-25,cy-25,cx+15,cy-75),fill=WHITE,width=3)

def shield(d,cx,cy,t):
    pts=[(cx,cy-165),(cx+265,cy-105),(cx+230,cy+100),(cx,cy+190),(cx-230,cy+100),(cx-265,cy-105),(cx,cy-165)]
    n=ease(t/.8)*(len(pts)-1)
    for i in range(min(int(n)+1,len(pts)-1)):
        f=min(1,max(0,n-i));a,b=pts[i],pts[i+1]
        if f:d.line((a[0],a[1],a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f),fill=GOLD,width=6)

def frame(s,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    if s['mode']=='sat_safe':
        satellite(d,1400,570,t,True)
        caption(d,(1400,300),'SATELLITE OPERATORS',46,WHITE,t,0,1.62)
        caption(d,(1400,300),'NON-ESSENTIAL SYSTEMS',46,GOLD,t,1.62,4.44)
        caption(d,(1400,820),'POWER DOWN',52,WHITE,t,1.9,4.44)
    else:
        satellite(d,1260,510,t)
        grid(d,1260,865)
        shield(d,1260,510,t)
        shield(d,1260,865,t-1.44)
        caption(d,(1260,200),'HARDENING SATELLITES',44,GOLD,t,0,1.44)
        caption(d,(1260,200),'AND POWER GRIDS',44,GOLD,t,1.44,3.28)
    a=max(0,min(1,t/.4,(s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v:round(v*a)))
    return im

def main(argv=None):return render(argv,specs=SPECS,render_frame=frame)
if __name__=='__main__':main()
