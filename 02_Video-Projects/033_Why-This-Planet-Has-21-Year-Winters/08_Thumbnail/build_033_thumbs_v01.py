#!/usr/bin/env python3
"""033 Uranus long thumbnails A/B/C. £0. Pillow grade of verified harvest plates only.

A is one real JWST frame (rule 19): the same plate fills the frame. Dark sky is
shadow-lifted in its own colour. Bright pixels take the saturation. No second
plate, no character, no flat black slab.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/tools"))
import thumb_preview  # noqa: E402

HARVEST = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01"
)
FONT = Path(__file__).resolve().parent / "fonts" / "BebasNeue-Regular.ttf"
OUT = Path(__file__).resolve().parent

W, H = 1920, 1080
GOLD = (255, 214, 10)
WHITE = (255, 255, 255)
STROKE = (10, 12, 22)
TOP = 0.20  # clear band for the hook; subject starts below it


def open_rgb(name: str) -> Image.Image:
    return Image.open(HARVEST / name).convert("RGB")


def bbox(im: Image.Image, thresh: float) -> tuple[int, int, int, int]:
    L = np.asarray(im.convert("L"), dtype=np.float32)
    ys, xs = np.where(L > thresh)
    pad_x = int((xs.max() - xs.min()) * 0.06) + 12
    pad_y = int((ys.max() - ys.min()) * 0.06) + 12
    return (
        max(0, int(xs.min()) - pad_x),
        max(0, int(ys.min()) - pad_y),
        min(im.width, int(xs.max()) + 1 + pad_x),
        min(im.height, int(ys.max()) + 1 + pad_y),
    )


def lift_shadows(im: Image.Image, floor: float, tint: tuple[float, float, float]) -> Image.Image:
    """Bring luma under `floor` up toward `tint`, keeping the plate's own texture."""
    arr = np.asarray(im, dtype=np.float32)
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(14)), dtype=np.float32)
    detail = arr - blur
    bL = 0.2126 * blur[:, :, 0] + 0.7152 * blur[:, :, 1] + 0.0722 * blur[:, :, 2]
    add = np.clip(floor - bL, 0, None)
    tint_a = np.array(tint, dtype=np.float32)
    tint_l = float(0.2126 * tint_a[0] + 0.7152 * tint_a[1] + 0.0722 * tint_a[2])
    lifted = blur + (add / max(tint_l, 1.0))[..., None] * tint_a
    out = np.clip(lifted + detail * 0.85, 0, 255)
    return Image.fromarray(out.astype(np.uint8), "RGB")


def saturate_bright(im: Image.Image, gain: float, thresh: float = 48) -> Image.Image:
    hsv = np.asarray(im.convert("HSV"), dtype=np.float32)
    L = np.asarray(im.convert("L"), dtype=np.float32)
    weight = np.clip((L - thresh) / 50.0, 0, 1)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1.0 + (gain - 1.0) * weight), 0, 255)
    return Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")


def grade(im: Image.Image, floor: float, tint: tuple[float, float, float], sat: float, contrast: float) -> Image.Image:
    im = saturate_bright(im, sat)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    # Lift last so contrast cannot push the sky back under the near-black cap.
    return lift_shadows(im, floor, tint)


def contain_extend(src: Image.Image, canvas_w: int, canvas_h: int, shift_down: int = 0, zoom: float = 1.0) -> Image.Image:
    """Fit the whole plate, then extend its own edge sky to the canvas. No inner rectangle."""
    scale = min(canvas_w / src.width, canvas_h / src.height) * zoom
    nw, nh = max(1, int(src.width * scale)), max(1, int(src.height * scale))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    if resized.width > canvas_w or resized.height > canvas_h:
        cx = max(0, (resized.width - canvas_w) // 2)
        cy = max(0, (resized.height - canvas_h) // 2 - shift_down)
        cy = min(cy, max(0, resized.height - canvas_h))
        cx = min(cx, max(0, resized.width - canvas_w))
        resized = resized.crop((
            cx,
            cy,
            cx + min(canvas_w, resized.width),
            cy + min(canvas_h, resized.height),
        ))
    pad_x = canvas_w - resized.width
    pad_y = canvas_h - resized.height
    left = max(0, pad_x // 2)
    right = max(0, pad_x - left)
    # Positive shift_down moves the plate down and gives the hook more sky.
    if pad_y > 0:
        top = min(pad_y, max(0, pad_y // 2 + shift_down))
        bottom = pad_y - top
    else:
        top = bottom = 0
    arr = np.asarray(resized)
    padded = np.pad(arr, ((max(0, top), max(0, bottom)), (max(0, left), max(0, right)), (0, 0)), mode="edge")
    padded = padded[:canvas_h, :canvas_w]
    out = Image.fromarray(padded, "RGB")
    blur = out.filter(ImageFilter.GaussianBlur(22))
    mask = Image.new("L", out.size, 0)
    draw = ImageDraw.Draw(mask)
    reach = 90
    if left:
        draw.rectangle((0, 0, left + reach, canvas_h), fill=255)
    if right:
        draw.rectangle((canvas_w - right - reach, 0, canvas_w, canvas_h), fill=255)
    if top:
        draw.rectangle((0, 0, canvas_w, top + reach), fill=255)
    if bottom:
        draw.rectangle((0, canvas_h - bottom - reach, canvas_w, canvas_h), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    return Image.composite(blur, out, mask)


def place(src: Image.Image, floor: float, tint, sat: float, contrast: float, bright: float, shift_down: int = 0, zoom: float = 1.0) -> Image.Image:
    framed = contain_extend(src, W, H, shift_down, zoom)
    framed = ImageEnhance.Brightness(framed).enhance(bright)
    return grade(framed, floor, tint, sat, contrast)


def place_half(src: Image.Image, floor, tint, sat, contrast, bright, shift_down: int = 0, zoom: float = 1.0) -> Image.Image:
    half_w = W // 2
    framed = contain_extend(src, half_w, H, shift_down, zoom)
    framed = ImageEnhance.Brightness(framed).enhance(bright)
    return grade(framed, floor, tint, sat, contrast)


def fit_font(draw: ImageDraw.ImageDraw, words: list[str], max_w: int, target_h: int) -> ImageFont.FreeTypeFont:
    size = target_h + 30
    gap_ratio = 0.16
    while size > 70:
        font = ImageFont.truetype(str(FONT), size)
        gap = font.size * gap_ratio
        total = sum(draw.textlength(w, font=font) for w in words) + gap * (len(words) - 1)
        cap = draw.textbbox((0, 0), "Hg", font=font)
        cap_h = cap[3] - cap[1]
        if total <= max_w and cap_h <= target_h:
            return font
        size -= 2
    return ImageFont.truetype(str(FONT), 72)


def draw_hook(im: Image.Image, parts: list[tuple[str, tuple[int, int, int]]]) -> None:
    draw = ImageDraw.Draw(im)
    words = [p[0] for p in parts]
    font = fit_font(draw, words, int(W * 0.92), int(H * 0.118))
    stroke = max(8, font.size // 15)
    gap = font.size * 0.16
    total = sum(draw.textlength(w, font=font) for w in words) + gap * (len(words) - 1)
    x = (W - total) / 2
    cap = draw.textbbox((0, 0), "Hg", font=font)
    cap_h = cap[3] - cap[1]
    band_h = int(H * TOP)
    y = max(14, (band_h - cap_h) / 2 - cap[1])
    for word, colour in parts:
        draw.text((x, y), word, font=font, fill=colour, stroke_width=stroke, stroke_fill=STROKE)
        x += draw.textlength(word, font=font) + gap


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    navy = (22, 36, 92)
    teal = (16, 92, 128)

    a = place(
        open_rgb("weic2332a_hires.jpg"),
        floor=34,
        tint=navy,
        sat=2.1,
        contrast=1.14,
        bright=1.08,
        shift_down=28,
        zoom=1.06,
    )
    draw_hook(a, [("21-YEAR", WHITE), ("WINTER", GOLD)])

    left = place_half(
        open_rgb("PIA18182.jpg"),
        floor=46,
        tint=(18, 70, 98),
        sat=1.9,
        contrast=1.1,
        bright=1.12,
        shift_down=8,
    )
    right = place_half(
        open_rgb("weic2310a_unannotated.png"),
        floor=38,
        tint=teal,
        sat=2.2,
        contrast=1.16,
        bright=1.12,
        shift_down=8,
    )
    b = Image.new("RGB", (W, H))
    b.paste(left, (0, 0))
    b.paste(right, (W // 2, 0))
    draw_hook(b, [("COLDER", GOLD), ("THAN", WHITE), ("NEPTUNE", WHITE)])

    c = place(
        open_rgb("weic2310a_unannotated.png"),
        floor=70,
        tint=(20, 140, 168),
        sat=2.2,
        contrast=1.1,
        bright=1.22,
        shift_down=90,
        zoom=0.86,
    )
    draw_hook(c, [("97.77°", GOLD), ("SIDEWAYS", WHITE)])

    made = {"A": a, "B": b, "C": c}
    for key, im in made.items():
        path = OUT / f"033_thumb_{key}_v01.jpg"
        im.save(path, quality=92, subsampling=0)
        r = thumb_preview.score(path, "long")
        print(key, r["saturation"], f"{r['near_black']:.1%}", "FAIL" if r["fails"] else "PASS", r["fails"])


if __name__ == "__main__":
    main()
