#!/usr/bin/env python3
"""024 light-speed long thumbnails v03 (J0098; thumb audit 9 Oct, item 2, rule §2.5: every thumb has a main
character). The film is the twin paradox, so each variant now shows a traveller.

A  7 YEARS GONE?   v01's night Earth + streak, with a small Voyager (PIA17049) at the head of the streak.
B  YOU AGE SLOWER  NASA spacewalk photo iss038e020263 (EVA 25, 24 Dec 2013), Earth's clouds behind.
                   No person is named on the thumb or in the listing.
C  ONE-WAY TRIP    NASA's Voyager illustration PIA17049 heading away from a small, distant Sun.

Text, font, tracking and the layout check come from v01. Sources live in the 024 pool
(nasa_pool_v01/024_harvest_v01; PIA17049 copied from the 026 pool).

  python3 _build_light_speed_thumbs_v03.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_light_speed_thumbs_v01 as v01  # noqa: E402

W, H = v01.W, v01.H
POOL = v01.POOL
ASTRONAUT = POOL / "iss038e020263.jpg"
VOYAGER = POOL / "PIA17049.jpg"
OUT = HERE / "abc_v03"
v01.OUT = OUT  # starfield_frame() writes its temp frame here


def voyager_layer(scale: float) -> Image.Image:
    """PIA17049 with its own star field dimmed out, so only the craft screens onto a new background."""
    im = Image.open(VOYAGER).convert("RGB")
    a = v01.arr(im)
    l = a.mean(-1)
    big = v01.arr(Image.fromarray(l.astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
    keep = np.clip((big - 40) / 40, 0, 1)  # craft and booms are wide; lone stars fade out
    keep = v01.arr(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) / 255
    out = v01.img(a * keep[..., None])
    return out.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)


def craft_box(layer: Image.Image) -> tuple[int, int, int, int]:
    return Image.fromarray((v01.arr(layer).mean(-1) > 30).astype(np.uint8) * 255).getbbox()


def sun_glow(cx: float, cy: float, r_core: float, reach: float) -> np.ndarray:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    core = np.clip((r_core * 1.3 - d) / (r_core * 0.3), 0, 1)
    halo = np.exp(-(d / reach) ** 2) * 0.85 + np.exp(-(d / (reach * 3)) ** 2) * 0.25
    warm = np.array([255, 214, 150], np.float32)
    return np.clip(core[..., None] * 255 + halo[..., None] * warm, 0, 255)


# ---- A: v01 night Earth + streak, small craft at the streak's head ---------------------
A_CRAFT_AT = (1105, 492)  # centre of the craft in thumb px; the streak's bright core sits behind it at ~1010


def variant_a(sf: Image.Image):
    base, subj = v01.variant_a(sf)
    layer = voyager_layer(0.30)
    bx = craft_box(layer)
    craft = layer.crop(bx)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    x0 = A_CRAFT_AT[0] - craft.width // 2
    y0 = A_CRAFT_AT[1] - craft.height // 2
    canvas.paste(craft, (x0, y0))
    lit = v01.arr(canvas) * 1.3
    glow = v01.arr(canvas.filter(ImageFilter.GaussianBlur(10))) * 0.8
    out = v01.img(v01.screen(v01.screen(v01.arr(base), glow), lit))
    return out, subj, {"craft_box": [x0, y0, x0 + craft.width, y0 + craft.height]}


# ---- B: spacewalker with Earth behind --------------------------------------------------
B_CROP_Y0 = 0
TEXT_SHADE = (1010, 120, 430)  # centre x, y and reach of the soft darkening behind the words


def variant_b():
    src = Image.open(ASTRONAUT).convert("RGB")
    ch = src.width * 9 // 16
    im = src.crop((0, B_CROP_Y0, src.width, B_CROP_Y0 + ch)).resize((W, H), Image.LANCZOS)
    a = v01.arr(im)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy, reach = TEXT_SHADE
    shade = np.clip(1 - np.hypot((xx - cx) / 1.4, yy - cy) / reach, 0, 1) ** 1.2
    a = a * (1 - 0.42 * shade[..., None])
    out = ImageEnhance.Contrast(v01.img(a)).enhance(1.05)
    out = ImageEnhance.Color(out).enhance(1.08).filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
    # helmet and visor (the face) in thumb px, measured on the source: centre ~(1758, 1544), radius ~860
    k = W / src.width
    return out, ("circle", 1758 * k, (1544 - B_CROP_Y0) * k, 860 * k)


# ---- C: Voyager leaving a small, distant Sun ------------------------------------------
C_SCALE = 1.0
C_SHIFT = (-170, 20)  # move the craft left so the words sit clear on the right
C_SUN = (120, 590, 9, 46)  # cx, cy, core radius, glow reach


def variant_c():
    layer = voyager_layer(C_SCALE)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(layer, C_SHIFT)
    bg = v01.glow_bg(W * 0.30, H * 0.55, W * 0.95, (10, 14, 32), (34, 52, 104), seed=343, stars=300)
    bg = v01.screen(bg, sun_glow(*C_SUN))
    a = v01.screen(bg, v01.arr(canvas))
    out = ImageEnhance.Contrast(v01.img(a)).enhance(1.04).filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=2))
    bx = craft_box(canvas)
    # the dish and bus are the subject; the thin booms may pass under the words' gap check
    body = ("circle", C_SHIFT[0] + 270 * C_SCALE * 1280 / 600, C_SHIFT[1] + 125 * C_SCALE * 720 / 337,
            80 * C_SCALE * 1280 / 600)
    return out, body, {"craft_bbox": list(bx), "sun_px": list(C_SUN[:2])}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    sf = v01.starfield_frame()
    a_img, a_subj, a_extra = variant_a(sf)
    b_img, b_subj = variant_b()
    c_img, c_subj, c_extra = variant_c()
    builds = {
        "A": (a_img, a_subj, {"x_right": W - 40, "x_left": None, "y_top": 90}, a_extra,
              "NASA GSFC Black Marble (GSFC_20171208_Archive_e001593) + starfield graphic (graphics_v03, 26.5 s) "
              "+ NASA/JPL-Caltech Voyager illustration (PIA17049)"),
        "B": (b_img, b_subj, {"x_right": W - 34, "x_left": None, "y_top": 34}, {},
              "NASA spacewalk photo (iss038e020263, EVA 25, 24 Dec 2013)"),
        "C": (c_img, c_subj, {"x_right": W - 36, "x_left": None, "y_top": 46}, c_extra,
              "NASA/JPL-Caltech Voyager illustration (PIA17049) + code-drawn distant Sun and star field"),
    }
    meta = {"version": "v03", "job": "J0098", "brief": "audits/THUMB_AUDIT_2026-10-09/AUDIT.md item 2",
            "rules": "THUMBNAIL_AND_TITLE_RULES.md §2.5 (main character) and §2.8 (week-to-week look)",
            "title": "What Happens If You Travel Near Light Speed?", "variants": []}
    paths = []
    for key, slug, lines, hook in v01.VARIANTS:
        base, subj, pos, extra, source = builds[key]
        im = base.copy()
        info = v01.place_text(im, lines, hook, subj, **pos)
        p = OUT / f"light_speed_thumb_{key}_{slug}.jpg"
        im.save(p, quality=94, optimize=True, subsampling=0)
        paths.append(p)
        meta["variants"].append({"key": key, "text": " ".join(lines), "yellow": hook, "file": p.name,
                                 "source": source, "near_black": v01.near_black(im), **info, **extra})
    sheet = OUT / "light_speed_thumbs_v03_small_size_check.jpg"
    subprocess.run([sys.executable, str(v01.REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
                    "long", *map(str, paths), "--out", str(sheet)], check=True)
    (OUT / "META.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    bad = [v["key"] for v in meta["variants"] if v["near_black"] > 0.30]
    if bad:
        print(f"near-black over 30%: {bad}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
