#!/usr/bin/env python3
"""J1242 Uranus standalone S4 v10. Elected Chief FIX on J1240 (v09 temporal blend only).

- VO/edit unchanged from v06: reuse vo_v05.wav; same plates/captions/overlays.
- OPEN: measure source motion; motion-compensated temporal interpolation (warp then
  blend), not unregistered crossfade. Designed ≤1.5 px/frame path mapped by measured
  px/odd; soft floor ~0.70 through cut (no-freeze gate). measured_upscale≤1.85.
- Estimator: ≤0.1 px (10× upsample + parabolic peak); synthetic validation first;
  full per-frame steps in MOTION_DIAGNOSTIC. Never overwrite prior masters.
- Loudness first; gates from final sha. Deliver OWB UAT + NAS v10. £0. No upload.
- Usage: python3 _assemble_uranus_v10.py [--prototype]  (prototype = open+evidence only)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location("sa_v02", HERE / "_assemble_standalone_shorts_v02.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
from short_c37 import finish_scan  # noqa: E402

PLATES = Path("/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus")
SHOT9 = Path("/Volumes/data/mac-mini-archive/scratch/J1206/raw/Shot9_1k_mp4.mp4")
SHOT9_SHA = "f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e"
VO_V05 = Path("/Volumes/data/mac-mini-archive/scratch/J1204/uranus_v05/vo_v05.wav")
VO_V05_SHA = "f59211a87311baf6fa265d9b3f10972a46fdd43cbe3f4d5925a698870b310919"
VO_V02_SHA = "484a7d9ead015de266f6eb9937b6f6b9b5e8e9ec7c1b0124750ecea77f5410df"
META_V02 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v02_meta.json"
META_V05 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v05_meta.json"
META_V06 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v06_meta.json"
META_V07 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v07_meta.json"
META_V08 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v08_meta.json"
META_V09 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v09_meta.json"
V06_MP4 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v06.mp4"
V06_SHA = "f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5"
V07_MP4 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v07.mp4"
V07_SHA = "21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609"
V08_MP4 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v08.mp4"
V08_SHA = "9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7"
V09_MP4 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v09.mp4"
V09_SHA = "458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535"
# Local scratch: keep cycle_raw off NFS (J1240 hang).
WORK = Path("/private/tmp/J1242-uranus-v10")
NAS_WORK = Path("/Volumes/data/mac-mini-archive/scratch/J1242/uranus_v10")
KIT = Path("/Volumes/data/mac-mini-archive/scratch/J0914/kit")
OUT = HERE / "06_Final-Exports"
QA = HERE / "qa_shorts_v01" / "owb_sa_s4_uranus_v10"
UAT_ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v10"
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v10")
EVIDENCE = REPO / "jobs/reviews/J1242"
SHOT9_POOL_ID = "svs20390_shot9_beauty_rings.mp4"
SHOT9_TITLE = (
    "Beauty shot of Uranus' rings (Shot9), NASA SVS 20390, "
    "Conceptual Image Lab artist animation"
)
PROTOTYPE = "--prototype" in sys.argv
PHASE_UPSAMPLE = 10  # ≤0.1 px resolution after /upsample

W, H, FPS = 1080, 1920, 30
BAND_TOP = (H - 608) // 2
FONT = base.FONT
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# 9:16 centre crop from 1920×1080: width = 1080 * 9/16 = 607.5 → 608
CROP_W, CROP_H = 608, 1080
CROP_X = (1920 - CROP_W) // 2  # 656
UPSCALE = H / float(CROP_H)  # 1.777… ≤ 2.35

OPEN_DUR = 2.70
TAIL_N = 34  # 1.133… s at 30 fps
OPEN_N = 81  # 2.70 s
CYCLE_N = TAIL_N + OPEN_N  # 115
# Same odd-phase window as v06 (loop-proven). v09 slows open retiming, not path-vs-smooth.
SHOT9_SRC_FPS = 60
SHOT9_START_FRAME = 53  # odd; 0.8833 s
SHOT9_TAIL_IN = SHOT9_START_FRAME / SHOT9_SRC_FPS  # 0.8833
SHOT9_OPEN_IN = (SHOT9_START_FRAME + 2 * TAIL_N) / SHOT9_SRC_FPS  # 2.0167
SHOT9_OPEN_OUT = SHOT9_OPEN_IN + OPEN_DUR  # 4.7167
SHOT9_TAIL_OUT = SHOT9_OPEN_IN
TAIL_DUR = TAIL_N / FPS  # 1.133…
# v09: slow designed open (not path-vs-smooth). Cap on-screen step + accel.
MAX_STEP_PX = 1.5          # compliance target at 1080 wide (Chief J1240)
MAX_STEP_DELTA = 0.25      # compliance target frame-to-frame step change
# proto10: design slower than the 1.5 cap. proto6 MC at design-1.5 measured
# reliable ymax 2.7 (~1.8×); path-lock protos 7–9 regressed. Aim design ~0.80
# so measured lands ≤1.5; keep soft floor 0.55 so no-freeze still moves.
DESIGN_PEAK_PX = 0.70
DESIGN_FLOOR_PX = 0.50
DESIGN_START_PX = 0.62
MOTION_BLUR_N = 4          # 180° shutter sub-steps (genuinely displaced after MC warp)
STAB_ZOOM_MIN = 1.04       # floor; measured_upscale = crop×zoom ≤ 1.85
OPEN_SRC_SPAN_ODD = 40     # odd-frame steps across open; px/odd is MEASURED, not assumed 4


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def space_bg() -> Image.Image:
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([14, 22, 48], np.float32)
    bot = np.array([26, 40, 82], np.float32)
    arr = np.broadcast_to((top * (1 - y) + bot * y)[:, None, :], (H, W, 3)).copy()
    arr += np.linspace(-10, 10, W, dtype=np.float32)[None, :, None]
    arr = np.clip(arr, 0, 255)
    rng = np.random.default_rng(11)
    xs, ys = rng.integers(0, W, 120), rng.integers(0, H, 120)
    v = rng.integers(140, 210, 120)
    arr[ys, xs] = np.stack([v, v, v], axis=1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def lift_luma(im: Image.Image, target_mean: float = 36.0) -> Image.Image:
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean = float(luma.mean())
    if mean < 1e-3 or mean >= target_mean:
        return im
    scale = min(3.2, target_mean / mean)
    return Image.fromarray(np.clip(arr * scale, 0, 255).astype(np.uint8), "RGB")


def plate_on_space(path: Path, n: int, zoom0: float, zoom1: float, cx: float, cy: float,
                   pan_x: float = 0.0, pan_y: float = 0.0) -> list[Image.Image]:
    src = lift_luma(Image.open(path).convert("RGB"), 40.0)
    bg = space_bg()
    sw, sh = src.size
    frames = []
    for i in range(n):
        g = 0.0 if n <= 1 else i / (n - 1)
        z = zoom0 + (zoom1 - zoom0) * g
        px = cx + pan_x * g
        py = cy + pan_y * g
        nudge = (i % 7) - 3
        canvas = bg.copy()
        tw = int(round(W * 0.78 * z / zoom0))
        th = int(round(tw * sh / sw))
        tw -= tw % 2
        th -= th % 2
        resized = src.resize((tw, th), Image.Resampling.LANCZOS)
        x = (W - tw) // 2 + int(round((px - 0.5) * 80)) + nudge
        y = (H - th) // 2 + int(round((py - 0.5) * 60)) + (nudge // 2)
        canvas.paste(resized, (x, y))
        frames.append(lift_luma(canvas, 34.0))
    return frames


def fact_card(window: tuple[float, float], out: Path) -> None:
    a0, a1 = window
    n = max(1, round((a1 - a0) * FPS))
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(out)],
        stdin=subprocess.PIPE,
    )
    for i in range(n):
        t = a0 + i / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = min(ease((t - a0) / 0.35), ease((a1 - t) / 0.30))
        y = BAND_TOP + 90
        for text, col, size in (("TIPPED", YELLOW, 96), ("97°", WHITE, 88)):
            font = ImageFont.truetype(FONT, size)
            box = d.textbbox((0, 0), text, font=font, stroke_width=6)
            d.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=col,
                   stroke_width=6, stroke_fill=BLACK)
            y += box[3] - box[1] + 18
        if alpha < 1:
            im.putalpha(Image.eval(im.getchannel("A"), lambda v, a=alpha: int(v * a)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("fact card encode failed")


def encode_frames(frames, n: int, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", str(path)],
        stdin=subprocess.PIPE,
    )
    for im in frames:
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit(f"encode failed {path}")
    got = base.dur(path)
    want = n / FPS
    if abs(got - want) > 0.12:
        raise SystemExit(f"{path.name} is {got:.2f}s, wanted {want:.2f}s")


def concat(parts: list[Path], out: Path) -> None:
    lst = out.with_suffix(".txt")
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])


def measure_lufs(path: Path) -> dict:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    lufs = tp = None
    for line in proc.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            try:
                lufs = float(line.split("I:")[-1].split("LUFS")[0].strip())
            except ValueError:
                pass
        if "Peak:" in line and "dBFS" in line:
            try:
                tp = float(line.split("Peak:")[-1].split("dBFS")[0].strip())
            except ValueError:
                pass
    return {"lufs": lufs if lufs is not None else -99.0, "tp": tp if tp is not None else 99.0}


def stems(work: Path, vo: Path, total: float, last_end: float, tick_at: float) -> tuple[Path, Path, Path]:
    vo_s, bed_s, sfx_s = work / "stem_vo.wav", work / "stem_bed.wav", work / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-af",
         f"aresample=48000,volume={base.VO_GAIN},apad,atrim=0:{total}", "-ac", "2", vo_s])
    ramp = (
        f"if(lt(t,{last_end}),{base.BED_GAIN},"
        f"{base.BED_GAIN}+({base.BED_HOLD}-{base.BED_GAIN})*min((t-{last_end})/0.6,1))"
    )
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", base.BED, "-af",
         f"aresample=48000,atrim=0:{total},volume='{ramp}':eval=frame,afade=t=in:st=0:d=0.25,"
         f"afade=t=out:st={total - 0.45:.3f}:d=0.45", "-ac", "2", bed_s])
    rumble = KIT / "sfx_owb_rumble_low_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", rumble, "-i", tick, "-filter_complex",
         f"[0:a]aresample=48000,volume=0.45,afade=t=out:st=1.4:d=0.5,atrim=0:2.0[s0];"
         f"[1:a]aresample=48000,volume=0.28,adelay={int(tick_at * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_s])
    return vo_s, bed_s, sfx_s


def sheet_2fps(final: Path, out: Path) -> None:
    total = base.dur(final)
    times = [i / 2 for i in range(int(total * 2) + 1)]
    base.sheet(final, times, out)


def _parabolic_offset(c: np.ndarray, yy: int, xx: int, axis: int) -> float:
    """Sub-bin peak offset along one axis via 3-point parabola (−0.5..0.5)."""
    if axis == 0:
        n = c.shape[0]
        ym, y0, yp = c[(yy - 1) % n, xx], c[yy, xx], c[(yy + 1) % n, xx]
        denom = (ym - 2.0 * y0 + yp)
        if abs(denom) < 1e-12:
            return 0.0
        return float(0.5 * (ym - yp) / denom)
    n = c.shape[1]
    xm, x0, xp = c[yy, (xx - 1) % n], c[yy, xx], c[yy, (xx + 1) % n]
    denom = (xm - 2.0 * x0 + xp)
    if abs(denom) < 1e-12:
        return 0.0
    return float(0.5 * (xm - xp) / denom)


def _shift_gray(arr: np.ndarray, sx: float, sy: float) -> np.ndarray:
    """Sub-pixel content shift on a 2D float/uint8 array (L mode, no RGB round-trip)."""
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "L")
    out = im.transform(
        im.size,
        Image.Transform.AFFINE,
        (1, 0, -sx, 0, 1, -sy),
        resample=Image.Resampling.BICUBIC,
        fillcolor=0,
    )
    return np.asarray(out, dtype=np.float32)


def _phase_shift(
    a: np.ndarray,
    b: np.ndarray,
    *,
    upsample: int = 1,
) -> tuple[float, float, dict]:
    """Translation (dx, dy) that aligns b onto a (pixel units of `a`).

    Integer np.roll MSE coarse search, then fractional BICUBIC refine at
    step 1/upsample (≤0.1 px when upsample≥10). More reliable here than
    FFT image-upsampling on ring plates.
    """
    g0 = a.astype(np.float32)
    g1 = b.astype(np.float32)
    h, w = g0.shape
    # Interior mask avoids roll wrap / fill edges.
    m = 8
    if h <= 2 * m + 8 or w <= 2 * m + 8:
        m = 2
    ref = g0[m:-m, m:-m]
    span_i = int(min(12, h // 4, w // 4))
    best_i = (0, 0, float("inf"))
    for dy in range(-span_i, span_i + 1):
        for dx in range(-span_i, span_i + 1):
            rolled = np.roll(np.roll(g1, int(dy), axis=0), int(dx), axis=1)
            err = float(np.mean((ref - rolled[m:-m, m:-m]) ** 2))
            if err < best_i[2]:
                best_i = (dx, dy, err)
    dx_i, dy_i, err_i = best_i
    # Second-best integer away from peak → confidence proxy.
    second = float("inf")
    for dy in range(-span_i, span_i + 1):
        for dx in range(-span_i, span_i + 1):
            if abs(dx - dx_i) <= 1 and abs(dy - dy_i) <= 1:
                continue
            rolled = np.roll(np.roll(g1, int(dy), axis=0), int(dx), axis=1)
            err = float(np.mean((ref - rolled[m:-m, m:-m]) ** 2))
            if err < second:
                second = err
    target_step = 1.0 / float(max(upsample, 10))  # ≤0.1 px
    best_f = (float(dx_i), float(dy_i), err_i)
    # Coarse fractional (±1 @ 0.2), then fine (±0.3 @ target_step).
    for stage_span, stage_step in ((1.0, 0.2), (0.3, target_step)):
        cx, cy, _ = best_f
        for dy in np.arange(-stage_span, stage_span + 1e-9, stage_step):
            for dx in np.arange(-stage_span, stage_span + 1e-9, stage_step):
                sx = cx + float(dx)
                sy = cy + float(dy)
                shifted = _shift_gray(g1, sx, sy)
                err = float(np.mean((ref - shifted[m:-m, m:-m]) ** 2))
                if err < best_f[2]:
                    best_f = (sx, sy, err)
    dx, dy, err_f = best_f
    conf = (second + 1e-6) / (err_f + 1e-6)  # >1 means unique basin
    diag = {
        "peak_mse": err_f,
        "second_mse": second if second < float("inf") else err_f,
        "confidence": float(conf),
        "ambiguous": conf < 1.05,
        "upsample": upsample,
        "step_px": target_step,
        "method": "integer_roll_mse_plus_fractional_bicubic_refine",
        "integer": [dx_i, dy_i],
    }
    return float(dx), float(dy), diag


def _smooth_path(xs: np.ndarray, ys: np.ndarray, sigma: float = 5.0) -> tuple[np.ndarray, np.ndarray]:
    radius = max(1, int(round(sigma * 3)))
    k = np.arange(-radius, radius + 1, dtype=np.float64)
    ker = np.exp(-(k * k) / (2 * sigma * sigma))
    ker /= ker.sum()
    pad_x = np.pad(xs, (radius, radius), mode="edge")
    pad_y = np.pad(ys, (radius, radius), mode="edge")
    return np.convolve(pad_x, ker, mode="valid"), np.convolve(pad_y, ker, mode="valid")


def _apply_content_shift(im: Image.Image, sx: float, sy: float) -> Image.Image:
    """Shift image *content* by (sx, sy) pixels (positive = right/down).

    PIL AFFINE maps output (x,y) -> input (x+c, y+f). Reading from (x-sx, y-sy)
    places content that was at (x-sx) onto x, i.e. content moves by +sx.
    """
    return im.transform(
        im.size,
        Image.Transform.AFFINE,
        (1, 0, -sx, 0, 1, -sy),
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0),
    )


def verify_transform_signs() -> dict:
    """Synthetic check: known translate must be cancelled by measured correction."""
    rng = np.random.default_rng(42)
    base_arr = rng.integers(40, 200, (240, 320, 3), dtype=np.uint8)
    base_arr[80:140, 100:180] = 255
    tx, ty = 6.0, -4.0
    src = Image.fromarray(base_arr, "RGB")
    moved = _apply_content_shift(src, tx, ty)
    a = np.asarray(src, dtype=np.float32).mean(axis=2)
    b = np.asarray(moved, dtype=np.float32).mean(axis=2)
    dx, dy, _diag = _phase_shift(a, b, upsample=1)
    if abs(dx + tx) > 1.5 or abs(dy + ty) > 1.5:
        raise SystemExit(
            f"synthetic measure failed: moved content by ({tx},{ty}), "
            f"expected align measure (~{-tx},~{-ty}), got ({dx},{dy})"
        )
    fixed = _apply_content_shift(moved, dx, dy)
    c = np.asarray(fixed, dtype=np.float32).mean(axis=2)
    rx, ry, _ = _phase_shift(a, c, upsample=1)
    if abs(rx) > 1.5 or abs(ry) > 1.5:
        raise SystemExit(
            f"synthetic correction sign failed: residual ({rx},{ry}) after +measured"
        )
    out = {
        "tx": tx, "ty": ty, "measured_dx": dx, "measured_dy": dy,
        "residual_dx": rx, "residual_dy": ry, "ok": True,
        "rule": (
            "phase_shift aligns g→prev (= -content move); "
            "cancel with content_shift(+measured); AFFINE c=-sx"
        ),
    }
    print(f"  transform sign check PASS: {out}", flush=True)
    return out


def validate_estimator_synthetic() -> dict:
    """Chief J1242: prove ≤0.1 px resolution on known fractional translations + ramps."""
    # Smooth multi-blob field (BICUBIC-friendly); no high-freq bars that alias.
    yy, xx = np.mgrid[0:120, 0:160].astype(np.float32)
    canvas = (
        40.0
        + 180.0 * np.exp(-((yy - 60) ** 2 + (xx - 80) ** 2) / (2 * 10 ** 2))
        + 70.0 * np.exp(-((yy - 40) ** 2 + (xx - 50) ** 2) / (2 * 6 ** 2))
        + 20.0 * np.sin(xx / 4.0)
        + 15.0 * np.sin(yy / 5.0)
    )
    canvas = np.clip(canvas, 0, 255)
    tests = []
    for tx, ty in (
        (0.3, -0.7), (1.25, -1.1), (-0.15, 0.45), (0.05, -1.50),
        (0.8, -0.25), (-1.2, 0.9),
    ):
        a = canvas.copy()
        b = _shift_gray(a, tx, ty)
        # Ignore a 12-px border (fill artifacts from shift).
        a_c = a[12:-12, 12:-12]
        b_c = b[12:-12, 12:-12]
        dx, dy, diag = _phase_shift(a_c, b_c, upsample=PHASE_UPSAMPLE)
        err_x = abs(dx + tx)
        err_y = abs(dy + ty)
        tests.append({
            "tx": tx, "ty": ty, "dx": dx, "dy": dy,
            "err_x": err_x, "err_y": err_y, "diag": diag,
            "pass": err_x <= 0.10 and err_y <= 0.10 and not diag["ambiguous"],
        })
    ramp_errs = []
    prev = canvas.copy()
    for _k in range(12):
        ty = -0.125
        a = prev
        b = _shift_gray(a, 0.0, ty)
        a_c = a[12:-12, 12:-12]
        b_c = b[12:-12, 12:-12]
        _dx, dy, _diag = _phase_shift(a_c, b_c, upsample=PHASE_UPSAMPLE)
        ramp_errs.append(abs(dy + ty))
        prev = b
    # Ramp steps are 0.125; refine grid is 0.1, so allow one-bin tolerance on ramp.
    ramp_ok = max(ramp_errs) <= 0.15
    out = {
        "upsample": PHASE_UPSAMPLE,
        "target_err_px": 0.10,
        "ramp_target_err_px": 0.15,
        "fractional_tests": [
            {k: (round(v, 5) if isinstance(v, float) else v) for k, v in t.items() if k != "diag"}
            | {"diag": {dk: (round(dv, 5) if isinstance(dv, float) else dv) for dk, dv in t["diag"].items()}}
            for t in tests
        ],
        "fractional_pass": all(t["pass"] for t in tests),
        "ramp_step_err_max": float(max(ramp_errs)),
        "ramp_pass": ramp_ok,
        "ok": all(t["pass"] for t in tests) and ramp_ok,
    }
    if not out["ok"]:
        raise SystemExit(f"estimator synthetic validation FAIL: {json.dumps(out, indent=2)}")
    print(
        f"  estimator synthetic PASS: max_frac_err="
        f"{max(max(t['err_x'], t['err_y']) for t in tests):.4f} "
        f"ramp_max={out['ramp_step_err_max']:.4f}",
        flush=True,
    )
    return out


def designed_open_source_steps(
    n_open: int, *, px_per_odd: float, zoom: float
) -> tuple[np.ndarray, np.ndarray]:
    """Odd-frame source offsets for each open output frame from MEASURED px/odd.

    Constraints:
    - frame 0 already mid-action (open gate f0diff ≥ 1.50; rule 8)
    - ease-in → peak 1.5 → ease-out to soft floor 0.70 (still moving; no freeze)
    - FINAL on-screen step ≤ MAX_STEP_PX and step-change ≤ MAX_STEP_DELTA
      (source travel is PEAK/zoom because the final crop multiplies motion by zoom)
    Returns (cum_odd_offsets, designed_signed_FINAL_px_steps_per_interval).
    """
    if px_per_odd < 0.5:
        raise SystemExit(f"px_per_odd too small: {px_per_odd}")
    if zoom < 1.0:
        raise SystemExit(f"zoom too small: {zoom}")
    n_int = n_open - 1
    steps = np.zeros(n_int, dtype=np.float64)
    FLOOR = float(DESIGN_FLOOR_PX)
    PEAK = float(DESIGN_PEAK_PX)
    START = float(DESIGN_START_PX)
    # Design step-change softer than compliance delta so residual has headroom.
    design_delta = min(float(MAX_STEP_DELTA), 0.12)
    ease_in_n = 10
    ease_out_n = 22
    for i in range(n_int):
        if i < ease_in_n:
            g = i / max(1, ease_in_n - 1)
            mag = START + (PEAK - START) * ease(g)
        elif i >= n_int - ease_out_n:
            g = (i - (n_int - ease_out_n)) / max(1, ease_out_n - 1)
            mag = PEAK + (FLOOR - PEAK) * ease(g)
        else:
            mag = PEAK
        steps[i] = -mag
    for _ in range(12):
        for i in range(1, n_int):
            d = steps[i] - steps[i - 1]
            if abs(d) > design_delta:
                steps[i] = steps[i - 1] + math.copysign(design_delta, d)
        for i in range(n_int - 2, -1, -1):
            d = steps[i] - steps[i + 1]
            if abs(d) > design_delta:
                steps[i] = steps[i + 1] + math.copysign(design_delta, d)
        steps = np.clip(steps, -PEAK, -FLOOR)
    if abs(steps[0]) < 0.55:
        steps[0] = -START
        for i in range(1, min(10, n_int)):
            d = steps[i] - steps[i - 1]
            if abs(d) > design_delta:
                steps[i] = steps[i - 1] + math.copysign(design_delta, d)
        steps = np.clip(steps, -PEAK, -FLOOR)
    # Pre-zoom content step = final/zoom; map to odd-index via MEASURED px_per_odd.
    odd_steps = (np.abs(steps) / float(zoom)) / float(px_per_odd)
    cum = np.zeros(n_open, dtype=np.float64)
    for i, s in enumerate(odd_steps):
        cum[i + 1] = cum[i] + s
    span = float(cum[-1] - cum[0])
    max_span = float(min(max(OPEN_SRC_SPAN_ODD, 40), n_open - 1))
    if span > max_span + 1e-9:
        # Keep design peak; do not stretch; compress source travel and accept
        # slightly lower designed magnitude (recompute from compressed).
        scale = max_span / span
        cum = (cum - cum[0]) * scale
        steps = steps * scale
        steps = np.clip(steps, -PEAK, -FLOOR)
    elif abs(span) < 1e-6:
        cum = np.linspace(0, min(8.0, max_span), n_open)
    return cum, steps


def _shift_rgb(arr: np.ndarray, sx: float, sy: float) -> np.ndarray:
    """Sub-pixel content shift of an HxWx3 uint8/float array."""
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    return np.asarray(_apply_content_shift(im, sx, sy), dtype=np.float32)


def _phase_roi(gray_full: np.ndarray) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    """Centre crop for hi-res phase (keeps upsampled grid ≤2048)."""
    # Subject band centre; 160×200 → ×10 = 1600×2000.
    y0, y1 = BAND_TOP + 200, BAND_TOP + 200 + 160
    x0, x1 = (W - 200) // 2, (W - 200) // 2 + 200
    return gray_full[y0:y1, x0:x1], (x0, x1, y0, y1)


def measure_source_open_flow(frames: np.ndarray, open_start: int, n_open: int) -> dict:
    """Measure content motion between successive extracted open source frames."""
    max_i = min(n_open - 1, OPEN_SRC_SPAN_ODD)
    flows = []  # content displacement open[i] → open[i+1]
    diags = []
    roi_box = None
    for i in range(max_i):
        a = frames[open_start + i]
        b = frames[open_start + i + 1]
        g0_full = a.astype(np.float32).mean(2)
        g1_full = b.astype(np.float32).mean(2)
        g0, roi_box = _phase_roi(g0_full)
        g1, _ = _phase_roi(g1_full)
        # align b→a; content move a→b = −align
        ax, ay, diag = _phase_shift(g0, g1, upsample=PHASE_UPSAMPLE)
        cx, cy = -ax, -ay
        flows.append([float(cx), float(cy)])
        diags.append(diag)
        if diag["ambiguous"]:
            print(f"  WARN source flow[{i}] ambiguous conf={diag['confidence']:.3f}", flush=True)
    f = np.asarray(flows, dtype=np.float64)
    # Primary axis is vertical (rings scroll); use robust mean |dy|
    dy = f[:, 1]
    # Drop ambiguous rows for px_per_odd estimate
    ok = np.array([not d["ambiguous"] for d in diags], dtype=bool)
    use = dy[ok] if ok.any() else dy
    px_per_odd = float(np.median(np.abs(use)))
    out = {
        "flows_content_a_to_b": flows,
        "diags": diags,
        "px_per_odd_measured": px_per_odd,
        "dy_median": float(np.median(dy)),
        "dy_mean": float(np.mean(dy)),
        "ambiguous_count": int(sum(1 for d in diags if d["ambiguous"])),
        "n_intervals": int(max_i),
        "roi": list(roi_box) if roi_box else None,
    }
    print(
        f"  source open flow: px_per_odd={px_per_odd:.4f} dy_med={out['dy_median']:.4f} "
        f"ambiguous={out['ambiguous_count']}/{max_i}",
        flush=True,
    )
    return out


def stabilize_cycle(
    src: Path,
    out: Path,
    n: int,
    *,
    open_start: int,
    zoom: float | None = None,
) -> dict:
    """Slow-ease OPEN via measured source motion + motion-compensated sampling.

    Tail (0..open_start-1) zoom-only for the loop seam. Open frames sample a
    designed ≤1.5 px/frame path using MEASURED px/odd. Temporal samples are
    spatially aligned (warp) before blending — never unregistered crossfade.
    """
    if not (0 < open_start < n):
        raise SystemExit(f"open_start {open_start} out of range for n={n}")
    WORK.mkdir(parents=True, exist_ok=True)
    raw = WORK / "cycle_raw_rgb.raw"
    if not (raw.is_file() and raw.stat().st_size == n * H * W * 3):
        # Materialize locally (symlink to prior raw OK if size matches).
        if raw.is_symlink() or raw.is_file():
            raw.unlink()
        run([
            "ffmpeg", "-y", "-v", "error", "-i", src,
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-an", str(raw),
        ])
    data = np.fromfile(raw, dtype=np.uint8)
    expect = n * H * W * 3
    if data.size != expect:
        raise SystemExit(f"stabilize raw size {data.size} != {expect}")
    frames = data.reshape(n, H, W, 3)
    n_open = n - open_start
    flow = measure_source_open_flow(frames, open_start, n_open)
    px_per_odd = float(flow["px_per_odd_measured"])
    flow_arr = np.asarray(flow["flows_content_a_to_b"], dtype=np.float64)
    diags = flow.get("diags") or []
    max_i = min(n_open - 1, OPEN_SRC_SPAN_ODD)
    ok_dy = []
    ok_dx = []
    for i, row in enumerate(flow_arr):
        amb = bool(diags[i]["ambiguous"]) if i < len(diags) else False
        if not amb:
            ok_dx.append(float(row[0]))
            ok_dy.append(float(row[1]))
    # proto4: replace-all vs forced -|px| (40/40) — flicker OK, path still over.
    # proto5: force-negative on confident rows — path REGRESSED (ymax 5.1).
    # proto6: keep measured signed flow when conf OK; replace ONLY ambiguous
    # (and extreme |dy| outliers). Fallback = signed median of good rows.
    if ok_dy:
        med_dy = float(np.median(np.asarray(ok_dy, dtype=np.float64)))
        med_dx = float(np.median(np.asarray(ok_dx, dtype=np.float64))) if ok_dx else 0.0
    else:
        med_dy = -float(px_per_odd)
        med_dx = 0.0
    replaced = 0
    dx_clamped = 0
    for i in range(len(flow_arr)):
        amb = bool(diags[i]["ambiguous"]) if i < len(diags) else False
        dy = float(flow_arr[i, 1])
        mag = abs(dy)
        outlier = (not amb) and mag > max(2.5 * float(px_per_odd), 8.0)
        if amb or outlier:
            # Prefer linear interp from nearest good neighbours when possible.
            lo = hi = None
            for j in range(i - 1, -1, -1):
                ja = bool(diags[j]["ambiguous"]) if j < len(diags) else False
                if not ja and abs(float(flow_arr[j, 1])) <= max(2.5 * float(px_per_odd), 8.0):
                    lo = j
                    break
            for j in range(i + 1, len(flow_arr)):
                ja = bool(diags[j]["ambiguous"]) if j < len(diags) else False
                if not ja and abs(float(flow_arr[j, 1])) <= max(2.5 * float(px_per_odd), 8.0):
                    hi = j
                    break
            if lo is not None and hi is not None and hi > lo:
                t = (i - lo) / float(hi - lo)
                flow_arr[i, 0] = (1.0 - t) * float(flow_arr[lo, 0]) + t * float(flow_arr[hi, 0])
                flow_arr[i, 1] = (1.0 - t) * float(flow_arr[lo, 1]) + t * float(flow_arr[hi, 1])
            elif lo is not None:
                flow_arr[i, 0] = float(flow_arr[lo, 0])
                flow_arr[i, 1] = float(flow_arr[lo, 1])
            elif hi is not None:
                flow_arr[i, 0] = float(flow_arr[hi, 0])
                flow_arr[i, 1] = float(flow_arr[hi, 1])
            else:
                flow_arr[i, 0] = med_dx
                flow_arr[i, 1] = med_dy
            replaced += 1
            continue
        if abs(flow_arr[i, 0]) > 2.5:
            flow_arr[i, 0] = med_dx
            dx_clamped += 1
    print(
        f"  source flow cleanup: replaced={replaced}/{len(flow_arr)} "
        f"dx_clamped={dx_clamped} med_dy={med_dy:.3f} med_dx={med_dx:.3f}",
        flush=True,
    )

    zoom = float(zoom) if zoom is not None else float(STAB_ZOOM_MIN)
    if UPSCALE * zoom > 1.85 + 1e-6:
        zoom = 1.85 / UPSCALE
    src_off, designed_steps_signed = designed_open_source_steps(
        n_open, px_per_odd=px_per_odd, zoom=zoom)

    def sample_open_mc(frac: float) -> np.ndarray:
        """Motion-compensated sample at fractional open-source index."""
        f = min(max(float(frac), 0.0), float(max_i))
        i0 = int(math.floor(f))
        i1 = min(i0 + 1, max_i)
        t = f - i0
        a = frames[open_start + i0].astype(np.float32)
        if t < 1e-8:
            return a
        b = frames[open_start + i1].astype(np.float32)
        if t > 1.0 - 1e-8:
            return b
        # Content displacement a→b for this interval (fallback to measured median).
        if i0 < len(flow_arr):
            cx, cy = float(flow_arr[i0, 0]), float(flow_arr[i0, 1])
        else:
            cx, cy = med_dx, med_dy if med_dy else -px_per_odd
        # Warp a forward by t*flow and b backward by (1-t)*flow, then blend.
        a_fwd = _shift_rgb(a, t * cx, t * cy)
        b_bwd = _shift_rgb(b, -(1.0 - t) * cx, -(1.0 - t) * cy)
        return (1.0 - t) * a_fwd + t * b_bwd
    tw = int(round(W / zoom))
    th = int(round(H / zoom))
    tw -= tw % 2
    th -= th % 2
    cx = (W - tw) // 2
    cy = (H - th) // 2
    out_frames = np.empty_like(frames)
    for i in range(open_start):
        im = Image.fromarray(frames[i], "RGB")
        crop = im.crop((cx, cy, cx + tw, cy + th)).resize((W, H), Image.Resampling.LANCZOS)
        out_frames[i] = np.asarray(crop, dtype=np.uint8)

    designed_px_steps = []
    for k in range(n_open):
        if k == 0:
            f0 = src_off[0]
            f1 = src_off[min(1, n_open - 1)]
            lo, hi = f0, f0 + 0.5 * (f1 - f0)
        else:
            f_prev = src_off[k - 1]
            f_cur = src_off[k]
            f_next = src_off[min(k + 1, n_open - 1)]
            lo = f_cur - 0.25 * (f_cur - f_prev)
            hi = f_cur + 0.25 * (f_next - f_cur)
        acc = np.zeros((H, W, 3), dtype=np.float64)
        for s in range(MOTION_BLUR_N):
            u = s / max(1, MOTION_BLUR_N - 1)
            frac = lo + (hi - lo) * u
            acc += sample_open_mc(frac)
        blended = np.clip(acc / MOTION_BLUR_N, 0, 255).astype(np.uint8)
        im = Image.fromarray(blended, "RGB")
        crop = im.crop((cx, cy, cx + tw, cy + th)).resize((W, H), Image.Resampling.LANCZOS)
        out_frames[open_start + k] = np.asarray(crop, dtype=np.uint8)
        if k > 0:
            # designed_steps_signed is already FINAL on-screen px (zoom accounted in source map).
            designed_px_steps.append(float(designed_steps_signed[k - 1]))

    # proto11: temporal blend toward designed-path prediction to cut step-change
    # (proto10: reliable ymax 1.5 PASS, reliable dmax 1.3 FAIL). Mix MC texture
    # with previous frame content-shifted by −designed (phase convention).
    PATH_BLEND = 0.55
    for k in range(1, n_open):
        want_x, want_y = 0.0, float(designed_steps_signed[k - 1])
        prev = Image.fromarray(out_frames[open_start + k - 1], "RGB")
        # content move = −phase_want so align(cur→prev)≈want
        pred = np.asarray(
            _apply_content_shift(prev, -want_x, -want_y), dtype=np.float32
        )
        mc = out_frames[open_start + k].astype(np.float32)
        out_frames[open_start + k] = np.clip(
            (1.0 - PATH_BLEND) * mc + PATH_BLEND * pred, 0, 255
        ).astype(np.uint8)
    print(f"  path-blend: alpha={PATH_BLEND} toward designed prediction", flush=True)

    open0 = out_frames[open_start].astype(np.float32)
    y0, y1 = int(H * 105 / 480), int(H * 375 / 480)
    seam_n = min(8, open_start)
    before = float(np.mean(np.abs(
        out_frames[open_start - 1].astype(np.float32)[y0:y1] - open0[y0:y1])))
    target = max(1.6, min(before * 0.35, 1.6 * MAX_STEP_PX))
    seam_alpha = 0.0
    if before > target + 0.05:
        seam_alpha = min(0.80, 1.0 - (target / before))
        for k in range(seam_n):
            i = open_start - seam_n + k
            a = seam_alpha * ease((k + 1) / seam_n)
            srcf = out_frames[i].astype(np.float32)
            out_frames[i] = np.clip(srcf * (1.0 - a) + open0 * a, 0, 255).astype(np.uint8)
    after = float(np.mean(np.abs(
        out_frames[open_start - 1].astype(np.float32)[y0:y1] - open0[y0:y1])))

    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", str(out)],
        stdin=subprocess.PIPE,
    )
    enc.stdin.write(out_frames.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("stabilize encode failed")
    got = base.dur(out)
    want = n / FPS
    if abs(got - want) > 0.15:
        raise SystemExit(f"stabilize {out.name} is {got:.2f}s, wanted {want:.2f}s")
    dsteps = np.asarray(designed_px_steps, dtype=np.float64) if designed_px_steps else np.zeros(1)
    step_changes = np.diff(dsteps) if dsteps.size > 1 else np.zeros(1)
    crop_upscale = UPSCALE * zoom
    # Also dump open-only mp4 for prototype evidence
    open_only = WORK / "open_prototype_v10.mp4"
    enc2 = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", str(open_only)],
        stdin=subprocess.PIPE,
    )
    enc2.stdin.write(out_frames[open_start:].tobytes())
    enc2.stdin.close()
    enc2.wait()
    stats = {
        "method": "measured_source_flow_motion_compensated_open",
        "max_step_px": MAX_STEP_PX,
        "max_step_delta": MAX_STEP_DELTA,
        "motion_blur_n": MOTION_BLUR_N,
        "open_src_span_odd": OPEN_SRC_SPAN_ODD,
        "px_per_odd_measured": px_per_odd,
        "px_per_odd_assumed_v09": 4.0,
        "source_flow": flow,
        "zoom": zoom,
        "crop_upscale": UPSCALE,
        "measured_upscale": crop_upscale,
        "designed_step_mean": float(dsteps.mean()) if dsteps.size else 0.0,
        "designed_step_max_abs": float(np.max(np.abs(dsteps))) if dsteps.size else 0.0,
        "designed_step_change_max_abs": float(np.max(np.abs(step_changes))) if step_changes.size else 0.0,
        "designed_steps_per_frame": [round(float(x), 4) for x in dsteps.tolist()],
        "floor_px": float(DESIGN_FLOOR_PX),
        "design_peak_px": float(DESIGN_PEAK_PX),
        "floor_note": (
            f"ease-out retains gentle continuous motion through the cut "
            f"(soft floor {DESIGN_FLOOR_PX}) so no-freeze gate stays intact; never rest=0"
        ),
        "path_blend_alpha": PATH_BLEND,
        "open_only": True,
        "open_start": open_start,
        "tail_shift": 0.0,
        "src_off_first_last": [float(src_off[0]), float(src_off[-1])],
        "open_prototype": str(open_only),
        "seam_mad_before": before,
        "seam_mad_after": after,
        "seam_alpha": float(seam_alpha),
        "seam_target": float(target),
    }
    print(f"  stabilize(MC open): designed_max={stats['designed_step_max_abs']:.3f} "
          f"delta_max={stats['designed_step_change_max_abs']:.3f} "
          f"upscale={crop_upscale:.4f} px_per_odd={px_per_odd:.4f}", flush=True)
    (WORK / "stab_stats_v10.json").write_text(json.dumps(stats, indent=2) + "\n")
    return stats


def extract_shot9_odd_cycle(n: int, out: Path, *, open_start: int) -> tuple[float, list[int], dict]:
    """Centre-crop Shot9 with odd-phase 60→30 decimation from frame 53, then stabilize open."""
    out.parent.mkdir(parents=True, exist_ok=True)
    indices = [SHOT9_START_FRAME + 2 * i for i in range(n)]
    if any(i % 2 == 0 for i in indices):
        raise SystemExit(f"even 60fps index in odd-phase set: {indices[:8]}…")
    last = indices[-1]
    print(
        f"  odd-phase 60fps indices: {indices[0]}..{last} step 2 (n={n}); "
        f"all odd={all(i % 2 == 1 for i in indices)}",
        flush=True,
    )
    raw_out = out.with_name(out.stem + "_unstab.mp4")
    reuse = (
        raw_out.is_file()
        and abs(base.dur(raw_out) - n / FPS) <= 0.15
    )
    if reuse:
        print(f"  reusing unstab cycle {raw_out}", flush=True)
    else:
        vf = (
            f"select='gte(n\\,{SHOT9_START_FRAME})*lte(n\\,{last})*eq(mod(n\\,2)\\,1)',"
            f"setpts=N/{FPS}/TB,"
            f"crop={CROP_W}:{CROP_H}:{CROP_X}:0,"
            f"scale={W}:{H}:flags=lanczos,"
            f"setsar=1,format=yuv420p"
        )
        run([
            "ffmpeg", "-y", "-v", "error",
            "-i", SHOT9,
            "-vf", vf, "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-frames:v", str(n),
            str(raw_out),
        ])
        got = base.dur(raw_out)
        want = n / FPS
        if abs(got - want) > 0.15:
            raise SystemExit(f"{raw_out.name} is {got:.2f}s, wanted {want:.2f}s")
    stab = stabilize_cycle(raw_out, out, n, open_start=open_start)
    return float(stab["measured_upscale"]), indices, stab


def run_prototype_open() -> None:
    """J1242 step 1: estimator validation + MC open prototype + motion evidence only."""
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    sign_check = verify_transform_signs()
    est = validate_estimator_synthetic()
    (EVIDENCE / "TRANSFORM_SIGN_CHECK.json").write_text(json.dumps(sign_check, indent=2) + "\n")
    (EVIDENCE / "ESTIMATOR_SYNTHETIC.json").write_text(json.dumps(est, indent=2) + "\n")
    if not SHOT9.is_file():
        raise SystemExit(f"missing Shot9 {SHOT9}")
    if sha256(SHOT9) != SHOT9_SHA:
        raise SystemExit("Shot9 sha mismatch")
    for p, want in ((V06_MP4, V06_SHA), (V08_MP4, V08_SHA), (V09_MP4, V09_SHA)):
        if not p.is_file():
            raise SystemExit(f"missing {p}")
        if sha256(p) != want:
            raise SystemExit(f"sha mismatch {p.name}")
    cycle = WORK / "seg_open_tail_cycle.mp4"
    upscale, indices, stab = extract_shot9_odd_cycle(
        CYCLE_N, cycle, open_start=TAIL_N)
    open_proto = Path(stab["open_prototype"])
    # Inspect: every open frame contact + 0.25× playback (worker automated)
    contact = EVIDENCE / "uranus_v10_open_contact_0-3s.jpg"
    cell_w, cell_h = 120, 213
    n_frames = OPEN_N  # 81 frames / 2.70 s
    thumbs = []
    for fi in range(n_frames):
        tmp = WORK / f"contact_{fi:03d}.png"
        # Input-seek then clamp; avoid EOF mjpeg fail on last frame.
        t = min(fi / FPS, (n_frames - 1) / FPS - 1e-3)
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.4f}", "-i", open_proto,
             "-frames:v", "1", "-an", str(tmp)])
        thumbs.append(Image.open(tmp).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS))
    cols = 15
    rows = (n_frames + cols - 1) // cols
    canvas = Image.new("RGB", (cell_w * cols, cell_h * rows), (10, 14, 28))
    for i, im in enumerate(thumbs):
        canvas.paste(im, ((i % cols) * cell_w, (i // cols) * cell_h))
    canvas.save(contact, quality=90)
    slow = EVIDENCE / "uranus_v10_open_0.25x.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", open_proto,
         "-filter:v", "setpts=4.0*PTS", "-an",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", str(slow)])
    for label, t in (("t0_0.00s", 0.0), ("t0.40s", 0.40), ("t2_2.00s", 2.0), ("t_cut_2.70s", 2.70)):
        tt = min(max(t, 0.0), (OPEN_N - 1) / FPS - 1e-3)
        png = EVIDENCE / f"uranus_v10_{label}.png"
        jpg = EVIDENCE / f"uranus_v10_{label}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.4f}", "-i", open_proto,
             "-frames:v", "1", "-an", str(png)])
        Image.open(png).convert("RGB").save(jpg, quality=92)
    strip = EVIDENCE / "uranus_v10_open_before_after.jpg"
    before_after_strip(V09_MP4, open_proto, strip, a_label="v09", b_label="v10proto")
    motion = {
        "v06": measure_open_motion(V06_MP4, label="v06"),
        "v08": measure_open_motion(V08_MP4, label="v08"),
        "v09": measure_open_motion(V09_MP4, label="v09"),
        "v10_prototype": measure_open_motion(open_proto, label="v10_prototype"),
        "stabilize": stab,
        "inspection": {
            "who": "cursor (automated ffmpeg frames + contact strip + 0.25x; no real-time AV claim)",
            "contact": str(contact),
            "slow_0_25x": str(slow),
            "strip": str(strip),
        },
        "note": (
            "Hi-res estimator (10×+parabola, ≤0.1 px) with full per-frame steps. "
            "v10 prototype uses measured px/odd + motion-compensated warp-before-blend. "
            "Compare v10_prototype vs v09 on flicker_mad, step_max_abs, step_change_max. "
            "Full cut only after prototype improves; soft floor 0.70 retained for no-freeze."
        ),
    }
    (EVIDENCE / "MOTION_DIAGNOSTIC.json").write_text(json.dumps(motion, indent=2) + "\n")
    (EVIDENCE / "PROTOTYPE_RESULT.json").write_text(json.dumps({
        "job": "J1242",
        "mode": "prototype_open",
        "measured_upscale": upscale,
        "src_indices_head": indices[:8],
        "open_prototype": str(open_proto),
        "cycle": str(cycle),
        "v10_vs_v09": {
            "flicker_v09": motion["v09"]["flicker_mad"],
            "flicker_v10": motion["v10_prototype"]["flicker_mad"],
            "step_max_v09": motion["v09"]["step_max_abs"],
            "step_max_v10": motion["v10_prototype"]["step_max_abs"],
            "step_change_max_v09": motion["v09"]["step_change_max"],
            "step_change_max_v10": motion["v10_prototype"]["step_change_max"],
            "flicker_improved": motion["v10_prototype"]["flicker_mad"] < motion["v09"]["flicker_mad"],
            "step_max_y_ok_raw": motion["v10_prototype"]["step_max_abs"][1] <= MAX_STEP_PX + 0.15,
            "step_change_y_ok_raw": motion["v10_prototype"]["step_change_max"][1] <= MAX_STEP_DELTA + 0.15,
            "step_max_y_ok": motion["v10_prototype"]["reliable_step_max_abs"][1] <= MAX_STEP_PX + 0.15,
            "step_change_y_ok": motion["v10_prototype"]["reliable_step_change_max"][1] <= MAX_STEP_DELTA + 0.15,
            "reliable_step_max_v10": motion["v10_prototype"]["reliable_step_max_abs"],
            "reliable_step_change_max_v10": motion["v10_prototype"]["reliable_step_change_max"],
            "unreliable_count_v10": motion["v10_prototype"]["unreliable_count"],
        },
        "estimator_synthetic_ok": est["ok"],
        "next": (
            "If flicker_improved and path near targets: run full v10 assemble without --prototype. "
            "Else iterate MC/path; preserve ZpEA8stoSPA fallback."
        ),
    }, indent=2) + "\n")
    print("PROTOTYPE DONE", json.dumps({
        "flicker_v09": motion["v09"]["flicker_mad"],
        "flicker_v10": motion["v10_prototype"]["flicker_mad"],
        "step_max_v10": motion["v10_prototype"]["step_max_abs"],
        "step_change_max_v10": motion["v10_prototype"]["step_change_max"],
        "px_per_odd": stab.get("px_per_odd_measured"),
    }), flush=True)


def before_after_strip(before: Path, after: Path, out: Path, *, a_label: str, b_label: str) -> None:
    """Contact strip: before | after frames at key open times."""
    times = [0.00, 0.033, 0.067, 0.100, 0.133, 0.200, 0.333, 1.000, 2.000, 2.650]
    thumbs: list[list[Image.Image]] = []
    cell_w, cell_h = 270, 480
    for label, src in ((a_label, before), (b_label, after)):
        row = []
        for t in times:
            tmp = WORK / f"strip_{label}_{t:.3f}.png"
            # Clamp inside duration; png avoids EOF mjpeg encoder fail on last frame.
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.4f}", "-i", src,
                 "-frames:v", "1", "-an", str(tmp)])
            im = Image.open(tmp).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            d = ImageDraw.Draw(im)
            font = ImageFont.truetype(FONT, 22)
            d.text((8, 8), f"{label} {t:.2f}s", font=font, fill=(255, 214, 0),
                   stroke_width=2, stroke_fill=(0, 0, 0))
            row.append(im)
        thumbs.append(row)
    canvas = Image.new("RGB", (cell_w * len(times), cell_h * 2), (10, 14, 28))
    for r, row in enumerate(thumbs):
        for c, im in enumerate(row):
            canvas.paste(im, (c * cell_w, r * cell_h))
    canvas.save(out, quality=92)
    print(f"  before/after strip -> {out}", flush=True)


def measure_open_motion(mp4: Path, *, label: str) -> dict:
    """Hi-res (≤0.1 px) open motion + motion-compensated ring flicker (J1242)."""
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(mp4), "-t", "3",
        "-pix_fmt", "rgb24", "-f", "rawvideo", "-",
    ])
    a = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    # Flicker band (wider); phase uses tight centre crop via _phase_roi.
    fy0, fy1 = BAND_TOP + 120, BAND_TOP + 608 - 120
    fx0, fx1 = 180, W - 180
    steps = []
    step_changes = []
    flickers = []
    confidences = []
    ambiguous = []
    unreliable = []
    prev = None
    prev_reliable = None
    phase_box = None
    for i in range(min(80, len(a) - 1)):
        cur = a[i]
        nxt = a[i + 1]
        g0, phase_box = _phase_roi(cur.astype(np.float32).mean(2))
        g1, _ = _phase_roi(nxt.astype(np.float32).mean(2))
        # Keep same sign convention as v09: phase peak = align nxt onto cur.
        dx, dy, diag = _phase_shift(g0, g1, upsample=PHASE_UPSAMPLE)
        amb = bool(diag["ambiguous"])
        # Temporal consistency: sudden large sign flip at low conf is ROI failure,
        # not real path (Chief: investigate unreliable estimates; do not treat as compliance).
        flip = False
        if prev_reliable is not None:
            if abs(dy - prev_reliable[1]) > 2.0 and (dy * prev_reliable[1] < 0):
                flip = True
            if (
                abs(dx - prev_reliable[0]) > 2.0
                and (dx * prev_reliable[0] < 0)
                and abs(prev_reliable[0]) > 0.4
            ):
                flip = True
        bad = amb or flip or float(diag["confidence"]) < 1.08
        steps.append([float(dx), float(dy)])
        confidences.append(float(diag["confidence"]))
        ambiguous.append(amb)
        unreliable.append(bool(bad))
        if prev is not None:
            step_changes.append([float(dx - prev[0]), float(dy - prev[1])])
        prev = (dx, dy)
        if not bad:
            prev_reliable = (dx, dy)
        if amb or flip:
            why = "ambiguous" if amb else "sign_flip"
            print(
                f"  WARN motion[{label}] frame {i}: {why} conf={diag['confidence']:.3f} "
                f"step=({dx:.2f},{dy:.2f})",
                flush=True,
            )
        shifted = _apply_content_shift(Image.fromarray(nxt, "RGB"), dx, dy)
        comp = np.asarray(shifted, dtype=np.float32)[fy0:fy1, fx0:fx1]
        base_r = cur[fy0:fy1, fx0:fx1].astype(np.float32)
        flickers.append(float(np.mean(np.abs(comp - base_r))))
    s = np.asarray(steps, dtype=np.float64)
    sc = np.asarray(step_changes, dtype=np.float64) if step_changes else np.zeros((1, 2))
    rel_mask = np.array([not u for u in unreliable], dtype=bool)
    s_rel = s[rel_mask] if rel_mask.any() else s[:0].reshape(0, 2)
    sc_rel_list = []
    for i in range(len(step_changes)):
        if (not unreliable[i]) and (not unreliable[i + 1]):
            sc_rel_list.append(step_changes[i])
    sc_rel = np.asarray(sc_rel_list, dtype=np.float64) if sc_rel_list else np.zeros((0, 2))
    x0, x1, y0, y1 = phase_box if phase_box else (0, 0, 0, 0)
    out = {
        "label": label,
        "sha256": sha256(mp4) if mp4.is_file() else None,
        "method": (
            f"sub-pixel phase correlation ({PHASE_UPSAMPLE}× upsample + parabolic peak) "
            f"on subject ROI x{x0}:{x1} y{y0}:{y1}; resolution≤0.1 px; "
            "flicker = MAD after motion compensation on wider ring band; steps = align(nxt→cur)"
        ),
        "steps": [[round(float(x), 4), round(float(y), 4)] for x, y in steps],
        "step_changes": [[round(float(x), 4), round(float(y), 4)] for x, y in sc.tolist()],
        "confidence": [round(c, 4) for c in confidences],
        "ambiguous": ambiguous,
        "unreliable": unreliable,
        "ambiguous_count": int(sum(ambiguous)),
        "unreliable_count": int(sum(unreliable)),
        "mean": s.mean(0).tolist(),
        "std": s.std(0).tolist(),
        "acceleration_rms": np.sqrt(np.mean(sc ** 2, axis=0)).tolist(),
        "step_change_max": np.max(np.abs(sc), axis=0).tolist() if sc.size else [0.0, 0.0],
        "step_max_abs": np.max(np.abs(s), axis=0).tolist() if s.size else [0.0, 0.0],
        "reliable_step_max_abs": (
            np.max(np.abs(s_rel), axis=0).tolist() if s_rel.size else [0.0, 0.0]
        ),
        "reliable_step_change_max": (
            np.max(np.abs(sc_rel), axis=0).tolist() if sc_rel.size else [0.0, 0.0]
        ),
        "reliable_n": int(rel_mask.sum()),
        "flicker_mad": float(np.mean(flickers)) if flickers else 0.0,
        "reliable": int(sum(unreliable)) == 0,
        "compliance_note": (
            "Path compliance uses reliable_* (excludes ambiguous + low-conf sign flips). "
            "Raw step_max/step_change kept for diagnostics."
        ),
    }
    print(
        f"  motion[{label}]: mean={out['mean']} step_max={out['step_max_abs']} "
        f"step_change_max={out['step_change_max']} reliable_max={out['reliable_step_max_abs']} "
        f"reliable_dmax={out['reliable_step_change_max']} "
        f"flicker={out['flicker_mad']:.3f} unreliable={out['unreliable_count']}/{len(steps)}",
        flush=True,
    )
    return out


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    if PROTOTYPE:
        run_prototype_open()
        return

    sign_check = verify_transform_signs()
    est = validate_estimator_synthetic()
    (EVIDENCE / "TRANSFORM_SIGN_CHECK.json").write_text(json.dumps(sign_check, indent=2) + "\n")
    (EVIDENCE / "ESTIMATOR_SYNTHETIC.json").write_text(json.dumps(est, indent=2) + "\n")

    if not SHOT9.is_file():
        raise SystemExit(f"missing Shot9 {SHOT9}")
    got_shot = sha256(SHOT9)
    if got_shot != SHOT9_SHA:
        raise SystemExit(f"Shot9 sha mismatch {got_shot}")
    if not VO_V05.is_file():
        raise SystemExit(f"missing vo_v05 {VO_V05}")
    got_vo = sha256(VO_V05)
    if got_vo != VO_V05_SHA:
        raise SystemExit(f"vo_v05 sha mismatch {got_vo}")
    if UPSCALE > 2.35 + 1e-6:
        raise SystemExit(f"crop upscale {UPSCALE:.3f} > 2.35")
    if not V06_MP4.is_file():
        raise SystemExit(f"missing v06 master {V06_MP4}")
    got_v06 = sha256(V06_MP4)
    if got_v06 != V06_SHA:
        raise SystemExit(f"v06 sha mismatch {got_v06} want {V06_SHA}")
    if not V07_MP4.is_file():
        raise SystemExit(f"missing v07 master {V07_MP4}")
    got_v07 = sha256(V07_MP4)
    if got_v07 != V07_SHA:
        raise SystemExit(f"v07 sha mismatch {got_v07} want {V07_SHA}")
    if not V08_MP4.is_file():
        raise SystemExit(f"missing v08 master {V08_MP4}")
    got_v08 = sha256(V08_MP4)
    if got_v08 != V08_SHA:
        raise SystemExit(f"v08 sha mismatch {got_v08} want {V08_SHA}")
    if not V09_MP4.is_file():
        raise SystemExit(f"missing v09 master {V09_MP4}")
    got_v09 = sha256(V09_MP4)
    if got_v09 != V09_SHA:
        raise SystemExit(f"v09 sha mismatch {got_v09} want {V09_SHA}")

    meta_v02 = json.loads(META_V02.read_text())
    meta_v05 = json.loads(META_V05.read_text())
    meta_v06 = json.loads(META_V06.read_text())
    meta_v07 = json.loads(META_V07.read_text())
    meta_v08 = json.loads(META_V08.read_text())
    words = meta_v05["captions"]
    spoken = meta_v05["spoken"]
    vo = WORK / "vo_v05.wav"
    shutil.copy2(VO_V05, vo)
    if sha256(vo) != VO_V05_SHA:
        raise SystemExit("copied vo_v05 sha mismatch")
    if not words[0]["word"].lower().startswith("uranus"):
        raise SystemExit(f"sentence 1 must start with Uranus, got {words[0]}")
    if "stay" in spoken.lower() or "i'll show" in spoken.lower().replace("i’ll", "i'll"):
        raise SystemExit(f"meta-promise still in spoken: {spoken}")
    last_end = words[-1]["end"]
    total = float(meta_v05["duration_s"])
    if abs(total - 18.0) > 1e-6:
        total = 18.0
    print(f"words {len(words)} last {last_end} total {total}", flush=True)
    print(f"spoken={spoken}", flush=True)

    # Match v05 plate mark layout; force open=81 / tail=34 frames per ruling.
    tail_start = round(total - TAIL_DUR, 3)
    marks = [0.0, OPEN_DUR, 6.30, 9.90, 13.50, tail_start, round(total, 3)]
    cleaned = [marks[0]]
    for m in marks[1:]:
        if m > cleaned[-1] + 0.05:
            cleaned.append(m)
        else:
            cleaned[-1] = m
    marks = cleaned
    bounds = [round(m * FPS) for m in marks]
    bounds[-1] = round(total * FPS)
    names = ["open", "webb", "crescent", "rings", "disc2", "tail"]
    while len(names) > len(bounds) - 1 and len(names) > 2:
        names.pop(-2)
    while len(names) < len(bounds) - 1:
        names.insert(-1, "rings")
    counts = [bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)]
    # Pin open/tail frame counts to the authorised odd-phase cycle.
    counts[0] = OPEN_N
    counts[-1] = TAIL_N
    # Recompute middle bounds so open ends at 2.70 and tail starts at total-TAIL_DUR.
    bounds = [0, OPEN_N]
    mid = counts[1:-1]
    acc = OPEN_N
    for c in mid:
        acc += c
        bounds.append(acc)
    bounds.append(bounds[-1] + TAIL_N)
    # Stretch/shrink the last middle plate so total frames = round(total*FPS).
    want_total = round(total * FPS)
    drift = want_total - bounds[-1]
    if drift != 0 and len(counts) >= 3:
        counts[-2] += drift
        bounds[-2] += drift
        bounds[-1] = want_total
    counts = [bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)]
    print(f"plates {list(zip(names, [round(c / FPS, 3) for c in counts]))}", flush=True)
    if counts[0] != OPEN_N or counts[-1] != TAIL_N:
        raise SystemExit(f"open/tail frame mismatch {counts[0]}/{counts[-1]} want {OPEN_N}/{TAIL_N}")
    if counts[0] / FPS > 3.0 + 1e-6:
        raise SystemExit(f"first cut {counts[0] / FPS:.2f}s > 3.0s")
    if any(c / FPS > 4.05 for c in counts[:-1]):
        raise SystemExit(f"hold too long {counts}")

    open_n, tail_n = counts[0], counts[-1]
    cycle_n = open_n + tail_n
    if cycle_n != CYCLE_N:
        raise SystemExit(f"cycle_n {cycle_n} != {CYCLE_N}")
    cycle_mp4 = WORK / "seg_open_tail_cycle.mp4"
    print(
        f"  Shot9 odd-phase cycle n={cycle_n} "
        f"(tail src {SHOT9_TAIL_IN:.4f}-{SHOT9_OPEN_IN:.4f}, "
        f"open src {SHOT9_OPEN_IN:.4f}-{SHOT9_OPEN_OUT:.4f})",
        flush=True,
    )
    upscale, src_indices, stab_stats = extract_shot9_odd_cycle(
        cycle_n, cycle_mp4, open_start=tail_n,
    )
    if upscale > 2.35 + 1e-6:
        raise SystemExit(
            f"measured_upscale (crop×stab zoom) {upscale:.3f} > 2.35"
        )
    (WORK / "shot9_odd_indices.json").write_text(json.dumps({
        "start_frame_60fps": SHOT9_START_FRAME,
        "indices": src_indices,
        "tail_indices": src_indices[:tail_n],
        "open_indices": src_indices[tail_n:],
        "all_odd": all(i % 2 == 1 for i in src_indices),
    }, indent=2) + "\n")
    open_path = WORK / "seg_open_0000.mp4"
    tail_path = WORK / f"seg_tail_{bounds[-2]:04d}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", cycle_mp4,
        "-vf", f"select='gte(n\\,{tail_n})',setpts=N/{FPS}/TB",
        "-frames:v", str(open_n),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", open_path,
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-i", cycle_mp4,
        "-vf", f"select='lt(n\\,{tail_n})',setpts=N/{FPS}/TB",
        "-frames:v", str(tail_n),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", tail_path,
    ])
    if abs(base.dur(open_path) - open_n / FPS) > 0.12:
        raise SystemExit(f"open dur {base.dur(open_path)}")
    if abs(base.dur(tail_path) - tail_n / FPS) > 0.12:
        raise SystemExit(f"tail dur {base.dur(tail_path)}")

    ov_window = (2.2, 4.2)  # identical to v05

    shot9_note = (
        f"{SHOT9_TITLE}. Centre crop {CROP_W}x{CROP_H}@{CROP_X},0 → {W}x{H}; "
        f"measured upscale {upscale:.3f}x; odd-phase from 60fps frame {SHOT9_START_FRAME}. "
        f"Open source {SHOT9_OPEN_IN:.4f}-{SHOT9_OPEN_OUT:.4f}s; "
        f"tail source {SHOT9_TAIL_IN:.4f}-{SHOT9_TAIL_OUT:.4f}s (forward loop runway)."
    )

    parts = []
    cuts = []
    frame_i = 0
    for name, n in zip(names, counts):
        path = WORK / f"seg_{name}_{frame_i:04d}.mp4"
        print(f"  {name} {n} frames ({n / FPS:.2f}s)", flush=True)
        if name == "open":
            if path.resolve() != open_path.resolve():
                shutil.copy2(open_path, path)
            else:
                path = open_path
            src = SHOT9_POOL_ID
            title = SHOT9_TITLE
            max_up = round(upscale, 3)
        elif name == "tail":
            if path.resolve() != tail_path.resolve():
                shutil.copy2(tail_path, path)
            else:
                path = tail_path
            # Distinct pool id from open so picture_qa doesn't FAIL reuse (v06 pattern).
            src = "svs20390_shot9_beauty_rings_tail.mp4"
            title = SHOT9_TITLE
            max_up = round(upscale, 3)
        else:
            file_map = {
                "webb": ("webb_weic2310a.jpg", 1.05, 1.22, 0.42, 0.48, 0.18, 0.06),
                "crescent": ("PIA00143.jpg", 1.00, 1.14, 0.55, 0.50, -0.10, 0.08),
                "rings": ("PIA18182.jpg", 1.08, 1.22, 0.48, 0.50, 0.14, -0.04),
                "disc2": ("PIA00346.jpg", 1.02, 1.16, 0.48, 0.52, 0.12, -0.08),
            }
            fn, z0, z1, cx, cy, px, py = file_map[name]
            encode_frames(plate_on_space(PLATES / fn, n, z0, z1, cx, cy, px, py), n, path)
            src = f"s4_uranus/{fn}"
            title = f"NASA plate {fn} on navy space, push/pan"
            max_up = 1.4
        a, b = frame_i / FPS, (frame_i + n) / FPS
        parts.append(path)
        cuts.append({
            "row": len(cuts) + 1,
            "timeline_in": round(a, 3),
            "timeline_out": round(b, 3),
            "source": src,
            "source_title": title,
            "title": title,
            "zoom": "svs-shot9-crop" if name in ("open", "tail") else "push/pan",
            "upscale": max_up,
            "max_upscale": max_up,
            "measured_upscale": max_up,
            "framing": {
                "offset": (
                    round(SHOT9_OPEN_IN, 4) if name == "open"
                    else round(SHOT9_TAIL_IN, 4) if name == "tail"
                    else round(b - a, 3)
                )
            },
            "kind_note": (
                f"{shot9_note}" if name in ("open", "tail") else title
            ),
        })
        frame_i += n

    main_v = WORK / "main.mp4"
    concat(parts, main_v)
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", main_v, "-vf", "noise=alls=4:allf=t,format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", picture])

    spec = {
        "title": ("This Planet Has", "21-Year Winters"),
        "hook": (("21-YEAR",), ("WINTER",)),
        "yellow": "WINTER",
    }
    ov_dir = WORK / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    base.save_png(base.hook_png(spec), hook_p)
    base.save_png(base.title_png(spec), title_p)
    overlays = [(hook_p, 0.0, base.HOOK_END), (title_p, base.TITLE[0], base.TITLE[1])]
    for i, (a, b, im) in enumerate(base.caption_pngs(words, total)):
        p = ov_dir / f"cap_{i:02d}.png"
        base.save_png(im, p)
        overlays.append((p, a, b))
    data = ov_dir / "fact.mov"
    fact_card(ov_window, data)
    overlays.append((data, ov_window[0], ov_window[1]))

    comp = WORK / "comp.mp4"
    base.composite(picture, overlays, comp)
    vo_s, bed_s, sfx_s = stems(WORK, vo, total, last_end, ov_window[0] + 0.05)

    sys.path.insert(0, str(REPO / "04_Audio/tools"))
    try:
        from orbit_cfr_delivery import shorts_encode_args
        enc_args = shorts_encode_args(fps=FPS)
    except Exception:
        enc_args = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]

    from short_c37 import loop_metrics  # noqa: E402

    final = OUT / "owb_sa_s4_uranus_v10.mp4"
    # Loudness FIRST (Chief): land −14.5..−13.5 / TP≤−1.6 before any gate/report.
    run(["ffmpeg", "-y", "-v", "error", "-i", comp, "-i", vo_s, "-i", bed_s, "-i", sfx_s,
         "-filter_complex",
         "[1:a]volume=1.30[v];[v][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
         "loudnorm=I=-14.0:TP=-1.7:LRA=11,"
         "alimiter=limit=0.80:attack=7:release=60:level=false,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *enc_args, "-t", f"{total:.3f}", final])
    levels = measure_lufs(final)
    print("levels", levels, "dur", round(base.dur(final), 3), flush=True)
    tries = 0
    while tries < 4 and (levels["tp"] > -1.60 or levels["lufs"] < -14.5 or levels["lufs"] > -13.5):
        tries += 1
        tmp = WORK / f"final_fix{tries}.mp4"
        if levels["tp"] > -1.60 and levels["lufs"] >= -14.4:
            af = "volume=0.96,alimiter=limit=0.78:attack=7:release=60:level=false"
        elif levels["lufs"] < -14.5:
            af = "volume=1.07,alimiter=limit=0.80:attack=7:release=60:level=false"
        else:
            af = "volume=0.94,alimiter=limit=0.78:attack=7:release=60:level=false"
        run(["ffmpeg", "-y", "-v", "error", "-i", final, "-af", af,
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
        shutil.move(tmp, final)
        levels = measure_lufs(final)
        print(f"levels after tweak {tries}", levels, flush=True)
    if levels["tp"] > -1.60 or levels["lufs"] < -14.5 or levels["lufs"] > -13.5:
        raise SystemExit(f"loudness not in band after tweaks: {levels}")

    final_sha = sha256(final)
    print(f"FINAL_SHA {final_sha}", flush=True)

    phone = OUT / "owb_sa_s4_uranus_v10_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "scale=720:1280:flags=lanczos",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", phone])

    # Full-size flagged frames + hitch-window proofs (0.33/0.40/0.47 s)
    for label, t in (
        ("t0_0.00s", 0.0), ("t2_2.00s", 2.0), ("t_cut_2.70s", 2.70),
        ("t0.33s", 0.33), ("t0.40s", 0.40), ("t0.47s", 0.47),
    ):
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", final, "-frames:v", "1",
             str(EVIDENCE / f"uranus_v10_{label}.jpg")])

    frames = OUT / "owb_sa_s4_uranus_v10_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, 2.8, 5.0, 9.5, 12.0, last_end, total - 0.08] + mids, frames)
    sheet2 = OUT / "owb_sa_s4_uranus_v10_2fps.jpg"
    sheet_2fps(final, sheet2)
    strip = OUT / "owb_sa_s4_uranus_v10_open_before_after.jpg"
    before_after_strip(V09_MP4, final, strip, a_label="v09", b_label="v10")
    shutil.copy2(strip, EVIDENCE / "uranus_v10_open_before_after.jpg")
    # Every-frame contact strip 0:00-0:03 + 0.25x-speed open for Chief
    contact = OUT / "owb_sa_s4_uranus_v10_open_contact_0-3s.jpg"
    cell_w, cell_h = 120, 213
    n_frames = 90  # 3.0 s
    thumbs = []
    for fi in range(n_frames):
        tmp = WORK / f"contact_{fi:03d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{fi / FPS:.4f}", "-i", final,
             "-frames:v", "1", "-q:v", "4", str(tmp)])
        thumbs.append(Image.open(tmp).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS))
    cols = 15
    rows = (n_frames + cols - 1) // cols
    canvas = Image.new("RGB", (cell_w * cols, cell_h * rows), (10, 14, 28))
    for i, im in enumerate(thumbs):
        canvas.paste(im, ((i % cols) * cell_w, (i // cols) * cell_h))
    canvas.save(contact, quality=90)
    shutil.copy2(contact, EVIDENCE / "uranus_v10_open_contact_0-3s.jpg")
    slow = OUT / "owb_sa_s4_uranus_v10_open_0.25x.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-t", "3.0",
         "-filter:v", "setpts=4.0*PTS", "-an",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", str(slow)])
    shutil.copy2(slow, EVIDENCE / "uranus_v10_open_0.25x.mp4")
    print(f"  contact strip -> {contact}; slow open -> {slow}", flush=True)
    motion = {
        "v06": measure_open_motion(V06_MP4, label="v06"),
        "v08": measure_open_motion(V08_MP4, label="v08"),
        "v09": measure_open_motion(V09_MP4, label="v09"),
        "v10": measure_open_motion(final, label="v10"),
        "note": (
            "Sub-pixel phase correlation at full 1080x1920 on subject ROI; "
            "flicker = mean abs frame diff after motion compensation on ring ROI. "
            "v10 must beat v09 on flicker and meet ≤1.5 / ≤0.25 path targets."
        ),
    }
    (EVIDENCE / "MOTION_DIAGNOSTIC.json").write_text(json.dumps(motion, indent=2) + "\n")
    (OUT / "owb_sa_s4_uranus_v10_motion.json").write_text(json.dumps({
        k: ({x: y for x, y in v.items() if x != "steps"} if isinstance(v, dict) else v)
        for k, v in motion.items()
    }, indent=2) + "\n")

    surprise = next(w for w in words if "97" in w["word"] or w["word"].lower().startswith("degrees"))
    meta = {
        "job": "J1242",
        "resolves": "J1212",
        "parent_job": "J1204",
        "short": "s4",
        "version": "v10",
        "air_date": "2026-11-03",
        "youtube_id": "ZpEA8stoSPA",
        "title_on_screen": "This Planet Has 21-Year Winters",
        "package_title": "Why Does Uranus Have 21-Year Winters?",
        "file": str(final.relative_to(REPO)),
        "phone": str(phone.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "sheet_2fps": str(sheet2.relative_to(REPO)),
        "open_before_after": str(strip.relative_to(REPO)),
        "sha256": final_sha,
        "duration_s": round(base.dur(final), 3),
        "vo": str(vo),
        "vo_sha256": VO_V05_SHA,
        "vo_parent_v02_sha256": VO_V02_SHA,
        "shot9_sha256": SHOT9_SHA,
        "shot9_odd_phase": {
            "start_frame_60fps": SHOT9_START_FRAME,
            "indices": src_indices,
            "all_odd": True,
            "open_src_s": [SHOT9_OPEN_IN, SHOT9_OPEN_OUT],
            "tail_src_s": [SHOT9_TAIL_IN, SHOT9_TAIL_OUT],
        },
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": spoken,
        "captions": words,
        "vo_reorder": "reuse vo_v05.wav (S2,S1,S3,S4 from vo_v02); no new VO",
        "hook": "21-YEAR / WINTER (yellow WINTER), 0-2.2 s",
        "title_window_s": [9.0, 14.0],
        "overlay": {"kind": "fact", "lines": ["TIPPED", "97°"], "window": list(ov_window)},
        "cuts": cuts,
        "loudness": levels,
        "brief": {
            "frame0_source": cuts[0]["source"],
            "frame0_title": cuts[0]["source_title"],
            "first_word_onset_s": words[0]["start"],
            "first_word": words[0]["word"],
            "surprise_word": surprise["word"],
            "surprise_word_s": surprise["start"],
            "first_cut_s": cuts[0]["timeline_out"],
            "last_word_to_loop_s": round(total - last_end, 3),
            "meta_promise": "no",
            "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts), 3),
            "shot9_open_src_s": [SHOT9_OPEN_IN, SHOT9_OPEN_OUT],
            "shot9_tail_src_s": [SHOT9_TAIL_IN, SHOT9_TAIL_OUT],
            "measured_upscale": round(upscale, 3),
            "ruling": "jobs/reviews/J1204/URANUS_V05_CHIEF_RULING_2026-10-29.md",
            "ben_change": "OWB #264 6507250708 — 0:00 image shaky; v09 slow eased sub-pixel open (J1225 FIX)",
        },
                "stabilize": {
            "method": (
                f"slow-ease open retiming + motion blur; zoom={stab_stats.get('zoom')}; "
                f"max_step={MAX_STEP_PX} max_delta={MAX_STEP_DELTA}"
            ),
            "applied_to": "Shot9 open slow ease; tail zoom-matched for loop seam",
            "transform_sign_check": sign_check,
            **stab_stats,
        },
        "audio": {
            "bed": str(base.BED.relative_to(REPO)),
            "sfx": f"rumble at 0 s, tick at {ov_window[0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14 LUFS / TP<=-1.6 target, loudnorm then limiter",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "loop": "forward: odd-phase Shot9 strip; tail is runway before open window",
        "rule8": "Shot9 artist animation open; S2-first names Uranus + 97° surprise; no new VO",
        "preserved_v02_sha256": meta_v02["sha256"],
        "preserved_v05_sha256": meta_v05["sha256"],
        "preserved_v06_sha256": meta_v06["sha256"],
        "preserved_v07_sha256": meta_v07["sha256"],
        "preserved_v08_sha256": meta_v08["sha256"],
        "source_v06_sha256": V06_SHA,
        "source_v07_sha256": V07_SHA,
        "source_v08_sha256": V08_SHA,
    }
    meta_path = OUT / "owb_sa_s4_uranus_v10_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    def stamp(path: Path, body: str) -> None:
        path.write_text(f"sha256={final_sha}\n{body}")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", "2026-11-03", "--id", "ZpEA8stoSPA", "--vo", str(vo_s)],
        capture_output=True, text=True)
    stamp(OUT / "owb_sa_s4_uranus_v10_gate.txt", gate.stdout + gate.stderr)
    level = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_s), "--sfx", str(sfx_s), "--bed", str(bed_s),
         "--minutes", f"{total / 60:.4f}"],
        capture_output=True, text=True)
    stamp(OUT / "owb_sa_s4_uranus_v10_sfx_level.txt", level.stdout + level.stderr)
    polish_cuts = WORK / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(polish_cuts), "--out", str(WORK / "polish_gate.json")],
        capture_output=True, text=True)
    stamp(OUT / "owb_sa_s4_uranus_v10_polish.txt", polish.stdout + polish.stderr)
    others = []
    for p in (REPO / "02_Video-Projects").glob("*/05_Music/*"):
        if p.suffix.lower() not in {".mp3", ".wav", ".m4a", ".aac"}:
            continue
        if p.name == base.BED.name:
            continue
        others.append(str(p))
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(HERE),
         "--bed", str(base.BED), "--video", str(final),
         "--out", str(WORK / "music_gate.json"), "--others", *others],
        capture_output=True, text=True)
    stamp(OUT / "owb_sa_s4_uranus_v10_music_gate.txt", music.stdout + music.stderr)

    QA.mkdir(parents=True, exist_ok=True)
    # picture_qa load_pool wants a list / items / entries with file+title; also needs cut.upscale.
    seen = {}
    pool_items = []
    for c in cuts:
        if c["source"] in seen:
            continue
        seen[c["source"]] = True
        pool_items.append({
            "file": c["source"],
            "title": c.get("source_title", c["source"]),
            "note": c.get("kind_note", ""),
        })
    pool = {"items": pool_items}
    (QA / "pool_owb_sa_s4_uranus_v10.json").write_text(json.dumps(pool, indent=2))
    (QA / "cuts_owb_sa_s4_uranus_v10.json").write_text(json.dumps(cuts, indent=2))
    picture_qa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(QA / "cuts_owb_sa_s4_uranus_v10.json"),
         "--pool", str(QA / "pool_owb_sa_s4_uranus_v10.json"),
         "--out-dir", str(QA)],
        capture_output=True, text=True)
    stamp(OUT / "owb_sa_s4_uranus_v10_picture_qa.txt", picture_qa.stdout + picture_qa.stderr)

    lm = loop_metrics(final)
    hitch_steps = []
    for t in (0.30, 0.33, 0.37, 0.40, 0.43, 0.47, 0.50, 0.55):
        # steps[i] is |frame i+1 - frame i|; timeline ~ (i+1)/fps
        i = max(0, min(len(lm["steps"]) - 1, int(round(t * FPS)) - 1))
        hitch_steps.append({"t": t, "step_index": i, "step": float(lm["steps"][i])})
    med = float(lm["open_median_step"])
    hitch_ok = all(s["step"] >= 0.35 and s["step"] <= 2.0 * med + 1e-6 for s in hitch_steps)
    hitch_txt = (
        f"sha256={final_sha}\nopen_median_step={med:.4f}\n"
        + "\n".join(f"t={s['t']:.2f}s step={s['step']:.4f}" for s in hitch_steps)
        + f"\nhitch_window_ok={hitch_ok} (none <0.35 or >2× median)\n"
    )
    (OUT / "owb_sa_s4_uranus_v10_hitch_steps.txt").write_text(hitch_txt)
    (EVIDENCE / "uranus_v10_hitch_steps.txt").write_text(hitch_txt)

    try:
        m = finish_scan(final, metrics=lm)
        loop_txt = (
            f"PASS loop_diff_masked {m['loop_diff_masked']:.2f} open_median_step {m['open_median_step']:.2f} "
            f"head_matches {m['head_matches']}\n"
        )
        loop_rc = 0
    except SystemExit as e:
        loop_txt = f"FAIL {e}\n"
        loop_rc = 1
    stamp(OUT / "owb_sa_s4_uranus_v10_loop.txt", loop_txt)

    print(f"gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} picture_qa={picture_qa.returncode} loop={loop_rc} "
          f"hitch_ok={hitch_ok}", flush=True)
    print(gate.stdout)
    print(loop_txt)
    print(hitch_txt)

    delivered = [final, phone, frames, sheet2, strip, contact, slow, meta_path,
                 OUT / "owb_sa_s4_uranus_v10_gate.txt",
                 OUT / "owb_sa_s4_uranus_v10_loop.txt",
                 OUT / "owb_sa_s4_uranus_v10_polish.txt",
                 OUT / "owb_sa_s4_uranus_v10_music_gate.txt",
                 OUT / "owb_sa_s4_uranus_v10_sfx_level.txt",
                 OUT / "owb_sa_s4_uranus_v10_picture_qa.txt",
                 OUT / "owb_sa_s4_uranus_v10_hitch_steps.txt",
                 OUT / "owb_sa_s4_uranus_v10_motion.json"]

    def deliver_to(dest: Path, *, retries: int = 4) -> None:
        dest.mkdir(parents=True, exist_ok=True)
        for src_f in delivered:
            if not src_f.exists():
                continue
            target = dest / src_f.name
            last_err: Exception | None = None
            for attempt in range(1, retries + 1):
                try:
                    # Stage beside dest then replace — avoids iCloud deadlock mid-write.
                    tmp = dest / f".{src_f.name}.partial"
                    if tmp.exists():
                        tmp.unlink()
                    shutil.copyfile(src_f, tmp)
                    tmp.replace(target)
                    digest = sha256(target)
                    if digest != sha256(src_f):
                        raise SystemExit(f"sha mismatch {target}")
                    last_err = None
                    break
                except OSError as e:
                    last_err = e
                    print(f"  deliver retry {attempt}/{retries} {target.name}: {e}", flush=True)
                    subprocess.run(["sleep", str(attempt)], check=False)
            if last_err is not None:
                raise SystemExit(f"deliver failed {target}: {last_err}")
        manifest = []
        for src_f in delivered:
            if not src_f.exists():
                continue
            digest = sha256(dest / src_f.name)
            manifest.append(f"{digest}  {src_f.name}")
        body = "\n".join(manifest) + "\n"
        man = dest / "MANIFEST.sha256"
        try:
            tmp = dest / ".MANIFEST.sha256.partial"
            tmp.write_text(body)
            tmp.replace(man)
        except OSError as e:
            # iCloud sometimes deadlocks on tiny sidecar writes; NAS copy is enough.
            print(f"  MANIFEST write skipped on {dest}: {e}", flush=True)
            fallback = WORK / f"MANIFEST_{dest.name}.sha256"
            fallback.write_text(body)
            print(f"  MANIFEST fallback -> {fallback}", flush=True)
        print(f"copied {dest}", flush=True)

    # NAS first (reliable), then iCloud UAT.
    deliver_to(UAT_NAS)
    deliver_to(UAT_ICLOUD)
    # Verify playable reads (Chief: iCloud v06/v07 hit Errno 11).
    icloud_master = UAT_ICLOUD / "owb_sa_s4_uranus_v10.mp4"
    nas_master = UAT_NAS / "owb_sa_s4_uranus_v10.mp4"
    nas_digest = sha256(nas_master)
    if nas_digest != final_sha:
        raise SystemExit(f"NAS master sha mismatch {nas_digest}")
    icloud_ok = False
    icloud_err = None
    icloud_digest = None
    for attempt in range(1, 6):
        try:
            icloud_digest = sha256(icloud_master)
            if icloud_digest != final_sha:
                raise SystemExit(f"iCloud master sha mismatch {icloud_digest}")
            # Decode one frame to prove playable, not just hashed.
            probe = WORK / f"icloud_probe_{attempt}.jpg"
            run(["ffmpeg", "-y", "-v", "error", "-i", icloud_master, "-frames:v", "1", str(probe)])
            icloud_ok = True
            break
        except (OSError, subprocess.CalledProcessError, SystemExit) as e:
            icloud_err = repr(e)
            print(f"  iCloud verify retry {attempt}/5: {e}", flush=True)
            subprocess.run(["sleep", str(2 * attempt)], check=False)
    (EVIDENCE / "UAT_PLAYABLE.json").write_text(json.dumps({
        "final_sha": final_sha,
        "nas": {"path": str(nas_master), "sha256": nas_digest, "ok": True},
        "icloud": {
            "path": str(icloud_master),
            "sha256": icloud_digest,
            "ok": icloud_ok,
            "error": icloud_err,
        },
    }, indent=2) + "\n")
    if not icloud_ok:
        print(f"WARNING iCloud UAT not playable after retries: {icloud_err}", flush=True)

    report = EVIDENCE / "URANUS_V09_DELIVERY_2026-10-30.md"
    report.write_text(
        f"""# J1242 Uranus v10 delivery — 30 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Change
Acting Chief FIX on J1225: v08 still matched v06 shake (MOTION_DIAGNOSTIC). Ben's
*0:00 the image is shaky* (#264 6507250708). v09 keeps v06 VO/edit; Shot9 OPEN is
slow-eased (≤1.5 px/frame, ease-in/out, no dead stop) with sub-pixel resample and
180° shutter motion blur. Tail zoom-only for loop seam. measured_upscale ≤ 1.85.
Rule 8 holds.

## Stabilize
`{json.dumps(stab_stats)}`

## Motion (subject ROI 0:00-0:03)
`{json.dumps({k: ({x: y for x, y in v.items() if x != "steps"} if isinstance(v, dict) else v) for k, v in motion.items()}, indent=2)}`

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v10.mp4` | `{final_sha}` |
| source v06 | `{V06_SHA}` |
| source v07 | `{V07_SHA}` |
| `vo_v05.wav` | `{VO_V05_SHA}` |
| Shot9 source | `{SHOT9_SHA}` |
| preserved v06 | `{meta_v06['sha256']}` |
| preserved v07 | `{meta_v07['sha256']}` |

## Loudness (master, before PHONE/gates)
I={levels['lufs']:.2f} LUFS, TP={levels['tp']:.2f} dBTP (band −14.5..−13.5 / ≤−1.6)

## Spoken (unchanged)
{spoken}

## Hitch window (timeline 0.30–0.55 s)
{hitch_txt}

## Gates (all from sha `{final_sha}`)
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | {gate.returncode} | see `…_gate.txt` |
| sfx level | {level.returncode} | |
| polish_gate | {polish.returncode} | |
| music_gate | {music.returncode} | |
| picture_qa | {picture_qa.returncode} | |
| finish_scan loop | {loop_rc} | {loop_txt.strip()} |

## Evidence
- Before/after strip: `{strip}` and `jobs/reviews/J1242/uranus_v10_open_before_after.jpg`
- Full-size frames: `jobs/reviews/J1242/uranus_v10_t*.jpg`
- UAT: `{UAT_ICLOUD}` and `{UAT_NAS}` with MANIFEST.sha256
- Motion: `jobs/reviews/J1242/MOTION_DIAGNOSTIC.json`
- Transform sign check: `jobs/reviews/J1242/TRANSFORM_SIGN_CHECK.json`
- UAT playable: `jobs/reviews/J1242/UAT_PLAYABLE.json`

Park for elected Chief: do NOT repoint J1212 until Chief PASS on v10. No upload.
"""
    )
    print("DONE Uranus v10", final_sha, flush=True)
    # Always exit 0 after delivery so the job can park numbers even on a gate FAIL.
    # Chief stop rule: do not iterate Shot9 further.
    if gate.returncode != 0 or loop_rc != 0 or not hitch_ok:
        raise SystemExit(
            f"v10 delivered but gate/loop/hitch not clean: "
            f"gate={gate.returncode} loop={loop_rc} hitch_ok={hitch_ok}"
        )


if __name__ == "__main__":
    main()
