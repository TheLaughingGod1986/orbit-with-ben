#!/usr/bin/env python3
"""024 light-speed long thumbnails v02 (J0049; Claude review of abc_v01, b4c06a1).

A and C passed and are copied from abc_v01 unchanged. Only B (YOU AGE SLOWER on iss071e439624) is rebuilt:
1. Grade in float from the original: crop and resize per channel in float, one gentle shadow curve,
   then dither once at the 8-bit quantise. No levels stretch and no warm floor band, so the land keeps
   its own dark-to-amber gradient without stepping.
2. Flares: the disc over the limb, the lower-left discs and the ISS module all sit left of x=2100 in the
   source and fall outside the tighter crop. The two discs in the sky above the limb (centres ~2536,577
   and ~2637,698, plus a partial at ~2670,96) are inside it and are removed by subtracting their
   low-frequency glow, which leaves the stars.
3. Crop tighter on the limb's apex (x>=2300) so the limb arcs through the frame and Earth fills the lower
   part; the black above the limb gets the graded star field, as A and C do.

Text, layout and rules unchanged from v01 (imported from it).

  python3 _build_light_speed_thumbs_v02.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_light_speed_thumbs_v01 as v01  # noqa: E402

W, H = v01.W, v01.H
SRC_DIR = HERE / "abc_v01"
OUT = HERE / "abc_v02"

CROP_X0 = 2300
CROP_W = 4928 - CROP_X0
CROP_H = CROP_W * 9 // 16
LIMB_AT = 0.42  # limb apex as a share of frame height
FLARES = [(2536, 577, 300), (2637, 698, 200), (2670, 96, 270)]  # source px: cx, cy, r
LAND_DISC = (2410, 1260, 245)  # faint disc on the land just under the limb, inside the crop
CURVE_S = 1.6


def _box(a: np.ndarray, r: int, axis: int) -> np.ndarray:
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis, dtype=np.float64)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return ((hi - lo) / (2 * r + 1)).astype(np.float32)


def gauss(a: np.ndarray, sigma: float) -> np.ndarray:
    """Three box passes per axis ~ a Gaussian of this sigma, in float (Pillow blurs only 8-bit)."""
    r = max(1, int(round((np.sqrt(4 * sigma * sigma + 1) - 1) / 2)))
    for axis in (0, 1):
        for _ in range(3):
            a = _box(a, r, axis)
    return a


def resize_f(a: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    return np.stack([np.asarray(Image.fromarray(a[..., c], "F").resize(size, Image.LANCZOS))
                     for c in range(a.shape[-1])], -1)


def remove_flares(a: np.ndarray) -> np.ndarray:
    hh, ww = a.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    m = np.zeros((hh, ww), np.float32)
    ring = np.zeros((hh, ww), bool)
    for cx, cy, r in FLARES:
        d = np.hypot(xx - cx, yy - cy)
        m = np.maximum(m, np.clip((r * 1.08 - d) / (r * 0.12), 0, 1))
        ring |= (d > r * 1.15) & (d < r * 1.4)
    sky = np.clip((860 - yy) / 120, 0, 1)  # fades out before the blue air above the limb (~y 900+)
    m *= sky
    bg = np.median(a[ring & (sky > 0.99)], axis=0)
    glow = np.clip(gauss(a, 14) - bg, 0, None)
    return a - glow * m[..., None]


def remove_disc_on_land(a: np.ndarray, cx: int, cy: int, r: int) -> np.ndarray:
    """Subtract a faint flare disc over textured land: fit the background along each row from just outside
    the disc, then take away the disc's median radial profile (flat body plus rim), keeping the texture."""
    y0, y1 = max(0, int(cy - 1.2 * r)), int(cy + 1.2 * r)
    x0, x1 = max(0, int(cx - 1.7 * r)), int(cx + 1.7 * r)
    sub = a[y0:y1, x0:x1].copy()
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    rho = np.hypot(xx - cx, yy - cy) / r
    bg = np.full_like(sub, np.nan)
    for i in range(sub.shape[0]):
        out = (rho[i] > 1.12) & (rho[i] < 1.7)
        if out.sum() < 20:
            continue
        xs = xx[i, out]
        for c in range(3):
            k, b = np.polyfit(xs, sub[i, out, c], 1)
            bg[i, :, c] = k * xx[i] + b
    resid = sub - bg
    edges = np.linspace(0, 1.12, 57)
    mids = (edges[:-1] + edges[1:]) / 2
    prof = np.zeros((len(mids), 3), np.float32)
    for j in range(len(mids)):
        sel = (rho >= edges[j]) & (rho < edges[j + 1]) & np.isfinite(resid[..., 0])
        if sel.sum() > 30:
            prof[j] = np.median(resid[sel], axis=0)
    prof = np.clip(prof, 0, None)
    taper = np.clip((1.12 - rho) / 0.06, 0, 1)
    flare = np.stack([np.interp(rho, mids, prof[:, c]) for c in range(3)], -1) * taper[..., None]
    a = a.copy()
    a[y0:y1, x0:x1] = sub - flare
    return a


def curve(x: np.ndarray) -> np.ndarray:
    """Shadow lift that eases back to identity at white, so the limb's white doesn't spread into the land.
    Monotonic while CURVE_S < 3."""
    return x + CURVE_S * x * (1 - x) ** 2


def variant_b() -> tuple[Image.Image, tuple]:
    src = np.asarray(Image.open(v01.LIMB).convert("RGB"), np.float32) / 255
    src = remove_flares(src)
    src = remove_disc_on_land(src, *LAND_DISC)
    lum = src.mean(-1)
    limb_y = int(np.median(lum[:, CROP_X0:CROP_X0 + 800].argmax(0)))
    y0 = max(0, limb_y - int(CROP_H * LIMB_AT))
    crop = src[y0:y0 + CROP_H, CROP_X0:CROP_X0 + CROP_W]
    a = resize_f(crop, (W, H))
    a = np.clip(a, 0, 1)
    a = curve(a)
    l = a.mean(-1, keepdims=True)
    a = l + (a - l) * 1.10

    # star field above the limb, following its curve column by column
    out_l = a.mean(-1)
    limb_rows = gauss(out_l.argmax(0).astype(np.float32)[None, :, None], 20)[0, :, 0]
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    above = np.clip((limb_rows[None] - 20 - yy) / 140, 0, 1)[..., None]
    sky = v01.glow_bg(W * 0.60, H * 0.15, W * 0.80, (10, 18, 40), (44, 84, 150), seed=242, stars=200) / 255
    a = 1 - (1 - a) * (1 - sky * above)

    rng = np.random.default_rng(2442)
    dither = (rng.random(a.shape) - rng.random(a.shape)).astype(np.float32)
    out8 = np.clip(a * 255 + dither, 0, 255).round().astype(np.uint8)
    out = Image.fromarray(out8)
    land = Image.fromarray((np.clip((yy - limb_rows[None] - 60) / 40, 0, 1) * 255).astype(np.uint8))
    out = Image.composite(out.filter(ImageFilter.MedianFilter(3)), out, land)  # sensor specks on the night land
    out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=3))
    subj_top = int(limb_rows.min()) - 30
    return out, ("below", subj_top)


def earth_share(im: Image.Image, subj_top: int) -> float:
    return round(1 - subj_top / H, 3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta_v01 = json.loads((SRC_DIR / "META.json").read_text())
    meta = {"version": "v02", "job": "J0049", "brief": "THUMB_BRIEF_v01.md",
            "review": "Claude on abc_v01 (b4c06a1): A and C pass; B regraded, flares out, tighter crop",
            "title": meta_v01["title"], "variants": []}
    paths = []
    for key, slug, lines, hook in v01.VARIANTS:
        name = f"light_speed_thumb_{key}_{slug}.jpg"
        p = OUT / name
        if key != "B":
            shutil.copy2(SRC_DIR / name, p)
            meta["variants"].append({**next(v for v in meta_v01["variants"] if v["key"] == key),
                                     "copied_from": "abc_v01"})
        else:
            base, subj = variant_b()
            im = base.copy()
            info = v01.place_text(im, lines, hook, subj, x_right=None, x_left=48, y_top=52)
            im.save(p, quality=94, optimize=True, subsampling=0)
            meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                                     "source": "NASA ISS orbital sunrise (iss071e439624)",
                                     "crop_src_px": [CROP_X0, CROP_W, CROP_H],
                                     "earth_share": earth_share(im, subj[1]),
                                     "near_black": v01.near_black(im), **info})
        paths.append(p)
    sheet = OUT / "light_speed_thumbs_v02_small_size_check.jpg"
    subprocess.run([sys.executable, str(v01.REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
