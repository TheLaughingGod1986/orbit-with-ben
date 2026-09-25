#!/usr/bin/env python3
"""Thumbnail phone-size preview — run on every thumb BEFORE upload (25 Sep 2026 audit).

Renders each thumb at the sizes people actually see it on a phone, next to the live
channel's current thumbs if you pass them too, and writes one sheet to eyeball:

  long (16:9)   phone search row 168×94 · phone home feed 360×202
  short (9:16)  search / channel tile 110×196 · centre 16:9 crop 168×94 (Shorts list)

The test (THUMBNAIL_AND_TITLE_RULES.md): at 168×94 every hook word is readable, the one
subject is recognisable, and nothing in the centre crop is cut off. If you have to lean
in, the text is too small or too long.

Usage
  python3 thumb_preview.py long  thumb.jpg [other.jpg ...] --out /tmp/long_preview.jpg
  python3 thumb_preview.py short thumb.jpg [other.jpg ...] --out /tmp/short_preview.jpg

Needs Pillow (pip install pillow).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

SIZES = {
    "long": [("search", (168, 94)), ("home", (360, 202))],
    "short": [("tile", (110, 196)), ("centre crop", (168, 94))],
}
GAP = 12


def render(path: Path, kind: str) -> list[Image.Image]:
    im = Image.open(path).convert("RGB")
    out = []
    for name, (w, h) in SIZES[kind]:
        if kind == "short" and name == "centre crop":
            # Shorts lists show a 16:9 slice from the middle of the 9:16 thumb.
            cw, ch = im.width, im.width * 9 // 16
            top = (im.height - ch) // 2
            out.append(im.crop((0, top, cw, top + ch)).resize((w, h), Image.LANCZOS))
        else:
            out.append(ImageOps.fit(im, (w, h), Image.LANCZOS))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=SIZES)
    ap.add_argument("thumbs", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ns = ap.parse_args()

    rows = [render(p, ns.kind) for p in ns.thumbs]
    col_w = [max(r[i].width for r in rows) for i in range(len(SIZES[ns.kind]))]
    row_h = [max(t.height for t in r) for r in rows]
    sheet = Image.new("RGB", (sum(col_w) + GAP * (len(col_w) + 1), sum(row_h) + GAP * (len(rows) + 1)), "white")
    y = GAP
    for r, h in zip(rows, row_h):
        x = GAP
        for tile, w in zip(r, col_w):
            sheet.paste(tile, (x, y))
            x += w + GAP
        y += h + GAP
    # Show it at 2× so the pixels are honest but visible on a laptop screen.
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(ns.out, quality=90)
    print(ns.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
