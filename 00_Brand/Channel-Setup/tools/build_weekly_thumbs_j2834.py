#!/usr/bin/env python3
"""J2834 / J2983: reproducible weekly thumbnail builder for Orbit With Ben (v03, 2026-11-17).
Rebuilds the 3 Test & Compare B challengers per Packaging Panel Decision J2843:
  1. m09jUdwC5hk (How Long Will Anything in Space Last?) -> m09jUdwC5hk_B_v05.jpg (RINGS ARE LEAVING)
     Real NASA/JPL/SSI Cassini backlit mosaic PIA08329 ('In Saturn's Shadow') + ring-rain arrow.
  2. Mo93x0fxB1Q (Why Haven't We Found Aliens Yet? The Fermi Paradox Explained) -> Mo93x0fxB1Q_B_v05.jpg (ZERO SIGNALS)
     Real NASA PIA12348 Milky Way Galactic Centre + PIA26716 Goldstone 70-m DSN dish, with smooth
     feathered top band (no y=72 seam), yellow reticle over dark empty sky pocket (broadly feathered
     darkened/desaturated dust region), and anchored dish pedestal with highlight compression + blue rim light.
  3. ziKBPJ6FY0U (JWST Found Galaxies That Shouldn't Exist Yet) -> ziKBPJ6FY0U_B_v06.jpg (300 MILLION YEARS)
     Real NASA/ESA/CSA/STScI JADES NIRCam deep field & native cutout of JADES-GS-z14-0 (z=14.32,
     ~290-300 Myr after the Big Bang, STScI-01HZ083EXXCJNE64ERAH2ER2FM), with small yellow origin
     ring centered on the exact pixel location of JADES-GS-z14-0, foreground star glare dimmed ~32%,
     smooth unposterised cosmic-navy grade, and tightened top-band tracking for 168x94 stroke weight.
£0 spend; 100% public-domain NASA/JPL/ESA/CSA/STScI plates; no YouTube Studio writes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = (
    Path(__file__).resolve().parents[3]
    if "00_Brand" in str(Path(__file__).resolve())
    else Path.cwd()
)
SYS_TOOLS = ROOT / "00_Brand/Channel-Setup/tools"
sys.path.insert(0, str(SYS_TOOLS))
from thumb_preview import score as score_thumb  # noqa: E402

DEFAULT_PLATES = Path.home() / "_desk/j2834/plates"
DEFAULT_LIVE = Path.home() / "_desk/j2834/live"
DEFAULT_OUT = Path.home() / "_desk/j2834/designs_v03"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

W, H = 1280, 720
BAND_H = 148
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def starfield_bg(
    seed: int,
    base_rgb: tuple[int, int, int],
    glow_rgb: tuple[int, int, int],
    gx: float = 640.0,
    gy: float = 435.0,
    gr: float = 560.0,
) -> Image.Image:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.exp(-(((xx - gx) ** 2) / (gr**2) + ((yy - gy) ** 2) / ((gr * 0.72) ** 2)))
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for k in range(3):
        arr[:, :, k] = base_rgb[k] + glow_rgb[k] * g
    arr += rng.normal(0, 0.9, (H, W, 1))
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(85):
        sx = int(rng.integers(20, W - 20))
        sy = int(rng.integers(BAND_H + 8, H - 20))
        sv = int(rng.integers(105, 215))
        r = 1 if rng.random() < 0.84 else 2
        d.ellipse((sx, sy, sx + r, sy + r), fill=(sv, sv, min(255, sv + 32)))
    return im


def draw_arrow(
    im: Image.Image,
    p0: tuple[float, float],
    p1: tuple[float, float],
    color: tuple[int, int, int] = WHITE,
    shaft_w: int = 15,
    head_len: float = 44.0,
    head_half: float = 25.0,
) -> None:
    d = ImageDraw.Draw(im)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    bx, by = p1[0] - ux * head_len, p1[1] - uy * head_len
    b_tip = (p1[0] + ux * 6, p1[1] + uy * 6)
    b_base_x, b_base_y = bx - ux * 4, by - uy * 4
    d.line((p0[0], p0[1], bx, by), fill=BLACK, width=shaft_w + 11)
    d.polygon(
        [
            b_tip,
            (b_base_x + px * (head_half + 7), b_base_y + py * (head_half + 7)),
            (b_base_x - px * (head_half + 7), b_base_y - py * (head_half + 7)),
        ],
        fill=BLACK,
    )
    d.line((p0[0], p0[1], bx + ux * 4, by + uy * 4), fill=color, width=shaft_w)
    d.polygon(
        [
            p1,
            (bx + px * head_half, by + py * head_half),
            (bx - px * head_half, by - py * head_half),
        ],
        fill=color,
    )


def _word_advance(
    d: ImageDraw.ImageDraw,
    word: str,
    font: ImageFont.FreeTypeFont,
    stroke: int,
    tracking: int,
) -> int:
    if tracking == 0:
        bb = d.textbbox((0, 0), word, font=font, stroke_width=stroke)
        return bb[2] - bb[0]
    adv = 0
    for i, ch in enumerate(word):
        cb = d.textbbox((0, 0), ch, font=font, stroke_width=0)
        adv += (cb[2] - cb[0]) + (tracking if i < len(word) - 1 else 0)
    return adv + stroke * 2


def _draw_tracked_word(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    word: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    stroke: int,
    tracking: int,
) -> tuple[int, int, int, int]:
    if tracking == 0:
        d.text((x + 4, y + 5), word, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        d.text((x, y), word, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
        return d.textbbox((x, y), word, font=font, stroke_width=stroke)

    cx = x
    boxes = []
    for ch in word:
        d.text((cx + 4, y + 5), ch, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        cb = d.textbbox((cx, y), ch, font=font, stroke_width=0)
        cx += (cb[2] - cb[0]) + tracking
    cx = x
    for ch in word:
        d.text((cx, y), ch, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        cb = d.textbbox((cx, y), ch, font=font, stroke_width=0)
        cx += (cb[2] - cb[0]) + tracking
    cx = x
    for ch in word:
        d.text((cx, y), ch, font=font, fill=fill, stroke_width=0)
        boxes.append(d.textbbox((cx, y), ch, font=font, stroke_width=stroke))
        cb = d.textbbox((cx, y), ch, font=font, stroke_width=0)
        cx += (cb[2] - cb[0]) + tracking
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


def draw_top_band(
    im: Image.Image,
    words: list[str],
    yellow_word: str,
    tracking: int = 0,
    space_scale: float = 1.0,
    max_w_frac: float = 0.92,
) -> list[int]:
    # Smooth cosine-feathered top navy gradient across y=0..192 (zero hard horizontal seam)
    arr = np.asarray(im).astype(np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    t = np.clip(yy / 192.0, 0.0, 1.0)
    alpha = (0.5 * (1.0 + np.cos(np.pi * t))) ** 1.15 * 0.86
    band_rgb = np.array([12.0, 19.0, 56.0], dtype=np.float32)[None, None, :]
    arr = arr * (1.0 - alpha) + band_rgb * alpha
    im.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))

    d = ImageDraw.Draw(im)
    size, stroke = 114, 9
    while size > 62:
        font = ImageFont.truetype(FONT_PATH, size)
        space = max(14, int(round(d.textbbox((0, 0), " ", font=font)[2] * space_scale)))
        widths = [_word_advance(d, w, font, stroke, tracking) for w in words]
        total_w = sum(widths) + space * (len(words) - 1)
        top_bb = d.textbbox((0, 0), " ".join(words), font=font, stroke_width=stroke)
        th = top_bb[3] - top_bb[1]
        if total_w <= W * max_w_frac and th <= BAND_H - 18:
            break
        size -= 2

    x = (W - total_w) // 2
    y = (BAND_H - th) // 2 - top_bb[1] + 2
    ink_boxes = []
    for w, ww in zip(words, widths):
        fill = YELLOW if w == yellow_word else WHITE
        bb = _draw_tracked_word(d, x, y, w, font, fill, stroke, tracking)
        ink_boxes.append(bb)
        x += ww + space
    return [
        min(b[0] for b in ink_boxes),
        min(b[1] for b in ink_boxes),
        max(b[2] for b in ink_boxes),
        max(b[3] for b in ink_boxes),
    ]


def build_compilation(plates: Path, out_dir: Path) -> dict:
    """m09jUdwC5hk — How Long Will Anything in Space Last? -> m09jUdwC5hk_B_v05.jpg (RINGS ARE LEAVING).
    Replaces cyan Helix Nebula (PIA09178) per 2-of-3 panel consensus (codex.md + cursor.md) with
    real NASA/JPL/SSI Cassini backlit mosaic PIA08329 ('In Saturn's Shadow') filling >1/3 of the frame,
    graded with warm golden-amber backlit ring detail (unclipped Cassini Division & ringlets) against
    deep cosmic midnight-indigo, plus one crisp white discovery arrow pointing directly into the inner
    C/D-ring gap raining inward toward Saturn's equatorial limb.
    """
    sat_path = plates / "PIA08329.tif" if (plates / "PIA08329.tif").exists() else plates / "PIA08329.jpg"
    sat_raw = Image.open(sat_path).convert("RGB")

    sat_rot = sat_raw.rotate(-10.0, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=(0, 0, 0))
    rw, rh = sat_rot.size
    cw, ch = 1640, 922
    cx0 = rw // 2 - cw // 2
    cy0 = rh // 2 - int(ch * 0.565)
    crop = sat_rot.crop((cx0, max(0, cy0), cx0 + cw, max(0, cy0) + ch)).resize((W, H), Image.Resampling.LANCZOS)

    bg = starfield_bg(19, (13, 21, 58), (24, 52, 132), gx=640.0, gy=445.0, gr=580.0)
    bg_arr = np.asarray(bg).astype(np.float32)

    s_arr = np.asarray(crop).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W]
    scx = (rw * 0.5 - cx0) * (W / cw)
    scy = (rh * 0.5 - max(0, cy0)) * (H / ch)
    sr_globe = 232.0 * (W / cw)
    dist_globe = np.hypot(xx - scx, (yy - scy) * 1.07)
    inside_globe = np.clip((sr_globe - dist_globe) / 10.0, 0.0, 1.0)[..., None]

    ring_lum = 0.299 * s_arr[:, :, 0] + 0.587 * s_arr[:, :, 1] + 0.114 * s_arr[:, :, 2]
    s_lifted = np.power(np.clip(s_arr, 0.0, 1.0), 0.80)
    halo_mask = np.clip(1.0 - ring_lum * 2.8, 0.0, 1.0)
    main_mask = 1.0 - halo_mask
    graded = np.zeros_like(s_lifted)
    r_ch = s_lifted[:, :, 0] * (1.36 * main_mask + 1.05 * halo_mask)
    g_ch = s_lifted[:, :, 1] * (1.12 * main_mask + 1.10 * halo_mask)
    b_ch = s_lifted[:, :, 2] * (0.82 * main_mask + 1.48 * halo_mask)
    graded[:, :, 0] = r_ch / (1.0 + 0.22 * r_ch * r_ch)
    graded[:, :, 1] = g_ch / (1.0 + 0.22 * g_ch * g_ch)
    graded[:, :, 2] = b_ch / (1.0 + 0.18 * b_ch * b_ch)

    globe_dark = np.clip(graded * 255.0 * 1.22 + np.array([4.0, 7.0, 18.0]), 0.0, 255.0)
    ring_alpha = np.clip((ring_lum - 0.025) * 4.2, 0.0, 1.0)[..., None]
    halo_screen = 255.0 * (1.0 - (1.0 - bg_arr / 255.0) * (1.0 - np.clip(graded * 1.10, 0.0, 1.0)))
    outer_comp = halo_screen * (1.0 - ring_alpha * 0.65) + np.clip(graded * 255.0 * 1.24, 0.0, 255.0) * (
        ring_alpha * 0.65
    )

    comp = inside_globe * globe_dark + (1.0 - inside_globe) * outer_comp
    im = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.16)
    im = ImageEnhance.Color(im).enhance(1.30)

    p_tip = (scx - sr_globe * 1.04, scy - sr_globe * 0.22)
    p_tail = (p_tip[0] - 208.0, p_tip[1] - 118.0)
    draw_arrow(im, p_tail, p_tip, color=WHITE, shaft_w=15, head_len=44.0, head_half=25.0)

    bbox = draw_top_band(im, ["RINGS", "ARE", "LEAVING"], "LEAVING", tracking=-3, space_scale=0.82)
    out = out_dir / "m09jUdwC5hk_B_v05.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "m09jUdwC5hk",
        "ledger_id": "T037",
        "prior_draft_file": "m09jUdwC5hk_B_v04.jpg",
        "film": "005_The-Last-Star-In-The-Universe (owb_compilation_v05)",
        "live_title": "How Long Will Anything in Space Last?",
        "proposed_title_b": "How Long Will the Universe Last? (Until the Last Star Dies)",
        "reserve_title_b": "When Will Saturn's Rings, the Moon and the Last Star Die?",
        "hook": "RINGS ARE LEAVING",
        "yellow": "LEAVING",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            f"NASA/JPL/Space Science Institute {sat_path.name} (Cassini 'In Saturn's Shadow' backlit Saturn & rings mosaic PIA08329, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_fermi(plates: Path, out_dir: Path) -> dict:
    """Mo93x0fxB1Q — Why Haven't We Found Aliens Yet? The Fermi Paradox Explained -> Mo93x0fxB1Q_B_v05.jpg.
    Keeps panel-winning ZERO SIGNALS concept and applies all 3 consensus fixes (3/3 critics):
      1. Full-bleed 1280x720 Milky Way plate + smooth cosine-feathered top navy gradient (zero y=72 seam).
      2. Yellow reticle moved well clear of the bright Sgr A* core onto an upper-right dark dust lane,
         with a broad, softly feathered 42% darkening/desaturation across that sky pocket so it reads
         naturally at 1280x720 and unmistakably as empty sky ('ZERO SIGNALS') at 168x94.
      3. Goldstone 70-m dish (PIA26716) anchored cleanly through bottom-left corner (zero slanted cut)
         with highlights pulled down ~13% and a subtle sky-side blue rim light preserving mesh detail.
    """
    mw_raw = Image.open(plates / "PIA12348.jpg").convert("RGB")
    rw, rh = mw_raw.size
    cw = 1560
    ch = int(round(cw * (H / W)))
    x0 = rw - cw
    y0 = (rh - ch) // 2
    mw = mw_raw.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
    mw = ImageEnhance.Contrast(mw).enhance(1.22)
    mw = ImageEnhance.Color(mw).enhance(1.38)

    arr = np.asarray(mw).astype(np.float32)
    lum_bg = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0
    lift = np.exp(-lum_bg * 4.2)
    arr[:, :, 0] += lift * 16.0
    arr[:, :, 1] += lift * 22.0
    arr[:, :, 2] += lift * 56.0

    cx, cy, rad = 955, 382, 96
    yy, xx = np.mgrid[0:H, 0:W]
    r_dist = np.hypot(xx - cx, (yy - cy) * 1.08)
    broad_dust = np.exp(-((r_dist / 155.0) ** 2)) * 0.72
    inner_void = (1.0 / (1.0 + np.exp((r_dist - (rad * 1.05)) / 32.0))) * 0.28
    void_mask = np.clip(broad_dust + inner_void, 0.0, 0.88)

    gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2])[..., None]
    desat = arr * 0.46 + gray * 0.54
    pocket_target = np.zeros_like(arr)
    pocket_target[:, :, 0] = np.clip(desat[:, :, 0] * 0.36 + 7.0, 9.0, 48.0)
    pocket_target[:, :, 1] = np.clip(desat[:, :, 1] * 0.40 + 11.0, 13.0, 56.0)
    pocket_target[:, :, 2] = np.clip(desat[:, :, 2] * 0.52 + 26.0, 28.0, 92.0)
    arr = arr * (1.0 - void_mask[..., None]) + pocket_target * void_mask[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    dsn_raw = Image.open(plates / "PIA26716.jpg").convert("RGB")
    dw, dh = dsn_raw.size
    dsn_crop = dsn_raw.crop((0, int(dh * 0.34), dw, dh))
    cw_d, ch_d = dsn_crop.size
    ext = Image.new("RGB", (cw_d, ch_d + 240), (0, 0, 0))
    ext.paste(dsn_crop, (0, 0))
    bottom_strip = dsn_crop.crop((0, ch_d - 16, cw_d, ch_d)).resize((cw_d, 240), Image.Resampling.BILINEAR)
    ext.paste(bottom_strip, (0, ch_d))

    d_arr = np.asarray(ext).astype(np.float32)
    lum = 0.299 * d_arr[:, :, 0] + 0.587 * d_arr[:, :, 1] + 0.114 * d_arr[:, :, 2]
    alpha = np.clip((lum - 18.0) * 6.2, 0.0, 255.0).astype(np.uint8)
    alpha_im = Image.fromarray(alpha).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.8))

    eh, ew = d_arr.shape[:2]
    dy_grid, dx_grid = np.mgrid[0:eh, 0:ew]
    sky_facing = np.clip((dx_grid / ew) * 0.65 + (1.0 - dy_grid / eh) * 0.55, 0.0, 1.0)
    norm = d_arr / 255.0
    compressed = (norm * 0.84) / (1.0 + 0.14 * norm * norm) * 255.0
    shade = (0.76 + 0.24 * sky_facing)[..., None]
    graded = compressed * shade
    rim = (sky_facing**2.2)[..., None]
    graded[:, :, 0] = np.clip(graded[:, :, 0] * 0.90 + 8.0 + rim[:, :, 0] * 8.0, 0, 242)
    graded[:, :, 1] = np.clip(graded[:, :, 1] * 0.95 + 14.0 + rim[:, :, 0] * 26.0, 0, 248)
    graded[:, :, 2] = np.clip(graded[:, :, 2] * 1.06 + 30.0 + rim[:, :, 0] * 48.0, 0, 255)

    dsn_rgba = Image.fromarray(graded.astype(np.uint8)).convert("RGBA")
    dsn_rgba.putalpha(alpha_im)
    dsn_rot = dsn_rgba.rotate(-16, resample=Image.Resampling.BICUBIC, expand=True)
    dsn_small = dsn_rot.resize((640, 665), Image.Resampling.LANCZOS)

    shadow_alpha = dsn_small.getchannel("A").filter(ImageFilter.GaussianBlur(6))
    shadow = Image.new("RGBA", dsn_small.size, (6, 10, 28, 0))
    shadow.putalpha(shadow_alpha)

    canvas = im.convert("RGBA")
    canvas.alpha_composite(shadow, (-80, 232))
    canvas.alpha_composite(dsn_small, (-86, 226))

    od = ImageDraw.Draw(canvas)
    od.ellipse((cx - rad - 4, cy - rad - 4, cx + rad + 4, cy + rad + 4), outline=(0, 0, 0, 240), width=15)
    od.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=(255, 230, 0, 255), width=9)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        od.line(
            (cx + dx * (rad - 18), cy + dy * (rad - 18), cx + dx * (rad + 24), cy + dy * (rad + 24)),
            fill=(0, 0, 0, 240),
            width=12,
        )
        od.line(
            (cx + dx * (rad - 15), cy + dy * (rad - 15), cx + dx * (rad + 20), cy + dy * (rad + 20)),
            fill=(255, 230, 0, 255),
            width=6,
        )

    im = canvas.convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.10)
    bbox = draw_top_band(im, ["ZERO", "SIGNALS"], "ZERO", tracking=-1, space_scale=0.92)
    out = out_dir / "Mo93x0fxB1Q_B_v05.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "Mo93x0fxB1Q",
        "ledger_id": "T038",
        "prior_draft_file": "Mo93x0fxB1Q_B_v04.jpg",
        "film": "001_Will-We-Ever-Meet-Aliens",
        "live_title": "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
        "proposed_title_b": "Fermi Paradox: Why Haven't We Found Aliens Yet?",
        "reserve_title_b": "The Fermi Paradox: Why Is the Universe So Quiet?",
        "hook": "ZERO SIGNALS",
        "yellow": "ZERO",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA/JPL-Caltech/ESA/CXC/STScI PIA12348 (Great Observatories Milky Way Galactic Centre composite, public domain)",
            "NASA/JPL-Caltech PIA26716 (Goldstone Deep Space Network 70-meter radio antenna photograph, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_jwst(plates: Path, out_dir: Path) -> dict:
    """ziKBPJ6FY0U — JWST Found Galaxies That Shouldn't Exist Yet -> ziKBPJ6FY0U_B_v06.jpg (300 MILLION YEARS).
    Fixes loupe source & origin ring per 2-of-3 panel consensus (codex.md + gemini.md):
      - Uses real NASA/ESA/CSA/STScI JADES NIRCam deep field & native cutout of JADES-GS-z14-0
        (STScI-01HZ083EXXCJNE64ERAH2ER2FM, spectroscopically confirmed at z=14.32, ~290-300 million
        years after the Big Bang; matches Scene 04: 'Some of the galaxies Webb confirmed are luminous
        when the universe was only about three hundred million years old').
      - Rotates field -28 deg around JADES-GS-z14-0 so the arrow corridor to the loupe is clean of
        bright foreground edge-on galaxies, and places the small yellow origin circle directly on the
        exact pixel coordinates of JADES-GS-z14-0.
      - Dims foreground diffraction-spiked star glare by ~32% and grades a deep, unposterised cosmic
        indigo background, with tightened tracking on '300 MILLION YEARS' for thicker 168x94 strokes.
    """
    field_raw = Image.open(plates / "JADES_GS_z14_0_field.jpg").convert("RGB")
    cutout_raw = Image.open(plates / "JADES_GS_z14_0_cutout.png").convert("RGB")
    fw, fh = field_raw.size

    gx_full = fw * 0.600500
    gy_full = fh * 0.463664

    field_rot = field_raw.rotate(
        -28.0, resample=Image.Resampling.BICUBIC, expand=False, center=(gx_full, gy_full), fillcolor=(6, 8, 18)
    )

    sx_target, sy_target = 468, 434
    cw, ch = 1920, 1080
    x0 = int(round(gx_full - (sx_target / W) * cw))
    y0 = int(round(gy_full - (sy_target / H) * ch))
    x0 = max(0, min(fw - cw, x0))
    y0 = max(0, min(fh - ch, y0))
    sx = int(round((gx_full - x0) * (W / cw)))
    sy = int(round((gy_full - y0) * (H / ch)))

    crop = field_rot.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
    c_arr = np.asarray(crop).astype(np.float32)

    lum = (0.299 * c_arr[:, :, 0] + 0.587 * c_arr[:, :, 1] + 0.114 * c_arr[:, :, 2]) / 255.0
    star_glare = np.clip((lum - 0.44) / 0.56, 0.0, 1.0) ** 1.35
    glare_blur = (
        np.asarray(Image.fromarray((star_glare * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(
            np.float32
        )
        / 255.0
    )
    dim_factor = 1.0 - 0.34 * np.maximum(star_glare, glare_blur * 0.75)
    c_arr = c_arr * dim_factor[..., None]

    norm = np.clip(c_arr / 255.0, 0.0, 1.0)
    lifted = np.power(norm, 0.82)
    yy, xx = np.mgrid[0:H, 0:W]
    radial = np.exp(-(((xx - 660.0) ** 2) / (680.0**2) + ((yy - 420.0) ** 2) / (460.0**2)))
    sky_r = 12.0 + 13.0 * radial
    sky_g = 19.0 + 19.0 * radial
    sky_b = 52.0 + 44.0 * radial
    out_arr = np.zeros_like(c_arr)
    out_arr[:, :, 0] = 255.0 * (1.0 - (1.0 - lifted[:, :, 0] * 1.26) * (1.0 - sky_r / 255.0))
    out_arr[:, :, 1] = 255.0 * (1.0 - (1.0 - lifted[:, :, 1] * 1.15) * (1.0 - sky_g / 255.0))
    out_arr[:, :, 2] = 255.0 * (1.0 - (1.0 - lifted[:, :, 2] * 1.12) * (1.0 - sky_b / 255.0))
    im = Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.45)

    im_arr = np.asarray(im).astype(np.float32)
    orig_r = np.hypot(xx - sx, yy - sy)
    orig_boost = np.exp(-((orig_r / 6.5) ** 2))
    im_arr[:, :, 0] = np.clip(im_arr[:, :, 0] + orig_boost * 88.0, 0, 255)
    im_arr[:, :, 1] = np.clip(im_arr[:, :, 1] + orig_boost * 26.0, 0, 255)
    im_arr[:, :, 2] = np.clip(im_arr[:, :, 2] + orig_boost * 14.0, 0, 255)
    im = Image.fromarray(im_arr.astype(np.uint8))

    cw_cut, ch_cut = cutout_raw.size
    gcx, gcy = cw_cut // 2 + 6, ch_cut // 2 + 5
    cut_rot = cutout_raw.rotate(-28.0, resample=Image.Resampling.BICUBIC, expand=False, center=(gcx, gcy))
    ghalf = 32
    zoom_d = 340
    gal_patch = cut_rot.crop((gcx - ghalf, gcy - ghalf, gcx + ghalf, gcy + ghalf)).resize(
        (zoom_d, zoom_d), Image.Resampling.BICUBIC
    )
    gp = np.asarray(gal_patch).astype(np.float32) / 255.0
    gp_clean = np.power(np.clip((gp - 0.022) / 0.978, 0.0, 1.0), 0.68)
    ly, lx = np.mgrid[0:zoom_d, 0:zoom_d]
    lr = np.hypot(lx - zoom_d * 0.5, ly - zoom_d * 0.5)
    center_focus = 0.45 + 0.55 / (1.0 + np.exp((lr - 82.0) / 16.0))
    gp_clean = gp_clean * center_focus[..., None]

    loupe_arr = np.zeros((zoom_d, zoom_d, 3), dtype=np.float32)
    loupe_bg = np.array([14.0, 18.0, 54.0], dtype=np.float32)[None, None, :]
    sig_r = np.clip(gp_clean[:, :, 0] * 2.25, 0.0, 1.0)
    sig_g = np.clip(gp_clean[:, :, 1] * 1.24, 0.0, 1.0)
    sig_b = np.clip(gp_clean[:, :, 2] * 0.88, 0.0, 1.0)
    loupe_arr[:, :, 0] = 255.0 * (1.0 - (1.0 - sig_r) * (1.0 - loupe_bg[:, :, 0] / 255.0))
    loupe_arr[:, :, 1] = 255.0 * (1.0 - (1.0 - sig_g) * (1.0 - loupe_bg[:, :, 1] / 255.0))
    loupe_arr[:, :, 2] = 255.0 * (1.0 - (1.0 - sig_b) * (1.0 - loupe_bg[:, :, 2] / 255.0))
    gal_loupe = Image.fromarray(np.clip(loupe_arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    gal_loupe = ImageEnhance.Contrast(gal_loupe).enhance(1.25)
    gal_loupe = ImageEnhance.Color(gal_loupe).enhance(1.34)

    zx, zy = 895, 406
    zmask = Image.new("L", (zoom_d, zoom_d), 0)
    ImageDraw.Draw(zmask).ellipse((4, 4, zoom_d - 5, zoom_d - 5), fill=255)
    im.paste(gal_loupe, (zx - zoom_d // 2, zy - zoom_d // 2), zmask)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    zr = zoom_d // 2
    od.ellipse((zx - zr - 6, zy - zr - 6, zx + zr + 6, zy + zr + 6), outline=(0, 0, 0, 242), width=18)
    od.ellipse((zx - zr, zy - zr, zx + zr, zy + zr), outline=(255, 230, 0, 255), width=10)

    sr = 34
    od.ellipse((sx - sr - 3, sy - sr - 3, sx + sr + 3, sy + sr + 3), outline=(0, 0, 0, 240), width=13)
    od.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), outline=(255, 230, 0, 255), width=7)

    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw_arrow(
        im,
        (sx + sr + 10, sy - 3),
        (zx - zr - 16, zy + 6),
        color=WHITE,
        shaft_w=15,
        head_len=42.0,
        head_half=24.0,
    )

    im = ImageEnhance.Color(im).enhance(1.12)
    bbox = draw_top_band(im, ["300", "MILLION", "YEARS"], "300", tracking=-4, space_scale=0.78, max_w_frac=0.93)
    out = out_dir / "ziKBPJ6FY0U_B_v06.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "ziKBPJ6FY0U",
        "ledger_id": "T039",
        "prior_draft_file": "ziKBPJ6FY0U_B_v05.jpg",
        "film": "004_JWST-Discoveries-That-Change-Everything",
        "live_title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "proposed_title_b": "James Webb Telescope: The Galaxies That Shouldn't Exist Yet",
        "reserve_title_b": "Why Did JWST Find Galaxies That Shouldn't Exist Yet?",
        "hook": "300 MILLION YEARS",
        "yellow": "300",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "origin_circle_px": [sx, sy, sr],
        "loupe_px": [zx, zy, zoom_d // 2],
        "sources": [
            "NASA/ESA/CSA/STScI JADES-GS-z14-0 NIRCam deep field & pullout (STScI-01HZ083EXXCJNE64ERAH2ER2FM / STScI-01HZ08HBSZYHDA52NPPB1BP4SR, spectroscopically confirmed z=14.32 galaxy ~290-300 Myr after the Big Bang, public domain)",
        ],
        "script_verification": "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md Scene 04 line 143: 'Some of the galaxies Webb confirmed are luminous when the universe was only about three hundred million years old.'",
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plates", type=Path, default=DEFAULT_PLATES)
    ap.add_argument("--live", type=Path, default=DEFAULT_LIVE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    out_dir: Path = args.out
    live_out = out_dir / "live"
    out_dir.mkdir(parents=True, exist_ok=True)
    live_out.mkdir(parents=True, exist_ok=True)

    rows = [
        build_compilation(args.plates, out_dir),
        build_fermi(args.plates, out_dir),
        build_jwst(args.plates, out_dir),
    ]
    for r in rows:
        assert r["bytes"] < 2_000_000, f"{r['abs_file']} >= 2MB"
        assert not r["score"]["fails"], f"Score fail on {r['abs_file']}: {r['score']}"
        src_live = args.live / f"{r['video']}.jpg"
        if src_live.exists():
            dst_live = live_out / f"{r['video']}.jpg"
            dst_live.write_bytes(src_live.read_bytes())

    preview_out = out_dir / "THUMB_PREVIEW_SCORE_SHEET.jpg"
    cmd = [
        sys.executable,
        str(SYS_TOOLS / "thumb_preview.py"),
        "long",
        *[r["abs_file"] for r in rows],
        "--out",
        str(preview_out),
        "--score",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(proc.stdout.strip())

    sheet = Image.new("RGB", (1120, 1060), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_PATH, 18)
    for i, r in enumerate(rows):
        y = 20 + i * 342
        d.text((20, y), f"{r['video']} — Live A vs Rebuilt B ({r['hook']})", font=f, fill="black")
        for j, p in enumerate([live_out / f"{r['video']}.jpg", Path(r["abs_file"])]):
            if p.exists():
                im = Image.open(p).convert("RGB")
                p168 = im.resize((168, 94), Image.Resampling.LANCZOS)
                ImageDraw.Draw(p168).rectangle((132, 76, 164, 90), fill=(0, 0, 0))
                sheet.paste(p168, (20 + j * 545, y + 34))
                sheet.paste(im.resize((352, 198), Image.Resampling.LANCZOS), (20 + j * 545, y + 138))
    phone_sheet = out_dir / "PHONE_SHEET_v03.jpg"
    sheet.save(phone_sheet, quality=95)

    clean_rows = []
    for r in rows:
        cr = dict(r)
        cr.pop("abs_file", None)
        clean_rows.append(cr)

    used_plate_names = (
        "PIA08329.tif",
        "PIA08329.jpg",
        "PIA12348.jpg",
        "PIA26716.jpg",
        "JADES_GS_z14_0_field.jpg",
        "JADES_GS_z14_0_cutout.png",
    )
    manifest = {
        "job": "J2983",
        "ref_jobs": ["J2834", "J2843", "J2844"],
        "date": "2026-11-17",
        "maker": "macbook",
        "status": "proposed; rebuilt per packaging panel DECISION.md (J2843), awaiting Chief PASS (J2844) before Studio arming (J2845-J2847)",
        "builder": "00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2834.py",
        "panel_decision": "05_Analytics/tests/panels/owb-j2834-weekly-2026-11-14/DECISION.md",
        "inputs": [
            {"name": p.name, "sha256": sha256(p)}
            for p in sorted(args.plates.iterdir())
            if p.is_file() and p.name in used_plate_names
        ],
        "phone_sheet": str(phone_sheet),
        "phone_sheet_sha256": sha256(phone_sheet),
        "preview_score_sheet": str(preview_out),
        "preview_score_sheet_sha256": sha256(preview_out),
        "gate_stdout": proc.stdout.strip(),
        "designs": clean_rows,
    }
    (out_dir / "DESIGN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
