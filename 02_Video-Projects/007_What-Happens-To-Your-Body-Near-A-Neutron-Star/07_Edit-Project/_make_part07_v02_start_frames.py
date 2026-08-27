#!/usr/bin/env python3
"""Part 07 v02 start frames — compact glowing remnant, never a grey moon wall.

Omni copies the start frame. Grey crater terrain became Death Star greebles.
These starts composite locked Omni remnant stills (Parts 01/04/05) + identity Orbit.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageFilter
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

OUT = HERE / "parts/starts_part07_v02"
REF = HERE / "parts/_ref_locked_remnant"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def fit(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    return im.resize((W, H), Image.Resampling.LANCZOS)


def star_crop(src: Image.Image) -> Image.Image:
    """Right-hand remnant from the locked compact-star still. Drop the old Orbit."""
    w, h = src.size
    # Original compact is 1280x720: Orbit left, glowing sphere right.
    left = int(w * 0.64)
    return src.crop((left, 0, w, h))


def paste_star_fit(bg: Image.Image, star: Image.Image, cx: int, cy: int, height_px: int) -> None:
    ratio = height_px / star.height
    nw, nh = max(2, int(star.width * ratio)), max(2, height_px)
    piece = star.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(piece, (int(cx - nw / 2), int(cy - nh / 2)))


def wash(seed: int, rgb: tuple[float, float, float], side: str = "right") -> Image.Image:
    rng = np.random.RandomState(seed)
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    if side == "right":
        t = np.clip((xx - 700.0) / 1100.0, 0, 1) ** 1.35
    else:
        t = np.clip((yy - 420.0) / 700.0, 0, 1) ** 1.2
    grain = (rng.rand(H, W).astype(np.float32) - 0.5) * 8.0
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:, :, 0] = 4 + rgb[0] * t + grain
    arr[:, :, 1] = 5 + rgb[1] * t + grain
    arr[:, :, 2] = 8 + rgb[2] * t + grain
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))
    compact_raw = Image.open(REF / "p01_compact.png").convert("RGB")
    star = star_crop(compact_raw)
    xray = fit(REF / "p04_xray.png")
    fold = fit(REF / "p05_fold.png")
    ring = fit(REF / "p05_ring.png")

    # 01 — careful DISTANCE. Wonder. No remnant hang (save hang for magnetar).
    bg = clean_space(n_faint=0, seed=71)
    paste_scaled(bg, orbit, 960, 620, 160)
    save(bg, "01_careful_distance.png")

    # 02 — GOLD: NEAR THE SURFACE. Close compact GLOWING remnant, not a grey wall.
    bg = clean_space(n_faint=0, seed=82)
    paste_star_fit(bg, star, 1380, 540, 1180)
    paste_scaled(bg, orbit, 260, 640, 150)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "02_near_surface.png")

    # 03 — hover at a “safe” radius. Station-keeping. No remnant.
    bg = clean_space(n_faint=0, seed=73)
    paste_scaled(bg, orbit, 720, 540, 280)
    save(bg, "03_hover_safe.png")

    # 04 — radiation cooks. Locked X-ray storm energy, plus Orbit flinching.
    bg = xray.copy()
    paste_scaled(bg, orbit, 420, 620, 220)
    save(bg, "04_radiation_cooks.png")

    # 05 — MAGNETAR: star still SMALL in the sky. THE one remnant hang.
    bg = clean_space(n_faint=0, seed=75)
    paste_star_fit(bg, star, 1640, 200, 220)
    mag = wash(75, (70, 40, 140), side="right")
    bg = Image.blend(bg, mag, 0.28)
    paste_scaled(bg, orbit, 480, 700, 140)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "05_magnetar_small.png")

    # 06 — electron clouds. Photoreal plasma, not a Bohr-model logo. No Orbit.
    bg = Image.blend(xray, wash(76, (40, 120, 180), side="right"), 0.35)
    save(bg.filter(ImageFilter.GaussianBlur(0.6)), "06_electron_clouds.png")

    # 07 — a STACK of dangers. Physics layers, no grey floor.
    bg = Image.blend(xray, fold, 0.45)
    paste_scaled(bg, orbit, 960, 560, 170)
    save(bg, "07_danger_stack.png")

    # 08 — surface that refuses to be a floor = you cannot stand on a STAR.
    bg = clean_space(n_faint=0, seed=88)
    paste_star_fit(bg, star, 1100, 860, 980)
    paste_scaled(bg, orbit, 960, 220, 150)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "08_refuses_floor.png")

    # 09 — keep closing. Gravity well, not a second remnant portrait.
    bg = Image.blend(ring, fold, 0.4)
    paste_scaled(bg, orbit, 380, 560, 190)
    save(bg, "09_keep_closing.png")

    # 10 — uncomfortable → impossible. Spacetime wins. Exactly one Orbit.
    bg = fold.copy()
    paste_scaled(bg, orbit, 900, 600, 200)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "10_uncomfortable_impossible.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
