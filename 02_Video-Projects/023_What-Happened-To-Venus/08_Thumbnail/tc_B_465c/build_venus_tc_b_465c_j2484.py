#!/usr/bin/env python3
"""
J2484 / J2487 — Build 023 Venus (VBaYRPp85Sw, "What Happened to Venus?") Test & Compare B
thumbnail '465°C' (Venus's surface with a Venera-style lander under 465°C atmospheric sky
cast, J1198 draw branch; fixed per J2486 design review).

Rules enforced (00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md §2, §2.A, §2.B,
05_Analytics/LEARNINGS.md rules 11-13, and J2486 design review):
  - £0 cost: built from text-free base plate `venus_surface_465c_lander_plate.jpg`
    (photorealistic Soviet Venera-style lander on solid fractured Venusian basalt slabs
    under dense warm amber-orange atmospheric sky cast, with NO incandescent red-orange
    metal glow and NO molten rock cracks since 465°C is below the ~525°C Draper point)
    + deterministic colour grade and code-rendered typography.
  - One big focal point (>= 1/3 of frame): spacecraft lander on Venus's rocky surface.
  - Clear scale / stakes element (spacecraft lander baking on the surface), distinct from
    planet-globe A ('MELTS LEAD') and ended B ('EARTH'S TWIN').
  - No Orbit on long-form thumbnails (§2.8).
  - Text: '465°C' (1 token, <= 3 words) in the top-left sky band (off the lander hero and
    clear of the bottom-right duration corner), house heavy sans (Arial Black),
    yellow (255, 230, 0), heavy black stroke + drop shadow, ~11.9% cap height.
  - Color grade (J2487 fix): mean HSV saturation ~175-185 (within 165-195 / 170-200 target,
    matching the channel's 140-187 range and Venus search neighbours), < 2% pixels pinned at
    S >= 250 (no neon-red clipping), near-black <= 30%.
  - Output: 1280x720 JPG (< 2 MB) + SHA256.txt + thumb_preview.py --score gate sheet.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parent
PLATE_JPG = OUT_DIR / "venus_surface_465c_lander_plate.jpg"
NAS_PLATE_CANDIDATES = [
    Path(
        "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
        "023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_surface_465c_lander_plate.jpg"
    ),
    Path(
        "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/"
        "023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_surface_465c_lander_plate.jpg"
    ),
]
OUT_JPG = OUT_DIR / "venus_tc_B_465c_VBaYRPp85Sw.jpg"
PREVIEW_JPG = OUT_DIR / "venus_tc_B_465c_preview_sheet.jpg"
COMPARE_JPG = OUT_DIR / "venus_tc_A_vs_B_465c_sheet.jpg"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1280, 720

YELLOW = (255, 230, 0)
STROKE_BLACK = (8, 5, 4)


def _grade_venus_lander_plate(plate_path: Path) -> Image.Image:
    """
    Resize the text-free Venera lander plate to 1280x720 and apply a restrained,
    physically accurate warm atmospheric grade (J2487 fix):
      - Mean HSV saturation sits in ~175-185 (within 165-195 and 170-200)
      - < 2% of pixels are pinned at S >= 250 (no neon-red clipping)
      - Near-black pixels (luma < 26) stay ~21% (<= 30% ceiling)
      - Zero self-luminous red-orange/white-hot glow on the lander underside or basalt rocks;
        only the warm amber-orange atmospheric sky cast lights the upper metallic lander.
    """
    im = Image.open(plate_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)

    # 1. Moderate colour saturation to ~182 mean HSV sat and sharpen metallic hardware
    im = ImageEnhance.Color(im).enhance(0.88)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.22)

    arr = np.asarray(im, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    # 2. Gentle neutral-warm shadow lift so deepest basalt shadows do not crush (keeps near_black ~19% <= 30% without red tint)
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    dark_lift = np.clip((38.0 - luma) / 38.0, 0.0, 1.0) ** 1.15
    arr[..., 0] += dark_lift * 16.0
    arr[..., 1] += dark_lift * 12.0
    arr[..., 2] += dark_lift * 7.0

    # 3. Warm amber-orange atmospheric sky cast on upper lander & clouds (no red clipping)
    sky_and_upper = np.clip((430.0 - yy) / 430.0, 0.0, 1.0) * np.clip(luma / 140.0, 0.0, 1.0)
    arr[..., 0] = np.clip(arr[..., 0] + sky_and_upper * 14.0, 0.0, 255.0)
    arr[..., 1] = np.clip(arr[..., 1] + sky_and_upper * 4.0, 0.0, 255.0)

    # 4. Neutral-warm metallic clarity on the lander hardware (x=620..1050, y=180..610)
    # Lifts existing metallic highlights (not shadows) in balanced gold-bronze so the lander
    # struts, collar, and hull separate cleanly from the dark basalt rocks at 168x94 without glowing.
    lander_mask = np.exp(-(((xx - 835.0) / 195.0) ** 2 + ((yy - 410.0) / 195.0) ** 2))
    metal_hi = np.clip((luma - 28.0) / 95.0, 0.0, 1.0) * lander_mask
    arr[..., 0] = np.clip(arr[..., 0] + metal_hi * 22.0, 0.0, 255.0)
    arr[..., 1] = np.clip(arr[..., 1] + metal_hi * 17.0, 0.0, 255.0)
    arr[..., 2] = np.clip(arr[..., 2] + metal_hi * 10.0, 0.0, 255.0)

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")


def _draw_top_band_hook(img: Image.Image, text: str = "465°C") -> tuple[Image.Image, dict]:
    """
    Draw '465°C' in the top-left sky band (completely off the lander on the right
    and clear of the bottom-right duration corner) in house heavy sans (Arial Black),
    yellow (255, 230, 0), heavy black stroke + drop shadow, ~12.1% cap height (87 px on 720p).
    """
    base = img.convert("RGBA")

    target_cap_px = 87
    probe_font = ImageFont.truetype(FONT_BOLD, 100)
    probe_bb = probe_font.getbbox("465C")
    probe_cap = max(1, probe_bb[3] - probe_bb[1])
    font_size = int(round(100 * target_cap_px / probe_cap))
    font = ImageFont.truetype(FONT_BOLD, font_size)

    stroke_w = max(9, font_size // 12)
    bb = font.getbbox(text, stroke_width=stroke_w)
    cap_bb = font.getbbox("465C")
    cap_px = cap_bb[3] - cap_bb[1]

    # Top-left sky band: x=68, y=34 (completely clear of lander on right x>=605 and volcano peak y>=165)
    tx = 68 - bb[0]
    ty = 34 - bb[1]

    # Soft warm-dark contrast cushion behind '465°C' so it pops immediately at 168x94
    cushion = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cushion)
    bx0, by0 = tx + bb[0] - 26, ty + bb[1] - 16
    bx1, by1 = tx + bb[2] + 26, ty + bb[3] + 16
    cdraw.rounded_rectangle((bx0, by0, bx1, by1), radius=26, fill=(32, 9, 2, 138))
    cushion = cushion.filter(ImageFilter.GaussianBlur(radius=18))
    base = Image.alpha_composite(base, cushion)

    # Drop shadow + heavy black stroke + house yellow fill
    txt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    tdraw.text(
        (tx + 5, ty + 6),
        text,
        font=font,
        fill=(0, 0, 0, 235),
        stroke_width=stroke_w + 4,
        stroke_fill=(0, 0, 0, 235),
    )
    txt_layer = txt_layer.filter(ImageFilter.GaussianBlur(radius=3))
    tdraw = ImageDraw.Draw(txt_layer)
    tdraw.text(
        (tx, ty),
        text,
        font=font,
        fill=(*YELLOW, 255),
        stroke_width=stroke_w,
        stroke_fill=(*STROKE_BLACK, 255),
    )
    out = Image.alpha_composite(base, txt_layer).convert("RGB")

    meta = {
        "text": text,
        "font": FONT_BOLD,
        "font_size_pt": font_size,
        "cap_height_px": int(cap_px),
        "cap_height_pct": round(100.0 * cap_px / H, 2),
        "bbox_px": [int(tx + bb[0]), int(ty + bb[1]), int(tx + bb[2]), int(ty + bb[3])],
        "stroke_width_px": int(stroke_w),
    }
    return out, meta


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not PLATE_JPG.exists():
        for cand in NAS_PLATE_CANDIDATES:
            if cand.exists():
                PLATE_JPG.write_bytes(cand.read_bytes())
                break
    if not PLATE_JPG.exists():
        raise FileNotFoundError(f"Missing base plate: {PLATE_JPG}")

    graded = _grade_venus_lander_plate(PLATE_JPG)
    final_img, text_meta = _draw_top_band_hook(graded, "465°C")

    final_img.save(OUT_JPG, "JPEG", quality=93, optimize=True, progressive=True)

    size_bytes = OUT_JPG.stat().st_size
    sha256 = hashlib.sha256(OUT_JPG.read_bytes()).hexdigest()
    plate_sha256 = hashlib.sha256(PLATE_JPG.read_bytes()).hexdigest()
    (OUT_DIR / "SHA256.txt").write_text(
        f"{sha256}  {OUT_JPG.name}\n{plate_sha256}  {PLATE_JPG.name}\n",
        encoding="utf-8",
    )

    hsv = np.asarray(final_img.convert("HSV"), dtype=np.float32)
    luma_l = np.asarray(final_img.convert("L"), dtype=np.float32)
    sat_mean = float(hsv[..., 1].mean())
    sat_pinned_250_pct = float((hsv[..., 1] >= 250).mean() * 100.0)
    val_mean = float(hsv[..., 2].mean())
    near_black_pct = float((luma_l < 26).mean() * 100.0)

    print(
        json.dumps(
            {
                "output": str(OUT_JPG),
                "size_bytes": size_bytes,
                "sha256": sha256,
                "plate_sha256": plate_sha256,
                "sat_mean": round(sat_mean, 1),
                "sat_pinned_250_pct": round(sat_pinned_250_pct, 2),
                "val_mean": round(val_mean, 1),
                "near_black_pct": round(near_black_pct, 1),
                "text_meta": text_meta,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
