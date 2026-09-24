#!/usr/bin/env python3
"""Monday Moon Short cover. Eclipse plate, yellow hook, centre stack."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, "/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/tools")
import build_yellow_white_short_thumbs_v04 as t4

HERE = Path(__file__).resolve().parent
PLATE = HERE / "sun.jpg"
OUT = HERE / "monday_moon_thumb.jpg"
CROP = HERE / "monday_moon_thumb_16x9.jpg"


def main() -> None:
    src = Image.open(PLATE).convert("RGB")
    w, h = src.size
    # Tight on the black Moon and the fire ring so the disc reads on a phone.
    cx, cy = w // 2, h // 2
    tight = src.crop((cx - 280, cy - 500, cx + 280, cy + 500))
    tight = tight.resize((t4.W, t4.H), Image.Resampling.LANCZOS)
    plate = HERE / "_plate.jpg"
    tight.save(plate, quality=95)
    job = {
        "id": "monday-moon",
        "plate": plate,
        "out_dir": HERE,
        "lines": ["THE MOON", "LEAVING US"],
        "yellow": {"LEAVING"},
        "hero": 1,
        "related": "2fsQcea-voM",
        "uk": "2026-10-05T11:30:00+01:00",
        "role": "monday_moon",
    }
    # compose() names the file cover_<id>.jpg
    t4.compose(job)
    cover = HERE / "cover_monday-moon.jpg"
    im = Image.open(cover).convert("RGB")
    im.save(OUT, quality=93, optimize=True)
    # 16:9 centre crop of the 9:16 thumb.
    crop_h = int(t4.W * 9 / 16)
    y0 = (t4.H - crop_h) // 2
    im.crop((0, y0, t4.W, y0 + crop_h)).save(CROP, quality=90)
    rgb = np.asarray(im)
    yellow = (rgb[:, :, 0] > 220) & (rgb[:, :, 1] > 180) & (rgb[:, :, 2] < 80)
    white = (rgb[:, :, 0] > 230) & (rgb[:, :, 1] > 230) & (rgb[:, :, 2] > 230)
    if yellow.sum() < 200:
        raise SystemExit("yellow hook missing")
    if white.sum() < 200:
        raise SystemExit("white type missing")
    # Both lines must sit inside the crop with a margin.
    ys, xs = np.where(yellow | white)
    top, bot = int(ys.min()), int(ys.max())
    left, right = int(xs.min()), int(xs.max())
    margin = 28
    if top < y0 + margin or bot > y0 + crop_h - margin:
        raise SystemExit(f"type clipped by 16:9 crop y {top}-{bot} band {y0}-{y0+crop_h}")
    if left < margin or right > t4.W - margin:
        raise SystemExit(f"type clipped on x {left}-{right}")
    print("ok", OUT, "type", left, top, right, bot, "crop", y0, y0 + crop_h)


if __name__ == "__main__":
    main()
