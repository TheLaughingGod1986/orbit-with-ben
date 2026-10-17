#!/usr/bin/env python3
"""020 Jupiter Short v01, lifted from the live long -jmMROGoZCM (J0150, backlog owb-short-from-locked).

Does not upload or schedule. VO and picture are the uploaded master jupiter_film_v04.mp4 (sha256 a658a785, copied
from the NAS to WORK), VO 125.20-144.62 s (picture from 128.60 s, the bright cloud deck): "There is no crust under the paint. ... you step onto atmosphere."
Reframe: centre crop 608x1080 -> 1080x1920 (1.78x). After the last word the picture holds 3 s, crossfading back to
the opening plate (master 128.60 s) so the Short loops to its own frame 0.
Audio: the master mix (VO + 020's own bed) to just before the next sentence, then 020's own bed from the master's
music-only tail (579.6 s) for the hold, a house-kit whoosh at frame 0 and a house-kit tick on the one overlay.
Teach on screen: one scale card, "1 BAR / EARTH SEA LEVEL", inside the 16:9 centre band, under "about one bar".
The air date is provisional (Chief picks the slot); the gate's opening-plate check is run against it.
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

WORK = Path("/private/tmp/jupiter020_short_lift")
MASTER = WORK / "jupiter_film_v04.mp4"
MASTER_SHA = "a658a785"
WORDS = WORK / "jupiter_v04_words.json"
KIT = WORK / "kit_v01"
OUT = HERE / "06_Final-Exports"
STEM = "jupiter_no_crust_v01"

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-16"
LONG_TITLE = "Why You Can't Stand On Jupiter"
LONG_ID = "-jmMROGoZCM"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SRC_IN = 125.20
PIC_IN = 128.60     # bright cloud deck: master 125.2 s opens on a near-dark swirl (frame-0 luma 23)
FIRST_WORD, LAST_WORD = "There", "atmosphere."
VO_OUT = 145.60     # "atmosphere." ends 144.62, "Why" starts 145.94
HOLD = 3.0
XFADE = 0.5
BED_TAIL = 579.6    # master tail after the last VO word: 020's bed alone
BED_TAIL_GAIN = 2.2
CROP_X = (1920 - 608) // 2
PUSH = 0.10         # first-second push on the opening plate
HOOK = ("JUPITER HAS", "NO GROUND")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)
END_TITLE_FROM = 18.0
BAND_TOP = (H - 608) // 2
CARD = (6.9, 8.9)   # "about one bar" is spoken 7.26-8.26 s into the Short


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
    y = int(H * 0.06)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 24
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path, with_id: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Why You Can't", "Stand On Jupiter"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    if with_id:
        centred(d, y + 14, LONG_ID, ImageFont.truetype(FONT, 72), YELLOW, 5)
    im.save(dest)


def card_png(dest: Path) -> None:
    """One-number scale card: a pressure bar filled to the 1 bar mark, lines at 11-12% of the 16:9 band."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    line_h = int(608 * 0.115)
    y = BAND_TOP + 40
    big = fit_font(d, "1 BAR", line_h + 30, int(W * 0.6), 6)
    y += centred(d, y, "1 BAR", big, YELLOW, 6) + 22
    small = fit_font(d, "EARTH SEA LEVEL", line_h, int(W * 0.84), 5)
    y += centred(d, y, "EARTH SEA LEVEL", small, WHITE, 5) + 30
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
        raise SystemExit("master sha256 does not match the uploaded v04")
    work = WORK / STEM
    work.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    allw = json.loads(WORDS.read_text())["words"]
    allw = [{"word": w["word"].strip(), "start": w["start"], "end": w["end"]} for w in allw]
    i0 = next(i for i, w in enumerate(allw) if w["word"] == FIRST_WORD and w["start"] >= SRC_IN)
    i1 = next(i for i, w in enumerate(allw) if w["word"] == LAST_WORD and i > i0)
    words = [{"word": w["word"], "start": round(w["start"] - SRC_IN, 3), "end": round(w["end"] - SRC_IN, 3)}
             for w in allw[i0:i1 + 1]]
    last_end = words[-1]["end"]
    total = round(last_end + HOLD, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"total {total} outside 22-27 s")
    vo_cut = VO_OUT - SRC_IN
    seg_a = last_end + XFADE

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
        "-ss", f"{PIC_IN:.3f}", "-t", f"{HOLD:.3f}", "-i", MASTER,
        "-ss", f"{SRC_IN:.3f}", "-t", f"{seg_a:.3f}", "-i", MASTER,
        "-loop", "1", "-i", hook, "-loop", "1", "-i", title,
        "-f", "concat", "-safe", "0", "-i", caps,
        "-loop", "1", "-i", end_title, "-loop", "1", "-i", card, "-loop", "1", "-i", work / "card_bar.png",
        "-ss", f"{BED_TAIL:.3f}", "-t", f"{HOLD + 1:.3f}", "-i", MASTER,
        "-i", whoosh, "-i", tick,
        "-filter_complex", (
            f"[0:v]fps={FPS},crop=608:1080:{CROP_X}:0,"
            f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a];"
            f"[1:v]fps={FPS},crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[b];"
            f"[a][b]xfade=transition=fade:duration={XFADE}:offset={last_end:.3f},split[b0][bhz];"
            f"[bhz]crop=1080:300:0:410,boxblur=4:40:4:2,format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/35,(300-Y)/35))'[hz];"
            f"[b0][hz]overlay=0:410:enable='between(t,7.4,15.4)',format=yuv420p[base];"
            f"[3:v]format=rgba[hk];[base][hk]overlay=0:0:enable='between(t,0,{HOOK_END})':shortest=1[v1];"
            f"[4:v]format=rgba[tt];[v1][tt]overlay=0:0:enable='{title_on}':shortest=1[v2a];"
            f"[6:v]format=rgba[et];[v2a][et]overlay=0:0:enable='gte(t,{END_TITLE_FROM})':shortest=1[v2b];"
            f"[7:v]fps={FPS},format=rgba,{card_fade}[cd];"
            f"[v2b][cd]overlay=0:0:enable='between(t,{c0},{c1})':shortest=1[v2c];"
            f"[8:v]fps={FPS},format=rgba,scale=w='{bar_w}':h=14:eval=frame,{card_fade}[br];"
            f"[v2c][br]overlay={bar_box['x']}:{bar_box['y']}:enable='between(t,{c0 + 0.2},{c1})':shortest=1[v2];"
            f"[5:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,format=yuv420p[v];"
            f"[2:a]aresample=48000,atrim=0:{vo_cut:.3f},afade=t=out:st={vo_cut - 0.3:.3f}:d=0.3,apad[va];"
            f"[9:a]aresample=48000,volume={BED_TAIL_GAIN},afade=t=in:st=0:d=0.4,"
            f"adelay={int((vo_cut - 0.4) * 1000)}:all=1,atrim=0:{total},"
            f"afade=t=out:st={total - 0.6:.3f}:d=0.6[mu];"
            f"[10:a]aresample=48000,volume=0.5[wh];"
            f"[11:a]aresample=48000,volume=0.6,adelay={int((c0 + 0.05) * 1000)}:all=1[tk];"
            f"[va][mu][wh][tk]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,"
            f"atrim=0:{total},loudnorm=I=-13:TP=-1.5:LRA=11[aout]"
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
        "job": "J0150", "air_provisional": AIR, "related": LONG_ID, "title_on_screen": LONG_TITLE,
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final), "duration_s": dur(final),
        "master": {"file": "020/09_Final-Export/jupiter_film_v04.mp4 (NAS)", "sha256_prefix": MASTER_SHA,
                   "from_s": SRC_IN, "to_s": round(SRC_IN + last_end, 3),
                   "picture_from_s": PIC_IN, "picture_note": "picture runs 3.4 s ahead of the VO (cloud deck throughout)"},
        "spoken": " ".join(w["word"] for w in words), "words": len(words),
        "last_word": {"word": LAST_WORD, "end_s": last_end}, "hold_s": HOLD,
        "loop": f"{XFADE} s crossfade from {last_end} s back to the opening plate (master {PIC_IN} s)",
        "reframe": f"crop 608x1080 at x={CROP_X}, scale {W}x{H} (1.78x), {PUSH:.0%} push over 1.2 s at the open",
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_windows_s": [*TITLE_WINDOWS, (END_TITLE_FROM, total)],
        "overlay": {"kind": "one-number scale card", "text": ["1 BAR", "EARTH SEA LEVEL"], "window_s": CARD,
                    "spoken": "about one bar, the weight of earth's air at sea level"},
        "audio": (f"master mix 0-{vo_cut:.2f} s, 020 bed from master tail {BED_TAIL} s x{BED_TAIL_GAIN} for the hold, "
                  "house kit whoosh at 0 + tick on the card, -14 LUFS"),
        "orbit": "none on screen", "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR, "--id", "23KZK7OjsEE"], capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout, gate.stderr)
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
