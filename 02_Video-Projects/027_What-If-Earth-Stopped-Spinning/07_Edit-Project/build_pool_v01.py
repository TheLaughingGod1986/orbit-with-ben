#!/usr/bin/env python3
"""Resolve OWB 027 pool picks (POOL_v01_DRAFT.md + Claude #6081907573 rows 22/34) to pool_v01.json.

Each NASA id is resolved through images-api.nasa.gov/asset/<id> to its largest copy (~orig first, then
~large), so fetch_pool_v01.py can download it and picture_qa can check the 2.35x upscale limit. £0.

Usage: python3 build_pool_v01.py   (then: python3 fetch_pool_v01.py --sheets)
"""
from __future__ import annotations
import json, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenEarthSpin/1.0"}

PICKS = [
    # section, nasa_id, rows
    ("airborne", "ED07-0256-09", "2"),
    ("airborne", "AFRC2022-0059-49", "2 (alt)"),
    ("earth", "GSFC_20171208_Archive_e002130", "8 / 34 oceans"),
    ("earth", "GSFC_20171208_Archive_e002131", "18 (one use each)"),
    ("earth", "GSFC_20171208_Archive_e000265", "15 EPIC full Earth"),
    ("britain", "iss042e230335", "13 (check by eye)"),
    ("britain", "iss025e012937", "13 (check by eye)"),
    ("sun", "GSFC_20171208_Archive_e002035", "15, 35"),
    ("venus", "PIA23791", "22 (Mariner 10 only, Claude #6081907573)"),
    ("moon", "GSFC_20171208_Archive_e000868", "23"),
    ("moon", "GSFC_20171208_Archive_e001939", "26 (check: may be montage)"),
    ("moon", "as14-67-09386", "25 (Claude #6083184015: first choice, 4020 px)"),
    ("moon", "PIA13037", "25 fallback only (<=1.4x on near-black)"),
    ("eclipse", "NHQ201708210100", "27 (Claude #6083184015: full-frame totality)"),
    ("eclipse", "NHQ201708210116", "27 not used (13-frame sequence strip)"),
    ("kilauea", "PIA09968", "34 molten core (candidate)"),
    ("kilauea", "GSFC_20171208_Archive_e000658", "34 molten core (candidate)"),
    ("kilauea", "PIA22899", "34 molten core (candidate)"),
    ("greenland", "GSFC_20171208_Archive_e000112", "34 melting ice (candidate)"),
    ("greenland", "GSFC_20171208_Archive_e000213", "34 melting ice (candidate)"),
    ("greenland", "GSFC_20171208_Archive_e001753", "34 melting ice (candidate)"),
    ("greenland", "GSFC_20171208_Archive_e001754", "34 melting ice (candidate)"),
    ("greenland", "chutes-and-fissures-in-greenland_17572779961_o", "34 melting ice (candidate)"),
]


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def largest(nasa_id: str) -> str | None:
    hrefs = [i["href"] for i in fetch_json(f"https://images-api.nasa.gov/asset/{nasa_id}")["collection"]["items"]]
    hrefs = [h.replace("http://", "https://").replace(" ", "%20") for h in hrefs]
    for tag in ("~orig.jpg", "~orig.png", "~orig.tif", "~large.jpg", "~large.png", "~medium.jpg"):
        for h in hrefs:
            if h.lower().endswith(tag):
                return h
    return None


def title_of(nasa_id: str) -> str:
    items = fetch_json(f"https://images-api.nasa.gov/search?nasa_id={nasa_id}")["collection"]["items"]
    return items[0]["data"][0]["title"] if items else ""


pool, missing = [], []
for section, nid, rows in PICKS:
    try:
        orig = largest(nid)
    except Exception as e:  # noqa: BLE001
        orig, err = None, str(e)
    if not orig:
        missing.append(nid)
        print("MISS", nid)
        continue
    title = title_of(nid)
    pool.append({"section": section, "source": "nasa", "id": nid, "file_id": nid, "title": title,
                 "credit": "NASA (public domain)", "rows": rows, "orig": orig})
    print("ok  ", section, nid, orig.rsplit("/", 1)[-1])

(HERE / "pool_v01.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False) + "\n")
print(f"wrote pool_v01.json ({len(pool)} entries, {len(missing)} missing: {missing})")
