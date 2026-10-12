#!/usr/bin/env python3
"""Standalone Shorts S5-S8 (J0163): pull candidate NASA plates from images-api.nasa.gov (free, no spend).

Same as _harvest_plates_v01.py (S1-S4): images to /private/tmp/owb_sa_shorts/plates/<short>/, a contact sheet per
Short, and plates_v02.json here (NASA id, title, date, source page, size).
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

import _harvest_plates_v01 as v01

HERE = Path(__file__).resolve().parent
CANDIDATES = {
    "s5_meteors": ["NHQ202108110003", "NHQ202108110001", "NHQ202108110005", "NHQ202108100009", "NHQ202508030001",
                   "ARC-2007-ACD07-0152-035"],
    "s6_titan": ["PIA06230", "PIA09739", "PIA06997", "PIA21625", "PIA07232", "PIA02238", "PIA14925"],
    "s7_pluto": ["PIA19708", "PIA20202", "PIA19952", "PIA19841", "PIA20726", "PIA21863", "PIA20336"],
    "s8_voyager": ["PIA17049", "PIA04495", "PIA00452", "PIA23645", "PIA17464", "PIA21741"],
}


def main() -> None:
    rows = {}
    for short, ids in CANDIDATES.items():
        d = v01.WORK / short
        d.mkdir(parents=True, exist_ok=True)
        tiles = []
        rows[short] = []
        for nid in ids:
            try:
                url = v01.pick_asset(nid)
                dest = d / f"{nid}{Path(url).suffix.lower()}"
                if not dest.exists():
                    urllib.request.urlretrieve(url, dest)
                with Image.open(dest) as im:
                    size = im.size
                    t = im.convert("RGB")
                    t.thumbnail((360, 360))
                    tiles.append((nid, t.copy(), size))
                rows[short].append({"nasa_id": nid, "url": url, "page": f"https://images.nasa.gov/details/{nid}",
                                    "size": list(size), **v01.meta(nid)})
                print(short, nid, size, flush=True)
            except Exception as e:  # noqa: BLE001
                rows[short].append({"nasa_id": nid, "error": str(e)})
                print(short, nid, "ERROR", e, flush=True)
        sheet = Image.new("RGB", (370 * max(1, len(tiles)), 400), (20, 20, 20))
        dr = ImageDraw.Draw(sheet)
        for i, (nid, t, size) in enumerate(tiles):
            sheet.paste(t, (370 * i + 5, 5))
            dr.text((370 * i + 8, 375), f"{nid} {size[0]}x{size[1]}", fill=(255, 255, 255))
        sheet.save(v01.WORK / f"{short}_contact.jpg", quality=88)
    (HERE / "plates_v02.json").write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
