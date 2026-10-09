#!/usr/bin/env python3
"""Search the motion rows still open in 027's pool: ISS (images-api video), ESO star trails and
NOAA spray/tide (Wikimedia Commons files, which carry the ESO and NOAA uploads with their licence).

Writes pool_candidates_v01c.json (title, size, duration, licence, page). £0.

Usage: python3 search_pool_v01c.py
"""
from __future__ import annotations
import json, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "OrbitWithBenEarthSpin/1.0 (owb studio; contact via commons)"}

NASA = [
    # key, rows, query
    ("iss_cirrus", "4 (v02), 11", "time-lapse clouds International Space Station"),
    ("iss_sunrise", "6, 33", "sunrise from the International Space Station"),
    ("iss_europe_night", "2, 13", "Europe at night International Space Station"),
    ("iss_timelapse", "2, 6, 13, 33", "ISS Earth time-lapse"),
    ("iss_terminator", "1, 37 alt", "orbital sunset time-lapse space station"),
]
COMMONS = [
    ("eso_star_trails", "7, 36", "ESO time-lapse star trails filetype:video"),
    ("eso_timelapse", "7, 36", "Paranal night sky timelapse filetype:video"),
    ("star_trails_still", "7, 36", "ESO star trails Paranal"),
    ("noaa_spray", "12", "waves crashing rocks filetype:video"),
    ("noaa_spray_still", "12", "NOAA waves breaking rocky shore"),
    ("tide_timelapse", "23", "tide time-lapse harbour filetype:video"),
    ("tide_still", "23", "Bay of Fundy low tide boats"),
]


def get(url: str) -> dict:
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if i == 2:
                raise
            time.sleep(5 * (i + 1))
    return {}


def nasa(q: str) -> list[dict]:
    url = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "video", "page_size": 15})
    out = []
    for it in get(url)["collection"]["items"][:15]:
        d = it["data"][0]
        out.append({"nasa_id": d.get("nasa_id"), "title": d.get("title"), "center": d.get("center"),
                    "date": (d.get("date_created") or "")[:10], "desc": (d.get("description") or "")[:240]})
    return out


def commons(q: str) -> list[dict]:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": q, "gsrnamespace": 6,
        "gsrlimit": 15, "prop": "imageinfo", "iiprop": "size|mime|url|extmetadata",
        "iiextmetadatafilter": "LicenseShortName|Artist"})
    pages = get(url).get("query", {}).get("pages", {})
    out = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        out.append({"title": p["title"], "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"),
                    "dur": ii.get("duration"), "licence": md.get("LicenseShortName", {}).get("value"),
                    "artist": (md.get("Artist", {}).get("value") or "")[:120], "page": ii.get("descriptionurl")})
    return out


res: dict = {}
for key, rows, q in NASA:
    try:
        res[key] = {"rows": rows, "src": "images-api", "query": q, "hits": nasa(q)}
    except Exception as e:  # noqa: BLE001
        res[key] = {"rows": rows, "src": "images-api", "query": q, "error": str(e)}
    print(key, len(res[key].get("hits", [])), flush=True)
for key, rows, q in COMMONS:
    try:
        res[key] = {"rows": rows, "src": "commons", "query": q, "hits": commons(q)}
    except Exception as e:  # noqa: BLE001
        res[key] = {"rows": rows, "src": "commons", "query": q, "error": str(e)}
    print(key, len(res[key].get("hits", [])), flush=True)
    time.sleep(2)
(HERE / "pool_candidates_v01c.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print("wrote pool_candidates_v01c.json")
