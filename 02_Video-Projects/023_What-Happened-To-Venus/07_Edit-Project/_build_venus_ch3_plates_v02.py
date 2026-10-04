"""Venus 023 ch.3 plates v02, rows 37-39, no generation (Claude PR #99 5985076831). Plate A (rows 35-36) is unchanged
from v01 (Claude PASS); this script reuses _build_venus_ch3_plates_v01.py helpers for plate A framing only.

Changes from v01 (Claude 5985076831):
  1. Plate B steam-lid globe: crisp limb. The texture is blurred inside the disc only (normalised masked blur, so the
     black sky never bleeds into the edge), the disc edge is a ~2 px anti-aliased line, the outer halo is thin and
     weak, and the haze overlay is masked to the disc so it can't fuzz the edge.
  2. Row 37 (312.96-320.54, 7.58 s): plate B, two cuts, haze on. The cut to row 38 lands on "found that clouds
     gathered on the night side" (320.54 in words.json), so row 38 starts there.
  3. Row 38 (320.54-331.34, 10.80 s): code graphic `nightlid` (code_graphics.py, main 33a51f3), 0-10.80 s of the 12 s
     render. Built by code_graphics.py, not here.
  4. Old #39 slot (331.34-338.98):
       39a 331.34-335.06 (3.72 s) split screen, plate A globe left, plate B globe right, no text. This file is a
           preview; the final split can be a Remotion composite in the edit.
       39b 335.06-338.98 (3.92 s) Magellan Alpha Regio tessera, PIA00215 (NASA/JPL), slow 5% push, for
           "Nobody has yet read the rocks that could settle it" (VO "Nobody" at 335.06).
PIA23791 is lighting only (blurred), not counted towards the <=3 Mariner limit (Claude 5985076831).
Run from anywhere: uv run --with numpy --with pillow python _build_venus_ch3_plates_v02.py  (needs ffmpeg)
Outputs to ../04_Generated-Clips/01_Raw/plates_v02/ (mp4 gitignored; sheets force-added).
"""
import json, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "04_Generated-Clips", "01_Raw", "plates_v02")
SRC_A = os.path.join(HERE, "..", "04_Generated-Clips", "01_Raw", "plates_v01", "src", "nasa_ancient-venus-new.jpg")
PIA23791 = os.path.join(HERE, "nasa_pool_v01", "open", "PIA23791.jpg")
PIA00215 = os.path.join(HERE, "nasa_pool_v01", "magellan_extra", "PIA00215.jpg")
FPS, OW, OH = 30, 1920, 1080
BW, BH = 3840, 2160
os.makedirs(os.path.join(OUT, "sheets"), exist_ok=True)


def starfield(w, h, n, seed):
    r = np.random.default_rng(seed)
    bg = np.zeros((h, w, 3), np.float32); bg[:] = (3, 3, 7)
    ys, xs = r.integers(0, h, n), r.integers(0, w, n)
    br = r.random(n) ** 3 * 160 + 20
    for y, x, b in zip(ys, xs, br):
        bg[y, x] += (b, b, b * 1.05)
        if b > 120 and 0 < y < h - 1 and 0 < x < w - 1:
            bg[y - 1:y + 2, x] += b * 0.25; bg[y, x - 1:x + 2] += b * 0.25
    return Image.fromarray(bg.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))


# ---------- Plate A base (same as v01) ----------
def base_a():
    il = Image.open(SRC_A).convert("RGB").resize((BH, BH), Image.LANCZOS)
    c = starfield(BW, BH, 900, 3)
    L = np.array(il.convert("L")).astype(np.float32)
    m = Image.fromarray(((L > 10) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(12))
    full = Image.new("L", (BW, BH), 0); full.paste(m, ((BW - BH) // 2, 0))
    stars = np.array(c).astype(np.float32) * (1 - np.array(full).astype(np.float32)[..., None] / 255)
    canvas = Image.fromarray(stars.clip(0, 255).astype(np.uint8))
    ilc = np.array(il).astype(np.float32); bgc = np.array(canvas.crop(((BW - BH) // 2, 0, (BW - BH) // 2 + BH, BH))).astype(np.float32)
    canvas.paste(Image.fromarray(np.maximum(ilc, bgc).astype(np.uint8)), ((BW - BH) // 2, 0))
    return canvas


# ---------- Plate B base: steam-lid globe with a crisp limb ----------
venus_src = Image.open(PIA23791).convert("RGB").crop((0, 0, 1040, 1096))
VBOX = (94, 79, 1031, 1016)


def disc_r(d):
    yy, xx = np.mgrid[0:d, 0:d]
    return np.hypot(xx - d / 2 + 0.5, yy - d / 2 + 0.5) / (d / 2)


def steam_lid_venus_sharp(d):
    r = disc_r(d)
    inside = (r <= 0.985).astype(np.float32)          # texture sample area, kept off the dark source limb
    g = np.array(venus_src.crop(VBOX).resize((d, d), Image.LANCZOS).convert("L")).astype(np.float32) / 255.0
    rad = d * 0.09
    num = np.array(Image.fromarray((g * inside * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(rad))).astype(np.float32)
    den = np.array(Image.fromarray((inside * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(rad))).astype(np.float32)
    L = (num / np.maximum(den, 1.0)).clip(0, 1)[..., None]   # blurred texture with no black bleed at the edge
    limb = (1.0 - 0.30 * r[..., None] ** 4)                  # gentle limb darkening, edge stays bright and hard
    col = (L ** 1.1) * limb * 0.86 * np.array((0.86, 0.80, 0.52), np.float32)
    a = np.clip((1.0 - r) * d / 2.0 + 0.5, 0, 1)             # ~2 px anti-aliased edge
    rgba = np.zeros((d, d, 4), np.float32); rgba[..., :3] = col.clip(0, 1); rgba[..., 3] = a
    disc = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    pad = int(d * 0.06); big = Image.new("RGBA", (d + 2 * pad,) * 2, (0, 0, 0, 0))
    halo = Image.new("L", big.size, 0); ImageDraw.Draw(halo).ellipse((pad, pad, pad + d, pad + d), fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(d * 0.012))
    hc = Image.new("RGBA", big.size, (190, 182, 130, 0)); hc.putalpha(halo.point(lambda p: int(p * 0.22)))
    big.alpha_composite(hc); big.alpha_composite(disc, (pad, pad))
    return big


D_B, CX_B, CY_B = 1500, BW // 2, BH // 2


def base_b():
    c = starfield(BW, BH, 900, 7).convert("RGBA")
    g = steam_lid_venus_sharp(D_B)
    c.alpha_composite(g, (CX_B - g.width // 2, CY_B - g.height // 2))
    m = Image.new("L", (BW, BH), 0)                     # haze only inside the disc, feathered inward
    k = 0.995
    ImageDraw.Draw(m).ellipse((CX_B - D_B / 2 * k, CY_B - D_B / 2 * k, CX_B + D_B / 2 * k, CY_B + D_B / 2 * k), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6))
    return c.convert("RGB"), m


def haze_tex(seed, w):
    r = np.random.default_rng(seed)
    h = OH
    acc = np.zeros((h, w), np.float32)
    for cells, wt in ((6, 0.55), (14, 0.3), (34, 0.15)):
        small = r.random((cells, cells * 3)).astype(np.float32)
        acc += wt * np.array(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    return np.clip((acc - 0.35) / 0.65, 0, 1) ** 1.4


HZ1, HZ2 = haze_tex(11, OW * 3), haze_tex(12, OW * 3)
HAZE_COL = np.array((214, 204, 150), np.float32)


def haze_on(fr, mask_view, t):
    mk = np.array(mask_view).astype(np.float32)[..., None] / 255
    w = fr.width
    o1 = int(t * 22) % (OW * 2); o2 = int(OW * 2 - (t * 13) % (OW * 2))
    h = 0.6 * HZ1[:fr.height, o1:o1 + w] + 0.4 * HZ2[:fr.height, o2:o2 + w]
    a = (h[..., None] * 0.22) * mk
    f = np.array(fr).astype(np.float32)
    return Image.fromarray((f + (HAZE_COL - f) * a).clip(0, 255).astype(np.uint8))


def view_box(cx, cy, z, bw=BW, bh=BH, ow=OW, oh=OH):
    w = bw / z; h = w * oh / ow
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def lerp_seg(s, u):
    cx = s["a"][0] + (s["b"][0] - s["a"][0]) * u
    cy = s["a"][1] + (s["b"][1] - s["a"][1]) * u
    z = s["a"][2] * (s["b"][2] / s["a"][2]) ** u
    return cx, cy, z


def encoder(path):
    return subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path],
                            stdin=subprocess.PIPE)


def grid(name, frames, labels):
    tw, th = 640, 360; cols = min(3, len(frames)); rows = (len(frames) + cols - 1) // cols
    sh = Image.new("RGB", (tw * cols, th * rows), (0, 0, 0))
    for i, im in enumerate(frames):
        sh.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
        ImageDraw.Draw(sh).text(((i % cols) * tw + 8, (i // cols) * th + 6), labels[i], fill=(255, 255, 0))
    p = os.path.join(OUT, "sheets", f"{name}_grid640.jpg"); sh.save(p, quality=90); return p


def render_frames(name, make_frame, segs):
    """segs: list of dicts with 'n' frames. make_frame(seg, u, t) -> PIL RGB OWxOH."""
    p = encoder(os.path.join(OUT, f"{name}.mp4"))
    fi = 0; picks = []; labels = []; cuts = []
    for si, s in enumerate(segs):
        n = s["n"]; cuts.append(round(fi / FPS, 3))
        for k in range(n):
            u = k / max(n - 1, 1)
            fr = make_frame(s, u, fi / FPS)
            if k in (0, n // 2, n - 1):
                picks.append(fr.copy()); labels.append(f"cut {si+1} {('start','mid','end')[(0, n//2, n-1).index(k)]} @ {fi/FPS:.2f}s")
            p.stdin.write(fr.tobytes()); fi += 1
    p.stdin.close(); p.wait()
    sheet = grid(f"{name}_cuts", picks, labels)
    return {"file": f"plates_v02/{name}.mp4", "frames": fi, "duration_s": round(fi / FPS, 3), "cuts_s": cuts,
            "sheet": os.path.relpath(sheet, OUT)}


def nf(sec):
    return int(round(sec * FPS))


C = (BW / 2, BH / 2)
rep = {}

# ----- Row 37: plate B, two cuts, 312.96-320.54 = 7.58 s (227 frames: 114 + 113) -----
bb, mb = base_b(); bb.save(os.path.join(OUT, "plateB_steam_lid_sharp_base_3840.jpg"), quality=92)
B37 = [
    {"n": 114, "a": (C[0], C[1], 1.00), "b": (C[0], C[1], 1.04)},                            # whole globe, crisp limb on stars
    {"n": 113, "a": (C[0] - 330, C[1] - 90, 1.55), "b": (C[0] - 315, C[1] - 90, 1.61)},      # lit limb close, edge + sky in frame
]
def frame_b(s, u, t):
    cx, cy, z = lerp_seg(s, u); box = view_box(cx, cy, z)
    fr = bb.resize((OW, OH), Image.BICUBIC, box=box)
    return haze_on(fr, mb.resize((OW, OH), Image.BILINEAR, box=box), t)
rep["row37_plateB"] = render_frames("venus_ch3_row37_plateB_steam_lid_sharp_v02", frame_b, B37)

# ----- Row 39a: split screen A | B, 331.34-335.06 = 3.72 s (112 frames) -----
ba = base_a()
HW = OW // 2
PAD = 900
def padded(img, mode_fill, star_seed=None):
    if star_seed is None:
        c = Image.new(img.mode, (img.width + 2 * PAD, img.height + 2 * PAD), mode_fill)
    else:
        c = starfield(img.width + 2 * PAD, img.height + 2 * PAD, 1500, star_seed)
    c.paste(img, (PAD, PAD)); return c
ba_p, bb_p, mb_p = padded(ba, None, 21), padded(bb, None, 22), padded(mb, 0)
def half(base, mask, cx, cy, gd, z, t):
    cx, cy = cx + PAD, cy + PAD
    w = gd * 1.18 / z; h = w * OH / HW
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    fr = base.resize((HW, OH), Image.BICUBIC, box=box)
    if mask is not None:
        fr = haze_on(fr, mask.resize((HW, OH), Image.BILINEAR, box=box), t)
    return fr
def frame_split(s, u, t):
    z = 1.00 * (1.04 / 1.00) ** u
    left = half(ba_p, None, BW / 2, BH / 2, BH * 0.85, z, t)   # illustration globe is ~85% of the square; match the right globe size
    right = half(bb_p, mb_p, CX_B, CY_B, D_B, z, t)
    fr = Image.new("RGB", (OW, OH), (3, 3, 7)); fr.paste(left, (0, 0)); fr.paste(right, (HW, 0))
    ImageDraw.Draw(fr).rectangle((HW - 2, 0, HW + 1, OH), fill=(0, 0, 0))
    return fr
rep["row39a_split_AB"] = render_frames("venus_ch3_row39a_split_ocean_vs_steamlid_v02", frame_split, [{"n": 112}])

# ----- Row 39b: Magellan Alpha Regio tessera PIA00215, 335.06-338.98 = 3.92 s (118 frames), 5% push -----
mg = Image.open(PIA00215).convert("RGB")
mw, mh = mg.size
cw = mw; ch = cw * OH / OW
if ch > mh: ch = mh; cw = ch * OW / OH
mcx, mcy = mw / 2, mh / 2
mga = np.array(mg).astype(np.float32)
lo, hi = np.percentile(mga, 1), np.percentile(mga, 99.5)
mg = Image.fromarray(((mga - lo) / (hi - lo) * 255).clip(0, 255).astype(np.uint8))
def frame_tess(s, u, t):
    z = 1.00 * 1.05 ** u
    w = cw / z; h = ch / z
    return mg.resize((OW, OH), Image.LANCZOS, box=(mcx - w / 2, mcy - h / 2, mcx + w / 2, mcy + h / 2))
rep["row39b_tessera"] = render_frames("venus_ch3_row39b_magellan_alpha_regio_tessera_PIA00215_v02", frame_tess, [{"n": 118}])

rep["notes"] = {"row38": "nightlid from code_graphics.py (main 33a51f3), use 0-10.80 s of 12 s render",
                "pia00215": "Magellan radar, Alpha Regio tessera, NASA/JPL. Percentile stretch only (1-99.5%), no colour grade.",
                "pia23791": "lighting only, blurred; not counted towards the <=3 Mariner limit"}
json.dump(rep, open(os.path.join(HERE, "plates_report_ch3_v02.json"), "w"), indent=2)
print(json.dumps(rep, indent=2))
