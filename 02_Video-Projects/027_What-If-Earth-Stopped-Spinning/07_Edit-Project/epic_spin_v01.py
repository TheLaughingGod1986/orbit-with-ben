#!/usr/bin/env python3
"""027 frame 0: a smooth turning-Earth clip from one day of DSCOVR EPIC frames (NASA, public domain).

EPIC frames are ~65 min apart (~16 degrees of turn), too far apart for optical-flow interpolation (it smears
blocks) or a cross-blend (it double-exposes the continents). Instead each output frame is drawn on the sphere:
the two neighbouring EPIC frames are re-projected (orthographic) to the in-between sub-view longitude, then
blended with weights that favour the nearer frame and the disc centre. Land stays put; only clouds cross-fade.

EPIC looks from L1 at the sunlit face, so there is no moving day-night line: the motion is the continents
and clouds turning.

Usage: python epic_spin_v01.py [--day-dir /private/tmp/owb027_epic_v01/2025-06-21] [--fps 30] [--per 30]
       [--size 1080] [--disc 1000] --out <mp4>
Needs numpy + Pillow (~/.venvs/orbit-code-graphics). £0.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--day-dir", default="/private/tmp/owb027_epic_v01/2025-06-21")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--per", type=int, default=30, help="output frames per EPIC interval")
ap.add_argument("--size", type=int, default=1080)
ap.add_argument("--disc", type=int, default=1000, help="output disc diameter in px")
ap.add_argument("--src", type=int, default=1400, help="source frames resized to this before sampling")
ap.add_argument("--out", required=True)
a = ap.parse_args()

day = Path(a.day_dir)
meta = json.loads((day / "frames.json").read_text())
pngs = sorted(day.glob("*.png"))
assert len(pngs) == len(meta), (len(pngs), len(meta))


def load(p: Path):
    im = Image.open(p).convert("RGB").resize((a.src, a.src), Image.LANCZOS)
    arr = np.asarray(im, np.float32)
    lum = arr.mean(axis=2)
    ys, xs = np.nonzero(lum > 12)
    # the bright halo adds a little; the solid disc edge is ~1% inside the threshold box
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = (xs.max() - xs.min() + ys.max() - ys.min()) / 4 * 0.99
    return arr, cx, cy, r


src = [load(p) for p in pngs]
lat = np.radians([m["centroid_coordinates"]["lat"] for m in meta])
lon = np.unwrap(np.radians([m["centroid_coordinates"]["lon"] for m in meta]))

S, R = a.size, a.disc / 2
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
X = (xx - S / 2 + 0.5) / R
Y = -(yy - S / 2 + 0.5) / R
rho = np.sqrt(X * X + Y * Y)
inside = rho < 1.0
edge_aa = np.clip((1.0 - rho) * R, 0, 1)  # one-pixel antialiased limb
c = np.arcsin(np.clip(rho, 0, 1))
sinc, cosc = np.sin(c), np.cos(c)
rho_safe = np.where(rho == 0, 1e-9, rho)


def geo(phi0, lam0):
    """Output pixel -> (lat, lon) for a view centred on (phi0, lam0)."""
    la = np.arcsin(np.clip(cosc * np.sin(phi0) + Y * sinc * np.cos(phi0) / rho_safe, -1, 1))
    lo = lam0 + np.arctan2(X * sinc, rho_safe * cosc * np.cos(phi0) - Y * sinc * np.sin(phi0))
    return la, lo


def sample(k, la, lo):
    """Sample source frame k at (lat, lon); returns rgb and a visibility weight."""
    arr, cx, cy, r = src[k]
    phik, lamk = lat[k], lon[k]
    cosck = np.sin(phik) * np.sin(la) + np.cos(phik) * np.cos(la) * np.cos(lo - lamk)
    x = np.cos(la) * np.sin(lo - lamk)
    y = np.cos(phik) * np.sin(la) - np.sin(phik) * np.cos(la) * np.cos(lo - lamk)
    px = np.clip(cx + x * r - 0.5, 0, a.src - 1.001)
    py = np.clip(cy - y * r - 0.5, 0, a.src - 1.001)
    x0, y0 = px.astype(np.int32), py.astype(np.int32)
    fx, fy = (px - x0)[..., None], (py - y0)[..., None]
    rgb = (arr[y0, x0] * (1 - fx) * (1 - fy) + arr[y0, x0 + 1] * fx * (1 - fy)
           + arr[y0 + 1, x0] * (1 - fx) * fy + arr[y0 + 1, x0 + 1] * fx * fy)
    w = np.clip(cosck, 0, None) ** 2
    return rgb, w


W = S * 16 // 9
pad = (W - S) // 2
ff = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{S}",
     "-r", str(a.fps), "-i", "-", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
     "-pix_fmt", "yuv420p", a.out],
    stdin=subprocess.PIPE)
canvas = np.zeros((S, W, 3), np.uint8)
n = len(meta)
total = (n - 1) * a.per + 1
for f in range(total):
    i = min(f // a.per, n - 2)
    t = (f - i * a.per) / a.per
    phi0 = lat[i] + t * (lat[i + 1] - lat[i])
    lam0 = lon[i] + t * (lon[i + 1] - lon[i])
    la, lo = geo(phi0, lam0)
    c1, w1 = sample(i, la, lo)
    c2, w2 = sample(i + 1, la, lo)
    w1, w2 = w1 * (1 - t), w2 * t
    tot = w1 + w2
    rgb = (c1 * w1[..., None] + c2 * w2[..., None]) / np.where(tot == 0, 1, tot)[..., None]
    rgb = rgb * (edge_aa * inside)[..., None]
    canvas[:, pad:pad + S] = np.clip(rgb, 0, 255).astype(np.uint8)
    ff.stdin.write(canvas.tobytes())
    if f % 60 == 0:
        print(f"frame {f}/{total}", flush=True)
ff.stdin.close()
ff.wait()
print("wrote", a.out, total, "frames", f"{total / a.fps:.2f}s")
