#!/usr/bin/env python3
"""Review pack for Sun 022 cut v04 (J0019, #99 6045620003).

The v03 pack (per-row sheet, mid-row frames, 0/0.5/1 s and last frame, rows 51/96/104,
clip_check, loudness) on v04, plus full-size frames through row 14 (the rising line under
"by a slow rise in the light of the whole star") and the swapped rows 8, 49 and 50.
The video itself stays out of git.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("rp3", HERE / "_review_pack_v03.py")
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)

rp.FILM = HERE / "sun_film/sun_first_cut_v04.mp4"
rp.WORK = HERE / "sun_film/work_first_cut_v04"
rp.OUT = HERE / "review_v04"

ROW14_TIMES = [55.6, 56.2, 56.6, 57.2, 57.8, 58.4]
SWAP_TIMES = {8: [25.6, 28.0, 30.4], 49: [227.2, 229.5, 231.7], 50: [232.5, 234.5, 236.5]}


def main() -> None:
    rp.main()
    old = rp.OUT / "sun_first_cut_v03_per_row.png"
    if old.exists():
        old.rename(rp.OUT / "sun_first_cut_v04_per_row.png")
    for t in ROW14_TIMES:
        rp.frame(t, rp.OUT / f"row014_t{t:06.1f}.jpg")
    for row, times in SWAP_TIMES.items():
        for t in times:
            rp.frame(t, rp.OUT / f"row{row:03d}_t{t:06.1f}.jpg")


if __name__ == "__main__":
    main()
