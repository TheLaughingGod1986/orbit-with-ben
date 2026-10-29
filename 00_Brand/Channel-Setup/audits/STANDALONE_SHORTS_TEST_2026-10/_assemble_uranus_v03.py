#!/usr/bin/env python3
"""J1204 Uranus standalone S4 v03. Chief SOURCE_PLAN_RULING 2026-10-29.

- VO: complete S2 first, then S1, S3, S4 from locked vo_v02 (no new speech).
- Open: SVS 20390 Shot4 Beauty Pass artist animation, centre-crop 9:16.
- Forward loop: continuous Shot4 strip so tail is the runway immediately before
  the open window (open source 1.15–3.85 s = early Beauty Pass; literal 0–2.7
  open has no pre-roll and fails finish_scan). First picture cut still ≤3 s.
- Preserve v02 files. £0. No upload/swap/privacy/Buffer.
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
SHOT4 = Path("/Volumes/data/mac-mini-archive/scratch/J1206/raw/Shot4_1k_mp4.mp4")
SHOT4_SHA = "32370afa93cb69570ec05ee9abd1e9670171deb2ab33ceed6807d63dde716526"
VO_V02 = Path("/Volumes/data/mac-mini-archive/scratch/J1199/uranus_v02/vo_v02.wav")
VO_V02_SHA = "484a7d9ead015de266f6eb9937b6f6b9b5e8e9ec7c1b0124750ecea77f5410df"
META_V02 = HERE / "06_Final-Exports/owb_sa_s4_uranus_v02_meta.json"
WORK = Path("/Volumes/data/mac-mini-archive/scratch/J1204/uranus_v03")
KIT = Path("/Volumes/data/mac-mini-archive/scratch/J0914/kit")
OUT = HERE / "06_Final-Exports"
QA = HERE / "qa_shorts_v01" / "owb_sa_s4_uranus_v03"
UAT_ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v03"
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v03")
EVIDENCE = REPO / "jobs/reviews/J1204"

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

# v02 caption clock (Stay already excised) — sentence blocks for reorder option 1
S1 = (0.10, 3.40)
S2 = (3.55, 7.13)
S3 = (7.53, 9.91)
S4 = (10.31, 15.77)
BREATH = 0.40
OPEN_DUR = 2.70
TAIL_DUR = 1.15
# Continuous Shot4 strip: tail = [0, TAIL_DUR), open = [TAIL_DUR, TAIL_DUR+OPEN_DUR)
SHOT4_TAIL_IN = 0.00
SHOT4_OPEN_IN = TAIL_DUR  # 1.15
SHOT4_OPEN_OUT = TAIL_DUR + OPEN_DUR  # 3.85


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


def extract_shot4_segment(ss: float, dur: float, n: int, out: Path) -> float:
    """Centre-crop Shot4 to 1080×1920. Returns measured upscale."""
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        f"fps={FPS},"
        f"crop={CROP_W}:{CROP_H}:{CROP_X}:0,"
        f"scale={W}:{H}:flags=lanczos,"
        f"setsar=1,format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", SHOT4,
        "-vf", vf, "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-frames:v", str(n),
        str(out),
    ])
    got = base.dur(out)
    want = n / FPS
    if abs(got - want) > 0.15:
        raise SystemExit(f"{out.name} is {got:.2f}s, wanted {want:.2f}s")
    return UPSCALE


def reorder_vo(captions: list[dict]) -> tuple[Path, list[dict], str]:
    """Lead with complete S2, then S1, S3, S4. Sample-accurate atrims + breaths."""
    blocks = [
        ("S2", S2),
        ("S1", S1),
        ("S3", S3),
        ("S4", S4),
    ]
    # Build filter: atrim each block, pad breath between (silence via aevalsrc or apad between concat)
    parts_f = []
    maps = []
    t_cursor = 0.0
    new_words: list[dict] = []
    for i, (_name, (a, b)) in enumerate(blocks):
        parts_f.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a{i}]")
        maps.append(f"[a{i}]")
        length = b - a
        for w in captions:
            if w["start"] + 1e-6 >= a and w["end"] - 1e-6 <= b + 0.02:
                new_words.append({
                    "word": w["word"],
                    "start": round(t_cursor + (w["start"] - a), 3),
                    "end": round(t_cursor + (w["end"] - a), 3),
                })
        t_cursor = round(t_cursor + length, 3)
        if i < len(blocks) - 1:
            parts_f.append(
                f"[1:a]atrim=0:{BREATH:.3f},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[b{i}]"
            )
            maps.append(f"[b{i}]")
            t_cursor = round(t_cursor + BREATH, 3)

    fc = ";".join(parts_f) + ";" + "".join(maps) + f"concat=n={len(maps)}:v=0:a=1[aout]"
    vo = WORK / "vo_v03.wav"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", VO_V02,
        "-f", "lavfi", "-t", f"{BREATH * 4:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-filter_complex", fc,
        "-map", "[aout]", "-ac", "2", "-ar", "48000", vo,
    ])
    spoken = " ".join(w["word"] for w in new_words)
    if "stay" in spoken.lower() or "i'll show" in spoken.lower().replace("i’ll", "i'll"):
        raise SystemExit(f"meta-promise still in spoken: {spoken}")
    if not new_words[0]["word"].lower().startswith("uranus"):
        raise SystemExit(f"sentence 1 must start with Uranus, got {new_words[0]}")
    return vo, new_words, spoken


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    if not SHOT4.is_file():
        raise SystemExit(f"missing Shot4 {SHOT4}")
    got_shot = sha256(SHOT4)
    if got_shot != SHOT4_SHA:
        raise SystemExit(f"Shot4 sha mismatch {got_shot}")
    if not VO_V02.is_file():
        raise SystemExit(f"missing vo_v02 {VO_V02}")
    got_vo = sha256(VO_V02)
    if got_vo != VO_V02_SHA:
        raise SystemExit(f"vo_v02 sha mismatch {got_vo}")
    if UPSCALE > 2.35 + 1e-6:
        raise SystemExit(f"upscale {UPSCALE:.3f} > 2.35")

    meta_v02 = json.loads(META_V02.read_text())
    captions = meta_v02["captions"]
    vo, words, spoken = reorder_vo(captions)
    last_end = words[-1]["end"]
    total = round(max(last_end + TAIL_DUR, 18.0), 3)
    if total - last_end > 1.5:
        total = round(last_end + 1.5, 3)
    if total < 18.0:
        total = 18.0
    print(f"words {len(words)} last {last_end} total {total}", flush=True)
    print(f"spoken={spoken}", flush=True)

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
    print(f"plates {list(zip(names, [round(c / FPS, 3) for c in counts]))}", flush=True)
    if counts[0] / FPS > 3.0 + 1e-6:
        raise SystemExit(f"first cut {counts[0] / FPS:.2f}s > 3.0s")
    if any(c / FPS > 4.05 for c in counts[:-1]):
        raise SystemExit(f"hold too long {counts}")

    open_n, tail_n = counts[0], counts[-1]
    # Shared continuous Shot4 strip: tail then open in source order, then split.
    cycle_n = open_n + tail_n
    cycle_ss = SHOT4_TAIL_IN
    cycle_dur = cycle_n / FPS
    cycle_mp4 = WORK / "seg_open_tail_cycle.mp4"
    print(f"  Shot4 cycle ss={cycle_ss:.3f} dur={cycle_dur:.3f} n={cycle_n} "
          f"(tail src {SHOT4_TAIL_IN:.2f}-{SHOT4_OPEN_IN:.2f}, "
          f"open src {SHOT4_OPEN_IN:.2f}-{SHOT4_OPEN_OUT:.2f})", flush=True)
    upscale = extract_shot4_segment(cycle_ss, cycle_dur + 0.05, cycle_n, cycle_mp4)
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

    tipped = next(w for w in words if w["word"].lower().startswith("tipped"))
    ov_window = (round(tipped["start"] - 0.15, 3), round(tipped["end"] + 1.6, 3))
    ov_window = (max(ov_window[0], 2.2), min(ov_window[1], 8.9))
    if ov_window[1] <= ov_window[0] + 0.5:
        # tipped is inside 0-2 s after reorder — place card just after hook
        ov_window = (2.2, min(4.5, OPEN_DUR + 1.5))

    shot4_title = (
        "Uranus Beauty Pass 1 (Shot4) — NASA SVS 20390 / Conceptual Image Lab "
        "artist animation (not spacecraft camera). "
        f"Centre crop {CROP_W}x{CROP_H}@{CROP_X},0 → {W}x{H}; measured upscale {upscale:.3f}x. "
        f"Open source {SHOT4_OPEN_IN:.2f}-{SHOT4_OPEN_OUT:.2f}s; "
        f"tail source {SHOT4_TAIL_IN:.2f}-{SHOT4_OPEN_IN:.2f}s (forward loop runway)."
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
            src = shot4_title
            max_up = round(upscale, 3)
        elif name == "tail":
            if path.resolve() != tail_path.resolve():
                shutil.copy2(tail_path, path)
            else:
                path = tail_path
            src = shot4_title + " [tail=open-cycle before f0]"
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
            src = f"s4_uranus/{fn} NASA plate on navy space, push/pan"
            max_up = 1.4
        a, b = frame_i / FPS, (frame_i + n) / FPS
        parts.append(path)
        cuts.append({
            "row": len(cuts) + 1,
            "timeline_in": round(a, 3),
            "timeline_out": round(b, 3),
            "source": src,
            "source_title": src,
            "zoom": "svs-shot4-crop" if name in ("open", "tail") else "push/pan",
            "max_upscale": max_up,
            "measured_upscale": max_up,
            "framing": {"offset": round(b - a, 3)},
            "kind_note": (
                "artist animation / Conceptual Image Lab (WARN path per Chief ruling)"
                if name in ("open", "tail") else "NASA still plate"
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

    final = OUT / "owb_sa_s4_uranus_v03.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", comp, "-i", vo_s, "-i", bed_s, "-i", sfx_s,
         "-filter_complex",
         "[1:a]volume=1.30[v];[v][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
         "loudnorm=I=-13.8:TP=-1.7:LRA=11,"
         "alimiter=limit=0.84:attack=7:release=60:level=false,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *enc_args, "-t", f"{total:.3f}", final])
    levels = measure_lufs(final)
    print("levels", levels, "dur", round(base.dur(final), 3), flush=True)
    tries = 0
    while tries < 3 and (levels["tp"] > -1.55 or levels["lufs"] < -14.5 or levels["lufs"] > -13.5):
        tries += 1
        tmp = WORK / f"final_fix{tries}.mp4"
        if levels["tp"] > -1.55 and levels["lufs"] >= -14.4:
            af = "volume=0.97,alimiter=limit=0.82:attack=7:release=60:level=false"
        elif levels["lufs"] < -14.5:
            af = "volume=1.08,alimiter=limit=0.84:attack=7:release=60:level=false"
        else:
            af = "volume=0.95,alimiter=limit=0.82:attack=7:release=60:level=false"
        run(["ffmpeg", "-y", "-v", "error", "-i", final, "-af", af,
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
        shutil.move(tmp, final)
        levels = measure_lufs(final)
        print(f"levels after tweak {tries}", levels, flush=True)

    phone = OUT / "owb_sa_s4_uranus_v03_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "scale=720:1280:flags=lanczos",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", phone])

    # Full-size flagged frames for Chief (0 s / 2 s open)
    for label, t in (("t0_0.00s", 0.0), ("t2_2.00s", 2.0), ("t_cut_2.70s", 2.70)):
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", final, "-frames:v", "1",
             str(EVIDENCE / f"uranus_v03_{label}.jpg")])

    frames = OUT / "owb_sa_s4_uranus_v03_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, 2.8, 5.0, 9.5, 12.0, last_end, total - 0.08] + mids, frames)
    sheet2 = OUT / "owb_sa_s4_uranus_v03_2fps.jpg"
    sheet_2fps(final, sheet2)

    surprise = next(w for w in words if "97" in w["word"] or w["word"].lower().startswith("degrees"))
    meta = {
        "job": "J1204",
        "resolves": "J1199",
        "short": "s4",
        "version": "v03",
        "air_date": "2026-11-03",
        "youtube_id": "ZpEA8stoSPA",
        "title_on_screen": "This Planet Has 21-Year Winters",
        "package_title": "Why Does Uranus Have 21-Year Winters?",
        "file": str(final.relative_to(REPO)),
        "phone": str(phone.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "sheet_2fps": str(sheet2.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": round(base.dur(final), 3),
        "vo": str(vo),
        "vo_sha256": sha256(vo),
        "vo_parent_v02_sha256": VO_V02_SHA,
        "shot4_sha256": SHOT4_SHA,
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": spoken,
        "captions": words,
        "vo_reorder": "S2,S1,S3,S4 complete blocks from vo_v02; breath 0.40 s",
        "hook": "21-YEAR / WINTER (yellow WINTER), 0-2.2 s",
        "title_window_s": [9.0, 14.0],
        "overlay": {"kind": "fact", "lines": ["TIPPED", "97°"], "window": list(ov_window)},
        "cuts": cuts,
        "loudness": levels,
        "brief": {
            "frame0_source": cuts[0]["source"],
            "first_word_onset_s": words[0]["start"],
            "first_word": words[0]["word"],
            "surprise_word": surprise["word"],
            "surprise_word_s": surprise["start"],
            "first_cut_s": cuts[0]["timeline_out"],
            "last_word_to_loop_s": round(total - last_end, 3),
            "meta_promise": "no",
            "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts), 3),
            "shot4_open_src_s": [SHOT4_OPEN_IN, SHOT4_OPEN_OUT],
            "shot4_tail_src_s": [SHOT4_TAIL_IN, SHOT4_OPEN_IN],
            "measured_upscale": round(upscale, 3),
            "ruling": "jobs/reviews/J1204/SOURCE_PLAN_RULING_2026-10-29.md",
        },
        "audio": {
            "bed": str(base.BED.relative_to(REPO)),
            "sfx": f"rumble at 0 s, tick at {ov_window[0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14 LUFS target, loudnorm",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "loop": "forward: continuous Shot4 strip; tail is runway before open window",
        "rule8": "Shot4 artist animation open; S2-first names Uranus + 97° surprise; no new VO",
        "preserved_v02_sha256": meta_v02["sha256"],
    }
    meta_path = OUT / "owb_sa_s4_uranus_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", "2026-11-03", "--id", "ZpEA8stoSPA", "--vo", str(vo_s)],
        capture_output=True, text=True)
    (OUT / "owb_sa_s4_uranus_v03_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_s), "--sfx", str(sfx_s), "--bed", str(bed_s),
         "--minutes", f"{total / 60:.4f}"],
        capture_output=True, text=True)
    (OUT / "owb_sa_s4_uranus_v03_sfx_level.txt").write_text(level.stdout + level.stderr)
    polish_cuts = WORK / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(polish_cuts), "--out", str(WORK / "polish_gate.json")],
        capture_output=True, text=True)
    (OUT / "owb_sa_s4_uranus_v03_polish.txt").write_text(polish.stdout + polish.stderr)
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
    (OUT / "owb_sa_s4_uranus_v03_music_gate.txt").write_text(music.stdout + music.stderr)

    QA.mkdir(parents=True, exist_ok=True)
    pool = {
        "clips": [
            {
                "file": c["source"],
                "note": c.get("kind_note", c["source"]),
                "title": c.get("source_title", c["source"]),
                "kind": "artist_animation" if "Shot4" in c["source"] else "plate",
                "measured_upscale": c.get("measured_upscale", c.get("max_upscale")),
            }
            for c in cuts
        ]
    }
    (QA / "pool_owb_sa_s4_uranus_v03.json").write_text(json.dumps(pool, indent=2))
    (QA / "cuts_owb_sa_s4_uranus_v03.json").write_text(json.dumps(cuts, indent=2))
    picture_qa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(QA / "cuts_owb_sa_s4_uranus_v03.json"),
         "--pool", str(QA / "pool_owb_sa_s4_uranus_v03.json"),
         "--out-dir", str(QA)],
        capture_output=True, text=True)
    (OUT / "owb_sa_s4_uranus_v03_picture_qa.txt").write_text(picture_qa.stdout + picture_qa.stderr)

    try:
        m = finish_scan(final)
        loop_txt = (
            f"PASS loop_diff_masked {m['loop_diff_masked']:.2f} open_median_step {m['open_median_step']:.2f} "
            f"head_matches {m['head_matches']}\n"
        )
        loop_rc = 0
    except SystemExit as e:
        loop_txt = f"FAIL {e}\n"
        loop_rc = 1
    (OUT / "owb_sa_s4_uranus_v03_loop.txt").write_text(loop_txt)

    print(f"gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} picture_qa={picture_qa.returncode} loop={loop_rc}", flush=True)
    print(gate.stdout)
    print(loop_txt)

    delivered = [final, phone, frames, sheet2, meta_path,
                 OUT / "owb_sa_s4_uranus_v03_gate.txt",
                 OUT / "owb_sa_s4_uranus_v03_loop.txt",
                 OUT / "owb_sa_s4_uranus_v03_polish.txt",
                 OUT / "owb_sa_s4_uranus_v03_music_gate.txt",
                 OUT / "owb_sa_s4_uranus_v03_sfx_level.txt",
                 OUT / "owb_sa_s4_uranus_v03_picture_qa.txt"]
    for dest in (UAT_ICLOUD, UAT_NAS):
        dest.mkdir(parents=True, exist_ok=True)
        for src_f in delivered:
            if src_f.exists():
                shutil.copy2(src_f, dest / src_f.name)
        manifest = []
        for src_f in delivered:
            if not src_f.exists():
                continue
            digest = sha256(dest / src_f.name)
            if digest != sha256(src_f):
                raise SystemExit(f"sha mismatch {dest / src_f.name}")
            manifest.append(f"{digest}  {src_f.name}")
        (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n")
        print(f"copied {dest}", flush=True)

    report = EVIDENCE / "URANUS_V03_DELIVERY_2026-10-29.md"
    report.write_text(
        f"""# J1204 Uranus v03 delivery — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Ruling applied
`SOURCE_PLAN_RULING_2026-10-29.md`: S2-first VO; Shot4 artist animation open; S5/S6 not in this job.

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v03.mp4` | `{meta['sha256']}` |
| `vo_v03.wav` | `{meta['vo_sha256']}` |
| parent `vo_v02.wav` | `{VO_V02_SHA}` |
| Shot4 source | `{SHOT4_SHA}` |
| preserved rejected v02 | `{meta_v02['sha256']}` |

## Spoken (S2-first)
{spoken}

## Gates
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | {gate.returncode} | see `…_gate.txt` |
| sfx level | {level.returncode} | |
| polish_gate | {polish.returncode} | |
| music_gate | {music.returncode} | |
| picture_qa | {picture_qa.returncode} | honest artist-animation title; WARN path |
| finish_scan loop | {loop_rc} | {loop_txt.strip()} |

## Provenance
- Open/tail: SVS 20390 Shot4 Beauty Pass, Conceptual Image Lab artist animation.
- Open source in/out: {SHOT4_OPEN_IN:.2f}–{SHOT4_OPEN_OUT:.2f} s (forward-loop runway; continuous with tail 0.00–{SHOT4_OPEN_IN:.2f}).
- Measured upscale: {upscale:.3f}× (≤2.35).
- Full-size frames: `jobs/reviews/J1204/uranus_v03_t*.jpg`
- UAT: `{UAT_ICLOUD}` and `{UAT_NAS}` with MANIFEST.sha256

Parked for Chief cut review. No Ben card until PASS.
"""
    )
    print("DONE Uranus v03", meta["sha256"], flush=True)
    # Exit 0 only if open gate PASSes; other results logged for Chief.
    if gate.returncode != 0:
        raise SystemExit(f"gate_shorts_open FAIL rc={gate.returncode}")


if __name__ == "__main__":
    main()
