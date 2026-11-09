#!/usr/bin/env python3
"""J0935 — 026 Wed 18 Nov Short v02. £0 local re-cut of cwU_0WWeNZ4. No upload.

Audit #11: cut the 0.14–8.02 s setup and the "Could a robot…?" question,
lead with this Short's own "Voyager moves 17 kilometers every second"
("17" by 1.5 s), cut "The full film…". v06 408.25 s (the named SDO disc)
measures f0diff 0.20, so it fails the moving-frame-0 gate. Frame 0 is the
moving Paranal Milky Way at v06 488.15 s (uhd_yb_paranal_02, about 8% black,
no Orbit). First cut 2.74 s, later plates under 4.0 s, no end card, 1.0 s loop.
paranal_06 ends at v06 17.27 s, so that plate stays at 3.62 s.

"75,000 years" is the title's answer, so it stays after the 9–14 s title
and past 70% of the runtime. Lines already on the locked long (Proxima,
1977, fifty years, moonlight, sunlight) fill the middle and keep 18–24 s.
v01 is left untouched.
"""
from __future__ import annotations

import hashlib
import json
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
WORK = Path("/private/tmp/j0935_wed18_v02")
STEM = "wed18_robot_reach_nearest_star_v02"

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
FIRST_CUT = 2.74
LOOP = 1.00
XFADE = 0.012
# Added only between sentences. Slice pads already hold a few hundredths.
GAP_S = 0.05
ROOM = (3.50, 4.05)
UPSCALE = 1.93

# (source, start, end, tempo). Tight pieces inside a sentence have no added gap.
# The 0.18 s breath between "kilometers" and "every", and the 0.30 s breath
# before "75,000", are cut by splitting the slices.
SENTENCES: list[list[tuple[str, float, float, float]]] = [
    [
        ("short", 2.78, 3.24, 1.0),  # Voyager
        ("short", 3.48, 3.68, 1.0),  # 1.
        ("short", 8.40, 9.94, 1.0),  # moves 17 kilometers
        ("short", 10.04, 10.98, 1.0),  # every second.
    ],
    [
        ("long", 346.12, 348.12, 1.0),  # It is not heading towards Proxima.
    ],
    [
        ("long", 299.74, 301.76, 1.0),  # Launched in nineteen seventy-seven.
    ],
    [
        ("long", 302.30, 304.48, 1.0),  # After nearly fifty years of flying,
    ],
    [
        ("long", 364.88, 367.64, 1.0),  # Moonlight reaches you in just over a second.
    ],
    [
        ("long", 368.14, 370.48, 1.0),  # Sunlight takes about eight minutes.
    ],
    [
        ("short", 11.48, 13.46, 1.0),  # At that speed, the trip would take about
        ("short", 13.66, 14.84, 1.0),  # 75,000
        ("short", 14.90, 15.46, 1.0),  # years,
    ],
]

# SDO at 408 s is a still disc (f0diff 0.20). This Paranal shot moves and stays
# under 30% black for the whole open. It is not mon16's paranal_07 plate.
FRAME0 = (488.15, "uhd_yb_paranal_02.mp4", "ESO Paranal Milky Way time-lapse")
# (v06 time, source, credit, max seconds inside that shot).
# paranal_01 is a horizon gutter. paranal_06's shot ends at 17.27 s.
PLATES = [
    (13.55, "uhd_bt_paranal_06.mp4", "ESO Paranal observatory time-lapse", 3.62),
    (153.20, "vltfromvistatimelapse.mp4", "ESO VLT from Vista time-lapse", 3.99),
    (200.60, "ESO_timelapse_La_Silla.webm", "ESO La Silla night-sky time-lapse", 3.99),
    (68.80, "bt_lasilla_crux.mp4", "ESO La Silla Crux time-lapse", 3.99),
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
    return data["words"] if isinstance(data, dict) else data


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


def gray_frames(path: Path, ss: float, length: float) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    frames = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
    frames = frames[: frames.size - (frames.size % (320 * 180))]
    return frames.reshape(-1, 320, 180)


def loop_measures(video: Path) -> dict:
    # Input -ss on this CFR file lands on a B-frame that is not frame 0.
    # Compare decoded frame 0 with the last decoded frame. The centre band
    # masks the hook and the captions.
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


def lufs(path: Path) -> float:
    p = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True)
    line = [ln for ln in p.stderr.splitlines() if "I:" in ln and "LUFS" in ln]
    if not line:
        raise SystemExit(f"no LUFS from {path}")
    return float(line[-1].split("I:")[1].split("LUFS")[0].strip())


def check_vo(marks: dict[str, float], cap_words: list[dict], spoken: str, total: float) -> None:
    low = spoken.lower()
    if "full film" in low or "could a robot" in low or "reach the nearest" in low:
        raise SystemExit(f"cut line still in the stem: {spoken}")
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
        raise SystemExit(f"17 at {seventeen}s, need ≤1.50")
    if marks.get("proxima", 9) > 6.0:
        raise SystemExit(f"Proxima at {marks.get('proxima')}s")
    payoff = marks.get("75,000", 0)
    if payoff < 14.0:
        raise SystemExit(f"75,000 at {payoff}s, still under the 9–14s title")
    if payoff < 0.70 * total:
        raise SystemExit(f"75,000 at {payoff}s before 70% of {total}s")
    if not (18.0 <= total <= 24.0):
        raise SystemExit(f"runtime {total}s outside 18–24")


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
    caps = [p[3] for p in PLATES]
    if sum(caps) + 0.02 < body:
        raise SystemExit(f"plate caps {sum(caps):.2f}s cannot cover {body:.2f}s")
    lengths = [float(c) for c in caps]
    surplus = sum(lengths) - body
    for i in range(len(lengths) - 1, -1, -1):
        if surplus <= 0.001:
            break
        trim = min(surplus, lengths[i] - 2.55)
        lengths[i] -= trim
        surplus -= trim
    if surplus > 0.02:
        raise SystemExit(f"could not fit plates into {body:.2f}s")
    lengths[-1] = round(body - sum(lengths[:-1]), 3)
    if lengths[-1] > caps[-1] + 0.01 or any(L > 4.0 for L in lengths):
        raise SystemExit(f"plate lengths over cap: {lengths}")
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
    bed_gain = (vo_i - 20.0) - lufs(bed_raw)
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
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
         "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(WORK / "mix.wav")])

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

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x4", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "select='lte(t,2)',scale=270:480,tile=3x1", "-frames:v", "1",
         str(OUT / f"{STEM}_open_sheet.jpg")])

    cuts_path = OUT / "cuts_v02.json"
    pool_path = OUT / "pool_v02.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": f0_src, "title": f0_title},
        {"file_id": "loop_uhd_yb_paranal_02.mp4", "title": "Loop back to the ESO Paranal Milky Way time-lapse"},
    ]
    for _ss, source, title, _cap in PLATES[: len(lengths)]:
        pool.append({"file_id": source, "title": title})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    mix_lufs = lufs(WORK / "mix.wav")
    meta = {
        "job": "J0935",
        "version": "v02",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": PLANNED,
        "replaces_for_review": "wed18_robot_reach_nearest_star_v01 (scheduled cwU_0WWeNZ4). v01 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": round(dur(final), 3),
        "spoken": spoken,
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
            "payoff_number_s": marks.get("75,000"),
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": mix_lufs,
            "runtime_s": total,
            "longest_plate_s": round(max([FIRST_CUT, *lengths]), 3),
            "loop_sentence": "…about 75,000 years. Voyager 1 moves 17 kilometers every second.",
        },
        "long_title_on_screen": {
            "title": PLANNED,
            "from_s": TITLE_IN, "to_s": round(title_out, 3),
        },
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "17 / KM/S (yellow KM/S), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", VIDEO_ID,
         "--sheet-dir", str(OUT), "--vo", str(vo_path)],
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
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v02.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v02.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v02")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v02.txt").write_text(pqa.stdout + pqa.stderr)
    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    print((sfx.stdout or sfx.stderr or "")[-500:], flush=True)
    print((music.stdout or music.stderr or "")[-600:], flush=True)
    print((polish.stdout or polish.stderr or "")[-500:], flush=True)
    print((pqa.stdout or pqa.stderr or "")[-800:], flush=True)
    raise SystemExit(0 if all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)) else 1)


if __name__ == "__main__":
    main()
