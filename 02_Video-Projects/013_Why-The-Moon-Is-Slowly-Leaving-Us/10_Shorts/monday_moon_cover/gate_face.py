#!/usr/bin/env python3
"""Face lock for Monday Orbit plates.

A frame passes only when one orange floater has a bounded black visor
with two separate cream eyes and dark pupils. A face that opens into the
sky (the rejected 3s black hole) fails. A melted body fails.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def orange_mask(rgb: np.ndarray) -> np.ndarray:
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    return (r > 140) & (g > 50) & (g < 210) & (b < 130) & (r > g + 15)


def frame_report(path: str) -> dict:
    rgb = np.asarray(Image.open(path).convert("RGB"))
    fh, fw = rgb.shape[:2]
    orange = orange_mask(rgb)
    out = {"file": Path(path).name, "orange": int(orange.sum()), "visor": 0, "eyes": 0, "reason": ""}
    if out["orange"] < 800:
        out["reason"] = "no orange floater"
        return out
    body_px = ndimage.binary_dilation(orange, iterations=8)
    labels, n = ndimage.label(body_px)
    sizes = ndimage.sum(body_px, labels, index=range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    share = float(sizes.max() / sizes.sum())
    body = labels == main
    ys, xs = np.where(body)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    bh, bw = y1 - y0 + 1, x1 - x0 + 1
    hw = bh / max(bw, 1)
    fill = float(body.sum()) / max(bh * bw, 1)
    out.update({"hw": round(hw, 3), "fill": round(fill, 3), "share": round(share, 3)})
    if share < 0.55:
        out["reason"] = f"orange split {share:.2f}"
        return out
    # Antenna makes a real floater taller than the sphere. A melted body still
    # fails the visor test. The rejected 3s frame is wide, not this tall.
    if hw > 1.85 or hw < 0.62:
        out["reason"] = f"blob body h/w {hw:.2f}"
        return out
    if bh < fh * 0.12 or bw < fw * 0.08:
        out["reason"] = "body too small"
        return out

    dark = (rgb[:, :, 0] < 70) & (rgb[:, :, 1] < 70) & (rgb[:, :, 2] < 80)
    near = ndimage.binary_dilation(body, iterations=max(6, fh // 120))
    dlab, dn = ndimage.label(dark)
    body_area = int(body.sum())
    cands = []
    for i in range(1, dn + 1):
        comp = dlab == i
        overlap = int((comp & near).sum())
        if overlap < 80:
            continue
        area = int(comp.sum())
        vys, vxs = np.where(comp)
        vy0, vy1 = int(vys.min()), int(vys.max())
        vx0, vx1 = int(vxs.min()), int(vxs.max())
        vh, vw = vy1 - vy0 + 1, vx1 - vx0 + 1
        frame_frac = (vh * vw) / float(fh * fw)
        cands.append((overlap, area, frame_frac, vy0, vy1, vx0, vx1))
    # The sky is one dark field. A visor that opens into it is the rejected face.
    bounded = [
        c for c in cands
        if c[2] < 0.12 and c[1] < max(body_area * 0.85, 1) and c[1] > body_area * 0.04
    ]
    if not bounded:
        out["reason"] = "black void"
        out["dark_cands"] = len(cands)
        return out
    overlap, area, frame_frac, vy0, vy1, vx0, vx1 = max(bounded, key=lambda c: c[0])
    vh, vw = vy1 - vy0 + 1, vx1 - vx0 + 1
    out["visor"] = area
    out["visor_box"] = [vy0, vy1, vx0, vx1]
    if max(vh, vw) / max(min(vh, vw), 1) > 3.2:
        out["reason"] = "visor slit"
        return out
    visor_mid_y = (vy0 + vy1) / 2
    if visor_mid_y > y0 + bh * 0.62 or visor_mid_y < y0:
        out["reason"] = "visor off the face"
        return out

    sub = rgb[vy0 : vy1 + 1, vx0 : vx1 + 1]
    cream = (
        (sub[:, :, 0] > 165)
        & (sub[:, :, 1] > 140)
        & (sub[:, :, 2] > 100)
        & (
            sub[:, :, 0].astype(np.int16) + sub[:, :, 1].astype(np.int16)
            > sub[:, :, 2].astype(np.int16) + 50
        )
    )
    clab, cn = ndimage.label(cream)
    min_area = max(36, int(vw * vh * 0.01))
    eyes = []
    for i in range(1, cn + 1):
        comp = clab == i
        eye_area = int(comp.sum())
        if eye_area < min_area or eye_area > area * 0.35:
            continue
        eys, exs = np.where(comp)
        eh = int(eys.max() - eys.min() + 1)
        ew = int(exs.max() - exs.min() + 1)
        if min(eh, ew) < 7:
            continue
        if max(eh, ew) / max(min(eh, ew), 1) > 2.4:
            continue
        pad = ndimage.binary_dilation(comp, iterations=2)
        pupil = int(((sub[:, :, 0] < 110) & pad).sum())
        if pupil < 4:
            continue
        eyes.append({"area": eye_area, "w": ew, "h": eh, "pupil": pupil, "x": round(float(exs.mean()), 1)})
    eyes.sort(key=lambda e: e["area"], reverse=True)
    out["eyes"] = len(eyes)
    out["eye_detail"] = eyes[:3]
    if len(eyes) < 2:
        out["reason"] = f"eyes {len(eyes)}"
        return out
    if abs(eyes[0]["x"] - eyes[1]["x"]) < max(10, vw * 0.08):
        out["reason"] = "eyes not side by side"
        return out
    return out


def main() -> None:
    frames = [frame_report(path) for path in sys.argv[1:]]
    reasons = [f"{row['file']}: {row['reason']}" for row in frames if row["reason"]]
    json.dump({"pass": not reasons and bool(frames), "reasons": reasons, "frames": frames}, sys.stdout)


if __name__ == "__main__":
    main()
