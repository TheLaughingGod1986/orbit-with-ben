#!/usr/bin/env python3
"""Build OWB:064 Every Planet Explained Thumbnails A, B, C as J3719_v02 (£0, Pillow).

Implements 05_Analytics/tests/panels/owb-064-every-planet/DECISION.md (J3719) & J3817:
- Zero Orbit character on any thumbnail; £0 cash, 0 Flow/Vertex credits.
- Verified real NASA/JPL/ESA spacecraft plates on studio-live only (PIA00271 removed).
- Clean dark-navy top band (y = 0..21%) with zero letters touching planets or dividers.
- Bottom-right duration zone (x > 75%, y > 78%) completely clear.
- NASA/NOAA Suomi NPP Blue Marble 2012 Earth (PIA18033) scale/story cue on all three (§2.A.5).
- All three PASS thumb_preview.py long --score (sat >= 120, Variant B <= 175, near_black <= 28%).
- Writes media strictly to NAS J3719_v02/ (no media committed to git); writes THUMB_SCORES_v02.json to both NAS and repo.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/tools"))
import thumb_preview  # noqa: E402

HARVEST_064 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes/03_Reference-Material/harvest_J3022_v01"
)
HARVEST_033 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01"
)
HARVEST_031 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01"
)
NAS_OUT = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/J3719_v02"
)
REPO_OUT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/08_Thumbnail/fonts/BebasNeue-Regular.ttf"

W, H = 1920, 1080
TOP_BAND_H = 226  # 20.9% of 1080 (cleanly inside y = 0..21%)
YELLOW = (255, 224, 0)  # #FFE000
WHITE = (255, 255, 255)
STROKE = (6, 10, 22)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)


def make_deep_navy_backdrop(
    w: int = W,
    h: int = H,
    top_band_rgb: tuple[float, float, float] = (8.0, 18.0, 46.0),
    mid_rgb: tuple[float, float, float] = (12.0, 28.0, 72.0),
    nebula_rgb: tuple[float, float, float] = (24.0, 52.0, 118.0),
    glow_center: tuple[float, float] = (0.44, 0.62),
    warm_left: float = 0.0,
    star_count: int = 95,
    seed: int = 6402,
) -> Image.Image:
    """Rich deep-navy cosmic space backdrop (no periwinkle flatness, no noisy paint dots)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xn = xx / float(w)
    yn = yy / float(h)

    # Smooth cosmic radial nebula glow in lower/mid space
    rx = (xn - glow_center[0]) / 0.58
    ry = (yn - glow_center[1]) / 0.50
    rad = np.sqrt(rx * rx + ry * ry)
    neb = np.exp(-rad * rad * 1.45)

    # Secondary subtle diagonal deep-space sheen
    sheen = np.exp(-((xn - 0.72) ** 2 / 0.28 + (yn - 0.45) ** 2 / 0.24))

    r = mid_rgb[0] + (nebula_rgb[0] - mid_rgb[0]) * neb + 8.0 * sheen
    g = mid_rgb[1] + (nebula_rgb[1] - mid_rgb[1]) * neb + 16.0 * sheen
    b = mid_rgb[2] + (nebula_rgb[2] - mid_rgb[2]) * neb + 34.0 * sheen

    if warm_left > 0.0:
        # Subtle warm amber solar rim at far-left edge behind inner planets
        sd = np.sqrt(((xn + 0.05) / 0.28) ** 2 + ((yn - 0.76) / 0.34) ** 2)
        wg = np.exp(-sd * sd * 1.7) * warm_left
        r = r + 135.0 * wg
        g = g + 78.0 * wg
        b = b + 16.0 * wg

    # Blend smoothly into clean dark-navy top band (y = 0..21%) with a natural cinematic gradient
    band_t = np.clip((yy - (TOP_BAND_H - 42.0)) / 105.0, 0.0, 1.0)
    band_t = band_t * band_t * (3.0 - 2.0 * band_t)
    r = top_band_rgb[0] * (1.0 - band_t) + r * band_t
    g = top_band_rgb[1] * (1.0 - band_t) + g * band_t
    b = top_band_rgb[2] * (1.0 - band_t) + b * band_t

    # Very gentle edge vignette so bottom-right stays clean deep navy without hitting flat black
    edge = np.clip(((xn - 0.5) * 1.55) ** 2 + ((yn - 0.52) * 1.45) ** 2, 0.0, 1.4)
    vig = 1.0 - 0.18 * np.clip(edge - 0.45, 0.0, 1.0)
    r = np.clip(r * vig, 0, 255)
    g = np.clip(g * vig, 0, 255)
    b = np.clip(b * vig, 0, 255)

    bg = Image.fromarray(np.stack([r, g, b], axis=-1).astype(np.uint8), "RGB").convert("RGBA")

    # Subtle distant pinpoint stars (strictly below top band, small and soft — never speckled paint dots)
    if star_count > 0:
        rng = np.random.default_rng(seed)
        stars = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stars)
        for _ in range(star_count):
            sx = int(rng.integers(12, w - 12))
            sy = int(rng.integers(TOP_BAND_H + 14, h - 12))
            br = int(rng.integers(140, 235))
            al = int(rng.integers(55, 135))
            if rng.random() < 0.18:
                sd.ellipse((sx - 1, sy - 1, sx + 1, sy + 1), fill=(br, br, 255, al))
            else:
                sd.point((sx, sy), fill=(br, br, 255, al))
        stars = stars.filter(ImageFilter.GaussianBlur(0.5))
        bg = Image.alpha_composite(bg, stars)

    return bg


def extract_sphere(
    path: Path,
    size: int,
    circle: tuple[float, float, float],
    crop_region: tuple[int, int, int, int] | None = None,
    sat: float = 1.32,
    bright: float = 1.06,
    contrast: float = 1.08,
    color_gain: tuple[float, float, float] = (1.0, 1.0, 1.0),
    shadow_lift_rgb: tuple[float, float, float] = (10.0, 22.0, 52.0),
    feather_frac: float = 0.018,
    inset_frac: float = 0.010,
) -> Image.Image:
    """Extract a NASA planet globe cleanly using its true geometric circle (zero black cutout halo)."""
    im = Image.open(path).convert("RGB")
    if crop_region is not None:
        im = im.crop(crop_region)
    cx, cy, rad = circle
    # Inset radius slightly so zero outer space black pixels ever enter the disk
    r_use = rad * (1.0 - inset_frac)
    x0 = cx - r_use
    y0 = cy - r_use
    x1 = cx + r_use
    y1 = cy + r_use

    # Pad if circle extends past image bounds
    pad_l = max(0, int(math.ceil(-x0)))
    pad_t = max(0, int(math.ceil(-y0)))
    pad_r = max(0, int(math.ceil(x1 - im.width)))
    pad_b = max(0, int(math.ceil(y1 - im.height)))
    if pad_l or pad_t or pad_r or pad_b:
        padded = Image.new("RGB", (im.width + pad_l + pad_r, im.height + pad_t + pad_b), (0, 0, 0))
        padded.paste(im, (pad_l, pad_t))
        im = padded
        x0 += pad_l
        x1 += pad_l
        y0 += pad_t
        y1 += pad_t

    im = im.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))))
    im = im.resize((size, size), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(contrast)

    arr = np.asarray(im, dtype=np.float32)
    arr[:, :, 0] *= color_gain[0]
    arr[:, :, 1] *= color_gain[1]
    arr[:, :, 2] *= color_gain[2]
    arr = np.clip(arr, 0, 255)

    # Gently blend near-black night/shadow limbs into deep-navy cosmic space so there is ZERO black halo
    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    shadow_w = np.clip((24.0 - lum) / 24.0, 0.0, 1.0) ** 1.4
    for ch in range(3):
        arr[:, :, ch] = arr[:, :, ch] * (1.0 - 0.65 * shadow_w) + shadow_lift_rgb[ch] * (0.65 * shadow_w)

    # Smooth anti-aliased radial alpha mask with feathered limb
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    mid = (size - 1) / 2.0
    dist = np.sqrt((xx - mid) ** 2 + (yy - mid) ** 2) / mid
    f_edge = max(0.012, feather_frac)
    alpha = np.clip((1.0 - dist) / f_edge, 0.0, 1.0)
    alpha = alpha * alpha * (3.0 - 2.0 * alpha)

    # Extra soft fade where outer limb is in deep shadow (gibbous terminator melts seamlessly into deep space!)
    outer_ring = np.clip((dist - 0.72) / 0.28, 0.0, 1.0)
    dark_outer = np.clip((lum - 14.0) / 34.0, 0.0, 1.0)
    alpha = alpha * (1.0 - outer_ring * (1.0 - dark_outer) * 0.96)

    out = np.dstack([np.clip(arr, 0, 255), np.clip(alpha * 255.0, 0, 255)]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def extract_saturn_clean(
    path: Path,
    target_w: int,
    sat: float = 1.42,
    bright: float = 1.12,
    contrast: float = 1.14,
    angle_deg: float = 0.0,
) -> Image.Image:
    """Extract Cassini PIA11141 Saturn + complete rings cleanly with zero black box or stray corner moon."""
    im = Image.open(path).convert("RGB")
    # Crop tightly around Saturn + full ring span (excluding faint lower-left moon at y>1980, x<450)
    im = im.crop((320, 320, 4280, 1990))
    arr0 = np.asarray(im, dtype=np.float32).copy()
    # Mask out tiny stray background moons/stars away from planet & rings
    h0, w0 = arr0.shape[:2]
    yy0, xx0 = np.mgrid[0:h0, 0:w0].astype(np.float32)
    # Keep Saturn globe ellipse + ring ellipse; zero stray dots outside both
    globe_d = ((xx0 - w0 * 0.502) / (w0 * 0.215)) ** 2 + ((yy0 - h0 * 0.505) / (h0 * 0.485)) ** 2
    ring_d = ((xx0 - w0 * 0.500) / (w0 * 0.498)) ** 2 + ((yy0 - h0 * 0.485) / (h0 * 0.165)) ** 2
    keep = (globe_d <= 1.06) | (ring_d <= 1.06)
    arr0[~keep] = 0.0

    im = Image.fromarray(arr0.astype(np.uint8), "RGB")
    target_h = int(round(im.height * (target_w / im.width)))
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(contrast)

    arr = np.asarray(im, dtype=np.float32)
    # Warm golden-cream highlight polish
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.06, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.02, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.94, 0, 255)

    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    # Preserve crisp ring details & softly fade pure-black space around Saturn
    alpha = np.clip((lum - 8.0) / 22.0, 0.0, 1.0)
    # Keep interior of Saturn's globe opaque even near shadowed southern/northern edge
    hh, ww = lum.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    globe_inner = ((xx - ww * 0.502) / (ww * 0.192)) ** 2 + ((yy - hh * 0.505) / (hh * 0.445)) ** 2
    globe_fill = np.clip((1.0 - globe_inner) / 0.08, 0.0, 1.0)
    alpha = np.maximum(alpha, globe_fill * 0.96)

    rgba = Image.fromarray(np.dstack([arr, alpha * 255.0]).astype(np.uint8), "RGBA")
    if abs(angle_deg) > 0.01:
        rgba = rgba.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rgba


def add_planet_glow(
    canvas: Image.Image,
    cx: int,
    cy: int,
    rx: int,
    ry: int,
    color: tuple[int, int, int],
    alpha: int = 58,
    blur: int = 24,
) -> Image.Image:
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=color + (alpha,))
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(canvas, glow)


def draw_top_band_text(
    im: Image.Image,
    segments: list[tuple[str, tuple[int, int, int]]],
    font_size: int = 166,
    y_center: int = 114,
    gap: int = 30,
    stroke_w: int = 10,
) -> Image.Image:
    """Draw heavy Bebas Neue all-caps hook text cleanly centered inside y = 0..21%."""
    rgba = im.convert("RGBA")
    font = load_font(font_size)
    draw = ImageDraw.Draw(rgba)

    boxes = [draw.textbbox((0, 0), txt, font=font, stroke_width=stroke_w) for txt, _ in segments]
    widths = [b[2] - b[0] for b in boxes]
    max_h = max(b[3] - b[1] for b in boxes)
    min_top = min(b[1] for b in boxes)
    total_w = sum(widths) + gap * (len(segments) - 1)
    x_start = (W - total_w) // 2
    y_pos = int(round(y_center - max_h / 2.0 - min_top))

    # Crisp drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    cx = x_start
    for (txt, _), w_seg in zip(segments, widths):
        sd.text((cx + 5, y_pos + 7), txt, font=font, fill=(0, 0, 0, 220), stroke_width=stroke_w + 2, stroke_fill=(0, 0, 0, 220))
        cx += w_seg + gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    rgba = Image.alpha_composite(rgba, shadow)

    draw = ImageDraw.Draw(rgba)
    cx = x_start
    for (txt, col), w_seg in zip(segments, widths):
        draw.text((cx, y_pos), txt, font=font, fill=col + (255,), stroke_width=stroke_w, stroke_fill=STROKE + (255,))
        cx += w_seg + gap
    return rgba.convert("RGB")


def build_thumb_A() -> Image.Image:
    """Variant A (Lead Arm 1): 8 EXTREME WORLDS — Deep-navy cosmic hierarchy, zero halos."""
    bg = make_deep_navy_backdrop(
        top_band_rgb=(7.0, 16.0, 44.0),
        mid_rgb=(11.0, 26.0, 68.0),
        nebula_rgb=(24.0, 56.0, 126.0),
        glow_center=(0.45, 0.62),
        warm_left=0.72,
        star_count=85,
        seed=6411,
    )

    # Extract all 8 REAL NASA planets (PIA00271 replaced with PIA23791 right globe only!)
    mercury = extract_sphere(
        HARVEST_064 / "PIA15162.jpg", 122, circle=(1072.5, 1072.5, 975.0),
        sat=1.25, bright=1.18, contrast=1.16, color_gain=(1.04, 1.00, 0.96),
    )
    venus = extract_sphere(
        HARVEST_064 / "PIA23791.jpg", 184, circle=(551.0, 548.0, 467.0),
        crop_region=(1160, 0, 2245, 1096),
        sat=1.55, bright=1.06, contrast=1.14, color_gain=(1.10, 0.96, 0.72),
    )
    earth = extract_sphere(
        HARVEST_033 / "PIA18033.jpg", 232, circle=(3996.0, 3996.0, 3440.0),
        sat=1.48, bright=1.10, contrast=1.12,
    )
    mars = extract_sphere(
        HARVEST_031 / "PIA00407.jpg", 162, circle=(3393.0, 3393.0, 3380.0),
        sat=1.50, bright=1.08, contrast=1.12, color_gain=(1.10, 0.96, 0.86),
    )
    jupiter = extract_sphere(
        HARVEST_064 / "PIA22946.jpg", 550, circle=(1461.0, 1495.0, 1082.0),
        sat=1.42, bright=1.10, contrast=1.14,
    )
    saturn = extract_saturn_clean(
        HARVEST_064 / "PIA11141.jpg", target_w=685, sat=1.46, bright=1.14, contrast=1.15, angle_deg=-9.5,
    )
    uranus = extract_sphere(
        HARVEST_033 / "PIA18182.jpg", 198, circle=(852.0, 855.0, 688.0),
        sat=1.55, bright=0.98, contrast=1.18, color_gain=(0.76, 1.04, 1.14),
    )
    neptune = extract_sphere(
        HARVEST_064 / "PIA01492.jpg", 188, circle=(1072.0, 1052.0, 1012.0),
        sat=1.45, bright=1.12, contrast=1.14, inset_frac=0.024,
    )

    # Clear focal hierarchy: Jupiter + Saturn dominate lower-centre/mid (>35% frame);
    # NASA/NOAA Suomi NPP Blue Marble 2012 Earth stands crisp lower-left; all worlds below y=226 and clear of bottom-right (x>1440, y>842).
    # Placed back-to-front along depth arc with clean separation and zero ring collisions.
    items = [
        # (img, cx, cy, glow_rgb, glow_alpha, rx_override, ry_override)
        (neptune, 1790, 498, (40, 115, 255), 48, None, None),
        (uranus,  1590, 360, (75, 210, 245), 44, None, None),
        (mercury,  104, 838, (185, 170, 150), 34, None, None),
        (mars,     414, 504, (225, 108, 48), 42, None, None),
        (venus,    214, 650, (245, 185, 80), 46, None, None),
        (earth,    352, 845, (55, 155, 255), 58, None, None),
        (saturn,  1328, 574, (240, 198, 115), 26, 215, 165),
        (jupiter,  758, 676, (235, 155, 88), 46, None, None),
    ]

    for pl, cx, cy, gcol, gal, rx_o, ry_o in items:
        rx = rx_o if rx_o is not None else int(pl.width * 0.52)
        ry = ry_o if ry_o is not None else int(pl.height * 0.52)
        bg = add_planet_glow(bg, cx, cy, rx, ry, gcol, alpha=gal, blur=26)
        bg.alpha_composite(pl, (cx - pl.width // 2, cy - pl.height // 2))

    out = bg.convert("RGB")
    out = draw_top_band_text(
        out,
        [("8", WHITE), ("EXTREME", YELLOW), ("WORLDS", WHITE)],
        font_size=168,
        y_center=113,
        gap=28,
        stroke_w=10,
    )
    return out


def build_thumb_B() -> Image.Image:
    """Variant B (Challenger B): 464°C (Venus) | -224°C (Uranus) + NASA/NOAA Suomi NPP Blue Marble 2012 Earth scale cue.

    - Real Mariner 10 Venus clouds (PIA23791 right globe) warm golden-amber at moderate sat (~150-165, <=175).
    - Real Voyager 2 Uranus (PIA18182) crisp ice-cyan matching -224.2°C coldest planetary atmosphere.
    - Clean dark-navy top band (y=0..21%), divider stops below text band, bold readable minus sign, no 'TO'.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xn = xx / float(W)
    yn = yy / float(H)

    # Split lower cosmic backdrop: subtle warm amber-navy left, crisp glacial-navy right
    left_mask = (xx < W // 2).astype(np.float32)
    # Soft glow behind each planet center
    dl = np.sqrt(((xn - 0.235) / 0.32) ** 2 + ((yn - 0.625) / 0.38) ** 2)
    dr = np.sqrt(((xn - 0.765) / 0.32) ** 2 + ((yn - 0.625) / 0.38) ** 2)
    gl = np.exp(-dl * dl * 1.4)
    gr = np.exp(-dr * dr * 1.4)

    r_l = 24.0 + 96.0 * gl
    g_l = 18.0 + 52.0 * gl
    b_l = 22.0 + 18.0 * gl

    r_r = 10.0 + 14.0 * gr
    g_r = 26.0 + 68.0 * gr
    b_r = 56.0 + 108.0 * gr

    r = r_l * left_mask + r_r * (1.0 - left_mask)
    g = g_l * left_mask + g_r * (1.0 - left_mask)
    b = b_l * left_mask + b_r * (1.0 - left_mask)

    # Clean dark-navy top band y = 0..226 with smooth transition below
    band_t = np.clip((yy - (TOP_BAND_H - 12.0)) / 36.0, 0.0, 1.0)
    band_t = band_t * band_t * (3.0 - 2.0 * band_t)
    top_r, top_g, top_b = 8.0, 18.0, 46.0
    r = top_r * (1.0 - band_t) + r * band_t
    g = top_g * (1.0 - band_t) + g * band_t
    b = top_b * (1.0 - band_t) + b * band_t

    bg = Image.fromarray(np.stack([np.clip(r, 0, 255), np.clip(g, 0, 255), np.clip(b, 0, 255)], axis=-1).astype(np.uint8), "RGB").convert("RGBA")

    # Left planet: REAL Mariner 10 Venus clouds (PIA23791 right globe only!), warm golden-amber (NOT Sun-lava)
    venus = extract_sphere(
        HARVEST_064 / "PIA23791.jpg",
        size=790,
        circle=(551.0, 548.0, 467.0),
        crop_region=(1160, 0, 2245, 1096),
        sat=1.55,
        bright=1.02,
        contrast=1.22,
        color_gain=(1.12, 0.90, 0.56),
        shadow_lift_rgb=(28.0, 20.0, 16.0),
        feather_frac=0.020,
    )
    # Right planet: REAL Voyager 2 Uranus (PIA18182), crisp glacial ice-cyan with subtle real limb shading
    uranus = extract_sphere(
        HARVEST_033 / "PIA18182.jpg",
        size=790,
        circle=(852.0, 855.0, 688.0),
        sat=1.62,
        bright=0.95,
        contrast=1.24,
        color_gain=(0.66, 1.03, 1.15),
        shadow_lift_rgb=(12.0, 30.0, 60.0),
        feather_frac=0.020,
    )

    # Shift both globes downward below y = 226 top band: top limb at y = 256!
    v_cx, v_cy = 468, 652
    u_cx, u_cy = 1452, 652

    # Clip left half and right half cleanly to their respective halves so planets never bleed across seam
    left_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    left_layer = add_planet_glow(left_layer, v_cx, v_cy, 415, 415, (235, 155, 55), alpha=65, blur=34)
    left_layer.alpha_composite(venus, (v_cx - venus.width // 2, v_cy - venus.height // 2))
    # Crop left_layer strictly to x < 956
    l_arr = np.asarray(left_layer).copy()
    l_arr[:, 956:, 3] = 0
    bg = Image.alpha_composite(bg, Image.fromarray(l_arr, "RGBA"))

    right_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    right_layer = add_planet_glow(right_layer, u_cx, u_cy, 415, 415, (70, 200, 245), alpha=62, blur=34)
    right_layer.alpha_composite(uranus, (u_cx - uranus.width // 2, u_cy - uranus.height // 2))
    r_arr = np.asarray(right_layer).copy()
    r_arr[:, :964, 3] = 0
    bg = Image.alpha_composite(bg, Image.fromarray(r_arr, "RGBA"))

    # Crisp luminous white vertical divider stopping cleanly BELOW the top band (y = 232..1080)
    div_top = TOP_BAND_H + 6
    line_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_glow)
    ld.rectangle((952, div_top, 968, H), fill=(195, 232, 255, 145))
    line_glow = line_glow.filter(ImageFilter.GaussianBlur(10))
    bg = Image.alpha_composite(bg, line_glow)
    d = ImageDraw.Draw(bg)
    d.rectangle((957, div_top, 963, H), fill=(255, 255, 255, 245))

    # Crisp subtle horizontal separator accent right under top band (optional hairline for polish)
    d.rectangle((0, div_top - 2, W, div_top), fill=(120, 165, 225, 70))

    # Crisp small NASA/NOAA Suomi NPP Blue Marble 2012 Earth (PIA18033) on lower-centre seam for scale (clear of bottom-right!)
    earth = extract_sphere(
        HARVEST_033 / "PIA18033.jpg",
        size=196,
        circle=(3996.0, 3996.0, 3440.0),
        sat=1.45,
        bright=1.10,
        contrast=1.14,
    )
    e_cx, e_cy = 960, 882
    bg = add_planet_glow(bg, e_cx, e_cy, 114, 114, (65, 175, 255), alpha=90, blur=18)
    # Thin crisp circular framing ring around Earth scale anchor so it pops against the white seam
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((e_cx - 101, e_cy - 101, e_cx + 101, e_cy + 101), outline=(225, 242, 255, 210), width=4)
    bg = Image.alpha_composite(bg, ring)
    bg.alpha_composite(earth, (e_cx - earth.width // 2, e_cy - earth.height // 2))

    # Top-band text: "464°C" (#FFE000, left above Venus) and "-224°C" (#FFFFFF, right above Uranus, bold custom minus)
    font = load_font(176)
    stroke_w = 10
    y_center = 114

    def draw_centered_text_at(canvas: Image.Image, text: str, col: tuple[int, int, int], center_x: int, custom_minus: bool = False) -> Image.Image:
        c = canvas.convert("RGBA")
        dr = ImageDraw.Draw(c)
        bb = dr.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        y_pos = int(round(y_center - th / 2.0 - bb[1]))

        minus_w = 54 if custom_minus else 0
        minus_gap = 14 if custom_minus else 0
        total_w = minus_w + minus_gap + tw
        x0 = center_x - total_w // 2
        tx = x0 + minus_w + minus_gap

        # Drop shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        if custom_minus:
            my = y_center + 4
            sd.rounded_rectangle(
                (x0 - stroke_w + 5, my - 13 - stroke_w + 7, x0 + minus_w + stroke_w + 5, my + 13 + stroke_w + 7),
                radius=6,
                fill=(0, 0, 0, 220),
            )
        sd.text((tx + 5, y_pos + 7), text, font=font, fill=(0, 0, 0, 220), stroke_width=stroke_w + 2, stroke_fill=(0, 0, 0, 220))
        sh = sh.filter(ImageFilter.GaussianBlur(6))
        c = Image.alpha_composite(c, sh)

        dr = ImageDraw.Draw(c)
        if custom_minus:
            my = y_center + 4
            # Stroke outline for bold minus bar
            dr.rounded_rectangle(
                (x0 - stroke_w, my - 12 - stroke_w, x0 + minus_w + stroke_w, my + 12 + stroke_w),
                radius=5,
                fill=STROKE + (255,),
            )
            # Crisp white bold minus bar (54 x 24 px -> ~5 x 2.2 px at 168x94, unmistakable!)
            dr.rounded_rectangle(
                (x0, my - 12, x0 + minus_w, my + 12),
                radius=3,
                fill=col + (255,),
            )
        dr.text((tx, y_pos), text, font=font, fill=col + (255,), stroke_width=stroke_w, stroke_fill=STROKE + (255,))
        return c

    bg = draw_centered_text_at(bg, "464°C", YELLOW, center_x=480, custom_minus=False)
    bg = draw_centered_text_at(bg, "224°C", WHITE, center_x=1440, custom_minus=True)
    return bg.convert("RGB")


def build_thumb_C() -> Image.Image:
    """Variant C (Challenger C — Rule 19 single real NASA spacecraft hero): REAL NASA PHOTOS.

    - One uncropped, aspect-preserved real NASA Cassini Saturn-and-rings hero frame (PIA11141.jpg) filling >40% of frame.
    - Deep-navy graded space (zero top-bar leak, zero triptych, zero dark-disc artifact).
    - Crisp NASA/NOAA Suomi NPP Blue Marble 2012 Earth (PIA18033) scale inset on lower-left with thin white pointer (§2.B.4).
    - Top-band text 'REAL NASA PHOTOS' completely off Saturn and its rings.
    """
    bg = make_deep_navy_backdrop(
        top_band_rgb=(8.0, 18.0, 48.0),
        mid_rgb=(12.0, 28.0, 74.0),
        nebula_rgb=(26.0, 56.0, 124.0),
        glow_center=(0.52, 0.62),
        warm_left=0.0,
        star_count=70,
        seed=6433,
    )

    # Full UNCROPPED, aspect-preserved PIA11141.jpg (4613 x 2233 -> 1920 x 929)
    # Wait: Saturn's visible bounding box in 4613x2233 is x=346..4255 (3909 wide) and y=356..1957 (1601 tall).
    # Scaling full 4613x2233 proportionally to width=2040 gives height=987, so Saturn rings span 1729 px (90% of 1920!)
    # and Saturn's globe stands 708 px tall (65.6% of 1080!), completely uncropped and exact 1:1 aspect ratio!
    sat_raw = Image.open(HARVEST_064 / "PIA11141.jpg").convert("RGB")
    scale = 2040.0 / sat_raw.width
    new_w = int(round(sat_raw.width * scale))
    new_h = int(round(sat_raw.height * scale))
    sat_im = sat_raw.resize((new_w, new_h), Image.Resampling.LANCZOS)
    sat_im = ImageEnhance.Color(sat_im).enhance(1.52)
    sat_im = ImageEnhance.Brightness(sat_im).enhance(1.13)
    sat_im = ImageEnhance.Contrast(sat_im).enhance(1.14)

    s_arr = np.asarray(sat_im, dtype=np.float32)
    # Rich natural Cassini gold enhancement
    s_arr[:, :, 0] = np.clip(s_arr[:, :, 0] * 1.07, 0, 255)
    s_arr[:, :, 1] = np.clip(s_arr[:, :, 1] * 1.02, 0, 255)
    s_arr[:, :, 2] = np.clip(s_arr[:, :, 2] * 0.93, 0, 255)

    # Softly lift PIA11141's pure black space into transparent so deep-navy cosmic space shines cleanly behind it
    lum = 0.2126 * s_arr[:, :, 0] + 0.7152 * s_arr[:, :, 1] + 0.0722 * s_arr[:, :, 2]
    alpha = np.clip((lum - 7.0) / 22.0, 0.0, 1.0)

    # Keep Saturn's globe + rings; suppress the stray faint background moon in bottom-left of PIA11141
    yy_s, xx_s = np.mgrid[0:new_h, 0:new_w].astype(np.float32)
    g_cx, g_cy = new_w * 0.5025, new_h * 0.5177
    g_rx, g_ry = new_w * 0.165, new_h * 0.345
    g_d = ((xx_s - g_cx) / g_rx) ** 2 + ((yy_s - g_cy) / g_ry) ** 2
    r_d = ((xx_s - new_w * 0.500) / (new_w * 0.445)) ** 2 + ((yy_s - new_h * 0.495) / (new_h * 0.155)) ** 2
    sat_region = (g_d <= 1.25) | (r_d <= 1.15)
    alpha = np.where(sat_region, alpha, 0.0)
    alpha = np.maximum(alpha, np.clip((1.0 - g_d) / 0.08, 0.0, 1.0) * 0.96)

    sat_rgba = Image.fromarray(np.dstack([s_arr, alpha * 255.0]).astype(np.uint8), "RGBA")

    # Place Saturn centered horizontally (slight right shift +24 px to balance lower-left Earth scale inset),
    # vertically so top pole sits cleanly below y = 226 top band:
    paste_x = (W - new_w) // 2 + 24
    paste_y = 128
    # Subtle golden atmospheric bloom tightly behind Saturn's globe
    sat_cx = paste_x + int(g_cx)
    sat_cy = paste_y + int(g_cy)
    bg = add_planet_glow(bg, sat_cx, sat_cy, 380, 320, (225, 185, 105), alpha=32, blur=44)
    bg.alpha_composite(sat_rgba, (paste_x, paste_y))

    # Crisp NASA/NOAA Suomi NPP Blue Marble 2012 Earth (PIA18033) scale inset on lower-left (clear of rings & bottom-right!)
    # Saturn globe height here is ~708 px; true 1:9.45 scale would be ~75 px.
    # Placed as a clearly framed 132 px circular scale inset (~1.76x enlarged for 168x94 phone legibility)
    # with a single thin white pointer arrow (§2.B.4) pointing directly at Earth, documented in BUILD_REPORT_v02.md.
    earth = extract_sphere(
        HARVEST_033 / "PIA18033.jpg",
        size=132,
        circle=(3996.0, 3996.0, 3440.0),
        sat=1.50,
        bright=1.12,
        contrast=1.14,
    )
    e_cx, e_cy = 236, 888
    bg = add_planet_glow(bg, e_cx, e_cy, 80, 80, (55, 165, 255), alpha=75, blur=18)

    # Framed circular scale ring + single thin white pointer arrow (§2.B.4) pointing AT Earth for scale
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    ring_r = 71
    od.ellipse((e_cx - ring_r, e_cy - ring_r, e_cx + ring_r, e_cy + ring_r), outline=(235, 245, 255, 230), width=3)

    # Thin white pointer arrow from Saturn side pointing directly at the Earth scale inset
    p_start = (e_cx + 232, e_cy - 104)
    p_end = (e_cx + 82, e_cy - 36)
    od.line([p_start, p_end], fill=STROKE + (220,), width=9)
    od.line([p_start, p_end], fill=(255, 255, 255, 245), width=4)
    ang = math.atan2(p_end[1] - p_start[1], p_end[0] - p_start[0])
    head_len = 22
    a1 = (p_end[0] - head_len * math.cos(ang - 0.48), p_end[1] - head_len * math.sin(ang - 0.48))
    a2 = (p_end[0] - head_len * math.cos(ang + 0.48), p_end[1] - head_len * math.sin(ang + 0.48))
    od.polygon([p_end, a1, a2], fill=(255, 255, 255, 245), outline=STROKE + (220,))

    bg = Image.alpha_composite(bg, overlay)
    bg.alpha_composite(earth, (e_cx - earth.width // 2, e_cy - earth.height // 2))

    out = bg.convert("RGB")
    out = draw_top_band_text(
        out,
        [("REAL", YELLOW), ("NASA PHOTOS", WHITE)],
        font_size=166,
        y_center=113,
        gap=28,
        stroke_w=10,
    )
    return out


def main() -> int:
    NAS_OUT.mkdir(parents=True, exist_ok=True)
    REPO_OUT.mkdir(parents=True, exist_ok=True)

    builders = [
        ("A", "064_thumb_A_extreme_worlds_v02.jpg", "8 EXTREME WORLDS", build_thumb_A),
        ("B", "064_thumb_B_venus_uranus_v02.jpg", "464°C / -224°C", build_thumb_B),
        ("C", "064_thumb_C_real_nasa_saturn_v02.jpg", "REAL NASA PHOTOS", build_thumb_C),
    ]

    scores = []
    nas_paths = []
    for label, fname, hook_text, fn in builders:
        im = fn()
        p_nas = NAS_OUT / fname
        im.save(p_nas, quality=93, optimize=True)
        nas_paths.append(p_nas)

        res = thumb_preview.score(p_nas, "long", "owb", False)
        res["variant"] = label
        res["hook_text"] = hook_text
        res["size"] = f"{im.width}x{im.height}"
        res["bytes"] = p_nas.stat().st_size
        res["sha256"] = hashlib.sha256(p_nas.read_bytes()).hexdigest()
        res["nas_path"] = str(p_nas)
        scores.append(res)

        sheet_nas = NAS_OUT / fname.replace(".jpg", "_sheet.jpg")
        sp.run(
            [
                sys.executable,
                str(ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                "long",
                str(p_nas),
                "--out",
                str(sheet_nas),
                "--score",
            ],
            check=True,
        )

    comb_nas = NAS_OUT / "064_thumbs_ABC_v02_preview_sheet.jpg"
    sp.run(
        [
            sys.executable,
            str(ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "long",
            *[str(p) for p in nas_paths],
            "--out",
            str(comb_nas),
            "--score",
        ],
        check=True,
    )

    payload = {
        "job": "J3817",
        "panel_decision": "J3719",
        "film": "OWB:064",
        "preview_sheet": {
            "nas_path": str(comb_nas),
            "bytes": comb_nas.stat().st_size,
            "sha256": hashlib.sha256(comb_nas.read_bytes()).hexdigest(),
        },
        "variants": scores,
    }
    txt = json.dumps(payload, indent=2) + "\n"
    (REPO_OUT / "THUMB_SCORES_v02.json").write_text(txt, encoding="utf-8")
    (NAS_OUT / "THUMB_SCORES_v02.json").write_text(txt, encoding="utf-8")

    # Enforce J3817 stricter score bars (sat >= 120, B <= 175, near_black <= 28%)
    errs = []
    for s in scores:
        if s["fails"]:
            errs.append(f"{s['variant']}: {s['fails']}")
        if s["saturation"] < 120.0:
            errs.append(f"{s['variant']}: sat {s['saturation']} < 120")
        if s["variant"] == "B" and s["saturation"] > 175.0:
            errs.append(f"B: sat {s['saturation']} > 175")
        if s["near_black"] > 0.28:
            errs.append(f"{s['variant']}: near_black {s['near_black']:.1%} > 28%")
    print(json.dumps(payload, indent=2))
    if errs:
        print("SCORE GATE ERRORS:", errs, file=sys.stderr)
        return 1
    print("ALL 3 v02 THUMBNAILS PASSED ALL J3817 SCORE GATES!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
