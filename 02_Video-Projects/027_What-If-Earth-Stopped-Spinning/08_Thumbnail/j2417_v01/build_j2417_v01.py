#!/usr/bin/env python3
"""J2430: Build 027 arm A and B thumbnails for J2417 title+thumbnail test.
Arm A: '4 CM A YEAR' — The Moon, huge and bright, edge-lit on dark space, Earth a thin crescent at the corner.
Arm B: 'CORALS KEPT COUNT' — One fossil coral, close-up, growth lines sharp, warm light on dark ground.
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

def draw_top_band_text(im: Image.Image, words: list[str], yellow_words: set[str], font_size: int = 108, y: int = 32) -> list[int]:
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size)
    total_w = sum(d.textlength(w, font=font) for w in words) + d.textlength(" ", font=font) * (len(words) - 1)
    x = max(44, round((W - total_w) / 2))
    x0 = x
    for i, w in enumerate(words):
        fill = YELLOW if w in yellow_words else WHITE
        d.text((x, y), w, font=font, fill=fill, stroke_width=6, stroke_fill=STROKE, anchor="lt")
        x += d.textlength(w + (" " if i < len(words) - 1 else ""), font=font)
    return [round(x0), y, round(x), y + round(font_size * 0.78)]

def build_arm_a(moon_path: Path, earth_path: Path, out_path: Path) -> dict:
    yy, xx = np.mgrid[:H, :W]
    mcx, mcy, mr = 760.0, 425.0, 275.0
    mdist = np.sqrt((xx - mcx)**2 + (yy - mcy)**2)
    halo = np.exp(-((mdist - mr * 0.85)**2) / (190.0**2))
    bg_grad = np.exp(-((xx - 680)**2 + (yy - 410)**2) / (680.0**2))

    bg = np.zeros((H, W, 3), dtype=np.float32)
    bg[:, :, 0] = 0.04 + 0.05 * bg_grad + 0.14 * halo
    bg[:, :, 1] = 0.10 + 0.12 * bg_grad + 0.30 * halo
    bg[:, :, 2] = 0.26 + 0.22 * bg_grad + 0.52 * halo

    moon_raw = Image.open(moon_path).convert("RGB")
    mbox = moon_raw.convert("L").point(lambda v: 255 if v > 15 else 0).getbbox()
    moon_crop = moon_raw.crop(mbox).resize((int(mr * 2), int(mr * 2)), Image.Resampling.LANCZOS)
    moon_crop = moon_crop.filter(ImageFilter.UnsharpMask(radius=1.8, percent=75, threshold=2))
    m_arr = np.asarray(moon_crop).astype(np.float32) / 255.0

    my, mx = np.mgrid[:int(mr * 2), :int(mr * 2)]
    nx = (mx - mr) / mr
    ny = (my - mr) / mr
    r2 = nx**2 + ny**2
    nz = np.sqrt(np.clip(1.0 - r2, 0, 1))
    dot = np.clip(-0.68 * nx - 0.15 * ny + 0.72 * nz, 0, 1)
    rim = np.clip((1.0 - nz) * np.clip(-nx + 0.25, 0, 1), 0, 1) ** 1.4
    shade = 0.18 + 0.95 * (dot ** 0.75) + 0.55 * rim

    m_lum = 0.299 * m_arr[:, :, 0] + 0.587 * m_arr[:, :, 1] + 0.114 * m_arr[:, :, 2]
    m_lum = np.power(np.clip(m_lum * 1.18, 0, 1), 0.82)
    moon_rgb = np.zeros_like(m_arr)
    moon_rgb[:, :, 0] = np.clip(m_lum * shade * 1.18 + 0.22 * rim, 0, 1)
    moon_rgb[:, :, 1] = np.clip(m_lum * shade * 1.02 + 0.18 * rim, 0, 1)
    moon_rgb[:, :, 2] = np.clip(m_lum * (0.68 * shade + 0.22) + 0.28 * rim, 0, 1)

    im = Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8))
    moon_im = Image.fromarray((moon_rgb * 255).astype(np.uint8))
    moon_mask = Image.new("L", (int(mr * 2), int(mr * 2)), 0)
    ImageDraw.Draw(moon_mask).ellipse((2, 2, int(mr * 2) - 3, int(mr * 2) - 3), fill=255)
    moon_mask = moon_mask.filter(ImageFilter.GaussianBlur(1.2))
    im.paste(moon_im, (int(mcx - mr), int(mcy - mr)), moon_mask)

    earth_raw = Image.open(earth_path).convert("RGB")
    ebox = earth_raw.convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    ed = 230
    er = ed / 2.0
    earth_crop = earth_raw.crop(ebox).resize((ed, ed), Image.Resampling.LANCZOS)
    earth_crop = ImageEnhance.Color(ImageEnhance.Brightness(earth_crop).enhance(1.35)).enhance(1.85)
    e_arr = np.asarray(earth_crop).astype(np.float32) / 255.0
    ey, ex = np.mgrid[:ed, :ed]
    enx = (ex - er) / er
    eny = (ey - er) / er
    enz = np.sqrt(np.clip(1.0 - (enx**2 + eny**2), 0, 1))
    edot = np.clip(0.82 * enx - 0.25 * eny + 0.25 * enz, 0, 1)
    ecres = (edot ** 1.35)
    erim = (np.clip(1.0 - enz, 0, 1) ** 1.8) * np.clip(enx + 0.1, 0, 1)
    e_rgb = np.zeros_like(e_arr)
    e_rgb[:, :, 0] = np.clip(e_arr[:, :, 0] * ecres * 1.1 + 0.05 + 0.25 * erim, 0, 1)
    e_rgb[:, :, 1] = np.clip(e_arr[:, :, 1] * ecres * 1.25 + 0.12 + 0.55 * erim, 0, 1)
    e_rgb[:, :, 2] = np.clip(e_arr[:, :, 2] * ecres * 1.45 + 0.26 + 0.85 * erim, 0, 1)
    earth_im = Image.fromarray((e_rgb * 255).astype(np.uint8))
    earth_mask = Image.new("L", (ed, ed), 0)
    ImageDraw.Draw(earth_mask).ellipse((2, 2, ed - 3, ed - 3), fill=255)
    earth_mask = earth_mask.filter(ImageFilter.GaussianBlur(1.0))
    im.paste(earth_im, (64, 445), earth_mask)

    hook_box = draw_top_band_text(im, ["4", "CM", "A", "YEAR"], {"4", "CM"}, font_size=110, y=30)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "A",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "Earth Is Losing Its Spin (And the Moon Is Taking It)",
        "text": "4 CM A YEAR",
        "yellow_word": "4 CM",
        "source_id": "GSFC_20171208_Archive_e000868 + GSFC_20171208_Archive_e002130",
        "source_credit": "NASA (public domain)",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def build_arm_b(coral_path: Path, out_path: Path) -> dict:
    src = Image.open(coral_path).convert("RGB")
    sw, sh = src.size
    arr_full = np.asarray(src).astype(np.float32) / 255.0
    r, g, b = arr_full[:, :, 0], arr_full[:, :, 1], arr_full[:, :, 2]
    warmth = np.clip((r - b) * 4.5 + (g - b) * 2.0, 0, 1)
    yy_f, xx_f = np.mgrid[:sh, :sw]
    ell = 1.0 - np.sqrt(((xx_f - sw * 0.50) / (sw * 0.44))**2 + ((yy_f - sh * 0.49) / (sh * 0.43))**2)
    top_taper = np.clip((yy_f - sh * 0.02) / (sh * 0.08), 0, 1)
    spec_raw = np.clip(((ell * 2.4) + warmth * 0.55 - 0.45) * top_taper, 0, 1)
    card_mask = ((xx_f < 720) & (yy_f > 2280)).astype(np.float32)
    spec_raw = spec_raw * (1.0 - card_mask)
    mask_im = Image.fromarray((spec_raw * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))

    target_w, target_h = 900, 565
    coral_resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mask_resized = mask_im.resize((target_w, target_h), Image.Resampling.LANCZOS)

    coral_sharp = coral_resized.filter(ImageFilter.UnsharpMask(radius=2.2, percent=110, threshold=2))
    c_arr = np.asarray(coral_sharp).astype(np.float32) / 255.0
    c_arr = np.power(np.clip(c_arr, 0, 1), 0.88)
    c_warm = np.zeros_like(c_arr)
    c_warm[:, :, 0] = np.clip(c_arr[:, :, 0] * 1.24 + 0.04, 0, 1)
    c_warm[:, :, 1] = np.clip(c_arr[:, :, 1] * 0.98 + 0.01, 0, 1)
    c_warm[:, :, 2] = np.clip(c_arr[:, :, 2] * 0.62, 0, 1)
    coral_final = Image.fromarray((c_warm * 255).astype(np.uint8))
    coral_final = ImageEnhance.Contrast(coral_final).enhance(1.18)
    coral_final = ImageEnhance.Color(coral_final).enhance(1.35)

    yy, xx = np.mgrid[:H, :W]
    spot = np.exp(-((xx - 640)**2 + (yy - 430)**2) / (520.0**2))
    bg = np.zeros((H, W, 3), dtype=np.float32)
    bg[:, :, 0] = 0.16 + 0.24 * spot
    bg[:, :, 1] = 0.08 + 0.12 * spot
    bg[:, :, 2] = 0.02 + 0.03 * spot
    im = Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8))

    im.paste(coral_final, (round((W - target_w) / 2), 142), mask_resized)

    hook_box = draw_top_band_text(im, ["CORALS", "KEPT", "COUNT"], {"CORALS"}, font_size=90, y=38)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "B",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)",
        "text": "CORALS KEPT COUNT",
        "yellow_word": "CORALS",
        "source_id": "File:Heliophyllum confluens (fossil coral) (Columbus Limestone, Middle Devonian; Delaware County, Ohio, USA).jpg",
        "source_credit": "James St. John / Wikimedia Commons (CC BY 2.0)",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def main():
    in_dir = Path("/private/tmp/j2430_inputs")
    earth_src = Path("/Users/benjaminoats/_desk/J1823/inputs/GSFC_20171208_Archive_e002130.jpg")
    nas_dir = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/j2417_v01")
    local_dir = REPO / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/08_Thumbnail/j2417_v01"
    stage = Path("/private/tmp/j2430_out/027")
    stage.mkdir(parents=True, exist_ok=True)

    a_file = stage / "027_j2417_A_4_cm_a_year_v01.jpg"
    b_file = stage / "027_j2417_B_corals_kept_count_v01.jpg"
    res_a = build_arm_a(in_dir / "e000868_moon.jpg", earth_src, a_file)
    res_b = build_arm_b(in_dir / "coral_1.jpg", b_file)

    preview_sheet = stage / "027_j2417_preview_sheet_v01.jpg"
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
        "film": "OWB:027",
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

    nas_dir.mkdir(parents=True, exist_ok=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    for item in stage.iterdir():
        shutil.copy2(item, nas_dir / item.name)
        if item.suffix.lower() in (".jpg", ".png"):
            shutil.copy2(item, local_dir / item.name)

if __name__ == "__main__":
    main()
