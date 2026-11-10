#!/usr/bin/env python3
"""J0099 items 2-3: Test & Compare variants for two live longs (thumb audit 9 Oct, items 5 and 6).

- Moon `2fsQcea-voM`: full-bleed Earth-Moon, "3.8 CM / A YEAR". Apollo 17 Blue Marble (as17-148-22727)
  low left as the scale reference, Apollo 11 trans-Earth full Moon (as11-44-6667) small and far, upper right.
- Alien Worlds `b8-X_FyJnHM`: the real-planet artwork for HD 189733b (NASA, ESA, M. Kornmesser;
  GSFC_20171208_Archive_e001427), "RAINS / GLASS".

Text, font and checks come from 024's house builder. Plates download from images.nasa.gov into WORK.
Slot A of each test is the live thumbnail (i.ytimg maxres), fetched next to the variant.
Does not upload; adding the test is a separate Studio step (CDP 9223).

  python3 00_Brand/Channel-Setup/tools/build_back_catalogue_tc_variants_j0099.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnail"))
import _build_light_speed_thumbs_v01 as house  # noqa: E402

W, H = house.W, house.H
WORK = Path(os.environ.get("J0099_WORK", "/tmp/j0099"))
OUT = Path(os.environ.get("J0099_TC_OUT", str(Path.home() / "_desk/j0099/tc")))


def nasa(nasa_id: str, kind: str = "orig") -> Image.Image:
    p = WORK / "nasa" / f"{nasa_id}_{kind}.jpg"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        urllib.request.urlretrieve(f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~{kind}.jpg", p)
    return Image.open(p).convert("RGB")


def live(vid: str) -> Path:
    p = OUT / f"live_A_{vid}.jpg"
    if not p.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", p)
    return p


def disk(im: Image.Image, thresh: int = 28) -> tuple[Image.Image, Image.Image]:
    """Crop a lit body off a black sky; returns the square crop and a feathered round mask."""
    lit = np.asarray(im.convert("L").filter(ImageFilter.MedianFilter(9))) > thresh
    xs = np.where(lit.sum(axis=0) > lit.shape[0] * 0.04)[0]
    ys = np.where(lit.sum(axis=1) > lit.shape[1] * 0.04)[0]
    r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2
    cx, cy = xs.max() - r, (ys.min() + ys.max()) / 2  # night side to the left: anchor on the lit limb
    box = tuple(int(v) for v in (cx - r, cy - r, cx + r, cy + r))
    sq = im.crop(box)
    m = Image.new("L", sq.size, 0)
    ImageDraw.Draw(m).ellipse((2, 2, sq.size[0] - 3, sq.size[1] - 3), fill=255)
    return sq, m.filter(ImageFilter.GaussianBlur(max(1, sq.size[0] // 400)))


def paste_disk(base: Image.Image, sq: Image.Image, m: Image.Image, cx: int, cy: int, d: int) -> float:
    s = sq.resize((d, d), Image.LANCZOS)
    base.paste(s, (cx - d // 2, cy - d // 2), m.resize((d, d), Image.LANCZOS))
    return round(d / sq.size[0], 2)


def moon_variant() -> tuple[Image.Image, tuple, dict]:
    bg = house.glow_bg(330, 560, 1150, (14, 20, 44), (46, 78, 140), seed=13, stars=260)
    im = house.img(bg)
    e_sq, e_m = disk(nasa("as17-148-22727"))
    m_sq, m_m = disk(nasa("as11-44-6667"))
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((330 - 610, 1000 - 610, 330 + 610, 1000 + 610), fill=150)
    halo = halo.filter(ImageFilter.GaussianBlur(38))
    im = Image.composite(Image.new("RGB", (W, H), (120, 170, 255)), im, halo)
    e_scale = paste_disk(im, e_sq, e_m, 330, 1000, 1180)
    m_scale = paste_disk(im, m_sq, m_m, 1015, 285, 300)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    src = {"plates": ["NASA Apollo 17 Blue Marble (as17-148-22727)",
                      "NASA Apollo 11 full Moon, trans-Earth coast (as11-44-6667)"],
           "scale": {"earth": e_scale, "moon": m_scale}}
    return im, ("circle", 1015, 285, 150), src


def alien_variant() -> tuple[Image.Image, tuple, dict]:
    p_sq, p_m = disk(nasa("GSFC_20171208_Archive_e001427"), thresh=22)
    bg = house.glow_bg(300, 400, 900, (10, 16, 40), (34, 60, 120), seed=7, stars=240)
    im = house.img(bg)
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((300 - 560, 400 - 560, 300 + 560, 400 + 560), fill=140)
    halo = halo.filter(ImageFilter.GaussianBlur(34))
    im = Image.composite(Image.new("RGB", (W, H), (90, 150, 255)), im, halo)
    scale = paste_disk(im, p_sq, p_m, 300, 400, 1040)
    im = ImageEnhance.Color(im).enhance(1.08)
    src = {"plates": ["NASA, ESA, M. Kornmesser: HD 189733b artist's impression "
                      "(GSFC_20171208_Archive_e001427, 'NASA Hubble Finds a True Blue Planet')"],
           "scale": {"planet": scale}}
    return im, ("circle", 300, 400, 520), src


VARIANTS = [
    {"vid": "2fsQcea-voM", "title": "Why the Moon Is Slowly Leaving Us", "build": moon_variant,
     "lines": ["3.8 CM", "A YEAR"], "hook": "3.8 CM", "pos": {"x_left": 48, "x_right": None, "y_top": 52},
     "file": "moon_tc_B_3-8-cm-a-year.jpg"},
    {"vid": "b8-X_FyJnHM", "title": "Alien Worlds: The Strangest Planets We've Ever Found", "build": alien_variant,
     "lines": ["RAINS", "GLASS"], "hook": "GLASS", "pos": {"x_left": None, "x_right": W - 40, "y_top": 60},
     "file": "alien_tc_B_rains-glass.jpg"},
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, sheets_in = [], []
    for v in VARIANTS:
        im, subj, src = v["build"]()
        info = house.place_text(im, v["lines"], v["hook"], subj, **v["pos"])
        p = OUT / v["file"]
        im.save(p, quality=94, optimize=True, subsampling=0)
        a = live(v["vid"])
        rows.append({"video": v["vid"], "title": v["title"], "A_live": a.name, "B_new": p.name,
                     "text": " ".join(v["lines"]), "yellow": v["hook"], **src,
                     "near_black": house.near_black(im), "near_black_live": house.near_black(Image.open(a).convert("RGB")),
                     "kb": round(p.stat().st_size / 1024), **info})
        sheets_in += [a, p]
    subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "long",
                    *map(str, sheets_in), "--out", str(OUT / "tc_variants_small_size_check.jpg")], check=True)
    (OUT / "META.json").write_text(json.dumps({"job": "J0099", "items": [2, 3], "variants": rows}, indent=2) + "\n")
    print(json.dumps(rows, indent=2))
    bad = [r["video"] for r in rows if r["near_black"] > 0.30 or r["kb"] > 2000]
    if bad:
        print(f"near-black over 30% or file over 2 MB: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
