#!/usr/bin/env python3
"""J2141: R33 sediment-core plate from one licensed NOAA photograph. £0.

The plate is a still with a linear push. This script does not claim motion
or audio perception, and it never re-downloads or overwrites a finished plate.
Run with /usr/bin/python3 (Pillow 11).
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSET = 'noaa_expl2290_tube_core'
PLATE = 'plate_031_r33_core_v01.mp4'
FRAMES = 111
FPS = 25
FILM_START = 336.92
SOURCE_SHA256 = 'b438fecc32a3cebe0b8a27e8cd34d4844c1105e597b15a3c7dec28f05b986f98'
SOURCE_SHA1 = 'fc7b11dbc4dbb0db4a33791d22416f7694a22beb'
CROP = (0, 150, 1578, 1038)  # drop the slide mount; 1578x888 is 16:9
REJECTED = {
    'aleutian_cores.jpg': 'b9d6ed360c626f12656b8c68eebf1e8b88e34eaf9d3f5afd01e3d972df212d64',
    'chile_seep_core.jpg': 'bceb68364d809edd3b33bad0d4895889282cf2eaa84263be071242fde8b81339',
}


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sha1(path):
    digest = hashlib.sha1()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def run(args):
    result = subprocess.run(args, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:].decode(errors='replace'))
    return result.stdout


def require(path, needle):
    text = path.read_text(errors='replace')
    if needle not in text:
        raise RuntimeError(f'{path.name} is missing {needle}')
    return text


def credit_png(path):
    if path.exists():
        return
    image = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28)
    text = 'Lisa Levin / NOAA'
    xy = (36, 1036)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((xy[0] + dx, xy[1] + dy), text, font=font, fill=(0, 0, 0, 180))
    draw.text(xy, text, font=font, fill=(255, 255, 255, 220))
    image.save(path)


def render(root, source):
    dest = root / PLATE
    if dest.exists():
        raise FileExistsError(dest)
    credit = root / 'credit_noaa.png'
    credit_png(credit)
    with Image.open(source) as opened:
        base = opened.convert('RGB').crop(CROP)
    width, height = base.size
    if (width, height) != (1578, 888):
        raise RuntimeError(f'crop {width}x{height}')
    encoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', 'pipe:0',
        '-i', str(credit),
        '-filter_complex',
        '[0:v]eq=brightness=0.02:saturation=1.08[plate];'
        '[plate][1:v]overlay=0:0:format=auto[out]',
        '-map', '[out]', '-an', '-frames:v', str(FRAMES),
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-pix_fmt', 'yuv420p', '-r', str(FPS), '-movflags', '+faststart', str(dest),
    ], stdin=subprocess.PIPE)
    try:
        for index in range(FRAMES):
            zoom = 1 + 0.06 * index / (FRAMES - 1)
            crop_w = width / zoom
            crop_h = height / zoom
            left = (width - crop_w) / 2
            top = (height - crop_h) / 2
            frame = base.crop((
                round(left), round(top), round(left + crop_w), round(top + crop_h)
            )).resize((1920, 1080), Image.Resampling.LANCZOS)
            encoder.stdin.write(frame.tobytes())
    finally:
        encoder.stdin.close()
        code = encoder.wait()
    if code:
        raise RuntimeError(f'ffmpeg exited {code}')


def probe(path):
    return json.loads(run([
        'ffprobe', '-v', 'error', '-count_frames', '-show_streams',
        '-show_format', '-of', 'json', str(path)]))


def contact(root, plate):
    sheet = root / 'CONTACT_v01.jpg'
    frames = []
    for index, at in enumerate((0.2, 1.4, 2.8, 4.1)):
        still = root / f'review_{index}.jpg'
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(at), '-i', str(plate),
             '-frames:v', '1', '-q:v', '3', str(still)])
        frames.append(Image.open(still).convert('RGB').resize((640, 360)))
    image = Image.new('RGB', (1280, 720), (12, 23, 39))
    for index, frame in enumerate(frames):
        image.paste(frame, ((index % 2) * 640, (index // 2) * 360))
    image.save(sheet, quality=85)
    return sheet


def rejected_sheet(root):
    sheet = root / 'CONTACT_rejected_v01.jpg'
    image = Image.new('RGB', (1280, 720), (18, 24, 32))
    draw = ImageDraw.Draw(image)
    names = (
        ('aleutian_cores.jpg', 'Art Howard, no licence on the page'),
        ('chile_seep_core.jpg', 'Jeff Beeson, no licence on the page'),
    )
    for index, (name, label) in enumerate(names):
        with Image.open(root / name) as src:
            thumb = src.convert('RGB')
            thumb.thumbnail((600, 560))
        x = index * 640 + (620 - thumb.width) // 2
        image.paste(thumb, (x, 20))
        draw.text((index * 640 + 16, 680), label, fill='white')
    image.save(sheet, quality=85)
    return sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    root = args.media_root.resolve()
    source = root / 'expl2290_commons.jpg'
    flickr = root / 'flickr_expl2290.html'
    wikitext = root / 'expl2290.wikitext'
    for path in (source, flickr, wikitext):
        if not path.is_file():
            raise FileNotFoundError(path)
    if sha(source) != SOURCE_SHA256 or sha1(source) != SOURCE_SHA1:
        raise RuntimeError('Commons original hash does not match')
    require(flickr, 'https://creativecommons.org/licenses/by/2.0/')
    require(flickr, 'expl2290')
    require(flickr, 'Lisa Levin')
    require(wikitext, 'tube core')
    require(wikitext, '{{cc-by-2.0}}')
    for name, expected in REJECTED.items():
        path = root / name
        if sha(path) != expected:
            raise RuntimeError('Rejected candidate hash changed: ' + name)
    require(root / 'noaa_aleutian.html', 'Art Howard')
    require(root / 'noaa_chile.html', 'Jeff Beeson')
    plate = root / PLATE
    if args.render:
        render(root, source)
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
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(plate), '-f', 'null', '-'])
    sheet = contact(root, plate)
    rejected = rejected_sheet(root)
    cuts = [{
        'row': 33, 'timeline_in': 0.0, 'timeline_out': round(FRAMES / FPS, 2),
        'source': 'expl2290_commons.jpg', 'framing': {},
    }]
    (root / 'cuts_r33.json').write_text(json.dumps(cuts, indent=2) + '\n')
    pool = json.loads(args.manifest.read_text())
    record = dict(
        asset_id=ASSET,
        title='expl2290 tube core, Peru-Chile oxygen-minimum zone',
        description=(
            'NOAA Photo Library expl2290: an 8 cm tube core from a Thioploca '
            'bacterial mat on the Chile margin. It is a real ocean sediment core. '
            'It is not an IODP paleomagnetic section and it does not show the '
            '100,000-year magnetic record. The white layer is the bacterial mat.'),
        source_page='https://commons.wikimedia.org/wiki/File:Expl2290_-_Flickr_-_NOAA_Photo_Library.jpg',
        flickr_page='https://www.flickr.com/photos/noaaphotolib/5277866198/',
        source_url='https://upload.wikimedia.org/wikipedia/commons/2/27/Expl2290_-_Flickr_-_NOAA_Photo_Library.jpg',
        credit='Lisa Levin / NOAA Photo Library',
        local_path=str(source), sha256=SOURCE_SHA256, source_sha1=SOURCE_SHA1,
        bytes=source.stat().st_size, width=1578, height=1171, rows=[33],
        planned_appearances=1, max_appearances=2,
        download_status='downloaded', review_status='static_candidate_not_KEEP',
        licence='CC BY 2.0',
        licence_url='https://creativecommons.org/licenses/by/2.0/',
        licence_status='Flickr_page_states_CC_BY_2.0; Commons also carries a PD-USGov-NOAA template, which is not the licence used',
        attribution_required=True,
        source_evidence_path=str(flickr), source_evidence_sha256=sha(flickr),
        wikitext_path=str(wikitext), wikitext_sha256=sha(wikitext),
        generation_authorized=False,
        review_note=(
            'Slide mount cropped off. Centre 16:9, then a linear 6% push. '
            'Maximum scale against the crop is 1.29. Stills inspected. No motion review. '
            'On-screen credit is Lisa Levin / NOAA. Changes: crop, grade, push.'))
    previous = next((item for item in pool['assets'] if item.get('asset_id') == ASSET), None)
    if previous:
        if previous['sha256'] != SOURCE_SHA256:
            raise RuntimeError('Pool hash does not match the original')
    else:
        pool['assets'].append(record)
    plate_record = dict(
        file=PLATE, path=str(plate), sha256=sha(plate), bytes=plate.stat().st_size,
        film_start_s=FILM_START, film_end_s=round(FILM_START + FRAMES / FPS, 2),
        row_end_s=349.16, frames=FRAMES, fps=FPS, width=1920, height=1080,
        audio=False, full_decode=True, crop_xywh=list(CROP),
        push='linear 1.00 to 1.06, centre', max_scale_vs_native_width=round(1920 / 1578 * 1.06, 3),
        credit='Lisa Levin / NOAA', licence='CC BY 2.0',
        no_loop=True, no_interpolation=True,
        hands_to='CODE paleo at the 41,000 cue, 341.38 s',
        status='technical_candidate_pending_motion_review')
    pool['r33_core_plate_v01'] = plate_record
    pool['r33_contact_sheet'] = str(sheet)
    pool['r33_contact_sheet_sha256'] = sha(sheet)
    checkpoints = pool.setdefault('search_checkpoints_v01', [])
    checkpoint = dict(
        input='R33 NOAA/IODP deep-ocean sediment core photo', date='2026-11-07',
        candidates_examined=3, active_minutes=18,
        budget_status='three-candidate limit reached; do not restart these three files',
        outcome=(
            'One licensed plate: NOAA Photo Library expl2290, CC BY 2.0, Lisa Levin. '
            'It is an 8 cm microbial-mat tube core, not a long paleomagnetic section. '
            'Two sharper NOAA Ocean Exploration cores were not used: the pages name '
            'Art Howard and Jeff Beeson and do not state a licence. Chief needs a '
            'new source before another R33 pass. The marine fossil plate and wildlife '
            'are different inputs.'),
        contact_sheet=str(rejected), contact_sheet_sha256=sha(rejected),
        admitted=ASSET,
        candidates=[
            dict(file='expl2290_commons.jpg', sha256=SOURCE_SHA256,
                 source='https://www.flickr.com/photos/noaaphotolib/5277866198/',
                 licence='CC BY 2.0', width=1578, height=1171,
                 result='Used. Real ocean sediment in a tube. Soft, scratched, slide-mounted. Microbial mat on top.'),
            dict(file='aleutian_cores.jpg', sha256=REJECTED['aleutian_cores.jpg'],
                 source='https://oceanexplorer.noaa.gov/multimedia/sediment-cores/',
                 licence='not stated on the saved page', width=3000, height=2015,
                 result='Push cores on deck after Alvin. Photographer Art Howard. Identifiable people. Not used.'),
            dict(file='chile_seep_core.jpg', sha256=REJECTED['chile_seep_core.jpg'],
                 source='https://oceanexplorer.noaa.gov/multimedia/explorations-25chile-seeps-cores/',
                 licence='not stated on the saved page', width=1920, height=2560,
                 result='Split large-diameter seep core. Credit Jeff Beeson only. Clearer core, no licence statement. Not used.'),
        ])
    if not any(item.get('input') == checkpoint['input'] for item in checkpoints):
        checkpoints.append(checkpoint)
    args.manifest.write_text(json.dumps(pool, indent=2) + '\n')
    polish_path = root / 'polish_r33.json'
    polish = json.loads(polish_path.read_text()) if polish_path.is_file() else None
    check = dict(
        job='J2141', spend_gbp=0, asset_id=ASSET, original_sha256=SOURCE_SHA256,
        plate=plate_record, contact_sheet_sha256=sha(sheet),
        rejected_contact_sheet_sha256=sha(rejected),
        component_polish=None if polish is None else dict(
            verdict=polish['verdict'], failed=len(polish['failed']),
            warnings=len(polish['warn'])),
        motion_perception=False, audio_perception=False,
        status='technical_checks_only_not_film_PASS')
    check_path = args.manifest.parent / 'HARVEST_R33_CORE_TECHNICAL_CHECK_v01.json'
    check_path.write_text(json.dumps(check, indent=2) + '\n')
    search_path = args.manifest.parent / 'HARVEST_R33_CORE_SEARCH_v01.json'
    search_path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(f'{ASSET} verified; plate {plate_record["sha256"][:12]} frames {FRAMES}')


if __name__ == '__main__':
    main()
