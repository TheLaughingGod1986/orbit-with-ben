#!/usr/bin/env python3
"""Download Venus 023 nasa_pool_v01.json into nasa_pool_v01/."""
from __future__ import annotations
import json, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "nasa_pool_v01"
pool = json.loads((HERE / "nasa_pool_v01.json").read_text())
UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenVenusHarvest/1.0"}
OUT.mkdir(parents=True, exist_ok=True)

def get(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 20_000:
        head = dest.read_bytes()[:15]
        if not head.lower().startswith(b"<!doctype") and not head.lower().startswith(b"<html"):
            print("have", dest.name); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if len(data) < 20_000 or data[:15].lower().startswith(b"<!doctype") or data[:10].lower().startswith(b"<html"):
            print("bad", dest.name, len(data)); return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print("get", dest.name, len(data)); return True
    except Exception as e:
        print("FAIL", dest.name, e); return False

ok = 0
for e in pool:
    ext = ".mp4" if e["orig"].endswith(".mp4") else ".jpg"
    if get(e["orig"], OUT / e["section"] / f"{e['nasa_id']}{ext}"):
        ok += 1
print(f"DONE ok={ok}/{len(pool)} out={OUT}")
