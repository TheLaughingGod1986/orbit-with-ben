#!/usr/bin/env python3
"""Bounded MacBook harvest + verified plate builder for NASA SVS moving visualizations (J2141).

Covers previously empty/unbuilt NASA SVS moving plate rows in SHOT_LIST_v02.md:
- R1a (4.38 s) + R1 full composite (7.70 s): SVS 3822 3D magnetic field lines around turning Earth + R1b compass flip
- R3  (5.16 s): SVS 12312 DSCOVR EPIC rotating Earth (2.60 s) + SVS 3822 magnetosphere push-in (2.56 s)
- R13a (3.24 s) + R13 full composite (8.86 s): SVS 12296 Earth interior cutaway rotation + R13b 2,900 KM depth graphic
- R15 (15.82 s, 3 cuts): SVS 12296 outer-core cutaway (5.28 s) + SVS 3822 southern-to-northern field lines (5.28 s + 5.26 s)
- R16b (4.24 s): SVS 12296 liquid outer-core cutaway motion separating R16 and R17 CODE graphics
- R31 (6.04 s): SVS 12312 DSCOVR EPIC full-disc Earth turning calmly in sunlight
- R39 (10.68 s, 2 cuts): SVS 20297 solar wind streaming past Earth's magnetosphere (wide + native 1080p Earth close-up)
- R50a (3.92 s) + R50 full composite (8.46 s): SVS 20297 solar-wind gust brushing field lines + R50b SHIELD HOLDS graphic
- R53 (9.42 s, 2 cuts): SVS 3822 magnetic field lines glowing softly around Earth in space

All renders are 1920x1080, 25 fps, yuv420p, silent (0 audio streams), verified by full ffmpeg decode,
5 sampled frames (5 distinct hashes), ITU-R BT.709 mean_luma >= 28.0, and max_upscale <= 2.35x.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw

BATCH_ROOT = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01")
ORIG_DIR = BATCH_ROOT / "originals"
PROV_DIR = BATCH_ROOT / "provenance"
PLATES_DIR = BATCH_ROOT / "plates"

EDIT_DIR = Path(
    "/Users/ben/_desk/worker/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def verify_clip(path: Path, expected_duration: float, max_upscale: float) -> dict:
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
    for idx, frac in enumerate(fractions):
        t = max(0.0, min(dur - 0.08, dur * frac))
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
        raw = im.tobytes()
        frame_hashes.append(hashlib.sha256(raw).hexdigest()[:16])
        # Compute ITU-R BT.709 mean luma on downsampled grid for speed & precision
        small = im.resize((320, 180), Image.Resampling.BILINEAR)
        px = small.getdata()
        luma = sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px) / len(px)
        lumas.append(round(luma, 2))
        tmp_png.unlink()

    distinct_hashes = len(set(frame_hashes))
    min_luma = min(lumas)
    mean_luma = round(sum(lumas) / len(lumas), 2)
    dur_diff = abs(info["duration_s"] - expected_duration)

    passed = (
        decode_ok
        and info["width"] == 1920
        and info["height"] == 1080
        and info["pix_fmt"] == "yuv420p"
        and info["r_frame_rate"] == "25/1"
        and info["audio_streams"] == 0
        and dur_diff <= 0.06
        and distinct_hashes == 5
        and min_luma >= 28.0
        and max_upscale <= 2.35
    )
    return {
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
        "min_sample_luma_bt709": min_luma,
        "mean_luma_bt709": mean_luma,
        "max_upscale_factor": round(max_upscale, 3),
        "status": "PASS" if passed else "FAIL",
    }


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def build_all() -> tuple[list[dict], list[dict]]:
    PLATES_DIR.mkdir(parents=True, exist_ok=True)

    svs20297 = ORIG_DIR / "svs_20297_H_0219_VC_Animation_Earth_Only.mp4"
    svs12312 = ORIG_DIR / "svs_12312_EPIC_EarthTimelapse_1920_MASTER_large.mp4"
    svs12296 = ORIG_DIR / "svs_12296_Earth_Interior_Cutaway_large.mp4"
    svs3822 = ORIG_DIR / "svs_3822_magField_left.mp4"

    r01b_code = Path("/Users/ben/_desk/J2141-opening-macbook-v01/code_graphic_031_r01_poledrift_v01.mp4")
    r13_code = Path("/Users/ben/_desk/J2141-depth-v01/code_graphic_031_r13_depth_v01.mov")
    r50b_plate = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r50_aurora_v01.mp4")

    # 1. R1a (4.38 s): SVS 3822 3D magnetic field lines around turning Earth
    p_r01a = PLATES_DIR / "plate_031_r01a_svs_magnetosphere_v01.mp4"
    if not p_r01a.exists():
        run_ffmpeg([
            "-ss", "22.0", "-i", str(svs3822),
            "-vf", (
                "setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.12:contrast=1.22:saturation=1.28:gamma=0.82,"
                "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',"
                "format=yuv420p"
            ),
            "-t", "4.38", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r01a),
        ])

    # 2. R1 full composite (7.70 s): R1a (4.38 s) + R1b (3.32 s)
    p_r01_comp = PLATES_DIR / "composite_031_r01_opening_svs_compass_v01.mp4"
    if not p_r01_comp.exists():
        run_ffmpeg([
            "-i", str(p_r01a),
            "-ss", "0.40", "-t", "3.32", "-i", str(r01b_code),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,trim=0:4.38,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,trim=0:3.32,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-t", "7.70", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r01_comp),
        ])

    # 3. R3 (5.16 s): Cut 1 DSCOVR EPIC rotating Earth (2.60 s) + Cut 2 SVS 3822 magnetosphere push-in (2.56 s)
    p_r03 = PLATES_DIR / "plate_031_r03_epic_magnetosphere_v01.mp4"
    if not p_r03.exists():
        run_ffmpeg([
            "-ss", "16.0", "-t", "7.80", "-i", str(svs12312),
            "-ss", "44.0", "-t", "5.12", "-i", str(svs3822),
            "-filter_complex",
            "[0:v]setpts=0.3333*PTS,fps=25,crop=1536:864:192:108,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.10:contrast=1.16:saturation=1.18:gamma=0.85,"
            "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,40)',trim=0:2.60,setpts=PTS-STARTPTS[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.12:contrast=1.22:saturation=1.25:gamma=0.82,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:2.56,setpts=PTS-STARTPTS[v1];"
            "[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[outv]",
            "-map", "[outv]", "-t", "5.16", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r03),
        ])

    # 4. R13a (3.24 s): SVS 12296 Earth cutaway rotation
    p_r13a = PLATES_DIR / "plate_031_r13a_earth_cutaway_v01.mp4"
    if not p_r13a.exists():
        run_ffmpeg([
            "-ss", "3.0", "-t", "6.48", "-i", str(svs12296),
            "-vf", (
                "setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.10:contrast=1.14:saturation=1.12:gamma=0.86,"
                "lutrgb=r='max(val,25)':g='max(val,28)':b='max(val,38)',"
                "format=yuv420p"
            ),
            "-t", "3.24", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r13a),
        ])

    # 5. R13 full composite (8.86 s): R13a cutaway (3.24 s) + R13b cutaway with 2,900 KM depth overlay (5.62 s)
    p_r13_comp = PLATES_DIR / "composite_031_r13_cutaway_depth_v01.mp4"
    if not p_r13_comp.exists():
        run_ffmpeg([
            "-ss", "1.5", "-t", "8.86", "-i", str(svs12296),
            "-i", str(r13_code),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.10:contrast=1.14:saturation=1.12:gamma=0.86,"
            "lutrgb=r='max(val,25)':g='max(val,28)':b='max(val,38)',format=rgba[bg];"
            "[1:v]fps=25,scale=1920:1080,format=rgba[fg];"
            "[bg][fg]overlay=0:0:enable='gte(t,3.24)',format=yuv420p[outv]",
            "-map", "[outv]", "-t", "8.86", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r13_comp),
        ])

    # 6. R15 (15.82 s, 3 cuts: 5.28s + 5.28s + 5.26s): SVS 12296 cutaway + SVS 3822 field lines (2 angles)
    p_r15 = PLATES_DIR / "plate_031_r15_svs_field_lines_v01.mp4"
    if not p_r15.exists():
        run_ffmpeg([
            "-ss", "2.6", "-t", "7.40", "-i", str(svs12296),
            "-ss", "24.0", "-t", "10.56", "-i", str(svs3822),
            "-ss", "52.0", "-t", "10.52", "-i", str(svs3822),
            "-filter_complex",
            "[0:v]setpts=0.7135*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.10:contrast=1.14:saturation=1.12:gamma=0.86,"
            "lutrgb=r='max(val,25)':g='max(val,28)':b='max(val,38)',trim=0:5.28,setpts=PTS-STARTPTS[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.12:contrast=1.22:saturation=1.28:gamma=0.82,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:5.28,setpts=PTS-STARTPTS[v1];"
            "[2:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.11:contrast=1.20:saturation=1.24:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',trim=0:5.26,setpts=PTS-STARTPTS[v2];"
            "[v0][v1][v2]concat=n=3:v=1:a=0,format=yuv420p[outv]",
            "-map", "[outv]", "-t", "15.82", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r15),
        ])

    # 7. R16b (4.24 s): SVS 12296 outer-core cutaway close-up separating R16 and R17 CODE graphics
    p_r16b = PLATES_DIR / "plate_031_r16b_outer_core_cutaway_v01.mp4"
    if not p_r16b.exists():
        run_ffmpeg([
            "-ss", "3.4", "-t", "6.78", "-i", str(svs12296),
            "-vf", (
                "setpts=0.625*PTS,fps=25,crop=1440:810:240:135,scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.10:contrast=1.15:saturation=1.14:gamma=0.86,"
                "lutrgb=r='max(val,25)':g='max(val,28)':b='max(val,38)',"
                "format=yuv420p"
            ),
            "-t", "4.24", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r16b),
        ])

    # 8. R31 (6.04 s): SVS 12312 DSCOVR EPIC full-disc Earth turning calmly in sunlight
    p_r31 = PLATES_DIR / "plate_031_r31_dscovr_epic_earth_v01.mp4"
    if not p_r31.exists():
        run_ffmpeg([
            "-ss", "135.8", "-t", "12.08", "-i", str(svs12312),
            "-vf", (
                "setpts=0.5*PTS,fps=25,crop=1536:864:192:108,scale=1920:1080:flags=lanczos,"
                "eq=brightness=0.10:contrast=1.16:saturation=1.18:gamma=0.85,"
                "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,40)',"
                "format=yuv420p"
            ),
            "-t", "6.04", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r31),
        ])

    # 9. R39 (10.68 s, 2 cuts: 5.34s + 5.34s): SVS 20297 solar wind streaming past Earth's magnetosphere
    p_r39 = PLATES_DIR / "plate_031_r39_svs_solar_wind_magnetosphere_v01.mp4"
    if not p_r39.exists():
        run_ffmpeg([
            "-ss", "3.8", "-t", "8.01", "-i", str(svs20297),
            "-ss", "4.8", "-t", "8.01", "-i", str(svs20297),
            "-filter_complex",
            "[0:v]setpts=0.6667*PTS,fps=25,crop=3456:1944:0:108,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.08:contrast=1.16:saturation=1.14:gamma=0.85,"
            "lutrgb=r='max(val,34)':g='max(val,30)':b='max(val,38)',trim=0:5.34,setpts=PTS-STARTPTS[v0];"
            "[1:v]setpts=0.6667*PTS,fps=25,crop=1920:1080:1100:540,"
            "eq=brightness=0.10:contrast=1.18:saturation=1.18:gamma=0.83,"
            "lutrgb=r='max(val,34)':g='max(val,30)':b='max(val,38)',trim=0:5.34,setpts=PTS-STARTPTS[v1];"
            "[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[outv]",
            "-map", "[outv]", "-t", "10.68", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r39),
        ])

    # 10. R50a (3.92 s): SVS 20297 solar-wind gust brushing field lines
    p_r50a = PLATES_DIR / "plate_031_r50a_svs_solar_wind_gust_v01.mp4"
    if not p_r50a.exists():
        run_ffmpeg([
            "-ss", "6.2", "-t", "5.88", "-i", str(svs20297),
            "-vf", (
                "setpts=0.6667*PTS,fps=25,crop=1920:1080:1020:540,"
                "eq=brightness=0.10:contrast=1.18:saturation=1.18:gamma=0.83,"
                "lutrgb=r='max(val,34)':g='max(val,30)':b='max(val,38)',"
                "format=yuv420p"
            ),
            "-t", "3.92", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r50a),
        ])

    # 11. R50 full composite (8.46 s): R50a solar-wind gust (3.92 s) + R50b SVS 3822 / aurora shield holds (4.54 s)
    p_r50_comp = PLATES_DIR / "composite_031_r50_gust_shield_holds_v01.mp4"
    if not p_r50_comp.exists():
        run_ffmpeg([
            "-i", str(p_r50a),
            "-ss", "30.0", "-t", "9.08", "-i", str(svs3822),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,trim=0:3.92,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.12:contrast=1.22:saturation=1.28:gamma=0.82,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',"
            "trim=0:4.54,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-t", "8.46", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r50_comp),
        ])

    # 12. R53 (9.42 s, 2 cuts: 4.72s + 4.70s): SVS 3822 magnetic field lines glowing softly around Earth
    p_r53 = PLATES_DIR / "plate_031_r53_svs_glowing_field_lines_v01.mp4"
    if not p_r53.exists():
        run_ffmpeg([
            "-ss", "36.0", "-t", "9.44", "-i", str(svs3822),
            "-ss", "61.0", "-t", "9.40", "-i", str(svs3822),
            "-filter_complex",
            "[0:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.12:contrast=1.22:saturation=1.28:gamma=0.82,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:4.72,setpts=PTS-STARTPTS[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,"
            "eq=brightness=0.11:contrast=1.20:saturation=1.24:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',trim=0:4.70,setpts=PTS-STARTPTS[v1];"
            "[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[outv]",
            "-map", "[outv]", "-t", "9.42", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r53),
        ])

    specs = [
        ("R1a", p_r01a, 4.38, 1.0, ["nasa_svs_3822_magfield_left"], "NASA SVS #3822 3D magnetic field lines around turning Earth (frame 0 opening)"),
        ("R1", p_r01_comp, 7.70, 1.0, ["nasa_svs_3822_magfield_left", "code_graphic_031_r01b_compass_flip_v02"], "Full Row 1 2-cut composite: R1a SVS 3822 magnetosphere (4.38s) + R1b compass flip (3.32s)"),
        ("R3", p_r03, 5.16, 1.25, ["nasa_svs_12312_dscovr_epic_earth", "nasa_svs_3822_magfield_left"], "2-cut Row 3 plate: DSCOVR EPIC rotating Earth (2.60s) + SVS 3822 magnetosphere push-in (2.56s)"),
        ("R13a", p_r13a, 3.24, 1.0, ["nasa_svs_12296_earth_interior_cutaway"], "NASA SVS #12296 Earth interior cutaway rotation separating R12 and R13b CODE graphics"),
        ("R13", p_r13_comp, 8.86, 1.0, ["nasa_svs_12296_earth_interior_cutaway", "code_graphic_031_r13_core_depth_v01"], "Full Row 13 2-cut composite: R13a SVS 12296 Earth cutaway (3.24s) + R13b 2,900 KM depth graphic (5.62s)"),
        ("R15", p_r15, 15.82, 1.0, ["nasa_svs_12296_earth_interior_cutaway", "nasa_svs_3822_magfield_left"], "3-cut Row 15 plate: SVS 12296 core cutaway (5.28s) + SVS 3822 southern-to-northern field lines (5.28s + 5.26s)"),
        ("R16b", p_r16b, 4.24, 1.333, ["nasa_svs_12296_earth_interior_cutaway"], "NASA SVS #12296 outer-core cutaway motion separating R16 and R17 CODE graphics"),
        ("R31", p_r31, 6.04, 1.25, ["nasa_svs_12312_dscovr_epic_earth"], "NASA SVS #12312 DSCOVR EPIC full-disc Earth turning calmly in sunlight"),
        ("R39", p_r39, 10.68, 1.0, ["nasa_svs_20297_magnetosphere_earth_only"], "2-cut Row 39 plate: SVS 20297 solar wind streaming past Earth's magnetosphere (wide + native 1080p close-up)"),
        ("R50a", p_r50a, 3.92, 1.0, ["nasa_svs_20297_magnetosphere_earth_only"], "NASA SVS #20297 solar-wind gust brushing and compressing Earth's field lines"),
        ("R50", p_r50_comp, 8.46, 1.0, ["nasa_svs_20297_magnetosphere_earth_only", "code_graphic_031_r50_shield_holds_v01"], "Full Row 50 2-cut composite: R50a SVS 20297 solar-wind gust (3.92s) + R50b SHIELD HOLDS graphic (4.54s)"),
        ("R53", p_r53, 9.42, 1.0, ["nasa_svs_3822_magfield_left"], "2-cut Row 53 plate: SVS 3822 magnetic field lines glowing softly around Earth in space"),
    ]

    checks = []
    for row_id, path, exp_dur, max_up, sources, desc in specs:
        res = verify_clip(path, exp_dur, max_up)
        res["row"] = row_id
        res["source_ids"] = sources
        res["description"] = desc
        checks.append(res)

    originals_meta = []
    orig_specs = [
        (
            "nasa_svs_20297_magnetosphere_earth_only",
            svs20297,
            "https://svs.gsfc.nasa.gov/20297/",
            "https://svs.gsfc.nasa.gov/vis/a020000/a020200/a020297/H_0219_VC_Animation_Earth_Only.mp4",
            "Magnetospheres of our Solar System (Earth Only 4K master)",
            "NASA's Goddard Space Flight Center / Scientific Visualization Studio (Bailee DesRocher, Genna Duberstein, Eric Christian)",
            ["R39", "R50", "R50a"],
        ),
        (
            "nasa_svs_12312_dscovr_epic_earth",
            svs12312,
            "https://svs.gsfc.nasa.gov/12312/",
            "https://svs.gsfc.nasa.gov/vis/a010000/a012300/a012312/12312_EPIC_EarthTimelapse-1920-MASTER_large.mp4",
            "One Year In The Life of Earth (DSCOVR EPIC 1080p master)",
            "NASA's Goddard Space Flight Center / DSCOVR EPIC Team (Kayvon Sharghi, Joycelyn Thomson Jones, Jay Herman, Adam Szabo, Alexander Marshak)",
            ["R3", "R31"],
        ),
        (
            "nasa_svs_12296_earth_interior_cutaway",
            svs12296,
            "https://svs.gsfc.nasa.gov/12296/",
            "https://svs.gsfc.nasa.gov/vis/a010000/a012200/a012296/Earth_Interior_Cutaway_large.mp4",
            "Earth Interior Cutaway (Crust, Mantle, Liquid Outer Core, Inner Core 1080p animation)",
            "NASA's Goddard Space Flight Center / Conceptual Image Lab (Walt Feimer, Lisa Poje, Chris Smith, Dan Gallagher, John Connerney)",
            ["R13", "R13a", "R15", "R16b"],
        ),
        (
            "nasa_svs_3822_magfield_left",
            svs3822,
            "https://svs.gsfc.nasa.gov/3822/",
            "https://svs.gsfc.nasa.gov/vis/a000000/a003800/a003822/magField_left.mp4",
            "Stereoscopic Magnetic Field Lines (Left-Eye 2D 1080p Master)",
            "NASA's Goddard Space Flight Center Scientific Visualization Studio (Greg Shirah, Tom Bridgman, Michael Starobin)",
            ["R1", "R1a", "R3", "R15", "R53"],
        ),
    ]
    for aid, opath, page_url, dl_url, title, credit, rows in orig_specs:
        pinfo = probe_video(opath)
        originals_meta.append({
            "id": aid,
            "title": title,
            "source_page_url": page_url,
            "download_url": dl_url,
            "local_original_path": str(opath),
            "sha256": sha256_file(opath),
            **pinfo,
            "credit": credit,
            "licence": "Public Domain (17 U.S.C. § 105 / NASA SVS General Usage Notice: SVS visualizations are generally not copyrighted and are available for commercial/educational reuse with NASA SVS credit)",
            "provenance_files": [
                str(PROV_DIR / f"svs_{page_url.strip('/').split('/')[-1]}_api.json"),
                str(PROV_DIR / f"svs_{page_url.strip('/').split('/')[-1]}_page.html"),
                str(PROV_DIR / "svs_help.html"),
                str(PROV_DIR / "nasa_images_and_media.html"),
            ],
            "target_rows": rows,
        })

    return originals_meta, checks


def build_contact_sheet(checks: list[dict], out_jpg: Path) -> None:
    cols = 3
    rows = 4
    tw, th = 480, 270
    pad_y = 34
    canvas = Image.new("RGB", (cols * tw, rows * (th + pad_y)), (14, 16, 22))
    draw = ImageDraw.Draw(canvas)

    for idx, item in enumerate(checks):
        r = idx // cols
        c = idx % cols
        x = c * tw
        y = r * (th + pad_y)
        mid_t = item["duration_s"] * 0.45
        tmp_jpg = PLATES_DIR / f"_thumb_{idx}.jpg"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{mid_t:.2f}",
                "-i",
                item["path"],
                "-frames:v",
                "1",
                "-vf",
                f"scale={tw - 8}:{th - 8}",
                str(tmp_jpg),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        im = Image.open(tmp_jpg)
        canvas.paste(im, (x + 4, y + pad_y - 2))
        label = f"{item['row']} | {item['file']} ({item['duration_s']:.2f}s, Y={item['mean_luma_bt709']}, {item['status']})"
        draw.text((x + 8, y + 8), label[:68], fill=(235, 240, 250))
        tmp_jpg.unlink()

    canvas.save(out_jpg, quality=92)


def main() -> None:
    originals_meta, checks = build_all()
    contact_path = BATCH_ROOT / "CONTACT_SVS_MOVING_MACBOOK_v01.jpg"
    build_contact_sheet(checks, contact_path)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "batch_id": "J2141-svs-moving-macbook-v01",
        "generated_at_utc": now_iso,
        "agent": "macbook",
        "job_id": "J2141",
        "batch_root": str(BATCH_ROOT),
        "contact_sheet": str(contact_path),
        "originals": originals_meta,
        "plates_and_composites": checks,
    }
    tech_check = {
        "batch_id": "J2141-svs-moving-macbook-v01",
        "generated_at_utc": now_iso,
        "all_passed": all(c["status"] == "PASS" for c in checks),
        "total_clips": len(checks),
        "passed_clips": sum(1 for c in checks if c["status"] == "PASS"),
        "checks": checks,
    }

    (EDIT_DIR / "HARVEST_SVS_MOVING_MACBOOK_v01.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (EDIT_DIR / "HARVEST_SVS_MOVING_MACBOOK_TECHNICAL_CHECK_v01.json").write_text(
        json.dumps(tech_check, indent=2) + "\n", encoding="utf-8"
    )
    print(f"All passed: {tech_check['all_passed']} ({tech_check['passed_clips']}/{tech_check['total_clips']})")
    for c in checks:
        print(
            f"  {c['row']:4s} | {c['file']:46s} | dur={c['duration_s']:6.2f}s | "
            f"distinct={c['distinct_sample_frames']} | minY={c['min_sample_luma_bt709']:5.2f} | "
            f"meanY={c['mean_luma_bt709']:5.2f} | upscale={c['max_upscale_factor']}x | {c['status']}"
        )


if __name__ == "__main__":
    main()
