#!/usr/bin/env python3
"""021 Short v01 — Saturn's Rings Weigh Less Than Half of One Small Moon (J0516, backlog). No spend, no upload.

021 is the live OWB long (saturn_first_cut_v03f.mp4, 55AEQwvs36g) with the fewest Shorts built among live/locked v05
longs (3: monday_saturn_tease, clock_100_300my, late_arrival_4_5b vs 4 on 022 and 6 on 023/024/025/026).
Lifts its own VO and picture from "The mass under that shine is small for the area it covers..." through
"...The mystery starts as a fall, not as a monument." (58 words, 21.80 s VO + 3.20 s end card = 25.00 s total).
Frame 0 is real NASA Cassini natural-colour portrait of Saturn and its concentric rings (PIA21046 at 315.30 s of v03f),
moving immediately with a 16% first-second push, with SATURN'S RINGS / 0.4x ONE MOON hook caption.
Exact long title ("How Long Do Saturn's Rings Have Left?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar scale comparison (RINGS MASS 0.4x MIMAS vs MOON MIMAS 1.0x MIMAS, stroke text only, growing bars
from a shared left edge, no dark box) at 14.30-18.10 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title and YouTube ID (55AEQwvs36g) on the opening PIA21046 Saturn plate so the last seconds
loop back to frame 0. House SFX kit only.
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

LONG = FILM / "07_Edit-Project/saturn_film/work_first_cut_v03f"
PICTURE = LONG / "picture_all.mp4"
VO = LONG / "vo_timeline.wav"
BED = LONG / "music_raw.m4a"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v01"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_mimas_mass_v01")
STEM = "saturn_mimas_mass_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 73.76       # "The mass under that shine is small for the area it covers..."
VO_LEN = 21.80      # through "...not as a monument." (word ends 95.32; next word "but" at 96.16)
END_LEN = 3.20
TOTAL = round(VO_LEN + END_LEN, 2)  # 25.00 s
FPS = 30
W, H = 1080, 1920
PUSH = 0.16
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
LONG_TITLE = "How Long Do Saturn's Rings Have Left?"
LONG_ID = "55AEQwvs36g"
TITLE_ROWS = ["How Long Do", "Saturn's Rings", "Have Left?"]
END_ROWS = [("How Long Do", WHITE), ("Saturn's Rings", WHITE), ("Have Left?", WHITE), (LONG_ID, YELLOW)]
HOOK_ROWS = [("SATURN'S RINGS", WHITE), ("0.4\u00d7 ONE MOON", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 14.30, 18.10
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-10-30"  # Provisional backlog slot

# Picture from v03f: 6 clean moving spans (3.15-4.35 s each), every cut snapped inside a 0.40-0.94 s VO pause,
# zero overlap with monday_saturn_tease, clock_100_300my, and late_arrival_4_5b, matching Saturn, rings and Mimas mass lines.
SPAN = [
    (315.30, 4.35),  # 0.00-4.35   NASA Cassini Saturn Approaching Northern Summer (PIA21046), frame 0
    (37.85, 3.55),   # 4.35-7.90   NASA Cassini Translucent Arcs across Saturn rings (PIA14943)
    (83.35, 3.15),   # 7.90-11.05  NASA Crescent Saturn with Rings and Ring Shadows (PIA00335) under 9-14s title
    (136.98, 3.85),  # 11.05-14.90 NASA Saturn Rings High Resolution concentric lanes (PIA02275) under "two fifths of Mimas"
    (68.35, 3.25),   # 14.90-18.15 NASA Colorful Structure at Fine Scales in Saturn rings (PIA21628) under 0.4x vs 1.0x Mimas scale bar
    (146.68, 3.65),  # 18.15-21.80 NASA Behold B Ring Clumps (PIA11569) under "The mystery starts as a fall, not as a monument"
]

WORDS_LIST = [
    {"w": "The", "s": 0.0, "e": 0.36},
    {"w": "mass", "s": 0.36, "e": 0.64},
    {"w": "under", "s": 0.64, "e": 1.02},
    {"w": "that", "s": 1.02, "e": 1.34},
    {"w": "shine", "s": 1.34, "e": 1.62},
    {"w": "is", "s": 1.62, "e": 2.2},
    {"w": "small", "s": 2.2, "e": 2.54},
    {"w": "for", "s": 2.54, "e": 3.02},
    {"w": "the", "s": 3.02, "e": 3.14},
    {"w": "area", "s": 3.14, "e": 3.38},
    {"w": "it", "s": 3.38, "e": 3.68},
    {"w": "covers.", "s": 3.68, "e": 4.04},
    {"w": "Cassini", "s": 4.7, "e": 5.14},
    {"w": "weighed", "s": 5.14, "e": 5.52},
    {"w": "the", "s": 5.52, "e": 5.9},
    {"w": "rings", "s": 5.9, "e": 6.12},
    {"w": "on", "s": 6.12, "e": 6.5},
    {"w": "its", "s": 6.5, "e": 6.64},
    {"w": "last", "s": 6.64, "e": 6.92},
    {"w": "orbits", "s": 6.92, "e": 7.46},
    {"w": "and", "s": 7.82, "e": 8.32},
    {"w": "found", "s": 8.32, "e": 8.52},
    {"w": "less", "s": 8.52, "e": 8.98},
    {"w": "than", "s": 8.98, "e": 9.32},
    {"w": "many", "s": 9.32, "e": 9.54},
    {"w": "maps", "s": 9.54, "e": 9.88},
    {"w": "had", "s": 9.88, "e": 10.22},
    {"w": "assumed,", "s": 10.22, "e": 10.58},
    {"w": "on", "s": 11.52, "e": 11.62},
    {"w": "the", "s": 11.62, "e": 11.76},
    {"w": "order", "s": 11.76, "e": 12.02},
    {"w": "of", "s": 12.02, "e": 12.24},
    {"w": "two", "s": 12.24, "e": 12.5},
    {"w": "fifths", "s": 12.5, "e": 12.94},
    {"w": "of", "s": 12.94, "e": 13.34},
    {"w": "the", "s": 13.34, "e": 13.5},
    {"w": "little", "s": 13.5, "e": 13.72},
    {"w": "moon", "s": 13.72, "e": 13.96},
    {"w": "Mimas.", "s": 13.96, "e": 14.66},
    {"w": "A", "s": 15.12, "e": 15.3},
    {"w": "lot", "s": 15.3, "e": 15.44},
    {"w": "of", "s": 15.44, "e": 15.62},
    {"w": "scenery.", "s": 15.62, "e": 15.84},
    {"w": "Not", "s": 16.76, "e": 17.04},
    {"w": "a", "s": 17.04, "e": 17.28},
    {"w": "lot", "s": 17.28, "e": 17.42},
    {"w": "of", "s": 17.42, "e": 17.56},
    {"w": "stuff.", "s": 17.56, "e": 17.8},
    {"w": "The", "s": 18.42, "e": 18.64},
    {"w": "mystery", "s": 18.64, "e": 18.94},
    {"w": "starts", "s": 18.94, "e": 19.38},
    {"w": "as", "s": 19.38, "e": 19.7},
    {"w": "a", "s": 19.7, "e": 19.8},
    {"w": "fall,", "s": 19.8, "e": 20.08},
    {"w": "not", "s": 20.74, "e": 21.02},
    {"w": "as", "s": 21.02, "e": 21.28},
    {"w": "a", "s": 21.28, "e": 21.38},
    {"w": "monument.", "s": 21.38, "e": 21.56},
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
    stroke_fill = (0, 0, 0, fill[3] if len(fill) == 4 else 255)
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
        bboxes.append(centred(d, y, t, f, c, stroke=7))
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


# One scale, two rows (Saturn ring mass ~0.41 Mimas vs Mimas 1.0 Mimas, Iess et al. 2019 Science). Each label <= 4 words. No dark plate.
SCALE = [
    ("RINGS MASS", "0.4\u00d7 MIMAS", 40, YELLOW),
    ("MOON MIMAS", "1.0\u00d7 MIMAS", 100, WHITE),
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
        "values_mass": ["~0.41 Mimas (1.54 x 10^19 kg, Cassini Grand Finale gravity, Iess et al. 2019 Science)", "1.0 Mimas (3.75 x 10^19 kg)"],
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


def _cut(src_t: float, length: float, dest: Path) -> None:
    pre = max(0.0, src_t - 2.0)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{pre:.3f}", "-i", str(PICTURE),
         "-ss", f"{src_t - pre:.3f}", "-t", f"{length:.3f}", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-video_track_timescale", "30000", str(dest)])


def accurate_span(dest: Path) -> None:
    if abs(sum(length for _, length in SPAN) - VO_LEN) > 0.05:
        raise SystemExit(f"span {sum(l for _, l in SPAN)} != VO_LEN {VO_LEN}")
    lines = []
    for i, (src_t, length) in enumerate(SPAN):
        piece = WORK / f"span_{i}.mp4"
        _cut(src_t, length, piece)
        lines.append(f"file '{piece.name}'")
    lst = WORK / "span_list.txt"
    lst.write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(dest)])


def end_plate(dest: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "picture_span.mp4"), "-frames:v", "1",
         "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos", str(WORK / "plate0.png")])
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(14)), 0.55)
    im = ImageEnhance.Brightness(im).enhance(0.84)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse((80, BAND_Y0 - 20, W - 80, BAND_Y0 + BAND_H + 20), fill=90)
    shade = shade.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.80)
    d = ImageDraw.Draw(im)
    rows = [("SATURN'S RINGS", WHITE), ("0.4\u00d7 ONE MOON", YELLOW)]
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
    times = [0.0, 0.5, 1.6, 5.5, 9.5, 12.5, 15.5, 17.5, 20.0, TOTAL - 0.5]
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
        f"[0:v]fps={FPS},crop=ih*9/16:ih,"
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
        {"row": "s01_pia21046_saturn_summer", "timeline_in": 0.0, "timeline_out": 4.35, "source": "021_v03f_span_315.30.mp4", "upscale": 1.0, "framing": {"offset": 315.30}, "video": True},
        {"row": "s02_pia14943_translucent_arcs", "timeline_in": 4.35, "timeline_out": 7.90, "source": "021_v03f_span_37.85.mp4", "upscale": 1.0, "framing": {"offset": 37.85}, "video": True},
        {"row": "s03_pia00335_crescent_saturn", "timeline_in": 7.90, "timeline_out": 11.05, "source": "021_v03f_span_83.35.mp4", "upscale": 1.0, "framing": {"offset": 83.35}, "video": True},
        {"row": "s04_pia02275_high_res_rings", "timeline_in": 11.05, "timeline_out": 14.90, "source": "021_v03f_span_136.98.mp4", "upscale": 1.0, "framing": {"offset": 136.98}, "video": True},
        {"row": "s05_pia21628_fine_scales", "timeline_in": 14.90, "timeline_out": 18.15, "source": "021_v03f_span_68.35.mp4", "upscale": 1.0, "framing": {"offset": 68.35}, "video": True},
        {"row": "s06_pia11569_b_ring_clumps", "timeline_in": 18.15, "timeline_out": 21.80, "source": "021_v03f_span_146.68.mp4", "upscale": 1.0, "framing": {"offset": 146.68}, "video": True},
        {"row": "s07_end_loop", "timeline_in": 21.80, "timeline_out": 25.00, "source": "end_card_loop_pia21046.mp4", "upscale": 1.0, "framing": {"offset": 315.30}, "video": True},
    ]
    pool = [
        {"file_id": "021_v03f_span_315.30.mp4", "title": "NASA Cassini Saturn Approaching Northern Summer portrait (PIA21046, 315.30s)"},
        {"file_id": "021_v03f_span_37.85.mp4", "title": "NASA Cassini Translucent Arcs across Saturn rings (PIA14943, 37.85s)"},
        {"file_id": "021_v03f_span_83.35.mp4", "title": "NASA Crescent Saturn with Rings and Ring Shadows (PIA00335, 83.35s)"},
        {"file_id": "021_v03f_span_136.98.mp4", "title": "NASA Saturn Rings High Resolution concentric lanes (PIA02275, 136.98s)"},
        {"file_id": "021_v03f_span_68.35.mp4", "title": "NASA Cassini Colorful Structure at Fine Scales in Saturn rings (PIA21628, 68.35s)"},
        {"file_id": "021_v03f_span_146.68.mp4", "title": "NASA Cassini Behold B Ring Clumps (PIA11569, 146.68s)"},
        {"file_id": "end_card_loop_pia21046.mp4", "title": "End-card loop: NASA Cassini Saturn Approaching Northern Summer (PIA21046, 315.30s)"},
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
        "file": str(FINAL), "version": "v01", "job": "J0516",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v03f",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": SPAN,
            "why_picture": "Frame 0 is real NASA Cassini Saturn Approaching Northern Summer portrait (PIA21046 at 315.30 s of v03f), moving immediately with a 16% push. Cuts land in VO pauses across Translucent Arcs (PIA14943 at 37.85 s), Crescent Saturn with Rings and Ring Shadows (PIA00335 at 83.35 s) under the 9-14 s title, Saturn Rings High Resolution concentric lanes (PIA02275 at 136.98 s) on the 'two fifths of the little moon Mimas' line, Colorful Structure at Fine Scales (PIA21628 at 68.35 s) under the 0.4x vs 1.0x Mimas scale bar, and Behold B Ring Clumps (PIA11569 at 146.68 s) under 'The mystery starts as a fall, not as a monument'; zero overlap with monday_saturn_tease, clock_100_300my, and late_arrival_4_5b; skips chapter cards, burned captions, and Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening Cassini Saturn Approaching Northern Summer plate (PIA21046 at 315.30 s)", "youtube_id": LONG_ID, **endt},
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
