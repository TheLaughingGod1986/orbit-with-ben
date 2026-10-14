#!/usr/bin/env python3
"""Standalone Shorts S1-S4 (J0163): pull candidate NASA plates from images-api.nasa.gov (free, no spend).

Writes the images to /private/tmp/owb_sa_shorts/plates/<short>/ (media stays off git), a contact sheet per Short,
and plates_v01.json here (NASA id, title, date, source URL, size) so the picks can be checked against their pages.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
WORK = Path("/private/tmp/owb_sa_shorts/plates")
CANDIDATES = {
    "s1_mercury": ["PIA13674", "PIA11351", "PIA14083", "PIA12266", "PIA12842"],
    "s2_neptune": ["PIA01492", "PIA00058", "PIA02210", "PIA01982", "PIA00063"],
    "s3_iss": ["iss040e080833", "iss061e123823", "iss054e002538", "iss059e027932", "iss064e044526"],
    "s4_uranus": ["PIA18182", "PIA00346", "PIA01391", "PIA00143"],
}


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def pick_asset(nasa_id: str) -> str:
    hrefs = [i["href"] for i in get_json(f"https://images-api.nasa.gov/asset/{nasa_id}")["collection"]["items"]]
    jpgs = [h for h in hrefs if h.lower().endswith((".jpg", ".jpeg", ".png", ".tif"))]
    for tag in ("~orig", "~large", "~medium"):
        for h in jpgs:
            if tag in h and not h.lower().endswith(".tif"):
                return h.replace("http://", "https://")
    return jpgs[0].replace("http://", "https://")


def meta(nasa_id: str) -> dict:
    item = get_json(f"https://images-api.nasa.gov/search?nasa_id={nasa_id}")["collection"]["items"][0]["data"][0]
    return {"title": item.get("title", ""), "date": item.get("date_created", "")[:10],
            "center": item.get("center", ""), "description": item.get("description", "")[:300]}


def main() -> None:
    rows = {}
    for short, ids in CANDIDATES.items():
        d = WORK / short
        d.mkdir(parents=True, exist_ok=True)
        tiles = []
        rows[short] = []
        for nid in ids:
            try:
                url = pick_asset(nid)
                dest = d / f"{nid}{Path(url).suffix.lower()}"
                if not dest.exists():
                    urllib.request.urlretrieve(url, dest)
                with Image.open(dest) as im:
                    size = im.size
                    t = im.convert("RGB")
                    t.thumbnail((360, 360))
                    tiles.append((nid, t.copy(), size))
                rows[short].append({"nasa_id": nid, "url": url, "page": f"https://images.nasa.gov/details/{nid}",
                                    "size": list(size), **meta(nid)})
                print(short, nid, size, flush=True)
            except Exception as e:  # noqa: BLE001
                rows[short].append({"nasa_id": nid, "error": str(e)})
                print(short, nid, "ERROR", e, flush=True)
        sheet = Image.new("RGB", (370 * max(1, len(tiles)), 400), (20, 20, 20))
        dr = ImageDraw.Draw(sheet)
        for i, (nid, t, size) in enumerate(tiles):
            sheet.paste(t, (370 * i + 5, 5))
            dr.text((370 * i + 8, 375), f"{nid} {size[0]}x{size[1]}", fill=(255, 255, 255))
        sheet.save(WORK / f"{short}_contact.jpg", quality=88)
    (HERE / "plates_v01.json").write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
