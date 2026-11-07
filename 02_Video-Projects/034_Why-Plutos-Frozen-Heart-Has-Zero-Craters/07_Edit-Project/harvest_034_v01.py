#!/usr/bin/env python3
"""J2370: £0 harvest of locked 034 SHOT_LIST_v01 plates.

Downloads every asset in SOURCE_EVIDENCE_v01.json, keeps a file only when its
SHA-256 matches that evidence, and writes HARVEST_POOL_v01.json plus a contact
sheet. No generation, no upload, no graphics renders.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "SOURCE_EVIDENCE_v01.json"
NAS_ROOT = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/harvest_v01"
)
UA = "OrbitWithBen/1.0 (https://github.com/TheLaughingGod1986/orbit-with-ben; J2370 archive harvest) python-urllib"
WIKI_LOCK = threading.Lock()
WIKI_NEXT = [0.0]
FRAME0_ID = "PIA20291"
SHORT_FRAME0_ID = "PIA19952"


def polite_wait(url: str) -> None:
    if "wikimedia.org" not in url:
        return
    with WIKI_LOCK:
        delay = WIKI_NEXT[0] - time.time()
        if delay > 0:
            time.sleep(delay)
        WIKI_NEXT[0] = time.time() + 12


def get_bytes(url: str, timeout: int = 180) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(4):
        polite_wait(url)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                ctype = response.headers.get("Content-Type", "")
                data = response.read()
            return data, ctype
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 429:
                time.sleep(20 * (attempt + 1))
                continue
            if exc.code in {500, 502, 503, 504}:
                time.sleep(5)
                continue
            raise
        except Exception as exc:  # noqa: BLE001 — retry transient NASA/Commons failures
            last_error = exc
            time.sleep(5)
    raise last_error or RuntimeError(url)


def get_json(url: str):
    data, ctype = get_bytes(url, timeout=60)
    if "html" in ctype.lower() or data[:1] in (b"<", b" "):
        raise RuntimeError(f"not json from {url} ({ctype})")
    return json.loads(data)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for url in urls:
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def nasa_urls(nasa_id: str) -> list[str]:
    urls: list[str] = []
    try:
        search = get_json(
            "https://images-api.nasa.gov/search?nasa_id=" + urllib.parse.quote(nasa_id)
        )
    except Exception as exc:  # noqa: BLE001 — one id must not stop the harvest
        return [f"ERROR nasa search: {exc}"]
    items = (search.get("collection") or {}).get("items") or []
    item = next(
        (
            entry
            for entry in items
            if (entry.get("data") or [{}])[0].get("nasa_id", "").lower() == nasa_id.lower()
        ),
        None,
    )
    if item is None and items:
        item = items[0]
    if not item:
        return urls
    for link in item.get("links") or []:
        href = link.get("href") or ""
        if any(token in href for token in ("~orig", "~large")):
            urls.append(href)
    collection = item.get("href")
    if collection:
        try:
            listing = get_json(collection)
        except Exception:
            listing = []
        if isinstance(listing, list):
            urls.extend(
                entry
                for entry in listing
                if isinstance(entry, str)
                and "~orig" in entry
                and not entry.endswith(".json")
            )
    return unique(urls)


def commons_original(file_title: str) -> list[str]:
    query = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": file_title,
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "format": "json",
        }
    )
    try:
        payload = get_json("https://commons.wikimedia.org/w/api.php?" + query)
    except Exception as exc:  # noqa: BLE001
        return [f"ERROR commons: {exc}"]
    pages = (payload.get("query") or {}).get("pages") or {}
    urls: list[str] = []
    for page in pages.values():
        for info in page.get("imageinfo") or []:
            if info.get("url"):
                urls.append(info["url"])
    return urls


def nasa_id_from(asset_id: str) -> str | None:
    stem = asset_id.split(":", 1)[-1].rsplit(".", 1)[0]
    if stem.startswith(("PIA", "KSC-", "NHQ", "as", "ksc_")):
        return stem
    return None


def candidate_urls(asset: dict) -> list[str]:
    direct = (asset.get("direct_file_url") or "").strip()
    urls: list[str] = []
    if direct and "/wiki/" not in direct:
        urls.append(direct)
    asset_id = asset["id"]
    nasa_id = nasa_id_from(asset_id)
    if asset.get("api_url") or nasa_id:
        found = nasa_urls(nasa_id or asset_id)
        urls.extend(url for url in found if not url.startswith("ERROR"))
    if asset_id.startswith("File:") or "commons.wikimedia.org" in (
        asset.get("canonical_url") or ""
    ):
        title = asset_id if asset_id.startswith("File:") else ""
        name = title.split(":", 1)[-1]
        if name:
            urls.append(
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                + urllib.parse.quote(name, safe="")
            )
        found = commons_original(title)
        urls.extend(url for url in found if url and not url.startswith("ERROR"))
    # Prefer original renditions over large derivatives.
    def rank(url: str) -> tuple[int, str]:
        if "~orig" in url or "upload.wikimedia.org" in url:
            return (0, url)
        if "~large" in url:
            return (1, url)
        return (2, url)

    return sorted(unique(urls), key=rank)


def safe_name(asset_id: str, url: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".mp4", ".webm", ".ogv", ".mov"}:
        suffix = ".bin"
    slug = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in asset_id)
    return (slug[:140] or "asset") + suffix


def looks_like_html(data: bytes, ctype: str) -> bool:
    if "html" in ctype.lower():
        return True
    head = data[:200].lstrip().lower()
    return head.startswith(b"<!doctype") or head.startswith(b"<html")


def index_matches(out_dir: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    if not out_dir.is_dir():
        return found
    for path in out_dir.iterdir():
        if not path.is_file() or path.suffix == ".part" or path.name.endswith(".contact.jpg"):
            continue
        digest = sha256(path.read_bytes())
        found[digest] = path
    return found


def harvest_one(
    asset: dict, banned: set[str], out_dir: Path, already: dict[str, Path], previous: dict[str, dict]
) -> dict:
    asset_id = asset["id"]
    record = {
        "id": asset_id,
        "title": asset.get("title"),
        "kind": asset["kind"],
        "license": asset.get("license"),
        "canonical_url": asset.get("canonical_url"),
        "rights_url": asset.get("rights_url"),
        "api_url": asset.get("api_url"),
        "evidence_sha256": asset["sha256"],
        "dimensions_expected": asset.get("dimensions"),
        "rows": asset.get("rows"),
        "raw_appearances": asset.get("raw_appearances"),
        "separated_appearances": asset.get("separated_appearances"),
        "spend_gbp": 0,
    }
    if asset_id in banned:
        record["download_status"] = "REFUSED_BANNED"
        return record
    existing = already.get(asset["sha256"])
    if existing is not None:
        kept = previous.get(asset_id)
        if kept and kept.get("sha256") == asset["sha256"]:
            kept["local_path"] = str(existing)
            kept["resumed"] = True
            print(f"KEEP {asset_id} {existing.name}", flush=True)
            return kept
        nasa_id = nasa_id_from(asset_id)
        record.update(
            download_status="HASH_MATCH",
            sha256=asset["sha256"],
            sha256_matches_evidence=True,
            local_path=str(existing),
            bytes=existing.stat().st_size,
            resumed=True,
            download_url=(
                f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~orig.jpg" if nasa_id else None
            ),
        )
        if asset["kind"] == "still_image":
            try:
                with Image.open(existing) as image:
                    record["width"] = image.width
                    record["height"] = image.height
            except Exception as exc:  # noqa: BLE001
                record["image_error"] = str(exc)[:200]
        print(f"KEEP {asset_id} {existing.name}", flush=True)
        return record
    urls = [url for url in candidate_urls(asset) if not url.startswith("ERROR")]
    record["candidate_urls"] = urls
    if not urls:
        record["download_status"] = "NO_URL"
        return record
    tried = []
    for url in urls:
        try:
            data, ctype = get_bytes(url, timeout=300 if asset["kind"] == "native_video" else 180)
        except Exception as exc:  # noqa: BLE001
            tried.append({"url": url, "error": f"{exc.__class__.__name__}: {exc}"[:300]})
            continue
        if looks_like_html(data, ctype):
            tried.append({"url": url, "error": f"html ({ctype})"})
            continue
        digest = sha256(data)
        tried.append({"url": url, "sha256": digest, "bytes": len(data), "content_type": ctype})
        if digest != asset["sha256"]:
            continue
        dest = out_dir / safe_name(asset_id, url)
        if dest.exists() and sha256(dest.read_bytes()) == digest:
            pass
        else:
            dest.write_bytes(data)
        record.update(
            download_status="HASH_MATCH",
            sha256=digest,
            sha256_matches_evidence=True,
            download_url=url,
            local_path=str(dest),
            bytes=len(data),
            content_type=ctype,
        )
        if asset["kind"] == "still_image":
            try:
                with Image.open(dest) as image:
                    record["width"] = image.width
                    record["height"] = image.height
            except Exception as exc:  # noqa: BLE001
                record["image_error"] = str(exc)[:200]
        print(f"MATCH {asset_id} {len(data)} {dest.name}", flush=True)
        return record
    record["download_status"] = "HASH_MISMATCH"
    record["sha256_matches_evidence"] = False
    record["tried"] = tried
    print(f"MISS {asset_id} tried {len(tried)}", flush=True)
    return record


def contact_sheet(matched: list[dict], dest: Path) -> None:
    columns = 8
    thumb_w, thumb_h, label_h = 240, 150, 32
    rows = max(1, (len(matched) + columns - 1) // columns)
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), (22, 34, 56))
    draw = ImageDraw.Draw(sheet)
    for index, record in enumerate(matched):
        x = (index % columns) * thumb_w
        y = (index // columns) * (thumb_h + label_h)
        frame = Image.new("RGB", (thumb_w - 8, thumb_h - 8), (40, 52, 74))
        path = Path(record["local_path"])
        try:
            if record["kind"] == "still_image":
                with Image.open(path) as image:
                    image = image.convert("RGB")
                    image.thumbnail((thumb_w - 8, thumb_h - 8))
                    frame.paste(image, ((frame.width - image.width) // 2, (frame.height - image.height) // 2))
            else:
                still = path.with_suffix(".contact.jpg")
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-ss", "1", "-i", str(path),
                        "-frames:v", "1", "-vf", "scale=232:142:force_original_aspect_ratio=decrease",
                        str(still),
                    ],
                    check=False,
                    capture_output=True,
                    timeout=60,
                )
                if still.exists():
                    with Image.open(still) as image:
                        image = image.convert("RGB")
                        frame.paste(image, ((frame.width - image.width) // 2, (frame.height - image.height) // 2))
        except Exception:
            pass
        sheet.paste(frame, (x + 4, y + 4))
        draw.text((x + 6, y + thumb_h), record["id"][:34], fill="white")
    sheet.save(dest, quality=85)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    evidence = json.loads(EVIDENCE.read_text())
    banned = set(evidence["banned_and_deduplicated_ids"])
    assets = list(evidence["assets"].values())
    if banned & {asset["id"] for asset in assets}:
        raise SystemExit("banned id is inside the harvest list")
    NAS_ROOT.mkdir(parents=True, exist_ok=True)
    matched_dir = NAS_ROOT / "matched"
    matched_dir.mkdir(exist_ok=True)
    already = index_matches(matched_dir)
    previous: dict[str, dict] = {}
    prior = NAS_ROOT / "HARVEST_POOL_v01.json"
    if prior.exists():
        for item in json.loads(prior.read_text()).get("assets") or []:
            if item.get("download_status") == "HASH_MATCH":
                previous[item["id"]] = item
    print(f"resume index {len(already)} hashed files, {len(previous)} prior matches", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(harvest_one, asset, banned, matched_dir, already, previous)
            for asset in assets
        ]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda record: record["id"])
    matched = [record for record in results if record.get("download_status") == "HASH_MATCH"]
    sheet = NAS_ROOT / "contact_sheet_v01.jpg"
    contact_sheet(matched, sheet)
    sums = NAS_ROOT / "SHA256SUMS.txt"
    sums.write_text(
        "".join(f"{record['sha256']}  matched/{Path(record['local_path']).name}\n" for record in matched)
    )
    over = [
        record["id"]
        for record in results
        if (record.get("raw_appearances") or 0) > 2 or (record.get("separated_appearances") or 0) > 2
    ]
    pool_doc = {
        "job": "J2370",
        "film": "OWB:034",
        "shot_list": "shot_list_v01.csv",
        "source_evidence": "SOURCE_EVIDENCE_v01.json",
        "source_evidence_sha256": sha256(EVIDENCE.read_bytes()),
        "spend_gbp": 0,
        "orbit_beats": 0,
        "frame0_id": FRAME0_ID,
        "excluded_short_frame0_id": SHORT_FRAME0_ID,
        "short_id_not_reused_at_frame0": "gmzaCfJF1gA",
        "banned_ids_excluded": sorted(banned),
        "banned_ids_present": sorted(banned & {record["id"] for record in results}),
        "assets_expected": len(assets),
        "assets_hash_matched": len(matched),
        "use_counts_over_2": over,
        "media_root": str(matched_dir),
        "contact_sheet": str(sheet),
        "sha256sums": str(sums),
        "status": "HASH_MATCHED" if len(matched) == len(assets) and not over else "PARTIAL",
        "assets": results,
    }
    text = json.dumps(pool_doc, indent=2) + "\n"
    (NAS_ROOT / "HARVEST_POOL_v01.json").write_text(text)
    (HERE / "HARVEST_POOL_v01.json").write_text(text)
    print(
        f"STATUS {pool_doc['status']} matched {len(matched)}/{len(assets)} sheet {sheet}",
        flush=True,
    )
    return 0 if pool_doc["status"] == "HASH_MATCHED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
