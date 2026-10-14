"""Light-speed 024 Omni start frames for shot list rows 15 and 27 (J0043, Claude #99 6057323916).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 023 #39 v02 and 022 rows 67/81), only scaled.
  row 15 light clock: `starfield` code graphic frame 90 (graphics_v02, text-free) + a small code-drawn light clock
                      (two short mirrors, one light pulse) beside Orbit's right hand. No planet.
  row 27 returns:     NASA iss035e017673 (ISS night pass, Florida city lights, station hardware at left = "the ship").
                      Part of Earth only, never a whole globe.
Run with a python that has numpy, pillow and rembg:  python _composite_light_speed_orbit_starts_v01.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
POOL = HERE / "nasa_pool_v01/024_harvest_v01"
STARTS = HERE.parent / "04_Generated-Clips/01_Raw/omni_v01/starts"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import write_orbit_source_sidecar  # noqa: E402

W, H = 1280, 720
ORBIT_PX = 150


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


def cover(path: Path, box: tuple[int, int, int, int] | None = None) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def light_clock(canvas: Image.Image, cx: int, cy: int) -> Image.Image:
    """Two short pale-blue mirrors 44 px apart with one glowing pulse between them."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for y in (cy - 22, cy + 22):
        g.rounded_rectangle((cx - 16, y - 3, cx + 16, y + 3), radius=3, fill=(170, 215, 255, 255))
    g.ellipse((cx - 6, cy - 12, cx + 6, cy), fill=(255, 250, 225, 255))
    halo = glow.filter(ImageFilter.GaussianBlur(7))
    c = canvas.convert("RGBA")
    c.alpha_composite(halo)
    c.alpha_composite(halo)
    c.alpha_composite(glow)
    return c


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int) -> Image.Image:
    c = bg.convert("RGBA")
    c.alpha_composite(orb, (cx - orb.width // 2, cy - orb.height // 2))
    return c


def frame_15(orb: Image.Image) -> Image.Image:
    bg = cover(HERE / "graphics_v02/starfield/0090.png")
    c = put_orbit(bg, orb, 560, 380)
    c = light_clock(c, 560 + orb.width // 2 + 22, 405)
    return c.convert("RGB")


def frame_27(orb: Image.Image) -> Image.Image:
    bg = cover(POOL / "iss035e017673.jpg")
    return put_orbit(bg, orb, 930, 300).convert("RGB")


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    orb = orbit_rgba()
    for row, name, fn, scene, bgsrc in (
        (15, "orbit_lightclock_start_v01", frame_15,
         "deep starfield (024 starfield code graphic, frame 90); Orbit ~150px left of centre with a small glowing light clock "
         "(two short mirrors, one pulse) beside his right hand; no planet",
         "024 `starfield` code graphic (graphics_v02 frame 0090) + code-drawn light clock"),
        (27, "orbit_returns_start_v01", frame_27,
         "ISS night pass over Florida city lights (iss035e017673), station hardware at left; Orbit ~150px right of centre "
         "over dark sea above the lit coast; part of Earth only, no globe",
         "NASA iss035e017673 (public domain)"),
    ):
        out = STARTS / f"{name}.png"
        fn(orb).save(out)
        write_orbit_source_sidecar(
            out, shot=row, scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project/_composite_light_speed_orbit_starts_v01.py",
            composited="2026-10-08", request="Claude PR #99 comment 6057323916 (J0043)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
