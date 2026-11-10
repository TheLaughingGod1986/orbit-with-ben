#!/usr/bin/env python3
"""Create unique vibrant 4s motion plates — never reused, never looped.
Used to fill picture time without repeating Seedance clips or boring starfields.
"""
from __future__ import annotations

import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/04_Generated-Clips/03_Polished/fill_plates")
W, H, FPS, DUR = 1920, 1080, 30, 4.0
SW, SH = 480, 270  # paint small, upscale

PALETTES = [
    ("teal_bio", [(8, 40, 70), (20, 160, 170), (255, 180, 60), (40, 220, 200)]),
    ("rust_dusk", [(40, 18, 12), (180, 70, 30), (255, 140, 50), (60, 90, 160)]),
    ("ice_giant", [(12, 24, 60), (80, 160, 220), (255, 140, 80), (200, 230, 255)]),
    ("observatory", [(18, 22, 40), (255, 120, 40), (40, 80, 160), (255, 220, 160)]),
    ("aurora", [(10, 20, 40), (40, 220, 120), (180, 60, 220), (80, 255, 200)]),
    ("vent_glow", [(8, 12, 30), (255, 90, 20), (40, 180, 200), (255, 200, 80)]),
    ("volcano", [(20, 8, 8), (220, 40, 20), (255, 160, 40), (60, 30, 30)]),
    ("crystal", [(20, 10, 40), (160, 80, 255), (40, 220, 255), (255, 200, 255)]),
    ("pulsar", [(8, 8, 24), (255, 220, 120), (80, 140, 255), (255, 80, 160)]),
    ("ion_trail", [(10, 16, 40), (40, 180, 255), (180, 220, 255), (255, 200, 80)]),
    ("earth_gold", [(8, 12, 28), (255, 190, 60), (40, 100, 200), (255, 240, 180)]),
    ("spectrum", [(12, 8, 28), (255, 40, 160), (40, 255, 220), (255, 200, 40)]),
    ("habitable", [(20, 40, 80), (40, 180, 200), (255, 255, 240), (80, 200, 120)]),
    ("mars_canyon", [(50, 20, 12), (200, 90, 40), (255, 170, 90), (90, 50, 30)]),
    ("geyser", [(8, 12, 28), (180, 220, 255), (255, 255, 255), (120, 160, 200)]),
    ("seti_blue", [(6, 12, 28), (40, 120, 255), (20, 200, 255), (180, 220, 255)]),
    ("wow_pulse", [(4, 6, 16), (255, 240, 200), (80, 255, 120), (255, 80, 60)]),
    ("binary_dusk", [(30, 10, 40), (255, 100, 40), (160, 60, 200), (255, 200, 80)]),
    ("microbe", [(8, 20, 30), (40, 220, 160), (200, 255, 180), (255, 220, 80)]),
    ("mirror_gold", [(12, 12, 24), (255, 200, 80), (180, 180, 220), (255, 240, 200)]),
    ("nebula_hot", [(20, 8, 40), (255, 60, 140), (40, 200, 255), (255, 180, 60)]),
    ("bio_forest", [(8, 20, 16), (40, 200, 80), (180, 255, 120), (255, 200, 40)]),
    ("comet", [(8, 10, 28), (200, 220, 255), (255, 255, 255), (120, 180, 255)]),
    ("accretion", [(8, 8, 16), (255, 180, 40), (40, 200, 180), (255, 240, 160)]),
    ("supernova", [(20, 8, 16), (255, 40, 60), (40, 120, 255), (255, 200, 100)]),
    ("invite_star", [(6, 8, 20), (255, 220, 140), (120, 160, 255), (255, 255, 220)]),
    ("amber_beacon", [(12, 8, 8), (255, 140, 20), (80, 40, 20), (255, 220, 120)]),
    ("worlds", [(10, 12, 30), (80, 200, 255), (255, 120, 80), (180, 255, 160)]),
    ("array_blink", [(8, 12, 28), (255, 220, 100), (60, 140, 255), (200, 200, 220)]),
    ("solar_arch", [(40, 16, 8), (255, 200, 40), (255, 80, 20), (255, 255, 200)]),
    ("europa_blue", [(8, 16, 40), (40, 160, 255), (200, 240, 255), (80, 200, 255)]),
    ("titan_haze", [(40, 24, 12), (220, 120, 40), (160, 80, 30), (255, 180, 80)]),
    ("magnetic", [(8, 8, 24), (120, 80, 255), (255, 80, 180), (80, 220, 255)]),
    ("aurora_ice", [(8, 16, 32), (40, 255, 160), (160, 80, 255), (200, 255, 220)]),
    ("antenna_field", [(20, 24, 40), (255, 140, 40), (60, 100, 180), (255, 220, 160)]),
    ("ring_glitter", [(10, 12, 28), (255, 220, 160), (80, 160, 255), (255, 255, 220)]),
    ("laser_green", [(8, 16, 20), (40, 255, 80), (255, 255, 200), (80, 200, 120)]),
    ("limb_aurora", [(8, 12, 40), (40, 255, 160), (255, 60, 180), (80, 160, 255)]),
    ("ice_shaft", [(8, 20, 40), (120, 200, 255), (255, 255, 255), (40, 80, 140)]),
    ("probe_blue", [(8, 12, 32), (40, 160, 255), (200, 240, 255), (255, 180, 60)]),
]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_still(seed: int, colors: list[tuple[int, int, int]]) -> Image.Image:
    rng = random.Random(seed)
    c0, c1, c2, c3 = colors
    img = Image.new("RGB", (SW, SH))
    px = img.load()
    cx, cy = SW * rng.uniform(0.3, 0.7), SH * rng.uniform(0.25, 0.7)
    for y in range(SH):
        for x in range(SW):
            dx, dy = (x - cx) / SW, (y - cy) / SH
            r = math.sqrt(dx * dx + dy * dy)
            t = min(1.0, r * 1.35)
            base = lerp(c1, c0, t)
            ribbon = 0.5 + 0.5 * math.sin((x * 0.05 + y * 0.03) + seed * 0.1)
            px[x, y] = lerp(base, c2, ribbon * 0.4 * (1 - t))

    draw = ImageDraw.Draw(img, "RGBA")
    motif = seed % 6
    if motif == 0:
        r = int(SH * rng.uniform(0.22, 0.38))
        ox, oy = int(SW * rng.uniform(0.55, 0.85)), int(SH * rng.uniform(0.45, 0.75))
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(*c2, 210))
        draw.ellipse([ox - int(r * 0.7), oy - int(r * 0.7), ox + int(r * 0.55), oy + int(r * 0.55)],
                     fill=(*c3, 90))
    elif motif == 1:
        y0 = int(SH * rng.uniform(0.55, 0.72))
        draw.rectangle([0, y0, SW, SH], fill=(*c2, 200))
        for _ in range(10):
            x = rng.randint(0, SW)
            draw.ellipse([x - 12, y0 - 8, x + 12, y0 + 14], fill=(*c3, 50))
    elif motif == 2:
        for _ in range(5):
            x0 = rng.randint(20, SW - 20)
            draw.line([(x0, SH), (x0 + rng.randint(-60, 60), 0)], fill=(*c2, 140), width=rng.randint(2, 5))
    elif motif == 3:
        for i in range(4):
            r = 50 + i * 22
            bbox = [SW // 2 - r, SH // 2 - r // 2, SW // 2 + r, SH // 2 + r]
            draw.arc(bbox, 200, 340, fill=(*c3, 180), width=2)
    elif motif == 4:
        for _ in range(90):
            x, y = rng.randint(0, SW - 1), rng.randint(0, SH - 1)
            rr = rng.randint(1, 3)
            col = c2 if rng.random() < 0.55 else c3
            draw.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*col, rng.randint(140, 230)))
    else:
        ox, oy = int(SW * 0.45), int(SH * 0.55)
        for i in range(5):
            rw, rh = 100 + i * 14, 22 + i * 4
            draw.ellipse([ox - rw, oy - rh, ox + rw, oy + rh], outline=(*c3, 120), width=2)

    for _ in range(35):
        x, y = rng.randint(0, SW - 1), rng.randint(0, SH - 1)
        draw.point((x, y), fill=c3)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return img.resize((W, H), Image.Resampling.LANCZOS)


def still_to_motion(png: Path, mp4: Path, seed: int):
    z = 1.08 + (seed % 7) * 0.015
    corners = [
        ("0", "0"),
        ("iw-iw/zoom", "0"),
        ("0", "ih-ih/zoom"),
        ("iw-iw/zoom", "ih-ih/zoom"),
        ("(iw-iw/zoom)/2", "(ih-ih/zoom)/2"),
        ("(iw-iw/zoom)*0.2", "(ih-ih/zoom)*0.6"),
        ("(iw-iw/zoom)*0.7", "(ih-ih/zoom)*0.25"),
    ]
    x, y = corners[seed % len(corners)]
    frames = int(DUR * FPS)
    vf = (
        f"zoompan=z='min(zoom+0.0009,{z})':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},"
        f"eq=saturation=1.28:contrast=1.06,format=yuv420p"
    )
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(png),
        "-vf", vf, "-t", f"{DUR}", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        str(mp4),
    ], check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for i, (name, colors) in enumerate(PALETTES, 1):
        stem = f"fill_plate_{i:03d}_{name}"
        png = OUT / f"{stem}.png"
        mp4 = OUT / f"{stem}_v01.mp4"
        if mp4.exists() and mp4.stat().st_size > 50_000:
            made.append(mp4.name)
            continue
        img = make_still(1000 + i * 17, colors)
        img.save(png, optimize=True)
        still_to_motion(png, mp4, 1000 + i)
        made.append(mp4.name)
        print("OK", mp4.name, flush=True)
    print(f"plates={len(made)} dir={OUT}")


if __name__ == "__main__":
    main()
