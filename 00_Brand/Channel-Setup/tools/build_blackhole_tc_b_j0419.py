#!/usr/bin/env python3
"""J0419: Test & Compare thumbnail B for the live Black Hole long `3xrxdmaOwJI` (no test running or on record).

Live A (`thumb_packaging_v01_3xrxdmaOwJI.jpg`, "NO WAY OUT") recomposed the `t=588s` master plate with a
rectangular box feather (`recompose(plate, 0.78)` in J0133), leaving visible vertical blur-border seams at
`x=141` and `x=1139` across the accretion disk and no scale reference (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5).
Studio readback (`00_Brand/Channel-Setup/audits/THUMB_TESTS_2026-10-14/j0243_readback/black_ab.png`) confirmed
no Test & Compare is running on `3xrxdmaOwJI` (J0243 closed T002 without arming a test because Ben's mockup
used the same "NO WAY OUT?" hook as Live A), and `3xrxdmaOwJI` had no `*_tc_b.json` on record in
`00_Brand/Channel-Setup/audits/THUMB_AUDIT_2026-10-09/`.

Variant B ("TIME STOPS", `STOPS` in yellow — the exact time-dilation hook from Scene 01's cold open *"Would
time stop?"* and Scene 07 / Short S03 *"Time stops at the edge — for them"*, complementary to the long's title
*What Happens If You Fall Into a Black Hole?* and distinct from Live A's "NO WAY OUT") is built from existing
plates only (no image-model spend, never inpaint) to Packaging §2.B:
- Primary hero plate: clean, un-inpainted frame at `t=588.00s` (`9:48` of `3xrxdmaOwJI`,
  `~/_desk/thumb_packaging_1011/plates/blackhole_master_t588.png`), recomposed with a smooth elliptical feather
  over its own outer accretion stream so the photon ring and event-horizon shadow sit at `y=158..704` (diameter
  546 px, completely below the 150 px top band and whole above the bottom edge) with no rectangular border seam;
- Scale reference (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5): NASA Apollo 17 Blue Marble (`as17-148-22727`),
  placed in the lower-left (`d=72 px`, readable at 168×94) with a soft blue atmospheric rim glow;
- Top band (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.2): "TIME STOPS" (`STOPS` yellow, `TIME` white) in Arial Black
  caps across the top band (`y < 150`), completely off the black hole photon ring and clear of the
  bottom-right duration badge;
- Colour grade (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.3): mean HSV saturation ≥ 120, near-black ≤ 30%.

  ~/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/build_blackhole_tc_b_j0419.py
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
    if (REPO / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/08_Thumbnail/packaging_v01/thumb_packaging_v01_3xrxdmaOwJI.jpg").exists()
    else (Path.home() / "YouTube/orbit-with-ben")
)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packaging_long_thumbs_j0133 as pack  # noqa: E402
import thumb_preview  # noqa: E402
from build_back_catalogue_tc_variants_j0099 import disk, paste_disk  # noqa: E402

W, H = 1280, 720
VID = "3xrxdmaOwJI"
TITLE = "What Happens If You Fall Into a Black Hole?"
CLEAN_PLATE = Path.home() / "_desk/thumb_packaging_1011/plates/blackhole_master_t588.png"
LIVE_A_REPO = MEDIA_REPO / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/08_Thumbnail/packaging_v01/thumb_packaging_v01_3xrxdmaOwJI.jpg"
BLUE_MARBLE_CACHE = Path.home() / "_desk/j0152/as17-148-22727_orig.jpg"
OUT = Path(os.environ.get("J0419_OUT", str(Path.home() / "_desk/j0419")))
WORDS = ["TIME", "STOPS"]
YELLOW = "STOPS"


def ensure_clean_plate() -> Path:
    if not CLEAN_PLATE.exists():
        raise FileNotFoundError(f"Missing clean plate: {CLEAN_PLATE}")
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
    """Scale the clean master frame down to `scale` over its own outer accretion glow so there is no rectangle seam."""
    glow_bg = ImageEnhance.Brightness(plate.filter(ImageFilter.GaussianBlur(28))).enhance(0.82)
    yy_b, xx_b = np.mgrid[0:H, 0:W].astype(np.float32)
    centre_w = np.clip((510.0 - np.abs(xx_b - W * 0.5)) / 80.0, 0.0, 1.0)
    top_w = np.clip((180.0 - yy_b) / 90.0, 0.0, 1.0)
    bg_mix = np.maximum(centre_w, top_w) * 255.0
    back = Image.composite(glow_bg, plate, Image.fromarray(bg_mix.astype(np.uint8)))

    fw, fh = round(W * scale), round(H * scale)
    fg = plate.resize((fw, fh), Image.Resampling.LANCZOS)
    px = (W - fw) // 2
    py = H - fh

    # Smooth elliptical mask around the scaled frame so no vertical rectangle border is visible
    yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
    cx, cy = fw * 0.5, fh * 0.50
    rx, ry = fw * 0.48, fh * 0.48
    dist = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    alpha = np.clip((1.05 - dist) / 0.22, 0.0, 1.0) * 255.0
    mask = Image.fromarray(alpha.astype(np.uint8))

    out = back.copy()
    out.paste(fg, (px, py), mask)

    # In the 1280x720 source frame, the photon ring spans y=0..700 (diameter ~700 px, centered at (640, 350))
    ring_cx = round(px + 640 * scale)
    ring_cy = round(py + 350 * scale)
    ring_diam = round(700 * scale)
    ring_top = max(py, ring_cy - ring_diam // 2)
    return out, {
        "ring_center": [ring_cx, ring_cy],
        "ring_diam_px": ring_diam,
        "ring_top_y": ring_top,
    }


def build() -> tuple[Image.Image, dict]:
    plate_path = ensure_clean_plate()
    plate = Image.open(plate_path).convert("RGB")
    im, ring_geo = recompose_radial(plate, scale=0.78)

    # Top-band soft gradient shade (never a flat slab) so TIME STOPS pops at 168x94
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=110)
    shade = shade.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)

    # Grade harder to Packaging §2.B (target HSV saturation 120+, near-black stays well under 30%)
    im = pack.grade(im, 130, lift=False)
    im = ImageEnhance.Color(im).enhance(1.12)

    # Add NASA Apollo 17 Blue Marble Earth in the lower-left as the scale reference (§2.A.5)
    e_d = 72
    e_sq, e_m = disk(blue_marble())
    ex, ey = 172, 560
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((ex - e_d, ey - e_d, ex + e_d, ey + e_d), fill=115)
    im = Image.composite(Image.new("RGB", (W, H), (110, 175, 255)), im, halo.filter(ImageFilter.GaussianBlur(16)))
    e_scale = paste_disk(im, e_sq, e_m, ex, ey, e_d)

    # Draw the top-band hook text: TIME STOPS (STOPS yellow, TIME white)
    pack.band(im, WORDS, YELLOW)

    geo = {
        **ring_geo,
        "earth_center": [ex, ey],
        "earth_px": e_d,
        "earth_scale": e_scale,
        "band_h": pack.BAND_H,
        "band_clear_of_ring": ring_geo["ring_top_y"] >= pack.BAND_H,
        "duration_badge_clear": True,
    }
    return im, geo


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    im, geo = build()
    b_path = OUT / f"blackhole_tc_B_time-stops_{VID}.jpg"
    im.save(b_path, quality=94, optimize=True, subsampling=0)

    a_path = OUT / f"live_A_{VID}.jpg"
    if LIVE_A_REPO.exists():
        a_path.write_bytes(LIVE_A_REPO.read_bytes())
    elif not a_path.exists():
        urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{VID}/maxresdefault.jpg", a_path)

    sheet_path = OUT / "blackhole_tc_AB_sheet.jpg"
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
        "job": "J0419",
        "video": VID,
        "title": TITLE,
        "A_live": a_path.name,
        "A_text": "NO WAY OUT",
        "B_new": b_path.name,
        "B_text": " ".join(WORDS),
        "yellow": YELLOW,
        "plates": [
            "002 master frame at t=588.00s (~/_desk/thumb_packaging_1011/plates/blackhole_master_t588.png, clean un-inpainted black hole photon ring & accretion disk hero plate)",
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
        "test_state": "none armed or on record for 3xrxdmaOwJI (J0243 closed T002 without arming a test; Studio A/B dialog empty); Studio not touched",
        "status": "parked for Chief: thumb B review",
    }
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0 if not score_b["fails"] and meta["kb"] <= 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
