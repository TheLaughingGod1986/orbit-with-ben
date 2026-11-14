#!/usr/bin/env python3
"""J2834: reproducible weekly thumbnail builder for Orbit With Ben (2026-11-14).
Builds Test & Compare B challengers for the 3 weakest untested public longs:
  - m09jUdwC5hk (How Long Will Anything in Space Last?) -> ALL STARS FADE
  - Mo93x0fxB1Q (Why Haven't We Found Aliens Yet? The Fermi Paradox Explained) -> ZERO SIGNALS
  - ziKBPJ6FY0U (JWST Found Galaxies That Shouldn't Exist Yet) -> 300 MILLION YEARS
Uses verified public-domain NASA/ESA/CSA/STScI photographs only (zero code-drawn cartoon
silhouettes, zero false planetary scale per J2456/J2701). £0 spend; no Studio writes.
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
DEFAULT_OUT = Path.home() / "_desk/j2834/designs_v02"
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
    top_lift = np.exp(-((yy / 220.0) ** 2)) * 0.22
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for k in range(3):
        arr[:, :, k] = base_rgb[k] + glow_rgb[k] * g + glow_rgb[k] * top_lift
    arr += rng.normal(0, 1.0, (H, W, 1))
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(95):
        sx = int(rng.integers(20, W - 20))
        sy = int(rng.integers(BAND_H + 6, H - 20))
        sv = int(rng.integers(110, 225))
        r = 1 if rng.random() < 0.82 else 2
        d.ellipse((sx, sy, sx + r, sy + r), fill=(sv, sv, min(255, sv + 30)))
    return im


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
    b_tip = (p1[0] + ux * 6, p1[1] + uy * 6)
    b_base_x, b_base_y = bx - ux * 4, by - uy * 4
    d.line((p0[0], p0[1], bx, by), fill=BLACK, width=shaft_w + 10)
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


def draw_top_band(im: Image.Image, words: list[str], yellow_word: str) -> list[int]:
    arr = np.asarray(im).astype(np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    alpha = np.clip(1.0 - yy / (BAND_H + 34.0), 0.0, 1.0) ** 1.35 * 0.84
    band_rgb = np.array([18.0, 26.0, 68.0], dtype=np.float32)[None, None, :]
    arr = arr * (1.0 - alpha) + band_rgb * alpha
    im.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))

    d = ImageDraw.Draw(im)
    text = " ".join(words)
    size, stroke = 112, 8
    while size > 62:
        font = ImageFont.truetype(FONT_PATH, size)
        bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bb[2] - bb[0] <= W * 0.91 and bb[3] - bb[1] <= BAND_H - 22:
            break
        size -= 3
    space = d.textbbox((0, 0), " ", font=font)[2]
    widths = [d.textbbox((0, 0), w, font=font, stroke_width=stroke)[2] for w in words]
    total_w = sum(widths) + space * (len(words) - 1)
    x = (W - total_w) // 2
    top_bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    y = (BAND_H - (top_bb[3] - top_bb[1])) // 2 - top_bb[1] + 4
    ink_boxes = []
    for w, ww in zip(words, widths):
        fill = YELLOW if w == yellow_word else WHITE
        d.text((x + 4, y + 5), w, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        d.text((x, y), w, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
        ink_boxes.append(d.textbbox((x, y), w, font=font, stroke_width=stroke))
        x += ww + space
    return [
        min(b[0] for b in ink_boxes),
        min(b[1] for b in ink_boxes),
        max(b[2] for b in ink_boxes),
        max(b[3] for b in ink_boxes),
    ]


def build_compilation(plates: Path, out_dir: Path) -> dict:
    """m09jUdwC5hk — How Long Will Anything in Space Last? -> ALL STARS FADE.
    Full-frame real NASA Spitzer/GALEX Helix Nebula (PIA09178: dying Sun-like star shedding
    its outer layers around a glowing white-dwarf core), clean of false-scale planets.
    """
    im = starfield_bg(19, (18, 28, 68), (24, 120, 165), gx=660.0, gy=435.0, gr=580.0)

    neb_raw = Image.open(plates / "PIA09178.jpg").convert("RGB")
    rw, rh = neb_raw.size
    crop = neb_raw.crop((int(rw * 0.04), int(rh * 0.06), int(rw * 0.96), int(rh * 0.94)))
    neb_w, neb_h = 1140, 610
    neb = crop.resize((neb_w, neb_h), Image.Resampling.LANCZOS)
    neb = ImageEnhance.Contrast(neb).enhance(1.34)
    neb = ImageEnhance.Color(neb).enhance(1.52)
    n_arr = np.asarray(neb).astype(np.float32) / 255.0
    # Smoothly suppress near-zero JPEG noise floor before screen-blending onto cosmic indigo starfield
    n_arr = np.clip((n_arr - 0.045) / 0.955, 0.0, 1.0)

    yy, xx = np.mgrid[0:neb_h, 0:neb_w]
    rx = (xx - neb_w * 0.50) / (neb_w * 0.48)
    ry = (yy - neb_h * 0.50) / (neb_h * 0.48)
    ell = np.clip(1.0 - np.sqrt(rx**2 + ry**2), 0.0, 1.0)
    w_mask = (np.power(ell, 0.55))[..., None]

    px0, py0 = (W - neb_w) // 2 + 20, 118
    bg_arr = np.asarray(im).astype(np.float32) / 255.0
    sub = bg_arr[py0 : py0 + neb_h, px0 : px0 + neb_w]
    sh, sw = sub.shape[:2]
    blended = 1.0 - (1.0 - sub) * (1.0 - n_arr[:sh, :sw] * w_mask[:sh, :sw] * 1.12)
    bg_arr[py0 : py0 + sh, px0 : px0 + sw] = np.clip(blended, 0.0, 1.0)
    im = Image.fromarray((bg_arr * 255.0).astype(np.uint8))

    # Single optional discovery pointer arrow (§2.B.4) from dark left space to the tiny white-dwarf remnant at the core
    draw_arrow(im, (255, 495), (618, 434), color=WHITE, shaft_w=14, head_len=42.0, head_half=24.0)

    im = ImageEnhance.Color(im).enhance(1.12)
    bbox = draw_top_band(im, ["ALL", "STARS", "FADE"], "FADE")
    out = out_dir / "m09jUdwC5hk_B_v04.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "m09jUdwC5hk",
        "film": "J01_Journey-To-Every-World",
        "live_title": "How Long Will Anything in Space Last?",
        "proposed_title_b": "How Long Will Everything in Space Last? (10 Trillion Years)",
        "hook": "ALL STARS FADE",
        "yellow": "FADE",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA/JPL-Caltech PIA09178 (Spitzer/GALEX Helix Nebula dying Sun-like star & white-dwarf core, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_fermi(plates: Path, out_dir: Path) -> dict:
    """Mo93x0fxB1Q — Why Haven't We Found Aliens Yet? The Fermi Paradox Explained -> ZERO SIGNALS.
    Uses two real NASA photographs: Great Observatories Milky Way Galactic Centre (PIA12348) +
    real NASA Deep Space Network 70-m radio telescope dish (PIA26716) aimed at the galactic core.
    """
    mw_raw = Image.open(plates / "PIA12348.jpg").convert("RGB")
    mw = mw_raw.resize((W, H - 70), Image.Resampling.LANCZOS)
    mw = ImageEnhance.Contrast(mw).enhance(1.25)
    mw = ImageEnhance.Color(mw).enhance(1.42)

    im = starfield_bg(23, (18, 24, 64), (90, 52, 138), gx=810.0, gy=420.0, gr=560.0)
    im.paste(mw, (0, 70))
    arr = np.asarray(im).astype(np.float32)
    arr[:, :, 0] = np.maximum(arr[:, :, 0], 18.0)
    arr[:, :, 1] = np.maximum(arr[:, :, 1], 22.0)
    arr[:, :, 2] = np.maximum(arr[:, :, 2], 58.0)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    # Extract the real NASA DSN 70-m radio antenna (PIA26716) from its pure-black night sky
    dsn_raw = Image.open(plates / "PIA26716.jpg").convert("RGB")
    dw, dh = dsn_raw.size
    dsn_crop = dsn_raw.crop((0, int(dh * 0.36), dw, dh))
    # Rotate -24 deg (clockwise) so the 70m dish tilts toward the upper-right Milky Way Galactic Centre
    dsn_rgba = dsn_crop.convert("RGBA")
    d_arr = np.asarray(dsn_crop).astype(np.float32)
    lum = 0.299 * d_arr[:, :, 0] + 0.587 * d_arr[:, :, 1] + 0.114 * d_arr[:, :, 2]
    # Clean alpha mask separating illuminated white steel dish from black sky (lum <= 18 is sky)
    alpha = np.clip((lum - 18.0) * 6.2, 0.0, 255.0).astype(np.uint8)
    alpha_im = Image.fromarray(alpha).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    # Cool cyan-gold galactic starlight grade on the real antenna so it sits naturally in the scene
    graded = d_arr.copy()
    graded[:, :, 0] = np.clip(graded[:, :, 0] * 0.88 + 14.0, 0, 255)
    graded[:, :, 1] = np.clip(graded[:, :, 1] * 0.96 + 22.0, 0, 255)
    graded[:, :, 2] = np.clip(graded[:, :, 2] * 1.12 + 44.0, 0, 255)
    dsn_rgba = Image.fromarray(graded.astype(np.uint8)).convert("RGBA")
    dsn_rgba.putalpha(alpha_im)
    dsn_rot = dsn_rgba.rotate(-18, resample=Image.Resampling.BICUBIC, expand=True)
    dsn_small = dsn_rot.resize((590, 560), Image.Resampling.LANCZOS)

    # Soft dark drop-shadow behind antenna steel lattice so white struts pop at 168x94
    shadow_alpha = dsn_small.getchannel("A").filter(ImageFilter.GaussianBlur(5))
    shadow = Image.new("RGBA", dsn_small.size, (8, 12, 32, 0))
    shadow.putalpha(shadow_alpha)

    canvas = im.convert("RGBA")
    # Anchor pedestal cleanly below bottom frame edge (y=720) so no bottom photo crop line is visible
    canvas.alpha_composite(shadow, (-44, 246))
    canvas.alpha_composite(dsn_small, (-50, 240))

    # Crisp empty yellow search reticle on the brightest Galactic Centre star cluster
    od = ImageDraw.Draw(canvas)
    cx, cy, rad = 875, 420, 96
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
    im = ImageEnhance.Color(im).enhance(1.12)
    bbox = draw_top_band(im, ["ZERO", "SIGNALS"], "ZERO")
    out = out_dir / "Mo93x0fxB1Q_B_v04.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "Mo93x0fxB1Q",
        "film": "001_Will-We-Ever-Meet-Aliens",
        "live_title": "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
        "proposed_title_b": "Fermi Paradox: Why Haven't We Found Aliens Yet?",
        "hook": "ZERO SIGNALS",
        "yellow": "ZERO",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA/JPL-Caltech/ESA/CXC/STScI PIA12348 (Great Observatories Milky Way Galactic Centre composite, public domain)",
            "NASA/JPL-Caltech PIA26716 (Deep Space Network 70-meter radio antenna photograph, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_jwst(plates: Path, out_dir: Path) -> dict:
    """ziKBPJ6FY0U — JWST Found Galaxies That Shouldn't Exist Yet -> 300 MILLION YEARS.
    Real Webb's First Deep Field (SMACS 0723 NIRCam) + 4.5x magnified loupe on a real
    high-redshift crimson galaxy & gravitational arc. Spoken script number: Scene 04 ('300 million years').
    """
    raw = Image.open(plates / "webb_first_deep_field.jpg").convert("RGB")
    rw, rh = raw.size
    crop = raw.crop((int(rw * 0.05), int(rh * 0.15), int(rw * 0.95), int(rh * 0.74))).resize(
        (W, H), Image.Resampling.LANCZOS
    )
    crop = ImageEnhance.Contrast(crop).enhance(1.30)
    crop = ImageEnhance.Color(crop).enhance(1.68)
    c_arr = np.asarray(crop).astype(np.float32)
    lum = (0.299 * c_arr[:, :, 0] + 0.587 * c_arr[:, :, 1] + 0.114 * c_arr[:, :, 2]) / 255.0
    bg_mix = np.clip(1.0 - lum * 2.6, 0.0, 1.0)
    c_arr[:, :, 0] = c_arr[:, :, 0] + bg_mix * 22.0
    c_arr[:, :, 1] = c_arr[:, :, 1] + bg_mix * 32.0
    c_arr[:, :, 2] = c_arr[:, :, 2] + bg_mix * 86.0
    im = Image.fromarray(np.clip(c_arr, 0, 255).astype(np.uint8))

    # Magnified circular zoom callout of real crimson high-redshift galaxy + gravitational arc
    gx0, gy0, g_half = int(rw * 0.595), int(rh * 0.262), int(rw * 0.052)
    gal_patch = raw.crop((gx0 - g_half, gy0 - g_half, gx0 + g_half, gy0 + g_half)).resize(
        (336, 336), Image.Resampling.LANCZOS
    )
    gal_patch = ImageEnhance.Contrast(gal_patch).enhance(1.42)
    gal_patch = ImageEnhance.Color(gal_patch).enhance(1.90)
    gp = np.asarray(gal_patch).astype(np.float32)
    glum = (0.299 * gp[:, :, 0] + 0.587 * gp[:, :, 1] + 0.114 * gp[:, :, 2]) / 255.0
    gp[:, :, 0] = np.clip(gp[:, :, 0] * 1.28 + (1.0 - glum) * 28.0, 0, 255)
    gp[:, :, 1] = np.clip(gp[:, :, 1] * 1.05 + (1.0 - glum) * 22.0, 0, 255)
    gp[:, :, 2] = np.clip(gp[:, :, 2] * 0.95 + (1.0 - glum) * 72.0, 0, 255)
    gal_patch = Image.fromarray(gp.astype(np.uint8))

    zoom_d = 336
    zx, zy = 890, 405  # bottom edge 573 -> completely clear of bottom-right duration badge (y>600)
    zmask = Image.new("L", (zoom_d, zoom_d), 0)
    ImageDraw.Draw(zmask).ellipse((4, 4, zoom_d - 5, zoom_d - 5), fill=255)
    im.paste(gal_patch, (zx - zoom_d // 2, zy - zoom_d // 2), zmask)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    zr = zoom_d // 2
    od.ellipse((zx - zr - 6, zy - zr - 6, zx + zr + 6, zy + zr + 6), outline=(0, 0, 0, 240), width=17)
    od.ellipse((zx - zr, zy - zr, cx_end := zx + zr, zy + zr), outline=(255, 230, 0, 255), width=10)
    _ = cx_end

    sx, sy, sr = 495, 438, 36
    od.ellipse((sx - sr - 3, sy - sr - 3, sx + sr + 3, sy + sr + 3), outline=(0, 0, 0, 235), width=12)
    od.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), outline=(255, 230, 0, 255), width=6)

    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw_arrow(im, (sx + sr + 10, sy - 4), (zx - zr - 16, zy + 8), color=WHITE, shaft_w=14, head_len=40.0, head_half=23.0)

    im = ImageEnhance.Color(im).enhance(1.12)
    bbox = draw_top_band(im, ["300", "MILLION", "YEARS"], "300")
    out = out_dir / "ziKBPJ6FY0U_B_v05.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "ziKBPJ6FY0U",
        "film": "004_JWST-Discoveries-That-Change-Everything",
        "live_title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "proposed_title_b": "James Webb Telescope: Galaxies 300 Million Years After the Big Bang",
        "hook": "300 MILLION YEARS",
        "yellow": "300",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA/ESA/CSA/STScI webb_first_deep_field (Webb's First Deep Field SMACS 0723 NIRCam, public domain)",
            "4.5x magnified high-redshift crimson galaxy & gravitational arc crop from webb_first_deep_field",
        ],
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
        d.text((20, y), f"{r['video']} — Live A vs Proposed B ({r['hook']})", font=f, fill="black")
        for j, p in enumerate([live_out / f"{r['video']}.jpg", Path(r["abs_file"])]):
            if p.exists():
                im = Image.open(p).convert("RGB")
                p168 = im.resize((168, 94), Image.Resampling.LANCZOS)
                ImageDraw.Draw(p168).rectangle((132, 76, 164, 90), fill=(0, 0, 0))
                sheet.paste(p168, (20 + j * 545, y + 34))
                sheet.paste(im.resize((352, 198), Image.Resampling.LANCZOS), (20 + j * 545, y + 138))
    phone_sheet = out_dir / "PHONE_SHEET_v02.jpg"
    sheet.save(phone_sheet, quality=95)

    clean_rows = []
    for r in rows:
        cr = dict(r)
        cr.pop("abs_file", None)
        clean_rows.append(cr)

    manifest = {
        "job": "J2834",
        "date": "2026-11-14",
        "maker": "macbook-2",
        "status": "proposed; awaiting packaging panel + Chief PASS before Studio arming",
        "builder": "00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2834.py",
        "inputs": [
            {"name": p.name, "sha256": sha256(p)}
            for p in sorted(args.plates.iterdir())
            if p.is_file() and p.name in ("PIA09178.jpg", "PIA12348.jpg", "PIA26716.jpg", "webb_first_deep_field.jpg")
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
