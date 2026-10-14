#!/usr/bin/env python3
"""Assemble the Sun 022 Short for Wed 21 Oct, v01 (J0030) for Claude's final OK.

"Could a Robot Survive Touching the Sun?" per SUN_SHORTS_SCRIPTS_v01.md §2. Does not upload or schedule.
No Orbit, no Omni (Claude, 4 Oct): the probe is the robot in the title. Picture:
  open   SVS 14741 PSP_AcrossAcutalSun: Parker Solar Probe crossing the Sun, crop tracks the probe, push-in
  robot  SVS 14036 Parker Solar Probe close-up, the spacecraft lighting up
  shield SVS 14036 heat shield turned to the Sun (title on screen 9-14 s)
  gas    SVS 10925 SDO AIA 171 close-up of the surface, no limb in frame ("no ground to touch")
  loop   SVS 14741 run up to the frame-0 source time, so the Short loops
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

VO = HERE / "wed21_robot_sun_vo_v01.wav"
WORDS = HERE / "words.json"
SVS = FILM / "04_Generated-Clips/svs"
ACROSS = SVS / "svs14741_psp_across_sun.mp4"   # 3840x1080
PSP = SVS / "svs14036_psp_alfven.mp4"          # 1920x1080
SDO = SVS / "svs10925.mp4"                     # 1920x1080
MUSIC = FILM / "05_Music/sun-brighter_score_bed_v01.mp3"

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v01"
STEM = "wed21_robot_sun_short_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-10-21"
TITLE = "Could a Robot Survive Touching the Sun?"
LONG_TITLE = "Is the Sun Getting Brighter?"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

ACROSS_T0 = 4.2    # source second at frame 0: probe already mid-pass over the active region
PROBE_X0 = 700     # probe centre x in 14741: x = X0 + VX*s - AX*s^2 (measured at s = 0, 2, 4, 6, 8)
PROBE_VX = 258
PROBE_AX = 4
TRACK_W, TRACK_H, TRACK_Y = 405, 720, 110
ROBOT_T0, ROBOT_X = 4.0, 736       # 14036 close-up, crop centred on the spacecraft
SHIELD_T0, SHIELD_X = 39.0, 380    # 14036 shield vs Sun, crop holds the Sun's limb and the shield
GAS_T0, GAS_X = 24.5, 1100         # 10925 AIA 171 close-up, right of the limb
T_ROBOT = 2.90    # "Could" starts 3.04
T_SHIELD = 4.95   # "Parker" starts 5.12
T_GAS = 15.15     # "But" starts 15.34
T_LOOP = 20.25    # "The full film" starts 20.38
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


def zoom(z: str) -> str:
    return f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1"


def track(dest: Path, src_start: float, length: float, push: bool) -> None:
    # crop follows the probe across the 3840-wide plate; the corona streams past behind it
    s = f"({src_start:.3f}+t)"
    x = f"{PROBE_X0 - TRACK_W // 2}+{PROBE_VX}*{s}-{PROBE_AX}*{s}*{s}"
    z = f"min(1.12,1+0.04*on/{FPS})" if push else "1"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{src_start:.3f}", "-i", str(ACROSS),
         "-vf", f"fps={FPS},crop={TRACK_W}:{TRACK_H}:'{x}':{TRACK_Y},scale={W}:{H}:flags=lanczos,{zoom(z)}",
         "-t", f"{length:.3f}", *enc(dest)])


def still_crop(dest: Path, src: Path, t0: float, x0: int, length: float, z: str, extra: str = "") -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(src),
         "-vf", f"fps={FPS},crop=608:1080:{x0}:0,{extra}scale={W}:{H}:flags=lanczos,{zoom(z)}",
         "-t", f"{length:.3f}", *enc(dest)])


def seg_open(dest: Path, length: float) -> None:
    track(dest, ACROSS_T0, length, True)


def seg_loop(dest: Path, length: float) -> None:
    start = ACROSS_T0 - length
    if start < 0:
        raise SystemExit(f"loop would start at {start:.2f} s, before the clip")
    track(dest, start, length, False)


def seg_robot(dest: Path, length: float) -> None:
    still_crop(dest, PSP, ROBOT_T0, ROBOT_X, length, f"1.05+0.05*on/{FPS}", "eq=gamma=1.25:contrast=1.08,")


def seg_shield(dest: Path, length: float) -> None:
    still_crop(dest, PSP, SHIELD_T0, SHIELD_X, length, f"min(1.15,1+0.015*on/{FPS})")


def seg_gas(dest: Path, length: float) -> None:
    still_crop(dest, SDO, GAS_T0, GAS_X, length, f"1.10+0.02*on/{FPS}")


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
    font = fit_font(d, "CLOSE", 200, int(W * 0.80), 8)
    y = int(H * 0.06)
    y += centred(d, y, "TOO", font, WHITE, 8) + 24
    centred(d, y, "CLOSE", font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot Survive", "Touching the Sun?"]
    font = fit_font(d, max(rows, key=len), 64, int(W * 0.86), 5)
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
        if len(cur) == 3 or w["word"][-1] in ".,?!:":
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
    for p in (VO, WORDS, ACROSS, PSP, SDO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]} for w in words]
    for w in words:
        # Scribe spells it the US way; the spoken script and the house style are British
        w["word"] = w["word"].replace("kilometers", "kilometres")
    vo_s = dur(VO)
    total = round(max(words[-1]["end"], vo_s) + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")

    segs = [
        (WORK / "s1_open.mp4", seg_open, T_ROBOT),
        (WORK / "s2_robot.mp4", seg_robot, T_SHIELD - T_ROBOT),
        (WORK / "s3_shield.mp4", seg_shield, T_GAS - T_SHIELD),
        (WORK / "s4_gas.mp4", seg_gas, T_LOOP - T_GAS),
        (WORK / "s5_loop.mp4", seg_loop, total - T_LOOP),
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
    times = [0.0, 1.0, 2.5, 4.0, 7.0, 11.0, 16.0, 19.0, 21.5, total - 0.1]
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
        "job": "J0030", "air": AIR, "file": str(final), "frames": str(sheet),
        "duration_s": dur(final), "vo_s": vo_s,
        "cuts_s": {"open": 0.0, "robot": T_ROBOT, "shield": T_SHIELD, "gas": T_GAS, "loop": T_LOOP, "end": total},
        "hook": "TOO CLOSE (yellow CLOSE), 0-2.2 s",
        "title_on_screen": TITLE, "title_window_s": [9.0, 14.0],
        "spoken_end_line": f"The full film: {LONG_TITLE}",
        "orbit": "none (Claude, 4 Oct, PR #99 5982450383: the probe is the robot)",
        "sources": {
            "open_loop": f"SVS 14741 PSP_AcrossAcutalSun_H264.mp4 (from {ACROSS_T0}s, crop {TRACK_W}x{TRACK_H} tracking the probe; loop ends at {ACROSS_T0}s)",
            "robot": f"SVS 14036 Final_PSPAlfvenWave_Version2_NoTransitions_H264.mp4 (from {ROBOT_T0}s, crop x={ROBOT_X})",
            "shield": f"SVS 14036 (from {SHIELD_T0}s, crop x={SHIELD_X})",
            "gas": f"SVS 10925 SDO AIA 171 close-up (from {GAS_T0}s, crop x={GAS_X})",
            "music": str(MUSIC.relative_to(REPO)),
        },
        "credits": [
            "SVS 14741 'Parker Solar Probe: Humanity's Closest Encounter with the Sun': NASA's Goddard Space Flight Center / Johns Hopkins APL (https://svs.gsfc.nasa.gov/14741)",
            "SVS 14036 'Animation: NASA's Parker Solar Probe Enters Solar Atmosphere': NASA's Goddard Space Flight Center / Conceptual Image Lab (https://svs.gsfc.nasa.gov/14036)",
            "SVS 10925 'HD Close up of March 6th X5.4 Flare': NASA/SDO/AIA, NASA's Goddard Space Flight Center (https://svs.gsfc.nasa.gov/10925)",
        ],
        "not_used": "SVS 14865 WISPR corona pass: the 1080 file is over 1.4 GB and was still downloading at the 25-minute run cap; left out (script says 'if available').",
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
