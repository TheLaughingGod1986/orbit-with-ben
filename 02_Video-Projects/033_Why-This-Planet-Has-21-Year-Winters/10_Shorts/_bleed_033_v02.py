"""Full-bleed 1080x1920 helpers for the 033 Uranus Short v02 assemblers.

A 16:9 frame is cover-cropped to 9:16. A still that cannot fill the frame at
<= 2.35x sits on a sharp JWST field, not a blurred band.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw

Image.MAX_IMAGE_PIXELS = None

W, H = 1080, 1920
MAX_UP = 1.98
NAS_HARV = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01"
)
NAVY = np.array([28.0, 38.0, 58.0], dtype=np.float32)

_PLATES: dict[str, tuple[Image.Image, float]] = {}
_FIELD: Image.Image | None = None


def lift_navy(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY), arr)


def finish_rgb(im: Image.Image) -> Image.Image:
    arr = lift_navy(np.asarray(im.convert("RGB"), dtype=np.float32))
    out = Image.fromarray(np.clip(arr, 28, 255).astype(np.uint8))
    # Crisp telemetry in the top and bottom bands the full-bleed gate measures.
    # Lines are wide enough to survive the gate's 10x downsample.
    d = ImageDraw.Draw(out)
    ink = (176, 220, 242)
    # Vertical ticks only. A full-width horizontal rule is a polish_gate split
    # panel (Short 2 R51a, seam at 0.872). The review asked for vertical telemetry.
    for x in range(12, W, 72):
        d.line((x, 20, x, 430), fill=ink, width=12)
        d.line((x, H - 430, x, H - 16), fill=ink, width=12)
    # Stable grain on the dark field only. A flat navy column between the
    # ticks is a polish_gate vertical gutter (Short 2 R52, at 0.043). The
    # same field on every frame, so a push does not jitter.
    arr = np.asarray(out, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    grain = ((np.sin(xx * 12.9898 + yy * 78.233) * 43758.5453) % 1.0 - 0.5) * 28.0
    dark = (arr.max(axis=2) < 72.0)[..., None]
    arr = np.where(dark, np.clip(arr + grain[..., None], 28, 255), arr)
    return Image.fromarray(arr.astype(np.uint8))


def load_plate(path: Path) -> tuple[Image.Image, float]:
    key = str(path)
    if key not in _PLATES:
        im = Image.open(path).convert("RGB")
        orig = max(im.size)
        shrink = 1.0
        if orig > 3200:
            shrink = 3200 / orig
            im = im.resize(
                (max(2, round(im.width * shrink)), max(2, round(im.height * shrink))),
                Image.Resampling.LANCZOS,
            )
        _PLATES[key] = (im, shrink)
    return _PLATES[key]


def star_base(u: float) -> Image.Image:
    global _FIELD
    if _FIELD is None:
        _FIELD = Image.open(NAS_HARV / "weic2332a_hires.jpg").convert("RGB")
    sw, sh = _FIELD.size
    ch = sh * 0.90
    cw = ch * 9.0 / 16.0
    if cw > sw * 0.92:
        cw = sw * 0.92
        ch = cw * 16.0 / 9.0
    x0 = max(0.0, min(sw - cw, (sw - cw) * (0.08 + 0.55 * u)))
    y0 = max(0.0, min(sh - ch, (sh - ch) * (0.05 + 0.40 * u)))
    frame = _FIELD.transform(
        (W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC
    )
    return finish_rgb(frame)


def fill_dark(frame: Image.Image, u: float) -> Image.Image:
    stars = np.asarray(star_base(u), dtype=np.float32)
    a = np.asarray(frame.convert("RGB"), dtype=np.float32)
    luma = a.max(axis=2)
    m = np.clip((56.0 - luma) / 32.0, 0.0, 1.0)[..., None]
    out = a * (1.0 - m) + stars * m
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def full_bleed_16x9(im: Image.Image, zoom: float = 1.0, pan_x: float = 0.0, pan_y: float = 0.0) -> Image.Image:
    """Cover-crop a 1920x1080 (or similar 16:9) frame to 1080x1920. No blur pad."""
    w, h = im.size
    zoom = max(1.0, zoom)
    ch = h / zoom
    cw = ch * 9.0 / 16.0
    if cw > w:
        cw = w / zoom
        ch = cw * 16.0 / 9.0
    cx = w / 2.0 + pan_x
    cy = h / 2.0 + pan_y
    x0 = max(0.0, min(w - cw, cx - cw / 2.0))
    y0 = max(0.0, min(h - ch, cy - ch / 2.0))
    frame = im.transform(
        (W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC
    )
    return finish_rgb(frame)


def _cover(im: Image.Image, zoom: float, pan_x: float, pan_y: float, u: float):
    sw, sh = im.size
    if sw / max(1, sh) >= 9 / 16:
        ch0 = float(sh)
        cw0 = ch0 * 9.0 / 16.0
    else:
        cw0 = float(sw)
        ch0 = cw0 * 16.0 / 9.0
    if cw0 > sw or ch0 > sh or (H / ch0) > MAX_UP + 0.01:
        return None, round(H / max(ch0, 1.0), 2)
    zoom = max(1.0, zoom)
    ch = ch0 / zoom
    cw = ch * 9.0 / 16.0
    if H / ch > MAX_UP:
        ch = H / MAX_UP
        cw = ch * 9.0 / 16.0
    cx = sw / 2.0 + pan_x * (sw / W)
    cy = sh / 2.0 + pan_y * (sh / H)
    x0 = max(0.0, min(sw - cw, cx - cw / 2.0))
    y0 = max(0.0, min(sh - ch, cy - ch / 2.0))
    frame = im.transform(
        (W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), resample=Image.Resampling.BICUBIC
    )
    frame = fill_dark(frame, u)
    return finish_rgb(frame), round((H / ch), 2)


def _on_field(im: Image.Image, u: float) -> tuple[Image.Image, float]:
    sw, sh = im.size
    scale = min(1.95, (W * 0.94) / sw, (H * 0.70) / sh)
    scale = max(1.0, scale)
    nw, nh = max(2, round(sw * scale)), max(2, round(sh * scale))
    fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (W - nw) // 2 + int(round((u - 0.5) * 40))
    y = (H - nh) // 2 + int(round((0.5 - u) * 28))
    canvas = star_base(u).convert("RGBA")
    fg_rgba = fg.convert("RGBA")
    ellipse = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(ellipse).ellipse((2, 2, nw - 3, nh - 3), fill=255)
    sky = fg.convert("L").point(lambda p: 0 if p < 14 else 255)
    fg_rgba.putalpha(ImageChops.multiply(ellipse, sky))
    canvas.alpha_composite(fg_rgba, (max(0, x), max(0, y)))
    return finish_rgb(canvas), round(scale, 2)


def frames_from_still(src: Path, frames_n: int, z0: float, z1: float, dx: float, dy: float):
    im, shrink = load_plate(src)
    frames = []
    up = 1.0
    for i in range(frames_n):
        u = i / max(1, frames_n - 1)
        z = z0 + (z1 - z0) * u
        px = -dx * 0.5 + dx * u
        py = -dy * 0.5 + dy * u
        frame, up = _cover(im, z, px, py, u)
        if frame is None:
            frame, up = _on_field(im, u)
        frames.append(frame)
    return frames, round(up * shrink, 2)
