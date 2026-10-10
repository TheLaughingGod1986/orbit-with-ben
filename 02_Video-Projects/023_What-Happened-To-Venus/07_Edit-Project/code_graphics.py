#!/usr/bin/env python3
"""Code-drawn graphics for the Venus film (023). 1920x1080, 30 fps, PNG frames then MP4.

AGENTS (9 Oct, Ben's v05c notes): every graphic must read with the sound off: real bodies, short labels from the
line being spoken (4 words at most), one idea at a time, timed to the voice.

  python3 code_graphics.py albedo    out/   # rows 13c-14b, 18.1 s: sunlight in (Venus ~2x) -> 77% bounced back -> Venus soaks up less
  python3 code_graphics.py heavyh    out/   # row 31, 10.9 s: hydrogen vs heavy hydrogen; Venus has ~100x the share Earth has
  python3 code_graphics.py deuterium out/   # rows 32a-32b, 13.3 s: sunlight splits water high up; light H escapes, heavy H stays
  python3 code_graphics.py line      out/   # ch.4 "The Line Earth Hasn't Crossed": the inner limit moves out as the Sun brightens
  python3 code_graphics.py nightlid  out/   # ch.3 Turbet 2021 beat: clouds gather on the night side and hold the heat in
  python3 code_graphics.py all       out/
  add --still to write one frame only (review); --seconds N to change length

Real bodies (put these next to this file, out of git):
  venus_disc.jpg   NASA PIA23791 (Mariner 10, 1974), https://images-assets.nasa.gov/image/PIA23791/PIA23791~orig.jpg
                   The left, natural-colour panel is used (the script crops it).
  blue_marble.jpg  NASA Blue Marble Next Generation, the same file as 027's code graphics (see 027 code_graphics.py).
Labels use Arial Bold (the house type), falling back to DejaVu Sans Bold.

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (01_Script/SOURCES.md, NASA NSSDCA fact sheets):
  albedo     Venus gets 2,601 W/m2 and reflects 0.77 (Bond); Earth gets 1,361 W/m2 and reflects 0.29.
             Photon rates and the absorbed bars are drawn to those ratios: Venus absorbs ~598, Earth ~966.
  deuterium  Pioneer Venus D/H ~100x Earth's. Real D is ~1 in 6,000 hydrogen on Earth, far too rare to see,
             so the starting share of D is exaggerated for the eye. What is honest is the direction: H escapes
             much more easily than D, so the D share climbs as the water is lost.
  line       Inner (moist-greenhouse) limit ~0.95 AU for today's Sun, scaling as sqrt(L) (Kopparapu et al. 2013).
             The Sun climbs from L=1.0 to L=1.1 (~1 billion years, Schroeder & Connon Smith 2008), which moves the
             limit to ~1.0 AU, Earth's orbit. Venus (0.72 AU) is already inside.
  nightlid   Turbet et al. 2021: on a slowly rotating young Venus, water clouds gather on the night side, where
             they warm the planet (they block outgoing heat) instead of shading the day side. Drawn as a lit day half,
             steam rising, cloud building over the night half, and heat arrows from the night side turned back down.
"""
import argparse, logging, math, os, subprocess, sys
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge, FancyArrow

W, H, DPI, FPS = 1920, 1080, 120, 30
BG = "#05060a"
GOLD = "#ffc94a"
WHITE = "#f4efe6"
DIM = "#8a8f9c"
VENUS = "#e8d29a"
EARTH = "#3a7bd5"
HEAT = "#ff8a3a"


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, t)))


def canvas():
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.imshow(backdrop(), extent=(-8, 8, -4.5, 4.5), zorder=0, interpolation="bilinear")
    return fig, ax


_BACK = []


def backdrop():
    """A deep warm-to-slate radial grade (luma ~34-60), so no graphic is mostly near-black (Chief, 10 Oct)."""
    if not _BACK:
        yy, xx = np.mgrid[0:270, 0:480].astype(np.float32)
        r = np.clip(np.hypot((xx - 240) / 290, (yy - 120) / 200), 0, 1)[..., None]
        _BACK.append((np.array([74, 56, 50]) * (1 - r) + np.array([34, 32, 46]) * r) / 255.0)
    return _BACK[0]


HERE = os.path.dirname(os.path.abspath(__file__))
_IMG = {}
CYAN = "#5fd6ff"
FONT = {"family": ["Arial", "Helvetica", "DejaVu Sans"], "weight": "bold"}


def _load(name, env):
    if name not in _IMG:
        from PIL import Image
        path = os.environ.get(env) or os.path.join(HERE, name)
        if not os.path.exists(path):
            sys.exit(f"missing {path} (see the docstring for the NASA download)")
        im = Image.open(path).convert("RGB")
        if name == "venus_disc.jpg" and im.width > 1.6 * im.height:
            im = im.crop((0, 0, int(im.width * 0.46), im.height))   # PIA23791: the natural-colour panel only
        _IMG[name] = im
    return _IMG[name]


def disc_rgba(px):
    """The real Venus (Mariner 10) cropped tight to its disc, px square, with a round alpha edge."""
    key = ("venus", px)
    if key not in _IMG:
        im = _load("venus_disc.jpg", "VENUS_DISC")
        a = np.asarray(im.convert("L"), dtype=np.float32)
        a[:, -int(a.shape[1] * 0.04):] = 0                          # ignore the panel's right edge
        ys, xs = np.where(a > 40)
        cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2
        im = im.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((px, px))
        rgb = np.asarray(im, dtype=np.float32) / 255.0
        u = np.linspace(-1, 1, px)
        rr = u[None, :] ** 2 + u[:, None] ** 2
        alpha = np.clip((1 - rr) * px * 0.5, 0, 1)
        _IMG[key] = np.dstack([rgb, alpha])
    return _IMG[key]


def earth_rgba(px, phase=0.6):
    """The real Earth (Blue Marble NG), orthographic, px square."""
    key = ("earth", px, phase)
    if key not in _IMG:
        tex = np.asarray(_load("blue_marble.jpg", "BLUE_MARBLE").reduce(2), dtype=np.float32) / 255.0
        th, tw = tex.shape[:2]
        u = np.linspace(-1, 1, px)[None, :].repeat(px, 0)
        v = np.linspace(1, -1, px)[:, None].repeat(px, 1)
        rr = u ** 2 + v ** 2
        z = np.sqrt(np.clip(1 - rr, 0, None))
        lat = np.arcsin(np.clip(v, -1, 1))
        lon = np.arctan2(u, z) - phase
        ty = ((0.5 - lat / math.pi) * (th - 1)).astype(np.int32)
        tx = (((lon / (2 * math.pi) + 0.5) % 1.0) * (tw - 1)).astype(np.int32)
        rgb = tex[ty, tx] * (0.55 + 0.45 * z)[..., None]
        _IMG[key] = np.dstack([rgb, np.clip((1 - rr) * px * 0.5, 0, 1) * (rr <= 1)])
    return _IMG[key]


def body(ax, which, x, y, r):
    px = int(round(2 * r * H / 9.0))
    img = disc_rgba(px) if which == "venus" else earth_rgba(px)
    ax.imshow(img, extent=(x - r, x + r, y - r, y + r), zorder=3, interpolation="bilinear")


HOUSE_PT = 60                                            # ~100 px at 1080: ~11-12% of frame height per line


def label(ax, x, y, text, size=None, color=WHITE, alpha=1.0, ha="left", va="center"):
    if alpha <= 0.01:
        return
    ax.text(x, y, text, color=color, alpha=alpha, fontsize=HOUSE_PT, ha=ha, va=va, zorder=9, fontdict=FONT,
            bbox=dict(facecolor=BG, alpha=0.7 * alpha, edgecolor="none", boxstyle="round,pad=0.25"))


def phase_alpha(t, start, fade=0.6):
    return ease((t - start) / fade)


def render_albedo(out, seconds, still):
    """Timed to rows 13c-14b (78.2-96.3 s, 18.1 s):
      0-5.4 s   "...nearer the fire. But that answer breaks on one number."  Sunlight arrives; Venus gets about twice as
                much. Bars: SUNLIGHT IN, Venus 1.9 against Earth 1.0.
      5.4-11.8  "...bright cloud that reflects about three-quarters of that sunlight straight back"  White photons
                bounce off Venus (77%), far fewer off Earth (29%). Labels say so.
      11.8-18.1 "...back to space. So Venus actually soaks up less sunlight than Earth does."  The bars turn into
                SOAKED UP: Venus 598 W/m2 against Earth 966. Venus's bar ends shorter.
    Numbers: NSSDCA fact sheets (Venus 2,601 W/m2, Bond albedo 0.77; Earth 1,361, 0.29)."""
    rng = np.random.default_rng(23)
    n = int(seconds * FPS)
    k = seconds / 18.1                                   # stretch the beats if a different length is asked for
    T_BOUNCE, T_SOAK = 5.4 * k, 11.8 * k
    rows = [("venus", 1.55, 1.15, 2601.0, 0.77, "VENUS", "77% BOUNCED BACK"),
            ("earth", -2.45, 1.15, 1361.0, 0.29, "EARTH", "29% BOUNCED BACK")]
    PX, BX, BL = -5.2, 0.2, 7.4                          # disc x; bar start and full length
    base_rate, speed = 2.6, 0.24
    photons = []
    target = int(n * 0.85) if still else None
    for i in range(n):
        t = i / FPS
        bounce_on = t >= T_BOUNCE
        for r, (_, cy, rad, flux, alb, _, _) in enumerate(rows):
            for _ in range(rng.poisson(base_rate * flux / 1361.0)):
                photons.append([-8.3, cy + rng.uniform(-rad * 0.9, rad * 0.9), speed, 0.0, r, False])
        keep = []
        for p in photons:
            p[0] += p[2]
            p[1] += p[3]
            _, cy, rad, _, alb, _, _ = rows[p[4]]
            if not p[5]:
                dy = p[1] - cy
                surf = PX - math.sqrt(max(0.0, rad * rad - dy * dy))
                if p[0] >= surf:
                    if bounce_on and rng.random() < alb:
                        p[0], p[2], p[5] = surf, -speed, True
                        p[3] = dy / rad * 0.04 + rng.normal(0, 0.01)
                    else:
                        continue
            if -8.5 < p[0] < 8.5 and -4.8 < p[1] < 4.8:
                keep.append(p)
        photons = keep
        if still and i != target:
            continue
        fig, ax = canvas()
        pts = np.array([[p[0], p[1], p[5]] for p in photons]) if photons else np.zeros((0, 3))
        if len(pts):
            inc, ref = pts[pts[:, 2] == 0], pts[pts[:, 2] == 1]
            ax.scatter(inc[:, 0], inc[:, 1], s=22, color=GOLD, alpha=0.9, lw=0, zorder=2)
            ax.scatter(ref[:, 0], ref[:, 1], s=26, color=WHITE, alpha=0.85, lw=0, zorder=2)
        soak = ease((t - T_SOAK) / 1.2)
        heading = "SUNLIGHT IN" if t < T_SOAK + 0.6 else "SOAKED UP"
        ha = phase_alpha(t, 0.3) * (1 - ease((t - T_SOAK) / 0.6)) + ease((t - T_SOAK - 0.6) / 0.6)
        label(ax, BX, 3.85, heading, color=GOLD, alpha=ha)
        for r, (which, cy, rad, flux, alb, name, bounced) in enumerate(rows):
            body(ax, which, PX, cy, rad)
            label(ax, BX, cy + 0.95, name, alpha=phase_alpha(t, 0.2))
            label(ax, 7.8, cy - 0.95, bounced, ha="right", alpha=phase_alpha(t, T_BOUNCE + 0.8))
            vin, vsoak = flux / 2601.0, flux * (1 - alb) / 2601.0
            frac = vin + (vsoak - vin) * soak
            grow = ease(t / 2.0)
            L = BL * frac * grow
            ax.add_patch(Rectangle((BX, cy - 0.36), BL, 0.72, color=DIM, alpha=0.25, lw=0, zorder=4))
            ax.add_patch(Rectangle((BX, cy - 0.36), L, 0.72, color=HEAT if t >= T_SOAK else GOLD, alpha=0.92, lw=0, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_heavyh(out, seconds, still):
    """Row 31 (236.2-247.1 s): "Some hydrogen is heavier than the rest. It is called deuterium. On Venus, the share of
    heavy hydrogen is around a hundred times higher than on Earth."
      0-4.5 s   Two atoms side by side: HYDROGEN (one proton) and HEAVY HYDROGEN (a proton and a neutron).
      4.5-end   Two samples of hydrogen: EARTH, where 1 dot in a crowd is cyan; VENUS, where many are. Label "100x MORE".
    Honest scale: on Earth about 1 hydrogen in 6,400 is heavy, far too rare to draw; so each sample shows the same
    crowd of 400 and the Earth one gets a single heavy atom, the Venus one about a hundred times the share (Donahue
    et al. 1982: D/H ~1.6e-2, ~100x Earth's). The drawing keeps the ratio between the planets, not the absolute share."""
    rng = np.random.default_rng(31)
    n = int(seconds * FPS)
    k = seconds / 10.9
    T2 = 4.5 * k
    target = int(n * 0.8) if still else None
    N = 400
    pos = {c: rng.uniform([-1.9, -1.6], [1.9, 1.6], (N, 2)) for c in ("earth", "venus")}
    heavy = {"earth": np.zeros(N, bool), "venus": np.zeros(N, bool)}
    heavy["earth"][0] = True
    heavy["venus"][rng.choice(N, 64, replace=False)] = True   # 16% drawn: ~100x Earth's 0.16%, rounded to what the eye can see
    jitter = {c: rng.normal(0, 1, (n, 2)) for c in ("earth", "venus")}
    for i in range(n):
        if still and i != target:
            continue
        t = i / FPS
        fig, ax = canvas()
        a1 = phase_alpha(t, 0.2) * (1 - ease((t - T2) / 0.6))
        if a1 > 0.01:
            for x, heavy_atom, name in ((-3.4, False, "HYDROGEN"), (3.4, True, "HEAVY HYDROGEN")):
                ax.add_patch(Circle((x, 0.3), 2.0, fill=False, ec=DIM, lw=1.5, alpha=0.5 * a1, zorder=3))
                wob = 0.05 * math.sin(t * 3 + x)
                ax.add_patch(Circle((x - (0.32 if heavy_atom else 0) + wob, 0.3), 0.42, color="#ff5a4a", alpha=a1, zorder=4))
                if heavy_atom:
                    ax.add_patch(Circle((x + 0.32 - wob, 0.3), 0.42, color="#c9c9cf", alpha=a1, zorder=4))
                ang = t * 2.2 + x
                ax.add_patch(Circle((x + 2.0 * math.cos(ang), 0.3 + 2.0 * math.sin(ang)), 0.14, color=CYAN if heavy_atom else WHITE, alpha=a1, zorder=5))
                label(ax, x, -2.55, name, ha="center", color=CYAN if heavy_atom else WHITE, alpha=a1)
        a2 = ease((t - T2 - 0.3) / 0.8)
        if a2 > 0.01:
            for c, cx, name in (("earth", -3.9, "EARTH"), ("venus", 3.9, "VENUS")):
                p = pos[c] + 0.03 * jitter[c][i]
                ax.add_patch(Rectangle((cx - 2.1, -1.8), 4.2, 3.6, fill=False, ec=DIM, lw=1.5, alpha=0.5 * a2, zorder=2))
                lt = ~heavy[c]
                ax.scatter(cx + p[lt, 0], p[lt, 1], s=14, color=WHITE, alpha=0.75 * a2, lw=0, zorder=3)
                ax.scatter(cx + p[heavy[c], 0], p[heavy[c], 1], s=60, color=CYAN, alpha=a2, lw=0, zorder=4)
                label(ax, cx, -2.55, name, ha="center", alpha=a2)
            label(ax, 3.9, 2.6, "100x MORE", ha="center", color=CYAN, alpha=ease((t - T2 - 2.5) / 0.8))
        save(fig, out, i, still)
    finish(out, still)


def render_deuterium(out, seconds, still):
    """Rows 32a-32b (247.1-260.4 s): "That number is a fingerprint. High in the air, sunlight breaks water apart. The
    light hydrogen escapes to space more easily than the heavy kind. Lose enough water that way..."
    The real Venus sits low in frame; above it the high air, lit from the Sun on the left. Water molecules drift up,
    sunlight splits them; white (light) hydrogen streams off the top, labelled ESCAPES TO SPACE; cyan (heavy)
    hydrogen sinks back, labelled HEAVY STAYS. Labels come in as the voice says each part."""
    rng = np.random.default_rng(230)
    n = int(seconds * FPS)
    k = seconds / 13.3
    T_SPLIT, T_ESC = 2.2 * k, 6.3 * k
    target = int(n * 0.8) if still else None
    VY, VR = -9.2, 6.2                                # Venus's limb arcs across the bottom of the frame
    N = 70
    mol = np.column_stack([rng.uniform(-6.5, 6.5, N), rng.uniform(-3.0, 0.5, N)])
    heavy = rng.random((N, 2)) < 0.16
    alive = np.ones(N, bool)
    free = []
    for i in range(n):
        t = i / FPS
        mol[alive] += rng.normal(0, 0.02, (int(alive.sum()), 2)) + np.array([0, 0.018])
        mol[:, 0] = np.clip(mol[:, 0], -6.8, 6.8)
        for kk in np.where(alive & (mol[:, 1] > 1.2))[0]:
            if t > T_SPLIT and rng.random() < 0.08:
                alive[kk] = False
                for j in range(2):
                    hv = bool(heavy[kk, j])
                    free.append([mol[kk, 0] + (j - 0.5) * 0.3, mol[kk, 1], rng.normal(0, 0.02),
                                 (0.0 if hv else 0.14) + rng.normal(0, 0.01), hv])
            elif mol[kk, 1] > 2.2:
                mol[kk, 1] = 2.2
        if alive.sum() < N * 0.35:                     # keep the air supplied: new water rises from below
            dead = np.where(~alive)[0][:6]
            alive[dead] = True
            mol[dead] = np.column_stack([rng.uniform(-6.5, 6.5, len(dead)), np.full(len(dead), -3.0)])
        nxt = []
        for f in free:
            f[0] += f[2]
            f[1] += f[3]
            if f[4]:
                f[3] = max(f[3] - 0.006, -0.05)
                if f[1] < 0.6:
                    f[3] = abs(rng.normal(0, 0.01))
            if f[1] > 4.8:
                continue
            nxt.append(f)
        free = nxt
        if still and i != target:
            continue
        fig, ax = canvas()
        body(ax, "venus", 0, VY, VR)
        sun = phase_alpha(t, T_SPLIT - 1.0)
        for kk in range(10):
            y = 1.2 + kk * 0.32
            ax.plot([-8, -7.2 + (t * 2 % 1.0)], [y, y - 0.05], color=GOLD, lw=2, alpha=0.35 * sun, zorder=2)
        ax.add_patch(Rectangle((-8, 1.2), 16, 3.3, color=GOLD, alpha=0.05 * sun, lw=0, zorder=1))
        a = np.where(alive)[0]
        ax.scatter(mol[a, 0], mol[a, 1], s=150, color="#ff5a4a", lw=0, zorder=4)
        for j, dx in ((0, -0.17), (1, 0.17)):
            hv = heavy[a, j]
            ax.scatter(mol[a, 0][~hv] + dx, mol[a, 1][~hv] + 0.12, s=45, color=WHITE, lw=0, zorder=5)
            ax.scatter(mol[a, 0][hv] + dx, mol[a, 1][hv] + 0.12, s=95, color=CYAN, lw=0, zorder=5)
        if free:
            fa = np.array(free, dtype=float)
            hv = fa[:, 4] > 0.5
            ax.scatter(fa[~hv, 0], fa[~hv, 1], s=45, color=WHITE, lw=0, zorder=5)
            ax.scatter(fa[hv, 0], fa[hv, 1], s=95, color=CYAN, lw=0, zorder=5)
        label(ax, -7.6, 3.85, "SUNLIGHT SPLITS WATER", color=GOLD, alpha=phase_alpha(t, T_SPLIT))
        label(ax, 7.6, 2.65, "ESCAPES TO SPACE", ha="right", alpha=phase_alpha(t, T_ESC))
        label(ax, 7.6, 0.3, "HEAVY STAYS", ha="right", color=CYAN, alpha=phase_alpha(t, T_ESC + 1.5))
        save(fig, out, i, still)
    finish(out, still)


def render_line(out, seconds, still):
    """The Sun at left, Venus and Earth on their orbits (arcs). A hot zone reaches out from the Sun to the inner
    limit (sqrt(L) scaling). Over the clip the Sun brightens from today to +10% and the limit's edge slides out
    from ~0.95 AU to Earth's orbit. Venus sits inside the whole time."""
    n = int(seconds * FPS)
    SX = -7.4
    scale = 11.0                                     # canvas units per AU
    frames = [int(n * 0.85)] if still else range(n)
    for i in frames:
        s = ease((i / max(1, n - 1) - 0.12) / 0.8)
        L = 1.0 + 0.10 * s
        limit = 0.95 * math.sqrt(L)
        fig, ax = canvas()
        ax.add_patch(Wedge((SX, 0), limit * scale, -40, 40, color=HEAT, alpha=0.16, lw=0))
        ax.add_patch(Wedge((SX, 0), limit * scale, -40, 40, width=0.18, color=HEAT, alpha=0.85, lw=0))
        for a_au, col, r in ((0.723, VENUS, 0.22), (1.0, EARTH, 0.24)):
            th = np.linspace(-0.62, 0.62, 200)
            R = a_au * scale
            ax.plot(SX + R * np.cos(th), R * np.sin(th), color=DIM, lw=1.6, alpha=0.6)
            ax.add_patch(Circle((SX + R, 0), r, color=col, lw=0, zorder=4))
        glow = 0.55 + 0.35 * s
        for rr, al in ((1.9, 0.10 * glow), (1.4, 0.22 * glow), (1.0, 0.95)):
            ax.add_patch(Circle((SX, 0), rr, color=GOLD, alpha=al, lw=0, zorder=5))
        save(fig, out, i, still)
    finish(out, still)


def render_nightlid(out, seconds, still):
    """A planet seen side-on, Sun off frame left. Steam rises everywhere; over the clip cloud builds over the night
    (right) half only. Heat arrows leave the night side: early on they escape to space, later they hit the cloud and
    turn back down, and the surface glow warms. Text-free."""
    rng = np.random.default_rng(2021)
    n = int(seconds * FPS)
    R = 2.6
    frames = [int(n * 0.8)] if still else range(n)
    steam = [[rng.uniform(-R, R), rng.uniform(-R, R), rng.uniform(0, 1)] for _ in range(70)]
    for i in frames:
        s = ease(i / max(1, n - 1))
        fig, ax = canvas()
        # planet: day half lit, night half dark, surface glow warms with s
        ax.add_patch(Circle((0, 0), R, color="#241a14", lw=0))
        ax.add_patch(Wedge((0, 0), R, 90, 270, color="#c9a46a", lw=0, alpha=0.95))
        ax.add_patch(Circle((0, 0), R * 0.98, color=HEAT, alpha=0.05 + 0.25 * s, lw=0))
        # steam: small pale dots drifting outwards from the surface
        t = i / FPS
        for sx, sy, ph in steam:
            a = math.atan2(sy, sx)
            r = R * 0.6 + ((t * 0.25 + ph) % 1.0) * R * 0.7
            ax.add_patch(Circle((r * math.cos(a), r * math.sin(a)), 0.05, color=WHITE, alpha=0.35, lw=0))
        # cloud deck building over the night side only
        for k in range(18):
            a = math.radians(-80 + k * 160 / 17)
            rr = R + 0.35 + 0.15 * math.sin(k * 1.7)
            ax.add_patch(Circle((rr * math.cos(a), rr * math.sin(a)), 0.32 + 0.12 * ((k * 5) % 3) / 2,
                                color=WHITE, alpha=0.72 * ease((s - 0.1 - k * 0.01) / 0.5), lw=0, zorder=3))
        # heat arrows from the night side: escape early, bounce back later
        for k in range(6):
            a = math.radians(-50 + k * 20)
            x0, y0 = R * math.cos(a), R * math.sin(a)
            blocked = s > 0.45 + 0.03 * k
            ph = ((t * 0.9 + k * 0.17) % 1.0)
            if not blocked:
                L = 0.4 + ph * 2.2
                ax.plot([x0, (R + L) * math.cos(a)], [y0, (R + L) * math.sin(a)], color=HEAT, lw=4.5, alpha=0.95, zorder=6)
            else:
                up = min(ph * 2, 1.0) * 0.45
                down = max(0.0, ph * 2 - 1.0) * 0.45
                ax.plot([x0, (R + up) * math.cos(a)], [y0, (R + up) * math.sin(a)], color=HEAT, lw=4.5, alpha=0.95, zorder=6)
                if down > 0:
                    b = a + 0.12
                    ax.plot([(R + 0.45) * math.cos(a), (R + 0.45 - down) * math.cos(b)],
                            [(R + 0.45) * math.sin(a), (R + 0.45 - down) * math.sin(b)], color=HEAT, lw=4.5, alpha=0.95, zorder=6)
        # the Sun's light arriving on the day side
        for k in range(7):
            y = -2.2 + k * 0.73
            x_edge = -math.sqrt(max(0.0, R * R - y * y))
            ax.plot([-8, x_edge - 0.1], [y, y], color=GOLD, lw=2, alpha=0.35)
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
    ap.add_argument("which", choices=["albedo", "heavyh", "deuterium", "line", "nightlid", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    jobs = {"albedo": (render_albedo, 18.1), "heavyh": (render_heavyh, 10.9), "deuterium": (render_deuterium, 13.3), "line": (render_line, 12),
            "nightlid": (render_nightlid, 12)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
