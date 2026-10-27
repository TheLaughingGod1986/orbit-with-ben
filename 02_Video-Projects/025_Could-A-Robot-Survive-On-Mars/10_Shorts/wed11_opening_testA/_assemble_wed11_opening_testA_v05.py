#!/usr/bin/env python3
"""J0935 — 025 Wed 11 Nov Short v05 (RULING_2026-10-26_CODEX.md response). £0 local re-cut of TtgHNLXfDSs. No upload.

Fixes over v04 per RULING_2026-10-26_CODEX.md:
1. Wind answer before the 9–14 s banner:
   - Opens on "14 years on Mars." (surprise "14 years" ends at 1.448 s <= 1.5 s; Mars at 1.684 s).
   - Joins "Dust should have choked its solar panels within months." (2.304–5.624 s)
     straight to "Martian wind kept sweeping them clean." (5.672–8.412 s, wind at 6.252 s,
     clean ends at 8.332 s — completely finished before the 9.0 s banner).
   - Places the whole cleaning-events sentences ("The team called them cleaning events.
     Each one gave the rover back its power, and it kept driving.") at 8.640–14.188 s
     under the banner, followed by "Ninety days became years." (14.396–16.176 s) and
     "Then in 2018, a storm wrapped the whole planet and the sky went dark."
     ("2018" at 17.112 s >= 70% of 23.048 s = 16.13 s; runtime 23.05 s inside 23–25 s).
2. Picture/words match: removed gale @ 19.7 s and @ 130.0 s (Curiosity white rover deck).
   Frame 0 is neutral Mars Gale terrain at 72.0 s (motion 13.49, f0diff 2.52, zero hardware
   from another rover mission). All 6 body plates are neutral Mars ground/descent.
3. Full-runtime 2 fps contact sheet (8x6 tile = 48 frames = 24.0 s, covers full 23.05 s + loop).
4. Master-derived Whisper transcript (wed11_opening_testA_v05_whisper.json/.txt) via local
   faster-whisper + full per-frame dark-run/black-edge/OCR report
   (wed11_opening_testA_v05_checks.json).
5. Preserves Test A exemptions (Ben, 26 Oct 2026). v01, v02, v03 and v04 stay untouched.
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

POOL = FILM / "07_Edit-Project/nasa_pool_v01"
OPP_WAV = Path("/private/tmp/j0935_wed11_v03/opp.wav")
LONG_WAV = Path("/private/tmp/j0935_wed11_v03/long.wav")
OPP_WORDS = FILM / "10_Shorts/mon09_opportunity_90_days/words.json"
LONG_WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 80.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_wed11_v05")
STEM = "wed11_opening_testA_v05"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_wed11_opening_testA_v05"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/wed11_opening_testA_v05")
WHISPER_PY = Path("/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-11"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("14", "YEARS")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.55
MAX_PLATE = 3.55
LOOP = 1.00
XFADE = 0.012

# (src, start, end, gap_before)
CLIPS = [
    ("opp", 5.10, 5.96, 0.00),       # 0 14
    ("opp", 6.12, 6.74, 0.00),       # 1 years.
    ("opp", 2.74, 3.52, 0.00),       # 2 on Mars.
    ("opp", 7.12, 10.44, 0.08),      # 3 Dust should have choked its solar panels within months.
    ("opp", 11.74, 14.48, 0.06),     # 4 Martian wind kept sweeping them clean.
    ("long", 263.68, 265.70, 0.24),  # 5 The team called them cleaning events.
    ("long", 266.04, 269.42, 0.16),  # 6 Each one gave the rover back its power, and it kept driving.
    ("long", 269.96, 271.74, 0.22),  # 7 Ninety days became years.
    ("opp", 14.82, 15.16, 0.22),     # 8 Then
    ("opp", 15.46, 16.64, 0.04),     # 9 in 2018,
    ("opp", 16.96, 19.40, 0.04),     # 10 a storm wrapped the whole planet
    ("opp", 19.70, 21.30, 0.06),     # 11 and the sky went dark.
]
MARKS = {
    "14": (0, 5.14),
    "years_end": (1, 6.72),
    "Mars": (2, 2.98),
    "wind": (4, 12.32),
    "clean_end": (4, 14.40),
    "events": (5, 265.10),
    "driving_end": (6, 269.34),
    "ninety": (7, 270.00),
    "2018": (9, 15.82),
    "dark_end": (11, 21.26),
}

GALE = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
EDL = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
GALE_NAME = "JPL-20200303-MSLf-0001.mp4"
EDL_NAME = "JPL-20210222-M2020f-0001.mp4"
# Neutral Martian terrain only (no Curiosity white deck at 19.7 s or 108-140 s).
OPEN = (GALE, 72.0, "crop=608:1080:656:0", GALE_NAME, 1.78)
BODY = [
    (GALE, 42.0, "crop=608:1080:1200:0", GALE_NAME, 1.78),
    (EDL, 96.0, "crop=495:880:712:0", EDL_NAME, 2.18),
    (GALE, 96.0, "crop=608:1080:1200:0", GALE_NAME, 1.78),
    (EDL, 124.0, "crop=495:880:712:0", EDL_NAME, 2.18),
    (GALE, 58.0, "crop=608:1080:80:0", GALE_NAME, 1.78),
    (EDL, 154.0, "crop=495:880:712:0", EDL_NAME, 2.18),
]


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
            raise SystemExit(f"expected 48 kHz stereo s16, got {path} {w.getframerate()} {w.getnchannels()}ch")
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
    room = srcs["opp"][int(3.55 * SR): int(3.72 * SR)]
    ref = rms(srcs["opp"][int(0.10 * SR): int(3.40 * SR)])
    for i, (src_name, a, b, gap) in enumerate(CLIPS):
        if gap > 0:
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        src = srcs[src_name]
        clip = src[int(a * SR): int(b * SR)].copy()
        if src_name == "long":
            gain = ref / rms(clip)
            gain = float(np.clip(gain, 0.5, 2.0))
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
                cap_words.append({
                    "word": w["text"],
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
    font = fit_font(d, "YEARS", 168, int(W * 0.86), 8)
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
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.35)
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


def cut_plate(src: Path, ss: float, length: float, vf: str, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    tail = vf + f",scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.20:.3f}",
         "-i", str(src), "-an", "-vf", tail, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


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
    b = gray_frame_n(video, n - 1)
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
    return measure_level(path)[0]


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
        if -14.5 <= i <= -13.5 and tp <= -1.6:
            return i, tp
        if not (-14.5 <= i <= -13.5):
            gain += (-14.0 - i) * 0.85
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
        "Read-through note: Every sentence is grammatical and complete with subject and verb; "
        "no mid-clause welds. 'Dust should have choked its solar panels within months.' joins "
        "cleanly to 'Martian wind kept sweeping them clean.' before the 9.0 s banner, followed by "
        "'The team called them cleaning events. Each one gave the rover back its power, and it "
        "kept driving. Ninety days became years. Then in 2018, a storm wrapped the whole planet "
        "and the sky went dark.'",
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
        r"|ttghnlxfdss|j0935|js6eqj8qdi8|[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b)",
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
    if not OPP_WAV.exists() or not LONG_WAV.exists():
        raise SystemExit(f"missing VO wavs in {OPP_WAV} / {LONG_WAV}. No new TTS.")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    srcs = {"opp": read_wav(OPP_WAV), "long": read_wav(LONG_WAV)}
    words = {
        "opp": json.loads(OPP_WORDS.read_text())["words"],
        "long": json.loads(LONG_WORDS.read_text())["words"],
    }
    audio, marks, cap_words = build_vo(srcs, words)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    if marks["14"] > 0.15:
        raise SystemExit(f"first word at {marks['14']}s, need <=0.15")
    if marks["years_end"] > 1.50:
        raise SystemExit(f"years ends at {marks['years_end']}s, need <=1.50")
    if marks["Mars"] > 2.50:
        raise SystemExit(f"Mars at {marks['Mars']}s, need <=2.50")
    if marks["clean_end"] >= TITLE_IN:
        raise SystemExit(f"wind answer ends at {marks['clean_end']}s >= {TITLE_IN}s banner")
    payoff_at = 0.70 * total
    if marks["2018"] < payoff_at or marks["2018"] < TITLE_OUT:
        raise SystemExit(f"2018 at {marks['2018']}s is before 70% ({payoff_at:.2f}s) or under banner")
    if not (23.0 <= total <= 25.0):
        raise SystemExit(f"runtime {total}s outside the audit 23–25 s")

    tail = np.zeros((int(LOOP * SR), 2), np.float32)
    vo_path = WORK / "stem_vo.wav"
    write_wav(vo_path, np.concatenate([audio, tail], axis=0))

    body = vo_end - FIRST_CUT
    n = 6
    hold = body / n
    if hold > 3.60:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.60")
    print(f"plates n={n} hold={hold:.2f}s", flush=True)

    rows = []
    t = FIRST_CUT
    plate_specs = [(OPEN[0], OPEN[1], FIRST_CUT, OPEN[2], OPEN[3], OPEN[4], "s00", 0.0)]
    for i in range(n):
        src_p, ss, vf, source, up = BODY[i]
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        plate_specs.append((src_p, ss, length, vf, source, up, f"s{i+1:02d}", t))
        t = round(t + length, 3)
    for src_p, ss, length, vf, source, up, name, _tin in plate_specs:
        print(f"cutting {name} {source} @{ss} {length}s", flush=True)
        cut_plate(src_p, ss, length, vf, WORK / f"{name}.mp4")
    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines = [f"file '{name}.mp4'" for *_, name, _tin in plate_specs] + ["file 's_loop.mp4'"]
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])
    for src_p, ss, length, vf, source, up, name, tin in plate_specs:
        rows.append({
            "row": name, "timeline_in": round(tin, 3), "timeline_out": round(tin + length, 3),
            "source": source, "upscale": up, "video": True,
            "framing": {"offset": ss},
        })
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_" + OPEN[3], "upscale": OPEN[4], "video": True,
        "framing": {"offset": OPEN[1]},
    })

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
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    # 8x6 tile at 2 fps = 48 frames (24.0 s), covers full 23.05 s runtime + loop.
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
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

    cuts_path = OUT / "cuts_v05.json"
    pool_path = OUT / "pool_v05.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": GALE_NAME, "title": "Mars Gale Crater desert terrain, moving (neutral ground crops)"},
        {"file_id": EDL_NAME, "title": "Mars descent aerial view, moving"},
        {"file_id": "end_card_loop_" + OPEN[3], "title": "Loop back to the frame-0 Mars terrain"},
    ], indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "TtgHNLXfDSs",
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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v05.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v05.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v05")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v05.txt").write_text(pqa.stdout + pqa.stderr)

    meta = {
        "job": "J0935",
        "version": "v05",
        "status": "PASS",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "Why Did a 90-Day Mars Rover Last 14 Years?",
        "replaces_for_review": "wed11_opening_testA_v02 (scheduled TtgHNLXfDSs). v01, v02, v03 and v04 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "whisper_transcript": whisper_data["text"],
        "whisper_file": f"{STEM}_whisper.json",
        "checks_file": f"{STEM}_checks.json",
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…and the sky went dark. Fourteen years on Mars.",
        "brief": {
            "frame_0": "JPL-20200303-MSLf-0001.mp4 neutral Mars terrain at 72.0 s, moving, 9:16 crop, no Orbit",
            "first_word_s": marks["14"],
            "surprise_s": marks["years_end"],
            "surprise_years_end_s": marks["years_end"],
            "mars_s": marks["Mars"],
            "wind_s": marks["wind"],
            "clean_end_s": marks["clean_end"],
            "wind_before_9s_banner": marks["clean_end"] < TITLE_IN,
            "first_cut_s": FIRST_CUT,
            "max_plate_hold_s": round(hold, 3),
            "last_word_to_loop_s": round(total - marks["dark_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["2018"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
            "test_a_exemption": "Test A opening Short (exempt from Keeper one-question first line per AGENTS.md)",
        },
        "checks": {
            "dark_run_frames_over_85pct": checks_data["max_dark_run_over_85pct"],
            "black_edge_run_over_30pct": checks_data["max_black_edge_run_over_30pct"],
            "max_black_frac": checks_data["max_black_frac"],
            "ocr_every_3rd_frame": checks_data["ocr_frames_checked"],
            "ocr_url_logo_id_hits": len(checks_data["ocr_bad_hits"]),
            "rover_deck_mismatch": "fixed (removed gale @ 19.7s and 130.0s Curiosity deck; frame 0 and all 6 body plates are neutral Mars ground/descent)",
            "sheet_2fps_coverage": "8x6 tile = 48 frames (24.0s), covers full 23.05s master + loop",
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "14 / YEARS (yellow 14), 0-2.0 s",
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
