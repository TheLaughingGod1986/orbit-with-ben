#!/usr/bin/env python3
"""Part 08 start frames — Surface That Isn’t a Floor.

Compact glowing remnant (locked Part 01/07 language). Never a grey moon,
never cratered iron wall, never clay sphere, never Death Star greebles.
"""
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
from _make_part07_v02_start_frames import fit, paste_star_fit, star_crop  # noqa: E402

OUT = HERE / "parts/starts_part08_v01"
REF = HERE / "parts/_ref_locked_remnant"


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def paste_star_fill(bg: Image.Image, star: Image.Image) -> None:
    """Scale the remnant so it fills 1920x1080 — no portrait inset."""
    ratio = max(W / star.width, H / star.height) * 1.08
    nw, nh = max(2, int(star.width * ratio)), max(2, int(star.height * ratio))
    piece = star.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(piece, (int((W - nw) / 2), int((H - nh) / 2)))


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))
    compact_raw = Image.open(REF / "p01_compact.png").convert("RGB")
    star = star_crop(compact_raw)
    fold = fit(REF / "p05_fold.png")
    ring = fit(REF / "p05_ring.png")

    # 01 — SHIP GATE: remnant / surface-that-isn’t-a-floor FILLS the frame. ZERO Orbit.
    bg = clean_space(n_faint=0, seed=81)
    paste_star_fill(bg, star)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "01_surface_isnt_floor.png")

    # 02 — ~8s: Orbit BANKS IN and tries to land; thrusters abort. Not idle hover.
    bg = clean_space(n_faint=0, seed=82)
    paste_star_fit(bg, star, 1200, 860, 1000)
    paste_scaled(bg, orbit, 160, 240, 130)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "02_land_abort.png")

    # 03 — the crust is real: a rigid outer layer. Close glowing remnant, not a grey moon.
    bg = clean_space(n_faint=0, seed=83)
    paste_star_fill(bg, star)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "03_crust_is_real.png")

    # 04 — centimetre mountains / sand-grain scale. Tiny ripples on a glowing star, not lunar peaks.
    bg = clean_space(n_faint=0, seed=84)
    paste_star_fit(bg, star, 960, 540, 980)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "04_centimetre_mountains.png")

    # 05 — ripple spacetime for gravitational-wave hunters. Wave, not a mountain wall.
    bg = Image.blend(ring, fold, 0.45)
    save(bg.filter(ImageFilter.GaussianBlur(0.4)), "05_spacetime_ripple.png")

    # 06 — body cannot be a rigid object. Orbit bracing, losing rigidity.
    bg = clean_space(n_faint=0, seed=86)
    paste_star_fit(bg, star, 1500, 700, 720)
    paste_scaled(bg, orbit, 520, 480, 240)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "06_not_rigid.png")

    # 07 — bones, steel, diamond are suggestions. Materials fail. No gore.
    bg = clean_space(n_faint=0, seed=87)
    paste_scaled(bg, orbit, 960, 560, 260)
    save(bg, "07_suggestions.png")

    # 08 — GOLD: an apple wouldn’t fall / becomes a rumour. Apple is the subject.
    bg = clean_space(n_faint=0, seed=88)
    paste_star_fit(bg, star, 1500, 820, 760)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "08_apple_rumour.png")

    # 09 — GOLD: underside glow flares, thrusters refuse the landing.
    bg = clean_space(n_faint=0, seed=89)
    paste_star_fit(bg, star, 1100, 900, 980)
    paste_scaled(bg, orbit, 960, 240, 170)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "09_refuse_landing.png")

    # 10 — a surface without visitors. Remnant as a star; Orbit leaving.
    bg = clean_space(n_faint=0, seed=90)
    paste_star_fit(bg, star, 1400, 540, 860)
    paste_scaled(bg, orbit, 320, 420, 150)
    save(bg.filter(ImageFilter.GaussianBlur(0.25)), "10_no_visitors.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
