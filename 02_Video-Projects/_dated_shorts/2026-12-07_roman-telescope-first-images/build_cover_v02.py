#!/usr/bin/env python3
"""J3337 — Cover-only rebuild for 7 Dec 2026 NASA Nancy Grace Roman Space Telescope First Images dated-event Short.

Replaces cover_v01.jpg (which had unmasked additive Hubble UDF galaxy bleed-through across the spacecraft hull)
with roman_2026_12_07_cover_v02.jpg (1080x1920):
- Pure graded NASA Goddard SVS #15081 Milky Way hero frame (frame 55 of the 36.0s Roman sweep, cropped strictly
  inside x <= 908, y <= 1645 so the bottom-right NASA 'Animation' credit is 100% excluded) — ZERO additive galaxy
  bleed-through, 100% solid opaque Roman Space Telescope hull and white sunshield.
- Clean NASA SVS #5587 plain 4K full Moon disc (frame 7864) with subtle outer lunar glow, positioned cleanly inside
  the 16:9 centre crop (y=656..1264) and clear of the spacecraft body.
- Bold house cover typography: '**100** / HUBBLES' (yellow 100, white HUBBLES, 2 words, zero words shared with title).
- Leaves locked video v01 (owb_dated_2026_12_07_roman_first_images_v01.mp4), cover_v01.jpg, and all v01 files untouched.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

BASE = Path(__file__).resolve().parent
MAIN_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SHARED_POOL = Path("/Users/benjaminoats/_desk/wt-J2478/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/07_Edit-Project/pool_v01")

SVS15081 = BASE / "07_Edit-Project/pool_v01/svs15081/15081-_Trailer_Long_Vertical.mp4"
MOON_4K = SHARED_POOL / "svs5587/phases_2026_plain_2160p30.mp4"
VIDEO_V01 = BASE / "06_Final-Exports/owb_dated_2026_12_07_roman_first_images_v01.mp4"
COVER_V01 = BASE / "11_Upload-Package/roman_2026_12_07_cover_v01.jpg"
COVER_V02 = BASE / "11_Upload-Package/roman_2026_12_07_cover_v02.jpg"
QA_DIR = BASE / "07_Edit-Project/assembly_j3331_v01/qa"
PREVIEW_V02 = QA_DIR / "cover_v02_thumb_preview.jpg"
PREVIEW_TXT = QA_DIR / "cover_v02_thumb_preview.txt"
DELIVERY_JSON = BASE / "DELIVERY_v01_cover_v02_SHA256.json"

EXPECTED_VIDEO_V01_SHA = "ff52475588e5ecee1caca6840105711bfed2b67c6b83ab3f08239e3761e47bd1"
EXPECTED_COVER_V01_SHA = "c17ac08de15dac4ac383e846374f8bd52059b14175ff985c7341f06bfb52c305"

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
FPS = 30
WHITE = (245, 248, 255, 255)
YELLOW = (255, 213, 64, 255)
STROKE = (8, 16, 28, 255)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def crop_box(im: Image.Image, cx_px: float, cy_px: float, ch_px: float) -> Image.Image:
    cw_px = ch_px * (W / H)
    x0 = min(max(cx_px - cw_px / 2.0, 0.0), im.width - cw_px)
    y0 = min(max(cy_px - ch_px / 2.0, 0.0), im.height - ch_px)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw_px, y0 + ch_px), Image.Resampling.BICUBIC)


def lift_if_dark(im: Image.Image, target_mean: float = 42.0, target_p95: float = 82.0) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean, p95 = float(luma.mean()), float(np.percentile(luma, 95))
    if mean >= target_mean and p95 >= target_p95:
        return im
    scale = max(1.0, target_p95 / max(p95, 1.0))
    lift = max(0.0, target_mean - mean * scale)
    lut = [min(255, int(v * scale + lift * (1.0 - min(255.0, v * scale) / 255.0))) for v in range(256)]
    return im.point(lut * 3)


def decode_svs_hero_frame(mp4: Path, start_s: float, frame_offset: int) -> Image.Image:
    ss = start_s + frame_offset / FPS
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(mp4),
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    return Image.frombytes("RGB", (W, H), raw)


def decode_svs_moon_disc(video_path: Path, frame_idx: int, diam: int) -> Image.Image:
    ss = frame_idx / FPS
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(video_path),
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    im = Image.frombytes("RGB", (3840, 2160), raw)
    box = (1920 - 1002, 1080 - 1002, 1920 + 1002, 1080 + 1002)
    sub = lift_if_dark(im.crop(box)).resize((diam, diam), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (diam, diam), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, diam - 3, diam - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))
    sub.putalpha(mask)
    return sub


def centred(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, stroke: int) -> int:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) / 2 - b[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=STROKE)
    return b[3] - b[1]


def grade_cosmic_hero(im: Image.Image) -> Image.Image:
    """Grade pure NASA SVS #15081 hero frame with rich cosmic contrast and zero external galaxy overlay."""
    im = ImageEnhance.Color(im).enhance(1.48)
    im = ImageEnhance.Contrast(im).enhance(1.17)
    arr = np.asarray(im, dtype=np.float32)
    # Smooth deep-space navy-indigo shadow lift keeps near-black <= 22% while preserving solid metallic hull contrast
    w_dark = np.clip(1.0 - (arr / 140.0), 0.0, 1.0) ** 1.38
    arr[:, :, 0] += 18.0 * w_dark[:, :, 0]
    arr[:, :, 1] += 23.0 * w_dark[:, :, 1]
    arr[:, :, 2] += 39.0 * w_dark[:, :, 2]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    out = ImageEnhance.Sharpness(out).enhance(1.20)
    return out


def main() -> None:
    vid_sha = sha256(VIDEO_V01)
    if vid_sha != EXPECTED_VIDEO_V01_SHA:
        raise SystemExit(f"Locked video v01 SHA mismatch: {vid_sha} != {EXPECTED_VIDEO_V01_SHA}")
    v01_cov_sha = sha256(COVER_V01)
    if v01_cov_sha != EXPECTED_COVER_V01_SHA:
        raise SystemExit(f"Untouched cover_v01 SHA mismatch: {v01_cov_sha} != {EXPECTED_COVER_V01_SHA}")

    raw_hero = decode_svs_hero_frame(SVS15081, start_s=36.0, frame_offset=55)
    # Crop strictly inside x <= 863, y <= 1620 (zero bottom-right NASA 'Animation' credit)
    # and elevate spacecraft neatly into the 16:9 centre crop (y=656..1264) while leaving clear top band for text
    cropped_hero = crop_box(raw_hero, cx_px=475.0, cy_px=930.0, ch_px=1380.0)
    base_rgba = grade_cosmic_hero(cropped_hero).convert("RGBA")

    # Clean SVS #5587 plain full Moon scale accent with soft lunar halo, cleanly inside 16:9 centre crop (y=672..877)
    moon_diam = 205
    moon_x, moon_y = 774, 672
    moon_disc = decode_svs_moon_disc(MOON_4K, frame_idx=7864, diam=moon_diam)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((moon_x - 24, moon_y - 24, moon_x + moon_diam + 24, moon_y + moon_diam + 24), fill=(195, 222, 255, 56))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=26))
    base_rgba = Image.alpha_composite(base_rgba, glow)
    base_rgba.alpha_composite(moon_disc, (moon_x, moon_y))

    # Bold house typography: '**100** / HUBBLES' (2 words, zero words shared with title, yellow 100 / white HUBBLES)
    d = ImageDraw.Draw(base_rgba)
    centred(d, 168, "100", ImageFont.truetype(FONT, 156), YELLOW, 10)
    centred(d, 342, "HUBBLES", ImageFont.truetype(FONT, 118), WHITE, 10)

    COVER_V02.parent.mkdir(parents=True, exist_ok=True)
    base_rgba.convert("RGB").save(COVER_V02, quality=93)

    # Run thumb_preview.py short --score
    res = subprocess.run(
        [
            sys.executable,
            str(MAIN_REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "short",
            str(COVER_V02),
            "--out",
            str(PREVIEW_V02),
            "--score",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    PREVIEW_TXT.write_text(res.stdout + res.stderr)
    print(res.stdout.strip())

    # Verify video v01 and cover_v01 remain untouched
    assert sha256(VIDEO_V01) == EXPECTED_VIDEO_V01_SHA
    assert sha256(COVER_V01) == EXPECTED_COVER_V01_SHA

    cover_v02_sha = sha256(COVER_V02)
    preview_v02_sha = sha256(PREVIEW_V02)
    preview_txt_sha = sha256(PREVIEW_TXT)
    script_sha = sha256(Path(__file__).resolve())

    manifest = {
        "job": "J3337",
        "parent_job": "J3331",
        "review_ref": "jobs/reviews/J3331/REVIEW.md",
        "delivery_folder": str(BASE),
        "video_v01_locked": {
            "file": "06_Final-Exports/owb_dated_2026_12_07_roman_first_images_v01.mp4",
            "bytes": VIDEO_V01.stat().st_size,
            "sha256": EXPECTED_VIDEO_V01_SHA,
            "status": "LOCKED (untouched from J3331 Chief KEEP)",
        },
        "cover_v01_superseded": {
            "file": "11_Upload-Package/roman_2026_12_07_cover_v01.jpg",
            "bytes": COVER_V01.stat().st_size,
            "sha256": EXPECTED_COVER_V01_SHA,
            "status": "UNTOUCHED (superseded by cover_v02.jpg)",
        },
        "cover_v02": {
            "file": "11_Upload-Package/roman_2026_12_07_cover_v02.jpg",
            "bytes": COVER_V02.stat().st_size,
            "sha256": cover_v02_sha,
            "dimensions": f"{W}x{H}",
            "cover_text": "**100** / HUBBLES",
            "fix": "Pure graded NASA SVS #15081 Milky Way hero frame (frame 55, cropped clear of NASA credit) with ZERO additive Hubble UDF bleed-through; 100% solid opaque Roman Space Telescope hull and sunshield + clean SVS #5587 full Moon accent inside 16:9 centre crop.",
        },
        "cover_v02_thumb_preview": {
            "file": "07_Edit-Project/assembly_j3331_v01/qa/cover_v02_thumb_preview.jpg",
            "bytes": PREVIEW_V02.stat().st_size,
            "sha256": preview_v02_sha,
            "score_output": res.stdout.strip().splitlines()[-1] if res.stdout.strip() else "",
        },
        "supporting_files": [
            {
                "file": "07_Edit-Project/assembly_j3331_v01/qa/cover_v02_thumb_preview.txt",
                "bytes": PREVIEW_TXT.stat().st_size,
                "sha256": preview_txt_sha,
            },
            {
                "file": "build_cover_v02.py",
                "bytes": Path(__file__).resolve().stat().st_size,
                "sha256": script_sha,
            },
        ],
    }
    DELIVERY_JSON.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {DELIVERY_JSON}")
    print(f"cover_v02.jpg SHA-256: {cover_v02_sha}")
    print(f"cover_v02_thumb_preview.jpg SHA-256: {preview_v02_sha}")


if __name__ == "__main__":
    main()
