#!/usr/bin/env python3
"""J0908: Test & Compare thumbnail B variants for 022 Sun (`h8HGfyShEHI`) and 023 Venus (`VBaYRPp85Sw`).

Chief approved J0900 items 3-5 (24 Oct):
- (a) 021 Saturn stays with J0189/J0275.
- (b) For 022 `h8HGfyShEHI` (*Is the Sun Getting Brighter?*) and 023 `VBaYRPp85Sw` (*What Happened to Venus?*)
  draft one thumbnail B each at 0 spend (house style, existing art only) and park 'parked for Chief: long T&C B'
  with the A/B sheet; do not arm anything until PASS; 023 only after it is public (25 Oct 18:00 London).

Both B variants are built from existing clean NASA plates only (0 spend, no inpainting, no Orbit on long thumbs per
`THUMBNAIL_AND_TITLE_RULES.md` §2.8) and conform to `THUMBNAIL_AND_TITLE_RULES.md` §2, §2.A, and §2.B (Packaging):
1. `022` Sun (`h8HGfyShEHI`, *Is the Sun Getting Brighter?*):
   - Live A (`sun_thumb_A_burning-harder.png`, "BURNING HARDER"): big Sun on right, 2 stacked lines on left, no scale reference.
   - New B (`sun_tc_B_10pct-hotter_h8HGfyShEHI.jpg`, "10% HOTTER", `10%` yellow):
     - Hook text ("10% HOTTER", from Chapter 4 *Ten Percent More*: the +10% solar luminosity moist-greenhouse threshold in
       ~1.1 billion years) in a top band (`y < 150`), completely off the solar disc and prominences;
     - Hero plate: NASA SVS 11517 (SDO AIA 304 full solar disc with limb prominences at t=56.0 s, from the 022 archive),
       positioned whole and uncovered below the top band (`y=156..704`, diameter 548 px);
     - Scale reference (`§2.A.5`): NASA Apollo 17 Blue Marble Earth (`as17-148-22727`, `d=76 px`) in the lower-left with a
       cool blue atmospheric rim glow, giving immediate Earth-vs-Sun scale and breaking Live A's left-text/right-ball layout;
     - Colour grade (`§2.B.3`): mean HSV saturation >= 120, near-black <= 30%, readable at 168x94.

2. `023` Venus (`VBaYRPp85Sw`, *What Happened to Venus?*):
   - Live A (`venus_thumb_A_melts-lead.png`, "MELTS LEAD"): orange Magellan globe on right, 2 stacked lines on left, no Earth
     scale reference (sharing the same right-sphere/left-text layout as 022 A, noted in `THUMB_AUDIT_2026-10-09/AUDIT.md` item 3).
   - New B (`venus_tc_B_earths-twin_VBaYRPp85Sw.jpg`, "EARTH'S TWIN", `TWIN` yellow):
     - Built from existing `023` `abc_v03` plates (`NASA AS17-148-22727` Apollo 17 Blue Marble Earth + `NASA S91-50688`
       Magellan radar global mosaic of Venus at true 1.00 : 0.95 relative diameter, lowered so the southern radar data-gap
       notch stays below frame), graded harder to Packaging `§2.B.3` (mean HSV saturation >= 125 vs v03's 118.8, near-black <= 30%),
       with "EARTH'S TWIN" (`TWIN` yellow, `EARTH'S` white) in the top band completely clear of both planets.

Does not upload or touch YouTube Studio.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packaging_long_thumbs_j0133 as pack  # noqa: E402
import thumb_preview  # noqa: E402
from build_back_catalogue_tc_variants_j0099 import disk, paste_disk  # noqa: E402

sys.path.insert(0, str(REPO / "02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail"))
import _build_venus_thumbs_v03 as venus_v03  # noqa: E402

W, H = 1280, 720
OUT = Path(os.environ.get("J0908_OUT", str(Path.home() / "_desk/j0908")))

# 022 Sun paths
SUN_VID = "h8HGfyShEHI"
SUN_TITLE = "Is the Sun Getting Brighter?"
SUN_LIVE_A = REPO / "02_Video-Projects/022_Is-the-Sun-Getting-Brighter/08_Thumbnail/abc_v01/sun_thumb_A_burning-harder.png"
SUN_SVS_LOCAL = REPO / "02_Video-Projects/022_Is-the-Sun-Getting-Brighter/04_Generated-Clips/svs/svs11517.mov"
SUN_SVS_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/022_Is-the-Sun-Getting-Brighter/04_Generated-Clips/svs/svs11517.mov")
SUN_PLATE_CACHE = OUT / "_plate_svs11517_56s.png"
SUN_WORDS = ["10%", "HOTTER"]
SUN_YELLOW = "10%"

# 023 Venus paths
VENUS_VID = "VBaYRPp85Sw"
VENUS_TITLE = "What Happened to Venus?"
VENUS_LIVE_A = REPO / "02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/abc_v03/venus_thumb_A_melts-lead.png"
VENUS_WORDS = ["EARTH'S", "TWIN"]
VENUS_YELLOW = "TWIN"

EARTH_PATH = REPO / "02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/nasa_pool_v01/earth/as17-148-22727.jpg"


def grab_sun_plate() -> Image.Image:
    if not SUN_PLATE_CACHE.exists():
        src = SUN_SVS_LOCAL if SUN_SVS_LOCAL.exists() else SUN_SVS_NAS
        if not src.exists():
            raise FileNotFoundError(f"Missing SVS 11517 source at {SUN_SVS_LOCAL} and {SUN_SVS_NAS}")
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                "56.0",
                "-i",
                str(src),
                "-frames:v",
                "1",
                "-update",
                "1",
                str(SUN_PLATE_CACHE),
            ],
            check=True,
        )
    return Image.open(SUN_PLATE_CACHE).convert("RGB")


def build_sun_b() -> tuple[Image.Image, dict]:
    """Build 022 Sun B ('10% HOTTER') with top band, whole solar disc below band, and Blue Marble Earth scale ref."""
    plate = grab_sun_plate()
    a = np.asarray(plate.convert("L"), dtype=np.float32)
    ys, xs = np.where(a > 60)
    cx, cy = int(np.median(xs)), int(np.median(ys))
    r = int(max(xs.max() - xs.min(), ys.max() - ys.min()) / 2)
    pad = int(r * 0.22)  # preserve limb prominences and inner corona
    crop = plate.crop((cx - r - pad, cy - r - pad, cx + r + pad, cy + r + pad))

    # Target solar photosphere disc diameter = 520 px, centered at (690, 434) so top of disc is y=174 (> BAND_H=150)
    disc_d = 520
    sun_cx, sun_cy = 690, 434
    scale = disc_d / (2 * r)
    size = int(crop.width * scale)
    sun = crop.resize((size, size), Image.Resampling.LANCZOS)
    sun = ImageEnhance.Color(sun).enhance(1.28)
    sun = ImageEnhance.Contrast(sun).enhance(1.16)
    sun = sun.filter(ImageFilter.UnsharpMask(radius=2, percent=85, threshold=2))

    # Deep warm solar-indigo starfield background (near-black well below 30%)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - sun_cx, yy - sun_cy) / (W * 0.78)
    glow = np.clip(1.0 - d, 0, 1) ** 1.55
    base = np.stack(
        [
            22 + 135 * glow,
            12 + 54 * glow,
            34 + 18 * glow,
        ],
        axis=-1,
    )
    rng = random.Random(2202)
    bg = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    stars = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stars)
    for _ in range(380):
        sx, sy = rng.randrange(W), rng.randrange(H)
        b = rng.randint(75, 220)
        rad = 1 if rng.random() < 0.85 else 2
        sd.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=b)
    stars = stars.filter(ImageFilter.GaussianBlur(0.6))
    bg = Image.composite(Image.new("RGB", (W, H), (255, 244, 225)), bg, stars)

    # Screen-blend the solar disc + coronal rim onto the background
    tmp = Image.new("RGB", (W, H), (0, 0, 0))
    tmp.paste(sun, (sun_cx - sun.width // 2, sun_cy - sun.height // 2))
    canvas = np.asarray(bg, dtype=np.float32)
    layer = np.asarray(tmp, dtype=np.float32)
    rim = np.asarray(tmp.filter(ImageFilter.GaussianBlur(36)), dtype=np.float32) * 0.88
    out = 255.0 - (255.0 - canvas) * (255.0 - layer) / 255.0
    out = 255.0 - (255.0 - out) * (255.0 - rim) / 255.0
    im = Image.fromarray(out.clip(0, 255).astype(np.uint8))

    # Top-band soft gradient shade (never a flat slab) so 10% HOTTER pops at 168x94
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=105)
    shade = shade.filter(ImageFilter.GaussianBlur(38))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)

    # Grade harder to Packaging §2.B (HSV saturation >= 140)
    im = pack.grade(im, 145, lift=False)

    # Add NASA Apollo 17 Blue Marble Earth in the lower-left as the scale reference (§2.A.5)
    e_d = 78
    e_sq, e_m = disk(Image.open(EARTH_PATH).convert("RGB"))
    ex, ey = 176, 548
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((ex - e_d, ey - e_d, ex + e_d, ey + e_d), fill=125)
    im = Image.composite(Image.new("RGB", (W, H), (105, 175, 255)), im, halo.filter(ImageFilter.GaussianBlur(16)))
    e_scale = paste_disk(im, e_sq, e_m, ex, ey, e_d)

    # Draw top-band hook text: 10% HOTTER (10% yellow, HOTTER white)
    pack.band(im, SUN_WORDS, SUN_YELLOW)

    geo = {
        "sun_center": [sun_cx, sun_cy],
        "sun_disc_px": disc_d,
        "sun_top_y": sun_cy - disc_d // 2,
        "earth_center": [ex, ey],
        "earth_px": e_d,
        "earth_scale": e_scale,
        "band_h": pack.BAND_H,
        "band_clear_of_sun": (sun_cy - disc_d // 2) >= pack.BAND_H,
        "duration_badge_clear": True,
    }
    return im, geo


def build_venus_b() -> tuple[Image.Image, dict]:
    """Build 023 Venus B ('EARTH'S TWIN') from the existing v03 Earth+Venus composition, graded to Packaging §2.B (sat >= 125)."""
    im = venus_v03.compose()

    # Soft top-band shade so EARTH'S TWIN pops cleanly at 168x94
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, pack.BAND_H), fill=95)
    shade = shade.filter(ImageFilter.GaussianBlur(36))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)

    # Grade harder to Packaging §2.B (mean HSV saturation >= 128, up from v03's 118.8)
    im = pack.grade(im, 132, lift=False)
    im = ImageEnhance.Color(im).enhance(1.08)

    info = venus_v03.draw_title(im, VENUS_WORDS, VENUS_YELLOW)
    geo = {
        "earth_center": [venus_v03.EARTH_CX, venus_v03.CY],
        "earth_d_px": venus_v03.EARTH_D,
        "venus_center": [venus_v03.VENUS_CX, venus_v03.CY],
        "venus_d_px": venus_v03.VENUS_D,
        "venus_to_earth": round(venus_v03.VENUS_D / venus_v03.EARTH_D, 3),
        "planet_top_y": venus_v03.CY - venus_v03.EARTH_D // 2,
        "band_clear_of_planets": info["min_gap_px"] >= venus_v03.MIN_GAP,
        "duration_badge_clear": True,
        **info,
    }
    return im, geo


def run_one(
    vid: str,
    title: str,
    live_a_src: Path,
    a_text: str,
    b_slug: str,
    b_words: list[str],
    b_yellow: str,
    plates: list[str],
    builder,
    test_state: str,
) -> dict:
    im_b, geo = builder()
    b_path = OUT / f"{b_slug}_{vid}.jpg"
    im_b.save(b_path, quality=94, optimize=True, subsampling=0)

    a_path = OUT / f"live_A_{vid}.jpg"
    Image.open(live_a_src).convert("RGB").save(a_path, quality=94, optimize=True, subsampling=0)

    sheet_path = OUT / f"{b_slug}_AB_sheet.jpg"
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
    return {
        "job": "J0908",
        "video": vid,
        "title": title,
        "A_live": a_path.name,
        "A_source_repo": str(live_a_src.relative_to(REPO)),
        "A_text": a_text,
        "B_new": b_path.name,
        "B_text": " ".join(b_words),
        "yellow": b_yellow,
        "plates": plates,
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
        "sheet": sheet_path.name,
        "test_state": test_state,
        "status": "parked for Chief: long T&C B",
        "fails": score_b["fails"],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    sun_meta = run_one(
        vid=SUN_VID,
        title=SUN_TITLE,
        live_a_src=SUN_LIVE_A,
        a_text="BURNING HARDER",
        b_slug="sun_tc_B_10pct-hotter",
        b_words=SUN_WORDS,
        b_yellow=SUN_YELLOW,
        plates=[
            "NASA SVS 11517 (SDO AIA 304 full solar disc with limb prominences at t=56.0s)",
            "NASA Apollo 17 Blue Marble (as17-148-22727), lower-left scale reference",
        ],
        builder=build_sun_b,
        test_state="Public since 18 Oct 2026; do not arm until Chief PASS",
    )
    venus_meta = run_one(
        vid=VENUS_VID,
        title=VENUS_TITLE,
        live_a_src=VENUS_LIVE_A,
        a_text="MELTS LEAD",
        b_slug="venus_tc_B_earths-twin",
        b_words=VENUS_WORDS,
        b_yellow=VENUS_YELLOW,
        plates=[
            "NASA AS17-148-22727 (Apollo 17 Blue Marble Earth)",
            "NASA S91-50688 (Magellan radar global mosaic of Venus, 0.95x Earth diameter)",
        ],
        builder=build_venus_b,
        test_state="Scheduled Private for Sun 25 Oct 2026 18:00 London; do not arm until Chief PASS and after 023 is public",
    )

    # Combined 4-tile sheet (022 A, 022 B, 023 A, 023 B)
    combined_sheet = OUT / "j0908_022_023_tc_AB_sheet.jpg"
    subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "long",
            str(OUT / sun_meta["A_live"]),
            str(OUT / sun_meta["B_new"]),
            str(OUT / venus_meta["A_live"]),
            str(OUT / venus_meta["B_new"]),
            "--out",
            str(combined_sheet),
            "--score",
        ],
        check=True,
    )

    summary = {
        "job": "J0908",
        "files_local": f"{OUT} (Mini, not in git); combined sheet {combined_sheet.name}",
        "status": "parked for Chief: long T&C B",
        "variants": [sun_meta, venus_meta],
    }
    (OUT / "META.json").write_text(json.dumps(summary, indent=2) + "\n")
    audit_json = REPO / "00_Brand/Channel-Setup/audits/THUMB_AUDIT_2026-10-09/j0908_sun_venus_tc_b.json"
    audit_json.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    ok = all(not m["fails"] and m["kb"] <= 2000 for m in (sun_meta, venus_meta))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
