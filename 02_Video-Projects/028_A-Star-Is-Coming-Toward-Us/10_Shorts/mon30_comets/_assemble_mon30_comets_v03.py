#!/usr/bin/env python3
"""J0936 — 028 Mon 30 Nov Short v03 (c59 FIX of v02). £0 local re-cut of bizlhspnVvY. No upload.

Chief ruling c59 (Mon 26 Oct 05:50 London, OWB #264 6409202315):
  (a) Sentence at 8.1-10.1 s was a fragment "straight through the Oort cloud."
      Reuse "The star is going" (260.12-261.24 s) from the 028 master VO before
      "straight through the Oort cloud." so the sentence is complete:
      "The star is going straight through the Oort cloud."
  (b) Mix level -14.0 ±0.5 LUFS and true peak <= -1.6 dBTP on the encoded AAC .mp4
      (alimiter latency=1).
  (c) Second Gaia stretch moved from 24.0 s (which crossed the 25.3 s 2-frame black dip)
      to 20.0 s (and first Gaia stretch to 5.0 s, >11 s apart, both 100% inside the
      clean 4.0-25.0 s starfield, 0 dark frames, 0 ESA end-slate frames).
  - Build _PHONE.mp4 (720x1280) + sheets + sha256_manifest.json, copy to OWB UAT and NAS.
  - v01 and v02 are left untouched.
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

VO_WAV = FILM / "02_Voiceover/star_coming_vo_v01.wav"
WORDS = FILM / "07_Edit-Project/full_master_v03_pack/gliese_words_list.json"
BED = FILM / "05_Music/gliese_score_bed_v03.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
HDIR = FILM / "07_Edit-Project/nasa_pool_v01/028_harvest_v01"
CDIR = FILM / "07_Edit-Project/code_graphics_v02"

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0936_mon30_v03")
STEM = "028_short_mon30_comets_v03"
SHORT_SLUG = "mon30_comets_v03"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
NAS_UAT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT")
NAS_STAGE = Path("/Volumes/data/mac-mini-archive/youtube-staging/028")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-30"
VIDEO_ID = "bizlhspnVvY"
LONG_TITLE = "What Happens When a Star Passes Through Our Solar System?"
LONG_ID = "F-jImX5h7ws"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
CARD_IN, CARD_OUT = 2.20, 5.70
FIRST_CUT = 2.55
LOOP = 1.00
XFADE = 0.012
GAP_S = 0.10
GAPS = {1: 0.02, 2: 0.02, 5: 0.08, 6: 0.06, 8: 0.08, 11: 0.08}
ROOM = (281.00, 281.45)

# Source times on star_coming_vo_v01.wav. Pauses over 0.20 s are split out.
SEGMENTS = [
    (283.22, 283.52, "Gliese"),
    (283.90, 284.36, "710"),
    (284.64, 287.06, "will send about 10 extra comets a year,"),
    (287.50, 289.42, "falling in close enough for us to see,"),
    (291.20, 293.52, "for three to four million years."),
    (260.12, 261.24, "The star is going"),
    (262.04, 264.00, "straight through the Oort cloud."),
    (264.86, 266.72, "A star passing through the cloud"),
    (267.18, 270.52, "is like a hand brushing through a bowl of floating marbles."),
    (297.10, 300.04, "The comets do not arrive while the star is passing."),
    (300.86, 301.22, "Why?"),
    (302.16, 307.08, "Because they are so far out that falling in takes hundreds of thousands of years."),
]
MARKS = {
    "Gliese": (0, 283.22),
    "710": (1, 283.90),
    "ten": (2, 285.32),
    "comets": (2, 286.18),
    "going": (5, 260.86),
    "arrive": (9, 298.02),
    "Why": (10, 300.86),
    "Because": (11, 302.16),
}

LAS = HDIR / "eso_lasilla_ntt.mp4"
SDO = HDIR / "sdo_solar_flare.mp4"
GAIA = HDIR / "gaia_motion_1_6my.mp4"
R28 = CDIR / "code_graphic_028_r28_hale_bopp_2_v02.mp4"
CROP_9 = "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"


def crop_x(x: int) -> str:
    return (
        f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    )


FRAME0 = (
    0.30,
    LAS,
    "ESO La Silla night sky, Milky Way over the telescope roof",
    1.78,
    crop_x(1300).replace(
        "scale=1080:1920",
        "eq=contrast=1.12:saturation=1.08,scale=1080:1920",
    ),
)
# Gaia offsets at 5.0 s and 20.0 s stay >11 s apart and well clear of the 25.3 s
# 2-frame black dip and 28.1 s fade-to-black / 29.3 s ESA end slate.
PLATES = [
    (22.0, SDO, "NASA SDO sun, bright solar surface", 1.78, True, CROP_9),
    (5.0, GAIA, "ESA Gaia star field in motion", 0.89, True, CROP_9),
    (33.0, SDO, "NASA SDO sun, second bright stretch", 1.78, True, CROP_9),
    (13.0, LAS, "ESO La Silla telescope wall and night sky", 1.78, True, crop_x(1100)),
    (58.0, SDO, "NASA SDO sun, third bright stretch", 1.78, True, CROP_9),
    (20.0, GAIA, "ESA Gaia star field, later stretch", 0.89, True, CROP_9),
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


def build_vo(src: np.ndarray, words_raw: list[dict]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(ROOM[0] * SR): int(ROOM[1] * SR)]
    for i, (a, b, _label) in enumerate(SEGMENTS):
        if i:
            need = int(GAPS.get(i, GAP_S) * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        i0, i1 = int(round(a * SR)), int(round(b * SR))
        clip = src[i0:i1].copy()
        if i and fade_n > 8:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        picked = []
        for w in words_raw:
            ws, we = float(w["start"]), float(w["end"])
            if a - 0.02 <= ws and we <= b + 0.04:
                picked.append(w)
        for prev, w in zip(picked, picked[1:]):
            gap = float(w["start"]) - float(prev["end"])
            if gap > 0.20:
                raise SystemExit(
                    f"pause {gap:.2f}s inside segment {i} before {w['text']!r} ({_label})"
                )
        for j, w in enumerate(picked):
            ws, we = float(w["start"]), float(w["end"])
            txt = w["text"]
            if i == 5 and j == 0:
                txt = "The"
            if i == 5 and txt.endswith(","):
                txt = txt.rstrip(",")
            cap_words.append({
                "word": txt,
                "start": round(starts[-1] + (ws - a), 3),
                "end": round(starts[-1] + (we - a), 3),
            })
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks = {}
    for name, (seg, src_t) in MARKS.items():
        a = SEGMENTS[seg][0]
        marks[name] = round(starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "10 COMETS", 118, int(W * 0.88), 8)
    y = int(H * 0.05)
    y += centred(d, y, "10 COMETS", font, YELLOW, 8)[3] - y + 10
    centred(d, y, "A YEAR", font, WHITE, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why Will Gliese 710's", "Comets Arrive After", "It Has Gone?"]
    font = fit_font(d, max(rows, key=len), 58, int(W * 0.86), 5)
    gap = d.textbbox((0, 0), "Hg", font=font)[3] + 10
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
    font = fit_font(probe, "10 EXTRA COMETS", 62, int(W * 0.84), 6)
    text_h = probe.textbbox((0, 0), "Hg", font=font)[3]
    for i in range(n):
        t = CARD_IN + i / FPS
        a = min(1.0, (t - CARD_IN) / 0.35, (CARD_OUT - t) / 0.30)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = int(255 * max(0.0, a))
        label = "10 EXTRA COMETS"
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
        font = fit_font(d, text, 54, int(W * 0.90), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_plate(src: Path, ss: float, length: float, dest: Path, vf: str) -> None:
    frames = max(1, round(length * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.25:.3f}",
         "-i", str(src), "-an", "-vf", vf,
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


def frame0_diff(path: Path) -> float:
    frames = []
    for t in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5):
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(path), "-frames:v", "1",
            "-vf", "scale=72:128,format=gray", "-f", "rawvideo", "-",
        ])
        frames.append(np.frombuffer(raw, dtype=np.uint8)[: 72 * 128].astype(np.float32).reshape(128, 72))
    y0, y1 = int(128 * 0.28), int(128 * 0.72)
    bands = [f[y0:y1].ravel() for f in frames]
    steps = [float(np.mean(np.abs(a - b)) / 255 * 100) for a, b in zip(bands, bands[1:])]
    return min((steps[i] + steps[i + 1]) / 2 for i in range(len(steps) - 1))


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
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True)
    i_lines = [ln for ln in p.stderr.splitlines() if "I:" in ln and "LUFS" in ln]
    tp_lines = [ln for ln in p.stderr.splitlines() if "Peak:" in ln and "dBFS" in ln]
    if not i_lines or not tp_lines:
        raise SystemExit(f"no ebur128 stats from {path}")
    lufs_val = float(i_lines[-1].split("I:")[1].split("LUFS")[0].strip())
    tp_val = float(tp_lines[-1].split("Peak:")[1].split("dBFS")[0].strip())
    return lufs_val, tp_val


def lufs(path: Path) -> float:
    return ebur128_stats(path)[0]


def fit_mix(vo_path: Path, bed_path: Path, sfx_path: Path, total: float, out_wav: Path) -> tuple[float, float]:
    raw_mix = WORK / "mix_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(bed_path),
         "-i", str(sfx_path), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14.0:TP=-2.2:LRA=11[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(raw_mix)])
    gain_db = 0.0
    lim_db = -2.1
    for _ in range(8):
        lin_lim = 10 ** (lim_db / 20.0)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(raw_mix),
             "-af", f"volume={gain_db:.2f}dB,alimiter=limit={lin_lim:.6f}:level=disabled:attack=5:release=50:latency=1,aresample={SR}",
             "-ar", str(SR), "-t", f"{total:.3f}", str(out_wav)])
        probe_aac = WORK / "mix_probe.m4a"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(out_wav),
             "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), str(probe_aac)])
        i_val, tp_val = ebur128_stats(probe_aac)
        print(f"fit_mix probe: gain={gain_db:.2f}dB lim={lim_db:.2f}dB -> I={i_val:.2f} LUFS, TP={tp_val:.2f} dBTP", flush=True)
        if -14.5 <= i_val <= -13.5 and tp_val <= -1.6:
            return i_val, tp_val
        if tp_val > -1.6:
            lim_db -= (tp_val - (-1.75))
        if i_val < -14.5 or i_val > -13.5:
            gain_db += (-14.0 - i_val) * 0.85
    raise SystemExit(f"could not converge mix to -14.0±0.5 LUFS & TP<=-1.6 dBTP (got {i_val:.2f} LUFS, {tp_val:.2f} dBTP)")


def dark_run(video: Path) -> dict:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(video),
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    n_pix = 180 * 320
    frames = np.frombuffer(raw, dtype=np.uint8)
    frames = frames[: (frames.size // n_pix) * n_pix].reshape(-1, n_pix)
    dark = np.mean(frames < 20, axis=1) > 0.85
    worst = cur = 0
    hits = []
    for idx, is_d in enumerate(dark):
        if is_d:
            cur += 1
            if cur >= 3:
                hits.append(round(idx / FPS, 3))
            worst = max(worst, cur)
        else:
            cur = 0
    return {"verdict": "PASS" if worst < 3 else "FAIL", "frames": int(len(frames)), "worst_run": int(worst), "hits": hits}


def ocr_every_third(video: Path) -> dict:
    ocr_dir = WORK / "ocr_frames"
    if ocr_dir.exists():
        shutil.rmtree(ocr_dir)
    ocr_dir.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video),
         "-vf", "fps=10,scale=540:960", str(ocr_dir / "f_%04d.png")])
    bad_pat = re.compile(r"(https?://|www\.|\.com\b|\.org\b|copyright|all rights reserved|youtube|bizlhspnVvY|F-jImX5h7ws|J0936|\.mp4|\.webm|\.mov|esa\.int)", re.I)
    hits = []
    files = sorted(ocr_dir.glob("f_*.png"))
    for f in files:
        p = subprocess.run(["tesseract", str(f), "stdout", "--psm", "6"], capture_output=True, text=True)
        txt = (p.stdout or "").strip()
        m = bad_pat.search(txt)
        if m:
            hits.append({"frame": f.name, "match": m.group(0), "text": txt})
    return {"verdict": "PASS" if not hits else "FAIL", "frames": len(files), "hits": len(hits), "details": hits}


def check_words(marks: dict, cap_words: list[dict], total: float) -> None:
    spoken = " ".join(w["word"] for w in cap_words)
    low = spoken.lower()
    for banned in ("full film", "stay, and", "calculation suggests", "should you worry"):
        if banned in low:
            raise SystemExit(f"banned line still in the stem: {banned}")
    if "the star is going straight through the oort cloud" not in low:
        raise SystemExit(f"complete Oort cloud sentence missing from spoken: {spoken}")
    if marks["Gliese"] > 0.15:
        raise SystemExit(f"first word at {marks['Gliese']}s")
    if marks["ten"] > 1.50:
        raise SystemExit(f"10 at {marks['ten']}s, need <=1.50")
    if marks["710"] > 2.50:
        raise SystemExit(f"710 at {marks['710']}s, need <=2.50")
    if marks["arrive"] < 14.0:
        raise SystemExit(f"arrive at {marks['arrive']}s is under the 9-14 s banner")
    if marks["Because"] < 0.70 * total:
        raise SystemExit(f"Because at {marks['Because']}s is before 70% ({0.70 * total:.2f})")
    if not (22.0 <= total <= 27.4):
        raise SystemExit(f"runtime {total}s outside 22-27")
    for prev, w in zip(cap_words, cap_words[1:]):
        gap = w["start"] - prev["end"]
        if gap > 0.22:
            raise SystemExit(f"pause {gap:.2f}s before {w['word']}")
    print("spoken", spoken, flush=True)


def publish() -> None:
    manifest_files = [
        f"{STEM}.mp4",
        f"{STEM}_PHONE.mp4",
        f"{STEM}_2fps.jpg",
        f"{STEM}_PHONE.jpg",
        f"{STEM}_open.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_meta.json",
        f"{STEM}_gate.txt",
        f"{STEM}_sfx.txt",
        f"{STEM}_music.txt",
        f"{STEM}_dark.txt",
        f"{STEM}_ocr.txt",
        "cuts_v03.json",
        "pool_v03.json",
        "polish_gate_v03.json",
        "polish_gate_v03.txt",
        "picture_qa_v03.txt",
    ]
    entries = {}
    for name in manifest_files:
        p = OUT / name
        if p.exists():
            entries[name] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    manifest = {
        "job": "J0936",
        "film": "028",
        "short": SHORT_SLUG,
        "stem": STEM,
        "video_id": VIDEO_ID,
        "files": entries,
    }
    (OUT / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    manifest_files.append("sha256_manifest.json")

    targets = [
        UAT / STEM,
        UAT / f"028_{SHORT_SLUG}",
        NAS_UAT / STEM,
        NAS_UAT / f"028_{SHORT_SLUG}",
        NAS_STAGE / SHORT_SLUG,
    ]
    for tgt in targets:
        tgt.mkdir(parents=True, exist_ok=True)
        for name in manifest_files:
            src = OUT / name
            if src.exists():
                shutil.copy2(src, tgt / name)
        pqa_src = OUT / "picture_qa_v03"
        if pqa_src.exists():
            pqa_dst = tgt / "picture_qa_v03"
            pqa_dst.mkdir(parents=True, exist_ok=True)
            for item in pqa_src.iterdir():
                if item.is_file():
                    shutil.copy2(item, pqa_dst / item.name)
    print("published to UAT and NAS", flush=True)


def main() -> None:
    for p in (VO_WAV, WORDS, BED, LAS, SDO, GAIA, R28):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words_raw = json.loads(WORDS.read_text())
    src = read_wav(VO_WAV)
    audio, marks, cap_words = build_vo(src, words_raw)
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
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.80")
    if hold < 2.40:
        raise SystemExit(f"plate hold {hold:.2f}s under 2.40")

    print("cutting frame 0", flush=True)
    f0_ss, f0_src, f0_title, f0_up, f0_vf = FRAME0
    cut_plate(f0_src, f0_ss, FIRST_CUT, WORK / "s00.mp4", f0_vf)
    blk = black_frac(WORK / "s00.mp4")
    motion = frame0_diff(WORK / "s00.mp4")
    print(f"frame0 black {blk:.3f} diff {motion:.2f}", flush=True)
    if blk > 0.25:
        raise SystemExit(f"frame 0 is {blk:.0%} black")
    if motion < 1.50:
        raise SystemExit(f"frame 0 diff {motion:.2f} under 1.50")

    rows = [{
        "row": "s01_lasilla_milky_way",
        "timeline_in": 0.0, "timeline_out": FIRST_CUT,
        "source": f0_src.name, "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss},
    }]
    lines = ["file 's00.mp4'"]
    t = FIRST_CUT
    for i, (ss, source, _title, up, video, vf) in enumerate(PLATES):
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        print(f"cutting s{i+2:02d} {source.name} @{ss} {length}s", flush=True)
        cut_plate(source, ss, length, WORK / f"s{i+1:02d}.mp4", vf)
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+2:02d}_{source.stem}",
            "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source.name, "upscale": up, "video": video,
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
        "source": "loop_eso_lasilla_ntt.mp4", "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    print("card frames", flush=True)
    card_frames(WORK / "card")
    caps = caption_pngs(cap_words, vo_end)
    title_out = min(TITLE_OUT, max(TITLE_IN + 1.0, vo_end - 0.4))

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_gain = (vo_i - 20.0) - lufs(bed_raw)
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

    final_lufs, final_tp = ebur128_stats(final)
    print(f"final AAC ebur128: I={final_lufs:.2f} LUFS, TP={final_tp:.2f} dBTP", flush=True)
    if not (-14.5 <= final_lufs <= -13.5) or final_tp > -1.6:
        raise SystemExit(f"final AAC audio out of c59 spec: {final_lufs:.2f} LUFS, {final_tp:.2f} dBTP")

    phone_mp4 = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos,setsar=1,fps=30,format=yuv420p",
         "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "copy",
         "-movflags", "+faststart", str(phone_mp4)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    d_res = dark_run(final)
    (OUT / f"{STEM}_dark.txt").write_text(json.dumps(d_res, indent=2) + "\n")
    print("dark_run", d_res, flush=True)
    if d_res["verdict"] != "PASS":
        raise SystemExit(f"dark_run failed: {d_res}")

    o_res = ocr_every_third(final)
    (OUT / f"{STEM}_ocr.txt").write_text(json.dumps(o_res, indent=2) + "\n")
    print("ocr", {k: v for k, v in o_res.items() if k != "details"}, flush=True)
    if o_res["verdict"] != "PASS":
        raise SystemExit(f"ocr failed: {o_res}")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x4", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.04", "-i", str(final), "-frames:v", "1",
         str(OUT / f"{STEM}_open.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "select='eq(n,0)+eq(n,7)+eq(n,30)+eq(n,60)+eq(n,90)',scale=270:480,tile=5x1",
         "-frames:v", "1", str(OUT / f"{STEM}_open_sheet.jpg")])

    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": f0_src.name, "title": f0_title},
        {"file_id": "loop_eso_lasilla_ntt.mp4", "title": "Loop back to the ESO La Silla Milky Way"},
    ]
    seen = {f0_src.name}
    for _ss, source, title, _up, _video, _vf in PLATES:
        if source.name in seen:
            continue
        seen.add(source.name)
        pool.append({"file_id": source.name, "title": title})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "job": "J0936",
        "version": "v03",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": "Why Will Gliese 710's Comets Arrive After It Has Gone?",
        "replaces_for_review": "028_short_mon30_comets_v01 (scheduled bizlhspnVvY). v01 and v02 not overwritten.",
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
            "frame_0": "ESO La Silla NTT, crop x=1300 onto the Milky Way, offset 0.30 s.",
            "frame_0_black": round(blk, 3),
            "frame_0_diff": round(motion, 2),
            "first_word_s": marks["Gliese"],
            "surprise_s": marks["ten"],
            "comets_s": marks["comets"],
            "subject_710_s": marks["710"],
            "going_s": marks["going"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["ten"],
            "answer_because_s": marks["Because"],
            "arrive_s": marks["arrive"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": final_lufs,
            "true_peak_dbtp": final_tp,
            "runtime_s": total,
            "longest_plate_s": round(max(FIRST_CUT, hold), 3),
            "dark_run": d_res["verdict"],
            "ocr": o_res["verdict"],
            "loop_sentence": (
                "Because they are so far out that falling in takes hundreds of thousands of years, "
                "Gliese 710 will send about 10 extra comets a year."
            ),
        },
        "long_title_on_screen": {
            "title": "Why Will Gliese 710's Comets Arrive After It Has Gone?",
            "from_s": TITLE_IN, "to_s": round(title_out, 3),
        },
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "10 COMETS / A YEAR (yellow 10 COMETS), 0-2.0 s",
        "teach_card": "10 EXTRA COMETS, inside the 16:9 band, 2.20-5.70 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", VIDEO_ID,
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(OUT / f"{STEM}_meta.json")],
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
    publish()


if __name__ == "__main__":
    main()
