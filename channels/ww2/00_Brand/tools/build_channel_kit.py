#!/usr/bin/env python3
"""Deterministic £0 builder for the WW2 documentary channel kit (J2999).

Builds ready-to-upload YouTube profile pictures (800x800, <4 MB) and banners
(2560x1440, <6 MB, all text & key marks strictly inside YouTube's centered
1546x423 all-devices safe area) for all three verified name options in
`channels/ww2/00_Brand/LAUNCH_PLAN.md`:

  1. Field Order History (@FieldOrderHistory) — Recommended
  2. Gridline History (@GridlineHistory)
  3. Iron & Compass (@IronAndCompass)

Media binaries (.png/.jpg) live on the NAS (`/Volumes/data/studio-live/ww2/00_Brand/Channel-Kit/`)
and are optionally mirrored to the iCloud watch folder (`WW2 UAT/00_Channel-Kit/`),
never committed to git (`channels/ww2/.gitignore`). Small clean vector `.svg` marks
and `ART_MANIFEST.json` live in `channels/ww2/00_Brand/`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import shutil
import subprocess
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

BRAND_DIR = pathlib.Path(__file__).resolve().parents[1]
SVG_DIR = BRAND_DIR / "svg"
KIT_DOC_DIR = BRAND_DIR / "Channel-Kit"

DEFAULT_NAS_DIR = pathlib.Path("/Volumes/data/studio-live/ww2/00_Brand/Channel-Kit")
DEFAULT_ICLOUD_DIR = (
    pathlib.Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/WW2 UAT/00_Channel-Kit"
)

# Official YouTube 2560x1440 banner geometry
BANNER_W, BANNER_H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SAFE_X0 = (BANNER_W - SAFE_W) // 2  # 507
SAFE_X1 = SAFE_X0 + SAFE_W          # 2053
SAFE_Y0 = (BANNER_H - SAFE_H) // 2  # 508
SAFE_Y1 = SAFE_Y0 + SAFE_H          # 931
TABLET_W = 1855
TABLET_X0 = (BANNER_W - TABLET_W) // 2  # 352
TABLET_X1 = TABLET_X0 + TABLET_W        # 2207

AVATAR_SIZE = 800

# House packaging palette (LAUNCH_PLAN.md §3B + RULES.md rule 2)
WHITE = (255, 255, 255)
SIGNAL_YELLOW = (255, 214, 0)     # #FFD600
TACTICAL_RED = (255, 59, 48)      # #FF3B30
KEYLINE_DARK = (11, 14, 20)       # #0B0E14
SLATE_NAVY = (26, 35, 46)         # lifted slate, never crushed black
SILVER_MIST = (224, 229, 235)

FONT_CONDENSED = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_ALT_BOLD = "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"

ARCHIVE_PLATES = {
    "nara_26_g_2517": {
        "filename": "nara_26_g_2517_normandy_supply.jpg",
        "collection": "US Coast Guard / US National Archives (NARA)",
        "archive_id": "26-G-2517",
        "date": "9 June 1944",
        "licence": "US Federal Government Public Domain (17 U.S.C. § 105)",
        "credit_line": "US Coast Guard / NARA 26-G-2517 (Public Domain)",
        "subject": "Allied LST landing ships, barrage balloons and supply trucks unloading at low tide on Omaha Beach, Normandy",
        "wikimedia_title": "File:Normandy Invasion, June 1944.jpg",
    },
    "iwm_bu1024": {
        "filename": "iwm_bu1024_mulberry_arromanches.jpg",
        "collection": "UK War Office / Imperial War Museums (No. 5 Army Film & Photographic Unit, Sgt Harrison)",
        "archive_id": "IWM BU 1024",
        "date": "September 1944",
        "licence": "UK Crown Copyright Expired (created 1944, >50 years old under CDPA 1988 s.163; Public Domain)",
        "credit_line": "UK War Office / Imperial War Museums BU 1024 (Crown Copyright Expired / Public Domain)",
        "subject": "Aerial reconnaissance view of Mulberry B artificial harbour, Whale floating roadways and Spud pierheads off Arromanches, Normandy",
        "wikimedia_title": "File:The Mulberry artificial harbour off Arromanches in Normandy, September 1944. BU1024.jpg",
    },
    "nara_80_g_266487": {
        "filename": "nara_80_g_266487_uss_ahrens_from_bogue.jpg",
        "collection": "US Navy / Naval History and Heritage Command / NARA (Photographed by F.B. Larrick, USN, from USS Bogue CVE-9)",
        "archive_id": "80-G-266487",
        "date": "13 May 1944",
        "licence": "US Federal Government Public Domain (17 U.S.C. § 105)",
        "credit_line": "US Navy / NARA 80-G-266487 (Public Domain)",
        "subject": "Destroyer escort USS Ahrens (DE-575) with HF/DF radio direction-finding mast underway in the Atlantic Ocean, seen from escort carrier USS Bogue (CVE-9)",
        "wikimedia_title": "File:USS Ahrens (DE-575) underway in the Atlantic Ocean on 13 May 1944 (80-G-266487).jpg",
    },
}

CHANNEL_OPTIONS = [
    {
        "slug": "field_order_history",
        "recommended": True,
        "name": "Field Order History",
        "handle": "@FieldOrderHistory",
        "monogram": "FO",
        "line1_white": "FIELD ORDER",
        "line1_yellow": "HISTORY",
        "subline": "HOW WW2 WAS ENGINEERED & FOUGHT",
        "coord_tag": "50°20'N 00°37'W  |  ARCHIVE DOCUMENTARIES",
        "plate_key": "nara_26_g_2517",
        # Crop box in normalized [x0, y0, x1, y1] of source 3482x2480 so LSTs, balloon & trucks sit cleanly in right half of safe strip
        "banner_crop": (0.04, 0.08, 1.00, 0.84),
        # Avatar crop focusing on LST US 510 + silver barrage balloon + trucks on beach
        "avatar_crop": (0.64, 0.22, 0.99, 0.72),
        # Tactical callout arrow [from_xy -> to_xy] inside safe strip pointing to right-side hero hardware
        "callout": ((1835, 588), (1735, 648), "OMAHA SUPPLY"),
    },
    {
        "slug": "gridline_history",
        "recommended": False,
        "name": "Gridline History",
        "handle": "@GridlineHistory",
        "monogram": "GH",
        "line1_white": "GRIDLINE",
        "line1_yellow": "HISTORY",
        "subline": "WW2 OPERATIONS  |  MAPS  |  ARCHIVES",
        "coord_tag": "GSGS GRID 40/16  |  ARCHIVE DOCUMENTARIES",
        "plate_key": "iwm_bu1024",
        # Crop Mulberry B Arromanches aerial so floating Whale roadways & Spud pierheads fill right-center of safe strip
        "banner_crop": (0.00, 0.27, 1.00, 0.83),
        "avatar_crop": (0.28, 0.42, 0.82, 0.96),
        "callout": ((1845, 588), (1725, 668), "MULBERRY B"),
    },
    {
        "slug": "iron_and_compass",
        "recommended": False,
        "name": "Iron & Compass",
        "handle": "@IronAndCompass",
        "monogram": "IC",
        "line1_white": "IRON &",
        "line1_yellow": "COMPASS",
        "subline": "NAVAL, AIR & INDUSTRIAL WARFARE",
        "coord_tag": "NORTH ATLANTIC  |  ARCHIVE DOCUMENTARIES",
        "plate_key": "nara_80_g_266487",
        # Shift USS Ahrens cleanly into right half of safe strip so bridge & mast sit clear of COMPASS
        "banner_crop": (-0.36, 0.16, 0.96, 0.96),
        "avatar_crop": (0.08, 0.36, 0.82, 0.98),
        "callout": ((1865, 588), (1685, 640), "HF/DF ESCORT"),
    },
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def image_stats(img: Image.Image) -> Dict[str, float]:
    gray = np.asarray(img.convert("L"), dtype=np.float32)
    return {
        "mean_luma": round(float(gray.mean()), 2),
        "p95_luma": round(float(np.percentile(gray, 95)), 2),
        "near_black_pct": round(float((gray < 28).mean() * 100.0), 2),
    }


def grade_wartime_plate(img: Image.Image, lift: float = 1.08, contrast: float = 1.24) -> Image.Image:
    """Bright, high-contrast silver-warm documentary tonal grade (never dark/crushed)."""
    gray = ImageOps.autocontrast(img.convert("L"), cutoff=0.6)
    arr = np.asarray(gray, dtype=np.float32) / 255.0
    # Lift deep shadows so near-black stays well below 25%, keep crisp highlights
    arr = 0.08 + 0.90 * np.power(np.clip(arr, 0.0, 1.0), 0.90)
    # Subtle warm archival silver-sepia split-tone (warm highlights, cool-slate mid-shadows)
    r = np.clip(arr * 255.0 * 1.02 + 3.0, 0, 255)
    g = np.clip(arr * 255.0 * 1.00 + 2.0, 0, 255)
    b = np.clip(arr * 255.0 * 0.96 + 4.0, 0, 255)
    rgb = np.stack([r, g, b], axis=-1).astype(np.uint8)
    out = Image.fromarray(rgb, mode="RGB")
    out = ImageEnhance.Contrast(out).enhance(contrast)
    out = ImageEnhance.Brightness(out).enhance(lift)
    out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=3))
    return out


def crop_with_horizon_extend(img: Image.Image, norm_box: Tuple[float, float, float, float], target_size: Tuple[int, int]) -> Image.Image:
    """Crop normalized box; if x0 < 0, seamlessly extend left sea/sky horizon so ship sits in right safe area."""
    w, h = img.size
    x0_f, y0_f, x1_f, y1_f = norm_box
    y0 = max(0, int(round(y0_f * h)))
    y1 = min(h, int(round(y1_f * h)))
    x1 = min(w, int(round(x1_f * w)))
    if x0_f >= 0:
        x0 = max(0, int(round(x0_f * w)))
        cropped = img.crop((x0, y0, x1, y1))
    else:
        pad_px = int(round(-x0_f * w))
        sub = img.crop((0, y0, x1, y1))
        # Build natural sea/sky extension from pure left ocean slice (6% width = 230px, 100% open ocean + sky, zero ship bow)
        strip_w = min(240, max(120, int(sub.width * 0.06)))
        left_strip = sub.crop((0, 0, strip_w, sub.height))
        mir = ImageOps.mirror(left_strip)
        ext_img = Image.new("RGB", (pad_px, sub.height))
        # Tile alternating mirror/normal ocean strips with wide feathered blends so real wave grain continues naturally
        cur_x = pad_px
        flip = True
        while cur_x > 0:
            tile = mir if flip else left_strip
            paste_x = cur_x - strip_w
            ext_img.paste(tile, (paste_x, 0))
            cur_x -= strip_w
            flip = not flip
        cropped = Image.new("RGB", (pad_px + sub.width, sub.height))
        cropped.paste(ext_img, (0, 0))
        cropped.paste(sub, (pad_px, 0))
        # Smooth seam blend across join
        seam_band = cropped.crop((max(0, pad_px - 36), 0, min(cropped.width, pad_px + 36), sub.height))
        seam_blur = seam_band.filter(ImageFilter.GaussianBlur(radius=6.0))
        mask = Image.new("L", seam_band.size, 0)
        md = ImageDraw.Draw(mask)
        bw_s = seam_band.width
        for sx_i in range(bw_s):
            a = int(190 * math.sin(math.pi * sx_i / max(1, bw_s - 1)))
            md.line([(sx_i, 0), (sx_i, sub.height)], fill=a)
        cropped.paste(seam_blur, (max(0, pad_px - 36), 0), mask)

    # Fit exact aspect ratio of target_size via center-preserve crop, then Lanczos resize
    tw, th = target_size
    target_ratio = tw / th
    cw, ch = cropped.size
    cur_ratio = cw / ch
    if cur_ratio > target_ratio:
        new_w = int(round(ch * target_ratio))
        off_x = (cw - new_w) // 2
        cropped = cropped.crop((off_x, 0, off_x + new_w, ch))
    elif cur_ratio < target_ratio:
        new_h = int(round(cw / target_ratio))
        off_y = (ch - new_h) // 2
        cropped = cropped.crop((0, off_y, cw, off_y + new_h))
    return cropped.resize((tw, th), Image.Resampling.LANCZOS)


def draw_stroked_text(
    canvas: Image.Image,
    pos: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int],
    stroke_width: int = 6,
    stroke_fill: Tuple[int, int, int] = KEYLINE_DARK,
    shadow_offset: Tuple[int, int] = (0, 5),
    shadow_blur: int = 8,
) -> Tuple[int, int, int, int]:
    """Render crisp stroked text with soft drop shadow; returns bounding box on canvas."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(layer)
    sx, sy = pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]
    sh_draw.text(
        (sx, sy),
        text,
        font=font,
        fill=(0, 0, 0, 175),
        stroke_width=stroke_width,
        stroke_fill=(0, 0, 0, 175),
    )
    if shadow_blur > 0:
        layer = layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))

    fg_draw = ImageDraw.Draw(layer)
    fg_draw.text(
        pos,
        text,
        font=font,
        fill=(*fill, 255),
        stroke_width=stroke_width,
        stroke_fill=(*stroke_fill, 255),
    )
    bbox = fg_draw.textbbox(pos, text, font=font, stroke_width=stroke_width)
    out = Image.alpha_composite(canvas.convert("RGBA"), layer)
    canvas.paste(out.convert("RGB"))
    return bbox


def build_banner(opt: dict, src_img: Image.Image) -> Tuple[Image.Image, Dict[str, object]]:
    base = crop_with_horizon_extend(src_img, opt["banner_crop"], (BANNER_W, BANNER_H))
    graded = grade_wartime_plate(base, lift=1.08, contrast=1.22)

    rgba = graded.convert("RGBA")
    overlay = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # 1. Subtle cartographic gridlines across outer TV frame (low opacity so archive photo shines)
    grid_step = 160
    for gx in range(grid_step, BANNER_W, grid_step):
        odraw.line([(gx, 0), (gx, BANNER_H)], fill=(255, 255, 255, 22), width=1)
    for gy in range(grid_step, BANNER_H, grid_step):
        odraw.line([(0, gy), (BANNER_W, gy)], fill=(255, 255, 255, 22), width=1)

    # 2. Translucent left-safe-zone readability gradient ONLY behind typography (x=480..1460, y=508..931)
    #    Keeps overall image bright while guaranteeing 100% contrast on white + yellow type.
    grad = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    g_arr = np.zeros((BANNER_H, BANNER_W, 4), dtype=np.uint8)
    xs = np.arange(BANNER_W, dtype=np.float32)
    ys = np.arange(BANNER_H, dtype=np.float32)
    # Smooth horizontal falloff from x=500..1490, vertical focus y=500..940
    hx = np.clip(1.0 - (xs - 520.0) / 960.0, 0.0, 1.0)
    hx = hx * hx * (3.0 - 2.0 * hx)
    # Taper left of x=520 softly too so TV view has no hard rectangle
    left_taper = np.clip((xs - 180.0) / 340.0, 0.35, 1.0)
    hx = hx * left_taper
    vy = np.exp(-0.5 * ((ys - 720.0) / 235.0) ** 2)
    alpha_map = (142.0 * np.outer(vy, hx)).astype(np.uint8)
    g_arr[:, :, 0] = SLATE_NAVY[0]
    g_arr[:, :, 1] = SLATE_NAVY[1]
    g_arr[:, :, 2] = SLATE_NAVY[2]
    g_arr[:, :, 3] = alpha_map
    grad = Image.fromarray(g_arr, mode="RGBA")
    rgba = Image.alpha_composite(rgba, grad)
    rgba = Image.alpha_composite(rgba, overlay)

    # 3. Tactical red accent bar & coordinate header strictly inside safe area (x >= 565, y >= 565)
    ui = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    udraw = ImageDraw.Draw(ui)
    left_x = 572  # 65 px inside SAFE_X0=507
    top_bar_y = 574  # 66 px inside SAFE_Y0=508

    # Vertical tactical red bar spanning title block
    udraw.rectangle([left_x - 18, top_bar_y + 4, left_x - 10, 858], fill=(*TACTICAL_RED, 255))

    # Small technical coordinate stamp above title (dynamic width so zero text clips)
    font_coord = load_font(FONT_ALT_BOLD, 22)
    cb = udraw.textbbox((0, 0), opt["coord_tag"], font=font_coord)
    coord_w = cb[2] - cb[0] + 28
    udraw.rounded_rectangle([left_x, top_bar_y, left_x + coord_w, top_bar_y + 34], radius=4, fill=(14, 19, 27, 200))
    udraw.text((left_x + 14, top_bar_y + 5), opt["coord_tag"], font=font_coord, fill=(*SILVER_MIST, 245))

    # One crisp #FF3B30 tactical callout arrow inside right half of safe area pointing to hero wartime hardware
    (cx0, cy0), (cx1, cy1), c_label = opt["callout"]
    font_call = load_font(FONT_ALT_BOLD, 22)
    cl_bbox = udraw.textbbox((0, 0), c_label, font=font_call)
    cl_w = cl_bbox[2] - cl_bbox[0] + 24
    # Place badge centered on cx0, strictly inside SAFE_X1 - 24
    bx0 = min(cx0 - cl_w // 2, SAFE_X1 - 28 - cl_w)
    bx1 = bx0 + cl_w
    udraw.rounded_rectangle([bx0, cy0 - 18, bx1, cy0 + 18], radius=4, fill=(14, 19, 27, 220), outline=(*TACTICAL_RED, 255), width=2)
    udraw.text((bx0 + 12, cy0 - 13), c_label, font=font_call, fill=(255, 255, 255, 255))
    line_start_x = bx0 if cx1 < bx0 else (bx1 if cx1 > bx1 else (bx0 + bx1) // 2)
    line_start_y = cy0 + 18 if cy1 > cy0 + 18 else cy0
    udraw.line([(line_start_x, line_start_y), (cx1, cy1)], fill=(*TACTICAL_RED, 255), width=4)
    # Arrowhead at (cx1, cy1)
    ang = math.atan2(cy1 - line_start_y, cx1 - line_start_x)
    ah = 13
    p1 = (cx1 - ah * math.cos(ang - 0.5), cy1 - ah * math.sin(ang - 0.5))
    p2 = (cx1 - ah * math.cos(ang + 0.5), cy1 - ah * math.sin(ang + 0.5))
    udraw.polygon([(cx1, cy1), p1, p2], fill=(*TACTICAL_RED, 255))
    # Target reticle ring at tip
    udraw.ellipse([cx1 - 16, cy1 - 16, cx1 + 16, cy1 + 16], outline=(*TACTICAL_RED, 220), width=2)

    rgba = Image.alpha_composite(rgba, ui)
    canvas = rgba.convert("RGB")

    # 4. Main channel title lockup (White + Signal Yellow, DIN Condensed Bold, strictly inside 1546x423 safe area)
    font_title = load_font(FONT_CONDENSED, 134)
    title_y = 626
    b_white = draw_stroked_text(
        canvas,
        (left_x, title_y),
        opt["line1_white"],
        font_title,
        WHITE,
        stroke_width=7,
    )
    yellow_x = b_white[2] + 22
    b_yellow = draw_stroked_text(
        canvas,
        (yellow_x, title_y),
        opt["line1_yellow"],
        font_title,
        SIGNAL_YELLOW,
        stroke_width=7,
    )

    # 5. Crisp 4-5 word subline below title + handle pill, strictly above SAFE_Y1=931
    font_sub = load_font(FONT_ALT_BOLD, 34)
    sub_y = 778
    b_sub = draw_stroked_text(
        canvas,
        (left_x + 2, sub_y),
        opt["subline"],
        font_sub,
        WHITE,
        stroke_width=4,
        shadow_offset=(0, 3),
        shadow_blur=5,
    )

    # Handle tag on same baseline or clean lower line at y=832..868 (well inside SAFE_Y1=931)
    font_handle = load_font(FONT_ALT_BOLD, 25)
    h_layer = Image.new("RGBA", (BANNER_W, BANNER_H), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(h_layer)
    hb = h_draw.textbbox((0, 0), opt["handle"], font=font_handle)
    hw = hb[2] - hb[0] + 26
    hy = 830
    h_draw.rounded_rectangle([left_x + 2, hy, left_x + 2 + hw, hy + 36], radius=5, fill=(14, 19, 27, 215), outline=(*SIGNAL_YELLOW, 230), width=2)
    h_draw.text((left_x + 15, hy + 5), opt["handle"], font=font_handle, fill=(*SIGNAL_YELLOW, 255))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), h_layer).convert("RGB")

    # Compute overall safe-area union bbox of all text + tactical callout elements
    union_x0 = min(left_x - 18, b_white[0], bx0)
    union_y0 = min(top_bar_y, b_white[1], cy0 - 18)
    union_x1 = max(b_yellow[2], b_sub[2], bx1, cx1 + 16, left_x + coord_w)
    union_y1 = max(hy + 36, b_sub[3], cy1 + 16)

    assert union_x0 >= SAFE_X0 + 20, f"Safe X0 violated: {union_x0} < {SAFE_X0}"
    assert union_x1 <= SAFE_X1 - 20, f"Safe X1 violated: {union_x1} > {SAFE_X1}"
    assert union_y0 >= SAFE_Y0 + 20, f"Safe Y0 violated: {union_y0} < {SAFE_Y0}"
    assert union_y1 <= SAFE_Y1 - 20, f"Safe Y1 violated: {union_y1} > {SAFE_Y1}"

    meta = {
        "safe_area_bounds": [SAFE_X0, SAFE_Y0, SAFE_X1, SAFE_Y1],
        "content_bounds": [int(union_x0), int(union_y0), int(union_x1), int(union_y1)],
        "margins_inside_safe_px": {
            "left": int(union_x0 - SAFE_X0),
            "top": int(union_y0 - SAFE_Y0),
            "right": int(SAFE_X1 - union_x1),
            "bottom": int(SAFE_Y1 - union_y1),
        },
        **image_stats(canvas),
    }
    return canvas, meta


def build_photo_avatar(opt: dict, src_img: Image.Image) -> Tuple[Image.Image, Dict[str, object]]:
    """800x800 archive-photo avatar with circular tactical compass bezel & bold monogram."""
    base = crop_with_horizon_extend(src_img, opt["avatar_crop"], (AVATAR_SIZE, AVATAR_SIZE))
    graded = grade_wartime_plate(base, lift=1.10, contrast=1.26)

    rgba = graded.convert("RGBA")
    ui = Image.new("RGBA", (AVATAR_SIZE, AVATAR_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ui)

    cx, cy = AVATAR_SIZE // 2, AVATAR_SIZE // 2

    # Soft bottom-center vignette inside circle so monogram pops at 36x36 px mobile avatar size
    vig = np.zeros((AVATAR_SIZE, AVATAR_SIZE, 4), dtype=np.uint8)
    yy, xx = np.ogrid[:AVATAR_SIZE, :AVATAR_SIZE]
    dist_bottom = np.sqrt(((xx - cx) / 290.0) ** 2 + ((yy - 565.0) / 210.0) ** 2)
    v_alpha = np.clip((1.0 - dist_bottom) * 165.0, 0, 165).astype(np.uint8)
    vig[:, :, 0] = SLATE_NAVY[0]
    vig[:, :, 1] = SLATE_NAVY[1]
    vig[:, :, 2] = SLATE_NAVY[2]
    vig[:, :, 3] = v_alpha
    rgba = Image.alpha_composite(rgba, Image.fromarray(vig, mode="RGBA"))

    # Tactical circular compass ring inside YouTube's circular avatar crop (radius 366 inside r=400)
    r_outer = 368
    r_inner = 348
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(14, 19, 27, 225), width=14)
    draw.ellipse([cx - r_outer + 3, cy - r_outer + 3, cx + r_outer - 3, cy + r_outer - 3], outline=(*SIGNAL_YELLOW, 245), width=5)

    # Compass degree ticks every 30 deg
    for deg in range(0, 360, 30):
        rad = math.radians(deg - 90)
        r0 = r_inner - (12 if deg % 90 == 0 else 4)
        r1 = r_outer - 6
        x0, y0 = cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)
        x1, y1 = cx + r1 * math.cos(rad), cy + r1 * math.sin(rad)
        col = TACTICAL_RED if deg == 0 else WHITE
        w = 6 if deg % 90 == 0 else 3
        draw.line([(x0, y0), (x1, y1)], fill=(*col, 235), width=w)

    # Crisp red north-bearing triangle at 12 o'clock (top of circle safe zone)
    draw.polygon([(cx, 44), (cx - 18, 78), (cx + 18, 78)], fill=(*TACTICAL_RED, 255), outline=(*KEYLINE_DARK, 255))

    rgba = Image.alpha_composite(rgba, ui)
    canvas = rgba.convert("RGB")

    # Bold condensed 2-letter monogram positioned at lower-center so top 55% showcases the wartime photograph
    # while 36x36 px mobile circle still reads instantly.
    mono = opt["monogram"]
    font_mono = load_font(FONT_CONDENSED, 290)
    tmp_draw = ImageDraw.Draw(canvas)
    c0, c1 = mono[0], mono[1]
    b0 = tmp_draw.textbbox((0, 0), c0, font=font_mono, stroke_width=11)
    b1 = tmp_draw.textbbox((0, 0), c1, font=font_mono, stroke_width=11)
    w0 = b0[2] - b0[0]
    w1 = b1[2] - b1[0]
    gap = 10
    total_w = w0 + gap + w1
    start_x = cx - total_w // 2
    mono_y = 408

    draw_stroked_text(canvas, (start_x, mono_y), c0, font_mono, WHITE, stroke_width=11, shadow_offset=(0, 6), shadow_blur=9)
    draw_stroked_text(canvas, (start_x + w0 + gap, mono_y), c1, font_mono, SIGNAL_YELLOW, stroke_width=11, shadow_offset=(0, 6), shadow_blur=9)

    return canvas, image_stats(canvas)


def build_drawn_avatar_and_svg(opt: dict) -> Tuple[Image.Image, str, Dict[str, object]]:
    """Pure drawn cartographic/compass 800x800 emblem + clean vector SVG source."""
    canvas = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), (34, 45, 58))
    # Bright radial parchment-slate lift in center so mean luma is bright & clean
    yy, xx = np.ogrid[:AVATAR_SIZE, :AVATAR_SIZE]
    cx, cy = AVATAR_SIZE // 2, AVATAR_SIZE // 2
    rr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / 420.0
    lift = np.clip(1.0 - 0.45 * (rr ** 1.4), 0.45, 1.0)
    bg = np.zeros((AVATAR_SIZE, AVATAR_SIZE, 3), dtype=np.uint8)
    bg[:, :, 0] = (58 * lift + 14).astype(np.uint8)
    bg[:, :, 1] = (72 * lift + 18).astype(np.uint8)
    bg[:, :, 2] = (90 * lift + 24).astype(np.uint8)
    canvas = Image.fromarray(bg, mode="RGB")

    rgba = canvas.convert("RGBA")
    ui = Image.new("RGBA", (AVATAR_SIZE, AVATAR_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ui)

    # Ordnance Survey / GSGS tactical gridlines
    for g in range(100, AVATAR_SIZE, 100):
        draw.line([(g, 0), (g, AVATAR_SIZE)], fill=(225, 232, 240, 48), width=2)
        draw.line([(0, g), (AVATAR_SIZE, g)], fill=(225, 232, 240, 48), width=2)

    # Concentric range rings + outer yellow compass bezel
    draw.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], outline=(225, 232, 240, 80), width=3)
    draw.ellipse([cx - 366, cy - 366, cx + 366, cy + 366], outline=(*KEYLINE_DARK, 255), width=16)
    draw.ellipse([cx - 363, cy - 363, cx + 363, cy + 363], outline=(*SIGNAL_YELLOW, 255), width=6)

    for deg in range(0, 360, 15):
        rad = math.radians(deg - 90)
        r0 = 334 if deg % 90 == 0 else (344 if deg % 45 == 0 else 350)
        r1 = 358
        col = TACTICAL_RED if deg == 0 else WHITE
        w = 7 if deg % 90 == 0 else 3
        draw.line([(cx + r0 * math.cos(rad), cy + r0 * math.sin(rad)), (cx + r1 * math.cos(rad), cy + r1 * math.sin(rad))], fill=(*col, 240), width=w)

    draw.polygon([(cx, 42), (cx - 22, 84), (cx + 22, 84)], fill=(*TACTICAL_RED, 255), outline=(*KEYLINE_DARK, 255))

    rgba = Image.alpha_composite(rgba, ui)
    canvas = rgba.convert("RGB")

    mono = opt["monogram"]
    font_mono = load_font(FONT_CONDENSED, 360)
    td = ImageDraw.Draw(canvas)
    c0, c1 = mono[0], mono[1]
    b0 = td.textbbox((0, 0), c0, font=font_mono, stroke_width=12)
    b1 = td.textbbox((0, 0), c1, font=font_mono, stroke_width=12)
    w0, w1 = b0[2] - b0[0], b1[2] - b1[0]
    gap = 12
    sx = cx - (w0 + gap + w1) // 2
    sy = 236
    draw_stroked_text(canvas, (sx, sy), c0, font_mono, WHITE, stroke_width=12, shadow_offset=(0, 7), shadow_blur=10)
    draw_stroked_text(canvas, (sx + w0 + gap, sy), c1, font_mono, SIGNAL_YELLOW, stroke_width=12, shadow_offset=(0, 7), shadow_blur=10)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#485A70"/>
      <stop offset="100%" stop-color="#222D3A"/>
    </radialGradient>
  </defs>
  <rect width="800" height="800" fill="url(#bg)"/>
  <g stroke="#E1E8F0" stroke-opacity="0.20" stroke-width="2">
    <line x1="200" y1="0" x2="200" y2="800"/><line x1="400" y1="0" x2="400" y2="800"/><line x1="600" y1="0" x2="600" y2="800"/>
    <line x1="0" y1="200" x2="800" y2="200"/><line x1="0" y1="400" x2="800" y2="400"/><line x1="0" y1="600" x2="800" y2="600"/>
  </g>
  <circle cx="400" cy="400" r="260" fill="none" stroke="#E1E8F0" stroke-opacity="0.32" stroke-width="3"/>
  <circle cx="400" cy="400" r="363" fill="none" stroke="#0B0E14" stroke-width="16"/>
  <circle cx="400" cy="400" r="363" fill="none" stroke="#FFD600" stroke-width="6"/>
  <polygon points="400,42 378,84 422,84" fill="#FF3B30" stroke="#0B0E14" stroke-width="3"/>
  <text x="392" y="520" text-anchor="end" font-family="DIN Condensed, Impact, Arial Narrow, sans-serif" font-weight="700" font-size="340" fill="#FFFFFF" stroke="#0B0E14" stroke-width="12" paint-order="stroke">{c0}</text>
  <text x="408" y="520" text-anchor="start" font-family="DIN Condensed, Impact, Arial Narrow, sans-serif" font-weight="700" font-size="340" fill="#FFD600" stroke="#0B0E14" stroke-width="12" paint-order="stroke">{c1}</text>
</svg>
"""
    return canvas, svg, image_stats(canvas)


def make_circle_preview(avatar: Image.Image, size: int) -> Image.Image:
    resized = avatar.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (18, 22, 28, 255))
    out.paste(resized, (0, 0), mask)
    return out.convert("RGB")


def build_preview_sheet(rows: List[Tuple[dict, Image.Image, Image.Image, Image.Image]]) -> Image.Image:
    """Verification contact sheet showing TV, Desktop strip, Tablet & Mobile 1546x423 safe guides + 120px/40px circle avatars."""
    sheet_w = 1800
    row_h = 540
    header_h = 80
    sheet = Image.new("RGB", (sheet_w, header_h + row_h * len(rows) + 20), (18, 22, 28))
    draw = ImageDraw.Draw(sheet)
    f_hdr = load_font(FONT_ALT_BOLD, 28)
    f_lbl = load_font(FONT_ALT_BOLD, 20)
    draw.text((32, 24), "WW2 CHANNEL KIT - SAFE-AREA & MOBILE CIRCLE VERIFICATION (J2999)", font=f_hdr, fill=WHITE)

    for idx, (opt, banner, av_photo, av_drawn) in enumerate(rows):
        y0 = header_h + idx * row_h
        tag = "[RECOMMENDED]" if opt["recommended"] else f"ALTERNATIVE {idx}"
        draw.text((32, y0 + 8), f"{tag}: {opt['name']} ({opt['handle']})", font=f_lbl, fill=SIGNAL_YELLOW if opt["recommended"] else SILVER_MIST)

        # Scaled banner with safe-area guides overlaid (width 860 -> height 484)
        bw, bh = 860, 484
        sx, sy = bw / BANNER_W, bh / BANNER_H
        b_prev = banner.resize((bw, bh), Image.Resampling.LANCZOS)
        bd = ImageDraw.Draw(b_prev)
        # Desktop strip (y=508..931)
        bd.rectangle([0, int(SAFE_Y0 * sy), bw - 1, int(SAFE_Y1 * sy)], outline=(120, 190, 255), width=2)
        # Tablet safe area
        bd.rectangle([int(TABLET_X0 * sx), int(SAFE_Y0 * sy), int(TABLET_X1 * sx), int(SAFE_Y1 * sy)], outline=(255, 180, 60), width=2)
        # All-devices / Mobile safe area (1546x423) in bright green
        bd.rectangle([int(SAFE_X0 * sx), int(SAFE_Y0 * sy), int(SAFE_X1 * sx), int(SAFE_Y1 * sy)], outline=(60, 245, 120), width=3)
        sheet.paste(b_prev, (32, y0 + 40))

        # Exact cropped mobile banner view (1546x423 safe box alone, scaled to 470x129)
        mob_crop = banner.crop((SAFE_X0, SAFE_Y0, SAFE_X1, SAFE_Y1)).resize((470, 129), Image.Resampling.LANCZOS)
        draw.text((920, y0 + 40), "Mobile Banner Crop (1546x423 exact):", font=f_lbl, fill=(60, 245, 120))
        sheet.paste(mob_crop, (920, y0 + 70))

        # Photo avatar circle previews: 180px, 88px (channel header), 40px (feed/comment)
        draw.text((920, y0 + 225), "Archive-Photo Avatar (180px / 88px / 40px):", font=f_lbl, fill=WHITE)
        sheet.paste(make_circle_preview(av_photo, 180), (920, y0 + 258))
        sheet.paste(make_circle_preview(av_photo, 88), (1120, y0 + 304))
        sheet.paste(make_circle_preview(av_photo, 40), (1228, y0 + 328))

        # Drawn avatar circle previews: 180px, 88px, 40px
        draw.text((1415, y0 + 225), "Drawn Emblem (180 / 88 / 40):", font=f_lbl, fill=SILVER_MIST)
        sheet.paste(make_circle_preview(av_drawn, 180), (1415, y0 + 258))
        sheet.paste(make_circle_preview(av_drawn, 88), (1615, y0 + 304))
        sheet.paste(make_circle_preview(av_drawn, 40), (1720, y0 + 328))

    return sheet


def save_png_and_jpg(img: Image.Image, stem_path: pathlib.Path, max_bytes: int) -> Dict[str, object]:
    png_path = stem_path.with_suffix(".png")
    jpg_path = stem_path.with_suffix(".jpg")
    img.save(png_path, format="PNG", compress_level=9)
    if png_path.stat().st_size >= max_bytes:
        # Quantize high-grain 2560x1440 banner PNG to 256-colour Floyd-Steinberg dithered palette so PNG is also <6 MB
        q_img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        q_img.save(png_path, format="PNG", optimize=True)
    img.save(jpg_path, format="JPEG", quality=94, subsampling=0, optimize=True)
    png_size = png_path.stat().st_size
    jpg_size = jpg_path.stat().st_size
    assert png_size < max_bytes, f"{png_path.name} exceeds YouTube size cap: {png_size} >= {max_bytes}"
    assert jpg_size < max_bytes, f"{jpg_path.name} exceeds YouTube size cap: {jpg_size} >= {max_bytes}"
    return {
        "png": png_path.name,
        "png_bytes": png_size,
        "png_under_youtube_limit": png_size < max_bytes,
        "png_sha256": sha256_file(png_path),
        "jpg": jpg_path.name,
        "jpg_bytes": jpg_size,
        "jpg_under_youtube_limit": jpg_size < max_bytes,
        "jpg_sha256": sha256_file(jpg_path),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=pathlib.Path, default=DEFAULT_NAS_DIR)
    ap.add_argument("--mirror-icloud", action="store_true", default=True)
    ap.add_argument("--no-mirror-icloud", action="store_false", dest="mirror_icloud")
    args = ap.parse_args()

    out_dir: pathlib.Path = args.out_dir
    sources_dir = out_dir / "sources"
    out_dir.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    KIT_DOC_DIR.mkdir(parents=True, exist_ok=True)

    loaded_plates: Dict[str, Image.Image] = {}
    plate_records: Dict[str, dict] = {}
    for key, pinfo in ARCHIVE_PLATES.items():
        p_path = sources_dir / pinfo["filename"]
        if not p_path.is_file():
            raise FileNotFoundError(f"Missing verified public-domain archive plate: {p_path}")
        im = Image.open(p_path).convert("RGB")
        loaded_plates[key] = im
        plate_records[key] = {
            **pinfo,
            "dimensions": list(im.size),
            "bytes": p_path.stat().st_size,
            "sha256": sha256_file(p_path),
        }

    manifest_options = []
    preview_rows = []

    for opt in CHANNEL_OPTIONS:
        slug = opt["slug"]
        opt_dir = out_dir / slug
        opt_dir.mkdir(parents=True, exist_ok=True)

        src_im = loaded_plates[opt["plate_key"]]
        banner_im, banner_meta = build_banner(opt, src_im)
        av_photo_im, av_photo_meta = build_photo_avatar(opt, src_im)
        av_drawn_im, svg_text, av_drawn_meta = build_drawn_avatar_and_svg(opt)

        svg_path = SVG_DIR / f"profile_mark_{slug}.svg"
        svg_path.write_text(svg_text, encoding="utf-8")

        banner_files = save_png_and_jpg(banner_im, opt_dir / f"{slug}_banner_2560x1440", max_bytes=6 * 1024 * 1024)
        av_photo_files = save_png_and_jpg(av_photo_im, opt_dir / f"{slug}_profile_photo_800x800", max_bytes=4 * 1024 * 1024)
        av_drawn_files = save_png_and_jpg(av_drawn_im, opt_dir / f"{slug}_profile_drawn_800x800", max_bytes=4 * 1024 * 1024)

        preview_rows.append((opt, banner_im, av_photo_im, av_drawn_im))
        manifest_options.append({
            "slug": slug,
            "recommended": opt["recommended"],
            "name": opt["name"],
            "handle": opt["handle"],
            "archive_plate": opt["plate_key"],
            "banner_2560x1440": {**banner_files, **banner_meta},
            "profile_photo_800x800": {**av_photo_files, **av_photo_meta},
            "profile_drawn_800x800": {**av_drawn_files, **av_drawn_meta, "svg_in_repo": f"00_Brand/svg/{svg_path.name}"},
        })

    sheet = build_preview_sheet(preview_rows)
    sheet_path = out_dir / "preview_sheet_safe_areas.jpg"
    sheet.save(sheet_path, format="JPEG", quality=92, optimize=True)

    # Also write SVG guide of YouTube 2560x1440 banner safe area in repo
    safe_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BANNER_W} {BANNER_H}" width="1280" height="720">
  <rect width="{BANNER_W}" height="{BANNER_H}" fill="#141A22"/>
  <rect x="0" y="{SAFE_Y0}" width="{BANNER_W}" height="{SAFE_H}" fill="none" stroke="#5AA9E6" stroke-width="4" stroke-dasharray="16,10"/>
  <rect x="{TABLET_X0}" y="{SAFE_Y0}" width="{TABLET_W}" height="{SAFE_H}" fill="none" stroke="#FFB43C" stroke-width="4" stroke-dasharray="12,8"/>
  <rect x="{SAFE_X0}" y="{SAFE_Y0}" width="{SAFE_W}" height="{SAFE_H}" fill="#1E2936" fill-opacity="0.55" stroke="#3CF578" stroke-width="6"/>
  <text x="{BANNER_W // 2}" y="{BANNER_H // 2 - 12}" text-anchor="middle" font-family="DIN Alternate, Helvetica, Arial, sans-serif" font-weight="700" font-size="44" fill="#FFFFFF">ALL-DEVICES SAFE AREA: {SAFE_W} x {SAFE_H} px (x={SAFE_X0}..{SAFE_X1}, y={SAFE_Y0}..{SAFE_Y1})</text>
  <text x="{BANNER_W // 2}" y="{BANNER_H // 2 + 44}" text-anchor="middle" font-family="DIN Alternate, Helvetica, Arial, sans-serif" font-size="30" fill="#FFD600">Tablet: {TABLET_W}x{SAFE_H} · Desktop: {BANNER_W}x{SAFE_H} · TV Full Canvas: {BANNER_W}x{BANNER_H}</text>
</svg>
"""
    (SVG_DIR / "youtube_banner_safe_area_guide.svg").write_text(safe_svg, encoding="utf-8")

    icloud_mirrored = False
    if args.mirror_icloud and DEFAULT_ICLOUD_DIR.parents[1].is_dir():
        DEFAULT_ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
        for opt in CHANNEL_OPTIONS:
            slug = opt["slug"]
            dst_sub = DEFAULT_ICLOUD_DIR / slug
            dst_sub.mkdir(parents=True, exist_ok=True)
            for src_file in (out_dir / slug).iterdir():
                if src_file.is_file():
                    shutil.copy2(src_file, dst_sub / src_file.name)
        shutil.copy2(sheet_path, DEFAULT_ICLOUD_DIR / sheet_path.name)
        icloud_mirrored = True

    manifest = {
        "job": "J2999",
        "generated_by": "00_Brand/tools/build_channel_kit.py",
        "nas_folder": "studio-live/ww2/00_Brand/Channel-Kit",
        "icloud_watch_folder": "WW2 UAT/00_Channel-Kit" if icloud_mirrored else None,
        "youtube_limits": {
            "profile_picture_px": [800, 800],
            "profile_picture_max_bytes": 4 * 1024 * 1024,
            "banner_px": [2560, 1440],
            "banner_safe_area_px": [1546, 423],
            "banner_max_bytes": 6 * 1024 * 1024,
        },
        "archive_plates": plate_records,
        "options": manifest_options,
        "preview_sheet": {
            "filename": sheet_path.name,
            "bytes": sheet_path.stat().st_size,
            "sha256": sha256_file(sheet_path),
        },
    }
    manifest_path = KIT_DOC_DIR / "ART_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built 3 channel art sets -> {out_dir} (iCloud mirror={icloud_mirrored})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
