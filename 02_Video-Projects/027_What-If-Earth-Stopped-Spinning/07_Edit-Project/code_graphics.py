#!/usr/bin/env python3
"""Code-drawn graphics for the Earth-spin film (027). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py speed   out/   # ch.0-1: a turning globe; arrows show ground speed, longest at the equator
  python3 code_graphics.py bulge   out/   # ch.1: the equator bulges (gently exaggerated) as the spin is shown
  python3 code_graphics.py air     out/   # ch.2: the globe stops; the air carries on east, fastest at the equator
  python3 code_graphics.py oceans  out/   # ch.3: slow stop: the oceans drain to two polar caps, one band of land
  python3 code_graphics.py dayyear out/   # ch.3: no spin: Earth goes round the Sun and each side gets half a year of day
  python3 code_graphics.py tides   out/   # ch.4: the tidal bulge rides ahead of the Moon; the Moon slowly backs away
  python3 code_graphics.py clock   out/   # ch.4: a dial whose day has 22 hour ticks, growing to today's 24
  python3 code_graphics.py all     out/
  add --still to write one frame only (review); --seconds N to change length

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (01_Script/SOURCES.md):
  speed    Ground speed = 465 m/s x cos(latitude): about 1,670 km/h at the equator, about 1,040 km/h at London (51.5 N),
           0 at the poles. Arrow length is proportional.
  bulge    Equatorial radius 6,378 km vs polar 6,357 km (about 0.3%); drawn at 8% so the eye can see it.
  air      Same profile as speed, arrows sweep east while the globe holds still.
  oceans   After Fraczek (Esri ArcUser, Summer 2010): two polar oceans and one equatorial band of land. Schematic.
  dayyear  Zero rotation relative to the stars: the lit half faces the Sun only as Earth goes round, so one solar
           day = one year.
  tides    Not to scale. The bulge leads the Earth-Moon line; the Moon's orbit widens (3.8 cm a year, exaggerated).
  clock    About 22 hours a day in the Devonian (Wells 1963), 24 today.
"""
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Wedge, FancyArrow

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
SEA = "#2f6fc0"
LAND = "#d8b36a"
ICE = "#dfeaf5"
AIR = "#9fe3ff"
MOON = "#c9c9cf"


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


def frames_for(seconds, still, at=0.8):
    n = int(seconds * FPS)
    return n, ([int(n * at)] if still else range(n))


def globe(ax, x, y, r, phase, rx=1.0, land=True):
    """A side-on globe: sea disc, meridians that slide with phase (the spin), a few latitude lines."""
    disc = Ellipse((x, y), 2 * r * rx, 2 * r, color=SEA, zorder=2)
    ax.add_patch(disc)
    if land:
        rng = np.random.default_rng(3)
        blobs = rng.uniform([-math.pi, -0.9], [math.pi, 0.9], (14, 2))
        for lon, lat in blobs:
            lo = (lon + phase + math.pi) % (2 * math.pi) - math.pi
            if abs(lo) < math.pi / 2:
                bx = x + r * rx * math.sin(lo) * math.cos(lat)
                by = y + r * math.sin(lat)
                w = 0.35 * r * math.cos(lo)
                blob = Ellipse((bx, by), w, 0.28 * r, color=LAND, alpha=0.85, zorder=3)
                ax.add_patch(blob)
                blob.set_clip_path(disc)                     # no slivers past the limb
    for k in range(12):
        lo = (k * math.pi / 6 + phase + math.pi) % (2 * math.pi) - math.pi
        if abs(lo) < math.pi / 2:
            ys = np.linspace(-1, 1, 60)
            xs = x + r * rx * math.sin(lo) * np.sqrt(1 - ys ** 2)
            ax.plot(xs, y + r * ys, color=WHITE, lw=0.6, alpha=0.18, zorder=4)
    for lat in (-60, -30, 0, 30, 60):
        yy = y + r * math.sin(math.radians(lat))
        hw = r * rx * math.cos(math.radians(lat))
        ax.plot([x - hw, x + hw], [yy, yy], color=WHITE, lw=0.6, alpha=0.18, zorder=4)
    ax.add_patch(Ellipse((x, y), 2 * r * rx, 2 * r, fill=False, ec=WHITE, lw=1, alpha=0.35, zorder=5))


def speed_arrows(ax, x, y, r, scale, alpha=0.9, shift=0.0):
    for lat in (-75, -60, -45, -30, -15, 0, 15, 30, 45, 51.5, 60, 75):
        c = math.cos(math.radians(lat))
        yy = y + r * math.sin(math.radians(lat))
        x0 = x + r * c + 0.15 + shift
        L = scale * c
        if L > 0.05:
            col = GOLD if lat == 51.5 else AIR
            ax.add_patch(FancyArrow(x0, yy, L, 0, width=0.04, head_width=0.16, head_length=0.18,
                                    length_includes_head=True, color=col, alpha=alpha, lw=0, zorder=6))


def render_speed(out, seconds, still):
    n, frames = frames_for(seconds, still)
    for i in frames:
        s = ease(i / max(1, n - 1) / 0.5)
        fig, ax = canvas()
        globe(ax, -1.5, 0, 3.2, i / FPS * 0.35)
        speed_arrows(ax, -1.5, 0, 3.2, 3.6 * s)
        save(fig, out, i, still)
    finish(out, still)


def render_bulge(out, seconds, still):
    n, frames = frames_for(seconds, still)
    for i in frames:
        s = ease(i / max(1, n - 1) / 0.6)
        fig, ax = canvas()
        globe(ax, 0, 0, 3.4, i / FPS * 0.35, rx=1 + 0.08 * s)
        ax.add_patch(Circle((0, 0), 3.4, fill=False, ec=DIM, lw=1.2, ls=(0, (5, 5)), alpha=0.6 * s, zorder=6))
        save(fig, out, i, still)
    finish(out, still)


def render_air(out, seconds, still):
    """The globe turns for a moment, then stops dead; the arrows of air keep streaming east and pull away."""
    n, frames = frames_for(seconds, still)
    stop = 0.2
    for i in frames:
        u = i / max(1, n - 1)
        phase = min(u, stop) * seconds * 0.35
        fig, ax = canvas()
        globe(ax, -2.5, 0, 3.2, phase)
        drift = max(0.0, u - stop) * 6.0
        for k in range(3):
            speed_arrows(ax, -2.5, 0, 3.2, 1.6, alpha=0.8 - 0.25 * k, shift=(drift + 1.8 * k) % 5.4)
        save(fig, out, i, still)
    finish(out, still)


def render_oceans(out, seconds, still):
    """Start as a normal blue globe; the sea retreats to two polar caps and a band of land spreads round the middle."""
    n, frames = frames_for(seconds, still, at=0.95)
    for i in frames:
        s = ease(i / max(1, n - 1) / 0.8)
        fig, ax = canvas()
        globe(ax, 0, 0, 3.4, i / FPS * 0.05 * (1 - s))
        band = 3.4 * (0.05 + 0.6 * s)
        ax.add_patch(Ellipse((0, 0), 6.8, 6.8, color=LAND, alpha=0.0, zorder=5))
        ys = np.linspace(-band, band, 80)
        hw = np.sqrt(np.clip(3.4 ** 2 - ys ** 2, 0, None))
        ax.fill_betweenx(ys, -hw, hw, color=LAND, alpha=0.9 * s, lw=0, zorder=6)
        save(fig, out, i, still)
    finish(out, still)


def render_dayyear(out, seconds, still):
    """The Sun at centre; Earth goes once round. The lit half always faces the Sun, but with no spin a fixed marker
    on the surface stays pointing the same way, so it sees half a year of day, then half a year of night."""
    n, frames = frames_for(seconds, still, at=0.4)
    R = 3.3
    for i in frames:
        th = 2 * math.pi * i / max(1, n)
        fig, ax = canvas()
        ax.add_patch(Circle((0, 0), R, fill=False, ec=DIM, lw=1, alpha=0.4))
        for k, a in ((2.2, 0.08), (1.5, 0.2)):
            ax.add_patch(Circle((0, 0), 0.45 * k, color=GOLD, alpha=a, lw=0))
        ax.add_patch(Circle((0, 0), 0.45, color=GOLD))
        ex, ey = R * math.cos(th), R * math.sin(th)
        ax.add_patch(Circle((ex, ey), 0.55, color="#10131c", zorder=5))
        sun_dir = math.degrees(math.atan2(-ey, -ex))
        ax.add_patch(Wedge((ex, ey), 0.55, sun_dir - 90, sun_dir + 90, color=SEA, zorder=6))
        mx, my = ex + 0.55, ey                                   # the marker never turns: it points the same way
        lit = math.cos(math.radians(sun_dir)) > 0
        ax.add_patch(Circle((mx, my), 0.09, color=GOLD if lit else DIM, zorder=7))
        save(fig, out, i, still)
    finish(out, still)


def render_tides(out, seconds, still):
    n, frames = frames_for(seconds, still)
    for i in frames:
        u = i / max(1, n - 1)
        th = 2 * math.pi * u * 1.5
        fig, ax = canvas()
        rm = 3.0 + 0.7 * ease(u)                                   # stays on screen at every angle
        ax.add_patch(Circle((0, 0), rm, fill=False, ec=DIM, lw=1, alpha=0.35))
        bulge = math.degrees(th) + 18                             # the bulge leads the Moon
        ax.add_patch(Ellipse((0, 0), 3.5, 2.9, angle=bulge, color=SEA, alpha=0.45, zorder=3))
        globe(ax, 0, 0, 1.4, i / FPS * 1.2)
        ax.add_patch(Circle((rm * math.cos(th), rm * math.sin(th)), 0.38, color=MOON, zorder=6))
        save(fig, out, i, still)
    finish(out, still)


def render_clock(out, seconds, still):
    """A dial with 22 hour ticks and a hand sweeping once; then the ticks spread and two more appear to make 24."""
    n, frames = frames_for(seconds, still, at=0.95)
    for i in frames:
        u = i / max(1, n - 1)
        s = ease((u - 0.45) / 0.4)
        ticks = 22 + 2 * s
        fig, ax = canvas()
        ax.add_patch(Circle((0, 0), 3.4, fill=False, ec=WHITE, lw=2, alpha=0.8))
        whole = int(math.floor(ticks))
        for k in range(whole + (1 if ticks > whole else 0)):
            a = math.pi / 2 - 2 * math.pi * k / ticks
            al = 1.0 if k < whole else ticks - whole
            ax.plot([3.0 * math.cos(a), 3.35 * math.cos(a)], [3.0 * math.sin(a), 3.35 * math.sin(a)],
                    color=GOLD if k % 6 == 0 else WHITE, lw=3, alpha=0.9 * al)
        h = math.pi / 2 - 2 * math.pi * (u * 1.6 % 1)
        ax.plot([0, 2.7 * math.cos(h)], [0, 2.7 * math.sin(h)], color=GOLD, lw=4)
        ax.add_patch(Circle((0, 0), 0.12, color=GOLD))
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
    jobs = {"speed": (render_speed, 12), "bulge": (render_bulge, 10), "air": (render_air, 14),
            "oceans": (render_oceans, 12), "dayyear": (render_dayyear, 14), "tides": (render_tides, 14),
            "clock": (render_clock, 12)}
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
