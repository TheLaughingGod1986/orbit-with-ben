#!/usr/bin/env python3
"""032 mechanism batch: reviewable alpha previews; no film background or approval.

Every row is independently named. Frames use a 0.4 s entry/exit and animate
throughout the 3.6 s window. Render only after an individual review decision.
These symbolic process diagrams contain no substitute celestial-body discs.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from code_graphics import W, H, GOLD, WHITE, font

BLUE = (102, 205, 245, 255)
DIM = (198, 215, 232, 255)
SPECS = [
    dict(id='r02_survive_check', row=2, kind='checks', labels=["WON'T EXPLODE", "BLOOD WON'T BOIL"], source_rows=[1]),
    dict(id='r05_rain_preview', row=5, kind='drop', labels=['METHANE RAIN'], source_rows=[8]),
    dict(id='r10_spectrum', row=10, kind='spectrum', labels=['LIGHT', 'METHANE'], source_rows=[4]),
    dict(id='r13_photolysis', row=13, kind='split', labels=['SUNLIGHT', 'NITROGEN + METHANE', 'HAZE'], source_rows=[5]),
    dict(id='r14_methane', row=14, kind='reservoir', labels=['METHANE', 'SUNLIGHT', '?'], source_rows=[6]),
    dict(id='r16_descent_147m', row=16, kind='counter', labels=['DESCENT', '147 MIN', '2 H 27 M'], value=147, source_rows=[7]),
    dict(id='r22_surface_72m', row=22, kind='counter', labels=['FROM THE SURFACE', '72 MIN'], value=72, source_rows=[7]),
    dict(id='r27_no_oxygen', row=27, kind='absence', labels=['ALMOST NO OXYGEN'], source_rows=[9]),
    dict(id='r30_dunes_label', row=30, kind='card', labels=['CENTURIES BETWEEN SHOWERS'], source_rows=[10]),
    dict(id='r32_scalemap', row=32, kind='area', labels=['KRAKEN MARE', '400,000 KM²', '≈ 5× LAKE SUPERIOR'], source_rows=[11]),
    dict(id='r37_spark_question', row=37, kind='question', labels=['WOULD IT EXPLODE?', '?'], source_rows=[14]),
    dict(id='r38_reserves', row=38, kind='qualitative', labels=['TITAN', 'HUNDREDS OF TIMES', 'EARTH OIL + GAS'], source_rows=[14]),
    dict(id='r41_no_flame', row=41, kind='extinguish', labels=['NO OXYGEN TO BURN'], source_rows=[14]),
    dict(id='r42_flipfire_earth', row=42, kind='combustion', labels=['EARTH', 'FUEL TANK', 'OXYGEN IN AIR'], source_rows=[14]),
    dict(id='r43_flipfire_titan', row=43, kind='combustion', labels=['TITAN', 'OXYGEN TANK', 'METHANE SKY'], source_rows=[14]),
    dict(id='r48_eight_rotors', row=48, kind='rotors', labels=['DRAGONFLY', '8 ROTORS', 'NUCLEAR-POWERED'], source_rows=[16]),
    dict(id='r50_selk_soup', row=50, kind='ingredients', labels=['WATER', 'ORGANICS', 'PRIMORDIAL SOUP'], source_rows=[16]),
]


def label(d, xy, text, size=60, colour=WHITE):
    d.text(xy, text, font=font(size), fill=colour, stroke_width=3,
           stroke_fill=(20, 28, 42, 255))


def arrow(d, start, end, colour=BLUE, width=7):
    d.line((*start, *end), fill=colour, width=width)
    angle = math.atan2(end[1]-start[1], end[0]-start[0])
    points = [end] + [(end[0]-24*math.cos(angle+a), end[1]-24*math.sin(angle+a))
                      for a in [-.5, .5]]
    d.polygon(points, fill=colour)


def frame(s, t=1.8):
    im = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(im)
    p = max(0, min(1, t/1.6))
    pulse = math.sin(t*3)*8
    kind, lines = s['kind'], s['labels']
    if kind not in ('checks', 'ingredients'):
        label(d, (160, 180), lines[0], colour=GOLD)
    if kind == 'checks':
        for i, line in enumerate(lines):
            y = 420+i*170
            label(d, (280, y), line, 68)
            if t > .5+i*.7:
                d.line((170, y+35, 200, y+65, 250, y), fill=BLUE, width=10)
    elif kind == 'drop':
        y = 390+(t*120)%280
        d.ellipse((660, y, 800, y+140), fill=BLUE)
        d.polygon([(660,y+70),(730,y-90),(800,y+70)], fill=BLUE)
    elif kind == 'spectrum':
        arrow(d, (200, 510), (610, 510))
        d.polygon([(620,360),(620,660),(830,510)], outline=WHITE, width=5)
        for i, col in enumerate([BLUE, WHITE, GOLD]):
            arrow(d, (840,510), (840+390*p,510+(-120+i*120)*p), col)
        d.line((1120,510,1120,640), fill=(25,40,60,255), width=18)
        label(d, (900,740), lines[1], colour=GOLD)
    elif kind == 'split':
        label(d, (190,440), lines[1], 54)
        arrow(d, (780,480), (1120,480))
        label(d, (1200,440), lines[2], colour=GOLD)
        for i in range(14):
            x=1200+(i*37)%260 + pulse
            y=580+(i*43)%210
            d.ellipse((x,y,x+9,y+9), fill=BLUE)
    elif kind == 'reservoir':
        d.rounded_rectangle((220,360,590,850), radius=25, outline=WHITE, width=6)
        level=430+100*(t/3.6)
        d.rectangle((230,level,580,840), fill=BLUE)
        arrow(d,(410,level),(410,300),GOLD)
        label(d,(700,390),lines[1],54)
        arrow(d,(730,800),(600,800))
        label(d,(830,740),'?',90,GOLD)
    elif kind == 'counter':
        value=round(s['value']*p)
        label(d,(200,440),f'{value} MIN',110,BLUE)
        d.line((200,650,200+1120*p,650),fill=GOLD,width=16)
        if len(lines)>2: label(d,(200,750),lines[2],64)
    elif kind == 'absence':
        # Deliberately no numeric zero: the source says almost none.
        d.rounded_rectangle((200,440,1320,550),radius=15,outline=WHITE,width=5)
        d.rectangle((210,450,220+pulse/3,540),fill=BLUE)
        label(d,(200,650),'ALMOST NONE',76,BLUE)
    elif kind == 'card':
        d.line((160,340,160+1160*p,340),fill=BLUE,width=7)
    elif kind == 'area':
        # One rectangle represents total area, not a fabricated geographic map.
        d.rectangle((210,390,1110,750),outline=WHITE,width=5)
        d.rectangle((216,396,216+888*p,744),fill=BLUE)
        for n in range(1,5):d.line((210+180*n,390,210+180*n,750),fill=WHITE,width=3)
        label(d,(240,450),lines[1],80,(20,28,42,255))
        label(d,(210,810),lines[2],58,GOLD)
    elif kind == 'question':
        label(d,(800,390+pulse),lines[1],220,BLUE)
    elif kind == 'qualitative':
        # Not a quantitative bar: no invented exact reserve ratio or baseline.
        d.line((200,500,200+1100*p,500),fill=BLUE,width=7)
        label(d,(200,680),lines[1],76,GOLD)
        label(d,(200,820),lines[2],48)
    elif kind == 'extinguish':
        d.line((600,800,600,550),fill=DIM,width=20)
        r=max(0,70*(1-t/2.3))
        if r>0:d.ellipse((600-r,520-r,600+r,520+r),fill=GOLD)
        arrow(d,(850,600),(1100,600),BLUE)
        label(d,(1150,560),'NO OXYGEN',48)
    elif kind == 'combustion':
        d.rounded_rectangle((220,400,550,760),radius=35,outline=WHITE,width=5)
        label(d,(200,820),lines[1],54)
        arrow(d,(550,580),(550+390*p,580),BLUE)
        label(d,(1000,430),lines[2],54)
        # Small nozzle flame, never an explosion or an oxygen-only flame.
        x=950+30*p
        d.polygon([(940,550),(x+120+pulse,580),(940,610)],fill=GOLD)
    elif kind == 'rotors':
        # Symbolic top view: eight rotors on four paired arms, not mission footage.
        cx,cy=800,590
        d.rounded_rectangle((720,520,880,660),radius=20,outline=WHITE,width=5)
        for ax,ay in [(480,390),(1120,390),(480,790),(1120,790)]:
            d.line((cx,cy,ax,ay),fill=DIM,width=7)
            for offset in [-45,45]:
                xx=ax+offset
                d.ellipse((xx-65,ay-65,xx+65,ay+65),outline=BLUE,width=3)
                angle=t*7+offset
                dx,dy=55*math.cos(angle),55*math.sin(angle)
                d.line((xx-dx,ay-dy,xx+dx,ay+dy),fill=WHITE,width=7)
        label(d,(1320,470),lines[1],50,GOLD)
        label(d,(1320,570),lines[2],40)
    elif kind == 'ingredients':
        label(d,(160,410),lines[0],60,BLUE)
        label(d,(160,610),lines[1],60,BLUE)
        arrow(d,(650,500),(650+380*p,500),GOLD)
        label(d,(1080,470),lines[2],54,GOLD)
    else:
        raise ValueError(kind)
    opacity=max(0,min(1,t/.4,(3.6-t)/.4))
    if opacity<1: im.putalpha(im.getchannel('A').point(lambda a:round(a*opacity)))
    return im


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--approved',nargs='*',default=[])
    ap.add_argument('--review-ref')
    a=ap.parse_args()
    ids={s['id'] for s in SPECS}
    if set(a.approved)-ids: ap.error('Unknown approved ids')
    if a.render and (not a.approved or not a.review_ref):
        ap.error('Render requires named reviewed ids and a review reference')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1280,360*math.ceil(len(SPECS)/2)),(40,58,79))
    records=[];checks=[]
    for i,s in enumerate(SPECS):
        name='code_graphic_032_'+s['id']+'_v01'
        preview=out/(name+'.png');im=frame(s);im.save(preview)
        bg=Image.new('RGBA',(W,H),(40,58,79,255));bg.alpha_composite(im)
        tile=bg.convert('RGB').resize((640,360))
        ImageDraw.Draw(tile).text((8,8),s['id'],fill='white')
        sheet.paste(tile,((i%2)*640,(i//2)*360))
        bounds=im.getchannel('A').getbbox()
        checks.append(dict(id=s['id'],entry_clear=frame(s,0).getbbox() is None,
                           exit_clear=frame(s,3.6).getbbox() is None,
                           alpha_bounds=bounds,
                           inside_5_percent=bool(bounds and bounds[0]>=96 and bounds[1]>=54 and bounds[2]<=1824 and bounds[3]<=1026),
                           motion_changes=frame(s,.8).tobytes()!=frame(s,1.5).tobytes()))
        rec=dict(**s,preview=str(preview),preview_sha256=hashlib.sha256(preview.read_bytes()).hexdigest(),
                 status='DRAFT_REQUIRES_ROW_STILL_REVIEW',duration=3.6,
                 composite_status='UNVERIFIED: approved graded moving real plate required',rendered=False)
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
            rec.update(rendered=True,render=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),review_ref=a.review_ref,status='RENDERED_NOT_COMPOSITE_APPROVED')
        records.append(rec)
    sheet.save(out/'mechanism_previews.jpg',quality=94)
    (out/'MECHANISM_MANIFEST_v01.json').write_text(json.dumps(dict(job='J2089',status='PARTIAL_DRAFT_BATCH',clips=records),indent=2)+'\n')
    (out/'MECHANISM_CHECKS_v01.json').write_text(json.dumps(checks,indent=2)+'\n')
    if not all(c['entry_clear'] and c['exit_clear'] and c['inside_5_percent'] and c['motion_changes'] for c in checks):
        raise SystemExit('Preview structural check failed; inspect MECHANISM_CHECKS_v01.json')


if __name__=='__main__':main()
