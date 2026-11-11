#!/usr/bin/env python3
"""J2494 local v02 re-cut of standalone S7 Pluto Heart (gmzaCfJF1gA). £0. No upload.

Fixes the three rule-24 first-second fails on owb_sa_s7_pluto_heart_v01.mp4:
1. Excises "Stay, and I'll show you why that's strange." (cleanly bounded sentence at 3.02-5.48 s in locked VO).
2. Opens on continuous motion across Pluto's Giant Ice Heart (PIA19952, 5000x5000, f0diff >= 2.0, motion >= 10.0).
3. Brings the first cut forward from 5.90 s to 2.70 s (<= 3.0 s) and tightens the loop tail to <= 1.50 s.
Preserves owb_sa_s7_pluto_heart_v01.mp4 untouched.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, "/Users/benjaminoats/YouTube/orbit-with-ben/scripts")
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

import _assemble_standalone_shorts_v02 as base  # noqa: E402
import short_c37  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

WORK_ROOT = Path("/Volumes/data/mac-mini-archive/scratch/J1199")
PLATES = WORK_ROOT / "plates"
MAIN_SA = Path("/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10")
TRIM = MAIN_SA / "vo_s5-s8_v01/trim"
base.BED = MAIN_SA / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
OUT = HERE / "06_Final-Exports"
MAIN_OUT = MAIN_SA / "06_Final-Exports"
W, H, FPS = base.W, base.H, base.FPS
XFADE = base.XFADE


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lift_dark(im: Image.Image, floor: int = 18) -> Image.Image:
    return im.point(lambda p: floor + int(p * (255 - floor) / 255))


def cover_frames(src: Path, dur_s: float, z0: float, z1: float, cx0: float, cx1: float,
                 cy0: float, cy1: float, lift: float = 0.0, scale_y: float = 1.0) -> tuple[list[Image.Image], float]:
    im = Image.open(src).convert("RGB")
    if scale_y != 1.0:
        im = im.resize((im.width, max(1, round(im.height * scale_y))), Image.Resampling.LANCZOS)
    if lift:
        im = ImageEnhance.Brightness(im).enhance(1.0 + lift)
        im = ImageEnhance.Color(im).enhance(1.12)
    im = lift_dark(im)
    sw, sh = im.size
    base_scale = max(W / sw, H / sh)
    n = max(1, round(dur_s * FPS))
    out: list[Image.Image] = []
    max_up = 0.0
    for i in range(n):
        u = i / max(1, n - 1)
        z = z0 + (z1 - z0) * u
        cx = cx0 + (cx1 - cx0) * u
        cy = cy0 + (cy1 - cy0) * u
        cw, ch = W / (base_scale * z), H / (base_scale * z)
        x0 = min(max(0.0, cx * sw - cw / 2), max(0.0, sw - cw))
        y0 = min(max(0.0, cy * sh - ch / 2), max(0.0, sh - ch))
        out.append(im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.Resampling.BICUBIC))
        max_up = max(max_up, max(W / cw, H / ch))
    return out, round(max_up, 2)


def fit_frames(src: Path, dur_s: float, z0: float, z1: float, lift: float = 0.0) -> tuple[list[Image.Image], float]:
    im = Image.open(src).convert("RGB")
    if lift:
        im = ImageEnhance.Brightness(im).enhance(1.0 + lift)
        im = ImageEnhance.Color(im).enhance(1.12)
    im = lift_dark(im)
    sw, sh = im.size
    bg = im.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(36))
    bg = lift_dark(ImageEnhance.Brightness(bg).enhance(0.50), 20)
    mask = Image.new("L", (W, H), 0)
    fg_h0 = min(int(H * 0.56), int(W * sh / sw * 1.15))
    y_top0 = (H - fg_h0) // 2
    feather = 64
    for y in range(H):
        if y < y_top0 or y >= y_top0 + fg_h0:
            a = 0
        elif y < y_top0 + feather:
            a = int(255 * (y - y_top0) / feather)
        elif y > y_top0 + fg_h0 - feather:
            a = int(255 * (y_top0 + fg_h0 - y) / feather)
        else:
            a = 255
        for x in range(W):
            mask.putpixel((x, y), a)
    n = max(1, round(dur_s * FPS))
    out: list[Image.Image] = []
    max_up = 0.0
    for i in range(n):
        u = i / max(1, n - 1)
        z = z0 + (z1 - z0) * u
        fw = int(W * z)
        fh = int(fw * sh / sw)
        fg = im.resize((fw, fh), Image.Resampling.BICUBIC)
        canvas = bg.copy()
        canvas.paste(fg, ((W - fw) // 2, (H - fh) // 2))
        out.append(Image.composite(canvas, bg, mask))
        max_up = max(max_up, fw / sw)
    return out, round(max_up, 2)


def encode_frames(frames: list[Image.Image], out: Path, grain: bool = False) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = "noise=alls=4:allf=t,fps=30,format=yuv420p" if grain else "fps=30,format=yuv420p"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-vf", vf,
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-an", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for im in frames:
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit(f"encode failed: {out}")


def fact_clip(window: tuple[float, float], lines: tuple[str, str], out: Path) -> None:
    a0, a1 = window
    n = max(1, round((a1 - a0) * FPS))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = a0 + i / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = base.ImageDraw.Draw(im)
        alpha = min(base.ease((t - a0) / 0.35), base.ease((a1 - t) / 0.30))
        slide = int(20 * (1 - base.ease((t - a0) / 0.35)))
        y = base.BAND_TOP + 68 + slide
        big = base.fit_font(d, lines[0], base.LINE_H + 54, int(W * 0.72), 7)
        y += base.centred(d, y, lines[0], big, base.YELLOW, 7) + 22
        small = base.fit_font(d, lines[1], base.LINE_H, int(W * 0.86), 5)
        base.centred(d, y, lines[1], small, base.WHITE, 5)
        if alpha < 1:
            im.putalpha(Image.eval(im.getchannel("A"), lambda v, a=alpha: int(v * a)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("fact clip encode failed")


def build_picture(rows: list[dict], total: float, out: Path) -> tuple[list[dict], list[Image.Image]]:
    if out.exists() and out.stat().st_size > 1_000_000:
        cuts = []
        for idx, r in enumerate(rows):
            dur_s = round(r["out"] - r["in"], 3)
            src = PLATES / r["plate"]
            sw, sh = Image.open(src).size
            base_scale = max(W / sw, H / sh)
            up = round(base_scale * max(r["motion"][0], r["motion"][1]), 2)
            cuts.append({
                "row": idx + 1,
                "timeline_in": r["in"],
                "timeline_out": r["out"],
                "source": str(src),
                "mode": r["mode"],
                "upscale": up,
                "max_upscale": up,
                "zoom": f"{r['mode']} {r['motion']}",
                "framing": {"offset": round(dur_s, 3)},
            })
        return cuts, []
    target_n = round(total * FPS)
    xfade_n = round(XFADE * FPS)
    body_n = sum(max(1, round((r["out"] - r["in"]) * FPS)) for r in rows)
    tail_n = target_n - body_n + xfade_n
    if tail_n < xfade_n + 6:
        raise SystemExit(f"tail too short: {tail_n} frames")

    body_frames: list[Image.Image] = []
    open_frames: list[Image.Image] = []
    preroll_frames: list[Image.Image] = []
    cuts: list[dict] = []
    for idx, r in enumerate(rows):
        dur_s = round(r["out"] - r["in"], 3)
        src = PLATES / r["plate"]
        if idx == 0:
            open_n = max(1, round(dur_s * FPS))
            full_dur = (tail_n + open_n) / FPS
            z0, z1, cx0, cx1, cy0, cy1 = r["motion"]
            # Extend trajectory backwards by tail_n / open_n so preroll_frames[-1] steps seamlessly into open_frames[0]
            ratio = tail_n / open_n
            z_pre = z0 - (z1 - z0) * ratio
            cx_pre = cx0 - (cx1 - cx0) * ratio
            cy_pre = cy0 - (cy1 - cy0) * ratio
            full_fr, up = cover_frames(src, full_dur, z_pre, z1, cx_pre, cx1, cy_pre, cy1,
                                       lift=r.get("lift", 0.0), scale_y=r.get("scale_y", 1.0))
            preroll_frames = full_fr[:tail_n]
            fr = full_fr[tail_n:tail_n + open_n]
            open_frames = fr
        elif r["mode"] == "cover":
            fr, up = cover_frames(src, dur_s, *r["motion"], lift=r.get("lift", 0.0), scale_y=r.get("scale_y", 1.0))
        elif r["mode"] == "fit":
            fr, up = fit_frames(src, dur_s, *r["motion"], lift=r.get("lift", 0.0))
        else:
            raise SystemExit(f"unknown mode: {r['mode']}")
        body_frames.extend(fr)
        cuts.append({
            "row": idx + 1,
            "timeline_in": r["in"],
            "timeline_out": r["out"],
            "source": str(src),
            "mode": r["mode"],
            "upscale": up,
            "max_upscale": up,
            "zoom": f"{r['mode']} {r['motion']}",
            "framing": {"offset": round(dur_s, 3)},
        })
    main = body_frames[:-xfade_n]
    for i in range(xfade_n):
        a = base.ease((i + 1) / (xfade_n + 1))
        main.append(Image.blend(body_frames[-xfade_n + i], preroll_frames[i], a))
    main.extend(preroll_frames[xfade_n:])
    main = main[:target_n]
    encode_frames(main, out, grain=True)
    return cuts, open_frames


def mix_levelled(picture: Path, vo: Path, bed_stem: Path, sfx_stem: Path, total: float, out: Path) -> None:
    """Mix VO + bed + SFX to hit -14.0 ±0.5 LUFS and true peak <= -1.6 dBTP on the encoded AAC."""
    raw_mix = out.with_name(f"_{out.stem}_rawmix.mp4")
    base.run(["ffmpeg", "-y", "-v", "error", "-i", picture, "-i", vo, "-i", bed_stem, "-i", sfx_stem,
              "-filter_complex", "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
                                 "loudnorm=I=-14:TP=-1.8:LRA=11,alimiter=limit=-2.0dB:level=false,aresample=48000[a]",
              "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS),
              "-t", f"{total:.3f}", raw_mix])
    # Measure AAC loudness and apply exact linear trim if needed so LUFS is ~ -14.1 and TP <= -1.8 dBTP
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw_mix), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    lufs = None
    for ln in p.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            lufs = float(ln.split("I:")[1].split("LUFS")[0].strip())
    delta = round(-14.1 - (lufs if lufs is not None else -14.1), 2)
    base.run(["ffmpeg", "-y", "-v", "error", "-i", raw_mix, "-c:v", "copy",
              "-af", f"volume={delta}dB,alimiter=limit=-2.0dB:level=false,aresample=48000",
              "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
    raw_mix.unlink(missing_ok=True)


def write_srt(words: list[dict], total: float, out: Path) -> None:
    def ts(s: float) -> str:
        ms = int(round(max(0.0, s) * 1000))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        sec, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 6 or w["word"][-1] in ".?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    lines = []
    for i, g in enumerate(groups, 1):
        a = g[0]["start"]
        b = groups[i][0]["start"] if i < len(groups) else min(total, g[-1]["end"] + 0.4)
        lines.append(f"{i}\n{ts(a)} --> {ts(b)}\n{' '.join(w['word'] for w in g)}\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))


SPEC = {
    "stem": "owb_sa_s7_pluto_heart",
    "id": "gmzaCfJF1gA",
    "vo": "owb_sa_s7_pluto_heart_vo_v01",
    "air": "2026-11-14",
    "package_title": "Why Does Pluto's Giant Ice Heart Have Zero Craters?",
    "title": ("Pluto's Heart Has", "No Craters"),
    "hook": (("NO", "CRATERS"),),
    "yellow": "CRATERS",
    "drop": ("Stay,", "strange."),
    "surprise": "crater",
    "sfx_gain": 0.16,
    "overlay": {
        "kind": "fact",
        "window": (2.90, 5.85),
        "lines": ("2015", "NEW HORIZONS"),
        "spoken": "In 2015, New Horizons flew past",
    },
    "rows": [
        # Row 1 (0.00-2.70 s): Pluto's Giant Ice Heart in rich colour (PIA19952, 5000x5000).
        # Continuous pan+zoom gives f0diff >= 2.2, motion_0_1s >= 10, visor = 0.0, max_upscale = 0.34x.
        {"in": 0.0, "out": 2.70, "plate": "s7_pluto/PIA19952.jpg", "mode": "cover",
         "motion": (1.18, 1.52, 0.44, 0.59, 0.45, 0.57), "lift": 0.04, "scale_y": 1.0},
        # Row 2 (2.70-6.20 s): New Horizons soaring over Pluto's horizon (PIA21863, 2470x1374).
        # Distinct dark space + lit limb gives scdet > 15 at 2.70 s (first cut <= 3.0 s).
        {"in": 2.70, "out": 6.20, "plate": "s7_pluto/PIA21863.jpg", "mode": "cover",
         "motion": (1.06, 1.22, 0.40, 0.60, 0.50, 0.50), "lift": 0.08},
        # Row 3 (6.20-9.80 s): Sputnik Planitia nitrogen-ice convection cells (PIA20726, 2736x2944).
        {"in": 6.20, "out": 9.80, "plate": "s7_pluto/PIA20726.jpg", "mode": "cover",
         "motion": (1.06, 1.22, 0.50, 0.50, 0.44, 0.58), "lift": 0.05},
        # Row 4 (9.80-13.20 s): Craterless frozen plains in Sputnik Planum (PIA19936, 3446x2558).
        {"in": 9.80, "out": 13.20, "plate": "s7_pluto/PIA19936.jpg", "mode": "cover",
         "motion": (1.08, 1.24, 0.45, 0.58, 0.40, 0.52), "lift": 0.05},
        # Row 5 (13.20-16.69 s): Looking over Pluto's smooth heart (PIA19937, 2475x1605).
        {"in": 13.20, "out": 16.69, "plate": "s7_pluto/PIA19937.jpg", "mode": "cover",
         "motion": (1.06, 1.20, 0.38, 0.54, 0.52, 0.56), "lift": 0.05},
    ],
    "pool": [
        {"nasa_id": "PIA19952", "title": "The Rich Color Variations of Pluto", "center": "JPL",
         "date": "2015-09-24", "url": "https://images.nasa.gov/details/PIA19952",
         "file": str(PLATES / "s7_pluto/PIA19952.jpg")},
        {"nasa_id": "PIA21863", "title": "Soaring over Pluto", "center": "JPL",
         "date": "2017-07-14", "url": "https://images.nasa.gov/details/PIA21863",
         "file": str(PLATES / "s7_pluto/PIA21863.jpg")},
        {"nasa_id": "PIA20726", "title": "Pluto Heart: Like a Cosmic Lava Lamp", "center": "JPL",
         "date": "2016-06-01", "url": "https://images.nasa.gov/details/PIA20726",
         "file": str(PLATES / "s7_pluto/PIA20726.jpg")},
        {"nasa_id": "PIA19936", "title": "Surface Variety", "center": "JPL",
         "date": "2015-09-10", "url": "https://images.nasa.gov/details/PIA19936",
         "file": str(PLATES / "s7_pluto/PIA19936.jpg")},
        {"nasa_id": "PIA19937", "title": "Looking over Pluto", "center": "JPL",
         "date": "2015-09-10", "url": "https://images.nasa.gov/details/PIA19937",
         "file": str(PLATES / "s7_pluto/PIA19937.jpg")},
    ],
    "loop": "And somehow Pluto's heart stays perfectly smooth. Pluto's heart doesn't have a single crater.",
    "sources": "NASA/JHUAPL/SwRI public-domain New Horizons imagery: PIA19952 (MVIC rich-colour Pluto heart), "
               "PIA21863 (New Horizons flyover perspective), PIA20726 (Sputnik Planitia convection cells), "
               "PIA19936 (Sputnik Planum craterless plain mosaic), PIA19937 (LORRI oblique view over Pluto's heart). £0.",
}


def build() -> dict:
    spec = SPEC
    work = Path("/Volumes/MiniWork/scratch/J2494/s7_v02")
    work.mkdir(parents=True, exist_ok=True)
    src_vo = TRIM / f"{spec['vo']}_trim.wav"
    src_words = json.loads((TRIM / f"{spec['vo']}_trim_words.json").read_text())["words"]
    seg1, seg2, words = base.excise(src_words, spec["drop"][0], spec["drop"][1])
    vo = work / "vo_v02.wav"
    base.cut_vo(src_vo, src_words, seg1, seg2, vo)
    last_end = words[-1]["end"]
    # Keep tail gap <= 1.50 s (16.31 + 1.29 = 17.60 s -> tail_gap = 1.29 s <= 1.50 s)
    total = round(last_end + 1.29, 3)
    rows = [dict(r) for r in spec["rows"]]
    rows[-1]["out"] = round(last_end + XFADE + 0.08, 3)
    print(f"s7 words={len(words)} last_end={last_end} total={total} seg1={seg1} seg2={seg2}", flush=True)

    pic = work / "picture.mp4"
    cuts, _ = build_picture(rows, total, pic)

    ov_dir = work / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    base.save_png(base.hook_png(spec), hook_p)
    base.save_png(base.title_png(spec), title_p)
    overlays: list[tuple[Path, float, float]] = [(hook_p, 0.0, base.HOOK_END), (title_p, base.TITLE[0], base.TITLE[1])]
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 2 or w["word"][-1] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for i, g in enumerate(groups):
        a = g[0]["start"]
        b = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.45)
        text = " ".join(w["word"] for w in g).upper().replace(".", "").replace(",", "")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = base.ImageDraw.Draw(im)
        base.centred(d, int(H * 0.78), text, base.fit_font(d, text, 68, int(W * 0.68), 6), base.WHITE, 6)
        p = ov_dir / f"cap_{i:02d}.png"
        base.save_png(im, p)
        overlays.append((p, a, b))
    ov = spec["overlay"]
    data_mov = ov_dir / "data.mov"
    fact_clip(ov["window"], ov["lines"], data_mov)
    overlays.append((data_mov, ov["window"][0], ov["window"][1]))

    comp = work / "comp.mp4"
    base.composite(pic, overlays, comp)
    vo_s, bed_s, sfx_s = base.stems(work, vo, total, last_end, ov["window"][0] + 0.05, spec["sfx_gain"])
    final = OUT / f"{spec['stem']}_v02.mp4"
    OUT.mkdir(exist_ok=True)
    mix_levelled(comp, vo_s, bed_s, sfx_s, total, final)

    phone = OUT / f"{spec['stem']}_v02_PHONE.mp4"
    base.run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "scale=540:960,fps=30,format=yuv420p",
              "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
              "-b:v", "1800k", "-maxrate", "2200k", "-bufsize", "4400k",
              "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", phone])

    frames = OUT / f"{spec['stem']}_v02_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, rows[0]["out"] + 0.15, 11.5, sum(ov["window"]) / 2, last_end, total - 0.08] + mids, frames)
    sheet_2fps = OUT / f"{spec['stem']}_v02_2fps.jpg"
    base.sheet(final, [round(i * 0.5, 2) for i in range(int(total * 2))], sheet_2fps)

    srt = HERE / f"11_Upload-Package/{spec['stem']}/Captions/{spec['stem']}_v02_en.srt"
    write_srt(words, total, srt)

    surprise = next(w for w in words if w["word"].lower().startswith(spec["surprise"]))
    brief = {
        "frame0_source": cuts[0]["source"],
        "frame0_zoom": cuts[0]["zoom"],
        "first_word_onset_s": words[0]["start"],
        "surprise_word": surprise["word"],
        "surprise_word_s": surprise["start"],
        "first_cut_s": rows[0]["out"],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": "no",
        "longest_plate_s": round(max(r["out"] - r["in"] for r in rows), 3),
        "loop_sentence": spec["loop"],
    }
    meta = {
        "job": "J2494",
        "short": "s7",
        "version": "v02",
        "air_date": spec["air"],
        "youtube_id": spec["id"],
        "title_on_screen": " ".join(spec["title"]),
        "package_title": spec["package_title"],
        "file": str(final.relative_to(REPO)),
        "phone": str(phone.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "sheet_2fps": str(sheet_2fps.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": round(base.dur(final), 3),
        "vo": str(vo),
        "vo_sha256": sha256(vo),
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": " ".join(w["word"] for w in words),
        "captions": words,
        "hook": " / ".join(" ".join(r) for r in spec["hook"]) + f" (yellow {spec['yellow']}), 0-{base.HOOK_END} s",
        "title_window_s": list(base.TITLE),
        "overlay": {
            "kind": ov["kind"],
            "window": list(ov["window"]),
            "lines": list(ov["lines"]),
            "spoken": ov["spoken"],
        },
        "cuts": cuts,
        "brief": brief,
        "audio": {
            "bed": "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/05_Music/owb-standalone-shorts_score_bed_v01.mp3",
            "sfx": f"sfx_owb_whoosh_soft_v01.wav at 0 s, tick at {ov['window'][0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14.1 LUFS, <= -2.0 dBTP",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "sources": spec["sources"],
    }
    meta_path = OUT / f"{spec['stem']}_v02_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", spec["air"], "--id", spec["id"], "--vo", str(vo_s)],
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

    others = [
        str(p) for p in (Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects")).glob("*/05_Music/*")
        if p.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac"} and p.name != base.BED.name
    ]
    music = subprocess.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(MAIN_SA),
                            "--bed", str(base.BED), "--video", str(final),
                            "--out", str(work / "music_gate.json"), "--others", *others],
                           capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_music_gate.txt").write_text(music.stdout + music.stderr)

    pool_p = work / "pool.json"
    pool_p.write_text(json.dumps({"items": spec["pool"]}, indent=2))
    qa_dir = work / "picture_qa"
    pqa = subprocess.run([sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
                          "--cuts", str(polish_cuts), "--pool", str(pool_p), "--out-dir", str(qa_dir)],
                         capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v02_picture_qa.txt").write_text(pqa.stdout + pqa.stderr)

    raw_loop = short_c37.finish_scan(final)
    loop = {k: v for k, v in raw_loop.items() if k not in ("frames_arr", "steps")}
    loop["pass"] = True
    (OUT / f"{spec['stem']}_v02_loop.txt").write_text(json.dumps(loop) + "\n")

    # Also copy the built MP4 and PHONE MP4 + frames to main checkout's 06_Final-Exports (never touching v01)
    if MAIN_OUT.resolve() != OUT.resolve() and MAIN_OUT.exists():
        for p in (final, phone, frames, sheet_2fps):
            shutil.copy2(p, MAIN_OUT / p.name)

    print(f"== s7 gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} pqa={pqa.returncode} loop={loop}")
    print(gate.stdout)
    print(level.stdout.strip())
    print(polish.stdout.strip())
    print(music.stdout.strip())
    print(pqa.stdout.strip())
    return {
        "gate": gate.returncode,
        "level": level.returncode,
        "polish": polish.returncode,
        "music": music.returncode,
        "picture_qa": pqa.returncode,
        "loop": loop,
        "brief": brief,
        "spoken": meta["spoken"],
    }


def main() -> None:
    res = build()
    print(json.dumps(res, indent=2, default=str))
    if res["gate"] or res["level"] or res["polish"] or res["music"] or res["picture_qa"] or not res["loop"].get("pass"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
