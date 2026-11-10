#!/usr/bin/env python3
"""Locked still chapter cards — 3-act framing + Orbit mascot. No zoom/fade/shake."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/04_Generated-Clips/03_Polished/chapter_cards")
ORBIT = Path(
    "/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/"
    "Overlay-Rig-v03/frames/orbit_present-left_normal.png"
)
W, H, FPS, DUR = 1920, 1080, 30, 2.8

CHAPTERS = [
    ("01_cold-open", 1, "ACT I  ·  THE PROBLEM", "LOOK UP", "A crowded sky… and a missing hello"),
    ("02_galaxy-scale", 2, "ACT I  ·  THE PROBLEM", "THE SCALE OF SPACE", "Distance is the first hard truth"),
    ("03_exoplanets", 3, "ACT I  ·  THE PROBLEM", "WORLDS BEYOND", "On paper, we should not be alone"),
    ("04_fermi-paradox", 4, "ACT I  ·  THE PROBLEM", "WHERE IS EVERYBODY?", "The silence that won’t go away"),
    ("05_great-filter", 5, "ACT II  ·  THE PATHS", "THE GREAT FILTER", "One answer people fear"),
    ("06_explanations", 6, "ACT II  ·  THE PATHS", "WHY THE SILENCE?", "Distance, time, and careful quiet"),
    ("07_detection", 7, "ACT II  ·  THE PATHS", "HOW WE LOOK", "Listening for a fingerprint of life"),
    ("08_first-contact", 8, "ACT III  ·  THE ANSWER", "WILL WE MEET THEM?", "What “meeting” could mean"),
    ("09_conclusion", 9, "ACT III  ·  THE ANSWER", "KEEP LISTENING", "An honest answer — and an open door"),
]
TOTAL = 9


def font(size: int, bold=True):
    bold_p = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        return ImageFont.truetype(bold_p if bold else reg, size)
    except Exception:
        return ImageFont.load_default()


def paste_orbit(img: Image.Image) -> None:
    if not ORBIT.exists():
        return
    orbit = Image.open(ORBIT).convert("RGBA")
    # Bottom-right companion, clear of title block
    target_w = 460
    scale = target_w / orbit.width
    orbit = orbit.resize((target_w, max(1, int(orbit.height * scale))), Image.Resampling.LANCZOS)
    x = W - orbit.width - 110
    y = H - orbit.height - 90
    img.paste(orbit, (x, y), orbit)


def make_card(num: int, act: str, title: str, subtitle: str) -> Image.Image:
    if num <= 4:
        accent = (255, 110, 70)
        bg0 = (18, 8, 10)
    elif num <= 7:
        accent = (70, 170, 255)
        bg0 = (8, 14, 28)
    else:
        accent = (255, 180, 60)
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
    for frac in (4 / TOTAL, 7 / TOTAL):
        tx = bar_x + int(bar_w * frac)
        d.rectangle([tx - 1, bar_y - 6, tx + 1, bar_y + bar_h + 6], fill=(140, 150, 170))

    d.rectangle([120, 380, 155, 620], fill=accent)
    d.text((190, 400), title, fill=(255, 255, 255), font=font(68))
    d.text((190, 520), subtitle, fill=(200, 210, 225), font=font(34, bold=False))

    paste_orbit(img)
    # Wordmark sits left of the mascot so both read clearly
    d.text((1180, H - 78), "ORBIT", fill=(255, 150, 50), font=font(26))
    return img


def encode_locked_still(png: Path, mp4: Path, dur: float = DUR) -> None:
    """True locked still — no fades, no zoom, all-intra for edit-friendly cuts."""
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", str(FPS), "-i", str(png),
            "-t", f"{dur:.3f}",
            "-vf", "scale=1920:1080:flags=neighbor,fps=30,format=yuv420p",
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "14",
            "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
            "-an", str(mp4),
        ],
        check=True,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for cid, num, act, title, subtitle in CHAPTERS:
        stem = f"chapter_{num:02d}_{cid}"
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        mp4_v02 = OUT / f"{stem}_v02.mp4"
        make_card(num, act, title, subtitle).save(png)
        encode_locked_still(png, mp4)
        # Keep v02 alias in sync for any builders that prefer it
        encode_locked_still(png, mp4_v02)
        print("OK", mp4.name)


if __name__ == "__main__":
    main()
