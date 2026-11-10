#!/usr/bin/env python3
"""Start frames for Part 01 first-7s recut.

Photosphere STAR that looks almost ordinary. Tiny Orbit. Not the 3-ring bauble.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _make_part01_v08_start_frames import FRONT, H, W, clean_space, crop_orbit, paste_scaled  # noqa: E402

EP = HERE.parent
OUT = HERE / "parts/starts_open7_v01"
GIANT = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_08_it-began-as-a-giant_cursor_v10.mp4"


def grab(src: Path, t: float, dest: Path) -> Image.Image:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-q:v", "2",
            str(dest),
        ],
        check=True,
    )
    return Image.open(dest).convert("RGB")


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name} {im.size}", flush=True)


def paste_star_fill(bg: Image.Image, star: Image.Image, scale: float = 1.06) -> None:
    ratio = max(W / star.width, H / star.height) * scale
    nw, nh = max(2, int(star.width * ratio)), max(2, int(star.height * ratio))
    piece = star.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(piece, (int((W - nw) / 2), int((H - nh) / 2)))


def main() -> None:
    if not GIANT.is_file():
        raise SystemExit(f"missing photosphere source {GIANT}")
    orbit = crop_orbit(Image.open(FRONT))
    star = grab(GIANT, 2.2, OUT / "_src_ordinary_photosphere.jpg")

    # 01 — STAR ONLY fills the frame. Zero Orbit.
    bg = clean_space(n_faint=0, seed=101)
    paste_star_fill(bg, star, 1.10)
    save(bg.filter(ImageFilter.GaussianBlur(0.15)), "01_star_only.png")

    # 02 — tiny Orbit just entering from the left; star still the subject.
    bg = clean_space(n_faint=0, seed=102)
    paste_star_fill(bg, star, 1.08)
    paste_scaled(bg, orbit, 220, 620, 88)
    save(bg.filter(ImageFilter.GaussianBlur(0.15)), "02_tiny_banks_in.png")

    # 03 — EWS hang: tiny probe in the dark against a huge almost-ordinary star.
    bg = clean_space(n_faint=0, seed=103)
    paste_star_fill(bg, star, 1.08)
    paste_scaled(bg, orbit, 640, 700, 78)
    save(bg.filter(ImageFilter.GaussianBlur(0.15)), "03_tiny_hang.png")

    # 04 — star only, a touch closer; ordinary is about to die.
    bg = clean_space(n_faint=0, seed=104)
    paste_star_fill(bg, star, 1.18)
    save(bg.filter(ImageFilter.GaussianBlur(0.15)), "04_ordinary_dies.png")

    print("done", OUT, flush=True)


if __name__ == "__main__":
    main()
