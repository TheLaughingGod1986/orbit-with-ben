#!/usr/bin/env python3
"""025 Short v01 — Curiosity on Mars: Nuclear Plutonium Power Day and Night vs Thin Aluminum Wheels (J0698, backlog). No spend, no upload.

025 is the locked/uploaded OWB long (025_MarsRobot_full_rough_v03f.mp4, Js6EQJ8qDi8) with the fewest Shorts built among
live/locked longs (only 5 built video Shorts in 10_Shorts/ and only 1 standard 22-27 s backlog lift Short vs 3 on 021/022
and 4 on 023/024/026/027).
Lifts its own VO and picture from "Curiosity runs on a nuclear power source, a small supply of plutonium that gives off
heat day and night, dust or no dust..." through "...But its wheels had a different problem. They are thin aluminum made
light enough to fly to Mars." (57 words, 22.90 s VO + 3.10 s end card = 26.00 s total).
Frame 0 is real NASA Curiosity's Selfie at Mont Mercou (PIA24543 at 90.60 s of v03f), moving immediately with
a 16% first-second push, with NUCLEAR ROVER / DAY AND NIGHT hook caption.
Exact long title ("Could a Robot Survive on Mars?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar number/timeline call-out (PLUTONIUM HEAT  DAY & NIGHT vs 2018 STORM  DARKENED SKY, stroke text only,
growing bars from a shared left edge, no dark box) at 14.20-18.00 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title and YouTube ID (Js6EQJ8qDi8) on the opening PIA24543 Curiosity Selfie at Mont Mercou plate so the
last seconds loop back to frame 0. House SFX kit only.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

PICTURE = FILM / "09_Final-Export/025_MarsRobot_full_rough_v03f.mp4"
VO = FILM / "02_Voiceover/mars_robot_vo_v01.wav"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v01"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/mars_curiosity_nuclear_v01")
STEM = "mars_curiosity_nuclear_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 334.70      # "Curiosity runs on a nuclear power source..." (starts in 0.80s silence after "out." at 334.04)
VO_LEN = 22.90      # through "...They are thin aluminum made light enough to fly to Mars." (ends 357.40; next word "In" at 357.98)
END_LEN = 3.10
TOTAL = round(VO_LEN + END_LEN, 2)  # 26.00 s
FPS = 30
W, H = 1080, 1920
PUSH = 0.16
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
TITLE_ROWS = ["Could a Robot", "Survive", "on Mars?"]
END_ROWS = [("Could a Robot", WHITE), ("Survive", WHITE), ("on Mars?", WHITE), (LONG_ID, YELLOW)]
HOOK_ROWS = [("NUCLEAR ROVER", WHITE), ("DAY AND NIGHT", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 14.20, 18.00
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-11-18"  # Provisional backlog slot (after 025 week and lift_insight_quakes)

# Picture from v03f: 7 clean moving spans (2.80-3.40 s each), zero overlap with mon09_night_cold,
# wed11_opening_testA, thu12_length_test_dust, fri13_ingenuity_72, and lift_insight_quakes.
SPAN = [
    (90.60,  2.80, "crop=ih*9/16:ih:1080:0"),  # 0.00-2.80   NASA Curiosity's Selfie at Mont Mercou (PIA24543), frame 0
    (336.10, 3.40, "crop=ih*9/16:ih"),         # 2.80-6.20   NASA Mars 2020/Curiosity MMRTG Nuclear Power Source (PIA23306) on "a small supply of plutonium that gives off heat"
    (341.20, 3.30, "crop=ih*9/16:ih:1080:0"),  # 6.20-9.50   NASA Curiosity's Dusty Selfie in June 2018 Dust Storm (PIA22486) on "day and night, dust or no dust"
    (86.75,  3.30, "crop=ih*9/16:ih:960:0"),   # 9.50-12.80  NASA Curiosity Self-Portrait at Martian Sand Dune (PIA20316) under "When the 2018 storm darkened Opportunity's sky" & 9-14s title
    (94.05,  3.40, "crop=ih*9/16:ih"),         # 12.80-16.20 NASA Curiosity's Selfie at Aberlady and Kilmarie (PIA23240) under "Curiosity kept working in another part of the planet"
    (351.45, 3.40, "crop=ih*9/16:ih"),         # 16.20-19.60 NASA Martian Soil on Curiosity Wheels After Sol 22 Drive (PIA15693) under "But its wheels had a different problem" & scale bar
    (355.70, 3.30, "crop=ih*9/16:ih"),         # 19.60-22.90 NASA Curiosity's Navcams View Its Thin Aluminum Wheels (PIA26016) under "They are thin aluminum made light enough to fly to Mars"
]

WORDS_LIST = [
    {"w": "Curiosity", "s": 0.14, "e": 0.82},
    {"w": "runs", "s": 0.92, "e": 1.26},
    {"w": "on", "s": 1.30, "e": 1.38},
    {"w": "a", "s": 1.42, "e": 1.50},
    {"w": "nuclear", "s": 1.56, "e": 2.00},
    {"w": "power", "s": 2.10, "e": 2.36},
    {"w": "source,", "s": 2.48, "e": 2.86},
    {"w": "a", "s": 3.38, "e": 3.44},
    {"w": "small", "s": 3.50, "e": 3.74},
    {"w": "supply", "s": 3.82, "e": 4.18},
    {"w": "of", "s": 4.22, "e": 4.30},
    {"w": "plutonium", "s": 4.34, "e": 5.02},
    {"w": "that", "s": 5.06, "e": 5.16},
    {"w": "gives", "s": 5.22, "e": 5.40},
    {"w": "off", "s": 5.44, "e": 5.58},
    {"w": "heat", "s": 5.62, "e": 5.88},
    {"w": "day", "s": 6.04, "e": 6.30},
    {"w": "and", "s": 6.32, "e": 6.44},
    {"w": "night,", "s": 6.52, "e": 6.86},
    {"w": "dust", "s": 7.26, "e": 7.62},
    {"w": "or", "s": 7.78, "e": 7.88},
    {"w": "no", "s": 7.98, "e": 8.12},
    {"w": "dust.", "s": 8.20, "e": 8.62},
    {"w": "When", "s": 9.62, "e": 9.70},
    {"w": "the", "s": 9.74, "e": 9.80},
    {"w": "2018", "s": 10.00, "e": 10.54},
    {"w": "storm", "s": 10.68, "e": 11.04},
    {"w": "darkened", "s": 11.16, "e": 11.60},
    {"w": "Opportunity's", "s": 11.64, "e": 12.26},
    {"w": "sky,", "s": 12.36, "e": 12.72},
    {"w": "Curiosity", "s": 13.28, "e": 13.82},
    {"w": "kept", "s": 13.94, "e": 14.12},
    {"w": "working", "s": 14.16, "e": 14.58},
    {"w": "in", "s": 14.62, "e": 14.68},
    {"w": "another", "s": 14.72, "e": 15.04},
    {"w": "part", "s": 15.08, "e": 15.26},
    {"w": "of", "s": 15.28, "e": 15.34},
    {"w": "the", "s": 15.38, "e": 15.46},
    {"w": "planet.", "s": 15.50, "e": 15.96},
    {"w": "But", "s": 16.50, "e": 16.56},
    {"w": "its", "s": 16.60, "e": 16.74},
    {"w": "wheels", "s": 16.80, "e": 17.14},
    {"w": "had", "s": 17.16, "e": 17.26},
    {"w": "a", "s": 17.30, "e": 17.36},
    {"w": "different", "s": 17.40, "e": 17.70},
    {"w": "problem.", "s": 17.72, "e": 18.14},
    {"w": "They", "s": 18.74, "e": 18.86},
    {"w": "are", "s": 18.88, "e": 18.98},
    {"w": "thin", "s": 19.12, "e": 19.56},
    {"w": "aluminum", "s": 19.62, "e": 20.24},
    {"w": "made", "s": 20.68, "e": 20.90},
    {"w": "light", "s": 20.96, "e": 21.18},
    {"w": "enough", "s": 21.22, "e": 21.48},
    {"w": "to", "s": 21.52, "e": 21.62},
    {"w": "fly", "s": 21.66, "e": 21.96},
    {"w": "to", "s": 22.04, "e": 22.12},
    {"w": "Mars.", "s": 22.18, "e": 22.70},
]


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], text=True))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lufs(path: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=5):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    stroke_fill = (48, 50, 56, fill[3] if len(fill) == 4 else 255)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def hook_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cap_h = H * 0.085
    f = font_for(cap_h / 0.72, 0.86)
    while max(d.textlength(t, font=f) for t, _ in HOOK_ROWS) > W * 0.86:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    y = 260
    bboxes = []
    for t, c in HOOK_ROWS:
        b = d.textbbox((0, 0), t, font=f, stroke_width=7)
        x = (W - (b[2] - b[0])) // 2 - b[0]
        d.text((x, y), t, font=f, fill=c, stroke_width=7, stroke_fill=(48, 50, 56, 255))
        bboxes.append(list(d.textbbox((x, y), t, font=f, stroke_width=7)))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in HOOK_ROWS), "font_px": f.size, "bboxes": bboxes}


def load_words() -> list[dict]:
    (WORK / "words.json").write_text(json.dumps(WORDS_LIST, indent=2) + "\n")
    return WORDS_LIST


def caption_chunks(words: list[dict]) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append((w["w"], float(w["s"]), float(w["e"])))
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0][1]
        nxt = chunks[i + 1][0][1] if i + 1 < len(chunks) else VO_LEN
        end = min(nxt, c[-1][2] + 0.45, VO_LEN)
        text = " ".join(x[0] for x in c).rstrip(",.")
        out.append({"text": text, "s": round(start, 2), "e": round(end, 2)})
    return out


def caption_png(dest: Path, text: str) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.95)
    while d.textlength(text.upper(), font=f) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    centred(d, BAND_Y0 + BAND_H + 70, text.upper(), f, WHITE, stroke=6)
    im.save(dest)


# One scale, two rows (Curiosity MMRTG plutonium power day & night vs 2018 global dust storm darkened sky, NASA/JPL-Caltech). Each label <= 4 words. No dark plate.
SCALE = [
    ("PLUTONIUM HEAT", "DAY & NIGHT", 100, YELLOW),
    ("2018 STORM", "DARKENED SKY", 35, WHITE),
]


def card_frames(dest_dir: Path) -> dict:
    dest_dir.mkdir(parents=True, exist_ok=True)
    f = font_for(LINE_H)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    labels = [f"{name}  {num}" for name, num, _, _ in SCALE]
    while max(probe.textlength(t, font=f) for t in labels) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    text_h = probe.textbbox((0, 0), "Hg", font=f)[3]
    row_h = text_h + 48
    block = row_h * len(SCALE)
    y0 = BAND_Y0 + (BAND_H - block) // 2
    n = round((CARD_OUT - CARD_IN) * FPS)
    sample_bb = None
    for i in range(n):
        t = CARD_IN + i / FPS
        a = min(1.0, (t - CARD_IN) / 0.35, (CARD_OUT - t) / 0.35)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = int(255 * a)
        for r, (name, num, value, colour) in enumerate(SCALE):
            delay = r * 0.25
            prog = min(1.0, max(0.0, (t - CARD_IN - delay) / 0.60))
            y = y0 + r * row_h
            label = f"{name}  {num}"
            fill = (colour[0], colour[1], colour[2], alpha)
            bb = centred(d, y, label, f, fill, stroke=6)
            if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
                raise SystemExit(f"scale text outside 16:9 band: {label} {bb}")
            full = int(W * 0.62)
            left = (W - full) // 2
            bar_w = int(full * (value / 100.0) * prog)
            if bar_w > 4:
                by = bb[3] + 8
                bar_col = (colour[0], colour[1], colour[2], alpha)
                d.rectangle((left, by, left + bar_w, by + 16), fill=bar_col)
                if by + 16 > BAND_Y0 + BAND_H:
                    raise SystemExit(f"scale bar outside 16:9 band: {by}")
            if i == n // 2 and r == 0:
                sample_bb = bb
        im.save(dest_dir / f"card_{i:04d}.png")
    return {
        "in": CARD_IN, "out": CARD_OUT,
        "labels": labels,
        "values": ["Curiosity MMRTG plutonium-238 nuclear power source gives off heat and electricity day and night, dust or no dust (NASA/JPL-Caltech)", "June 2018 global dust storm darkened Opportunity's sky while Curiosity kept working (NASA/JPL-Caltech)"],
        "band": [BAND_Y0, BAND_Y0 + BAND_H],
        "line_px": f.size,
        "sample_bbox": sample_bb,
        "style": "stroke text and growing bars from shared left edge, no dark box",
    }


def title_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    while max(d.textlength(r, font=f) for r in TITLE_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - gap * len(TITLE_ROWS)) // 2
    placed = []
    for r in TITLE_ROWS:
        bb = centred(d, y, r, f, WHITE)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"text outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed}


def end_title_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    while max(d.textlength(r, font=f) for r, _ in END_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 14
    y = BAND_Y0 + (BAND_H - gap * len(END_ROWS)) // 2
    placed = []
    for r, col in END_ROWS:
        bb = centred(d, y, r, f, col)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"end text outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed}


def _cut(src_t: float, length: float, vf_crop: str, dest: Path) -> None:
    pre = max(0.0, src_t - 2.0)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{pre:.3f}", "-i", str(PICTURE),
         "-ss", f"{src_t - pre:.3f}", "-t", f"{length:.3f}", "-an",
         "-vf", f"fps={FPS},{vf_crop},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-video_track_timescale", "30000", str(dest)])


def accurate_span(dest: Path) -> None:
    if abs(sum(length for _, length, _ in SPAN) - VO_LEN) > 0.05:
        raise SystemExit(f"span {sum(l for _, l, _ in SPAN)} != VO_LEN {VO_LEN}")
    lines = []
    for i, (src_t, length, vf_crop) in enumerate(SPAN):
        piece = WORK / f"span_{i}.mp4"
        _cut(src_t, length, vf_crop, piece)
        lines.append(f"file '{piece.name}'")
    lst = WORK / "span_list.txt"
    lst.write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(dest)])


def end_plate(dest: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "picture_span.mp4"), "-frames:v", "1",
         str(WORK / "plate0.png")])
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.92)
    im = ImageEnhance.Sharpness(im).enhance(1.45)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse((80, BAND_Y0 - 20, W - 80, BAND_Y0 + BAND_H + 20), fill=40)
    shade = shade.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.80)
    d = ImageDraw.Draw(im)
    rows = [("NUCLEAR ROVER", WHITE), ("DAY AND NIGHT", YELLOW)]
    size = 60
    while True:
        f = ImageFont.truetype(FONT, size + 2)
        if max(d.textlength(r, font=f) for r, _ in rows) > W * 0.78:
            break
        size += 2
    f = ImageFont.truetype(FONT, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 20
    y = (H - lh * len(rows)) // 2
    for r, c in rows:
        centred(d, y, r, f, c, stroke=9)
        y += lh
    im.save(dest, quality=92)


def contact_sheet(video: Path, dest: Path) -> None:
    times = [0.0, 0.5, 1.6, 4.5, 8.0, 11.0, 14.5, 17.5, 21.0, TOTAL - 0.5]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
             "-vf", "scale=216:384", str(p)])
        tiles.append((p, t))
    cols, rows_n = 5, 2
    canvas = Image.new("RGB", (216 * cols, 410 * rows_n), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(tiles):
        cx = (i % cols) * 216
        cy = (i // cols) * 410
        canvas.paste(Image.open(p), (cx, cy))
        d.text((cx + 8, cy + 388), f"{t:.1f}s", fill=(255, 255, 255))
    canvas.save(dest, quality=90)


def audio() -> dict:
    vo = WORK / "stem_vo.wav"
    bed = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{VO_T0:.3f}", "-t", f"{VO_LEN:.3f}", "-i", VO,
         "-af", f"afade=t=out:st={VO_LEN - 0.08:.3f}:d=0.08,apad=whole_dur={TOTAL:.3f}",
         "-ar", "48000", "-ac", "2", str(vo)])
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{VO_T0:.3f}", "-t", f"{TOTAL:.3f}", "-i", BED,
         "-af", f"afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.5:.3f}:d=0.5",
         "-ar", "48000", "-ac", "2", str(bed)])
    vo_i, bed_i = lufs(vo), lufs(bed)
    bed_gain = (vo_i - 22.0) - bed_i
    bed_l = WORK / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", bed, "-af", f"volume={bed_gain:.2f}dB", str(bed_l)])
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    hits = [(whoosh, 0.0), (tick, TITLE_IN), (tick, CARD_IN)]
    sfx_raw = WORK / "stem_sfx_raw.wav"
    inputs, parts = [], []
    for i, (f, at) in enumerate(hits):
        inputs += ["-i", str(f)]
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(hits)))
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(parts) + f";{mix}amix=inputs={len(hits)}:normalize=0,apad=whole_dur={TOTAL:.3f}[o]",
         "-map", "[o]", "-t", f"{TOTAL:.3f}", str(sfx_raw)])
    sfx_gain = (vo_i - 23.0) - lufs(sfx_raw)
    sfx = WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", sfx_raw, "-af", f"volume={sfx_gain:.2f}dB", str(sfx)])
    mixed = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-i", bed_l, "-i", sfx, "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", "48000", "-t", f"{TOTAL:.3f}", str(mixed)])
    return {
        "vo_lufs": vo_i, "bed_gain_db": round(bed_gain, 2), "sfx_gain_db": round(sfx_gain, 2),
        "sfx_hits": [[Path(f).name, round(a, 2)] for f, a in hits], "mix_lufs": lufs(mixed),
    }


def main() -> None:
    if not PICTURE.exists():
        raise SystemExit(f"missing picture master: {PICTURE}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words = load_words()
    if not 55 <= len(words) <= 65:
        raise SystemExit(f"word count {len(words)} outside 55-65")
    hook = hook_png(WORK / "hook.png")
    caps = caption_chunks(words)
    for i, c in enumerate(caps):
        caption_png(WORK / f"cap_{i:02d}.png", c["text"])
    card = card_frames(WORK / "card")
    title = title_png(WORK / "title.png")
    endt = end_title_png(WORK / "end_text.png")
    accurate_span(WORK / "picture_span.mp4")
    end_plate(WORK / "end_bg.png")
    cover_path = OUT / f"{STEM}_cover.jpg"
    cover(cover_path)
    aud = audio()

    inputs = ["-t", f"{VO_LEN:.3f}", "-i", str(WORK / "picture_span.mp4"),
              "-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}", "-i", str(WORK / "end_bg.png"),
              "-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}", "-i", str(WORK / "hook.png"),
              "-framerate", str(FPS), "-i", str(WORK / "card" / "card_%04d.png"),
              "-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}", "-i", str(WORK / "title.png"),
              "-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}", "-i", str(WORK / "end_text.png"),
              "-i", str(WORK / "mix.wav")]
    base = 7
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}", "-i", str(WORK / f"cap_{i:02d}.png")]
    end_frames = round(END_LEN * FPS) + 2
    fc = [
        f"[0:v]fps={FPS},"
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a]",
        f"[1:v]scale={W * 2}:{H * 2},zoompan=z='1.03-0.03*on/{end_frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS},trim=0:{END_LEN:.3f},setpts=PTS-STARTPTS,format=yuv420p[e]",
        "[e][5:v]overlay=0:0:shortest=1,format=yuv420p[ecard]",
        "[a][ecard]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={HOOK_END - 0.3:.2f}:d=0.3:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[3:v]setpts=PTS-STARTPTS+{CARD_IN}/TB[cd]",
        "[v1][cd]overlay=0:0:eof_action=pass[v2]",
        f"[4:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.3:alpha=1,fade=t=out:st={TITLE_OUT - 0.3}:d=0.3:alpha=1[tt]",
        f"[v2][tt]overlay=0:0:enable='between(t,{TITLE_IN},{TITLE_OUT})'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='between(t,{c['s']},{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "6:a", *enc, "-t", f"{TOTAL:.3f}", FINAL])

    contact_path = OUT / f"{STEM}_contact.jpg"
    contact_sheet(FINAL, contact_path)
    thumb_sheet = OUT / f"{STEM}_cover_preview.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
         "short", str(cover_path), "--out", str(thumb_sheet)])

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--json"],
        capture_output=True, text=True,
    )
    (OUT / f"{STEM}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE],
        capture_output=True, text=True,
    )
    (OUT / f"{STEM}_gate.txt").write_text(gate_txt.stdout or gate_txt.stderr)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(WORK / "stem_vo.wav"),
         "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"),
         "--minutes", f"{TOTAL / 60.0:.3f}"],
        capture_output=True, text=True,
    )
    (OUT / f"{STEM}_sfx.txt").write_text((sfx_chk.stdout or "") + (sfx_chk.stderr or ""))

    cuts = [
        {"row": "s01_pia24543_mont_mercou", "timeline_in": 0.0, "timeline_out": 2.80, "source": "025_v03f_span_90.60.mp4", "upscale": 1.0, "framing": {"offset": 90.60}, "video": True},
        {"row": "s02_pia23306_mmrtg_nuclear", "timeline_in": 2.80, "timeline_out": 6.20, "source": "025_v03f_span_336.10.mp4", "upscale": 1.0, "framing": {"offset": 336.10}, "video": True},
        {"row": "s03_pia22486_dusty_selfie", "timeline_in": 6.20, "timeline_out": 9.50, "source": "025_v03f_span_341.20.mp4", "upscale": 1.0, "framing": {"offset": 341.20}, "video": True},
        {"row": "s04_pia20316_curiosity_dune", "timeline_in": 9.50, "timeline_out": 12.80, "source": "025_v03f_span_86.75.mp4", "upscale": 1.0, "framing": {"offset": 86.75}, "video": True},
        {"row": "s05_pia23240_aberlady_selfie", "timeline_in": 12.80, "timeline_out": 16.20, "source": "025_v03f_span_94.05.mp4", "upscale": 1.0, "framing": {"offset": 94.05}, "video": True},
        {"row": "s06_pia15693_curiosity_wheel_soil", "timeline_in": 16.20, "timeline_out": 19.60, "source": "025_v03f_span_351.45.mp4", "upscale": 1.0, "framing": {"offset": 351.45}, "video": True},
        {"row": "s07_pia26016_curiosity_navcam_wheels", "timeline_in": 19.60, "timeline_out": 22.90, "source": "025_v03f_span_355.70.mp4", "upscale": 1.0, "framing": {"offset": 355.70}, "video": True},
        {"row": "s08_end_loop", "timeline_in": 22.90, "timeline_out": 26.00, "source": "end_card_loop_pia24543.mp4", "upscale": 1.0, "framing": {"offset": 90.60}, "video": True},
    ]
    pool = [
        {"file_id": "025_v03f_span_90.60.mp4", "title": "NASA/JPL-Caltech Curiosity's Selfie at Mont Mercou (PIA24543, 90.60s)"},
        {"file_id": "025_v03f_span_336.10.mp4", "title": "NASA/JPL-Caltech Mars 2020 and Curiosity MMRTG Nuclear Power Source (PIA23306, 336.10s)"},
        {"file_id": "025_v03f_span_341.20.mp4", "title": "NASA/JPL-Caltech Curiosity's Dusty Selfie in the June 2018 Dust Storm (PIA22486, 341.20s)"},
        {"file_id": "025_v03f_span_86.75.mp4", "title": "NASA/JPL-Caltech Curiosity Self-Portrait at Martian Sand Dune (PIA20316, 86.75s)"},
        {"file_id": "025_v03f_span_94.05.mp4", "title": "NASA/JPL-Caltech Curiosity's Selfie at Aberlady and Kilmarie (PIA23240, 94.05s)"},
        {"file_id": "025_v03f_span_351.45.mp4", "title": "NASA/JPL-Caltech Martian Soil on Curiosity Wheels After Sol 22 Drive (PIA15693, 351.45s)"},
        {"file_id": "025_v03f_span_355.70.mp4", "title": "NASA/JPL-Caltech Curiosity's Navcams View Its Thin Aluminum Wheels (PIA26016, 355.70s)"},
        {"file_id": "end_card_loop_pia24543.mp4", "title": "End-card loop: NASA/JPL-Caltech Curiosity's Selfie at Mont Mercou (PIA24543, 90.60s)"},
    ]
    (OUT / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / "pool_v01.json").write_text(json.dumps(pool, indent=2) + "\n")

    pg_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v01.json"),
         "--out", str(OUT / "polish_gate_v01.json"), "--no-jitter"],
        capture_output=True, text=True,
    )
    (OUT / "polish_gate_v01.txt").write_text((pg_chk.stdout or "") + (pg_chk.stderr or ""))

    pqa_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v01.json"),
         "--pool", str(OUT / "pool_v01.json"),
         "--out-dir", str(OUT / "picture_qa_v01")],
        capture_output=True, text=True,
    )
    (OUT / "picture_qa_v01.txt").write_text((pqa_chk.stdout or "") + (pqa_chk.stderr or ""))

    UAT.mkdir(parents=True, exist_ok=True)
    for p in (FINAL, contact_path, cover_path, thumb_sheet,
              OUT / f"{STEM}_gate.json", OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt",
              OUT / "cuts_v01.json", OUT / "pool_v01.json",
              OUT / "polish_gate_v01.json", OUT / "polish_gate_v01.txt", OUT / "picture_qa_v01.txt"):
        if p.exists():
            shutil.copy2(p, UAT / p.name)
    if (OUT / "picture_qa_v01").exists():
        shutil.copytree(OUT / "picture_qa_v01", UAT / "picture_qa_v01", dirs_exist_ok=True)

    meta = {
        "file": str(FINAL), "version": "v01", "job": "J0698",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v03f",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": [[s, l] for s, l, _ in SPAN],
            "why_picture": "Frame 0 is real NASA/JPL-Caltech Curiosity's Selfie at Mont Mercou (PIA24543 at 90.60 s of v03f), moving immediately with a 16% push. Cuts land across Mars 2020 and Curiosity MMRTG Nuclear Power Source (PIA23306 at 336.10 s) on 'a small supply of plutonium that gives off heat', Curiosity's Dusty Selfie in the June 2018 Dust Storm (PIA22486 at 341.20 s) on 'day and night, dust or no dust', Curiosity Self-Portrait at Martian Sand Dune (PIA20316 at 86.75 s) under 'When the 2018 storm darkened Opportunity's sky' and the 9-14 s title, Curiosity's Selfie at Aberlady and Kilmarie (PIA23240 at 94.05 s) under 'Curiosity kept working in another part of the planet', Martian Soil on Curiosity Wheels After Sol 22 Drive (PIA15693 at 351.45 s) under 'But its wheels had a different problem' and the PLUTONIUM HEAT DAY & NIGHT vs 2018 STORM DARKENED SKY scale bar, and Curiosity's Navcams View Its Thin Aluminum Wheels (PIA26016 at 355.70 s) under 'They are thin aluminum made light enough to fly to Mars'; zero overlap with mon09_night_cold, wed11_opening_testA, thu12_length_test_dust, fri13_ingenuity_72, and lift_insight_quakes; skips chapter cards, burned captions, and Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening NASA/JPL-Caltech Curiosity's Selfie at Mont Mercou (PIA24543 at 90.60 s)", "youtube_id": LONG_ID, **endt},
        "audio": aud, "sfx_level_check": (sfx_chk.stdout or sfx_chk.stderr).strip(),
        "sfx_level_ok": sfx_chk.returncode == 0,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "polish_gate_ok": pg_chk.returncode == 0,
        "picture_qa_ok": pqa_chk.returncode == 0,
        "cover": str(cover_path), "cover_preview": str(thumb_sheet), "contact_sheet": str(contact_path),
        "uat_dir": str(UAT), "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(OUT / f"{STEM}_meta.json", UAT / f"{STEM}_meta.json")
    shutil.rmtree(WORK, ignore_errors=True)
    print(gate_txt.stdout or gate_txt.stderr)
    print("--- sfx", sfx_chk.returncode)
    print(sfx_chk.stdout or sfx_chk.stderr)
    print("--- polish_gate", pg_chk.returncode)
    print(pg_chk.stdout or pg_chk.stderr)
    print("--- picture_qa", pqa_chk.returncode)
    print(pqa_chk.stdout or pqa_chk.stderr)
    print(json.dumps({k: meta[k] for k in ("file", "duration_s", "words", "gate_ok", "sfx_level_ok", "polish_gate_ok", "picture_qa_ok", "audio")}, indent=2))
    if gate.returncode != 0 or sfx_chk.returncode != 0 or pg_chk.returncode != 0 or pqa_chk.returncode != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
