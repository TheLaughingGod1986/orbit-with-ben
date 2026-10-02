#!/usr/bin/env python3
"""Short covers on NASA plates, for Shorts whose own frames all carry burned-in captions (NEEDS PLATE).

Same look as build_yellow_white_short_thumbs_v04.py (it reuses that file's compose()): Arial Black caps,
yellow hook word, white rest, black letterbox, no Orbit. The plates are fetched from images-api.nasa.gov
on first run and are git-ignored, like every other image.

  python3 00_Brand/Channel-Setup/tools/build_nasa_plate_short_covers.py
  ONLY_IDS=DN4L1DkerMM python3 00_Brand/Channel-Setup/tools/build_nasa_plate_short_covers.py

Writes cover_<id>.jpg and MANIFEST.json to each job's out_dir. Does not upload. Swaps on the back catalogue
need Ben's OK first (AGENTS.md).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

ROOT = v04.ROOT
LS = ROOT / "02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/08_Thumbs"
JW = ROOT / "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/10_Shorts/08_Thumbs"

JOBS = [
    {
        # Studio cover showed Europa's THIS OCEAN SHOULDN'T EXIST: set by mistake in the 3 Sep 8Bym upload mix-up.
        "id": "DN4L1DkerMM",
        "title": "The Universe Is Running Out of New Stars",
        "related": "REXYxuLOBoI",
        "uk": "",
        "role": "needs_plate_refresh",
        "nasa_id": "carina_nebula",
        "nasa_file": "carina_nebula~orig.png",
        "credit": "NASA, ESA, CSA, STScI (Webb, Cosmic Cliffs in the Carina Nebula, NGC 3324)",
        "crop_cx": 0.40,  # 9:16 window centre as a fraction of plate width: cliff edge plus the bright stars above it
        "out_dir": LS / "nasa_plate_v01",
        "lines": ["RUNNING OUT", "OF STARS"],
        "yellow": {"STARS"},
        "hero": 1,
    },
    {
        "id": "l1d1ypHxLk0",
        "title": "These Galaxies Appeared Too Early",
        "related": "ziKBPJ6FY0U",
        "uk": "",
        "role": "needs_plate_refresh",
        "nasa_id": "GSFC_20171208_Archive_e001651",
        "nasa_file": "GSFC_20171208_Archive_e001651~orig.jpg",
        "credit": "NASA, ESA (Hubble eXtreme Deep Field)",
        "crop_cx": 0.50,
        "out_dir": JW / "nasa_plate_v01",
        "lines": ["TOO", "EARLY?"],
        "yellow": {"TOO"},
        "hero": 0,
    },
]


def fetch_plate(job: dict) -> Path:
    """Download the NASA original once, then cut the 9:16 window so v04.cover_plate() keeps it whole."""
    out_dir: Path = job["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    src = out_dir / job["nasa_file"].replace("~", "_")
    if not src.exists():
        url = f"https://images-assets.nasa.gov/image/{job['nasa_id']}/{job['nasa_file']}"
        urllib.request.urlretrieve(url, src)
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    cw = min(sw, round(sh * v04.W / v04.H))
    x0 = min(max(0, round(job["crop_cx"] * sw - cw / 2)), sw - cw)
    plate = out_dir / f"plate_{job['id']}.png"
    im.crop((x0, 0, x0 + cw, sh)).save(plate)
    scale = v04.H / sh
    if scale > 2.35:
        print(f"warning: {job['id']} plate upscaled {scale:.2f}x (house limit ~2.35x)")
    return plate


def main() -> None:
    only = {x.strip() for x in os.environ.get("ONLY_IDS", "").split(",") if x.strip()}
    jobs = [j for j in JOBS if not only or j["id"] in only]
    if not jobs:
        raise SystemExit("No jobs matched ONLY_IDS")
    print("font:", v04.FONT_PATH)
    for job in jobs:
        job = dict(job, plate=fetch_plate(job))
        row = v04.compose(job)
        row.update(title=job["title"], nasa_id=job["nasa_id"], credit=job["credit"])
        Path(job["out_dir"], "MANIFEST.json").write_text(
            json.dumps({"version": "nasa_plate_v01", "font": v04.FONT_PATH,
                        "note": "NEEDS PLATE refresh on a NASA plate. Swap only after Ben's OK.",
                        "shorts": [row]}, indent=2) + "\n")
        print("wrote", row["file"])


if __name__ == "__main__":
    main()
