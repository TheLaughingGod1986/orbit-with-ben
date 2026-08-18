#!/usr/bin/env python3
"""Start frames for P01 v12 last plate + P07 v04 last-10s recut.

Photosphere STAR (from the locked giant-star plate), not city-crust, not
the 3-ring bauble, not a portal. Compact glowing remnant.
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
OUT = HERE / "parts/starts_last10s_v01"
GIANT = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_08_it-began-as-a-giant_cursor_v10.mp4"
SUPERNOVA = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_09_supernova-goodbye_cursor_v10.mp4"
SPIRAL = OUT / "p01_12_rising_from_spiral.png"


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


def paste_star_fill(bg: Image.Image, star: Image.Image) -> None:
    ratio = max(W / star.width, H / star.height) * 1.08
    nw, nh = max(2, int(star.width * ratio)), max(2, int(star.height * ratio))
    piece = star.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(piece, (int((W - nw) / 2), int((H - nh) / 2)))


def main() -> None:
    if not GIANT.is_file():
        raise SystemExit(f"missing giant photosphere {GIANT}")
    orbit = crop_orbit(Image.open(FRONT))
    photosphere = grab(GIANT, 4.0, OUT / "_src_giant_photosphere.jpg")

    if SUPERNOVA.is_file():
        grab(SUPERNOVA, 6.5, SPIRAL)
        print("grabbed", SPIRAL.name, flush=True)
    elif SPIRAL.exists():
        print("keep", SPIRAL.name, flush=True)
    else:
        raise SystemExit("missing supernova clip and spiral start")

    # P07 08 — compact GLOWING STAR fills the frame. No Orbit. Not a cracked city.
    bg = clean_space(n_faint=0, seed=708)
    paste_star_fill(bg, photosphere)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "p07_08_star_intensifies.png")

    # P07 09 — Orbit abort-thrusts AWAY from a compact star (not a floor).
    bg = clean_space(n_faint=0, seed=709)
    paste_star_fill(bg, photosphere)
    paste_scaled(bg, orbit, 960, 260, 150)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "p07_09_abort_thrust.png")

    # P07 10 — same star, Orbit further into the abort (higher, leaving).
    bg = clean_space(n_faint=0, seed=710)
    paste_star_fill(bg, photosphere)
    paste_scaled(bg, orbit, 480, 200, 130)
    save(bg.filter(ImageFilter.GaussianBlur(0.2)), "p07_10_abort_away.png")

    print("done", OUT, flush=True)


if __name__ == "__main__":
    main()
