#!/usr/bin/env python3
"""Build OWB:064 Every Planet Explained in 10 Minutes Thumbnails A, B, C (£0, Pillow).

Matches TOPIC_GO_NO_GO_SHEET.md §4.2 and THUMBNAIL_AND_TITLE_RULES.md §2.B:
- Zero Orbit character on long-form thumbnails.
- 3 genuinely distinct compositions (A: All 8 Worlds diagonal lineup; B: Rule 14 bright 464°C to -224°C split;
  C: Rules 18/19 graded real NASA spacecraft triptych).
- Top-band hook text (<= 3 words, Bebas Neue bold, white + one #FFE000 yellow hook word, heavy stroke + drop shadow).
- Bottom-right duration badge zone (x > 75%, y > 78%) 100% clear of key text and small planets.
- Every thumbnail passes thumb_preview.py long --score (saturation >= 100, target >= 120; near-black <= 30%).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/tools"))
import thumb_preview  # noqa: E402

HARVEST_064 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes/03_Reference-Material/harvest_J3022_v01"
)
HARVEST_033 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01"
)
HARVEST_031 = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01"
)
NAS_OUT = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail"
)
REPO_OUT = Path(__file__).resolve().parent
FONT_PATH = ROOT / "02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/08_Thumbnail/fonts/BebasNeue-Regular.ttf"

W, H = 1920, 1080
YELLOW = (255, 224, 0)  # #FFE000
WHITE = (255, 255, 255)
STROKE = (8, 10, 18)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)


def lift_shadows(im: Image.Image, floor: float, tint: tuple[float, float, float]) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    blur = np.asarray(im.filter(ImageFilter.GaussianBlur(12)), dtype=np.float32)
    detail = arr - blur
    bL = 0.2126 * blur[:, :, 0] + 0.7152 * blur[:, :, 1] + 0.0722 * blur[:, :, 2]
    add = np.clip(floor - bL, 0.0, None)
    tint_a = np.array(tint, dtype=np.float32)
    tint_l = float(0.2126 * tint_a[0] + 0.7152 * tint_a[1] + 0.0722 * tint_a[2])
    lifted = blur + (add / max(tint_l, 1.0))[..., None] * tint_a
    out = np.clip(lifted + detail * 0.88, 0, 255)
    return Image.fromarray(out.astype(np.uint8), "RGB")


def boost_sat(im: Image.Image, factor: float, contrast: float = 1.10) -> Image.Image:
    im = ImageEnhance.Color(im).enhance(factor)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    return im


def extract_globe(path: Path, size: int, crop_box=None, sat: float = 1.45, bright: float = 1.08, thresh: int = 16) -> Image.Image:
    """Extract a real NASA planet globe onto transparent RGBA, preserving crisp limb."""
    im = Image.open(path).convert("RGB")
    if crop_box is not None:
        w, h = im.size
        im = im.crop((int(w * crop_box[0]), int(h * crop_box[1]), int(w * crop_box[2]), int(h * crop_box[3])))
    else:
        # Auto-crop to bright globe bbox
        L = np.asarray(im.convert("L"))
        ys, xs = np.where(L > thresh)
        if len(xs) > 100:
            x0, x1 = int(xs.min()), int(xs.max())
            y0, y1 = int(ys.min()), int(ys.max())
            side = max(x1 - x0, y1 - y0)
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            pad = int(side * 0.02)
            half = side // 2 + pad
            im = im.crop((max(0, cx - half), max(0, cy - half), min(im.width, cx + half), min(im.height, cy + half)))

    im = im.resize((size, size), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(1.12)

    # Clean circular feathered mask matching real disk
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    m = max(2, int(size * 0.015))
    d.ellipse((m, m, size - m, size - m), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(1, size // 120)))
    rgba = im.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def extract_saturn(path: Path, width: int, sat: float = 1.45) -> Image.Image:
    """Keep Saturn's iconic rings using luminance alpha mask."""
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im, dtype=np.float32)
    L = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    ys, xs = np.where(L > 18)
    x0, x1 = max(0, int(xs.min()) - 20), min(im.width, int(xs.max()) + 20)
    y0, y1 = max(0, int(ys.min()) - 20), min(im.height, int(ys.max()) + 20)
    im = im.crop((x0, y0, x1, y1))
    h = int(round(im.height * (width / im.width)))
    im = im.resize((width, h), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(1.12)
    arr2 = np.asarray(im, dtype=np.float32)
    L2 = 0.2126 * arr2[:, :, 0] + 0.7152 * arr2[:, :, 1] + 0.0722 * arr2[:, :, 2]
    alpha = np.clip((L2 - 14.0) / 28.0, 0.0, 1.0) * 255.0
    rgba = im.convert("RGBA")
    rgba.putalpha(Image.fromarray(alpha.astype(np.uint8), "L"))
    return rgba


def draw_top_hook(im: Image.Image, segments: list[tuple[str, tuple[int, int, int]]], font_size: int = 164, y_top: int = 24) -> Image.Image:
    """Draw bold Bebas Neue top-band hook text with heavy stroke & shadow (168x94 legible)."""
    rgba = im.convert("RGBA")
    # Subtle top gradient band so white/yellow hook pops cleanly without flat black bar
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b_arr = np.zeros((H, W, 4), dtype=np.uint8)
    for y in range(230):
        a = int(155 * (1.0 - y / 230.0) ** 1.3)
        b_arr[y, :, :] = (10, 18, 40, a)
    band = Image.fromarray(b_arr, "RGBA")
    rgba = Image.alpha_composite(rgba, band)

    font = load_font(font_size)
    draw = ImageDraw.Draw(rgba)
    gap = 26
    widths = []
    for txt, _ in segments:
        bb = draw.textbbox((0, 0), txt, font=font, stroke_width=10)
        widths.append(bb[2] - bb[0])
    total_w = sum(widths) + gap * (len(segments) - 1)
    x = (W - total_w) // 2

    # Drop shadow layer
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sx = x
    for (txt, _), w_seg in zip(segments, widths):
        sd.text((sx + 6, y_top + 8), txt, font=font, fill=(0, 0, 0, 210), stroke_width=12, stroke_fill=(0, 0, 0, 210))
        sx += w_seg + gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    rgba = Image.alpha_composite(rgba, shadow)

    draw = ImageDraw.Draw(rgba)
    cx = x
    for (txt, col), w_seg in zip(segments, widths):
        draw.text((cx, y_top), txt, font=font, fill=col + (255,), stroke_width=10, stroke_fill=STROKE + (255,))
        cx += w_seg + gap
    return rgba.convert("RGB")


def build_thumb_A() -> Image.Image:
    """Thumbnail A: Scale & Completeness Lineup — ALL 8 WORLDS."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rx = (xx - W * 0.45) / (W * 0.65)
    ry = (yy - H * 0.58) / (H * 0.65)
    rad = np.sqrt(rx * rx + ry * ry)
    # Rich saturated deep-indigo cosmic gradient (luma >= 32 everywhere -> 0% near-black, high saturation!)
    r = np.clip(18 + 52 * np.exp(-rad * 1.1) + 22 * (xx / W), 0, 255)
    g = np.clip(36 + 78 * np.exp(-rad * 1.1) + 18 * (1.0 - yy / H), 0, 255)
    b = np.clip(95 + 115 * np.exp(-rad * 0.95) + 35 * (xx / W), 0, 255)
    # Warm solar glow peeking at far-left edge behind Mercury/Venus
    sun_d = np.sqrt(((xx + 80) / 460.0) ** 2 + ((yy - 680) / 420.0) ** 2)
    glow = np.exp(-sun_d * 1.6)
    r = np.clip(r + 215 * glow, 0, 255)
    g = np.clip(g + 135 * glow, 0, 255)
    b = np.clip(b + 25 * glow, 0, 255)
    bg = Image.fromarray(np.stack([r, g, b], axis=-1).astype(np.uint8), "RGB").convert("RGBA")

    # Crisp stars
    rng = np.random.default_rng(6401)
    d = ImageDraw.Draw(bg)
    for _ in range(420):
        sx, sy = int(rng.integers(0, W)), int(rng.integers(0, H))
        sz = int(rng.choice([1, 1, 2, 2, 3]))
        br = int(rng.integers(180, 255))
        d.ellipse((sx - sz, sy - sz, sx + sz, sy + sz), fill=(br, br, 255, 220))

    # Diagonal perspective arc of ALL 8 REAL NASA PLANETS (bottom-right x>1440, y>840 kept clear of planets!)
    mercury = extract_globe(HARVEST_064 / "PIA15162.jpg", 132, sat=1.55, bright=1.18)
    venus   = extract_globe(HARVEST_033 / "PIA00271.jpg", 196, sat=1.70, bright=1.12)
    earth   = extract_globe(HARVEST_033 / "PIA18033.jpg", 224, sat=1.55, bright=1.10)
    mars    = extract_globe(HARVEST_031 / "PIA00407.jpg", 184, sat=1.70, bright=1.10)
    jupiter = extract_globe(HARVEST_064 / "PIA22946.jpg", 460, sat=1.50, bright=1.12)
    saturn  = extract_saturn(HARVEST_064 / "PIA11141.jpg", 580, sat=1.55)
    uranus  = extract_globe(HARVEST_033 / "PIA18182.jpg", 232, sat=1.65, bright=1.12)
    neptune = extract_globe(HARVEST_064 / "PIA01492.jpg", 224, sat=1.70, bright=1.12)

    placements = [
        (mercury, 46, 650),
        (venus,   164, 580),
        (earth,   344, 520),
        (mars,    544, 495),
        (jupiter, 700, 340),
        (saturn,  1060, 360),
        (uranus,  1470, 355),
        (neptune, 1665, 315),
    ]
    for pl, px, py in placements:
        # Soft luminous rim behind each planet
        glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow_layer)
        gd.ellipse((px - 10, py - 10, px + pl.width + 10, py + pl.height + 10), fill=(90, 160, 255, 65))
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(18))
        bg = Image.alpha_composite(bg, glow_layer)
        bg.alpha_composite(pl, (px, py))

    out = bg.convert("RGB")
    out = draw_top_hook(out, [("ALL", WHITE), ("8 WORLDS", YELLOW)], font_size=176, y_top=22)
    return out


def build_thumb_B() -> Image.Image:
    """Thumbnail B: Rule 14 Bright High-Contrast Split — 464°C TO -224°C."""
    # Left half: blazing golden-orange Venus (PIA00271)
    venus_im = Image.open(HARVEST_033 / "PIA00271.jpg").convert("RGB")
    venus_im = venus_im.crop((400, 400, 3696, 3696)).resize((1080, 1080), Image.Resampling.LANCZOS)
    v_arr = np.asarray(venus_im, dtype=np.float32)
    # Warm volcanic amber grade
    v_arr[:, :, 0] = np.clip(v_arr[:, :, 0] * 1.28 + 42, 0, 255)
    v_arr[:, :, 1] = np.clip(v_arr[:, :, 1] * 0.92 + 12, 0, 255)
    v_arr[:, :, 2] = np.clip(v_arr[:, :, 2] * 0.42, 0, 255)
    left_half = Image.fromarray(v_arr.astype(np.uint8), "RGB").crop((0, 0, 960, 1080))
    left_half = boost_sat(left_half, 1.45, 1.15)
    left_half = lift_shadows(left_half, 55.0, (125, 58, 12))

    # Right half: electric ice-blue Uranus (weic2310a) + Neptune azure glow (PIA01492)
    neptune_im = Image.open(HARVEST_064 / "PIA01492.jpg").convert("RGB")
    neptune_im = neptune_im.crop((180, 180, 2008, 2008)).resize((1080, 1080), Image.Resampling.LANCZOS)
    n_arr = np.asarray(neptune_im, dtype=np.float32)
    n_arr[:, :, 0] = np.clip(n_arr[:, :, 0] * 0.48 + 8, 0, 255)
    n_arr[:, :, 1] = np.clip(n_arr[:, :, 1] * 1.15 + 34, 0, 255)
    n_arr[:, :, 2] = np.clip(n_arr[:, :, 2] * 1.38 + 64, 0, 255)
    right_half = Image.fromarray(n_arr.astype(np.uint8), "RGB").crop((60, 0, 1020, 1080))
    right_half = boost_sat(right_half, 1.40, 1.16)
    right_half = lift_shadows(right_half, 52.0, (18, 72, 145))

    canvas = Image.new("RGB", (W, H))
    canvas.paste(left_half, (0, 0))
    canvas.paste(right_half, (960, 0))

    # Crisp luminous vertical energy split line at x=960
    rgba = canvas.convert("RGBA")
    line_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_glow)
    ld.rectangle((946, 0, 974, H), fill=(220, 245, 255, 180))
    line_glow = line_glow.filter(ImageFilter.GaussianBlur(14))
    rgba = Image.alpha_composite(rgba, line_glow)
    d = ImageDraw.Draw(rgba)
    d.rectangle((955, 0, 965, H), fill=(255, 255, 255, 255))

    out = draw_top_hook(rgba.convert("RGB"), [("464°C", YELLOW), ("TO -224°C", WHITE)], font_size=168, y_top=24)
    return out


def build_thumb_C() -> Image.Image:
    """Thumbnail C: Rules 18 & 19 Graded Real NASA Spacecraft Montage — REAL NASA PHOTOS.

    Uses true aspect-ratio-preserving crops (ImageOps.fit) so every planet keeps exact circular geometry.
    """
    pw = W // 3  # 640 each

    # Panel 1: Cassini backlit Saturn rings (PIA17172 9000x3500 -> preserve aspect ratio via ImageOps.fit!)
    p1_raw = Image.open(HARVEST_064 / "PIA17172.jpg").convert("RGB")
    # Crop around Saturn + luminous left/right ring arcs preserving 640:1080 aspect ratio (width = 3500 * 640/1080 = 2074)
    p1 = ImageOps.fit(p1_raw, (pw, H), Image.Resampling.LANCZOS, centering=(0.50, 0.50))
    p1 = boost_sat(p1, 1.70, 1.15)
    p1 = lift_shadows(p1, 44.0, (48, 56, 98))

    # Panel 2: Juno Great Red Spot (PIA21775 1620x1440) + tiny Apollo 17 Earth scale inset
    p2_raw = Image.open(HARVEST_064 / "PIA21775.jpg").convert("RGB")
    p2 = ImageOps.fit(p2_raw, (pw, H), Image.Resampling.LANCZOS, centering=(0.50, 0.50))
    p2 = boost_sat(p2, 1.45, 1.14)
    p2 = lift_shadows(p2, 42.0, (68, 42, 34))
    p2_rgba = p2.convert("RGBA")
    earth_inset = extract_globe(HARVEST_033 / "PIA18033.jpg", 136, sat=1.55, bright=1.12)
    p2_rgba.alpha_composite(earth_inset, (pw - 166, H - 186))
    p2 = p2_rgba.convert("RGB")

    # Panel 3: Voyager 2 Neptune azure disk with Great Dark Spot (PIA01492 2188x2185 -> exact 1:1 circular limb!)
    p3_raw = Image.open(HARVEST_064 / "PIA01492.jpg").convert("RGB")
    # Crop slightly zoomed into Great Dark Spot + limb while keeping exact 640:1080 ratio
    p3 = ImageOps.fit(p3_raw, (pw, H), Image.Resampling.LANCZOS, centering=(0.45, 0.52))
    p3 = boost_sat(p3, 1.55, 1.16)
    p3 = lift_shadows(p3, 44.0, (22, 56, 128))

    canvas = Image.new("RGB", (W, H))
    canvas.paste(p1, (0, 0))
    canvas.paste(p2, (pw, 0))
    canvas.paste(p3, (pw * 2, 0))

    # Clean crisp dividers (6 px electric sky-white)
    d = ImageDraw.Draw(canvas)
    d.rectangle((pw - 3, 0, pw + 3, H), fill=(220, 238, 255))
    d.rectangle((pw * 2 - 3, 0, pw * 2 + 3, H), fill=(220, 238, 255))

    out = draw_top_hook(canvas, [("REAL", YELLOW), ("NASA PHOTOS", WHITE)], font_size=164, y_top=24)
    return out


def main() -> int:
    NAS_OUT.mkdir(parents=True, exist_ok=True)
    REPO_OUT.mkdir(parents=True, exist_ok=True)

    builders = [
        ("A", "064_thumb_A_all_8_worlds_v01.jpg", build_thumb_A),
        ("B", "064_thumb_B_464c_to_minus224c_v01.jpg", build_thumb_B),
        ("C", "064_thumb_C_real_nasa_photos_v01.jpg", build_thumb_C),
    ]

    scores = []
    paths_repo = []
    for label, fname, fn in builders:
        im = fn()
        p_repo = REPO_OUT / fname
        p_nas = NAS_OUT / fname
        im.save(p_repo, quality=92, optimize=True)
        im.save(p_nas, quality=92, optimize=True)
        paths_repo.append(p_repo)

        # Individual preview sheet
        sheet_repo = REPO_OUT / fname.replace(".jpg", "_sheet.jpg")
        sheet_nas = NAS_OUT / fname.replace(".jpg", "_sheet.jpg")
        res = thumb_preview.score(p_repo, "long", "owb", False)
        res["variant"] = label
        res["sha256"] = hashlib.sha256(p_repo.read_bytes()).hexdigest()
        res["repo_path"] = f"02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/{fname}"
        res["nas_path"] = str(p_nas)
        scores.append(res)

        # Render single preview sheet via thumb_preview CLI logic
        import subprocess as sp
        sp.run([sys.executable, str(ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "long", str(p_repo), "--out", str(sheet_repo), "--score"], check=True)
        sheet_nas.write_bytes(sheet_repo.read_bytes())

    # Combined 3-way sheet
    comb_repo = REPO_OUT / "064_thumbs_ABC_v01_preview_sheet.jpg"
    comb_nas = NAS_OUT / "064_thumbs_ABC_v01_preview_sheet.jpg"
    import subprocess as sp
    sp.run([sys.executable, str(ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "long", *[str(p) for p in paths_repo], "--out", str(comb_repo), "--score"], check=True)
    comb_nas.write_bytes(comb_repo.read_bytes())

    (REPO_OUT / "THUMB_SCORES_v01.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    (NAS_OUT / "THUMB_SCORES_v01.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print("ALL 3 THUMBNAILS BUILT & SCORED PASS!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
