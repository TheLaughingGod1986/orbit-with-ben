#!/usr/bin/env python3
"""Part 05 composition start frames — fold / last image / mismatch. No placeholder primitives."""
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
from _make_part04_v01_start_frames import paint_sphere  # noqa: E402

OUT = HERE / "parts/starts_part05_v01"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def gaussian_ring(cx: float, cy: float, r: float, sigma: float) -> np.ndarray:
    yy, xx = np.mgrid[:H, :W]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    return np.exp(-((dist - r) ** 2) / (2 * sigma ** 2))


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — universe FOLDS. Curved light, not oval galaxies.
    bg = Image.new("RGB", (W, H), (3, 4, 8))
    d = ImageDraw.Draw(bg)
    for i in range(18):
        y = 80 + i * 55
        d.arc((80 - i * 12, y - 220, 1840 + i * 12, y + 220), start=200, end=340, fill=(40 + i * 4, 50 + i * 3, 80 + i * 5), width=2)
    save(bg.filter(ImageFilter.GaussianBlur(1.1)), "01_universe_fold.png")

    # 02 — GOLD: warped starlight RING tightens. Complete ring, no clip plane.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    ring = gaussian_ring(960, 540, 250, 14)
    inner = gaussian_ring(960, 540, 218, 9) * 0.45
    arr[:, :, 0] = 30 + 180 * ring + 70 * inner
    arr[:, :, 1] = 40 + 200 * ring + 90 * inner
    arr[:, :, 2] = 70 + 220 * ring + 110 * inner
    save(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4)), "02_ring_tightens.png")

    # 03 — not a distant Sun: compact remnant WITH a crust. One sphere, no halo.
    bg = clean_space(n_faint=0, seed=53)
    bg = paint_sphere(bg, 960, 540, 200, (132, 118, 108))
    save(bg, "03_not_a_sun.png")

    # 04 — photon map rewriting. Light paths as arcs, not HUD, not ovals.
    bg = clean_space(n_faint=0, seed=54)
    d = ImageDraw.Draw(bg)
    for i, col in enumerate(((210, 190, 140), (160, 180, 220), (200, 160, 120))):
        d.arc((280 - i * 40, 140 - i * 18, 1640 + i * 40, 940 + i * 18), start=190, end=350, fill=col, width=5)
    save(bg.filter(ImageFilter.GaussianBlur(0.6)), "04_photon_map.png")

    # 05 — last clear image? Visor searching. Orbit is the subject.
    bg = clean_space(n_faint=0, seed=55)
    paste_scaled(bg, orbit, 960, 560, 520)
    save(bg, "05_last_image.png")

    # 06 — last honest photons from the galaxy BEHIND you. Soft band, not oval sprites.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[:H, :W]
    t = ((xx / W) * 0.35 + (yy / H) * 0.65) - 0.48
    band = np.exp(-(t ** 2) / (2 * 0.045 ** 2))
    arr[:, :, 0] = 18 + 90 * band
    arr[:, :, 1] = 20 + 95 * band
    arr[:, :, 2] = 28 + 120 * band
    save(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2)), "06_galaxy_behind.png")

    # 07 — ahead: magnetism and radiation erase a calm view.
    bg = Image.new("RGB", (W, H), (8, 4, 10))
    d = ImageDraw.Draw(bg)
    for x0, y0, x1, y1, col, w in (
        (400, 0, 1920, 420, (160, 90, 255), 7),
        (200, 200, 1920, 700, (90, 180, 255), 5),
        (0, 500, 1920, 1080, (255, 140, 80), 6),
    ):
        d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    save(bg.filter(ImageFilter.GaussianBlur(0.9)), "07_radiation_ahead.png")

    # 08 — for a fragile moment, eyes still work. Visor CU.
    bg = clean_space(n_faint=0, seed=58)
    paste_scaled(bg, orbit, 980, 540, 640)
    save(bg, "08_eyes_still_work.png")

    # 09 — mismatch: light still arrives; matter is already failing. One Orbit, tipping.
    bg = clean_space(n_faint=0, seed=59)
    d = ImageDraw.Draw(bg)
    d.line([(40, 160), (780, 500)], fill=(255, 220, 150), width=7)
    paste_scaled(bg, orbit, 1180, 640, 280)
    save(bg, "09_mismatch.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
