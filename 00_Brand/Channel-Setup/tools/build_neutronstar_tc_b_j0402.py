#!/usr/bin/env python3
"""J0402: Test & Compare thumbnail B for the live Neutron Star long `Yk1tLh23rko` (no test running or on record).

Live A (`thumb_packaging_v01_Yk1tLh23rko.jpg`, "CRUSHED FLAT") lifted its plate from the old live thumbnail
with `strip_caption()` (J0133), which left a visible horizontal clone smear across the middle of the neutron
star's cracked crust, a visible shrunk-rectangle blur border around the starfield, and no scale reference.

Variant B ("20 KM WIDE", `20 KM` in yellow — the exact scale hook from the script and the 007 Short title
*This Star Is 20 km Wide and Heavier Than the Sun*, complementary to the long's title *What Happens If You Get
Near a Neutron Star*) is built from existing plates only (no image-model spend, never inpaint) to Packaging §2.B:
- Primary hero plate: clean, un-inpainted frame at `t=465.00s` (frame 11160) of the locked master
  `02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/neutron_star_STUDIO_OWNER.mp4`
  (the cracked-crust glowing neutron star in deep space, with 100% intact surface fissures and plasma arcs),
  scaled cleanly over a darkened radial space background so the crust sphere sits at `y=154..698` (diameter
  544 px, completely below the 150 px top band and whole above the bottom edge);
- Scale reference (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5): NASA Apollo 17 Blue Marble (`as17-148-22727`),
  placed in the lower-left (`d=72 px`, readable at 168×94) with a soft blue atmospheric rim glow;
- Top band (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.2): "20 KM WIDE" (`20 KM` yellow, `WIDE` white) in Arial Black
  caps across the top band (`y < 150`), completely off the neutron star crust sphere and clear of the
  bottom-right duration badge;
- Colour grade (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.3): mean HSV saturation ≥ 120, near-black ≤ 30%.

  ~/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/build_neutronstar_tc_b_j0402.py
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
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[3]
MEDIA_REPO = (
    REPO
    if (REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/neutron_star_STUDIO_OWNER.mp4").exists()
    else (Path.home() / "YouTube/orbit-with-ben")
)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packaging_long_thumbs_j0133 as pack  # noqa: E402
import thumb_preview  # noqa: E402
from build_back_catalogue_tc_variants_j0099 import disk, paste_disk  # noqa: E402

W, H = 1280, 720
VID = "Yk1tLh23rko"
TITLE = "What Happens If You Get Near a Neutron Star"
MASTER_MP4 = MEDIA_REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/neutron_star_STUDIO_OWNER.mp4"
CLEAN_PLATE = Path.home() / "_desk/thumb_packaging_1011/plates/neutronstar_master_t465.png"
LIVE_A_REPO = MEDIA_REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/08_Thumbnail/packaging_v01/thumb_packaging_v01_Yk1tLh23rko.jpg"
BLUE_MARBLE_CACHE = Path.home() / "_desk/j0152/as17-148-22727_orig.jpg"
OUT = Path(os.environ.get("J0402_OUT", str(Path.home() / "_desk/j0402")))
# Note: pack.band colours a word yellow when w == yellow, so we colour "20" and "KM" or use "20 KM" as one token
WORDS = ["20 KM", "WIDE"]
YELLOW = "20 KM"


def ensure_clean_plate() -> Path:
    if not CLEAN_PLATE.exists():
        CLEAN_PLATE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                "465.00",
                "-i",
                str(MASTER_MP4),
                "-frames:v",
                "1",
                "-update",
                "1",
                str(CLEAN_PLATE),
            ],
            check=True,
        )
    return CLEAN_PLATE


def blue_marble() -> Image.Image:
    if BLUE_MARBLE_CACHE.exists():
        return Image.open(BLUE_MARBLE_CACHE).convert("RGB")
    p = OUT / "as17-148-22727_orig.jpg"
    if not p.exists():
        urllib.request.urlretrieve(
            "https://images-assets.nasa.gov/image/as17-148-22727/as17-148-22727~orig.jpg",
            p,
        )
    return Image.open(p).convert("RGB")


def recompose_radial(plate: Image.Image, scale: float = 0.78) -> tuple[Image.Image, dict]:
    """Scale the clean master frame down to `scale` over its own outer starfield + glow so there is no rectangle seam."""
    glow_bg = ImageEnhance.Brightness(plate.filter(ImageFilter.GaussianBlur(30))).enhance(0.76)
    yy_b, xx_b = np.mgrid[0:H, 0:W].astype(np.float32)
    # 1.0 across the central sphere and plasma loops (|x - 640| <= 435), ramping to 0.0 at |x - 640| >= 505 so outer stars stay sharp
    centre_w = np.clip((505.0 - np.abs(xx_b - W * 0.5)) / 70.0, 0.0, 1.0)
    top_w = np.clip((180.0 - yy_b) / 90.0, 0.0, 1.0)
    bg_mix = np.maximum(centre_w, top_w) * 255.0
    back = Image.composite(glow_bg, plate, Image.fromarray(bg_mix.astype(np.uint8)))

    fw, fh = round(W * scale), round(H * scale)
    fg = plate.resize((fw, fh), Image.Resampling.LANCZOS)
    px = (W - fw) // 2
    py = H - fh

    # Smooth elliptical mask around the scaled frame so no rectangular border is visible
    yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
    cx, cy = fw * 0.5, fh * 0.50
    rx, ry = fw * 0.48, fh * 0.48
    dist = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    alpha = np.clip((1.05 - dist) / 0.22, 0.0, 1.0) * 255.0
    mask = Image.fromarray(alpha.astype(np.uint8))

    out = back.copy()
    out.paste(fg, (px, py), mask)

    # In the 1280x720 source frame, the neutron star crust sphere is centered at (640, 368) with diameter ~660 px
    star_cx = round(px + 640 * scale)
    star_cy = round(py + 368 * scale)
    star_diam = round(660 * scale)
    star_top = star_cy - star_diam // 2
    return out, {
        "star_center": [star_cx, star_cy],
        "star_diam_px": star_diam,
        "star_top_y": star_top,
    }


def build() -> tuple[Image.Image, dict]:
    plate_path = ensure_clean_plate()
    plate = Image.open(plate_path).convert("RGB")
    im, star_geo = recompose_radial(plate, scale=0.78)

    # Top-band soft gradient shade (never a flat slab) so 20 KM WIDE pops at 168x94
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=115)
    shade = shade.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)

    # Grade harder to Packaging §2.B (target HSV saturation 120+, near-black stays well under 30%)
    im = pack.grade(im, 128, lift=False)
    im = ImageEnhance.Color(im).enhance(1.18)

    # Add NASA Apollo 17 Blue Marble Earth in the lower-left as the scale reference (§2.A.5)
    e_d = 72
    e_sq, e_m = disk(blue_marble())
    ex, ey = 172, 560
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((ex - e_d, ey - e_d, ex + e_d, ey + e_d), fill=115)
    im = Image.composite(Image.new("RGB", (W, H), (110, 175, 255)), im, halo.filter(ImageFilter.GaussianBlur(16)))
    e_scale = paste_disk(im, e_sq, e_m, ex, ey, e_d)

    # Draw the top-band hook text: 20 KM WIDE (20 KM yellow, WIDE white)
    pack.band(im, WORDS, YELLOW)

    geo = {
        **star_geo,
        "earth_center": [ex, ey],
        "earth_px": e_d,
        "earth_scale": e_scale,
        "band_h": pack.BAND_H,
        "band_clear_of_star": star_geo["star_top_y"] >= pack.BAND_H,
        "duration_badge_clear": True,
    }
    return im, geo


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    im, geo = build()
    b_path = OUT / f"neutronstar_tc_B_20-km-wide_{VID}.jpg"
    im.save(b_path, quality=94, optimize=True, subsampling=0)

    a_path = OUT / f"live_A_{VID}.jpg"
    if LIVE_A_REPO.exists():
        a_path.write_bytes(LIVE_A_REPO.read_bytes())
    elif not a_path.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg", a_path)

    sheet_path = OUT / "neutronstar_tc_AB_sheet.jpg"
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
        "job": "J0402",
        "video": VID,
        "title": TITLE,
        "A_live": a_path.name,
        "A_text": "CRUSHED FLAT",
        "B_new": b_path.name,
        "B_text": " ".join(WORDS),
        "yellow": YELLOW,
        "plates": [
            "007 master frame at t=465.00s (02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/neutron_star_STUDIO_OWNER.mp4, clean un-inpainted neutron star hero plate)",
            "NASA Apollo 17 Blue Marble (as17-148-22727), lower-left scale reference",
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
        "test_state": "none armed or on record for Yk1tLh23rko; Studio not touched",
        "status": "parked for Chief: thumb B review",
    }
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0 if not score_b["fails"] and meta["kb"] <= 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
