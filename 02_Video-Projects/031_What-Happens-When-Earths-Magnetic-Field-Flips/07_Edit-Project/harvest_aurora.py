#!/usr/bin/env python3
"""J2141: index existing NASA CEO originals and render three row plates, £0.

Requires the catalog, FAQ and three original MP4s in --media-root. Never
overwrites output. Downloads are separate so a partial download cannot be
mistaken for verified media. No audio or moving-video perception claimed.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = 'https://eol.jsc.nasa.gov/Videos/CrewEarthObservationsVideos/'
ITEMS = [
    ('europeaurora_iss_20120405', [4], 'Aurora Borealis over Europe'),
    ('aurora_iss_20110911', [36, 50], 'Aurora Australis south of Australia'),
    ('auroraus_iss_20120413', [], 'Aurora Borealis across Northern United States'),
]
PLATES = [
    (4, 'europeaurora_iss_20120405', 8, 3.44, 31.86, 64),
    (36, 'aurora_iss_20110911', 18, 4.88, 373.84, 192),
    (50, 'aurora_iss_20110911', 4, 4, 517.86, 192),
]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout

def probe(p):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_format', '-of', 'json', str(p)]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--media-root', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    a = ap.parse_args()
    root = a.media_root.resolve()
    catalog = root / 'catalog.html'
    faq = root / 'EOL_FAQ.html'
    source = catalog.read_text()
    assert 'NASA material is not protected by copyright unless noted' in re.sub('<[^>]+>', ' ', faq.read_text())
    pool = json.loads(a.manifest.read_text())
    results = []
    for key, rows, title in ITEMS:
        marker = 'id="' + key + '"'
        pos = source.index(marker)
        end = source.index('<!--row-->', pos)
        excerpt = root / (key + '_catalog.html')
        text = source[pos:end]
        assert title in text
        assert not re.search(r'copyright|©', text, re.I), 'Per-item rights restriction needs review'
        if excerpt.exists():
            assert excerpt.read_text() == text
        else:
            excerpt.write_text(text)
        p = root / (key + '.mp4')
        info = probe(p)
        stream = next(s for s in info['streams'] if s['codec_type'] == 'video' and not s.get('disposition', {}).get('attached_pic'))
        assert (stream['width'], stream['height']) == (1024, 768)
        run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(p), '-map', '0:v:0', '-f', 'null', '-'])
        rec = dict(asset_id='eol-' + key, title=title, rows=rows,
                   source_page=BASE + '#' + key,
                   source_url=BASE + 'videos/' + key + '/' + key + 'HD_web.mp4',
                   local_path=str(p), sha256=sha(p), bytes=p.stat().st_size,
                   width=1024, height=768, fps=stream['r_frame_rate'],
                   duration_s=float(info['format']['duration']),
                   description=html.unescape(re.sub('<[^>]+>', ' ', text.split('</p>')[0])),
                   source_evidence_path=str(excerpt), source_evidence_sha256=sha(excerpt),
                   catalog_path=str(catalog), catalog_sha256=sha(catalog),
                   licence='NASA federal astronaut photography; subject to NASA conditions',
                   licence_status='per_item_NASA_crew_origin_no_third_party_notice_in_catalog',
                   licence_policy='https://eol.jsc.nasa.gov/FAQ/default.htm#terms',
                   licence_evidence_path=str(faq), licence_evidence_sha256=sha(faq),
                   credit='NASA / ISS Crew Earth Observations / Earth Science and Remote Sensing Unit, NASA Johnson Space Center',
                   rights_obligations='Factual documentary use; acknowledge NASA; link https://eol.jsc.nasa.gov/ in delivery credits; no implied endorsement; no source audio used.',
                   review_status='static_candidate_not_KEEP', generation_authorized=False,
                   planned_appearances=len(rows), max_appearances=5,
                   native_time_lapse=True, attached_cover_excluded=True,
                   review_note=('Not selected: sampled northern-US clip is very dark with prominent station hardware.' if not rows else 'Aurora recognisable in sampled stills. Full composite gates and final watch remain.'))
        previous = next((r for r in pool['assets'] if r['asset_id'] == rec['asset_id']), None)
        if previous:
            assert previous['sha256'] == rec['sha256']
        else:
            pool['assets'].append(rec)
        results.append(dict(asset_id=rec['asset_id'], sha256=rec['sha256'], full_decode=True))
    rendered = []
    if a.render:
        credit = root / 'NASA_credit.png'
        if not credit.exists():
            im = Image.new('RGBA', (1920, 1080))
            ImageDraw.Draw(im).text((36, 1024), 'NASA', font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28), fill=(255,255,255,204))
            im.save(credit)
        for row, key, start, duration, film_start, crop_y in PLATES:
            p = root / (key + '.mp4')
            out = root / f'plate_031_r{row:02d}_aurora_v01.mp4'
            if out.exists():
                raise FileExistsError(out)
            # No optical flow or loops. 12 fps time-lapse duplicated to house
            # 25 fps; crop 1024x576 then scale 1.875x, inside the 2.35x cap.
            vf = (f'crop=1024:576:0:{crop_y},scale=1920:1080:flags=lanczos,'
                  'eq=brightness=0.015:saturation=1.04,noise=alls=4:allf=t,'
                  'fps=25')
            run(['ffmpeg', '-v', 'error', '-n', '-ss', str(start), '-i', str(p),
                 '-loop', '1', '-i', str(credit), '-t', str(duration),
                 '-filter_complex', '[0:v:0]' + vf + '[plate];[plate][1:v:0]overlay=0:0:shortest=1[out]', '-map', '[out]', '-an',
                 '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
                 '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)])
            run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'])
            inf = probe(out)
            assert abs(float(inf['format']['duration']) - duration) <= .041
            rendered.append(dict(row=row, path=str(out), sha256=sha(out),
                                 film_start_s=film_start, source_interval_s=[start, start + duration],
                                 duration_s=float(inf['format']['duration']), crop_xywh=[0, crop_y, 1024, 576],
                                 scale=1.875, fps=25, native_fps=12, full_decode=True,
                                 audio=False, credit='NASA', no_loop=True,
                                 status='technical_candidate_pending_composite_QA'))
    pool['aurora_plates_v01'] = rendered or pool.get('aurora_plates_v01', [])
    pool['aurora_contact_sheet'] = str(root / 'CONTACT_v01.jpg')
    pool['aurora_contact_sheet_sha256'] = sha(root / 'CONTACT_v01.jpg')
    pool.setdefault('search_checkpoints_v01', []).append(dict(
        input='R4c northern aurora and R36/R50 southern aurora', date='2026-11-06',
        candidates_examined=3, active_minutes=8,
        outcome='Two distinct crew sequences selected as candidates; northern-US clip unassigned for dark/obstructed picture. No horse/R41 search repeated.',
        budget_status='Search stopped with candidates; no further unchanged search needed.'))
    a.manifest.write_text(json.dumps(pool, indent=2) + '\n')
    check_path = a.manifest.parent / 'HARVEST_AURORA_TECHNICAL_CHECK_v01.json'
    check = json.loads(check_path.read_text()) if check_path.exists() else {}
    check.update(job='J2141', spend_gbp=0, original_checks=results,
                 motion_perception=False, audio_perception=False,
                 status='technical_checks_only_not_film_PASS')
    if rendered:
        check['rendered_plates'] = rendered
    check_path.write_text(json.dumps(check, indent=2) + '\n')
    print(f'{len(results)} originals decoded; {len(rendered)} row plates built')

if __name__ == '__main__':
    main()
