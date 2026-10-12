#!/usr/bin/env python3
"""J0152: Test & Compare thumbnail B for the live Saturn long `55AEQwvs36g` (no test armed or on record).

Live A is "HOW LONG?" over a close Saturn crop: a vague question that repeats the title (Packaging §2.B bans
both). B is "RINGS ARE FALLING" (FALLING yellow), the film's own chapter-card words, in a top band off the
subject. Existing plates only, no generation, no inpainting:
- NASA/JPL/Space Science Institute PIA06193 (Cassini natural-colour Saturn), already in the repo;
- NASA Apollo 17 Blue Marble as17-148-22727, to scale (Earth ~1/9.45 of Saturn's diameter), lower left.
Saturn and its rings are cut out of the black sky and laid on the house navy glow, so the frame stays under
the 30% near-black cap.

  ~/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/build_saturn_tc_b_j0152.py
Does not upload or touch Studio.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / "02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnail"))
import _build_light_speed_thumbs_v01 as house  # noqa: E402
import build_packaging_long_thumbs_j0133 as pack  # noqa: E402
from build_back_catalogue_tc_variants_j0099 import disk, paste_disk  # noqa: E402

W, H = house.W, house.H
VID = "55AEQwvs36g"
FILM = REPO / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings"
PLATE = FILM / "10_Shorts/monday_saturn_tease/PIA06193_orig.jpg"
OUT = Path(os.environ.get("J0152_OUT", str(Path.home() / "_desk/j0152")))
WORDS, YELLOW = ["RINGS", "ARE", "FALLING"], "FALLING"
# ring system in PIA06193, as fractions of the plate (outer ring tips, top of the north pole to the south limb)
SYS_BOX = (0.085, 0.185, 0.905, 0.83)
SYS_W, SYS_TOP = 1230, 175
SATURN_DIAM_FRAC = 0.356  # Saturn's disc width / plate width
# the night limb is darker than the sky threshold, so the disc is masked as an ellipse (cx, cy, rx, ry as plate fractions)
PLANET = (0.495, 0.50, 0.178, 0.311)


def blue_marble() -> Image.Image:
    p = OUT / "as17-148-22727_orig.jpg"
    if not p.exists():
        urllib.request.urlretrieve("https://images-assets.nasa.gov/image/as17-148-22727/as17-148-22727~orig.jpg", p)
    return Image.open(p).convert("RGB")


def build() -> tuple[Image.Image, dict]:
    plate = Image.open(PLATE).convert("RGB")
    pw, ph = plate.size
    x0, y0, x1, y1 = (round(f * d) for f, d in zip(SYS_BOX, (pw, ph, pw, ph)))
    sys_im = plate.crop((x0, y0, x1, y1))
    s = SYS_W / sys_im.width
    sys_im = sys_im.resize((SYS_W, round(sys_im.height * s)), Image.Resampling.LANCZOS)

    bg = house.img(house.glow_bg(W / 2, 430, 820, (22, 32, 68), (52, 76, 138), seed=21, stars=240))
    layer = Image.new("RGB", (W, H), 0)
    ox = (W - SYS_W) // 2
    layer.paste(sys_im, (ox, SYS_TOP))
    # body + rings opaque (shadowed ring and night limb included), black sky out
    lit = (np.asarray(layer.convert("L")) > 14).astype(np.uint8) * 255
    lit = cv2.morphologyEx(lit, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    filled = lit.copy()
    cv2.floodFill(filled, None, (0, H - 1), 128)
    mask = np.where(filled == 128, 0, 255).astype(np.uint8)
    cx, cy = ox + (PLANET[0] - SYS_BOX[0]) * pw * s, SYS_TOP + (PLANET[1] - SYS_BOX[1]) * ph * s
    rx, ry = PLANET[2] * pw * s, PLANET[3] * ph * s
    cv2.ellipse(mask, (round(cx), round(cy)), (round(rx), round(ry)), 0, 0, 360, 255, -1)
    mask = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(2))
    im = Image.composite(layer, bg, mask)

    saturn_px = SATURN_DIAM_FRAC * pw * s
    e_d = max(40, round(saturn_px / 9.45))
    e_sq, e_m = disk(blue_marble())
    halo = Image.new("L", (W, H), 0)
    ex, ey = 120, 610
    ImageDraw.Draw(halo).ellipse((ex - e_d, ey - e_d, ex + e_d, ey + e_d), fill=90)
    im = Image.composite(Image.new("RGB", (W, H), (120, 170, 255)), im, halo.filter(ImageFilter.GaussianBlur(12)))
    e_scale = paste_disk(im, e_sq, e_m, ex, ey, e_d)

    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=110)
    shade = shade.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)
    im = pack.grade(im, 95, lift=False)
    pack.band(im, WORDS, YELLOW)
    return im, {"saturn_px": round(saturn_px), "earth_px": e_d, "earth_scale": e_scale}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    im, geo = build()
    b = OUT / f"saturn_tc_B_rings-are-falling_{VID}.jpg"
    im.save(b, quality=94, optimize=True, subsampling=0)
    a = OUT / f"live_A_{VID}.jpg"
    if not a.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg", a)
    meta = {"job": "J0152", "video": VID, "title": "How Long Do Saturn's Rings Have Left?",
            "A_live": a.name, "A_text": "HOW LONG?", "B_new": b.name, "B_text": " ".join(WORDS), "yellow": YELLOW,
            "plates": ["NASA/JPL/Space Science Institute PIA06193 (Cassini natural colour)",
                       "NASA Apollo 17 Blue Marble (as17-148-22727), to scale"],
            **geo, "near_black": house.near_black(im),
            "near_black_live": house.near_black(Image.open(a).convert("RGB")),
            "kb": round(b.stat().st_size / 1024)}
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0 if meta["near_black"] <= 0.30 and meta["kb"] <= 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
