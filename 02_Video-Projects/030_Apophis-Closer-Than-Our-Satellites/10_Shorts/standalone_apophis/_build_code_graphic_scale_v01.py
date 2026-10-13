#!/usr/bin/env python3
"""J0225: transparent, surface-referenced Apophis altitude comparison.
Requires Pillow, numpy and ffmpeg. No generation service or paid calls.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, FRAMES = 1080, 1920, 30, 108
STEM = 'code_graphic_030short_r05_scale_v01'
FONT = '/System/Library/Fonts/Supplemental/Arial Black.ttf'

def ease(v):
    v = max(0., min(1., v))
    return v*v*(3-2*v)

def globe(path):
    # Orthographic projection of NASA's Blue Marble texture, with limb shading.
    tex = np.asarray(Image.open(path).convert('RGB'))
    y, x = np.mgrid[:104, :104]
    x, y = (x-51.5)/50, (51.5-y)/50
    r2 = x*x+y*y
    z = np.sqrt(np.maximum(0, 1-r2))
    lon = np.arctan2(x,z) + math.radians(20)
    lat = np.arcsin(np.clip(y,-1,1))
    u = ((lon/(2*math.pi)+.5)*tex.shape[1]).astype(int)%tex.shape[1]
    v = np.clip(((.5-lat/math.pi)*tex.shape[0]).astype(int),0,tex.shape[0]-1)
    rgb = tex[v,u].astype(float)*(0.50+0.50*z[...,None])
    alpha = np.clip((1-np.sqrt(r2))*50,0,1)*255
    return Image.fromarray(np.dstack([rgb,alpha]).astype('uint8'))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--earth',type=Path,required=True,help='NASA Blue Marble equirectangular texture')
    p.add_argument('--out',type=Path,default=Path(__file__).parent/'code_graphics_v01')
    a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    earth=globe(a.earth)
    font=ImageFont.truetype(FONT,96)  # measured cap height 69 px
    cap=font.getbbox('KM')[3]-font.getbbox('KM')[1]
    assert 67 <= cap <= 73, cap
    def label(im,text,y,opacity):
        layer=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(layer)
        box=d.textbbox((0,0),text,font=font,stroke_width=0)
        d.text(((W-(box[2]-box[0]))/2,y-box[1]),text,font=font,
               fill='white',stroke_width=5,stroke_fill=(10,20,34,255))
        layer.putalpha(layer.getchannel('A').point(lambda x:round(x*opacity)))
        im.alpha_composite(layer)
    def frame(t):
        im=Image.new('RGBA',(W,H)); base=Image.new('RGBA',(W,H))
        d=ImageDraw.Draw(base)
        # Physical radius scale: 50 px Earth = 6371 km; altitude measured from surface.
        r=50*(1+36000/6371); cy=1200
        points=[(540+r*math.cos(math.radians(deg)),cy+r*math.sin(math.radians(deg))) for deg in range(220,321)]
        d.line(points,fill=(128,214,255,255),width=5)
        d.line([(540,786),(540,cy-r-10)],fill=(128,214,255,255),width=3)
        base.alpha_composite(earth,(488,1148))
        enter=ease(t/.4); shift=round(12*(1-enter))
        base.putalpha(base.getchannel('A').point(lambda x:round(x*enter)))
        im.alpha_composite(base,(0,shift))
        if t>=.5:
            label(im,'36,000 KM',700,ease((t-.5)/.3))
            d=ImageDraw.Draw(im)
            yy=cy-50*(1+32000/6371)
            progress=ease((t-.5)/1.1); end=410+260*progress
            if progress>0:
                d.line([(410,yy),(end,yy)],fill=(255,209,64,255),width=7)
                d.polygon([(end,yy),(end-15,yy-9),(end-15,yy+9)],fill=(255,209,64,255))
            if t>=1.1:
                opacity=ease((t-1.1)/.3)
                d.line([(540,yy+12),(540,988)],fill=(255,209,64,round(255*opacity)),width=3)
                label(im,'32,000 KM',1010,opacity)
        fade=1-ease((t-3.2)/(11/30))
        im.putalpha(im.getchannel('A').point(lambda x:round(x*fade)))
        bbox=im.getchannel('A').getbbox()
        assert bbox is None or (bbox[1]>=656 and bbox[3]<=1264),bbox
        return im
    movie=a.out/(STEM+'.mov')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','prores_ks',
         '-profile:v','4','-pix_fmt','yuva444p10le','-alpha_bits','16','-threads','2',str(movie)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FRAMES): proc.stdin.write(frame(i/FPS).tobytes())
    proc.stdin.close()
    if proc.wait(): raise RuntimeError('ffmpeg failed')
    still=a.out/(STEM+'.png'); frame(2).save(still)
    meta={'job':'J0225','row':'030short_r05','width':W,'height':H,'fps':FPS,'frames':FRAMES,
          'duration_seconds':3.6,'alpha':'straight; ProRes 4444','centre_band_y':[656,1264],
          'label_cap_height_px':cap,'labels':['36,000 KM','32,000 KM'],
          'ticks':[{'seconds':.5,'label':'36,000 KM'},{'seconds':1.1,'label':'32,000 KM'}],
          'animation':{'earth_ring_in':[0,.4],'path_draw':[.5,1.6],'hold':[1.6,3.2],'out':[3.2,3.6]},
          'assembly':'Place clip start 0.5 s before trimmed VO word 36,000 (raw 18.58 s). Keep clear of title and first 2 s; composite over moving graded plate. Silent clip; assembler supplies house ticks.',
          'geometry':'Earth radius 50 px; ring radius 50*(1+36000/6371); closest path height 50*(1+32000/6371). Altitudes measured from surface. Straight schematic flyby segment, not an orbit.',
          'source':{'asset':str(a.earth.resolve()),'credit':'NASA Blue Marble',
                    'sha256':hashlib.sha256(a.earth.read_bytes()).hexdigest()},
          'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [movie,still]}}
    (a.out/(STEM+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({'movie':str(movie),'still':str(still),'cap_height':cap}))
if __name__=='__main__': main()
