#!/usr/bin/env python3
"""025 Mars, Fri 13 Nov Short v01: Ingenuity Was Built for 5 Flights. It Flew 72. (J0103; MARS_SHORTS_SCRIPTS_v01 §3).

Does not upload or schedule. VO v01 (5 Oct, 23.97 s) + 025's own bed v02 + a whoosh at frame 0.
Picture is NASA/JPL Ingenuity imagery from 07_Edit-Project/nasa_pool_v01/ingenuity. The two Mastcam-Z flight videos
show Ingenuity as a few pixels, so the Short uses the stills and the animated shadow GIF. Small (<=640 px) sources sit
full-width on a feathered blur of themselves so the upscale stays at or under 2.16x; large stills fill the frame.
The last 5.9 s return to the opening shadow in flight, so the Short loops to its own frame 0.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(FILM / "10_Shorts/wed11_opening_testA"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
from _assemble_wed11_opening_testA_v01 import (  # noqa: E402
    WHITE, centred, fit_font, sha256, dur, run, whoosh, YELLOW,
)
import _assemble_wed11_opening_testA_v01 as wed  # noqa: E402

POOL = FILM / "07_Edit-Project/nasa_pool_v01/ingenuity"
VO = HERE / "fri13_ingenuity_72_vo_v01.wav"
WORDS = HERE / "words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
BED_VOL = 0.134
BED_FROM = 150.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_fri13_v01")
STEM = "fri13_ingenuity_72_v01"

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

# (start_s, source, mode, push, push_s, fit_y_offset_px or (crop_x_frac, crop_y_frac));
# mode "fit" = full width on blur, "fill" = cover crop. push_s None = push over the whole shot.
# Shots 0 and 6: the shadow sits in the GIF's top tenth, so it drops 300 px to clear the frame-0 hook, and
# shot 0's push is front-loaded for first-second motion.
SHOTS = [
    (0.00, "PIA24644.gif", "fit", 0.16, 1.0, 300),       # Ingenuity's shadow, third flight (animated)
    (3.98, "PIA24593.jpg", "fill", 0.10, None, (0.5, 0.5)),   # first aerial colour image, from Ingenuity
    (5.88, "PIA26237.jpg", "fill", 0.08, None, (0.45, 0.5)),  # Valinor Hills: the thin Mars sky
    (9.96, "PIA24584.jpg", "fit", 0.10, None, 0),        # rotor shadow from the air
    (14.42, "PIA26244.gif", "fit", 0.08, None, 0),       # Navcam: the missing blade (animated)
    (18.88, "PIA26243.jpg", "fill", 0.10, None, (0.5, 0.5)),  # its own camera: the damaged blade's shadow, grounded
    (20.54, "PIA24644.gif", "fit", 0.10, None, 300),     # back to the opening shadow (loop)
]


def shot_clip(i: int, src: Path, mode: str, push: float, push_s: float | None, place, length: float) -> Path:
    out = WORK / f"shot_{i:02d}.mp4"
    pt = push_s or length
    grow = f"(1+{push}*min(t,{pt:.3f})/{pt:.3f})"
    if mode == "fit":
        inp = ["-ignore_loop", "0", "-i", src] if src.suffix == ".gif" else ["-loop", "1", "-i", src]
        vf = (f"[0:v]fps={FPS},split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:2,eq=brightness=-0.08[bg];"
              f"[b]scale=w='trunc({W}*{grow}/2)*2':h=-2:eval=frame:flags=lanczos[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2+{place}:eval=frame,setsar=1,format=yuv420p[v]")
    else:
        cx, cy = place
        inp = ["-loop", "1", "-i", src]
        with Image.open(src) as im:
            sw, sh = im.size
        # 9:16 window, then scale to 2x the frame so the push never upsamples past the source
        ch = min(sh, int(sw * H / W))
        cw = int(ch * W / H)
        x = int(max(0, min(sw - cw, cx * sw - cw / 2)))
        y = int(max(0, min(sh - ch, cy * sh - ch / 2)))
        vf = (f"[0:v]crop={cw}:{ch}:{x}:{y},scale={W * 2}:{H * 2}:flags=lanczos,fps={FPS},"
              f"scale=w='trunc({W}*{grow}/2)*2':h='trunc({H}*{grow}/2)*2':eval=frame:flags=lanczos,"
              f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", *inp, "-filter_complex", vf, "-map", "[v]", "-t", f"{length:.3f}",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out])
    return out


def main() -> None:
    for p in (VO, WORDS, BED, *(POOL / s[1] for s in SHOTS)):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
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

    hook, title = WORK / "hook.png", WORK / "title.png"
    wed.hook_png(hook)
    wed.title_png(title)
    caps = wed.caption_track(words, total)
    whoosh(WORK / "whoosh.wav")

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS) + f"+gte(t,{END_TITLE_FROM})"
    vfade = total - FADE
    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", base, "-loop", "1", "-t", f"{total:.3f}", "-i", hook, "-loop", "1", "-t", f"{total:.3f}", "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps,
        "-i", VO, "-i", WORK / "whoosh.wav", "-ss", f"{BED_FROM}", "-i", BED,
        "-filter_complex", (
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,{HOOK_END})'[v1];"
            f"[v1][2:v]overlay=0:0:enable='{title_on}'[v2];"
            f"[3:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,"
            f"fade=t=out:st={vfade:.3f}:d={FADE},format=yuv420p[v];"
            f"[4:a]aresample=48000,apad[va];"
            f"[5:a]aresample=48000,volume=0.45[wh];"
            f"[6:a]aresample=48000,atrim=0:{total},asetpts=PTS-STARTPTS,volume={BED_VOL},"
            f"afade=t=in:st=0:d=0.3,afade=t=out:st={vfade:.3f}:d={FADE}[mu];"
            f"[va][wh][mu]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        ),
        "-map", "[v]", "-map", "[a]", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 4.5, 7.5, 11.0, 16.0, 19.5, 22.0, total - 1.2]
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

    meta = {
        "job": "J0103", "air": AIR, "related": LONG_ID, "planned_title": "Ingenuity Was Built for 5 Flights. It Flew 72.",
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "shots": [{"from_s": s[0], "source": s[1], "mode": s[2], "push": s[3], "push_s": s[4]} for s in SHOTS],
        "hook": f"{HOOK[0]} / {HOOK[1]}, 0-{HOOK_END} s", "title_on_screen": LONG_TITLE,
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "audio": f"VO v01 + {BED.relative_to(REPO)} from {BED_FROM} s x{BED_VOL} + whoosh at 0, -14 LUFS",
        "orbit": "none on screen", "credit": "NASA/JPL-Caltech; NASA/JPL-Caltech/ASU/MSSS",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR], capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr)
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
