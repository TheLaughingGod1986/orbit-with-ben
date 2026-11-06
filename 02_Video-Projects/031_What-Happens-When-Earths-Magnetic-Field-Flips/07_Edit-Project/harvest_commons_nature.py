#!/usr/bin/env python3
"""J2141: bounded real-photo harvest, preserving per-file rights evidence. £0.

Candidates only: no KEEP, film-stage approval or finished crop is implied.
Run with /usr/bin/python3 (Pillow is installed there). Existing assets are
verified, never overwritten. Media and HTML/API evidence stay outside git.
"""
import argparse
import hashlib
import html
import json
import re
import urllib.parse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps
from harvest_portraits import get, digest

ITEMS = [
    ('Tane Mahuta from viewing platform further away - portrait.jpg',
     'tane_mahuta', 34, 'Public domain', 'Pseudopanax',
     'Living kauri establishing picture only; not the ancient Laschamp specimen.'),
    ('Cuevamanos.jpg', 'hand_stencils', 37, 'CC BY-SA 3.0', 'Fjturban',
     'Cueva de las Manos hand stencils; illustrative cave-art example, not proof of Laschamp age.'),
]


def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value)).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    pool = json.loads(a.manifest.read_text())
    existing = {r['asset_id']: r for r in pool['assets']}
    for title, ident, row, expected, author, note in ITEMS:
        asset_id = 'commons_' + ident
        if asset_id in existing:
            if digest(Path(existing[asset_id]['local_path'])) != existing[asset_id]['sha256']:
                raise ValueError('Existing asset hash mismatch: ' + asset_id)
            continue
        api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(dict(
            action='query', format='json', prop='imageinfo',
            iiprop='url|size|extmetadata|sha1', titles='File:' + title))
        raw = get(api)
        page = next(iter(json.loads(raw)['query']['pages'].values()))
        info = page['imageinfo'][0]
        meta = {k: v['value'] for k, v in info['extmetadata'].items()}
        if meta['LicenseShortName'] != expected or author not in plain(meta.get('Artist', '')):
            raise ValueError('Unexpected licence or author: ' + title)
        source = 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote('File:' + title)
        api_file = a.out / (ident + '_api.json')
        rights_file = a.out / (ident + '_rights.html')
        for path, content in [(api_file, raw), (rights_file, get(source))]:
            if not path.exists():
                path.write_bytes(content)
        dest = a.out / (ident + '.jpg')
        if not dest.exists():
            dest.write_bytes(get(info['url']))
        with Image.open(dest) as im:
            im.verify()
        with Image.open(dest) as im:
            width, height = im.size
        if (width, height) != (info['width'], info['height']):
            raise ValueError('Native dimensions differ from API')
        if hashlib.sha1(dest.read_bytes()).hexdigest() != info['sha1']:
            raise ValueError('Original file differs from Commons SHA1')
        licence_url = meta.get('LicenseUrl')
        required = meta.get('AttributionRequired', '').lower() == 'true'
        if required and not licence_url:
            raise ValueError('Missing required licence URL')
        terms_file = None
        if licence_url:
            terms_file = a.out / (ident + '_licence.html')
            if not terms_file.exists():
                terms_file.write_bytes(get(licence_url))
        record = dict(asset_id=asset_id, title=title, rows=[row],
            source_page=source, source_api=api, source_url=info['url'],
            local_path=str(dest), sha256=digest(dest), source_sha1=info['sha1'],
            bytes=dest.stat().st_size, width=width, height=height,
            credit=author + ' / Wikimedia Commons', licence=expected,
            licence_url=licence_url, attribution_required=required,
            licence_status='Commons_per_file_assertion_verified',
            source_evidence_path=str(api_file), source_evidence_sha256=digest(api_file),
            licence_evidence_path=str(rights_file), licence_evidence_sha256=digest(rights_file),
            licence_terms_path=str(terms_file) if terms_file else None,
            licence_terms_sha256=digest(terms_file) if terms_file else None,
            rights_obligations=('Credit author and source; link CC BY-SA 3.0; indicate crops/grade; '
                'license adaptations under same/compatible terms; carry these into delivery credits.'
                if required else 'Author releases photograph into public domain; courtesy credit retained.'),
            planned_appearances=1, max_appearances=2, max_upscale=2.35,
            full_width_scale=round(1920 / width, 4),
            full_height_scale=round(1080 / height, 4),
            download_status='downloaded', review_status='pending_Chief_crop_and_composite_review',
            review_note=note, generation_authorized=False)
        pool['assets'].append(record)
        a.manifest.write_text(json.dumps(pool, indent=2) + '\n')
        print(asset_id, width, height, expected, flush=True)
    records = [r for r in pool['assets'] if r['asset_id'] in
               {'commons_tane_mahuta', 'commons_hand_stencils'}]
    sheet = Image.new('RGB', (1280, 800), (30, 45, 65))
    dr = ImageDraw.Draw(sheet)
    for i, r in enumerate(records):
        with Image.open(r['local_path']) as src:
            im = ImageOps.exif_transpose(src).convert('RGB')
            im.thumbnail((600, 680))
        x = i * 640
        sheet.paste(im, (x + (640 - im.width) // 2, 0))
        dr.text((x + 12, 710), r['asset_id'], fill='white')
        dr.text((x + 12, 735), f"{r['width']}x{r['height']} | {r['licence']}", fill='white')
        dr.text((x + 12, 760), 'CANDIDATE ONLY - crop/composite pending', fill='white')
    contact = a.out / 'CONTACT_v01.jpg'
    sheet.save(contact, quality=92)
    pool['nature_contact_sheet'] = str(contact)
    pool['nature_contact_sheet_sha256'] = digest(contact)
    a.manifest.write_text(json.dumps(pool, indent=2) + '\n')


if __name__ == '__main__':
    main()
