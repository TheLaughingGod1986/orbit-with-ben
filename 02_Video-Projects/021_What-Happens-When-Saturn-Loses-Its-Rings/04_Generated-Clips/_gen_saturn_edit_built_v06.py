#!/usr/bin/env python3
"""Saturn edit-built OPENING + ICE CROWD v06 — Ben 1 Oct 12:00 London.

B = stop Veo on open/ice; build both in the edit.

OPENING:
  - first 2.5 s of veo_open_rings_v04 (before eruption)
  - then v05-plate opening still (saturn_open_rings_v06.png) with slow push
  - composite fine bright ice grains from INNER ring edge → equator cloud tops
    from frame 0; nothing below planet / nothing flying outward

ICE CROWD:
  - approved saturn_ice_chunks_v05.png slow push
  - 3–4 separate foreground ice-chunk layers, different speeds (parallax)
  - black space between chunks; no floor

Approved leave-alone: veo_bare_saturn_v05 · friday_black_dwarf_cooling_v02

UAT: OWB UAT/saturn_edit_built_v06_for_ben_ok/ + 4-frame contacts.
WAIT Ben OK before cut. No media in git — sha256 in MANIFEST only.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
CLIPS = EP / "04_Generated-Clips"
OUT = CLIPS / "edit_built_v06"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_edit_built_v06_for_ben_ok"
)
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/artifacts"
)

V04_OPEN = CLIPS / "veo_approved_v04" / "veo_open_rings_v04.mp4"
OPEN_STILL = CLIPS / "stills_v06" / "saturn_open_rings_v06.png"  # locked still for v05 open plate
ICE_STILL = CLIPS / "stills_v05" / "saturn_ice_chunks_v05.png"
BARE_APPROVED = CLIPS / "veo_v05" / "veo_bare_saturn_v05.mp4"
FRI_APPROVED = CLIPS / "shorts_stills_v02" / "friday_black_dwarf_cooling_v02.png"

W, H = 1920, 1080
FPS = 24
DUR = 8.0
NFRAMES = int(DUR * FPS)  # 192
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


def chunk_write(src: Path | bytes, dest: Path, retries: int = 12) -> None:
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
            time.sleep(0.3)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    # fallback local stage
    stage = Path("/tmp") / f"uat_stage_{dest.name}"
    stage.write_bytes(data)
    print(f"  STAGED {stage} (iCloud lock)", flush=True)


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd[:8]), "...", flush=True)
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
    # 2x2
    fw, fh = frames[0].size
    tw, th = fw // 2, fh // 2
    sheet = Image.new("RGB", (tw * 2 + 6, th * 2 + 6), (12, 12, 14))
    for i, im in enumerate(frames):
        im = im.resize((tw, th), Image.Resampling.LANCZOS)
        x = (i % 2) * (tw + 6)
        y = (i // 2) * (th + 6)
        sheet.paste(im, (x, y))
        draw = ImageDraw.Draw(sheet)
        draw.text((x + 8, y + 8), f"t={times[i]:.2f}s", fill=(255, 220, 80))
    sheet.save(dest)
    return times


# ── geometry helpers (open still: Saturn right, rings horizontal) ──────────


def open_geometry(w: int = W, h: int = H) -> dict:
    # Fitted to saturn_open_rings_v06 / v04 open framing
    return {
        "planet_cx": int(w * 0.93),
        "planet_cy": int(h * 0.50),
        "planet_r": int(h * 0.52),
        "equator_y": int(h * 0.50),
        "inner_ring_x0": int(w * 0.55),
        "inner_ring_x1": int(w * 0.78),
        "inner_ring_y": int(h * 0.48),
        "south_limb_y": int(h * 0.50 + h * 0.52 * 0.85),  # below equator on disk
    }


def resize_cover(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return im.crop((left, top, left + w, top + h))


def ken_burns_frame(still: Image.Image, t: float, dur: float, zoom_end: float = 1.08) -> Image.Image:
    """Slow push: zoom toward Saturn (right-center)."""
    base = resize_cover(still, W, H)
    z = 1.0 + (zoom_end - 1.0) * (t / max(dur, 1e-6))
    cw, ch = int(W / z), int(H / z)
    # bias crop toward right (Saturn)
    cx = int(W * 0.62)
    cy = H // 2
    left = max(0, min(W - cw, cx - cw // 2))
    top = max(0, min(H - ch, cy - ch // 2))
    crop = base.crop((left, top, left + cw, top + ch))
    return crop.resize((W, H), Image.Resampling.LANCZOS)


def make_grain_overlay(nframes: int, seed: int = 7) -> Path:
    """RGBA particle strip: grains from inner ring → equator cloud tops."""
    work = OUT / "_work" / "grains"
    work.mkdir(parents=True, exist_ok=True)
    g = open_geometry()
    rng = np.random.default_rng(seed)
    n = 420
    # spawn along inner ring edge
    # ~25% already mid-flight at t=0 so grains move from frame 0
    births = rng.uniform(-2.2, DUR * 0.75, size=n)
    life = rng.uniform(2.0, 4.0, size=n)
    sx = rng.uniform(g["inner_ring_x0"], g["inner_ring_x1"], size=n)
    sy = g["inner_ring_y"] + rng.normal(0, 6, size=n)
    # curve INTO planet (right + slight down), never outward (left)
    tx = g["planet_cx"] - g["planet_r"] * 0.92 + rng.uniform(-20, 40, size=n)
    ty = g["equator_y"] + rng.uniform(-18, 55, size=n)  # land on cloud tops near equator
    sizes = rng.uniform(0.8, 2.4, size=n)

    for fi in range(nframes):
        t = fi / FPS
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        for i in range(n):
            if t < births[i] or t > births[i] + life[i]:
                continue
            u = (t - births[i]) / life[i]
            # ease into planet
            ee = u * u * (3 - 2 * u)
            x = sx[i] + (tx[i] - sx[i]) * ee
            # slight downward curve (quadratic)
            y = sy[i] + (ty[i] - sy[i]) * ee + 18 * math.sin(math.pi * ee)
            # kill if below south limb / outside planet approach band
            if y > g["south_limb_y"]:
                continue
            if x < g["inner_ring_x0"] - 30:
                continue  # never fly outward left
            # fade in/out
            a = int(255 * (1 - abs(2 * u - 1) ** 1.2) * 0.85)
            if a < 8:
                continue
            r = max(1, int(sizes[i]))
            col = (235, 240, 250, a)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=col)
            if r >= 2 and a > 120:
                draw.point((x, y - 1), fill=(255, 255, 255, min(255, a + 40)))
        # slight blur for soft grains
        layer = layer.filter(ImageFilter.GaussianBlur(radius=0.6))
        layer.save(work / f"g_{fi:04d}.png")
    # encode overlay with alpha via png sequence → mov with alpha? use ffmpeg overlay later from pngs
    # We'll composite in Python onto plates instead for control — return dir
    return work


def build_opening() -> dict:
    work = OUT / "_work"
    work.mkdir(parents=True, exist_ok=True)
    print("=== OPENING v06 ===", flush=True)

    # 1) trim first 2.5s of v04, scale to 1920x1080
    v04_trim = work / "open_v04_2p5.mp4"
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

    # 2) still push for full DUR (we'll xfade after 2.5)
    still = Image.open(OPEN_STILL)
    still_dir = work / "open_still_frames"
    still_dir.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        t = fi / FPS
        ken_burns_frame(still, t, DUR, zoom_end=1.07).save(still_dir / f"s_{fi:04d}.png")
    still_mp4 = work / "open_still_push.mp4"
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

    # 3) xfade: v04 for 2.5s into still push
    base_mp4 = work / "open_base_xfade.mp4"
    # offset = V04_HOLD - XFADE
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

    # 4) grain overlays composited frame-by-frame onto base
    grain_dir = make_grain_overlay(NFRAMES)
    base_frames = work / "open_base_frames"
    base_frames.mkdir(exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(base_mp4),
            "-vf",
            f"fps={FPS}",
            str(base_frames / "b_%04d.png"),
        ]
    )
    # ffmpeg numbers from 1
    out_frames = work / "open_final_frames"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        bp = base_frames / f"b_{fi+1:04d}.png"
        if not bp.exists():
            bp = base_frames / f"b_{fi:04d}.png"
        base = Image.open(bp).convert("RGBA")
        grain = Image.open(grain_dir / f"g_{fi:04d}.png").convert("RGBA")
        comp = Image.alpha_composite(base, grain).convert("RGB")
        comp.save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_open_rings_v06.mp4"
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
    cs = OUT / "edit_open_rings_v06_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "sources": {
            "v04_open_trim_s": V04_HOLD,
            "v04_sha256": sha256(V04_OPEN),
            "open_still": OPEN_STILL.name,
            "open_still_sha256": sha256(OPEN_STILL),
        },
        "notes": "2.5s v04 open + still push + inner-ring ice grains to equator; void below clean",
    }


# ── ICE CROWD ──────────────────────────────────────────────────────────────


def make_ice_chunk_sprite(size: int, seed: int) -> Image.Image:
    """Procedural crystalline ice chunk — no rectangular still crops (those pulled planet/rings)."""
    rng = np.random.default_rng(seed)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    cx = cy = size / 2
    # irregular polygon
    nvert = int(rng.integers(6, 10))
    pts = []
    for k in range(nvert):
        ang = 2 * math.pi * k / nvert + float(rng.uniform(-0.25, 0.25))
        rad = size * float(rng.uniform(0.28, 0.48))
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    # base fill
    base = (
        int(rng.integers(200, 235)),
        int(rng.integers(205, 240)),
        int(rng.integers(215, 245)),
        245,
    )
    draw.polygon(pts, fill=base)
    # facet overlays
    for _ in range(int(rng.integers(3, 6))):
        a0 = float(rng.uniform(0, 2 * math.pi))
        span = float(rng.uniform(0.6, 1.4))
        facet = []
        for k in range(3):
            ang = a0 + span * k / 2
            rad = size * float(rng.uniform(0.12, 0.42))
            facet.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        bright = int(rng.integers(0, 2)) == 0
        if bright:
            col = (250, 252, 255, int(rng.integers(120, 200)))
        else:
            col = (140, 150, 165, int(rng.integers(80, 140)))
        draw.polygon(facet, fill=col)
    # soft alpha edge via mask
    arr = np.asarray(canvas).astype(np.float32)
    alpha = arr[:, :, 3]
    # distance-ish falloff already from polygon; slight blur
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    # erode hard square bounds: keep only non-zero alpha region
    a = out.split()[-1].filter(ImageFilter.GaussianBlur(radius=1.2))
    out.putalpha(a)
    return out


def extract_chunk_sprites(still: Image.Image, n: int = 4) -> list[Image.Image]:
    """Build n parallax ice-chunk sprites (procedural — avoids still-crop planet/ring cards)."""
    del still  # still used as bed only; sprites are separate layers
    sizes = [220, 170, 130, 95]
    return [make_ice_chunk_sprite(sizes[i % len(sizes)], seed=40 + i * 17) for i in range(n)]


def build_ice_crowd() -> dict:
    work = OUT / "_work"
    work.mkdir(parents=True, exist_ok=True)
    print("=== ICE CROWD v06 ===", flush=True)
    still = Image.open(ICE_STILL)
    sprites = extract_chunk_sprites(still, n=4)
    for i, sp in enumerate(sprites):
        sp.save(work / f"ice_sprite_{i}.png")

    # motion paths: different speeds (parallax). Closer (larger) moves faster L→R or R→L
    paths = [
        {"scale": 1.35, "speed": 95, "y0": 0.72, "x0": -0.15, "dir": 1},  # near, fast
        {"scale": 1.10, "speed": 55, "y0": 0.58, "x0": 0.85, "dir": -1},
        {"scale": 0.85, "speed": 32, "y0": 0.48, "x0": -0.05, "dir": 1},
        {"scale": 0.65, "speed": 18, "y0": 0.40, "x0": 0.70, "dir": -1},  # far, slow
    ]

    out_frames = work / "ice_final_frames"
    out_frames.mkdir(exist_ok=True)
    for fi in range(NFRAMES):
        t = fi / FPS
        base = ken_burns_frame(still, t, DUR, zoom_end=1.06).convert("RGBA")
        # slight extra push bias already in ken_burns
        for si, (sp, path) in enumerate(zip(sprites, paths)):
            sw = max(8, int(sp.size[0] * path["scale"]))
            sh = max(8, int(sp.size[1] * path["scale"]))
            layer = sp.resize((sw, sh), Image.Resampling.LANCZOS)
            x = path["x0"] * W + path["dir"] * path["speed"] * t
            y = path["y0"] * H + 8 * math.sin(0.7 * t + si)
            # wrap gently so always some chunks
            while x > W + sw:
                x -= W + 2 * sw
            while x < -sw:
                x += W + 2 * sw
            base.alpha_composite(layer, (int(x), int(y)))
        base.convert("RGB").save(out_frames / f"f_{fi:04d}.png")

    dest = OUT / "edit_ice_chunks_v06.mp4"
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
    cs = OUT / "edit_ice_chunks_v06_contact.png"
    times = contact_sheet(dest, cs)
    return {
        "file": dest.name,
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "contact": cs.name,
        "contact_times": times,
        "sources": {
            "ice_still": ICE_STILL.name,
            "ice_still_sha256": sha256(ICE_STILL),
            "parallax_layers": 4,
        },
        "notes": "ice still slow push + 4 parallax chunk layers; black between; no floor",
    }


def write_approvals() -> dict:
    return {
        "ben_order": "2026-10-01T12:00 London — B edit-built open+ice; approve bare v05 + Friday BD v02",
        "approved_no_touch": [
            {
                "file": BARE_APPROVED.name,
                "path": str(BARE_APPROVED),
                "sha256": sha256(BARE_APPROVED),
                "bytes": BARE_APPROVED.stat().st_size,
                "status": "APPROVED — do not remint",
            },
            {
                "file": FRI_APPROVED.name,
                "path": str(FRI_APPROVED),
                "sha256": sha256(FRI_APPROVED),
                "bytes": FRI_APPROVED.stat().st_size,
                "status": "APPROVED — do not remint",
            },
        ],
        "omni": "Vertex Free Trial only — no AI Studio prepay; prior 500s recorded in MANIFEST_OMNI_VERTEX.json",
        "stop": "WAIT Ben OK on edit-built contacts before cut",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_work").mkdir(exist_ok=True)
    (OUT / "_contact").mkdir(exist_ok=True)

    approvals = write_approvals()
    print("APPROVED leave-alone:", json.dumps(approvals["approved_no_touch"], indent=2), flush=True)

    open_meta = build_opening()
    ice_meta = build_ice_crowd()

    # move contacts also under _contact
    for name in (open_meta["contact"], ice_meta["contact"]):
        src = OUT / name
        chunk_write(src, OUT / "_contact" / name)

    manifest = {
        "engine": "edit_built",
        "ben_order": approvals["ben_order"],
        "duration_seconds": DUR,
        "fps": FPS,
        "size": f"{W}x{H}",
        "approvals": approvals,
        "clips": [open_meta, ice_meta],
        "stop": "WAIT Ben OK — contacts only; not in cut yet",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    sha_md = "# SHA-256 — saturn_edit_built_v06\n\n| File | SHA-256 | Bytes |\n|---|---|---|\n"
    for c in manifest["clips"]:
        sha_md += f"| `{c['file']}` | `{c['sha256']}` | {c['bytes']} |\n"
        sha_md += f"| `{c['contact']}` | `{sha256(OUT / c['contact'])}` | {(OUT / c['contact']).stat().st_size} |\n"
    for a in approvals["approved_no_touch"]:
        sha_md += f"| `{a['file']}` (approved leave) | `{a['sha256']}` | {a['bytes']} |\n"
    (OUT / "SHA256.md").write_text(sha_md)
    readme = """# Saturn edit-built v06 — Ben OK

Ben 1 Oct 12:00 London · path **B** (stop Veo on open/ice).

| File | What |
|---|---|
| `edit_open_rings_v06.mp4` | 2.5s v04 open → open still slow push + inner-ring ice grains to equator |
| `edit_open_rings_v06_contact.png` | 4-frame contact |
| `edit_ice_chunks_v06.mp4` | ice v05 still slow push + 4 parallax chunk layers |
| `edit_ice_chunks_v06_contact.png` | 4-frame contact |

**Approved leave-alone:** `veo_bare_saturn_v05` · `friday_black_dwarf_cooling_v02`

**WAIT Ben OK on contacts before these go into the cut.** Omni stays Vertex-only.
"""
    (OUT / "README.md").write_text(readme)

    # pack UAT + artifacts (media OK in UAT; not git)
    UAT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    pack_files = [
        OUT / open_meta["file"],
        OUT / open_meta["contact"],
        OUT / ice_meta["file"],
        OUT / ice_meta["contact"],
        OUT / "MANIFEST.json",
        OUT / "SHA256.md",
        OUT / "README.md",
    ]
    for p in pack_files:
        chunk_write(p, UAT / p.name)
        if p.suffix in {".png", ".md", ".json"} or "contact" in p.name:
            chunk_write(p, ART / p.name)
        elif p.suffix == ".mp4":
            # also stage contacts already; copy mp4 sha note only to ART via manifest
            pass
    # always put contacts in ART for CoS
    for c in (open_meta["contact"], ice_meta["contact"]):
        chunk_write(OUT / c, ART / c)

    print(json.dumps({"EDIT_BUILT_V06_DONE": True, **manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
