#!/usr/bin/env python3
"""Review pack for Sun 022 cut v05 (J0024).

The v03 pack (per-row sheet, mid-row frames, 0/0.5/1 s and last frame, rows 51/96/104,
clip_check, loudness) on v05, plus full-size frames through row 49 (now PIA22646).
The video itself stays out of git.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("rp3", HERE / "_review_pack_v03.py")
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)

rp.FILM = HERE / "sun_film/sun_first_cut_v05.mp4"
rp.WORK = HERE / "sun_film/work_first_cut_v05"
rp.OUT = HERE / "review_v05"

ROW49_TIMES = [227.2, 229.5, 231.7]


def main() -> None:
    rp.main()
    old = rp.OUT / "sun_first_cut_v03_per_row.png"
    if old.exists():
        old.rename(rp.OUT / "sun_first_cut_v05_per_row.png")
    for t in ROW49_TIMES:
        rp.frame(t, rp.OUT / f"row049_t{t:06.1f}.jpg")


if __name__ == "__main__":
    main()
