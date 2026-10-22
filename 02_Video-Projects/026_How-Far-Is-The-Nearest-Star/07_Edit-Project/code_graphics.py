#!/usr/bin/env python3
"""Code-drawn graphics for the nearest-star film (026 v06, J0794). 1920x1080, 30 fps, PNG frames then MP4.

All diagrams explain step-by-step with the sound off so a school child understands (AGENTS.md lesson 7 & Teach on screen):
  - Lifted dark-navy starfield bed (passes polish_gate near-black & low-detail without needing waivers).
  - Real NASA cut-out discs (Earth Blue Marble e002130, Moon LRO e001982, Sun SDO e000759) + glowing red dwarf Proxima.
  - Step-by-step animation matched to the spoken VO, with labels of at most 4 words from the spoken line.
  - Numbers shown as physical objects (year ticks + growing distance bar, orbit baseline + sight-line shift, grapefruit
    vs pinhead scale bar, London-to-Cairo cherry scale, moving walker/car/jet/Voyager/light objects with time bars,
    and stacked 3-lane Moon/Sun/Proxima light race).

Usage:
  python3 code_graphics.py all code_out_v06/
  python3 code_graphics.py <which> code_out_v06/ [--still] [--seconds N]
"""
import argparse, logging, math, os, subprocess, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#080d1a"
NAVY_CARD = "#142238"
GOLD = "#ffc94a"
YELLOW = "#ffd23f"
WHITE = "#f4efe6"
DIM = "#9aa6b8"
CYAN = "#5fd6ff"
RED = "#ff6a4a"
GREEN = "#6be5a0"
FONT = {"family": ["Arial", "Helvetica", "DejaVu Sans"], "weight": "bold"}
UNIT_PX = W / 16.0

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(HERE, "pool_v01")
EARTH_IMG = "earth_moon/GSFC_20171208_Archive_e002130.jpg"
MOON_IMG = "earth_moon/GSFC_20171208_Archive_e001982.jpg"
SUN_IMG = "sun/GSFC_20171208_Archive_e000759.jpg"
_DISCS = {}
_BEDS = {}
BED_EXT = (-8.2, 8.2, -4.6, 4.6)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, float(t))))


def make_bed(seed, N=1800):
    """Lifted navy starfield bed with subtle grid lines (mean luma ~40, std > 20 so polish_gate passes cleanly)."""
    if seed in _BEDS:
        return _BEDS[seed]
    from PIL import Image, ImageFilter
    rng = np.random.default_rng(seed)
    h, w = 540, 960
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w * 0.50) / (w * 0.60), (yy - h * 0.50) / (h * 0.60))
    g = np.clip(1.0 - r, 0.0, 1.0) ** 1.25
    cloud = Image.fromarray((rng.random((24, 42)) * 255).astype(np.uint8)).resize((w, h), Image.Resampling.BICUBIC)
    cloud = np.asarray(cloud.filter(ImageFilter.GaussianBlur(14)), dtype=float) / 255.0
    k = 0.52 * g + 0.62 * cloud * (0.48 + 0.52 * g)
    edge, centre = np.array([0.06, 0.10, 0.20]), np.array([0.23, 0.34, 0.60])
    img = np.clip(edge + (centre - edge) * k[..., None], 0.0, 1.0)
    st = dict(
        x=rng.uniform(-7.9, 7.9, N),
        y=rng.uniform(-4.4, 4.4, N),
        s=1.2 + 9.0 * rng.uniform(0.0, 1.0, N) ** 3.6,
        a=rng.uniform(0.35, 0.92, N),
    )
    _BEDS[seed] = (img, st)
    return _BEDS[seed]


def canvas(seed=101, grid=True):
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    bed_img, st = make_bed(seed)
    ax.imshow(bed_img, extent=BED_EXT, origin="lower", interpolation="bilinear", zorder=-10)
    rgba = np.column_stack([np.full_like(st["a"], 0.94), np.full_like(st["a"], 0.96), np.ones_like(st["a"]), st["a"]])
    ax.scatter(st["x"], st["y"], s=st["s"], c=rgba, lw=0, zorder=-9)
    if grid:
        for gx in range(-6, 7, 2):
            ax.plot([gx, gx], [-4.5, 4.5], color="#6fa8ff", lw=0.7, alpha=0.10, zorder=-8)
        for gy in range(-3, 4, 2):
            ax.plot([-8.0, 8.0], [gy, gy], color="#6fa8ff", lw=0.7, alpha=0.10, zorder=-8)
    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def disc(rel, px=600, tint=None):
    """Real NASA photo cut out as an RGBA disc with feathered circular edge."""
    key = (rel, tuple(tint) if tint else None)
    if key in _DISCS:
        return _DISCS[key]
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(os.path.join(POOL, rel)).convert("RGB")
    im.thumbnail((2400, 2400))
    a = np.asarray(im, dtype=np.float32) / 255.0
    lit = a.max(axis=2) > 0.08
    rows = np.where(lit.sum(axis=1) > 0.15 * lit.sum(axis=1).max())[0]
    cols = np.where(lit.sum(axis=0) > 0.15 * lit.sum(axis=0).max())[0]
    cy, cx = (rows[0] + rows[-1]) / 2, (cols[0] + cols[-1]) / 2
    r = max(rows[-1] - rows[0], cols[-1] - cols[0]) / 2
    sq = im.crop((round(cx - r), round(cy - r), round(cx + r), round(cy + r))).resize((px, px), Image.Resampling.LANCZOS)
    rgb = np.asarray(sq, dtype=np.float32) / 255.0
    if rel == SUN_IMG:
        lum = np.clip(rgb.max(axis=2, keepdims=True), 0, 1) ** 0.42
        col_vec = np.array(tint or [1.0, 0.90, 0.60], dtype=np.float32)
        rgb = np.clip(0.22 * rgb + 0.88 * lum * col_vec, 0, 1)
    else:
        rgb = np.clip(rgb * 1.08, 0, 1)
    yy, xx = np.mgrid[0:px, 0:px]
    d = np.hypot(xx - (px - 1) / 2, yy - (px - 1) / 2) / (px / 2)
    alpha = np.clip((1.0 - d) / 0.025, 0, 1)
    _DISCS[key] = np.dstack([rgb, alpha])
    return _DISCS[key]


def put_disc(ax, rel, x, y, r, alpha=1.0, z=5, glow_col=None, tint=None):
    if alpha <= 0.01:
        return
    if glow_col:
        for k, ga in ((1.35, 0.12), (1.16, 0.24)):
            ax.add_patch(Circle((x, y), r * k, color=glow_col, alpha=ga * alpha, lw=0, zorder=z - 1))
    img = disc(rel, tint=tint).copy()
    img[..., 3] *= alpha
    ax.imshow(img, extent=(x - r, x + r, y - r, y + r), zorder=z, interpolation="bilinear")


def red_dwarf(ax, x, y, alpha=1.0, scale=1.0, z=5):
    if alpha <= 0.01:
        return
    for r, a in ((0.95, 0.09), (0.60, 0.18), (0.34, 0.34)):
        ax.add_patch(Circle((x, y), r * scale, color=RED, alpha=a * alpha, lw=0, zorder=z - 1))
    ax.add_patch(Circle((x, y), 0.16 * scale, color="#ffd8c8", ec=RED, lw=1.5, alpha=alpha, zorder=z))


def badge(ax, x, y, text, col=WHITE, bg=NAVY_CARD, ec="#4a6fa5", fontsize=36, alpha=1.0, ha="center", pad_w=0.35, pad_h=0.22, z=10):
    """Clean rounded pill label with <= 4 words using matplotlib's exact text bbox sizing."""
    if alpha <= 0.01:
        return
    ax.text(
        x, y, text, color=col, alpha=alpha, fontsize=fontsize, fontdict=FONT, ha=ha, va="center", zorder=z + 1,
        bbox=dict(boxstyle="round,pad=0.30,rounding_size=0.35", facecolor=bg, edgecolor=ec, lw=1.8, alpha=0.90 * alpha),
    )


def pulse(ax, x0, y, x, alpha=1.0, trail=1.6, col=GOLD):
    if alpha <= 0.01:
        return
    t0 = max(x0, x - trail)
    xs = np.linspace(t0, x, 36)
    for k in range(len(xs) - 1):
        f = (k + 1) / len(xs)
        ax.plot(xs[k:k + 2], [y, y], color=col, lw=5, alpha=0.65 * f * f * alpha, solid_capstyle="butt", zorder=6)
    for r, a in ((0.42, 0.14), (0.24, 0.30), (0.12, 0.65)):
        ax.add_patch(Circle((x, y), r, color="#fff3c8", alpha=a * alpha, lw=0, zorder=7))
    ax.add_patch(Circle((x, y), 0.065, color="white", alpha=alpha, zorder=8))


def draw_icon(ax, kind, x, y, col=WHITE, alpha=1.0, scale=1.0, z=8):
    """Simple unmistakable silhouettes for Walk, Car, Jet, Voyager, Light."""
    if alpha <= 0.01:
        return
    s = scale * 0.32
    if kind == "walk":
        # Stick figure mid-stride
        ax.add_patch(Circle((x, y + 0.75 * s), 0.25 * s, color=col, alpha=alpha, zorder=z))
        ax.plot([x, x - 0.05 * s], [y + 0.48 * s, y - 0.15 * s], color=col, lw=3.5, alpha=alpha, zorder=z)
        ax.plot([x - 0.35 * s, x + 0.35 * s], [y + 0.15 * s, y + 0.35 * s], color=col, lw=3.0, alpha=alpha, zorder=z)
        ax.plot([x - 0.05 * s, x - 0.35 * s], [y - 0.15 * s, y - 0.75 * s], color=col, lw=3.2, alpha=alpha, zorder=z)
        ax.plot([x - 0.05 * s, x + 0.32 * s], [y - 0.15 * s, y - 0.75 * s], color=col, lw=3.2, alpha=alpha, zorder=z)
    elif kind == "car":
        # Car body + roof + 2 wheels
        ax.add_patch(FancyBboxPatch((x - 0.85 * s, y - 0.30 * s), 1.7 * s, 0.55 * s,
                                    boxstyle="round,pad=0.02,rounding_size=0.10", facecolor=col, edgecolor="none", alpha=alpha, zorder=z))
        roof = Polygon([(x - 0.50 * s, y + 0.22 * s), (x - 0.25 * s, y + 0.62 * s),
                        (x + 0.35 * s, y + 0.62 * s), (x + 0.60 * s, y + 0.22 * s)],
                       closed=True, facecolor=col, edgecolor="none", alpha=alpha, zorder=z)
        ax.add_patch(roof)
        for wx in (-0.48 * s, 0.48 * s):
            ax.add_patch(Circle((x + wx, y - 0.35 * s), 0.22 * s, color=BG, ec=col, lw=2.5, alpha=alpha, zorder=z + 1))
    elif kind == "jet":
        # Swept-wing jet silhouette pointing right
        pts = [(x + 0.95 * s, y), (x + 0.20 * s, y + 0.18 * s), (x - 0.25 * s, y + 0.85 * s),
               (x - 0.50 * s, y + 0.85 * s), (x - 0.25 * s, y + 0.16 * s), (x - 0.85 * s, y + 0.42 * s),
               (x - 0.95 * s, y + 0.42 * s), (x - 0.75 * s, y),
               (x - 0.95 * s, y - 0.42 * s), (x - 0.85 * s, y - 0.42 * s), (x - 0.25 * s, y - 0.16 * s),
               (x - 0.50 * s, y - 0.85 * s), (x - 0.25 * s, y - 0.85 * s), (x + 0.20 * s, y - 0.18 * s)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=col, edgecolor="none", alpha=alpha, zorder=z))
    elif kind == "voyager":
        # Spacecraft dish + boom
        ax.add_patch(Ellipse((x + 0.15 * s, y), 0.45 * s, 0.95 * s, color=col, alpha=alpha, zorder=z))
        ax.add_patch(Rectangle((x - 0.45 * s, y - 0.22 * s), 0.55 * s, 0.44 * s, color=col, alpha=alpha, zorder=z))
        ax.plot([x + 0.35 * s, x + 0.90 * s], [y, y], color=col, lw=2.5, alpha=alpha, zorder=z)
        ax.plot([x - 0.20 * s, x - 0.95 * s], [y - 0.15 * s, y - 0.70 * s], color=col, lw=2.2, alpha=alpha, zorder=z)
    elif kind == "light":
        for r, a in ((0.75 * s, 0.20), (0.45 * s, 0.45)):
            ax.add_patch(Circle((x, y), r, color=YELLOW, alpha=a * alpha, lw=0, zorder=z))
        ax.add_patch(Circle((x, y), 0.22 * s, color="white", alpha=alpha, zorder=z + 1))


def render_triple(out, seconds, still, mode="a"):
    """mode='a' (Row 4, 20.1-24.6s): 'which star it is' -> highlights Proxima Centauri (Nearest star) looping around
    Alpha Centauri A, B. mode='b' (Row 8, 88.3-92.9s): 'The three are one family. Proxima loops around the bright pair...
    half a million years'."""
    n = int(seconds * FPS)
    t0 = 0.0 if mode == "a" else 28.0
    seed = 401 if mode == "a" else 801
    frames = [int(n * 0.65)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(seed=seed)
        # Orbit ellipse of Proxima around Alpha Cen A & B
        th = np.linspace(0, 2 * math.pi, 320)
        ox, oy = -0.6, -0.15
        rx, ry = 5.8, 2.95
        ax.plot(ox + rx * np.cos(th), oy + ry * np.sin(th), color=CYAN, lw=2.2, alpha=0.45, ls=(0, (5, 5)), zorder=2)

        # Alpha Centauri A & B orbiting their centre of mass
        a = 2 * math.pi * (t0 + t) / 3.6
        ax_a, ay_a = ox + 0.58 * math.cos(a), oy + 0.58 * math.sin(a)
        ax_b, ay_b = ox - 0.72 * math.cos(a), oy - 0.72 * math.sin(a)
        ax.plot(ox + 0.65 * np.cos(th), oy + 0.65 * np.sin(th), color=WHITE, lw=1.2, alpha=0.25, zorder=2)
        put_disc(ax, SUN_IMG, ax_a, ay_a, 0.42, glow_col=GOLD, tint=[1.0, 0.95, 0.75], z=5)
        put_disc(ax, SUN_IMG, ax_b, ay_b, 0.31, glow_col="#ff9e44", tint=[1.0, 0.72, 0.42], z=5)

        # Proxima moving along the outer loop
        ang0 = math.radians(300 if mode == "a" else 155)
        ang = ang0 + 2 * math.pi * t / 24.0
        # Swept trail arc behind Proxima
        arc_th = np.linspace(ang - 0.55, ang, 60)
        ax.plot(ox + rx * np.cos(arc_th), oy + ry * np.sin(arc_th), color=RED, lw=4.5, alpha=0.75, zorder=4)
        px, py = ox + rx * math.cos(ang), oy + ry * math.sin(ang)
        red_dwarf(ax, px, py, scale=1.35, z=6)
        ax.add_patch(Circle((px, py), 0.52, fill=False, ec=YELLOW, lw=2.2, alpha=0.85, zorder=7))

        if mode == "a":
            badge(ax, 0.0, 3.70, "Which star it is", col=YELLOW, fontsize=46, alpha=ease(t / 0.35))
            badge(ax, ox, -1.65, "Alpha Centauri A, B", col=WHITE, fontsize=36, alpha=ease((t - 0.3) / 0.35))
            badge(ax, px - 0.2, py + 1.05, "Proxima Centauri", col=YELLOW, ec=RED, fontsize=40, alpha=ease((t - 0.6) / 0.35))
            badge(ax, px - 0.2, py - 1.05, "Nearest star", col=WHITE, ec=RED, fontsize=36, alpha=ease((t - 1.0) / 0.35))
        else:
            badge(ax, 0.0, 3.70, "One family: 3 stars", col=YELLOW, fontsize=46, alpha=ease(t / 0.35))
            badge(ax, 0.6, -1.60, "Bright pair (A, B)", col=WHITE, fontsize=36, alpha=ease((t - 0.3) / 0.35))
            badge(ax, -3.6, 2.25, "Proxima loops around", col=YELLOW, ec=RED, fontsize=38, alpha=ease((t - 0.6) / 0.35))
            badge(ax, 0.0, -3.65, "Half a million years", col=CYAN, fontsize=42, alpha=ease((t - 1.4) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_lightyear(out, seconds, still, leave=0.5, arrive=8.1):
    """Row 9 (112.20-121.73s, 9.53s): 'It is how far light travels in a year. So when you look towards Proxima, you are
    seeing light that left it more than four years ago.'
    Shows Proxima (left) and real Earth (right), with 4 year marks lighting up one by one ('1 year', '2 years', '3 years',
    '4 years') as the pulse crosses, plus a growing distance bar reaching 'More than 4 years'."""
    n = int(seconds * FPS)
    PX, EX, Y = -5.8, 5.8, 0.35
    ticks = [PX + (EX - PX) * k / 4.24 for k in range(1, 5)]
    tick_times = [leave + (arrive - leave) * (k / 4.24) for k in range(1, 5)]
    tick_labels = ["1 year", "2 years", "3 years", "4 years"]
    frames = [int(n * 0.82)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(seed=901)
        badge(ax, 0.0, 3.65, "Travels in a year", col=WHITE, fontsize=46, alpha=ease(t / 0.35))

        # Guide track between Proxima and Earth
        ax.plot([PX, EX], [Y, Y], color=WHITE, lw=3.0, alpha=0.35, zorder=2)
        s = min(1.0, max(0.0, (t - leave) / (arrive - leave)))
        x = PX + (EX - PX) * s

        # Lit track behind the light pulse
        if t >= leave:
            ax.plot([PX, x], [Y, Y], color=GOLD, lw=5.0, alpha=0.85, zorder=3)

        # Year ticks & step-by-step year labels
        for k, (tx, tt, tlab) in enumerate(zip(ticks, tick_times, tick_labels)):
            lit = x >= tx
            col = YELLOW if lit else "#7a8ba8"
            th = 0.42 if lit else 0.28
            ax.plot([tx, tx], [Y - th, Y + th], color=col, lw=4.5 if lit else 2.5, alpha=1.0 if lit else 0.65, zorder=4)
            if lit:
                a_tick = ease((t - tt) / 0.30)
                ax.add_patch(Circle((tx, Y), 0.16, color=YELLOW, alpha=a_tick, zorder=5))
                ly = Y + (1.15 if k % 2 == 0 else 1.85)
                badge(ax, tx, ly, tlab, col=YELLOW, fontsize=34, alpha=a_tick, pad_w=0.25, pad_h=0.15)

        # Bodies and their names
        red_dwarf(ax, PX, Y, scale=1.45, z=6)
        put_disc(ax, EARTH_IMG, EX, Y, 0.68, glow_col="#4ea2ff", z=6)
        badge(ax, PX, Y - 1.35, "Proxima", col=RED, fontsize=38, alpha=ease(t / 0.35))
        badge(ax, EX, Y - 1.35, "Earth", col=CYAN, fontsize=38, alpha=ease(t / 0.35))

        if t >= leave:
            fade = 1.0 - ease((t - arrive) / 0.5) if t > arrive else 1.0
            pulse(ax, PX, Y, min(x, EX - 0.5), alpha=fade, trail=1.8)
        if t > arrive:
            g = 1.0 - ease((t - arrive) / 1.1)
            ax.add_patch(Circle((EX, Y), 1.05, color="#fff3c8", alpha=0.35 * g, lw=0, zorder=9))

        # Bottom growing distance bar (number as object)
        bar_y, bar_h = -2.65, 0.52
        ax.add_patch(FancyBboxPatch((PX, bar_y - bar_h / 2), EX - PX, bar_h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor="#101a2e", edgecolor="#3b5988", lw=1.8, alpha=0.9, zorder=3))
        if s > 0.01:
            ax.add_patch(FancyBboxPatch((PX, bar_y - bar_h / 2), (EX - PX) * s, bar_h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                        facecolor=GOLD, edgecolor="none", alpha=0.85, zorder=4))
        if t >= 7.2:
            badge(ax, 0.0, -3.65, "More than 4 years", col=YELLOW, ec=GOLD, fontsize=48, alpha=ease((t - 7.2) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_parallax(out, seconds, still, mode="a"):
    """mode='a' (Row 12, 143.87-148.67s, 4.8s): Earth on its orbit around the Sun (January -> July), sight-line pivoting
    across the Nearby star so it shifts against Distant stars.
    mode='b' (Row 14, 181.70-186.63s, 4.93s): Friedrich Bessel 1838 parallax measurement of 61 Cygni (kept in upper frame
    above y=-1.4 so the lower-third 1838 WHEN and Bessel WHO cards have clear space)."""
    n = int(seconds * FPS)
    seed = 1201 if mode == "a" else 1401
    frames = [int(n * 0.75)] if still else range(n)
    for i in frames:
        t = i / FPS
        s = ease((t - 0.25) / max(0.5, seconds - 0.8))
        fig, ax = canvas(seed=seed)

        if mode == "a":
            sx, sy = -4.6, -0.2
            orx, ory = 1.45, 2.15
            nx, ny = 0.2, -0.2
            wall_x = 5.6

            badge(ax, 0.0, 3.65, "Whole of Earth's orbit", col=YELLOW, fontsize=46, alpha=ease(t / 0.35))

            # Earth's orbit ellipse around real Sun
            th = np.linspace(0, 2 * math.pi, 240)
            ax.plot(sx + orx * np.cos(th), sy + ory * np.sin(th), color=CYAN, lw=2.5, alpha=0.65, ls=(0, (5, 4)), zorder=3)
            put_disc(ax, SUN_IMG, sx, sy, 0.58, glow_col=GOLD, z=5)
            badge(ax, sx, sy - 2.85, "Earth's orbit", col=CYAN, fontsize=36, alpha=ease(t / 0.35))

            # January (top) & July (bottom) markers, and Earth moving from Jan (pi/2) to Jul (-pi/2)
            ang = math.pi / 2 - math.pi * s
            ex, ey = sx + orx * math.cos(ang), sy + ory * math.sin(ang)
            ax.add_patch(Circle((sx, sy + ory), 0.12, color=WHITE, alpha=0.7, zorder=4))
            ax.add_patch(Circle((sx, sy - ory), 0.12, color=WHITE, alpha=0.7, zorder=4))
            badge(ax, sx - 1.9, sy + ory, "January", col=WHITE, fontsize=32, alpha=ease((t - 0.2) / 0.3), pad_w=0.22, pad_h=0.14)
            badge(ax, sx - 1.7, sy - ory, "July", col=WHITE, fontsize=32, alpha=ease((t - 0.6) / 0.3), pad_w=0.22, pad_h=0.14)
            put_disc(ax, EARTH_IMG, ex, ey, 0.36, glow_col="#4ea2ff", z=7)

            # Distant stars wall on the right
            ax.plot([wall_x, wall_x], [-3.1, 2.7], color=DIM, lw=2.0, alpha=0.45, ls=(0, (3, 4)), zorder=2)
            for wy in (-2.5, -1.5, -0.5, 0.5, 1.5, 2.3):
                ax.scatter([wall_x + 0.25], [wy], s=55, color=WHITE, alpha=0.85, zorder=3)
            badge(ax, wall_x - 0.2, 3.05, "Distant stars", col=WHITE, fontsize=34, alpha=ease((t - 0.3) / 0.35))

            # Sight-line from Earth through Nearby star to Distant stars wall
            slope = (ny - ey) / (nx - ex)
            proj_y = ey + slope * (wall_x - ex)
            # Ghost January sight-line
            slope_jan = (ny - (sy + ory)) / (nx - sx)
            proj_jan = (sy + ory) + slope_jan * (wall_x - sx)
            ax.plot([sx, wall_x], [sy + ory, proj_jan], color=WHITE, lw=1.6, alpha=0.28, ls="--", zorder=3)
            ax.add_patch(Circle((wall_x, proj_jan), 0.14, color=RED, alpha=0.35, zorder=4))

            # Live sight-line & apparent shifted position on background
            ax.plot([ex, wall_x], [ey, proj_y], color=YELLOW, lw=3.0, alpha=0.90, zorder=5)
            red_dwarf(ax, nx, ny, scale=1.15, z=6)
            badge(ax, nx, ny + 1.15, "Nearby star shifts", col=YELLOW, ec=RED, fontsize=36, alpha=ease((t - 0.5) / 0.35))

            # Apparent shift arrow on background wall
            ax.add_patch(Circle((wall_x, proj_y), 0.20, color=RED, ec=YELLOW, lw=2.0, zorder=7))
            if abs(proj_y - proj_jan) > 0.15:
                ax.annotate("", xy=(wall_x + 0.55, proj_y), xytext=(wall_x + 0.55, proj_jan),
                            arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=3.0), zorder=8)
        else:
            # Row 14 (Bessel 1838 / 61 Cygni): kept in upper band y in [-1.1, 3.9] above lower-third cards
            sx, sy = -5.0, 1.15
            orx, ory = 1.15, 1.65
            nx, ny = 4.2, 1.15

            badge(ax, 0.0, 3.70, "First star measured", col=YELLOW, fontsize=44, alpha=ease(t / 0.35))

            th = np.linspace(0, 2 * math.pi, 240)
            ax.plot(sx + orx * np.cos(th), sy + ory * np.sin(th), color=CYAN, lw=2.4, alpha=0.65, ls=(0, (5, 4)), zorder=3)
            put_disc(ax, SUN_IMG, sx, sy, 0.48, glow_col=GOLD, z=5)
            ang = math.pi / 2 - math.pi * s
            ex, ey = sx + orx * math.cos(ang), sy + ory * math.sin(ang)
            put_disc(ax, EARTH_IMG, ex, ey, 0.32, glow_col="#4ea2ff", z=7)
            badge(ax, sx, sy - 2.15, "Earth's orbit", col=CYAN, fontsize=34, alpha=ease(t / 0.35))

            # Sight-lines from top and bottom of Earth's orbit to 61 Cygni
            ax.plot([sx, nx], [sy + ory, ny], color=GOLD, lw=2.6, alpha=0.80, zorder=4)
            ax.plot([sx, nx], [sy - ory, ny], color=GOLD, lw=2.6, alpha=0.80, zorder=4)
            ax.plot([ex, nx], [ey, ny], color=YELLOW, lw=3.2, alpha=0.95, zorder=5)

            # 61 Cygni binary pair
            put_disc(ax, SUN_IMG, nx - 0.14, ny + 0.10, 0.26, glow_col="#ff9e44", tint=[1.0, 0.78, 0.48], z=6)
            put_disc(ax, SUN_IMG, nx + 0.16, ny - 0.10, 0.22, glow_col="#ff9e44", tint=[1.0, 0.72, 0.42], z=6)
            badge(ax, nx, ny - 1.15, "Star: 61 Cygni", col=YELLOW, fontsize=36, alpha=ease((t - 0.4) / 0.35))
            badge(ax, -0.3, 2.35, "Tiny shift measured", col=WHITE, ec=GOLD, fontsize=34, alpha=ease((t - 0.8) / 0.35))

        save(fig, out, i, still)
    finish(out, still)


def render_scale(out, seconds, still, mode="a"):
    """mode='a' (Row 18, 239.47-246.47s, 7.0s): Beat 1 (0-4.07s) 'Make the Sun the size of a grapefruit and put it on a
    table.' Beat 2 (4.07-7.0s) 'At that scale, Earth is a pinhead' (+ 15 meters scale bar).
    mode='b' (Row 21, 282.07-286.63s, 4.6s): Grapefruit Sun in London -> Cherry Proxima at 4,000 km (further than Cairo)
    + Alpha Centauri A & B (big grapefruit & orange)."""
    n = int(seconds * FPS)
    seed = 1801 if mode == "a" else 2101
    frames = [int(n * 0.82)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(seed=seed)

        if mode == "a":
            sx, sy, sr = -4.6, 0.25, 1.35
            ex, ey = 4.8, 0.25

            # Grapefruit Sun on left
            put_disc(ax, SUN_IMG, sx, sy, sr, glow_col=GOLD, z=5)
            badge(ax, sx, sy + 2.15, "Sun: a grapefruit", col=YELLOW, fontsize=42, alpha=ease(t / 0.35))
            badge(ax, sx, sy - 2.05, "14 cm across", col=WHITE, fontsize=34, alpha=ease((t - 0.4) / 0.35))

            # Beat 2: pinhead Earth + 15 meters scale bar
            b2 = ease((t - 3.6) / 0.8)
            if b2 > 0.01:
                bar_x0, bar_x1 = sx + sr + 0.3, ex - 0.25
                bx = bar_x0 + (bar_x1 - bar_x0) * b2
                ax.plot([bar_x0, bx], [sy, sy], color=CYAN, lw=4.0, alpha=0.9 * b2, zorder=4)
                ax.plot([bar_x0, bar_x0], [sy - 0.25, sy + 0.25], color=CYAN, lw=3.5, alpha=0.9 * b2, zorder=4)
                ax.plot([bx, bx], [sy - 0.25, sy + 0.25], color=CYAN, lw=3.5, alpha=0.9 * b2, zorder=4)
                badge(ax, (bar_x0 + bar_x1) / 2, sy + 0.85, "About 15 meters", col=CYAN, fontsize=38, alpha=b2)

                # Pinhead speck at ex, ey + magnifier ring above showing real Blue Marble Earth
                ax.add_patch(Circle((ex, ey), 0.055, color="#8ec5ff", alpha=b2, zorder=7))
                ax.add_patch(Circle((ex, ey), 0.22, fill=False, ec=CYAN, lw=2.0, alpha=b2, zorder=6))
                # Magnifier inset circle
                mag_y = sy + 1.55
                ax.plot([ex, ex], [ey + 0.22, mag_y - 0.55], color=CYAN, lw=2.0, alpha=0.8 * b2, ls="--", zorder=5)
                ax.add_patch(Circle((ex, mag_y), 0.55, facecolor="#0c1629", edgecolor=CYAN, lw=2.5, alpha=b2, zorder=6))
                put_disc(ax, EARTH_IMG, ex, mag_y, 0.44, alpha=b2, z=7)
                badge(ax, ex, sy - 1.15, "Earth: a pinhead", col=YELLOW, fontsize=40, alpha=b2)
                badge(ax, ex, sy - 1.95, "1.3 mm wide", col=WHITE, fontsize=32, alpha=b2)
        else:
            # Row 21: London (Sun grapefruit) -> 4,000 km -> Proxima (cherry) + Alpha Cen A (big grapefruit) & B (orange)
            badge(ax, 0.0, 3.65, "About 4,000 kilometers", col=YELLOW, fontsize=46, alpha=ease(t / 0.35))

            sx, sy = -5.8, -0.25
            put_disc(ax, SUN_IMG, sx, sy, 0.80, glow_col=GOLD, z=5)
            badge(ax, sx, sy - 1.35, "Sun: grapefruit", col=WHITE, fontsize=30, alpha=ease(t / 0.35))
            badge(ax, sx, sy - 2.15, "In London", col=CYAN, fontsize=30, alpha=ease(t / 0.35))

            # Animated distance arc from London (-4.7) to Proxima (0.8)
            arc_s = ease((t - 0.2) / 1.0)
            xs = np.linspace(-4.7, 0.4 * arc_s + -4.7 * (1 - arc_s), 50)
            ys = sy + 0.85 * np.sin(np.pi * (xs - (-4.7)) / 5.1)
            ax.plot(xs, ys, color=GOLD, lw=3.5, alpha=0.85, ls=(0, (6, 4)), zorder=4)
            badge(ax, -2.1, sy + 1.55, "Further than Cairo", col=GOLD, fontsize=32, alpha=arc_s)

            # Proxima (cherry, 2.1 cm)
            px, py = 0.8, -0.25
            red_dwarf(ax, px, py, scale=0.85, z=6)
            badge(ax, px, py - 1.35, "Proxima: cherry", col=RED, fontsize=32, alpha=ease((t - 0.3) / 0.35))

            # Alpha Centauri A (big grapefruit, 17 cm) and B (orange, 12 cm)
            a_ab = ease((t - 0.5) / 0.45)
            ax_a, ay_a = 4.3, 0.45
            ax_b, ay_b = 5.7, -0.60
            put_disc(ax, SUN_IMG, ax_a, ay_a, 0.98, alpha=a_ab, glow_col=GOLD, tint=[1.0, 0.95, 0.75], z=5)
            put_disc(ax, SUN_IMG, ax_b, ay_b, 0.68, alpha=a_ab, glow_col="#ff9e44", tint=[1.0, 0.70, 0.38], z=5)
            badge(ax, 4.8, 2.05, "Big grapefruit (A)", col=YELLOW, fontsize=32, alpha=a_ab)
            badge(ax, 5.0, -2.00, "More like an orange", col="#ffb35c", fontsize=32, alpha=ease((t - 1.2) / 0.4))

        save(fig, out, i, still)
    finish(out, still)


def render_journey(out, seconds, still, stage="all"):
    """Five lanes from Earth/Sun (left) to Proxima (right) with moving vehicle/walker icons, growing comparison bars,
    and <=4-word VO labels:
      stage='intro' (Row 4, 28.73-33.13s): preview of the 5 lanes & 'How long it takes'
      stage='car'   (Row 24 cut 70, 323.63-329.13s): Walk (900 million years) + Car (46 million years)
      stage='jet'   (Row 24 cut 72, 332.10-336.57s): adds Jet (5 million years)
      stage='full'  (Row 25 cut 76, 349.73-354.73s): adds Voyager 1 (75,000 years) + Light (4.24 years)
    """
    n = int(seconds * FPS)
    seed = {"intro": 403, "car": 2401, "jet": 2402, "full": 2501}.get(stage, 2401)
    lanes = [
        ("walk", "Walk: 900 million years", "Walk", WHITE, 0.42),
        ("car", "Car: 46 million years", "Car", CYAN, 0.52),
        ("jet", "Jet: 5 million years", "Jet", "#7fe3ff", 0.64),
        ("voyager", "Voyager: 75,000 years", "Voyager 1", "#ffa64d", 0.78),
        ("light", "Light: 4.24 years", "Light", YELLOW, 1.00),
    ]
    max_lanes = {"intro": 5, "car": 2, "jet": 3, "full": 5}.get(stage, 5)
    X0, X1 = -5.2, 5.5
    frames = [int(n * 0.85)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(seed=seed)

        title_txt = "How long it takes" if stage == "intro" else "Journey to Proxima"
        badge(ax, 0.0, 3.75, title_txt, col=YELLOW, fontsize=42, alpha=ease(t / 0.35))

        # Left start (Earth) and Right finish (Proxima) headers
        put_disc(ax, EARTH_IMG, X0 - 1.45, 0.0, 0.52, glow_col="#4ea2ff", z=5)
        badge(ax, X0 - 1.45, -1.05, "Earth", col=CYAN, fontsize=30)
        red_dwarf(ax, X1 + 1.25, 0.0, scale=1.2, z=5)
        badge(ax, X1 + 1.25, -1.05, "Proxima", col=RED, fontsize=30)

        for k in range(max_lanes):
            kind, full_lab, short_lab, col, reach = lanes[k]
            y = 2.40 - k * 1.26
            is_new = (stage == "intro") or (stage == "car" and k == 1) or (stage == "jet" and k == 2) or (stage == "full" and k >= 3)
            delay = (k * 0.25) if stage == "intro" else (0.15 if not is_new else (0.25 + (k - 3) * 0.9 if stage == "full" else 0.25))
            a = ease((t - delay) / 0.35)
            if a <= 0.01:
                continue

            # Track background
            ax.add_patch(FancyBboxPatch((X0, y - 0.26), X1 - X0, 0.52, boxstyle="round,pad=0.01,rounding_size=0.12",
                                        facecolor="#101a2e", edgecolor="#34507a", lw=1.5, alpha=0.85 * a, zorder=2))

            # Animated progress along the lane
            prog = ease((t - delay) / max(0.8, seconds - delay - 0.4)) if is_new else 1.0
            span = (X1 - X0) * reach * (0.45 + 0.55 * prog if kind != "light" else prog)
            ax.add_patch(FancyBboxPatch((X0, y - 0.23), max(0.20, span), 0.46, boxstyle="round,pad=0.01,rounding_size=0.10",
                                        facecolor=col, edgecolor="none", alpha=0.35 * a if kind != "light" else 0.72 * a, zorder=3))

            # Moving object icon placed just past the right tip of the bar (never overlapping left-aligned text)
            ix = min(X1 - 0.35, X0 + max(2.2 if stage == "intro" else 4.9, span) + 0.38)
            draw_icon(ax, kind, ix, y, col=col if kind != "light" else YELLOW, alpha=a, scale=1.25, z=9)

            # Label left-aligned inside the lane
            lab = short_lab if stage == "intro" else full_lab
            badge(ax, X0 + 0.20, y, lab, col=YELLOW if is_new and stage != "intro" else WHITE,
                  bg="#0d172a", ec=col, fontsize=28, alpha=a, ha="left", z=8)

        save(fig, out, i, still)
    finish(out, still)


def render_lightrace(out, seconds, still):
    """Row 27 (361.80-378.53s, 16.8s): Three stacked horizontal lanes that build in turn and stay on screen side by side:
      Lane 1 (Moon -> Earth): 'Just over a second'
      Lane 2 (Sun -> Earth):  'About 8 minutes'
      Lane 3 (Proxima -> Earth): 'More than 4 years' (with 4 year ticks)
    """
    n = int(seconds * FPS)
    SX, EX = -5.6, 5.6
    lanes = [
        ("Moon", MOON_IMG, 0.42, 2.25, 1.8, 3.1, 4.3, 4.4, "Just over a second", CYAN),
        ("Sun", SUN_IMG, 0.68, -0.05, 5.7, 6.4, 9.4, 7.6, "About 8 minutes", GOLD),
        ("Proxima", None, 0.48, -2.35, 9.5, 10.2, None, 11.2, "More than 4 years", RED),
    ]
    frames = [int(n * 0.82)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(seed=2701)
        badge(ax, 0.0, 3.75, "Light travel time", col=YELLOW, fontsize=46, alpha=ease(t / 0.35))

        for name, img_rel, r_body, y, fin, leave, arrive, lab_in, lab_txt, col in lanes:
            a = ease((t - fin) / 0.45)
            if a <= 0.01:
                continue
            x0, x1 = SX + 0.85, EX - 0.85
            ax.plot([x0, x1], [y, y], color=WHITE, lw=2.5, alpha=0.32 * a, zorder=2)

            # Source body on left + label
            if img_rel:
                put_disc(ax, img_rel, SX, y, r_body, alpha=a, glow_col=col, z=5)
            else:
                red_dwarf(ax, SX, y, alpha=a, scale=1.25, z=5)
                for k in range(1, 5):
                    tx = x0 + (x1 - x0) * (k / 4.24)
                    ax.plot([tx, tx], [y - 0.22, y + 0.22], color=DIM, lw=2.2, alpha=0.7 * a, zorder=3)
            badge(ax, SX, y - 0.92, name, col=col, fontsize=30, alpha=a, pad_w=0.20, pad_h=0.10)

            # Destination Earth on right + label
            put_disc(ax, EARTH_IMG, EX, y, 0.52, alpha=a, glow_col="#4ea2ff", z=5)
            if name == "Moon":
                badge(ax, EX, y + 0.92, "Earth", col=CYAN, fontsize=30, alpha=a, pad_w=0.20, pad_h=0.10)

            # Pulse movement
            if t >= leave:
                if arrive is not None:
                    s = min(1.0, (t - leave) / (arrive - leave))
                    px = x0 + (x1 - x0) * s
                    ax.plot([x0, px], [y, y], color=GOLD, lw=5.0, alpha=0.85 * a, zorder=4)
                    if t <= arrive + 0.4:
                        pulse(ax, x0, y, px, alpha=a * (1.0 - ease((t - arrive) / 0.4) if t > arrive else 1.0))
                    if t >= arrive:
                        ax.add_patch(Circle((EX, y), 0.65, fill=False, ec=YELLOW, lw=2.5, alpha=0.8 * a, zorder=7))
                else:
                    # Proxima crawls slowly across the first year tick
                    crawl = min(0.24, 0.24 * (t - leave) / max(0.5, seconds - leave))
                    px = x0 + (x1 - x0) * crawl
                    ax.plot([x0, px], [y, y], color=GOLD, lw=5.5, alpha=0.95 * a, zorder=4)
                    pulse(ax, x0, y, px, alpha=a, trail=0.8)

            # Time badge over the centre of the lane
            a_lab = ease((t - lab_in) / 0.4)
            if a_lab > 0.01:
                badge(ax, 0.0, y + 0.55, lab_txt, col=YELLOW, ec=col, fontsize=38, alpha=a * a_lab, pad_w=0.30, pad_h=0.14)

        save(fig, out, i, still)
    finish(out, still)


def save(fig, out, i, still):
    os.makedirs(out, exist_ok=True)
    fig.savefig(os.path.join(out, "still.png" if still else f"{i:04d}.png"), facecolor=BG)
    plt.close(fig)


def finish(out, still):
    if still:
        print("wrote", os.path.join(out, "still.png"), flush=True)
        return
    mp4 = out.rstrip("/") + ".mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(out, "%04d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", mp4],
        check=True,
    )
    print("wrote", mp4, flush=True)


JOBS = {
    "triple": (lambda o, s, st: render_triple(o, s, st, mode="a"), 6.0),
    "triple_b": (lambda o, s, st: render_triple(o, s, st, mode="b"), 6.0),
    "lightyear": (render_lightyear, 10.2),
    "parallax_a": (lambda o, s, st: render_parallax(o, s, st, mode="a"), 6.0),
    "parallax_b": (lambda o, s, st: render_parallax(o, s, st, mode="b"), 6.0),
    "scale_a": (lambda o, s, st: render_scale(o, s, st, mode="a"), 7.6),
    "scale_b": (lambda o, s, st: render_scale(o, s, st, mode="b"), 5.5),
    "journey_a": (lambda o, s, st: render_journey(o, s, st, stage="intro"), 5.5),
    "journey_b": (lambda o, s, st: render_journey(o, s, st, stage="car"), 6.2),
    "journey_c": (lambda o, s, st: render_journey(o, s, st, stage="jet"), 5.2),
    "journey_d": (lambda o, s, st: render_journey(o, s, st, stage="full"), 5.8),
    "lightrace": (render_lightrace, 17.5),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=[*JOBS.keys(), "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    names = list(JOBS.keys()) if a.which == "all" else [a.which]
    if not a.still and len(names) > 1:
        from concurrent.futures import ProcessPoolExecutor
        procs = []
        for name in names:
            _, secs = JOBS[name]
            cmd = [sys.executable, os.path.abspath(__file__), name, a.out, "--seconds", str(a.seconds or secs)]
            procs.append((name, subprocess.Popen(cmd)))
        for name, p in procs:
            if p.wait() != 0:
                raise SystemExit(f"failed rendering {name}")
        return 0
    for name in names:
        fn, secs = JOBS[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)
    return 0


if __name__ == "__main__":
    sys.exit(main())
