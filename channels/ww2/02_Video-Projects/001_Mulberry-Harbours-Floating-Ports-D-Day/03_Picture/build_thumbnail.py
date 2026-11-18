"""Two real-archive thumbnail drafts. No generated pixels or new factual claims."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    source = Image.open(a.source).convert('RGB')
    if source.size != (4580, 4590):
        raise ValueError('Crop recipe is only for the verified 4580x4590 BU 1024 original')
    crop = (0, 1650, 4580, 4226)
    image = source.crop(crop).resize((1280, 720), Image.Resampling.LANCZOS)
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Brightness(image).enhance(1.10)
    image = ImageEnhance.Contrast(image).enhance(1.10)
    image.save(a.out / 'ww2_001_thumb_A_archive_v01.jpg', quality=96)
    labelled = image.copy()
    d = ImageDraw.Draw(labelled)
    f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 92)
    d.text((42, 24), 'FLOATING PORT', font=f, fill='#fff9e9', stroke_width=5, stroke_fill='#242424')
    labelled.save(a.out / 'ww2_001_thumb_B_floating_port_v01.jpg', quality=96)
    sheet = Image.new('RGB', (700, 245), '#e8e5db')
    d = ImageDraw.Draw(sheet)
    small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 20)
    for i, (im, label) in enumerate([(image, 'A: archive only'), (labelled, 'B: FLOATING PORT')]):
        x = 24 + 350*i
        d.text((x, 12), label, font=small, fill='#222222')
        sheet.paste(im.resize((320,180), Image.Resampling.LANCZOS), (x,44))
    sheet.save(a.out / 'ww2_001_thumb_comparison_v01.jpg', quality=95)
    phone = Image.new('RGB', (360, 120), '#e8e5db')
    phone.paste(image.resize((168,94), Image.Resampling.LANCZOS), (8,12))
    phone.paste(labelled.resize((168,94), Image.Resampling.LANCZOS), (184,12))
    phone.save(a.out / 'ww2_001_thumb_phone_v01.jpg', quality=95)
    (a.out / 'thumbnail_recipe_v01.json').write_text(json.dumps(dict(
        source='IWM BU 1024 / Harrison (Sgt), No 5 Army Film & Photographic Unit',
        source_sha256=hashlib.sha256(a.source.read_bytes()).hexdigest(),
        source_page='https://commons.wikimedia.org/wiki/File:The_Mulberry_artificial_harbour_off_Arromanches_in_Normandy,_September_1944._BU1024.jpg',
        primary='https://www.iwm.org.uk/collections/item/object/205021912',
        licence_evidence='Commons PD-scan (PD-UKGov); official War Office collection; IWM primary returned HTTP 403 on 18 Nov 2026, so primary verification remains pending',
        crop=crop, output=[1280,720], grade='autocontrast 1%, brightness 1.10, contrast 1.10',
        review='DRAFT — primary verification and Chief packaging decision required'), indent=2)+'\n')


if __name__ == '__main__':
    main()
