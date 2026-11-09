#!/usr/bin/env python3
"""J0935 c61 — 025 Thu 12 Nov length-test Short v03. £0 local re-cut of N42gKBbD7tE. No upload.

Chief c61:
- Restore the recorded wind clause after "Instead, again and again," so the sentence reads:
  "Instead, again and again, Martian wind and passing dust devils swept its panels clean.
   The team called them cleaning events…"
- Crop inside the rover deck mosaics (PIA18079, PIA17759, PIA07372) to full-bleed with
  zero unfilled black corners.
- Normalise AAC to -14.0 ±0.5 LUFS and TP <= -1.6 dBTP (alimiter latency=1).
- Write _PHONE.mp4 (720x1280) and sha256_manifest.json across repo, OWB UAT and NAS.
- v01 and v02 stay untouched.
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
WORK = Path("/private/tmp/j0935_thu12_v03")
STEM = "thu12_length_test_dust_v03"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT" / "025_thu12_length_test_dust_v03"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/thu12_length_test_dust_v03")

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

# (start, end, gap_before) on the locked long.
# Re-uses the recorded wind clause after "Instead, again and again," so every sentence is whole.
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

# Interior 9:16 crops for the deck mosaics so there are zero unfilled black corners.
STILL_CROPS = {
    "PIA18079.jpg": (916, 986, 2378, 4228),
    "PIA17759.jpg": (538, 507, 807, 1434),
    "PIA07372.jpg": (600, 4450, 900, 1600),
}


def gale_vf(ss: float) -> str:
    if ss < 30:
        x = 656
    elif ss < 50:
        x = 1200
    elif ss < 100:
        x = 80
    elif ss < 120:
        x = 656
    else:
        x = 1100
    return f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"


BODY = [
    ("gale", 19.7),
    ("still", "PIA18079"),
    ("edl", 96.0),
    ("still", "PIA17759"),
    ("gale", 108.0),
    ("still", "PIA22520"),
    ("edl", 124.0),
    ("still", "PIA06739"),
    ("gif", 0.0),
    ("still", "PIA07372"),
    ("gale", 58.0),
    ("still", "PIA17956"),
    ("gale", 42.0),
    ("gale", 130.0),
]
OPEN_SS = 154.0

TITLES = {
    GALE_NAME: "Curiosity Gale panorama, moving",
    EDL_NAME: "Perseverance descent, moving",
    "PIA26673.gif": "Curiosity dusk clouds, moving",
    "PIA18079.jpg": "Opportunity solar panels after a cleaning event",
    "PIA07458.jpg": "Spirit dust devils on the plain",
    "PIA17759.jpg": "Opportunity self-portrait on Mars",
    "PIA22520.jpg": "Curiosity view of the 2018 dust storm",
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
    layers = [(c["s"], c["e"], Image.open(c["png"]).convert("RGBA")) for c in caps]
    frame_bytes = W * H * 3
    dec = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(picture), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", str(mix), "-map", "0:v", "-map", "1:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", str(dest)],
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
            for s, e, layer in layers:
                if s <= t < e:
                    _paste(im, layer)
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
    raise SystemExit(f"AAC level still outside -14.0±0.5 / ≤-1.6 dBTP: {last}")


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
    ids = ("n42gkbbd7te", "j0935", "js6eqj8qdi8")

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
        raise SystemExit(f"first word at {marks['Martian']}s, need ≤0.15")
    if marks["wind"] > 1.50:
        raise SystemExit(f"wind at {marks['wind']}s, need ≤1.50")
    if marks["Martian"] > 2.50:
        raise SystemExit(f"Martian at {marks['Martian']}s, need ≤2.50")
    if 9.0 <= marks["fourteen"] < 14.0:
        raise SystemExit(f"fourteen at {marks['fourteen']}s lands under the 9–14 s title")
    payoff_at = 0.70 * total
    if marks["fourteen"] < payoff_at:
        print(f"NOTE fourteen at {marks['fourteen']}s is before 70% ({payoff_at:.2f}s); "
              "ruling keeps the story order and fixes the opening only", flush=True)
    if not (50.0 <= total <= 60.5):
        raise SystemExit(f"runtime {total}s outside the 50–60 s length test")
    tail_gap = total - marks["off_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((max(1, round(total * SR) - len(audio)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

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
    specs = []
    specs.append(("s00", EDL, OPEN_SS, EDL_NAME, 2.18, open_f / FPS, 0.0, "edl"))
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

    reuse = "--finish-only" in sys.argv
    for name, src_p, ss, source, up, length, tin, kind in specs:
        dest = WORK / f"{name}.mp4"
        if reuse and dest.exists() and dest.stat().st_size > 10000:
            print(f"reuse {name}", flush=True)
            if kind == "still":
                up = still_window(src_p)[5]
        else:
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

    if reuse and (WORK / "s_loop.mp4").exists() and (WORK / "picture.mp4").exists():
        print("reuse picture", flush=True)
    else:
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

    vo_path = WORK / "stem_vo.wav"
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

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x8", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x10", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
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
    pool_items = [{"file_id": k, "title": v} for k, v in TITLES.items()]
    pool_items.append({"file_id": "end_card_loop_" + EDL_NAME, "title": "Loop back to the frame-0 descent"})
    pool_path.write_text(json.dumps(pool_items, indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v03",
        "test": "Short length test, 50-60 s",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?",
        "replaces_for_review": "thu12_length_test_dust_v01 (scheduled N42gKBbD7tE). v01 and v02 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…the sky turning off. Martian wind and passing dust devils swept its panels clean.",
        "brief": {
            "frame_0": f"{EDL_NAME} Perseverance descent at {OPEN_SS}s, moving, 9:16 crop, no Orbit",
            "first_word_s": marks["Martian"],
            "surprise_s": marks["wind"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": round(total - marks["off_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["fourteen"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "wind_s": marks["wind"],
            "clean_end_s": marks["clean_end"],
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": file_i,
            "true_peak_dbtp": file_tp,
            "probe_lufs": aac_i,
            "probe_true_peak_dbtp": aac_tp,
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "THE / WIND (yellow WIND), 0-2.0 s",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v03.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v03.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v03")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v03.txt").write_text(pqa.stdout + pqa.stderr)
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
            print((proc.stdout or "")[-2500:], (proc.stderr or "")[-800:], flush=True)
    checks_ok = all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa))
    checks_ok = checks_ok and dark["verdict"] == "PASS" and edge["verdict"] == "PASS" and ocr["verdict"] == "PASS"
    if checks_ok:
        open_sheet = OUT / f"{STEM}_open_sheet.jpg"
        publish([
            final, phone, OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_2fps.jpg",
            open_sheet, meta_path,
        ])
    raise SystemExit(0 if checks_ok else 1)


if __name__ == "__main__":
    main()
