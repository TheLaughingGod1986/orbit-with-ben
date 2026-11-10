#!/usr/bin/env python3
"""Add genuine blink animation to every clean Orbit performance pose."""
from __future__ import annotations

from pathlib import Path
import subprocess

import numpy as np
from PIL import Image


PROJECT = Path("/Users/ben/code/Orbit-YouTube")
SOURCE = PROJECT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v02/normalised"
RIG = PROJECT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03"
FRAMES = RIG / "frames"
LOOPS = RIG / "loops"
FPS = 30
POSES = ("neutral-left", "present-left", "thinking-left", "amazed", "wave-camera")


def eye_boxes(image: Image.Image) -> list[tuple[int, int, int, int]]:
    """Find the two cream eye components while ignoring orange highlights."""
    pixels = np.asarray(image.convert("RGBA"))
    r = pixels[:, :, 0]
    g = pixels[:, :, 1]
    b = pixels[:, :, 2]
    a = pixels[:, :, 3]
    mask = (
        (a > 120)
        & (r > 180)
        & (g > 150)
        & (b > 70)
        & (g.astype(float) / np.maximum(r, 1) > 0.70)
        & (b.astype(float) / np.maximum(g, 1) > 0.38)
    )
    mask[:120] = False
    mask[290:] = False

    seen = np.zeros(mask.shape, dtype=bool)
    components = []
    height, width = mask.shape
    for y, x in zip(*np.where(mask)):
        if seen[y, x]:
            continue
        stack = [(int(y), int(x))]
        seen[y, x] = True
        xs, ys = [], []
        while stack:
            yy, xx = stack.pop()
            xs.append(xx)
            ys.append(yy)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = yy + dy, xx + dx
                if (
                    0 <= ny < height
                    and 0 <= nx < width
                    and mask[ny, nx]
                    and not seen[ny, nx]
                ):
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if len(xs) > 700:
            components.append((len(xs), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))

    boxes = [box for _, box in sorted(components, reverse=True)[:2]]
    if len(boxes) != 2:
        raise RuntimeError(f"Expected two eyes, found {len(boxes)}")
    return sorted(boxes)


def dark_faceplate_colour(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    pixels = np.asarray(image.convert("RGBA"))
    x0, y0, x1, y1 = box
    pad = 7
    sample = pixels[max(0, y0 - pad):min(pixels.shape[0], y1 + pad),
                    max(0, x0 - pad):min(pixels.shape[1], x1 + pad)]
    rgb = sample[:, :, :3]
    alpha = sample[:, :, 3]
    dark = rgb[(alpha > 180) & (rgb.max(axis=2) < 85)]
    if len(dark) == 0:
        return (7, 18, 27, 255)
    median = np.median(dark, axis=0).astype(np.uint8)
    return (int(median[0]), int(median[1]), int(median[2]), 255)


def blink_frame(image: Image.Image, factor: float) -> Image.Image:
    result = image.copy().convert("RGBA")
    for x0, y0, x1, y1 in eye_boxes(image):
        margin = 3
        box = (
            max(0, x0 - margin),
            max(0, y0 - margin),
            min(image.width, x1 + margin),
            min(image.height, y1 + margin),
        )
        crop = image.crop(box)
        colour = dark_faceplate_colour(image, box)
        result.paste(colour, box)

        new_height = max(3, round(crop.height * factor))
        squeezed = crop.resize((crop.width, new_height), Image.Resampling.LANCZOS)
        paste_y = box[1] + (crop.height - new_height) // 2
        result.alpha_composite(squeezed, (box[0], paste_y))
    return result


def prepare_pose(pose: str) -> tuple[Path, Path, Path]:
    image = Image.open(SOURCE / f"orbit_{pose}_normalised_v01.png").convert("RGBA")
    normal = FRAMES / f"orbit_{pose}_normal.png"
    half = FRAMES / f"orbit_{pose}_blink-half.png"
    closed = FRAMES / f"orbit_{pose}_blink-closed.png"
    image.save(normal)
    blink_frame(image, 0.48).save(half)
    blink_frame(image, 0.13).save(closed)
    return normal, half, closed


def encode_loop(pose: str, normal: Path, half: Path, closed: Path) -> Path:
    sequence = RIG / f"_{pose}_blink.ffconcat"
    timeline = [
        (normal, 1.35),
        (half, 0.067),
        (closed, 0.100),
        (half, 0.067),
        (normal, 2.55),
        (half, 0.067),
        (closed, 0.100),
        (half, 0.067),
        (normal, 1.632),
    ]
    sequence.write_text(
        "ffconcat version 1.0\n"
        + "".join(f"file '{path}'\nduration {duration:.3f}\n" for path, duration in timeline)
        + f"file '{normal}'\n"
    )
    output = LOOPS / f"orbit_{pose}_animated-blink_6s_v01.mov"
    tilt = 0.010 if pose == "neutral-left" else 0.016
    period = 6.2 if pose == "neutral-left" else 5.2
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(sequence),
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
    FRAMES.mkdir(parents=True, exist_ok=True)
    LOOPS.mkdir(parents=True, exist_ok=True)
    for pose in POSES:
        frames = prepare_pose(pose)
        output = encode_loop(pose, *frames)
        print(pose, output)
    (RIG / "README.md").write_text(
        "# Orbit Animated Performance Rig v03\n\n"
        "Five clean, body-anchored performance poses with two genuine facial "
        "blinks per six-second loop. The face animation is combined with "
        "restrained hover/tilt motion and cross-pose choreography in v25.\n"
    )


if __name__ == "__main__":
    main()

