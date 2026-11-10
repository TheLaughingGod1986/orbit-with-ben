#!/usr/bin/env python3
"""J2510 — 025 Mars, Thu 12 Nov Short length test v05 (N42gKBbD7tE).

Built from _assemble_thu12_length_test_v01.py (the scheduled J0134 cut on disk):
1. Removes the raw video ID (Js6EQJ8qDi8) from the end card (title_png(..., with_id=False)).
2. Fixes the first-second Rule 24 gate failure (first cut > 3.0 s): hard-cuts from s01_r20
   (PIA22909.jpg, 0.000-2.400 s with the 12% opening push) to s02_r20 (PIA17759.jpg,
   2.400-6.733 s, sub-pixel push matching v03f at the 6.533 s crossfade into s03_r20) in the
   sentence pause after "Opportunity should have starved within months." (2.20-2.64 s).
3. Levels the locked v01 audio mix to the 26 Oct gate (-14.2 LUFS / -2.2 dBTP).
4. Leaves v01..v04 untouched and does not upload or change YouTube Studio.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(FILM / "07_Edit-Project"))
from fillbox import best_box  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

MASTER = Path("/Volumes/data/mac-mini-archive/youtube-staging/025/025_MarsRobot_full_rough_v03f.mp4")
MASTER_SHA = "cce6268c"
WORDS = FILM / "02_Voiceover/words.json"
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
PIA17759 = Path(
    "/Volumes/MiniWork/scratch/J2510/from_tar/02_Video-Projects/"
    "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/opp_deck/PIA17759.jpg"
)
V01_EXPORT_DIR = Path(
    "/Volumes/MiniWork/scratch/J2510/from_tar/02_Video-Projects/"
    "025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports"
)

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/mars025_thu12_lentest_v05")
STEM = "thu12_length_test_dust_v05"

W, H, FPS = 1080, 1920, 30
AIR = "2026-11-12"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)

SRC_IN = 254.70           # "Opportunity" starts 254.80; row 20 (PIA22909) runs 254.47-258.87
FIRST_WORD = "Opportunity"
LAST_WORD_END = 306.82    # "off." of "It was the sky turning off."
VO_CUT_ABS = 307.30       # next word "Why" starts 308.44
HOLD = 2.5
FADE = 1.0
CROP_X = (1920 - 608) // 2
CUT1_S = 2.400            # 72 frames: sentence pause between "months." (2.20s) and "Instead," (2.64s)
S02_JOIN_S = 6.533333     # 196 frames: 0.2s before s02_r20->s03_r20 cut at 6.7333s (where v03f xfade starts)
SHOT1_PUSH = 0.12
HOOK = ("SAVED BY", "THE WIND")
HOOK_END = 2.2
TITLE_WINDOWS = ((9.0, 14.0),)


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip())


def fit_font(draw: ImageDraw.ImageDraw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
    while size > 30:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, size)


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    draw.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return box[3] - box[1]


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, max(HOOK, key=len), 190, int(W * 0.84), 8)
    y = int(H * 0.06)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 24
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path, with_id: bool = False) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot", "Survive on Mars?"]
    font = fit_font(d, max(rows, key=len), 84, int(W * 0.86), 5)
    y = int(H * 0.10)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 18
    if with_id:
        centred(d, y + 14, LONG_ID, ImageFont.truetype(FONT, 72), YELLOW, 5)
    im.save(dest)


def caption_track(words: list[dict], end: float) -> Path:
    """PNG concat list: 1-3 word groups, broken at punctuation, phone-safe lower third."""
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cap_dir = WORK / "captions"
    if cap_dir.exists():
        shutil.rmtree(cap_dir)
    cap_dir.mkdir(parents=True, exist_ok=True)
    blank = cap_dir / "blank.png"
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
    lines = ["ffconcat version 1.0"]
    t = 0.0
    for i, g in enumerate(groups):
        start = max(g[0]["start"], t)
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.05)
        if start > t + 0.01:
            lines += [f"file '{blank}'", f"duration {start - t:.3f}"]
        text = " ".join(w["word"] for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 68, int(W * 0.72), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = cap_dir / f"cap_{i:03d}.png"
        im.save(p)
        lines += [f"file '{p}'", f"duration {stop - start:.3f}"]
        t = stop
    if end > t:
        lines += [f"file '{blank}'", f"duration {end - t:.3f}"]
    lines.append(f"file '{blank}'")
    lst = cap_dir / "captions.ffconcat"
    lst.write_text("\n".join(lines) + "\n")
    return lst


def render_s02_pia17759(dest: Path, frames: int) -> None:
    """Render s02_r20 (PIA17759.jpg, quad='c') with the exact v03f prep_still + subpixel push,
    ending at z = 1 + 0.05 * (77 / 89) at frame `frames` so it joins MASTER at 261.2333 s seamlessly."""
    im = Image.open(PIA17759).convert("RGB")
    fb = best_box(im, min_h_px=1) or (0, 0, 1, 1)
    need = 1080 * 1.05 / (2.35 - 0.02) * 2
    if (fb[3] - fb[1]) * im.height < need:
        h = min(im.height, need)
        w = min(im.width, h * 16 / 9)
        h = min(h, w * 9 / 16)
        cx = (fb[0] + fb[2]) / 2 * im.width
        cy = (fb[1] + fb[3]) / 2 * im.height
        x0 = min(max(0, cx - w / 2), im.width - w)
        y0 = min(max(0, cy - h / 2), im.height - h)
        fb = (x0 / im.width, y0 / im.height, (x0 + w) / im.width, (y0 + h) / im.height)
    im = im.crop((round(im.width * fb[0]), round(im.height * fb[1]),
                  round(im.width * fb[2]), round(im.height * fb[3])))
    # quad='c' -> (0.25, 0.25) to (0.75, 0.75)
    im = im.crop((int(im.width * 0.25), int(im.height * 0.25),
                  int(im.width * 0.75), int(im.height * 0.75)))
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    scale = max(2112 / im.width, 1188 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - 2112) // 2
    y = (im.height - 1188) // 2
    im = im.crop((x, y, x + 2112, y + 1188))

    end_pct = 0.05 * (77.0 / 89.0)
    pw, ph = im.width, im.height
    p = subprocess.Popen(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-",
            "-vf", f"crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p",
            "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
            str(dest),
        ],
        stdin=subprocess.PIPE,
    )
    assert p.stdin is not None
    for n in range(frames):
        z = 1.0 + end_pct * (n / frames)
        bw, bh = pw / z, ph / z
        box = ((pw - bw) / 2.0, (ph - bh) / 2.0, (pw + bw) / 2.0, (ph + bh) / 2.0)
        p.stdin.write(im.resize((1920, 1080), Image.Resampling.BICUBIC, box=box).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("s02 subpixel render failed")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def measure_ebur128(path: Path) -> tuple[float, float]:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    i_lufs = tp_db = None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("I:") and "LUFS" in s:
            i_lufs = float(s.split()[1])
        elif s.startswith("Peak:") and "dBFS" in s:
            tp_db = float(s.split()[1])
    if i_lufs is None or tp_db is None:
        raise RuntimeError(f"Could not parse ebur128 for {path}")
    return i_lufs, tp_db


def relevel_audio(src_media: Path, dst_wav: Path, target_i: float = -14.2, ceiling_db: float = -2.25) -> tuple[float, float]:
    cur_i, _ = measure_ebur128(src_media)
    gain_db = target_i - cur_i
    limit_lin = 10.0 ** (ceiling_db / 20.0)
    for _ in range(4):
        af = f"volume={gain_db:+.3f}dB,alimiter=limit={limit_lin:.6f}:attack=5:release=50:level=false"
        run(["ffmpeg", "-y", "-v", "error", "-i", src_media, "-vn", "-af", af,
             "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", dst_wav])
        new_i, new_tp = measure_ebur128(dst_wav)
        if -14.4 <= new_i <= -13.9 and new_tp <= -2.05:
            return new_i, new_tp
        gain_db += target_i - new_i
    return measure_ebur128(dst_wav)


def main() -> None:
    for p in (MASTER, WORDS, BED, PIA17759):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    if not sha256(MASTER).startswith(MASTER_SHA):
        raise SystemExit("master sha256 does not match the uploaded v03f")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    raw = json.loads(WORDS.read_text())
    words = raw.get("words", raw) if isinstance(raw, dict) else raw
    words = [
        {"word": (w.get("word") or w.get("text")).strip(), "start": w["start"] - SRC_IN, "end": w["end"] - SRC_IN}
        for w in words if SRC_IN <= w["start"] and w["end"] <= LAST_WORD_END + 0.01
    ]
    if words[0]["word"] != FIRST_WORD or not words[-1]["word"].startswith("off"):
        raise SystemExit(f"stretch words wrong: {words[0]['word']} .. {words[-1]['word']}")
    last_end = words[-1]["end"]
    vo_cut = VO_CUT_ABS - SRC_IN
    total = round(last_end + HOLD, 3)
    if not 50.0 <= total <= 60.0:
        raise SystemExit(f"total {total} outside the 50-60 s length-test band")
    tail = total - vo_cut

    hook, title, end_title = WORK / "hook.png", WORK / "title.png", WORK / "end_title.png"
    hook_png(hook)
    title_png(title, with_id=False)
    # J2510: remove raw video ID Js6EQJ8qDi8 from the end card
    title_png(end_title, with_id=False)
    caps = caption_track(words, total)

    # Copy locked v01 stems so sfx_kit.py level and gate_shorts_open.py vo_src check run against the exact stems.
    vo_stem = OUT / f"{STEM}_stem_vo.wav"
    sfx_stem = OUT / f"{STEM}_stem_sfx.wav"
    bed_stem = OUT / f"{STEM}_stem_bed.wav"
    shutil.copy2(V01_EXPORT_DIR / "thu12_length_test_dust_v01_stem_vo.wav", vo_stem)
    shutil.copy2(V01_EXPORT_DIR / "thu12_length_test_dust_v01_stem_sfx.wav", sfx_stem)
    shutil.copy2(V01_EXPORT_DIR / "thu12_length_test_dust_v01_stem_bed.wav", bed_stem)

    # Relevel the locked v01 audio mix to the 26 Oct gate (-14.2 LUFS / -2.2 dBTP).
    leveled_wav = WORK / "audio_leveled.wav"
    wav_i, wav_tp = relevel_audio(V01_EXPORT_DIR / "thu12_length_test_dust_v01.mp4", leveled_wav)
    print(f"leveled WAV: {wav_i:.2f} LUFS / {wav_tp:.2f} dBTP", flush=True)

    # Render s02_r20 (PIA17759.jpg, 2.400s -> 6.5333s = 124 frames) to hard-cut at 2.400s and join MASTER at 6.5333s.
    s02_frames = round((S02_JOIN_S - CUT1_S) * FPS)
    s02_mp4 = WORK / "s02_pia17759.mp4"
    render_s02_pia17759(s02_mp4, s02_frames)

    vfade = total - FADE
    title_on = "+".join(f"between(t,{a},{b})" for a, b in TITLE_WINDOWS)
    final = OUT / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{SRC_IN}", "-t", f"{vo_cut:.3f}", "-i", MASTER,
        "-ss", f"{SRC_IN}", "-t", f"{tail:.3f}", "-i", MASTER,
        "-i", hook, "-i", title, "-f", "concat", "-safe", "0", "-i", caps,
        "-loop", "1", "-i", end_title,
        "-i", leveled_wav,
        "-i", s02_mp4,
        "-filter_complex", (
            f"[0:v]setpts=PTS-STARTPTS,split[s1in][s3in];"
            f"[s1in]trim=0:{CUT1_S:.3f},setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,"
            f"scale=w='trunc({W}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':"
            f"h='trunc({H}*(1+{SHOT1_PUSH}*min(t,1.2)/1.2)/2)*2':eval=frame:flags=lanczos,"
            f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1[s1];"
            f"[7:v]setpts=PTS-STARTPTS,setsar=1[s2];"
            f"[s3in]trim={S02_JOIN_S:.6f},setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,"
            f"scale={W}:{H}:flags=lanczos,setsar=1[s3];"
            f"[1:v]setpts=PTS-STARTPTS,crop=608:1080:{CROP_X}:0,scale={W}:{H}:flags=lanczos,setsar=1[s4];"
            f"[s1][s2][s3][s4]concat=n=4:v=1:a=0,fps={FPS},split[b0][bhz];"
            f"[bhz]crop=1080:160:0:0,boxblur=4:36:4:2,format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,(160-Y)/40)'[hz];"
            f"[b0][hz]overlay=0:0:enable='between(t,44.0,49.0)',format=yuv420p[base];"
            f"[base][2:v]overlay=0:0:enable='between(t,0,{HOOK_END})'[v1];"
            f"[v1][3:v]overlay=0:0:enable='{title_on}'[v2a];"
            f"[v2a][5:v]overlay=0:0:enable='gte(t,{last_end:.3f})':shortest=1[v2];"
            f"[4:v]fps={FPS},format=rgba[cp];[v2][cp]overlay=0:0:eof_action=pass,"
            f"fade=t=out:st={vfade:.3f}:d={FADE},format=yuv420p[v]"
        ),
        "-map", "[v]", "-map", "6:a", *shorts_encode_args(fps=FPS),
        "-t", f"{total:.3f}", "-movflags", "+faststart", final,
    ])

    final_i, final_tp = measure_ebur128(final)
    print(f"final MP4 ebur128: {final_i:.2f} LUFS / {final_tp:.2f} dBTP", flush=True)

    # Contact sheets (frames sheet + 2fps full sheet + PHONE preview)
    sheet = OUT / f"{STEM}_frames.jpg"
    times = [0.0, 1.0, 2.5, 5.0, 8.0, 11.0, 16.0, 22.0, 28.0, 34.0, 40.0, 46.0, 52.5, total - 0.9]
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1",
             "-vf", "scale=216:384", p])
        tiles.append(p)
    cols = 7
    canvas = Image.new("RGB", (216 * cols, 404 * 2), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        x, y = 216 * (i % cols), 404 * (i // cols)
        canvas.paste(Image.open(p), (x, y))
        d.text((x + 6, y + 388), f"{t:.1f}s", fill=WHITE)
    canvas.save(sheet, quality=90)

    # Write cuts_v05.json and pool_v05.json
    cuts_v01 = json.loads((OUT / "cuts_v01.json").read_text())
    cuts_v05 = [dict(r) for r in cuts_v01]
    cuts_v05[0]["timeline_out"] = CUT1_S
    cuts_v05[1]["timeline_in"] = CUT1_S
    cuts_v05[1]["framing"] = {"quad": "c"}
    (OUT / "cuts_v05.json").write_text(json.dumps(cuts_v05, indent=2) + "\n")
    shutil.copy2(OUT / "pool_v01.json", OUT / "pool_v05.json")

    meta = {
        "job": "J2510",
        "version": "v05",
        "replaces_for_watch": "thu12_length_test_dust_v01 (scheduled N42gKBbD7tE). v01..v04 untouched.",
        "test": "Short length test, 50-60 s (AGENTS.md -> Packaging 5)",
        "air": AIR,
        "related": LONG_ID,
        "file": str(final.relative_to(REPO)),
        "frames": str(sheet.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "master": {
            "file": "02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/09_Final-Export/025_MarsRobot_full_rough_v03f.mp4",
            "sha256_prefix": MASTER_SHA,
            "from_s": SRC_IN,
            "to_s": VO_CUT_ABS,
            "loop_tail_from_s": SRC_IN,
            "loop_tail_s": round(tail, 3),
        },
        "first_line": "Opportunity should have starved within months.",
        "last_line": "It was the sky turning off.",
        "words": len(words),
        "last_word_end_s": last_end,
        "hold_s": HOLD,
        "fade_s": FADE,
        "first_cut_s": CUT1_S,
        "reframe": (
            f"crop 608x1080 at x={CROP_X}, scale to {W}x{H} (1.78x); opening shot pushed {SHOT1_PUSH:.0%} "
            f"over 1.2 s (1.99x at the end of the push); hard cut at {CUT1_S} s (after 'months.') to "
            "s02_r20 (PIA17759.jpg quad='c' sub-pixel push)"
        ),
        "hook": f"{HOOK[0]} / {HOOK[1]} (yellow {HOOK[1]}), 0-{HOOK_END} s",
        "title_on_screen": LONG_TITLE,
        "title_windows_s": [*TITLE_WINDOWS, (last_end, total)],
        "long_id_on_screen": None,
        "audio": (
            f"locked v01 mix releveled to {final_i:.1f} LUFS / {final_tp:.1f} dBTP "
            "(26 Oct gate: -14.0±0.5 LUFS, <=-1.6 dBTP)"
        ),
        "stems": [vo_stem.name, sfx_stem.name, bed_stem.name],
        "spend": "none (£0 local re-cut)",
        "orbit": "none on screen (no Omni shot in master 254-310 s)",
        "overlay": "none",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
