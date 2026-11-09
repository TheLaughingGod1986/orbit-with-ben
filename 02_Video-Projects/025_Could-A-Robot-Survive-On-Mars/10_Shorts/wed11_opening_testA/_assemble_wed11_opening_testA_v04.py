#!/usr/bin/env python3
"""J0935 c61 — 025 Wed 11 Nov Short v04. £0 local re-cut of TtgHNLXfDSs. No upload.

Chief c61: drop the two broken long-VO slices ("It wears them down…" and
"The cold that kills a phone battery"). Join "within months." straight to
"Martian wind kept sweeping them clean." Add the recorded sentences
"The team called them cleaning events. Each one gave the rover back its
power, and it kept driving." Keep "2018" at ≥70% and the runtime at 23–25 s.
Level the AAC to −14.0 ±0.5 LUFS and ≤ −1.6 dBTP.

v01, v02 and v03 are not overwritten. The scheduled file stays v02.
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
BED_FROM = 80.0  # mon09 v02 used 300 s of the same bed

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_wed11_v04")
STEM = "wed11_opening_testA_v04"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_wed11_opening_testA_v04"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/wed11_opening_testA_v04")

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

# (src, start, end, gap_before). Opening is "fourteen years on Mars" with no gap,
# so the phrase ends by 1.5 s. The broken middle is gone: months joins straight
# to "Martian wind kept sweeping them clean." The two cleaning-event sentences
# are whole lines from the locked long (263.76–269.34 s). "2018" is the payoff.
CLIPS = [
    ("opp", 5.10, 5.96, 0.00),       # fourteen
    ("opp", 6.12, 6.74, 0.00),       # years.
    ("opp", 2.74, 3.52, 0.00),       # on Mars.
    ("opp", 0.06, 2.78, 0.14),       # This rover was built to last 90 days
    ("opp", 7.12, 10.44, 0.14),      # Dust should have choked its solar panels within months.
    ("opp", 11.74, 14.48, 0.06),     # Martian wind kept sweeping them clean.
    ("long", 263.68, 265.70, 0.12),  # The team called them cleaning events.
    ("long", 266.04, 269.42, 0.10),  # Each one gave the rover back its power, and it kept driving.
    ("opp", 14.82, 15.16, 0.16),     # Then
    ("opp", 15.46, 16.64, 0.04),     # in 2018,
    ("opp", 16.96, 19.40, 0.04),     # a storm wrapped the whole planet
    ("opp", 19.70, 21.30, 0.06),     # and the sky went dark.
]
MARKS = {
    "14": (0, 5.14),
    "years_end": (1, 6.72),
    "Mars": (2, 2.98),
    "wind": (5, 12.32),
    "clean_end": (5, 14.40),
    "events": (6, 265.10),
    "driving_end": (7, 269.34),
    "2018": (9, 15.82),
    "dark_end": (11, 21.26),
}

# Body plates, in order. Frame 0 is separate (Gale rover deck at 19.7 s).
# Offsets on one file stay more than 10 s apart. Windows were checked clear of
# burned-in labels, arrows and panorama seams.
GALE = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
EDL = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
GALE_NAME = "JPL-20200303-MSLf-0001.mp4"
EDL_NAME = "JPL-20210222-M2020f-0001.mp4"
OPEN = (GALE, 19.70, "crop=608:1080:656:0", GALE_NAME, 1.78)
BODY = [
    (GALE, 58.0, "crop=608:1080:80:0", GALE_NAME, 1.78),
    (EDL, 96.0, "crop=495:880:712:0", EDL_NAME, 2.18),
    (GALE, 42.0, "crop=608:1080:1200:0", GALE_NAME, 1.78),  # @70 x=80 showed a panorama seam on v04
    (EDL, 124.0, "crop=495:880:712:0", EDL_NAME, 2.18),
    (GALE, 130.0, "crop=608:1080:1100:0", GALE_NAME, 1.78),
    (EDL, 154.0, "crop=495:880:712:0", EDL_NAME, 2.18),
    (GALE, 42.0, "crop=608:1080:1200:0", GALE_NAME, 1.78),
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
    # Booth tone from the gap after "Mars." in the opportunity take.
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
    """One frame by index. A keyframe seek sits on the moving plate a few frames early."""
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
    integrated, _peak = measure_level(path)
    return integrated


def limit_db(db: float) -> float:
    return 10 ** (db / 20.0)


def fit_mix(mix: Path, dest: Path) -> tuple[float, float]:
    """Hit AAC integrated -14.0 ±0.5 and true peak ≤ -1.6 dBTP.

    alimiter latency=1. PCM is held about 0.4 dB under the AAC true peak,
    because the 256k encode comes back about 0.1 dB hotter.
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
        if -14.5 <= i <= -13.5 and tp <= -1.6:
            return i, tp
        if not (-14.5 <= i <= -13.5):
            gain += (-14.0 - i) * 0.85
        if tp > -1.6:
            limit -= max(0.2, tp + 1.6 + 0.15)
    raise SystemExit(f"AAC level still outside -14.0±0.5 / ≤-1.6 dBTP: {last}")


def dark_run(path: Path, report: Path) -> dict:
    """Fail a run of 3 or more frames with more than 85% of pixels below luma 20."""
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
    """Fail a run of 15 or more frames with more than 30% of pixels below luma 20."""
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
    # 10 fps on a 30 fps master is every 3rd frame.
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path),
         "-vf", "fps=10,scale=720:1280", str(frames / "%05d.jpg")])
    paths = sorted(frames.glob("*.jpg"))
    tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
    url = re.compile(r"(https?://|www\.|\.int\b|\.gov\b|esa\.int)", re.I)
    copyright_re = re.compile(r"(copyright|all rights reserved|©\s*(?:19|20)\d{2})", re.I)
    file_tag = re.compile(r"[a-z0-9_]{3,}\.(?:mp4|mov|py|json|wav|jpg|png)\b", re.I)
    ids = ("ttghnlxfdss", "j0935", "js6eqj8qdi8")

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
    if not OPP_WAV.exists() or not LONG_WAV.exists():
        raise SystemExit(f"missing VO wavs in {WORK} (opportunity + locked long). No new TTS.")
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
        raise SystemExit(f"first word at {marks['14']}s, need ≤0.15")
    if marks["years_end"] > 1.50:
        raise SystemExit(f"years ends at {marks['years_end']}s, need ≤1.50")
    if marks["Mars"] > 2.50:
        raise SystemExit(f"Mars at {marks['Mars']}s, need ≤2.50")
    payoff_at = 0.70 * total
    if 9.0 <= marks["wind"] < 14.0:
        print(f"NOTE wind at {marks['wind']}s overlaps the 9–14 s title. "
              "c61 joins months straight to the wind line and keeps 23–25 s, "
              "so the wind line cannot also start after 14 s.", flush=True)
    if marks["2018"] < payoff_at:
        raise SystemExit(f"2018 at {marks['2018']}s is before 70% ({payoff_at:.2f}s)")
    if not (23.0 <= total <= 25.05):
        raise SystemExit(f"runtime {total}s outside the audit 23–25 s")
    tail = np.zeros((int(LOOP * SR), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    body = vo_end - FIRST_CUT
    n = max(3, int(np.ceil(body / MAX_PLATE - 1e-6)))
    if n > len(BODY):
        raise SystemExit(f"need {n} body plates, have {len(BODY)}")
    hold = body / n
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.8")
    print(f"plates n={n} hold={hold:.2f}s", flush=True)
    skip_plates = "--reencode" in sys.argv and (WORK / "picture.mp4").exists() and (WORK / "mix.wav").exists()

    rows = []
    lines = []
    t = FIRST_CUT
    plate_specs = [(OPEN[0], OPEN[1], FIRST_CUT, OPEN[2], OPEN[3], OPEN[4], "s00", 0.0)]
    for i in range(n):
        src_p, ss, vf, source, up = BODY[i]
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        plate_specs.append((src_p, ss, length, vf, source, up, f"s{i+1:02d}", t))
        t = round(t + length, 3)
    if skip_plates:
        print("reencode: keeping picture.mp4 and mix.wav", flush=True)
    else:
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

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_i = lufs(bed_raw)
    bed_gain = (vo_i - 20.0) - bed_i
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
         "-vf", "fps=2,scale=180:320,tile=8x8", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x5", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(phone)])
    file_i, file_tp = measure_level(final)
    print(f"master ebur128 {file_i:.2f} LUFS / {file_tp:.2f} dBTP", flush=True)
    if not (-14.5 <= file_i <= -13.5) or file_tp > -1.6:
        raise SystemExit(f"master level {file_i:.2f}/{file_tp:.2f} outside -14.0±0.5 and ≤-1.6")

    cuts_path = OUT / "cuts_v04.json"
    pool_path = OUT / "pool_v04.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": GALE_NAME, "title": "Curiosity Gale Crater panorama, moving"},
        {"file_id": EDL_NAME, "title": "Perseverance descent and touchdown, moving"},
        {"file_id": "end_card_loop_" + OPEN[3], "title": "Loop back to the frame-0 Gale rover deck"},
    ], indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v04",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "Why Did a 90-Day Mars Rover Last 14 Years?",
        "replaces_for_review": "wed11_opening_testA_v02 (scheduled TtgHNLXfDSs). v01, v02 and v03 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…and the sky went dark. Fourteen years on Mars.",
        "brief": {
            "frame_0": "JPL-20200303-MSLf-0001.mp4 Gale rover deck at 19.7 s, moving, 9:16 crop, no Orbit",
            "first_word_s": marks["14"],
            "surprise_s": marks["years_end"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": round(total - marks["dark_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["2018"],
            "surprise_years_end_s": marks["years_end"],
            "mars_s": marks["Mars"],
            "wind_s": marks["wind"],
            "clean_end_s": marks["clean_end"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
            "wind_under_title_note": (
                "Wind starts during the 9–14 s long-title card. c61 joins "
                "months straight to that line and keeps 23–25 s, so the wind "
                "line cannot also start after 14 s."
            ),
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "14 / YEARS (yellow 14), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

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
            print((proc.stdout or "")[-2000:], (proc.stderr or "")[-2000:], flush=True)
    checks_ok = all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa))
    checks_ok = checks_ok and dark["verdict"] == "PASS" and edge["verdict"] == "PASS" and ocr["verdict"] == "PASS"
    if checks_ok:
        open_sheet = OUT / f"{STEM}_open_sheet.jpg"
        publish([
            final, phone, OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_2fps.jpg",
            open_sheet, OUT / f"{STEM}_meta.json",
        ])
    raise SystemExit(0 if checks_ok else 1)


if __name__ == "__main__":
    main()
