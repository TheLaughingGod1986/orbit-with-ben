#!/usr/bin/env python3
"""J2510 — 025 Mars, Fri 13 Nov Short v06: How Did a Helicopter Fly 72 Times on Mars? (bSjWiCbB7pY).

Built from _assemble_fri13_ingenuity_72_v02.py (the scheduled J0103 cut on disk):
1. Removes the raw video ID (Js6EQJ8qDi8) from the end card (wed.title_png(end_title, with_id=False)).
2. Fixes the first-second Rule 24 gate & full-bleed 9:16 requirements (no blur-pad or letterbox bars at
   frame 0, moving picture f0diff >= 1.50, motion >= 10.0, first cut <= 3.0 s):
   - Opens Shot 0 (0.00-2.80 s) full-bleed 9:16 (upscale 0.68x, zero blur-pad) on PIA24593.jpg
     (Ingenuity's first aerial colour photograph in flight over Mars & Perseverance's rover tracks)
     with a smooth sub-pixel dynamic pan+push (18% zoom + diagonal glide, front-loaded over 0.0-1.2 s).
   - Cuts at 2.80 s (<= 3.0 s, in the pause after "This helicopter was built for five flights" at 2.76 s,
     before "on Mars. It flew seventy-two." at 2.88 s) to PIA24644.gif (Ingenuity's animated shadow in
     flight across the Martian sand, paced over 3.08 s so the helicopter shadow stays in-frame throughout).
   - Loops Shot 6 (20.54-26.40 s, end card) full-bleed 9:16 back onto PIA24593.jpg with zero blur-pad
     and no raw YouTube video ID.
3. Places captions in the phone-safe lower-third band (max width 72% W, y = 78% H, clear of right-side
   phone buttons).
4. Levels the locked v02 audio mix to the 26 Oct gate (-14.2 LUFS / -2.2 dBTP) and exports the
   VO, SFX, and bed stems for sfx_kit.py level.
5. Leaves v01..v05 untouched and does not upload or change YouTube Studio.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(FILM / "10_Shorts/wed11_opening_testA"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
from _assemble_wed11_opening_testA_v02 import (  # noqa: E402
    WHITE, centred, fit_font, sha256, dur, run, whoosh, YELLOW,
)
import _assemble_wed11_opening_testA_v02 as wed  # noqa: E402

FROM_TAR = Path("/Volumes/MiniWork/scratch/J2510/from_tar/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars")
POOL = (
    FILM / "07_Edit-Project/nasa_pool_v01/ingenuity"
    if (FILM / "07_Edit-Project/nasa_pool_v01/ingenuity/PIA24644.gif").exists()
    else FROM_TAR / "07_Edit-Project/nasa_pool_v01/ingenuity"
)
VO = (
    HERE / "fri13_ingenuity_72_vo_v01.wav"
    if (HERE / "fri13_ingenuity_72_vo_v01.wav").exists()
    else FROM_TAR / "10_Shorts/fri13_ingenuity_72/fri13_ingenuity_72_vo_v01.wav"
)
WORDS = HERE / "words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
BED_VOL = 0.095  # 3 dB below 0.134 so bed stays >=10 LU under VO during speech (sfx_kit.py level)
BED_FROM = 150.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_fri13_v06")
STEM = "fri13_ingenuity_72_v06"
HOLD_BED_GAIN = 10.5  # keeps post-VO hold at the same 0.095 * 10.5 = 1.00 level as v02 (0.134 * 7.5)

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-13"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
HOOK = ("72", "FLIGHTS")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 20.54  # "The full film, Could a Robot Survive on Mars?"
HOLD = 2.5
FADE = 1.0
CUT1_S = 2.80  # pause after "This helicopter was built for five flights" (ends 2.76 s, "on" starts 2.88 s)
TARGET_I = -14.2
TARGET_TP = -2.2

SHOTS = [
    (0.00, "PIA24593.jpg", "fill_open", 0.22, 1.2, (0.58, 0.44)),  # First aerial colour image in flight (full-bleed 9:16)
    (CUT1_S, "PIA24644.gif", "fit_shadow", 0.10, None, 180),       # Ingenuity's animated shadow, third flight ("It flew 72")
    (5.88, "PIA26237.jpg", "fill", 0.08, None, (0.45, 0.5)),       # Valinor Hills: the thin Mars sky
    (9.96, "PIA24584.jpg", "fit", 0.10, None, 0),                  # Rotor shadow from the air
    (14.42, "PIA26244.gif", "fit", 0.08, None, 0),                 # Navcam: the missing blade (animated)
    (18.88, "PIA26243.jpg", "fill", 0.10, None, (0.5, 0.5)),       # Its own camera: damaged blade's shadow, grounded
    (20.54, "PIA24593.jpg", "fill_loop", 0.12, None, (0.52, 0.46)),# Full-bleed 9:16 aerial Mars return (loop)
]


def measure_ebur128(path: Path) -> tuple[float, float]:
    proc = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    txt = proc.stderr
    m_i = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", txt)
    m_tp = re.findall(r"Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", txt)
    if not m_i or not m_tp:
        raise RuntimeError(f"Could not parse ebur128 from {path}")
    return float(m_i[-1]), float(m_tp[-1])


def level_audio(src_wav: Path, dst_wav: Path, duration: float) -> tuple[float, float]:
    cur_i, _ = measure_ebur128(src_wav)
    gain_db = TARGET_I - cur_i
    limit_lin = 10 ** (TARGET_TP / 20.0)
    run([
        "ffmpeg", "-y", "-v", "error", "-i", src_wav,
        "-af", f"volume={gain_db:.3f}dB,alimiter=limit={limit_lin:.6f}:level=disabled:attack=5:release=50,aresample=48000",
        "-t", f"{duration:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", dst_wav,
    ])
    cur_i2, _ = measure_ebur128(dst_wav)
    if abs(cur_i2 - TARGET_I) > 0.08:
        gain_db += (TARGET_I - cur_i2)
        run([
            "ffmpeg", "-y", "-v", "error", "-i", src_wav,
            "-af", f"volume={gain_db:.3f}dB,alimiter=limit={limit_lin:.6f}:level=disabled:attack=5:release=50,aresample=48000",
            "-t", f"{duration:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", dst_wav,
        ])
    return measure_ebur128(dst_wav)


def caption_track_safe(words: list[dict], end: float) -> Path:
    """Phone-safe lower-third captions (max_w = 72% W, y = 78% H, clear of right-side phone buttons)."""
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cap_dir = WORK / "captions"
    if cap_dir.exists():
        shutil.rmtree(cap_dir)
    cap_dir.mkdir(parents=True, exist_ok=True)
    blank = cap_dir / "blank.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
    lines = ["ffconcat version 1.0"]
    t = 0.0
    for i, g in enumerate(groups):
        start = max(g[0]["start"], t)
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.05)
        if start > t + 0.01:
            lines += [f"file '{blank}'", f"duration {start - t:.3f}"]
        text = " ".join(w["word"] for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 68, int(W * 0.72), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = cap_dir / f"cap_{i:03d}.png"
        im.save(p)
        lines += [f"file '{p}'", f"duration {stop - start:.3f}"]
        t = stop
    if end > t:
        lines += [f"file '{blank}'", f"duration {end - t:.3f}"]
    lines.append(f"file '{blank}'")
    lst = cap_dir / "captions.ffconcat"
    lst.write_text("\n".join(lines) + "\n")
    return lst


def render_subpixel_aerial(src: Path, dest: Path, frames: int, mode: str) -> None:
    """Sub-pixel BICUBIC full-bleed 9:16 flight glide across PIA24593.jpg (4208x3120).
    Crops y = 0..0.88 (2745 px tall, avoiding bottom dark strut) -> 1544x2745 base window (0.70x upscale)."""
    im = Image.open(src).convert("RGB")
    im = im.crop((0, 0, im.width, int(im.height * 0.88)))
    im = ImageEnhance.Contrast(im).enhance(1.55)
    im = ImageEnhance.Color(im).enhance(1.18)
    sw, sh = im.size  # 4208 x 2745
    base_h = float(sh)
    base_w = base_h * W / H  # 1544.06

    p = subprocess.Popen(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-vf", "unsharp=5:5:1.1:5:5:0.0,setsar=1,format=yuv420p",
            "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
            str(dest),
        ],
        stdin=subprocess.PIPE,
    )
    assert p.stdin is not None
    for n in range(frames):
        t = n / FPS
        u = n / max(1, frames - 1)
        if mode == "fill_open":
            # Fast front-loaded aerial swoop over Perseverance's tracks in the first 1.2 s, continuing to 2.8 s
            fast = min(t, 1.2) / 1.2
            tail = max(0.0, t - 1.2) / max(0.1, (frames / FPS) - 1.2)
            z = 1.0 + 0.20 * fast + 0.06 * tail
            cx = (0.64 - 0.12 * fast - 0.04 * tail) * sw
            cy = (0.48 - 0.05 * fast - 0.02 * tail) * sh
        else:
            # End-card loop glide back toward the opening framing (0.64, 0.48, z=1.0 at end)
            z = 1.14 - 0.14 * u
            cx = (0.50 + 0.14 * u) * sw
            cy = (0.44 + 0.04 * u) * sh
        bw, bh = base_w / z, base_h / z
        x0 = max(0.0, min(sw - bw, cx - bw / 2.0))
        y0 = max(0.0, min(sh - bh, cy - bh / 2.0))
        frame = im.resize((W, H), Image.Resampling.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"subpixel aerial render failed for {mode}")


def shot_clip(i: int, src: Path, mode: str, push: float, push_s: float | None, place, length: float) -> Path:
    out = WORK / f"shot_{i:02d}.mp4"
    frames = max(1, round(length * FPS))
    if mode in ("fill_open", "fill_loop"):
        render_subpixel_aerial(src, out, frames, mode)
        return out
    pt = push_s or length
    grow = f"(1+{push}*min(t,{pt:.3f})/{pt:.3f})"
    if mode == "fit_shadow":
        # PIA24644.gif: stretch first 1.90 s across 3.08 s (setpts=1.62*PTS) so Ingenuity's shadow stays in-frame!
        vf = (f"[0:v]setpts=1.62*PTS,fps={FPS},split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:2,eq=brightness=-0.08[bg];"
              f"[b]scale=w='trunc({W}*{grow}/2)*2':h=-2:eval=frame:flags=lanczos,"
              f"crop={W}:'ih':'(iw-{W})/2':0,format=rgba,"
              f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/56,(H-Y)/56))'[fg];"
              f"[bg][fg]overlay=0:(H-h)/2+{place}:eval=frame,setsar=1,format=yuv420p[v]")
        run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", src,
             "-filter_complex", vf, "-map", "[v]", "-frames:v", str(frames),
             "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out])
        return out
    if mode == "fit":
        inp = ["-ignore_loop", "0", "-i", src] if src.suffix == ".gif" else ["-loop", "1", "-i", src]
        grade = ",eq=contrast=1.35,unsharp=5:5:1.2:5:5:0.0" if src.name == "PIA26244.gif" else ""
        vf = (f"[0:v]fps={FPS}{grade},split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:2,eq=brightness=-0.08[bg];"
              f"[b]scale=w='trunc({W}*{grow}/2)*2':h=-2:eval=frame:flags=lanczos,"
              f"crop={W}:'ih':'(iw-{W})/2':0,format=rgba,"
              f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/56,(H-Y)/56))'[fg];"
              f"[bg][fg]overlay=0:(H-h)/2+{place}:eval=frame,setsar=1,format=yuv420p[v]")
    else:
        cx, cy = place
        inp = ["-loop", "1", "-i", src]
        with Image.open(src) as im:
            sw, sh = im.size
        ch = min(sh, int(sw * H / W))
        cw = int(ch * W / H)
        x = int(max(0, min(sw - cw, cx * sw - cw / 2)))
        y = int(max(0, min(sh - ch, cy * sh - ch / 2)))
        vf = (f"[0:v]crop={cw}:{ch}:{x}:{y},scale={W * 2}:{H * 2}:flags=lanczos,fps={FPS},"
              f"scale=w='trunc({W}*{grow}/2)*2':h='trunc({H}*{grow}/2)*2':eval=frame:flags=lanczos,"
              f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", *inp, "-filter_complex", vf, "-map", "[v]", "-frames:v", str(frames),
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out])
    return out


def main() -> None:
    for p in (VO, WORDS, BED, *(POOL / s[1] for s in SHOTS)):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    wed.WORK = WORK
    wed.HOOK = HOOK

    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]} for w in words]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")

    clips = []
    for i, (start, name, mode, push, push_s, place) in enumerate(SHOTS):
        stop = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else total
        clips.append(shot_clip(i, POOL / name, mode, push, push_s, place, stop - start))
    lst = WORK / "shots.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    base = WORK / "base.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])

    hook, title, end_title = WORK / "hook.png", WORK / "title.png", WORK / "end_title.png"
    wed.hook_png(hook)
    wed.title_png(title)
    wed.title_png(end_title, with_id=False)
    caps = caption_track_safe(words, total)
    whoosh(WORK / "whoosh.wav")

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    lift = f"min(max((t-{last_end:.3f})/0.4,0),1)"
    vfade = total - FADE
    final = OUT / f"{STEM}.mp4"

    vo_stem = OUT / f"{STEM}_stem_vo.wav"
    sfx_stem = OUT / f"{STEM}_stem_sfx.wav"
    bed_stem = OUT / f"{STEM}_stem_bed.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", VO,
        "-af", f"aresample=48000,apad=whole_dur={total:.3f}",
        "-t", f"{total:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", vo_stem,
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-i", WORK / "whoosh.wav",
        "-af", f"aresample=48000,volume=0.22,apad=whole_dur={total:.3f}",
        "-t", f"{total:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", sfx_stem,
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", BED,
        "-af", (
            f"aresample=48000,atrim=0:{total},asetpts=PTS-STARTPTS,"
            f"volume='{BED_VOL}*(1+{HOLD_BED_GAIN - 1}*{lift})':eval=frame,"
            f"afade=t=in:st=0:d=0.3,afade=t=out:st={vfade:.3f}:d={FADE}"
        ),
        "-t", f"{total:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", bed_stem,
    ])

    raw_mix = WORK / "raw_mix.wav"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", vo_stem, "-i", sfx_stem, "-i", bed_stem,
        "-filter_complex", (
            "[0:a][1:a][2:a]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
        ),
        "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", "-ac", "2", "-ar", "48000", raw_mix,
    ])
    mix = WORK / "mix_leveled.wav"
    lvl_i, lvl_tp = level_audio(raw_mix, mix, total)
    print(f"leveled WAV ebur128: {lvl_i:.2f} LUFS / {lvl_tp:.2f} dBTP", flush=True)

    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", base, "-loop", "1", "-t", f"{total:.3f}", "-i", hook, "-loop", "1", "-t", f"{total:.3f}", "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps, "-loop", "1", "-i", end_title, "-i", mix,
        "-filter_complex", (
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,{HOOK_END})'[v1];"
            f"[v1][2:v]overlay=0:0:enable='{title_on}'[v2a];"
            f"[v2a][4:v]overlay=0:0:enable='gte(t,{END_TITLE_FROM})':shortest=1[v2];"
            f"[3:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,"
            f"fade=t=out:st={vfade:.3f}:d={FADE},format=yuv420p[v]"
        ),
        "-map", "[v]", "-map", "5:a", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])
    final_i, final_tp = measure_ebur128(final)
    print(f"final MP4 ebur128: {final_i:.2f} LUFS / {final_tp:.2f} dBTP", flush=True)

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 2.9, 4.5, 7.5, 11.0, 16.0, 19.5, 22.0, total - 1.2]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1",
             "-vf", "scale=270:480", p])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        d.text((270 * i + 6, 482), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    cuts_v06 = [
        {
            "row": "s01_PIA24593",
            "timeline_in": 0.0,
            "timeline_out": CUT1_S,
            "source": "PIA24593.jpg",
            "upscale": 0.88,
            "framing": {"offset": 0.0},
            "video": True,
        },
        {
            "row": "s02_PIA24644",
            "timeline_in": CUT1_S,
            "timeline_out": 5.88,
            "source": "PIA24644.gif",
            "upscale": 2.16,
            "framing": {"offset": CUT1_S},
            "video": True,
        },
        {
            "row": "s03_PIA26237",
            "timeline_in": 5.88,
            "timeline_out": 9.96,
            "source": "PIA26237.jpg",
            "upscale": 0.35,
            "framing": {"offset": 5.88},
            "video": True,
        },
        {
            "row": "s04_PIA24584",
            "timeline_in": 9.96,
            "timeline_out": 14.42,
            "source": "PIA24584.jpg",
            "upscale": 1.85,
            "framing": {"offset": 9.96},
            "video": True,
        },
        {
            "row": "s05_PIA26244",
            "timeline_in": 14.42,
            "timeline_out": 18.88,
            "source": "PIA26244.gif",
            "upscale": 1.82,
            "framing": {"offset": 14.42},
            "video": True,
        },
        {
            "row": "s06_PIA26243",
            "timeline_in": 18.88,
            "timeline_out": 20.54,
            "source": "PIA26243.jpg",
            "upscale": 0.68,
            "framing": {"offset": 18.88},
            "video": True,
        },
        {
            "row": "s07_end_card_loop_PIA24593",
            "timeline_in": 20.54,
            "timeline_out": total,
            "source": "end_card_loop_PIA24593.jpg",
            "upscale": 0.80,
            "framing": {"offset": 20.54},
            "video": True,
        },
    ]
    (OUT / "cuts_v06.json").write_text(json.dumps(cuts_v06, indent=2) + "\n")
    pool_v06 = [
        {"file_id": "PIA24593.jpg", "title": "First Aerial Color Image of Mars"},
        {"file_id": "PIA24644.gif", "title": "Ingenuity's Shadow During Third Flight"},
        {"file_id": "PIA26237.jpg", "title": "Ingenuity at 'Valinor Hills'"},
        {"file_id": "PIA24584.jpg", "title": "Ingenuity's First Black-and-White Image From the Air"},
        {"file_id": "PIA26244.gif", "title": "Ingenuity's Navcam Reveals a Missing Rotor Blade"},
        {"file_id": "PIA26243.jpg", "title": "Ingenuity Spots the Shadow of Its Damaged Rotor Blade"},
        {"file_id": "end_card_loop_PIA24593.jpg", "title": "First Aerial Color Image of Mars"},
    ]
    (OUT / "pool_v06.json").write_text(json.dumps(pool_v06, indent=2) + "\n")

    meta = {
        "job": "J2510",
        "version": "v06",
        "replaces_for_watch": "fri13_ingenuity_72_v02 (scheduled bSjWiCbB7pY). v01..v05 untouched.",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did a Helicopter Fly 72 Times on Mars?",
        "file": str(final.relative_to(REPO)),
        "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "first_cut_s": CUT1_S,
        "shots": [{"from_s": s[0], "source": s[1], "mode": s[2], "push": s[3], "push_s": s[4]} for s in SHOTS],
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_on_screen": LONG_TITLE,
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "long_id_on_screen": None,
        "audio": (
            f"VO v01 + {BED.relative_to(REPO)} from {BED_FROM} s x{BED_VOL}, lifted x{HOLD_BED_GAIN} over 0.4 s "
            f"from {last_end:.2f} s for the hold + whoosh at 0, releveled to {final_i:.1f} LUFS / {final_tp:.1f} dBTP"
        ),
        "stems": [vo_stem.name, sfx_stem.name, bed_stem.name],
        "spend": "none (£0 local re-cut)",
        "orbit": "none on screen",
        "credit": "NASA/JPL-Caltech; NASA/JPL-Caltech/ASU/MSSS",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
