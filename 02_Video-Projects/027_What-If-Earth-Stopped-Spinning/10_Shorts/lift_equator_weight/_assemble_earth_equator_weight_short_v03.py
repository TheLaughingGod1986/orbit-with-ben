#!/usr/bin/env python3
"""J0936 c59 — 027 Mon 23 Nov Short v03. £0 local re-cut of emwQsPxnRGM. No upload.

Chief c59 fixes on top of v02:
1. Frame-0 hook ("0.5% LIGHTER / AT THE EQUATOR") fitted by bounding box to <=86%
   of frame width (both rows verified inside x=54..1026, <=90% width).
2. Equator-speed sentence spliced from the v01i master VO ahead of
   "it is faster than a jet airliner, and you feel nothing at all." so "it" has
   its subject and the 1,670 km/h ("more than one and a half thousand kilometers
   an hour") equator speed is stated before the jet airliner comparison.
3. Level: AAC integrated loudness -14.0 ±0.5 LUFS, true peak <= -1.6 dBTP
   (alimiter latency=1, verified on the encoded .mp4).
4. Deliverables: _PHONE.mp4 (720x1280) + sha256_manifest.json across repo,
   OWB UAT, and NAS. v01 and v02 are left untouched.
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

MASTER = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4"
)
WORDS = FILM / "07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json"
BED = FILM / "05_Music/earth-spin_score_take2_straight_v01j.wav"
KIT = FILM / "06_Sound-Effects/kit_v01"

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0936_equator_v03")
STEM = "earth_equator_weight_v03"

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-23"
VIDEO_ID = "emwQsPxnRGM"
LONG_TITLE = "What If Earth Stopped Spinning?"
LONG_ID = "6bbbvfCx6zY"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
CARD_IN, CARD_OUT = 2.15, 5.70
FIRST_CUT = 2.30
LOOP = 1.00
XFADE = 0.012
GAP_S = 0.08
GAPS = {1: 0.06, 2: 0.06, 4: 0.05, 5: 0.05}
ROOM = (125.55, 125.90)

# Source times on the v01i VO-only master (start, end, tempo, label).
# Splices the equator-speed sentence ahead of "it is faster than a jet airliner".
SEGMENTS = [
    (131.50, 133.68, 1.00, "you weigh about half of one percent less"),
    (128.88, 129.66, 1.00, "at the equator"),
    (134.24, 135.22, 1.00, "than at the poles,"),
    (9.74, 10.72, 1.08, "At the equator,"),
    (4.02, 6.40, 1.08, "the ground under you is carrying you east"),
    (34.96, 37.70, 1.08, "at more than one and a half thousand kilometers an hour."),
    (10.88, 12.90, 1.05, "it is faster than a jet airliner,"),
    (13.76, 14.40, 1.05, "and you"),
    (14.72, 16.08, 1.05, "feel nothing at all."),
    (137.96, 141.50, 1.05, "Earth is about forty-three kilometers wider across the equator"),
    (141.80, 143.42, 1.05, "than it is from pole to pole."),
    (128.18, 131.20, 1.00, "Because the ground at the equator swings round so fast,"),
]
MARKS = {
    "you": (0, 131.54),
    "weigh": (0, 131.68),
    "half": (0, 132.20),
    "percent": (0, 132.90),
    "less": (0, 133.36),
    "equator": (1, 129.12),
    "ground": (4, 4.16),
    "thousand": (5, 36.20),
    "airliner": (6, 12.28),
    "forty": (9, 138.76),
    "Because": (11, 128.22),
}

PLATES = [
    (322.80, "NOAA_sat_eclipse_2024_notext.webm", "NOAA GOES-16 satellite sunlit Earth disk", 0.60, True),
    (120.80, "ESO_timelapse_La_Silla.webm", "ESO La Silla Observatory night sky timelapse", 1.00, True),
    (144.20, "Foucault_pendulum_1.webm", "Foucault pendulum swinging over floor in Paris", 1.25, True),
    (226.30, "Gerst_Earth_timelapses_2017.webm", "ESA/NASA Alexander Gerst ISS Earth orbital timelapse", 0.556, True),
    (138.20, "GSFC_20171208_Archive_e002130.jpg", "NASA GSFC Blue Marble equatorial Earth", 0.763, False),
    (438.00, "epic_spin_v01.mp4", "NASA DSCOVR EPIC full-disk sunlit rotating Earth", 1.00, True),
]
FRAME0 = (28.30, "ISS_sunrise_to_sunset.ogv", "NASA ISS Sunrise to Sunset orbital Earth limb", 1.50)


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


def fit_font(draw, texts, size, max_w, stroke):
    if isinstance(texts, str):
        texts = (texts,)
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        widths = []
        for t in texts:
            box = draw.textbbox((0, 0), t, font=font, stroke_width=stroke)
            widths.append(box[2] - box[0])
        if max(widths) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, 28)


def centred(draw, y, text, font, fill, stroke):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return draw.textbbox((x, y), text, font=font, stroke_width=stroke)


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise SystemExit(f"expected 48 kHz stereo s16, got {w.getframerate()} {w.getnchannels()}ch")
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


def extract_seg(src_wav: Path, a: float, b: float, tempo: float, dest: Path) -> np.ndarray:
    af = f"atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS"
    if abs(tempo - 1.0) > 0.005:
        af += f",atempo={tempo:.4f}"
    af += f",aformat=sample_fmts=s16:channel_layouts=stereo,aresample={SR}"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", af, str(dest)])
    return read_wav(dest)


def build_vo(src_wav: Path, src: np.ndarray, words_raw: list[dict]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    rates: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(ROOM[0] * SR): int(ROOM[1] * SR)]
    for i, (a, b, tempo, _label) in enumerate(SEGMENTS):
        if i:
            need = int(GAPS.get(i, GAP_S) * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.45
            parts.append(tone)
            cursor += need
        clip = extract_seg(src_wav, a, b, tempo, WORK / f"seg_{i:02d}.wav")
        rate = (len(clip) / SR) / (b - a)
        rates.append(rate)
        if i and fade_n > 8:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip = clip.copy()
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        for w in words_raw:
            ws, we = float(w["start"]), float(w["end"])
            if a - 0.02 <= ws and we <= b + 0.04:
                cap_words.append({
                    "word": w["text"],
                    "start": round(starts[-1] + (ws - a) * rate, 3),
                    "end": round(starts[-1] + (we - a) * rate, 3),
                })
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks = {}
    for name, (seg, src_t) in MARKS.items():
        a = SEGMENTS[seg][0]
        marks[name] = round(starts[seg] + (src_t - a) * rates[seg], 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ("0.5% LIGHTER", "AT THE EQUATOR")
    max_w = int(W * 0.86)
    font = fit_font(d, rows, 110, max_w, 8)
    y = int(H * 0.05)
    b1 = centred(d, y, rows[0], font, YELLOW, 8)
    b2 = centred(d, b1[3] + 10, rows[1], font, WHITE, 8)
    for r, b in zip(rows, (b1, b2)):
        w_px = b[2] - b[0]
        if b[0] < int(W * 0.05) or b[2] > int(W * 0.95) or w_px > int(W * 0.90):
            raise SystemExit(f"hook row {r!r} clipped or over 90% width: bbox={b} width={w_px}")
    im.save(dest)
    return {
        "font_px": font.size,
        "row1_bbox": list(b1),
        "row2_bbox": list(b2),
        "max_width_frac": round(max(b1[2] - b1[0], b2[2] - b2[0]) / W, 3),
    }


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why Do You Weigh", "Less at Earth's", "Equator?"]
    font = fit_font(d, rows, 64, int(W * 0.86), 5)
    gap = d.textbbox((0, 0), "Hg", font=font)[3] + 12
    block = gap * len(rows)
    y = BAND_Y0 + (BAND_H - block) // 2
    for row in rows:
        box = centred(d, y, row, font, WHITE, 5)
        if box[1] < BAND_Y0 or box[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"title outside the 16:9 band: {row} {box}")
        y += gap
    im.save(dest)


def card_frames(dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    n = round((CARD_OUT - CARD_IN) * FPS)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    font = fit_font(probe, "0.5% LESS   AT EQUATOR", 62, int(W * 0.84), 6)
    text_h = probe.textbbox((0, 0), "Hg", font=font)[3]
    for i in range(n):
        t = CARD_IN + i / FPS
        a = min(1.0, (t - CARD_IN) / 0.35, (CARD_OUT - t) / 0.30)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = int(255 * max(0.0, a))
        label = "0.5% LESS   AT EQUATOR"
        fill = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)
        y = BAND_Y0 + (BAND_H - text_h - 36) // 2
        box = centred(d, y, label, font, fill, 6)
        if box[1] < BAND_Y0 or box[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"card outside the 16:9 band: {box}")
        prog = min(1.0, max(0.0, (t - CARD_IN) / 0.55))
        full = int(W * 0.62)
        left = (W - full) // 2
        bar_w = int(full * 0.82 * prog)
        by = box[3] + 10
        if bar_w > 4:
            d.rectangle((left, by, left + bar_w, by + 14), fill=fill)
            if by + 14 > BAND_Y0 + BAND_H:
                raise SystemExit("card bar outside the 16:9 band")
        im.save(dest / f"card_{i:04d}.png")
    return n


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
        font = fit_font(d, text, 58, int(W * 0.88), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def plate_vf() -> str:
    return f"crop=ih*9/16:ih,scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p"


def cut_plate(ss: float, length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.25:.3f}",
         "-i", str(MASTER), "-an", "-vf", plate_vf(),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def black_frac(path: Path, t: float = 0.04) -> float:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    pix = np.frombuffer(raw, dtype=np.uint8)
    frame = pix[: 180 * 320]
    return float(np.mean(frame < 30))


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


def ebur128_stats(path: Path) -> tuple[float, float]:
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    m_i = re.findall(r"I:\s*([-\d.]+)\s*LUFS", p.stderr)
    m_tp = re.findall(r"Peak:\s*([-\d.]+)\s*dBFS", p.stderr)
    if not m_i or not m_tp:
        raise SystemExit(f"no ebur128 stats from {path}")
    return float(m_i[-1]), float(m_tp[-1])


def lufs(path: Path) -> float:
    return ebur128_stats(path)[0]


def fit_mix(vo_path: Path, bed_path: Path, sfx_path: Path, total: float, out_wav: Path) -> None:
    raw_mix = WORK / "mix_pre.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(bed_path),
         "-i", str(sfx_path), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,"
         "loudnorm=I=-14.0:TP=-2.0:LRA=11[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(raw_mix)])
    gain_db = 0.0
    lim_db = -2.1
    for _ in range(6):
        run(["ffmpeg", "-y", "-v", "error", "-i", str(raw_mix),
             "-af", f"volume={gain_db:.2f}dB,alimiter=limit={lim_db:.2f}dB:level=false:attack=5:release=50:latency=1,aresample={SR}",
             "-t", f"{total:.3f}", str(out_wav)])
        aac_probe = WORK / "aac_probe.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s=64x64:r={FPS}:d={total:.3f}",
             "-i", str(out_wav), "-c:v", "libx264", "-preset", "ultrafast",
             "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-t", f"{total:.3f}", str(aac_probe)])
        i_val, tp_val = ebur128_stats(aac_probe)
        print(f"fit_mix probe: gain={gain_db:.2f}dB lim={lim_db:.2f}dB -> I={i_val:.2f} LUFS, TP={tp_val:.2f} dBTP", flush=True)
        if -14.35 <= i_val <= -13.65 and tp_val <= -1.65:
            return
        gain_db += (-14.0 - i_val)
        if tp_val > -1.65:
            lim_db -= (tp_val - (-1.85))


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
    ids = ("emwqspxnrgm", "j0936", "6bbbvfcx6zy")

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


def check_words(marks: dict, cap_words: list[dict], total: float) -> None:
    spoken = " ".join(w["word"] for w in cap_words)
    low = spoken.lower()
    if "full film" in low or "stay, and" in low or "should you worry" in low:
        raise SystemExit(f"banned line still in the stem: {spoken}")
    for req in ("ground under you is carrying you east", "one and a half thousand kilometers an hour", "faster than a jet airliner"):
        if req not in low:
            raise SystemExit(f"missing equator-speed setup {req!r} in: {spoken}")
    if marks["you"] > 0.15:
        raise SystemExit(f"first word at {marks['you']}s")
    if marks["percent"] > 1.50:
        raise SystemExit(f"percent at {marks['percent']}s, need <=1.50")
    if marks["equator"] > 2.50:
        raise SystemExit(f"equator at {marks['equator']}s, need <=2.50")
    if marks["Because"] < 0.70 * total:
        raise SystemExit(f"Because at {marks['Because']}s is before 70% ({0.70 * total:.2f})")
    if not (18.0 <= total <= 24.05):
        raise SystemExit(f"runtime {total}s outside 18–24")
    for prev, w in zip(cap_words, cap_words[1:]):
        gap = w["start"] - prev["end"]
        if gap > 0.20:
            raise SystemExit(f"pause {gap:.2f}s before {w['word']}")
    print("spoken", spoken, flush=True)


def publish(files: list[Path]) -> None:
    entries = []
    for f in files:
        entries.append({
            "name": f.name,
            "relpath": str(f.relative_to(REPO)),
            "bytes": f.stat().st_size,
            "sha256": sha256(f),
        })
    manifest = {
        "job": "J0936",
        "short_id": VIDEO_ID,
        "version": "v03",
        "files": entries,
    }
    manifest_p = OUT / "sha256_manifest.json"
    manifest_p.write_text(json.dumps(manifest, indent=2) + "\n")
    all_files = [*files, manifest_p]
    dests = [
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / STEM,
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / f"027_{STEM}",
        Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / STEM,
        Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / f"027_{STEM}",
        Path("/Volumes/data/mac-mini-archive/youtube-staging/027") / STEM,
    ]
    for dest_dir in dests:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in all_files:
            shutil.copy2(f, dest_dir / f.name)


def main() -> None:
    if not MASTER.exists():
        raise SystemExit(f"missing master {MASTER}")
    if not WORDS.exists():
        raise SystemExit(f"missing words {WORDS}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words_raw = json.loads(WORDS.read_text())
    lock = WORK / "master_vo.wav"
    if not lock.exists():
        cached = Path("/private/tmp/j0936_equator_v02/master_vo.wav")
        if cached.exists() and cached.stat().st_size > 100_000:
            shutil.copy2(cached, lock)
        else:
            print("extracting VO-only master audio", flush=True)
            run(["ffmpeg", "-y", "-v", "error", "-i", str(MASTER), "-vn",
                 "-ac", "2", "-ar", str(SR), str(lock)])
    src = read_wav(lock)
    audio, marks, cap_words = build_vo(lock, src, words_raw)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    check_words(marks, cap_words, total)
    tail = np.zeros((int(round(LOOP * SR)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    spoken = " ".join(w["word"] for w in cap_words)
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    body = vo_end - FIRST_CUT
    n = len(PLATES)
    hold = body / n
    print(f"plates {n} hold {hold:.2f}s body {body:.2f}s", flush=True)
    if hold > 3.70:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.70")
    if hold < 2.40:
        raise SystemExit(f"plate hold {hold:.2f}s under 2.40")

    print("cutting frame 0", flush=True)
    f0_ss, f0_src, f0_title, f0_up = FRAME0
    cut_plate(f0_ss, FIRST_CUT, WORK / "s00.mp4")
    blk = black_frac(WORK / "s00.mp4")
    print(f"frame0 black {blk:.3f}", flush=True)
    if blk > 0.30:
        raise SystemExit(f"frame 0 is {blk:.0%} black")

    rows = [{
        "row": "s01_iss_sunrise_limb",
        "timeline_in": 0.0, "timeline_out": FIRST_CUT,
        "source": f0_src, "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss},
    }]
    lines = ["file 's00.mp4'"]
    t = FIRST_CUT
    for i, (ss, source, _title, up, video) in enumerate(PLATES):
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        if source.endswith(".jpg") and length > 3.70:
            raise SystemExit(f"s06 still {length}s over 3.70")
        print(f"cutting s{i+2:02d} {source} @{ss} {length}s", flush=True)
        cut_plate(ss, length, WORK / f"s{i+1:02d}.mp4")
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+2:02d}",
            "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source, "upscale": up, "video": video,
            "framing": {"offset": ss},
        })
        t = round(t + length, 3)

    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines.append("file 's_loop.mp4'")
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "loop_ISS_sunrise_to_sunset.ogv", "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_info = hook_png(WORK / "hook.png")
    print("hook_info", hook_info, flush=True)
    title_png(WORK / "title.png")
    print("card frames", flush=True)
    card_frames(WORK / "card")
    caps = caption_pngs(cap_words, vo_end)
    title_out = min(TITLE_OUT, max(TITLE_IN + 1.0, vo_end - 0.4))

    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_gain = (vo_i - 22.0) - lufs(bed_raw)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.20,afade=t=out:st={max(0.1, total - 0.55):.3f}:d=0.45",
         str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick), "-i", str(tick),
         "-filter_complex",
         f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0|0[w];"
         f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(CARD_IN * 1000)}|{int(CARD_IN * 1000)}[c];"
         f"[2:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(TITLE_IN * 1000)}|{int(TITLE_IN * 1000)}[t];"
         f"[w][c][t]amix=inputs=3:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_gain = (vo_i - 18.0) - lufs(WORK / "stem_sfx_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    fit_mix(vo_path, WORK / "stem_bed.wav", WORK / "stem_sfx.wav", total, WORK / "mix.wav")

    final = OUT / f"{STEM}.mp4"
    ff_in = ["-i", str(WORK / "picture.mp4"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "hook.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "title.png"),
             "-framerate", str(FPS), "-i", str(WORK / "card" / "card_%04d.png"),
             "-i", str(WORK / "mix.wav")]
    base = 5
    for c in caps:
        ff_in += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(c["png"])]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.20:.2f}:d=0.20:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={title_out - 0.20:.2f}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{title_out})'[v2]",
        f"[3:v]setpts=PTS-STARTPTS+{CARD_IN}/TB,format=rgba[cd]",
        f"[v2][cd]overlay=0:0:enable='gte(t,{CARD_IN})*lt(t,{CARD_OUT})':eof_action=pass[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    print("encoding", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "4:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)])

    aac_lufs, aac_tp = ebur128_stats(final)
    print(f"final AAC ebur128: I={aac_lufs:.2f} LUFS, TP={aac_tp:.2f} dBTP", flush=True)
    if not (-14.5 <= aac_lufs <= -13.5) or aac_tp > -1.6:
        raise SystemExit(f"AAC level out of spec: I={aac_lufs:.2f} LUFS, TP={aac_tp:.2f} dBTP")

    phone_mp4 = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "23",
         "-c:a", "copy", "-movflags", "+faststart", str(phone_mp4)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    d_run = dark_run(final, OUT / f"{STEM}_dark.txt")
    print("dark_run", d_run, flush=True)
    if d_run["verdict"] != "PASS":
        raise SystemExit(f"dark run {d_run}")

    ocr_res = ocr_every_third(final, OUT / f"{STEM}_ocr.txt")
    print("ocr", ocr_res, flush=True)
    if ocr_res["verdict"] != "PASS":
        raise SystemExit(f"foreign text in middle band: {ocr_res}")

    sheet_2fps = OUT / f"{STEM}_2fps.jpg"
    sheet_phone = OUT / f"{STEM}_PHONE.jpg"
    sheet_open = OUT / f"{STEM}_open_sheet.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(sheet_2fps)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(sheet_phone)])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.04", "-i", str(final), "-frames:v", "1",
         str(OUT / f"{STEM}_open.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "select='lte(t,2)',scale=270:480,tile=3x1", "-frames:v", "1", str(sheet_open)])

    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": f0_src, "title": f0_title},
        {"file_id": "loop_ISS_sunrise_to_sunset.ogv", "title": "Loop back to the NASA ISS sunrise Earth limb"},
    ]
    for _ss, source, title, _up, _video in PLATES:
        pool.append({"file_id": source, "title": title})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    meta_p = OUT / f"{STEM}_meta.json"
    meta = {
        "job": "J0936",
        "version": "v03",
        "ruling": "c59",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": "Why Do You Weigh Less at Earth's Equator?",
        "replaces_for_review": "earth_equator_weight_v01/v02 (scheduled emwQsPxnRGM). Earlier versions not overwritten.",
        "file": str(final.relative_to(REPO)),
        "phone_file": str(phone_mp4.relative_to(REPO)),
        "sha256": sha256(final),
        "phone_sha256": sha256(phone_mp4),
        "duration_s": round(dur(final), 3),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "bed": BED.name,
        "brief": {
            "frame_0": "NASA ISS sunrise-to-sunset at v01i 28.30 s, 9:16 centre crop, Earth limb moving.",
            "frame_0_black": round(blk, 3),
            "hook_fit": hook_info,
            "first_word_s": marks["you"],
            "surprise_s": marks["percent"],
            "less_s": marks["less"],
            "subject_equator_s": marks["equator"],
            "ground_s": marks["ground"],
            "equator_speed_thousand_s": marks["thousand"],
            "airliner_s": marks["airliner"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["percent"],
            "second_beat_forty_three_s": marks["forty"],
            "answer_because_s": marks["Because"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": aac_lufs,
            "true_peak_dbtp": aac_tp,
            "runtime_s": total,
            "longest_plate_s": round(max(FIRST_CUT, hold), 3),
            "s06_still_s": round(hold, 3),
            "dark_run": d_run["verdict"],
            "ocr": ocr_res["verdict"],
            "loop_sentence": "Because the ground at the equator swings round so fast, you weigh about half of one percent less at the equator than at the poles.",
        },
        "long_title_on_screen": {
            "title": "Why Do You Weigh Less at Earth's Equator?",
            "from_s": TITLE_IN, "to_s": round(title_out, 3),
        },
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "0.5% LIGHTER / AT THE EQUATOR (yellow 0.5% LIGHTER, <=86% width), 0-2.0 s",
        "teach_card": "0.5% LESS AT EQUATOR, inside the 16:9 band, 2.15-5.70 s",
    }
    meta_p.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", VIDEO_ID,
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(meta_p)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout[-2500:], gate.stderr[-400:], flush=True)

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
    print((music.stdout or music.stderr or "")[-700:], flush=True)
    print((polish.stdout or polish.stderr or "")[-500:], flush=True)
    print((pqa.stdout or pqa.stderr or "")[-900:], flush=True)
    if not all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)):
        raise SystemExit(1)

    publish([
        final, phone_mp4, sheet_2fps, sheet_phone, sheet_open,
        OUT / f"{STEM}_open.jpg", meta_p, cuts_path, pool_path,
        OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt", OUT / f"{STEM}_music.txt",
        OUT / f"{STEM}_dark.txt", OUT / f"{STEM}_ocr.txt",
        OUT / "polish_gate_v03.json", OUT / "polish_gate_v03.txt", OUT / "picture_qa_v03.txt",
    ])
    print("published to UAT and NAS", flush=True)


if __name__ == "__main__":
    main()
