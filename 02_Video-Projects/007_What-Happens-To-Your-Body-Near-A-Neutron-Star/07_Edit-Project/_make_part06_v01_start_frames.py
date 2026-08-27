#!/usr/bin/env python3
"""Part 06 composition start frames — Feel chapter, physics-led, not gore."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _make_part01_v08_start_frames import (  # noqa: E402
    FRONT,
    H,
    W,
    clean_space,
    crop_orbit,
    paste_scaled,
)

OUT = HERE / "parts/starts_part06_v01"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — uniform field: floating. Calm. One Orbit, no remnant.
    bg = clean_space(n_faint=0, seed=61)
    paste_scaled(bg, orbit, 960, 540, 220)
    save(bg, "01_float_uniform.png")

    # 02 — not uniform over HEIGHT. Orbit tall in frame: underside vs antenna.
    bg = clean_space(n_faint=0, seed=62)
    paste_scaled(bg, orbit, 960, 540, 380)
    save(bg, "02_over_height.png")

    # 03 — nearer side outruns farther. Gradient pull toward bottom.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    pull = yy ** 1.6
    arr[:, :, 0] = 8 + 40 * pull
    arr[:, :, 2] = 12 + 55 * pull
    bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    paste_scaled(bg, orbit, 960, 500, 260)
    save(bg, "03_nearer_outruns.png")

    # 04 — GOLD: the tide. Stretch along one axis. One Orbit, one face.
    bg = clean_space(n_faint=0, seed=64)
    stretched = orbit.resize((int(orbit.width * 0.55), int(orbit.height * 1.55)), Image.Resampling.LANCZOS)
    paste_scaled(bg, stretched, 960, 540, 420)
    save(bg, "04_the_tide.png")

    # 05 — crushed or too fast? Visor question.
    bg = clean_space(n_faint=0, seed=65)
    paste_scaled(bg, orbit, 980, 540, 560)
    save(bg, "05_crushed_or_fast.png")

    # 06 — structures fail / chemistry fails. Lattice cracking. No gore, no Orbit.
    bg = Image.new("RGB", (W, H), (10, 8, 12))
    d = ImageDraw.Draw(bg)
    for i in range(0, W, 70):
        d.line([(i, 0), (i + 40, H)], fill=(70, 80, 110), width=2)
    for j in range(0, H, 70):
        d.line([(0, j), (W, j + 30)], fill=(50, 60, 90), width=2)
    d.line([(200, 200), (900, 860)], fill=(180, 190, 220), width=4)
    d.line([(1100, 80), (1700, 980)], fill=(160, 140, 200), width=3)
    save(bg.filter(ImageFilter.GaussianBlur(0.6)), "06_structures_fail.png")

    # 07 — one second. A single bright tick of time — not a HUD clock.
    bg = clean_space(n_faint=0, seed=67)
    yy, xx = np.mgrid[:H, :W]
    dist = np.sqrt((xx - 960.0) ** 2 + (yy - 540.0) ** 2)
    flash = np.exp(-(dist / 90.0) ** 2)
    arr = np.array(bg, dtype=np.float32)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + 220 * flash, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + 210 * flash, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + 180 * flash, 0, 255)
    save(Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), "07_one_second.png")

    # 08 — where that second is spent. Distance as a soft radial well. Tiny Orbit far, no remnant hang.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[:H, :W]
    dist = np.sqrt((xx - 1680.0) ** 2 + (yy - 540.0) ** 2)
    well = np.exp(-((dist / 520.0) ** 2) * 1.1)
    arr[:, :, 0] = 6 + 80 * well
    arr[:, :, 1] = 8 + 70 * well
    arr[:, :, 2] = 14 + 110 * well
    bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    paste_scaled(bg, orbit, 280, 720, 90)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "08_where_spent.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
