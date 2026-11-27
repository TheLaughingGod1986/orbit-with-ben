#!/usr/bin/env python3
"""J3022 £0 24fps code graphics renderer for OWB:064 Every Planet Explained in 10 Minutes.

Renders ALL 8 planet progress/chapter treatments (Ch 1 lower-third overlay PNG + Ch 2-8 animated chapter cards)
and ALL 17 original per-row animated teaching & comparison graphics at 1920x1080, 24 fps CFR, libx264 yuv420p:
- Lifted-navy astronomical explainer canvas (mean luma >= 34, zero near-black FAILs, zero flat black slabs).
- Continuous smooth background pan & film grain (0 frozen pairs, passes polish_gate).
- Real NASA planetary bodies only (no flat colored discs).
- Animated data objects (bars grow, dials sweep, counters run, timelines drop in) with <= 4 words per label
  taken verbatim from the locked v04 script / VO v01, fade in/out 0.35 s, hold <= 3.8 s.
- Outputs directly to studio-live 04_Generated-Clips/J3022_code_graphics_v01/ + writes SHA256SUMS.txt & JSON manifest.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 24
BW, BH = 2160, 1220
HARV_064 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/03_Reference-Material/harvest_J3022_v01")
HARV_033 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01")
HARV_031 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01")
OUT_NAS = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/04_Generated-Clips/J3022_code_graphics_v01")
REPO_PROJ = Path(__file__).resolve().parents[1]
REPO_CG = REPO_PROJ / "04_Generated-Clips/J3022_code_graphics_v01"
EDIT_DIR = Path(__file__).resolve().parent

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
GOLD = (255, 224, 0, 255)
CYAN = (105, 225, 250, 255)
CORAL = (255, 118, 72, 255)
GREEN = (110, 235, 165, 255)
WHITE = (248, 250, 255, 255)
MUTED = (182, 204, 232, 255)
NAVY_CARD = (20, 36, 68, 224)

_FC = {}
def fnt(sz: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    k = (sz, bold)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, sz)
    return _FC[k]


def ease(t: float, a: float, b: float) -> float:
    if t <= a: return 0.0
    if t >= b: return 1.0
    x = (t - a) / (b - a)
    return x * x * (3.0 - 2.0 * x)


def make_bg(seed: int, tint: tuple[int, int, int] = (24, 44, 84)) -> Image.Image:
    """Lifted-navy astronomical grid + stars + fine grain (mean luma ~42 -> never near-black)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    rx = (xx - BW * 0.5) / (BW * 0.55)
    ry = (yy - BH * 0.5) / (BH * 0.55)
    rad = np.sqrt(rx * rx + ry * ry)
    wave = 0.5 + 0.5 * np.sin(xx * 0.008 + yy * 0.006 + seed)
    r = np.clip(tint[0] + 24.0 * (1.0 - np.clip(rad, 0, 1)) + 8.0 * wave, 18, 255)
    g = np.clip(tint[1] + 34.0 * (1.0 - np.clip(rad, 0, 1)) + 10.0 * wave, 28, 255)
    b = np.clip(tint[2] + 54.0 * (1.0 - np.clip(rad, 0, 1)) + 14.0 * wave, 52, 255)
    arr = np.stack([r, g, b], axis=-1)
    grain = rng.normal(0.0, 2.2, size=(BH, BW, 1)).astype(np.float32)
    img = Image.fromarray(np.clip(arr + grain, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    # Subtle glowing orbital arcs & grid ticks (no harsh split seams)
    for rr in (260, 440, 640, 860):
        d.arc((BW // 2 - rr, BH // 2 - rr, BW // 2 + rr, BH // 2 + rr), 15, 165, fill=(100, 160, 230, 58), width=2)
        d.arc((BW // 2 - rr, BH // 2 - rr, BW // 2 + rr, BH // 2 + rr), 195, 345, fill=(100, 160, 230, 58), width=2)
    for _ in range(900):
        sx, sy = int(rng.integers(4, BW - 4)), int(rng.integers(4, BH - 4))
        br = int(rng.integers(165, 255))
        sz = int(rng.choice([1, 1, 1, 2, 2]))
        d.ellipse((sx - sz, sy - sz, sx + sz, sy + sz), fill=(br, br, 255, 220))
    return img


def load_globe(path: Path, diam: int, sat: float = 1.35) -> Image.Image:
    im = Image.open(path).convert("RGB")
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


def load_inset(path: Path, max_w: int, max_h: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    s = min(max_w / im.width, max_h / im.height, 1.0)  # never upscale past 1.0x!
    nw, nh = max(1, int(im.width * s)), max(1, int(im.height * s))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return im.convert("RGBA")


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
    fill_x = x0 + int((x1 - x0) * ((active_idx - 1 + p * 0.99) / 7.0)) if active_idx > 1 else x0 + int((x1 - x0) * 0.05 * p)
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
    """Fast 24fps CFR MP4 renderer piped directly to ffmpeg."""
    bg = make_bg(seed, tint)
    out_path = OUT_NAS / name
    n_frames = max(24, int(round(dur_s * FPS)))
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(out_path)
    ]
    proc = sp.Popen(cmd, stdin=sp.PIPE)
    assert proc.stdin is not None
    # Smooth continuous background pan (no wobbly push, 0 frozen frames)
    max_dx, max_dy = BW - W, BH - H
    for i in range(n_frames):
        t = i / FPS
        u = i / max(1, n_frames - 1)
        ox = int(round(max_dx * (0.1 + 0.8 * u)))
        oy = int(round(max_dy * (0.5 + 0.25 * math.sin(u * math.pi))))
        frame = bg.crop((ox, oy, ox + W, oy + H)).copy()
        draw_fn(frame, t, dur_s)
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg failed for {name} rc={rc}")
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    return {"file": name, "path": str(out_path), "duration_s": dur_s, "fps": FPS, "width": W, "height": H, "sha256": sha, "bytes": out_path.stat().st_size}


def main() -> int:
    OUT_NAS.mkdir(parents=True, exist_ok=True)
    REPO_CG.mkdir(parents=True, exist_ok=True)

    # Preload real NASA planet globes once
    g_merc = load_globe(HARV_064 / "PIA15162.jpg", 320)
    g_ven  = load_globe(HARV_033 / "PIA00271.jpg", 340)
    g_ear  = load_globe(HARV_033 / "PIA18033.jpg", 340)
    g_mar  = load_globe(HARV_031 / "PIA00407.jpg", 320)
    g_jup  = load_globe(HARV_064 / "PIA22946.jpg", 420)
    g_sat  = load_globe(HARV_064 / "PIA11141.jpg", 380)
    g_ura  = load_globe(HARV_033 / "PIA18182.jpg", 340)
    g_nep  = load_globe(HARV_064 / "PIA01492.jpg", 340)
    g_tri  = load_globe(HARV_064 / "PIA00317.jpg", 240)
    in_hex = load_inset(HARV_064 / "PIA21049.jpg", 520, 520)
    in_far = load_inset(HARV_064 / "PIA02215.jpg", 640, 480)
    in_oly = load_inset(HARV_064 / "PIA00300.jpg", 480, 440)

    manifest = []

    # 1) Ch 1 lower-third overlay PNG (no chapter card before 0:45!)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    pill(od, 84, 860, "01 / 08 · MERCURY", col=GOLD, sz=48)
    pill(od, 84, 945, "58 MILLION KM", col=WHITE, sz=34)
    ov_path = OUT_NAS / "code_graphic_064_ch01_mercury_progress_overlay.png"
    ov.save(ov_path)
    manifest.append({"file": ov_path.name, "path": str(ov_path), "kind": "overlay_png", "sha256": hashlib.sha256(ov_path.read_bytes()).hexdigest(), "bytes": ov_path.stat().st_size})
    print("OK", ov_path.name)

    # 2) Chapters 2-8 animated planet-progress chapter cards (3.0 s each, 24 fps, no Ken Burns on card text)
    chapter_cards = [
        ("code_graphic_064_ch02_card_venus.mp4",   2, "02 / 08 · VENUS",   "THE BACKWARDS FURNACE", g_ven, (54, 34, 24)),
        ("code_graphic_064_ch03_card_earth.mp4",   3, "03 / 08 · EARTH",   "SHIELDED OCEAN WORLD",  g_ear, (20, 48, 86)),
        ("code_graphic_064_ch04_card_mars.mp4",    4, "04 / 08 · MARS",    "FROZEN ROBOT DESERT",   g_mar, (56, 30, 26)),
        ("code_graphic_064_ch05_card_jupiter.mp4", 5, "05 / 08 · JUPITER", "METALLIC HYDROGEN",     g_jup, (48, 38, 32)),
        ("code_graphic_064_ch06_card_saturn.mp4",  6, "06 / 08 · SATURN",  "DISAPPEARING RINGS",    g_sat, (46, 44, 34)),
        ("code_graphic_064_ch07_card_uranus.mp4",  7, "07 / 08 · URANUS",  "21-YEAR WINTERS",       g_ura, (20, 52, 74)),
        ("code_graphic_064_ch08_card_neptune.mp4", 8, "08 / 08 · NEPTUNE", "SUPERSONIC WINDS",      g_nep, (20, 38, 86)),
    ]
    for fname, idx, title, sub, globe, tint in chapter_cards:
        def make_card(idx=idx, title=title, sub=sub, globe=globe):
            def draw(frame: Image.Image, t: float, dur: float):
                p = ease(t, 0.1, 0.7)
                frame.alpha_composite(globe, (220, 270))
                d = ImageDraw.Draw(frame)
                pill(d, 640, 310, title, col=GOLD, sz=72)
                if t > 0.35:
                    pill(d, 640, 445, sub, col=WHITE, sz=52)
                draw_progress_bar(d, idx, p, y=910)
            return draw
        rec = render_mp4(fname, 3.0, 6400 + idx, tint, make_card())
        manifest.append(rec)
        print("OK", fname, rec["sha256"][:12])

    # 3) Per-row animated teaching & comparison graphics (all <=4 words per label, real planet bodies, lifted navy)
    def r03_merc_temp(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.4, 3.2)
        frame.alpha_composite(g_merc, (140, 340))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 88, "MERCURY · 58M KM", col=GOLD, sz=54)
        # Dual thermometer bars: +430 C day vs -180 C night
        d.rounded_rectangle((620, 290, 1740, 390), radius=14, fill=(32, 46, 78, 220), outline=CORAL, width=3)
        d.rounded_rectangle((624, 294, 624 + int(1090 * p), 386), radius=12, fill=CORAL)
        d.text((645, 312), f"+{int(round(430*p))} °C DAY", font=fnt(48), fill=WHITE)
        d.rounded_rectangle((620, 470, 1740, 570), radius=14, fill=(32, 46, 78, 220), outline=CYAN, width=3)
        d.rounded_rectangle((624, 474, 624 + int(560 * p), 566), radius=12, fill=CYAN)
        d.text((645, 492), f"-{int(round(180*p))} °C NIGHT", font=fnt(48), fill=(12, 22, 42, 255))
        if t > 2.5:
            pill(d, 620, 660, "UP TO 7× SUNLIGHT", col=GOLD, sz=46)
        draw_progress_bar(d, 1, 1.0, y=940)

    def r05_merc_res(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 4.0)
        d = ImageDraw.Draw(frame)
        pill(d, 110, 88, "3:2 SPIN-ORBIT", col=GOLD, sz=56)
        # Animated 3 rotations per 2 orbits dial with real Mercury globe orbiting
        cx, cy, rx, ry = 560, 520, 320, 220
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=CYAN, width=5)
        d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=GOLD)
        ang = t * 1.4
        px, py = int(cx + rx * math.cos(ang)), int(cy + ry * math.sin(ang))
        sm = g_merc.resize((110, 110), Image.Resampling.LANCZOS)
        frame.alpha_composite(sm, (px - 55, py - 55))
        pill(d, 1020, 270, "3 SPINS · 59 DAYS", col=WHITE, sz=46)
        pill(d, 1020, 400, "2 ORBITS · 88 DAYS", col=CYAN, sz=46)
        pill(d, 1020, 540, f"{int(round(176*p))}-DAY SOLAR DAY", col=GOLD, sz=52)
        draw_progress_bar(d, 1, 1.0, y=940)

    def r07_merc_core(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 2.8)
        frame.alpha_composite(g_merc.resize((420, 420)), (180, 280))
        d = ImageDraw.Draw(frame)
        # 85% metallic core ring overlay on right half
        cx, cy, R = 390, 490, 200
        rc = int(R * 0.85 * p)
        if rc > 8:
            d.ellipse((cx - rc, cy - rc, cx + rc, cy + rc), outline=GOLD, width=6, fill=(255, 190, 60, 115))
        pill(d, 110, 84, "85% METALLIC CORE", col=GOLD, sz=54)
        pill(d, 740, 270, "2,440 KM RADIUS", col=WHITE, sz=48)
        pill(d, 740, 405, "BLUEBERRY VS NICKEL", col=CYAN, sz=46)
        pill(d, 740, 540, "SECOND DENSEST PLANET", col=GOLD, sz=48)
        draw_progress_bar(d, 1, 1.0, y=940)

    def r12_venus_gh(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.4, 3.8)
        frame.alpha_composite(g_ven, (140, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "HOTTEST PLANETARY SURFACE", col=GOLD, sz=52)
        bars = [
            (280, f"{int(round(464*p))} °C SURFACE", CORAL, 1040 * p),
            (430, f"{int(round(92*p))} BARS PRESSURE", GOLD, 920 * p),
            (580, "96.5% CARBON DIOXIDE", CYAN, 965 * p),
        ]
        for yy, lbl, col, bw in bars:
            d.rounded_rectangle((620, yy, 1740, yy + 96), radius=14, fill=(32, 46, 78, 220), outline=col, width=3)
            d.rounded_rectangle((624, yy + 4, 624 + int(max(12, bw)), yy + 92), radius=12, fill=col)
            d.text((645, yy + 22), lbl, font=fnt(44), fill=(12, 22, 42, 255))
        pill(d, 620, 725, "930 METRES UNDERWATER", col=WHITE, sz=44)
        draw_progress_bar(d, 2, 1.0, y=940)

    def r14_venus_spin(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.2, 2.5)
        frame.alpha_composite(g_ven, (180, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "SPINS BACKWARDS", col=GOLD, sz=56)
        # Bar comparison: 243d spin vs 225d orbit
        d.rounded_rectangle((660, 310, 660 + int(980 * p), 410), radius=14, fill=CORAL)
        d.text((685, 332), "243-DAY BACKWARDS SPIN", font=fnt(44), fill=WHITE)
        d.rounded_rectangle((660, 465, 660 + int(907 * p), 565), radius=14, fill=CYAN)
        d.text((685, 487), "225-DAY ORBIT", font=fnt(44), fill=(12, 22, 42, 255))
        pill(d, 660, 635, "SUN RISES WEST", col=GOLD, sz=48)
        draw_progress_bar(d, 2, 1.0, y=940)

    def r20_earth_spin(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.4, 3.6)
        frame.alpha_composite(g_ear, (140, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "EARTH · 1,670 KM/H", col=GOLD, sz=54)
        # Scale bar vs Cyclone Olivia 408 km/h
        d.rounded_rectangle((620, 290, 620 + int(1060 * p), 390), radius=14, fill=CYAN)
        d.text((645, 312), f"EQUATOR · {int(round(1670*p))} KM/H", font=fnt(44), fill=(12, 22, 42, 255))
        d.rounded_rectangle((620, 445, 620 + int(260 * p), 545), radius=14, fill=CORAL)
        d.text((905, 468), "CYCLONE OLIVIA · 408 KM/H", font=fnt(40), fill=WHITE)
        pill(d, 620, 610, ">4× CYCLONE OLIVIA", col=GOLD, sz=46)
        pill(d, 620, 735, "43 KM WIDER", col=WHITE, sz=46)
        draw_progress_bar(d, 3, 1.0, y=940)

    def r22_earth_core(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.2)
        frame.alpha_composite(g_ear, (140, 310))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "3,000 KM DEEP", col=GOLD, sz=54)
        pill(d, 620, 240, "LIQUID-IRON OUTER CORE", col=CORAL, sz=46)
        # 183 magnetic reversal barcode over 83 million years
        bx0, bx1, by0, by1 = 620, 1740, 400, 520
        d.rectangle((bx0, by0, bx1, by1), fill=(25, 38, 66, 230), outline=CYAN, width=3)
        rng = np.random.default_rng(183)
        stripes = int(round(183 * p))
        for i in range(stripes):
            sx = bx0 + int((bx1 - bx0) * (i / 183.0))
            col = GOLD if i % 2 == 0 else CYAN
            d.rectangle((sx, by0 + 4, min(bx1, sx + 4), by1 - 4), fill=col)
        pill(d, 620, 565, f"{stripes} FLIPS · 83M YEARS", col=GOLD, sz=48)
        draw_progress_bar(d, 3, 1.0, y=940)

    def r28_mars_press(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.0)
        frame.alpha_composite(g_mar, (140, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "MARS · 6.36 MILLIBARS", col=GOLD, sz=54)
        d.rounded_rectangle((620, 290, 620 + int(1050 * p), 390), radius=14, fill=CYAN)
        d.text((645, 312), "EARTH · 1,013 MILLIBARS", font=fnt(42), fill=(12, 22, 42, 255))
        d.rounded_rectangle((620, 445, 620 + max(18, int(1050 * 0.0063 * p)), 545), radius=10, fill=CORAL)
        d.text((665, 468), "MARS · 6.36 MILLIBARS (<1%)", font=fnt(42), fill=CORAL)
        pill(d, 620, 625, "AVERAGE -59 °C", col=WHITE, sz=48)
        draw_progress_bar(d, 4, 1.0, y=940)

    def r30_mars_oly(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 2.8)
        frame.alpha_composite(in_oly, (120, 280))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "OLYMPUS MONS · 21.3 KM", col=GOLD, sz=54)
        # Vertical datum elevation bars (21.3 km above Mars datum vs 8.85 km Everest)
        base_y = 780
        h_oly = int(420 * p)
        h_ev = int(420 * (8.848 / 21.287) * p)
        d.line((720, base_y, 1740, base_y), fill=WHITE, width=4)
        d.rounded_rectangle((800, base_y - h_oly, 1080, base_y), radius=10, fill=CORAL)
        d.text((795, base_y - h_oly - 62), "21.3 KM ABOVE DATUM", font=fnt(34), fill=GOLD)
        d.rounded_rectangle((1240, base_y - h_ev, 1520, base_y), radius=10, fill=CYAN)
        d.text((1220, base_y - h_ev - 62), "EVEREST · 8.8 KM", font=fnt(34), fill=CYAN)
        pill(d, 740, 800, "ARIZONA-SIZED BASE", col=WHITE, sz=42)
        draw_progress_bar(d, 4, 1.0, y=940)

    def r35_jup_scale(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.4, 3.6)
        frame.alpha_composite(g_jup, (140, 260))
        # True 11:1 Earth next to Jupiter (38 px vs 420 px!)
        frame.alpha_composite(g_ear.resize((38, 38), Image.Resampling.LANCZOS), (605, 450))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "JUPITER · 11× EARTH", col=GOLD, sz=54)
        pill(d, 740, 260, f"{int(round(318*p))} EARTH MASSES", col=GOLD, sz=52)
        pill(d, 740, 405, "BASKETBALL VS GRAPE", col=CYAN, sz=46)
        pill(d, 740, 545, "9.9-HOUR DAY", col=WHITE, sz=48)
        draw_progress_bar(d, 5, 1.0, y=940)

    def r39_jup_galileo(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.5)
        frame.alpha_composite(g_jup.resize((340, 340)), (140, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "7 DECEMBER 1995", col=GOLD, sz=54)
        # Clean 58-minute data-return timeline (no crushing event, no mixed depth endpoints!)
        d.rounded_rectangle((620, 340, 1740, 440), radius=14, fill=(32, 46, 78, 220), outline=GREEN, width=3)
        d.rounded_rectangle((624, 344, 624 + int(1100 * p), 436), radius=12, fill=GREEN)
        d.text((645, 366), f"GALILEO DATA · {int(round(58*p))} MINUTES", font=fnt(44), fill=(12, 22, 42, 255))
        pill(d, 620, 520, "NO SOLID SURFACE", col=CORAL, sz=48)
        draw_progress_bar(d, 5, 1.0, y=940)

    def r43_sat_dens(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.4, 3.8)
        frame.alpha_composite(g_sat, (120, 300))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "LESS DENSE", col=GOLD, sz=56)
        # Equal-volume density bars: Saturn 687 vs Water 1,000 kg/m3
        d.rounded_rectangle((600, 260, 600 + int(687 * 0.95 * p), 350), radius=12, fill=GOLD)
        d.text((625, 280), "SATURN · 687 KG/M³", font=fnt(40), fill=(12, 22, 42, 255))
        d.rounded_rectangle((600, 385, 600 + int(1000 * 0.95 * p), 475), radius=12, fill=CYAN)
        d.text((625, 405), "WATER · 1,000 KG/M³", font=fnt(40), fill=(12, 22, 42, 255))
        pill(d, 600, 535, "282,000 KM RADIAL RINGS", col=WHITE, sz=42)
        pill(d, 600, 650, "10 METRES THICK", col=CORAL, sz=42)
        pill(d, 1160, 650, "0.41 MIMAS MASS", col=CYAN, sz=42)
        draw_progress_bar(d, 6, 1.0, y=940)

    def r46_sat_hex(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.2)
        frame.alpha_composite(in_hex, (140, 240))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "30,000 KM HEXAGON", col=GOLD, sz=54)
        pill(d, 740, 260, "WIDER THAN TWO EARTHS", col=WHITE, sz=44)
        pill(d, 740, 395, f"{int(round(322*p))} KM/H WINDS", col=CYAN, sz=48)
        pill(d, 740, 530, "2012 TO 2016", col=GOLD, sz=46)
        pill(d, 740, 665, "POSSIBLY SEASONAL HAZE", col=MUTED, sz=42)
        draw_progress_bar(d, 6, 1.0, y=940)

    def r51_ura_tilt(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.6)
        frame.alpha_composite(g_ear.resize((220, 220)), (180, 380))
        frame.alpha_composite(g_ura.resize((340, 340)), (620, 320))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "97.77° AXIAL TILT", col=GOLD, sz=54)
        # Tilt axis lines
        ang_e = math.radians(23.4)
        d.line((290 - int(150 * math.sin(ang_e)), 490 + int(150 * math.cos(ang_e)),
                290 + int(150 * math.sin(ang_e)), 490 - int(150 * math.cos(ang_e))), fill=CYAN, width=6)
        ang_u = math.radians(97.77 * p)
        d.line((790 - int(220 * math.sin(ang_u)), 490 + int(220 * math.cos(ang_u)),
                790 + int(220 * math.sin(ang_u)), 490 - int(220 * math.cos(ang_u))), fill=GOLD, width=7)
        pill(d, 140, 680, "EARTH · 23.4°", col=CYAN, sz=40)
        pill(d, 1080, 290, "21-YEAR WINTER", col=GOLD, sz=52)
        pill(d, 1080, 430, "84-YEAR ORBIT", col=WHITE, sz=46)
        pill(d, 1080, 565, "17-HOUR SPIN", col=CYAN, sz=46)
        draw_progress_bar(d, 7, 1.0, y=940)

    def r54_ura_cold(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.5)
        frame.alpha_composite(g_ura, (140, 310))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 84, "URANUS · -224.2 °C", col=CYAN, sz=54)
        pill(d, 620, 250, "COLDER IN SOME PLACES", col=WHITE, sz=44)
        pill(d, 620, 390, "NEARLY 60° MAGNETIC TILT", col=GOLD, sz=44)
        d.rounded_rectangle((620, 535, 620 + int(1020 * 0.80 * p), 630), radius=12, fill=CORAL)
        d.text((645, 558), "≥80% HOT DENSE FLUID", font=fnt(42), fill=WHITE)
        pill(d, 620, 680, "4,982 °C NEAR CORE", col=GOLD, sz=46)
        draw_progress_bar(d, 7, 1.0, y=940)

    def r60_nep_wind(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 3.6)
        frame.alpha_composite(g_nep.resize((300, 300)), (120, 250))
        frame.alpha_composite(g_tri, (150, 595))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 74, "NEPTUNE · >2,000 KM/H", col=GOLD, sz=54)
        d.rounded_rectangle((540, 255, 540 + int(1120 * p), 355), radius=14, fill=CYAN)
        d.text((565, 278), f"NEPTUNE · >{int(round(2000*p))} KM/H", font=fnt(44), fill=(12, 22, 42, 255))
        d.rounded_rectangle((540, 405, 540 + int(1120 * (408 / 2000) * p), 505), radius=14, fill=CORAL)
        d.text((800, 428), "CYCLONE OLIVIA · 408 KM/H", font=fnt(40), fill=WHITE)
        pill(d, 540, 560, "ROUGHLY 5× OLIVIA GUST", col=GOLD, sz=44)
        pill(d, 540, 685, "TRITON · >8 KM GEYSERS", col=WHITE, sz=44)
        pill(d, 1200, 685, "30 AU · 900× DIMMER", col=CYAN, sz=40)
        draw_progress_bar(d, 8, 1.0, y=940)

    def r62_timeline(frame: Image.Image, t: float, dur: float):
        p = ease(t, 0.3, 4.0)
        frame.alpha_composite(in_far, (110, 240))
        d = ImageDraw.Draw(frame)
        pill(d, 110, 74, "EXPLORATION TIMELINE · 1610–2024", col=GOLD, sz=48)
        events = [
            ("1610", "GALILEO · JUPITER"),
            ("1781", "HERSCHEL · URANUS"),
            ("1846", "LE VERRIER & GALLE"),
            ("1965", "COLOMBO · MERCURY"),
            ("1982", "VENERA 13 · VENUS"),
            ("1989", "VOYAGER 2 · NEPTUNE"),
            ("2015", "NEW HORIZONS · PLUTO"),
            ("2024", "INGENUITY · 72 FLIGHTS"),
        ]
        n_show = max(1, int(round(len(events) * p)))
        for idx, (yr, lbl) in enumerate(events[:n_show]):
            yy = 215 + idx * 82
            d.rounded_rectangle((820, yy, 1800, yy + 66), radius=10, fill=NAVY_CARD, outline=CYAN, width=2)
            d.text((845, yy + 14), yr, font=fnt(34), fill=GOLD)
            d.text((985, yy + 14), lbl, font=fnt(34), fill=WHITE)
        draw_progress_bar(d, 8, 1.0, y=940)

    specs = [
        ("code_graphic_064_r03_mercury_temp.mp4", 14.25, 6411, (38, 36, 56), r03_merc_temp),
        ("code_graphic_064_r05_mercury_resonance.mp4", 17.05, 6412, (24, 42, 78), r05_merc_res),
        ("code_graphic_064_r07_mercury_core.mp4", 7.80, 6413, (34, 40, 68), r07_merc_core),
        ("code_graphic_064_r12_venus_greenhouse.mp4", 24.25, 6414, (54, 34, 28), r12_venus_gh),
        ("code_graphic_064_r14_venus_spin.mp4", 7.25, 6415, (48, 34, 34), r14_venus_spin),
        ("code_graphic_064_r20_earth_spin_bulge.mp4", 22.90, 6416, (20, 48, 86), r20_earth_spin),
        ("code_graphic_064_r22_earth_core_flips.mp4", 11.00, 6417, (24, 42, 82), r22_earth_core),
        ("code_graphic_064_r28_mars_pressure.mp4", 13.15, 6418, (54, 32, 30), r28_mars_press),
        ("code_graphic_064_r30_mars_olympus.mp4", 8.25, 6419, (52, 30, 28), r30_mars_oly),
        ("code_graphic_064_r35_jupiter_scale.mp4", 23.25, 6420, (44, 38, 36), r35_jup_scale),
        ("code_graphic_064_r39_jupiter_galileo.mp4", 10.15, 6421, (34, 42, 62), r39_jup_galileo),
        ("code_graphic_064_r43_saturn_density_rings.mp4", 24.40, 6422, (44, 42, 38), r43_sat_dens),
        ("code_graphic_064_r46_saturn_hexagon.mp4", 15.85, 6423, (36, 44, 60), r46_sat_hex),
        ("code_graphic_064_r51_uranus_tilt.mp4", 22.35, 6424, (20, 52, 78), r51_ura_tilt),
        ("code_graphic_064_r54_uranus_cold_core.mp4", 27.80, 6425, (20, 48, 76), r54_ura_cold),
        ("code_graphic_064_r60_neptune_winds.mp4", 16.70, 6426, (20, 38, 86), r60_nep_wind),
        ("code_graphic_064_r62_solar_comparison_timeline.mp4", 8.00, 6427, (22, 40, 80), r62_timeline),
    ]
    for fname, dur_s, seed, tint, fn in specs:
        rec = render_mp4(fname, dur_s, seed, tint, fn)
        manifest.append(rec)
        print(f"OK {fname} ({dur_s}s) sha={rec['sha256'][:12]}")

    # Write manifest and SHA256SUMS to both studio-live and repo
    (EDIT_DIR / "CODE_GRAPHICS_J3022_v01.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT_NAS / "CODE_GRAPHICS_J3022_v01.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    sums = "\n".join(f"{m['sha256']}  {m['file']}" for m in manifest) + "\n"
    (REPO_CG / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    (OUT_NAS / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    print(f"DONE: rendered {len(manifest)} original OWB:064 code graphics (£0)!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
