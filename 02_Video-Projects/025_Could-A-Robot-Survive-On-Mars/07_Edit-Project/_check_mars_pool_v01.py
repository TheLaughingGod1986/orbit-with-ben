#!/usr/bin/env python3
"""J0051 step 1: check every nasa_pool_v01 entry against its published NASA page.

Writes ../_evidence/mars_robot_pool_check_v01.json (row, source URL, published title,
licence, credit, flags). Read-only on the pool; no downloads beyond API metadata.
"""
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
POOL = HERE / "nasa_pool_v01.json"
OUT = FILM / "_evidence" / "mars_robot_pool_check_v01.json"

NASA_OK = re.compile(r"NASA|JPL|Caltech|Cornell|Arizona|UArizona|ASU|Texas A&M|MSSS|Malin|LANL|"
                     r"Southwest Research|SwRI|USGS|KSC|Lockheed|Kennedy|Goddard|Ames|Glenn|DOE|"
                     r"Idaho National|CNES|IRAP|IPGP|Imperial|DLR|Honeybee|AeroVironment|Univ", re.I)
NON_PD = re.compile(r"©|copyright|all rights reserved|ESA/|Getty|Reuters|AP Photo|United Launch Alliance photo", re.I)


def api(nasa_id: str):
    url = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"nasa_id": nasa_id})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                items = json.load(r)["collection"]["items"]
            return items[0] if items else None
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def canonical_size(item):
    for link in item.get("links", []) if item else []:
        if link.get("rel") == "canonical":
            return link.get("width"), link.get("height")
    return None, None


def local_size(path: Path):
    if not path.exists():
        return None, None
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height", "-of", "csv=p=0", str(path)],
                             capture_output=True, text=True, timeout=60).stdout.strip().split("\n")[0]
        w, h = out.split(",")[:2]
        return int(w), int(h)
    except Exception:
        return None, None


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


REPORT = HERE / "nasa_pool_v01" / "_fetch_report.json"

# Subject review against SHOT_LIST_v02 rows (Cursor, 8 Oct 2026). "drop" = not what its row says, or rights unclear.
REVIEW = {
    "PIA26147": ("drop", "Photographer credit MDSCC/INTA (Francisco Moreno), not NASA staff: rights not clearly public domain. Four other DSN plates cover row 11."),
    "PIA10664": ("drop", "Artist concept of Phoenix under parachute, not the HiRISE photo NASA_POOL_v01.md says. Row 16 asks for real landing/winter/HiRISE plates."),
    "PIA06263": ("drop", "Rock layers inside Endurance Crater: geology, not dust. Not what rows 10/18-20 or Mon S3 say."),
    "PIA15689": ("hold", "False-colour panorama. Usable for row 5/28 texture only if graded and not presented as true colour; never frame 0 (PIA22909 true colour is the open)."),
    "PIA14839": ("note", "Artist concept (sky crane). Row 26 allows EDL art; keep it as art, not as a photo."),
    "PIA12337": ("note", "Software reconstruction (screen shot), not a photo. Fine as a row 14 teaching cutaway."),
    "PIA13730": ("note", "Traverse map graphic. Fine for row 15 montage."),
    "PIA22549": ("note", "HiRISE orbital crop of Perseverance Valley (not a globe). Row 21 is ground-level/sky-from-surface first; use only after."),
    "PIA12205": ("note", "HiRISE orbital crop of Troy (not a globe). Credit NASA/JPL-Caltech/UArizona."),
    "PIA13158": ("note", "HiRISE 2008 vs 2010 pair. Credit NASA/JPL-Caltech/UArizona on screen or in the description."),
    "PIA24270": ("note", "HiRISE of descent. Credit NASA/JPL-Caltech/UArizona."),
    "PIA26302": ("note", "2024 solar-storm Navcam frames: radiation context for row 8, not the RAD dose itself."),
    "PIA22330": ("note", "Two-panel before/after comparison image: crop to one panel for row 24."),
}


def main():
    pool = json.loads(POOL.read_text())
    report = {(r["section"], r["nasa_id"]): r for r in json.loads(REPORT.read_text())}
    rows = []
    for e in pool:
        nid = e["nasa_id"]
        e = {**report.get((e["section"], nid), {}), **e}
        item = api(nid)
        data = (item or {}).get("data", [{}])[0]
        pub_title = data.get("title")
        creator = data.get("secondary_creator") or data.get("photographer") or ""
        desc = data.get("description") or ""
        cw, ch = canonical_size(item)
        local = Path(e["local"]) if e.get("local") else HERE / "nasa_pool_v01" / e["section"] / "__missing__"
        lw, lh = local_size(local)
        is_pia = nid.startswith("PIA")
        page = (f"https://photojournal.jpl.nasa.gov/catalog/{nid}" if is_pia
                else f"https://images.nasa.gov/details/{urllib.parse.quote(nid)}")
        flags = []
        if not item:
            flags.append("no NASA images API record")
        if pub_title and norm(pub_title) != norm(e.get("title")):
            flags.append(f"title differs from harvest ({e.get('title')!r})")
        if NON_PD.search(desc + " " + creator):
            flags.append("possible non-NASA rights text")
        if creator and not NASA_OK.search(creator):
            flags.append(f"creator not NASA family: {creator}")
        if not local.exists():
            flags.append("local file missing")
        elif cw and lw and e.get("orig", "").endswith(("~orig.jpg", "~orig.png", "~orig.tif")) \
                and (abs(cw - lw) > 2 or abs(ch - lh) > 2):
            flags.append(f"local {lw}x{lh} != published {cw}x{ch} (wrong file?)")
        verdict, why = REVIEW.get(nid, ("keep", ""))
        if flags and verdict == "keep":
            verdict = "check"
        rows.append({
            "verdict": verdict,
            "review": why,
            "section": e["section"],
            "rows": e.get("rows"),
            "nasa_id": nid,
            "source_url": page,
            "asset_url": e.get("orig"),
            "published_title": pub_title,
            "harvest_title": e.get("title"),
            "description_head": desc[:300],
            "credit": creator or e.get("credit"),
            "center": data.get("center"),
            "date_created": data.get("date_created"),
            "licence": "Public domain (NASA media usage guidelines: not copyrighted; credit given)",
            "local": str(local.relative_to(HERE)) if local.is_relative_to(HERE) else str(local),
            "local_px": [lw, lh],
            "published_px": [cw, ch],
            "flags": flags,
        })
        print(f"{nid:40.40} {'FLAG' if flags else 'ok  '} {'; '.join(flags)[:120]}", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"checked": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                               "pool": str(POOL.relative_to(FILM)),
                               "count": len(rows),
                               "flagged": sum(1 for r in rows if r["flags"]),
                               "verdicts": {v: sum(1 for r in rows if r["verdict"] == v)
                                            for v in ("keep", "note", "hold", "check", "drop")},
                               "dropped": [r["nasa_id"] for r in rows if r["verdict"] == "drop"],
                               "entries": rows}, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({len(rows)} entries)")


if __name__ == "__main__":
    sys.exit(main())
