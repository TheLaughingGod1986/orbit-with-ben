#!/usr/bin/env python3
"""Code-drawn graphics for the Gliese 710 film (028). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py drift   out/   # ch.1: most stars slide sideways; one orange star stays put and grows
  python3 code_graphics.py path    out/   # ch.2: the predicted path narrows and moves inwards, Hipparcos -> Gaia DR3
  python3 code_graphics.py scale   out/   # ch.2: 1 AU = 1 cm; pull back from Earth and Neptune to the star's pass
  python3 code_graphics.py shell   out/   # ch.3: pull back from the planets to the Oort Cloud shell
  python3 code_graphics.py shower  out/   # ch.4: the star crosses the shell; comets near its path are nudged in or out
  python3 code_graphics.py sky     out/   # ch.5: a night sky in which one orange star brightens past the brightest
  python3 code_graphics.py traffic out/   # ch.6: stars drifting past the Sun over millions of years
  python3 code_graphics.py all     out/
  add --still to write one frame only (review); --seconds N to change length

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (01_Script/SOURCES.md):
  drift    Not to scale. Gliese 710's proper motion is 0.43 mas/yr against a radial velocity of -14.4 km/s; the other
           stars' sideways drift is exaggerated so the contrast reads.
  path     Closest approach shrinks from about 1 ly (Hipparcos, 0.27-0.31 pc) to about 0.2 ly (Gaia DR3 0.064 pc), and
           the band narrows with each release (DR2, then DR3). Not to scale; the inward move and the narrowing are the
           point.
  scale    1 AU = 1 cm: Earth at 1 cm, Neptune at 30 cm, the pass at 105-131 m (10,500-13,100 AU). The pull-back is
           logarithmic, so all three fit one move.
  shell    Inner edge 2,000-5,000 AU, outer edge to about 100,000 AU (NASA). Drawn as a 2D shell, log-compressed so the
           planets are still a visible dot.
  shower   Comets within a band of the star's path get a kick: some outwards, some onto long ellipses towards the Sun.
           The infall lag is shown by the inward trails starting after the star has passed.
  sky      Peak V = -2.7 against Sirius at -1.46 (about 3x brighter). Glow size follows brightness.
  traffic  Not to scale. Straight-line passes at random impact distances; a few cross the outer shell.
"""
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
ORANGE = "#ff9a3c"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
ICE = "#a9d8ff"
EARTH = "#3a7bd5"
NEPTUNE = "#4f6bff"


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


def glow(ax, x, y, r, col, z=5):
    for k, a in ((3.2, 0.06), (2.0, 0.14), (1.3, 0.3)):
        ax.add_patch(Circle((x, y), r * k, color=col, alpha=a, lw=0, zorder=z))
    ax.add_patch(Circle((x, y), r, color=col, lw=0, zorder=z + 1))


def frames_for(seconds, still, at=0.8):
    n = int(seconds * FPS)
    return n, ([int(n * at)] if still else range(n))


def render_drift(out, seconds, still):
    """Field stars slide sideways at different speeds; Gliese 710 sits still near centre and slowly grows."""
    rng = np.random.default_rng(710)
    n, frames = frames_for(seconds, still)
    stars = rng.uniform([-9, -4.4], [9, 4.4], (220, 2))
    vx = rng.uniform(0.15, 0.6, 220) * rng.choice([-1, 1], 220)
    vy = rng.uniform(-0.08, 0.08, 220)
    size = rng.uniform(2, 10, 220)
    for i in frames:
        t = i / FPS
        s = ease(i / max(1, n - 1))
        fig, ax = canvas()
        x = (stars[:, 0] + vx * t + 9) % 18 - 9
        y = stars[:, 1] + vy * t
        ax.scatter(x, y, s=size, color=WHITE, alpha=0.75, lw=0)
        glow(ax, 0.3, 0.2, 0.05 + 0.13 * s, ORANGE)
        save(fig, out, i, still)
    finish(out, still)


def render_path(out, seconds, still):
    """The Sun at left; a fuzzy band (the predicted path) sweeps past it. Three steps: wide and far (Hipparcos),
    narrower and nearer (DR2), thin and nearest (DR3). A faint ring marks about 1 ly."""
    n, frames = frames_for(seconds, still, at=0.95)
    steps = [(2.6, 1.6), (0.75, 0.45), (0.6, 0.12)]    # (miss distance, half-width), in ring units of about 1 ly = 2.6
    sx, sy = -4.5, 0.0
    for i in frames:
        u = i / max(1, n - 1) * 3
        k = min(2, int(u))
        f = ease((u - k) / 0.6) if k > 0 else 1.0
        d0, w0 = steps[max(0, k - 1)] if k > 0 else steps[0]
        d1, w1 = steps[k]
        d = d0 + (d1 - d0) * f
        w = w0 + (w1 - w0) * f
        fig, ax = canvas()
        ax.add_patch(Circle((sx, sy), 2.6, fill=False, ec=DIM, lw=1.2, alpha=0.35, ls=(0, (5, 6))))
        glow(ax, sx, sy, 0.22, GOLD)
        xs = np.linspace(-8, 8, 200)
        yc = sy + d + 0.0 * xs
        for j, a in enumerate(np.linspace(0.05, 0.22, 8)):
            ww = w * (1 - j / 8)
            ax.fill_between(xs, yc - ww, yc + ww, color=ORANGE, alpha=a, lw=0)
        ax.plot(xs, yc, color=ORANGE, lw=1.6, alpha=0.9)
        glow(ax, 6.2 - 2.0 * (i / max(1, n - 1)), sy + d, 0.12, ORANGE, z=8)
        save(fig, out, i, still)
    finish(out, still)


def render_scale(out, seconds, still):
    """1 AU = 1 cm along a line. The view width grows from 2.5 cm to 300 m on a log scale; Earth, Neptune, then the
    band of the star's pass (105-131 m) come into frame."""
    n, frames = frames_for(seconds, still, at=0.99)
    for i in frames:
        s = ease(i / max(1, n - 1))
        width_cm = 10 ** (math.log10(2.5) + (math.log10(30000) - math.log10(2.5)) * s)
        k = 14.0 / width_cm                           # screen units per cm; the Sun sits at x = -7
        fig, ax = canvas()
        ax.plot([-7, 8], [0, 0], color=DIM, lw=1, alpha=0.4)
        glow(ax, -7, 0, 0.18, GOLD)
        for cm, col, r in ((1, EARTH, 0.1), (30, NEPTUNE, 0.12)):
            x = -7 + cm * k
            if 0.35 < x + 7 and x < 8.5:                  # drawn only while it is clear of the Sun's glow
                ax.add_patch(Circle((x, 0), r, color=col, zorder=6))
        a, b = -7 + 10500 * k, -7 + 13100 * k
        if a < 8.5:
            ax.axvspan(a, min(b, 8.5), color=ORANGE, alpha=0.18, lw=0)
            glow(ax, (a + min(b, 8.5)) / 2, 1.6, 0.12, ORANGE)
        save(fig, out, i, still)
    finish(out, still)


def oort_points(rng, n=2600):
    r = 10 ** rng.uniform(math.log10(2.0), math.log10(4.2), n)    # log-compressed radius, screen units
    th = rng.uniform(0, 2 * math.pi, n)
    return np.c_[r * np.cos(th), r * np.sin(th)], rng.uniform(1, 5, n)


def render_shell(out, seconds, still):
    """Start close on the Sun with the planet orbits; pull back until the orbits are a dot inside the icy shell."""
    rng = np.random.default_rng(1950)
    pts, sz = oort_points(rng)
    n, frames = frames_for(seconds, still, at=0.95)
    for i in frames:
        s = ease(i / max(1, n - 1))
        zoom = 10 ** (math.log10(12) * (1 - s))              # 12x at the start, 1x at the end
        fig, ax = canvas()
        for r, a in ((0.25, 0.5), (0.45, 0.45), (0.7, 0.4), (0.95, 0.35)):
            ax.add_patch(Circle((0, 0), r * zoom * 0.1 + 0.02, fill=False, ec=DIM, lw=1, alpha=a))
        glow(ax, 0, 0, 0.05 + 0.04 * (1 - s), GOLD)
        p = pts * zoom
        m = (np.abs(p[:, 0]) < 8.5) & (np.abs(p[:, 1]) < 5)
        ax.scatter(p[m, 0], p[m, 1], s=sz[m], color=ICE, alpha=0.18 + 0.4 * s, lw=0)
        save(fig, out, i, still)
    finish(out, still)


def render_shower(out, seconds, still):
    """The orange star crosses the upper part of the shell left to right. Comets within a band of its path are kicked:
    about a third flung outwards, the rest onto long trails towards the Sun that start after the star has passed."""
    rng = np.random.default_rng(2016)
    pts, sz = oort_points(rng, 2200)
    n, frames = frames_for(seconds, still, at=0.9)
    py = 2.9
    near = np.abs(pts[:, 1] - py) < 0.45
    out_kick = near & (rng.uniform(0, 1, len(pts)) < 0.35)
    in_fall = near & ~out_kick
    depth = rng.uniform(0.45, 0.85, int(in_fall.sum()))      # how far each one falls by the end; never a single clump
    for i in frames:
        u = i / max(1, n - 1)
        sx = -9 + 18 * ease(u / 0.6)
        fig, ax = canvas()
        glow(ax, 0, 0, 0.07, GOLD)
        passed = np.clip((sx - pts[:, 0]) / 3.0, 0, 1)        # how long since the star went by each comet
        p = pts.copy()
        p[out_kick, 1] += 1.6 * passed[out_kick] ** 1.5
        lag = np.clip((u - 0.55) / 0.45, 0, 1)                 # the infall starts late
        fall = ease(lag) * passed[in_fall] * depth
        p[in_fall] = pts[in_fall] * (1 - fall[:, None])
        ax.scatter(p[~near, 0], p[~near, 1], s=sz[~near], color=ICE, alpha=0.35, lw=0)
        ax.scatter(p[near, 0], p[near, 1], s=sz[near] + 2, color=WHITE, alpha=0.8, lw=0)
        for (x0, y0), (x1, y1) in zip(pts[in_fall][::4], p[in_fall][::4]):
            ax.plot([x0, x1], [y0, y1], color=ICE, lw=0.8, alpha=0.25 * lag)
        glow(ax, sx, py, 0.16, ORANGE, z=8)
        save(fig, out, i, still)
    finish(out, still)


def render_sky(out, seconds, still):
    """A night sky with a horizon. Sirius is the brightest point at the start; one orange star brightens until its
    glow is clearly larger (-2.7 against -1.46, about 3x)."""
    rng = np.random.default_rng(1046)
    n, frames = frames_for(seconds, still, at=0.95)
    stars = rng.uniform([-8, -2.6], [8, 4.4], (420, 2))
    size = rng.exponential(2.0, 420) + 0.5
    for i in frames:
        s = ease(i / max(1, n - 1))
        fig, ax = canvas()
        hx = np.linspace(-8, 8, 60)
        ax.fill_between(hx, -4.5, -3.0 + 0.25 * np.sin(hx * 0.7), color="#010204", lw=0, zorder=9)   # dark ground
        ax.scatter(stars[:, 0], stars[:, 1], s=size, color=WHITE, alpha=0.75, lw=0)
        glow(ax, -3.6, 1.2, 0.07, WHITE)                       # Sirius
        r = 0.03 + 0.09 * s                                    # ends about 1.75x Sirius's radius, about 3x its area
        glow(ax, 2.4, 2.1, r, ORANGE)
        save(fig, out, i, still)
    finish(out, still)


def render_traffic(out, seconds, still):
    """The Sun with a faint shell at centre. Stars cross on straight lines at random miss distances; the slow pace
    stands for millions of years. A few cut through the shell."""
    rng = np.random.default_rng(70000)
    pts, sz = oort_points(rng, 1400)
    n, frames = frames_for(seconds, still, at=0.6)
    k = 16
    ang = rng.uniform(0, math.pi, k)
    miss = rng.uniform(-4.2, 4.2, k)
    miss[:3] = (3.4, -2.6, 3.9)
    t0 = rng.uniform(-0.4, 0.8, k)
    col = rng.choice([WHITE, ORANGE, "#ffb3a0", GOLD], k)
    for i in frames:
        u = i / max(1, n - 1)
        fig, ax = canvas()
        ax.scatter(pts[:, 0], pts[:, 1], s=sz, color=ICE, alpha=0.18, lw=0)
        glow(ax, 0, 0, 0.08, GOLD)
        for a, m, t, c in zip(ang, miss, t0, col):
            d = (u - t) * 26 - 13
            x = d * math.cos(a) - m * math.sin(a)
            y = d * math.sin(a) + m * math.cos(a)
            if abs(x) < 9 and abs(y) < 5.5:
                glow(ax, x, y, 0.06, c, z=7)
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
    jobs = {"drift": (render_drift, 12), "path": (render_path, 12), "scale": (render_scale, 12),
            "shell": (render_shell, 12), "shower": (render_shower, 16), "sky": (render_sky, 12),
            "traffic": (render_traffic, 16)}
    ap.add_argument("which", choices=[*jobs, "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
