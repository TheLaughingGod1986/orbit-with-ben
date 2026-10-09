#!/usr/bin/env python3
"""025 Mars robot long thumbnails v03 (J0084 step 0, Cursor covering, 9 Oct 2026).

Claude (#6077231242): A (BUILT FOR 90 DAYS) still showed the PIA07372 mosaic's black wedge top-left and black
strip top-right. A pushes in about 10% (crop width 0.58 -> 0.52) and moves down-right so no mosaic black touches
any edge; same words. B and C are unchanged from v02.

  python3 _build_mars_robot_thumbs_v03.py
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
V02 = HERE / "abc_v02"
OUT = HERE / "abc_v03"

A = ("A", "built-for-90-days", ["BUILT FOR", "90 DAYS"], "90 DAYS", "opp_deck/PIA07372.jpg",
     "NASA/JPL Opportunity self-portrait, sols 322-323 (PIA07372)", (0.11, 0.55, 0.52),
     ("circle", 860, 430, 290), {"x_left": 40, "x_right": None, "y_top": 56})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    old = json.loads((V02 / "META.json").read_text())
    meta = {"version": "v03", "job": "J0084", "brief": "THUMB_BRIEF_v02.md", "title": v01.TITLE, "variants": []}
    key, slug, lines, hook, src, credit, crop, subj, pos = A
    im = v01.plate(src, crop)
    name = f"mars_robot_thumb_{key}_{slug}.jpg"
    info = house.place_text(im, lines, hook, subj, **pos)
    im.save(OUT / name, quality=94, optimize=True, subsampling=0)
    meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                             "source": credit, "crop_share": list(crop),
                             "near_black": house.near_black(im), **info})
    for v in old["variants"]:
        if v["key"] in ("B", "C"):
            shutil.copy2(V02 / v["file"], OUT / v["file"])
            meta["variants"].append(v)
    order = {"A": 0, "C": 1, "B": 2}
    meta["variants"].sort(key=lambda v: order[v["key"]])
    paths = [OUT / v["file"] for v in meta["variants"]]
    sheet = OUT / "mars_robot_thumbs_v03_small_size_check.jpg"
    subprocess.run([sys.executable, str(v01.REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(meta["variants"][0], indent=2, ensure_ascii=False))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
