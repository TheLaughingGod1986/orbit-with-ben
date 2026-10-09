#!/usr/bin/env python3
"""Build OWB 026 pool_v02.json: pool_v01 plus more plates, resolving every new ID live (J0065, Cursor covering, 9 Oct 2026).

Why: with every picture capped at two uses and every hold at 6 s, v01's 27 items cover at most ~370 s of the 494 s cut.
v02 adds real night-sky / Milky Way photos (frame 0 and the row 33 return, until Claude names ESO time-lapses), more
Voyager, DSN, ACS3, SDO, Moon and night-Earth plates (City Lights of the Nile for the London-Cairo row). ESO ids were
checked against their ESO page titles; annotated or diagram versions (eso1629c/f/j, eso1241b) are left out, and so is potw1606a
(a transporter truck, not sky). £0.

Usage: python3 build_pool_v02.py   then   python3 fetch_pool_v01.py --pool pool_v02.json --sheets
"""
from __future__ import annotations
import json, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenNearestStar/1.0"}
ESO = "ESO (CC BY 4.0)"
NASA_PD = "NASA (public domain)"
JPL = "NASA/JPL-Caltech (public domain)"
ADD = [
    # section, kind, id, credit, rows, title
    ("nightsky", "eso", "eso0932a", "ESO/S. Brunier (CC BY 4.0)", "long 1,2,33 (pan; stands in for the time-lapse)", "The Milky Way panorama"),
    ("nightsky", "eso", "eso0934a", "ESO/S. Guisard (CC BY 4.0)", "long 2,10,17", "A 340-million pixel starscape from Paranal"),
    ("alphacen", "eso", "eso1702b", ESO, "long 7,21", "The Alpha Centauri star system"),
    ("nightsky", "nasa", "iss073e0982261", NASA_PD, "long 1,2,10", "The Milky Way spans the night sky above a yellow-green airglow (ISS)"),
    ("nightsky", "nasa", "iss073e0982679", NASA_PD, "long 10,17,21", "The Milky Way spans the night sky above an orange-yellow airglow (ISS)"),
    ("nightsky", "nasa", "KSC-20191031-PH-GEB01_0005", NASA_PD, "long 7,21", "Night sky over Kennedy Space Center"),
    ("nightsky", "nasa", "KSC-20191031-PH-GEB01_0003", NASA_PD, "long 7,21", "Night sky over Kennedy Space Center (2)"),
    ("nightsky", "nasa", "GSFC_20171208_Archive_e000256", "NASA/ESA Hubble (public domain)", "long 10,17,21", "A Hubble sky full of stars"),
    ("voyager", "nasa", "PIA04495", JPL, "long 22,25", "Artist concept of Voyager"),
    ("voyager", "nasa", "PIA14111", JPL, "long 25", "Model of Voyager artist concept"),
    ("voyager", "nasa", "PIA21746", JPL, "long 22", "Voyager 1 launch (2)"),
    ("voyager", "nasa", "PIA21739", JPL, "long 22", "Voyager 1's launch vehicle"),
    ("dsn", "nasa", "PIA25136", JPL, "long 32", "A new antenna for NASA's Deep Space Network"),
    ("dsn", "nasa", "PIA25137", JPL, "long 32", "The Deep Space Network's new DSS-53 at night"),
    ("dsn", "nasa", "PIA24163", JPL, "long 32", "New all-in-one antenna for the Deep Space Network"),
    ("sail", "nasa", "CamC_Seq109_2024-08-28_17-17-13Z_V2_S595171", NASA_PD, "long 31", "ACS3 onboard view of sail and booms (camera C)"),
    ("sail", "nasa", "CamB_Seq109_2024-08-28_17-17-12Z_V2_S577666", NASA_PD, "long 31", "ACS3 onboard view of sail and booms (camera B)"),
    ("sail", "nasa", "ACS3_SolarPanels_001", NASA_PD, "long 31", "ACS3 artist's concept"),
    ("sun", "nasa", "GSFC_20171208_Archive_e000790", NASA_PD, "long 6,30", "SDO sees giant filament on the Sun"),
    ("sun", "nasa", "GSFC_20171208_Archive_e000759", NASA_PD, "long 6", "Two coronal holes on the Sun (SDO)"),
    ("sun", "nasa", "GSFC_20171208_Archive_e000885", NASA_PD, "long 19", "SDO shows the Moon transiting the Sun"),
    ("earth_moon", "nasa", "GSFC_20171208_Archive_e001982", NASA_PD, "long 19", "The Moon"),
    ("earth_moon", "nasa", "GSFC_20171208_Archive_e001586", NASA_PD, "long 20", "City lights illuminate the Nile"),
    ("earth_moon", "nasa", "iss025e015176", NASA_PD, "long 19,20", "Night view of Earth (Expedition 25)"),
]


def get_json(url: str):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def head_ok(url: str) -> bool:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA, method="HEAD"), timeout=30) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def nasa_orig(nid: str) -> str | None:
    hrefs = [i["href"] for i in get_json(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(nid)}")["collection"]["items"]]
    for tag in ("~orig.jpg", "~orig.tif", "~large.jpg", "~orig.png"):
        for h in hrefs:
            if h.endswith(tag):
                return h.replace("http://", "https://").replace(" ", "%20")
    return None


pool = json.loads((HERE / "pool_v01.json").read_text())
have = {p["id"] for p in pool}
unresolved = []
for section, kind, fid, credit, rows, title in ADD:
    if fid in have:
        continue
    try:
        url = nasa_orig(fid) if kind == "nasa" else f"https://cdn.eso.org/images/large/{fid}.jpg"
        if kind != "nasa" and not head_ok(url):
            url = None
    except Exception as e:  # noqa: BLE001
        url = None
        print("ERR", fid, e)
    entry = {"section": section, "source": kind, "id": fid, "file_id": fid, "title": title, "credit": credit, "rows": rows, "orig": url}
    (pool if url else unresolved).append(entry)
    print("ok  " if url else "MISS", section, fid, url or "")

(HERE / "pool_v02.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False) + "\n")
print(f"pool={len(pool)} added={len(pool) - len(have)} unresolved={len(unresolved)}")
for u in unresolved:
    print("  unresolved:", u["id"])
