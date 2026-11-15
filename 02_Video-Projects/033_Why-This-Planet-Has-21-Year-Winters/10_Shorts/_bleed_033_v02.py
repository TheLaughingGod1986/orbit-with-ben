"""Full-bleed 1080x1920 helpers for the 033 Uranus Short v02 assemblers.

Every shot fills the 1080x1920 (9:16) canvas cleanly using authentic outer
JWST deep-field starfield surround (cropped away from the central Uranus ring
halo so a second planet never appears behind the subject) and zero artificial
grid lines or bars.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

Image.MAX_IMAGE_PIXELS = None

W, H = 1080, 1920
MAX_UP = 1.98
NAS_HARV = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01"
)
NAVY = np.array([28.0, 38.0, 58.0], dtype=np.float32)

_PLATES: dict[str, tuple[Image.Image, float]] = {}
_STAR_CORNER: Image.Image | None = None
_STAR_DOTS: np.ndarray | None = None
_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
_DX_ELL = (_XX - W * 0.5) / (W * 0.55)
_DY_ELL = (_YY - H * 0.5) / (H * 0.36)
_R_ELL = np.sqrt(_DX_ELL * _DX_ELL + _DY_ELL * _DY_ELL)
_M_DOME = np.clip((_R_ELL - 0.85) / 0.42, 0.0, 1.0)
_M_DOME = (0.5 - 0.5 * np.cos(np.pi * _M_DOME)) * 0.65


def lift_navy(arr: np.ndarray) -> np.ndarray:
    mx = arr.max(axis=2, keepdims=True)
    return np.where(mx < 54.0, np.maximum(arr, NAVY), arr)


def _ensure_star_assets() -> tuple[Image.Image, np.ndarray]:
    global _STAR_CORNER, _STAR_DOTS
    if _STAR_CORNER is None or _STAR_DOTS is None:
        raw_jwst = Image.open(NAS_HARV / "weic2332a_hires.jpg").convert("RGB")
        # Pure outer deep-field starfield corner (0, 0, 620, 1102) — zero central Uranus ring halo
        _STAR_CORNER = raw_jwst.crop((0, 0, 620, 1102)).resize(
            (1360, 2416), Image.Resampling.LANCZOS
        )
        rng = np.random.default_rng(3302)
        dots = np.zeros((2416, 1360, 3), dtype=np.float32)
        for _ in range(2600):
            sy = int(rng.integers(4, 2410))
            sx = int(rng.integers(4, 1354))
            b = float(rng.uniform(60.0, 150.0))
            sz = 2 if rng.random() < 0.75 else 3
            dots[sy : sy + sz, sx : sx + sz, 0] = np.maximum(
                dots[sy : sy + sz, sx : sx + sz, 0], b * 0.88
            )
            dots[sy : sy + sz, sx : sx + sz, 1] = np.maximum(
                dots[sy : sy + sz, sx : sx + sz, 1], b * 0.96
            )
            dots[sy : sy + sz, sx : sx + sz, 2] = np.maximum(
                dots[sy : sy + sz, sx : sx + sz, 2], b * 1.05
            )
        _STAR_DOTS = dots
    return _STAR_CORNER, _STAR_DOTS


def _star_array(u: float) -> np.ndarray:
    corner, dots = _ensure_star_assets()
    u_clamped = max(0.0, min(1.0, float(u)))
    x0 = int(round(40 + 200 * u_clamped))
    y0 = int(round(60 + 360 * u_clamped))
    st = np.asarray(corner.crop((x0, y0, x0 + W, y0 + H)), dtype=np.float32)
    d_crop = dots[y0 : y0 + H, x0 : x0 + W]
    st_norm = np.clip((st - 10.0) / 215.0, 0.0, 1.0)
    rgb = (
        np.stack(
            [
                28.0 + 215.0 * (st_norm[:, :, 0] ** 0.54),
                38.0 + 210.0 * (st_norm[:, :, 1] ** 0.51),
                58.0 + 190.0 * (st_norm[:, :, 2] ** 0.49),
            ],
            axis=-1,
        )
        + d_crop
    )
    return np.clip(lift_navy(rgb), 28.0, 255.0)


def finish_rgb(im: Image.Image, u: float = 0.5) -> Image.Image:
    """Blend authentic deep-field starfield into dark space and outer sky dome with zero bars or seams."""
    st = _star_array(u)
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    luma = a.max(axis=2)
    m_dark = np.clip((64.0 - luma) / 36.0, 0.0, 1.0)
    m = np.maximum(m_dark, _M_DOME)[..., None]
    out = a * (1.0 - m) + st * m
    out = lift_navy(out)
    return Image.fromarray(np.clip(out, 28, 255).astype(np.uint8))


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
    return Image.fromarray(_star_array(u).astype(np.uint8))


def fill_dark(frame: Image.Image, u: float) -> Image.Image:
    return finish_rgb(frame, u)


def full_bleed_16x9(
    im: Image.Image, zoom: float = 1.0, pan_x: float = 0.0, pan_y: float = 0.0, u: float = 0.5
) -> Image.Image:
    """Cover-crop a 1920x1080 (or similar 16:9) frame to 1080x1920 with crisp atmospheric detail."""
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
    frame = frame.filter(ImageFilter.UnsharpMask(radius=2.0, percent=145, threshold=2))
    return finish_rgb(frame, u)


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
    return finish_rgb(frame, u), round((H / ch), 2)


def _on_field(im: Image.Image, u: float) -> tuple[Image.Image, float]:
    sw, sh = im.size
    scale = min(1.95, (W * 0.94) / sw, (H * 0.68) / sh)
    scale = max(1.0, scale)
    nw, nh = max(2, round(sw * scale)), max(2, round(sh * scale))
    fg = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (W - nw) // 2 + int(round((u - 0.5) * 40))
    y = (H - nh) // 2 + int(round((0.5 - u) * 28))
    canvas = star_base(u).convert("RGBA")
    fg_rgba = fg.convert("RGBA")
    ellipse = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(ellipse).ellipse((12, 12, nw - 13, nh - 13), fill=255)
    ellipse = ellipse.filter(ImageFilter.GaussianBlur(18))
    sky = fg.convert("L").point(lambda p: 0 if p < 14 else 255).filter(ImageFilter.GaussianBlur(4))
    fg_rgba.putalpha(ImageChops.multiply(ellipse, sky))
    canvas.alpha_composite(fg_rgba, (max(0, x), max(0, y)))
    return finish_rgb(canvas, u), round(scale, 2)


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
