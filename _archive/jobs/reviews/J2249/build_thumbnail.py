#!/usr/bin/env python3
"""J2249: deterministic typography and grade over one authentic DISR frame."""
import argparse, hashlib, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '00_Brand/Channel-Setup/tools'))
from thumb_preview import score
p = argparse.ArgumentParser()
p.add_argument('--assets', type=Path, required=True)
a = p.parse_args().assets
src = a / 'PIA07232_surface_source.jpg'
im = Image.open(src).convert('RGB')
# Exclude the source's white border. One contiguous landscape crop contains
# the prominent pebbles; no outpaint, collage, stretch or synthetic detail.
crop = (120, 330, 424, 501)
im = im.crop(crop).resize((1280, 720), Image.Resampling.LANCZOS)
im = ImageEnhance.Contrast(im).enhance(1.35)
im = ImageEnhance.Color(im).enhance(1.25)
im = ImageEnhance.Brightness(im).enhance(1.08)
im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=3))
d = ImageDraw.Draw(im)
f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf',112)
x, y = 60, 42 - f.getbbox('REAL SURFACE')[1]
d.text((x,y), 'REAL', font=f, fill='#ffe347', stroke_width=5, stroke_fill='#20180f')
x += d.textlength('REAL ', font=f)
d.text((x,y), 'SURFACE', font=f, fill='white', stroke_width=5, stroke_fill='#20180f')
out = a / '032_A_real_surface_v04.jpg'
im.save(out, quality=95, subsampling=0)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
kept = ['032_B_bright_methane_shore_v02.jpg','032_C_scale_ice_is_rock_v03.jpg']
manifest = {
 'job':'J2249','film':'OWB:032','status':'WORKER_DELIVERY_PENDING_INDEPENDENT_REVIEW','cost_gbp':0,
 'file':str(out),'sha256':sha(out),'size':[1280,720],'score':score(out,'long'),
 'source':{'file':str(src),'sha256':sha(src),'id':'PIA07232','page':'https://science.nasa.gov/photojournal/first-color-view-of-titans-surface/', 'credit':'NASA/JPL/ESA/University of Arizona', 'policy':'https://www.jpl.nasa.gov/jpl-image-use-policy/', 'rights_note':'Official NASA caption identifies DISR surface image and joint agency/university credit. Educational editorial use with credit; no endorsement. Carry credit into upload description.', 'native_file_size':list(Image.open(src).size)},
 'recipe':{'crop_xyxy':crop,'resize':'Lanczos to 1280x720, no synthetic pixels or composite','source_crop_width':304,'linear_upscale':1280/304,'contrast':1.35,'saturation':1.25,'brightness':1.08,'unsharp_mask':{'radius':1,'percent':70,'threshold':3}},
 'typography':{'font':'Arial Black','size_px':112,'visible_cap_height_px':82,'visible_top_px':42,'left_px':60,'hook':'REAL SURFACE','yellow_word':'REAL','outline_px':5},
 'retained_variants':[{'file':str(a/n),'sha256':sha(a/n)} for n in kept],
 'review_limitations':['Native DISR frame is low resolution; 304px crop enlarged 4.21x. Do not claim film picture-QA upscale compliance; reviewer must resolve suitability before approval.','Landscape crop emphasizes the pebbles and excludes the original horizon.'],
 'phone_preview':str(a/'PHONE_PREVIEW_v04.jpg'),
 'boundary':'Normal independent review still required. B/C unchanged; no upload or scheduling.'}
(a/'MANIFEST_v04.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest['score']))
