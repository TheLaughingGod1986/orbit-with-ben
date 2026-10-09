#!/usr/bin/env python3
"""Resolve 027's last open rows (28 eclipse path, 32 second NIST plate, 37 young Earth) on Wikimedia Commons
into pool_v01d.json for fetch_pool_v01.py --pool pool_v01d.json. Picked from Commons searches on 9 Oct (rows 28, 32 second plate, 37). £0.

Usage: python3 build_pool_v01d.py
"""
from __future__ import annotations
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "OrbitWithBenEarthSpin/1.0 (owb studio)"}

PICKS = [
    # section, rows, Commons file title, file_id
    ("eclipse", "28 eclipse path (NASA SVS flyover, no-text version)",
     "File:2024 Path of Totality (SVS5219 - eclipse2024 flyover notext 2160p30).webm", "SVS5219_path_of_totality_notext"),
    ("eclipse", "28 eclipse shadow (real NOAA satellite view, no-text version)",
     "File:NOAA Satellites View Total Solar Eclipse (NESDIS 2024-04-12 2024-4-12-Total-Solar-Eclipse-NO-TEXT).webm",
     "NOAA_sat_eclipse_2024_notext"),
    ("nist", "32 second NIST lab plate", "File:Ytterbium Lattice Atomic Clock (10444764266).jpg", "NIST_ytterbium_lattice_clock"),
    ("nist", "32 second NIST lab plate (alt)", "File:Atomic Clock006.jpg", "NIST_atomic_clock_006"),
    ("young", "37 young Earth art", "File:BENNU’S JOURNEY - Early Earth.jpg", "NASA_Bennu_journey_early_Earth"),
    ("young", "37 young Earth art (alt)", "File:Hadean.png", "Hadean_Bertelink"),
]


def query(titles: list[str]) -> dict:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": "|".join(titles), "prop": "imageinfo",
        "iiprop": "size|mime|url|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist"})
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if i == 4:
                raise
            print("  retry", e, flush=True)
            time.sleep(15 * (i + 1))
    return {}


pages = {p["title"]: p for p in query([t for _, _, t, _ in PICKS])["query"]["pages"].values()}
pool = []
for sec, rows, title, fid in PICKS:
    p = pages.get(title.replace("_", " "))
    ii = ((p or {}).get("imageinfo") or [{}])[0]
    if not ii.get("url"):
        print("MISS", title)
        continue
    md = ii.get("extmetadata", {})
    lic = md.get("LicenseShortName", {}).get("value", "")
    artist = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
    pool.append({"section": sec, "source": "commons", "id": title, "file_id": fid, "title": title[5:],
                 "credit": f"{artist} / Wikimedia Commons, {lic}", "licence": lic, "rows": rows,
                 "orig": ii["url"], "page": ii.get("descriptionurl"), "w": ii.get("width"), "h": ii.get("height"),
                 "mime": ii.get("mime"), "dur": ii.get("duration"), "mb": round(ii.get("size", 0) / 1e6, 1)})
    print(f"{sec:6} {fid:32} {ii.get('width')}x{ii.get('height')} {pool[-1]['mb']} MB {lic} | {artist[:50]}")
(HERE / "pool_v01d.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False))
print("wrote pool_v01d.json", len(pool))
