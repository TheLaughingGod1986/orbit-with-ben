#!/usr/bin/env python3
"""J2141 R41: preserve two NASA ISS sunrise candidates and usage evidence.

No admission, motion or quality approval. Append records without replacing prior
pool entries. Originals/evidence/contact sheet stay outside git. Never overwrite.
"""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageStat

POLICY = 'https://www.nasa.gov/nasa-brand-center/images-and-media/'
ITEMS = [
    ('iss059e027932', 'https://www.nasa.gov/image-article/suns-first-rays-peek-above-earths-limb/'),
    ('iss069e025345', 'https://www.nasa.gov/image-article/an-orbital-sunrise-illuminates-earths-atmosphere/'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fetch(url, path):
    if path.exists():
        return path.read_bytes()
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    with path.open('xb') as handle:
        handle.write(data)
    return data

def metrics(image):
    y = image.convert('YCbCr').getchannel('Y')
    hist = y.histogram()
    count = image.width * image.height
    return {'mean_luma': round(ImageStat.Stat(y).mean[0], 2),
            'near_black_fraction_y_lt_20': round(sum(hist[:20])/count, 4)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    pool = json.loads(args.manifest.read_text())
    ids = {a['asset_id'] for a in pool['assets']}
    if any(ident in ids for ident, _ in ITEMS):
        raise ValueError('Candidates already registered; preserve existing records')
    policy = args.out/'NASA_MEDIA_POLICY.html'
    fetch(POLICY, policy)
    records = []
    sheet = Image.new('RGB', (1280, 900), (30, 45, 65))
    draw = ImageDraw.Draw(sheet)
    for n, (ident, page) in enumerate(ITEMS):
        api = 'https://images-api.nasa.gov/search?nasa_id='+ident
        evidence = args.out/(ident+'_api.json')
        body = json.loads(fetch(api, evidence))
        item = next(i for i in body['collection']['items'] if i['data'][0]['nasa_id']==ident)
        data = item['data'][0]
        url = next(link['href'] for link in item['links'] if link['rel']=='canonical')
        original = args.out/(ident+'.jpg')
        fetch(url, original)
        page_file = args.out/(ident+'_source.html')
        fetch(page, page_file)
        with Image.open(original) as image:
            image.verify()
        with Image.open(original) as image:
            image = image.convert('RGB')
            w, h = image.size
            # Full-width 16:9 crop keeps the horizon in the lower half for 059;
            # 069 is already 16:9. No sky/atmosphere geometry is stretched.
            ch = min(h, round(w*9/16))
            top = min(h-ch, round(h*.23)) if ident=='iss059e027932' else (h-ch)//2
            box = [0, top, w, top+ch]
            crop = image.crop(box).resize((1920,1080), Image.Resampling.LANCZOS)
            crop_file = args.out/(ident+'_crop_preview.jpg')
            if crop_file.exists():
                raise FileExistsError(crop_file)
            crop.save(crop_file, quality=94)
            for col, img in enumerate([image, crop]):
                thumb = ImageOps.contain(img, (620, 365))
                sheet.paste(thumb, (col*640+(640-thumb.width)//2, n*450))
                draw.text((col*640+12, n*450+375), ident+(' ORIGINAL' if col==0 else ' 16:9 CROP'), fill='white')
            m = metrics(crop)
        records.append(dict(asset_id=ident, title=data['title'], description=data['description'],
            source_page=page, source_api=api, source_url=url, credit='NASA',
            local_path=str(original), sha256=sha(original), bytes=original.stat().st_size,
            width=w, height=h, rows=[41], download_status='downloaded',
            licence_status='NASA_JSC_editorial_use_subject_to_NASA_media_conditions',
            licence_policy=POLICY, licence_evidence_path=str(policy), licence_evidence_sha256=sha(policy),
            source_evidence_path=str(evidence), source_evidence_sha256=sha(evidence),
            page_evidence_path=str(page_file), page_evidence_sha256=sha(page_file),
            rights_review='NASA JSC ISS photograph; source page/API show no third-party copyright credit. Credit NASA; factual editorial use only, no endorsement.',
            generation_authorized=False, native_motion=False, assigned_uses=0, max_uses=2,
            review_status='not_admitted_R41_still_and_darkness_constraints',
            review_note='Actual sunrise/blue atmospheric limb verified as a static image. This is a still, not timelapse; full R41 is 4.38 s and requires picture change before 4 s. Dark framing needs final grade and polish QA; no gate waived.',
            crop_recipe=dict(source_box_xyxy=box, output=[1920,1080], stretch=False,
                             scale_factor=round(1920/w,4), preview=str(crop_file), preview_sha256=sha(crop_file)),
            crop_metrics=m,
            metadata_note=('API date_created differs from description: preserve both; do not use as a spoken date.' if ident=='iss069e025345' else '')))
    contact = args.out/'CONTACT_R41_v01.jpg'
    if contact.exists():
        raise FileExistsError(contact)
    sheet.save(contact, quality=93)
    pool['assets'].extend(records)
    pool['r41_candidate_contact_sheet'] = dict(path=str(contact), sha256=sha(contact))
    pool['r41_investigation'] = dict(date='2026-11-07', candidates_examined=2,
        status='two_stills_inspected_not_admitted',
        next_action='Chief/editor chooses bounded bright moving ISS limb source or a reviewed two-plate still treatment; do not recheck these unchanged originals as new candidates.',
        remaining_budget='At most one further in-depth candidate in this R41 investigation; do not reset the 20-minute budget.')
    args.manifest.write_text(json.dumps(pool, indent=2)+'\n')
    print(json.dumps({'added':len(records), 'metrics':{r['asset_id']:r['crop_metrics'] for r in records}, 'contact_sheet':str(contact)}))

if __name__ == '__main__':
    main()
