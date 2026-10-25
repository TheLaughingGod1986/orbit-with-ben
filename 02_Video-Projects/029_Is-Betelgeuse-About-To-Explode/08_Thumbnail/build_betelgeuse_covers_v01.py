#!/usr/bin/env python3
"""029 Betelgeuse long thumbnails A/B/C v01 (J0921; 0 credits, real harvest plates only).

Title under test: "Is Betelgeuse About to Explode?"
Variants:
  A: BRIGHT AS MOON   (yellow: MOON)     - Top band; ESO VLT/SPHERE Betelgeuse (sphere_jan.jpg) left + NASA First Quarter Moon (half_moon.jpg) right
  B: PAST MARS        (yellow: MARS)     - Left edge band; ESO VLT/SPHERE Betelgeuse (sphere_jan.jpg) large right + NASA SDO Sun dot + NASA EPIC Earth scale ref
  C: IT WAS DUST      (yellow: DUST)     - Top band; ESO/ESA/Hubble Betelgeuse dust cloud (dust_impression.jpg) right + NASA Blue Marble Earth left

Rules: THUMBNAIL_AND_TITLE_RULES.md §2, §2.A, §2.B:
  - 0 credits (harvest plates + Pillow/NumPy compositing only)
  - No Orbit
  - HOOK: names the subject or consequence/dare; no vague question
  - BAND: 2-3 words in a top band or clear left edge; no letter over the subject; one yellow hook word; clear of bottom-right duration badge
  - GRADE: saturation >= 120 (floor 100), near-black <= 30%
  - PHONE: every word readable at 168x94
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPO = PROJECT.parents[1]
HARVEST = PROJECT / "07_Edit-Project" / "harvest_v01"
OUT = HERE / "abc_v01"
REVIEW = PROJECT / "11_Upload-Package" / "Review"

sys.path.insert(0, str(REPO / "00_Brand" / "Channel-Setup" / "tools"))
from thumb_preview import score as preview_score  # noqa: E402

W, H = 1280, 720
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (3, 7, 16)
STROKE = 6


def make_starfield_bg(
    base_rgb: tuple[int, int, int],
    glows: list[tuple[float, float, float, tuple[int, int, int], float]],
    seed: int,
    n_stars: int = 280,
) -> Image.Image:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    canvas = np.zeros((H, W, 3), dtype=np.float32)
    canvas[:, :] = np.array(base_rgb, dtype=np.float32)
    # Subtle vertical gradient so top band is clean and rich
    v_grad = np.clip(yy / H, 0, 1)[..., None]
    canvas = canvas * (0.88 + 0.22 * v_grad)

    for cx, cy, radius, col, power in glows:
        dist = np.hypot(xx - cx, yy - cy) / radius
        g = np.clip(1.0 - dist, 0.0, 1.0) ** power
        c = np.array(col, dtype=np.float32)
        # Screen-like additive blend that preserves saturation
        canvas = 255.0 - (255.0 - canvas) * (1.0 - (c / 255.0) * g[..., None])

    rng = random.Random(seed)
    stars = Image.new("RGB", (W, H), (0, 0, 0))
    sd = ImageDraw.Draw(stars)
    star_tints = [(255, 245, 230), (210, 230, 255), (255, 220, 185)]
    for _ in range(n_stars):
        x, y = rng.randrange(W), rng.randrange(H)
        # Keep top text band sparser
        if y < 150 and rng.random() < 0.65:
            continue
        r = 1 if rng.random() < 0.86 else 2
        b = rng.uniform(0.35, 0.90)
        tint = rng.choice(star_tints)
        col = tuple(int(c * b) for c in tint)
        sd.ellipse((x - r, y - r, x + r, y + r), fill=col)
    stars_arr = np.asarray(stars.filter(ImageFilter.GaussianBlur(0.55)), dtype=np.float32)
    canvas = 255.0 - (255.0 - np.clip(canvas, 0, 255)) * (255.0 - stars_arr) / 255.0
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))


def load_sphere_star(src_name: str, out_size: int, boost_sat: float = 1.65) -> tuple[Image.Image, Image.Image]:
    """Load ESO VLT/SPHERE Betelgeuse image and extract a soft alpha mask from its natural glow."""
    raw = Image.open(HARVEST / src_name).convert("RGB")
    # Crop centered on the bright photosphere + halo (raw is 816x816)
    lum = np.asarray(raw.convert("L"), dtype=np.float32)
    ys, xs = np.where(lum > 18)
    cx = int(xs.mean()) if len(xs) else raw.width // 2
    cy = int(ys.mean()) if len(ys) else raw.height // 2
    half = 270
    crop = raw.crop((cx - half, cy - half, cx + half, cy + half)).resize((out_size, out_size), Image.Resampling.LANCZOS)

    arr = np.asarray(crop, dtype=np.float32) / 255.0
    # Boost warm orange-red chromaticity while keeping core golden-white
    r = np.clip(arr[:, :, 0] ** 0.78 * 1.18, 0, 1)
    g = np.clip(arr[:, :, 1] ** 0.92 * 0.96, 0, 1)
    b = np.clip(arr[:, :, 2] ** 1.15 * 0.65, 0, 1)
    graded = Image.fromarray((np.stack([r, g, b], axis=-1) * 255.0).astype(np.uint8))
    graded = ImageEnhance.Color(graded).enhance(boost_sat)
    graded = ImageEnhance.Contrast(graded).enhance(1.12)

    # Smooth radial alpha so the black square background disappears cleanly into the graded sky
    yy, xx = np.mgrid[0:out_size, 0:out_size].astype(np.float32)
    rc = out_size / 2.0
    rad = np.hypot(xx - rc, yy - rc) / (rc * 0.94)
    radial_falloff = np.clip(1.0 - rad ** 2.4, 0.0, 1.0)
    intensity = np.max(np.stack([r, g, b], axis=-1), axis=-1)
    alpha = np.clip((intensity - 0.03) / 0.72, 0.0, 1.0) ** 0.72 * radial_falloff
    mask = Image.fromarray((alpha * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.0))
    return graded, mask


def load_dust_star(out_size: int) -> tuple[Image.Image, Image.Image]:
    """Load ESO/ESA/Hubble Betelgeuse dust impression (1632x1630) with its dramatic dark dust plume."""
    raw = Image.open(HARVEST / "dust_impression.jpg").convert("RGB")
    lum = np.asarray(raw.convert("L"), dtype=np.float32)
    ys, xs = np.where(lum > 14)
    cx = int(xs.mean()) if len(xs) else raw.width // 2
    cy = int(ys.mean()) if len(ys) else raw.height // 2
    half = 490
    crop = raw.crop((cx - half, cy - half, cx + half, cy + half)).resize((out_size, out_size), Image.Resampling.LANCZOS)

    arr = np.asarray(crop, dtype=np.float32) / 255.0
    # Lift midtones so the dusty cloud silhouette reads sharply at 168x94 without crushing to near-black
    r = np.clip(arr[:, :, 0] ** 0.72 * 1.25, 0, 1)
    g = np.clip(arr[:, :, 1] ** 0.86 * 1.02, 0, 1)
    b = np.clip(arr[:, :, 2] ** 1.05 * 0.75, 0, 1)
    graded = Image.fromarray((np.stack([r, g, b], axis=-1) * 255.0).astype(np.uint8))
    graded = ImageEnhance.Color(graded).enhance(1.55)
    graded = ImageEnhance.Contrast(graded).enhance(1.18)
    graded = graded.filter(ImageFilter.UnsharpMask(radius=2.0, percent=65, threshold=2))

    yy, xx = np.mgrid[0:out_size, 0:out_size].astype(np.float32)
    rc = out_size / 2.0
    rad = np.hypot(xx - rc, yy - rc) / (rc * 0.95)
    radial_falloff = np.clip(1.0 - rad ** 2.2, 0.0, 1.0)
    intensity = np.max(np.stack([r, g, b], axis=-1), axis=-1)
    # Keep dust cloud interior opaque while feathering outer black corners
    core_circle = np.clip(1.0 - (np.hypot(xx - rc, yy - rc * 1.04) / (rc * 0.62)) ** 3.2, 0.0, 1.0)
    alpha = np.maximum(np.clip((intensity - 0.025) / 0.55, 0.0, 1.0) ** 0.75, core_circle * 0.92) * radial_falloff
    mask = Image.fromarray((alpha * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.5))
    return graded, mask


def load_half_moon(diameter: int) -> tuple[Image.Image, Image.Image]:
    """Load NASA GSFC First Quarter Moon (half_moon.jpg), grade warm-silver with sunlit blue/gold rim."""
    raw = Image.open(HARVEST / "half_moon.jpg").convert("RGB")
    lum = np.asarray(raw.convert("L"), dtype=np.float32)
    ys, xs = np.where(lum > 12)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = max(x1 - x0, y1 - y0) // 2 + 8
    crop = raw.crop((cx - r, cy - r, cx + r, cy + r)).resize((diameter, diameter), Image.Resampling.LANCZOS)

    arr = np.asarray(crop, dtype=np.float32) / 255.0
    # Lift the dark lunar night side into a rich earthshine sapphire-blue so it has zero near-black crush
    # and give the sunlit half a warm golden-ivory luster
    lum_n = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2])[..., None]
    lit = np.clip(lum_n ** 0.72, 0.0, 1.0)
    earthshine = np.array([0.16, 0.28, 0.54], dtype=np.float32)
    sunlit = np.array([1.00, 0.93, 0.74], dtype=np.float32)
    col = earthshine * (1.0 - lit * 0.75) + sunlit * (lit * 1.08)
    graded = Image.fromarray((np.clip(col, 0.0, 1.0) * 255.0).astype(np.uint8))
    graded = ImageEnhance.Contrast(graded).enhance(1.16)
    graded = ImageEnhance.Color(graded).enhance(1.30)
    graded = graded.filter(ImageFilter.UnsharpMask(radius=1.8, percent=70, threshold=2))

    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.5))
    return graded, mask


def load_earth_disc(src_name: str, diameter: int) -> tuple[Image.Image, Image.Image]:
    """Load NASA Blue Marble or DSCOVR EPIC Earth disc, graded vibrantly with zero dark rim."""
    raw = Image.open(HARVEST / src_name).convert("RGB")
    lum = np.asarray(raw.convert("L"), dtype=np.float32)
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    # Ignore any corner labels/borders outside central 92% radius
    central = np.hypot(xx - w / 2.0, yy - h / 2.0) < (min(w, h) * 0.46)
    ys, xs = np.where((lum > 28) & central)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = int(min(x1 - x0, y1 - y0) * 0.492)
    crop = raw.crop((cx - r, cy - r, cx + r, cy + r)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    crop_lum = np.asarray(crop.convert("L"), dtype=np.float32)
    crop = ImageEnhance.Brightness(crop).enhance(1.18)
    crop = ImageEnhance.Color(crop).enhance(1.75)
    crop = ImageEnhance.Contrast(crop).enhance(1.12)
    crop = crop.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))

    cy_m, cx_m = np.mgrid[0:diameter, 0:diameter].astype(np.float32)
    rad = np.hypot(cx_m - diameter / 2.0, cy_m - diameter / 2.0) / (diameter * 0.485)
    circle_alpha = np.clip((1.0 - rad) * 18.0, 0.0, 1.0)
    lum_alpha = np.clip((crop_lum - 18.0) / 22.0, 0.0, 1.0)
    alpha = np.minimum(circle_alpha, np.maximum(lum_alpha, (rad < 0.92).astype(np.float32)))
    mask = Image.fromarray((alpha * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    return crop, mask


def load_sdo_sun(diameter: int) -> tuple[Image.Image, Image.Image]:
    """Load NASA SDO continuum Sun disc for scale comparison with zero dark rim."""
    raw = Image.open(HARVEST / "sdo_hmi_continuum.jpg").convert("RGB")
    lum = np.asarray(raw.convert("L"), dtype=np.float32)
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    central = np.hypot(xx - w / 2.0, yy - h / 2.0) < (min(w, h) * 0.47)
    ys, xs = np.where((lum > 40) & central)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = int(min(x1 - x0, y1 - y0) * 0.490)
    crop = raw.crop((cx - r, cy - r, cx + r, cy + r)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    crop_lum = np.asarray(crop.convert("L"), dtype=np.float32)
    crop = ImageEnhance.Brightness(crop).enhance(1.18)
    crop = ImageEnhance.Color(crop).enhance(1.45)

    cy_m, cx_m = np.mgrid[0:diameter, 0:diameter].astype(np.float32)
    rad = np.hypot(cx_m - diameter / 2.0, cy_m - diameter / 2.0) / (diameter * 0.482)
    circle_alpha = np.clip((1.0 - rad) * 14.0, 0.0, 1.0)
    lum_alpha = np.clip((crop_lum - 30.0) / 35.0, 0.0, 1.0)
    alpha = np.minimum(circle_alpha, lum_alpha)
    mask = Image.fromarray((alpha * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    return crop, mask


def draw_top_band_text(im: Image.Image, words: list[str], hook: str, top_y: int = 34) -> dict:
    """Draw 2-3 words in a single horizontal band across the top (THUMBNAIL_AND_TITLE_RULES.md §2.B.2)."""
    d = ImageDraw.Draw(im)
    size = 114
    while size > 50:
        f = ImageFont.truetype(FONT_PATH, size)
        cap = f.getbbox("H")
        cap_h = cap[3] - cap[1]
        space = 26
        widths = [d.textlength(w, font=f) for w in words]
        total = sum(widths) + space * (len(words) - 1)
        if cap_h <= 84 and total <= 1180:
            break
        size -= 1

    x = (W - total) / 2.0
    y = top_y - cap[1]
    boxes = []
    for w, width in zip(words, widths):
        color = YELLOW if w == hook else WHITE
        d.text((x + 3, y + 4), w, font=f, fill=BLACK, stroke_width=STROKE + 1, stroke_fill=BLACK)
        d.text((x, y), w, font=f, fill=color, stroke_width=STROKE, stroke_fill=BLACK)
        boxes.append([round(v, 1) for v in d.textbbox((x, y), w, font=f, stroke_width=STROKE)])
        x += width + space

    return {
        "band": "top",
        "font": "Arial Black",
        "font_size": size,
        "cap_height": cap_h,
        "cap_share": round(cap_h / H, 3),
        "text_boxes": boxes,
    }


def draw_left_band_text(im: Image.Image, lines: list[str], hook: str, x_left: int = 44, y_top: int = 210, max_w: int = 520) -> dict:
    """Draw 2 words stacked on the clear left edge, away from the right-hand hero."""
    d = ImageDraw.Draw(im)
    size = 118
    while size > 50:
        f = ImageFont.truetype(FONT_PATH, size)
        cap = f.getbbox("H")
        cap_h = cap[3] - cap[1]
        widths = [d.textlength(ln, font=f) for ln in lines]
        if cap_h <= 86 and max(widths) <= max_w:
            break
        size -= 1

    gap = int(cap_h * 0.34)
    y = y_top - cap[1]
    boxes = []
    for ln in lines:
        color = YELLOW if ln == hook else WHITE
        d.text((x_left + 3, y + 4), ln, font=f, fill=BLACK, stroke_width=STROKE + 1, stroke_fill=BLACK)
        d.text((x_left, y), ln, font=f, fill=color, stroke_width=STROKE, stroke_fill=BLACK)
        boxes.append([round(v, 1) for v in d.textbbox((x_left, y), ln, font=f, stroke_width=STROKE)])
        y += cap_h + gap

    return {
        "band": "left",
        "font": "Arial Black",
        "font_size": size,
        "cap_height": cap_h,
        "cap_share": round(cap_h / H, 3),
        "text_boxes": boxes,
    }


def build_variant_a() -> tuple[Image.Image, dict]:
    """Variant A: BRIGHT AS MOON.
    Hero: ESO VLT/SPHERE Betelgeuse (left, glowing red-orange supergiant) + NASA First Quarter Moon (right, scale/brightness reference).
    Top band: BRIGHT AS MOON (MOON in yellow).
    """
    bg = make_starfield_bg(
        base_rgb=(16, 26, 58),
        glows=[
            (370, 445, 520, (255, 92, 22), 1.45),
            (370, 445, 290, (255, 190, 70), 1.8),
            (930, 435, 480, (55, 125, 235), 1.55),
            (640, 120, 620, (35, 65, 145), 1.7),
        ],
        seed=2901,
    )

    star_d = 560
    star, star_mask = load_sphere_star("sphere_jan.jpg", star_d, boost_sat=1.75)
    bg.paste(star, (370 - star_d // 2, 445 - star_d // 2), star_mask)

    moon_d = 430
    moon, moon_mask = load_half_moon(moon_d)
    # Soft blue-gold halo behind the Moon
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse((930 - 235, 435 - 235, 930 + 235, 435 + 235), fill=(90, 165, 255, 95))
    halo = halo.filter(ImageFilter.GaussianBlur(22))
    bg = Image.alpha_composite(bg.convert("RGBA"), halo).convert("RGB")
    bg.paste(moon, (930 - moon_d // 2, 435 - moon_d // 2), moon_mask)

    info = draw_top_band_text(bg, ["BRIGHT", "AS", "MOON"], "MOON", top_y=36)
    return bg, {
        "variant": "A",
        "text": "BRIGHT AS MOON",
        "yellow": "MOON",
        "sources": [
            "ESO/M. Montargès et al., VLT/SPHERE January 2019 view of Betelgeuse (eso2003b, CC BY 4.0)",
            "NASA/GSFC Scientific Visualization Studio, First Quarter Moon (half_moon.jpg, public domain)",
        ],
        "hero_boxes": {
            "betelgeuse": [370 - 230, 445 - 230, 370 + 230, 445 + 230],
            "half_moon": [930 - 215, 435 - 215, 930 + 215, 435 + 215],
        },
        **info,
    }


def build_variant_b() -> tuple[Image.Image, dict]:
    """Variant B: PAST MARS.
    Hero: ESO VLT/SPHERE Betelgeuse enormous on the right (d=620), with a crisp golden Mars-orbit ring inside its reach,
    NASA SDO Sun dot + NASA EPIC Earth on the lower-left as the scale reference.
    Left edge band: PAST / MARS (MARS in yellow).
    """
    bg = make_starfield_bg(
        base_rgb=(14, 24, 54),
        glows=[
            (890, 380, 590, (255, 84, 18), 1.35),
            (890, 380, 340, (255, 185, 60), 1.75),
            (280, 560, 440, (42, 118, 225), 1.55),
        ],
        seed=2902,
    )

    star_d = 640
    star, star_mask = load_sphere_star("sphere_jan.jpg", star_d, boost_sat=1.80)
    bg.paste(star, (895 - star_d // 2, 380 - star_d // 2), star_mask)

    # Scale reference in lower-left (clear of the PAST / MARS text at y=150..360):
    # Earth (NASA EPIC, d=164) + glowing golden Sun (NASA SDO, d=84) beside the giant red supergiant
    earth_d = 164
    earth, earth_mask = load_earth_disc("dscovr_epic.jpg", earth_d)
    ehalo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ehalo).ellipse((195 - 98, 555 - 98, 195 + 98, 555 + 98), fill=(70, 165, 255, 115))
    ehalo = ehalo.filter(ImageFilter.GaussianBlur(15))
    bg = Image.alpha_composite(bg.convert("RGBA"), ehalo).convert("RGB")
    bg.paste(earth, (195 - earth_d // 2, 555 - earth_d // 2), earth_mask)

    sun_d = 84
    sun, sun_mask = load_sdo_sun(sun_d)
    shalo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shalo).ellipse((425 - 60, 555 - 60, 425 + 60, 555 + 60), fill=(255, 205, 65, 155))
    shalo = shalo.filter(ImageFilter.GaussianBlur(12))
    bg = Image.alpha_composite(bg.convert("RGBA"), shalo).convert("RGB")
    bg.paste(sun, (425 - sun_d // 2, 555 - sun_d // 2), sun_mask)

    info = draw_left_band_text(bg, ["PAST", "MARS"], "MARS", x_left=48, y_top=140, max_w=500)
    return bg, {
        "variant": "B",
        "text": "PAST MARS",
        "yellow": "MARS",
        "sources": [
            "ESO/M. Montargès et al., VLT/SPHERE January 2019 view of Betelgeuse (eso2003b, CC BY 4.0)",
            "NASA/DSCOVR EPIC Earth (dscovr_epic.jpg, public domain)",
            "NASA/SDO HMI Continuum Sun (sdo_hmi_continuum.jpg, public domain)",
        ],
        "hero_boxes": {
            "betelgeuse": [895 - 260, 380 - 260, 895 + 260, 380 + 260],
            "earth_scale_ref": [195 - 82, 555 - 82, 195 + 82, 555 + 82],
            "sun_scale_ref": [425 - 42, 555 - 42, 425 + 42, 555 + 42],
        },
        **info,
    }


def build_variant_c() -> tuple[Image.Image, dict]:
    """Variant C: IT WAS DUST.
    Hero: ESO/ESA/Hubble Betelgeuse Great Dimming dust cloud impression (dust_impression.jpg) large center-right (d=570),
    with NASA Apollo 17 Blue Marble Earth (d=190) at lower-left as the observer vantage reference.
    Top band: IT WAS DUST (DUST in yellow).
    """
    bg = make_starfield_bg(
        base_rgb=(22, 18, 52),
        glows=[
            (790, 435, 560, (245, 95, 28), 1.4),
            (790, 435, 310, (255, 175, 65), 1.8),
            (250, 495, 450, (52, 115, 235), 1.5),
            (520, 140, 580, (75, 45, 145), 1.6),
        ],
        seed=2903,
    )

    dust_d = 560
    dust, dust_mask = load_dust_star(dust_d)
    bg.paste(dust, (790 - dust_d // 2, 435 - dust_d // 2), dust_mask)

    earth_d = 210
    earth, earth_mask = load_earth_disc("blue_marble.jpg", earth_d)
    ehalo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ehalo).ellipse((235 - 120, 495 - 120, 235 + 120, 495 + 120), fill=(75, 160, 255, 110))
    ehalo = ehalo.filter(ImageFilter.GaussianBlur(16))
    bg = Image.alpha_composite(bg.convert("RGBA"), ehalo).convert("RGB")
    bg.paste(earth, (235 - earth_d // 2, 495 - earth_d // 2), earth_mask)

    info = draw_top_band_text(bg, ["IT", "WAS", "DUST"], "DUST", top_y=36)
    return bg, {
        "variant": "C",
        "text": "IT WAS DUST",
        "yellow": "DUST",
        "sources": [
            "ESO, ESA/Hubble, M. Kornmesser, Betelgeuse's Dust Cloud Artist's Impression (heic2009a / eso2003, CC BY 4.0)",
            "NASA Apollo 17 Blue Marble Earth (AS17-148-22727, public domain)",
        ],
        "hero_boxes": {
            "betelgeuse_dust": [790 - 235, 435 - 235, 790 + 235, 435 + 235],
            "earth_vantage_ref": [235 - 105, 495 - 105, 235 + 105, 495 + 105],
        },
        **info,
    }


def build_sheets(paths: list[Path], score_lines: list[str]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    # 1. Standard thumb_preview.py sheet + score
    preview_sheet = REVIEW / "thumb_preview_v01.jpg"
    res = subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand" / "Channel-Setup" / "tools" / "thumb_preview.py"),
            "long",
            *map(str, paths),
            "--out",
            str(preview_sheet),
            "--score",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    (REVIEW / "THUMB_SCORE.txt").write_text(res.stdout)

    # 2. Full-size vertical stack (THUMBNAILS_FULL_SIZE.jpg)
    full_stack = Image.new("RGB", (W, H * 3), (0, 0, 0))
    for idx, p in enumerate(paths):
        full_stack.paste(Image.open(p).convert("RGB"), (0, idx * H))
    full_stack.save(REVIEW / "THUMBNAILS_FULL_SIZE.jpg", quality=92)

    # 3. OWB family sheet (preceding 028 primary + 029 A/B/C)
    prev_028 = REPO / "02_Video-Projects" / "028_A-Star-Is-Coming-Toward-Us" / "08_Thumbnail" / "abc_v01" / "gliese_thumb_A.jpg"
    fam_inputs = ([prev_028] if prev_028.exists() else []) + paths
    subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand" / "Channel-Setup" / "tools" / "thumb_preview.py"),
            "long",
            *map(str, fam_inputs),
            "--out",
            str(REVIEW / "owb_family_sheet_v01.jpg"),
        ],
        check=True,
    )

    # 4. 360x202 style sheet against live/scheduled OWB long primaries (021-028)
    live_primaries = [
        REPO / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/08_Thumbnail/abc_v02_no_orbit/saturn_thumb_A_already-falling.jpg",
        REPO / "02_Video-Projects/022_Is-the-Sun-Getting-Brighter/08_Thumbnail/abc_v01/sun_thumb_A_burning-harder.png",
        REPO / "02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/abc_v02/venus_thumb_A_melts-lead.png",
        REPO / "02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnail/abc_v01/light_speed_thumb_A_7-years-gone.jpg",
        REPO / "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/08_Thumbnail/abc_v03/mars_robot_thumb_A_built-for-90-days.jpg",
        REPO / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/abc_v01/nearest_star_thumb_A_you-cant-see-it.jpg",
        REPO / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/abc_v01/earth_spin_thumb_A.jpg",
        REPO / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/08_Thumbnail/abc_v01/gliese_thumb_A.jpg",
    ]
    tiles: list[tuple[Image.Image, bool]] = [(Image.open(p).convert("RGB"), True) for p in paths]
    for lp in live_primaries:
        if lp.exists():
            tiles.append((Image.open(lp).convert("RGB"), False))

    tw, th, gap = 360, 202, 10
    cols = 4
    rows_n = (len(tiles) + cols - 1) // cols
    grid = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows_n * th + (rows_n + 1) * gap), "white")
    gd = ImageDraw.Draw(grid)
    for i, (im_tile, is_new) in enumerate(tiles):
        r, c = divmod(i, cols)
        x = gap + c * (tw + gap)
        y = gap + r * (th + gap)
        resized = im_tile.resize((tw, th), Image.Resampling.LANCZOS)
        grid.paste(resized, (x, y))
        if is_new:
            gd.rectangle((x - 2, y - 2, x + tw + 1, y + th + 1), outline=(220, 30, 30), width=3)
    grid.save(REVIEW / "style_sheet_v01.jpg", quality=92)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)

    builders = [
        ("A", build_variant_a),
        ("B", build_variant_b),
        ("C", build_variant_c),
    ]
    meta = []
    paths = []
    score_lines = []
    for key, fn in builders:
        im, info = fn()
        dst = OUT / f"betelgeuse_thumb_{key}.jpg"
        im.save(dst, quality=94, subsampling=0)
        paths.append(dst)
        sc = preview_score(dst, "long", "owb", False)
        info["file"] = dst.name
        info["bytes"] = dst.stat().st_size
        info["sha256"] = hashlib.sha256(dst.read_bytes()).hexdigest()
        info["score"] = sc
        meta.append(info)
        if sc["fails"]:
            print(f"FAIL on {dst.name}: {sc['fails']}", file=sys.stderr)
            return 1

    (OUT / "COVER_LAYOUT.json").write_text(json.dumps(meta, indent=2) + "\n")
    (REVIEW / "COVER_LAYOUT.json").write_text(json.dumps(meta, indent=2) + "\n")
    build_sheets(paths, score_lines)
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
