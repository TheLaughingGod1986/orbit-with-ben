#!/usr/bin/env python3
"""Code-drawn graphics for the Sun film (022). 1920x1080, 30 fps, rendered to PNG frames, then to MP4.

  python3 code_graphics.py zoom      out/   # ch.1 "The Climb You Cannot See": the 11-year wobble, then zoom out to the climb
  python3 code_graphics.py clocks    out/   # ch.5 recap: three clocks on one log time axis, lit in turn
  python3 code_graphics.py core      out/   # ch.2 "Brighter While It Runs Down": H -> He, core tightens, more light out
  python3 code_graphics.py all       out/
  add --still to write one middle frame only (review); --seconds N to change length; --nolabels for zoom/clocks with no text (core is text-free unless --labels)

Each run writes out/<name>/%04d.png and out/<name>.mp4 (ffmpeg, yuv420p, crf 16). Media stays out of git.

Numbers (SOURCES.md): secular brightening ~1% per 110 Myr (Schroeder & Connon Smith 2008); sunspot cycle ~11 yr,
total-irradiance swing ~0.1% peak to peak; prominences last hours to days. The zoom keeps both curves honest:
the wobble is drawn at its true size and only stops being visible because the time axis widens.
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
WHITE = "#f4efe6"
DIM = "#8a8f9c"
YEAR = 1.0
CLIMB_PER_YEAR = 1.0 / 110e6          # percent per year
CYCLE = 11.0                          # years
WOBBLE = 0.05                         # percent, half of the ~0.1% peak-to-peak swing


def fig_ax():
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0.08, 0.14, 0.86, 0.74], facecolor=BG)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=DIM, labelsize=26, length=0, pad=14)
    return fig, ax


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, t)))


def brightness(t_years):
    """Percent above today's light: the slow climb plus the 11-year wobble."""
    return CLIMB_PER_YEAR * t_years + WOBBLE * np.sin(2 * np.pi * t_years / CYCLE)


def fmt_years(y):
    if y >= 1e9:
        return f"{y / 1e9:g} billion years"
    if y >= 1e6:
        return f"{y / 1e6:g} million years"
    if y >= 1e3:
        return f"{y / 1e3:g} thousand years"
    return f"{y:g} years"


def render_zoom(out, seconds, still, labels):
    """Hold 3 s on 33 years of wobble, then widen the window (log-eased) to 1.1 billion years."""
    n = int(seconds * FPS)
    hold = int(3 * FPS)
    frames = [n // 2] if still else range(n)
    span0, span1 = 33.0, 1.1e9
    for i in frames:
        p = 0 if i < hold else ease((i - hold) / max(1, n - hold - FPS))
        span = math.exp(math.log(span0) + p * (math.log(span1) - math.log(span0)))
        t = np.linspace(0, span, 4000)
        y = brightness(t)
        fig, ax = fig_ax()
        cycles_per_px = span / CYCLE / 1650.0
        top = max(WOBBLE * 1.8, CLIMB_PER_YEAR * span * 1.1)
        ax.set_xlim(0, span)
        ax.set_ylim(-top * (0.9 - 0.78 * ease((p - 0.3) / 0.4)), top)
        if cycles_per_px < 0.25:
            ax.plot(t, y, color=GOLD, lw=3.2, solid_capstyle="round")
        else:
            # finer than a pixel: draw the wobble as the band it really is (climb +/- 0.05%), no aliasing
            base = CLIMB_PER_YEAR * t
            ax.fill_between(t, base - WOBBLE, base + WOBBLE, color=GOLD, alpha=0.9, lw=0)
            ax.plot(t, base, color="#fff1c8", lw=3.2, solid_capstyle="round")
        ax.axhline(0, color=DIM, lw=1, alpha=0.5)
        ax.set_yticks([])
        ax.set_xticks([0, span])
        nice = float(f"{span:.2g}")
        ax.set_xticklabels(["today", fmt_years(nice)] if labels else ["", ""])
        ax.get_xticklabels()[0].set_ha("left")
        ax.get_xticklabels()[-1].set_ha("right")
        if labels:
            a = 1 - ease(p * 3)          # wobble label fades as the climb takes over
            b = ease((p - 0.55) / 0.3)
            if a > 0.02:
                fig.text(0.5, 0.92, "the 11-year wobble: about 0.1%", color=WHITE, alpha=a, ha="center", fontsize=34)
            if b > 0.02:
                fig.text(0.5, 0.92, "the climb: about 1% every 110 million years", color=GOLD, alpha=b, ha="center", fontsize=34)
        save(fig, out, i, still)
    finish(out, still)


def render_clocks(out, seconds, still, labels):
    """Log time axis from an hour to 2 billion years; three markers light up in turn, the third stays."""
    n = int(seconds * FPS)
    marks = [(3 / 365.25, "a prominence", "days", WHITE),
             (11.0, "the sunspot wobble", "11 years, up and down", WHITE),
             (110e6, "the climb", "+1% every 110 million years", GOLD)]
    frames = [int(n * 0.8)] if still else range(n)
    for i in frames:
        s = i / n
        fig, ax = fig_ax()
        ax.set_xscale("log")
        ax.set_xlim(1 / (365.25 * 24), 2e9)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.axhline(0.40, color=DIM, lw=2, alpha=0.7)
        ticks = [1 / (365.25 * 24), 1 / 365.25, 1, 1e3, 1e6, 1e9]
        ax.set_xticks(ticks)
        ax.set_xticklabels(["hour", "day", "year", "1,000 yr", "1 Myr", "1 Gyr"] if labels else [""] * 6)
        for k, (x, name, sub, col) in enumerate(marks):
            on = ease((s - (0.08 + 0.25 * k)) / 0.12)
            fade = 1.0 if k == 2 else 1 - 0.65 * ease((s - (0.33 + 0.25 * k)) / 0.15)
            alpha = on * fade
            if alpha < 0.02:
                continue
            ax.scatter([x], [0.40], s=600 if k == 2 else 380, color=col, alpha=alpha, zorder=3,
                       edgecolors="none")
            if labels:
                # the prominence label sits under the line so it never collides with the 11-year one
                y1, y2 = (0.22, 0.13) if k == 0 else (0.62, 0.52)
                xt, ha = (1.9e9, "right") if k == 2 else (x, "center")
                ax.text(xt, y1, name, color=col, alpha=alpha, ha=ha, fontsize=34)
                ax.text(xt, y2, sub, color=col, alpha=alpha * 0.85, ha=ha, fontsize=24)
        save(fig, out, i, still)
    finish(out, still)


def render_core(out, seconds, still, labels):
    """A cut-away Sun: core particles, hydrogen (small, many) fusing four-to-one into helium (larger, fewer).
    As helium builds up, the core radius eases down ~12%, its glow warms, and the light rays leaving the
    photosphere lengthen and brighten. No text by default (the VISUAL MUST says no text on the plate)."""
    rng = np.random.default_rng(22)
    n = int(seconds * FPS)
    frames = [int(n * 0.7)] if still else range(n)
    R_SUN, R_CORE0 = 2.7, 1.25
    N_H = 420
    pos = rng.uniform(-1, 1, (N_H, 2))
    pos = pos[np.hypot(pos[:, 0], pos[:, 1]) < 1][:300]
    vel = rng.normal(0, 0.004, pos.shape)
    order = rng.permutation(len(pos))
    for i in frames:
        s = i / max(1, n - 1)
        he_frac = ease(s) * 0.6                        # up to 60% of hydrogen fused, four at a time
        n_fused = int(len(pos) * he_frac) // 4 * 4
        r_core = R_CORE0 * (1 - 0.12 * ease(s))
        lum = 1 + 0.35 * ease(s)                       # exaggerated for the eye; the VO carries the real 1%
        fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
        ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
        ax.set_xlim(-8, 8)
        ax.set_ylim(-4.5, 4.5)
        ax.set_aspect("equal")
        ax.axis("off")
        # light leaving the photosphere
        for k in range(48):
            a = 2 * np.pi * k / 48
            L = (0.6 + 0.5 * ((k * 7) % 5) / 5) * lum ** 2
            ax.plot([R_SUN * np.cos(a), (R_SUN + L) * np.cos(a)], [R_SUN * np.sin(a), (R_SUN + L) * np.sin(a)],
                    color=GOLD, lw=3.0, alpha=min(1, 0.45 * lum), solid_capstyle="round")
        # the star, cut away
        for rr, al in [(R_SUN, 0.95), (R_SUN * 0.75, 0.6), (R_SUN * 0.5, 0.5)]:
            ax.add_patch(Circle((0, 0), rr, color="#c96a12" if rr < R_SUN else "#e88a1a", alpha=al, lw=0))
        glow = min(1, 0.55 + 0.35 * ease(s))
        ax.add_patch(Circle((0, 0), r_core * 1.25, color="#ffdd88", alpha=0.35 * glow, lw=0))
        ax.add_patch(Circle((0, 0), r_core, color="#fff1c8", alpha=glow, lw=0))
        # particles jiggle inside the (shrinking) core
        t = i if not still else int(n * 0.7)
        p = pos + vel * t
        p = (p + 1) % 2 - 1
        p = p[np.hypot(p[:, 0], p[:, 1]) < 1] if False else p
        fused = set(order[:n_fused].tolist())
        h_idx = [k for k in range(len(p)) if k not in fused]
        he_groups = [order[j:j + 4] for j in range(0, n_fused, 4)]
        hx = p[h_idx] * r_core * 0.9
        ax.scatter(hx[:, 0], hx[:, 1], s=30, color="#ff7a2c", alpha=0.95, lw=0)
        if he_groups:
            he = np.array([p[g].mean(axis=0) for g in he_groups]) * r_core * 0.9
            ax.scatter(he[:, 0], he[:, 1], s=120, color="#5fc4ff", alpha=0.95, lw=0)
            prev = int(len(pos) * ease(max(0, s - 8 / n)) * 0.6) // 4 * 4   # fused 8 frames ago
            new = he[prev // 4:]
            if len(new):
                ax.scatter(new[:, 0], new[:, 1], s=520, color="white", alpha=0.35, lw=0)   # the flash of each fusion
        if labels:
            ax.text(0, -4.2, "4 hydrogen -> 1 helium: the core tightens, heats and burns faster", color=WHITE,
                    ha="center", fontsize=30)
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
    ap.add_argument("which", choices=["zoom", "clocks", "core", "all"])
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--still", action="store_true")
    ap.add_argument("--nolabels", action="store_true")
    ap.add_argument("--labels", action="store_true", help="core only: add the one-line caption")
    a = ap.parse_args()
    jobs = {"zoom": (render_zoom, 12), "clocks": (render_clocks, 10), "core": (render_core, 12)}
    for name in (jobs if a.which == "all" else [a.which]):
        fn, secs = jobs[name]
        # the core plate defaults to no text (script: "No text on the plate"); --labels adds its caption line
        labels = a.labels if name == "core" else not a.nolabels
        fn(os.path.join(a.out, name + ("" if labels else "_nolabels")), a.seconds or secs, a.still, labels)


if __name__ == "__main__":
    sys.exit(main())
