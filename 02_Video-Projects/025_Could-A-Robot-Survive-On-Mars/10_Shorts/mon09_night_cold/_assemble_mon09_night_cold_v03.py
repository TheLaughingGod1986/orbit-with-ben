#!/usr/bin/env python3
"""J0935 c61 — 025 Mon 9 Nov Short v03. £0 local re-cut of iyvWYFP_ETA. No upload.

Chief c61 (26 Oct 2026): v02 reordered sentence 1 into "On Mars, minus 90
degrees. The night can fall…" and dropped "to". v03 puts the recorded sentence
back: "On Mars, the night can fall to minus 90 degrees." The 0.16 s and 0.40 s
pauses are closed, then sentence 1 only is sped at atempo 1.08 (the cap). The
words themselves run about 1.9 s, so "90" cannot reach 1.5 s inside that cap;
the measured time is written into the meta. Body pauses open back up so the
runtime is 18–19 s. The "In 2009" plate is a full-bleed plain-ground window,
not the Curiosity deck mosaic. v01 and v02 are not overwritten.

The film's own bed is mars-robot_score_bed_v02_full.mp3. This script does not
generate a new one.
"""
from __future__ import annotations

import hashlib
import json
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
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 300.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_mon09_v03")
STEM = "mon09_night_cold_v03"

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
MAX_PLATE = 3.60
LOOP = 1.00
XFADE = 0.012

# Sentence 1, recorded order, pauses closed. "Could a robot survive one?"
# (4.26–5.70) and "The full film…" (19.74–23.00) stay cut.
# Pieces are source spans. The 0.16 s gap (0.72–0.88) and the 0.40 s gap
# (2.62–3.02) are not in any span. Internal breaths in sentence 1 are trimmed
# too, then the whole sentence is atempo'd at ATEMPO (Chief cap 1.08).
ATEMPO = 1.08
S1_PIECES = [
    (0.00, 0.74),  # On Mars,
    (0.86, 1.52),  # the night can
    (1.62, 2.08),  # fall to
    (2.18, 2.66),  # minus
    (2.98, 3.96),  # 90 degrees.
]
BODY = [
    (6.06, 8.14, "Batteries hate deep cold,"),
    (8.46, 10.28, "like your phone on a frozen day,"),
    (10.66, 14.34, "so rovers burn power just to keep their insides warm."),
    (14.66, 19.42, "In 2009, Spirit got stuck and couldn't catch the winter sun."),
]
MARK_SRC = {
    "On": ("s1", 0, 0.06),
    "Mars": ("s1", 0, 0.26),
    "minus": ("s1", 3, 2.20),
    "90": ("s1", 4, 3.02),
    "couldn't": ("body", 3, 17.74),
    "sun": ("body", 3, 19.00),
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


ROOM = (3.86, 4.10)  # booth tone after "degrees.", before the cut question


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


def build_vo(src: np.ndarray, gap_s: float) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    """Recorded sentence 1, pauses closed, atempo 1.08, then the body with gap_s breaths."""
    words_raw = json.loads(WORDS.read_text())["words"]
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
        s1_words.extend(_words_in(words_raw, a, b, starts[-1]))
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
    for i, (a, b, _label) in enumerate(BODY):
        need = int(gap_s * SR)
        tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
        if body_parts:
            body_parts[-1], tone, n = _xfade(body_parts[-1], tone)
            cursor -= n
        body_parts.append(tone)
        cursor += len(tone)
        clip = src[int(a * SR): int(b * SR)].copy()
        body_parts[-1], clip, n = _xfade(body_parts[-1], clip)
        cursor -= n
        body_starts.append(cursor / SR)
        for w in _words_in(words_raw, a, b, body_starts[-1]):
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
            a = BODY[seg][0]
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


def cut_plate(src: Path, ss: float, length: float, vf: str, dest: Path, reverse: bool = False) -> None:
    frames = max(1, round(length * FPS))
    tail = vf + f",scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p"
    if reverse:
        tail += ",reverse"
    extra = 0.20 if not reverse else 0.05
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + extra:.3f}",
         "-i", str(src), "-an", "-vf", tail, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_gif(length: float, dest: Path, reverse: bool = False) -> None:
    """PIA26673 is 6 frames at 2 fps. Blend it up to 30 fps so the dusk clouds move."""
    frames = max(1, round(length * FPS))
    src = POOL / "dusk_plain/PIA26673.gif"
    # Slightly larger than 9:16, then a short pan, so the dusk clouds clear the
    # first-second motion warn without turning the GIF into a pushed still.
    vf = ("crop=576:1024:224:0,scale=1152:2048:flags=lanczos,"
          "minterpolate=fps=30:mi_mode=blend,"
          "crop=1080:1920:x='8+18*t':y='8+16*t',fps=30,setsar=1,format=yuv420p")
    if reverse:
        vf += ",reverse"
    run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", str(src), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def gray_frames(path: Path, ss: float, length: float) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
           "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.check_output(cmd)
    frames = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
    frames = frames[: frames.size - (frames.size % (320 * 180))]
    return frames.reshape(-1, 320, 180)


def loop_measures(video: Path) -> dict:
    length = dur(video)
    a = gray_frames(video, 0.04, 0.04)[0]
    b = gray_frames(video, max(0.0, length - 0.08), 0.04)[0]
    diff = np.abs(a - b)
    return {
        "whole": round(float(np.mean(diff)), 2),
        "masked": round(float(np.mean(diff[110:240])), 2),
    }


def lufs(path: Path) -> float:
    i, _tp = measure_level(path)
    return i


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
    """Hit AAC integrated -14.0 ±0.5 and true peak ≤ -1.6 dBTP.

    The limiter is alimiter latency=1. PCM is held about 0.4 dB under the AAC
    true peak, because the 256k encode comes back ~0.1 dB hotter.
    """
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
    raise SystemExit(f"AAC level still outside -14.0±0.5 / ≤-1.6 dBTP: {last}")


def main() -> None:
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    src = read_wav(VO)
    # Body breaths open until the cut sits in the 18–19 s band Chief asked for.
    audio = marks = cap_words = None
    gap_s = 0.20
    for gap_s in (0.20, 0.28, 0.36, 0.44, 0.52, 0.60, 0.70):
        audio, marks, cap_words = build_vo(src, gap_s)
        total_try = len(audio) / SR + LOOP
        print(f"gap {gap_s:.2f} total {total_try:.2f} 90@{marks['90']:.2f}", flush=True)
        if 18.05 <= total_try <= 18.95:
            break
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, "gap", gap_s, flush=True)
    spoken_preview = " ".join(w["word"] for w in cap_words)
    print("spoken", spoken_preview, flush=True)
    if marks["On"] > 0.15:
        raise SystemExit(f"first word at {marks['On']}s, need ≤0.15")
    if marks["Mars"] > 1.50:
        raise SystemExit(f"Mars at {marks['Mars']}s, need ≤1.50")
    if not (18.0 <= total <= 19.2):
        raise SystemExit(f"runtime {total}s outside 18–19 s")
    if marks["90"] > 1.50:
        print(f"NOTE 90 at {marks['90']}s after atempo {ATEMPO} (cap). "
              "Full sentence cannot reach 1.5 s without dropping words.", flush=True)
    couldnt = marks["couldn't"]
    if couldnt < 0.70 * total:
        raise SystemExit(f"couldn't at {couldnt}s is before 70% ({0.70 * total:.2f}s)")
    tail = np.zeros((int(LOOP * SR), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total,
        "spoken": " ".join(w["word"] for w in cap_words),
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    # Picture. First cut at 2.55 s. Later plates share the remainder, each ≤3.6 s.
    body = total - LOOP - FIRST_CUT
    n = max(3, int(np.ceil(body / MAX_PLATE - 1e-6)))
    hold = body / n
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.8")
    gale = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
    edl = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
    # The descent film has a lower bar (seam at 0.83). Crop above it.
    edl_vf = "crop=495:880:712:0"
    gale_vf_note = "per-window crops that already cleared polish on v02 / wed11"
    # v03's first auto-pick (gale @8 s, x=656) was a panorama seam (polish split panel).
    # These offsets and x crops are ones a passing cut already used.
    cycle = [
        (gale, 20.0, "crop=608:1080:656:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
        (edl, 96.0, edl_vf, "JPL-20210222-M2020f-0001.mp4", 2.18),
        (gale, 58.0, "crop=608:1080:80:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
        (edl, 154.0, edl_vf, "JPL-20210222-M2020f-0001.mp4", 2.18),
        (gale, 42.0, "crop=608:1080:1200:0", "JPL-20200303-MSLf-0001.mp4", 1.78),
    ]
    if n > len(cycle):
        raise SystemExit(f"need {n} plates, only {len(cycle)} safe windows")
    cycle = cycle[:n]
    for src_p, ss, vf, source, _up in cycle:
        black = window_black(src_p, ss, hold + 0.15, vf)
        print(f"probe {source} @{ss:.0f} black {black:.1%}", flush=True)
        if black > 0.25:
            raise SystemExit(f"{source} @{ss} is {black:.0%} black")
    _ = gale_vf_note
    rows = []
    lines = []
    print("cutting frame 0 dusk gif", flush=True)
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
        print(f"cutting s{i+1:02d} {source} @{ss} {length}s", flush=True)
        cut_plate(src_p, ss, length, vf, WORK / f"s{i+1:02d}.mp4")
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+1:02d}", "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source, "upscale": up, "video": True,
            "framing": {"offset": ss},
        })
        t = round(t + length, 3)
    print("cutting loop", flush=True)
    # Reverse the first second of the frame-0 plate. Reversing the GIF
    # itself never ends (the file loops) and the encode gets killed.
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

    if not BED.exists():
        (WORK / "NEEDS_BED.txt").write_text(
            "mars-robot_score_bed_v02_full.mp3 is not in 05_Music. "
            "Picture and stem_vo.wav are in this folder. Do not generate a new bed "
            "(ElevenLabs credit hold; Chief OK required).\n")
        print("NEEDS_BED picture+vo ready", WORK, flush=True)
        raise SystemExit(3)

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_i = lufs(bed_raw)
    bed_gain = (vo_i - 28.0) - bed_i  # quiet last words still stay 10 LU over the bed
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
    print("encoding", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "3:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x4", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(phone)])

    file_i, file_tp = measure_level(final)
    print(f"master ebur128 {file_i:.2f} LUFS / {file_tp:.2f} dBTP", flush=True)
    if not (-14.5 <= file_i <= -13.5) or file_tp > -1.6:
        raise SystemExit(f"master level {file_i:.2f}/{file_tp:.2f} outside -14.0±0.5 and ≤-1.6")

    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": "PIA26673.gif", "title": "Curiosity dusk clouds, moving GIF"},
        {"file_id": "JPL-20200303-MSLf-0001.mp4", "title": "Curiosity Gale Crater panorama, moving"},
        {"file_id": "JPL-20210222-M2020f-0001.mp4", "title": "Perseverance descent and touchdown, moving"},
        {"file_id": "end_card_loop_PIA26673.gif", "title": "Loop back to the frame-0 dusk clouds"},
    ], indent=2) + "\n")

    spoken = " ".join(w["word"] for w in cap_words)
    meta = {
        "job": "J0935",
        "version": "v03",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "Could a Robot Survive a Night on Mars?",
        "replaces_for_review": "mon09_night_cold_v01 (scheduled iyvWYFP_ETA). v01 and v02 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "brief": {
            "frame_0": "PIA26673.gif moving dusk clouds, 9:16 crop, no Orbit",
            "first_word_s": marks["On"],
            "surprise_s": marks["90"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["couldn't"],
            "surprise_note": (f"90 at {marks['90']}s after atempo {ATEMPO}. "
                              "Recorded sentence cannot reach 1.5 s inside the cap."),
            "couldnt_s": marks["couldn't"],
            "body_gap_s": gap_s,
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "MINUS / 90 (yellow 90), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "iyvWYFP_ETA",
         "--sheet-dir", str(OUT), "--vo", str(vo_path)],
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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v03.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v03.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v03")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v03.txt").write_text(pqa.stdout + pqa.stderr)
    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    raise SystemExit(0 if all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)) else 1)


if __name__ == "__main__":
    main()
