#!/usr/bin/env python3
"""023 Venus v05d rows 39a/39b (J0096, Ben's 5:38 note "Same with this one").

39a  330.90-334.60  the v02 split plate (ocean world | steam lid) with a label under each half, from the line:
                    "Way 2016: shallow oceans" | "Turbet 2021: a lid of steam". Labels fade in from 0.3 s.
39b  334.60-338.47  opens on Magellan's 0 deg E global (PIA00257) with Alpha Regio (22 S, 5 E) ringed, slow push
                    toward it, dissolves into PIA00215 (the eastern edge of Alpha Regio) with a 5% push, labelled
                    "Alpha Regio: Venus's oldest rock". PIA00271 (brief) is the north-polar view and PIA00104 the
                    180 deg E face; Alpha Regio is on neither.
Outputs (out of git): 04_Generated-Clips/01_Raw/plates_v03/venus_row39a_split_labelled_v03.mp4, ..._row39b_alpha_regio_v03.mp4
Usage: python3 _build_venus_v05d_rows39_v01.py [--stills DIR]
"""
import argparse, math, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / '04_Generated-Clips/01_Raw'
OUT = RAW / 'plates_v03'
POOL = HERE / 'nasa_pool_v01'
W, H, FPS = 1920, 1080, 30
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
BG, GOLD, WHITE = (5, 6, 10), (255, 201, 74), (244, 239, 230)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def label_layer(parts, cx, cy, size=54, alpha=1.0):
    """parts: [(text, colour)] on one line, centred on (cx, cy), on the house dark box (70% BG)."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if alpha <= 0.01:
        return layer
    f = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(layer)
    widths = [d.textlength(t, font=f) for t, _ in parts]
    tw = sum(widths)
    asc, desc = f.getmetrics()
    x0, y0 = cx - tw / 2, cy - (asc + desc) / 2
    pad = size * 0.32
    d.rounded_rectangle((x0 - pad, y0 - pad * 0.7, x0 + tw + pad, y0 + asc + desc + pad * 0.7), radius=pad * 0.8,
                        fill=BG + (int(255 * 0.7 * alpha),))
    x = x0
    for (t, c), w in zip(parts, widths):
        d.text((x, y0), t, font=f, fill=c + (int(255 * alpha),))
        x += w
    return layer


def encoder(path, n):
    path.parent.mkdir(parents=True, exist_ok=True)
    return sp.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                     '-i', '-', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt',
                     'yuv420p', str(path)], stdin=sp.PIPE)


def decode(path):
    raw = sp.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                 capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


# ----- 39a -----
def row39a():
    src = decode(RAW / 'plates_v02/venus_ch3_row39a_split_ocean_vs_steamlid_v02.mp4')
    out = OUT / 'venus_row39a_split_labelled_v03.mp4'
    enc = encoder(out, len(src))
    frames = []
    for i, fr in enumerate(src):
        a = ease((i / FPS - 0.3) / 0.5)
        im = Image.fromarray(fr).convert('RGBA')
        im.alpha_composite(label_layer([('Way 2016: ', GOLD), ('shallow oceans', WHITE)], W * 0.25, 1010, alpha=a))
        im.alpha_composite(label_layer([('Turbet 2021: ', GOLD), ('a lid of steam', WHITE)], W * 0.75, 1010, alpha=a))
        rgb = im.convert('RGB')
        enc.stdin.write(rgb.tobytes())
        frames.append(rgb)
    enc.stdin.close(); enc.wait()
    return out, frames


# ----- 39b -----
N39B = 120            # 4.0 s; the slot is 3.87 s
T_DISS0, T_DISS1 = 1.55, 2.05
GLOBE_PUSH = 2.2      # whole disc -> 3.2x by the end of the dissolve
# PIA00215 is a slanted strip: the left edge runs from x~30 (top) to x~465 (bottom). This box stays inside it.
TESS_CX, TESS_CY, TESS_W = 1670, 1280, 2200


def alpha_regio_xy(size):
    a = np.array(Image.open(POOL / 'harvest_v04/PIA00257.jpg').convert('L'))
    ys, xs = np.where(a > 20)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = (xs.max() - xs.min()) / 2
    lat, lon = math.radians(-22), math.radians(5)
    return cx + r * math.cos(lat) * math.sin(lon), cy - r * math.sin(lat), r


def crop_view(img, cx, cy, vw):
    vw = min(vw, img.size[0], img.size[1] * W / H)
    vh = vw * H / W
    cx = min(max(cx, vw / 2), img.size[0] - vw / 2)
    cy = min(max(cy, vh / 2), img.size[1] - vh / 2)
    box = (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2)
    return img.resize((W, H), Image.LANCZOS, box=box), box


def row39b():
    sq = Image.open(POOL / 'harvest_v04/PIA00257.jpg').convert('RGB')
    ax, ay, R = alpha_regio_xy(sq.size)
    gh = sq.size[1]
    gw = int(gh * W / H)
    g = Image.new('RGB', (gw, gh), (0, 0, 0))
    off = (gw - sq.size[0]) // 2
    g.paste(sq, (off, 0))
    ax += off
    t = Image.open(POOL / 'magellan_extra/PIA00215.jpg').convert('RGB')
    tw, th = t.size
    out = OUT / 'venus_row39b_alpha_regio_v03.mp4'
    enc = encoder(out, N39B)
    frames = []
    # globe: whole disc, pushing toward Alpha Regio (slow while the ring draws, then faster into the dissolve)
    v0w = gh * 1.0 * W / H
    for i in range(N39B):
        s = i / FPS
        u = ease(s / T_DISS1) ** 1.6
        vw = v0w / (1.0 + GLOBE_PUSH * u)
        cx = gw / 2 + (ax - gw / 2) * min(1.0, u * 1.2)
        cy = gh / 2 + (ay - gh / 2) * min(1.0, u * 1.2)
        gl, box = crop_view(g, cx, cy, vw)
        k = W / (box[2] - box[0])
        rx, ry, rr = (ax - box[0]) * k, (ay - box[1]) * k, R * 0.13 * k
        ring = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ra = ease((s - 0.25) / 0.5)
        if ra > 0:
            d = ImageDraw.Draw(ring)
            d.arc((rx - rr, ry - rr, rx + rr, ry + rr), -90, -90 + 360 * ra, fill=GOLD + (255,), width=7)
        gl = gl.convert('RGBA'); gl.alpha_composite(ring); gl = gl.convert('RGB')
        # tessera: 16:9 full-width crop, 5% push
        p = 1.0 + 0.05 * ease((s - T_DISS0) / (N39B / FPS - T_DISS0))
        te, _ = crop_view(t, TESS_CX, TESS_CY, TESS_W / p)
        m = ease((s - T_DISS0) / (T_DISS1 - T_DISS0))
        im = Image.blend(gl, te, m).convert('RGBA')
        im.alpha_composite(label_layer([('Alpha Regio: ', GOLD), ("Venus's oldest rock", WHITE)], W / 2, 1000,
                                       alpha=ease((s - (T_DISS1 + 0.1)) / 0.5)))
        rgb = im.convert('RGB')
        enc.stdin.write(rgb.tobytes())
        frames.append(rgb)
    enc.stdin.close(); enc.wait()
    return out, frames


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--stills', default=str(HERE))
    a = ap.parse_args()
    oa, fa = row39a()
    ob, fb = row39b()
    picks = [('39a 0.2s', fa[6]), ('39a 2.5s', fa[75]), ('39b 0.9s ring', fb[27]), ('39b 1.8s dissolve', fb[54]),
             ('39b 3.5s label', fb[105])]
    sheet = Image.new('RGB', (960 * 3, 560 * 2), BG)
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 24)
    for k, (name, im) in enumerate(picks):
        x, y = k % 3 * 960, k // 3 * 560
        sheet.paste(im.resize((960, 540)), (x, y))
        d.text((x + 8, y + 536), name, font=f, fill=WHITE)
    dst = Path(a.stills) / 'J0096_v05d_stills_part2_rows39.jpg'
    sheet.save(dst, quality=88)
    print(oa, ob, dst)
