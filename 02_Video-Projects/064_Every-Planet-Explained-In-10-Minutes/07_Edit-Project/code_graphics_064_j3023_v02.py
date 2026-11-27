#!/usr/bin/env python3
"""J3023 v02 £0 24fps code graphics renderer for OWB:064 Every Planet Explained in 12 Minutes.

Renders the new/corrected v02 graphics into studio-live 04_Generated-Clips/J3023_code_graphics_v02/
(leaving J3022_code_graphics_v01/ untouched for history):
  1. code_graphic_064_ch01_mercury_progress_strip_v02.png  (sleek 8-planet progress strip highlighting 01 / 08 · MERCURY)
  2. code_graphic_064_r03a_mercury_sunlight.mp4            (3.80 s, +430 °C day / 58M km / 7× sunlight)
  3. code_graphic_064_r03b_mercury_night.mp4               (3.60 s, -180 °C night plunge / DATA #1 Ch 1)
  4. code_graphic_064_ch02_card_venus_v02.mp4              (3.00 s, Venus chapter card using real Mariner 10 PIA23791 right globe — zero PIA00271)
  5. code_graphic_064_r12_venus_greenhouse_v02.mp4         (10.00 s, 464 °C / 92 bars / 96.5% CO2 using real PIA23791 right globe)
  6. code_graphic_064_r12b_venus_pressure_v02.mp4          (7.00 s, 92 bars = 930 m underwater scale gauge using real PIA23791 right globe)
  7. code_graphic_064_r14_venus_spin_v02.mp4               (7.25 s, 243-day backwards spin vs 225-day orbit using real PIA23791 right globe)
  8. code_graphic_064_r43b_saturn_rings_v02.mp4            (6.00 s, 282,000 km radial rings / 10 m thick / 0.41 Mimas mass)
  9. code_graphic_064_r54b_uranus_core_v02.mp4             (6.00 s, >=80% hot dense fluid / 4,982 °C near core / ~60° magnetic tilt)

All renders are 1920x1080, 24 fps CFR, libx264 yuv420p, lifted navy (never near-black), real NASA planet bodies,
<= 4 words per label verbatim from locked v04 script / VO v01, continuous smooth motion, £0 spend.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess as sp
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 24
BW, BH = 2160, 1220
HARV_064 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/03_Reference-Material/harvest_J3022_v01")
HARV_033 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01")
OUT_NAS = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/04_Generated-Clips/J3023_code_graphics_v02")
PREV_NAS = OUT_NAS / "previews"
REPO_PROJ = Path(__file__).resolve().parents[1]
REPO_CG = REPO_PROJ / "04_Generated-Clips/J3023_code_graphics_v02"
EDIT_DIR = Path(__file__).resolve().parent

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
GOLD = (255, 224, 0, 255)
CYAN = (105, 225, 250, 255)
CORAL = (255, 118, 72, 255)
WHITE = (248, 250, 255, 255)
MUTED = (182, 204, 232, 255)
NAVY_CARD = (20, 36, 68, 228)

_FC: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}


def fnt(sz: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    k = (sz, bold)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, sz)
    return _FC[k]


def ease(t: float, a: float, b: float) -> float:
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    x = (t - a) / (b - a)
    return x * x * (3.0 - 2.0 * x)


def make_bg(seed: int, tint: tuple[int, int, int] = (24, 44, 84)) -> Image.Image:
    """Lifted-navy astronomical grid + stars + fine grain (mean luma ~44 -> never near-black)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    rx = (xx - BW * 0.5) / (BW * 0.55)
    ry = (yy - BH * 0.5) / (BH * 0.55)
    rad = np.sqrt(rx * rx + ry * ry)
    wave = 0.5 + 0.5 * np.sin(xx * 0.008 + yy * 0.006 + seed)
    r = np.clip(tint[0] + 24.0 * (1.0 - np.clip(rad, 0, 1)) + 8.0 * wave, 20, 255)
    g = np.clip(tint[1] + 34.0 * (1.0 - np.clip(rad, 0, 1)) + 10.0 * wave, 30, 255)
    b = np.clip(tint[2] + 54.0 * (1.0 - np.clip(rad, 0, 1)) + 14.0 * wave, 54, 255)
    arr = np.stack([r, g, b], axis=-1)
    grain = rng.normal(0.0, 2.2, size=(BH, BW, 1)).astype(np.float32)
    img = Image.fromarray(np.clip(arr + grain, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    for rr in (260, 440, 640, 860):
        d.arc((BW // 2 - rr, BH // 2 - rr, BW // 2 + rr, BH // 2 + rr), 15, 165, fill=(100, 160, 230, 58), width=2)
        d.arc((BW // 2 - rr, BH // 2 - rr, BW // 2 + rr, BH // 2 + rr), 195, 345, fill=(100, 160, 230, 58), width=2)
    for _ in range(900):
        sx, sy = int(rng.integers(4, BW - 4)), int(rng.integers(4, BH - 4))
        br = int(rng.integers(165, 255))
        sz = int(rng.choice([1, 1, 1, 2, 2]))
        d.ellipse((sx - sz, sy - sz, sx + sz, sy + sz), fill=(br, br, 255, 220))
    return img


def load_globe(path: Path, diam: int, sat: float = 1.35, pre_crop: tuple[int, int, int, int] | None = None) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if pre_crop is not None:
        im = im.crop(pre_crop)
    L = np.asarray(im.convert("L"))
    ys, xs = np.where(L > 18)
    if len(xs) > 100:
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        side = max(x1 - x0, y1 - y0)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        half = side // 2 + int(side * 0.02)
        im = im.crop((max(0, cx - half), max(0, cy - half), min(im.width, cx + half), min(im.height, cy + half)))
    im = im.resize((diam, diam), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    mask = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, diam - 2, diam - 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def load_saturn_rings(path: Path, max_w: int = 460, sat: float = 1.25) -> Image.Image:
    """Aspect-preserving Saturn + rings cutout on soft-feathered alpha (never squashed into a square)."""
    im = Image.open(path).convert("RGB")
    L = np.asarray(im.convert("L"))
    ys, xs = np.where(L > 14)
    if len(xs) > 100:
        x0, x1, y0, y1 = max(0, int(xs.min()) - 24), min(im.width, int(xs.max()) + 24), max(0, int(ys.min()) - 24), min(im.height, int(ys.max()) + 24)
        im = im.crop((x0, y0, x1, y1))
    s = max_w / float(im.width)
    nw, nh = max_w, max(64, int(round(im.height * s)))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    # Softly fade outer dark background into alpha so Saturn + rings float cleanly on the lifted navy canvas
    lum = np.asarray(im.convert("L")).astype(np.float32)
    alpha = np.clip((lum - 8.0) / 18.0, 0.0, 1.0)
    # Feather outer 14 px border
    xx = np.minimum(np.arange(nw), np.arange(nw)[::-1]).astype(np.float32)
    yy = np.minimum(np.arange(nh), np.arange(nh)[::-1]).astype(np.float32)
    edge = np.outer(np.clip(yy / 14.0, 0.0, 1.0), np.clip(xx / 14.0, 0.0, 1.0))
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray((alpha * edge * 255.0).astype(np.uint8), "L"))
    return out


def pill(d: ImageDraw.ImageDraw, x: int, y: int, text: str, col=WHITE, sz: int = 44, fill=NAVY_CARD, border=(110, 175, 245, 190)):
    font = fnt(sz, True)
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad_x, pad_y = 26, 14
    d.rounded_rectangle((x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y), radius=14, fill=fill, outline=border, width=3)
    d.text((x + pad_x, y + pad_y - bb[1]), text, font=font, fill=col)


def draw_progress_bar(d: ImageDraw.ImageDraw, active_idx: int, p: float, y: int = 930):
    names = ["MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"]
    x0, x1 = 150, 1770
    d.line((x0, y, x1, y), fill=(90, 130, 185, 160), width=5)
    fill_x = min(x1, max(x0, x0 + int((x1 - x0) * ((active_idx - 1) / 7.0) * p)))
    d.line((x0, y, fill_x, y), fill=GOLD, width=6)
    for i, nm in enumerate(names, 1):
        cx = x0 + int((x1 - x0) * (i - 1) / 7.0)
        r = 18 if i == active_idx else 11
        col = GOLD if i == active_idx else (CYAN if i < active_idx else (110, 140, 180, 220))
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=col, outline=WHITE if i == active_idx else None, width=3)
        f = fnt(24 if i == active_idx else 20, True)
        bb = d.textbbox((0, 0), nm, font=f)
        d.text((cx - (bb[2] - bb[0]) // 2, y + 26), nm, font=f, fill=GOLD if i == active_idx else MUTED)


def render_mp4(name: str, dur_s: float, seed: int, tint: tuple[int, int, int], draw_fn) -> dict:
    bg = make_bg(seed, tint)
    out_path = OUT_NAS / name
    n_frames = max(24, int(round(dur_s * FPS)))
    mid_idx = n_frames // 2
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-fps_mode", "cfr", "-g", str(FPS),
        "-movflags", "+faststart", str(out_path)
    ]
    proc = sp.Popen(cmd, stdin=sp.PIPE)
    assert proc.stdin is not None
    max_dx, max_dy = BW - W, BH - H
    for i in range(n_frames):
        t = i / FPS
        u = i / max(1, n_frames - 1)
        ox = int(round(max_dx * (0.1 + 0.8 * u)))
        oy = int(round(max_dy * (0.5 + 0.25 * math.sin(u * math.pi))))
        frame = bg.crop((ox, oy, ox + W, oy + H)).copy()
        draw_fn(frame, t, dur_s)
        rgb = frame.convert("RGB")
        if i == mid_idx:
            PREV_NAS.mkdir(parents=True, exist_ok=True)
            rgb.save(PREV_NAS / (Path(name).stem + "_mid.jpg"), quality=90)
        proc.stdin.write(rgb.tobytes())
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg failed for {name} rc={rc}")
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    return {
        "file": name, "path": str(out_path), "duration_s": dur_s,
        "fps": FPS, "width": W, "height": H, "sha256": sha, "bytes": out_path.stat().st_size,
    }


def main() -> int:
    OUT_NAS.mkdir(parents=True, exist_ok=True)
    PREV_NAS.mkdir(parents=True, exist_ok=True)
    REPO_CG.mkdir(parents=True, exist_ok=True)

    g_merc = load_globe(HARV_064 / "PIA15162.jpg", 360)
    # Real Mariner 10 Venus right colour-enhanced globe only (cleanly cropped past x=1160 divider; ZERO PIA00271!)
    g_ven = load_globe(HARV_064 / "PIA23791.jpg", 340, sat=1.30, pre_crop=(1160, 0, 2245, 1096))
    g_sat = load_saturn_rings(HARV_064 / "PIA11141.jpg", 460)
    g_ura = load_globe(HARV_033 / "PIA18182.jpg", 360)

    manifest = []

    # 1) Revised sleek 8-planet progress strip highlighting 01 / 08 · MERCURY (frame 0 overlay)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    # Clean bottom strip bar (y=935..1045) so frame 0 sells the 8-world journey unobtrusively
    od.rounded_rectangle((70, 938, 1850, 1044), radius=18, fill=(14, 24, 46, 218), outline=(110, 175, 245, 185), width=2)
    pill(od, 92, 954, "01 / 08 · MERCURY", col=GOLD, sz=34, fill=(24, 42, 78, 245), border=GOLD)
    names = ["MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE"]
    x0, x1, yy = 540, 1790, 976
    od.line((x0, yy, x1, yy), fill=(95, 132, 185, 175), width=4)
    for i, nm in enumerate(names, 1):
        cx = x0 + int((x1 - x0) * (i - 1) / 7.0)
        r = 14 if i == 1 else 8
        col = GOLD if i == 1 else (120, 152, 195, 220)
        od.ellipse((cx - r, yy - r, cx + r, yy + r), fill=col, outline=WHITE if i == 1 else None, width=2)
        f = fnt(19 if i == 1 else 16, True)
        bb = od.textbbox((0, 0), nm, font=f)
        od.text((cx - (bb[2] - bb[0]) // 2, yy + 20), nm, font=f, fill=GOLD if i == 1 else MUTED)
    ov_path = OUT_NAS / "code_graphic_064_ch01_mercury_progress_strip_v02.png"
    ov.save(ov_path)
    manifest.append({
        "file": ov_path.name, "path": str(ov_path), "kind": "overlay_png",
        "sha256": hashlib.sha256(ov_path.read_bytes()).hexdigest(), "bytes": ov_path.stat().st_size,
    })
    print("OK", ov_path.name, flush=True)

    # 2) Split Mercury Sunlight graphic (R03b, 3.80 s)
    def r03a_sunlight(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.20, 2.30)
        p2 = ease(t, 1.40, 3.10)
        frame.alpha_composite(g_merc, (150, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "MERCURY · 58 MILLION KM", col=GOLD, sz=52)
        d.rounded_rectangle((620, 290, 1750, 410), radius=16, fill=(32, 46, 78, 225), outline=CORAL, width=3)
        d.rounded_rectangle((624, 294, 624 + max(18, int(1100 * p)), 406), radius=14, fill=CORAL)
        d.text((650, 318), f"+{int(round(430 * p))} °C DAY", font=fnt(54), fill=WHITE)
        if p2 > 0.02:
            pill(d, 620, 480, "UP TO 7× SUNLIGHT", col=GOLD, sz=52)
            pill(d, 620, 620, "WITHOUT AN ATMOSPHERE", col=CYAN, sz=44)
        draw_progress_bar(d, 1, 1.0, y=935)

    # 3) Split Mercury Night graphic (R03d, 3.60 s, DATA #1 / NUMBER OBJECT Ch 1)
    def r03b_night(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.20, 2.20)
        p2 = ease(t, 1.30, 3.00)
        frame.alpha_composite(g_merc, (150, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "NIGHT PLUNGE", col=CYAN, sz=52)
        # Reference +430 C top bar + animated -180 C night plunge bar
        d.rounded_rectangle((620, 275, 1750, 375), radius=14, fill=(32, 46, 78, 220), outline=CORAL, width=3)
        d.rounded_rectangle((624, 279, 1744, 371), radius=12, fill=(210, 92, 58, 235))
        d.text((648, 298), "+430 °C DAY", font=fnt(46), fill=WHITE)
        d.rounded_rectangle((620, 445, 1750, 565), radius=16, fill=(32, 46, 78, 225), outline=CYAN, width=3)
        d.rounded_rectangle((624, 449, 624 + max(18, int(680 * p)), 561), radius=14, fill=CYAN)
        d.text((648, 474), f"-{int(round(180 * p))} °C NIGHT", font=fnt(54), fill=(12, 22, 42, 255))
        if p2 > 0.02:
            pill(d, 620, 640, "WITHOUT AN ATMOSPHERE", col=GOLD, sz=46)
        draw_progress_bar(d, 1, 1.0, y=935)

    # 4) Venus Chapter Card v02 (uses real Mariner 10 PIA23791 right globe — zero PIA00271!)
    def ch02_venus(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.10, 0.70)
        frame.alpha_composite(g_ven, (220, 270))
        d = ImageDraw.Draw(frame)
        pill(d, 640, 310, "02 / 08 · VENUS", col=GOLD, sz=72)
        if t > 0.35:
            pill(d, 640, 445, "THE BACKWARDS FURNACE", col=WHITE, sz=52)
        draw_progress_bar(d, 2, p, y=910)

    # 5) Venus Greenhouse v02 (10.00 s, staggered beats so motion continues across clip, real PIA23791)
    def r12_venus_gh(frame: Image.Image, t: float, dur: float):
        p1 = ease(t, 0.3, 3.0)
        p2 = ease(t, 2.8, 5.8)
        p3 = ease(t, 5.2, 8.2)
        frame.alpha_composite(g_ven, (140, 310))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "HOTTEST PLANETARY SURFACE", col=GOLD, sz=52)
        bars = [
            (280, f"{int(round(464 * p1))} °C SURFACE", CORAL, 1040 * p1),
            (435, f"{int(round(92 * p2))} BARS PRESSURE", GOLD, 920 * p2),
            (590, "96.5% CARBON DIOXIDE", CYAN, 965 * p3),
        ]
        for yy, lbl, col, bw in bars:
            d.rounded_rectangle((620, yy, 1740, yy + 96), radius=14, fill=(32, 46, 78, 220), outline=col, width=3)
            d.rounded_rectangle((624, yy + 4, 624 + int(max(12, bw)), yy + 92), radius=12, fill=col)
            if bw > 140:
                d.text((645, yy + 22), lbl, font=fnt(44), fill=(12, 22, 42, 255))
        draw_progress_bar(d, 2, 1.0, y=935)

    # 6) Venus Crushing Pressure Depth Scale v02 (7.00 s, real PIA23791)
    def r12b_venus_press(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.5)
        p2 = ease(t, 3.0, 5.5)
        frame.alpha_composite(g_ven, (140, 310))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "92 BARS PRESSURE", col=GOLD, sz=54)
        # Vertical ocean-depth gauge descending to 930 metres underwater
        gx0, gx1, gy0, gy1 = 660, 810, 260, 790
        d.rounded_rectangle((gx0, gy0, gx1, gy1), radius=14, fill=(28, 44, 78, 225), outline=CYAN, width=3)
        fill_h = int((gy1 - gy0 - 8) * p)
        d.rounded_rectangle((gx0 + 4, gy0 + 4, gx1 - 4, gy0 + 4 + max(12, fill_h)), radius=10, fill=CYAN)
        pill(d, 870, 290, f"{int(round(930 * p))} METRES UNDERWATER", col=CYAN, sz=48)
        if p2 > 0.05:
            pill(d, 870, 445, "CRUSHES AT 92 BARS", col=CORAL, sz=46)
            pill(d, 870, 595, "96.5% CARBON DIOXIDE", col=WHITE, sz=44)
        draw_progress_bar(d, 2, 1.0, y=935)

    # 7) Venus Backwards Spin v02 (7.25 s, real PIA23791)
    def r14_venus_spin(frame: Image.Image, t: float, dur: float):
        p1 = ease(t, 0.2, 2.8)
        p2 = ease(t, 2.2, 4.8)
        frame.alpha_composite(g_ven, (180, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "SPINS BACKWARDS", col=GOLD, sz=56)
        d.rounded_rectangle((660, 310, 660 + max(18, int(980 * p1)), 410), radius=14, fill=CORAL)
        d.text((685, 332), f"{int(round(243 * p1))}-DAY BACKWARDS SPIN", font=fnt(44), fill=WHITE)
        d.rounded_rectangle((660, 465, 660 + max(18, int(907 * p2)), 565), radius=14, fill=CYAN)
        if p2 > 0.15:
            d.text((685, 487), f"{int(round(225 * p2))}-DAY ORBIT", font=fnt(44), fill=(12, 22, 42, 255))
        if t > 3.4:
            pill(d, 660, 635, "SUN RISES WEST", col=GOLD, sz=48)
        draw_progress_bar(d, 2, 1.0, y=935)

    # 8) Saturn Rings Scale v02 (6.00 s, breaks up R34 cleanly so zero LONG_RUN!)
    def r43b_sat_rings(frame: Image.Image, t: float, dur: float):
        p1 = ease(t, 0.25, 2.6)
        p2 = ease(t, 2.3, 4.6)
        frame.alpha_composite(g_sat, (85, 360))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "SATURN'S VANISHING RINGS", col=GOLD, sz=52)
        d.rounded_rectangle((600, 275, 600 + max(18, int(1100 * p1)), 375), radius=14, fill=GOLD)
        d.text((625, 298), f"{int(round(282000 * p1)):,} KM RADIAL", font=fnt(44), fill=(12, 22, 42, 255))
        pill(d, 600, 445, "10 METRES THICK", col=CORAL, sz=48)
        if p2 > 0.05:
            pill(d, 600, 590, "0.41 MIMAS MASS", col=CYAN, sz=46)
            pill(d, 1150, 590, "10–100 MILLION YEARS", col=WHITE, sz=42)
        draw_progress_bar(d, 6, 1.0, y=935)

    # 9) Uranus Interior & Core v02 (6.00 s, breaks up R43 cleanly so zero LONG_RUN!)
    def r54b_ura_core(frame: Image.Image, t: float, dur: float):
        p1 = ease(t, 0.25, 2.8)
        p2 = ease(t, 2.4, 4.8)
        frame.alpha_composite(g_ura, (140, 300))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "URANUS INTERIOR HEAT", col=GOLD, sz=54)
        d.rounded_rectangle((620, 285, 620 + max(18, int(1040 * 0.80 * p1)), 385), radius=14, fill=CORAL)
        d.text((645, 308), "≥80% HOT DENSE FLUID", font=fnt(44), fill=WHITE)
        d.rounded_rectangle((620, 455, 1660, 555), radius=14, fill=(32, 46, 78, 225), outline=GOLD, width=3)
        d.rounded_rectangle((624, 459, 624 + max(18, int(1032 * p2)), 551), radius=12, fill=GOLD)
        if p2 > 0.05:
            d.text((645, 478), f"{int(round(4982 * p2)):,} °C NEAR CORE", font=fnt(44), fill=(12, 22, 42, 255) if p2 > 0.52 else WHITE)
        pill(d, 620, 635, "NEARLY 60° MAGNETIC TILT", col=CYAN, sz=46)
        draw_progress_bar(d, 7, 1.0, y=935)

    specs = [
        ("code_graphic_064_r03a_mercury_sunlight.mp4", 3.80, 6431, (44, 34, 48), r03a_sunlight),
        ("code_graphic_064_r03b_mercury_night.mp4", 3.60, 6432, (20, 42, 78), r03b_night),
        ("code_graphic_064_ch02_card_venus_v02.mp4", 3.00, 6433, (54, 34, 24), ch02_venus),
        ("code_graphic_064_r12_venus_greenhouse_v02.mp4", 10.00, 6434, (54, 34, 28), r12_venus_gh),
        ("code_graphic_064_r12b_venus_pressure_v02.mp4", 7.00, 6435, (40, 38, 62), r12b_venus_press),
        ("code_graphic_064_r14_venus_spin_v02.mp4", 7.25, 6436, (48, 34, 34), r14_venus_spin),
        ("code_graphic_064_r43b_saturn_rings_v02.mp4", 6.00, 6437, (44, 42, 38), r43b_sat_rings),
        ("code_graphic_064_r54b_uranus_core_v02.mp4", 6.00, 6438, (22, 46, 76), r54b_ura_core),
    ]
    import sys
    only = set(sys.argv[1:])
    existing_by_name = {}
    if only and (EDIT_DIR / "CODE_GRAPHICS_J3023_v02.json").exists():
        for rec in json.loads((EDIT_DIR / "CODE_GRAPHICS_J3023_v02.json").read_text(encoding="utf-8")):
            existing_by_name[rec["file"]] = rec
    for fname, dur_s, seed, tint, fn in specs:
        if only and fname not in only and fname in existing_by_name:
            manifest.append(existing_by_name[fname])
            continue
        rec = render_mp4(fname, dur_s, seed, tint, fn)
        manifest.append(rec)
        print(f"OK {fname} ({dur_s}s) sha={rec['sha256'][:12]}", flush=True)

    (EDIT_DIR / "CODE_GRAPHICS_J3023_v02.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT_NAS / "CODE_GRAPHICS_J3023_v02.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    sums = "\n".join(f"{m['sha256']}  {m['file']}" for m in manifest) + "\n"
    (REPO_CG / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    (OUT_NAS / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    print(f"DONE: rendered {len(manifest)} v02 OWB:064 code graphics (£0)!", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
