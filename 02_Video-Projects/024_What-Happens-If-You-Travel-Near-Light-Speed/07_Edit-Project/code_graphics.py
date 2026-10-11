#!/usr/bin/env python3
"""Code-drawn graphics for the light-speed film (024). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py starfield out/   # frame 0 and the trip: stars crowd forward and turn blue as speed rises
  python3 code_graphics.py lightclock out/  # ch.2: a light clock at rest beside the same clock moving (zigzag, slower ticks)
  python3 code_graphics.py energy    out/   # ch.4: kinetic energy against speed, flat then nearly vertical near c
  python3 code_graphics.py muons     out/   # ch.2 + Fri 6 Short: a shower falls past the no-relativity decay line to the ground
  python3 code_graphics.py gpsclocks out/   # ch.1: speed slows GPS clocks, gravity speeds them, net +38 us/day (bars to scale)
  python3 code_graphics.py mapdrift  out/   # ch.1: the map dot drifting off the road without corrections
  python3 code_graphics.py gammaclocks out/ # ch.2: five clocks at 0, 0.1c, 0.9c, 0.99c, 0.9999c
  python3 code_graphics.py twinclocks out/  # ch.3/5: home clock vs ship clock at 0.99c
  python3 code_graphics.py contraction out/ # ch.3: 10 ly shrinking to ~1.41 ly in the ship's frame
  python3 code_graphics.py all       out/
  add --still to write one frame only (review); --seconds N to change length

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

v05 variants (J0129, the Chief's v04 FAIL #99 6097002634): --variant a|b|c|d gives each beat its own render: its own
seed, a continuous float camera move (no integer zoompan, so no push jitter), its own palette, and a lifted navy star
bed under the plate (v04 plates were mean ~7, near-black). Mapdrift's grid, the muons ground line and the GPS
baseline are faded so they no longer read as split-panel seams. Variant runs pipe frames straight into ffmpeg
(no PNGs on disk) and write out/<name>_<variant>.mp4.

Physics (01_Script/SOURCES.md):
  starfield  Relativistic aberration cos(t') = (cos t + b) / (1 + b cos t), azimuth unchanged; Doppler factor
             D = 1 / (g (1 - b cos t')). Stars with D > 1 shift blue, D < 1 red. Speed ramps 0.2c -> 0.99c.
  lightclock Moving clock at 0.8c (gamma 1.667): the photon's path is the diagonal, so each tick takes 1.667x longer.
  energy     E_k = (gamma - 1) m c^2, drawn from 0 to 0.995c; the dashed line is c. No numbers on the plate.
  muons      Born about 15 km up; without dilation a 2.2 us muon at ~c goes ~660 m (the faint line near the top).
             With gamma ~9 most reach the ground. Heights to scale on the plate (15 km tall column).
"""
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
CYAN = "#5fd6ff"


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, t)))


# camera: (cx, cy, zoom) at the start and end; zoom 1 = the original 16 x 9 view, < 1 pushes in
VARIANTS = {
    "a": dict(seed=101, gold="#ffc94a", cyan="#5fd6ff", cam=((0.0, 0.0, 1.06), (0.35, 0.15, 0.86))),
    "b": dict(seed=202, gold="#ffa64d", cyan="#6ff0c0", cam=((-0.5, 0.1, 0.95), (0.5, -0.1, 0.95))),
    "c": dict(seed=303, gold="#ffe27a", cyan="#a3a9ff", cam=((0.25, -0.2, 0.84), (0.0, 0.0, 1.06))),
    "d": dict(seed=404, gold="#ff9f8a", cyan="#7cc8ff", cam=((0.4, 0.2, 1.02), (-0.3, -0.15, 0.88))),
    "e": dict(seed=505, gold="#ffd36b", cyan="#7fe3ff", cam=((-0.3, -0.2, 0.88), (0.45, 0.2, 1.04))),
    "f": dict(seed=606, gold="#ffb870", cyan="#9cf5d4", cam=((0.5, -0.1, 1.0), (-0.45, 0.15, 0.9))),
    "g": dict(seed=707, gold="#fff09a", cyan="#b7a3ff", cam=((0.0, 0.3, 0.92), (0.2, -0.25, 1.06))),
    "h": dict(seed=808, gold="#ffab9a", cyan="#8ab8ff", cam=((-0.45, 0.1, 1.05), (0.3, -0.1, 0.87))),
}
# bed star count per plate: thin-line plates get fewer, so the stars don't read as grain over the element
BED_STARS = dict(lightclock=700, energy=1600)
# tightest zoom per plate, so its key elements (outer clocks, the muon birth line, GPS bars) stay in frame
ZMIN = dict(starfield=0.7, lightclock=0.86, energy=0.9, muons=0.99, gpsclocks=0.97, mapdrift=0.8, gammaclocks=0.98,
            twinclocks=0.8, contraction=0.92)
STYLE = dict(on=False, name="", cam=((0, 0, 1), (0, 0, 1)), bed=None, stars=None)
BED_EXT = (-11.0, 11.0, -6.5, 6.5)


def make_bed(seed, stars=True, N=2600):
    """Lifted navy bed: a radial gradient with soft cloud texture and fixed background stars (mean luma ~40)."""
    from PIL import Image, ImageFilter
    rng = np.random.default_rng(seed)
    h, w = 650, 1100
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w * 0.55) / (w * 0.6), (yy - h * 0.45) / (h * 0.6))
    g = np.clip(1 - r, 0, 1) ** 1.3
    cloud = Image.fromarray((rng.random((26, 44)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    cloud = np.asarray(cloud.filter(ImageFilter.GaussianBlur(18)), dtype=float) / 255
    k = 0.5 * g + 0.65 * cloud * (0.5 + 0.5 * g)
    edge, centre = np.array([0.05, 0.07, 0.16]), np.array([0.23, 0.33, 0.60])
    img = edge + (centre - edge) * k[..., None]
    st = None
    if stars:
        st = dict(x=rng.uniform(BED_EXT[0], BED_EXT[1], N), y=rng.uniform(BED_EXT[2], BED_EXT[3], N),
                  s=1.0 + 9 * rng.uniform(0, 1, N) ** 4, a=rng.uniform(0.35, 0.9, N))
    return np.clip(img, 0, 1), st


def view(p):
    (x0, y0, z0), (x1, y1, z1) = STYLE["cam"]
    e = ease(p)
    z = max(z0 + (z1 - z0) * e, ZMIN.get(STYLE["name"], 0.8))
    m = z - ZMIN.get(STYLE["name"], 0.8) + 0.04
    cx = float(np.clip(x0 + (x1 - x0) * e, -8 * m, 8 * m))
    cy = float(np.clip(y0 + (y1 - y0) * e, -4.5 * m, 4.5 * m))
    return cx, cy, z


def canvas(p=0.0):
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    cx, cy, z = (0.0, 0.0, 1.0)
    if STYLE["on"]:
        cx, cy, z = view(p)
        ax.imshow(STYLE["bed"], extent=BED_EXT, origin="lower", interpolation="bilinear", zorder=-10)
        st = STYLE["stars"]
        if st is not None:
            rgba = np.column_stack([np.full_like(st["a"], 0.92), np.full_like(st["a"], 0.94), np.ones_like(st["a"]), st["a"]])
            ax.scatter(st["x"], st["y"], s=st["s"], c=rgba, lw=0, zorder=-9)
    ax.set_xlim(cx - 8 * z, cx + 8 * z)
    ax.set_ylim(cy - 4.5 * z, cy + 4.5 * z)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def doppler_colour(D):
    """Blend white towards blue for D > 1 and towards red for D < 1 (log scale, capped)."""
    k = np.clip(np.log(D) / np.log(4.0), -1, 1)
    white = np.array([0.96, 0.94, 0.90])
    blue = np.array([0.45, 0.70, 1.0])
    red = np.array([1.0, 0.45, 0.30])
    out = np.where(k[:, None] >= 0, white + (blue - white) * k[:, None], white + (red - white) * (-k[:, None]))
    return np.clip(out, 0, 1)


def render_starfield(out, seconds, still):
    rng = np.random.default_rng(STYLE.get("seed", 24))
    n = int(seconds * FPS)
    N = 6000
    v = rng.normal(size=(N, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    th = np.arccos(v[:, 2])                          # angle from the direction of travel (+z)
    ph = np.arctan2(v[:, 1], v[:, 0])
    mag = rng.uniform(0.2, 1.0, N) ** 3              # few bright, many faint
    f = 7.0 / math.tan(math.radians(55))             # pinhole: half-width 8 units at 55 degrees off-axis
    frames = [int(n * 0.6)] if still else range(n)
    for i in frames:
        b = 0.2 + 0.79 * ease(i / max(1, n - 1))
        g = 1 / math.sqrt(1 - b * b)
        c = np.cos(th)
        cp = (c + b) / (1 + b * c)
        thp = np.arccos(np.clip(cp, -1, 1))
        D = 1 / (g * (1 - b * cp))
        front = thp < math.radians(80)
        r = f * np.tan(thp[front])
        x, y = r * np.cos(ph[front]), r * np.sin(ph[front])
        s = 1.5 + 13 * mag[front] * np.clip(D[front], 0.3, 3) ** 1.2
        fig, ax = canvas(i / max(1, n - 1))
        vis = (np.abs(x) < 8.3) & (np.abs(y) < 4.8)
        ax.scatter(x[vis], y[vis], s=s[vis], c=doppler_colour(D[front][vis]), lw=0, alpha=0.95)
        save(fig, out, i, still)
    finish(out, still)


def render_lightclock(out, seconds, still):
    n = int(seconds * FPS)
    b = 0.8
    g = 1 / math.sqrt(1 - b * b)
    Hgap = 3.0                                       # mirror separation (canvas units)
    tick = 1.0                                       # seconds per rest tick
    vx = b * Hgap / tick                             # moving clock speed in canvas units/s, scaled so c = Hgap/tick
    frames = [int(n * 0.55)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(i / max(1, n - 1))
        # rest clock (left)
        X0 = -5.0
        ph = (t / tick) % 2
        yy = -1.5 + Hgap * (ph if ph <= 1 else 2 - ph)
        for yM in (-1.5, 1.5):
            ax.plot([X0 - 0.8, X0 + 0.8], [yM, yM], color=WHITE, lw=10, solid_capstyle="round")
        ax.add_patch(Circle((X0, yy), 0.24, color=GOLD, zorder=5))
        ax.add_patch(Circle((X0, yy), 0.70, color=GOLD, alpha=0.22, lw=0))
        # moving clock (right half): wraps across x in [-1, 8]
        span = 9.0
        x_c = -1.0 + (vx * t) % span
        ph2 = (t / (tick * g)) % 2
        y2 = -1.5 + Hgap * (ph2 if ph2 <= 1 else 2 - ph2)
        for yM in (-1.5, 1.5):
            ax.plot([x_c - 0.8, x_c + 0.8], [yM, yM], color=WHITE, lw=10, solid_capstyle="round")
        # the zigzag trail of the photon over the last tick (one mirror-to-mirror trip)
        ts = np.linspace(max(0, t - tick * g), t, 80)
        xs = -1.0 + (vx * ts) % span
        p = (ts / (tick * g)) % 2
        ys = -1.5 + Hgap * np.where(p <= 1, p, 2 - p)
        breaks = np.where(np.diff(xs) < 0)[0]
        for seg in np.split(np.arange(len(ts)), breaks + 1):
            ax.plot(xs[seg], ys[seg], color=GOLD, lw=5, alpha=0.7)
        ax.add_patch(Circle((x_c, y2), 0.24, color=GOLD, zorder=5))
        ax.add_patch(Circle((x_c, y2), 0.70, color=GOLD, alpha=0.22, lw=0))
        if not STYLE["on"]:
            ax.plot([-1.6, -1.6], [-3.6, 3.6], color=DIM, lw=1.2, alpha=0.4)
        save(fig, out, i, still)
    finish(out, still)


def render_energy(out, seconds, still):
    n = int(seconds * FPS)
    vmax = 0.995
    vv = np.linspace(0, vmax, 1200)
    E = 1 / np.sqrt(1 - vv ** 2) - 1
    X0, X1, Y0, Y1 = -6.5, 6.0, -3.6, 3.8
    xs = X0 + (X1 - X0) * vv
    ys = Y0 + (Y1 - Y0) * E / E.max()
    frames = [int(n * 0.85)] if still else range(n)
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.05) / 0.85)
        k = max(2, int(len(vv) * s))
        fig, ax = canvas(i / max(1, n - 1))
        on = STYLE["on"]
        ax.plot([X0, X1 + 0.6], [Y0, Y0], color=DIM, lw=4 if on else 2, alpha=0.7 if on else 1)
        if not on:                                   # a full-height axis reads as a split-panel seam on the v05 bed
            ax.plot([X0, X0], [Y0, Y1 + 0.4], color=DIM, lw=2)
        ax.plot([X0 + (X1 - X0) * 1.0] * 2, [Y0, Y1 + 0.4], color=WHITE, lw=3 if on else 2, ls=(0, (6, 6)), alpha=0.7)
        if on:
            ax.plot(xs[:k], ys[:k], color=GOLD, lw=24, alpha=0.18, solid_capstyle="round")
        ax.plot(xs[:k], ys[:k], color=GOLD, lw=10 if on else 4, solid_capstyle="round")
        ax.add_patch(Circle((xs[k - 1], ys[k - 1]), 0.24 if on else 0.14, color=WHITE, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_muons(out, seconds, still):
    rng = np.random.default_rng(STYLE.get("seed", 1963))
    n = int(seconds * FPS)
    TOP, GROUND = 4.2, -3.8                          # 15 km column
    km = (TOP - GROUND) / 15.0
    classical = TOP - 0.66 * km                      # ~660 m below birth height
    speed = (TOP - GROUND) / (1.6 * FPS)             # each muon crosses in ~1.6 s on screen
    mu = []                                          # [x, y, dx, born_frame]
    frames = [int(n * 0.6)] if still else range(n)
    target = set(frames)
    for i in range(n):
        for _ in range(rng.poisson(1.6)):
            ang = rng.normal(0, 0.12)
            mu.append([rng.uniform(-6.5, 6.5), TOP, speed * math.sin(ang), i])
        nxt = []
        for m in mu:
            m[0] += m[2]
            m[1] -= speed
            if m[1] > GROUND:
                nxt.append(m)
        mu = nxt
        if i not in target:
            continue
        fig, ax = canvas(i / max(1, n - 1))
        on = STYLE["on"]
        if on:                                       # soft ground haze and a dotted birth line: no straight seams
            haze = np.zeros((64, 1, 4)); haze[..., :3] = (0.09, 0.13, 0.16); haze[:, 0, 3] = np.linspace(0.5, 0, 64) ** 1.5
            ax.imshow(haze, extent=(-12, 12, -8, GROUND + 1.2), origin="lower", aspect="auto", interpolation="bilinear", zorder=-8)
            ax.set_aspect("equal")
            ax.plot([-8, 8], [TOP, TOP], color="#9f8cff", lw=2.5, alpha=0.6, ls=(0, (1, 5)))
        else:
            ax.add_patch(Rectangle((-12, -8), 24, GROUND + 8, color="#16202a", lw=0))
            ax.plot([-12, 12], [GROUND, GROUND], color=DIM, lw=2)
            ax.plot([-8, 8], [TOP, TOP], color="#9f8cff", lw=1.5, alpha=0.5)
        ax.plot([-8, 8], [classical, classical], color=WHITE, lw=1.2, ls=(0, (4, 6)), alpha=0.45)
        for m in mu:
            ax.plot([m[0] - m[2] * 10, m[0]], [m[1] + speed * 10, m[1]], color=CYAN, lw=2.2, alpha=0.75)
            ax.add_patch(Circle((m[0], m[1]), 0.06, color=WHITE, lw=0))
        save(fig, out, i, still)
    finish(out, still)


def dial(ax, cx, cy, r, angle, col, alpha=1.0):
    """A plain clock face: ring, 12 ticks, one hand at `angle` (radians, 0 = 12 o'clock, clockwise)."""
    ax.add_patch(Circle((cx, cy), r, fill=False, ec=col, lw=4, alpha=alpha))
    for k in range(12):
        a = 2 * math.pi * k / 12
        ax.plot([cx + 0.82 * r * math.sin(a), cx + 0.95 * r * math.sin(a)],
                [cy + 0.82 * r * math.cos(a), cy + 0.95 * r * math.cos(a)], color=col, lw=2, alpha=alpha)
    ax.plot([cx, cx + 0.78 * r * math.sin(angle)], [cy, cy + 0.78 * r * math.cos(angle)], color=col, lw=5,
            alpha=alpha, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 0.08 * r, color=col, alpha=alpha))


def render_gpsclocks(out, seconds, still):
    """GPS: a satellite circles Earth's limb; bars show the speed effect (-7.2 us/day, down, blue), the gravity
    effect (+45.9, up, gold) and the net (+38.7, white). Bars drawn to scale, one after another. Text-free."""
    n = int(seconds * FPS)
    frames = [int(n * 0.9)] if still else range(n)
    scale = 3.2 / 45.9
    for i in frames:
        s = i / max(1, n - 1)
        fig, ax = canvas(i / max(1, n - 1))
        ax.add_patch(Circle((-4.5, -9.0), 7.2, color="#1d4f8f", lw=0))
        a = math.radians(100 - 40 * s)
        R = 8.6
        sx, sy = -4.5 + R * math.cos(a), -9.0 + R * math.sin(a)
        ax.add_patch(Rectangle((sx - 0.25, sy - 0.15), 0.5, 0.3, color=WHITE, lw=0))
        ax.plot([sx - 0.9, sx + 0.9], [sy, sy], color=GOLD, lw=6)
        base = 0.0
        for k, (val, col, x) in enumerate(((-7.2, CYAN, 3.0), (45.9, GOLD, 4.6), (38.7, WHITE, 6.2))):
            g = ease((s - 0.15 - 0.22 * k) / 0.2)
            h = val * scale * g
            ax.add_patch(Rectangle((x - 0.45, base if h >= 0 else base + h), 0.9, abs(h), color=col, lw=0))
        ax.plot([2.2, 7.0], [base, base], color=DIM, lw=1.2 if STYLE["on"] else 2, alpha=0.45 if STYLE["on"] else 1)
        save(fig, out, i, still)
    finish(out, still)


def render_mapdrift(out, seconds, still):
    """A text-free street grid. A ring marks where you really are; the position dot drifts away about 10 km a day
    (sped up), leaving a trail. Shows what uncorrected GPS clocks would do."""
    n = int(seconds * FPS)
    frames = [int(n * 0.8)] if still else range(n)
    roads = None
    if STYLE["on"]:
        # curved, lit roads as scattered dots: any straight full-frame line (v04's grid, v05's faded grid) reads
        # as a split-panel seam in polish_gate
        rng = np.random.default_rng(STYLE.get("seed", 24) + 7)
        xs, ys = [], []
        for k in range(14):
            t = rng.uniform(0, 1, 260)
            if k % 2:
                y0, amp, ph, fq = rng.uniform(-6.2, 6.2), rng.uniform(0.4, 1.4), rng.uniform(0, 6.3), rng.uniform(0.25, 0.6)
                x = -11.2 + 22.4 * t
                y = y0 + amp * np.sin(fq * x + ph)
            else:
                x0, amp, ph, fq = rng.uniform(-10.5, 10.5), rng.uniform(0.4, 1.4), rng.uniform(0, 6.3), rng.uniform(0.3, 0.7)
                y = -6.5 + 13 * t
                x = x0 + amp * np.sin(fq * y + ph)
            xs.append(x + rng.normal(0, 0.05, t.size)); ys.append(y + rng.normal(0, 0.05, t.size))
        sx, sy = rng.uniform(-11, 11, 900), rng.uniform(-6.4, 6.4, 900)
        roads = dict(x=np.concatenate(xs + [sx]), y=np.concatenate(ys + [sy]),
                     s=np.concatenate([rng.uniform(2, 9, 14 * 260), rng.uniform(1, 4, 900)]),
                     a=np.concatenate([rng.uniform(0.45, 0.85, 14 * 260), rng.uniform(0.2, 0.5, 900)]))
    for i in frames:
        s = ease(i / max(1, n - 1))
        fig, ax = canvas(i / max(1, n - 1))
        if roads is not None:
            rgba = np.column_stack([np.full_like(roads["a"], 1.0), np.full_like(roads["a"], 0.80),
                                    np.full_like(roads["a"], 0.52), roads["a"]])
            ax.scatter(roads["x"], roads["y"], s=roads["s"], c=rgba, lw=0, zorder=1)
        else:
            for x in np.arange(-8, 8.1, 1.6):
                ax.plot([x, x], [-4.5, 4.5], color="#2a3140", lw=6)
            for y in np.arange(-4.5, 4.6, 1.5):
                ax.plot([-8, 8], [y, y], color="#2a3140", lw=6)
        ax.add_patch(Circle((-3.2, -1.5), 0.45, fill=False, ec=WHITE, lw=3))
        ts = np.linspace(0, s, 60)
        px, py = -3.2 + 8.5 * ts, -1.5 + 4.2 * ts ** 1.2
        ax.plot(px, py, color=CYAN, lw=3, alpha=0.5)
        ax.add_patch(Circle((px[-1], py[-1]), 0.22, color=CYAN, zorder=5))
        ax.add_patch(Circle((px[-1], py[-1]), 0.5, color=CYAN, alpha=0.2, lw=0, zorder=4))
        save(fig, out, i, still)
    finish(out, still)


def render_gammaclocks(out, seconds, still):
    """Five identical clocks for 0, 0.1c, 0.9c, 0.99c and 0.9999c: hands turn at 1/gamma of the first. Each clock
    lights in turn (one per VO line). Text-free."""
    n = int(seconds * FPS)
    vs = [0.0, 0.1, 0.9, 0.99, 0.9999]
    rates = [math.sqrt(1 - v * v) for v in vs]
    frames = [int(n * 0.95)] if still else range(n)
    for i in frames:
        t = i / FPS
        s = i / max(1, n - 1)
        fig, ax = canvas(i / max(1, n - 1))
        for k, rate in enumerate(rates):
            lit = ease((s - k * 0.17) / 0.1) if k else 1.0
            cx = -6.0 + k * 3.0
            col = WHITE if k == 0 else GOLD
            dial(ax, cx, 0, 1.35 if STYLE["on"] else 1.15, 2 * math.pi * 0.5 * t * rate, col, alpha=0.25 + 0.75 * lit)
        save(fig, out, i, still)
    finish(out, still)


def render_twinclocks(out, seconds, still):
    """Home (blue, left) and ship (gold, right) clocks start together; at 0.99c the home hand runs 7.09x faster.
    Text-free."""
    n = int(seconds * FPS)
    g = 7.0888
    frames = [int(n * 0.7)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(i / max(1, n - 1))
        dial(ax, -3.5, 0, 2.3, 2 * math.pi * 0.35 * t, CYAN)
        dial(ax, 3.5, 0, 2.3, 2 * math.pi * 0.35 * t / g, GOLD)
        save(fig, out, i, still)
    finish(out, still)


def render_contraction(out, seconds, still):
    """Ship (left dot) to star (right): the gap is 10 ly at rest and shrinks to 1/7.09 of that in the ship's frame
    at 0.99c (to ~1.41 ly). The star slides in; no numbers. A faint ghost marks the rest-frame distance."""
    rng = np.random.default_rng(STYLE.get("seed", 10))
    n = int(seconds * FPS)
    bg = rng.uniform([-8, -4.5], [8, 4.5], (400, 2))
    frames = [int(n * 0.85)] if still else range(n)
    x0, L0 = -6.5, 13.0
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.15) / 0.7)
        L = L0 * (1 - s * (1 - 1 / 7.0888))
        fig, ax = canvas(i / max(1, n - 1))
        ax.scatter(bg[:, 0], bg[:, 1], s=4, color=WHITE, alpha=0.5, lw=0)
        ax.add_patch(Circle((x0 + L0, 0), 0.35, fill=False, ec=DIM, lw=2, ls=(0, (3, 4))))
        ax.plot([x0, x0 + L], [0, 0], color=GOLD, lw=4)
        ax.add_patch(Circle((x0, 0), 0.22, color=CYAN, zorder=5))
        ax.add_patch(Circle((x0 + L, 0), 0.35, color=GOLD, zorder=5))
        ax.add_patch(Circle((x0 + L, 0), 0.8, color=GOLD, alpha=0.2, lw=0, zorder=4))
        save(fig, out, i, still)
    finish(out, still)


PIPE = {}


def save(fig, out, i, still):
    if STYLE["on"] and not still:
        if out not in PIPE:
            PIPE[out] = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
                                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                                          "-pix_fmt", "yuv420p", "-crf", "16", out.rstrip("/") + ".mp4"],
                                         stdin=subprocess.PIPE)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        assert buf.shape[:2] == (H, W), buf.shape
        PIPE[out].stdin.write(buf.tobytes())
        plt.close(fig)
        return
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, "still.png" if still else f"{i:04d}.png"), facecolor=BG)
    plt.close(fig)


def finish(out, still):
    if still:
        print("wrote", os.path.join(out, "still.png"))
        return
    mp4 = out.rstrip("/") + ".mp4"
    if out in PIPE:
        PIPE[out].stdin.close()
        if PIPE.pop(out).wait():
            raise SystemExit(f"ffmpeg failed on {mp4}")
        print("wrote", mp4)
        return
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(out, "%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", mp4], check=True)
    print("wrote", mp4)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=["starfield", "lightclock", "energy", "muons", "gpsclocks", "mapdrift", "gammaclocks", "twinclocks", "contraction", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    ap.add_argument("--variant", choices=sorted(VARIANTS))
    a = ap.parse_args()
    global GOLD, CYAN
    jobs = {"starfield": (render_starfield, 14), "lightclock": (render_lightclock, 12),
            "energy": (render_energy, 10), "muons": (render_muons, 12),
            "gpsclocks": (render_gpsclocks, 12), "mapdrift": (render_mapdrift, 8), "gammaclocks": (render_gammaclocks, 18),
            "twinclocks": (render_twinclocks, 16), "contraction": (render_contraction, 10)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        if not a.variant:
            fn(os.path.join(a.out, name), a.seconds or secs, a.still)
            continue
        V = VARIANTS[a.variant]
        GOLD, CYAN = V["gold"], V["cyan"]
        bed, stars = make_bed(V["seed"] + len(name), stars=(name != "starfield"), N=BED_STARS.get(name, 2600))
        STYLE.update(on=True, name=name, cam=V["cam"], bed=bed, stars=stars, seed=V["seed"] + len(name))
        fn(os.path.join(a.out, f"{name}_{a.variant}"), a.seconds or secs + 8, a.still)


if __name__ == "__main__":
    sys.exit(main())
