#!/usr/bin/env python3
"""Download one day of DSCOVR EPIC natural-colour frames (2048x2048 PNG, NASA public domain) for 027's frame 0.

EPIC shoots about hourly around the June solstice (22 frames a day, ~16 degrees of turn between frames), the
best cadence in the archive. The frames go to render scratch, not the repo. £0.

Usage: python3 fetch_epic_v01.py [--day 2025-06-21] [--out /private/tmp/owb027_epic_v01]
"""
from __future__ import annotations
import argparse, json, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 OrbitWithBenEarthSpin/1.0"}


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


ap = argparse.ArgumentParser()
ap.add_argument("--day", default="2025-06-21")
ap.add_argument("--out", default="/private/tmp/owb027_epic_v01")
a = ap.parse_args()

out = Path(a.out) / a.day
out.mkdir(parents=True, exist_ok=True)
frames = json.loads(get(f"https://epic.gsfc.nasa.gov/api/natural/date/{a.day}"))
y, m, d = a.day.split("-")
for i, f in enumerate(frames):
    dest = out / f"{i:02d}_{f['image']}.png"
    if dest.exists() and dest.stat().st_size > 100_000:
        continue
    dest.write_bytes(get(f"https://epic.gsfc.nasa.gov/archive/natural/{y}/{m}/{d}/png/{f['image']}.png"))
    print("ok", dest.name, f["date"], flush=True)
(out / "frames.json").write_text(json.dumps(frames, indent=1) + "\n")
print(f"done {len(frames)} frames -> {out}")
