#!/usr/bin/env python3
"""025 Short v01 — Mars Radiation Dose: 1 Day on Mars vs 3 Months on Earth (J0729, backlog). No spend, no upload.

025 is the locked/uploaded OWB long (025_MarsRobot_full_rough_v03f.mp4, Js6EQJ8qDi8) with the fewest backlog lift Shorts
built among locked/live longs with a local SSD master (2 in 10_Shorts/: lift_insight_quakes, lift_curiosity_nuclear vs 3
on 021/022 and 4 on 023/024/026/027).
Lifts its own VO and picture from "In one day on Mars, the dose is roughly what you would get in three months on Earth..."
through "...So the thin air and the radiation are not what usually ends a robot's life on Mars." (58 words, 21.50 s VO +
3.10 s end card = 24.60 s total).
Frame 0 is real NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207 at 78.60 s of v03f), moving immediately with
a 16% first-second push, with MARS RADIATION / 3 MONTHS DOSE hook caption.
Exact long title ("Could a Robot Survive on Mars?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar number/scale call-out (1 MARS DAY  90X DOSE vs 3 EARTH MONTHS  SAME DOSE, stroke text only,
growing bars from a shared left edge, no dark box) at 3.80-7.50 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title and YouTube ID (Js6EQJ8qDi8) on the opening PIA22207 Mount Sharp 'Photobombs' Curiosity plate
so the last seconds loop back to frame 0. House SFX kit only.
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
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/mars_radiation_3months_v01")
STEM = "mars_radiation_3months_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 75.90       # "In one day on Mars, the dose is roughly what you would get in three months on Earth..." (starts in 0.60s silence after "it." at 75.50)
VO_LEN = 21.50      # through "...So the thin air and the radiation are not what usually ends a robot's life on Mars." (ends 97.14; next word "The" at 98.06)
END_LEN = 3.10
TOTAL = round(VO_LEN + END_LEN, 2)  # 24.60 s
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
HOOK_ROWS = [("MARS RADIATION", WHITE), ("3 MONTHS DOSE", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 3.80, 7.50
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-11-21"  # Provisional backlog slot (after 025 week, lift_insight_quakes, and lift_curiosity_nuclear)

# Picture from v03f: 7 clean moving spans (2.80-3.30 s each), zero overlap with mon09_night_cold,
# wed11_opening_testA, thu12_length_test_dust, fri13_ingenuity_72, lift_insight_quakes, and lift_curiosity_nuclear.
SPAN = [
    (78.60,  2.80, "crop=ih*9/16:ih"),  # 0.00-2.80   NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207), frame 0
    (61.10,  3.00, "crop=ih*9/16:ih"),  # 2.80-5.80   NASA/JPL-Caltech Curiosity's View of Paraitepuy Pass (PIA25413) on "what you would get in three months on Earth" & scale bar
    (46.10,  3.10, "crop=ih*9/16:ih"),  # 5.80-8.90   NASA/JPL-Caltech Full-Circle Panorama Beside Namib Dune on Mars (PIA20284) on "A person would need a pressure suit"
    (484.20, 3.30, "crop=ih*9/16:ih"),  # 8.90-12.20  NASA/JPL-Caltech Perseverance's Office on Mars (PIA24765) under "But a robot does not breathe" & 9-14s title
    (462.20, 3.20, "crop=ih*9/16:ih"),  # 12.20-15.40 NASA/JPL-Caltech Curiosity Self-Portrait at Big Sky Drilling Site (PIA19920) under "and it does not get sick"
    (122.10, 3.10, "crop=ih*9/16:ih"),  # 15.40-18.50 NASA/JPL-Caltech Perseverance's Three Forks Sample Depot Selfie (PIA25681) under "So the thin air and the radiation"
    (430.35, 3.00, "crop=ih*9/16:ih"),  # 18.50-21.50 NASA/JPL-Caltech Perseverance's Selfie With 'Cheyava Falls' (PIA26344) under "are not what usually ends a robot's life on Mars"
]

WORDS_LIST = [
    {"w": "In", "s": 0.2, "e": 0.32},
    {"w": "one", "s": 0.42, "e": 0.64},
    {"w": "day", "s": 0.76, "e": 1.08},
    {"w": "on", "s": 1.14, "e": 1.28},
    {"w": "Mars,", "s": 1.32, "e": 1.74},
    {"w": "the", "s": 2.08, "e": 2.18},
    {"w": "dose", "s": 2.22, "e": 2.54},
    {"w": "is", "s": 2.64, "e": 2.76},
    {"w": "roughly", "s": 2.82, "e": 3.18},
    {"w": "what", "s": 3.2, "e": 3.34},
    {"w": "you", "s": 3.38, "e": 3.42},
    {"w": "would", "s": 3.44, "e": 3.58},
    {"w": "get", "s": 3.64, "e": 3.92},
    {"w": "in", "s": 4.04, "e": 4.28},
    {"w": "three", "s": 4.32, "e": 4.64},
    {"w": "months", "s": 4.78, "e": 5.26},
    {"w": "on", "s": 5.34, "e": 5.48},
    {"w": "Earth.", "s": 5.58, "e": 5.98},
    {"w": "A", "s": 6.9, "e": 6.96},
    {"w": "person", "s": 7.02, "e": 7.42},
    {"w": "would", "s": 7.44, "e": 7.56},
    {"w": "need", "s": 7.6, "e": 7.72},
    {"w": "a", "s": 7.76, "e": 7.84},
    {"w": "pressure", "s": 7.9, "e": 8.2},
    {"w": "suit", "s": 8.3, "e": 8.6},
    {"w": "just", "s": 8.78, "e": 9.02},
    {"w": "to", "s": 9.04, "e": 9.16},
    {"w": "stand", "s": 9.24, "e": 9.54},
    {"w": "there.", "s": 9.6, "e": 9.82},
    {"w": "But", "s": 11.02, "e": 11.12},
    {"w": "a", "s": 11.18, "e": 11.24},
    {"w": "robot", "s": 11.28, "e": 11.84},
    {"w": "does", "s": 11.88, "e": 12.06},
    {"w": "not", "s": 12.1, "e": 12.36},
    {"w": "breathe,", "s": 12.38, "e": 12.88},
    {"w": "and", "s": 13.32, "e": 13.38},
    {"w": "it", "s": 13.44, "e": 13.5},
    {"w": "does", "s": 13.54, "e": 13.7},
    {"w": "not", "s": 13.76, "e": 14.0},
    {"w": "get", "s": 14.04, "e": 14.24},
    {"w": "sick.", "s": 14.32, "e": 14.68},
    {"w": "So", "s": 15.58, "e": 15.68},
    {"w": "the", "s": 15.74, "e": 15.84},
    {"w": "thin", "s": 15.9, "e": 16.1},
    {"w": "air", "s": 16.18, "e": 16.46},
    {"w": "and", "s": 16.5, "e": 16.56},
    {"w": "the", "s": 16.6, "e": 16.68},
    {"w": "radiation", "s": 16.72, "e": 17.5},
    {"w": "are", "s": 17.82, "e": 17.96},
    {"w": "not", "s": 18.04, "e": 18.4},
    {"w": "what", "s": 18.42, "e": 18.62},
    {"w": "usually", "s": 18.74, "e": 19.12},
    {"w": "ends", "s": 19.2, "e": 19.52},
    {"w": "a", "s": 19.58, "e": 19.64},
    {"w": "robot's", "s": 19.68, "e": 20.16},
    {"w": "life", "s": 20.22, "e": 20.54},
    {"w": "on", "s": 20.6, "e": 20.74},
    {"w": "Mars.", "s": 20.78, "e": 21.24},
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


# One scale, two rows (Curiosity RAD surface radiation dose: 1 day on Mars ~ 3 months on Earth, Hassler et al. 2014 Science). Each label <= 4 words. No dark plate.
SCALE = [
    ("1 MARS DAY", "3 MONTHS DOSE", 100, YELLOW),
    ("1 EARTH DAY", "1 DAY DOSE", 18, WHITE),
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
        "values": [
            "Curiosity RAD surface radiation dose: 1 day on Mars is roughly what you would get in 3 months on Earth (Hassler et al. 2014, Science / NASA/JPL-Caltech)",
            "Earth global magnetic shield and thick atmosphere keep 1 day surface dose ~90x lower",
        ],
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
    rows = [("MARS RADIATION", WHITE), ("3 MONTHS DOSE", YELLOW)]
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
    times = [0.0, 0.5, 1.6, 4.5, 7.5, 11.0, 14.0, 17.0, 20.0, TOTAL - 0.5]
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
    hits = [(whoosh, 0.0), (tick, CARD_IN), (tick, TITLE_IN)]
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
        {"row": "s01_pia22207_mount_sharp", "timeline_in": 0.0, "timeline_out": 2.80, "source": "025_v03f_span_78.60.mp4", "upscale": 1.0, "framing": {"offset": 78.60}, "video": True},
        {"row": "s02_pia25413_paraitepuy", "timeline_in": 2.80, "timeline_out": 5.80, "source": "025_v03f_span_61.10.mp4", "upscale": 1.0, "framing": {"offset": 61.10}, "video": True},
        {"row": "s03_pia20284_namib_dune", "timeline_in": 5.80, "timeline_out": 8.90, "source": "025_v03f_span_46.10.mp4", "upscale": 1.0, "framing": {"offset": 46.10}, "video": True},
        {"row": "s04_pia24765_perseverance_office", "timeline_in": 8.90, "timeline_out": 12.20, "source": "025_v03f_span_484.20.mp4", "upscale": 1.0, "framing": {"offset": 484.20}, "video": True},
        {"row": "s05_pia19920_big_sky", "timeline_in": 12.20, "timeline_out": 15.40, "source": "025_v03f_span_462.20.mp4", "upscale": 1.0, "framing": {"offset": 462.20}, "video": True},
        {"row": "s06_pia25681_three_forks", "timeline_in": 15.40, "timeline_out": 18.50, "source": "025_v03f_span_122.10.mp4", "upscale": 1.0, "framing": {"offset": 122.10}, "video": True},
        {"row": "s07_pia26344_cheyava_falls", "timeline_in": 18.50, "timeline_out": 21.50, "source": "025_v03f_span_430.35.mp4", "upscale": 1.0, "framing": {"offset": 430.35}, "video": True},
        {"row": "s08_end_loop", "timeline_in": 21.50, "timeline_out": 24.60, "source": "end_card_loop_pia22207.mp4", "upscale": 1.0, "framing": {"offset": 78.60}, "video": True},
    ]
    pool = [
        {"file_id": "025_v03f_span_78.60.mp4", "title": "NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207, 78.60s)"},
        {"file_id": "025_v03f_span_61.10.mp4", "title": "NASA/JPL-Caltech Curiosity's View of Paraitepuy Pass (PIA25413, 61.10s)"},
        {"file_id": "025_v03f_span_46.10.mp4", "title": "NASA/JPL-Caltech Full-Circle Panorama Beside Namib Dune on Mars (PIA20284, 46.10s)"},
        {"file_id": "025_v03f_span_484.20.mp4", "title": "NASA/JPL-Caltech Perseverance's Office on Mars (PIA24765, 484.20s)"},
        {"file_id": "025_v03f_span_462.20.mp4", "title": "NASA/JPL-Caltech Curiosity Self-Portrait at Big Sky Drilling Site (PIA19920, 462.20s)"},
        {"file_id": "025_v03f_span_122.10.mp4", "title": "NASA/JPL-Caltech Perseverance's Three Forks Sample Depot Selfie (PIA25681, 122.10s)"},
        {"file_id": "025_v03f_span_430.35.mp4", "title": "NASA/JPL-Caltech Perseverance's Selfie With 'Cheyava Falls' (PIA26344, 430.35s)"},
        {"file_id": "end_card_loop_pia22207.mp4", "title": "End-card loop: NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207, 78.60s)"},
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
        "file": str(FINAL), "version": "v01", "job": "J0729",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v03f",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": [[s, l] for s, l, _ in SPAN],
            "why_picture": "Frame 0 is real NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207 at 78.60 s of v03f), moving immediately with a 16% push. Cuts land across Curiosity's View of Paraitepuy Pass (PIA25413 at 61.10 s) on 'what you would get in three months on Earth' and the 1 MARS DAY 3 MONTHS DOSE vs 1 EARTH DAY 1 DAY DOSE scale bar, Full-Circle Panorama Beside Namib Dune on Mars (PIA20284 at 46.10 s) on 'A person would need a pressure suit just to stand there', Perseverance's Office on Mars (PIA24765 at 484.20 s) under 'But a robot does not breathe' and the 9-14 s title, Curiosity Self-Portrait at Big Sky Drilling Site (PIA19920 at 462.20 s) under 'and it does not get sick', Perseverance's Three Forks Sample Depot Selfie (PIA25681 at 122.10 s) under 'So the thin air and the radiation', and Perseverance's Selfie With 'Cheyava Falls' (PIA26344 at 430.35 s) under 'are not what usually ends a robot's life on Mars'; zero overlap with mon09_night_cold, wed11_opening_testA, thu12_length_test_dust, fri13_ingenuity_72, lift_insight_quakes, and lift_curiosity_nuclear; skips chapter cards, burned captions, and Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening NASA/JPL-Caltech Mount Sharp 'Photobombs' Curiosity (PIA22207 at 78.60 s)", "youtube_id": LONG_ID, **endt},
        "audio": aud, "sfx_level_check": (sfx_chk.stdout or sfx_chk.stderr).strip(),
        "sfx_level_ok": sfx_chk.returncode == 0,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "polish_gate_ok": pg_chk.returncode == 0,
        "picture_qa_ok": pqa_chk.returncode == 0,
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(OUT / f"{STEM}_meta.json", UAT / f"{STEM}_meta.json")
    print(json.dumps({"sha256": meta["sha256"], "duration_s": meta["duration_s"], "words": meta["words"],
                      "gate_ok": meta["gate_ok"], "sfx_level_ok": meta["sfx_level_ok"],
                      "polish_gate_ok": meta["polish_gate_ok"], "picture_qa_ok": meta["picture_qa_ok"]}, indent=2))
    if not (meta["gate_ok"] and meta["sfx_level_ok"] and meta["polish_gate_ok"] and meta["picture_qa_ok"]):
        raise SystemExit("one or more checks failed")


if __name__ == "__main__":
    main()
