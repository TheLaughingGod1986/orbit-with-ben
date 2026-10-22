#!/usr/bin/env python3
"""J0347: 029 Betelgeuse teaching graphics from PLATE_BOARDS_v02. £0. No mint.

13 route=code plates plus the r22 subscribe card. 1920x1080, 50 fps so every
board duration lands on a whole frame. Labels are consecutive words from the
locked Scribe transcript, inside the action-safe area, 4 words or fewer.
Streams RGB to ffmpeg. Pictures stay out of git.

  python3 build_code_graphics_v01.py --out <edit>/code_graphics_v01 --previews
  python3 build_code_graphics_v01.py --out <edit>/code_graphics_v01
  python3 build_code_graphics_v01.py --out <edit>/code_graphics_v01 --only r05_scale
"""
import argparse, hashlib, json, math, subprocess
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1920, 1080, 50
GOLD = (255, 201, 74)
WHITE = (244, 239, 230)
ICE = (176, 214, 232)
ORANGE = (255, 154, 72)
DIM = (150, 168, 190)
HERE = Path(__file__).resolve().parent
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
# Local seconds inside each plate. Each phrase is consecutive spoken words.
LABELS = {
    "r03_r04_promise": [(6.2, 9.4, "daytime sky"), (9.6, 12.8, "kind of star"),
                        (13.1, 15.1, "in 2019"), (15.2, 18.6, "giant star actually dies"),
                        (19.5, 21.0, "your garden"), (21.2, 22.98, "honest answer")],
    # Text-free (script v02 line 24). Chief FIX 16 Oct: no "where the Sun is" / "orbit of Mars".
    "r05_scale": [],
    "r09_finder": [(3.6, 6.2, "three stars"), (6.3, 9.6, "to the left"), (10.6, 12.56, "glows orange")],
    "r10_r11_dip": [(3.6, 5.4, "began to fade"), (5.5, 7.7, "February 2020"),
                    (7.8, 11.0, "about a third"), (12.1, 13.66, "fifty years")],
    "r15_dip": [(0.2, 3.4, "that point fades"), (3.6, 4.96, "happening inside")],
    "r17_r20_shells": [(0.15, 3.2, "Gravity pulls"), (3.4, 6.6, "nuclear fusion"),
                       (9.4, 12.4, "into helium"), (12.6, 15.0, "into carbon"),
                       (15.1, 18.3, "heavier and heavier"), (21.8, 25.0, "only years, then days"),
                       (25.4, 28.6, "is iron"), (29.2, 32.4, "costs energy"),
                       (34.4, 36.5, "gravity wins"), (36.6, 39.8, "less than a second"),
                       (41.2, 44.4, "size of a city"), (46.8, 48.62, "into space")],
    "r21_hero": [(0.0, 3.4, "a mountain")],
    "r23_paranal": [(0.1, 3.4, "imagine the night"), (4.8, 6.32, "not be light")],
    "r25_orion": [(0.3, 2.3, "the light arrives"), (2.4, 5.8, "Within days"), (6.6, 8.04, "at half phase")],
    "r27_orion": [(0.7, 4.0, "bright for weeks"), (4.2, 7.4, "over months"),
                  (7.6, 10.8, "simply gone"), (15.9, 18.48, "a different Orion")],
    "r29_span_astrolabe": [(4.2, 7.4, "takes centuries"), (8.8, 11.0, "late Middle Ages"),
                           (11.1, 14.3, "five hundred years"), (21.5, 23.44, "hundred thousand years")],
    "r31_shells_twins": [(5.1, 8.4, "deep in the core"), (13.0, 15.6, "100,000 years"),
                         (15.8, 17.5, "a hundred years"), (17.6, 18.94, "almost the same")],
    "r35_song": [(3.5, 6.0, "1054"), (6.1, 9.4, "in China")],
    "r13_compare": [],
    "r21_bh": [(1.9, 5.08, "black hole")],
}
SKY = {"r09_finder", "r23_paranal", "r25_orion", "r27_orion", "r35_song"}
ORION = {
    "betelgeuse": (5.919, 7.41, "orange"), "bellatrix": (5.418, 6.35, "blue"),
    "meissa": (5.585, 9.93, "white"), "alnitak": (5.679, -1.94, "belt"),
    "alnilam": (5.604, -1.20, "belt"), "mintaka": (5.533, -0.30, "belt"),
    "saiph": (5.796, -9.67, "white"), "rigel": (5.242, -8.20, "blue"),
}
SHELLS = [(255, 176, 122), (255, 210, 122), (242, 226, 160), (183, 217, 138), (143, 208, 216), (176, 182, 194)]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 0.5 - 0.5 * math.cos(math.pi * x)


def scale_s(t):
    """Fraction of the 3.55 AU outline. Mars (1.52 AU) at t=4.1 s; belt outer near the end."""
    return ease(max(0.0, min(1.0, -0.19 + 0.157 * t)))


def tokens(s):
    out, buf = [], ""
    for ch in s.lower().replace("’", "'"):
        if ch.isalnum() or ch == "'":
            buf += ch
        elif ch == "," and buf and buf[-1].isdigit():
            buf += ch
        else:
            if buf:
                out.append(buf.strip(","))
                buf = ""
    if buf:
        out.append(buf.strip(","))
    return out


@lru_cache(None)
def font(n):
    return ImageFont.truetype(FONT, n)


def text(im, s, xy, size=64, color=WHITE, alpha=1, anchor="mm"):
    if alpha <= 0.02 or not s:
        return
    last = None
    for size in (size, 56, 46, 40):
        layer = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(layer)
        box = d.textbbox(xy, s, font=font(size), anchor=anchor, stroke_width=2)
        last = box
        if 95 <= box[0] and box[2] <= 1825 and 54 <= box[1] and box[3] <= 1026:
            d.text(xy, s, font=font(size), fill=(*color, int(255 * alpha)), anchor=anchor,
                   stroke_width=2, stroke_fill=(12, 23, 39, int(210 * alpha)))
            im.paste(layer, (0, 0), layer)
            return
    raise ValueError(f"Unsafe text {s!r}: {last}")


def luma(im):
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    g = a[:, :, 0] * 0.2126 + a[:, :, 1] * 0.7152 + a[:, :, 2] * 0.0722
    return float(g.mean()), float(np.percentile(g, 95))


def orion_px(ra, dec):
    x = -(ra - 5.58) * 15 * 0.42
    y = (dec - -0.5) * 0.42
    return 960 + x * 120, 540 - y * 120


def label_y(ident, t):
    if ident == "r03_r04_promise":
        return 900 if t < 8.7 else 150
    if ident == "r29_span_astrolabe":
        return 900
    if ident in SKY:
        return 900
    return 150


class Renderer:
    def __init__(self, assets):
        sun = Image.open(assets / "sun_sdo.jpg").convert("RGB").crop((448, 212, 3648, 3412))
        self.sun = sun
        self.earth = Image.open(assets / "earth.jpg").convert("RGB")
        self.mars = Image.open(assets / "mars.jpg").convert("RGB")
        hdir = HERE / "harvest_v01"
        self.sphere_jan = Image.open(hdir / "sphere_jan.jpg").convert("RGB")
        self.sphere_dec = Image.open(hdir / "sphere_dec.jpg").convert("RGB")
        self.bodies = {}
        self.blobs = {}
        rng = np.random.default_rng(1054)
        y, x = np.mgrid[:H, :W]
        rad = np.sqrt(((x - 960) / 840) ** 2 + ((y - 540) / 540) ** 2)
        g1 = np.exp(-rad ** 2 * 1.4)
        band_d = ((x - 960) * 0.42 + (y - 540) * 0.91) / 340.0
        band_l = ((x - 960) * 0.91 - (y - 540) * 0.42) / 780.0
        mw = np.exp(-band_d ** 2) * np.exp(-band_l ** 2 * 0.7)
        dust = np.exp(-((band_d - 0.18) / 0.32) ** 2) * np.exp(-band_l ** 2 * 1.1)
        g2 = np.exp(-(((x - 520) / 400) ** 2 + ((y - 340) / 280) ** 2))
        g3 = np.exp(-(((x - 1400) / 420) ** 2 + ((y - 720) / 300) ** 2))
        glow = np.clip(0.68 * g1 + 0.45 * mw - 0.22 * dust + 0.32 * g2 + 0.28 * g3, 0, 1.35)
        base = np.stack([16 + 64 * glow, 24 + 84 * glow, 38 + 112 * glow], axis=-1)
        bg = Image.fromarray(np.uint8(np.clip(base, 0, 255)))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for cr in (220, 350, 480, 620, 760, 900):
            ld.ellipse((960 - cr, 540 - int(cr * 0.62), 960 + cr, 540 + int(cr * 0.62)),
                       outline=(165, 195, 230, 88), width=2)
            for deg in range(0, 360, 3):
                ang = math.radians(deg)
                r1 = cr - (10 if deg % 12 == 0 else 6)
                r2 = cr + (10 if deg % 12 == 0 else 6)
                ld.line((960 + r1 * math.cos(ang), 540 + r1 * 0.62 * math.sin(ang),
                         960 + r2 * math.cos(ang), 540 + r2 * 0.62 * math.sin(ang)),
                        fill=(185, 212, 242, 115), width=2)
        srng = np.random.default_rng(10540)
        for n_stars, r_px, alpha in [(420, 2.2, 130), (190, 3.2, 155), (55, 4.5, 175)]:
            for sx, sy in srng.uniform([70, 100], [1850, 980], (n_stars, 2)):
                ld.ellipse((sx - r_px, sy - r_px, sx + r_px, sy + r_px), fill=(215, 232, 252, alpha))
        self.bg = Image.alpha_composite(bg.convert("RGBA"), layer).convert("RGB")
        self.field = rng.uniform([8, 8], [1912, 1072], (140, 2))
        self.belt = np.stack([
            rng.uniform(2.2, 3.3, 280),
            rng.uniform(0, 2 * math.pi, 280),
        ], axis=1)
        self.orion = {n: (*orion_px(ra, dec), kind) for n, (ra, dec, kind) in ORION.items()}

    def sun_dot(self, im, xy, r=8):
        """A small yellow-white Sun. Not the SDO disc."""
        x, y = xy
        glow = Image.new("RGBA", im.size)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((x - r * 3, y - r * 3, x + r * 3, y + r * 3), fill=(255, 232, 170, 80))
        gd.ellipse((x - r, y - r, x + r, y + r), fill=(255, 248, 220, 255))
        im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def body(self, im, xy, r, kind="sun"):
        r = max(4, int(r))
        key = (r, kind)
        if key not in self.bodies:
            src = {"earth": self.earth, "mars": self.mars}.get(kind, self.sun)
            sprite = ImageOps.fit(src, (2 * r, 2 * r), method=Image.Resampling.LANCZOS)
            if kind == "sun":
                sprite = sprite.filter(ImageFilter.GaussianBlur(radius=max(1, r / 12)))
            mask = Image.new("L", (2 * r, 2 * r))
            ImageDraw.Draw(mask).ellipse((1, 1, 2 * r - 2, 2 * r - 2), fill=255)
            sprite.putalpha(mask)
            self.bodies[key] = sprite
        im.paste(self.bodies[key], (int(xy[0] - r), int(xy[1] - r)), self.bodies[key])

    def base(self, t, grid=False):
        im = self.bg.copy()
        d = ImageDraw.Draw(im)
        shift = (t * 18) % 40
        for x, y in self.field:
            x = 8 + (x - 8 + shift) % 1904
            d.ellipse((x, y, x + 2.2, y + 2.2), fill=(196, 208, 222))
        if grid:
            gshift = int(t * 6) % 90
            for x in range(-90, 2010, 90):
                d.line((x + gshift, 150, x + gshift, 960), fill=(58, 82, 112), width=1)
            for y in range(170, 980, 90):
                d.line((70, y, 1850, y), fill=(58, 82, 112), width=1)
        return im

    def credit(self, im, kind):
        if kind == "eso_cgi":
            text(im, "ESO/M. Montargès et al. · CGI", (120, 990), 28, ICE, anchor="lm")
        else:
            text(im, "NASA · CGI" if kind == "nasa" else "CGI", (120, 990), 28, ICE, anchor="lm")

    def stars(self, im, t, flare=0, fade=0, zoom=1, focus=None, hide=False):
        if hide:
            return
        d = ImageDraw.Draw(im)
        fx, fy = focus or self.orion["betelgeuse"][:2]
        def Z(x, y):
            return fx + (x - fx) * zoom, fy + (y - fy) * zoom
        for name, (x, y, kind) in self.orion.items():
            if name == "betelgeuse":
                continue
            x, y = Z(x, y)
            col = (210, 226, 255) if kind == "blue" else WHITE
            r = 9 if kind == "belt" else 6
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)
        x, y = Z(*self.orion["betelgeuse"][:2])
        a = max(0, 1 - fade)
        if a > 0.03:
            col = WHITE if flare > 0.55 else ORANGE
            radius = int(28 + 210 * flare * a)
            key = (radius, col)
            if key not in self.blobs:
                s = radius * 2
                yy, xx = np.mgrid[:s, :s]
                dist = np.sqrt((xx - radius) ** 2 + (yy - radius) ** 2) / max(1, radius)
                alpha = np.clip(1 - dist, 0, 1) ** 0.85
                arr = np.zeros((s, s, 4), np.uint8)
                arr[..., 0], arr[..., 1], arr[..., 2] = col
                arr[..., 3] = (alpha * 255).astype(np.uint8)
                self.blobs[key] = Image.fromarray(arr, "RGBA")
            glow = Image.new("RGBA", im.size)
            glow.paste(self.blobs[key], (int(x - radius), int(y - radius)), self.blobs[key])
            # Fade the whole glow with the shoulder.
            if a < 0.98:
                band = glow.getchannel("A").point(lambda p: int(p * a))
                glow.putalpha(band)
            im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def sky(self, im, t, flare=0, fade=0, zoom=1, hide=False):
        self.stars(im, t, flare, fade, zoom, hide=hide)

    def scale(self, im, t, s, moving=True):
        d = ImageDraw.Draw(im)
        cx, cy, k = 960, 530, 148
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        R = max(8, 3.55 * k * s)
        ld.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(*ORANGE, 70))
        im.paste(Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB"))
        d = ImageDraw.Draw(im)
        for au, col in ((0.39, DIM), (0.72, DIM), (1.0, ICE), (1.52, (214, 122, 86))):
            rr = au * k
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=col, width=2)
        for rad, ang in self.belt:
            d.ellipse((cx + rad * k * math.cos(ang) - 1.4, cy + rad * k * math.sin(ang) - 1.4,
                       cx + rad * k * math.cos(ang) + 1.4, cy + rad * k * math.sin(ang) + 1.4), fill=WHITE)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=ORANGE, width=3)
        ang = t * 0.55
        # Small yellow-white dot. The mottled SDO disc reads as Betelgeuse (Chief FIX 16 Oct).
        self.sun_dot(im, (cx, cy))
        self.body(im, (cx + k * math.cos(ang), cy + k * math.sin(ang)), 22, "earth")
        self.body(im, (cx + 1.52 * k * math.cos(ang * 0.6 + 1), cy + 1.52 * k * math.sin(ang * 0.6 + 1)), 18, "mars")

    def dip(self, im, t, pen, tight=False):
        d = ImageDraw.Draw(im)
        cx, trough = 0.687, None
        xs, ys = [], []
        for i in range(240):
            u = i / 239
            flux = 1 - 0.64 * math.exp(-((u - cx) / 0.10) ** 2)
            x = 240 + 1440 * u
            y = 250 + 520 * (1 - (flux - 0.30) / 0.75)
            xs.append(x); ys.append(y)
            if trough is None or y > trough[1]:
                trough = (x, y)
        z = 1.85 if tight else 1.0
        fx, fy = trough
        def Z(x, y):
            return fx + (x - fx) * z, fy + (y - fy) * z
        d.line([Z(240, ys[0]), Z(1680, ys[0])], fill=DIM, width=2)
        m = max(2, int(len(xs) * pen))
        pts = [Z(xs[i], ys[i]) for i in range(m)]
        if len(pts) >= 2:
            d.line(pts, fill=ORANGE, width=5)
        x, y = pts[-1]
        pulse = 10 + 4 * math.sin(t * 5)
        glow = Image.new("RGBA", im.size)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((x - pulse * 2, y - pulse * 2, x + pulse * 2, y + pulse * 2), fill=(*ORANGE, 50))
        gd.ellipse((x - pulse, y - pulse, x + pulse, y + pulse), fill=(*ORANGE, 230))
        im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def shells(self, im, t, grow, snap, shock, zoom=1, leader=True):
        d = ImageDraw.Draw(im)
        cx, cy = 960, 560
        radii = [330, 270, 215, 165, 120]
        ang = (t * 28) % 360
        wedge = 70
        for r, col in zip(radii, SHELLS):
            rr = r * (1 - 0.75 * snap) * zoom
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        core = (28 + 90 * grow) * (1 - 0.88 * snap) * zoom
        d.ellipse((cx - core, cy - core, cx + core, cy + core), fill=SHELLS[-1])
        if wedge > 0 and snap < 0.8:
            box_r = radii[0] * (1 - 0.75 * snap) * zoom
            d.pieslice((cx - box_r, cy - box_r, cx + box_r, cy + box_r), ang - wedge / 2, ang + wedge / 2, fill=(20, 28, 42))
            for r, col in zip(radii, SHELLS):
                rr = r * (1 - 0.75 * snap) * zoom
                d.pieslice((cx - rr, cy - rr, cx + rr, cy + rr), ang - wedge / 2, ang + wedge / 2, fill=col)
            d.pieslice((cx - core, cy - core, cx + core, cy + core), ang - wedge / 2, ang + wedge / 2, fill=SHELLS[-1])
        if snap > 0.45:
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=WHITE)
        # The rotating radius had no label. Chief FIX 16 Oct: off on r17 and r31.
        if leader:
            arm = radii[0] * (1 - 0.75 * snap) * zoom
            d.line((cx, cy, cx + arm * math.cos(ang * math.pi / 180), cy + arm * math.sin(ang * math.pi / 180)), fill=WHITE, width=3)
        if shock > 0:
            rs = 40 + 900 * shock
            width = max(2, int(14 * (1 - 0.7 * shock)))
            outline = tuple(int(255 * (1 - 0.55 * shock)) for _ in range(3))
            d.ellipse((cx - rs, cy - rs, cx + rs, cy + rs), outline=outline, width=width)

    def twins(self, im, t, open_):
        d = ImageDraw.Draw(im)
        for x0 in (-360, 360):
            cx, cy = 960 + x0, 540
            self.body(im, (cx, cy), 150, "sun")
            if open_ > 0.02:
                th = 64 * open_
                ang = -90
                radii = [150, 112, 78] if x0 < 0 else [150, 124, 100, 78, 56, 34]
                cols = SHELLS[:3] if x0 < 0 else SHELLS
                for r, col in zip(radii, cols):
                    d.pieslice((cx - r, cy - r, cx + r, cy + r), ang - th / 2, ang + th / 2, fill=col)

    def astrolabe(self, im, t, reveal):
        d = ImageDraw.Draw(im)
        cx, cy = 960, 560
        for i, r in enumerate((250, 190, 120)):
            if reveal > i / 3:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=3)
        ticks = int(24 * reveal)
        for i in range(ticks):
            a = i / 24 * 2 * math.pi
            d.line((cx + 200 * math.cos(a), cy + 200 * math.sin(a),
                    cx + 248 * math.cos(a), cy + 248 * math.sin(a)), fill=GOLD, width=2)
        arm = t * 0.7
        d.line((cx - 230 * math.cos(arm), cy - 230 * math.sin(arm),
                cx + 230 * math.cos(arm), cy + 230 * math.sin(arm)), fill=WHITE, width=4)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=ORANGE)

    def teaspoon(self, im, t):
        d = ImageDraw.Draw(im)
        grow = ease(min(1, t / 1.1))
        # Level beam. "weigh as much as a mountain" — neither pan sits lower (Chief FIX 16 Oct).
        beam_y = 750
        d.line((960, 800, 960, 940), fill=ICE, width=6)
        d.line((360, beam_y, 1560, beam_y), fill=ICE, width=7)
        # Side-view teaspoon on the left pan (Chief FIX 16 Oct, second pass).
        # Oval bowl, handle running sideways along the beam. Not a vertical flask neck.
        fill = (232, 226, 214)
        handle = [(620, 628), (930, 648), (930, 688), (620, 708)]
        d.polygon(handle, fill=fill)
        d.line(handle + [handle[0]], fill=WHITE, width=5)
        bowl = (390, 545, 680, 755)
        d.ellipse(bowl, fill=fill, outline=WHITE, width=7)
        d.arc((455, 590, 640, 720), 200, 340, fill=(150, 140, 128), width=4)
        peak = beam_y - int(360 * max(grow, 0.2))
        d.line([(1160, beam_y), (1360, peak), (1560, beam_y)], fill=GOLD, width=7)

    def song(self, im, t):
        d = ImageDraw.Draw(im)
        reveal = ease(min(1, t / 2.2))
        box = (700, 180, 1220, 760)
        d.rounded_rectangle(box, radius=18, fill=(214, 196, 164), outline=(120, 96, 64), width=4)
        # Ink builds across the scroll. Not a sourced painting, and not the 1054 record.
        if reveal > 0:
            hill = [(760, 640), (860, 640 - 120 * reveal), (980, 640), (1100, 640 - 180 * reveal), (1180, 640)]
            d.line(hill, fill=(92, 64, 42), width=4)
        if t > 1.4:
            a = ease((t - 1.4) / 0.6)
            d.ellipse((980 - 8, 280 - 8, 980 + 8, 280 + 8), fill=(160, 40, 36))
            yy = 300 + 80 * a
            d.line((1040, 300, 1120, yy), fill=(92, 64, 42), width=3)
        if t > 3:
            tw = 0.55 + 0.45 * math.sin(t * 3)
            d.ellipse((930, 250, 948, 268), fill=tuple(int(c * tw) for c in (180, 40, 36)))

    def sphere_split(self, im, t, dur):
        # J0353 Chief ruling: our own £0 code split of sphere_jan | sphere_dec with house labels (Jan 2019 / Dec 2019),
        # then push into the December half (no vertical seam/gutter across full height).
        push = ease(max(0.0, (t - 3.6) / max(0.1, dur - 3.6)))
        s_jan = int(round(560 * (1.0 - 0.18 * push)))
        s_dec = int(round(560 * (1.0 + 0.28 * push)))
        x_jan = int(round(540 - 240 * push))
        x_dec = int(round(1380 - 420 * push))
        y_c = 520
        for src_im, sz, cx, lbl, col in (
            (self.sphere_jan, s_jan, x_jan, "Jan 2019", ICE),
            (self.sphere_dec, s_dec, x_dec, "Dec 2019", GOLD),
        ):
            key = ("sphere_card", id(src_im), sz)
            if key not in self.bodies:
                tile = src_im.resize((sz, sz), Image.Resampling.LANCZOS)
                arr = np.asarray(tile, dtype=np.float32) / 255.0
                arr = np.clip((arr ** 0.72) * 255.0 + 14.0, 0.0, 255.0).astype(np.uint8)
                tile = Image.fromarray(arr)
                mask = Image.new("L", (sz, sz), 0)
                ImageDraw.Draw(mask).rounded_rectangle((2, 2, sz - 3, sz - 3), radius=28, fill=255)
                rgba = tile.convert("RGBA")
                rgba.putalpha(mask)
                self.bodies[key] = rgba
            card = self.bodies[key]
            x0, y0 = cx - sz // 2, y_c - sz // 2
            im.paste(card, (x0, y0), card)
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((x0 + 2, y0 + 2, x0 + sz - 3, y0 + sz - 3), radius=28, outline=col, width=4)
            text(im, lbl, (cx, max(96, y0 - 42)), 52, col, 1.0)

    def core_collapse_bh(self, im, t, dur):
        # J0353 Chief ruling: £0 code graphic of single-star core collapse into a black hole.
        cx, cy = 960, 560
        collapse = ease(min(1.0, t / 2.2))
        bh_reveal = ease(max(0.0, (t - 1.5) / 1.4))
        d = ImageDraw.Draw(im)
        # Infalling core shells & streamlines
        for i, col in enumerate(SHELLS):
            r_start = 320 - i * 42
            r_end = 52 + i * 6
            rr = r_start * (1.0 - collapse) + r_end * collapse
            if rr > 54:
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=col, width=4)
        for k in range(16):
            ang = k * (math.pi / 8.0) + t * 0.45
            r_outer = 380 - 220 * ((t * 0.65 + k * 0.13) % 1.0)
            r_inner = max(58, r_outer - 65)
            d.line(
                (
                    cx + r_outer * math.cos(ang),
                    cy + r_outer * math.sin(ang),
                    cx + r_inner * math.cos(ang + 0.12),
                    cy + r_inner * math.sin(ang + 0.12),
                ),
                fill=ICE if k % 2 == 0 else GOLD,
                width=3,
            )
        # Accretion photon ring + black hole shadow
        if bh_reveal > 0.02:
            ring_r = int(84 + 28 * bh_reveal + 4 * math.sin(t * 4.0))
            glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            for dr, a_mul, c_rgb in ((44, 55, ORANGE), (22, 120, GOLD), (8, 220, WHITE)):
                rr = ring_r + dr
                gd.ellipse((cx - rr, cy - int(rr * 0.38), cx + rr, cy + int(rr * 0.38)), outline=(*c_rgb, int(a_mul * bh_reveal)), width=6)
                gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(*c_rgb, int(a_mul * 0.85 * bh_reveal)), width=5)
            sh_r = int(58 * bh_reveal)
            gd.ellipse((cx - sh_r, cy - sh_r, cx + sh_r, cy + sh_r), fill=(8, 11, 18, int(255 * bh_reveal)))
            gd.ellipse((cx - sh_r - 3, cy - sh_r - 3, cx + sh_r + 3, cy + sh_r + 3), outline=(*GOLD, int(240 * bh_reveal)), width=4)
            im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))

    def subscribe(self, im, t):
        a = min(ease((t - 1.9) / 0.4), ease((4.2 - t) / 0.35))
        if a > 0:
            text(im, "Subscribe", (1520, 860), 58, GOLD, a)

    def frame(self, plate, t):
        ident = plate["id"]
        dur = plate["use_s"]
        chart = ident in ("r05_scale", "r10_r11_dip", "r13_compare", "r15_dip", "r17_r20_shells", "r21_hero", "r21_bh", "r31_shells_twins")
        if ident == "r03_r04_promise":
            chart = t >= 8.7
        if ident == "r29_span_astrolabe":
            chart = 7.6 <= t <= 15.4
        im = self.base(t, grid=chart)
        if ident == "r03_r04_promise":
            if t < 8.7:
                self.sky(im, t, flare=ease((t - 4.2) / 2.4), zoom=1 + 0.18 * ease(t / 8))
            elif t < 13.5:
                self.scale(im, t, ease((t - 8.7) / 4.6) * 0.48)
            elif t < 18.3:
                self.dip(im, t, ease((t - 13.5) / 4.4))
            else:
                u = (t - 18.3) / 4.6
                self.shells(im, t, grow=ease(u), snap=0, shock=0, zoom=1)
        elif ident == "r05_scale":
            self.scale(im, t, scale_s(t))
        elif ident == "r09_finder":
            u = t / dur
            self.sky(im, t, flare=0, zoom=1 + 0.45 * ease((u - 0.62) / 0.38))
            d = ImageDraw.Draw(im)
            belt = ease(u / 0.28)
            trail = ease((u - 0.28) / 0.34)
            for name in ("alnitak", "alnilam", "mintaka"):
                x, y, _ = self.orion[name]
                r = 8 + 7 * belt
                d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)
            if trail > 0:
                bx, by = self.orion["alnilam"][:2]
                tx, ty = self.orion["betelgeuse"][:2]
                n = max(2, int(16 * trail))
                for i in range(n):
                    m = 0.08 + 0.84 * (i / max(1, n - 1)) * trail
                    d.ellipse((bx + (tx - bx) * m - 3, by + (ty - by) * m - 3,
                               bx + (tx - bx) * m + 3, by + (ty - by) * m + 3), fill=GOLD)
        elif ident == "r10_r11_dip":
            pen = min(1, t / 11.2)
            self.dip(im, t, pen, tight=False)
        elif ident == "r15_dip":
            self.dip(im, t, 1, tight=True)
        elif ident == "r17_r20_shells":
            grow = ease(max(0, (t - 5.5) / 30))
            # Snap starts on "collapses" (film 215.32 s), not on "In" (211.94 s).
            snap_at = 215.32 - 175.4
            snap = ease((t - snap_at) / 0.8)
            shock = 0 if t < snap_at + 0.85 else ease(min(1, (t - (snap_at + 0.85)) / 5.5))
            zoom = 1 + 0.28 * ease(max(0, (t - 12) / 22))
            if t > snap_at - 0.05:
                zoom = max(0.72, 1.28 - 0.7 * ease((t - (snap_at - 0.05)) / 3))
            self.shells(im, t, grow, snap, shock, zoom, leader=False)
        elif ident == "r21_hero":
            self.teaspoon(im, t)
        elif ident == "r22_subscribe":
            self.sky(im, t, zoom=1 + 0.06 * (t / dur))
            self.subscribe(im, t)
        elif ident == "r23_paranal":
            self.sky(im, t, zoom=1 + 0.08 * (t / dur))
        elif ident == "r25_orion":
            flare = ease((t - 2.58) / 1.5)
            self.sky(im, t, flare=flare, zoom=1 + 0.32 * ease(t / dur))
        elif ident == "r27_orion":
            fade = ease(t / dur)
            self.sky(im, t, flare=1 - fade, fade=fade, zoom=1.25 - 0.25 * ease(t / dur))
        elif ident == "r29_span_astrolabe":
            self.sky(im, t, zoom=1 + 0.08 * math.sin(t * 0.15), hide=7.5 <= t <= 15.6)
            if 7.5 <= t <= 15.6:
                reveal = ease((t - 7.5) / 1.3)
                fade = ease((t - 14.6) / 1.0) if t > 14.6 else 0
                if fade < 0.98:
                    self.astrolabe(im, t, reveal * (1 - fade))
        elif ident == "r31_shells_twins":
            if t < 3.3:
                self.shells(im, t, grow=0.72, snap=0, shock=0, zoom=1.35, leader=False)
            else:
                local = t - 3.3
                # Open on "deep in the core", close as the two lives "look almost the same".
                open_ = ease((t - 5.2) / 1.6) * (1 - ease((t - 16.4) / 1.5))
                self.twins(im, t, open_)
        elif ident == "r35_song":
            self.song(im, t)
        elif ident == "r13_compare":
            self.sphere_split(im, t, dur)
        elif ident == "r21_bh":
            self.core_collapse_bh(im, t, dur)
        else:
            raise ValueError(ident)
        for start, end, label in LABELS.get(ident, []):
            if start <= t <= end:
                alpha = min(ease((t - start) / 0.4), ease((end - t) / 0.4))
                text(im, label, (960, label_y(ident, t)), 64, GOLD, alpha)
        if ident == "r13_compare":
            kind = "eso_cgi"
        elif ident in ("r05_scale", "r31_shells_twins") or (ident == "r03_r04_promise" and 8.7 <= t < 13.5):
            kind = "nasa"
        else:
            kind = "cgi"
        self.credit(im, kind)
        return im


def check_labels(words):
    board_file = HERE / ("PLATE_BOARDS_v03.json" if (HERE / "PLATE_BOARDS_v03.json").exists() else "PLATE_BOARDS_v02.json")
    plates = {p["id"]: p for p in json.loads(board_file.read_text())["plates"]}
    for ident, rows in LABELS.items():
        prev = -1
        for start, end, label in rows:
            if start < prev:
                raise SystemExit(f"overlap {ident} {label}")
            prev = end
            if label == "1054":
                continue
            t0 = plates[ident]["t_in_s"] + start - 0.35
            t1 = plates[ident]["t_in_s"] + end + 0.35
            spoken = []
            for w in words:
                if w["end"] < t0 or w["start"] > t1:
                    continue
                spoken.extend(tokens(w["word"]))
            need = tokens(label)
            found = False
            for i in range(len(spoken) - len(need) + 1):
                if spoken[i:i + len(need)] == need:
                    found = True
                    break
            if not found:
                raise SystemExit(f"label {ident!r} {label!r} not in VO window: {spoken}")
    # 1054 is the year said as "ten fifty-four".
    p = plates["r35_song"]
    heard = " ".join(w["word"] for w in words if p["t_in_s"] <= w["start"] <= p["t_in_s"] + p["use_s"])
    if "fifty-four" not in heard and "fifty four" not in heard:
        raise SystemExit("1054 year not spoken in r35")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--previews", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    assert abs(scale_s(4.1) * 3.55 - 1.52) < 0.03, scale_s(4.1) * 3.55
    words = json.loads((HERE.parent / "02_Voiceover" / "words.json").read_text())["words"]
    check_labels(words)
    boards = HERE / ("PLATE_BOARDS_v03.json" if (HERE / "PLATE_BOARDS_v03.json").exists() else "PLATE_BOARDS_v02.json")
    all_plates = [p for p in json.loads(boards.read_text())["plates"] if p["route"] in ("code", "card")]
    if len(all_plates) not in (14, 16):
        raise SystemExit(f"expected 14 or 16 plates, got {[p['id'] for p in all_plates]}")
    want = {s.strip() for s in a.only.split(",")} if a.only else None
    plates = [p for p in all_plates if want is None or p["id"] in want]
    if want and len(plates) != len(want):
        raise SystemExit(f"unknown plate in --only {a.only}: have {[p['id'] for p in plates]}")
    a.out.mkdir(parents=True, exist_ok=True)
    r = Renderer(a.out / "assets")
    records, thumbs = [], []
    for p in plates:
        frames = round(p["use_s"] * FPS)
        if abs(frames / FPS - p["use_s"]) > 1e-9:
            raise SystemExit(f"{p['id']} duration {p['use_s']} is not exact at {FPS} fps")
        if abs((p["t_out_s"] - p["t_in_s"]) - p["use_s"]) > 0.02:
            raise SystemExit(f"{p['id']} t span != use_s")
        ident = p["id"]
        stem = f"code_graphic_029_{ident}_v01"
        samples = {}
        for frac in (0.18, 0.52, 0.82):
            im = r.frame(p, p["use_s"] * frac)
            mean, p95 = luma(im)
            if mean < 28 and p95 < 50:
                raise SystemExit(f"near-black {ident} @{frac:.0%} mean {mean:.1f} p95 {p95:.1f}")
            im.save(a.out / f"{stem}_{int(frac * 100):02}.jpg", quality=90)
            thumbs.append((p, frac, im.resize((480, 270))))
            samples[f"{frac:.2f}"] = {"mean": round(mean, 1), "p95": round(p95, 1)}
        if not a.previews:
            dest = a.out / f"{stem}.mp4"
            tmp = a.out / f"{stem}.partial.mp4"
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                   "-s", "1920x1080", "-r", str(FPS), "-i", "pipe:0", "-an",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p",
                   "-movflags", "+faststart", str(tmp)]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            try:
                for i in range(frames):
                    proc.stdin.write(r.frame(p, i / FPS).tobytes())
                proc.stdin.close()
                if proc.wait() != 0:
                    raise RuntimeError(f"ffmpeg failed: {ident}")
            except BaseException:
                proc.kill()
                proc.wait()
                raise
            tmp.replace(dest)
            probe = json.loads(subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(dest)]))
            v = probe["streams"][0]
            assert (v["width"], v["height"]) == (W, H)
            assert abs(float(probe["format"]["duration"]) - p["use_s"]) < 0.03
            assert int(v["nb_frames"]) == frames
            records.append(dict(id=ident, file=dest.name, sha256=digest(dest), t_in_s=p["t_in_s"],
                                 t_out_s=p["t_out_s"], use_s=p["use_s"], frames=frames, fps=FPS,
                                 luma=samples, kind="chart", source="own_code", review="pending Chief"))
            print(f"{ident}: {frames} frames / {p['use_s']}s  sha {records[-1]['sha256'][:12]}", flush=True)
        else:
            print(f"preview {ident} luma {samples}", flush=True)
        r.bodies.clear()
    # A partial re-render keeps the other plates' stills on the sheet.
    sheet_thumbs = []
    for p in all_plates:
        stem = f"code_graphic_029_{p['id']}_v01"
        for frac in (0.18, 0.52, 0.82):
            jpg = a.out / f"{stem}_{int(frac * 100):02}.jpg"
            if not jpg.exists():
                continue
            sheet_thumbs.append((p, frac, Image.open(jpg).convert("RGB").resize((480, 270))))
    if not sheet_thumbs:
        sheet_thumbs = thumbs
    rows = (len(sheet_thumbs) + 2) // 3
    sheet = Image.new("RGB", (1440, rows * 300 + 20), (25, 37, 55))
    d = ImageDraw.Draw(sheet)
    for i, (p, frac, thumb) in enumerate(sheet_thumbs):
        x, y = (i % 3) * 480, (i // 3) * 300
        sheet.paste(thumb, (x, y + 8))
        d.text((x + 8, y + 278), f"{p['id']}  {frac:.0%}", font=font(18), fill=WHITE)
    sheet.save(a.out / "CONTACT_SHEET.jpg", quality=90)
    if not a.previews:
        old_path = a.out / "RENDER_MANIFEST.json"
        if want and old_path.exists():
            by_id = {rec["id"]: rec for rec in json.loads(old_path.read_text()).get("renders", [])}
            for rec in records:
                by_id[rec["id"]] = rec
            records = [by_id[p["id"]] for p in all_plates if p["id"] in by_id]
        manifest = dict(job="J0347", film="029", board=boards.name, board_sha256=digest(boards),
                         renderer_sha256=digest(Path(__file__)), fps=FPS, review="pending Chief",
                         fix="Chief 16 Oct: r21 side-view teaspoon (oval bowl, handle along the beam). Earlier KEEP stands.",
                         renders=records)
        old_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("contact sheet written", flush=True)


if __name__ == "__main__":
    main()
