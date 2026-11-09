#!/usr/bin/env python3
"""032 remaining process overlays: draft stills, never approval or stock footage.

Independent row renders; 1920x1080 RGBA, 3.6 seconds, 30fps. Use only over a
reviewed moving plate. Preview backdrops are illustrative and never exported.
No renders without an explicit list of reviewed ids and a review reference.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font
from mechanism_graphics import arrow, label, BLUE, DIM

SPECS = [
    dict(id='r21_cycle_clouds', row=21, kind='clouds', source_rows=[8],
         labels=['EARTH', 'WATER', 'TITAN', 'METHANE + ETHANE']),
    dict(id='r21_cycle_lakes', row=21, kind='rivers', source_rows=[8],
         labels=['RAIN', 'RIVER CHANNELS', 'LAKES']),
    dict(id='r25_heated_suit', row=25, kind='suit', source_rows=[1,8,9],
         labels=['HEATED SUIT']),
    dict(id='r29_rain_comparison', row=29, kind='rain', source_rows=[10],
         labels=['BIGGEST DROPS', 'EARTH', 'TITAN', '≈ FALLING SNOWFLAKES']),
    dict(id='r39_fire_partners', row=39, kind='partners', source_rows=[9,14],
         labels=['FUEL', 'OXYGEN', 'FIRE']),
    dict(id='r40_fire_missing', row=40, kind='missing', source_rows=[9,14],
         labels=['FUEL', 'ALMOST NO OXYGEN', 'NO FIRE']),
    dict(id='r45_lift_mechanism', row=45, kind='lift', source_rows=[15],
         labels=['LIFT', 'AIR', 'WEIGHT', 'GRAVITY']),
]


def text(d, xy, s, size=54, colour=WHITE):
    label(d, xy, s, size, colour)


def cloud(d, x, y):
    for dx,dy,r in [(0,0,55),(65,-20,70),(135,0,55)]:
        d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=DIM)


def frame(s, t=1.8):
    im = Image.new('RGBA', (W,H))
    d = ImageDraw.Draw(im)
    p = min(1,max(0,t/1.6))
    lines=s['labels'];k=s['kind']
    if k=='clouds':
        for i,(body,liquid) in enumerate([(lines[0],lines[1]),(lines[2],lines[3])]):
            x=200+i*850
            text(d,(x,160),body,64,GOLD)
            cloud(d,x+160,390)
            text(d,(x,760),liquid,48)
            d.line((x,700,x+560,700),fill=BLUE,width=8)
            for n in range(5):
                xx=x+100+n*75;yy=470+(t*90+n*33)%180
                d.line((xx,yy,xx-6,yy+22),fill=BLUE,width=5)
            arrow(d,(x+460,660),(x+460,660-200*p),GOLD)
        # Symbols only: not a terrain map or a claim about comparative rain rate.
    elif k=='rivers':
        cloud(d,300,300)
        text(d,(180,150),lines[0],60,GOLD)
        for n in range(6):
            xx=240+n*52;yy=380+(t*85+n*19)%170
            d.line((xx,yy,xx-4,yy+20),fill=BLUE,width=5)
        points=[(250,580),(450,650),(650,590),(900,700),(1100,650),(1250,720)]
        d.line(points,fill=BLUE,width=12)
        d.line([(450,510),(650,590)],fill=BLUE,width=8)
        d.line([(780,480),(900,700)],fill=BLUE,width=8)
        d.ellipse((1200,650,1600,870),outline=WHITE,width=5)
        d.ellipse((1210,660,1210+380*p,860),fill=BLUE)
        text(d,(560,800),lines[1],48)
        text(d,(1320,570),lines[2],52,GOLD)
        # A moving marker shows drainage, rather than Ken-Burning the overlay.
        at=(t/3.6)*5
        segment=min(4,int(at));fraction=at-segment
        x=points[segment][0]+(points[segment+1][0]-points[segment][0])*fraction
        y=points[segment][1]+(points[segment+1][1]-points[segment][1])*fraction
        d.ellipse((x-8,y-8,x+8,y+8),fill=GOLD)
    elif k=='suit':
        # Human outline is symbolic; no astronaut photograph or invented Orbit.
        d.ellipse((510,220,650,360),outline=WHITE,width=6)
        d.rounded_rectangle((460,370,700,700),radius=55,outline=WHITE,width=6)
        d.line((490,700,460,900),fill=WHITE,width=15)
        d.line((670,700,700,900),fill=WHITE,width=15)
        d.line((460,410,340,640),fill=WHITE,width=15)
        d.line((700,410,800,640),fill=WHITE,width=15)
        for i in range(4):
            yy=440+i*55
            xx=485+20*math.sin(t*3+i)
            d.line((xx,yy,xx+160,yy),fill=GOLD,width=8)
        text(d,(1000,400),lines[0],64,GOLD)
        arrow(d,(960,465),(730,520),GOLD)
    elif k=='rain':
        text(d,(160,150),lines[0],62,GOLD)
        for x,body,diameter,speed in [(220,'EARTH',6.5,9.2),(1040,'TITAN',9.5,1.6)]:
            text(d,(x,270),body,54)
            # Equal linear diameter scale; equal spatial/time speed scale.
            r=diameter*9
            y=420+speed*10*t
            d.ellipse((x+180-r,y-r,x+180+r,y+r),fill=BLUE,outline=WHITE,width=3)
            text(d,(x,850),f'{diameter:g} MM',54,GOLD)
            text(d,(x+340,850),f'{speed:g} M/S',54)
        text(d,(1030,950),lines[3],38)
    elif k in ('partners','missing'):
        text(d,(170,260),lines[0],70,GOLD)
        text(d,(760,260),lines[1],52,BLUE if k=='partners' else DIM)
        arrow(d,(320,380),(320+480*p,380+270*p),BLUE)
        arrow(d,(1030,380),(1030-160*p,380+270*p),BLUE)
        text(d,(840,740),lines[2],80,GOLD)
        if k=='partners':
            x,y=1120,650
            d.polygon([(x-50,y),(x-25,y-80-15*math.sin(t*4)),(x+50,y)],fill=GOLD)
        else:
            # Almost none, never a quantitative zero measurement.
            d.line((830,620,930,700),fill=DIM,width=7)
            d.line((930,620,830,700),fill=DIM,width=7)
    elif k=='lift':
        # Airfoil is an engineering symbol, never a flat planetary disc.
        cy=540-12*math.sin(t*2)
        d.polygon([(500,cy),(760,cy-55),(1150,cy+10),(760,cy+25)],fill=WHITE)
        arrow(d,(780,cy-80),(780,cy-80-190*p),BLUE)
        arrow(d,(780,cy+60),(780,cy+60+190*p),GOLD)
        text(d,(920,230),lines[0],64,BLUE)
        text(d,(1160,470),lines[1],54,BLUE)
        text(d,(920,800),lines[2],64,GOLD)
        text(d,(1160,700),lines[3],54,GOLD)
        for n in range(4):
            xx=180+(t*130+n*120)%280
            arrow(d,(xx,450+n*60),(xx+120,450+n*60),BLUE,width=3)
    else:
        raise ValueError(k)
    opacity=max(0,min(1,t/.4,(3.6-t)/.4))
    if opacity<1:im.putalpha(im.getchannel('A').point(lambda a:round(a*opacity)))
    return im


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--approved',nargs='*',default=[])
    ap.add_argument('--review-ref')
    a=ap.parse_args()
    if set(a.approved)-{s['id'] for s in SPECS}:ap.error('Unknown ids')
    if a.render and (not a.approved or not a.review_ref):
        ap.error('Render requires individually reviewed ids and review reference')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1280,360*math.ceil(len(SPECS)/2)),(40,58,79))
    clips=[];checks=[]
    for i,s in enumerate(SPECS):
        name='code_graphic_032_'+s['id']+'_v01'
        preview=out/(name+'.png');im=frame(s);im.save(preview)
        bg=Image.new('RGBA',(W,H),(40,58,79,255));bg.alpha_composite(im)
        tile=bg.convert('RGB').resize((640,360));ImageDraw.Draw(tile).text((8,8),s['id'],fill='white')
        sheet.paste(tile,((i%2)*640,(i//2)*360))
        box=im.getchannel('A').getbbox()
        c=dict(id=s['id'],alpha_bounds=box,
               entry_clear=frame(s,0).getbbox() is None,
               exit_clear=frame(s,3.6).getbbox() is None,
               inside_5_percent=bool(box and box[0]>=96 and box[1]>=54 and box[2]<=1824 and box[3]<=1026),
               changing_frames=frame(s,.8).tobytes()!=frame(s,1.5).tobytes())
        checks.append(c)
        rec=dict(**s,preview=str(preview),preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),
                 status='DRAFT_REQUIRES_INDIVIDUAL_STILL_REVIEW',rendered=False,
                 duration=3.6,needs_background='Reviewed graded moving real plate',
                 composite_status='UNVERIFIED',source='01_Script/SOURCES.md, v01 governing table')
        if a.render and s['id'] in a.approved:
            dest=out/(name+'.mov')
            proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pixel_format','rgba',
                '-video_size',f'{W}x{H}','-framerate','30','-i','pipe:0','-an','-c:v','qtrle',str(dest)],stdin=subprocess.PIPE)
            try:
                for j in range(108):proc.stdin.write(frame(s,j/30).tobytes())
                proc.stdin.close()
                if proc.wait():raise RuntimeError('Render failed')
            except BaseException:
                proc.kill();raise
            rec.update(rendered=True,render=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),review_ref=a.review_ref)
        clips.append(rec)
    sheet.save(out/'process_previews.jpg',quality=95)
    (out/'PROCESS_MANIFEST_v01.json').write_text(json.dumps(dict(job='J2089',clips=clips),indent=2)+'\n')
    (out/'PROCESS_CHECKS_v01.json').write_text(json.dumps(checks,indent=2)+'\n')
    if not all(c['entry_clear'] and c['exit_clear'] and c['inside_5_percent'] and c['changing_frames'] for c in checks):
        raise SystemExit('Structural check failed; inspect PROCESS_CHECKS_v01.json')


if __name__=='__main__':main()
