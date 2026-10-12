#!/usr/bin/env python3
"""J0143 v02: Chief revision (12 Oct). Free generated ship plate (no text, no Orbit),
enlarged to >=40% of frame height, cyan blue-shift rim, same approved copy.
Usage: python3 this.py --source /path/024_ship_plate_j0143_v02.jpg --out /path/j0143_v02
Media stays local; META.json records source and output hashes. Chief reviews the art.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import _build_light_speed_thumbs_v01 as house

W, H = 1280, 720
ZOOM = 1.8
CROP = (290, 140, 290 + round(W / ZOOM), 140 + round(H / ZOOM))
BAND_BOTTOM = 260


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hull_mask(a):
    lum = a.mean(-1)
    sat = a.max(-1) - a.min(-1)
    m = ((lum > 110) & (sat < 80)).astype(np.uint8) * 255
    return Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))


def ship_box(a):
    """Rows/columns with solid hull coverage; lone stars and streaks don't reach the counts."""
    lum = a.mean(-1)
    sat = a.max(-1) - a.min(-1)
    m = ((lum > 70) & (sat < 110)).astype(np.uint8) * 255
    m = np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))) > 0
    m[:, :100] = False
    rows = np.where(m.sum(1) > 40)[0]
    cols = np.where(m.sum(0) > 14)[0]
    return [int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())]


def plate(source):
    src = Image.open(source).convert('RGB').crop(CROP).resize((W, H), Image.Resampling.LANCZOS)
    a = house.arr(src)
    mask = hull_mask(a)
    edge = Image.fromarray(np.clip(
        np.asarray(mask.filter(ImageFilter.MaxFilter(9)), float) - np.asarray(mask, float), 0, 255
    ).astype(np.uint8))
    tight = np.asarray(edge.filter(ImageFilter.GaussianBlur(3)), float)[..., None] / 255
    broad = np.asarray(mask.filter(ImageFilter.GaussianBlur(28)), float)[..., None] / 255
    cyan = np.array([70, 190, 255])
    out = house.screen(a, tight * cyan * 0.95 + broad * cyan * 0.45)
    return house.img(out), ship_box(a)


def words(im, lines, yellow):
    d = ImageDraw.Draw(im)
    f = house.font(115)
    cap = d.textbbox((0, 0), 'H', font=f)
    boxes = []
    for i, line in enumerate(lines):
        width = house.line_w(d, line, f)
        x = (W - width) / 2
        y = 39 + i * 108 - cap[1]
        assert width < W - 70
        house.draw_line(d, x + 3, y + 4, line, f, house.BLACK)
        if line.startswith('EARTH:'):
            house.draw_line(d, x, y, line, f, house.WHITE)
            prefix = 'EARTH: 7 '
            offset = sum(d.textlength(c, font=f) + house.TRACK for c in prefix)
            house.draw_line(d, x + offset, y, 'YEARS', f, house.YELLOW)
        else:
            house.draw_line(d, x, y, line, f, house.YELLOW if i == yellow else house.WHITE)
        boxes.append([round(x), 39 + i * 108 - 7, round(x + width), 39 + i * 108 + 82 + 7])
    assert max(b[3] for b in boxes) <= BAND_BOTTOM - 24
    return boxes


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    variants = [('answer', ['YOU: 1 YEAR', 'EARTH: 7 YEARS'], 1), ('tease', ['OUTRUN', 'EARTH’S CLOCK'], 0)]
    meta = {
        'job': 'J0143', 'version': 'v02', 'approval': 'pending Chief cover review',
        'source': str(args.source), 'source_sha256': sha(args.source),
        'source_credit': 'No-cost generated plate (Cursor image tool, 12 Oct 2026), no text, no Orbit; Chief OK 12 Oct 12:17Z for a free alternative ship plate. Not NASA imagery.',
        'crop': list(CROP), 'zoom': ZOOM,
        'script': 'light_speed_script_master_v02.md, opening paragraph',
        'answer_quote': 'You are gone for one year by your own watch. You land, and seven years have passed at home.',
        'variants': [],
    }
    paths = []
    for name, lines, yellow in variants:
        im, ship = plate(args.source)
        assert ship[1] >= BAND_BOTTOM, ship
        assert (ship[3] - ship[1]) >= 0.40 * H, ship
        boxes = words(im, lines, yellow)
        path = args.out / f'024_{name}_j0143_v02.jpg'
        im.save(path, quality=95, subsampling=0)
        paths.append(path)
        meta['variants'].append({'file': str(path), 'text': lines, 'sha256': sha(path), 'text_boxes': boxes,
                                 'cap_height': 82, 'ship_box': ship,
                                 'ship_height_share': round((ship[3] - ship[1]) / H, 3)})
    gate = Path(__file__).resolve().parents[3] / '00_Brand/Channel-Setup/tools/thumb_preview.py'
    result = subprocess.run([sys.executable, str(gate), 'long', *map(str, paths), '--out',
                             str(args.out / '024_j0143_v02_phone_sheet.jpg'), '--score'], capture_output=True, text=True)
    (args.out / 'SCORE.txt').write_text(result.stdout + result.stderr)
    (args.out / 'META.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n')
    print(result.stdout + result.stderr)
    print(json.dumps([v['ship_box'] for v in meta['variants']]))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
