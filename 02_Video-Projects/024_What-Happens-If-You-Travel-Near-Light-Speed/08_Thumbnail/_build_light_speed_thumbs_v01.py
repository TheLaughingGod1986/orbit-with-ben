#!/usr/bin/env python3
"""024 light-speed long thumbnails A/B/C v01 (J0047; brief THUMB_BRIEF_v01.md, Claude 8 Oct).

A  7 YEARS GONE?   NASA Black Marble night Earth (GSFC_20171208_Archive_e001593) on the left,
                   a blue star streak from the `starfield` graphic on the right.
B  YOU AGE SLOWER  NASA ISS orbital sunrise over Earth's limb (iss071e439624), limb in the lower half.
C  ONE-WAY TRIP    `starfield` graphic (graphics_v03, 26.5 s) dense blue core, slightly left of centre.

Words from the locked script v02. Rules: THUMBNAIL_AND_TITLE_RULES.md §2 / §2.A (no Orbit, subject
>= 1/3 of frame, near-black <= 30%, ~82 px text line on 720, text off the subject and out of the
bottom-right, yellow hook word, Arial Black). Title it sits under: "What Happens If You Travel Near Light Speed?".

  python3 _build_light_speed_thumbs_v01.py
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EDIT = HERE.parent / "07_Edit-Project"
POOL = EDIT / "nasa_pool_v01" / "024_harvest_v01"
EARTH = POOL / "GSFC_20171208_Archive_e001593.jpg"
LIMB = POOL / "iss071e439624.jpg"
STARFIELD = EDIT / "graphics_v03" / "starfield.mp4"
STARFIELD_T = 26.5
OUT = HERE / "abc_v01"
W, H = 1280, 720
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Black.ttf",
]
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STROKE = 7
CAP_TARGET = 82
TRACK = -4
MIN_GAP = 24

VARIANTS = [
    ("A", "7-years-gone", ["7 YEARS", "GONE?"], "7 YEARS"),
    ("B", "you-age-slower", ["YOU AGE", "SLOWER"], "SLOWER"),
    ("C", "one-way-trip", ["ONE-WAY", "TRIP"], "ONE-WAY"),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    sys.exit("Arial Black not found")


def arr(img: Image.Image) -> np.ndarray:
    return np.asarray(img, dtype=np.float32)


def img(a: np.ndarray) -> Image.Image:
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def screen(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return 255 - (255 - a) * (255 - b) / 255


def lift(a: np.ndarray, gamma: float) -> np.ndarray:
    return 255 * (a / 255) ** gamma


def glow_bg(cx: float, cy: float, reach: float, rgb_lo, rgb_hi, seed: int, stars: int = 320) -> np.ndarray:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip(1.0 - np.hypot(xx - cx, yy - cy) / reach, 0, 1) ** 1.5
    lo, hi = np.array(rgb_lo, np.float32), np.array(rgb_hi, np.float32)
    base = lo + (hi - lo) * g[..., None]
    rng = random.Random(seed)
    s = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(s)
    for _ in range(stars):
        x, y = rng.randrange(W), rng.randrange(H)
        r = 1 if rng.random() < 0.85 else 2
        sd.ellipse((x - r, y - r, x + r, y + r), fill=rng.randint(60, 200))
    s = arr(s.filter(ImageFilter.GaussianBlur(0.6)))[..., None] / 255
    return base * (1 - s) + np.array([230, 238, 255], np.float32) * s


def starfield_frame() -> Image.Image:
    tmp = OUT / "_starfield_frame.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(STARFIELD_T), "-i", str(STARFIELD),
                    "-frames:v", "1", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


# ---- A: night Earth + star streak -------------------------------------------------
A_D = 660
A_CX, A_CY = 40 + A_D // 2, H // 2 + 10


def variant_a(sf: Image.Image) -> tuple[Image.Image, tuple]:
    src = Image.open(EARTH).convert("RGB")
    box = src.convert("L").point(lambda v: 255 if v > 6 else 0).getbbox()
    side = max(box[2] - box[0], box[3] - box[1])
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    g = src.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)).resize((A_D, A_D), Image.LANCZOS)
    g = img(lift(arr(g), 0.62))
    g = ImageEnhance.Color(g).enhance(1.25)
    g = ImageEnhance.Contrast(g).enhance(1.08).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

    bg = glow_bg(A_CX + 40, A_CY, W * 0.85, (10, 16, 34), (40, 70, 130), seed=241)
    # star streak: the starfield core squeezed into a thin horizontal band, motion-blurred
    core = sf.crop((sf.width // 2 - 360, sf.height // 2 - 220, sf.width // 2 + 360, sf.height // 2 + 220))
    streak = core.resize((900, 90), Image.LANCZOS).filter(ImageFilter.BoxBlur(2))
    streak = img(arr(streak) * 1.4)
    band = np.zeros((H, W, 3), np.float32)
    sx, sy = 560, 470
    band_img = img(band)
    band_img.paste(streak, (sx, sy))
    band = arr(band_img.filter(ImageFilter.GaussianBlur(1.2)))
    band = screen(band, arr(band_img.filter(ImageFilter.GaussianBlur(18))) * 0.9)
    bg = screen(bg, band)

    tmp = Image.new("RGB", (W, H), BLACK)
    mask = Image.new("L", (A_D, A_D), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, A_D - 3, A_D - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.5))
    tmp.paste(g, (A_CX - A_D // 2, A_CY - A_D // 2), mask)
    planet = Image.new("L", (W, H), 0)
    planet.paste(mask, (A_CX - A_D // 2, A_CY - A_D // 2))
    rim = arr(tmp.filter(ImageFilter.GaussianBlur(40))) * 0.9
    out = img(screen(bg, rim))
    return Image.composite(tmp, out, planet), ("circle", A_CX, A_CY, A_D / 2)


# ---- B: ISS orbital sunrise limb --------------------------------------------------
def variant_b() -> tuple[Image.Image, tuple]:
    src = Image.open(LIMB).convert("RGB")
    cw = int(src.width * 0.80)
    ch = cw * 9 // 16
    x0 = src.width - cw
    im = src.crop((x0, 0, x0 + cw, ch)).resize((W, H), Image.LANCZOS)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32) / H
    warm = np.clip((yy - 0.45) / 0.3, 0, 1)[..., None]
    raw = arr(im)
    a = lift(raw, 0.66) * (1 - warm) + lift(raw, 0.45) * warm
    # warm-to-blue: warm the land under the limb, cool the sky above it
    land = np.clip((yy - 0.50) / 0.50, 0, 1)[..., None]
    a = screen(a, (1 - land) * np.array([70, 34, 8], np.float32) * (yy > 0.48)[..., None])
    a = a * (1 + warm * np.array([0.10, 0.02, -0.08], np.float32)) + (1 - warm) * np.array([0, 4, 14], np.float32)
    sky = glow_bg(W * 0.60, H * 0.42, W * 0.80, (10, 18, 40), (44, 84, 150), seed=242, stars=200)
    above = np.clip((0.43 - yy) / 0.12, 0, 1)[..., None]
    a = screen(a, sky * above)
    floor = np.clip((yy - 0.62) / 0.38, 0, 1)[..., None]
    a = screen(a, floor * np.array([62, 32, 12], np.float32))
    out = ImageEnhance.Contrast(img(a)).enhance(1.06)
    out = ImageEnhance.Color(out).enhance(1.12).filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
    return out, ("below", int(H * 0.40))


# ---- C: starfield dense blue core -------------------------------------------------
def variant_c(sf: Image.Image) -> tuple[Image.Image, tuple]:
    scale = 1.18
    big = sf.resize((int(sf.width * scale), int(sf.height * scale)), Image.LANCZOS)
    ccx, ccy = big.width // 2, big.height // 2
    tx, ty = 440, H // 2 + 40  # where the core lands in the thumb
    im = big.crop((ccx - tx, ccy - ty, ccx - tx + W, ccy - ty + H))
    a = arr(im)
    halo = arr(im.filter(ImageFilter.GaussianBlur(60))) * 1.5
    bg = glow_bg(tx, ty, W * 0.80, (8, 12, 30), (30, 56, 120), seed=243, stars=160)
    a = screen(screen(bg, halo), a)
    out = ImageEnhance.Color(img(a)).enhance(1.10)
    r = 0.26 * sf.height * scale  # dense-core radius in thumb px (measured on the 26.5 s frame)
    return out, ("circle", tx, ty, r)


# ---- text -------------------------------------------------------------------------
def line_w(draw: ImageDraw.ImageDraw, ln: str, f) -> int:
    return int(sum(draw.textlength(ch, font=f) for ch in ln) + TRACK * (len(ln) - 1) + 2 * STROKE)


def draw_line(draw: ImageDraw.ImageDraw, x: float, y: int, ln: str, f, fill) -> None:
    for ch in ln:
        draw.text((x, y), ch, font=f, fill=fill, stroke_width=STROKE, stroke_fill=BLACK)
        x += draw.textlength(ch, font=f) + TRACK


def gap_to_subject(box, subj) -> float:
    if subj[0] == "circle":
        _, cx, cy, r = subj
        dx = max(box[0] - cx, 0, cx - box[2])
        dy = max(box[1] - cy, 0, cy - box[3])
        return float(np.hypot(dx, dy)) - r
    return float(subj[1] - box[3])


def layout(draw, lines, f, x_right: int | None, x_left: int | None, y_top: int | None):
    cap = draw.textbbox((0, 0), "H", font=f)
    cap_h = cap[3] - cap[1]
    gap = int(cap_h * 0.32)
    block = len(lines) * cap_h + (len(lines) - 1) * gap
    y = (y_top if y_top is not None else (H - block) // 2 - 40) - cap[1]
    rows = []
    for ln in lines:
        w = line_w(draw, ln, f)
        x = x_left if x_left is not None else x_right - w
        top = y + cap[1] - STROKE
        rows.append((ln, x, y, (x, top, x + 4 + w, top + cap_h + 2 * STROKE + 5)))
        y += cap_h + gap
    return rows, cap_h


def place_text(im: Image.Image, lines, hook, subj, **pos) -> dict:
    d = ImageDraw.Draw(im)
    size = 140
    while size > 40:
        f = font(size)
        rows, cap_h = layout(d, lines, f, **pos)
        if cap_h <= CAP_TARGET and all(b[0] >= 20 and b[2] <= W - 20 for *_, b in rows) \
                and min(gap_to_subject(b, subj) for *_, b in rows) >= MIN_GAP:
            break
        size -= 1
    else:
        sys.exit("text cannot clear the subject")
    for ln, x, y, b in rows:
        assert not (b[2] > W * 0.70 and b[3] > H * 0.72), "text in the duration-badge corner"
        col = YELLOW if ln == hook else WHITE
        draw_line(d, x + 4, y + 5, ln, f, BLACK)
        draw_line(d, x, y, ln, f, col)
    return {"font_size": f.size, "cap_px": cap_h, "cap_share": round(cap_h / H, 3),
            "min_gap_px": round(min(gap_to_subject(b, subj) for *_, b in rows), 1), "tracking_px": TRACK}


def near_black(im: Image.Image) -> float:
    return round(float((np.asarray(im.convert("L")) < 26).mean()), 3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    sf = starfield_frame()
    builds = {
        "A": (variant_a(sf), {"x_right": W - 40, "x_left": None, "y_top": 90}),
        "B": (variant_b(), {"x_right": None, "x_left": 48, "y_top": 52}),
        "C": (variant_c(sf), {"x_right": W - 36, "x_left": None, "y_top": 46}),
    }
    sources = {
        "A": "NASA GSFC Black Marble (GSFC_20171208_Archive_e001593) + starfield graphic (graphics_v03, 26.5 s)",
        "B": "NASA ISS orbital sunrise (iss071e439624)",
        "C": "starfield graphic (graphics_v03, 26.5 s), code-rendered",
    }
    meta = {"version": "v01", "job": "J0047", "brief": "THUMB_BRIEF_v01.md",
            "title": "What Happens If You Travel Near Light Speed?", "variants": []}
    paths = []
    for key, slug, lines, hook in VARIANTS:
        (base, subj), pos = builds[key]
        im = base.copy()
        info = place_text(im, lines, hook, subj, **pos)
        p = OUT / f"light_speed_thumb_{key}_{slug}.jpg"
        im.save(p, quality=92, optimize=True)
        paths.append(p)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": p.name,
                                 "source": sources[key], "near_black": near_black(im), **info})
    sheet = OUT / "light_speed_thumbs_v01_small_size_check.jpg"
    subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
