#!/usr/bin/env python3
"""023 Venus long thumbnails v03 (J0098; thumb audit 9 Oct, item 3, rules §2.5 and §2.8).

Only B (EARTH'S TWIN) changes: the Blue Marble Earth (NASA AS17-148-22727) beside Venus (S91-50688) at true
relative size, Venus 0.95x Earth's diameter. Both sit low so Venus's bottom data-gap notch stays below frame,
and the words run along the top on one line. That also breaks the 022/023 look of one orange ball on the right
with two words on the left. A and C are copied from abc_v02 unchanged.

  python3 _build_venus_thumbs_v03.py
"""
from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_venus_thumbs_v02 as v02  # noqa: E402

W, H = v02.W, v02.H
EARTH = HERE.parent / "07_Edit-Project" / "nasa_pool_v01" / "earth" / "as17-148-22727.jpg"
SRC_DIR = HERE / "abc_v02"
OUT = HERE / "abc_v03"

VENUS_TO_EARTH = 0.95  # equatorial diameters 12,104 km / 12,756 km
EARTH_D = 560
VENUS_D = round(EARTH_D * VENUS_TO_EARTH)
GAP = 50
NOTCH = 0.12  # share of the Venus disc kept below frame (the mosaic's data gap sits in the lowest ~11%)
CY = H + int(VENUS_D * NOTCH) - VENUS_D // 2
LEFT = (W - (EARTH_D + GAP + VENUS_D)) // 2
EARTH_CX = LEFT + EARTH_D // 2
VENUS_CX = LEFT + EARTH_D + GAP + VENUS_D // 2
TEXT_TOP = 58
MIN_GAP = 24


def earth_disc() -> Image.Image:
    im = Image.open(EARTH).convert("RGB")
    box = im.convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    side = max(box[2] - box[0], box[3] - box[1])
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    im = im.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)).resize((EARTH_D, EARTH_D), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def venus_disc() -> Image.Image:
    v02.DISC_D = VENUS_D
    return v02.disc()


def background() -> Image.Image:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ge = np.clip(1.0 - np.hypot(xx - EARTH_CX, yy - CY) / (W * 0.55), 0, 1) ** 1.6
    gv = np.clip(1.0 - np.hypot(xx - VENUS_CX, yy - CY) / (W * 0.55), 0, 1) ** 1.6
    base = (np.array([30, 22, 40], np.float32)
            + ge[..., None] * np.array([10, 40, 90], np.float32)
            + gv[..., None] * np.array([100, 38, 6], np.float32))
    img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    rng = random.Random(323)
    stars = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stars)
    for _ in range(360):
        x, y = rng.randrange(W), rng.randrange(H)
        r = 1 if rng.random() < 0.85 else 2
        sd.ellipse((x - r, y - r, x + r, y + r), fill=rng.randint(70, 210))
    stars = stars.filter(ImageFilter.GaussianBlur(0.6))
    return Image.composite(Image.new("RGB", (W, H), (255, 244, 225)), img, stars)


def disc_mask(d: int) -> Image.Image:
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((2, 2, d - 3, d - 3), fill=255)
    return m.filter(ImageFilter.GaussianBlur(1.5))


def compose() -> Image.Image:
    bg = background()
    tmp = Image.new("RGB", (W, H), v02.BLACK)
    planets = Image.new("L", (W, H), 0)
    for disc, d, cx in ((earth_disc(), EARTH_D, EARTH_CX), (venus_disc(), VENUS_D, VENUS_CX)):
        m = disc_mask(d)
        at = (cx - d // 2, CY - d // 2)
        tmp.paste(disc, at, m)
        planets.paste(m, at, m)
    rim = np.asarray(tmp.filter(ImageFilter.GaussianBlur(30)), dtype=np.float32) * 0.6
    out = 255 - (255 - np.asarray(bg, dtype=np.float32)) * (255 - rim) / 255
    out = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    return Image.composite(tmp, out, planets)


def gap_to_discs(box) -> float:
    gaps = []
    for cx, d in ((EARTH_CX, EARTH_D), (VENUS_CX, VENUS_D)):
        dx = max(box[0] - cx, 0, cx - box[2])
        dy = max(box[1] - CY, 0, CY - box[3])
        gaps.append(float(np.hypot(dx, dy)) - d / 2)
    return min(gaps)


def draw_title(img: Image.Image, words: list[str], hook: str) -> dict:
    """One centred line, each word in its own colour."""
    d = ImageDraw.Draw(img)
    size = int(H * v02.LINE_H / 0.72)
    while size > 40:
        f = v02.font(size)
        cap = d.textbbox((0, 0), "H", font=f)
        cap_h = cap[3] - cap[1]
        space = d.textlength(" ", font=f)
        widths = [v02.line_w(d, w, f) - 2 * v02.STROKE for w in words]
        total = sum(widths) + space * (len(words) - 1)
        x0 = (W - total) / 2
        y = TEXT_TOP - cap[1]
        box = (x0 - v02.STROKE, TEXT_TOP - v02.STROKE, x0 + total + v02.STROKE + 4, TEXT_TOP + cap_h + v02.STROKE + 5)
        if box[0] >= 30 and box[2] <= W - 30 and gap_to_discs(box) >= MIN_GAP:
            break
        size -= 1
    else:
        sys.exit("title cannot clear the planets")
    x = x0
    for w, ww in zip(words, widths):
        v02.draw_line(d, x + 4, y + 5, w, f, v02.BLACK)
        v02.draw_line(d, x, y, w, f, v02.YELLOW if w == hook else v02.WHITE)
        x += ww + space
    return {"font_size": f.size, "cap_px": cap_h, "cap_share": round(cap_h / H, 3),
            "min_gap_px": round(gap_to_discs(box), 1), "tracking_px": v02.TRACK}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta_v02 = json.loads((SRC_DIR / "META.json").read_text())
    meta = {"version": "v03", "job": "J0098", "brief": "audits/THUMB_AUDIT_2026-10-09/AUDIT.md item 3",
            "rules": "THUMBNAIL_AND_TITLE_RULES.md §2.5 (scale reference) and §2.8 (week-to-week look)",
            "title": meta_v02["title"], "variants": []}
    paths = []
    for key, slug, lines, hook in v02.VARIANTS:
        name = f"venus_thumb_{key}_{slug}.png"
        p = OUT / name
        if key != "B":
            shutil.copy2(SRC_DIR / name, p)
            meta["variants"].append({**next(v for v in meta_v02["variants"] if v["key"] == key),
                                     "copied_from": "abc_v02"})
        else:
            img = compose()
            info = draw_title(img, lines, hook)
            img.save(p, optimize=True)
            meta["variants"].append({
                "key": key, "text": " ".join(lines), "yellow": hook, "file": name,
                "source": "NASA AS17-148-22727 (Apollo 17 Blue Marble) + NASA S91-50688 (Magellan radar mosaic)",
                "earth_d_px": EARTH_D, "venus_d_px": VENUS_D, "venus_to_earth": round(VENUS_D / EARTH_D, 3),
                "near_black": v02.near_black(img), **info})
        paths.append(p)
    sheet = OUT / "venus_thumbs_v03_small_size_check.jpg"
    subprocess.run([sys.executable, str(v02.REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
