#!/usr/bin/env python3
"""Index verified NASA SDO originals and build £0 row candidates; no KEEP.

Download originals and HTML evidence first. Existing media is never overwritten.
Use /usr/bin/python3 for Pillow. Media and evidence remain outside git.
"""
import argparse
import hashlib
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPECS = [
    dict(row=14, key='sdo_prominence', filename='sdo_prominence.mp4',
         asset_id='svs-3693-sdo-launching-filament', page='svs3693.html',
         page_url='https://svs.gsfc.nasa.gov/3693/',
         url='https://svs.gsfc.nasa.gov/vis/a000000/a003600/a003693/SDOAIAZoomIn_1080.mp4',
         title='SDO/AIA Zoom-In on Launching Filament (Bands 304, 171, 211)',
         credit='NASA/Goddard Space Flight Center Scientific Visualization Studio',
         source_start=6.0, duration=2.42, film_start=138.70,
         crop=[320, 0, 1600, 900], scale=1.2,
         note='Observed EUV false-colour solar imagery, with an editorial zoom. Not a simulation or visible-light photograph. Illustrates the Sun; the prominence/corona is not a surface-temperature measurement. Crop removes baked timestamp; no exact event-date claim is made.'),
    dict(row=46, key='sdo_flare', filename='sdo_flare.m4v',
         asset_id='svs-12706-sdo-x8-flare-171-304', page='svs12706.html',
         page_url='https://svs.gsfc.nasa.gov/12706/',
         url='https://svs.gsfc.nasa.gov/vis/a010000/a012700/a012706/12706_SDO_X8_Flare_171-304_H264_Good_1080.m4v',
         title='September 10, 2017 X8.2 flare, SDO 171/304 angstrom blend',
         credit='NASA/GSFC/SDO', source_start=9.0, duration=2.34,
         film_start=469.88, crop=[0, 0, 1920, 1080], scale=1.0,
         note='Observed extreme-ultraviolet image blend, false colour. This is the separately credited raw X8.2 event clip, not the produced September montage with Killer Tracks music. No source audio used. Ends at the existing hardening graphic cue (472.22 s).'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode(errors='replace'))
    return r.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_format', '-of', 'json', str(path)]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--media-root', required=True, type=Path)
    ap.add_argument('--pool', required=True, type=Path)
    a = ap.parse_args()
    root = a.media_root.resolve()
    pool = json.loads(a.pool.read_text())
    terms = root / 'NASA_MEDIA_TERMS.html'
    assert 'educational or informational purposes' in terms.read_text()
    credit_path = root / 'NASA_credit.png'
    if credit_path.exists():
        raise FileExistsError(credit_path)
    im = Image.new('RGBA', (1920, 1080))
    ImageDraw.Draw(im).text((36, 1024), 'NASA/SDO',
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28),
        fill=(255, 255, 255, 220), stroke_width=1, stroke_fill=(10, 15, 25, 200))
    im.save(credit_path)
    checks, plates = [], []
    sheet = Image.new('RGB', (1440, 620), (29, 35, 49))
    draw = ImageDraw.Draw(sheet)
    for idx, spec in enumerate(SPECS):
        src = root / spec['filename']
        page = root / spec['page']
        assert spec['url'].split('/')[-1] in page.read_text()
        info = probe(src)
        vs = next(s for s in info['streams'] if s['codec_type'] == 'video')
        assert (vs['width'], vs['height']) == (1920, 1080)
        assert spec['source_start'] + spec['duration'] < float(info['format']['duration'])
        run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(src), '-map', '0:v:0', '-f', 'null', '-'])
        record = dict(asset_id=spec['asset_id'], rows=[spec['row']], title=spec['title'],
            source_page=spec['page_url'], source_url=spec['url'], local_path=str(src),
            sha256=sha(src), bytes=src.stat().st_size, width=1920, height=1080,
            fps=vs['r_frame_rate'], duration_s=float(info['format']['duration']),
            source_evidence_path=str(page), source_evidence_sha256=sha(page),
            licence='NASA factual educational use under NASA media guidelines',
            licence_status='item_credit_and_raw_observation_origin_checked',
            licence_policy='https://www.nasa.gov/nasa-brand-center/images-and-media/',
            licence_evidence_path=str(terms), licence_evidence_sha256=sha(terms),
            credit=spec['credit'], rights_obligations='Acknowledge source; no implied endorsement; no source audio; NASA identifiers are not granted for promotional use.',
            review_status='static_candidate_not_KEEP', planned_appearances=1,
            max_appearances=5, generation_authorized=False, review_note=spec['note'])
        assert not any(r['asset_id'] == record['asset_id'] for r in pool['assets'])
        pool['assets'].append(record)
        checks.append(dict(asset_id=record['asset_id'], full_decode=True,
                           sha256=record['sha256'], bytes=record['bytes']))
        out = root / f"plate_031_r{spec['row']:02d}_solar_v01.mp4"
        x, y, w, h = spec['crop']
        vf = (f'crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,'
              'eq=brightness=0.01:saturation=1.02,noise=alls=4:allf=t,fps=25')
        run(['ffmpeg', '-v', 'error', '-n', '-ss', str(spec['source_start']),
             '-i', str(src), '-loop', '1', '-i', str(credit_path), '-t', str(spec['duration']),
             '-filter_complex', '[0:v:0]' + vf + '[p];[p][1:v]overlay=0:0:shortest=1[out]',
             '-map', '[out]', '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)])
        pi = probe(out)
        ps = next(s for s in pi['streams'] if s['codec_type'] == 'video')
        actual = float(pi['format']['duration'])
        assert abs(actual - spec['duration']) <= .021
        assert (ps['width'], ps['height'], ps['r_frame_rate'], ps['pix_fmt']) == (1920, 1080, '25/1', 'yuv420p')
        assert not any(s['codec_type'] == 'audio' for s in pi['streams'])
        run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(out), '-f', 'null', '-'])
        plate = dict(row=spec['row'], path=str(out), sha256=sha(out), bytes=out.stat().st_size,
            film_start_s=spec['film_start'], intended_duration_s=spec['duration'],
            encoded_duration_s=actual, source_interval_s=[spec['source_start'], spec['source_start']+spec['duration']],
            source_sha256=record['sha256'], crop_xywh=spec['crop'], scale=spec['scale'],
            fps=25, full_decode=True, no_loop=True, no_speed_change=True, audio=False,
            credit=spec['credit'], note=spec['note'],
            status='technical_candidate_pending_assembly_QA_and_review')
        plates.append(plate)
        for col, t in enumerate([.12, actual/2, actual-.12]):
            raw = run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(out),
                       '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'])
            im = Image.open(io.BytesIO(raw)).convert('RGB')
            im.thumbnail((480,270))
            sheet.paste(im, (col*480,idx*310))
            draw.text((col*480+10,idx*310+278), f"R{spec['row']} @ {t:.2f}s", fill='white')
        (root / f"cuts_r{spec['row']:02d}.json").write_text(json.dumps([
            dict(row=spec['row'], timeline_in=0, timeline_out=actual,
                 source=str(src), kind='footage', framing={'offset':spec['source_start']})], indent=2)+'\n')
    contact = root / 'CONTACT_v01.jpg'
    sheet.save(contact, quality=94)
    pool['solar_plates_v01'] = plates
    pool['solar_contact_sheet'] = str(contact)
    pool['solar_contact_sheet_sha256'] = sha(contact)
    pool.setdefault('search_checkpoints_v01', []).append(dict(
        input='R14b prominence and R46a solar flare', date='2026-11-06',
        candidates_examined=2, active_minutes=10,
        outcome='Two official observed SDO clips selected as static candidates; excluded music-bearing produced montage. No exhausted archive search repeated.',
        budget_status='Stopped with candidates; no unchanged search needed.'))
    a.pool.write_text(json.dumps(pool,indent=2)+'\n')
    (a.pool.parent/'HARVEST_SOLAR_TECHNICAL_CHECK_v01.json').write_text(json.dumps(dict(
        job='J2141', spend_gbp=0, original_checks=checks, rendered_plates=plates,
        contact_sheet=str(contact), contact_sheet_sha256=sha(contact),
        audio_perception=False, motion_perception=False,
        status='technical_checks_only_not_film_PASS'),indent=2)+'\n')
    print('2 originals decoded; 2 solar plates built and technically checked; no KEEP')


if __name__ == '__main__':
    main()
