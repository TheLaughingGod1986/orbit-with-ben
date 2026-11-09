#!/usr/bin/env python3
"""J2290: £0 harvest of the 38 missing film-033 pool IDs plus aux PIA00271.

Downloads public NASA / ESA Webb / Wikimedia files only. Records the path,
byte size, pixel size and SHA-256 of whatever actually arrived. Nothing here
is marked KEEP: a filename is not evidence of the subject. svs20390 is never
fetched. No Omni, Veo, Flow, Vertex or cash.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "03_Reference-Material" / "harvest_J2290_v01"
POOL_IN = HERE / "STILLS_POOL_STATUS_v01.json"
MANIFEST = HERE / "HARVEST_MANIFEST_J2290.json"
POOL_OUT = HERE / "STILLS_POOL_STATUS_v02.json"
UA = "OrbitWithBenStudio/1.0 (film 033 public-domain harvest; +https://github.com/TheLaughingGod1986/orbit-with-ben)"

# Frame-0 Hubble pair is harvested as itself. The standalone Short open is banned.
BANNED = {"svs20390_shot9_beauty_rings.mp4", "svs20390"}


def get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_stem(asset_id: str) -> str:
    name = asset_id[5:] if asset_id.startswith("File:") else asset_id
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")


def looks_like_image(data: bytes) -> bool:
    return data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff" or data[:4] == b"GIF8" or data[:4] == b"RIFF"


def image_info(path: Path) -> dict:
    with Image.open(path) as im:
        im.load()
        return {"width": im.width, "height": im.height, "mode": im.mode, "format": im.format}


def pick_raster(urls: list[str]) -> str | None:
    ranked = []
    for url in urls:
        low = url.lower().split("?")[0]
        if not low.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            continue
        score = 0
        if "~orig" in low:
            score += 50
        elif "~large" in low or "/large/" in low:
            score += 40
        elif "~medium" in low:
            score += 30
        if low.endswith(".png"):
            score += 5
        if "thumb" in low or "~small" in low or "~thumb" in low:
            score -= 30
        ranked.append((score, len(url), url))
    if not ranked:
        return None
    ranked.sort(reverse=True)
    return ranked[0][2]


def nasa_item(nasa_id: str | None = None, query: str | None = None) -> dict | None:
    if nasa_id:
        url = "https://images-api.nasa.gov/search?media_type=image&nasa_id=" + urllib.parse.quote(nasa_id)
    else:
        url = "https://images-api.nasa.gov/search?media_type=image&q=" + urllib.parse.quote(query or "")
    payload = json.loads(get(url))
    items = payload.get("collection", {}).get("items") or []
    if nasa_id:
        for item in items:
            data = (item.get("data") or [{}])[0]
            if data.get("nasa_id") == nasa_id:
                return item
        # Never keep a search neighbour. A different nasa_id is a different picture.
        return None
    return items[0] if items else None


def nasa_asset_urls(item: dict) -> list[str]:
    href = item.get("href")
    if not href:
        return []
    body = json.loads(get(href))
    return body if isinstance(body, list) else []


def meta_of(item: dict) -> dict:
    data = (item.get("data") or [{}])[0]
    keep = ("nasa_id", "title", "description", "center", "date_created", "secondary_creator", "media_type", "keywords")
    out = {k: data.get(k) for k in keep if k in data}
    desc = out.get("description") or ""
    if isinstance(desc, str) and len(desc) > 700:
        out["description"] = desc[:700] + "…"
    return out


def save_image(dest: Path, data: bytes) -> dict:
    dest.write_bytes(data)
    info = image_info(dest)
    info.update(bytes=len(data), sha256=sha256(data), local_path=str(dest))
    return info


def harvest_nasa(asset_id: str, nasa_id: str | None = None, query: str | None = None) -> dict:
    rec = {
        "canonical_id": asset_id,
        "review_status": "HARVESTED_NOT_KEEP",
        "spend_gbp": 0,
    }
    item = nasa_item(nasa_id=nasa_id, query=query)
    if not item and query is None and nasa_id:
        item = nasa_item(query=nasa_id)
    if not item:
        rec.update(download_status="ERROR", error="no NASA images-api hit")
        return rec
    meta = meta_of(item)
    rec["nasa_metadata"] = meta
    rec["source_page"] = "https://images.nasa.gov/details/" + urllib.parse.quote(meta.get("nasa_id") or asset_id)
    urls = nasa_asset_urls(item)
    chosen = pick_raster(urls)
    if not chosen:
        # Photojournal fallbacks. Recorded only if the bytes are a real image.
        nid = meta.get("nasa_id") or nasa_id or asset_id
        for url in (
            f"https://photojournal.jpl.nasa.gov/jpeg/{nid}.jpg",
            f"https://images-assets.nasa.gov/image/{nid}/{nid}~medium.jpg",
            f"https://images-assets.nasa.gov/image/{nid}/{nid}~orig.jpg",
        ):
            try:
                data = get(url)
            except Exception:
                continue
            if looks_like_image(data) and len(data) > 8000:
                chosen = url
                urls = [url]
                break
        if not chosen:
            rec.update(download_status="ERROR", error="metadata found but no raster URL", candidate_urls=urls[:12])
            return rec
    data = get(chosen, timeout=120)
    if not looks_like_image(data) or len(data) < 4000:
        rec.update(download_status="ERROR", error="download was not an image", download_url=chosen, bytes=len(data))
        return rec
    ext = ".png" if data[:8] == b"\x89PNG\r\n\x1a\n" else ".gif" if data[:4] == b"GIF8" else ".jpg"
    dest = OUT / f"{safe_stem(asset_id)}{ext}"
    rec.update(save_image(dest, data))
    rec.update(download_status="downloaded", download_url=chosen, credit=meta.get("secondary_creator") or meta.get("center") or "NASA")
    # Identity comes from the catalogue title, not from the pool filename.
    rec["catalogue_title"] = meta.get("title")
    return rec


def harvest_commons(asset_id: str) -> dict:
    title = asset_id if asset_id.startswith("File:") else "File:" + asset_id
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "titles": title,
    })
    rec = {
        "canonical_id": asset_id,
        "review_status": "HARVESTED_NOT_KEEP",
        "spend_gbp": 0,
        "source_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        "source_api": api,
    }
    payload = json.loads(get(api))
    pages = (payload.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()), {})
    if page.get("missing") is not None or "imageinfo" not in page:
        rec.update(download_status="ERROR", error="commons file missing", commons_page=page.get("title"))
        return rec
    info = page["imageinfo"][0]
    meta = info.get("extmetadata") or {}
    licence = (meta.get("LicenseShortName") or {}).get("value")
    artist = (meta.get("Artist") or {}).get("value")
    credit = re.sub(r"<[^>]+>", "", artist or "Wikimedia Commons")
    rec.update(licence=licence, credit=credit[:240], commons_mime=info.get("mime"), commons_description=(meta.get("ImageDescription") or {}).get("value", "")[:400])
    url = info["url"]
    # Prefer a large thumbnail when the original is a multi-10 MB tiff.
    thumb = info.get("thumburl")
    download = url
    if info.get("mime") not in ("image/jpeg", "image/png", "image/gif", "image/webp"):
        thumb_api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url", "iiurlwidth": "2000", "titles": title,
        })
        thumb_payload = json.loads(get(thumb_api))
        tpages = (thumb_payload.get("query") or {}).get("pages") or {}
        tpage = next(iter(tpages.values()), {})
        tinfo = (tpage.get("imageinfo") or [{}])[0]
        download = tinfo.get("thumburl") or thumb or url
        rec["original_url"] = url
        rec["download_note"] = "original was not a jpeg/png; saved the 2000px Commons thumbnail"
    data = get(download, timeout=120)
    if not looks_like_image(data) or len(data) < 4000:
        rec.update(download_status="ERROR", error="commons download was not an image", download_url=download)
        return rec
    ext = ".png" if data[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg"
    dest = OUT / f"{safe_stem(asset_id)}{ext}"
    rec.update(save_image(dest, data))
    rec.update(download_status="downloaded", download_url=download, catalogue_title=page.get("title"))
    return rec


def harvest_webb(asset_id: str) -> dict:
    page = "https://esawebb.org/images/weic2332a/"
    rec = {
        "canonical_id": asset_id,
        "review_status": "HARVESTED_NOT_KEEP",
        "spend_gbp": 0,
        "source_page": page,
        "alt_id": "STScI-01HGG9F546W7BDCRK3N9WRWT9Z",
        "credit": "NASA, ESA, CSA, STScI",
    }
    errors = []
    for url in (
        "https://cdn.esawebb.org/archives/images/large/weic2332a.jpg",
        "https://cdn.esawebb.org/archives/images/screen/weic2332a.jpg",
    ):
        try:
            data = get(url, timeout=120)
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            continue
        if looks_like_image(data) and len(data) > 8000:
            dest = OUT / "weic2332a.jpg"
            rec.update(save_image(dest, data))
            rec.update(download_status="downloaded", download_url=url, catalogue_title="ESA/Webb weic2332a")
            return rec
        errors.append(f"{url}: not an image ({len(data)} bytes)")
    # Fall through to NASA search on the STScI id or the word Uranus NIRCam 2023.
    try:
        alt = harvest_nasa(asset_id, query="weic2332a Uranus NIRCam")
        alt["webb_errors"] = errors
        alt["source_page"] = alt.get("source_page") or page
        return alt
    except Exception as exc:
        errors.append(str(exc))
    rec.update(download_status="ERROR", error="; ".join(errors))
    return rec


def one(asset_id: str) -> dict:
    if asset_id in BANNED or "svs20390" in asset_id:
        return {"canonical_id": asset_id, "download_status": "EXCLUDED", "error": "banned Short open"}
    try:
        if asset_id.startswith("File:"):
            return harvest_commons(asset_id)
        if asset_id == "weic2332a":
            return harvest_webb(asset_id)
        if asset_id == "KAO_airborne_915_in_flight":
            # ARC-1979-AC79-0334 is not in images.nasa.gov. Do not accept a
            # search neighbour (the demolition photo ACD24-0161-013 is a
            # different subject). The repair pass resolves a Commons C-141A file.
            rec = harvest_nasa(asset_id, nasa_id="ARC-1979-AC79-0334")
            rec["pool_alias"] = "ARC-1979-AC79-0334"
            return rec
        if asset_id.startswith("ARC-"):
            return harvest_nasa(asset_id, nasa_id=asset_id)
        if asset_id.startswith("PIA"):
            return harvest_nasa(asset_id, nasa_id=asset_id)
        return {"canonical_id": asset_id, "download_status": "ERROR", "error": "no route"}
    except Exception as exc:
        return {"canonical_id": asset_id, "download_status": "ERROR", "review_status": "HARVESTED_NOT_KEEP", "error": str(exc), "spend_gbp": 0}


def main() -> None:
    pool = json.loads(POOL_IN.read_text())
    ids = list(pool["missing_ids_only"]) + list(pool.get("missing_auxiliary_ids") or [])
    if any("svs20390" in i for i in ids):
        raise SystemExit("banned id present in the harvest list")
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(one, asset_id): asset_id for asset_id in ids}
        for fut in as_completed(futures):
            rec = fut.result()
            records.append(rec)
            print(f"{rec.get('download_status','?'):12} {rec['canonical_id']} {rec.get('error','')}", flush=True)
    records.sort(key=lambda r: ids.index(r["canonical_id"]))
    downloaded = [r for r in records if r.get("download_status") == "downloaded"]
    failed = [r for r in records if r.get("download_status") != "downloaded"]
    sums = "".join(f"{r['sha256']}  {Path(r['local_path']).name}\n" for r in downloaded)
    (OUT / "SHA256SUMS.txt").write_text(sums)
    manifest = {
        "job": "J2290",
        "film": "033_Why-This-Planet-Has-21-Year-Winters",
        "spend_gbp": 0,
        "rule": "Paths and SHA-256 are from the downloaded bytes. review_status is HARVESTED_NOT_KEEP. Catalogue titles are copied from the source record, not inferred from the pool filename.",
        "banned_not_fetched": ["svs20390_shot9_beauty_rings.mp4"],
        "frame_0_lock": "PIA01283 + PIA01280 stay the Frame-0 Hubble pair. They are not the Short open svs20390.",
        "appearance_cap": "≤2 still appearances remain the lock in STILLS_LOCK_v01.md. This harvest does not assign extra cuts.",
        "requested": ids,
        "downloaded": len(downloaded),
        "failed": len(failed),
        "assets": records,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    status = dict(pool)
    status.update({
        "job": "J2290",
        "upstream_job": pool.get("job"),
        "spend_gbp": 0,
        "summary": {
            **pool.get("summary", {}),
            "harvest_requested": len(ids),
            "harvest_downloaded": len(downloaded),
            "harvest_failed": len(failed),
            "keep_assigned": 0,
        },
        "harvested_assets": [
            {
                "canonical_id": r["canonical_id"],
                "catalogue_title": r.get("catalogue_title"),
                "local_path": r.get("local_path"),
                "sha256": r.get("sha256"),
                "bytes": r.get("bytes"),
                "width": r.get("width"),
                "height": r.get("height"),
                "download_url": r.get("download_url"),
                "source_page": r.get("source_page"),
                "credit": r.get("credit"),
                "licence": r.get("licence"),
                "review_status": "HARVESTED_NOT_KEEP",
            }
            for r in downloaded
        ],
        "harvest_failed": [{"canonical_id": r["canonical_id"], "error": r.get("error")} for r in failed],
    })
    POOL_OUT.write_text(json.dumps(status, indent=2) + "\n")
    print(f"DONE downloaded={len(downloaded)} failed={len(failed)}", flush=True)


if __name__ == "__main__":
    main()
