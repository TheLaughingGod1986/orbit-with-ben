#!/usr/bin/env python3
"""Code-drawn graphics for the light-speed film (024 v06, J0792). 1920x1080, 30 fps.

All diagrams explain with the sound off (AGENTS.md lesson 7 & Teach on screen):
  - Real NASA Blue Marble Earth cut-out disc (`GSFC_20171208_Archive_e002130.jpg`).
  - Moving spacecraft outline with engine plume so the viewer sees the ship vs Earth.
  - Short labels (at most 4 words, taken from the spoken VO line) in large house type.
  - Numbers shown as animated objects (growing bars, tick counters, distance bars).
"""
import argparse, math, os, subprocess, sys
import logging
import numpy as np
import matplotlib
matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
YELLOW = "#ffd23f"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
CYAN = "#5fd6ff"
RED = "#ff6a4a"
FONT = {"family": ["Arial", "Helvetica", "DejaVu Sans"], "weight": "bold"}
UNIT_PX = W / 16.0

HERE = os.path.dirname(os.path.abspath(__file__))
EARTH_IMG = os.path.join(HERE, "nasa_pool_v01/024_harvest_v01/GSFC_20171208_Archive_e002130.jpg")
_DISCS = {}


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, float(t))))


VARIANTS = {
    "a": dict(seed=101, gold="#ffc94a", cyan="#5fd6ff", cam=((0.0, 0.0, 1.04), (0.20, 0.08, 0.94))),
    "b": dict(seed=202, gold="#ffa64d", cyan="#6ff0c0", cam=((-0.25, 0.06, 0.96), (0.25, -0.06, 0.96))),
    "c": dict(seed=303, gold="#ffe27a", cyan="#7fe3ff", cam=((0.18, -0.10, 0.94), (0.0, 0.0, 1.04))),
    "d": dict(seed=404, gold="#ffb870", cyan="#7cc8ff", cam=((0.22, 0.10, 1.02), (-0.18, -0.08, 0.94))),
    "e": dict(seed=505, gold="#ffd36b", cyan="#7fe3ff", cam=((-0.18, -0.10, 0.94), (0.22, 0.10, 1.02))),
    "f": dict(seed=606, gold="#ffb870", cyan="#9cf5d4", cam=((0.25, -0.06, 1.00), (-0.22, 0.08, 0.94))),
    "g": dict(seed=707, gold="#fff09a", cyan="#8ab8ff", cam=((0.0, 0.15, 0.95), (0.12, -0.12, 1.03))),
    "h": dict(seed=808, gold="#ffab9a", cyan="#8ab8ff", cam=((-0.22, 0.06, 1.03), (0.18, -0.06, 0.94))),
    "i": dict(seed=909, gold="#ffc6e8", cyan="#b9f7a6", cam=((0.20, 0.12, 1.02), (-0.15, -0.10, 0.92))),
}
VARIANT_COLOURS = {("twinclocks", "e"): dict(gold="#ff8fd0", cyan="#a6ff9a")}
BED_STARS = dict(lightclock=900, energy=2400)
ZMIN = dict(starfield=0.75, lightclock=0.94, energy=0.95, muons=0.98, gpsclocks=0.96, mapdrift=0.94,
            gammaclocks=0.97, twinclocks=0.95, contraction=0.95)
STYLE = dict(on=False, name="", var="a", cam=((0, 0, 1), (0, 0, 1)), bed=None, stars=None, seed=101)
BED_EXT = (-11.0, 11.0, -6.5, 6.5)


def make_bed(seed, stars=True, N=2600):
    """Lifted navy bed: radial gradient with soft cloud texture and background stars (mean luma ~42, std > 20)."""
    from PIL import Image, ImageFilter
    rng = np.random.default_rng(seed)
    h, w = 650, 1100
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w * 0.52) / (w * 0.58), (yy - h * 0.48) / (h * 0.58))
    g = np.clip(1 - r, 0, 1) ** 1.25
    cloud = Image.fromarray((rng.random((28, 48)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    cloud = np.asarray(cloud.filter(ImageFilter.GaussianBlur(16)), dtype=float) / 255
    k = 0.52 * g + 0.65 * cloud * (0.5 + 0.5 * g)
    edge, centre = np.array([0.05, 0.08, 0.18]), np.array([0.25, 0.36, 0.64])
    img = edge + (centre - edge) * k[..., None]
    st = None
    if stars:
        st = dict(x=rng.uniform(BED_EXT[0], BED_EXT[1], N), y=rng.uniform(BED_EXT[2], BED_EXT[3], N),
                  s=1.2 + 10 * rng.uniform(0, 1, N) ** 3.8, a=rng.uniform(0.4, 0.95, N))
    return np.clip(img, 0, 1), st


def view(p):
    (x0, y0, z0), (x1, y1, z1) = STYLE["cam"]
    e = ease(p)
    zmin = ZMIN.get(STYLE["name"], 0.94)
    z = max(z0 + (z1 - z0) * e, zmin)
    m = max(0.02, 1.04 - z)
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
            rgba = np.column_stack([np.full_like(st["a"], 0.93), np.full_like(st["a"], 0.95), np.ones_like(st["a"]), st["a"]])
            ax.scatter(st["x"], st["y"], s=st["s"], c=rgba, lw=0, zorder=-9)
    ax.set_xlim(cx - 8 * z, cx + 8 * z)
    ax.set_ylim(cy - 4.5 * z, cy + 4.5 * z)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def disc(path=EARTH_IMG, px=600):
    """Real NASA photo cut out as an RGBA disc with feathered circular edge."""
    if path in _DISCS:
        return _DISCS[path]
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path).convert("RGB")
    im.thumbnail((2400, 2400))
    a = np.asarray(im, dtype=np.float32) / 255.0
    lit = a.max(axis=2) > 0.08
    rows = np.where(lit.sum(axis=1) > 0.15 * lit.sum(axis=1).max())[0]
    cols = np.where(lit.sum(axis=0) > 0.15 * lit.sum(axis=0).max())[0]
    cy, cx = (rows[0] + rows[-1]) / 2, (cols[0] + cols[-1]) / 2
    r = max(rows[-1] - rows[0], cols[-1] - cols[0]) / 2
    sq = im.crop((round(cx - r), round(cy - r), round(cx + r), round(cy + r))).resize((px, px), Image.Resampling.LANCZOS)
    rgb = np.clip(np.asarray(sq, dtype=np.float32) / 255.0 * 1.08, 0, 1)
    yy, xx = np.mgrid[0:px, 0:px]
    d = np.hypot(xx - (px - 1) / 2, yy - (px - 1) / 2) / (px / 2)
    alpha = np.clip((1.0 - d) / 0.025, 0, 1)
    _DISCS[path] = np.dstack([rgb, alpha])
    return _DISCS[path]


def put_earth(ax, x, y, r, alpha=1.0, z=5):
    if alpha <= 0.01:
        return
    ax.add_patch(Circle((x, y), r * 1.18, color="#4ea2ff", alpha=0.18 * alpha, lw=0, zorder=z - 1))
    img = disc(EARTH_IMG).copy()
    img[..., 3] *= alpha
    ax.imshow(img, extent=(x - r, x + r, y - r, y + r), zorder=z, interpolation="bilinear")


def draw_ship(ax, x, y, scale=1.0, angle_deg=0.0, col=GOLD, thrust=True, alpha=1.0, z=6):
    """Clean spacecraft silhouette with nose cone, fins, viewport, and engine plume."""
    if alpha <= 0.01:
        return
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)

    def rot(pts):
        out = []
        for px, py in pts:
            px, py = px * scale, py * scale
            out.append((x + px * ca - py * sa, y + px * sa + py * ca))
        return out

    if thrust:
        plume = rot([(-0.55, 0.16), (-1.25, 0.0), (-0.55, -0.16)])
        ax.add_patch(Polygon(plume, closed=True, facecolor="#ff8833", edgecolor="none", alpha=0.65 * alpha, zorder=z - 1))
        core = rot([(-0.52, 0.09), (-0.95, 0.0), (-0.52, -0.09)])
        ax.add_patch(Polygon(core, closed=True, facecolor=YELLOW, edgecolor="none", alpha=0.9 * alpha, zorder=z))
    fins = rot([(-0.50, 0.42), (-0.15, 0.22), (-0.15, -0.22), (-0.50, -0.42), (-0.38, 0.0)])
    ax.add_patch(Polygon(fins, closed=True, facecolor= col, edgecolor=WHITE, lw=1.5, alpha=0.9 * alpha, zorder=z))
    hull = rot([(-0.48, 0.22), (0.28, 0.22), (0.68, 0.0), (0.28, -0.22), (-0.48, -0.22)])
    ax.add_patch(Polygon(hull, closed=True, facecolor="#e8eef5", edgecolor=col, lw=2.5, alpha=alpha, zorder=z + 1))
    wx, wy = rot([(0.12, 0.0)])[0]
    ax.add_patch(Circle((wx, wy), 0.11 * scale, facecolor=CYAN, edgecolor="#162238", lw=1.5, alpha=alpha, zorder=z + 2))


def pill_text(ax, x, y, text, col=WHITE, bg="#142034", ec=None, pt=36, alpha=1.0, pad_x=0.38, pad_y=0.22, z=12):
    """House-style rounded pill label (<=4 words) with high-contrast backing."""
    if alpha <= 0.01 or not text:
        return
    w_est = max(1.4, len(text) * (pt / 42.0) * 0.34 + 2 * pad_x)
    h_est = (pt / 42.0) * 0.56 + 2 * pad_y
    box = FancyBboxPatch((x - w_est / 2, y - h_est / 2), w_est, h_est,
                         boxstyle="round,pad=0.04,rounding_size=0.22",
                         facecolor=bg, edgecolor=ec or col, linewidth=2.0 if ec else 1.2,
                         alpha=0.88 * alpha, zorder=z)
    ax.add_patch(box)
    ax.text(x, y, text, color=col, fontsize=pt, fontdict=FONT, ha="center", va="center", alpha=alpha, zorder=z + 1)


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
    th = np.arccos(v[:, 2])
    ph = np.arctan2(v[:, 1], v[:, 0])
    mag = rng.uniform(0.2, 1.0, N) ** 3
    f = 7.0 / math.tan(math.radians(55))
    var = STYLE.get("var", "")
    frames = [int(n * 0.6)] if still else range(n)
    for i in frames:
        t = i / FPS
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
        if var == "e":
            # Row 24 (4:19.4–4:29.1, offset 0.50 s -> t in [0.5, 10.2]):
            # "The stars ahead crowd together and shift towards blue. The stars behind thin out and fade to red."
            # Left side: forward window (blue-shifted, crowded); Right side: rear view (red-shifted, thinned out)
            vis_f = (np.abs(x) < 3.6) & (np.abs(y) < 3.8)
            ax.scatter(x[vis_f] - 3.7, y[vis_f], s=s[vis_f] * 1.1, c=doppler_colour(np.maximum(D[front][vis_f], 1.8)),
                       lw=0, alpha=0.95)
            ax.add_patch(Circle((-3.7, 0.0), 3.3, fill=False, ec="#5fd6ff", lw=3.5, alpha=0.85, zorder=6))
            # Rear window (right)
            back = th > math.radians(105)
            rb = 3.1 * np.sin(np.pi - th[back])
            xb, yb = rb * np.cos(ph[back]), rb * np.sin(ph[back])
            vis_b = np.hypot(xb, yb) < 3.1
            ax.scatter(xb[vis_b] + 3.7, yb[vis_b], s=2.5 + 6 * mag[back][vis_b],
                       c=doppler_colour(np.full(vis_b.sum(), 0.32)), lw=0, alpha=0.75)
            ax.add_patch(Circle((3.7, 0.0), 3.3, fill=False, ec=RED, lw=3.5, alpha=0.85, zorder=6))
            draw_ship(ax, 0.0, -3.5, scale=0.85, col=GOLD, thrust=True, z=8)
            a_ahead = ease((t - 2.6) / 0.4)
            a_behind = ease((t - 6.4) / 0.4)
            pill_text(ax, -3.7, 3.75, "Stars ahead", col=WHITE, ec="#5fd6ff", pt=34, alpha=max(0.85, a_ahead))
            if a_ahead > 0.02:
                pill_text(ax, -3.7, -3.75, "Shift towards blue", col="#5fd6ff", ec="#5fd6ff", pt=34, alpha=a_ahead)
            if a_behind > 0.02:
                pill_text(ax, 3.7, 3.75, "Stars behind", col=WHITE, ec=RED, pt=34, alpha=a_behind)
                pill_text(ax, 3.7, -3.75, "Fade to red", col=RED, ec=RED, pt=34, alpha=a_behind)
        else:
            vis = (np.abs(x) < 8.3) & (np.abs(y) < 4.8)
            ax.scatter(x[vis], y[vis], s=s[vis], c=doppler_colour(D[front][vis]), lw=0, alpha=0.95)
        save(fig, out, i, still)
    finish(out, still)


def render_lightclock(out, seconds, still):
    """Light clock comparison:
    Left: clock at rest by Earth (photon bounces straight up and down between two mirrors, fast ticks).
    Right: clock inside a moving ship (photon travels on a long, slanted zigzag path because the mirrors move,
    so every tick takes longer). Variants tailor the focus to the exact spoken VO beat."""
    n = int(seconds * FPS)
    b = 0.8
    g = 1 / math.sqrt(1 - b * b)
    Hgap = 2.6
    tick = 1.05
    vx = b * Hgap / tick
    var = STYLE.get("var", "a")
    frames = [int(n * 0.55)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(i / max(1, n - 1))
        # Rest clock on the left (paired with real Earth disc)
        X0 = -4.8 if var != "d" else 0.0
        ph = (t / tick) % 2
        yy = -1.2 + Hgap * (ph if ph <= 1 else 2 - ph)
        put_earth(ax, X0 - 1.65, 0.1, 0.52, alpha=0.95)
        for yM in (-1.2, 1.4):
            ax.plot([X0 - 0.85, X0 + 0.85], [yM, yM], color=WHITE, lw=9, solid_capstyle="round", zorder=5)
        ax.plot([X0, X0], [-1.2, 1.4], color=CYAN, lw=2.5, ls=(0, (4, 4)), alpha=0.55, zorder=3)
        ax.add_patch(Circle((X0, yy), 0.23, color=CYAN, zorder=6))
        ax.add_patch(Circle((X0, yy), 0.60, color=CYAN, alpha=0.24, lw=0, zorder=5))
        ticks_rest = int(t / tick)

        if var == "d":
            # Row 14a (1:58.7–2:06.8): "Imagine a clock made of light, a flash bouncing between two mirrors, one tick for every trip."
            pill_text(ax, X0, 2.75, "Clock made of light", col=WHITE, ec=CYAN, pt=38, alpha=ease((t - 0.3) / 0.4))
            pill_text(ax, X0 + 2.8, 1.4, "Two mirrors", col=WHITE, ec=WHITE, pt=32, alpha=ease((t - 3.2) / 0.4))
            pill_text(ax, X0, -2.55, f"One tick: {ticks_rest}", col=YELLOW, ec=CYAN, pt=36, alpha=ease((t - 4.2) / 0.4))
        else:
            # Moving clock on the right: one full up-down bounce (ph2 in 0..2) sweeps x_c from -0.2 to 4.6
            x_left, x_mid, x_right = -0.2, 2.2, 4.6
            ph2 = (t / (tick * g)) % 2
            x_c = x_left + (x_right - x_left) * (ph2 / 2.0)
            y2 = -1.2 + Hgap * (ph2 if ph2 <= 1 else 2 - ph2)
            # Dashed full slanted V-path guide (shows why the moving path is longer than the vertical rest path)
            ax.plot([x_left, x_mid, x_right], [-1.2, 1.4, -1.2], color=GOLD, lw=2.5, ls=(0, (5, 5)), alpha=0.50, zorder=3)
            # Ship frame around the moving mirrors
            hull = FancyBboxPatch((x_c - 1.05, -1.55), 2.1, 3.3, boxstyle="round,pad=0.05,rounding_size=0.35",
                                  facecolor="#192842", edgecolor=GOLD, lw=2.5, alpha=0.55, zorder=2)
            ax.add_patch(hull)
            draw_ship(ax, x_c, 2.05, scale=0.65, col=GOLD, thrust=True, z=6)
            for yM in (-1.2, 1.4):
                ax.plot([x_c - 0.80, x_c + 0.80], [yM, yM], color=GOLD, lw=9, solid_capstyle="round", zorder=5)
            # Solid slanted zigzag photon trail traced up to (x_c, y2)
            if ph2 <= 1.0:
                ax.plot([x_left, x_c], [-1.2, y2], color=GOLD, lw=5.5, alpha=0.90, zorder=4)
            else:
                ax.plot([x_left, x_mid, x_c], [-1.2, 1.4, y2], color=GOLD, lw=5.5, alpha=0.90, zorder=4)
            ax.add_patch(Circle((x_c, y2), 0.24, color=YELLOW, zorder=6))
            ax.add_patch(Circle((x_c, y2), 0.65, color=GOLD, alpha=0.26, lw=0, zorder=5))
            ticks_mov = int(t / (tick * g))

            pill_text(ax, X0, 2.55, "At rest", col=CYAN, ec=CYAN, pt=32, alpha=0.95)
            pill_text(ax, X0, -2.35, f"Ticks: {ticks_rest}", col=WHITE, ec=CYAN, pt=32, alpha=0.95)
            pill_text(ax, 2.2, -2.35, f"Ticks: {ticks_mov}", col=YELLOW, ec=GOLD, pt=32, alpha=0.95)

            if var == "a":
                # Row 3: "Time itself ran at a different pace for you."
                pill_text(ax, 2.2, 3.15, "Different pace", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 2.2) / 0.4))
            elif var in ("b", "c"):
                # Row 6 / Row 12: "why a moving clock runs slow"
                pill_text(ax, 2.2, 3.15, "Moving clock runs slow", col=YELLOW, ec=GOLD, pt=34, alpha=ease((t - 1.0) / 0.4))
            elif var == "e":
                # Row 14b: "traveling on a long, slanted path"
                pill_text(ax, 2.2, 3.15, "Long, slanted path", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 2.0) / 0.4))
            elif var == "f":
                # Row 15b: "so every tick takes longer. The moving clock runs slow"
                lbl = "Moving clock runs slow" if t > 3.2 else "Every tick takes longer"
                pill_text(ax, 2.2, 3.15, lbl, col=YELLOW, ec=GOLD, pt=35, alpha=ease((t - 0.5) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_energy(out, seconds, still):
    """Kinetic energy vs speed: curve climbs steeply as speed approaches the dashed speed-of-light limit line,
    plus side-by-side 90% vs 99% energy bars ("nearly five times") so a viewer sees why you can't reach c."""
    n = int(seconds * FPS)
    vmax = 0.994
    vv = np.linspace(0, vmax, 1200)
    E = 1 / np.sqrt(1 - vv ** 2) - 1
    X0, X1, Y0, Y1 = -6.2, 4.6, -2.7, 3.2
    xs = X0 + (X1 - X0) * vv
    ys = Y0 + (Y1 - Y0) * E / E.max()
    var = STYLE.get("var", "a")
    frames = [int(n * 0.85)] if still else range(n)
    for i in frames:
        t = i / FPS
        s = ease((i / max(1, n - 1) - 0.04) / 0.82)
        k = max(2, int(len(vv) * s))
        fig, ax = canvas(i / max(1, n - 1))
        # Horizontal speed baseline & dashed speed-of-light barrier
        ax.plot([X0, X1 + 0.3], [Y0, Y0], color=WHITE, lw=3.5, alpha=0.75)
        x_lim = X0 + (X1 - X0) * 1.0
        ax.plot([x_lim, x_lim], [Y0, Y1 + 0.4], color=RED, lw=3.5, ls=(0, (6, 5)), alpha=0.9)
        pill_text(ax, x_lim - 0.2, Y1 + 0.55, "Speed of light", col=RED, ec=RED, pt=30, alpha=0.95)
        # Speed ticks on horizontal axis
        for v_mark, txt in ((0.5, "50%"), (0.9, "90%"), (0.99, "99%")):
            xm = X0 + (X1 - X0) * v_mark
            ax.plot([xm, xm], [Y0 - 0.18, Y0 + 0.18], color=WHITE, lw=2.5, alpha=0.8)
            ax.text(xm, Y0 - 0.52, txt, color=WHITE, fontsize=25, fontdict=FONT, ha="center", va="center", alpha=0.9)
        # Growing energy curve + moving ship climbing the hill
        ax.plot(xs[:k], ys[:k], color=GOLD, lw=22, alpha=0.18, solid_capstyle="round")
        ax.plot(xs[:k], ys[:k], color=GOLD, lw=9, solid_capstyle="round", zorder=4)
        ang = math.degrees(math.atan2(ys[k - 1] - ys[max(0, k - 15)], xs[k - 1] - xs[max(0, k - 15)]))
        draw_ship(ax, xs[k - 1], ys[k - 1], scale=0.62, angle_deg=ang, col=GOLD, thrust=True, z=7)

        if var == "a":
            # Row 6c (0:35.7–0:41.5): "and why you can never quite reach the limit."
            pill_text(ax, -1.5, 2.6, "Never reach the limit", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 1.8) / 0.4))
        elif var == "b":
            # Row 30a (5:29.5–5:33.1): "Take a single ton, about the mass of a small car."
            pill_text(ax, -1.8, 2.5, "1 ton: small car", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 0.5) / 0.4))
        elif var == "c":
            # Row 30d/e & 31a (5:42.0–5:56.3, offset 0.50 s):
            # "90 to 99% takes nearly five times as much, close to a whole year of the world's energy..."
            g90 = ease((t - 0.3) / 0.6)
            g99 = ease((t - 1.5) / 0.8)
            bx0, bx1, by = -5.2, -3.2, -1.4
            h90 = 0.85 * g90
            h99 = 4.00 * g99
            ax.add_patch(Rectangle((bx0 - 0.55, by), 1.1, h90, color=CYAN, alpha=0.9, zorder=5))
            ax.add_patch(Rectangle((bx1 - 0.55, by), 1.1, h99, color=GOLD, alpha=0.9, zorder=5))
            ax.text(bx0, by - 0.42, "90%", color=CYAN, fontsize=26, fontdict=FONT, ha="center", va="center")
            ax.text(bx1, by - 0.42, "99%", color=GOLD, fontsize=26, fontdict=FONT, ha="center", va="center")
            if t < 5.0:
                pill_text(ax, -3.5, 3.25, "Nearly five times", col=YELLOW, ec=GOLD, pt=35, alpha=ease((t - 2.0) / 0.4))
            elif t < 9.8:
                pill_text(ax, -3.5, 3.25, "1 year world energy", col=YELLOW, ec=GOLD, pt=34, alpha=ease((t - 5.2) / 0.4))
            else:
                pill_text(ax, -3.5, 3.25, "Each extra nine", col=YELLOW, ec=GOLD, pt=35, alpha=ease((t - 10.0) / 0.4))
        else:
            # var d: Row 31c/d (5:59.2–6:08.5): "nothing with mass ever reaches light speed... a hill that keeps getting steeper."
            lbl = "Hill gets steeper" if t > 4.6 else "Never reaches light speed"
            pill_text(ax, -2.0, 2.6, lbl, col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 0.5) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_muons(out, seconds, still):
    """Cosmic-ray muons born at the top of the atmosphere (15 km up) cross the 660 m classical limit line
    and reach the ground because their moving clocks run slow."""
    rng = np.random.default_rng(STYLE.get("seed", 1963))
    n = int(seconds * FPS)
    TOP, GROUND = 3.6, -3.5
    km = (TOP - GROUND) / 15.0
    classical = TOP - 1.35 * km
    speed = (TOP - GROUND) / (1.6 * FPS)
    mu = []
    var = STYLE.get("var", "a")
    frames = [int(n * 0.6)] if still else range(n)
    target = set(frames)
    for i in range(n):
        for _ in range(rng.poisson(1.6)):
            ang = rng.normal(0, 0.10)
            mu.append([rng.uniform(-5.8, 5.8), TOP, speed * math.sin(ang), i])
        nxt = []
        for m in mu:
            m[0] += m[2]
            m[1] -= speed
            if m[1] > GROUND:
                nxt.append(m)
        mu = nxt
        if i not in target:
            continue
        t = i / FPS
        fig, ax = canvas(i / max(1, n - 1))
        # Soft ground mountain/surface profile and top-of-atmosphere band (no full-width straight seam)
        xs_g = np.linspace(-8.5, 8.5, 200)
        ys_g = GROUND + 0.35 * np.exp(-((xs_g + 4.2) / 1.8) ** 2) + 0.12 * np.sin(xs_g * 0.9)
        ax.fill_between(xs_g, -5.0, ys_g, color="#1a2c38", alpha=0.85, zorder=-5)
        ax.plot([-6.2, 6.2], [TOP, TOP], color="#9f8cff", lw=3.0, alpha=0.75, ls=(0, (2, 5)))
        ax.plot([-6.2, 6.2], [classical, classical], color=RED, lw=2.5, ls=(0, (6, 5)), alpha=0.85)
        for m in mu:
            ax.plot([m[0] - m[2] * 10, m[0]], [m[1] + speed * 10, m[1]], color=CYAN, lw=2.6, alpha=0.82)
            ax.add_patch(Circle((m[0], m[1]), 0.07, color=WHITE, lw=0, zorder=5))

        pill_text(ax, -4.6, TOP + 0.42, "Top of atmosphere", col=WHITE, ec="#9f8cff", pt=28, alpha=0.92)
        pill_text(ax, 4.8, GROUND + 0.45, "Reach the ground", col=CYAN, ec=CYAN, pt=28, alpha=0.92)

        if var == "a":
            pill_text(ax, 4.4, TOP + 0.42, "Particles called muons", col=YELLOW, ec=CYAN, pt=32, alpha=ease((t - 3.5) / 0.4))
        elif var == "b":
            pill_text(ax, 0.0, classical - 0.55, "Only about 660 meters", col=YELLOW, ec=RED, pt=34, alpha=ease((t - 0.4) / 0.4))
        elif var == "c":
            pill_text(ax, 0.0, -1.2, "Reach the ground", col=YELLOW, ec=CYAN, pt=36, alpha=ease((t - 0.4) / 0.4))
        else:
            pill_text(ax, 0.0, -1.2, "Clocks running slow", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 0.4) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def dial(ax, cx, cy, r, angle, col, alpha=1.0):
    """Clock face with ring, 12 ticks, and hand at `angle` (radians, clockwise from 12 o'clock)."""
    ax.add_patch(Circle((cx, cy), r, facecolor="#0e1726", edgecolor=col, lw=4, alpha=0.9 * alpha, zorder=3))
    for k in range(12):
        a = 2 * math.pi * k / 12
        ax.plot([cx + 0.82 * r * math.sin(a), cx + 0.95 * r * math.sin(a)],
                [cy + 0.82 * r * math.cos(a), cy + 0.95 * r * math.cos(a)], color=col, lw=2, alpha=alpha, zorder=4)
    ax.plot([cx, cx + 0.78 * r * math.sin(angle)], [cy, cy + 0.78 * r * math.cos(angle)], color=col, lw=5,
            alpha=alpha, solid_capstyle="round", zorder=5)
    ax.add_patch(Circle((cx, cy), 0.08 * r, color=col, alpha=alpha, zorder=6))


def render_gpsclocks(out, seconds, still):
    """GPS satellite orbiting a real NASA Earth disc on the left; on the right, three to-scale bars with clear labels:
    Speed (-7 millionths, slow), Weaker gravity (+46 millionths, fast), Total (+38 millionths a day gained)."""
    n = int(seconds * FPS)
    frames = [int(n * 0.9)] if still else range(n)
    scale = 2.8 / 45.9
    var = STYLE.get("var", "a")
    for i in frames:
        t = i / FPS
        s = i / max(1, n - 1)
        fig, ax = canvas(i / max(1, n - 1))
        # Real Earth on the left + dashed orbital ring + moving GPS satellite
        EX, EY, ER = -4.3, -0.3, 1.55
        put_earth(ax, EX, EY, ER)
        orb_r = 2.65
        th = np.linspace(0, 2 * math.pi, 180)
        ax.plot(EX + orb_r * np.cos(th), EY + orb_r * np.sin(th), color=CYAN, lw=1.8, ls=(0, (4, 5)), alpha=0.55)
        a = math.radians(135 - 95 * s)
        sx, sy = EX + orb_r * math.cos(a), EY + orb_r * np.sin(a)
        ax.plot([sx - 0.65, sx + 0.65], [sy, sy], color=GOLD, lw=6, zorder=6)
        ax.add_patch(Rectangle((sx - 0.22, sy - 0.16), 0.44, 0.32, color=WHITE, zorder=7))
        pill_text(ax, EX, 2.85, "GPS satellite clock", col=WHITE, ec=CYAN, pt=30, alpha=0.95)

        # Right side: bar chart of daily drift (microseconds per day)
        base = -0.75
        ax.plot([0.0, 7.2], [base, base], color=WHITE, lw=2.2, alpha=0.65)
        bars = [
            (-7.2, CYAN, 1.15, "Speed", "-7 µs"),
            (45.9, GOLD, 3.65, "Gravity", "+46 µs"),
            (38.7, WHITE, 6.15, "Total", "+38 µs"),
        ]
        for k, (val, col, x, top_lbl, num_lbl) in enumerate(bars):
            if var == "a":
                g = ease((t - 0.4 - 0.4 * k) / 0.6) * 0.35
            elif var == "b":
                g = ease((t - 0.2) / 0.6) if k == 0 else (ease((t - 2.8) / 0.7) if k == 1 else 0.0)
            else:
                g = 1.0 if k < 2 else ease((t - 0.3) / 0.7)
            if g <= 0.01:
                continue
            h = val * scale * g
            ax.add_patch(Rectangle((x - 0.55, base if h >= 0 else base + h), 1.1, max(0.06, abs(h)), color=col, alpha=0.92, zorder=5))
            lbl_y = (base + 0.42) if val < 0 else (base - 0.48)
            ax.text(x, lbl_y, top_lbl, color=WHITE, fontsize=25, fontdict=FONT, ha="center", va="center", alpha=min(1.0, g * 1.5))
            if var != "a" and g > 0.25:
                ty = (base + h + 0.40) if h >= 0 else (base + h - 0.44)
                pill_text(ax, x, ty, num_lbl, col=YELLOW if k == 2 else col, ec=col, pt=24, pad_x=0.20, pad_y=0.14, alpha=min(1.0, g * 1.3))

        if var == "a":
            pill_text(ax, 3.65, 3.15, "Every clock drifts", col=YELLOW, ec=GOLD, pt=34, alpha=ease((t - 1.2) / 0.4))
        elif var == "b":
            pill_text(ax, 3.65, 3.35, "7 millionths slow", col=CYAN, ec=CYAN, pt=34, alpha=ease((t - 0.3) / 0.4))
        else:
            pill_text(ax, 3.65, 3.35, "38 millionths a day", col=YELLOW, ec=WHITE, pt=34, alpha=ease((t - 0.4) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_mapdrift(out, seconds, still):
    """Curved street network where the true position ring stays fixed and the uncorrected GPS position dot drifts
    off the road with a growing distance bar ('10 kilometers every day')."""
    n = int(seconds * FPS)
    frames = [int(n * 0.8)] if still else range(n)
    rng = np.random.default_rng(STYLE.get("seed", 24) + 7)
    xs, ys = [], []
    for k in range(14):
        u = rng.uniform(0, 1, 260)
        if k % 2:
            y0, amp, ph, fq = rng.uniform(-6.2, 6.2), rng.uniform(0.4, 1.4), rng.uniform(0, 6.3), rng.uniform(0.25, 0.6)
            x = -11.2 + 22.4 * u
            y = y0 + amp * np.sin(fq * x + ph)
        else:
            x0, amp, ph, fq = rng.uniform(-10.5, 10.5), rng.uniform(0.4, 1.4), rng.uniform(0, 6.3), rng.uniform(0.3, 0.7)
            y = -6.5 + 13 * u
            x = x0 + amp * np.sin(fq * y + ph)
        xs.append(x + rng.normal(0, 0.05, u.size))
        ys.append(y + rng.normal(0, 0.05, u.size))
    sx, sy = rng.uniform(-11, 11, 900), rng.uniform(-6.4, 6.4, 900)
    roads = dict(x=np.concatenate(xs + [sx]), y=np.concatenate(ys + [sy]),
                 s=np.concatenate([rng.uniform(2, 9, 14 * 260), rng.uniform(1, 4, 900)]),
                 a=np.concatenate([rng.uniform(0.45, 0.85, 14 * 260), rng.uniform(0.2, 0.5, 900)]))
    for i in frames:
        t = i / FPS
        s = ease(i / max(1, n - 1))
        fig, ax = canvas(i / max(1, n - 1))
        rgba = np.column_stack([np.full_like(roads["a"], 1.0), np.full_like(roads["a"], 0.80),
                                np.full_like(roads["a"], 0.52), roads["a"]])
        ax.scatter(roads["x"], roads["y"], s=roads["s"], c=rgba, lw=0, zorder=1)
        # True position ring
        tx0, ty0 = -3.6, -1.2
        ax.add_patch(Circle((tx0, ty0), 0.45, fill=False, ec=WHITE, lw=3.5, zorder=5))
        ax.add_patch(Circle((tx0, ty0), 0.14, color=WHITE, zorder=6))
        pill_text(ax, tx0, ty0 - 0.95, "Your position", col=WHITE, ec=WHITE, pt=28, alpha=0.95)
        # Drifting GPS pin
        ts = np.linspace(0, s, 60)
        px, py = tx0 + 7.8 * ts, ty0 + 3.2 * ts ** 1.15
        ax.plot(px, py, color=CYAN, lw=4, ls=(0, (5, 4)), alpha=0.8, zorder=4)
        ax.add_patch(Circle((px[-1], py[-1]), 0.24, color=CYAN, zorder=6))
        ax.add_patch(Circle((px[-1], py[-1]), 0.55, color=CYAN, alpha=0.25, lw=0, zorder=5))
        km_val = 10.0 * s
        pill_text(ax, px[-1], py[-1] + 0.85, f"Drift: {km_val:.1f} km", col=CYAN, ec=CYAN, pt=28, alpha=0.95)
        if t > 3.5:
            pill_text(ax, 0.0, -3.2, "10 kilometers every day", col=YELLOW, ec=GOLD, pt=36, alpha=ease((t - 3.5) / 0.4))
        save(fig, out, i, still)
    finish(out, still)


def render_gammaclocks(out, seconds, still):
    """Five clocks for Home (0), 10%, 90%, 99% (7 to 1) and 99.99% (70 to 1) with persistent speed labels
    and pace bars so all five speeds compare at a glance."""
    n = int(seconds * FPS)
    vs = [0.0, 0.1, 0.9, 0.99, 0.9999]
    labels_top = ["Home", "10%", "90%", "99%", "99.99%"]
    labels_bot = ["Normal pace", "Half a percent", "Half pace", "7 to 1", "70 to 1"]
    cues = [0.0, 0.6, 5.2, 10.8, 14.6]
    rates = [math.sqrt(1 - v * v) for v in vs]
    frames = [int(n * 0.95)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas(i / max(1, n - 1))
        for k, rate in enumerate(rates):
            lit = ease((t - cues[k]) / 0.5) if k else 1.0
            cx = -5.8 + k * 2.9
            col = CYAN if k == 0 else GOLD
            alpha = 0.30 + 0.70 * lit
            if k == 0:
                put_earth(ax, cx, 2.35, 0.42, alpha=0.95)
            else:
                draw_ship(ax, cx, 2.35, scale=0.48, col=col, thrust=(lit > 0.3), alpha=alpha)
            dial(ax, cx, 0.35, 1.18, 2 * math.pi * 0.55 * t * rate, col, alpha=alpha)
            pill_text(ax, cx, -1.45, labels_top[k], col=YELLOW if lit > 0.5 and k > 0 else WHITE, ec=col, pt=26, pad_x=0.22, alpha=alpha)
            # Pace bar showing how fast the clock ticks relative to Home
            bw = 1.8 * rate
            ax.add_patch(Rectangle((cx - 0.9, -2.25), 1.8, 0.24, color=DIM, alpha=0.35 * alpha, zorder=3))
            ax.add_patch(Rectangle((cx - 0.9, -2.25), max(0.08, bw), 0.24, color=col, alpha=0.9 * alpha, zorder=4))
            if lit > 0.1:
                pill_text(ax, cx, -3.05, labels_bot[k], col=YELLOW if k >= 3 else WHITE, ec=col, pt=21, pad_x=0.18, pad_y=0.14, alpha=lit)
        save(fig, out, i, still)
    finish(out, still)


def render_twinclocks(out, seconds, still):
    """Variants a/b/e: Earth twin clock (left, real Earth disc, 20 years bar growing) vs Ship twin clock
    (right, ship icon, 3 years bar growing).
    Variants c/d (Row 26 turnaround): Diagram showing Earth's straight course vs the Ship firing its engines,
    stopping at the star 10 light-years out, turning around, and flying back."""
    n = int(seconds * FPS)
    g = 7.0888
    var = STYLE.get("var", "a")
    frames = [int(n * 0.7)] if still else range(n)
    for i in frames:
        t = i / FPS
        s = i / max(1, n - 1)
        fig, ax = canvas(i / max(1, n - 1))
        if var in ("c", "d"):
            # Row 26 turnaround diagram: why isn't your twin the younger one?
            put_earth(ax, -5.6, 1.3, 0.65)
            pill_text(ax, -5.6, 2.55, "Twin on Earth", col=CYAN, ec=CYAN, pt=28, alpha=0.95)
            ax.plot([-4.6, 4.2], [1.3, 1.3], color=CYAN, lw=4, ls=(0, (6, 4)), alpha=0.8)
            pill_text(ax, -0.2, 2.05, "Never changed course", col=WHITE, ec=CYAN, pt=28, alpha=0.95)

            # Star on the right (turnaround point)
            sx, sy = 5.4, -1.2
            for r_s, a_s in ((0.85, 0.08), (0.5, 0.18), (0.25, 0.45)):
                ax.add_patch(Circle((sx, sy), r_s, color=RED, alpha=a_s, lw=0, zorder=4))
            ax.add_patch(Circle((sx, sy), 0.14, color=WHITE, zorder=5))

            # Ship outbound -> turnaround loop -> inbound
            u = min(1.0, max(0.0, (t - 0.2) / 5.2))
            ax.plot([-4.6, 4.6], [-0.7, -0.7], color=GOLD, lw=3.5, alpha=0.65)
            ax.plot([4.6, -4.6], [-1.7, -1.7], color=GOLD, lw=3.5, alpha=0.65)
            th_arc = np.linspace(math.pi / 2, -math.pi / 2, 40)
            ax.plot(4.6 + 0.5 * np.cos(th_arc), -1.2 + 0.5 * np.sin(th_arc), color=GOLD, lw=3.5, alpha=0.65)
            if u < 0.42:
                k = u / 0.42
                sh_x, sh_y, ang = -4.6 + 9.2 * k, -0.7, 0.0
            elif u < 0.62:
                k = (u - 0.42) / 0.20
                ang_r = math.pi / 2 - math.pi * k
                sh_x, sh_y = 4.6 + 0.5 * math.cos(ang_r), -1.2 + 0.5 * np.sin(ang_r)
                ang = -180.0 * k
                # Bright braking/turnaround thruster flash at the turn
                ax.add_patch(Circle((sh_x, sh_y), 0.75, color=YELLOW, alpha=0.35, lw=0, zorder=6))
            else:
                k = (u - 0.62) / 0.38
                sh_x, sh_y, ang = 4.6 - 9.2 * k, -1.7, 180.0
            draw_ship(ax, sh_x, sh_y, scale=0.82, angle_deg=ang, col=GOLD, thrust=True, z=8)
            lbl = "Turned around" if var == "d" else "Two trips not the same"
            pill_text(ax, 0.0, -3.15, lbl, col=YELLOW, ec=GOLD, pt=34, alpha=0.95)
        else:
            # Side-by-side Home vs Ship clocks + growing 20 YEARS vs 3 YEARS bars
            put_earth(ax, -3.6, 2.55, 0.55)
            pill_text(ax, -1.4, 2.55, "On Earth", col=CYAN, ec=CYAN, pt=30, alpha=0.95)
            draw_ship(ax, 1.8, 2.55, scale=0.72, col=GOLD, thrust=True)
            pill_text(ax, 4.1, 2.55, "On board", col=GOLD, ec=GOLD, pt=30, alpha=0.95)

            dial(ax, -3.5, 0.25, 1.65, 2 * math.pi * 0.38 * t, CYAN)
            dial(ax, 3.5, 0.25, 1.65, 2 * math.pi * 0.38 * t / g, GOLD)

            prog = min(1.0, max(0.15, (t - 0.3) / 4.2))
            yr_earth = 20.0 * prog
            yr_ship = 3.0 * prog
            # Growing horizontal year bars under each clock
            ax.add_patch(Rectangle((-6.1, -2.15), 5.2, 0.42, color=DIM, alpha=0.3, zorder=3))
            ax.add_patch(Rectangle((-6.1, -2.15), 5.2 * prog, 0.42, color=CYAN, alpha=0.92, zorder=4))
            pill_text(ax, -3.5, -3.05, f"{yr_earth:.0f} years" if prog < 0.95 else "20 years", col=YELLOW, ec=CYAN, pt=34, alpha=0.95)

            ax.add_patch(Rectangle((0.9, -2.15), 5.2, 0.42, color=DIM, alpha=0.3, zorder=3))
            ax.add_patch(Rectangle((0.9, -2.15), 5.2 * (3.0 / 20.0) * prog, 0.42, color=GOLD, alpha=0.92, zorder=4))
            pill_text(ax, 3.5, -3.05, f"{yr_ship:.1f} years" if prog < 0.95 else "About 3 years", col=YELLOW, ec=GOLD, pt=34, alpha=0.95)
        save(fig, out, i, still)
    finish(out, still)


def render_contraction(out, seconds, still):
    """Length contraction (Row 25):
    Top reference bar: rest distance from Earth to the star = '10 light-years'.
    Bottom ship-frame bar: as the ship travels at 99% of c, the gap ahead shrinks to 1/7.09 = 'About 1.5 light-years'."""
    rng = np.random.default_rng(STYLE.get("seed", 10))
    n = int(seconds * FPS)
    bg = rng.uniform([-8, -4.5], [8, 4.5], (400, 2))
    var = STYLE.get("var", "a")
    frames = [int(n * 0.85)] if still else range(n)
    x0, L0 = -5.6, 11.2
    for i in frames:
        t = i / FPS
        s = 1.0 if var == "b" else ease((t - 1.2) / 6.2)
        L = L0 * (1 - s * (1 - 1 / 7.0888))
        fig, ax = canvas(i / max(1, n - 1))
        ax.scatter(bg[:, 0], bg[:, 1], s=4, color=WHITE, alpha=0.45, lw=0)

        # Top: Earth rest frame (10 light-years fixed)
        y_top = 1.65
        put_earth(ax, x0, y_top, 0.55)
        ax.plot([x0 + 0.65, x0 + L0], [y_top, y_top], color=DIM, lw=3.5, ls=(0, (6, 5)), alpha=0.85)
        for r_s, a_s in ((0.75, 0.08), (0.45, 0.18), (0.22, 0.45)):
            ax.add_patch(Circle((x0 + L0, y_top), r_s, color=RED, alpha=a_s, lw=0, zorder=4))
        ax.add_patch(Circle((x0 + L0, y_top), 0.13, color=WHITE, zorder=5))
        pill_text(ax, x0 + L0 / 2, y_top + 0.95, "10 light-years", col=WHITE, ec=CYAN, pt=34, alpha=0.95)

        # Bottom: Ship frame (shrinking distance from 10 ly to 1.5 ly)
        y_bot = -1.35
        draw_ship(ax, x0, y_bot, scale=0.85, col=GOLD, thrust=True, z=7)
        ax.plot([x0 + 0.65, x0 + L], [y_bot, y_bot], color=GOLD, lw=6, zorder=5)
        for r_s, a_s in ((0.85, 0.10), (0.50, 0.22), (0.25, 0.55)):
            ax.add_patch(Circle((x0 + L, y_bot), r_s, color=GOLD, alpha=a_s, lw=0, zorder=5))
        ax.add_patch(Circle((x0 + L, y_bot), 0.16, color=WHITE, zorder=6))

        cur_ly = 10.0 * (1 - s * (1 - 1.5 / 10.0))
        lbl_bot = "One and a half" if s > 0.85 else f"Gap shrinks: {cur_ly:.1f} ly"
        pill_text(ax, x0 + max(2.2, L / 2), y_bot - 1.15, lbl_bot, col=YELLOW, ec=GOLD, pt=34, alpha=0.95)
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
            STYLE.update(on=False, name=name, var="")
            fn(os.path.join(a.out, name), a.seconds or secs, a.still)
            continue
        V = VARIANTS[a.variant]
        C = VARIANT_COLOURS.get((name, a.variant), V)
        GOLD, CYAN = C["gold"], C["cyan"]
        bed, stars = make_bed(V["seed"] + len(name), stars=(name != "starfield"), N=BED_STARS.get(name, 2600))
        STYLE.update(on=True, name=name, var=a.variant, cam=V["cam"], bed=bed, stars=stars, seed=V["seed"] + len(name))
        fn(os.path.join(a.out, f"{name}_{a.variant}"), a.seconds or secs + 8, a.still)


if __name__ == "__main__":
    sys.exit(main())
