#!/usr/bin/env python3
"""Standalone Shorts S5-S8 (J0163): the same 0.4 s pause trim as S1-S4 (_pause_trim_v01.py), on vo_s5-s8_v01.

Writes vo_s5-s8_v01/trim/<stem>_trim.wav (git-ignored), <stem>_trim_words.json and pause_trim_meta.json. No spend.
"""
from __future__ import annotations

import json

import _pause_trim_v01 as v01

v01.VO = v01.HERE / "vo_s5-s8_v01"
v01.OUT = v01.VO / "trim"
STEMS = ["owb_sa_s5_shooting_stars_vo_v01", "owb_sa_s6_titan_vo_v01",
         "owb_sa_s7_pluto_heart_vo_v01", "owb_sa_s8_voyager1_vo_v01"]


def main() -> None:
    rows = [v01.trim(s) for s in STEMS]
    (v01.OUT / "pause_trim_meta.json").write_text(json.dumps(rows, indent=1) + "\n")
    for r in rows:
        print(f"{r['stem']}: {r['source_s']} s -> {r['trimmed_s']} s ({r['segments']} segments)")


if __name__ == "__main__":
    main()
