"""Build J2143 from saved plates; no generation or network. Media stays outside git.

python3 build_j2143.py --assets /Users/benjaminoats/_desk/j2143/assets --out <directory>
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('preview', ROOT / '00_Brand/Channel-Setup/tools/thumb_preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)
FONT = '/System/Library/Fonts/Supplemental/Arial Black.ttf'


def headline(plate, words, out):
    im = ImageOps.fit(Image.open(plate).convert('RGB'), (1280, 720), method=Image.Resampling.LANCZOS)
    # Exact house font; 82 px visible capitals = 11.4% of 720 px.
    font = ImageFont.truetype(FONT, 114)
    box = font.getbbox('H')
    glyph_height = box[3] - box[1]
    font = ImageFont.truetype(FONT, round(114 * 82 / glyph_height))
    widths = [font.getlength(w) for w in words]
    gap = font.getlength(' ')
    layer = Image.new('RGBA', (round(sum(widths) + gap + 20), 110))
    draw = ImageDraw.Draw(layer)
    x = 10
    for word, width, color in zip(words, widths, ['white', '#ffe600']):
        draw.text((x, 8), word, font=font, anchor='lt', fill=color, stroke_width=5, stroke_fill='#06101c')
        x += width + gap
    # Condense horizontally only if required; retain exact visible cap height.
    if layer.width > 1180:
        layer = layer.resize((1180, layer.height), Image.Resampling.LANCZOS)
    im.paste(layer, ((1280-layer.width)//2, 12), layer)
    im.save(out, quality=96, subsampling=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--assets', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    headline(args.assets/'A_clean_plate.png', ['COMPASS', 'REVERSED'], args.out/'031_A_compass_v03.jpg')
    headline(args.assets/'C_clean_plate.png', ['GLOBAL', 'AURORAS'], args.out/'031_C_bright_v03.jpg')
    # Single NASA photograph only: no compositing, generative editing or text.
    filters = 'scale=1280:-2,crop=1280:720:0:ih-oh,eq=saturation=3:gamma=1.1:brightness=0.015,hue=s=1.2'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(args.assets/'iss062e098264_source.jpg'),
                    '-vf', filters, '-frames:v', '1', '-q:v', '2', str(args.out/'031_B_real_v04.jpg')], check=True)
    records = []
    for path in sorted(args.out.glob('031_*.jpg')):
        record = preview.score(path, 'long')
        record.update(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size,
                      dimensions=list(Image.open(path).size))
        records.append(record)
    (args.out/'measurements.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(records, indent=2))
    if any(r['fails'] for r in records):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
