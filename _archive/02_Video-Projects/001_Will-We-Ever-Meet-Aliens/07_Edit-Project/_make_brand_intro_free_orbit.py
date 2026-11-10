#!/usr/bin/env python3
"""Brand intro without boxed Orbit — free-floating mascot over full-bleed field."""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand"
RGBA = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba"
W, H = 1920, 1080


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_field() -> Image.Image:
    """Soft full-bleed space field — no inset square plate."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    rng = np.random.default_rng(7)
    for y in range(H):
        # subtle vertical gradient navy → deeper black
        t = y / H
        r = int(6 + 4 * (1 - t))
        g = int(8 + 6 * (1 - t))
        b = int(18 + 10 * (1 - t))
        for x in range(W):
            # gentle vignette
            cx, cy = (x - W / 2) / (W / 2), (y - H / 2) / (H / 2)
            v = min(1.0, (cx * cx + cy * cy) * 0.35)
            px[x, y] = (
                max(0, int(r * (1 - v))),
                max(0, int(g * (1 - v))),
                max(0, int(b * (1 - 0.5 * v))),
            )
    # sparse stars (not dense plate texture)
    for _ in range(90):
        x = int(rng.integers(0, W))
        y = int(rng.integers(0, H))
        bright = int(rng.integers(140, 255))
        sz = int(rng.choice([1, 1, 1, 2]))
        for dy in range(sz):
            for dx in range(sz):
                xx, yy = x + dx, y + dy
                if 0 <= xx < W and 0 <= yy < H:
                    px[xx, yy] = (bright, bright, min(255, bright + 20))
    return img


def main() -> None:
    orbit_path = RGBA / "orbit_rgba_curious.png"
    if not orbit_path.exists():
        orbit_path = RGBA / "orbit_rgba_neutral.png"
    orbit = Image.open(orbit_path).convert("RGBA")
    # Free-floating size — not trapped in a square tile
    target_h = 420
    ow = int(orbit.width * (target_h / orbit.height))
    orbit = orbit.resize((ow, target_h), Image.Resampling.LANCZOS)

    base = make_field().convert("RGBA")
    ox = (W - ow) // 2
    oy = 160
    base.alpha_composite(orbit, (ox, oy))

    draw = ImageDraw.Draw(base)
    title = "ORBIT"
    tag = "Stories from the sky"
    f_title = font(96)
    f_tag = font(36)
    # center text under Orbit
    tb = draw.textbbox((0, 0), title, font=f_title)
    tw = tb[2] - tb[0]
    tx = (W - tw) // 2
    ty = oy + target_h + 36
    draw.text((tx, ty), title, fill=(255, 122, 36, 255), font=f_title)
    tb2 = draw.textbbox((0, 0), tag, font=f_tag)
    tw2 = tb2[2] - tb2[0]
    draw.text(((W - tw2) // 2, ty + 110), tag, fill=(230, 235, 245, 255), font=f_tag)

    png = BRAND / "orbit_brand_intro_v03_free.png"
    base.convert("RGB").save(png, quality=95)
    mp4 = BRAND / "orbit_brand_intro_v01.mp4"
    # Replace the boxed intro used by the edit pipeline
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png),
        "-t", "1.2", "-r", "30",
        "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-crf", "14",
        "-pix_fmt", "yuv420p",
        str(mp4),
    ], check=True)
    print(f"brand intro → {png.name} / {mp4.name}")


if __name__ == "__main__":
    main()
