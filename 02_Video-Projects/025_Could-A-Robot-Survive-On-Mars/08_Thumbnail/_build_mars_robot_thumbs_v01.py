#!/usr/bin/env python3
"""025 Mars robot long thumbnails v01 (J0066, Cursor covering, 9 Oct 2026).

Brief: THUMB_BRIEF_v01.md. Text layout, font, colours and checks come from 024's builder
(THUMBNAIL_AND_TITLE_RULES.md §2/§2.A). Every plate is a real NASA/JPL photo from the 025 pool; no Orbit.

  python3 _build_mars_robot_thumbs_v01.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "024_What-Happens-If-You-Travel-Near-Light-Speed" / "08_Thumbnail"))
import _build_light_speed_thumbs_v01 as house  # noqa: E402

W, H = house.W, house.H
REPO = HERE.parents[2]
POOL = HERE.parent / "07_Edit-Project" / "nasa_pool_v01"
OUT = HERE / "abc_v01"
TITLE = "Could a Robot Survive on Mars?"

# key, slug, lines, hook, source, crop (x0, y0, width as shares of the source), subject circle on 1280x720, text pos
VARIANTS = [
    ("A", "built-for-90-days", ["BUILT FOR", "90 DAYS"], "90 DAYS", "opp_deck/PIA07372.jpg",
     "NASA/JPL Opportunity self-portrait, sols 322-323 (PIA07372)", (0.06, 0.44, 0.58),
     ("circle", 860, 430, 290), {"x_left": 40, "x_right": None, "y_top": 56}),
    ("B", "planned-5-flew-72", ["PLANNED 5.", "FLEW 72"], "FLEW 72", "rover_work/PIA24542.jpg",
     "NASA/JPL Perseverance with Ingenuity, Wright Brothers Field (PIA24542)", (0.24, 0.14, 0.70),
     ("circle", 860, 430, 250), {"x_left": 40, "x_right": None, "y_top": 56}),
    ("C", "14-years-of-dust", ["14 YEARS", "OF DUST"], "14 YEARS", "opp_deck/PIA15115.jpg",
     "NASA/JPL dusty Opportunity self-portrait (PIA15115)", (0.13, 0.24, 0.58),
     ("circle", 820, 450, 260), {"x_left": 40, "x_right": None, "y_top": 56}),
]


def plate(src: str, crop: tuple[float, float, float]) -> Image.Image:
    im = Image.open(POOL / src).convert("RGB")
    sw, sh = im.size
    cw = int(sw * crop[2])
    ch = cw * 9 // 16
    x0, y0 = int(sw * crop[0]), int(sh * crop[1])
    y0 = min(y0, sh - ch)
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.15)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=45, threshold=3))


def main() -> int:
    plates_only = "--plates" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"version": "v01", "job": "J0066", "brief": "THUMB_BRIEF_v01.md", "title": TITLE, "variants": []}
    paths = []
    for key, slug, lines, hook, src, credit, crop, subj, pos in VARIANTS:
        im = plate(src, crop)
        name = f"mars_robot_thumb_{key}_{slug}.jpg"
        p = OUT / name
        if plates_only:
            im.save(OUT / f"_plate_{key}.jpg", quality=90)
            continue
        info = house.place_text(im, lines, hook, subj, **pos)
        im.save(p, quality=94, optimize=True, subsampling=0)
        paths.append(p)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                                 "source": credit, "crop_share": list(crop),
                                 "near_black": house.near_black(im), **info})
    if plates_only:
        return 0
    sheet = OUT / "mars_robot_thumbs_v01_small_size_check.jpg"
    subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
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
