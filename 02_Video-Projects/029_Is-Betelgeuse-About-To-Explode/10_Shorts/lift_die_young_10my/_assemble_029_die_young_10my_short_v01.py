#!/usr/bin/env python3
"""029 Short v01 — Betelgeuse Dying Young at 10 Million Years Old (`J0979`).

Lifts one self-contained 22.40 s stretch (61 spoken words) from the locked 029 long
(`029_Is-Betelgeuse-About-To-Explode` — *"Is Betelgeuse About to Explode?"*, `vP1BbqZ_dnM`),
Chapter 1 (`67.64–91.92 s`):
  > "Betelgeuse is only about ten million years old, and it is already near the end of
  > its life. Why so fast? Because it is heavy. With somewhere around fifteen to twenty
  > times the sun's mass, it burns its fuel ferociously. It gives out around a hundred
  > thousand times as much light as the sun. Big stars live fast and die young."

- Spoken words: 61 (inside 55–65 word band), VO ends at `20.96 s`.
- Runtime: `22.40 s` (`20.96 s` VO + `1.44 s` loop tail `<= 1.50 s`).
- Air date: `2026-12-18` (first free OWB Short weekday 11:30 London after 028/029 slots through Wed 16 Dec).
- Frame 0: native 9:16 supergiant scale graphic (`code_graphic_029_lift_r01_scale.mp4`),
  with Betelgeuse expanding past Earth and Mars orbits (`motion_0_1s >= 15`, `visor_frac = 0.0000`,
  distinct from all Shorts in the ±14-day / last-10 window).
- Hook caption (frame 0, `0.00–2.20 s`): `10 MILLION` (white) / `YEARS OLD` (yellow `#FFE000`).
- Exact long title at `9.00–14.00 s`: `Is Betelgeuse / About to / Explode?`.
- Teach on screen (`14.40–17.60 s`, inside 16:9 band): `100,000x THE SUN` on native 9:16 luminosity graphic.
- Timeline/mass call-out (`7.45–8.92 s`, out before 9.0 s banner): `BETELGEUSE` / `15-20x the Sun's mass`.
- End card (`20.96–22.40 s` inside the `1.44 s` reversed-open loop tail):
  `Is Betelgeuse / About to / Explode?` + yellow `Full film on the channel` (zero YouTube IDs on screen).
- Audio: existing VO + existing score bed `betelgeuse_score_bed_v01.mp3` + house SFX kit (`kit_v01`),
  integrated `-14.0 ± 0.5 LUFS`, true peak `<= -1.6 dBTP`.
- Spend: £0 (0 credits). Never upload.
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
HDIR = EDIT / "harvest_v01"
CDIR = EDIT / "code_graphics_v01"
VO_WAV = FILM / "02_Voiceover" / "betelgeuse_vo_v01.wav"
BED_MP3 = FILM / "05_Music" / "betelgeuse_score_bed_v01.mp3"
KIT_DIR = FILM / "06_Sound-Effects" / "kit_v01"
WORDS_JSON = EDIT / "full_rough_v03b_pack" / "betelgeuse_words_list.json"
REV_OK_LONG = EDIT / "full_rough_v03b_pack" / "reviewed_ok_v03b.json"

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/betelgeuse029_die_young_work_v01")
UAT_ROOT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR_NAME = "029_short_lift_die_young_10my_v01"
NAS_UAT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / UAT_DIR_NAME
NAS_STAGE = Path("/Volumes/data/mac-mini-archive/youtube-staging/029/lift_die_young_10my_v01")

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
ORANGE = (255, 148, 62)

STEM = "029_short_lift_die_young_10my_v01"
SHORT_SLUG = "lift_die_young_10my"
SHORT_TITLE = "Why Is Betelgeuse Already Dying at Just 10 Million Years Old?"
AIR_DATE = "2026-12-18"
LONG_ID = "vP1BbqZ_dnM"
LONG_TITLE = "Is Betelgeuse About to Explode?"
TITLE_ROWS = [
    "Is Betelgeuse",
    "About to",
    "Explode?",
]
END_CARD_LINE = "Full film on the channel"
END_ROWS = [
    ("Is Betelgeuse", WHITE),
    ("About to", WHITE),
    ("Explode?", WHITE),
    (END_CARD_LINE, YELLOW),
]
HOOK_ROWS = [("10 MILLION", WHITE), ("YEARS OLD", YELLOW)]
COVER_ROWS = [("DYING AT", WHITE), ("10M YEARS?", YELLOW)]

HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
CALL_IN, CALL_OUT = 7.45, 8.92
CALL_ROWS = [("BETELGEUSE", (255, 214, 64, 255)), ("15-20x the Sun's mass", WHITE)]

# Master VO segments from Chapter 1 (67.62-91.94 s) with tightened pauses (<=0.22 s)
VO_SEGMENTS = [
    (67.62, 70.48),  # "Betelgeuse is only about ten million years old,"
    (70.84, 72.86),  # "and it is already near the end of its life."
    (73.84, 74.82),  # "Why so fast?"
    (75.52, 76.56),  # "Because it is heavy."
    (77.40, 81.14),  # "With somewhere around fifteen to twenty times the sun's mass,"
    (81.54, 83.62),  # "it burns its fuel ferociously."
    (84.28, 88.38),  # "It gives out around a hundred thousand times as much light as the sun."
    (89.20, 91.94),  # "Big stars live fast and die young."
]
VO_LEAD_S = 0.08
VO_GAPS = [0.12, 0.20, 0.18, 0.22, 0.16, 0.22, 0.22]
LAST_WORD_S = 20.94
VO_END_S = 20.96
END_CARD_LEN = 1.44
TOTAL_S = 22.40  # 20.96 s + 1.44 s loop tail (<= 1.50 s) = 22.40 s (inside 22.0-27.0 s)
END_CARD_IN = round(TOTAL_S - END_CARD_LEN, 2)  # 20.96 s

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
    stroke_fill = (20, 32, 56, alpha)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


class BetelgeuseCodeRenderer:
    """Renders 029's Chapter 1 scale and luminosity teaching graphics natively at 1080x1920 (9:16) inside the 16:9 centre band."""

    def __init__(self, assets_dir: Path, harvest_dir: Path):
        self.sun = Image.open(assets_dir / "sun_sdo.jpg").convert("RGB").crop((448, 212, 3648, 3412))
        self.earth = Image.open(assets_dir / "earth.jpg").convert("RGB")
        self.mars = Image.open(assets_dir / "mars.jpg").convert("RGB")
        self.sphere = Image.open(harvest_dir / "sphere_jan.jpg").convert("RGB").crop((275, 295, 555, 565))
        self.rng = np.random.default_rng(1029)
        self.stars = self.rng.uniform([45, 85], [1035, 1835], (150, 2))
        self.belt = np.stack([
            self.rng.uniform(2.05, 2.75, 220),
            self.rng.uniform(0, 2 * math.pi, 220),
        ], axis=1)

        # Build a scrolling 1560x2400 cosmic nebula + coordinate-grid backdrop from jwst_pillars.jpg
        # mapped into cool cosmic blue-silver (B >= 56 everywhere so visor_frac == 0.0000 and near-black == 0%)
        BW, BH = 1560, 2400
        neb = Image.open(harvest_dir / "jwst_pillars.jpg").convert("RGB")
        neb = ImageOps.fit(neb, (BW, BH), method=Image.Resampling.LANCZOS)
        n_arr = np.asarray(neb, dtype=np.float32) / 255.0
        lum = 0.25 * n_arr[:, :, 0] + 0.50 * n_arr[:, :, 1] + 0.25 * n_arr[:, :, 2]
        lum = np.clip((lum ** 0.78) * 1.35, 0.0, 1.35)
        # Cool sapphire-indigo palette (S <= 0.48, V >= 0.22 everywhere)
        r_ch = 32.0 + 118.0 * (lum ** 1.15)
        g_ch = 50.0 + 138.0 * lum
        b_ch = 78.0 + 152.0 * (lum ** 0.90)
        bg_big = Image.fromarray(np.uint8(np.clip(np.stack([r_ch, g_ch, b_ch], axis=-1), 54, 255)))
        bd = ImageDraw.Draw(bg_big)
        srng = np.random.default_rng(2910)
        for n_stars, r_px, col in [(650, 2.5, (215, 232, 252)), (260, 3.8, (235, 244, 255)), (90, 5.2, (255, 248, 225))]:
            for sx, sy in srng.uniform([20, 20], [BW - 20, BH - 20], (n_stars, 2)):
                bd.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=col)
        self.bg_big = bg_big
        self.bodies: dict = {}

    def body(self, im: Image.Image, xy: tuple[float, float], r: float, kind: str = "sun") -> None:
        r_i = max(4, int(round(r)))
        key = (r_i, kind)
        if key not in self.bodies:
            src = {"earth": self.earth, "mars": self.mars, "betelgeuse": self.sphere}.get(kind, self.sun)
            b_im = ImageOps.fit(src, (2 * r_i, 2 * r_i), method=Image.Resampling.LANCZOS)
            arr = np.asarray(b_im, dtype=np.float32)
            # Lift dark shadow pixels to navy (26, 38, 62) so max(R,G,B) >= 52 (V >= 0.204 > 0.18)
            mx = arr.max(axis=2, keepdims=True)
            navy = np.array([26.0, 38.0, 62.0], dtype=np.float32)
            arr = np.where(mx < 54.0, np.maximum(arr, navy), arr)
            b_im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
            mask = Image.new("L", (2 * r_i, 2 * r_i))
            ImageDraw.Draw(mask).ellipse((1, 1, 2 * r_i - 2, 2 * r_i - 2), fill=255)
            b_im.putalpha(mask)
            self.bodies[key] = b_im
        im.paste(self.bodies[key], (int(round(xy[0] - r_i)), int(round(xy[1] - r_i))), self.bodies[key])

    def base(self, t: float, speed_px: float = 28.0) -> Image.Image:
        bw, bh = self.bg_big.size
        ox = int(round(t * speed_px * 3.8)) % max(1, bw - W)
        oy = int(round(t * speed_px * 3.0)) % max(1, bh - H)
        im = self.bg_big.crop((ox, oy, ox + W, oy + H)).copy()
        d = ImageDraw.Draw(im)
        shift_x = int(t * speed_px * 2.2) % 90
        shift_y = int(t * speed_px * 1.6) % 90
        for x in range(-90, W + 90, 90):
            d.line((x + shift_x, 120, x + shift_x, H - 120), fill=(68, 96, 134), width=1)
        for y in range(120, H - 119, 90):
            d.line((48, y + shift_y, W - 48, y + shift_y), fill=(68, 96, 134), width=1)
        return im

    def draw_band_label(
        self,
        im: Image.Image,
        text: str,
        xy: tuple[float, float],
        size: int = 42,
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
            stroke_fill=(20, 32, 56, int(235 * alpha)),
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
            im = self.base(t, speed_px=34.0 if mode == "r01_scale_open" else 22.0)
            d = ImageDraw.Draw(im)

            if mode == "r01_scale_open":
                # Frame 0 open strictly inside the 16:9 centre band (y=656..1264), clear of the hook caption:
                # Real SDO Sun on the left (x=175, y=960), real Earth (r=135) and Mars (r=255) on their orbit arcs,
                # and real ESO VLT SPHERE Betelgeuse on the right (x=835, y=960) expanding leftward across Mars & Earth orbits.
                sx, sy = 175.0, 960.0
                for r_orb, col, w_px in ((135, ICE, 3), (255, (195, 222, 255), 3), (380, (165, 195, 230), 2)):
                    d.arc((sx - r_orb, sy - r_orb, sx + r_orb, sy + r_orb), start=-62, end=62, fill=col, width=w_px)

                bx, by = 835.0, 960.0
                r_bet = 215.0 + 185.0 * (lt / max(0.001, dur_s))

                glow_layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
                gd = ImageDraw.Draw(glow_layer)
                r_halo = r_bet + 55.0
                gd.ellipse((bx - r_halo, by - r_halo, bx + r_halo, by + r_halo), fill=(255, 165, 85, 95))
                # Expanding stellar wind / shock-wave arcs sweeping leftward across the 16:9 band (motion >= 12)
                for k_wave in range(6):
                    rw = ((lt * 460.0 + k_wave * 95.0) % 580.0) + 120.0
                    gd.arc(
                        (bx - rw, by - rw * 0.62, bx + rw, by + rw * 0.62),
                        start=122,
                        end=238,
                        fill=(255, 226, 155, 215),
                        width=8,
                    )
                im.paste(Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB"))
                d = ImageDraw.Draw(im)

                # Real VLT SPHERE Betelgeuse supergiant body expanding in the 16:9 band
                self.body(im, (bx, by), r_bet, kind="betelgeuse")
                d.ellipse((bx - r_bet, by - r_bet, bx + r_bet, by + r_bet), outline=GOLD, width=4)

                # Real Sun, Blue Marble Earth, and Mars on left
                ang_e = -0.32 + lt * 0.85
                ang_m = 0.28 - lt * 0.65
                self.body(im, (sx, sy), 26, kind="sun")
                self.body(im, (sx + 135 * math.cos(ang_e), sy + 135 * math.sin(ang_e)), 18, kind="earth")
                self.body(im, (sx + 255 * math.cos(ang_m), sy + 255 * math.sin(ang_m)), 15, kind="mars")

                self.draw_band_label(im, "Sun & Mars Orbit", (265, BAND_Y1 - 46), size=36, color=ICE)
                self.draw_band_label(im, "Betelgeuse", (760, BAND_Y1 - 46), size=42, color=GOLD)

            elif mode == "r06_luminosity_100k":
                # 14.02-18.00 s: "It gives out around a hundred thousand times as much light as the sun."
                # Sun on left vs blazing Betelgeuse on right with animated light-wave rings + scale bar
                sx, bx, cy = 235.0, 745.0, 965.0
                self.body(im, (sx, cy), 34, kind="sun")

                # Expanding concentric light rings from Betelgeuse
                glow_layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
                gd = ImageDraw.Draw(glow_layer)
                prog = ease(min(1.0, u * 1.15))
                r_halo = int(115 + 75 * prog + 10 * math.sin(lt * 5.0))
                gd.ellipse((bx - r_halo, cy - r_halo, bx + r_halo, cy + r_halo), fill=(255, 200, 115, 95))
                for k_ring in range(4):
                    rr = 65.0 + ((lt * 165.0 + k_ring * 62.0) % 245.0)
                    ra = int(210 * (1.0 - (rr - 65.0) / 245.0))
                    gd.ellipse((bx - rr, cy - rr, bx + rr, cy + rr), outline=(255, 230, 150, ra), width=4)
                im.paste(Image.alpha_composite(im.convert("RGBA"), glow_layer).convert("RGB"))
                d = ImageDraw.Draw(im)

                self.body(im, (bx, cy), 84, kind="betelgeuse")
                # Animated comparison bar inside lower 16:9 band
                bar_y = BAND_Y1 - 115
                bar_x0, bar_x1 = 160, 920
                d.rounded_rectangle((bar_x0, bar_y - 16, bar_x1, bar_y + 16), radius=12, fill=(28, 44, 70), outline=ICE, width=2)
                fill_w = int((bar_x1 - bar_x0) * prog)
                if fill_w > 12:
                    d.rounded_rectangle((bar_x0, bar_y - 16, bar_x0 + fill_w, bar_y + 16), radius=12, fill=GOLD)

                self.draw_band_label(im, "Sun (1x)", (sx, cy + 84), size=38, color=WHITE[:3])
                self.draw_band_label(im, "Betelgeuse", (bx, cy + 112), size=40, color=GOLD)

            else:
                raise ValueError(f"Unknown mode: {mode}")

            if band_label is not None:
                l_in, l_out, l_txt = band_label
                if l_in <= lt <= l_out:
                    alpha = min(ease((lt - l_in) / 0.35), ease((l_out - lt) / 0.35))
                    bb = self.draw_band_label(
                        im,
                        l_txt,
                        (540, BAND_Y0 + 64 + int(10 * (1.0 - alpha))),
                        size=50,
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
    pct: float = 0.05,
    gamma: float = 0.85,
    lift: float = 6.0,
    color: float = 1.12,
    contrast: float = 1.10,
    shimmer: bool = False,
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
        arr = np.clip((arr ** gamma) * 255.0 + lift, 0.0, 255.0)
        mx = arr.max(axis=2, keepdims=True)
        navy = np.array([26.0, 38.0, 64.0], dtype=np.float32)
        arr = np.where(mx < 48.0, np.maximum(arr, navy), arr).astype(np.uint8)
        im = Image.fromarray(arr)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = im.filter(ImageFilter.UnsharpMask(radius=2.0, percent=135, threshold=2))

    # Cap sharp upscale at 1.90x (well under picture_qa 2.00x WARN / 2.35x FAIL),
    # and fill any top/bottom margin with a feathered Gaussian blur of the same crop.
    max_up = 1.90
    cover = max(W / im.width, H / im.height)
    fit = min(cover, max_up)
    sharp = im.resize((max(2, round(im.width * fit)), max(2, round(im.height * fit))), Image.Resampling.LANCZOS)
    if sharp.width >= W - 2 and sharp.height >= H - 2:
        sx = (sharp.width - W) // 2
        sy = (sharp.height - H) // 2
        base_frame = sharp.crop((sx, sy, sx + W, sy + H))
    else:
        bg = im.resize((max(W + 4, round(im.width * cover)), max(H + 4, round(im.height * cover))), Image.Resampling.BILINEAR)
        bg = bg.filter(ImageFilter.GaussianBlur(32))
        bx, by = (bg.width - W) // 2, (bg.height - H) // 2
        base_arr = np.asarray(bg.crop((bx, by, bx + W, by + H)), dtype=np.float32)
        px = (W - sharp.width) // 2
        py = (H - sharp.height) // 2
        sx0, sy0 = max(0, -px), max(0, -py)
        dx0, dy0 = max(0, px), max(0, py)
        sub_w = min(sharp.width - sx0, W - dx0)
        sub_h = min(sharp.height - sy0, H - dy0)
        src_arr = np.asarray(sharp, dtype=np.float32)
        fg = np.zeros_like(base_arr)
        al = np.zeros((H, W), dtype=np.float32)
        fg[dy0:dy0 + sub_h, dx0:dx0 + sub_w] = src_arr[sy0:sy0 + sub_h, sx0:sx0 + sub_w]
        al[dy0:dy0 + sub_h, dx0:dx0 + sub_w] = 1.0
        fade = min(80, sub_h // 3, sub_w // 3)
        if fade > 4:
            ramp = np.linspace(0, 1, fade, dtype=np.float32)
            if dy0 > 0:
                al[dy0:dy0 + fade, dx0:dx0 + sub_w] *= ramp[:, None]
            if dy0 + sub_h < H:
                al[dy0 + sub_h - fade:dy0 + sub_h, dx0:dx0 + sub_w] *= ramp[::-1, None]
            if dx0 > 0:
                al[dy0:dy0 + sub_h, dx0:dx0 + fade] *= ramp[None, :]
            if dx0 + sub_w < W:
                al[dy0:dy0 + sub_h, dx0 + sub_w - fade:dx0 + sub_w] *= ramp[::-1][None, :]
        out_arr = base_arr * (1.0 - al[..., None]) + fg * al[..., None]
        base_frame = Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8))

    room = 1.0 if pct <= 0.0 else 1.04
    big = base_frame.resize((round(W * room), round(H * room)), Image.Resampling.BICUBIC)
    bw, bh = big.size

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
    yy, xx = np.mgrid[:H, :W]
    for n in range(frames):
        t_u = n / max(1, frames - 1)
        drift = 0.0 if pct <= 0.0 else (t_u - 0.5) * 0.02
        cx = (bw - W) / 2.0 + drift * bw
        cy = (bh - H) / 2.0
        cx = min(max(0.0, cx), bw - W)
        cy = min(max(0.0, cy), bh - H)
        frame = base_frame if pct <= 0.0 else big.resize((W, H), Image.Resampling.BICUBIC, box=(cx, cy, cx + W, cy + H))
        if shimmer:
            arr_f = np.asarray(frame, dtype=np.float32)
            bright = np.array([110.0, 48.0, 12.0], dtype=np.float32)
            for k_s in range(5):
                cxp = ((n * 22 + k_s * 210) % (W + 180)) - 90
                cyp = 640 + (k_s % 4) * 160
                blob = np.exp(-(((xx - cxp) / 55.0) ** 2 + ((yy - cyp) / 90.0) ** 2))
                arr_f += blob[..., None] * bright
            frame = Image.fromarray(np.clip(arr_f, 0, 255).astype(np.uint8))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"render_still_9x16 failed: {dest}")
    return round(fit * room, 3)


def render_video_9x16(
    src: Path,
    offset_s: float,
    dur_s: float,
    dest: Path,
    crop_box: tuple[int, int, int, int] = (608, 1080, 656, 0),
    grade: dict | None = None,
) -> float:
    cw, ch, cx, cy = crop_box
    upscale = round(max(W / cw, H / ch), 3)
    g = grade or {}
    contrast = g.get("contrast", 1.20)
    brightness = g.get("brightness", 0.05)
    gamma = g.get("gamma", 0.76)
    saturation = g.get("saturation", 1.22)
    floor = g["floor"] if "floor" in g else (24, 36, 58)
    eq = f"eq=contrast={contrast}:brightness={brightness}:gamma={gamma}:saturation={saturation},"
    lut = ""
    if floor:
        fr, fg, fb = floor
        lut = f"lutrgb=r='max(val,{fr})':g='max(val,{fg})':b='max(val,{fb})',"
    vf = (
        f"fps={FPS},crop={cw}:{ch}:{cx}:{cy},"
        f"{eq}"
        f"unsharp=5:5:1.4:5:5:0.0,"
        f"{lut}"
        f"scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p"
    )
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


def render_loop_from_open(open_piece: Path, dur_s: float, dest: Path) -> None:
    """Play the opening backwards so the tail lands on frame 0."""
    n = round(dur_s * FPS)
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(open_piece),
            "-vf",
            f"fps={FPS},trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,reverse,format=yuv420p",
            "-an",
            "-frames:v",
            str(n),
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


def make_callout_card_png(dest: Path) -> dict:
    """Mass call-out card on s03 (`7.45–8.92 s`), out before the 9.0 s banner."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sizes = [54, 42]
    fonts = []
    for text, _col, size in ((CALL_ROWS[0][0], CALL_ROWS[0][1], sizes[0]), (CALL_ROWS[1][0], CALL_ROWS[1][1], sizes[1])):
        f = ImageFont.truetype(FONT_BLACK, size)
        while d.textlength(text, font=f) > W * 0.86 and f.size > 28:
            f = ImageFont.truetype(FONT_BLACK, f.size - 2)
        fonts.append(f)
    gap = d.textbbox((0, 0), "Hg", font=fonts[0])[3] + 10
    y = BAND_Y0 + 36
    placed = []
    for (text, col), f in zip(CALL_ROWS, fonts):
        bb = centred(d, y, text, f, col, stroke=6)
        if bb[3] > BAND_Y1 - 80:
            raise SystemExit(f"Call-out hits the caption zone: {text} {bb}")
        placed.append({"text": text, "bbox": bb, "font_px": f.size})
        y += gap
    im.save(dest)
    return {"rows": placed, "window_s": [CALL_IN, CALL_OUT]}


def measure_aac(path: Path) -> dict:
    p = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    integrated = peak = None
    for ln in p.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            integrated = float(ln.split("I:")[1].split("LUFS")[0].strip())
        if "Peak:" in ln and "dBFS" in ln:
            peak = float(ln.split("Peak:")[1].split("dBFS")[0].strip())
    if integrated is None or peak is None:
        raise SystemExit(f"Could not read ebur128 stats for {path}")
    return {"lufs": round(integrated, 2), "true_peak_dbtp": round(peak, 2)}


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
    return {"font_px": f.size, "rows": placed, "long_title": LONG_TITLE, "yellow": END_CARD_LINE}


def map_words_for_segments(segments: list[tuple[float, float]], lead_s: float, gaps: list[float]) -> tuple[list[dict], list[dict], float]:
    slices = []
    mapped = []
    local = lead_s
    for i, (s_in, s_out) in enumerate(segments):
        seg_dur = s_out - s_in
        slices.append({"a": s_in, "b": s_out, "local": round(local, 3)})
        for w in ALL_WORDS:
            if w["end"] <= s_in + 0.01 or w["start"] >= s_out - 0.01:
                continue
            ws = max(0.0, w["start"] - s_in) + local
            we = min(seg_dur, w["end"] - s_in) + local
            mapped.append({
                "w": w["text"],
                "word": w["text"],
                "s": round(ws, 3),
                "e": round(we, 3),
                "start": round(ws, 3),
                "end": round(we, 3),
            })
        local = round(local + seg_dur, 3)
        if i < len(gaps):
            local = round(local + gaps[i], 3)
    return slices, mapped, local


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
    im = ImageEnhance.Contrast(im).enhance(1.14)
    arr = np.asarray(im, dtype=np.float32)
    arr = np.clip(((arr / 255.0) ** 0.78) * 255.0 + 14.0, 0.0, 255.0)
    lum = 0.299 * arr[:, :, 0:1] + 0.587 * arr[:, :, 1:2] + 0.114 * arr[:, :, 2:3]
    dark_w = np.clip((42.0 - lum) / 42.0, 0.0, 1.0)
    floor_rgb = np.array([20.0, 38.0, 76.0], dtype=np.float32)[None, None, :]
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
    slices: list[dict],
    total_s: float,
    sfx_hits: list[tuple[str, float, float]],
) -> dict:
    vo_parts = []
    cursor = 0.0
    for i, sl in enumerate(slices):
        gap_samples = int(round((sl["local"] - cursor) * SR))
        if gap_samples > 0:
            vo_parts.append(np.zeros((gap_samples, 2), dtype=np.float32))
        s_in, s_out = sl["a"], sl["b"]
        seg_dur = s_out - s_in
        p = work / f"vo_part_{i}.wav"
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
        part_arr = read_wav(p)
        vo_parts.append(part_arr)
        cursor = sl["local"] + len(part_arr) / SR

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

    bed_start = slices[0]["a"]
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
            "loudnorm=I=-13.8:TP=-2.2:LRA=11,aresample=192000,alimiter=limit=0.7762:level=disabled:attack=1:release=50:latency=1,aresample=48000",
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
    times = [0.0, 0.5, 1.8, 4.2, 6.8, 10.2, 12.8, 15.8, 19.2, TOTAL_S - 0.6]
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
        # 0.00-2.96 s (2.96 s <= 3.00 s): "Betelgeuse is only about ten million years old,"
        # Frame 0: native 9:16 supergiant scale graphic expanding past Earth & Mars orbits
        "row": "s01_r01_scale_open",
        "in": 0.00,
        "out": 2.96,
        "kind": "code",
        "src": "code_graphic_029_lift_r01_scale.mp4",
        "mode": "r01_scale_open",
        "t_offset": 0.0,
        "band_label": None,
    },
    {
        # 2.96-5.18 s (2.22 s): "and it is already near the end of its life."
        "row": "s02_sphere_jan",
        "in": 2.96,
        "out": 5.18,
        "kind": "still",
        "src": "sphere_jan.jpg",
        "box": (0.06, 0.06, 0.94, 0.94),
        "pct": 0.0,
        "gamma": 0.82,
        "lift": 8.0,
        "color": 1.18,
        "contrast": 1.12,
        "shimmer": False,
    },
    {
        # 5.18-7.58 s (2.40 s): "Why so fast? Because it is heavy."
        # Bridges the 5.06-5.30 s sentence-1 seam (0.24 s < 0.25 s) on moving ESO La Silla Milky Way footage
        "row": "s03_lasilla_mw",
        "in": 5.18,
        "out": 7.58,
        "kind": "video",
        "src": "lasilla_mw.mp4",
        "offset": 1.20,
        "crop_box": (608, 1080, 500, 0),
        "grade": {
            "contrast": 1.25,
            "brightness": 0.12,
            "gamma": 1.40,
            "saturation": 1.30,
            "floor": (26, 38, 62),
        },
    },
    {
        # 7.58-11.52 s (3.94 s <= 4.00 s): "With somewhere around fifteen to twenty times the sun's mass,"
        # Carries call-out (7.45-8.92 s) then parent-title banner (9.00-14.00 s)
        "row": "s04_westerlund_cluster",
        "in": 7.58,
        "out": 11.52,
        "kind": "still",
        "src": "westerlund.jpg",
        "box": (0.22, 0.14, 0.78, 0.86),
        "pct": 0.05,
        "gamma": 0.84,
        "lift": 6.0,
        "color": 1.14,
        "contrast": 1.10,
    },
    {
        # 11.52-14.38 s (2.86 s): "it burns its fuel ferociously. It gives out"
        # Completes parent-title banner (9.00-14.00 s)
        "row": "s05_visir_plume",
        "in": 11.52,
        "out": 14.38,
        "kind": "still",
        "src": "visir_flames.jpg",
        "box": (0.12, 0.08, 0.88, 0.92),
        "pct": 0.06,
        "gamma": 0.82,
        "lift": 8.0,
        "color": 1.16,
        "contrast": 1.12,
    },
    {
        # 14.38-18.10 s (3.72 s <= 4.00 s): "around a hundred thousand times as much light as the sun."
        # Single Teach on screen overlay: "100,000x THE SUN" at 14.55-17.85 s inside 16:9 band
        "row": "s06_r06_luminosity",
        "in": 14.38,
        "out": 18.10,
        "kind": "code",
        "src": "code_graphic_029_lift_r06_luminosity.mp4",
        "mode": "r06_luminosity_100k",
        "t_offset": 0.0,
        "band_label": (0.17, 3.47, "100,000x THE SUN"),
    },
    {
        # 18.10-20.96 s (2.86 s): "Big stars live fast and die young." (Payoff at 80.8%-93.5% of runtime >= 70%)
        "row": "s07_tarantula_nursery",
        "in": 18.10,
        "out": 20.96,
        "kind": "still",
        "src": "tarantula.jpg",
        "box": (0.20, 0.08, 0.80, 0.92),
        "pct": 0.06,
        "gamma": 0.82,
        "lift": 8.0,
        "color": 1.16,
        "contrast": 1.12,
    },
    {
        # 20.96-22.40 s (1.44 s <= 1.50 s): reverse of the opening clip so the last frame is frame 0
        "row": "s08_end_loop_scale",
        "in": 20.96,
        "out": 22.40,
        "kind": "loop",
        "src": "code_graphic_029_lift_r01_scale_loop.mp4",
        "offset": 0.0,
    },
]

SFX_HITS = [
    ("whoosh", 0.00, -5.0),
    ("tick", 2.96, -4.5),
    ("tick", 9.00, -4.0),
    ("tick", 14.38, -4.0),
    ("tick", 20.96, -4.0),
]

POOL_TITLES = {
    "code_graphic_029_lift_r01_scale.mp4": "Our own 9:16 code graphic of Betelgeuse supergiant radius vs Earth and Mars orbits",
    "sphere_jan.jpg": "ESO VLT SPHERE resolved surface photograph of Betelgeuse in January 2019 (eso2003b)",
    "orion_over_paranal.mp4": "ESO Paranal Observatory time-lapse of Orion rising in the night sky (orion_over_paranal.mp4)",
    "lasilla_mw.mp4": "ESO La Silla Observatory time-lapse of the Milky Way rising in the night sky (lasilla_mw.mp4)",
    "westerlund.jpg": "NASA/ESA Hubble Space Telescope photograph of massive star cluster Westerlund 2 (heic1509a)",
    "visir_flames.jpg": "ESO VLT VISIR infrared photograph of Betelgeuse's circumstellar plume (eso1121a)",
    "code_graphic_029_lift_r06_luminosity.mp4": "Our own 9:16 code graphic comparing Betelgeuse luminosity (100,000x Sun) with the Sun",
    "tarantula.jpg": "ESO/NASA photograph of massive stars in the Tarantula Nebula (tarantula.jpg)",
    "code_graphic_029_lift_r01_scale_loop.mp4": "Our own 9:16 opening scale graphic reversed so the last frame matches frame 0",
}


def ocr_every_frame(final: Path, report: Path) -> dict:
    """Tesseract on every frame. Fail if a YouTube ID, file name or job tag is on screen."""
    frames = WORK / "ocr_jpg"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "fps=30,scale=540:960", str(frames / "%05d.jpg")])
    paths = sorted(frames.glob("*.jpg"))
    tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
    banned = ("vp1bbq", "bbqzdnm", "j0979", "j0944", "j0929", "dieyoung", "betelgeuse029")
    file_tag = re.compile(r"[a-z0-9_]{4,}\.(?:mp4|py|json|tif|wav|jpg)\b")

    def one(path: Path) -> tuple[str, str]:
        got = sp.run([tess, str(path), "stdout", "--psm", "6", "-l", "eng"], capture_output=True, text=True)
        return path.name, (got.stdout or "").replace("\n", " ").strip()

    from concurrent.futures import ThreadPoolExecutor

    hits: list[str] = []
    kept: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for name, said in pool.map(one, paths):
            if not said:
                continue
            kept.append(f"{name}\t{said}")
            norm = re.sub(r"[^a-z0-9.]", "", said.lower())
            if any(bit in norm for bit in banned) or file_tag.search(said.lower()):
                hits.append(f"{name}\t{said}")
    report.write_text(
        f"engine tesseract\nframes {len(paths)}\nhits {len(hits)}\n"
        + "\n".join(hits)
        + "\n---\n"
        + "\n".join(kept)
        + "\n"
    )
    shutil.rmtree(frames, ignore_errors=True)
    verdict = "PASS" if not hits and len(paths) >= 600 else "FAIL"
    return {"verdict": verdict, "frames": len(paths), "hits": len(hits)}


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    slices, words, last_s = map_words_for_segments(VO_SEGMENTS, VO_LEAD_S, VO_GAPS)
    print(f"mapped {len(words)} words, last word ends at {last_s:.3f}s")
    if not (55 <= len(words) <= 65):
        raise SystemExit(f"word count {len(words)} outside 55-65")
    (WORK / "words.json").write_text(json.dumps(words, indent=2) + "\n")
    (OUT / f"{STEM}_words.json").write_text(json.dumps(words, indent=2) + "\n")
    spoken_text = " ".join(w["w"] for w in words)
    (OUT / f"{STEM}_transcript.txt").write_text(spoken_text + "\n")
    caps = build_caption_chunks(words, last_s)

    # Audit that no cut clips a spoken word
    clipped_words = []
    for p in PLATES:
        for bt in (p["in"], p["out"]):
            if bt <= 0.05 or bt >= last_s - 0.02:
                continue
            bad = [w for w in words if w["s"] < bt - 0.02 and w["e"] > bt + 0.02]
            if bad:
                clipped_words.append({"cut_s": bt, "row": p["row"], "words": bad})
    if clipped_words:
        raise SystemExit(f"cut clips word: {clipped_words}")

    hook_info = make_hook_png(WORK / "hook.png", HOOK_ROWS)
    title_info = make_title_banner_png(WORK / "title.png")
    end_info = make_end_card_png(WORK / "end_card.png")
    call_info = make_callout_card_png(WORK / "callout_card.png")
    for i, c in enumerate(caps):
        c["bbox"] = make_caption_png(WORK / f"cap_{i:02d}.png", c["text"])

    cover_path = OUT / f"{STEM}_cover.jpg"
    cover_info = make_cover_jpg(cover_path, HDIR / "sphere_jan.jpg", (0.08, 0.08, 0.92, 0.92), COVER_ROWS)

    renderer = BetelgeuseCodeRenderer(CDIR / "assets", HDIR)
    concat_lines = []
    cuts_json = []
    pool_json = []
    seen_pool = set()
    code_labels_audit = []

    for i, p in enumerate(PLATES):
        piece = WORK / f"piece_{i:02d}.mp4"
        p_dur = round(p["out"] - p["in"], 3)
        if p_dur > 4.02:
            raise SystemExit(f"{p['row']} duration {p_dur}s > 4.0s limit")
        kind = p["kind"]
        src_name = p["src"]

        if kind == "still":
            animated = bool(p.get("shimmer"))
            up = render_still_9x16(
                HDIR / src_name,
                p_dur,
                piece,
                box=p["box"],
                pct=p.get("pct", 0.05),
                gamma=p.get("gamma", 0.84),
                lift=p.get("lift", 6.0),
                color=p.get("color", 1.14),
                contrast=p.get("contrast", 1.10),
                shimmer=animated,
            )
            cuts_json.append(
                {
                    "row": p["row"],
                    "timeline_in": p["in"],
                    "timeline_out": p["out"],
                    "source": src_name,
                    "upscale": up,
                    "framing": {"offset": 0.0} if animated else {"box": list(p["box"]), "pct": p.get("pct", 0.05)},
                    "video": animated,
                }
            )
        elif kind == "video":
            up = render_video_9x16(
                HDIR / src_name,
                p["offset"],
                p_dur,
                piece,
                crop_box=p["crop_box"],
                grade=p.get("grade"),
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
        elif kind == "loop":
            render_loop_from_open(WORK / "piece_00.mp4", p_dur, piece)
            open_raw = sp.check_output(
                ["ffmpeg", "-v", "error", "-i", str(WORK / "piece_00.mp4"), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
            )
            tail_raw = sp.check_output(
                ["ffmpeg", "-v", "error", "-sseof", "-0.04", "-i", str(piece), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
            )
            a = np.frombuffer(open_raw, dtype=np.uint8).astype(np.int16)
            b = np.frombuffer(tail_raw, dtype=np.uint8).astype(np.int16)
            loop_diff = float(np.abs(a - b).mean())
            print(f"loop last-frame vs frame 0 mean abs diff {loop_diff:.2f}")
            if loop_diff > 6.0:
                raise SystemExit(f"loop frame does not match frame 0 (diff {loop_diff:.2f})")
            cuts_json.append(
                {
                    "row": p["row"],
                    "timeline_in": p["in"],
                    "timeline_out": p["out"],
                    "source": src_name,
                    "upscale": 1.0,
                    "framing": {"offset": 0.0, "loop": "reverse opening so the last frame is frame 0"},
                    "video": True,
                }
            )
        elif kind == "code":
            info = renderer.render_clip(
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

    aud_info = build_short_audio(WORK, slices, TOTAL_S, SFX_HITS)

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
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-t",
        f"{TOTAL_S:.3f}",
        "-i",
        str(WORK / "callout_card.png"),
        "-i",
        str(WORK / "mix.wav"),
    ]
    base_idx = 6
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
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v3]",
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
            "5:a",
            *enc,
            "-t",
            f"{TOTAL_S:.3f}",
            str(final_mp4),
        ]
    )

    aac = measure_aac(final_mp4)
    print("aac", aac)
    if aac["true_peak_dbtp"] > -1.6 or not (-14.5 <= aac["lufs"] <= -13.5):
        fixed = WORK / "mix_relimit.wav"
        gain = -14.0 - aac["lufs"]
        gain = max(-1.5, min(1.5, gain))
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", str(WORK / "mix.wav"),
                "-af", f"volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.7762:level=disabled:attack=1:release=50:latency=1,aresample=48000",
                "-ar", str(SR), "-ac", "2", str(fixed),
            ]
        )
        remuxed = WORK / "final_relimit.mp4"
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", str(final_mp4), "-i", str(fixed),
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-ar", "48000", "-ac", "2", "-t", f"{TOTAL_S:.3f}", str(remuxed),
            ]
        )
        shutil.move(remuxed, final_mp4)
        aac = measure_aac(final_mp4)
        print("aac after relimit", aac)
        if aac["true_peak_dbtp"] > -1.6 or not (-14.5 <= aac["lufs"] <= -13.5):
            raise SystemExit(f"AAC level still outside the brief: {aac}")

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

    # Write initial sidecar so gate_shorts_open reads spoken text and last_word_end_s
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "spoken": spoken_text,
                "last_word_end_s": last_s,
                "words_file": str(OUT / f"{STEM}_words.json"),
            },
            indent=2,
        )
        + "\n"
    )

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
            "--vo",
            str(WORK / "stem_vo.wav"),
            "--meta",
            str(meta_path),
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
            "--vo",
            str(WORK / "stem_vo.wav"),
            "--meta",
            str(meta_path),
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

    music_json_p = OUT / f"{STEM}_music_gate.json"
    music_chk = sp.run(
        [
            sys.executable,
            str(REPO / "scripts/music_gate.py"),
            str(FILM),
            "--bed",
            str(BED_MP3),
            "--video",
            str(final_mp4),
            "--out",
            str(music_json_p),
        ],
        capture_output=True,
        text=True,
    )
    (OUT / f"{STEM}_music_gate.txt").write_text((music_chk.stdout or "") + (music_chk.stderr or ""))

    ocr_txt_p = OUT / f"{STEM}_ocr.txt"
    ocr = ocr_every_frame(final_mp4, ocr_txt_p)

    gate_data = json.loads(gate_json_p.read_text())[0]
    meta = {
        "job": "J0979",
        "slug": SHORT_SLUG,
        "stem": STEM,
        "air_date": AIR_DATE,
        "title": SHORT_TITLE,
        "long": {"id": LONG_ID, "title": LONG_TITLE, "master": "029_Betelgeuse_full_rough_v03b.mp4"},
        "file": str(final_mp4.relative_to(REPO)),
        "phone_file": str(phone_mp4.relative_to(REPO)),
        "sha256": sha256(final_mp4),
        "phone_sha256": sha256(phone_mp4),
        "duration_s": round(dur(final_mp4), 2),
        "spoken": spoken_text,
        "vo_segments_master_s": VO_SEGMENTS,
        "last_word_end_s": last_s,
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
        "callout": call_info,
        "aac": aac,
        "cover": {**cover_info, "score_output": cover_score_txt.strip()},
        "audio": aud_info,
        "brief": {
            "frame_0_source": "code_graphic_029_lift_r01_scale.mp4 (native 9:16 supergiant scale animation, moving at frame 0)",
            "first_word_s": words[0]["s"],
            "surprise_word_s": next(w["s"] for w in words if w["w"].lower() == "ten"),
            "first_cut_s": PLATES[0]["out"],
            "last_word_to_loop_s": round(TOTAL_S - last_s, 2),
            "meta_promise": False,
            "runtime_s": TOTAL_S,
            "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts_json), 2),
            "payoff_s": 17.76,
            "payoff_vs_70pct_s": round(0.70 * TOTAL_S, 2),
            "loop_sentence": "Big stars live fast and die young — Betelgeuse is only about ten million years old, and it is already near the end of its life.",
        },
        "gates": {
            "gate_shorts_open": gate_data["verdict"],
            "gate_shorts_open_warns": gate_data["warns"],
            "gate_shorts_open_motion_0_1s": gate_data["motion_0_1s"],
            "gate_shorts_open_frame0_diff": gate_data.get("frame0_diff_0_1_5s"),
            "gate_shorts_open_visor_frac": gate_data.get("orbit", {}).get("visor_frac", 0.0),
            "sfx_kit_level": "PASS" if sfx_chk.returncode == 0 else "FAIL",
            "polish_gate": "PASS" if pg_chk.returncode == 0 else "FAIL",
            "picture_qa": "PASS" if pqa_chk.returncode == 0 else "FAIL",
            "music_gate": "PASS" if music_chk.returncode == 0 else "FAIL",
            "ocr": ocr["verdict"],
            "cover_preview_score": "PASS" if cov_chk.returncode == 0 else "FAIL",
        },
        "ocr": ocr,
        "spend": "£0 (0 credits)",
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    sha_lines = [
        f"{meta['sha256']}  {final_mp4.name}",
        f"{meta['phone_sha256']}  {phone_mp4.name}",
    ]
    sha_txt = OUT / f"{STEM}_SHA256.txt"
    sha_txt.write_text("\n".join(sha_lines) + "\n")

    print(json.dumps(meta["gates"], indent=2))
    print(gate_t.stdout)
    print(sfx_chk.stdout)
    print(pg_chk.stdout)
    print(pqa_chk.stdout)
    print(cover_score_txt)

    if any(
        v != "PASS"
        for k, v in meta["gates"].items()
        if k
        not in (
            "gate_shorts_open_warns",
            "gate_shorts_open_motion_0_1s",
            "gate_shorts_open_frame0_diff",
            "gate_shorts_open_visor_frac",
        )
    ):
        raise SystemExit("One or more gates failed")
    if meta["gates"]["gate_shorts_open_warns"]:
        print("WARNS:", meta["gates"]["gate_shorts_open_warns"])

    ship = [
        final_mp4,
        phone_mp4,
        contact_path,
        cover_path,
        cover_prev_p,
        OUT / f"{STEM}_open_sheet.jpg",
        meta_path,
        sha_txt,
        ocr_txt_p,
    ]
    try:
        if UAT_ROOT.exists():
            uat_sub = UAT_ROOT / UAT_DIR_NAME
            uat_sub.mkdir(parents=True, exist_ok=True)
            for p in ship:
                if p.exists():
                    dst_sub = uat_sub / p.name
                    if dst_sub.exists():
                        dst_sub.unlink()
                    shutil.copy2(p, dst_sub)
                    if p in (final_mp4, phone_mp4) and sha256(dst_sub) != sha256(p):
                        raise SystemExit(f"UAT sha mismatch {p.name}")
            (uat_sub / "SHA256.txt").write_text(sha_txt.read_text())
    except OSError as exc:
        print(f"warn: UAT copy skipped: {exc}")

    for nas_target in (NAS_UAT, NAS_STAGE):
        try:
            if nas_target.parent.exists():
                nas_target.mkdir(parents=True, exist_ok=True)
                for p in ship:
                    if p.exists():
                        dst = nas_target / p.name
                        if dst.exists():
                            dst.unlink()
                        shutil.copy2(p, dst)
                        if p in (final_mp4, phone_mp4) and sha256(dst) != sha256(p):
                            raise SystemExit(f"NAS sha mismatch {p.name}")
                (nas_target / "SHA256.txt").write_text(sha_txt.read_text())
        except OSError as exc:
            print(f"warn: NAS copy skipped ({nas_target}): {exc}")

    if WORK.exists():
        shutil.rmtree(WORK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
