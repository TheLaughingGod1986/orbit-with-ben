#!/usr/bin/env python3
"""025 Short v01 — InSight on Mars: Four Years, 1,000+ Marsquakes, Silenced by Dust (J0668, backlog). No spend, no upload.

025 is the locked/uploaded OWB long (025_MarsRobot_full_rough_v03f.mp4, Js6EQJ8qDi8) with the fewest Shorts built among
live/locked longs (only 4 built video Shorts in 10_Shorts/: mon09_night_cold, wed11_opening_testA, thu12_length_test_dust,
fri13_ingenuity_72, and 0 standard 22-27 s backlog lift Shorts vs 3 on 021/022 and 4 on 023/024/026/027).
Lifts its own VO and picture from "Why does dust matter so much? Because on Mars, there is no rain to wash anything clean..."
through "...In December 2022, it went quiet the same way. Not broken, just out of light." (57 words, 22.40 s VO + 3.20 s
end card = 25.60 s total).
Frame 0 is real NASA InSight's Dusty Solar Panel (PIA25286 at 312.55 s of v03f), moving immediately with a 16% first-second
push, with 1,000+ QUAKES / OUT OF LIGHT hook caption.
Exact long title ("Could a Robot Survive on Mars?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar timeline/number call-out (FOUR YEARS  1,000+ QUAKES vs DECEMBER 2022  OUT OF LIGHT, stroke text only,
growing bars from a shared left edge, no dark box) at 14.30-18.10 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title and YouTube ID (Js6EQJ8qDi8) on the opening PIA25286 InSight solar panel plate so the last
seconds loop back to frame 0. House SFX kit only.
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
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/mars_insight_quakes_v01")
STEM = "mars_insight_quakes_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 308.30      # "Why does dust matter so much?..." (starts in 1.62s silence after "off." at 306.82)
VO_LEN = 22.40      # through "...Not broken, just out of light." (word ends 330.50; next word "Even" at 331.50)
END_LEN = 3.20
TOTAL = round(VO_LEN + END_LEN, 2)  # 25.60 s
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
HOOK_ROWS = [("1,000+ QUAKES", WHITE), ("OUT OF LIGHT", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 14.30, 18.10
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-11-16"  # Provisional backlog slot (after 025 week Mon 9 / Wed 11 / Thu 12 / Fri 13 Nov)

# Picture from v03f: 7 clean moving spans (2.45-3.85 s each), zero overlap with mon09_night_cold,
# wed11_opening_testA, thu12_length_test_dust, and fri13_ingenuity_72.
SPAN = [
    (312.55, 2.45, "crop=ih*9/16:ih"),        # 0.00-2.45   NASA InSight's Dusty Solar Panel (PIA25286), frame 0
    (70.75,  3.65, "crop=ih*9/16:ih"),        # 2.45-6.10   NASA Martian Boxwork desert rock and ridge (PIA26559) on "Because on Mars, there is no rain to wash anything clean"
    (308.00, 3.35, "crop=ih*9/16:ih"),        # 6.10-9.45   NASA InSight's Dusty Selfie deck and arm (PIA23203) on "The lander InSight spent four years listening"
    (322.25, 3.25, "crop=ih*9/16:ih"),        # 9.45-12.70  NASA InSight's Deck and SEIS Seismometer (PIA22871) under "for Mars quakes and felt more than a thousand of them" & 9-14s title
    (326.15, 2.95, "crop=ih*9/16:ih:480:0"),  # 12.70-15.65 NASA InSight's Final Selfie dust-blanketed deck (PIA25287) under "But dust kept building on its panels"
    (74.95,  3.85, "crop=ih*9/16:ih"),        # 15.65-19.50 NASA Martian Gator-Back bedrock and dust (PIA25176) under "In December 2022, it went quiet the same way" & timeline bar
    (235.50, 2.90, "crop=ih*9/16:ih"),        # 19.50-22.40 NASA Martian plain and crater rim horizon (PIA16122) under "Not broken, just out of light"
]

WORDS_LIST = [
    {"w": "Why", "s": 0.14, "e": 0.26},
    {"w": "does", "s": 0.28, "e": 0.48},
    {"w": "dust", "s": 0.54, "e": 0.90},
    {"w": "matter", "s": 0.96, "e": 1.18},
    {"w": "so", "s": 1.26, "e": 1.38},
    {"w": "much?", "s": 1.48, "e": 1.82},
    {"w": "Because", "s": 2.48, "e": 2.68},
    {"w": "on", "s": 2.72, "e": 2.84},
    {"w": "Mars,", "s": 2.90, "e": 3.32},
    {"w": "there", "s": 3.40, "e": 3.48},
    {"w": "is", "s": 3.52, "e": 3.66},
    {"w": "no", "s": 3.74, "e": 3.88},
    {"w": "rain", "s": 4.00, "e": 4.28},
    {"w": "to", "s": 4.38, "e": 4.46},
    {"w": "wash", "s": 4.52, "e": 4.78},
    {"w": "anything", "s": 4.82, "e": 5.20},
    {"w": "clean.", "s": 5.30, "e": 5.70},
    {"w": "The", "s": 6.48, "e": 6.56},
    {"w": "lander", "s": 6.62, "e": 6.94},
    {"w": "InSight", "s": 7.06, "e": 7.62},
    {"w": "spent", "s": 7.76, "e": 8.10},
    {"w": "four", "s": 8.16, "e": 8.36},
    {"w": "years", "s": 8.50, "e": 8.88},
    {"w": "listening", "s": 8.94, "e": 9.28},
    {"w": "for", "s": 9.30, "e": 9.40},
    {"w": "Mars", "s": 9.44, "e": 9.76},
    {"w": "quakes", "s": 9.80, "e": 10.24},
    {"w": "and", "s": 10.58, "e": 10.68},
    {"w": "felt", "s": 10.80, "e": 11.12},
    {"w": "more", "s": 11.16, "e": 11.30},
    {"w": "than", "s": 11.32, "e": 11.42},
    {"w": "a", "s": 11.46, "e": 11.52},
    {"w": "thousand", "s": 11.58, "e": 11.98},
    {"w": "of", "s": 12.04, "e": 12.16},
    {"w": "them.", "s": 12.22, "e": 12.38},
    {"w": "But", "s": 13.00, "e": 13.18},
    {"w": "dust", "s": 13.22, "e": 13.56},
    {"w": "kept", "s": 13.68, "e": 13.90},
    {"w": "building", "s": 13.92, "e": 14.22},
    {"w": "on", "s": 14.26, "e": 14.32},
    {"w": "its", "s": 14.36, "e": 14.50},
    {"w": "panels.", "s": 14.58, "e": 15.06},
    {"w": "In", "s": 15.82, "e": 15.88},
    {"w": "December", "s": 15.92, "e": 16.30},
    {"w": "2022,", "s": 16.52, "e": 17.34},
    {"w": "it", "s": 17.72, "e": 17.80},
    {"w": "went", "s": 17.84, "e": 18.04},
    {"w": "quiet", "s": 18.12, "e": 18.48},
    {"w": "the", "s": 18.50, "e": 18.60},
    {"w": "same", "s": 18.66, "e": 18.92},
    {"w": "way.", "s": 18.98, "e": 19.28},
    {"w": "Not", "s": 19.78, "e": 19.94},
    {"w": "broken,", "s": 19.98, "e": 20.48},
    {"w": "just", "s": 20.90, "e": 21.18},
    {"w": "out", "s": 21.48, "e": 21.62},
    {"w": "of", "s": 21.68, "e": 21.78},
    {"w": "light.", "s": 21.84, "e": 22.20},
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


# One scale, two rows (InSight 4 years listening, 1,000+ marsquakes felt vs December 2022 out of light, NASA/JPL-Caltech). Each label <= 4 words. No dark plate.
SCALE = [
    ("FOUR YEARS", "1,000+ QUAKES", 100, YELLOW),
    ("DECEMBER 2022", "OUT OF LIGHT", 35, WHITE),
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
        "values": ["4 years listening on Mars (2018-2022), more than 1,000 (1,300+) marsquakes detected (NASA/JPL-Caltech)", "December 2022: solar panels covered in dust, mission ended out of light (NASA/JPL-Caltech)"],
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
    im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(5)), 0.20)
    im = ImageEnhance.Brightness(im).enhance(0.88)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse((80, BAND_Y0 - 20, W - 80, BAND_Y0 + BAND_H + 20), fill=75)
    shade = shade.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.80)
    d = ImageDraw.Draw(im)
    rows = [("1,000+ QUAKES", WHITE), ("OUT OF LIGHT", YELLOW)]
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
    times = [0.0, 0.5, 1.6, 4.5, 8.0, 11.0, 14.0, 16.5, 20.5, TOTAL - 0.5]
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
        {"row": "s01_pia25286_insight_solar", "timeline_in": 0.0, "timeline_out": 2.45, "source": "025_v03f_span_312.55.mp4", "upscale": 1.0, "framing": {"offset": 312.55}, "video": True},
        {"row": "s02_pia26559_mars_desert", "timeline_in": 2.45, "timeline_out": 6.10, "source": "025_v03f_span_70.75.mp4", "upscale": 1.0, "framing": {"offset": 70.75}, "video": True},
        {"row": "s03_pia23203_insight_selfie", "timeline_in": 6.10, "timeline_out": 9.45, "source": "025_v03f_span_308.00.mp4", "upscale": 1.0, "framing": {"offset": 308.00}, "video": True},
        {"row": "s04_pia22871_insight_seis", "timeline_in": 9.45, "timeline_out": 12.70, "source": "025_v03f_span_322.25.mp4", "upscale": 1.0, "framing": {"offset": 322.25}, "video": True},
        {"row": "s05_pia25287_final_selfie", "timeline_in": 12.70, "timeline_out": 15.65, "source": "025_v03f_span_326.15.mp4", "upscale": 1.0, "framing": {"offset": 326.15}, "video": True},
        {"row": "s06_pia25176_mars_bedrock", "timeline_in": 15.65, "timeline_out": 19.50, "source": "025_v03f_span_74.95.mp4", "upscale": 1.0, "framing": {"offset": 74.95}, "video": True},
        {"row": "s07_pia16122_mars_plain", "timeline_in": 19.50, "timeline_out": 22.40, "source": "025_v03f_span_235.50.mp4", "upscale": 1.0, "framing": {"offset": 235.50}, "video": True},
        {"row": "s08_end_loop", "timeline_in": 22.40, "timeline_out": 25.60, "source": "end_card_loop_pia25286.mp4", "upscale": 1.0, "framing": {"offset": 312.55}, "video": True},
    ]
    pool = [
        {"file_id": "025_v03f_span_312.55.mp4", "title": "NASA/JPL-Caltech InSight's Dusty Solar Panel (PIA25286, 312.55s)"},
        {"file_id": "025_v03f_span_70.75.mp4", "title": "NASA/JPL-Caltech Martian Boxwork desert rock and ridge (PIA26559, 70.75s)"},
        {"file_id": "025_v03f_span_308.00.mp4", "title": "NASA/JPL-Caltech InSight's Dusty Selfie deck and arm (PIA23203, 308.00s)"},
        {"file_id": "025_v03f_span_322.25.mp4", "title": "NASA/JPL-Caltech Full View of InSight's Deck and Two Science Instruments (PIA22871, 322.25s)"},
        {"file_id": "025_v03f_span_326.15.mp4", "title": "NASA/JPL-Caltech InSight's Final Selfie dust-blanketed deck (PIA25287, 326.15s)"},
        {"file_id": "025_v03f_span_74.95.mp4", "title": "NASA/JPL-Caltech Martian Gator-Back bedrock and red dust (PIA25176, 74.95s)"},
        {"file_id": "025_v03f_span_235.50.mp4", "title": "NASA/JPL-Caltech Martian plain and crater rim horizon (PIA16122, 235.50s)"},
        {"file_id": "end_card_loop_pia25286.mp4", "title": "End-card loop: NASA/JPL-Caltech InSight's Dusty Solar Panel (PIA25286, 312.55s)"},
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
        "file": str(FINAL), "version": "v01", "job": "J0668",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v03f",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": [[s, l] for s, l, _ in SPAN],
            "why_picture": "Frame 0 is real NASA/JPL-Caltech InSight's Dusty Solar Panel (PIA25286 at 312.55 s of v03f), moving immediately with a 16% push. Cuts land across Martian Boxwork desert rock and ridge (PIA26559 at 70.75 s) on 'Because on Mars, there is no rain to wash anything clean', InSight's Dusty Selfie deck and arm (PIA23203 at 308.00 s) on 'The lander InSight spent four years listening', Full View of InSight's Deck and Two Science Instruments (PIA22871 at 322.25 s, showing the white SEIS seismometer dome on Mars) under 'for Mars quakes and felt more than a thousand of them' and the 9-14 s title, InSight's Final Selfie dust-blanketed deck (PIA25287 at 326.15 s) under 'But dust kept building on its panels', Martian Gator-Back bedrock and red dust (PIA25176 at 74.95 s) under 'In December 2022, it went quiet the same way' and the FOUR YEARS 1,000+ QUAKES vs DECEMBER 2022 OUT OF LIGHT scale bar, and Martian plain and crater rim horizon (PIA16122 at 235.50 s) under 'Not broken, just out of light'; zero overlap with mon09_night_cold, wed11_opening_testA, thu12_length_test_dust, and fri13_ingenuity_72; skips chapter cards, burned captions, and Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening NASA/JPL-Caltech InSight's Dusty Solar Panel (PIA25286 at 312.55 s)", "youtube_id": LONG_ID, **endt},
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
