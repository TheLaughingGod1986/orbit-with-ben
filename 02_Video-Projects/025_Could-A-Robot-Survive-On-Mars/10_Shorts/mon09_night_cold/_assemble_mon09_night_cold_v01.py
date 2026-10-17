#!/usr/bin/env python3
"""025 Mars, Mon 9 Nov Short v01: Could a Robot Survive a Night on Mars? (J0103; MARS_SHORTS_SCRIPTS_v01 §2).

Chief ruling #6101571703: Mon swaps to the kept "minus 90" night script (wed11_night_cold VO v01, nothing new to
spend) on NASA frost + Spirit imagery (the script's no-Omni fallback), hook ONE / NIGHT, the long's id in yellow
under the end title, bed lifted in the post-VO hold, Related = Js6EQJ8qDi8.

Does not upload or schedule. Built on the Fri 13 v02 assembler (mix rendered to its own WAV before the mux).
The last 5.8 s return to the opening frost, so the Short loops to its own frame 0.
"""
from __future__ import annotations

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
from _assemble_wed11_opening_testA_v02 import WHITE, sha256, dur, run, whoosh  # noqa: E402
import _assemble_wed11_opening_testA_v02 as wed  # noqa: E402

POOL = FILM / "07_Edit-Project/nasa_pool_v01"
VO_DIR = FILM / "10_Shorts/wed11_night_cold"
VO = VO_DIR / "wed11_night_cold_vo_v01.wav"
WORDS = VO_DIR / "words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
BED_VOL = 0.134
BED_FROM = 300.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_mon09_v01")
STEM = "mon09_night_cold_v01"
HOLD_BED_GAIN = 7.5

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-09"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
HOOK = ("ONE", "NIGHT")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 19.74  # "The full film, Could a Robot Survive on Mars?"
HOLD = 2.5
FADE = 1.0

# (start_s, source, mode, push, push_s, (crop_x_frac, crop_y_frac, crop_h_frac)); "fill" = 9:16 cover crop
# of crop_h_frac of the source height. Shot 0's push is front-loaded for first-second motion.
SHOTS = [
    (0.00, "frost/PIA11132.jpg", "fill", 0.16, 1.0, (0.5, 0.55, 1.0)),    # frost on the Martian ground at dawn
    (4.10, "dusk_plain/PIA19400.jpg", "fill", 0.08, None, (0.5, 0.5, 1.0)),  # Curiosity: sunset at Gale crater
    (6.00, "frost/PIA11182.jpg", "fill", 0.10, None, (0.5, 0.5, 1.0)),    # Phoenix: morning frost in its trench
    (10.55, "spirit/PIA07371.jpg", "fill", 0.10, None, (0.38, 0.64, 0.42)),  # Spirit self-portrait: deck + panels
    (14.55, "spirit/PIA12142.jpg", "fill", 0.10, None, (0.77, 0.50, 0.80)),  # Spirit's view from Troy: its tracks
    (16.90, "spirit/PIA12457.jpg", "fill", 0.08, None, (0.5, 0.55, 1.0)),  # Spirit's wheels dug in for winter
    (19.55, "frost/PIA11132.jpg", "fill", 0.10, None, (0.5, 0.62, 0.88)),  # back to the opening frost (loop, clear of top sky gutter)
]


def shot_clip(i: int, src: Path, push: float, push_s: float | None, place, length: float) -> Path:
    out = WORK / f"shot_{i:02d}.mp4"
    pt = push_s or length
    grow = f"(1+{push}*min(t,{pt:.3f})/{pt:.3f})"
    cx, cy, hf = place
    with Image.open(src) as im:
        sw, sh = im.size
    ch = min(int(sh * hf), int(sw * H / W))
    cw = int(ch * W / H)
    x = int(max(0, min(sw - cw, cx * sw - cw / 2)))
    y = int(max(0, min(sh - ch, cy * sh - ch / 2)))
    vf = (f"[0:v]crop={cw}:{ch}:{x}:{y},scale={W * 2}:{H * 2}:flags=lanczos,fps={FPS},"
          f"scale=w='trunc({W}*{grow}/2)*2':h='trunc({H}*{grow}/2)*2':eval=frame:flags=lanczos,"
          f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src, "-filter_complex", vf, "-map", "[v]",
         "-t", f"{length:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out])
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
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]}
             for w in words if w.get("type", "word") == "word"]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")

    clips = []
    for i, (start, name, _mode, push, push_s, place) in enumerate(SHOTS):
        stop = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else total
        clips.append(shot_clip(i, POOL / name, push, push_s, place, stop - start))
    lst = WORK / "shots.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    base = WORK / "base.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])

    hook, title, end_title = WORK / "hook.png", WORK / "title.png", WORK / "end_title.png"
    wed.hook_png(hook)
    wed.title_png(title)
    wed.title_png(end_title, with_id=True)
    caps = wed.caption_track(words, total)
    whoosh(WORK / "whoosh.wav")

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    lift = f"min(max((t-{last_end:.3f})/0.4,0),1)"
    vfade = total - FADE
    final = OUT / f"{STEM}.mp4"
    mix = WORK / "mix.wav"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", VO, "-i", WORK / "whoosh.wav", "-ss", f"{BED_FROM}", "-i", BED,
        "-filter_complex", (
            f"[0:a]aresample=48000,apad[va];"
            f"[1:a]aresample=48000,volume=0.45[wh];"
            f"[2:a]aresample=48000,atrim=0:{total},asetpts=PTS-STARTPTS,"
            f"volume='{BED_VOL}*(1+{HOLD_BED_GAIN - 1}*{lift})':eval=frame,"
            f"afade=t=in:st=0:d=0.3,afade=t=out:st={vfade:.3f}:d={FADE}[mu];"
            f"[va][wh][mu]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
        ),
        "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", "-ac", "2", mix,
    ])
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

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 5.0, 8.0, 12.0, 15.5, 18.0, 21.0, total - 1.2]
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
        "job": "J0103", "air": AIR, "related": LONG_ID, "planned_title": "Could a Robot Survive a Night on Mars?",
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "shots": [{"from_s": s[0], "source": s[1], "mode": s[2], "push": s[3], "push_s": s[4], "crop": s[5]}
                  for s in SHOTS],
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s", "title_on_screen": LONG_TITLE,
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "long_id_on_screen": {"id": LONG_ID, "from_s": END_TITLE_FROM, "to_s": total},
        "audio": (f"wed11_night_cold VO v01 + {BED.relative_to(REPO)} from {BED_FROM} s x{BED_VOL}, lifted "
                  f"x{HOLD_BED_GAIN} over 0.4 s from {last_end:.2f} s for the hold + whoosh at 0, -14 LUFS"),
        "orbit": "none on screen", "credit": "NASA/JPL-Caltech; NASA/JPL-Caltech/Cornell; NASA/JPL-Caltech/UA/TAMU",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR, "--id", "iyvWYFP_ETA"], capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr)
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
