"""Venus 023 ch.3 plates #35-#38 (+ dropped #39 slot), no generation (Claude PR #99 5984968873).

Plate A  rows 35-36 (291.78-312.96, 21.18 s): NASA's own illustration of ancient Venus with a shallow
         ocean, from the Way et al. 2016 GISS release "NASA Climate Modeling Suggests Venus May Have
         Been Habitable" (11 Aug 2016). Credit: NASA. Source:
         https://www.nasa.gov/wp-content/uploads/2016/08/ancient-venus-new.jpg (4096x4096,
         sha1 696b521b8f694557676b7e72bab9f5404553aa4a).
Plate B  rows 37-38 + #39 slot (312.96-338.98, 26.02 s): the v02 steam-lid globe (dim sulphur-yellow/grey,
         flat featureless; Mariner 10 PIA23791 lighting only, texture blurred out; same recipe as
         _composite_venus_orbit_start_39_v02.py::steam_lid_venus) as a still, slow pushes, plus a light
         drifting haze overlay. The haze here is a preview of the edit-side Remotion noise layer.
Cuts are 4-6 s (SHOT_LIST VISUAL MUST): hard cuts between framings of the same still; each framing
pushes in slowly (about 1% per second).
Run: uv run --with numpy --with pillow python _build_venus_ch3_plates_v01.py  (needs ffmpeg)
"""
import subprocess, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

FPS, OW, OH = 30, 1920, 1080
BW, BH = 3840, 2160
rng = np.random.default_rng(35)

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

# ---------- Plate A base: NASA illustration on black + masked stars ----------
def base_a():
    il = Image.open("nasa_ancient-venus-new.jpg").convert("RGB").resize((BH, BH), Image.LANCZOS)
    c = starfield(BW, BH, 900, 3)
    L = np.array(il.convert("L")).astype(np.float32)
    m = Image.fromarray(((L > 10) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(12))
    full = Image.new("L", (BW, BH), 0); full.paste(m, ((BW - BH) // 2, 0))
    stars = np.array(c).astype(np.float32) * (1 - np.array(full).astype(np.float32)[..., None] / 255)
    canvas = Image.fromarray(stars.clip(0, 255).astype(np.uint8))
    ilc = np.array(il).astype(np.float32); bgc = np.array(canvas.crop(((BW - BH) // 2, 0, (BW - BH) // 2 + BH, BH))).astype(np.float32)
    canvas.paste(Image.fromarray(np.maximum(ilc, bgc).astype(np.uint8)), ((BW - BH) // 2, 0))
    return canvas, None

# ---------- Plate B base: steam-lid globe ----------
venus_src = Image.open("PIA23791.jpg").convert("RGB").crop((0, 0, 1040, 1096))
VBOX = (94, 79, 1031, 1016)
def disc_alpha(d):
    yy, xx = np.mgrid[0:d, 0:d]
    r = np.hypot(xx - d / 2 + 0.5, yy - d / 2 + 0.5) / (d / 2)
    return r, np.clip((1.0 - r) * d / 3.0, 0, 1)
def halo_wrap(out, d, rim, rim_w, strength=0.55):
    pad = int(d * 0.30); big = Image.new("RGBA", (d + 2 * pad,) * 2, (0, 0, 0, 0))
    halo = Image.new("L", big.size, 0); ImageDraw.Draw(halo).ellipse((pad - 2, pad - 2, pad + d + 2, pad + d + 2), fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(d * rim_w))
    col = Image.new("RGBA", big.size, rim + (0,)); col.putalpha(halo.point(lambda p: int(p * strength)))
    big.alpha_composite(col); big.alpha_composite(out, (pad, pad)); return big
def steam_lid_venus(d):
    g = venus_src.crop(VBOX).resize((d, d), Image.LANCZOS).filter(ImageFilter.GaussianBlur(d * 0.09))
    L = np.array(g.convert("L")).astype(np.float32)[..., None] / 255.0
    r, a = disc_alpha(d)
    limb = (1.0 - 0.25 * r[..., None] ** 3)
    g = (L ** 1.1) * limb * 0.80 * np.array((0.86, 0.80, 0.52), np.float32)
    rgba = np.zeros((d, d, 4), np.float32); rgba[..., :3] = g.clip(0, 1); rgba[..., 3] = a
    return halo_wrap(Image.fromarray((rgba * 255).astype(np.uint8), "RGBA"), d, (190, 182, 130), 0.07, 0.45)
D_B, CX_B, CY_B = 1500, BW // 2, BH // 2
def base_b():
    c = starfield(BW, BH, 900, 7).convert("RGBA")
    g = steam_lid_venus(D_B)
    c.alpha_composite(g, (CX_B - g.width // 2, CY_B - g.height // 2))
    m = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(m).ellipse((CX_B - D_B * 0.53, CY_B - D_B * 0.53, CX_B + D_B * 0.53, CY_B + D_B * 0.53), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(D_B * 0.03))
    return c.convert("RGB"), m

def haze_tex(seed):
    r = np.random.default_rng(seed)
    w, h = OW * 3, OH
    acc = np.zeros((h, w), np.float32)
    for cells, wt in ((6, 0.55), (14, 0.3), (34, 0.15)):
        small = r.random((cells, cells * 3)).astype(np.float32)
        acc += wt * np.array(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    return np.clip((acc - 0.35) / 0.65, 0, 1) ** 1.4
HZ1, HZ2 = haze_tex(11), haze_tex(12)
HAZE_COL = np.array((214, 204, 150), np.float32)

def view_box(cx, cy, z):
    w = BW / z; h = BH / z
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

def render(name, base, mask, segs, haze):
    total = sum(s["dur"] for s in segs)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{name}.mp4"],
                         stdin=subprocess.PIPE)
    fi = 0; sheet = []; cuts = []; t0 = 0.0
    for si, s in enumerate(segs):
        n = round(s["dur"] * FPS); cuts.append(round(t0, 2))
        for k in range(n):
            u = k / max(n - 1, 1)
            cx = s["a"][0] + (s["b"][0] - s["a"][0]) * u
            cy = s["a"][1] + (s["b"][1] - s["a"][1]) * u
            z = s["a"][2] * (s["b"][2] / s["a"][2]) ** u
            box = view_box(cx, cy, z)
            fr = base.resize((OW, OH), Image.BICUBIC, box=box)
            if haze:
                t = fi / FPS
                mk = np.array(mask.resize((OW, OH), Image.BILINEAR, box=box)).astype(np.float32)[..., None] / 255
                o1 = int(t * 22) % (OW * 2); o2 = int(OW * 2 - (t * 13) % (OW * 2))
                h = 0.6 * HZ1[:, o1:o1 + OW] + 0.4 * HZ2[:, o2:o2 + OW]
                a = (h[..., None] * 0.22) * mk
                f = np.array(fr).astype(np.float32)
                fr = Image.fromarray((f + (HAZE_COL - f) * a).clip(0, 255).astype(np.uint8))
            if k == n // 2: sheet.append(fr.copy())
            p.stdin.write(fr.tobytes()); fi += 1
        t0 += s["dur"]
    p.stdin.close(); p.wait()
    tw, th = 640, 360; cols = 3; rows = (len(sheet) + cols - 1) // cols
    sh = Image.new("RGB", (tw * cols, th * rows), (0, 0, 0))
    for i, im in enumerate(sheet):
        sh.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * th))
        ImageDraw.Draw(sh).text(((i % cols) * tw + 8, (i // cols) * th + 6), f"cut {i+1} @ {cuts[i]:.2f}s", fill=(255, 255, 0))
    sh.save(f"{name}_cuts_grid640.jpg", quality=90)
    return {"file": f"{name}.mp4", "duration_s": round(fi / FPS, 3), "frames": fi, "cuts_s": cuts}

C = BW / 2, BH / 2
# Plate A: NASA illustration. Globe is BH tall, centred. Coordinates in base pixels.
gx0 = (BW - BH) / 2
A = [
    {"dur": 4.60, "a": (C[0], C[1], 1.00), "b": (C[0], C[1], 1.05)},                       # 35: whole world
    {"dur": 4.30, "a": (gx0 + 1100, 1080, 1.70), "b": (gx0 + 1140, 1080, 1.78)},          # 35: cloud band over the sea
    {"dur": 4.32, "a": (gx0 + 800, 1440, 1.85), "b": (gx0 + 840, 1430, 1.94)},            # 35: highland coast
    {"dur": 3.96, "a": (gx0 + 1080, 1080, 1.20), "b": (gx0 + 1080, 1080, 1.25)},          # 36: wide again (shallow oceans)
    {"dur": 4.00, "a": (gx0 + 900, 650, 1.75), "b": (gx0 + 940, 660, 1.83)},              # 36: northern continent + sea
]
# Plate B: steam-lid globe (D_B=1500 at centre).
B = [
    {"dur": 4.20, "a": (C[0], C[1], 1.00), "b": (C[0], C[1], 1.05)},                       # 37
    {"dur": 3.92, "a": (C[0] - 380, C[1] - 120, 1.75), "b": (C[0] - 360, C[1] - 120, 1.83)},  # 37: lit side
    {"dur": 3.92, "a": (C[0] + 420, C[1] + 60, 1.60), "b": (C[0] + 400, C[1] + 60, 1.67)},    # 37: terminator side
    {"dur": 6.34 / 2, "a": (C[0], C[1], 1.25), "b": (C[0], C[1], 1.29)},                   # 38
    {"dur": 6.34 / 2, "a": (C[0] - 200, C[1] + 260, 1.90), "b": (C[0] - 190, C[1] + 250, 1.98)},  # 38: haze close
    {"dur": 3.82, "a": (C[0] + 120, C[1], 1.40), "b": (C[0] + 120, C[1], 1.46)},           # 39 slot
    {"dur": 3.82, "a": (C[0], C[1], 1.08), "b": (C[0], C[1], 1.00)},                       # 39 slot: slow pull back out
]
which = sys.argv[1:] or ["A", "B"]
rep = {}
if "A" in which:
    ba, _ = base_a(); ba.save("plateA_nasa_ancient_venus_base_3840.jpg", quality=92)
    rep["A"] = render("venus_ch3_plateA_ocean_nasa_v01", ba, None, A, False)
if "B" in which:
    bb, mb = base_b(); bb.save("plateB_steam_lid_base_3840.jpg", quality=92)
    rep["B"] = render("venus_ch3_plateB_steam_lid_v01", bb, mb, B, True)
json.dump(rep, open("plates_report_v01.json", "w"), indent=2); print(json.dumps(rep, indent=2))
