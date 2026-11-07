#!/usr/bin/env python3
"""J2141: record the closed R9 columnar search and the R7 crust plate. £0.

Downloads stay in the media directory. This script never re-fetches them and
never overwrites a plate. It does not claim motion or audio perception.
Run with /usr/bin/python3 (Pillow 11). A fresh plate is made only with --render.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSET = 'commons_usgs_kilauea_skylight'
PLATE = 'plate_031_r07_crust_v01.mp4'
FRAMES = 131
FPS = 25
FILM_START = 59.92
SOURCE_SHA256 = '418b953d6d490d0537912d5f4f0b7860bdf75fa6835bae1518312a8e635f4d49'
SOURCE_SHA1 = 'cc53ecc474c7eda5032d6150b3849a923953d867'
REJECTED = {
    'craters_of_the_moon.jpg': '8f4bb9de6d874dccb4b28eba1aa526b5515a217f11080561e45d9e583859c0ba',
    'little_devils_postpile.jpg': 'ef8338c27eb5f6c89adde08485c9945db798bc310a6423959814365b3980b166',
    'uvalde_columns.jpg': '29333354e7fa429a695ce76639347fe68e407cf2c30dde0e312693ea30e1cd8a',
}
TERMS = Path('/Users/benjaminoats/_desk/J2141-lava-v01/PD-USGov-USGS-en.wikitext')


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


def run(args, stdin=None):
    result = subprocess.run(args, input=stdin, capture_output=True)
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
    ImageDraw.Draw(image).text(
        (36, 1036), 'USGS',
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28),
        fill=(255, 255, 255, 210))
    image.save(path)


def render(root, source):
    dest = root / PLATE
    if dest.exists():
        raise FileExistsError(dest)
    credit = root / 'USGS_credit.png'
    credit_png(credit)
    with Image.open(source) as opened:
        base = opened.convert('RGB').crop((0, 270, 5184, 3186))
    width, height = base.size
    if (width, height) != (5184, 2916):
        raise RuntimeError(f'crop {width}x{height}')
    encoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', str(FPS), '-i', 'pipe:0',
        '-i', str(credit),
        '-filter_complex',
        '[0:v]eq=brightness=0.012:saturation=1.06,noise=alls=4:allf=t[plate];'
        '[plate][1:v]overlay=0:0:format=auto[out]',
        '-map', '[out]', '-an', '-frames:v', str(FRAMES),
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-pix_fmt', 'yuv420p', '-r', str(FPS), '-movflags', '+faststart', str(dest),
    ], stdin=subprocess.PIPE)
    try:
        for index in range(FRAMES):
            zoom = 1 + 0.08 * index / (FRAMES - 1)
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
    for index, at in enumerate((0.2, 1.6, 3.2, 5.0)):
        still = root / f'review_{index}.jpg'
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(at), '-i', str(plate),
             '-frames:v', '1', '-q:v', '3', str(still)])
        frames.append(Image.open(still).convert('RGB').resize((640, 360)))
    image = Image.new('RGB', (1280, 720), (12, 23, 39))
    for index, frame in enumerate(frames):
        image.paste(frame, ((index % 2) * 640, (index // 2) * 360))
    image.save(sheet, quality=85)
    return sheet


def r09_sheet(root):
    sheet = root / 'CONTACT_r09.jpg'
    image = Image.new('RGB', (1920, 640), (18, 24, 32))
    draw = ImageDraw.Draw(image)
    names = (
        ('craters_of_the_moon.jpg', 'Idaho flow, not columns'),
        ('little_devils_postpile.jpg', 'Columns, 700 px wide'),
        ('uvalde_columns.jpg', 'Nephelinite, 307 px'),
    )
    for index, (name, label) in enumerate(names):
        with Image.open(root / name) as src:
            thumb = src.convert('RGB')
            thumb.thumbnail((620, 520))
        x = index * 640 + (620 - thumb.width) // 2
        image.paste(thumb, (x, 20))
        draw.text((index * 640 + 16, 560), label, fill='white')
    image.save(sheet, quality=85)
    return sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    root = args.media_root.resolve()
    source = root / 'skylight_usgs_flickr.jpg'
    page = root / 'skylight_flickr.wikitext'
    for path in (source, page, TERMS):
        if not path.is_file():
            raise FileNotFoundError(path)
    if sha(source) != SOURCE_SHA256 or sha1(source) != SOURCE_SHA1:
        raise RuntimeError('Flickr original hash does not match Commons')
    require(page, '{{PD-USGov-USGS}}')
    require(page, 'U.S. Geological Survey')
    require(page, 'Kīlauea')
    terms = require(TERMS, 'public domain')
    if 'United States Geological Survey' not in terms:
        raise RuntimeError('USGS template wording missing')
    for name, expected in REJECTED.items():
        path = root / name
        if sha(path) != expected:
            raise RuntimeError('Rejected candidate hash changed: ' + name)
    require(root / 'little_devils.wikitext', '{{PD-USGov-USGS}}')
    require(root / 'craters.wikitext', '{{PD-USGov-USGS}}')
    require(root / 'uvalde.wikitext', '{{PD-USGS}}')
    require(root / 'uvalde.wikitext', 'nephelinite')
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
    rejected_sheet = r09_sheet(root)
    pool = json.loads(args.manifest.read_text())
    record = dict(
        asset_id=ASSET,
        title='The Skylight, Puʻu ʻŌʻō, Kīlauea, 2 June 2016',
        description=('USGS Flickr original: a skylight about 6 m across in solidified '
                     'pahoehoe at Puʻu ʻŌʻō, eruption episode 61g. The lava stream '
                     'travels toward the upper right. This is the cooling-crust close-up, '
                     'not a columnar hillside.'),
        source_page='https://commons.wikimedia.org/wiki/File:The_Skylight_(27889592710).jpg',
        flickr_page='https://www.flickr.com/photos/usgeologicalsurvey/27889592710/',
        source_url='https://upload.wikimedia.org/wikipedia/commons/5/5f/The_Skylight_%2827889592710%29.jpg',
        credit='U.S. Geological Survey',
        local_path=str(source), sha256=SOURCE_SHA256, source_sha1=SOURCE_SHA1,
        bytes=source.stat().st_size, width=5184, height=3456, rows=[7],
        planned_appearances=1, max_appearances=2,
        download_status='downloaded', review_status='static_candidate_not_KEEP',
        licence='Public domain',
        licence_status='Commons_PD-USGov-USGS_template_on_this_file',
        licence_evidence_path=str(TERMS), licence_evidence_sha256=sha(TERMS),
        source_evidence_path=str(page), source_evidence_sha256=sha(page),
        generation_authorized=False,
        review_note=('Centre 16:9 crop, then a linear 8% push. Maximum scale against '
                     'the crop is 0.40, a downscale. Stills inspected. No motion review.'))
    previous = next((item for item in pool['assets'] if item.get('asset_id') == ASSET), None)
    if previous:
        if previous['sha256'] != SOURCE_SHA256:
            raise RuntimeError('Pool hash does not match the original')
    else:
        pool['assets'].append(record)
    plate_record = dict(
        file=PLATE, path=str(plate), sha256=sha(plate), bytes=plate.stat().st_size,
        film_start_s=FILM_START, film_end_s=round(FILM_START + FRAMES / FPS, 2),
        row_end_s=65.14, frames=FRAMES, fps=FPS, width=1920, height=1080,
        audio=False, full_decode=True, crop_xywh=[0, 270, 5184, 2916],
        push='linear 1.00 to 1.08, centre', max_scale_vs_crop=0.4,
        credit='USGS', no_loop=True, no_interpolation=True,
        follows='code_graphic_031_r07_grains_v02 ends 59.92',
        status='technical_candidate_pending_motion_review')
    pool['r07_crust_plate_v01'] = plate_record
    pool['r07_contact_sheet'] = str(sheet)
    pool['r07_contact_sheet_sha256'] = sha(sheet)
    checkpoints = pool.setdefault('search_checkpoints_v01', [])
    if not any(item.get('input') == 'R9 USGS columnar basalt hillside' for item in checkpoints):
        checkpoints.append(dict(
            input='R9 USGS columnar basalt hillside', date='2026-11-07',
            candidates_examined=3, active_minutes=16,
            budget_status='three-candidate limit reached; do not restart these three files',
            outcome=('No examined USGS still is a sharp full-frame columnar basalt hillside. '
                     'Chief needs a larger columnar source before another R9 pass. '
                     'Cooling crust, a hand sample, cores and wildlife are different inputs.'),
            contact_sheet=str(rejected_sheet),
            contact_sheet_sha256=sha(rejected_sheet),
            candidates=[
                dict(file='craters_of_the_moon.jpg',
                     sha256=REJECTED['craters_of_the_moon.jpg'],
                     source='https://commons.wikimedia.org/wiki/File:Basalt_flow_on_craters_of_the_moon_idaho.jpg',
                     licence='PD-USGov-USGS', width=4725, height=2562,
                     result='1925 G.R. Mansfield photograph of a recent basalt flow at Craters of the Moon. Public domain. It is a wide flow with an empty sky, not columnar joints. Rejected for R9.'),
                dict(file='little_devils_postpile.jpg',
                     sha256=REJECTED['little_devils_postpile.jpg'],
                     source='https://commons.wikimedia.org/wiki/File:Little-Devils-Postpile.jpg',
                     licence='PD-USGov-USGS', width=700, height=454,
                     result='N.K. Huber, USGS Bulletin 1595, columnar joints in a basalt plug, Little Devils Postpile. The subject matches. Full frame would be 2.74×. The library original URL returns 404. Not rendered.'),
                dict(file='uvalde_columns.jpg',
                     sha256=REJECTED['uvalde_columns.jpg'],
                     source='https://commons.wikimedia.org/wiki/File:Uvalde_columns.jpg',
                     licence='PD-USGS', width=307, height=230,
                     result='Columnar jointing in melilite-olivine nephelinite, Uvalde County, extracted from a banner. Wrong rock and 307 px wide. Rejected for R9.'),
            ]))
    if not any(item.get('input') == 'R7 USGS cooling basalt crust close-up' for item in checkpoints):
        checkpoints.append(dict(
            input='R7 USGS cooling basalt crust close-up', date='2026-11-07',
            candidates_examined=1, active_minutes=12,
            budget_status='Stopped when the USGS Flickr original of this skylight was suitable.',
            outcome=('Admitted The Skylight, 5184×3456, PD-USGov-USGS. A smaller Pixabay '
                     'reupload of the same picture was opened first and is not the plate source. '
                     'Two other Commons pahoehoe titles were identified and not downloaded.'),
            identified_not_examined=[
                dict(source='https://commons.wikimedia.org/wiki/File:Ropy_pahoehoe.jpg',
                     result='500×800. Close ropy pahoehoe, public domain. Too small for a full frame. Not downloaded.'),
                dict(source='https://commons.wikimedia.org/wiki/File:Pahoehoe_toe.jpg',
                     result='800×500. Advancing toe, public domain. Full-frame scale would exceed 2.35×. Not downloaded.'),
            ]))
    args.manifest.write_text(json.dumps(pool, indent=2) + '\n')
    polish_path = root / 'polish_r07.json'
    polish = json.loads(polish_path.read_text()) if polish_path.is_file() else None
    check = dict(
        job='J2141', spend_gbp=0, asset_id=ASSET, original_sha256=SOURCE_SHA256,
        plate=plate_record, contact_sheet_sha256=sha(sheet),
        r09_contact_sheet_sha256=sha(rejected_sheet),
        component_polish=None if polish is None else dict(
            verdict=polish['verdict'], failed=len(polish['failed']),
            warnings=len(polish['warn'])),
        motion_perception=False, audio_perception=False,
        status='technical_checks_only_not_film_PASS')
    check_path = args.manifest.parent / 'HARVEST_R07_CRUST_TECHNICAL_CHECK_v01.json'
    check_path.write_text(json.dumps(check, indent=2) + '\n')
    search_path = args.manifest.parent / 'HARVEST_R09_COLUMNAR_SEARCH_v01.json'
    search_path.write_text(json.dumps(
        next(item for item in checkpoints if item['input'] == 'R9 USGS columnar basalt hillside'),
        indent=2) + '\n')
    print(f'{ASSET} verified; plate {plate_record["sha256"][:12]} frames {FRAMES}')


if __name__ == '__main__':
    main()
