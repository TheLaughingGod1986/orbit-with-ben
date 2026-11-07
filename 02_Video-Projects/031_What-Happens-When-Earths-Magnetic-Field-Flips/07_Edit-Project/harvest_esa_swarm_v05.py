#!/usr/bin/env python3
"""J2141: three ESA/DTU Swarm candidates. £0. None admitted.

The shot list names CC BY-SA 3.0 IGO. The live ESA pages do not.
June 2014 is kept only as a Commons copy with that conflict on the record.
The constellation still is not downloaded: ESA asks for extra permission.
SAA 2020 is a CC BY-SA 4.0 paper figure and fails the upscale cap.
Existing outputs are refused. Reproduce only into an empty directory.
"""
import argparse
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE = Path(__file__).resolve().parent
POOL = HERE / "HARVEST_POOL_v01.json"
UA = "OrbitWithBenStudio/1.0 (J2141 provenance; educational)"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get(url):
    import time
    import urllib.error
    delay = 5
    last = None
    for _ in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return response.read(), response.geturl()
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code != 429:
                raise
            time.sleep(delay)
            delay *= 2
    raise last


def need(path, url):
    if path.exists():
        return path.read_bytes()
    raw, _ = get(url)
    path.write_bytes(raw)
    return raw


def luma(path):
    with Image.open(path) as im:
        gray = im.convert("L")
        stat = ImageStat.Stat(gray)
        hist = gray.histogram()
        size = im.size
    total = sum(hist) or 1
    acc = 0
    p95 = 255
    need_count = 0.95 * total
    for index, count in enumerate(hist):
        acc += count
        if acc >= need_count:
            p95 = index
            break
    return size, round(stat.mean[0], 1), p95, round(sum(hist[:16]) / total, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--media-root", type=Path, required=True)
    ap.add_argument("--pool", type=Path, default=POOL)
    args = ap.parse_args()
    root = args.media_root
    root.mkdir(parents=True, exist_ok=True)
    pool = json.loads(args.pool.read_text())
    have = {asset["asset_id"] for asset in pool["assets"]}
    for ident in ("esa_june_2014_magnetic_field", "esa_swarm_constellation_over_earth", "commons_saa_2020"):
        if ident in have:
            raise SystemExit(f"already in pool: {ident}")

    esa_june = root / "esa_june_2014.html"
    esa_swarm = root / "esa_swarm_constellation.html"
    esa_changes = root / "esa_field_changes.html"
    need(esa_june, "https://www.esa.int/ESA_Multimedia/Images/2014/06/June_2014_magnetic_field")
    need(esa_swarm, "https://www.esa.int/ESA_Multimedia/Images/2013/10/Swarm_constellation_over_Earth")
    need(esa_changes, "https://www.esa.int/ESA_Multimedia/Images/2014/06/Magnetic_field_changes")
    june_html = esa_june.read_text(errors="replace")
    swarm_html = esa_swarm.read_text(errors="replace")
    changes_html = esa_changes.read_text(errors="replace")
    if "ESA/DTU Space" not in june_html or "No ESA licences available" not in june_html:
        raise SystemExit("June 2014 ESA page no longer matches the recorded licence line")
    if "ESA/AOES Medialab" not in swarm_html or "Additional permission may be required" not in swarm_html:
        raise SystemExit("Swarm constellation ESA page no longer matches the recorded licence line")
    if "No ESA licences available" not in changes_html:
        raise SystemExit("Magnetic field changes page no longer says no licence is available")

    titles = "File:June 2014 magnetic field.jpg|File:SAA 2020.png"
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "titles": titles,
    })
    evidence = root / "commons_api_v05.json"
    raw = need(evidence, api)
    pages = {page["title"]: page for page in json.loads(raw)["query"]["pages"].values()}

    def commons_file(title, dest_name, rights_name):
        page = pages[title]
        info = page["imageinfo"][0]
        rights = root / rights_name
        image = root / dest_name
        page_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
        need(rights, page_url)
        if not image.exists():
            body, _ = get(info["url"])
            image.write_bytes(body)
        with Image.open(image) as im:
            im.verify()
        if Image.open(image).size != (info["width"], info["height"]):
            raise SystemExit(f"size disagrees with Commons: {title}")
        return info, image, rights, page_url

    june_info, june_path, june_rights, june_page = commons_file(
        "File:June 2014 magnetic field.jpg", "june2014.jpg", "june2014_rights.html")
    saa_info, saa_path, saa_rights, saa_page = commons_file(
        "File:SAA 2020.png", "saa2020.png", "saa2020_rights.html")
    june_lic = (june_info["extmetadata"].get("LicenseShortName") or {}).get("value")
    saa_lic = (saa_info["extmetadata"].get("LicenseShortName") or {}).get("value")
    if june_lic != "Public domain" or saa_lic != "CC BY-SA 4.0":
        raise SystemExit(f"Commons licence changed: june={june_lic} saa={saa_lic}")
    if "Public domain" not in june_rights.read_text(errors="replace"):
        raise SystemExit("June 2014 Commons page lost its public-domain assertion")
    if "creativecommons.org/licenses/by-sa/4.0" not in saa_rights.read_text(errors="replace"):
        raise SystemExit("SAA 2020 Commons page lost the CC BY-SA 4.0 link")

    june_size, june_mean, june_p95, june_dark = luma(june_path)
    saa_size, saa_mean, saa_p95, saa_dark = luma(saa_path)
    june_scale = round(1920 / june_size[0], 3)
    saa_scale = round(1920 / saa_size[0], 3)

    june = {
        "asset_id": "esa_june_2014_magnetic_field",
        "title": "June 2014 magnetic field.jpg",
        "agency": "ESA/DTU Space",
        "description": (
            "Snapshot of the main magnetic field at Earth's surface as of June 2014, "
            "from Swarm data. Red is stronger. Blue is weaker."
        ),
        "source_page": "https://www.esa.int/ESA_Multimedia/Images/2014/06/June_2014_magnetic_field",
        "commons_page": june_page,
        "source_api": api,
        "source_url": june_info["url"],
        "credit": "ESA/DTU Space",
        "local_path": str(june_path),
        "sha256": sha(june_path),
        "bytes": june_path.stat().st_size,
        "width": june_size[0],
        "height": june_size[1],
        "mean_luma": june_mean,
        "gray_p95": june_p95,
        "fraction_under_luma_16": june_dark,
        "full_frame_scale_to_1920": june_scale,
        "upscale_cap": 2.35,
        "rows": [23, 24],
        "assigned_uses": 0,
        "max_uses": 2,
        "native_motion": False,
        "download_status": "downloaded_commons_copy_only",
        "review_status": "candidate_still_not_admitted",
        "review_note": (
            "Visual check: oval world map, blue dent over South America and the South Atlantic, "
            "red at the poles and Australia, coastlines, dotted grid, and a colour bar labelled "
            "20000 to 60000 nanotesla. Black surround is 0.441 of the frame, so a full-frame hold "
            "would fail near-black. It is a labelled sourced map, which picture_qa still forbids, "
            "and it is a still. Shot-list rows 23 and 24 would share it, but assigned uses stay 0. "
            "Commons asserts public domain via the old ESA template. The live ESA page credits "
            "ESA/DTU Space and says 'No ESA licences available'. It does not say CC BY-SA 3.0 IGO. "
            "Not admitted."
        ),
        "licence": "unresolved",
        "licence_status": "conflict_commons_pd_template_vs_esa_no_licence_available",
        "licence_evidence_path": str(esa_june),
        "licence_evidence_sha256": sha(esa_june),
        "commons_rights_path": str(june_rights),
        "commons_rights_sha256": sha(june_rights),
        "source_evidence_path": str(evidence),
        "source_evidence_sha256": sha(evidence),
        "generation_authorized": False,
        "rights_review": (
            "Do not treat the Commons public-domain box as clearance. "
            "The publisher page currently offers no ESA licence."
        ),
    }
    swarm = {
        "asset_id": "esa_swarm_constellation_over_earth",
        "title": "Swarm constellation over Earth",
        "agency": "ESA",
        "description": (
            "ESA page for an artist's view of the three Swarm satellites over Earth. "
            "Image bytes were not downloaded."
        ),
        "source_page": "https://www.esa.int/ESA_Multimedia/Images/2013/10/Swarm_constellation_over_Earth",
        "credit": "ESA/AOES Medialab",
        "local_path": None,
        "rows": [24],
        "assigned_uses": 0,
        "max_uses": 2,
        "native_motion": False,
        "download_status": "not_downloaded_additional_permission_required",
        "review_status": "rejected_rights_not_admitted",
        "review_note": (
            "Row 24 wants a moving three-satellite constellation. This ESA page is a still, "
            "credited to ESA/AOES Medialab, under 'ESA Standard Licence and Additional permission "
            "may be required'. That is not CC BY-SA 3.0 IGO. Third-party Medialab credit means "
            "the extra permission is real. Image not downloaded. Not admitted."
        ),
        "licence": "ESA Standard Licence; additional permission may be required",
        "licence_status": "not_cleared_additional_permission_required",
        "licence_evidence_path": str(esa_swarm),
        "licence_evidence_sha256": sha(esa_swarm),
        "generation_authorized": False,
        "rights_review": "No image bytes taken. Do not fetch the media.esa.int file without permission.",
    }
    saa = {
        "asset_id": "commons_saa_2020",
        "title": "SAA 2020.png",
        "agency": "paper figure from Swarm models",
        "description": (
            "Field strength in 2020 from the CHAOS-7 paper, drawn from Swarm measurements. "
            "The South Atlantic Anomaly is the dark oval west of Africa's coast, over South America."
        ),
        "source_page": saa_page,
        "source_api": api,
        "source_url": saa_info["url"],
        "paper": "https://earth-planets-space.springeropen.com/articles/10.1186/s40623-020-01252-9",
        "credit": "Finlay, Kloss, Olsen, Hammer, Tøffner-Clausen, Grayver and Kuvshinov, 2020",
        "local_path": str(saa_path),
        "sha256": sha(saa_path),
        "bytes": saa_path.stat().st_size,
        "width": saa_size[0],
        "height": saa_size[1],
        "mean_luma": saa_mean,
        "gray_p95": saa_p95,
        "fraction_under_luma_16": saa_dark,
        "full_frame_scale_to_1920": saa_scale,
        "upscale_cap": 2.35,
        "rows": [23],
        "assigned_uses": 0,
        "max_uses": 2,
        "native_motion": False,
        "download_status": "downloaded",
        "review_status": "candidate_still_not_admitted",
        "review_note": (
            "Visual check: white-background oval map labelled 2020, colour bar 22000 to 62000 nT, "
            "and contour lines around a dark-blue minimum over South America. It is a sourced "
            "labelled figure, so picture_qa still forbids it. 700×430. Full-frame scale to 1920 "
            f"is {saa_scale}×, over the 2.35× cap. Credit is the paper's authors, not the "
            "on-screen line 'ESA/DTU Space'. Licence is CC BY-SA 4.0, not CC BY-SA 3.0 IGO. "
            "A still. Not admitted."
        ),
        "licence": "CC BY-SA 4.0",
        "licence_status": "Commons_per_file_CC_BY_SA_4_0_verified",
        "licence_url": "https://creativecommons.org/licenses/by-sa/4.0",
        "licence_evidence_path": str(saa_rights),
        "licence_evidence_sha256": sha(saa_rights),
        "source_evidence_path": str(evidence),
        "source_evidence_sha256": sha(evidence),
        "generation_authorized": False,
        "rights_review": (
            "CC BY-SA 4.0 allows use with attribution and share-alike. "
            "That does not clear the upscale cap or the sourced-map gate."
        ),
    }
    pool["assets"].extend([june, swarm, saa])
    sheet = Image.new("RGB", (1600, 980), (18, 32, 52))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
    small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    for index, (record, path) in enumerate(((june, june_path), (saa, saa_path))):
        im = Image.open(path).convert("RGB")
        im.thumbnail((740, 620))
        x = 40 + index * 780
        sheet.paste(im, (x, 40))
        draw.multiline_text(
            (x, 690),
            f"{record['asset_id']}\nnot admitted",
            font=font, fill=(244, 239, 230), spacing=6,
        )
    draw.multiline_text(
        (40, 860),
        "Third candidate, Swarm constellation over Earth: not downloaded.\n"
        "ESA Standard Licence and additional permission. Credit ESA/AOES Medialab.",
        font=small, fill=(244, 239, 230), spacing=6,
    )
    sheet_path = root / "contact_sheet_esa_v05.jpg"
    if sheet_path.exists():
        raise SystemExit(f"refusing existing file: {sheet_path}")
    sheet.save(sheet_path, quality=90)
    pool["status"] = "partial_harvest_not_KEEP"
    pool["spend_gbp"] = 0
    pool["esa_v05_contact_sheet"] = str(sheet_path)
    pool["esa_v05_contact_sheet_sha256"] = sha(sheet_path)
    pool["esa_v05_investigation"] = {
        "date": "2026-11-07",
        "candidates_examined": 3,
        "status": "three_candidates_not_admitted",
        "examined": [june["asset_id"], swarm["asset_id"], saa["asset_id"]],
        "licence_context_only": {
            "page": "https://www.esa.int/ESA_Multimedia/Images/2014/06/Magnetic_field_changes",
            "evidence": str(esa_changes),
            "note": "Licence line only. Same 'No ESA licences available' and credit ESA/DTU Space. Image not downloaded and not counted as a picture exam.",
        },
        "shot_list_licence_claim": "CC BY-SA 3.0 IGO",
        "found_instead": "ESA pages say no licence, or ESA Standard Licence plus extra permission. Neither downloaded file carries CC BY-SA 3.0 IGO.",
        "next_action": "Chief reconciles the licence conflict and the sourced-map gate before any of these enters a cut. Do not re-download these three. A moving Swarm clip still needs its own bounded search.",
    }
    args.pool.write_text(json.dumps(pool, indent=2) + "\n")
    check = {
        "job": "J2141",
        "spend_gbp": 0,
        "status": "esa_candidates_not_admitted",
        "contact_sheet": str(sheet_path),
        "contact_sheet_sha256": sha(sheet_path),
        "assets": [
            {
                "asset_id": record["asset_id"],
                "download_status": record["download_status"],
                "sha256": record.get("sha256"),
                "width": record.get("width"),
                "height": record.get("height"),
                "mean_luma": record.get("mean_luma"),
                "gray_p95": record.get("gray_p95"),
                "fraction_under_luma_16": record.get("fraction_under_luma_16"),
                "full_frame_scale_to_1920": record.get("full_frame_scale_to_1920"),
                "assigned_uses": 0,
                "licence_status": record["licence_status"],
            }
            for record in (june, swarm, saa)
        ],
    }
    check_path = HERE / "HARVEST_ESA_TECHNICAL_CHECK_v05.json"
    if check_path.exists():
        raise SystemExit(f"refusing existing file: {check_path}")
    check_path.write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
