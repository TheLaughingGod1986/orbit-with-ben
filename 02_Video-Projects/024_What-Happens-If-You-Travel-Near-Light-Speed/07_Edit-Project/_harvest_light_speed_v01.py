#!/usr/bin/env python3
"""024 light speed: harvest v01 (J0042). Checks each item's published title before it enters the pool.

  python3 _harvest_light_speed_v01.py   # -> nasa_pool_v01/024_harvest_v01/, _evidence/light_speed_harvest_v01.json

NASA images library = public domain (NASA media guidelines). Commons items carry the licence read from the file page.
Media stays out of git.
"""
from __future__ import annotations
import datetime, json, sys, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "nasa_pool_v01" / "024_harvest_v01"
EVIDENCE = HERE / "_evidence" / "light_speed_harvest_v01.json"
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenLightSpeedHarvest/1.0"}

# (rows, nasa_id, words that must appear in the published title, media)
NASA = [
    ("2", "Earth Views from the International Space Station", "Earth Views", "video"),
    ("8", "PIA24573", "Atomic Clock", "image"),
    ("10,27", "iss035e017673", "Earth Observation", "image"),
    ("10,27", "iss040e091231", "Earth Observation", "image"),
    ("10,27,36", "iss040e085126", "Earth Observation", "image"),
    ("11,28", "EC00-0050-001", "DC-8 Airborne Laboratory", "image"),
    ("11,28", "EC98-44444-004", "DC-8 Airborne Laboratory", "image"),
    ("11,28", "ED07-0256-09", "DC-8", "image"),
    ("18,38", "iss071e439624", "orbital sunrise", "image"),
    ("21", "KSC-20221116-MH-AJN01-0001-Artemis_I_Isolated_Launch_Views-3314595", "Artemis I", "video"),
    ("22,36", "NHQ_2019_0626_Earth Views from the ISS", "Earth Views", "video"),
    ("23", "sts33-17-005a", "drink", "image"),
    ("23", "iss019e018483", "water", "image"),
    ("29", "SSC-20240229-s00309", "RS-25", "image"),
    ("29", "SSC-2015-00064", "Lighting up the Night", "image"),
    ("30", "GSFC_20171208_Archive_e001593", "Black Marble", "image"),
    ("32", "sts080-326-010", "debris impact", "image"),
    ("33", "NHQ201808120013", "Parker Solar Probe", "image"),
    ("34", "ACS3_SolarSailSunrise", "Solar Sail", "image"),
    ("34", "ACS3_LookingDown", "Solar Sail", "image"),
]

COMMONS = [
    ("5,7,38", "File:GPS Block IIIA.jpg", "Public domain", "U.S. Air Force (GPS.gov)"),
    ("35", "File:Gaia\u2019s sky in colour ESA393127.jpg", "CC BY-SA 3.0 igo", "ESA/Gaia/DPAC"),
]

BAD_WORDS = ("ISSpresso", "AccuSoft", "All right", "Breakthrough", "Lockheed", "image courtesy", "photo courtesy")


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url.replace(" ", "%20"), headers=UA), timeout=120) as r:
        return json.load(r)


def download(url, dest: Path) -> int:
    if dest.exists() and dest.stat().st_size > 20_000:
        return dest.stat().st_size
    with urllib.request.urlopen(urllib.request.Request(url.replace(" ", "%20"), headers=UA), timeout=600) as r:
        data = r.read()
    if len(data) < 20_000 or data[:15].lower().startswith((b"<!doctype", b"<html")):
        raise RuntimeError(f"bad body {len(data)} bytes")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def pick(files, media):
    files = [f.replace("http://", "https://") for f in files]
    if media == "video":
        for tag in ("~medium.mp4", "~orig.mp4", "~large.mp4", "~mobile.mp4"):
            hit = [f for f in files if f.endswith(tag)]
            if hit:
                return hit[0]
    for tag in ("~orig.jpg", "~orig.jpeg", "~orig.png", "~orig.tif", "~large.jpg"):
        hit = [f for f in files if f.lower().endswith(tag)]
        if hit:
            return hit[0]
    return None


def main():
    items, rejected = [], []
    for rows, nid, must, media in NASA:
        q = get_json("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"nasa_id": nid}))
        hits = q["collection"]["items"]
        if not hits:
            rejected.append({"row": rows, "nasa_id": nid, "why": "not found"}); continue
        m = hits[0]["data"][0]
        title = m.get("title", "")
        blob = " ".join(str(m.get(k, "")) for k in ("title", "description", "secondary_creator", "photographer"))
        if must.lower() not in title.lower():
            rejected.append({"row": rows, "nasa_id": nid, "title": title, "why": f"title lacks '{must}'"}); continue
        bad = [w for w in BAD_WORDS if w.lower() in blob.lower()]
        if bad:
            rejected.append({"row": rows, "nasa_id": nid, "title": title, "why": f"flag words {bad}"}); continue
        files = get_json(hits[0]["href"])
        url = pick(files, media)
        if not url:
            rejected.append({"row": rows, "nasa_id": nid, "title": title, "why": "no usable rendition"}); continue
        ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
        dest = OUT / f"{nid.replace(' ', '_')}{ext}"
        try:
            size = download(url, dest)
        except Exception as e:
            rejected.append({"row": rows, "nasa_id": nid, "title": title, "why": f"download: {e}"}); continue
        who = m.get("secondary_creator") or m.get("photographer") or ""
        items.append({
            "row": rows, "id": nid, "media": media, "title": title, "center": m.get("center"),
            "date": (m.get("date_created") or "")[:10], "source_url": f"https://images.nasa.gov/details/{urllib.parse.quote(nid)}",
            "file_url": url, "file": str(dest.relative_to(HERE)), "bytes": size,
            "licence": "Public domain (NASA images library; NASA media usage guidelines)",
            "credit": f"NASA{(' / ' + who) if who and 'NASA' not in who else (' (' + who + ')' if who else '')}",
        })
        print("ok ", rows, nid, "|", title)
    for rows, title, want_lic, credit in COMMONS:
        q = get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url|size|extmetadata", "titles": title}))
        page = next(iter(q["query"]["pages"].values()))
        ii = page["imageinfo"][0]
        lic = ii["extmetadata"].get("LicenseShortName", {}).get("value", "")
        if lic.lower() != want_lic.lower():
            rejected.append({"row": rows, "id": title, "why": f"licence '{lic}' != '{want_lic}'"}); continue
        url = ii["url"].split("?")[0]
        dest = OUT / Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).name
        size = download(url, dest)
        items.append({
            "row": rows, "id": title, "media": "image", "title": page["title"],
            "source_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(page["title"].replace(" ", "_")),
            "file_url": url, "file": str(dest.relative_to(HERE)), "bytes": size, "w": ii["width"], "h": ii["height"],
            "licence": lic, "credit": credit,
        })
        print("ok ", rows, title, "|", lic)
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps({
        "date": datetime.date.today().isoformat(), "job": "J0042", "by": "cursor",
        "pool": str(OUT.relative_to(HERE)), "items": items, "rejected": rejected,
    }, indent=1, ensure_ascii=False) + "\n")
    print(f"DONE ok={len(items)} rejected={len(rejected)} -> {EVIDENCE.relative_to(HERE)}")
    for r in rejected:
        print("rej", r)


if __name__ == "__main__":
    sys.exit(main())
