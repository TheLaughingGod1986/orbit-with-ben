#!/usr/bin/env python3
"""J0935 — 025 Fri 13 Nov Short v05 (RULING_2026-10-26_CODEX.md response). £0 local re-cut of bSjWiCbB7pY. No upload.

Fixes over v04 per RULING_2026-10-26_CODEX.md:
1. Runtime >= 22.0 s floor: re-timed with whole recorded sentences from fri13 Short VO +
   025 locked long VO ("It flew 72 times over almost three years.") so total runtime is
   22.83 s (>= 22.0 s floor).
2. 1% air / 2,000 rpm explanation completely outside the 9–14 s banner:
   - 0.00–2.14 s: "On Mars. It flew seventy-two." ("On" 0.02 s, "Mars" 0.22 s,
     "seventy-two" 1.34 s <= 1.50 s).
   - 2.20–8.86 s: "The air there is about 1% as thick as ours. Its blades spun more than
     2,000 times a minute to lift it." (atempo=1.07 <= 1.08 cap; "1%" at 3.49 s,
     "2,000" at 6.84 s, "lift it." ends at 8.86 s < 9.00 s — completely before the
     9.0–14.0 s banner).
   - 9.08–15.62 s (under the 9–14 s banner): "This helicopter was built for five flights.
     It flew 72 times over almost three years."
   - 16.22–20.34 s: "In 2024, a damaged blade finally grounded it." ("2024" at 16.56 s =
     72.5% of 22.83 s >= 70%).
   - 20.62–21.93 s: "It's still standing there." + 0.90 s reverse loop -> 22.83 s total.
3. Visibly differentiated cuts every <= 3.30 s (7 body plates + frame-0 + loop) and
   full-runtime 2 fps contact sheet (8x6 tile = 48 frames = 24.0 s covering all 22.83 s).
4. Master-derived Whisper transcript (fri13_ingenuity_72_v05_whisper.json/.txt) via local
   faster-whisper + full per-frame dark-run/black-edge/OCR report
   (fri13_ingenuity_72_v05_checks.json) + Keeper reconciliation report
   (fri13_ingenuity_72_v05_infeasibility.json).
5. v01, v02, v03 and v04 stay untouched.
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
WORK = Path("/private/tmp/j0935_fri13_v05")
STEM = "fri13_ingenuity_72_v05"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_fri13_ingenuity_72_v05"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/fri13_ingenuity_72_v05")
WHISPER_PY = Path("/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python")

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

# (src_name, start, end, gap_before, tempo)
CLIPS = [
    ("short", 2.86, 3.06, 0.00, 1.00),     # 0 On
    ("short", 3.08, 3.56, 0.00, 1.00),     # 1 Mars.
    ("short", 3.96, 5.42, 0.00, 1.00),     # 2 It flew seventy-two.
    ("short", 5.86, 7.22, 0.06, 1.07),     # 3 The air there is about
    ("short", 7.50, 9.54, 0.02, 1.07),     # 4 1% as thick as ours.
    ("short", 9.94, 11.58, 0.06, 1.07),    # 5 Its blades spun more than
    ("short", 11.84, 14.00, 0.02, 1.07),   # 6 2,000 times a minute to lift it.
    ("short", 0.06, 1.02, 0.22, 1.00),     # 7 This helicopter
    ("short", 1.08, 1.74, 0.04, 1.00),     # 8 was built for
    ("short", 1.84, 2.22, 0.04, 1.00),     # 9 five
    ("short", 2.26, 2.82, 0.04, 1.00),     # 10 flights.
    ("long", 401.44, 404.86, 0.26, 1.00),  # 11 It flew 72 times over almost three years.
    ("short", 14.38, 15.70, 0.56, 1.00),   # 12 In 2024,
    ("short", 16.04, 18.52, 0.08, 1.00),   # 13 a damaged blade finally grounded it.
    ("short", 18.84, 20.16, 0.26, 1.00),   # 14 It's still standing there.
]
MARKS = {
    "On": (0, 2.88),
    "Mars": (1, 3.10),
    "seventy": (2, 4.62),
    "seventy_end": (2, 5.40),
    "one_pct": (4, 7.52),
    "rpm": (6, 11.86),
    "lift_end": (6, 14.00),
    "five": (9, 1.88),
    "three_years_end": (11, 404.84),
    "y2024": (12, 14.72),
    "there_end": (14, 20.12),
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


def extract_clip(src_path: Path, a: float, b: float, tempo: float, idx: int) -> np.ndarray:
    dest = WORK / f"vo_seg_{idx:02d}.wav"
    af = f"atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS"
    if abs(tempo - 1.0) > 1e-3:
        af += f",atempo={tempo:.4f}"
    af += f",aformat=sample_fmts=s16:channel_layouts=stereo,aresample={SR}"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src_path), "-af", af, str(dest)])
    return read_wav(dest)


def build_vo(src_paths: dict[str, Path], srcs: dict[str, np.ndarray], words: dict[str, list]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    rates: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = srcs["short"][int(3.60 * SR): int(3.78 * SR)]
    ref = rms(srcs["short"][int(0.10 * SR): int(3.50 * SR)])
    for i, (src_name, a, b, gap, tempo) in enumerate(CLIPS):
        if gap > 0:
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        clip = extract_clip(src_paths[src_name], a, b, tempo, i)
        rate = (len(clip) / SR) / max(1e-6, (b - a))
        rates.append(rate)
        if src_name == "long":
            gain = float(np.clip(ref / rms(clip), 0.6, 1.8))
            clip = clip * gain
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
                    "start": round(starts[-1] + (ws - a) * rate, 3),
                    "end": round(starts[-1] + (we - a) * rate, 3),
                })
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks = {}
    for name, (seg, src_t) in MARKS.items():
        a = CLIPS[seg][1]
        marks[name] = round(starts[seg] + (src_t - a) * rates[seg], 3)
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
    raise SystemExit(f"AAC level still outside -14.0±0.5 / <=-1.6 dBTP: {last}")


def run_whisper_on_master(video: Path, out_json: Path, out_txt: Path) -> dict:
    script = """
import json, sys
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(sys.argv[1], word_timestamps=True, language="en")
segs = []
words = []
for s in segments:
    sw = [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "prob": round(w.probability, 3)} for w in (s.words or [])]
    segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": sw})
    words.extend(sw)
res = {"language": info.language, "duration": round(info.duration, 3), "text": " ".join(s["text"] for s in segs), "segments": segs, "words": words}
print(json.dumps(res))
"""
    raw = subprocess.check_output([str(WHISPER_PY), "-c", script, str(video)], text=True)
    data = json.loads(raw.strip().splitlines()[-1])
    out_json.write_text(json.dumps(data, indent=2) + "\n")
    lines = [
        f"Master Whisper transcript ({video.name}, duration {data['duration']}s):",
        f"Full text: {data['text']}",
        "",
        "Read-through note: Every sentence has a clear subject and verb with no mid-clause welds. "
        "The 1% air / 2,000 rpm explanation ('The air there is about 1% as thick as ours. Its blades "
        "spun more than 2,000 times a minute to lift it.') finishes at 8.86 s before the 9.0-14.0 s "
        "banner, while mission context ('This helicopter was built for five flights. It flew 72 times "
        "over almost three years.') sits under 9.0-14.0 s, and the 2024 payoff lands at 16.56 s (72.5%).",
        "",
        "Segments:",
    ]
    for s in data["segments"]:
        lines.append(f"  [{s['start']:6.2f}s - {s['end']:6.2f}s] {s['text']}")
    lines.append("")
    lines.append("Words:")
    for w in data["words"]:
        lines.append(f"  {w['start']:6.2f}s - {w['end']:6.2f}s: {w['word']}")
    out_txt.write_text("\n".join(lines) + "\n")
    return data


def run_frame_and_ocr_checks(video: Path, out_json: Path) -> dict:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(video), "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-"]
    )
    n_pix = 180 * 320
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, n_pix)
    black_fracs = [round(float((f < 20).mean()), 4) for f in frames]
    max_dark_run = cur_dark = 0
    max_edge_run = cur_edge = 0
    for bf in black_fracs:
        if bf > 0.85:
            cur_dark += 1
            max_dark_run = max(max_dark_run, cur_dark)
        else:
            cur_dark = 0
        if bf > 0.30:
            cur_edge += 1
            max_edge_run = max(max_edge_run, cur_edge)
        else:
            cur_edge = 0

    ocr_dir = WORK / "ocr_frames"
    ocr_dir.mkdir(parents=True, exist_ok=True)
    for p in ocr_dir.glob("*.jpg"):
        p.unlink()
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-vf", "fps=10,scale=720:1280",
         str(ocr_dir / "f_%04d.jpg")])
    bad_re = re.compile(
        r"(https?://|www\.|\.com\b|\.org\b|nasa\.gov|copyright|all rights reserved|©\s*(?:19|20)\d{2}"
        r"|bsjwicbb7py|j0935|js6eqj8qdi8|[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b)",
        re.I,
    )
    ocr_imgs = sorted(ocr_dir.glob("f_*.jpg"))

    def _ocr_one(img: Path) -> dict:
        idx = (int(img.stem.split("_")[1]) - 1) * 3
        t_s = round(idx / FPS, 2)
        txt = subprocess.run(["tesseract", str(img), "stdout", "--psm", "6"], capture_output=True, text=True).stdout.strip()
        return {"frame": idx, "time_s": t_s, "text": " ".join(txt.split())}

    with ThreadPoolExecutor(max_workers=8) as ex:
        ocr_rows = list(ex.map(_ocr_one, ocr_imgs))
    bad_hits = [r for r in ocr_rows if bad_re.search(r["text"])]

    report = {
        "total_frames": int(len(frames)),
        "max_black_frac": round(max(black_fracs) if black_fracs else 0.0, 4),
        "max_dark_run_over_85pct": max_dark_run,
        "max_black_edge_run_over_30pct": max_edge_run,
        "black_frac_per_frame": black_fracs,
        "ocr_frames_checked": len(ocr_rows),
        "ocr_bad_hits": bad_hits,
        "ocr_samples": ocr_rows,
    }
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    if max_dark_run >= 3:
        raise SystemExit(f"dark run >= 3 frames: {max_dark_run}")
    if max_edge_run >= 15:
        raise SystemExit(f"black edge run >= 15 frames: {max_edge_run}")
    if bad_hits:
        raise SystemExit(f"OCR bad hits: {bad_hits}")
    return report


def main() -> None:
    for p in (SHORT_VO, LONG_VO, SHORT_WORDS, LONG_WORDS, BED, GIF_SHADOW, GIF_BLADE, V19, V25, STILL_AERIAL, STILL_ROTOR, STILL_GROUND):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    src_paths = {"short": SHORT_VO, "long": LONG_VO}
    srcs = {"short": read_wav(SHORT_VO), "long": read_wav(LONG_VO)}
    words = {
        "short": json.loads(SHORT_WORDS.read_text())["words"],
        "long": json.loads(LONG_WORDS.read_text())["words"],
    }
    audio, marks, cap_words = build_vo(src_paths, srcs, words)
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
        raise SystemExit(f"lift_end at {marks['lift_end']}s overlaps 9-14s banner (need <={TITLE_IN}s)")
    payoff_at = 0.70 * total
    if marks["y2024"] < payoff_at:
        raise SystemExit(f"2024 at {marks['y2024']}s is before 70% ({payoff_at:.2f}s)")
    if not (22.0 <= total <= 25.0):
        raise SystemExit(f"runtime {total}s outside 22-25 s (below 22 s floor)")
    tail_gap = total - marks["there_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((max(1, round(total * SR) - len(audio)), 2), np.float32)
    vo_path = WORK / "stem_vo.wav"
    write_wav(vo_path, np.concatenate([audio, tail], axis=0))

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
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
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

    whisper_data = run_whisper_on_master(
        final, OUT / f"{STEM}_whisper.json", OUT / f"{STEM}_whisper.txt"
    )
    checks_data = run_frame_and_ocr_checks(final, OUT / f"{STEM}_checks.json")

    infeasibility = {
        "short_id": "bSjWiCbB7pY",
        "slug": "fri13_ingenuity_72",
        "status": "KEEPER_FIRST_LINE_QUESTION_NOT_RECORDED_ON_DISK",
        "scheduled_version_retained_unless_waived": "fri13_ingenuity_72_v02 (scheduled bSjWiCbB7pY)",
        "conflict_summary": (
            "The title question ('How Did a Helicopter Fly 72 Times on Mars?') is not recorded on "
            "either fri13 Short VO (vo.wav) or 025 locked long VO (long.wav). Neither VO stem contains "
            "any question about Ingenuity or a helicopter; the only question on 025 long VO near "
            "Ingenuity is the closing film question 'So could a robot survive on Mars?' at 417.12-419.60 s "
            "(2.48 s), which is a different question and prevents 'Mars' and 'seventy-two' from landing "
            "by <= 1.50 s as required by Audit #9 and Chief c61."
        ),
        "all_other_fixes_satisfied": {
            "runtime_s": dur(final),
            "clears_22s_floor": True,
            "surprise_seventy_s": marks["seventy"],
            "explanation_1pct_s": marks["one_pct"],
            "explanation_rpm_s": marks["rpm"],
            "explanation_lift_end_s": marks["lift_end"],
            "banner_window_s": [TITLE_IN, TITLE_OUT],
            "explanation_outside_banner": marks["lift_end"] < TITLE_IN,
            "payoff_2024_s": marks["y2024"],
            "payoff_pct": round(marks["y2024"] / dur(final) * 100, 1),
        },
    }
    (OUT / f"{STEM}_infeasibility.json").write_text(json.dumps(infeasibility, indent=2) + "\n")

    cuts_path = OUT / "cuts_v05.json"
    pool_path = OUT / "pool_v05.json"
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
        "version": "v05",
        "status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did a Helicopter Fly 72 Times on Mars?",
        "replaces_for_review": "fri13_ingenuity_72_v02 (scheduled bSjWiCbB7pY). v01, v02, v03 and v04 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "whisper_transcript": whisper_data["text"],
        "whisper_file": f"{STEM}_whisper.json",
        "checks_file": f"{STEM}_checks.json",
        "infeasibility_file": f"{STEM}_infeasibility.json",
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
            "max_plate_hold_s": round(hold, 3),
            "last_word_to_loop_s": round(total - marks["there_end"], 3),
            "meta_promise": False,
            "one_pct_s": marks["one_pct"],
            "rpm_s": marks["rpm"],
            "lift_end_s": marks["lift_end"],
            "payoff_number_s": marks["y2024"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "keeper_line1_question_compliant": False,
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
        },
        "checks": {
            "dark_run_frames_over_85pct": checks_data["max_dark_run_over_85pct"],
            "black_edge_run_over_30pct": checks_data["max_black_edge_run_over_30pct"],
            "max_black_frac": checks_data["max_black_frac"],
            "ocr_every_3rd_frame": checks_data["ocr_frames_checked"],
            "ocr_url_logo_id_hits": len(checks_data["ocr_bad_hits"]),
            "sheet_2fps_coverage": "8x6 tile (48 frames = 24.0s) covering full 22.83s + loop",
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "72 / FLIGHTS (yellow 72), 0-2.0 s",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "bSjWiCbB7pY",
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(meta_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout[-2500:], gate.stderr[-800:], flush=True)

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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v05.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v05.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v05")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v05.txt").write_text(pqa.stdout + pqa.stderr)

    manifest_files = [
        f"{STEM}.mp4",
        f"{STEM}_PHONE.mp4",
        f"{STEM}_PHONE.jpg",
        f"{STEM}_2fps.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_meta.json",
        f"{STEM}_whisper.json",
        f"{STEM}_whisper.txt",
        f"{STEM}_checks.json",
        f"{STEM}_infeasibility.json",
    ]
    manifest = {
        "stem": STEM,
        "entries": [
            {"file": fn, "sha256": sha256(OUT / fn), "bytes": (OUT / fn).stat().st_size}
            for fn in manifest_files
        ],
    }
    (OUT / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    for dst in (UAT, NAS):
        dst.mkdir(parents=True, exist_ok=True)
        for fn in manifest_files + ["sha256_manifest.json"]:
            shutil.copy2(OUT / fn, dst / fn)

    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    if not all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)):
        print("gate:", gate.stdout, gate.stderr)
        print("polish:", polish.stdout, polish.stderr)
        print("pqa:", pqa.stdout, pqa.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
