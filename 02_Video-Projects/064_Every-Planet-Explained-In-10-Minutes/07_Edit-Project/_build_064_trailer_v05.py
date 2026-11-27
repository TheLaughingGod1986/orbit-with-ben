#!/usr/bin/env python3
"""J3909: reframe opening pictures, retaining locked audio and end card; retain v01 AAC packets and end card.

Run with Pillow installed. No generation, master render or overwrite on NAS.
Numbers are final locked values (script v04 / NASA Mercury Facts), never
interpolated temperatures. The ten opening cuts are reframed; original end-card frames remain intact.
"""
from pathlib import Path
import hashlib, json, math, shutil, subprocess as sp
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
@lru_cache(maxsize=8)
def load_image(path):
    return Image.open(path).convert('RGB')

FILM = Path('/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes')
WORK = Path('/Users/ben/_desk/worker/slot2/J3909-evidence')
SRC = FILM/'11_Upload-Package/Trailer/064_every_planet_explained_trailer.mp4'
OUT = FILM/'11_Upload-Package/Trailer/064_every_planet_explained_trailer_v05.mp4'
W,H,FPS=608,1080,24
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SPANS=[(0,84,'open'),(84,171,'map'),(171,224,'pole'),(224,275,'pole'),(275,360,'map'),(360,453,'day'),(453,532,'ice'),(532,619,'night'),(619,704,'1965'),(704,789,'colombo')]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def run(args):
    sp.run(args,check=True)
def panel(kind,progress):
    # Full-frame lifted navy; genuine NASA globe, complete limb, no letterboxing.
    im=Image.new('RGB',(W,H),(18,32,55));d=ImageDraw.Draw(im)
    for y in range(H):
        d.line((0,y,W,y),fill=(18+int(8*y/H),32+int(8*y/H),55+int(12*y/H)))
    def text(s,y,size,color='white'):
        font=ImageFont.truetype(FONT,size);box=d.textbbox((0,0),s,font=font)
        assert box[2]-box[0] <= W-88,s
        d.text(((W-(box[2]-box[0]))/2,y),s,font=font,fill=color)
    if kind in ('map','pole','ice'):
        name={'map':'PIA17386.jpg','pole':'PIA16523.jpg','ice':'PIA19411.jpg'}[kind]
        plate=load_image(FILM/'03_Reference-Material/harvest_J3022_v01'/name)
        if kind=='map':plate=plate.crop((200,240,3896,1808))
        # Restrict the polar picture to real terrain, excluding its black top margin.
        if kind in ('pole','ice'):plate=plate.crop((0,int(plate.height*.30),plate.width,plate.height))
        scale=max(W/plate.width,H/plate.height)*(1+.025*progress)
        plate=plate.resize((round(plate.width*scale),round(plate.height*scale)),Image.Resampling.LANCZOS)
        x=(plate.width-W)//2;y=(plate.height-H)//2
        return plate.crop((x,y,x+W,y+H))
    size=int(448+12*progress)
    globe=load_image(FILM/'03_Reference-Material/harvest_J3022_v01/PIA15162.jpg')
    if kind=='day':
        globe=load_image(FILM/'03_Reference-Material/harvest_J3022_v01/PIA11364.jpg').crop((960,0,1920,1020))
    if kind in ('1965','colombo'):
        globe=load_image(FILM/'03_Reference-Material/harvest_J3022_v01/PIA16853.jpg').crop((450,28,1468,1046))
    globe=globe.resize((size,size),Image.Resampling.LANCZOS)
    mask=Image.new('L',(size,size));ImageDraw.Draw(mask).ellipse((4,4,size-5,size-5),fill=255)
    im.paste(globe,((W-size)//2,270),mask);d=ImageDraw.Draw(im)
    if kind in ('open','colombo','1965'):
        text('01 / 08',158,30,'#b6cde8');text('MERCURY',205,48,'#ffe000')
        text({"open":"Sun’s closest planet","colombo":"Giuseppe Colombo","1965":"1965 · SPIN RESONANCE"}[kind],794,32)
    else:
        text('MERCURY',165,39,'#ffe000')
        text('UP TO 7×' if kind=='day' else '−180 °C',760,66,'#ffce71' if kind=='day' else '#8bd3ff')
        text('brighter' if kind=='day' else 'at night',850,34)
        # A bounded building bar; numeric label remains the actual sourced endpoint.
        width=int(360*(.15+.85*progress));d.rounded_rectangle((124,930,124+width,946),radius=6,fill='#ffce71' if kind=='day' else '#8bd3ff')
    text('NASA / JHU APL / Carnegie',1005,20,'#b6cde8')
    return im

def main():
    assert sha(SRC)=='771d1f2a368ad4dbe1ee7b4cb541b0422a8d4d739ae946a8923f5ae9a4fe3cff'
    assert not OUT.exists(), 'Version already exists: do not overwrite'
    WORK.mkdir(exist_ok=True)
    # One continuous opening stream prevents first/last-frame overlay leaks.
    opening=WORK/'opening_v05.mp4'
    proc=sp.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','24','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',str(opening)],stdin=sp.PIPE)
    for start,end,kind in SPANS:
        for frame in range(end-start):
            proc.stdin.write(panel(kind,frame/max(1,end-start-1)).tobytes())
    proc.stdin.close();assert proc.wait()==0
    dest=WORK/OUT.name
    # Retain original end-card frames 789 onward; same AAC packets throughout.
    filters='[0:v]setpts=N/(24*TB)[a];[1:v]fps=24,trim=start_frame=789,setpts=N/(24*TB)[b];[a][b]concat=n=2:v=1:a=0[v]'
    run(['ffmpeg','-v','error','-y','-i',str(opening),'-i',str(SRC),'-filter_complex',filters,'-map','[v]','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','24','-fps_mode','cfr','-video_track_timescale','12288','-c:a','copy','-movflags','+faststart',str(dest)])
    with dest.open('rb') as a, OUT.open('xb') as b:shutil.copyfileobj(a,b)
    assert sha(dest)==sha(OUT)
    print(json.dumps({'file':str(OUT),'sha256':sha(OUT),'bytes':OUT.stat().st_size,'spans_frames':SPANS},indent=2))
if __name__=='__main__':main()
