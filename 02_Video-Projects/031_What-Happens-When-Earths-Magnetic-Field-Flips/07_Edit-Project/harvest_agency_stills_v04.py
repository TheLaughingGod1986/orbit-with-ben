#!/usr/bin/env python3
"""J2141: three agency still candidates via Commons. £0. Not admitted.

USGS, NOAA and USFWS hosts blocked this machine (empty 202, 405, 403).
Each file below is the Commons original whose own page credits that agency
and asserts public domain. Existing files are refused. Candidates stay
outside the film until Chief accepts a row. A still is not the moving clip.
"""
import argparse
import hashlib
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE = Path(__file__).resolve().parent
POOL = HERE / "HARVEST_POOL_v01.json"
UA = "OrbitWithBenStudio/1.0 (J2141 provenance; educational)"

# Three files examined in depth. Search hits were not downloaded.
ITEMS = [
    {
        "asset_id": "commons_usgs_kilauea_978",
        "title": "USGS Kīlauea MultimediaFile-978.jpg",
        "rows": [6],
        "agency": "USGS",
        "must_contain": ("kilauea", "kīlauea"),
        "credit_expect": "Geological Survey",
        "review_note": (
            "USGS HVO still, 12 Nov 2014, Puʻu ʻŌʻō, Commons file citing "
            "hvo.wr.usgs.gov multimediaFile-978. Visual check: cooled black lava around a damaged house "
            "and a standing garage, with a burned-in label 'Transfer station'. No glowing flow and no clay "
            "being baked. Text on the plate. Not a row 6 match. usgs.gov returned an empty 202 from this machine."
        ),
    },
    {
        "asset_id": "commons_noaa_humpback_anim1107",
        "title": "Humpback Megaptera novaeangliae.jpg",
        "rows": [49],
        "agency": "NOAA",
        "must_contain": ("humpback", "megaptera"),
        "credit_expect": "NOAA",
        "review_note": (
            "NOAA Photo Library anim1107. Visual check: one raised humpback flipper among sea ice, "
            "snow mountains behind. Spyhopping, not an underwater swim, and not a sea turtle. "
            "1154×602, 1.664× to 1920 wide, short of 16:9. Credit line stays 'Courtesy of Dr. Brandon Southall, NMFS/OPR'. "
            "noaa.gov returned 405 from this machine."
        ),
    },
    {
        "asset_id": "commons_usfws_tundra_swans",
        "title": "Migrating tundra swans (6531261593).jpg",
        "rows": [49],
        "agency": "USFWS",
        "must_contain": ("migrat", "swan"),
        "credit_expect": "Fish and Wildlife",
        "review_note": (
            "USFWS photograph, Erin Clark, Red Rock Lakes. Visual check: white swans in flight in a loose V "
            "against blue sky. Mean luma 141. A still, not flight footage. Candidate for the row 49 bird beat. "
            "fws.gov returned 403 from this machine."
        ),
    },
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get(url):
    import time
    delay = 5
    last = None
    for _ in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                return response.read(), response.geturl()
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code != 429:
                raise
            time.sleep(delay)
            delay *= 2
    raise last


def plain(value):
    text = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", text).strip()


def meta_text(meta):
    parts = []
    for key in ("ObjectName", "ImageDescription", "Credit", "Artist", "LicenseShortName"):
        parts.append(plain((meta.get(key) or {}).get("value")))
    return " ".join(parts)


def luma(path):
    with Image.open(path) as im:
        gray = im.convert("L")
        stat = ImageStat.Stat(gray)
        hist = gray.histogram()
    total = sum(hist) or 1
    need = 0.95 * total
    acc = 0
    p95 = 255
    for index, count in enumerate(hist):
        acc += count
        if acc >= need:
            p95 = index
            break
    return round(stat.mean[0], 1), p95, round(sum(hist[:16]) / total, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--media-root", type=Path, required=True)
    ap.add_argument("--pool", type=Path, default=POOL)
    args = ap.parse_args()
    root = args.media_root
    root.mkdir(parents=True, exist_ok=True)
    pool = json.loads(args.pool.read_text())
    have = {asset["asset_id"] for asset in pool["assets"]}
    titles = "|".join("File:" + item["title"] for item in ITEMS)
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "titles": titles,
    })
    evidence = root / "commons_api_v04.json"
    if evidence.exists():
        raw = evidence.read_bytes()
    else:
        raw, _ = get(api)
        evidence.write_bytes(raw)
    pages = json.loads(raw)["query"]["pages"]
    by_title = {page["title"]: page for page in pages.values()}
    added = []
    for item in ITEMS:
        ident = item["asset_id"]
        if ident in have:
            raise SystemExit(f"already in pool: {ident}")
        page = by_title.get("File:" + item["title"])
        if not page or "imageinfo" not in page:
            raise SystemExit(f"missing Commons record: {item['title']}")
        info = page["imageinfo"][0]
        meta = info["extmetadata"]
        licence = (meta.get("LicenseShortName") or {}).get("value")
        copyrighted = ((meta.get("Copyrighted") or {}).get("value") or "").lower()
        if licence != "Public domain" or copyrighted != "false":
            raise SystemExit(f"rights assertion changed: {ident}: {licence} copyrighted={copyrighted}")
        blob = (item["title"] + " " + meta_text(meta)).lower()
        if not any(token in blob for token in item["must_contain"]):
            raise SystemExit(f"subject text missing for {ident}: {blob[:400]}")
        if item["credit_expect"].lower() not in blob:
            raise SystemExit(f"agency credit missing for {ident}: {blob[:400]}")
        page_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote("File:" + item["title"])
        rights = root / f"{ident}_rights.html"
        image_path = root / f"{ident}.jpg"
        if rights.exists():
            rights_bytes = rights.read_bytes()
        else:
            rights_bytes, _ = get(page_url)
            rights.write_bytes(rights_bytes)
        if image_path.exists():
            final_url = info["url"]
        else:
            image_bytes, final_url = get(info["url"])
            image_path.write_bytes(image_bytes)
        with Image.open(image_path) as im:
            im.verify()
        with Image.open(image_path) as im:
            width, height = im.size
        if (width, height) != (info["width"], info["height"]):
            raise SystemExit(f"size disagrees with Commons: {ident}")
        mean_luma, p95, dark = luma(image_path)
        scale = round(1920 / width, 3)
        note = item["review_note"]
        if scale > 2.35:
            note += f" Full-frame scale to 1920 is {scale}×, over the 2.35× cap."
        record = {
            "asset_id": ident,
            "title": item["title"],
            "agency": item["agency"],
            "description": plain((meta.get("ImageDescription") or {}).get("value")),
            "object_name": plain((meta.get("ObjectName") or {}).get("value")),
            "source_page": page_url,
            "source_api": api,
            "source_url": info["url"],
            "download_url": final_url,
            "credit": plain((meta.get("Artist") or {}).get("value")) or plain((meta.get("Credit") or {}).get("value")),
            "commons_credit": plain((meta.get("Credit") or {}).get("value")),
            "local_path": str(image_path),
            "sha256": sha(image_path),
            "bytes": image_path.stat().st_size,
            "width": width,
            "height": height,
            "mean_luma": mean_luma,
            "gray_p95": p95,
            "fraction_under_luma_16": dark,
            "full_frame_scale_to_1920": scale,
            "upscale_cap": 2.35,
            "rows": item["rows"],
            "assigned_uses": 0,
            "max_uses": 2,
            "native_motion": False,
            "download_status": "downloaded",
            "review_status": "candidate_still_not_admitted",
            "review_note": note,
            "licence": "Public domain",
            "licence_status": "Commons_per_file_public_domain_assertion_verified",
            "licence_evidence_path": str(rights),
            "licence_evidence_sha256": sha(rights),
            "source_evidence_path": str(evidence),
            "source_evidence_sha256": sha(evidence),
            "generation_authorized": False,
            "rights_review": (
                "Commons file page asserts public domain and names the agency. "
                "The agency host was not the byte source. Not cleared for the cut."
            ),
        }
        pool["assets"].append(record)
        added.append(record)
        print(ident, width, height, "luma", mean_luma, flush=True)

    sheet = Image.new("RGB", (1800, 760), (18, 32, 52))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
    for index, record in enumerate(added):
        im = Image.open(record["local_path"]).convert("RGB")
        im.thumbnail((560, 560))
        x = 30 + index * 590
        sheet.paste(im, (x, 30))
        label = f"{record['asset_id']}\nrow {record['rows'][0]} candidate"
        draw.multiline_text((x, 610), label, font=font, fill=(244, 239, 230), spacing=6)
    sheet_path = root / "contact_sheet_stills_v04.jpg"
    if sheet_path.exists():
        raise SystemExit(f"refusing existing file: {sheet_path}")
    sheet.save(sheet_path, quality=90)
    pool["status"] = "partial_harvest_not_KEEP"
    pool["spend_gbp"] = 0
    pool["stills_v04_contact_sheet"] = str(sheet_path)
    pool["stills_v04_contact_sheet_sha256"] = sha(sheet_path)
    pool["stills_v04_host_blocks"] = {
        "usgs.gov": "empty HTTP 202",
        "noaa.gov": "HTTP 405",
        "fws.gov": "HTTP 403",
    }
    args.pool.write_text(json.dumps(pool, indent=2) + "\n")
    check = {
        "job": "J2141",
        "spend_gbp": 0,
        "status": "candidate_stills_not_admitted",
        "contact_sheet": str(sheet_path),
        "contact_sheet_sha256": sha(sheet_path),
        "assets": [
            {
                "asset_id": record["asset_id"],
                "sha256": record["sha256"],
                "width": record["width"],
                "height": record["height"],
                "bytes": record["bytes"],
                "mean_luma": record["mean_luma"],
                "gray_p95": record["gray_p95"],
                "fraction_under_luma_16": record["fraction_under_luma_16"],
                "full_frame_scale_to_1920": record["full_frame_scale_to_1920"],
                "rows": record["rows"],
                "assigned_uses": 0,
            }
            for record in added
        ],
    }
    check_path = HERE / "HARVEST_STILLS_TECHNICAL_CHECK_v04.json"
    if check_path.exists():
        raise SystemExit(f"refusing existing file: {check_path}")
    check_path.write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
