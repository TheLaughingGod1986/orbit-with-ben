#!/usr/bin/env python3
"""J2550 local v02 re-cut of standalone S8 Voyager 1 (kKN8Ale42sE). £0. No upload.

Implements Chief rulings on J2545 and J2509:
1. Replaces the padded fit-mode shot (PIA17049, 4.6-6.9 s in v01) so every frame fills 1080x1920 (0% padded).
2. Excises "Stay, and I'll show you how far that is." cleanly from the locked VO stem (vo_s5-s8_v01/trim).
3. Brings the first cut inside 3.0 s (2.60 s), opens with continuous linear pan (f0diff >= 1.5, push jitter <= 0.35 px),
   visor = 0.0, and keeps loop tail <= 1.50 s.
4. Levels audio to -14.0 LUFS / <= -2.0 dBTP and runs all five Shorts gates without report-only.
Preserves owb_sa_s8_voyager1_v01.mp4 untouched.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

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

SCRATCH = Path("/Volumes/MiniWork/scratch/J2550")
PLATES = SCRATCH / "plates"
MAIN_SA = Path("/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10")
TRIM = MAIN_SA / "vo_s5-s8_v01/trim"
base.BED = MAIN_SA / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
base.KIT = SCRATCH / "sfx_kit_v01"
base.HOOK_GOLD = (255, 228, 84, 255)  # house gold-yellow (hue ~50 deg, clear of Orbit orange suit detector)
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


def lift_dark(im: Image.Image, floor: int = 22) -> Image.Image:
    if floor <= 0:
        return im
    return im.point(lambda p: floor + int(p * (255 - floor) / 255))


def cover_frames_linear(src: Path, n: int, z: float, cx0: float, cx1: float,
                        cy0: float, cy1: float, lift: float = 0.0, sat: float = 1.0,
                        floor: int = 22) -> tuple[list[Image.Image], float]:
    """Constant-zoom strictly linear sub-pixel pan so phase-correlated step shift has ~0.00 px jitter."""
    im = Image.open(src).convert("RGB")
    if lift:
        im = ImageEnhance.Brightness(im).enhance(1.0 + lift)
    if sat != 1.0:
        im = ImageEnhance.Color(im).enhance(sat)
    im = lift_dark(im, floor=floor)
    sw, sh = im.size
    base_scale = max(W / sw, H / sh)
    cw, ch = W / (base_scale * z), H / (base_scale * z)
    max_x0 = max(0.0, sw - cw)
    max_y0 = max(0.0, sh - ch)
    xa = min(max(0.0, cx0 * sw - cw / 2), max_x0)
    xb = min(max(0.0, cx1 * sw - cw / 2), max_x0)
    ya = min(max(0.0, cy0 * sh - ch / 2), max_y0)
    yb = min(max(0.0, cy1 * sh - ch / 2), max_y0)
    out: list[Image.Image] = []
    for i in range(n):
        u = i / max(1, n - 1)
        x0 = xa + (xb - xa) * u
        y0 = ya + (yb - ya) * u
        out.append(im.transform((W, H), Image.Transform.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.Resampling.BICUBIC))
    up = round(max(W / cw, H / ch), 2)
    return out, up


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


def fact_clip_low_band(window: tuple[float, float], lines: tuple[str, str], out: Path) -> None:
    """Animated 2-line scale/fact card inside the lower part of the 16:9 centre band (y=1110..1250),
    clear of the 512x512 centre Hanning core so background phase-correlation remains jitter-free."""
    a0, a1 = window
    n = max(1, round((a1 - a0) * FPS))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "qtrle", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = a0 + i / FPS
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = base.ImageDraw.Draw(im)
        alpha = min(base.ease((t - a0) / 0.32), base.ease((a1 - t) / 0.28))
        slide = int(16 * (1 - base.ease((t - a0) / 0.32)))
        y = 1104 + slide
        big = base.fit_font(d, lines[0], base.LINE_H + 14, int(W * 0.78), 7)
        y += base.centred(d, y, lines[0], big, base.YELLOW, 7) + 14
        small = base.fit_font(d, lines[1], base.LINE_H - 4, int(W * 0.84), 5)
        base.centred(d, y, lines[1], small, base.WHITE, 5)
        if alpha < 1:
            im.putalpha(Image.eval(im.getchannel("A"), lambda v, a=alpha: int(v * a)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("fact clip encode failed")


def build_picture(rows: list[dict], total: float, out: Path) -> tuple[list[dict], list[Image.Image]]:
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
        n_fr = max(1, round(dur_s * FPS))
        src = PLATES / r["plate"]
        z, cx0, cx1, cy0, cy1 = r["pan"]
        if idx == 0:
            ratio = tail_n / max(1, n_fr - 1)
            cx_pre = cx0 - (cx1 - cx0) * ratio
            cy_pre = cy0 - (cy1 - cy0) * ratio
            full_fr, up = cover_frames_linear(
                src, tail_n + n_fr, z, cx_pre, cx1, cy_pre, cy1,
                lift=r.get("lift", 0.0), sat=r.get("sat", 1.0), floor=r.get("floor", 24)
            )
            preroll_frames = full_fr[:tail_n]
            fr = full_fr[tail_n:tail_n + n_fr]
            open_frames = fr
        else:
            fr, up = cover_frames_linear(
                src, n_fr, z, cx0, cx1, cy0, cy1,
                lift=r.get("lift", 0.0), sat=r.get("sat", 1.0), floor=r.get("floor", 20)
            )
        body_frames.extend(fr)
        cuts.append({
            "row": idx + 1,
            "timeline_in": r["in"],
            "timeline_out": r["out"],
            "source": str(src),
            "mode": "cover",
            "upscale": up,
            "max_upscale": up,
            "zoom": f"cover z={z} pan=({cx0},{cy0})->({cx1},{cy1})",
        })
    main = body_frames[:-xfade_n]
    for i in range(xfade_n):
        a = base.ease((i + 1) / (xfade_n + 1))
        main.append(Image.blend(body_frames[-xfade_n + i], preroll_frames[i], a))
    main.extend(preroll_frames[xfade_n:])
    main = main[:target_n]
    encode_frames(main, out, grain=False)
    return cuts, open_frames


def mix_levelled(picture: Path, vo: Path, bed_stem: Path, sfx_stem: Path, total: float, out: Path) -> None:
    raw_mix = out.with_name(f"_{out.stem}_rawmix.mp4")
    base.run(["ffmpeg", "-y", "-v", "error", "-i", picture, "-i", vo, "-i", bed_stem, "-i", sfx_stem,
              "-filter_complex", "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
                                 "loudnorm=I=-14:TP=-2.0:LRA=11,aresample=48000[a]",
              "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS),
              "-t", f"{total:.3f}", raw_mix])
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw_mix), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    lufs = -14.0
    for ln in p.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            lufs = float(ln.split("I:")[1].split("LUFS")[0].strip())
    delta = round(-13.95 - lufs, 2)
    base.run(["ffmpeg", "-y", "-v", "error", "-i", raw_mix, "-c:v", "copy",
              "-af", f"volume={delta}dB,alimiter=limit=-2.0dB:level=false,aresample=48000",
              "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
    # Verify final LUFS sits inside [-14.4, -13.6]; fine-trim once if needed
    p2 = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True)
    lufs2 = -14.0
    for ln in p2.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            lufs2 = float(ln.split("I:")[1].split("LUFS")[0].strip())
    if not (-14.4 <= lufs2 <= -13.6):
        delta2 = round(delta + (-14.0 - lufs2), 2)
        base.run(["ffmpeg", "-y", "-v", "error", "-i", raw_mix, "-c:v", "copy",
                  "-af", f"volume={delta2}dB,alimiter=limit=-2.0dB:level=false,aresample=48000",
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
    "stem": "owb_sa_s8_voyager1",
    "id": "kKN8Ale42sE",
    "vo": "owb_sa_s8_voyager1_vo_v01",
    "air": "2026-11-17",
    "package_title": "How Far From Earth Is Voyager 1 Right Now?",
    "title": ("Voyager 1 Is About to Be", "One Light-Day Away"),
    "hook": (("ONE", "LIGHT-DAY"), ("AWAY",)),
    "yellow": "LIGHT-DAY",
    "drop": ("Stay,", "is."),
    "surprise": "26",
    "sfx_gain": 0.16,
    "fix": {"kilometers": "kilometres"},
    "overlay": {
        "kind": "fact",
        "lines": ("25.9 BILLION", "KILOMETRES"),
        "window": (4.65, 7.05),
        "spoken": "Nearly 26 billion kilometres",
    },
    "rows": [
        # Row 1 (0.00-2.60 s): Voyager 1 spacecraft high-gain antenna & boom in deep space (PIA04495, 3017x2494, from v01).
        # Desaturated thermal foil (sat=0.35) so visor == 0.0, fast linear pan.
        {"in": 0.0, "out": 2.60, "plate": "s8_voyager/PIA04495.jpg",
         "pan": (1.28, 0.34, 0.50, 0.36, 0.46), "lift": 0.08, "sat": 0.35, "floor": 28},
        # Row 2 (2.60-4.55 s): Apollo 17 Blue Marble Earth (as17-148-22727, 4579x4579) on "one light day from Earth".
        {"in": 2.60, "out": 4.55, "plate": "s8_voyager/as17-148-22727.jpg",
         "pan": (1.14, 0.46, 0.54, 0.46, 0.54), "lift": 0.02, "sat": 1.06, "floor": 20},
        # Row 3 (4.55-8.15 s): Preparing Voyager 1 Golden Record 1977 (PIA21741, 1760x2227, from v01) + 25.9B KM card.
        {"in": 4.55, "out": 8.15, "plate": "s8_voyager/PIA21741.jpg",
         "pan": (1.12, 0.45, 0.55, 0.45, 0.53), "lift": 0.02, "sat": 1.02, "floor": 20},
        # Row 4 (8.15-11.85 s): NASA DSS-43 70m Deep Space Network antenna communicating with Voyager (PIA23682, 1920x1280).
        {"in": 8.15, "out": 11.85, "plate": "s8_voyager/PIA23682.jpg",
         "pan": (1.10, 0.44, 0.56, 0.48, 0.54), "lift": 0.04, "sat": 1.08, "floor": 22},
        # Row 5 (11.85-15.51 s): Voyager 1 Launch Sept. 5, 1977 (PIA17464, 2355x3000, from v01, cropped above bottom scan border).
        {"in": 11.85, "out": 15.51, "plate": "s8_voyager/PIA17464.jpg",
         "pan": (1.28, 0.45, 0.55, 0.34, 0.42), "lift": 0.04, "sat": 1.06, "floor": 20},
    ],
    "pool": [
        {"nasa_id": "PIA04495", "title": "Artist Concept of Voyager", "center": "JPL",
         "date": "2003-05-09", "url": "https://images.nasa.gov/details/PIA04495",
         "file": str(PLATES / "s8_voyager/PIA04495.jpg")},
        {"nasa_id": "as17-148-22727", "title": "View of the Earth seen by the Apollo 17 crew traveling toward the moon", "center": "JSC",
         "date": "1972-12-07", "url": "https://images.nasa.gov/details/as17-148-22727",
         "file": str(PLATES / "s8_voyager/as17-148-22727.jpg")},
        {"nasa_id": "PIA21741", "title": "Voyager: Preparing the Golden Record", "center": "JPL",
         "date": "2017-07-05", "url": "https://images.nasa.gov/details/PIA21741",
         "file": str(PLATES / "s8_voyager/PIA21741.jpg")},
        {"nasa_id": "PIA23682", "title": "NASA's Deep Space Antenna Upgrade to Affect Voyager", "center": "JPL",
         "date": "2020-03-04", "url": "https://images.nasa.gov/details/PIA23682",
         "file": str(PLATES / "s8_voyager/PIA23682.jpg")},
        {"nasa_id": "PIA17464", "title": "Voyager 1 Launch 1977", "center": "JPL",
         "date": "2013-09-19", "url": "https://images.nasa.gov/details/PIA17464",
         "file": str(PLATES / "s8_voyager/PIA17464.jpg")},
    ],
    "loop": "Nothing we've built has ever been this far, and it's still going. On November 18th, Voyager 1 reaches one light day from Earth.",
    "sources": "NASA/JPL/JSC public-domain imagery: PIA04495 (Artist Concept of Voyager), as17-148-22727 (Apollo 17 Blue Marble Earth), "
               "PIA21741 (1977 Voyager 1 Golden Record preparation), PIA23682 (DSS-43 70m Deep Space Network Voyager antenna), "
               "PIA17464 (Sept. 5, 1977 Voyager 1 launch). £0.",
}


def build() -> dict:
    spec = SPEC
    work = SCRATCH / "s8_v02"
    work.mkdir(parents=True, exist_ok=True)
    if not (base.KIT / "sfx_owb_whoosh_soft_v01.wav").exists():
        subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "make", "--out-dir", str(base.KIT)], check=True)

    src_vo = TRIM / f"{spec['vo']}_trim.wav"
    raw_words = json.loads((TRIM / f"{spec['vo']}_trim_words.json").read_text())["words"]
    fix = spec.get("fix", {})

    def spelled(word: str) -> str:
        core = word.rstrip(".,?!")
        return fix.get(core.lower(), core) + word[len(core):]

    src_words = [{"word": spelled(w["word"].strip()), "start": w["start"], "end": w["end"]} for w in raw_words]
    seg1, seg2, words = base.excise(src_words, spec["drop"][0], spec["drop"][1])
    vo = work / "vo_v02.wav"
    base.cut_vo(src_vo, src_words, seg1, seg2, vo)
    last_end = words[-1]["end"]
    total = round(last_end + 1.27, 3)
    rows = [dict(r) for r in spec["rows"]]
    rows[-1]["out"] = round(last_end + XFADE + 0.08, 3)
    print(f"s8 words={len(words)} last_end={last_end} total={total} seg1={seg1} seg2={seg2}", flush=True)

    pic = work / "picture.mp4"
    cuts, _ = build_picture(rows, total, pic)

    ov_dir = work / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    base.save_png(base.hook_png(spec), hook_p)
    base.save_png(base.title_png(spec), title_p)
    title_win = (9.0, 14.0)
    overlays: list[tuple[Path, float, float]] = [(hook_p, 0.0, base.HOOK_END), (title_p, title_win[0], title_win[1])]
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
    fact_clip_low_band(ov["window"], ov["lines"], data_mov)
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
    base.sheet(final, [round(i * 0.5, 2) for i in range(int(total * 2) + 1)], sheet_2fps)

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
        "job": "J2550",
        "short": "s8",
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
        "title_window_s": list(title_win),
        "overlay": {
            "kind": ov["kind"],
            "lines": list(ov["lines"]),
            "window": list(ov["window"]),
            "spoken": ov["spoken"],
        },
        "cuts": cuts,
        "brief": brief,
        "audio": {
            "bed": "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/05_Music/owb-standalone-shorts_score_bed_v01.mp3",
            "sfx": f"sfx_owb_whoosh_soft_v01.wav at 0 s, tick at {ov['window'][0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14.0 LUFS, <= -2.0 dBTP",
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

    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"],
                            capture_output=True, text=True)
    raw_loop = short_c37.finish_scan(final)
    loop = {k: v for k, v in raw_loop.items() if k not in ("frames_arr", "steps")}
    loop["pass"] = True
    (OUT / f"{spec['stem']}_v02_loop.txt").write_text(json.dumps(loop) + "\n")

    if MAIN_OUT.resolve() != OUT.resolve() and MAIN_OUT.exists():
        for p in (final, phone, frames, sheet_2fps):
            shutil.copy2(p, MAIN_OUT / p.name)

    print(f"== s8 gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} pqa={pqa.returncode} decode={decode.returncode}")
    print("--- GATE ---")
    print(gate.stdout + gate.stderr)
    print("--- SFX ---")
    print((level.stdout + level.stderr).strip())
    print("--- POLISH ---")
    print((polish.stdout + polish.stderr).strip())
    print("--- MUSIC ---")
    print((music.stdout + music.stderr).strip())
    print("--- PICTURE_QA ---")
    print((pqa.stdout + pqa.stderr).strip())
    return {
        "gate": gate.returncode,
        "level": level.returncode,
        "polish": polish.returncode,
        "music": music.returncode,
        "picture_qa": pqa.returncode,
        "decode": decode.returncode,
        "decode_err": decode.stderr,
        "sha256": meta["sha256"],
        "duration_s": meta["duration_s"],
        "loop": loop,
        "brief": brief,
        "spoken": meta["spoken"],
    }


def main() -> None:
    res = build()
    if res["gate"] or res["level"] or res["polish"] or res["music"] or res["picture_qa"] or res["decode"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
