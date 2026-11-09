#!/usr/bin/env python3
"""J2141 revised R7/R8 alpha schematics; moving basalt plates required. £0.

Red tips denote the north-seeking ends. In the recorded reversed field they
point screen-south, compared with a modern desk compass pointing screen-north.
Geometry is illustrative, not a measurement of a particular rock sample.
"""
import math
from PIL import Image, ImageDraw
from mechanism_graphics import W,H,GOLD,WHITE,BLUE,RED,ease,needle
from evidence_graphics import caption,main as render
SPECS=[
 dict(row=7,mode='grains_south',version='v04',start_s=54.2,duration_s=5.72,
      source_rows=[3],alpha=True,cue='As lava or brick cools'),
 dict(row=8,mode='grains_comparison',version='v04',start_s=73.28,duration_s=5.96,
      source_rows=[3],alpha=True,cue='Instead')]

def grain_angle(i,t):
    # Lock starts with the spoken "lock" at 58.88; red tips end downward.
    p=ease((t-4.68)/.72)
    return math.pi+(math.sin(i*2.7)*2.6+.12*math.sin(t*9+i))*(1-p)

def frame(s,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    if s['mode']=='grains_south':
        # Sparse crystal outlines overlay the real rock instead of a flat slab.
        for i in range(15):
            x=1000+(i%5)*155;y=340+(i//5)*180
            d.ellipse((x-53,y-53,x+53,y+53),outline=BLUE,width=3)
            needle(d,x,y,grain_angle(i,t),42,8)
        caption(d,(1330,155),'IRON OXIDE',56,GOLD,t,2.96,5.72)
        caption(d,(1330,960),'LOCK INTO LINE',54,WHITE,t,4.68,5.72)
    else:
        # Left: modern compass red tip north. Right: recorded grains south.
        p=ease(t/.8)
        cx,cy,r=570,550,205
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=GOLD,width=8)
        for a in range(0,360,30):
            q=math.radians(a)
            d.line((cx+(r-18)*math.sin(q),cy-(r-18)*math.cos(q),
                    cx+r*math.sin(q),cy-r*math.cos(q)),fill=GOLD,width=4)
        needle(d,cx,cy,0,150,25)
        for i in range(9):
            x=1140+(i%3)*160;y=370+(i//3)*170
            d.ellipse((x-51,y-51,x+51,y+51),outline=BLUE,width=3)
            needle(d,x,y,math.pi+.2*math.sin(i*2.7)*(1-p),42,8)
        # Labels are exact spoken words and fade; none holds four seconds.
        caption(d,(570,220),'COMPASS',56,WHITE,t,0,3.6)
        caption(d,(570,850),'NORTH',52,RED,t,0,3.6)
        caption(d,(1300,220),'LAVA',56,GOLD,t,1.08,4.7)
        # The spoken 'opposite way' leaves 0.76 s: show the direction,
        # rather than add an unreadably short end caption.
    a=max(0,min(1,t/.4,(s['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda v:round(v*a)))
    return im

def main(argv=None):return render(argv,specs=SPECS,render_frame=frame)
if __name__=='__main__':main()
