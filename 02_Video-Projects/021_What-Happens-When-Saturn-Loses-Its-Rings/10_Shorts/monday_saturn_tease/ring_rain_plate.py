#!/usr/bin/env python3
"""Monday Short opening plate: NASA Saturn photo + drawn ring rain that always lands on the planet.

Plate: PIA06193 "The Greatest Saturn Portrait ...Yet" (NASA/JPL/Space Science Institute), from the
verified pool. Ice streaks are drawn along Saturn's dipole field lines from the B ring (1.53-1.95
Saturn radii) to the southern mid-latitudes they reach (about 37-44 deg), so every streak starts on
the ring and ends on the visible disk. Nothing is drawn in open space or under the Shorts buttons.
On screen it is an illustration over a NASA photo: caption it that way and credit PIA06193.

  python3 ring_rain_plate.py --still out.png            # one frame for review
  python3 ring_rain_plate.py --frames out_dir --seconds 6 --fps 30
  ffmpeg -framerate 30 -i out_dir/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 plate.mp4
  python3 ring_rain_plate.py --still thumb.png --thumb  # 1280x720 long-thumbnail plate, planet right, brighter ice

Needs Pillow and numpy. Downloads the NASA original on first run (about 10 MB).
"""
import argparse, math, os, random, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PLATE_URL = "https://images-assets.nasa.gov/image/PIA06193/PIA06193~orig.jpg"
PLATE = os.path.join(HERE, "PIA06193_orig.jpg")   # *.jpg is git-ignored

W, H = 1080, 1920
# Measured on PIA06193 (8888 x 4544): planet centre and equatorial radius in source pixels.
SRC_CX, SRC_CY, SRC_R = 4404.0, 2321.0, 1590.0
B = -math.radians(15.4)          # ring opening; negative = camera below the ring plane, as in this photo
R = 470.0                        # planet radius on the 9:16 canvas (whole disk fits, clear of the side buttons)
CX, CY = 540.0, 1010.0           # planet centre: keeps ring + rain between 30% and 75% of the height
CAM = np.array([0.0, math.sin(B), math.cos(B)])
ICE = np.array([205.0, 228.0, 255.0])
GAIN = 1.0                       # streak brightness/width multiplier (thumbnails need more)


def project(p):
    up = p[1] * math.cos(B) - p[2] * math.sin(B)
    return CX + R * p[0], CY - R * up


def visibility(p):
    """1.0 visible, 0.35 seen through the ring plane, 0 hidden behind the planet."""
    r = float(np.linalg.norm(p))
    if r < 1.0005:
        return 1.0 if np.dot(p / r, CAM) > 0.05 else 0.0
    b, c = float(np.dot(p, CAM)), r * r - 1.0
    disc = b * b - c
    if disc > 0 and -b - math.sqrt(disc) > 0:
        return 0.0
    if p[1] * CAM[1] < 0:
        q = p + (-p[1] / CAM[1]) * CAM
        if 1.24 < math.hypot(q[0], q[2]) < 2.27:
            return 0.35
    return 1.0


def build_lines(n=140, seed=7, steps=60):
    rng = random.Random(seed)
    lines = []
    while len(lines) < n:
        L = rng.uniform(1.53, 1.95)
        phi = rng.uniform(-math.radians(36), math.radians(36))
        if abs(L * math.sin(phi)) > 0.75:
            continue
        lam_end = math.acos(math.sqrt(1 / L))
        pts = []
        for i in range(steps + 1):
            lam = -lam_end * i / steps                      # southern (visible) branch
            r = L * math.cos(lam) ** 2
            p = np.array([r * math.cos(lam) * math.sin(phi), r * math.sin(lam), r * math.cos(lam) * math.cos(phi)])
            pts.append((project(p), visibility(p)))
        lines.append({"pts": pts, "len": rng.uniform(0.25, 0.6), "phase": rng.random(),
                      "speed": rng.uniform(0.25, 0.45), "grains": [rng.random() for _ in range(8)],
                      "jit": [(rng.gauss(0, 2.5), rng.gauss(0, 2.5)) for _ in range(8)]})
    return lines


def base_plate():
    if not os.path.exists(PLATE):
        urllib.request.urlretrieve(PLATE_URL, PLATE)
    src = Image.open(PLATE).convert("RGB")
    k = R / SRC_R
    scaled = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    canvas.paste(scaled, (round(CX - SRC_CX * k), round(CY - SRC_CY * k)))
    return np.asarray(canvas, float)


def frame(base, lines, t):
    """t in seconds. Each streak is a window of grains sliding from the ring down to the planet."""
    glow, core = Image.new("L", (W, H), 0), Image.new("L", (W, H), 0)
    dg, dc = ImageDraw.Draw(glow), ImageDraw.Draw(core)
    for ln in lines:
        head = (ln["phase"] + t * ln["speed"]) % 1.0 * (1 + ln["len"])   # 0..1+len, enters from the ring
        a0, a1 = max(0.0, head - ln["len"]), min(1.0, head)
        if a1 <= a0:
            continue
        pts, n = ln["pts"], len(ln["pts"]) - 1
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            (P0, v0), (P1, v1) = pts[i], pts[i + 1]
            if t0 < a0 or t1 > a1 or not (v0 and v1):
                continue
            w = (t0 - a0) / (a1 - a0 + 1e-6)
            val = int(255 * min(v0, v1) * (0.25 + 0.75 * w))
            dg.line([P0, P1], fill=val, width=round(5 * GAIN))
            dc.line([P0, P1], fill=int(val * 0.9), width=max(1, round(GAIN)))
        for g, (jx, jy) in zip(ln["grains"], ln["jit"]):
            tt = a0 + g * (a1 - a0)
            P, v = pts[min(n, int(tt * n))]
            if v:
                x, y = P[0] + jx, P[1] + jy
                dc.ellipse([x - 0.8, y - 0.8, x + 0.8, y + 0.8], fill=int(200 * v))
    g = np.asarray(glow.filter(ImageFilter.GaussianBlur(4 * GAIN)), float) / 255 * min(0.9, 0.45 * GAIN)
    c = np.asarray(core.filter(ImageFilter.GaussianBlur(0.6 * GAIN)), float) / 255 * 0.85
    lay = np.clip(g + c, 0, 1)[..., None]
    return Image.fromarray(np.clip(base + (ICE - base) * lay, 0, 255).astype("uint8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still")
    ap.add_argument("--frames")
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--thumb", action="store_true", help="16:9 thumbnail plate: rendered at 2560x1440, saved at 1280x720")
    a = ap.parse_args()
    global W, H, R, CX, CY, GAIN
    if a.thumb:
        W, H, R, CX, CY, GAIN = 2560, 1440, 600.0, 1640.0, 760.0, 2.2   # planet right, room for text on the left
    base, lines = base_plate(), build_lines()
    if a.still:
        img = frame(base, lines, 1.3 if a.thumb else 1.0)
        if a.thumb:
            img = img.resize((1280, 720), Image.LANCZOS)
        img.save(a.still)
        print("wrote", a.still)
    if a.frames:
        os.makedirs(a.frames, exist_ok=True)
        total = int(a.seconds * a.fps)
        for i in range(total):
            frame(base, lines, i / a.fps).save(os.path.join(a.frames, f"{i:04d}.png"))
        print(f"wrote {total} frames to {a.frames}")


if __name__ == "__main__":
    main()
