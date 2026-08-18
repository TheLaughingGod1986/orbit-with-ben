#!/usr/bin/env python3
"""Part 09 close start frames — leave, shrink to jewel, galaxy almost normal."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageFilter

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
from _make_part07_v02_start_frames import paste_star_fit, star_crop  # noqa: E402
from _make_part08_v01_start_frames import paste_star_fill  # noqa: E402

OUT = HERE / "parts/starts_part09_close_v01"
REF = HERE / "parts/_ref_locked_remnant"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))
    compact_raw = Image.open(REF / "p01_compact.png").convert("RGB")
    star = star_crop(compact_raw)

    # 01 — leaving a still-large remnant. Orbit already in frame, upper-left.
    bg = clean_space(n_faint=0, seed=91)
    paste_star_fill(bg, star)
    paste_scaled(bg, orbit, 220, 180, 140)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "01_turns_away.png")

    # 02 — winning distance: remnant recedes but still a real star in frame
    bg = clean_space(n_faint=0, seed=92)
    paste_star_fit(bg, star, 1240, 620, 900)
    paste_scaled(bg, orbit, 280, 200, 120)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "02_winning_distance.png")

    # 03 — shrinking toward a fierce jewel. Tiny Orbit.
    bg = clean_space(n_faint=0, seed=93)
    paste_star_fit(bg, star, 1180, 540, 520)
    paste_scaled(bg, orbit, 340, 280, 90)
    save(bg.filter(ImageFilter.GaussianBlur(0.3)), "03_shrinks_jewel.png")

    # 04 — leftover engine / fierce jewel. ZERO Orbit.
    bg = clean_space(n_faint=0, seed=94)
    paste_star_fit(bg, star, 960, 540, 380)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "04_fierce_jewel.png")

    # 05 — light leans
    ring_path = REF / "p05_ring.png"
    bg = clean_space(n_faint=0, seed=95)
    if ring_path.exists():
        ring = Image.open(ring_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        bg = Image.blend(bg, ring, 0.72)
    else:
        paste_star_fit(bg, star, 960, 540, 320)
    save(bg.filter(ImageFilter.GaussianBlur(0.35)), "05_light_leans.png")

    # 06 — galaxy almost normal: faint band, small jewel
    bg = clean_space(n_faint=18, seed=96)
    paste_star_fit(bg, star, 1400, 480, 160)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "06_galaxy_almost.png")

    # 07 — almost: quieter pinprick jewel
    bg = clean_space(n_faint=12, seed=97)
    paste_star_fit(bg, star, 1280, 520, 90)
    save(bg.filter(ImageFilter.GaussianBlur(0.45)), "07_almost.png")

    # 08 — Orbit tiny, looking back, no spin
    bg = clean_space(n_faint=8, seed=98)
    paste_star_fit(bg, star, 1460, 380, 140)
    paste_scaled(bg, orbit, 480, 640, 95)
    save(bg.filter(ImageFilter.GaussianBlur(0.3)), "08_never_trust.png")

    # 09 — last real picture: jewel large enough to read as a star
    bg = clean_space(n_faint=4, seed=99)
    paste_star_fit(bg, star, 960, 540, 340)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "09_jewel_hold.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
