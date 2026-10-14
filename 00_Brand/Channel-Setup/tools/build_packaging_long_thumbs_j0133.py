#!/usr/bin/env python3
"""J0133: rebuild five back-catalogue long thumbs to THUMBNAIL_AND_TITLE_RULES.md §2.B (Packaging, 11 Oct 2026).

Top band of 2-3 words off the subject, yellow hook word, harder grade, no Orbit. No generation:
the original clean plates are gone, so 005/007 lift the live art (rollback copy) with the centre
caption inpainted out, 006 uses frame 0 of its own master (europa_v02_STUDIO_OWNER.mp4 on the NAS),
002 uses 9:48 of its own live video (3xrxdmaOwJI, the live thumb's source frame), and 019 uses
NASA/JPL-Caltech GALEX PIA15416 (Andromeda).
The subject is recomposed lower over a blurred fill of its own plate so the band sits clear of it.

Needs OpenCV: run with ~/_desk/venvs/thumbs/bin/python. Does not upload or touch Studio.
"""
from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[3]
DESK = Path.home() / "_desk/thumb_packaging_1011"
ROLLBACK = DESK / "rollback"
PLATES = DESK / "plates"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1280, 720
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BAND_H = 150
CAPTION_BOX = (420, 262, 862, 478)  # where the v04 live caption sits on all four lifted thumbs
CLONE_SHIFT = 115

JOBS = [
    {"id": "ojk-dfOpAmw", "film": "019_Andromeda-Milky-Way-Collision", "words": ["THIS", "IS", "ANDROMEDA"],
     "yellow": "ANDROMEDA", "plate": "nasa", "crop": (1400, 1610, 8000, 5322), "fg_scale": 0.84, "lift": True},
    {"id": "Yk1tLh23rko", "film": "007_What-Happens-To-Your-Body-Near-A-Neutron-Star", "words": ["CRUSHED", "FLAT"],
     "yellow": "FLAT", "plate": "live", "fg_scale": 0.76},
    {"id": "NbW5G1BpPY0", "film": "006_Could-Life-Exist-Under-The-Ice-Of-Europa", "words": ["A", "HIDDEN", "OCEAN"],
     "yellow": "OCEAN", "plate": "frame", "frame": "europa_master_t0.png", "fg_scale": 0.78, "pale": True,
     "lift": True},
    {"id": "REXYxuLOBoI", "film": "005_The-Last-Star-In-The-Universe", "words": ["LAST", "LIGHT"],
     "yellow": "LIGHT", "plate": "live", "fg_scale": 0.80, "lift": True},
    {"id": "3xrxdmaOwJI", "film": "002_What-Happens-If-You-Fall-Into-A-Black-Hole", "words": ["NO", "WAY", "OUT"],
     "yellow": "OUT", "plate": "frame", "frame": "blackhole_master_t588.png", "fg_scale": 0.78},
]


def strip_caption(path: Path, min_area: int = 1500, seam: int = 12) -> Image.Image:
    bgr = cv2.imread(str(path))
    x0, y0, x1, y1 = CAPTION_BOX
    roi = bgr[y0:y1, x0:x1].astype(int)
    b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
    yellow = (r > 190) & (g > 170) & (b < 120)
    white = (np.minimum(np.minimum(r, g), b) > 205)
    m = np.zeros(bgr.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = ((yellow | white) * 255).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = np.isin(lab, [i for i in range(1, n) if st[i, 4] > min_area]).astype(np.uint8) * 255
    # wide enough to take the black outline and drop shadow with the letters
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (37, 37)))
    # Telea/FSR leave a blotch on the subject; borrow the subject's own texture from above and
    # below the caption instead, then Poisson-blend it in so the colour matches the hole's edge
    ys, xs = np.where(m > 0)
    ty0, ty1, tx0, tx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    mid, shift, pad = (ty0 + ty1) // 2, CLONE_SHIFT, 10
    src = bgr.copy()
    src[ty0:mid] = bgr[ty0 - shift:mid - shift]
    src[mid:ty1] = bgr[mid + shift:ty1 + shift]
    k = 2 * seam + 1
    src[mid - seam:mid + seam] = cv2.GaussianBlur(src[mid - seam:mid + seam].copy(), (1, k), 0)
    bm = cv2.dilate(m, np.ones((9, 9), np.uint8))
    sl = (slice(ty0 - pad, ty1 + pad), slice(tx0 - pad, tx1 + pad))
    centre = ((tx0 + tx1) // 2, (ty0 + ty1) // 2)
    out = cv2.seamlessClone(src[sl], bgr, bm[sl], centre, cv2.NORMAL_CLONE)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((round(sw * s), round(sh * s)), Image.Resampling.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def recompose(plate: Image.Image, scale: float) -> Image.Image:
    back = cover(plate, W, H).filter(ImageFilter.GaussianBlur(22))
    back = ImageEnhance.Brightness(back).enhance(0.8)
    fw, fh = round(W * scale), round(H * scale)
    fg = plate.resize((fw, fh), Image.Resampling.LANCZOS)
    mask = Image.new("L", (fw, fh), 0)
    feather = 40
    ImageDraw.Draw(mask).rectangle((feather, feather, fw - feather, fh), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
    back.paste(fg, ((W - fw) // 2, H - fh), mask)
    return back


def grade(im: Image.Image, target: float, lift: bool) -> Image.Image:
    glow = im.filter(ImageFilter.GaussianBlur(18))
    im = Image.blend(im, Image.eval(glow, lambda v: min(255, int(v * 1.25))), 0.18)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    colour = 1.2
    out = ImageEnhance.Color(im).enhance(colour)
    while ImageStat.Stat(out.convert("HSV").getchannel("S")).mean[0] < target and colour < 2.2:
        colour += 0.1
        out = ImageEnhance.Color(im).enhance(colour)
    if lift:
        arr = np.asarray(out).astype(np.float32)
        navy = np.array([20, 28, 56], np.float32)
        arr = navy + arr * (1 - navy / 255.0)
        out = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    return out


def band(im: Image.Image, words: list[str], yellow: str) -> None:
    draw = ImageDraw.Draw(im)
    text = " ".join(words)
    size, stroke = 124, 7
    while size > 60:
        font = ImageFont.truetype(FONT, size)
        bb = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bb[2] - bb[0] <= W * 0.9 and bb[3] - bb[1] <= BAND_H - 24:
            break
        size -= 4
    space = draw.textbbox((0, 0), " ", font=font)[2]
    widths = [draw.textbbox((0, 0), w, font=font, stroke_width=stroke)[2] for w in words]
    x = (W - sum(widths) - space * (len(words) - 1)) // 2
    top = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    y = (BAND_H - (top[3] - top[1])) // 2 - top[1] + 6
    for w, ww in zip(words, widths):
        fill = YELLOW if w == yellow else WHITE
        draw.text((x + 3, y + 4), w, font=font, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0))
        draw.text((x, y), w, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
        x += ww + space


def build(job: dict) -> dict:
    if job["plate"] == "nasa":
        src = PLATES / "andromeda_PIA15416.jpg"
        plate = cover(Image.open(src).convert("RGB").crop(job["crop"]), W, H)
    elif job["plate"] == "frame":
        src = PLATES / job["frame"]
        plate = cover(Image.open(src).convert("RGB"), W, H)
    else:
        src = ROLLBACK / f"live_{job['id']}.jpg"
        plate = strip_caption(src, job.get("min_area", 1500), job.get("seam", 12))
    im = recompose(plate, job["fg_scale"])
    # top band darkened a touch so the words read at 168x94; a gradient, never a flat slab
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, 0, W, BAND_H), fill=110)
    shade = shade.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shade)
    im = grade(im, 95 if job.get("pale") else 125, job.get("lift", False))
    band(im, job["words"], job["yellow"])
    out_dir = ROOT / "02_Video-Projects" / job["film"] / "08_Thumbnail/packaging_v01"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"thumb_packaging_v01_{job['id']}.jpg"
    im.save(out, quality=93, optimize=True)
    return {"id": job["id"], "file": str(out.relative_to(ROOT)), "text": " ".join(job["words"]),
            "yellow": job["yellow"], "plate": str(src.name), "pale": bool(job.get("pale"))}


def main() -> None:
    rows = [build(j) for j in JOBS]
    for r in rows:
        print("wrote", r["file"])
    (DESK / "MANIFEST.json").write_text(json.dumps({"job": "J0133", "thumbs": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
