#!/usr/bin/env python3
"""031 £0 second mechanism batch. Schematics, not measured datasets.

All overlays need graded moving plates and composite review. No approval implied.
Barcode stripe widths, particle paths and tree rings are illustrative, never
presented as a measured reversal chronology, radiation model or kauri sample.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from mechanism_graphics import W, H, FPS, NAVY, WHITE, GOLD, BLUE, RED, label, ease

HERE = Path(__file__).resolve().parent
SPECS = [
    dict(row=18, mode='barcode', start_s=191.48, duration_s=3.56,
         cue='it records every flip', source_rows=[7], alpha=False),
    dict(row=19, mode='flip_tally', start_s=199.1, duration_s=3.28,
         cue='Earth has flipped', source_rows=[7], alpha=True),
    dict(row=35, mode='rings', start_s=362.1, duration_s=10.96,
         cue='As the shield dropped', source_rows=[14], alpha=True),
    dict(row=42, mode='column_mass', start_s=427.04, duration_s=6.56,
         cue='a kilogram', source_rows=[16], alpha=True),
    dict(row=43, mode='column_stop', start_s=441.28, duration_s=4.22,
         cue='gas molecules', source_rows=[16], alpha=False),
]


def arrow(dr, x1, y1, x2, y2, colour=GOLD, width=6):
    dr.line((x1, y1, x2, y2), fill=colour, width=width)
    a = math.atan2(y2-y1, x2-x1)
    dr.polygon([(x2,y2), (x2-22*math.cos(a-.5),y2-22*math.sin(a-.5)),
                (x2-22*math.cos(a+.5),y2-22*math.sin(a+.5))], fill=colour)


def caption(dr, xy, text, size, colour, t, start, end):
    if not start<=t<end:return
    opacity=max(0,min(1,(t-start)/.35,(end-t)/.35))
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    label(ImageDraw.Draw(layer),xy,text,size,colour)
    layer.putalpha(layer.getchannel('A').point(lambda p:round(p*opacity)))
    dr._image.alpha_composite(layer)


def barcode(dr, spec, t):
    # A mirrored spreading-ridge cross-section; no time axis or invented dates.
    for side in [-1, 1]:
        for i in range(11):
            shift = (t*34) % 70
            x = 960 + side*(i*70+shift)
            dr.rectangle((min(x,x+side*68),350,max(x,x+side*68),710),
                         fill=BLUE if i%2 else RED)
            angle = 0 if i%2 else math.pi
            cy = 520
            dy = math.cos(angle)*75
            arrow(dr,x+side*34,cy+dy,x+side*34,cy-dy,WHITE,4)
    dr.line((960,320,960,745),fill=GOLD,width=8)
    for side in [-1,1]:arrow(dr,960+side*90,790,960+side*570,790)
    caption(dr,(960,160),'EVERY FLIP',64,GOLD,t,.84,3.56)
    caption(dr,(960,930),'LIKE A BARCODE',64,WHITE,t,1.92,3.56)


def flip_tally(dr, spec, t):
    # A tally, explicitly not the occurrence times of 183 individual events.
    n = round(183*ease(t/1.32))
    for i in range(n):
        x=1080+(i%31)*20; y=450+(i//31)*28
        dr.line((x,y,x,y+18),fill=GOLD,width=5)
    caption(dr,(1380,750),'183 TIMES',72,GOLD,t,1.32,3.28)


def rings(dr, spec, t):
    # A generic tree section; ring radii do not encode years or measured C14.
    cx,cy=1400,595
    for i in range(16,0,-1):
        r=18*i
        pulse=round(15*math.sin(t*1.4+i*.25))
        dr.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(133+pulse,93+pulse//2,54,245),
                   outline=(221,170,100,255),width=3)
    if t>=1.44:
        # Slider uses a shared 0..100 range, the sourced low endpoint is 6%.
        low=1-.94*ease((t-1.44)/.58)
        dr.line((1040,930,1740,930),fill=WHITE,width=4)
        dr.rounded_rectangle((1040,914,1040+700*low,946),radius=8,fill=BLUE)
        caption(dr,(1400,1000),'ABOUT 6%',54,GOLD,t,1.44,4.8)
    if t>=3.5:
        for i in range(12):
            x=1130+i*48; y=220+((t*105+i*53)%190)
            dr.line((x,y-18,x,y),fill=BLUE,width=4)
    if t>=6.56:
        # The highlighted ring grows as carbon is mentioned; no fake isotope curve.
        r=230+8*math.sin(t*2)
        dr.arc((cx-r,cy-r,cx+r,cy+r),-90,-90+360*ease((t-6.56)/1.7),fill=GOLD,width=9)
        caption(dr,(1400,180),'RADIOACTIVE CARBON',48,GOLD,t,6.56,10.3)


def column_mass(dr, spec, t):
    # Local mass-per-area comparison, not a flat-disc drawing of a planet.
    top,base=350,880
    x1,x2=1100,1540
    air=ease(t/1.1)
    water=ease((t-4.52)/.56)
    dr.rectangle((x1-95,top,x1+95,base),outline=BLUE,width=4)
    for i in range(45):
        x=x1-75+(i*37)%150;y=base-((i*67+t*18)%500)*air
        dr.ellipse((x-4,y-4,x+4,y+4),fill=BLUE)
    caption(dr,(x1,270),'1 KILOGRAM',44,GOLD,t,.14,3.7)
    caption(dr,(x1,950),'1 cm²',48,WHITE,t,1.28,4.8)
    dr.rectangle((x2-95,top,x2+95,base),outline=BLUE,width=4)
    if water>0:dr.rectangle((x2-90,base-520*water,x2+90,base),fill=(50,145,214,230))
    if t>=4.52:
        caption(dr,(x2,270),'10 METRES',48,GOLD,t,4.52,6.56)
        caption(dr,(x2,950),'WATER',48,WHITE,t,4.52,6.56)
        caption(dr,(1320,620),'=',72,WHITE,t,4.52,6.56)


def column_stop(dr, spec, t):
    # Gas molecules, not a prediction of collision altitude or particle spectrum.
    for i in range(90):
        x=180+(i*137)%1560; y=420+(i*61)%300
        wobble=4*math.sin(t*2+i)
        dr.ellipse((x-11,y-11+wobble,x+11,y+11+wobble),fill=BLUE)
        dr.ellipse((x+8,y-11+wobble,x+30,y+11+wobble),fill=BLUE)
    dr.rectangle((120,860,1800,950),fill=(92,110,119))
    for i in range(15):
        x=210+i*105
        p=(t*.65+i*.12)%1
        y=170+320*min(1,p*2)
        if p<.5:dr.line((x,y-35,x,y),fill=GOLD,width=5)
        elif p<.7:
            r=5+30*(p-.5)/.2
            dr.ellipse((x-r,y-r,x+r,y+r),outline=GOLD,width=3)
    caption(dr,(960,115),'GAS MOLECULES',64,GOLD,t,0,2.4)
    caption(dr,(960,115),'STOP',64,GOLD,t,2.2,4.22)
    # Ground is already visible; no unreadable half-second end label.


def frame(spec,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0) if spec['alpha'] else NAVY+(255,))
    dr=ImageDraw.Draw(im)
    if not spec['alpha']:
        for x in range(0,W,80):dr.line((x,0,x,H),fill=(32,52,75))
        for y in range(0,H,80):dr.line((0,y,W,y),fill=(32,52,75))
    globals()[spec['mode']](dr,spec,t)
    if spec['alpha']:
        a=max(0,min(1,t/.4,(spec['duration_s']-t)/.4))
        im.putalpha(im.getchannel('A').point(lambda p:round(p*a)))
    return im


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--previews',action='store_true')
    args=ap.parse_args(argv)
    words_path=HERE.parent/'02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json'
    words=[w for w in json.loads(words_path.read_text())['words'] if w.get('type')=='word']
    args.out.mkdir(parents=True,exist_ok=True)
    records=[]
    for spec0 in SPECS:
        spec=dict(spec0)
        spec['id']=f"code_graphic_031_r{spec['row']:02d}_{spec['mode']}_v01"
        if not any(abs(w['start']-spec['start_s'])<.001 for w in words):
            raise ValueError(f'Not a locked cue: {spec}')
        end=spec['start_s']+spec['duration_s']
        if not spec['alpha'] and any(w['start']+1e-6<end<w['end']-1e-6 for w in words):
            raise ValueError(f'Cut splits a word: {spec}')
        spec['locked_start_words']=' '.join(w['text'] for w in words if spec['start_s']<=w['start']<spec['start_s']+1)
        preview=args.out/(spec['id']+'.png')
        if not preview.exists():frame(spec,spec['duration_s']*.75).save(preview)
        if not args.previews:
            dest=args.out/(spec['id']+('.mov' if spec['alpha'] else '.mp4'))
            if dest.exists():raise FileExistsError(dest)
            tmp=dest.with_name(dest.stem+'.partial'+dest.suffix)
            codec=['-c:v','qtrle','-pix_fmt','argb'] if spec['alpha'] else ['-vf','noise=alls=2:allf=t','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p']
            proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an',*codec,str(tmp)],stdin=subprocess.PIPE)
            try:
                for i in range(round(spec['duration_s']*FPS)):proc.stdin.write(frame(spec,i/FPS).tobytes())
                proc.stdin.close()
                if proc.wait():raise RuntimeError(tmp)
            except BaseException:
                proc.kill();proc.wait();raise
            tmp.rename(dest)
            spec.update(path=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size)
        spec.update(preview=str(preview),width=W,height=H,fps=FPS,schematic=True,
                    review_status='pending_composite_motion_and_Chief_review')
        records.append(spec)
        print(spec['id'],flush=True)
    args.manifest.write_text(json.dumps(dict(job='J2141',spend_gbp=0,status='partial_mechanisms_only',
        locked_words_sha256=hashlib.sha256(words_path.read_bytes()).hexdigest(),graphics=records),indent=2)+'\n')


if __name__=='__main__':main()
