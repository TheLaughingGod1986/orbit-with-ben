#!/usr/bin/env python3
"""Force every title/beat/brand text plate to be pixel-locked stills.

No zoompan, no Ken Burns, no scale resampling — text must not vibrate.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
CARDS = ROOT / "04_Generated-Clips/03_Polished/unique_cards"
BRAND = ROOT / "04_Generated-Clips/03_Polished/brand"
W, H, FPS = 1920, 1080, 30


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)], text=True).strip())


def encode_still(png: Path, mp4: Path, dur: float) -> None:
    """Identical frame repeated. All-intra + stillimage = no temporal drift."""
    # Ensure PNG is exact 1920x1080 first (one Lanczos resize on the still only)
    tmp = mp4.with_suffix(".sized.png")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(png),
        "-vf", f"scale={W}:{H}:flags=lanczos,setsar=1",
        str(tmp),
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(tmp),
        "-t", f"{dur:.3f}",
        "-vf", "format=yuv420p",
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "14",
        "-x264-params", "keyint=1:min-keyint=1:scenecut=0:ref=1:bframes=0",
        "-an", "-movflags", "+faststart",
        str(mp4),
    ], check=True)
    tmp.unlink(missing_ok=True)


def main() -> None:
    n = 0
    for png in sorted(CARDS.glob("*.png")):
        mp4 = CARDS / f"{png.stem}_v01.mp4"
        dur = 3.0
        if mp4.exists():
            try:
                dur = max(1.0, probe(mp4))
            except Exception:
                dur = 3.0
        encode_still(png, mp4, dur)
        n += 1
        if n % 25 == 0:
            print(f"locked {n}…", flush=True)
    print(f"cards_locked={n}")

    intro = BRAND / "orbit_brand_intro_v02.png"
    if not intro.exists():
        intro = BRAND / "orbit_brand_intro_v01.png"
    outro = BRAND / "orbit_brand_outro_subscribe_v02.png"
    if not outro.exists():
        outro = BRAND / "orbit_brand_outro_subscribe_v01.png"
    encode_still(intro, BRAND / "orbit_brand_intro_v01.mp4", 1.2)
    encode_still(outro, BRAND / "orbit_brand_outro_subscribe_v01.mp4", 8.0)
    print("brand_locked")


if __name__ == "__main__":
    main()
