#!/usr/bin/env python3
"""Clean-vacuum + on-model Orbit start frames for Neutron Star Part 01 v08.

Canonical Orbit from the identity still, on near-black with at most one
distant star — not a dense starfield, not a glowing-belly knockoff.
"""
from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
OUT = HERE / "parts/starts_v08"
REPO = Path("/Users/ben/code/Orbit-YouTube")
FRONT = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
W, H = 1920, 1080


def clean_space(*, main_star: tuple[int, int, int] | None = None, n_faint: int = 0, seed: int = 1) -> Image.Image:
    rng = random.Random(seed)
    bg = Image.new("RGB", (W, H), (2, 3, 6))
    px = bg.load()
    for _ in range(n_faint):
        x, y = rng.randint(40, W - 40), rng.randint(40, H - 40)
        v = rng.randint(28, 70)
        px[x, y] = (v, v, min(255, v + 8))
    if main_star:
        sx, sy, r = main_star
        d = ImageDraw.Draw(bg)
        for i in range(8, 0, -1):
            rr = r + i * 6
            col = 18 + i * 10
            d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), fill=(col, col, min(255, col + 20)))
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(236, 242, 255))
    return bg


def crop_orbit(im: Image.Image) -> Image.Image:
    """Cut Orbit off the identity still's starfield. Keep visor + body only."""
    arr = np.array(im.convert("RGB"))
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    orange = (r > 95) & (g > 35) & (r > g + 12) & (r > b + 18)
    glow = (r > 150) & (g > 80) & (b < 100)
    seed = orange | glow
    ys, xs = np.where(seed)
    if ys.size == 0:
        raise SystemExit("could not find Orbit orange in identity still")
    pad = 36
    box = (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(im.width, int(xs.max()) + pad),
        min(im.height, int(ys.max()) + pad),
    )
    crop = im.convert("RGBA").crop(box)
    c = np.array(crop)
    ch = c[:, :, :3].astype(np.int16)
    cr, cg, cb = ch[:, :, 0], ch[:, :, 1], ch[:, :, 2]
    body = (cr > 90) & (cg > 30) & (cr > cg + 10) & (cr > cb + 14)
    glow2 = (cr > 140) & (cg > 70) & (cb < 110)
    solid = Image.fromarray(np.where(body | glow2, 255, 0).astype(np.uint8), "L")
    solid = solid.filter(ImageFilter.MaxFilter(5))
    work = Image.eval(solid, lambda p: 255 - p)
    for xy in (
        (0, 0),
        (work.width - 1, 0),
        (0, work.height - 1),
        (work.width - 1, work.height - 1),
    ):
        ImageDraw.floodfill(work, xy, 64)
    keep = np.array(work) != 64
    c[:, :, 3] = np.where(keep, 255, 0).astype(np.uint8)
    return Image.fromarray(c, "RGBA")


def paste_scaled(bg: Image.Image, sprite: Image.Image, cx: int, cy: int, height_px: int) -> None:
    ratio = height_px / sprite.height
    nw, nh = max(2, int(sprite.width * ratio)), max(2, height_px)
    sp = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(sp, (int(cx - nw / 2), int(cy - nh / 2)), sp)


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name}", flush=True)


def main() -> None:
    orbit = crop_orbit(Image.open(FRONT))

    # 01 — tiny figure, still on-model, one ordinary star
    bg = clean_space(main_star=(1380, 420, 14), n_faint=0, seed=11)
    paste_scaled(bg, orbit, 820, 560, 150)
    save(bg, "01_hang_clean.png")

    # 02 — the star is the subject. No Orbit. Clean void.
    bg = clean_space(main_star=(1040, 540, 95), n_faint=0, seed=12)
    save(bg, "02_ordinary_star.png")

    # 03 — weightless tumble, on-model, no destination
    bg = clean_space(n_faint=0, seed=13)
    paste_scaled(bg, orbit, 960, 560, 220)
    save(bg, "03_tumble.png")

    # 04 — on-model Orbit; stretch happens in the take, not a deformed still
    bg = clean_space(n_faint=0, seed=14)
    paste_scaled(bg, orbit, 960, 540, 240)
    save(bg, "04_tidal.png")

    # 05 — photon ring, tiny on-model Orbit in the centre
    bg = clean_space(n_faint=0, seed=15)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    cx, cy = 960, 540
    rd.ellipse((cx - 400, cy - 400, cx + 400, cy + 400), outline=(255, 236, 190, 80), width=28)
    rd.ellipse((cx - 378, cy - 378, cx + 378, cy + 378), outline=(255, 250, 235, 170), width=10)
    bg = Image.alpha_composite(bg.convert("RGBA"), ring).convert("RGB")
    paste_scaled(bg, orbit, 960, 540, 48)
    save(bg, "05_photon_ring.png")

    # 06 — hold; remnant a small point above, not a corner approach
    bg = clean_space(main_star=(960, 220, 12), n_faint=0, seed=16)
    paste_scaled(bg, orbit, 960, 640, 140)
    save(bg, "06_hold.png")

    # 07 — full canonical Orbit CU on true black (no identity-still starfield)
    bg = clean_space(n_faint=0, seed=17)
    paste_scaled(bg, orbit, 960, 560, 820)
    save(bg, "07_visor_cu.png")

    # 08 — living giant, clean void
    bg = clean_space(n_faint=0, seed=18)
    d = ImageDraw.Draw(bg)
    gx, gy, gr = 960, 560, 330
    for i in range(16, 0, -1):
        rr = gr + i * 6
        d.ellipse((gx - rr, gy - rr, gx + rr, gy + rr), fill=(255, 150 + i * 3, 36))
    d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=(255, 198, 72))
    save(bg.filter(ImageFilter.GaussianBlur(0.5)), "08_living_giant.png")

    # 09 — supernova wall, no Orbit
    bg = Image.new("RGB", (W, H), (12, 4, 6))
    d = ImageDraw.Draw(bg)
    for i in range(18, 0, -1):
        rr = 70 + i * 26
        d.ellipse((960 - rr, 540 - rr, 960 + rr, 540 + rr), fill=(min(255, 30 + i * 12), min(180, i * 6), min(80, i * 3)))
    d.ellipse((910, 500, 1010, 600), fill=(255, 248, 230))
    save(bg, "09_supernova.png")

    # 10 — leftover remnant, clean void, no Orbit
    bg = clean_space(n_faint=0, seed=20)
    d = ImageDraw.Draw(bg)
    mx, my, mr = 960, 540, 150
    for i in range(8, 0, -1):
        rr = mr + i * 6
        d.ellipse((mx - rr, my - rr, mx + rr, my + rr), fill=(30 + i * 8, 40 + i * 7, 70 + i * 12))
    d.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(210, 224, 255))
    save(bg, "10_remnant.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
