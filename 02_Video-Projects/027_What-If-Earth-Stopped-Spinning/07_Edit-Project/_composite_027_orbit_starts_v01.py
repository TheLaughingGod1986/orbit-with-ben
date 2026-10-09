"""027 Omni start frames for SHOT_LIST rows 14 and 21 (J0077, Claude #99 6086047504: pool complete, go on to Omni).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 024 rows 15/27), only scaled.
  row 14 north pole: NASA "ICESCAPE.jpg" (Commons, public domain), cropped to the right third so the four
                     scientists on the horizon are out of frame: melt ponds, sea ice, pale overcast sky. No globe.
  row 21 hilltop:    Poly Haven "Qwantani sunset" panorama (Greg Zaal and Jarod Guest, CC0), cropped round the
                     low Sun near the horizon line (little equirectangular bend there): dry grass hilltop. No planet.
Backgrounds are fetched by curl into 04_Generated-Clips/01_Raw/omni_v01/bg/ (media, not in git):
  ICESCAPE.jpg  https://commons.wikimedia.org/wiki/File:ICESCAPE.jpg (3840 px thumb)
  qwantani.jpg  https://commons.wikimedia.org/wiki/File:Qwantani_sunset_–_Panorama_(Greg_Zaal_and_Jarod_Guest_via_Poly_Haven)_Kopie.jpg (3840 px thumb)
Run with ~/.venvs/orbit-omni/bin/python3 (numpy, pillow, rembg).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OMNI = HERE.parent / "04_Generated-Clips/01_Raw/omni_v01"
BG = OMNI / "bg"
STARTS = OMNI / "starts"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import write_orbit_source_sidecar  # noqa: E402

W, H = 1280, 720
ORBIT_PX = 170


def orbit_rgba() -> Image.Image:
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
    return o.resize((round(o.width * ORBIT_PX / o.height), ORBIT_PX), Image.LANCZOS)


def crop_frac(path: Path, x0: float, y0: float, x1: float) -> Image.Image:
    """Crop a 16:9 box starting at (x0, y0), x1 wide, as fractions of the image, then fit to W x H."""
    im = Image.open(path).convert("RGB")
    l, t = round(x0 * im.width), round(y0 * im.height)
    w = round((x1 - x0) * im.width)
    h = round(w * H / W)
    box = im.crop((l, t, l + w, t + h))
    print(f"  {path.name}: crop {w}x{h} -> {W}x{H} (scale {W / w:.2f}x)")
    return box.resize((W, H), Image.LANCZOS)


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int) -> Image.Image:
    c = bg.convert("RGBA")
    c.alpha_composite(orb, (cx - orb.width // 2, cy - orb.height // 2))
    return c.convert("RGB")


def frame_14(orb: Image.Image) -> Image.Image:
    bg = crop_frac(BG / "ICESCAPE.jpg", 0.665, 0.08, 1.0)
    return put_orbit(bg, orb, 640, 470)


def frame_21(orb: Image.Image) -> Image.Image:
    bg = crop_frac(BG / "qwantani.jpg", 0.39, 0.25, 0.81)
    return put_orbit(bg, orb, 470, 520)


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    orb = orbit_rgba()
    for row, name, fn, scene, bgsrc in (
        (14, "orbit_northpole_start_v01", frame_14,
         "Arctic sea ice with melt ponds under a pale overcast sky (NASA ICESCAPE, right third, no people); "
         "Orbit ~170px floating just above the ice, centre; no globe",
         "NASA ICESCAPE.jpg (Commons, public domain)"),
        (21, "orbit_sunset_start_v01", frame_21,
         "dry-grass hilltop with the low Sun on the horizon (Poly Haven Qwantani sunset, CC0); "
         "Orbit ~170px left of centre floating over the grass; no planet",
         "Poly Haven Qwantani sunset panorama (Greg Zaal and Jarod Guest, CC0)"),
    ):
        out = STARTS / f"{name}.png"
        fn(orb).save(out)
        write_orbit_source_sidecar(
            out, shot=row, scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/_composite_027_orbit_starts_v01.py",
            composited="2026-10-09", request="Claude PR #99 comment 6086047504 (J0077)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
