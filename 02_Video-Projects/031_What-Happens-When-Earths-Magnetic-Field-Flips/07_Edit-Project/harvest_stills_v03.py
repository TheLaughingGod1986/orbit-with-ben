#!/usr/bin/env python3
"""J2141: three NASA still candidates. £0. Not admitted, not KEEP.

Downloads original NASA Images files plus the API JSON that names them.
Existing files are refused. Candidates stay outside the film until Chief
accepts a row. A still is not a substitute for a shot-list time-lapse.
"""
import argparse, hashlib, json, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE = Path(__file__).resolve().parent
POOL = HERE / "HARVEST_POOL_v01.json"
POLICY = "https://www.nasa.gov/nasa-brand-center/images-and-media/"
# Examined in depth. A fourth metadata-only reject (iss058e005282) is
# recorded in the handoff: the frame is over Ukraine, not an Arctic limb.
ITEMS = [
    {
        "asset_id": "PIA22661",
        "rows": [14],
        "title_expect": "Twisting Prominences",
        "review_note": (
            "SDO extreme-ultraviolet still of two solar prominences, 30-31 July 2018. "
            "Candidate for row 14. It is one frame, not the moving prominence clip, "
            "and the colour is the instrument wavelength, not visible light."
        ),
    },
    {
        "asset_id": "GSFC_20171208_Archive_e000678",
        "rows": [3],
        "title_expect": "NASA Captures 'EPIC' Earth Image",
        "review_note": (
            "First full sunlit Earth from DSCOVR EPIC, released July 2015, one million miles out. "
            "Candidate frame for row 3. It is not the rotating EPIC sequence, and it does not "
            "replace the VIIRS Blue Marble already in this pool."
        ),
    },
    {
        "asset_id": "sts061-57-021",
        "rows": [27],
        "title_expect": "Onboard view from STS-61 of the Hubble Space Telescope and moon together",
        "review_note": (
            "STS-61 photograph of Hubble in orbit with the Moon, December 1993. "
            "Candidate still for row 27. It is not servicing-mission motion footage."
        ),
    },
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url, dest):
    if dest.exists():
        raise SystemExit(f"refusing existing file: {dest}")
    req = urllib.request.Request(url, headers={"User-Agent": "orbit-with-ben-J2141/harvest-stills-v03"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        final = response.geturl()
    dest.write_bytes(data)
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-root", type=Path, required=True)
    ap.add_argument("--pool", type=Path, default=POOL)
    args = ap.parse_args()
    root = args.media_root
    root.mkdir(parents=True, exist_ok=True)
    policy_path = root / "NASA_MEDIA_POLICY.html"
    fetch(POLICY, policy_path)
    pool = json.loads(args.pool.read_text())
    have = {asset["asset_id"] for asset in pool["assets"]}
    added = []
    for item in ITEMS:
        ident = item["asset_id"]
        if ident in have:
            raise SystemExit(f"already in pool: {ident}")
        api = "https://images-api.nasa.gov/search?nasa_id=" + ident
        evidence = root / f"{ident}_api.json"
        fetch(api, evidence)
        body = json.loads(evidence.read_text())
        hit = next(x for x in body["collection"]["items"] if x["data"][0]["nasa_id"] == ident)
        data = hit["data"][0]
        if data.get("title") != item["title_expect"]:
            raise SystemExit(f"title mismatch for {ident}: {data.get('title')!r}")
        link = next(x["href"] for x in hit["links"] if x.get("rel") == "canonical")
        image_path = root / f"{ident}.jpg"
        fetch(link, image_path)
        with Image.open(image_path) as im:
            im.verify()
        with Image.open(image_path) as im:
            width, height = im.size
            rgb = im.convert("RGB")
            stat = ImageStat.Stat(rgb)
            mean_luma = round(sum(stat.mean) / 3, 1)
        full_frame_scale = round(1920 / width, 3) if width else None
        record = {
            "asset_id": ident,
            "nasa_id": ident,
            "title": data["title"],
            "description": data.get("description"),
            "source_page": "https://images.nasa.gov/details/" + ident,
            "source_api": api,
            "source_url": link,
            "credit": data.get("secondary_creator") or data.get("center") or "NASA",
            "date_created": data.get("date_created"),
            "local_path": str(image_path),
            "sha256": sha(image_path),
            "bytes": image_path.stat().st_size,
            "width": width,
            "height": height,
            "mean_luma": mean_luma,
            "full_frame_scale_to_1920": full_frame_scale,
            "upscale_cap": 2.35,
            "rows": item["rows"],
            "assigned_uses": 0,
            "max_uses": 2,
            "native_motion": False,
            "download_status": "downloaded",
            "review_status": "candidate_still_not_admitted",
            "review_note": item["review_note"],
            "licence_status": "pending_per_asset_NASA_media_guidelines",
            "licence_policy": POLICY,
            "licence_evidence_path": str(policy_path),
            "licence_evidence_sha256": sha(policy_path),
            "source_evidence_path": str(evidence),
            "source_evidence_sha256": sha(evidence),
            "generation_authorized": False,
            "rights_review": "NASA Images record read. Not cleared for the cut. No third-party waiver claimed.",
        }
        if full_frame_scale and full_frame_scale > 2.35:
            record["review_note"] += f" Full-frame scale to 1920 is {full_frame_scale}×, over the 2.35× cap; inset only."
        pool["assets"].append(record)
        added.append(record)

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
    sheet_path = root / "contact_sheet_stills_v03.jpg"
    if sheet_path.exists():
        raise SystemExit(f"refusing existing file: {sheet_path}")
    sheet.save(sheet_path, quality=90)
    pool["status"] = "partial_harvest_not_KEEP"
    pool["spend_gbp"] = 0
    pool["stills_v03_contact_sheet"] = str(sheet_path)
    pool["stills_v03_contact_sheet_sha256"] = sha(sheet_path)
    pool["stills_v03_rejected_at_metadata"] = [
        {
            "asset_id": "iss058e005282",
            "title": "View of the Earth's limb with an aurora",
            "source_page": "https://images.nasa.gov/details/iss058e005282",
            "reason": "Metadata places the frame over Ukraine and Russia, not an Arctic limb. Still, not a time-lapse. Not downloaded.",
        }
    ]
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
                "full_frame_scale_to_1920": record["full_frame_scale_to_1920"],
                "rows": record["rows"],
            }
            for record in added
        ],
    }
    check_path = HERE / "HARVEST_STILLS_TECHNICAL_CHECK_v03.json"
    if check_path.exists():
        raise SystemExit(f"refusing existing file: {check_path}")
    check_path.write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
