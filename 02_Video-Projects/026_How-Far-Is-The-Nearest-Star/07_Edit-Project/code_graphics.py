#!/usr/bin/env python3
"""Code-drawn graphics for the nearest-star film (026). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py parallax   out/   # ch.2: Earth moves Jan -> Jul; the near star shifts against the far stars
  python3 code_graphics.py triple     out/   # ch.1: Alpha Cen A and B orbit each other; Proxima loops round them, far out
  python3 code_graphics.py journey    out/   # ch.4: five lanes to Proxima at true relative speeds; only light moves visibly
  python3 code_graphics.py lighttimes out/   # ch.4: Moon, Sun, Proxima light-travel times as bars on a log scale
  python3 code_graphics.py scale      out/   # ch.3 row 18: grapefruit-scale Sun left, pin-prick Earth far right, push across
  python3 code_graphics.py lightyear  out/   # row 9 (v05): one pulse Proxima -> real Earth, a tick lights per year (4.25 yr)
  python3 code_graphics.py lightrace  out/   # row 27 (v05): real Moon, real Sun, then Proxima each send a pulse to Earth
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
  scale      Sizes, not distance: at grapefruit scale Earth is about 1/109 of the Sun's width, but sits about 15 m away,
             so the gap is drawn short to fit one frame. The point is a big warm disc and a dot you can barely see.
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
    """The sky seen from Earth, full frame: far stars fill the frame and stay fixed; the near star (red, with a glow)
    slides across them as Earth goes round the Sun. No panels or border lines."""
    rng = np.random.default_rng(1838)
    n = int(seconds * FPS)
    far = rng.uniform([-8.2, -4.7], [8.2, 4.7], (1400, 2))
    size = rng.pareto(2.2, 1400) * 3 + 2
    alpha = rng.uniform(0.35, 0.95, 1400)
    tint = np.where(rng.random(1400) < 0.15, "#ffd9a8", np.where(rng.random(1400) < 0.15, "#bcd4ff", WHITE))
    frames = [int(n * 0.8)] if still else range(n)
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.1) / 0.8)
        fig, ax = canvas()
        ax.scatter(far[:, 0], far[:, 1], s=size, c=tint, alpha=alpha, lw=0)
        nx = 3.2 - 6.4 * s
        for r, a in ((0.9, 0.06), (0.55, 0.12), (0.3, 0.25)):
            ax.add_patch(Circle((nx, 0.3), r, color=RED, alpha=a, lw=0, zorder=4))
        ax.add_patch(Circle((nx, 0.3), 0.14, color="#ffd0c0", zorder=5))
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
    grows in turn. A faint tick marks each power of ten. Text-free. The longest bar is centred and reaches 80% of the
    frame width; each bar starts within 1 s of the last, so no small bar is held alone. Moon and Sun grow in 2 s;
    Proxima keeps drawing slowly until 2 s before the end (row 27 runs it whole: the slow draw is the 4.2 years)."""
    n = int(seconds * FPS)
    grow = [2.0, 2.0, max(2.0, seconds - 1.9 - 2.0)]
    vals = [1.3, 499.0, 1.34e8]
    cols = ["#d9d9d9", GOLD, RED]
    L0, L1 = -1.0, 9.0
    longest = (math.log10(max(vals)) - L0) / (L1 - L0)
    X0 = -6.4
    X1 = X0 + 12.8 / longest
    frames = [int(n * 0.95)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas()
        for p in range(int(L0), int(L1) + 1):
            x = X0 + (X1 - X0) * (p - L0) / (L1 - L0)
            if x <= 6.5:
                ax.plot([x, x], [-3.6, 3.6], color=DIM, lw=1, alpha=0.08)
        for k, (v, col) in enumerate(zip(vals, cols)):
            g = ease((t - 0.3 - k * 0.8) / grow[k])
            full = (math.log10(v) - L0) / (L1 - L0)
            y = 2.4 - k * 2.4
            ax.add_patch(Rectangle((X0, y - 1.05), (X1 - X0) * full * g, 2.1, color=col, lw=0))
        save(fig, out, i, still)
    finish(out, still)


def render_scale(out, seconds, still):
    """A warm glowing Sun disc at grapefruit scale sits left; Earth is a single pin-prick dot far right. The view
    pushes slowly from the Sun across the empty gap towards the dot. Text-free."""
    rng = np.random.default_rng(109)
    n = int(seconds * FPS)
    stars = rng.uniform([-12, -6], [16, 6], (260, 2))
    SX, SR = -5.4, 0.9
    EX, EY = 6.6, 0.15
    frames = [int(n * 0.6)] if still else range(n)
    for i in frames:
        s = ease(i / max(1, n - 1))
        fig, ax = canvas()
        cx = 0.7 * s
        half = 8.0 - 1.0 * s
        ax.set_xlim(cx - half, cx + half)
        ax.set_ylim(-half * 9 / 16, half * 9 / 16)
        ax.scatter(stars[:, 0], stars[:, 1], s=3, color=WHITE, alpha=0.35, lw=0)
        for k in np.linspace(3.0, 1.05, 24):
            ax.add_patch(Circle((SX, 0), SR * k, color=GOLD, alpha=0.025, lw=0, zorder=3))
        ax.add_patch(Circle((SX, 0), SR, color="#ffd77a", zorder=5))
        ax.add_patch(Circle((SX, 0), SR * 0.8, color="#fff0c0", alpha=0.6, lw=0, zorder=6))
        ax.add_patch(Circle((EX, EY), 0.09, color=EARTH, alpha=0.3, lw=0, zorder=5))
        ax.add_patch(Circle((EX, EY), 0.035, color="#9cc8ff", zorder=6))
        save(fig, out, i, still)
    finish(out, still)


POOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool_v01")
EARTH_IMG = "earth_moon/GSFC_20171208_Archive_e002130.jpg"
MOON_IMG = "earth_moon/GSFC_20171208_Archive_e001982.jpg"
SUN_IMG = "sun/GSFC_20171208_Archive_e002035.jpg"
_DISCS = {}


def disc(rel, px=600):
    """A real photo cut out as an RGBA disc: the body's bounding box (rows/columns with a run of lit pixels, so captions
    and single bright specks don't count), squared about its centre, with a feathered circular edge."""
    if rel in _DISCS:
        return _DISCS[rel]
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
    yy, xx = np.mgrid[0:px, 0:px]
    d = np.hypot(xx - (px - 1) / 2, yy - (px - 1) / 2) / (px / 2)
    alpha = np.clip((1.0 - d) / 0.02, 0, 1)
    _DISCS[rel] = np.dstack([rgb, alpha])
    return _DISCS[rel]


def put_disc(ax, rel, x, y, r, alpha=1.0, z=5):
    img = disc(rel).copy()
    img[..., 3] *= alpha
    ax.imshow(img, extent=(x - r, x + r, y - r, y + r), zorder=z, interpolation="bilinear")


def red_dwarf(ax, x, y, alpha=1.0, scale=1.0):
    for r, a in ((0.9, 0.06), (0.55, 0.12), (0.3, 0.25)):
        ax.add_patch(Circle((x, y), r * scale, color=RED, alpha=a * alpha, lw=0, zorder=4))
    ax.add_patch(Circle((x, y), 0.14 * scale, color="#ffd0c0", alpha=alpha, zorder=5))


def pulse(ax, x0, y, x, alpha=1.0, trail=1.6):
    """A bright pulse of light at x travelling right from x0, with a fading trail."""
    if alpha <= 0:
        return
    t0 = max(x0, x - trail)
    xs = np.linspace(t0, x, 40)
    for k in range(len(xs) - 1):
        f = (k + 1) / len(xs)
        ax.plot(xs[k:k + 2], [y, y], color=GOLD, lw=4, alpha=0.55 * f * f * alpha, solid_capstyle="butt", zorder=6)
    for r, a in ((0.42, 0.10), (0.24, 0.25), (0.12, 0.6)):
        ax.add_patch(Circle((x, y), r, color="#fff3c8", alpha=a * alpha, lw=0, zorder=7))
    ax.add_patch(Circle((x, y), 0.06, color="white", alpha=alpha, zorder=8))


def star_field(seed, n=900):
    rng = np.random.default_rng(seed)
    pts = rng.uniform([-8.2, -4.7], [8.2, 4.7], (n, 2))
    size = rng.pareto(2.2, n) * 2.5 + 1.5
    alpha = rng.uniform(0.25, 0.8, n)
    tint = np.where(rng.random(n) < 0.15, "#ffd9a8", np.where(rng.random(n) < 0.15, "#bcd4ff", WHITE))
    return pts, size, alpha, tint


def render_lightyear(out, seconds, still, leave=0.6, arrive=8.3):
    """Row 9: Proxima (red-dwarf glow, left) and a small real Earth (right) across a full-frame star field. One pulse
    leaves Proxima at `leave` s and reaches Earth at `arrive` s at constant speed. Four ticks at 1/4.25 .. 4/4.25 of the
    path (one per year of the 4.25-year trip) light up as the pulse passes; the last quarter year has no tick."""
    pts, size, alpha, tint = star_field(4246)
    n = int(seconds * FPS)
    PX, EX, Y = -6.2, 6.2, 0.0
    ticks = [PX + (EX - PX) * k / 4.25 for k in range(1, 5)]
    frames = [int(n * 0.6)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas()
        ax.scatter(pts[:, 0], pts[:, 1], s=size, c=tint, alpha=alpha, lw=0)
        ax.plot([PX, EX], [Y, Y], color=DIM, lw=1, alpha=0.18, zorder=2)
        s = min(1.0, max(0.0, (t - leave) / (arrive - leave)))
        x = PX + (EX - PX) * s
        for tx in ticks:
            lit = x >= tx
            ax.plot([tx, tx], [Y - 0.22, Y + 0.22], color=GOLD if lit else DIM, lw=3 if lit else 2,
                    alpha=0.95 if lit else 0.35, zorder=3)
        red_dwarf(ax, PX, Y, scale=1.3)
        put_disc(ax, EARTH_IMG, EX, Y, 0.42)
        if t >= leave:
            fade = 1.0 - ease((t - arrive) / 0.5) if t > arrive else 1.0
            pulse(ax, PX, Y, min(x, EX - 0.3), alpha=fade)
        if t > arrive:
            g = 1.0 - ease((t - arrive) / 1.2)
            ax.add_patch(Circle((EX, Y), 0.75, color="#fff3c8", alpha=0.25 * g, lw=0, zorder=9))
        save(fig, out, i, still)
    finish(out, still)


def render_lightrace(out, seconds, still):
    """Row 27, timed to the VO from the row's start (361.80 s): a small real Earth on the right throughout; on the left,
    in turn, the real Moon (LRO e001982), the real Sun (SDO e002035) and Proxima (code red-dwarf glow), each a cut-out
    disc on black space. Each sends a pulse to Earth: the Moon's lands in 1 s, the Sun's in 3 s, Proxima's sets out on
    "Light from the nearest star" and is still only a sliver of the way across when the row ends. Text-free."""
    pts, size, alpha, tint = star_field(1338, 500)
    n = int(seconds * FPS)
    SX, EX, Y = -5.4, 5.8, 0.0
    # (source, fade in, pulse leaves, pulse arrives, fade out); local seconds from the row start
    beats = [("moon", 1.9, 3.3, 4.3, 5.9), ("sun", 6.0, 6.5, 9.5, 9.6), ("proxima", 9.7, 10.2, None, None)]
    crawl = 0.035 / max(0.1, seconds - 10.2)
    frames = [int(n * 0.6)] if still else range(n)
    for i in frames:
        t = i / FPS
        fig, ax = canvas()
        ax.scatter(pts[:, 0], pts[:, 1], s=size, c=tint, alpha=alpha * 0.8, lw=0)
        put_disc(ax, EARTH_IMG, EX, Y, 0.6)
        for name, fin, leave, arrive, fout in beats:
            a = ease((t - fin) / 0.5) * (1.0 - ease((t - fout) / 0.5) if fout else 1.0)
            if a <= 0:
                continue
            if name == "moon":
                put_disc(ax, MOON_IMG, SX, Y, 0.75, a)
                x0 = SX + 0.75
            elif name == "sun":
                put_disc(ax, SUN_IMG, SX, Y, 1.2, a)
                x0 = SX + 1.2
            else:
                red_dwarf(ax, SX, Y, a, scale=1.5)
                x0 = SX + 0.3
            if t < leave:
                continue
            x1 = EX - 0.6
            if arrive:
                s = min(1.0, (t - leave) / (arrive - leave))
                fade = 1.0 - ease((t - arrive) / 0.4) if t > arrive else 1.0
                pulse(ax, x0, Y, x0 + (x1 - x0) * s, alpha=a * fade)
                if t > arrive:
                    g = 1.0 - ease((t - arrive) / 1.0)
                    ax.add_patch(Circle((EX, Y), 0.95, color="#fff3c8", alpha=0.25 * g * a, lw=0, zorder=9))
            else:
                s = crawl * (t - leave)
                pulse(ax, x0, Y, x0 + (x1 - x0) * s, alpha=a, trail=0.35)
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
    ap.add_argument("which", choices=["parallax", "triple", "journey", "lighttimes", "scale", "lightyear", "lightrace", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    jobs = {"parallax": (render_parallax, 12), "triple": (render_triple, 12), "journey": (render_journey, 14),
            "lighttimes": (render_lighttimes, 18), "scale": (render_scale, 10),
            "lightyear": (render_lightyear, 9.6), "lightrace": (render_lightrace, 16.8)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
