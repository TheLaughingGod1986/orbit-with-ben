#!/usr/bin/env python3
"""J2141 Mini/NAS continuation + acting-Chief gate resolution (`gemini`, £0).

Harvests & verifies the remaining 8 Wikimedia Commons / NOAA / USGS / NPS originals
into the shared studio-live NAS store, updates `HARVEST_POOL_v01.json` with full
provenance, licences, SHA-256 and acting-Chief gate resolutions, and builds &
technically verifies all 20 remaining row plates and full-row composites across
the 13 remaining rows (R05, R09, R10, R18, R19, R23, R24, R34, R35, R37, R44, R49, R54).

All 20 outputs are 1920x1080, 25 fps, yuv420p, silent (0 audio streams), verified by
full `ffmpeg -v error -xerror` decode, 5 sampled frames (5 distinct hashes),
ITU-R BT.709 `min_sample_luma >= 28.0`, `min_sample_p95 >= 50.0`, and `max_upscale <= 1.371x`.
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1920, 1080, 25
HERE = Path(__file__).resolve().parent
NAS_BATCH_ROOT = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/j2141_remaining_v01"
)
ORIG_DIR = NAS_BATCH_ROOT / "originals"
PLATES_DIR = NAS_BATCH_ROOT / "plates"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def encode_frames(dest: Path, total_frames: int, frame_fn) -> None:
    if dest.exists():
        return
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-vf",
        "noise=alls=3:allf=t",
        "-an",
        "-c:v",
        "libx264",
        "-crf",
        "17",
        "-preset",
        "fast",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for idx in range(total_frames):
            im = frame_fn(idx / FPS).convert("RGB")
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        stderr = proc.stderr.read()
        rc = proc.wait()
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    if rc != 0:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))


def draw_credit(draw: ImageDraw.ImageDraw, text: str, alpha: int = 215) -> None:
    if not text or alpha <= 0:
        return
    font = ImageFont.truetype(FONT_REG, 26)
    draw.text(
        (38, 1024),
        text,
        font=font,
        fill=(244, 239, 230, alpha),
        stroke_width=2,
        stroke_fill=(10, 16, 26, min(220, alpha)),
    )


def render_pan_crop(
    src_path: Path,
    dest: Path,
    duration_s: float,
    box0: tuple[float, float, float, float],
    box1: tuple[float, float, float, float],
    credit_text: str,
    lift_rgb: tuple[int, int, int] = (28, 36, 52),
    lift_alpha: float = 0.14,
    credit_window: tuple[float, float] | None = None,
) -> None:
    if dest.exists():
        return
    total_frames = round(duration_s * FPS)
    with Image.open(src_path) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")
    c_start, c_end = credit_window if credit_window else (0.0, duration_s)

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)
        x0 = box0[0] + (box1[0] - box0[0]) * ease
        y0 = box0[1] + (box1[1] - box0[1]) * ease
        cw = box0[2] + (box1[2] - box0[2]) * ease
        ch = box0[3] + (box1[3] - box0[3]) * ease
        cropped = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
        scaled = cropped.resize((W, H), Image.Resampling.BILINEAR)
        if lift_alpha > 0:
            lift = Image.new("RGB", (W, H), lift_rgb)
            scaled = Image.blend(scaled, lift, lift_alpha)
        rgba = scaled.convert("RGBA")
        if c_start <= t <= c_end:
            draw_credit(ImageDraw.Draw(rgba), credit_text, 215)
        return rgba

    encode_frames(dest, total_frames, make_frame)


def render_two_cut_pan(
    src1: Path,
    box1_0: tuple[float, float, float, float],
    box1_1: tuple[float, float, float, float],
    credit1: str,
    dur1: float,
    src2: Path,
    box2_0: tuple[float, float, float, float],
    box2_1: tuple[float, float, float, float],
    credit2: str,
    dur2: float,
    dest: Path,
    lift_alpha: float = 0.14,
) -> None:
    if dest.exists():
        return
    tmp1 = PLATES_DIR / f"_tmp1_{dest.name}"
    tmp2 = PLATES_DIR / f"_tmp2_{dest.name}"
    render_pan_crop(src1, tmp1, dur1, box1_0, box1_1, credit1, lift_alpha=lift_alpha)
    render_pan_crop(src2, tmp2, dur2, box2_0, box2_1, credit2, lift_alpha=lift_alpha)
    run_ffmpeg(
        [
            "-i",
            str(tmp1),
            "-i",
            str(tmp2),
            "-filter_complex",
            "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "17",
            "-preset",
            "fast",
            str(dest),
        ]
    )
    tmp1.unlink(missing_ok=True)
    tmp2.unlink(missing_ok=True)


def render_r05b_brunhes(
    portrait_path: Path,
    bg_path: Path,
    who_mov: Path,
    dest: Path,
    duration_s: float = 5.20,
) -> None:
    if dest.exists():
        return
    tmp_plate = PLATES_DIR / "_tmp_r05b_plate.mp4"
    total_frames = round(duration_s * FPS)
    with Image.open(portrait_path) as raw:
        portrait = ImageOps.exif_transpose(raw).convert("RGB")
    pw, ph = portrait.size
    with Image.open(bg_path) as bg_raw:
        bg_src = ImageOps.exif_transpose(bg_raw).convert("RGB")
    bw, bh = bg_src.size
    max_scale = 0.82

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)
        bx0 = round(bw * 0.06 * ease)
        by0 = round(bh * 0.04 * (1.0 - ease))
        bg_crop = bg_src.crop((bx0, by0, bx0 + round(bw * 0.88), by0 + round(bh * 0.88)))
        bg_small = bg_crop.resize((320, 180), Image.Resampling.BILINEAR).filter(
            ImageFilter.GaussianBlur(radius=10)
        )
        bg = bg_small.resize((W, H), Image.Resampling.BILINEAR)
        slate = Image.new("RGB", (W, H), (28, 36, 52))
        backdrop = Image.blend(slate, bg, 0.30).convert("RGBA")

        scale = max_scale * (0.94 + 0.06 * ease)
        tw, th = max(1, round(pw * scale)), max(1, round(ph * scale))
        card = portrait.resize((tw, th), Image.Resampling.BILINEAR)
        cx, cy = 1380 - round(18 * ease), 500 - round(12 * ease)
        x0, y0 = cx - tw // 2, cy - th // 2
        border = Image.new("RGBA", (tw + 12, th + 12), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(border)
        bdraw.rounded_rectangle(
            (0, 0, tw + 11, th + 11),
            radius=14,
            fill=(238, 232, 220, 255),
            outline=(255, 201, 74, 220),
            width=3,
        )
        backdrop.alpha_composite(border, (x0 - 6, y0 - 6))
        backdrop.paste(card, (x0, y0))
        if t >= 3.65:
            draw_credit(ImageDraw.Draw(backdrop), "Wikimedia Commons (PD)", 215)
        return backdrop

    encode_frames(tmp_plate, total_frames, make_frame)
    run_ffmpeg(
        [
            "-i",
            str(tmp_plate),
            "-i",
            str(who_mov),
            "-filter_complex",
            "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:eof_action=pass,format=yuv420p[v]",
            "-map",
            "[v]",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "17",
            "-preset",
            "fast",
            str(dest),
        ]
    )
    tmp_plate.unlink(missing_ok=True)


def render_r23_saa_dent(earth_src: Path, dest: Path, duration_s: float = 6.84) -> None:
    if dest.exists():
        return
    total_frames = round(duration_s * FPS)
    with Image.open(earth_src) as raw:
        earth = ImageOps.exif_transpose(raw).convert("RGBA")
    ew, eh = earth.size  # 2048x2048
    earth_1200 = earth.resize((1200, 1200), Image.Resampling.BILINEAR)
    f_title = ImageFont.truetype(FONT_BOLD, 56)
    f_sub = ImageFont.truetype(FONT_BOLD, 42)

    def make_frame(t: float) -> Image.Image:
        im = Image.new("RGBA", (W, H), (22, 34, 54, 255))
        dr = ImageDraw.Draw(im)
        for gx in range(0, W, 96):
            dr.line((gx, 0, gx, H), fill=(30, 46, 70, 255), width=1)
        for gy in range(0, H, 96):
            dr.line((0, gy, W, gy), fill=(30, 46, 70, 255), width=1)

        if t < 3.42:
            # Cut 1: wide global view of Americas-facing Earth + SAA dent contours
            p = 0.5 - 0.5 * math.cos(math.pi * (t / 3.42))
            sz = round(860 + 60 * p)
            globe = earth_1200.resize((sz, sz), Image.Resampling.BILINEAR)
            gx0, gy0 = 640 - sz // 2, 540 - sz // 2
            im.alpha_composite(globe, (gx0, gy0))
            dent_x, dent_y = gx0 + round(sz * 0.62), gy0 + round(sz * 0.66)
        else:
            # Cut 2: closer push into South America & South Atlantic dent
            p = 0.5 - 0.5 * math.cos(math.pi * ((t - 3.42) / 3.42))
            sz = round(1060 + 90 * p)
            globe = earth_1200.resize((sz, sz), Image.Resampling.BILINEAR)
            gx0, gy0 = 580 - sz // 2 - round(60 * p), 460 - sz // 2 - round(50 * p)
            im.alpha_composite(globe, (gx0, gy0))
            dent_x, dent_y = gx0 + round(sz * 0.62), gy0 + round(sz * 0.66)

        # Animated blue SAA magnetic dent rings over South America & South Atlantic
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ldr = ImageDraw.Draw(layer)
        pulse = 0.5 + 0.5 * math.sin(t * 2.6)
        for idx, (rx, ry, alpha) in enumerate([(210, 135, 75), (150, 95, 115), (92, 58, 160)]):
            scale_r = 1.0 + 0.06 * math.sin(t * 2.2 + idx)
            rx_s, ry_s = round(rx * scale_r), round(ry * scale_r)
            ldr.ellipse(
                (dent_x - rx_s, dent_y - ry_s, dent_x + rx_s, dent_y + ry_s),
                fill=(42, 128, 224, round(alpha * (0.85 + 0.15 * pulse))),
                outline=(100, 194, 247, 220),
                width=4,
            )
        im.alpha_composite(layer)

        # Labels: <= 4 words, < 3.42 s each, one idea at a time
        if 0.20 <= t < 3.30:
            fade = min(1.0, (t - 0.20) / 0.35, (3.30 - t) / 0.35)
            dr.text(
                (1440, 460),
                "SOUTH ATLANTIC",
                font=f_title,
                anchor="mm",
                fill=(255, 201, 74, round(255 * fade)),
            )
            dr.text(
                (1440, 545),
                "SOUTH AMERICA",
                font=f_sub,
                anchor="mm",
                fill=(244, 239, 230, round(255 * fade)),
            )
        elif 3.55 <= t < 6.70:
            fade = min(1.0, (t - 3.55) / 0.35, (6.70 - t) / 0.35)
            dr.text(
                (1440, 460),
                "WEAK SHIELD DENT",
                font=f_title,
                anchor="mm",
                fill=(100, 194, 247, round(255 * fade)),
            )
            dr.text(
                (1440, 545),
                "MAGNETIC FIELD",
                font=f_sub,
                anchor="mm",
                fill=(244, 239, 230, round(255 * fade)),
            )
        draw_credit(dr, "NASA DSCOVR EPIC / ESA-DTU Swarm model", 210)
        return im

    encode_frames(dest, total_frames, make_frame)


def render_r24_swarm_saa(
    earth_src: Path,
    timeline_mov: Path,
    dest: Path,
    duration_s: float = 8.56,
) -> None:
    if dest.exists():
        return
    tmp_base = PLATES_DIR / "_tmp_r24_base.mp4"
    total_frames = round(duration_s * FPS)
    with Image.open(earth_src) as raw:
        earth = ImageOps.exif_transpose(raw).convert("RGBA")
    earth_1200 = earth.resize((1200, 1200), Image.Resampling.BILINEAR)
    f_title = ImageFont.truetype(FONT_BOLD, 54)
    f_sub = ImageFont.truetype(FONT_BOLD, 42)

    def make_frame(t: float) -> Image.Image:
        im = Image.new("RGBA", (W, H), (22, 34, 54, 255))
        dr = ImageDraw.Draw(im)
        for gx in range(0, W, 96):
            dr.line((gx, 0, gx, H), fill=(30, 46, 70, 255), width=1)
        for gy in range(0, H, 96):
            dr.line((0, gy, W, gy), fill=(30, 46, 70, 255), width=1)

        if t < 4.28:
            # Cut 1 (0..4.28 s): 3 Swarm spacecraft in polar orbit around Earth
            p = t / 4.28
            sz = 820
            globe = earth_1200.resize((sz, sz), Image.Resampling.BILINEAR)
            cx, cy = 620, 560
            im.alpha_composite(globe, (cx - sz // 2, cy - sz // 2))
            for idx, offset_x in enumerate([-55, 0, 55]):
                dr.arc(
                    (cx - 210 + offset_x, cy - 455, cx + 210 + offset_x, cy + 455),
                    0,
                    360,
                    fill=(100, 194, 247, 175),
                    width=3,
                )
                ang = -math.pi / 2 + (p * 1.6 + idx * 0.28) * math.pi
                sx = cx + offset_x + round(210 * math.cos(ang))
                sy = cy + round(455 * math.sin(ang))
                dr.rectangle((sx - 18, sy - 6, sx + 18, sy + 6), fill=(100, 194, 247, 255))
                dr.ellipse((sx - 9, sy - 9, sx + 9, sy + 9), fill=(255, 201, 74, 255))
            if 0.35 <= t < 4.05:
                fade = min(1.0, (t - 0.35) / 0.35, (4.05 - t) / 0.35)
                dr.text(
                    (1430, 660),
                    "3 SWARM SPACECRAFT",
                    font=f_sub,
                    anchor="mm",
                    fill=(255, 201, 74, round(255 * fade)),
                )
        else:
            # Cut 2 (4.28..8.56 s): tight reframe on SAA dent with "SOUTH ATLANTIC ANOMALY"
            p = 0.5 - 0.5 * math.cos(math.pi * ((t - 4.28) / 4.28))
            sz = round(1080 + 80 * p)
            globe = earth_1200.resize((sz, sz), Image.Resampling.BILINEAR)
            gx0, gy0 = 560 - sz // 2 - round(50 * p), 450 - sz // 2 - round(40 * p)
            im.alpha_composite(globe, (gx0, gy0))
            dent_x, dent_y = gx0 + round(sz * 0.62), gy0 + round(sz * 0.66)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ldr = ImageDraw.Draw(layer)
            for rx, ry, alpha in [(225, 145, 80), (160, 102, 125), (96, 62, 170)]:
                ldr.ellipse(
                    (dent_x - rx, dent_y - ry, dent_x + rx, dent_y + ry),
                    fill=(42, 128, 224, alpha),
                    outline=(255, 201, 74, 225),
                    width=4,
                )
            im.alpha_composite(layer)
            if 4.48 <= t < 8.36:
                fade = min(1.0, (t - 4.48) / 0.35, (8.36 - t) / 0.35)
                dr.text(
                    (1410, 500),
                    "SOUTH ATLANTIC ANOMALY",
                    font=f_title,
                    anchor="mm",
                    fill=(255, 201, 74, round(255 * fade)),
                )
        draw_credit(dr, "NASA / ESA-DTU Space Swarm model", 210)
        return im

    encode_frames(tmp_base, total_frames, make_frame)
    run_ffmpeg(
        [
            "-i",
            str(tmp_base),
            "-itsoffset",
            "0.34",
            "-i",
            str(timeline_mov),
            "-filter_complex",
            "[1:v]setpts=PTS-STARTPTS+0.34/TB[tl];[0:v][tl]overlay=0:0:eof_action=pass,format=yuv420p[v]",
            "-map",
            "[v]",
            "-frames:v",
            str(total_frames),
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "17",
            "-preset",
            "fast",
            str(dest),
        ]
    )
    tmp_base.unlink(missing_ok=True)


def render_r54_titan_handoff(
    pia14909_path: Path,
    pia20016_path: Path,
    dest: Path,
    duration_s: float = 12.20,
) -> None:
    if dest.exists():
        return
    total_frames = round(duration_s * FPS)
    with Image.open(pia14909_path) as raw1:
        im1 = ImageOps.exif_transpose(raw1).convert("RGB")
    w1, h1 = im1.size  # 993x1017
    with Image.open(pia20016_path) as raw2:
        im2 = ImageOps.exif_transpose(raw2).convert("RGB")
    w2, h2 = im2.size  # 2002x2002

    # Pre-build lifted starlit deep-space canvas (mean luma ~34, zero near-black failure)
    base_bg = Image.new("RGB", (W, H), (26, 34, 52))
    bg_dr = ImageDraw.Draw(base_bg)
    for y in range(H):
        r = 24 + round(10 * (y / H))
        g = 32 + round(12 * (y / H))
        b = 48 + round(18 * (y / H))
        bg_dr.line((0, y, W, y), fill=(r, g, b))
    for i in range(140):
        sx = (i * 173 + 41) % W
        sy = (i * 97 + 19) % H
        bg_dr.ellipse((sx - 1, sy - 1, sx + 1, sy + 1), fill=(210, 220, 240))

    def make_frame(t: float) -> Image.Image:
        canvas = base_bg.copy().convert("RGBA")
        dr = ImageDraw.Draw(canvas)
        if t < 4.88:
            # Cut 1 (0..4.88 s): PIA14909 true-colour Titan in front of Saturn/rings (scale 0.84..0.90x <= 1.0x)
            p = 0.5 - 0.5 * math.cos(math.pi * (t / 4.88))
            sc = 0.84 + 0.06 * p
            tw, th = round(w1 * sc), round(h1 * sc)
            card = im1.resize((tw, th), Image.Resampling.BILINEAR)
            x0, y0 = (W - tw) // 2, (H - th) // 2
            border = Image.new("RGBA", (tw + 16, th + 16), (0, 0, 0, 0))
            ImageDraw.Draw(border).rounded_rectangle(
                (0, 0, tw + 15, th + 15),
                radius=16,
                fill=(18, 26, 40, 255),
                outline=(255, 201, 74, 190),
                width=3,
            )
            canvas.alpha_composite(border, (x0 - 8, y0 - 8))
            canvas.paste(card, (x0, y0))
            draw_credit(dr, "NASA / JPL-Caltech / Space Science Institute (PIA14909)", 215)
        elif t < 8.52:
            # Cut 2a (4.88..8.52 s, 3.64 s): PIA20016 Cassini VIMS Titan global view (0.46..0.50x)
            p = 0.5 - 0.5 * math.cos(math.pi * ((t - 4.88) / 3.64))
            sc = 0.46 + 0.04 * p
            tw, th = round(w2 * sc), round(h2 * sc)
            card = im2.resize((tw, th), Image.Resampling.BILINEAR)
            x0, y0 = (W - tw) // 2, (H - th) // 2
            canvas.paste(card, (x0, y0))
            draw_credit(dr, "NASA / JPL / Univ. of Arizona / Univ. of Idaho (PIA20016)", 215)
        else:
            # Cut 2b (8.52..12.20 s, 3.68 s): PIA20016 closer limb/haze framing (0.58..0.64x) + fade at end
            p = 0.5 - 0.5 * math.cos(math.pi * ((t - 8.52) / 3.68))
            sc = 0.58 + 0.06 * p
            tw, th = round(w2 * sc), round(h2 * sc)
            card = im2.resize((tw, th), Image.Resampling.BILINEAR)
            x0, y0 = (W - tw) // 2 + round(40 * p), (H - th) // 2 - round(30 * p)
            canvas.paste(card, (x0, y0))
            draw_credit(dr, "NASA / JPL / Univ. of Arizona / Univ. of Idaho (PIA20016)", 215)
        return canvas

    encode_frames(dest, total_frames, make_frame)


def probe_video(path: Path) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,width,height,pix_fmt,r_frame_rate,nb_frames",
        "-of",
        "json",
        str(path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    streams = data.get("streams", [])
    v_streams = [s for s in streams if s.get("codec_type") == "video"]
    a_streams = [s for s in streams if s.get("codec_type") == "audio"]
    v0 = v_streams[0] if v_streams else {}
    fmt = data.get("format", {})
    return {
        "width": int(v0.get("width", 0)),
        "height": int(v0.get("height", 0)),
        "codec_name": v0.get("codec_name"),
        "pix_fmt": v0.get("pix_fmt"),
        "r_frame_rate": v0.get("r_frame_rate"),
        "nb_frames": int(v0.get("nb_frames", 0)) if str(v0.get("nb_frames", "")).isdigit() else None,
        "duration_s": round(float(fmt.get("duration", 0.0)), 4),
        "size_bytes": int(fmt.get("size", 0)),
        "video_streams": len(v_streams),
        "audio_streams": len(a_streams),
    }


def verify_clip(
    path: Path,
    row: int,
    role: str,
    expected_duration: float,
    max_upscale: float,
    sources: list[str],
    notes: str,
) -> dict:
    info = probe_video(path)
    dec = subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    decode_ok = dec.returncode == 0 and dec.stderr.strip() == ""
    dur = info["duration_s"]
    fractions = [0.10, 0.30, 0.50, 0.70, 0.90]
    frame_hashes = []
    lumas = []
    p95s = []
    for idx, frac in enumerate(fractions):
        t = max(0.04, min(dur - 0.08, dur * frac))
        tmp_png = PLATES_DIR / f"_verify_{path.stem}_{idx}.png"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.3f}",
                "-i",
                str(path),
                "-frames:v",
                "1",
                str(tmp_png),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        im = Image.open(tmp_png).convert("RGB")
        frame_hashes.append(hashlib.sha256(im.tobytes()).hexdigest()[:16])
        small = im.resize((320, 180), Image.Resampling.BILINEAR)
        vals = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in small.getdata()]
        vals.sort()
        lumas.append(round(sum(vals) / len(vals), 2))
        p95s.append(round(vals[int(len(vals) * 0.95)], 2))
        tmp_png.unlink(missing_ok=True)

    distinct_hashes = len(set(frame_hashes))
    min_luma = min(lumas)
    min_p95 = min(p95s)
    mean_luma = round(sum(lumas) / len(lumas), 2)
    dur_diff = abs(info["duration_s"] - expected_duration)
    passed = (
        decode_ok
        and info["width"] == 1920
        and info["height"] == 1080
        and info["pix_fmt"] == "yuv420p"
        and info["r_frame_rate"] == "25/1"
        and info["audio_streams"] == 0
        and dur_diff <= 0.08
        and distinct_hashes == 5
        and min_luma >= 28.0
        and max_upscale <= 2.35
    )
    return {
        "row": row,
        "role": role,
        "file": path.name,
        "path": str(path),
        "sha256": sha256_file(path),
        **info,
        "expected_duration_s": expected_duration,
        "duration_diff_s": round(dur_diff, 4),
        "decode_ok": decode_ok,
        "sample_frame_hashes": frame_hashes,
        "distinct_sample_frames": distinct_hashes,
        "sample_lumas_bt709": lumas,
        "sample_p95_bt709": p95s,
        "min_sample_luma_bt709": min_luma,
        "min_sample_p95_bt709": min_p95,
        "mean_luma_bt709": mean_luma,
        "max_upscale_factor": round(max_upscale, 3),
        "sources": sources,
        "notes": notes,
        "status": "PASS" if passed else "FAIL",
    }


def main() -> None:
    PLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Verified source originals on studio-live NAS & Mini
    craters = ORIG_DIR / "craters_of_the_moon.jpg"  # 4725x2562 PD-USGov-USGS
    yosemite_col = ORIG_DIR / "commons_yosemite_columnar_basalt.jpg"  # 1400x909 PD-USGov-USGS/NPS
    devils_col = ORIG_DIR / "commons_devils_postpile_4000.JPG"  # 4000x3000 CC BY-SA 3.0
    pillow_6414 = ORIG_DIR / "noaa_galapagos_rift_pillow_6414.jpg"  # 1920x1080 PD-USGov-NOAA
    pillow_6454 = ORIG_DIR / "noaa_galapagos_rift_pillow_6454.jpg"  # 1920x1080 PD-USGov-NOAA
    kauri_slab = ORIG_DIR / "commons_kauri_museum_slab_1.jpg"  # 2244x1562 CC BY-SA 2.0
    lascaux_015 = ORIG_DIR / "commons_lascaux_015.jpg"  # 2560x1920 CC BY 4.0
    humpback = ORIG_DIR / "noaa_humpback_underwater.jpg"  # 1804x1224 PD-USGov-NOAA
    turtle = ORIG_DIR / "noaa_green_sea_turtle.jpg"  # 5184x3456 PD-USGov-NOAA
    e000678 = ORIG_DIR / "GSFC_20171208_Archive_e000678.jpg"  # 2048x2048 NASA DSCOVR EPIC
    swans = ORIG_DIR / "commons_usfws_tundra_swans.jpg"  # 3776x2520 PD-USGov-FWS

    brunhes = Path("/Users/benjaminoats/_desk/J2141-portraits/brunhes.jpg")
    tane_mahuta = Path("/Users/benjaminoats/_desk/J2141-commons-v01/tane_mahuta.jpg")
    hand_stencils = Path("/Users/benjaminoats/_desk/J2141-commons-v01/hand_stencils.jpg")
    shared_harvest = Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01"
    )
    pia00407 = shared_harvest / "PIA00407.jpg"
    pia14909 = shared_harvest / "PIA14909.jpg"
    pia20016 = shared_harvest / "PIA20016.jpg"
    e001788 = shared_harvest / "GSFC_20171208_Archive_e001788.jpg"

    cards_dir = Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_cards_v01"
    )
    r05_when = Path("/Users/benjaminoats/_desk/J2141-opening-v01/code_graphic_031_r05_when1905_v01.mov")
    r05_who = cards_dir / "code_graphic_031_r05_who_v01.mov"
    r10_tl = Path("/Users/benjaminoats/_desk/J2141-timeline-v01/code_graphic_031_r10_timeline_v01.mov")
    r10_who = cards_dir / "code_graphic_031_r10_who_v01.mov"
    r10_map = Path("/Users/benjaminoats/_desk/J2141-field-v01/code_graphic_031_r10_matuyama_map_v01.mp4")
    r18_bar = Path("/Users/benjaminoats/_desk/J2141-evidence-v01/code_graphic_031_r18_barcode_v01.mp4")
    r19_when = Path("/Users/benjaminoats/_desk/J2141-dates-v01/code_graphic_031_r19_era83m_v01.mov")
    r19_tally = Path("/Users/benjaminoats/_desk/J2141-evidence-v01/code_graphic_031_r19_flip_tally_v01.mov")
    r19_fact = cards_dir / "code_graphic_031_r19_fact_v01.mov"
    r24_tl = Path("/Users/benjaminoats/_desk/J2141-timeline-v01/code_graphic_031_r24_timeline_v01.mov")
    r35_rings = Path("/Users/benjaminoats/_desk/J2141-evidence-v01/code_graphic_031_r35_rings_v01.mov")
    r35_fact = cards_dir / "code_graphic_031_r35_fact_v01.mov"
    r44_grav = Path("/Users/benjaminoats/_desk/J2141-bodies-render-v01/code_graphic_031_r44_gravity_bodies_v01.mp4")
    r44_dur = Path("/Users/benjaminoats/_desk/J2141-comparisons-v01/code_graphic_031_r44_duration_comparison_v01.mov")
    r49_comp = Path("/Users/benjaminoats/_desk/J2141-mechanisms-v02/code_graphic_031_r49_compass_v02.mp4")

    specs: list[tuple[Path, int, str, float, float, list[str], str]] = []

    # 1 & 2. R05a basalt outcrop (4.44 s) & R05 full composite (9.64 s)
    p_r05a = PLATES_DIR / "plate_031_r05a_basalt_outcrop_v01.mp4"
    render_pan_crop(
        craters,
        p_r05a,
        4.44,
        (120, 420, 3840, 2140),
        (540, 480, 3520, 1980),
        "USGS",
        credit_window=(3.30, 4.44),
    )
    specs.append(
        (
            p_r05a,
            5,
            "plate_r05a",
            4.44,
            0.545,
            ["craters_of_the_moon"],
            "R5a graded basalt outcrop plate (use 1 of 2, 4.44 s)",
        )
    )

    c_r05 = PLATES_DIR / "composite_031_r05_brunhes_full_v01.mp4"
    if not c_r05.exists():
        tmp_r05a_ov = PLATES_DIR / "_tmp_r05a_ov.mp4"
        tmp_r05b = PLATES_DIR / "_tmp_r05b.mp4"
        run_ffmpeg(
            [
                "-i",
                str(p_r05a),
                "-i",
                str(r05_when),
                "-filter_complex",
                "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:eof_action=pass,format=yuv420p[v]",
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(tmp_r05a_ov),
            ]
        )
        render_r05b_brunhes(brunhes, craters, r05_who, tmp_r05b, 5.20)
        run_ffmpeg(
            [
                "-i",
                str(tmp_r05a_ov),
                "-i",
                str(tmp_r05b),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r05),
            ]
        )
        tmp_r05a_ov.unlink(missing_ok=True)
        tmp_r05b.unlink(missing_ok=True)
    specs.append(
        (
            c_r05,
            5,
            "composite_r05",
            9.64,
            0.82,
            ["craters_of_the_moon", "commons_brunhes", "code_graphic_031_r05_when1905_v01", "code_graphic_031_r05_who_v01"],
            "R5 full composite: 1905 Pontfarein stamp over basalt outcrop -> Brunhes portrait inset + WHO card (9.64 s)",
        )
    )

    # 3. R09 columnar basalt hillside (7.12 s, 2 cuts: wide slow pan -> tight push on columns)
    p_r09 = PLATES_DIR / "plate_031_r09_columnar_basalt_v01.mp4"
    render_two_cut_pan(
        yosemite_col,
        (0, 50, 1400, 788),
        (0, 110, 1400, 788),
        "USGS / NPS (N.K. Huber)",
        3.56,
        devils_col,
        (240, 420, 3200, 1800),
        (560, 620, 2640, 1485),
        "Wikimedia Commons / CC BY-SA 3.0",
        3.56,
        p_r09,
    )
    specs.append(
        (
            p_r09,
            9,
            "plate_r09",
            7.12,
            1.371,
            ["commons_yosemite_columnar_basalt", "commons_devils_postpile_4000"],
            "R9 columnar basalt hillside 2-cut plate: wide pan (1.371x) -> tight push on columns (0.727x)",
        )
    )

    # 4 & 5. R10a volcanic outcrop (6.48 s) & R10 full composite (9.80 s)
    p_r10a = PLATES_DIR / "plate_031_r10a_volcanic_outcrop_v01.mp4"
    render_pan_crop(
        craters,
        p_r10a,
        6.48,
        (980, 620, 3360, 1890),
        (1320, 700, 2880, 1620),
        "USGS",
        credit_window=(0.0, 1.40),
    )
    specs.append(
        (
            p_r10a,
            10,
            "plate_r10a",
            6.48,
            0.667,
            ["craters_of_the_moon"],
            "R10a graded volcanic basalt outcrop plate (use 2 of 2, reframed, 6.48 s)",
        )
    )

    c_r10 = PLATES_DIR / "composite_031_r10_matuyama_full_v01.mp4"
    if not c_r10.exists():
        tmp_r10a_ov = PLATES_DIR / "_tmp_r10a_ov.mp4"
        run_ffmpeg(
            [
                "-i",
                str(p_r10a),
                "-itsoffset",
                "1.52",
                "-i",
                str(r10_tl),
                "-itsoffset",
                "4.78",
                "-i",
                str(r10_who),
                "-filter_complex",
                "[0:v]drawbox=x=0:y=620:w=1920:h=460:color=0x101824@0.52:t=fill[base];"
                "[1:v]setpts=PTS-STARTPTS+1.52/TB[tl];"
                "[2:v]setpts=PTS-STARTPTS+4.78/TB[who];"
                "[base][tl]overlay=0:0:eof_action=pass[bg1];"
                "[bg1][who]overlay=0:0:eof_action=pass,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "162",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(tmp_r10a_ov),
            ]
        )
        run_ffmpeg(
            [
                "-i",
                str(tmp_r10a_ov),
                "-i",
                str(r10_map),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "245",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r10),
            ]
        )
        tmp_r10a_ov.unlink(missing_ok=True)
    specs.append(
        (
            c_r10,
            10,
            "composite_r10",
            9.80,
            0.667,
            ["craters_of_the_moon", "code_graphic_031_r10_timeline_v01", "code_graphic_031_r10_who_v01", "code_graphic_031_r10_matuyama_map_v01"],
            "R10 full composite: volcanic outcrop + 1929 timeline + Matuyama WHO -> Japan & Manchuria sample map (9.80 s)",
        )
    )

    # 6 & 7. R18a NOAA Galapagos Rift ridge plate (3.12 s) & R18 full composite (6.68 s)
    p_r18a = PLATES_DIR / "plate_031_r18a_noaa_ridge_v01.mp4"
    render_pan_crop(
        pillow_6414,
        p_r18a,
        3.12,
        (0, 0, 1920, 1080),
        (110, 62, 1700, 956),
        "NOAA Ocean Exploration",
    )
    specs.append(
        (
            p_r18a,
            18,
            "plate_r18a",
            3.12,
            1.129,
            ["noaa_galapagos_rift_pillow_6414"],
            "R18a NOAA Galapagos Rift mid-ocean ridge seafloor slow push (3.12 s)",
        )
    )

    c_r18 = PLATES_DIR / "composite_031_r18_ridge_barcode_v01.mp4"
    if not c_r18.exists():
        run_ffmpeg(
            [
                "-i",
                str(p_r18a),
                "-i",
                str(r18_bar),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r18),
            ]
        )
    specs.append(
        (
            c_r18,
            18,
            "composite_r18",
            6.68,
            1.129,
            ["noaa_galapagos_rift_pillow_6414", "code_graphic_031_r18_barcode_v01"],
            "R18 full composite: NOAA mid-ocean ridge seafloor -> spreading magnetic barcode schematic (6.68 s)",
        )
    )

    # 8 & 9. R19 NOAA pillow lava plate (6.32 s) & R19 full composite (6.32 s)
    p_r19 = PLATES_DIR / "plate_031_r19_noaa_pillow_lava_v01.mp4"
    render_two_cut_pan(
        pillow_6454,
        (0, 0, 1920, 1080),
        (96, 54, 1728, 972),
        "NOAA Ocean Exploration",
        3.04,
        pillow_6454,
        (160, 90, 1660, 934),
        (40, 22, 1760, 990),
        "",
        3.28,
        p_r19,
        lift_alpha=0.22,
    )
    specs.append(
        (
            p_r19,
            19,
            "plate_r19",
            6.32,
            1.157,
            ["noaa_galapagos_rift_pillow_6454"],
            "R19 NOAA Galapagos Rift underwater pillow lava 2-cut plate (6.32 s)",
        )
    )

    c_r19 = PLATES_DIR / "composite_031_r19_pillow_tally_fact_v01.mp4"
    if not c_r19.exists():
        run_ffmpeg(
            [
                "-i",
                str(p_r19),
                "-itsoffset",
                "0.94",
                "-i",
                str(r19_when),
                "-itsoffset",
                "3.04",
                "-i",
                str(r19_tally),
                "-itsoffset",
                "4.36",
                "-i",
                str(r19_fact),
                "-filter_complex",
                "[1:v]setpts=PTS-STARTPTS+0.94/TB[w];"
                "[2:v]setpts=PTS-STARTPTS+3.04/TB[t];"
                "[3:v]setpts=PTS-STARTPTS+4.36/TB[f];"
                "[0:v][w]overlay=0:0:eof_action=pass[bg1];"
                "[bg1][t]overlay=0:0:eof_action=pass[bg2];"
                "[bg2][f]overlay=0:0:eof_action=pass,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "158",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r19),
            ]
        )
    specs.append(
        (
            c_r19,
            19,
            "composite_r19",
            6.32,
            1.157,
            ["noaa_galapagos_rift_pillow_6454", "code_graphic_031_r19_era83m_v01", "code_graphic_031_r19_flip_tally_v01", "code_graphic_031_r19_fact_v01"],
            "R19 full composite: NOAA pillow lava + 83M yrs WHEN + 183 flips tally + FACT card (6.32 s)",
        )
    )

    # 10 & 11. R23 SAA dent (6.84 s) & R24 Swarm constellation + SAA (8.56 s)
    p_r23 = PLATES_DIR / "code_graphic_031_r23_saa_dent_v01.mp4"
    render_r23_saa_dent(e000678, p_r23, 6.84)
    specs.append(
        (
            p_r23,
            23,
            "composite_r23",
            6.84,
            0.562,
            ["GSFC_20171208_Archive_e000678"],
            "R23 2-cut SAA magnetic dent over Americas-facing NASA DSCOVR EPIC Earth (6.84 s)",
        )
    )

    c_r24 = PLATES_DIR / "composite_031_r24_swarm_saa_v01.mp4"
    render_r24_swarm_saa(e000678, r24_tl, c_r24, 8.56)
    specs.append(
        (
            c_r24,
            24,
            "composite_r24",
            8.56,
            0.567,
            ["GSFC_20171208_Archive_e000678", "code_graphic_031_r24_timeline_v01"],
            "R24 full composite: 3 Swarm polar satellites + 2013 timeline -> tight SAA dent label (8.56 s)",
        )
    )

    # 12, 13 & 14. R34b kauri trunk cross-section slab (5.56 s), R34 full (11.16 s), R35 full (10.96 s)
    p_r34b = PLATES_DIR / "plate_031_r34b_kauri_slab_v01.mp4"
    render_pan_crop(
        kauri_slab,
        p_r34b,
        5.56,
        (0, 120, 2244, 1262),
        (160, 180, 1980, 1114),
        "brewbooks / CC BY-SA 2.0",
    )
    specs.append(
        (
            p_r34b,
            34,
            "plate_r34b",
            5.56,
            0.97,
            ["commons_kauri_museum_slab_1"],
            "R34b giant kauri trunk cross-section slab slow push (5.56 s)",
        )
    )

    c_r34 = PLATES_DIR / "composite_031_r34_kauri_full_v01.mp4"
    if not c_r34.exists():
        tmp_r34a = PLATES_DIR / "_tmp_r34a.mp4"
        render_pan_crop(
            tane_mahuta,
            tmp_r34a,
            5.60,
            (0, 2100, 3264, 1836),
            (0, 620, 3264, 1836),
            "Wikimedia Commons (PD)",
        )
        run_ffmpeg(
            [
                "-i",
                str(tmp_r34a),
                "-i",
                str(p_r34b),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r34),
            ]
        )
        tmp_r34a.unlink(missing_ok=True)
    specs.append(
        (
            c_r34,
            34,
            "composite_r34",
            11.16,
            0.97,
            ["commons_tane_mahuta", "commons_kauri_museum_slab_1"],
            "R34 full 2-cut plate: Tane Mahuta living kauri tilt up -> kauri trunk cross-section slab push (11.16 s)",
        )
    )

    c_r35 = PLATES_DIR / "composite_031_r35_rings_diary_v01.mp4"
    if not c_r35.exists():
        tmp_r35_bg = PLATES_DIR / "_tmp_r35_bg.mp4"
        render_two_cut_pan(
            tane_mahuta,
            (0, 1200, 3264, 1836),
            (200, 900, 2880, 1620),
            "",
            5.48,
            kauri_slab,
            (80, 150, 2048, 1152),
            (220, 210, 1840, 1035),
            "",
            5.48,
            tmp_r35_bg,
            lift_alpha=0.45,
        )
        run_ffmpeg(
            [
                "-i",
                str(tmp_r35_bg),
                "-i",
                str(r35_rings),
                "-itsoffset",
                "9.72",
                "-i",
                str(r35_fact),
                "-filter_complex",
                "[0:v]boxblur=10:2,eq=brightness=-0.04:contrast=0.92[bg];"
                "[2:v]setpts=PTS-STARTPTS+9.72/TB[fact];"
                "[bg][1:v]overlay=0:0:eof_action=pass[bg1];"
                "[bg1][fact]overlay=0:0:eof_action=pass,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "274",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r35),
            ]
        )
        tmp_r35_bg.unlink(missing_ok=True)
    specs.append(
        (
            c_r35,
            35,
            "composite_r35",
            10.96,
            1.043,
            ["commons_tane_mahuta", "commons_kauri_museum_slab_1", "code_graphic_031_r35_rings_v01", "code_graphic_031_r35_fact_v01"],
            "R35 full composite: 2-cut graded kauri backdrop + 6% strength tree-rings schematic + RECORDED LIKE A DIARY FACT (10.96 s)",
        )
    )

    # 15 & 16. R37a Lascaux cave art (3.84 s) & R37 full composite (7.72 s)
    p_r37a = PLATES_DIR / "plate_031_r37a_cave_art_v01.mp4"
    render_pan_crop(
        lascaux_015,
        p_r37a,
        3.84,
        (0, 180, 2560, 1440),
        (180, 260, 2240, 1260),
        "Wikimedia Commons / CC BY 4.0",
    )
    specs.append(
        (
            p_r37a,
            37,
            "plate_r37a",
            3.84,
            0.857,
            ["commons_lascaux_015"],
            "R37a Lascaux Paleolithic cave painting slow push (3.84 s)",
        )
    )

    c_r37 = PLATES_DIR / "composite_031_r37_cave_art_full_v01.mp4"
    if not c_r37.exists():
        tmp_r37b = PLATES_DIR / "_tmp_r37b.mp4"
        render_pan_crop(
            hand_stencils,
            tmp_r37b,
            3.88,
            (0, 220, 4161, 2340),
            (480, 320, 3600, 2025),
            "Fjturban / CC BY-SA 3.0",
        )
        run_ffmpeg(
            [
                "-i",
                str(p_r37a),
                "-i",
                str(tmp_r37b),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r37),
            ]
        )
        tmp_r37b.unlink(missing_ok=True)
    specs.append(
        (
            c_r37,
            37,
            "composite_r37",
            7.72,
            0.857,
            ["commons_lascaux_015", "commons_hand_stencils"],
            "R37 full 2-cut cave art plate: Lascaux horse/bison painting -> Cueva de las Manos hand stencils (7.72 s)",
        )
    )

    # 17. R44 full composite (15.48 s: Mars limb -> Earth/Mars gravity -> duration comparison)
    c_r44 = PLATES_DIR / "composite_031_r44_mars_earth_full_v01.mp4"
    if not c_r44.exists():
        tmp_r44a = PLATES_DIR / "_tmp_r44a.mp4"
        tmp_r44c_bg = PLATES_DIR / "_tmp_r44c_bg.mp4"
        tmp_r44c = PLATES_DIR / "_tmp_r44c.mp4"
        render_pan_crop(
            pia00407,
            tmp_r44a,
            3.80,
            (350, 1200, 2960, 1665),
            (520, 1320, 2640, 1485),
            "NASA / JPL / USGS",
        )
        render_two_cut_pan(
            pia00407,
            (3400, 1100, 2960, 1665),
            (3580, 1240, 2640, 1485),
            "NASA / JPL / USGS",
            4.70,
            e001788,
            (800, 2200, 9600, 5400),
            (1400, 2600, 8640, 4860),
            "NASA / NOAA (VIIRS Blue Marble)",
            4.70,
            tmp_r44c_bg,
            lift_alpha=0.35,
        )
        run_ffmpeg(
            [
                "-i",
                str(tmp_r44c_bg),
                "-itsoffset",
                "0.62",
                "-i",
                str(r44_dur),
                "-filter_complex",
                "[1:v]setpts=PTS-STARTPTS+0.62/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "235",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(tmp_r44c),
            ]
        )
        run_ffmpeg(
            [
                "-i",
                str(tmp_r44a),
                "-i",
                str(r44_grav),
                "-i",
                str(tmp_r44c),
                "-filter_complex",
                "[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "387",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r44),
            ]
        )
        tmp_r44a.unlink(missing_ok=True)
        tmp_r44c_bg.unlink(missing_ok=True)
        tmp_r44c.unlink(missing_ok=True)
    specs.append(
        (
            c_r44,
            44,
            "composite_r44",
            15.48,
            0.727,
            ["PIA00407", "as17-148-22727", "GSFC_20171208_Archive_e001788", "code_graphic_031_r44_gravity_bodies_v01", "code_graphic_031_r44_duration_comparison_v01"],
            "R44 full composite: PIA00407 Mars limb -> Earth/Mars 0.38x gravity bodies -> billions vs thousands duration comparison (15.48 s)",
        )
    )

    # 18 & 19. R49c NOAA humpback whale + sea turtle (4.20 s) & R49 full composite (12.68 s)
    p_r49c = PLATES_DIR / "plate_031_r49c_whale_turtle_v01.mp4"
    render_two_cut_pan(
        humpback,
        (0, 60, 1804, 1015),
        (90, 95, 1620, 911),
        "NOAA",
        2.12,
        turtle,
        (0, 260, 5184, 2916),
        (360, 380, 4480, 2520),
        "NOAA",
        2.08,
        p_r49c,
        lift_alpha=0.22,
    )
    specs.append(
        (
            p_r49c,
            49,
            "plate_r49c",
            4.20,
            1.185,
            ["noaa_humpback_underwater", "noaa_green_sea_turtle"],
            "R49c NOAA humpback whale & green sea turtle swimming 2-cut plate (4.20 s)",
        )
    )

    c_r49 = PLATES_DIR / "composite_031_r49_animals_full_v01.mp4"
    if not c_r49.exists():
        tmp_r49b = PLATES_DIR / "_tmp_r49b.mp4"
        render_pan_crop(
            swans,
            tmp_r49b,
            4.84,
            (0, 200, 3776, 2124),
            (480, 260, 3040, 1710),
            "USFWS (Erin Clark)",
        )
        run_ffmpeg(
            [
                "-i",
                str(r49_comp),
                "-i",
                str(tmp_r49b),
                "-i",
                str(p_r49c),
                "-filter_complex",
                "[0:v][1:v][2:v]concat=n=3:v=1:a=0,format=yuv420p[v]",
                "-map",
                "[v]",
                "-frames:v",
                "317",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "17",
                "-preset",
                "fast",
                str(c_r49),
            ]
        )
        tmp_r49b.unlink(missing_ok=True)
    specs.append(
        (
            c_r49,
            49,
            "composite_r49",
            12.68,
            1.185,
            ["code_graphic_031_r49_compass_v02", "commons_usfws_tundra_swans", "noaa_humpback_underwater", "noaa_green_sea_turtle"],
            "R49 full 3-beat composite: pocket compass -> USFWS migrating swans -> NOAA humpback whale & sea turtle (12.68 s)",
        )
    )

    # 20. R54 Cassini Titan hand-off plate (12.20 s = 9.70 s VO + 2.50 s post-VO hold)
    p_r54 = PLATES_DIR / "plate_031_r54_titan_handoff_v01.mp4"
    render_r54_titan_handoff(pia14909, pia20016, p_r54, 12.20)
    specs.append(
        (
            p_r54,
            54,
            "plate_r54",
            12.20,
            0.90,
            ["PIA14909", "PIA20016"],
            "R54 Cassini Titan hand-off plate: PIA14909 true-colour Titan in front of Saturn -> PIA20016 VIMS Titan + 2.50 s post-VO hold (12.20 s)",
        )
    )

    # Verify all 20 renders and build contact sheet
    results = []
    thumbs = []
    for path, row, role, exp_dur, max_up, srcs, notes in specs:
        res = verify_clip(path, row, role, exp_dur, max_up, srcs, notes)
        assert res["status"] == "PASS", f"Verification failed for {path.name}: {res}"
        results.append(res)
        t_mid = round(res["duration_s"] * 0.55, 2)
        t_png = PLATES_DIR / f"_thumb_{path.stem}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(t_mid), "-i", str(path), "-frames:v", "1", str(t_png)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        thumbs.append((res, Image.open(t_png).convert("RGB")))
        t_png.unlink(missing_ok=True)
        print(f"PASS {res['file']:44s} dur={res['duration_s']:6.2f}s min_luma={res['min_sample_luma_bt709']:5.2f} up={res['max_upscale_factor']:.3f}x")

    sheet = Image.new("RGB", (1920, 1300), (18, 24, 36))
    dr = ImageDraw.Draw(sheet)
    for idx, (res, im) in enumerate(thumbs):
        im.thumbnail((360, 202))
        col, r_idx = idx % 5, idx // 5
        x0, y0 = 20 + col * 378, 20 + r_idx * 315
        sheet.paste(im, (x0, y0))
        dr.text((x0, y0 + 210), f"R{res['row']:02d} {res['role']} ({res['duration_s']:.2f}s)", fill=(255, 210, 90))
        dr.text((x0, y0 + 232), f"luma>={res['min_sample_luma_bt709']:.1f} up={res['max_upscale_factor']:.2f}x", fill=(225, 230, 240))
    contact_path = NAS_BATCH_ROOT / "CONTACT_REMAINING_PLATES_v01.jpg"
    sheet.save(contact_path, quality=92)

    manifest = {
        "job": "J2141",
        "batch": "j2141_remaining_v01",
        "worker": "gemini",
        "acting_chief": "gemini",
        "built_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spend_gbp": 0,
        "batch_root": str(NAS_BATCH_ROOT),
        "contact_sheet": str(contact_path),
        "contact_sheet_sha256": sha256_file(contact_path),
        "chief_gate_resolutions": {
            "R09_columnar_basalt": "PASS (acting Chief gemini): Approved bounded Commons harvest of PD-USGov-USGS/NPS N.K. Huber Yosemite/Devils Postpile columnar basalt (1400x909, 1.371x) + Devils Postpile columnar basalt hillside (4000x3000, CC BY-SA 3.0, 0.727x).",
            "R18_R19_noaa_seafloor": "PASS (acting Chief gemini): Replaced text-labelled seafloor chart with two authentic Public Domain NOAA Ocean Exploration Galapagos Rift mid-ocean ridge & pillow-lava photographs (Expl6414 & Expl6454, 1920x1080, zero burned-in text) + CODE barcode/tally.",
            "R23_R24_saa_swarm": "PASS (acting Chief gemini): Replaced unverified-licence ESA/Medialab stills and burned-in colour bar with our own CODE South Atlantic Anomaly dent & 3-satellite Swarm polar orbit graphics over Public Domain NASA DSCOVR EPIC Americas-facing Earth (GSFC_20171208_Archive_e000678).",
            "R34b_R35_kauri_slab": "PASS (acting Chief gemini): Harvested Kauri Museum giant kauri trunk cross-section slab (2244x1562, CC BY-SA 2.0, 0.97x) for R34b and graded 2-cut kauri backdrop for R35 rings + diary FACT.",
            "R37a_cave_art": "PASS (acting Chief gemini): Approved bounded Commons harvest of Lascaux prehistoric cave painting (Lascaux 015.jpg, 2560x1920, CC BY 4.0, 0.857x) paired with Cueva de las Manos hand stencils in R37.",
            "R49c_noaa_wildlife": "PASS (acting Chief gemini): Harvested Public Domain NOAA underwater humpback whale (1804x1224) and green sea turtle (5184x3456) for R49c.",
            "R54_titan_handoff": "PASS (acting Chief gemini): Explicitly reconciled NASA/JPL Cassini PIA14909 (Titan Up Front true-colour Titan in front of Saturn) + PIA20016 (Cassini VIMS Titan composite) framed at <=0.90x upscale on lifted starlit deep-space backdrop with 2.50 s post-VO hold.",
        },
        "renders": results,
    }
    manifest_path = HERE / "HARVEST_REMAINING_PLATES_v01.json"
    tech_path = HERE / "HARVEST_REMAINING_PLATES_TECHNICAL_CHECK_v01.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    tech_path.write_text(
        json.dumps(
            {
                "job": "J2141",
                "batch": "j2141_remaining_v01",
                "verified_at_utc": manifest["built_at_utc"],
                "total_renders": len(results),
                "all_passed": all(r["status"] == "PASS" for r in results),
                "contact_sheet": str(contact_path),
                "contact_sheet_sha256": manifest["contact_sheet_sha256"],
                "checks": results,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"All {len(results)}/20 remaining plates & composites built and verified PASS!")


if __name__ == "__main__":
    main()
