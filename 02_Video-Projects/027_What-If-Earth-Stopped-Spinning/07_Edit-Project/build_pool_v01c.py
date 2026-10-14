#!/usr/bin/env python3
"""Resolve 027's motion-row picks (ISS, ESO, sea spray, tide) and the coral retry on Wikimedia Commons
into pool_v01c.json for fetch_pool_v01.py --pool pool_v01c.json. Picked from pool_candidates_v01c.json. £0.

Usage: python3 build_pool_v01c.py
"""
from __future__ import annotations
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "OrbitWithBenEarthSpin/1.0 (owb studio)"}

PICKS = [
    # section, rows, Commons file title, file_id
    ("iss", "4 (v02) cirrus, 6 + 33 orbital sunrise, 2 + 13 night Europe",
     "File:Alexander Gerst’s Earth timelapses (2017 reissue).webm", "Gerst_Earth_timelapses_2017"),
    ("iss", "6, 33 orbital sunrise (alt)", "File:Sunrise To Sunset Aboard The ISS.ogv", "ISS_sunrise_to_sunset"),
    ("iss", "2, 11, 13 (alt, day + night passes)", "File:Five Minutes in Orbit (154728).webm", "Five_Minutes_in_Orbit"),
    ("stars", "7, 36 star time-lapse", "File:Time-lapse Over La Silla.webm", "ESO_timelapse_La_Silla"),
    ("stars", "7, 36 star trails still (alt)", "File:Star trails over the VLT in Paranal.jpg", "ESO_star_trails_VLT_Paranal"),
    ("sea", "12 sea spray on rocks", "File:Waves crashing on rocks off Beach 4, Kalaloch Beach, Washington 02.webm",
     "Kalaloch_waves_rocks_02"),
    ("tide", "23 tide in (pair with tide out)", "File:Bay of Fundy - Tide In.jpg", "Bay_of_Fundy_tide_in"),
    ("tide", "23 tide out", "File:Bay of Fundy - Tide Out.jpg", "Bay_of_Fundy_tide_out"),
    ("coral", "29 coral 2 (retry from pool_v01b)",
     "File:Eridophyllum seriale (fossil rugose coral) (Middle Devonian) 2 (35474153592).jpg", "Eridophyllum_seriale_2"),
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
(HERE / "pool_v01c.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False))
print("wrote pool_v01c.json", len(pool))
