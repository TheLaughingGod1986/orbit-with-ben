#!/usr/bin/env python3
"""Build polished, tightly-cropped Orbit overlay loops from Overlay-Rig-v03.

Source loops are ~580x430 with lots of empty canvas. We crop to the opaque
silhouette and keep a thin anti-aliased alpha rim so large on-screen Orbit
stays crisp (not the jagged 144px narrator loops).
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SRC = ROOT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops"
OUT = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/04_Generated-Clips/03_Polished/orbit_narrator/rgba/loops_polished_v25"
OUT.mkdir(parents=True, exist_ok=True)

# Map performance names → emotion-ish filenames used by the edit EDL / pool
NAME_MAP = {
    "present-left": "present",
    "neutral-left": "neutral",
    "thinking-left": "thinking",
    "amazed": "amazed",
    "wave-camera": "wave",
}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def content_bbox(path: Path, pad: int = 6) -> tuple[int, int, int, int]:
    with tempfile.TemporaryDirectory() as td:
        frame = Path(td) / "f.png"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(path), "-frames:v", "1", str(frame),
        ])
        arr = np.asarray(Image.open(frame).convert("RGBA"))
    ys, xs = np.where(arr[:, :, 3] > 24)
    if len(xs) == 0:
        h, w = arr.shape[:2]
        return 0, 0, w, h
    x0 = max(0, int(xs.min()) - pad)
    y0 = max(0, int(ys.min()) - pad)
    x1 = min(arr.shape[1], int(xs.max()) + 1 + pad)
    y1 = min(arr.shape[0], int(ys.max()) + 1 + pad)
    return x0, y0, x1, y1


def clean_alpha(im: Image.Image) -> Image.Image:
    """Drop dust; keep a thin AA rim for crisp large overlays."""
    arr = np.asarray(im.convert("RGBA")).copy()
    a = arr[:, :, 3].astype(np.int16)
    # kill near-zero fringe dust
    a = np.where(a < 28, 0, a)
    # solid core
    a = np.where(a > 210, 255, a)
    arr[:, :, 3] = a.astype(np.uint8)
    clear = arr[:, :, 3] == 0
    arr[:, :, 0][clear] = 0
    arr[:, :, 1][clear] = 0
    arr[:, :, 2][clear] = 0
    return Image.fromarray(arr, "RGBA")


def convert_loop(src: Path, dst: Path, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    with tempfile.TemporaryDirectory(prefix="orb_pol_") as td:
        td = Path(td)
        # explode frames
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-vf", f"crop={w}:{h}:{x0}:{y0},format=rgba",
            str(td / "f_%04d.png"),
        ])
        frames = sorted(td.glob("f_*.png"))
        assert frames, src
        for fr in frames:
            clean_alpha(Image.open(fr)).save(fr)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", "30",
            "-i", str(td / "f_%04d.png"),
            "-c:v", "png", "-pix_fmt", "rgba",
            "-an", str(dst),
        ])


def main() -> None:
    print(f"OUT → {OUT}")
    for src in sorted(SRC.glob("orbit_*_animated-blink_6s_v01.mov")):
        # orbit_present-left_animated-blink_6s_v01.mov
        key = src.name.replace("orbit_", "").replace("_animated-blink_6s_v01.mov", "")
        alias = NAME_MAP.get(key, key.replace("-", "_"))
        box = content_bbox(src)
        dst = OUT / f"orbit_{alias}_idle.mov"
        print(f"  {src.name} bbox={box} → {dst.name}")
        convert_loop(src, dst, box)
        # talk alias = same performance for now (blink loop reads fine under VO)
        talk = OUT / f"orbit_{alias}_talk.mov"
        talk.write_bytes(dst.read_bytes())

    # Also bake a high-res static present from the polished RGBA pose (no blink)
    pose = ROOT / "01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v02/poses-rgba/orbit_present-left_rgba_v02.png"
    if pose.exists():
        im = clean_alpha(Image.open(pose))
        arr = np.asarray(im)
        ys, xs = np.where(arr[:, :, 3] > 24)
        im = im.crop((max(0, xs.min() - 8), max(0, ys.min() - 8),
                      min(im.width, xs.max() + 9), min(im.height, ys.max() + 9)))
        # 2s hold loop
        with tempfile.TemporaryDirectory(prefix="orb_static_") as td:
            td = Path(td)
            for i in range(60):
                im.save(td / f"f_{i:04d}.png")
            dst = OUT / "orbit_present_hires_idle.mov"
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "30", "-i", str(td / "f_%04d.png"),
                "-c:v", "png", "-pix_fmt", "rgba", "-an", str(dst),
            ])
            (OUT / "orbit_present_hires_talk.mov").write_bytes(dst.read_bytes())
            print(f"  hires present → {dst.name} size={im.size}")

    print("DONE")


if __name__ == "__main__":
    main()
