#!/usr/bin/env python3
"""Part 02 composition start frames — VO-literal, Orbit in-scene, clean vacuum."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

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

OUT = HERE / "parts/starts_part02_v01"


def remnant(bg: Image.Image, cx: int, cy: int, r: int) -> None:
    d = ImageDraw.Draw(bg)
    for i in range(7, 0, -1):
        rr = r + i * 5
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(18 + i * 6, 22 + i * 5, 40 + i * 10))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(196, 214, 255))
    # one hot patch
    d.ellipse((cx - r // 4, cy - r // 5, cx + r // 8, cy + r // 6), fill=(255, 210, 160))


def draw_metal_teaspoon(im: Image.Image, bowl_x: int, bowl_y: int, scale: float = 1.0) -> None:
    """Side-on kitchen teaspoon: open rim, cup bowl, shaft, paddle. Not a dish, lens, or antenna."""
    d = ImageDraw.Draw(im)
    s = scale
    w, h = int(300 * s), int(150 * s)
    x, y = bowl_x, bowl_y
    d.chord(
        (x, y, x + w, y + h),
        start=0,
        end=180,
        fill=(198, 204, 214),
        outline=(236, 238, 242),
    )
    d.chord(
        (x + int(22 * s), y + int(22 * s), x + w - int(22 * s), y + h - int(10 * s)),
        start=0,
        end=180,
        fill=(68, 74, 84),
    )
    d.ellipse(
        (x, y, x + w, y + int(40 * s)),
        fill=(206, 212, 220),
        outline=(240, 242, 246),
        width=max(3, int(4 * s)),
    )
    d.ellipse(
        (x + int(28 * s), y + int(10 * s), x + w - int(28 * s), y + int(32 * s)),
        fill=(78, 84, 94),
    )
    hx = x + w - int(12 * s)
    hy = y + int(18 * s)
    d.polygon(
        [
            (hx, hy - int(11 * s)),
            (hx + int(240 * s), hy - int(16 * s)),
            (hx + int(240 * s), hy + int(16 * s)),
            (hx, hy + int(13 * s)),
        ],
        fill=(186, 192, 202),
        outline=(228, 232, 236),
    )
    d.ellipse(
        (hx + int(220 * s), hy - int(26 * s), hx + int(330 * s), hy + int(26 * s)),
        fill=(192, 198, 208),
        outline=(236, 238, 242),
        width=max(3, int(3 * s)),
    )


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — Orbit banks/drifts; remnant stays compact and small
    bg = clean_space(n_faint=0, seed=21)
    remnant(bg, 1280, 380, 28)
    paste_scaled(bg, orbit, 620, 620, 110)
    save(bg, "01_drifts_closer.png")

    # 02 — remnant is the subject; does not grow
    bg = clean_space(n_faint=0, seed=22)
    remnant(bg, 980, 520, 70)
    save(bg, "02_stays_compact.png")

    # 03 — fierce / wrong compact leftover
    bg = clean_space(n_faint=0, seed=23)
    remnant(bg, 1040, 500, 85)
    save(bg, "03_fierce_wrong.png")

    # 04 — Orbit reacts (medium, not CU hero); remnant still tiny
    bg = clean_space(n_faint=0, seed=24)
    remnant(bg, 1400, 280, 18)
    paste_scaled(bg, orbit, 820, 580, 200)
    save(bg, "04_why_so_small.png")

    # 05 — not a world with air: vacuum, no atmosphere limb
    bg = clean_space(n_faint=0, seed=25)
    remnant(bg, 960, 540, 90)
    save(bg, "05_not_a_world.png")

    # 06 — crushed matter / density (no Orbit)
    bg = Image.new("RGB", (W, H), (4, 4, 8))
    d = ImageDraw.Draw(bg)
    for i in range(14, 0, -1):
        rr = 40 + i * 22
        d.ellipse((960 - rr, 560 - rr, 960 + rr, 560 + rr), fill=(12 + i * 4, 10 + i * 2, 18 + i * 3))
    d.ellipse((900, 500, 1020, 620), fill=(80, 90, 110))
    save(bg.filter(ImageFilter.GaussianBlur(0.6)), "06_crushed_matter.png")

    # 07 — metal kitchen teaspoon vs Earth mountains (NOT an antenna / orb-on-stem)
    bg = Image.new("RGB", (W, H), (14, 18, 32))
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 0, W, 560), fill=(22, 28, 46))
    d.polygon(
        [(0, 780), (160, 420), (340, 700), (500, 280), (760, 680), (980, 220),
         (1260, 640), (1500, 180), (1760, 620), (1920, 760), (1920, 1080), (0, 1080)],
        fill=(52, 60, 72),
    )
    d.polygon([(0, 880), (1920, 800), (1920, 1080), (0, 1080)], fill=(70, 64, 56))
    d.ellipse((540, 900, 860, 980), fill=(36, 32, 28))
    draw_metal_teaspoon(bg, 520, 790, scale=1.2)
    save(bg, "07_teaspoon_mountains.png")

    # 08 — Orbit far out, empty, remnant spinning small
    bg = clean_space(n_faint=0, seed=28)
    remnant(bg, 1320, 360, 22)
    paste_scaled(bg, orbit, 700, 640, 100)
    save(bg, "08_not_holding_yet.png")

    # 09 — lighthouse beam; Orbit already banking away, not a corner-approach
    bg = clean_space(n_faint=0, seed=29)
    remnant(bg, 1080, 500, 40)
    d = ImageDraw.Draw(bg)
    d.polygon([(1080, 500), (1920, 220), (1920, 780)], fill=(40, 70, 120))
    paste_scaled(bg, orbit, 480, 700, 120)
    save(bg, "09_lighthouse_beam.png")

    # 10 — distance is mercy; pull steepens — Orbit braces / underside glow
    bg = clean_space(n_faint=0, seed=30)
    remnant(bg, 1500, 300, 16)
    paste_scaled(bg, orbit, 760, 600, 160)
    save(bg, "10_mercy_runs_out.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
