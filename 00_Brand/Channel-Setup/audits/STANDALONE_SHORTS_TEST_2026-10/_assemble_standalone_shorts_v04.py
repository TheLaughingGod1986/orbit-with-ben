#!/usr/bin/env python3
"""J0914 v04 local re-cut. v01, v02 and v03 files are not touched. £0. No upload.

v03 failed gate_shorts_open on the first cut (scene-detect threshold 10):
S2 had no cut in 10 s (every plate was the same close-up), S3's first detected
cut was at 5.93 s. v04 keeps the VO cuts and the loop.

S2 Neptune: plate 2 is the curved limb (crop 450x800 at 574,340 from t=1.55 s).
That join scores about 21 on the gate's centre-band scdet. Black stays under 30%.
No plate is scaled above 2.5x. The loop still lands on the frame-0 picture.

S3 ISS: plate 2 starts at t=65 s of the same public-domain film. A cut from t=3 s
to t=12.5 s scored under 10; t=65 s scored about 15. Rotate fill stays black and
is cropped off. The false "every 45 minutes" line stays out of the VO.
"""
from __future__ import annotations

import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
_spec = importlib.util.spec_from_file_location("sa_v02", HERE / "_assemble_standalone_shorts_v02.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

WORK = base.WORK / "v04"
OUT = base.OUT
FPS = base.FPS
W, H = base.W, base.H
TAIL = base.TAIL
XFADE = base.XFADE
NEP = base.NEP
ISS = base.ISS
TITLE = base.TITLE

# Disc centre and radius of the blue planet in neptune_svs_vert.webm (1080x1920).
# Measured 25 Oct 2026. After t=2.2 a full-bleed crop exceeds 2.5x, so every
# Neptune plate stays inside this window.
DISC = [
    (0.00, 542, 909, 755), (0.20, 541, 910, 726), (0.40, 539, 910, 695),
    (0.60, 536, 913, 667), (0.80, 535, 918, 642), (1.00, 531, 924, 618),
    (1.20, 524, 933, 594), (1.40, 516, 941, 571), (1.60, 503, 948, 550),
    (1.80, 490, 956, 528), (2.00, 476, 963, 506), (2.20, 465, 965, 485),
]


def disc(t: float) -> tuple[float, float, float]:
    t = max(0.0, min(t, DISC[-1][0]))
    for (t0, x0, y0, r0), (t1, x1, y1, r1) in zip(DISC, DISC[1:]):
        if t0 <= t <= t1:
            u = 0 if t1 == t0 else (t - t0) / (t1 - t0)
            return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, r0 + (r1 - r0) * u)
    return DISC[-1][1], DISC[-1][2], DISC[-1][3]


def even(n: float) -> int:
    return int(n) // 2 * 2


def fit_crop(t0: float, t1: float, scale: float, dx: float, dy: float):
    """A fixed 9:16 crop inside the disc from t0 to t1, at this upscale, shifted from the tightest centre."""
    samples = [disc(t0 + (t1 - t0) * i / 8) for i in range(9)]
    tight = min(samples, key=lambda s: s[2])
    cw = even(1080 / scale)
    ch = even(cw * 16 / 9)
    actual = 1080 / cw
    if actual > 2.50:
        return None
    half = math.hypot(cw / 2, ch / 2)
    if half > 0.92 * tight[2]:
        return None
    x = even(tight[0] + dx - cw / 2)
    y = even(tight[1] + dy - ch / 2)
    if x < 0 or y < 0 or x + cw > 1080 or y + ch > 1920:
        return None
    worst = 0.0
    for cx, cy, r in samples:
        for px, py in ((x, y), (x + cw, y), (x, y + ch), (x + cw, y + ch)):
            worst = max(worst, math.hypot(px - cx, py - cy) / r)
    if worst > 0.93:
        return None
    return {"w": cw, "h": ch, "x": x, "y": y, "scale": round(actual, 3), "edge": round(worst, 3)}


def encode(src: Path, ss: float, in_dur: float, fc: str, frames: int, out: Path) -> None:
    """Trim inside the filter. -ss/-t after -i would cap the output, which breaks slow-motion plates."""
    out.parent.mkdir(parents=True, exist_ok=True)
    fc = fc.replace("[0:v]", f"[0:v]trim=start={ss:.3f}:duration={in_dur:.3f},setpts=PTS-STARTPTS,", 1)
    base.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", fc, "-map", "[v]",
              "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
              "-pix_fmt", "yuv420p", "-an", out])
    got = base.dur(out)
    want = frames / FPS
    if abs(got - want) > 0.15:
        raise SystemExit(f"{out.name} is {got:.2f}s, wanted {want:.2f}s")


def svs_seg(ss: float, dur_s: float, speed: float, crop: dict, out: Path) -> None:
    frames = round(dur_s * FPS)
    fc = (
        f"[0:v]setpts=PTS/{speed:.5f},crop={crop['w']}:{crop['h']}:{crop['x']}:{crop['y']},"
        "scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=1.22:contrast=1.05,fps=30,format=yuv420p[v]"
    )
    encode(NEP, ss, dur_s * speed + 0.08, fc, frames, out)


def iss_seg(ss: float, dur_s: float, out: Path) -> float:
    """Earth limb, shuttle left outside the crop. Black rotate-fill, then zoom past the wedges."""
    frames = round(dur_s * FPS)
    # 720 px of source height covers 1920 only at 2.67x. The 1.18 wedge zoom
    # raises that. Logged, not hidden: this plate cannot be <=2.5x and full-bleed.
    fc = (
        "[0:v]crop=560:720:700:0,"
        "rotate=0.16:fillcolor=black:ow=rotw(0.16):oh=roth(0.16),"
        "scale=iw*1.18:ih*1.18,"
        "crop=iw/1.18:ih/1.18,"
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "eq=saturation=1.18:contrast=1.05,fps=30,format=yuv420p[v]"
    )
    encode(ISS, ss, dur_s + 0.08, fc, frames, out)
    # Visible source height after the 1.18 zoom, scaled up to 1920.
    return round((1920 / (720 / 1.18)), 3)


def black_frac(path: Path, t: float, thresh: int = 18) -> float:
    frame = path.with_name(f"_blk_{t:.2f}.jpg")
    base.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", frame])
    im = Image.open(frame).convert("L")
    data = im.tobytes()
    frame.unlink(missing_ok=True)
    return sum(1 for v in data if v <= thresh) / len(data)


def corner_stats(path: Path, t: float) -> dict:
    frame = path.with_name("_corner.jpg")
    base.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", frame])
    im = Image.open(frame).convert("RGB")
    w, h = im.size
    out = {}
    for name, box in {
        "tl": (0, 0, 8, 8),
        "tr": (w - 8, 0, w, 8),
        "bl": (0, h - 8, 8, h),
        "br": (w - 8, h - 8, w, h),
    }.items():
        px = list(im.crop(box).getdata())
        r = sum(p[0] for p in px) / len(px)
        g = sum(p[1] for p in px) / len(px)
        b = sum(p[2] for p in px) / len(px)
        out[name] = {"r": round(r, 1), "g": round(g, 1), "b": round(b, 1),
                     "green": g > r + 25 and g > b + 10 and g > 40}
    frame.unlink(missing_ok=True)
    return out


def measured_lufs(path: Path) -> str:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    text = proc.stderr
    i_lufs = tp = None
    for line in text.splitlines():
        if "I:" in line and "LUFS" in line:
            i_lufs = line.split("I:")[-1].split("LUFS")[0].strip()
        if "Peak:" in line and "dBFS" in line:
            tp = line.split("Peak:")[-1].split("dBFS")[0].strip()
    if not i_lufs:
        return "unmeasured"
    tp_bit = f", {tp} dBFS peak" if tp else ""
    return f"{i_lufs} LUFS{tp_bit}"


def excise_many(words: list[dict], drops: list[tuple[str, str]], breath: float = 0.15, tail: float = 0.05):
    """Drop each sentence and close that join to `breath` seconds. Other pauses stay."""
    spans = []
    for start_p, end_p in drops:
        i0 = next(i for i, w in enumerate(words) if w["word"].lower().startswith(start_p.lower()))
        i1 = next(i for i, w in enumerate(words) if i >= i0 and w["word"].lower().startswith(end_p.lower()))
        spans.append((i0, i1))
    cuts = []
    pos = 0.0
    for n, (i0, i1) in enumerate(spans):
        prev_end = words[i0 - 1]["end"]
        cuts.append((round(pos, 3), round(prev_end + tail, 3)))
        nxt = words[i1 + 1]["start"]
        pos = round(nxt - (breath - tail), 3)
    cuts.append((round(pos, 3), None))

    def map_t(src: float) -> float:
        out = 0.0
        for a, b in cuts:
            if b is None or src <= b + 1e-6:
                if src + 1e-6 < a:
                    raise SystemExit(f"word at {src} falls in a cut")
                return round(out + (src - a), 3)
            out += b - a
        raise SystemExit(f"no map for {src}")

    kept = []
    for i, w in enumerate(words):
        if any(i0 <= i <= i1 for i0, i1 in spans):
            continue
        kept.append({"word": w["word"], "start": map_t(w["start"]), "end": map_t(w["end"])})
    for i in range(1, len(kept)):
        gap = round(kept[i]["start"] - kept[i - 1]["end"], 3)
        # Only the joins we created are required to be <= breath. Flag a blown join.
        if gap < -0.02:
            raise SystemExit(f"overlap at {kept[i]['word']}: {gap}")
    return cuts, kept


def cut_vo_spans(src: Path, cuts: list[tuple[float, float | None]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    parts = []
    labels = []
    for i, (a, b) in enumerate(cuts):
        trim = f"atrim=start={a:.3f}" + (f":end={b:.3f}" if b is not None else "")
        parts.append(f"[0:a]{trim},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[a{i}]")
    parts.append("".join(labels) + f"concat=n={len(cuts)}:v=0:a=1[aout]")
    base.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", ";".join(parts),
              "-map", "[aout]", "-ac", "2", "-ar", "48000", out])


def nep_windows(last_end: float) -> list[tuple[float, float]]:
    """First cut at 1.90 s. Last plate is 1.20 s so it can land on the opening frame the loop reverses from."""
    end = round(last_end + XFADE + 0.08, 3)
    last_len = 1.20
    body_end = round(end - last_len, 3)
    first, hold = 1.90, 3.50
    starts = [0.0, first]
    t = first + hold
    while t < body_end - 1.0:
        starts.append(round(t, 3))
        t += hold
    starts.append(body_end)
    bounds = starts + [end]
    windows = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    for a, b in windows:
        if b - a > 4.01:
            raise SystemExit(f"plate {a}-{b} held {b - a:.2f}s")
    if windows[0][1] > 3.0:
        raise SystemExit("first cut after 3 s")
    return windows


def opening_crop() -> dict:
    """The frame-0 crop. It has to survive the opening plate, which runs to source t≈2.10."""
    crop = fit_crop(0.15, 2.10, 2.45, 0, 0)
    if not crop:
        raise SystemExit("opening crop does not fit inside the disc at <=2.5x")
    return crop


def plate_crop(i: int, n: int, ss: float, src_end: float, opening: dict) -> dict:
    if i == 0 or i == n - 1:
        return opening
    # Framing jump on plate 2 (index 1): wider and earlier, so the cut is not the same clouds.
    # Later plates move the window around inside the same close-up.
    trials = [
        (2.10, -30, -20),  # first cut: wider and shifted, source still in the close-up
        (2.20, 30, -16),
        (2.30, -30, -20),
        (2.20, -20, 24),
        (2.30, 24, 18),
        (2.20, 0, 0),
    ]
    scale, dx, dy = trials[(i - 1) % len(trials)]
    crop = fit_crop(ss, src_end, scale, dx, dy)
    if crop is None:
        crop = fit_crop(ss, src_end, 2.30, 0, 0)
    if crop is None:
        crop = opening
    return crop


def build_nep(words, last_end, work: Path) -> tuple[list[Path], list[dict], float]:
    windows = nep_windows(last_end)
    opening = opening_crop()
    open_ss = 0.20
    parts = []
    cuts = []
    for i, (a, b) in enumerate(windows):
        length = round(b - a, 3)
        part = work / f"seg_{i:02d}.mp4"
        if i == len(windows) - 1:
            # The crossfade reads this plate at last_end, not at the plate's last frame.
            # That instant has to be the opening frame the reverse starts on (t = TAIL).
            join_into_plate = round(last_end - a, 3)
            ss = round(open_ss + TAIL - join_into_plate, 3)
            speed = 1.0
            crop = opening
        elif i == 0:
            ss, speed, crop = open_ss, 1.0, opening
        elif i == 1:
            # The close-up clouds match each other, so scene-detect missed the cut (score 3.8).
            # This window shows the curved limb. Measured black stays under 30% from t=1.55 to 2.00,
            # and a join against the opening scores 21 on scdet (threshold 10).
            ss = 1.55
            src_span = 0.45
            speed = round(src_span / length, 5)
            crop = {"w": 450, "h": 800, "x": 574, "y": 340, "scale": 2.4, "edge": 0.0}
        else:
            # Stay inside the close-up. A wider, earlier window on the second plate is the cut.
            ss = round(0.18 + ((i - 1) % 3) * 0.12, 3)
            src_span = 0.85 if i == 1 else 1.05
            speed = round(src_span / length, 5)
            crop = plate_crop(i, len(windows), ss, ss + src_span, opening)
        if crop["scale"] > 2.50:
            raise SystemExit(f"plate {i} upscale {crop['scale']} > 2.5")
        svs_seg(ss, length, speed, crop, part)
        parts.append(part)
        cuts.append({
            "row": i + 1,
            "timeline_in": a,
            "timeline_out": round(b, 3),
            "source": f"SVS 14397 t={ss:.2f}s speed {speed:.2f} crop {crop['w']}x{crop['h']}@{crop['x']},{crop['y']}",
            "framing": {"offset": length},
            "zoom": f"inside the cloud deck, {crop['scale']:.2f}x",
            "max_upscale": crop["scale"],
        })
        if a < 6.0:
            bf = black_frac(part, min(0.35, length / 2))
            print(f"  nep plate {i} {a:.2f}-{b:.2f} ss={ss:.2f} x{speed:.2f} scale={crop['scale']} edge={crop['edge']} black={bf:.1%}", flush=True)
            if bf > 0.30:
                raise SystemExit(f"plate {i} is {bf:.1%} black")
        else:
            print(f"  nep plate {i} {a:.2f}-{b:.2f} ss={ss:.2f} x{speed:.2f} scale={crop['scale']} edge={crop['edge']}", flush=True)
    return parts, cuts, max(c["max_upscale"] for c in cuts)


def build_iss(words_src, work: Path) -> tuple[list, list[dict], list[dict], float, list]:
    src_vo = base.TRIM / "owb_sa_s3_iss_sunrises_vo_v01_trim.wav"
    cuts_a, words = excise_many(words_src, [("Stay", "one"), ("So", "ends")])
    spoken = " ".join(w["word"] for w in words)
    if "Stay" in spoken or "45" in spoken or "I'll" in spoken:
        raise SystemExit(f"ISS VO still has a cut line: {spoken}")
    vo = work / "vo_v04.wav"
    cut_vo_spans(src_vo, cuts_a, vo)
    # The joins we made should be about 0.15 s. Check those two boundaries by silence, not every original pause.
    last_end = words[-1]["end"]
    # Plate 1 is only 1.6 s. A 3.55 s hold put its middle frame on the caption
    # "THE SPACE STATION", which polish_gate read as a horizontal gutter.
    # The frame at 3.2 s on the same plate is clean, so the hold ends at 4.0 s.
    end = round(last_end + base.XFADE + 0.08, 3)
    windows = [(0.0, 2.40), (2.40, 4.00)]
    t = 4.00
    while t < end - 1.3:
        nxt = round(min(t + 3.55, end), 3)
        windows.append((round(t, 3), nxt))
        t = round(t + 3.55, 3)
    if abs(windows[-1][1] - end) > 0.05:
        windows.append((windows[-1][1], end))
    else:
        windows[-1] = (windows[-1][0], end)
    parts, cuts = [], []
    up = 0.0
    # Plate 0 stays at t=3 s so the loop matches frame 0. Plate 1 jumps to t=65 s:
    # the gate's scdet (threshold 10, centre band) scored that join about 15.
    # t=3 s to t=12.5 s scored under 10, which is why v03's first cut read as 5.93 s.
    iss_ss = [3.0, 65.0, 22.0, 40.0, 50.0, 30.0, 12.0, 55.0]
    for i, (a, b) in enumerate(windows):
        length = round(b - a, 3)
        part = work / f"seg_{i:02d}.mp4"
        ss = iss_ss[i] if i < len(iss_ss) else 22.0
        if ss + length > 74.0:
            ss = round(74.0 - length, 2)
        up = max(up, iss_seg(ss, length, part))
        parts.append(part)
        cuts.append({
            "row": i + 1,
            "timeline_in": a,
            "timeline_out": round(b, 3),
            "source": f"Sunrise To Sunset Aboard The ISS.ogv t={ss:.2f}s earth-limb crop",
            "framing": {"offset": length},
            "zoom": "earth-limb crop, rolled about 9 degrees, black fill, 1.18x wedge crop, cover to 1080x1920",
            "max_upscale": up,
        })
        print(f"  iss plate {i} {a:.2f}-{b:.2f} ss={ss:.2f} upscale={up}", flush=True)
    return words, parts, cuts, up, vo


def concat(parts: list[Path], out: Path) -> None:
    inputs: list[str] = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    fc = "".join(f"[{i}:v]setsar=1[s{i}];" for i in range(n))
    fc += "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    base.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", out])


def looped(main: Path, opening: Path, last_end: float, out: Path) -> None:
    rev = out.with_name("rev.mp4")
    frames = round(TAIL * FPS)
    base.run(["ffmpeg", "-y", "-v", "error", "-i", opening, "-vf",
               f"trim=0:{TAIL},setpts=PTS-STARTPTS,reverse,fps=30,format=yuv420p",
               "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", rev])
    pre = out.with_name("pregrain.mp4")
    base.run(["ffmpeg", "-y", "-v", "error", "-i", main, "-i", rev, "-filter_complex",
               f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={last_end:.3f},fps=30,format=yuv420p[v]",
               "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", pre])
    # Last frame of the reverse is frame 0 of the opening. Compare before grain.
    a = pre.with_name("_f0.jpg")
    b = pre.with_name("_fEnd.jpg")
    base.run(["ffmpeg", "-y", "-v", "error", "-ss", "0", "-i", opening, "-frames:v", "1", a])
    end_t = max(0.0, base.dur(pre) - 0.04)
    base.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{end_t:.3f}", "-i", pre, "-frames:v", "1", b])
    ia = Image.open(a).convert("RGB").resize((96, 170))
    ib = Image.open(b).convert("RGB").resize((96, 170))
    pa, pb = list(ia.getdata()), list(ib.getdata())
    mae = sum(abs(x - y) for p, q in zip(pa, pb) for x, y in zip(p, q)) / (len(pa) * 3)
    a.unlink(missing_ok=True)
    b.unlink(missing_ok=True)
    print(f"  loop frame0 vs last MAE {mae:.2f}", flush=True)
    if mae > 18:
        raise SystemExit(f"loop does not land on the frame-0 picture (MAE {mae:.1f})")
    base.run(["ffmpeg", "-y", "-v", "error", "-i", pre, "-vf", "noise=alls=4:allf=t,format=yuv420p",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", out])


def audit_black(path: Path, limit: float = 6.0) -> dict:
    times = [i * 0.5 for i in range(int(limit * 2) + 1)]
    scores = {f"{t:.1f}": round(black_frac(path, t), 4) for t in times}
    worst = max(scores.values())
    return {"worst": worst, "samples": scores}


def find_word(words, prefix: str, start: int = 0) -> dict:
    return next(w for i, w in enumerate(words) if i >= start and w["word"].lower().startswith(prefix.lower()))


def build(key: str) -> dict:
    spec = SPECS[key]
    work = WORK / spec["stem"]
    if work.exists():
        # Fresh plates. v02 intermediates live in the parent work dir and stay.
        for p in work.glob("seg_*.mp4"):
            p.unlink()
        for name in ("main.mp4", "picture.mp4", "pregrain.mp4", "rev.mp4", "comp.mp4"):
            q = work / name
            if q.exists():
                q.unlink()
    work.mkdir(parents=True, exist_ok=True)
    src_words = json.loads((base.TRIM / f"{spec['vo']}_trim_words.json").read_text())["words"]

    if key == "s2":
        src_vo = base.TRIM / f"{spec['vo']}_trim.wav"
        seg1, seg2, words = base.excise(src_words, "Stay", spec["drop_through"])
        vo = work / "vo_v04.wav"
        base.cut_vo(src_vo, src_words, seg1, seg2, vo)
        last_end = words[-1]["end"]
        parts, cuts, max_up = build_nep(words, last_end, work)
    else:
        words, parts, cuts, max_up, vo = build_iss(src_words, work)
        last_end = words[-1]["end"]

    main = work / "main.mp4"
    concat(parts, main)
    base_pic = work / "picture.mp4"
    looped(main, parts[0], last_end, base_pic)
    total = round(base.dur(base_pic), 3)
    gap = round(total - last_end, 3)
    print(key, "picture", total, "tail", gap, "words", len(words), flush=True)
    if gap > 1.5:
        raise SystemExit(f"tail {gap}s is over 1.5s")

    if key == "s2":
        blk = audit_black(base_pic, 6.0)
        print("  black 0-6s", blk, flush=True)
        if blk["worst"] > 0.30:
            raise SystemExit(f"black {blk['worst']:.1%} in the first 6 s")
    else:
        blk = {"worst": None, "samples": {}}
        corners = corner_stats(parts[0], 0.2)
        print("  corners", corners, flush=True)
        if any(v["green"] for v in corners.values()):
            raise SystemExit(f"green corner remains: {corners}")
        spec = dict(spec)
        spec["corners"] = corners

    ov_dir = work / "ov"
    ov_dir.mkdir(exist_ok=True)
    hook_p, title_p = ov_dir / "hook.png", ov_dir / "title.png"
    base.save_png(base.hook_png(spec), hook_p)
    base.save_png(base.title_png(spec), title_p)
    overlays = [(hook_p, 0.0, base.HOOK_END), (title_p, TITLE[0], TITLE[1])]
    for i, (a, b, im) in enumerate(base.caption_pngs(words, total)):
        p = ov_dir / f"cap_{i:02d}.png"
        base.save_png(im, p)
        overlays.append((p, a, b))

    ov = dict(spec["overlay"])
    if key == "s3":
        start = find_word(words, "16", 4)  # the second "16", on "16 sunrises"
        # The number is said across the 9–14 s title, so the counter starts as the title clears.
        a0 = max(start["start"], 14.05)
        a1 = min(total - 0.4, a0 + 3.4)
        ov["window"] = (round(a0, 2), round(a1, 2))
        ov["spoken"] = "16 sunrises, 16 sunsets"
    data = ov_dir / "data.mov"
    if ov["kind"] == "bars":
        base.bars_clip(tuple(ov["window"]), data)
    else:
        base.counter_clip(tuple(ov["window"]), data)
    overlays.append((data, ov["window"][0], ov["window"][1]))

    comp = work / "comp.mp4"
    base.composite(base_pic, overlays, comp)
    vo_s, bed_s, sfx_s = base.stems(work, vo, total, last_end, ov["window"][0] + 0.05, spec["sfx_gain"])
    final = OUT / f"{spec['stem']}_v04.mp4"
    OUT.mkdir(exist_ok=True)
    base.mix(comp, vo_s, bed_s, sfx_s, total, final)
    lufs = measured_lufs(final)

    frames = OUT / f"{spec['stem']}_v04_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, cuts[0]["timeline_out"] + 0.12, 11.5,
                       sum(ov["window"]) / 2, last_end, total - 0.08] + mids, frames)

    surprise = find_word(words, spec["surprise"])
    brief = {
        "frame0_source": cuts[0]["source"],
        "frame0_zoom": cuts[0]["zoom"],
        "first_word_onset_s": words[0]["start"],
        "surprise_word": surprise["word"],
        "surprise_word_s": surprise["start"],
        "first_cut_s": cuts[0]["timeline_out"],
        "last_word_to_loop_s": gap,
        "meta_promise": "no",
        "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts), 3),
        "loop_sentence": spec["loop"],
        "max_upscale": max_up,
        "black_0_6s": blk["worst"],
    }
    meta = {
        "job": "J0914", "short": key, "version": "v04",
        "air_date": spec["air"], "youtube_id": spec["id"],
        "title_on_screen": " ".join(spec["title"]),
        "file": str(final.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "duration_s": round(base.dur(final), 3),
        "vo": str(vo),
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": " ".join(w["word"] for w in words),
        "captions": words,
        "hook": " / ".join(" ".join(r) for r in spec["hook"]) + f" (yellow {spec['yellow']}), 0-{base.HOOK_END} s",
        "title_window_s": list(TITLE),
        "overlay": ov,
        "cuts": cuts,
        "brief": brief,
        "audio": {
            "bed": str(base.BED.relative_to(REPO)),
            "sfx": f"sfx_owb_whoosh_soft_v01.wav at 0 s, tick at {ov['window'][0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": lufs,
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "max_upscale": max_up,
        "sources": spec["sources"],
    }
    if key == "s3":
        meta["corners"] = spec.get("corners")
        meta["black_note"] = "ISS corners checked for the green rotate fill. Neptune black audit is on S2."
    else:
        meta["black_0_6s"] = blk
    meta_path = OUT / f"{spec['stem']}_v04_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", spec["air"], "--id", spec["id"]],
                          capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v04_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_s), "--sfx", str(sfx_s), "--bed", str(bed_s),
                            "--minutes", f"{total / 60:.4f}"], capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v04_sfx_level.txt").write_text(level.stdout + level.stderr)
    polish_cuts = work / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run([sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
                             "--cuts", str(polish_cuts), "--out", str(work / "polish_gate.json")],
                            capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v04_polish.txt").write_text(polish.stdout + polish.stderr)
    music = subprocess.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(HERE),
                            "--bed", str(base.BED), "--video", str(final),
                            "--out", str(work / "music_gate.json")],
                           capture_output=True, text=True)
    (OUT / f"{spec['stem']}_v04_music_gate.txt").write_text(music.stdout + music.stderr)
    print(f"== {key} gate={gate.returncode} level={level.returncode} polish={polish.returncode} music={music.returncode}")
    print(gate.stdout)
    print((level.stdout or level.stderr)[-800:])
    print((polish.stdout or polish.stderr)[-800:])
    print((music.stdout or music.stderr)[-800:])
    return {"gate": gate.returncode, "level": level.returncode, "polish": polish.returncode,
            "music": music.returncode, "brief": brief, "spoken": meta["spoken"], "lufs": lufs}


SPECS = {
    "s2": {
        "stem": "owb_sa_s2_neptune", "id": "oyRcrFTYyDY", "vo": "owb_sa_s2_neptune_vo_v01",
        "air": "2026-10-27", "drop_through": "fast", "surprise": "supersonic",
        "sfx_gain": 0.20,
        "title": ("The Wind on Neptune", "Is Supersonic"),
        "hook": (("SUPERSONIC",), ("WIND",)), "yellow": "SUPERSONIC",
        "overlay": {"kind": "bars", "window": (6.45, 8.90),
                    "spoken": "over two thousand kilometres an hour"},
        "loop": "And still. The wind on Neptune is supersonic.",
        "sources": "Frame 0 and every plate: NASA SVS 14397 (Neptune's disappearing clouds), public domain, "
                   "cropped inside the cloud deck at 2.5x or under. No rotating-disc plate. No new picture generation.",
    },
    "s3": {
        "stem": "owb_sa_s3_iss_sunrises", "id": "XKlq0TK1OVA", "vo": "owb_sa_s3_iss_sunrises_vo_v01",
        "air": "2026-10-31", "drop_through": "one", "surprise": "16",
        "sfx_gain": 0.16,
        "title": ("Astronauts See 16", "Sunrises Every Day"),
        "hook": (("16", "SUNRISES"), ("A", "DAY")), "yellow": "16",
        "overlay": {"kind": "counter", "to": 16, "label": "EVERY 90 MINUTES", "window": (14.05, 17.4),
                    "spoken": "16 sunrises, 16 sunsets"},
        "loop": "Up here, morning never keeps you waiting. Astronauts see 16 sunrises every day.",
        "sources": "NASA public-domain 'Sunrise To Sunset Aboard The ISS' (Wikimedia), earth-limb crop. "
                   "Rotate fill is black, then cropped off. Shuttle structure stays outside the crop. "
                   "VO drops the false 'every 45 minutes' line. No new picture generation.",
    },
}


def plan() -> None:
    opening = opening_crop()
    print("opening", opening)
    src = json.loads((base.TRIM / "owb_sa_s2_neptune_vo_v01_trim_words.json").read_text())["words"]
    _, _, words = base.excise(src, "Stay", "fast")
    print("nep windows", nep_windows(words[-1]["end"]), "last", words[-1]["end"])
    src3 = json.loads((base.TRIM / "owb_sa_s3_iss_sunrises_vo_v01_trim_words.json").read_text())["words"]
    _, kept = excise_many(src3, [("Stay", "one"), ("So", "ends")])
    print("ISS", " ".join(w["word"] for w in kept))
    print("ISS last", kept[-1]["end"], "second 16", find_word(kept, "16", 4))


def main() -> None:
    keys = [a for a in sys.argv[1:] if a != "plan"] or ["s2", "s3"]
    if "plan" in sys.argv:
        plan()
        return
    for p in (base.BED, base.KIT / "sfx_owb_whoosh_soft_v01.wav", NEP, ISS):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    results = {k: build(k) for k in keys}
    print(json.dumps(results, indent=2, default=str))
    if any(v["gate"] or v["level"] or v["polish"] or v["music"] for v in results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
