#!/usr/bin/env python3
"""Assemble the Sun 022 Short for Mon 19 Oct (J0021) for Claude's final OK.

Does not upload or schedule. Picture, per SUN_SHORTS_SCRIPTS_v01.md §1:
  open  SDO AIA 304 disc (SVS 5649), limb prominences moving, push-in from 1.5 s
  core  code_graphics core_nolabels (H -> He, centre tightening), title 9-14 s
  climb code_graphics clocks, climb marker only (right-hand crop, last frames held)
  loop  the same disc run up to the frame-0 source time, so the Short loops
No Orbit anywhere (frame 0 rule; Omni beat optional in the script, skipped).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

VO = HERE / "mon19_brighter_fuel_vo_v01.wav"
WORDS = HERE / "words.json"
DISC = HERE / "out_nasa/svs_motion/svs5649_aia304_1024p.mp4"
CORE = FILM / "04_Generated-Clips/code_graphics/core_nolabels.mp4"
CLOCKS = FILM / "04_Generated-Clips/code_graphics/clocks.mp4"
MUSIC = FILM / "05_Music/sun-brighter_score_bed_v01.mp3"

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v01"
STEM = "mon19_brighter_fuel_short_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-10-19"
TITLE = "Why Is the Sun Getting Brighter as It Runs Out of Fuel?"
LONG_TITLE = "Is the Sun Getting Brighter?"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
BG = "0x03060A"

DISC_T0 = 600.0   # source second shown at frame 0 (right-limb prominences)
DISC_SPEED = 6.0  # time-lapse sped up so the limb visibly moves by ~1 s
T_CORE = 4.30     # "Deep in the core" starts 4.42
T_CLOCKS = 17.60  # "About one percent" starts 17.92
T_LOOP = 21.90    # "The full film" starts 22.20
HOLD = 1.0        # picture + music past the last word


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def enc(dest: Path) -> list[str]:
    return ["-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", str(dest)]


def disc_filter(push: bool) -> str:
    # Drop the SVS timestamp strip, blurred fill behind a full-width disc, optional push-in.
    z = f"if(lt(on/{FPS},1.5),1+0.03*on/{FPS}/1.5,min(1.13,1.03+0.10*(on/{FPS}-1.5)/2.8))" if push else "1"
    return (
        f"setpts=PTS/{DISC_SPEED},crop=1024:950:0:0,split[a][b];"
        f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:2,eq=brightness=-0.18[bg];"
        f"[b]scale={W}:-2[fg];[bg][fg]overlay=0:500,"
        f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1"
    )


def seg_open(dest: Path, length: float) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{DISC_T0}", "-i", str(DISC),
         "-filter_complex", f"[0:v]{disc_filter(True)}[v]", "-map", "[v]", "-t", f"{length:.3f}", *enc(dest)])


def seg_loop(dest: Path, length: float) -> None:
    start = DISC_T0 - length * DISC_SPEED
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(DISC),
         "-filter_complex", f"[0:v]{disc_filter(False)}[v]", "-map", "[v]", "-t", f"{length:.3f}", *enc(dest)])


def seg_core(dest: Path, length: float) -> None:
    k = length / dur(CORE)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(CORE),
         "-vf", f"setpts={k:.5f}*PTS,crop=1080:1080:420:0,pad={W}:{H}:0:(oh-ih)/2-40:color={BG},fps={FPS},setsar=1",
         "-t", f"{length:.3f}", *enc(dest)])


def seg_clocks(dest: Path, length: float) -> None:
    tail = 1.9
    start = dur(CLOCKS) - tail
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(CLOCKS),
         "-vf", (f"crop=920:700:1000:330,scale={W}:-2,pad={W}:{H}:0:(oh-ih)/2:color={BG},"
                 f"tpad=stop_mode=clone:stop_duration={length:.3f},fps={FPS},setsar=1"),
         "-t", f"{length:.3f}", *enc(dest)])


def fit_font(draw: ImageDraw.ImageDraw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
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
    font = fit_font(d, "BRIGHTER", 200, int(W * 0.80), 8)
    y = int(H * 0.06)
    y += centred(d, y, "IT'S", font, WHITE, 8) + 24
    centred(d, y, "BRIGHTER", font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why Is the Sun Getting", "Brighter as It Runs", "Out of Fuel?"]
    font = fit_font(d, max(rows, key=len), 60, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    im.save(dest)


def caption_track(words: list[dict], end: float) -> Path:
    """PNG concat list: 1-3 word groups, broken at punctuation, lower third."""
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


def whoosh(dest: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=0.45:sample_rate=48000",
         "-af", "highpass=f=300,lowpass=f=2200,afade=t=in:st=0:d=0.02,afade=t=out:st=0.12:d=0.33,volume=0.55",
         str(dest)])


def main() -> None:
    for p in (VO, WORDS, DISC, CORE, CLOCKS, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]} for w in words]
    vo_s = dur(VO)
    total = round(max(words[-1]["end"], vo_s) + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")

    segs = [
        (WORK / "s1_open.mp4", seg_open, T_CORE),
        (WORK / "s2_core.mp4", seg_core, T_CLOCKS - T_CORE),
        (WORK / "s3_climb.mp4", seg_clocks, T_LOOP - T_CLOCKS),
        (WORK / "s4_loop.mp4", seg_loop, total - T_LOOP),
    ]
    for dest, fn, length in segs:
        fn(dest, length)
    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{d}'\n" for d, _, _ in segs))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(picture)])

    hook, title = WORK / "hook.png", WORK / "title.png"
    hook_png(hook)
    title_png(title)
    caps = caption_track(words, total)
    whoosh(WORK / "whoosh.wav")

    final = OUT / f"{STEM}.mp4"
    fade_at = total - 0.8
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(picture), "-i", str(hook), "-i", str(title),
        "-f", "concat", "-safe", "0", "-i", str(caps),
        "-i", str(VO), "-i", str(WORK / "whoosh.wav"), "-i", str(MUSIC),
        "-filter_complex", (
            f"[0:v][1:v]overlay=0:0:enable='between(t,0,2.2)'[v1];"
            f"[v1][2:v]overlay=0:0:enable='between(t,9,14)'[v2];"
            f"[3:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,format=yuv420p[v];"
            f"[4:a]aresample=48000,apad[va];[5:a]aresample=48000,volume=0.45[wh];"
            f"[6:a]aresample=48000,volume=0.16,afade=t=in:st=0:d=0.3,afade=t=out:st={fade_at:.3f}:d=0.8[mu];"
            f"[va][wh][mu]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        ),
        "-map", "[v]", "-map", "[a]", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", str(final),
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 3.5, 6.0, 10.0, 15.0, 19.0, 23.0, total - 0.1]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1",
             "-vf", "scale=270:480", str(p)])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        d.text((270 * i + 6, 482), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    meta = {
        "job": "J0021", "air": AIR, "file": str(final), "frames": str(sheet),
        "duration_s": dur(final), "vo_s": vo_s,
        "cuts_s": {"open": 0.0, "core": T_CORE, "climb": T_CLOCKS, "loop": T_LOOP, "end": total},
        "hook": "IT'S BRIGHTER (yellow BRIGHTER), 0-2.2 s",
        "title_on_screen": TITLE, "title_window_s": [9.0, 14.0],
        "spoken_end_line": f"The full film: {LONG_TITLE}",
        "orbit": "none",
        "sources": {"open_loop": f"SVS 5649 AIA 304 (from {DISC_T0}s source, x{DISC_SPEED})",
                    "core": str(CORE.relative_to(REPO)), "climb": str(CLOCKS.relative_to(REPO)),
                    "music": str(MUSIC.relative_to(REPO))},
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
