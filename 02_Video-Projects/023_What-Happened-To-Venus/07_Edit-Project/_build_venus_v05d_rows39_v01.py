#!/usr/bin/env python3
"""023 Venus v05d rows 39a/39b (J0096, Ben's 5:38 note "Same with this one").

39a  330.90-334.60  the v02 split plate (ocean world | steam lid) with a label under each half, from the line:
                    "Way 2016: shallow oceans" | "Turbet 2021: a lid of steam". Labels fade in from 0.3 s.
39b  334.60-338.47  opens on Magellan's 0 deg E global (PIA00257) with Alpha Regio (22 S, 5 E) ringed, slow push
                    toward it, dissolves into PIA00147 (the Alpha Regio ridged upland, gaps filled) with a 5% push, labelled
                    "Alpha Regio: Venus's oldest rock". PIA00271 (brief) is the north-polar view and PIA00104 the
                    180 deg E face; Alpha Regio is on neither.
Round 2 (Chief, 10 Oct): labels at house size (100 px, two lines), near-black lifted onto a graded backdrop.
Outputs (out of git): 04_Generated-Clips/01_Raw/plates_v04/venus_row39a_split_labelled_v04.mp4, ..._row39b_alpha_regio_v04.mp4
Usage: python3 _build_venus_v05d_rows39_v01.py [--stills DIR]
"""
import argparse, math, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / '04_Generated-Clips/01_Raw'
OUT = RAW / 'plates_v04'
POOL = HERE / 'nasa_pool_v01'
W, H, FPS = 1920, 1080, 30
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
BG, GOLD, WHITE = (5, 6, 10), (255, 201, 74), (244, 239, 230)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


LABEL_PX = 100       # house type: ~11-12% of frame height per line (Chief, 10 Oct: 54 px read at 4-5%)


def label_layer(lines, cx, y_bottom, size=LABEL_PX, alpha=1.0):
    """lines: [(text, colour)], one per line, centred on cx, the last line's box ending at y_bottom, on the house
    dark box (70% BG)."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if alpha <= 0.01:
        return layer
    f = ImageFont.truetype(FONT, size)
    d = ImageDraw.Draw(layer)
    asc, desc = f.getmetrics()
    lh = asc + desc
    pad = size * 0.22
    tw = max(d.textlength(t, font=f) for t, _ in lines)
    y0 = y_bottom - pad - lh * len(lines)
    d.rounded_rectangle((cx - tw / 2 - pad, y0 - pad, cx + tw / 2 + pad, y_bottom), radius=pad,
                        fill=BG + (int(255 * 0.7 * alpha),))
    for k, (t, c) in enumerate(lines):
        d.text((cx - d.textlength(t, font=f) / 2, y0 + k * lh), t, font=f, fill=c + (int(255 * alpha),))
    return layer


BACKDROP = None


def graded_backdrop():
    """Deep warm-to-slate radial grade (luma ~32-60) laid under near-black space, so no frame is mostly black."""
    global BACKDROP
    if BACKDROP is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.clip(np.hypot((xx - W / 2) / (W * 0.6), (yy - H * 0.45) / (H * 0.75)), 0, 1)[..., None]
        BACKDROP = (np.array([74, 56, 50], np.float32) * (1 - r) + np.array([34, 32, 46], np.float32) * r)
    return BACKDROP


def lift_black(fr, thr=40.0):
    """Blend the backdrop in where the plate is near-black; lit subjects keep their own pixels."""
    f = fr.astype(np.float32)
    w = np.clip(1 - f.max(axis=2, keepdims=True) / thr, 0, 1)
    return np.clip(f * (1 - w) + graded_backdrop() * w + f * w, 0, 255).astype(np.uint8)


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
    out = OUT / 'venus_row39a_split_labelled_v04.mp4'
    enc = encoder(out, len(src))
    frames = []
    for i, fr in enumerate(src):
        a = ease((i / FPS - 0.3) / 0.5)
        im = Image.fromarray(lift_black(fr)).convert('RGBA')
        im.alpha_composite(label_layer([('Way 2016', GOLD), ('shallow oceans', WHITE)], W * 0.25, 1060, alpha=a))
        im.alpha_composite(label_layer([('Turbet 2021', GOLD), ('a lid of steam', WHITE)], W * 0.75, 1060, alpha=a))
        rgb = im.convert('RGB')
        enc.stdin.write(rgb.tobytes())
        frames.append(rgb)
    enc.stdin.close(); enc.wait()
    return out, frames


# ----- 39b -----
N39B = 120            # 4.0 s; the slot is 3.87 s
T_DISS0, T_DISS1 = 1.55, 2.05
GLOBE_PUSH = 2.2      # whole disc -> 3.2x by the end of the dissolve
# PIA00147 (3584 sq, Magellan false colour of the Alpha Regio upland) has slanted black data gaps on its left
# two-thirds; this box sits right of them on the ridged tessera (1.37x up). PIA00215 is the pancake domes, already at 15b/49.
TESS_CX, TESS_CY, TESS_W = 2660, 1520, 1400


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
    t = np.array(Image.open(POOL / 'magellan_extra/PIA00147.jpg').convert('RGB'))
    gap = (t.max(axis=2) < 18).astype(np.uint8) * 255       # small data-gap dashes inside the box: fill from around them
    gap = np.array(Image.fromarray(gap).filter(ImageFilter.MaxFilter(9))) > 0
    fill = np.array(Image.fromarray(t).filter(ImageFilter.MedianFilter(31)))
    t[gap] = fill[gap]
    t = Image.fromarray(t)
    out = OUT / 'venus_row39b_alpha_regio_v04.mp4'
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
        gl = Image.fromarray(lift_black(np.array(gl))).convert('RGBA'); gl.alpha_composite(ring); gl = gl.convert('RGB')
        # tessera: 16:9 full-width crop, 5% push
        p = 1.0 + 0.05 * ease((s - T_DISS0) / (N39B / FPS - T_DISS0))
        te, _ = crop_view(t, TESS_CX, TESS_CY, TESS_W / p)
        m = ease((s - T_DISS0) / (T_DISS1 - T_DISS0))
        im = Image.blend(gl, te, m).convert('RGBA')
        im.alpha_composite(label_layer([('Alpha Regio', GOLD), ("Venus's oldest rock", WHITE)], W / 2, 1060,
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
    dst = Path(a.stills) / 'J0096_v05d_stills_round2_rows39.jpg'
    sheet.save(dst, quality=88)
    print(oa, ob, dst)
