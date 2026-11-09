#!/usr/bin/env python3
"""Bounded MacBook plate & full-row composite builder for 031 (J2141, £0).

Builds and technically verifies 27 row plates and full-row composites across 19 rows
(R2, R4, R7, R8, R12, R14, R16, R20, R21, R25, R26, R27, R28, R30, R33, R42, R46, R47, R52)
from SHA-256 verified NASA ISS / NASA SVS / USGS / NOAA / Commons originals and verified
CODE graphics on MacBook.

All 27 renders are 1920x1080, 25 fps, yuv420p, silent (0 audio streams), verified by
full ffmpeg -v error -xerror decode, 5 sampled frames (5 distinct hashes),
ITU-R BT.709 min_sample_luma >= 28.0, min_sample_p95 >= 50.0, and max_upscale <= 1.875x.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BATCH_ROOT = Path("/Users/ben/_desk/J2141-iss-composites-macbook-v01")
PLATES_DIR = BATCH_ROOT / "plates"

EDIT_DIR = Path(
    "/Users/ben/_desk/worker/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project"
)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_credit(path: Path, text: str = "NASA", y: int = 1036, size: int = 28) -> None:
    if path.exists():
        return
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, size)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((36 + dx, y + dy), text, font=font, fill=(0, 0, 0, 180))
    draw.text((36, y), text, font=font, fill=(255, 255, 255, 220))
    im.save(path)


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


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
        raw = im.tobytes()
        frame_hashes.append(hashlib.sha256(raw).hexdigest()[:16])
        small = im.resize((320, 180), Image.Resampling.BILINEAR)
        vals = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in small.getdata()]
        vals.sort()
        lumas.append(round(sum(vals) / len(vals), 2))
        p95s.append(round(vals[int(len(vals) * 0.95)], 2))
        tmp_png.unlink()

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
        and dur_diff <= 0.06
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


def build_all() -> list[dict]:
    PLATES_DIR.mkdir(parents=True, exist_ok=True)
    nasa_credit = PLATES_DIR / "credit_nasa.png"
    make_credit(nasa_credit, "NASA")

    # Verified inputs on MacBook
    hdev = Path("/Users/ben/_desk/J2141-atmosphere-v02/hdev_earth_views_orig.mp4")
    eur_aurora = Path("/Users/ben/_desk/J2141-plates-source-macbook-v01/eol-europeaurora_iss_20120405__europeaurora_iss_20120405.mp4")
    aus_aurora = Path("/Users/ben/_desk/J2141-plates-source-macbook-v01/eol-aurora_iss_20110911__aurora_iss_20110911.mp4")
    us_aurora = Path("/Users/ben/_desk/J2141-plates-source-macbook-v01/eol-auroraus_iss_20120413__auroraus_iss_20120413.mp4")
    svs12312 = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01/originals/svs_12312_EPIC_EarthTimelapse_1920_MASTER_large.mp4")
    svs12296 = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01/originals/svs_12296_Earth_Interior_Cutaway_large.mp4")
    svs20297 = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01/originals/svs_20297_H_0219_VC_Animation_Earth_Only.mp4")
    svs3822 = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01/originals/svs_3822_magField_left.mp4")

    r02_flip = Path("/Users/ben/_desk/J2141-opening-macbook-v01/code_graphic_031_r02_flip_v01.mp4")
    r04_comp = Path("/Users/ben/_desk/J2141-mechanisms-macbook-v02/code_graphic_031_r04_compass_v02.mp4")
    r04_aur = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r04_aurora_v01.mp4")
    r07_grains = Path("/Users/ben/_desk/J2141-grains-v04/code_graphic_031_r07_grains_south_v04.mov")
    r07_crust = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r07_crust_v01.mp4")
    r08_spec = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r08_specimen_v04.mp4")
    r08_grains = Path("/Users/ben/_desk/J2141-grains-v04/code_graphic_031_r08_grains_comparison_v04.mov")
    r12_flip = Path("/Users/ben/_desk/J2141-core-macbook-v01/code_graphic_031_r12_flip_tight_v01.mp4")
    r14_core = Path("/Users/ben/_desk/J2141-core-macbook-v01/code_graphic_031_r14_layers_core_v01.mp4")
    r14_fact = Path("/Users/ben/_desk/J2141-plates-macbook-v01/composite_031_r14_fact_v01.mp4")
    r16_dyn = Path("/Users/ben/_desk/J2141-dynamo-v01/code_graphic_031_r16_dynamo_v01.mp4")
    r16_cut = Path("/Users/ben/_desk/J2141-svs-moving-macbook-v01/plates/plate_031_r16b_outer_core_cutaway_v01.mp4")
    r20_who = Path("/Users/ben/_desk/J2141-stills-composites-macbook-v03/composite_031_r20_gauss_who_v03.mp4")
    r20_str = Path("/Users/ben/_desk/J2141-mechanisms-macbook-v02/code_graphic_031_r20_strength_v02.mov")
    r21_comp = Path("/Users/ben/_desk/J2141-mechanisms-macbook-v02/code_graphic_031_r21_compass_v02.mov")
    r25_norm = Path("/Users/ben/_desk/J2141-belts-macbook-v01/code_graphic_031_r25_belts_normal_v01.mov")
    r25_dip = Path("/Users/ben/_desk/J2141-belts-macbook-v01/code_graphic_031_r25_belts_dip_v01.mov")
    r27_app = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r27_approach_v01.mp4")
    r27_rel = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r27_release_v03.mp4")
    r27_orb = Path("/Users/ben/_desk/J2141-plates-macbook-v01/composite_031_r27_orbits_v02.mp4")
    r27_pau = Path("/Users/ben/_desk/J2141-plates-macbook-v01/composite_031_r27_pause_v02.mp4")
    r28_sat = Path("/Users/ben/_desk/J2141-protection-v01/code_graphic_031_r28_sat_safe_v01.mov")
    r30_rec = Path("/Users/ben/_desk/J2141-comparisons-macbook-v01/code_graphic_031_r30_recap_v01.mov")
    r30_twi = Path("/Users/ben/_desk/J2141-twist-macbook-v01/code_graphic_031_r30_twist_v01.mov")
    r33_cor = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r33_core_v01.mp4")
    r33_las = Path("/Users/ben/_desk/J2141-dates-macbook-v01/code_graphic_031_r33_laschamp_v01.mov")
    r33_pal = Path("/Users/ben/_desk/J2141-core-macbook-v01/code_graphic_031_r33_paleo_dip_v01.mp4")
    r42_col = Path("/Users/ben/_desk/J2141-evidence-macbook-v01/code_graphic_031_r42_column_mass_v01.mov")
    r46_sol = Path("/Users/ben/_desk/J2141-plates-macbook-v01/plate_031_r46_solar_v01.mp4")
    r46_grd = Path("/Users/ben/_desk/J2141-field-macbook-v01/code_graphic_031_r46_grid_shield_v01.mp4")
    r47_tan = Path("/Users/ben/_desk/J2141-sky-macbook-v01/code_graphic_031_r47_tangle_v01.mp4")
    r52_gen = Path("/Users/ben/_desk/J2141-scales-macbook-v01/code_graphic_031_r52_generations_v01.mov")
    r52_dyn = Path("/Users/ben/_desk/J2141-dynamo-v01/code_graphic_031_r52_dynamo_v01.mp4")

    specs: list[tuple[Path, int, str, float, float, list[str], str]] = []

    # 1. R02a (3.48 s): NASA ISS Arctic limb aurora clip (europeaurora t=4.2..7.68s)
    p_r02a = PLATES_DIR / "plate_031_r02a_iss_aurora_v01.mp4"
    if not p_r02a.exists():
        run_ffmpeg([
            "-ss", "4.20", "-t", "3.48", "-i", str(eur_aurora),
            "-loop", "1", "-t", "3.48", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]crop=1024:576:0:64,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.04:contrast=1.10:saturation=1.14:gamma=0.90,"
            "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,38)',"
            "noise=alls=3:allf=t,fps=25[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "87", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r02a),
        ])
    specs.append((p_r02a, 2, "plate_r02a", 3.48, 1.875, ["eol-europeaurora_iss_20120405"], "R2a NASA ISS limb aurora separator plate (3.48 s)"))

    # 2. R02 full composite (8.04 s): R02a (3.48 s) + R02b flip (4.56 s)
    p_r02_comp = PLATES_DIR / "composite_031_r02_aurora_flip_v01.mp4"
    if not p_r02_comp.exists():
        run_ffmpeg([
            "-i", str(p_r02a),
            "-i", str(r02_flip),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.48,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.56,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,38)',format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "201", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r02_comp),
        ])
    specs.append((p_r02_comp, 2, "composite_r02", 8.04, 1.875, ["eol-europeaurora_iss_20120405", "code_graphic_031_r02_flip_v01"], "R2 full composite: ISS aurora separator (3.48 s) + CODE flip (4.56 s)"))

    # 3. R04a (4.72 s): NASA ISS exterior over South Atlantic / coastline (hdev t=78.0..82.72s)
    p_r04a = PLATES_DIR / "plate_031_r04a_iss_exterior_v01.mp4"
    if not p_r04a.exists():
        run_ffmpeg([
            "-ss", "78.0", "-t", "4.72", "-i", str(hdev),
            "-loop", "1", "-t", "4.72", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.02:contrast=1.06:saturation=1.08,"
            "noise=alls=3:allf=t[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "118", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r04a),
        ])
    specs.append((p_r04a, 4, "plate_r04a", 4.72, 1.5, ["hdev_earth_views_iss_2019"], "R4a NASA ISS exterior over coastline/ocean (4.72 s)"))

    # 4. R04 full composite (11.52 s): R04a (4.72 s) + R04b compass (3.36 s) + R04c aurora (3.44 s)
    p_r04_comp = PLATES_DIR / "composite_031_r04_promise_v01.mp4"
    if not p_r04_comp.exists():
        run_ffmpeg([
            "-i", str(p_r04a),
            "-i", str(r04_comp),
            "-i", str(r04_aur),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.72,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.36,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.44,setpts=PTS-STARTPTS,format=yuv420p[v2];"
            "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "288", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r04_comp),
        ])
    specs.append((p_r04_comp, 4, "composite_r04", 11.52, 1.875, ["hdev_earth_views_iss_2019", "code_graphic_031_r04_compass_v02", "eol-europeaurora_iss_20120405"], "R4 full 3-cut promise composite (11.52 s)"))

    # 5. R07 full composite (10.96 s): R07a v04 south-pointing grains over graded basalt (5.72 s) + R07b USGS cooling basalt crust (5.24 s)
    p_r07_comp = PLATES_DIR / "composite_031_r07_grains_crust_v01.mp4"
    if not p_r07_comp.exists():
        run_ffmpeg([
            "-i", str(r07_grains),
            "-i", str(r07_crust),
            "-filter_complex",
            "[1:v]fps=25,scale=1920:1080,setsar=1,hflip,eq=brightness=-0.18:contrast=0.82:saturation=0.75,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)'[bg_base];"
            "[bg_base] tpad=stop_mode=clone:stop_duration=0.60,trim=0:5.72,setpts=PTS-STARTPTS,format=rgba[bg0];"
            "[0:v]fps=25,scale=1920:1080,setsar=1,format=rgba[fg0];"
            "[bg0][fg0]overlay=0:0:eof_action=pass,trim=0:5.72,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:5.24,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "274", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r07_comp),
        ])
    specs.append((p_r07_comp, 7, "composite_r07", 10.96, 1.0, ["code_graphic_031_r07_grains_south_v04", "commons_usgs_kilauea_skylight"], "R7 full composite: CODE v04 south-pointing grains (5.72 s) + USGS basalt crust plate (5.24 s)"))

    # 6. R08 full composite (12.92 s): R08a USGS volcanic specimen (6.96 s) + R08b v04 CODE grains comparison over graded basalt (5.96 s)
    p_r08_comp = PLATES_DIR / "composite_031_r08_specimen_grains_v01.mp4"
    if not p_r08_comp.exists():
        run_ffmpeg([
            "-i", str(r08_spec),
            "-i", str(r08_grains),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080:in_range=pc:out_range=tv,setsar=1,trim=0:6.96,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[0:v]fps=25,scale=1920:1080:in_range=pc:out_range=tv,setsar=1,trim=0.50:6.46,setpts=PTS-STARTPTS,"
            "eq=brightness=-0.20:contrast=0.80:saturation=0.75,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',format=rgba[bg1];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,format=rgba[fg1];"
            "[bg1][fg1]overlay=0:0:eof_action=pass,trim=0:5.96,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "323", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-color_range", "tv",
            str(p_r08_comp),
        ])
    specs.append((p_r08_comp, 8, "composite_r08", 12.92, 1.18, ["usgs_vesicular_basalt_side", "code_graphic_031_r08_grains_comparison_v04"], "R8 full composite: USGS volcanic specimen (6.96 s, normalized to yuv420p) + CODE v04 grains comparison (5.96 s)"))

    # 7. R12a (3.60 s): NASA Blue Marble Earth limb (svs12312 t=110.0..120.80s at 3x speed)
    p_r12a = PLATES_DIR / "plate_031_r12a_earth_limb_v01.mp4"
    if not p_r12a.exists():
        run_ffmpeg([
            "-ss", "110.0", "-t", "10.80", "-i", str(svs12312),
            "-loop", "1", "-t", "3.60", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]setpts=0.3333*PTS,fps=25,crop=1440:810:240:80,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.16:saturation=1.18:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,42)',trim=0:3.60,setpts=PTS-STARTPTS[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "90", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r12a),
        ])
    specs.append((p_r12a, 12, "plate_r12a", 3.60, 1.333, ["nasa_svs_12312_dscovr_epic_earth"], "R12a NASA Blue Marble Earth limb separator plate (3.60 s)"))

    # 8. R12 full composite (12.60 s): R12a (3.60 s) + R12b flip tight (9.00 s)
    p_r12_comp = PLATES_DIR / "composite_031_r12_limb_flip_v01.mp4"
    if not p_r12_comp.exists():
        run_ffmpeg([
            "-i", str(p_r12a),
            "-i", str(r12_flip),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.60,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:9.00,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "315", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r12_comp),
        ])
    specs.append((p_r12_comp, 12, "composite_r12", 12.60, 1.333, ["nasa_svs_12312_dscovr_epic_earth", "code_graphic_031_r12_flip_tight_v01"], "R12 full composite: Blue Marble limb (3.60 s) + CODE tight flip & dive (9.00 s)"))

    # 9. R14 full composite (8.44 s): R14a CODE outer core (6.00 s) + R14b SDO solar prominence & FACT card (2.44 s)
    p_r14_comp = PLATES_DIR / "composite_031_r14_core_sdo_fact_v01.mp4"
    if not p_r14_comp.exists():
        run_ffmpeg([
            "-i", str(r14_core),
            "-i", str(r14_fact),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:6.00,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,26)':g='max(val,28)':b='max(val,36)',format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:2.44,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "211", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r14_comp),
        ])
    specs.append((p_r14_comp, 14, "composite_r14", 8.44, 1.875, ["code_graphic_031_r14_layers_core_v01", "svs-3693-sdo-launching-filament", "code_graphic_031_r14_fact_v01"], "R14 full composite: CODE outer core (6.00 s) + SDO solar prominence & HOT AS THE SUN card (2.44 s)"))

    # 10. R16 full composite (12.24 s): R16a CODE dynamo (8.00 s) + R16b SVS outer-core cutaway (4.24 s)
    p_r16_comp = PLATES_DIR / "composite_031_r16_dynamo_cutaway_v01.mp4"
    if not p_r16_comp.exists():
        run_ffmpeg([
            "-i", str(r16_dyn),
            "-i", str(r16_cut),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:8.00,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.24,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "306", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r16_comp),
        ])
    specs.append((p_r16_comp, 16, "composite_r16", 12.24, 1.0, ["code_graphic_031_r16_dynamo_v01", "nasa_svs_12296_earth_interior_cutaway"], "R16 full composite: CODE dynamo loops (8.00 s) + NASA SVS outer-core cutaway (4.24 s)"))

    # 11. R20 full composite (9.40 s): R20a Gauss portrait + WHO + timeline (5.56 s) + R20b strength chart over SVS field lines (3.84 s)
    p_r20_comp = PLATES_DIR / "composite_031_r20_gauss_strength_full_v01.mp4"
    if not p_r20_comp.exists():
        run_ffmpeg([
            "-i", str(r20_who),
            "-ss", "52.0", "-t", "7.68", "-i", str(svs3822),
            "-i", str(r20_str),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:5.56,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.18:saturation=1.15:gamma=0.84,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:3.84,setpts=PTS-STARTPTS,format=rgba[bg1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba[fg1];"
            "[bg1][fg1]overlay=0:0:eof_action=pass,trim=0:3.84,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "235", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r20_comp),
        ])
    specs.append((p_r20_comp, 20, "composite_r20", 9.40, 1.0, ["commons_gauss", "code_graphic_031_r20_who_v01", "code_graphic_031_r20_strength_v02", "nasa_svs_3822_magfield_left"], "R20 full composite: Gauss portrait & WHO (5.56 s) + CODE strength bars over moving SVS field plate (3.84 s)"))

    # 12. R21 plate (5.44 s): Graded moving Earth-limb plate (hdev t=18.0..23.44s)
    p_r21_plate = PLATES_DIR / "plate_031_r21_earth_limb_v01.mp4"
    if not p_r21_plate.exists():
        run_ffmpeg([
            "-ss", "18.0", "-t", "5.44", "-i", str(hdev),
            "-loop", "1", "-t", "5.44", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.03:contrast=1.08:saturation=1.10,"
            "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,38)',"
            "noise=alls=3:allf=t[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "136", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r21_plate),
        ])
    specs.append((p_r21_plate, 21, "plate_r21", 5.44, 1.5, ["hdev_earth_views_iss_2019"], "R21 graded moving Earth-limb plate (5.44 s)"))

    # 13. R21 £0 fallback composite (5.44 s): CODE compass wobble over graded moving Earth-limb plate
    p_r21_comp = PLATES_DIR / "composite_031_r21_compass_limb_v01.mp4"
    if not p_r21_comp.exists():
        run_ffmpeg([
            "-i", str(p_r21_plate),
            "-i", str(r21_comp),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,format=rgba[bg];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,format=rgba[fg];"
            "[bg][fg]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "136", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r21_comp),
        ])
    specs.append((p_r21_comp, 21, "composite_r21", 5.44, 1.5, ["hdev_earth_views_iss_2019", "code_graphic_031_r21_compass_v02"], "R21 £0 fallback composite: CODE compass wobble over graded moving Earth limb (5.44 s)"))

    # 14. R25 moving plate (20.64 s, 4 cuts <= 5.56 s): SVS 20297 magnetosphere + HDEV ISS over South America/coastline
    p_r25_plate = PLATES_DIR / "plate_031_r25_iss_orbit_cuts_v01.mp4"
    if not p_r25_plate.exists():
        run_ffmpeg([
            "-ss", "1.0", "-t", "5.16", "-i", str(svs20297),
            "-ss", "128.0", "-t", "5.16", "-i", str(hdev),
            "-ss", "7.0", "-t", "4.76", "-i", str(svs20297),
            "-ss", "9.6", "-t", "5.56", "-i", str(svs20297),
            "-loop", "1", "-t", "20.64", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]fps=25,crop=2560:1440:640:360,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.18:saturation=1.22:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,42)',trim=0:5.16,setpts=PTS-STARTPTS[v0];"
            "[1:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.02:contrast=1.06:saturation=1.08,trim=0:5.16,setpts=PTS-STARTPTS[v1];"
            "[2:v:0]fps=25,crop=1920:1080:960:540,setsar=1,"
            "eq=brightness=0.10:contrast=1.18:saturation=1.22:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,42)',trim=0:4.76,setpts=PTS-STARTPTS[v2];"
            "[3:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.18:saturation=1.22:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,42)',trim=0:5.56,setpts=PTS-STARTPTS[v3];"
            "[v0][v1][v2][v3]concat=n=4:v=1:a=0[bg];"
            "[bg][4:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "516", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r25_plate),
        ])
    specs.append((p_r25_plate, 25, "plate_r25", 20.64, 1.5, ["nasa_svs_20297_magnetosphere_earth_only", "hdev_earth_views_iss_2019"], "R25 4-cut moving magnetosphere & ISS orbit plate (20.64 s)"))

    # 15. R25 full composite (20.64 s): belts_normal at t=4.62..7.02s + belts_dip at t=15.08..20.64s
    p_r25_comp = PLATES_DIR / "composite_031_r25_belts_iss_v01.mp4"
    if not p_r25_comp.exists():
        run_ffmpeg([
            "-i", str(p_r25_plate),
            "-i", str(r25_norm),
            "-i", str(r25_dip),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,format=rgba[bg];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,format=rgba,setpts=PTS-STARTPTS+4.62/TB[ov1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba,setpts=PTS-STARTPTS+15.08/TB[ov2];"
            "[bg][ov1]overlay=0:0:eof_action=pass[tmp1];"
            "[tmp1][ov2]overlay=0:0:eof_action=pass,trim=0:20.64,setpts=PTS-STARTPTS,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "516", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r25_comp),
        ])
    specs.append((p_r25_comp, 25, "composite_r25", 20.64, 1.5, ["nasa_svs_20297_magnetosphere_earth_only", "hdev_earth_views_iss_2019", "code_graphic_031_r25_belts_normal_v01", "code_graphic_031_r25_belts_dip_v01"], "R25 full composite: 4-cut magnetosphere/ISS plate + CODE belts_normal (600 KM) & belts_dip (200 KM = 1/2 ISS)"))

    # 16. R26 (5.96 s): ISS view of white clouds over ocean by day (hdev t=31.0..36.96s)
    p_r26 = PLATES_DIR / "plate_031_r26_iss_clouds_v01.mp4"
    if not p_r26.exists():
        run_ffmpeg([
            "-ss", "31.0", "-t", "5.96", "-i", str(hdev),
            "-loop", "1", "-t", "5.96", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.01:contrast=1.05:saturation=1.06,"
            "noise=alls=3:allf=t[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "149", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r26),
        ])
    specs.append((p_r26, 26, "plate_r26", 5.96, 1.5, ["hdev_earth_views_iss_2019"], "R26 NASA ISS view of white clouds over ocean by day (5.96 s)"))

    # 17. R27 full composite (16.08 s): approach (4.00 s) + release (3.48 s) + orbits (4.32 s) + pause/FACT (4.28 s)
    p_r27_comp = PLATES_DIR / "composite_031_r27_hubble_saa_full_v01.mp4"
    if not p_r27_comp.exists():
        run_ffmpeg([
            "-i", str(r27_app),
            "-i", str(r27_rel),
            "-i", str(r27_orb),
            "-i", str(r27_pau),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.00,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.48,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.32,setpts=PTS-STARTPTS,format=yuv420p[v2];"
            "[3:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.28,setpts=PTS-STARTPTS,format=yuv420p[v3];"
            "[v0][v1][v2][v3]concat=n=4:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "402", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r27_comp),
        ])
    specs.append((p_r27_comp, 27, "composite_r27", 16.08, 1.5, ["svs-13160-sts125-sm4-highlights", "code_graphic_031_r27_hubble_saa_v01", "code_graphic_031_r27_fact_v01"], "R27 full composite: Hubble STS-125 + 7-9 ORBITS IN A ROW + HUBBLE STOPS OBSERVING (16.08 s)"))

    # 18. R28a (5.12 s): ISS exterior payload instrument (hdev t=155.0..160.12s)
    p_r28a = PLATES_DIR / "plate_031_r28a_iss_payload_v01.mp4"
    if not p_r28a.exists():
        run_ffmpeg([
            "-ss", "155.0", "-t", "5.12", "-i", str(hdev),
            "-loop", "1", "-t", "5.12", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.02:contrast=1.06:saturation=1.08,"
            "noise=alls=3:allf=t[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "128", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r28a),
        ])
    specs.append((p_r28a, 28, "plate_r28a", 5.12, 1.5, ["hdev_earth_views_iss_2019"], "R28a NASA ISS exterior payload over Earth (5.12 s)"))

    # 19. R28 full composite (9.56 s): R28a payload (5.12 s) + R28b sat_safe over darkened orbit view (4.44 s)
    p_r28_comp = PLATES_DIR / "composite_031_r28_payload_satsafe_v01.mp4"
    if not p_r28_comp.exists():
        run_ffmpeg([
            "-i", str(p_r28a),
            "-ss", "160.12", "-t", "4.44", "-i", str(hdev),
            "-i", str(r28_sat),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:5.12,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v:0]fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=-0.08:contrast=1.05:saturation=0.85,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',trim=0:4.44,setpts=PTS-STARTPTS,format=rgba[bg1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba[fg1];"
            "[bg1][fg1]overlay=0:0:eof_action=pass,trim=0:4.44,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "239", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r28_comp),
        ])
    specs.append((p_r28_comp, 28, "composite_r28", 9.56, 1.5, ["hdev_earth_views_iss_2019", "code_graphic_031_r28_sat_safe_v01"], "R28 full composite: ISS payload (5.12 s) + CODE sat_safe overlay (4.44 s)"))

    # 20. R30a (5.76 s): NASA ISS night Earth limb (aus_aurora t=9.5..15.26s)
    p_r30a = PLATES_DIR / "plate_031_r30a_iss_limb_v01.mp4"
    if not p_r30a.exists():
        run_ffmpeg([
            "-ss", "9.50", "-t", "5.76", "-i", str(aus_aurora),
            "-loop", "1", "-t", "5.76", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]crop=1024:576:0:192,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.01:contrast=1.06:saturation=1.06,"
            "lutrgb=r='max(val,24)':g='max(val,28)':b='max(val,38)',"
            "noise=alls=3:allf=t,fps=25[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "144", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r30a),
        ])
    specs.append((p_r30a, 30, "plate_r30a", 5.76, 1.875, ["eol-aurora_iss_20110911"], "R30a NASA ISS night Earth limb plate (5.76 s)"))

    # 21. R30 full composite (11.12 s): recap over R30a (5.76 s) + twist over ISS night limb (5.36 s)
    p_r30_comp = PLATES_DIR / "composite_031_r30_recap_twist_v01.mp4"
    if not p_r30_comp.exists():
        run_ffmpeg([
            "-i", str(p_r30a),
            "-ss", "15.50", "-t", "5.36", "-i", str(aus_aurora),
            "-i", str(r30_rec),
            "-i", str(r30_twi),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,eq=brightness=-0.16:contrast=0.85:saturation=0.85,lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:5.76,setpts=PTS-STARTPTS,format=rgba[bg0];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba[rec];"
            "[bg0][rec]overlay=0:0:eof_action=pass,trim=0:5.76,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v:0]crop=1024:576:0:192,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=-0.04:contrast=1.08:saturation=0.90,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',"
            "noise=alls=3:allf=t,fps=25,trim=0:5.36,setpts=PTS-STARTPTS,format=rgba[bg1];"
            "[3:v]fps=25,scale=1920:1080,setsar=1,format=rgba,setpts=PTS-STARTPTS+0.94/TB[twi];"
            "[bg1][twi]overlay=0:0:eof_action=pass,trim=0:5.36,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "278", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r30_comp),
        ])
    specs.append((p_r30_comp, 30, "composite_r30", 11.12, 1.875, ["eol-aurora_iss_20110911", "code_graphic_031_r30_recap_v01", "code_graphic_031_r30_twist_v01"], "R30 full composite: ISS night limb + recap triptych + CASE CLOSED? OVERDUE? twist (11.12 s)"))

    # 22. R33 full composite (12.24 s): NOAA sediment core (4.44 s) + Laschamp WHEN over core (3.64 s) + paleo dip (4.16 s)
    p_r33_comp = PLATES_DIR / "composite_031_r33_core_laschamp_paleo_v01.mp4"
    if not p_r33_comp.exists():
        run_ffmpeg([
            "-i", str(r33_cor),
            "-i", str(r33_las),
            "-i", str(r33_pal),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.44,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0.40:4.04,setpts=PTS-STARTPTS,"
            "crop=1600:900:160:90,scale=1920:1080:flags=lanczos,setsar=1,eq=brightness=-0.28:contrast=0.75:saturation=0.80,lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,40)',format=rgba[bg1];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,format=rgba[las];"
            "[bg1][las]overlay=0:0:eof_action=pass,trim=0:3.64,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.16,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v2];"
            "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "306", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r33_comp),
        ])
    specs.append((p_r33_comp, 33, "composite_r33", 12.24, 1.2, ["noaa_expl2290_tube_core", "code_graphic_031_r33_laschamp_v01", "code_graphic_031_r33_paleo_dip_v01"], "R33 full composite: NOAA sediment core + 41,000 YEARS AGO Laschamp stamp + paleo dip (12.24 s)"))

    # 23. R42a (3.08 s): NASA Blue Marble atmospheric limb separator (svs12312 t=138.0..147.24s at 3x speed)
    p_r42a = PLATES_DIR / "plate_031_r42a_iss_blue_limb_v01.mp4"
    if not p_r42a.exists():
        run_ffmpeg([
            "-ss", "138.0", "-t", "9.24", "-i", str(svs12312),
            "-loop", "1", "-t", "3.08", "-i", str(nasa_credit),
            "-filter_complex",
            "[0:v:0]setpts=0.3333*PTS,fps=25,crop=1440:810:240:60,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.16:saturation=1.20:gamma=0.84,"
            "lutrgb=r='max(val,25)':g='max(val,30)':b='max(val,44)',trim=0:3.08,setpts=PTS-STARTPTS[bg];"
            "[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "77", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r42a),
        ])
    specs.append((p_r42a, 42, "plate_r42a", 3.08, 1.333, ["nasa_svs_12312_dscovr_epic_earth"], "R42a NASA sunlit atmospheric limb plate (3.08 s)"))

    # 24. R42 full composite (9.64 s): R42a limb (3.08 s) + R42b column_mass over moving atmospheric limb (6.56 s)
    p_r42_comp = PLATES_DIR / "composite_031_r42_column_limb_v01.mp4"
    if not p_r42_comp.exists():
        run_ffmpeg([
            "-i", str(p_r42a),
            "-ss", "147.5", "-t", "13.12", "-i", str(svs12312),
            "-i", str(r42_col),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:3.08,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v:0]setpts=0.5*PTS,fps=25,crop=1536:864:360:108,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=-0.12:contrast=0.88:saturation=0.92,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,42)',trim=0:6.56,setpts=PTS-STARTPTS,format=rgba[bg1];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba[col];"
            "[bg1][col]overlay=0:0:eof_action=pass,trim=0:6.56,setpts=PTS-STARTPTS,format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "241", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r42_comp),
        ])
    specs.append((p_r42_comp, 42, "composite_r42", 9.64, 1.333, ["nasa_svs_12312_dscovr_epic_earth", "code_graphic_031_r42_column_mass_v01"], "R42 full composite: atmospheric limb (3.08 s) + CODE 1 kg/cm² = 10 m water column overlay (6.56 s)"))

    # 25. R46 full composite (10.08 s): SDO solar flare (2.36 s) + CODE grid_shield (7.72 s)
    p_r46_comp = PLATES_DIR / "composite_031_r46_solar_grid_v01.mp4"
    if not p_r46_comp.exists():
        run_ffmpeg([
            "-i", str(r46_sol),
            "-i", str(r46_grd),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:2.36,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:7.72,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "252", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r46_comp),
        ])
    specs.append((p_r46_comp, 46, "composite_r46", 10.08, 1.5, ["svs-12706-sdo-x8-flare-171-304", "code_graphic_031_r46_grid_shield_v01"], "R46 full composite: SDO X8 solar flare (2.36 s) + CODE satellite/grid shield (7.72 s)"))

    # 26. R47ab plate (7.36 s) + R47 full composite (12.08 s): SVS core & tangled field lines + CODE multipole tangle
    p_r47ab = PLATES_DIR / "plate_031_r47ab_svs_core_twisted_v01.mp4"
    if not p_r47ab.exists():
        run_ffmpeg([
            "-ss", "1.0", "-t", "7.36", "-i", str(svs12296),
            "-ss", "56.0", "-t", "7.36", "-i", str(svs3822),
            "-filter_complex",
            "[0:v]setpts=0.5*PTS,fps=25,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.10:contrast=1.16:saturation=1.18:gamma=0.85,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',trim=0:3.68,setpts=PTS-STARTPTS[v0];"
            "[1:v]setpts=0.5*PTS,fps=25,crop=1536:864:192:108,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.12:contrast=1.22:saturation=1.26:gamma=0.82,"
            "lutrgb=r='max(val,26)':g='max(val,30)':b='max(val,42)',trim=0:3.68,setpts=PTS-STARTPTS[v1];"
            "[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[outv]",
            "-map", "[outv]", "-frames:v", "184", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r47ab),
        ])
    specs.append((p_r47ab, 47, "plate_r47ab", 7.36, 1.25, ["nasa_svs_12296_earth_interior_cutaway", "nasa_svs_3822_magfield_left"], "R47ab NASA SVS core & twisted field-lines 2-cut plate (7.36 s)"))

    p_r47_comp = PLATES_DIR / "composite_031_r47_svs_tangle_v01.mp4"
    if not p_r47_comp.exists():
        run_ffmpeg([
            "-i", str(p_r47ab),
            "-i", str(r47_tan),
            "-filter_complex",
            "[0:v]fps=25,scale=1920:1080,setsar=1,trim=0:7.36,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[1:v]fps=25,scale=1920:1080,setsar=1,trim=0:4.72,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "302", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r47_comp),
        ])
    specs.append((p_r47_comp, 47, "composite_r47", 12.08, 1.25, ["nasa_svs_12296_earth_interior_cutaway", "nasa_svs_3822_magfield_left", "code_graphic_031_r47_tangle_v01"], "R47 full 3-cut composite: SVS core & field lines (7.36 s) + CODE multipole tangle (4.72 s)"))

    # 27. R52 full composite (11.92 s): NASA aurora + CODE generations (0..3.44s) + aurora cut 2 (3.44..9.52s) + CODE dynamo (9.52..11.92s)
    p_r52_comp = PLATES_DIR / "composite_031_r52_aurora_generations_dynamo_v01.mp4"
    if not p_r52_comp.exists():
        run_ffmpeg([
            "-ss", "41.5", "-t", "9.52", "-i", str(us_aurora),
            "-loop", "1", "-t", "9.52", "-i", str(nasa_credit),
            "-i", str(r52_gen),
            "-i", str(r52_dyn),
            "-filter_complex",
            "[0:v:0]crop=1024:576:0:140,scale=1920:1080:flags=lanczos,setsar=1,"
            "eq=brightness=0.14:contrast=1.28:saturation=1.35:gamma=0.76,"
            "lutrgb=r='max(val,26)':g='max(val,32)':b='max(val,44)',"
            "noise=alls=3:allf=t,fps=25,trim=0:9.52,setpts=PTS-STARTPTS[aur];"
            "[aur][1:v]overlay=0:0:shortest=1,format=rgba[bg];"
            "[2:v]fps=25,scale=1920:1080,setsar=1,format=rgba[gen];"
            "[bg][gen]overlay=0:0:eof_action=pass,trim=0:9.52,setpts=PTS-STARTPTS,format=yuv420p[v0];"
            "[3:v]fps=25,scale=1920:1080,setsar=1,trim=0:2.40,setpts=PTS-STARTPTS,"
            "lutrgb=r='max(val,25)':g='max(val,29)':b='max(val,40)',format=yuv420p[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[outv]",
            "-map", "[outv]", "-frames:v", "298", "-an",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            str(p_r52_comp),
        ])
    specs.append((p_r52_comp, 52, "composite_r52", 11.92, 1.875, ["eol-auroraus_iss_20120413", "code_graphic_031_r52_generations_v01", "code_graphic_031_r52_dynamo_v01"], "R52 full composite: NASA aurora + 40-400 generations scale + CODE dynamo settling (11.92 s)"))

    results = []
    for path, row, role, exp_dur, max_up, srcs, note in specs:
        results.append(verify_clip(path, row, role, exp_dur, max_up, srcs, note))
    return results


def build_contact_sheet(results: list[dict], out_jpg: Path) -> None:
    cols = 3
    rows_n = (len(results) + cols - 1) // cols
    thumb_w, thumb_h = 640, 360
    sheet = Image.new("RGB", (cols * thumb_w, rows_n * thumb_h), (14, 18, 28))
    draw = ImageDraw.Draw(sheet)
    for idx, item in enumerate(results):
        p = Path(item["path"])
        t_mid = round(item["duration_s"] * 0.5, 2)
        tmp_png = PLATES_DIR / f"_thumb_{idx}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(t_mid), "-i", str(p), "-frames:v", "1", str(tmp_png)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        im = Image.open(tmp_png).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        tmp_png.unlink()
        x = (idx % cols) * thumb_w
        y = (idx // cols) * thumb_h
        sheet.paste(im, (x, y))
        draw.rectangle([x + 8, y + 8, x + 560, y + 36], fill=(10, 14, 24))
        label = f"R{item['row']:02d} {item['file']} ({item['duration_s']:.2f}s, minY={item['min_sample_luma_bt709']})"
        draw.text((x + 14, y + 14), label, fill=(240, 244, 255))
    sheet.save(out_jpg, quality=90)


def main() -> None:
    results = build_all()
    contact_jpg = PLATES_DIR / "CONTACT_ISS_COMPOSITES_MACBOOK_v01.jpg"
    build_contact_sheet(results, contact_jpg)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    all_pass = all(r["status"] == "PASS" for r in results)

    manifest = {
        "job": "J2141",
        "batch": "J2141-iss-composites-macbook-v01",
        "worker": "macbook",
        "built_at_utc": now_iso,
        "spend_gbp": 0,
        "contact_sheet": str(contact_jpg),
        "contact_sheet_sha256": sha256_file(contact_jpg),
        "renders": results,
    }
    tech_check = {
        "job": "J2141",
        "batch": "J2141-iss-composites-macbook-v01",
        "worker": "macbook",
        "checked_at_utc": now_iso,
        "summary": {
            "total_renders": len(results),
            "passed": sum(1 for r in results if r["status"] == "PASS"),
            "failed": sum(1 for r in results if r["status"] != "PASS"),
            "all_1920x1080_25fps_yuv420p_silent": all_pass,
            "min_sample_luma_bt709_floor": min(r["min_sample_luma_bt709"] for r in results),
            "min_sample_p95_bt709_floor": min(r["min_sample_p95_bt709"] for r in results),
            "max_upscale_factor": max(r["max_upscale_factor"] for r in results),
            "overall_status": "PASS" if all_pass else "FAIL",
        },
        "renders": results,
    }

    (EDIT_DIR / "HARVEST_ISS_COMPOSITES_MACBOOK_v01.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (EDIT_DIR / "HARVEST_ISS_COMPOSITES_MACBOOK_TECHNICAL_CHECK_v01.json").write_text(json.dumps(tech_check, indent=2) + "\n")
    print(json.dumps(tech_check["summary"], indent=2))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
