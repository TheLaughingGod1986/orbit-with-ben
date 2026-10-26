#!/usr/bin/env python3
"""J0935 — 025 Fri 13 Nov Short v03. £0 local re-cut of bSjWiCbB7pY. No upload.

Audit #9: "Mars" and "seventy-two" by 1.5 s from this Short's own VO,
spoken CTA cut, PIA24644.gif stays at frame 0, the s03/s04 still holds
become the two JPL Ingenuity flight videos, first cut 2.50 s, later plates
≤3.8 s, no end card, 0.90 s matched loop.

The scheduled file is already v02. v01 and v02 are not overwritten.
The full audit phrase "On Mars, this helicopter flew seventy-two" cannot
reach 1.5 s: those words alone run past 1.7 s. This cut says
"On Mars, it flew seventy-two flights. This helicopter was built for five."
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

POOL = Path(
    "/private/tmp/j0935_fri13_v03/pool/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars"
    "/07_Edit-Project/nasa_pool_v01/ingenuity"
)
VO = Path("/private/tmp/j0935_fri13_v03/vo.wav")
WORDS = HERE / "words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 220.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_fri13_v03")
STEM = "fri13_ingenuity_72_v03"

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-13"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("72", "FLIGHTS")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.50
MAX_PLATE = 3.55
LOOP = 0.90
XFADE = 0.012

# (start, end, gap_before) on fri13_ingenuity_72_vo_v01.wav. CTA is not here.
CLIPS = [
    (2.84, 3.08, 0.00),   # 0 On
    (3.06, 3.58, 0.00),   # 1 Mars.
    (3.92, 5.46, 0.00),   # 2 It flew seventy-two.
    (0.06, 1.02, 0.10),   # 3 This helicopter
    (1.08, 1.74, 0.06),   # 4 was built for
    (1.84, 2.22, 0.02),   # 5 five
    (2.26, 2.82, 0.02),   # 6 flights
    (5.84, 7.24, 0.12),   # 7 The air there is about
    (7.48, 9.56, 0.08),   # 8 1% as thick as ours.
    (9.92, 14.04, 0.12),  # 9 Its blades spun more than 2,000 times a minute to lift it.
    (14.38, 15.70, 0.12), # 10 In 2024,
    (16.04, 18.52, 0.08), # 11 a damaged blade finally grounded it.
    (18.84, 20.16, 0.10), # 12 It's still standing there.
]
MARKS = {
    "On": (0, 2.88),
    "Mars": (1, 3.10),
    "seventy": (2, 4.62),
    "seventy_end": (2, 5.40),
    "five": (5, 1.88),
    "rpm": (9, 11.86),
    "y2024": (10, 14.72),
    "there_end": (12, 20.12),
}

GIF = POOL / "PIA24644.gif"
V19 = POOL / "JPL-20210419-TECHf-0001.mp4"
V25 = POOL / "JPL-20210425-TECHf-0001.mp4"
# (src, ss, crop_x). Offsets on one file stay more than 10 s apart.
BODY = [
    (V19, 2.0, 370, "JPL-20210419-TECHf-0001.mp4", 2.0),
    (V25, 4.0, 40, "JPL-20210425-TECHf-0001.mp4", 2.0),
    (V19, 33.0, 360, "JPL-20210419-TECHf-0001.mp4", 2.0),
    (V25, 30.0, 80, "JPL-20210425-TECHf-0001.mp4", 2.0),
    (V19, 44.0, 390, "JPL-20210419-TECHf-0001.mp4", 2.0),
    (V25, 52.0, 60, "JPL-20210425-TECHf-0001.mp4", 2.0),
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


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x)) + 1e-12))


def build_vo(src: np.ndarray, words: list) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(3.60 * SR): int(3.78 * SR)]
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
                text = w["text"]
                if text == "flights":
                    text = "flights."
                cap_words.append({
                    "word": text,
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
    font = fit_font(d, "FLIGHTS", 168, int(W * 0.86), 8)
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
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.25)
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


def cut_gif(length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    # Sharp layer is 2.16x (500 → 1080), feathered into a blur fill so the join
    # is not a seam. A sideways drift keeps the opening from reading as a still.
    vf = (
        "fps=30,scale=1080:1080:flags=lanczos,split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=28:3,eq=brightness=0.04:saturation=1.05[bg];"
        "[b]scale=1080:1080:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/96,(H-Y)/96))'[fg];"
        "[bg][fg]overlay=x='(W-w)/2+48*t':y='(H-h)/2-80':eval=frame,"
        "fps=30,setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", str(GIF), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_video(src: Path, ss: float, length: float, crop_x: int, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    # 540 px wide → 1080 is 2.00x. Height stays inside that, with a blur fill.
    vf = (
        f"crop=540:500:{crop_x}:210,split[a][b];"
        f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=18:2[bg];"
        f"[b]scale=1080:-2:flags=lanczos,format=rgba,"
        f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/120,(H-Y)/120))'[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2,fps={FPS},setsar=1,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.15:.3f}",
         "-i", str(src), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


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
    b = gray_frame_n(video, n - 1)
    diff = np.abs(a - b)
    return {
        "whole": round(float(np.mean(diff)), 2),
        "masked": round(float(np.mean(diff[110:240])), 2),
        "frames": n,
    }


def lufs(path: Path) -> float:
    p = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True)
    line = [ln for ln in (p.stderr or "").splitlines() if "I:" in ln and "LUFS" in ln]
    if not line:
        raise SystemExit(f"no LUFS from {path}")
    return float(line[-1].split("I:")[1].split("LUFS")[0].strip())


def main() -> None:
    for p in (VO, WORDS, BED, GIF, V19, V25):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    src = read_wav(VO)
    words = json.loads(WORDS.read_text())["words"]
    audio, marks, cap_words = build_vo(src, words)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    low = spoken.lower()
    if "full film" in low or "could a robot survive one" in low:
        raise SystemExit("CTA or agenda question still in the VO")
    if marks["On"] > 0.15:
        raise SystemExit(f"first word at {marks['On']}s, need ≤0.15")
    if marks["Mars"] > 1.50 or marks["seventy"] > 1.50:
        raise SystemExit(f"Mars {marks['Mars']}s seventy {marks['seventy']}s, need both ≤1.50")
    if 9.0 <= marks["seventy"] < 14.0:
        raise SystemExit("seventy-two lands under the 9–14 s title")
    payoff_at = 0.70 * total
    if marks["y2024"] < payoff_at:
        print(f"NOTE 2024 at {marks['y2024']}s is before 70% ({payoff_at:.2f}s). "
              "Audit #9 puts seventy-two at ≤1.5 s, so the title number is the early surprise.", flush=True)
    if not (18.0 <= total <= 24.05):
        raise SystemExit(f"runtime {total}s outside 18–24 s")
    tail_gap = total - marks["there_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((int(round(LOOP * SR)), 2), np.float32)
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

    rows = []
    print("cutting frame 0 gif", flush=True)
    cut_gif(FIRST_CUT, WORK / "s00.mp4")
    rows.append({
        "row": "s00", "timeline_in": 0.0, "timeline_out": FIRST_CUT,
        "source": "PIA24644.gif", "upscale": 2.16, "video": True,
        "framing": {"offset": 0.0},
    })
    t = FIRST_CUT
    specs = []
    for i in range(n):
        src_p, ss, crop_x, source, up = BODY[i]
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        specs.append((src_p, ss, crop_x, length, source, up, f"s{i+1:02d}", t))
        t = round(t + length, 3)
    for src_p, ss, crop_x, length, source, up, name, tin in specs:
        print(f"cutting {name} {source} @{ss} {length}s", flush=True)
        cut_video(src_p, ss, length, crop_x, WORK / f"{name}.mp4")
        rows.append({
            "row": name, "timeline_in": round(tin, 3), "timeline_out": round(tin + length, 3),
            "source": source, "upscale": up, "video": True,
            "framing": {"offset": ss},
        })
    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines = ["file 's00.mp4'"] + [f"file '{name}.mp4'" for *_, name, _tin in specs] + ["file 's_loop.mp4'"]
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_PIA24644.gif", "upscale": 2.16, "video": True,
        "framing": {"offset": 0.0},
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
    bed_gain = (vo_i - 26.0) - bed_i
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={total - 0.55:.3f}:d=0.45",
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
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={TITLE_OUT - 0.20}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
    ]
    last = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    print("encoding", len(caps), "captions", flush=True)
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

    cuts_path = OUT / "cuts_v03.json"
    pool_path = OUT / "pool_v03.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_path.write_text(json.dumps([
        {"file_id": "PIA24644.gif", "title": "Ingenuity shadow during its third flight, moving"},
        {"file_id": "JPL-20210419-TECHf-0001.mp4", "title": "Ingenuity first flight, Mastcam-Z"},
        {"file_id": "JPL-20210425-TECHf-0001.mp4", "title": "Ingenuity flight, Mastcam-Z"},
        {"file_id": "end_card_loop_PIA24644.gif", "title": "Loop back to the frame-0 Ingenuity shadow"},
    ], indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v03",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did a Helicopter Fly 72 Times on Mars?",
        "replaces_for_review": "fri13_ingenuity_72_v02 (scheduled bSjWiCbB7pY). v01 and v02 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…still standing there. On Mars, it flew seventy-two.",
        "note": ("Audit phrase 'this helicopter flew' cannot fit before 1.5 s. "
                 "Spoken order is 'On Mars, it flew seventy-two flights. This helicopter was built for five.'"),
        "brief": {
            "frame_0": "PIA24644.gif Ingenuity shadow, moving, 9:16 blur fill, no Orbit",
            "first_word_s": marks["On"],
            "surprise_s": marks["seventy"],
            "mars_s": marks["Mars"],
            "seventy_end_s": marks["seventy_end"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": round(total - marks["there_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["y2024"],
            "rpm_s": marks["rpm"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": lufs(WORK / "mix.wav"),
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "72 / FLIGHTS (yellow 72), 0-2.0 s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "bSjWiCbB7pY",
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
    for name, proc in (("sfx", sfx), ("music", music), ("polish", polish), ("picture_qa", pqa)):
        if proc.returncode != 0:
            print(f"--- {name} ---", flush=True)
            print((proc.stdout or "")[-2500:], (proc.stderr or "")[-1500:], flush=True)
    raise SystemExit(0 if all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)) else 1)


if __name__ == "__main__":
    main()
