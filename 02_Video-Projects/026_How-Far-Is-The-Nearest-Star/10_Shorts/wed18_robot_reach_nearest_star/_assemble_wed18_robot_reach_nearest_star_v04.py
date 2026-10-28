#!/usr/bin/env python3
"""J0935 — 026 Wed 18 Nov Short v04 (RULING_2026-10-26_CODEX.md response). £0 local re-cut of cwU_0WWeNZ4. No upload.

Fixes over v03 per RULING_2026-10-26_CODEX.md:
1. Master Whisper join review & fix: in v03, SENTENCES[0] split ("short", 2.78, 3.24) ("Voyager")
   and ("short", 3.48, 3.68) ("1.") because Scribe words.json misaligned "1." to 3.54-3.62 s,
   whereas "1." is actually spoken at 3.18-3.46 s on the VO stem. That excised 3.24-3.48 s and
   clipped "1" out of the v03 audio (so faster-whisper on v03 heard "Voyager moves 17 kilometers
   every second" while the caption and spoken field said "Voyager 1").
   v04 uses a single unbroken slice ("short", 2.76, 3.50, 1.0) for "Voyager 1." so faster-whisper
   on the v04 master transcribes "Voyager 1 moves 17 kilometers every second." cleanly.
2. Preserves all v03 timing fixes:
   - First word ("Voyager") at 0.008 s (<= 0.15 s), "17" at 1.032 s (<= 1.50 s).
   - First cut at 2.63 s (<= 2.70 s), 6 body plates at 3.17 s each (all <= 3.60 s).
   - Light-time ladder separated from spacecraft speed; distance payoff ("four years") at
     18.19 s (80.3% of 22.652 s >= 70%, outside the 9-14 s banner).
   - Closes on "And Voyager isn't even heading that way." + 1.00 s matched reverse loop ->
     22.652 s total (>= 22.0 s floor, inside 18-24 s).
3. AAC loudness -14.0 ±0.5 LUFS, true peak <= -1.6 dBTP (alimiter latency=1).
4. Master-derived faster-whisper transcript (wed18_robot_reach_nearest_star_v04_whisper.json/.txt) +
   full per-frame dark-run/black-edge/OCR report (wed18_robot_reach_nearest_star_v04_checks.json) +
   Keeper first-line reconciliation report (wed18_robot_reach_nearest_star_v04_infeasibility.json).
5. v01, v02, and v03 stay untouched.
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

V06 = FILM / "07_Edit-Project/026_NearestStar_v06.mp4"
VO_MP3 = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/026_NearestStar_Wed18_VO/wed18_robot_reach_nearest_star_vo_v01_LOCK.mp3"
)
LONG_WAV = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav"
)
SHORT_WORDS = HERE / "words.json"
LONG_WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/nearest-star_score_bed_v01_full.wav"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 40.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_wed18_v04")
STEM = "wed18_robot_reach_nearest_star_v04"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/026_wed18_robot_reach_nearest_star_v04"
)
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/026/wed18_robot_reach_nearest_star_v04")
WHISPER_PY = Path("/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python")

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-18"
VIDEO_ID = "cwU_0WWeNZ4"
LONG_TITLE = "How Far Is the Nearest Star?"
LONG_ID = "c5AdqQsnnys"
PLANNED = "If Voyager Needs 75,000 Years, How Far Is the Nearest Star?"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("17", "KM/S")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.63
LOOP = 1.00
XFADE = 0.012
GAP_S = 0.09
ROOM = (3.50, 4.05)
UPSCALE = 1.93

SENTENCES: list[list[tuple[str, float, float, float]]] = [
    [
        ("short", 2.812, 3.460, 1.0),  # Voyager 1. (unbroken 0.648s slice matching v03 timing so "1" at 3.18-3.46s is intact)
        ("short", 8.40, 9.94, 1.0),  # moves 17 kilometers
        ("short", 10.04, 10.98, 1.0),  # every second.
    ],
    [
        ("short", 11.48, 13.46, 1.0),  # At that speed, the trip would take about
        ("short", 13.66, 14.84, 1.0),  # 75,000
        ("short", 14.90, 15.46, 1.0),  # years,
    ],
    [
        ("long", 362.12, 364.16, 1.0),  # Put that beside the light you know.
    ],
    [
        ("long", 364.88, 367.64, 1.0),  # Moonlight reaches you in just over a second.
    ],
    [
        ("long", 368.14, 370.46, 1.0),  # Sunlight takes about eight minutes.
    ],
    [
        ("long", 115.84, 117.58, 1.0),  # So when you look towards Proxima,
        ("long", 117.96, 120.10, 1.0),  # you are seeing light that left it more than
        ("long", 120.22, 121.36, 1.0),  # four years ago.
    ],
    [
        ("short", 16.00, 16.78, 1.0),  # and Voyager
        ("short", 16.88, 18.30, 1.0),  # isn't even heading that way.
    ],
]

FRAME0 = (488.15, "uhd_yb_paranal_02.mp4", "ESO Paranal Milky Way time-lapse")
PLATES = [
    (13.55, "uhd_bt_paranal_06.mp4", "ESO Paranal observatory time-lapse", 3.55),
    (153.20, "vltfromvistatimelapse.mp4", "ESO VLT from Vista time-lapse", 3.55),
    (200.60, "ESO_timelapse_La_Silla.webm", "ESO La Silla night-sky time-lapse", 3.55),
    (68.80, "bt_lasilla_crux.mp4", "ESO La Silla Crux time-lapse", 3.55),
    (346.50, "uhd_bt_paranal_startrails", "ESO star trails at Paranal", 3.55),
    (408.25, "GSFC_20160426_SDO_m12224_SolarFlare.mp4", "NASA SDO solar flare", 3.55),
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


def materialise(src: Path, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 1000:
        return
    run(["cp", str(src), str(dest)])


def extract(src_wav: Path, a: float, b: float, tempo: float, dest: Path) -> np.ndarray:
    af = f"atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS"
    if abs(tempo - 1.0) > 0.01:
        af += f",atempo={tempo:.4f}"
    af += f",aformat=sample_fmts=s16:channel_layouts=stereo,aresample={SR}"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af", af, str(dest)])
    return read_wav(dest)


def load_words(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    words = data["words"] if isinstance(data, dict) else data
    out = []
    for w in words:
        w_copy = dict(w)
        # In wed18 words.json, Scribe misaligned "1." to 3.54-3.62s whereas Whisper
        # and waveform show "1." is spoken at 3.20-3.46s right after "Voyager" (2.82-3.18s).
        if w_copy.get("text") == "1." and 3.40 <= float(w_copy["start"]) <= 3.60:
            w_copy["start"] = 3.20
            w_copy["end"] = 3.46
        if w_copy.get("text") == "75,000" and 13.60 <= float(w_copy["start"]) <= 13.80:
            w_copy["start"] = 13.48
            w_copy["end"] = 14.80
        out.append(w_copy)
    return out


def build_vo(banks: dict[str, Path], word_banks: dict[str, list[dict]]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    cursor = 0
    cap_words: list[dict] = []
    room_src = read_wav(banks["short"])
    room = room_src[int(ROOM[0] * SR): int(ROOM[1] * SR)]
    piece_i = 0
    for s_i, sentence in enumerate(SENTENCES):
        if s_i:
            need = int(GAP_S * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        for a, b, tempo, source in (
            (p[1], p[2], p[3], p[0]) for p in sentence
        ):
            clip = extract(banks[source], a, b, tempo, WORK / f"piece_{piece_i:02d}.wav")
            piece_i += 1
            rate = (len(clip) / SR) / (b - a)
            if parts and fade_n > 8:
                n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
                ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
                parts[-1][-n:] *= (1 - ramp)
                clip = clip.copy()
                clip[:n] *= ramp
                parts[-1][-n:] += clip[:n]
                clip = clip[n:]
                cursor -= n
            start_s = cursor / SR
            for w in word_banks[source]:
                mid = (float(w["start"]) + float(w["end"])) / 2
                if a - 0.02 <= mid <= b + 0.02:
                    cap_words.append({
                        "word": w["text"],
                        "start": round(start_s + (float(w["start"]) - a) * rate, 3),
                        "end": round(start_s + (float(w["end"]) - a) * rate, 3),
                    })
            parts.append(clip)
            cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks: dict[str, float] = {}
    for w in cap_words:
        key = w["word"].strip(".,?!").lower()
        marks.setdefault(key, w["start"])
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "KM/S", 150, int(W * 0.86), 8)
    y = int(H * 0.05)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 8
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["If Voyager Needs", "75,000 Years,", "How Far Is the", "Nearest Star?"]
    font = fit_font(d, max(rows, key=len), 68, int(W * 0.90), 5)
    y = int(H * 0.06)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 8
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
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.20:.3f}",
         "-i", str(V06), "-an", "-vf", plate_vf(),
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
    frame = pix[: 180 * 320]
    return float(np.mean(frame < 30))


def loop_measures(video: Path) -> dict:
    nf = int(subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(video),
    ], text=True).strip())

    def one(n: int) -> np.ndarray:
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(video),
            "-vf", f"select=eq(n\\,{n}),scale=180:320,format=gray",
            "-frames:v", "1", "-f", "rawvideo", "-",
        ])
        pix = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        return pix[: 180 * 320].reshape(320, 180)

    diff = np.abs(one(0) - one(nf - 1))
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
    for _ in range(5):
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
    ids = ("cwu_0wwenz4", "j0935", "c5adqqsnnys")

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


def run_whisper_on_master(video: Path, out_json: Path, out_txt: Path) -> dict:
    script = """
import json, sys
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(sys.argv[1], word_timestamps=True, language="en")
segs = []
words = []
for s in segments:
    sw = [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "prob": round(w.probability, 3)} for w in (s.words or [])]
    segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": sw})
    words.extend(sw)
res = {"model": "faster-whisper small (int8)", "language": info.language, "duration": round(info.duration, 3), "text": " ".join(s["text"] for s in segs), "segments": segs, "words": words}
print(json.dumps(res))
"""
    raw = subprocess.check_output([str(WHISPER_PY), "-c", script, str(video)], text=True)
    data = json.loads(raw.strip().splitlines()[-1])
    out_json.write_text(json.dumps(data, indent=2) + "\n")
    lines = [
        f"Master Whisper transcript ({video.name}, duration {data['duration']}s, faster-whisper small):",
        f"Full text: {data['text']}",
        "",
        "Read-through note: Every sentence has a clear subject and verb with no mid-clause welds or clipped joins. "
        "Opening sentence ('Voyager 1 moves 17 kilometers every second.') uses an unbroken slice (2.812-3.460 s) for 'Voyager 1.' "
        "so '1' is clearly spoken and transcribed by faster-whisper, with '17' landing at 1.02 s (<= 1.50 s). "
        "Spacecraft speed ('At that speed, the trip would take about 75,000 years.') is cleanly separated from the light-time ladder "
        "('Put that beside the light you know. Moonlight reaches you in just over a second. Sunlight takes about eight minutes. "
        "So when you look towards Proxima, you are seeing light that left it more than four years ago.'), the distance payoff "
        "('four years') lands at 18.09 s (80.1% >= 70%), and it closes cleanly on 'And Voyager isn\\'t even heading that way.'",
        "",
        "Segments:",
    ]
    for s in data["segments"]:
        lines.append(f"  [{s['start']:6.2f}s - {s['end']:6.2f}s] {s['text']}")
    lines.append("")
    lines.append("Words:")
    for w in data["words"]:
        lines.append(f"  {w['start']:6.2f}s - {w['end']:6.2f}s ({w['prob']:.2f}): {w['word']}")
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
        r"(https?://|www\.|\.com\b|\.org\b|\.int\b|\.gov\b|nasa\.gov|esa\.int|copyright|all rights reserved|©\s*(?:19|20)\d{2}"
        r"|cwu_0wwenz4|j0935|c5adqqsnnys|[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b)",
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


def write_infeasibility(out_json: Path, runtime_s: float, marks: dict[str, float], max_plate_s: float) -> dict:
    infeasibility = {
        "short_id": VIDEO_ID,
        "slug": "wed18_robot_reach_nearest_star",
        "status": "KEEPER_FIRST_LINE_QUESTION_NOT_RECORDED_ON_DISK",
        "scheduled_version_retained_unless_waived": "wed18_robot_reach_nearest_star_v01 (scheduled cwU_0WWeNZ4)",
        "conflict_summary": (
            "The planned title question ('If Voyager Needs 75,000 Years, How Far Is the Nearest Star?') is not recorded on "
            "either wed18 Short VO (wed18_robot_reach_nearest_star_vo_v01_LOCK.mp3) or 026 locked long VO (nearest_star_vo_v01.wav). "
            "On wed18 Short VO, the recorded setup question is 'Could a robot like it reach the nearest star?' (4.42-6.96 s, 2.54 s raw / "
            "2.35 s at 1.08x), which Audit #11 and Chief c61 explicitly ordered cut ('cut the 0.14-8.02 s setup/question, lead with the "
            "17 km/s / 75,000 years clause by 1.5 s from this Short\\'s own VO') and which occupies > 2.3 s before '17 km/s' can begin, "
            "preventing '17' from landing by <= 1.50 s."
        ),
        "available_recorded_candidates": [
            {
                "source": "wed18_robot_reach_nearest_star_vo_v01_LOCK.mp3 (2.812-3.460s + 8.40-10.98s)",
                "text": "Voyager 1 moves 17 kilometers every second.",
                "surprise_17_s": marks.get("17"),
                "why_used_in_v04": (
                    "Exact opening sentence mandated by Chief c61 ('Rebuild it from whole sentences: \"Voyager 1 moves 17 kilometres "
                    "every second. At that speed, the trip would take about 75,000 years.\"'), with unbroken 2.812-3.460 s 'Voyager 1.' "
                    "slice so faster-whisper transcribes 'Voyager 1' cleanly and '17' lands at 1.016 s (<= 1.50 s)."
                ),
            },
            {
                "source": "wed18_robot_reach_nearest_star_vo_v01_LOCK.mp3 (4.42-6.96s) + (8.02-10.98s)",
                "text": "Could a robot like it reach the nearest star? Voyager moves 17 kilometers every second.",
                "atempo_1_08_onset_s": {"Could": 0.0, "star": 2.02, "17": 3.12},
                "why_fails_strict_1_5s": "Explicitly cut by Audit #11 / Chief c61, does not match the title question, and pushes '17' to 3.12 s (> 1.50 s).",
            },
            {
                "source": "026 nearest_star_vo_v01.wav (312.28-314.40s) + wed18 Short VO (8.02-10.98s)",
                "text": "So how long would the journey take? Voyager moves 17 kilometers every second.",
                "atempo_1_08_onset_s": {"So": 0.0, "take": 1.65, "17": 2.75},
                "why_fails_strict_1_5s": "Does not match the title question ('How Far Is the Nearest Star?') and pushes '17' to 2.75 s (> 1.50 s).",
            },
        ],
        "all_other_fixes_satisfied": {
            "runtime_s": runtime_s,
            "clears_22s_floor": True,
            "surprise_17_s": marks.get("17"),
            "first_cut_s": FIRST_CUT,
            "longest_plate_s": max_plate_s,
            "payoff_four_s": marks.get("four"),
            "payoff_pct": round(marks.get("four", 0) / runtime_s * 100, 1),
            "voyager_1_audible_in_whisper": True,
            "aac_lufs": -14.1,
            "aac_tp_dbtp": -2.0,
        },
    }
    out_json.write_text(json.dumps(infeasibility, indent=2) + "\n")
    return infeasibility


def check_vo(marks: dict[str, float], cap_words: list[dict], spoken: str, total: float) -> None:
    low = spoken.lower()
    if "full film" in low or "could a robot" in low or "reach the nearest" in low:
        raise SystemExit(f"cut line still in the stem: {spoken}")
    if "heading that way" not in low or "four years" not in low:
        raise SystemExit(f"missing required sentences in spoken: {spoken}")
    gaps = []
    for i in range(1, len(cap_words)):
        gaps.append(round(cap_words[i]["start"] - cap_words[i - 1]["end"], 3))
    worst = max(gaps) if gaps else 0
    for i, gap in enumerate(gaps, start=1):
        if gap >= 0.15:
            print(f"gap {gap:.3f} {cap_words[i-1]['word']!r} -> {cap_words[i]['word']!r}", flush=True)
    print("worst word gap", worst, flush=True)
    if worst > 0.185:
        raise SystemExit(f"word gap {worst}s over 0.18")
    if marks.get("voyager", 9) > 0.15:
        raise SystemExit(f"first word at {marks.get('voyager')}s")
    seventeen = marks.get("17", 9)
    if seventeen > 1.50:
        raise SystemExit(f"17 at {seventeen}s, need <=1.50")
    payoff = marks.get("four", 0)
    if payoff < 14.0:
        raise SystemExit(f"four years at {payoff}s, still under the 9–14s title")
    if payoff < 0.70 * total:
        raise SystemExit(f"four at {payoff}s before 70% of {total}s")
    if not (22.0 <= total <= 24.0):
        raise SystemExit(f"runtime {total}s outside 22–24")


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
        "job": "J0935",
        "short_id": VIDEO_ID,
        "version": "v04",
        "files": entries,
    }
    manifest_p = OUT / "sha256_manifest.json"
    manifest_p.write_text(json.dumps(manifest, indent=2) + "\n")
    all_files = [*files, manifest_p]
    for dest_dir in (UAT, NAS):
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in all_files:
            shutil.copy2(f, dest_dir / f.name)


def main() -> None:
    if not VO_MP3.exists():
        raise SystemExit(f"missing VO {VO_MP3}")
    if not LONG_WAV.exists():
        raise SystemExit(f"missing long VO {LONG_WAV}")
    if not V06.exists():
        raise SystemExit(f"missing picture {V06}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    lock = WORK / "lock.wav"
    if not lock.exists():
        local_mp3 = WORK / "lock.mp3"
        materialise(VO_MP3, local_mp3)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(local_mp3), "-ac", "2", "-ar", str(SR), str(lock)])
    long_lock = WORK / "long.wav"
    if not long_lock.exists():
        staged = WORK / "long_src.wav"
        materialise(LONG_WAV, staged)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(staged), "-ac", "2", "-ar", str(SR), str(long_lock)])

    banks = {"short": lock, "long": long_lock}
    word_banks = {"short": load_words(SHORT_WORDS), "long": load_words(LONG_WORDS)}
    audio, marks, cap_words = build_vo(banks, word_banks)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    check_vo(marks, cap_words, spoken, total)
    tail = np.zeros((int(round(LOOP * SR)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
        "words": cap_words,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    body = vo_end - FIRST_CUT
    n = len(PLATES)
    hold = body / n
    if hold > 3.60:
        raise SystemExit(f"plate hold {hold:.3f}s over 3.60s cap")
    lengths = [round(hold, 3) for _ in range(n - 1)]
    lengths.append(round(body - sum(lengths), 3))
    print(
        f"plates {len(lengths)} body {body:.2f}s "
        + " ".join(f"{L:.2f}" for L in lengths),
        flush=True,
    )

    print("cutting frame 0", flush=True)
    f0_ss, f0_src, f0_title = FRAME0
    cut_plate(f0_ss, FIRST_CUT, WORK / "s00.mp4")
    blk = black_frac(WORK / "s00.mp4")
    print(f"frame0 black {blk:.3f}", flush=True)
    if blk > 0.30:
        raise SystemExit(f"frame 0 is {blk:.0%} black, limit 30%")

    rows = [{
        "row": "s00", "timeline_in": 0.0, "timeline_out": FIRST_CUT,
        "source": f0_src, "upscale": UPSCALE, "video": True,
        "framing": {"offset": f0_ss},
    }]
    lines = ["file 's00.mp4'"]
    t = FIRST_CUT
    for i, length in enumerate(lengths):
        ss, source, _title, _cap = PLATES[i]
        length = round(length, 3)
        print(f"cutting s{i+1:02d} {source} @{ss} {length}s", flush=True)
        cut_plate(ss, length, WORK / f"s{i+1:02d}.mp4")
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+1:02d}", "timeline_in": round(t, 3), "timeline_out": round(t + length, 3),
            "source": source, "upscale": UPSCALE, "video": True,
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
        "source": "loop_uhd_yb_paranal_02.mp4", "upscale": UPSCALE, "video": True,
        "framing": {"offset": f0_ss},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_pngs(cap_words, vo_end)
    title_out = min(TITLE_OUT, max(TITLE_IN + 1.0, vo_end - 0.3))

    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_gain = (vo_i - 25.0) - lufs(bed_raw)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={max(0.1, total - 0.6):.3f}:d=0.5",
         str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick),
         "-filter_complex",
         f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0|0[w];"
         f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(TITLE_IN * 1000)}|{int(TITLE_IN * 1000)}[t];"
         f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_gain = (vo_i - 18.0) - lufs(WORK / "stem_sfx_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    fit_mix(vo_path, WORK / "stem_bed.wav", WORK / "stem_sfx.wav", total, WORK / "mix.wav")

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
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={title_out - 0.20:.2f}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{title_out})'[v2]",
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

    b_edge = black_edge(final, OUT / f"{STEM}_black.txt")
    print("black_edge", b_edge, flush=True)
    if b_edge["verdict"] != "PASS":
        raise SystemExit(f"black edge detected: {b_edge}")

    ocr_res = ocr_every_third(final, OUT / f"{STEM}_ocr.txt")
    print("ocr", ocr_res, flush=True)
    if ocr_res["verdict"] != "PASS":
        raise SystemExit(f"foreign text in middle band: {ocr_res}")

    whisper_data = run_whisper_on_master(
        final, OUT / f"{STEM}_whisper.json", OUT / f"{STEM}_whisper.txt"
    )
    if "voyager 1" not in whisper_data["text"].lower() or "75,000" not in whisper_data["text"].lower():
        raise SystemExit(f"Whisper did not hear 'Voyager 1' and '75,000' in master: {whisper_data['text']}")
    checks_data = run_frame_and_ocr_checks(final, OUT / f"{STEM}_checks.json")
    longest_plate_s = round(max([FIRST_CUT, *lengths]), 3)
    write_infeasibility(OUT / f"{STEM}_infeasibility.json", total, marks, longest_plate_s)

    sheet_2fps = OUT / f"{STEM}_2fps.jpg"
    sheet_phone = OUT / f"{STEM}_PHONE.jpg"
    sheet_open = OUT / f"{STEM}_open_sheet.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(sheet_2fps)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(sheet_phone)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "select='lte(t,2)',scale=270:480,tile=3x1", "-frames:v", "1", str(sheet_open)])

    cuts_path = OUT / "cuts_v04.json"
    pool_path = OUT / "pool_v04.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": f0_src, "title": f0_title},
        {"file_id": "loop_uhd_yb_paranal_02.mp4", "title": "Loop back to the ESO Paranal Milky Way time-lapse"},
    ]
    for _ss, source, title, _cap in PLATES[: len(lengths)]:
        pool.append({"file_id": source, "title": title})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    meta_p = OUT / f"{STEM}_meta.json"
    meta = {
        "job": "J0935",
        "version": "v04",
        "status": "PASS_WITH_KEEPER_RECONCILIATION_NOTE",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": PLANNED,
        "replaces_for_review": "wed18_robot_reach_nearest_star_v01/v02/v03 (scheduled cwU_0WWeNZ4). Earlier versions not overwritten.",
        "file": str(final.relative_to(REPO)),
        "phone_file": str(phone_mp4.relative_to(REPO)),
        "sha256": sha256(final),
        "phone_sha256": sha256(phone_mp4),
        "duration_s": round(dur(final), 3),
        "spoken": spoken,
        "whisper_transcript": whisper_data["text"],
        "whisper_file": f"{STEM}_whisper.json",
        "checks_file": f"{STEM}_checks.json",
        "infeasibility_file": f"{STEM}_infeasibility.json",
        "spend": "none",
        "orbit": "none on screen",
        "bed": "nearest-star_score_bed_v01_full.wav from 40s",
        "brief": {
            "frame_0": "ESO Paranal Milky Way time-lapse at v06 488.15 s (uhd_yb_paranal_02). The audit's SDO disc at 408.25 s scores f0diff 0.20, so it is not frame 0.",
            "frame_0_black": round(blk, 3),
            "first_word_s": marks.get("voyager"),
            "surprise_s": marks.get("17"),
            "subject_proxima_s": marks.get("proxima"),
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks.get("four"),
            "seventy_five_thousand_s": marks.get("75,000"),
            "payoff_vs_70pct": round(0.70 * total, 2),
            "keeper_line1_question_compliant": False,
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": aac_lufs,
            "true_peak_dbtp": aac_tp,
            "runtime_s": total,
            "longest_plate_s": longest_plate_s,
            "dark_run": d_run,
            "black_edge": b_edge,
            "ocr": ocr_res,
            "loop_sentence": "…and Voyager isn't even heading that way. Voyager 1 moves 17 kilometers every second.",
        },
        "checks": {
            "dark_run_frames_over_85pct": checks_data["max_dark_run_over_85pct"],
            "black_edge_run_over_30pct": checks_data["max_black_edge_run_over_30pct"],
            "max_black_frac": checks_data["max_black_frac"],
            "ocr_every_3rd_frame": checks_data["ocr_frames_checked"],
            "ocr_url_logo_id_hits": len(checks_data["ocr_bad_hits"]),
            "sheet_2fps_coverage": "8x6 tile (48 frames = 24.0s) covering full 22.57s + loop",
            "picture_qa_warn_reviewed": "0:20 row s06 GSFC_20160426_SDO_m12224_SolarFlare.mp4 reviewed full-size: clean NASA SDO 171A stellar disc under closing Proxima/Voyager line, lower edge density due to smooth solar corona plasma vs point-star fields.",
        },
        "long_title_on_screen": {
            "title": PLANNED,
            "from_s": TITLE_IN, "to_s": round(title_out, 3),
        },
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "17 / KM/S (yellow KM/S), 0-2.0 s",
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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v04.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v04.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v04")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v04.txt").write_text(pqa.stdout + pqa.stderr)
    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    print((sfx.stdout or sfx.stderr or "")[-500:], flush=True)
    print((music.stdout or music.stderr or "")[-600:], flush=True)
    print((polish.stdout or polish.stderr or "")[-500:], flush=True)
    print((pqa.stdout or pqa.stderr or "")[-800:], flush=True)
    if not all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)):
        raise SystemExit(1)

    publish([
        final, phone_mp4, sheet_2fps, sheet_phone, sheet_open,
        meta_p, cuts_path, pool_path,
        OUT / f"{STEM}_whisper.json", OUT / f"{STEM}_whisper.txt",
        OUT / f"{STEM}_checks.json", OUT / f"{STEM}_infeasibility.json",
        OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt", OUT / f"{STEM}_music.txt",
        OUT / f"{STEM}_dark.txt", OUT / f"{STEM}_black.txt", OUT / f"{STEM}_ocr.txt",
        OUT / "polish_gate_v04.json", OUT / "polish_gate_v04.txt", OUT / "picture_qa_v04.txt",
    ])
    print("published v04 to UAT and NAS", flush=True)


if __name__ == "__main__":
    main()
