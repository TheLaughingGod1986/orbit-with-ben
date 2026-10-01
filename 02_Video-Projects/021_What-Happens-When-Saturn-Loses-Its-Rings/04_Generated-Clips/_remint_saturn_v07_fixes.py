#!/usr/bin/env python3
"""Remint v07 fails — Ben 12:27 reads.

OPEN: v04 only ~1.2s (pre-eruption); dense bright STREAM curving DOWN into equator.
ICE: compact rocks from still only (reject strip/wedge aspect ratios).
MONDAY: soft feather erase below limb (no hard pixel blocks).
Re-pack UAT saturn_v07_for_ben_ok contacts.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import _gen_saturn_v07 as v07

OUT = v07.OUT
UAT = v07.UAT
ART = v07.ART
W, H, FPS, DUR, NFRAMES = v07.W, v07.H, v07.FPS, v07.DUR, v07.NFRAMES


def rebuild_opening() -> dict:
    print("=== REMINT OPENING v07 ===", flush=True)
    work = OUT / "_work" / "open_b"
    work.mkdir(parents=True, exist_ok=True)
    v04_trim = work / "v04_1p2.mp4"
    v07.run(
        [
            "ffmpeg", "-y", "-i", str(v07.V04_OPEN), "-t", "1.2",
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(v04_trim),
        ]
    )
    still = Image.open(v07.OPEN_STILL)
    still_dir = work / "still_frames"
    still_dir.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        v07.ken_burns(still, fi / FPS, DUR, zoom_end=1.10).save(still_dir / f"s_{fi:04d}.png")
    still_mp4 = work / "still_push.mp4"
    v07.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(still_dir / "s_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(still_mp4),
        ]
    )
    base_mp4 = work / "base.mp4"
    # pad v04 to 1.2 then xfade into still
    v07.run(
        [
            "ffmpeg", "-y", "-i", str(v04_trim), "-i", str(still_mp4),
            "-filter_complex",
            "[0:v]tpad=stop_mode=clone:stop_duration=0.01[v0];"
            "[v0][1:v]xfade=transition=fade:duration=0.35:offset=0.85,"
            f"trim=duration={DUR},setpts=PTS-STARTPTS,format=yuv420p[v]",
            "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", str(base_mp4),
        ]
    )
    base_frames = work / "base_frames"
    base_frames.mkdir(exist_ok=True)
    v07.run(["ffmpeg", "-y", "-i", str(base_mp4), "-vf", f"fps={FPS}", str(base_frames / "b_%04d.png")])

    g = v07.open_geometry()
    rng = np.random.default_rng(33)
    n = 2200
    births = rng.uniform(-3.0, DUR * 0.65, size=n)
    life = rng.uniform(2.0, 4.2, size=n)
    sx = rng.uniform(g["inner_ring_x0"], g["inner_ring_x1"], size=n)
    sy = g["inner_ring_y"] + rng.normal(0, 8, size=n)
    # land ON equator cloud tops (right, slight down — never up into void above rings)
    tx = g["planet_cx"] - g["planet_r"] * 0.88 + rng.uniform(-20, 40, size=n)
    ty = g["equator_y"] + rng.uniform(8, 85, size=n)  # always below ring plane
    sizes = rng.uniform(2.2, 5.5, size=n)
    lengths = rng.uniform(8, 22, size=n)

    out_frames = work / "final"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        bp = base_frames / f"b_{fi+1:04d}.png"
        if not bp.exists():
            bp = base_frames / f"b_{fi:04d}.png"
        base = Image.open(bp).convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        t = fi / FPS
        for i in range(n):
            if t < births[i] or t > births[i] + life[i]:
                continue
            u = (t - births[i]) / life[i]
            ee = u * u * (3 - 2 * u)
            x = sx[i] + (tx[i] - sx[i]) * ee
            # strong downward curve into planet
            y = sy[i] + (ty[i] - sy[i]) * ee + 90 * (ee * ee)
            if y > g["south_limb_y"] - 2:
                continue
            if x < g["inner_ring_x0"] - 20:
                continue
            fade = 1.0 if u < 0.75 else max(0.0, 1.0 - (u - 0.75) / 0.25)
            a = int(255 * fade * 0.95)
            if a < 20:
                continue
            r = max(2, int(sizes[i]))
            dx = (tx[i] - sx[i]) * 0.02
            dy = (ty[i] - sy[i]) * 0.02 + 3
            L = lengths[i]
            draw.line([(x - dx * L, y - dy * L), (x + dx * L * 0.2, y + dy * L * 0.2)], fill=(250, 252, 255, a), width=max(2, r // 2 + 1))
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, min(255, a + 30)))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=0.55))
        Image.alpha_composite(base, layer).convert("RGB").save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_open_rings_v07.mp4"
    v07.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_frames / "f_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-an", str(dest),
        ]
    )
    cs = OUT / "edit_open_rings_v07_contact.png"
    times = v07.contact_sheet(dest, cs)
    return {"file": dest.name, "sha256": v07.sha256(dest), "bytes": dest.stat().st_size, "contact": cs.name, "contact_times": times, "section6": "N/A world"}


def rebuild_ice() -> dict:
    print("=== REMINT ICE v07 ===", flush=True)
    work = OUT / "_work" / "ice_b"
    work.mkdir(parents=True, exist_ok=True)
    still = Image.open(v07.ICE_STILL)
    im = v07.resize_cover(still, W, H)
    arr = np.asarray(im).astype(np.float32)
    r, g, bch = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * bch
    chroma = np.maximum(np.maximum(r, g), bch) - np.minimum(np.minimum(r, g), bch)
    yy = np.arange(H)[:, None]
    xx = np.arange(W)[None, :]
    mask = (luma > 160) & (chroma < 50) & (yy > H * 0.42) & (xx < W * 0.72) & ~((xx > W * 0.52) & (yy < H * 0.58))
    mimg = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    mask = np.asarray(mimg) > 128
    visited = np.zeros_like(mask, dtype=bool)
    comps = []
    ys, xs = np.where(mask)
    for y, x in zip(ys[::4], xs[::4]):
        if visited[y, x] or not mask[y, x]:
            continue
        stack = [(y, x)]
        visited[y, x] = True
        cells = []
        while stack:
            cy, cx = stack.pop()
            cells.append((cy, cx))
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx] and mask[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
        if not (1200 < len(cells) < 28000):
            continue
        ys_c = [c[0] for c in cells]
        xs_c = [c[1] for c in cells]
        bh = max(ys_c) - min(ys_c) + 1
        bw = max(xs_c) - min(xs_c) + 1
        aspect = bw / max(bh, 1)
        if aspect > 2.2 or aspect < 0.45:
            continue  # reject strips/wedges
        comps.append(cells)
    comps.sort(key=len, reverse=True)
    sprites = []
    for cells in comps[:4]:
        ys_c = [c[0] for c in cells]
        xs_c = [c[1] for c in cells]
        y0, y1 = max(0, min(ys_c) - 3), min(H, max(ys_c) + 4)
        x0, x1 = max(0, min(xs_c) - 3), min(W, max(xs_c) + 4)
        crop = im.crop((x0, y0, x1, y1)).convert("RGBA")
        local = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
        for cy, cx in cells:
            local[cy - y0, cx - x0] = 255
        a = Image.fromarray(local, "L").filter(ImageFilter.GaussianBlur(radius=1.5))
        ca = np.asarray(crop).astype(np.float32)
        cl = 0.299 * ca[:, :, 0] + 0.587 * ca[:, :, 1] + 0.114 * ca[:, :, 2]
        am = np.asarray(a).astype(np.float32) * np.clip((cl - 60) / 160, 0, 1)
        crop.putalpha(Image.fromarray(np.clip(am, 0, 255).astype(np.uint8), "L"))
        sprites.append(crop)
        crop.save(work / f"rock_{len(sprites)-1}.png")
    if len(sprites) < 3:
        raise SystemExit(f"only {len(sprites)} compact rocks — abort")
    while len(sprites) < 4:
        s = sprites[0]
        sprites.append(s.resize((max(8, int(s.size[0] * 0.75)), max(8, int(s.size[1] * 0.75))), Image.Resampling.LANCZOS))

    paths = [
        {"scale": 1.2, "speed": 65, "y0": 0.68, "x0": -0.1, "dir": 1, "rot": 7},
        {"scale": 1.0, "speed": 40, "y0": 0.54, "x0": 0.88, "dir": -1, "rot": -5},
        {"scale": 0.78, "speed": 24, "y0": 0.45, "x0": -0.06, "dir": 1, "rot": 4},
        {"scale": 0.58, "speed": 13, "y0": 0.38, "x0": 0.72, "dir": -1, "rot": -3},
    ]
    out_frames = work / "final"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        t = fi / FPS
        base = v07.ken_burns(still, t, DUR, zoom_end=1.08).convert("RGBA")
        for si, (sp, path) in enumerate(zip(sprites, paths)):
            layer = sp.rotate(path["rot"] * t, resample=Image.Resampling.BICUBIC, expand=True)
            sw = max(8, int(layer.size[0] * path["scale"]))
            sh = max(8, int(layer.size[1] * path["scale"]))
            layer = layer.resize((sw, sh), Image.Resampling.LANCZOS)
            x = path["x0"] * W + path["dir"] * path["speed"] * t
            y = path["y0"] * H + 5 * math.sin(0.5 * t + si)
            while x > W + sw:
                x -= W + 2 * sw
            while x < -sw:
                x += W + 2 * sw
            base.alpha_composite(layer, (int(x), int(y)))
        base.convert("RGB").save(out_frames / f"f_{fi:04d}.png")
    dest = OUT / "edit_ice_chunks_v07.mp4"
    v07.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_frames / "f_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-an", str(dest),
        ]
    )
    cs = OUT / "edit_ice_chunks_v07_contact.png"
    times = v07.contact_sheet(dest, cs)
    return {"file": dest.name, "sha256": v07.sha256(dest), "bytes": dest.stat().st_size, "contact": cs.name, "contact_times": times, "section6": "N/A world", "n_rocks": len(sprites)}


def rebuild_monday() -> dict:
    print("=== REMINT MONDAY v04 soft ===", flush=True)
    img = Image.open(v07.MON_V01).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    h, w = arr.shape[:2]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    warm = (r > 95) & (g > 75) & (b < 145) & ((r + g) > (b + 50)) & (r > b + 15) & (luma > 60) & (luma < 210)
    ice_white = (luma > 150) & (chroma < 45)
    disk = warm & (~ice_white)
    dmask = Image.fromarray((disk * 255).astype(np.uint8))
    dmask = dmask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(7))
    dmask = dmask.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.MinFilter(7))
    dm = np.asarray(dmask) > 128
    ys = np.where(dm.any(axis=1))[0]
    south = int(ys.max()) if len(ys) else int(h * 0.65)
    ice = (luma > 110) & (chroma < 85) & (b + 35 >= r * 0.48) & (abs(r - g) < 60)

    # build soft starfield fill from corners
    fill = arr.copy()
    rng = np.random.default_rng(5)
    for y in range(h):
        for x in range(w):
            if y > south + 1 and not dm[y, x]:
                fill[y, x] = [4, 4, 6]
    # sprinkle stars
    for _ in range(400):
        x = int(rng.integers(0, w))
        y = int(rng.integers(south + 2, h))
        fill[y, x] = [float(rng.integers(140, 220))] * 3

    out = arr.copy()
    # soft strength by distance below south
    for y in range(south - 20, h):
        if y < 0:
            continue
        if y <= south:
            # on-disk fade of curtains into atmosphere
            t = (y - (south - 20)) / 20.0
            strength = 0.15 + 0.55 * max(0, t)
            xs = np.where(ice[y])[0]
            blur_row = arr[y]  # will mix toward local warm
            for x in xs:
                # mix toward nearby warm disk color
                wx = min(w - 1, max(0, x))
                warm_c = arr[max(0, south - 40), wx]
                out[y, x] = (1 - strength) * out[y, x] + strength * warm_c
        else:
            dist = y - south
            # feather 0→1 over 28px then hard
            strength = min(1.0, dist / 28.0)
            strength = strength * strength * (3 - 2 * strength)
            xs = np.where(ice[y] & (~dm[y]))[0]
            for x in xs:
                if luma[y, x] < 35:
                    continue
                out[y, x] = (1 - strength) * out[y, x] + strength * fill[y, x]

    # second pass: any remaining bright in deep void
    for y in range(south + 30, h):
        for x in range(int(w * 0.1), int(w * 0.9)):
            if dm[y, x]:
                continue
            lu = 0.299 * out[y, x, 0] + 0.587 * out[y, x, 1] + 0.114 * out[y, x, 2]
            if lu > 42:
                out[y, x] = fill[y, x]

    result = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    dest = OUT / "monday_saturn_rings_streaming_v04.png"
    result.save(dest)
    result.crop((0, int(h * 0.55), w, h)).save(OUT / "monday_v04_bottom_qa.png")
    result.crop((int(w * 0.12), int(h * 0.38), int(w * 0.88), south)).save(OUT / "monday_v04_face_qa.png")
    v01 = Image.open(v07.MON_V01).convert("RGB")
    if v01.size != result.size:
        v01 = v01.resize(result.size, Image.Resampling.LANCZOS)
    yb0, yb1 = int(h * 0.45), int(h * 0.85)
    band = Image.new("RGB", (w * 2 + 8, yb1 - yb0), (20, 20, 20))
    band.paste(v01.crop((0, yb0, w, yb1)), (0, 0))
    band.paste(result.crop((0, yb0, w, yb1)), (w + 8, 0))
    band.save(OUT / "monday_v01_vs_v04_south.png")
    return {
        "file": dest.name,
        "sha256": v07.sha256(dest),
        "bytes": dest.stat().st_size,
        "south_y": south,
        "method": "surgical_soft_feather_v01",
        "qa": ["monday_v04_bottom_qa.png", "monday_v04_face_qa.png", "monday_v01_vs_v04_south.png"],
    }


def main() -> None:
    open_m = rebuild_opening()
    ice_m = rebuild_ice()
    mon_m = rebuild_monday()
    # keep orbit + tumble from prior
    orb = OUT / "edit_bare_orbit_composite_v07.mp4"
    tum = OUT / "veo_orbit_tumble_v03_fallback_0-3s.mp4"
    manifest = {
        "ben_order": "2026-10-01T12:27 remint fixes",
        "clips": [
            open_m,
            ice_m,
            {
                "file": orb.name,
                "sha256": v07.sha256(orb),
                "bytes": orb.stat().st_size,
                "contact": "edit_bare_orbit_composite_v07_contact.png",
                "section6": "PASS_CANDIDATE — Orbit from bare_orbit_v06 still",
            },
            {
                "file": tum.name,
                "sha256": v07.sha256(tum),
                "bytes": tum.stat().st_size,
                "contact": "veo_orbit_tumble_v03_fallback_0-3s_contact.png",
                "section6": "FALLBACK 0–3s",
            },
        ],
        "monday_still": mon_m,
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = ["# SHA-256 — saturn_v07", "", "| File | SHA-256 | Bytes |", "|---|---|---|"]
    for c in manifest["clips"]:
        lines.append(f"| `{c['file']}` | `{c['sha256']}` | {c['bytes']} |")
        if "contact" in c:
            cp = OUT / c["contact"]
            if cp.exists():
                lines.append(f"| `{c['contact']}` | `{v07.sha256(cp)}` | {cp.stat().st_size} |")
    lines.append(f"| `{mon_m['file']}` | `{mon_m['sha256']}` | {mon_m['bytes']} |")
    (OUT / "SHA256.md").write_text("\n".join(lines) + "\n")

    UAT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    pack = [OUT / c["file"] for c in manifest["clips"]]
    pack += [OUT / open_m["contact"], OUT / ice_m["contact"]]
    pack += [OUT / mon_m["file"]] + [OUT / q for q in mon_m["qa"]]
    pack += [OUT / "MANIFEST.json", OUT / "SHA256.md", OUT / "README.md"]
    # regenerate contacts for open/ice
    for c in (open_m, ice_m):
        v07.chunk_write(OUT / c["contact"], UAT / c["contact"])
        v07.chunk_write(OUT / c["contact"], ART / c["contact"])
    for p in pack:
        if p.exists():
            v07.chunk_write(p, UAT / p.name)
            if p.suffix in {".png", ".md", ".json"}:
                v07.chunk_write(p, ART / p.name)
    print(json.dumps({"REMINT_DONE": True, "manifest": manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
