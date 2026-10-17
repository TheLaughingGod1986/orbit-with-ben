#!/usr/bin/env python3
"""025 Mars, Thu 12 Nov Short length test v01 (J0134; AGENTS.md -> Packaging 5, Chief OK 11 Oct 2026).

One 50-60 s Short lifted from the locked v03f master (sha256 cce6268c, uploaded as Js6EQJ8qDi8). Nothing is spent:
the picture is the master, the VO is the locked long VO, the bed is 025's own laid bed (2.5 dB under the master's level while the VO speaks), and the
frame-0 whoosh is from the house SFX kit (06_Sound-Effects/kit_v01, own synthesis).

Stretch: master 254.70 s ("Opportunity should have starved within months.") to the end of "It was the sky turning
off." (306.82 s), then 2.5 s of picture and music past the last word. The hold cuts back to the opening plate
(PIA22909, the master from 254.70 s again), so the last seconds loop to frame 0, and fades out over the last 1 s.
Picture is centre-cropped 608x1080 -> 1080x1920 (1.78x); the opening shot gets a 12% push over 1.2 s for the
first-second motion. Not the subject of that week's Mon/Wed/Fri Shorts (Night Cold, the opening, Ingenuity).

Does not upload or schedule.
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
BED_VOL = 0.10  # 2.5 dB under the master's 0.134 while the VO speaks: sfx_kit.py level needs the bed 10 LU under
BED_DIP = (2.1, 3.3, 0.55)  # the bed swells in at 2.3 s under the onset of "Instead"; ramped dip to 55%
WHOOSH = FILM / "06_Sound-Effects/kit_v01/sfx_owb_whoosh_soft_v01.wav"
WHOOSH_VOL = 0.12

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_thu12_lentest_v01")
STEM = "thu12_length_test_dust_v01"
HOLD_BED_GAIN = 3.75  # post-VO hold at 0.375, the Wed v02 hold level (Chief ruling), over BED_VOL

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-12"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SRC_IN = 254.70           # "Opportunity" starts 254.80; row 20 (PIA22909) runs 254.47-258.87
FIRST_WORD = "Opportunity"
LAST_WORD_END = 306.82    # "off." of "It was the sky turning off."
VO_CUT_ABS = 307.30       # next word "Why" starts 308.44
HOLD = 2.5
FADE = 1.0
CROP_X = (1920 - 608) // 2
SHOT1_END = 258.8667 - SRC_IN
SHOT1_PUSH = 0.12
HOOK = ("SAVED BY", "THE WIND")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)


def run(cmd: list) -> None:
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


def title_png(dest: Path, with_id: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot", "Survive on Mars?"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    if with_id:
        centred(d, y + 14, LONG_ID, ImageFont.truetype(FONT, 72), YELLOW, 5)
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
        start = max(g[0]["start"], t)
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.6)
        if start > t + 0.01:
            lines += [f"file '{blank}'", f"duration {start - t:.3f}"]
        text = " ".join(w["word"] for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 76, int(W * 0.88), 6)
        centred(d, int(H * 0.83), text, font, WHITE, 6)
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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    for p in (MASTER, VO, WORDS, BED, WHOOSH):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if not sha256(MASTER).startswith(MASTER_SHA):
        raise SystemExit("master sha256 does not match the uploaded v03f")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [{"word": (w.get("word") or w.get("text")).strip(), "start": w["start"] - SRC_IN, "end": w["end"] - SRC_IN}
             for w in words if SRC_IN <= w["start"] and w["end"] <= LAST_WORD_END + 0.01]
    if words[0]["word"] != FIRST_WORD or not words[-1]["word"].startswith("off"):
        raise SystemExit(f"stretch words wrong: {words[0]['word']} .. {words[-1]['word']}")
    last_end = words[-1]["end"]
    vo_cut = VO_CUT_ABS - SRC_IN
    total = round(last_end + HOLD, 3)
    if not 50.0 <= total <= 60.0:
        raise SystemExit(f"total {total} outside the 50-60 s length-test band")
    tail = total - vo_cut

    hook, title, end_title = WORK / "hook.png", WORK / "title.png", WORK / "end_title.png"
    hook_png(hook)
    title_png(title)
    title_png(end_title, with_id=True)
    caps = caption_track(words, total)

    # Separate stems at their mix levels, for sfx_kit.py level (Polish pass 1).
    vo_stem, sfx_stem, bed_stem = WORK / "stem_vo.wav", WORK / "stem_sfx.wav", WORK / "stem_bed.wav"
    lift = f"min(max((t-{vo_cut})/0.4,0),1)"
    d0, d1, dg = BED_DIP
    dip = f"(1-{1 - dg}*min(max(min((t-{d0})/0.3,({d1}-t)/0.3),0),1))"
    vfade = total - FADE
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{SRC_IN}", "-t", f"{vo_cut}", "-i", VO, "-af",
         f"aresample=48000,afade=t=out:st={vo_cut - 0.15:.3f}:d=0.15,apad,atrim=0:{total}",
         "-ac", "2", vo_stem])
    run(["ffmpeg", "-y", "-v", "error", "-i", WHOOSH, "-af",
         f"aresample=48000,volume={WHOOSH_VOL},apad,atrim=0:{total}", "-ac", "2", sfx_stem])
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{SRC_IN}", "-t", f"{total}", "-i", BED, "-af",
         f"aresample=48000,asetpts=PTS-STARTPTS,volume='{BED_VOL}*(1+{HOLD_BED_GAIN - 1}*{lift})*{dip}':eval=frame,"
         f"afade=t=out:st={vfade:.3f}:d={FADE}", "-ac", "2", bed_stem])

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{SRC_IN}", "-t", f"{vo_cut:.3f}", "-i", MASTER,
        "-ss", f"{SRC_IN}", "-t", f"{tail:.3f}", "-i", MASTER,
        "-i", hook, "-i", title, "-f", "concat", "-safe", "0", "-i", caps,
        "-loop", "1", "-i", end_title,
        "-i", vo_stem, "-i", sfx_stem, "-i", bed_stem,
        "-filter_complex", (
            f"[0:v]setpts=PTS-STARTPTS,split[s1in][s2in];"
            f"[s1in]trim=0:{SHOT1_END:.3f},setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,"
            f"scale=w='trunc({W}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1[s1];"
            f"[s2in]trim={SHOT1_END:.3f},setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,"
            f"scale={W}:{H}:flags=lanczos,setsar=1[s2];"
            f"[1:v]setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1[s3];"
            f"[s1][s2][s3]concat=n=3:v=1:a=0,fps={FPS},split[b0][bhz];"
            f"[bhz]crop=1080:160:0:0,boxblur=4:36:4:2,format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,(160-Y)/40)'[hz];"
            f"[b0][hz]overlay=0:0:enable='between(t,44.0,49.0)',format=yuv420p[base];"
            f"[base][2:v]overlay=0:0:enable='between(t,0,{HOOK_END})'[v1];"
            f"[v1][3:v]overlay=0:0:enable='{title_on}'[v2a];"
            f"[v2a][5:v]overlay=0:0:enable='gte(t,{last_end:.3f})':shortest=1[v2];"
            f"[4:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,"
            f"fade=t=out:st={vfade:.3f}:d={FADE},format=yuv420p[v];"
            f"[6:a][7:a][8:a]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[a]"
        ),
        "-map", "[v]", "-map", "[a]", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 4.0, 8.0, 11.0, 16.0, 22.0, 28.0, 34.0, 40.0, 46.0, 51.0, 53.0, total - 0.9]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1",
             "-vf", "scale=216:384", p])
        tiles.append(p)
    cols = 7
    canvas = Image.new("RGB", (216 * cols, 404 * 2), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        x, y = 216 * (i % cols), 404 * (i // cols)
        canvas.paste(Image.open(p), (x, y))
        d.text((x + 6, y + 388), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    for s in (vo_stem, sfx_stem, bed_stem):
        (OUT / f"{STEM}_{s.stem}.wav").write_bytes(s.read_bytes())

    meta = {
        "job": "J0134", "test": "Short length test, 50-60 s (AGENTS.md -> Packaging 5)", "air": AIR,
        "related": LONG_ID, "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "master": {"file": str(MASTER.relative_to(REPO)), "sha256_prefix": MASTER_SHA,
                   "from_s": SRC_IN, "to_s": VO_CUT_ABS, "loop_tail_from_s": SRC_IN, "loop_tail_s": round(tail, 3)},
        "first_line": "Opportunity should have starved within months.",
        "last_line": "It was the sky turning off.",
        "words": len(words), "last_word_end_s": last_end, "hold_s": HOLD, "fade_s": FADE,
        "reframe": (f"crop 608x1080 at x={CROP_X}, scale to {W}x{H} (1.78x); opening shot pushed {SHOT1_PUSH:.0%} "
                    f"over 1.2 s (1.99x at the end of the push)"),
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_on_screen": LONG_TITLE, "title_windows_s": [*TITLE_WINDOWS, (last_end, total)],
        "long_id_on_screen": {"id": LONG_ID, "from_s": last_end, "to_s": total},
        "audio": (f"locked long VO {SRC_IN}-{VO_CUT_ABS} s + {BED.relative_to(REPO)} x{BED_VOL} (master 0.134 less 2.5 dB), "
                  f"lifted x{HOLD_BED_GAIN} in the hold + house whoosh x{WHOOSH_VOL} at 0, -14 LUFS"),
        "stems": [f"{STEM}_{s.stem}.wav" for s in (vo_stem, sfx_stem, bed_stem)],
        "spend": "none (no VO, picture generation or bed; house SFX kit is own synthesis)",
        "orbit": "none on screen (no Omni shot in master 254-310 s)",
        "overlay": "none (Teach on screen allows at most one; not used)",
        "grain": "not added: no dark-space background in the stretch (Mars surface, rover hardware)",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR, "--id", "N42gKBbD7tE", "--length-test"], capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo_stem),
                            "--sfx", str(sfx_stem), "--bed", str(bed_stem), "--minutes", f"{total / 60:.3f}",
                            "--out", str(OUT / f"{STEM}_sfx_level.json")], capture_output=True, text=True)
    (OUT / f"{STEM}_sfx_level.txt").write_text(level.stdout + level.stderr)
    print(level.stdout, level.stderr)
    raise SystemExit(gate.returncode or level.returncode)


if __name__ == "__main__":
    main()
