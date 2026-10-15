#!/usr/bin/env python3
"""J0232: existing locked Venus v05e opening, 0-23.6 s. No generation or upload.
Render and gate a review-only Short with a loop, captions, depth scale and house SFX.
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

WORK = Path("/private/tmp/j0232-assets")
MASTER = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/023_Venus_full_rough_v05e.mp4")
VO_SOURCE = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.mp3")
BED_SOURCE = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3")
MASTER_SHA = "5d8a8f73454f889a38590661885a21702690a42c8ebfd940868d033f0174e6fc"
WORDS = FILM / "07_Edit-Project/full_rough_v05e_pack/venus_words_list.json"
KIT = WORK / "kit_v01"
OUT = Path("/Users/benjaminoats/_desk/J0232-venus-short")
STEM = "venus_two_hours_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-17"
LONG_TITLE = "What Happened to Venus?"
LONG_ID = "VBaYRPp85Sw"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SRC_IN = 0.0
PIC_IN = 0.0
FIRST_WORD, LAST_WORD = "Venus", "hours."
VO_OUT = 24.05
HOLD = 3.0
XFADE = 0.5
BED_TAIL = 509.0
BED_TAIL_GAIN = 1.0
CROP_X = (1920 - 608) // 2
PUSH = 0.10
HOOK = ("VENUS MELTS", "LEAD")
HOOK_END = 2.5
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 22.0
BAND_TOP = (H - 608) // 2
CARD = (16.9, 19.1)



def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True, check=True).stdout.strip())


def fit_font(draw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
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
    y = int(H * 0.37)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 24
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path, with_id: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["What Happened", "to Venus?"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    if with_id:
        centred(d, y + 14, LONG_ID, ImageFont.truetype(FONT, 72), YELLOW, 5)
    im.save(dest)


def card_png(dest: Path) -> None:
    """One-number scale card: a depth bar filled to the depth mark, lines at 11-12% of the 16:9 band."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    line_h = int(608 * 0.115)
    y = BAND_TOP + 40
    big = fit_font(d, "NEARLY 1 KM", line_h + 30, int(W * 0.6), 6)
    y += centred(d, y, "NEARLY 1 KM", big, YELLOW, 6) + 22
    small = fit_font(d, "DEEP", line_h, int(W * 0.84), 5)
    y += centred(d, y, "DEEP", small, WHITE, 5) + 30
    x0, x1 = int(W * 0.18), int(W * 0.82)
    d.rounded_rectangle((x0, y, x1, y + 26), radius=13, fill=(0, 0, 0, 150), outline=WHITE, width=4)
    im.save(dest)
    Image.new("RGBA", (x1 - x0 - 12, 14), YELLOW + (255,)).save(dest.with_name("card_bar.png"))
    dest.with_name("card_bar_box.json").write_text(json.dumps({"x": x0 + 6, "y": y + 6, "w": x1 - x0 - 12}))


def caption_track(words: list[dict], end: float, work: Path) -> Path:
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cap_dir = work / "captions"
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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    whoosh, tick = KIT / "sfx_owb_whoosh_soft_v01.wav", KIT / "sfx_owb_tick_ui_v01.wav"
    for p in (MASTER, WORDS, whoosh, tick):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if not sha256(MASTER).startswith(MASTER_SHA):
        raise SystemExit("master sha256 does not match locked v05e")
    work = WORK / STEM
    work.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    allw = json.loads(WORDS.read_text())
    allw = [{"word": w["text"].strip(), "start": w["start"], "end": w["end"]} for w in allw]
    i0 = next(i for i, w in enumerate(allw) if w["word"] == FIRST_WORD and w["start"] >= SRC_IN)
    i1 = next(i for i, w in enumerate(allw) if w["word"] == LAST_WORD and i > i0)
    words = [{"word": w["word"], "start": round(w["start"] - SRC_IN, 3), "end": round(w["end"] - SRC_IN, 3)}
             for w in allw[i0:i1 + 1]]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")
    vo_cut = VO_OUT - SRC_IN
    loop_start = total - 4.0
    seg_a = loop_start + XFADE

    hook, title, end_title, card = (work / n for n in ("hook.png", "title.png", "end_title.png", "card.png"))
    hook_png(hook)
    title_png(title)
    title_png(end_title, with_id=True)
    card_png(card)
    bar_box = json.loads((work / "card_bar_box.json").read_text())
    caps = caption_track(words, total, work)

    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    c0, c1 = CARD
    card_fade = (f"fade=t=in:st={c0}:d=0.35:alpha=1,fade=t=out:st={c1 - 0.35:.2f}:d=0.35:alpha=1")
    bar_w = f"max(2,trunc({bar_box['w']}*min(max((t-{c0 + 0.2})/0.9,0),1)))"
    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{PIC_IN:.3f}", "-t", f"{seg_a:.3f}", "-i", MASTER,
        "-ss", f"{PIC_IN:.3f}", "-t", f"4.0", "-i", MASTER,
        "-ss", f"{SRC_IN:.3f}", "-t", f"{VO_OUT:.3f}", "-i", VO_SOURCE,
        "-loop", "1", "-i", hook, "-loop", "1", "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps,
        "-loop", "1", "-i", end_title, "-loop", "1", "-i", card, "-loop", "1", "-i", work / "card_bar.png",
        "-ss", "0", "-t", f"{total:.3f}", "-i", BED_SOURCE,
        "-i", whoosh, "-i", tick,
        "-filter_complex", (
            f"[0:v]fps={FPS},crop=608:1080:{CROP_X}:0,"
            f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a];"
            f"[1:v]fps={FPS},crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[b];"
            f"[a][b]xfade=transition=fade:duration={XFADE}:offset={loop_start:.3f}[base];"
            f"[3:v]format=rgba[hk];[base][hk]overlay=0:0:enable='between(t,0,{HOOK_END})':shortest=1[v1];"
            f"[4:v]format=rgba[tt];[v1][tt]overlay=0:0:enable='{title_on}':shortest=1[v2a];"
            f"[6:v]format=rgba[et];[v2a][et]overlay=0:0:enable='gte(t,{END_TITLE_FROM})':shortest=1[v2b];"
            f"[7:v]fps={FPS},format=rgba,{card_fade}[cd];"
            f"[v2b][cd]overlay=0:0:enable='between(t,{c0},{c1})':shortest=1[v2c];"
            f"[8:v]fps={FPS},format=rgba,scale=w='{bar_w}':h=14:eval=frame,{card_fade}[br];"
            f"[v2c][br]overlay={bar_box['x']}:{bar_box['y']}:enable='between(t,{c0 + 0.2},{c1})':shortest=1[v2];"
            f"[5:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,noise=alls=4:allf=t,format=yuv420p[v];"
            f"[2:a]aresample=48000,atrim=0:{vo_cut:.3f},afade=t=out:st={vo_cut - 0.3:.3f}:d=0.3,apad[va];"
            f"[9:a]aresample=48000,volume=0.06,atrim=0:{total}[mu];"
            f"[10:a]aresample=48000,volume=0.06[wh];"
            f"[11:a]aresample=48000,volume=0.06,adelay={int((c0 + 0.05) * 1000)}:all=1[tk];"
            f"[va][mu][wh][tk]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,"
            f"atrim=0:{total},loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ),
        "-map", "[v]", "-map", "[aout]", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 3.0, 5.5, 7.8, 11.0, 15.0, 18.5, 20.5, total - 0.3]
    tiles = []
    for i, t in enumerate(times):
        p = work / f"sheet_{i}.jpg"
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
        "job": "J0232", "air_provisional": AIR, "related": LONG_ID, "title_on_screen": LONG_TITLE,
        "file": str(final), "frames": str(sheet),
        "sha256": sha256(final), "duration_s": dur(final),
        "master": {"file": "iCloud OWB UAT/023_Venus_full_rough_v05e.mp4", "sha256_prefix": MASTER_SHA,
                   "from_s": SRC_IN, "to_s": round(SRC_IN + last_end, 3),
                   "picture_from_s": PIC_IN, "picture_note": "picture and VO use the same locked master times"},
        "spoken": " ".join(w["word"] for w in words), "words": len(words),
        "last_word": {"word": LAST_WORD, "end_s": last_end}, "hold_s": HOLD,
        "loop": f"{XFADE} s crossfade from {loop_start} s back to the opening plate (master {PIC_IN} s)",
        "reframe": f"crop 608x1080 at x={CROP_X}, scale {W}x{H} (1.78x), {PUSH:.0%} push over 1.2 s at the open",
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "overlay": {"kind": "one-number scale card", "text": ["NEARLY 1 KM", "DEEP"], "window_s": CARD,
                    "spoken": "nearly a kilometer deep"},
        "audio": (f"locked original VO 0-{vo_cut:.2f} s; 023 own score 0-{total} s at 0.06 gain; "
                  "house kit whoosh at 0 + tick on the card, -14 LUFS"),
        "orbit": "none on screen", "spend": "none",
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
