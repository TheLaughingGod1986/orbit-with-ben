#!/usr/bin/env python3
"""023 Short v02 — Venus is 95% as wide as Earth (J0838, Chief FIX on J0824). No spend, no upload.

v02 keeps v01's open, VO, captions, bar, title, end card, SFX and cover. Two picture fixes:
s04's v05e in-point moves 221.20 -> 221.00 so the 2.90 s span ends at 223.90, before the
long's dissolve (ghost from 224.00). s05's in-point moves 338.55 -> 338.87, past the baked
'Alpha Regio' lower-third (last faint frame 338.80; clean from 338.83). Timeline in/outs stay.
Caption, hook, title and card overlays use gte(t,s)*lt(t,e) so a boundary frame shows one layer.
The same inclusive between() is still in the other 023 lift assemblers (lift_90x_air at ~0.70 s):
backlog, not rebuilt here.


023 is the earliest locked/scheduled OWB long (023_Venus_full_rough_v05e.mp4, VBaYRPp85Sw) tied for the fewest
Shorts built (4: lift_two_hours, lift_heavy_water, lift_90x_air, lift_less_sunlight). 028/029 have none and no master.
Lifts its own VO and picture from "Venus is ninety-five percent as wide as Earth..." through
"...It is also closer to the sun." (55 words, 22.22 s VO + 2.28 s end card = 24.50 s total).
Frame 0 is the full-disk cloudy Venus globe (PIA23791.jpg at 24.62 s of v05e), already mid-move, with a 16%
first-second push and a 95% / AS WIDE hook caption. No chapter card, no Orbit, no subscribe cue.
Exact long title ("What Happened to Venus?") at 9-14 s inside the 16:9 centre band.
One animated number bar (FOUR-FIFTHS MASS, stroke text only, bar grows to four-fifths, no dark box)
at 4.30-6.85 s while "four-fifths of its mass" is spoken, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with the exact long title and YouTube ID (VBaYRPp85Sw) on the opening cloudy Venus plate so the
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

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

PICTURE = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-13/loose_renders/023_Venus_full_rough_v05e.mp4")
VO = FILM / "02_Voiceover/venus_vo_v01.mp3"
BED = FILM / "05_Music/venus_score_bed_v01_full.mp3"
WORDS = FILM / "07_Edit-Project/full_rough_v05e_pack/venus_words_list.json"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v02"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/venus_95pct_wide_v02")
STEM = "venus_95pct_wide_v02"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 46.90       # "Venus is ninety-five percent..." (word starts 46.98)
VO_LEN = 22.22      # through "sun." (word ends 69.04; next word at 69.98)
END_LEN = 2.28
TOTAL = round(VO_LEN + END_LEN, 2)  # 24.50 s
FPS = 30
W, H = 1080, 1920
PUSH = 0.16
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
LONG_TITLE = "What Happened to Venus?"
LONG_ID = "VBaYRPp85Sw"
TITLE_ROWS = ["What Happened", "to Venus?"]
END_ROWS = [("What Happened", WHITE), ("to Venus?", WHITE), (LONG_ID, YELLOW)]
HOOK_ROWS = [("95%", YELLOW), ("AS WIDE", WHITE)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 4.30, 6.85
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-11-02"  # Follow-on slot after Chief PASS: Mon 2 Nov 11:30 London. Not uploaded here.

# Picture from v05e. No overlap with the four built 023 lifts. No chapter card, subscribe cue, Orbit, or labelled graphic.
SPAN = [
    (24.62, 4.90),   # 0.00-4.90   full-disk cloudy Venus (PIA23791.jpg), frame 0, "ninety-five percent as wide"
    (35.68, 3.80),   # 4.90-8.70   Magellan radar global view (PIA00257.jpg) under the four-fifths bar
    (207.82, 4.30),  # 8.70-13.00  Magellan volcanic terrain (PIA00200.jpg) under "same kind of rock"
    (221.00, 2.90),  # 13.00-15.90 full-disk Venus globe (S91-50688.jpg); ends 223.90, before dissolve at 224.00
    (338.87, 3.80),  # 15.90-19.70 Magellan ridged highlands (PIA00109.jpg); in after Alpha Regio card (clean from 338.83)
    (67.40, 2.52),   # 19.70-22.22 SDO Venus transit of the Sun (AIA171) under "closer to the sun"
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
    p = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    m = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", p.stderr)
    return float(m[-1])


def font_for(px: float, max_w_frac: float = 0.88) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, max(24, round(px)))


def centred(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont,
            fill: tuple, stroke: int = 6) -> list[int]:
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
    raw = json.loads(WORDS.read_text())
    src = raw["words"] if isinstance(raw, dict) and "words" in raw else raw
    out = []
    for w in src:
        if w["start"] >= VO_T0 + VO_LEN - 0.05:
            break
        if w["end"] <= VO_T0 + 0.01:
            continue
        out.append({
            "w": w["text"],
            "s": round(max(0.0, w["start"] - VO_T0), 3),
            "e": round(w["end"] - VO_T0, 3),
        })
    (WORK / "words.json").write_text(json.dumps(out, indent=2) + "\n")
    return out


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


# One number: four-fifths of Earth's mass. Two words on the label. Bar grows to 80%. No dark plate.
SCALE = [
    ("FOUR-FIFTHS", "MASS", 80, YELLOW),
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
        "values_c": [80],
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
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
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
    im = ImageEnhance.Brightness(im).enhance(0.84)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.78)
    d = ImageDraw.Draw(im)
    rows = [("95%", YELLOW), ("AS WIDE", WHITE)]
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


def cut_strip(video: Path, dest: Path) -> None:
    """Full frame rate, +/-0.2 s, around every timeline cut. One row per cut."""
    bounds = [0.0]
    t = 0.0
    for _, length in SPAN:
        t = round(t + length, 2)
        bounds.append(t)
    if bounds[-1] != TOTAL:
        bounds.append(TOTAL)
    rows = []
    for b in bounds:
        start = max(0.0, round(b - 0.2, 3))
        length = min(0.4, round(TOTAL - start, 3))
        tile = WORK / f"cutrow_{b:.2f}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", str(video),
             "-vf", f"fps={FPS},scale=120:214,tile=12x1", "-frames:v", "1", str(tile)])
        rows.append((tile, b, start))
    im0 = Image.open(rows[0][0])
    w, h = im0.size
    canvas = Image.new("RGB", (w, (h + 18) * len(rows)), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (tile, b, start) in enumerate(rows):
        y = i * (h + 18)
        canvas.paste(Image.open(tile), (0, y))
        d.text((6, y + h + 2), f"cut {b:.2f}s  frames from {start:.2f}s", fill=(255, 220, 0))
    canvas.save(dest, quality=90)


def contact_sheet(video: Path, dest: Path) -> None:
    times = [0.0, 0.5, 1.6, 4.6, 8.0, 11.0, 14.5, 18.0, 21.5, TOTAL - 0.4]
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
         "-af", f"afade=t=in:st=0:d=0.25,afade=t=out:st={TOTAL - 0.35:.3f}:d=0.35",
         "-ar", "48000", "-ac", "2", str(bed)])
    vo_i = lufs(vo)
    bed_i = lufs(bed)
    bed_gain = (vo_i - 25.5) - bed_i
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

    zoom = f"1+{PUSH}*clip(1-t,0,1)"
    fc = [
        f"[0:v]fps={FPS},crop=ih*9/16:ih,scale='trunc(1080*({zoom})/2)*2':'trunc(1920*({zoom})/2)*2':eval=frame,"
        f"crop=1080:1920,setsar=1,format=yuv420p[a]",
        f"[1:v]fps={FPS},trim=0:{END_LEN:.3f},setpts=PTS-STARTPTS,"
        f"scale='trunc(1080*(1+0.05*t/{END_LEN:.3f})/2)*2':'trunc(1920*(1+0.05*t/{END_LEN:.3f})/2)*2':eval=frame,"
        f"crop=1080:1920,setsar=1[ebg]",
        f"[5:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={END_LEN - 0.35:.2f}:d=0.35:alpha=1[et]",
        "[ebg][et]overlay=0:0:shortest=1,format=yuv420p[ecard]",
        "[a][ecard]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={HOOK_END - 0.3:.2f}:d=0.3:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[3:v]setpts=PTS-STARTPTS+{CARD_IN}/TB[cd]",
        f"[v1][cd]overlay=0:0:enable='gte(t,{CARD_IN})*lt(t,{CARD_OUT})':eof_action=pass[v2]",
        f"[4:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.3:alpha=1,fade=t=out:st={TITLE_OUT - 0.3}:d=0.3:alpha=1[tt]",
        f"[v2][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "6:a", *enc, "-t", f"{TOTAL:.3f}", FINAL])

    contact_path = OUT / f"{STEM}_contact.jpg"
    contact_sheet(FINAL, contact_path)
    strip_path = OUT / f"{STEM}_cut_strip.jpg"
    cut_strip(FINAL, strip_path)
    thumb_sheet = OUT / f"{STEM}_cover_preview.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
         "short", str(cover_path), "--out", str(thumb_sheet)])

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--sheet-dir", str(OUT), "--json"],
        capture_output=True, text=True,
    )
    (OUT / f"{STEM}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--sheet-dir", str(OUT)],
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
        {"row": "s01_cloudy_venus", "timeline_in": 0.0, "timeline_out": 4.90, "source": "PIA23791.jpg", "upscale": 1.78, "framing": {"offset": 24.62}, "video": True},
        {"row": "s02_radar_globe", "timeline_in": 4.90, "timeline_out": 8.70, "source": "PIA00257.jpg", "upscale": 1.78, "framing": {"offset": 35.68}, "video": True},
        {"row": "s03_volcanic_terrain", "timeline_in": 8.70, "timeline_out": 13.00, "source": "PIA00200.jpg", "upscale": 1.78, "framing": {"offset": 207.82}, "video": True},
        {"row": "s04_full_globe", "timeline_in": 13.00, "timeline_out": 15.90, "source": "S91-50688.jpg", "upscale": 1.78, "framing": {"offset": 221.00}, "video": True},
        {"row": "s05_ridged_highlands", "timeline_in": 15.90, "timeline_out": 19.70, "source": "PIA00109.jpg", "upscale": 1.78, "framing": {"offset": 338.87}, "video": True},
        {"row": "s06_venus_transit", "timeline_in": 19.70, "timeline_out": 22.22, "source": "AIA171VenusTransit_HD1080.mp4", "upscale": 1.78, "framing": {"offset": 67.40}, "video": True},
        {"row": "s07_end_loop", "timeline_in": 22.22, "timeline_out": 24.50, "source": "end_card_loop_PIA23791.mp4", "upscale": 1.78, "framing": {"offset": 24.62}, "video": True},
    ]
    pool = [
        {"file_id": "PIA23791.jpg", "title": "NASA full-disk cloudy Venus globe (24.62s)"},
        {"file_id": "PIA00257.jpg", "title": "NASA Magellan radar global view of Venus (35.68s)"},
        {"file_id": "PIA00200.jpg", "title": "NASA Magellan volcanic terrain on Venus (207.82s)"},
        {"file_id": "S91-50688.jpg", "title": "NASA Magellan full-disk Venus globe (221.00s)"},
        {"file_id": "PIA00109.jpg", "title": "NASA Magellan ridged highlands on Venus (338.87s)"},
        {"file_id": "AIA171VenusTransit_HD1080.mp4", "title": "NASA SDO AIA 171 Venus transit of the Sun (67.40s)"},
        {"file_id": "end_card_loop_PIA23791.mp4", "title": "End-card loop: NASA full-disk cloudy Venus globe (24.62s)"},
    ]
    (OUT / "cuts_v02.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / "pool_v02.json").write_text(json.dumps(pool, indent=2) + "\n")

    pg_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v02.json"),
         "--out", str(OUT / "polish_gate_v02.json"), "--no-jitter"],
        capture_output=True, text=True,
    )
    (OUT / "polish_gate_v02.txt").write_text((pg_chk.stdout or "") + (pg_chk.stderr or ""))

    pqa_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v02.json"),
         "--pool", str(OUT / "pool_v02.json"),
         "--out-dir", str(OUT / "picture_qa_v02")],
        capture_output=True, text=True,
    )
    (OUT / "picture_qa_v02.txt").write_text((pqa_chk.stdout or "") + (pqa_chk.stderr or ""))

    UAT.mkdir(parents=True, exist_ok=True)
    for p in (FINAL, contact_path, strip_path, cover_path, thumb_sheet,
              OUT / f"{STEM}_gate.json", OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt",
              OUT / f"{STEM}_open_sheet.jpg",
              OUT / "cuts_v02.json", OUT / "pool_v02.json",
              OUT / "polish_gate_v02.json", OUT / "polish_gate_v02.txt", OUT / "picture_qa_v02.txt"):
        if p.exists():
            shutil.copy2(p, UAT / p.name)
    if (OUT / "picture_qa_v02").exists():
        shutil.copytree(OUT / "picture_qa_v02", UAT / "picture_qa_v02", dirs_exist_ok=True)

    meta = {
        "file": str(FINAL), "version": "v02", "job": "J0838",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": LONG_ID, "title": LONG_TITLE, "cut": "v05e",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": SPAN,
            "why_picture": "Frame 0 is the full-disk cloudy Venus globe (PIA23791.jpg at 24.62 s of v05e), already moving, plus a 16% first-second push. Later cuts: Magellan radar globe (35.68 s) under the four-fifths bar, Magellan volcanic terrain (207.82 s) under same rock, Magellan full-disk globe (221.00 s, ended before the 224.00 dissolve) and ridged highlands (338.87 s, after the Alpha Regio card) under second Earth, SDO Venus transit (67.40 s) only under closer to the sun. No overlap with the four built 023 lifts. No chapter card, subscribe cue, labelled graphic, or Orbit.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening full-disk cloudy Venus globe (24.62 s)", "youtube_id": LONG_ID, **endt},
        "audio": aud, "sfx_level_check": (sfx_chk.stdout or sfx_chk.stderr).strip(),
        "sfx_level_ok": sfx_chk.returncode == 0,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "polish_gate_ok": pg_chk.returncode == 0,
        "picture_qa_ok": pqa_chk.returncode == 0,
        "cover": str(cover_path), "cover_preview": str(thumb_sheet),
        "contact_sheet": str(contact_path), "cut_strip": str(strip_path),
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
