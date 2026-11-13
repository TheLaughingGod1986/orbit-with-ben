#!/usr/bin/env python3
"""J2221 — Journey Film 01 v01. £0. No new credits.

Stitches the locked 023–029 masters on the plan's slice windows, lays the eight
selected linking takes from J2784_PACE_v01.json, and builds our own distance maps,
chapter cards, Option A bed (owned 023/024/026 stems) and house SFX.

Masters are 1920x1080 30 fps. This cut conforms them to 24 fps and keeps duration.
Linking words are padded so the 0.5 s joins fall on silence, not on a syllable.
The 18 s end hold is picture and music after the closing line.

Scratch stays on MiniWork. The finished file is copied to the studio-live edit folder.
A second copy refuses to start while RUNNING names a live process.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SCRATCH = Path("/Volumes/MiniWork/scratch/J2221")
TMP = SCRATCH / "tmp"
FILM = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World")
OUT_DIR = FILM / "07_Edit-Project"
VO_DIR = FILM / "02_Voiceover"
FINAL_NAME = "J01_Journey_v01.mp4"
W, H, FPS = 1920, 1080, 24
XFADE = 0.50
HOLD = 18.0
HEAD = 0.55
TAIL = 0.55
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
EARTH = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18033.jpg")
VENUS_STILL = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_surface_465c_lander_plate.jpg")

MASTERS = {
    "027": ("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01m.mp4",
            "499e8edc06910cb646006a260fccbbbd9b9bc9e975f39940b0cbec2fc457b31d"),
    "023": ("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-13/loose_renders/023_Venus_full_rough_v05e.mp4",
            "5d8a8f73454f889a38590661885a21702690a42c8ebfd940868d033f0174e6fc"),
    "025": ("/Volumes/data/mac-mini-archive/youtube-staging/025/025_MarsRobot_full_rough_v03f.mp4",
            "cce6268cbd571f1f404ee98b86e089bbe3cabed15017113bd9559951ee36e09f"),
    "028": ("/Volumes/data/mac-mini-archive/youtube-staging/028/028_Gliese710_full_master_v03.mp4",
            "a9780e548a2775f4e7a1acecb6ac24308927f0b58ab1d606e67d27741e3db824"),
    "026": ("/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4",
            "6e587bb5ac33552cef55ac897d89f5516a90acef9473155254dd313fc73e09d3"),
    "024": ("/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v06.mp4",
            "8d0b131771c1e6bfc8b33f49f5c628e96ae3db3af7a890864f2239960a5bde02"),
    "029": ("/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4",
            "54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93"),
}
BEDS = {
    "026": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav",
    "023": "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3",
    "024": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/05_Music/light-speed_score_bed_v01_full.mp3",
}
# Plan slice windows, seconds. Parts 2–7 drop the agenda line, the extra subscribe beat, and the outro teaser.
PARTS = [
    ("part1_027", "027", "What If Earth Stopped Spinning", [(0.0, 443.50)]),
    ("part2_023", "023", "What Happened to Venus", [(0.0, 35.80), (43.20, 212.20), (218.20, 504.80)]),
    ("part3_025", "025", "Could a Robot Survive on Mars", [(0.0, 29.80), (40.80, 224.50), (231.00, 483.20)]),
    ("part4_028", "028", "What Happens When a Star Enters Our Solar System", [(0.0, 30.80), (42.20, 204.20), (209.80, 469.80)]),
    ("part5_026", "026", "Why Reaching the Nearest Star Takes 75,000 Years", [(0.0, 20.50), (32.80, 224.40), (232.00, 491.30)]),
    ("part6_024", "024", "What Happens If You Travel Near Light Speed", [(0.0, 28.30), (41.60, 213.10), (220.00, 483.00)]),
    ("part7_029", "029", "Is Betelgeuse About to Explode", [(0.0, 22.10), (37.20, 242.20), (247.60, 514.80)]),
]
CARDS = [
    ("PART ONE", "THE GROUND MOVING UNDER YOUR FEET", "0 KM"),
    ("PART TWO", "THE TWIN THAT LOST ITS WATER", "40 MILLION KM"),
    ("PART THREE", "THE RED WORLD FULL OF QUIET MACHINES", "225 MILLION KM"),
    ("PART FOUR", "THE STAR HEADING FOR OUR OUTER EDGE", "13,000 AU"),
    ("PART FIVE", "FOUR LIGHT-YEARS THROUGH THE DARK", "4.24 LIGHT-YEARS"),
    ("PART SIX", "WHEN YOUR CLOCK SLOWS DOWN", "99% LIGHT SPEED"),
    ("PART SEVEN", "THE DYING GIANT THAT MADE US", "600 LIGHT-YEARS"),
]
# bridge index 0..5 uses takes 2..7, maps 01..06
BRIDGE_META = [
    ("01", "023", 110.0, "023", "40 MILLION KM", "95% EARTH'S WIDTH"),
    ("02", "025", 120.0, "023", "225 MILLION KM", "127 MINUTES"),
    ("03", "028", 130.0, "024", "13,000 AU", "1.3 MILLION YEARS"),
    ("04", "026", 140.0, "026", "4.24 LIGHT-YEARS", "75,000 YEARS"),
    ("05", "024", 150.0, "024", "99% LIGHT SPEED", "7× SLOWER"),
    ("06", "029", 160.0, "026", "600 LIGHT-YEARS", "764× THE SUN"),
]
CARD_BED = ["026", "023", "023", "024", "026", "024", "026"]

os.environ["TMPDIR"] = str(TMP)
TMP.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd: list, timeout: int | None = None) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        tail = (r.stderr or r.stdout or "")[-800:]
        raise RuntimeError(f"command failed ({r.returncode}): {' '.join(cmd[:8])}\n{tail}")


def probe(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True)
    return float(out.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ready(path: Path, min_dur: float, slack: float = 0.2) -> bool:
    if not path.exists() or path.stat().st_size < 10000:
        return False
    try:
        return probe(path) + slack >= min_dur
    except Exception:
        return False


def encode_video(src_args: list, out: Path, duration: float, vf: str, silent: bool = True) -> None:
    if ready(out, duration):
        log(f"keep {out.name}")
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *src_args,
           "-t", f"{duration:.3f}", "-vf", vf, "-an" if silent else "-af", "aresample=48000,aformat=channel_layouts=stereo",
           "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    if silent:
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *src_args,
               "-t", f"{duration:.3f}", "-vf", vf, "-an",
               "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", str(out)]
    run(cmd)


def excerpt(key: str, start: float, duration: float, out: Path) -> None:
    src = MASTERS[key][0]
    pre = max(0.0, start - 2.0)
    inner = start - pre
    vf = ("fps=24,scale=2048:1152:force_original_aspect_ratio=increase,"
          "crop=1920:1080:x='(in_w-1920)/2+18*sin(2*PI*t/7)':y='(in_h-1080)/2+8*cos(2*PI*t/9)',"
          "format=yuv420p")
    encode_video(["-ss", f"{pre:.3f}", "-i", src, "-ss", f"{inner:.3f}"], out, duration, vf)


def cut_slice(key: str, start: float, end: float, out: Path) -> None:
    src = MASTERS[key][0]
    dur = end - start
    if dur <= 0.4:
        raise RuntimeError(f"bad slice {key} {start}-{end}")
    pre = max(0.0, start - 2.0)
    inner = start - pre
    vf = "fps=24,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
    if ready(out, dur - 0.08):
        log(f"keep {out.name}")
        return
    log(f"slice {key} {start:.2f}-{end:.2f}")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", f"{pre:.3f}", "-i", src, "-ss", f"{inner:.3f}", "-t", f"{dur:.3f}",
         "-vf", vf, "-af", "aresample=48000,aformat=channel_layouts=stereo",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)])


def xfade_join(files: list[Path], out: Path) -> float:
    durs = [probe(p) for p in files]
    if len(files) == 1:
        if not ready(out, durs[0] - 0.05):
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(files[0]), "-c", "copy", str(out)])
        return durs[0]
    expect = sum(durs) - XFADE * (len(files) - 1)
    if ready(out, expect - 0.4):
        log(f"keep {out.name}")
        return probe(out)
    log(f"join {out.name} ({len(files)} parts, ~{expect:.0f}s)")
    parts = []
    v, a = "[0:v]", "[0:a]"
    acc = durs[0]
    for i in range(1, len(files)):
        off = max(0.0, acc - XFADE)
        parts.append(f"{v}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={off:.3f}[vx{i}]")
        parts.append(f"{a}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[ax{i}]")
        v, a = f"[vx{i}]", f"[ax{i}]"
        acc += durs[i] - XFADE
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in files:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", ";".join(parts), "-map", v, "-map", a,
            "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)]
    run(cmd)
    return probe(out)


def font(size: int, didot: bool = False):
    path = FONT_DIDOT if didot else FONT_BOLD
    try:
        return ImageFont.truetype(path, size, index=1 if didot else 0)
    except Exception:
        return ImageFont.truetype(FONT_BOLD, size)


def fit(draw, text, max_w, start):
    size = start
    while size > 28:
        f = font(size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return font(28)


STARS = np.random.default_rng(11).random((180, 3))


def background(shift: int) -> np.ndarray:
    yy, xx = np.mgrid[0:H, 0:W]
    rad = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    rad = np.clip(rad, 0, 1)
    lift = 1.0 - rad
    img = np.empty((H, W, 3), np.float32)
    img[:, :, 0] = 22 + 28 * lift
    img[:, :, 1] = 40 + 36 * lift
    img[:, :, 2] = 72 + 48 * lift
    for sx, sy, br in STARS:
        x = int((sx * W + shift) % W)
        y = int(sy * H)
        c = 170 + int(br * 80)
        img[y, x] = (c, min(255, c + 12), min(255, c + 24))
    return img


def globe() -> np.ndarray:
    im = Image.open(EARTH).convert("RGBA")
    im = im.resize((150, 150), Image.Resampling.LANCZOS)
    arr = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:150, 0:150]
    mask = ((xx - 75) ** 2 + (yy - 75) ** 2) <= 70 ** 2
    arr[:, :, 3] = np.where(mask, arr[:, :, 3], 0)
    return arr


GLOBE = None


def paste(img: np.ndarray, sprite: np.ndarray, x: int, y: int) -> None:
    h, w = sprite.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    sx0, sy0 = x0 - x, y0 - y
    cut = sprite[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
    a = cut[:, :, 3:4] / 255.0
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + cut[:, :, :3] * a


def render_frames(path: Path, duration: float, draw_fn) -> None:
    if ready(path, duration - 0.05):
        log(f"keep {path.name}")
        return
    n = int(round(duration * FPS))
    log(f"render {path.name} {n} frames")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", str(path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for i in range(n):
            frame = draw_fn(i / FPS, duration)
            proc.stdin.write(np.ascontiguousarray(frame, dtype=np.uint8).tobytes())
            if i and i % (FPS * 5) == 0:
                log(f"  {path.name} {i / n:.0%}")
    finally:
        proc.stdin.close()
        code = proc.wait()
    if code != 0:
        raise RuntimeError(f"frame encode failed for {path}")


def label_layer(text: str, sub: str | None = None) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = fit(d, text, 1500, 78)
    tw = d.textlength(text, font=f)
    x, y = (W - tw) / 2, 78
    d.text((x, y), text, font=f, fill=(255, 214, 90, 255), stroke_width=3, stroke_fill=(12, 18, 32, 230))
    if sub:
        fs = fit(d, sub, 1400, 42)
        sw = d.textlength(sub, font=fs)
        d.text(((W - sw) / 2, y + 96), sub, font=fs, fill=(244, 244, 236, 255),
               stroke_width=2, stroke_fill=(12, 18, 32, 210))
    credit = font(28, didot=True)
    d.text((48, H - 64), "NASA", font=credit, fill=(244, 244, 236, 210))
    return layer


def blend_label(img: np.ndarray, layer: Image.Image, alpha: float) -> np.ndarray:
    if alpha <= 0.01:
        return img
    ov = np.asarray(layer).astype(np.float32)
    a = (ov[:, :, 3:4] / 255.0) * alpha
    out = img * (1 - a) + ov[:, :, :3] * a
    return np.clip(out, 0, 255)


def map_drawer(kind: str, title: str, scale: str):
    global GLOBE
    if GLOBE is None:
        GLOBE = globe()
    title_im = label_layer(title)
    scale_im = label_layer(scale)
    marks = {
        "00": [("EARTH", 0.04), ("VENUS", 0.18), ("MARS", 0.32), ("OORT", 0.50), ("PROXIMA", 0.70), ("BETELGEUSE", 0.90)],
        "01": [("EARTH", 0.24), ("VENUS", 0.74)],
        "02": [("VENUS", 0.24), ("MARS", 0.74)],
        "03": [("MARS", 0.24), ("OORT", 0.74)],
        "04": [("OORT", 0.24), ("PROXIMA", 0.74)],
        "06": [("PROXIMA", 0.24), ("BETELGEUSE", 0.74)],
    }.get(kind, [])

    def draw(t, duration):
        img = background(int(t * 36))
        p = min(1.0, t / max(0.8, duration * 0.82))
        y = 690
        x0, x1 = 180, 1740
        if kind == "05":
            # Earth bar full, ship bar to about 1/7, both growing with p.
            img[430:468, 360:360 + int(900 * p)] = (120, 190, 230)
            img[520:558, 360:360 + int(900 * p / 7)] = (255, 176, 90)
        else:
            x_end = int(x0 + (x1 - x0) * p)
            img[y - 2:y + 3, x0:max(x0 + 4, x_end)] = (255, 206, 90)
            paste(img, GLOBE, 70, 560)
            for name, pos in marks:
                if p + 0.02 < pos:
                    continue
                x = int(x0 + (x1 - x0) * pos)
                img[y - 18:y + 19, x - 3:x + 4] = (244, 244, 236)
        alpha = min(1.0, t / 0.4) * (1.0 if t < duration - 0.35 else max(0.0, (duration - t) / 0.35))
        layer = title_im if t < duration * 0.55 else scale_im
        return blend_label(img, layer, alpha)

    return draw


def card_drawer(lines):
    a, b, c = lines
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fa, fb, fc = fit(d, a, 1600, 42), fit(d, b, 1680, 72), fit(d, c, 1400, 40)
    y = 360
    for text, f, col in ((a, fa, (190, 210, 230, 255)), (b, fb, (255, 214, 90, 255)), (c, fc, (244, 244, 236, 255))):
        tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, y), text, font=f, fill=col, stroke_width=2, stroke_fill=(10, 16, 28, 220))
        y += f.size + 28

    def draw(t, duration):
        img = background(int(t * 28))
        # a thin rule draws across the card so the frame keeps moving
        p = min(1.0, t / 0.8)
        img[330:334, 360:360 + int(1200 * p)] = (255, 214, 90)
        alpha = min(1.0, t / 0.35) * (1.0 if t < duration - 0.3 else max(0.0, (duration - t) / 0.3))
        return blend_label(img, layer, alpha)

    return draw


def sfx_paths() -> dict[str, Path]:
    ui = SCRATCH / "sfx_ui"
    ink = SCRATCH / "sfx_ink"
    if not (ui / "sfx_kit_manifest.json").exists():
        run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "make", "--house", "owb", "--out-dir", str(ui)])
    if not (ink / "sfx_kit_manifest.json").exists():
        run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "make", "--house", "hos", "--out-dir", str(ink)])
    return {
        "rumble": next(ui.glob("*rumble_low*.wav")),
        "whoosh": next(ui.glob("*whoosh_soft*.wav")),
        "tick": next(ink.glob("*tick_ink*.wav")),
    }


def mix(out: Path, duration: float, bed_key: str, vo: Path | None, vo_delay: float,
        events: list[tuple[Path, float, str]]) -> None:
    if ready(out, duration - 0.08):
        log(f"keep {out.name}")
        return
    bed = BEDS[bed_key]
    target = "-30" if vo is not None else "-23"
    filters = []
    inputs = ["-stream_loop", "-1", "-i", bed]
    filters.append(f"[0:a]atrim=0:{duration:.3f},asetpts=PTS-STARTPTS,loudnorm=I={target}:TP=-8:LRA=7[bed]")
    mix_in = ["[bed]"]
    if vo is not None:
        inputs += ["-i", str(vo)]
        delay = int(vo_delay * 1000)
        filters.append(f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,adelay={delay}|{delay},apad=whole_dur={duration:.3f}[vo]")
        mix_in.append("[vo]")
    for n, (path, at, gain) in enumerate(events):
        idx = 1 + (1 if vo is not None else 0) + n
        inputs += ["-i", str(path)]
        ms = int(at * 1000)
        filters.append(f"[{idx}:a]volume={gain},adelay={ms}|{ms},apad=whole_dur={duration:.3f}[s{n}]")
        mix_in.append(f"[s{n}]")
    n_in = len(mix_in)
    filters.append("".join(mix_in) + f"amix=inputs={n_in}:duration=first:dropout_transition=0:normalize=0[a]")
    log(f"mix {out.name}")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
         "-filter_complex", ";".join(filters), "-map", "[a]",
         "-t", f"{duration:.3f}", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)])


def mux(video: Path, audio: Path, out: Path, duration: float) -> None:
    if ready(out, duration - 0.12):
        log(f"keep {out.name}")
        return
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(video), "-i", str(audio), "-t", f"{duration:.3f}",
         "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-shortest", str(out)])


def concat_video(files: list[Path], out: Path, duration: float) -> None:
    if ready(out, duration - 0.15):
        log(f"keep {out.name}")
        return
    labels = []
    parts = []
    for i in range(len(files)):
        parts.append(f"[{i}:v]fps={FPS},format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
        labels.append(f"[v{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(files)}:v=1:a=0[v]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in files:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-an",
            "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", str(out)]
    run(cmd)


def verify_inputs(takes: list[dict]) -> None:
    log("checking master and voice hashes")
    for key, (path, expect) in MASTERS.items():
        got = sha256(Path(path))
        if got != expect:
            raise RuntimeError(f"master {key} hash {got} != plan {expect}")
        log(f"  master {key} ok")
    for t in takes:
        rel = t["selected_path"]
        fp = VO_DIR / rel
        expect = t["output_sha256"] if "pace_v01" in rel else t["original_wav_sha256"]
        got = sha256(fp)
        if got != expect:
            raise RuntimeError(f"take {t['n']} hash {got} != manifest {expect}")
        log(f"  take {t['n']} ok {probe(fp):.2f}s")


def load_takes() -> list[dict]:
    data = json.loads((REPO / "02_Video-Projects/J01_Journey-To-Every-World/02_Voiceover/J2784_PACE_v01.json").read_text())
    takes = sorted(data["takes"], key=lambda t: t["n"])
    if [t["n"] for t in takes] != list(range(1, 9)):
        raise RuntimeError("expected eight linking takes")
    return takes


def report(step: int, action: str, note: str) -> None:
    try:
        subprocess.run([sys.executable, str(REPO / "scripts/jobs.py"), "progress", "J2221",
                        "--agent", "cursor", "--step", str(step), "--of", "5",
                        "--action", action, "--note", note[:110], "--git"],
                       check=False, timeout=180)
    except Exception as exc:
        log(f"progress note failed: {exc}")


def running_pid() -> int | None:
    flag = SCRATCH / "RUNNING"
    if not flag.exists():
        return None
    try:
        pid = int(flag.read_text().strip())
    except ValueError:
        return None
    try:
        os.kill(pid, 0)
    except OSError:
        return None
    return pid


def build() -> None:
    if (pid := running_pid()) and pid != os.getpid():
        log(f"already running as pid {pid}")
        return 3
    (SCRATCH / "RUNNING").write_text(str(os.getpid()))
    takes = load_takes()
    verify_inputs(takes)
    report(1, "Render the maps, cards and the stitched Journey film", "Hashes match the plan and the pace manifest.")
    sfx = sfx_paths()
    gdir = SCRATCH / "graphics"
    gdir.mkdir(parents=True, exist_ok=True)
    vo_dur = [probe(VO_DIR / t["selected_path"]) for t in takes]
    # maps: 00 for the cold open, 01-06 for the six bridges
    cold_dur = vo_dur[0] + TAIL
    render_frames(gdir / "code_graphic_J01_map_00.mp4", cold_dur,
                  map_drawer("00", "OUTWARD FROM EARTH", "SUNLIGHT 8 MINUTES"))
    bridge_dur = []
    for i, (mid, _film, _start, _bed, title, scale) in enumerate(BRIDGE_META):
        dur = HEAD + vo_dur[i + 1] + TAIL
        bridge_dur.append(dur)
        render_frames(gdir / f"code_graphic_J01_map_{mid}.mp4", dur, map_drawer(mid, title, scale))
    for i, lines in enumerate(CARDS, start=1):
        render_frames(gdir / f"code_graphic_J01_card_{i:02d}.mp4", 3.0, card_drawer(lines))
    report(2, "Cut the seven films and lay the linking voice", "Maps and chapter cards are rendered.")

    # plates and cold open
    beats_d = cold_dur / 11
    cold_pieces = []
    pattern = [("027", 390.0), None, ("023", 100.0), None, ("025", 110.0), None,
               ("029", 180.0), None, ("027", 250.0), None, ("027", 410.0)]
    for i, item in enumerate(pattern):
        piece = gdir / f"cold_{i:02d}.mp4"
        if item is None:
            run_trim(gdir / "code_graphic_J01_map_00.mp4", i * beats_d, beats_d, piece)
        else:
            excerpt(item[0], item[1], beats_d, piece)
        cold_pieces.append(piece)
    cold_v = gdir / "cold_picture.mp4"
    concat_video(cold_pieces, cold_v, cold_dur)
    cold_a = SCRATCH / "audio" / "cold.wav"
    cold_a.parent.mkdir(parents=True, exist_ok=True)
    mix(cold_a, cold_dur, "026", VO_DIR / takes[0]["selected_path"], 0.0, [
        (sfx["rumble"], 0.2, "-18dB"),
        (sfx["tick"], beats_d + 0.1, "-16dB"),
        (sfx["tick"], 3 * beats_d + 0.1, "-16dB"),
        (sfx["tick"], 5 * beats_d + 0.1, "-16dB"),
        (sfx["tick"], 7 * beats_d + 0.1, "-16dB"),
        (sfx["tick"], 9 * beats_d + 0.1, "-16dB"),
    ])
    cold = SCRATCH / "seg_cold.mp4"
    mux(cold_v, cold_a, cold, cold_dur)

    segs: list[tuple[str, Path, str]] = [("cold", cold, "Cold open")]
    # cards and bridges and parts interleaved
    for i in range(7):
        card_v = gdir / f"code_graphic_J01_card_{i+1:02d}.mp4"
        card_a = SCRATCH / "audio" / f"card_{i+1}.wav"
        mix(card_a, 3.0, CARD_BED[i], None, 0.0, [(sfx["tick"], 0.25, "-16dB")])
        card = SCRATCH / f"seg_card_{i+1}.mp4"
        mux(card_v, card_a, card, 3.0)
        segs.append((f"card{i+1}", card, CARDS[i][0] + " " + CARDS[i][1]))
        name, key, title, windows = PARTS[i]
        slices = []
        for n, (a, b) in enumerate(windows):
            sl = SCRATCH / "slices" / f"{name}_{n}.mp4"
            sl.parent.mkdir(parents=True, exist_ok=True)
            cut_slice(key, a, b, sl)
            slices.append(sl)
        part = SCRATCH / f"seg_{name}.mp4"
        xfade_join(slices, part)
        segs.append((name, part, title))
        if i < 6:
            dur = bridge_dur[i]
            mid, film, start, bed, _title, _scale = BRIDGE_META[i]
            plate = gdir / f"bridge_{i+1}_plate.mp4"
            excerpt(film, start, dur, plate)
            graphic = gdir / f"code_graphic_J01_map_{mid}.mp4"
            pieces = []
            nbeats = 5
            beat = dur / nbeats
            for b in range(nbeats):
                piece = gdir / f"bridge_{i+1}_{b}.mp4"
                src = plate if b % 2 == 0 else graphic
                run_trim(src, b * beat, beat, piece)
                pieces.append(piece)
            bv = gdir / f"bridge_{i+1}_picture.mp4"
            concat_video(pieces, bv, dur)
            ba = SCRATCH / "audio" / f"bridge_{i+1}.wav"
            events = [(sfx["tick"], beat + 0.05, "-16dB"), (sfx["tick"], 3 * beat + 0.05, "-16dB")]
            if i in (0, 2, 4):
                events.insert(0, (sfx["whoosh"], 0.15, "-16dB"))
            if i == 5:
                events.insert(0, (sfx["rumble"], 0.2, "-18dB"))
            mix(ba, dur, bed, VO_DIR / takes[i + 1]["selected_path"], HEAD, events)
            bridge = SCRATCH / f"seg_bridge_{i+1}.mp4"
            mux(bv, ba, bridge, dur)
            segs.append((f"bridge{i+1}", bridge, _title))

    close_dur = HEAD + vo_dur[7] + HOLD
    close_pieces = []
    sources = [("029", 200.0), ("025", 180.0), ("023", 140.0), ("027", 300.0)]
    beat = close_dur / 8
    for b in range(8):
        film, start = sources[b % 4]
        piece = gdir / f"close_{b}.mp4"
        excerpt(film, start + b * 3, beat, piece)
        close_pieces.append(piece)
    cv = gdir / "close_picture.mp4"
    concat_video(close_pieces, cv, close_dur)
    ca = SCRATCH / "audio" / "close.wav"
    mix(ca, close_dur, "026", VO_DIR / takes[7]["selected_path"], HEAD, [(sfx["rumble"], 0.3, "-18dB")])
    closing = SCRATCH / "seg_close.mp4"
    mux(cv, ca, closing, close_dur)
    segs.append(("close", closing, "Closing and end hold"))

    report(3, "Join the Journey film and normalise the loudness", "Linking pieces and film slices are cut.")
    final_local = SCRATCH / FINAL_NAME
    xfade_join([p for _n, p, _t in segs], final_local)
    norm = SCRATCH / "J01_Journey_v01_loudnorm.mp4"
    loudnorm(final_local, norm)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / FINAL_NAME
    log(f"copy {dest}")
    run(["rsync", "-a", "--partial", str(norm), str(dest)])
    digest = sha256(dest)
    (OUT_DIR / "J01_Journey_v01.sha256").write_text(f"{digest}  {FINAL_NAME}\n")
    timeline = []
    t = 0.0
    files = [p for _n, p, _t in segs]
    durs = [probe(p) for p in files]
    for i, ((name, path, title), dur) in enumerate(zip(segs, durs)):
        span = dur if i == len(segs) - 1 else dur - XFADE / 2
        # The xfade shortens the join. Record the placed window from a running offset.
        timeline.append({"name": name, "title": title, "file": path.name,
                         "source_duration": round(dur, 3)})
    # Recompute placed times the same way xfade does.
    acc = 0.0
    placed = []
    for i, ((name, path, title), dur) in enumerate(zip(segs, durs)):
        start = 0.0 if i == 0 else acc - XFADE
        # After the first, acc already includes previous full durations minus fades.
        placed.append({"name": name, "title": title, "file": str(path),
                       "timeline_in": round(max(0.0, acc if i == 0 else acc), 3),
                       "duration": round(dur, 3)})
        acc = dur if i == 0 else acc + dur - XFADE
    for i, row in enumerate(placed):
        row["timeline_in"] = round(0.0 if i == 0 else sum(durs[:i]) - XFADE * i, 3)
        row["timeline_out"] = round(row["timeline_in"] + durs[i] - (XFADE if i < len(durs) - 1 else 0.0), 3)
    (OUT_DIR / "J01_Journey_v01_timeline.json").write_text(json.dumps({
        "duration": probe(dest), "sha256": digest, "fps": FPS, "hold_s": HOLD,
        "segments": placed, "note": "Chapter times follow the real takes, which run longer than the plan's targets.",
    }, indent=2) + "\n")
    build_thumbs()
    qa_code, music_code = gates(dest, placed)
    report(4, "Journey cut is on the shared film folder for review",
           f"File {probe(dest):.0f}s. picture_qa {qa_code}, music_gate {music_code}.")
    (SCRATCH / "RUNNING").unlink(missing_ok=True)
    log("done")
    return 0


def run_trim(src: Path, start: float, duration: float, out: Path) -> None:
    if ready(out, duration - 0.08):
        return
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{duration:.3f}",
         "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-pix_fmt", "yuv420p", str(out)])


def loudnorm(src: Path, out: Path) -> None:
    if ready(out, probe(src) - 1.0):
        log("keep loudnorm")
        return
    log("measure loudness")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src),
                        "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    blob = r.stderr
    i = blob.rfind("{")
    if i < 0:
        raise RuntimeError("loudnorm measure failed\n" + blob[-500:])
    measured = json.loads(blob[i:])
    af = ("loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={input_i}:measured_TP={input_tp}:"
          "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true")
    af = af.format(**{k: measured[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")})
    log("apply loudnorm")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out)])


def build_thumbs() -> None:
    thumb = OUT_DIR.parent / "08_Thumbnail" / "j01_v01"
    thumb.mkdir(parents=True, exist_ok=True)
    mars = SCRATCH / "thumb_mars.jpg"
    betel = SCRATCH / "thumb_betel.jpg"
    if not mars.exists():
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "140", "-i", MASTERS["025"][0],
             "-frames:v", "1", str(mars)])
    if not betel.exists():
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "200", "-i", MASTERS["029"][0],
             "-frames:v", "1", str(betel)])
    earth = Image.open(EARTH).convert("RGB")
    venus = Image.open(VENUS_STILL).convert("RGB")
    mars_im = Image.open(mars).convert("RGB")
    betel_im = Image.open(betel).convert("RGB")

    def cover(im, box):
        im = ImageOps_fit(im, box)
        return im

    a = Image.new("RGB", (W, H))
    a.paste(cover(venus, (W, H)), (0, 0))
    right = cover(mars_im, (W // 2, H))
    a.paste(right, (W // 2, 0))
    stamp(a, "464°C", "TO -60°C")
    b = cover(betel_im, (W, H))
    # bright grade
    arr = np.clip(np.asarray(b).astype(np.float32) * 1.15 + 8, 0, 255).astype(np.uint8)
    b = Image.fromarray(arr)
    disc = earth.resize((220, 220), Image.Resampling.LANCZOS)
    mask = Image.new("L", (220, 220), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, 218, 218), fill=255)
    b.paste(disc, (140, 620), mask)
    stamp(b, "764×", "OUR SUN")
    c = Image.new("RGB", (W, H), (18, 28, 52))
    bodies = [earth, venus, mars_im, betel_im]
    for i, im in enumerate(bodies):
        d = 280
        sprite = im.resize((d, d), Image.Resampling.LANCZOS)
        m = Image.new("L", (d, d), 0)
        ImageDraw.Draw(m).ellipse((2, 2, d - 2, d - 2), fill=255)
        c.paste(sprite, (180 + i * 430, 430), m)
    stamp(c, "EARTH", "TO ORION")
    # The plan's "8 WORLDS OUT" counts Apophis, which has no long master in this cut.
    paths = {
        "thumb_A_real_venera_mars.jpg": a,
        "thumb_B_bright_supergiant_scale.jpg": b,
        "thumb_C_outward_worlds_lineup.jpg": c,
    }
    for name, im in paths.items():
        im.save(thumb / name, quality=92)
    sheet = thumb / "thumb_preview_long.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "long",
         *[str(thumb / n) for n in paths], "--out", str(sheet), "--score"])
    log(f"thumbs {thumb}")


def ImageOps_fit(im: Image.Image, box: tuple[int, int]) -> Image.Image:
    tw, th = box
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def stamp(im: Image.Image, yellow: str, white: str) -> None:
    d = ImageDraw.Draw(im)
    yf, wf = font(150), font(150)
    x, y = 80, 70
    d.text((x, y), yellow, font=yf, fill=(255, 214, 40), stroke_width=8, stroke_fill=(8, 10, 16))
    gap = d.textlength(yellow + " ", font=yf)
    d.text((x + gap, y), white, font=wf, fill=(248, 248, 242), stroke_width=8, stroke_fill=(8, 10, 16))


def gates(video: Path, placed: list[dict]) -> None:
    cuts = []
    pool = []
    for i, row in enumerate(placed):
        cuts.append({
            "row": i + 1,
            "source": row["file"],
            "timeline_in": row["timeline_in"],
            "timeline_out": row["timeline_out"],
            "upscale": 1.07,
            "video": True,
            "framing": {"offset": 0},
        })
        if "code_graphic" not in Path(row["file"]).name and "card" not in row["name"]:
            pool.append({"file": Path(row["file"]).name, "title": row["title"]})
    pack = OUT_DIR / "j01_v01_pack"
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (pack / "pool.json").write_text(json.dumps(pool, indent=2) + "\n")
    qa = subprocess.run([sys.executable, str(REPO / "scripts/picture_qa.py"), str(video),
                         "--cuts", str(pack / "cuts.json"), "--pool", str(pack / "pool.json"),
                         "--out-dir", str(pack)], capture_output=True, text=True)
    (pack / "picture_qa_run.txt").write_text(qa.stdout + "\n" + qa.stderr)
    music = FILM / "05_Music"
    music.mkdir(parents=True, exist_ok=True)
    bed = music / "j01_journey_linking_bed_v01.wav"
    if not bed.exists():
        # A short owned-stem bed for the linking sections. It is the Option A source, not a new purchase.
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", BEDS["026"],
             "-t", "180", "-af", "lowpass=f=3200,loudnorm=I=-28:TP=-8:LRA=7",
             "-c:a", "pcm_s16le", str(bed)])
    plan = {
        "file": bed.name,
        "prompt": "Pace: 66-70 BPM. Warm C-minor space drone reused from the owned 026 nearest-star stem for the Journey linking sections. NOT: no heavy percussion, no horror dissonance, no trailer brass, not a copy laid under a different film's title.",
        "option": "A",
        "note": "Linking bed only. The seven locked films keep the score already mixed into their masters. music_gate reused-check is expected to fail because this stem is the 026 bed on purpose.",
    }
    (music / "j01_journey_linking_bed_v01_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    # music_gate wants the plan beside the bed. The generator's name is the json above.
    mg = subprocess.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
                         "--bed", str(bed), "--video", str(video), "--out", str(pack / "music_gate.json")],
                        capture_output=True, text=True)
    (pack / "music_gate_run.txt").write_text(mg.stdout + "\n" + mg.stderr)
    log(f"picture_qa exit {qa.returncode}; music_gate exit {mg.returncode}")
    return qa.returncode, mg.returncode


def smoke() -> None:
    """A short join so a bad filter shows up before the 50-minute encode."""
    sdir = SCRATCH / "smoke"
    sdir.mkdir(parents=True, exist_ok=True)
    render_frames(sdir / "map.mp4", 4.0, map_drawer("01", "40 MILLION KM", "95% EARTH'S WIDTH"))
    render_frames(sdir / "card.mp4", 3.0, card_drawer(CARDS[0]))
    excerpt("027", 80.0, 4.0, sdir / "plate.mp4")
    # Give the plate a silent audio bed so xfade has audio on every input.
    for name, dur in (("map", 4.0), ("card", 3.0), ("plate", 4.0)):
        v = sdir / f"{name}.mp4"
        a = sdir / f"{name}_a.wav"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
             f"anullsrc=r=48000:cl=stereo", "-t", str(dur), str(a)])
        mux(v, a, sdir / f"{name}_av.mp4", dur)
    xfade_join([sdir / "plate_av.mp4", sdir / "map_av.mp4", sdir / "card_av.mp4"], sdir / "smoke.mp4")
    frame = sdir / "map_frame.jpg"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "1.5", "-i", str(sdir / "map.mp4"),
         "-frames:v", "1", str(frame)])
    log(f"smoke ok {probe(sdir / 'smoke.mp4'):.2f}s frame {frame}")


def main() -> int:
    if "--smoke" in sys.argv:
        smoke()
        return 0
    try:
        return build() or 0
    except Exception as exc:
        log(f"FAILED {exc}")
        (SCRATCH / "RUNNING").unlink(missing_ok=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
