#!/usr/bin/env python3
"""Code-drawn graphics for the Venus film (023). 1920x1080, 30 fps, PNG frames then MP4. Text-free by design.

  python3 code_graphics.py albedo    out/   # ch.1 "The Twin Next Door": sunlight in, reflected, absorbed (Venus above, Earth below)
  python3 code_graphics.py deuterium out/   # ch.3 "Where Did the Water Go?": water split high up, light H escapes, heavy D stays
  python3 code_graphics.py line      out/   # ch.4 "The Line Earth Hasn't Crossed": the inner limit moves out as the Sun brightens
  python3 code_graphics.py nightlid  out/   # ch.3 Turbet 2021 beat: clouds gather on the night side and hold the heat in
  python3 code_graphics.py all       out/
  add --still to write one frame only (review); --seconds N to change length

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
import argparse, math, os, subprocess, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge

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
    return fig, ax


def render_albedo(out, seconds, still):
    """Photons stream in from the left (the Sun is off frame). Venus (top) gets 1.91x the photons; 77% bounce back.
    Earth (bottom) gets fewer; 29% bounce back. The rest are absorbed. A bar beside each planet grows with the
    expected absorbed energy, so Venus's bar ends shorter than Earth's even though more light arrived."""
    rng = np.random.default_rng(23)
    n = int(seconds * FPS)
    rows = [  # name, centre y, radius, colour, flux (W/m2), albedo
        ("venus", 1.95, 1.05, VENUS, 2601.0, 0.77),
        ("earth", -2.05, 1.10, EARTH, 1361.0, 0.29),
    ]
    PX = -0.6
    base_rate = 3.2                                  # photons per frame for 1,361 W/m2
    speed = 0.22
    photons = []                                     # [x, y, vx, vy, row, reflected]
    target = n // 2 if still else None
    absorbed_max = max(f * (1 - a) for _, _, _, _, f, a in rows)
    for i in range(n):
        for r, (_, cy, rad, _, flux, alb) in enumerate(rows):
            for _ in range(rng.poisson(base_rate * flux / 1361.0)):
                photons.append([-8.2, cy + rng.uniform(-rad * 0.95, rad * 0.95), speed, 0.0, r, False])
        keep = []
        for p in photons:
            p[0] += p[2]
            p[1] += p[3]
            _, cy, rad, _, _, alb = rows[p[4]]
            if not p[5]:
                dy = p[1] - cy
                surf = PX - math.sqrt(max(0.0, rad * rad - dy * dy))
                if p[0] >= surf:
                    if rng.random() < alb:           # reflected back out towards space
                        p[0] = surf
                        p[2] = -speed
                        p[3] = dy / rad * 0.035 + rng.normal(0, 0.008)
                        p[5] = True
                    else:                            # absorbed: becomes heat in the planet
                        continue
            if -8.5 < p[0] < 8.5 and -4.8 < p[1] < 4.8:
                keep.append(p)
        photons = keep
        if still and i != target:
            continue
        s = i / max(1, n - 1)
        fig, ax = canvas()
        for r, (_, cy, rad, col, flux, alb) in enumerate(rows):
            absorbed = flux * (1 - alb)
            warm = absorbed / absorbed_max
            ax.add_patch(Circle((PX, cy), rad * 1.18, color=HEAT, alpha=0.18 * warm * ease(s * 3), lw=0))
            ax.add_patch(Circle((PX, cy), rad, color=col, lw=0))
            # absorbed energy bar, to scale, growing as the light keeps arriving
            L = 5.2 * absorbed / absorbed_max * ease((s - 0.15) / 0.7)
            ax.add_patch(Rectangle((2.0, cy - 0.32), 5.4, 0.64, color=DIM, alpha=0.18, lw=0))
            ax.add_patch(Rectangle((2.0, cy - 0.32), L, 0.64, color=HEAT, alpha=0.9, lw=0))
        pts = np.array([[p[0], p[1], p[5]] for p in photons]) if photons else np.zeros((0, 3))
        if len(pts):
            inc = pts[pts[:, 2] == 0]
            ref = pts[pts[:, 2] == 1]
            ax.scatter(inc[:, 0], inc[:, 1], s=26, color=GOLD, alpha=0.95, lw=0)
            ax.scatter(ref[:, 0], ref[:, 1], s=26, color=WHITE, alpha=0.75, lw=0)
        save(fig, out, i, still)
    finish(out, still)


def render_deuterium(out, seconds, still):
    """A column of air. Water molecules (one O, two hydrogens) drift; light from above splits the ones that rise
    into the top band. Freed light hydrogen (small, white) shoots off the top and is gone; freed heavy hydrogen
    (larger, cyan) mostly stays. A meter on the right shows the heavy share of the hydrogen left behind."""
    rng = np.random.default_rng(230)
    n = int(seconds * FPS)
    N = 90
    mol = rng.uniform([-5.5, -4.0], [3.5, 2.6], (N, 2))
    heavy = rng.random((N, 2)) < 0.12                # exaggerated D share for the eye (see module docstring)
    alive = np.ones(N, bool)
    free = []                                        # [x, y, vx, vy, is_heavy]
    escaped_h = escaped_d = 0
    target = int(n * 0.75) if still else None
    TOP = 2.9
    h0 = int((~heavy).sum())
    d0 = int(heavy.sum())
    start_share = d0 / (h0 + d0)
    for i in range(n):
        mol[alive] += rng.normal(0, 0.035, (int(alive.sum()), 2)) + np.array([0, 0.012])
        mol[:, 0] = np.clip(mol[:, 0], -5.8, 3.8)
        mol[:, 1] = np.clip(mol[:, 1], -4.2, TOP + 0.6)
        for k in np.where(alive & (mol[:, 1] > TOP))[0]:
            if rng.random() < 0.06:                  # sunlight splits it
                alive[k] = False
                for j in range(2):
                    hv = bool(heavy[k, j])
                    free.append([mol[k, 0] + (j - 0.5) * 0.3, mol[k, 1], rng.normal(0, 0.03),
                                 (0.05 if hv else 0.16) + rng.normal(0, 0.015), hv])
        nxt = []
        for f in free:
            f[0] += f[2]
            f[1] += f[3]
            if f[4]:
                f[3] -= 0.004                        # heavy: gravity wins, it sinks back into the air below
                if f[1] < TOP - 0.4:                 # then wanders there like the rest of the air
                    f[2] = rng.normal(0, 0.03)
                    f[3] = rng.normal(0, 0.03)
                    f[1] = min(f[1], TOP - 0.4)
            f[0] = min(max(f[0], -5.8), 3.8)
            if f[1] > 4.7:
                if f[4]:
                    escaped_d += 1
                else:
                    escaped_h += 1
                continue
            nxt.append(f)
        free = nxt
        if still and i != target:
            continue
        fig, ax = canvas()
        # the top band, lit from above
        ax.add_patch(Rectangle((-6.2, TOP), 10.4, 1.9, color="#6a5cff", alpha=0.10, lw=0))
        for k in range(14):
            x = -6 + k * 0.75 + (i * 0.05) % 0.75
            ax.plot([x, x - 0.25], [4.5, TOP + 0.2], color="#9f8cff", lw=2, alpha=0.35)
        a = np.where(alive)[0]
        ax.scatter(mol[a, 0], mol[a, 1], s=150, color="#ff5a4a", lw=0, zorder=3)
        for j, dx in ((0, -0.17), (1, 0.17)):
            hv = heavy[a, j]
            ax.scatter(mol[a, 0][~hv] + dx, mol[a, 1][~hv] + 0.12, s=45, color=WHITE, lw=0, zorder=4)
            ax.scatter(mol[a, 0][hv] + dx, mol[a, 1][hv] + 0.12, s=95, color="#5fd6ff", lw=0, zorder=4)
        if free:
            fa = np.array(free, dtype=float)
            hv = fa[:, 4] > 0.5
            ax.scatter(fa[~hv, 0], fa[~hv, 1], s=45, color=WHITE, lw=0)
            ax.scatter(fa[hv, 0], fa[hv, 1], s=95, color="#5fd6ff", lw=0)
        # meter: heavy share of the hydrogen still on the planet, scaled from its start value to 3x
        h_left = h0 - escaped_h
        d_left = d0 - escaped_d
        share = d_left / max(1, h_left + d_left)
        fill = min(1.0, (share / start_share - 1) / 2.0)
        ax.add_patch(Rectangle((5.6, -3.6), 0.9, 7.0, color=DIM, alpha=0.18, lw=0))
        ax.add_patch(Rectangle((5.6, -3.6), 0.9, 7.0 * (0.12 + 0.88 * fill), color="#5fd6ff", alpha=0.9, lw=0))
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
    ap.add_argument("which", choices=["albedo", "deuterium", "line", "nightlid", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    a = ap.parse_args()
    jobs = {"albedo": (render_albedo, 12), "deuterium": (render_deuterium, 12), "line": (render_line, 12),
            "nightlid": (render_nightlid, 12)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        fn(os.path.join(a.out, name), a.seconds or secs, a.still)


if __name__ == "__main__":
    sys.exit(main())
