#!/usr/bin/env python3
"""J0136: no-cover-text Test & Compare thumbnail B for the live Jupiter long `-jmMROGoZCM`.

A is the live "NO FLOOR?" thumb (`audits/THUMB_AUDIT_2026-10-04/jupiter_v02_final.jpg`): Cassini PIA02873
Jupiter globe and a code-drawn Galileo probe silhouette on the right, the words on the empty starfield to the
left. Its builder did not survive the 8 Oct NAS move, so B is made from A itself: every pixel of the globe,
the glow and the probe stays as it is, and only the starfield behind the words is redrawn by code:
- the smooth sky gradient comes from OpenCV's Telea fill over a star-free (median-filtered) copy of A;
- the stars come from A's own empty sky (the top-left strip), laid back in at the same density.
No image model, no generation, no spend. Same crop and grade as A.

  ~/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/build_jupiter_notext_tc_b_j0136.py
Does not upload or touch Studio.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "00_Brand/Channel-Setup/audits/THUMB_AUDIT_2026-10-04/jupiter_v02_final.jpg"
OUT = Path(os.environ.get("J0136_OUT", str(Path.home() / "_desk/notext_tc_1011/jupiter")))
TEXT_X_MAX = 560  # the words end at x 549, the glow starts at x 552
GLOBE = (903, 372, 333)  # centre x, centre y, radius of the globe disc (the glow outside it is redrawn)
STAR_STRIP = (0, 95)  # rows of empty sky above "NO"


def text_mask(img: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2], hsv[..., 1]
    fill = ((v > 200) & (s < 60)) | ((v > 170) & (s > 120) & (hsv[..., 0] > 15) & (hsv[..., 0] < 40))
    fill[:, TEXT_X_MAX:] = False
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fill.astype(np.uint8), 8)
    glyphs = np.zeros(fill.shape, np.uint8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > 300:
            glyphs[lab == i] = 255
    # outline + drop shadow around the glyphs
    mask = cv2.dilate(glyphs, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    # the drop shadow falls down and to the right
    mask = np.maximum(mask, np.roll(np.roll(mask, 14, axis=0), 10, axis=1))
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    yy, xx = np.mgrid[: mask.shape[0], : mask.shape[1]]
    cx, cy, r = GLOBE
    mask[(xx - cx) ** 2 + (yy - cy) ** 2 <= r * r] = 0
    return mask


def main() -> None:
    a = cv2.imread(str(SRC))
    h, w = a.shape[:2]
    mask = text_mask(a)

    sky = cv2.medianBlur(a, 9)
    q = 4
    small = cv2.resize(sky, (w // q, h // q), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[:h, :w]
    cx, cy, r = GLOBE
    disc = (((xx - cx) ** 2 + (yy - cy) ** 2) <= (r + 4) ** 2).astype(np.uint8) * 255
    # the disc is in the fill mask too, so the glow is filled from glow, not from the planet's dark limb
    small_mask = cv2.dilate(cv2.resize(np.maximum(mask, disc), (w // q, h // q), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
    small = cv2.inpaint(small, small_mask, 12, cv2.INPAINT_TELEA)
    small = cv2.GaussianBlur(small, (0, 0), 3)
    smooth = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)

    y0, y1 = STAR_STRIP
    strip = a[y0:y1, :TEXT_X_MAX].astype(np.int16) - cv2.medianBlur(a, 9)[y0:y1, :TEXT_X_MAX].astype(np.int16)
    strip = np.clip(strip, 0, 255)
    reps = int(np.ceil(h / (y1 - y0)))
    rng = np.random.default_rng(136)
    stars = np.concatenate([np.roll(strip, int(rng.integers(0, TEXT_X_MAX)), axis=1) for _ in range(reps)])[:h]
    stars_full = np.zeros_like(a, dtype=np.int16)
    stars_full[:, :TEXT_X_MAX] = stars

    filled = np.clip(smooth.astype(np.int16) + stars_full, 0, 255).astype(np.uint8)
    alpha = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 6)[..., None]
    b = (filled * alpha + a * (1 - alpha)).astype(np.uint8)

    OUT.mkdir(parents=True, exist_ok=True)
    out_b = OUT / "B_notext_-jmMROGoZCM.jpg"
    cv2.imwrite(str(out_b), b, [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(str(OUT / "B_mask_debug.png"), mask)
    keep = mask == 0
    rec = {
        "job": "J0136",
        "video": "-jmMROGoZCM",
        "A_source": str(SRC.relative_to(REPO)),
        "A_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "B": str(out_b),
        "B_sha256": hashlib.sha256(out_b.read_bytes()).hexdigest(),
        "size": [w, h],
        "pixels_redrawn_pct": round(100 * float((~keep).mean()), 2),
        "untouched_max_diff": int(np.abs(b.astype(int) - a.astype(int))[keep & (alpha[..., 0] < 0.001)].max()),
        "method": "Telea fill on median-filtered A + A's own top-left stars; globe, glow and probe untouched",
    }
    (OUT / "B_build.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
