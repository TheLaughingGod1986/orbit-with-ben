#!/usr/bin/env python3
"""Render static preview frames for the Orbit Shorts caption style."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from onscreen_captions import render_beat_png, render_cta_png  # noqa: E402

OUT = ROOT.parent / "_caption_style_previews"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLES = [
    ("01_reality_directly.png", [("reality directly", "yellow")]),
    ("02_your.png", [("your", "white")]),
    ("03_your_senses_first.png", [("your", "yellow"), ("senses", "white"), ("first", "yellow")]),
    ("04_because_everything.png", [("because everything", "yellow")]),
    ("05_glass_rain.png", [("it rains", "yellow"), ("glass", "white"), ("sideways", "yellow")]),
    ("06_never_come_back.png", [("cross this line", "yellow"), ("and you never", "white"), ("come back", "yellow")]),
]


def main() -> None:
    for name, lines in SAMPLES:
        render_beat_png(OUT / name, lines)
        print(OUT / name)
    render_cta_png(OUT / "07_cta.png")
    print(OUT / "07_cta.png")
    print("OK", OUT)


if __name__ == "__main__":
    main()
