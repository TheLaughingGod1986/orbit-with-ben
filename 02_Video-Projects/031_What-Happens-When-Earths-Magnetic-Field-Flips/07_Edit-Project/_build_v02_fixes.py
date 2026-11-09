#!/usr/bin/env python3
"""Build clean v02 replacement plates and composites for 031 (J2387, £0).

Fixes:
1. R01 c1, R15 c2-c3, R39 c1-c2, R50 c1, R53 c1: real graded SVS magnetosphere/solar-wind plates
   with zero synthetic wave/bullseye overlay.
2. R03 c1-c2: honest DSCOVR EPIC Blue Marble Earth (svs_12312) for both cuts; R53 c2: honest ISS
   aurora limb (iss030e078095_aurora_timelapse.mp4), keeping svs_3822 to 4 stretches (<= 5 cap).
3. R25 c1-c4: belts_normal (600 km) on c1, ISS over South America on c2, belts_dip (200 km) on c3,
   and ISS 400 km / HALF THE HEIGHT comparison on c4 over graded moving plates.
4. R32 c1-c2: sourced paleointensity comparison bars from paleo_comparison_graphics.py (TODAY vs
   MILLION-YEAR AVERAGE, 100,000 YEARS, TWICE ITS AVERAGE synced to 334.02 s) composited over a
   graded moving Earth/core background plate + Blue Marble globe.
"""
from __future__ import annotations

import math
import subprocess as sp
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

NAS_EDIT = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project"
)
OUT = NAS_EDIT / "nas_plates_v02"
SVS_ORIG = NAS_EDIT / "svs_moving_v01" / "originals"
HARVEST = NAS_EDIT / "harvest_v01"
DESK = Path("/Users/benjaminoats/_desk")

sys.path.insert(0, str(NAS_EDIT))
from mechanism_graphics import W, H, FPS, WHITE, GOLD, BLUE, ease, label  # noqa: E402

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def run_ffmpeg(args: list[str]) -> None:
    sp.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def make_credit(path: Path, text: str = "NASA", y: int = 1036, size: int = 28) -> None:
    if path.exists():
        return
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_REG, size)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((36 + dx, y + dy), text, font=font, fill=(0, 0, 0, 180))
    draw.text((36, y), text, font=font, fill=(255, 255, 255, 220))
    im.save(path)


def caption_rgba(im: Image.Image, xy: tuple[int, int], text: str, size: int, colour: tuple, t: float, start: float, end: float) -> None:
    if not (start <= t < end):
        return
    opacity = max(0.0, min(1.0, (t - start) / 0.35, (end - t) / 0.35))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    label(ImageDraw.Draw(layer), xy, text, size, colour)
    layer.putalpha(layer.getchannel("A").point(lambda p: round(p * opacity)))
    im.alpha_composite(layer)


def build_r01_r03_r15_r39_r50_r53(nasa_credit: Path) -> None:
    svs3822 = SVS_ORIG / "svs_3822_magfield_left.mp4"
    svs12312 = SVS_ORIG / "svs_12312_epic_earth_timelapse.mp4"
    svs12296 = SVS_ORIG / "svs_12296_earth_interior_cutaway.mp4"
    svs20297 = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
    eur_aurora = DESK / "J2141-aurora-v01" / "europeaurora_iss_20120405.mp4"

    lut_3822 = (
        "lutrgb=r='28+220*pow(val/255,0.45)':g='32+215*pow(val/255,0.45)':b='44+205*pow(val/255,0.45)',"
        "unsharp=5:5:1.0:5:5:0.0"
    )
    lut_20297 = (
        "lutrgb=r='28+220*pow(min(val/160,1),0.70)':g='30+215*pow(min(val/160,1),0.70)':b='42+205*pow(min(val/160,1),0.70)',"
        "unsharp=7:7:1.2:7:7:0.0"
    )

    # 1. R01 c1 (4.60 s): svs_3822 at ss=22.0, cropped to focus on Earth + inner magnetosphere loops
    p_r01a = OUT / "plate_031_r01a_svs_magnetosphere_v02.mp4"
    run_ffmpeg([
        "-ss", "22.0", "-t", "9.20", "-i", str(svs3822),
        "-loop", "1", "-t", "4.60", "-i", str(nasa_credit),
        "-filter_complex",
        f"[0:v]setpts=0.5*PTS,fps=25,crop=1120:630:220:225,scale=1920:1080:flags=lanczos,setsar=1,{lut_3822},trim=0:4.60,setpts=PTS-STARTPTS[bg];"
        "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "115", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r01a),
    ])
    print("Built", p_r01a.name, flush=True)

    # 2. R03 c1-c2 (5.40 s): BOTH cuts honestly from svs_12312 (DSCOVR EPIC rotating Earth)
    p_r03 = OUT / "plate_031_r03_epic_earth_v02.mp4"
    run_ffmpeg([
        "-ss", "16.0", "-t", "8.52", "-i", str(svs12312),
        "-ss", "28.0", "-t", "7.68", "-i", str(svs12312),
        "-loop", "1", "-t", "5.40", "-i", str(nasa_credit),
        "-filter_complex",
        "[0:v]setpts=0.3333*PTS,fps=25,crop=1536:864:192:108,scale=1920:1080:flags=lanczos,setsar=1,"
        "eq=brightness=0.10:contrast=1.18:saturation=1.20:gamma=0.84,"
        "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:2.84,setpts=PTS-STARTPTS[v0];"
        "[1:v]setpts=0.3333*PTS,fps=25,crop=1280:720:320:180,scale=1920:1080:flags=lanczos,setsar=1,"
        "eq=brightness=0.10:contrast=1.20:saturation=1.22:gamma=0.82,"
        "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:2.56,setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[bg];"
        "[bg][2:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "135", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r03),
    ])
    print("Built", p_r03.name, flush=True)

    # 3. R15 c1-c3 (16.92 s): c1 svs_12296, c2-c3 svs_3822 cleanly graded
    p_r15 = OUT / "plate_031_r15_svs_field_lines_v02.mp4"
    run_ffmpeg([
        "-ss", "2.6", "-t", "7.40", "-i", str(svs12296),
        "-ss", "30.0", "-t", "11.28", "-i", str(svs3822),
        "-ss", "42.0", "-t", "11.28", "-i", str(svs3822),
        "-loop", "1", "-t", "16.92", "-i", str(nasa_credit),
        "-filter_complex",
        "[0:v]setpts=0.762*PTS,fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
        "eq=brightness=0.10:contrast=1.14:saturation=1.12:gamma=0.86,"
        "lutrgb=r='max(val,25)':g='max(val,28)':b='max(val,38)',trim=0:5.64,setpts=PTS-STARTPTS[v0];"
        f"[1:v]setpts=0.5*PTS,fps=25,crop=1120:630:220:225,scale=1920:1080:flags=lanczos,setsar=1,{lut_3822},trim=0:5.64,setpts=PTS-STARTPTS[v1];"
        f"[2:v]setpts=0.5*PTS,fps=25,crop=1440:810:120:135,scale=1920:1080:flags=lanczos,setsar=1,{lut_3822},trim=0:5.64,setpts=PTS-STARTPTS[v2];"
        "[v0][v1][v2]concat=n=3:v=1:a=0[bg];"
        "[bg][3:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "423", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r15),
    ])
    print("Built", p_r15.name, flush=True)

    # 4. R39 c1-c2 (11.68 s): svs_20297 cleanly graded (2 angles: wide stream -> closer bow shock)
    p_r39 = OUT / "plate_031_r39_svs_solar_wind_magnetosphere_v02.mp4"
    run_ffmpeg([
        "-ss", "2.0", "-t", "8.76", "-i", str(svs20297),
        "-ss", "6.0", "-t", "8.76", "-i", str(svs20297),
        "-loop", "1", "-t", "11.68", "-i", str(nasa_credit),
        "-filter_complex",
        f"[0:v]setpts=0.6667*PTS,fps=25,crop=3456:1944:0:108,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:5.84,setpts=PTS-STARTPTS[v0];"
        f"[1:v]setpts=0.6667*PTS,fps=25,crop=2400:1350:520:405,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:5.84,setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[bg];"
        "[bg][2:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "292", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r39),
    ])
    print("Built", p_r39.name, flush=True)

    # 5. R50 c1 (4.32 s): svs_20297 cleanly graded
    p_r50a = OUT / "plate_031_r50a_svs_solar_wind_gust_v02.mp4"
    run_ffmpeg([
        "-ss", "8.5", "-t", "6.48", "-i", str(svs20297),
        "-loop", "1", "-t", "4.32", "-i", str(nasa_credit),
        "-filter_complex",
        f"[0:v]setpts=0.6667*PTS,fps=25,crop=2240:1260:640:450,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:4.32,setpts=PTS-STARTPTS[bg];"
        "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "108", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r50a),
    ])
    print("Built", p_r50a.name, flush=True)

    # 6. R53 c1-c2 (10.72 s): c1 svs_3822 (5.40 s) -> c2 ISS glowing green aurora limb (5.32 s, europeaurora_iss_20120405.mp4)
    p_r53 = OUT / "plate_031_r53_svs_glowing_field_lines_v02.mp4"
    run_ffmpeg([
        "-ss", "66.5", "-t", "8.10", "-i", str(svs3822),
        "-ss", "18.0", "-t", "5.32", "-i", str(eur_aurora),
        "-loop", "1", "-t", "10.72", "-i", str(nasa_credit),
        "-filter_complex",
        f"[0:v]setpts=0.6667*PTS,fps=25,crop=960:540:420:270,scale=1920:1080:flags=lanczos,setsar=1,{lut_3822},trim=0:5.40,setpts=PTS-STARTPTS[v0];"
        "[1:v]crop=1024:576:0:64,scale=1920:1080:flags=lanczos,setsar=1,"
        "eq=brightness=0.06:contrast=1.14:saturation=1.18:gamma=0.88,"
        "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',"
        "noise=alls=3:allf=t,fps=25,trim=0:5.32,setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[bg];"
        "[bg][2:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "268", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(p_r53),
    ])
    print("Built", p_r53.name, flush=True)


def build_r25_composite(nasa_credit: Path) -> None:
    """R25 (21.84 s / 546f): c1 (5.48s) belts_normal 600km, c2 (5.48s) ISS HDEV, c3 (5.16s) belts_dip 200km, c4 (5.72s) ISS 400km scale."""
    svs20297 = SVS_ORIG / "svs_20297_van_allen_earth_only.mp4"
    hdev = SVS_ORIG / "hdev_earth_views_orig.mp4"
    lut_20297 = (
        "lutrgb=r='28+220*pow(min(val/160,1),0.70)':g='30+215*pow(min(val/160,1),0.70)':b='42+205*pow(min(val/160,1),0.70)',"
        "unsharp=7:7:1.2:7:7:0.0"
    )
    bg_path = OUT / "_tmp_r25_bg.mp4"
    run_ffmpeg([
        "-ss", "0.5", "-t", "8.22", "-i", str(svs20297),
        "-ss", "128.0", "-t", "5.48", "-i", str(hdev),
        "-ss", "4.0", "-t", "7.74", "-i", str(svs20297),
        "-ss", "8.0", "-t", "8.58", "-i", str(svs20297),
        "-loop", "1", "-t", "21.84", "-i", str(nasa_credit),
        "-filter_complex",
        f"[0:v]setpts=0.6667*PTS,fps=25,crop=2560:1440:420:360,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:5.48,setpts=PTS-STARTPTS[v0];"
        "[1:v]fps=25,scale=1920:1080:flags=lanczos,setsar=1,eq=brightness=0.02:contrast=1.06:saturation=1.08,trim=0:5.48,setpts=PTS-STARTPTS[v1];"
        f"[2:v]setpts=0.6667*PTS,fps=25,crop=2240:1260:580:450,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:5.16,setpts=PTS-STARTPTS[v2];"
        f"[3:v]setpts=0.6667*PTS,fps=25,crop=2560:1440:420:360,scale=1920:1080:flags=lanczos,setsar=1,{lut_20297},trim=0:5.72,setpts=PTS-STARTPTS[v3];"
        "[v0][v1][v2][v3]concat=n=4:v=1:a=0[bg];"
        "[bg][4:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "546", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(bg_path),
    ])

    # Render full 21.84 s RGBA overlay from belt_graphics logic so c1, c3, c4 each have crisp animated ruler + labels
    ov_path = OUT / "_tmp_r25_ov.mov"
    total_frames = 546

    def y_at(km: float) -> int:
        return round(900 - km * 0.8)

    def draw_ruler(d: ImageDraw.ImageDraw, im: Image.Image, t: float, start: float, end: float) -> None:
        x = 1180
        d.line((x, y_at(0), x, y_at(650)), fill=WHITE, width=4)
        for km in (0, 200, 400, 600):
            y = y_at(km)
            d.line((x - 10, y, x + 12, y), fill=WHITE, width=3)
        caption_rgba(im, (1420, 955), "SURFACE · 0 KM", 38, WHITE, t, start, end)

    def draw_marker(d: ImageDraw.ImageDraw, km: float, colour: tuple, dt: float) -> None:
        y = y_at(km)
        d.line((1200, y, 1200 + round(480 * ease(dt / 0.45)), y), fill=colour, width=6)
        d.ellipse((1170, y - 10, 1190, y + 10), fill=colour)

    proc = sp.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", "-c:v", "png", str(ov_path),
    ], stdin=sp.PIPE)
    assert proc.stdin is not None
    for idx in range(total_frames):
        t = idx / float(FPS)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if 0.20 <= t < 5.30:
            dt = t - 0.20
            draw_ruler(d, im, t, 0.20, 5.30)
            draw_marker(d, 600, GOLD, dt)
            caption_rgba(im, (1460, 275), "TRAPPED RADIATION", 48, WHITE, t, 0.20, 5.30)
            caption_rgba(im, (1460, 365), "BEYOND ≈ 600 KM", 48, GOLD, t, 1.20, 5.30)
            a = max(0.0, min(1.0, dt / 0.35, (5.30 - t) / 0.35))
            im.putalpha(im.getchannel("A").point(lambda p: round(p * a)))
        elif 11.10 <= t < 21.60:
            dt = t - 11.10
            draw_ruler(d, im, t, 11.10, 21.60)
            height = 600.0 - 400.0 * ease(dt / 1.80)
            draw_marker(d, height, GOLD, dt)
            caption_rgba(im, (1460, 275), "RADIATION DIPS", 48, WHITE, t, 11.10, 16.12)
            caption_rgba(im, (1460, 795), "≈ 200 KM", 50, GOLD, t, 12.20, 21.60)
            if t >= 16.12:
                draw_marker(d, 400, BLUE, t - 16.12)
                caption_rgba(im, (1460, 510), "ISS ≈ 400 KM", 46, BLUE, t, 16.12, 21.60)
                caption_rgba(im, (1460, 275), "HALF THE HEIGHT", 50, GOLD, t, 16.12, 21.60)
            a = max(0.0, min(1.0, dt / 0.35, (21.60 - t) / 0.35))
            im.putalpha(im.getchannel("A").point(lambda p: round(p * a)))
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Failed encoding R25 overlay")

    dest = OUT / "composite_031_r25_belts_iss_v02.mp4"
    run_ffmpeg([
        "-i", str(bg_path),
        "-i", str(ov_path),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "546", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(dest),
    ])
    bg_path.unlink(missing_ok=True)
    ov_path.unlink(missing_ok=True)
    print("Built", dest.name, flush=True)


def build_r32_paleo_comparison(nasa_credit: Path) -> None:
    """R32 (10.60 s / 265f): paleo_comparison_graphics.py bars composited over graded moving Earth/core cutaway plate (Earth on left, bars on right)."""
    svs12296 = SVS_ORIG / "svs_12296_earth_interior_cutaway.mp4"

    bg_path = OUT / "_tmp_r32_bg.mp4"
    run_ffmpeg([
        "-ss", "1.5", "-t", "5.30", "-i", str(svs12296),
        "-filter_complex",
        "[0:v]setpts=2.0*PTS,fps=25,crop=1280:720:600:180,scale=1920:1080:flags=lanczos,setsar=1,"
        "eq=brightness=0.08:contrast=1.18:saturation=1.16:gamma=0.84,"
        "lutrgb=r='max(val,28)':g='max(val,34)':b='max(val,48)',"
        "noise=alls=3:allf=t,trim=0:10.60,setpts=PTS-STARTPTS,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "265", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(bg_path),
    ])

    ov_path = OUT / "_tmp_r32_ov.mov"
    total_frames = 265
    font_cred = ImageFont.truetype(FONT_REG, 28)
    proc = sp.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", "-c:v", "png", str(ov_path),
    ], stdin=sp.PIPE)
    assert proc.stdin is not None
    # R32 starts at 326.32 s; c1 is 0..5.28 s (mid 2.64 s = 5:29), c2 is 5.28..10.60 s (mid 7.94 s).
    # Exact "twice" word begins at 334.02 s (t = 7.70 s into R32; bar 2 builds at 7.40..7.85 s).
    for idx in range(total_frames):
        t = idx / float(FPS)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)

        # paleo_comparison_graphics.py geometry & bars over right-side clearance (x=1080..1700, completely off the left-side Earth cutaway):
        x, width = 1080, 620
        d.line((x, 420, x, 830), fill=WHITE, width=4)

        # Bar 1 (TODAY / 100,000 YEARS) builds at t=0.45..1.15 s so R32 c1 (5:29, t=2.64 s) shows the full bar
        p = ease((t - 0.45) / 0.70)
        if p > 0:
            d.rounded_rectangle((x, 460, x + max(1, round(width * p)), 515), radius=10, fill=BLUE)
        caption_rgba(im, (1390, 320), "TODAY'S FIELD", 54, GOLD, t, 0.0, 2.20)
        caption_rgba(im, (1390, 320), "100,000 YEARS", 50, GOLD, t, 2.20, 7.40)
        caption_rgba(im, (1390, 555), "TODAY", 44, WHITE, t, 0.60, 10.60)

        # Bar 2 (MILLION-YEAR AVERAGE = 0.5x TODAY) synced to "twice" (334.02 s, t=7.70 s)
        if t >= 7.40:
            q = ease((t - 7.40) / 0.45)
            d.rounded_rectangle((x, 710, x + max(1, round(width * 0.5 * q)), 765), radius=10, fill=GOLD)
            caption_rgba(im, (1390, 320), "TWICE ITS AVERAGE", 50, GOLD, t, 7.40, 10.60)
            caption_rgba(im, (1390, 650), "MILLION-YEAR AVERAGE", 44, WHITE, t, 7.40, 10.60)

        a = max(0.0, min(1.0, t / 0.40, (10.60 - t) / 0.40))
        im.putalpha(im.getchannel("A").point(lambda v: round(v * a)))
        d2 = ImageDraw.Draw(im)
        d2.text((48, 960), "NASA", font=font_cred, fill=(255, 255, 255, 220))
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Failed encoding R32 overlay")

    dest = OUT / "code_graphic_031_r32_paleo_v02.mp4"
    run_ffmpeg([
        "-i", str(bg_path),
        "-i", str(ov_path),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "265", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(dest),
    ])
    bg_path.unlink(missing_ok=True)
    ov_path.unlink(missing_ok=True)
    print("Built", dest.name, flush=True)


def build_r33c_paleo_dip() -> None:
    """R33 c3 (4.16 s / 104f): paleo_dip from core_graphics.py composited over softly blurred moving core plate (zero subject collision, zero seams)."""
    svs12296 = SVS_ORIG / "svs_12296_earth_interior_cutaway.mp4"
    bg_path = OUT / "_tmp_r33c_bg.mp4"
    run_ffmpeg([
        "-ss", "6.5", "-t", "4.16", "-i", str(svs12296),
        "-filter_complex",
        "[0:v]fps=25,crop=1120:630:440:210,scale=1920:1080:flags=lanczos,setsar=1,"
        "gblur=sigma=32,eq=brightness=-0.04:contrast=1.08:saturation=0.90:gamma=0.92,"
        "lutrgb=r='max(val,26)':g='max(val,32)':b='max(val,46)',"
        "noise=alls=3:allf=t,trim=0:4.16,setpts=PTS-STARTPTS,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "104", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(bg_path),
    ])

    ov_path = OUT / "_tmp_r33c_ov.mov"
    total_frames = 104
    font_cred = ImageFont.truetype(FONT_REG, 28)
    proc = sp.Popen([
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", "-c:v", "png", str(ov_path),
    ], stdin=sp.PIPE)
    assert proc.stdin is not None
    for idx in range(total_frames):
        t = idx / float(FPS)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        if t < 1.58:
            level = 0.92
        elif t < 3.44:
            level = 0.92 - 0.84 * ease((t - 1.58) / 1.3)
        else:
            level = 0.08 + 0.84 * ease((t - 3.44) / 0.5)
        x, y, width = 460, 620, 1000
        dr.line((x, y, x + width, y), fill=(180, 198, 218, 255), width=6)
        dr.rounded_rectangle((x, y - 36, x + max(8, int(width * level)), y + 36), radius=16, fill=BLUE)
        mx = x + int(width * level)
        dr.ellipse((mx - 16, y - 16, mx + 16, y + 16), fill=GOLD)
        caption_rgba(im, (960, 280), "TRIED TO FLIP", 56, WHITE, t, 0.2, 1.58)
        caption_rgba(im, (960, 280), "NEARLY TO ZERO", 60, GOLD, t, 1.58, 3.44)
        caption_rgba(im, (960, 280), "SNAPPED BACK", 60, WHITE, t, 3.44, 4.16)
        caption_rgba(im, (960, 820), "LASCHAMP DIP", 48, WHITE, t, 0.3, 4.0)
        dr.text((48, 1012), "NASA", font=font_cred, fill=(255, 255, 255, 220))
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("Failed encoding R33c overlay")

    dest = OUT / "code_graphic_031_r33c_paleo_dip_v02.mp4"
    run_ffmpeg([
        "-i", str(bg_path),
        "-i", str(ov_path),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
        "-map", "[outv]", "-frames:v", "104", "-an",
        "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        str(dest),
    ])
    bg_path.unlink(missing_ok=True)
    ov_path.unlink(missing_ok=True)
    print("Built", dest.name, flush=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    nasa_credit = OUT / "credit_nasa.png"
    make_credit(nasa_credit, "NASA")
    build_r01_r03_r15_r39_r50_r53(nasa_credit)
    build_r25_composite(nasa_credit)
    build_r32_paleo_comparison(nasa_credit)
    build_r33c_paleo_dip()


if __name__ == "__main__":
    main()
