#!/usr/bin/env python3
"""Cut Orbit free of black/star plates → true RGBA sprites (keeps black visor)."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path("/Users/ben/code/Orbit-YouTube")
EP = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
CHAR = ROOT / "01_Orbit-Character"
OUT = EP / "04_Generated-Clips/03_Polished/orbit_narrator/rgba"
OUT.mkdir(parents=True, exist_ok=True)
CHAR_OUT = CHAR / "02_Transparent-PNGs"
CHAR_OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "curious": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_curious.png",
        CHAR / "06_Animation-Exports/Expressions/_sheet-extracts/sheet_curious_crop_v01.png",
    ],
    "surprised": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_surprised.png",
        CHAR / "06_Animation-Exports/Expressions/_sheet-extracts/sheet_surprised_crop_v01.png",
    ],
    "concerned": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_concerned.png",
        CHAR / "06_Animation-Exports/Expressions/_sheet-extracts/sheet_concerned_crop_v01.png",
    ],
    "happy": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_happy.png",
        CHAR / "06_Animation-Exports/Expressions/_sheet-extracts/sheet_happy_crop_v01.png",
    ],
    "thinking": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_thinking.png",
        CHAR / "06_Animation-Exports/Expressions/thinking/orbit_expression-thinking_frame-extract_v01.png",
    ],
    "wonder": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_expr_looking_up.png",
        CHAR / "06_Animation-Exports/Expressions/looking-up/orbit_expression-looking-up_frame-extract_v01.png",
    ],
    "neutral": [
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_float_avatar.png",
        CHAR / "06_Animation-Exports/Expressions/neutral/orbit_expression-neutral_ref_v01.png",
        EP / "04_Generated-Clips/03_Polished/orbit_narrator/orbit_avatar_rgba.png",
    ],
}


def flood_background(dark: np.ndarray) -> np.ndarray:
    """Flood from image edges through dark pixels → background mask."""
    h, w = dark.shape
    bg = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for y in range(h):
        for x in (0, w - 1):
            if dark[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if dark[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and dark[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))
    return bg


def cutout(path: Path) -> Image.Image | None:
    im = Image.open(path).convert("RGBA")
    # Work at reasonable size; huge frame extracts get cropped to orange region later
    if max(im.size) > 1600:
        im.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
    arr = np.asarray(im).copy()
    r, g, b = arr[:, :, 0].astype(np.int16), arr[:, :, 1].astype(np.int16), arr[:, :, 2].astype(np.int16)
    lum = (r.astype(np.int32) + g + b) // 3

    # Near-black / deep navy starfield = floodable background
    dark = (lum < 48) & (r < 55) & (g < 55) & (b < 70)
    bg = flood_background(dark)

    # Soft edge: pixels near bg that are still quite dark → fade
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # Slight feather
    soft = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=1.2))
    alpha = np.asarray(soft)
    # Force fully transparent where we flooded
    alpha = np.where(bg, 0, alpha)

    arr[:, :, 3] = alpha
    out = Image.fromarray(arr, "RGBA")

    # Trim to content bbox with padding
    bbox = out.split()[-1].getbbox()
    if not bbox:
        return None
    pad = 12
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(out.width, x1 + pad)
    y1 = min(out.height, y1 + pad)
    out = out.crop((x0, y0, x1, y1))

    # Reject bad cutouts (too empty / mostly transparent)
    a = np.asarray(out)[:, :, 3]
    if (a > 20).mean() < 0.05:
        return None
    return out


def pick_best(name: str, paths: list[Path]) -> Image.Image | None:
    best = None
    best_score = -1.0
    for p in paths:
        if not p.exists():
            continue
        try:
            cut = cutout(p)
        except Exception as e:
            print(f"  fail {p.name}: {e}")
            continue
        if cut is None:
            continue
        a = np.asarray(cut)[:, :, 3]
        # Prefer tighter character fills with decent resolution
        score = float((a > 40).mean() * min(cut.width, cut.height))
        print(f"  try {p.name}: {cut.size} score={score:.1f}")
        if score > best_score:
            best_score = score
            best = cut
    return best


def main() -> None:
    print(f"Writing sprites → {OUT}")
    for name, paths in SOURCES.items():
        print(f"[{name}]")
        img = pick_best(name, paths)
        if img is None:
            print(f"  SKIP — no usable source")
            continue
        # Normalize to ~900px tall for consistent overlay scaling
        target_h = 900
        if img.height != target_h:
            w = int(img.width * (target_h / img.height))
            img = img.resize((w, target_h), Image.Resampling.LANCZOS)
        dest = OUT / f"orbit_rgba_{name}.png"
        img.save(dest)
        img.save(CHAR_OUT / f"orbit_rgba_{name}.png")
        print(f"  → {dest.name} {img.size}")

    # Alias: scared uses concerned art with same cutout
    scared_src = OUT / "orbit_rgba_concerned.png"
    if scared_src.exists():
        (OUT / "orbit_rgba_scared.png").write_bytes(scared_src.read_bytes())
        (CHAR_OUT / "orbit_rgba_scared.png").write_bytes(scared_src.read_bytes())
        print("[scared] aliased from concerned")


if __name__ == "__main__":
    main()
