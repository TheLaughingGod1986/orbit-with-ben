#!/usr/bin/env python3
"""025 Mars, Wed 11 Nov Short v01: Test A, the long's own opening (J0103; 05_Analytics/tests/SHORTS_TESTS.md).

Does not upload or schedule. Picture is the v03f master (sha256 cce6268c, Claude's FINAL OK 9 Oct) from 0:00,
centre-cropped 608x1080 -> 1080x1920 (1.78x). The cut ends on the sentence end before 38 s ("Could Orbit?", 29.32 s),
then holds picture and music 2.5 s with a 1 s fade. At ~30 s the master returns to the opening Opportunity deck,
so the Short loops to its own frame 0.
Audio is rebuilt the way the master mixed it: the locked VO from 0 s plus 025's own bed at the master's level
(v03f: volume 0.134), so the tail is music only, not the next sentence.
"""
from __future__ import annotations

import hashlib
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

MASTER = FILM / "09_Final-Export/025_MarsRobot_full_rough_v03f.mp4"
MASTER_SHA = "cce6268c"
VO = FILM / "02_Voiceover/mars_robot_vo_v01.mp3"
WORDS = FILM / "07_Edit-Project/full_rough_v03f_pack/mars_robot_words_list.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
BED_VOL = 0.134

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_wed11_opening_v01")
STEM = "wed11_opening_testA_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-11"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

LAST_WORD = "Orbit?"
VO_CUT = 29.90     # "Orbit?" ends 29.32, "In" starts 30.32
HOLD = 2.5         # picture + music past the last word, fade inside the last FADE
FADE = 1.0
CROP_X = (1920 - 608) // 2
# Shot 1 (PIA15115 deck, 0-5.667 s): the centre crop puts the mast shadow on the orange deck, which the gate's Orbit
# heuristic reads as a visor (0.0052, FAIL). x=1150 keeps the deck, drops the long's "Opportunity" label and scores 0.0;
# the 12% push over 1.2 s gives the first-second motion (11.4). Total upscale 1.78 x 1.12 = 1.99x.
SHOT1_END = 5.667
SHOT1_X = 1150
SHOT1_PUSH = 0.12
HOOK = ("BUILT FOR", "90 DAYS")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 26.28  # "So could a robot survive on Mars?" is spoken from here


def run(cmd: list[str]) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout.strip())


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
    font = fit_font(d, max(HOOK, key=len), 190, int(W * 0.84), 8)
    y = int(H * 0.06)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 24
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot", "Survive on Mars?"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
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
         dest])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    for p in (MASTER, VO, WORDS, BED):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if not sha256(MASTER).startswith(MASTER_SHA):
        raise SystemExit("master sha256 does not match the uploaded v03f")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"], "end": w["end"]} for w in words]
    last = next(i for i, w in enumerate(words) if w["word"] == LAST_WORD)
    words = words[:last + 1]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 30.0 <= total < 38.0:
        raise SystemExit(f"total {total} outside the Test A 30-38 s window")

    hook, title = WORK / "hook.png", WORK / "title.png"
    hook_png(hook)
    title_png(title)
    caps = caption_track(words, total)
    whoosh(WORK / "whoosh.wav")

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS) + f"+gte(t,{END_TITLE_FROM})"
    vfade = total - FADE
    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-t", f"{total:.3f}", "-i", MASTER, "-i", hook, "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps,
        "-i", VO, "-i", WORK / "whoosh.wav", "-i", BED,
        "-filter_complex", (
            f"[0:v]split[s1in][s2in];"
            f"[s1in]trim=0:{SHOT1_END},setpts=PTS-STARTPTS,"
            f"crop=608:1080:{SHOT1_X}:0,"
            f"scale=w='trunc({W}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1[s1];"
            f"[s2in]trim={SHOT1_END},setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,"
            f"scale={W}:{H}:flags=lanczos,setsar=1[s2];"
            f"[s1][s2]concat=n=2:v=1:a=0[base];"
            f"[base][1:v]overlay=0:0:enable='between(t,0,{HOOK_END})'[v1];"
            f"[v1][2:v]overlay=0:0:enable='{title_on}'[v2];"
            f"[3:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,"
            f"fade=t=out:st={vfade:.3f}:d={FADE},format=yuv420p[v];"
            f"[4:a]aresample=48000,atrim=0:{VO_CUT},afade=t=out:st={VO_CUT - 0.15:.3f}:d=0.15,apad[va];"
            f"[5:a]aresample=48000,volume=0.45[wh];"
            f"[6:a]aresample=48000,atrim=0:{total},asetpts=PTS-STARTPTS,volume={BED_VOL},"
            f"afade=t=out:st={vfade:.3f}:d={FADE}[mu];"
            f"[va][wh][mu]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        ),
        "-map", "[v]", "-map", "[a]", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 3.5, 7.0, 11.0, 16.0, 21.0, 25.0, 28.0, total - 1.2]
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
        "job": "J0103", "test": "A (the long's own opening, SHORTS_TESTS.md)", "air": AIR,
        "related": LONG_ID, "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "master": {"file": str(MASTER.relative_to(REPO)), "sha256_prefix": MASTER_SHA, "from_s": 0.0, "to_s": total},
        "last_word": {"word": LAST_WORD, "end_s": last_end}, "hold_s": HOLD, "fade_s": FADE,
        "reframe": (f"shot 1 (0-{SHOT1_END} s): crop 608x1080 at x={SHOT1_X} with a {SHOT1_PUSH:.0%} push over 1.2 s; "
                    f"then crop 608x1080 at x={CROP_X}; scale to {W}x{H} (1.78x, 1.99x at the end of the push)"),
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_on_screen": LONG_TITLE, "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "audio": f"locked VO 0-{VO_CUT} s + {BED.relative_to(REPO)} x{BED_VOL} (master level) + whoosh at 0, -14 LUFS",
        "orbit": "none on screen (the master's first Orbit shot is later)",
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
