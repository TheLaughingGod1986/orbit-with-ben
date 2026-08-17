#!/usr/bin/env python3
"""Reframe the on-model v10 hang into a tiny-figure EWS.

Omni I2V grows Orbit into a foreground hero even from a 56px start.
Ben likes the v10 identity — keep that take, put him in the dark, then a
slow push toward camera so he comes into the foreground without a CU.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
SRC = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_01_orbit-already-hanging_cursor_v10.mp4"
DEST = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_01_orbit-already-hanging_cursor_v11.mp4"
QC = EP / "_qc_p01_v11_hang"
DUR = 8.0

# Inner plate ~30% of 1920x1080, then a slow centered push-in (still a small figure).
VF = (
    "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
    "fps=24,format=yuv420p,scale=576:324,"
    "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x020306,"
    "zoompan=z='min(1.45,1+0.45*on/191)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    ":d=1:s=1920x1080:fps=24"
)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    QC.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SRC),
            "-vf", VF,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-t", f"{DUR:.3f}",
            str(DEST),
        ],
        check=True,
    )
    for t, name in [(0.4, "src_t00_4"), (4.0, "src_t04"), (7.2, "src_t07")]:
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{t:.3f}", "-i", str(DEST), "-frames:v", "1", "-q:v", "2",
                str(QC / f"{name}.jpg"),
            ],
            check=True,
        )
    print(f"wrote {DEST} {DEST.stat().st_size} bytes", flush=True)


if __name__ == "__main__":
    main()
