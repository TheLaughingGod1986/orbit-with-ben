#!/usr/bin/env python3
"""v18 retention cards — documentary hook + wonder ending (still locked text)."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    "/04_Generated-Clips/03_Polished/unique_cards"
)
LOGO = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Logos/orbit_mark_cutout_72.png")
W, H, FPS = 1920, 1080, 30

# (stem, eyebrow, title, lines, accent, dur)
CARDS = [
    (
        "card_hook_mystery",
        "1977",
        "ONE SIGNAL. NEVER REPEATED.",
        [
            "A burst from the sky that looked artificial…",
            "then vanished. We still don’t know what it was.",
        ],
        (255, 150, 70),
        4.8,
    ),
    (
        "card_hook_crowded",
        "THE SETUP",
        "A CROWDED SKY. A MISSING HELLO.",
        [
            "Hundreds of billions of stars.",
            "And so far — silence.",
        ],
        (90, 170, 255),
        4.5,
    ),
    (
        "card_hook_promise",
        "THIS FILM",
        "FOLLOW THE SILENCE.",
        [
            "Not as a meme. Not as a movie.",
            "As a real scientific mystery.",
        ],
        (255, 170, 80),
        4.5,
    ),
    (
        "card_end_wonder",
        "THE LAST QUESTION",
        "IF SOMEONE IS OUT THERE…",
        [
            "would we recognise the message?",
            "Or would we mistake it for noise?",
        ],
        (255, 140, 90),
        5.0,
    ),
    (
        "card_end_perspective",
        "SCALE",
        "WE ARE A NOISY LITTLE PLANET",
        [
            "in a sky that has stayed quiet — so far.",
            "That quiet makes this place precious.",
        ],
        (120, 190, 255),
        5.0,
    ),
    (
        "card_end_invitation",
        "KEEP LOOKING",
        "THE SILENCE IS AN INVITATION",
        [
            "Not an answer.",
            "A reason to keep listening.",
        ],
        (255, 160, 70),
        4.8,
    ),
    (
        "card_end_subscribe",
        "ORBIT WITH BEN",
        "BIG QUESTIONS. BIGGER UNIVERSE.",
        [
            "If this mystery stays with you —",
            "come back for the next one.",
        ],
        (255, 150, 60),
        4.5,
    ),
]


def font(size: int, bold=True):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_card(eyebrow: str, title: str, lines: list[str], accent: tuple[int, int, int]) -> Image.Image:
    bg0 = (8, 10, 18)
    img = Image.new("RGB", (W, H), bg0)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(bg0[0] + 14 * t),
            int(bg0[1] + 16 * t),
            int(bg0[2] + 28 * t),
        ))
    import random
    rng = random.Random(hash(title) & 0xFFFF)
    for _ in range(110):
        x, y = rng.randint(40, W - 40), rng.randint(40, H - 40)
        c = rng.randint(45, 95)
        d.ellipse([x, y, x + 2, y + 2], fill=(c, c + 8, c + 18))

    d.rectangle([100, 260, 136, 740], fill=accent)
    d.text((170, 190), eyebrow, fill=accent, font=font(28))
    title_font = font(58 if len(title) < 30 else 48)
    d.text((170, 250), title, fill=(255, 255, 255), font=title_font)
    y = 400
    for line in lines:
        d.text((170, y), line, fill=(200, 210, 225), font=font(34, bold=False))
        y += 58

    # Wordmark only — living Orbit companion is composited bottom-left.
    # (A second baked mascot here reads as a double / watermark.)
    d.text((W - 200, H - 72), "ORBIT", fill=(255, 150, 50), font=font(22))
    return img


def encode(png: Path, mp4: Path, dur: float):
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-t", f"{dur:.3f}", "-vf", "format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "14",
        "-x264-params", "keyint=1:min-keyint=1:scenecut=0:bframes=0",
        "-an", str(mp4),
    ], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, eyebrow, title, lines, accent, dur in CARDS:
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        make_card(eyebrow, title, lines, accent).save(png)
        encode(png, mp4, dur)
        print("OK", mp4.name)


if __name__ == "__main__":
    main()
