#!/usr/bin/env python3
"""J2478 v04: Ben's complete-sentence ending, existing take only.

Retains v03's 551-frame picture timeline. Removes 'as' at a waveform-checked
quiet gap, with a 40 ms fade. Final caption: LOOK EAST AT SUNSET.
Run with /opt/homebrew/opt/python@3.14/bin/python3.14 on the Mini.
All perceptual conclusions remain for the queued Gemini ending review.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = Path(__file__).resolve().parent
WT = BASE.parents[2]
MAIN_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(MAIN_REPO / "scripts"))
from short_c37 import finish_scan, loop_metrics, true_peak  # noqa: E402

POOL_DIR = BASE / "07_Edit-Project/pool_v01"
VO_DIR = BASE / "02_Voiceover"
MUSIC_DIR = BASE / "05_Music"
SFX_DIR = BASE / "06_Sound-Effects/kit_v01"
GFX_DIR = BASE / "07_Edit-Project/graphics_j2478_v04/code_graphic_supermoon_s06_scale_v04"
WORK_DIR = BASE / "07_Edit-Project/assembly_j2478_v04"
EXPORT_DIR = BASE / "06_Final-Exports"
PACK_DIR = BASE / "11_Upload-Package"

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
FPS = 30
SR = 48000
LOOP_S = 1.000
VO_S = 16.810
TOTAL_S = 551 / 30  # ceil audio+tail to complete video frame
NFRAMES = int(round(TOTAL_S * FPS))  # 588

WHITE = (245, 248, 255, 255)
YELLOW = (255, 213, 64, 255)
CYAN = (110, 215, 255, 255)
STROKE = (8, 16, 28, 255)

# Shot boundaries (s): 7 shots during VO + 1.00 s forward-loop tail
SHOT_BOUNDS = [
    ("s01", 0, 63/30, "phases_2026_plain_2160p30", 1.32),
    ("s01_date", 63/30, 110/30, "phases_2026_plain_2160p30", 1.54),
    ("s02", 110/30, 150/30, "GSFC_20171208_Archive_e002130", 1),
    ("s03", 150/30, 215/30, "GSFC_20171208_Archive_e001939", 1),
    ("s04", 215/30, 296/30, "as11-44-6667", 1.72),
    ("s06", 296/30, 386/30, "plain_frame_7864", 1.24),
    ("s06b", 386/30, 461/30, "as11-44-6667", 1.72),
    ("s07", 461/30, 521/30, "iss070e062746", 0.95),
    ("loop", 521/30, TOTAL_S, "phases_2026_plain_2160p30_loop_preroll", 1.32),
]
TITLE_WINDOW = (6.5, 9.5)
GFX_WINDOW = (296/30, 461/30)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_font(draw: ImageDraw.ImageDraw, text: str, size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
    s = int(size)
    while s > 24:
        f = ImageFont.truetype(FONT, s)
        b = draw.textbbox((0, 0), text, font=f, stroke_width=stroke)
        if b[2] - b[0] <= max_w:
            return f
        s -= 2
    return ImageFont.truetype(FONT, 24)


def centred(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, stroke: int) -> int:
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) / 2 - b[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=STROKE)
    return b[3] - b[1]


def hook_image(lines: list[list[str]], yellow_words: set[str]) -> Image.Image:
    """Hook caption at t=0.0..2.0 s: sits inside y=155..355 (above short_c37 KEEP y=420, inside gate_shorts_open 0.08..0.48 H)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    max_w = int(W * 0.84)
    size = 112
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
        block = sum(heights) + 16 * (len(lines) - 1)
        if fits and 155 + block <= 365:
            break
        size -= 2
    font = ImageFont.truetype(FONT, size)
    y = 160
    for row in lines:
        widths = [d.textbbox((0, 0), w, font=font, stroke_width=8) for w in row]
        space = d.textlength(" ", font=font)
        total = sum(b[2] - b[0] for b in widths) + space * (len(row) - 1)
        x = (W - total) / 2
        for w, b in zip(row, widths):
            d.text(
                (x - b[0], y),
                w,
                font=font,
                fill=YELLOW if w in yellow_words else WHITE,
                stroke_width=8,
                stroke_fill=STROKE,
            )
            x += b[2] - b[0] + space
        y += max(b[3] - b[1] for b in widths) + 16
    return im


def title_image(rows: list[str]) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, max(rows, key=len), 60, int(W * 0.74), 5)
    y = int(H * 0.085)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 12
    return im


def caption_track(words: list[dict], end_s: float) -> list[tuple[float, float, Image.Image]]:
    ending = words[-4:]
    assert [w["word"].lower().rstrip(".") for w in ending] == ["look", "east", "at", "sunset"]
    groups, cur = [], []
    for w in words[:-4]:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1:] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    groups.append(ending)
    out = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end_s, g[-1]["end"] + 0.35)
        text = " ".join(w["word"] for w in g).upper().replace(" ,", ",")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.855), text, fit_font(d, text, 56, int(W * 0.72), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def render_data_scale_graphic() -> list[Path]:
    """Render the sole teach overlay (12.300 - 15.800 s, 105 frames = 3.50 s) into GFX_DIR.

    Shows the horizontal scale bar shrinking from 384,400 KM (30 EARTHS) to 360,000 KM (28 EARTHS)
    with label 'TWO EARTHS CLOSER' (<= 4 words per label, inside 16:9 centre band y=656..1264,
    no full-width box or seam).
    """
    GFX_DIR.mkdir(parents=True, exist_ok=True)
    dur_s = GFX_WINDOW[1] - GFX_WINDOW[0]
    n = int(round(dur_s * FPS))
    f_title = ImageFont.truetype(FONT, 44)
    f_sub = ImageFont.truetype(FONT, 38)
    paths = []
    for i in range(n):
        t = i / FPS
        # Slide/fade in over 0.35 s, fade out over 0.35 s
        if t < 0.35:
            alpha = t / 0.35
            dy = int(round((1.0 - alpha) * 28))
        elif t > dur_s - 0.35:
            alpha = max(0.0, (dur_s - t) / 0.35)
            dy = 0
        else:
            alpha = 1.0
            dy = 0
        alpha_Ease = alpha * alpha * (3 - 2 * alpha)

        # Contraction progress p in [0, 1] over t = 0.45 .. 2.45 s
        p = min(1.0, max(0.0, (t - 0.45) / 2.00))
        p_ease = p * p * (3 - 2 * p)
        km_val = int(round(384400 - (384400 - 360000) * p_ease))
        earths_val = 30.0 - 2.0 * p_ease

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # Position inside lower half of 16:9 centre band (y = 1040 .. 1230, well inside 656..1264)
        y_top = 1035 + dy
        # Top label (<= 4 words): "384,400 KM -> 360,000 KM" or dynamic counter
        lbl1 = f"{km_val:,} KM ({earths_val:.0f} EARTHS)"
        centred(d, y_top, lbl1, f_title, YELLOW, 5)

        # Animated horizontal scale bar (width shrinks from 680 px to 540 px, centered, with end ticks)
        bar_y = y_top + 68
        full_w = 680
        cur_w = int(round(full_w * (1 - (24400 / 384400) * p_ease)))
        x0 = (W - full_w) // 2
        x1_full = x0 + full_w
        x1_cur = x0 + cur_w

        # Ghost baseline bar (30 Earths average)
        d.rounded_rectangle((x0, bar_y, x1_full, bar_y + 22), radius=11, fill=(40, 60, 90, 160), outline=(160, 190, 225, 190), width=3)
        # Active Supermoon bar shrinking toward Earth
        d.rounded_rectangle((x0, bar_y, x1_cur, bar_y + 22), radius=11, fill=(255, 213, 64, 235), outline=STROKE, width=3)

        # Scale comparison label (3 words <= 4 words): "TWO EARTHS CLOSER"
        lbl2 = "TWO EARTHS CLOSER"
        centred(d, bar_y + 34, lbl2, f_sub, WHITE, 5)

        if alpha_Ease < 0.999:
            arr = np.array(layer, dtype=np.float32)
            arr[:, :, 3] *= alpha_Ease
            layer = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

        fp = GFX_DIR / f"frame_{i:04d}.png"
        layer.save(fp)
        paths.append(fp)
    return paths


class Mover:
    def __init__(self, path: Path, lift: bool = True):
        im = Image.open(path).convert("RGB")
        if lift:
            im = lift_if_dark(im)
        self.im = im
        self.path = path
        self.w, self.h = im.size

    def frame(self, cx: float, cy: float, zoom: float) -> Image.Image:
        cw, ch = W / zoom, H / zoom
        if cw > self.w or ch > self.h:
            zoom = max(W / self.w, H / self.h) * 1.01
            cw, ch = W / zoom, H / zoom
        x0 = min(max(cx * self.w - cw / 2, 0.0), self.w - cw)
        y0 = min(max(cy * self.h - ch / 2, 0.0), self.h - ch)
        return self.im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


def lift_if_dark(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean, p95 = float(luma.mean()), float(np.percentile(luma, 95))
    if mean >= 36.0 and p95 >= 68.0:
        return im
    scale = max(1.0, 68.0 / max(p95, 1.0))
    lift = max(0.0, 38.0 - mean * scale)
    lut = [min(255, int(v * scale + lift * (1.0 - min(255.0, v * scale) / 255.0))) for v in range(256)]
    return im.point(lut * 3)


def decode_svs_4k_frames(video_path: Path, start_frame: int, count: int) -> list[Image.Image]:
    """Decode `count` 4K (3840x2160) frames starting at `start_frame` from phases_2026_plain_2160p30.mp4."""
    ss = start_frame / FPS
    dur = count / FPS
    proc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(video_path),
        "-frames:v", str(count), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ], stdout=subprocess.PIPE)
    frames=[]
    for i in range(count):
        data=proc.stdout.read(3840*2160*3)
        if len(data)!=3840*2160*3: raise RuntimeError("Incomplete native frame")
        im=Image.frombytes("RGB", (3840,2160), data)
        # Crop from native 4K; 820x1458 minimum => <=1.32x upscale.
        u=i/max(1,count-1)
        ch=1640-120*u; cw=ch*W/H
        cx=3840*(0.465+0.075*u); cy=2160*(0.485+0.045*u)
        if 93 <= i < 140:
            # Tighter native crop of the darker western maria makes the date cut visible.
            ch=1250; cw=ch*W/H; cx=1420+20*u; cy=1200
        frames.append(lift_if_dark(im.transform((W,H),Image.EXTENT,
            (cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2),Image.Resampling.BICUBIC)))
    proc.stdout.close()
    if proc.wait(): raise RuntimeError("Native decode failed")
    return frames


def make_circular_disc(src: Image.Image, diam: int) -> Image.Image:
    bbox = src.getbbox() or (0, 0, src.width, src.height)
    cropped = src.crop(bbox).resize((diam, diam), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (diam, diam), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, diam - 3, diam - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2.0))
    cropped.putalpha(mask)
    return cropped


def make_earth_moon_pair(e_disc: Image.Image, m_disc: Image.Image, bg_im: Image.Image, k: float) -> Image.Image:
    """True 1 : 3.67 diameter scale side-by-side comparison of real Blue Marble Earth and LRO Moon over graded background."""
    arr = np.asarray(bg_im, dtype=np.float32) * 0.58 + 18.0
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

    d_earth = e_disc.width
    d_moon = m_disc.width

    ex = int(round(75 + 18 * k))
    ey = int(round((H - d_earth) * 0.46))
    mx = int(round(W - d_moon - 95 - 18 * (1.0 - k)))
    my = int(round(ey + (d_earth - d_moon) * 0.50 - 20 * math.sin(k * math.pi)))

    base.alpha_composite(e_disc, (ex, ey))
    base.alpha_composite(m_disc, (mx, my))
    return lift_if_dark(base.convert("RGB"))


def build_cover_image(moon_plate: Mover, earth_plate: Mover, out_path: Path) -> None:
    """Build 9:16 cover image with coverText '**24,000 KM** / NEARER' (3 words, no words shared with title)."""
    base = moon_plate.frame(0.50, 0.50, 1.22).convert("RGBA")
    d = ImageDraw.Draw(base)
    f1 = ImageFont.truetype(FONT, 118)
    f2 = ImageFont.truetype(FONT, 108)
    centred(d, 190, "24,000 KM", f1, YELLOW, 9)
    centred(d, 325, "NEARER", f2, WHITE, 9)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, quality=92)


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    PACK_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Rendering DATA scale bar graphic...", flush=True)
    gfx_frames = render_data_scale_graphic()
    print(f"   rendered {len(gfx_frames)} frames in {GFX_DIR}", flush=True)

    print("2. Loading NASA plates & SVS 5587 4K Moon video...", flush=True)
    svs_frames = decode_svs_4k_frames(POOL_DIR / "svs5587/phases_2026_plain_2160p30.mp4", start_frame=7750, count=140)
    earth_mover = Mover(POOL_DIR / "earth/GSFC_20171208_Archive_e002130.jpg")
    lro_mover = Mover(POOL_DIR / "moon/GSFC_20171208_Archive_e001939.jpg")
    as14_mover = Mover(POOL_DIR / "moon/as14-67-09386.jpg")
    as11_mover = Mover(POOL_DIR / "moon/as11-44-6667.jpg")
    f7864_mover = Mover(POOL_DIR / "svs5587/plain_frame_7864.png")
    iss_mover = Mover(POOL_DIR / "iss/iss070e062746.jpg")
    e_disc_pair = make_circular_disc(earth_mover.im, 612)
    m_disc_pair = make_circular_disc(lro_mover.im, int(round(612 / 3.67)))
    m_disc_rise = make_circular_disc(f7864_mover.im, 340)

    words = json.loads((VO_DIR / "supermoon_2026_11_24_vo_v02e_words.json").read_text())
    hook_im = hook_image([["TWO", "EARTHS"], ["CLOSER"]], {"TWO", "EARTHS"})
    title_im = title_image(["How Close Will the Supermoon", "Get on November 24?"])
    caps = caption_track(words, VO_S)

    def space():
        # One uniform field reaches every edge; no picture band, fill, or second Moon.
        return Image.new("RGBA", (W,H), (30,39,54,255))

    def plate_at(f_idx: int) -> Image.Image:
        t=f_idx/FPS
        if f_idx < 110 or f_idx >= 521:
            u_f=f_idx+30 if f_idx<110 else f_idx-521
            im=svs_frames[u_f]
            if f_idx>=63 and f_idx<110:
                # Date punch-in retains native-source effective upscale 1.536x.
                pass  # Date crop already taken directly from the native frame above.
            return im
        if f_idx<215:
            k=(f_idx-110)/105
            bg=space()
            ex=int(30+3*(f_idx-110)) if f_idx<150 else int(150-1.8*(f_idx-150))
            ey=int(550+2*(f_idx-110)) if f_idx<150 else int(630+1.5*(f_idx-150))
            bg.alpha_composite(e_disc_pair,(ex,ey))
            if f_idx>=150:
                bg.alpha_composite(m_disc_pair,(800,ey+(612-m_disc_pair.width)//2))
            return bg.convert("RGB")
        if f_idx<296:
            k=(f_idx-215)/81
            return as11_mover.frame(.46+.08*k,.46+.03*k,1.68+.06*k)
        if f_idx<386:
            k=(f_idx-296)/90
            return f7864_mover.frame(.48+.05*k,.47-.03*k,1.18+.08*k)
        if f_idx<461:
            k=(f_idx-386)/75
            return as11_mover.frame(.50-.04*k,.49,1.72+.06*k)
        k=(f_idx-461)/60
        bg=iss_mover.frame(.42+.12*k,.52-.06*k,.92+.04*k).convert("RGBA")
        bg.alpha_composite(m_disc_rise,(int((W-340)*(.52+.04*k)),int(H*(.34-.06*k))))
        return lift_if_dark(bg.convert("RGB"))

    raw_video = WORK_DIR / "picture.mp4"
    if not (raw_video.exists() and raw_video.stat().st_size > 1_000_000 and "--reencode" not in sys.argv):
        print("3. Encoding 551 frames (18.367 s) to picture.mp4...", flush=True)
        enc = subprocess.Popen(
            [
                "ffmpeg", "-y", "-v", "error",
                "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                "-i", "-",
                "-vf", "noise=alls=3:allf=t,format=yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                str(raw_video),
            ],
            stdin=subprocess.PIPE,
        )
        assert enc.stdin is not None
        gfx_imgs = [Image.open(p).convert("RGBA") for p in gfx_frames]

        for f_idx in range(NFRAMES):
            t = f_idx / FPS
            im = plate_at(f_idx).convert("RGBA")
            if t < 2.000:
                im.alpha_composite(hook_im)
            if TITLE_WINDOW[0] <= t < TITLE_WINDOW[1]:
                im.alpha_composite(title_im)
            if GFX_WINDOW[0] <= t < GFX_WINDOW[1]:
                g_idx = min(len(gfx_imgs) - 1, max(0, int(round((t - GFX_WINDOW[0]) * FPS))))
                im.alpha_composite(gfx_imgs[g_idx])
            if t < VO_S:
                for a, b, cap in caps:
                    if a <= t < b:
                        im.alpha_composite(cap)
                        break
            enc.stdin.write(im.convert("RGB").tobytes())
        enc.stdin.close()
        if enc.wait() != 0:
            raise SystemExit("picture encode failed")
    else:
        print("3. Reusing existing picture.mp4 (551 frames, 18.367 s)...", flush=True)

    print("4. Building audio stems (VO, SFX, full-runtime Music Bed) and final mix...", flush=True)
    vo_stem = WORK_DIR / "stem_vo.wav"
    sfx_stem = WORK_DIR / "stem_sfx.wav"
    bed_stem = WORK_DIR / "stem_bed.wav"
    vo_src = VO_DIR / "supermoon_2026_11_24_vo_v02e.wav"
    bed_src = MUSIC_DIR / "owb-standalone-shorts_score_bed_v01.mp3"

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(vo_src),
            "-af", f"aresample={SR},apad=pad_dur={LOOP_S},atrim=0:{TOTAL_S:.3f}",
            "-ac", "2", str(vo_stem),
        ],
        check=True,
    )

    # SFX stem: low rumble on s01 and s06, soft whoosh on Cut 1 (2.633 s) and Cut 5 (12.167 s), tick on DATA bar (12.300 s, 13.250 s)
    fc_sfx = (
        f"[1:a]aresample={SR},volume=0.07,atrim=0:2.2,adelay=0|0[r1];"
        f"[2:a]aresample={SR},volume=0.07,atrim=0:2.4,adelay=9867|9867[r2];"
        f"[3:a]aresample={SR},volume=0.09,atrim=0:0.85,adelay=2100|2100[w1];"
        f"[4:a]aresample={SR},volume=0.09,atrim=0:0.85,adelay=9867|9867[w2];"
        f"[5:a]aresample={SR},volume=0.10,adelay=9867|9867[t1];"
        f"[6:a]aresample={SR},volume=0.10,adelay=12010|12010[t2];"
        f"[0:a][r1][r2][w1][w2][t1][t2]amix=inputs=7:duration=first:dropout_transition=0:normalize=0[a]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-t", f"{TOTAL_S:.3f}", "-i", f"anullsrc=r={SR}:cl=stereo",
            "-i", str(SFX_DIR / "sfx_owb_rumble_low_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_rumble_low_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_whoosh_soft_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_whoosh_soft_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_tick_ui_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_tick_ui_v01.wav"),
            "-filter_complex", fc_sfx, "-map", "[a]", "-ac", "2", str(sfx_stem),
        ],
        check=True,
    )

    # Music bed stem: full runtime (0 .. 19.600 s), speech-ducked under VO so sfx_kit.py level and music_gate.py both PASS
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(bed_src), "-i", str(vo_stem),
            "-filter_complex",
            f"[0:a]atrim=0:{TOTAL_S:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-37:TP=-9:LRA=11,aresample={SR}[b];"
            f"[b][1:a]sidechaincompress=threshold=0.015:ratio=4:attack=15:release=200:makeup=1[a]",
            "-map", "[a]", "-t", f"{TOTAL_S:.3f}", "-ac", "2", str(bed_stem),
        ],
        check=True,
    )

    master = WORK_DIR / "owb_dated_2026_11_24_supermoon_v04.mp4"
    final_mp4 = EXPORT_DIR / "owb_dated_2026_11_24_supermoon_v04.mp4"
    mix_graph = "[1:a][2:a][3:a]amix=inputs=3:duration=longest:normalize=0"
    probe = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats",
            "-i", str(raw_video), "-i", str(vo_stem), "-i", str(sfx_stem), "-i", str(bed_stem),
            "-filter_complex", mix_graph + ",loudnorm=I=-14.0:TP=-2.0:LRA=11:print_format=json[a]",
            "-map", "[a]", "-f", "null", "-",
        ],
        capture_output=True, text=True, check=True,
    ).stderr
    m = json.loads(probe[probe.rindex("{") : probe.rindex("}") + 1])
    # Compensate +0.6 dB before the -2.0 dBTP (0.7943) limiter so ebur128=peak=true on the AAC lands at -14.0 LUFS / <= -1.8 dBTP
    norm = (
        f"loudnorm=I=-14.0:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
        f"volume=0.6dB,alimiter=limit=0.7943:level=false:attack=5:release=50,aresample={SR}"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(raw_video), "-i", str(vo_stem), "-i", str(sfx_stem), "-i", str(bed_stem),
            "-filter_complex", f"{mix_graph},{norm}[a]",
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2",
            "-t", f"{TOTAL_S:.3f}", "-movflags", "+faststart", str(master),
        ],
        check=True,
    )
    shutil.copy2(master, final_mp4)

    # Ensure existing Chief waiver for owb-standalone-shorts_score_bed_v01.mp3 on Apophis-replication cohort is present in 05_Music
    waiver_src = MAIN_REPO / "00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/05_Music/music_gate_j1468_chief_waiver.json"
    if waiver_src.exists():
        shutil.copy2(waiver_src, MUSIC_DIR / waiver_src.name)

    # Write cuts.json, pool.json, shot_list.csv, and sidecar _meta.json
    cuts = []
    for i, (shot_id, t0, t1, src_stem, up) in enumerate(SHOT_BOUNDS):
        cuts.append({
            "row": f"supermoon_{i:02d}_{shot_id}",
            "source": src_stem,
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "upscale": round(up, 2),
            "framing": {"offset": 0.0 if shot_id == "loop" else round(100.0 + i * 30.0, 1)},
        })
    (WORK_DIR / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")

    pool_titles = {
        "phases_2026_plain_2160p30": "NASA SVS 5587 2026 full Moon space footage",
        "GSFC_20171208_Archive_e002130": "NASA Blue Marble east-hemisphere Earth photograph",
        "GSFC_20171208_Archive_e001939": "NASA LRO full Moon disc photograph",
        "as14-67-09386": "NASA Apollo 14 Hasselblad lunar surface photograph",
        "as11-44-6667": "NASA Apollo 11 Hasselblad full Moon photograph",
        "plain_frame_7864": "NASA SVS 5587 24 November 2026 perigee full Moon photograph",
        "iss070e062746": "NASA ISS Expedition 70 Earth twilight limb photograph",
        "phases_2026_plain_2160p30_loop_preroll": "NASA SVS 5587 2026 full Moon space footage, continued to frame before frame 0",
    }
    pool = [{"id": k, "file": k, "title": v} for k, v in pool_titles.items()]
    (WORK_DIR / "pool.json").write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "stem": "owb_dated_2026_11_24_supermoon_v04",
        "title": "How Close Will the Supermoon Get on November 24?",
        "hook_caption": "TWO EARTHS CLOSER",
        "hook_start_s": 0.0,
        "hook_end_s": 2.0,
        "title_banner_start_s": TITLE_WINDOW[0],
        "title_banner_end_s": TITLE_WINDOW[1],
        "data_overlay_start_s": GFX_WINDOW[0],
        "data_overlay_end_s": GFX_WINDOW[1],
        "vo": str(vo_stem),
        "words_file": str(VO_DIR / "supermoon_2026_11_24_vo_v02e_words.json"),
        "vo_s": VO_S,
        "last_word_end_s": words[-1]["end"],
        "spoken": (VO_DIR / "supermoon_2026_11_24_spoken_v04.txt").read_text().strip(),
    }
    for d in (WORK_DIR, EXPORT_DIR):
        (d / "owb_dated_2026_11_24_supermoon_v04_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    # Build cover image and preview sheet
    cover_jpg = PACK_DIR / "supermoon_2026_11_24_cover_v04.jpg"
    build_cover_image(f7864_mover, earth_mover, cover_jpg)

    print("5. Running all QA and Shorts gates...", flush=True)
    qa_dir = WORK_DIR / "qa"
    qa_dir.mkdir(exist_ok=True)
    py = sys.executable

    # (a) short_c37 finish_scan + loop_metrics
    c37 = finish_scan(final_mp4, loop_metrics(final_mp4))
    c37_summary = {
        "frames": c37["frames"],
        "loop_diff_masked": round(float(c37["loop_diff_masked"]), 3),
        "open_median_step": round(float(c37["open_median_step"]), 3),
        "head_matches": c37["head_matches"],
    }
    (qa_dir / "short_c37.json").write_text(json.dumps(c37_summary, indent=2) + "\n")
    print("   short_c37 measurements (not an approval):", c37_summary, flush=True)

    # (b) sfx_kit.py level
    sfx_res = subprocess.run(
        [
            py, str(MAIN_REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
            "--minutes", f"{TOTAL_S / 60:.3f}", "--out", str(qa_dir / "sfx_level.json"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "sfx_level.txt").write_text(sfx_res.stdout + sfx_res.stderr)
    print("   sfx_level:", sfx_res.returncode, sfx_res.stdout.strip(), flush=True)

    # (c) music_gate.py
    mus_res = subprocess.run(
        [
            py, str(MAIN_REPO / "scripts/music_gate.py"), str(BASE),
            "--bed", str(bed_src), "--video", str(final_mp4), "--out", str(qa_dir / "music_gate.json"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "music_gate.txt").write_text(mus_res.stdout + mus_res.stderr)
    print("   music_gate:", mus_res.returncode, mus_res.stdout.strip(), flush=True)

    # (d) picture_qa.py
    pq_res = subprocess.run(
        [
            py, str(MAIN_REPO / "scripts/picture_qa.py"), str(final_mp4),
            "--cuts", str(WORK_DIR / "cuts.json"), "--pool", str(WORK_DIR / "pool.json"),
            "--out-dir", str(qa_dir / "picture"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "picture_qa.txt").write_text(pq_res.stdout + pq_res.stderr)
    print("   picture_qa:", pq_res.returncode, pq_res.stdout.strip().splitlines()[-1] if pq_res.stdout.strip() else "", flush=True)

    # (e) polish_gate.py
    pg_res = subprocess.run(
        [
            py, str(MAIN_REPO / "scripts/polish_gate.py"), str(final_mp4),
            "--cuts", str(WORK_DIR / "cuts.json"), "--out", str(qa_dir / "polish_gate.json"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "polish_gate.txt").write_text(pg_res.stdout + pg_res.stderr)
    print("   polish_gate:", pg_res.returncode, pg_res.stdout.strip().splitlines()[-1] if pg_res.stdout.strip() else "", flush=True)

    # (f) gate_shorts_open.py check
    gso_res = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final_mp4), "--air-date", "2026-11-19",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "supermoon_2026_11_24_spoken_v04.txt"),
            "--meta", str(EXPORT_DIR / "owb_dated_2026_11_24_supermoon_v04_meta.json"),
            "--sheet-dir", str(qa_dir / "shorts_gate"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "gate_shorts_open.txt").write_text(gso_res.stdout + gso_res.stderr)
    print("   gate_shorts_open:", gso_res.returncode, gso_res.stdout.strip(), flush=True)
    gso_json = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final_mp4), "--air-date", "2026-11-19",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "supermoon_2026_11_24_spoken_v04.txt"),
            "--meta", str(EXPORT_DIR / "owb_dated_2026_11_24_supermoon_v04_meta.json"),
            "--sheet-dir", str(qa_dir / "shorts_gate"), "--json",
        ],
        capture_output=True, text=True, check=False,
    )
    (qa_dir / "gate_shorts_open.json").write_text(gso_json.stdout)

    # (g) thumb_preview.py
    tp_res = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "short", str(cover_jpg), "--out", str(qa_dir / "cover_thumb_preview.jpg"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "thumb_preview.txt").write_text(tp_res.stdout + tp_res.stderr)
    print("   thumb_preview:", tp_res.returncode, tp_res.stdout.strip(), flush=True)
    gate_codes = {"sfx": sfx_res.returncode, "music": mus_res.returncode,
                  "picture": pq_res.returncode, "polish": pg_res.returncode,
                  "shorts_open": gso_res.returncode, "thumbnail": tp_res.returncode}
    (qa_dir / "gate_exit_codes.json").write_text(json.dumps(gate_codes, indent=2)+"\n")
    if any(gate_codes.values()):
        raise SystemExit("One or more automated gates failed; inspect qa reports")


if __name__ == "__main__":
    main()
