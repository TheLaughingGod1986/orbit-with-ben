#!/usr/bin/env python3
"""Normalise the interactive Orbit pose library to one stable screen anchor."""
from __future__ import annotations

from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageFilter


PROJECT = Path("/Users/ben/code/Orbit-YouTube")
RIG = PROJECT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v02"
SRC = RIG / "poses-rgba"
NORM = RIG / "normalised"
LOOPS = RIG / "loops"
CANVAS = (580, 430)
MAX_SIZE = (520, 325)
BASELINE = 388
TARGET_X = 300
FPS = 30

# Anchor fractions refer to the tight visible crop, not the full generated PNG.
# They keep the spherical body fixed while arms extend in different directions.
POSES = {
    "neutral-left": {"file": "orbit_neutral-left_rgba_v02.png", "anchor_x": 0.50, "tilt": 0.010, "period": 6.2},
    "present-left": {"file": "orbit_present-left_rgba_v02.png", "anchor_x": 0.76, "tilt": 0.016, "period": 5.4},
    "thinking-left": {"file": "orbit_thinking-left_rgba_v02.png", "anchor_x": 0.51, "tilt": 0.012, "period": 6.8},
    "amazed": {"file": "orbit_amazed_rgba_v02.png", "anchor_x": 0.50, "tilt": 0.020, "period": 4.8, "flip": True},
    "wave-camera": {"file": "orbit_wave-camera_rgba_v02.png", "anchor_x": 0.59, "tilt": 0.018, "period": 4.6},
}


def despill(image: Image.Image) -> Image.Image:
    arr = np.asarray(image.convert("RGBA")).copy()
    r = arr[:, :, 0].astype(np.float32)
    g = arr[:, :, 1].astype(np.float32)
    b = arr[:, :, 2].astype(np.float32)
    a = arr[:, :, 3]
    green = (a > 0) & (g > r * 1.08) & (g > b * 1.18)
    # Convert the last key-colored edge/glow pixels to a restrained amber glow.
    new_r = np.maximum(r, g * 0.92)
    new_g = np.minimum(g, new_r * 0.66)
    new_b = np.minimum(b, new_r * 0.22)
    arr[:, :, 0] = np.where(green, new_r, r).clip(0, 255).astype(np.uint8)
    arr[:, :, 1] = np.where(green, new_g, g).clip(0, 255).astype(np.uint8)
    arr[:, :, 2] = np.where(green, new_b, b).clip(0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def normalise(name: str, cfg: dict) -> Path:
    image = despill(Image.open(SRC / cfg["file"]))
    if cfg.get("flip"):
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError(f"{name} has no visible alpha")
    tight = image.crop(bbox)
    scale = min(MAX_SIZE[0] / tight.width, MAX_SIZE[1] / tight.height)
    resized = tight.resize(
        (max(1, round(tight.width * scale)), max(1, round(tight.height * scale))),
        Image.Resampling.LANCZOS,
    )
    anchor_x = round(resized.width * float(cfg["anchor_x"]))
    x = TARGET_X - anchor_x
    y = BASELINE - resized.height

    layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    alpha = resized.getchannel("A")
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(10)).point(lambda p: round(p * 0.38))
    shadow = Image.new("RGBA", resized.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_alpha)
    layer.alpha_composite(shadow, (x + 7, y + 10))
    layer.alpha_composite(resized, (x, y))

    out = NORM / f"orbit_{name}_normalised_v01.png"
    layer.save(out)
    return out


def encode_loop(name: str, png: Path, cfg: dict) -> Path:
    output = LOOPS / f"orbit_{name}_performance-loop_6s_v01.mov"
    tilt = float(cfg["tilt"])
    period = float(cfg["period"])
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(png),
        "-t", "6.0",
        "-vf",
        (
            f"fps={FPS},format=rgba,"
            f"rotate=a='{tilt:.4f}*sin(2*PI*t/{period:.3f})':"
            "fillcolor=0x00000000:ow=iw:oh=ih"
        ),
        "-an", "-c:v", "prores_ks", "-profile:v", "4",
        "-pix_fmt", "yuva444p10le", "-vendor", "apl0", str(output),
    ], check=True)
    return output


def main() -> None:
    NORM.mkdir(parents=True, exist_ok=True)
    LOOPS.mkdir(parents=True, exist_ok=True)
    outputs = []
    for name, cfg in POSES.items():
        png = normalise(name, cfg)
        mov = encode_loop(name, png, cfg)
        outputs.append((name, png, mov))
        print(name, png, mov)
    (RIG / "README.md").write_text(
        "# Orbit Performance Rig v02\n\n"
        "Five identity-consistent transparent performance poses, normalised to a "
        "single body anchor on a 580x430 canvas.\n\n"
        "- `neutral-left`: default content-focused gaze\n"
        "- `present-left`: points into the documentary frame\n"
        "- `thinking-left`: reflective scientific beat\n"
        "- `amazed`: discovery and scale reaction\n"
        "- `wave-camera`: direct viewer address\n\n"
        "All loops use ProRes 4444 transparency and restrained motion. Position "
        "the canvas at one fixed lower-right screen anchor; change pose without "
        "changing overlay coordinates.\n"
    )


if __name__ == "__main__":
    main()
