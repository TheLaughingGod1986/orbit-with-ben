#!/usr/bin/env python3
"""Build OWB 026 pool_v01.json from SHOT_LIST_v01 sources, resolving every ID live.

NASA ids resolve through images-api.nasa.gov (largest ~orig/~large asset); Commons files
through the Commons API; ESO / ESA-Hubble / ESA URLs are checked with a HEAD request.
Anything that does not resolve is left out and listed under "unresolved". £0.

Usage: python3 build_pool_v01.py   (writes pool_v01.json next to this file)
Then:  python3 fetch_pool_v01.py --sheets
"""
from __future__ import annotations
import json, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenNearestStar/1.0"}

ESO = "ESO (CC BY 4.0)"
NASA_PD = "NASA (public domain)"
WANT = [
    # section, kind, id, credit, rows, title
    ("proxima", "esahubble", "potw1343a", "ESA/Hubble & NASA (CC BY 4.0)", "long 3,5,6; Mon S2,S3", "Hubble image of Proxima Centauri"),
    ("proxima", "eso", "eso1629g", ESO, "long 7", "Proxima Centauri in the southern constellation of Centaurus"),
    ("proxima", "nasa", "GSFC_20171208_Archive_e000214", "NASA/ESA Hubble (public domain)", "long 7,21", "Hubble's best image of Alpha Centauri A and B"),
    ("alphacen", "eso", "eso1629i", "ESO/Digitized Sky Survey 2 (CC BY 4.0)", "long 7,21", "The sky around Alpha Centauri and Proxima Centauri"),
    ("alphacen", "eso", "eso1629b", ESO, "long 7", "The location of Proxima Centauri in the southern skies"),
    ("alphacen", "eso", "eso1702a", ESO, "long 7,21,33", "The Very Large Telescope and the star system Alpha Centauri"),
    ("proxima_b", "eso", "eso1629a", "ESO/M. Kornmesser (CC BY 4.0)", "long 28", "Artist's impression of Proxima b (1)"),
    ("proxima_b", "eso", "eso1629e", "ESO/M. Kornmesser (CC BY 4.0)", "long 29", "Artist's impression of Proxima b (2)"),
    ("proxima_b", "esovid", "eso1629d", ESO, "long 28 (option)", "A journey to Proxima Centauri and its planet (video, mute)"),
    ("proxima_b", "esovid", "eso1629e", ESO, "long 28-29 (option)", "A fly-through of the Proxima Centauri system (video, mute)"),
    ("sun", "nasa", "GSFC_20171208_Archive_e002035", NASA_PD, "long 6", "SDO full disk view of the Sun, 21 June 2010"),
    ("sun", "nasa", "GSFC_20160426_SDO_m12224_SolarFlare", NASA_PD, "long 30", "SDO view of the 17 April 2016 solar flare (video)"),
    ("earth_moon", "nasa", "GSFC_20171208_Archive_e002130", NASA_PD, "long 19,20; Fri S3", "NASA Blue Marble 2007 East"),
    ("earth_moon", "nasa", "GSFC_20171208_Archive_e001788", NASA_PD, "long 19,20; Fri S3", "Eastern Hemisphere - Blue Marble 2012"),
    ("earth_moon", "nasa", "GSFC_20171208_Archive_e000868", NASA_PD, "long 19", "Full Moon (LRO)"),
    ("voyager", "nasa", "PIA17049", "NASA/JPL-Caltech (public domain)", "long 22,25; Wed S1,S3,S4", "Voyager in space artist concept"),
    ("voyager", "nasa", "PIA21839", "NASA/JPL-Caltech (public domain)", "long 22,25; Wed S1,S3", "Voyager in deep space artist concept"),
    ("voyager", "nasa", "PIA17462", "NASA/JPL-Caltech (public domain)", "long 25", "Voyager 1 entering interstellar space artist concept"),
    ("voyager", "nasa", "PIA17464", "NASA/JPL-Caltech (public domain)", "long 22; Wed S2", "Voyager 1 launch 1977"),
    ("voyager", "nasa", "PIA21747", "NASA/JPL-Caltech (public domain)", "long 22; Wed S2", "Voyager 1 launch"),
    ("sail", "nasa", "ACD24-0020-061", NASA_PD, "long 31", "ACS3 test and final preparation for launch"),
    ("sail", "nasa", "CamA_Seq109_2024-08-28_17-17-11Z_V2_S560161", NASA_PD, "long 31", "ACS3 onboard view of sail and booms"),
    ("dsn", "nasa", "PIA23214", "NASA/JPL-Caltech (public domain)", "long 32", "Deep Space Network Goldstone complex"),
    ("dsn", "nasa", "PIA26147", "NASA/JPL-Caltech (public domain)", "long 32", "Six DSN antennas in Madrid arrayed"),
    ("gaia", "url", "gaia_sky_in_colour", "ESA/Gaia/DPAC (CC BY-SA 3.0 IGO)", "long 15",
     "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2018/04/gaia_s_sky_in_colour2/17475368-10-eng-GB/Gaia_s_sky_in_colour.jpg"),
    ("portraits", "commons", "File:Tycho Brahe.JPG", "Public domain painting (Wikimedia Commons)", "long 13", "Portrait of Tycho Brahe"),
    ("portraits", "commons", "File:Friedrich Wilhelm Bessel (1839 painting).jpg", "Public domain painting, C. A. Jensen 1839 (Wikimedia Commons)", "long 14", "Portrait of Friedrich Bessel"),
]


def get_json(url: str):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def head_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def nasa_orig(nid: str) -> str | None:
    hrefs = [i["href"] for i in get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(nid)}")["collection"]["items"]]
    for tag in ("~orig.mp4", "~large.mp4", "~orig.jpg", "~orig.tif", "~large.jpg", "~orig.png"):
        for h in hrefs:
            if h.endswith(tag):
                return h.replace("http://", "https://").replace(" ", "%20")
    return None


def commons_url(title: str) -> str | None:
    q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "format": "json"})
    pages = get_json(f"https://commons.wikimedia.org/w/api.php?{q}")["query"]["pages"]
    for p in pages.values():
        if p.get("imageinfo"):
            return p["imageinfo"][0]["url"]
    return None


pool, unresolved = [], []
for section, kind, fid, credit, rows, title in WANT:
    try:
        if kind == "nasa":
            url = nasa_orig(fid)
        elif kind == "eso":
            url = f"https://cdn.eso.org/images/large/{fid}.jpg"
        elif kind == "esovid":
            url = f"https://cdn.eso.org/videos/hd_and_apple/{fid}.m4v"
        elif kind == "esahubble":
            url = f"https://cdn.esahubble.org/archives/images/large/{fid}.jpg"
        elif kind == "commons":
            url = commons_url(fid)
        else:
            url, title = title, fid.replace("_", " ")
        if kind != "nasa" and url and not head_ok(url):
            url = None
    except Exception as e:  # noqa: BLE001
        url = None
        print("ERR", fid, e)
    file_id = fid.split(":", 1)[-1].rsplit(".", 1)[0].replace(" ", "_").replace("(", "").replace(")", "")
    if kind == "esovid":
        file_id += "_video"
    entry = {"section": section, "source": kind, "id": fid, "file_id": file_id, "title": title, "credit": credit, "rows": rows, "orig": url}
    (pool if url else unresolved).append(entry)
    print("ok  " if url else "MISS", section, fid, url or "")

(HERE / "pool_v01.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False) + "\n")
print(f"pool={len(pool)} unresolved={len(unresolved)}")
for u in unresolved:
    print("  unresolved:", u["id"])
