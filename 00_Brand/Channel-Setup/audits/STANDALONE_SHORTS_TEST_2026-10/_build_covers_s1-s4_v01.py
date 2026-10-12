#!/usr/bin/env python3
"""Standalone Shorts S1-S4 custom covers v01 (J0163 step 7).

The plate is each Short's frame-0 picture with no burned-in text, drawn by the assembler's own Plate class at the
opening zoom. Words are house v04 (Arial Black, yellow hook word, white rest) in the 16:9 centre band, so both crops
keep them (THUMBNAIL_AND_TITLE_RULES.md §2.6, §2.7). Cover words add to the title and never repeat it (§2.3).
No Orbit. Does not upload; covers are set in Studio after Chief's PASS (J0164).

  python3 _build_covers_s1-s4_v01.py [s1 s2 s3 s4]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import _assemble_standalone_shorts_v01 as asm  # noqa: E402
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

OUT = HERE / "08_Covers"
PLATE_DIR = asm.WORK / "covers_v01"

COVERS = {
    "s1": {"lines": ["SLOWEST", "SUNRISE"], "yellow": {"SLOWEST"}, "hero": 1},
    "s2": {"lines": ["2,000 KM/H", "WINDS"], "yellow": {"2,000"}, "hero": 0},
    "s3": {"lines": ["DAWN EACH", "90 MINUTES"], "yellow": {"90"}, "hero": 1},
    "s4": {"lines": ["TIPPED ON", "ITS SIDE"], "yellow": {"SIDE"}, "hero": 1},
}


def frame0(key: str) -> Path:
    spec = asm.SHORTS[key]
    _, rel, mode, cx, cy, z0, _ = spec["rows"][0]
    plate = asm.Plate(asm.PLATES / rel, mode, cx, cy)
    if "open_pan" in spec:
        cx = spec["open_pan"][0]
    im = plate.frame(z0, cx).convert("RGB")
    PLATE_DIR.mkdir(parents=True, exist_ok=True)
    out = PLATE_DIR / f"{spec['stem']}_frame0.png"
    im.save(out)
    return out


def main() -> None:
    keys = [k for k in sys.argv[1:] if k in COVERS] or list(COVERS)
    rows = []
    for key in keys:
        spec, cov = asm.SHORTS[key], COVERS[key]
        title = " ".join(spec["title"])
        overlap = {w.strip(",").upper() for l in cov["lines"] for w in l.split()} & {
            w.strip(",").upper() for w in title.split()}
        if overlap:
            raise SystemExit(f"{key}: cover repeats title words {sorted(overlap)} (§2.3)")
        row = v04.compose(dict(cov, id=spec["stem"], plate=frame0(key), out_dir=OUT, related="",
                               uk=f"{spec['air']}T11:30:00+01:00", role="owb_standalone_test"))
        row.update(title=title, source=spec["rows"][0][1])
        rows.append(row)
        print("wrote", row["file"])
    (OUT / "MANIFEST.json").write_text(json.dumps(
        {"version": "owb_standalone_covers_v01", "job": "J0163", "font": v04.FONT_PATH, "size": [v04.W, v04.H],
         "note": "9:16, words in the 16:9 centre band; frame-0 plate, no Orbit. Set in Studio after Chief PASS.",
         "shorts": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
