#!/usr/bin/env python3
"""027 Short v01 — If Earth Stopped Spinning, One Day Would Last a Year (J0532, backlog). No spend, no upload.

027 is the locked OWB long (027_EarthSpin_rough_v01i.mp4 / v01l, "What If Earth Stopped Spinning?") with the fewest
Shorts built among locked/live longs (2: lift_40000_years and lift_sudden_air vs 4 on 021/022 and 6 on 023/024/025/026).
Lifts its own VO and picture from "With no spin at all, the sun would cross the sky just once as Earth went round it..."
through "...and the night side would freeze in the dark, with the wind always pouring from one side to the other."
(65 words, 22.90 s VO + 3.10 s end card = 26.00 s total).
Frame 0 is real daylight Earth from space (DSCOVR EPIC full-disk sunlit rotating Earth at 439.60 s of the locked cut),
moving immediately with a 16% first-second push, with EARTH DAY / 1 YEAR LONG hook caption.
Exact long title ("What If Earth Stopped Spinning?") at 9-14 s inside the 16:9 centre band.
One animated 2-bar day/night split scale (DAY SIDE 6 MONTHS vs NIGHT SIDE 6 MONTHS, stroke text only, growing bars
from a shared left edge, no dark box) at 14.30-18.10 s, clear of 0-2 s and 9-14 s, inside the 16:9 centre band.
End card with exact long title on the opening Earth plate so the last seconds loop back to frame 0 (027 has no YouTube ID yet).
House SFX kit only.
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

PICTURE = FILM / "07_Edit-Project/027_EarthSpin_rough_v01i.mp4"
VO = FILM / "02_Voiceover/earth_spin_vo_v02order.wav"
BED = FILM / "05_Music/earth-spin_score_take2_straight_v01j.wav"
WORDS = FILM / "07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v01"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/earth_day_one_year_v01")
STEM = "earth_day_one_year_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 206.68      # "With no spin at all..."
VO_LEN = 22.90      # through "...from one side to the other." (word ends 229.54; next word at 231.24)
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
LONG_TITLE = "What If Earth Stopped Spinning?"
TITLE_ROWS = ["What If Earth", "Stopped Spinning?"]
END_ROWS = [("What If Earth", WHITE), ("Stopped Spinning?", YELLOW)]
HOOK_ROWS = [("EARTH DAY", WHITE), ("1 YEAR LONG", YELLOW)]
HOOK_END = 2.2
CARD_IN, CARD_OUT = 14.30, 18.10
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-11-27"  # Provisional 027 week slot

# Picture from locked cut: 6 clean moving spans (3.00-5.50 s each), every cut snapped inside a 0.42-1.06 s VO pause,
# zero overlap with lift_40000_years and lift_sudden_air, no Orbit, no chapter cards, no code graphics.
SPAN = [
    (439.60, 5.50),  # 0.00-5.50   DSCOVR EPIC full-disk sunlit rotating Earth (ends in 5.22-6.18 pause)
    (13.45, 3.20),   # 5.50-8.70   ISS orbital Earth sunrise & limb (ends in 8.20-8.92 pause)
    (104.30, 4.20),  # 8.70-12.90  ISS Gerst Earth day-to-night orbital timelapse (ends in 12.04-13.10 pause)
    (120.50, 3.50),  # 12.90-16.40 ESO La Silla bright desert sky timelapse (ends in 16.18-16.68 pause)
    (421.20, 3.00),  # 16.40-19.40 ESO La Silla night dome & starlight timelapse (ends in 19.06-19.48 pause)
    (226.05, 3.50),  # 19.40-22.90 ISS Gerst terminator & clouds timelapse from row 21 (through 22.86 end)
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
    src = json.loads(WORDS.read_text())
    out = []
    for w in src:
        if w["start"] >= VO_T0 + VO_LEN - 0.02:
            break
        if w["end"] <= VO_T0 - 0.02:
            continue
        out.append({
            "w": w["text"],
            "s": round(max(0.0, w["start"] - VO_T0), 3),
            "e": round(min(VO_LEN, w["end"] - VO_T0), 3),
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


# One animated 2-row scale comparison. Each label is 4 words or fewer. No dark plate.
SCALE = [
    ("DAY SIDE", "6 MONTHS", 6, YELLOW),
    ("NIGHT SIDE", "6 MONTHS", 6, WHITE),
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
            delay = r * 0.22
            prog = min(1.0, max(0.0, (t - CARD_IN - delay) / 0.55))
            y = y0 + r * row_h
            label = f"{name}  {num}"
            fill = (colour[0], colour[1], colour[2], alpha)
            bb = centred(d, y, label, f, fill, stroke=6)
            if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
                raise SystemExit(f"scale text outside 16:9 band: {label} {bb}")
            full = int(W * 0.64)
            left = (W - full) // 2
            bar_w = int(full * (value / 6) * prog)
            if bar_w > 4:
                by = bb[3] + 8
                bar_col = (255, 214, 0, alpha) if r == 0 else (255, 255, 255, alpha)
                d.rectangle((left, by, left + bar_w, by + 16), fill=bar_col)
                if by + 16 > BAND_Y0 + BAND_H:
                    raise SystemExit(f"scale bar outside 16:9 band: {by}")
            if i == n // 2 and r == 0:
                sample_bb = bb
        im.save(dest_dir / f"card_{i:04d}.png")
    return {
        "in": CARD_IN, "out": CARD_OUT,
        "labels": labels,
        "values_months": [6, 6],
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


def end_text_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    while max(d.textlength(r, font=f) for r, _ in END_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - gap * len(END_ROWS)) // 2
    placed = []
    for r, col in END_ROWS:
        bb = centred(d, y, r, f, col, stroke=6)
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
    im = ImageEnhance.Brightness(im).enhance(0.75)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, BAND_Y0 - 40, W, BAND_Y0 + BAND_H + 40), fill=100)
    shade = shade.filter(ImageFilter.GaussianBlur(50))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.80)
    d = ImageDraw.Draw(im)
    rows = [("1 DAY =", WHITE), ("1 YEAR", YELLOW)]
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
    times = [0.0, 0.6, 1.8, 6.0, 9.6, 12.0, 15.2, 17.5, 21.0, TOTAL - 0.5]
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
    endt = end_text_png(WORK / "end_text.png")
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
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
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
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
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

    UAT.mkdir(parents=True, exist_ok=True)
    for p in (FINAL, contact_path, cover_path, thumb_sheet,
              OUT / f"{STEM}_gate.json", OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt"):
        if p.exists():
            shutil.copy2(p, UAT / p.name)

    meta = {
        "file": str(FINAL), "version": "v01", "job": "J0532",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {
            "id": None, "title": LONG_TITLE, "cut": "v01i",
            "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
            "picture_spans": SPAN,
            "why_picture": "Frame 0 is DSCOVR EPIC full-disk sunlit rotating Earth from space. All 6 spans are clean real moving footage with cuts snapped to VO pauses and zero overlap with lift_40000_years and lift_sudden_air.",
        },
        "words": len(words),
        "hook": hook, "captions": caps, "overlay": card,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening DSCOVR EPIC sunlit Earth plate", "youtube_id": None, **endt},
        "audio": aud, "sfx_level_check": (sfx_chk.stdout or sfx_chk.stderr).strip(),
        "sfx_level_ok": sfx_chk.returncode == 0,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "cover": str(cover_path), "cover_preview": str(thumb_sheet), "contact_sheet": str(contact_path),
        "uat_dir": str(UAT), "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(OUT / f"{STEM}_meta.json", UAT / f"{STEM}_meta.json")
    print(gate_txt.stdout or gate_txt.stderr)
    print("--- sfx", sfx_chk.returncode)
    print(sfx_chk.stdout or sfx_chk.stderr)
    print(json.dumps({k: meta[k] for k in ("file", "duration_s", "words", "gate_ok", "sfx_level_ok", "audio")}, indent=2))
    if gate.returncode != 0 or sfx_chk.returncode != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
