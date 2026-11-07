#!/usr/bin/env python3
"""J2141 R6: verify the USGS fissure-20 overflight and its silent plate. £0.

The original download is separate. This script never overwrites a plate, never
uses source audio, and does not claim motion or audio perception. A fresh
media directory can be rendered with --render; an existing plate is checked.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSET = 'commons_usgs_fissure20_overflight'
PLATE = 'plate_031_r06_lava_v01.mp4'
FACT_SHA = 'aba986c5eb692f377580df14e24e35855665ad2272e23ebb240d9a8ef2c16eab'
SOURCE_START = 6.0
SOURCE_END = 12.68
FILM_START = 46.64
FRAMES = 167
CARD_DELAY = 4.20


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return result.stdout


def probe(path):
    return json.loads(run([
        'ffprobe', '-v', 'error', '-count_frames', '-show_streams',
        '-show_format', '-of', 'json', str(path)]))


def credit_png(path):
    if path.exists():
        return
    image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(image).text(
        (36, 1036), 'USGS',
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28),
        fill=(255, 255, 255, 204))
    image.save(path)


def render(root, fact):
    dest = root / PLATE
    if dest.exists():
        raise FileExistsError(dest)
    credit = root / 'USGS_credit.png'
    credit_png(credit)
    run([
        'ffmpeg', '-v', 'error', '-i', str(root / 'fissure20_overflight.webm'),
        '-i', str(credit), '-i', str(fact),
        '-filter_complex',
        '[0:v]trim=start=6.0:end=12.68,setpts=PTS-STARTPTS,'
        'crop=1908:900:6:0,scale=2290:1080:flags=lanczos,crop=1920:1080:185:0,'
        'eq=brightness=0.015:saturation=1.05,noise=alls=4:allf=t,fps=25[plate];'
        '[plate][1:v]overlay=0:0:format=auto[graded];'
        '[2:v]setpts=PTS-STARTPTS+4.20/TB[card];'
        '[graded][card]overlay=0:0:eof_action=pass:format=auto[out]',
        '-map', '[out]', '-an', '-frames:v', str(FRAMES),
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-pix_fmt', 'yuv420p', '-r', '25', '-movflags', '+faststart', str(dest)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--fact-card', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    root = args.media_root.resolve()
    original = root / 'fissure20_overflight.webm'
    page = root / 'commons_filepage.html'
    terms = root / 'PD-USGov-USGS-en.wikitext'
    for path in (original, page, terms, args.fact_card):
        if not path.is_file():
            raise FileNotFoundError(path)
    page_text = page.read_text(errors='replace')
    terms_text = terms.read_text()
    if 'PD-USGov-USGS' not in page_text and 'PD USGS' not in page_text:
        raise RuntimeError('File page is missing the USGS public-domain tag')
    if 'public domain' not in terms_text.lower() or 'United States Geological Survey' not in terms_text:
        raise RuntimeError('USGS public-domain wording was not in the saved template')
    if sha(args.fact_card) != FACT_SHA:
        raise RuntimeError('R6 FACT card hash does not match CODE_CARDS_v01.json')
    plate = root / PLATE
    if args.render:
        render(root, args.fact_card)
    if not plate.is_file():
        raise FileNotFoundError(plate)
    info = probe(plate)
    video = next(stream for stream in info['streams'] if stream['codec_type'] == 'video')
    if any(stream['codec_type'] == 'audio' for stream in info['streams']):
        raise RuntimeError('Plate contains audio')
    if (video['width'], video['height']) != (1920, 1080):
        raise RuntimeError('Plate dimensions')
    if video.get('nb_read_frames') != str(FRAMES):
        raise RuntimeError(f"Frame count {video.get('nb_read_frames')}")
    if abs(float(info['format']['duration']) - FRAMES / 25) > 0.02:
        raise RuntimeError('Duration')
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(plate), '-f', 'null', '-'])
    sheet = root / 'CONTACT_v01.jpg'
    frames = []
    for index, at in enumerate((0.4, 2.0, 4.6, 6.2)):
        still = root / f'review_{index}.jpg'
        run(['ffmpeg', '-v', 'error', '-ss', str(at), '-i', str(plate), '-frames:v', '1', '-q:v', '3', str(still)])
        frames.append(Image.open(still).convert('RGB').resize((640, 360)))
    contact = Image.new('RGB', (1280, 720), (12, 23, 39))
    for index, frame in enumerate(frames):
        contact.paste(frame, ((index % 2) * 640, (index // 2) * 360))
    contact.save(sheet, quality=85)
    pool = json.loads(args.manifest.read_text())
    record = dict(
        asset_id=ASSET,
        title='Helicopter overflight of a fast-moving lava flow, Fissure 20, 19 May 2018',
        description=('End card, read from the original: Helicopter overflight of a '
                     'fast-moving lava flow emerging from Fissure 20 on May 19, at '
                     '7:52 AM HST. The flow is advancing to the southeast. Lava '
                     'fountaining is visible in the background. USGS Hawaiian Volcano '
                     'Observatory. Commons description text is truncated by the uploader.'),
        source_page='https://commons.wikimedia.org/wiki/File:Helicopter_overflight_of_a_fast-moving_lava_flow_emerging_from_fissure_20_on_....webm',
        source_url='https://upload.wikimedia.org/wikipedia/commons/f/f1/Helicopter_overflight_of_a_fast-moving_lava_flow_emerging_from_fissure_20_on_....webm',
        credit='U.S. Geological Survey, Hawaiian Volcano Observatory',
        local_path=str(original), sha256=sha(original), bytes=original.stat().st_size,
        width=1920, height=1080, duration_s=33.539, rows=[6],
        planned_appearances=1, max_appearances=2,
        download_status='downloaded', review_status='static_candidate_not_KEEP',
        licence='Public domain',
        licence_status='Commons_PD-USGov-USGS_template_on_this_file',
        licence_evidence_path=str(terms), licence_evidence_sha256=sha(terms),
        source_evidence_path=str(page), source_evidence_sha256=sha(page),
        end_card_still=str(root / 'sample_30s.jpg'),
        generation_authorized=False,
        review_note=('Wide aerial flow only. Source title card and end card are '
                     'outside 6.00–12.68 s. The tight glowing-edge beat is not in '
                     'this interval. Source audio excluded. R7 must use a different stretch.'))
    previous = next((item for item in pool['assets'] if item.get('asset_id') == ASSET), None)
    if previous:
        if previous['sha256'] != record['sha256']:
            raise RuntimeError('Pool hash does not match the original')
    else:
        pool['assets'].append(record)
    plate_record = dict(
        file=PLATE, path=str(plate), sha256=sha(plate), bytes=plate.stat().st_size,
        film_start_s=FILM_START, film_end_s=53.32,
        source_interval_s=[SOURCE_START, SOURCE_END], frames=FRAMES, fps=25,
        width=1920, height=1080, audio=False, full_decode=True,
        crop_xywh=[6, 0, 1908, 900], scale=1.2, credit='USGS',
        fact_card='code_graphic_031_r06_fact_v01', fact_card_sha256=FACT_SHA,
        fact_delay_s=CARD_DELAY, no_loop=True, no_interpolation=True,
        status='technical_candidate_pending_motion_review')
    pool['r06_lava_plate_v01'] = plate_record
    pool['r06_contact_sheet'] = str(sheet)
    pool['r06_contact_sheet_sha256'] = sha(sheet)
    checkpoints = pool.setdefault('search_checkpoints_v01', [])
    if not any(item.get('input') == 'R6 USGS HVO Kilauea lava flow' for item in checkpoints):
        checkpoints.append(dict(
            input='R6 USGS HVO Kilauea lava flow', date='2026-11-07',
            candidates_examined=1, active_minutes=12,
            outcome=('Downloaded and statically inspected one PD-USGS fissure-20 '
                     'overflight. Two other Commons USGS fissure-20 titles were '
                     'identified and not downloaded. Search stopped with a candidate.'),
            budget_status='Stopped when a suitable wide-flow candidate was found.'))
    args.manifest.write_text(json.dumps(pool, indent=2) + '\n')
    check = dict(
        job='J2141', spend_gbp=0, asset_id=ASSET, original_sha256=record['sha256'],
        plate=plate_record, contact_sheet_sha256=sha(sheet),
        motion_perception=False, audio_perception=False,
        status='technical_checks_only_not_film_PASS')
    check_path = args.manifest.parent / 'HARVEST_USGS_LAVA_TECHNICAL_CHECK_v01.json'
    check_path.write_text(json.dumps(check, indent=2) + '\n')
    print(f'{ASSET} verified; plate {plate_record["sha256"][:12]}')


if __name__ == '__main__':
    main()
