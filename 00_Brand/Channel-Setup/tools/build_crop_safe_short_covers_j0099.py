#!/usr/bin/env python3
"""J0099 item 1: nine back-catalogue Short covers rebuilt crop-safe (THUMBNAIL_AND_TITLE_RULES.md §2.6, §2.7).

The live covers are 16:9, so the Shorts feed's 9:16 crop cut their words (thumb audit 9 Oct, item 10).
These are 9:16 (1080x1920) in the v04 house look: words in the 16:9 centre band, so both crops keep them.
Plates are frames from each Short (no Orbit; the burned-in caption band blurred under the new words)
or a NASA plate where every frame has Orbit.
Frames come from the public Short (yt-dlp) into FRAMES; nothing here goes in git but this script.

  python3 00_Brand/Channel-Setup/tools/build_crop_safe_short_covers_j0099.py
  ONLY_IDS=xQlV9G9lqLI python3 00_Brand/Channel-Setup/tools/build_crop_safe_short_covers_j0099.py

Does not upload. Setting the covers is a separate step (Studio on CDP 9223, or thumbnails.set).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_yellow_white_short_thumbs_v04 as v04  # noqa: E402

WORK = Path(os.environ.get("J0099_WORK", "/tmp/j0099"))
FRAMES = WORK / "vid"
OUT = WORK / "after"

JOBS = [
    {"id": "xQlV9G9lqLI", "title": "Why Stars Don't Crash When Galaxies Meet", "t": 6,
     "lines": ["STARS DON'T", "CRASH"], "yellow": {"CRASH"}, "hero": 1},
    {"id": "e-7hzJv4c80", "title": "How Long Until Andromeda Hits Us?", "t": 6,
     "lines": ["ANDROMEDA", "HITS US?"], "yellow": {"ANDROMEDA"}, "hero": 1},
    {"id": "CtllH6VOhEI", "title": "What Happens When Galaxies Actually Collide?", "t": 10,
     "lines": ["GALAXIES", "COLLIDE?"], "yellow": {"GALAXIES"}, "hero": 1},
    {"id": "P9Jiw-MwUEU", "title": "Is Andromeda Coming to Destroy Us?", "t": 18,
     "lines": ["COMING", "FOR US?"], "yellow": {"COMING"}, "hero": 1},
    {"id": "U5Baf_CjhKc", "title": "Will Andromeda Fill the Entire Sky?", "t": 6,
     "lines": ["FILL THE", "SKY?"], "yellow": {"FILL"}, "hero": 1},
    {"id": "17zpT_u7XsY", "title": "Will Earth Survive the Galaxy Crash?", "t": 6,
     "lines": ["EARTH", "SURVIVE?"], "yellow": {"EARTH"}, "hero": 1},
    {"id": "QRi6Dxq0hz0", "title": "We Could Smell Alien Life in a Spectrum",
     "nasa_id": "GSFC_20171208_Archive_e001427", "nasa_file": "GSFC_20171208_Archive_e001427~orig.jpg",
     "credit": "NASA, ESA, M. Kornmesser (HD 189733b)", "crop_cx": 0.5,
     "lines": ["SMELL", "ALIEN LIFE"], "yellow": {"SMELL"}, "hero": 0},
    {"id": "ZnsJTCcrTlA", "title": "Black Holes Grew Too Big, Too Fast",
     "nasa_id": "PIA12966", "nasa_file": "PIA12966~orig.jpg",
     "credit": "NASA/JPL-Caltech (prehistoric black hole)", "crop_cx": 0.30,
     "lines": ["TOO BIG", "TOO FAST"], "yellow": {"FAST"}, "hero": 1},
    {"id": "tEOHYQbcgOw", "title": "This Planet's Night Never Cools Down",
     "nasa_id": "PIA20056", "nasa_file": "PIA20056~orig.jpg",
     "credit": "NASA/ESA/STScI (hot Jupiters)", "crop_cx": 0.12,
     "lines": ["NIGHT NEVER", "COOLS"], "yellow": {"NEVER"}, "hero": 1},
]


def plate(job: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"plate_{job['id']}.png"
    if "nasa_id" not in job:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(job["t"]),
                        "-i", str(FRAMES / f"{job['id']}.mp4"), "-frames:v", "1", str(out)], check=True)
        im = Image.open(out).convert("RGB")
        w, h = im.size
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rectangle((0, int(h * 0.36), w, int(h * 0.62)), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(40))
        Image.composite(im.filter(ImageFilter.GaussianBlur(28)), im, mask).save(out)
        return out
    src = WORK / "nasa" / job["nasa_file"].replace("~", "_")
    src.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        urllib.request.urlretrieve(f"https://images-assets.nasa.gov/image/{job['nasa_id']}/{job['nasa_file']}", src)
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    cw = min(sw, round(sh * v04.W / v04.H))
    x0 = min(max(0, round(job["crop_cx"] * sw - cw / 2)), sw - cw)
    im.crop((x0, 0, x0 + cw, sh)).save(out)
    if v04.H / sh > 2.35:
        print(f"warning: {job['id']} plate upscaled {v04.H / sh:.2f}x (house limit ~2.35x)")
    return out


def main() -> None:
    only = {x.strip() for x in os.environ.get("ONLY_IDS", "").split(",") if x.strip()}
    jobs = [j for j in JOBS if not only or j["id"] in only]
    rows = []
    for job in jobs:
        row = v04.compose(dict(job, plate=plate(job), out_dir=OUT, related="", uk="", role="j0099_crop_safe"))
        row.update(title=job["title"], source=job.get("nasa_id", f"own frame t={job.get('t')}s"),
                   credit=job.get("credit", ""))
        rows.append(row)
        print("wrote", row["file"])
    (OUT / "MANIFEST.json").write_text(json.dumps(
        {"version": "j0099_crop_safe_v01", "font": v04.FONT_PATH, "size": [v04.W, v04.H],
         "note": "9:16 covers, words in the 16:9 centre band (§2.6/§2.7). Set the cover only; video untouched.",
         "shorts": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
