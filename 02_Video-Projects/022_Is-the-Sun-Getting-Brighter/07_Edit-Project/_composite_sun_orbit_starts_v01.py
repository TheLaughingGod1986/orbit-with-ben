"""Sun 022 Omni start frames for shot list rows 67 and 81 (J0012, Claude #99 6042034289).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 023 #39 v02), only scaled.
Backgrounds come from the 022 NASA pool only:
  row 67 young-Sun shore:   s04-41-1206 ocean/cloud limb + PIA21218 disc graded dim and cooler (-30%)
  row 81 brighter-Sun cloud: iss071e364425 thin bright cloud skin on the limb (solar array cropped out)
                             + PIA21218 disc graded +10% and scaled 1.04
Each disc sits part-way off the frame edge: never a whole globe as the start frame.
Run with a python that has numpy, pillow and rembg:  python _composite_sun_orbit_starts_v01.py
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


def sun_disc(diam: int, gain: float, tint: tuple[float, float, float], halo_k: float) -> Image.Image:
    src = Image.open(POOL / "S2/PIA21218.jpg").convert("L").crop((40, 25, 1490, 1475))  # disc only, no timestamp
    src = src.filter(ImageFilter.GaussianBlur(6))
    L = np.array(src.resize((diam, diam), Image.LANCZOS)).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:diam, 0:diam]
    r = np.hypot(xx - diam / 2 + 0.5, yy - diam / 2 + 0.5) / (diam / 2)
    a = np.clip((1.0 - r) * diam / 3.0, 0, 1)
    rgb = np.clip((L[..., None] / max(L.max(), 1e-3)) ** 0.6 * gain * np.array(tint, np.float32), 0, 1)
    pad = int(diam * 0.6)
    big = Image.new("RGBA", (diam + 2 * pad,) * 2, (0, 0, 0, 0))
    glow_col = tuple(int(255 * min(c * gain, 1.0)) for c in tint) + (0,)
    for blur, k in ((diam * 0.30, halo_k * 0.6), (diam * 0.07, halo_k)):
        halo = Image.new("L", big.size, 0)
        ImageDraw.Draw(halo).ellipse((pad, pad, pad + diam, pad + diam), fill=255)
        halo = halo.filter(ImageFilter.GaussianBlur(blur))
        col = Image.new("RGBA", big.size, glow_col)
        col.putalpha(halo.point(lambda p, k=k: int(p * k)))
        big.alpha_composite(col)
    disc = np.zeros((diam, diam, 4), np.float32)
    disc[..., :3] = rgb
    disc[..., 3] = a
    big.alpha_composite(Image.fromarray((disc * 255).astype(np.uint8), "RGBA"), (pad, pad))
    return big


def screen_into_sky(bg: Image.Image, layer: Image.Image, cx: int, cy: int, sky_mask: np.ndarray) -> Image.Image:
    P = max(layer.size)
    canvas = Image.new("RGBA", (W + 2 * P, H + 2 * P), (0, 0, 0, 0))
    canvas.alpha_composite(layer, (cx - layer.width // 2 + P, cy - layer.height // 2 + P))
    canvas = canvas.crop((P, P, P + W, P + H))
    c = np.array(canvas).astype(np.float32) / 255.0
    b = np.array(bg).astype(np.float32) / 255.0
    k = c[..., 3:4] * sky_mask[..., None]
    out = b * (1 - k) + c[..., :3] * k
    return Image.fromarray((out.clip(0, 1) * 255).astype(np.uint8))


def sky_mask_from(bg: Image.Image, thresh: float, soft: float) -> np.ndarray:
    lum = np.array(bg.convert("L").filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255.0
    return np.clip((thresh - lum) / soft, 0, 1)


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int) -> Image.Image:
    c = bg.convert("RGBA")
    c.alpha_composite(orb, (cx - orb.width // 2, cy - orb.height // 2))
    return c.convert("RGB")


def frame_67(orb: Image.Image) -> Image.Image:
    bg = cover(POOL / "S5/s04-41-1206.jpg", (0, 600, 5739, 3828))
    bg = Image.fromarray((np.array(bg).astype(np.float32) * 0.80).clip(0, 255).astype(np.uint8))
    sky = sky_mask_from(bg, 0.16, 0.08)
    disc = sun_disc(300, 1.15, (1.0, 0.62, 0.30), 0.55)
    bg = screen_into_sky(bg, disc, 1190, 70, sky)
    return put_orbit(bg, orb, 840, 125)


def frame_81(orb: Image.Image) -> Image.Image:
    bg = cover(POOL / "S5/iss071e364425.jpg", (0, 1200, 5300, 5504))
    sky = np.ones((H, W), np.float32)
    disc = sun_disc(round(300 * 1.04), 1.8, (1.0, 0.97, 0.88), 0.85)
    bg = screen_into_sky(bg, disc, 90, 60, sky)
    return put_orbit(bg, orb, 760, 330)


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    orb = orbit_rgba()
    for row, fn, scene, bgsrc in (
        (67, frame_67, "young-Sun shore: dim cooler Sun disc part-off top right over the s04-41-1206 ocean/cloud limb; Orbit ~150px upper left-centre",
         "NASA s04-41-1206 + NASA/SDO PIA21218"),
        (81, frame_81, "brighter Sun disc part-off top left over the iss071e364425 thin bright cloud skin; Orbit ~150px low centre-right above the limb",
         "NASA iss071e364425 + NASA/SDO PIA21218"),
    ):
        out = STARTS / f"sun_orbit_row{row}_start_v01.png"
        fn(orb).save(out)
        write_orbit_source_sidecar(
            out, shot=row, scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/022_Is-the-Sun-Getting-Brighter/07_Edit-Project/_composite_sun_orbit_starts_v01.py",
            composited="2026-10-07", request="Claude PR #99 comment 6042034289 (J0012)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
