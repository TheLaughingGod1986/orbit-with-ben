#!/usr/bin/env python3
"""028 Short v01 — Gliese 710 Night Sky: 3x Brighter Than Sirius, 1 Moon Width / 35 Years (J0897, backlog).

028 (A Star Is Coming Into Our Solar System / Gliese 710, F-jImX5h7ws) is the locked OWB long with the fewest
Shorts built (3 weekday Shorts, 0 backlog lift Shorts vs 3-5 lift Shorts on 021-027).
Lifts its own VO and picture from Chapter 5 ("A New Brightest Star", Reserve Sky Short in SHORTS_PLAN_v01.md):
  - Slice 1 (340.96-354.60 s, 13.64 s): "A new star has been brightening for thousands of years. Now it is the
    brightest star in the whole night sky, about three times brighter than Sirius, and as bright as Jupiter at its
    best. And it glows orange."
  - Slice 2 (364.40-373.26 s, 8.86 s): "Most stars look fixed for a lifetime. This one will creep across the sky
    by about the width of the full Moon every thirty-five years."
64 spoken words, 22.20 s VO (with 0.30 s audio tail to 22.50 s) + 2.30 s end card = 24.50 s total (inside 22-27 s).
Spend: £0 (0 credits; existing VO + existing score bed + house SFX kit only). Never upload.
"""
from __future__ import annotations

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
SHORTS_DIR = HERE.parent
FILM = SHORTS_DIR.parent
REPO = FILM.parents[1]
EDIT = FILM / "07_Edit-Project"
HDIR = EDIT / "nasa_pool_v01" / "028_harvest_v01"
CDIR = EDIT / "code_graphics_v02"
VO_WAV = FILM / "02_Voiceover" / "star_coming_vo_v01.wav"
BED_MP3 = FILM / "05_Music" / "gliese_score_bed_v03.mp3"
KIT_DIR = FILM / "06_Sound-Effects" / "kit_v01"
WORDS_JSON = EDIT / "full_master_v03_pack" / "gliese_words_list.json"
REV_OK_LONG = EDIT / "full_master_v03_pack" / "reviewed_ok_v03.json"

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/gliese028_night_sky_35yr_work_v01")
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
YELLOW = (255, 224, 0, 255)
GOLD = (255, 214, 64)
ICE = (169, 216, 255)

STEM = "028_short_lift_night_sky_35yr_v01"
SHORT_TITLE = "What Will the Night Sky Look Like When Gliese 710 Arrives?"
AIR_DATE = "2026-12-07"
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
HOOK_ROWS = [("3X BRIGHTER", YELLOW), ("THAN SIRIUS", WHITE)]
COVER_ROWS = [("BRIGHTER THAN", WHITE), ("SIRIUS", YELLOW)]

HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
VO_SLICES = [(340.96, 354.60), (364.40, 373.26)]  # 13.64 s + 8.86 s = 22.50 s (includes 0.30 s tail after 22.20 s)
LAST_WORD_S = 22.20
VO_TAIL_S = 0.30
END_CARD_LEN = 2.30
TOTAL_S = 24.50  # 22.20 s + 2.30 s end card = 24.50 s
END_CARD_IN = round(TOTAL_S - END_CARD_LEN, 2)  # 22.20 s

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


class SkyCodeRenderer:
    """Renders 028's Chapter 5 night-sky teaching graphics natively at 1080x1920 (9:16) inside the 16:9 centre band."""

    def __init__(self, assets_dir: Path, moon_src: Path):
        self.sun = Image.open(assets_dir / "sun_sdo.jpg").convert("RGB").crop((140, 15, 1560, 1435))
        self.moon = Image.open(moon_src).convert("RGB").crop((220, 220, 3020, 3020))
        self.rng = np.random.default_rng(710)
        self.stars = self.rng.uniform([50, 90], [1030, 1830], (140, 2))

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
        srng = np.random.default_rng(7105)
        for n_stars, r_px, alpha in [(520, 2.2, 135), (220, 3.2, 165), (65, 4.5, 185)]:
            for sx, sy in srng.uniform([35, 60], [1045, 1860], (n_stars, 2)):
                ld.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=(215, 232, 252, alpha))
        self.background = Image.alpha_composite(bg.convert("RGBA"), layer).convert("RGB")
        self.bodies: dict = {}

    def body(self, im: Image.Image, xy: tuple[float, float], r: float, kind: str = "gliese") -> None:
        r_i = max(4, int(round(r)))
        key = (r_i, kind)
        if key not in self.bodies:
            if kind == "moon":
                b_im = ImageOps.fit(self.moon, (2 * r_i, 2 * r_i), method=Image.Resampling.LANCZOS)
                b_im = ImageEnhance.Contrast(b_im).enhance(1.18)
            elif kind == "sirius":
                b_im = ImageOps.fit(self.sun, (2 * r_i, 2 * r_i), method=Image.Resampling.LANCZOS)
                grey = ImageOps.grayscale(b_im)
                b_im = ImageOps.colorize(grey, (40, 75, 130), (225, 242, 255))
            else:
                b_im = ImageOps.fit(self.sun, (2 * r_i, 2 * r_i), method=Image.Resampling.LANCZOS)
                grey = ImageOps.grayscale(b_im)
                b_im = ImageOps.colorize(grey, (92, 42, 16), (255, 196, 68))
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
            xx = 48 + (x - 48 + t * (12 + (k % 5) * 5)) % (W - 96)
            yy = 80 + (y - 80 + t * (5 + (k % 3) * 3)) % (H - 160)
            d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(165, 192, 224))
        return im

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
        box = d.textbbox(xy, text, font=f, anchor="mm", stroke_width=4)
        d.text(
            xy,
            text,
            font=f,
            fill=(*color[:3], int(255 * alpha)),
            anchor="mm",
            stroke_width=4,
            stroke_fill=(12, 23, 39, int(235 * alpha)),
        )
        im.paste(layer, (0, 0), layer)
        return list(box)

    def render_clip(
        self,
        mode: str,
        dur_s: float,
        dest: Path,
        t_offset: float = 0.0,
        band_label: tuple[float, float, str] | None = None,
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
            im = self.base(t, speed_px=18.0)
            d = ImageDraw.Draw(im)

            if mode == "r29_sky_bright":
                # Sirius vs Gliese 710 (3.1x brighter than Sirius, V = -2.7 vs -1.46) inside 16:9 centre band
                sx, gx, cy = 300.0, 760.0, 965.0
                self.body(im, (sx, cy), 34, kind="sirius")
                f = ease(min(1.0, u * 1.35))
                r_g = 24.0 + 36.0 * f
                self.body(im, (gx, cy), r_g, kind="gliese")
                # Calibrated brightness comparison bars below the stars inside the 16:9 band
                bar_y = cy + 115
                d.rounded_rectangle((170, bar_y, 430, bar_y + 24), radius=8, fill=(52, 72, 98))
                d.rounded_rectangle((630, bar_y, 890, bar_y + 24), radius=8, fill=(52, 72, 98))
                d.rounded_rectangle((170, bar_y, 170 + int(84 * f), bar_y + 24), radius=8, fill=ICE)
                d.rounded_rectangle((630, bar_y, 630 + int(260 * f), bar_y + 24), radius=8, fill=GOLD)
                self.draw_band_label(im, "Sirius", (sx, cy - 72), size=40, color=ICE)
                self.draw_band_label(im, "Gliese 710", (gx, cy - 84), size=42, color=GOLD)

            elif mode == "r31_sky_creep":
                # Gliese 710 creeping across the sky by 1 full Moon width (30 arcmin) every 35 years
                mx, my, mr = 540.0, 1020.0, 92.0
                self.body(im, (mx, my), mr, kind="moon")
                # Ruler bracket above the Moon showing 1 full Moon width
                by = my - mr - 36
                x_left, x_right = mx - mr, mx + mr
                d.line((x_left, by, x_right, by), fill=ICE, width=4)
                for xx in (x_left, x_right):
                    d.line((xx, by - 14, xx, by + 14), fill=ICE, width=4)
                gx = x_left + (x_right - x_left) * ease(u)
                self.body(im, (gx, by - 46), 30, kind="gliese")
                d.line((x_left, by - 46, gx, by - 46), fill=GOLD, width=5)
                self.draw_band_label(im, "Full Moon", (mx, my + mr + 44), size=38, color=WHITE[:3])
                self.draw_band_label(im, "Gliese 710", (min(max(gx, 320.0), 760.0), by - 96), size=38, color=GOLD)
            else:
                raise ValueError(f"Unknown mode: {mode}")

            if band_label is not None:
                l_in, l_out, l_txt = band_label
                if l_in <= lt <= l_out:
                    alpha = min(ease((lt - l_in) / 0.35), ease((l_out - lt) / 0.35))
                    bb = self.draw_band_label(
                        im,
                        l_txt,
                        (540, BAND_Y0 + 66 + int(10 * (1.0 - alpha))),
                        size=48,
                        color=GOLD,
                        alpha=alpha,
                    )
                    label_bboxes.append(bb)

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


def render_still_9x16(
    src: Path,
    dur_s: float,
    dest: Path,
    box: tuple[float, float, float, float],
    pct: float = 0.06,
    gamma: float = 0.85,
    lift: float = 6.0,
    color: float = 1.12,
    contrast: float = 1.10,
    open_push: float = 0.0,
) -> float:
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
        if open_push > 0 and lt < 1.0:
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
    crop_box: tuple[int, int, int, int] = (608, 1080, 656, 0),
    open_push: float = 0.0,
) -> float:
    cw, ch, cx, cy = crop_box
    upscale = round(max(W / cw, H / ch), 3)
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
    im = Image.open(bg_src).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * crop_box[0]), int(h * crop_box[1]), int(w * crop_box[2]), int(h * crop_box[3])))
    im = ImageOps.fit(im, (W, H), method=Image.Resampling.LANCZOS)

    im = ImageEnhance.Color(im).enhance(1.55)
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


def build_short_audio(
    work: Path,
    slices: list[tuple[float, float]],
    total_s: float,
    sfx_hits: list[tuple[str, float, float]],
) -> dict:
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
                f"afade=t=in:d=0.02,afade=t=out:st={max(0.0, seg_dur - 0.04):.3f}:d=0.04",
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


def make_contact_sheet(video: Path, dest: Path) -> None:
    times = [0.0, 0.5, 1.6, 4.5, 7.5, 11.0, 14.0, 17.5, 20.5, TOTAL_S - 0.8]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
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
                "scale=216:384",
                str(p),
            ]
        )
        tiles.append((p, t))
    cols, rows_n = 5, 2
    canvas = Image.new("RGB", (216 * cols, 410 * rows_n), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(tiles):
        cx = (i % cols) * 216
        cy = (i // cols) * 410
        canvas.paste(Image.open(p), (cx, cy))
        d.text((cx + 8, cy + 388), f"{t:.1f}s", fill=(255, 255, 255))
    canvas.save(dest, quality=92)


PLATES = [
    {
        # 0.00-3.54 s: "A new star has been brightening for thousands of years." (pause 3.14-3.94 s)
        # Frame 0: ESO La Silla Milky Way night-sky timelapse by S. Brunier (eso_mw_lasilla.mp4)
        "row": "s01_mw_lasilla_open",
        "in": 0.00,
        "out": 3.54,
        "kind": "video",
        "src": "eso_mw_lasilla.mp4",
        "offset": 1.00,
        "crop_box": (608, 1080, 656, 0),
        "open_push": 0.16,
    },
    {
        # 3.54-6.90 s: "Now it is the brightest star in the whole night sky," (pause 6.62-7.18 s)
        "row": "s02_serpens_sky",
        "in": 3.54,
        "out": 6.90,
        "kind": "still",
        "src": "wise_sky.jpg",
        "box": (0.18, 0.04, 0.82, 0.96),
        "pct": 0.05,
        "gamma": 0.86,
        "lift": 4.0,
        "color": 1.14,
        "contrast": 1.10,
    },
    {
        # 6.90-9.32 s: "about three times brighter than Sirius," (pause 9.12-9.52 s)
        "row": "s03_r29_sky_bright",
        "in": 6.90,
        "out": 9.32,
        "kind": "code",
        "src": "code_graphic_028_lift_r29_sky_bright.mp4",
        "mode": "r29_sky_bright",
        "t_offset": 0.0,
        "band_label": None,  # clear of 9-14 s title banner
    },
    {
        # 9.32-13.59 s: "and as bright as Jupiter at its best. And it glows orange." (pause 13.44-13.74 s)
        # Carries the 9.0-14.0 s exact long title banner over real Juno Jupiter photograph
        "row": "s04_jupiter_juno",
        "in": 9.32,
        "out": 13.59,
        "kind": "still",
        "src": "jupiter_juno.tif",
        "box": (0.28, 0.04, 0.72, 0.96),
        "pct": 0.06,
        "gamma": 0.86,
        "lift": 6.0,
        "color": 1.14,
        "contrast": 1.10,
    },
    {
        # 13.59-16.31 s: "Most stars look fixed for a lifetime." (pause 15.96-16.66 s)
        "row": "s05_startrails",
        "in": 13.59,
        "out": 16.31,
        "kind": "video",
        "src": "eso_startrails.mp4",
        "offset": 6.00,
        "crop_box": (608, 1080, 656, 0),
    },
    {
        # 16.31-18.71 s: "This one will creep across the sky" (pause 18.52-18.90 s)
        # Single teach overlay: "1 MOON WIDTH / 35 YRS" (16.51-18.55 s) inside 16:9 centre band
        "row": "s06_r31_sky_creep",
        "in": 16.31,
        "out": 18.71,
        "kind": "code",
        "src": "code_graphic_028_lift_r31_sky_creep.mp4",
        "mode": "r31_sky_creep",
        "t_offset": 2.0,
        "band_label": (0.20, 2.24, "1 MOON WIDTH / 35 YRS"),
    },
    {
        # 18.71-22.20 s: "by about the width of the full Moon every thirty-five years." (ends 22.20 s)
        "row": "s07_moon_lro",
        "in": 18.71,
        "out": 22.20,
        "kind": "still",
        "src": "moon_lro.jpg",
        "box": (0.16, 0.06, 0.84, 0.94),
        "pct": 0.05,
        "gamma": 0.86,
        "lift": 6.0,
        "color": 1.08,
        "contrast": 1.12,
    },
    {
        # 22.20-24.50 s: 2.30 s end card on opening eso_mw_lasilla.mp4 plate so the end loops seamlessly back to frame 0
        "row": "s08_end_loop_mw",
        "in": 22.20,
        "out": 24.50,
        "kind": "video",
        "src": "eso_mw_lasilla.mp4",
        "offset": 12.00,
        "crop_box": (608, 1080, 1140, 0),
    },
]

SFX_HITS = [
    ("whoosh", 0.00, -5.0),
    ("tick", 6.90, -4.0),
    ("tick", 9.00, -4.0),
    ("tick", 16.51, -4.0),
    ("tick", 22.20, -4.0),
]

POOL_TITLES = {
    "eso_mw_lasilla.mp4": "ESO La Silla Milky Way night-sky timelapse by S. Brunier (eso_mw_lasilla.mp4)",
    "wise_sky.jpg": "NASA/JPL-Caltech/UCLA WISE infrared night-sky starfield photograph (wise_sky.jpg)",
    "jupiter_juno.tif": "NASA/JPL-Caltech/SwRI/MSSS Juno colour-enhanced photograph of Jupiter (PIA21974 / jupiter_juno.tif)",
    "eso_startrails.mp4": "ESO La Silla Observatory night-sky star-trails timelapse by R. Wesson (eso_startrails.mp4)",
    "moon_lro.jpg": "NASA/GSFC/Arizona State University Lunar Reconnaissance Orbiter full-Moon photograph (moon_lro.jpg)",
}


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    words, _ = map_words_for_slices(VO_SLICES)
    if not (55 <= len(words) <= 65):
        raise SystemExit(f"word count {len(words)} outside 55-65")
    (WORK / "words.json").write_text(json.dumps(words, indent=2) + "\n")
    caps = build_caption_chunks(words, LAST_WORD_S)

    # Audit that no cut clips a spoken word
    clipped_words = []
    for p in PLATES:
        for bt in (p["in"], p["out"]):
            if bt <= 0.05 or bt >= LAST_WORD_S - 0.02:
                continue
            bad = [w for w in words if w["s"] < bt - 0.02 and w["e"] > bt + 0.02]
            if bad:
                clipped_words.append({"cut_s": bt, "row": p["row"], "words": bad})
    if clipped_words:
        raise SystemExit(f"cut clips word: {clipped_words}")

    hook_info = make_hook_png(WORK / "hook.png", HOOK_ROWS)
    title_info = make_title_banner_png(WORK / "title.png")
    end_info = make_end_card_png(WORK / "end_card.png")
    for i, c in enumerate(caps):
        c["bbox"] = make_caption_png(WORK / f"cap_{i:02d}.png", c["text"])

    cover_path = OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover_jpg(cover_path, FILM / "08_Thumbnail" / "art_v01" / "gliese_art_B.png", (0.20, 0.02, 0.80, 0.98), COVER_ROWS)

    scr = SkyCodeRenderer(CDIR / "assets", HDIR / "moon_lro.jpg")
    concat_lines = []
    cuts_json = []
    pool_json = []
    seen_pool = set()
    code_labels_audit = []

    for i, p in enumerate(PLATES):
        piece = WORK / f"piece_{i:02d}.mp4"
        p_dur = round(p["out"] - p["in"], 3)
        if p_dur > 6.01:
            raise SystemExit(f"{p['row']} duration {p_dur}s > 6.0s limit")
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
            up = render_video_9x16(
                HDIR / src_name,
                p["offset"],
                p_dur,
                piece,
                crop_box=p["crop_box"],
                open_push=p.get("open_push", 0.0),
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
            info = scr.render_clip(
                mode=p["mode"],
                dur_s=p_dur,
                dest=piece,
                t_offset=p.get("t_offset", 0.0),
                band_label=p.get("band_label"),
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

    span_list = WORK / "span_list.txt"
    span_list.write_text("\n".join(concat_lines) + "\n")
    pic_span = WORK / "picture_span.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(span_list), "-c", "copy", str(pic_span)])

    aud_info = build_short_audio(WORK, VO_SLICES, TOTAL_S, SFX_HITS)

    final_mp4 = OUT / f"{STEM}.mp4"
    inputs = [
        "-t",
        f"{TOTAL_S:.3f}",
        "-i",
        str(pic_span),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{TOTAL_S:.3f}",
        "-i",
        str(WORK / "hook.png"),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{TOTAL_S:.3f}",
        "-i",
        str(WORK / "title.png"),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{TOTAL_S:.3f}",
        "-i",
        str(WORK / "end_card.png"),
        "-i",
        str(WORK / "mix.wav"),
    ]
    base_idx = 5
    for i in range(len(caps)):
        inputs += [
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-t",
            f"{TOTAL_S:.3f}",
            "-i",
            str(WORK / f"cap_{i:02d}.png"),
        ]

    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={TITLE_OUT - 0.30:.2f}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={END_CARD_IN:.2f}:d=0.28:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{END_CARD_IN})*lte(t,{TOTAL_S})'[v3]",
    ]
    last_v = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base_idx + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
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
            f"{TOTAL_S:.3f}",
            str(final_mp4),
        ]
    )

    phone_mp4 = OUT / f"{STEM}_PHONE.mp4"
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

    contact_path = OUT / f"{STEM}_contact.jpg"
    make_contact_sheet(final_mp4, contact_path)

    cuts_path = OUT / f"{STEM}_cuts.json"
    pool_path = OUT / f"{STEM}_pool.json"
    cuts_path.write_text(json.dumps(cuts_json, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_json, indent=2) + "\n")

    gate_json_p = OUT / f"{STEM}_gate.json"
    gate_txt_p = OUT / f"{STEM}_gate.txt"
    gate_j = sp.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check",
            str(final_mp4),
            "--air-date",
            AIR_DATE,
            "--sheet-dir",
            str(OUT),
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
            AIR_DATE,
            "--sheet-dir",
            str(OUT),
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
            str(WORK / "stem_vo.wav"),
            "--sfx",
            str(WORK / "stem_sfx.wav"),
            "--bed",
            str(WORK / "stem_bed.wav"),
            "--minutes",
            f"{TOTAL_S / 60.0:.3f}",
        ],
        capture_output=True,
        text=True,
    )
    sfx_txt_p = OUT / f"{STEM}_sfx.txt"
    sfx_txt_p.write_text((sfx_chk.stdout or "") + (sfx_chk.stderr or ""))

    pg_json_p = OUT / f"{STEM}_polish_gate.json"
    pg_txt_p = OUT / f"{STEM}_polish_gate.txt"
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

    pqa_dir = OUT / f"{STEM}_picture_qa"
    pqa_txt_p = OUT / f"{STEM}_picture_qa.txt"
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

    cover_prev_p = OUT / f"{STEM}_cover_preview.jpg"
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

    gate_data = json.loads(gate_json_p.read_text())[0]
    meta = {
        "job": "J0897",
        "slug": "lift_night_sky_35yr",
        "stem": STEM,
        "air_date": AIR_DATE,
        "title": SHORT_TITLE,
        "long": {"id": LONG_ID, "title": LONG_TITLE, "master": "028_Gliese710_full_master_v03.mp4"},
        "file": str(final_mp4.relative_to(REPO)),
        "phone_file": str(phone_mp4.relative_to(REPO)),
        "sha256": sha256(final_mp4),
        "phone_sha256": sha256(phone_mp4),
        "duration_s": round(dur(final_mp4), 2),
        "vo_slices_master_s": VO_SLICES,
        "last_word_s": LAST_WORD_S,
        "vo_tail_s": VO_TAIL_S,
        "end_card_window_s": [END_CARD_IN, TOTAL_S],
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
        },
        "spend": "£0 (0 credits)",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    try:
        if UAT_ROOT.exists():
            for p_top in (final_mp4, phone_mp4):
                dst_top = UAT_ROOT / p_top.name
                if dst_top.exists():
                    dst_top.unlink()
                shutil.copy2(p_top, dst_top)
            uat_sub = UAT_ROOT / STEM
            uat_sub.mkdir(parents=True, exist_ok=True)
            for p in (final_mp4, phone_mp4, contact_path, cover_path, cover_prev_p, OUT / f"{STEM}_open_sheet.jpg", OUT / f"{STEM}_meta.json"):
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

    print(json.dumps(meta["gates"], indent=2))
    print(gate_t.stdout)
    print(sfx_chk.stdout)
    print(pg_chk.stdout)
    print(pqa_chk.stdout)
    print(cover_score_txt)

    if any(v != "PASS" for k, v in meta["gates"].items() if k not in ("gate_shorts_open_warns", "gate_shorts_open_motion_0_1s", "gate_shorts_open_visor_frac")):
        raise SystemExit("One or more gates failed")
    if meta["gates"]["gate_shorts_open_warns"]:
        print("WARNS:", meta["gates"]["gate_shorts_open_warns"])

    if WORK.exists():
        shutil.rmtree(WORK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
