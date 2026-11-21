#!/usr/bin/env python3
"""J3302: reproducible weekly thumbnail builder for Orbit With Ben (2026-11-21).

Builds the 3 Test & Compare Challenger B thumbnails for the 3 weakest untested
public longs (no running Studio test and no pending Chief-approved proposal):
  1. NbW5G1BpPY0 (006 Europa: Could Life Exist Under The Ice Of Europa?)
     -> NbW5G1BpPY0_B_v01.jpg  |  2× EARTH'S WATER  (yellow: 2×)
     Real NASA/JPL-Caltech/SETI Galileo enhanced-color Europa mosaic (PIA19048)
     + Apollo 17 Blue Marble Earth scale/ocean reference (as17-148-22727)
     + crisp white discovery arrow to Europa's fractured red-brown ice lineae.
  2. rVqgtkBV3jc (024 Light Speed: What Happens If You Travel Near Light Speed?)
     -> rVqgtkBV3jc_B_v01.jpg  |  YOU AGE SLOWER  (yellow: SLOWER)
     Real NASA STS-41B photograph of Bruce McCandless II floating untethered
     above Earth's curved blue limb (S84-27018), composited against a
     relativistic blue-shifted forward / red-shifted aft starlight field
     (024 locked script v02 Scene 03; replaces synthetic sci-fi ship and
     fixes 6-word §2.B.2 style FAIL).
  3. REXYxuLOBoI (005 Last Star: The Last Star: What Happens When a Red Dwarf Dies?)
     -> REXYxuLOBoI_B_v01.jpg  |  OUTLIVES OUR SUN  (yellow: OUTLIVES)
     Real NASA/GSFC SDO AIA 304 Å extreme-UV full-disk solar plate with
     erupting filament (GSFC_20171208_Archive_e002069) graded as a blazing
     crimson red dwarf + Apollo 17 Blue Marble Earth story/scale inset
     (as17-148-22727; fixes missing §2.A.5 scale ref and vague LAST LIGHT hook).

£0 spend; 100% public-domain NASA plates; no YouTube Studio writes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = (
    Path(__file__).resolve().parents[3]
    if "00_Brand" in str(Path(__file__).resolve())
    else Path.cwd()
)
SYS_TOOLS = ROOT / "00_Brand/Channel-Setup/tools"
sys.path.insert(0, str(SYS_TOOLS))
from thumb_preview import score as score_thumb  # noqa: E402

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1280, 720
BAND_H = 148
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NAS_BASE = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
DEFAULT_PLATES = Path.home() / "_desk/j3302/plates"
DEFAULT_EARTH = Path.home() / "_desk/j2834/plates/as17-148-22727.jpg"
DEFAULT_LIVE = Path.home() / "_desk/j3302/live"
DEFAULT_OUT = Path.home() / "_desk/j3302/designs_v01"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def make_cosmic_bg(
    seed: int,
    base_rgb: tuple[int, int, int],
    glow_rgb: tuple[int, int, int],
    gx: float,
    gy: float,
    gr: float,
    sec_glow: tuple[tuple[int, int, int], float, float, float] | None = None,
    stars: int = 95,
) -> Image.Image:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.exp(-(((xx - gx) ** 2) / (gr ** 2) + ((yy - gy) ** 2) / ((gr * 0.72) ** 2)))
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for k in range(3):
        arr[:, :, k] = base_rgb[k] + glow_rgb[k] * g
    if sec_glow is not None:
        rgb2, x2, y2, r2 = sec_glow
        g2 = np.exp(-(((xx - x2) ** 2) / (r2 ** 2) + ((yy - y2) ** 2) / ((r2 * 0.8) ** 2)))
        for k in range(3):
            arr[:, :, k] += rgb2[k] * g2
    arr += rng.normal(0, 1.0, (H, W, 1))
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(stars):
        sx = int(rng.integers(14, W - 14))
        sy = int(rng.integers(BAND_H + 6, H - 14))
        sv = int(rng.integers(120, 235))
        r = 1 if rng.random() < 0.82 else 2
        d.ellipse((sx, sy, sx + r, sy + r), fill=(sv, sv, min(255, sv + 30)))
    return im


def apply_top_band_scrim(im: Image.Image, band_rgb: tuple[int, int, int] = (14, 24, 52), strength: float = 0.72) -> Image.Image:
    """Smooth cosine-feathered top band (y=0..186) with zero hard seam."""
    arr = np.asarray(im, dtype=np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None]
    t = np.clip((yy - 95.0) / (195.0 - 95.0), 0.0, 1.0)
    alpha = strength * 0.5 * (1.0 + np.cos(math.pi * t))
    alpha = np.where(yy < 95.0, strength, alpha)[:, :, None]
    tint = np.array(band_rgb, dtype=np.float32)[None, None, :]
    out = arr * (1.0 - alpha) + tint * alpha
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def draw_top_band_text(
    im: Image.Image,
    tokens: list[tuple[str, tuple[int, int, int]]],
    max_w: int = 1190,
    start_size: int = 104,
    y_center: int = 74,
) -> tuple[int, int]:
    """Draw bold ALL-CAPS single-line house headline in top band, yellow hook word + heavy black outline."""
    d = ImageDraw.Draw(im)
    size = start_size
    while size >= 66:
        font = ImageFont.truetype(FONT_PATH, size)
        space_w = int(d.textlength(" ", font=font))
        widths = [int(d.textlength(w, font=font)) for w, _ in tokens]
        total_w = sum(widths) + space_w * (len(tokens) - 1)
        if total_w <= max_w:
            break
        size -= 2
    font = ImageFont.truetype(FONT_PATH, size)
    space_w = int(d.textlength(" ", font=font))
    widths = [int(d.textlength(w, font=font)) for w, _ in tokens]
    total_w = sum(widths) + space_w * (len(tokens) - 1)
    bbox_sample = d.textbbox((0, 0), "EARTHS", font=font)
    th = bbox_sample[3] - bbox_sample[1]
    x = (W - total_w) // 2
    y = y_center - th // 2 - bbox_sample[1]
    stroke_w = max(7, size // 11)
    # Soft drop shadow layer
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    cx = x
    for (w, _), ww in zip(tokens, widths):
        sd.text((cx + 4, y + 6), w, font=font, fill=(0, 0, 0, 210), stroke_width=stroke_w + 3, stroke_fill=(0, 0, 0, 210))
        cx += ww + space_w
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    im_rgba = im.convert("RGBA")
    im_rgba.alpha_composite(shadow)
    im.paste(im_rgba.convert("RGB"))

    d = ImageDraw.Draw(im)
    cx = x
    for (w, col), ww in zip(tokens, widths):
        d.text((cx, y), w, font=font, fill=col, stroke_width=stroke_w, stroke_fill=BLACK)
        cx += ww + space_w
    return size, y + th + bbox_sample[1]


def draw_arrow(
    im: Image.Image,
    p0: tuple[float, float],
    p1: tuple[float, float],
    color: tuple[int, int, int] = WHITE,
    shaft_w: int = 14,
    head_len: float = 42.0,
    head_half: float = 24.0,
) -> None:
    d = ImageDraw.Draw(im)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    bx, by = p1[0] - ux * head_len, p1[1] - uy * head_len
    d.line((p0[0], p0[1], bx, by), fill=BLACK, width=shaft_w + 10)
    d.polygon(
        [
            (p1[0] + ux * 6, p1[1] + uy * 6),
            (bx - ux * 4 + px * (head_half + 6), by - uy * 4 + py * (head_half + 6)),
            (bx - ux * 4 - px * (head_half + 6), by - uy * 4 - py * (head_half + 6)),
        ],
        fill=BLACK,
    )
    d.line((p0[0], p0[1], bx, by), fill=color, width=shaft_w)
    d.polygon(
        [
            p1,
            (bx + px * head_half, by + py * head_half),
            (bx - px * head_half, by - py * head_half),
        ],
        fill=color,
    )


def extract_earth_globe(earth_path: Path, diam: int, warm_rim: bool = False) -> Image.Image:
    """Cleanly extract circular Apollo 17 Blue Marble globe with vivid ocean grade & soft atmospheric rim."""
    src = Image.open(earth_path).convert("RGB")
    arr = np.asarray(src, dtype=np.float32)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    ys, xs = np.where(lum > 24)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    r = min(x1 - x0, y1 - y0) / 2.0
    crop = src.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((diam, diam), Image.LANCZOS)
    crop = ImageEnhance.Color(crop).enhance(1.55)
    crop = ImageEnhance.Contrast(crop).enhance(1.18)
    crop = ImageEnhance.Brightness(crop).enhance(1.06)

    # Circular alpha mask with 2px feathered edge
    yy, xx = np.mgrid[0:diam, 0:diam]
    rr = np.sqrt((xx - diam / 2.0) ** 2 + (yy - diam / 2.0) ** 2)
    alpha = np.clip((diam / 2.0 - 1.5 - rr) / 2.5, 0.0, 1.0)
    rgba = np.zeros((diam, diam, 4), dtype=np.uint8)
    rgb = np.asarray(crop, dtype=np.float32)
    if warm_rim:
        # Subtle fiery starlight rim on the right limb facing the red dwarf
        rim = np.clip((rr / (diam / 2.0) - 0.65) / 0.35, 0.0, 1.0) * np.clip((xx - diam * 0.42) / (diam * 0.5), 0.0, 1.0)
        rgb[:, :, 0] = np.clip(rgb[:, :, 0] + 115 * rim, 0, 255)
        rgb[:, :, 1] = np.clip(rgb[:, :, 1] + 45 * rim, 0, 255)
    rgba[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    rgba[:, :, 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def paste_with_glow(canvas: Image.Image, fg: Image.Image, xy: tuple[int, int], glow_rgb: tuple[int, int, int], blur: int = 24, strength: float = 0.65) -> None:
    alpha = fg.getchannel("A")
    glow = Image.new("RGBA", fg.size, (*glow_rgb, 255))
    glow.putalpha(alpha.point(lambda p: int(p * strength)))
    pad = blur * 2
    gpad = Image.new("RGBA", (fg.width + pad * 2, fg.height + pad * 2), (0, 0, 0, 0))
    gpad.paste(glow, (pad, pad))
    gpad = gpad.filter(ImageFilter.GaussianBlur(blur))
    base = canvas.convert("RGBA")
    base.alpha_composite(gpad, (xy[0] - pad, xy[1] - pad))
    base.alpha_composite(fg, xy)
    canvas.paste(base.convert("RGB"))


def build_europa(plates: Path, earth_path: Path, out_path: Path) -> dict:
    """1. NbW5G1BpPY0 (006 Europa) -> 2× EARTH'S WATER (yellow 2×)."""
    bg = make_cosmic_bg(
        seed=601,
        base_rgb=(8, 18, 50),
        glow_rgb=(16, 78, 178),
        gx=790, gy=540, gr=620,
        sec_glow=((22, 102, 205), 215, 515, 310),
        stars=110,
    )
    eu = Image.open(plates / "PIA19048_europa_hi.jpg").convert("RGB")
    # PIA19048 is 1280x946: Europa's sunlit circular limb arch is centered near (cx=636, cy=696), radius ~598px!
    # Fit a clean geometric circle mask to the sunlit outer limb and anchor Europa's dark terminator cleanly at y=720
    # so there is ZERO jagged luminance-cutout edge!
    arr = np.asarray(eu, dtype=np.float32)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    ys, xs = np.where(lum > 18)
    x0, x1 = int(xs.min()), int(xs.max())
    y0 = int(ys.min())
    # Top of arch is y0, width spans x0..x1 -> radius r = (x1 - x0)/2, center = ((x0+x1)/2, y0 + r)
    eu_r = (x1 - x0) / 2.0
    eu_cx = (x0 + x1) / 2.0
    eu_cy = y0 + eu_r
    # Crop from top of limb down to slightly past the equator/terminator (y0..y0+int(eu_r*1.04))
    crop_box = (max(0, int(eu_cx - eu_r - 4)), max(0, y0 - 4), min(eu.width, int(eu_cx + eu_r + 4)), min(eu.height, int(y0 + eu_r * 1.03)))
    eu_crop = eu.crop(crop_box)
    target_w = 880
    scale = target_w / eu_crop.width
    target_h = int(eu_crop.height * scale)
    eu_scaled = eu_crop.resize((target_w, target_h), Image.LANCZOS)
    eu_scaled = ImageEnhance.Contrast(eu_scaled).enhance(1.26)
    eu_scaled = ImageEnhance.Color(eu_scaled).enhance(1.52)
    eu_scaled = ImageEnhance.Sharpness(eu_scaled).enhance(1.30)

    earr = np.asarray(eu_scaled, dtype=np.float32)
    yy_e, xx_e = np.mgrid[0:target_h, 0:target_w]
    scx = (eu_cx - crop_box[0]) * scale
    scy = (eu_cy - crop_box[1]) * scale
    sr = eu_r * scale - 2.0
    rr = np.sqrt((xx_e - scx) ** 2 + (yy_e - scy) ** 2)
    # Crisp geometric circular outer limb mask (zero speckle)
    alpha = np.clip((sr - rr) / 3.0, 0.0, 1.0)
    # Gently lift Europa's shadowed lower terminator with deep ocean-blue bounce light (no near-black band)
    elum = 0.299 * earr[:, :, 0] + 0.587 * earr[:, :, 1] + 0.114 * earr[:, :, 2]
    lift = np.clip((48.0 - elum) / 48.0, 0.0, 1.0) * alpha
    earr[:, :, 0] = np.clip(earr[:, :, 0] + 10.0 * lift, 0, 255)
    earr[:, :, 1] = np.clip(earr[:, :, 1] + 32.0 * lift, 0, 255)
    earr[:, :, 2] = np.clip(earr[:, :, 2] + 68.0 * lift, 0, 255)

    eu_rgba = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    eu_rgba[:, :, :3] = np.clip(earr, 0, 255).astype(np.uint8)
    eu_rgba[:, :, 3] = (alpha * 255).astype(np.uint8)
    eu_fg = Image.fromarray(eu_rgba, "RGBA")

    # Anchor Europa cleanly against the bottom edge (y=720 - target_h + 18) -> giant horizon globe, zero floating edge!
    ex = 375
    ey = H - target_h + 22
    paste_with_glow(bg, eu_fg, (ex, ey), glow_rgb=(45, 165, 255), blur=26, strength=0.58)

    # Scale/story reference: Apollo 17 Blue Marble Earth on lower-left
    earth = extract_earth_globe(earth_path, diam=232)
    paste_with_glow(bg, earth, (82, 416), glow_rgb=(40, 155, 255), blur=22, strength=0.68)

    # Crisp white discovery pointer arrow onto Europa's fractured red-brown icy crust
    draw_arrow(bg, (336, 316), (576, 368), color=WHITE, shaft_w=13, head_len=38, head_half=21)

    bg = apply_top_band_scrim(bg, band_rgb=(8, 16, 46), strength=0.72)
    font_sz, text_bot = draw_top_band_text(
        bg,
        [("2×", YELLOW), ("EARTH'S", WHITE), ("WATER", WHITE)],
        max_w=1180,
        start_size=102,
        y_center=76,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=93, optimize=True)
    sc = score_thumb(out_path, "long")
    return {
        "video": "NbW5G1BpPY0",
        "film": "006",
        "hook": "2× EARTH'S WATER",
        "yellow_word": "2×",
        "font_size": font_sz,
        "text_bottom_y": text_bot,
        "file": str(out_path),
        "bytes": out_path.stat().st_size,
        "sha256": sha256(out_path),
        "score": sc,
        "sources": [
            {"nasa_id": "PIA19048", "desc": "NASA/JPL-Caltech/SETI Institute Galileo enhanced-color Europa mosaic"},
            {"nasa_id": "as17-148-22727", "desc": "NASA Apollo 17 Blue Marble Earth (scale & ocean-volume reference)"},
        ],
    }


def _exterior_bg_mask(lum: np.ndarray, thresh: float = 28.0) -> np.ndarray:
    """Flood-fill exterior black space from image borders so interior dark regions (e.g., helmet visor) stay 100% opaque."""
    h, w = lum.shape
    bg = np.zeros((h, w), dtype=bool)
    dark = lum < thresh
    stack = []
    for x in range(w):
        if dark[0, x]:
            bg[0, x] = True; stack.append((0, x))
        if dark[h - 1, x]:
            bg[h - 1, x] = True; stack.append((h - 1, x))
    for y in range(h):
        if dark[y, 0] and not bg[y, 0]:
            bg[y, 0] = True; stack.append((y, 0))
        if dark[y, w - 1] and not bg[y, w - 1]:
            bg[y, w - 1] = True; stack.append((y, w - 1))
    while stack:
        cy, cx = stack.pop()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not bg[ny, nx] and dark[ny, nx]:
                bg[ny, nx] = True
                stack.append((ny, nx))
    return ~bg  # True = foreground (including solid dark visor!)


def build_light_speed(plates: Path, out_path: Path) -> dict:
    """2. rVqgtkBV3jc (024 Light Speed) -> YOU AGE SLOWER (yellow SLOWER)."""
    src = Image.open(plates / "nasa_astronaut_eva.jpg").convert("RGB")
    w0, h0 = src.size  # 1920x1920
    # Earth limb slice: y=1225..1900 -> resize to 1280x360 across lower frame
    earth_strip = src.crop((0, 1225, w0, 1900)).resize((W, 360), Image.LANCZOS)
    earth_strip = ImageEnhance.Color(earth_strip).enhance(1.90)
    earth_strip = ImageEnhance.Contrast(earth_strip).enhance(1.24)
    earth_strip = ImageEnhance.Brightness(earth_strip).enhance(1.02)

    # Deep dramatic cosmic space with vivid blue-shifted forward aberration glow (right) & deep crimson aft shift (far left)
    bg = make_cosmic_bg(
        seed=2402,
        base_rgb=(8, 14, 42),
        glow_rgb=(16, 118, 245),
        gx=960, gy=330, gr=470,
        sec_glow=((135, 32, 46), 110, 320, 340),
        stars=70,
    )
    # Crisp relativistic radial starlight streaks fanning toward the forward blue-shift convergence point (970, 335)
    rng = np.random.default_rng(2409)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    vx, vy = 975.0, 338.0
    for _ in range(260):
        ang = rng.uniform(0, 2 * math.pi)
        r_start = rng.uniform(38, 560)
        length = rng.uniform(45, 220) * (0.45 + r_start / 440.0)
        x0 = vx + math.cos(ang) * r_start
        y0 = vy + math.sin(ang) * r_start
        x1 = vx + math.cos(ang) * (r_start + length)
        y1 = vy + math.sin(ang) * (r_start + length)
        if y0 > 540 and y1 > 540:
            continue
        if x0 < 310:
            col = (255, int(rng.integers(105, 165)), int(rng.integers(75, 115)), int(rng.integers(120, 215)))
        else:
            col = (int(rng.integers(125, 225)), int(rng.integers(215, 255)), 255, int(rng.integers(140, 240)))
        lw = int(rng.choice([2, 2, 3, 4]))
        od.line((x0, y0, x1, y1), fill=col, width=lw)
    core = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.ellipse((vx - 125, vy - 125, vx + 125, vy + 125), fill=(70, 195, 255, 125))
    cd.ellipse((vx - 44, vy - 44, vx + 44, vy + 44), fill=(225, 248, 255, 210))
    core = core.filter(ImageFilter.GaussianBlur(26))
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.7))

    base = bg.convert("RGBA")
    base.alpha_composite(overlay)
    base.alpha_composite(core)

    # Seamlessly blend Earth's glowing blue curved limb along the bottom (y=360..720)
    earr = np.asarray(earth_strip, dtype=np.float32)
    elum = 0.299 * earr[:, :, 0] + 0.587 * earr[:, :, 1] + 0.114 * earr[:, :, 2]
    e_alpha = np.clip((elum - 14.0) / 34.0, 0.0, 1.0)
    e_rgba = np.zeros((360, W, 4), dtype=np.uint8)
    e_rgba[:, :, :3] = np.clip(earr, 0, 255).astype(np.uint8)
    e_rgba[:, :, 3] = (e_alpha * 255).astype(np.uint8)
    base.alpha_composite(Image.fromarray(e_rgba, "RGBA"), (0, 360))
    bg = base.convert("RGB")

    # Extract Bruce McCandless II astronaut with exterior flood-fill (keeps dark helmet visor 100% solid, zero dark outline!)
    sub = src.crop((790, 620, 1070, 920))
    sub_arr = np.asarray(sub, dtype=np.float32)
    slum = 0.299 * sub_arr[:, :, 0] + 0.587 * sub_arr[:, :, 1] + 0.114 * sub_arr[:, :, 2]
    ys, xs = np.where(slum > 36)
    astro_crop = sub.crop((max(0, int(xs.min()) - 10), max(0, int(ys.min()) - 10),
                           min(sub.width, int(xs.max()) + 10), min(sub.height, int(ys.max()) + 10)))
    scale = 1.75  # strictly < 2.35x upscale limit
    aw, ah = int(astro_crop.width * scale), int(astro_crop.height * scale)
    astro_hi = astro_crop.resize((aw, ah), Image.LANCZOS)
    astro_hi = ImageEnhance.Contrast(astro_hi).enhance(1.16)
    astro_hi = ImageEnhance.Sharpness(astro_hi).enhance(1.25)

    aarr = np.asarray(astro_hi, dtype=np.float32)
    alum = 0.299 * aarr[:, :, 0] + 0.587 * aarr[:, :, 1] + 0.114 * aarr[:, :, 2]
    fg_bool = _exterior_bg_mask(alum, thresh=34.0)
    # Erode 1px to remove any residual dark space fringe, then soften edge 1px
    m_img = Image.fromarray((fg_bool.astype(np.uint8) * 255)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    a_mask = np.asarray(m_img, dtype=np.float32) / 255.0

    yy_a, xx_a = np.mgrid[0:ah, 0:aw]
    right_bias = np.clip((xx_a - aw * 0.45) / (aw * 0.55), 0.0, 1.0)
    aarr[:, :, 2] = np.clip(aarr[:, :, 2] + 34.0 * right_bias, 0, 255)
    aarr[:, :, 1] = np.clip(aarr[:, :, 1] + 20.0 * right_bias, 0, 255)

    astro_rgba = np.zeros((ah, aw, 4), dtype=np.uint8)
    astro_rgba[:, :, :3] = np.clip(aarr, 0, 255).astype(np.uint8)
    astro_rgba[:, :, 3] = (a_mask * 255).astype(np.uint8)
    astro_fg = Image.fromarray(astro_rgba, "RGBA")

    paste_with_glow(bg, astro_fg, (305, 198), glow_rgb=(75, 205, 255), blur=22, strength=0.65)

    bg = apply_top_band_scrim(bg, band_rgb=(8, 14, 44), strength=0.74)
    font_sz, text_bot = draw_top_band_text(
        bg,
        [("YOU", WHITE), ("AGE", WHITE), ("SLOWER", YELLOW)],
        max_w=1180,
        start_size=106,
        y_center=76,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=93, optimize=True)
    sc = score_thumb(out_path, "long")
    return {
        "video": "rVqgtkBV3jc",
        "film": "024",
        "hook": "YOU AGE SLOWER",
        "yellow_word": "SLOWER",
        "font_size": font_sz,
        "text_bottom_y": text_bot,
        "astronaut_upscale": scale,
        "file": str(out_path),
        "bytes": out_path.stat().st_size,
        "sha256": sha256(out_path),
        "score": sc,
        "sources": [
            {"nasa_id": "S84-27018", "desc": "NASA STS-41B Bruce McCandless II untethered EVA above Earth's curved limb"},
        ],
    }


def build_last_star(plates: Path, earth_path: Path, out_path: Path) -> dict:
    """3. REXYxuLOBoI (005 Last Star) -> OUTLIVES OUR SUN (yellow OUTLIVES)."""
    bg = make_cosmic_bg(
        seed=503,
        base_rgb=(12, 16, 48),
        glow_rgb=(155, 32, 14),
        gx=800, gy=432, gr=520,
        sec_glow=((22, 68, 168), 210, 445, 390),
        stars=110,
    )
    sun = Image.open(plates / "nasa_sdo_304.jpg").convert("RGB")
    sarr = np.asarray(sun, dtype=np.float32)
    slum = 0.299 * sarr[:, :, 0] + 0.587 * sarr[:, :, 1] + 0.114 * sarr[:, :, 2]
    ys, xs = np.where(slum > 10)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    scrop = sun.crop((max(0, x0 - 10), max(0, y0 - 10), min(sun.width, x1 + 10), min(sun.height, y1 + 10)))

    target_h = 532
    target_w = int(scrop.width * target_h / scrop.height)
    star_scaled = scrop.resize((target_w, target_h), Image.LANCZOS)
    star_scaled = ImageEnhance.Contrast(star_scaled).enhance(1.16)
    star_scaled = ImageEnhance.Color(star_scaled).enhance(1.22)
    star_scaled = ImageEnhance.Brightness(star_scaled).enhance(1.10)

    # Pure Screen blend (zero muddy dark coronal halo; fiery prominence glows radiantly into deep indigo space!)
    star_layer = Image.new("RGB", (W, H), (0, 0, 0))
    star_layer.paste(star_scaled, (492, 166))
    # Add soft fiery outer corona bloom via blurred screen layer
    bloom = star_layer.filter(ImageFilter.GaussianBlur(22))
    bg_f = np.asarray(bg, dtype=np.float32) / 255.0
    st_f = np.asarray(star_layer, dtype=np.float32) / 255.0
    bl_f = (np.asarray(bloom, dtype=np.float32) / 255.0) * 0.55
    comp = 1.0 - (1.0 - bg_f) * (1.0 - bl_f)
    comp = 1.0 - (1.0 - comp) * (1.0 - st_f)
    bg = Image.fromarray(np.clip(comp * 255.0, 0, 255).astype(np.uint8))

    # Scale/story reference: Apollo 17 Blue Marble Earth on lower-left with subtle warm red-star rim light
    earth = extract_earth_globe(earth_path, diam=182, warm_rim=True)
    paste_with_glow(bg, earth, (132, 416), glow_rgb=(50, 150, 255), blur=20, strength=0.68)

    bg = apply_top_band_scrim(bg, band_rgb=(12, 14, 44), strength=0.70)
    font_sz, text_bot = draw_top_band_text(
        bg,
        [("OUTLIVES", YELLOW), ("OUR", WHITE), ("SUN", WHITE)],
        max_w=1180,
        start_size=106,
        y_center=76,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=93, optimize=True)
    sc = score_thumb(out_path, "long")
    return {
        "video": "REXYxuLOBoI",
        "film": "005",
        "hook": "OUTLIVES OUR SUN",
        "yellow_word": "OUTLIVES",
        "font_size": font_sz,
        "text_bottom_y": text_bot,
        "file": str(out_path),
        "bytes": out_path.stat().st_size,
        "sha256": sha256(out_path),
        "score": sc,
        "sources": [
            {"nasa_id": "GSFC_20171208_Archive_e002069", "desc": "NASA/GSFC SDO AIA 304 Å extreme-UV full-disk solar plate with launching filament (red-dwarf photosphere visual)"},
            {"nasa_id": "as17-148-22727", "desc": "NASA Apollo 17 Blue Marble Earth (habitable-zone story/scale inset, not to scale)"},
        ],
    }


def make_comparison_sheet(pairs: list[tuple[str, Path, Path]], out_path: Path) -> None:
    """Build A vs B comparison sheet showing 168x94 phone search tiles (with simulated duration badge) + 360x202 home tiles."""
    font = ImageFont.truetype(FONT_PATH, 16)
    badge_font_sm = ImageFont.truetype(FONT_PATH, 10)
    badge_font_lg = ImageFont.truetype(FONT_PATH, 14)

    def with_badge(im: Image.Image, size: tuple[int, int], dur: str, bfont) -> Image.Image:
        tile = ImageOps.fit(im.convert("RGB"), size, Image.LANCZOS)
        d = ImageDraw.Draw(tile)
        bw = int(d.textlength(dur, font=bfont)) + 10
        bh = int(bfont.size * 1.45)
        pad = 5 if size[0] < 200 else 8
        x0, y0 = size[0] - bw - pad, size[1] - bh - pad
        d.rounded_rectangle((x0, y0, size[0] - pad, size[1] - pad), radius=3, fill=(0, 0, 0))
        d.text((x0 + 5, y0 + 1), dur, font=bfont, fill=WHITE)
        return tile

    row_h = 240
    sheet_w = 1140
    sheet_h = 34 + row_h * len(pairs)
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    d.text((16, 8), "J3302 Weekly Audit (2026-11-21) — Live A (left) vs Proposed B (right) @ 168x94 + 360x202 with duration badge", font=font, fill=(20, 20, 20))

    durs = {"NbW5G1BpPY0": "9:19", "rVqgtkBV3jc": "8:55", "REXYxuLOBoI": "8:38"}
    for idx, (vid, live_p, new_p) in enumerate(pairs):
        y = 38 + idx * row_h
        dur = durs.get(vid, "9:00")
        im_a = Image.open(live_p)
        im_b = Image.open(new_p)
        d.text((16, y), f"{vid}: Live A vs Proposed B", font=font, fill=(30, 30, 30))
        sheet.paste(with_badge(im_a, (168, 94), dur, badge_font_sm), (16, y + 26))
        sheet.paste(with_badge(im_a, (360, 202), dur, badge_font_lg), (196, y + 26))
        sheet.paste(with_badge(im_b, (168, 94), dur, badge_font_sm), (580, y + 26))
        sheet.paste(with_badge(im_b, (360, 202), dur, badge_font_lg), (760, y + 26))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=92)


def copy_verified(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    h1, h2 = sha256(src), sha256(dst)
    if h1 != h2:
        raise RuntimeError(f"SHA-256 mismatch copying {src} -> {dst}: {h1} != {h2}")
    return h2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plates", type=Path, default=DEFAULT_PLATES)
    ap.add_argument("--earth", type=Path, default=DEFAULT_EARTH)
    ap.add_argument("--live", type=Path, default=DEFAULT_LIVE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--publish-nas", action="store_true", help="Copy verified v01 Bs, live As, and phone sheets to /Volumes/data/studio-live film folders")
    ns = ap.parse_args()

    ns.out.mkdir(parents=True, exist_ok=True)
    r1 = build_europa(ns.plates, ns.earth, ns.out / "NbW5G1BpPY0_B_v01.jpg")
    r2 = build_light_speed(ns.plates, ns.out / "rVqgtkBV3jc_B_v01.jpg")
    r3 = build_last_star(ns.plates, ns.earth, ns.out / "REXYxuLOBoI_B_v01.jpg")
    results = [r1, r2, r3]

    # Run official thumb_preview.py --score
    tp = SYS_TOOLS / "thumb_preview.py"
    score_sheet = ns.out / "THUMB_PREVIEW_SCORE_SHEET.jpg"
    proc = subprocess.run(
        [sys.executable, str(tp), "long", r1["file"], r2["file"], r3["file"], "--out", str(score_sheet), "--score"],
        capture_output=True, text=True,
    )
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode

    comp_sheet = ns.out / "PHONE_BADGE_SHEET_v01.jpg"
    make_comparison_sheet(
        [
            ("NbW5G1BpPY0", ns.live / "NbW5G1BpPY0.jpg", Path(r1["file"])),
            ("rVqgtkBV3jc", ns.live / "rVqgtkBV3jc.jpg", Path(r2["file"])),
            ("REXYxuLOBoI", ns.live / "REXYxuLOBoI.jpg", Path(r3["file"])),
        ],
        comp_sheet,
    )

    nas_dirs = {
        "NbW5G1BpPY0": NAS_BASE / "006_Could-Life-Exist-Under-The-Ice-Of-Europa/08_Thumbnails/repackage_2026-11/J3302_v01",
        "rVqgtkBV3jc": NAS_BASE / "024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnails/repackage_2026-11/J3302_v01",
        "REXYxuLOBoI": NAS_BASE / "005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3302_v01",
    }

    if ns.publish_nas:
        if not NAS_BASE.exists():
            raise RuntimeError(f"NAS share not mounted: {NAS_BASE}")
        for r in results:
            vid = r["video"]
            nd = nas_dirs[vid]
            b_dst = nd / f"{vid}_B_v01.jpg"
            a_dst = nd / f"{vid}_live_A.jpg"
            s_dst = nd / f"{vid}_phone_badge_sheet_v01.jpg"
            r["nas_b"] = str(b_dst)
            r["nas_b_sha256"] = copy_verified(Path(r["file"]), b_dst)
            r["nas_a"] = str(a_dst)
            r["nas_a_sha256"] = copy_verified(ns.live / f"{vid}.jpg", a_dst)
            r["nas_sheet"] = str(s_dst)
            # Individual A vs B badge sheet per film
            indiv_tmp = ns.out / f"{vid}_phone_badge_sheet_v01.jpg"
            make_comparison_sheet([(vid, ns.live / f"{vid}.jpg", Path(r["file"]))], indiv_tmp)
            r["nas_sheet_sha256"] = copy_verified(indiv_tmp, s_dst)

    manifest = {
        "job": "J3302",
        "date": "2026-11-21",
        "builder": "00_Brand/Channel-Setup/tools/build_weekly_thumbs_j3302.py",
        "score_output": proc.stdout.strip().splitlines(),
        "comparison_sheet": str(comp_sheet),
        "candidates": results,
    }
    (ns.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {ns.out / 'MANIFEST.json'} and {comp_sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
