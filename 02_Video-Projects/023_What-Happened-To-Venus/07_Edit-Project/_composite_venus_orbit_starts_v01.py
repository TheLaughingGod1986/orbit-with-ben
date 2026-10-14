"""Recomposite Venus 023 Orbit start frames (#39, #46) from canonical ORBIT_REF.

Orbit is cut from orbit-seedance-reference-16x9-v01.png (u2net matte + hand masks for
antenna bulb/stalk and underside glow ring). Not redrawn, not mirrored.
Backgrounds: NASA/JPL Mariner 10 Venus PIA23791 (left panel), colour-graded; procedural starfield.
Run (4 Oct 2026) on the Grok box with inputs copied into cwd: orbit_ref.png = ORBIT_REF,
PIA23791.jpg from 07_Edit-Project/nasa_pool_v01/open/. Outputs to out/. Needs numpy, pillow, rembg.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove, new_session

W, H = 1280, 720
ref = Image.open("orbit_ref.png").convert("RGB")
rng = np.random.default_rng(23)

def orbit_rgba():
    a = np.array(remove(ref, session=new_session("u2net")).split()[3]).astype(np.float32)
    m = Image.new("L", ref.size, 0); d = ImageDraw.Draw(m)
    d.ellipse((297, 111, 332, 146), fill=255)                      # antenna bulb
    d.line([(312, 143), (310, 158), (308, 172), (306, 188), (305, 206)], fill=255, width=8)  # stalk
    d.ellipse((262, 546, 390, 584), fill=255)                      # underside glow ring
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.maximum(a, np.array(m).astype(np.float32))
    # choke matte slightly to drop Jupiter fringe
    al = Image.fromarray(alpha.clip(0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    o = ref.convert("RGBA"); o.putalpha(al)
    return o.crop(o.getbbox())

def starfield():
    bg = np.zeros((H, W, 3), np.float32); bg[:] = (4, 4, 9)
    n = 260
    ys, xs = rng.integers(0, H, n), rng.integers(0, W, n)
    br = rng.random(n) ** 3 * 170 + 20
    for y, x, b in zip(ys, xs, br):
        bg[y, x] += (b, b, b * 1.05)
    img = Image.fromarray(bg.clip(0, 255).astype(np.uint8))
    return img.filter(ImageFilter.GaussianBlur(0.5))

venus_src = Image.open("PIA23791.jpg").convert("RGB").crop((0, 0, 1040, 1096))  # Mariner 10 cloud-white globe (left panel)

def venus_disc(diam, tint, gain=1.0, gamma=1.0, rim=None, rim_w=0.06):
    # crop to the globe and resample
    box = (94, 79, 1031, 1016)  # true disc: lit limb x=94, poles y=79..1016 (night side to the right)
    g = venus_src.crop(box).resize((diam, diam), Image.LANCZOS)
    g = np.array(g).astype(np.float32) / 255.0
    L = g.mean(axis=2, keepdims=True)
    g = 0.35 * g + 0.65 * L               # desaturate then re-tint
    g = (g ** gamma) * gain * np.array(tint, np.float32)
    rgba = np.zeros((diam, diam, 4), np.float32); rgba[..., :3] = g.clip(0, 1)
    yy, xx = np.mgrid[0:diam, 0:diam]; r = np.hypot(xx - diam / 2 + 0.5, yy - diam / 2 + 0.5) / (diam / 2)
    rgba[..., 3] = np.clip((1.0 - r) * diam / 3.0, 0, 1)
    out = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    if rim:  # soft atmospheric haze halo
        pad = int(diam * 0.30); big = Image.new("RGBA", (diam + 2 * pad,) * 2, (0, 0, 0, 0))
        halo = Image.new("L", big.size, 0); ImageDraw.Draw(halo).ellipse((pad - 2, pad - 2, pad + diam + 2, pad + diam + 2), fill=255)
        halo = halo.filter(ImageFilter.GaussianBlur(diam * rim_w))
        col = Image.new("RGBA", big.size, rim + (0,)); col.putalpha(halo.point(lambda p: int(p * 0.55)))
        big.alpha_composite(col); big.alpha_composite(out, (pad, pad)); return big, pad
    return out, 0

def put(canvas, layer, cx, cy):
    canvas.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def underside_glow(canvas, cx, cy, rx, ry, col=(255, 190, 110), k=0.55):
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(ry * 0.9))
    c = np.array(canvas).astype(np.float32); a = np.array(g).astype(np.float32)[..., None] / 255 * k
    c[..., :3] = c[..., :3] + a * np.array(col, np.float32) * (1 - c[..., :3] / 255 * 0.6)
    return Image.fromarray(c.clip(0, 255).astype(np.uint8), "RGBA")

orb = orbit_rgba()
print("orbit cut", orb.size)

def placed_orbit(height):
    s = height / orb.height
    return orb.resize((round(orb.width * s), height), Image.LANCZOS)

# ---- #39 orbit_between_two_venus: two Venus worlds flank a small Orbit ----
c = starfield().convert("RGBA")
left, _ = venus_disc(400, (1.00, 0.97, 0.90), gain=1.08, gamma=0.9, rim=(235, 235, 245), rim_w=0.05)      # milder, cloud-bright
right, _ = venus_disc(400, (1.00, 0.66, 0.36), gain=0.95, gamma=1.15, rim=(255, 140, 60), rim_w=0.08)     # hotter, steam-lidded
put(c, left, 215, 360); put(c, right, 1065, 360)
o = placed_orbit(178); ox, oy = 640, 350
c = underside_glow(c, ox, oy + o.height // 2 - 6, 48, 18)
put(c, o, ox, oy)
c.convert("RGB").save("out/orbit_between_two_venus_start.png")

# ---- #46 orbit_looks_back_earth: Venus behind, Earth a bright blue POINT ----
c = starfield().convert("RGBA")
ven, _ = venus_disc(760, (1.00, 0.97, 0.91), gain=1.05, gamma=0.95, rim=(235, 232, 240), rim_w=0.04)
put(c, ven, 150, 470)          # big cloud-white Venus filling behind, lower-left, partly off-frame
# Earth: tiny blue point of light upper right (core ~2px + small halo); no disc, no edge
e = np.array(c).astype(np.float32); ex, ey = 1020, 210
yy, xx = np.mgrid[0:H, 0:W]; r = np.hypot(xx - ex, yy - ey)
core = np.clip(1.0 - r / 2.8, 0, 1)[..., None]
halo = np.exp(-(r / 8.0) ** 2)[..., None] * 0.85
e[..., :3] += core * np.array([235, 245, 255]) + halo * np.array([70, 150, 255])
c = Image.fromarray(e.clip(0, 255).astype(np.uint8), "RGBA")
o = placed_orbit(160); ox, oy = 690, 390
c = underside_glow(c, ox, oy + o.height // 2 - 6, 44, 16)
put(c, o, ox, oy)
c.convert("RGB").save("out/orbit_looks_back_earth_start.png")
print("ok")
