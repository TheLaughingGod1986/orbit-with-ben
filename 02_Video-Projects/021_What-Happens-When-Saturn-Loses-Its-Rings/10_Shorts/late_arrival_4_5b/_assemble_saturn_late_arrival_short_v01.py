#!/usr/bin/env python3
"""Saturn Short — "late arrival / 4.5 billion years" (J0253, backlog). No spend, no upload.

Lifts rows 82–85 of the live long 55AEQwvs36g (v03f, VO 380.10–401.60 s, picture 383.20–404.70 s):
its own VO, picture and score bed. Reframed 9:16 (centre crop, 1.78×),
frame-0 hook caption ("YOUNGER THAN SATURN?"), word captions, one 4.5-billion-year scale bar (3.6–8.0 s),
the long's exact title at 9–14 s, and an end card (title + id) over the opening
plate so the last seconds loop to frame 0. House SFX kit only.
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
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_late_arrival_4_5b_v01")
STEM = "saturn_late_arrival_4_5b_v01"
FINAL = OUT / f"{STEM}.mp4"

VO_T0 = 380.10       # "The rings look like a late arrival."
PIC_T0 = 383.20      # clean cut to PIA11141 (Saturn + bright concentric rings across golden disc)
VO_LEN = 21.50       # ends after "a few hundred million years at most."
END_LEN = 3.50
TOTAL = VO_LEN + END_LEN  # 25.00 s (inside 22–27 s lock)
FPS = 30
W, H = 1080, 1920
PUSH = 0.12          # smooth 12% push over first 1.0 s so frame 0–1 s has clear motion (>= 10)
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
HOOK_ROWS = [("YOUNGER THAN", WHITE), ("SATURN?", YELLOW)]
HOOK_END = 2.2
BAR_IN, BAR_OUT = 3.6, 8.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
AIR_DATE = "2026-10-26"


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


def caption_chunks() -> list[dict]:
    words = json.loads((WORK / "words.json").read_text())
    chunks, cur = [], []
    for w in words:
        t0 = float(w["s"])
        t1 = float(w["e"])
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
    """4.5 billion year Saturn age scale bar; builds with the spoken numbers (3.6–8.0 s)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    f_lab = font_for(LINE_H)
    f_tick = font_for(LINE_H * 0.82)
    n = round((BAR_OUT - BAR_IN) * FPS)
    x0, x1 = 180, W - 180
    by = BAND_Y0 + BAND_H // 2 + 10
    bh = 34
    t_saturn = 4.22  # "Saturn" spoken
    t_45b = 5.54     # "four and a half billion" spoken

    for i in range(n):
        t = BAR_IN + i / FPS
        a = min(1.0, (t - BAR_IN) / 0.4, (BAR_OUT - t) / 0.4)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shade = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shade).rectangle((0, by - 250, W, by + 180), fill=int(155 * a))
        shade = shade.filter(ImageFilter.GaussianBlur(55))
        im.paste((0, 0, 0, 255), (0, 0), shade)
        bar_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        db = ImageDraw.Draw(bar_layer)
        grow = min(1.0, max(0.0, (t - BAR_IN - 0.2) / 0.6))
        db.rounded_rectangle((x0, by, x0 + (x1 - x0) * grow, by + bh), radius=bh // 2,
                             fill=(255, 255, 255, int(70 * a)), outline=(255, 255, 255, int(220 * a)), width=3)
        if t >= t_saturn:
            fill_prog = min(1.0, max(0.05, (t - t_saturn) / max(0.3, (t_45b + 1.1) - t_saturn)))
            db.rounded_rectangle((x0, by, x0 + (x1 - x0) * fill_prog, by + bh), radius=bh // 2,
                                 fill=(255, 214, 0, int(255 * a)))
        bar_layer = bar_layer.filter(ImageFilter.GaussianBlur(8.0))
        im = Image.alpha_composite(im, bar_layer)
        d = ImageDraw.Draw(im)
        if t >= t_45b:
            label = "4.5 BILLION YRS"
            b = d.textbbox((0, 0), label, font=f_tick, stroke_width=4)
            tx = (W - (b[2] - b[0])) // 2
            d.text((tx, by + bh + 24), label, font=f_tick, fill=(255, 214, 0, int(255 * a)),
                   stroke_width=4, stroke_fill=(0, 0, 0, int(255 * a)))
        lab = "SATURN'S AGE"
        b = d.textbbox((0, 0), lab, font=f_lab, stroke_width=5)
        d.text(((W - (b[2] - b[0])) // 2, by - 30 - (b[3] - b[1]) - 20), lab, font=f_lab,
               fill=(255, 255, 255, int(255 * a)), stroke_width=5, stroke_fill=(0, 0, 0, int(255 * a)))
        im.save(dest_dir / f"bar_{i:04d}.png")
    return {
        "in": BAR_IN,
        "out": BAR_OUT,
        "labels": ["SATURN'S AGE", "4.5 BILLION YRS"],
        "t_saturn": t_saturn,
        "t_45b": t_45b,
        "band": [BAND_Y0, BAND_Y0 + BAND_H],
    }


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
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{PIC_T0 + 0.02:.3f}", "-i", PICTURE, "-frames:v", "1",
         "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos", WORK / "plate0.png"])
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.7)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle((0, BAND_Y0 - 40, W, BAND_Y0 + BAND_H + 40), fill=100)
    shade = shade.filter(ImageFilter.GaussianBlur(60))
    im = Image.composite(Image.new("RGB", (W, H)), im, shade)
    im.save(dest)


def cover(dest: Path) -> None:
    im = Image.open(WORK / "plate0.png").convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.75)
    d = ImageDraw.Draw(im)
    rows = [("YOUNGER THAN", WHITE), ("SATURN?", YELLOW)]
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


def contact_sheet(video: Path, dest: Path) -> None:
    times = [0.0, 0.3, 1.0, 2.5, 5.8, 7.2, 11.0, 16.0, 20.0, TOTAL - 0.5]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
             "-vf", "scale=216:384", p])
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
         "-af", f"afade=t=out:st={VO_LEN - 0.08:.3f}:d=0.08,apad=whole_dur={TOTAL:.3f}", "-ar", "48000", "-ac", "2", vo])
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{VO_T0:.3f}", "-t", f"{TOTAL:.3f}", "-i", BED,
         "-af", f"afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.5:.3f}:d=0.5", "-ar", "48000", "-ac", "2", bed])
    vo_i, bed_i = lufs(vo), lufs(bed)
    bed_gain = (vo_i - 22.0) - bed_i
    bed_l = WORK / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", bed, "-af", f"volume={bed_gain:.2f}dB", bed_l])
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    hits = [(whoosh, 0.0), (tick, BAR_IN + 0.05), (tick, 4.22), (tick, 5.54), (tick, TITLE_IN)]
    sfx_raw = WORK / "stem_sfx_raw.wav"
    inputs, parts = [], []
    for i, (f, at) in enumerate(hits):
        inputs += ["-i", f]
        parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(hits)))
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(parts) + f";{mix}amix=inputs={len(hits)}:normalize=0,apad=whole_dur={TOTAL:.3f}[o]",
         "-map", "[o]", "-t", f"{TOTAL:.3f}", sfx_raw])
    sfx_gain = (vo_i - 23.0) - lufs(sfx_raw)
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
    cover_path = OUT / f"{STEM}_cover.jpg"
    cover(cover_path)
    aud = audio()

    inputs = ["-ss", f"{PIC_T0:.3f}", "-t", f"{VO_LEN:.3f}", "-i", PICTURE,
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
        f"[0:v]fps={FPS},crop=ih*9/16:ih,"
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:0:'if(gte(t,19.7),120,0)',setsar=1,format=yuv420p[a]",
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

    contact_path = OUT / f"{STEM}_contact.jpg"
    contact_sheet(FINAL, contact_path)

    thumb_sheet = OUT / f"{STEM}_cover_preview.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
         "short", str(cover_path), "--out", str(thumb_sheet)])

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--id", "82Ao0v5XiQI", "--json"],
        capture_output=True, text=True, check=True,
    )
    (OUT / f"{STEM}_gate.json").write_text(gate.stdout)

    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--id", "82Ao0v5XiQI"],
        capture_output=True, text=True, check=True,
    )
    (OUT / f"{STEM}_gate.txt").write_text(gate_txt.stdout)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(WORK / "stem_vo.wav"),
         "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"),
         "--minutes", f"{TOTAL / 60.0:.3f}"],
        capture_output=True, text=True, check=True,
    )

    meta = {
        "file": str(FINAL), "version": "v01", "job": "J0253", "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "long": {"id": LONG_ID, "title": LONG_TITLE, "cut": "v03f", "rows": "82-85",
                 "vo_source_s": [VO_T0, round(VO_T0 + VO_LEN, 2)],
                 "pic_source_s": [PIC_T0, round(PIC_T0 + VO_LEN, 2)],
                 "upscale": 1080 / 607.5},
        "hook": hook, "captions": caps, "overlay_scale_bar": bar,
        "title_card": {"in": TITLE_IN, "out": TITLE_OUT, **title},
        "end_card": {"start_s": VO_LEN, "len_s": END_LEN, "bg": "opening plate PIA11141 (loop)", **endt},
        "audio": aud, "sfx_level_check": sfx_chk.stdout.strip(),
        "grain": "noise=alls=4:allf=t",
        "cover": str(cover_path), "cover_preview": str(thumb_sheet), "contact_sheet": str(contact_path),
        "uat_dir": str(UAT), "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    UAT.mkdir(parents=True, exist_ok=True)
    for p in (FINAL, contact_path, cover_path, thumb_sheet, OUT / f"{STEM}_gate.json", OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_meta.json"):
        dst = UAT / p.name
        dst.unlink(missing_ok=True)
        shutil.copy2(p, dst)
    print(gate_txt.stdout)
    print(json.dumps({k: meta[k] for k in ("file", "duration_s", "audio", "sfx_level_check")}, indent=2))


if __name__ == "__main__":
    main()
