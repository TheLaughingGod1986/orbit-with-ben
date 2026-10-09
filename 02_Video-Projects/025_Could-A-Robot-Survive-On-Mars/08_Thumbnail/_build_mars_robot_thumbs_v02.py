#!/usr/bin/env python3
"""025 Mars robot long thumbnails v02 (J0066, Cursor covering, 9 Oct 2026).

Claude's ideas sort (#6078316104, Gemini 3): C swaps "14 YEARS OF DUST" for a hazard hook from the locked
script, on a low-angle rover with wheels and mast showing, so Test & Compare has one peril variant against
A's triumph. A and B are unchanged from v01.

  python3 _build_mars_robot_thumbs_v02.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_mars_robot_thumbs_v01 as v01  # noqa: E402

house = v01.house
OUT = HERE / "abc_v02"

C = ("C", "minus-90-nights", ["MINUS 90°", "NIGHTS"], "MINUS 90°", "rover_work/PIA20316.jpg",
     "NASA/JPL-Caltech/MSSS Curiosity self-portrait at Namib Dune (PIA20316)", (0.0, 0.10, 1.0),
     ("circle", 870, 390, 300), {"x_left": 40, "x_right": None, "y_top": 56})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    old = json.loads((v01.OUT / "META.json").read_text())
    meta = {"version": "v02", "job": "J0066", "brief": "THUMB_BRIEF_v02.md", "title": v01.TITLE, "variants": []}
    paths = []
    for v in old["variants"]:
        if v["key"] in ("A", "B"):
            shutil.copy2(v01.OUT / v["file"], OUT / v["file"])
            paths.append(OUT / v["file"])
            meta["variants"].append(v)
    key, slug, lines, hook, src, credit, crop, subj, pos = C
    im = v01.plate(src, crop)
    name = f"mars_robot_thumb_{key}_{slug}.jpg"
    info = house.place_text(im, lines, hook, subj, **pos)
    im.save(OUT / name, quality=94, optimize=True, subsampling=0)
    paths.append(OUT / name)
    meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                             "source": credit, "crop_share": list(crop),
                             "near_black": house.near_black(im), **info})
    sheet = OUT / "mars_robot_thumbs_v02_small_size_check.jpg"
    subprocess.run([sys.executable, str(v01.REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(meta["variants"][-1], indent=2, ensure_ascii=False))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
