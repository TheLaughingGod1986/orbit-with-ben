#!/usr/bin/env python3
"""Download the Saturn NASA pool (nasa_pool_v01.json) and build one contact sheet per section.

Usage: python3 fetch_nasa_pool.py [out_dir]   (default: ./nasa_pool_v01, git-ignored media)
Needs Pillow for the contact sheets; downloads work without it.
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "nasa_pool_v01")
pool = json.load(open(os.path.join(HERE, "nasa_pool_v01.json")))

for e in pool:
    d = os.path.join(OUT, e["section"])
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{e['nasa_id']}.jpg")
    if not os.path.exists(p):
        print("get", e["nasa_id"])
        urllib.request.urlretrieve(e["orig"], p)

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("downloaded; install Pillow for contact sheets")

sections = {}
for e in pool:
    sections.setdefault(e["section"], []).append(e["nasa_id"])
W, H, COLS = 320, 220, 6
for sec, ids in sections.items():
    rows = (len(ids) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * W, rows * (H + 24)), "white")
    draw = ImageDraw.Draw(sheet)
    for k, i in enumerate(ids):
        x, y = (k % COLS) * W, (k // COLS) * (H + 24)
        im = Image.open(os.path.join(OUT, sec, f"{i}.jpg")).convert("RGB")
        im.thumbnail((W - 6, H - 6))
        sheet.paste(im, (x + 3, y + 3))
        draw.text((x + 4, y + H + 4), i, fill="black")
    sheet.save(os.path.join(OUT, f"sheet_{sec}.jpg"), quality=85)
    print("sheet", sec, len(ids))
