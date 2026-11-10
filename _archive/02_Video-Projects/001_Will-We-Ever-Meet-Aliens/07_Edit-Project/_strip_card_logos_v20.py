#!/usr/bin/env python3
"""Strip baked Orbit mascot from bottom-right of text cards (wordmark stays).

Companion Orbit is composited live — a second logo mascot reads as a double.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
DIRS = [
    ROOT / "04_Generated-Clips/03_Polished/unique_cards",
    ROOT / "04_Generated-Clips/03_Polished/chapter_cards",
]
W, H, FPS = 1920, 1080, 30


def font(size: int):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def strip_png(png: Path) -> bool:
    img = Image.open(png).convert("RGBA")
    # Sample a quiet pixel near the BR plate (just above logo zone)
    sample = img.getpixel((W - 80, H - 160))[:3]
    d = ImageDraw.Draw(img)
    # Cover logo + old wordmark plate
    d.rectangle([W - 280, H - 160, W - 8, H - 8], fill=sample + (255,))
    d.text((W - 200, H - 72), "ORBIT", fill=(255, 150, 50), font=font(22))
    img.convert("RGB").save(png)
    return True


def encode(png: Path, mp4: Path, dur: float | None = None):
    if dur is None:
        # probe existing mp4 duration if present
        if mp4.exists():
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp4)],
                capture_output=True, text=True,
            )
            try:
                dur = float(r.stdout.strip())
            except ValueError:
                dur = 4.8
        else:
            dur = 4.8
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-t", f"{dur:.3f}", "-vf", "format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "veryfast", "-crf", "14",
        "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
        "-an", str(mp4),
    ], check=True)


def main():
    n = 0
    for d in DIRS:
        if not d.exists():
            continue
        for png in sorted(d.glob("*.png")):
            strip_png(png)
            mp4 = png.with_name(png.stem + "_v01.mp4")
            # chapter pngs are like chapter_02_....png → chapter_02_...._v01.mp4
            if not mp4.exists():
                mp4 = png.with_suffix(".mp4")
            # retention pattern: card_foo.png → card_foo_v01.mp4
            alt = d / f"{png.stem}_v01.mp4"
            target = alt if alt.exists() or not mp4.exists() else mp4
            if not target.exists():
                target = alt
            encode(png, target)
            n += 1
            print("stripped", png.name, "→", target.name)
    print(f"done {n} cards")


if __name__ == "__main__":
    main()
