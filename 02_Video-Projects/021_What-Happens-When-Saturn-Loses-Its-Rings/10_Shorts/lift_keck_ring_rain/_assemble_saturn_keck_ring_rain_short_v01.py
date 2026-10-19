#!/usr/bin/env python3
"""021 Short v01 — Keck Ring Rain: How Astronomers on Earth Measured Saturn's Rings Raining In (J0653, backlog). No spend, no upload.

021 is the live OWB long (saturn_first_cut_v03f.mp4, 55AEQwvs36g) with the fewest Shorts built among live/locked longs
(5 in 10_Shorts/: monday_saturn_tease, clock_100_300my, late_arrival_4_5b, lift_mimas_mass, lift_ten_hour_day vs 6 on
022/025 and 7 on 023/024/026/027, and only 2 backlog lift Shorts vs 3 on 022 and 4 on 023/024/026/027).
Lifts its own VO and picture from "Ring rain. We did not need a spacecraft inside that rain to know it was there..."
through "...At that magnetic rain rate alone, the sheet would last about three hundred million years." (56 words,
22.80 s VO + 3.20 s end card = 26.00 s total).
Frame 0 is real NASA Saturn and its Rings golden portrait (PIA01969 at 360.15 s of v03f), moving
immediately with a 16% first-second push, with RING RAIN / 300M YEARS hook caption.
Exact long title ("How Long Do Saturn's Rings Have Left?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar scale comparison (MAGNETIC RAIN  300M YRS vs WITH D-RING  100M YRS, stroke text only, growing bars
from a shared left edge, no dark box) at 14.30-18.10 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title and YouTube ID (55AEQwvs36g) on the opening PIA01969 Saturn plate so the last seconds
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
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_keck_ring_rain_v01")
STEM = "saturn_keck_ring_rain_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 255.60      # "Ring rain. We did not need a spacecraft..." (starts in 0.68s silence after "above." at 255.04)
VO_LEN = 22.80      # through "...about three hundred million years." (word ends 278.12; next word "But" at 279.00)
END_LEN = 3.20
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
LONG_TITLE = "How Long Do Saturn's Rings Have Left?"
LONG_ID = "55AEQwvs36g"
TITLE_ROWS = ["How Long Do", "Saturn's Rings", "Have Left?"]
END_ROWS = [("How Long Do", WHITE), ("Saturn's Rings", WHITE), ("Have Left?", WHITE), (LONG_ID, YELLOW)]
HOOK_ROWS = [("RING RAIN", WHITE), ("300M YEARS", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 14.30, 18.10
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-10-30"  # Provisional backlog slot

# Picture from v03f: 7 clean moving spans (2.35-3.80 s each), zero overlap with monday_saturn_tease,
# clock_100_300my, late_arrival_4_5b, lift_mimas_mass, and lift_ten_hour_day.
SPAN = [
    (360.15, 3.55),  # 0.00-3.55   NASA Saturn and its Rings golden portrait (PIA01969), frame 0
    (132.60, 2.35),  # 3.55-5.90   NASA Cassini Saturn B Ring Finer Than Ever (PIA21058) on "that rain to know it was there"
    (167.50, 3.75),  # 5.90-9.65   NASA Cassini A-Ring Structures sunlit ring edge (PIA12727) on "Astronomers on Earth, using the Keck telescope"
    (310.10, 3.80),  # 9.65-13.45  NASA Cassini So Far from Home Saturn and ring plane (PIA21345) under "watched the glow of that water in Saturn's upper air" & 9-14s title
    (331.50, 2.90),  # 13.45-16.35 NASA Cassini The Inner Rings concentric lanes (PIA08869) under "and measured how fast the ice was leaving" & scale bar
    (336.50, 2.65),  # 16.35-19.00 NASA Cassini Inner B Ring Terminus ice lanes (PIA11671) under "At that magnetic rain rate alone" & scale bar
    (341.50, 3.80),  # 19.00-22.80 NASA Cassini Panoramic Rings colour bands (PIA06175) under "the sheet would last about three hundred million years"
]

WORDS_LIST = [
    {"w": "Ring", "s": 0.12, "e": 0.46},
    {"w": "rain.", "s": 0.46, "e": 0.72},
    {"w": "We", "s": 1.48, "e": 1.64},
    {"w": "did", "s": 1.64, "e": 1.80},
    {"w": "not", "s": 1.80, "e": 1.94},
    {"w": "need", "s": 1.94, "e": 2.24},
    {"w": "a", "s": 2.24, "e": 2.38},
    {"w": "spacecraft", "s": 2.38, "e": 2.82},
    {"w": "inside", "s": 2.82, "e": 3.56},
    {"w": "that", "s": 3.56, "e": 3.90},
    {"w": "rain", "s": 3.90, "e": 4.20},
    {"w": "to", "s": 4.20, "e": 4.50},
    {"w": "know", "s": 4.50, "e": 4.74},
    {"w": "it", "s": 4.74, "e": 4.92},
    {"w": "was", "s": 4.92, "e": 5.06},
    {"w": "there.", "s": 5.06, "e": 5.58},
    {"w": "Astronomers", "s": 6.30, "e": 6.94},
    {"w": "on", "s": 6.94, "e": 7.18},
    {"w": "Earth,", "s": 7.18, "e": 7.48},
    {"w": "using", "s": 7.92, "e": 8.26},
    {"w": "the", "s": 8.26, "e": 8.46},
    {"w": "Keck", "s": 8.46, "e": 8.76},
    {"w": "telescope,", "s": 8.76, "e": 9.24},
    {"w": "watched", "s": 10.14, "e": 10.30},
    {"w": "the", "s": 10.30, "e": 10.62},
    {"w": "glow", "s": 10.62, "e": 10.90},
    {"w": "of", "s": 10.90, "e": 11.12},
    {"w": "that", "s": 11.12, "e": 11.26},
    {"w": "water", "s": 11.26, "e": 11.62},
    {"w": "in", "s": 11.62, "e": 11.94},
    {"w": "Saturn's", "s": 11.94, "e": 12.56},
    {"w": "upper", "s": 12.56, "e": 12.68},
    {"w": "air", "s": 12.68, "e": 13.20},
    {"w": "and", "s": 13.72, "e": 13.78},
    {"w": "measured", "s": 13.78, "e": 14.12},
    {"w": "how", "s": 14.12, "e": 14.38},
    {"w": "fast", "s": 14.38, "e": 14.84},
    {"w": "the", "s": 14.84, "e": 15.06},
    {"w": "ice", "s": 15.06, "e": 15.24},
    {"w": "was", "s": 15.24, "e": 15.56},
    {"w": "leaving.", "s": 15.56, "e": 15.96},
    {"w": "At", "s": 16.78, "e": 16.90},
    {"w": "that", "s": 16.90, "e": 17.08},
    {"w": "magnetic", "s": 17.08, "e": 17.48},
    {"w": "rain", "s": 17.48, "e": 17.94},
    {"w": "rate", "s": 17.94, "e": 18.32},
    {"w": "alone,", "s": 18.32, "e": 18.64},
    {"w": "the", "s": 19.40, "e": 19.50},
    {"w": "sheet", "s": 19.50, "e": 19.76},
    {"w": "would", "s": 19.76, "e": 20.06},
    {"w": "last", "s": 20.06, "e": 20.32},
    {"w": "about", "s": 20.32, "e": 20.82},
    {"w": "three", "s": 20.82, "e": 21.08},
    {"w": "hundred", "s": 21.08, "e": 21.36},
    {"w": "million", "s": 21.36, "e": 22.02},
    {"w": "years.", "s": 22.02, "e": 22.52},
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


# One scale, two rows (Keck magnetic ring rain lifetime ~300 Myr, O'Donoghue et al. 2019 vs ~100 Myr with D-ring inflow, Waite et al. 2018). Each label <= 4 words. No dark plate.
SCALE = [
    ("MAGNETIC RAIN", "300M YRS", 100, YELLOW),
    ("WITH D-RING", "100M YRS", 33, WHITE),
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
        "values": ["~300 million years at magnetic ring rain rate alone (O'Donoghue et al. 2019, Keck)", "under ~100 million years adding D-ring equatorial inflow (Waite et al. 2018, Cassini Grand Finale)"],
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
    rows = [("RING RAIN", WHITE), ("300M YEARS", YELLOW)]
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
    times = [0.0, 0.5, 1.6, 4.8, 9.5, 12.5, 15.5, 17.5, 20.5, TOTAL - 0.5]
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
        {"row": "s01_pia01969_saturn_rings", "timeline_in": 0.0, "timeline_out": 3.55, "source": "021_v03f_span_360.15.mp4", "upscale": 1.0, "framing": {"offset": 360.15}, "video": True},
        {"row": "s02_pia21058_b_ring_finer", "timeline_in": 3.55, "timeline_out": 5.90, "source": "021_v03f_span_132.60.mp4", "upscale": 1.0, "framing": {"offset": 132.60}, "video": True},
        {"row": "s03_pia12727_a_ring_structures", "timeline_in": 5.90, "timeline_out": 9.65, "source": "021_v03f_span_167.50.mp4", "upscale": 1.0, "framing": {"offset": 167.50}, "video": True},
        {"row": "s04_pia21345_so_far_from_home", "timeline_in": 9.65, "timeline_out": 13.45, "source": "021_v03f_span_310.10.mp4", "upscale": 1.0, "framing": {"offset": 310.10}, "video": True},
        {"row": "s05_pia08869_inner_rings", "timeline_in": 13.45, "timeline_out": 16.35, "source": "021_v03f_span_331.50.mp4", "upscale": 1.0, "framing": {"offset": 331.50}, "video": True},
        {"row": "s06_pia11671_inner_b_ring", "timeline_in": 16.35, "timeline_out": 19.00, "source": "021_v03f_span_336.50.mp4", "upscale": 1.0, "framing": {"offset": 336.50}, "video": True},
        {"row": "s07_pia06175_panoramic_rings", "timeline_in": 19.00, "timeline_out": 22.80, "source": "021_v03f_span_341.50.mp4", "upscale": 1.0, "framing": {"offset": 341.50}, "video": True},
        {"row": "s08_end_loop", "timeline_in": 22.80, "timeline_out": 26.00, "source": "end_card_loop_pia01969.mp4", "upscale": 1.0, "framing": {"offset": 360.15}, "video": True},
    ]
    pool = [
        {"file_id": "021_v03f_span_360.15.mp4", "title": "NASA Saturn and its Rings golden portrait (PIA01969, 360.15s)"},
        {"file_id": "021_v03f_span_132.60.mp4", "title": "NASA Cassini Saturn B Ring, Finer Than Ever (PIA21058, 132.60s)"},
        {"file_id": "021_v03f_span_167.50.mp4", "title": "NASA Cassini A-Ring Structures sunlit ring edge (PIA12727, 167.50s)"},
        {"file_id": "021_v03f_span_310.10.mp4", "title": "NASA Cassini So Far from Home Saturn and ring plane (PIA21345, 310.10s)"},
        {"file_id": "021_v03f_span_331.50.mp4", "title": "NASA Cassini The Inner Rings concentric lanes (PIA08869, 331.50s)"},
        {"file_id": "021_v03f_span_336.50.mp4", "title": "NASA Cassini Inner B Ring Terminus fine ice lanes (PIA11671, 336.50s)"},
        {"file_id": "021_v03f_span_341.50.mp4", "title": "NASA Cassini Panoramic Rings natural-colour bands (PIA06175, 341.50s)"},
        {"file_id": "end_card_loop_pia01969.mp4", "title": "End-card loop: NASA Saturn and its Rings golden portrait (PIA01969, 360.15s)"},
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
        "file": str(FINAL), "version": "v01", "job": "J0653",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v03f",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": SPAN,
            "why_picture": "Frame 0 is real NASA Saturn and its Rings golden portrait (PIA01969 at 360.15 s of v03f), moving immediately with a 16% push. Cuts land across Cassini Saturn B Ring, Finer Than Ever (PIA21058 at 132.60 s) on 'that rain to know it was there', Cassini A-Ring Structures sunlit ring edge (PIA12727 at 167.50 s) on 'Astronomers on Earth, using the Keck telescope', Cassini So Far from Home Saturn and ring plane (PIA21345 at 310.10 s) under 'watched the glow of that water in Saturn's upper air' and the 9-14 s title, Cassini The Inner Rings (PIA08869 at 331.50 s) under 'and measured how fast the ice was leaving' and the 300M vs 100M yr scale bar, Cassini Inner B Ring Terminus (PIA11671 at 336.50 s) under 'At that magnetic rain rate alone', and Cassini Panoramic Rings (PIA06175 at 341.50 s) under 'the sheet would last about three hundred million years'; zero overlap with monday_saturn_tease, clock_100_300my, late_arrival_4_5b, lift_mimas_mass, and lift_ten_hour_day; skips chapter cards, burned captions, and Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening NASA Saturn and its Rings golden portrait (PIA01969 at 360.15 s)", "youtube_id": LONG_ID, **endt},
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
