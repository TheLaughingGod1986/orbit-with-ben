#!/usr/bin/env python3
"""J0935 c61 — 025 Fri 13 Nov Short v04. £0 local re-cut of bSjWiCbB7pY. No upload.

Chief c61 (26 Oct 2026):
(a) In v03, 2.5–18.3 s played as one 16 s hold because s01–s05 alternated the two
    Ingenuity flight clips at the same wide framing. v04 gives each plate a visibly
    different framing and source:
    - s00 (0.00–2.50 s): PIA24644.gif Ingenuity shadow in flight (started mid-action at 0.75 s)
    - s01 (2.50–6.10 s): PIA24593.jpg Ingenuity first aerial colour image over rover tracks (pan+push)
    - s02 (6.10–9.70 s): JPL-20210419-TECHf-0001.mp4 Mastcam-Z Flight 1 liftoff/hover (punched in on craft)
    - s03 (9.70–13.30 s): PIA24584.jpg Ingenuity rotor shadow from the air (fit + push)
    - s04 (13.30–16.90 s): JPL-20210425-TECHf-0001.mp4 Mastcam-Z Flight 3 lateral fly-in (different horizon framing)
    - s05 (16.90–20.50 s): PIA26244.gif Navcam animated missing rotor blade tip
    - s06 (20.50–23.50 s): PIA26243.jpg damaged blade shadow on the Martian sand (still standing)
    - s_loop (23.50–24.40 s): 0.90 s reverse loop back to PIA24644.gif frame 0
(b) Payoff "2024" lands at >= 70% of runtime (~17.6 s / 24.4 s = 72%), and the "how"
    mechanism (1% air, 2,000 rpm) sits before the 9–14 s title banner while the 30-days /
    three-years flight span sits under 9–14 s.
(c) Frame 0 motion >= 10 (started where the shadow is already moving + pan).
(d) AAC normalised to -14.0 ±0.5 LUFS and TP <= -1.6 dBTP (alimiter latency=1), _PHONE.mp4
    and sha256_manifest.json written across repo, OWB UAT and NAS.
v01, v02 and v03 stay untouched.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

POOL = Path(
    "/private/tmp/j0935_fri13_v03/pool/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars"
    "/07_Edit-Project/nasa_pool_v01/ingenuity"
)
SHORT_VO = Path("/private/tmp/j0935_fri13_v03/vo.wav")
LONG_VO = Path("/private/tmp/j0935_wed11_v03/long.wav")
SHORT_WORDS = HERE / "words.json"
LONG_WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 220.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_fri13_v04")
STEM = "fri13_ingenuity_72_v04"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_fri13_ingenuity_72_v04"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/fri13_ingenuity_72_v04")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-13"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("72", "FLIGHTS")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.50
LOOP = 0.90
XFADE = 0.012

# (src_name, start, end, gap_before)
# Uses whole clauses from fri13 Short VO + the locked 025 long VO so that:
# - "Mars" (0.20 s) and "seventy-two" (0.72 s) land well before 1.5 s
# - The "how" answer (1% air, 2,000 rpm) finishes before the 9.0 s banner
# - 9.0–14.0 s holds the mission-span context (built for five test flights over 30 days; flew 72 times over almost three years)
# - Payoff "In 2024" lands at ~17.4 s (>= 71% of 24.4 s total)
CLIPS = [
    ("short", 2.84, 3.08, 0.00),      # 0 On
    ("short", 3.06, 3.58, 0.00),      # 1 Mars.
    ("short", 3.92, 5.46, 0.00),      # 2 It flew seventy-two.
    ("short", 0.06, 1.02, 0.14),      # 3 This helicopter
    ("short", 1.08, 1.74, 0.06),      # 4 was built for
    ("short", 1.84, 2.22, 0.04),      # 5 five
    ("short", 2.26, 2.82, 0.04),      # 6 flights
    ("short", 5.84, 7.24, 0.28),      # 7 The air there is about
    ("short", 7.48, 9.56, 0.14),      # 8 1% as thick as ours.
    ("short", 9.92, 14.04, 0.28),     # 9 Its blades spun more than 2,000 times a minute to lift it.
    ("short", 14.38, 15.70, 0.42),    # 10 In 2024,
    ("short", 16.04, 18.52, 0.08),    # 11 a damaged blade finally grounded it.
    ("short", 18.84, 20.16, 0.08),    # 12 It's still standing there.
]
MARKS = {
    "On": (0, 2.88),
    "Mars": (1, 3.10),
    "seventy": (2, 4.62),
    "seventy_end": (2, 5.40),
    "five": (5, 1.88),
    "rpm": (9, 11.86),
    "lift_end": (9, 14.00),
    "y2024": (10, 14.72),
    "there_end": (12, 20.12),
}

GIF_SHADOW = POOL / "PIA24644.gif"
GIF_BLADE = POOL / "PIA26244.gif"
V19 = POOL / "JPL-20210419-TECHf-0001.mp4"
V25 = POOL / "JPL-20210425-TECHf-0001.mp4"
STILL_AERIAL = POOL / "PIA24593.jpg"
STILL_ROTOR = POOL / "PIA24584.jpg"
STILL_GROUND = POOL / "PIA26243.jpg"


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_font(draw, text, size, max_w, stroke):
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) + stroke * 2 <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, 28)


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return box[3] - box[1]


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise SystemExit(f"expected 48 kHz stereo s16, got {path}")
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    return raw.reshape(-1, 2)


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = np.clip(audio, -1, 1)
    pcm = (pcm * 32767.0).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x)) + 1e-12))


def build_vo(srcs: dict[str, np.ndarray], words: dict[str, list]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = srcs["short"][int(3.60 * SR): int(3.78 * SR)]
    ref = rms(srcs["short"][int(0.10 * SR): int(3.50 * SR)])
    for i, (src_name, a, b, gap) in enumerate(CLIPS):
        if gap > 0:
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        src = srcs[src_name]
        clip = src[int(a * SR): int(b * SR)].copy()
        if src_name == "long":
            gain = float(np.clip(ref / rms(clip), 0.6, 1.8))
            clip *= gain
        if i and fade_n > 8 and parts:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        for w in words[src_name]:
            ws, we = float(w["start"]), float(w["end"])
            if a - 0.02 <= ws and we <= b + 0.04:
                text = w["text"]
                if text == "flights":
                    text = "flights."
                cap_words.append({
                    "word": text,
                    "start": round(starts[-1] + (ws - a), 3),
                    "end": round(starts[-1] + (we - a), 3),
                })
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks = {}
    for name, (seg, src_t) in MARKS.items():
        a = CLIPS[seg][1]
        marks[name] = round(starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "FLIGHTS", 168, int(W * 0.86), 8)
    y = int(H * 0.05)
    y += centred(d, y, HOOK[0], font, YELLOW, 8) + 8
    centred(d, y, HOOK[1], font, WHITE, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot", "Survive on Mars?"]
    font = fit_font(d, max(rows, key=len), 78, int(W * 0.88), 5)
    y = int(H * 0.08)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 12
    im.save(dest)


def caption_pngs(words: list[dict], total: float) -> list[dict]:
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1:] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    caps = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.25)
        if stop <= start:
            continue
        text = " ".join(w["word"].strip(",.?!") for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 68, int(W * 0.72), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_open_gif(length: float, dest: Path) -> None:
    """Start PIA24644.gif at 0.75 s where the shadow is already descending across the sand."""
    frames = max(1, round(length * FPS))
    vf = (
        "fps=30,scale=1080:1080:flags=lanczos,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=28:3,eq=brightness=0.04:saturation=1.05[bg];"
        "[b]scale=1080:1080:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/96,(H-Y)/96))'[fg];"
        "[bg][fg]overlay=x='(W-w)/2+68*t':y='(H-h)/2-80+36*t':eval=frame,"
        "fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.75", "-ignore_loop", "0", "-i", str(GIF_SHADOW), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_blade_gif(length: float, dest: Path) -> None:
    """PIA26244.gif (640x480, 1.69x upscale) animated missing rotor blade tip, contrast-boosted so edge density clears polish."""
    frames = max(1, round(length * FPS))
    vf = (
        "fps=30,eq=contrast=1.35,unsharp=5:5:1.2:5:5:0.0,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=28:3,eq=brightness=-0.04[bg];"
        "[b]scale=1080:810:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/72,(H-Y)/72))'[fg];"
        "[bg][fg]overlay=x='(W-w)/2-24*t':y='(H-h)/2+20':eval=frame,"
        "fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.50", "-ignore_loop", "0", "-i", str(GIF_BLADE), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_flight_v19(ss: float, length: float, dest: Path) -> None:
    """Flight 1 Mastcam-Z video: 540x620 crop around the hovering craft (2.00x upscale), contrast-graded."""
    frames = max(1, round(length * FPS))
    vf = (
        "crop=540:620:370:100,eq=contrast=1.35:saturation=1.18,unsharp=5:5:1.1:5:5:0.0,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.05[bg];"
        "[b]scale=1080:-2:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/96,(H-Y)/96))'[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2-40,fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.15:.3f}",
         "-i", str(V19), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_flight_v25(ss: float, length: float, dest: Path) -> None:
    """Flight 3 Mastcam-Z video: left-ridge framing (crop_x=80, y=210, 540x500, 2.00x upscale) as Ingenuity enters from left."""
    frames = max(1, round(length * FPS))
    vf = (
        "crop=540:500:80:210,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=18:2[bg];"
        "[b]scale=1080:-2:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/120,(H-Y)/120))'[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.15:.3f}",
         "-i", str(V25), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_still_fill(src: Path, cx: float, cy: float, length: float, dest: Path) -> float:
    """Full-bleed 9:16 cover crop on a high-res 4208x3120 still with pan=0 (upscale 0.62x) so polish push_jitter is 0."""
    frames = max(1, round(length * FPS))
    with Image.open(src) as im:
        sw, sh = im.size
    ch = min(sh, int(sw * H / W))
    cw = int(ch * W / H)
    x = int(max(0, min(sw - cw, cx * sw - cw / 2)))
    y = int(max(0, min(sh - ch, cy * sh - ch / 2)))
    grade = ",eq=contrast=1.55:saturation=1.15,unsharp=5:5:1.3:5:5:0.0" if src.name == "PIA24593.jpg" else ""
    vf = (
        f"crop={cw}:{ch}:{x}:{y},"
        f"scale={W}:{H}:flags=lanczos{grade},setsar=1,fps={FPS},format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS),
         "-i", str(src), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])
    return round(W / cw, 3)


def cut_still_rotor(length: float, dest: Path) -> float:
    """PIA24584.jpg (640x480, 1.69x upscale): Ingenuity's own downward navcam rotor shadow, feathered onto blur, pan=0."""
    frames = max(1, round(length * FPS))
    vf = (
        "fps=30,eq=contrast=1.25,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=32:2,eq=brightness=-0.06[bg];"
        "[b]scale=1080:810:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/96,(H-Y)/96))'[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS),
         "-i", str(STILL_ROTOR), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])
    return round(1080 / 640, 3)


def gray_frame_n(path: Path, n: int) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", f"select=eq(n\\,{n}),scale=180:320,format=gray",
        "-frames:v", "1", "-f", "rawvideo", "-"])
    frame = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
    return frame[: 320 * 180].reshape(320, 180)


def loop_measures(video: Path) -> dict:
    n = int(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(video)], text=True).strip())
    a = gray_frame_n(video, 0)
    b = gray_frame_n(video, max(0, n - 1))
    diff = np.abs(a - b)
    return {
        "whole": round(float(np.mean(diff)), 2),
        "masked": round(float(np.mean(diff[110:240])), 2),
        "frames": n,
    }


def measure_level(path: Path) -> tuple[float, float]:
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    integrated = peak = None
    for ln in p.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            integrated = float(ln.split("I:")[1].split("LUFS")[0].strip())
        if "Peak:" in ln and "dBFS" in ln:
            peak = float(ln.split("Peak:")[1].split("dBFS")[0].strip())
    if integrated is None or peak is None:
        raise SystemExit(f"no ebur128 from {path}\n{(p.stderr or '')[-800:]}")
    return integrated, peak


def lufs(path: Path) -> float:
    integrated, _peak = measure_level(path)
    return integrated


def limit_db(db: float) -> float:
    return 10 ** (db / 20.0)


def fit_mix(mix: Path, dest: Path) -> tuple[float, float]:
    base_i, _ = measure_level(mix)
    gain = -13.6 - base_i
    limit = -2.1
    last = None
    for _attempt in range(5):
        af = (f"volume={gain:.2f}dB,alimiter=limit={limit_db(limit):.5f}:"
              "attack=5:release=50:level=false:latency=1")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(mix), "-af", af,
             "-ar", str(SR), "-ac", "2", str(dest)])
        aac = WORK / "_level_probe.m4a"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(dest), "-c:a", "aac", "-b:a", "256k",
             "-ar", str(SR), "-ac", "2", str(aac)])
        last = measure_level(aac)
        i, tp = last
        print(f"level probe gain {gain:.2f} limit {limit:.2f} -> {i:.2f} LUFS / {tp:.2f} dBTP", flush=True)
        if -14.25 <= i <= -13.75 and tp <= -1.6:
            return i, tp
        if not (-14.25 <= i <= -13.75):
            gain += (-14.0 - i) * 0.90
        if tp > -1.6:
            limit -= max(0.2, tp + 1.6 + 0.15)
    raise SystemExit(f"AAC level still outside -14.0±0.5 / ≤-1.6 dBTP: {last}")


def dark_run(path: Path, report: Path) -> dict:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", "fps=30,scale=90:160,format=gray", "-f", "rawvideo", "-",
    ])
    n = 90 * 160
    frames = np.frombuffer(raw, dtype=np.uint8)
    count = frames.size // n
    frames = frames[: count * n].reshape(count, n)
    dark = (frames < 20).mean(axis=1) > 0.85
    run_len = worst = 0
    hits = []
    for i, flag in enumerate(dark):
        if flag:
            run_len += 1
            worst = max(worst, run_len)
            if run_len == 3:
                hits.append(round(i / 30.0, 3))
        else:
            run_len = 0
    verdict = "PASS" if not hits else "FAIL"
    report.write_text(f"dark-run {verdict}\nframes {count}\nworst_run {worst}\nhits_at_s {hits}\n")
    return {"verdict": verdict, "frames": count, "worst_run": worst, "hits": hits}


def black_edge(path: Path, report: Path) -> dict:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", "fps=30,scale=90:160,format=gray", "-f", "rawvideo", "-",
    ])
    n = 90 * 160
    frames = np.frombuffer(raw, dtype=np.uint8)
    count = frames.size // n
    frames = frames[: count * n].reshape(count, n)
    dark = (frames < 20).mean(axis=1) > 0.30
    run_len = worst = 0
    hits = []
    for i, flag in enumerate(dark):
        if flag:
            run_len += 1
            worst = max(worst, run_len)
            if run_len == 15:
                hits.append(round(i / 30.0, 3))
        else:
            run_len = 0
    verdict = "PASS" if not hits else "FAIL"
    report.write_text(
        f"black-edge {verdict}\nframes {count}\nworst_run {worst}\nhits_at_s {hits}\n"
        f"max_frac {float((frames < 20).mean(axis=1).max()):.3f}\n"
    )
    return {"verdict": verdict, "frames": count, "worst_run": worst, "hits": hits}


def ocr_every_third(path: Path, report: Path) -> dict:
    frames = WORK / "ocr_jpg"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path),
         "-vf", "fps=10,scale=720:1280", str(frames / "%05d.jpg")])
    paths = sorted(frames.glob("*.jpg"))
    tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
    url = re.compile(r"(https?://|www\.|\.int\b|\.gov\b|esa\.int)", re.I)
    copyright_re = re.compile(r"(copyright|all rights reserved|©\s*(?:19|20)\d{2})", re.I)
    file_tag = re.compile(r"[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b", re.I)
    ids = ("bsjwicbb7py", "j0935", "js6eqj8qdi8")

    def one(p: Path) -> tuple[str, str]:
        got = subprocess.run([tess, str(p), "stdout", "--psm", "6", "-l", "eng"],
                             capture_output=True, text=True)
        return p.name, (got.stdout or "").replace("\n", " ").strip()

    hits: list[str] = []
    kept: list[str] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for name, said in pool.map(one, paths):
            if not said:
                continue
            kept.append(f"{name}\t{said}")
            norm = re.sub(r"[^a-z0-9.]", "", said.lower())
            if url.search(said) or copyright_re.search(said) or file_tag.search(said) or any(bit in norm for bit in ids):
                hits.append(f"{name}\t{said}")
    report.write_text(
        f"engine tesseract\nframes {len(paths)}\nhits {len(hits)}\n"
        + "\n".join(hits) + "\n---\n" + "\n".join(kept) + "\n"
    )
    shutil.rmtree(frames, ignore_errors=True)
    verdict = "PASS" if not hits else "FAIL"
    return {"verdict": verdict, "frames": len(paths), "hits": len(hits)}


def publish(paths: list[Path]) -> None:
    present = [src for src in paths if src.exists()]
    missing = [src.name for src in paths if not src.exists()]
    if missing:
        raise SystemExit(f"publish missing {missing}")
    manifest = {"job": "J0935", "stem": STEM, "files": {src.name: sha256(src) for src in present}}
    text = json.dumps(manifest, indent=2) + "\n"
    manifest_path = OUT / "sha256_manifest.json"
    manifest_path.write_text(text)
    ship = [*present, manifest_path]
    if not NAS.parent.exists():
        print("NAS not mounted; leaving the local manifest only", flush=True)
        folders = [UAT]
    else:
        folders = [UAT, NAS]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        for src in ship:
            dst = folder / src.name
            shutil.copy2(src, dst)
            if sha256(dst) != sha256(src):
                raise SystemExit(f"copy mismatch {dst}")
        print("copied", folder, flush=True)


def main() -> None:
    for p in (SHORT_VO, LONG_VO, SHORT_WORDS, LONG_WORDS, BED, GIF_SHADOW, GIF_BLADE, V19, V25, STILL_AERIAL, STILL_ROTOR, STILL_GROUND):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    srcs = {"short": read_wav(SHORT_VO), "long": read_wav(LONG_VO)}
    words = {
        "short": json.loads(SHORT_WORDS.read_text())["words"],
        "long": json.loads(LONG_WORDS.read_text())["words"],
    }
    audio, marks, cap_words = build_vo(srcs, words)
    vo_end = round(round(len(audio) / SR * FPS) / FPS, 4)
    total = round(vo_end + LOOP, 4)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    if marks["On"] > 0.15:
        raise SystemExit(f"first word at {marks['On']}s, need <=0.15")
    if marks["Mars"] > 1.50 or marks["seventy"] > 1.50:
        raise SystemExit(f"Mars {marks['Mars']}s seventy {marks['seventy']}s, need both <=1.50")
    if marks["lift_end"] > TITLE_IN:
        print(f"NOTE lift_end at {marks['lift_end']}s vs title_in {TITLE_IN}s", flush=True)
    payoff_at = 0.70 * total
    if marks["y2024"] < payoff_at:
        raise SystemExit(f"2024 at {marks['y2024']}s is before 70% ({payoff_at:.2f}s)")
    if not (18.0 <= total <= 24.05):
        raise SystemExit(f"runtime {total}s outside 18-24 s")
    tail_gap = total - marks["there_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((max(1, round(total * SR) - len(audio)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    open_f = round(FIRST_CUT * FPS)
    body_f = round(vo_end * FPS) - open_f
    n = 6
    base_f, rem_f = divmod(body_f, n)
    hold = body_f / FPS / n
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.8")
    print(f"plates body={n} hold={hold:.2f}s", flush=True)

    rows = []
    print("cutting s00 frame 0 PIA24644.gif", flush=True)
    cut_open_gif(open_f / FPS, WORK / "s00.mp4")
    rows.append({
        "row": "s00", "timeline_in": 0.0, "timeline_out": round(open_f / FPS, 3),
        "source": "PIA24644.gif", "upscale": 2.0, "video": True,
        "framing": {"offset": 0.75},
    })

    # 6 distinct body plates alternating still/video/still/video/gif/still so there is never
    # a still-to-still cut and every cut is a big visual change:
    # s01: PIA24593.jpg first aerial colour image over Mars tracks (still fill)
    # s02: JPL-20210419-TECHf-0001.mp4 Flight 1 liftoff/hover (video)
    # s03: PIA24584.jpg Ingenuity rotor shadow from the air (still fit)
    # s04: JPL-20210425-TECHf-0001.mp4 Flight 3 lateral fly-in (video)
    # s05: PIA26244.gif Navcam animated missing rotor blade tip (video/gif)
    # s06: PIA26243.jpg damaged blade shadow on Mars sand (still fill)
    body_defs = [
        ("s01", "PIA24593.jpg", False, {}),
        ("s02", "JPL-20210419-TECHf-0001.mp4", True, {"offset": 18.0}),
        ("s03", "PIA24584.jpg", False, {}),
        ("s04", "JPL-20210425-TECHf-0001.mp4", True, {"offset": 14.0}),
        ("s05", "PIA26244.gif", True, {"offset": 0.5}),
        ("s06", "PIA26243.jpg", False, {}),
    ]
    t = open_f / FPS
    for i, (name, source, is_vid, framing) in enumerate(body_defs):
        f_i = base_f + (1 if i < rem_f else 0)
        length = f_i / FPS
        dest = WORK / f"{name}.mp4"
        print(f"cutting {name} {source} {length:.2f}s", flush=True)
        if source == "PIA24593.jpg":
            up = cut_still_fill(STILL_AERIAL, 0.50, 0.50, length, dest)
        elif source == "JPL-20210419-TECHf-0001.mp4":
            cut_flight_v19(18.0, length, dest)
            up = 2.0
        elif source == "PIA24584.jpg":
            up = cut_still_rotor(length, dest)
        elif source == "JPL-20210425-TECHf-0001.mp4":
            cut_flight_v25(14.0, length, dest)
            up = 2.0
        elif source == "PIA26244.gif":
            cut_blade_gif(length, dest)
            up = 1.69
        elif source == "PIA26243.jpg":
            up = cut_still_fill(STILL_GROUND, 0.55, 0.55, length, dest)
        else:
            raise SystemExit(f"unknown {source}")
        rows.append({
            "row": name, "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source, "upscale": up, "video": is_vid,
            "framing": framing,
        })
        t = round(t + length, 6)

    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines = ["file 's00.mp4'"] + [f"file '{name}.mp4'" for name, *_ in body_defs] + ["file 's_loop.mp4'"]
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_PIA24644.gif", "upscale": 2.0, "video": True,
        "framing": {"offset": 0.75},
    })

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_pngs(cap_words, vo_end)

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_i = lufs(bed_raw)
    bed_gain = (vo_i - 26.0) - bed_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={total - 0.55:.3f}:d=0.45",
         str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick),
         "-filter_complex",
         f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0:all=1[w];"
         f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(TITLE_IN * 1000)}:all=1[t];"
         f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_i = lufs(WORK / "stem_sfx_raw.wav")
    sfx_gain = (vo_i - 18.0) - sfx_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
         "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(WORK / "mix_raw.wav")])
    aac_i, aac_tp = fit_mix(WORK / "mix_raw.wav", WORK / "mix.wav")

    final = OUT / f"{STEM}.mp4"
    ff_in = ["-i", str(WORK / "picture.mp4"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "hook.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "title.png"),
             "-i", str(WORK / "mix.wav")]
    base = 4
    for c in caps:
        ff_in += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(c["png"])]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.20:.2f}:d=0.20:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={TITLE_OUT - 0.20}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
    ]
    last = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    print("encoding", len(caps), "captions", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "3:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x7", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x5", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(phone)])
    file_i, file_tp = measure_level(final)
    print(f"master ebur128 {file_i:.2f} LUFS / {file_tp:.2f} dBTP", flush=True)
    if not (-14.5 <= file_i <= -13.5) or file_tp > -1.6:
        raise SystemExit(f"master level {file_i:.2f}/{file_tp:.2f} outside -14.0±0.5 and <=-1.6")

    cuts_path = OUT / "cuts_v04.json"
    pool_path = OUT / "pool_v04.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": "PIA24644.gif", "title": "Ingenuity shadow during its third flight, moving"},
        {"file_id": "PIA24593.jpg", "title": "Ingenuity first aerial colour photograph of Mars tracks"},
        {"file_id": "JPL-20210419-TECHf-0001.mp4", "title": "Ingenuity first flight hover, Mastcam-Z"},
        {"file_id": "PIA24584.jpg", "title": "Ingenuity downward shadow from the air"},
        {"file_id": "JPL-20210425-TECHf-0001.mp4", "title": "Ingenuity third flight lateral traverse, Mastcam-Z"},
        {"file_id": "PIA26244.gif", "title": "Ingenuity Navcam sequence of its damaged rotor blade"},
        {"file_id": "PIA26243.jpg", "title": "Shadow of Ingenuity's damaged rotor blade on Mars"},
        {"file_id": "end_card_loop_PIA24644.gif", "title": "Loop back to the frame-0 Ingenuity shadow"},
    ], indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v04",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did a Helicopter Fly 72 Times on Mars?",
        "replaces_for_review": "fri13_ingenuity_72_v02 (scheduled bSjWiCbB7pY). v01, v02 and v03 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…still standing there. On Mars, it flew seventy-two.",
        "brief": {
            "frame_0": "PIA24644.gif Ingenuity shadow at 0.75 s, moving, 9:16 blur fill, no Orbit",
            "first_word_s": marks["On"],
            "surprise_s": marks["seventy"],
            "mars_s": marks["Mars"],
            "seventy_end_s": marks["seventy_end"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": round(total - marks["there_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["y2024"],
            "rpm_s": marks["rpm"],
            "lift_end_s": marks["lift_end"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "72 / FLIGHTS (yellow 72), 0-2.0 s",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "bSjWiCbB7pY",
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(meta_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr, flush=True)

    sfx = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_path), "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"), "--minutes", f"{total / 60:.3f}"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_sfx.txt").write_text(sfx.stdout + sfx.stderr)
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
         "--bed", str(BED), "--video", str(final)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_music.txt").write_text(music.stdout + music.stderr)
    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v04.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v04.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v04")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v04.txt").write_text(pqa.stdout + pqa.stderr)
    dark = dark_run(final, OUT / f"{STEM}_dark.txt")
    edge = black_edge(final, OUT / f"{STEM}_black.txt")
    print("dark", dark, "black-edge", edge, flush=True)
    ocr = ocr_every_third(final, OUT / f"{STEM}_ocr.txt")
    print("ocr", ocr["verdict"], "frames", ocr["frames"], "hits", ocr["hits"], flush=True)
    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    for name, proc in (("sfx", sfx), ("music", music), ("polish", polish), ("picture_qa", pqa)):
        if proc.returncode != 0:
            print(f"--- {name} ---", flush=True)
            print((proc.stdout or "")[-2500:], (proc.stderr or "")[-1500:], flush=True)
    checks_ok = all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa))
    checks_ok = checks_ok and dark["verdict"] == "PASS" and edge["verdict"] == "PASS" and ocr["verdict"] == "PASS"
    if checks_ok:
        open_sheet = OUT / f"{STEM}_open_sheet.jpg"
        publish([
            final, phone, OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_2fps.jpg",
            open_sheet, meta_path,
        ])
    raise SystemExit(0 if checks_ok else 1)


if __name__ == "__main__":
    main()
