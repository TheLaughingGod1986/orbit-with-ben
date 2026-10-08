"""Mars 025 Omni start frames for the SHOT_LIST_v02 Omni queue (J0050, Claude #99 6060307881).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 024 rows 15/27), only scaled.
All three are ground-level NASA plates from nasa_pool_v01. Never a whole-globe Mars.
  cold  (long 13-14): PIA13804 Phoenix lander deck panorama, right half (deck + plain to horizon),
                      graded down to late dusk with low warm light from the left. Orbit on the ground left of the deck.
  wheel (long 25):    PIA17751 Curiosity left-front wheel with punctures. Orbit hovers low over the rocks, upper right.
  night (Wed S2):     PIA11132 Phoenix "Frost on Mars" plain, graded to cold pre-dawn blue. Orbit small on the ground.
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
POOL = HERE / "nasa_pool_v01"
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


def grade(im: Image.Image, gain: tuple[float, float, float], lift: float = 0.0,
          side_light: tuple[float, float, float] | None = None) -> Image.Image:
    """Per-channel gain, optional left-to-right light falloff (warm low sun at the left edge)."""
    a = np.asarray(im).astype(np.float32) / 255.0
    a = a * np.array(gain, dtype=np.float32) + lift
    if side_light is not None:
        x = np.linspace(1.0, 0.0, a.shape[1], dtype=np.float32) ** 1.6
        a = a + x[None, :, None] * np.array(side_light, dtype=np.float32)[None, None, :] * a
    return Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8))


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int, dim: float = 1.0,
              shadow: bool = False) -> Image.Image:
    c = bg.convert("RGBA")
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((cx - orb.width * 0.38, cy + orb.height * 0.47,
                                    cx + orb.width * 0.38, cy + orb.height * 0.60), fill=(0, 0, 0, 120))
        c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    o = orb
    if dim != 1.0:
        rgb = Image.fromarray((np.asarray(orb.convert("RGB")).astype(np.float32) * dim).clip(0, 255).astype(np.uint8))
        o = rgb.convert("RGBA")
        o.putalpha(orb.split()[3])
    c.alpha_composite(o, (cx - o.width // 2, cy - o.height // 2))
    return c


def smooth_sky(im: Image.Image, horizon: int, feather: int = 8) -> Image.Image:
    """Sky rows above the horizon become their row median, hiding the panorama tile seams."""
    a = np.asarray(im).astype(np.float32)
    med = np.median(a[:horizon], axis=1, keepdims=True)
    out = a.copy()
    out[:horizon] = med
    for i in range(feather):
        y = horizon - feather + i
        t = i / feather
        out[y] = med[y] * (1 - t) + a[y] * t
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def frame_cold() -> Image.Image:
    bg = cover(POOL / "phoenix/PIA13804.jpg", (12500, 0, 23487, 6180))
    bg = smooth_sky(bg, 106)
    bg = grade(bg, (0.36, 0.30, 0.28), side_light=(0.85, 0.45, 0.08))
    return put_orbit(bg, orbit_rgba(120), 205, 300, dim=0.72, shadow=True).convert("RGB")


def frame_wheel() -> Image.Image:
    bg = cover(POOL / "wheel/PIA17751.jpg", (0, 150, 1632, 1068))
    return put_orbit(bg, orbit_rgba(150), 1085, 215).convert("RGB")


def frame_night() -> Image.Image:
    bg = cover(POOL / "frost/PIA11132.jpg", (10, 40, 1014, 605))
    bg = grade(bg, (0.42, 0.47, 0.60), lift=0.02)
    return put_orbit(bg, orbit_rgba(120), 560, 470, dim=0.78, shadow=True).convert("RGB")


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    for shot, name, fn, scene, bgsrc in (
        ("long 13-14", "orbit_mars_cold_start_v01", frame_cold,
         "Phoenix lander deck and solar array on the right, flat Mars plain to the horizon, graded to late dusk with "
         "low warm light from the left (sky rows smoothed to hide panorama seams); Orbit ~120px on the ground left of the "
         "deck; ground level, no globe",
         "NASA PIA13804 (Phoenix deck panorama, right half; public domain), dusk grade"),
        ("long 25", "orbit_mars_wheel_start_v01", frame_wheel,
         "Curiosity left-front wheel close-up with punctured aluminium tread over Gale rocks; Orbit ~150px hovering "
         "low over the rocks upper right; ground level, no globe",
         "NASA PIA17751 (Curiosity left-front wheel; public domain)"),
        ("Wed 11 Nov S2", "orbit_mars_night_start_v01", frame_night,
         "Phoenix 'Frost on Mars' rocky plain to a flat horizon, graded to cold pre-dawn blue; Orbit ~120px on the "
         "ground centre; ground level, no globe",
         "NASA PIA11132 (Phoenix 'Frost on Mars'; public domain), pre-dawn grade"),
    ):
        out = STARTS / f"{name}.png"
        fn().save(out)
        write_orbit_source_sidecar(
            out, shot=shot, scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/_composite_mars_orbit_starts_v01.py",
            composited="2026-10-08", request="Claude PR #99 comment 6060307881 (J0050)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
