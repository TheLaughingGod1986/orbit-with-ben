#!/usr/bin/env python3
"""Part 07 composition start frames — rest of Feel: distance / magnetar / stack."""
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

OUT = HERE / "parts/starts_part07_v01"


def crust_terrain(*, mode: str, seed: int) -> Image.Image:
    """Finished iron crust as a WALL (right) or FLOOR (bottom). No sphere primitive."""
    rng = np.random.RandomState(seed)
    yy, xx = np.mgrid[:H, :W].astype(np.float32)

    def fbm(blur: float, amp: float) -> np.ndarray:
        n = rng.rand(H, W).astype(np.float32)
        im = Image.fromarray((n * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(blur)
        )
        return (np.array(im, dtype=np.float32) / 255.0 - 0.5) * amp

    detail = fbm(14, 38) + fbm(5.0, 22) + fbm(1.8, 12)
    pits = np.zeros((H, W), dtype=np.float32)
    for _ in range(22):
        px = rng.randint(100, W - 100)
        py = rng.randint(80, H - 80)
        pr = float(rng.uniform(14, 72))
        dist = np.sqrt((xx - px) ** 2 + (yy - py) ** 2)
        pits -= 32.0 * np.exp(-(dist / pr) ** 2)
    base = np.array([176.0, 166.0, 156.0], dtype=np.float32)
    if mode == "wall":
        term = 680.0 + 110.0 * np.sin((yy - 540.0) / 260.0)
        inside = xx > term
        light = np.clip((xx - term) / 420.0, 0.0, 1.0)
    else:
        hz = 500.0 + 70.0 * ((xx - 960.0) / 920.0) ** 2
        inside = yy > hz
        light = np.clip((yy - hz) / 300.0, 0.0, 1.0) * 0.55 + 0.40
    shade = 0.38 + 0.62 * light
    arr = np.zeros((H, W, 3), dtype=np.float32)
    space = np.array([3.0, 4.0, 7.0], dtype=np.float32)
    for i in range(3):
        ch = np.full((H, W), space[i], dtype=np.float32)
        ch[inside] = np.clip(
            base[i] * shade[inside] + detail[inside] + pits[inside], 0, 255
        )
        arr[:, :, i] = ch
    return Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.3))


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — careful DISTANCE. Wonder. No remnant hang (save hang for magnetar).
    bg = clean_space(n_faint=0, seed=71)
    paste_scaled(bg, orbit, 960, 620, 160)
    save(bg, "01_careful_distance.png")

    # 02 — GOLD: NEAR THE SURFACE. Textured crust WALL, never a clay grey sphere.
    bg = crust_terrain(mode="wall", seed=82)
    paste_scaled(bg, orbit, 300, 620, 120)
    save(bg, "02_near_surface_v04.png")

    # 03 — thought experiment: hover at a “safe” radius. Station-keeping.
    bg = clean_space(n_faint=0, seed=73)
    paste_scaled(bg, orbit, 720, 540, 280)
    save(bg, "03_hover_safe.png")

    # 04 — radiation cooks systems. Wash of hard light.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[:H, :W]
    wash = np.clip((xx / W) ** 1.4, 0, 1)
    arr[:, :, 0] = 18 + 160 * wash
    arr[:, :, 1] = 12 + 90 * wash
    arr[:, :, 2] = 8 + 40 * wash
    bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    paste_scaled(bg, orbit, 420, 560, 240)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "04_radiation_cooks.png")

    # 05 — MAGNETAR: star still looks SMALL in the sky. THE one remnant hang.
    bg = clean_space(n_faint=0, seed=75)
    bg = paint_sphere(bg, 1580, 280, 36, (210, 220, 235))
    d = ImageDraw.Draw(bg)
    for i, col in enumerate(((90, 70, 160), (70, 110, 190), (140, 80, 180))):
        d.arc((200 - i * 30, 80 - i * 20, 1700 + i * 20, 980 + i * 30), start=200, end=340, fill=col, width=4)
    paste_scaled(bg, orbit, 480, 700, 140)
    save(bg.filter(ImageFilter.GaussianBlur(0.5)), "05_magnetar_small.png")

    # 06 — electron clouds distort. Wispy orbital shear — not stacked oval sprites.
    bg = Image.new("RGB", (W, H), (6, 8, 14))
    d = ImageDraw.Draw(bg)
    for i, col in enumerate(((80, 160, 220), (160, 90, 210), (70, 180, 200), (120, 80, 190))):
        d.arc((420 - i * 40, 220 - i * 18, 1500 + i * 40, 860 + i * 18), start=200, end=350, fill=col, width=4)
        d.arc((380 + i * 30, 160 + i * 22, 1540 - i * 20, 920 - i * 10), start=20, end=160, fill=col, width=3)
    save(bg.filter(ImageFilter.GaussianBlur(1.2)), "06_electron_clouds.png")

    # 07 — a STACK of dangers. Four layered bands, not labels.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    arr[:, :, 0] = 20 + 80 * np.exp(-((yy - 0.18) ** 2) / 0.012)
    arr[:, :, 1] = 18 + 70 * np.exp(-((yy - 0.40) ** 2) / 0.012)
    arr[:, :, 2] = 40 + 110 * np.exp(-((yy - 0.62) ** 2) / 0.012)
    arr[:, :, 0] += 90 * np.exp(-((yy - 0.84) ** 2) / 0.010)
    arr[:, :, 1] += 70 * np.exp(-((yy - 0.84) ** 2) / 0.010)
    bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    paste_scaled(bg, orbit, 960, 540, 180)
    save(bg.filter(ImageFilter.GaussianBlur(0.8)), "07_danger_stack.png")

    # 08 — surface that refuses to be a floor. Textured crust FLOOR, never a clay grey sphere.
    bg = crust_terrain(mode="floor", seed=88)
    paste_scaled(bg, orbit, 960, 300, 150)
    save(bg, "08_refuses_floor_v03.png")

    # 09 — keep closing. Soft well, not a second hang disc.
    arr = np.zeros((H, W, 3), dtype=np.float32)
    yy, xx = np.mgrid[:H, :W]
    dist = np.sqrt((xx - 1700.0) ** 2 + (yy - 540.0) ** 2)
    well = np.exp(-((dist / 380.0) ** 2) * 1.2)
    arr[:, :, 0] = 8 + 90 * well
    arr[:, :, 1] = 10 + 80 * well
    arr[:, :, 2] = 16 + 120 * well
    bg = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    paste_scaled(bg, orbit, 420, 560, 200)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "09_keep_closing.png")

    # 10 — uncomfortable → impossible. Warp steepens. Physics, not gore.
    bg = Image.new("RGB", (W, H), (4, 5, 10))
    d = ImageDraw.Draw(bg)
    for i in range(16):
        y = 40 + i * 66
        d.arc(
            (60 - i * 18, y - 260, 1860 + i * 18, y + 260),
            start=195,
            end=345,
            fill=(50 + i * 6, 30 + i * 4, 80 + i * 7),
            width=2,
        )
    paste_scaled(bg, orbit, 900, 600, 220)
    save(bg.filter(ImageFilter.GaussianBlur(1.0)), "10_uncomfortable_impossible.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
