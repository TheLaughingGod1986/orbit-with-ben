#!/usr/bin/env python3
"""Composition-lock stills for Neutron Star Part 01 v06.

Do not I2V from the full-frame Orbit identity still — that makes a hero CU
and often stamps a visor on every side. These frames already have the scale
and camera the VO beat needs.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
OUT = HERE / "parts/starts_v06"
REPO = Path("/Users/ben/code/Orbit-YouTube")
EP = REPO / "02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star"
FRONT = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
BACK_SRC = HERE / "parts/_ref_orbit_back_src.png"
SPACE_CLIP = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_01_orbit-already-hanging_cursor_v05.mp4"
REMNANT_CLIP = EP / "04_Generated-Clips/01_Raw/part-01/omni_p01_07_it-began-as-a-giant_cursor_v01.mp4"
W, H = 1920, 1080


def grab(clip: Path, t: float, dest: Path) -> Image.Image:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(t), "-i", str(clip), "-frames:v", "1", str(dest),
        ],
        check=True,
    )
    return Image.open(dest).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)


def crop_sprite(im: Image.Image, thresh: int = 28) -> Image.Image:
    arr = np.array(im.convert("RGB"))
    mx = arr.max(axis=2)
    mask = mx > thresh
    ys, xs = np.where(mask)
    if len(xs) < 50:
        raise SystemExit("sprite crop failed")
    pad = 4
    box = (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(im.width, int(xs.max()) + pad),
        min(im.height, int(ys.max()) + pad),
    )
    crop = im.convert("RGBA").crop(box)
    c = np.array(crop)
    ch = c[:, :, :3]
    keep = ch.max(axis=2) > thresh
    yy, xx = np.ogrid[: c.shape[0], : c.shape[1]]
    cy, cx = c.shape[0] / 2.0, c.shape[1] / 2.0
    ell = ((yy - cy) / (c.shape[0] * 0.50)) ** 2 + ((xx - cx) / (c.shape[1] * 0.50)) ** 2 <= 1.0
    alpha = np.where(keep & ell, 255, 0).astype(np.uint8)
    c[:, :, 3] = alpha
    return Image.fromarray(c, "RGBA")


def paste_scaled(bg: Image.Image, sprite: Image.Image, cx: int, cy: int, height_px: int) -> None:
    ratio = height_px / sprite.height
    nw, nh = max(2, int(sprite.width * ratio)), max(2, height_px)
    sp = sprite.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(sp, (int(cx - nw / 2), int(cy - nh / 2)), sp)


def hide_blob(im: Image.Image, cx: int, cy: int, r: int) -> Image.Image:
    """Cover a small Orbit with nearby empty sky so the open starfield stays photographic."""
    arr = np.array(im)
    src = arr[cy - r : cy + r, 120 : 120 + 2 * r].copy()
    if src.shape[0] != 2 * r or src.shape[1] != 2 * r:
        arr[max(0, cy - r) : cy + r, max(0, cx - r) : cx + r] = (4, 4, 8)
        return Image.fromarray(arr)
    arr[cy - r : cy + r, cx - r : cx + r] = src
    return Image.fromarray(arr)


def save(im: Image.Image, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "PNG")
    print(f"wrote {dest.name} {dest.stat().st_size}", flush=True)
    return dest


def main() -> None:
    front = crop_sprite(Image.open(FRONT))
    back = crop_sprite(Image.open(BACK_SRC), thresh=32)
    space = grab(SPACE_CLIP, 0.4, OUT / "_space_src.png")
    space = hide_blob(space, 960, 520, 70)
    remnant = grab(REMNANT_CLIP, 2.0, OUT / "_remnant_src.png")

    # 02 — the ordinary star is the subject. No Orbit.
    star = space.copy()
    save(star.crop((480, 0, 1920, 1080)).resize((W, H), Image.Resampling.LANCZOS), "02_ordinary_star.png")

    # 03 — weightless tumble, mid-frame, no destination
    bg = space.copy()
    paste_scaled(bg, front, 960, 560, 200)
    save(bg, "03_tumble_no_destination.png")

    # 04 — tidal stretch (VO-literal line of atoms)
    bg = space.copy()
    stretched = front.resize(
        (max(2, int(front.width * 0.38)), int(front.height * 1.9)),
        Image.Resampling.LANCZOS,
    )
    paste_scaled(bg, stretched, 960, 540, 460)
    save(bg, "04_tidal_line.png")

    # 05 — photon ring fills frame; Orbit is a speck in the ring
    bg = space.copy()
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    cx, cy = 960, 540
    rd.ellipse((cx - 420, cy - 420, cx + 420, cy + 420), outline=(255, 230, 170, 70), width=48)
    rd.ellipse((cx - 390, cy - 390, cx + 390, cy + 390), outline=(255, 250, 230, 160), width=16)
    bg = Image.alpha_composite(bg.convert("RGBA"), ring).convert("RGB")
    paste_scaled(bg, front, 960, 540, 34)
    save(bg, "05_photon_ring.png")

    # 06 — hold station, remnant stays small (not an approach)
    bg = space.copy()
    paste_scaled(bg, front, 760, 640, 110)
    d = ImageDraw.Draw(bg)
    d.ellipse((1160, 360, 1210, 410), fill=(230, 240, 255))
    save(bg, "06_hold_constant_distance.png")

    # 07 — visor CU, one face
    visor = front.crop((
        int(front.width * 0.10),
        int(front.height * 0.16),
        int(front.width * 0.90),
        int(front.height * 0.84),
    ))
    bg = space.copy()
    paste_scaled(bg, visor, 960, 540, 760)
    save(bg, "07_visor_cu_one_face.png")

    # 08 — living giant: recolour the leftover sphere toward a boiling yellow sun
    giant = remnant.copy()
    arr = np.array(giant).astype(np.float32)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.25 + 40, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 0.85 + 20, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.35, 0, 255)
    save(Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)), "08_living_giant.png")

    # 09 — supernova wall; tiny back-view Orbit for scale, not a corner hero
    blast = remnant.copy()
    b = np.array(blast).astype(np.float32)
    b[:, :, 0] = np.clip(b[:, :, 0] * 1.4 + 30, 0, 255)
    b[:, :, 1] = np.clip(b[:, :, 1] * 0.7, 0, 255)
    save_im = Image.fromarray(b.astype(np.uint8))
    paste_scaled(save_im, back, 960, 820, 52)
    save(save_im, "09_supernova_wall.png")

    # 10 — leftover remnant macro. No Orbit.
    save(remnant, "10_remnant_leftover.png")

    print("done", OUT)


if __name__ == "__main__":
    main()
