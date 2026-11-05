#!/usr/bin/env python3
"""Small, resumable £0 J2141 mechanism batch; no approval implied.

Compass/grain drawings are explanatory schematics, not measured geometry.
Strength uses two sourced endpoints, never an invented historical time series.
Outputs are row-specific; existing media is never overwritten.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 25
NAVY = (25, 42, 64)
WHITE = (244, 239, 230)
GOLD = (255, 201, 74)
BLUE = (100, 194, 247)
RED = (246, 121, 98)
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
HERE = Path(__file__).resolve().parent

# Timings are from locked Scribe words, inside the approved row boundaries.
# Grain R7 ends before the row's real-lava separator: compositor still owns it.
SPECS = [
    dict(row=4, mode='compass', variant='flip', start_s=28.5, duration_s=3.36,
         source_rows=[3, 4], cue='How do we know', alpha=False),
    dict(row=7, mode='grains', variant='cool', start_s=54.2, duration_s=5.72,
         source_rows=[3], cue='As lava or brick cools', alpha=False),
    dict(row=8, mode='grains', variant='reverse', start_s=73.28, duration_s=5.96,
         source_rows=[3], cue='Instead', alpha=False),
    dict(row=20, mode='strength', variant='endpoints', start_s=209.1, duration_s=3.8,
         source_rows=[8], cue='1830s', alpha=True),
    dict(row=21, mode='compass', variant='wobble', start_s=214.18, duration_s=5.44,
         source_rows=[8], cue='Why is it dropping now', alpha=True),
    dict(row=49, mode='compass', variant='local', start_s=500.24, duration_s=3.64,
         source_rows=[18], cue='A pocket compass', alpha=False),
]


def ease(x):
    return .5 - .5 * math.cos(math.pi * max(0, min(1, x)))


def label(dr, xy, text, size=52, colour=WHITE, anchor='mm'):
    if len(text.split()) > 4:
        raise ValueError(f'Label exceeds four words: {text}')
    font = ImageFont.truetype(FONT, size)
    box = dr.textbbox(xy, text, font=font, anchor=anchor)
    if not (60 <= box[0] <= box[2] <= W-60 and 40 <= box[1] <= box[3] <= H-40):
        raise ValueError(f'Unsafe label: {text}: {box}')
    dr.text(xy, text, font=font, anchor=anchor, fill=colour)


def needle(dr, x, y, angle, length=180, width=30, alpha=255):
    # Angle zero points to the top of the screen; red end is north-seeking.
    u = (math.sin(angle), -math.cos(angle))
    v = (math.cos(angle), math.sin(angle))
    left = (x + width*v[0], y + width*v[1])
    right = (x - width*v[0], y - width*v[1])
    dr.polygon([left, (x+length*u[0], y+length*u[1]), right], fill=RED+(alpha,))
    dr.polygon([left, (x-length*u[0], y-length*u[1]), right], fill=WHITE+(alpha,))
    dr.ellipse((x-10,y-10,x+10,y+10), fill=GOLD+(alpha,))


def compass(dr, spec, t):
    x, y, r = (960, 530, 310) if not spec['alpha'] else (1450, 540, 245)
    # Opaque brass housing only; the rest of R21 remains transparent for Earth limb.
    dr.ellipse((x-r-12,y-r-12,x+r+12,y+r+12), fill=(119,88,42,255), outline=GOLD, width=5)
    dr.ellipse((x-r,y-r,x+r,y+r), fill=NAVY+(255,), outline=(196,160,92), width=5)
    for degree in range(0,360,10):
        a=math.radians(degree)
        rr=r-(25 if degree%30==0 else 13)
        dr.line((x+rr*math.sin(a),y-rr*math.cos(a),x+(r-5)*math.sin(a),y-(r-5)*math.cos(a)),fill=GOLD,width=3)
    label(dr,(x,y-r+54),'N',40,RED)
    label(dr,(x,y+r-54),'S',40)
    variant=spec['variant']
    if variant=='flip':
        angle=math.pi*ease((t-.6)/1.8)
        title='UPSIDE DOWN'
    elif variant=='wobble':
        angle=.45*math.sin(t*3)+.18*math.sin(t*5.1)
        title=''
    else:
        angle=1.1*ease(t/1.5)
        title='NEAREST POLE'
        # Single illustrative target, explicitly no invented geographic placement.
        a=1.1
        tx=x+(r+70)*math.sin(a);ty=y-(r+70)*math.cos(a)
        pulse=10+5*math.sin(t*3)**2
        dr.ellipse((tx-pulse,ty-pulse,tx+pulse,ty+pulse),fill=GOLD)
    needle(dr,x,y,angle,r*.66,r*.09)
    if title:label(dr,(960,945),title,64,GOLD)


def grains(dr,spec,t):
    # Each crystal carries one little compass, held in the solid matrix once cool.
    cool=spec['variant']=='cool'
    s=ease((t-.5)/2.5)
    target=0 if cool else math.pi
    col=tuple(round(a+(b-a)*s) for a,b in zip((146,70,44),(78,85,95)))
    dr.rounded_rectangle((160,220,1760,850),radius=32,fill=col,outline=(165,168,175),width=3)
    for i in range(24):
        x=290+(i%8)*190;y=355+(i//8)*180
        # Deterministic starting angles, not scientific sample measurements.
        initial=math.sin(i*2.7)*2.6
        angle=initial*(1-s)+target*s
        if cool:angle+=.12*math.sin(t*9+i)*(1-s)
        dr.ellipse((x-65,y-65,x+65,y+65),fill=(45,54,67),outline=(172,177,181),width=2)
        needle(dr,x,y,angle,47,9)
    label(dr,(960,120),'IRON OXIDE GRAINS',60,GOLD)
    label(dr,(960,950),'COOL → LOCK IN' if cool else 'OPPOSITE WAY',64)


def strength(dr,spec,t):
    # Lower-right alpha panel, for a graded moving plate; no black panel.
    # These are bars with a shared zero; the 9% loss is not exaggerated.
    s=ease((t-.65)/2.25)
    base=915;scale=4.5
    for x,value,name in [(1180,100,'1830s'),(1540,100-9*s,'TODAY')]:
        height=value*scale
        dr.rounded_rectangle((x-105,base-height,x+105,base),radius=8,fill=(100,194,247,230) if name=='1830s' else (255,201,74,240))
        label(dr,(x,base+52),name,48)
        label(dr,(x,base-height-45),f'{round(value)}%',50)
    dr.line((1030,base,1690,base),fill=WHITE,width=4)
    label(dr,(1360,325),'ABOUT 9% LOWER',54,GOLD)


def frame(spec,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0) if spec['alpha'] else NAVY+(255,))
    dr=ImageDraw.Draw(im)
    if not spec['alpha']:
        for x in range(0,W,80):dr.line((x,0,x,H),fill=(32,52,75),width=1)
        for y in range(0,H,80):dr.line((0,y,W,y),fill=(32,52,75),width=1)
    {'compass':compass,'grains':grains,'strength':strength}[spec['mode']](dr,spec,t)
    if spec['alpha']:
        a=min(1,t/.4,(spec['duration_s']-t)/.4)
        im.putalpha(im.getchannel('A').point(lambda p:round(p*max(0,a))))
    return im


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--previews',action='store_true')
    args=ap.parse_args(argv)
    args.out.mkdir(parents=True,exist_ok=True)
    words_path=HERE.parent/'02_Voiceover/stt/magnetic_field_flip_vo_v02a/stt_raw.json'
    words=json.loads(words_path.read_text())['words']
    records=[]
    for s0 in SPECS:
        s=dict(s0)
        s['id']=f"code_graphic_031_r{s['row']:02d}_{s['mode']}_v02"
        # Verify the declared row-specific cue against the locked transcript.
        cue=' '.join(w['text'] for w in words if w.get('type')=='word' and s['start_s']<=w['start']<s['start_s']+1)
        s['locked_start_words']=cue
        if not any(w.get('type')=='word' and abs(w['start']-s['start_s'])<.001 for w in words):
            raise ValueError(f'No locked word at start: {s}')
        # A full-frame graphic may be an actual cut. Never end inside a word.
        if not s['alpha'] and any(w.get('type')=='word' and w['start']<s['start_s']+s['duration_s']<w['end'] for w in words):
            raise ValueError(f'Full-frame cut splits a locked word: {s}')
        png=args.out/(s['id']+'.png')
        if not png.exists():frame(s,s['duration_s']*.65).save(png)
        dest=args.out/(s['id']+('.mov' if s['alpha'] else '.mp4'))
        if not args.previews:
            if dest.exists():raise FileExistsError(f'Preserving existing output: {dest}')
            tmp=dest.with_name(dest.stem+'.partial'+dest.suffix)
            codec=['-c:v','qtrle','-pix_fmt','argb'] if s['alpha'] else ['-vf','noise=alls=2:allf=t','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p']
            proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an',*codec,str(tmp)],stdin=subprocess.PIPE)
            try:
                for i in range(round(s['duration_s']*FPS)):proc.stdin.write(frame(s,i/FPS).tobytes())
                proc.stdin.close()
                if proc.wait():raise RuntimeError(f'Encoding failed: {tmp}')
            except BaseException:
                proc.kill();proc.wait();raise
            tmp.rename(dest)
            s.update(path=str(dest),bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
        s.update(preview=str(png),width=W,height=H,fps=FPS,review_status='pending_composite_motion_and_Chief_review',schematic=True)
        records.append(s)
        print(s['id'],flush=True)
    args.manifest.write_text(json.dumps(dict(job='J2141',spend_gbp=0,status='partial_mechanisms_only',locked_words_sha256=hashlib.sha256(words_path.read_bytes()).hexdigest(),graphics=records),indent=2)+'\n')


if __name__=='__main__':main()
