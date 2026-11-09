#!/usr/bin/env python3
"""J2141: R45 marine-fossil plate from one NPS ammonite photograph. £0.

The plate is a still with a linear push. It does not claim motion or audio
perception, and it never re-downloads or overwrites a finished plate.
Run with /usr/bin/python3 (Pillow 11).
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSET = 'nps_katm_pachydiscus_ammonite'
PLATE = 'plate_031_r45_fossil_v01.mp4'
FRAMES = 165
FPS = 25
FILM_START = 462.40
CROP = (40, 300, 3240, 2100)  # 3200x1800, 16:9; label, ruler and colour chart stay out
SOURCE_SHA256 = 'c506b78501e0c1cb3c551253d17fc6e94d48aa73653511e15b8374f95f92a6bf'
WIKI_SHA256 = '3e5278e4a25b36e73aaab5a0f0f34b6b4b2f757e4ab874ba3b268775a59f1aa5'
REJECTED = {
    'ehmania.jpg': 'cd6cdcbc8101dd0c2963f4ba662bc9e68fca002662c622901833a7f1e826ea53',
    'blountia.jpg': 'c39188e6cb977d280b29f02b983d80df684750527b83d92af64b9a47ee3f60eb',
}


def sha(path):
    digest = hashlib.sha256()
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
    text = 'Frank Ruggles / NPS'
    xy = (36, 1036)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((xy[0] + dx, xy[1] + dy), text, font=font, fill=(0, 0, 0, 180))
    draw.text(xy, text, font=font, fill=(255, 255, 255, 220))
    image.save(path)


def render(root, source):
    dest = root / PLATE
    if dest.exists():
        raise FileExistsError(dest)
    credit = root / 'credit_nps.png'
    credit_png(credit)
    with Image.open(source) as opened:
        base = opened.convert('RGB').crop(CROP)
    width, height = base.size
    if (width, height) != (3200, 1800):
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
    for index, at in enumerate((0.3, 2.2, 4.4, 6.2)):
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
        ('ehmania.jpg', 'USNM trilobite; frame is a scale card'),
        ('blountia.jpg', 'USNM trilobite; fossil does not read'),
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
    source = root / 'ammonite.jpg'
    wikitext = root / 'ammonite.wikitext'
    for path in (source, wikitext):
        if not path.is_file():
            raise FileNotFoundError(path)
    if sha(source) != SOURCE_SHA256:
        raise RuntimeError('NPS original hash does not match')
    if sha(wikitext) != WIKI_SHA256:
        raise RuntimeError('Commons wikitext hash does not match')
    require(wikitext, '{{PD-USGov-NPS}}')
    require(wikitext, 'Frank Ruggles')
    require(wikitext, 'Pachydiscus')
    for name, expected in REJECTED.items():
        path = root / name
        if sha(path) != expected:
            raise RuntimeError('Rejected candidate hash changed: ' + name)
        wiki = root / name.replace('.jpg', '.wikitext')
        require(wiki, '{{PD-USGov-NPS}}')
    plate = root / PLATE
    if args.render:
        render(root, source)
    if not plate.is_file():
        raise FileNotFoundError(plate)
    info = probe(plate)
    video = next(stream for stream in info['streams'] if stream['codec_type'] == 'video')
    if any(stream['codec_type'] == 'audio' for stream in info['streams']):
        raise RuntimeError('Plate contains audio')
    if (int(video['width']), int(video['height'])) != (1920, 1080):
        raise RuntimeError('Plate dimensions')
    if video.get('nb_read_frames') != str(FRAMES):
        raise RuntimeError(f"Frame count {video.get('nb_read_frames')}")
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(plate), '-f', 'null', '-'])
    sheet = contact(root, plate)
    rejected = rejected_sheet(root)
    cuts = [{
        'row': 45, 'timeline_in': 0.0, 'timeline_out': round(FRAMES / FPS, 2),
        'source': 'ammonite.jpg', 'framing': {},
    }]
    (root / 'cuts_r45.json').write_text(json.dumps(cuts, indent=2) + '\n')
    pool = json.loads(args.manifest.read_text())
    record = dict(
        asset_id=ASSET,
        title='Pachydiscus kamishakensis, Kaguyak Formation, Katmai',
        description=(
            'NPS photograph of one ammonite, Pachydiscus kamishakensis, about 24 cm '
            'wide, from the Kaguyak Formation. It is a real extinct marine mollusc. '
            'It is not a sediment core, not a USGS core, and not a Smithsonian drawer '
            'specimen. The accession label, ruler and colour chart are cropped off.'),
        source_page='https://commons.wikimedia.org/wiki/File:File-Photograph_of_the_ammonite_Pachydiscus-kamishakensis_from_the_Kaguyak_Formation._This-specimen_is_approximately_24_cm_wide_(0197c09f-9653-4f8c-83b2-69f55bb2c1de).jpg',
        source_url='https://upload.wikimedia.org/wikipedia/commons/4/44/File-Photograph_of_the_ammonite_Pachydiscus-kamishakensis_from_the_Kaguyak_Formation._This-specimen_is_approximately_24_cm_wide_%280197c09f-9653-4f8c-83b2-69f55bb2c1de%29.jpg',
        nps_unit='KATM',
        accession='KATM00165',
        credit='Frank Ruggles / NPS',
        local_path=str(source), sha256=SOURCE_SHA256,
        bytes=source.stat().st_size, width=4256, height=2832, rows=[45],
        planned_appearances=1, max_appearances=2,
        download_status='downloaded', review_status='static_candidate_not_KEEP',
        licence='PD-USGov-NPS',
        licence_status='Commons file page uses {{PD-USGov-NPS}}; photographer Frank Ruggles; NPGallery credit',
        attribution_required=False,
        source_evidence_path=str(wikitext), source_evidence_sha256=WIKI_SHA256,
        generation_authorized=False,
        review_note=(
            'Crop (40, 300, 3240, 2100) drops the accession label, ruler and colour '
            'chart. Centre 6% push. Maximum scale against the 3200 px crop is 0.636. '
            'Stills inspected. No motion review. On-screen credit is Frank Ruggles / NPS.'))
    previous = next((item for item in pool['assets'] if item.get('asset_id') == ASSET), None)
    if previous:
        if previous['sha256'] != SOURCE_SHA256:
            raise RuntimeError('Pool hash does not match the original')
    else:
        pool['assets'].append(record)
    plate_record = dict(
        file=PLATE, path=str(plate), sha256=sha(plate), bytes=plate.stat().st_size,
        film_start_s=FILM_START, film_end_s=round(FILM_START + FRAMES / FPS, 2),
        row_end_s=468.98, frames=FRAMES, fps=FPS, width=1920, height=1080,
        audio=False, full_decode=True, crop_xyxy=list(CROP),
        push='linear 1.00 to 1.06, centre',
        max_scale_vs_crop_width=round(1920 / 3200 * 1.06, 3),
        credit='Frank Ruggles / NPS', licence='PD-USGov-NPS',
        no_loop=True, no_interpolation=True,
        hands_to='existing alpha extinction_check, which still starts at 462.40 s; compositor places this plate under it',
        status='technical_candidate_pending_motion_review')
    pool['r45_fossil_plate_v01'] = plate_record
    pool['r45_contact_sheet'] = str(sheet)
    pool['r45_contact_sheet_sha256'] = sha(sheet)
    checkpoints = pool.setdefault('search_checkpoints_v01', [])
    checkpoint = dict(
        input='R45 USGS/Smithsonian marine fossil plate', date='2026-11-07',
        candidates_examined=3, active_minutes=16,
        budget_status='three-candidate limit reached; do not restart these three files',
        outcome=(
            'One licensed plate: NPS Pachydiscus kamishakensis, PD-USGov-NPS, '
            'Frank Ruggles, Katmai. It is one ammonite, not a fossil core. '
            'Two Yellowstone NPS photographs of Smithsonian USNM trilobites were '
            'not used: each frame is mostly a ruler and colour card, and the '
            'Blountia fossil does not read. si.edu blocked a direct Smithsonian '
            'download. Wildlife cuts are a different input.'),
        contact_sheet=str(rejected), contact_sheet_sha256=sha(rejected),
        admitted=ASSET,
        candidates=[
            dict(file='ammonite.jpg', sha256=SOURCE_SHA256,
                 source='https://commons.wikimedia.org/wiki/File:File-Photograph_of_the_ammonite_Pachydiscus-kamishakensis_from_the_Kaguyak_Formation._This-specimen_is_approximately_24_cm_wide_(0197c09f-9653-4f8c-83b2-69f55bb2c1de).jpg',
                 licence='PD-USGov-NPS', width=4256, height=2832,
                 result='Used. Real marine ammonite. Label, ruler and colour chart cropped off.'),
            dict(file='ehmania.jpg', sha256=REJECTED['ehmania.jpg'],
                 source='https://commons.wikimedia.org/wiki/File:USNM_90667_Ehmania_walcotti_trilobite_(30513613841).jpg',
                 licence='PD-USGov-NPS', width=4065, height=2340,
                 result='Smithsonian USNM 90667, Yellowstone NPS photo. Partial trilobite beside a ruler and checker. Not used.'),
            dict(file='blountia.jpg', sha256=REJECTED['blountia.jpg'],
                 source='https://commons.wikimedia.org/wiki/File:USNM_96488_Blountia_polita_trilobite_(30513613421).jpg',
                 licence='PD-USGov-NPS', width=3688, height=2811,
                 result='Smithsonian USNM 96488. The fossil is a small bump and does not read. Not used.'),
        ])
    if not any(item.get('input') == checkpoint['input'] for item in checkpoints):
        checkpoints.append(checkpoint)
    args.manifest.write_text(json.dumps(pool, indent=2) + '\n')
    polish_path = root / 'polish_r45.json'
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
    edit = args.manifest.parent
    check_path = edit / 'HARVEST_R45_FOSSIL_TECHNICAL_CHECK_v01.json'
    check_path.write_text(json.dumps(check, indent=2) + '\n')
    search_path = edit / 'HARVEST_R45_FOSSIL_SEARCH_v01.json'
    search_path.write_text(json.dumps(checkpoint, indent=2) + '\n')
    print(f'{ASSET} verified; plate {plate_record["sha256"][:12]} frames {FRAMES}')


if __name__ == '__main__':
    main()
