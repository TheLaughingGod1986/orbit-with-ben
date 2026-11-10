#!/usr/bin/env python3
"""Build over-the-top expressive Orbit cutouts from the clean body sprite.

Takes the solid curious RGBA body, clears the visor, paints big cartoon eyes
(+ optional reaction glyphs), then writes hard-alpha corner/pip assets.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
BODY = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba/orbit_body_master_v17.png"
OUT = ROOT / "04_Generated-Clips/03_Polished/orbit_narrator/rgba"
CORNER = OUT / "corner"
SIZED = CORNER / "sized"
PIP_H = 112  # large enough that eyes read on phone

# Emotion → eye recipe
# shape: oval | round | crescent | wink | think | scared | sad
EMOTIONS = {
    # No floating glyphs — they read as messy dotted outlines on video.
    "curious":   {"shape": "oval", "look": (0.22, -0.28), "scale": 1.05, "glyph": None},
    "wonder":    {"shape": "round", "look": (0.08, -0.32), "scale": 1.22, "glyph": None},
    "amazed":    {"shape": "round", "look": (0.0, -0.34), "scale": 1.30, "glyph": None},
    "happy":     {"shape": "crescent", "look": (0.0, 0.0), "scale": 1.08, "glyph": None},
    "playful":   {"shape": "wink", "look": (0.12, -0.12), "scale": 1.08, "glyph": None},
    "excited":   {"shape": "round", "look": (0.0, -0.18), "scale": 1.28, "glyph": None},
    "surprise":  {"shape": "round", "look": (0.0, -0.22), "scale": 1.32, "glyph": None},
    "thinking":  {"shape": "think", "look": (0.30, -0.32), "scale": 0.95, "glyph": None},
    "deep":      {"shape": "think", "look": (0.18, -0.38), "scale": 0.90, "glyph": None},
    "explain":   {"shape": "oval", "look": (0.0, 0.05), "scale": 1.02, "glyph": None},
    "concerned": {"shape": "sad", "look": (0.12, 0.20), "scale": 0.98, "glyph": None},
    "scared":    {"shape": "scared", "look": (0.0, -0.12), "scale": 1.20, "glyph": None},
    "warm":      {"shape": "crescent", "look": (0.05, -0.05), "scale": 1.10, "glyph": None},
    "invite":    {"shape": "wink", "look": (0.0, 0.0), "scale": 1.12, "glyph": None},
    "neutral":   {"shape": "oval", "look": (0.0, 0.0), "scale": 0.98, "glyph": None},
}


def harden(im: Image.Image) -> Image.Image:
    """Binary alpha — keep body/visor/glows. No erode (MinFilter was eating holes)."""
    arr = np.asarray(im.convert("RGBA")).copy()
    a = arr[:, :, 3]
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    keep = (a > 120) | ((r > 140) & (r > g + 15) & (r > b + 20)) | ((r > 200) & (g > 180) & (b > 140))
    # Keep charcoal visor + very dark panel lines inside the hull
    keep |= (a > 100) & (r < 55) & (g < 55) & (b < 65)
    arr[:, :, 3] = np.where(keep, 255, 0).astype(np.uint8)
    # Clear RGB under transparent pixels (clean premultiply)
    clear = arr[:, :, 3] == 0
    arr[:, :, 0][clear] = 0
    arr[:, :, 1][clear] = 0
    arr[:, :, 2][clear] = 0
    return Image.fromarray(arr, "RGBA")


def find_visor(arr: np.ndarray) -> tuple[int, int, int, int]:
    """BBox of the real dark visor + glowing eyes (tight, no forehead)."""
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    a = arr[:, :, 3]
    body = a > 200
    bys, bxs = np.where(body)
    if len(bxs) == 0:
        h, w = arr.shape[:2]
        return w // 4, h // 3, 3 * w // 4, 2 * h // 3
    bx0, bx1 = int(bxs.min()), int(bxs.max())
    by0, by1 = int(bys.min()), int(bys.max())
    bw, bh = bx1 - bx0, by1 - by0

    fx0 = bx0 + int(0.24 * bw)
    fx1 = bx0 + int(0.76 * bw)
    fy0 = by0 + int(0.30 * bh)
    fy1 = by0 + int(0.56 * bh)
    band = np.zeros(body.shape, dtype=bool)
    band[fy0:fy1, fx0:fx1] = True

    orange = (r > 125) & (r > g + 12) & (r > b + 20) & (g < 205)
    # Glass: dark, not orange metal
    dark = band & body & (r < 65) & (g < 65) & (b < 80) & (~orange)
    # Hot yellow/cream eye cores
    glow = band & body & (r > 175) & (g > 135) & (b < 165) & ((r.astype(np.int32) - b) > 75)

    ys_d, xs_d = np.where(dark)
    ys_g, xs_g = np.where(glow)
    if len(xs_d) < 80:
        cx = bx0 + bw // 2
        cy = by0 + int(0.42 * bh)
        vw, vh = int(0.42 * bw), int(0.26 * bh)
        return cx - vw // 2, cy - vh // 2, cx + vw // 2, cy + vh // 2

    if len(xs_g):
        xs = np.concatenate([xs_d, xs_g])
        ys = np.concatenate([ys_d, ys_g])
    else:
        xs, ys = xs_d, ys_d

    # Tight pad — stay inside the orange rim
    x0 = max(fx0, int(xs.min()) - 4)
    y0 = max(fy0, int(ys.min()) - 4)
    x1 = min(fx1, int(xs.max()) + 4)
    y1 = min(fy1 + 6, int(ys.max()) + 10)
    return x0, y0, x1, y1


def visor_mask(arr: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    """Boolean mask of pixels that must be wiped (glass + eyes), dilated slightly."""
    x0, y0, x1, y1 = box
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)
    a = arr[:, :, 3]
    h, w = a.shape
    orange = (a > 200) & (r > 125) & (r > g + 12) & (r > b + 20) & (g < 205)
    neigh = np.zeros((h, w), dtype=bool)
    neigh[max(0, y0 - 2):min(h, y1 + 4), max(0, x0 - 2):min(w, x1 + 2)] = True
    dark = neigh & (a > 40) & (r < 75) & (g < 75) & (b < 95) & (~orange)
    glow = neigh & (a > 40) & (r > 160) & (g > 120) & (b < 175) & ((r.astype(np.int32) - b) > 55) & (~orange)
    mask = dark | glow
    # Dilate 2px so eye holes and rim glow can't survive
    from PIL import ImageFilter as _IF
    mimg = Image.fromarray((mask.astype(np.uint8) * 255), "L").filter(_IF.MaxFilter(5))
    # But never paint over strong orange metal
    dilated = np.asarray(mimg) > 128
    return dilated & (~orange) & (a > 40)


def clear_visor(arr: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    """Erase original eyes/glass via pixel mask — never stamp a plate onto orange."""
    out = arr.copy()
    wipe = visor_mask(out, box)
    out[:, :, 0][wipe] = 16
    out[:, :, 1][wipe] = 18
    out[:, :, 2][wipe] = 26
    out[:, :, 3][wipe] = 255

    # Soft charcoal ellipse *clipped to the wipe hull* so eyes have a screen,
    # without rectangular bleed onto the forehead.
    x0, y0, x1, y1 = box
    vw, vh = max(1, x1 - x0), max(1, y1 - y0)
    plate = Image.new("RGBA", (vw, vh), (16, 18, 26, 255))
    emask = Image.new("L", (vw, vh), 0)
    d = ImageDraw.Draw(emask)
    d.ellipse([1, 1, vw - 2, vh - 2], fill=255)
    # Intersect ellipse with non-orange pixels only
    roi = out[y0:y1, x0:x1]
    rr = roi[:, :, 0].astype(np.int16)
    gg = roi[:, :, 1].astype(np.int16)
    bb = roi[:, :, 2].astype(np.int16)
    aa = roi[:, :, 3]
    orange = (aa > 200) & (rr > 125) & (rr > gg + 12) & (rr > bb + 20) & (gg < 205)
    e = np.array(emask, copy=True)
    e[orange] = 0
    # Also require we're inside original wipe neighborhood (darkish or already charcoal)
    allow = (aa > 40) & ((rr < 90) | ((rr < 40) & (gg < 40)))
    e = np.where(allow, e, 0).astype(np.uint8)
    base = Image.fromarray(out, "RGBA")
    base.paste(plate, (x0, y0), Image.fromarray(e, "L"))
    cleaned = np.asarray(base).copy()

    # Final pass: any remaining glow in box → charcoal
    wipe2 = visor_mask(cleaned, box)
    # Re-detect glow only (dark already charcoal)
    r = cleaned[:, :, 0].astype(np.int16)
    g = cleaned[:, :, 1].astype(np.int16)
    b = cleaned[:, :, 2].astype(np.int16)
    a = cleaned[:, :, 3]
    orange = (a > 200) & (r > 125) & (r > g + 12) & (r > b + 20) & (g < 205)
    leftover = wipe2 & (~orange) & (r > 100)
    cleaned[:, :, 0][leftover] = 16
    cleaned[:, :, 1][leftover] = 18
    cleaned[:, :, 2][leftover] = 26
    return cleaned


def draw_eye(draw: ImageDraw.ImageDraw, cx: float, cy: float, rx: float, ry: float,
             shape: str, look: tuple[float, float], pupil_scale: float = 0.38):
    lx, ly = look
    if shape == "crescent":
        # Happy ^_^ style closed smile-eyes (thick upward arcs)
        thick = max(4, int(ry * 0.55))
        for t in range(thick):
            draw.arc(
                [cx - rx, cy - ry * 0.1 + t, cx + rx, cy + ry * 1.15 + t],
                start=200, end=340, fill=(255, 245, 210, 255), width=2,
            )
        return
    if shape == "wink":
        # left open, right crescent — caller draws both; here generic open
        shape = "round"

    # eyeball
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 245, 210, 255))

    if shape == "scared":
        pr = min(rx, ry) * 0.22
        px = cx + lx * rx * 0.35
        py = cy + ly * ry * 0.35
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(20, 22, 28, 255))
        # tiny highlight
        draw.ellipse([px - pr * 0.35, py - pr * 0.55, px, py - pr * 0.1], fill=(255, 255, 255, 220))
        return

    if shape == "sad":
        # squash top, tilt by clipping
        draw.ellipse([cx - rx, cy - ry * 0.55, cx + rx, cy + ry * 1.05], fill=(18, 20, 28, 255))
        draw.ellipse([cx - rx * 0.92, cy - ry * 0.15, cx + rx * 0.92, cy + ry * 0.95],
                     fill=(255, 245, 210, 255))
        pr = min(rx, ry) * 0.34
        px = cx + lx * rx * 0.45
        py = cy + ly * ry * 0.25 + ry * 0.15
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(20, 22, 28, 255))
        return

    if shape == "think":
        # half-lidded
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 245, 210, 255))
        draw.rectangle([cx - rx - 1, cy - ry - 1, cx + rx + 1, cy - ry * 0.15], fill=(18, 20, 28, 255))
        pr = min(rx, ry) * 0.32
        px = cx + lx * rx * 0.55
        py = cy + ly * ry * 0.15 + ry * 0.2
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(20, 22, 28, 255))
        return

    # oval / round default
    if shape == "oval":
        # already oval via rx/ry
        pass
    pr = min(rx, ry) * pupil_scale
    px = cx + lx * (rx - pr * 1.1)
    py = cy + ly * (ry - pr * 1.1)
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(20, 22, 28, 255))
    # sparkle highlight for lovable look
    hr = pr * 0.35
    draw.ellipse([px - pr * 0.55, py - pr * 0.7, px - pr * 0.55 + hr, py - pr * 0.7 + hr],
                 fill=(255, 255, 255, 230))


def paint_face(base: Image.Image, emotion: str, cfg: dict) -> Image.Image:
    """Keep the rendered 3D eyes as-is.

    Previous clear+repaint stacked cartoon eyes on leftovers → ghost/four-eye look.
    Emotion variety comes from blink/talk animation, not a second eyeball layer.
    """
    _ = emotion, cfg  # reserved for future lid accents
    return harden(base.convert("RGBA"))


def crop_tight(im: Image.Image, pad: int = 10) -> Image.Image:
    a = np.asarray(im)[:, :, 3]
    ys, xs = np.where(a > 128)
    box = (max(0, xs.min() - pad), max(0, ys.min() - pad),
           min(im.width, xs.max() + 1 + pad), min(im.height, ys.max() + 1 + pad))
    return im.crop(box)


def make_pip(im: Image.Image, h: int = PIP_H) -> Image.Image:
    w = max(1, int(round(im.width * (h / im.height))))
    scaled = im.resize((w, h), Image.Resampling.LANCZOS)
    return harden(scaled)


def main() -> None:
    assert BODY.exists(), BODY
    body = harden(Image.open(BODY))
    # Prefer episode body that is full sphere — strip any leftover soft alpha
    CORNER.mkdir(parents=True, exist_ok=True)
    SIZED.mkdir(parents=True, exist_ok=True)

    print(f"body {body.size} → expressive set")
    for name, cfg in EMOTIONS.items():
        face = paint_face(body, name, cfg)
        face = crop_tight(face)
        rgba_path = OUT / f"orbit_rgba_{name}.png"
        face.save(rgba_path)
        corner = crop_tight(face, pad=8)
        corner.save(CORNER / f"orbit_corner_{name}.png")
        pip = make_pip(corner)
        pip.save(SIZED / f"orbit_pip_{name}.png")
        print(f"  {name:10s} {face.size} pip={pip.size}")

    # Aliases used by compositor
    aliases = {
        "surprised": "surprise",
    }
    for dst, src in aliases.items():
        for folder, prefix in ((OUT, "orbit_rgba_"), (CORNER, "orbit_corner_"), (SIZED, "orbit_pip_")):
            src_p = folder / f"{prefix}{src}.png"
            dst_p = folder / f"{prefix}{dst}.png"
            if src_p.exists():
                dst_p.write_bytes(src_p.read_bytes())

    # contact sheet for QC
    names = list(EMOTIONS.keys())
    thumbs = []
    for n in names:
        im = Image.open(SIZED / f"orbit_pip_{n}.png").convert("RGBA")
        bg = Image.new("RGBA", (140, 140), (12, 16, 28, 255))
        bg.paste(im, ((140 - im.width) // 2, (140 - im.height) // 2), im)
        thumbs.append(bg.convert("RGB"))
    sheet = Image.new("RGB", (140 * len(thumbs), 140), (12, 16, 28))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * 140, 0))
    qc = OUT / "orbit_expr_contact_v17.png"
    sheet.save(qc)
    print(f"QC → {qc}")


if __name__ == "__main__":
    main()
