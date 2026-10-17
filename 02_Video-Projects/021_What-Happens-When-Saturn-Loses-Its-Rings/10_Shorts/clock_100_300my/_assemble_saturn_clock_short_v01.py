#!/usr/bin/env python3
"""Saturn Short — "the clock" (J0186, backlog). No spend, no upload.

Lifts rows 110–113 of the live long 55AEQwvs36g (v03f, 516.17–536.30 s):
its own VO, picture and score bed. Reframed 9:16 (centre crop, ≤1.78×),
frame-0 hook caption, word captions, one 100–300 million year bar (3.6–8.0 s),
the long's exact title at 9–14 s, and an end card (title + id) over the opening
plate so the last seconds loop to frame 0. House SFX kit only.
"""
from __future__ import annotations

import hashlib
import json
import re
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
STEM = "saturn_clock_100_300my_v01"
FINAL = OUT / f"{STEM}.mp4"

T0 = 516.17          # picture cut to PIA17127; VO onset 516.22
VO_LEN = 20.13       # ends after "The rings are the clearest case."
END_LEN = 3.50
TOTAL = VO_LEN + END_LEN
WORDS_OFFSET = 515.90  # words.json times are relative to this
FPS = 30
W, H = 1080, 1920
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
BLACK = (0, 0, 0, 255)
LONG_TITLE = "How Long Do Saturn's Rings Have Left?"
LONG_ID = "55AEQwvs36g"
TITLE_ROWS = ["How Long Do", "Saturn's Rings", "Have Left?"]
HOOK = [("NOT ", WHITE), ("FOREVER", YELLOW)]
HOOK_END = 2.2
BAR_IN, BAR_OUT = 3.6, 8.0
TITLE_IN, TITLE_OUT = 9.0, 14.0


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
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def hook_png(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cap_h = H * 0.09
    f = font_for(cap_h / 0.72, 0.86)
    while sum(d.textlength(t, font=f) for t, _ in HOOK) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    widths = [d.textlength(t, font=f) for t, _ in HOOK]
    x = (W - sum(widths)) / 2
    y = 300
    for (t, c), w in zip(HOOK, widths):
        d.text((x, y), t, font=f, fill=c, stroke_width=7, stroke_fill=BLACK)
        x += w
    im.save(dest)
    return {"text": "".join(t for t, _ in HOOK), "font_px": f.size}


def caption_chunks() -> list[dict]:
    words = json.loads((WORK / "words.json").read_text())
    chunks, cur = [], []
    for w in words:
        t0 = w["s"] + WORDS_OFFSET - T0
        t1 = w["e"] + WORDS_OFFSET - T0
        if t0 >= VO_LEN - 0.05:
            break
        cur.append((w["w"], max(0.0, t0), t1))
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0][1]
        nxt = chunks[i + 1][0][1] if i + 1 < len(chunks) else VO_LEN
        end = min(nxt, c[-1][2] + 0.6)
        text = " ".join(x[0] for x in c).rstrip(",.")
        out.append({"text": text, "s": round(start, 2), "e": round(end, 2)})
    return out


def caption_png(dest: Path, text: str) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.95)
    centred(d, BAND_Y0 + BAND_H + 70, text.upper(), f, WHITE, stroke=6)
    im.save(dest)


def bar_frames(dest_dir: Path) -> dict:
    """100–300 million year bar; builds with the spoken numbers."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    f_lab = font_for(LINE_H)
    f_tick = font_for(LINE_H * 0.8)
    n = round((BAR_OUT - BAR_IN) * FPS)
    x0, x1 = 120, W - 120
    by = BAND_Y0 + BAND_H // 2 + 10
    bh = 34
    t100 = 5.16 + WORDS_OFFSET - T0  # "100" spoken
    t300 = 6.34 + WORDS_OFFSET - T0  # "300" spoken

    def xmy(my: float) -> float:
        return x0 + (x1 - x0) * my / 300.0

    for i in range(n):
        t = BAR_IN + i / FPS
        a = min(1.0, (t - BAR_IN) / 0.4, (BAR_OUT - t) / 0.4)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shade = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shade).rectangle((0, by - 230, W, by + 170), fill=int(120 * a))
        shade = shade.filter(ImageFilter.GaussianBlur(50))
        im.paste((0, 0, 0, 255), (0, 0), shade)
        d = ImageDraw.Draw(im)
        grow = min(1.0, max(0.0, (t - BAR_IN - 0.2) / 0.6))
        d.rounded_rectangle((x0, by, x0 + (x1 - x0) * grow, by + bh), radius=bh // 2,
                            fill=(255, 255, 255, int(70 * a)), outline=(255, 255, 255, int(220 * a)), width=3)
        if t >= t100:
            hi = 100 + 200 * min(1.0, max(0.0, (t - t100) / max(0.3, t300 + 0.4 - t100)))
            d.rounded_rectangle((xmy(100), by, xmy(hi), by + bh), radius=bh // 2, fill=(255, 214, 0, int(255 * a)))
        for my, label, show in ((100, "100", t >= t100), (300, "300", t >= t300)):
            if not show:
                continue
            x = xmy(my)
            d.line((x, by - 14, x, by + bh + 14), fill=(255, 255, 255, int(255 * a)), width=4)
            b = d.textbbox((0, 0), label, font=f_tick, stroke_width=4)
            tx = min(max(x - (b[2] - b[0]) / 2, 20), W - 20 - (b[2] - b[0]))
            d.text((tx, by + bh + 24), label, font=f_tick, fill=(255, 255, 255, int(255 * a)),
                   stroke_width=4, stroke_fill=(0, 0, 0, int(255 * a)))
        lab = "MILLION YEARS"
        b = d.textbbox((0, 0), lab, font=f_lab, stroke_width=5)
        d.text(((W - (b[2] - b[0])) // 2, by - 30 - (b[3] - b[1]) - 20), lab, font=f_lab,
               fill=(255, 255, 255, int(255 * a)), stroke_width=5, stroke_fill=(0, 0, 0, int(255 * a)))
        im.save(dest_dir / f"bar_{i:04d}.png")
    return {"in": BAR_IN, "out": BAR_OUT, "labels": ["MILLION YEARS", "100", "300"], "t100": round(t100, 2),
            "t300": round(t300, 2), "band": [BAND_Y0, BAND_Y0 + BAND_H]}


def title_png(dest: Path, with_id: bool) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    rows = [(r, WHITE) for r in TITLE_ROWS] + ([(LONG_ID, YELLOW)] if with_id else [])
    gap = LINE_H + 8
    y = BAND_Y0 + (BAND_H - gap * len(rows)) // 2
    placed = []
    for r, c in rows:
        bb = centred(d, y, r, f, c)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"text outside 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed}


def end_plate(dest: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{T0 + 0.02:.3f}", "-i", PICTURE, "-frames:v", "1",
         "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos", WORK / "plate0.png"])
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(16)), 0.65)
    im = ImageEnhance.Brightness(im).enhance(0.82)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse((80, BAND_Y0 - 20, W - 80, BAND_Y0 + BAND_H + 20), fill=95)
    shade = shade.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.75)
    d = ImageDraw.Draw(im)
    rows = [("RINGS ON", WHITE), ("A CLOCK", YELLOW)]
    size = 60
    while True:
        f = ImageFont.truetype(FONT, size + 2)
        if max(d.textlength(r, font=f) for r, _ in rows) > W * 0.80:
            break
        size += 2
    f = ImageFont.truetype(FONT, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 20
    y = (H - lh * len(rows)) // 2
    for r, c in rows:
        centred(d, y, r, f, c, stroke=9)
        y += lh
    im.save(dest, quality=92)


def audio() -> dict:
    vo = WORK / "stem_vo.wav"
    bed = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{T0:.3f}", "-t", f"{VO_LEN:.3f}", "-i", VO,
         "-af", f"afade=t=out:st={VO_LEN - 0.08:.3f}:d=0.08,apad=whole_dur={TOTAL:.3f}", "-ar", "48000", "-ac", "2", vo])
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{T0:.3f}", "-t", f"{TOTAL:.3f}", "-i", BED,
         "-af", f"afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.5:.3f}:d=0.5", "-ar", "48000", "-ac", "2", bed])
    vo_i, bed_i = lufs(vo), lufs(bed)
    bed_gain = (vo_i - 17.0) - bed_i
    bed_l = WORK / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", bed, "-af", f"volume={bed_gain:.2f}dB", bed_l])
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    t100 = 5.16 + WORDS_OFFSET - T0
    t300 = 6.34 + WORDS_OFFSET - T0
    hits = [(whoosh, 0.0), (tick, BAR_IN + 0.05), (tick, t100), (tick, t300), (tick, TITLE_IN)]
    sfx_raw = WORK / "stem_sfx_raw.wav"
    inputs, parts = [], []
    for i, (f, at) in enumerate(hits):
        inputs += ["-i", f]
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(hits)))
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(parts) + f";{mix}amix=inputs={len(hits)}:normalize=0,apad=whole_dur={TOTAL:.3f}[o]",
         "-map", "[o]", "-t", f"{TOTAL:.3f}", sfx_raw])
    sfx_gain = (vo_i - 15.0) - lufs(sfx_raw)
    sfx = WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", sfx_raw, "-af", f"volume={sfx_gain:.2f}dB", sfx])
    mixed = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-i", bed_l, "-i", sfx, "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", "48000", "-t", f"{TOTAL:.3f}", mixed])
    return {"vo_lufs": vo_i, "bed_gain_db": round(bed_gain, 2), "sfx_gain_db": round(sfx_gain, 2),
            "sfx_hits": [[Path(f).name, round(a, 2)] for f, a in hits], "mix_lufs": lufs(mixed),
            "stems": {"vo": str(vo), "bed": str(bed_l), "sfx": str(sfx)}}


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    hook = hook_png(WORK / "hook.png")
    caps = caption_chunks()
    for i, c in enumerate(caps):
        caption_png(WORK / f"cap_{i:02d}.png", c["text"])
    bar = bar_frames(WORK / "bar")
    title = title_png(WORK / "title.png", with_id=False)
    endt = title_png(WORK / "end_text.png", with_id=True)
    end_plate(WORK / "end_bg.png")
    cover(OUT / f"{STEM}_cover.jpg")
    aud = audio()

    inputs = ["-ss", f"{T0:.3f}", "-t", f"{VO_LEN:.3f}", "-i", PICTURE,
              "-loop", "1", "-framerate", FPS, "-t", TOTAL, "-i", WORK / "end_bg.png",
              "-loop", "1", "-framerate", FPS, "-t", TOTAL, "-i", WORK / "hook.png",
              "-framerate", FPS, "-i", WORK / "bar" / "bar_%04d.png",
              "-loop", "1", "-framerate", FPS, "-t", TOTAL, "-i", WORK / "title.png",
              "-loop", "1", "-framerate", FPS, "-t", TOTAL, "-i", WORK / "end_text.png",
              "-i", WORK / "mix.wav"]
    base = 7
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", FPS, "-t", TOTAL, "-i", WORK / f"cap_{i:02d}.png"]
    end_frames = round(END_LEN * FPS) + 2
    fc = [
        f"[0:v]fps={FPS},crop=ih*9/16:ih,scale={W}:{H}:flags=lanczos,eq=brightness=0.02:gamma=1.12:enable='gte(t,10.4)',setsar=1,format=yuv420p[a]",
        f"[1:v]scale={W*2}:{H*2},zoompan=z='1.03-0.03*on/{end_frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS},trim=0:{END_LEN:.3f},setpts=PTS-STARTPTS,format=yuv420p[e]",
        "[e][5:v]overlay=0:0:shortest=1,format=yuv420p[ecard]",
        "[a][ecard]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={HOOK_END - 0.3:.2f}:d=0.3:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[3:v]setpts=PTS-STARTPTS+{BAR_IN}/TB[br]",
        "[v1][br]overlay=0:0:eof_action=pass[v2]",
        f"[4:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.3:alpha=1,fade=t=out:st={TITLE_OUT - 0.3}:d=0.3:alpha=1[tt]",
        f"[v2][tt]overlay=0:0:enable='between(t,{TITLE_IN},{TITLE_OUT})'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='between(t,{c['s']},{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]noise=alls=4:allf=t,format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "6:a", *enc, "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", FINAL])

    meta = {
        "file": str(FINAL), "version": "v01", "job": "J0186", "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {"id": LONG_ID, "title": LONG_TITLE, "cut": "v03f", "rows": "110-113",
                 "source_s": [T0, round(T0 + VO_LEN, 2)], "upscale": 1080 / 607.5},
        "hook": hook, "captions": caps, "overlay_scale_bar": bar,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening plate (loop)", **endt},
        "audio": aud, "grain": "noise=alls=4:allf=t", "cover": str(OUT / f"{STEM}_cover.jpg"),
        "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in ("file", "duration_s", "audio")}, indent=2))


if __name__ == "__main__":
    main()
