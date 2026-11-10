#!/usr/bin/env python3
"""J2430: Build 032 arm A and B thumbnails for J2417 title+thumbnail test.
Arm A: 'WATER DEEP BELOW' — Titan as a cut-away sphere: orange haze shell, a thin blue water layer inside. One object, centred.
Arm B: '72 MINUTES' — The real Huygens surface frame (rounded ice pebbles, orange ground), graded hot, full bleed.
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

def draw_top_band_text(im: Image.Image, words: list[str], yellow_words: set[str], font_size: int = 104, y: int = 34) -> list[int]:
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

def build_arm_a(titan_src: Path, out_path: Path) -> dict:
    # PIA14602.jpg: Cassini natural-colour view of Titan.
    # Spec: "Titan as a cut-away sphere: orange haze shell, a thin blue water layer inside. One object, centred"
    # Text: "WATER DEEP BELOW"
    yy, xx = np.mgrid[:H, :W]
    cx, cy, R = 640.0, 435.0, 255.0
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)

    # Rich deep cosmic teal-indigo background with warm golden atmospheric glow around Titan
    atmo_glow = np.exp(-((dist - R * 0.92)**2) / (155.0**2))
    bg_grad = np.exp(-(dist**2) / (620.0**2))
    bg = np.zeros((H, W, 3), dtype=np.float32)
    bg[:, :, 0] = 0.05 + 0.08 * bg_grad + 0.42 * atmo_glow
    bg[:, :, 1] = 0.10 + 0.12 * bg_grad + 0.24 * atmo_glow
    bg[:, :, 2] = 0.24 + 0.18 * bg_grad + 0.08 * atmo_glow

    im = Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8))

    # Extract Titan sphere from PIA14602 (crop 265, 275, 775, 785)
    raw = Image.open(titan_src).convert("RGB").crop((265, 275, 775, 785))
    diam = int(R * 2)
    globe = raw.resize((diam, diam), Image.Resampling.LANCZOS)
    globe = ImageEnhance.Color(ImageEnhance.Contrast(globe).enhance(1.28)).enhance(1.95)
    g_arr = np.asarray(globe).astype(np.float32) / 255.0

    # Local coordinates inside the diam x diam sphere
    gy, gx = np.mgrid[:diam, :diam]
    nx = (gx - R) / R
    ny = (gy - R) / R
    r = np.sqrt(nx**2 + ny**2)
    angle = np.arctan2(ny, nx) # radians: 0 is right, pi/2 is down, -pi/2 is up

    # Push Titan's outer globe toward rich golden-orange haze with a cyan-blue photochemical upper limb
    limb = np.clip((r - 0.88) / 0.12, 0, 1) * (r <= 1.0)
    g_arr[:, :, 0] = np.clip(g_arr[:, :, 0] * 1.18 * (1.0 - 0.45 * limb), 0, 1)
    g_arr[:, :, 1] = np.clip(g_arr[:, :, 1] * 0.96 + 0.18 * limb, 0, 1)
    g_arr[:, :, 2] = np.clip(g_arr[:, :, 2] * 0.55 + 0.55 * limb, 0, 1)

    # Cutaway sector on the right hemisphere: nx > 0.02 and ny > -0.68 and ny < 0.72
    # Use smooth anti-aliased masks for the cutaway wedge:
    in_sphere = np.clip((1.0 - r) * R / 1.5, 0, 1)
    cut_mask_x = np.clip((nx - 0.0) * R / 2.0, 0, 1)
    cut_mask_y1 = np.clip((ny + 0.62) * R / 2.0, 0, 1)
    cut_mask_y2 = np.clip((0.72 - ny) * R / 2.0, 0, 1)
    cut_wedge = cut_mask_x * cut_mask_y1 * cut_mask_y2 * (r <= 0.995)

    # Concentric interior shells inside the cutaway wedge:
    # 1. Outer orange haze + crust rim: r in [0.87, 1.00]
    # 2. Bright cyan-blue subsurface liquid water ocean: r in [0.71, 0.87]
    # 3. Inner ice mantle: r in [0.46, 0.71]
    # 4. Rocky/hydro-silicate core: r in [0.00, 0.46]
    # Add 3D shading across the cutaway cross-section planes so it looks dimensional
    plane_shade = 0.78 + 0.25 * np.cos((ny + 0.1) * 2.2) - 0.12 * (nx - 0.4)

    interior = np.zeros_like(g_arr)
    # Outer orange haze & ice crust layer (0.87..1.00)
    w_outer = np.clip((r - 0.865) * 90.0, 0, 1)
    # Subsurface liquid water ocean layer (0.71..0.865) — vivid glowing cyan-blue!
    w_ocean = np.clip((0.865 - r) * 90.0, 0, 1) * np.clip((r - 0.705) * 90.0, 0, 1)
    # Inner ice shell (0.46..0.705)
    w_mantle = np.clip((0.705 - r) * 90.0, 0, 1) * np.clip((r - 0.45) * 90.0, 0, 1)
    # Rocky core (< 0.45)
    w_core = np.clip((0.45 - r) * 90.0, 0, 1)

    # Core shading (3D sphere at center)
    core_z = np.sqrt(np.clip(0.45**2 - r**2, 0, 1)) / 0.45
    core_light = 0.45 + 0.65 * np.clip(-0.4 * (nx / 0.45) - 0.4 * (ny / 0.45) + 0.8 * core_z, 0, 1)

    # Combine layers
    # Outer haze/crust: warm golden-amber
    c_outer = np.stack([
        np.full_like(r, 0.95) * plane_shade,
        np.full_like(r, 0.56) * plane_shade,
        np.full_like(r, 0.14) * plane_shade,
    ], axis=2)
    # Ocean layer: luminous electric cyan-blue with subtle radial wave shimmer
    ocean_radial = (r - 0.705) / 0.16
    ocean_glow = 0.85 + 0.20 * np.sin(ocean_radial * np.pi)
    c_ocean = np.stack([
        np.full_like(r, 0.06) * ocean_glow,
        np.full_like(r, 0.72) * ocean_glow * plane_shade,
        np.full_like(r, 1.00) * ocean_glow,
    ], axis=2)
    # Bright white-cyan specular lines at top/bottom boundaries of the ocean layer
    ocean_rim = np.exp(-((r - 0.865) / 0.008)**2) + np.exp(-((r - 0.705) / 0.008)**2)
    # Inner mantle: muted steel-blue ice
    c_mantle = np.stack([
        np.full_like(r, 0.24) * plane_shade,
        np.full_like(r, 0.36) * plane_shade,
        np.full_like(r, 0.52) * plane_shade,
    ], axis=2)
    # Core: warm ochre-brown rock
    c_core = np.stack([
        np.full_like(r, 0.68) * core_light,
        np.full_like(r, 0.44) * core_light,
        np.full_like(r, 0.24) * core_light,
    ], axis=2)

    interior = (
        c_outer * w_outer[:, :, None]
        + c_ocean * w_ocean[:, :, None]
        + c_mantle * w_mantle[:, :, None]
        + c_core * w_core[:, :, None]
    )
    interior[:, :, 0] = np.clip(interior[:, :, 0] + 0.55 * ocean_rim, 0, 1)
    interior[:, :, 1] = np.clip(interior[:, :, 1] + 0.85 * ocean_rim, 0, 1)
    interior[:, :, 2] = np.clip(interior[:, :, 2] + 1.00 * ocean_rim, 0, 1)

    # Crisp edge highlight along the cutaway boundary lines
    edge_line = (
        np.exp(-((nx - 0.0) / 0.010)**2) * (ny > -0.62) * (ny < 0.72)
        + np.exp(-((ny + 0.62) / 0.010)**2) * (nx > 0.0)
        + np.exp(-((ny - 0.72) / 0.010)**2) * (nx > 0.0)
    ) * (r <= 0.99)
    interior[:, :, 0] = np.clip(interior[:, :, 0] + 0.45 * edge_line, 0, 1)
    interior[:, :, 1] = np.clip(interior[:, :, 1] + 0.35 * edge_line, 0, 1)
    interior[:, :, 2] = np.clip(interior[:, :, 2] + 0.20 * edge_line, 0, 1)

    comp_globe = g_arr * (1.0 - cut_wedge[:, :, None]) + interior * cut_wedge[:, :, None]
    globe_im = Image.fromarray((np.clip(comp_globe, 0, 1) * 255).astype(np.uint8))
    mask_im = Image.fromarray((in_sphere * 255).astype(np.uint8))
    im.paste(globe_im, (int(cx - R), int(cy - R)), mask_im)

    hook_box = draw_top_band_text(im, ["WATER", "DEEP", "BELOW"], {"WATER"}, font_size=96, y=34)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "A",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "Titan Hides an Ocean Under Its Ice (And Seas of Natural Gas on Top)",
        "text": "WATER DEEP BELOW",
        "yellow_word": "WATER",
        "source_id": "PIA14602",
        "source_credit": "NASA/JPL-Caltech/Space Science Institute",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def build_arm_b(huygens_src: Path, out_path: Path) -> dict:
    # PIA07232_surface_source.jpg (546x693): Real Huygens DISR surface frame (rounded ice pebbles, orange ground).
    # Spec: "The real Huygens surface frame (rounded ice pebbles, orange ground), graded hot, full bleed"
    # Text: "72 MINUTES"
    src = Image.open(huygens_src).convert("RGB")
    # Crop the real Huygens pebble field (excluding white border around PIA07232)
    crop = src.crop((120, 330, 424, 501)).resize((W, H), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(crop).enhance(1.38)
    im = ImageEnhance.Color(im).enhance(1.28)
    im = ImageEnhance.Brightness(im).enhance(1.06)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=75, threshold=3))

    hook_box = draw_top_band_text(im, ["72", "MINUTES"], {"72"}, font_size=112, y=32)
    im.save(out_path, quality=95, subsampling=0, optimize=True)
    return {
        "arm": "B",
        "file": out_path.name,
        "sha256": sha256(out_path),
        "title": "We Landed on Titan Once (And It's Still Our Most Distant Landing)",
        "text": "72 MINUTES",
        "yellow_word": "72",
        "source_id": "PIA07232",
        "source_credit": "NASA/JPL/ESA/University of Arizona",
        "hook_box": hook_box,
        "score": score_thumb(out_path, "long"),
    }

def main():
    titan_src = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Thumbnails/J2144_v01/PIA14602.jpg")
    huygens_src = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Thumbnails/J2144_v02/PIA07232_surface_source.jpg")
    nas_dir = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/08_Thumbnail/j2417_v01")
    local_dir = REPO / "02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/08_Thumbnail/j2417_v01"
    stage = Path("/private/tmp/j2430_out/032")
    stage.mkdir(parents=True, exist_ok=True)

    a_file = stage / "032_j2417_A_water_deep_below_v01.jpg"
    b_file = stage / "032_j2417_B_72_minutes_v01.jpg"
    res_a = build_arm_a(titan_src, a_file)
    res_b = build_arm_b(huygens_src, b_file)

    preview_sheet = stage / "032_j2417_preview_sheet_v01.jpg"
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
        "film": "OWB:032",
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
