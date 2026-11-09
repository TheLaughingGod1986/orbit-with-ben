#!/usr/bin/env python3
"""J0954 c60 — code-rendered Apophis for the v13 Short. £0. No matte.

v12's solid alpha stays: a smooth SDF silhouette, alpha 1 inside, a 1.5 px
edge, craters and lumps in the shading only. The size and the lobes go back
to v11 (commit 75f0af664). v12 had pulled both in so a smooth outline could
pass the 40 px straight-run gate, and the rock became a pebble with no waist.
That gate is gone. The straight cap of a large smooth body is not a cut-out.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920
FPS = 24
NFRAMES = 192  # 8.0 s, covers src times through 7.60
# Half-length of the peanut in source pixels, and a constant right shift.
# These are the v11 values (75f0af664). Worst composite is the loop start:
# dx ≈ -364 at the open's scale. Margin stays above 24 px there. The 40 px
# straight-run limit is not a size constraint any more.
HALF_PX = 178
SHIFT_X = 78
AA_PX = 1.5

# v11 lobe radii. The v11 centres (-0.28 and +0.30) with SMIN_K 0.26 overlap
# into one convex egg once the silhouette is a smooth SDF: area/hull stays
# about 0.99, which is the v12 failure. The centres sit 20% further apart and
# the blend is 0.14, so a side view has a real waist (area/hull about 0.95)
# while the outline stays smooth (perim/hull about 1.07, under the 1.15 gate).
LOBE_A = np.array([-0.336, 0.015, 0.0])
LOBE_B = np.array([0.360, -0.01, 0.02])
RAD_A = np.array([0.46, 0.38, 0.36])
RAD_B = np.array([0.34, 0.29, 0.27])
SMIN_K = 0.14

# Key is off-axis so a terminator crosses the lit face. Rim lights the dark side.
KEY = np.array([-0.62, 0.38, 0.48], dtype=np.float64)
KEY /= np.linalg.norm(KEY)
RIM = np.array([0.78, -0.22, -0.48], dtype=np.float64)
RIM /= np.linalg.norm(RIM)
FILL = np.array([0.20, -0.55, 0.28], dtype=np.float64)
FILL /= np.linalg.norm(FILL)


def _rot(t: float) -> np.ndarray:
    """Object-to-camera. A slow yaw, held near broadside.

    v11's yaw (0.46*t) turned the peanut end-on, and from that angle the
    silhouette is one oval: area/hull sits near 1.0 for about half the frames.
    c60 needs a visible waist on at least 80% of source frames, so the yaw
    rocks about ±30° instead of winding through the end-on view. Pitch still
    brings the dark side around.
    """
    yaw = 0.55 * np.sin(0.45 * t)
    pitch = 0.42 + 0.25 * np.sin(0.33 * t)
    roll = 0.12 * np.sin(0.22 * t + 0.4)
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
    return centre + d * radii * rng.uniform(0.55, 0.92)


def _paint_sets():
    """Shading-only craters. They never enter the silhouette SDF."""
    rng = np.random.default_rng(340)
    ppos, prad, pdep = [], [], []
    for centre, radii, n in ((LOBE_A, RAD_A, 48), (LOBE_B, RAD_B, 28)):
        for _ in range(n):
            ppos.append(_on_lobe(rng, centre, radii))
            prad.append(float(rng.uniform(0.018, 0.055)))
            pdep.append(float(rng.uniform(0.55, 1.0)))
    return np.array(ppos), np.array(prad), np.array(pdep)


PAINT_POS, PAINT_R, PAINT_D = _paint_sets()
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


def _sdf_body(p: np.ndarray) -> np.ndarray:
    """Smooth peanut. No rubble, no craters, no ripple. This is the silhouette."""
    return _smin(_sd_ellipsoid(p - LOBE_A, RAD_A), _sd_ellipsoid(p - LOBE_B, RAD_B), SMIN_K)


def _px_per_unit() -> float:
    """Scale so the longest axis, at any yaw, is HALF_PX from the origin."""
    reach = max(
        float(np.linalg.norm(LOBE_A) + RAD_A.max()),
        float(np.linalg.norm(LOBE_B) + RAD_B.max()),
    )
    return HALF_PX / (reach + 0.03)


PX = _px_per_unit()


def _paint_craters(p: np.ndarray):
    """Albedo darkening and a normal kick. Not in the march."""
    d = p[..., None, :] - PAINT_POS
    dist = np.sqrt(np.sum(d * d, axis=-1) + 1e-12)
    u = dist / PAINT_R
    inner = np.clip((0.85 - u) / 0.85, 0.0, 1.0) ** 1.2
    ring = np.exp(-((u - 0.82) ** 2) * 80.0)
    dark = np.clip(np.sum(inner * PAINT_D, axis=-1), 0.0, 1.6)
    bright = np.sum(ring, axis=-1) * 0.22
    kick = np.sum(d * inner[..., None], axis=-2)
    return dark, bright, kick


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def render_crop(t: float) -> tuple[np.ndarray, np.ndarray, int]:
    """Return rgb uint8, alpha uint8, and the crop origin in a centred frame.

    The ray marches the smooth peanut only. Inside the body alpha is 1.0.
    The edge is a 1.5 px band. Craters and lumps are shading.
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
    reach = HALF_PX / PX + 0.06
    live = (x * x + y * y) < reach * reach
    dist = np.full(x.shape, max(0.0, z0 - reach - 0.02))
    # Every silhouette pixel is a ray that meets the front surface, so the
    # surface distance there is ~0. Coverage comes from the closest approach:
    # a ray that enters the body is fully opaque, and only the outer 1.5 px
    # grades off. Steps stay short so a graze cannot tunnel through.
    # The neck is thin. A 0.05 step tunnels through it and splits the peanut
    # into two lobes with a gap. Shorter steps keep the bridge solid.
    min_sdf = np.full(x.shape, 1e9)
    for _ in range(48):
        pos = origin + direction * dist[..., None]
        step = _sdf_body(pos)
        min_sdf = np.minimum(min_sdf, step)
        dist = np.where(live, dist + np.clip(step, 0.0, 0.02) * 0.85, dist)
    for _ in range(16):
        pos = origin + direction * dist[..., None]
        step = _sdf_body(pos)
        min_sdf = np.minimum(min_sdf, step)
        dist = np.where(live & (step > 0), dist + np.clip(step, 0.0, 0.002) * 0.95, dist)
    pos = origin + direction * dist[..., None]
    # Shade the front surface. A ray that stopped just outside still has a normal.
    eps_hit = 0.40 / PX
    aa = AA_PX / PX
    alpha = np.where(
        min_sdf <= eps_hit,
        1.0,
        np.clip(1.0 - (min_sdf - eps_hit) / aa, 0.0, 1.0),
    )
    alpha = np.where(live, alpha, 0.0)

    eps = 0.0035
    axes = np.eye(3) * eps
    n_obj = np.stack([_sdf_body(pos + axes[i]) - _sdf_body(pos - axes[i]) for i in range(3)], axis=-1)
    n_len = np.sqrt(np.sum(n_obj * n_obj, axis=-1) + 1e-12)
    n_cam = np.einsum("ij,hwj->hwi", cam, n_obj / n_len[..., None])

    paint_dark, paint_bright, kick = _paint_craters(pos)
    e = 0.018
    gx = _value_noise(pos + np.array([e, 0, 0])) - _value_noise(pos - np.array([e, 0, 0]))
    gy = _value_noise(pos + np.array([0, e, 0])) - _value_noise(pos - np.array([0, e, 0]))
    gz = _value_noise(pos + np.array([0, 0, e])) - _value_noise(pos - np.array([0, 0, e]))
    grad = np.stack([gx, gy, gz], axis=-1)
    # Shading only. The kick is capped so a crater cannot flip the normal.
    bump = np.einsum("ij,hwj->hwi", cam, grad * 1.4 + kick * 3.5)
    bump_len = np.sqrt(np.sum(bump * bump, axis=-1) + 1e-12)
    bump = bump * np.minimum(1.0, 0.55 / bump_len)[..., None]
    n_cam = n_cam + bump
    n_len = np.sqrt(np.sum(n_cam * n_cam, axis=-1) + 1e-12)
    n_cam = n_cam / n_len[..., None]

    ndot_key = np.sum(n_cam * KEY, axis=-1)
    ndot_fill = np.sum(n_cam * FILL, axis=-1)
    ndot_rim = np.sum(n_cam * RIM, axis=-1)
    term = _smoothstep(-0.08, 0.55, ndot_key)
    fill = np.clip(ndot_fill, 0.0, 1.0) * 0.10
    rim = np.clip(ndot_rim, 0.0, 1.0) ** 1.35
    rim *= np.clip(0.22 - ndot_key, 0.0, 1.0) * 3.6
    shade = 0.07 + 0.93 * term + fill
    rough = _value_noise(pos * 3.2)
    albedo = np.array([0.72, 0.67, 0.60])
    mottled = albedo * (0.78 + 0.32 * np.clip(rough, -1.0, 1.0))[..., None]
    mottled = mottled * np.clip(1.0 - paint_dark * 0.62, 0.22, 1.2)[..., None]
    mottled = mottled * (1.0 + paint_bright)[..., None]
    rgb = mottled * shade[..., None]
    rgb = rgb + np.array([0.55, 0.64, 0.82]) * (rim * 0.85)[..., None]
    rgb = np.clip(rgb, 0.0, 1.0)
    # Colour only where the body is. A miss stays transparent, never a grey disc.
    rgb = np.where(alpha[..., None] > 0, rgb, 0.0)
    alpha[:4, :] = 0
    alpha[-4:, :] = 0
    alpha[:, :4] = 0
    alpha[:, -4:] = 0
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
        (out_dir / ".done").write_text(
            f"n={n} half={HALF_PX} shift={SHIFT_X} px={PX:.3f} aa={AA_PX} solid=1\n"
        )
    return paths


def hole_fraction(alpha: np.ndarray, close_px: int = 7) -> float:
    """Share of the filled silhouette whose alpha is under 0.5.

    A morphological close bridges see-through gaps. The anti-aliased rim sits
    outside the 0.5 contour, so a solid body with a smooth edge scores ~0.
    """
    a = alpha if alpha.dtype != np.uint8 and alpha.max() <= 1.0 else alpha.astype(np.float32) / 255.0
    if a.ndim == 3:
        a = a[..., 3] if a.shape[-1] == 4 else a.mean(-1)
    solid = a >= 0.5
    if int(solid.sum()) < 80:
        return 1.0
    im = Image.fromarray(np.where(solid, np.uint8(255), np.uint8(0)))
    k = close_px if close_px % 2 == 1 else close_px + 1
    closed = np.asarray(im.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))) > 127
    holes = closed & (a < 0.5)
    return float(holes.sum()) / float(max(1, int(closed.sum())))


def _grid_perim(mask: np.ndarray) -> float:
    # int16: uint8 diff wraps 0-1 into 255 and inflates the length ~255×.
    m = mask.astype(np.int16)
    return float(np.abs(np.diff(m, axis=0)).sum() + np.abs(np.diff(m, axis=1)).sum())


def _hull_perim(mask: np.ndarray) -> float:
    """Andrew's monotone chain. Returns 0 when the mask is too small."""
    ys, xs = np.where(mask)
    if xs.size < 3:
        return 0.0
    step = max(1, xs.size // 4000)
    pts = np.unique(np.stack([xs[::step], ys[::step]], axis=1), axis=0)
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in pts[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = np.array(lower[:-1] + upper[:-1], dtype=np.float64)
    if len(hull) < 3:
        return 0.0
    d = np.diff(np.vstack([hull, hull[:1]]), axis=0)
    return float(np.sqrt((d * d).sum(axis=1)).sum())


def _hull_mask(solid: np.ndarray) -> np.ndarray:
    """Raster of the convex hull, so its perimeter uses the same grid measure."""
    from PIL import ImageDraw
    ys, xs = np.where(solid)
    if xs.size < 3:
        return solid
    step = max(1, int(xs.size // 2500))
    pts = np.stack([xs[::step], ys[::step]], axis=1)
    pts = np.unique(pts, axis=0)
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list = []
    for p in pts:
        p = (int(p[0]), int(p[1]))
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in pts[::-1]:
        p = (int(p[0]), int(p[1]))
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    im = Image.new("L", (solid.shape[1], solid.shape[0]), 0)
    if len(hull) >= 3:
        ImageDraw.Draw(im).polygon(hull, fill=1)
    return np.asarray(im) > 0


def area_over_hull(alpha: np.ndarray) -> float:
    """Solid area divided by the convex-hull area. A peanut waist sits under 0.97."""
    a = alpha if alpha.max() <= 1.0 else alpha.astype(np.float32) / 255.0
    if a.ndim == 3:
        a = a[..., 3] if a.shape[-1] == 4 else a.mean(-1)
    solid = a >= 0.5
    hull = _hull_mask(solid)
    hs = int(hull.sum())
    if hs < 80:
        return 1.0
    return float(int(solid.sum())) / float(hs)


def serration_ratio(alpha: np.ndarray) -> tuple[float, float]:
    """(perimeter / smoothed perimeter, perimeter / convex-hull perimeter).

    Both references use the same grid-edge length. A smooth outline sits near
    1.0 against a 2 px blur. The hull ratio is higher on a peanut waist; the
    sawtooth on v11 is several times either reference.
    """
    a = alpha if alpha.max() <= 1.0 else alpha.astype(np.float32) / 255.0
    if a.ndim == 3:
        a = a[..., 3] if a.shape[-1] == 4 else a.mean(-1)
    solid = a >= 0.5
    per = _grid_perim(solid)
    im = Image.fromarray(np.where(solid, np.uint8(255), np.uint8(0)))
    smooth = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=2))) >= 128
    sm = _grid_perim(smooth)
    hull = _grid_perim(_hull_mask(solid))
    return (per / sm if sm else 99.0), (per / hull if hull else 99.0)


def frame_stats(path: Path) -> dict:
    im = np.asarray(Image.open(path).convert("RGBA"))
    a = im[..., 3].astype(np.float32) / 255.0
    holes = hole_fraction(a)
    smooth_r, hull_r = serration_ratio(a)
    return {
        "holes": round(holes, 5),
        "perim_over_smooth": round(smooth_r, 4),
        "perim_over_hull": round(hull_r, 4),
        "area_over_hull": round(area_over_hull(a), 4),
        "solid_px": int((a >= 0.5).sum()),
    }


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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else here / "04_Generated-Clips/code_rock_v13"
    limit = None
    if "--preview" in sys.argv:
        limit = 2
    if "--stats" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--stats") + 1])
        paths = sorted(target.glob("[0-9][0-9][0-9][0-9].png"))
        step = max(1, len(paths) // 32)
        worst_h, worst_s = 0.0, 0.0
        for p in paths[::step]:
            st = frame_stats(p)
            worst_h = max(worst_h, st["holes"])
            worst_s = max(worst_s, st["perim_over_smooth"])
            print(p.name, st, flush=True)
        print(f"worst holes {worst_h:.5f} worst serration {worst_s:.4f}")
        return
    render_frames(out, limit=limit)
    print("px_per_unit", round(PX, 3), "half", HALF_PX, "shift", SHIFT_X, "aa_px", AA_PX, "dir", out)
    if limit:
        for p in sorted(out.glob("[0-9][0-9][0-9][0-9].png"))[:limit]:
            print(p.name, frame_stats(p), flush=True)


if __name__ == "__main__":
    main()
