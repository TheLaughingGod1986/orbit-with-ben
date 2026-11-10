#!/usr/bin/env python3
"""Part 04 composition start frames — VO-literal see-chapter, teaspoon grammar."""
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
from _make_part02_v01_start_frames import remnant  # noqa: E402

OUT = HERE / "parts/starts_part04_v01"


def paint_sphere(
    im: Image.Image,
    cx: int,
    cy: int,
    r: int,
    rgb: tuple[int, int, int],
    light: tuple[float, float, float] = (-0.42, -0.50, 0.72),
) -> Image.Image:
    arr = np.array(im)
    yy, xx = np.mgrid[:H, :W]
    dx = (xx - cx).astype(np.float32) / r
    dy = (yy - cy).astype(np.float32) / r
    z2 = 1.0 - dx * dx - dy * dy
    mask = z2 > 0
    z = np.zeros((H, W), dtype=np.float32)
    z[mask] = np.sqrt(z2[mask])
    lx, ly, lz = light
    n = np.clip(lx * dx + ly * dy + lz * z, 0, 1)
    for i, base in enumerate(rgb):
        ch = arr[:, :, i].astype(np.float32)
        ch[mask] = np.clip(base * 0.12 + base * 0.88 * n[mask], 0, 255)
        arr[:, :, i] = ch
    return Image.fromarray(arr.astype(np.uint8))


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — cinema's lie: a dull 3D grey sphere in vacuum. NOT a flat UI disc.
    bg = clean_space(n_faint=0, seed=41)
    arr = np.array(bg)
    cx, cy, r = 960, 540, 220
    yy, xx = np.mgrid[:H, :W]
    dx = (xx - cx).astype(np.float32) / r
    dy = (yy - cy).astype(np.float32) / r
    z2 = 1.0 - dx * dx - dy * dy
    mask = z2 > 0
    z = np.zeros((H, W), dtype=np.float32)
    z[mask] = np.sqrt(z2[mask])
    n = np.clip(-0.42 * dx - 0.50 * dy + 0.72 * z, 0, 1)
    shade = 22 + 175 * n
    for c, add in enumerate((0, 1, 6)):
        ch = arr[:, :, c].astype(np.float32)
        ch[mask] = np.clip(shade[mask] + add, 0, 255)
        arr[:, :, c] = ch
    bg = Image.fromarray(arr.astype(np.uint8))
    save(bg, "01_grey_ball.png")

    # 02 — light as a traveller: one ray bending around a compact mass
    bg = clean_space(n_faint=0, seed=42)
    remnant(bg, 960, 540, 55)
    d = ImageDraw.Draw(bg)
    d.arc((520, 180, 1400, 900), start=200, end=340, fill=(255, 230, 160), width=10)
    d.arc((500, 160, 1420, 920), start=205, end=330, fill=(255, 210, 120), width=4)
    save(bg, "02_light_bends.png")

    # 03 — rays bent into your eyes: visor, the ray arriving
    bg = clean_space(n_faint=0, seed=43)
    d = ImageDraw.Draw(bg)
    d.line([(80, 200), (720, 520)], fill=(255, 220, 140), width=8)
    paste_scaled(bg, orbit, 1180, 620, 420)
    save(bg, "03_into_eyes.png")

    # 04 — ONE weary remnant as a clean sphere. No halo, no limb overlay
    # (Omni copies extras into a bulge / second disc).
    bg = clean_space(n_faint=0, seed=44)
    bg = paint_sphere(bg, 960, 540, 210, (148, 62, 48))
    save(bg, "04_redshifted_climb.png")

    # 05 — falling sky leans: light streaks, not oval galaxy sprites.
    bg = Image.new("RGB", (W, H), (3, 4, 8))
    d = ImageDraw.Draw(bg)
    for i in range(28):
        x0 = -200 + i * 80
        y0 = -40 + (i % 7) * 90
        col = 40 + (i * 7) % 90
        d.line([(x0, y0), (x0 + 1600, y0 + 720)], fill=(col, col + 8, min(255, col + 40)), width=2)
    save(bg.filter(ImageFilter.GaussianBlur(0.8)), "05_sky_leans.png")

    # 06 — GOLD: distant galaxies smear into arcs. NO Orbit.
    bg = clean_space(n_faint=0, seed=46)
    d = ImageDraw.Draw(bg)
    for i, col in enumerate(((180, 170, 210), (220, 200, 160), (160, 180, 230), (200, 160, 140))):
        d.arc((240 - i * 30, 160 - i * 20, 1680 + i * 30, 920 + i * 20), start=200, end=340, fill=col, width=7)
    remnant(bg, 960, 540, 28)
    save(bg, "06_smear_arcs.png")

    # 07 — complete photon ring; brightness blooms from off-frame right (circular, no clip plane).
    yy, xx = np.mgrid[:H, :W]
    ring_cx, ring_cy, ring_r = 520, 540, 210
    dist = np.sqrt((xx - ring_cx) ** 2 + (yy - ring_cy) ** 2)
    ring = np.exp(-((dist - ring_r) ** 2) / (2 * 16 ** 2))
    inner = np.exp(-((dist - (ring_r - 38)) ** 2) / (2 * 10 ** 2)) * 0.35
    src_x, src_y = 1640, 540
    dist_src = np.sqrt((xx - src_x) ** 2 + (yy - src_y) ** 2)
    wall = np.exp(-((dist_src / 430.0) ** 2) * 1.15)
    grad = np.zeros((H, W, 3), dtype=np.float32)
    grad[:, :, 0] = 8 + 70 * ring + 40 * inner + 210 * wall
    grad[:, :, 1] = 10 + 110 * ring + 70 * inner + 220 * wall
    grad[:, :, 2] = 16 + 160 * ring + 90 * inner + 235 * wall
    bg = Image.fromarray(np.clip(grad, 0, 255).astype(np.uint8))
    save(bg.filter(ImageFilter.GaussianBlur(1.6)), "07_wrong_crown.png")

    # 08 — pulsar lighthouse beam. Beam is the subject; Orbit small, banking away.
    bg = clean_space(n_faint=0, seed=48)
    remnant(bg, 640, 500, 40)
    d = ImageDraw.Draw(bg)
    d.polygon([(640, 500), (1920, 120), (1920, 880)], fill=(90, 140, 220))
    paste_scaled(bg, orbit, 420, 780, 110)
    save(bg, "08_pulsar_beam.png")

    # 09 — X-ray / charged-particle storm. Seeing is the least of your problems.
    bg = Image.new("RGB", (W, H), (8, 6, 12))
    d = ImageDraw.Draw(bg)
    for x0, y0, x1, y1, col, w in (
        (0, 80, 1920, 200, (180, 210, 255), 6),
        (0, 400, 1920, 520, (220, 160, 255), 8),
        (0, 700, 1920, 860, (255, 220, 180), 5),
        (200, 0, 700, 1080, (140, 200, 255), 4),
    ):
        d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    remnant(bg, 1600, 200, 22)
    save(bg, "09_xray_storm.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
