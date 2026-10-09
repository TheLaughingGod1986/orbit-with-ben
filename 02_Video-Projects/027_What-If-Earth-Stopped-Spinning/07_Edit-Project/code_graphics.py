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

The globe is the real Earth (Claude, 9 Oct: no cartoon land blobs). It maps NASA's Blue Marble Next Generation
(December 2004, topography + bathymetry; NASA Earth Observatory / Reto Stockli; public domain) onto the sphere:
  curl -o blue_marble.jpg https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg
Put it next to this file, or point BLUE_MARBLE at it. Without it the script stops rather than fall back to blobs.
Credit line for the description: "Earth texture: NASA Earth Observatory (Blue Marble Next Generation)."

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
import argparse, logging, math, os, subprocess, sys
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

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


_TEX = None


def texture():
    """Blue Marble as a float array (H, W, 3), loaded once and halved for speed."""
    global _TEX
    if _TEX is None:
        from PIL import Image
        path = os.environ.get("BLUE_MARBLE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "blue_marble.jpg")
        if not os.path.exists(path):
            sys.exit(f"missing Earth texture {path} (see the docstring for the NASA download)")
        im = Image.open(path).convert("RGB")
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
        _TEX = np.asarray(im, dtype=np.float32) / 255.0
    return _TEX


def earth_image(px, phase, rx=1.0, night=None, drain=None):
    """An orthographic view of the real Earth, px pixels tall, as RGBA. phase turns it east (radians).
    night: a screen-space unit vector (dx, dy) pointing at the Sun; the far half is shaded.
    drain: (band, s) for the slow stop. Inside |latitude| < band the sea dries to sand-coloured ground (keeping the
    texture's own light and shade); outside it the land floods to sea. s (0-1) blends from today's Earth."""
    tex = texture()
    th, tw = tex.shape[:2]
    pw = max(2, int(round(px * rx)))
    u = np.linspace(-1, 1, pw)[None, :]
    v = np.linspace(1, -1, px)[:, None]
    uu, vv = u / 1.0, np.broadcast_to(v, (px, pw))
    uu = np.broadcast_to(uu, (px, pw))
    rr = uu ** 2 + vv ** 2
    inside = rr <= 1.0
    z = np.sqrt(np.clip(1 - rr, 0, None))
    lat = np.arcsin(np.clip(vv, -1, 1))
    lon = np.arctan2(uu, z) - phase                       # features drift east (left to right) as phase grows
    ty = ((0.5 - lat / math.pi) * (th - 1)).astype(np.int32)
    tx = (((lon / (2 * math.pi) + 0.5) % 1.0) * (tw - 1)).astype(np.int32)
    rgb = tex[ty, tx]
    if drain is not None:
        band, sd = drain
        sea = (rgb[..., 2] > rgb[..., 0] * 1.15) & (rgb[..., 2] > rgb[..., 1] * 0.95)
        lum = rgb.mean(axis=-1, keepdims=True)
        sand = np.clip(np.array([0.80, 0.66, 0.44]) * (0.75 + 0.9 * lum), 0, 1)
        ocean = np.clip(np.array([0.10, 0.24, 0.48]) * (0.8 + 0.6 * lum), 0, 1)
        mid = (np.abs(lat) < band)[..., None]
        target = np.where(mid, np.where(sea[..., None], sand, rgb), np.where(sea[..., None], rgb, ocean))
        rgb = rgb * (1 - sd) + target * sd
    shade = 0.55 + 0.45 * z                                 # soft limb darkening
    if night is not None:
        dx, dy = night
        lit = uu * dx + vv * dy + 0.0 * z
        shade = shade * np.where(lit > 0, 1.0, 0.18) * (0.85 + 0.15 * np.clip(lit * 4 + 0.5, 0, 1))
    rgb = rgb * shade[..., None]
    a = np.clip((1 - rr) * px * 0.5, 0, 1) * inside       # an anti-aliased rim
    return np.dstack([rgb, a])


def globe(ax, x, y, r, phase, rx=1.0, land=True, night=None, drain=None):
    """The real Earth, side-on, turning with phase. Meridian and latitude guides are left out: the land shows the spin."""
    px = int(round(2 * r * H / 9.0))                      # the canvas is 9 units tall
    ax.imshow(earth_image(px, phase, rx, night, drain), extent=(x - r * rx, x + r * rx, y - r, y + r), zorder=2,
              interpolation="bilinear")
    ax.add_patch(Ellipse((x, y), 2 * r * rx * 1.02, 2 * r * 1.02, fill=False, ec=AIR, lw=2.5, alpha=0.18, zorder=5))


LABELS = ["", ""]                                     # set per row from --label / --label2 (AGENTS: words from that row's line)
FONT = {"family": ["Arial", "Helvetica", "DejaVu Sans"], "weight": "bold"}


def label(ax, x, y, text, alpha=1.0, color=WHITE, size=34, ha="center"):
    if not text or alpha <= 0.01:
        return
    ax.text(x, y, text, color=color, alpha=alpha, fontsize=size * 0.85, ha=ha, va="center", zorder=9, fontdict=FONT,
            bbox=dict(facecolor=BG, alpha=0.7 * alpha, edgecolor="none", boxstyle="round,pad=0.25"))


def speed_arrows(ax, x, y, r, scale, alpha=0.9, shift=0.0):
    for lat in (-75, -60, -45, -30, -15, 0, 15, 30, 45, 51.5, 60, 75):
        c = math.cos(math.radians(lat))
        yy = y + r * math.sin(math.radians(lat))
        x0 = x + shift                                    # from the central meridian, across the face, pointing east
        L = scale * c
        if L > 0.05:
            col = GOLD if lat == 51.5 else AIR
            ax.add_patch(FancyArrow(x0, yy, L, 0, width=0.06, head_width=0.2, head_length=0.2,
                                    length_includes_head=True, color=col, alpha=alpha, lw=0.8, ec="#05060a", zorder=6))


def render_speed(out, seconds, still):
    n, frames = frames_for(seconds, still)
    for i in frames:
        s = ease(i / max(1, n - 1) / 0.5)
        fig, ax = canvas()
        globe(ax, -1.5, 0, 3.2, i / FPS * 0.35)
        speed_arrows(ax, -1.5, 0, 3.2, 3.6 * s)
        la = ease((i / max(1, n - 1) - 0.55) / 0.12)
        label(ax, 2.6, 3.2 * math.sin(math.radians(51.5)), LABELS[0], alpha=la, color=GOLD, ha="left")  # by the gold arrow
        label(ax, 2.6, 0, LABELS[1], alpha=la, ha="left")                                                  # by the equator arrow
        save(fig, out, i, still)
    finish(out, still)


def render_bulge(out, seconds, still):
    n, frames = frames_for(seconds, still)
    for i in frames:
        s = ease(i / max(1, n - 1) / 0.6)
        fig, ax = canvas()
        globe(ax, 0, 0, 3.4, i / FPS * 0.35, rx=1 + 0.08 * s)
        ax.add_patch(Circle((0, 0), 3.4, fill=False, ec=DIM, lw=1.2, ls=(0, (5, 5)), alpha=0.6 * s, zorder=6))
        if LABELS[0]:
            ax.annotate("", xy=(-3.4 * (1 + 0.08 * s), -3.9), xytext=(3.4 * (1 + 0.08 * s), -3.9),
                        arrowprops=dict(arrowstyle="<->", color=WHITE, lw=2, alpha=s), zorder=8)
        label(ax, 0, -3.9, LABELS[0], alpha=ease((i / max(1, n - 1) - 0.5) / 0.15))
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
        label(ax, 4.6, 3.7, LABELS[0], alpha=ease((u - stop - 0.05) / 0.12))        # e.g. THE AIR KEEPS GOING
        label(ax, 4.6, -3.7, LABELS[1], alpha=ease((u - 0.55) / 0.12))             # e.g. FASTER THAN SOUND
        save(fig, out, i, still)
    finish(out, still)


def render_oceans(out, seconds, still):
    """Start as today's Earth; the sea drains to two polar oceans and one band of dry land spreads round the middle.
    The land keeps the real texture's light and shade (sand-coloured), so it reads as ground, not a printed band.
    --label goes beside the polar ocean at the top right, --label2 across the band of land."""
    n, frames = frames_for(seconds, still, at=0.95)
    R, CX = 3.4, -1.6                                   # left of centre so the label fits inside the frame
    for i in frames:
        u = i / max(1, n - 1)
        s = ease(u / 0.8)
        fig, ax = canvas()
        band = math.radians(8 + 37 * s)                   # the dry band widens to about 45 degrees either side
        globe(ax, CX, 0, R, i / FPS * 0.05 * (1 - s), drain=(band, s))
        label(ax, CX + R + 0.35, R * 0.8, LABELS[0], alpha=ease((u - 0.35) / 0.15), ha="left")  # beside the north polar sea
        label(ax, CX, 0, LABELS[1], alpha=ease((u - 0.6) / 0.15))
        save(fig, out, i, still)
    finish(out, still)


def render_dayyear(out, seconds, still):
    """The Sun at centre; Earth goes once round. With no spin, the gold marker on its surface keeps pointing the same
    way, so it sits in daylight for half the year, then in night for the other half."""
    n, frames = frames_for(seconds, still, at=0.4)
    R, er, CX = 3.4, 1.0, -2.0                             # fills the height; left of centre so the label fits
    for i in frames:
        th = 2 * math.pi * i / max(1, n)
        fig, ax = canvas()
        ax.add_patch(Circle((CX, 0), R, fill=False, ec=DIM, lw=1, alpha=0.4))
        for k, a in ((2.2, 0.08), (1.5, 0.2)):
            ax.add_patch(Circle((CX, 0), 0.5 * k, color=GOLD, alpha=a, lw=0))
        ax.add_patch(Circle((CX, 0), 0.5, color=GOLD))
        dx, dy = R * math.cos(th), R * math.sin(th)
        ex, ey = CX + dx, dy
        d = math.hypot(dx, dy)
        globe(ax, ex, ey, er, 0.0, night=(-dx / d, -dy / d))   # phase fixed: no spin; the night side faces away
        mx, my = ex + er, ey                                     # the marker never turns: it points the same way
        lit = -dx > 0
        ax.plot([ex + er * 0.82, mx + 0.18], [ey, my], color=GOLD if lit else DIM, lw=3, zorder=7)
        ax.add_patch(Circle((mx + 0.22, my), 0.13, color=GOLD if lit else DIM, zorder=7))
        label(ax, CX + R + er + 0.5, R * 0.8, LABELS[0], alpha=ease((i / max(1, n) - 0.08) / 0.1), ha="left")  # e.g. 1 DAY = 1 YEAR
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
        label(ax, 5.6, 0, LABELS[0], alpha=ease((u - 0.5) / 0.12))                      # e.g. 4 CM A YEAR
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
        label(ax, 5.6, 0.5, LABELS[0], alpha=ease(u / 0.1) * (1 - ease((u - 0.45) / 0.1)) if LABELS[1] else ease(u / 0.1))
        label(ax, 5.6, 0.5, LABELS[1], alpha=ease((u - 0.85) / 0.1), color=GOLD)      # e.g. 22 HOURS, then TODAY: 24
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
    ap.add_argument("--label", default="", help="words from the row's own line, 4 at most (AGENTS); placement per graphic")
    ap.add_argument("--label2", default="", help="a second label where the graphic has a place for one")
    a = ap.parse_args()
    LABELS[:] = [a.label.upper(), a.label2.upper()]
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
