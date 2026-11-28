#!/usr/bin/env python3
"""J3331 — Assemble the 7 December 2026 NASA Nancy Grace Roman Space Telescope First Images dated-event Short
(owb_dated_2026_12_07_roman_first_images_v01.mp4).

- VO: roman_2026_12_07_vo_v02.wav (17.200 s, C7 Trim 2 = 39 words exact, natural 1.00x, zero atempo)
  + 1.000 s forward-loop tail = 18.200 s (546 frames at 30 fps CFR).
  Squarely inside Ben's 16.0-19.0 s Shorts gate band and Rule 16's 17.0-20.0 s band.
- Visuals: 100% full-bleed 9:16 (mode: cover, zero blur-pad/bars per J2545, upscale <= 1.25x) public-domain unlabelled
  NASA plates & footage (£0 spend):
  * NASA Goddard SVS #15081 (15081-_Trailer_Long_Vertical.mp4, 1080x1920 native, caption-free):
    Roman spacecraft in Milky Way (s01 + loop pre-roll), NASA cleanroom mirror barrel (s02),
    dark-energy cosmic web (s06), deep-space galaxy fly-through (s07).
    (Note: SVS #15121 vertical was downloaded & inspected; rejected due to burned-in subtitles on every frame.)
  * NASA/ESA Hubble Ultra Deep Field (GSFC_20171208_Archive_e001061~orig.jpg, 2300x2100) & XDF (e001651~orig.jpg).
  * Own unlabelled code_graphics.py 10x10 real-image mosaic (code_graphic_roman_s04_100x_v01) multiplying 1 real
    Hubble Ultra Deep Field frame into a 10x10 (100x) Roman panorama over full-bleed deep-space stars.
  * NASA KSC 4K SpaceX Falcon Heavy launch footage (KSC-20260830-MH-SPX01-0001_ISO_Drone_4K.mp4, 3840x2160, 0.89x crop).
  * Local SSD NASA SVS #5587 plain 4K full Moon (phases_2026_plain_2160p30.mp4 around full Moon frame 7864) for the
    true-body full-Moon scale icon inside the sole animated DATA overlay.
- Sole Teach Overlay (12.800 - 16.000 s, 3.20 s <= 4.0 s, inside 16:9 centre band y=656..1264, clear of 0-2 s hook
  and 9.20-12.50 s title banner): animated DATA expansion HUBBLE: 1 FRAME -> ROMAN: 100X MORE SKY · BIGGER THAN FULL MOON.
- Audio: VO + synthesized house SFX kit + full-runtime nearest-star_score_bed_v01.mp3 (45 s clean slice under J3299/J3331
  Chief reuse waiver), mixed to -14.0 LUFS / <= -1.8 dBTP.
- Runs all gates: short_c37, sfx_kit.py level, music_gate.py, picture_qa.py, polish_gate.py,
  gate_shorts_open.py (--air-date 2026-12-03), thumb_preview.py short.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

BASE = Path(__file__).resolve().parent
MAIN_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SHARED_POOL = Path("/Users/benjaminoats/_desk/wt-J2478/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/07_Edit-Project/pool_v01")
sys.path.insert(0, str(MAIN_REPO / "scripts"))
from short_c37 import finish_scan, loop_metrics  # noqa: E402

POOL_DIR = BASE / "07_Edit-Project/pool_v01"
VO_DIR = BASE / "02_Voiceover"
MUSIC_DIR = BASE / "05_Music"
SFX_DIR = BASE / "06_Sound-Effects/kit_v01"
GFX_DIR = BASE / "07_Edit-Project/graphics_j3331_v01/code_graphic_roman_s06_fov_data_v01"
MOSAIC_DIR = BASE / "07_Edit-Project/graphics_j3331_v01/code_graphic_roman_s04_100x_v01"
WORK_DIR = BASE / "07_Edit-Project/assembly_j3331_v01"
EXPORT_DIR = BASE / "06_Final-Exports"
PACK_DIR = BASE / "11_Upload-Package"

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
FPS = 30
SR = 48000
VO_S = 17.200
LOOP_S = 1.000
TOTAL_S = 18.200
NFRAMES = int(round(TOTAL_S * FPS))  # 546

WHITE = (245, 248, 255, 255)
YELLOW = (255, 213, 64, 255)
CYAN = (120, 220, 255, 255)
STROKE = (8, 16, 28, 255)

# 8 cuts: Cut 1 at 2.500 s (<= 2.8 s, distinct scene), Cut 2 at 4.667 s (<= 4.8 s), max hold 3.400 s (<= 4.0 s).
# All SVS #15081 stretches separated by >= 10.5 s (37.0, 58.5, 48.0, 0.5).
SHOT_BOUNDS = [
    ("s01", 0.000, 2.500, "15081-_Trailer_Long_Vertical", 1.68, 37.0),
    ("s02", 2.500, 4.667, "15081-_Trailer_Long_Vertical", 1.04, 58.5),
    ("s03", 4.667, 6.700, "GSFC_20171208_Archive_e001061", 1.18, 0.0),
    ("s04", 6.700, 9.300, "code_graphic_roman_s04_100x_v01", 1.00, 0.0),
    ("s05", 9.300, 12.600, "KSC-20260830-MH-SPX01-0001_ISO_Drone_4K", 0.89, 0.5),
    ("s06", 12.600, 16.000, "15081-_Trailer_Long_Vertical", 1.16, 48.0),
    ("s07", 16.000, 17.200, "15081-_Trailer_Long_Vertical", 1.06, 0.5),
    ("loop", 17.200, 18.200, "svs15081_loop_preroll", 1.68, 0.0),
]

TITLE_WINDOW = (9.200, 12.500)
GFX_WINDOW = (12.800, 16.000)


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
    """Hook caption at t=0.0..2.0 s inside y=155..365 (above short_c37 KEEP y=420, inside gate_shorts_open 0.08..0.48 H)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    max_w = int(W * 0.84)
    size = 114
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
    y = 165
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
    font = fit_font(d, max(rows, key=len), 58, int(W * 0.78), 5)
    y = int(H * 0.085)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 12
    return im


def caption_track(words: list[dict], end_s: float) -> list[tuple[float, float, Image.Image]]:
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
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(end_s, g[-1]["end"] + 0.35)
        text = " ".join(w["word"] for w in g).upper().replace(" ,", ",")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        centred(d, int(H * 0.855), text, fit_font(d, text, 56, int(W * 0.76), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def lift_if_dark(im: Image.Image, target_mean: float = 42.0, target_p95: float = 82.0) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean, p95 = float(luma.mean()), float(np.percentile(luma, 95))
    if mean >= target_mean and p95 >= target_p95:
        return im
    scale = max(1.0, target_p95 / max(p95, 1.0))
    lift = max(0.0, target_mean - mean * scale)
    lut = [min(255, int(v * scale + lift * (1.0 - min(255.0, v * scale) / 255.0))) for v in range(256)]
    return im.point(lut * 3)


def crop_box(im: Image.Image, cx_px: float, cy_px: float, ch_px: float) -> Image.Image:
    cw_px = ch_px * (W / H)
    x0 = min(max(cx_px - cw_px / 2.0, 0.0), im.width - cw_px)
    y0 = min(max(cy_px - ch_px / 2.0, 0.0), im.height - ch_px)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw_px, y0 + ch_px), Image.Resampling.BICUBIC)


def decode_video_frames(mp4: Path, start_s: float, count: int, w: int, h: int, vf: str | None = None) -> list[Image.Image]:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(mp4), "-r", str(FPS)]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-frames:v", str(count), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    assert proc.stdout is not None
    fbytes = w * h * 3
    frames: list[Image.Image] = []
    for _ in range(count):
        data = proc.stdout.read(fbytes)
        if len(data) != fbytes:
            raise RuntimeError(f"Incomplete frame decode from {mp4.name} at {start_s}s ({len(frames)}/{count})")
        frames.append(Image.frombytes("RGB", (w, h), data))
    proc.stdout.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg decode failed for {mp4.name}")
    return frames


def decode_svs_moon_disc(video_path: Path, frame_idx: int, diam: int) -> Image.Image:
    """Decode one native 4K SVS #5587 full-Moon frame and extract a clean RGBA disc."""
    ss = frame_idx / FPS
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(video_path),
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    im = Image.frombytes("RGB", (3840, 2160), raw)
    box = (1920 - 1002, 1080 - 1002, 1920 + 1002, 1080 + 1002)
    sub = lift_if_dark(im.crop(box)).resize((diam, diam), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (diam, diam), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, diam - 3, diam - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.5))
    sub.putalpha(mask)
    return sub


def render_mosaic_s04(udf: Image.Image, xdf: Image.Image, nframes: int) -> list[Image.Image]:
    """Own unlabelled code_graphics.py 10x10 real-image mosaic (s04: 6.700-9.300 s, 78 frames).

    Starts close on 1 real NASA/ESA Hubble Ultra Deep Field frame and pulls back smoothly as 100 (10x10)
    real-image deep-field tiles light up around it over a rich full-bleed Hubble XDF starfield.
    Zero text/labels; rounded inset mosaic region so zero full-width/full-height polish_gate seams exist.
    """
    shutil.rmtree(MOSAIC_DIR, ignore_errors=True)
    MOSAIC_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare 10x10 tile sheet (780x780 px = 72% of width, 40% of height -> strictly inset, never full-height/width seams)
    sheet_sz = 780
    cell = sheet_sz // 10  # 78 px
    tile_base = udf.resize((cell, cell), Image.Resampling.LANCZOS)
    tile_alt = xdf.resize((cell, cell), Image.Resampling.LANCZOS)
    tiles_rgb = [
        tile_base,
        tile_base.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
        tile_base.transpose(Image.Transpose.FLIP_TOP_BOTTOM),
        tile_alt,
        tile_alt.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
        tile_alt.transpose(Image.Transpose.ROTATE_90),
    ]

    # Pre-build full 10x10 sheet image
    full_sheet = Image.new("RGB", (sheet_sz, sheet_sz), (14, 24, 42))
    for r in range(10):
        for c in range(10):
            t_im = tiles_rgb[(r * 7 + c * 3) % len(tiles_rgb)]
            full_sheet.paste(t_im, (c * cell, r * cell))
    full_sheet = ImageEnhance.Color(full_sheet).enhance(1.26)
    full_sheet = ImageEnhance.Brightness(full_sheet).enhance(1.22)

    centre_r, centre_c = 4, 4

    out_frames: list[Image.Image] = []
    for i in range(nframes):
        k = i / max(1, nframes - 1)
        ease = k * k * (3.0 - 2.0 * k)

        # Rich full-bleed background cosmos (zero black bands, continuous zoom-out across Hubble XDF)
        bg = crop_box(
            xdf,
            cx_px=1190.0 + 110.0 * k,
            cy_px=1040.0 - 80.0 * k,
            ch_px=1960.0 - 180.0 * k,
        )
        bg = ImageEnhance.Brightness(bg).enhance(0.92)
        canvas = lift_if_dark(bg, target_mean=40.0, target_p95=86.0).convert("RGBA")

        # Draw strictly inset 10x10 mosaic (780x780 centered at 540, 940 -> x=150..930, y=550..1330).
        # Progressive ripple from 1 central cyan-framed Hubble tile out to 100 golden-edged Roman panorama tiles.
        ring_layer = Image.new("RGBA", (sheet_sz, sheet_sz), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring_layer)
        max_dist = math.hypot(5.5, 5.5)
        reveal_radius = 0.55 + ease * (max_dist + 0.7)
        for r in range(10):
            for c in range(10):
                dist = math.hypot(c - centre_c, r - centre_r)
                if dist <= reveal_radius:
                    a = min(1.0, max(0.0, (reveal_radius - dist) / 1.1))
                    if r == centre_r and c == centre_c:
                        a = 1.0
                    patch = full_sheet.crop((c * cell + 3, r * cell + 3, (c + 1) * cell - 3, (r + 1) * cell - 3)).convert("RGBA")
                    if a < 0.99:
                        arr = np.array(patch, dtype=np.float32)
                        arr[:, :, 3] *= a
                        patch = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
                    ring_layer.alpha_composite(patch, (c * cell + 3, r * cell + 3))
                    if r == centre_r and c == centre_c:
                        rd.rounded_rectangle(
                            (c * cell + 2, r * cell + 2, (c + 1) * cell - 3, (r + 1) * cell - 3),
                            radius=6, outline=(110, 225, 255, 245), width=4,
                        )
                    else:
                        rd.rounded_rectangle(
                            (c * cell + 3, r * cell + 3, (c + 1) * cell - 4, (r + 1) * cell - 4),
                            radius=5, outline=(255, 213, 64, int(130 * a)), width=2,
                        )

        if ease > 0.25:
            oa = int(min(225, (ease - 0.25) / 0.55 * 225))
            rd.rounded_rectangle((1, 1, sheet_sz - 2, sheet_sz - 2), radius=16, outline=(255, 213, 64, oa), width=5)

        # Gentle zoom-out from 1.12x -> 0.96x so mosaic always stays strictly inset (never full-width/full-height)
        scale = 1.12 - 0.16 * ease
        vis_w = int(round(sheet_sz * scale))
        scaled = ring_layer.resize((vis_w, vis_w), Image.Resampling.BICUBIC)
        px = (W - vis_w) // 2
        py = (H - vis_w) // 2 - 20
        canvas.alpha_composite(scaled, (px, py))

        rgb = lift_if_dark(canvas.convert("RGB"), target_mean=44.0, target_p95=92.0)
        if i in (0, nframes // 2, nframes - 1):
            rgb.save(MOSAIC_DIR / f"sample_{i:04d}.jpg", quality=92)
        out_frames.append(rgb)
    return out_frames


def render_data_fov_overlay(moon_disc: Image.Image) -> list[Path]:
    """Sole Teach Overlay (12.800 - 16.000 s, 96 frames = 3.20 s <= 4.0 s, inside 16:9 centre band y=656..1264).

    Animated DATA comparison:
    - Line 1 (cyan): HUBBLE: 1 FRAME (3 words <= 4) + 1 reference tile pip
    - Line 2 (yellow): ROMAN: 100X MORE SKY (4 words <= 4) + segmented 20-capsule expanding golden scale bar
    - Line 3 (white): BIGGER THAN FULL MOON (4 words <= 4) + real SVS #5587 full Moon disc icon
    Zero full-width solid bar/box (avoids polish_gate horizontal seam).
    """
    shutil.rmtree(GFX_DIR, ignore_errors=True)
    GFX_DIR.mkdir(parents=True, exist_ok=True)
    dur_s = GFX_WINDOW[1] - GFX_WINDOW[0]
    n = int(round(dur_s * FPS))
    f_hub = ImageFont.truetype(FONT, 38)
    f_rom = ImageFont.truetype(FONT, 44)
    f_sub = ImageFont.truetype(FONT, 38)
    moon_icon = moon_disc.resize((54, 54), Image.Resampling.LANCZOS)

    paths: list[Path] = []
    for i in range(n):
        t = i / FPS
        if t < 0.35:
            alpha = t / 0.35
            dy = int(round((1.0 - alpha) * 26))
        elif t > dur_s - 0.35:
            alpha = max(0.0, (dur_s - t) / 0.35)
            dy = 0
        else:
            alpha = 1.0
            dy = 0
        alpha_ease = alpha * alpha * (3.0 - 2.0 * alpha)

        # Expansion progress p in [0, 1] over t = 0.35 .. 2.05 s
        p = min(1.0, max(0.0, (t - 0.35) / 1.70))
        p_ease = p * p * (3.0 - 2.0 * p)

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # Placed cleanly inside 16:9 centre band (y = 920 .. 1235, strictly within 656..1264; ~11.5% band text height)
        y_top = 925 + dy
        full_w = 520
        x0 = (W - full_w) // 2

        # Row 1: HUBBLE: 1 FRAME (3 words <= 4) + single cyan tile pip
        centred(d, y_top, "HUBBLE: 1 FRAME", f_hub, CYAN, 5)
        hub_bar_y = y_top + 54
        d.rounded_rectangle((x0, hub_bar_y, x0 + 22, hub_bar_y + 18), radius=6, fill=CYAN, outline=STROKE, width=3)

        # Row 2: Animated ROMAN: 100X MORE SKY (4 words <= 4)
        val = max(1, int(round(1 + 99 * p_ease)))
        lbl_rom = f"ROMAN: {val}X MORE SKY" if p_ease < 0.995 else "ROMAN: 100X MORE SKY"
        rom_lbl_y = hub_bar_y + 28
        centred(d, rom_lbl_y, lbl_rom, f_rom, YELLOW, 6)

        # Segmented 20-capsule golden expansion bar (zero continuous seam)
        rom_bar_y = rom_lbl_y + 62
        n_segs = 20
        seg_pitch = full_w / n_segs
        seg_w = int(seg_pitch - 7)
        active_segs = max(1, int(round(1 + (n_segs - 1) * p_ease)))
        for s_i in range(n_segs):
            sx0 = int(round(x0 + s_i * seg_pitch))
            sy_off = 0 if s_i % 5 != 0 else -3
            sh = 20 if s_i % 5 != 0 else 26
            if s_i < active_segs:
                d.rounded_rectangle(
                    (sx0, rom_bar_y + sy_off, sx0 + seg_w, rom_bar_y + sy_off + sh),
                    radius=6,
                    fill=YELLOW,
                    outline=STROKE,
                    width=2,
                )
            else:
                d.rounded_rectangle(
                    (sx0, rom_bar_y + 2, sx0 + seg_w, rom_bar_y + 18),
                    radius=5,
                    fill=(36, 54, 82, 140),
                    outline=(165, 195, 230, 150),
                    width=2,
                )

        # Row 3: SCALE comparison + real full Moon disc (4 words <= 4)
        sub_txt = "BIGGER THAN FULL MOON"
        sb = d.textbbox((0, 0), sub_txt, font=f_sub, stroke_width=5)
        tw = sb[2] - sb[0]
        gap_ic = 14
        tot_w = moon_icon.width + gap_ic + tw
        sx = int(round((W - tot_w) / 2.0))
        sub_y = rom_bar_y + 40
        layer.alpha_composite(moon_icon, (sx, sub_y - 4))
        d.text((sx + moon_icon.width + gap_ic - sb[0], sub_y), sub_txt, font=f_sub, fill=WHITE, stroke_width=5, stroke_fill=STROKE)

        if alpha_ease < 0.999:
            arr = np.array(layer, dtype=np.float32)
            arr[:, :, 3] *= alpha_ease
            layer = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

        fp = GFX_DIR / f"frame_{i:04d}.png"
        layer.save(fp)
        paths.append(fp)
    return paths


def build_cover_image(roman_hero: Image.Image, udf: Image.Image, moon_disc: Image.Image, out_path: Path) -> None:
    """Build 9:16 custom cover (1080x1920) with coverText '**100** / HUBBLES' (2 words, zero words shared with title)."""
    # Vibrant deep-field cosmos backdrop blended gently behind Roman hero spacecraft so near-black stays <= 30%
    bg_udf = crop_box(udf, 1150.0, 1050.0, 1900.0)
    bg_udf = ImageEnhance.Color(bg_udf).enhance(1.35)
    bg_udf = ImageEnhance.Brightness(bg_udf).enhance(1.22)

    hero = ImageEnhance.Color(roman_hero).enhance(1.28)
    hero = ImageEnhance.Contrast(hero).enhance(1.18)
    hero = lift_if_dark(hero, target_mean=48.0, target_p95=115.0)

    # Screen-like bright galaxy infusion into dark sky regions around the Roman spacecraft
    a_h = np.asarray(hero, dtype=np.float32)
    a_u = np.asarray(bg_udf, dtype=np.float32)
    comp = np.clip(a_h + a_u * 0.42, 0, 255).astype(np.uint8)
    base_rgba = lift_if_dark(Image.fromarray(comp, "RGB"), target_mean=54.0, target_p95=135.0).convert("RGBA")

    # Subtle glowing real full Moon scale accent clear of the Roman telescope body (upper-right of centre band)
    m_small = moon_disc.resize((210, 210), Image.Resampling.LANCZOS)
    base_rgba.alpha_composite(m_small, (780, 675))

    d = ImageDraw.Draw(base_rgba)
    f1 = ImageFont.truetype(FONT, 152)
    f2 = ImageFont.truetype(FONT, 116)
    centred(d, 175, "100", f1, YELLOW, 10)
    centred(d, 345, "HUBBLES", f2, WHITE, 10)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base_rgba.convert("RGB").save(out_path, quality=93)


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    PACK_DIR.mkdir(parents=True, exist_ok=True)

    svs15081 = POOL_DIR / "svs15081/15081-_Trailer_Long_Vertical.mp4"
    ksc_drone = POOL_DIR / "ksc_launch/KSC-20260830-MH-SPX01-0001_ISO_Drone_4K.mp4"
    udf_path = POOL_DIR / "hubble/GSFC_20171208_Archive_e001061~orig.jpg"
    xdf_path = POOL_DIR / "hubble/GSFC_20171208_Archive_e001651~orig.jpg"
    moon_4k = SHARED_POOL / "svs5587/phases_2026_plain_2160p30.mp4"

    print("1. Loading NASA Hubble UDF/XDF & decoding SVS #5587 full Moon disc...", flush=True)
    udf_im = lift_if_dark(Image.open(udf_path).convert("RGB"), target_mean=42.0, target_p95=90.0)
    xdf_im = lift_if_dark(Image.open(xdf_path).convert("RGB"), target_mean=42.0, target_p95=90.0)
    moon_disc = decode_svs_moon_disc(moon_4k, frame_idx=7864, diam=260)

    print("2. Rendering sole DATA+SCALE overlay & s04 10x10 real-image mosaic...", flush=True)
    gfx_frames = render_data_fov_overlay(moon_disc)
    print(f"   DATA overlay: {len(gfx_frames)} frames in {GFX_DIR}", flush=True)
    s04_frames = render_mosaic_s04(udf_im, xdf_im, nframes=78)
    print(f"   s04 10x10 mosaic: {len(s04_frames)} frames", flush=True)

    print("3. Decoding clean unlabelled NASA SVS #15081 and KSC 4K Falcon Heavy clips...", flush=True)
    # Loop pre-roll (30 frames: 36.0-37.0 s) + s01 (75 frames: 37.0-39.5 s) = 105 continuous frames of Roman in Milky Way
    # Cropped 915x1626 at (40, 80) -> cleanly removes bottom-right tiny 'Animation' text; plus gentle push-in for crisp open motion.
    open_raw = decode_video_frames(svs15081, start_s=36.0, count=105, w=1080, h=1920)
    open_frames: list[Image.Image] = []
    for i, im in enumerate(open_raw):
        u = i / 104.0
        # Crop strictly inside x <= 908, y <= 1645 across all 105 frames (including loop pre-roll i=0..29)
        # so the bottom-right NASA 'Animation' credit is 100% excluded, with brisk push-in (upscale <= 1.68x).
        ch = 1540.0 - 400.0 * u
        cx = 475.0 - 60.0 * u
        cy = 875.0 - 80.0 * u
        fr = crop_box(im, cx_px=cx, cy_px=cy, ch_px=ch)
        fr = ImageEnhance.Color(fr).enhance(1.18)
        fr = lift_if_dark(fr, target_mean=42.0, target_p95=92.0)
        open_frames.append(fr)

    # s02 (frames 75..139 = 65 frames, 2.500-4.667 s): Real NASA Goddard cleanroom footage of Roman Space Telescope (58.5 s)
    s02_raw = decode_video_frames(svs15081, start_s=58.5, count=65, w=1080, h=1920)
    s02_frames = [
        crop_box(im, 540.0, 960.0 - 15.0 * (i / 64.0), 1860.0 - 50.0 * (i / 64.0))
        for i, im in enumerate(s02_raw)
    ]

    # s05 (frames 279..377 = 99 frames, 9.300-12.600 s): Real NASA KSC 4K Falcon Heavy launch of Roman (0.5 s)
    # Native 3840x2160 cropped centred to 1215x2160 -> 1080x1920 (upscale 0.89x, zero upscaling!)
    s05_raw = decode_video_frames(
        ksc_drone, start_s=0.5, count=99, w=1080, h=1920,
        vf="crop=1215:2160:1312:0,scale=1080:1920:flags=lanczos",
    )
    s05_frames = [lift_if_dark(ImageEnhance.Contrast(im).enhance(1.08), target_mean=44.0, target_p95=120.0) for im in s05_raw]

    # s06 (frames 378..479 = 102 frames, 12.600-16.000 s): SVS #15081 cosmic web dark energy / dark matter filaments (48.0 s)
    # Cropped inside top-left 0..930, 0..1650 to remove tiny bottom-right credit
    s06_raw = decode_video_frames(svs15081, start_s=48.0, count=102, w=1080, h=1920)
    s06_frames: list[Image.Image] = []
    for i, im in enumerate(s06_raw):
        u = i / 101.0
        fr = crop_box(im, cx_px=475.0 + 18.0 * u, cy_px=830.0 + 15.0 * u, ch_px=1655.0 - 45.0 * u)
        s06_frames.append(lift_if_dark(fr, target_mean=48.0, target_p95=115.0))

    # s07 (frames 480..515 = 36 frames + 8 extra for loop crossfade = 44 frames, 16.000-17.200 s): SVS #15081 galaxy fly-through (0.5 s)
    s07_raw = decode_video_frames(svs15081, start_s=0.5, count=44, w=1080, h=1920)
    s07_frames = [
        lift_if_dark(
            ImageEnhance.Color(crop_box(im, 540.0, 960.0, 1840.0 - 70.0 * (i / 43.0))).enhance(1.22),
            target_mean=42.0, target_p95=92.0,
        )
        for i, im in enumerate(s07_raw)
    ]

    words = json.loads((VO_DIR / "roman_2026_12_07_vo_v02_words.json").read_text())
    hook_im = hook_image([["100X"], ["MORE", "SKY"]], {"100X"})
    title_im = title_image(["What Will NASA's Roman", "Telescope Reveal on Dec 7?"])
    caps = caption_track(words, VO_S)

    def plate_at(f_idx: int) -> Image.Image:
        # s01 (0..74): Roman Space Telescope gliding across Milky Way (continuous after loop pre-roll 0..29)
        if f_idx < 75:
            return open_frames[f_idx + 30]
        # s02 (75..139): Real NASA Goddard cleanroom Roman Space Telescope
        if f_idx < 140:
            return s02_frames[f_idx - 75]
        # s03 (140..200): Hubble Ultra Deep Field smooth push-out
        if f_idx < 201:
            k = (f_idx - 140) / 60.0
            return crop_box(udf_im, cx_px=1150.0 + 80.0 * k, cy_px=1050.0 - 50.0 * k, ch_px=1680.0 + 260.0 * k)
        # s04 (201..278): Own unlabelled 10x10 real-image Hubble->Roman mosaic
        if f_idx < 279:
            return s04_frames[f_idx - 201]
        # s05 (279..377): Real NASA KSC 4K Falcon Heavy launch of Roman
        if f_idx < 378:
            return s05_frames[f_idx - 279]
        # s06 (378..479): Dark energy / dark matter cosmic web filaments (hosts sole DATA+SCALE overlay)
        if f_idx < 480:
            return s06_frames[f_idx - 378]
        # s07 (480..515): Deep-space galaxy fly-through
        if f_idx < 516:
            return s07_frames[f_idx - 480]
        # loop (516..545): 1.000 s forward-loop tail (7-frame / 0.233 s crossfade from s07 into open_frames[0..29])
        u_f = f_idx - 516
        preroll = open_frames[u_f]
        if u_f < 7:
            alpha = (u_f + 1) / 8.0
            tail = s07_frames[min(len(s07_frames) - 1, 36 + u_f)]
            return Image.blend(tail, preroll, alpha)
        return preroll

    raw_video = WORK_DIR / "picture.mp4"
    print(f"4. Encoding {NFRAMES} frames ({TOTAL_S:.3f} s) to picture.mp4...", flush=True)
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

    print("5. Building audio stems (VO, SFX, full-runtime nearest-star bed) and -14 LUFS final mix...", flush=True)
    vo_stem = WORK_DIR / "stem_vo.wav"
    sfx_stem = WORK_DIR / "stem_sfx.wav"
    bed_stem = WORK_DIR / "stem_bed.wav"
    vo_src = VO_DIR / "roman_2026_12_07_vo_v02.wav"
    bed_src = MUSIC_DIR / "nearest-star_score_bed_v01.mp3"

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(vo_src),
            "-af", f"aresample={SR},apad=pad_dur={LOOP_S + 0.1:.3f},atrim=0:{TOTAL_S:.3f}",
            "-ac", "2", str(vo_stem),
        ],
        check=True,
    )

    # House SFX: whoosh at Frame 0 (0.00 s) & Cut 5 deep-space reveal (12.60 s),
    # low rumble under s05 Falcon Heavy launch (9.30-12.60 s),
    # subtle ticks at DATA overlay entry (12.80 s) & 100X full expansion (14.85 s).
    fc_sfx = (
        f"[1:a]aresample={SR},volume=0.065,atrim=0:3.1,adelay=9300|9300[r1];"
        f"[2:a]aresample={SR},volume=0.085,atrim=0:0.85,adelay=0|0[w1];"
        f"[3:a]aresample={SR},volume=0.085,atrim=0:0.85,adelay=12600|12600[w2];"
        f"[4:a]aresample={SR},volume=0.095,adelay=12800|12800[t1];"
        f"[5:a]aresample={SR},volume=0.095,adelay=14850|14850[t2];"
        f"[0:a][r1][w1][w2][t1][t2]amix=inputs=6:duration=first:dropout_transition=0:normalize=0[a]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-t", f"{TOTAL_S:.3f}", "-i", f"anullsrc=r={SR}:cl=stereo",
            "-i", str(SFX_DIR / "sfx_owb_rumble_low_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_whoosh_soft_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_whoosh_soft_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_tick_ui_v01.wav"),
            "-i", str(SFX_DIR / "sfx_owb_tick_ui_v01.wav"),
            "-filter_complex", fc_sfx, "-map", "[a]", "-ac", "2", str(sfx_stem),
        ],
        check=True,
    )

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

    stem_name = "owb_dated_2026_12_07_roman_first_images_v01"
    master = WORK_DIR / f"{stem_name}.mp4"
    final_mp4 = EXPORT_DIR / f"{stem_name}.mp4"
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
    norm = (
        f"loudnorm=I=-14.0:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
        f"volume=0.5dB,alimiter=limit=0.7943:level=false:attack=5:release=50,aresample={SR}"
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

    cuts = []
    for i, (shot_id, t0, t1, src_stem, up, off_s) in enumerate(SHOT_BOUNDS):
        cuts.append({
            "row": f"roman_{i:02d}_{shot_id}",
            "source": src_stem,
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "upscale": round(up, 2),
            "framing": {"offset": round(off_s, 1)},
        })
    (WORK_DIR / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")

    pool_titles = {
        "15081-_Trailer_Long_Vertical": "NASA Goddard SVS 15081 Nancy Grace Roman Space Telescope spacecraft, cleanroom and cosmic web footage",
        "GSFC_20171208_Archive_e001061": "NASA ESA Hubble Ultra Deep Field deep-space galaxy photograph",
        "code_graphic_roman_s04_100x_v01": "Own unlabelled 10x10 Hubble-to-Roman wide-field deep-space tile sequence over NASA Hubble XDF",
        "KSC-20260830-MH-SPX01-0001_ISO_Drone_4K": "NASA Kennedy Space Center 4K SpaceX Falcon Heavy liftoff footage of Roman Space Telescope",
        "svs15081_loop_preroll": "NASA Goddard SVS 15081 Roman Space Telescope Milky Way pre-roll continued into frame 0",
    }
    pool = [{"id": k, "file": k, "title": v} for k, v in pool_titles.items()]
    (WORK_DIR / "pool.json").write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "stem": stem_name,
        "title": "What Will NASA's Roman Telescope Reveal on Dec 7?",
        "hook_caption": "100X MORE SKY",
        "hook_start_s": 0.0,
        "hook_end_s": 2.0,
        "title_banner_start_s": TITLE_WINDOW[0],
        "title_banner_end_s": TITLE_WINDOW[1],
        "data_overlay_start_s": GFX_WINDOW[0],
        "data_overlay_end_s": GFX_WINDOW[1],
        "vo": str(vo_stem),
        "words_file": str(VO_DIR / "roman_2026_12_07_vo_v02_words.json"),
        "vo_s": VO_S,
        "last_word_end_s": words[-1]["end"],
        "spoken": (VO_DIR / "roman_2026_12_07_spoken_v02_trim2.txt").read_text().strip(),
    }
    for d in (WORK_DIR, EXPORT_DIR):
        (d / f"{stem_name}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    cover_jpg = PACK_DIR / "roman_2026_12_07_cover_v01.jpg"
    build_cover_image(open_frames[55], udf_im, moon_disc, cover_jpg)

    print("6. Running all QA and Shorts gates...", flush=True)
    qa_dir = WORK_DIR / "qa"
    qa_dir.mkdir(exist_ok=True)
    py = sys.executable

    # (a) short_c37
    c37 = finish_scan(final_mp4, loop_metrics(final_mp4))
    c37_summary = {
        "frames": c37["frames"],
        "loop_diff_masked": round(float(c37["loop_diff_masked"]), 3),
        "open_median_step": round(float(c37["open_median_step"]), 3),
        "head_matches": c37["head_matches"],
    }
    (qa_dir / "short_c37.json").write_text(json.dumps(c37_summary, indent=2) + "\n")
    print("   short_c37:", c37_summary, flush=True)

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
    print("   music_gate:", mus_res.returncode, mus_res.stdout.strip().splitlines()[-1] if mus_res.stdout.strip() else "", flush=True)

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

    # (f) gate_shorts_open.py check (--air-date 2026-12-03)
    gso_res = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final_mp4), "--air-date", "2026-12-03",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "roman_2026_12_07_spoken_v02_trim2.txt"),
            "--meta", str(EXPORT_DIR / f"{stem_name}_meta.json"),
            "--sheet-dir", str(qa_dir / "shorts_gate"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "gate_shorts_open.txt").write_text(gso_res.stdout + gso_res.stderr)
    print("   gate_shorts_open:", gso_res.returncode, gso_res.stdout.strip(), flush=True)

    gso_json = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final_mp4), "--air-date", "2026-12-03",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "roman_2026_12_07_spoken_v02_trim2.txt"),
            "--meta", str(EXPORT_DIR / f"{stem_name}_meta.json"),
            "--sheet-dir", str(qa_dir / "shorts_gate"), "--json",
        ],
        capture_output=True, text=True, check=False,
    )
    (qa_dir / "gate_shorts_open.json").write_text(gso_json.stdout)

    # (g) thumb_preview.py short
    tp_res = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"),
            "short", str(cover_jpg), "--out", str(qa_dir / "cover_thumb_preview.jpg"),
        ],
        capture_output=True, text=True,
    )
    (qa_dir / "thumb_preview.txt").write_text(tp_res.stdout + tp_res.stderr)
    print("   thumb_preview:", tp_res.returncode, tp_res.stdout.strip(), flush=True)

    gate_codes = {
        "sfx": sfx_res.returncode,
        "music": mus_res.returncode,
        "picture": pq_res.returncode,
        "polish": pg_res.returncode,
        "shorts_open": gso_res.returncode,
        "thumbnail": tp_res.returncode,
    }
    (qa_dir / "gate_exit_codes.json").write_text(json.dumps(gate_codes, indent=2) + "\n")
    print("   gate_exit_codes:", gate_codes, flush=True)
    if any(gate_codes.values()):
        raise SystemExit(f"One or more automated gates failed: {gate_codes}")


if __name__ == "__main__":
    main()
