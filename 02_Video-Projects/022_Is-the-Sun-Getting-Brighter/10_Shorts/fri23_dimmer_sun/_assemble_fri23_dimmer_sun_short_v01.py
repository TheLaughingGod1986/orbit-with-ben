#!/usr/bin/env python3
"""Assemble the Sun 022 Short for Fri 23 Oct (J0022) for Claude's final OK.

Does not upload or schedule. Picture, per SUN_SHORTS_SCRIPTS_v01.md §3:
  open   SDO AIA 304 disc (SVS 5649) in the long's young-Sun grade (-30%, warm-neutral),
         filling the upper frame over a cold ISS sea horizon; push-in from frame 0
  frozen GSFC CI Lab globe, graded cold
  rocks  GSFC CI Lab early-Earth shore, title 9-14 s; then the ISS limb for "greenhouse air"
  today  the same framing as the open, cut from the young grade to today's disc
  loop   the young-grade open, run up to the frame-0 source time, so the Short loops
No Orbit anywhere (Omni skipped: "if Omni is down, stay on the world").
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

VO = HERE / "fri23_dimmer_sun_vo_v01.wav"
WORDS = HERE / "words.json"
NASA = HERE / "out_nasa"
DISC = FILM / "04_Generated-Clips/svs/svs5649.mp4"
SEA = NASA / "iss017e011603.jpg"
GLOBE = NASA / "GSFC_20171208_Archive_e002130.jpg"
SHORE = NASA / "GSFC_20171208_Archive_e000888.jpg"
LIMB = NASA / "iss071e439624.jpg"
MUSIC = FILM / "05_Music/sun-brighter_score_bed_v01.mp3"

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v01"
STEM = "fri23_dimmer_sun_short_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-10-23"
TITLE = "Why Didn't Earth Freeze Under a Dimmer Young Sun?"
LONG_TITLE = "Is the Sun Getting Brighter?"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

# Young-Sun grade from _assemble_sun_first_cut_v03.py: brightness 0.70 x YOUNG_RGB (1.12, 0.98, 0.76).
YOUNG = "colorchannelmixer=rr=0.784:gg=0.686:bb=0.532"
TODAY = "null"
COLD = "colorchannelmixer=rr=0.55:gg=0.72:bb=0.95,eq=brightness=-0.06"

DISC_T0 = 240.0   # source second shown at frame 0
DISC_SPEED = 8.0
T_FROZEN = 4.50   # "Earth" starts 4.70
T_ROCKS = 7.40    # "Rocks" starts 7.56
T_AIR = 10.50     # "The usual answer" starts 10.62
T_TODAY = 16.80   # "It's been brightening" starts 16.94
T_SWAP = 17.30    # cut young -> today's disc on "brightening"
T_LOOP = 19.10    # "The full film" starts 19.26
HOLD = 1.0


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def enc(dest: Path) -> list[str]:
    return ["-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", str(dest)]


def sun_over_sea(dest: Path, start: float, length: float, grade: str, push: bool, drift_end: float) -> None:
    """Disc fills the upper frame (lighten-blended so its black sky drops out) over a drifting sea horizon."""
    n = length * FPS
    # Sea drifts left; the loop drifts drift_end px into frame 0's framing.
    x_expr = f"-1266+{drift_end:.1f}*(1-t/{length:.3f})" if drift_end else "-1266-60*t/4.5"
    z = f"if(lt(on/{FPS},1.0),1+0.22*on/{FPS},min(1.30,1.22+0.08*(on/{FPS}-1.0)/3.5))" if push else "1"
    run(["ffmpeg", "-y", "-v", "error",
         "-ss", f"{start:.3f}", "-i", str(DISC),
         "-loop", "1", "-framerate", str(FPS), "-i", str(SEA),
         "-filter_complex", (
             f"color=c=black:s={W}x{H}:r={FPS}:d={length:.3f}[bg];"
             f"[1:v]scale=-2:2400,{COLD}[sea];"
             f"[bg][sea]overlay=x='{x_expr}':y=200:shortest=1,format=gbrp[base];"
             f"[0:v]setpts=PTS/{DISC_SPEED},crop=1024:950:0:0,{grade},scale=1300:-2,"
             f"crop={W}:ih:(iw-{W})/2:0,pad={W}:{H}:0:0:black,fps={FPS},format=gbrp[sun];"
             f"[base][sun]blend=all_mode=lighten,format=yuv420p,"
             f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih*0.33-(ih*0.33/zoom)':d=1:s={W}x{H}:fps={FPS},setsar=1[v]"),
         "-map", "[v]", "-frames:v", f"{int(round(n))}", *enc(dest)])


def ken_burns(dest: Path, still: Path, length: float, grade: str, z0: float, z1: float) -> None:
    n = int(round(length * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still),
         "-vf", (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},{grade},"
                 f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                 f"setsar=1"),
         "-frames:v", str(n), *enc(dest)])


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
    font = fit_font(d, "DIMMER", 200, int(W * 0.80), 8)
    y = int(H * 0.06)
    y += centred(d, y, "30%", font, YELLOW, 8) + 24
    centred(d, y, "DIMMER", font, WHITE, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why Didn't Earth Freeze", "Under a Dimmer", "Young Sun?"]
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
    for p in (VO, WORDS, DISC, SEA, GLOBE, SHORE, LIMB, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]}
             for w in words if w.get("type", "word") == "word"]
    vo_s = dur(VO)
    total = round(max(words[-1]["end"], vo_s) + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")

    loop_len = total - T_LOOP
    today_src = DISC_T0 + T_FROZEN * DISC_SPEED
    segs = [
        (WORK / "s1_open.mp4", lambda d: sun_over_sea(d, DISC_T0, T_FROZEN, YOUNG, True, 0.0)),
        (WORK / "s2_frozen.mp4", lambda d: ken_burns(d, GLOBE, T_ROCKS - T_FROZEN, COLD, 1.05, 1.15)),
        (WORK / "s3_rocks.mp4", lambda d: ken_burns(d, SHORE, T_AIR - T_ROCKS, "null", 1.10, 1.22)),
        (WORK / "s4_air.mp4", lambda d: ken_burns(d, LIMB, T_TODAY - T_AIR, "null", 1.25, 1.10)),
        (WORK / "s5_young.mp4", lambda d: sun_over_sea(d, today_src, T_SWAP - T_TODAY, YOUNG, False, 0.0)),
        (WORK / "s6_today.mp4", lambda d: sun_over_sea(
            d, today_src + (T_SWAP - T_TODAY) * DISC_SPEED, T_LOOP - T_SWAP, TODAY, False, 0.0)),
        (WORK / "s7_loop.mp4", lambda d: sun_over_sea(
            d, DISC_T0 - loop_len * DISC_SPEED, loop_len, YOUNG, False, 60.0)),
    ]
    for dest, fn in segs:
        fn(dest)
    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{d}'\n" for d, _ in segs))
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
    times = [0.0, 1.0, 3.5, 6.0, 9.0, 12.0, 15.0, 17.0, 18.0, 20.0, total - 0.1]
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
        "job": "J0022", "air": AIR, "file": str(final), "frames": str(sheet),
        "duration_s": dur(final), "vo_s": vo_s,
        "cuts_s": {"open": 0.0, "frozen": T_FROZEN, "rocks": T_ROCKS, "air": T_AIR,
                   "young_disc": T_TODAY, "today_disc": T_SWAP, "loop": T_LOOP, "end": total},
        "hook": "30% DIMMER (yellow 30%), 0-2.2 s",
        "title_on_screen": TITLE, "title_window_s": [9.0, 14.0],
        "spoken_end_line": f"The full film: {LONG_TITLE}",
        "orbit": "none (Omni skipped; script: stay on the world)",
        "sources": {"disc": f"SVS 5649 AIA 304 (from {DISC_T0}s source, x{DISC_SPEED}), young grade = long v03",
                    "sea": SEA.name, "frozen": GLOBE.name, "rocks": SHORE.name, "air": LIMB.name,
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
