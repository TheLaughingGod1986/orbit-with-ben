#!/usr/bin/env python3
"""J2299 £0 24fps code graphics for film 033 (Why This Planet Has 21-Year Winters).

Fixes all J2297 Chief review and J2299 Codex audit findings:
1. Rendered at 24 fps (1920x1080, libx264 yuv420p CRF 18), replacing 12 fps drafts.
2. Continuous background starfield + graded NASA plate motion on every frame (0 frozen pairs).
3. Visual stage transitions at exact sub-cut boundaries every 3.3-5.6 s matching cuts_033_j2299_v01.json.
4. Animated cards fade in/out over 0.35 s, hold <= 3.8 s (< 4.0 s lock), <= 4 words per label, one label at a time.
5. Corner credit in white Didot italic appears only when no main label card is on screen.
6. Real globes only: PIA18182 (Uranus), PIA18033 (Earth), PIA01492 (Neptune), PIA01490 (Miranda), PIA00405 (Moon).
   True 1:4 Earth:Uranus diameter ratio in R14 (140 px vs 560 px) and true 1:7 Miranda:Moon ratio in R59 (90 px vs 630 px).
7. Retires code_graphic_033_r55_pressure_gauge.mp4 per J2386 (R55 uses accepted 3-cut passage r55_passage_v01_silent.mp4).
   Writes byte-identical R26 alias code_graphic_033_r26_axial_tilt_97deg.mp4.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
BW, BH = 2320, 1320  # Oversized canvas for continuous smooth pan
NAVY = (12, 22, 42)
GOLD = (255, 210, 72, 255)
CYAN = (110, 220, 245, 255)
CORAL = (245, 115, 80, 255)
WHITE = (248, 248, 242, 255)

HARV = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01")
OUT_NAS = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2299_code_graphics_v01")
HERE = Path(__file__).resolve().parent

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

_FONT_CACHE: dict[tuple[str, int, int], ImageFont.FreeTypeFont] = {}


def get_font(size: int, italic_credit: bool = False) -> ImageFont.FreeTypeFont:
    key = (FONT_DIDOT if italic_credit else FONT_BOLD, size, 1 if italic_credit else 0)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(key[0], size, index=key[2])
        except Exception:
            _FONT_CACHE[key] = ImageFont.truetype(FONT_BOLD, size)
    return _FONT_CACHE[key]


def ease(t: float, a: float, b: float) -> float:
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    x = (t - a) / (b - a)
    return x * x * (3.0 - 2.0 * x)


def card_alpha(t: float, t_start: float, t_end: float, fade: float = 0.35) -> float:
    if t_end - t_start > 3.95:
        t_end = t_start + 3.85
    if t <= t_start or t >= t_end:
        return 0.0
    if t < t_start + fade:
        return ease(t, t_start, t_start + fade)
    if t > t_end - fade:
        return 1.0 - ease(t, t_end - fade, t_end)
    return 1.0


def build_oversized_plate(path: Path, mix: float = 0.34, seed: int = 33) -> Image.Image:
    rng = np.random.default_rng(seed)
    im = Image.open(path).convert("RGB")
    scale = max(BW / im.width, BH / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left, top = (im.width - BW) // 2, (im.height - BH) // 2
    im = im.crop((left, top, left + BW, top + BH))

    arr = np.asarray(im, dtype=np.float32)
    yy, xx = np.mgrid[0:BH, 0:BW]
    # Rich radial deep-space cosmic gradient + subtle nebula waves so foreground globes pop cleanly
    rx = (xx - BW * 0.5) / (BW * 0.5)
    ry = (yy - BH * 0.5) / (BH * 0.5)
    rad = np.sqrt(rx * rx + ry * ry)
    wave = 0.5 + 0.5 * np.sin(xx * 0.011 + yy * 0.007 + seed)
    base_r = 16.0 + 22.0 * (1.0 - np.clip(rad, 0, 1)) + 8.0 * wave
    base_g = 28.0 + 36.0 * (1.0 - np.clip(rad, 0, 1)) + 12.0 * wave
    base_b = 54.0 + 58.0 * (1.0 - np.clip(rad, 0, 1)) + 18.0 * wave
    base = np.stack([base_r, base_g, base_b], axis=-1)

    blended = base * (1.0 - mix) + arr * mix
    # Add fine film grain
    grain = rng.normal(0.0, 2.6, size=(BH, BW, 1)).astype(np.float32)
    blended = np.clip(blended + grain, 0, 255).astype(np.uint8)
    canvas = Image.fromarray(blended, mode="RGB").convert("RGBA")

    # Draw dense starfield + astronomical coordinate rings (no full-frame straight lines -> 0 seams, high edge density)
    d = ImageDraw.Draw(canvas)
    for r_ring in (220, 360, 500, 650, 800, 960):
        d.arc((BW // 2 - r_ring, BH // 2 - r_ring, BW // 2 + r_ring, BH // 2 + r_ring), 12, 168, fill=(95, 145, 205, 75), width=2)
        d.arc((BW // 2 - r_ring, BH // 2 - r_ring, BW // 2 + r_ring, BH // 2 + r_ring), 192, 348, fill=(95, 145, 205, 75), width=2)

    for _ in range(1800):
        sx = int(rng.integers(6, BW - 6))
        sy = int(rng.integers(6, BH - 6))
        br = int(rng.integers(145, 255))
        sz = int(rng.choice([1, 1, 1, 2, 2, 3]))
        col = (br, min(255, br + 10), min(255, br + 25), 240)
        d.ellipse((sx - sz, sy - sz, sx + sz, sy + sz), fill=col)

    return canvas


def make_globe(path: Path, diameter: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((diameter, diameter), Image.Resampling.LANCZOS)
    circle = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(circle).ellipse((2, 2, diameter - 3, diameter - 3), fill=255)
    sky = im.convert("L").point(lambda p: 0 if p < 10 else 255)
    alpha = ImageChops.multiply(circle, sky)
    out = im.convert("RGBA")
    out.putalpha(alpha)
    # Add crisp rim glow so small/large globes read clearly
    ImageDraw.Draw(out).ellipse((2, 2, diameter - 3, diameter - 3), outline=(180, 225, 255, 160), width=max(2, diameter // 90))
    return out


def moving_bg(plate: Image.Image, t: float, dur: float, stage_cuts: list[float]) -> Image.Image:
    stage = 0
    for sc in stage_cuts:
        if t >= sc:
            stage += 1
    p = t / max(dur, 0.001)
    # Continuous sub-pixel camera pan + distinct framing step on each stage cut
    fx0 = 30.0 + stage * 85.0 + 180.0 * p
    fy0 = 24.0 + (stage % 2) * 65.0 + 110.0 * p
    fx0 = max(0.0, min(float(BW - W - 1), fx0))
    fy0 = max(0.0, min(float(BH - H - 1), fy0))
    return plate.transform(
        (W, H),
        Image.Transform.EXTENT,
        (fx0, fy0, fx0 + W, fy0 + H),
        Image.Resampling.BILINEAR,
    )


def draw_label_or_credit(
    im: Image.Image,
    t: float,
    cards: list[tuple[float, float, tuple[int, int], str, int, tuple[int, int, int, int]]],
    credit_text: str,
) -> None:
    """Enforces <= 4 words, <= 3.85 s hold, fade in/out, and 1 label at a time (credit hides when card is active)."""
    d = ImageDraw.Draw(im)
    active_card = False
    for t0, t1, xy, words, sz, col in cards:
        if len(words.split()) > 4:
            raise ValueError(f"Label exceeds 4 words: {words!r}")
        a = card_alpha(t, t0, t1)
        if a > 0.02:
            active_card = True
            fnt = get_font(sz, italic_credit=False)
            x, y = xy
            y_anim = int(round(y + (1.0 - a) * 14))
            bbox = d.textbbox((x, y_anim), words, font=fnt)
            pad_x, pad_y = 22, 14
            d.rounded_rectangle(
                (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y),
                radius=16,
                fill=(10, 20, 38, int(215 * a)),
                outline=(col[0], col[1], col[2], int(190 * a)),
                width=3,
            )
            d.text(
                (x, y_anim),
                words,
                font=fnt,
                fill=(col[0], col[1], col[2], int(255 * a)),
                stroke_width=3,
                stroke_fill=(6, 12, 24, int(230 * a)),
            )
            break  # Strictly one label at a time

    if not active_card and credit_text:
        fnt_c = get_font(28, italic_credit=True)
        d.text(
            (38, H - 54),
            credit_text,
            font=fnt_c,
            fill=(235, 240, 248, 215),
            stroke_width=2,
            stroke_fill=(8, 14, 26, 200),
        )


def render_clip(name: str, seconds: float, draw_fn) -> dict:
    frames = max(1, round(seconds * FPS))
    dest = OUT_NAS / name
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-movflags", "+faststart", str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    lumas = []
    stds = []
    prev_arr = None
    diffs = []
    frozen = 0
    try:
        for i in range(frames):
            t = i / FPS
            rgb = draw_fn(t, seconds).convert("RGB")
            arr = np.asarray(rgb, dtype=np.uint8)
            g = arr.mean(axis=2)
            if i in (frames // 4, frames // 2, (3 * frames) // 4):
                lumas.append(float(g.mean()))
                stds.append(float(g.std()))
            if prev_arr is not None:
                diff = float(np.abs(arr.astype(np.int16) - prev_arr.astype(np.int16)).mean())
                diffs.append(diff)
                if diff < 0.05:
                    frozen += 1
            prev_arr = arr
            proc.stdin.write(arr.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed for {name}")
    except BaseException:
        proc.kill()
        raise

    data = dest.read_bytes()
    return {
        "file": name,
        "path": str(dest),
        "seconds": seconds,
        "frames": frames,
        "fps": FPS,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "mid_frame_mean_luma": round(sum(lumas) / max(len(lumas), 1), 2),
        "mid_frame_std_luma": round(sum(stds) / max(len(stds), 1), 2),
        "mean_frame_diff": round(sum(diffs) / max(len(diffs), 1), 3),
        "frozen_pairs": frozen,
        "orbit_character": False,
        "review_status": "READY_FOR_J2300_QA",
    }


def main() -> None:
    OUT_NAS.mkdir(parents=True, exist_ok=True)

    p_uranus = HARV / "PIA18182.jpg"
    p_earth = HARV / "PIA18033.jpg"
    p_neptune = HARV / "PIA01492.jpg"
    p_miranda = HARV / "PIA01490.jpg"
    p_moon = HARV / "PIA00405.jpg"
    p_hubble = HARV / "PIA01280.jpg"
    p_jwst = HARV / "weic2332a_hires.jpg"
    p_verona = HARV / "PIA00044.jpg"
    p_starfield = HARV / "PIA01984.jpg"

    bg_uranus = build_oversized_plate(p_starfield, 0.36, seed=101)
    bg_hubble = build_oversized_plate(p_hubble, 0.42, seed=102)
    bg_miranda = build_oversized_plate(p_starfield, 0.38, seed=103)
    bg_jwst = build_oversized_plate(p_jwst, 0.45, seed=104)
    bg_verona = build_oversized_plate(p_verona, 0.44, seed=105)

    g_u_620 = make_globe(p_uranus, 620)
    g_u_560 = make_globe(p_uranus, 560)
    g_u_460 = make_globe(p_uranus, 460)
    g_u_360 = make_globe(p_uranus, 360)
    g_e_460 = make_globe(p_earth, 460)
    g_e_140 = make_globe(p_earth, 140)  # Exact 1:4 scale with g_u_560 (4 * 140 = 560)
    g_n_460 = make_globe(p_neptune, 460)
    g_mir_90 = make_globe(p_miranda, 90)  # Exact 1:7 scale with g_moon_630 (90 * 7 = 630)
    g_moon_630 = make_globe(p_moon, 630)
    g_jwst_420 = make_globe(p_jwst, 420)

    # R03 (5.19 s): 21-year winter shadow sweep + counter
    def r03(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [])
        gx = int(round(160 + 16 * math.sin(t * 0.6)))
        gy = int(round(210 + 10 * math.cos(t * 0.5)))
        im.alpha_composite(g_u_620, (gx, gy))
        shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        sweep = ease(t, 0.15, dur - 0.35)
        sd.pieslice((gx, gy, gx + 620, gy + 620), 90, 90 + 180 * sweep, fill=(6, 14, 28, 175))
        im.alpha_composite(shade)
        d = ImageDraw.Draw(im)
        # Dial gauge on right
        cx, cy, r = 1340, 520, 230
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(120, 170, 220, 180), width=6)
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * sweep, fill=GOLD, width=14)
        yr = max(1, int(round(21 * sweep)))
        f_num = get_font(96)
        d.text((cx - 55, cy - 55), f"{yr:02d}", font=f_num, fill=GOLD, stroke_width=4, stroke_fill=(8, 14, 28, 230))
        draw_label_or_credit(
            im, t,
            [(0.65, 4.35, (1060, 120), "21 EARTH YEARS", 64, GOLD)],
            "NASA / JPL",
        )
        return im

    # R05 (7.06 s, sub-cut at 4.45 s): Earth 23.44 deg vs Uranus 97.77 deg axial tilt
    def r05(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.45])
        d = ImageDraw.Draw(im)
        if t < 4.45:
            im.alpha_composite(g_e_460, (210, 300))
            im.alpha_composite(g_u_460, (1180, 300))
            e_ang = 23.44 * ease(t, 0.2, 3.6)
            u_ang = 97.77 * ease(t, 0.2, 4.1)
            d.arc((190, 280, 690, 780), -90, -90 + e_ang, fill=CYAN, width=12)
            d.arc((1160, 280, 1660, 780), -90, -90 + u_ang, fill=GOLD, width=12)
            r_e = math.radians(-90 + e_ang)
            r_u = math.radians(-90 + u_ang)
            d.line((440 - 270 * math.cos(r_e), 530 - 270 * math.sin(r_e), 440 + 270 * math.cos(r_e), 530 + 270 * math.sin(r_e)), fill=CYAN, width=6)
            d.line((1410 - 270 * math.cos(r_u), 530 - 270 * math.sin(r_u), 1410 + 270 * math.cos(r_u), 530 + 270 * math.sin(r_u)), fill=GOLD, width=6)
        else:
            # Stage 2: close focus on Uranus 97.77 deg sideways tilt
            im.alpha_composite(g_u_620, (650, 230))
            u_ang = 97.77
            r_u = math.radians(-90 + u_ang)
            cx, cy = 960, 540
            d.arc((cx - 350, cy - 350, cx + 350, cy + 350), -90, -90 + u_ang, fill=GOLD, width=14)
            d.line((cx - 380 * math.cos(r_u), cy - 380 * math.sin(r_u), cx + 380 * math.cos(r_u), cy + 380 * math.sin(r_u)), fill=GOLD, width=8)
        draw_label_or_credit(
            im, t,
            [
                (0.55, 4.15, (200, 110), "EARTH 23.44° TILT", 58, WHITE),
                (4.60, 6.90, (640, 100), "URANUS 97.77° TILT", 64, GOLD),
            ],
            "NASA / JPL",
        )
        return im

    # R08 (10.04 s, sub-cut at 5.02 s): -224.2 C thermometer + real Uranus & Neptune comparison
    def r08(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_hubble, t, dur, [5.02])
        d = ImageDraw.Draw(im)
        if t < 5.02:
            im.alpha_composite(g_u_560, (220, 260))
            drop = ease(t, 0.25, 4.6)
            bx, top, bot = 1280, 200, 860
            d.rounded_rectangle((bx, top, bx + 76, bot), radius=30, outline=WHITE, width=6)
            y = int(round(top + 16 + (bot - top - 32) * drop))
            d.rounded_rectangle((bx + 10, y, bx + 66, bot - 10), radius=18, fill=CYAN)
        else:
            # Stage 2: Uranus (-224.2 C) side by side with real Voyager 2 Neptune PIA01492 (-214 C)
            im.alpha_composite(g_u_460, (240, 300))
            im.alpha_composite(g_n_460, (1220, 300))
            p2 = ease(t, 5.15, 8.8)
            d.rounded_rectangle((780, 420, 850, 820), radius=16, fill=CYAN, outline=WHITE, width=4)
            d.rounded_rectangle((1050, 340 + int(60 * (1 - p2)), 1120, 820), radius=16, fill=(70, 130, 235, 255), outline=WHITE, width=4)
        draw_label_or_credit(
            im, t,
            [
                (0.60, 4.35, (920, 95), "−224.2 °C RECORD COLD", 60, GOLD),
                (5.25, 8.95, (590, 95), "COLDER THAN NEPTUNE", 62, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R14 (10.39 s, sub-cut at 5.20 s): True 4:1 Uranus (560 px) vs 4 Earths (4 x 140 px = 560 px)
    def r14(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [5.20])
        d = ImageDraw.Draw(im)
        if t < 5.20:
            im.alpha_composite(g_u_560, (680, 250))
            span = ease(t, 0.25, 4.6)
            x0, x1, y = 680, int(round(680 + 560 * span)), 530
            d.line((x0, y, x1, y), fill=GOLD, width=8)
            d.line((x0, y - 32, x0, y + 32), fill=GOLD, width=6)
            d.line((x1, y - 32, x1, y + 32), fill=GOLD, width=6)
        else:
            im.alpha_composite(g_u_560, (680, 170))
            p2 = ease(t, 5.30, 8.8)
            n_show = min(4, max(1, int(math.ceil(4 * p2))))
            for i in range(n_show):
                im.alpha_composite(g_e_140, (680 + i * 140, 770))
            d.line((680, 750, 680 + int(560 * p2), 750), fill=CYAN, width=6)
        draw_label_or_credit(
            im, t,
            [
                (0.60, 4.35, (690, 90), "51,118 KM WIDE", 66, GOLD),
                (5.40, 9.15, (660, 935), "FOUR EARTHS WIDE", 60, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R17 (8.89 s, sub-cut at 4.45 s): 2.9 billion km (19.2 AU) distance & 84-year orbit
    def r17(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_jwst, t, dur, [4.45])
        d = ImageDraw.Draw(im)
        if t < 4.45:
            p1 = ease(t, 0.2, 4.0)
            d.ellipse((150, 490, 250, 590), fill=GOLD)  # Sun
            x_end = int(round(260 + 1320 * p1))
            d.line((260, 540, x_end, 540), fill=GOLD, width=10)
            im.alpha_composite(g_u_360, (max(260, x_end - 180), 360))
        else:
            cx, cy, rx, ry = 960, 560, 620, 320
            d.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=GOLD)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(140, 195, 240, 200), width=6)
            p2 = (t - 4.45) / max(dur - 4.45, 0.1)
            ang = -math.pi / 2 + p2 * math.tau
            ux = int(round(cx + rx * math.cos(ang)))
            uy = int(round(cy + ry * math.sin(ang)))
            d.ellipse((ux - 22, uy - 22, ux + 22, uy + 22), fill=CYAN, outline=WHITE, width=4)
        draw_label_or_credit(
            im, t,
            [
                (0.50, 4.10, (620, 110), "2.9 BILLION KM", 66, GOLD),
                (4.65, 8.30, (640, 110), "84 EARTH YEARS", 64, WHITE),
            ],
            "NASA / ESA / CSA / STScI",
        )
        return im

    # R20 (13.39 s, sub-cuts at 4.47 s, 8.93 s): 1977 KAO stellar occultation trace
    def r20(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.47, 8.93])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_360, (780, 160))
        # Draw occultation photometer box in lower half (bounded width 220..1700 -> no seam)
        d.rounded_rectangle((200, 580, 1720, 920), radius=20, fill=(10, 20, 38, 195), outline=(110, 165, 220, 190), width=4)
        dip_x = [380, 440, 500, 560, 630, 1290, 1360, 1420, 1480, 1540]
        prog = t / dur
        x_max = int(round(230 + 1460 * prog))
        pts = []
        for x in range(230, x_max, 6):
            y = 660
            for dx in dip_x:
                dist = abs(x - dx)
                if dist < 18:
                    y += int(round(180 * math.cos((dist / 18.0) * (math.pi / 2)) ** 2))
            pts.append((x, y))
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=6)
            d.ellipse((pts[-1][0] - 10, pts[-1][1] - 10, pts[-1][0] + 10, pts[-1][1] + 10), fill=WHITE)
        draw_label_or_credit(
            im, t,
            [
                (0.55, 4.15, (180, 90), "MARCH 10, 1977", 62, WHITE),
                (4.70, 8.35, (180, 90), "FIVE SHARP DIPS", 62, GOLD),
                (9.15, 12.80, (180, 90), "NINE NARROW RINGS", 62, CYAN),
            ],
            "NASA / JPL",
        )
        return im

    # R22 (6.51 s, sub-cut at 3.26 s): Inner rings charcoal albedo (2% reflected light)
    def r22(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_jwst, t, dur, [3.26])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_460, (240, 290))
        for r_ring in range(260, 360, 12):
            d.arc((470 - r_ring, 520 - r_ring, 470 + r_ring, 520 + r_ring), -80, 80, fill=(140, 155, 175, 210), width=3)
        if t < 3.26:
            p1 = ease(t, 0.2, 2.9)
            d.rounded_rectangle((1080, 340, 1680, 500), radius=18, fill=(28, 34, 44, 240), outline=GOLD, width=5)
            d.rectangle((1110, 380, 1110 + int(500 * p1), 460), fill=(55, 62, 74, 255))
        else:
            p2 = ease(t, 3.35, 6.0)
            # Saturn bright ice bar vs Uranus 2% charcoal bar
            d.rounded_rectangle((1080, 320, 1080 + int(560 * p2), 420), radius=14, fill=(225, 235, 248, 245))
            d.rounded_rectangle((1080, 520, 1120, 620), radius=10, fill=GOLD)
        draw_label_or_credit(
            im, t,
            [
                (0.35, 3.05, (1060, 140), "DARK AS CHARCOAL", 62, GOLD),
                (3.45, 6.20, (1060, 140), "2% REFLECTED LIGHT", 62, WHITE),
            ],
            "NASA / ESA / CSA / STScI",
        )
        return im

    # R24 (5.46 s): Outer red (Nu) and blue (Mu) rings
    def r24(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_hubble, t, dur, [])
        d = ImageDraw.Draw(im)
        cx, cy = 960, 540
        im.alpha_composite(g_u_360, (cx - 180, cy - 180))
        p = ease(t, 0.2, 4.6)
        sweep = int(round(360 * p))
        if sweep > 5:
            d.arc((cx - 310, cy - 310, cx + 310, cy + 310), -90, -90 + sweep, fill=CORAL, width=14)
            d.arc((cx - 430, cy - 430, cx + 430, cy + 430), -90, -90 + sweep, fill=CYAN, width=16)
        draw_label_or_credit(
            im, t,
            [(0.65, 4.40, (590, 85), "RED AND BLUE RINGS", 64, GOLD)],
            "NASA / ESA / STScI",
        )
        return im

    # R26 (8.30 s, sub-cut at 4.15 s): 97.77 deg axial tilt + retrograde spin
    def r26(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.15])
        d = ImageDraw.Draw(im)
        cx, cy = 960, 540
        im.alpha_composite(g_u_560, (cx - 280, cy - 280))
        tilt = 97.77 * ease(t, 0.25, 3.7)
        ang = math.radians(tilt - 90)
        dx, dy = math.cos(ang) * 360, math.sin(ang) * 360
        d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=GOLD, width=8)
        if t >= 4.15:
            p2 = ease(t, 4.25, 7.8)
            d.arc((cx - 340, cy - 220, cx + 340, cy + 220), 20, 20 + int(290 * p2), fill=CYAN, width=12)
        draw_label_or_credit(
            im, t,
            [
                (0.45, 3.90, (120, 95), "97.77° AXIAL TILT", 64, GOLD),
                (4.35, 7.90, (120, 95), "RETROGRADE SPIN", 64, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R29 (12.44 s, sub-cuts at 4.15 s, 8.29 s): Option B £0 seasonal dial
    def r29(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.15, 8.29])
        im.alpha_composite(g_u_560, (140, 250))
        d = ImageDraw.Draw(im)
        cx, cy, rad = 1360, 540, 270
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=GOLD, width=8)
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=GOLD)
        if t >= 4.15:
            sweep = 90 * ease(t, 4.20, 7.90)
            if sweep > 1:
                d.pieslice((cx - rad + 14, cy - rad + 14, cx + rad - 14, cy + rad - 14), -90, -90 + sweep, fill=(110, 210, 245, 115))
        if t >= 8.29:
            sweep2 = 90 * ease(t, 8.35, 11.9)
            if sweep2 > 1:
                d.pieslice((cx - rad + 14, cy - rad + 14, cx + rad - 14, cy + rad - 14), 90, 90 + sweep2, fill=(255, 205, 70, 125))
        ang = -math.pi / 2 + (t / dur) * math.tau
        px, py = cx + math.cos(ang) * rad, cy + math.sin(ang) * rad
        d.ellipse((px - 16, py - 16, px + 16, py + 16), fill=WHITE, outline=GOLD, width=4)
        draw_label_or_credit(
            im, t,
            [
                (0.45, 3.90, (1120, 95), "84-YEAR ORBIT", 62, GOLD),
                (4.35, 7.95, (1100, 95), "21-YEAR WINTER", 62, CYAN),
                (8.50, 12.00, (1100, 95), "POLE FACES SUN", 62, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R35 (8.16 s, sub-cut at 4.08 s): 2.3% methane & red-light absorption
    def r35(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_hubble, t, dur, [4.08])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_460, (1240, 310))
        if t < 4.08:
            grow = ease(t, 0.25, 3.6)
            parts = [(0.825, (190, 210, 230, 245)), (0.152, (130, 165, 205, 245)), (0.023, CYAN)]
            x = 160
            for frac, col in parts:
                w = int(round(920 * frac * grow))
                if w > 2:
                    d.rounded_rectangle((x, 380, x + w, 520), radius=10, fill=col)
                x += w
        else:
            p2 = ease(t, 4.20, 7.6)
            # Red ray absorbed in atmosphere, cyan ray scattered outward
            d.line((160, 420, int(round(160 + 1080 * p2)), 510), fill=CORAL, width=16)
            d.line((160, 620, 1260, 560), fill=CYAN, width=16)
            if p2 > 0.4:
                d.line((1260, 560, int(round(1260 - 760 * (p2 - 0.4) / 0.6)), int(round(560 + 260 * (p2 - 0.4) / 0.6))), fill=CYAN, width=16)
        draw_label_or_credit(
            im, t,
            [
                (0.45, 3.85, (160, 110), "2.3% METHANE GAS", 64, GOLD),
                (4.25, 7.85, (160, 110), "RED LIGHT ABSORBED", 62, CYAN),
            ],
            "NASA / ESA / STScI",
        )
        return im

    # R38 (10.26 s, sub-cut at 5.13 s): Cold paradox bar (Neptune internal heat vs Uranus stagnant heat)
    def r38(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [5.13])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_n_460, (240, 300))
        im.alpha_composite(g_u_460, (1220, 300))
        if t < 5.13:
            p1 = ease(t, 0.3, 4.5)
            # Outward thermal flux arrows around Neptune (470, 530)
            for a_deg in range(0, 360, 45):
                ar = math.radians(a_deg)
                r0, r1 = 240, int(round(240 + 95 * p1))
                d.line((470 + r0 * math.cos(ar), 530 + r0 * math.sin(ar), 470 + r1 * math.cos(ar), 530 + r1 * math.sin(ar)), fill=CORAL, width=10)
        else:
            p2 = ease(t, 5.25, 9.2)
            # Heat flux comparison bars in center
            d.rounded_rectangle((790, int(round(820 - 420 * p2)), 890, 820), radius=14, fill=CORAL, outline=WHITE, width=4)
            d.rounded_rectangle((1030, 795, 1130, 820), radius=8, fill=CYAN, outline=WHITE, width=4)
        draw_label_or_credit(
            im, t,
            [
                (0.60, 4.40, (180, 95), "NEPTUNE RADIATES HEAT", 58, GOLD),
                (5.35, 9.15, (640, 95), "NEAR-ZERO HEAT FLUX", 60, CYAN),
            ],
            "NASA / JPL",
        )
        return im

    # R43 (6.96 s, sub-cut at 3.48 s): 900 km/h (560 mph) wind gauge
    def r43(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_hubble, t, dur, [3.48])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_560, (180, 260))
        box = (1120, 230, 1740, 850)
        d.arc(box, 195, 345, fill=(160, 190, 225, 180), width=18)
        sweep = 150 * ease(t, 0.25, 6.2)
        d.arc(box, 195, 195 + sweep, fill=GOLD if t < 3.48 else CYAN, width=22)
        spd = int(round(900 * ease(t, 0.25, 3.2)))
        f_num = get_font(86)
        d.text((1310, 500), f"{spd}", font=f_num, fill=WHITE, stroke_width=4, stroke_fill=(8, 14, 28, 230))
        draw_label_or_credit(
            im, t,
            [
                (0.35, 3.25, (1080, 100), "900 KM/H WINDS", 64, GOLD),
                (3.65, 6.60, (1120, 100), "560 MPH JETS", 64, CYAN),
            ],
            "NASA / ESA / STScI",
        )
        return im

    # R46 (14.12 s, sub-cuts at 4.71 s, 9.41 s): 58.6 deg magnetic tilt & 1/3 radius offset
    def r46(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.71, 9.41])
        d = ImageDraw.Draw(im)
        cx, cy = 960, 540
        im.alpha_composite(g_u_560, (cx - 280, cy - 280))
        spin = ease(t, 0.25, 3.8)
        ang = math.radians(-90 + 97.77 * spin)
        d.line((cx - math.cos(ang) * 370, cy - math.sin(ang) * 370, cx + math.cos(ang) * 370, cy + math.sin(ang) * 370), fill=WHITE, width=8)
        if t >= 4.71:
            mag = math.radians(-90 + 97.77 + 58.6 * ease(t, 4.80, 8.6))
            d.line((cx - math.cos(mag) * 350, cy - math.sin(mag) * 350, cx + math.cos(mag) * 350, cy + math.sin(mag) * 350), fill=GOLD, width=10)
        if t >= 9.41:
            p3 = ease(t, 9.50, 13.4)
            ox, oy = int(round(cx + 95 * p3)), int(round(cy - 45 * p3))
            d.ellipse((ox - 18, oy - 18, ox + 18, oy + 18), fill=CORAL, outline=WHITE, width=4)
            for loop_r in (220, 310):
                d.arc((ox - loop_r, oy - loop_r, ox + loop_r, oy + loop_r), -60, 120, fill=CYAN, width=5)
                d.arc((ox - loop_r, oy - loop_r, ox + loop_r, oy + loop_r), 120, 300, fill=CYAN, width=5)
        draw_label_or_credit(
            im, t,
            [
                (0.50, 4.20, (120, 95), "97.77° SPIN AXIS", 62, WHITE),
                (4.90, 8.70, (120, 95), "58.6° MAGNETIC TILT", 62, GOLD),
                (9.60, 13.40, (120, 95), "OFFSET 1/3 RADIUS", 62, CYAN),
            ],
            "NASA / JPL",
        )
        return im

    # R52 (13.90 s, sub-cuts at 4.63 s, 9.27 s): Interior cutaway (outer gas, >=80% hot icy fluid, small rocky core)
    def r52(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [4.63, 9.27])
        d = ImageDraw.Draw(im)
        cx, cy = 960, 540
        im.alpha_composite(g_u_620, (cx - 310, cy - 310))
        d.pieslice((cx - 295, cy - 295, cx + 295, cy + 295), -45, 45, fill=(38, 76, 122, 235), outline=WHITE, width=4)
        if t >= 4.63:
            d.pieslice((cx - 235, cy - 235, cx + 235, cy + 235), -42, 42, fill=(35, 145, 175, 245), outline=CYAN, width=4)
        if t >= 9.27:
            d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=CORAL, outline=GOLD, width=5)
        draw_label_or_credit(
            im, t,
            [
                (0.50, 4.20, (120, 95), "OUTER GAS SHELL", 62, WHITE),
                (4.85, 8.60, (120, 95), "80% HOT ICY FLUID", 62, CYAN),
                (9.50, 13.20, (120, 95), "SMALL ROCKY CORE", 62, GOLD),
            ],
            "NASA / JPL",
        )
        return im

    # R54 (5.77 s): Cloud-top (-224.2 C) vs core (~5,000 C) temperature comparison
    def r54(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_uranus, t, dur, [])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_460, (180, 310))
        grow = ease(t, 0.25, 4.4)
        d.rounded_rectangle((880, int(round(820 - 180 * grow)), 1020, 820), radius=16, fill=CYAN, outline=WHITE, width=4)
        d.rounded_rectangle((1260, int(round(820 - 560 * grow)), 1400, 820), radius=16, fill=CORAL, outline=GOLD, width=4)
        draw_label_or_credit(
            im, t,
            [(0.65, 4.45, (840, 95), "CORE NEAR 5,000 °C", 64, GOLD)],
            "NASA / JPL",
        )
        return im

    # R59 (11.30 s, sub-cut at 5.65 s): True 1:7 Miranda (90 px, 472 km) vs Moon (630 px, 3,475 km)
    def r59(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_miranda, t, dur, [5.65])
        d = ImageDraw.Draw(im)
        # Miranda (90 px diameter) on left with caliper
        im.alpha_composite(g_mir_90, (360, 495))
        d.line((360, 620, 450, 620), fill=GOLD, width=5)
        if t >= 5.65:
            # Moon (630 px diameter = exact 7.0x Miranda) on right
            im.alpha_composite(g_moon_630, (980, 225))
            d.line((980, 885, 1610, 885), fill=CYAN, width=6)
        draw_label_or_credit(
            im, t,
            [
                (0.60, 4.40, (220, 110), "MIRANDA: 472 KM", 64, GOLD),
                (5.85, 9.60, (220, 110), "1/7 MOON'S DIAMETER", 64, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R61 (8.37 s, sub-cut at 4.19 s): Verona Rupes 20 km cliff vs Grand Canyon (12x deeper)
    def r61(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_verona, t, dur, [4.19])
        d = ImageDraw.Draw(im)
        p1 = ease(t, 0.25, 3.8)
        d.rounded_rectangle((1320, int(round(860 - 600 * p1)), 1440, 860), radius=14, fill=GOLD, outline=WHITE, width=4)
        if t >= 4.19:
            # Grand Canyon 1.6 km bar (1/12th height = 50 px) beside Verona Rupes 20 km (600 px)
            d.rounded_rectangle((1080, 810, 1200, 860), radius=10, fill=CORAL, outline=WHITE, width=4)
        draw_label_or_credit(
            im, t,
            [
                (0.45, 3.90, (140, 95), "20 KM DEEP CLIFF", 64, GOLD),
                (4.40, 8.00, (140, 95), "12× GRAND CANYON", 64, WHITE),
            ],
            "NASA / JPL",
        )
        return im

    # R64 (8.34 s, sub-cut at 4.17 s): Dual viewpoint 2024 (Voyager 2 1986 vs JWST infrared)
    def r64(t: float, dur: float) -> Image.Image:
        im = moving_bg(bg_jwst, t, dur, [4.17])
        d = ImageDraw.Draw(im)
        im.alpha_composite(g_u_460, (220, 310))
        d.ellipse((210, 300, 690, 780), outline=GOLD, width=5)
        if t >= 4.17:
            im.alpha_composite(g_jwst_420, (1240, 330))
            d.ellipse((1230, 320, 1670, 760), outline=CYAN, width=5)
            p2 = ease(t, 4.25, 7.8)
            d.line((710, 540, int(round(710 + 500 * p2)), 540), fill=WHITE, width=6)
        draw_label_or_credit(
            im, t,
            [
                (0.45, 3.90, (180, 95), "VOYAGER 2: 1986", 62, GOLD),
                (4.35, 7.95, (1120, 95), "WEBB INFRARED VIEW", 62, CYAN),
            ],
            "NASA / ESA / CSA / STScI",
        )
        return im

    jobs = [
        ("code_graphic_033_r03_winter_counter.mp4", 5.19, r03, "R03", "21-year winter shadow sweep and counter"),
        ("code_graphic_033_r05_tilt_gauge.mp4", 7.06, r05, "R05", "Earth PIA18033 23.44 deg vs Uranus PIA18182 97.77 deg"),
        ("code_graphic_033_r08_hook_temp_drop.mp4", 10.04, r08, "R08", "-224.2 C gauge and real Uranus PIA18182 + Neptune PIA01492"),
        ("code_graphic_033_r14_diameter_scale.mp4", 10.39, r14, "R14", "True 4:1 diameter scale: 560px Uranus vs four 140px Earths"),
        ("code_graphic_033_r17_distance_orbit_bar.mp4", 8.89, r17, "R17", "2.9 billion km distance and 84-year orbital ring"),
        ("code_graphic_033_r20_occultation_trace.mp4", 13.39, r20, "R20", "1977 KAO stellar occultation 5-dip pre/post trace"),
        ("code_graphic_033_r22_inner_rings.mp4", 6.51, r22, "R22", "Charcoal-dark inner rings 2% albedo comparison"),
        ("code_graphic_033_r24_outer_ring_colors.mp4", 5.46, r24, "R24", "Outer red (Nu) and blue (Mu) rings"),
        ("code_graphic_033_r26_retrograde_tilt.mp4", 8.30, r26, "R26", "97.77 deg axial tilt and retrograde spin on real Uranus"),
        ("code_graphic_033_r29_seasonal_dial.mp4", 12.44, r29, "R29", "Option B £0 84-year orbit and 21-year winter dial"),
        ("code_graphic_033_r35_methane_spectrum.mp4", 8.16, r35, "R35", "2.3% methane fraction and red-light absorption"),
        ("code_graphic_033_r38_cold_paradox_bar.mp4", 10.26, r38, "R38", "Neptune PIA01492 vs Uranus PIA18182 internal heat flux"),
        ("code_graphic_033_r43_wind_gauge.mp4", 6.96, r43, "R43", "900 km/h (560 mph) zonal wind arc"),
        ("code_graphic_033_r46_corkscrew_magnet.mp4", 14.12, r46, "R46", "58.6 deg magnetic tilt and 1/3 radius offset"),
        ("code_graphic_033_r52_interior_mantle.mp4", 13.90, r52, "R52", "Interior cutaway: outer gas, 80% hot icy fluid, rocky core"),
        ("code_graphic_033_r54_core_vs_cloud_temp.mp4", 5.77, r54, "R54", "Cloud -224.2 C vs core ~5,000 C bar comparison"),
        ("code_graphic_033_r59_miranda_size_scale.mp4", 11.30, r59, "R59", "True 1:7 scale: Miranda PIA01490 (90px) vs Moon PIA00405 (630px)"),
        ("code_graphic_033_r61_canyon_depth_scale.mp4", 8.37, r61, "R61", "Verona Rupes 20 km cliff vs 1.6 km Grand Canyon (12x)"),
        ("code_graphic_033_r64_dual_viewpoint_2024.mp4", 8.34, r64, "R64", "Voyager 2 1986 vs JWST NIRCam dual perspective"),
    ]

    clips = []
    for name, seconds, fn, row, note in jobs:
        print(f"Rendering {name} ({seconds:.2f}s @ {FPS}fps)...", flush=True)
        rec = render_clip(name, seconds, fn)
        rec.update(row=row, note=note)
        clips.append(rec)
        print(
            f"  -> {rec['sha256'][:12]} | luma={rec['mid_frame_mean_luma']} std={rec['mid_frame_std_luma']} "
            f"diff={rec['mean_frame_diff']} frozen={rec['frozen_pairs']}",
            flush=True,
        )

    # Byte-identical R26 alias required by STILLS_LOCK reconciliation
    src_r26 = OUT_NAS / "code_graphic_033_r26_retrograde_tilt.mp4"
    alias_r26 = OUT_NAS / "code_graphic_033_r26_axial_tilt_97deg.mp4"
    shutil.copy2(src_r26, alias_r26)
    r26_rec = next(c for c in clips if c["row"] == "R26")
    clips.append({
        **r26_rec,
        "file": alias_r26.name,
        "path": str(alias_r26),
        "row": "R26_ALIAS",
        "note": "Byte-identical alias of code_graphic_033_r26_retrograde_tilt.mp4",
    })

    # Write SHA256SUMS.txt in OUT_NAS
    sums = [f"{c['sha256']}  {c['file']}" for c in sorted(clips, key=lambda x: x["file"])]
    (OUT_NAS / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n")

    manifest = {
        "job": "J2299",
        "version": "v02",
        "spend_gbp": 0,
        "orbit_character": False,
        "fps": FPS,
        "resolution": f"{W}x{H}",
        "r01_opener": "Accepted 24fps sideways Uranus composite r01_sourced_composite_v01_silent.mp4 (SHA-256 aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d) under J2386",
        "r29": "Option B £0 seasonal dial at 24fps with 3 stage cuts (0.00, 4.15, 8.29s). Neighbours R28 and R30 are NASA plates.",
        "r55": "code_graphic_033_r55_pressure_gauge.mp4 is RETIRED under J2334/J2386; R55 (493.01-505.35s) uses accepted 3-cut cloud passage r55_passage_v01_silent.mp4 (SHA-256 4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f) for R54 CODE -> R55 moving-world separation.",
        "r26_alias": "code_graphic_033_r26_axial_tilt_97deg.mp4 is byte-identical to code_graphic_033_r26_retrograde_tilt.mp4.",
        "r46_vs_r52": "R46 is code_graphic_033_r46_corkscrew_magnet.mp4 (58.6 deg magnetic tilt & 1/3 radius offset); R52 is code_graphic_033_r52_interior_mantle.mp4 (outer gas, 80% hot icy fluid, rocky core).",
        "true_globe_scaling": {
            "R14_uranus_to_earth": "560 px vs 140 px = 4.00:1 (51,118 km vs 12,742 km = 4.01:1)",
            "R59_miranda_to_moon": "90 px vs 630 px = 1:7.00 (471.6 km vs 3,474.8 km = 1:7.37, matching spoken 'one-seventh')",
        },
        "sources": {
            "uranus": str(p_uranus),
            "earth": str(p_earth),
            "neptune": str(p_neptune),
            "miranda": str(p_miranda),
            "moon": str(p_moon),
            "hubble_uranus": str(p_hubble),
            "jwst_uranus": str(p_jwst),
            "verona_rupes": str(p_verona),
        },
        "clips": clips,
    }
    (OUT_NAS / "CODE_GRAPHICS_J2299_v02.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (HERE / "CODE_GRAPHICS_J2299_v02.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"ALL DONE: {len(clips)} files written to {OUT_NAS}", flush=True)


if __name__ == "__main__":
    main()
