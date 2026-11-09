#!/usr/bin/env python3
"""J0935 — 025 Mon 9 Nov Short v04 (RULING_2026-10-26_CODEX.md response). £0 local re-cut of iyvWYFP_ETA. No upload.

Fixes over v03 per RULING_2026-10-26_CODEX.md:
1. Runtime >= 22.0 s floor (22.30 s, inside 22–24 s) using whole sentences from the
   locked 025 long VO ("That only works while power keeps coming in." at 11.0–13.4 s
   under the 9–14 s banner, then "In 2009, Spirit got stuck and couldn't catch the
   winter sun. As the days shortened, its power fell." with payoff after 14.0 s and
   at >= 70% of runtime).
2. Picture/words match: removed gale @ 20.0 s (Curiosity white rover deck). All body
   plates use neutral Martian terrain/descent windows with zero identifiable hardware
   from another rover mission.
3. Full-runtime 2 fps contact sheet: 8x6 tile (48 frames = 24.0 s) covers the entire
   22.30 s runtime including the 1.0 s loop.
4. Master-derived Whisper transcript (mon09_night_cold_v04_whisper.json/.txt) via local
   faster-whisper + full per-frame dark-run/black-edge/OCR report
   (mon09_night_cold_v04_checks.json).
5. Explicit infeasibility report in mon09_night_cold_v04_infeasibility.json and meta:
   documents why the recorded stems cannot simultaneously satisfy Ben's 26 Oct Keeper
   first-line question rule and c61's <= 1.5 s surprise target inside the 1.08x tempo
   cap without new TTS spend, so scheduled v01 (iyvWYFP_ETA) is retained unless waived.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

POOL = FILM / "07_Edit-Project/nasa_pool_v01"
VO = FILM / "10_Shorts/wed11_night_cold/wed11_night_cold_vo_v01.wav"
WORDS = FILM / "10_Shorts/wed11_night_cold/words.json"
LONG_VO = Path("/private/tmp/j0935_wed11_v03/long.wav")
LONG_WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 300.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_mon09_v04")
STEM = "mon09_night_cold_v04"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_mon09_night_cold_v04"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/mon09_night_cold_v04")
WHISPER_PY = Path("/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-09"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("MINUS", "90")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.55
MAX_PLATE = 3.55
LOOP = 1.00
XFADE = 0.012
ATEMPO = 1.08

S1_PIECES = [
    (0.00, 0.74),  # On Mars,
    (0.86, 1.52),  # the night can
    (1.62, 2.08),  # fall to
    (2.18, 2.66),  # minus
    (2.98, 3.96),  # 90 degrees.
]
# (src_name, start, end, text)
BODY = [
    ("short", 6.06, 8.14, "Batteries hate deep cold,"),
    ("short", 8.46, 10.28, "like your phone on a frozen day,"),
    ("short", 10.66, 14.34, "so rovers burn power just to keep their insides warm."),
    ("long", 157.86, 160.36, "That only works while power keeps coming in."),
    ("short", 14.66, 19.42, "In 2009, Spirit got stuck and couldn't catch the winter sun."),
    ("long", 176.44, 179.02, "As the days shortened, its power fell."),
]
MARK_SRC = {
    "On": ("s1", 0, 0.06),
    "Mars": ("s1", 0, 0.26),
    "minus": ("s1", 3, 2.20),
    "90": ("s1", 4, 3.02),
    "2009": ("body", 4, 14.98),
    "couldn't": ("body", 4, 17.74),
    "sun": ("body", 4, 19.00),
    "fell_end": ("body", 5, 178.98),
}


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
            raise SystemExit(f"expected 48 kHz stereo s16, got {w.getframerate()} {w.getnchannels()}ch")
        n = w.getnframes()
        raw = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
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


ROOM = (3.86, 4.10)


def _xfade(prev: np.ndarray, clip: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    fade_n = int(XFADE * SR)
    if fade_n > 8 and len(prev) > fade_n * 2 and len(clip) > fade_n * 2:
        n = fade_n
        ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
        prev = prev.copy()
        clip = clip.copy()
        prev[-n:] *= (1 - ramp)
        clip[:n] *= ramp
        prev[-n:] += clip[:n]
        return prev, clip[n:], n
    return prev, clip, 0


def _words_in(words_raw, a, b, start_out) -> list[dict]:
    out = []
    for w in words_raw:
        ws, we = float(w["start"]), float(w["end"])
        if a - 0.02 <= ws and we <= b + 0.04:
            out.append({
                "word": w["text"],
                "start": start_out + (ws - a),
                "end": start_out + (we - a),
            })
    return out


def _atempo(audio: np.ndarray, rate: float) -> np.ndarray:
    src_p = WORK / "_s1_in.wav"
    dst_p = WORK / "_s1_out.wav"
    write_wav(src_p, audio)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src_p), "-af", f"atempo={rate:.3f}",
         "-ar", str(SR), "-ac", "2", str(dst_p)])
    return read_wav(dst_p)


def build_vo(srcs: dict[str, np.ndarray], words_map: dict[str, list], gap_s: float) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    src = srcs["short"]
    ref = rms(src[int(6.10 * SR): int(14.20 * SR)])
    room = src[int(ROOM[0] * SR): int(ROOM[1] * SR)]
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    s1_words: list[dict] = []
    for i, (a, b) in enumerate(S1_PIECES):
        clip = src[int(a * SR): int(b * SR)].copy()
        if parts:
            parts[-1], clip, n = _xfade(parts[-1], clip)
            cursor -= n
        starts.append(cursor / SR)
        s1_words.extend(_words_in(words_map["short"], a, b, starts[-1]))
        parts.append(clip)
        cursor += len(clip)
    s1 = np.concatenate(parts, axis=0)
    s1 = _atempo(s1, ATEMPO)
    scale = 1.0 / ATEMPO
    for w in s1_words:
        w["start"] = round(w["start"] * scale, 3)
        w["end"] = round(w["end"] * scale, 3)
    s1_starts = [s * scale for s in starts]

    cap_words = list(s1_words)
    body_starts: list[float] = []
    cursor = len(s1)
    body_parts = [s1]
    for i, (sname, a, b, _label) in enumerate(BODY):
        need = int(gap_s * SR)
        tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
        if body_parts:
            body_parts[-1], tone, n = _xfade(body_parts[-1], tone)
            cursor -= n
        body_parts.append(tone)
        cursor += len(tone)
        clip = srcs[sname][int(a * SR): int(b * SR)].copy()
        if sname == "long":
            gain = float(np.clip(ref / rms(clip), 0.65, 1.65))
            clip *= gain
        body_parts[-1], clip, n = _xfade(body_parts[-1], clip)
        cursor -= n
        body_starts.append(cursor / SR)
        for w in _words_in(words_map[sname], a, b, body_starts[-1]):
            w["start"] = round(w["start"], 3)
            w["end"] = round(w["end"], 3)
            cap_words.append(w)
        body_parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(body_parts, axis=0)
    marks = {}
    for name, (kind, seg, src_t) in MARK_SRC.items():
        if kind == "s1":
            a = S1_PIECES[seg][0]
            marks[name] = round(s1_starts[seg] + (src_t - a) * scale, 3)
        else:
            a = BODY[seg][1]
            marks[name] = round(body_starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "MINUS", 150, int(W * 0.86), 8)
    y = int(H * 0.05)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 8
    centred(d, y, HOOK[1], font, YELLOW, 8)
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
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.35)
        if stop <= start:
            continue
        text = " ".join(w["word"].strip(",.?!") for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 72, int(W * 0.90), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_plate(src: Path, ss: float, length: float, vf: str, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    tail = vf + f",scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.20:.3f}",
         "-i", str(src), "-an", "-vf", tail, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_gif(length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    src = POOL / "dusk_plain/PIA26673.gif"
    vf = ("crop=576:1024:224:0,scale=1152:2048:flags=lanczos,"
          "minterpolate=fps=30:mi_mode=blend,"
          "crop=1080:1920:x='8+18*t':y='8+16*t',fps=30,setsar=1,format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", str(src), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


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
        raise SystemExit(f"no ebur128 from {path}\n{p.stderr[-800:]}")
    return integrated, peak


def lufs(path: Path) -> float:
    return measure_level(path)[0]


def frame_black(src: Path, ss: float, vf: str) -> float:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-ss", f"{ss:.2f}", "-i", str(src),
         "-vf", vf + ",scale=180:320,format=gray", "-frames:v", "1", "-f", "rawvideo", "-"])
    a = np.frombuffer(raw, dtype=np.uint8)
    n = 180 * 320
    if a.size < n:
        return 1.0
    return float((a[:n] < 20).mean())


def window_black(src: Path, ss: float, length: float, vf: str) -> float:
    worst = 0.0
    t = 0.0
    while t < max(0.05, length - 0.05):
        worst = max(worst, frame_black(src, ss + t, vf))
        t += 0.45
    return worst


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
        ok_i = -14.5 <= i <= -13.5
        ok_tp = tp <= -1.6
        if ok_i and ok_tp:
            return i, tp
        if not ok_i:
            gain += (-14.0 - i) * 0.85
        if not ok_tp:
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
    lines = [f"Master Whisper transcript ({video.name}, duration {data['duration']}s):", f"Full text: {data['text']}", "", "Segments:"]
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
    bad_re = re.compile(r"(https?://|www\.|\.com\b|\.org\b|nasa\.gov|copyright|all rights reserved|©\s*(?:19|20)\d{2}|iyvWYFP|Js6EQJ8qDi8|[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b)", re.I)
    from concurrent.futures import ThreadPoolExecutor
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
    if not VO.exists() or not LONG_VO.exists():
        raise SystemExit(f"missing VO {VO} or {LONG_VO}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    srcs = {
        "short": read_wav(VO),
        "long": read_wav(LONG_VO),
    }
    words_map = {
        "short": json.loads(WORDS.read_text())["words"],
        "long": json.loads(LONG_WORDS.read_text())["words"],
    }
    gap_s = 0.22
    audio, marks, cap_words = build_vo(srcs, words_map, gap_s)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    spoken = " ".join(w["word"] for w in cap_words)
    print("spoken:", spoken, flush=True)
    if marks["On"] > 0.15:
        raise SystemExit(f"first word at {marks['On']}s > 0.15")
    if marks["Mars"] > 1.50:
        raise SystemExit(f"Mars at {marks['Mars']}s > 1.50")
    if not (22.0 <= total <= 24.0):
        raise SystemExit(f"runtime {total}s outside 22.0–24.0 s floor")
    c_t = marks["couldn't"]
    if c_t < 0.70 * total or marks["2009"] < TITLE_OUT:
        raise SystemExit(f"2009@{marks['2009']}s or couldnt@{c_t}s violates banner/70% ({0.70*total:.2f}s)")

    tail = np.zeros((int(LOOP * SR), 2), np.float32)
    vo_path = WORK / "stem_vo.wav"
    write_wav(vo_path, np.concatenate([audio, tail], axis=0))

    # Picture: FIRST_CUT = 2.55 s, then 6 body plates <= 3.55 s each, zero Curiosity deck hardware.
    body_dur = total - LOOP - FIRST_CUT
    n = 6
    hold = body_dur / n
    if hold > 3.60:
        raise SystemExit(f"plate hold {hold:.2f}s > 3.60")
    gale = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
    edl = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
    edl_vf = "crop=495:880:712:0"
    # Neutral Martian desert & descent windows only (no rover deck at 19.7s or 108-140s).
    cycle = [
        (edl, 74.0, edl_vf, "JPL-20210222-M2020f-0001.mp4", 2.18),
        (gale, 42.0, "crop=608:1080:1200:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
        (edl, 96.0, edl_vf, "JPL-20210222-M2020f-0001.mp4", 2.18),
        (gale, 58.0, "crop=608:1080:80:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
        (edl, 154.0, edl_vf, "JPL-20210222-M2020f-0001.mp4", 2.18),
        (gale, 72.0, "crop=608:1080:656:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
    ]
    for src_p, ss, vf, source, _up in cycle:
        black = window_black(src_p, ss, hold + 0.15, vf)
        print(f"probe {source} @{ss:.0f} black {black:.1%}", flush=True)
        if black > 0.25:
            raise SystemExit(f"{source} @{ss} is {black:.0%} black")

    rows = []
    lines = []
    cut_gif(FIRST_CUT, WORK / "s00.mp4")
    lines.append("file 's00.mp4'")
    rows.append({
        "row": "s00", "timeline_in": 0.0, "timeline_out": FIRST_CUT,
        "source": "PIA26673.gif", "upscale": 2.0, "video": True,
        "framing": {"offset": 0.0},
    })
    t = FIRST_CUT
    for i in range(n):
        src_p, ss, vf, source, up = cycle[i]
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        cut_plate(src_p, ss, length, vf, WORK / f"s{i+1:02d}.mp4")
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+1:02d}", "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source, "upscale": up, "video": True,
            "framing": {"offset": ss},
        })
        t = round(t + length, 3)

    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines.append("file 's_loop.mp4'")
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_PIA26673.gif", "upscale": 2.0, "video": True,
        "framing": {"offset": 0.0},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_pngs(cap_words, vo_end)

    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_i = lufs(bed_raw)
    bed_gain = (vo_i - 28.0) - bed_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={total - 0.6:.3f}:d=0.5",
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
    hook_im = Image.open(WORK / "hook.png").convert("RGBA")
    title_im = Image.open(WORK / "title.png").convert("RGBA")
    cap_layers = []
    for c in caps:
        im_c = Image.open(c["png"]).convert("RGBA")
        box = im_c.getbbox()
        if box:
            cap_layers.append((c["s"], c["e"], im_c.crop(box), box[:2]))

    def _scaled_layer(im_l: Image.Image, alpha: float) -> Image.Image:
        if alpha >= 0.99:
            return im_l
        r, g, b, a = im_l.split()
        a = a.point(lambda p, k=alpha: int(p * k))
        return Image.merge("RGBA", (r, g, b, a))

    def _paste_layer(base_im: Image.Image, layer: Image.Image, alpha: float = 1.0) -> None:
        piece = _scaled_layer(layer, alpha)
        box = piece.getbbox()
        if not box:
            return
        crop = piece.crop(box)
        base_im.paste(crop, box[:2], crop)

    frame_bytes = W * H * 3
    dec = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(WORK / "picture.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", str(WORK / "mix.wav"), "-map", "0:v", "-map", "1:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)],
        stdin=subprocess.PIPE)
    assert dec.stdout is not None and enc.stdin is not None
    f_idx = 0
    try:
        while True:
            raw = dec.stdout.read(frame_bytes)
            if len(raw) < frame_bytes:
                break
            im = Image.frombytes("RGB", (W, H), raw)
            t_cur = f_idx / FPS
            if t_cur < HOOK_END:
                fade = 1.0 if t_cur < HOOK_END - 0.20 else (HOOK_END - t_cur) / 0.20
                _paste_layer(im, hook_im, fade)
            if TITLE_IN <= t_cur < TITLE_OUT:
                inn = 1.0 if t_cur > TITLE_IN + 0.20 else (t_cur - TITLE_IN) / 0.20
                out = 1.0 if t_cur < TITLE_OUT - 0.20 else (TITLE_OUT - t_cur) / 0.20
                _paste_layer(im, title_im, min(inn, out))
            for s_t, e_t, crop_im, pos in cap_layers:
                if s_t <= t_cur < e_t:
                    im.paste(crop_im, pos, crop_im)
                    break
            enc.stdin.write(im.tobytes())
            f_idx += 1
    finally:
        enc.stdin.close()
        dec.stdout.close()
        dec.wait()
    if enc.wait() != 0:
        raise SystemExit("encode failed")

    loop = loop_measures(final)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    # 8x6 tile at 2 fps covers up to 24.0 s (full runtime + loop).
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(phone)])

    file_i, file_tp = measure_level(final)
    if not (-14.5 <= file_i <= -13.5) or file_tp > -1.6:
        raise SystemExit(f"master level {file_i:.2f}/{file_tp:.2f} outside -14.0±0.5 and <=-1.6")

    whisper_data = run_whisper_on_master(
        final, OUT / f"{STEM}_whisper.json", OUT / f"{STEM}_whisper.txt"
    )
    checks_data = run_frame_and_ocr_checks(final, OUT / f"{STEM}_checks.json")

    infeasibility = {
        "short_id": "iyvWYFP_ETA",
        "slug": "mon09_night_cold",
        "status": "INFEASIBLE_OPENING_UNDER_COMBINED_CONSTRAINTS",
        "scheduled_version_retained": "mon09_night_cold_v01 (scheduled iyvWYFP_ETA)",
        "conflict_summary": (
            "No grammatical slice of the recorded stems on disk (wed11_night_cold_vo_v01.wav "
            "or 025 long.wav) can place the numeric surprise '90' at <= 1.50 s inside the "
            "atempo <= 1.08 cap, nor combine Ben's 26 Oct Keeper line-1 question with a "
            "<= 1.50 s surprise without new TTS spend (£0 lock)."
        ),
        "available_recorded_candidates": [
            {
                "source": "wed11_night_cold_vo_v01.wav (0.04-3.92s)",
                "text": "On Mars, the night can fall to minus 90 degrees.",
                "raw_durations_s": {
                    "On Mars,": 0.60,
                    "the night can": 0.64,
                    "fall to": 0.44,
                    "minus": 0.44,
                    "90": 0.18,
                    "degrees.": 0.56,
                },
                "atempo_1_08_onset_s": {
                    "On": 0.019,
                    "Mars": 0.204,
                    "minus": 1.544,
                    "90": 1.970,
                },
                "why_fails_strict_1_5s": (
                    "Even with internal pauses closed (0.16s and 0.40s removed) and atempo=1.08 "
                    "(the Chief cap), the spoken syllables 'On Mars, the night can fall to' take "
                    "1.544 s before 'minus' and 1.970 s before '90'. Dropping 'the night can fall to' "
                    "was rejected by Chief c61 as ungrammatical ('On Mars, minus 90 degrees.')."
                ),
            },
            {
                "source": "wed11_night_cold_vo_v01.wav (21.06-23.00s + 0.86-3.92s)",
                "text": "Could a Robot Survive on Mars? The night can fall to minus 90 degrees.",
                "atempo_1_08_onset_s": {
                    "Could": 0.00,
                    "Mars": 1.41,
                    "minus": 2.98,
                    "90": 3.41,
                },
                "why_fails_strict_1_5s": (
                    "Satisfies Ben's 26 Oct Keeper question-first rule, but the question itself "
                    "occupies 1.80 s at 1.08x before the temperature clause can begin, pushing "
                    "'minus 90' to 2.98-3.41 s."
                ),
            },
            {
                "source": "025 long.wav (61.34-66.00s)",
                "text": "At the first Viking landing site, nights fell to nearly minus ninety.",
                "atempo_1_08_onset_s": {
                    "At": 0.00,
                    "minus": 3.12,
                    "ninety": 3.50,
                },
                "why_fails_strict_1_5s": (
                    "Does not name Mars in sentence 1 and places 'minus ninety' after 3.1 s."
                ),
            },
        ],
    }
    (OUT / f"{STEM}_infeasibility.json").write_text(json.dumps(infeasibility, indent=2) + "\n")

    cuts_path = OUT / "cuts_v04.json"
    pool_path = OUT / "pool_v04.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": "PIA26673.gif", "title": "Curiosity dusk clouds, moving GIF"},
        {"file_id": "JPL-20200303-MSLf-0001.mp4", "title": "Mars Gale Crater desert terrain, moving (neutral ground crops)"},
        {"file_id": "JPL-20210222-M2020f-0001.mp4", "title": "Mars descent aerial view, moving"},
        {"file_id": "end_card_loop_PIA26673.gif", "title": "Loop back to the frame-0 dusk clouds"},
    ], indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "iyvWYFP_ETA",
         "--sheet-dir", str(OUT), "--vo", str(vo_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)

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

    meta = {
        "job": "J0935",
        "version": "v04",
        "status": "INFEASIBLE_OPENING_RETAIN_V01",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "Could a Robot Survive a Night on Mars?",
        "replaces_for_review": "mon09_night_cold_v01 (scheduled iyvWYFP_ETA retained; v01/v02/v03 untouched).",
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
        "brief": {
            "frame_0": "PIA26673.gif moving dusk clouds, 9:16 crop, no Orbit",
            "first_word_s": marks["On"],
            "planet_s": marks["Mars"],
            "minus_s": marks["minus"],
            "surprise_s": marks["90"],
            "surprise_compliant_with_1_5s": False,
            "keeper_line1_question_compliant": False,
            "first_cut_s": FIRST_CUT,
            "max_plate_hold_s": round(hold, 3),
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["couldn't"],
            "payoff_vs_70pct": round(0.70 * total, 2),
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
            "rover_deck_mismatch": "fixed (removed gale @ 20.0s Curiosity deck; all 6 body plates are neutral Mars ground/descent)",
            "sheet_2fps_coverage": "8x6 tile = 48 frames (24.0s), covers full 22.30s master + loop",
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "MINUS / 90 (yellow 90), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

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
