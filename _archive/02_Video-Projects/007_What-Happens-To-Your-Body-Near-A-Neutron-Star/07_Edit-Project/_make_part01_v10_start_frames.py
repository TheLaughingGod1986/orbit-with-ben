#!/usr/bin/env python3
"""v10 composition start frames — orange back / tidal line / star-only / supernova wall.

Do not I2V acting plates from the full-frame identity still.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

HERE = Path(__file__).resolve().parent
OUT = HERE / "parts/starts_v10"
REPO = Path("/Users/ben/code/Orbit-YouTube")
EP = REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
FRONT = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
RAW = EP / "04_Generated-Clips/01_Raw/part-01"
W, H = 1920, 1080


def clean_space(*, main_star: tuple[int, int, int] | None = None) -> Image.Image:
    bg = Image.new("RGB", (W, H), (2, 3, 6))
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
    arr = np.array(im.convert("RGB"))
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    orange = (r > 95) & (g > 35) & (r > g + 12) & (r > b + 18)
    glow = (r > 150) & (g > 80) & (b < 100)
    seed = orange | glow
    ys, xs = np.where(seed)
    if ys.size == 0:
        raise SystemExit("could not find Orbit orange")
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


def paint_orange_back(sprite: Image.Image) -> Image.Image:
    """Replace the visor FACEPLATE with matte orange so the I2V source has no second face."""
    arr = np.array(sprite)
    rgb = arr[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    a = arr[:, :, 3]
    visor = (a > 80) & (r < 90) & (g < 90) & (b < 110) & (np.abs(r.astype(int) - b.astype(int)) < 40)
    # cream eyes sit inside the visor — paint those too
    cream = (a > 80) & (r > 180) & (g > 160) & (b > 120) & (r < 255)
    mask = visor | cream
    ys, xs = np.where(mask)
    if ys.size:
        # sample nearby orange body for a matching fill
        body = (a > 80) & (r > 120) & (g > 50) & (r > g + 20)
        if body.any():
            fill = tuple(int(x) for x in rgb[body].mean(axis=0))
        else:
            fill = (214, 112, 36)
        arr[mask, 0] = fill[0]
        arr[mask, 1] = fill[1]
        arr[mask, 2] = fill[2]
    out = Image.fromarray(arr, "RGBA")
    return out.filter(ImageFilter.GaussianBlur(0.4))


def paste_scaled(bg: Image.Image, sprite: Image.Image, cx: int, cy: int, height_px: int) -> None:
    ratio = height_px / sprite.height
    nw, nh = max(2, int(sprite.width * ratio)), max(2, height_px)
    sp = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(sp, (int(cx - nw / 2), int(cy - nh / 2)), sp)


def extract_frame(src: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        check=True,
    )


def living_giant() -> Image.Image:
    bg = clean_space()
    arr = np.array(bg)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy, rad = 960, 540, 430
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    rng = np.random.default_rng(18)
    noise = rng.normal(0, 18, (H, W))
    # low-freq blotches
    blotch = Image.fromarray(((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)), "L")
    blotch = blotch.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(12))
    bn = np.array(blotch).astype(np.float32) / 255.0
    inside = d < rad
    t = np.clip(1.0 - (d / rad), 0, 1)
    r = np.clip(255 * (0.72 + 0.28 * t) + noise + (bn - 0.5) * 50, 0, 255)
    g = np.clip(140 + 90 * t + noise * 0.4 + (bn - 0.5) * 30, 0, 255)
    b = np.clip(28 + 40 * t, 0, 255)
    arr[inside, 0] = r[inside]
    arr[inside, 1] = g[inside]
    arr[inside, 2] = b[inside]
    im = Image.fromarray(arr, "RGB")
    ddraw = ImageDraw.Draw(im, "RGBA")
    for i in range(10, 0, -1):
        rr = rad + i * 7
        ddraw.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(255, 160, 40, 18 + i), width=3)
    return im.filter(ImageFilter.GaussianBlur(0.6))


def supernova_wall() -> Image.Image:
    """Frame-filling ejecta — not a leftover remnant portrait."""
    rng = np.random.default_rng(91)
    base = Image.new("RGB", (W, H), (8, 2, 3))
    arr = np.array(base).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = 960, 540
    ang = np.arctan2(yy - cy, xx - cx)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    # radial filaments
    filaments = 0.55 + 0.45 * np.sin(ang * 11 + d / 40)
    blotch = Image.fromarray(((rng.random((H // 6, W // 6)) * 255).astype(np.uint8)), "L")
    blotch = blotch.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(8))
    bn = np.array(blotch).astype(np.float32) / 255.0
    glow = np.clip(1.15 - d / 980, 0.08, 1.0)
    r = np.clip(40 + 215 * glow * filaments * (0.65 + bn), 0, 255)
    g = np.clip(8 + 110 * glow * filaments * bn, 0, 255)
    b = np.clip(4 + 28 * glow, 0, 255)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b
    im = Image.fromarray(arr.astype(np.uint8), "RGB")
    im = ImageEnhance.Contrast(im).enhance(1.15)
    return im.filter(ImageFilter.GaussianBlur(0.8))


def save(im: Image.Image, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest}", flush=True)
    return dest


def main() -> None:
    front = crop_orbit(Image.open(FRONT))
    back = paint_orange_back(front)

    # Prefer a real generated orange-back (plate 05 mid is rear-facing)
    ring = RAW / "omni_p01_05_light-bends-into-a-ring_cursor_v08.mp4"
    tmp = OUT / "_tmp_p05_mid.jpg"
    if ring.exists():
        extract_frame(ring, 4.0, tmp)
        try:
            extracted = crop_orbit(Image.open(tmp))
            a = np.array(extracted)
            rgb = a[:, :, :3].astype(np.int16)
            visor_px = int(
                ((a[:, :, 3] > 80) & (rgb[:, :, 0] < 80) & (rgb[:, :, 1] < 80) & (rgb[:, :, 2] < 100)).sum()
            )
            if visor_px < 800:
                back = extracted
                print(f"using extracted orange-back from plate 05 mid visor_px={visor_px}", flush=True)
            else:
                print(f"plate 05 mid still has visor_px={visor_px} — using painted orange back", flush=True)
        except Exception as e:
            print(f"extract back fallback: {e}", flush=True)

    # 01 — tiny orange figure in the void (v09 hang was a left-third hero)
    bg = clean_space(main_star=(1320, 400, 11))
    paste_scaled(bg, front, 900, 580, 56)
    save(bg, "01_hang_tiny.png")

    # 03 — tumble: already showing orange BACK, mid-frame, no destination
    bg = clean_space()
    paste_scaled(bg, back, 960, 560, 260)
    save(bg, "03_tumble_orange_back.png")

    # 04 — tidal: ONE visor on a body already stretched into a line
    bg = clean_space()
    tall = max(8, int(front.height * 2.6))
    thin = max(8, int(front.width * 0.28))
    stretched = front.resize((thin, tall), Image.Resampling.LANCZOS)
    bg.paste(stretched, (960 - thin // 2, 540 - tall // 2), stretched)
    save(bg, "04_tidal_line.png")

    save(living_giant(), "08_living_giant.png")
    save(supernova_wall(), "09_supernova_wall.png")
    print("done", OUT)


if __name__ == "__main__":
    main()
