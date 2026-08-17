#!/usr/bin/env python3
"""Part 03 composition start frames — density chapter, VO-literal."""
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
from _make_part02_v01_start_frames import draw_metal_teaspoon, remnant  # noqa: E402

OUT = HERE / "parts/starts_part03_v01"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — kitchen density: Orbit with a dull heavy lump (lead)
    bg = Image.new("RGB", (W, H), (28, 24, 22))
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 780, W, H), fill=(48, 42, 38))
    d.ellipse((860, 820, 980, 900), fill=(90, 90, 95))
    paste_scaled(bg, orbit, 720, 560, 220)
    save(bg, "01_kitchen_lead.png")

    # 02 — osmium feels wrong; denser lump
    bg = Image.new("RGB", (W, H), (22, 22, 28))
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 800, W, H), fill=(40, 40, 48))
    d.ellipse((900, 830, 980, 890), fill=(40, 50, 70))
    paste_scaled(bg, orbit, 760, 540, 240)
    save(bg, "02_osmium_wrong.png")

    # 03 — Sun core plasma, no Orbit
    bg = Image.new("RGB", (W, H), (40, 8, 4))
    d = ImageDraw.Draw(bg)
    for i in range(18, 0, -1):
        rr = 80 + i * 22
        d.ellipse((960 - rr, 540 - rr, 960 + rr, 540 + rr), fill=(min(255, 80 + i * 10), min(180, i * 8), 10))
    save(bg.filter(ImageFilter.GaussianBlur(0.8)), "03_sun_core.png")

    # 04 — white dwarf
    bg = clean_space(n_faint=0, seed=34)
    d = ImageDraw.Draw(bg)
    d.ellipse((820, 400, 1100, 680), fill=(230, 240, 255))
    save(bg, "04_white_dwarf.png")

    # 05 — neutron star past that line
    bg = clean_space(n_faint=0, seed=35)
    remnant(bg, 980, 520, 55)
    save(bg, "05_past_the_line.png")

    # 06 — squeezed into neutrons (interior)
    bg = Image.new("RGB", (W, H), (6, 4, 10))
    d = ImageDraw.Draw(bg)
    for i in range(12, 0, -1):
        rr = 50 + i * 28
        d.ellipse((960 - rr, 540 - rr, 960 + rr, 540 + rr), fill=(20 + i * 3, 8, 30 + i * 4))
    save(bg, "06_squeezed_neutrons.png")

    # 07 — Orbit stares at a metal kitchen teaspoon (bowl + handle, not an antenna)
    bg = clean_space(n_faint=0, seed=37)
    draw_metal_teaspoon(bg, 980, 560, scale=0.78)
    paste_scaled(bg, orbit, 620, 560, 180)
    save(bg, "07_stares_teaspoon.png")

    # 08 — teaspoon punches through Earth
    bg = Image.new("RGB", (W, H), (4, 6, 12))
    d = ImageDraw.Draw(bg)
    d.ellipse((620, 280, 1300, 960), fill=(40, 80, 160))
    d.ellipse((700, 360, 1220, 880), fill=(50, 120, 70))
    d.polygon([(960, 200), (990, 540), (930, 540)], fill=(255, 220, 120))
    save(bg, "08_punch_through_earth.png")

    # 09 — YOU are the object approaching: remnant limb fills the left; Orbit is the incoming mass
    bg = clean_space(n_faint=0, seed=39)
    d = ImageDraw.Draw(bg)
    remnant(bg, -80, 540, 520)
    paste_scaled(bg, orbit, 1480, 420, 70)
    save(bg, "09_you_approaching.png")

    # 10 — physics without a narrator: visor CU, sky starting to smear — not another hang
    bg = clean_space(n_faint=0, seed=40)
    d = ImageDraw.Draw(bg)
    for i, col in ((0, (40, 50, 80)), (1, (70, 80, 120)), (2, (120, 140, 190))):
        d.arc((200 - i * 40, 80 - i * 20, 1720 + i * 40, 980 + i * 20), start=200, end=340, fill=col, width=8)
    paste_scaled(bg, orbit, 960, 720, 520)
    save(bg, "10_without_narrator.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
