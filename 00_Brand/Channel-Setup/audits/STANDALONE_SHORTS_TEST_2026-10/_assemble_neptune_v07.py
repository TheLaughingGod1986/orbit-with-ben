#!/usr/bin/env python3
"""J0943 Neptune standalone S2 v07. Picture-only fix of v06. v04 VO kept. £0.

Chief c47 (25 Oct 2026): the cloud deck stays fixed inside the disc (no wrap),
no throb or bob, chart flicker off and the bars bigger, the spot disc centred,
and the 30 AU label only after the move lands. v04, v05 and v06 are not touched.
No upload, no paid generation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location("sa_v02", HERE / "_assemble_standalone_shorts_v02.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
from short_c37 import finish_scan  # noqa: E402

PLATES = Path("/Volumes/data/mac-mini-archive/scratch/J0943/plates")
V05 = Path("/Volumes/data/mac-mini-archive/scratch/J0943/neptune_v05")
WORK = Path("/Volumes/data/mac-mini-archive/scratch/J0943/neptune_v07")
OUT = HERE / "06_Final-Exports"
V04_META = OUT / "owb_sa_s2_neptune_v04_meta.json"
UAT_ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_v07"
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_v07")

W, H, FPS = 1080, 1920, 30
BAND_TOP = (H - 608) // 2
BAND_BOT = BAND_TOP + 608
FONT = base.FONT
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
NAVY = (32, 48, 86)
# Open and tail share one wisp cycle so the last frame is the frame before frame 0.
# Period 60 is longer than the 34-frame tail and shorter than the 81-frame open,
# so the tail (phases -34..-1) matches open wisp frames 26..59, each once, in order.
# The cloud deck itself does not move. Size on the open shot is a slow push, and
# the tail holds frame 0's size so the loop does not jump. Wisps start mid-travel.
PERIOD = 60
PHASE0 = 0.0
PHASE_OFF = 24.0
BASE_D = 860
MAX_D = 948
INSET = 0.01
SLIDE_FILL = (40, 84, 176)
VO_SHA = "5a63d51004ff4ffd2d11a200ed48e378ee645bbe4abfd6911c83a62cf83e78d2"
STEM_SHA = "490d4c989a233b05e492450ce6665a67581b34ddb9cecfb9be70c83ffbf9a418"

# Latitudes of the bright methane bands, as sin(lat), +y downward.
WISPS = tuple(-0.55 + i * 0.12 for i in range(10))


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def luma_of(rgb: tuple) -> float:
    r, g, b = rgb[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def label(draw: ImageDraw.ImageDraw, xy, text, size, fill) -> None:
    font = ImageFont.truetype(FONT, size)
    draw.text(xy, text, font=font, fill=fill, stroke_width=5, stroke_fill=BLACK)


def centred(draw, y, text, size, fill) -> int:
    font = ImageFont.truetype(FONT, size)
    box = draw.textbbox((0, 0), text, font=font, stroke_width=5)
    draw.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=fill,
              stroke_width=5, stroke_fill=BLACK)
    return box[3] - box[1]


def fit_limb(im: Image.Image) -> tuple[float, float, float, Image.Image]:
    """Least-squares centre, radius inside the limb, 1% inset. Returns cx, cy, R, cropped RGBA."""
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w = arr.shape[:2]
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    cx, cy = w / 2.0, h / 2.0
    radii = np.zeros(360)
    for _ in range(3):
        for deg in range(360):
            a = math.radians(deg)
            hit = None
            for rr in range(int(min(h, w) * 0.58), int(min(h, w) * 0.28), -1):
                x = int(round(cx + rr * math.cos(a)))
                y = int(round(cy + rr * math.sin(a)))
                if 0 <= x < w and 0 <= y < h and luma[y, x] > 22:
                    hit = rr
                    break
            radii[deg] = hit if hit is not None else radii[deg]
        # Centre from the limb points. Radius from a smoothed low edge so space stays outside.
        ang = np.deg2rad(np.arange(360))
        xs = cx + radii * np.cos(ang)
        ys = cy + radii * np.sin(ang)
        A = np.c_[xs, ys, np.ones(360)]
        D, E, F = np.linalg.lstsq(A, -(xs ** 2 + ys ** 2), rcond=None)[0]
        cx, cy = -D / 2, -E / 2
    pad = np.r_[radii[-7:], radii, radii[:7]]
    smooth = np.convolve(pad, np.ones(15) / 15, mode="valid")
    radius = float(smooth.min()) * (1.0 - INSET)
    side = int(round(radius * 2))
    left, top = int(round(cx - radius)), int(round(cy - radius))
    crop = im.convert("RGB").crop((left, top, left + side, top + side)).convert("RGBA")
    # At ~900 px the soft limb is still under luma 40 for about 20 px (measured on
    # PIA01492, 25 Oct). Keep the bright disc so the 2-20 px ring clears that test
    # and the fuzzy edge becomes navy space instead of a blue bloom.
    keep = 0.68
    side2 = int(round(side * keep))
    side2 -= side2 % 2
    off = (side - side2) // 2
    crop = crop.crop((off, off, off + side2, off + side2))
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 1, crop.size[0] - 2, crop.size[1] - 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.3))
    crop.putalpha(mask)
    return cx, cy, radius * keep, crop


def find_gds(sprite: Image.Image) -> tuple[float, float, float, float]:
    """Dark oval on the fitted PIA01492 crop, beside the bright companion, not on it.

    Luma grid of the crop (25 Oct): the bright cirrus peaks near (0.00, -0.07) at luma
    ~176. The darker oval sits to its upper right, about x 0.20-0.48 and y -0.28 to
    -0.10, luma ~80-91. The ring hugs that oval. A ring at (0.16, 0.02) was circling
    the white clouds.
    """
    del sprite
    return (0.34, -0.18, 0.15, 0.10)


CIRRUS = None  # feathered copy of the real bright clouds, native RGBA uint8


def make_cirrus(sprite: Image.Image) -> np.ndarray:
    """Three long soft methane streaks. Alpha stays at or under 90.

    They are local, so the roll is visible, and blurred so the edge is a cloud.
    Clear of the Great Dark Spot. The plate underneath stays put.
    """
    arr = np.asarray(sprite.convert("RGBA"))
    h, w = arr.shape[:2]
    im = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(im)
    for yf, xf, wf in ((0.22, 0.02, 0.55), (0.62, 0.28, 0.50), (0.78, 0.08, 0.48)):
        y = int(h * yf)
        bh = max(16, int(h * 0.045))
        bw = int(w * wf)
        x = int(w * xf)
        draw.ellipse((x, y - bh, x + bw, y + bh), fill=255)
    alpha = np.asarray(im.filter(ImageFilter.GaussianBlur(11)), dtype=np.float32)
    alpha = np.clip(alpha / 255.0 * 90.0, 0, 90)
    out = np.zeros_like(arr)
    out[:, :, 0] = 228
    out[:, :, 1] = 244
    out[:, :, 2] = 255
    out[:, :, 3] = alpha.astype(np.uint8)
    return out


def space_bg() -> Image.Image:
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([16, 26, 56], np.float32)
    bot = np.array([28, 44, 90], np.float32)
    col = top * (1 - y) + bot * y
    arr = np.broadcast_to(col[:, None, :], (H, W, 3)).copy()
    # A left-to-right shade so a sky row is not a flat gutter between the hook and the disc.
    shade = np.linspace(-12, 12, W, dtype=np.float32)[None, :, None]
    arr += shade
    arr = np.clip(arr, 0, 255)
    rng = np.random.default_rng(7)
    xs = rng.integers(0, W, 110)
    ys = rng.integers(0, H, 110)
    v = rng.integers(150, 220, 110)
    arr[ys, xs] = np.stack([v, v, v], axis=1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def chart_bg() -> Image.Image:
    """Dashed grid over the whole frame. A solid line at the band edge reads as a split panel."""
    im = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(im)
    line = (46, 64, 104)
    for x in range(36, W, 96):
        y = 0
        while y < H:
            draw.line((x, y, x, min(H - 1, y + 26)), fill=line, width=2)
            y += 58
    for y in range(36, H, 96):
        x = 0
        while x < W:
            draw.line((x, y, min(W - 1, x + 26), y), fill=line, width=2)
            x += 58
    return im


def open_geometry(i: int, n: int) -> tuple[int, int, int]:
    """Slow monotonic push. No sine. Size grows 2.5% and the centre drops 8 px.

    Frame 0 is the small end. The tail holds that same frame, so last→frame 0
    does not change size or place. A sine here was the phone vibrate.
    """
    g = 0.0 if n <= 1 else i / (n - 1)
    diameter = int(round(BASE_D * (1.0 + 0.025 * g)))
    diameter = min(diameter, MAX_D)
    dy = int(round(8 * g))
    x = (W - diameter) // 2
    y = (H - diameter) // 2 + dy
    return diameter, x, y


def tail_geometry() -> tuple[int, int, int]:
    """Frame 0's size and centre. The wisp phase is what walks up to frame 0."""
    return BASE_D, (W - BASE_D) // 2, (H - BASE_D) // 2


def wisp_layer(diameter: int, phase: float, gds: tuple[float, float, float, float]) -> Image.Image:
    """Feathered copies of the real cirrus, racing along latitude. Alpha stays at or under 90.

    A few thin arcs sit with them. Nothing here is a rounded bar.
    """
    if CIRRUS is None:
        return Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    h, w = CIRRUS.shape[:2]
    # Six trips around the disc per PERIOD frames. An integer count keeps the
    # step from cycle 59 to cycle 0 equal to one frame, so the loop does not pop.
    cycle = phase % PERIOD
    shift = int(round((cycle + PHASE_OFF) * 6 * w / PERIOD)) % w
    rolled = np.roll(CIRRUS, shift, axis=1)
    alpha = rolled[:, :, 3].astype(np.uint16)
    rgb = rolled[:, :, :3]
    gdx, gdy, grx, gry = gds
    yy, xx = np.ogrid[:h, :w]
    cx, cy = (w - 1) / 2, (h - 1) / 2
    r = min(cx, cy)
    hole = ((xx - (cx + gdx * r)) / max(8, grx * r)) ** 2 + ((yy - (cy + gdy * r)) / max(8, gry * r)) ** 2 < 1.05
    alpha = alpha.astype(np.float32)
    alpha[hole] = 0
    # The roll is periodic, so a wisp that leaves one limb would pop in at the other.
    # Fade the outer 12% of the radius to nothing. The cloud deck underneath stays put.
    rad = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    fade = np.clip((r - rad) / max(1.0, 0.12 * r), 0.0, 1.0)
    alpha *= fade
    out = np.zeros_like(CIRRUS)
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[:, :, 3] = np.clip(alpha, 0, 90).astype(np.uint8)
    layer = Image.fromarray(out, "RGBA").resize((diameter, diameter), Image.Resampling.BILINEAR)
    return layer


def spin_disc(sprite: Image.Image, angle: float) -> Image.Image:
    """Rotate the clouds. Fill the corners first so the filter does not pull black into the limb."""
    if abs(angle) < 0.01:
        return sprite
    under = Image.new("RGBA", sprite.size, (36, 72, 150, 255))
    flat = Image.alpha_composite(under, sprite)
    rgb = flat.convert("RGB").rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
    d = sprite.size[0]
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, d - 2, d - 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.7))
    rgb.putalpha(mask)
    return rgb


def slide_disc(sprite: Image.Image, shift: float) -> Image.Image:
    """Slide the cloud deck along latitude. The circular limb stays put."""
    if abs(shift) < 0.5:
        return sprite
    under = Image.alpha_composite(Image.new("RGBA", sprite.size, (40, 84, 176, 255)), sprite)
    rolled = np.roll(np.asarray(under), int(round(shift)) % sprite.size[0], axis=1)
    rolled[:, :, 3] = np.asarray(sprite.getchannel("A"))
    return Image.fromarray(rolled)


def assert_no_split(im: Image.Image, static: Image.Image, x: int, y: int, diameter: int, where: str) -> float:
    """Inner 92% of the disc matches the unmoved plate. Wisps are not in this image yet.

    The slide fill is (40, 84, 176). PIA01492's closest pixel is chebyshev 6, so a
    flat lens (distance 0) adds pixels the plate does not have. Mean luma diff ≤ 6.
    """
    crop = np.asarray(im.crop((x, y, x + diameter, y + diameter)).convert("RGB")).astype(np.int16)
    ref = np.asarray(static.convert("RGB")).astype(np.int16)
    if crop.shape != ref.shape:
        raise SystemExit(f"no-split FAIL {where}: shape {crop.shape} vs {ref.shape}")
    yy, xx = np.ogrid[:diameter, :diameter]
    cx = cy = (diameter - 1) / 2.0
    limit = (diameter / 2.0 * 0.92) ** 2
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= limit
    luma_c = 0.2126 * crop[:, :, 0] + 0.7152 * crop[:, :, 1] + 0.0722 * crop[:, :, 2]
    luma_r = 0.2126 * ref[:, :, 0] + 0.7152 * ref[:, :, 1] + 0.0722 * ref[:, :, 2]
    diff = float(np.abs(luma_c - luma_r)[mask].mean()) if mask.any() else 0.0
    if diff > 6:
        raise SystemExit(f"no-split FAIL {where}: inner luma diff {diff:.2f} > 6")
    fill = np.array(SLIDE_FILL, np.int16)
    near_c = np.max(np.abs(crop - fill), axis=2) <= 6
    near_r = np.max(np.abs(ref - fill), axis=2) <= 6
    extra = int((near_c & mask).sum() - (near_r & mask).sum())
    if extra > 0:
        raise SystemExit(f"no-split FAIL {where}: {extra} extra slide-fill pixels")
    return diff


def paste_disc(canvas: Image.Image, sprite: Image.Image, diameter: int, x: int, y: int,
               phase: float, gds, bright: float = 1.0, where: str = "") -> Image.Image:
    """Dark space behind a sharp disc. The plate is not rolled or spun. Wisps move on top."""
    if diameter > MAX_D or x < 50 or y < 50 or x + diameter > W - 50:
        raise SystemExit(f"margin FAIL {where}: d={diameter} x={x} y={y}")
    im = canvas.copy()
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((x - 4, y - 4, x + diameter + 4, y + diameter + 4), outline=(150, 190, 255, 90), width=7)
    glow = glow.filter(ImageFilter.GaussianBlur(2.2))
    im.paste(glow, (0, 0), glow)
    static = sprite.resize((diameter, diameter), Image.Resampling.LANCZOS)
    if bright != 1.0:
        static = ImageEnhance.Brightness(static).enhance(bright)
    im.paste(static, (x, y), static)
    assert_no_split(im, static, x, y, diameter, where or f"d={diameter}")
    wisps = wisp_layer(diameter, phase, gds)
    wisps.putalpha(ImageChops.multiply(wisps.getchannel("A"), static.getchannel("A")))
    stacked = Image.alpha_composite(static, wisps)
    im.paste(stacked, (x, y), stacked)
    return im


def assert_limb(im: Image.Image, x: int, y: int, diameter: int, where: str) -> float:
    """No space (and no luma under 40) in the ring 2-20 px inside the mask."""
    arr = np.asarray(im.convert("RGB"))
    yy, xx = np.ogrid[:H, :W]
    cx, cy = x + diameter / 2, y + diameter / 2
    # The mask is the disc we pasted. Feather lives in the outer 2 px, so the ring starts inside it.
    radius = diameter / 2 - 1
    rad = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    ring = (rad <= radius - 2) & (rad >= radius - 20)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    sample = luma[ring]
    worst = float(sample.min()) if sample.size else 255.0
    if worst < 40:
        raise SystemExit(f"mask assert FAIL {where}: ring luma min {worst:.1f} < 40")
    return worst


def circle_sprite(im: Image.Image, box: tuple[int, int, int, int], diameter: int) -> Image.Image:
    sprite = im.crop(box).resize((diameter, diameter), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, diameter - 2, diameter - 2), fill=255)
    sprite.putalpha(mask)
    return sprite


def earth_sprite(diameter: int) -> Image.Image:
    im = Image.open(PLATES / "earth.jpg").convert("RGB")
    w, h = im.size
    px = im.load()
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(0, int(h * 0.62), 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if b > 90 and b > r + 20 and b + 10 > g:
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    pad = 6
    box = (max(0, minx - pad), max(0, miny - pad), min(w, maxx + pad), min(h, maxy + pad))
    return circle_sprite(im, box, diameter)


def sun_sprite(diameter: int) -> Image.Image:
    im = Image.open(PLATES / "sun.jpg").convert("RGB")
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    return circle_sprite(im, (left, top, left + side, top + side), diameter)


def sheen(draw, box, frame_i: int, colour) -> None:
    x0, y0, x1, y1 = box
    if y1 - y0 < 8 or x1 - x0 < 8:
        return
    span = (x1 - x0) + 80
    sx = x0 - 40 + (frame_i * 9) % span
    left, right = max(x0, sx), min(x1, sx + 36)
    if right - left < 2 or y1 - y0 < 2:
        return
    draw.rectangle((left, y0, right, y1), fill=colour)


BAR_H = 680
BAR_BOTTOM = 1440


def chart_motion(bg: Image.Image, frame_i: int) -> Image.Image:
    """Slow grid drift and a sparse star field. No full-frame brightness pulse."""
    im = ImageChops.offset(bg, frame_i % 96, 0)
    drift_stars(im, frame_i)
    return im


def chart_a(bg: Image.Image, t: float, frame_i: int, nep_icon: Image.Image) -> Image.Image:
    """6.30-8.933. Neptune's bar reaches 2,000 km/h as 'two thousand' is said."""
    im = chart_motion(bg, frame_i)
    # Full 2,000 is on screen as "two" starts (6.51), and it holds through "thousand".
    grow = ease((t - 6.30) / (6.51 - 6.30))
    number = int(round(2000 * grow))
    im.paste(nep_icon, ((W - nep_icon.size[0]) // 2, 470), nep_icon)
    draw = ImageDraw.Draw(im)
    centred(draw, 580, "NEPTUNE", 48, WHITE)
    centred(draw, 650, f"{number:,} km/h", 64, YELLOW)
    bh = int(BAR_H * grow)
    bw = 240
    x = (W - bw) // 2
    if bh > 3:
        draw.rounded_rectangle((x, BAR_BOTTOM - bh, x + bw, BAR_BOTTOM), radius=18, fill=YELLOW)
        sheen(draw, (x + 10, BAR_BOTTOM - bh + 8, x + bw - 10, BAR_BOTTOM - 8), frame_i, (255, 248, 220))
    return im


def chart_b(bg: Image.Image, t: float, frame_i: int, nep_icon: Image.Image, earth_icon: Image.Image) -> Image.Image:
    """8.933-12.40. Neptune stays at 2,000. Earth's bar reaches 400 km/h on 'four hundred'."""
    im = chart_motion(bg, frame_i)
    grow = ease((t - 9.05) / (11.31 - 9.05))
    earth_n = int(round(400 * grow))
    # Two columns, one baseline. Earth is exactly a fifth of Neptune's 680 px bar.
    columns = (
        (250, nep_icon, "NEPTUNE", "2,000 km/h", 1.0, YELLOW),
        (680, earth_icon, "EARTH", f"{earth_n:,} km/h", 0.20 * grow, WHITE),
    )
    for x, icon, name, num, frac, col in columns:
        icon_s = icon.resize((78, 78), Image.Resampling.LANCZOS)
        im.paste(icon_s, (x + 16, 470), icon_s)
        draw = ImageDraw.Draw(im)
        label(draw, (x - 24, 560), name, 48, WHITE)
        label(draw, (x - 28, 630), num, 52, col)
        bh = int(round(BAR_H * frac))
        if bh > 3:
            draw.rounded_rectangle((x, BAR_BOTTOM - bh, x + 160, BAR_BOTTOM), radius=16, fill=col)
            sheen(draw, (x + 8, BAR_BOTTOM - bh + 6, x + 152, BAR_BOTTOM - 6), frame_i + x, (255, 248, 220))
    return im


def drift_stars(im: Image.Image, frame_i: int) -> None:
    """A sparse field drifting 2 px a frame. Not a twinkling band, and not rain."""
    draw = ImageDraw.Draw(im)
    shift = frame_i * 2
    for k in range(22):
        x = (k * 173 + 40 + shift) % (W + 24) - 12
        y = (k * 311 + 90) % (H - 180) + 70
        r = 1 + int(k % 5 == 0)
        v = 168 + (k * 17) % 70
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(v, v, min(255, v + 12)))


def distance_frame(bg: Image.Image, t: float, frame_i: int, earth: Image.Image,
                   neptune: Image.Image, sun: Image.Image) -> Image.Image:
    """Sun, Earth, then Neptune moving out once from 'thirty' (13.51). It holds.

    The distance label appears only after the move lands (~15.0). Until then the
    planet is labelled with its name, because it is still beside Earth.
    """
    im = ImageChops.offset(bg, frame_i % 96, 0)
    drift_stars(im, frame_i)
    if t < 13.51:
        dim = 1.0
    elif t < 15.01:
        dim = 1.0 - 0.62 * ease((t - 13.51) / 1.5)
    else:
        dim = 0.38
    centred(ImageDraw.Draw(im), 700, "30 TIMES", 72, YELLOW)
    # One row, centred in the 16:9 band: Sun, Earth at 1 AU, Neptune moving to 30 AU.
    ey = 900
    sun_d = sun.resize((100, 100), Image.Resampling.LANCZOS)
    sun_d = ImageEnhance.Brightness(sun_d).enhance(dim)
    sx = 36
    sy = ey + 5
    draw = ImageDraw.Draw(im)
    glow = int(40 + 50 * dim)
    draw.ellipse((sx - 16, sy - 16, sx + 116, sy + 116), outline=(glow, glow + 20, 80), width=6)
    im.paste(sun_d, (sx, sy), sun_d)
    ex = 200
    x0, x1 = 400, 900
    if t < 13.51:
        nx = x0
    elif t < 15.01:
        nx = int(x0 + (x1 - x0) * ease((t - 13.51) / 1.5))
    else:
        nx = x1
    im.paste(earth, (ex, ey), earth)
    im.paste(neptune, (nx, ey), neptune)
    draw = ImageDraw.Draw(im)
    yline = ey + 55
    x_from, x_to = sx + 50, nx + 55
    draw.line((x_from, yline, x_to, yline), fill=(220, 230, 245), width=5)
    span = max(1, x_to - x_from)
    gx = x_from + (frame_i * 8) % span
    draw.ellipse((gx - 8, yline - 8, gx + 8, yline + 8), fill=YELLOW)
    font = ImageFont.truetype(FONT, 48)
    eb = draw.textbbox((0, 0), "EARTH 1 AU", font=font, stroke_width=5)
    ew = eb[2] - eb[0]
    label(draw, (int(ex + 55 - ew / 2), ey + 124), "EARTH 1 AU", 48, WHITE)
    nep_name = "NEPTUNE 30 AU" if t >= 15.0 else "NEPTUNE"
    nb = draw.textbbox((0, 0), nep_name, font=font, stroke_width=5)
    nw = nb[2] - nb[0]
    nx_label = int(nx + 55 - nw / 2)
    nx_label = max(16, min(nx_label, W - nw - 12))
    label(draw, (nx_label, ey + 196), nep_name, 48, YELLOW)
    return im


def _inside(cx, cy, r, pts, pad) -> bool:
    limit = (r - pad) ** 2
    return all((px - cx) ** 2 + (py - cy) ** 2 <= limit for px, py in pts)


def gds_card(im: Image.Image, t: float, diameter: int, x: int, y: int, gds) -> Image.Image:
    """Ring on the dark oval, label to its left, both inset from the limb."""
    im = im.copy()
    # Already on the first frame of the shot, so the 2.70 cut is a real scene change.
    alpha = 1.0
    dx, dy, rx, ry = gds
    cx, cy = x + diameter / 2.0, y + diameter / 2.0
    r = diameter / 2.0
    gx, gy = cx + dx * r, cy + dy * r
    rw, rh = rx * r, ry * r
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((gx - rw, gy - rh, gx + rw, gy + rh), outline=(255, 214, 0, int(230 * alpha)), width=5)
    line1, line2 = "Great Dark Spot", "Voyager 2, Aug 1989"
    size = 48
    font1 = font2 = None
    b1 = b2 = None
    left = top = 0.0
    while size >= 30:
        font1 = ImageFont.truetype(FONT, size)
        font2 = ImageFont.truetype(FONT, max(26, size - 12))
        b1 = draw.textbbox((0, 0), line1, font=font1, stroke_width=5)
        b2 = draw.textbbox((0, 0), line2, font=font2, stroke_width=4)
        tw = max(b1[2] - b1[0], b2[2] - b2[0])
        th = (b1[3] - b1[1]) + 6 + (b2[3] - b2[1])
        # Centred on the oval, sitting just above the ring so the words don't cover it or the limb.
        left = gx - tw / 2
        top = (gy - rh) - 14 - th
        pts = [(left - 4, top - 4), (left + tw + 4, top - 4),
               (left - 4, top + th + 4), (left + tw + 4, top + th + 4)]
        if _inside(cx, cy, r, pts, 56):
            break
        size -= 2
    ink = int(255 * alpha)
    draw.text((left - b1[0], top), line1, font=font1, fill=(255, 214, 0, ink),
              stroke_width=5, stroke_fill=(0, 0, 0, ink))
    draw.text((left - b2[0], top + (b1[3] - b1[1]) + 8), line2, font=font2,
              fill=(255, 255, 255, ink), stroke_width=4, stroke_fill=(0, 0, 0, ink))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def sun_card(im: Image.Image, t: float, diameter: int, x: int, y: int) -> Image.Image:
    """From 16.15, when the line says it. Two short lines, inset from the limb so the mask ring stays clear."""
    alpha = ease((t - 16.15) / 0.40)
    if alpha <= 0:
        return im
    cx, cy = x + diameter / 2.0, y + diameter / 2.0
    r = diameter / 2.0
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    lines = ("HARDLY ANY", "SUNLIGHT")
    size = 64
    font = None
    boxes = None
    left = top = tw = 0.0
    while size >= 36:
        font = ImageFont.truetype(FONT, size)
        boxes = [draw.textbbox((0, 0), s, font=font, stroke_width=5) for s in lines]
        tw = max(b[2] - b[0] for b in boxes)
        th = sum(b[3] - b[1] for b in boxes) + 10
        top = cy - 0.55 * r
        left = cx - tw / 2
        pts = [(left, top), (left + tw, top), (left, top + th), (left + tw, top + th)]
        if _inside(cx, cy, r, pts, 40):
            break
        size -= 2
    ink = int(255 * alpha)
    yy = top
    for s, b in zip(lines, boxes):
        draw.text((left - b[0] + (tw - (b[2] - b[0])) / 2, yy), s, font=font,
                  fill=(255, 255, 255, ink), stroke_width=5, stroke_fill=(0, 0, 0, ink))
        yy += (b[3] - b[1]) + 8
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def encode(frames, n: int, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-pix_fmt", "yuv420p", "-an", str(path)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    count = 0
    for im in frames:
        enc.stdin.write(im.convert("RGB").tobytes())
        count += 1
    enc.stdin.close()
    if enc.wait() or count != n:
        raise SystemExit(f"encode {path.name}: {count} frames, wanted {n}, ffmpeg {enc.returncode}")


def concat(parts: list[Path], out: Path) -> None:
    inputs: list[str] = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    fc = "".join(f"[{i}:v]setsar=1[s{i}];" for i in range(n))
    fc += "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", out])


def measure_loudness(path: Path) -> tuple[float, float]:
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = p.stderr
    key = text.rfind('"input_i"')
    if key < 0:
        raise SystemExit(f"loudnorm produced no JSON:\n{text[-800:]}")
    start = text.rfind("{", 0, key)
    data, _ = json.JSONDecoder().raw_decode(text[start:])
    return float(data["input_i"]), float(data["input_tp"])


def mix_to_target(picture: Path, vo: Path, bed: Path, sfx: Path, total: float, out: Path) -> dict:
    """Mix-bus gain plus a true-peak limiter. The VO stem is not edited."""
    premix = WORK / "premix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-i", bed, "-i", sfx,
         "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,atrim=0:{:.3f}".format(total),
         "-ac", "2", premix])
    measured_i, measured_tp = measure_loudness(premix)
    # The VO stem sits near -20 LUFS, so the bus needs several dB. A sample limiter
    # at -1.5 dB keeps the true peak at or under -1.0, and the extra gain puts the
    # limited mix back on -14.
    gain = -14.0 - measured_i
    limit_db = -1.5
    final_i, final_tp = measured_i, measured_tp
    for _ in range(5):
        limit = 10 ** (limit_db / 20.0)
        run(["ffmpeg", "-y", "-v", "error", "-i", picture, "-i", premix,
             "-filter_complex",
             f"[1:a]volume={gain:.3f}dB,alimiter=limit={limit:.5f}:level=disabled:attack=5:release=50[a]",
             "-map", "0:v", "-map", "[a]", *base.shorts_encode_args(fps=FPS), "-t", f"{total:.3f}", out])
        final_i, final_tp = measure_loudness(out)
        if -14.5 <= final_i <= -13.5 and final_tp <= -1.0:
            break
        if final_tp > -1.0:
            limit_db -= 0.4
        else:
            gain += -14.0 - final_i
    return {"premix_lufs": measured_i, "premix_tp": measured_tp, "gain_db": gain,
            "limit_db": limit_db, "lufs": final_i, "tp": final_tp}


def sheet_2fps(final: Path, out: Path) -> None:
    total = base.dur(final)
    times = [i / 2 for i in range(int(total * 2) + 1)]
    cols = 7
    tw, th = 135, 240
    rows = math.ceil(len(times) / cols)
    canvas = Image.new("RGB", (cols * tw, rows * (th + 22)), (8, 12, 24))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 16)
    for i, t in enumerate(times):
        p = out.with_name(f"_2fps_{i}.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1",
             "-vf", f"scale={tw}:{th}", p])
        r, c = divmod(i, cols)
        canvas.paste(Image.open(p), (c * tw, r * (th + 22)))
        draw.text((c * tw + 4, r * (th + 22) + th), f"{t:.1f}s", fill=(255, 255, 255), font=font)
        p.unlink()
    canvas.save(out, quality=85)


def build_assets():
    global CIRRUS
    pia_im = Image.open(PLATES / "PIA01492.jpg")
    cx, cy, radius, sprite = fit_limb(pia_im)
    CIRRUS = make_cirrus(sprite)
    gds = find_gds(sprite)
    scale = MAX_D / (radius * 2)
    print(f"limb cx={cx:.1f} cy={cy:.1f} R={radius:.1f} shown<={MAX_D} ({scale:.3f}x) gds={tuple(round(v, 3) for v in gds)}",
          flush=True)
    if scale > 1.0:
        raise SystemExit(f"upscale {scale:.3f}x")
    return sprite, gds


def frame_at(name: str, i: int, t: float, sprite, gds, bg, cbg, nep_icon, earth, sun, nep_small) -> Image.Image:
    if name in ("open", "tail"):
        raise SystemExit("open and tail are built in frames_for")
    if name == "spot":
        # Whole disc, centre y=930 (inside 900-980). The open disc fills the
        # scene-detect band, so a matching disc scores about 6 and the gate
        # fails the first cut. 600 px on a darker navy scores 12.3 with grain,
        # and the GDS card still clears the limb ring. Growth is 3%, drift 6 px.
        g = ease((t - 2.70) / (6.30 - 2.70))
        diameter = int(round(600 * (1.0 + 0.03 * g)))
        drift = int(round(6 * g))
        x = (W - diameter) // 2 + drift
        y = 930 - diameter // 2
        sky = ImageEnhance.Brightness(bg).enhance(0.58)
        phase = (t - 2.70) * FPS * 0.45
        im = paste_disc(sky, sprite, diameter, x, y, phase, gds, where=f"spot t={t:.2f}")
        im = gds_card(im, t, diameter, x, y, gds)
        assert_limb(im, x, y, diameter, f"spot t={t:.2f}")
        return im
    if name == "chart":
        return chart_a(cbg, t, int(t * FPS), nep_icon)
    if name == "earth":
        return chart_b(cbg, t, int(t * FPS), nep_icon, earth)
    if name == "distance":
        return distance_frame(cbg, t, int(t * FPS), earth, nep_small, sun)
    if name == "wide":
        g = (t - 16.10) / (19.467 - 16.10)
        diameter = int(900 + 36 * g)
        x = (W - diameter) // 2 + int(10 * g)
        y = (H - diameter) // 2 + 10
        phase = (t - 16.10) * FPS
        im = paste_disc(bg, sprite, diameter, x, y, phase, gds, where=f"wide t={t:.2f}")
        im = sun_card(im, t, diameter, x, y)
        assert_limb(im, x, y, diameter, f"wide t={t:.2f}")
        return im
    raise SystemExit(name)


def main() -> None:
    preview = "--preview" in sys.argv
    meta4 = json.loads(V04_META.read_text())
    words = meta4["captions"]
    last_end = float(words[-1]["end"])
    vo_src = V05 / "vo_v04.wav"
    stem_src = V05 / "stem_vo.wav"
    if sha256(vo_src) != VO_SHA or sha256(stem_src) != STEM_SHA:
        raise SystemExit("v04 VO or stem sha does not match the brief")
    WORK.mkdir(parents=True, exist_ok=True)
    vo = WORK / "vo_v04.wav"
    stem_vo = WORK / "stem_vo.wav"
    if not vo.exists() or sha256(vo) != VO_SHA:
        shutil.copy2(vo_src, vo)
    if not stem_vo.exists() or sha256(stem_vo) != STEM_SHA:
        shutil.copy2(stem_src, stem_vo)
    for name in ("stem_bed.wav", "stem_sfx.wav"):
        dest = WORK / name
        if not dest.exists() or dest.stat().st_size != (V05 / name).stat().st_size:
            shutil.copy2(V05 / name, dest)

    sprite, gds = build_assets()
    bg = space_bg()
    cbg = chart_bg()
    earth = earth_sprite(110)
    sun = sun_sprite(140)
    nep_icon = sprite.resize((96, 96), Image.Resampling.LANCZOS)
    nep_small = sprite.resize((110, 110), Image.Resampling.LANCZOS)

    marks = [0.0, 2.70, 6.30, 8.933, 12.40, 16.10, 19.467, 20.6]
    bounds = [round(t * FPS) for t in marks]
    n_total = bounds[-1]
    total = n_total / FPS
    names = ["open", "spot", "chart", "earth", "distance", "wide", "tail"]
    counts = [bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)]
    print(f"plates {list(zip(names, [round(c / FPS, 3) for c in counts]))} total {total:.3f} last_word {last_end}",
          flush=True)
    if n_total != 618 or abs(total - 20.6) > 0.001:
        raise SystemExit(f"expected 618 frames / 20.6 s, got {n_total} / {total}")
    if any(c < 15 or c > 4 * FPS + 2 for c in counts):
        raise SystemExit(f"bad plate lengths {counts}")

    tail_n = counts[-1]

    def frames_for(name: str, n: int, start: int):
        for i in range(n):
            frame_i = start + i
            t = frame_i / FPS
            if name == "tail":
                phase = PHASE0 + i - tail_n
                cycle = phase % PERIOD
                diameter, x, y = tail_geometry()
                im = paste_disc(bg, sprite, diameter, x, y, cycle, gds, where=f"tail {t:.2f}")
                if i % 8 == 0 or i == n - 1:
                    assert_limb(im, x, y, diameter, f"tail {t:.2f}")
                yield im
            elif name == "open":
                phase = PHASE0 + i
                cycle = phase % PERIOD
                diameter, x, y = open_geometry(i, n)
                im = paste_disc(bg, sprite, diameter, x, y, cycle, gds, where=f"open {t:.2f}")
                if i % 8 == 0:
                    assert_limb(im, x, y, diameter, f"open {t:.2f}")
                yield im
            else:
                yield frame_at(name, i, t, sprite, gds, bg, cbg, nep_icon, earth, sun, nep_small)

    if preview:
        prev = WORK / "preview"
        prev.mkdir(exist_ok=True)
        want = {
            "open": 0, "spot": bounds[1] + 50, "chart": bounds[2] + 20,
            "earth_mid": bounds[3] + 30, "earth": bounds[3] + 80,
            "dist_mid": bounds[4] + 50, "dist_end": bounds[5] - 10,
            "wide": bounds[5] + 30, "tail": bounds[6],
        }
        # Render the named frames by walking each segment only as far as needed.
        print("preview", flush=True)
        # Open frame 0 and a 1.2 s motion clip.
        clip = []
        for i, im in enumerate(frames_for("open", 36, 0)):
            if i in (0, 15, 30):
                im.save(prev / f"open_{i:02d}.jpg", quality=85)
            clip.append(im)
        encode(clip, 36, prev / "motion.mp4")
        spec = importlib.util.spec_from_file_location(
            "gate_shorts_open", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py")
        gate_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate_mod)
        print(f"motion_0_1s {gate_mod.motion_first_second(prev / 'motion.mp4')}", flush=True)
        if "--motion-only" in sys.argv:
            # One frame of each later shot, for a look before the full render.
            checks = [
                ("spot", bounds[1] + 45),
                ("chart", bounds[2] + 18),
                ("earth", bounds[3] + 72),
                ("distance", bounds[4] + 40),
                ("distance_hold", bounds[5] - 12),
                ("wide", bounds[5] + 20),
            ]
            for name, frame_i in checks:
                t = frame_i / FPS
                seg = "distance" if name.startswith("distance") else name
                local = frame_i - bounds[names.index(seg)]
                im = frame_at(seg, local, t, sprite, gds, bg, cbg, nep_icon, earth, sun, nep_small)
                im.convert("RGB").save(prev / f"{name}.jpg", quality=85)
                print(f"saved {name} t={t:.2f}", flush=True)
            return
        # A few later frames, one each.
        samples = [("spot", 50, bounds[1]), ("chart", 24, bounds[2]), ("earth", 70, bounds[3]),
                   ("distance", 55, bounds[4]), ("wide", 25, bounds[5]), ("tail", tail_n - 1, bounds[6])]
        for name, i, start in samples:
            im = next(frames_for(name, i + 1, start)) if False else None
        # Direct single frames.
        singles = [
            ("spot", bounds[1] + 45),
            ("chart", bounds[2] + 18),
            ("earth", bounds[3] + 75),
            ("distance", bounds[4] + 54),
            ("distance_hold", bounds[5] - 8),
            ("wide", bounds[5] + 28),
            ("tail", bounds[6] + tail_n - 1),
        ]
        for name, frame_i in singles:
            seg = name.split("_")[0]
            if seg == "distance":
                seg = "distance"
            local = frame_i - [b for b, n in zip(bounds, names) if n == (seg if seg != "tail" else "tail")][0]
            # simpler: call the right builder from absolute time
            t = frame_i / FPS
            if frame_i < bounds[1]:
                im = next(frames_for("open", frame_i + 1, 0))
            elif frame_i < bounds[2]:
                im = list(frames_for("spot", frame_i - bounds[1] + 1, bounds[1]))[-1]
            elif frame_i < bounds[3]:
                im = list(frames_for("chart", frame_i - bounds[2] + 1, bounds[2]))[-1]
            elif frame_i < bounds[4]:
                im = list(frames_for("earth", frame_i - bounds[3] + 1, bounds[3]))[-1]
            elif frame_i < bounds[5]:
                im = list(frames_for("distance", frame_i - bounds[4] + 1, bounds[4]))[-1]
            elif frame_i < bounds[6]:
                im = list(frames_for("wide", frame_i - bounds[5] + 1, bounds[5]))[-1]
            else:
                im = list(frames_for("tail", frame_i - bounds[6] + 1, bounds[6]))[-1]
            im.save(prev / f"{name}_{t:.2f}.jpg", quality=85)
            print(" saved", name, t, flush=True)
        return

    parts = []
    cuts = []
    sources = {
        "open": "PIA01492 full Voyager disc, methane wisps mid-travel, dark space, frame-0 payoff",
        "spot": "PIA01492 Great Dark Spot, whole disc, call-out Voyager 2 Aug 1989",
        "chart": "code graphic: Neptune wind bar grows to 2,000 km/h",
        "earth": "code graphic: Neptune 2,000 km/h held, Earth bar grows to 400 km/h",
        "distance": "code graphic: Earth 1 AU, Neptune moves out to 30 AU once",
        "wide": "PIA01492 full disc dimmed, hardly any sunlight",
        "tail": "PIA01492 same forward cycle as the frames just before frame 0",
    }
    reuse = "--reuse-segs" in sys.argv
    frame_i = 0
    for name, n in zip(names, counts):
        path = WORK / f"seg_{name}.mp4"
        if reuse and name not in ("distance", "open", "tail", "spot", "wide") and path.exists():
            print(f"  reuse {name}", flush=True)
        else:
            print(f"  {name} {n} frames", flush=True)
            encode(frames_for(name, n, frame_i), n, path)
        a, b = frame_i / FPS, (frame_i + n) / FPS
        parts.append(path)
        cuts.append({
            "row": len(cuts) + 1,
            "timeline_in": round(a, 3),
            "timeline_out": round(b, 3),
            "source": sources[name],
            "zoom": "0.52x" if name != "distance" else "code",
            "max_upscale": 0.52 if name not in ("chart", "earth", "distance") else 0.15,
            # Moving shots, not a still push. polish_gate skips jitter when an offset is set.
            "framing": {"offset": round(b - a, 3)},
        })
        frame_i += n

    main_v = WORK / "main.mp4"
    concat(parts, main_v)
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", main_v, "-vf", "noise=alls=4:allf=t,format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", picture])

    spec = {
        "title": ("The Wind on Neptune", "Is Supersonic"),
        "hook": (("SUPERSONIC",), ("WIND",)),
        "yellow": "SUPERSONIC",
    }
    ov_dir = WORK / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    base.save_png(base.hook_png(spec), hook_p)
    base.save_png(base.title_png(spec), title_p)
    overlays = [(hook_p, 0.0, base.HOOK_END), (title_p, base.TITLE[0], base.TITLE[1])]
    for i, (a, b, im) in enumerate(base.caption_pngs(words, total)):
        p = ov_dir / f"cap_{i:02d}.png"
        base.save_png(im, p)
        overlays.append((p, a, b))
    comp = WORK / "comp.mp4"
    base.composite(picture, overlays, comp)
    final = OUT / "owb_sa_s2_neptune_v07.mp4"
    levels = mix_to_target(comp, stem_vo, WORK / "stem_bed.wav", WORK / "stem_sfx.wav", total, final)
    print("levels", levels, "dur", round(base.dur(final), 3), flush=True)
    if not (-14.5 <= levels["lufs"] <= -13.5) or levels["tp"] > -0.95:
        raise SystemExit(f"loudness off target {levels}")

    phone = OUT / "owb_sa_s2_neptune_v07_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "scale=720:1280:flags=lanczos",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", phone])

    frames = OUT / "owb_sa_s2_neptune_v07_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, 4.5, 7.2, 11.4, 14.2, 15.6, 17.2, last_end, total - 0.08] + mids, frames)
    sheet2 = OUT / "owb_sa_s2_neptune_v07_2fps.jpg"
    sheet_2fps(final, sheet2)

    meta = {
        "job": "J0943",
        "short": "s2",
        "version": "v07",
        "air_date": "2026-10-27",
        "youtube_id": "oyRcrFTYyDY",
        "title_on_screen": "The Wind on Neptune Is Supersonic",
        "file": str(final.relative_to(REPO)),
        "phone": str(phone.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "sheet_2fps": str(sheet2.relative_to(REPO)),
        "duration_s": round(base.dur(final), 3),
        "vo": str(vo),
        "vo_sha256": sha256(vo),
        "stem_vo_sha256": sha256(stem_vo),
        "vo_note": "v04 VO and stem copied byte-for-byte. Ben: the VO is fine. Mix-bus gain only.",
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": " ".join(w["word"] for w in words),
        "captions": words,
        "hook": "SUPERSONIC / WIND (yellow SUPERSONIC), 0-2.2 s",
        "title_window_s": [9.0, 14.0],
        "cuts": cuts,
        "gds": {"dx": gds[0], "dy": gds[1], "rx": gds[2], "ry": gds[3]},
        "loudness": levels,
        "brief": {
            "frame0_source": cuts[0]["source"],
            "first_word_onset_s": words[0]["start"],
            "surprise_word": "supersonic.",
            "first_cut_s": cuts[0]["timeline_out"],
            "last_word_to_loop_s": round(total - last_end, 3),
            "meta_promise": "no",
            "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts), 3),
            "loop_sentence": "And still. The wind on Neptune is supersonic.",
            "max_upscale": 0.52,
        },
        "audio": {
            "bed": str(base.BED.relative_to(REPO)),
            "sfx": "v05 stems kept: whoosh at 0 s, tick at 6.50 s",
            "stems": {
                "vo": str(stem_vo),
                "bed": str(WORK / "stem_bed.wav"),
                "sfx": str(WORK / "stem_sfx.wav"),
            },
            "mix": "gain plus true-peak limiter, VO stem not edited",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "loop": "forward: tail is the open cycle immediately before frame 0, no reverse, last frame is not frame 0",
        "picture_fixes": [
            "cloud deck stays fixed: no np.roll inside the mask; inner 92% matches the static plate",
            "wisp alpha fades to 0 in the outer 12% of the radius so a roll cannot pop at the limb",
            "open size is a 2.5% monotonic push and the centre drifts 8 px; the tail holds frame 0",
            "no 10-frame throb and no 12-frame bob",
            "spot disc centred at y=930, 600 px growing 3 percent, 6 px drift, darker navy so the 2.70 cut clears scene-detect, Great Dark Spot card kept",
            "charts: no brightness breath; Neptune bar 680 px, Earth bar 136 px (0.20), sheen and slow grid drift",
            "30 AU label only once the move has landed at 15.0s; NEPTUNE until then; Sun at the left of the line",
            "sparse slow star field, not twinkling bands",
            "limb fit, dark navy, km/h timings 6.51 and 11.31, one-way 30 AU move, and the v04 VO are unchanged",
        ],
        "sources": (
            "Picture: NASA/JPL Voyager 2 PIA01492 (full disc, 1989), public domain, shown under 1.0x. "
            "Earth: NASA AS11-44-6552, the Earth disc only. Sun: NASA PIA03149. "
            "Gemini OK 25 Oct 2026 on https://science.nasa.gov/neptune/neptune-facts/ : "
            "winds more than 2,000 km/h; Earth's most powerful winds about 400 km/h; "
            "30 AU and more than 30 times as far; Voyager 2 encountered Neptune in August 1989; "
            "the Great Dark Spot is the 1989 southern-hemisphere storm. No paid generation."
        ),
        "facts_gemini": [
            "OK 2,000 km/h — These winds whip clouds of frozen methane across the planet at speeds of more than 1,200 miles per hour (2,000 kilometers per hour).",
            "OK 400 km/h — Even Earth's most powerful winds hit only about 250 miles per hour (400 kilometers per hour).",
            "OK 30 AU and 30 times — Dark, cold, and whipped by supersonic winds, ice giant Neptune is more than 30 times as far from the Sun as Earth. Neptune is 30 astronomical units away from the Sun.",
            "OK Great Dark Spot, Aug 1989 — In 1989 a large, oval-shaped storm in Neptune's southern hemisphere dubbed the \"Great Dark Spot\" was large enough to contain the entire Earth. Voyager 2 acquired this image as it encountered Neptune in August of 1989.",
            "Re-check 25 Oct 2026 18:00 London by agy gemini-4-argon-high on https://science.nasa.gov/neptune/neptune-facts/. All four OK. No spoken line was changed.",
            "v07 label timing 25 Oct 2026 19:10 London, agy gemini-4-argon-high, ALL OK. NEPTUNE alone states no distance. NEPTUNE 30 AU, EARTH 1 AU, 30 TIMES, 2,000 km/h, 400 km/h and Great Dark Spot Aug 1989 each matched a quote on https://science.nasa.gov/neptune/neptune-facts/. No spoken line was changed.",
        ],
        "facts_url": "https://science.nasa.gov/neptune/neptune-facts/",
    }
    meta_path = OUT / "owb_sa_s2_neptune_v07_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", "2026-10-27", "--id", "oyRcrFTYyDY",
                           "--vo", str(stem_vo)],
                          capture_output=True, text=True)
    (OUT / "owb_sa_s2_neptune_v07_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                            "--vo", str(stem_vo), "--sfx", str(WORK / "stem_sfx.wav"),
                            "--bed", str(WORK / "stem_bed.wav"),
                            "--minutes", f"{total / 60:.4f}"], capture_output=True, text=True)
    (OUT / "owb_sa_s2_neptune_v07_sfx_level.txt").write_text(level.stdout + level.stderr)
    polish_cuts = WORK / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run([sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
                             "--cuts", str(polish_cuts), "--out", str(WORK / "polish_gate.json")],
                            capture_output=True, text=True)
    (OUT / "owb_sa_s2_neptune_v07_polish.txt").write_text(polish.stdout + polish.stderr)
    others = []
    for p in (REPO / "02_Video-Projects").glob("*/05_Music/*"):
        if p.suffix.lower() not in {".mp3", ".wav", ".m4a", ".aac"}:
            continue
        if p.name == base.BED.name:
            continue
        others.append(str(p))
    music = subprocess.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(HERE),
                            "--bed", str(base.BED), "--video", str(final),
                            "--out", str(WORK / "music_gate.json"), "--others", *others],
                           capture_output=True, text=True)
    (OUT / "owb_sa_s2_neptune_v07_music_gate.txt").write_text(music.stdout + music.stderr)
    try:
        m = finish_scan(final)
        loop_txt = (
            f"PASS loop_diff_masked {m['loop_diff_masked']:.2f} open_median_step {m['open_median_step']:.2f} "
            f"head_matches {m['head_matches']}\n"
        )
        loop_rc = 0
    except SystemExit as e:
        loop_txt = f"FAIL {e}\n"
        loop_rc = 1
    (OUT / "owb_sa_s2_neptune_v07_loop.txt").write_text(loop_txt)
    print(f"gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} loop={loop_rc}", flush=True)
    print(gate.stdout)
    print(loop_txt)
    print((level.stdout or level.stderr)[-500:])
    print((polish.stdout or polish.stderr)[-800:])
    print((music.stdout or music.stderr)[-400:])
    if any((gate.returncode, level.returncode, polish.returncode, music.returncode, loop_rc)):
        raise SystemExit(1)

    delivered = [final, phone, frames, sheet2, meta_path,
                 OUT / "owb_sa_s2_neptune_v07_gate.txt",
                 OUT / "owb_sa_s2_neptune_v07_loop.txt",
                 OUT / "owb_sa_s2_neptune_v07_polish.txt",
                 OUT / "owb_sa_s2_neptune_v07_music_gate.txt",
                 OUT / "owb_sa_s2_neptune_v07_sfx_level.txt"]
    lines = []
    for dest in (UAT_ICLOUD, UAT_NAS):
        dest.mkdir(parents=True, exist_ok=True)
        for src_f in delivered:
            shutil.copy2(src_f, dest / src_f.name)
        manifest = []
        for src_f in delivered:
            digest = sha256(dest / src_f.name)
            if digest != sha256(src_f):
                raise SystemExit(f"sha mismatch {dest / src_f.name}")
            manifest.append(f"{digest}  {src_f.name}")
        (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n")
        lines.append(f"{dest} {manifest[0][:16]}")
        print(f"copied {dest}", flush=True)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
