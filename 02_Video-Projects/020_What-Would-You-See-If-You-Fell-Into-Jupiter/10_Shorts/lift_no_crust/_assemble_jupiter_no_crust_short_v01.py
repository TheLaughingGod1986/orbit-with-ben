#!/usr/bin/env python3
"""020 Jupiter Short v01, lifted from the live long -jmMROGoZCM (J0150, J1063, backlog owb-short-from-locked).

Does not upload or schedule. VO and picture are the uploaded master jupiter_film_v04.mp4 (sha256 a658a785, copied
from the NAS to WORK), VO 125.20-144.62 s (picture from 128.60 s for 0-2.5 s, 112.50 s for 2.5-7.4 s, and 136.00 s
for 7.4-19.92 s): "There is no crust under the paint. ... you step onto atmosphere."
Reframe: centre crop 608x1080 -> 1080x1920 (1.78x). After the last word the picture holds 3 s, crossfading back to
the opening plate (master 128.60 s) so the Short loops to its own frame 0.
Audio: the master VO mix (0-20.40 s) + 020's own 0-credit harmonic pad bed in 05_Music/jupiter_no_crust_short_bed_v01.mp3
(with jupiter_no_crust_short_bed_v01_plan.json, Pace: 60-80 BPM, NOT ...), a house-kit whoosh at frame 0 and a house-kit
tick on the one overlay, two-pass linear loudnorm to -14.0 LUFS / <= -1.6 dBTP.
Teach on screen: one scale card, "1 BAR / EARTH SEA LEVEL", inside the 16:9 centre band, under "about one bar".
The air date is provisional (Chief picks the slot); the gate's opening-plate check is run against it.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
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

WORK = Path("/private/tmp/jupiter020_short_lift")
MASTER = WORK / "jupiter_film_v04.mp4"
MASTER_SHA = "a658a785"
WORDS = WORK / "jupiter_v04_words.json"
KIT = WORK / "kit_v01"
OUT = HERE / "06_Final-Exports"
MUSIC_DIR = FILM / "05_Music"
STEM = "jupiter_no_crust_v01"
BED_NAME = "jupiter_no_crust_short_bed_v01.mp3"

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-16"
LONG_TITLE = "Why You Can't Stand On Jupiter"
LONG_ID = "-jmMROGoZCM"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SRC_IN = 125.20
PIC_IN = 128.60       # bright cloud deck: master 125.2 s opens on a near-dark swirl (frame-0 luma 23)
CUT1_T = 2.00         # first cut at 2.00 s (<= 3.0 s gate_shorts_open requirement; mid=1.00 s has 0 seams)
PIC_B_IN = 112.50     # 2.00-7.40 s: Jupiter cloud bands drift (master s14)
CUT2_T = 7.40
PIC_C_IN = 136.00     # 7.40-19.92 s: cloud descent & amber weather (master s17-s18)
FIRST_WORD, LAST_WORD = "There", "atmosphere."
VO_OUT = 145.60       # "atmosphere." ends 144.62, "Why" starts 145.94
HOLD = 3.0
XFADE = 0.5
CROP_X = (1920 - 608) // 2
PUSH = 0.10           # first-second push on the opening plate
HOOK = ("JUPITER HAS", "NO GROUND")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 18.0
BAND_TOP = (H - 608) // 2
CARD = (6.9, 8.9)     # "about one bar" is spoken 7.26-8.26 s into the Short


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def synthesize_jupiter_short_bed(work: Path) -> Path:
    """Synthesise an own 0-credit harmonic pad + _plan.json in 020/05_Music/ at 68.6 BPM (£0, no spend)."""
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    bed_s = 30.0
    beat_s = 0.875  # 68.6 BPM (inside 60-80 BPM brief)
    n_samples = int(round(bed_s * SR))
    t = np.arange(n_samples, dtype=np.float32) / SR
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    chords = [
        (30, 42, 49, 54, 57, 64),  # F#m7
        (38, 50, 54, 57, 61, 66),  # Dmaj7
        (35, 47, 50, 54, 59, 62),  # Bm7
        (37, 49, 54, 59, 61, 65),  # C#7sus4
        (33, 45, 52, 57, 61, 68),  # Amaj7
    ]
    bar_len = 7.0 * beat_s
    n_bars = int(math.ceil(bed_s / bar_len))
    for b_idx in range(n_bars):
        t0 = b_idx * bar_len
        t1 = min(bed_s, (b_idx + 1) * bar_len + 1.2)
        i0 = int(round(t0 * SR))
        i1 = min(n_samples, int(round(t1 * SR)))
        if i1 <= i0:
            continue
        lt = t[i0:i1] - t0
        d_s = t1 - t0
        fi = np.clip(lt / 1.2, 0.0, 1.0)
        fo = np.clip((d_s - lt) / 1.2, 0.0, 1.0)
        env = np.sin(0.5 * math.pi * fi) * np.sin(0.5 * math.pi * fo)
        notes = chords[b_idx % len(chords)]
        pad_l = np.zeros_like(lt)
        pad_r = np.zeros_like(lt)
        for v_idx, m_note in enumerate(notes):
            f = midi_hz(m_note)
            det = 1.0 + (v_idx - 2.5) * 0.0009
            vib = 1.0 + 0.0011 * np.sin(2.0 * math.pi * (0.16 + 0.03 * v_idx) * lt)
            pl = 2.0 * math.pi * f * det * lt + v_idx * 0.8 + b_idx * 0.4
            pr = 2.0 * math.pi * f * (2.0 - det) * lt + v_idx * 1.3 + b_idx * 0.6
            amp = 0.20 / (1.0 + 0.26 * v_idx)
            h2 = 0.22 * (0.6 + 0.4 * math.sin(0.6 * b_idx + v_idx))
            h3 = 0.08 * (0.6 + 0.4 * math.cos(0.5 * b_idx - v_idx))
            sl = amp * (np.sin(pl * vib) + h2 * np.sin(2.0 * pl) + h3 * np.sin(3.0 * pl))
            sr = amp * (np.sin(pr * vib) + h2 * np.sin(2.0 * pr) + h3 * np.sin(3.0 * pr))
            pan = 0.20 + 0.60 * (v_idx / max(1, len(notes) - 1))
            pad_l += sl * math.cos(0.5 * math.pi * pan)
            pad_r += sr * math.sin(0.5 * math.pi * pan)
        left[i0:i1] += pad_l * env
        right[i0:i1] += pad_r * env

    beat_phase = np.mod(t, beat_s) / beat_s
    pulse_mod = 0.75 + 0.35 * np.exp(-beat_phase / 0.18)
    left *= pulse_mod
    right *= pulse_mod

    arp_pattern = [0, 3, 5, 2, 4, 1, 5, 3]
    for k in range(int(bed_s / beat_s)):
        bt = k * beat_s
        if bt >= bed_s - 1.5:
            break
        chord = chords[int(bt // bar_len) % len(chords)]
        f = midi_hz(chord[arp_pattern[k % len(arp_pattern)]] + (12 if k % 2 == 0 else 0))
        i0 = int(round(bt * SR))
        i1 = min(n_samples, i0 + int(round(0.50 * SR)))
        nt = np.arange(i1 - i0, dtype=np.float32) / SR
        tone = 0.18 * np.clip(nt / 0.012, 0.0, 1.0) * np.exp(-nt / 0.17) * (
            np.sin(2.0 * math.pi * f * nt) + 0.30 * np.sin(3.0 * math.pi * f * nt)
        )
        pan = 0.30 + 0.40 * math.cos(k * 0.8)
        left[i0:i1] += tone * math.cos(0.5 * math.pi * pan)
        right[i0:i1] += tone * math.sin(0.5 * math.pi * pan)

    env_g = np.clip(t / 1.0, 0.0, 1.0) * np.clip((bed_s - t) / 1.2, 0.0, 1.0)
    stereo = np.stack([left * env_g, right * env_g], axis=1)
    peak = float(np.max(np.abs(stereo))) or 1.0
    stereo = stereo * (10.0 ** (-14.0 / 20.0) / peak)

    bed_wav = work / "jupiter_no_crust_short_bed_v01.wav"
    pcm = (np.clip(stereo, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(bed_wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    bed_mp3 = MUSIC_DIR / BED_NAME
    run(["ffmpeg", "-y", "-v", "error", "-i", bed_wav, "-c:a", "libmp3lame", "-b:a", "192k", bed_mp3])

    prompt = (
        "Instrumental cinematic space documentary underscore for Orbit with Ben — 020 Jupiter lift Short "
        "(no crust under the cloud bands). Deep Jovian atmospheric harmonic pad in F# minor / D major / "
        "B minor / C#7sus4 with gentle 68.6 BPM pulse shimmer. Pace: 60-80 BPM. "
        "NOT saturn-rings, NOT sun-brighter, NOT venus, NOT light-speed, NOT mars-robot, "
        "NOT nearest-star, NOT earth-spin, NOT gliese, NOT betelgeuse, NOT jupiter-music."
    )
    plan = {
        "created_at": "2026-10-28T05:45:00+00:00",
        "film": "020_What-Would-You-See-If-You-Fell-Into-Jupiter",
        "project": "jupiter-no-crust-short",
        "script": "020 Short lift_no_crust v01",
        "prompt": prompt,
        "length_ms": int(bed_s * 1000),
        "duration_s": bed_s,
        "model_id": "own_synthesis_v01",
        "force_instrumental": True,
        "generate": False,
        "audio_file": BED_NAME,
        "status": "own 0-credit harmonic pad synthesis (_assemble_jupiter_no_crust_short_v01.py); £0, no spend",
        "sha256": sha256(bed_mp3),
    }
    (MUSIC_DIR / "jupiter_no_crust_short_bed_v01_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return bed_mp3


def fit_font(draw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
    while size > 30:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, size)


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    draw.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return box[3] - box[1]


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, max(HOOK, key=len), 190, int(W * 0.84), 8)
    y = int(H * 0.06)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 24
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path, with_id: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why You Can't", "Stand On Jupiter"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    if with_id:
        centred(d, y + 14, LONG_ID, ImageFont.truetype(FONT, 72), YELLOW, 5)
    im.save(dest)


def card_png(dest: Path) -> None:
    """One-number scale card: a pressure bar filled to the 1 bar mark, lines at 11-12% of the 16:9 band."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    line_h = int(608 * 0.115)
    y = BAND_TOP + 40
    big = fit_font(d, "1 BAR", line_h + 30, int(W * 0.6), 6)
    y += centred(d, y, "1 BAR", big, YELLOW, 6) + 22
    small = fit_font(d, "EARTH SEA LEVEL", line_h, int(W * 0.84), 5)
    y += centred(d, y, "EARTH SEA LEVEL", small, WHITE, 5) + 30
    x0, x1 = int(W * 0.18), int(W * 0.82)
    d.rounded_rectangle((x0, y, x1, y + 26), radius=13, fill=(0, 0, 0, 150), outline=WHITE, width=4)
    im.save(dest)
    Image.new("RGBA", (x1 - x0 - 12, 14), YELLOW + (255,)).save(dest.with_name("card_bar.png"))
    dest.with_name("card_bar_box.json").write_text(json.dumps({"x": x0 + 6, "y": y + 6, "w": x1 - x0 - 12}))


def caption_track(words: list[dict], end: float, work: Path) -> Path:
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cap_dir = work / "captions"
    cap_dir.mkdir(parents=True, exist_ok=True)
    blank = cap_dir / "blank.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
    lines = ["ffconcat version 1.0"]
    t = 0.0
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.6)
        if start > t + 0.01:
            lines += [f"file '{blank}'", f"duration {start - t:.3f}"]
        text = " ".join(w["word"] for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 76, int(W * 0.88), 6)
        centred(d, int(H * 0.83), text, font, WHITE, 6)
        p = cap_dir / f"cap_{i:02d}.png"
        im.save(p)
        lines += [f"file '{p}'", f"duration {stop - start:.3f}"]
        t = stop
    if end > t:
        lines += [f"file '{blank}'", f"duration {end - t:.3f}"]
    lines.append(f"file '{blank}'")
    lst = cap_dir / "captions.ffconcat"
    lst.write_text("\n".join(lines) + "\n")
    return lst


def build_normalized_audio(vo_cut: float, total: float, c0: float, bed_mp3: Path,
                           whoosh: Path, tick: Path, work: Path) -> Path:
    """Mix VO + own 05_Music harmonic pad bed + SFX and two-pass linear loudnorm to -14.0 LUFS / <= -1.6 dBTP."""
    mix_raw = work / "mix_raw.wav"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{SRC_IN:.3f}", "-t", f"{vo_cut:.3f}", "-i", MASTER,
        "-i", bed_mp3,
        "-i", whoosh, "-i", tick,
        "-filter_complex", (
            f"[0:a]aresample=48000,atrim=0:{vo_cut:.3f},afade=t=out:st={vo_cut - 0.3:.3f}:d=0.3,apad[va];"
            f"[1:a]aresample=48000,volume='if(lt(t,{vo_cut - 0.4:.3f}),0.12,0.40)':eval=frame,"
            f"afade=t=in:st=0:d=0.4,atrim=0:{total},afade=t=out:st={total - 0.6:.3f}:d=0.6[mu];"
            f"[2:a]aresample=48000,volume=0.5[wh];"
            f"[3:a]aresample=48000,volume=0.6,adelay={int((c0 + 0.05) * 1000)}:all=1[tk];"
            f"[va][mu][wh][tk]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,atrim=0:{total}[aout]"
        ),
        "-map", "[aout]", "-ar", "48000", "-ac", "2", mix_raw,
    ])
    first_err = subprocess.run([
        "ffmpeg", "-hide_banner", "-i", str(mix_raw),
        "-af", "loudnorm=I=-13.3:TP=-2.2:LRA=11:print_format=json",
        "-f", "null", "-",
    ], capture_output=True, text=True, check=True).stderr
    st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', first_err, re.S)[-1])
    norm = (
        f"loudnorm=I=-13.3:TP=-2.2:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
        f"linear=true,alimiter=limit=0.77:level=disabled"
    )
    mix_norm = work / "mix_norm.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", mix_raw, "-af", norm, "-ar", "48000", "-ac", "2", mix_norm])
    return mix_norm


def main() -> None:
    whoosh, tick = KIT / "sfx_owb_whoosh_soft_v01.wav", KIT / "sfx_owb_tick_ui_v01.wav"
    for p in (MASTER, WORDS, whoosh, tick):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if not sha256(MASTER).startswith(MASTER_SHA):
        raise SystemExit("master sha256 does not match the uploaded v04")
    work = WORK / STEM
    work.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    bed_mp3 = synthesize_jupiter_short_bed(work)

    allw = json.loads(WORDS.read_text())["words"]
    allw = [{"word": w["word"].strip(), "start": w["start"], "end": w["end"]} for w in allw]
    i0 = next(i for i, w in enumerate(allw) if w["word"] == FIRST_WORD and w["start"] >= SRC_IN)
    i1 = next(i for i, w in enumerate(allw) if w["word"] == LAST_WORD and i > i0)
    words = [{"word": w["word"], "start": round(w["start"] - SRC_IN, 3), "end": round(w["end"] - SRC_IN, 3)}
             for w in allw[i0:i1 + 1]]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")
    vo_cut = VO_OUT - SRC_IN
    seg_a = last_end + XFADE
    seg1_d = CUT1_T
    seg2_d = round(CUT2_T - CUT1_T, 3)
    seg3_d = round(seg_a - CUT2_T, 3)

    hook, title, end_title, card = (work / n for n in ("hook.png", "title.png", "end_title.png", "card.png"))
    hook_png(hook)
    title_png(title)
    title_png(end_title, with_id=True)
    card_png(card)
    bar_box = json.loads((work / "card_bar_box.json").read_text())
    caps = caption_track(words, total, work)

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    c0, c1 = CARD
    card_fade = f"fade=t=in:st={c0}:d=0.35:alpha=1,fade=t=out:st={c1 - 0.35:.2f}:d=0.35:alpha=1"
    bar_w = f"max(2,trunc({bar_box['w']}*min(max((t-{c0 + 0.2})/0.9,0),1)))"
    mix_norm = build_normalized_audio(vo_cut, total, c0, bed_mp3, whoosh, tick, work)

    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{PIC_IN:.3f}", "-t", f"{seg1_d:.3f}", "-i", MASTER,
        "-ss", f"{PIC_B_IN:.3f}", "-t", f"{seg2_d:.3f}", "-i", MASTER,
        "-ss", f"{PIC_C_IN:.3f}", "-t", f"{seg3_d:.3f}", "-i", MASTER,
        "-ss", f"{PIC_IN:.3f}", "-t", f"{HOLD:.3f}", "-i", MASTER,
        "-loop", "1", "-i", hook, "-loop", "1", "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps,
        "-loop", "1", "-i", end_title, "-loop", "1", "-i", card, "-loop", "1", "-i", work / "card_bar.png",
        "-i", mix_norm,
        "-filter_complex", (
            f"[0:v]fps={FPS},crop=608:1080:{CROP_X}:0,"
            f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a1];"
            f"[1:v]fps={FPS},crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[a2];"
            f"[2:v]fps={FPS},crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[a3];"
            f"[a1][a2][a3]concat=n=3:v=1:a=0,fps={FPS}[a];"
            f"[3:v]fps={FPS},crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[b];"
            f"[a][b]xfade=transition=fade:duration={XFADE}:offset={last_end:.3f},split[b0][bhz];"
            f"[bhz]crop=1080:300:0:410,boxblur=4:40:4:2,format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/35,(300-Y)/35))'[hz];"
            f"[b0][hz]overlay=0:410:enable='between(t,7.4,15.4)',format=yuv420p[base];"
            f"[4:v]format=rgba[hk];[base][hk]overlay=0:0:enable='between(t,0,{HOOK_END})':shortest=1[v1];"
            f"[5:v]format=rgba[tt];[v1][tt]overlay=0:0:enable='{title_on}':shortest=1[v2a];"
            f"[7:v]format=rgba[et];[v2a][et]overlay=0:0:enable='gte(t,{END_TITLE_FROM})':shortest=1[v2b];"
            f"[8:v]fps={FPS},format=rgba,{card_fade}[cd];"
            f"[v2b][cd]overlay=0:0:enable='between(t,{c0},{c1})':shortest=1[v2c];"
            f"[9:v]fps={FPS},format=rgba,scale=w='{bar_w}':h=14:eval=frame,{card_fade}[br];"
            f"[v2c][br]overlay={bar_box['x']}:{bar_box['y']}:enable='between(t,{c0 + 0.2},{c1})':shortest=1[v2];"
            f"[6:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,format=yuv420p[v]"
        ),
        "-map", "[v]", "-map", "10:a", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 3.0, 5.5, 7.8, 11.0, 15.0, 18.5, 20.5, total - 0.3]
    tiles = []
    for i, t in enumerate(times):
        p = work / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1",
             "-vf", "scale=270:480", p])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        d.text((270 * i + 6, 482), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    meta = {
        "job": "J1063", "air_provisional": AIR, "related": LONG_ID, "title_on_screen": LONG_TITLE,
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "master": {"file": "020/09_Final-Export/jupiter_film_v04.mp4 (NAS)", "sha256_prefix": MASTER_SHA,
                   "from_s": SRC_IN, "to_s": round(SRC_IN + last_end, 3),
                   "picture_from_s": PIC_IN,
                   "picture_note": "0-2.0 s master 128.6 s, 2.0-7.4 s master 112.5 s, 7.4-19.42 s master 136.0 s"},
        "spoken": " ".join(w["word"] for w in words), "words": len(words),
        "last_word": {"word": LAST_WORD, "end_s": last_end}, "hold_s": HOLD,
        "loop": f"{XFADE} s crossfade from {last_end} s back to the opening plate (master {PIC_IN} s)",
        "reframe": f"crop 608x1080 at x={CROP_X}, scale {W}x{H} (1.78x), {PUSH:.0%} push over 1.2 s at the open",
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "overlay": {"kind": "one-number scale card", "text": ["1 BAR", "EARTH SEA LEVEL"], "window_s": CARD,
                    "spoken": "about one bar, the weight of earth's air at sea level"},
        "audio": (f"master VO mix 0-{vo_cut:.2f} s + own 05_Music/{BED_NAME} harmonic pad bed (68.6 BPM, £0), "
                  "house kit whoosh at 0 + tick on the card, -14.0 LUFS / <= -1.6 dBTP"),
        "music_bed": f"05_Music/{BED_NAME}",
        "orbit": "none on screen", "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR, "--id", "23KZK7OjsEE"], capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr)
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
