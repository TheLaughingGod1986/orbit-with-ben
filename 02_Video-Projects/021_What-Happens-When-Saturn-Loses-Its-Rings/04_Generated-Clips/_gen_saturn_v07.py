#!/usr/bin/env python3
"""Saturn v07 assets — Ben 1 Oct 12:27 London.

OPENING v07: dense bright grain STREAM + motion blur; curves into equator;
  fades at cloud tops; ~10% push-in (phone-readable).
ICE CROWD v07: parallax layers cut from ice still's OWN white rocks + slow rotation.
MONDAY v04: surgical edit of v01 only — keep curtains; erase below lower limb;
  soft-fade at cloud tops. No regenerate.
SMALL ORBIT: cut Orbit from saturn_bare_orbit_v06 (from-behind) onto bare v05 + slight drift.
TUMBLE: copy 0–3s fallback (no Omni wait; one Vertex retry only if working before Tue).

UAT: OWB UAT/saturn_v07_for_ben_ok/ + 4-frame contacts + §6 notes.
No media in git — sha256 in MANIFEST.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
CLIPS = EP / "04_Generated-Clips"
OUT = CLIPS / "v07"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_v07_for_ben_ok"
)
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/assets"
)

V04_OPEN = CLIPS / "veo_approved_v04" / "veo_open_rings_v04.mp4"
OPEN_STILL = CLIPS / "stills_v06" / "saturn_open_rings_v06.png"
ICE_STILL = CLIPS / "stills_v05" / "saturn_ice_chunks_v05.png"
MON_V01 = CLIPS / "shorts_stills_v01" / "monday_saturn_rings_streaming_v01.png"
BARE_V05 = CLIPS / "veo_v05" / "veo_bare_saturn_v05.mp4"
BARE_ORBIT_STILL = CLIPS / "stills_v06" / "saturn_bare_orbit_v06.png"
TUMBLE_FALLBACK = CLIPS / "veo_v05" / "veo_orbit_tumble_v03_fallback_0-3s.mp4"

W, H = 1920, 1080
FPS = 24
DUR = 8.0
NFRAMES = int(DUR * FPS)
V04_HOLD = 2.5
XFADE = 0.45


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def chunk_write(src: Path | bytes, dest: Path, retries: int = 14) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 256 * 1024):
                    o.write(data[i : i + 256 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.25)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    Path("/tmp").joinpath(f"uat_stage_{dest.name}").write_bytes(data)
    print(f"  STAGED /tmp/uat_stage_{dest.name}", flush=True)


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd[:10]), "...", flush=True)
    subprocess.check_call(cmd)


def contact_sheet(mp4: Path, dest: Path) -> list[float]:
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(mp4)]
    )
    dur = float(json.loads(probe)["format"]["duration"])
    times = [0.05, dur / 3, 2 * dur / 3, max(0.05, dur - 0.08)]
    work = OUT / "_work"
    work.mkdir(parents=True, exist_ok=True)
    frames = []
    for i, t in enumerate(times):
        p = work / f"_cs_{mp4.stem}_{i}.png"
        run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.3f}",
                "-i",
                str(mp4),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(p),
            ]
        )
        frames.append(Image.open(p).convert("RGB"))
    fw, fh = frames[0].size
    tw, th = fw // 2, fh // 2
    sheet = Image.new("RGB", (tw * 2 + 6, th * 2 + 6), (12, 12, 14))
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(frames):
        im = im.resize((tw, th), Image.Resampling.LANCZOS)
        x = (i % 2) * (tw + 6)
        y = (i // 2) * (th + 6)
        sheet.paste(im, (x, y))
        draw.text((x + 8, y + 8), f"t={times[i]:.2f}s", fill=(255, 220, 80))
    sheet.save(dest)
    return times


def resize_cover(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return im.crop((left, top, left + w, top + h))


def ken_burns(still: Image.Image, t: float, dur: float, zoom_end: float = 1.10) -> Image.Image:
    """~10% push toward Saturn (right-center)."""
    base = resize_cover(still, W, H)
    z = 1.0 + (zoom_end - 1.0) * (t / max(dur, 1e-6))
    cw, ch = int(W / z), int(H / z)
    cx = int(W * 0.64)
    cy = H // 2
    left = max(0, min(W - cw, cx - cw // 2))
    top = max(0, min(H - ch, cy - ch // 2))
    return base.crop((left, top, left + cw, top + ch)).resize((W, H), Image.Resampling.LANCZOS)


def open_geometry() -> dict:
    return {
        "planet_cx": int(W * 0.93),
        "planet_cy": int(H * 0.50),
        "planet_r": int(H * 0.52),
        "equator_y": int(H * 0.50),
        "inner_ring_x0": int(W * 0.52),
        "inner_ring_x1": int(W * 0.80),
        "inner_ring_y": int(H * 0.475),
        "south_limb_y": int(H * 0.50 + H * 0.52 * 0.88),
    }


# ── OPENING v07 ────────────────────────────────────────────────────────────


def grain_layer(fi: int, n: int, births, life, sx, sy, tx, ty, sizes, lengths, rng) -> Image.Image:
    g = open_geometry()
    t = fi / FPS
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(n):
        if t < births[i] or t > births[i] + life[i]:
            continue
        u = (t - births[i]) / life[i]
        ee = u * u * (3 - 2 * u)
        # curve INTO planet: right + down arc
        x = sx[i] + (tx[i] - sx[i]) * ee
        y = sy[i] + (ty[i] - sy[i]) * ee + 55 * math.sin(math.pi * ee)
        if y > g["south_limb_y"] - 4:
            continue
        if x < g["inner_ring_x0"] - 40:
            continue
        # fade hard near cloud tops (end of path)
        fade = 1.0
        if u > 0.72:
            fade = max(0.0, 1.0 - (u - 0.72) / 0.28)
        a = int(255 * fade * (0.55 + 0.45 * (1 - abs(2 * u - 1))) )
        if a < 12:
            continue
        r = max(1, int(sizes[i]))
        # motion blur streak along velocity
        dx = (tx[i] - sx[i]) / max(life[i] * FPS, 1)
        dy = (ty[i] - sy[i]) / max(life[i] * FPS, 1) + 55 * math.pi * math.cos(math.pi * ee) / max(life[i] * FPS, 1)
        L = lengths[i]
        x0, y0 = x - dx * L * 0.5, y - dy * L * 0.5
        x1, y1 = x + dx * L * 0.5, y + dy * L * 0.5
        col = (245, 248, 255, a)
        draw.line([(x0, y0), (x1, y1)], fill=col, width=max(1, r))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, min(255, a + 40)))
    return layer.filter(ImageFilter.GaussianBlur(radius=0.45))


def build_opening_v07() -> dict:
    print("=== OPENING v07 ===", flush=True)
    work = OUT / "_work" / "open"
    work.mkdir(parents=True, exist_ok=True)
    v04_trim = work / "v04_2p5.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(V04_OPEN),
            "-t",
            f"{V04_HOLD}",
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            str(v04_trim),
        ]
    )
    still = Image.open(OPEN_STILL)
    still_dir = work / "still_frames"
    still_dir.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        ken_burns(still, fi / FPS, DUR, zoom_end=1.10).save(still_dir / f"s_{fi:04d}.png")
    still_mp4 = work / "still_push.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(still_dir / "s_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            str(still_mp4),
        ]
    )
    base_mp4 = work / "base_xfade.mp4"
    offset = max(0.05, V04_HOLD - XFADE)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(v04_trim),
            "-i",
            str(still_mp4),
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={offset},trim=duration={DUR},setpts=PTS-STARTPTS,format=yuv420p[v]",
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "16",
            str(base_mp4),
        ]
    )
    base_frames = work / "base_frames"
    base_frames.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-i", str(base_mp4), "-vf", f"fps={FPS}", str(base_frames / "b_%04d.png")])

    g = open_geometry()
    rng = np.random.default_rng(21)
    n = 1400  # dense stream
    births = rng.uniform(-2.5, DUR * 0.7, size=n)
    life = rng.uniform(1.6, 3.4, size=n)
    sx = rng.uniform(g["inner_ring_x0"], g["inner_ring_x1"], size=n)
    sy = g["inner_ring_y"] + rng.normal(0, 10, size=n)
    tx = g["planet_cx"] - g["planet_r"] * 0.90 + rng.uniform(-30, 50, size=n)
    ty = g["equator_y"] + rng.uniform(-10, 70, size=n)
    sizes = rng.uniform(1.6, 4.2, size=n)
    lengths = rng.uniform(4, 14, size=n)

    out_frames = work / "final_frames"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        bp = base_frames / f"b_{fi+1:04d}.png"
        if not bp.exists():
            bp = base_frames / f"b_{fi:04d}.png"
        base = Image.open(bp).convert("RGBA")
        grain = grain_layer(fi, n, births, life, sx, sy, tx, ty, sizes, lengths, rng)
        Image.alpha_composite(base, grain).convert("RGB").save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_open_rings_v07.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(out_frames / "f_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "15",
            "-an",
            str(dest),
        ]
    )
    cs = OUT / "edit_open_rings_v07_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "section6": "N/A world — no Orbit",
    }


# ── ICE CROWD v07 — rocks from still ───────────────────────────────────────


def cut_rocks_from_still(still: Image.Image, n: int = 4) -> list[Image.Image]:
    """Extract n white ice rocks from the still with soft alpha (no new shapes)."""
    im = resize_cover(still, W, H)
    arr = np.asarray(im).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    # white rocks: high luma, low chroma, in lower 70% / not on Saturn (right-upper)
    yy = np.arange(H)[:, None]
    xx = np.arange(W)[None, :]
    mask = (luma > 155) & (chroma < 55) & (yy > H * 0.38) & (xx < W * 0.78) & ~((xx > W * 0.55) & (yy < H * 0.55))
    # morphological open via max/min
    mimg = Image.fromarray((mask * 255).astype(np.uint8))
    mimg = mimg.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    mask = np.asarray(mimg) > 128

    # connected components (simple flood)
    visited = np.zeros_like(mask, dtype=bool)
    comps = []
    ys, xs = np.where(mask)
    for y, x in zip(ys[::3], xs[::3]):  # stride for speed
        if visited[y, x] or not mask[y, x]:
            continue
        stack = [(y, x)]
        visited[y, x] = True
        cells = []
        while stack:
            cy, cx = stack.pop()
            cells.append((cy, cx))
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx] and mask[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
        if 800 < len(cells) < 45000:
            comps.append(cells)
    comps.sort(key=len, reverse=True)
    sprites = []
    for cells in comps[:n]:
        ys_c = [c[0] for c in cells]
        xs_c = [c[1] for c in cells]
        y0, y1 = max(0, min(ys_c) - 4), min(H, max(ys_c) + 5)
        x0, x1 = max(0, min(xs_c) - 4), min(W, max(xs_c) + 5)
        crop = im.crop((x0, y0, x1, y1)).convert("RGBA")
        local = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
        for cy, cx in cells:
            local[cy - y0, cx - x0] = 255
        a = Image.fromarray(local, "L").filter(ImageFilter.GaussianBlur(radius=1.8))
        # multiply alpha by luma so edges soft
        ca = np.asarray(crop).astype(np.float32)
        cl = 0.299 * ca[:, :, 0] + 0.587 * ca[:, :, 1] + 0.114 * ca[:, :, 2]
        am = np.asarray(a).astype(np.float32) * np.clip((cl - 50) / 180, 0, 1)
        crop.putalpha(Image.fromarray(np.clip(am, 0, 255).astype(np.uint8), "L"))
        sprites.append(crop)
    # if fewer than n, duplicate with scale variants from largest
    while len(sprites) < n and sprites:
        sprites.append(sprites[0].resize(
            (max(8, int(sprites[0].size[0] * 0.7)), max(8, int(sprites[0].size[1] * 0.7))),
            Image.Resampling.LANCZOS,
        ))
    if not sprites:
        raise RuntimeError("no ice rocks extracted from still")
    return sprites[:n]


def build_ice_v07() -> dict:
    print("=== ICE CROWD v07 ===", flush=True)
    work = OUT / "_work" / "ice"
    work.mkdir(parents=True, exist_ok=True)
    still = Image.open(ICE_STILL)
    sprites = cut_rocks_from_still(still, n=4)
    for i, sp in enumerate(sprites):
        sp.save(work / f"rock_{i}.png")

    paths = [
        {"scale": 1.25, "speed": 70, "y0": 0.70, "x0": -0.12, "dir": 1, "rot": 8},
        {"scale": 1.05, "speed": 42, "y0": 0.55, "x0": 0.90, "dir": -1, "rot": -6},
        {"scale": 0.80, "speed": 26, "y0": 0.46, "x0": -0.08, "dir": 1, "rot": 4},
        {"scale": 0.60, "speed": 14, "y0": 0.38, "x0": 0.75, "dir": -1, "rot": -3},
    ]
    out_frames = work / "final_frames"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        t = fi / FPS
        base = ken_burns(still, t, DUR, zoom_end=1.08).convert("RGBA")
        for si, (sp, path) in enumerate(zip(sprites, paths)):
            ang = path["rot"] * t  # slow rotation deg
            layer = sp.rotate(ang, resample=Image.Resampling.BICUBIC, expand=True)
            sw = max(8, int(layer.size[0] * path["scale"]))
            sh = max(8, int(layer.size[1] * path["scale"]))
            layer = layer.resize((sw, sh), Image.Resampling.LANCZOS)
            x = path["x0"] * W + path["dir"] * path["speed"] * t
            y = path["y0"] * H + 6 * math.sin(0.55 * t + si)
            while x > W + sw:
                x -= W + 2 * sw
            while x < -sw:
                x += W + 2 * sw
            base.alpha_composite(layer, (int(x), int(y)))
        base.convert("RGB").save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_ice_chunks_v07.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(out_frames / "f_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "15",
            "-an",
            str(dest),
        ]
    )
    cs = OUT / "edit_ice_chunks_v07_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "section6": "N/A world — no Orbit",
        "rocks_from": ICE_STILL.name,
    }


# ── MONDAY v04 surgical ────────────────────────────────────────────────────


def monday_v04() -> dict:
    print("=== MONDAY v04 (surgical v01) ===", flush=True)
    work = OUT / "_work" / "monday"
    work.mkdir(parents=True, exist_ok=True)
    img = Image.open(MON_V01).convert("RGB")
    arr = np.asarray(img).astype(np.float32).copy()
    h, w = arr.shape[:2]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    # warm disk (exclude near-white ice)
    warm = (r > 95) & (g > 75) & (b < 145) & ((r + g) > (b + 50)) & (r > b + 15) & (luma > 60) & (luma < 210)
    ice_white = (luma > 150) & (chroma < 45)
    disk = warm & (~ice_white)
    dmask = Image.fromarray((disk * 255).astype(np.uint8))
    dmask = dmask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5))
    dmask = dmask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    dm = np.asarray(dmask) > 128
    ys = np.where(dm.any(axis=1))[0]
    south = int(ys.max()) if len(ys) else int(h * 0.65)
    # curtain ice: pale bright vertical-ish (not warm planet)
    ice = (luma > 115) & (chroma < 80) & (b + 30 >= r * 0.5) & (abs(r - g) < 55)

    rng = np.random.default_rng(3)
    fill = arr[int(h * 0.88) : h, int(w * 0.72) : w].reshape(-1, 3)
    fill_luma = 0.299 * fill[:, 0] + 0.587 * fill[:, 1] + 0.114 * fill[:, 2]
    dark = fill[fill_luma < 28]
    if len(dark) < 40:
        dark = fill

    # erase ONLY below south+2
    y0 = min(h - 1, south + 2)
    erased = 0
    for y in range(y0, h):
        xs = np.where(ice[y] & (~dm[y]))[0]
        for x in xs:
            if luma[y, x] < 38:
                continue
            sample = dark[rng.integers(0, len(dark))]
            if rng.random() < 0.003:
                sample = np.array([170, 170, 180], dtype=np.float32)
            arr[y, x] = sample
            erased += 1

    # soft-fade curtains in last 22px ON disk at limb
    blurred = np.asarray(img.filter(ImageFilter.GaussianBlur(radius=7))).astype(np.float32)
    fade = 22
    for y in range(max(0, south - fade), south + 1):
        t = (y - (south - fade)) / max(fade, 1)
        strength = 0.25 + 0.75 * t
        xs = np.where(ice[y])[0]
        for x in xs:
            arr[y, x] = (1 - strength) * arr[y, x] + strength * blurred[y, x]

    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    dest = OUT / "monday_saturn_rings_streaming_v04.png"
    out.save(dest)
    # QA crops
    bottom = out.crop((0, int(h * 0.55), w, h))
    bottom.save(OUT / "monday_v04_bottom_qa.png")
    face = out.crop((int(w * 0.12), int(h * 0.38), int(w * 0.88), south))
    face.save(OUT / "monday_v04_face_qa.png")
    v01 = Image.open(MON_V01).convert("RGB")
    if v01.size != out.size:
        v01 = v01.resize(out.size, Image.Resampling.LANCZOS)
    yb0, yb1 = int(h * 0.45), int(h * 0.85)
    band = Image.new("RGB", (w * 2 + 8, yb1 - yb0), (20, 20, 20))
    band.paste(v01.crop((0, yb0, w, yb1)), (0, 0))
    band.paste(out.crop((0, yb0, w, yb1)), (w + 8, 0))
    band.save(OUT / "monday_v01_vs_v04_south.png")
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "south_y": south,
        "erased_void_pixels": erased,
        "method": "surgical_edit_v01_no_regen",
        "qa": [
            "monday_v04_bottom_qa.png",
            "monday_v04_face_qa.png",
            "monday_v01_vs_v04_south.png",
        ],
    }


# ── SMALL ORBIT composite ──────────────────────────────────────────────────


def cut_orbit_sprite(still: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    """Cut orange Orbit (from-behind) from bare_orbit still — shape locked."""
    im = still.convert("RGB")
    arr = np.asarray(im).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    # matte orange sphere
    orange = (r > 140) & (g > 60) & (g < 180) & (b < 110) & (r > g + 25) & (r > b + 40)
    # include underside glow (warm yellow)
    glow = (r > 180) & (g > 120) & (b < 100) & (r + g > 300)
    mask = orange | glow
    mimg = Image.fromarray((mask * 255).astype(np.uint8))
    mimg = mimg.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(3))
    mimg = mimg.filter(ImageFilter.MaxFilter(7))
    mask = np.asarray(mimg) > 128
    ys, xs = np.where(mask)
    if len(xs) < 50:
        raise RuntimeError("Orbit cutout failed — no orange mask")
    pad = 8
    y0, y1 = max(0, ys.min() - pad), min(im.size[1], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(im.size[0], xs.max() + pad + 1)
    crop = im.crop((x0, y0, x1, y1)).convert("RGBA")
    local = mask[y0:y1, x0:x1]
    a = Image.fromarray((local * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(radius=1.2))
    crop.putalpha(a)
    # original center in still
    cx = int((xs.min() + xs.max()) / 2)
    cy = int((ys.min() + ys.max()) / 2)
    return crop, (cx, cy)


def build_small_orbit() -> dict:
    print("=== SMALL ORBIT composite ===", flush=True)
    work = OUT / "_work" / "orbit"
    work.mkdir(parents=True, exist_ok=True)
    still = Image.open(BARE_ORBIT_STILL)
    sprite, (ocx, ocy) = cut_orbit_sprite(still)
    sprite.save(work / "orbit_sprite.png")
    # scale sprite to match bare v05 framing (bare v05 is planet-only; place small Orbit left)
    # resize still to 1920x1080 space for placement reference
    still_cov = resize_cover(still, W, H)
    scale = W / still.size[0]
    sw = max(8, int(sprite.size[0] * scale * 0.95))
    sh = max(8, int(sprite.size[1] * scale * 0.95))
    sprite_r = sprite.resize((sw, sh), Image.Resampling.LANCZOS)
    # place similar to still: left of planet
    base_x = int(W * 0.28) - sw // 2
    base_y = int(H * 0.48) - sh // 2

    # extract bare frames
    bare_frames = work / "bare_frames"
    bare_frames.mkdir(exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(BARE_V05),
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
            str(bare_frames / "b_%04d.png"),
        ]
    )
    frames = sorted(bare_frames.glob("b_*.png"))
    out_frames = work / "final_frames"
    out_frames.mkdir(exist_ok=True)
    for i, fp in enumerate(frames):
        t = i / FPS
        # very slight drift
        dx = int(6 * math.sin(0.35 * t))
        dy = int(4 * math.cos(0.28 * t))
        base = Image.open(fp).convert("RGBA")
        base.alpha_composite(sprite_r, (base_x + dx, base_y + dy))
        base.convert("RGB").save(out_frames / f"f_{i:04d}.png")

    dest = OUT / "edit_bare_orbit_composite_v07.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(out_frames / "f_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "15",
            "-an",
            str(dest),
        ]
    )
    cs = OUT / "edit_bare_orbit_composite_v07_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "section6": "PASS_CANDIDATE — Orbit cut from approved bare_orbit_v06 still (from-behind); shape locked; slight drift; single Orbit",
        "orbit_still": BARE_ORBIT_STILL.name,
        "orbit_still_sha256": sha256(BARE_ORBIT_STILL),
        "bare_clip": BARE_V05.name,
        "bare_sha256": sha256(BARE_V05),
    }


def pack_tumble() -> dict:
    dest = OUT / "veo_orbit_tumble_v03_fallback_0-3s.mp4"
    shutil.copy2(TUMBLE_FALLBACK, dest)
    # normalize contact at 1920 if needed — contact from native
    cs = OUT / "veo_orbit_tumble_v03_fallback_0-3s_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "section6": "FALLBACK 0–3s — prior Veo tumble FAIL §6; use until Vertex Omni works (1 retry before Tue 6 Oct); never AI Studio",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_work").mkdir(exist_ok=True)

    open_m = build_opening_v07()
    ice_m = build_ice_v07()
    mon_m = monday_v04()
    orb_m = build_small_orbit()
    tum_m = pack_tumble()

    manifest = {
        "ben_order": "2026-10-01T12:27 London — v07 open/ice; Monday v04 surgical; Orbit composite; tumble fallback",
        "engine": "edit_built",
        "ai_studio_prepay": False,
        "clips": [open_m, ice_m, orb_m, tum_m],
        "monday_still": mon_m,
        "omni": "no wait; one Vertex retry only if working before Tue 6 Oct",
        "stop": "contacts to Ben then first cut",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = ["# SHA-256 — saturn_v07", "", "| File | SHA-256 | Bytes |", "|---|---|---|"]
    for c in manifest["clips"]:
        lines.append(f"| `{c['file']}` | `{c['sha256']}` | {c['bytes']} |")
        lines.append(
            f"| `{c['contact']}` | `{sha256(OUT / c['contact'])}` | {(OUT / c['contact']).stat().st_size} |"
        )
    lines.append(f"| `{mon_m['file']}` | `{mon_m['sha256']}` | {mon_m['bytes']} |")
    for q in mon_m["qa"]:
        lines.append(f"| `{q}` | `{sha256(OUT / q)}` | {(OUT / q).stat().st_size} |")
    (OUT / "SHA256.md").write_text("\n".join(lines) + "\n")
    (OUT / "README.md").write_text(
        """# Saturn v07 — Ben OK then first cut

| File | What |
|---|---|
| `edit_open_rings_v07.mp4` | Dense bright grain stream + 10% push |
| `edit_ice_chunks_v07.mp4` | Rocks from ice still + slow rotation parallax |
| `edit_bare_orbit_composite_v07.mp4` | Orbit cutout from bare_orbit_v06 on bare v05 |
| `veo_orbit_tumble_v03_fallback_0-3s.mp4` | Tumble fallback |
| `monday_saturn_rings_streaming_v04.png` | Surgical edit of v01 |

**WAIT contacts → then first cut.** Never AI Studio prepaid.
"""
    )

    UAT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    pack = [OUT / c["file"] for c in manifest["clips"]]
    pack += [OUT / c["contact"] for c in manifest["clips"]]
    pack += [OUT / mon_m["file"]] + [OUT / q for q in mon_m["qa"]]
    pack += [OUT / "MANIFEST.json", OUT / "SHA256.md", OUT / "README.md"]
    for p in pack:
        chunk_write(p, UAT / p.name)
        if p.suffix in {".png", ".md", ".json"} or "contact" in p.name:
            chunk_write(p, ART / p.name)

    print(json.dumps({"V07_DONE": True, "manifest": manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
