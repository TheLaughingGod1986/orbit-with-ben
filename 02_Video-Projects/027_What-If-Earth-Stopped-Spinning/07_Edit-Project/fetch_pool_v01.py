#!/usr/bin/env python3
"""Download OWB 027 Earth Stopped Spinning pool_v01.json into pool_v01/<section>/ (gitignored).

Usage: python3 fetch_pool_v01.py [OUT_DIR] [--sheets]
- Originals land as <file_id>.<ext> (jpg / png / tif / mp4; ESO .m4v saved as .mp4). TIF originals also get a
  same-name .jpg derivative for the edit (q=92) via Pillow if available.
- --sheets builds one contact sheet per section in OUT_DIR/_contact/<section>.jpg (stills only).
- Writes OUT_DIR/_fetch_report.json with ok/fail per entry.
Sources: NASA (PD). £0.
"""
from __future__ import annotations
import json, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = sys.argv[sys.argv.index("--pool") + 1] if "--pool" in sys.argv else "pool_v01.json"
args = [a for a in sys.argv[1:] if not a.startswith("--") and a != POOL]
SHEETS = "--sheets" in sys.argv
OUT = Path(args[0]) if args else HERE / "pool_v01"
pool = json.loads((HERE / POOL).read_text())
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenEarthSpin/1.0"}
MAGIC = {".png": [b"\x89PNG"], ".jpg": [b"\xff\xd8"], ".gif": [b"GIF8"], ".tif": [b"II*\x00", b"MM\x00*"], ".mp4": [b"ftyp"],
         ".webm": [b"\x1a\x45\xdf\xa3"]}
OUT.mkdir(parents=True, exist_ok=True)

def ext_of(url: str) -> str:
    u = url.lower().split("?")[0]
    for e in (".mp4", ".m4v", ".webm", ".gif", ".tif", ".png", ".jpg", ".jpeg"):
        if u.endswith(e):
            return {".jpeg": ".jpg", ".m4v": ".mp4"}.get(e, e)
    return ".jpg"

def valid(data: bytes, ext: str) -> bool:
    head = data[:16]
    if ext == ".mp4":
        return b"ftyp" in head
    return any(head.startswith(m) for m in MAGIC[ext])

def get(url: str, dest: Path, ext: str) -> tuple[bool, str]:
    if dest.exists() and dest.stat().st_size > 4_000:
        with dest.open("rb") as f:
            if valid(f.read(16), ext):
                return True, "have"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            tmp = dest.with_suffix(dest.suffix + ".part")
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(req, timeout=300) as r, tmp.open("wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            with tmp.open("rb") as f:
                head = f.read(16)
            if tmp.stat().st_size < 4_000 or not valid(head, ext):
                tmp.unlink(missing_ok=True)
                return False, f"bad content ({head[:8]!r})"
            tmp.replace(dest)
            return True, f"get {dest.stat().st_size}"
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(2 * (attempt + 1))
    return False, err

def tif_to_jpg(src: Path) -> None:
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        dst = src.with_suffix(".jpg")
        if dst.exists():
            return
        im = Image.open(src)
        im = im.convert("RGB")
        im.save(dst, "JPEG", quality=92)
    except Exception as e:  # noqa: BLE001
        print("  tif->jpg FAIL", src.name, e)

report, ok = [], 0
for e in pool:
    ext = ext_of(e["orig"])
    dest = OUT / e["section"] / f"{e['file_id']}{ext}"
    good, msg = get(e["orig"], dest, ext)
    if good and ext == ".tif":
        tif_to_jpg(dest)
    print(("ok  " if good else "FAIL"), e["section"], dest.name, msg, flush=True)
    ok += good
    report.append({**e, "local": str(dest), "ok": good, "msg": msg})

(OUT / ("_fetch_report.json" if POOL == "pool_v01.json" else f"_fetch_report_{Path(POOL).stem}.json")).write_text(json.dumps(report, indent=1, ensure_ascii=False))
print(f"DONE ok={ok}/{len(pool)} out={OUT}")

if SHEETS:
    try:
        from PIL import Image, ImageDraw, ImageSequence
    except ImportError:
        print("Pillow missing; no sheets"); sys.exit(0)
    Image.MAX_IMAGE_PIXELS = None
    sheet_dir = OUT / "_contact"; sheet_dir.mkdir(exist_ok=True)
    secs: dict[str, list[dict]] = {}
    for r in report:
        if r["ok"]:
            secs.setdefault(r["section"], []).append(r)
    TW, TH, COLS = 480, 300, 4
    for sec, items in secs.items():
        tiles = []
        for r in items:
            p = Path(r["local"])
            label = r["file_id"]
            try:
                if p.suffix == ".mp4":
                    import subprocess, tempfile
                    fr = Path(tempfile.mkstemp(suffix=".jpg")[1])
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "8", "-i", str(p), "-frames:v", "1", str(fr)], check=True)
                    im = Image.open(fr); label += " [mp4]"
                else:
                    src = p.with_suffix(".jpg") if p.suffix == ".tif" and p.with_suffix(".jpg").exists() else p
                    im = Image.open(src)
                    if p.suffix == ".gif":
                        im = next(ImageSequence.Iterator(im)); label += " [gif]"
                im = im.convert("RGB"); im.thumbnail((TW, TH - 24))
                t = Image.new("RGB", (TW, TH), (20, 20, 20)); t.paste(im, ((TW - im.width) // 2, 0))
                ImageDraw.Draw(t).text((6, TH - 20), label[:60], fill=(255, 220, 0))
                tiles.append(t)
            except Exception as ex:  # noqa: BLE001
                print("  sheet skip", p.name, ex)
        if not tiles:
            continue
        rows = (len(tiles) + COLS - 1) // COLS
        sheet = Image.new("RGB", (TW * COLS, TH * rows + 30), (0, 0, 0))
        ImageDraw.Draw(sheet).text((8, 8), f"OWB 027 pool_v01 / {sec} ({len(tiles)})", fill=(255, 255, 255))
        for k, t in enumerate(tiles):
            sheet.paste(t, ((k % COLS) * TW, 30 + (k // COLS) * TH))
        sheet.save(sheet_dir / f"{sec}.jpg", quality=85)
        print("sheet", sheet_dir / f"{sec}.jpg")
