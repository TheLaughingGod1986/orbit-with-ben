#!/usr/bin/env python3
"""Build all remaining 031 row plates/composites on Mini/NAS from existing local files."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_EDIT = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project")
sys.path.insert(0, str(REPO_EDIT))

from build_stills_and_composites_macbook import (
    render_portrait_inset_plate,
    render_mars_wide_plate,
    render_overlay_composite,
    render_r45_fossil_extinction_composite,
)

NAS_EDIT = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project")
OUT = NAS_EDIT / "nas_plates_v01"
DESK = Path("/Users/benjaminoats/_desk")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


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


def build_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    nas_cards = NAS_EDIT / "code_cards_v01"
    nas_harvest = NAS_EDIT / "harvest_v01"
    nas_orig = NAS_EDIT / "j2141_remaining_v01" / "originals"
    svs_orig = NAS_EDIT / "svs_moving_v01" / "originals"

    nasa_credit = OUT / "credit_nasa.png"
    make_credit(nasa_credit, "NASA")

    # --- Part A: 5 missing renders from build_stills_and_composites_macbook.py ---
    c_r06 = OUT / "composite_031_r06_lava_fact_v03.mp4"
    if not c_r06.exists():
        render_overlay_composite(
            DESK / "J2141-lava-v01" / "plate_031_r06_lava_v01.mp4",
            nas_cards / "code_graphic_031_r06_fact_v01.mov",
            c_r06,
            overlay_offset_s=4.20,
            duration_s=6.68,
        )
        print("Built", c_r06.name, flush=True)

    p_r20 = OUT / "plate_031_r20_gauss_v03.mp4"
    if not p_r20.exists():
        render_portrait_inset_plate(
            DESK / "J2141-portraits" / "gauss.jpg",
            DESK / "J2141-basalt-v01" / "skylight_usgs_flickr.jpg",
            p_r20,
            duration_s=5.56,
            credit_text="C. A. Jensen (1840) / Wikimedia Commons",
            credit_window=(0.00, 1.92),
            max_scale=0.39,
        )
    c_r20 = OUT / "composite_031_r20_gauss_who_v03.mp4"
    if not c_r20.exists():
        render_overlay_composite(
            p_r20,
            nas_cards / "code_graphic_031_r20_who_v01.mov",
            c_r20,
            overlay_offset_s=1.96,
            duration_s=5.56,
        )
        print("Built", c_r20.name, flush=True)

    c_r29 = OUT / "composite_031_r29_saa_when_v03.mp4"
    if not c_r29.exists():
        render_overlay_composite(
            DESK / "J2141-saa-v01" / "code_graphic_031_r29_saa_v01.mp4",
            DESK / "J2141-timeline-v01" / "code_graphic_031_r29_timeline_v01.mov",
            c_r29,
            overlay_offset_s=0.10,
            duration_s=5.12,
        )
        print("Built", c_r29.name, flush=True)

    p_r38 = OUT / "plate_031_r38_mars_wide_v03.mp4"
    if not p_r38.exists():
        render_mars_wide_plate(
            nas_harvest / "PIA00407.jpg",
            p_r38,
            duration_s=4.80,
            credit_text="NASA/JPL/USGS",
        )
        print("Built", p_r38.name, flush=True)

    c_r45 = OUT / "composite_031_r45_fossil_extinction_v03.mp4"
    if not c_r45.exists():
        render_r45_fossil_extinction_composite(
            DESK / "J2141-fossil-v01" / "plate_031_r45_fossil_v01.mp4",
            DESK / "J2141-field-v01" / "code_graphic_031_r45_extinction_check_v01.mov",
            c_r45,
            duration_s=6.60,
            overlay_offset_s=3.16,
        )
        print("Built", c_r45.name, flush=True)

    # --- Part B: 12 SVS moving plates & composites from harvest_svs_moving_macbook_v01.py ---
    svs20297 = svs_orig / "svs_20297_van_allen_earth_only.mp4"
    svs12312 = svs_orig / "svs_12312_epic_earth_timelapse.mp4"
    svs12296 = svs_orig / "svs_12296_earth_interior_cutaway.mp4"
    svs3822 = svs_orig / "svs_3822_magfield_left.mp4"
    hdev = svs_orig / "hdev_earth_views_orig.mp4"

    r01b_code = DESK / "J2141-opening-v01" / "code_graphic_031_r01_poledrift_v01.mp4"
    r13_code = DESK / "J2141-depth-v01" / "code_graphic_031_r13_depth_v01.mov"

    p_r01a = OUT / "plate_031_r01a_svs_magnetosphere_v01.mp4"
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
    p_r01_comp = OUT / "composite_031_r01_opening_svs_compass_v01.mp4"
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
        print("Built", p_r01_comp.name, flush=True)

    p_r03 = OUT / "plate_031_r03_epic_magnetosphere_v01.mp4"
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
        print("Built", p_r03.name, flush=True)

    p_r13a = OUT / "plate_031_r13a_earth_cutaway_v01.mp4"
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
    p_r13_comp = OUT / "composite_031_r13_cutaway_depth_v01.mp4"
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
        print("Built", p_r13_comp.name, flush=True)

    p_r15 = OUT / "plate_031_r15_svs_field_lines_v01.mp4"
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
        print("Built", p_r15.name, flush=True)

    p_r16b = OUT / "plate_031_r16b_outer_core_cutaway_v01.mp4"
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
        print("Built", p_r16b.name, flush=True)

    p_r31 = OUT / "plate_031_r31_dscovr_epic_earth_v01.mp4"
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
        print("Built", p_r31.name, flush=True)

    p_r39 = OUT / "plate_031_r39_svs_solar_wind_magnetosphere_v01.mp4"
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
        print("Built", p_r39.name, flush=True)

    p_r50a = OUT / "plate_031_r50a_svs_solar_wind_gust_v01.mp4"
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
    p_r50_comp = OUT / "composite_031_r50_gust_shield_holds_v01.mp4"
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
        print("Built", p_r50_comp.name, flush=True)

    p_r53 = OUT / "plate_031_r53_svs_glowing_field_lines_v01.mp4"
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
        print("Built", p_r53.name, flush=True)

    # --- Part C: 27 ISS / composite clips from harvest_iss_composites_macbook_v01.py ---
    eur_aurora = DESK / "J2141-aurora-v01" / "europeaurora_iss_20120405.mp4"
    aus_aurora = DESK / "J2141-aurora-v01" / "aurora_iss_20110911.mp4"
    us_aurora = DESK / "J2141-aurora-v01" / "auroraus_iss_20120413.mp4"

    r02_flip = DESK / "J2141-opening-v01" / "code_graphic_031_r02_flip_v01.mp4"
    r04_comp = DESK / "J2141-mechanisms-v02" / "code_graphic_031_r04_compass_v02.mp4"
    r04_aur = DESK / "J2141-aurora-v01" / "plate_031_r04_aurora_v01.mp4"
    r07_grains = DESK / "J2141-grains-v04" / "code_graphic_031_r07_grains_south_v04.mov"
    r07_crust = DESK / "J2141-basalt-v01" / "plate_031_r07_crust_v01.mp4"
    r08_spec = DESK / "J2141-hand-sample-v01" / "plate_031_r08_specimen_v04.mp4"
    r08_grains = DESK / "J2141-grains-v04" / "code_graphic_031_r08_grains_comparison_v04.mov"
    r12_flip = DESK / "J2141-core-v01" / "code_graphic_031_r12_flip_tight_v01.mp4"
    r14_core = DESK / "J2141-core-v01" / "code_graphic_031_r14_layers_core_v01.mp4"
    r14_fact = DESK / "J2141-solar-v01" / "composite_031_r14_fact_v01.mp4"
    r16_dyn = DESK / "J2141-dynamo-v01" / "code_graphic_031_r16_dynamo_align_v01.mp4"
    r16_cut = p_r16b
    r20_who = c_r20
    r20_str = DESK / "J2141-mechanisms-v02" / "code_graphic_031_r20_strength_v02.mov"
    r21_comp = DESK / "J2141-mechanisms-v02" / "code_graphic_031_r21_compass_v02.mov"
    r25_norm = DESK / "J2141-belts-macbook-v01" / "code_graphic_031_r25_belts_normal_v01.mov"
    r25_dip = DESK / "J2141-belts-macbook-v01" / "code_graphic_031_r25_belts_dip_v01.mov"
    r27_app = DESK / "J2141-hubble-v01" / "plate_031_r27_approach_v01.mp4"
    r27_rel = DESK / "J2141-hubble-v01" / "plate_031_r27_release_v03.mp4"
    r27_orb = DESK / "J2141-r27-composite-v02" / "composite_031_r27_orbits_v02.mp4"
    r27_pau = DESK / "J2141-r27-composite-v02" / "composite_031_r27_pause_v02.mp4"
    r28_sat = DESK / "J2141-saa-v01" / "code_graphic_031_r28_sat_safe_v01.mov"
    r30_rec = DESK / "J2141-comparisons-v01" / "code_graphic_031_r30_recap_v01.mov"
    r30_twi = DESK / "J2141-twist-v01" / "code_graphic_031_r30_twist_v01.mov"
    r33_cor = DESK / "J2141-sediment-v01" / "plate_031_r33_core_v01.mp4"
    r33_las = DESK / "J2141-dates-v01" / "code_graphic_031_r33_laschamp_v01.mov"
    r33_pal = DESK / "J2141-core-v01" / "code_graphic_031_r33_paleo_dip_v01.mp4"
    r42_col = DESK / "J2141-evidence-v01" / "code_graphic_031_r42_column_mass_v01.mov"
    r46_sol = DESK / "J2141-solar-v01" / "plate_031_r46_solar_v01.mp4"
    r46_grd = DESK / "J2141-field-v01" / "code_graphic_031_r46_grid_shield_v01.mp4"
    r47_tan = DESK / "J2141-multipole-v01" / "code_graphic_031_r47_multipole_tangle_v01.mp4"
    r52_gen = DESK / "J2141-scales-v01" / "code_graphic_031_r52_generations_v01.mov"
    r52_dyn = DESK / "J2141-dynamo-v01" / "code_graphic_031_r52_dynamo_settle_v01.mp4"

    p_r02a = OUT / "plate_031_r02a_iss_aurora_v01.mp4"
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
    p_r02_comp = OUT / "composite_031_r02_aurora_flip_v01.mp4"
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
        print("Built", p_r02_comp.name, flush=True)

    p_r04a = OUT / "plate_031_r04a_iss_exterior_v01.mp4"
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
    p_r04_comp = OUT / "composite_031_r04_promise_v01.mp4"
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
        print("Built", p_r04_comp.name, flush=True)

    p_r07_comp = OUT / "composite_031_r07_grains_crust_v01.mp4"
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
        print("Built", p_r07_comp.name, flush=True)

    p_r08_comp = OUT / "composite_031_r08_specimen_grains_v01.mp4"
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
        print("Built", p_r08_comp.name, flush=True)

    p_r12a = OUT / "plate_031_r12a_earth_limb_v01.mp4"
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
    p_r12_comp = OUT / "composite_031_r12_limb_flip_v01.mp4"
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
        print("Built", p_r12_comp.name, flush=True)

    p_r14_comp = OUT / "composite_031_r14_core_sdo_fact_v01.mp4"
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
        print("Built", p_r14_comp.name, flush=True)

    p_r16_comp = OUT / "composite_031_r16_dynamo_cutaway_v01.mp4"
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
        print("Built", p_r16_comp.name, flush=True)

    p_r20_comp = OUT / "composite_031_r20_gauss_strength_full_v01.mp4"
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
        print("Built", p_r20_comp.name, flush=True)

    p_r21_plate = OUT / "plate_031_r21_earth_limb_v01.mp4"
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
    p_r21_comp = OUT / "composite_031_r21_compass_limb_v01.mp4"
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
        print("Built", p_r21_comp.name, flush=True)

    p_r25_plate = OUT / "plate_031_r25_iss_orbit_cuts_v01.mp4"
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
    p_r25_comp = OUT / "composite_031_r25_belts_iss_v01.mp4"
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
        print("Built", p_r25_comp.name, flush=True)

    p_r26 = OUT / "plate_031_r26_iss_clouds_v01.mp4"
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
        print("Built", p_r26.name, flush=True)

    p_r27_comp = OUT / "composite_031_r27_hubble_saa_full_v01.mp4"
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
        print("Built", p_r27_comp.name, flush=True)

    p_r28a = OUT / "plate_031_r28a_iss_payload_v01.mp4"
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
    p_r28_comp = OUT / "composite_031_r28_payload_satsafe_v01.mp4"
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
        print("Built", p_r28_comp.name, flush=True)

    p_r30a = OUT / "plate_031_r30a_iss_limb_v01.mp4"
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
    p_r30_comp = OUT / "composite_031_r30_recap_twist_v01.mp4"
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
        print("Built", p_r30_comp.name, flush=True)

    p_r33_comp = OUT / "composite_031_r33_core_laschamp_paleo_v01.mp4"
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
        print("Built", p_r33_comp.name, flush=True)

    p_r42a = OUT / "plate_031_r42a_iss_blue_limb_v01.mp4"
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
    p_r42_comp = OUT / "composite_031_r42_column_limb_v01.mp4"
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
        print("Built", p_r42_comp.name, flush=True)

    p_r46_comp = OUT / "composite_031_r46_solar_grid_v01.mp4"
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
        print("Built", p_r46_comp.name, flush=True)

    p_r47ab = OUT / "plate_031_r47ab_svs_core_twisted_v01.mp4"
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
    p_r47_comp = OUT / "composite_031_r47_svs_tangle_v01.mp4"
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
        print("Built", p_r47_comp.name, flush=True)

    p_r52_comp = OUT / "composite_031_r52_aurora_generations_dynamo_v01.mp4"
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
        print("Built", p_r52_comp.name, flush=True)


if __name__ == "__main__":
    build_all()
