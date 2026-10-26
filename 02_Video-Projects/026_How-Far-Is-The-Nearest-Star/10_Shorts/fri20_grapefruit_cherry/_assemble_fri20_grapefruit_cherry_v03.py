#!/usr/bin/env python3
"""J0936 c59 — 026 Fri 20 Nov Short v03. £0 local re-cut of A6TW_6CXhcs. No upload.

v02 (15.07 s) stays untouched. v03 opens the pauses to about 0.25 s and splices
the locked long VO ("Proxima Centauri." / "four point two four light-years away.")
so the runtime is 18–20 s and "four thousand kilometers" lands at or after 70%,
clear of the 9–14 s title. The cherry line sits on a star field, not the SDO Sun.
Frame 0 is the SDO flare already in motion. A scale card sits in the 16:9 band.
Level is −14.0 LUFS with true peak ≤ −1.6 dBTP. v01 is not touched.
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
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import libx264_cfr_video_args  # noqa: E402

V06 = FILM / "07_Edit-Project/026_NearestStar_v06.mp4"
VO_MP3 = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/026_NearestStar_Fri20_VO/fri20_grapefruit_cherry_vo_v01_LOCK.mp3"
)
LONG_WAV = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav"
)
SHORT_WORDS = HERE / "words.json"
LONG_WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/nearest-star_score_bed_v01_full.wav"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 180.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0936_fri20_v03")
STEM = "fri20_grapefruit_cherry_v03"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / STEM
NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / STEM

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-20"
VIDEO_ID = "A6TW_6CXhcs"
LONG_TITLE = "How Far Is the Nearest Star?"
LONG_ID = "c5AdqQsnnys"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("A", "CHERRY")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.30
LOOP = 1.00
XFADE = 0.012
UPSCALE = 1.93
BAND_Y0, BAND_H = 656, 608
# Locked by the --vo-only search (18–20 s, "four" ≥ 70% and ≥ 14.02 s).
BODY_GAP = 0.25
PAYOFF_GAP = 0.60
TAIL_GAP = 0.04
TAIL_TEMPO = 1.18

# sentence, source, start, end, role
# role "tail" is sped at TAIL_TEMPO. "payoff" is the four-thousand line.
PIECES = [
    (0, "short", 0.08, 1.08, "open"),    # Shrink the sun to
    (0, "short", 1.60, 2.52, "open"),    # a grapefruit.
    (1, "short", 3.10, 5.64, "body"),    # Earth is a pinhead fifteen meters away.
    (2, "short", 6.00, 8.02, "cherry"),  # The nearest star becomes a cherry.
    (3, "long", 35.72, 37.48, "name"),   # Proxima Centauri.
    (4, "long", 105.06, 107.78, "ly"),   # four point two four light-years away.
    (5, "short", 8.48, 9.32, "where"),   # Where is it?
    (6, "short", 9.74, 11.92, "payoff"), # About four thousand kilometers away.
    (7, "short", 12.50, 14.18, "tail"),  # Put the grapefruit in London,
    (8, "short", 14.36, 16.36, "tail"),  # and the cherry is past Cairo.
]
PAYOFF_SENTENCE = 6

# Frame 0: SDO flare mid-burst (motion ~14, black ~16%). Not used under the cherry.
FRAME0 = (412.00, "GSFC_20160426_SDO_m12224_SolarFlare.mp4", "NASA SDO solar flare")
STAR_PLATES = [
    (98.50, "uhd_bt_paranal_07.mp4", "ESO Paranal night-sky time-lapse"),
    (69.20, "bt_lasilla_crux.mp4", "ESO La Silla Crux time-lapse"),
]
OTHER_PLATES = [
    (157.00, "vltfromvistatimelapse.mp4", "ESO VLT from Vista time-lapse"),
    (18.00, "uhd_bt_paranal_06.mp4", "ESO Paranal observatory time-lapse"),
    (168.00, "vltfromvistatimelapse.mp4", "ESO VLT from Vista time-lapse, later window"),
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


def centred(draw, y, text, font, fill, stroke):
    probe = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (probe[2] - probe[0])) // 2 - probe[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return draw.textbbox((x, y), text, font=font, stroke_width=stroke)


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise SystemExit(f"expected 48 kHz stereo s16, got {w.getframerate()} {w.getnchannels()}ch {path}")
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


def rms(clip: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(clip)) + 1e-12))


def atempo(clip: np.ndarray, rate: float) -> np.ndarray:
    if abs(rate - 1.0) < 0.005 or len(clip) < 8:
        return clip
    n = max(8, int(round(len(clip) / rate)))
    idx = np.linspace(0, len(clip) - 1, n)
    i0 = np.floor(idx).astype(np.int32)
    i1 = np.minimum(i0 + 1, len(clip) - 1)
    frac = (idx - i0).astype(np.float32)[:, None]
    return clip[i0] * (1 - frac) + clip[i1] * frac


def load_words(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    return data["words"] if isinstance(data, dict) else data


def build_vo(banks: dict[str, np.ndarray], word_banks: dict[str, list[dict]],
             body_gap: float, payoff_gap: float, tail_gap: float, tail_tempo: float):
    fade_n = int(XFADE * SR)
    room = banks["short"][int(2.60 * SR): int(2.85 * SR)]
    ref = rms(banks["short"][int(0.20 * SR): int(2.40 * SR)])
    parts: list[np.ndarray] = []
    cap_words: list[dict] = []
    spans: dict[str, tuple[float, float]] = {}
    marks: dict[str, float] = {}
    cursor = 0
    prev_sent = None
    for sent, source, a, b, role in PIECES:
        if prev_sent is not None and sent != prev_sent:
            gap = payoff_gap if sent == PAYOFF_SENTENCE else (tail_gap if role == "tail" else body_gap)
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        prev_sent = sent
        rate = tail_tempo if role == "tail" else 1.0
        i0, i1 = int(round(a * SR)), int(round(b * SR))
        clip = banks[source][i0:i1].copy()
        if source == "long":
            gain = ref / rms(clip)
            clip *= float(np.clip(gain, 0.4, 3.0))
        clip = atempo(clip, rate)
        if parts and fade_n > 8:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        start_s = cursor / SR
        spans[role] = (round(start_s, 3), round(start_s + (b - a) / rate, 3))
        for w in word_banks[source]:
            ws, we = float(w["start"]), float(w["end"])
            mid = (ws + we) / 2
            if a - 0.02 <= mid <= b + 0.02:
                cap_words.append({
                    "word": w["text"],
                    "start": round(start_s + (ws - a) / rate, 3),
                    "end": round(start_s + (we - a) / rate, 3),
                    "role": role,
                })
                key = w["text"].strip(".,?!").lower()
                when = round(start_s + (ws - a) / rate, 3)
                if key == "shrink" and "Shrink" not in marks:
                    marks["Shrink"] = when
                elif key == "grapefruit" and role == "open":
                    marks["grapefruit"] = when
                elif key == "sun" and role == "open":
                    marks["sun"] = when
                elif key == "star" and role == "cherry":
                    marks["star"] = when
                elif key == "cherry" and role == "cherry":
                    marks["cherry"] = when
                elif key == "proxima" and role == "name":
                    marks["Proxima"] = when
                elif key == "four" and role == "payoff":
                    marks["four"] = when
                elif key == "cairo" and role == "tail":
                    marks["Cairo"] = when
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    return audio, marks, cap_words, spans


def choose_timing(banks, word_banks) -> tuple[float, float, float, float]:
    """Body pauses stay near 0.25 s. The payoff gap and the tail pace move
    'four thousand' to ≥70% and clear of the 9–14 s title, inside 18–20 s."""
    best = None
    for payoff_gap in (0.25, 0.45, 0.65, 0.85, 1.05, 1.25):
        for tail_gap in (0.06, 0.10, 0.16, 0.25):
            for tail_tempo in (1.00, 1.06, 1.10, 1.12, 1.16):
                audio, marks, _caps, _spans = build_vo(
                    banks, word_banks, BODY_GAP, payoff_gap, tail_gap, tail_tempo)
                total = len(audio) / SR + LOOP
                four = marks.get("four")
                if four is None:
                    continue
                ok = (18.0 <= total <= 20.0 and four >= 0.70 * total - 1e-6
                      and four >= 14.02 and marks["Shrink"] <= 0.15
                      and marks["grapefruit"] <= 1.15)
                score = (
                    0 if ok else 1,
                    abs(total - 19.0),
                    abs(payoff_gap - 0.25),
                    abs(tail_tempo - 1.0),
                    abs(tail_gap - 0.25),
                )
                if best is None or score < best[0]:
                    best = (score, payoff_gap, tail_gap, tail_tempo, total, four, ok)
    if best is None or not best[6]:
        raise SystemExit(f"no timing hits 18–20 s with four at ≥70% and ≥14.02 s: {best}")
    print(f"timing payoff_gap {best[1]:.2f} tail_gap {best[2]:.2f} "
          f"tail_tempo {best[3]:.2f} total {best[4]:.2f} four {best[5]:.2f}", flush=True)
    return best[1], best[2], best[3], best[4]


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "CHERRY", 150, int(W * 0.86), 8)
    y = int(H * 0.05)
    box = centred(d, y, HOOK[0], font, WHITE, 8)
    centred(d, y + (box[3] - box[1]) + 8, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["The Nearest Star", "Is a Cherry", "Past Cairo.", "How Do We Know?"]
    font = fit_font(d, max(rows, key=len), 72, int(W * 0.90), 5)
    y = int(H * 0.06)
    for row in rows:
        box = centred(d, y, row, font, WHITE, 5)
        y = box[3] + 8
    im.save(dest)


def scale_card_png(dest: Path) -> None:
    """SUN = GRAPEFRUIT / NEAREST STAR = CHERRY / 4,000 KM inside y=656..1264."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = [
        ("SUN = GRAPEFRUIT", WHITE),
        ("NEAREST STAR = CHERRY", WHITE),
        ("4,000 KM", YELLOW),
    ]
    font = fit_font(d, "NEAREST STAR = CHERRY", 68, int(W * 0.90), 6)
    gap = d.textbbox((0, 0), "Hg", font=font)[3] + 10
    block = gap * len(rows)
    y = BAND_Y0 + (BAND_H - block) // 2
    for text, fill in rows:
        box = centred(d, y, text, font, fill, 6)
        if box[1] < BAND_Y0 or box[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"scale card outside the 16:9 band: {text} {box}")
        y = box[3] + 10
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
        font = fit_font(d, text, 68, int(W * 0.90), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def plate_vf() -> str:
    y = 42
    x = (1920 - 560) // 2
    return (
        f"crop=560:996:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1,"
        f"fps={FPS},format=yuv420p"
    )


def cut_plate(ss: float, length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    # A fast seek lands on a dark keyframe. Seek near the window, then trim exactly.
    pre = max(0.0, ss - 0.40)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{pre:.3f}", "-i", str(V06),
         "-ss", f"{ss - pre:.3f}", "-t", f"{length + 0.08:.3f}",
         "-an", "-vf", plate_vf(),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def black_frac(path: Path, t: float = 0.04) -> float:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    pix = np.frombuffer(raw, dtype=np.uint8)
    if pix.size < 180 * 320:
        return 1.0
    return float(np.mean(pix[: 180 * 320] < 30))


def gray_frames(path: Path, ss: float, length: float) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
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
    i, _tp = measure_level(path)
    return i


def limit_db(db: float) -> float:
    return 10 ** (db / 20.0)


def fit_mix(mix: Path, dest_wav: Path, dest_aac: Path) -> tuple[float, float]:
    """AAC integrated −14.0 ±0.5 and true peak ≤ −1.6 dBTP. alimiter latency=1."""
    base_i, _ = measure_level(mix)
    gain = -13.6 - base_i
    limit = -2.1
    last = None
    for _attempt in range(6):
        af = (f"volume={gain:.2f}dB,alimiter=limit={limit_db(limit):.5f}:"
              "attack=5:release=50:level=false:latency=1")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(mix), "-af", af,
             "-ar", str(SR), "-ac", "2", str(dest_wav)])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(dest_wav), "-c:a", "aac", "-b:a", "256k",
             "-ar", str(SR), "-ac", "2", str(dest_aac)])
        last = measure_level(dest_aac)
        i, tp = last
        print(f"level probe gain {gain:.2f} limit {limit:.2f} -> {i:.2f} LUFS / {tp:.2f} dBTP", flush=True)
        if -14.5 <= i <= -13.5 and tp <= -1.6:
            return i, tp
        if not (-14.5 <= i <= -13.5):
            gain += (-14.0 - i) * 0.85
        if tp > -1.6:
            limit -= max(0.2, tp + 1.6 + 0.15)
    raise SystemExit(f"AAC level still outside -14.0±0.5 / ≤-1.6 dBTP: {last}")


def picture_plan(vo_end: float, spans: dict[str, tuple[float, float]]) -> list[tuple[float, float, tuple]]:
    star0 = spans["cherry"][0]
    star1 = spans["ly"][1]
    bounds = [0.0, FIRST_CUT]
    if star0 > FIRST_CUT + 0.35:
        bounds.append(round(star0, 3))
    t = star0
    while star1 - t > 3.70:
        t = round(t + 3.40, 3)
        bounds.append(t)
    if bounds[-1] < star1 - 0.20:
        bounds.append(round(star1, 3))
    t = bounds[-1]
    while vo_end - t > 3.70:
        t = round(min(vo_end, t + 3.40), 3)
        if t not in bounds:
            bounds.append(t)
    if bounds[-1] < vo_end - 0.05:
        bounds.append(round(vo_end, 3))
    bounds = sorted(set(bounds))
    star_i = 0
    other_i = 0
    plan = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b - a < 0.40:
            continue
        if i == 0:
            src = FRAME0
        elif b > star0 + 0.05 and a < star1 - 0.05:
            src = STAR_PLATES[star_i % len(STAR_PLATES)]
            star_i += 1
        else:
            src = OTHER_PLATES[other_i % len(OTHER_PLATES)]
            other_i += 1
        plan.append((a, b, src))
    # The cherry line through the 4.24 light-year line must not sit on the Sun.
    c0, c1 = spans["cherry"][0], spans["ly"][1]
    for a, b, src in plan:
        if a < c1 - 0.05 and b > c0 + 0.05 and "SolarFlare" in src[1]:
            raise SystemExit(f"star line {a:.2f}-{b:.2f} landed on the Sun plate {src[1]}")
    return plan


def dark_run(path: Path, report: Path) -> dict:
    """Fail a run of ≥3 frames with >85% of pixels below luma 20."""
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", "fps=30,scale=90:160,format=gray", "-f", "rawvideo", "-",
    ])
    n = 90 * 160
    frames = np.frombuffer(raw, dtype=np.uint8)
    count = frames.size // n
    frames = frames[: count * n].reshape(count, n)
    dark = (frames < 20).mean(axis=1) > 0.85
    run_len = 0
    worst = 0
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
    report.write_text(
        f"dark-run {verdict}\nframes {count}\nworst_run {worst}\nhits_at_s {hits}\n"
    )
    return {"verdict": verdict, "frames": count, "worst_run": worst, "hits": hits}


def ocr_every_third(path: Path, report: Path) -> dict:
    frames = WORK / "ocr_jpg"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path),
         "-vf", "fps=10,scale=540:960", str(frames / "%05d.jpg")])
    paths = sorted(frames.glob("*.jpg"))
    tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
    url = re.compile(r"(https?://|www\.|\.int\b|\.gov\b|esa\.int)", re.I)
    copyright_re = re.compile(r"(copyright|all rights reserved|©\s*(?:19|20)\d{2})", re.I)
    file_tag = re.compile(r"[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b", re.I)
    ids = ("a6tw_6cxhcs", "j0936", "c5adqqsnnys")

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
    verdict = "PASS" if not hits and len(paths) >= 60 else "FAIL"
    return {"verdict": verdict, "frames": len(paths), "hits": len(hits)}


def copy_out(paths: list[Path]) -> None:
    manifest = {"files": []}
    for folder in (UAT, NAS):
        folder.mkdir(parents=True, exist_ok=True)
        for src in paths:
            dst = folder / src.name
            shutil.copy2(src, dst)
            if sha256(dst) != sha256(src):
                raise SystemExit(f"copy mismatch {dst}")
        print("copied", folder, flush=True)
    for src in paths:
        manifest["files"].append({"name": src.name, "sha256": sha256(src)})
    text = json.dumps(manifest, indent=2) + "\n"
    for folder in (OUT, UAT, NAS):
        (folder / "sha256_manifest.json").write_text(text)


def main() -> None:
    if not VO_MP3.exists():
        raise SystemExit(f"missing VO {VO_MP3}")
    if not LONG_WAV.exists():
        raise SystemExit(f"missing long VO {LONG_WAV}")
    if not V06.exists():
        raise SystemExit(f"missing picture {V06}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    short_wav = WORK / "short.wav"
    long_wav = WORK / "long.wav"
    if not short_wav.exists():
        # The iCloud lock mp3 is a dataless placeholder (errno 11). The v02
        # run already materialised the same take.
        cached = Path("/private/tmp/j0936_fri20_v02/lock.wav")
        if cached.exists() and cached.stat().st_size > 100_000:
            shutil.copy2(cached, short_wav)
        else:
            local_mp3 = WORK / "lock.mp3"
            run(["cp", str(VO_MP3), str(local_mp3)])
            run(["ffmpeg", "-y", "-v", "error", "-i", str(local_mp3), "-ac", "2", "-ar", str(SR), str(short_wav)])
    if not long_wav.exists():
        run(["ffmpeg", "-y", "-v", "error", "-i", str(LONG_WAV), "-ac", "2", "-ar", str(SR), str(long_wav)])
    banks = {"short": read_wav(short_wav), "long": read_wav(long_wav)}
    word_banks = {"short": load_words(SHORT_WORDS), "long": load_words(LONG_WORDS)}

    if "--search" in sys.argv:
        choose_timing(banks, word_banks)
        return

    payoff_gap, tail_gap, tail_tempo = PAYOFF_GAP, TAIL_GAP, TAIL_TEMPO
    audio, marks, cap_words, spans = build_vo(
        banks, word_banks, BODY_GAP, payoff_gap, tail_gap, tail_tempo)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spans", json.dumps(spans), flush=True)
    print("spoken", spoken, flush=True)
    if "full film" in spoken.lower():
        raise SystemExit("CTA still in the stem")
    if "size of" in spoken.lower():
        raise SystemExit("'the size of' still in the stem")
    for key in ("Shrink", "grapefruit", "star", "cherry", "Proxima", "four", "Cairo"):
        if key not in marks:
            raise SystemExit(f"missing mark {key}")
    if marks["Shrink"] > 0.15:
        raise SystemExit(f"first word at {marks['Shrink']}s")
    if marks["grapefruit"] > 1.20:
        raise SystemExit(f"grapefruit at {marks['grapefruit']}s")
    if not (18.0 <= total <= 20.05):
        raise SystemExit(f"runtime {total}s outside 18–20 s")
    if marks["four"] < 0.70 * total:
        raise SystemExit(f"four at {marks['four']}s is before 70% ({0.70 * total:.2f}s)")
    if marks["four"] < 14.00:
        raise SystemExit(f"four at {marks['four']}s is under the 9–14 s title")
    tail = np.zeros((int(round(LOOP * SR)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "spans": spans, "vo_end": vo_end, "total": total, "spoken": spoken,
        "payoff_gap": payoff_gap, "tail_gap": tail_gap, "tail_tempo": tail_tempo,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    plan = picture_plan(vo_end, spans)
    print("plan", [(round(a, 2), round(b, 2), src[1]) for a, b, src in plan], flush=True)
    rows = []
    lines = []
    for i, (a, b, src) in enumerate(plan):
        length = round(b - a, 3)
        print(f"cutting s{i:02d} {src[1]} @{src[0]} {length}s", flush=True)
        cut_plate(src[0], length, WORK / f"s{i:02d}.mp4")
        blk = black_frac(WORK / f"s{i:02d}.mp4")
        print(f"  black {blk:.3f}", flush=True)
        if i == 0 and blk > 0.30:
            raise SystemExit(f"frame 0 is {blk:.0%} black")
        if blk > 0.45:
            raise SystemExit(f"s{i:02d} is {blk:.0%} black")
        lines.append(f"file 's{i:02d}.mp4'")
        rows.append({
            "row": f"s{i:02d}", "timeline_in": round(a, 3), "timeline_out": round(b, 3),
            "source": src[1], "upscale": UPSCALE, "video": True,
            "framing": {"offset": src[0]},
        })
    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines.append("file 's_loop.mp4'")
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "loop_" + FRAME0[1], "upscale": UPSCALE, "video": True,
        "framing": {"offset": FRAME0[0]},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    scale_card_png(WORK / "card.png")
    caps = caption_pngs(cap_words, vo_end)
    card_in = round(marks["four"], 3)
    card_out = round(min(card_in + 3.50, total - 0.30), 3)
    if card_out - card_in > 4.0:
        raise SystemExit("scale card holds longer than 4 s")
    if card_in < 14.0:
        raise SystemExit("scale card overlaps the title window")

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(WORK / "stem_bed_raw.wav")])
    bed_gain = (vo_i - 28.0) - lufs(WORK / "stem_bed_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_bed_raw.wav"),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={max(0.1, total - 0.6):.3f}:d=0.5",
         str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    tick_ms = int(card_in * 1000)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick),
         "-filter_complex",
         f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0|0[w];"
         f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={tick_ms}|{tick_ms}[t];"
         f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_gain = (vo_i - 18.0) - lufs(WORK / "stem_sfx_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
         "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(WORK / "mix_raw.wav")])
    aac_i, aac_tp = fit_mix(WORK / "mix_raw.wav", WORK / "mix.wav", WORK / "mix.m4a")

    final = OUT / f"{STEM}.mp4"
    ff_in = ["-i", str(WORK / "picture.mp4"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "hook.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "title.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "card.png"),
             "-i", str(WORK / "mix.m4a")]
    base = 5
    for c in caps:
        ff_in += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(c["png"])]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.20:.2f}:d=0.20:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={TITLE_OUT - 0.20:.2f}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={card_in}:d=0.40:alpha=1,fade=t=out:st={card_out - 0.35:.2f}:d=0.35:alpha=1[cd]",
        f"[v2][cd]overlay=0:0:enable='gte(t,{card_in})*lt(t,{card_out})'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    print("encoding", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "4:a", *libx264_cfr_video_args(Fraction(FPS, 1)),
         "-c:a", "copy", "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    file_i, file_tp = measure_level(final)
    print(f"master ebur128 {file_i:.2f} LUFS / {file_tp:.2f} dBTP (probe {aac_i:.2f}/{aac_tp:.2f})", flush=True)
    if not (-14.5 <= file_i <= -13.5) or file_tp > -1.6:
        raise SystemExit(f"master level {file_i:.2f}/{file_tp:.2f} outside -14.0±0.5 and ≤-1.6")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(phone)])

    dark = dark_run(final, OUT / f"{STEM}_dark.txt")
    print("dark", dark, flush=True)
    if dark["verdict"] != "PASS":
        raise SystemExit(f"dark-run FAIL {dark}")
    ocr = ocr_every_third(final, OUT / f"{STEM}_ocr.txt")
    print("ocr", ocr["verdict"], ocr["frames"], "hits", ocr["hits"], flush=True)
    if ocr["verdict"] != "PASS":
        raise SystemExit("OCR FAIL")

    f0_black = black_frac(final, 0.04)
    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = []
    seen = set()
    for _a, _b, src in plan:
        if src[1] not in seen:
            pool.append({"file_id": src[1], "title": src[2]})
            seen.add(src[1])
    pool.append({"file_id": "loop_" + FRAME0[1], "title": "Loop back to the frame-0 SDO flare"})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "job": "J0936",
        "version": "v03",
        "ruling": "c59",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": "The Nearest Star Is a Cherry Past Cairo. How Do We Know?",
        "replaces_for_review": "fri20_grapefruit_cherry_v01 (scheduled A6TW_6CXhcs). v01 and v02 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "phone_mp4": str(phone.relative_to(REPO)),
        "phone_sha256": sha256(phone),
        "duration_s": round(dur(final), 3),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "bed": "nearest-star_score_bed_v01_full.wav from 180s",
        "brief": {
            "frame_0": "NASA SDO solar flare at v06 412.00 s, already mid-flare, 9:16 centre crop. The cherry line is on the Paranal and Crux star fields, not this plate.",
            "frame_0_black": round(f0_black, 3),
            "first_word_s": marks["Shrink"],
            "surprise_s": marks["grapefruit"],
            "subject_sun_s": marks["sun"],
            "nearest_star_s": marks["star"],
            "proxima_s": marks["Proxima"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["four"],
            "cairo_s": marks["Cairo"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "runtime_s": total,
            "longest_plate_s": round(max(b - a for a, b, _s in plan), 3),
            "loop_sentence": "…the cherry is past Cairo. Shrink the sun to a grapefruit.",
            "body_gap_s": BODY_GAP,
            "payoff_gap_s": payoff_gap,
            "tail_gap_s": tail_gap,
            "tail_tempo": tail_tempo,
            "scale_card": "SUN = GRAPEFRUIT / NEAREST STAR = CHERRY / 4,000 KM",
            "scale_card_s": [card_in, card_out],
            "dark_run": dark["verdict"],
            "ocr": ocr["verdict"],
        },
        "long_title_on_screen": {"title": "The Nearest Star Is a Cherry Past Cairo. How Do We Know?",
                                 "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "A / CHERRY (yellow CHERRY), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", VIDEO_ID,
         "--sheet-dir", str(OUT), "--vo", str(vo_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print((gate.stdout or "")[-1500:], (gate.stderr or "")[-400:], flush=True)

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
    print((sfx.stdout or sfx.stderr or "")[-500:], flush=True)
    print((music.stdout or music.stderr or "")[-500:], flush=True)
    print((polish.stdout or polish.stderr or "")[-500:], flush=True)
    print((pqa.stdout or pqa.stderr or "")[-800:], flush=True)
    codes = (gate.returncode, sfx.returncode, music.returncode, polish.returncode, pqa.returncode)
    if any(c != 0 for c in codes):
        raise SystemExit(1)

    ship = [final, phone, OUT / f"{STEM}_2fps.jpg", OUT / f"{STEM}_PHONE.jpg",
            OUT / f"{STEM}_meta.json", OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_dark.txt"]
    copy_out(ship)
    print("PASS", meta["sha256"][:12], flush=True)


if __name__ == "__main__":
    main()
