#!/usr/bin/env python3
"""J0386: Test & Compare thumbnail B for the live Last Star long `REXYxuLOBoI` (no test running or on record).

Live A (`thumb_packaging_v01_REXYxuLOBoI.jpg`, "LAST LIGHT") lifted its plate from the old live thumbnail
with `strip_caption()` (J0133), which left a visible horizontal clone smear across the middle of the red
dwarf star, a visible shrunk-rectangle blur border around the starfield, and no scale reference.

Variant B ("THEN DARK", `DARK` in yellow — the exact companion hook text named in `THUMBNAIL_AND_TITLE_RULES.md`
§2.3 for *What Happens When the Last Star Dies?*) is built from existing plates only (no image-model spend,
never inpaint) to Packaging §2.B:
- Primary hero plate: clean, un-inpainted frame at `t=243.00s` (frame 5832) of the locked master
  `02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4`
  (the flaring red dwarf star in deep space, with 100% intact surface flare filaments), shifted down 54 px
  full-width so the starfield stays crisp edge-to-edge (`y=166..675` for the red dwarf disc, completely
  below the 150 px top band and whole above the bottom edge);
- Scale reference (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5): NASA Apollo 17 Blue Marble (`as17-148-22727`),
  placed in the lower-left (`d=72 px`, readable at 168×94) with a soft blue atmospheric rim glow;
- Top band (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.2): "THEN DARK" (`DARK` yellow, `THEN` white) in Arial Black
  caps across the top band (`y < 150`), completely off the red dwarf disc and clear of the bottom-right
  duration badge;
- Colour grade (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.3): mean HSV saturation ≥ 120, near-black ≤ 30%.

  ~/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/build_laststar_tc_b_j0386.py
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
    if (REPO / "02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4").exists()
    else (Path.home() / "YouTube/orbit-with-ben")
)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packaging_long_thumbs_j0133 as pack  # noqa: E402
import thumb_preview  # noqa: E402
from build_back_catalogue_tc_variants_j0099 import disk, paste_disk  # noqa: E402

W, H = 1280, 720
VID = "REXYxuLOBoI"
TITLE = "What Happens When the Last Star Dies?"
MASTER_MP4 = MEDIA_REPO / "02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4"
CLEAN_PLATE = Path.home() / "_desk/thumb_packaging_1011/plates/laststar_master_t243.png"
LIVE_A_REPO = MEDIA_REPO / "02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnail/packaging_v01/thumb_packaging_v01_REXYxuLOBoI.jpg"
BLUE_MARBLE_CACHE = Path.home() / "_desk/j0152/as17-148-22727_orig.jpg"
OUT = Path(os.environ.get("J0386_OUT", str(Path.home() / "_desk/j0386")))
WORDS, YELLOW = ["THEN", "DARK"], "DARK"


def ensure_clean_plate() -> Path:
    if not CLEAN_PLATE.exists():
        CLEAN_PLATE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                "243.00",
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


def recompose_fullbleed(plate: Image.Image, dy: int = 54) -> tuple[Image.Image, dict]:
    """Shift the full-width 1280x720 clean master frame down by dy px so the starfield stays crisp edge-to-edge."""
    back = pack.cover(plate, W, H).filter(ImageFilter.GaussianBlur(18))
    back = ImageEnhance.Brightness(back).enhance(0.82)
    mask = Image.new("L", (W, H), 0)
    # Feather only the top seam (inside the top band y=dy..dy+48)
    arr_m = np.zeros((H, W), dtype=np.float32)
    for y in range(dy, H):
        arr_m[y, :] = min(1.0, (y - dy) / 48.0) * 255.0
    mask = Image.fromarray(arr_m.astype(np.uint8))
    shifted = Image.new("RGB", (W, H), (0, 0, 0))
    shifted.paste(plate.crop((0, 0, W, H - dy)), (0, dy))
    out = Image.composite(shifted, back, mask)
    # In the 1280x720 source frame, the red dwarf disc spans y=112..621 (diameter 509 px, centre (634, 366))
    star_cx = 634
    star_cy = 366 + dy
    star_diam = 509
    star_top = 112 + dy
    return out, {
        "star_center": [star_cx, star_cy],
        "star_diam_px": star_diam,
        "star_top_y": star_top,
    }


def build() -> tuple[Image.Image, dict]:
    plate_path = ensure_clean_plate()
    plate = Image.open(plate_path).convert("RGB")
    im, star_geo = recompose_fullbleed(plate, dy=54)

    # Top-band soft gradient shade (never a flat slab) so THEN DARK pops at 168x94
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=115)
    shade = shade.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)

    # Grade harder to Packaging §2.B (target HSV saturation 120+, lift deep navy so near-black stays well under 30%)
    im = pack.grade(im, 134, lift=True)
    im = ImageEnhance.Color(im).enhance(1.12)

    # Add NASA Apollo 17 Blue Marble Earth in the lower-left as the scale reference (§2.A.5)
    e_d = 72
    e_sq, e_m = disk(blue_marble())
    ex, ey = 172, 560
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((ex - e_d, ey - e_d, ex + e_d, ey + e_d), fill=115)
    im = Image.composite(Image.new("RGB", (W, H), (110, 175, 255)), im, halo.filter(ImageFilter.GaussianBlur(16)))
    e_scale = paste_disk(im, e_sq, e_m, ex, ey, e_d)

    # Draw the top-band hook text: THEN DARK (DARK yellow, THEN white)
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
    b_path = OUT / f"laststar_tc_B_then-dark_{VID}.jpg"
    im.save(b_path, quality=94, optimize=True, subsampling=0)

    a_path = OUT / f"live_A_{VID}.jpg"
    if LIVE_A_REPO.exists():
        a_path.write_bytes(LIVE_A_REPO.read_bytes())
    elif not a_path.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg", a_path)

    sheet_path = OUT / "laststar_tc_AB_sheet.jpg"
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
        "job": "J0386",
        "video": VID,
        "title": TITLE,
        "A_live": a_path.name,
        "A_text": "LAST LIGHT",
        "B_new": b_path.name,
        "B_text": " ".join(WORDS),
        "yellow": YELLOW,
        "plates": [
            "005 master frame at t=243.00s (02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4, clean un-inpainted red dwarf hero plate)",
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
        "test_state": "none armed or on record for REXYxuLOBoI; Studio not touched",
        "status": "parked for Chief: thumb B review",
    }
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0 if not score_b["fails"] and meta["kb"] <= 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
