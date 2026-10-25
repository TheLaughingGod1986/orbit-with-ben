#!/usr/bin/env python3
"""J0931 — 027 Short dM1OgGPAYvw stayed60 re-cut. £0. No upload.

The scheduled master is earth_sudden_air_v02 (sha 4ab2b658). This cut is v03
beside it. v02 is not overwritten.

VO is spliced from the locked long stem (stem_vo_v01i.wav, same clock as
words_v02order.json). "Now imagine the impossible." is removed. The two
named pauses are tightened. The next sentence (oceans, master 44.96–49.50)
is placed before the 1,500 km/h line so that number and the scale card sit
clear of the 9–14 s title. Picture is the locked long plus the existing
row10 air graphic. The end card is gone; the last 1 s is the frame-0 EPIC
plate played back onto frame 0.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

VO_WAV = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/"
    "earth027_v_before_last/earth027_score_v01i/stem_vo_v01i.wav"
)
SCORED = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/"
    "earth027_v_before_last/027_EarthSpin_rough_v01i_scored.mp4"
)
LONG = Path(
    "/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/027_EarthSpin_rough_v01l.mp4"
)
AIR = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/code_out_v03/row10/air.mp4"
)
WORDS = FILM / "02_Voiceover/words_v02order.json"
KIT = FILM / "06_Sound-Effects/kit_v01"
MUSIC = FILM / "05_Music"
BED_NAME = "earth-spin_score_take2_straight_v01j.wav"
WORK = Path("/private/tmp/j0931/work_v03")
OUT = HERE / "06_Final-Exports"
STEM = "earth_sudden_air_v03"
FINAL = OUT / f"{STEM}.mp4"
UAT_NAS = Path(f"/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/{STEM}")

# stem clock == words_v02order. "Now" is at 23.26.
# (src_start, src_end, gap_after). Earth's (25.08) lands at 0.06.
SEGMENTS = [
    (25.02, 27.64, 0.12),  # Earth's rock stops turning in an instant,
    (28.24, 29.38, 0.18),  # but the air does not.
    (30.22, 31.62, 0.18),  # Nothing has told it to stop.
    (44.96, 50.18, 0.18),  # oceans line, plus the take's own pause so "one" starts after the 9–14 s title
    (32.40, 37.68, 0.18),  # At the equator ... one and a half thousand ... hour.
    (38.36, 44.18, 0.00),  # That is faster than the speed of sound ... measured.
]
LOOP = 1.00
FPS = 30
W, H = 1080, 1920
SR = 48000
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
HOOK_END = 2.2
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-10-26"
LONG_TITLE = "What If Earth Stopped Spinning?"
LONG_ID = "6bbbvfCx6zY"

# 9:16 windows. Opening is the DSCOVR EPIC Africa/Nile plate at 82.0 s of v01l
# (the v02 frame-0 shot). Later plates stay <=3.5 s. Loop replays that plate
# backwards so the last frame is frame 0.
EPIC_SS = 83.0
# Pre-scale stays at 1.12 so the 608→1080 step is 1.99×, under the 2.35 fail.
ZOOM = "scale=2150:1210"
PLATES = [
    # name, src, ss, dur, vf (before scale to 1080x1920), source id, offset, upscale
    ("s01_epic", LONG, EPIC_SS, 2.50,
     f"{ZOOM},crop=608:1080:(iw-608)/2:(ih-1080)/2",
     "epic_earth_rotation.mp4", 83.0, 1.99),
    ("s02_iss", LONG, 28.40, 3.20,
     f"{ZOOM},crop=608:1080:(iw-608)/2:ih-1080",
     "027_v01k_span_28.40.mp4", 28.40, 1.99),
    ("s03_gerst", LONG, 74.80, 3.20,
     f"{ZOOM},crop=608:1080:iw*0.38:ih-1080,eq=gamma=1.15:brightness=0.05",
     "Gerst_Earth_timelapses_2017.webm", 316.0, 1.99),
    ("s04_air", AIR, 0.40, 3.20,
     f"{ZOOM},crop=608:1080:iw*0.22:(ih-1080)/2",
     "row10_air.mp4", 0.40, 1.99),
    ("s05_ocean", LONG, 45.30, 3.30,
     "crop=608:1080:(iw-608)/2:0",
     "027_v01k_span_45.30.mp4", 45.30, 1.78),
    ("s06_globe", LONG, 0.55, 3.20,
     f"{ZOOM},crop=608:1080:(iw-608)/2:(ih-1080)/2",
     "epic_spin_v01.mp4", 0.55, 1.99),
    ("s07_foucault", LONG, 144.20, None,
     "crop=608:1080:(iw-608)/2:0",
     "Foucault_pendulum_1.webm", 144.20, 1.78),
]


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lufs(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def vo_len() -> float:
    total = 0.0
    for a, b, gap in SEGMENTS:
        total += (b - a) + gap
    return round(total, 3)


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=6) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, fill[3]))
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def pcm(path: Path, ss: float, length: float, sr: int = SR) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
        "-ac", "2", "-ar", str(sr), "-f", "f32le", "-",
    ])
    x = np.frombuffer(raw, dtype=np.float32)
    if x.size % 2:
        x = x[:-1]
    return x.reshape(-1, 2)


def write_wav(path: Path, samples: np.ndarray, sr: int = SR) -> None:
    import wave
    pcm16 = np.clip(samples, -1, 1)
    pcm16 = (pcm16 * 32767.0).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm16.tobytes())


def atempo(samples: np.ndarray, factor: float) -> np.ndarray:
    """Speed a slice slightly so 'turning' finishes by 1.74 s. Same take, no new TTS."""
    src = WORK / "_atempo_in.wav"
    dst = WORK / "_atempo_out.wav"
    WORK.mkdir(parents=True, exist_ok=True)
    write_wav(src, samples)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", f"atempo={factor:.5f}", str(dst)])
    out = pcm(dst, 0, dur(dst) + 0.05)
    return out


def build_vo() -> tuple[np.ndarray, list[dict], float]:
    words = json.loads(WORDS.read_text())["words"]
    room = pcm(VO_WAV, 27.72, 0.25)
    # First slice runs 1.80 s to the end of "turning"; pull it to 1.74 s.
    first_factor = 1.80 / 1.74
    pieces = []
    cursor = 0.0
    spans = []  # (src_a, src_b, new_a, time_scale)
    for i, (a, b, gap) in enumerate(SEGMENTS):
        chunk = pcm(VO_WAV, a, b - a)
        scale = first_factor if i == 0 else 1.0
        if scale != 1.0:
            chunk = atempo(chunk, scale)
        pieces.append(chunk)
        spans.append((a, b, cursor, scale))
        cursor += len(chunk) / SR
        if gap > 0:
            need = int(round(gap * SR))
            tile = np.resize(room, (need, 2)).astype(np.float32) * 0.15
            pieces.append(tile)
            cursor += gap
    vo = np.concatenate(pieces, axis=0)
    spoken = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        for a, b, new_a, scale in spans:
            if a - 0.02 <= mid <= b + 0.02:
                spoken.append({
                    "w": w["text"],
                    "s": round(new_a + (w["start"] - a) / scale, 3),
                    "e": round(new_a + (w["end"] - a) / scale, 3),
                })
                break
    return vo, spoken, cursor


def caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
    words = sorted(words, key=lambda w: w["s"])
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.35, vo_end)
        # hook owns 0–2 s; the title owns 9–14 s
        if end <= 2.0 or start >= TITLE_OUT and False:
            pass
        text = " ".join(x["w"] for x in c).rstrip(",.?!").upper()
        spans = []
        if start < 2.0:
            start = 2.0
        if start >= end:
            continue
        if start < TITLE_IN and end > TITLE_IN:
            spans.append((start, min(end, TITLE_IN)))
            if end > TITLE_OUT:
                spans.append((TITLE_OUT, end))
        elif TITLE_IN <= start < TITLE_OUT:
            if end > TITLE_OUT:
                spans.append((TITLE_OUT, end))
        else:
            spans.append((start, end))
        for s, e in spans:
            if e - s >= 0.12:
                out.append({"text": text, "s": round(s, 2), "e": round(e, 2)})
    return sorted(out, key=lambda c: c["s"])


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.078)
    rows = [("EARTH", WHITE), ("STOPS", YELLOW)]
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.86:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 250
    for t, c in rows:
        centred(d, y, t, f, c, stroke=8)
        y += lh
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    rows = ["What If Earth", "Stopped Spinning?"]
    while max(d.textlength(r, font=f) for r in rows) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - gap * len(rows)) // 2
    for r in rows:
        centred(d, y, r, f, WHITE, stroke=6)
        y += gap
    im.save(dest)


def caption_png(dest: Path, text: str) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.72)
    while d.textlength(text, font=f) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    centred(d, 1560, text, f, WHITE, stroke=6)
    im.save(dest)


def card_frames(dest: Path, card_in: float, card_out: float) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    rows = [("AIR  1,500 KM/H", 1500, YELLOW), ("SOUND  1,235 KM/H", 1235, WHITE), ("GUST  408 KM/H", 408, WHITE)]
    f = font_for(LINE_H * 0.62)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while max(probe.textlength(t, font=f) for t, _, _ in rows) > W * 0.78:
        f = ImageFont.truetype(FONT, f.size - 2)
    text_h = probe.textbbox((0, 0), "Hg", font=f)[3]
    row_h = text_h + 36
    y0 = 760
    n = max(1, round((card_out - card_in) * FPS))
    max_w = int(W * 0.72)
    for i in range(n):
        t = card_in + i / FPS
        fade = min(1.0, (t - card_in) / 0.35, (card_out - t) / 0.30)
        grow = min(1.0, max(0.0, (t - card_in) / 0.90))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = int(255 * max(0.0, fade))
        for k, (label, value, col) in enumerate(rows):
            y = y0 + k * row_h
            bw = int(max_w * (value / 1500) * grow)
            if bw > 4:
                d.rectangle([120, y + text_h + 6, 120 + bw, y + text_h + 16],
                            fill=(col[0], col[1], col[2], alpha))
            centred_left = 120
            d.text((centred_left, y), label, font=f, fill=(*col[:3], alpha),
                   stroke_width=5, stroke_fill=(0, 0, 0, alpha))
        im.save(dest / f"card_{i:04d}.png")


def recover_bed(length: float) -> Path:
    """The wav left 05_Music. Restore it from the scored master minus the VO stem. £0."""
    dest = MUSIC / BED_NAME
    if dest.exists() and dest.stat().st_size > 1_000_000:
        return dest
    print("recovering bed from v01i_scored − stem_vo_v01i")
    # The sudden-stop cue sits under this Short. A full-length restore is the
    # film's own bed; take the 23–48 s window, which is long enough for the cut.
    ss, take = 20.0, max(length + 2.0, 26.0)
    vo = pcm(VO_WAV, ss, take)
    mix = pcm(SCORED, ss, take)
    n = min(len(vo), len(mix))
    vo, mix = vo[:n], mix[:n]
    # least-squares gain, both channels
    g = float(np.sum(vo * mix) / (np.sum(vo * vo) + 1e-9))
    bed = np.clip(mix - g * vo, -1, 1)
    # fade the splice ends
    fade = int(0.05 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
    bed[:fade] *= ramp
    bed[-fade:] *= ramp[::-1]
    write_wav(dest, bed)
    return dest


def cut_plate(src: Path, ss: float, length: float, vf: str, dest: Path, reverse: bool = False) -> None:
    filt = vf + ",scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    if reverse:
        filt += ",reverse"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(src),
         "-an", "-vf", filt, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-r", "30", str(dest)])


def loop_diff(video: Path) -> float:
    def gray(t: float) -> np.ndarray:
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
            "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
        ])
        return np.frombuffer(raw, dtype=np.uint8).astype(np.float32).reshape(320, 180)
    a, b = gray(0.05), gray(max(0.0, dur(video) - 0.05))
    # mask hook (top) and lower captions
    a[:70, :] = 0
    b[:70, :] = 0
    a[250:, :] = 0
    b[250:, :] = 0
    return float(np.mean(np.abs(a - b)))


def main() -> None:
    for p in (VO_WAV, LONG, AIR, SCORED, WORDS):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    vo, words, vo_end = build_vo()
    total = round(vo_end + LOOP, 3)
    print(f"vo_end {vo_end:.2f} total {total:.2f} words {len(words)}")
    stops = next(w for w in words if w["w"].lower().startswith("stops"))
    turning = next(w for w in words if w["w"].lower().startswith("turning"))
    one = next(w for w in words if w["w"].lower() == "one")
    print(f"Earth's {words[0]['s']:.2f} stops {stops['s']:.2f}-{turning['e']:.2f} one {one['s']:.2f}")
    if words[0]["s"] > 0.15 or turning["e"] > 1.74:
        raise SystemExit("surprise timing missed")
    if one["s"] < 14.0:
        raise SystemExit(f"1,500 still under the 9–14 s title ({one['s']:.2f})")
    if not (18.0 <= total <= 24.0):
        raise SystemExit(f"runtime {total} outside 18–24")

    write_wav(WORK / "stem_vo.wav", vo)
    bed_file = recover_bed(total)
    bed = pcm(bed_file, 0.5, total)
    if len(bed) < int(total * SR):
        reps = int(np.ceil(int(total * SR) / max(len(bed), 1)))
        bed = np.tile(bed, (reps, 1))[: int(total * SR)]
    else:
        bed = bed[: int(total * SR)]
    write_wav(WORK / "stem_bed_raw.wav", bed)

    # plates
    vo_body = vo_end
    used = 0.0
    rows = []
    lines = []
    plates = []
    for name, src, ss, length, vf, source, offset, upscale in PLATES:
        if length is None:
            length = round(vo_body - used, 3)
        plates.append((name, src, ss, length, vf, source, offset, upscale))
        used = round(used + length, 3)
    if abs(used - vo_body) > 0.08:
        raise SystemExit(f"plates {used} != vo {vo_body}")
    t = 0.0
    for name, src, ss, length, vf, source, offset, upscale in plates:
        dest = WORK / f"{name}.mp4"
        cut_plate(src, ss, length, vf, dest)
        lines.append(f"file '{dest.name}'")
        rows.append({
            "row": name, "timeline_in": round(t, 2), "timeline_out": round(t + length, 2),
            "source": source, "upscale": upscale, "framing": {"offset": offset}, "video": True,
        })
        t += length
    loop_mp4 = WORK / "s08_loop.mp4"
    cut_plate(LONG, EPIC_SS, LOOP, plates[0][4], loop_mp4, reverse=True)
    lines.append(f"file '{loop_mp4.name}'")
    rows.append({
        "row": "s08_loop_epic", "timeline_in": round(t, 2), "timeline_out": round(t + LOOP, 2),
        "source": "end_card_loop_epic_earth.mp4", "upscale": 1.99,
        "framing": {"offset": 83.3}, "video": True,
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_chunks(words, vo_end)
    for i, c in enumerate(caps):
        caption_png(WORK / f"cap_{i:02d}.png", c["text"])
    # scale card over the "faster than sound / gust" line, clear of 9–14
    card_in = round(max(14.15, next(w["s"] for w in words if w["w"].lower().startswith("faster"))), 2)
    card_out = round(min(vo_end - 0.15, card_in + 3.6), 2)
    card_frames(WORK / "card", card_in, card_out)

    # audio levels
    vo_path = WORK / "stem_vo.wav"
    # pad VO with the loop tail of room
    room = pcm(VO_WAV, 27.72, 0.25)
    tail_n = int(LOOP * SR)
    tail = np.resize(room, (tail_n, 2)).astype(np.float32) * 0.15
    write_wav(vo_path, np.concatenate([vo, tail], axis=0))
    vo_i = lufs(vo_path)
    bed_i = lufs(WORK / "stem_bed_raw.wav")
    bed_gain = (vo_i - 22.0) - bed_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_bed_raw.wav"),
         "-af", f"volume={bed_gain:.2f}dB", str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    hits = [(whoosh, 0.0), (tick, TITLE_IN), (tick, card_in)]
    inputs, parts = [], []
    for i, (f, at) in enumerate(hits):
        inputs += ["-i", str(f)]
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(hits)))
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(parts) + f";{mix}amix=inputs={len(hits)}:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_gain = (vo_i - 18.0) - lufs(WORK / "stem_sfx_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
         "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", "48000", "-t", f"{total:.3f}", str(WORK / "mix.wav")])

    # overlays
    ff_in = ["-i", str(WORK / "picture.mp4"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "hook.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "title.png"),
             "-framerate", str(FPS), "-i", str(WORK / "card" / "card_%04d.png"),
             "-i", str(WORK / "mix.wav")]
    base = 5
    for i in range(len(caps)):
        ff_in += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.25:alpha=1,fade=t=out:st={TITLE_OUT - 0.25}:d=0.25:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]setpts=PTS-STARTPTS+{card_in}/TB,format=rgba[cd]",
        f"[v2][cd]overlay=0:0:enable='gte(t,{card_in})*lt(t,{card_out})'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "4:a", *enc, "-t", f"{total:.3f}", str(FINAL)])

    diff = loop_diff(FINAL)
    print(f"loop_diff {diff:.2f}")

    # sheets
    run(["ffmpeg", "-y", "-v", "error", "-i", str(FINAL),
         "-vf", "fps=2,scale=180:320,tile=8x6", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(FINAL),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    contact = OUT / f"{STEM}_contact.jpg"
    times = [0.0, 0.5, 1.6, 2.4, 4.5, 7.5, 10.5, 13.0, 16.5, 19.5, total - 0.4]
    tiles = []
    for i, ts in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ts:.2f}", "-i", str(FINAL), "-frames:v", "1",
             "-vf", "scale=216:384", str(p)])
        tiles.append((p, ts))
    canvas = Image.new("RGB", (216 * 4, 410 * 3), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, ts) in enumerate(tiles):
        canvas.paste(Image.open(p), ((i % 4) * 216, (i // 4) * 410))
        d.text(((i % 4) * 216 + 8, (i // 4) * 410 + 388), f"{ts:.1f}s", fill=(255, 255, 255))
    canvas.save(contact, quality=90)

    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": "epic_earth_rotation.mp4", "title": "DSCOVR EPIC daylight Earth"},
        {"file_id": "027_v01k_span_28.40.mp4", "title": "027 v01l ISS Earth limb at 28.40s"},
        {"file_id": "Gerst_Earth_timelapses_2017.webm", "title": "ISS Gerst Earth night city lights"},
        {"file_id": "row10_air.mp4", "title": "027 code graphic air arrows over a real Earth, row10"},
        {"file_id": "027_v01k_span_45.30.mp4", "title": "027 v01l ocean at 45.30s"},
        {"file_id": "epic_spin_v01.mp4", "title": "NASA full-disk sunlit Earth"},
        {"file_id": "Foucault_pendulum_1.webm", "title": "Foucault pendulum swinging"},
        {"file_id": "end_card_loop_epic_earth.mp4", "title": "Loop back to the frame-0 DSCOVR EPIC Earth"},
    ]
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    # The gate reads this file's captions for the last-word time, so it has to
    # exist before the check. The full meta is written again after the gates.
    (OUT / f"{STEM}_meta.json").write_text(json.dumps({"captions": caps}) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--sheet-dir", str(OUT),
         "--vo", str(vo_path), "--json"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--sheet-dir", str(OUT),
         "--vo", str(vo_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate_txt.stdout or gate_txt.stderr)

    sfx = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_path), "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"), "--minutes", f"{total / 60:.3f}"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_sfx.txt").write_text((sfx.stdout or "") + (sfx.stderr or ""))

    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
         "--bed", str(bed_file), "--video", str(FINAL)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_music.txt").write_text((music.stdout or "") + (music.stderr or ""))

    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(FINAL),
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v03.json"), "--no-jitter"],
        capture_output=True, text=True)
    (OUT / "polish_gate_v03.txt").write_text((polish.stdout or "") + (polish.stderr or ""))

    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(FINAL),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v03")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v03.txt").write_text((pqa.stdout or "") + (pqa.stderr or ""))

    mix_lufs = lufs(WORK / "mix.wav")
    meta = {
        "file": str(FINAL),
        "version": "v03",
        "job": "J0931",
        "replaces_for_review": "earth_sudden_air_v02 sha 4ab2b658 (scheduled dM1OgGPAYvw). v02 not overwritten.",
        "sha256": sha256(FINAL),
        "duration_s": dur(FINAL),
        "spoken": " ".join(w["w"] for w in words),
        "words": len(words),
        "long_title": LONG_TITLE,
        "long_id": LONG_ID,
        "air_date": AIR_DATE,
        "spend": "none",
        "brief": {
            "frame_0": "moving DSCOVR EPIC Earth, v01l 83.0s (past the held first frames), tight 9:16 crop, no Orbit",
            "first_word_s": words[0]["s"],
            "surprise_s": f"stops {stops['s']:.2f} turning {turning['e']:.2f}",
            "first_cut_s": 2.50,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": one["s"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff": round(diff, 2),
            "lufs": mix_lufs,
        },
        "vo": {
            "source": str(VO_WAV),
            "cut": "dropped 23.26–25.02 (Now imagine the impossible), pauses 4.38–4.98 and 6.12–6.96 tightened, oceans 44.96–49.50 placed before the 1,500 line",
            "words": words,
        },
        "bed": {
            "file": str(bed_file),
            "how": "recovered from 027_EarthSpin_rough_v01i_scored.mp4 minus stem_vo_v01i.wav (the wav was missing from 05_Music). Not a new generate.",
            "gain_db": round(bed_gain, 2),
        },
        "card": {"in": card_in, "out": card_out, "labels": ["AIR 1,500 KM/H", "SOUND 1,235 KM/H", "GUST 408 KM/H"]},
        "captions": caps,
        "gate_ok": gate.returncode == 0,
        "sfx_ok": sfx.returncode == 0,
        "music_ok": music.returncode == 0,
        "polish_ok": polish.returncode == 0,
        "picture_qa_ok": pqa.returncode == 0,
        "loop_diff": round(diff, 2),
        "lufs": mix_lufs,
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    try:
        if UAT_NAS.parent.exists():
            UAT_NAS.mkdir(parents=True, exist_ok=True)
            for p in OUT.iterdir():
                if p.is_file() and ("v03" in p.name or p.name in {"cuts_v03.json", "pool_v03.json", "polish_gate_v03.json", "polish_gate_v03.txt", "picture_qa_v03.txt"}):
                    shutil.copy2(p, UAT_NAS / p.name)
            src_qa = OUT / "picture_qa_v03"
            if src_qa.exists():
                shutil.copytree(src_qa, UAT_NAS / "picture_qa_v03", dirs_exist_ok=True)
    except Exception as exc:
        print(f"warn UAT: {exc}")

    print("--- gate", gate.returncode)
    print(gate_txt.stdout or gate_txt.stderr)
    print("--- sfx", sfx.returncode)
    print((sfx.stdout or sfx.stderr)[-800:])
    print("--- music", music.returncode)
    print((music.stdout or music.stderr)[-800:])
    print("--- polish", polish.returncode)
    print((polish.stdout or polish.stderr)[-800:])
    print("--- picture", pqa.returncode)
    print((pqa.stdout or pqa.stderr)[-800:])


if __name__ == "__main__":
    main()
