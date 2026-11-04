#!/usr/bin/env python3
"""Bounded two-file Commons portrait harvest for J2141. No generation or spend.

Keeps original API and file-page rights evidence with hashes. Commons public-domain
assertions are recorded as such, independently of identity/composite approval.
"""
import argparse
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

ITEMS = [
    ('Bernard Brunhes (1867-1910).jpg', 'brunhes', 5),
    ('Carl Friedrich Gauss 1840 by Jensen.jpg', 'gauss', 20),
]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'OrbitWithBenStudio/1.0 (research provenance)'}), timeout=30).read()


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    pool=json.loads(a.manifest.read_text())
    existing={r['asset_id'] for r in pool['assets']}
    for title,ident,row in ITEMS:
        asset_id='commons_'+ident
        if asset_id in existing:continue
        api='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(
            action='query',format='json',prop='imageinfo',iiprop='url|size|extmetadata',titles='File:'+title))
        raw=get(api);data=json.loads(raw)
        page=next(iter(data['query']['pages'].values()));ii=page['imageinfo'][0]
        meta=ii['extmetadata']
        if meta['LicenseShortName']['value']!='Public domain' or meta['Copyrighted']['value'].lower()!='false':
            raise ValueError(f'Unexpected rights assertion: {title}')
        api_file=a.out/(ident+'_commons_api.json');api_file.write_bytes(raw)
        source_page='https://commons.wikimedia.org/wiki/'+urllib.parse.quote('File:'+title)
        evidence=a.out/(ident+'_rights.html');evidence.write_bytes(get(source_page))
        dest=a.out/(ident+'.jpg')
        if not dest.exists():dest.write_bytes(get(ii['url']))
        with Image.open(dest) as im:im.verify()
        with Image.open(dest) as im:width,height=im.size
        if (width,height)!=(ii['width'],ii['height']):raise ValueError('Size disagrees with source')
        pool['assets'].append(dict(asset_id=asset_id,title=title,source_page=source_page,
            source_api=api,source_url=ii['url'],local_path=str(dest),sha256=digest(dest),
            bytes=dest.stat().st_size,width=width,height=height,rows=[row],planned_appearances=1,
            max_appearances=2,max_upscale=2.35,credit=('Unknown photographer / Wikimedia Commons' if ident=='brunhes' else 'Christian Albrecht Jensen (1840) / Wikimedia Commons'),
            licence_status='Commons_per_file_public_domain_assertion_verified',licence='Public domain',
            licence_note=('Commons: pre-1910 photograph; PD in origin/life+70 countries and US pre-1931 publication' if ident=='brunhes' else 'Commons: PD-Art faithful reproduction; painter died 1870; life+100 expired'),
            attribution_required=False,licence_evidence_path=str(evidence),licence_evidence_sha256=digest(evidence),
            source_evidence_path=str(api_file),source_evidence_sha256=digest(api_file),
            review_status='pending_Chief_identity_crop_and_composite_review',download_status='downloaded',
            review_note='Use as sourced portrait inset/cutout, not full-frame stretched portrait; no cutout produced yet.'))
        print(asset_id,flush=True)
        # Checkpoint after each completed file, so an error preserves prior success.
        a.manifest.write_text(json.dumps(pool,indent=2)+'\n')
    sheet=Image.new('RGB',(1280,400*((len(pool['assets'])+1)//2)),(30,45,65));dr=ImageDraw.Draw(sheet)
    for i,r in enumerate(pool['assets']):
        with Image.open(r['local_path']) as src:
            im=src.convert('RGB');im.thumbnail((600,320))
        x=i%2*640;y=i//2*400;sheet.paste(im,(x+(640-im.width)//2,y))
        dr.text((x+16,y+332),r['asset_id'],fill='white')
        dr.text((x+16,y+352),r['licence_status'][:75],fill='white')
    contact=a.out/'contact_sheet_portraits_v02.jpg';sheet.save(contact,quality=92)
    pool.update(contact_sheet=str(contact),contact_sheet_sha256=digest(contact))
    a.manifest.write_text(json.dumps(pool,indent=2)+'\n')


if __name__=='__main__':main()
