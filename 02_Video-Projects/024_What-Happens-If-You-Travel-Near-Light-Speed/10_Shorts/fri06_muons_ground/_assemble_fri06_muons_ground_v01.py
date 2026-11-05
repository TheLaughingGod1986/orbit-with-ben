#!/usr/bin/env python3
"""024 Short fri06 muons / ground, v01 (J2248). £0. Locked VO, existing muon code graphic, house SFX, the film's own bed.

No new mint. Mon 9 Nov is already taken by iyvWYFP_ETA, so the gate air date is the next free
Mon/Wed/Fri/Sat 11:30 slot that was free on 5 Nov: Sat 21 Nov 2026. Scheduling waits on review and Ben's watch.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

SRC = Path("/tmp/j2248-muons/muons_b.mp4")
VO = Path("/tmp/j2248-vo/vo.mp3")
BED = FILM / "05_Music/light-speed_score_bed_v01_full.mp3"
WORDS = HERE / "words.json"
KIT = FILM / "06_Sound-Effects/kit_v01"
WORK = HERE / "_work_v01"
OUT = HERE / "06_Final-Exports"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/024_fri06_muons_ground_v01")
STEM = "fri06_muons_ground_v01"
GRAPHIC = "code_graphic_024_fri06_muons_b.mp4"
FINAL = OUT / f"{STEM}.mp4"

TOTAL = 22.20
FPS = 30
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
LONG_TITLE = "What Happens If You Travel Near Light Speed?"
HOOK_ROWS = [("THEY", WHITE), ("LIVE", YELLOW)]
HOOK_END = 2.15
TITLE_IN, TITLE_OUT = 9.0, 14.0
TITLE_ROWS = ["Muons Shouldn't", "Reach the Ground.", "They Do."]
FACT_IN, FACT_OUT = 6.55, 8.75
FACT_ROWS = ["TWO MILLIONTHS"]
AIR_DATE = "2026-11-21"
BED_AT = 48.0  # into the film's own bed; the file itself stays the music-gate source

# Each row is its own portrait render of the same shower (new seed, no full-width rules).
# The 16:9 muons graphic's atmosphere and ground lines fail polish_gate as horizontal seams,
# and a centre crop that drops them upscales past 2.35x. These are the same cyan streaks, full frame.
SEGS = [
    # film_in, dur, seed, speed px/frame, mode
    (0.00, 2.60, 1963, 36, "dense"),
    (2.60, 3.50, 2201, 28, "clock"),
    (6.10, 2.90, 2447, 40, "dense"),
    (9.00, 3.60, 2711, 34, "dense"),
    (12.60, 3.80, 3001, 38, "dense"),
    (16.40, 3.40, 3313, 44, "burst"),
    (19.80, 2.40, 1963, 36, "dense"),
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
    (WORK / "words_used.json").write_text(json.dumps(out, indent=2) + "\n")
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


def navy() -> np.ndarray:
    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(0, 1, W)[None, :]
    r = np.hypot((xx - 0.5) / 0.72, (yy - 0.42) / 0.85)
    k = np.clip(1 - r, 0, 1) ** 1.2
    edge = np.array([18, 28, 52], dtype=np.float32)
    centre = np.array([42, 68, 112], dtype=np.float32)
    img = edge + (centre - edge) * k[..., None]
    return img


def render_shower(dest: Path, seconds: float, seed: int, speed: float, mode: str) -> None:
    """Portrait cosmic-ray shower. No full-width rules (those read as split panels)."""
    rng = np.random.default_rng(seed)
    n = int(round(seconds * FPS))
    bed = navy()
    if mode == "clock":
        bed = bed * 0.72 + np.array([28, 36, 18], dtype=np.float32)
    elif mode == "burst":
        bed = bed * 0.85 + np.array([24, 18, 8], dtype=np.float32)
    grain = rng.normal(0, 3.5, (H, W, 1)).astype(np.float32)
    base = np.clip(bed + grain, 0, 255).astype(np.uint8)
    count = 28 if mode == "clock" else (40 if mode == "burst" else 110)
    x = rng.uniform(0, W, count)
    y = rng.uniform(-200, H, count)
    ang = rng.normal(0, 0.08 if mode == "dense" else 0.2, count)
    length = rng.uniform(220, 420, count)
    width = 11 if mode == "dense" else 16
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-crf", "16", str(dest)],
        stdin=subprocess.PIPE)
    assert enc.stdin is not None
    for frame_i in range(n):
        im = Image.fromarray(base.copy(), "RGB")
        draw = ImageDraw.Draw(im)
        y = y + speed
        x = x + ang * speed * 0.35
        wrap = y > H + 40
        y = np.where(wrap, rng.uniform(-420, -30, count), y)
        x = np.where(wrap, rng.uniform(-40, W + 40, count), x)
        colour = (255, 196, 70) if mode == "burst" else (90, 214, 255)
        for i in range(count):
            x2 = float(x[i] - ang[i] * length[i])
            y2 = float(y[i] - length[i])
            draw.line([(x2, y2), (float(x[i]), float(y[i]))], fill=colour, width=width)
            draw.ellipse((float(x[i]) - 8, float(y[i]) - 8, float(x[i]) + 8, float(y[i]) + 8), fill=(244, 239, 230))
        if mode == "clock":
            cx, cy, r = W // 2, int(H * 0.48), 340
            ang_h = frame_i * 0.22
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(18, 32, 58), outline=(255, 210, 60), width=22)
            hx = cx + int(np.sin(ang_h) * (r - 50))
            hy = cy - int(np.cos(ang_h) * (r - 50))
            draw.line([(cx, cy), (hx, hy)], fill=(255, 210, 60), width=22)
            draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(255, 210, 60))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit(f"shower encode failed: {dest}")


def plates() -> list[Path]:
    paths = []
    for i, (t0, length, seed, speed, mode) in enumerate(SEGS):
        nxt = SEGS[i + 1][0] if i + 1 < len(SEGS) else TOTAL
        if abs((t0 + length) - nxt) > 0.011:
            raise SystemExit(f"segment {i} does not meet the next")
        dest = OUT / f"code_graphic_024_fri06_muons_s{i + 1:02d}.mp4"
        render_shower(dest, length, seed, speed, mode)
        paths.append(dest)
    lst = WORK / "plates.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(WORK / "plates.mp4")])
    return paths


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
    sfx = WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick), "-filter_complex",
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=-8dB[w];"
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,adelay={int(FACT_IN * 1000)}:all=1[t];"
         f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={TOTAL:.3f}[o]",
         "-map", "[o]", "-t", f"{TOTAL:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_i = lufs(WORK / "stem_sfx_raw.wav")
    sfx_gain = (vo_i - 23.0) - sfx_i
    run(["ffmpeg", "-y", "-v", "error", "-i", WORK / "stem_sfx_raw.wav", "-af", f"volume={sfx_gain:.2f}dB", str(sfx)])
    return {"vo_lufs": vo_i, "bed_lufs": bed_i, "bed_gain_db": round(bed_gain, 2),
            "sfx_gain_db": round(sfx_gain, 2), "bed_at_s": BED_AT}


def composite(caps: list[dict]) -> None:
    loop = ["-loop", "1", "-framerate", str(FPS), "-t", f"{TOTAL:.3f}"]
    inputs = ["-i", str(WORK / "plates.mp4")]
    for name in ("hook.png", "title.png", "fact.png"):
        inputs += [*loop, "-i", str(WORK / name)]
    for i in range(len(caps)):
        inputs += [*loop, "-i", str(WORK / f"cap_{i:02d}.png")]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN:.2f}:d=0.25:alpha=1,fade=t=out:st={TITLE_OUT - 0.25:.2f}:d=0.25:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='between(t,{TITLE_IN},{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={FACT_IN:.2f}:d=0.25:alpha=1,fade=t=out:st={FACT_OUT - 0.25:.2f}:d=0.25:alpha=1[ft]",
        f"[v2][ft]overlay=0:0:enable='between(t,{FACT_IN},{FACT_OUT})'[v3]",
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
    times = [0.0, 0.5, 1.6, 2.7, 6.7, 9.4, 12.2, 15.2, 18.0, 21.6]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"tile_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
             "-vf", "scale=216:384", str(p)])
        tiles.append((p, t))
    canvas = Image.new("RGB", (216 * 5, 410 * 2), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 22)
    for i, (p, t) in enumerate(tiles):
        cx, cy = (i % 5) * 216, (i // 5) * 410
        canvas.paste(Image.open(p), (cx, cy))
        d.text((cx + 8, cy + 388), f"{t:.1f}s", font=font, fill=(255, 255, 255))
    canvas.save(dest, quality=90)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing muon graphic: {SRC}")
    if sha256(VO) != "3b17b23c8c476efa240375375ffe738fd8dacd254f622f2cef97152089779e8a":
        raise SystemExit("VO hash is not the locked v01 take")
    if sha256(BED) != "7859c2294b05250d24e733d22a971d5356fc6a92056f5fba0bf828035af8673b":
        raise SystemExit("bed hash is not light-speed_score_bed_v01_full")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words = load_words()
    if not 55 <= len(words) <= 65:
        raise SystemExit(f"word count {len(words)} outside 55-65")
    text_png(WORK / "hook.png", [t for t, _ in HOOK_ROWS], 220, H * 0.090, [c for _, c in HOOK_ROWS], stroke=8)
    text_png(WORK / "title.png", TITLE_ROWS, 430, H * 0.052, stroke=6)
    text_png(WORK / "fact.png", FACT_ROWS, 980, H * 0.070, [YELLOW], stroke=8)
    caps = caption_chunks(words)
    for i, c in enumerate(caps):
        text_png(WORK / f"cap_{i:02d}.png", [c["text"].upper()], 1460, H * 0.042, stroke=5)
    shower_paths = plates()
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.2", "-i", str(WORK / "plates.mp4"), "-frames:v", "1",
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

    cuts = []
    pool = []
    for i, (t0, length, _seed, _speed, _mode) in enumerate(SEGS):
        name = shower_paths[i].name
        cuts.append({
            "row": f"s{i + 1:02d}_muons",
            "timeline_in": t0,
            "timeline_out": round(t0 + length, 2),
            "source": name,
            "upscale": 1.0,
            "framing": {"offset": 0.0},
            "video": True,
        })
        pool.append({
            "file_id": name,
            "title": "Our own cosmic-ray muon shower, cyan streaks already falling",
        })
    (OUT / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / "pool_v01.json").write_text(json.dumps(pool, indent=2) + "\n")

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
         "--bed", str(BED), "--video", str(FINAL), "--out", str(OUT / "music_gate_v01.json")],
        capture_output=True, text=True)
    (OUT / "music_gate_v01.txt").write_text((music.stdout or "") + (music.stderr or ""))

    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v01.json"), "--out", str(OUT / "polish_gate_v01.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v01.txt").write_text((polish.stdout or "") + (polish.stderr or ""))

    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(FINAL),
         "--cuts", str(OUT / "cuts_v01.json"), "--pool", str(OUT / "pool_v01.json"),
         "--out-dir", str(OUT / "picture_qa_v01")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v01.txt").write_text((pqa.stdout or "") + (pqa.stderr or ""))

    meta = {
        "file": str(FINAL), "version": "v01", "job": "J2248",
        "sha256": sha256(FINAL), "duration_s": dur(FINAL),
        "spoken": " ".join(w["w"] for w in words),
        "air_date_provisional": AIR_DATE,
        "slot_note": "Mon 9 Nov 2026 is occupied by iyvWYFP_ETA. Do not schedule until review KEEP and Ben's watch. Recheck the slot first.",
        "long": {"id": "rVqgtkBV3jc", "title": LONG_TITLE},
        "title": "Muons Shouldn't Reach the Ground. They Do.",
        "hook": "THEY LIVE",
        "words": len(words),
        "vo_sha256": sha256(VO),
        "bed_sha256": sha256(BED),
        "graphic_sha256": {p.name: sha256(p) for p in shower_paths},
        "wide_reference_sha256": sha256(SRC),
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
    UAT.mkdir(parents=True, exist_ok=True)
    for p in (FINAL, contact_path, cover_path, thumb_sheet, OUT / f"{STEM}_meta.json",
              OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_sfx.txt", OUT / "music_gate_v01.txt",
              OUT / "polish_gate_v01.txt", OUT / "picture_qa_v01.txt"):
        if p.exists():
            shutil.copy2(p, UAT / p.name)
    print(gate_txt.stdout or gate_txt.stderr)
    print("--- sfx", sfx_chk.returncode)
    print((sfx_chk.stdout or sfx_chk.stderr)[-800:])
    print("--- music", music.returncode)
    print((music.stdout or music.stderr)[-500:])
    print("--- polish", polish.returncode)
    print((polish.stdout or polish.stderr)[-800:])
    print("--- picture", pqa.returncode)
    print((pqa.stdout or pqa.stderr)[-800:])
    print(json.dumps({k: meta[k] for k in (
        "duration_s", "gate_ok", "sfx_level_ok", "music_gate_ok", "polish_gate_ok", "picture_qa_ok", "audio")}, indent=2))
    if not all(meta[k] for k in ("gate_ok", "sfx_level_ok", "music_gate_ok", "polish_gate_ok", "picture_qa_ok")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
