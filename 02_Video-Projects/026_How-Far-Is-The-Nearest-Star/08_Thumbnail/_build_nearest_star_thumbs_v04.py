#!/usr/bin/env python3
"""J1823: deterministic no-generation layout from previously approved pool plates.
Usage: python3 _build_nearest_star_thumbs_v04.py --inputs DIR --out DIR --original-a FILE
Outputs are review candidates only. Never changes abc_v01 or upload manifests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

W,H=1280,720
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
YELLOW=(255,230,0)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def grade(im, cool=False):
    # Lift the actual telescope plate, then colour grade its shadows; no invented stars.
    # Suppress compression blocks in faint sky before lifting; preserve bright stars.
    original=im
    lum=np.asarray(im.convert('L')).astype(float)
    sky_mask=np.clip((55-lum)/40,0,1)
    im=Image.composite(im.filter(ImageFilter.GaussianBlur(2.2)),original,
                       Image.fromarray((sky_mask*255).astype('uint8')))
    a=np.asarray(im).astype(float)/255
    a=a**0.62
    shadows=(1-a.max(axis=2))[...,None]**2
    tint=np.array([0.015,0.055,0.16] if cool else [0.12,0.045,0.008])
    a=np.clip(a+shadows*tint,0,1)
    im=Image.fromarray((a*255).astype('uint8'))
    return ImageEnhance.Color(im).enhance(2.8).filter(ImageFilter.UnsharpMask(radius=1.5,percent=40,threshold=3))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--original-a',type=Path,required=True)
    args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=False)
    meta={'job':'J1823','version':'v04','status':'REVIEW ONLY — no publishing authority','title':'How Far Is the Nearest Star?',
          'correction':'Both candidates depict Proxima, not Alpha Centauri A/B. The pair image is retained in source history only and unused in v04. Locked title unchanged.',
          'composition':'Earth is a familiar foreground reference; angular sizes and separation are NOT a physical scale diagram. Telescope diffraction halos are not stellar surfaces.',
          'original_a':{'path':str(args.original_a),'sha256':sha(args.original_a)},'sources':[],'variants':[]}
    sources=[('potw1343a','Proxima Centauri','ESA/Hubble & NASA; CC BY 4.0','https://esahubble.org/media/archives/images/large/potw1343a.jpg'),
             ('GSFC_20171208_Archive_e000214','Alpha Centauri A and B, not Proxima','NASA/ESA Hubble','https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000214/GSFC_20171208_Archive_e000214~orig.jpg'),
             ('GSFC_20171208_Archive_e002130','Blue Marble 2007 East — Earth','NASA','https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e002130/GSFC_20171208_Archive_e002130~orig.jpg')]
    for id,subject,credit,url in sources:
        p=args.inputs/(id+'.jpg');meta['sources'].append({'id':id,'subject':subject,'credit':credit,'recovered_url':url,'path':str(p),'sha256':sha(p),'dimensions':Image.open(p).size})
    earth=Image.open(args.inputs/'GSFC_20171208_Archive_e002130.jpg').convert('RGB')
    # Crop the full photographed globe, retain its limb, mask only the black surround.
    box=earth.convert('L').point(lambda x:255 if x>12 else 0).getbbox()
    earth=earth.crop(box).resize((190,190),Image.Resampling.LANCZOS)
    earth=ImageEnhance.Color(ImageEnhance.Brightness(earth).enhance(1.3)).enhance(1.5)
    mask=Image.new('L',(190,190));ImageDraw.Draw(mask).ellipse((1,1,188,188),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(0.7))
    font=ImageFont.truetype(FONT,112) # 80px capitals, 11.1% of height
    for key,id,words,yellow,cool in [('B','potw1343a',['900M','YEAR','WALK'],'900M',True),('C','potw1343a',['4.2','LIGHT','YEARS'],'4.2',True)]:
        src=Image.open(args.inputs/(id+'.jpg')).convert('RGB')
        cw=src.width;ch=round(cw*9/16);top=90
        im=grade(src.crop((0,top,cw,top+ch)).resize((W,H),Image.Resampling.LANCZOS),cool)
        # Soften the photographed sky behind the top band continuously, not a slab.
        # This defocuses the upper diffraction spikes without painting a stellar surface.
        soft=im.filter(ImageFilter.GaussianBlur(38))
        soft=ImageEnhance.Brightness(soft).enhance(0.45)
        yy=np.arange(H)[:,None]
        weight=np.clip((220-yy)/70,0,1)
        blend=np.repeat(weight,W,axis=1)
        im=Image.composite(soft,im,Image.fromarray((blend*255).astype('uint8')))
        # Subject core at approximately (640,435); full Earth clears the lower-left spike.
        d=ImageDraw.Draw(im); x=48
        for word in words:
            d.text((x,34),word,font=font,fill=YELLOW if word==yellow else 'white',stroke_width=5,stroke_fill=(8,12,22),anchor='lt')
            x+=d.textlength(word+' ',font=font)
        im.paste(earth,(70,440),mask)
        name=f'nearest_star_thumb_{key}_v04.jpg';p=args.out/name;im.save(p,quality=95,subsampling=0,optimize=True)
        meta['variants'].append({'key':key,'file':name,'sha256':sha(p),'hook':' '.join(words),'yellow_word':yellow,'source_id':id,'sky_treatment':'Continuous top-edge defocus/dimming, full at y<=150 tapering to original at y220; no flat slab', 'crop':[0,top,cw,top+ch],'upscale':W/cw,'earth_box':[70,440,260,630],'hook_box':[48,34,round(x),114]})
    # Honest 168x94 samples, no final 2x enlargement (stock tool enlarges its sheet).
    sheet=Image.new('RGB',(580,142),(242,242,242));d=ImageDraw.Draw(sheet)
    paths=[args.original_a]+[args.out/v['file'] for v in meta['variants']]
    for x,label,p in zip([14,206,398],['A — existing','B v04 — Proxima','C v04 — Proxima'],paths):
        d.text((x,10),label,fill='black');sheet.paste(Image.open(p).convert('RGB').resize((168,94),Image.Resampling.LANCZOS),(x,34))
    sheet.save(args.out/'comparison_true_168x94.png')
    (args.out/'META.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':main()
