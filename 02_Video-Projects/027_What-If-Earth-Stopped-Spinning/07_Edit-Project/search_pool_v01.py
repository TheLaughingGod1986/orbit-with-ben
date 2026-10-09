#!/usr/bin/env python3
"""Search images-api.nasa.gov for OWB 027 pool candidates, one query per SHOT_LIST_v01 need.

Writes pool_candidates_v01.json (top hits per need: nasa_id, media, title, centre, date) so the
pool can be picked by title before build_pool_v01.py resolves the chosen IDs. £0.

Usage: python3 search_pool_v01.py
"""
from __future__ import annotations
import json, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenEarthSpin/1.0"}

NEEDS = [
    # key, rows, media_type, query
    ("epic_turning", "1,15,37", "video", "DSCOVR EPIC Earth rotation"),
    ("iss_terminator", "1,37", "video", "ISS time-lapse terminator night day"),
    ("airborne_jet", "2", "image", "DC-8 airborne science flight"),
    ("airborne_er2", "2", "image", "ER-2 in flight"),
    ("iss_europe_night", "2,13", "video", "ISS time-lapse Europe night"),
    ("iss_britain_night", "13", "image", "ISS night British Isles London"),
    ("orbital_sunrise", "6,33", "video", "orbital sunrise space station"),
    ("cirrus_iss", "4 (v02)", "video", "jet stream clouds space station"),
    ("cirrus_iss_img", "4 (v02)", "image", "jet stream cirrus clouds astronaut photograph"),
    ("blue_marble", "8,18", "image", "Blue Marble"),
    ("sdo_sun", "15,35", "image", "SDO full disk Sun"),
    ("epic_full", "15", "image", "EPIC DSCOVR full Earth"),
    ("magellan_venus", "22", "image", "Magellan Venus global view"),
    ("venus_clouds", "22", "image", "Venus clouds Mariner 10"),
    ("lro_full_moon", "23", "image", "LRO full Moon"),
    ("lro_far_side", "26", "image", "Moon far side LRO"),
    ("apollo_retro", "25", "image", "AS11-40-5952"),
    ("eclipse_2024", "27", "image", "total solar eclipse 2024 corona"),
    ("eclipse_path_svs", "28", "video", "2024 eclipse path animation"),
    ("earth_interior", "34", "image", "Earth interior core cutaway"),
    ("icebridge_greenland", "34", "image", "Operation IceBridge Greenland ice sheet"),
    ("young_earth", "37", "image", "Moon forming impact artist"),
    ("tide_harbour", "23", "video", "tide time-lapse"),
    ("sea_spray", "12", "video", "waves crashing rocky coast"),
]


def search(q: str, media: str) -> list[dict]:
    url = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": media, "page_size": 12})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        items = json.load(r)["collection"]["items"]
    out = []
    for it in items[:12]:
        d = it["data"][0]
        out.append({"nasa_id": d.get("nasa_id"), "media": d.get("media_type"), "title": d.get("title"),
                    "center": d.get("center"), "date": (d.get("date_created") or "")[:10]})
    return out


res = {}
for key, rows, media, q in NEEDS:
    try:
        res[key] = {"rows": rows, "query": q, "hits": search(q, media)}
    except Exception as e:  # noqa: BLE001
        res[key] = {"rows": rows, "query": q, "error": str(e)}
    print(key, len(res[key].get("hits", [])), flush=True)
(HERE / "pool_candidates_v01.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print("wrote pool_candidates_v01.json")
