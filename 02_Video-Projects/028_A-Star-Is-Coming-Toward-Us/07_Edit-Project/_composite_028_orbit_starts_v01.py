#!/usr/bin/env python3
"""028 Gliese 710 Omni start frames for Orbit's two beats (J0850, Chief price PASS; SHOT_LIST_v01 rows 8 and 23).

Orbit is cut from the canonical ORBIT_REF (u2net matte + hand masks, as 026/027), only scaled.
Both are starfields with no planet in frame:
  r08_orbit_binoculars (row 8): dark hill at night under a real starfield (ngc3603 outer crop) with a smooth
                                faint warm orange point-spread star (Gliese 710) in the upper-left sky;
                                Orbit ~170px on the hill crest.
  r23_orbit_ice        (row 23): deep outer Oort Cloud starfield on black with 3D-shaded, textured dark icy
                                 cometary boulders floating; Orbit ~170px beside one dark ice lump.
Run with ~/.venvs/orbit-omni/bin/python (numpy, pillow, rembg).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import new_session, remove

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
POOL = HERE / "nasa_pool_v01/028_harvest_v01"
POOL_027 = REPO / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01"
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


def put_orbit(bg: Image.Image, orb: Image.Image, cx: int, cy: int) -> Image.Image:
    c = bg.convert("RGBA")
    c.alpha_composite(orb, (cx - orb.width // 2, cy - orb.height // 2))
    return c


def make_starfield_bg(dark_factor: float = 0.58) -> np.ndarray:
    """Real Hubble starfield crop darkened and graded so stars are crisp points on a deep night sky."""
    src = POOL / "ngc3603.jpg"
    im = Image.open(src).convert("RGB")
    im = im.crop((0, 0, im.width // 2, int(im.height * 0.45)))
    im = im.resize((W, H), Image.LANCZOS)
    arr = np.asarray(im, dtype=np.float32) / 255.0
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    arr = arr * 0.42 + luma[:, :, None] * 0.58
    arr = np.power(np.clip(arr, 0.0, 1.0), 1.70) * dark_factor
    arr[:, :, 0] = np.clip(arr[:, :, 0] + 0.032, 0.0, 1.0)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + 0.042, 0.0, 1.0)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + 0.070, 0.0, 1.0)
    return arr


def frame_binoculars() -> Image.Image:
    arr = make_starfield_bg(dark_factor=0.62)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    # Smooth astronomical PSF for the faint orange star (Gliese 710) at (340, 195)
    dx = xx - 340.0
    dy = yy - 195.0
    r2 = dx * dx + dy * dy
    psf_core = np.exp(-r2 / (2.0 * 2.2 * 2.2))
    psf_halo = 0.35 * np.exp(-r2 / (2.0 * 7.5 * 7.5))
    psf = np.clip(psf_core + psf_halo, 0.0, 1.0)
    orange_col = np.array([1.0, 0.62, 0.30], dtype=np.float32)
    arr = np.clip(arr + psf[:, :, None] * orange_col[None, None, :], 0.0, 1.0)

    # Real grassy hilltop from 027's CC0 sunset start frame lower grass band, graded to starlit night
    sunset_src = REPO / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/04_Generated-Clips/01_Raw/omni_v01/starts/orbit_sunset_start_v01.png"
    if sunset_src.exists():
        sh = Image.open(sunset_src).convert("RGB").resize((W, H), Image.LANCZOS)
        sh_arr = np.asarray(sh, dtype=np.float32) / 255.0
        # Roll horizontally so the right-side clean grass covers the whole width
        grass_tex = np.roll(sh_arr, -420, axis=1)
        grass_luma = 0.299 * grass_tex[:, :, 0] + 0.587 * grass_tex[:, :, 1] + 0.114 * grass_tex[:, :, 2]
        night_grass = np.zeros_like(grass_tex)
        night_grass[:, :, 0] = 0.04 + grass_luma * 0.14
        night_grass[:, :, 1] = 0.06 + grass_luma * 0.18
        night_grass[:, :, 2] = 0.10 + grass_luma * 0.24
    else:
        night_grass = np.full((H, W, 3), [0.06, 0.08, 0.12], dtype=np.float32)

    # Smooth hill crest peaking gently around x=760
    t_hill = (xx - 740.0) / 540.0
    y_crest = 545.0 + 44.0 * (t_hill * t_hill) + 5.0 * np.sin(xx * 0.012)
    hill_mask = np.clip((yy - y_crest) / 6.0, 0.0, 1.0)
    # Subtle starlit rim along crest and warm glow under Orbit at (760, 548)
    rim = np.exp(-((yy - y_crest) ** 2) / (2.0 * 3.0 * 3.0)) * 0.06
    orb_glow = np.exp(-(((xx - 760.0) / 55.0) ** 2 + ((yy - 552.0) / 16.0) ** 2)) * 0.22
    night_grass[:, :, 0] += rim * 0.7 + orb_glow * 1.0
    night_grass[:, :, 1] += rim * 0.8 + orb_glow * 0.58
    night_grass[:, :, 2] += rim * 1.0 + orb_glow * 0.22
    night_grass = np.clip(night_grass, 0.0, 1.0)

    comp = arr * (1.0 - hill_mask[:, :, None]) + night_grass * hill_mask[:, :, None]
    bg = Image.fromarray((comp * 255.0).astype(np.uint8))
    return put_orbit(bg, orbit_rgba(170), 760, 468).convert("RGB")


def _render_3d_ice_boulder(
    rock_tex: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Render a 3D normal-mapped, textured icy Oort Cloud cometary lump (returns rgb[H,W,3], alpha[H,W])."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - cx) / rx
    ny = (yy - cy) / ry
    ang = np.arctan2(ny, nx)

    # Irregular craggy silhouette via multi-harmonic radial perturbation
    r_mod = np.ones_like(ang)
    for k in range(2, 8):
        amp = rng.uniform(0.03, 0.09) / (k ** 0.55)
        phase = rng.uniform(0.0, 2.0 * math.pi)
        r_mod += amp * np.cos(k * ang + phase)
    r_eff = np.sqrt(nx * nx + ny * ny) / np.clip(r_mod, 0.72, 1.28)

    mask = np.clip((1.0 - r_eff) * max(rx, ry) * 0.45, 0.0, 1.0)
    nz = np.sqrt(np.clip(1.0 - r_eff * r_eff, 0.0, 1.0))

    # Extract a random patch from the real Apollo 14 boulder / Greenland ice texture for real micro-facets
    th, tw, _ = rock_tex.shape
    ox = int(rng.integers(0, max(1, tw - W)))
    oy = int(rng.integers(0, max(1, th - H)))
    patch = rock_tex[oy : oy + H, ox : ox + W, :]
    patch_luma = 0.299 * patch[:, :, 0] + 0.587 * patch[:, :, 1] + 0.114 * patch[:, :, 2]

    # Perturb 3D normals with texture gradients for craggy icy facets
    gy, gx = np.gradient(patch_luma)
    n_x = nx * 0.75 + gx * 2.8
    n_y = ny * 0.75 + gy * 2.8
    n_z = nz
    norm = np.sqrt(n_x * n_x + n_y * n_y + n_z * n_z + 1e-6)
    n_x /= norm
    n_y /= norm
    n_z /= norm

    # Distant starlight from upper-left (-0.55, -0.50, 0.67) + cool rim light
    lx, ly, lz = -0.55, -0.50, 0.67
    ndotl = np.clip(n_x * lx + n_y * ly + n_z * lz, 0.0, 1.0)
    rim = np.power(np.clip(1.0 - n_z, 0.0, 1.0), 2.2) * np.clip(-n_x * 0.6 - n_y * 0.5 + 0.4, 0.0, 1.0)
    spec = np.power(ndotl, 12.0) * (0.35 + 0.65 * patch_luma)

    # Dark slate-blue cometary ice albedo with frosty patches
    albedo = 0.55 + 0.45 * patch_luma
    shade = (0.14 + 0.42 * ndotl) * albedo + 0.22 * rim + 0.20 * spec
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    rgb[:, :, 0] = np.clip(shade * 0.78, 0.04, 0.68)
    rgb[:, :, 1] = np.clip(shade * 0.88, 0.05, 0.76)
    rgb[:, :, 2] = np.clip(shade * 1.06, 0.07, 0.88)
    return rgb, mask


def frame_ice() -> Image.Image:
    arr = make_starfield_bg(dark_factor=0.60)
    # Load real lunar boulder texture (Apollo 14 public domain) for realistic craggy ice/rock micro-relief
    boulder_src = POOL_027 / "moon/as14-67-09386.jpg"
    if boulder_src.exists():
        tex_im = Image.open(boulder_src).convert("RGB").resize((W * 2, H * 2), Image.LANCZOS)
        rock_tex = np.asarray(tex_im, dtype=np.float32) / 255.0
    else:
        rock_tex = np.full((H * 2, W * 2, 3), 0.5, dtype=np.float32)

    for cx, cy, rx, ry, seed in (
        (195.0, 180.0, 44.0, 34.0, 301),
        (1065.0, 210.0, 54.0, 40.0, 302),
        (255.0, 545.0, 60.0, 44.0, 303),
        (985.0, 535.0, 48.0, 36.0, 304),
        (825.0, 138.0, 28.0, 22.0, 305),
        # Hero ice lump next to Orbit's right hand
        (675.0, 395.0, 74.0, 56.0, 306),
    ):
        rgb, mask = _render_3d_ice_boulder(rock_tex, cx, cy, rx, ry, seed)
        arr = arr * (1.0 - mask[:, :, None]) + rgb * mask[:, :, None]

    bg = Image.fromarray((np.clip(arr, 0.0, 1.0) * 255.0).astype(np.uint8))
    return put_orbit(bg, orbit_rgba(170), 475, 390).convert("RGB")


def main() -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    for shot, name, fn, scene, bgsrc in (
        (
            8,
            "orbit_binoculars_start_v01",
            frame_binoculars,
            "Dark hilltop at night under a real starfield with a faint warm orange star (Gliese 710) upper left; "
            "Orbit ~170px standing on the hill crest; no planet in frame",
            "NASA/ESA Hubble ngc3603 outer starfield crop (public domain) + CC0 hilltop night-graded",
        ),
        (
            23,
            "orbit_ice_start_v01",
            frame_ice,
            "Deep outer Oort Cloud starfield on black with slow dark grey/slate lumps of ice floating; "
            "Orbit ~170px floating beside a dark ice lump; no planet in frame",
            "NASA/ESA Hubble ngc3603 outer starfield crop + NASA Apollo 14 boulder relief shaded as Oort Cloud ice lumps",
        ),
    ):
        out = STARTS / f"{name}.png"
        fn().save(out)
        write_orbit_source_sidecar(
            out,
            shot=shot,
            scene=scene,
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {bgsrc}",
            script="02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/_composite_028_orbit_starts_v01.py",
            composited="2026-10-22",
            request="Chief J0850 price PASS (Claude, acting Chief, 22 Oct 2026)",
        )
        print("ok", out)


if __name__ == "__main__":
    main()
