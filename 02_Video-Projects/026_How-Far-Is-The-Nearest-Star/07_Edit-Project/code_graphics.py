#!/usr/bin/env python3
"""Code-drawn graphics for the nearest-star film (026). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py parallax   out/   # ch.2: Earth moves Jan -> Jul; the near star shifts against the far stars
  python3 code_graphics.py triple     out/   # ch.1: Alpha Cen A and B orbit each other; Proxima loops round them, far out
  python3 code_graphics.py journey    out/   # ch.4: five lanes to Proxima at true relative speeds; only light moves visibly
  python3 code_graphics.py lighttimes out/   # ch.4: Moon, Sun, Proxima light-travel times as bars on a log scale
  python3 code_graphics.py all        out/
  add --still to write one frame only (review); --seconds N to change length

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (01_Script/SOURCES.md):
  parallax   Exaggerated for the eye (Proxima's real shift is 0.77 arcsec). The geometry is the point: a bigger shift
             means a nearer star.
  triple     Not to scale. AB separation is about 11-35 AU over 80 years; Proxima is about 13,000 AU out on a ~550,000-yr
             orbit. Drawn as a slow wide loop and a fast tight pair so the family relation reads.
  journey    Lanes are walking 5 km/h, car 100 km/h, jet 900 km/h, Voyager 1 about 61,000 km/h, and light. Speeds are
             to scale, with light set to cross in 3 s. The other four markers never visibly move, and that is honest.
  lighttimes Moon 1.3 s, Sun 499 s, Proxima 4.25 yr (1.34e8 s), as bar lengths on log10(seconds) from 0.1 s to 1e9 s.
"""
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
CYAN = "#5fd6ff"
RED = "#ff6a4a"
EARTH = "#3a7bd5"


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


def render_parallax(out, seconds, still):
    """Bottom: the Sun, Earth's orbit seen at a tilt, Earth moving from one side (January) to the other (July), with
    a sight line to a near star above. Top: the sky view from Earth, far stars fixed and the near star sliding across
    them as Earth moves."""
    rng = np.random.default_rng(1838)
    n = int(seconds * FPS)
    far = rng.uniform([-7.5, 0.6], [7.5, 4.3], (160, 2))
    frames = [int(n * 0.8)] if still else range(n)
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.1) / 0.8)
        fig, ax = canvas()
        # sky panel
        ax.add_patch(Rectangle((-7.8, 0.4), 15.6, 4.0, fill=False, ec=DIM, lw=1.5, alpha=0.5))
        ax.scatter(far[:, 0], far[:, 1], s=6, color=WHITE, alpha=0.7, lw=0)
        nx = 2.2 - 4.4 * s                           # near star slides opposite to Earth's move
        ax.add_patch(Circle((nx, 2.5), 0.12, color=RED, zorder=5))
        ax.add_patch(Circle((nx, 2.5), 0.35, color=RED, alpha=0.25, lw=0, zorder=4))
        # orbit panel
        ax.add_patch(Ellipse((0, -2.7), 9.0, 2.2, fill=False, ec=DIM, lw=1.5, alpha=0.7))
        ax.add_patch(Circle((0, -2.7), 0.35, color=GOLD, zorder=5))
        th = math.pi * (1 - s)                       # from the left side (Jan) to the right side (Jul) along the front
        ex, ey = 4.5 * math.cos(th), -2.7 - 1.1 * math.sin(th)
        ax.add_patch(Circle((ex, ey), 0.16, color=EARTH, zorder=6))
        ax.plot([ex, 0], [ey, -0.2], color=RED, lw=1.5, alpha=0.6, ls=(0, (4, 4)))
        ax.add_patch(Circle((0, -0.2), 0.1, color=RED, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_triple(out, seconds, still):
    """Alpha Cen A (larger, yellow-white) and B (smaller, orange) circle their centre of mass fast; Proxima (small,
    red) moves slowly on a wide loop round the pair. Not to scale (see module docstring)."""
    rng = np.random.default_rng(4)
    n = int(seconds * FPS)
    bg = rng.uniform([-8, -4.5], [8, 4.5], (300, 2))
    frames = [int(n * 0.5)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas()
        ax.scatter(bg[:, 0], bg[:, 1], s=3, color=WHITE, alpha=0.4, lw=0)
        a = 2 * math.pi * t / 4.0
        ax.add_patch(Circle((0.55 * math.cos(a), 0.55 * math.sin(a)), 0.32, color="#fff2c4", zorder=5))
        ax.add_patch(Circle((-0.7 * math.cos(a), -0.7 * math.sin(a)), 0.24, color="#ffb35c", zorder=5))
        ang = math.radians(200) + 2 * math.pi * t / 60.0
        th = np.linspace(0, 2 * math.pi, 300)
        ax.plot(6.2 * np.cos(th), 3.6 * np.sin(th), color=DIM, lw=1.2, alpha=0.35, ls=(0, (3, 5)))
        px, py = 6.2 * math.cos(ang), 3.6 * math.sin(ang)
        ax.add_patch(Circle((px, py), 0.11, color=RED, zorder=6))
        ax.add_patch(Circle((px, py), 0.35, color=RED, alpha=0.25, lw=0, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_journey(out, seconds, still):
    """Five lanes from the Sun (left) to Proxima (right). The lanes appear one by one: walking, car, jet, Voyager,
    then light. Each marker moves at its true speed relative to light, with light crossing in 3 s, so only light
    visibly moves."""
    n = int(seconds * FPS)
    c = 1.079e9
    speeds = [5, 100, 900, 61000, c]
    cols = [WHITE, WHITE, WHITE, CYAN, GOLD]
    X0, X1 = -6.8, 6.8
    frames = [int(n * 0.92)] if still else range(n)
    for i in frames:
        s = i / max(1, n - 1)
        fig, ax = canvas()
        for k, (v, col) in enumerate(zip(speeds, cols)):
            y = 3.0 - k * 1.5
            appear = ease((s - k * 0.12) / 0.06)
            if appear <= 0:
                continue
            ax.plot([X0, X1], [y, y], color=DIM, lw=1.5, alpha=0.4 * appear)
            ax.add_patch(Circle((X0, y), 0.18, color=GOLD, alpha=appear))
            ax.add_patch(Circle((X1, y), 0.14, color=RED, alpha=appear))
            t_lane = max(0.0, (s - k * 0.12) * seconds)
            frac = min(1.0, (v / c) * t_lane / 3.0)
            mx = X0 + (X1 - X0) * frac
            if k == 4:
                ax.plot([X0, mx], [y, y], color=GOLD, lw=3, alpha=0.8 * appear)
            ax.add_patch(Circle((mx, y), 0.1, color=col, alpha=appear, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_lighttimes(out, seconds, still):
    """Three bars on a log10(seconds) scale from 0.1 s to 1e9 s: Moon (1.3 s), Sun (499 s), Proxima (1.34e8 s). Each
    grows in turn. A faint tick marks each power of ten. Text-free."""
    n = int(seconds * FPS)
    vals = [1.3, 499.0, 1.34e8]
    cols = ["#d9d9d9", GOLD, RED]
    L0, L1 = -1.0, 9.0
    X0, X1 = -6.5, 6.5
    frames = [int(n * 0.95)] if still else range(n)
    for i in frames:
        s = i / max(1, n - 1)
        fig, ax = canvas()
        for p in range(int(L0), int(L1) + 1):
            x = X0 + (X1 - X0) * (p - L0) / (L1 - L0)
            ax.plot([x, x], [-3.2, 3.2], color=DIM, lw=1, alpha=0.18)
        for k, (v, col) in enumerate(zip(vals, cols)):
            g = ease((s - 0.05 - k * 0.3) / 0.25)
            full = (math.log10(v) - L0) / (L1 - L0)
            y = 2.0 - k * 2.0
            ax.add_patch(Rectangle((X0, y - 0.35), (X1 - X0) * full * g, 0.7, color=col, lw=0))
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
    ap.add_argument("which", choices=["parallax", "triple", "journey", "lighttimes", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    jobs = {"parallax": (render_parallax, 12), "triple": (render_triple, 12), "journey": (render_journey, 14),
            "lighttimes": (render_lighttimes, 10)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
