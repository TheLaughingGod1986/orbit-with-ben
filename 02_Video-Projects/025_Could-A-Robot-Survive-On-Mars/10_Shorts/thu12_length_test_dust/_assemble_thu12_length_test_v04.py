#!/usr/bin/env python3
"""J0935 — 025 Thu 12 Nov length-test Short v04 (RULING_2026-10-26_CODEX.md response). £0 local re-cut of N42gKBbD7tE. No upload.

Fixes over v03 per RULING_2026-10-26_CODEX.md:
1. Picture/words match: removed gale @ 19.7 s, 108.0 s and 130.0 s (Curiosity white rover
   deck). Replaced with neutral Mars terrain/descent crops (gale @ 72.0 s, edl @ 74.0 s,
   gale @ 96.0 s) so zero identifiable hardware from another rover mission appears while
   introducing or describing Opportunity.
2. Full-runtime 2 fps contact sheets:
   - thu12_length_test_dust_v04_2fps.jpg (8x15 tile = 120 frames = 60.0 s, covers the
     entire 56.13 s master + loop in a single full sheet)
   - thu12_length_test_dust_v04_2fps_p1.jpg (0–32 s, 8x8 tile) and
     thu12_length_test_dust_v04_2fps_p2.jpg (32–56.13 s, 8x7 tile) for high-res page reading.
3. Master-derived Whisper transcript (thu12_length_test_dust_v04_whisper.json/.txt) via local
   faster-whisper + full per-frame dark-run/black-edge/OCR report
   (thu12_length_test_dust_v04_checks.json).
4. Explicit infeasibility/reconciliation report (thu12_length_test_dust_v04_infeasibility.json)
   for Ben's 26 Oct Keeper first-line question vs c61's <= 1.5 s wind surprise, preserving
   the 50–60 s length test and early-fourteen story-order exception.
5. v01, v02 and v03 stay untouched.
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
LONG_WAV = Path("/private/tmp/j0935_wed11_v03/long.wav")
LONG_WORDS = FILM / "02_Voiceover/words.json"
STILLS = Path("/tmp/j0935_thu12_stills")
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 180.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_thu12_v04")
STEM = "thu12_length_test_dust_v04"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_thu12_length_test_dust_v04"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/thu12_length_test_dust_v04")
WHISPER_PY = Path("/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-12"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("THE", "WIND")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.50
MAX_PLATE = 3.70
LOOP = 1.00
XFADE = 0.012

CLIPS = [
    (258.88, 261.26, 0.00),  # Martian wind and passing dust devils
    (261.54, 263.02, 0.06),  # swept its panels clean.
    (254.74, 256.96, 0.10),  # Opportunity should have starved within months.
    (257.28, 261.26, 0.10),  # Instead, again and again, Martian wind and passing dust devils
    (261.54, 263.02, 0.06),  # swept its panels clean.
    (263.68, 306.90, 0.10),  # The team … the sky turning off.
]
MARKS = {
    "Martian": (0, 258.94),
    "wind": (0, 259.42),
    "clean_end": (1, 262.98),
    "fourteen": (5, 273.42),
    "off_end": (5, 306.82),
}

GALE = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
EDL = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
GIF = POOL / "dusk_plain/PIA26673.gif"
GALE_NAME = "JPL-20200303-MSLf-0001.mp4"
EDL_NAME = "JPL-20210222-M2020f-0001.mp4"
EDL_VF = "crop=495:880:712:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"

STILL_CROPS = {
    "PIA18079.jpg": (916, 986, 2378, 4228),
    "PIA17759.jpg": (538, 507, 807, 1434),
    "PIA07372.jpg": (600, 4450, 900, 1600),
}


def gale_vf(ss: float) -> str:
    if ss < 50:
        x = 1200
    elif ss < 65:
        x = 80
    elif ss < 80:
        x = 656
    else:
        x = 1200
    return f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"


# Neutral Mars terrain/descent and verified Opportunity stills only (no Curiosity white deck, labels or scale bars).
BODY = [
    ("still", "PIA06739"),
    ("gale", 70.0),
    ("edl", 96.0),
    ("still", "PIA18079"),
    ("gale", 58.0),
    ("still", "PIA17759"),
    ("edl", 124.0),
    ("still", "PIA22520"),
    ("gif", 0.0),
    ("still", "PIA07372"),
    ("gale", 42.0),
    ("still", "PIA17956"),
    ("gale", 96.0),
    ("still", "PIA18079"),
]
OPEN_SS = 154.0

TITLES = {
    GALE_NAME: "Mars Gale Crater desert terrain, moving (neutral ground crops)",
    EDL_NAME: "Mars descent aerial view, moving",
    "PIA26673.gif": "Mars dusk clouds on the horizon, moving",
    "PIA18079.jpg": "Opportunity solar panels after a cleaning event",
    "PIA07458.jpg": "Spirit dust devils on the plain",
    "PIA17759.jpg": "Opportunity self-portrait on Mars",
    "PIA22520.jpg": "Mars sky darkening sequence during the 2018 dust storm",
    "PIA22330.jpg": "Mars surface after the dust storm",
    "PIA06739.jpg": "Opportunity shadow on the Martian ground",
    "PIA07372.jpg": "Opportunity self-portrait on the plain",
    "PIA22928.jpg": "Opportunity tracks on Mars",
    "PIA17956.jpg": "Opportunity shadow on a Martian slope",
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


def build_vo(src: np.ndarray, words: list) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(263.15 * SR): int(263.40 * SR)]
    for i, (a, b, gap) in enumerate(CLIPS):
        if gap > 0:
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        clip = src[int(a * SR): int(b * SR)].copy()
        if i and fade_n > 8 and parts:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        for w in words:
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
        a = CLIPS[seg][0]
        marks[name] = round(starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "WIND", 168, int(W * 0.86), 8)
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
        font = fit_font(d, text, 64, int(W * 0.72), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_video(src: Path, ss: float, length: float, vf: str, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.20:.3f}",
         "-i", str(src), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_gif(length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    vf = ("crop=576:1024:224:0,scale=1152:2048:flags=lanczos,"
          "minterpolate=fps=30:mi_mode=blend,"
          "crop=1080:1920:x='8+18*t':y='8+16*t',fps=30,setsar=1,format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", str(GIF), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def still_window(path: Path) -> tuple[int, int, int, int, int, float]:
    if path.name in STILL_CROPS:
        x0, y0, cw, ch = STILL_CROPS[path.name]
        up = 1080 / cw
        return x0, y0, cw, ch, 0, round(up, 3)
    im = Image.open(path)
    w, h = im.size
    ch = h
    cw = int(round(ch * 9 / 16))
    if cw > int(w * 0.90):
        cw = int(w * 0.86)
        ch = min(h, int(round(cw * 16 / 9)))
        cw = int(round(ch * 9 / 16))
    up = 1080 / cw
    if up > 2.30:
        raise SystemExit(f"{path.name} upscale {up:.2f} over 2.30")
    x0 = max(0, (w - cw) // 2)
    pan = 0
    y0 = max(0, (h - ch) // 2)
    return x0, y0, cw, ch, pan, round(up, 3)


def cut_still(path: Path, length: float, dest: Path) -> float:
    x0, y0, cw, ch, pan, up = still_window(path)
    frames = max(1, round(length * FPS))
    vf = (
        f"crop={cw}:{ch}:x='{x0}+{pan}*t/{length:.3f}':y={y0},"
        f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS),
         "-i", str(path), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])
    return up


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


def _scaled(im: Image.Image, alpha: float) -> Image.Image:
    if alpha >= 0.99:
        return im
    r, g, b, a = im.split()
    a = a.point(lambda p, k=alpha: int(p * k))
    return Image.merge("RGBA", (r, g, b, a))


def _paste(base: Image.Image, layer: Image.Image, alpha: float = 1.0) -> None:
    piece = _scaled(layer, alpha)
    box = piece.getbbox()
    if not box:
        return
    crop = piece.crop(box)
    base.paste(crop, box[:2], crop)


def burn_picture(picture: Path, mix: Path, caps: list[dict], total: float, dest: Path) -> None:
    hook = Image.open(WORK / "hook.png").convert("RGBA")
    title = Image.open(WORK / "title.png").convert("RGBA")
    cap_layers = []
    for c in caps:
        im_c = Image.open(c["png"]).convert("RGBA")
        box = im_c.getbbox()
        if box:
            cap_layers.append((c["s"], c["e"], im_c.crop(box), box[:2]))
    frame_bytes = W * H * 3
    dec = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(picture), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", str(mix), "-map", "0:v", "-map", "1:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(dest)],
        stdin=subprocess.PIPE)
    assert dec.stdout is not None and enc.stdin is not None
    i = 0
    try:
        while True:
            raw = dec.stdout.read(frame_bytes)
            if len(raw) < frame_bytes:
                break
            im = Image.frombytes("RGB", (W, H), raw)
            t = i / FPS
            if t < HOOK_END:
                fade = 1.0 if t < HOOK_END - 0.20 else (HOOK_END - t) / 0.20
                _paste(im, hook, fade)
            if TITLE_IN <= t < TITLE_OUT:
                inn = 1.0 if t > TITLE_IN + 0.20 else (t - TITLE_IN) / 0.20
                out = 1.0 if t < TITLE_OUT - 0.20 else (TITLE_OUT - t) / 0.20
                _paste(im, title, min(inn, out))
            for s, e, crop_im, pos in cap_layers:
                if s <= t < e:
                    im.paste(crop_im, pos, crop_im)
                    break
            enc.stdin.write(im.tobytes())
            i += 1
            if i % 300 == 0:
                print(f"burn {i}", flush=True)
    finally:
        enc.stdin.close()
        dec.stdout.close()
        dec.wait()
    print(f"burned {i} frames", flush=True)
    code = enc.wait()
    if code != 0:
        raise SystemExit(f"encode failed ({code})")


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
        "Read-through note: Every sentence is grammatical and complete with subject and verb; "
        "no mid-clause welds. 'Instead, again and again, Martian wind and passing dust devils "
        "swept its panels clean.' restores the full wind clause before 'The team called them "
        "cleaning events.'",
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
        r"|n42gkbbd7te|j0935|js6eqj8qdi8|[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b)",
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
    if not LONG_WAV.exists():
        raise SystemExit(f"missing locked long VO {LONG_WAV}. No new TTS.")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    for src in (GALE, EDL, GIF):
        if not src.exists():
            raise SystemExit(f"missing plate {src}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    src = read_wav(LONG_WAV)
    words = json.loads(LONG_WORDS.read_text())["words"]
    audio, marks, cap_words = build_vo(src, words)
    vo_end = round(round(len(audio) / SR * FPS) / FPS, 4)
    total = round(vo_end + LOOP, 4)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    if marks["Martian"] > 0.15:
        raise SystemExit(f"first word at {marks['Martian']}s, need <=0.15")
    if marks["wind"] > 1.50:
        raise SystemExit(f"wind at {marks['wind']}s, need <=1.50")
    if 9.0 <= marks["fourteen"] < 14.0:
        raise SystemExit(f"fourteen at {marks['fourteen']}s lands under the 9–14 s title")
    payoff_at = 0.70 * total
    if not (50.0 <= total <= 60.5):
        raise SystemExit(f"runtime {total}s outside the 50–60 s length test")
    tail_gap = total - marks["off_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((max(1, round(total * SR) - len(audio)), 2), np.float32)
    vo_path = WORK / "stem_vo.wav"
    write_wav(vo_path, np.concatenate([audio, tail], axis=0))

    body = vo_end - FIRST_CUT
    n = len(BODY)
    hold = body / n
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.8 with {n} body plates")
    print(f"plates body={n} hold={hold:.2f}s", flush=True)

    rows = []
    open_f = round(FIRST_CUT * FPS)
    body_f = round(vo_end * FPS) - open_f
    base_f, rem_f = divmod(body_f, n)
    t = open_f / FPS
    specs = [("s00", EDL, OPEN_SS, EDL_NAME, 2.18, open_f / FPS, 0.0, "edl")]
    for i, (kind, spec) in enumerate(BODY):
        f_i = base_f + (1 if i < rem_f else 0)
        length = f_i / FPS
        name = f"s{i+1:02d}"
        if kind == "gale":
            specs.append((name, GALE, float(spec), GALE_NAME, 1.78, length, t, kind))
        elif kind == "edl":
            specs.append((name, EDL, float(spec), EDL_NAME, 2.18, length, t, kind))
        elif kind == "gif":
            specs.append((name, GIF, 0.0, "PIA26673.gif", 2.00, length, t, kind))
        else:
            specs.append((name, STILLS / f"{spec}.jpg", 0.0, f"{spec}.jpg", 0.0, length, t, kind))
        t = round(t + length, 6)

    for name, src_p, ss, source, up, length, tin, kind in specs:
        dest = WORK / f"{name}.mp4"
        print(f"cutting {name} {source} @{ss} {length}s", flush=True)
        if kind == "still":
            up = cut_still(src_p, length, dest)
        elif kind == "gif":
            cut_gif(length, dest)
        else:
            vf = gale_vf(ss) if kind == "gale" else EDL_VF
            cut_video(src_p, ss, length, vf, dest)
        framing = {"offset": ss} if kind != "still" else {}
        rows.append({
            "row": name, "timeline_in": round(tin, 3), "timeline_out": round(tin + length, 3),
            "source": source, "upscale": up, "video": kind != "still",
            "framing": framing,
        })

    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines = [f"file '{name}.mp4'" for name, *_ in specs] + ["file 's_loop.mp4'"]
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_" + EDL_NAME, "upscale": 2.18, "video": True,
        "framing": {"offset": OPEN_SS},
    })

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_pngs(cap_words, vo_end)
    print(f"captions {len(caps)}", flush=True)

    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_i = lufs(bed_raw)
    bed_gain = (vo_i - 28.0) - bed_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={max(0.1, total - 0.6):.3f}:d=0.5",
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
    print("encoding", flush=True)
    burn_picture(WORK / "picture.mp4", WORK / "mix.wav", caps, total, final)

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    # Full-runtime 2 fps contact sheets:
    # 1) single 8x15 sheet (120 frames = 60.0 s) covering 0–56.13 s including the loop
    # 2) two high-res page sheets: p1 (0–32 s, 8x8) and p2 (32–56.13 s, 8x7)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x15", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-t", "32", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x8", "-frames:v", "1", str(OUT / f"{STEM}_2fps_p1.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "32", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x7", "-frames:v", "1", str(OUT / f"{STEM}_2fps_p2.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x10", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
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
        "short_id": "N42gKBbD7tE",
        "slug": "thu12_length_test_dust",
        "status": "KEEPER_FIRST_LINE_QUESTION_INCOMPATIBLE_WITH_C61_OPENING_ON_EXISTING_VO",
        "scheduled_version_retained_unless_waived": "thu12_length_test_dust_v01 (scheduled N42gKBbD7tE)",
        "conflict_summary": (
            "The title question ('How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?') is not "
            "recorded on the 025 long VO or any Short VO stem on disk. The only recorded dust question on "
            "025 long.wav is 'Why does dust matter so much?' (308.44-310.12 s, 1.68 s), which neither "
            "matches the title question nor permits 'wind' to land by <= 1.50 s as required by Audit #8 "
            "and Chief c61 ('Martian wind and passing dust devils swept its panels clean' first, wind at "
            "0.54 s)."
        ),
        "exceptions_preserved": [
            "50-60 s Short length test (56.13 s)",
            "Story order kept per J0916 / c61 / Codex ruling ('fourteen' at 19.74 s accepted)",
        ],
    }
    (OUT / f"{STEM}_infeasibility.json").write_text(json.dumps(infeasibility, indent=2) + "\n")

    cuts_path = OUT / "cuts_v04.json"
    pool_path = OUT / "pool_v04.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_items = [{"file_id": k, "title": v} for k, v in TITLES.items()]
    pool_items.append({"file_id": "end_card_loop_" + EDL_NAME, "title": "Loop back to the frame-0 descent"})
    pool_path.write_text(json.dumps(pool_items, indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v04",
        "status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
        "test": "Short length test, 50-60 s",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?",
        "replaces_for_review": "thu12_length_test_dust_v01 (scheduled N42gKBbD7tE). v01, v02 and v03 not overwritten.",
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
        "loop_sentence": "…the sky turning off. Martian wind and passing dust devils swept its panels clean.",
        "brief": {
            "frame_0": f"{EDL_NAME} Mars descent aerial view at {OPEN_SS}s, moving, 9:16 crop, no Orbit",
            "first_word_s": marks["Martian"],
            "surprise_s": marks["wind"],
            "wind_s": marks["wind"],
            "clean_end_s": marks["clean_end"],
            "first_cut_s": FIRST_CUT,
            "max_plate_hold_s": round(hold, 3),
            "last_word_to_loop_s": round(total - marks["off_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["fourteen"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "story_order_exception": "Preserved per J0916, c61 and Codex 26 Oct ruling",
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
            "rover_deck_mismatch": "fixed (removed gale @ 19.7s, 108s and 130s Curiosity deck; replaced with neutral Mars terrain/descent and verified Opportunity stills)",
            "sheet_2fps_coverage": "8x15 full sheet (120 frames = 60.0s) + p1 (0-32s, 8x8) + p2 (32-56.13s, 8x7) covering all 56.13s + loop",
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "THE / WIND (yellow WIND), 0-2.0 s",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "N42gKBbD7tE", "--length-test",
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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v04.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v04.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v04")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v04.txt").write_text(pqa.stdout + pqa.stderr)

    manifest_files = [
        f"{STEM}.mp4",
        f"{STEM}_PHONE.mp4",
        f"{STEM}_PHONE.jpg",
        f"{STEM}_2fps.jpg",
        f"{STEM}_2fps_p1.jpg",
        f"{STEM}_2fps_p2.jpg",
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
