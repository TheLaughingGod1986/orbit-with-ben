#!/usr/bin/env python3
"""J0350: 028 Gliese 710 harvest v01. £0. No mint.

Pulls every PLATE_BOARDS_v02 plate with route "harvest" (33 plates, 21 files).
Media stays in nasa_pool_v01 (gitignored). This script writes the licence check,
SHA-256 list and contact sheet under _evidence/.

  OWB_HARVEST_POOL=/path/to/028_harvest_v01 python3 _harvest_gliese_v01.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARDS = HERE / "PLATE_BOARDS_v02.json"
POOL_JSON = HERE / "SOURCE_POOL_v02.json"
OUT = Path(os.environ.get("OWB_HARVEST_POOL", str(HERE / "nasa_pool_v01" / "028_harvest_v01")))
EVIDENCE = HERE / "_evidence"
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenGlieseHarvest/1.0 (J0350; research)"}
ESO_POLICY = "https://www.eso.org/public/copyright/"
HUBBLE_POLICY = "https://esahubble.org/copyright/"
# Same asset, higher rendition from the same page. The boarded URL stays on the record.
HIGHER = {
    "gaia_motion_1_6my": "https://dlmultimedia.esa.int/download/public/videos/2020/12/004/orig-2012_004_AR_EN.mp4",
    "gaia_gliese_encounter": "https://dlmultimedia.esa.int/download/public/videos/2017/08/022/orig-1708_022_AR_EN.mov",
    "eso_chajnantor": "https://cdn.eso.org/videos/hd_and_apple/chajnantormilkyway.m4v",
}


def get(url: str, timeout: int = 90) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), r.headers.get("Content-Type", "")


def get_text(url: str) -> str:
    _status, data, _ct = get(url, timeout=60)
    return data.decode("utf-8", "replace")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def visible(html: str) -> str:
    p = _Text()
    p.feed(html)
    return re.sub(r"\s+", " ", " ".join(p.parts))


def credit_div(html: str) -> str:
    m = re.search(r'<div class="credit">(.*?)</div>', html, re.S | re.I)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()


def nasa_id_from(url: str) -> str | None:
    m = re.search(r"/image/([^/]+)/", url)
    return urllib.parse.unquote(m.group(1)) if m else None


def nasa_check(nasa_id: str) -> tuple[str, str]:
    url = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"nasa_id": nasa_id})
    try:
        payload = json.loads(get_text(url))
    except Exception as e:
        return "FLAG", f"images API failed: {e}"
    hits = payload.get("collection", {}).get("items") or []
    if not hits:
        return "FLAG", f"images API has no item for {nasa_id}"
    data = hits[0].get("data") or [{}]
    title = data[0].get("title", "")
    center = data[0].get("center", "")
    return "PASS", f"NASA images library: {title} ({center}). Public domain under NASA media guidelines."


def policy_sentence(html: str, needle: str) -> str:
    text = visible(html)
    i = text.lower().find(needle.lower())
    if i < 0:
        return ""
    return text[max(0, i - 180): i + 220].strip()


def licence_check(asset: dict, eso_html: str, hubble_html: str) -> dict:
    page = asset.get("page") or ""
    file_url = asset["file"]
    stated = asset.get("licence") or ""
    notes: list[str] = []
    status = "PASS"
    credit = asset.get("credit") or ""

    if nasa_id_from(file_url) and "images-assets.nasa.gov" in file_url:
        nid = nasa_id_from(file_url)
        st, note = nasa_check(nid)
        status = st
        notes.append(note)
        notes.append(f"Boarded licence: {stated}")
    elif "sdo.gsfc.nasa.gov" in file_url:
        notes.append(
            "SDO/HMI browse jpeg. Licence is NASA's media policy (images produced by NASA are not copyrighted), "
            "as boarded. The file carries an SDO/HMI stamp in the corner; crop it at the edit, not in this pool."
        )
        notes.append(f"Boarded licence: {stated}")
    elif "esa.int" in page or "dlmultimedia.esa.int" in file_url:
        try:
            html = get_text(page)
        except Exception as e:
            status = "FLAG"
            notes.append(f"ESA page failed: {e}")
            html = ""
        if "CC BY-SA 3.0 IGO" in html:
            notes.append("ESA page contains the credit line CC BY-SA 3.0 IGO.")
        else:
            status = "FLAG"
            notes.append("ESA page does not contain CC BY-SA 3.0 IGO.")
        c = credit_div(html)
        if c:
            credit = c
            notes.append(f"Page credit: {c}")
    elif "eso.org" in page or "cdn.eso.org" in file_url:
        try:
            html = get_text(page)
        except Exception as e:
            status = "FLAG"
            notes.append(f"ESO page failed: {e}")
            html = ""
        c = credit_div(html)
        if c:
            credit = c
            notes.append(f"Page credit: {c}")
        else:
            status = "FLAG"
            notes.append("ESO page has no credit div.")
        if 'href="/public/outreach/copyright/"' in html or "Usage of ESO Images" in html:
            notes.append("Page points at the ESO usage policy.")
        else:
            status = "FLAG"
            notes.append("ESO page does not link the usage policy.")
        sentence = policy_sentence(eso_html, "Creative Commons Attribution 4.0 International License")
        if sentence:
            notes.append("ESO policy page: " + sentence)
        else:
            status = "FLAG"
            notes.append("ESO policy page did not show the CC BY 4.0 sentence this run.")
        if re.search(r"all rights reserved|not released under", html, re.I):
            status = "FLAG"
            notes.append("ESO page mentions a rights hold-back. Read it before use.")
    elif "esahubble.org" in page or "esahubble.org" in file_url:
        try:
            html = get_text(page)
        except Exception as e:
            status = "FLAG"
            notes.append(f"Hubble page failed: {e}")
            html = ""
        c = credit_div(html)
        if c:
            credit = c
            notes.append(f"Page credit: {c}")
        sentence = policy_sentence(hubble_html, "Creative Commons")
        if sentence:
            notes.append("Hubble policy page: " + sentence)
        else:
            status = "FLAG"
            notes.append("Hubble policy page did not show a Creative Commons sentence this run.")
        if "CC BY" in html or "Creative Commons" in html:
            notes.append("Image page itself names Creative Commons.")
    else:
        status = "FLAG"
        notes.append(f"No licence checker for this host. Boarded licence: {stated}")

    return {"licence_check": status, "credit_on_page": credit, "licence_notes": notes}


def download(url: str, dest: Path) -> tuple[int, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 20_000:
        return dest.stat().st_size, "cached"
    status, data, ctype = get(url, timeout=300)
    if status != 200 or len(data) < 20_000 or data[:15].lower().startswith((b"<!doctype", b"<html")):
        raise RuntimeError(f"bad body status={status} bytes={len(data)} type={ctype}")
    dest.write_bytes(data)
    return len(data), ctype


def probe(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,codec_name,duration",
        "-of", "json", str(path),
    ]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=60)
        streams = json.loads(out).get("streams") or [{}]
        s = streams[0]
        return {
            "width": int(s.get("width") or 0),
            "height": int(s.get("height") or 0),
            "codec": s.get("codec_name"),
            "duration_s": float(s["duration"]) if s.get("duration") else None,
        }
    except Exception as e:
        return {"probe_error": str(e)}


def thumb(path: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        im.thumbnail((320, 180))
        canvas = Image.new("RGB", (320, 180), (8, 10, 16))
        canvas.paste(im, ((320 - im.width) // 2, (180 - im.height) // 2))
        canvas.save(dest, quality=85)
        return
    cmd = [
        "ffmpeg", "-y", "-i", str(path), "-ss", "0.5",
        "-frames:v", "1",
        "-vf", "scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2",
        str(dest),
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)


def contact_sheet(items: list[dict], thumbs: Path, dest: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font = ImageFont.truetype(font_path, 16) if Path(font_path).exists() else ImageFont.load_default()
    cols = 5
    cell_w, cell_h = 340, 230
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (18, 22, 32))
    draw = ImageDraw.Draw(sheet)
    for i, item in enumerate(items):
        im = Image.open(thumbs / f"{item['id']}.jpg").convert("RGB")
        x = (i % cols) * cell_w + 10
        y = (i // cols) * cell_h + 8
        sheet.paste(im, (x, y))
        mark = "FLAG" if item["licence_check"] != "PASS" else "ok"
        draw.text((x, y + 184), f"{item['id']}  {mark}", fill=(240, 220, 80), font=font)
        label = ", ".join(item["plates"])
        draw.text((x, y + 204), label[:42], fill=(210, 210, 210), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, quality=85)


def main() -> None:
    boards = json.loads(BOARDS.read_text())
    pool = {a["id"]: a for a in json.loads(POOL_JSON.read_text())["assets"]}
    plates = [p for p in boards["plates"] if p.get("route") == "harvest"]
    if len(plates) != 33:
        raise SystemExit(f"expected 33 harvest plates, found {len(plates)}")
    order: list[str] = []
    by_asset: dict[str, list[str]] = {}
    for p in plates:
        by_asset.setdefault(p["asset_id"], []).append(p["id"])
        if p["asset_id"] not in order:
            order.append(p["asset_id"])

    print("fetching policy pages")
    eso_html = get_text(ESO_POLICY)
    hubble_html = get_text(HUBBLE_POLICY)

    items = []
    rejected = []
    thumbs = OUT / "_thumbs"
    for aid in order:
        asset = pool[aid]
        file_url = HIGHER.get(aid, asset["file"])
        ext = Path(urllib.parse.urlparse(file_url).path).suffix.lower() or ".bin"
        dest = OUT / f"{aid}{ext}"
        print("licence", aid)
        try:
            lic = licence_check(asset, eso_html, hubble_html)
        except Exception as e:
            lic = {"licence_check": "FLAG", "credit_on_page": asset.get("credit"), "licence_notes": [str(e)]}
        print("download", aid, file_url)
        try:
            size, ctype = download(file_url, dest)
        except Exception as e:
            rejected.append({"id": aid, "plates": by_asset[aid], "why": str(e), **lic})
            print("  REJECT", e)
            continue
        digest = sha256(dest)
        meta = probe(dest)
        try:
            thumb(dest, thumbs / f"{aid}.jpg")
        except Exception as e:
            print("  thumb failed", e)
        items.append({
            "id": aid,
            "plates": by_asset[aid],
            "title": asset.get("title"),
            "page": asset.get("page"),
            "boarded_file": asset["file"],
            "file_url": file_url,
            "rendition": "same-page higher file" if aid in HIGHER else "boarded file",
            "file": f"nasa_pool_v01/028_harvest_v01/{dest.name}",
            "bytes": size,
            "content_type": ctype,
            "sha256": digest,
            "boarded_licence": asset.get("licence"),
            "boarded_credit": asset.get("credit"),
            "picture_qa_flag": asset.get("picture_qa_flag"),
            "note": asset.get("note"),
            **meta,
            **lic,
            "generation_authorized": False,
        })
        print(f"  {lic['licence_check']} {size} {digest[:12]}")

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    payload = {
        "job": "J0350",
        "film": "028",
        "by": "cursor",
        "date": datetime.date.today().isoformat(),
        "boards": "PLATE_BOARDS_v02.json",
        "pool": "SOURCE_POOL_v02.json",
        "spend": "£0",
        "generation_authorized": False,
        "plates": len(plates),
        "files_ok": len(items),
        "files_rejected": len(rejected),
        "items": items,
        "rejected": rejected,
    }
    (EVIDENCE / "gliese_harvest_v01.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [f"{it['sha256']}  {it['file']}" for it in items]
    (EVIDENCE / "gliese_harvest_v01.sha256").write_text("\n".join(lines) + "\n")
    if items and all((thumbs / f"{it['id']}.jpg").exists() for it in items):
        contact_sheet(items, thumbs, EVIDENCE / "gliese_harvest_v01_contact.jpg")
        print("contact sheet", EVIDENCE / "gliese_harvest_v01_contact.jpg")

    flags = [it for it in items if it["licence_check"] != "PASS"]
    md = [
        "# 028 harvest v01 (J0350)",
        "",
        "£0. No Flow, Vertex, Omni, Veo or ElevenLabs. `generation_authorized` stays false.",
        "",
        f"{len(plates)} harvest plates, {len(items)} files in `nasa_pool_v01/028_harvest_v01/`, {len(rejected)} rejected, {len(flags)} licence FLAGs.",
        "Media is gitignored. This note, the JSON and the SHA-256 list are the record.",
        "",
        "| Asset | Plates | Licence check | SHA-256 |",
        "|---|---|---|---|",
    ]
    for it in items:
        md.append(
            f"| {it['id']} | {', '.join(it['plates'])} | {it['licence_check']} | `{it['sha256'][:12]}` |"
        )
    md += [
        "",
        "Proxima Centauri (`potw1343a`) has no larger Hubble rendition. The large jpeg is 604×592, so the edit scales it to frame height (under 2.35×) and fills the sides.",
        "",
    ]
    upgrades = [it for it in items if it.get("rendition") != "boarded file"]
    if upgrades:
        md += ["", "## Higher rendition from the same page", ""]
        for it in upgrades:
            md.append(
                f"- **{it['id']}**: stored `{it['file_url']}` ({it.get('width')}×{it.get('height')}). "
                f"Boarded file was `{it['boarded_file']}`."
            )
    if rejected:
        md += ["", "## Rejected", ""]
        for r in rejected:
            md.append(f"- {r['id']}: {r['why']}")
    if flags:
        md += ["", "## Licence flags", ""]
        for it in flags:
            md.append(f"- **{it['id']}**: " + " ".join(it["licence_notes"]))
    md += ["", "## Notes carried from the boards", ""]
    for it in items:
        if it.get("picture_qa_flag") or (it.get("note") and ("WARN" in it["note"] or "stamp" in it["note"].lower() or "crop" in it["note"].lower() or "colour" in it["note"].lower() or "color" in it["note"].lower())):
            md.append(f"- **{it['id']}**: {it.get('picture_qa_flag') or ''} {it.get('note') or ''}".strip())
    (EVIDENCE / "gliese_harvest_v01.md").write_text("\n".join(md) + "\n")
    print(f"DONE ok={len(items)} rejected={len(rejected)} flags={len(flags)}")


if __name__ == "__main__":
    main()
