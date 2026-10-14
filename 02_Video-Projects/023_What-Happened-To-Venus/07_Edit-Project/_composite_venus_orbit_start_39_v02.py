"""Venus 023 #39 orbit_between_two_venus start frame v02 (Claude 5984886311).

Recomposited from canonical ORBIT_REF (orbit-seedance-reference-16x9-v01.png): Orbit is cut
(u2net matte + hand masks for antenna bulb/stalk and underside glow ring), only scaled.
Backgrounds: NASA/JPL Mariner 10 Venus PIA23791 globe, graded, over a procedural starfield.
v02 changes vs v01 (the right world drifted to Jupiter):
  - LEFT  (the "may have had oceans" Venus): cloud-white, a few soft cloud gaps showing dark blue sea.
  - RIGHT (the steam-lid Venus): dim sulphur-yellow/grey haze, flat featureless globe (texture blurred out).
  - Neither world gets an orange grade, bands or swirls.
Run on the Grok box with orbit_ref.png and PIA23791.jpg in cwd; needs numpy, pillow, rembg.
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
    d.ellipse((297, 111, 332, 146), fill=255)
    d.line([(312, 143), (310, 158), (308, 172), (306, 188), (305, 206)], fill=255, width=8)
    d.ellipse((262, 546, 390, 584), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.maximum(a, np.array(m).astype(np.float32))
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
    return Image.fromarray(bg.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))

venus_src = Image.open("PIA23791.jpg").convert("RGB").crop((0, 0, 1040, 1096))
BOX = (94, 79, 1031, 1016)

def disc_alpha(diam):
    yy, xx = np.mgrid[0:diam, 0:diam]
    r = np.hypot(xx - diam / 2 + 0.5, yy - diam / 2 + 0.5) / (diam / 2)
    return r, np.clip((1.0 - r) * diam / 3.0, 0, 1)

def halo_wrap(out, diam, rim, rim_w, strength=0.55):
    pad = int(diam * 0.30); big = Image.new("RGBA", (diam + 2 * pad,) * 2, (0, 0, 0, 0))
    halo = Image.new("L", big.size, 0); ImageDraw.Draw(halo).ellipse((pad - 2, pad - 2, pad + diam + 2, pad + diam + 2), fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(diam * rim_w))
    col = Image.new("RGBA", big.size, rim + (0,)); col.putalpha(halo.point(lambda p: int(p * strength)))
    big.alpha_composite(col); big.alpha_composite(out, (pad, pad)); return big

def ocean_venus(diam):
    g = venus_src.crop(BOX).resize((diam, diam), Image.LANCZOS).filter(ImageFilter.GaussianBlur(diam * 0.012))
    g = np.array(g).astype(np.float32) / 255.0
    L = g.mean(axis=2, keepdims=True)
    g = 0.15 * g + 0.85 * L                       # near-neutral cloud white
    g = (g ** 0.9) * 1.08 * np.array((1.00, 0.985, 0.95), np.float32)
    # a few soft, irregular cloud gaps showing dark blue sea (stretched along the cloud flow)
    nr = np.random.default_rng(7)
    small = nr.random((9, 5)).astype(np.float32)                      # coarse noise, wide in x
    n1 = np.array(Image.fromarray((small * 255).astype(np.uint8)).resize((diam, diam), Image.BICUBIC)).astype(np.float32) / 255
    fine = nr.random((40, 22)).astype(np.float32)
    n2 = np.array(Image.fromarray((fine * 255).astype(np.uint8)).resize((diam, diam), Image.BICUBIC)).astype(np.float32) / 255
    n = 0.7 * n1 + 0.3 * n2
    r0, _ = disc_alpha(diam)
    yy, xx = np.mgrid[0:diam, 0:diam] / diam
    lit = np.clip((0.70 - xx) / 0.25, 0, 1) * np.clip((0.86 - r0) / 0.15, 0, 1)   # keep off terminator and limb
    m = np.clip((n - 0.66) / 0.10, 0, 1) * lit
    ga = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(diam * 0.008))).astype(np.float32)[..., None] / 255.0 * 0.75
    sea = np.array((0.07, 0.16, 0.30), np.float32)
    g = g * (1 - ga) + sea * ga * (0.6 + 0.4 * L)
    r, a = disc_alpha(diam)
    rgba = np.zeros((diam, diam, 4), np.float32); rgba[..., :3] = g.clip(0, 1); rgba[..., 3] = a
    return halo_wrap(Image.fromarray((rgba * 255).astype(np.uint8), "RGBA"), diam, (235, 235, 245), 0.05)

def steam_lid_venus(diam):
    # keep only the Mariner 10 lighting (terminator / limb), blur all cloud texture away
    g = venus_src.crop(BOX).resize((diam, diam), Image.LANCZOS).filter(ImageFilter.GaussianBlur(diam * 0.09))
    L = np.array(g.convert("L")).astype(np.float32)[..., None] / 255.0
    r, a = disc_alpha(diam)
    limb = (1.0 - 0.25 * r[..., None] ** 3)
    g = (L ** 1.1) * limb * 0.80 * np.array((0.86, 0.80, 0.52), np.float32)   # dim sulphur-yellow/grey
    rgba = np.zeros((diam, diam, 4), np.float32); rgba[..., :3] = g.clip(0, 1); rgba[..., 3] = a
    return halo_wrap(Image.fromarray((rgba * 255).astype(np.uint8), "RGBA"), diam, (190, 182, 130), 0.07, 0.45)

def put(canvas, layer, cx, cy):
    canvas.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def underside_glow(canvas, cx, cy, rx, ry, col=(255, 190, 110), k=0.55):
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(ry * 0.9))
    c = np.array(canvas).astype(np.float32); a = np.array(g).astype(np.float32)[..., None] / 255 * k
    c[..., :3] = c[..., :3] + a * np.array(col, np.float32) * (1 - c[..., :3] / 255 * 0.6)
    return Image.fromarray(c.clip(0, 255).astype(np.uint8), "RGBA")

orb = orbit_rgba()
c = starfield().convert("RGBA")
put(c, ocean_venus(400), 215, 360); put(c, steam_lid_venus(400), 1065, 360)
o = orb.resize((round(orb.width * 178 / orb.height), 178), Image.LANCZOS); ox, oy = 640, 350
c = underside_glow(c, ox, oy + o.height // 2 - 6, 48, 18)
put(c, o, ox, oy)
c.convert("RGB").save("out_v02/orbit_between_two_venus_start_v02.png")
print("ok")
