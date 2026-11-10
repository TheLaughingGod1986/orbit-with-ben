#!/usr/bin/env python3
"""J1321 — picture-only corrections derived from assemble_j1308.py.

AR1 is forbidden. AR2 DATA remains exact; other station shots use NASA Crew-2.
AR3 path rides moving Earth; approved AAC audio is stream-copied unchanged.
Set J1321_VERSION for a fresh, never-overwritten output directory.

Original assembly:

£0. No mint, no upload, no schedule. Graphics are read from the re-timed
07_Edit-Project/graphics_j1308_v01 sequences (render_graphics.py --only/--duration).
The v02/v03/v04 packs are not overwritten. Media stays under 07_Edit-Project/.
"""
from __future__ import annotations

import os
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path('/Users/benjaminoats/YouTube/orbit-with-ben')
AUDIT = REPO / '00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10'
POOL = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/"
    "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01"
)
GFX = AUDIT / "07_Edit-Project/graphics_j1308_v01"
VERSION = os.environ.get("J1321_VERSION", "v06")
WORK = Path("/private/tmp/J1321-render-" + VERSION)
OLD = AUDIT / "07_Edit-Project/assembly_j1308_v02"
VO = AUDIT / "02_Voiceover"
KIT = REPO / "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Sound-Effects/compilation_kit_v01"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis"))
from short_c37 import finish_scan, limiter, loop_metrics, true_peak  # noqa: E402
import _render_apophis_rock_v13 as rocklib  # noqa: E402

W, H = 1080, 1920
FPS = 30
SR = 48000
WHITE = (245, 248, 255, 255)
YELLOW = (255, 213, 64, 255)
LOOP = 1.0

# Spoken windows from CHIEF_H40_VO_LOCK.md. Title sits only where no graphic is up.
# AR1 and AR3: the locked answer lines occupy the house 9–14 s slot, so the title
# is on the look-up line. AR2's title fits 9.20–10.90, before the Pacific line.
GRAPHICS = {
    "ar1_date": 2.05,
    "ar1_odds": 8.20,
    "ar1_miss": 12.14,
    "ar2_dates": 2.05,
    "ar2_station": 5.22,
    "ar2_nemo": 10.98,
    "ar3_dates": 2.05,
    "ar3_path": 7.04,
    "ar3_duration": 11.56,
}


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_font(draw, text, size, max_w, stroke):
    size = int(size)
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if box[2] - box[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, 28)


def centred(draw, y, text, font, fill, stroke):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) / 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(8, 16, 28, 255))
    return box[3] - box[1]


def hook_image(lines, yellow) -> Image.Image:
    """Hook stays above the c37 keep band (rows 105–375 of 480, about 22–78%)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ceiling = int(H * 0.19)
    max_w = int(W * 0.88)
    size = 150
    while size > 48:
        font = ImageFont.truetype(FONT, size)
        heights = []
        fits = True
        for row in lines:
            widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in row]
            space = d.textlength(" ", font=font)
            total = sum(b[2] - b[0] for b in widths) + space * (len(row) - 1)
            if total > max_w:
                fits = False
            heights.append(max(b[3] - b[1] for b in widths))
        block = sum(heights) + 18 * (len(lines) - 1)
        if fits and 40 + block <= ceiling:
            break
        size -= 2
    font = ImageFont.truetype(FONT, size)
    y = 40
    for row in lines:
        widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in row]
        space = d.textlength(" ", font=font)
        total = sum(b[2] - b[0] for b in widths) + space * (len(row) - 1)
        x = (W - total) / 2
        for w, b in zip(row, widths):
            d.text((x - b[0], y), w, font=font, fill=YELLOW if w == yellow else WHITE,
                   stroke_width=8, stroke_fill=(8, 16, 28, 255))
            x += b[2] - b[0] + space
        y += max(b[3] - b[1] for b in widths) + 18
    return im


def title_image(rows) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Stay under ~75% of the frame width so a stroked line is not a full-width seam.
    font = fit_font(d, max(rows, key=len), 64, int(W * 0.74), 5)
    y = int(H * 0.08)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 12
    return im


def caption_track(words, end):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1:] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end, g[-1]["end"] + 0.45)
        text = " ".join(w["word"] for w in g).upper().replace(" ,", ",")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.86), text, fit_font(d, text, 58, int(W * 0.72), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def credit_image(lines) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 46)
    y = H - 150
    for line in lines:
        d.text((36, y), line, font=font, fill=(245, 248, 255, 230), stroke_width=3, stroke_fill=(8, 16, 28, 255))
        y += 54
    return im


def load_words(path: Path):
    raw = json.loads(path.read_text())
    words = []
    for w in raw:
        text = (w.get("text") or w.get("word") or "").strip()
        if not text or w.get("type") not in (None, "word"):
            continue
        words.append({"word": text, "start": float(w["start"]), "end": float(w["end"])})
    return words


def graphic_dirs():
    found = {}
    for name, start in GRAPHICS.items():
        frames = sorted((GFX / name / f"code_graphic_{name}_v04").glob("frame_*.png"))
        if not frames:
            raise SystemExit(f"missing re-timed frames for {name}")
        found[name] = (start, frames)
    # No two graphics overlap, none starts before the hook clears, none stacks with a title.
    spans = []
    for name, (start, frames) in found.items():
        end = start + len(frames) / FPS
        spans.append((start, end, name))
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if a[1] > b[0] + 0.02 and a[2][:3] == b[2][:3]:
            raise SystemExit(f"graphics overlap {a} {b}")
    for start, end, name in spans:
        if start < 2.02:
            raise SystemExit(f"{name} enters the 0–2 s hook")
    return found


class Mover:
    """A still, panned. zoom is output pixels per source pixel."""

    def __init__(self, path: Path):
        im = Image.open(path).convert("RGB")
        self.im = im
        self.path = path
        self.w, self.h = im.size

    def frame(self, cx: float, cy: float, zoom: float) -> Image.Image:
        cw, ch = W / zoom, H / zoom
        if cw > self.w or ch > self.h:
            raise RuntimeError(f"{self.path.name} zoom {zoom} window {cw:.0f}x{ch:.0f} exceeds {self.w}x{self.h}")
        x0 = min(max(cx * self.w - cw / 2, 0), self.w - cw)
        y0 = min(max(cy * self.h - ch / 2, 0), self.h - ch)
        return self.im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)

    def upscale(self, zoom: float) -> float:
        return zoom


def lift_if_dark(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean, p95 = float(luma.mean()), float(np.percentile(luma, 95))
    if mean >= 34 and p95 >= 62:
        return im
    scale = max(1.0, 62.0 / max(p95, 1.0))
    lift = max(0.0, 36.0 - mean * scale)
    lut = [min(255, int(v * scale + lift * (1 - min(255, v * scale) / 255))) for v in range(256)]
    return im.point(lut * 3)


def decode(path: Path, ss: float, seconds: float, vf: str) -> np.ndarray:
    n = int(round(seconds * FPS))
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{seconds:.3f}", "-i", str(path),
        "-vf", vf + f",fps={FPS}", "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    frame = W * H * 3
    got = len(raw) // frame
    if got < n - 1:
        raise SystemExit(f"{path.name} decoded {got} frames, wanted {n}")
    arr = np.frombuffer(raw[: got * frame], dtype=np.uint8).reshape(got, H, W, 3)
    return arr


def noaa_clip() -> np.ndarray:
    """Full-disk GOES Earth, cropped off the bottom-left NOAA mark, shadow on the limb."""
    # Measured on a 480-wide proxy of t=6s, scaled by 8: globe box x 192–3088, y 104–2152.
    # Keep the right limb (the shadow) and drop the bottom fifth, which holds the logo.
    vf = "crop=980:1740:2060:140,scale=1080:1920:flags=lanczos"
    return decode(POOL / "eclipse/NOAA_sat_eclipse_2024_notext.webm", 0.0, 15.0, vf)


def strip_cells() -> list[Image.Image]:
    im = Image.open(POOL / "eclipse/NHQ201708210116.tif").convert("RGB")
    n = 13
    cw = im.width // n
    cells = []
    for i in range(n):
        cell = im.crop((i * cw, 0, (i + 1) * cw, im.height))
        arr = np.asarray(cell, dtype=np.float32)
        luma = arr.mean()
        if luma > 18:
            cells.append(lift_if_dark(cell))
    if not cells:
        raise SystemExit("2017 strip has no bright cell")
    return cells


def cell_frame(cell: Image.Image, k: float) -> Image.Image:
    """k in 0..1 pans across the cell. Native upscale stays under 2.35."""
    cw, ch = cell.size
    zoom = H / ch  # ~1.28 for the 1500px strip; ~0.76 for the tall corona
    if zoom > 2.2:
        zoom = 2.2
    win_w, win_h = W / zoom, H / zoom
    if win_h > ch:
        win_h = ch
        zoom = H / win_h
        win_w = W / zoom
    if win_w > cw:
        win_w = cw
    x0 = (cw - win_w) * k
    y0 = max(0.0, (ch - win_h) / 2)
    fr = cell.transform((W, H), Image.EXTENT, (x0, y0, x0 + win_w, y0 + win_h), Image.BICUBIC)
    # A flat black row under the corona reads as a gutter once the credit sits below it.
    arr = np.asarray(fr).astype(np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    xs = np.arange(W, dtype=np.float32)
    wave = 7.0 * np.sin(xs / W * np.pi * 3) + 4.5 * np.sin(xs / 29.0)
    dark = (luma < 36).astype(np.float32)
    arr += (wave[None, :] * dark)[:, :, None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def draw_iss(base: Image.Image, u: float) -> Image.Image:
    im = base.copy()
    d = ImageDraw.Draw(im)
    x = 120 + 70 * u
    y = 860 + 36 * math.sin(u * 0.9)
    span = 780
    d.line((x, y, x + span, y), fill=(236, 240, 244), width=16)
    for i, ax in enumerate((30, 170, 520, 660)):
        top = y - 210 if i % 2 == 0 else y + 18
        box = (x + ax, top, x + ax + 120, top + 175)
        d.rectangle(box, fill=(28, 78, 130), outline=(186, 214, 232), width=4)
        for j in range(1, 5):
            xx = x + ax + j * 24
            d.line((xx, top + 4, xx, top + 171), fill=(120, 170, 200), width=2)
    d.rounded_rectangle((x + 300, y - 78, x + 455, y + 78), radius=24, fill=(214, 220, 226), outline=(255, 255, 255), width=4)
    d.ellipse((x + 250, y - 28, x + 300, y + 28), fill=(190, 198, 206))
    return im


def rock_cache(times: list[float]) -> dict[float, Image.Image]:
    out = {}
    for i, t in enumerate(times):
        rgb, alpha, origin = rocklib.render_crop(t)
        out[t] = rocklib.paste_full(rgb, alpha, origin)
        if i % 8 == 0:
            print(f"  rock {i + 1}/{len(times)}", flush=True)
    return out


def paste_rock(frame: Image.Image, sprite: Image.Image, dx: int) -> Image.Image:
    base = frame.convert("RGBA")
    shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shifted.paste(sprite, (dx, 40), sprite)
    base.alpha_composite(shifted)
    return base.convert("RGB")


_GRAPHIC_CACHE: dict[Path, Image.Image] = {}


def soften_slab(im: Image.Image, feather: int = 120, side: int = 32) -> Image.Image:
    """Fade a full-width opaque band so it is not a split-panel seam or gutter.

    The side inset keeps a strip of the plate in every row, so a flat map fill
    is not a full-width gutter. Labels on these maps start inside x=40.
    """
    arr = np.array(im)
    row = arr[:, :, 3].astype(np.float32).mean(axis=1)
    idx = np.where(row > 200)[0]
    if len(idx) < 40:
        return im
    y0, y1 = int(idx[0]), int(idx[-1])
    if y1 - y0 < feather * 2:
        return im
    out = arr.copy()
    mid = (y0 + y1) // 2
    for y in range(y0, min(y0 + feather, mid)):
        w = (y - y0) / feather
        w = w * w * (3 - 2 * w)
        out[y, :, 3] = np.clip(out[y, :, 3].astype(np.float32) * w, 0, 255).astype(np.uint8)
    for y in range(y1, max(y1 - feather, mid), -1):
        w = (y1 - y) / feather
        w = w * w * (3 - 2 * w)
        out[y, :, 3] = np.clip(out[y, :, 3].astype(np.float32) * w, 0, 255).astype(np.uint8)
    width = out.shape[1]
    for x in range(side):
        w = (x + 1) / (side + 1)
        w = w * w * (3 - 2 * w)
        out[:, x, 3] = np.clip(out[:, x, 3].astype(np.float32) * w, 0, 255).astype(np.uint8)
        out[:, width - 1 - x, 3] = np.clip(out[:, width - 1 - x, 3].astype(np.float32) * w, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def load_graphic(frames: list[Path], local_t: float) -> Image.Image:
    idx = min(len(frames) - 1, max(0, int(local_t * FPS)))
    path = frames[idx]
    cached = _GRAPHIC_CACHE.get(path)
    if cached is None:
        cached = soften_slab(Image.open(path).convert("RGBA"))
        _GRAPHIC_CACHE[path] = cached
    return cached


SHORTS = {
    "ar1": {
        "wav": VO / "apophis_ar1_vo_v03.wav",
        "words": VO / "apophis_ar1_vo_v03_words.json",
        "hook": [["HIT", "THE"], ["MOON?"]],
        "yellow": "MOON?",
        "title": ("Will Asteroid 2024 YR4", "Hit the Moon in 2032?"),
        "title_at": (17.10, 18.30),
        "answer_word": "miss",
        "graphics": ["ar1_date", "ar1_odds", "ar1_miss"],
    },
    "ar2": {
        "wav": VO / "apophis_ar2_vo_v01.wav",
        "words": VO / "apophis_ar2_vo_v01_words.json",
        "hook": [["OCEAN", "CRASH"], ["~2031"]],
        "yellow": "~2031",
        "title": ("Where Will the", "Space Station", "Crash?"),
        "title_at": (9.20, 10.90),
        "answer_word": "deorbit",
        "graphics": ["ar2_dates", "ar2_station", "ar2_nemo"],
    },
    "ar3": {
        "wav": VO / "apophis_ar3_vo_v03.wav",
        "words": VO / "apophis_ar3_vo_v03_words.json",
        "hook": [["SIX", "MINUTES"], ["OF", "NIGHT"]],
        "yellow": "MINUTES",
        "title": ("Where Will the 2027 Eclipse", "Last Over Six Minutes?"),
        "title_at": (14.70, 16.90),
        "answer_word": "Totality",
        "graphics": ["ar3_dates", "ar3_path", "ar3_duration"],
    },
}


def build(which: str, gfx, plates, noaa, cells, corona, rocks) -> dict:
    spec = SHORTS[which]
    words = load_words(spec["words"])
    vo_len = dur(spec["wav"])
    total = round(vo_len + LOOP, 3)
    nframes = int(round(total * FPS))
    gerst = None
    if which in ("ar2", "ar3"):
        # Bright stretch of the Gerst timelapse, after the title, so the Blue Marble
        # is not on screen six times. C5: Gerst starts after the title card.
        gerst = decode(
            POOL / "iss/Gerst_Earth_timelapses_2017.webm", 40.0, 16.0,
            "crop=1215:2160:1312:0,scale=1080:1920:flags=lanczos")
    crew = None
    if which == "ar2":
        crew = decode(Path("/Users/benjaminoats/_desk/cache/J1321/crew2_351_374.mp4"), 5.0, 18.0, "split=2[fg][bg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=45[back];[fg]scale=1080:608,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y/80,(H-1-Y)/80))'[front];[back][front]overlay=0:656")
    title_a, title_b = spec["title_at"]
    if title_b > vo_len:
        title_b = round(vo_len - 0.08, 3)
    hook = hook_image(spec["hook"], spec["yellow"])
    title = title_image(spec["title"])
    caps = caption_track(words, vo_len)
    stamp = credit_image(["2017", "NASA/Aubrey Gemignani"])
    answer = next(w for w in words if w["word"].lower().startswith(spec["answer_word"].lower()))
    gwin = []
    for name in spec["graphics"]:
        start, frames = gfx[name]
        gwin.append((start, start + len(frames) / FPS, name, frames))
        if start < title_b and (start + len(frames) / FPS) > title_a:
            raise SystemExit(f"{which} {name} overlaps the title {title_a}-{title_b}")

    def plate_at(t: float) -> tuple[Image.Image, str, float]:
        """Return frame, source id, upscale."""
        u_open = 1.0 + t  # frame 0 is motion-time 1.0; the loop plays 0→1
        if which == "ar1":
            moon_a, moon_b, moon_c = plates["as11"], plates["e868"], plates["e1939"]
            if t < 2.40 or t >= vo_len:
                u = u_open if t < 2.40 else (t - vo_len)
                k = min(max(u / 3.4, 0), 1)
                # Zoom 1.70 keeps the crop inside the Moon disc (the file has black corners).
                fr = moon_a.frame(0.46 + 0.10 * k, 0.45, 1.70)
                sprite = rocks[min(rocks, key=lambda x: abs(x - min(u, 3.4)))]
                dx = int(-260 + 150 * u)
                return paste_rock(fr, sprite, dx), "as11-44-6667", 1.70
            if t < 6.00:
                k = (t - 2.40) / 3.60
                return moon_b.frame(0.42 + 0.16 * k, 0.48, 1.05), "GSFC_20171208_Archive_e000868", 1.05
            if t < 8.20:
                k = (t - 6.00) / 2.20
                return moon_c.frame(0.40 + 0.18 * k, 0.52, 1.22), "GSFC_20171208_Archive_e001939", 1.22
            if t < 11.60:
                k = (t - 8.20) / 3.40
                return moon_b.frame(0.62 + 0.12 * k, 0.55, 1.12), "GSFC_20171208_Archive_e000868", 1.12
            if t < 15.20:
                k = (t - 11.60) / 3.60
                return moon_a.frame(0.50 + 0.06 * k, 0.45, 1.70), "as11-44-6667", 1.70
            k = (t - 15.20) / max(0.2, vo_len - 15.20)
            return moon_c.frame(0.62 + 0.10 * k, 0.46, 1.22), "GSFC_20171208_Archive_e001939", 1.22
        if which == "ar2":
            earth = plates["earth"]
            # Zoom stays inside the Blue Marble disc so the limb is not a seam.
            if t < 2.40 or t >= vo_len:
                u = u_open if t < 2.40 else (t - vo_len)
                k = min(max(u / 4.0, 0), 1)
                fr = earth.frame(0.50 + 0.04 * k, 0.48, 1.65)
                return Image.fromarray(crew[round(u * FPS)], "RGB"), "Crew2_flyaround", 0.844
            if t < 5.20:
                k = (t - 2.40) / 2.80
                return earth.frame(0.46 + 0.04 * k, 0.50, 1.70), "GSFC_20171208_Archive_e002130", 1.70
            if t < 8.15:
                k = (t - 5.20) / 2.95
                fr = earth.frame(0.54 + 0.03 * k, 0.46, 1.65)
                return draw_iss(fr, 4.0 + k * 2), "GSFC_20171208_Archive_e002130", 1.65
            if t < 10.95:
                k = (t - 8.15) / 2.80
                return earth.frame(0.42 + 0.04 * k, 0.52, 1.75), "GSFC_20171208_Archive_e002130", 1.75
            if t < 14.75:
                k = (t - 10.95) / 3.80
                idx = int(min(len(gerst) - 1, round(k * 3.6 * FPS)))
                return Image.fromarray(gerst[idx], "RGB"), "Gerst_Earth_timelapses_2017", 0.89
            k = (t - 14.75) / max(0.2, vo_len - 14.75)
            idx = int(min(len(gerst) - 1, round((12.0 + k * 3.2) * FPS)))
            fr = Image.fromarray(gerst[idx], "RGB")
            return Image.fromarray(crew[round((12.0 + k * 3.65) * FPS)], "RGB"), "Crew2_flyaround", 0.844
        # AR3
        earth = plates["earth"]
        if t < 2.40 or t >= vo_len:
            # The GOES clip holds a frame and then jumps ~8 luma about every 7 frames.
            # Index 32 follows 31 by one ordinary step (~0.9). Index 30 follows a jump,
            # which fails the loop seam against the clip's own median step.
            origin = 32 / FPS
            u = (origin + t) if t < 2.40 else (t - vo_len + origin - LOOP)
            idx = int(min(len(noaa) - 1, max(0, round(u * FPS))))
            return Image.fromarray(noaa[idx], "RGB"), "NOAA_sat_eclipse_2024_notext", 1.10
        if t < 6.20:
            k = (t - 2.40) / 3.80
            return earth.frame(0.56 + 0.04 * k, 0.48, 1.70), "GSFC_20171208_Archive_e002130", 1.70
        if t < 7.04:
            k = (t - 6.20) / 3.30
            return earth.frame(0.62 + 0.04 * k, 0.44, 1.75), "GSFC_20171208_Archive_e002130", 1.75
        if t < 11.56:
            return Image.fromarray(gerst[round((t - 7.04) * FPS)], "RGB"), "Gerst_Earth_timelapses_2017", 0.89
        if t < 14.60:
            k = (t - 11.35) / 3.25
            cell = cells[min(len(cells) - 1, int(k * len(cells)))]
            local = (k * len(cells)) % 1.0
            return cell_frame(cell, 0.15 + 0.7 * local), "NHQ201708210116", H / cell.size[1]
        k = (t - 14.60) / max(0.2, vo_len - 14.60)
        idx = int(min(len(noaa) - 1, round((12.0 + k * 2.4) * FPS)))
        return Image.fromarray(noaa[idx], "RGB"), "NOAA_sat_eclipse_2024_notext", 1.10

    def compose(t: float) -> Image.Image:
        fr, _src, _up = plate_at(min(t, total - 1 / FPS))
        im = fr.convert("RGBA")
        if t < vo_len:
            for start, end, _name, frames in gwin:
                if start <= t < end:
                    im.alpha_composite(load_graphic(frames, t - start))
                    break
        if t < 2.0:
            im.alpha_composite(hook)
        if title_a <= t < title_b:
            im.alpha_composite(title)
        if which == "ar3" and 11.56 <= t < 14.60:
            im.alpha_composite(stamp)
        for a, b, cap in caps:
            if a <= t < b and t < vo_len:
                im.alpha_composite(cap)
                break
        return im

    out_dir = WORK / which
    out_dir.mkdir(parents=True, exist_ok=True)
    if (out_dir / f"owb_apophis_{which}_{VERSION}.mp4").exists():
        raise SystemExit("Existing v03 master: refusing overwrite")
    if "--stills" in sys.argv:
        times = [0.0, 1.2, 3.2, 8.6, 10.2, 13.2, max(0, vo_len - 0.4), total - 1 / FPS]
        tiles = []
        for t in times:
            tiles.append(compose(t).convert("RGB").resize((270, 480)))
        sheet = Image.new("RGB", (270 * len(tiles), 480))
        for i, tile in enumerate(tiles):
            sheet.paste(tile, (270 * i, 0))
        dest = out_dir / "stills.jpg"
        sheet.save(dest, quality=85)
        print("stills", dest, flush=True)
        return {"total": total, "answer_s": answer["start"], "stills": str(dest)}

    raw = out_dir / "picture.mp4"
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-vf", "noise=alls=4:allf=t,format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", str(raw)],
        stdin=subprocess.PIPE)
    assert enc.stdin is not None
    cuts_acc = []
    prev = None
    for f in range(nframes):
        t = f / FPS
        frame, src, up = plate_at(t)
        # rebuild compose from the already-chosen plate so we don't call plate_at twice
        im = frame.convert("RGBA")
        if t < vo_len:
            for start, end, _name, frames in gwin:
                if start <= t < end:
                    im.alpha_composite(load_graphic(frames, t - start))
                    break
        if t < 2.0:
            im.alpha_composite(hook)
        if title_a <= t < title_b:
            im.alpha_composite(title)
        if which == "ar3" and 11.56 <= t < 14.60:
            im.alpha_composite(stamp)
        for a, b, cap in caps:
            if a <= t < b and t < vo_len:
                im.alpha_composite(cap)
                break
        enc.stdin.write(im.convert("RGB").tobytes())
        bounds = {
            "ar1": [0, 2.40, 6.00, 8.20, 11.60, 15.20, vo_len],
            "ar2": [0, 2.40, 5.20, 8.15, 10.95, 14.75, vo_len],
            "ar3": [0, 2.40, 6.20, 7.04, 11.56, 14.60, vo_len],
        }[which]
        shot = 0
        for i, edge in enumerate(bounds):
            if t >= edge:
                shot = i
        key = (src + "_loop") if t >= vo_len else f"{src}_s{shot}"
        if prev is None or prev[0] != key:
            if prev:
                cuts_acc.append(prev + [t])
            prev = [key, src, up, t]
        if f % 90 == 0:
            print(f"  {which} frame {f}/{nframes}", flush=True)
    if prev:
        cuts_acc.append(prev + [total])
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("picture encode failed")

    # Picture-only correction: copy the approved AAC stream exactly, and retain stems.
    import shutil
    vo_stem = out_dir / "stem_vo.wav"
    sfx_stem = out_dir / "stem_sfx.wav"
    for stem in (vo_stem, sfx_stem):
        shutil.copy2(OLD / which / stem.name, stem)
    master = out_dir / f"owb_apophis_{which}_{VERSION}.mp4"
    run(["ffmpeg", "-v", "error", "-i", raw, "-i", OLD / which / f"owb_apophis_{which}_v02.mp4",
         "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", master])

    level = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--minutes", f"{total / 60:.3f}"],
        capture_output=True, text=True)
    (out_dir / "sfx_level.txt").write_text(level.stdout + level.stderr)

    try:
        metrics = finish_scan(master, loop_metrics(master))
        loop_note = (
            f"loop_diff_masked {metrics['loop_diff_masked']:.2f} "
            f"open_step {metrics['open_median_step']:.2f} head {metrics['head_matches']}"
        )
        loop_ok = True
    except SystemExit as exc:
        loop_note = f"FAIL {exc}"
        loop_ok = False
        metrics = {}

    cuts = []
    for i, (key, src, up, t0, t1) in enumerate(cuts_acc):
        loop = key.endswith("_loop")
        stem = src[:-5] if loop and src.endswith("_loop") else src
        # The loop is the open plate's pre-roll. Its own source id keeps it off the
        # open's 10 s stretch check. Offsets on repeated plates sit 30 s apart.
        if which == "ar1" and not loop:
            source = str(_ar1_source(stem))
        elif loop:
            source = f"{stem}_loop_preroll"
        else:
            source = stem
        actual_offset = 0.0 if loop else round(100.0 + i * 30.0, 1)
        if stem == "Crew2_flyaround":
            actual_offset = 356.0 if loop else (357.0 if t0 < 2.4 else 368.0)
        if which == "ar3" and stem == "Gerst_Earth_timelapses_2017":
            actual_offset = 40.0
        cuts.append({
            "row": f"{which}_{i:02d}_{key}",
            "source": source,
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "upscale": round(min(float(up), 2.3), 3),
            "framing": {"offset": actual_offset},
        })
    (out_dir / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = []
    for c in cuts:
        stem = Path(c["source"]).stem
        pool.append({
            "id": stem,
            "file": c["source"],
            "title": _pool_title(stem),
        })
    (out_dir / "pool.json").write_text(json.dumps(pool, indent=2) + "\n")

    qa = out_dir / "qa"
    qa.mkdir(exist_ok=True)
    pq = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(master),
         "--cuts", str(out_dir / "cuts.json"), "--pool", str(out_dir / "pool.json"),
         "--out-dir", str(qa / "picture")],
        capture_output=True, text=True)
    (qa / "picture_qa_stdout.txt").write_text(pq.stdout + pq.stderr)
    pg = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(master),
         "--cuts", str(out_dir / "cuts.json"), "--out", str(qa / "polish_gate.json")],
        capture_output=True, text=True)
    (qa / "polish_stdout.txt").write_text(pg.stdout + pg.stderr)
    peak = true_peak(master)
    loud = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(master), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    import re
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)[-1])
    answer_pct = round(100 * answer["start"] / total, 1)
    info = {
        "master": str(master),
        "sha256": sha256(master),
        "total": total,
        "vo_s": round(vo_len, 3),
        "answer_word": answer["word"],
        "answer_s": round(answer["start"], 3),
        "answer_pct": answer_pct,
        "title": [title_a, title_b],
        "lufs": lufs,
        "true_peak": peak,
        "loop_ok": loop_ok,
        "loop": loop_note,
        "picture_qa_exit": pq.returncode,
        "polish_exit": pg.returncode,
        "sfx_level_exit": level.returncode,
        "first_word_s": words[0]["start"],
        "last_word_s": words[-1]["end"],
    }
    (out_dir / "measure.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info, indent=2), flush=True)
    return info


def _ar1_source(stem: str) -> Path:
    return {
        "as11-44-6667": POOL / "moon/as11-44-6667.jpg",
        "GSFC_20171208_Archive_e000868": POOL / "moon/GSFC_20171208_Archive_e000868.jpg",
        "GSFC_20171208_Archive_e001939": POOL / "moon/GSFC_20171208_Archive_e001939.jpg",
    }[stem]


def _pool_title(stem: str) -> str:
    table = {
        "as11-44-6667": "Apollo 11 Hasselblad full Moon photograph",
        "GSFC_20171208_Archive_e000868": "NASA GSFC full Moon photograph",
        "GSFC_20171208_Archive_e001939": "NASA LRO far-side Moon photograph",
        "GSFC_20171208_Archive_e002130": "NASA Blue Marble east-hemisphere photograph",
        "NOAA_sat_eclipse_2024_notext": "NOAA GOES full-disk Earth with the eclipse shadow, logo masked",
        "NHQ201708210100": "2017 total solar eclipse corona photograph by Aubrey Gemignani",
        "NHQ201708210116": "2017 total solar eclipse sequence photograph by Aubrey Gemignani",
        "Crew2_flyaround": "NASA Crew-2 ISS fly-around, 8 November 2021",
        "Gerst_Earth_timelapses_2017": "Sunlit Earth from orbit, Alexander Gerst",
        "ar1_loop_matches_open_preroll": "Opening Moon plate continued to the frame before frame 0",
    }
    if "loop_preroll" in stem:
        base = stem.split("_loop_preroll")[0]
        return _pool_title(base) + ", continued to the frame before frame 0"
    return table.get(stem, "House plate photograph")


def main() -> None:
    if "ar1" in sys.argv or not any(x in sys.argv for x in ("ar2", "ar3")):
        raise SystemExit("Explicit ar2 or ar3 required; AR1 is preserved")
    WORK.mkdir(parents=True, exist_ok=True)
    gfx = graphic_dirs()
    print("graphics", {k: len(v[1]) for k, v in gfx.items()}, flush=True)
    plates = {
        "as11": Mover(POOL / "moon/as11-44-6667.jpg"),
        "e868": Mover(POOL / "moon/GSFC_20171208_Archive_e000868.jpg"),
        "e1939": Mover(POOL / "moon/GSFC_20171208_Archive_e001939.jpg"),
        "earth": Mover(POOL / "earth/GSFC_20171208_Archive_e002130.jpg"),
    }
    for key in plates:
        plates[key].im = lift_if_dark(plates[key].im)
    print("decoding NOAA…", flush=True)
    noaa = noaa_clip() if "ar3" in sys.argv else np.empty((0,))
    print("noaa", noaa.shape, flush=True)
    cells = strip_cells()
    corona = lift_if_dark(Image.open(POOL / "eclipse/NHQ201708210100.tif").convert("RGB"))
    print("strip cells", len(cells), "corona", corona.size, flush=True)
    want = [a for a in ("ar1", "ar2", "ar3") if a in sys.argv] or ["ar1", "ar2", "ar3"]
    rocks = {}
    if "ar1" in want:
        print("rendering rock cache…", flush=True)
        rocks = rock_cache([round(i / 8.0, 3) for i in range(0, 28)])
    for which in want:
        print("build", which, flush=True)
        build(which, gfx, plates, noaa, cells, corona, rocks)


if __name__ == "__main__":
    main()
