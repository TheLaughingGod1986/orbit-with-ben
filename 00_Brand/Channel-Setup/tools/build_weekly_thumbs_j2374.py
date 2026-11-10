#!/usr/bin/env python3
"""J2374 weekly OWB thumbnail audit — build 3 new Test & Compare B drafts:
1. 2fsQcea-voM (013 Why the Moon Is Slowly Leaving Us): 'NO MORE ECLIPSES' (yellow ECLIPSES)
   Plates: NASA GSFC_20171208_Archive_e000868 (Full Moon) + NASA Apollo 17 as17-148-22727 (Earth).
2. Yk1tLh23rko (007 What Happens If You Get Near a Neutron Star or Pulsar?): '20 KM WIDE' (yellow 20)
   Plates: 007 master frame at t=465.00s (clean un-inpainted neutron star) + NASA Apollo 17 as17-148-22727 (Earth).
3. b8-X_FyJnHM (003 Alien Worlds: The Strangest Planets We've Ever Found): 'RAINS MOLTEN GLASS' (yellow GLASS)
   Plates: NASA Hubble GSFC_20171208_Archive_e001427 (HD 189733 b) + NASA Apollo 17 as17-148-22727 (Earth).

House rules (THUMBNAIL_AND_TITLE_RULES.md §§2, 2.A, 2.B):
- 1280x720 JPEG, < 2 MB
- 2-3 words in top band, off the subject, one yellow hook word, heavy black stroke
- Mean HSV saturation >= 100 (aim 120+), near-black <= 30%
- Scale reference (Earth) present and clear of bottom-right duration badge
- Zero generation spend; does not touch YouTube Studio.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
SYS_TOOLS = ROOT / "00_Brand/Channel-Setup/tools"
sys.path.insert(0, str(SYS_TOOLS))
from thumb_preview import score as score_thumb  # noqa: E402

DESK = Path("/Users/ben/_desk/j2374")
PLATES = DESK / "plates"
LIVE = DESK / "live"
OUT = DESK / "designs"
EARTH_SRC = Path("/Users/ben/_desk/J2141-bodies-source-macbook-v01/as17-148-22727.jpg")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

W, H = 1280, 720
BAND_H = 148
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def starfield_bg(seed: int, base_rgb: tuple[int, int, int], glow_rgb: tuple[int, int, int],
                 gx: float = 720.0, gy: float = 440.0, gr: float = 520.0) -> Image.Image:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.exp(-(((xx - gx) ** 2) / (gr ** 2) + ((yy - gy) ** 2) / ((gr * 0.72) ** 2)))
    top_lift = np.exp(-((yy / 240.0) ** 2)) * 0.25
    arr = np.zeros((H, W, 3), dtype=np.float32)
    for k in range(3):
        arr[:, :, k] = base_rgb[k] + glow_rgb[k] * g + glow_rgb[k] * top_lift
    arr += rng.normal(0, 1.1, (H, W, 1))
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(110):
        sx = int(rng.integers(20, W - 20))
        sy = int(rng.integers(140, H - 20))
        sv = int(rng.integers(90, 210))
        r = 1 if rng.random() < 0.82 else 2
        d.ellipse((sx, sy, sx + r, sy + r), fill=(sv, sv, min(255, sv + 30)))
    return im


def extract_disc(path: Path, size: int, thresh: int = 14) -> tuple[Image.Image, Image.Image]:
    raw = Image.open(path).convert("RGB")
    bbox = raw.convert("L").point(lambda v: 255 if v > thresh else 0).getbbox()
    crop = raw.crop(bbox).resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, size - 3, size - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.4))
    return crop, mask


def paste_earth_reference(im: Image.Image, diam: int = 160, pos: tuple[int, int] = (72, 470)) -> None:
    earth, emask = extract_disc(EARTH_SRC, diam, thresh=12)
    earth = ImageEnhance.Color(ImageEnhance.Contrast(earth).enhance(1.18)).enhance(1.55)
    # Subtle atmospheric rim glow
    glow = Image.new("RGBA", (diam + 24, diam + 24), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((4, 4, diam + 19, diam + 19), fill=(70, 165, 255, 95))
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    im.paste(glow.convert("RGB"), (pos[0] - 12, pos[1] - 12), glow.getchannel("A"))
    im.paste(earth, pos, emask)


def draw_top_band(im: Image.Image, words: list[str], yellow_word: str) -> list[int]:
    # Subtle top gradient so text pops without creating near-black pixels
    d = ImageDraw.Draw(im)
    text = " ".join(words)
    size, stroke = 112, 7
    while size > 64:
        font = ImageFont.truetype(FONT_PATH, size)
        bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bb[2] - bb[0] <= W * 0.90 and bb[3] - bb[1] <= BAND_H - 22:
            break
        size -= 3
    space = d.textbbox((0, 0), " ", font=font)[2]
    widths = [d.textbbox((0, 0), w, font=font, stroke_width=stroke)[2] for w in words]
    total_w = sum(widths) + space * (len(words) - 1)
    x = (W - total_w) // 2
    x0 = x
    top_bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    y = (BAND_H - (top_bb[3] - top_bb[1])) // 2 - top_bb[1] + 4
    for w, ww in zip(words, widths):
        fill = YELLOW if w == yellow_word else WHITE
        d.text((x + 3, y + 4), w, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        d.text((x, y), w, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
        x += ww + space
    return [int(x0), int(y), int(x), int(y + (top_bb[3] - top_bb[1]))]


def build_moon() -> dict:
    # Deep indigo + warm golden-amber cosmic glow (distinct from 027's blue-only look)
    im = starfield_bg(13, (22, 26, 64), (135, 78, 28), gx=830.0, gy=430.0, gr=490.0)
    moon_d = 490
    moon, mmask = extract_disc(PLATES / "GSFC_20171208_Archive_e000868.jpg", moon_d, thresh=15)
    moon = moon.filter(ImageFilter.UnsharpMask(radius=1.8, percent=85, threshold=2))
    m_arr = np.asarray(moon).astype(np.float32) / 255.0
    mr = moon_d / 2.0
    my, mx = np.mgrid[:moon_d, :moon_d]
    nx = (mx - mr) / mr
    ny = (my - mr) / mr
    nz = np.sqrt(np.clip(1.0 - nx ** 2 - ny ** 2, 0, 1))
    dot = np.clip(-0.55 * nx - 0.18 * ny + 0.80 * nz, 0, 1)
    rim = np.clip((1.0 - nz) * np.clip(-nx + 0.35, 0, 1), 0, 1) ** 1.3
    shade = 0.28 + 0.88 * (dot ** 0.75) + 0.55 * rim
    lum = 0.299 * m_arr[:, :, 0] + 0.587 * m_arr[:, :, 1] + 0.114 * m_arr[:, :, 2]
    lum = np.power(np.clip(lum * 1.18, 0, 1), 0.82)
    m_rgb = np.zeros_like(m_arr)
    # Warm golden-amber sunlit Moon so saturation >= 120 without pale exception
    m_rgb[:, :, 0] = np.clip(lum * shade * 1.28 + 0.26 * rim, 0, 1)
    m_rgb[:, :, 1] = np.clip(lum * shade * 0.94 + 0.16 * rim, 0, 1)
    m_rgb[:, :, 2] = np.clip(lum * shade * 0.52 + 0.06 * rim, 0, 1)
    moon_im = Image.fromarray((m_rgb * 255).astype(np.uint8))
    im.paste(moon_im, (625, 185), mmask)

    # Foreground Earth on lower-left
    paste_earth_reference(im, diam=220, pos=(85, 420))
    im = ImageEnhance.Color(im).enhance(1.38)
    bbox = draw_top_band(im, ["NO", "MORE", "ECLIPSES"], "ECLIPSES")
    out = OUT / "2fsQcea-voM_B_v01.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "2fsQcea-voM",
        "film": "013_Why-The-Moon-Is-Slowly-Leaving-Us",
        "live_title": "Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone",
        "title_b": "Why Does the Moon Drift 3.8 cm Farther Every Year?",
        "hook": "NO MORE ECLIPSES",
        "yellow": "ECLIPSES",
        "file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA GSFC_20171208_Archive_e000868 (Full Moon, public domain)",
            "NASA Apollo 17 as17-148-22727 (Blue Marble Earth, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_neutron() -> dict:
    src = Image.open(PLATES / "neutron_star_t465.png").convert("RGB")
    # Recompose clean neutron star lower so top band is completely clear of star
    bg = starfield_bg(7, (24, 22, 54), (145, 82, 24), gx=660.0, gy=445.0, gr=470.0)
    fg_w, fg_h = round(W * 0.80), round(H * 0.80)
    fg = src.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    # Feather edges of the master frame into the cosmic background
    yy, xx = np.mgrid[:fg_h, :fg_w]
    rx = (xx - fg_w / 2.0) / (fg_w * 0.44)
    ry = (yy - fg_h / 2.0) / (fg_h * 0.46)
    ell = np.clip(1.0 - np.sqrt(rx ** 2 + ry ** 2), 0, 1)
    mask = Image.fromarray((np.power(ell, 0.55) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))
    bg.paste(fg, ((W - fg_w) // 2 + 30, H - fg_h + 10), mask)

    # Add Earth scale reference in lower-left (clear of neutron star and duration badge)
    paste_earth_reference(bg, diam=148, pos=(68, 495))
    bg = ImageEnhance.Contrast(bg).enhance(1.12)
    bg = ImageEnhance.Color(bg).enhance(1.38)
    bbox = draw_top_band(bg, ["20", "KM", "WIDE"], "20")
    out = OUT / "Yk1tLh23rko_B_v01.jpg"
    bg.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "Yk1tLh23rko",
        "film": "007_What-Happens-To-Your-Body-Near-A-Neutron-Star",
        "live_title": "What Happens If You Get Near a Neutron Star or Pulsar?",
        "title_b": "What Happens to Your Body Near a Neutron Star?",
        "hook": "20 KM WIDE",
        "yellow": "20",
        "file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "007 master frame at t=465.00s (neutron_star_STUDIO_OWNER.mp4, clean un-inpainted hero plate)",
            "NASA Apollo 17 as17-148-22727 (Blue Marble Earth scale reference, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def build_alien_worlds() -> dict:
    im = starfield_bg(3, (18, 28, 68), (28, 115, 220), gx=740.0, gy=435.0, gr=500.0)
    planet_d = 510
    raw = Image.open(PLATES / "GSFC_20171208_Archive_e001427.jpg").convert("RGB")
    raw_arr = np.asarray(raw).astype(np.int32)
    # Blue excess (B - R > 55) finds top, bottom, and right sunlit limb of HD 189733 b
    blue_mask = Image.fromarray(((raw_arr[:, :, 2] - raw_arr[:, :, 0]) > 55).astype(np.uint8) * 255)
    pb = blue_mask.getbbox()
    pr = (pb[3] - pb[1]) // 2
    pcx = pb[2] - pr
    pcy = (pb[1] + pb[3]) // 2
    planet = raw.crop((pcx - pr, pcy - pr, pcx + pr, pcy + pr)).resize(
        (planet_d, planet_d), Image.Resampling.LANCZOS
    )
    planet = planet.filter(ImageFilter.UnsharpMask(radius=1.8, percent=80, threshold=2))
    p_arr = np.asarray(planet).astype(np.float32) / 255.0
    py, px = np.mgrid[:planet_d, :planet_d]
    pnx = (px - planet_d / 2.0) / (planet_d / 2.0)
    pny = (py - planet_d / 2.0) / (planet_d / 2.0)
    pnz = np.sqrt(np.clip(1.0 - pnx ** 2 - pny ** 2, 0, 1))
    # Smoothly shade the nightside limb in deep cobalt blue so the full 3D sphere reads cleanly
    sunlit = np.clip((p_arr[:, :, 2] - p_arr[:, :, 0] * 0.5) * 2.2, 0, 1)
    night_r = 0.05 + 0.06 * pnz
    night_g = 0.16 + 0.18 * pnz
    night_b = 0.46 + 0.36 * pnz
    p_arr = np.power(np.clip(p_arr, 0, 1), 0.78)
    p_arr[:, :, 0] = np.clip(p_arr[:, :, 0] * 0.95 * sunlit + night_r * (1.0 - sunlit), 0, 1)
    p_arr[:, :, 1] = np.clip(p_arr[:, :, 1] * 1.18 * sunlit + night_g * (1.0 - sunlit), 0, 1)
    p_arr[:, :, 2] = np.clip(p_arr[:, :, 2] * 1.38 * sunlit + night_b * (1.0 - sunlit), 0, 1)
    planet_im = Image.fromarray((p_arr * 255).astype(np.uint8))
    pmask = Image.new("L", (planet_d, planet_d), 0)
    ImageDraw.Draw(pmask).ellipse((6, 6, planet_d - 7, planet_d - 7), fill=255)
    pmask = pmask.filter(ImageFilter.GaussianBlur(2.0))
    im.paste(planet_im, (560, 175), pmask)

    # Add subtle diagonal glass-rain streaks across the atmosphere limb
    streaks = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(streaks)
    rng = np.random.default_rng(33)
    for _ in range(28):
        x0 = int(rng.integers(540, 1040))
        y0 = int(rng.integers(220, 620))
        dx = int(rng.integers(45, 95))
        dy = int(dx * 0.28)
        sd.line((x0, y0, x0 + dx, y0 + dy), fill=(185, 235, 255, 90), width=2)
    streaks = streaks.filter(ImageFilter.GaussianBlur(1.0))
    im.paste(streaks.convert("RGB"), (0, 0), streaks.getchannel("A"))

    # Earth scale reference on lower-left
    paste_earth_reference(im, diam=175, pos=(85, 455))
    im = ImageEnhance.Color(im).enhance(1.25)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    bbox = draw_top_band(im, ["RAINS", "MOLTEN", "GLASS"], "GLASS")
    out = OUT / "b8-X_FyJnHM_B_v01.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "b8-X_FyJnHM",
        "film": "003_Exoplanets-Strangest-Alien-Worlds",
        "live_title": "Alien Worlds: The Strangest Planets We've Ever Found",
        "title_b": "What Are the Strangest Planets We've Ever Found?",
        "hook": "RAINS MOLTEN GLASS",
        "yellow": "GLASS",
        "file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            "NASA Hubble GSFC_20171208_Archive_e001427 (HD 189733 b True Blue Planet, public domain)",
            "NASA Apollo 17 as17-148-22727 (Blue Marble Earth scale reference, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [build_moon(), build_neutron(), build_alien_worlds()]
    for r in rows:
        assert r["bytes"] < 2_000_000, f"{r['file']} >= 2MB"
        assert not r["score"]["fails"], f"Score fail on {r['file']}: {r['score']}"

    # Run official thumb_preview.py --score
    preview_out = OUT / "THUMB_PREVIEW_SCORE_SHEET.jpg"
    cmd = [
        sys.executable,
        str(SYS_TOOLS / "thumb_preview.py"),
        "long",
        *[r["file"] for r in rows],
        "--out",
        str(preview_out),
        "--score",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(proc.stdout.strip())

    # Build side-by-side Live A vs Proposed B sheet at 168x94 and 352x198
    sheet = Image.new("RGB", (1100, 1050), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_PATH, 18)
    for i, r in enumerate(rows):
        y = 20 + i * 340
        d.text((20, y), f"{r['video']} — live A vs proposed B ({r['hook']})", font=f, fill="black")
        for j, p in enumerate([LIVE / f"{r['video']}.jpg", Path(r["file"])]):
            im = Image.open(p).convert("RGB")
            sheet.paste(im.resize((168, 94), Image.Resampling.LANCZOS), (20 + j * 540, y + 35))
            sheet.paste(im.resize((352, 198), Image.Resampling.LANCZOS), (20 + j * 540, y + 138))
    phone_sheet = OUT / "PHONE_SHEET_v01.jpg"
    sheet.save(phone_sheet, quality=95)

    manifest = {
        "job": "J2374",
        "date": "2026-11-09",
        "builder": "00_Brand/Channel-Setup/tools/build_weekly_thumbs_j2374.py",
        "phone_sheet": str(phone_sheet),
        "phone_sheet_sha256": sha256(phone_sheet),
        "preview_score_sheet": str(preview_out),
        "preview_score_sheet_sha256": sha256(preview_out),
        "gate_stdout": proc.stdout.strip(),
        "designs": rows,
    }
    (OUT / "DESIGN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    EVID = ROOT / "05_Analytics/weekly_thumb_audit/OWB/2026-11-09_evidence"
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "DESIGN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
