#!/usr/bin/env python3
"""J2916 — Assemble the 30 November 2026 Moon-Jupiter conjunction dated-event Short
(owb_dated_2026_11_30_moon_jupiter_v01.mp4).

- VO: moon_jupiter_2026_11_30_vo_v02.wav (18.480 s, 47 words exact) + 1.020 s forward-loop tail = 19.500 s (585 frames at 30 fps).
- Visuals: 100% full-bleed 9:16 (mode: cover, zero blur-pad/bars per J2545, upscale <= 1.96x) public-domain unlabelled NASA plates:
  Juno PIA22946, PIA26077, PIA21974; SVS 5587 4K 2026 Moon video & Frame 8001 (2026-11-30 08:00 UTC);
  NASA Blue Marble Earth; NASA LRO Moon; Apollo 11 Moon; NASA ISS Expedition 70 pre-dawn twilight limb.
- Sole Teach Overlay (12.400 - 16.200 s, 3.80 s <= 4.0 s, inside 16:9 band): animated DATA horizontal distance bar
  comparing MOON: 373,000 KM with JUPITER: 754 MILLION KM and SCALE: 2,000 TIMES FARTHER.
- Audio: VO + synthesized house SFX kit + full-runtime 020 Jupiter Short score bed, mixed to -14.0 LUFS / <= -1.8 dBTP.
- Runs all gates: vo_check, sfx_kit.py level, music_gate.py, picture_qa.py, polish_gate.py, short_c37.py, gate_shorts_open.py, thumb_preview.py.
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
GFX_DIR = BASE / "07_Edit-Project/graphics_j2916_v01/code_graphic_moon_jupiter_s07_dist_v01"
WORK_DIR = BASE / "07_Edit-Project/assembly_j2916_v01"
EXPORT_DIR = BASE / "06_Final-Exports"
PACK_DIR = BASE / "11_Upload-Package"

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
W, H = 1080, 1920
FPS = 30
SR = 48000
VO_S = 18.480
LOOP_S = 1.020
TOTAL_S = 19.500
NFRAMES = int(round(TOTAL_S * FPS))  # 585

WHITE = (245, 248, 255, 255)
YELLOW = (255, 213, 64, 255)
CYAN = (120, 220, 255, 255)
STROKE = (8, 16, 28, 255)

# Shot boundaries (s): 8 VO shots + 1.000 s forward-loop tail (max hold 3.167 s <= 4.0 s; Cut 1 at 2.567 s <= 2.8 s; Cut 2 at 4.200 s <= 4.8 s)
SHOT_BOUNDS = [
    ("s01", 0.000, 2.567, "PIA22946", 1.32),
    ("s02", 2.567, 4.200, "moon.8001", 1.48),
    ("s03", 4.200, 5.733, "GSFC_20171208_Archive_e002130", 0.85),
    ("s04", 5.733, 7.733, "PIA26077", 1.94),
    ("s05", 7.733, 10.500, "code_graphic_moon_jupiter_s05_40x_v01", 1.76),
    ("s06", 10.500, 13.667, "GSFC_20171208_Archive_e001939", 1.85),
    ("s07", 13.667, 16.667, "as11-44-6667", 1.76),
    ("s08", 16.667, 18.500, "iss070e062746", 0.92),
    ("loop", 18.500, 19.500, "PIA22946_loop_preroll", 1.26),
]

TITLE_WINDOW = (9.100, 12.600)
GFX_WINDOW = (13.200, 16.300)


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
    """Hook caption at t=0.0..2.0 s: sits inside y=155..365 (above short_c37 KEEP y=420, inside gate_shorts_open 0.08..0.48 H)."""
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
    font = fit_font(d, max(rows, key=len), 60, int(W * 0.76), 5)
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
        centred(d, int(H * 0.855), text, fit_font(d, text, 56, int(W * 0.74), 6), WHITE, 6)
        out.append((start, stop, im))
    return out


def render_data_scale_graphic() -> list[Path]:
    """Render the sole teach overlay (12.400 - 16.200 s, 114 frames = 3.80 s) into GFX_DIR.

    Shows animated horizontal distance bar comparing MOON: 373,000 KM with JUPITER: 754 MILLION KM
    and SCALE sub-line '2,000 TIMES FARTHER' (<= 4 words per label, inside 16:9 centre band y=656..1264,
    zero full-width box or seam).
    """
    shutil.rmtree(GFX_DIR, ignore_errors=True)
    GFX_DIR.mkdir(parents=True, exist_ok=True)
    dur_s = GFX_WINDOW[1] - GFX_WINDOW[0]
    n = int(round(dur_s * FPS))
    f_moon = ImageFont.truetype(FONT, 36)
    f_jup = ImageFont.truetype(FONT, 42)
    f_sub = ImageFont.truetype(FONT, 38)
    paths = []
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
        alpha_ease = alpha * alpha * (3 - 2 * alpha)

        # Extension progress p in [0, 1] over t = 0.35 .. 2.15 s
        p = min(1.0, max(0.0, (t - 0.35) / 1.80))
        p_ease = p * p * (3 - 2 * p)

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # Inside lower half of 16:9 centre band (y = 975 .. 1245, inside 656..1264)
        y_top = 975 + dy
        full_w = 500
        x0 = (W - full_w) // 2

        # Reference row: MOON: 373,000 KM (3 words <= 4) + reference pip
        centred(d, y_top, "MOON: 373,000 KM", f_moon, CYAN, 5)
        moon_bar_y = y_top + 52
        d.rounded_rectangle((x0, moon_bar_y, x0 + 18, moon_bar_y + 16), radius=8, fill=CYAN, outline=STROKE, width=3)

        # Animated Jupiter distance bar & counter: JUPITER: 754 MILLION KM (4 words <= 4)
        mio_val = max(1, int(round(1 + (754 - 1) * p_ease)))
        lbl_jup = f"JUPITER: {mio_val} MILLION KM" if p_ease < 0.995 else "JUPITER: 754 MILLION KM"
        jup_lbl_y = moon_bar_y + 26
        centred(d, jup_lbl_y, lbl_jup, f_jup, YELLOW, 5)

        # Segmented 20-capsule scale track (prevents any continuous horizontal seam across crater background)
        jup_bar_y = jup_lbl_y + 58
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
                    (sx0, jup_bar_y + sy_off, sx0 + seg_w, jup_bar_y + sy_off + sh),
                    radius=6,
                    fill=YELLOW,
                    outline=STROKE,
                    width=2,
                )
            else:
                d.rounded_rectangle(
                    (sx0, jup_bar_y + 2, sx0 + seg_w, jup_bar_y + 18),
                    radius=5,
                    fill=(36, 54, 82, 135),
                    outline=(165, 195, 230, 145),
                    width=2,
                )

        # Scale comparison label (3 words <= 4): 2,000 TIMES FARTHER
        centred(d, jup_bar_y + 34, "2,000 TIMES FARTHER", f_sub, WHITE, 5)

        if alpha_ease < 0.999:
            arr = np.array(layer, dtype=np.float32)
            arr[:, :, 3] *= alpha_ease
            layer = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")

        fp = GFX_DIR / f"frame_{i:04d}.png"
        layer.save(fp)
        paths.append(fp)
    return paths


def lift_if_dark(im: Image.Image) -> Image.Image:
    arr = np.asarray(im, dtype=np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mean, p95 = float(luma.mean()), float(np.percentile(luma, 95))
    if mean >= 38.0 and p95 >= 72.0:
        return im
    scale = max(1.0, 72.0 / max(p95, 1.0))
    lift = max(0.0, 40.0 - mean * scale)
    lut = [min(255, int(v * scale + lift * (1.0 - min(255.0, v * scale) / 255.0))) for v in range(256)]
    return im.point(lut * 3)


def crop_box(im: Image.Image, cx_px: float, cy_px: float, ch_px: float) -> Image.Image:
    """Smooth sub-pixel crop of size (ch_px * 9/16, ch_px) centered at (cx_px, cy_px), scaled to 1080x1920."""
    cw_px = ch_px * (W / H)
    x0 = min(max(cx_px - cw_px / 2.0, 0.0), im.width - cw_px)
    y0 = min(max(cy_px - ch_px / 2.0, 0.0), im.height - ch_px)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw_px, y0 + ch_px), Image.Resampling.BICUBIC)


def make_circular_disc(src: Image.Image, bbox: tuple[int, int, int, int], diam: int) -> Image.Image:
    cropped = src.crop(bbox).resize((diam, diam), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (diam, diam), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, diam - 3, diam - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2.0))
    cropped.putalpha(mask)
    return cropped


def decode_svs_moon_discs(video_path: Path, start_frame: int, count: int, diam: int) -> list[Image.Image]:
    """Decode `count` 4K (3840x2160) frames around Nov 30 (Frame 8001) and extract circular Moon RGBA discs."""
    ss = start_frame / FPS
    proc = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(video_path),
            "-frames:v", str(count), "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=subprocess.PIPE,
    )
    assert proc.stdout is not None
    mask = Image.new("L", (diam, diam), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, diam - 3, diam - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2.2))

    discs: list[Image.Image] = []
    # In SVS 5587 3840x2160 plain frames, the Moon disc sits centered at (1920, 1080) with radius ~996 px.
    box = (1920 - 1002, 1080 - 1002, 1920 + 1002, 1080 + 1002)
    fbytes = 3840 * 2160 * 3
    for _ in range(count):
        data = proc.stdout.read(fbytes)
        if len(data) != fbytes:
            raise RuntimeError("Incomplete SVS 4K frame")
        im = Image.frombytes("RGB", (3840, 2160), data)
        sub = lift_if_dark(im.crop(box)).resize((diam, diam), Image.Resampling.LANCZOS).convert("RGBA")
        sub.putalpha(mask)
        discs.append(sub)
    proc.stdout.close()
    if proc.wait() != 0:
        raise RuntimeError("SVS 4K ffmpeg decode failed")
    return discs


def make_jupiter_beacon(jup_disc: Image.Image, core_d: int = 34) -> Image.Image:
    """Bright -2.2 mag Jupiter beacon with warm golden atmospheric glow for sky/distance shots."""
    size = core_d * 5
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    c = size // 2
    for r, a in ((core_d * 2, 38), (int(core_d * 1.4), 75), (int(core_d * 0.9), 135)):
        d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 232, 175, a))
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=6.0))
    core = jup_disc.resize((core_d, core_d), Image.Resampling.LANCZOS)
    canvas.alpha_composite(core, (c - core_d // 2, c - core_d // 2))
    return canvas


def build_cover_image(jup_im: Image.Image, moon8001_rgba: Image.Image, out_path: Path) -> None:
    """Build 9:16 cover image (1080x1920) with coverText '**2,000X** / FARTHER' (2 words, zero words shared with title)."""
    # Rich full-bleed Juno Jupiter crop (including Great Red Spot / storm)
    base = crop_box(jup_im, 1520.0, 1420.0, 1480.0)
    base = ImageEnhance.Color(base).enhance(1.28)
    base = ImageEnhance.Contrast(base).enhance(1.12)
    base_rgba = lift_if_dark(base).convert("RGBA")

    # Crisp 30 Nov 2026 waning gibbous Moon inside both 9:16 frame and 16:9 centre crop (y=656..1264)
    m_crop = moon8001_rgba.crop((920, 80, 2920, 2080)).resize((390, 390), Image.Resampling.LANCZOS)
    base_rgba.alpha_composite(m_crop, (590, 730))

    d = ImageDraw.Draw(base_rgba)
    f1 = ImageFont.truetype(FONT, 128)
    f2 = ImageFont.truetype(FONT, 110)
    centred(d, 185, "2,000X", f1, YELLOW, 9)
    centred(d, 330, "FARTHER", f2, WHITE, 9)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base_rgba.convert("RGB").save(out_path, quality=93)


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    PACK_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Rendering DATA distance scale bar graphic...", flush=True)
    gfx_frames = render_data_scale_graphic()
    print(f"   rendered {len(gfx_frames)} frames in {GFX_DIR}", flush=True)

    print("2. Loading NASA Juno/Moon/Earth/ISS plates & SVS 5587 4K Nov 30 Moon video...", flush=True)
    jup_22946 = lift_if_dark(Image.open(POOL_DIR / "jupiter/PIA22946~orig.jpg").convert("RGB")).filter(
        ImageFilter.UnsharpMask(radius=1.6, percent=135, threshold=2)
    )
    jup_26077 = lift_if_dark(Image.open(POOL_DIR / "jupiter/PIA26077~orig.jpg").convert("RGB")).filter(
        ImageFilter.UnsharpMask(radius=1.5, percent=145, threshold=2)
    )
    jup_21974 = lift_if_dark(Image.open(POOL_DIR / "jupiter/PIA21974~orig.tif").convert("RGB"))
    moon_8001_rgba = Image.open(POOL_DIR / "svs5587/moon.8001.tif").convert("RGBA")
    moon_8001_canvas = Image.new("RGBA", moon_8001_rgba.size, (0, 0, 0, 255))
    moon_8001_canvas.alpha_composite(moon_8001_rgba)
    moon_8001_rgb = lift_if_dark(moon_8001_canvas.convert("RGB"))

    earth_im = lift_if_dark(Image.open(SHARED_POOL / "earth/GSFC_20171208_Archive_e002130.jpg").convert("RGB"))
    lro_im = lift_if_dark(Image.open(SHARED_POOL / "moon/GSFC_20171208_Archive_e001939.jpg").convert("RGB"))
    as11_raw = Image.open(SHARED_POOL / "moon/as11-44-6667.jpg").convert("RGB")
    iss_im = lift_if_dark(Image.open(SHARED_POOL / "iss/iss070e062746.jpg").convert("RGB"))

    # Composite real ISS070 starfield into the black space sky above Apollo 11's curved lunar horizon
    as11_arr = np.asarray(as11_raw, dtype=np.float32)
    as11_luma = 0.2126 * as11_arr[:, :, 0] + 0.7152 * as11_arr[:, :, 1] + 0.0722 * as11_arr[:, :, 2]
    sky_mask = np.clip((26.0 - as11_luma) / 16.0, 0.0, 1.0)
    iss_stars = np.asarray(iss_im.crop((600, 0, 600 + as11_raw.width * 2, 1100)).resize(as11_raw.size, Image.Resampling.BICUBIC), dtype=np.float32)
    iss_stars = np.clip(iss_stars * 1.45, 0.0, 255.0)
    as11_comp = np.clip(as11_arr * (1.0 - sky_mask[:, :, None]) + iss_stars * sky_mask[:, :, None], 0.0, 255.0).astype(np.uint8)
    as11_im = lift_if_dark(Image.fromarray(as11_comp, "RGB"))

    # Native 4K Moon discs around Frame 8001 (2026-11-30T08:00 UTC): 110 frames covers loop (30f) + s01 (77f)
    svs_moon_discs = decode_svs_moon_discs(
        SHARED_POOL / "svs5587/phases_2026_plain_2160p30.mp4",
        start_frame=7945,
        count=110,
        diam=500,
    )

    # True-scale real-body discs:
    # - s04 (11 : 1 Jupiter-to-Earth): PIA26077 cropped at ch=990 spans ~2,600 px of Jupiter diameter -> Earth diam = 236 px (~1 : 11)
    earth_disc_11x = make_circular_disc(earth_im, (150, 150, 3565, 3565), 236)
    # - s05 (40 : 1 Jupiter-to-Moon): PIA21974 cropped at ch=1090 spans ~3,800 px of Jupiter diameter -> Moon diam = 95 px (exact 40 : 1)
    moon_disc_40x = make_circular_disc(lro_im, (55, 55, 1545, 1545), 95)
    # - s07 & s08 Jupiter beacon + rising Nov 30 Moon
    jup_full_disc = make_circular_disc(jup_22946, (380, 415, 2550, 2530), 240)
    jup_beacon_far = make_jupiter_beacon(jup_full_disc, core_d=36)
    jup_beacon_sky = make_jupiter_beacon(jup_full_disc, core_d=28)
    moon_rise_disc = moon_8001_rgba.crop((920, 80, 2920, 2080)).resize((250, 250), Image.Resampling.LANCZOS)

    words = json.loads((VO_DIR / "moon_jupiter_2026_11_30_vo_v02_words.json").read_text())
    hook_im = hook_image([["FORTY", "TIMES"], ["WIDER"]], {"FORTY", "TIMES"})
    title_im = title_image(["Why Is Jupiter Beside the", "Moon on November 30?"])
    caps = caption_track(words, VO_S)

    def open_pair_frame(u_f: int) -> Image.Image:
        """Continuous full-bleed opening across loop (u_f=0..29) -> s01 (u_f=30..106).
        Full-bleed Juno Jupiter cloud bands (PIA22946 interior crop, zero black borders) sweeping smoothly
        while the native-rotating 4K Nov 30 Moon glides across the foreground (high 0-1.5s motion, seamless loop).
        """
        u = u_f / 106.0  # 0.0 -> 1.0 continuously across loop + s01
        bg = crop_box(
            jup_22946,
            cx_px=1395.0 + 210.0 * u,
            cy_px=1520.0 - 135.0 * u,
            ch_px=1520.0 - 95.0 * u,
        ).convert("RGBA")
        m_disc = svs_moon_discs[min(u_f, len(svs_moon_discs) - 1)]
        mx = int(round(520.0 - 150.0 * u))
        my = int(round(930.0 - 165.0 * u))
        bg.alpha_composite(m_disc, (mx, my))
        return lift_if_dark(bg.convert("RGB"))

    def s08_sky_frame(k: float) -> Image.Image:
        """Pre-dawn twilight horizon (ISS070-E-062746) with waning gibbous Nov 30 Moon and Jupiter 1.05 deg beside it in the sky above Earth's limb."""
        bg = crop_box(
            iss_im,
            cx_px=2420.0 + 420.0 * k,
            cy_px=1560.0 - 110.0 * k,
            ch_px=2180.0 - 90.0 * k,
        ).convert("RGBA")
        mx = int(round(555.0 + 24.0 * k))
        my = int(round(190.0 - 38.0 * k))
        bg.alpha_composite(moon_rise_disc, (mx, my))
        # Brilliant Jupiter shining right beside the Moon (~1.05 deg) in the starry sky above Earth's horizon
        jx = mx - 165
        jy = my + 30
        bg.alpha_composite(jup_beacon_sky, (jx, jy))
        return lift_if_dark(bg.convert("RGB"))

    def plate_at(f_idx: int) -> Image.Image:
        t = f_idx / FPS
        # s01 (frames 0..76, 0.000 - 2.567 s)
        if f_idx < 77:
            return open_pair_frame(f_idx + 30)

        # s02 (frames 77..125, 2.567 - 4.200 s): Nov 30 2026 waning gibbous Moon (SVS 5587 Frame 8001, interior sunlit craters)
        if f_idx < 126:
            k = (f_idx - 77) / 49.0
            return crop_box(moon_8001_rgb, cx_px=1720.0 + 55.0 * k, cy_px=1080.0 - 35.0 * k, ch_px=1340.0 - 45.0 * k)

        # s03 (frames 126..171, 4.200 - 5.733 s): NASA Blue Marble Earth ("If Earth were a grape,")
        if f_idx < 172:
            k = (f_idx - 126) / 46.0
            return crop_box(earth_im, cx_px=1780.0 + 140.0 * k, cy_px=1850.0 - 90.0 * k, ch_px=2360.0 - 120.0 * k)

        # s04 (frames 172..231, 5.733 - 7.733 s): Juno Jupiter Belts & Zones + true 11:1 Earth disc ("Jupiter is a whole basketball.")
        if f_idx < 232:
            k = (f_idx - 172) / 60.0
            bg = crop_box(jup_26077, cx_px=1210.0 + 110.0 * k, cy_px=935.0 - 20.0 * k, ch_px=995.0 - 20.0 * k).convert("RGBA")
            ex = int(round(135.0 + 35.0 * k))
            ey = int(round(1080.0 - 30.0 * k))
            bg.alpha_composite(earth_disc_11x, (ex, ey))
            return lift_if_dark(bg.convert("RGB"))

        # s05 (frames 232..314, 7.733 - 10.500 s): True 40:1 Jupiter-to-Moon diameter comparison over Juno PIA21974
        if f_idx < 315:
            k = (f_idx - 232) / 83.0
            bg = crop_box(jup_21974, cx_px=1840.0 + 160.0 * k, cy_px=735.0 - 15.0 * k, ch_px=1095.0 - 25.0 * k).convert("RGBA")
            mx = int(round(760.0 - 70.0 * k))
            my = int(round(980.0 - 40.0 * k))
            bg.alpha_composite(moon_disc_40x, (mx, my))
            return lift_if_dark(bg.convert("RGB"))

        # s06 (frames 315..409, 10.500 - 13.667 s): Sharp LRO Moon sunlit craters ("yet Jupiter sits 2,000 times farther,")
        if f_idx < 410:
            k = (f_idx - 315) / 95.0
            return crop_box(lro_im, cx_px=775.0 + 60.0 * k, cy_px=810.0 - 45.0 * k, ch_px=1075.0 - 35.0 * k)

        # s07 (frames 410..499, 13.667 - 16.667 s): Apollo 11 curved lunar horizon + distant Jupiter shining in starry space sky + DATA distance bar
        if f_idx < 500:
            k = (f_idx - 410) / 90.0
            bg = crop_box(as11_im, cx_px=960.0 + 70.0 * k, cy_px=635.0 - 30.0 * k, ch_px=1120.0 - 40.0 * k).convert("RGBA")
            jx = int(round(665.0 + 22.0 * k))
            jy = int(round(48.0 - 14.0 * k))
            bg.alpha_composite(jup_beacon_far, (jx, jy))
            return lift_if_dark(bg.convert("RGB"))

        # s08 (frames 500..554, 16.667 - 18.500 s): Pre-dawn twilight horizon ("Look south in the morning sky.")
        if f_idx < 555:
            k = (f_idx - 500) / 55.0
            return s08_sky_frame(k)

        # loop (frames 555..584, 18.500 - 19.500 s): <= 0.25 s (7-frame) crossfade from s08 into s01 pre-roll (u_f = 0..29)
        u_f = f_idx - 555
        preroll = open_pair_frame(u_f)
        if u_f < 7:
            alpha = (u_f + 1) / 8.0
            tail_sky = s08_sky_frame(1.0 + 0.12 * (u_f / 7.0))
            return Image.blend(tail_sky, preroll, alpha)
        return preroll

    raw_video = WORK_DIR / "picture.mp4"
    print(f"3. Encoding {NFRAMES} frames ({TOTAL_S:.3f} s) to picture.mp4...", flush=True)
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

    print("4. Building audio stems (VO, SFX, full-runtime 020 Jupiter Short score bed) and final mix...", flush=True)
    vo_stem = WORK_DIR / "stem_vo.wav"
    sfx_stem = WORK_DIR / "stem_sfx.wav"
    bed_stem = WORK_DIR / "stem_bed.wav"
    vo_src = VO_DIR / "moon_jupiter_2026_11_30_vo_v02.wav"
    bed_src = MUSIC_DIR / "jupiter_no_crust_short_bed_v01.mp3"

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(vo_src),
            "-af", f"aresample={SR},apad=pad_dur={LOOP_S + 0.1:.3f},atrim=0:{TOTAL_S:.3f}",
            "-ac", "2", str(vo_stem),
        ],
        check=True,
    )

    # SFX stem: low rumble under s01 (0.00 s) and s05 40x Jupiter scale reveal (7.73 s),
    # soft whoosh at Frame 0 (0.00 s) and Cut 6 distance reveal (13.67 s),
    # UI tick when DATA distance bar animates in (13.20 s) and hits 754 MILLION KM (15.35 s).
    fc_sfx = (
        f"[1:a]aresample={SR},volume=0.065,atrim=0:2.2,adelay=0|0[r1];"
        f"[2:a]aresample={SR},volume=0.065,atrim=0:2.4,adelay=7733|7733[r2];"
        f"[3:a]aresample={SR},volume=0.085,atrim=0:0.85,adelay=0|0[w1];"
        f"[4:a]aresample={SR},volume=0.085,atrim=0:0.85,adelay=13667|13667[w2];"
        f"[5:a]aresample={SR},volume=0.095,adelay=13200|13200[t1];"
        f"[6:a]aresample={SR},volume=0.095,adelay=15350|15350[t2];"
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

    # Music bed stem: full runtime (0 .. 19.500 s), speech-ducked under VO so sfx_kit.py level and music_gate.py both PASS
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

    stem_name = "owb_dated_2026_11_30_moon_jupiter_v01"
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

    cuts = []
    for i, (shot_id, t0, t1, src_stem, up) in enumerate(SHOT_BOUNDS):
        cuts.append({
            "row": f"moon_jupiter_{i:02d}_{shot_id}",
            "source": src_stem,
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "upscale": round(up, 2),
            "framing": {"offset": 0.0 if shot_id == "loop" else round(100.0 + i * 30.0, 1)},
        })
    (WORK_DIR / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")

    pool_titles = {
        "PIA22946": "NASA JunoCam southern hemisphere Jupiter cloud bands and Great Red Spot photograph",
        "moon.8001": "NASA SVS 5587 30 November 2026 waning gibbous Moon space photograph",
        "GSFC_20171208_Archive_e002130": "NASA Blue Marble east-hemisphere Earth photograph",
        "PIA26077": "NASA JunoCam Jupiter belts and zones cloud tops photograph",
        "code_graphic_moon_jupiter_s05_40x_v01": "Own unlabelled 40-to-1 Jupiter and Moon real-body diameter scale over NASA Juno PIA21974 photograph",
        "as11-44-6667": "NASA Apollo 11 Hasselblad lunar highlands photograph",
        "GSFC_20171208_Archive_e001939": "NASA Lunar Reconnaissance Orbiter Moon disc photograph",
        "iss070e062746": "NASA ISS Expedition 70 pre-dawn Earth twilight limb photograph",
        "PIA22946_loop_preroll": "NASA JunoCam Jupiter and SVS 5587 Moon space footage continued into frame 0",
    }
    pool = [{"id": k, "file": k, "title": v} for k, v in pool_titles.items()]
    (WORK_DIR / "pool.json").write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "stem": stem_name,
        "title": "Why Is Jupiter Beside the Moon on November 30?",
        "hook_caption": "FORTY TIMES WIDER",
        "hook_start_s": 0.0,
        "hook_end_s": 2.0,
        "title_banner_start_s": TITLE_WINDOW[0],
        "title_banner_end_s": TITLE_WINDOW[1],
        "data_overlay_start_s": GFX_WINDOW[0],
        "data_overlay_end_s": GFX_WINDOW[1],
        "vo": str(vo_stem),
        "words_file": str(VO_DIR / "moon_jupiter_2026_11_30_vo_v02_words.json"),
        "vo_s": VO_S,
        "last_word_end_s": words[-1]["end"],
        "spoken": (VO_DIR / "moon_jupiter_2026_11_30_spoken_v01.txt").read_text().strip(),
    }
    for d in (WORK_DIR, EXPORT_DIR):
        (d / f"{stem_name}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    cover_jpg = PACK_DIR / "moon_jupiter_2026_11_30_cover_v01.jpg"
    build_cover_image(jup_22946, moon_8001_rgba, cover_jpg)

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

    # (f) gate_shorts_open.py check (--air-date 2026-11-26)
    gso_res = subprocess.run(
        [
            py, str(MAIN_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final_mp4), "--air-date", "2026-11-26",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "moon_jupiter_2026_11_30_spoken_v01.txt"),
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
            "check", str(final_mp4), "--air-date", "2026-11-26",
            "--vo", str(vo_stem),
            "--script", str(VO_DIR / "moon_jupiter_2026_11_30_spoken_v01.txt"),
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
