#!/usr/bin/env python3
"""J2430: Build 026 arm A and B thumbnails for J2417 title+thumbnail test.
Arm A: '11-DAY YEAR' — Proxima b as a dark crescent against a small red star (ESO eso1629e).
Arm B: 'TRILLIONS OF YEARS' — Proxima, a single red star, huge, high contrast, no other stars (Hubble potw1343a).
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
STROKE = (8, 10, 18)

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SYS_TOOLS = REPO / "00_Brand/Channel-Setup/tools"
sys.path.insert(0, str(SYS_TOOLS))
from thumb_preview import score as score_thumb

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def draw_top_band_text(im: Image.Image, words: list[str], yellow_word: str, font_size: int = 112, y: int = 34) -> list[int]:
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size)
    total_w = sum(d.textlength(w, font=font) for w in words) + d.textlength(" ", font=font) * (len(words) - 1)
    x = max(44, round((W - total_w) / 2))
    x0 = x
    for i, w in enumerate(words):
        fill = YELLOW if w == yellow_word else WHITE
        d.text((x, y), w, font=font, fill=fill, stroke_width=6, stroke_fill=STROKE, anchor="lt")
        x += d.textlength(w + (" " if i < len(words) - 1 else ""), font=font)
    return [round(x0), y, round(x), y + round(font_size * 0.78)]

def build_arm_a(src_path: Path, out_path: Path) -> dict:
    src = Image.open(src_path).convert("RGB")
    sw, sh = src.size
    cw = sw
    ch = round(cw * 9 / 16)
    crop = src.crop((0, 0, cw, ch)).resize((W, H), Image.Resampling.LANCZOS)

    arr = np.asarray(crop).astype(np.float32) / 255.0
    yy, xx = np.mgrid[:H, :W]
    star_glow = np.exp(-((xx - 260)**2 + (yy - 380)**2) / (340.0**2))
    rim_glow = np.exp(-((xx - 680)**2 + (yy - 460)**2) / (480.0**2))
    space_grad = np.clip(1.0 - 0.25 * (yy / H), 0.65, 1.0)

    arr = np.power(np.clip(arr, 0, 1), 0.72)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    dark_mask = np.clip((0.24 - lum) / 0.24, 0, 1)[:, :, None]

    # Rich cosmic crimson-violet lift so shadows/night side sit around luma 30-45 (keeping near-black ~12%)
    cosmic_bg = np.zeros_like(arr)
    cosmic_bg[:, :, 0] = 0.14 + 0.22 * star_glow + 0.10 * rim_glow
    cosmic_bg[:, :, 1] = 0.06 + 0.07 * star_glow + 0.05 * rim_glow
    cosmic_bg[:, :, 2] = 0.22 * space_grad + 0.08 * rim_glow

    planet_night = np.exp(-(((xx - 745)**2 + (yy - 430)**2) / (190.0**2)))[:, :, None]
    lift_weight = dark_mask * (1.0 - 0.55 * planet_night)
    arr = arr * (1.0 - 0.75 * lift_weight) + cosmic_bg * (0.88 * lift_weight)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.22 + 0.16 * star_glow, 0, 1)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.06 + 0.04 * star_glow, 0, 1)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 1.06, 0, 1)

    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.55)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=3))

    hook_box = draw_top_band_text(im, ["11-DAY", "YEAR"], "11-DAY", font_size=112, y=32)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "A",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "The Nearest Star Is One You Can't See (And It Has a Planet)",
        "text": "11-DAY YEAR",
        "yellow_word": "11-DAY",
        "source_id": "eso1629e",
        "source_credit": "ESO/M. Kornmesser (CC BY 4.0)",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def build_arm_b(src_path: Path, out_path: Path) -> dict:
    src = Image.open(src_path).convert("RGB")
    cw = 1360
    ch = round(cw * 9 / 16)
    cx, cy = 1024, 768
    left = round(cx - cw / 2)
    top = round(cy - 0.597 * ch)
    crop = src.crop((left, top, left + cw, top + ch)).resize((W, H), Image.Resampling.LANCZOS)

    arr = np.asarray(crop).astype(np.float32) / 255.0
    yy, xx = np.mgrid[:H, :W]
    scx, scy = 640.0, 435.0
    dist = np.sqrt((xx - scx)**2 + (yy - scy)**2)

    # Suppress isolated background field stars outside Proxima's inner corona (r > 135)
    blurred = np.asarray(crop.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255.0
    outer_mask = np.clip((dist - 125.0) / 80.0, 0, 1)[:, :, None]
    arr = arr * (1.0 - outer_mask) + blurred * outer_mask

    # Smooth stellar profile (no hard circular step!) + rich glowing red corona
    disc_glow = np.exp(-((dist / 135.0) ** 3.2))
    core_glow = np.exp(-((dist / 85.0) ** 2.2))
    halo_glow = np.exp(-((dist / 290.0) ** 1.8))
    bg_glow = np.exp(-((dist / 620.0) ** 1.6))

    star_lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    corona_tex = np.power(np.clip(star_lum, 0, 1), 0.75) * np.exp(-((dist / 220.0) ** 2.0))

    out_arr = np.zeros_like(arr)
    out_arr[:, :, 0] = 0.17 + 0.18 * bg_glow + 0.45 * halo_glow + 0.55 * disc_glow + 0.35 * corona_tex
    out_arr[:, :, 1] = 0.03 + 0.04 * bg_glow + 0.10 * halo_glow + 0.28 * disc_glow + 0.52 * core_glow + 0.22 * corona_tex
    out_arr[:, :, 2] = 0.07 + 0.05 * bg_glow + 0.04 * halo_glow + 0.06 * disc_glow + 0.24 * (core_glow**1.8)

    out_arr = np.clip(out_arr, 0, 1)
    im = Image.fromarray((out_arr * 255).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=45, threshold=3))

    hook_box = draw_top_band_text(im, ["TRILLIONS", "OF", "YEARS"], "TRILLIONS", font_size=96, y=36)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "B",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "The Star Next Door Is Invisible (And It Will Outlive Our Sun)",
        "text": "TRILLIONS OF YEARS",
        "yellow_word": "TRILLIONS",
        "source_id": "potw1343a",
        "source_credit": "ESA/Hubble & NASA (CC BY 4.0)",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def main():
    in_dir = Path("/private/tmp/j2430_inputs")
    out_dirs = [
        REPO / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/j2417_v01",
        Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/08_Thumbnail/j2417_v01"),
    ]
    stage = Path("/private/tmp/j2430_out/026")
    stage.mkdir(parents=True, exist_ok=True)

    a_file = stage / "026_j2417_A_11_day_year_v01.jpg"
    b_file = stage / "026_j2417_B_trillions_of_years_v01.jpg"
    res_a = build_arm_a(in_dir / "eso1629e.jpg", a_file)
    res_b = build_arm_b(in_dir / "potw1343a_2048.jpg", b_file)

    preview_sheet = stage / "026_j2417_preview_sheet_v01.jpg"
    cmd = [
        sys.executable,
        str(SYS_TOOLS / "thumb_preview.py"),
        "long",
        str(a_file),
        str(b_file),
        "--out",
        str(preview_sheet),
        "--score",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(proc.stdout)
    (stage / "GATE.txt").write_text(proc.stdout)

    meta = {
        "job": "J2430",
        "ref": "J2417",
        "film": "OWB:026",
        "version": "j2417_v01",
        "cost_gbp": 0,
        "variants": [res_a, res_b],
        "preview_sheet": {
            "file": preview_sheet.name,
            "sha256": sha256(preview_sheet),
        },
    }
    (stage / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copyfile(__file__, stage / "build_j2417_v01.py")

    for d in out_dirs:
        d.mkdir(parents=True, exist_ok=True)
        for item in stage.iterdir():
            shutil.copy2(item, d / item.name)

if __name__ == "__main__":
    main()
