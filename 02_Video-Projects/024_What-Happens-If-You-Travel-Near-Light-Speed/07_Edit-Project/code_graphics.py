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


def canvas():
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-4.5, 4.5)
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
    rng = np.random.default_rng(24)
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
        fig, ax = canvas()
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
        fig, ax = canvas()
        # rest clock (left)
        X0 = -5.0
        ph = (t / tick) % 2
        yy = -1.5 + Hgap * (ph if ph <= 1 else 2 - ph)
        for yM in (-1.5, 1.5):
            ax.plot([X0 - 0.8, X0 + 0.8], [yM, yM], color=WHITE, lw=5, solid_capstyle="round")
        ax.add_patch(Circle((X0, yy), 0.16, color=GOLD, zorder=5))
        ax.add_patch(Circle((X0, yy), 0.40, color=GOLD, alpha=0.18, lw=0))
        # moving clock (right half): wraps across x in [-1, 8]
        span = 9.0
        x_c = -1.0 + (vx * t) % span
        ph2 = (t / (tick * g)) % 2
        y2 = -1.5 + Hgap * (ph2 if ph2 <= 1 else 2 - ph2)
        for yM in (-1.5, 1.5):
            ax.plot([x_c - 0.8, x_c + 0.8], [yM, yM], color=WHITE, lw=5, solid_capstyle="round")
        # the zigzag trail of the photon over the last tick (one mirror-to-mirror trip)
        ts = np.linspace(max(0, t - tick * g), t, 80)
        xs = -1.0 + (vx * ts) % span
        p = (ts / (tick * g)) % 2
        ys = -1.5 + Hgap * np.where(p <= 1, p, 2 - p)
        breaks = np.where(np.diff(xs) < 0)[0]
        for seg in np.split(np.arange(len(ts)), breaks + 1):
            ax.plot(xs[seg], ys[seg], color=GOLD, lw=2.2, alpha=0.55)
        ax.add_patch(Circle((x_c, y2), 0.16, color=GOLD, zorder=5))
        ax.add_patch(Circle((x_c, y2), 0.40, color=GOLD, alpha=0.18, lw=0))
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
        fig, ax = canvas()
        ax.plot([X0, X1 + 0.6], [Y0, Y0], color=DIM, lw=2)
        ax.plot([X0, X0], [Y0, Y1 + 0.4], color=DIM, lw=2)
        ax.plot([X0 + (X1 - X0) * 1.0] * 2, [Y0, Y1 + 0.4], color=WHITE, lw=2, ls=(0, (6, 6)), alpha=0.7)
        ax.plot(xs[:k], ys[:k], color=GOLD, lw=4, solid_capstyle="round")
        ax.add_patch(Circle((xs[k - 1], ys[k - 1]), 0.14, color=WHITE, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_muons(out, seconds, still):
    rng = np.random.default_rng(1963)
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
        fig, ax = canvas()
        ax.add_patch(Rectangle((-8, -4.5), 16, GROUND + 4.5, color="#16202a", lw=0))
        ax.plot([-8, 8], [GROUND, GROUND], color=DIM, lw=2)
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
        fig, ax = canvas()
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
        ax.plot([2.2, 7.0], [base, base], color=DIM, lw=2)
        save(fig, out, i, still)
    finish(out, still)


def render_mapdrift(out, seconds, still):
    """A text-free street grid. A ring marks where you really are; the position dot drifts away about 10 km a day
    (sped up), leaving a trail. Shows what uncorrected GPS clocks would do."""
    n = int(seconds * FPS)
    frames = [int(n * 0.8)] if still else range(n)
    for i in frames:
        s = ease(i / max(1, n - 1))
        fig, ax = canvas()
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
        fig, ax = canvas()
        for k, rate in enumerate(rates):
            lit = ease((s - k * 0.17) / 0.1) if k else 1.0
            cx = -6.0 + k * 3.0
            col = WHITE if k == 0 else GOLD
            dial(ax, cx, 0, 1.15, 2 * math.pi * 0.5 * t * rate, col, alpha=0.25 + 0.75 * lit)
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
        fig, ax = canvas()
        dial(ax, -3.5, 0, 2.3, 2 * math.pi * 0.35 * t, CYAN)
        dial(ax, 3.5, 0, 2.3, 2 * math.pi * 0.35 * t / g, GOLD)
        save(fig, out, i, still)
    finish(out, still)


def render_contraction(out, seconds, still):
    """Ship (left dot) to star (right): the gap is 10 ly at rest and shrinks to 1/7.09 of that in the ship's frame
    at 0.99c (to ~1.41 ly). The star slides in; no numbers. A faint ghost marks the rest-frame distance."""
    rng = np.random.default_rng(10)
    n = int(seconds * FPS)
    bg = rng.uniform([-8, -4.5], [8, 4.5], (400, 2))
    frames = [int(n * 0.85)] if still else range(n)
    x0, L0 = -6.5, 13.0
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.15) / 0.7)
        L = L0 * (1 - s * (1 - 1 / 7.0888))
        fig, ax = canvas()
        ax.scatter(bg[:, 0], bg[:, 1], s=4, color=WHITE, alpha=0.5, lw=0)
        ax.add_patch(Circle((x0 + L0, 0), 0.35, fill=False, ec=DIM, lw=2, ls=(0, (3, 4))))
        ax.plot([x0, x0 + L], [0, 0], color=GOLD, lw=4)
        ax.add_patch(Circle((x0, 0), 0.22, color=CYAN, zorder=5))
        ax.add_patch(Circle((x0 + L, 0), 0.35, color=GOLD, zorder=5))
        ax.add_patch(Circle((x0 + L, 0), 0.8, color=GOLD, alpha=0.2, lw=0, zorder=4))
        save(fig, out, i, still)
    finish(out, still)


def save(fig, out, i, still):
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, "still.png" if still else f"{i:04d}.png"), facecolor=BG)
    plt.close(fig)


def finish(out, still):
    if still:
        print("wrote", os.path.join(out, "still.png"))
        return
    mp4 = out.rstrip("/") + ".mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(out, "%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", mp4], check=True)
    print("wrote", mp4)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=["starfield", "lightclock", "energy", "muons", "gpsclocks", "mapdrift", "gammaclocks", "twinclocks", "contraction", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    jobs = {"starfield": (render_starfield, 14), "lightclock": (render_lightclock, 12),
            "energy": (render_energy, 10), "muons": (render_muons, 12),
            "gpsclocks": (render_gpsclocks, 12), "mapdrift": (render_mapdrift, 8), "gammaclocks": (render_gammaclocks, 18),
            "twinclocks": (render_twinclocks, 16), "contraction": (render_contraction, 10)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
