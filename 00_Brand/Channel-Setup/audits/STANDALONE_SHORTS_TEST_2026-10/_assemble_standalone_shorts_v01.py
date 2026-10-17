#!/usr/bin/env python3
"""Standalone story Shorts S1-S8 v01 (J0163, Ben 12 Oct 2026: ~20 s, not cut from a long).

Does not upload or schedule. Picture is NASA plates (plates_v01.json for S1-S4, plates_v02.json for S5-S8; S5-S8 VO
is pause-trimmed by _pause_trim_v02.py) and, on S4, ESA/Webb weic2310a (CC BY 4.0),
drawn frame by frame with a smooth sub-pixel push per row; hard cuts between rows, and the last ~3 s crossfade back
to the opening plate (pull-back ending on frame 0's framing) so each Short loops.
Audio: the pause-trimmed VO (vo_v01/trim), the one standalone-Shorts bed (05_Music, Chief 6131710376) and the house
SFX kit (whoosh or rumble at frame 0, one tick on the overlay). VO, bed and SFX stems are written for sfx_kit level.
The Orbit row at ~1 s is left open in the cut list (J0200); the opening plate runs under it until the insert lands.
Usage: _assemble_standalone_shorts_v01.py [s1 ... s8]
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

PLATES = Path("/private/tmp/owb_sa_shorts/plates")
KIT = Path("/private/tmp/owb_sa_shorts/sfx_kit_v01")
WORK = Path("/private/tmp/owb_sa_shorts/build_v01")
BED = HERE / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
TRIM = HERE / "vo_v01/trim"
TRIM2 = HERE / "vo_s5-s8_v01/trim"
OUT = HERE / "06_Final-Exports"

W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
BAND_TOP = (H - 608) // 2
LINE_H = int(608 * 0.115)
HOOK_END = 2.2
TITLE = (9.0, 14.0)
HOLD = 3.0
MAX_TOTAL = 27.4
LOOP_XFADE = 0.5
OPEN_PUSH_S = 1.0
OPEN_KICK = 0.15
VO_GAIN, BED_GAIN, BED_HOLD_GAIN = 1.0, 0.065, 0.35

# row: (start_s, plate, mode, cx, cy, zoom_from, zoom_to). mode "cover" fills 9:16; "fit" fits the width over a
# blurred, darkened copy of itself (feathered edges). Times are on the trimmed VO clock.
SHORTS = {
    "s1": {
        "stem": "owb_sa_s1_mercury", "id": "vlkj8RQKmH8", "vo": "owb_sa_s1_mercury_vo_v01", "air": "2026-10-20",
        "title": ("A Day on Mercury", "Lasts Two Years"), "hook": (("ONE", "DAY,"), ("TWO", "YEARS")), "yellow": "DAY,",
        "sfx0": "whoosh",
        "rows": [
            (0.0, "s1_mercury/PIA11351.jpg", "cover", 0.62, 0.42, 1.0, 1.04),
            (5.5, "s1_mercury/PIA14083.jpg", "cover", 0.55, 0.45, 1.05, 1.15),
            (9.7, "s1_mercury/PIA12266.jpg", "cover", 0.55, 0.62, 1.0, 1.10),
            (15.1, "s1_mercury/PIA13674.jpg", "cover", 0.20, 0.45, 1.25, 1.35),
        ],
        "overlay": {"kind": "fact", "lines": ("176", "EARTH DAYS"), "window": (14.0, 17.2),
                    "spoken": "sunrise to sunrise takes a hundred and seventy-six"},
    },
    "s2": {
        "stem": "owb_sa_s2_neptune", "id": "oyRcrFTYyDY", "vo": "owb_sa_s2_neptune_vo_v01", "air": "2026-10-24",
        "title": ("The Wind on Neptune", "Is Supersonic"), "kick": 0.25, "open_pan": (0.26, 0.44),
        "hook": (("SUPERSONIC",), ("WIND",)), "yellow": "SUPERSONIC",
        "sfx0": "whoosh",
        "rows": [
            (0.0, "s2_neptune/PIA01492.jpg", "cover", 0.44, 0.47, 1.55, 1.65),
            (5.9, "s2_neptune/PIA00063.jpg", "fit", 0.5, 0.5, 1.0, 1.12),
            (11.6, "s2_neptune/PIA00058.jpg", "fit", 0.5, 0.5, 1.12, 1.0),
            (16.3, "s2_neptune/PIA02210.jpg", "fit", 0.5, 0.5, 1.6, 1.8),
        ],
        "overlay": {"kind": "bars", "rows": (("EARTH 400", 0.2), ("NEPTUNE 2,000 KM/H", 1.0)), "window": (14.1, 17.9),
                    "spoken": "Earth's strongest winds barely reach four hundred"},
    },
    "s3": {
        "stem": "owb_sa_s3_iss_sunrises", "id": "XKlq0TK1OVA", "vo": "owb_sa_s3_iss_sunrises_vo_v01", "air": "2026-10-27",
        "title": ("Astronauts See 16", "Sunrises Every Day"), "hook": (("16", "SUNRISES"), ("A", "DAY")), "yellow": "16",
        "sfx0": "whoosh", "sfx_gain": 0.15,
        "rows": [
            (0.0, "s3_iss/iss040e080833.jpg", "cover", 0.62, 0.45, 1.0, 1.12),
            (4.0, "s3_iss/iss054e002538.jpg", "cover", 0.30, 0.45, 1.0, 1.10),
            (7.1, "s3_iss/iss064e044526.jpg", "cover", 0.42, 0.5, 1.0, 1.10),
            (12.8, "s3_iss/iss059e027932.jpg", "cover", 0.12, 0.47, 1.5, 1.65),
            (17.6, "s3_iss/iss061e123823.jpg", "cover", 0.5, 0.52, 1.9, 2.05),
            (22.0, "s3_iss/iss064e044526.jpg", "cover", 0.78, 0.5, 1.1, 1.0),
        ],
        "overlay": {"kind": "counter", "to": 16, "label": "EVERY 90 MINUTES", "window": (17.5, 21.6),
                    "spoken": "Sixteen sunrises. Sixteen sunsets."},
    },
    "s4": {
        "stem": "owb_sa_s4_uranus", "id": "ZpEA8stoSPA", "vo": "owb_sa_s4_uranus_vo_v01", "air": "2026-10-31",
        "title": ("This Planet Has", "21-Year Winters"), "hook": (("21-YEAR",), ("WINTER",)), "yellow": "WINTER",
        "sfx0": "rumble",
        "rows": [
            (0.0, "s4_uranus/webb_weic2310a.jpg", "fit", 0.5, 0.5, 1.25, 1.42),
            (5.9, "s4_uranus/PIA00143.jpg", "cover", 0.62, 0.5, 1.0, 1.08),
            (9.9, "s4_uranus/PIA18182.jpg", "fit", 0.5, 0.5, 1.0, 1.08),
            (12.7, "s4_uranus/PIA01391.jpg", "cover", 0.35, 0.5, 1.08, 1.0),
            (16.2, "s4_uranus/PIA00346.jpg", "fit", 0.5, 0.5, 1.0, 1.08),
        ],
        "overlay": {"kind": "fact", "lines": ("TIPPED", "97°"), "window": (6.4, 9.0),
                    "spoken": "Uranus is tipped ninety-seven degrees"},
    },
    "s5": {
        "stem": "owb_sa_s5_shooting_stars", "id": "T9fVlG3CCzU", "vo": "owb_sa_s5_shooting_stars_vo_v01", "trim": TRIM2, "air": "2026-11-03",
        "title": ("Shooting Stars", "Aren't Stars"), "hook": (("NOT", "A", "STAR"),), "yellow": "STAR",
        "sfx0": "whoosh", "kick": 0.2,
        "rows": [
            (0.0, "s5_meteors/NHQ202108110001.jpg", "cover", 0.63, 0.35, 1.0, 1.06),
            (4.7, "s5_meteors/NHQ202108110005.jpg", "cover", 0.50, 0.40, 1.0, 1.10),
            (8.9, "s5_meteors/NHQ202108100009.jpg", "cover", 0.55, 0.45, 1.08, 1.0),
            (13.36, "s5_meteors/NHQ202108110003.jpg", "cover", 0.32, 0.45, 1.0, 1.08),
        ],
        "overlay": {"kind": "scale", "labels": ("SAND", "PEA"), "window": (6.5, 8.9),
                    "spoken": "between a grain of sand and a pea"},
    },
    "s6": {
        "stem": "owb_sa_s6_titan", "id": "RLSJm59OSzI", "vo": "owb_sa_s6_titan_vo_v01", "trim": TRIM2, "air": "2026-11-07",
        "title": ("Standing on Titan Feels Like", "Diving 15 Metres Down"), "hook": (("15", "M"), ("UNDERWATER",)),
        "yellow": "15", "sfx0": "rumble", "fix": {"meters": "metres"}, "kick": 0.30,
        "rows": [
            (0.0, "s6_titan/PIA14925.jpg", "cover", 0.5, 0.5, 1.0, 1.06),
            (4.3, "s6_titan/PIA06230.jpg", "fit", 0.5, 0.5, 1.0, 1.10),
            (8.7, "s6_titan/PIA09739.jpg", "cover", 0.3, 0.5, 1.0, 1.04),
            (13.62, "s6_titan/PIA21625.jpg", "fit", 0.5, 0.5, 1.0, 1.10),
        ],
        "overlay": {"kind": "fact", "lines": ("2034", "LANDS"), "window": (17.3, 20.4),
                    "spoken": "and lands in 2034"},
    },
    "s7": {
        "stem": "owb_sa_s7_pluto_heart", "id": "gmzaCfJF1gA", "vo": "owb_sa_s7_pluto_heart_vo_v01", "trim": TRIM2, "air": "2026-11-10",
        "title": ("Pluto's Heart Has", "No Craters"), "hook": (("NO", "CRATERS"),), "yellow": "CRATERS",
        "sfx0": "whoosh",
        "rows": [
            (0.0, "s7_pluto/PIA19952.jpg", "cover", 0.62, 0.58, 1.0, 1.08),
            (5.88, "s7_pluto/PIA21863.jpg", "cover", 0.55, 0.5, 1.08, 1.0),
            (10.5, "s7_pluto/PIA20726.jpg", "cover", 0.5, 0.5, 1.0, 1.10),
            (13.62, "s7_pluto/PIA19708.jpg", "fit", 0.5, 0.5, 1.0, 1.10),
        ],
        "overlay": {"kind": "fact", "lines": ("2015", "NEW HORIZONS"), "window": (5.8, 8.9),
                    "spoken": "In 2015, New Horizons flew past"},
    },
    "s8": {
        "stem": "owb_sa_s8_voyager1", "id": "kKN8Ale42sE", "vo": "owb_sa_s8_voyager1_vo_v01", "trim": TRIM2, "air": "2026-11-14",
        "title": ("Voyager 1 Is About to Be", "One Light-Day Away"), "hook": (("ONE", "LIGHT-DAY"), ("AWAY",)),
        "yellow": "LIGHT-DAY", "sfx0": "whoosh", "fix": {"kilometers": "kilometres"},
        "open_pan": (0.66, 0.56),
        "rows": [
            (0.0, "s8_voyager/PIA04495.jpg", "cover", 0.40, 0.45, 1.0, 1.08),
            (4.6, "s8_voyager/PIA17049.jpg", "fit", 0.5, 0.5, 1.0, 1.10),
            (6.9, "s8_voyager/PIA23645.jpg", "cover", 0.5, 0.5, 1.0, 1.08),
            (9.98, "s8_voyager/PIA21741.jpg", "cover", 0.5, 0.45, 1.0, 1.08),
            (14.12, "s8_voyager/PIA17464.jpg", "cover", 0.5, 0.5, 1.0, 1.08),
        ],
        "overlay": {"kind": "counter", "to": 25.9, "decimals": 1, "run": 1.6, "label": "BILLION KM",
                    "window": (6.9, 8.95), "spoken": "Nearly 26 billion kilometres"},
    },
}


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def fit_font(draw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
    while size > 30:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, size)


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    draw.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return box[3] - box[1]


class Plate:
    """One source still, drawn at any zoom with a float crop box (no integer stepping, so pushes stay smooth)."""

    def __init__(self, path: Path, mode: str, cx: float, cy: float):
        im = Image.open(path).convert("RGB")
        self.src_size = im.size
        cap = 2600
        if max(im.size) > cap:
            k = cap / max(im.size)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        if "iss040e080833" in str(path) or "iss061e123823" in str(path):
            w, h = im.size
            rot = im.rotate(5.5, resample=Image.BICUBIC, expand=False)
            im = rot.crop((int(w * 0.05), int(h * 0.05), int(w * 0.95), int(h * 0.95)))
        self.im, self.mode, self.cx, self.cy = im, mode, cx, cy
        self.down = im.width / self.src_size[0]
        if mode == "cover":
            self.base = max(W / im.width, H / im.height)
            self.fg_h = H
        else:
            self.base = W / im.width
            self.fg_h = min(H, round(im.height * self.base))
            bg_scale = max(W / im.width, H / im.height)
            bg = im.resize((math.ceil(im.width * bg_scale), math.ceil(im.height * bg_scale)), Image.BILINEAR)
            bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
            bg = bg.filter(ImageFilter.GaussianBlur(40))
            self.bg = Image.eval(bg, lambda v: int(v * 0.55))
            mask = Image.new("L", (W, self.fg_h), 255)
            md = ImageDraw.Draw(mask)
            feather = min(90, self.fg_h // 6)
            for i in range(feather):
                a = int(255 * i / feather)
                md.line((0, i, W, i), fill=a)
                md.line((0, self.fg_h - 1 - i, W, self.fg_h - 1 - i), fill=a)
            self.mask = mask

    def prepare(self, z_from: float, z_to: float, cxs: tuple[float, ...] = ()) -> "Plate":
        import numpy as np

        check_cxs = (self.cx,) + tuple(cxs)
        for _ in range(3):
            need_scale, need_lift = 1.0, 0.0
            for cx_val in check_cxs:
                for z_val in (z_from, (z_from + z_to) / 2, z_to):
                    fr = np.array(self.frame(z_val, cx_val), dtype=np.float32)
                    luma = 0.299 * fr[:, :, 0] + 0.587 * fr[:, :, 1] + 0.114 * fr[:, :, 2]
                    p95 = float(np.percentile(luma[::4, ::4], 95))
                    mean = float(luma[::4, ::4].mean())
                    if p95 < 62.0:
                        need_scale = max(need_scale, 62.0 / max(p95, 1.0))
                    if mean * need_scale < 33.5:
                        need_lift = max(need_lift, (34.5 - mean * need_scale) * 1.25)
            if need_scale > 1.001 or need_lift > 0.1:
                lut = [
                    min(255, max(0, int(round(v * need_scale + need_lift * (1.0 - min(255.0, v * need_scale) / 255.0)))))
                    for v in range(256)
                ] * 3
                self.im = self.im.point(lut)
                if self.mode != "cover":
                    self.bg = self.bg.point(lut)
            else:
                break
        cw = W / self.base
        xs = np.arange(self.im.width, dtype=np.float32)
        h_wave = (8.5 + 8.5 * np.cos(2.0 * np.pi * (xs - self.cx * self.im.width) / cw)).reshape(1, self.im.width, 1)
        self.im = Image.fromarray(np.clip(np.array(self.im, dtype=np.float32) + h_wave, 0, 255).astype(np.uint8))
        if self.mode != "cover":
            x_bg = np.arange(W, dtype=np.float32)
            bg_wave = (8.5 + 8.5 * np.cos(2.0 * np.pi * (x_bg - W / 2) / W)).reshape(1, W, 1)
            self.bg = Image.fromarray(np.clip(np.array(self.bg, dtype=np.float32) + bg_wave, 0, 255).astype(np.uint8))
        return self

    def upscale(self, zoom: float) -> float:
        """Output pixels per original source pixel."""
        return self.base * zoom * self.down

    def frame(self, zoom: float, cx: float | None = None) -> Image.Image:
        cx = self.cx if cx is None else cx
        s = self.base * zoom
        out_h = self.fg_h
        cw, ch = W / s, out_h / s
        x0 = min(max(cx * self.im.width - cw / 2, 0), self.im.width - cw)
        y0 = min(max(self.cy * self.im.height - ch / 2, 0), self.im.height - ch)
        fg = self.im.transform((W, out_h), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)
        if self.mode == "cover":
            return fg
        canvas = self.bg.copy()
        canvas.paste(fg, (0, (H - out_h) // 2), self.mask)
        return canvas


def hook_png(spec) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lines = [" ".join(l) for l in spec["hook"]]
    font = fit_font(d, max(lines, key=len), 190, int(W * 0.84), 8)
    y = int(H * 0.06)
    for words in spec["hook"]:
        widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in words]
        space = d.textlength(" ", font=font)
        total = sum(b[2] - b[0] for b in widths) + space * (len(words) - 1)
        x = (W - total) / 2
        for w, b in zip(words, widths):
            d.text((x - b[0], y), w, font=font, fill=YELLOW if w == spec["yellow"] else WHITE,
                   stroke_width=8, stroke_fill=(0, 0, 0, 255))
            x += b[2] - b[0] + space
        y += max(b[3] - b[1] for b in widths) + 24
    return im


def title_png(spec) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, max(spec["title"], key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in spec["title"]:
        y += centred(d, y, row, font, WHITE, 5) + 18
    return im


def captions(words: list[dict], end: float) -> list[tuple[float, float, Image.Image]]:
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.6)
        text = " ".join(w["word"] for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.83), text, fit_font(d, text, 76, int(W * 0.78), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def overlay_frame(ov: dict, t: float) -> Image.Image | None:
    """One Teach-on-screen overlay inside the 16:9 centre band, lines at 11.5% of the band height, animated in/out."""
    a0, a1 = ov["window"]
    if not a0 <= t <= a1:
        return None
    alpha = min(ease((t - a0) / 0.4), ease((a1 - t) / 0.35))
    slide = int(24 * (1 - ease((t - a0) / 0.4)))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = BAND_TOP + 60 + slide
    if ov["kind"] == "fact":
        big = fit_font(d, ov["lines"][0], LINE_H + 40, int(W * 0.7), 7)
        y += centred(d, y, ov["lines"][0], big, YELLOW, 7) + 26
        small = fit_font(d, ov["lines"][1], LINE_H + 40, int(W * 0.84), 6)
        centred(d, y, ov["lines"][1], small, WHITE, 6)
    elif ov["kind"] == "bars":
        grow = ease((t - a0 - 0.3) / 1.2)
        x0, full = int(W * 0.10), int(W * 0.80)
        for i, (label, frac) in enumerate(ov["rows"]):
            font = fit_font(d, label, LINE_H, int(W * 0.84), 5)
            box = d.textbbox((0, 0), label, font=font, stroke_width=5)
            d.text((x0 - box[0], y), label, font=font, fill=YELLOW if i else WHITE, stroke_width=5,
                   stroke_fill=(0, 0, 0, 255))
            y += box[3] - box[1] + 16
            g = grow if i == 0 else ease((t - a0 - 0.8) / 1.4)
            d.rounded_rectangle((x0, y, x0 + full, y + 34), radius=17, fill=(0, 0, 0, 140), outline=WHITE, width=3)
            wbar = max(4, int((full - 12) * frac * g))
            d.rounded_rectangle((x0 + 6, y + 6, x0 + 6 + wbar, y + 28), radius=11, fill=(YELLOW if i else WHITE) + (255,))
            y += 34 + 40
    elif ov["kind"] == "counter":
        dec = ov.get("decimals", 0)
        k = ease((t - a0 - 0.2) / ov.get("run", 2.6))
        n = ov["to"] * k if dec else max(1, min(ov["to"], 1 + int((ov["to"] - 1) * k)))
        big = fit_font(d, f"{ov['to']:.{dec}f}", LINE_H + 90, int(W * 0.6), 8)
        y += centred(d, y, f"{n:.{dec}f}", big, YELLOW, 8) + 26
        small = fit_font(d, ov["label"], LINE_H, int(W * 0.86), 5)
        centred(d, y, ov["label"], small, WHITE, 5)
    elif ov["kind"] == "scale":
        # a grain growing into a pea along a drawn line: SAND (small) to PEA (big), labels under each
        x_a, x_b, cy = int(W * 0.22), int(W * 0.78), y + 90
        line = ease((t - a0 - 0.2) / 0.8)
        d.line((x_a, cy, x_a + (x_b - x_a) * line, cy), fill=WHITE + (255,), width=6)
        d.ellipse((x_a - 12, cy - 12, x_a + 12, cy + 12), fill=(235, 215, 170, 255), outline=(0, 0, 0, 255), width=3)
        r = int(70 * ease((t - a0 - 0.9) / 0.6))
        if r > 2:
            d.ellipse((x_b - r, cy - r, x_b + r, cy + r), fill=(140, 190, 90, 255), outline=(0, 0, 0, 255), width=4)
        font = fit_font(d, "SAND", LINE_H, int(W * 0.4), 6)
        for x, label, col in ((x_a, ov["labels"][0], WHITE), (x_b, ov["labels"][1], YELLOW)):
            box = d.textbbox((0, 0), label, font=font, stroke_width=6)
            d.text((x - (box[2] - box[0]) // 2 - box[0], cy + 100), label, font=font, fill=col, stroke_width=6,
                   stroke_fill=(0, 0, 0, 255))
    if alpha < 1:
        im.putalpha(Image.eval(im.getchannel("A"), lambda v: int(v * alpha)))
    return im


def build(key: str) -> dict:
    spec = SHORTS[key]
    work = WORK / spec["stem"]
    work.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    trim = spec.get("trim", TRIM)
    vo = trim / f"{spec['vo']}_trim.wav"
    words = json.loads((trim / f"{spec['vo']}_trim_words.json").read_text())["words"]
    fix = spec.get("fix", {})

    def spelled(word: str) -> str:
        core = word.rstrip(".,?!")
        return fix.get(core.lower(), core) + word[len(core):]

    words = [{"word": spelled(w["word"].strip()), "start": w["start"], "end": w["end"]} for w in words]
    last_end = words[-1]["end"]
    total = round(min(last_end + HOLD, MAX_TOTAL), 3)
    nframes = int(round(total * FPS))

    rows = spec["rows"]
    open_cxs = spec.get("open_pan", ())
    plates = [
        Plate(PLATES / r[1], r[2], r[3], r[4]).prepare(r[5], r[6], open_cxs if i == 0 else ())
        for i, r in enumerate(rows)
    ]
    ends = [r[0] for r in rows[1:]] + [last_end]
    opening = Plate(PLATES / rows[0][1], rows[0][2], rows[0][3], rows[0][4]).prepare(rows[0][5], rows[0][6], open_cxs)
    z_open_from, z_open_to = rows[0][5], rows[0][6]
    hook, title = hook_png(spec), title_png(spec)
    caps = captions(words, total)

    raw = work / "picture.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "noise=alls=4:allf=t,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "14", str(raw)], stdin=subprocess.PIPE)
    max_up = {}
    for f in range(nframes):
        t = f / FPS
        if t < last_end:
            i = max(j for j, r in enumerate(rows) if r[0] <= t)
            r = rows[i]
            if i == 0:
                # fast ease-out push in the first second, so frame 0 is already moving (gate motion check)
                x = min(t / OPEN_PUSH_S, 1.0)
                z = r[5] * (1 + spec.get("kick", OPEN_KICK) * (1 - (1 - x) ** 2)) + (r[6] - r[5]) * (t / ends[0])
                cx = None
                if "open_pan" in spec:
                    a, b = spec["open_pan"]
                    cx = a + (b - a) * (1 - (1 - x) ** 2)
            else:
                z = r[5] + (r[6] - r[5]) * ease((t - r[0]) / (ends[i] - r[0]))
                cx = None
            frame = plates[i].frame(z, cx)
            max_up[r[1]] = max(max_up.get(r[1], 0), plates[i].upscale(z))
        else:
            # loop: pull back onto frame 0's framing, crossfading from the last row
            k = (t - last_end) / max(total - last_end, 1e-3)
            z = z_open_from + (z_open_to - z_open_from) * 0.5 * (1 - ease(k))
            cx = None
            if "open_pan" in spec:
                a, b = spec["open_pan"]
                cx = b + (a - b) * ease(k)
            frame = opening.frame(z, cx)
            dt = t - last_end
            if dt < LOOP_XFADE:
                r = rows[-1]
                prev = plates[-1].frame(r[6])
                frame = Image.blend(prev, frame, ease(dt / LOOP_XFADE))
        frame = frame.convert("RGBA")
        if t < HOOK_END:
            frame.alpha_composite(hook)
        if TITLE[0] <= t < TITLE[1]:
            frame.alpha_composite(title)
        ov = overlay_frame(spec["overlay"], t)
        if ov is not None:
            frame.alpha_composite(ov)
        for a, b, im in caps:
            if a <= t < b:
                frame.alpha_composite(im)
                break
        enc.stdin.write(frame.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("picture encode failed")

    sfx0 = KIT / ("sfx_owb_rumble_low_v01.wav" if spec["sfx0"] == "rumble" else "sfx_owb_whoosh_soft_v01.wav")
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    c0 = spec["overlay"]["window"][0]
    vo_stem, bed_stem, sfx_stem = work / "stem_vo.wav", work / "stem_bed.wav", work / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-af",
         f"aresample=48000,volume={VO_GAIN},apad,atrim=0:{total}", "-ac", "2", vo_stem])
    hold_ramp = f"if(lt(t,{last_end}),{BED_GAIN},{BED_GAIN}+({BED_HOLD_GAIN}-{BED_GAIN})*min((t-{last_end})/0.6,1))"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total},volume='{hold_ramp}':eval=frame,afade=t=in:st=0:d=0.3,"
         f"afade=t=out:st={total - 0.6:.3f}:d=0.6", "-ac", "2", bed_stem])
    sfx_gain = spec.get("sfx_gain", 0.45 if spec["sfx0"] == "rumble" else 0.22)
    run(["ffmpeg", "-y", "-v", "error", "-i", sfx0, "-i", tick, "-filter_complex",
         f"[0:a]aresample=48000,volume={sfx_gain},afade=t=out:st=1.6:d=0.8,atrim=0:2.4[s0];"
         f"[1:a]aresample=48000,volume=0.3,adelay={int((c0 + 0.05) * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_stem])

    final = OUT / f"{spec['stem']}_v01.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", vo_stem, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
                            "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}",
         "-movflags", "+faststart", final])

    sheet = OUT / f"{spec['stem']}_v01_frames.jpg"
    times = [0.0, 1.0, 2.5] + [r[0] + 0.6 for r in rows[1:]] + [11.0, sum(spec["overlay"]["window"]) / 2, total - 0.1]
    times = sorted({round(min(x, total - 0.1), 2) for x in times})
    tiles = []
    for i, t in enumerate(times):
        p = work / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-vf", "scale=270:480", p])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    dd = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        dd.text((270 * i + 6, 482), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    cuts = [{"row": i + 1, "start_s": r[0], "end_s": round(ends[i], 3), "file": r[1], "mode": r[2],
             "zoom": [r[5], r[6]], "max_upscale": round(max_up.get(r[1], 0), 2)} for i, r in enumerate(rows)]
    cuts.append({"row": len(rows) + 1, "start_s": last_end, "end_s": total, "file": rows[0][1],
                 "mode": "loop", "note": f"{LOOP_XFADE} s crossfade back to the opening plate, pull-back to frame 0"})
    meta = {
        "job": "J0163", "short": key, "air_provisional": spec["air"], "title_on_screen": " ".join(spec["title"]),
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)), "sha256": sha256(final),
        "duration_s": dur(final), "vo": str(vo.relative_to(REPO)), "words": len(words), "last_word_end_s": last_end,
        "spoken": " ".join(w["word"] for w in words),
        "hook": " / ".join(" ".join(l) for l in spec["hook"]) + f" (yellow {spec['yellow']}), 0-{HOOK_END} s",
        "title_window_s": TITLE, "overlay": spec["overlay"], "cuts": cuts,
        "orbit_slot": {"start_s": 1.0, "status": "open: J0200 Omni insert, opening plate runs under it until then"},
        "audio": {"vo_gain": VO_GAIN, "bed": str(BED.relative_to(REPO)), "bed_gain": BED_GAIN,
                  "bed_hold_gain": BED_HOLD_GAIN, "sfx": f"{sfx0.name} at 0 s, tick at {c0 + 0.05:.2f} s",
                  "stems": {k: str(p) for k, p in (("vo", vo_stem), ("bed", bed_stem), ("sfx", sfx_stem))},
                  "mix": "-14 LUFS, -1.5 dBTP"},
        "grain": "noise=alls=4:allf=t", "spend": "none",
    }
    (OUT / f"{spec['stem']}_v01_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", spec["air"], "--id", spec["id"]],
                          capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v01_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo_stem),
                            "--sfx", str(sfx_stem), "--bed", str(bed_stem), "--minutes", f"{total / 60:.3f}"],
                           capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v01_sfx_level.txt").write_text(level.stdout + level.stderr)
    print(f"== {key} {final.name} {meta['duration_s']:.2f}s gate={gate.returncode} level={level.returncode}")
    print(gate.stdout[-1500:], level.stdout[-800:], flush=True)
    return {"gate": gate.returncode, "level": level.returncode}


def main() -> None:
    keys = sys.argv[1:] or list(SHORTS)
    for p in [BED, KIT / "sfx_owb_tick_ui_v01.wav"]:
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    results = {k: build(k) for k in keys}
    print(json.dumps(results))


if __name__ == "__main__":
    main()
