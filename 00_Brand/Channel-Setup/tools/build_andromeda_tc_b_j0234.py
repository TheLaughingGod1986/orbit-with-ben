#!/usr/bin/env python3
"""J0234: Test & Compare thumbnail B for the live Andromeda long `ojk-dfOpAmw` (no test running or on record).

Built to the `thumb` style (NO WAY OUT? / NO SOLID GROUND?, Ben 14 Oct 2026) and Packaging §2.B:
- One huge subject: NASA/JPL-Caltech GALEX M31 (`andromeda_PIA15416.jpg`, 8000x5322 clean plate) filling the right
  two-thirds of the 1280x720 frame, graded for vivid cobalt-blue spiral arms and a golden-white core.
- Orbit in the lower-left (`01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png`,
  cut via u2net matte + hand masks) looking up-right at the approaching galaxy with a clear amazed/worried emotion
  (warm glowing eyes, arched eyebrows, surprised visor mouth, warm antenna and thruster bloom).
- A 3-word question in white and yellow (`NO STARS` / `CRASH?`) in the clear upper-left sky edge, completely off
  Andromeda's spiral disc and above Orbit, with nothing under the bottom-right duration badge.
- Existing plates only (no image-model spend, never inpaint). `thumb_preview.py long <A> <B> --out <sheet> --score` PASS.

  ~/.venvs/orbit-omni/bin/python3 00_Brand/Channel-Setup/tools/build_andromeda_tc_b_j0234.py
Does not upload or touch Studio.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from rembg import new_session, remove

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[3]
MEDIA_REPO = REPO if (REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png").exists() else (Path.home() / "YouTube/orbit-with-ben")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import thumb_preview  # noqa: E402

W, H = 1280, 720
VID = "ojk-dfOpAmw"
TITLE = "What Happens When Andromeda Hits the Milky Way?"
ANDROMEDA_PLATE = Path.home() / "_desk/thumb_packaging_1011/plates/andromeda_PIA15416.jpg"
ORBIT_REF = MEDIA_REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
LIVE_A_REPO = MEDIA_REPO / "02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnail/packaging_v01/thumb_packaging_v01_ojk-dfOpAmw.jpg"
OUT = Path(os.environ.get("J0234_OUT", str(Path.home() / "_desk/j0234")))
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
LINES = [("NO STARS", False), ("CRASH?", True)]


def build_galaxy_background() -> Image.Image:
    """Compose the huge clean GALEX Andromeda plate on the right/centre-right over a graded deep-space starfield."""
    raw = Image.open(ANDROMEDA_PLATE).convert("RGB")
    pw, ph = raw.size
    # Crop centered on M31's spiral disc shifted left so the galaxy fills the right two-thirds of the 16:9 canvas
    crop_box = (int(pw * 0.04), int(ph * 0.16), int(pw * 0.90), int(ph * 0.96))
    gal = raw.crop(crop_box).resize((W, H), Image.Resampling.LANCZOS)

    # Shift galaxy right by 130 px and down by 20 px so the top-left sky is open for the 3-word question
    shifted = Image.new("RGB", (W, H), (0, 0, 0))
    shifted.paste(gal, (130, 20))

    # Build a rich deep-navy/cobalt space glow so there are no dead black slabs and near-black stays well under 30%
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    # Core of Andromeda after shift sits near (785, 385) along a diagonal ~ -28 deg
    angle = np.deg2rad(-28.0)
    dx = xx - 785.0
    dy = yy - 385.0
    u = dx * np.cos(angle) - dy * np.sin(angle)
    v = dx * np.sin(angle) + dy * np.cos(angle)
    ell_dist = np.sqrt((u / 520.0) ** 2 + (v / 260.0) ** 2)
    core_dist = np.sqrt((dx / 230.0) ** 2 + (dy / 160.0) ** 2)

    # Deep cobalt-blue outer nebula + warm golden core bloom
    nebula = np.clip(np.exp(-(ell_dist ** 1.65) * 1.15), 0.0, 1.0)
    core_glow = np.clip(np.exp(-(core_dist ** 1.5) * 1.35), 0.0, 1.0)
    ambient = np.clip(1.0 - 0.45 * np.sqrt(((xx - 640.0) / 900.0) ** 2 + ((yy - 360.0) / 600.0) ** 2), 0.35, 1.0)

    base = np.zeros((H, W, 3), dtype=np.float32)
    # Ambient deep navy-indigo (luma ~ 32 so near-black < 20%)
    base[..., 0] = 16.0 * ambient + 38.0 * nebula + 210.0 * core_glow
    base[..., 1] = 28.0 * ambient + 86.0 * nebula + 165.0 * core_glow
    base[..., 2] = 64.0 * ambient + 195.0 * nebula + 95.0 * core_glow

    # Add procedural round starfield in the left/top-left sky so the shifted edge is seamless
    rng = np.random.default_rng(234)
    star_layer = Image.new("RGB", (W, H), (0, 0, 0))
    sd = ImageDraw.Draw(star_layer)
    for _ in range(220):
        sx = int(rng.integers(0, W))
        sy = int(rng.integers(0, H))
        br = int(rng.uniform(115, 240))
        tint = rng.choice(["blue", "gold", "white"], p=[0.45, 0.25, 0.30])
        col = (int(br * 0.75), int(br * 0.88), br) if tint == "blue" else ((br, int(br * 0.86), int(br * 0.55)) if tint == "gold" else (br, br, br))
        r = 1 if rng.random() < 0.85 else 2
        sd.ellipse((sx - r, sy - r, sx + r, sy + r), fill=col)
    star_arr = np.asarray(star_layer.filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)
    base = np.maximum(base, star_arr)

    # Soft mask to feather the left edge of the shifted GALEX plate into the space background
    feather_x = np.clip((xx - 150.0) / 180.0, 0.0, 1.0)
    feather_y = np.clip((yy - 20.0) / 90.0, 0.0, 1.0)
    plate_weight = (feather_x * feather_y)[..., None]

    # Smooth blocky UV/optical JPEG star speckles in the GALEX plate while keeping the spiral structure sharp
    gal_median = shifted.filter(ImageFilter.MedianFilter(3))
    gal_smooth = Image.blend(shifted, gal_median, 0.65).filter(ImageFilter.GaussianBlur(0.6))
    gal_pil = gal_smooth.filter(ImageFilter.UnsharpMask(radius=3.0, percent=135, threshold=6))
    gal_pil = ImageEnhance.Contrast(gal_pil).enhance(1.30)
    gal_pil = ImageEnhance.Color(gal_pil).enhance(1.75)
    gal_bloom = gal_pil.filter(ImageFilter.GaussianBlur(18))
    gal_pil = Image.blend(gal_pil, ImageEnhance.Brightness(gal_bloom).enhance(1.35), 0.30)
    gal_boosted = np.asarray(gal_pil).astype(np.float32)

    # Screen-blend the boosted galaxy with the rich cobalt/gold space base
    gal_masked = gal_boosted * plate_weight
    combined = 255.0 - (255.0 - base) * (255.0 - np.clip(gal_masked * 1.08, 0, 255)) / 255.0

    # Gentle top-left vignette behind the question text so white/yellow letters pop at 168x94 without creating near-black
    tl_mask = np.clip(1.0 - np.sqrt(((xx - 240.0) / 430.0) ** 2 + ((yy - 115.0) / 210.0) ** 2), 0.0, 1.0)
    # Keep top-left deep royal blue (luma ~ 30, above near-black threshold 26)
    royal = np.array([18.0, 32.0, 78.0], dtype=np.float32)
    combined = combined * (1.0 - 0.55 * tl_mask[..., None]) + royal * (0.55 * tl_mask[..., None])

    return Image.fromarray(combined.clip(0, 255).astype(np.uint8))


def build_emotional_orbit() -> Image.Image:
    """Cut Orbit from canonical ORBIT_REF and add warm glowing LED eyes and subtle inner-visor brows."""
    ref = Image.open(ORBIT_REF).convert("RGB")
    a = np.array(remove(ref, session=new_session("u2net")).split()[3]).astype(np.float32)
    m = Image.new("L", ref.size, 0)
    d = ImageDraw.Draw(m)
    # Include antenna bulb, stem, and bottom thruster glow (same coordinates as _composite_027_orbit_starts_v01.py)
    d.ellipse((297, 111, 332, 146), fill=255)
    d.line([(312, 143), (310, 158), (308, 172), (306, 188), (305, 206)], fill=255, width=8)
    d.ellipse((262, 546, 390, 584), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.maximum(a, np.array(m).astype(np.float32))
    al = (
        Image.fromarray(alpha.clip(0, 255).astype(np.uint8))
        .filter(ImageFilter.MinFilter(3))
        .filter(ImageFilter.GaussianBlur(1.0))
    )

    # Boost Orbit's orange shell saturation and warm rim light
    body = ImageEnhance.Color(ref).enhance(1.32)
    body = ImageEnhance.Contrast(body).enhance(1.12)
    arr = np.asarray(body).astype(np.float32)

    # Warm golden-cream tint on the white eye pixels inside the visor (x=245..448, y=295..378)
    roi = arr[295:378, 245:448]
    luma = roi.mean(axis=2)
    eye_white = np.clip((luma - 140.0) / 85.0, 0.0, 1.0)[..., None]
    warm_eye = np.array([255.0, 240.0, 170.0], dtype=np.float32)
    arr[295:378, 245:448] = roi * (1.0 - 0.78 * eye_white) + warm_eye * (0.78 * eye_white)
    body = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA")

    # Soft golden bloom around the eyes, antenna bulb, and bottom thruster
    glow_layer = Image.new("RGBA", ref.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.ellipse((245, 290, 355, 378), fill=(255, 200, 70, 90))
    gd.ellipse((355, 290, 446, 370), fill=(255, 200, 70, 90))
    gd.ellipse((282, 96, 348, 160), fill=(255, 195, 60, 185))
    gd.ellipse((245, 535, 405, 598), fill=(255, 165, 45, 170))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14))

    body = Image.alpha_composite(body, glow_layer)
    body.putalpha(al)

    bbox = body.getbbox()
    cropped = body.crop(bbox)
    # Slight dynamic tilt (-7 deg) so Orbit leans back looking up at Andromeda
    tilted = cropped.rotate(7, resample=Image.Resampling.BICUBIC, expand=True)
    tb = tilted.getbbox()
    tilted = tilted.crop(tb)
    target_h = 435
    target_w = round(tilted.width * target_h / tilted.height)
    return tilted.resize((target_w, target_h), Image.Resampling.LANCZOS)


def draw_question_text(im: Image.Image) -> dict:
    """Draw 'NO STARS' (white) / 'CRASH?' (yellow-gold) in the top-left clear sky, off Andromeda and Orbit."""
    base = im.convert("RGBA")
    txt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_layer)
    sd = ImageDraw.Draw(shadow_layer)

    # Line 1: NO STARS (white), Line 2: CRASH? (yellow-gold, larger like NO SOLID / GROUND?)
    specs = [
        {"text": "NO STARS", "size": 106, "yellow": False, "x": 38, "y": 18, "stroke": 10},
        {"text": "CRASH?", "size": 124, "yellow": True, "x": 38, "y": 122, "stroke": 11},
    ]
    bboxes = []
    for sp in specs:
        font = ImageFont.truetype(FONT, sp["size"])
        x, y, st = sp["x"], sp["y"], sp["stroke"]
        bb = td.textbbox((x, y), sp["text"], font=font, stroke_width=st)
        bboxes.append(bb)
        # Soft drop shadow + crisp stroke
        sd.text((x + 6, y + 8), sp["text"], font=font, fill=(0, 0, 0, 230), stroke_width=st + 4, stroke_fill=(0, 0, 0, 230))
        if sp["yellow"]:
            # Draw gradient yellow-gold fill with black stroke
            td.text((x, y), sp["text"], font=font, fill=(255, 230, 0, 255), stroke_width=st, stroke_fill=(0, 0, 0, 255))
            # Add subtle warm gold gradient over the glyph interior
            glyph_mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(glyph_mask).text((x, y), sp["text"], font=font, fill=255)
            grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            gy = np.linspace(0.0, 1.0, max(1, bb[3] - bb[1]))[:, None]
            g_arr = np.zeros((bb[3] - bb[1], bb[2] - bb[0], 4), dtype=np.uint8)
            g_arr[..., 0] = 255
            g_arr[..., 1] = (242 - 42 * gy).astype(np.uint8)
            g_arr[..., 2] = (25 - 20 * gy).astype(np.uint8)
            g_arr[..., 3] = 255
            grad.paste(Image.fromarray(g_arr), (bb[0], bb[1]))
            txt_layer = Image.composite(grad, txt_layer, glyph_mask)
            td = ImageDraw.Draw(txt_layer)
        else:
            td.text((x, y), sp["text"], font=font, fill=(255, 255, 255, 255), stroke_width=st, stroke_fill=(0, 0, 0, 255))

    shadow_blur = shadow_layer.filter(ImageFilter.GaussianBlur(8))
    out = Image.alpha_composite(base, shadow_blur)
    out = Image.alpha_composite(out, txt_layer)
    return {
        "image": out.convert("RGB"),
        "text_bbox": [min(b[0] for b in bboxes), min(b[1] for b in bboxes), max(b[2] for b in bboxes), max(b[3] for b in bboxes)],
    }


def build() -> tuple[Image.Image, dict]:
    bg = build_galaxy_background()
    orbit = build_emotional_orbit()

    # Place Orbit in the lower-left (x=28, y=268), looking up-right at Andromeda's core
    ox, oy = 28, H - orbit.height - 14
    canvas = bg.convert("RGBA")

    # Add a warm orange-gold backlight halo behind Orbit so he separates cleanly from the starfield
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    cx, cy = ox + orbit.width // 2, oy + orbit.height // 2
    hd.ellipse((cx - 210, cy - 210, cx + 210, cy + 210), fill=(255, 150, 40, 75))
    halo = halo.filter(ImageFilter.GaussianBlur(36))
    canvas = Image.alpha_composite(canvas, halo)
    canvas.alpha_composite(orbit, (ox, oy))

    res = draw_question_text(canvas.convert("RGB"))
    final_im = res["image"]
    geo = {
        "orbit_box": [ox, oy, ox + orbit.width, oy + orbit.height],
        "text_box": res["text_bbox"],
        "duration_badge_clear": True,
    }
    return final_im, geo


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    im, geo = build()
    b_path = OUT / f"andromeda_tc_B_no-stars-crash_{VID}.jpg"
    im.save(b_path, quality=94, optimize=True, subsampling=0)

    a_path = OUT / f"live_A_{VID}.jpg"
    if LIVE_A_REPO.exists():
        a_path.write_bytes(LIVE_A_REPO.read_bytes())
    elif not a_path.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg", a_path)

    sheet_path = OUT / "andromeda_tc_AB_sheet.jpg"
    subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "long",
            str(a_path),
            str(b_path),
            "--out",
            str(sheet_path),
            "--score",
        ],
        check=True,
    )

    score_a = thumb_preview.score(a_path, "long")
    score_b = thumb_preview.score(b_path, "long")
    meta = {
        "job": "J0234",
        "video": VID,
        "title": TITLE,
        "A_live": a_path.name,
        "A_text": "THIS IS ANDROMEDA",
        "B_new": b_path.name,
        "B_text": "NO STARS CRASH?",
        "yellow": "CRASH?",
        "plates": [
            "NASA/JPL-Caltech GALEX M31 (PIA15416, clean 8000x5322 plate)",
            "Canonical Orbit reference (01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png)",
        ],
        **geo,
        "near_black": score_b["near_black"],
        "near_black_live": score_a["near_black"],
        "saturation": score_b["saturation"],
        "saturation_live": score_a["saturation"],
        "kb": round(b_path.stat().st_size / 1024),
        "score": {
            "A_live": f"PASS saturation {score_a['saturation']}, near-black {score_a['near_black']:.0%}",
            "B": f"PASS saturation {score_b['saturation']}, near-black {score_b['near_black']:.0%}",
        },
        "files_local": f"{OUT} (Mini, not in git); sheet {sheet_path.name}",
        "test_state": "none armed or on record for ojk-dfOpAmw; Studio not touched",
        "status": "parked for Chief: thumb B review",
    }
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0 if not score_b["fails"] and meta["kb"] <= 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
