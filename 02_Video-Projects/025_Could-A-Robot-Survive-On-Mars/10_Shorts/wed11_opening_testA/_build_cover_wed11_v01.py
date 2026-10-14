#!/usr/bin/env python3
"""025 Wed 11 Nov Short cover (J0103; Chief ruling #6101571703): white WHAT FINALLY / yellow STOPPED IT?, no Orbit,
centre stack in the v04 house look. Plate: the Opportunity deck (PIA15115) from the v03f master at 3 s, the same
crop as the Short's shot 1, so no burned-in captions sit under the words."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

MASTER = FILM / "09_Final-Export/025_MarsRobot_full_rough_v03f.mp4"
OUT = HERE / "08_Covers"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plate = OUT / "_plate_deck_3s.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", str(MASTER), "-frames:v", "1",
                    "-vf", f"crop=608:1080:1150:0,scale={v04.W}:{v04.H}:flags=lanczos", str(plate)], check=True)
    row = v04.compose({"id": "wed11_opening_testA", "plate": plate, "out_dir": OUT,
                       "lines": ["WHAT FINALLY", "STOPPED IT?"], "yellow": {"STOPPED", "IT?"}, "hero": 1,
                       "related": "Js6EQJ8qDi8", "uk": "2026-11-11 11:30", "role": "short_cover"})
    print(row["file"])


if __name__ == "__main__":
    main()
