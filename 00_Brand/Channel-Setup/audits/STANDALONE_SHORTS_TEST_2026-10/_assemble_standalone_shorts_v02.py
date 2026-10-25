#!/usr/bin/env python3
"""J0914 local v02 re-cut of standalone S2 Neptune and S3 ISS. £0. No upload.

Cuts the "Stay, and I'll show you" sentence out of the locked VO, opens on
public-domain moving footage, first cut by 3 s, plates held at most 4 s,
loop crossfade 0.3 s, tail at most 1.5 s. v01 files are not touched.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

RAW = Path("/Volumes/data/mac-mini-archive/scratch/J0914/raw")
WORK = Path("/Volumes/data/mac-mini-archive/scratch/J0914/work")
KIT = Path("/Volumes/data/mac-mini-archive/scratch/J0914/kit")
BED = HERE / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
TRIM = HERE / "vo_v01/trim"
OUT = HERE / "06_Final-Exports"

W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
BAND_TOP = (H - 608) // 2
LINE_H = int(608 * 0.115)
HOOK_END = 2.2
TITLE = (9.0, 14.0)
TAIL = 1.15
XFADE = 0.30
VO_GAIN, BED_GAIN, BED_HOLD = 1.0, 0.065, 0.35

NEP = RAW / "neptune_svs_vert.webm"
ROT = RAW / "neptune_rotating.webm"
ISS = RAW / "iss_sunrise.ogv"


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def fit_font(draw, text, size, max_w, stroke):
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, size)


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    draw.text(((W - (box[2] - box[0])) // 2 - box[0], y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=BLACK)
    return box[3] - box[1]


def excise(words: list[dict], drop_from: str, drop_through: str, breath: float = 0.15, tail: float = 0.05):
    """Drop one sentence and close the join to `breath` seconds. Times stay on the original clock until shifted."""
    i0 = next(i for i, w in enumerate(words) if w["word"].lower().startswith(drop_from.lower()))
    i1 = next(i for i, w in enumerate(words) if i >= i0 and w["word"].lower().startswith(drop_through.lower()))
    prev_end = words[i0 - 1]["end"]
    next_start = words[i1 + 1]["start"]
    seg1_end = round(prev_end + tail, 3)
    target = prev_end + breath
    seg2_start = round(seg1_end + next_start - target, 3)
    removed = round(seg2_start - seg1_end, 3)
    kept = []
    for w in words[:i0]:
        kept.append({"word": w["word"], "start": w["start"], "end": w["end"]})
    for w in words[i1 + 1:]:
        kept.append({"word": w["word"], "start": round(w["start"] - removed, 3), "end": round(w["end"] - removed, 3)})
    gap = round(kept[i0]["start"] - kept[i0 - 1]["end"], 3)
    if gap > breath + 0.02:
        raise SystemExit(f"breath {gap}s is over {breath}s")
    return seg1_end, seg2_start, kept


def cut_vo(src: Path, words: list[dict], seg1: float, seg2: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex",
         f"[0:a]atrim=0:{seg1},asetpts=PTS-STARTPTS[a];"
         f"[0:a]atrim={seg2},asetpts=PTS-STARTPTS[b];"
         f"[a][b]concat=n=2:v=0:a=1[aout]",
         "-map", "[aout]", "-ac", "2", "-ar", "48000", out])


def spans(first: float, last_end: float, hold: float = 3.7) -> list[tuple[float, float]]:
    """Plate windows. First cut at `first` (<=3 s). Later holds <= 4 s. Picture runs TAIL past the last word."""
    end = last_end + XFADE + 0.08  # xfade must finish inside the main, not on its last frame
    starts = [0.0, first]
    t = first + hold
    while t < end - 1.3:
        starts.append(round(t, 3))
        t += hold
    bounds = starts + [round(end, 3)]
    out = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    for a, b in out:
        if b - a > 4.01:
            raise SystemExit(f"plate {a}-{b} held {b - a:.2f}s")
    if out[0][1] > 3.0:
        raise SystemExit("first cut after 3 s")
    return out


def encode(src: Path, ss: float, in_dur: float, fc: str, frames: int, out: Path) -> None:
    if out.exists() and out.stat().st_size > 100000:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{in_dur:.3f}", "-i", src,
         "-filter_complex", fc, "-map", "[v]", "-frames:v", str(frames),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", out])


def opening_nep(dur_s: float, out: Path) -> None:
    frames = round(dur_s * FPS)
    fc = ("[0:v]crop=800:1200:140:160,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "eq=saturation=1.22:contrast=1.05,fps=30,format=yuv420p[v]")
    encode(NEP, 0.20, dur_s, fc, frames, out)


def rot_seg(ss: float, dur_s: float, speed: float, out: Path) -> None:
    frames = round(dur_s * FPS)
    # Crop inside the disc so the frame is cloud, not a square pasted on black (that seam fails polish).
    fc = (f"[0:v]setpts=PTS/{speed},crop=220:220:526:250,"
          "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "eq=saturation=1.4:contrast=1.12:brightness=0.02,unsharp=5:5:0.6,fps=30,format=yuv420p[v]")
    encode(ROT, ss, dur_s * speed, fc, frames, out)


def limb_seg(ss: float, dur_s: float, speed: float, out: Path) -> None:
    """Second plate: the disc's top limb in the centre band.

    An inside-the-disc crop matches the opening clouds, so scdet (threshold 10)
    reports no cut. This crop was measured on Neptune Rotating at t=18 s:
    score about 19.6 at the join. The limb is curved, so it is not a straight seam.
    """
    frames = round(dur_s * FPS)
    fc = (f"[0:v]setpts=PTS/{speed},crop=180:320:548:100,"
          "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "eq=saturation=1.35:contrast=1.1:brightness=0.04,unsharp=5:5:0.45,fps=30,format=yuv420p[v]")
    encode(ROT, ss, dur_s * speed, fc, frames, out)


def iss_seg(ss: float, dur_s: float, out: Path) -> None:
    frames = round(dur_s * FPS)
    # A few degrees of roll so the limb is not a straight full-width seam (polish_gate).
    fc = ("[0:v]crop=420:720:860:0,rotate=0.16:c=none:ow=rotw(0.16):oh=roth(0.16),"
          "crop=in_w*0.82:in_h*0.82,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "eq=saturation=1.2:contrast=1.06,fps=30,format=yuv420p[v]")
    encode(ISS, ss, dur_s, fc, frames, out)


def concat(parts: list[Path], out: Path) -> None:
    if out.exists() and out.stat().st_size > 100000:
        return
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    fc = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", out])


def looped(main: Path, opening: Path, last_end: float, out: Path) -> None:
    """0.3 s crossfade from the end of the body into a reverse of the opening, landing on frame 0."""
    rev = out.with_name("rev.mp4")
    frames = round(TAIL * FPS)
    run(["ffmpeg", "-y", "-v", "error", "-i", opening, "-vf",
         f"trim=0:{TAIL},setpts=PTS-STARTPTS,reverse,fps=30,format=yuv420p",
         "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", rev])
    run(["ffmpeg", "-y", "-v", "error", "-i", main, "-i", rev, "-filter_complex",
         f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={last_end:.3f},"
         f"noise=alls=4:allf=t,fps=30,format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", out])


def hook_png(spec) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lines = [" ".join(row) for row in spec["hook"]]
    font = fit_font(d, max(lines, key=len), 168, int(W * 0.86), 8)
    y = int(H * 0.055)
    for words in spec["hook"]:
        widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in words]
        space = d.textlength(" ", font=font)
        total = sum(b[2] - b[0] for b in widths) + space * (len(words) - 1)
        x = (W - total) / 2
        for w, b in zip(words, widths):
            d.text((x - b[0], y), w, font=font, fill=YELLOW if w == spec["yellow"] else WHITE,
                   stroke_width=8, stroke_fill=BLACK)
            x += b[2] - b[0] + space
        y += max(b[3] - b[1] for b in widths) + 18
    return im


def title_png(spec) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, max(spec["title"], key=len), 78, int(W * 0.88), 5)
    y = int(H * 0.09)
    for row in spec["title"]:
        y += centred(d, y, row, font, WHITE, 5) + 14
    return im


def caption_pngs(words, total) -> list[tuple[float, float, Image.Image]]:
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.45)
        text = " ".join(w["word"] for w in g).upper().replace(".", "").replace(",", "")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.78), text, fit_font(d, text, 72, int(W * 0.90), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def bars_clip(window, out: Path) -> None:
    a0, a1 = window
    n = max(1, round((a1 - a0) * FPS))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rows = (("EARTH 400", 0.20, WHITE), ("NEPTUNE 2,000", 1.0, YELLOW))
    for i in range(n):
        t = a0 + i / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = min(ease((t - a0) / 0.35), ease((a1 - t) / 0.30))
        y = BAND_TOP + 80
        x0, full = int(W * 0.10), int(W * 0.80)
        for k, (label, frac, col) in enumerate(rows):
            font = fit_font(d, label, LINE_H, int(W * 0.84), 5)
            box = d.textbbox((0, 0), label, font=font, stroke_width=5)
            d.text((x0 - box[0], y), label, font=font, fill=col, stroke_width=5, stroke_fill=BLACK)
            y += box[3] - box[1] + 14
            g = ease((t - a0 - (0.25 if k == 0 else 0.7)) / 1.1)
            d.rounded_rectangle((x0, y, x0 + full, y + 36), radius=18, fill=(0, 0, 0, 130), outline=WHITE, width=3)
            d.rounded_rectangle((x0 + 6, y + 6, x0 + 6 + max(4, int((full - 12) * frac * g)), y + 30),
                                radius=12, fill=col)
            y += 36 + 36
        if alpha < 1:
            im.putalpha(Image.eval(im.getchannel("A"), lambda v, a=alpha: int(v * a)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("bars encode failed")


def counter_clip(window, out: Path) -> None:
    a0, a1 = window
    n = max(1, round((a1 - a0) * FPS))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = a0 + i / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = min(ease((t - a0) / 0.35), ease((a1 - t) / 0.30))
        k = ease((t - a0 - 0.15) / 2.4)
        num = max(1, min(16, 1 + int(15 * k)))
        y = BAND_TOP + 70
        big = fit_font(d, "16", LINE_H + 80, int(W * 0.6), 8)
        y += centred(d, y, str(num), big, YELLOW, 8) + 20
        small = fit_font(d, "EVERY 90 MINUTES", LINE_H, int(W * 0.86), 5)
        centred(d, y, "EVERY 90 MINUTES", small, WHITE, 5)
        if alpha < 1:
            im.putalpha(Image.eval(im.getchannel("A"), lambda v, a=alpha: int(v * a)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("counter encode failed")


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def composite(picture: Path, overlays: list[tuple[Path, float, float]], out: Path) -> None:
    frames = round(dur(picture) * FPS)
    inputs: list[str] = ["-i", str(picture)]
    for p, _, _ in overlays:
        if p.suffix == ".png":
            inputs += ["-loop", "1", "-framerate", str(FPS), "-i", str(p)]
        else:
            inputs += ["-i", str(p)]
    parts, prev = [], "[0:v]"
    for i, (p, a, b) in enumerate(overlays, start=1):
        tag = f"[v{i}]"
        if p.suffix == ".mov":
            parts.append(
                f"[{i}:v]setpts=PTS+{a:.3f}/TB[d{i}];{prev}[d{i}]overlay=enable='between(t,{a:.3f},{b:.3f})'{tag}"
            )
        else:
            parts.append(f"{prev}[{i}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'{tag}")
        prev = tag
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(parts), "-map", prev,
         "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", out])


def mix(picture, vo, bed_stem, sfx_stem, total, out) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-i", picture, "-i", vo, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
                            "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", out])


def stems(work, vo, total, last_end, tick_at, sfx_gain) -> tuple[Path, Path, Path]:
    vo_s, bed_s, sfx_s = work / "stem_vo.wav", work / "stem_bed.wav", work / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-af",
         f"aresample=48000,volume={VO_GAIN},apad,atrim=0:{total}", "-ac", "2", vo_s])
    ramp = f"if(lt(t,{last_end}),{BED_GAIN},{BED_GAIN}+({BED_HOLD}-{BED_GAIN})*min((t-{last_end})/0.6,1))"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total},volume='{ramp}':eval=frame,afade=t=in:st=0:d=0.25,"
         f"afade=t=out:st={total - 0.45:.3f}:d=0.45", "-ac", "2", bed_s])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", whoosh, "-i", tick, "-filter_complex",
         f"[0:a]aresample=48000,volume={sfx_gain},afade=t=out:st=1.2:d=0.5,atrim=0:1.8[s0];"
         f"[1:a]aresample=48000,volume=0.28,adelay={int(tick_at * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_s])
    return vo_s, bed_s, sfx_s


def sheet(final: Path, times: list[float], out: Path) -> None:
    tiles = []
    total = dur(final)
    times = sorted({round(min(t, total - 0.08), 2) for t in times})
    for i, t in enumerate(times):
        p = out.with_name(f"_tile_{i}.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-vf", "scale=216:384", p])
        tiles.append((p, t))
    canvas = Image.new("RGB", (216 * len(tiles), 408), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 22)
    for i, (p, t) in enumerate(tiles):
        canvas.paste(Image.open(p), (216 * i, 0))
        d.text((216 * i + 6, 386), f"{t:.1f}s", fill=(255, 255, 255), font=font)
        p.unlink()
    canvas.save(out, quality=88)


def build(key: str) -> dict:
    spec = SPECS[key]
    work = WORK / spec["stem"]
    work.mkdir(parents=True, exist_ok=True)
    src_vo = TRIM / f"{spec['vo']}_trim.wav"
    src_words = json.loads((TRIM / f"{spec['vo']}_trim_words.json").read_text())["words"]
    seg1, seg2, words = excise(src_words, "Stay", spec["drop_through"])
    vo = work / "vo_v02.wav"
    cut_vo(src_vo, src_words, seg1, seg2, vo)
    last_end = words[-1]["end"]
    total = round(last_end + TAIL, 3)
    windows = spans(spec["first"], last_end, spec["hold"])
    print(key, "words", len(words), "last", last_end, "total", total, "cuts", windows, flush=True)

    parts = []
    cuts = []
    speed = 2.5
    for i, (a, b) in enumerate(windows):
        part = work / f"seg_{i:02d}.mp4"
        length = round(b - a, 3)
        if key == "s2" and i == 0:
            opening_nep(length, part)
            src = f"SVS 14397 Neptune close-up t=0.20+{length:.2f}s crop 800x1200"
            zoom = "cover into cloud deck, about 1.5x"
        elif key == "s2" and i == 1:
            ss = 18.0
            limb_seg(ss, length, speed, part)
            src = f"Neptune Rotating.webm t={ss:.2f}s limb crop 180x320"
            zoom = "top limb in the centre band, cover to 1080x1920"
        elif key == "s2":
            ss = 12.0 + (a - windows[0][1]) * speed
            rot_seg(ss, length, speed, part)
            src = f"Neptune Rotating.webm t={ss:.2f}s at {speed}x, disc centred"
            zoom = "inside the disc, cover to 1080x1920 (about 5x; source disc is ~400 px)"
        else:
            ss = 5.0 + i * 9.0
            iss_seg(ss, length, part)
            src = f"Sunrise To Sunset Aboard The ISS.ogv t={ss:.2f}s earth-limb crop"
            zoom = "earth-limb crop, rolled about 9 degrees, cover to 1080x1920"
        parts.append(part)
        cuts.append({"row": i + 1, "timeline_in": a, "timeline_out": round(b, 3), "source": src,
                     "framing": {"offset": round(b - a, 3)}, "zoom": zoom})

    main = work / "main.mp4"
    concat(parts, main)
    base = work / "picture.mp4"
    looped(main, parts[0], last_end, base)
    total = round(dur(base), 3)
    gap = round(total - last_end, 3)
    if gap > 1.5:
        raise SystemExit(f"tail {gap}s is over 1.5s")
    print(key, "picture", total, "tail", gap, flush=True)

    ov_dir = work / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    save_png(hook_png(spec), hook_p)
    save_png(title_png(spec), title_p)
    overlays = [(hook_p, 0.0, HOOK_END), (title_p, TITLE[0], TITLE[1])]
    for i, (a, b, im) in enumerate(caption_pngs(words, total)):
        p = ov_dir / f"cap_{i:02d}.png"
        save_png(im, p)
        overlays.append((p, a, b))
    ov = spec["overlay"]
    data = ov_dir / "data.mov"
    if ov["kind"] == "bars":
        bars_clip(ov["window"], data)
    else:
        counter_clip(ov["window"], data)
    overlays.append((data, ov["window"][0], ov["window"][1]))

    comp = work / "comp.mp4"
    composite(base, overlays, comp)
    vo_s, bed_s, sfx_s = stems(work, vo, total, last_end, ov["window"][0] + 0.05, spec["sfx_gain"])
    final = OUT / f"{spec['stem']}_v02.mp4"
    OUT.mkdir(exist_ok=True)
    mix(comp, vo_s, bed_s, sfx_s, total, final)

    frames = OUT / f"{spec['stem']}_v02_frames.jpg"
    mids = [ (c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts ]
    sheet(final, [0.0, 0.5, 1.2, windows[0][1] + 0.15, 11.5, sum(ov["window"]) / 2, last_end, total - 0.08] + mids, frames)

    surprise = next(w for w in words if w["word"].lower().startswith(spec["surprise"]))
    brief = {
        "frame0_source": cuts[0]["source"],
        "frame0_zoom": cuts[0]["zoom"],
        "first_word_onset_s": words[0]["start"],
        "surprise_word": surprise["word"],
        "surprise_word_s": surprise["start"],
        "first_cut_s": windows[0][1],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": "no",
        "longest_plate_s": round(max(b - a for a, b in windows), 3),
        "loop_sentence": spec["loop"],
    }
    meta = {
        "job": "J0914", "short": key, "version": "v02",
        "air_date": spec["air"], "youtube_id": spec["id"],
        "title_on_screen": " ".join(spec["title"]),
        "file": str(final.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "duration_s": round(dur(final), 3),
        "vo": str(vo),
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": " ".join(w["word"] for w in words),
        "captions": words,
        "hook": " / ".join(" ".join(r) for r in spec["hook"]) + f" (yellow {spec['yellow']}), 0-{HOOK_END} s",
        "title_window_s": list(TITLE),
        "overlay": ov,
        "cuts": cuts,
        "brief": brief,
        "audio": {
            "bed": str(BED.relative_to(REPO)),
            "sfx": f"sfx_owb_whoosh_soft_v01.wav at 0 s, tick at {ov['window'][0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14 LUFS, -1.5 dBTP",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "sources": spec["sources"],
    }
    meta_path = OUT / f"{spec['stem']}_v02_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", spec["air"], "--id", spec["id"]],
                          capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_s), "--sfx", str(sfx_s), "--bed", str(bed_s),
                            "--minutes", f"{total / 60:.4f}"], capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_sfx_level.txt").write_text(level.stdout + level.stderr)
    polish_cuts = work / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run([sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
                             "--cuts", str(polish_cuts), "--out", str(work / "polish_gate.json")],
                            capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_polish.txt").write_text(polish.stdout + polish.stderr)
    music = subprocess.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(HERE),
                            "--bed", str(BED), "--video", str(final),
                            "--out", str(work / "music_gate.json")],
                           capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_music_gate.txt").write_text(music.stdout + music.stderr)
    print(f"== {key} gate={gate.returncode} level={level.returncode} polish={polish.returncode} music={music.returncode}")
    print(gate.stdout)
    print(level.stdout[-600:])
    print(polish.stdout[-800:])
    print(music.stdout[-800:])
    return {"gate": gate.returncode, "level": level.returncode, "polish": polish.returncode,
            "music": music.returncode, "brief": brief, "spoken": meta["spoken"]}


SPECS = {
    "s2": {
        "stem": "owb_sa_s2_neptune", "id": "oyRcrFTYyDY", "vo": "owb_sa_s2_neptune_vo_v01",
        "air": "2026-10-27", "drop_through": "fast", "surprise": "supersonic",
        "first": 1.95, "hold": 3.55, "sfx_gain": 0.20,
        "title": ("The Wind on Neptune", "Is Supersonic"),
        "hook": (("SUPERSONIC",), ("WIND",)), "yellow": "SUPERSONIC",
        "overlay": {"kind": "bars", "window": (6.45, 8.90),
                    "spoken": "over two thousand kilometres an hour"},
        "loop": "And still. The wind on Neptune is supersonic.",
        "sources": "Frame 0: NASA SVS 14397 (Neptune's disappearing clouds), public domain, cropped to the cloud deck. "
                   "First cut: Wikimedia Neptune Rotating.webm top-limb crop (public domain). "
                   "Later plates: the same rotation, inside the disc, 2.5x.",
    },
    "s3": {
        "stem": "owb_sa_s3_iss_sunrises", "id": "XKlq0TK1OVA", "vo": "owb_sa_s3_iss_sunrises_vo_v01",
        "air": "2026-10-31", "drop_through": "one", "surprise": "16",
        "first": 2.45, "hold": 3.65, "sfx_gain": 0.16,
        "title": ("Astronauts See 16", "Sunrises Every Day"),
        "hook": (("16", "SUNRISES"), ("A", "DAY")), "yellow": "16",
        "overlay": {"kind": "counter", "to": 16, "label": "EVERY 90 MINUTES", "window": (15.35, 19.15),
                    "spoken": "16 sunrises, 16 sunsets"},
        "loop": "Up here, morning never keeps you waiting. Astronauts see 16 sunrises every day.",
        "sources": "NASA public-domain 'Sunrise To Sunset Aboard The ISS' (Wikimedia), earth-limb crop. "
                   "Shuttle structure is outside the crop. No new picture generation.",
    },
}


def main() -> None:
    keys = sys.argv[1:] or ["s2", "s3"]
    for p in (BED, KIT / "sfx_owb_whoosh_soft_v01.wav", NEP, ROT, ISS):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    results = {k: build(k) for k in keys}
    print(json.dumps(results, indent=2, default=str))
    if any(v["gate"] or v["level"] or v["polish"] or v["music"] for v in results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
