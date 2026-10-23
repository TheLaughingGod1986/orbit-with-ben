#!/usr/bin/env python3
"""028 A Star Is Coming Toward Us (Gliese 710) — Build 3 Weekday Shorts from SHORTS_PLAN_v01 (J0895).

Follows 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/10_Shorts/SHORTS_PLAN_v01.md (Claude, J0893):
  1. Mon 30 Nov (2026-11-30): "Why Will Gliese 710's Comets Arrive After It Has Gone?"
     - Hook caption (frame 0): 10 COMETS / A YEAR (yellow A YEAR)
     - Lift (master s): 281.74–293.52 (s53) + 297.10–315.46 (s55–58), skipping s54 meta line
     - Picture: r26_hale_bopp (2 crops), r26_a3 (2 crops), r27_shower (3 stretches), r27_leaving (3 stretches)
  2. Wed 2 Dec (2026-12-02, Test A opening): "Is a Star Really Coming Towards Us?"
     - Hook caption (frame 0): A STAR IS / COMING (yellow COMING)
     - Lift (master s): 0.00–30.14 (s0–6, the long's opening)
     - Picture: r01 (4 non-overlapping stretches/crops cut on word pauses at 2.68, 6.00, 9.00, 13.66 s),
       r03_serpens_sky (13.66–17.61 s), r04 (4 stretches + end card on Gaia starfield)
  3. Fri 4 Dec (2026-12-04): "How Close Will Gliese 710 Come to the Sun?"
     - Hook caption (frame 0): A FIFTH OF A / LIGHT-YEAR (yellow LIGHT-YEAR)
     - Lift (master s): 162.06–166.36 (s30) + 178.36–198.52 (s33–36)
     - Picture: r15_16_path (0–4.48 s), r17_scale_a (4.48–8.11 s), r17_neptune (8.11–12.81 s),
       r17_scale_b (12.81–17.41 s), r17_pitch (17.41–21.55 s), r18_shell (21.55–24.82 s), end card (24.82–26.82 s)

All three:
  - £0 spend (long's locked VO and score bed + house SFX kit).
  - 9:16 (1080x1920 @ 30 fps CFR), cuts on sentence/clause pauses only, picture changes every 2.2–4.7 s (< 6.0 s max).
  - No Orbit at frame 0 (and no Orbit on covers).
  - 9.0–14.0 s title banner inside the 16:9 centre band (y=656..1264).
  - Last 2.0 s end card naming the long's exact listing title ("What Happens When a Star Passes Through Our Solar System?")
    and YouTube ID ("F-jImX5h7ws") inside the 16:9 centre band, after the last word + 0.30 s VO audio tail.
  - Gates per Short: gate_shorts_open.py, sfx_kit.py level, polish_gate.py, picture_qa.py, thumb_preview.py --score,
    and caption + title-safe bounding-box audit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
REPO = FILM.parents[1]
EDIT = FILM / "07_Edit-Project"
HDIR = EDIT / "nasa_pool_v01" / "028_harvest_v01"
CDIR = EDIT / "code_graphics_v02"
VDIR = FILM / "04_Generated-Clips" / "01_Raw" / "veo_v01"
THUMB_ART_DIR = FILM / "08_Thumbnail" / "art_v01"
VO_WAV = FILM / "02_Voiceover" / "star_coming_vo_v01.wav"
BED_MP3 = FILM / "05_Music" / "gliese_score_bed_v03.mp3"
KIT_DIR = FILM / "06_Sound-Effects" / "kit_v01"
WORDS_JSON = EDIT / "full_master_v03_pack" / "gliese_words_list.json"
REV_OK_LONG = EDIT / "full_master_v03_pack" / "reviewed_ok_v03.json"

PACK = HERE / "shorts_v01_pack"
WORK = Path("/private/tmp/gliese028_shorts_work_v01")
UAT_ROOT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
NAS_STAGE = Path("/Volumes/data/mac-mini-archive/youtube-staging/028/shorts_v01")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
BAND_H = round(W * 9 / 16)          # 608 px
BAND_Y0 = (H - BAND_H) // 2         # 656 px
BAND_Y1 = BAND_Y0 + BAND_H          # 1264 px
LINE_H = round(BAND_H * 0.115)      # 70 px

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)         # hue 52.7 deg > 42 deg so gate_shorts_open never mistakes yellow text for orange Orbit
GOLD = (255, 214, 64)
ICE = (169, 216, 255)
ORANGE = (255, 154, 60)

LONG_ID = "F-jImX5h7ws"
LONG_TITLE = "What Happens When a Star Passes Through Our Solar System?"
TITLE_ROWS = [
    "What Happens When",
    "a Star Passes Through",
    "Our Solar System?",
]
END_ROWS = [
    ("What Happens When", WHITE),
    ("a Star Passes Through", WHITE),
    ("Our Solar System?", WHITE),
    (LONG_ID, YELLOW),
]
HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
END_CARD_LEN = 2.00
VO_TAIL_S = 0.30

ALL_WORDS = json.loads(WORDS_JSON.read_text())


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    return (1.0 - math.cos(math.pi * max(0.0, min(1.0, x)))) / 2.0


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, w.getnchannels())


def write_wav_dithered(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    zmask = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if zmask.any():
        idx = np.arange(zmask.sum())
        pcm[zmask, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[zmask, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def font_for(line_h: float, ratio: float = 0.86, font_path: str = FONT_BLACK) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(font_path, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(font_path, size)
        size += 1


def centred(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    stroke: int = 6,
) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    stroke_fill = (10, 18, 32, alpha)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


# =============================================================================
# 9:16 Native Code Graphics Renderer (adapted from build_code_graphics_v02.py)
# =============================================================================
class VerticalCodeRenderer:
    """Renders 028's teaching diagrams natively at 1080x1920 (9:16) with all bodies and labels inside the 16:9 band."""

    def __init__(self, assets_dir: Path):
        self.sun = Image.open(assets_dir / "sun_sdo.jpg").convert("RGB").crop((140, 15, 1560, 1435))
        self.earth = Image.open(assets_dir / "earth.jpg").convert("RGB")
        self.rng = np.random.default_rng(710)
        self.stars = self.rng.uniform([50, 90], [1030, 1830], (130, 2))
        v = self.rng.normal(size=(420, 3))
        v /= np.linalg.norm(v, axis=1)[:, None]
        self.cloud = v * self.rng.uniform(0.72, 1.0, (420, 1))

        # Full-frame 1080x1920 lifted navy + Milky Way background (mean luma ~38, B >= 50 so visor_frac == 0.0000)
        y, x = np.mgrid[:H, :W]
        rad = np.sqrt(((x - 540.0) / 480.0) ** 2 + ((y - 960.0) / 680.0) ** 2)
        g1 = np.exp(-rad ** 2 * 1.2)
        band_d = ((x - 540.0) * 0.65 + (y - 960.0) * 0.76) / 300.0
        band_l = ((x - 540.0) * 0.76 - (y - 960.0) * 0.65) / 760.0
        mw = np.exp(-band_d ** 2) * np.exp(-band_l ** 2 * 0.6)
        dust = np.exp(-((band_d - 0.16) / 0.32) ** 2) * np.exp(-band_l ** 2 * 1.0)
        g2 = np.exp(-(((x - 310.0) / 320.0) ** 2 + ((y - 620.0) / 420.0) ** 2))
        g3 = np.exp(-(((x - 780.0) / 340.0) ** 2 + ((y - 1280.0) / 440.0) ** 2))
        glow = np.clip(0.65 * g1 + 0.45 * mw - 0.18 * dust + 0.34 * g2 + 0.30 * g3, 0.0, 1.35)
        base = np.stack([20.0 + 58.0 * glow, 30.0 + 78.0 * glow, 50.0 + 105.0 * glow], axis=-1)
        bg = Image.fromarray(np.uint8(np.clip(base, 0, 255)))

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for cr in (160, 260, 360, 460, 560, 680, 820):
            ld.ellipse((540 - cr, 960 - int(cr * 0.72), 540 + cr, 960 + int(cr * 0.72)), outline=(165, 195, 230, 82), width=2)
            for deg in range(0, 360, 4):
                ang = math.radians(deg)
                r1 = cr - (9 if deg % 12 == 0 else 5)
                r2 = cr + (9 if deg % 12 == 0 else 5)
                ld.line(
                    (
                        540 + r1 * math.cos(ang),
                        960 + r1 * 0.72 * math.sin(ang),
                        540 + r2 * math.cos(ang),
                        960 + r2 * 0.72 * math.sin(ang),
                    ),
                    fill=(185, 212, 242, 108),
                    width=2,
                )
        srng = np.random.default_rng(7100)
        for n_stars, r_px, alpha in [(520, 2.2, 135), (220, 3.2, 165), (65, 4.5, 185)]:
            for sx, sy in srng.uniform([35, 60], [1045, 1860], (n_stars, 2)):
                ld.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=(215, 232, 252, alpha))
        self.background = Image.alpha_composite(bg.convert("RGBA"), layer).convert("RGB")
        self.bodies: dict = {}

    def body(self, im: Image.Image, xy: tuple[float, float], r: float, kind: str = "sun", tint: bool = False) -> None:
        r_i = max(4, int(round(r)))
        key = (r_i, kind, tint)
        if key not in self.bodies:
            src = self.earth if kind == "earth" else self.sun
            b_im = ImageOps.fit(src, (2 * r_i, 2 * r_i), method=Image.Resampling.LANCZOS)
            if kind != "earth":
                grey = ImageOps.grayscale(b_im)
                # Use warm gold/amber for Gliese 710 on open frame or standard orange-gold
                hi_col = (255, 192, 68) if tint else (255, 237, 168)
                lo_col = (90, 42, 18) if tint else (99, 61, 17)
                b_im = ImageOps.colorize(grey, lo_col, hi_col)
            mask = Image.new("L", (2 * r_i, 2 * r_i))
            ImageDraw.Draw(mask).ellipse((1, 1, 2 * r_i - 2, 2 * r_i - 2), fill=255)
            b_im.putalpha(mask)
            self.bodies[key] = b_im
        im.paste(self.bodies[key], (int(round(xy[0] - r_i)), int(round(xy[1] - r_i))), self.bodies[key])

    def base(self, t: float, speed_px: float = 18.0) -> Image.Image:
        im = self.background.copy()
        d = ImageDraw.Draw(im)
        shift_x = int(t * speed_px) % 90
        shift_y = int(t * (speed_px * 0.6)) % 90
        for x in range(-90, W + 90, 90):
            d.line((x + shift_x, 120, x + shift_x, H - 120), fill=(46, 66, 92), width=1)
        for y in range(120, H - 119, 90):
            d.line((48, y + shift_y, W - 48, y + shift_y), fill=(46, 66, 92), width=1)
        for k, (x, y) in enumerate(self.stars):
            xx = 48 + (x - 48 + t * (12 + (k % 5) * 6)) % (W - 96)
            yy = 80 + (y - 80 + t * (6 + (k % 3) * 4)) % (H - 160)
            d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(165, 192, 224))
        return im

    def cloud_draw(self, im: Image.Image, t: float, scale: float = 1.0, cx: float = 540.0, cy: float = 980.0) -> None:
        a = t * 0.08
        v = self.cloud.copy()
        x = v[:, 0] * math.cos(a) - v[:, 2] * math.sin(a)
        z = v[:, 0] * math.sin(a) + v[:, 2] * math.cos(a)
        d = ImageDraw.Draw(im)
        for xx, yy, zz in zip(x, v[:, 1], z):
            px = cx + xx * 370.0 * scale
            py = cy + yy * 215.0 * scale
            rr = 1.8 + (zz + 1.0) * 1.4
            if 55 < px < W - 55 and BAND_Y0 - 120 < py < BAND_Y1 + 120:
                c = tuple(int(n * (0.48 + 0.25 * (zz + 1.0))) for n in ICE)
                d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=c)
        self.body(im, (cx, cy), max(16, 30 * scale))

    def draw_band_label(
        self,
        im: Image.Image,
        text: str,
        xy: tuple[float, float],
        size: int = 44,
        color: tuple = WHITE[:3],
        alpha: float = 1.0,
    ) -> list[int]:
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        f = ImageFont.truetype(FONT_BOLD, size)
        box = d.textbbox(xy, text, font=f, anchor="mm", stroke_width=3)
        d.text(
            xy,
            text,
            font=f,
            fill=(*color[:3], int(255 * alpha)),
            anchor="mm",
            stroke_width=3,
            stroke_fill=(12, 23, 39, int(225 * alpha)),
        )
        im.paste(layer, (0, 0), layer)
        return list(box)

    def render_clip(
        self,
        mode: str,
        dur_s: float,
        dest: Path,
        t_offset: float = 0.0,
        zoom_range: tuple[float, float] = (1.0, 1.06),
        pan_xy: tuple[float, float] = (0.0, 0.0),
        band_label: tuple[float, float, str] | None = None,
        open_push: float = 0.0,
    ) -> dict:
        frames = round(dur_s * FPS)
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-video_track_timescale",
            "30000",
            str(dest),
        ]
        proc = sp.Popen(cmd, stdin=sp.PIPE)
        label_bboxes = []
        for i in range(frames):
            lt = i / FPS
            t = t_offset + lt
            u = lt / max(0.001, dur_s)
            speed = 42.0 if open_push > 0 and lt <= 1.2 else 20.0
            im = self.base(t, speed_px=speed)
            d = ImageDraw.Draw(im)

            if mode == "r15_16_path":
                # Closest-approach path graphic inside 16:9 centre band (y=656..1264)
                sx, sy = 260.0, 1085.0
                self.body(im, (sx, sy), 52)
                f = ease(min(1.0, (lt + 0.15) / max(0.8, dur_s * 0.75)))
                distance = 1.0 - 0.72 * f
                yy = sy - 255.0 * distance
                wide = 58.0 * (1.0 - f) + 12.0 * f
                d.ellipse((sx - 255, sy - 255, sx + 255, sy + 255), outline=(92, 132, 172), width=3)
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ld = ImageDraw.Draw(layer)
                ld.polygon([(110, yy - wide), (970, yy - wide), (970, yy + wide), (110, yy + wide)], fill=(*GOLD, 46))
                im.paste(layer, (0, 0), layer)
                d = ImageDraw.Draw(im)
                d.line((110, yy, 970, yy), fill=GOLD, width=5)
                gx = 900.0 - 520.0 * ease(u)
                self.body(im, (gx, yy), 34, tint=True)
                d.line((sx + 68, sy, sx + 68, yy), fill=ICE, width=4)
                for y_tick in (sy, yy):
                    d.line((sx + 56, y_tick, sx + 80, y_tick), fill=ICE, width=4)
                self.draw_band_label(im, "Sun", (sx, sy + 76), size=40, color=WHITE[:3])
                self.draw_band_label(im, "Gliese 710", (min(max(gx, 240.0), 840.0), yy - 58), size=38, color=GOLD)

            elif mode == "r17_scale_a":
                # Sun–Earth = 1 cm scale inside 16:9 centre band
                sx, ex, cy = 220.0, 860.0, 930.0
                self.body(im, (sx, cy), 72)
                self.body(im, (ex, cy), 52, kind="earth")
                end = sx + (ex - sx) * ease(min(1.0, u * 1.5))
                d.line((sx, cy + 145, end, cy + 145), fill=GOLD, width=6)
                for xx in (sx, end):
                    d.line((xx, cy + 125, xx, cy + 165), fill=GOLD, width=5)
                self.draw_band_label(im, "Sun", (sx, cy - 105), size=42, color=WHITE[:3])
                self.draw_band_label(im, "Earth", (ex, cy - 105), size=42, color=WHITE[:3])

            elif mode == "r17_scale_b":
                # 30 cm ruler extending toward Gliese 710 inside 16:9 centre band
                sx, cy = 150.0, 965.0
                self.body(im, (sx, cy), 42)
                end = 360.0 + 560.0 * ease(u)
                d.line((sx, cy + 95, end, cy + 95), fill=GOLD, width=6)
                for xx in np.linspace(sx, end, 31):
                    d.line((xx, cy + 95, xx, cy + 115), fill=ICE, width=2)
                self.body(im, (end, cy), 34, tint=True)
                self.draw_band_label(im, "Sun", (sx, cy - 72), size=36, color=WHITE[:3])
                self.draw_band_label(im, "Gliese 710", (min(end, 855.0), cy - 76), size=40, color=GOLD)

            elif mode == "r18_shell":
                # Planetary orbits safe inside 100 m scale
                cx, cy = 540.0, 980.0
                self.body(im, (cx, cy), 44)
                for rr in (105, 180, 265, 360):
                    d.ellipse((cx - rr, cy - rr * 0.54, cx + rr, cy + rr * 0.54), outline=(96, 138, 174), width=3)
                a = t * 0.45
                self.body(im, (cx + 180 * math.cos(a), cy + 180 * 0.54 * math.sin(a)), 24, kind="earth")
                self.draw_band_label(im, "Planets", (cx, cy + 230), size=38, color=ICE)

            elif mode.startswith("r27_shower") or mode.startswith("r04_shower"):
                late = mode.startswith("r27_shower")
                cx = 540.0 + pan_xy[0]
                cy = 985.0 + pan_xy[1]
                sc = zoom_range[0] + (zoom_range[1] - zoom_range[0]) * ease(u)
                self.cloud_draw(im, t, scale=sc, cx=cx, cy=cy)
                d = ImageDraw.Draw(im)
                # Gliese 710 passing across upper Oort shell inside the 16:9 centre band
                y_line = cy - 165.0 * min(1.15, sc)
                d.line((110, y_line, 970, y_line), fill=(138, 112, 76), width=3)
                if late:
                    sx = 620.0 + 270.0 * u
                else:
                    sx = 170.0 + 740.0 * ease(u)
                self.body(im, (sx, y_line), 30, tint=True)
                fall = 0.28 + 0.62 * u if late else ease(max(0.0, (u - 0.15) / 0.85))
                for k in range(9):
                    start = np.array([290.0 + k * 58.0, y_line - 8.0 + 18.0 * math.sin(k)])
                    control = np.array([860.0 - 48.0 * k, cy + 45.0 + 12.0 * k])
                    end_pt = np.array([cx - 35.0 + 9.0 * k, cy + 35.0])
                    ts = np.linspace(0.0, fall, 32)
                    pts = [tuple((1 - v) ** 2 * start + 2 * (1 - v) * v * control + v * v * end_pt) for v in ts]
                    if fall > 0.02 and len(pts) >= 2:
                        d.line(pts, fill=ICE, width=2)
                    px, py = pts[-1]
                    d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=WHITE[:3])
            else:
                raise ValueError(f"Unknown code graphic mode: {mode}")

            # Optional single centre-band label (strictly inside y=656..1264)
            if band_label is not None:
                l_in, l_out, l_txt = band_label
                if l_in <= lt <= l_out:
                    alpha = min(ease((lt - l_in) / 0.35), ease((l_out - lt) / 0.35))
                    bb = self.draw_band_label(
                        im,
                        l_txt,
                        (540, BAND_Y0 + 68 + int(10 * (1.0 - alpha))),
                        size=50,
                        color=GOLD,
                        alpha=alpha,
                    )
                    label_bboxes.append(bb)

            # Apply first-second opening push if requested (for frame-0 motion >= 12)
            if open_push > 0 and lt < 1.1:
                z = 1.0 + open_push * (1.0 - min(1.0, lt / 1.0))
                bw, bh = W / z, H / z
                box = ((W - bw) / 2.0, (H - bh) / 2.0, (W + bw) / 2.0, (H + bh) / 2.0)
                im = im.resize((W, H), Image.Resampling.BICUBIC, box=box)

            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"render_clip failed: {dest}")
        bbox_union = None
        if label_bboxes:
            bbox_union = [
                min(b[0] for b in label_bboxes),
                min(b[1] for b in label_bboxes),
                max(b[2] for b in label_bboxes),
                max(b[3] for b in label_bboxes),
            ]
        return {"mode": mode, "dur_s": dur_s, "label_bbox": bbox_union}


# =============================================================================
# 9:16 Still & Video Plate Renderers
# =============================================================================
def render_still_9x16(
    src: Path,
    dur_s: float,
    dest: Path,
    box: tuple[float, float, float, float],
    pct: float = 0.06,
    gamma: float = 0.85,
    lift: float = 6.0,
    color: float = 1.10,
    contrast: float = 1.10,
    open_push: float = 0.0,
) -> float:
    """Render a smooth subpixel 9:16 push on a high-res still (zero jitter, exact frame count)."""
    frames = round(dur_s * FPS)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    cw = int(round(w * (box[2] - box[0])))
    ch = int(round(h * (box[3] - box[1])))
    x0 = int(round(w * box[0]))
    y0 = int(round(h * box[1]))
    im = im.crop((x0, y0, x0 + cw, y0 + ch))

    if gamma != 1.0 or lift != 0.0:
        arr = np.asarray(im, dtype=np.float32) / 255.0
        arr = np.clip((arr ** gamma) * 255.0 + lift, 0.0, 255.0).astype(np.uint8)
        im = Image.fromarray(arr)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Contrast(im).enhance(contrast)

    # Oversample canvas for smooth subpixel push
    target_w = round(W * (1.0 + pct + open_push + 0.04))
    target_h = round(H * (1.0 + pct + open_push + 0.04))
    scale = max(target_w / im.width, target_h / im.height)
    upscale = round(max(W / cw, H / ch) * (1.0 + pct + open_push), 3)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    cx0 = (im.width - target_w) // 2
    cy0 = (im.height - target_h) // 2
    im = im.crop((cx0, cy0, cx0 + target_w, cy0 + target_h))
    W_c, H_c = im.size

    proc = sp.Popen(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-video_track_timescale",
            "30000",
            str(dest),
        ],
        stdin=sp.PIPE,
    )
    for n in range(frames):
        lt = n / FPS
        # Monotonic linear zoom-in so polish_gate jitter check sees 0 reversals and <0.1 px off-trend
        if open_push > 0 and lt < 1.0:
            # Fast initial push in first second, then steady linear drift
            z = 1.0 + open_push * (lt / 1.0) + pct * (n / max(1, frames - 1))
        else:
            z = 1.0 + open_push + pct * (n / max(1, frames - 1))
        bw, bh = W_c / z, H_c / z
        cbox = ((W_c - bw) / 2.0, (H_c - bh) / 2.0, (W_c + bw) / 2.0, (H_c + bh) / 2.0)
        proc.stdin.write(im.resize((W, H), Image.Resampling.BICUBIC, box=cbox).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"render_still_9x16 failed: {dest}")
    return upscale


def render_video_9x16(
    src: Path,
    offset_s: float,
    dur_s: float,
    dest: Path,
    crop_box: tuple[int, int, int, int] | None = None,
    open_push: float = 0.0,
    feathered_720p: bool = False,
) -> float:
    """Render a video stretch to 1080x1920 @ 30 fps."""
    if feathered_720p:
        # For 1280x720 football_pitch_veo_v01.mp4: scale foreground 1.50x (1920x1080 -> crop 1080x1080) over
        # smoothly feathered blurred vertical background so upscale is 1.50x (<= 2.0x) and zero horizontal seams.
        frames = round(dur_s * FPS)
        raw = sp.check_output(
            [
                "ffmpeg",
                "-v",
                "error",
                "-ss",
                f"{offset_s:.3f}",
                "-t",
                f"{dur_s + 0.2:.3f}",
                "-i",
                str(src),
                "-vf",
                f"fps={FPS}",
                "-frames:v",
                str(frames),
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-",
            ]
        )
        sw, sh = 1280, 720
        frame_bytes = sw * sh * 3
        # Smooth cosine vertical mask over 1160 px height with 240 px feather ramps top and bottom
        fg_h = 1160
        fg_w = round(sw * (fg_h / sh))  # 2062 -> upscale 1160/720 = 1.61x
        ramp = 240
        y_idx = np.arange(fg_h, dtype=np.float32)
        top_w = 0.5 * (1.0 - np.cos(math.pi * np.clip(y_idx / ramp, 0.0, 1.0)))
        bot_w = 0.5 * (1.0 - np.cos(math.pi * np.clip((fg_h - 1 - y_idx) / ramp, 0.0, 1.0)))
        mask_1d = np.minimum(top_w, bot_w)
        mask_im = Image.fromarray((np.broadcast_to(mask_1d[:, None], (fg_h, W)) * 255.0).astype(np.uint8), "L")
        y_paste = (H - fg_h) // 2

        proc = sp.Popen(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                f"{W}x{H}",
                "-r",
                str(FPS),
                "-i",
                "-",
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "16",
                "-pix_fmt",
                "yuv420p",
                "-video_track_timescale",
                "30000",
                str(dest),
            ],
            stdin=sp.PIPE,
        )
        for i in range(frames):
            chunk = raw[i * frame_bytes : (i + 1) * frame_bytes]
            if len(chunk) < frame_bytes:
                chunk = raw[-frame_bytes:]
            im = Image.frombytes("RGB", (sw, sh), chunk)
            bg = ImageOps.fit(im, (W, H), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=42))
            bg = ImageEnhance.Brightness(bg).enhance(0.85)
            fg_src = im.rotate(4.5, resample=Image.Resampling.BICUBIC, expand=False).crop((68, 38, sw - 68, sh - 38))
            fg = fg_src.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
            fx0 = fg_w - W
            fg = fg.crop((fx0, 0, fx0 + W, fg_h))
            bg.paste(fg, (0, y_paste), mask_im)
            proc.stdin.write(bg.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"feathered_720p failed: {dest}")
        return 1.61

    cw, ch, cx, cy = crop_box if crop_box else (608, 1080, 656, 0)
    upscale = round(max(W / cw, H / ch) * (1.0 + open_push), 3)
    if open_push > 0:
        vf = (
            f"fps={FPS},"
            f"crop={cw}:{ch}:'{max(0, cx - 220)}+400*min(t,1.0)':'{max(0, cy - 40)}+80*min(t,1.0)',"
            f"eq=contrast=1.20:brightness=0.03:gamma=0.80:saturation=1.22,"
            f"scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p"
        )
    else:
        vf = f"fps={FPS},crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            f"{offset_s:.3f}",
            "-t",
            f"{dur_s:.3f}",
            "-i",
            str(src),
            "-an",
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "16",
            "-r",
            str(FPS),
            "-video_track_timescale",
            "30000",
            str(dest),
        ]
    )
    return upscale


# =============================================================================
# Overlays: Hook Caption, 9-14s Title Banner, Lower-Third Captions, End Card, Cover
# =============================================================================
def make_hook_png(dest: Path, rows: list[tuple[str, tuple]]) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cap_h = H * 0.082
    f = font_for(cap_h / 0.72, 0.86)
    if f.size > 140:
        f = ImageFont.truetype(FONT_BLACK, 140)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    y = 250
    bboxes = []
    for t, c in rows:
        bboxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in rows), "font_px": f.size, "bboxes": bboxes}


def make_title_banner_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    while max(d.textlength(r, font=f) for r in TITLE_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 14
    y = BAND_Y0 + (BAND_H - gap * len(TITLE_ROWS)) // 2
    placed = []
    for r in TITLE_ROWS:
        bb = centred(d, y, r, f, WHITE, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"title banner outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "joined": LONG_TITLE}


def make_end_card_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.88)
    while max(d.textlength(r, font=f) for r, _ in END_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 12
    y = BAND_Y0 + (BAND_H - gap * len(END_ROWS)) // 2
    placed = []
    for r, col in END_ROWS:
        bb = centred(d, y, r, f, col, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"end card outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "long_title": LONG_TITLE, "youtube_id": LONG_ID}


def map_words_for_slices(slices: list[tuple[float, float]]) -> tuple[list[dict], float]:
    """Map master v03 word timestamps across one or two (master_in, master_out) VO slices."""
    mapped = []
    t_cursor = 0.0
    for s_in, s_out in slices:
        for w in ALL_WORDS:
            if w["end"] <= s_in + 0.01 or w["start"] >= s_out - 0.01:
                continue
            ws = max(0.0, w["start"] - s_in) + t_cursor
            we = min(s_out - s_in, w["end"] - s_in) + t_cursor
            mapped.append({"w": w["text"], "s": round(ws, 3), "e": round(we, 3)})
        t_cursor = round(t_cursor + (s_out - s_in), 3)
    return mapped, t_cursor


def build_caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.40, vo_end)
        text = " ".join(x["w"] for x in c).rstrip(",.")
        if end - start >= 0.18:
            out.append({"text": text, "s": round(start, 2), "e": round(end, 2)})
    return out


def make_caption_png(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    shown = text.upper()
    while d.textlength(shown, font=f) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 + 72, shown, f, WHITE, stroke=6)
    im.save(dest)
    return bb


def make_cover_jpg(dest: Path, bg_src: Path, crop_box: tuple[float, float, float, float], rows: list[tuple[str, tuple]]) -> dict:
    """Build a 1080x1920 Short cover with zero Orbit, saturation >= 120, near-black <= 30%, text inside 16:9 centre band."""
    im = Image.open(bg_src).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * crop_box[0]), int(h * crop_box[1]), int(w * crop_box[2]), int(h * crop_box[3])))
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS)

    # Rich grade so HSV saturation >= 125 and near-black <= 10% (after contrast)
    im = ImageEnhance.Color(im).enhance(1.45)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    arr = np.asarray(im, dtype=np.float32)
    arr = np.clip(((arr / 255.0) ** 0.78) * 255.0 + 14.0, 0.0, 255.0)
    lum = 0.299 * arr[:, :, 0:1] + 0.587 * arr[:, :, 1:2] + 0.114 * arr[:, :, 2:3]
    dark_w = np.clip((38.0 - lum) / 38.0, 0.0, 1.0)
    floor_rgb = np.array([18.0, 36.0, 74.0], dtype=np.float32)[None, None, :]
    arr = np.maximum(arr, dark_w * floor_rgb + (1.0 - dark_w) * arr)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(im)
    size = 64
    while size < 130:
        f_try = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=f_try) for r, _ in rows) > W * 0.78:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    block_h = lh * len(rows)
    y = BAND_Y0 + (BAND_H - block_h) // 2
    bboxes = []
    for r, col in rows:
        bb = centred(d, y, r, f, col, stroke=8)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"cover text outside 16:9 centre band: {r} {bb}")
        bboxes.append(bb)
        y += lh
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in rows], "font_px": size, "bboxes": bboxes}


# =============================================================================
# Audio Builder: Master v03 VO + J0079 Envelope-Ducked Score Bed + House SFX
# =============================================================================
def build_short_audio(
    work: Path,
    slices: list[tuple[float, float]],
    total_s: float,
    sfx_hits: list[tuple[str, float, float]],
) -> dict:
    """Slice master VO and score bed, apply J0079 ducking + house SFX, verify sfx_kit.py level, and mix to -14 LUFS."""
    # 1. Slice VO from VO_WAV and normalize to -14 LUFS
    vo_parts = []
    for i, (s_in, s_out) in enumerate(slices):
        p = work / f"vo_part_{i}.wav"
        seg_dur = s_out - s_in
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{s_in:.3f}",
                "-t",
                f"{seg_dur:.3f}",
                "-i",
                str(VO_WAV),
                "-af",
                f"afade=t=in:d=0.02,afade=t=out:st={ max(0.0, seg_dur - 0.04):.3f}:d=0.04",
                "-ar",
                str(SR),
                "-ac",
                "2",
                str(p),
            ]
        )
        vo_parts.append(read_wav(p))
    vo_cat = np.concatenate(vo_parts, axis=0)
    total_samples = int(round(total_s * SR))
    if len(vo_cat) < total_samples:
        pad = np.zeros((total_samples - len(vo_cat), 2), dtype=np.float32)
        vo_cat = np.concatenate([vo_cat, pad], axis=0)
    else:
        vo_cat = vo_cat[:total_samples]

    vo_raw = work / "stem_vo_raw.wav"
    write_wav_dithered(vo_cat, vo_raw)
    vo_wav = work / "stem_vo.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(vo_raw),
            "-af",
            "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-ar",
            str(SR),
            "-ac",
            "2",
            "-t",
            f"{total_s:.3f}",
            str(vo_wav),
        ]
    )
    vo_norm = read_wav(vo_wav)[:total_samples]
    if len(vo_norm) < total_samples:
        vo_norm = np.pad(vo_norm, ((0, total_samples - len(vo_norm)), (0, 0)))
    write_wav_dithered(vo_norm, vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    # 2. Slice continuous score bed from BED_MP3 starting at slices[0][0]
    bed_start = slices[0][0]
    bed_raw_wav = work / "stem_bed_raw.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-ss",
            f"{bed_start:.3f}",
            "-t",
            f"{total_s:.3f}",
            "-i",
            str(BED_MP3),
            "-af",
            f"afade=t=in:d=0.10,afade=t=out:st={total_s - 0.60:.3f}:d=0.60",
            "-ar",
            str(SR),
            "-ac",
            "2",
            str(bed_raw_wav),
        ]
    )
    raw_bed = read_wav(bed_raw_wav)[:total_samples]
    if len(raw_bed) < total_samples:
        raw_bed = np.pad(raw_bed, ((0, total_samples - len(raw_bed)), (0, 0)))

    # Set initial bed level ~14 dB below VO, then apply J0079 envelope ducking so sfx_kit.py level has 0 breaches
    _, bi0 = sfx_kit.ebur128(bed_raw_wav)
    init_gain_db = (vo_i - 15.0) - bi0
    raw_bed = raw_bed * (10.0 ** (init_gain_db / 20.0))

    T = np.arange(len(raw_bed)) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k_smooth = int(0.35 * SR)
    bed_wav = work / "stem_bed.wav"
    write_wav_dithered(raw_bed, bed_wav)
    for _ in range(10):
        bm, bi = sfx_kit.ebur128(bed_wav)
        n = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:n])
        d = vo_m_arr[:n] - bm_arr
        shortfall = np.where(speaking[:n], np.clip(12.2 - d, 0.0, None), 0.0)
        pause_over = np.where(~speaking[:n], np.clip(bm_arr - (vo_i - 12.5), 0.0, None), 0.0)
        need = np.maximum(shortfall, pause_over)
        if not (d[speaking[:n]] < 10.5).any() and not (bm_arr[~speaking[:n]] > vo_i - 11.0).any():
            break
        held = np.array([need[max(0, i - 3) : min(n, i + 4)].max() for i in range(n)])
        duck[:n] = np.minimum(duck[:n] + held, 20.0)
        env_db = np.convolve(np.interp(T, grid, duck, left=0.0, right=0.0), np.ones(k_smooth) / k_smooth, mode="same")
        write_wav_dithered(raw_bed * (10.0 ** (-env_db / 20.0))[:, None], bed_wav)

    # 3. Build SFX stem from KIT_DIR
    sfx_buf = np.zeros((total_samples, 2), dtype=np.float32)
    kit_files = {
        "whoosh": KIT_DIR / "sfx_owb_whoosh_soft_v01.wav",
        "tick": KIT_DIR / "sfx_owb_tick_ui_v01.wav",
        "rumble": KIT_DIR / "sfx_owb_rumble_low_v01.wav",
    }
    for kind, at_s, gain_db in sfx_hits:
        sample = read_wav(kit_files[kind]) * (10.0 ** (gain_db / 20.0))
        i0 = int(round(at_s * SR))
        i1 = min(total_samples, i0 + len(sample))
        if i1 > i0:
            sfx_buf[i0:i1] += sample[: i1 - i0]

    sfx_wav = work / "stem_sfx.wav"
    write_wav_dithered(sfx_buf, sfx_wav)
    # Ensure SFX stem sits cleanly >= 15 LU under VO integrated and >= 12 LU under VO at every speaking step
    sm, si = sfx_kit.ebur128(sfx_wav)
    target_sfx_i = vo_i - 22.0
    if si > target_sfx_i:
        sfx_buf *= 10.0 ** ((target_sfx_i - si) / 20.0)
        write_wav_dithered(sfx_buf, sfx_wav)
    for _ in range(6):
        sm, si = sfx_kit.ebur128(sfx_wav)
        n = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:n])
        d_speak = vo_m_arr[:n] - sm_arr
        over_pause = np.where(~speaking[:n], sm_arr - (vo_i - 8.0), 0.0)
        under_speak = np.where(speaking[:n], 12.5 - d_speak, 0.0)
        worst = max(float(over_pause.max()), float(under_speak.max()))
        if worst <= 0.0:
            break
        sfx_buf *= 10.0 ** (-(worst + 1.0) / 20.0)
        write_wav_dithered(sfx_buf, sfx_wav)

    # 4. Mix VO + Bed + SFX to -14.0 LUFS
    mix_raw = work / "mix_raw.wav"
    bed_final = read_wav(bed_wav)[:total_samples]
    vo_final = read_wav(vo_wav)[:total_samples]
    write_wav_dithered(vo_final + bed_final + sfx_buf, mix_raw)
    mix_wav = work / "mix.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(mix_raw),
            "-af",
            "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-ar",
            str(SR),
            "-ac",
            "2",
            "-t",
            f"{total_s:.3f}",
            str(mix_wav),
        ]
    )
    _, mix_i = sfx_kit.ebur128(mix_wav)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return {
        "vo_lufs": round(vo_i, 2),
        "bed_lufs": round(bed_i, 2),
        "sfx_lufs": round(sfx_i, 2),
        "mix_lufs": round(mix_i, 2),
    }


# =============================================================================
# Review Sheets (5-point per-Short sheet, cut strip, contact sheet)
# =============================================================================
def make_5pt_frame_sheet(video: Path, times: list[tuple[float, str]], dest: Path, title_hdr: str) -> None:
    """Build the J0895 required 5-frame sheet: (0 s, 4.5 s, 10 s, payoff, end)."""
    tiles = []
    tw, th = 270, 480
    for i, (t, label) in enumerate(times):
        p = WORK / f"pt5_{dest.stem}_{i}.jpg"
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{t:.2f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-vf",
                f"scale={tw}:{th}",
                str(p),
            ]
        )
        tiles.append((Image.open(p).convert("RGB"), t, label))
    canvas = Image.new("RGB", (tw * len(tiles), th + 64), (16, 22, 34))
    d = ImageDraw.Draw(canvas)
    f_hdr = ImageFont.truetype(FONT_BOLD, 20)
    f_sub = ImageFont.truetype(FONT_BOLD, 17)
    d.text((12, 8), title_hdr, font=f_hdr, fill=(255, 224, 0))
    for i, (im, t, label) in enumerate(tiles):
        x = i * tw
        canvas.paste(im, (x, 34))
        d.text((x + 8, th + 38), f"{label} ({t:.1f}s)", font=f_sub, fill=(255, 255, 255))
    canvas.save(dest, quality=92)


def make_cut_strip(video: Path, cuts: list[dict], total_s: float, dest: Path) -> None:
    bounds = [0.0] + [round(c["timeline_out"], 2) for c in cuts]
    rows = []
    for b in bounds:
        start = max(0.0, round(b - 0.2, 3))
        length = min(0.4, round(total_s - start, 3))
        if length <= 0.05:
            continue
        tile = WORK / f"cutrow_{dest.stem}_{b:.2f}.jpg"
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{start:.3f}",
                "-t",
                f"{length:.3f}",
                "-i",
                str(video),
                "-vf",
                f"fps={FPS},scale=120:214,tile=12x1",
                "-frames:v",
                "1",
                str(tile),
            ]
        )
        rows.append((tile, b, start))
    im0 = Image.open(rows[0][0])
    w, h = im0.size
    canvas = Image.new("RGB", (w, (h + 18) * len(rows)), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (tile, b, start) in enumerate(rows):
        y = i * (h + 18)
        canvas.paste(Image.open(tile), (0, y))
        d.text((6, y + h + 2), f"cut {b:.2f}s  frames from {start:.2f}s", fill=(255, 220, 0))
    canvas.save(dest, quality=90)


# =============================================================================
# Specifications for the 3 Shorts (SHORTS_PLAN_v01.md)
# =============================================================================
SHORTS_SPECS = [
    {
        "slug": "mon30_comets",
        "stem": "028_short_mon30_comets_v01",
        "day_label": "Mon 30 Nov",
        "air_date": "2026-11-30",
        "title": "Why Will Gliese 710's Comets Arrive After It Has Gone?",
        "hook_rows": [("10 COMETS", WHITE), ("A YEAR", YELLOW)],
        "cover_src": HDIR / "comet_a3.jpg",
        "cover_crop": (0.18, 0.04, 0.72, 0.88),
        "cover_rows": [("AFTER IT'S", WHITE), ("GONE?", YELLOW)],
        # Master VO slices: s53 (281.64-293.82 = 12.18s) + s55-58 (297.00-315.76 = 18.76s, includes 0.30s VO tail after 315.46)
        "vo_slices": [(281.64, 293.82), (297.00, 315.76)],
        "last_word_s": 30.64,  # "dark." ends at 12.18 + (315.46 - 297.00) = 30.64 s; VO tail runs to 30.94 s
        "total_s": 32.64,      # 30.64 s + 2.00 s end card = 32.64 s
        "payoff_sample_s": 26.5,
        "sfx_hits": [
            ("whoosh", 0.00, -5.0),
            ("tick", 9.00, -4.0),
            ("tick", 15.80, -4.0),
            ("whoosh", 22.62, -7.0),
            ("tick", 30.64, -4.0),
        ],
        # Picture cuts (every cut inside a VO pause, every shot 2.42-4.12 s, max < 6.0 s):
        "plates": [
            {
                "row": "s01_hale_bopp_close",
                "in": 0.00,
                "out": 2.88,  # pause after "Gliese 710" (2.72-3.00s)
                "kind": "still",
                "src": "sts083_hale_bopp.jpg",
                "box": (0.24, 0.10, 0.72, 0.86),
                "pct": 0.05,
                "open_push": 0.26,
                "gamma": 0.78,
                "lift": 8.0,
                "color": 1.16,
                "contrast": 1.14,
            },
            {
                "row": "s02_hale_bopp_wide",
                "in": 2.88,
                "out": 5.64,  # comma pause after "10 extra comets a year," (5.42-5.86s)
                "kind": "still",
                "src": "sts083_hale_bopp.jpg",
                "box": (0.12, 0.06, 0.68, 0.94),
                "pct": 0.06,
                "gamma": 0.80,
                "lift": 8.0,
                "color": 1.14,
                "contrast": 1.12,
            },
            {
                "row": "s03_comet_a3_core",
                "in": 5.64,
                "out": 8.06,  # comma pause after "close enough for us to see," (7.78-8.34s)
                "kind": "still",
                "src": "comet_a3.jpg",
                "box": (0.10, 0.14, 0.72, 0.96),
                "pct": 0.05,
                "gamma": 0.56,
                "lift": 12.0,
                "color": 1.12,
                "contrast": 1.10,
            },
            {
                "row": "s04_comet_a3_tail",
                "in": 8.06,
                "out": 12.08,  # sentence pause after "three to four million years." (11.88-12.28s)
                "kind": "still",
                "src": "comet_a3.jpg",
                "box": (0.14, 0.04, 0.66, 0.86),
                "pct": 0.06,
                "gamma": 0.56,
                "lift": 12.0,
                "color": 1.12,
                "contrast": 1.10,
            },
            {
                "row": "s05_r27_shower_s1",
                "in": 12.08,
                "out": 15.63,  # sentence pause after "while the star is passing." (15.22-16.04s)
                "kind": "code",
                "src": "code_graphic_028_mon_r27_s1.mp4",
                "mode": "r27_shower_s1",
                "t_offset": 0.0,
                "zoom_range": (0.95, 1.05),
                "pan_xy": (0.0, 0.0),
                "band_label": None,  # clear of 9-14 s title banner!
            },
            {
                "row": "s06_r27_shower_s2",
                "in": 15.63,
                "out": 18.60,  # pause after "Why? Because they are so far" (18.54-18.66s)
                "kind": "code",
                "src": "code_graphic_028_mon_r27_s2.mp4",
                "mode": "r27_shower_s2",
                "t_offset": 3.5,
                "zoom_range": (1.12, 1.24),
                "pan_xy": (-25.0, -15.0),
                "band_label": (0.20, 2.80, "SO FAR OUT"),  # 15.83-18.43 s, inside 16:9 band
            },
            {
                "row": "s07_r27_shower_s3",
                "in": 18.60,
                "out": 22.62,  # sentence pause after "hundreds of thousands of years." (22.26-22.98s)
                "kind": "code",
                "src": "code_graphic_028_mon_r27_s3.mp4",
                "mode": "r27_shower_s3",
                "t_offset": 7.0,
                "zoom_range": (1.26, 1.38),
                "pan_xy": (20.0, 15.0),
                "band_label": None,
            },
            {
                "row": "s08_r27_leaving_a",
                "in": 22.62,
                "out": 25.21,  # comma pause after "at its height," (25.00-25.42s)
                "kind": "video",
                "src": "eso_startrails.mp4",
                "offset": 14.0,
                "crop_box": (540, 960, 740, 60),
            },
            {
                "row": "s09_r27_leaving_b",
                "in": 25.21,
                "out": 28.59,  # comma pause after "heading away again," (28.34-28.84s)
                "kind": "video",
                "src": "eso_startrails.mp4",
                "offset": 17.5,
                "crop_box": (608, 1080, 656, 0),
            },
            {
                "row": "s10_r27_leaving_c",
                "in": 28.59,
                "out": 32.64,  # through "shrinking back into the dark." (30.64s) + 2.00s end card (30.64-32.64s)
                "kind": "video",
                "src": "eso_startrails.mp4",
                "offset": 21.8,
                "crop_box": (608, 1080, 1120, 0),
            },
        ],
    },
    {
        "slug": "wed02_opening_testA",
        "stem": "028_short_wed02_opening_testA_v01",
        "day_label": "Wed 2 Dec (Test A)",
        "air_date": "2026-12-02",
        "title": "Is a Star Really Coming Towards Us?",
        "hook_rows": [("A STAR IS", WHITE), ("COMING", YELLOW)],
        "cover_src": THUMB_ART_DIR / "gliese_art_A.png",
        "cover_crop": (0.22, 0.0, 0.78, 1.0),
        "cover_rows": [("COMING", YELLOW), ("TOWARDS US?", WHITE)],
        # Master VO slice: 0.00-30.44 s (last word "system." ends at 30.14s, 0.30s audio tail to 30.44s)
        "vo_slices": [(0.00, 30.44)],
        "last_word_s": 30.14,
        "total_s": 32.14,      # 30.14 s + 2.00 s end card = 32.14 s (Test A 30-38 s window)
        "payoff_sample_s": 27.8,
        "sfx_hits": [
            ("whoosh", 0.00, -5.0),
            ("tick", 9.00, -4.0),
            ("rumble", 17.61, -6.0),
            ("tick", 17.85, -4.0),
            ("tick", 30.14, -4.0),
        ],
        "plates": [
            {
                "row": "s01_r01_gaia_a",
                "in": 0.00,
                "out": 2.68,  # sentence pause after "coming towards us." (2.36-3.00s)
                "kind": "video",
                "src": "gaia_motion_1_6my.mp4",
                "offset": 3.80,
                "crop_box": (1080, 1920, 1380, 120),
                "open_push": 0.18,
            },
            {
                "row": "s02_r01_gaia_b",
                "in": 2.68,
                "out": 6.00,  # sentence pause after "should you worry?" (5.60-6.64s)
                "kind": "video",
                "src": "gaia_motion_1_6my.mp4",
                "offset": 7.00,
                "crop_box": (1080, 1920, 680, 160),
            },
            {
                "row": "s03_r01_gaia_c",
                "in": 6.00,
                "out": 9.00,  # sentence pause after "not a rumor." (8.84-9.36s)
                "kind": "video",
                "src": "gaia_motion_1_6my.mp4",
                "offset": 11.00,
                "crop_box": (1080, 1920, 2020, 140),
            },
            {
                "row": "s04_r01_gaia_d",
                "in": 9.00,
                "out": 13.66,  # sentence pause after "straight at the sun." (13.18-14.14s)
                "kind": "video",
                "src": "gaia_motion_1_6my.mp4",
                "offset": 15.00,
                "crop_box": (1152, 2048, 1344, 56),
            },
            {
                "row": "s05_r03_serpens_sky",
                "in": 13.66,
                "out": 17.61,  # sentence pause after "Its name is Gliese 710." (17.20-18.02s)
                "kind": "still",
                "src": "gaia_edr3_sky.png",
                "box": (0.22, 0.02, 0.78, 0.98),
                "pct": 0.05,
                "gamma": 0.88,
                "lift": 4.0,
                "color": 1.12,
                "contrast": 1.10,
            },
            {
                "row": "s06_r04_shell_s1",
                "in": 17.61,
                "out": 20.66,  # comma pause after "one point three million years," (20.58-20.74s)
                "kind": "code",
                "src": "code_graphic_028_wed_r04_s1.mp4",
                "mode": "r04_shower_s1",
                "t_offset": 0.0,
                "zoom_range": (0.94, 1.04),
                "pan_xy": (0.0, 0.0),
                "band_label": (0.24, 2.85, "1.3 MILLION YEARS"),  # 17.85-20.46s, inside 16:9 band
            },
            {
                "row": "s07_r04_shell_s2",
                "in": 20.66,
                "out": 24.24,  # sentence pause after "any star we know of." (23.82-24.66s)
                "kind": "code",
                "src": "code_graphic_028_wed_r04_s2.mp4",
                "mode": "r04_shower_s2",
                "t_offset": 3.2,
                "zoom_range": (1.12, 1.24),
                "pan_xy": (18.0, -12.0),
                "band_label": None,
            },
            {
                "row": "s08_r04_shell_s3",
                "in": 24.24,
                "out": 26.40,  # comma pause after "It will not hit anything," (26.04-26.74s)
                "kind": "code",
                "src": "code_graphic_028_wed_r04_s3.mp4",
                "mode": "r04_shower_s3",
                "t_offset": 6.8,
                "zoom_range": (1.25, 1.35),
                "pan_xy": (-20.0, 14.0),
                "band_label": None,
            },
            {
                "row": "s09_r04_shell_s4",
                "in": 26.40,
                "out": 32.14,  # through "outer edge of our solar system." (30.14s) + 2.00s end card (30.14-32.14s)
                "kind": "code",
                "src": "code_graphic_028_wed_r04_s4.mp4",
                "mode": "r04_shower_s4",
                "t_offset": 9.0,
                "zoom_range": (1.06, 1.18),
                "pan_xy": (10.0, 0.0),
                "band_label": None,
            },
        ],
    },
    {
        "slug": "fri04_scale",
        "stem": "028_short_fri04_scale_v01",
        "day_label": "Fri 4 Dec",
        "air_date": "2026-12-04",
        "title": "How Close Will Gliese 710 Come to the Sun?",
        "hook_rows": [("A FIFTH OF A", WHITE), ("LIGHT-YEAR", YELLOW)],
        "cover_src": HDIR / "neptune.jpg",
        "cover_crop": (0.14, 0.02, 0.86, 0.98),
        "cover_rows": [("HOW CLOSE", YELLOW), ("TO THE SUN?", WHITE)],
        # Master VO slices: s30 (162.00-166.48 = 4.48s) + s33-36 (178.18-198.82 = 20.64s, includes 0.30s VO tail after 198.52)
        "vo_slices": [(162.00, 166.48), (178.18, 198.82)],
        "last_word_s": 24.82,  # "planets." ends at 4.48 + (198.52 - 178.18) = 24.82 s; VO tail runs to 25.12 s
        "total_s": 26.82,      # 24.82 s + 2.00 s end card = 26.82 s (inside 22.0-27.5 s band)
        "payoff_sample_s": 18.5,
        "sfx_hits": [
            ("whoosh", 0.00, -5.0),
            ("tick", 4.48, -4.0),
            ("tick", 9.00, -4.0),
            ("tick", 12.81, -4.0),
            ("tick", 15.20, -4.0),
            ("tick", 24.82, -4.0),
        ],
        "plates": [
            {
                "row": "s01_r15_16_path",
                "in": 0.00,
                "out": 4.51,  # sentence pause after "a fifth of a light-year." (4.36-4.66s)
                "kind": "code",
                "src": "code_graphic_028_fri_r15_path.mp4",
                "mode": "r15_16_path",
                "t_offset": 1.96,
                "open_push": 0.28,
                "band_label": None,  # frame 0 carries hook caption "A FIFTH OF A / LIGHT-YEAR"
            },
            {
                "row": "s02_r17_scale_a",
                "in": 4.51,
                "out": 8.11,  # sentence pause after "one centimeter." (7.74-8.48s)
                "kind": "code",
                "src": "code_graphic_028_fri_r17_scale_a.mp4",
                "mode": "r17_scale_a",
                "t_offset": 0.0,
                "band_label": None,
            },
            {
                "row": "s03_r17_neptune_a",
                "in": 8.11,
                "out": 10.52,  # comma pause after "Neptune, our outermost planet," (10.34-10.70s)
                "kind": "still",
                "src": "neptune.jpg",
                "box": (0.18, 0.06, 0.82, 0.94),
                "pct": 0.05,
                "gamma": 0.84,
                "lift": 8.0,
                "color": 1.14,
                "contrast": 1.10,
            },
            {
                "row": "s04_r17_neptune_b",
                "in": 10.52,
                "out": 14.70,  # sentence pause after "about the length of a ruler." (14.40-15.00s)
                "kind": "still",
                "src": "neptune.jpg",
                "box": (0.12, 0.02, 0.88, 0.98),
                "pct": 0.06,
                "gamma": 0.84,
                "lift": 8.0,
                "color": 1.14,
                "contrast": 1.10,
            },
            {
                "row": "s05_r17_scale_b",
                "in": 14.70,
                "out": 19.34,  # comma pause after "passes more than 100 meters away," (19.12-19.56s)
                "kind": "code",
                "src": "code_graphic_028_fri_r17_scale_b.mp4",
                "mode": "r17_scale_b",
                "t_offset": 0.0,
                "band_label": (0.50, 4.30, "100 METRES AWAY"),  # 15.20-19.00s, clear of 9-14s title banner!
            },
            {
                "row": "s06_r17_pitch",
                "in": 19.34,
                "out": 21.55,  # sentence pause after "length of a football pitch." (21.12-21.98s)
                "kind": "video",
                "src": "football_pitch_veo_v01.mp4",
                "offset": 1.50,
                "feathered_720p": True,
            },
            {
                "row": "s07_r18_shell",
                "in": 21.55,
                "out": 26.82,  # through "will not come anywhere near the planets." (24.82s) + 2.00s end card (24.82-26.82s)
                "kind": "code",
                "src": "code_graphic_028_fri_r18_shell.mp4",
                "mode": "r18_shell",
                "t_offset": 0.0,
                "band_label": None,
            },
        ],
    },
]

POOL_TITLES = {
    "sts083_hale_bopp.jpg": "NASA STS-83 Space Shuttle photograph of Comet Hale-Bopp over Earth's airglow limb (sts083_hale_bopp.jpg)",
    "comet_a3.jpg": "NASA ISS photograph of Comet C/2023 A3 Tsuchinshan-ATLAS by Matthew Dominick (comet_a3.jpg)",
    "eso_startrails.mp4": "ESO La Silla Observatory night-sky star-trails timelapse by R. Wesson (eso_startrails.mp4)",
    "gaia_motion_1_6my.mp4": "ESA/Gaia proper-motion starfield sweep across 1.6 million years (gaia_motion_1_6my.mp4)",
    "gaia_edr3_sky.png": "ESA/Gaia EDR3 all-sky Milky Way star map toward Serpens Cauda (gaia_edr3_sky.png)",
    "neptune.jpg": "NASA/JPL Voyager 2 full-disk photograph of Neptune (PIA01492 / neptune.jpg)",
    "football_pitch_veo_v01.mp4": "Floodlit football pitch aerial sweep (football_pitch_veo_v01.mp4)",
}


def build_one_short(spec: dict, vcr: VerticalCodeRenderer) -> dict:
    slug = spec["slug"]
    stem = spec["stem"]
    air_date = spec["air_date"]
    total_s = spec["total_s"]
    last_word_s = spec["last_word_s"]
    end_card_in = round(total_s - END_CARD_LEN, 2)

    s_dir = HERE / slug
    out_dir = s_dir / "06_Final-Exports"
    s_work = WORK / slug
    if s_work.exists():
        shutil.rmtree(s_work)
    s_work.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Building {slug} ({spec['day_label']} · {air_date} · {total_s:.2f}s) ===", flush=True)

    # 1. Verify word alignment and build captions (kept clear of 9-14s if desired, or in lower third y=1336)
    words, _ = map_words_for_slices(spec["vo_slices"])
    (s_work / "words.json").write_text(json.dumps(words, indent=2) + "\n")
    caps = build_caption_chunks(words, last_word_s)

    # Audit that no cut clips a spoken word
    clipped_words = []
    for p in spec["plates"]:
        for bt in (p["in"], p["out"]):
            if bt <= 0.05 or bt >= last_word_s - 0.02:
                continue
            bad = [w for w in words if w["s"] < bt - 0.02 and w["e"] > bt + 0.02]
            if bad:
                clipped_words.append({"cut_s": bt, "row": p["row"], "words": bad})
    if clipped_words:
        raise SystemExit(f"{slug}: cut clips word: {clipped_words}")

    # 2. Render overlays (hook, 9-14s title banner, lower-third captions, 2s end card, cover)
    hook_info = make_hook_png(s_work / "hook.png", spec["hook_rows"])
    title_info = make_title_banner_png(s_work / "title.png")
    end_info = make_end_card_png(s_work / "end_card.png")
    for i, c in enumerate(caps):
        c["bbox"] = make_caption_png(s_work / f"cap_{i:02d}.png", c["text"])

    cover_path = out_dir / f"{stem}_cover.jpg"
    cover_info = make_cover_jpg(cover_path, spec["cover_src"], spec["cover_crop"], spec["cover_rows"])

    # 3. Render 9:16 plate pieces and concat
    concat_lines = []
    cuts_json = []
    pool_json = []
    seen_pool = set()
    code_labels_audit = []

    for i, p in enumerate(spec["plates"]):
        piece = s_work / f"piece_{i:02d}.mp4"
        p_dur = round(p["out"] - p["in"], 3)
        if p_dur > 6.01:
            raise SystemExit(f"{slug} {p['row']} duration {p_dur}s > 6.0s limit")
        kind = p["kind"]
        src_name = p["src"]

        if kind == "still":
            up = render_still_9x16(
                HDIR / src_name,
                p_dur,
                piece,
                box=p["box"],
                pct=p.get("pct", 0.05),
                gamma=p.get("gamma", 0.85),
                lift=p.get("lift", 6.0),
                color=p.get("color", 1.12),
                contrast=p.get("contrast", 1.10),
                open_push=p.get("open_push", 0.0),
            )
            cuts_json.append(
                {
                    "row": p["row"],
                    "timeline_in": p["in"],
                    "timeline_out": p["out"],
                    "source": src_name,
                    "upscale": up,
                    "framing": {"box": list(p["box"]), "pct": p.get("pct", 0.05)},
                    "video": False,
                }
            )
        elif kind == "video":
            src_path = VDIR / src_name if "veo" in src_name else HDIR / src_name
            up = render_video_9x16(
                src_path,
                p["offset"],
                p_dur,
                piece,
                crop_box=p.get("crop_box"),
                open_push=p.get("open_push", 0.0),
                feathered_720p=p.get("feathered_720p", False),
            )
            cuts_json.append(
                {
                    "row": p["row"],
                    "timeline_in": p["in"],
                    "timeline_out": p["out"],
                    "source": src_name,
                    "upscale": up,
                    "framing": {"offset": p["offset"]},
                    "video": True,
                }
            )
        elif kind == "code":
            info = vcr.render_clip(
                mode=p["mode"],
                dur_s=p_dur,
                dest=piece,
                t_offset=p.get("t_offset", 0.0),
                zoom_range=p.get("zoom_range", (1.0, 1.06)),
                pan_xy=p.get("pan_xy", (0.0, 0.0)),
                band_label=p.get("band_label"),
                open_push=p.get("open_push", 0.0),
            )
            if p.get("band_label") and info.get("label_bbox"):
                l_in, l_out, l_txt = p["band_label"]
                code_labels_audit.append(
                    {
                        "row": p["row"],
                        "text": l_txt,
                        "short_in": round(p["in"] + l_in, 2),
                        "short_out": round(p["in"] + l_out, 2),
                        "bbox": info["label_bbox"],
                        "inside_16x9_band": (
                            BAND_Y0 <= info["label_bbox"][1] and info["label_bbox"][3] <= BAND_Y1
                        ),
                    }
                )
            cuts_json.append(
                {
                    "row": p["row"],
                    "timeline_in": p["in"],
                    "timeline_out": p["out"],
                    "source": src_name,
                    "upscale": 1.0,
                    "framing": {"offset": 0.0},
                    "video": True,
                }
            )
        else:
            raise ValueError(kind)

        if src_name not in seen_pool:
            seen_pool.add(src_name)
            pool_json.append(
                {
                    "file_id": src_name,
                    "title": POOL_TITLES.get(src_name, f"Our own 9:16 code graphic ({src_name})"),
                }
            )
        concat_lines.append(f"file '{piece.name}'")

    span_list = s_work / "span_list.txt"
    span_list.write_text("\n".join(concat_lines) + "\n")
    pic_span = s_work / "picture_span.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(span_list), "-c", "copy", str(pic_span)])

    # 4. Build audio stems and mix
    aud_info = build_short_audio(s_work, spec["vo_slices"], total_s, spec["sfx_hits"])

    # 5. Composite overlays onto picture_span + mix.wav
    final_mp4 = out_dir / f"{stem}.mp4"
    inputs = [
        "-t",
        f"{total_s:.3f}",
        "-i",
        str(pic_span),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{total_s:.3f}",
        "-i",
        str(s_work / "hook.png"),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{total_s:.3f}",
        "-i",
        str(s_work / "title.png"),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{total_s:.3f}",
        "-i",
        str(s_work / "end_card.png"),
        "-i",
        str(s_work / "mix.wav"),
    ]
    base_idx = 5
    for i in range(len(caps)):
        inputs += [
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-t",
            f"{total_s:.3f}",
            "-i",
            str(s_work / f"cap_{i:02d}.png"),
        ]

    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={TITLE_OUT - 0.30:.2f}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={end_card_in:.2f}:d=0.28:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{end_card_in})*lte(t,{total_s})'[v3]",
    ]
    last_v = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    # Subtle film grain on dark space gradients (STUDIO_PLAYBOOK §5 item 5) + final yuv420p
    fc.append(f"[{last_v}]noise=alls=3:allf=t,format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            *inputs,
            "-filter_complex",
            ";".join(fc),
            "-map",
            "[v]",
            "-map",
            "4:a",
            *enc,
            "-t",
            f"{total_s:.3f}",
            str(final_mp4),
        ]
    )

    # Also build 720p _PHONE.mp4 copy (< 15 MB) for instant mobile playback in OWB UAT
    phone_mp4 = out_dir / f"{stem}_PHONE.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(final_mp4),
            "-vf",
            "scale=720:1280:flags=lanczos",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(phone_mp4),
        ]
    )

    # 6. Write cuts & pool JSON and run all gates
    cuts_path = out_dir / f"{stem}_cuts.json"
    pool_path = out_dir / f"{stem}_pool.json"
    cuts_path.write_text(json.dumps(cuts_json, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_json, indent=2) + "\n")

    gate_json_p = out_dir / f"{stem}_gate.json"
    gate_txt_p = out_dir / f"{stem}_gate.txt"
    gate_j = sp.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check",
            str(final_mp4),
            "--air-date",
            air_date,
            "--sheet-dir",
            str(out_dir),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    gate_json_p.write_text(gate_j.stdout or gate_j.stderr)
    gate_t = sp.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check",
            str(final_mp4),
            "--air-date",
            air_date,
            "--sheet-dir",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
    )
    gate_txt_p.write_text(gate_t.stdout or gate_t.stderr)

    sfx_chk = sp.run(
        [
            sys.executable,
            str(REPO / "scripts/sfx_kit.py"),
            "level",
            "--vo",
            str(s_work / "stem_vo.wav"),
            "--sfx",
            str(s_work / "stem_sfx.wav"),
            "--bed",
            str(s_work / "stem_bed.wav"),
            "--minutes",
            f"{total_s / 60.0:.3f}",
        ],
        capture_output=True,
        text=True,
    )
    sfx_txt_p = out_dir / f"{stem}_sfx.txt"
    sfx_txt_p.write_text((sfx_chk.stdout or "") + (sfx_chk.stderr or ""))

    pg_json_p = out_dir / f"{stem}_polish_gate.json"
    pg_txt_p = out_dir / f"{stem}_polish_gate.txt"
    pg_chk = sp.run(
        [
            sys.executable,
            str(REPO / "scripts/polish_gate.py"),
            str(final_mp4),
            "--cuts",
            str(cuts_path),
            "--reviewed-ok",
            str(REV_OK_LONG),
            "--out",
            str(pg_json_p),
        ],
        capture_output=True,
        text=True,
    )
    pg_txt_p.write_text((pg_chk.stdout or "") + (pg_chk.stderr or ""))

    pqa_dir = out_dir / f"{stem}_picture_qa"
    pqa_txt_p = out_dir / f"{stem}_picture_qa.txt"
    pqa_chk = sp.run(
        [
            sys.executable,
            str(REPO / "scripts/picture_qa.py"),
            str(final_mp4),
            "--cuts",
            str(cuts_path),
            "--pool",
            str(pool_path),
            "--reviewed-ok",
            str(REV_OK_LONG),
            "--out-dir",
            str(pqa_dir),
        ],
        capture_output=True,
        text=True,
    )
    pqa_txt_p.write_text((pqa_chk.stdout or "") + (pqa_chk.stderr or ""))

    cover_prev_p = out_dir / f"{stem}_cover_preview.jpg"
    cov_chk = sp.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "short",
            str(cover_path),
            "--out",
            str(cover_prev_p),
            "--score",
        ],
        capture_output=True,
        text=True,
    )
    cover_score_txt = (cov_chk.stdout or "") + (cov_chk.stderr or "")

    # 7. Build J0895 required 5-point frame sheet: (0 s, 4.5 s, 10 s, payoff, end) + cut strip
    pt5_times = [
        (0.25, "0s Open"),
        (4.50, "4.5s Seam"),
        (10.00, "10s Banner"),
        (spec["payoff_sample_s"], "Payoff"),
        (round(total_s - 1.0, 2), "End Card"),
    ]
    frames_5pt_p = out_dir / f"{stem}_frames_5pt.jpg"
    make_5pt_frame_sheet(final_mp4, pt5_times, frames_5pt_p, f"{spec['day_label']} · {spec['title']}")
    cut_strip_p = out_dir / f"{stem}_cut_strip.jpg"
    make_cut_strip(final_mp4, cuts_json, total_s, cut_strip_p)

    # 8. Title-safe & caption audit
    all_bboxes_ok = True
    for bb in hook_info["bboxes"]:
        if not (54 <= bb[0] and bb[2] <= W - 54 and 120 <= bb[1] and bb[3] <= BAND_Y0 - 10):
            all_bboxes_ok = False
    for r in title_info["rows"]:
        bb = r["bbox"]
        if not (54 <= bb[0] and bb[2] <= W - 54 and BAND_Y0 <= bb[1] and bb[3] <= BAND_Y1):
            all_bboxes_ok = False
    for r in end_info["rows"]:
        bb = r["bbox"]
        if not (54 <= bb[0] and bb[2] <= W - 54 and BAND_Y0 <= bb[1] and bb[3] <= BAND_Y1):
            all_bboxes_ok = False
    for c in caps:
        bb = c["bbox"]
        if not (54 <= bb[0] and bb[2] <= W - 54 and BAND_Y1 + 20 <= bb[1] and bb[3] <= H - 220):
            all_bboxes_ok = False
    for cl in code_labels_audit:
        bb = cl["bbox"]
        if not (54 <= bb[0] and bb[2] <= W - 54 and BAND_Y0 <= bb[1] and bb[3] <= BAND_Y1):
            all_bboxes_ok = False
        # Verify no overlap with 0-2.2s hook or 9-14s title banner or end card
        if cl["short_in"] < HOOK_END or (cl["short_in"] < TITLE_OUT and cl["short_out"] > TITLE_IN) or cl["short_out"] > end_card_in:
            all_bboxes_ok = False

    gate_data = json.loads(gate_json_p.read_text())[0]
    meta = {
        "job": "J0895",
        "slug": slug,
        "stem": stem,
        "day": spec["day_label"],
        "air_date": air_date,
        "title": spec["title"],
        "long": {"id": LONG_ID, "title": LONG_TITLE, "master": "028_Gliese710_full_master_v03.mp4"},
        "file": str(final_mp4.relative_to(REPO)),
        "phone_file": str(phone_mp4.relative_to(REPO)),
        "sha256": sha256(final_mp4),
        "phone_sha256": sha256(phone_mp4),
        "duration_s": round(dur(final_mp4), 2),
        "vo_slices_master_s": spec["vo_slices"],
        "last_word_s": last_word_s,
        "vo_tail_s": VO_TAIL_S,
        "end_card_window_s": [end_card_in, total_s],
        "title_banner_window_s": [TITLE_IN, TITLE_OUT],
        "hook_window_s": [0.0, HOOK_END],
        "words_count": len(words),
        "captions_count": len(caps),
        "cuts_count": len(cuts_json),
        "max_shot_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts_json), 2),
        "min_shot_s": round(min(c["timeline_out"] - c["timeline_in"] for c in cuts_json), 2),
        "hook": hook_info,
        "title_banner": title_info,
        "end_card": end_info,
        "code_labels": code_labels_audit,
        "cover": {**cover_info, "score_output": cover_score_txt.strip()},
        "audio": aud_info,
        "gates": {
            "gate_shorts_open": gate_data["verdict"],
            "gate_shorts_open_warns": gate_data["warns"],
            "gate_shorts_open_motion_0_1s": gate_data["motion_0_1s"],
            "gate_shorts_open_visor_frac": gate_data.get("orbit", {}).get("visor_frac", 0.0),
            "sfx_kit_level": "PASS" if sfx_chk.returncode == 0 else "FAIL",
            "polish_gate": "PASS" if pg_chk.returncode == 0 else "FAIL",
            "picture_qa": "PASS" if pqa_chk.returncode == 0 else "FAIL",
            "cover_preview_score": "PASS" if cov_chk.returncode == 0 else "FAIL",
            "caption_and_title_safe": "PASS" if (all_bboxes_ok and not clipped_words) else "FAIL",
        },
        "spend": "£0 (0 credits)",
    }
    (out_dir / f"{stem}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    print(
        f"  -> {stem}: dur={meta['duration_s']}s shots={meta['cuts_count']} (max {meta['max_shot_s']}s) "
        f"open={meta['gates']['gate_shorts_open']} (motion={gate_data['motion_0_1s']}, visor={meta['gates']['gate_shorts_open_visor_frac']}) "
        f"sfx={meta['gates']['sfx_kit_level']} polish={meta['gates']['polish_gate']} pqa={meta['gates']['picture_qa']} "
        f"cover={meta['gates']['cover_preview_score']} safe={meta['gates']['caption_and_title_safe']}",
        flush=True,
    )
    if any(v != "PASS" for k, v in meta["gates"].items() if k not in ("gate_shorts_open_warns", "gate_shorts_open_motion_0_1s", "gate_shorts_open_visor_frac")):
        print("GATE FAILURE DETAILS:", json.dumps(meta["gates"], indent=2))
        print(gate_t.stdout, gate_t.stderr)
        print(sfx_chk.stdout, sfx_chk.stderr)
        print(pg_chk.stdout, pg_chk.stderr)
        print(pqa_chk.stdout, pqa_chk.stderr)
        raise SystemExit(f"Gate failed on {slug}")

    # Copy to pack, OWB UAT, and NAS staging
    PACK.mkdir(parents=True, exist_ok=True)
    for p in (
        frames_5pt_p,
        cut_strip_p,
        cover_prev_p,
        out_dir / f"{stem}_open_sheet.jpg",
        gate_json_p,
        gate_txt_p,
        sfx_txt_p,
        pg_json_p,
        pg_txt_p,
        pqa_txt_p,
        cuts_path,
        pool_path,
        out_dir / f"{stem}_meta.json",
    ):
        if p.exists():
            shutil.copy2(p, PACK / p.name)

    try:
        if UAT_ROOT.exists():
            for p_top in (final_mp4, phone_mp4):
                dst_top = UAT_ROOT / p_top.name
                if dst_top.exists():
                    dst_top.unlink()
                shutil.copy2(p_top, dst_top)
            uat_sub = UAT_ROOT / stem
            uat_sub.mkdir(parents=True, exist_ok=True)
            for p in (final_mp4, phone_mp4, cover_path, cover_prev_p, frames_5pt_p, cut_strip_p, out_dir / f"{stem}_meta.json"):
                if p.exists():
                    dst_sub = uat_sub / p.name
                    if dst_sub.exists():
                        dst_sub.unlink()
                    shutil.copy2(p, dst_sub)
    except OSError as exc:
        print(f"warn: UAT copy skipped: {exc}")

    try:
        if NAS_STAGE.parent.exists():
            NAS_STAGE.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_mp4, NAS_STAGE / final_mp4.name)
            shutil.copy2(phone_mp4, NAS_STAGE / phone_mp4.name)
            shutil.copy2(cover_path, NAS_STAGE / cover_path.name)
    except OSError as exc:
        print(f"warn: NAS copy skipped: {exc}")

    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="Build only one slug (mon30_comets, wed02_opening_testA, fri04_scale)")
    ap.add_argument("--pack-only", action="store_true", help="Assemble combined pack from existing built Shorts")
    ns = ap.parse_args()

    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    vcr = VerticalCodeRenderer(CDIR / "assets")

    if ns.pack_only:
        results = [json.loads((HERE / s["slug"] / "06_Final-Exports" / f"{s['stem']}_meta.json").read_text()) for s in SHORTS_SPECS]
    else:
        specs = [s for s in SHORTS_SPECS if not ns.only or s["slug"] == ns.only]
        results = []
        for spec in specs:
            results.append(build_one_short(spec, vcr))

    if not ns.only:
        # Build combined 3x5 frame overview sheet and combined cover preview sheet in PACK
        rows_im = [Image.open(PACK / f"{s['stem']}_frames_5pt.jpg").convert("RGB") for s in SHORTS_SPECS]
        w_all = max(im.width for im in rows_im)
        h_all = sum(im.height for im in rows_im)
        combined = Image.new("RGB", (w_all, h_all), (16, 22, 34))
        y = 0
        for im in rows_im:
            combined.paste(im, (0, y))
            y += im.height
        combined.save(PACK / "shorts_v01_all_frames_sheet.jpg", quality=92)

        covers = [HERE / s["slug"] / "06_Final-Exports" / f"{s['stem']}_cover.jpg" for s in SHORTS_SPECS]
        run(
            [
                sys.executable,
                str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                "short",
                *[str(c) for c in covers],
                "--out",
                str(PACK / "shorts_v01_covers_preview.jpg"),
                "--score",
            ]
        )

        # Write summary, caption/title-safe audit, and SHA256 manifest
        audit = {
            "job": "J0895",
            "film": "028_A-Star-Is-Coming-Toward-Us",
            "long_id": LONG_ID,
            "long_title": LONG_TITLE,
            "canvas": [W, H],
            "centre_band_16x9_y": [BAND_Y0, BAND_Y1],
            "all_title_safe": True,
            "zero_clipped_words": True,
            "zero_orbit_frame0": True,
            "zero_orbit_covers": True,
            "shorts": [
                {
                    "slug": r["slug"],
                    "stem": r["stem"],
                    "air_date": r["air_date"],
                    "duration_s": r["duration_s"],
                    "max_shot_s": r["max_shot_s"],
                    "hook_bboxes": r["hook"]["bboxes"],
                    "title_banner_rows": r["title_banner"]["rows"],
                    "end_card_rows": r["end_card"]["rows"],
                    "code_labels": r["code_labels"],
                    "cover_bboxes": r["cover"]["bboxes"],
                    "gates": r["gates"],
                }
                for r in results
            ],
        }
        (PACK / "caption_title_safe_audit_v01.json").write_text(json.dumps(audit, indent=2) + "\n")
        (PACK / "summary_v01.json").write_text(json.dumps(results, indent=2) + "\n")

        sha_lines = []
        for r in results:
            sha_lines.append(f"{r['sha256']}  {Path(r['file']).name}")
            sha_lines.append(f"{r['phone_sha256']}  {Path(r['phone_file']).name}")
        (PACK / "SHA256.txt").write_text("\n".join(sha_lines) + "\n")

    print("ALL requested Shorts built and gated successfully.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
