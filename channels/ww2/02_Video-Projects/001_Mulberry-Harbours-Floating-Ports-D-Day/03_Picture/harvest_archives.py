"""Fetch exact archive-ID candidates, retaining evidence; this never grants KEEP.

Usage: python3 harvest_archives.py --out /path/to/media/03_Picture
Only public-domain metadata with an official collection is downloaded. Every
caption and primary catalogue link still needs a human/model still review.
"""
import argparse
import hashlib
import html
import json
import re
import time
from pathlib import Path

import requests

IDS = ['BU 1024', 'B 5726', 'A 24675', 'A 24159', 'A 24678',
       'A 24066', 'A 24071', 'A 24084', 'A 25799', 'A 24115',
       'A 23738', 'A 25814', 'A 25826', 'H 35379', 'H 40320',
       'H 32129', 'H 32144', 'TR 1347', 'T 29', 'T 30', 'T 31',
       'T 32', 'T 54', '80-G-285176', '80-G-285167', '80-G-252794',
       'SC 195881', '26-G-2963', '80-G-285123', 'C-029878']
API = 'https://commons.wikimedia.org/w/api.php'


def plain(value):
    return html.unescape(re.sub('<[^>]+>', ' ', value)).strip()


def request(session, url, **kwargs):
    for attempt in range(4):
        response = session.get(url, timeout=40, **kwargs)
        if response.status_code in (429, 502, 503):
            retry = response.headers.get('Retry-After', '')
            time.sleep(min(90, max(10 * (attempt + 1), int(retry) if retry.isdigit() else 0)))
            continue
        response.raise_for_status()
        return response
    raise RuntimeError('Repeated HTTP failure')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers['User-Agent'] = 'FieldOrderHistoryArchiveResearch/1.0'
    records = []
    manifest = args.out / 'archive_candidates_v01.json'
    if manifest.exists():
        records = json.loads(manifest.read_text())
    finished = {r['requested_id'] for r in records if r.get('status') != 'ERROR'}
    for archive_id in IDS:
        if archive_id in finished:
            continue
        records = [r for r in records if r['requested_id'] != archive_id]
        record = {'requested_id': archive_id, 'status': 'UNRESOLVED', 'candidates': []}
        try:
            params = dict(action='query', format='json', generator='search',
                          gsrsearch='"' + archive_id + '"', gsrnamespace=6,
                          gsrlimit=4, prop='imageinfo', iiprop='url|extmetadata|size')
            data = request(session, API, params=params).json()
            for page in data.get('query', {}).get('pages', {}).values():
                info = page.get('imageinfo', [{}])[0]
                meta = info.get('extmetadata', {})
                value = lambda key: meta.get(key, {}).get('value', '')
                # Exact token in title/credit/description, rather than search rank.
                context = page['title'] + ' ' + plain(value('Credit')) + ' ' + plain(value('ImageDescription'))
                parts = re.findall('[A-Za-z]+|[0-9]+', archive_id)
                pattern = r'(?<![A-Za-z0-9])' + r'[\s_-]*'.join(parts) + r'(?![0-9])'
                exact = bool(re.search(pattern, context, re.I))
                official = bool(re.search('Official Collection|National Archives|Naval History|U.S. Navy|US Navy|Signal Corps|Coast Guard|Library and Archives Canada',
                                          plain(value('Categories') + value('Artist') + value('Credit')), re.I))
                pd = value('LicenseShortName').lower() == 'public domain'
                primary = re.findall(r'https?://(?:www\.)?(?:iwm\.org\.uk/collections/[^"<> ]+|catalog\.archives\.gov/[^"<> ]+|history\.navy\.mil/[^"<> ]+)', value('Credit'))
                candidate = dict(title=page['title'], page=info.get('descriptionurl'),
                                 url=info.get('url'), width=info.get('width'), height=info.get('height'),
                                 creator=plain(value('Artist')), date=plain(value('DateTimeOriginal')),
                                 caption=plain(value('ImageDescription')), licence=plain(value('LicenseShortName')),
                                 categories=plain(value('Categories')), primary_urls=list(dict.fromkeys(primary)),
                                 exact_id=exact, official_collection=official, review='NOT_REVIEWED')
                if exact and official and pd and info.get('url', '').split('?')[0].lower().endswith(('.jpg', '.jpeg', '.png')):
                    suffix = '.png' if '.png' in info['url'].lower() else '.jpg'
                    name = re.sub('[^A-Za-z0-9-]', '_', archive_id) + '_' + str(page['pageid']) + suffix
                    destination = args.out / name
                    if not destination.exists():
                        destination.write_bytes(request(session, info['url']).content)
                    candidate['file'] = name
                    candidate['sha256'] = hashlib.sha256(destination.read_bytes()).hexdigest()
                    record['status'] = 'CANDIDATES_DOWNLOADED_REVIEW_REQUIRED'
                record['candidates'].append(candidate)
        except Exception as exc:
            record.update(status='ERROR', error=str(exc))
        records.append(record)
        temporary = manifest.with_suffix('.tmp')
        temporary.write_text(json.dumps(records, indent=2) + '\n')
        temporary.replace(manifest)
        print(archive_id, record['status'], flush=True)
        time.sleep(8)


if __name__ == '__main__':
    main()
