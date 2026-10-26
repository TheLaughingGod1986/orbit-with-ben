#!/usr/bin/env python3
"""J0954 — code-rendered Apophis for the v11 Short. £0. No matte.

A two-lobed (peanut) rock, lit side plus a soft terminator and a rim-lit
dark side. Alpha is the whole silhouette, so the dark side stays in frame.
The body sits right of centre in the 1080x1920 plate so v10's dx path
(loop start near dx=-360 at scale 1.20) still clears a 24 px margin.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1080, 1920
FPS = 24
NFRAMES = 192  # 8.0 s, covers src times through 7.60
# Half-length of the peanut in source pixels, and a constant right shift.
# Worst composite is the loop start: dx ≈ -364, scale 1.20. These two
# numbers leave about 40 px on the near edge. v10 dx / scale / timing stay.
HALF_PX = 178
SHIFT_X = 78

# Two lobes of a contact binary. Smooth-min fuses them into one peanut.
LOBE_A = np.array([-0.28, 0.015, 0.0])
LOBE_B = np.array([0.30, -0.01, 0.02])
RAD_A = np.array([0.46, 0.38, 0.36])
RAD_B = np.array([0.34, 0.29, 0.27])
SMIN_K = 0.26

KEY = np.array([-0.42, 0.48, 0.77], dtype=np.float64)
KEY /= np.linalg.norm(KEY)
RIM = np.array([0.72, -0.18, -0.55], dtype=np.float64)
RIM /= np.linalg.norm(RIM)
FILL = np.array([0.15, -0.35, 0.45], dtype=np.float64)
FILL /= np.linalg.norm(FILL)


def _rot(t: float) -> np.ndarray:
    """Object-to-camera. Slow tumble: both lobes and the dark side come around."""
    yaw = 0.46 * t
    pitch = 0.42 + 0.20 * np.sin(0.33 * t)
    roll = 0.10 * np.sin(0.21 * t + 0.6)
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    rz = np.array([[cr, -sr, 0], [sr, cr, 0], [0, 0, 1]])
    return rz @ rx @ ry


def _on_lobe(rng: np.random.Generator, centre: np.ndarray, radii: np.ndarray) -> np.ndarray:
    d = rng.normal(size=3)
    d /= np.linalg.norm(d)
    return centre + d * radii * rng.uniform(0.82, 0.98)


def _crater_sets():
    """A few shallow bowls in the silhouette, and many more that only shade."""
    rng = np.random.default_rng(340)
    spos, srad, sdep = [], [], []
    for centre, radii, n in ((LOBE_A, RAD_A, 7), (LOBE_B, RAD_B, 4)):
        for _ in range(n):
            spos.append(_on_lobe(rng, centre, radii))
            srad.append(float(rng.uniform(0.055, 0.11)))
            sdep.append(float(rng.uniform(0.0035, 0.008)))
    ppos, prad, pdep = [], [], []
    for centre, radii, n in ((LOBE_A, RAD_A, 36), (LOBE_B, RAD_B, 22)):
        for _ in range(n):
            ppos.append(_on_lobe(rng, centre, radii))
            prad.append(float(rng.uniform(0.012, 0.040)))
            pdep.append(float(rng.uniform(0.45, 0.95)))
    return (
        np.array(spos), np.array(srad), np.array(sdep),
        np.array(ppos), np.array(prad), np.array(pdep),
    )


CRATER_POS, CRATER_R, CRATER_D, PAINT_POS, PAINT_R, PAINT_D = _crater_sets()


def _rubble() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(7)
    pos, rad = [], []
    for centre, radii, n in ((LOBE_A, RAD_A, 10), (LOBE_B, RAD_B, 7)):
        for _ in range(n):
            d = rng.normal(size=3)
            d /= np.linalg.norm(d)
            pos.append(centre + d * radii * 0.96)
            rad.append(float(rng.uniform(0.055, 0.10)))
    return np.array(pos), np.array(rad)


RUBBLE_POS, RUBBLE_R = _rubble()
_NOISE = np.random.default_rng(13).uniform(-1.0, 1.0, (24, 24, 24)).astype(np.float32)


def _value_noise(p: np.ndarray) -> np.ndarray:
    q = p * 2.2
    i = np.floor(q).astype(np.int32)
    f = q - i
    f = f * f * (3.0 - 2.0 * f)
    i = i % 24
    x0, y0, z0 = i[..., 0], i[..., 1], i[..., 2]
    x1, y1, z1 = (x0 + 1) % 24, (y0 + 1) % 24, (z0 + 1) % 24
    fx, fy, fz = f[..., 0], f[..., 1], f[..., 2]

    def g(ix, iy, iz):
        return _NOISE[ix, iy, iz]

    c00 = g(x0, y0, z0) * (1 - fx) + g(x1, y0, z0) * fx
    c01 = g(x0, y0, z1) * (1 - fx) + g(x1, y0, z1) * fx
    c10 = g(x0, y1, z0) * (1 - fx) + g(x1, y1, z0) * fx
    c11 = g(x0, y1, z1) * (1 - fx) + g(x1, y1, z1) * fx
    c0 = c00 * (1 - fy) + c10 * fy
    c1 = c01 * (1 - fy) + c11 * fy
    return c0 * (1 - fz) + c1 * fz


def _smin(a: np.ndarray, b: np.ndarray, k: float) -> np.ndarray:
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1.0 - h) + a * h - k * h * (1.0 - h)


def _sd_ellipsoid(p: np.ndarray, r: np.ndarray) -> np.ndarray:
    k0 = np.sqrt(np.sum((p / r) ** 2, axis=-1) + 1e-12)
    k1 = np.sqrt(np.sum((p / (r * r)) ** 2, axis=-1) + 1e-12)
    return k0 * (k0 - 1.0) / k1


def _crater_disp(p: np.ndarray) -> np.ndarray:
    d = p[..., None, :] - CRATER_POS
    dist = np.sqrt(np.sum(d * d, axis=-1) + 1e-12)
    u = dist / CRATER_R
    bowl = np.exp(-(u ** 2) * 2.4)
    rim = np.exp(-((u - 1.0) ** 2) * 22.0) * 0.22
    return np.sum((bowl - rim) * CRATER_D, axis=-1)


def _paint_craters(p: np.ndarray):
    """Albedo darkening and a normal kick. Not in the march, so it stays cheap."""
    d = p[..., None, :] - PAINT_POS
    dist = np.sqrt(np.sum(d * d, axis=-1) + 1e-12)
    u = dist / PAINT_R
    inner = np.clip((0.72 - u) / 0.72, 0.0, 1.0) ** 1.15
    ring = np.exp(-((u - 0.78) ** 2) * 70.0)
    dark = np.clip(np.sum(inner * PAINT_D, axis=-1), 0.0, 1.8)
    bright = np.sum(ring, axis=-1) * 0.16
    kick = np.sum(d * inner[..., None], axis=-2)
    return dark, bright, kick


def sdf(p: np.ndarray) -> np.ndarray:
    """Rubble peanut. Lumps live in the surface, so the outline is anti-aliased
    rock, not a scanline saw (that saw was passing the 40 px straight-run gate
    and reading as a chopped cut-out)."""
    d = _sdf_base(p)
    rough = _value_noise(p * 5.0) * 0.008
    lump = _value_noise(p * 9.0) * 0.028
    # Short ripple so a lobe's tangent cannot sit on one scanline for 40 px.
    ripple = _value_noise(p * 28.0) * 0.009
    return d + _crater_disp(p) + rough + lump + ripple


def _px_per_unit() -> float:
    """Scale so the longest axis, at any yaw, is HALF_PX from the origin."""
    reach = max(
        float(np.linalg.norm(LOBE_A) + RAD_A.max()),
        float(np.linalg.norm(LOBE_B) + RAD_B.max()),
    )
    for c, r in zip(RUBBLE_POS, RUBBLE_R):
        reach = max(reach, float(np.linalg.norm(c) + r))
    return HALF_PX / (reach + 0.03)


PX = _px_per_unit()


def _sdf_base(p: np.ndarray) -> np.ndarray:
    d = _smin(_sd_ellipsoid(p - LOBE_A, RAD_A), _sd_ellipsoid(p - LOBE_B, RAD_B), SMIN_K)
    delta = p[..., None, :] - RUBBLE_POS
    ds = np.sqrt(np.sum(delta * delta, axis=-1) + 1e-12) - RUBBLE_R
    # Fold the rubble in one smooth-min against the nearest chunk so the
    # silhouette is a rubble pile, not one long shallow arc.
    nearest = ds.min(axis=-1)
    return _smin(d, nearest, 0.06)


def render_crop(t: float) -> tuple[np.ndarray, np.ndarray, int]:
    """Return rgb uint8, alpha uint8, and the crop origin in a centred frame.

    Raymarched peanut: fused lobes, crater bowls, a lit face, a soft terminator
    and a rim on the dark side. Alpha covers the whole body, dark side included.
    """
    cam = _rot(t)
    half = HALF_PX + 22
    n = half * 2
    cols = (np.arange(n) - half + 0.5) / PX
    rows = -((np.arange(n) - half + 0.5) / PX)
    x, y = np.meshgrid(cols, rows)
    z0 = 1.55
    origin = np.einsum("ij,hwj->hwi", cam.T, np.dstack([x, y, np.full_like(x, z0)]))
    direction = -cam.T[:, 2]
    reach = HALF_PX / PX + 0.08
    live = (x * x + y * y) < reach * reach
    dist = np.full(x.shape, max(0.0, z0 - reach - 0.05))
    for _ in range(18):
        pos = origin + direction * dist[..., None]
        step = _sdf_base(pos)
        dist = np.where(live, dist + np.clip(step, 0.0, 0.18), dist)
    for _ in range(6):
        pos = origin + direction * dist[..., None]
        step = sdf(pos)
        dist = dist + np.clip(step, -0.045, 0.05)
    pos = origin + direction * dist[..., None]
    d_hit = sdf(pos)
    hit = live & (d_hit < 0.006) & (dist < z0 + reach)

    eps = 0.004
    axes = np.eye(3) * eps
    n_obj = np.stack([sdf(pos + axes[i]) - sdf(pos - axes[i]) for i in range(3)], axis=-1)
    n_len = np.sqrt(np.sum(n_obj * n_obj, axis=-1) + 1e-12)
    n_cam = np.einsum("ij,hwj->hwi", cam, n_obj / n_len[..., None])

    disp = _crater_disp(pos)
    paint_dark, paint_bright, kick = _paint_craters(pos)
    rough = _value_noise(pos * 3.4)
    e = 0.012
    gx = _value_noise(pos + np.array([e, 0, 0])) - _value_noise(pos - np.array([e, 0, 0]))
    gy = _value_noise(pos + np.array([0, e, 0])) - _value_noise(pos - np.array([0, e, 0]))
    gz = _value_noise(pos + np.array([0, 0, e])) - _value_noise(pos - np.array([0, 0, e]))
    grad = np.stack([gx, gy, gz], axis=-1)
    n_cam = n_cam + np.einsum("ij,hwj->hwi", cam, grad * 2.2 + kick * 6.0)
    n_len = np.sqrt(np.sum(n_cam * n_cam, axis=-1) + 1e-12)
    n_cam = n_cam / n_len[..., None]
    ndot_key = np.sum(n_cam * KEY, axis=-1)
    ndot_fill = np.sum(n_cam * FILL, axis=-1)
    ndot_rim = np.sum(n_cam * RIM, axis=-1)
    wrap = np.clip(ndot_key * 0.78 + 0.06, 0.0, 1.0)
    fill = np.clip(ndot_fill, 0.0, 1.0) * 0.07
    rim = np.clip(ndot_rim, 0.0, 1.0) ** 1.7
    rim *= np.clip(0.28 - ndot_key, 0.0, 1.0) * 3.2
    shade = wrap + fill
    albedo = np.array([0.66, 0.63, 0.58])
    crater_dark = np.clip(disp / 0.012, 0.0, 1.0)
    mottled = albedo * (0.82 + 0.28 * np.clip(rough, -1.0, 1.0))[..., None]
    mottled = mottled * np.clip(1.0 - crater_dark * 0.55 - paint_dark * 0.42, 0.18, 1.15)[..., None]
    mottled = mottled * (1.0 + paint_bright)[..., None]
    rgb = mottled * (0.11 + 0.89 * shade)[..., None]
    rgb = rgb + np.array([0.58, 0.66, 0.78]) * rim[..., None]
    rgb = np.clip(rgb, 0.0, 1.0)
    alpha = np.clip(1.0 - np.maximum(d_hit, 0.0) / 0.007, 0.0, 1.0) * hit
    alpha[:6, :] = 0
    alpha[-6:, :] = 0
    alpha[:, :6] = 0
    alpha[:, -6:] = 0
    return (rgb * 255.0).astype(np.uint8), (np.clip(alpha, 0, 1) * 255.0).astype(np.uint8), -half


def paste_full(rgb: np.ndarray, alpha: np.ndarray, origin: int) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crop = Image.fromarray(np.dstack([rgb, alpha]), "RGBA")
    xy = (W // 2 + SHIFT_X + origin, H // 2 + origin)
    im.paste(crop, xy, crop)
    return im


def render_frames(out_dir: Path, limit: int | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = NFRAMES if limit is None else limit
    paths = []
    for i in range(n):
        dest = out_dir / f"{i:04d}.png"
        if not dest.exists():
            rgb, alpha, origin = render_crop(i / FPS)
            paste_full(rgb, alpha, origin).save(dest)
        paths.append(dest)
        if i % 12 == 0:
            print(f"  rock frame {i + 1}/{n}", flush=True)
    if limit is None:
        (out_dir / ".done").write_text(f"n={n} half={HALF_PX} shift={SHIFT_X} px={PX:.3f}\n")
    return paths


class CodeRock:
    """Pre-rendered RGBA rock. Same layer() placement as v10's Rock24."""

    def __init__(self, paths: list[Path]):
        self.paths = paths
        self.raw_cache: dict[int, tuple[Image.Image, Image.Image]] = {}

    def _raw_pair(self, i: int) -> tuple[Image.Image, Image.Image]:
        i = min(max(int(i), 0), len(self.paths) - 1)
        if i in self.raw_cache:
            return self.raw_cache[i]
        im = Image.open(self.paths[i]).convert("RGBA")
        pair = (im.convert("RGB"), im.getchannel("A"))
        self.raw_cache[i] = pair
        return pair

    def layer(self, src_t: float, scale: float, dx: int, dy: int):
        x = min(max(src_t * FPS, 0.0), len(self.paths) - 1)
        i0 = int(np.floor(x))
        i1 = min(len(self.paths) - 1, i0 + 1)
        frac = float(x - i0) if i1 != i0 else 0.0
        rgb0, a0 = self._raw_pair(i0)
        if frac < 0.02:
            im_rgb, im_a = rgb0, a0
        else:
            rgb1, a1 = self._raw_pair(i1)
            im_rgb = Image.blend(rgb0, rgb1, frac)
            im_a = Image.blend(a0, a1, frac)
        src_area = int((np.asarray(im_a) > 115).sum())
        if scale != 1.0:
            sz = (round(W * scale), round(H * scale))
            im_rgb = im_rgb.resize(sz, Image.BILINEAR)
            im_a = im_a.resize(sz, Image.BILINEAR)
        c_rgb = Image.new("RGB", (W, H), (0, 0, 0))
        c_a = Image.new("L", (W, H), 0)
        xy = ((W - im_rgb.width) // 2 + dx, (H - im_rgb.height) // 2 + dy)
        c_rgb.paste(im_rgb, xy)
        c_a.paste(im_a, xy)
        alpha = np.asarray(c_a).astype(np.float32) / 255.0
        return np.asarray(c_rgb).astype(np.float32), alpha, src_area


def main() -> None:
    here = Path(__file__).resolve().parent
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "04_Generated-Clips/code_rock_v11"
    limit = None
    if "--preview" in sys.argv:
        limit = 6
    render_frames(out, limit=limit)
    print("px_per_unit", round(PX, 3), "half", HALF_PX, "shift", SHIFT_X, "dir", out)


if __name__ == "__main__":
    main()
