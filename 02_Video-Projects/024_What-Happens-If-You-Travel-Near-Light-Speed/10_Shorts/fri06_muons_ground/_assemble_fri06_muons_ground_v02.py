#!/usr/bin/env python3
"""024 Short fri06 muons / ground, v02 (J2248). £0 corrective picture.

J2250 FIX + J2278 acting-Chief ruling: real moving 024 plates, at most one code
graphic, no TWO MILLIONTHS card, METRES in the caption, cover off the new open.
Locked VO and locked title stay. No mint, no upload, no schedule.

Plates are Earth Views from the International Space Station (public domain,
NASA images library, 1280x720). A full-bleed 9:16 crop of 720p is 2.67x, over
the 2.35x limit, so the sharp frame stays at 0.84x inside a blurred fill.
The blur is sigma 18 and the mask is clear before the bitmap edge: a hard
letterbox reads as a split panel, and this feather does not. Station hardware,
the Canadarm, and the limb horizon after 49 s are not used. Offsets stay at
least 10 s apart. The one graphic is streaks over a real Earth frame, on the
"born high up" line. "600 metres" is spoken under the 9–14 s title, so the
caption carries METRES and the graphic does not repeat it early.
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

SRC = Path("/tmp/j2248-v02")
EARTH = SRC / "Earth_Views_from_the_International_Space_Station.mp4"
NHQ_A = SRC / "nhq_1740.mp4"  # source offset 1740 of the NHQ file
NHQ_B = SRC / "nhq_560.mp4"   # source offset 560
VO = Path("/tmp/j2248-vo/vo.mp3")
BED = FILM / "05_Music/light-speed_score_bed_v01_full.mp3"
WORDS = HERE / "words.json"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v02"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/024_fri06_muons_ground_v02")
STEM = "fri06_muons_ground_v02"
GRAPHIC = "code_graphic_024_fri06_muons_v02_scale.mp4"
FINAL = OUT / f"{STEM}.mp4"

TOTAL = 22.20
FPS = 30
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
CYAN = (120, 220, 255, 210)
LONG_TITLE = "What Happens If You Travel Near Light Speed?"
LONG_ID = "rVqgtkBV3jc"
HOOK_ROWS = [("THEY", WHITE), ("LIVE", YELLOW)]
HOOK_END = 2.15
TITLE_IN, TITLE_OUT = 9.0, 14.0
TITLE_ROWS = ["Muons Shouldn't", "Reach the Ground.", "They Do."]
END_IN, END_OUT = 16.90, 21.05
END_ROWS = ["What Happens If", "You Travel Near", "Light Speed?"]
AIR_DATE = "2026-11-21"
BED_AT = 48.0
# v06's crop that drops the burnt-in "Earth from the Space Station" bug.
NHQ_CROP = "1096:616:88:104"
VO_SHA = "3b17b23c8c476efa240375375ffe738fd8dacd254f622f2cef97152089779e8a"
BED_SHA = "7859c2294b05250d24e733d22a971d5356fc6a92056f5fba0bf828035af8673b"

# film_in, dur, source key, source offset in THAT file, crop or None, upscale, title
# Earth offsets are >=10 s apart (picture_qa's same-stretch rule). Windows stay
# in the station-free earth, and stop before the limb seam at 49.2 s.
GRAPHIC_AT = 3.00
GRAPHIC_SS = 21.6  # ends at 25.8 s, before the 26 s plate
SEGS = [
    # 36.0 is the fast cloud pass (frame-0 motion). First cut at 3.0 s.
    (0.00, 3.00, "earth", 36.0, None, 0.84, "Earth Views from the International Space Station"),
    # Ends at 7.2 s so the following Earth run is 15.0 s, not over picture_qa's 15 s look.
    (3.00, 4.20, "graphic", 0.0, None, 1.0, "Muon streaks over a real ISS Earth view"),
    (7.20, 4.00, "earth", 14.0, None, 0.84, "Earth Views from the International Space Station"),
    (11.20, 4.00, "earth", 26.0, None, 0.84, "Earth Views from the International Space Station"),
    # 46–49 only: the limb horizon at 49.2 s is a full-width seam.
    (15.20, 3.00, "earth", 46.0, None, 0.84, "Earth Views from the International Space Station"),
    (18.20, 4.00, "earth", 60.0, None, 0.84, "Earth Views from the International Space Station"),
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
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def true_peak(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1])


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=6):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    stroke_fill = (0, 0, 0, fill[3] if len(fill) == 4 else 255)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def load_words() -> list[dict]:
    src = json.loads(WORDS.read_text())
    words = src["words"] if isinstance(src, dict) else src
    out = [{"w": w["text"], "s": float(w["start"]), "e": float(w["end"])} for w in words]
    return out


def caption_chunks(words: list[dict]) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else min(c[-1]["e"] + 0.35, TOTAL)
        end = min(nxt, c[-1]["e"] + 0.40, TOTAL)
        if end <= start:
            end = start + 0.2
        text = " ".join(x["w"] for x in c).rstrip(",.")
        text = re.sub(r"\bmeters\b", "metres", text, flags=re.I)
        out.append({"text": text, "s": round(start, 2), "e": round(end, 2)})
    return out


def text_png(dest: Path, rows: list, y0: int, cap_h: float, fills: list | None = None, stroke=7) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(cap_h)
    fills = fills or [WHITE] * len(rows)
    while max(d.textlength(t, font=f) for t in rows) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = y0
    for t, c in zip(rows, fills):
        centred(d, y, t, f, c, stroke=stroke)
        y += lh
    im.save(dest)


def feather_mask() -> Path:
    """Sharp centre, transparent before the 16:9 bitmap edge (about 304 px from centre)."""
    dest = WORK / "feather.png"
    # A 1280x720 frame scaled to width 1080 is 608 px tall, so its edge sits
    # 304 px from the centre of a 1920 frame. Alpha is 0 by 280 px, past which
    # only the blurred cover remains, so the bitmap edge is not a step.
    mid = H // 2
    opaque, fade = 70, 210
    im = Image.new("L", (W, H), 0)
    px = im.load()
    for y in range(H):
        dist = abs(y - mid)
        if dist <= opaque:
            v = 255
        elif dist >= opaque + fade:
            v = 0
        else:
            v = int(255 * (1 - (dist - opaque) / fade))
        for x in range(W):
            px[x, y] = v
    im.save(dest)
    return dest


def portrait_vf(pre_crop: str | None) -> str:
    pre = f"crop={pre_crop}," if pre_crop else ""
    # Sharp 16:9 band from the native frame (no upscale past 1x on a 1280 source),
    # feathered over a blurred cover so the 9:16 frame is full and has no seam.
    return (
        f"{pre}split[fg][bg];"
        f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=18[b];"
        f"[fg]scale={W}:-2,format=rgba,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black@0[f];"
        f"[f][1:v]alphamerge[s];"
        f"[b][s]overlay=0:0,format=yuv420p"
    )


def cut_clip(src: Path, ss: float, seconds: float, dest: Path, pre_crop: str | None, mask: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{seconds:.3f}", "-i", str(src),
         "-loop", "1", "-i", str(mask), "-filter_complex", portrait_vf(pre_crop),
         "-an", "-r", str(FPS), "-shortest", "-t", f"{seconds:.3f}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(dest)])


def make_graphic(mask: Path, seconds: float) -> Path:
    """One code graphic: real ISS Earth (not used as its own row) plus falling streaks."""
    dest = OUT / GRAPHIC
    plate = WORK / "graphic_base.mp4"
    cut_clip(EARTH, GRAPHIC_SS, seconds, plate, None, mask)
    streaks = WORK / "streaks.png"
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, x in enumerate(range(80, W, 90)):
        y0 = 180 + (i % 5) * 70
        d.line([(x, y0), (x - 40, y0 + 520)], fill=CYAN, width=4)
        d.ellipse([x - 46, y0 + 512, x - 34, y0 + 528], fill=(255, 244, 180, 230))
    im.save(streaks)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(plate), "-loop", "1", "-i", str(streaks),
         "-filter_complex",
         "[1:v]format=rgba,fade=t=in:d=0.35:alpha=1[s];"
         "[0:v][s]overlay=0:y='-180+70*t':format=auto,format=yuv420p[v]",
         "-map", "[v]", "-an", "-t", f"{seconds:.3f}", "-r", str(FPS),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(dest)])
    return dest


def plates(mask: Path, graphic: Path) -> list[Path]:
    files = {"earth": EARTH, "nhq_a": NHQ_A, "nhq_b": NHQ_B, "graphic": graphic}
    out = []
    for i, (t0, length, key, ss, crop, _up, _title) in enumerate(SEGS):
        dest = WORK / f"seg_{i:02d}.mp4"
        if key == "graphic":
            run(["ffmpeg", "-y", "-v", "error", "-i", str(graphic), "-an", "-r", str(FPS),
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-t", f"{length:.3f}", str(dest)])
        else:
            cut_clip(files[key], ss, length, dest, crop, mask)
        out.append(dest)
    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in out))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-r", str(FPS),
         str(WORK / "plates.mp4")])
    return out


def cover(plate: Path, dest: Path) -> None:
    im = Image.open(plate).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.25)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    d = ImageDraw.Draw(im)
    rows = [("SLOW", YELLOW), ("CLOCKS", WHITE)]
    size = 40
    while True:
        f = ImageFont.truetype(FONT, size + 4)
        if max(d.textlength(r, font=f) for r, _ in rows) > W * 0.86:
            break
        size += 4
    f = ImageFont.truetype(FONT, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 24
    y = (H - lh * len(rows)) // 2
    for r, c in rows:
        centred(d, y, r, f, c, stroke=10)
        y += lh
    im.save(dest, quality=92)


def audio() -> dict:
    vo = WORK / "stem_vo.wav"
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(VO),
         "-af", f"aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL:.3f}",
         "-ar", "48000", "-ac", "2", "-t", f"{TOTAL:.3f}", str(vo)])
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_AT:.3f}", "-t", f"{TOTAL:.3f}", "-i", str(BED),
         "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.15,afade=t=out:st={TOTAL - 0.45:.3f}:d=0.45",
         "-ar", "48000", "-ac", "2", str(bed_raw)])
    vo_i, bed_i = lufs(vo), lufs(bed_raw)
    bed_gain = (vo_i - 22.0) - bed_i
    bed = WORK / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", bed_raw, "-af", f"volume={bed_gain:.2f}dB", str(bed)])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick), "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=-8dB[w];"
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,adelay={int(GRAPHIC_AT * 1000)}:all=1[t];"
         f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={TOTAL:.3f}[o]",
         "-map", "[o]", "-t", f"{TOTAL:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_i = lufs(WORK / "stem_sfx_raw.wav")
    sfx_gain = (vo_i - 23.0) - sfx_i
    run(["ffmpeg", "-y", "-v", "error", "-i", WORK / "stem_sfx_raw.wav", "-af", f"volume={sfx_gain:.2f}dB",
         str(WORK / "stem_sfx.wav")])
    return {"vo_lufs": vo_i, "bed_lufs": bed_i, "bed_gain_db": round(bed_gain, 2),
            "sfx_gain_db": round(sfx_gain, 2), "bed_at_s": BED_AT}


def composite(caps: list[dict]) -> None:
    loop = ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}"]
    inputs = ["-i", str(WORK / "plates.mp4")]
    for name in ("hook.png", "title.png", "endcard.png"):
        inputs += [*loop, "-i", str(WORK / name)]
    for i in range(len(caps)):
        inputs += [*loop, "-i", str(WORK / f"cap_{i:02d}.png")]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN:.2f}:d=0.25:alpha=1,fade=t=out:st={TITLE_OUT - 0.25:.2f}:d=0.25:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='between(t,{TITLE_IN},{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={END_IN:.2f}:d=0.30:alpha=1,fade=t=out:st={END_OUT - 0.25:.2f}:d=0.25:alpha=1[en]",
        f"[v2][en]overlay=0:0:enable='between(t,{END_IN},{END_OUT})'[v3]",
    ]
    last = "v3"
    base = 4
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='between(t,{c['s']:.2f},{c['e']:.2f})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
         "-t", f"{TOTAL:.3f}", str(WORK / "picture.mp4")])


def mix_onto(picture: Path, aud: dict) -> None:
    vo, bed, sfx = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
    mix = "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(picture), "-i", str(vo), "-i", str(bed), "-i", str(sfx),
         "-filter_complex", mix + "loudnorm=I=-14:TP=-2:LRA=11:print_format=json[a]",
         "-map", "[a]", "-f", "null", "-"],
        capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = (
        f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
        f"linear=true,alimiter=limit=0.82:level=false"
    )
    enc = shorts_encode_args(fps=FPS)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(picture), "-i", str(vo), "-i", str(bed), "-i", str(sfx),
         "-filter_complex", mix + norm + ",aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *enc, "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", str(FINAL)])
    aud["mix_lufs"] = lufs(FINAL)
    aud["mix_true_peak"] = true_peak(FINAL)


def contact_sheet(video: Path, dest: Path) -> None:
    times = [0.0, 0.5, 1.6, 3.4, 6.8, 9.4, 12.8, 16.6, 18.4, 21.4]
    canvas = Image.new("RGB", (216 * 5, 410 * 2), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 22)
    for i, t in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
             "-vf", "scale=216:384", str(p)])
        cx, cy = (i % 5) * 216, (i // 5) * 410
        canvas.paste(Image.open(p), (cx, cy))
        d.text((cx + 8, cy + 388), f"{t:.1f}s", font=font, fill=(255, 255, 255))
    canvas.save(dest, quality=90)


def main() -> None:
    for p in (EARTH, NHQ_A, NHQ_B, VO, BED):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    if sha256(VO) != VO_SHA:
        raise SystemExit("VO hash is not the locked v01 take")
    if sha256(BED) != BED_SHA:
        raise SystemExit("bed hash is not light-speed_score_bed_v01_full")
    if abs(sum(s[1] for s in SEGS) - TOTAL) > 0.02:
        raise SystemExit("segment lengths do not add up")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words = load_words()
    if len(words) != 55:
        raise SystemExit(f"word count {len(words)} is not the locked 55")
    mask = feather_mask()
    graphic_len = next(s[1] for s in SEGS if s[2] == "graphic")
    graphic = make_graphic(mask, graphic_len)
    plates(mask, graphic)
    text_png(WORK / "hook.png", [t for t, _ in HOOK_ROWS], 220, H * 0.090, [c for _, c in HOOK_ROWS], stroke=8)
    text_png(WORK / "title.png", TITLE_ROWS, 430, H * 0.048, stroke=6)
    text_png(WORK / "endcard.png", END_ROWS + [LONG_ID], 980, H * 0.046,
             [WHITE, WHITE, YELLOW, WHITE], stroke=6)
    caps = caption_chunks(words)
    if not any("metres" in c["text"].lower() for c in caps):
        raise SystemExit("METRES caption did not land")
    if any(re.search(r"\bmeters\b", c["text"], re.I) for c in caps):
        raise SystemExit("US meters caption still present")
    for i, c in enumerate(caps):
        text_png(WORK / f"cap_{i:02d}.png", [c["text"].upper()], 1460, H * 0.042, stroke=5)
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.15", "-i", str(WORK / "plates.mp4"), "-frames:v", "1",
         str(WORK / "plate0.png")])
    cover_path = OUT / f"{STEM}_cover.jpg"
    cover(WORK / "plate0.png", cover_path)
    aud = audio()
    composite(caps)
    mix_onto(WORK / "picture.mp4", aud)

    contact_path = OUT / f"{STEM}_contact.jpg"
    contact_sheet(FINAL, contact_path)
    thumb_sheet = OUT / f"{STEM}_cover_preview.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
         "short", str(cover_path), "--out", str(thumb_sheet)])

    names = {
        "earth": EARTH.name,
        "nhq_a": "NHQ_2019_0626_Earth_Views_from_the_ISS.mp4",
        "nhq_b": "NHQ_2019_0626_Earth_Views_from_the_ISS.mp4",
        "graphic": GRAPHIC,
    }
    # NHQ rows are different stretches of one NASA film. Record the real source
    # offset (1740 / 560) so picture_qa does not treat the two extracts as one stretch.
    real_offset = {"nhq_a": 1740.0, "nhq_b": 560.0}
    cuts, pool, seen = [], [], set()
    for i, (t0, length, key, ss, _crop, up, title) in enumerate(SEGS):
        src_name = GRAPHIC if key == "graphic" else names[key]
        off = real_offset.get(key, ss)
        cuts.append({
            "row": f"s{i + 1:02d}_{key}",
            "timeline_in": t0,
            "timeline_out": round(t0 + length, 2),
            "source": src_name,
            "upscale": up,
            "framing": {"offset": off},
            "video": True,
        })
        if src_name not in seen:
            pool.append({"file_id": src_name, "title": title})
            seen.add(src_name)
    (OUT / "cuts_v02.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / "pool_v02.json").write_text(json.dumps(pool, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--json",
         "--vo", str(VO), "--script", str(HERE / "fri06_muons_ground_vo_v01.txt")],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(FINAL), "--air-date", AIR_DATE, "--vo", str(VO),
         "--script", str(HERE / "fri06_muons_ground_vo_v01.txt")],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate_txt.stdout or gate_txt.stderr)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(WORK / "stem_vo.wav"), "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"), "--minutes", f"{TOTAL / 60.0:.4f}"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_sfx.txt").write_text((sfx_chk.stdout or "") + (sfx_chk.stderr or ""))

    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
         "--bed", str(BED), "--video", str(FINAL), "--out", str(OUT / "music_gate_v02.json")],
        capture_output=True, text=True)
    (OUT / "music_gate_v02.txt").write_text((music.stdout or "") + (music.stderr or ""))

    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v02.json"), "--out", str(OUT / "polish_gate_v02.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v02.txt").write_text((polish.stdout or "") + (polish.stderr or ""))

    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v02.json"), "--pool", str(OUT / "pool_v02.json"),
         "--out-dir", str(OUT / "picture_qa_v02")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v02.txt").write_text((pqa.stdout or "") + (pqa.stderr or ""))

    meta = {
        "file": str(FINAL), "version": "v02", "job": "J2248",
        "sha256": sha256(FINAL), "duration_s": round(dur(FINAL), 3),
        "replaces": "fri06_muons_ground_v01.mp4 left in place, sha256 9fc197dcdbcd16d3812a183779b2c8dcba38f67495d5738741b4c6e8f411fd28",
        "air_date_provisional": AIR_DATE,
        "slot_note": "Mon 9 Nov 2026 is occupied by iyvWYFP_ETA. Do not schedule until v02 review KEEP and Ben's watch.",
        "long": {"id": LONG_ID, "title": LONG_TITLE},
        "title": "Muons Shouldn't Reach the Ground. They Do.",
        "hook": "THEY LIVE",
        "words": len(words),
        "vo_sha256": sha256(VO),
        "bed_sha256": sha256(BED),
        "plates": {
            "earth": {
                "file": EARTH.name,
                "sha256": sha256(EARTH),
                "url": "https://images.nasa.gov/details/Earth%20Views%20from%20the%20International%20Space%20Station",
                "licence": "Public domain (NASA images library)",
            },
            "graphic": {
                "file": GRAPHIC,
                "sha256": sha256(graphic),
                "base_offset": GRAPHIC_SS,
                "note": "Streaks over Earth Views from 21.6 s. Not a second cut of that stretch. No 600 METRES label: those words are spoken under the 9-14 s title, and the caption says METRES.",
            },
        },
        "inherited_scope": [
            "Locked statement title and locked VO kept (J2248 brief; J2278: no remint).",
            "Line 1 does not ask one question. Muons is first spoken at 4.82 s.",
            "0.68 s pause at 4.14-4.82 s was not trimmed.",
            "Payoff 'clocks run slow' overlaps the 9-14 s title.",
            "Spoken end line says 'The Speed Of Light'; the end card shows the live title and rVqgtkBV3jc.",
            "Last plate is the same Earth film at 60 s, not a pixel copy of frame 0.",
            "Sharp picture is a 0.84x 16:9 band with a sigma-18 feather. Full-bleed 9:16 would be 2.67x.",
            "The streak graphic runs 4.2 s and ends at 7.2 s, so the Earth run after it is 15.0 s and not over picture_qa's look threshold.",
        ],
        "audio": aud,
        "captions": caps,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "sfx_level_ok": sfx_chk.returncode == 0,
        "music_gate_ok": music.returncode == 0,
        "polish_gate_ok": polish.returncode == 0,
        "picture_qa_ok": pqa.returncode == 0,
        "spend": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(gate_txt.stdout or gate_txt.stderr)
    print("--- sfx", sfx_chk.returncode, (sfx_chk.stdout or sfx_chk.stderr)[-400:])
    print("--- music", music.returncode, (music.stdout or music.stderr)[-400:])
    print("--- polish", polish.returncode, (polish.stdout or polish.stderr)[-600:])
    print("--- picture", pqa.returncode, (pqa.stdout or pqa.stderr)[-800:])
    print(json.dumps({k: meta[k] for k in (
        "duration_s", "gate_ok", "sfx_level_ok", "music_gate_ok", "polish_gate_ok", "picture_qa_ok", "audio")}, indent=2))
    if not all(meta[k] for k in ("gate_ok", "sfx_level_ok", "music_gate_ok", "polish_gate_ok", "picture_qa_ok")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
