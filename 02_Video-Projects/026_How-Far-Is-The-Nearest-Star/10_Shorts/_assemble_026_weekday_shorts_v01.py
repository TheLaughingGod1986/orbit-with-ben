#!/usr/bin/env python3
"""J0141 — 026 weekday Shorts. Assembly only. No new VO, no new picture, no credit.

Locked takes stay whole (no trim). The end card replaces the last-3-s loop (Chief OK, 12 Oct).
Picture is cut from the v06 long. The long's upload id is c5AdqQsnnys.

Quote times are the v06 caption lock (nearest_star_long_v06_en-GB.srt), timed to the
picture, not the VO file:
  Mon  "Your two eyes are a ruler."     141.400 s (00:02:21.400)
  Wed  "Could we ever go and look?"     421.904 s (00:07:01.904)
  Fri  "It has barely left the town."   309.800 s (00:05:09.800)
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
FILM = HERE.parent
REPO = FILM.parents[1]
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

PICTURE = FILM / "07_Edit-Project/026_NearestStar_v06.mp4"
BED = FILM / "05_Music/nearest-star_score_bed_v01_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
THUMB = FILM / "08_Thumbnail/abc_v01/nearest_star_thumb_A_you-cant-see-it.jpg"
NAS = Path("/Volumes/data/mac-mini-archive/youtube-staging/026/shorts_j0141")

HOLD = 2.00          # seconds of card after the last VO word
CARD = 3.85          # end card length; under the 4 s still-hold
FPS = 30
W, H = 1080, 1920
PUSH = 0.16
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
LONG_TITLE = "How Far Is the Nearest Star?"
LONG_ID = "c5AdqQsnnys"
TITLE_IN, TITLE_OUT = 9.0, 14.0
HOOK_END = 2.0

# (src_t, length) inside v06. Lengths stay inside that cut. Sums equal VO + HOLD - CARD.
SHORTS = [
    {
        "slug": "mon16_cant_see_nearest_star",
        "stem": "mon16_cant_see_nearest_star_v01",
        "air": "2026-11-16",
        "vo": 24.48,
        "lock": "mon16_cant_see_nearest_star_vo_v01_LOCK.wav",
        "words": "words.json",
        "title": "If You Can't See the Nearest Star, How Far Away Is It?",
        "title_rows": ["If You Can't See", "the Nearest Star,", "How Far Away", "Is It?"],
        "hook": [("TOO", WHITE), ("FAINT", YELLOW)],
        "cover": [("4.24", YELLOW), ("LIGHT-YEARS", WHITE)],
        "quote": "Your two eyes are a ruler.",
        "quote_s": 141.400,
        "voyager": False,
        # Spans stay off v06 overlay windows. A 9:16 centre crop clips those cards.
        "spans": [
            (98.17, 4.80, "ESO Paranal night sky (uhd_bt_paranal_07)"),
            (152.73, 4.50, "ESO VLT from Vista time-lapse"),
            (157.57, 4.50, "NASA/ESA Hubble star field (e000256)"),
            (68.33, 4.50, "ESO La Silla Crux (bt_lasilla_crux)"),
            (200.50, 4.33, "ESO La Silla night-sky time-lapse"),
        ],
    },
    {
        "slug": "wed18_robot_reach_nearest_star",
        "stem": "wed18_robot_reach_nearest_star_v01",
        "air": "2026-11-18",
        "vo": 21.60,
        "lock": "wed18_robot_reach_nearest_star_vo_v01_LOCK.wav",
        "words": "words.json",
        "title": "If Voyager Needs 75,000 Years, How Far Is the Nearest Star?",
        "title_rows": ["If Voyager Needs", "75,000 Years,", "How Far Is the", "Nearest Star?"],
        "hook": [("75,000", WHITE), ("YEARS", YELLOW)],
        "cover": [("17 KM/S", YELLOW), ("NOT ENOUGH", WHITE)],
        "quote": "Could we ever go and look?",
        "quote_s": 421.904,
        "voyager": False,
        # 9:16 centre crop. Stay off v06 cards and the crossfades that carry them:
        # PIA17049 is clean 296.7–299.6 (card "1977 · VOYAGER" is on screen by 300.0);
        # PIA14111 is clean after the Journey-to-Proxima fade, 337.4–340.9;
        # flare stays in the full-disc stretch (letterbox by 413.8);
        # star trails from 346.5 (launch dissolve is gone);
        # paranal_01 ends before the "LIGHT FROM PROXIMA" card at 12.0;
        # paranal_06 13.8–17.0 is the observatory with no card.
        "spans": [
            (296.75, 2.85, "NASA Voyager plate (PIA17049)"),
            (337.45, 3.50, "NASA Voyager plate (PIA14111)"),
            (408.25, 4.20, "NASA SDO solar flare"),
            (346.50, 3.10, "ESO star trails at Paranal"),
            (8.40, 2.90, "ESO Paranal night sky (uhd_bt_paranal_01)"),
            (13.80, 3.20, "ESO Paranal observatory (uhd_bt_paranal_06)"),
        ],
    },
    {
        "slug": "fri20_grapefruit_cherry",
        "stem": "fri20_grapefruit_cherry_v01",
        "air": "2026-11-20",
        "vo": 20.64,
        "lock": "fri20_grapefruit_cherry_vo_v01_LOCK.wav",
        "words": "words.json",
        "title": "The Nearest Star Is a Cherry Past Cairo. How Do We Know?",
        "title_rows": ["The Nearest Star", "Is a Cherry", "Past Cairo.", "How Do We Know?"],
        "hook": [("A", WHITE), ("CHERRY", YELLOW)],
        "cover": [("4,000 KM", YELLOW), ("AWAY", WHITE)],
        "quote": "It has barely left the town.",
        "quote_s": 309.800,
        "voyager": True,
        "spans": [
            (68.33, 4.77, "ESO La Silla Crux (bt_lasilla_crux)"),
            (250.03, 4.63, "NASA Blue Marble 2007 Earth"),
            (286.63, 4.70, "ESO star field (eso0905a)"),
            (277.37, 4.69, "ESO La Silla night-sky time-lapse"),
        ],
    },
]


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lufs(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
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


def joined(rows: list[str]) -> str:
    return " ".join(rows)


def check_plan() -> None:
    for s in SHORTS:
        need = round(s["vo"] + HOLD - CARD, 2)
        got = round(sum(length for _, length, _ in s["spans"]), 2)
        if abs(got - need) > 0.02:
            raise SystemExit(f"{s['slug']} spans {got} != card start {need}")
        if joined(s["title_rows"]) != s["title"]:
            raise SystemExit(f"{s['slug']} title rows do not join to the listing title")
        if s["vo"] + HOLD < 22 or s["vo"] + HOLD >= 40:
            raise SystemExit(f"{s['slug']} duration {s['vo'] + HOLD} outside 22–39 s")


def load_words(path: Path, work: Path, vo_len: float) -> list[dict]:
    raw = json.loads(path.read_text())
    src = raw["words"] if isinstance(raw, dict) and "words" in raw else raw
    out = [{"w": w["text"], "s": round(float(w["start"]), 3), "e": round(float(w["end"]), 3)} for w in src]
    if out and out[-1]["e"] > vo_len + 0.15:
        raise SystemExit(f"words run past the locked take ({out[-1]['e']} > {vo_len})")
    (work / "words.json").write_text(json.dumps(out, indent=2) + "\n")
    return out


def caption_chunks(words: list[dict], vo_len: float, card_in: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    raw = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_len
        end = min(nxt, c[-1]["e"] + 0.45, vo_len)
        raw.append({"text": " ".join(x["w"] for x in c).rstrip(",."), "s": start, "e": end})
    # Keep captions off the 9–14 s title and off the end card.
    out = []
    for c in raw:
        for a, b in ((0.0, TITLE_IN), (TITLE_OUT, card_in)):
            ss, ee = max(c["s"], a), min(c["e"], b)
            if ee - ss >= 0.25:
                out.append({"text": c["text"], "s": round(ss, 2), "e": round(ee, 2)})
    return out


def hook_png(dest: Path, rows: list[tuple[str, tuple]]) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.085 / 0.72, 0.86)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.86:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    y = 260
    boxes = []
    for t, c in rows:
        boxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in rows), "font_px": f.size, "bboxes": boxes}


def title_png(dest: Path, rows: list[str]) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = font_for(LINE_H).size
    gap = 0
    f = ImageFont.truetype(FONT, size)
    while size >= 28:
        f = ImageFont.truetype(FONT, size)
        gap = d.textbbox((0, 0), "Hg", font=f)[3] + 8
        block = gap * len(rows)
        wide = max(d.textlength(r, font=f) for r in rows)
        if block <= BAND_H - 12 and wide <= W * 0.90:
            break
        size -= 2
    else:
        raise SystemExit(f"title does not fit the 16:9 band: {rows}")
    y = BAND_Y0 + (BAND_H - gap * len(rows)) // 2
    placed = []
    for r in rows:
        bb = centred(d, y, r, f, WHITE)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"title outside the 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "joined": joined(rows)}


def caption_png(dest: Path, text: str) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.92)
    shown = text.upper()
    while d.textlength(shown, font=f) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    centred(d, BAND_Y0 + BAND_H + 70, shown, f, WHITE, stroke=6)
    im.save(dest)


def end_card_png(dest: Path, quote: str, voyager: bool) -> dict:
    thumb = Image.open(THUMB).convert("RGB")
    tw, th = thumb.size
    scale = max(W / tw, H / th)
    rw, rh = round(tw * scale), round(th * scale)
    bg = thumb.resize((rw, rh), Image.Resampling.LANCZOS)
    # The thumb's own words sit on the left. Keep the blurred ground on the star.
    left = min(rw - W, int((rw - W) * 0.92))
    top = (rh - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(22))).enhance(0.72)
    im = bg.convert("RGBA")
    max_h = int(BAND_H * 0.56)
    s = min(860 / tw, max_h / th)
    sw, sh = round(tw * s), round(th * s)
    sharp = thumb.resize((sw, sh), Image.Resampling.LANCZOS)
    x = (W - sw) // 2
    y = BAND_Y0 + 4
    im.paste(sharp, (x, y))
    d = ImageDraw.Draw(im)
    rows: list[tuple[str, tuple, str]] = [
        ("How Far Is", WHITE, "title"),
        ("the Nearest Star?", WHITE, "title"),
        (LONG_ID, YELLOW, "id"),
    ]
    if voyager:
        rows.append(("VOYAGER", YELLOW, "label"))
    rows.append((quote, WHITE, "quote"))
    y_text = y + sh + 6
    limit = BAND_Y0 + BAND_H - 6
    size = 40
    fonts: list[ImageFont.FreeTypeFont] = []
    heights: list[int] = []
    while size >= 20:
        fonts, heights = [], []
        ok = True
        for text, _col, kind in rows:
            px = size if kind in ("title", "id") else max(18, size - 8)
            if kind == "label":
                px = max(16, size - 14)
            ff = ImageFont.truetype(FONT, px)
            bb = d.textbbox((0, 0), text, font=ff, stroke_width=4)
            if d.textlength(text, font=ff) > W * 0.92:
                ok = False
            fonts.append(ff)
            heights.append(bb[3] - bb[1])
        if ok and y_text + sum(heights) + 4 * (len(rows) - 1) <= limit:
            break
        size -= 2
    else:
        raise SystemExit("end card does not fit the 16:9 band")
    yy = y_text
    placed = []
    for (text, col, kind), ff, h in zip(rows, fonts, heights):
        bb = centred(d, yy, text, ff, col, stroke=4)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"end card outside the 16:9 band: {text} {bb}")
        placed.append({"text": text, "kind": kind, "bbox": bb})
        yy += h + 4
    im.convert("RGB").save(dest, quality=95)
    return {"rows": placed, "thumb": str(THUMB), "thumb_unaltered": True, "youtube_id": LONG_ID}


def cover_png(dest: Path, plate: Path, rows: list[tuple[str, tuple]]) -> None:
    im = Image.open(plate).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.78)
    d = ImageDraw.Draw(im)
    size = 60
    while True:
        f = ImageFont.truetype(FONT, size + 2)
        if max(d.textlength(r, font=f) for r, _ in rows) > W * 0.78:
            break
        size += 2
        if size > 160:
            break
    f = ImageFont.truetype(FONT, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    block = lh * len(rows)
    y = BAND_Y0 + (BAND_H - block) // 2
    for r, c in rows:
        centred(d, y, r, f, c, stroke=8)
        y += lh
    im.save(dest, quality=92)


def cut_spans(work: Path, spans: list[tuple]) -> None:
    lines = []
    for i, (src_t, length, _label) in enumerate(spans):
        piece = work / f"span_{i}.mp4"
        pre = max(0.0, src_t - 1.5)
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{pre:.3f}", "-i", str(PICTURE),
             "-ss", f"{src_t - pre:.3f}", "-t", f"{length:.3f}", "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-video_track_timescale", "30000", str(piece)])
        lines.append(f"file '{piece.name}'")
    lst = work / "span_list.txt"
    lst.write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(work / "picture_span.mp4")])


def audio(work: Path, lock: Path, total: float, vo_len: float, card_in: float) -> dict:
    vo = work / "stem_vo.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(lock),
         "-af", f"apad=whole_dur={total:.3f}",
         "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", str(vo)])
    bed = work / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{total:.3f}", "-i", str(BED),
         "-af", f"afade=t=in:d=0.05,afade=t=out:st={total - 0.5:.3f}:d=0.5",
         "-ar", "48000", "-ac", "2", str(bed)])
    vo_i, bed_i = lufs(vo), lufs(bed)
    bed_gain = (vo_i - 24.0) - bed_i
    bed_l = work / "stem_bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed), "-af", f"volume={bed_gain:.2f}dB", str(bed_l)])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    hits = [(whoosh, 0.0), (tick, TITLE_IN), (tick, card_in)]
    inputs, parts = [], []
    for i, (f, at) in enumerate(hits):
        inputs += ["-i", str(f)]
        parts.append(
            f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(at * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(hits)))
    sfx_raw = work / "stem_sfx_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(parts) + f";{mix}amix=inputs={len(hits)}:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(sfx_raw)])
    sfx_gain = (vo_i - 23.0) - lufs(sfx_raw)
    sfx = work / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(sfx_raw), "-af", f"volume={sfx_gain:.2f}dB", str(sfx)])
    mixed = work / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo), "-i", str(bed_l), "-i", str(sfx),
         "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", "48000", "-t", f"{total:.3f}", str(mixed)])
    return {
        "vo_lufs": vo_i, "bed_gain_db": round(bed_gain, 2), "sfx_gain_db": round(sfx_gain, 2),
        "mix_lufs": lufs(mixed), "lock": str(lock), "vo_len_s": vo_len, "no_trim": True,
    }


def build(spec: dict) -> dict:
    slug = spec["slug"]
    folder = HERE / slug
    work = folder / "_work_j0141"
    out = folder / "06_Final-Exports"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    out.mkdir(parents=True, exist_ok=True)
    vo_len = spec["vo"]
    total = round(vo_len + HOLD, 2)
    card_in = round(vo_len + HOLD - CARD, 2)
    lock = folder / spec["lock"]
    if abs(dur(lock) - vo_len) > 0.05:
        raise SystemExit(f"{slug} lock is {dur(lock):.3f}s, expected {vo_len}")
    words = load_words(folder / spec["words"], work, vo_len)
    caps = caption_chunks(words, vo_len, card_in)
    hook = hook_png(work / "hook.png", spec["hook"])
    title = title_png(work / "title.png", spec["title_rows"])
    for i, c in enumerate(caps):
        caption_png(work / f"cap_{i:02d}.png", c["text"])
    end = end_card_png(work / "end_card.png", spec["quote"], spec["voyager"])
    print(f"{slug}: cutting {len(spec['spans'])} spans", flush=True)
    cut_spans(work, spec["spans"])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "picture_span.mp4"), "-frames:v", "1",
         "-vf", "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos", str(work / "plate0.png")])
    cover_path = out / f"{spec['stem']}_cover.jpg"
    cover_png(cover_path, work / "plate0.png", spec["cover"])
    aud = audio(work, lock, total, vo_len, card_in)

    final = out / f"{spec['stem']}.mp4"
    inputs = [
        "-t", f"{card_in:.3f}", "-i", str(work / "picture_span.mp4"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{CARD:.3f}", "-i", str(work / "end_card.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "hook.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "title.png"),
        "-i", str(work / "mix.wav"),
    ]
    base = 5
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i",
                   str(work / f"cap_{i:02d}.png")]
    fc = [
        f"[0:v]fps={FPS},crop=ih*9/16:ih,"
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a]",
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,trim=0:{CARD:.3f},setpts=PTS-STARTPTS[e]",
        "[a][e]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[3:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={TITLE_OUT - 0.30}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='between(t,{TITLE_IN},{TITLE_OUT})'[v2]",
    ]
    last = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = shorts_encode_args(fps=FPS)
    print(f"{slug}: encoding", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "4:a", *enc, "-t", f"{total:.3f}", str(final)])

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", spec["air"], "--json"],
        capture_output=True, text=True)
    (out / f"{spec['stem']}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", spec["air"]],
        capture_output=True, text=True)
    (out / f"{spec['stem']}_gate.txt").write_text(gate_txt.stdout or gate_txt.stderr)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(work / "stem_vo.wav"), "--sfx", str(work / "stem_sfx.wav"),
         "--bed", str(work / "stem_bed.wav"), "--minutes", f"{total / 60:.3f}"],
        capture_output=True, text=True)
    (out / f"{spec['stem']}_sfx.txt").write_text((sfx_chk.stdout or "") + (sfx_chk.stderr or ""))

    t = 0.0
    cuts, pool = [], []
    for i, (src_t, length, label) in enumerate(spec["spans"]):
        name = f"v06_{src_t:.2f}.mp4"
        cuts.append({
            "row": f"s{i + 1:02d}", "timeline_in": round(t, 2), "timeline_out": round(t + length, 2),
            "source": name, "upscale": 1.78, "framing": {"offset": src_t}, "video": True,
        })
        pool.append({"file_id": name, "title": f"{label} at {src_t:.2f}s of 026 v06"})
        t += length
    cuts.append({
        "row": "end_card", "timeline_in": card_in, "timeline_out": total,
        "source": "end_card_thumb_A.png", "upscale": 1.0, "video": False,
    })
    pool.append({"file_id": "end_card_thumb_A.png", "title": "End card: thumb A unaltered, long title, yellow id"})
    (out / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (out / "pool_v01.json").write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "job": "J0141", "file": str(final), "sha256": sha256(final), "duration_s": dur(final),
        "listing_title": spec["title"], "on_screen_title": title,
        "long": {"id": LONG_ID, "title": LONG_TITLE, "cut": "v06"},
        "quote": {"text": spec["quote"], "v06_picture_s": spec["quote_s"], "voyager_label": spec["voyager"]},
        "end_card": {"start_s": card_in, "len_s": CARD, "hold_after_vo_s": HOLD, **end},
        "hook": hook, "words": len(words), "captions": caps, "audio": aud,
        "spans": [{"t": a, "len": b, "what": c} for a, b, c in spec["spans"]],
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "sfx_ok": sfx_chk.returncode == 0,
        "spend": "none", "loop": "replaced by end card (Chief OK 12 Oct)",
    }
    (out / f"{spec['stem']}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{slug}: {meta['duration_s']:.2f}s gate={meta['gate_ok']} sfx={meta['sfx_ok']} {meta['sha256'][:12]}",
          flush=True)
    try:
        NAS.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final, NAS / final.name)
        (NAS / f"{final.name}.sha256").write_text(f"{meta['sha256']}  {final.name}\n")
    except OSError as e:
        print(f"{slug}: NAS copy skipped ({e})", flush=True)
    return meta


def main() -> int:
    check_plan()
    for p in (PICTURE, BED, THUMB, KIT / "sfx_owb_whoosh_soft_v01.wav", KIT / "sfx_owb_tick_ui_v01.wav"):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    quotes = {
        "cut": "026_NearestStar_v06",
        "source": "11_Upload-Package/Captions/nearest_star_long_v06_en-GB.srt",
        "measured": "picture-timed captions, not the VO file",
        "lines": [
            {"short": "mon", "text": "Your two eyes are a ruler.", "v06_s": 141.400},
            {"short": "wed", "text": "Could we ever go and look?", "v06_s": 421.904},
            {"short": "fri", "text": "It has barely left the town.", "v06_s": 309.800, "label": "VOYAGER"},
        ],
        "long_id": LONG_ID,
    }
    (HERE / "J0141_QUOTE_TIMES.json").write_text(json.dumps(quotes, indent=2) + "\n")
    fails = 0
    for spec in SHORTS:
        meta = build(spec)
        if not (meta["gate_ok"] and meta["sfx_ok"]):
            fails += 1
    print(f"done fails={fails}", flush=True)
    return fails


if __name__ == "__main__":
    if "--plan" in sys.argv:
        check_plan()
        for s in SHORTS:
            need = round(s["vo"] + HOLD - CARD, 2)
            print(s["slug"], "card_in", need, "total", round(s["vo"] + HOLD, 2), "title", joined(s["title_rows"]))
        raise SystemExit(0)
    raise SystemExit(main())
