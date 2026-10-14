#!/usr/bin/env python3
"""026 Nearest Star long thumbnails v01 (J0076, Cursor covering, 9 Oct 2026).

Brief: THUMB_BRIEF_v01.md. Text layout, font, colours and checks come from 024's builder
(THUMBNAIL_AND_TITLE_RULES.md §2/§2.A). Every plate is a real telescope image from the 026 pool; no Orbit,
no labelled frames (eso1702a carries constellation labels, so it is not used).

  python3 _build_nearest_star_thumbs_v01.py
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
POOL = HERE.parent / "07_Edit-Project" / "pool_v01"
OUT = HERE / "abc_v01"
TITLE = "How Far Is the Nearest Star?"

# key, slug, lines, hook, source, credit, crop (x0, y0, width as shares of the source), lift,
# subject circle on 1280x720, text pos
VARIANTS = [
    ("A", "you-cant-see-it", ["YOU CAN'T", "SEE IT"], "SEE IT", "proxima/potw1343a.jpg",
     "ESA/Hubble & NASA, Hubble image of Proxima Centauri (potw1343a, CC BY 4.0)", (0.16, 0.31, 0.50), 0.22,
     ("circle", 875, 375, 230), {"x_left": 40, "x_right": None, "y_top": 56}),
    ("B", "light-takes-4-years", ["LIGHT TAKES", "4 YEARS"], "4 YEARS", "proxima/GSFC_20171208_Archive_e000214.jpg",
     "NASA/ESA Hubble, Alpha Centauri A and B (GSFC e000214)", (0.0, 0.0, 1.0), 0.30,
     ("below", 300), {"x_left": 40, "x_right": None, "y_top": 30}),
    ("C", "900m-years-on-foot", ["900M YEARS", "ON FOOT"], "900M YEARS", "alphacen/eso1629i.jpg",
     "ESO/Digitized Sky Survey 2, the sky around Alpha Centauri and Proxima (eso1629i, CC BY 4.0)",
     (0.18, 0.12, 0.45), 0.0,
     ("circle", 375, 360, 210), {"x_left": None, "x_right": 1240, "y_top": 56}),
]


def plate(src: str, crop: tuple[float, float, float], lift: float) -> Image.Image:
    im = Image.open(POOL / src).convert("RGB")
    sw, sh = im.size
    cw = int(sw * crop[2])
    ch = cw * 9 // 16
    x0, y0 = int(sw * crop[0]), int(sh * crop[1])
    y0 = max(0, min(y0, sh - ch))
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    if lift:
        a = np.asarray(im).astype(np.float32)
        a = 255.0 * (a / 255.0) ** (1.0 - lift)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.15)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=45, threshold=3))


def main() -> int:
    plates_only = "--plates" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {"version": "v01", "job": "J0076", "brief": "THUMB_BRIEF_v01.md", "title": TITLE, "variants": []}
    paths = []
    for key, slug, lines, hook, src, credit, crop, lift, subj, pos in VARIANTS:
        im = plate(src, crop, lift)
        if plates_only:
            im.save(OUT / f"_plate_{key}.jpg", quality=90)
            print(key, "near_black", house.near_black(im))
            continue
        name = f"nearest_star_thumb_{key}_{slug}.jpg"
        info = house.place_text(im, lines, hook, subj, **pos)
        im.save(OUT / name, quality=94, optimize=True, subsampling=0)
        paths.append(OUT / name)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                                 "source": credit, "crop_share": list(crop), "lift": lift,
                                 "near_black": house.near_black(im), **info})
    if plates_only:
        return 0
    sheet = OUT / "nearest_star_thumbs_v01_small_size_check.jpg"
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
