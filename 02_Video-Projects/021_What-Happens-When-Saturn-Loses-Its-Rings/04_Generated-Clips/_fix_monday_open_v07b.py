#!/usr/bin/env python3
"""v07b — Monday limb-following soft erase + opening grains that CURVE into equator."""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import _gen_saturn_v07 as v07

OUT = v07.OUT
W, H, FPS, DUR, NFRAMES = v07.W, v07.H, v07.FPS, v07.DUR, v07.NFRAMES


def monday_v04b() -> dict:
    print("=== MONDAY v04b limb-curve ===", flush=True)
    img = Image.open(v07.MON_V01).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    h, w = arr.shape[:2]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    warm = (r > 90) & (g > 70) & (b < 150) & ((r + g) > (b + 45)) & (r > b + 12) & (luma > 55) & (luma < 215)
    ice_white = (luma > 155) & (chroma < 40)
    disk = warm & (~ice_white)
    dmask = Image.fromarray((disk * 255).astype(np.uint8))
    for _ in range(2):
        dmask = dmask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    dm = np.asarray(dmask) > 128

    # per-column south limb (curve)
    south_col = np.full(w, -1, dtype=np.int32)
    for x in range(w):
        ys = np.where(dm[:, x])[0]
        if len(ys):
            south_col[x] = int(ys.max())
    # interpolate gaps + smooth
    known = south_col >= 0
    xs = np.arange(w)
    if known.any():
        south_col = np.interp(xs, xs[known], south_col[known]).astype(np.float32)
        # gaussian smooth
        k = np.array([1, 4, 6, 4, 1], dtype=np.float32)
        k /= k.sum()
        pad = np.pad(south_col, 2, mode="edge")
        south_col = np.convolve(pad, k, mode="valid")
    else:
        south_col = np.full(w, h * 0.65, dtype=np.float32)

    ice = (luma > 105) & (chroma < 90) & (abs(r - g) < 65)

    # void fill
    fill = np.zeros_like(arr)
    fill[:] = (3, 3, 5)
    rng = np.random.default_rng(7)
    for _ in range(500):
        x = int(rng.integers(0, w))
        y = int(rng.integers(int(south_col.min()) + 5, h))
        fill[y, x] = [float(rng.integers(120, 210))] * 3

    out = arr.copy()
    FADE_ON = 28.0  # soft fade into cloud tops above limb
    FADE_OFF = 36.0  # soft erase below limb

    for y in range(h):
        for x in range(w):
            if not ice[y, x]:
                continue
            limb = south_col[x]
            # on disk, near limb: soft-fade curtain into warm cloud
            if y <= limb and (limb - y) <= FADE_ON and dm[y, x]:
                t = 1.0 - (limb - y) / FADE_ON
                t = t * t * (3 - 2 * t)
                # sample warm below toward limb
                wy = int(max(0, limb - 35))
                warm_c = arr[wy, x]
                out[y, x] = (1 - 0.7 * t) * out[y, x] + (0.7 * t) * warm_c
            # below limb in void: erase with soft feather along curve
            if y > limb and not dm[y, x]:
                dist = y - limb
                if dist < FADE_OFF:
                    t = dist / FADE_OFF
                    t = t * t * (3 - 2 * t)
                else:
                    t = 1.0
                if luma[y, x] > 28:
                    out[y, x] = (1 - t) * out[y, x] + t * fill[y, x]

    # final void sweep (anything bright below limb+fade)
    for x in range(w):
        y0 = int(south_col[x] + FADE_OFF)
        for y in range(max(0, y0), h):
            if dm[y, x]:
                continue
            lu = 0.299 * out[y, x, 0] + 0.587 * out[y, x, 1] + 0.114 * out[y, x, 2]
            if lu > 30:
                out[y, x] = fill[y, x]

    result = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    # light blur only on void band to kill stair-steps
    void_band = result.crop((0, int(south_col.min()) - 5, w, h))
    void_band = void_band.filter(ImageFilter.GaussianBlur(radius=0.8))
    result.paste(void_band, (0, int(south_col.min()) - 5))

    dest = OUT / "monday_saturn_rings_streaming_v04.png"
    result.save(dest)
    south_med = int(np.median(south_col[south_col > 0]))
    result.crop((0, int(h * 0.55), w, h)).save(OUT / "monday_v04_bottom_qa.png")
    result.crop((int(w * 0.12), int(h * 0.38), int(w * 0.88), south_med)).save(OUT / "monday_v04_face_qa.png")
    v01 = Image.open(v07.MON_V01).convert("RGB")
    if v01.size != result.size:
        v01 = v01.resize(result.size, Image.Resampling.LANCZOS)
    yb0, yb1 = int(h * 0.45), int(h * 0.88)
    band = Image.new("RGB", (w * 2 + 8, yb1 - yb0), (20, 20, 20))
    band.paste(v01.crop((0, yb0, w, yb1)), (0, 0))
    band.paste(result.crop((0, yb0, w, yb1)), (w + 8, 0))
    band.save(OUT / "monday_v01_vs_v04_south.png")
    return {"file": dest.name, "sha256": v07.sha256(dest), "bytes": dest.stat().st_size, "south_median": south_med}


def opening_v07b() -> dict:
    print("=== OPENING v07b curved stream ===", flush=True)
    work = OUT / "_work" / "open_c"
    work.mkdir(parents=True, exist_ok=True)
    # start from open still only (no v04 eruption) — Ben wants stream into equator readable
    still = Image.open(v07.OPEN_STILL)
    still_dir = work / "still_frames"
    still_dir.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        v07.ken_burns(still, fi / FPS, DUR, zoom_end=1.10).save(still_dir / f"s_{fi:04d}.png")

    g = v07.open_geometry()
    rng = np.random.default_rng(41)
    n = 1800
    # each grain: start on inner ring, end on equator face; cubic Bezier control below
    sx = rng.uniform(g["inner_ring_x0"], g["inner_ring_x1"] - 20, size=n)
    sy = g["inner_ring_y"] + rng.normal(0, 6, size=n)
    ex = g["planet_cx"] - g["planet_r"] * 0.92 + rng.uniform(-15, 55, size=n)
    ey = g["equator_y"] + rng.uniform(15, 95, size=n)
    # control points pull path DOWN then RIGHT into planet
    c1x = sx + (ex - sx) * 0.35
    c1y = sy + 40 + rng.uniform(0, 50, size=n)
    c2x = sx + (ex - sx) * 0.75
    c2y = ey + rng.uniform(-10, 30, size=n)
    births = rng.uniform(-2.5, DUR * 0.55, size=n)
    life = rng.uniform(2.2, 4.5, size=n)
    sizes = rng.uniform(2.0, 5.0, size=n)

    out_frames = work / "final"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        base = Image.open(still_dir / f"s_{fi:04d}.png").convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        t = fi / FPS
        for i in range(n):
            if t < births[i] or t > births[i] + life[i]:
                continue
            u = (t - births[i]) / life[i]
            # cubic Bezier
            u2 = u * u
            u3 = u2 * u
            mu = 1 - u
            x = mu**3 * sx[i] + 3 * mu**2 * u * c1x[i] + 3 * mu * u2 * c2x[i] + u3 * ex[i]
            y = mu**3 * sy[i] + 3 * mu**2 * u * c1y[i] + 3 * mu * u2 * c2y[i] + u3 * ey[i]
            if y > g["south_limb_y"] - 2:
                continue
            # fade at cloud tops (end of path)
            fade = 1.0 if u < 0.78 else max(0.0, 1.0 - (u - 0.78) / 0.22)
            a = int(250 * fade)
            if a < 18:
                continue
            # tangent for motion blur
            du = 0.04
            u_b = max(0, u - du)
            u_f = min(1, u + du)
            def bez(uu):
                uu2 = uu * uu
                uu3 = uu2 * uu
                m = 1 - uu
                return (
                    m**3 * sx[i] + 3 * m**2 * uu * c1x[i] + 3 * m * uu2 * c2x[i] + uu3 * ex[i],
                    m**3 * sy[i] + 3 * m**2 * uu * c1y[i] + 3 * m * uu2 * c2y[i] + uu3 * ey[i],
                )
            x0, y0 = bez(u_b)
            x1, y1 = bez(u_f)
            r = max(2, int(sizes[i]))
            draw.line([(x0, y0), (x1, y1)], fill=(252, 253, 255, a), width=max(2, r))
            draw.ellipse([x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7], fill=(255, 255, 255, min(255, a + 40)))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=0.5))
        Image.alpha_composite(base, layer).convert("RGB").save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_open_rings_v07.mp4"
    v07.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_frames / "f_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-an", str(dest),
        ]
    )
    cs = OUT / "edit_open_rings_v07_contact.png"
    times = v07.contact_sheet(dest, cs)
    return {"file": dest.name, "sha256": v07.sha256(dest), "bytes": dest.stat().st_size, "contact": cs.name, "times": times}


def main() -> None:
    o = opening_v07b()
    m = monday_v04b()
    for p in [
        OUT / o["file"],
        OUT / o["contact"],
        OUT / m["file"],
        OUT / "monday_v04_bottom_qa.png",
        OUT / "monday_v04_face_qa.png",
        OUT / "monday_v01_vs_v04_south.png",
    ]:
        v07.chunk_write(p, v07.UAT / p.name)
        if p.suffix == ".png":
            v07.chunk_write(p, v07.ART / p.name)
    print(json.dumps({"V07B": True, "open": o, "monday": m}, indent=2), flush=True)


if __name__ == "__main__":
    main()
