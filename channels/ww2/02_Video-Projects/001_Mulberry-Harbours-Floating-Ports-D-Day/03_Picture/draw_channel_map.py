"""G11 draft: code-drawn Channel geography and schematic tow connections.

Uses Natural Earth's public-domain country boundaries. Connections communicate
endpoints, NOT surveyed convoy tracks. Pass --video for a 12-second route build.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
SEA, LAND, INK, GOLD = '#cad9da', '#ece5d5', '#203436', '#a44e28'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
POINTS = {'Portsmouth': (-1.108, 50.80), 'Poole': (-1.98, 50.72),
          'Selsey': (-0.79, 50.73), 'Omaha': (-0.87, 49.37),
          'Arromanches': (-0.62, 49.34)}


def font(size):
    return ImageFont.truetype(FONT, size)


def xy(lon, lat):
    # Equirectangular with longitude scaled for central latitude 50 degrees.
    scale = 365
    return ((lon + 3.6) * math.cos(math.radians(50)) * scale + 200,
            (51.5 - lat) * scale + 70)


def base(geo):
    im = Image.new('RGB', (W, H), SEA)
    d = ImageDraw.Draw(im)
    for feature in geo['features']:
        geometry = feature['geometry']
        polygons = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
        for polygon in polygons:
            ring = polygon[0]
            if not any(-5 < p[0] < 4 and 48 < p[1] < 53 for p in ring):
                continue
            d.polygon([xy(*p[:2]) for p in ring], fill=LAND, outline='#8b9690', width=2)
    d.rectangle((0, 0, W, 140), fill=LAND)
    d.text((72, 35), 'THE HARBOURS CROSS THE CHANNEL', font=font(52), fill=INK)
    d.text((1450, 62), 'JUNE 1944', font=font(27), fill=INK)
    d.text((950, 570), 'ENGLISH CHANNEL', font=font(32), fill='#607b7d')
    d.text((1130, 200), 'ENGLAND', font=font(38), fill=INK)
    d.text((1200, 910), 'NORMANDY', font=font(38), fill=INK)
    return im


def frame(background, progress):
    im = background.copy()
    d = ImageDraw.Draw(im)
    for start, end in [('Poole', 'Omaha'), ('Portsmouth', 'Arromanches'), ('Selsey', 'Arromanches')]:
        a, b = xy(*POINTS[start]), xy(*POINTS[end])
        q = (a[0] + (b[0] - a[0]) * progress, a[1] + (b[1] - a[1]) * progress)
        d.line([a, q], fill=GOLD, width=6)
        if progress > 0:
            d.ellipse((q[0]-8, q[1]-8, q[0]+8, q[1]+8), fill=GOLD)
    offsets = {'Poole': (-100, -53), 'Portsmouth': (-140, -100),
               'Selsey': (10, -44), 'Omaha': (-175, 20), 'Arromanches': (24, 8)}
    for name, point in POINTS.items():
        x, y = xy(*point)
        d.ellipse((x-8, y-8, x+8, y+8), fill=INK)
        ox, oy = offsets[name]
        d.text((x+ox, y+oy), name, font=font(30), fill=INK, stroke_width=3, stroke_fill=LAND)
    x, y = xy(*POINTS['Omaha'])
    d.text((x-175, y+57), 'Mulberry A', font=font(25), fill=INK)
    x, y = xy(*POINTS['Arromanches'])
    d.text((x+24, y+48), 'Mulberry B', font=font(25), fill=INK)
    d.rectangle((0, H-72, W, H), fill=LAND)
    d.text((72, H-52), 'Schematic tow connections — not navigational tracks', font=font(25), fill=INK)
    d.text((1510, H-48), 'Natural Earth / own map', font=font(20), fill=INK)
    return im


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--geography', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--video', action='store_true')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    background = base(json.loads(a.geography.read_text()))
    frame(background, 1).save(a.out / 'code_graphic_ww2_001_G11_draft_v02.png')
    if a.video:
        command = ['ffmpeg', '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                   '-s', f'{W}x{H}', '-r', '25', '-i', '-', '-an', '-c:v', 'libx264',
                   '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                   str(a.out / 'code_graphic_ww2_001_G11_draft_v02.mp4')]
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        for n in range(300):
            progress = min(1, max(0, (n/25-1)/8))
            process.stdin.write(frame(background, progress).tobytes())
        process.stdin.close()
        if process.wait():
            raise RuntimeError('Map encode failed')


if __name__ == '__main__':
    main()
