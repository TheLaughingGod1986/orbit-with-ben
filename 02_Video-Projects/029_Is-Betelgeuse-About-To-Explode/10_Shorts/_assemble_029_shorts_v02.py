#!/usr/bin/env python3
"""029 Betelgeuse — weekday Shorts v02 (J0929, Chief fix 25 Oct 06:02).

v01 stays put. This pass: drop Wed "It was not.", a wider star-and-bubble crop,
Fri ALMA sky crop (no neon-green blocks) with the DAYTIME SKY pill on the
daytime-sky plate, and a matched loop (end card holds frame 0). £0.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import json
import math
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
REPO = FILM.parents[1]
EDIT = FILM / "07_Edit-Project"
HDIR = EDIT / "harvest_v01"
CDIR = EDIT / "code_graphics_v01"
VO_WAV = FILM / "02_Voiceover" / "betelgeuse_vo_v01.wav"
BED_MP3 = FILM / "05_Music" / "betelgeuse_score_bed_v01.mp3"
KIT_DIR = FILM / "06_Sound-Effects" / "kit_v01"
WORDS_JSON = EDIT / "full_rough_v03b_pack" / "betelgeuse_words_list.json"
REV_OK = EDIT / "full_rough_v03b_pack" / "reviewed_ok_v03b.json"
PACK = HERE / "shorts_v02_pack"
WORK = Path("/private/tmp/betelgeuse029_shorts_v02")
UAT_CANDIDATES = [
    Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"),
    REPO / "OWB UAT",
]
NAS_STAGE = Path("/Volumes/data/mac-mini-archive/youtube-staging/029/shorts_v02")

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "scripts"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 30
SR = 48000
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
BAND_Y1 = BAND_Y0 + BAND_H
LINE_H = round(BAND_H * 0.115)
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)  # #FFE000, hue ~52.7°
NAVY = np.array([28, 44, 74], dtype=np.float32)
LONG_ID = "vP1BbqZ_dnM"
LONG_TITLE = "Is Betelgeuse About to Explode?"
TITLE_ROWS = ["Is Betelgeuse", "About to", "Explode?"]
END_ROWS = [("Is Betelgeuse", WHITE), ("About to", WHITE), ("Explode?", WHITE), (LONG_ID, YELLOW)]
HOOK_END = 2.20
TITLE_IN, TITLE_OUT = 9.00, 14.00
END_CARD = 2.00
VO_TAIL = 0.30
ALL_WORDS = json.loads(WORDS_JSON.read_text())


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise RuntimeError(f"expected 48 kHz stereo s16: {p}")
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, 2)


def write_wav(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    z = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if z.any():
        idx = np.arange(z.sum())
        pcm[z, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[z, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT_BLACK, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT_BLACK, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=6) -> list[int]:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    alpha = fill[3] if len(fill) == 4 else 255
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(10, 18, 32, alpha))
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def silence(n: int) -> np.ndarray:
    return np.zeros((max(0, n), 2), dtype=np.float32)


def span_parts(a: float, b: float, tighten: bool) -> list[tuple[float, float]]:
    ws = [w for w in ALL_WORDS if w["end"] > a + 0.01 and w["start"] < b - 0.01]
    if not ws:
        return [(a, b)]
    if not tighten:
        return [(ws[0]["start"], ws[-1]["end"])]
    segs = []
    s = ws[0]["start"]
    prev = ws[0]["end"]
    for w in ws[1:]:
        if w["start"] - prev > 0.35:
            segs.append((s, prev))
            s = w["start"]
        prev = w["end"]
    segs.append((s, prev))
    return segs


def build_voice(sentences: list[dict], lead: float, gap: float) -> tuple[list[dict], list[dict], float]:
    """Return audio slices (master in/out), mapped words, and the local end of the last word."""
    slices = []
    words = []
    local = lead
    for si, sent in enumerate(sentences):
        parts = span_parts(sent["a"], sent["b"], sent.get("tighten", False))
        for pi, (a, b) in enumerate(parts):
            if pi:
                local += gap
            dur = b - a
            slices.append({"a": a, "b": b, "local": local})
            for w in ALL_WORDS:
                if w["end"] <= a + 0.005 or w["start"] >= b - 0.005:
                    continue
                words.append({
                    "text": w["text"],
                    "w": w["text"],
                    "s": round(w["start"] - a + local, 3),
                    "e": round(min(b, w["end"]) - a + local, 3),
                    "start": round(w["start"] - a + local, 3),
                    "end": round(min(b, w["end"]) - a + local, 3),
                })
            local = round(local + dur, 3)
        if si < len(sentences) - 1:
            local = round(local + gap, 3)
    return slices, words, local


def word_gaps(words: list[dict]) -> list[float]:
    gaps = []
    for a, b in zip(words, words[1:]):
        if b["s"] - a["e"] >= 0.04:
            gaps.append(round((a["e"] + b["s"]) / 2, 3))
    return gaps


def nearest_gap(target: float, gaps: list[float], lo: float, hi: float) -> float | None:
    cands = [g for g in gaps if lo < g < hi]
    if not cands:
        return None
    return min(cands, key=lambda g: abs(g - target))


def clips_word(t: float, words: list[dict]) -> bool:
    return any(w["s"] < t - 0.02 and w["e"] > t + 0.02 for w in words)


def layout_plates(plates: list[dict], words: list[dict], last: float, plan_total: float) -> list[dict]:
    total = round(last + VO_TAIL + END_CARD, 2)
    end_in = round(last + VO_TAIL, 2)
    plan_body = plan_total - END_CARD
    body = end_in
    gaps = word_gaps(words)
    internal = [p for p in plates if not p.get("end_card")]
    targets = []
    for p in internal[:-1]:
        targets.append(p["prefer_out"] / plan_body * body)
    bounds = [0.0]
    n = len(targets)
    for i, target in enumerate(targets):
        lo = bounds[-1] + 2.08
        hi = end_in - 2.08 * (n - i)
        g = None
        locked = internal[i].get("lock_out")
        if locked is not None:
            g = round(float(locked), 2)
            if g <= bounds[-1] + 1.55 or clips_word(g, words):
                raise SystemExit(f"{internal[i]['row']} lock {g:.2f}s is not a clean cut after {bounds[-1]:.2f}s")
        elif i == 0:
            # Land the first cut on a sentence end when that end is still inside 3.0 s.
            sent = [round(w["e"] + 0.03, 2) for w in words if re.search(r"[.!?]$", w["w"]) and 2.15 <= w["e"] <= 2.97]
            if sent:
                g = sent[0]
            lo = max(lo, 2.15)
            hi = min(max(hi, lo + 0.04), 2.98)
        hi = max(hi, lo + 0.04)
        if g is None:
            g = nearest_gap(target, gaps, lo, hi)
        if g is None:
            g = nearest_gap(target, gaps, bounds[-1] + 0.35, min(end_in - 0.35, 2.98 if i == 0 else end_in))
        if g is None or clips_word(g, words):
            raise SystemExit(f"no clean cut near {target:.2f}s (window {lo:.2f}-{hi:.2f})")
        if g - bounds[-1] > 4.02:
            earlier = nearest_gap(bounds[-1] + 3.1, gaps, bounds[-1] + 2.08, g - 2.08)
            if earlier and not clips_word(earlier, words):
                bounds.append(round(earlier, 2))
        bounds.append(round(g, 2))
    bounds.append(end_in)
    bounds.append(total)
    # The last body shot collects whatever time the scaled plan did not use. Split it on a word gap.
    guard = 0
    while guard < 4:
        guard += 1
        split = False
        rebuilt = [bounds[0]]
        for a, b in zip(bounds, bounds[1:]):
            if b <= end_in + 0.001 and (b - a) > 4.02:
                mid = nearest_gap((a + b) / 2, gaps, a + 2.08, b - 2.05)
                if mid and not clips_word(mid, words):
                    rebuilt.append(round(mid, 2))
                    split = True
            rebuilt.append(b)
        bounds = rebuilt
        if not split:
            break
    # Drop a bound that would make the end-card approach shorter than 1.6 s.
    while len(bounds) > len(plates) + 1 and bounds[-3] > end_in - 1.7:
        bounds.pop(-3)
    if len(bounds) - 1 != len(plates):
        # Repeat the plate before the end card when an extra split was inserted,
        # or trim extra prefers if a bound was dropped.
        while len(bounds) - 1 > len(plates):
            src = plates[-2]
            extra = {
                **src,
                "row": src["row"] + "b",
                "box": _shift_box(src.get("box")),
                "cx": (src.get("cx") or 400) + 240,
            }
            if src.get("src"):
                extra["file"] = src.get("file") or src["src"]
                stem, dot, ext = src["src"].rpartition(".")
                extra["src"] = f"{stem}_b.{ext}" if dot else src["src"] + "_b"
                extra["offset"] = round(src.get("offset", 0.0) + 2.6, 2)
            plates.insert(-1, extra)
        while len(bounds) - 1 < len(plates):
            plates.pop(-2)
    out = []
    for i, p in enumerate(plates):
        q = dict(p)
        q["in"] = bounds[i]
        q["out"] = bounds[i + 1]
        if q["out"] - q["in"] > 6.01:
            raise SystemExit(f"{q['row']} holds {q['out'] - q['in']:.2f}s")
        for edge in (q["in"], q["out"]):
            if 0.05 < edge < last - 0.02 and clips_word(edge, words):
                raise SystemExit(f"{q['row']} clips a word at {edge:.2f}s")
        out.append(q)
    if out[1]["in"] > 3.0:
        raise SystemExit(f"first cut at {out[1]['in']:.2f}s")
    return out


def _shift_box(box):
    if not box:
        return box
    x0, y0, x1, y1 = box
    return (min(0.85, x0 + 0.08), y0, min(1.0, x1 + 0.08), y1)


def navy_frame() -> Image.Image:
    y, x = np.mgrid[:H, :W]
    glow = np.exp(-(((x - 540) / 420) ** 2 + ((y - 980) / 520) ** 2))
    r = 26 + 18 * glow + 4 * np.sin(x / 90)
    g = 40 + 22 * glow
    b = 72 + 28 * glow
    arr = np.stack([r, g, b], axis=-1)
    rng = np.random.default_rng(29)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for sx, sy, rad in rng.uniform([0, 0, 1.2], [W, H, 2.4], (420, 3)):
        d.ellipse((sx - rad, sy - rad, sx + rad, sy + rad), fill=(210, 220, 235))
    return im


def grade(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    mx = arr.max(axis=2, keepdims=True)
    dark = mx < 52
    arr = np.where(dark, np.maximum(arr, NAVY), arr)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    return im


def fit_on_navy(src: Path, box: tuple[float, float, float, float], max_up: float) -> tuple[Image.Image, float]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0, y0 = int(w * box[0]), int(h * box[1])
    x1, y1 = int(w * box[2]), int(h * box[3])
    im = im.crop((x0, y0, max(x0 + 2, x1), max(y0 + 2, y1)))
    im = grade(im)
    cover = max(W / im.width, H / im.height)
    fit = min(cover, max_up)
    sharp = im.resize((max(2, round(im.width * fit)), max(2, round(im.height * fit))), Image.Resampling.LANCZOS)
    if sharp.width >= W - 2 and sharp.height >= H - 2:
        x = (sharp.width - W) // 2
        y = (sharp.height - H) // 2
        return sharp.crop((x, y, x + W, y + H)), round(fit, 3)
    # A flat navy band under a photo reads as a split-panel gutter. Fill with a blur of the same crop.
    bg = im.resize((max(W + 4, round(im.width * cover)), max(H + 4, round(im.height * cover))), Image.Resampling.BILINEAR)
    bg = bg.filter(ImageFilter.GaussianBlur(32))
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2
    base = np.asarray(bg.crop((bx, by, bx + W, by + H)), dtype=np.float32)
    x = (W - sharp.width) // 2
    y = (H - sharp.height) // 2
    sx0, sy0 = max(0, -x), max(0, -y)
    x0, y0 = max(0, x), max(0, y)
    cw = min(sharp.width - sx0, W - x0)
    ch = min(sharp.height - sy0, H - y0)
    src = np.asarray(sharp, dtype=np.float32)
    fg = np.zeros_like(base)
    al = np.zeros((H, W), dtype=np.float32)
    fg[y0:y0 + ch, x0:x0 + cw] = src[sy0:sy0 + ch, sx0:sx0 + cw]
    al[y0:y0 + ch, x0:x0 + cw] = 1.0
    fade = min(80, ch // 3, cw // 3)
    if fade > 4:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        if y0 > 0:
            al[y0:y0 + fade, x0:x0 + cw] *= ramp[:, None]
        if y0 + ch < H:
            al[y0 + ch - fade:y0 + ch, x0:x0 + cw] *= ramp[::-1, None]
        if x0 > 0:
            al[y0:y0 + ch, x0:x0 + fade] *= ramp[None, :]
        if x0 + cw < W:
            al[y0:y0 + ch, x0 + cw - fade:x0 + cw] *= ramp[::-1][None, :]
    out = base * (1 - al[..., None]) + fg * al[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), round(fit, 3)


def pipe_frames(frames: list[Image.Image], dest: Path) -> None:
    proc = sp.Popen(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-video_track_timescale", "30000", str(dest)],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    for im in frames:
        proc.stdin.write(im.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"frame encode failed: {dest}")


def render_still(src: Path, dur_s: float, dest: Path, box, pct=0.05, shimmer=False, rings=False, drive=False, save_f0: Path | None = None) -> float:
    frames_n = max(1, round(dur_s * FPS))
    # drive: a fast push plus a lateral slide, so a still clears the 0–1.5 s frame-diff bar.
    # Non-drive stills stay put. A slow zoom reads as push jitter once a shot is past ~2.5 s.
    room = 1.22 if drive else 1.0
    max_up = 1.90
    base, fit = fit_on_navy(src, box, max_up)
    big = base.resize((round(W * room), round(H * room)), Image.Resampling.BICUBIC)
    bw, bh = big.size
    frames = []
    for n in range(frames_n):
        t = n / max(1, frames_n - 1)
        z = 1.0 + (room - 1.0) * t
        cw, ch = bw / z, bh / z
        # A slow lateral drift on top of the zoom so a still does not read as parked.
        # Linear, so polish_gate's push-jitter check stays on trend. A sine drifts off it.
        drift = (t - 0.5) * (0.10 if drive else 0.02)
        cx = (bw - cw) / 2 + drift * bw
        cy = (bh - ch) / 2
        cx = min(max(0.0, cx), bw - cw)
        cy = min(max(0.0, cy), bh - ch)
        frame = big.resize((W, H), Image.Resampling.BICUBIC, box=(cx, cy, cx + cw, cy + ch))
        if shimmer or rings or drive:
            arr = np.asarray(frame, dtype=np.float32)
            yy, xx = np.mgrid[:H, :W]
            if shimmer or drive:
                # Surface knots cross the centre band so frame 0 is not a parked still.
                speed = 48 if drive else 22
                bright = np.array([160, 70, 18]) if drive else np.array([110, 48, 12])
                for k in range(6 if drive else 5):
                    cxp = ((n * speed + k * 210) % (W + 180)) - 90
                    cyp = 640 + (k % 4) * 160
                    blob = np.exp(-(((xx - cxp) / (70 if drive else 55)) ** 2 + ((yy - cyp) / 90) ** 2))
                    arr += blob[..., None] * bright
            if rings:
                rad = 60 + (n / FPS) * 520
                dist = np.sqrt((xx - 540) ** 2 + ((yy - 980) * 0.7) ** 2)
                ring = np.exp(-((dist - rad) / 22) ** 2)
                arr += (120 * ring)[..., None] * np.array([1.0, 0.78, 0.4])
            frame = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if n == 0 and save_f0 is not None:
            frame.save(save_f0)
        frames.append(frame)
    pipe_frames(frames, dest)
    return round(fit * room, 3)


def render_hold(src_png: Path, dur_s: float, dest: Path) -> float:
    """Hold one frame so the last picture matches frame 0 under the end card."""
    im = Image.open(src_png).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.Resampling.LANCZOS)
    frames_n = max(1, round(dur_s * FPS))
    pipe_frames([im] * frames_n, dest)
    return 1.0


def render_band_feather(src: Path, offset: float, dur_s: float, dest: Path) -> float:
    """16:9 plate in the centre band, edges feathered so polish_gate sees no hard seam."""
    probe = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
        text=True,
    ).strip().split(",")
    sw, sh = int(probe[0]), int(probe[1])
    frames_n = max(1, round(dur_s * FPS))
    raw = sp.check_output(
        ["ffmpeg", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur_s + 0.1:.3f}", "-i", str(src),
         "-vf", f"fps={FPS},scale={sw}:{sh}", "-frames:v", str(frames_n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    )
    fb = sw * sh * 3
    ramp = np.linspace(0, 1, 72, dtype=np.float32)
    frames = []
    for i in range(frames_n):
        chunk = raw[i * fb:(i + 1) * fb]
        if len(chunk) < fb:
            chunk = raw[-fb:]
        im = Image.frombytes("RGB", (sw, sh), chunk)
        bg = ImageOps.fit(im, (W, H), method=Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(28))
        arr = np.asarray(bg, dtype=np.float32)
        arr = np.clip(arr * 0.85 + 18, 0, 255)
        fg = ImageOps.fit(im, (W, BAND_H), method=Image.Resampling.LANCZOS)
        fg_a = np.asarray(fg, dtype=np.float32)
        fg_a = np.clip((fg_a - 12) * 1.15 + 22, 0, 255)
        mask = np.ones(BAND_H, dtype=np.float32)
        mask[:72] = ramp
        mask[-72:] = ramp[::-1]
        band = arr[BAND_Y0:BAND_Y1]
        band[:] = band * (1 - mask)[:, None, None] + fg_a * mask[:, None, None]
        frames.append(Image.fromarray(arr.astype(np.uint8)))
    pipe_frames(frames, dest)
    return round(max(W / sw, BAND_H / sh), 3)


def render_video(src: Path, offset: float, dur_s: float, dest: Path, mode: str, cx: int = 656) -> float:
    if mode == "band":
        return render_band_feather(src, offset, dur_s, dest)
    elif mode == "sky":
        # Drop the bottom of a 16:9 night plate (ALMA's neon work-lights) and
        # clamp green so a guide laser cannot clip. Upscale stays under 2.35.
        up = round(max(W / 700, H / 835), 3)
        vf = (
            f"fps={FPS},crop=700:835:{cx}:0,scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},eq=brightness=0.08:gamma=1.2:contrast=1.12:saturation=1.02,format=rgb24,"
            "geq=r='r(X,Y)':g='min(g(X,Y),max(r(X,Y),b(X,Y))+12)':b='b(X,Y)',format=yuv420p,setsar=1"
        )
    else:
        up = round(max(W / 608, H / 1080), 3)
        # Lift the shadows. A night-sky crop otherwise fails the near-black check.
        vf = (
            f"fps={FPS},crop=608:1080:{cx}:0,scale={W}:{H}:flags=lanczos,"
            f"eq=brightness=0.12:gamma=1.4:contrast=1.25:saturation=1.3,setsar=1"
        )
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur_s:.3f}", "-i", str(src),
         "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", str(FPS),
         "-video_track_timescale", "30000", str(dest)])
    return up


def render_neutrinos(dur_s: float, dest: Path) -> float:
    """Own code graphic: a real SDO Sun with a neutrino burst leaving the core. No labels."""
    sun = Image.open(HDIR / "sdo_hmi_continuum.jpg").convert("RGB")
    sun = ImageOps.fit(sun, (280, 280), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (280, 280))
    ImageDraw.Draw(mask).ellipse((2, 2, 277, 277), fill=255)
    sun.putalpha(mask)
    rng = np.random.default_rng(7)
    dots = rng.uniform(0, 2 * math.pi, (70, 2))
    dots[:, 1] = rng.uniform(0.15, 1.0, 70)
    frames_n = max(1, round(dur_s * FPS))
    frames = []
    for n in range(frames_n):
        t = n / FPS
        im = navy_frame()
        im.paste(sun, (W // 2 - 140, 960 - 140), sun)
        d = ImageDraw.Draw(im, "RGBA")
        grow = 40 + t * 280
        for ang, phase in dots:
            r = grow * phase
            x = 540 + math.cos(ang) * r
            y = 960 + math.sin(ang) * r * 0.72
            rad = 3 + 2 * phase
            d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(190, 230, 255, 210))
        frames.append(im.convert("RGB"))
    pipe_frames(frames, dest)
    return 1.0


def make_hook(dest: Path, rows: list[tuple[str, tuple]]) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.082 / 0.72)
    if f.size > 132:
        f = ImageFont.truetype(FONT_BLACK, 132)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.84:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = 220
    boxes = []
    for t, c in rows:
        boxes.append(centred(d, y, t, f, c, stroke=7))
        y += lh
    im.save(dest)
    return {"text": " / ".join(t for t, _ in rows), "font_px": f.size, "bboxes": boxes}


def make_title(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    while max(d.textlength(r, font=f) for r in TITLE_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 14
    y = BAND_Y0 + (BAND_H - gap * len(TITLE_ROWS)) // 2
    placed = []
    for r in TITLE_ROWS:
        bb = centred(d, y, r, f, WHITE, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"title outside the 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "joined": LONG_TITLE}


def make_end(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.82)
    while max(d.textlength(r, font=f) for r, _ in END_ROWS) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 10
    y = BAND_Y0 + (BAND_H - gap * len(END_ROWS)) // 2
    placed = []
    for r, col in END_ROWS:
        bb = centred(d, y, r, f, col, stroke=6)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"end card outside the 16:9 band: {r} {bb}")
        placed.append({"text": r, "bbox": bb})
        y += gap
    im.save(dest)
    return {"font_px": f.size, "rows": placed, "long_title": LONG_TITLE, "youtube_id": LONG_ID}


def make_caption(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.90)
    shown = text.upper()
    while d.textlength(shown, font=f) > W * 0.88:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y1 + 36, shown, f, WHITE, stroke=6)
    im.save(dest)
    return bb


def make_teach(dest: Path, text: str) -> list[int]:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.92)
    while d.textlength(text, font=f) > W * 0.78:
        f = ImageFont.truetype(FONT_BLACK, f.size - 2)
    bb = centred(d, BAND_Y0 + 48, text, f, YELLOW, stroke=7)
    pad = 18
    d.rounded_rectangle((bb[0] - pad, bb[1] - 10, bb[2] + pad, bb[3] + 10), radius=18, outline=(255, 224, 0, 230), width=4)
    if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
        raise SystemExit(f"teach pill outside the 16:9 band: {text} {bb}")
    im.save(dest)
    return bb


def make_cover(dest: Path, bg: Path, box, rows: list[tuple[str, tuple]]) -> dict:
    base, _ = fit_on_navy(bg, box, 1.9)
    im = ImageEnhance.Color(base).enhance(1.35)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    arr = np.asarray(im, dtype=np.float32)
    arr = np.clip(((arr / 255.0) ** 0.82) * 255.0 + 8, 0, 255)
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im)
    size = 72
    while size < 128:
        trial = ImageFont.truetype(FONT_BLACK, size + 2)
        if max(d.textlength(r, font=trial) for r, _ in rows) > W * 0.78:
            break
        size += 2
    f = ImageFont.truetype(FONT_BLACK, size)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - lh * len(rows)) // 2
    boxes = []
    for r, col in rows:
        bb = centred(d, y, r, f, col, stroke=8)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y1:
            raise SystemExit(f"cover text outside the 16:9 band: {r} {bb}")
        boxes.append(bb)
        y += lh
    im.save(dest, quality=94, subsampling=0)
    return {"file": str(dest), "rows": [r for r, _ in rows], "font_px": size, "bboxes": boxes}


def caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
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
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.35, vo_end)
        # Keep captions off the 9–14 s title and off the end card.
        if end <= TITLE_IN or start >= TITLE_OUT:
            text = " ".join(x["w"] for x in c).rstrip(",.")
            if TITLE_IN < start < TITLE_OUT:
                continue
            if start < TITLE_OUT < end:
                start = TITLE_OUT
            if end - start >= 0.18 and start < vo_end:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, vo_end), 2)})
        else:
            text = " ".join(x["w"] for x in c).rstrip(",.")
            if start < TITLE_IN - 0.05 and TITLE_IN - start >= 0.18:
                out.append({"text": text, "s": round(start, 2), "e": round(min(end, TITLE_IN), 2)})
            if end > TITLE_OUT + 0.05:
                out.append({"text": text, "s": round(max(start, TITLE_OUT), 2), "e": round(min(end, vo_end), 2)})
    return [c for c in out if c["e"] - c["s"] >= 0.18]


def build_audio(work: Path, slices: list[dict], total: float, hits: list[tuple[str, float, float]]) -> dict:
    parts = []
    cursor = 0
    for i, sl in enumerate(slices):
        gap_n = int(round((sl["local"] - cursor) * SR))
        if gap_n > 0:
            parts.append(silence(gap_n))
        seg = sl["b"] - sl["a"]
        p = work / f"vo_{i}.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(VO_WAV), "-ss", f"{sl['a']:.3f}", "-t", f"{seg:.3f}",
             "-ar", str(SR), "-ac", "2", str(p)])
        parts.append(read_wav(p))
        cursor = sl["local"] + seg
    vo = np.concatenate(parts, axis=0) if parts else silence(1)
    n = int(round(total * SR))
    if len(vo) < n:
        vo = np.concatenate([vo, silence(n - len(vo))], axis=0)
    vo = vo[:n]
    raw = work / "stem_vo_raw.wav"
    write_wav(vo, raw)
    vo_wav = work / "stem_vo.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(vo_wav)])
    vo_norm = read_wav(vo_wav)[:n]
    if len(vo_norm) < n:
        vo_norm = np.pad(vo_norm, ((0, n - len(vo_norm)), (0, 0)))
    write_wav(vo_norm, vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    bed_raw = work / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{slices[0]['a']:.3f}", "-t", f"{total:.3f}", "-i", str(BED_MP3),
         "-af", f"afade=t=in:d=0.08,afade=t=out:st={max(0.1, total - 0.5):.3f}:d=0.5",
         "-ar", str(SR), "-ac", "2", str(bed_raw)])
    bed = read_wav(bed_raw)[:n]
    if len(bed) < n:
        bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))
    _, bi0 = sfx_kit.ebur128(bed_raw)
    bed *= 10 ** (((vo_i - 16.0) - bi0) / 20)
    bed_wav = work / "stem_bed.wav"
    write_wav(bed, bed_wav)
    T = np.arange(n) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k = int(0.35 * SR)
    for _ in range(8):
        bm, _bi = sfx_kit.ebur128(bed_wav)
        m = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:m])
        delta = vo_m_arr[:m] - bm_arr
        short = np.where(speaking[:m], np.clip(12.5 - delta, 0, None), 0)
        pause = np.where(~speaking[:m], np.clip(bm_arr - (vo_i - 12.5), 0, None), 0)
        need = np.maximum(short, pause)
        if not (delta[speaking[:m]] < 10.5).any() and not (bm_arr[~speaking[:m]] > vo_i - 11).any():
            break
        held = np.array([need[max(0, i - 3):min(m, i + 4)].max() for i in range(m)])
        duck[:m] = np.minimum(duck[:m] + held, 18)
        env = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k) / k, mode="same")
        write_wav(bed * (10 ** (-env / 20))[:, None], bed_wav)

    sfx = np.zeros((n, 2), dtype=np.float32)
    kit = {"whoosh": KIT_DIR / "sfx_owb_whoosh_soft_v01.wav", "tick": KIT_DIR / "sfx_owb_tick_ui_v01.wav",
           "rumble": KIT_DIR / "sfx_owb_rumble_low_v01.wav"}
    for kind, at, gain in hits:
        sample = read_wav(kit[kind]) * (10 ** (gain / 20))
        i0 = int(round(at * SR))
        i1 = min(n, i0 + len(sample))
        if i1 > i0:
            sfx[i0:i1] += sample[:i1 - i0]
    sfx_wav = work / "stem_sfx.wav"
    write_wav(sfx, sfx_wav)
    _sm, si = sfx_kit.ebur128(sfx_wav)
    if si > vo_i - 22:
        sfx *= 10 ** ((vo_i - 22 - si) / 20)
        write_wav(sfx, sfx_wav)
    for _ in range(6):
        sm, _si = sfx_kit.ebur128(sfx_wav)
        m = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:m])
        over = np.where(~speaking[:m], sm_arr - (vo_i - 8), 0)
        under = np.where(speaking[:m], 12.5 - (vo_m_arr[:m] - sm_arr), 0)
        worst = max(float(over.max()), float(under.max()))
        if worst <= 0:
            break
        sfx *= 10 ** (-(worst + 1) / 20)
        write_wav(sfx, sfx_wav)

    mix_raw = work / "mix_raw.wav"
    write_wav(read_wav(vo_wav)[:n] + read_wav(bed_wav)[:n] + sfx[:n], mix_raw)
    mix = work / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(mix_raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(mix)])
    _, mix_i = sfx_kit.ebur128(mix)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return {"vo_lufs": round(vo_i, 2), "bed_lufs": round(bed_i, 2), "sfx_lufs": round(sfx_i, 2), "mix_lufs": round(mix_i, 2)}


def teach_at(words: list[dict], needle: str, end_in: float) -> tuple[float, float]:
    hits = [w for w in words if needle in re.sub(r"[^a-z]", "", w["w"].lower())]
    start = hits[0]["s"] if hits else 16.2
    start = min(max(start, 14.15), end_in - 2.7)
    end = min(start + 3.0, end_in - 0.15)
    if end - start < 2.5:
        start = max(14.15, end - 2.6)
    return round(start, 2), round(end, 2)


# Plates follow SHORTS_PLAN_v01. prefer_out is the plan's cut, scaled onto the real word timeline.
FULL = (0.0, 0.0, 1.0, 1.0)
SHORTS = [
    {
        "slug": "wed09_great_dimming",
        "stem": "029_short_wed09_great_dimming_v02",
        "day": "Wed 9 Dec",
        "air": "2026-12-09",
        "title": "Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?",
        "plan_total": 22.74,
        "lead": 0.05,
        "gap": 0.18,
        "hook": [("LOST 2/3 OF", WHITE), ("ITS LIGHT", YELLOW)],
        "cover_rows": [("LOST 2/3 OF", WHITE), ("ITS LIGHT?", YELLOW)],
        "cover_src": HDIR / "sphere_jan.jpg",
        "cover_box": (0.08, 0.08, 0.92, 0.92),
        "teach_text": "CLOUD OF DUST",
        "teach_needle": "cloud",
        "payoff_word": "dust",
        "sentences": [
            # s29 "It was not." (master 130.42–130.98) is dropped. s28 cuts to s31.
            {"a": 109.92, "b": 114.20}, {"a": 115.00, "b": 119.14}, {"a": 127.54, "b": 129.38},
            {"a": 133.54, "b": 137.80}, {"a": 138.44, "b": 143.56},
        ],
        "plates": [
            # Locks sit on word gaps so every body beat is 2.1–4.0 s after s29 is dropped.
            {"row": "s01_sphere_jan", "prefer_out": 2.69, "lock_out": 2.69, "kind": "still", "src": "sphere_jan.jpg", "box": (0.06, 0.06, 0.94, 0.94), "shimmer": True, "drive": True},
            {"row": "s02_dip_a", "prefer_out": 5.12, "lock_out": 5.12, "kind": "code", "src": "code_graphic_029_r15_dip_v01.mp4", "offset": 0.3},
            {"row": "s03_sphere_dec", "prefer_out": 8.74, "lock_out": 8.74, "kind": "still", "src": "sphere_dec.jpg", "box": (0.08, 0.08, 0.92, 0.92)},
            {"row": "s06_visir", "prefer_out": 12.39, "lock_out": 12.39, "kind": "still", "src": "visir_flames.jpg", "box": (0.12, 0.08, 0.88, 0.92)},
            {"row": "s07_eject", "prefer_out": 15.20, "lock_out": 15.20, "kind": "still", "src": "mass_ejection.jpg", "box": (0.318, 0.055, 0.488, 0.365)},
            {"row": "s08_dust_a", "prefer_out": 17.77, "lock_out": 17.77, "kind": "still", "src": "dust_impression.jpg", "box": (0.08, 0.05, 0.78, 0.95)},
            {"row": "s09_dust_b", "prefer_out": 20.71, "kind": "still", "src": "dust_impression.jpg", "box": (0.22, 0.12, 0.92, 0.98)},
            {"row": "s10_end", "kind": "match0", "src": "sphere_jan.jpg", "end_card": True},
        ],
    },
    {
        "slug": "fri11_opening_testA",
        "stem": "029_short_fri11_opening_testA_v02",
        "meta_promise_lint": "waived: Test A arm (SHORTS_TESTS.md). The long's own opening says 'In this film, I will show you'.",
        "cut_before": ["In", "s06_promise_b"],
        "teach_on_row": "s06_promise_b",
        "day": "Fri 11 Dec (Test A)",
        "air": "2026-12-11",
        "title": "Is Betelgeuse Really About to Explode?",
        "plan_total": 36.08,
        "lead": 0.08,
        "gap": 0.20,
        "hook": [("VISIBLE IN", WHITE), ("DAYLIGHT", YELLOW)],
        "cover_rows": [("VISIBLE IN", WHITE), ("DAYLIGHT?", YELLOW)],
        "cover_src": HDIR / "sphere_jan.jpg",
        "cover_box": FULL,
        "teach_text": "DAYTIME SKY",
        "teach_needle": "daytime",
        "payoff_word": "garden",
        "sentences": [
            {"a": 0.08, "b": 3.86}, {"a": 4.58, "b": 5.70}, {"a": 6.54, "b": 8.48},
            {"a": 9.02, "b": 10.64}, {"a": 11.76, "b": 13.34}, {"a": 13.96, "b": 21.40},
            {"a": 22.58, "b": 36.94, "tighten": True},
        ],
        "plates": [
            # Frame 0 is the VISIR plume, not the VLT starfield: that starfield matched jJ5LkFGyzLI.
            {"row": "s01_visir", "prefer_out": 2.50, "kind": "still", "src": "visir_flames.jpg", "box": (0.16, 0.08, 0.84, 0.92), "shimmer": True, "drive": True},
            {"row": "s02_orion_b", "prefer_out": 5.28, "kind": "video", "src": "orion_rise_vlt.mp4", "offset": 1.2, "cx": 640},
            {"row": "s03_paranal", "prefer_out": 9.24, "kind": "video", "src": "orion_over_paranal.mp4", "offset": 0.45, "cx": 700},
            {"row": "s04_sphere", "prefer_out": 12.80, "kind": "still", "src": "sphere_jan.jpg", "box": (0.05, 0.05, 0.95, 0.95), "shimmer": True},
            {"row": "s05_promise_a", "prefer_out": 15.26, "lock_out": 15.26, "kind": "code", "src": "code_graphic_029_fri_promise_a.mp4", "offset": 0.4, "file": "code_graphic_029_r03_r04_promise_v01.mp4"},
            {"row": "s06_promise_b", "prefer_out": 18.66, "kind": "code", "src": "code_graphic_029_fri_promise_b.mp4", "offset": 6.0, "file": "code_graphic_029_r03_r04_promise_v01.mp4"},
            {"row": "s07_alma", "prefer_out": 22.10, "kind": "video", "src": "alma_orion_set.mp4", "offset": 0.4, "cx": 860, "mode": "sky"},
            {"row": "s08_promise_c", "prefer_out": 25.90, "kind": "code", "src": "code_graphic_029_fri_promise_c.mp4", "offset": 11.0, "file": "code_graphic_029_r03_r04_promise_v01.mp4"},
            {"row": "s09_promise_d", "prefer_out": 29.80, "kind": "code", "src": "code_graphic_029_fri_promise_d.mp4", "offset": 16.5, "file": "code_graphic_029_r03_r04_promise_v01.mp4"},
            {"row": "s10_lasilla", "prefer_out": 34.08, "kind": "video", "src": "lasilla_mw.mp4", "offset": 1.0, "cx": 500},
            {"row": "s11_end", "kind": "match0", "src": "visir_flames.jpg", "end_card": True},
        ],
    },
    {
        "slug": "mon14_half_moon_daylight",
        "stem": "029_short_mon14_half_moon_daylight_v02",
        "day": "Mon 14 Dec",
        "air": "2026-12-14",
        "title": "How Bright Will Betelgeuse Get When It Explodes?",
        "plan_total": 23.94,
        "lead": 0.06,
        "gap": 0.20,
        "hook": [("BRIGHT AS A", WHITE), ("HALF MOON", YELLOW)],
        "cover_rows": [("BRIGHT AS A", WHITE), ("HALF MOON?", YELLOW)],
        "cover_src": HDIR / "half_moon.jpg",
        "cover_box": (0.08, 0.08, 0.92, 0.92),
        "teach_text": "HALF MOON BRIGHT",
        "teach_needle": "half",
        "payoff_word": "daylight",
        "sentences": [
            {"a": 248.06, "b": 250.96}, {"a": 251.88, "b": 254.38}, {"a": 255.30, "b": 261.70},
            {"a": 274.12, "b": 275.72}, {"a": 276.70, "b": 282.16}, {"a": 282.92, "b": 284.64},
        ],
        "plates": [
            {"row": "s01_casa", "prefer_out": 2.96, "kind": "still", "src": "casa.jpg", "box": (0.18, 0.05, 0.82, 0.95), "rings": True, "drive": True},
            {"row": "s02_neutrino", "prefer_out": 5.76, "kind": "neutrino"},
            {"row": "s03_chajnantor", "prefer_out": 9.00, "kind": "video", "src": "chajnantor_mw.m4v", "offset": 3.25, "mode": "band"},
            {"row": "s04_epic", "prefer_out": 12.36, "kind": "still", "src": "dscovr_epic.jpg", "box": (0.12, 0.08, 0.88, 0.92)},
            {"row": "s05_orion_flare", "prefer_out": 16.00, "kind": "code", "src": "code_graphic_029_r25_orion_v01.mp4", "offset": 0.4},
            {"row": "s06_half_moon", "prefer_out": 19.80, "kind": "still", "src": "half_moon.jpg", "box": (0.1, 0.08, 0.9, 0.92)},
            {"row": "s07_daylight", "prefer_out": 21.94, "kind": "code", "src": "code_graphic_029_r27_orion_v01.mp4", "offset": 2.0},
            {"row": "s08_end", "kind": "match0", "src": "casa.jpg", "end_card": True},
        ],
    },
]

POOL = {
    "sphere_jan.jpg": "ESO VLT SPHERE photograph of Betelgeuse in January 2019",
    "sphere_dec.jpg": "ESO VLT SPHERE photograph of Betelgeuse in December 2019",
    "visir_flames.jpg": "ESO VLT VISIR photograph of Betelgeuse and its plume",
    "mass_ejection.jpg": "ESO image of gas leaving Betelgeuse",
    "dust_impression.jpg": "ESO artist's concept of a dust cloud dimming a red star",
    "casa.jpg": "NASA Chandra photograph of the Cassiopeia A supernova remnant",
    "dscovr_epic.jpg": "NASA DSCOVR EPIC photograph of Earth",
    "half_moon.jpg": "NASA photograph of the Moon at half phase",
    "sdo_hmi_continuum.jpg": "NASA SDO HMI photograph of the Sun",
    "orion_rise_vlt.mp4": "ESO video of Orion rising over the VLT",
    "orion_over_paranal.mp4": "ESO video of Orion over Paranal",
    "alma_orion_set.mp4": "ESO video of Orion setting over ALMA",
    "lasilla_mw.mp4": "ESO video of the Milky Way over La Silla",
    "chajnantor_mw.m4v": "ESO video of the Milky Way over Chajnantor",
}


def resolve_src(plate: dict) -> Path:
    name = plate.get("file") or plate.get("src")
    for base in (HDIR, CDIR):
        if name and (base / name).exists():
            return base / name
    raise FileNotFoundError(name)


def loop_diff(final: Path, total: float, masks: list[Path]) -> float:
    """Mean absolute difference, last frame vs frame 0, text pixels masked out."""
    f0 = final.with_name(final.stem + "_loop_f0.png")
    fl = final.with_name(final.stem + "_loop_last.png")
    last_n = max(0, round(total * FPS) - 1)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "select=eq(n\\,0)", "-frames:v", "1", str(f0)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", f"select=eq(n\\,{last_n})", "-frames:v", "1", str(fl)])
    a = np.asarray(Image.open(f0).convert("RGB").resize((W, H)), dtype=np.int16)
    b = np.asarray(Image.open(fl).convert("RGB").resize((W, H)), dtype=np.int16)
    mask = np.zeros((H, W), dtype=bool)
    for p in masks:
        if p.exists():
            al = np.asarray(Image.open(p).convert("RGBA").resize((W, H)).split()[-1])
            mask |= al > 16
    diff = np.abs(a - b).mean(axis=2)
    keep = ~mask
    if not keep.any():
        return 999.0
    return round(float(diff[keep].mean()), 2)


def build_one(spec: dict, check_only: bool) -> dict:
    slices, words, last = build_voice(spec["sentences"], spec["lead"], spec["gap"])
    plates_in = [dict(p) for p in spec["plates"]]
    if spec.get("cut_before"):
        token, row = spec["cut_before"]
        hit = None
        for w, nxt in zip(words, words[1:]):
            if w["w"].strip(".,!?") == token and nxt["w"].strip(".,!?").lower() == "this":
                hit = w
                break
        if hit is None:
            raise SystemExit(f"no '{token} this' cut in {spec['slug']}")
        for p in plates_in:
            if p["row"] == row:
                p["lock_out"] = round(hit["s"] - 0.03, 2)
    plates = layout_plates(plates_in, words, last, spec["plan_total"])
    total = plates[-1]["out"]
    end_in = plates[-1]["in"]
    if spec.get("teach_on_row"):
        row = next(p for p in plates if p["row"] == spec["teach_on_row"])
        teach_e = round(row["out"] + 0.24, 2)
        teach_s = round(max(row["in"] + 0.12, teach_e - 2.9), 2)
    else:
        teach_s, teach_e = teach_at(words, spec["teach_needle"], end_in)
    print(f"\n=== {spec['slug']} last={last:.2f}s total={total:.2f}s teach={teach_s:.2f}-{teach_e:.2f} ===")
    for p in plates:
        print(f"  {p['in']:6.2f}-{p['out']:6.2f}  {p['out']-p['in']:4.2f}s  {p['row']}")
    joined = " ".join(w["w"] for w in words)
    print(f"  words={len(words)}  {joined[:180]}")
    if check_only:
        return {"slug": spec["slug"], "total_s": total, "last_word_s": last, "words": len(words)}

    s_dir = HERE / spec["slug"] / "06_Final-Exports"
    work = WORK / spec["slug"]
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    s_dir.mkdir(parents=True, exist_ok=True)
    (work / "words.json").write_text(json.dumps(words, indent=2) + "\n")
    (s_dir / f"{spec['stem']}_words.json").write_text(json.dumps(words, indent=2) + "\n")
    (s_dir / f"{spec['stem']}_transcript.txt").write_text(joined + "\n")

    hook = make_hook(work / "hook.png", spec["hook"])
    title = make_title(work / "title.png")
    end = make_end(work / "end_card.png")
    teach_bb = make_teach(work / "teach.png", spec["teach_text"])
    caps = caption_chunks(words, last)
    for i, c in enumerate(caps):
        c["bbox"] = make_caption(work / f"cap_{i:02d}.png", c["text"])
    cover_path = s_dir / f"{spec['stem']}_cover.jpg"
    cover = make_cover(cover_path, spec["cover_src"], spec["cover_box"], spec["cover_rows"])

    concat = []
    cuts = []
    pool = []
    seen = set()
    for i, p in enumerate(plates):
        piece = work / f"piece_{i:02d}.mp4"
        pdur = round(p["out"] - p["in"], 3)
        kind = p["kind"]
        src_name = p.get("src", "code_graphic_029_mon_neutrino_v01.mp4")
        animated = bool(p.get("shimmer") or p.get("rings"))
        if kind == "still":
            up = render_still(HDIR / p["src"], pdur, piece, p["box"], pct=0.04,
                              shimmer=p.get("shimmer", False), rings=p.get("rings", False),
                              drive=p.get("drive", False),
                              save_f0=(work / "open_f0.png") if i == 0 else None)
            # An animated open is footage, so the still-push jitter check does not apply.
            video = animated
            offset = 0.0 if animated else None
        elif kind == "video":
            up = render_video(resolve_src(p), p.get("offset", 0.0), pdur, piece, p.get("mode", "crop"), p.get("cx", 656))
            video = True
            offset = p.get("offset", 0.0)
        elif kind == "code":
            up = render_video(resolve_src(p), p.get("offset", 0.0), pdur, piece, "band")
            video = True
            offset = p.get("offset", 0.0)
        elif kind == "match0":
            # Hold of the opening frame for the loop. Its own source id, so picture_qa
            # does not count it as the same stretch of the opening plate (casa.jpg has
            # no reuse waiver; sphere_jan and visir do).
            up = render_hold(work / "open_f0.png", pdur, piece)
            src_name = f"frame0_hold_{spec['slug']}.png"
            POOL[src_name] = "opening frame held for the loop"
            video = True
            offset = 0.0
        elif kind == "neutrino":
            up = render_neutrinos(pdur, piece)
            src_name = "code_graphic_029_mon_neutrino_v01.mp4"
            video = True
            offset = 0.0
        else:
            raise SystemExit(kind)
        if kind == "still" and not animated:
            framing = {"box": list(p["box"])}
        else:
            framing = {"offset": 0.0 if offset is None else offset}
        cuts.append({"row": p["row"], "timeline_in": p["in"], "timeline_out": p["out"], "source": src_name,
                     "upscale": up, "framing": framing, "video": video})
        if src_name not in seen:
            seen.add(src_name)
            pool.append({"file_id": src_name, "title": POOL.get(p.get("file") or src_name, "our own code graphic")})
        concat.append(f"file '{piece.name}'")
        print(f"    plate {p['row']} up={up}", flush=True)

    (work / "list.txt").write_text("\n".join(concat) + "\n")
    pic = work / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-c", "copy", str(pic)])
    hits = [("whoosh", 0.0, -6.0), ("tick", TITLE_IN, -8.0), ("tick", teach_s, -8.0)]
    aud = build_audio(work, slices, total, hits)

    final = s_dir / f"{spec['stem']}.mp4"
    inputs = ["-t", f"{total:.3f}", "-i", str(pic)]
    for name in ("hook.png", "title.png", "end_card.png", "teach.png"):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / name)]
    inputs += ["-i", str(work / "mix.wav")]
    base = 6
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / f"cap_{i:02d}.png")]
    fc = [
        f"[0:v]fps={FPS},setsar=1,format=yuv420p[v0]",
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='gte(t,0)*lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.30:alpha=1,fade=t=out:st={TITLE_OUT - 0.30:.2f}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{TITLE_OUT})'[v2]",
        f"[3:v]format=rgba,fade=t=in:st={end_in:.2f}:d=0.28:alpha=1[ec]",
        f"[v2][ec]overlay=0:0:enable='gte(t,{end_in})'[v3]",
        f"[4:v]format=rgba,fade=t=in:st={teach_s}:d=0.25:alpha=1,fade=t=out:st={teach_e - 0.25:.2f}:d=0.25:alpha=1[th]",
        f"[v3][th]overlay=0:0:enable='gte(t,{teach_s})*lt(t,{teach_e})'[v4]",
    ]
    last_v = "v4"
    for i, c in enumerate(caps):
        fc.append(f"[{last_v}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last_v = f"c{i}"
    fc.append(f"[{last_v}]noise=alls=3:allf=t,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "5:a", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}", str(final)])
    phone = s_dir / f"{spec['stem']}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", "scale=720:1280:flags=lanczos",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone)])
    if phone.stat().st_size > 120 * 1024 * 1024:
        raise SystemExit(f"phone copy is {phone.stat().st_size} bytes")

    cuts_path = s_dir / f"{spec['stem']}_cuts.json"
    pool_path = s_dir / f"{spec['stem']}_pool.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    # Sidecar before the gate so the stayed-to-watch transcript check sees the spoken line.
    meta_path = s_dir / f"{spec['stem']}_meta.json"
    meta_path.write_text(json.dumps({
        "spoken": joined, "last_word_end_s": last, "words_file": str(s_dir / f"{spec['stem']}_words.json"),
    }) + "\n")

    def gate(cmd: list) -> sp.CompletedProcess:
        return sp.run(cmd, capture_output=True, text=True)

    g_json = gate([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                   "check", str(final), "--air-date", spec["air"], "--sheet-dir", str(s_dir), "--json"])
    g_txt = gate([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                  "check", str(final), "--air-date", spec["air"], "--sheet-dir", str(s_dir)])
    (s_dir / f"{spec['stem']}_gate.json").write_text(g_json.stdout or g_json.stderr)
    (s_dir / f"{spec['stem']}_gate.txt").write_text(g_txt.stdout or g_txt.stderr)
    sfx = gate([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(work / "stem_vo.wav"),
                "--sfx", str(work / "stem_sfx.wav"), "--bed", str(work / "stem_bed.wav"),
                "--minutes", f"{total / 60:.3f}"])
    (s_dir / f"{spec['stem']}_sfx.txt").write_text((sfx.stdout or "") + (sfx.stderr or ""))
    pg = gate([sys.executable, str(REPO / "scripts/polish_gate.py"), str(final), "--cuts", str(cuts_path),
               "--reviewed-ok", str(REV_OK), "--out", str(s_dir / f"{spec['stem']}_polish_gate.json")])
    (s_dir / f"{spec['stem']}_polish_gate.txt").write_text((pg.stdout or "") + (pg.stderr or ""))
    pqa_dir = s_dir / f"{spec['stem']}_picture_qa"
    pqa = gate([sys.executable, str(REPO / "scripts/picture_qa.py"), str(final), "--cuts", str(cuts_path),
                "--pool", str(pool_path), "--reviewed-ok", str(REV_OK), "--out-dir", str(pqa_dir)])
    (s_dir / f"{spec['stem']}_picture_qa.txt").write_text((pqa.stdout or "") + (pqa.stderr or ""))
    cov = gate([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "short",
                str(cover_path), "--out", str(s_dir / f"{spec['stem']}_cover_preview.jpg"), "--score"])

    safe = True
    for bb in hook["bboxes"]:
        if not (40 <= bb[0] and bb[2] <= W - 40 and 80 <= bb[1] and bb[3] <= BAND_Y0 - 8):
            safe = False
    for row in title["rows"] + end["rows"]:
        bb = row["bbox"]
        if not (40 <= bb[0] and bb[2] <= W - 40 and BAND_Y0 <= bb[1] and bb[3] <= BAND_Y1):
            safe = False
    if not (BAND_Y0 <= teach_bb[1] and teach_bb[3] <= BAND_Y1):
        safe = False
    if not (teach_s >= TITLE_OUT - 0.05 and teach_e <= end_in - 0.05 and teach_e - teach_s <= 4.0):
        safe = False
    text_masks = [work / "hook.png", work / "end_card.png", work / "teach.png"]
    text_masks += [work / f"cap_{i:02d}.png" for i in range(len(caps))]
    ld = loop_diff(final, total, text_masks)

    try:
        gdata = json.loads(g_json.stdout)[0]
        g_verdict = gdata.get("verdict", "FAIL")
    except (json.JSONDecodeError, IndexError, KeyError):
        gdata = {}
        g_verdict = "FAIL"
    gates = {
        "gate_shorts_open": g_verdict,
        "gate_shorts_open_warns": gdata.get("warns", []),
        "gate_shorts_open_fails": gdata.get("fails", []),
        "motion_0_1s": gdata.get("motion_0_1s"),
        "visor_frac": (gdata.get("orbit") or {}).get("visor_frac"),
        "first_cut_s": gdata.get("first_cut_s"),
        "sfx_kit_level": "PASS" if sfx.returncode == 0 else "FAIL",
        "polish_gate": "PASS" if pg.returncode == 0 else "FAIL",
        "picture_qa": "PASS" if pqa.returncode == 0 else "FAIL",
        "cover_score": "PASS" if cov.returncode == 0 else "FAIL",
        "caption_title_safe": "PASS" if safe else "FAIL",
        "loop_diff": ld,
        "loop_diff_ok": "PASS" if ld <= 15 else "FAIL",
    }
    payoff_t = next((w["s"] for w in words if spec["payoff_word"] in w["w"].lower()), round(0.75 * total, 2))
    frames = [
        (0.12, "0s Open"), (4.50, "4.5s Seam"), (10.0, "10s Banner"),
        (round(min(payoff_t, total - 2.2), 2), "Payoff"), (round(total - 1.0, 2), "End Card"),
    ]
    sheet = s_dir / f"{spec['stem']}_frames_5pt.jpg"
    tiles = []
    for i, (t, label) in enumerate(frames):
        fp = work / f"f{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1", "-vf", "scale=270:480", str(fp)])
        tiles.append((Image.open(fp).convert("RGB"), t, label))
    canvas = Image.new("RGB", (270 * len(tiles), 544), (16, 22, 34))
    d = ImageDraw.Draw(canvas)
    d.text((8, 6), f"{spec['day']} · {spec['title']}", font=ImageFont.truetype(FONT_BOLD, 18), fill=(255, 224, 0))
    for i, (im, t, label) in enumerate(tiles):
        canvas.paste(im, (i * 270, 32))
        d.text((i * 270 + 6, 516), f"{label} {t:.1f}s", font=ImageFont.truetype(FONT_BOLD, 16), fill=(255, 255, 255))
    canvas.save(sheet, quality=90)

    meta = {
        "job": "J0929", "slug": spec["slug"], "stem": spec["stem"], "day": spec["day"], "air_date": spec["air"],
        "title": spec["title"], "long": {"id": LONG_ID, "title": LONG_TITLE},
        "spoken": joined, "last_word_end_s": last, "duration_s": round(dur(final), 2),
        "sha256": sha256(final), "phone_sha256": sha256(phone),
        "phone_bytes": phone.stat().st_size, "words_count": len(words),
        "teach": {"text": spec["teach_text"], "s": teach_s, "e": teach_e, "bbox": teach_bb},
        "hook": hook, "title_banner": title, "end_card": end, "cover": cover,
        "lufs": aud.get("mix_lufs"),
        "loop_diff": ld,
        "meta_promise_lint": spec.get("meta_promise_lint", "none"),
        "audio": aud, "gates": gates, "cuts": [{"row": c["row"], "in": c["timeline_in"], "out": c["timeline_out"]} for c in cuts],
        "spend": "£0",
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"  GATES {spec['slug']}: {json.dumps(gates)}", flush=True)
    if g_verdict != "PASS" or any(gates[k] != "PASS" for k in ("sfx_kit_level", "polish_gate", "picture_qa", "cover_score", "caption_title_safe", "loop_diff_ok")):
        (s_dir / f"{spec['stem']}_FAIL.txt").write_text(
            (g_txt.stdout or "") + "\n" + (pg.stdout or "") + (pg.stderr or "") + "\n" + (pqa.stdout or "") + (pqa.stderr or "")
            + "\n" + (sfx.stdout or "") + (sfx.stderr or "") + "\n" + (cov.stdout or "") + (cov.stderr or "")
        )
    else:
        fail_note = s_dir / f"{spec['stem']}_FAIL.txt"
        if fail_note.exists():
            fail_note.unlink()
        ship(spec, final, phone, cover_path, sheet, meta_path, s_dir)
    return meta


def ship(spec, final, phone, cover, sheet, meta, s_dir) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    for p in s_dir.glob(f"{spec['stem']}*"):
        if p.suffix == ".mp4":
            continue
        if p.is_file():
            shutil.copy2(p, PACK / p.name)
    for root in UAT_CANDIDATES:
        if not root.exists():
            continue
        sub = root / spec["stem"]
        sub.mkdir(parents=True, exist_ok=True)
        for p in (final, phone, cover, sheet, meta):
            shutil.copy2(p, root / p.name)
            shutil.copy2(p, sub / p.name)
    if NAS_STAGE.parent.exists():
        NAS_STAGE.mkdir(parents=True, exist_ok=True)
        for p in (final, phone, cover, sheet, meta):
            shutil.copy2(p, NAS_STAGE / p.name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--check", action="store_true")
    ns = ap.parse_args()
    if not ns.check:
        session = sp.run(["tmux", "has-session", "-t", "J0929-v02"], capture_output=True)
        done = Path.home() / "_desk/logs/J0929-v02.done"
        if session.returncode == 0 and not os.environ.get("J0929_RENDER"):
            print("J0929 v02 render already running in tmux J0929-v02")
            return 0
        if done.exists() and done.read_text().strip() == "0" and not os.environ.get("J0929_RENDER"):
            print(f"J0929 render already finished cleanly ({done})")
            return 0
    specs = [s for s in SHORTS if not ns.only or s["slug"] == ns.only]
    results = []
    failed = []
    for spec in specs:
        try:
            results.append(build_one(spec, ns.check))
        except SystemExit as e:
            print(f"FAIL {spec['slug']}: {e}", flush=True)
            failed.append(spec["slug"])
            break
        if results and not ns.check:
            g = results[-1].get("gates") or {}
            bad = [k for k in ("gate_shorts_open", "sfx_kit_level", "polish_gate", "picture_qa", "cover_score", "caption_title_safe", "loop_diff_ok") if g.get(k) not in (None, "PASS")]
            if bad:
                failed.append(spec["slug"])
                print(f"stop: {spec['slug']} failed {bad}", flush=True)
                break
    if not ns.check and not ns.only and not failed:
        PACK.mkdir(parents=True, exist_ok=True)
        (PACK / "summary_v02.json").write_text(json.dumps(results, indent=2) + "\n")
        lines = []
        for r in results:
            lines.append(f"{r['sha256']}  {r['stem']}.mp4")
            lines.append(f"{r['phone_sha256']}  {r['stem']}_PHONE.mp4")
        (PACK / "SHA256.txt").write_text("\n".join(lines) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
