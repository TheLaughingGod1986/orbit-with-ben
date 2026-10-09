"""026 Omni start frames for Orbit's two beats (J0085, Claude #99 6077058676; SHOT_LIST_v01 rows 11 and 24).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 025), only scaled.
Both are star fields with no planet in frame.
  thumb (long 11): ESO eso1629i, the sky around Alpha Centauri (bright) and Proxima (red), top band.
                   Orbit small, lower right, facing the stars.
  walk  (long 24): NASA/ESA Hubble star field GSFC_20171208_Archive_e000256. Orbit small, left of centre,
                   room to drift right.
Run with ~/.venvs/orbit-omni/bin/python (numpy, pillow, rembg).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
POOL = HERE / "pool_v01"
STARTS = HERE.parent / "04_Generated-Clips/01_Raw/omni_v01/starts"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import write_orbit_source_sidecar  # noqa: E402

W, H = 1280, 720
Image.MAX_IMAGE_PIXELS = None


def orbit_rgba(px: int) -> Image.Image:
    ref = Image.open(ORBIT_REF).convert("RGB")
    a = np.array(remove(ref, session=new_session("u2net")).split()[3]).astype(np.float32)
    m = Image.new("L", ref.size, 0)
    d = ImageDraw.Draw(m)
    d.ellipse((297, 111, 332, 146), fill=255)
    d.line([(312, 143), (310, 158), (308, 172), (306, 188), (305, 206)], fill=255, width=8)
    d.ellipse((262, 546, 390, 584), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.maximum(a, np.array(m).astype(np.float32))
    al = Image.fromarray(alpha.clip(0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    o = ref.convert("RGBA")
    o.putalpha(al)
    o = o.crop(o.getbbox())
    return o.resize((round(o.width * px / o.height), px), Image.LANCZOS)


def cover(path: Path, box: tuple[int, int, int, int] | None = None) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int) -> Image.Image:
    c = bg.convert("RGBA")
    c.alpha_composite(orb, (cx - orb.width // 2, cy - orb.height // 2))
    return c


def frame_thumb() -> Image.Image:
    bg = cover(POOL / "alphacen/eso1629i.jpg", (0, 300, 11086, 6536))
    return put_orbit(bg, orbit_rgba(170), 1010, 500).convert("RGB")


def frame_walk() -> Image.Image:
    bg = cover(POOL / "nightsky/GSFC_20171208_Archive_e000256.jpg", (0, 270, 1280, 990))
    return put_orbit(bg, orbit_rgba(150), 330, 380).convert("RGB")


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    for shot, name, fn, scene, bgsrc in (
        ("long 11", "orbit_thumb_start_v01", frame_thumb,
         "Star field around Alpha Centauri (bright blue-white) and Proxima (small red) in the upper left; Orbit "
         "~170px lower right, facing the stars; no planet",
         "ESO eso1629i (sky around Alpha Centauri and Proxima; ESO/Digitized Sky Survey 2, CC BY 4.0)"),
        ("long 24", "orbit_walk_start_v01", frame_walk,
         "Dense Hubble star field on black; Orbit ~150px left of centre with open space to the right; no planet",
         "NASA/ESA Hubble GSFC_20171208_Archive_e000256 (public domain)"),
    ):
        out = STARTS / f"{name}.png"
        fn().save(out)
        write_orbit_source_sidecar(
            out, shot=shot, scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/_composite_nearest_star_orbit_starts_v01.py",
            composited="2026-10-09", request="Claude PR #99 comment 6077058676 (J0085)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
