#!/usr/bin/env python3
"""Drake Equation blackboard + brief-candles explainer stills (locked, no zoompan)."""
from __future__ import annotations

import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    "/04_Generated-Clips/03_Polished/unique_cards"
)
LOGO = Path("/Users/ben/code/Orbit-YouTube/00_Brand/Logos/orbit_youtube-avatar_800x800_v02.png")
W, H, FPS = 1920, 1080, 30


def font(size: int, chalk: bool = False):
    candidates = []
    if chalk:
        candidates += [
            "/System/Library/Fonts/Supplemental/Chalkduster.ttf",
            "/Library/Fonts/Chalkduster.ttf",
            "/System/Library/Fonts/Supplemental/Marker Felt.ttc",
        ]
    candidates += [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def chalk_board_bg() -> Image.Image:
    """Green chalkboard with subtle grain + wooden rail."""
    rng = random.Random(42)
    # Fast grain via small noise image + resize
    noise = Image.effect_noise((W // 4, H // 4), 28).convert("L")
    noise = noise.resize((W, H), Image.Resampling.BILINEAR)
    base = Image.new("RGB", (W, H), (32, 62, 44))
    npx = noise.load()
    px = base.load()
    for y in range(H):
        shade = 8 * y // H
        for x in range(W):
            n = (npx[x, y] - 128) // 6
            g = max(20, min(72, 48 + shade + n))
            px[x, y] = (g - 8, g + 6, g - 4)

    # Soft chalk dust / wipe marks
    dust = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(dust)
    for _ in range(36):
        x0 = rng.randint(80, W - 220)
        y0 = rng.randint(80, H - 180)
        dd.ellipse(
            [x0, y0, x0 + rng.randint(50, 240), y0 + rng.randint(14, 55)],
            fill=rng.randint(10, 30),
        )
    dust = dust.filter(ImageFilter.GaussianBlur(14))
    board = base.convert("RGBA")
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wpx = wash.load()
    dpx = dust.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            a = dpx[x, y]
            if a:
                wpx[x, y] = (236, 230, 210, int(a * 0.5))
                if x + 1 < W:
                    wpx[x + 1, y] = wpx[x, y]
                if y + 1 < H:
                    wpx[x, y + 1] = wpx[x, y]
                    if x + 1 < W:
                        wpx[x + 1, y + 1] = wpx[x, y]
    board = Image.alpha_composite(board, wash)

    d = ImageDraw.Draw(board)
    wood = (92, 58, 32)
    wood_hi = (120, 78, 44)
    m = 36
    d.rectangle([0, 0, W, m], fill=wood)
    d.rectangle([0, H - m, W, H], fill=wood)
    d.rectangle([0, 0, m, H], fill=wood)
    d.rectangle([W - m, 0, W, H], fill=wood)
    d.rectangle([m - 8, m - 8, W - m + 8, H - m + 8], outline=wood_hi, width=3)

    d.rectangle([120, H - m - 18, W - 120, H - m + 6], fill=(70, 44, 24))
    for i, cx in enumerate((280, 420, 560)):
        col = [(240, 240, 235), (255, 210, 90), (255, 140, 90)][i]
        d.rounded_rectangle([cx, H - m - 12, cx + 70, H - m + 2], radius=4, fill=col)

    return board.convert("RGB")


def draw_orbit(img: Image.Image):
    """Wordmark only — avoid a second baked mascot vs the corner companion."""
    d = ImageDraw.Draw(img)
    d.text((W - 200, H - 72), "ORBIT", fill=(255, 170, 70), font=font(22))


def make_drake_blackboard() -> Image.Image:
    img = chalk_board_bg()
    d = ImageDraw.Draw(img)
    chalk = (236, 232, 214)
    chalk_dim = (190, 200, 175)
    accent = (255, 196, 90)

    d.text((120, 70), "THE DRAKE EQUATION", fill=accent, font=font(34, chalk=True))
    d.text((120, 120), "How many communicative civilisations in our galaxy?", fill=chalk_dim, font=font(28))

    # Main equation — large chalk (ASCII subscripts: Chalkduster lacks Unicode)
    eq = "N  =  R*  ·  fp  ·  ne  ·  fl  ·  fi  ·  fc  ·  L"
    d.text((120, 220), eq, fill=chalk, font=font(56, chalk=True))
    # underline chalk stroke
    d.line([(120, 295), (1680, 295)], fill=(210, 205, 180), width=2)

    terms = [
        ("R*", "star formation rate"),
        ("fp", "fraction of stars with planets"),
        ("ne", "habitable worlds per system"),
        ("fl", "fraction where life appears"),
        ("fi", "fraction that become intelligent"),
        ("fc", "fraction that can communicate"),
        ("L", "lifetime of such a civilisation"),
    ]
    y = 340
    for sym, label in terms:
        d.text((160, y), sym, fill=accent, font=font(32, chalk=True))
        d.text((280, y + 4), "—  " + label, fill=chalk, font=font(28))
        y += 58

    d.text((120, 820), "Not a final answer — a way to line up our ignorance.", fill=chalk_dim, font=font(26, chalk=True))
    draw_orbit(img)
    return img


def make_brief_candles() -> Image.Image:
    img = chalk_board_bg()
    d = ImageDraw.Draw(img)
    chalk = (236, 232, 214)
    chalk_dim = (190, 200, 175)
    accent = (255, 196, 90)

    d.text((120, 90), "THE HIDDEN VARIABLE", fill=accent, font=font(32, chalk=True))
    d.text((120, 160), "TIME", fill=chalk, font=font(96, chalk=True))
    d.text((120, 290), "A civilisation lasting 10,000 years is a spark.", fill=chalk, font=font(34))
    d.text((120, 350), "One lasting a million years is a beacon.", fill=chalk, font=font(34))

    d.line([(120, 430), (1500, 430)], fill=(200, 195, 170), width=2)

    d.text((120, 480), "If technological species are brief candles…", fill=chalk, font=font(36, chalk=True))
    d.text((120, 560), "the galaxy can be full of life", fill=chalk_dim, font=font(32))
    d.text((120, 610), "and still empty of overlapping radio eras.", fill=chalk_dim, font=font(32))

    d.text((120, 740), "Crowded maths  ->  lonely sky", fill=accent, font=font(36, chalk=True))
    draw_orbit(img)
    return img


def encode_still(png: Path, mp4: Path, dur: float):
    # Still image: normal GOP is fine (no Ken Burns). Noisy chalk compresses poorly with keyint=1.
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-t", f"{dur:.3f}", "-vf", "format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "18",
        "-an", str(mp4),
    ], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cards = [
        ("card_drake_blackboard", make_drake_blackboard, 9.0),
        ("card_brief_candles", make_brief_candles, 7.0),
    ]
    for stem, maker, dur in cards:
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        maker().save(png)
        encode_still(png, mp4, dur)
        print("OK", mp4.name, f"{dur}s")


if __name__ == "__main__":
    main()
