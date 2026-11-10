#!/usr/bin/env python3
"""Prepare a clean, consistent Orbit overlay rig.

The current broadcast enlarges 112 px proxy sprites and swaps between cutouts
with different crops.  This utility keeps the canonical neutral artwork,
removes disconnected background debris, creates a restrained blink, and
renders a reusable transparent ProRes 4444 loop on a fixed canvas.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


PROJECT = Path("/Users/ben/code/Orbit-YouTube")
SOURCE = PROJECT / "01_Orbit-Character/02_Transparent-PNGs/orbit_rgba_neutral.png"
OUT = PROJECT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v01"
FPS = 30
CANVAS = (420, 380)
BODY_H = 282


def connected_core(alpha: np.ndarray, threshold: int = 72) -> np.ndarray:
    """Return the alpha component connected to the character centre."""
    solid = alpha >= threshold
    h, w = solid.shape
    # Search outward from the visual centre until a solid character pixel is found.
    cx, cy = w // 2, h // 2
    seed = None
    for radius in range(0, max(w, h), 8):
        x0, x1 = max(0, cx - radius), min(w, cx + radius + 1)
        y0, y1 = max(0, cy - radius), min(h, cy + radius + 1)
        ys, xs = np.where(solid[y0:y1, x0:x1])
        if len(xs):
            seed = (int(ys[0] + y0), int(xs[0] + x0))
            break
    if seed is None:
        raise RuntimeError("No opaque Orbit pixels found")

    seen = np.zeros_like(solid, dtype=np.uint8)
    q: deque[tuple[int, int]] = deque([seed])
    seen[seed] = 1
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and solid[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1
                q.append((ny, nx))
    return seen.astype(bool)


def clean_source() -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA")
    arr = np.asarray(image).copy()
    alpha = arr[:, :, 3]
    core = connected_core(alpha)
    # Keep original antialiasing and the antenna glow close to the solid body,
    # while discarding stars and background flecks elsewhere.
    halo = Image.fromarray(core.astype(np.uint8) * 255, "L").filter(ImageFilter.MaxFilter(31))
    keep = np.asarray(halo) > 0
    arr[:, :, 3] = np.where(keep, alpha, 0).astype(np.uint8)
    cleaned = Image.fromarray(arr, "RGBA")
    bbox = cleaned.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("Cleaned Orbit has no alpha bounds")
    pad = 12
    x0, y0, x1, y1 = bbox
    return cleaned.crop((max(0, x0 - pad), max(0, y0 - pad),
                         min(cleaned.width, x1 + pad), min(cleaned.height, y1 + pad)))


def add_shadow(image: Image.Image) -> Image.Image:
    scale = BODY_H / image.height
    size = (max(1, round(image.width * scale)), BODY_H)
    body = image.resize(size, Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = (CANVAS[0] - body.width) // 2
    y = (CANVAS[1] - body.height) // 2 - 4

    alpha = body.getchannel("A")
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(11)).point(lambda p: round(p * 0.42))
    shadow = Image.new("RGBA", body.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    layer.alpha_composite(shadow, (x + 7, y + 11))
    layer.alpha_composite(body, (x, y))
    return layer


def blink_frame(clean: Image.Image, amount: float) -> Image.Image:
    """Paint a blink onto the canonical visor without changing the body."""
    # Coordinates are proportional to the clean canonical crop.
    image = clean.copy()
    w, h = image.size
    draw = ImageDraw.Draw(image)
    visor = (18, 22, 31, 255)
    cream = (255, 239, 190, 255)
    eyes = [
        (0.360 * w, 0.370 * h, 0.570 * w, 0.610 * h),
        (0.595 * w, 0.370 * h, 0.810 * w, 0.610 * h),
    ]
    for x0, y0, x1, y1 in eyes:
        # Cover the original eye inside the black faceplate.
        margin_x, margin_y = 0.008 * w, 0.006 * h
        draw.ellipse((x0 - margin_x, y0 - margin_y, x1 + margin_x, y1 + margin_y), fill=visor)
        cy = (y0 + y1) / 2
        half_h = max(2.0, (y1 - y0) * (1.0 - amount) * 0.48)
        if amount < 0.82:
            draw.ellipse((x0, cy - half_h, x1, cy + half_h), fill=cream)
            pupil_w = (x1 - x0) * 0.34
            pupil_h = max(2.0, half_h * 0.95)
            pcx = (x0 + x1) / 2 + (x1 - x0) * 0.13
            draw.ellipse((pcx - pupil_w / 2, cy - pupil_h / 2,
                          pcx + pupil_w / 2, cy + pupil_h / 2), fill=visor)
        else:
            width = max(4, round((y1 - y0) * 0.07))
            draw.arc((x0, cy - 0.18 * (y1 - y0), x1, cy + 0.30 * (y1 - y0)),
                     200, 340, fill=cream, width=width)
    return image


def encode_loop(frames: list[tuple[Path, float]], output: Path) -> None:
    concat = OUT / "_blink_sequence.ffconcat"
    lines = ["ffconcat version 1.0"]
    for path, duration in frames:
        lines += [f"file '{path}'", f"duration {duration:.6f}"]
    lines.append(f"file '{frames[-1][0]}'")
    concat.write_text("\n".join(lines) + "\n")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-safe", "0", "-f", "concat", "-i", str(concat),
        "-t", "6.0",
        "-vf",
        (
            f"fps={FPS},format=rgba,"
            "rotate=a='0.018*sin(2*PI*t/6)':"
            "fillcolor=0x00000000:ow=iw:oh=ih"
        ),
        "-an", "-c:v", "prores_ks", "-profile:v", "4",
        "-pix_fmt", "yuva444p10le", "-vendor", "apl0",
        str(output),
    ], check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    clean = clean_source()
    neutral = add_shadow(clean)
    half = add_shadow(blink_frame(clean, 0.55))
    closed = add_shadow(blink_frame(clean, 1.0))

    neutral_path = OUT / "orbit_overlay_neutral_clean_v01.png"
    half_path = OUT / "orbit_overlay_blink-half_v01.png"
    closed_path = OUT / "orbit_overlay_blink-closed_v01.png"
    neutral.save(neutral_path)
    half.save(half_path)
    closed.save(closed_path)

    loop = OUT / "orbit_overlay_idle-blink_6s_v01.mov"
    encode_loop([
        (neutral_path, 3.10),
        (half_path, 0.067),
        (closed_path, 0.100),
        (half_path, 0.067),
        (neutral_path, 2.666),
    ], loop)
    (OUT / "README.md").write_text(
        "# Orbit Overlay Rig v01\n\n"
        "A clean, fixed-canvas Orbit companion for documentary overlays.\n\n"
        "- Canonical source: `orbit_rgba_neutral.png`\n"
        "- Transparent 420x380 ProRes 4444 loop\n"
        "- 6-second seamless idle with restrained blink and tilt\n"
        "- Keep at one fixed lower-corner anchor; do not reposition per shot\n"
        "- Recommended rendered height: about 22% of a 1080p frame\n"
        "- Hide on text cards, chapter cards, and brand plates\n"
    )
    print(loop)


if __name__ == "__main__":
    main()
