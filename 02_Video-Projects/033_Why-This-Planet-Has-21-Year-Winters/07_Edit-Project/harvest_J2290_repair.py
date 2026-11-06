#!/usr/bin/env python3
"""J2290 repair: fill the six misses and drop the one wrong-subject KAO hit.

The first pass trusted images-api search. One KAO query returned a 2024
demolition photo (ACD24-0161-013), not ARC-1979-AC79-0334. That file is removed.
Commons names in the pool that are not real titles are resolved to the title
the API actually returned, and recorded as HARVESTED_NOT_KEEP.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "03_Reference-Material" / "harvest_J2290_v01"
MANIFEST = HERE / "HARVEST_MANIFEST_J2290.json"
POOL_OUT = HERE / "STILLS_POOL_STATUS_v02.json"
UA = "OrbitWithBenStudio/1.0 (film 033 public-domain harvest; +https://github.com/TheLaughingGod1986/orbit-with-ben)"

# What STILLS_LOCK_v01.md called each id, kept so a mismatch stays visible.
LOCK_CAPTION = {
    "PIA01283": "Hubble NICMOS Uranus moving clouds and rings time-lapse",
    "PIA01280": "Hubble NICMOS clouds on Uranus",
    "PIA17306": "Voyager 2 departure artwork",
    "KAO_airborne_915_in_flight": "KAO C-141A N714NA in flight",
    "ARC-1973-AC73-4189-89": "KAO telescope cavity and cabin",
    "PIA01534": "Hubble ACS Uranus rings, Aug 2003",
    "PIA01364": "Voyager 2 Uranus rings in false colour",
    "PIA01356": "Voyager 2 Cordelia and Ophelia",
    "PIA01978": "Voyager 2 backlit Uranus ring dust lanes",
    "PIA01361": "Voyager 2 false-colour polar haze over Uranus",
    "PIA01278": "Hubble WFPC2 four Uranian moons and rings",
    "PIA01279": "Hubble NICMOS Uranus cloud system",
    "PIA18033": "Hubble WFC3 storms on Uranus, Nov 2014",
    "PIA02875": "Hubble seasonal roll of Uranus 1994-1998",
    "PIA01492": "Hubble WFPC2 Uranus clouds and rings",
    "PIA00369": "Hubble ACS dark cloud on Uranus",
    "PIA01975": "Hubble ACS Ariel and its shadow",
    "PIA02963": "Hubble WFPC2 Uranus equinox rings",
    "PIA19857": "Hubble WFC3 Uranus aurora",
    "PIA01354": "Voyager 2 true and false colour Uranus",
    "PIA00141": "Voyager 2 Uranus upper atmosphere limb",
    "PIA00037": "Voyager 2 Uranus with major moons",
    "PIA01486": "Voyager 2 Miranda high-resolution mosaic",
    "PIA01490": "Voyager 2 Miranda south polar mosaic",
    "PIA01488": "Voyager 2 Miranda Inverness Corona",
    "PIA01389": "Voyager 2 Miranda Elsinore Corona",
    "PIA01390": "Voyager 2 Miranda Arden Corona",
    "PIA01485": "Voyager 2 Verona Rupes on Miranda",
    "PIA00032": "Voyager 2 Verona Rupes perspective",
    "PIA19952": "Hubble WFC3 Uranus, 2015",
    "PIA00271": "Apollo 17 Blue Marble Earth",
    "weic2332a": "JWST NIRCam Uranus, 18 Dec 2023",
}


def get(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def looks_like_image(data: bytes) -> bool:
    return data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff" or data[:4] == b"GIF8"


def save_image(dest: Path, data: bytes) -> dict:
    dest.write_bytes(data)
    with Image.open(dest) as im:
        im.load()
        width, height, fmt = im.width, im.height, im.format
    return {"local_path": str(dest), "bytes": len(data), "sha256": sha256(data), "width": width, "height": height, "format": fmt}


def commons_info(title: str) -> dict:
    for attempt in range(4):
        api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "1800", "titles": title,
        })
        try:
            payload = json.loads(get(api))
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(8 * (attempt + 1))
                continue
            raise
    import urllib.error  # noqa: F401 — used above if the first import path fails
    page = next(iter(payload["query"]["pages"].values()))
    if "imageinfo" not in page:
        raise RuntimeError(f"missing commons file: {title}")
    return page


def harvest_commons(requested_id: str, title: str, note: str) -> dict:
    import urllib.error
    page = None
    for attempt in range(4):
        api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "1800", "titles": title,
        })
        try:
            page = next(iter(json.loads(get(api))["query"]["pages"].values()))
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(8 * (attempt + 1))
                continue
            raise
    info = page["imageinfo"][0]
    meta = info.get("extmetadata") or {}
    licence = (meta.get("LicenseShortName") or {}).get("value")
    mime = info.get("mime") or ""
    rec = {
        "canonical_id": requested_id,
        "resolved_title": page.get("title"),
        "resolution_note": note,
        "review_status": "HARVESTED_NOT_KEEP",
        "spend_gbp": 0,
        "licence": licence,
        "source_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        "credit": re.sub("<[^>]+>", "", (meta.get("Artist") or {}).get("value") or "Wikimedia Commons")[:240],
        "catalogue_title": page.get("title"),
    }
    if mime == "application/pdf" or title.lower().endswith(".pdf"):
        pdf = Path("/tmp") / (hashlib.sha256(title.encode()).hexdigest()[:12] + ".pdf")
        pdf.write_bytes(get(info["url"], timeout=180))
        dest = OUT / (re.sub(r"[^A-Za-z0-9._-]+", "_", requested_id) + "_page1.jpg")
        # ImageMagick needs Ghostscript, which is not installed. Quick Look rasters page 1.
        subprocess.check_call(["qlmanage", "-t", "-s", "1400", "-o", str(OUT), str(pdf)], timeout=90)
        produced = OUT / (pdf.name + ".png")
        if not produced.exists():
            raise RuntimeError("qlmanage produced no thumbnail for " + title)
        Image.open(produced).convert("RGB").save(dest, quality=90)
        produced.unlink(missing_ok=True)
        pdf.unlink(missing_ok=True)
        data = dest.read_bytes()
        rec.update(save_image(dest, data))
        rec.update(download_status="downloaded", download_url=info["url"], download_note="first page raster of the Commons PDF via Quick Look; not a separate engraved plate")
        return rec
    url = info.get("thumburl") if mime not in ("image/jpeg", "image/png") else info["url"]
    if mime not in ("image/jpeg", "image/png"):
        url = info.get("thumburl") or info["url"]
        rec["original_url"] = info["url"]
        rec["download_note"] = "saved the Commons 1800px thumbnail of a non-jpeg original"
    else:
        url = info["url"]
    data = get(url, timeout=120)
    if not looks_like_image(data):
        raise RuntimeError(f"not an image: {title}")
    ext = ".png" if data[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg"
    dest = OUT / (re.sub(r"[^A-Za-z0-9._-]+", "_", requested_id) + ext)
    rec.update(save_image(dest, data))
    rec.update(download_status="downloaded", download_url=url)
    return rec


def harvest_nasa_asset(asset_id: str) -> dict:
    meta_loc = json.loads(get(f"https://images-api.nasa.gov/metadata/{asset_id}"))
    meta = json.loads(get(meta_loc["location"]))
    urls = [item["href"] for item in json.loads(get(f"https://images-api.nasa.gov/asset/{asset_id}"))["collection"]["items"]]
    chosen = next(u for u in urls if u.lower().endswith((".jpg", ".jpeg", ".png")) and "~orig" in u.lower())
    data = get(chosen, timeout=120)
    dest = OUT / f"{asset_id}.jpg"
    rec = {
        "canonical_id": asset_id,
        "review_status": "HARVESTED_NOT_KEEP",
        "spend_gbp": 0,
        "catalogue_title": meta.get("AVAIL:Title") or meta.get("title"),
        "nasa_metadata": {"nasa_id": asset_id, "title": meta.get("AVAIL:Title") or meta.get("title"), "description": (meta.get("AVAIL:Description") or meta.get("description") or "")[:700]},
        "source_page": f"https://images.nasa.gov/details/{asset_id}",
        "credit": meta.get("AVAIL:Center") or meta.get("center") or "NASA",
        "download_status": "downloaded",
        "download_url": chosen,
    }
    # images-api metadata.json uses different shapes; fall back to the search record title if needed
    if not rec["catalogue_title"]:
        search = json.loads(get(f"https://images-api.nasa.gov/search?nasa_id={asset_id}"))
        data0 = search["collection"]["items"][0]["data"][0]
        if data0.get("nasa_id") != asset_id:
            raise RuntimeError("search hit did not match " + asset_id)
        rec["catalogue_title"] = data0.get("title")
        rec["nasa_metadata"] = {"nasa_id": asset_id, "title": data0.get("title"), "description": (data0.get("description") or "")[:700], "center": data0.get("center")}
        rec["credit"] = data0.get("center") or "NASA"
    rec.update(save_image(dest, data))
    return rec


def main() -> None:
    import urllib.error
    manifest = json.loads(MANIFEST.read_text())
    assets = [r for r in manifest["assets"] if r["canonical_id"] != "KAO_airborne_915_in_flight"]
    wrong = OUT / "KAO_airborne_915_in_flight.jpg"
    if wrong.exists():
        wrong.unlink()
    # also any other extension
    for p in OUT.glob("KAO_airborne_915_in_flight.*"):
        p.unlink()

    replacements = []
    commons_jobs = [
        ("File:Herschel_40_foot_telescope.jpg", "File:Herschel 40 foot.jpg",
         "Pool filename is not a Commons title. Resolved to File:Herschel 40 foot.jpg via Commons search."),
        ("File:Caroline_Herschel-1829.jpg", "File:Herschel Caroline 1829.jpg",
         "Pool filename is not a Commons title. Resolved to File:Herschel Caroline 1829.jpg."),
        ("File:Martin_Heinrich_Klaproth_portrait.jpg", "File:Martin Heinrich Klaproth. Mezzotint. Wellcome V0003234.jpg",
         "Pool filename is not a Commons title. Resolved to the Wellcome mezzotint."),
        ("File:Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg", "File:Herschel-Account of a Comet.pdf",
         "No bitmap of this paper was on Commons. First page of File:Herschel-Account of a Comet.pdf."),
        ("File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg",
         "File:On the Diameter and Magnitude of the Georgium Sidus; With a Description of the Dark and Lucid Disk and Periphery Micrometers. By William Herschel, Esq. F. R. S. (IA paper-doi-10 1098 rstl 1783 0002).pdf",
         "No bitmap of the Banks letter was on Commons. First page of the 1783 Phil. Trans. Georgium Sidus paper. This is not a verified letter-to-Banks scan."),
        ("KAO_airborne_915_in_flight", "File:NASA C-141A KAO.jpg",
         "NASA id ARC-1979-AC79-0334 is not in images.nasa.gov. The first-pass hit ACD24-0161-013 was a demolition photo and was deleted. This Commons file is the C-141A KAO."),
    ]
    for requested, title, note in commons_jobs:
        print("commons", requested, flush=True)
        time.sleep(2)
        try:
            rec = harvest_commons(requested, title, note)
        except Exception as exc:
            rec = {"canonical_id": requested, "download_status": "ERROR", "review_status": "HARVESTED_NOT_KEEP", "error": str(exc), "resolution_note": note, "spend_gbp": 0}
        replacements.append(rec)
        print("  ", rec["download_status"], rec.get("width"), rec.get("error", ""), flush=True)

    print("nasa PIA01389", flush=True)
    replacements.append(harvest_nasa_asset("PIA01389"))
    print("  ", replacements[-1]["catalogue_title"], replacements[-1]["width"], flush=True)

    by_id = {r["canonical_id"]: r for r in assets}
    for rec in replacements:
        by_id[rec["canonical_id"]] = rec
    order = manifest["requested"]
    merged = [by_id[i] for i in order if i in by_id]
    # identity notes: catalogue title versus the lock's caption
    notes = []
    for rec in merged:
        cap = LOCK_CAPTION.get(rec["canonical_id"])
        title = rec.get("catalogue_title") or ""
        if cap:
            rec["lock_caption"] = cap
            rec["identity_note"] = "Catalogue title is the source of identity. The lock caption is not confirmed by this file."
        if cap and title and cap.lower().split(",")[0][:18] not in title.lower() and title.lower()[:18] not in cap.lower():
            notes.append({"canonical_id": rec["canonical_id"], "catalogue_title": title, "lock_caption": cap})
    downloaded = [r for r in merged if r.get("download_status") == "downloaded"]
    failed = [r for r in merged if r.get("download_status") != "downloaded"]
    manifest["assets"] = merged
    manifest["downloaded"] = len(downloaded)
    manifest["failed"] = len(failed)
    manifest["repair"] = "Dropped ACD24-0161-013 (KAO demolition, wrong subject). Filled Commons misses and PIA01389 from the asset endpoint."
    manifest["identity_mismatches_vs_lock_caption"] = notes
    manifest["keep_assigned"] = 0
    (OUT / "SHA256SUMS.txt").write_text("".join(f"{r['sha256']}  {Path(r['local_path']).name}\n" for r in downloaded))
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    pool = json.loads(POOL_OUT.read_text()) if POOL_OUT.exists() else {}
    pool["harvested_assets"] = [
        {k: r.get(k) for k in ("canonical_id", "catalogue_title", "resolved_title", "local_path", "sha256", "bytes", "width", "height", "download_url", "source_page", "credit", "licence", "lock_caption", "resolution_note")}
        | {"review_status": "HARVESTED_NOT_KEEP"}
        for r in downloaded
    ]
    pool["harvest_failed"] = [{"canonical_id": r["canonical_id"], "error": r.get("error")} for r in failed]
    pool["identity_mismatches_vs_lock_caption"] = notes
    pool["summary"] = {**pool.get("summary", {}), "harvest_downloaded": len(downloaded), "harvest_failed": len(failed), "keep_assigned": 0}
    POOL_OUT.write_text(json.dumps(pool, indent=2) + "\n")
    print(f"REPAIRED downloaded={len(downloaded)} failed={len(failed)} mismatches={len(notes)}", flush=True)


if __name__ == "__main__":
    main()
