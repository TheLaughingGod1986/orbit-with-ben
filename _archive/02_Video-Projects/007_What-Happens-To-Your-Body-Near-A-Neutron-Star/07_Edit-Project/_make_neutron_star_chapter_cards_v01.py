#!/usr/bin/env python3
"""Locked still chapter cards for Neutron Star — Europa / Aliens house style.

No Ken Burns. Mid-film acts only (no card on the picture-first open).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
OUT = EP / "04_Generated-Clips/03_Polished/chapter_cards"
ORBIT = Path(
    "/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/"
    "Overlay-Rig-v03/frames/orbit_present-left_normal.png"
)
W, H, FPS, DUR = 1920, 1080, 24, 2.58

# Inserted BEFORE these part roughs in broadcast v02.
CHAPTERS = [
    ("01_corpse", 1, "ACT I  ·  ORIGIN", "THE CORPSE OF A STAR", "What remains after a star loses"),
    ("02_density", 2, "ACT I  ·  ORIGIN", "DENSITY YOU CAN'T IMAGINE", "A teaspoon that outweighs mountains"),
    ("03_see", 3, "ACT II  ·  APPROACH", "WHAT YOU WOULD SEE", "When the sky starts to lean"),
    ("04_feel", 4, "ACT II  ·  APPROACH", "WHAT YOU WOULD FEEL", "Falling that is no longer floating"),
    ("05_surface", 5, "ACT III  ·  THE EDGE", "THE SURFACE THAT ISN'T A FLOOR", "A crust you cannot stand on"),
]
TOTAL = len(CHAPTERS)


def font(size: int, bold: bool = True):
    bold_p = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        return ImageFont.truetype(bold_p if bold else reg, size)
    except OSError:
        return ImageFont.load_default()


def paste_orbit(img: Image.Image) -> None:
    if not ORBIT.exists():
        return
    orbit = Image.open(ORBIT).convert("RGBA")
    target_w = 420
    scale = target_w / orbit.width
    orbit = orbit.resize((target_w, max(1, int(orbit.height * scale))), Image.Resampling.LANCZOS)
    x = W - orbit.width - 90
    y = H - orbit.height - 70
    img.paste(orbit, (x, y), orbit)


def make_card(num: int, act: str, title: str, subtitle: str) -> Image.Image:
    if num <= 2:
        accent = (255, 110, 70)
        bg0 = (18, 8, 10)
    elif num <= 4:
        accent = (255, 160, 70)
        bg0 = (12, 10, 18)
    else:
        accent = (255, 196, 80)
        bg0 = (10, 12, 22)

    img = Image.new("RGB", (W, H), bg0)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(bg0[0] + 8 * t)
        g = int(bg0[1] + 10 * t)
        b = int(bg0[2] + 18 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    d.text((120, 140), act, fill=accent, font=font(28))
    d.text((120, 190), f"CHAPTER  {num}  OF  {TOTAL}", fill=(220, 225, 235), font=font(32))

    bar_x, bar_y, bar_w, bar_h = 120, 250, 980, 16
    d.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=8, fill=(36, 42, 58))
    fill_w = int(bar_w * (num / TOTAL))
    d.rounded_rectangle([bar_x, bar_y, bar_x + max(12, fill_w), bar_y + bar_h], radius=8, fill=accent)

    title_size = 64 if len(title) > 28 else 68
    d.rectangle([120, 380, 155, 620], fill=accent)
    d.text((190, 400), title, fill=(255, 255, 255), font=font(title_size))
    d.text((190, 520), subtitle, fill=(200, 210, 225), font=font(34, bold=False))

    paste_orbit(img)
    d.text((1180, H - 78), "ORBIT", fill=(255, 150, 50), font=font(26))
    return img


def encode_locked_still(png: Path, mp4: Path, dur: float = DUR) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", str(FPS), "-i", str(png),
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", f"{dur:.3f}",
            "-vf", "scale=1920:1080:flags=neighbor,fps=24,format=yuv420p",
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "14",
            "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "96k",
            "-shortest", str(mp4),
        ],
        check=True,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for cid, num, act, title, subtitle in CHAPTERS:
        stem = f"chapter_{num:02d}_{cid}"
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        make_card(num, act, title, subtitle).save(png)
        encode_locked_still(png, mp4)
        print("OK", mp4.name, flush=True)


if __name__ == "__main__":
    main()
