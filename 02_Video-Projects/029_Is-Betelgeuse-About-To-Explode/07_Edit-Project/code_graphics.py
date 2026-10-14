#!/usr/bin/env python3
"""Code-drawn graphics for the Betelgeuse film (029). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py scale  out/   # ch.1: the Sun as a dot, then Betelgeuse's outline over the inner Solar System
  python3 code_graphics.py dip    out/   # ch.2: the 2019-20 Great Dimming as a light curve drawing itself (no axes text)
  python3 code_graphics.py shells out/   # ch.3: onion shells, the iron core grows, collapses, the shock races out
  python3 code_graphics.py orion  out/   # ch.4: Orion; the shoulder flares to a brilliant white point, then fades away
  python3 code_graphics.py finder out/   # ch.1: the belt glows, a soft trail runs up and left, the orange shoulder brightens
  python3 code_graphics.py twins  out/   # ch.5: two identical orange stars; cutaways show one young inside, one near the end
  python3 code_graphics.py all    out/
  add --still to write one frame only (review); --seconds N to change length

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (01_Script/SOURCES.md, CLAUDE_QUOTE_CHECK_v02.md):
  scale   Radius 764 R_sun = 3.55 AU (Joyce et al. 2020). Orbits drawn at Mercury 0.39, Venus 0.72, Earth 1.0,
          Mars 1.52 AU and the main belt 2.2-3.3 AU, all to scale with the star's outline.
  dip     V about 0.5 to about 1.6 (Feb 2020) and back by April 2020: drawn as relative flux, about 36% at the bottom.
  shells  H, He, C, O, Si, Fe from outside in. Not to scale; the collapse is one sharp move, the shock a bright ring.
  orion   Star positions from RA/Dec (east to the left). Peak about a half Moon; fade over the clip's second half.
  finder  Same positions as orion. Up and to the left of the belt, as the script says (northern-hemisphere view).
  twins   Schematic only: left has a helium-burning core (H, He, C); right has the full onion to an iron core.
"""
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
ORANGE = "#ff8a3c"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
EARTH = "#3a7bd5"
MARS = "#d0603a"
SHELLS = ["#ff8a3c", "#ffb347", "#f2d16b", "#9fd36b", "#6bc4d3", "#8a8f9c"]   # H, He, C, O, Si, Fe


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


def glow(ax, x, y, r, col, z=5, a=1.0):
    for k, al in ((3.2, 0.06), (2.0, 0.14), (1.3, 0.3)):
        ax.add_patch(Circle((x, y), r * k, color=col, alpha=al * a, lw=0, zorder=z))
    ax.add_patch(Circle((x, y), r, color=col, alpha=a, lw=0, zorder=z + 1))


def soft_glow(ax, x, y, r, col, z=5, a=1.0):
    """Many faint layers, so a big flare reads as light rather than rings."""
    for k in np.linspace(4.0, 1.05, 24):
        ax.add_patch(Circle((x, y), r * k, color=col, alpha=a * 0.05 * math.exp(-(k - 1) * 0.6), lw=0, zorder=z))
    ax.add_patch(Circle((x, y), r, color=col, alpha=a, lw=0, zorder=z + 1))


def frames_for(seconds, still, at=0.8):
    n = int(seconds * FPS)
    return n, ([int(n * at)] if still else range(n))


def render_scale(out, seconds, still):
    """Inner Solar System to scale (1 AU = 1.1 units). Betelgeuse's surface grows out from the Sun's place until it
    swallows Mercury to Mars and passes the belt."""
    n, frames = frames_for(seconds, still, at=0.95)
    k = 1.1
    rng = np.random.default_rng(3)
    belt_r = rng.uniform(2.2, 3.3, 500) * k
    belt_t = rng.uniform(0, 2 * math.pi, 500)
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.25) / 0.6)
        fig, ax = canvas()
        for au, col in ((0.39, DIM), (0.72, DIM), (1.0, EARTH), (1.52, MARS)):
            ax.add_patch(Circle((0, 0), au * k, fill=False, ec=col, lw=1.4, alpha=0.8, zorder=7))
        ax.scatter(belt_r * np.cos(belt_t), belt_r * np.sin(belt_t), s=3, color=WHITE, alpha=0.45, lw=0, zorder=7)
        r = 0.02 + 3.55 * k * s
        if s > 0:
            for j, a in enumerate((0.12, 0.2, 0.35)):
                ax.add_patch(Circle((0, 0), r * (1 - 0.05 * j), color=ORANGE, alpha=a, lw=0, zorder=4))
            ax.add_patch(Circle((0, 0), r, fill=False, ec=ORANGE, lw=2, alpha=0.9, zorder=5))
        glow(ax, 0, 0, 0.06, GOLD, z=6, a=1 - s)
        save(fig, out, i, still)
    finish(out, still)


def render_dip(out, seconds, still):
    """A smooth light curve from mid-2019 to mid-2020 drawing itself left to right; the dip to about 36% in Feb 2020."""
    n, frames = frames_for(seconds, still, at=0.95)
    t = np.linspace(0, 1, 400)
    flux = 1 - 0.64 * np.exp(-((t - 0.62) / 0.11) ** 2) + 0.05 * np.sin(t * 9)
    x = -7 + 14 * t
    y = -3.2 + 6.0 * (flux - 0.3) / 0.8
    for i in frames:
        u = ease(i / max(1, n - 1) / 0.85)
        m = max(2, int(len(t) * u))
        fig, ax = canvas()
        ax.plot([-7, 7], [y[0], y[0]], color=DIM, lw=1, alpha=0.3, ls=(0, (5, 6)))
        ax.plot(x[:m], y[:m], color=ORANGE, lw=3)
        glow(ax, x[m - 1], y[m - 1], 0.08, ORANGE, z=6)
        save(fig, out, i, still)
    finish(out, still)


def render_shells(out, seconds, still):
    """Nested shells; the grey iron core grows (0-55%), snaps inward (55-62%), then a bright shock ring races out."""
    n, frames = frames_for(seconds, still, at=0.75)
    radii = [3.8, 3.0, 2.3, 1.7, 1.15]
    for i in frames:
        u = i / max(1, n - 1)
        grow = ease(u / 0.55)
        snap = ease((u - 0.55) / 0.07)
        shock = max(0.0, (u - 0.6) / 0.4)
        fig, ax = canvas()
        for r, col in zip(radii, SHELLS):
            rr = r * (1 - 0.15 * snap)
            ax.add_patch(Circle((0, 0), rr, color=col, alpha=0.85 * (1 - 0.8 * shock), lw=0))
        core = (0.25 + 0.6 * grow) * (1 - 0.92 * snap)
        ax.add_patch(Circle((0, 0), core, color=SHELLS[-1], lw=0, zorder=5))
        if snap > 0.5:
            glow(ax, 0, 0, 0.07, WHITE, z=6)
        if shock > 0:
            rs = 0.3 + 9 * ease(shock)
            ax.add_patch(Circle((0, 0), rs, fill=False, ec=WHITE, lw=6 * (1 - shock) + 1, alpha=1 - 0.7 * shock, zorder=7))
        save(fig, out, i, still)
    finish(out, still)


ORION = {  # name: (RA hours, Dec degrees, size)
    "betelgeuse": (5.919, 7.41, 0.10), "bellatrix": (5.418, 6.35, 0.07), "meissa": (5.585, 9.93, 0.04),
    "alnitak": (5.679, -1.94, 0.06), "alnilam": (5.604, -1.20, 0.065), "mintaka": (5.533, -0.30, 0.055),
    "saiph": (5.796, -9.67, 0.06), "rigel": (5.242, -8.20, 0.10),
}


def orion_xy(ra, dec, ra0=5.58, dec0=-0.5):
    return -(ra - ra0) * 15 * 0.42, (dec - dec0) * 0.42


def render_finder(out, seconds, still):
    """Orion, no flare. The belt brightens (0-30%), a dotted trail draws from Alnilam to Betelgeuse (30-65%), then
    Betelgeuse's orange glow lifts while the view eases in on it (65-100%)."""
    rng = np.random.default_rng(1054)
    field = rng.uniform([-8, -4.5], [8, 4.5], (300, 2))
    fs = rng.exponential(1.5, 300) + 0.3
    n, frames = frames_for(seconds, still, at=0.8)
    bx, by = orion_xy(*ORION["alnilam"][:2])
    tx, ty = orion_xy(*ORION["betelgeuse"][:2])
    for i in frames:
        u = i / max(1, n - 1)
        belt = ease(u / 0.3)
        trail = ease((u - 0.3) / 0.35)
        lift = ease((u - 0.65) / 0.35)
        fig, ax = canvas()
        z = 1 - 0.35 * lift
        cx, cy = tx * 0.5 * lift, ty * 0.5 * lift
        ax.set_xlim(cx - 8 * z, cx + 8 * z)
        ax.set_ylim(cy - 4.5 * z, cy + 4.5 * z)
        ax.scatter(field[:, 0], field[:, 1], s=fs, color=WHITE, alpha=0.45, lw=0)
        for name, (ra, dec, sz) in ORION.items():
            x, y = orion_xy(ra, dec)
            if name == "betelgeuse":
                soft_glow(ax, x, y, sz * (1 + 0.6 * lift), ORANGE, z=8)
            elif name in ("alnitak", "alnilam", "mintaka"):
                soft_glow(ax, x, y, sz * (1 + 0.5 * belt), WHITE, z=6)
            else:
                glow(ax, x, y, sz, "#cfe0ff" if name in ("rigel", "bellatrix") else WHITE, z=6)
        if trail > 0:
            m = np.linspace(0.12, 0.88 * trail, max(2, int(14 * trail)))
            ax.scatter(bx + (tx - bx) * m, by + (ty - by) * m, s=10, color=GOLD, alpha=0.7, lw=0, zorder=7)
        save(fig, out, i, still)
    finish(out, still)


def render_twins(out, seconds, still):
    """Two identical orange stars. A wedge opens in each (25-40%): the left shows a helium-burning star, the right a
    star with the full onion down to iron. They hold, close again (75-90%) and look the same once more."""
    n, frames = frames_for(seconds, still, at=0.6)
    env = "#b8582a"   # the hydrogen envelope seen in cut, darker than the surface so the wedge reads
    inside = {-4.0: ([2.4, 1.2, 0.65], [env, *SHELLS[1:3]]),
              4.0: ([2.4, 1.8, 1.45, 1.12, 0.82, 0.5], [env, *SHELLS[1:]])}
    for i in frames:
        u = i / max(1, n - 1)
        open_ = ease((u - 0.25) / 0.15) * (1 - ease((u - 0.75) / 0.15))
        fig, ax = canvas()
        for x0, (radii, cols) in inside.items():
            for k, al in ((1.12, 0.12), (1.05, 0.25)):
                ax.add_patch(Circle((x0, 0), 2.4 * k, color=ORANGE, alpha=al, lw=0, zorder=3))
            ax.add_patch(Circle((x0, 0), 2.4, color=ORANGE, lw=0, zorder=4))
            if open_ > 0.01:
                th = 100 * open_
                for r, col in zip(radii, cols):
                    ax.add_patch(Wedge((x0, 0), r, 90 - th / 2, 90 + th / 2, color=col, lw=0, zorder=6))
        save(fig, out, i, still)
    finish(out, still)


def render_orion(out, seconds, still):
    """Orion on a dark sky. Betelgeuse holds orange, swells to a brilliant white point (15-30%), holds, then fades
    over the second half until the shoulder is empty."""
    rng = np.random.default_rng(1054)
    field = rng.uniform([-8, -4.5], [8, 4.5], (300, 2))
    fs = rng.exponential(1.5, 300) + 0.3
    n, frames = frames_for(seconds, still, at=0.3)
    ra0, dec0 = 5.58, -0.5
    for i in frames:
        u = i / max(1, n - 1)
        flare = ease((u - 0.15) / 0.15)
        fade = ease((u - 0.5) / 0.45)
        fig, ax = canvas()
        ax.scatter(field[:, 0], field[:, 1], s=fs, color=WHITE, alpha=0.45, lw=0)
        for name, (ra, dec, sz) in ORION.items():
            x, y = orion_xy(ra, dec, ra0, dec0)
            if name == "betelgeuse":
                r = sz + 0.45 * flare * (1 - fade)
                col = ORANGE if flare < 0.5 else WHITE
                a = 1 - fade
                if a > 0.02:
                    soft_glow(ax, x, y, r * 0.55, col, z=8, a=a)
            else:
                glow(ax, x, y, sz, "#cfe0ff" if name in ("rigel", "bellatrix") else WHITE, z=6)
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
    jobs = {"scale": (render_scale, 12), "dip": (render_dip, 10), "shells": (render_shells, 14),
            "orion": (render_orion, 16), "finder": (render_finder, 12), "twins": (render_twins, 18)}
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
