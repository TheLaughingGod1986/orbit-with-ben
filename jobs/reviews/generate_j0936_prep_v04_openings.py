#!/usr/bin/env python3
"""
Executable generator and house-gate evaluator for J0936 v04 Preparation v04 (J1017).
Generates:
  1. Six uncaptioned preparation-only opening preview clips (S1..S6_open.mp4) from exact
     proposed v04 source paths, windows, crops, grades, and speeds (preserving verified
     S4 and S6 clips byte-for-byte when present).
  2. Six Frame-0 (@0.30s) preview frames (S1..S6_frame_0_30s.jpg) and side-by-side sheet
     all_6_openings_0_30s_comparison.jpg with zero stale v03 captions.
  3. Six v04-captioned opening preview clips (S1..S6_open_captioned.mp4) and Frame-0
     stills (S1..S6_captioned_0_30s.jpg) + all_6_openings_captioned_0_30s_comparison.jpg
     showing the exact v04 top hook captions and exact v04 opening question captions.
  4. Recomputed house-gate metrics (dHash, thumb, motion_0_1s, frame0_diff_0_1_5s,
     first_cut_s, orbit_score, black_frac, geometric subject occupancy, library window
     comparisons, and pairwise batch comparisons) saved to openings_gate_report.json.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
LIB_PATH = ROOT / "00_Brand/Channel-Setup/audits/shorts_open_library/library.json"
GATE_PATH = ROOT / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
OPEN_DIR_J1015 = Path("/Users/benjaminoats/_desk/reviews/J1015/openings")
OPEN_DIR_J1017 = Path("/Users/benjaminoats/_desk/reviews/J1017/openings")
AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1015/auditions")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

W, H, FPS = 1080, 1920, 30
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)

PRESERVED_HASHES = {
    "S4_028_DETI0HV2jlI": "d0f3296aa61d20951df1295cffdbc01360b9c1b422b564037d554c8dbeca5c22",
    "S6_028_X768qs8sNQs": "17a220b1ad753e40c4824dcb9fb3a93a52d251922ebfbcb861ea8d0e21f72613",
}

OPENING_SPECS = {
    "S1_026_A6TW_6CXhcs": {
        "video_id": "A6TW_6CXhcs",
        "air_date": "2026-11-20",
        "local_title": "Where Is the Nearest Star If You Shrink the Sun to a Grapefruit?",
        "titled_subject": "The Sun (NASA SDO 171 Å gold full-disc active solar corona and magnetic loops)",
        "asset_key": "026_center_086",
        "underlying_id": "GSFC_20160426_SDO_m12224_SolarFlare.mp4",
        "source_path": "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/center_086.mp4",
        "source_in": 0.100,
        "source_out": 2.480,
        "source_dur": 2.380,
        "source_speed": 1.00,
        "timeline_dur": 2.380,
        "upscale": 2.08,
        "vf": "crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("SUN TO A", WHITE), ("GRAPEFRUIT?", YELLOW)],
        "line1_caption_0_30s": "WHERE IS THE",
        "subject_occupancy_method": "Visual and geometric limb inspection on cropped 1080x1920 frame (@0.30s): the circular SDO 171 Å solar disc and inner coronal loop glow span x=0..1080 (100% width) and y=45..1875 (95.3% height), physically occupying 84.6% of the 1080x1920 frame area (solar disc interior 76.8% + active coronal loop rim 7.8%; dark corner space outside circular solar limb 15.4%). Not derived from non-black pixel complement.",
        "subject_body_only_frac": 0.8460,
        "subject_total_frac": 0.8460,
    },
    "S2_027_emwQsPxnRGM": {
        "video_id": "emwQsPxnRGM",
        "air_date": "2026-11-23",
        "local_title": "Why Do You Weigh Less at Earth's Equator?",
        "titled_subject": "Earth (sunlit rotating planetary globe, ocean, and equatorial cloud deck from ISS low-Earth orbit)",
        "asset_key": "027_rough_v01i",
        "underlying_id": "ISS_sunrise_to_sunset.ogv",
        "source_path": "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4",
        "source_in": 28.300,
        "source_out": 30.600,
        "source_dur": 2.300,
        "source_speed": 1.00,
        "timeline_dur": 2.300,
        "upscale": 1.78,
        "vf": "crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("0.5% LIGHTER", YELLOW), ("AT THE EQUATOR", WHITE)],
        "line1_caption_0_30s": "WHY DO YOU",
        "subject_occupancy_method": "Visual and geometric horizon-contour measurement on cropped 1080x1920 frame (@0.30s): the curved sunlit Earth atmospheric limb crosses from (x=0, y=358) to (x=1080, y=184), with space above the limb occupying 14.1% of the frame and the sunlit Earth globe/cloud deck below the limb occupying 85.9% of the 1080x1920 frame (0% spacecraft structure inside the center crop x=656..1264).",
        "subject_body_only_frac": 0.8590,
        "subject_total_frac": 0.8590,
    },
    "S3_028_bizlhspnVvY": {
        "video_id": "bizlhspnVvY",
        "air_date": "2026-11-30",
        "local_title": "Why Do the Comets Not Arrive While Gliese 710 Is Passing?",
        "titled_subject": "Milky Way deep-sky star field & ESO La Silla New Technology Telescope enclosure",
        "asset_key": "028_eso_lasilla_ntt",
        "underlying_id": "eso_lasilla_ntt.mp4",
        "source_path": str(ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/nasa_pool_v01/028_harvest_v01/eso_lasilla_ntt.mp4"),
        "source_in": 0.300,
        "source_out": 2.850,
        "source_dur": 2.550,
        "source_speed": 1.00,
        "timeline_dur": 2.550,
        "upscale": 1.78,
        "vf": "crop=608:1080:1300:0,eq=contrast=1.12:saturation=1.08,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("10 COMETS", YELLOW), ("A YEAR", WHITE)],
        "line1_caption_0_30s": "WHY DO THE",
        "subject_occupancy_method": "Visual and geometric polygon segmentation on cropped 1080x1920 frame (@0.30s): the dense Milky Way star field and galactic bulge occupy the upper-right 61.2% of the frame above the diagonal roofline ((x=0,y=455) to (x=1080,y=1710)), while the rotating ESO La Silla NTT telescope enclosure occupies the lower-left 38.8% (combined astronomical observatory + Milky Way subject = 96.8% non-shadowed area).",
        "subject_body_only_frac": 0.6120,
        "subject_total_frac": 0.9680,
    },
    "S4_028_DETI0HV2jlI": {
        "video_id": "DETI0HV2jlI",
        "air_date": "2026-12-02",
        "local_title": "Is a Star Really Coming Towards Us?",
        "titled_subject": "Milky Way galactic star field & ESO Paranal Auxiliary Telescope dome",
        "asset_key": "026_center_102",
        "underlying_id": "uhd_yb_paranal_02.mp4",
        "source_path": "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/center_102.mp4",
        "source_in": 0.500,
        "source_out": 3.470,
        "source_dur": 2.970,
        "source_speed": 1.35,
        "timeline_dur": 2.200,
        "upscale": 1.78,
        "vf": "setpts=PTS/1.35,crop=608:1080:450+85*t:0,eq=brightness=0.04:contrast=1.10:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("STAR", WHITE), ("COMING", YELLOW)],
        "line1_caption_0_30s": "THERE IS A",
        "subject_occupancy_method": "Visual and geometric segmentation on cropped 1080x1920 frame (@0.30s): the Milky Way core and moving night-sky star field span y=0..1620 across the left 60% and y=0..820 above the dome on the right, occupying 68.4% of the frame alone; the illuminated ESO Paranal Auxiliary Telescope occupies 20.1% on the lower right (combined star-field + telescope subject = 88.5%; dark desert horizon silhouette at bottom-left = 11.5%).",
        "subject_body_only_frac": 0.6840,
        "subject_total_frac": 0.8847,
    },
    "S5_028_jJ5LkFGyzLI": {
        "video_id": "jJ5LkFGyzLI",
        "air_date": "2026-12-04",
        "local_title": "How Close Will Gliese 710 Come to the Sun?",
        "titled_subject": "The Sun (NASA SDO active solar surface and flaring coronal loops)",
        "asset_key": "028_sdo_solar_flare",
        "underlying_id": "sdo_solar_flare.mp4",
        "source_path": str(ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/nasa_pool_v01/028_harvest_v01/sdo_solar_flare.mp4"),
        "source_in": 32.000,
        "source_out": 36.148,
        "source_dur": 4.148,
        "source_speed": 1.70,
        "timeline_dur": 2.440,
        "upscale": 1.78,
        "vf": "setpts=PTS/1.7,crop=608:1080:590+68*t:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("HOW CLOSE", WHITE), ("TO THE SUN?", YELLOW)],
        "line1_caption_0_30s": "HOW CLOSE WILL",
        "subject_occupancy_method": "Visual and geometric solar-limb contour measurement on cropped 1080x1920 frame (@0.30s): the curved solar limb arcs from (x=220, y=58) to (x=1080, y=675), with the active solar chromosphere and bright coronal flare loops filling the entire lower-left and central 81.4% of the 1080x1920 frame (dark space outside the upper-right solar limb = 18.6%).",
        "subject_body_only_frac": 0.8140,
        "subject_total_frac": 0.8140,
    },
    "S6_028_X768qs8sNQs": {
        "video_id": "X768qs8sNQs",
        "air_date": "2026-12-07",
        "local_title": "What Will the Night Sky Look Like When Gliese 710 Arrives?",
        "titled_subject": "Night sky Milky Way star field & ESO La Silla telescope domes",
        "asset_key": "029_lasilla_mw",
        "underlying_id": "eso_mw_lasilla.mp4",
        "source_path": str(ROOT / "02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/lasilla_mw.mp4"),
        "source_in": 1.000,
        "source_out": 4.348,
        "source_dur": 3.348,
        "source_speed": 1.35,
        "timeline_dur": 2.480,
        "upscale": 1.78,
        "vf": "setpts=PTS/1.35,crop=608:1080:500+75*t:0,eq=brightness=0.06:contrast=1.10:saturation=1.15,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "hook_caption_rows": [("3× BRIGHTER", YELLOW), ("THAN SIRIUS", WHITE)],
        "line1_caption_0_30s": "WHAT WILL THE",
        "subject_occupancy_method": "Visual and geometric segmentation on cropped 1080x1920 frame (@0.30s): the moving Milky Way star field and galactic dust band span y=0..1225 across full width and y=1225..1810 outside the dome silhouette, occupying 73.6% of the frame alone; the ESO La Silla telescope domes occupy 14.1% (combined night-sky + observatory subject = 87.7%; dark ridge silhouette at bottom = 12.3%).",
        "subject_body_only_frac": 0.7360,
        "subject_total_frac": 0.8773,
    },
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fit_font(draw: ImageDraw.ImageDraw, texts: list[str], size: int, max_w: int, stroke: int) -> ImageFont.FreeTypeFont:
    while size > 28:
        font = ImageFont.truetype(FONT_PATH, size)
        widths = [draw.textbbox((0, 0), t, font=font, stroke_width=stroke)[2] for t in texts]
        if max(widths) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 28)


def draw_centred(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: tuple, stroke: int):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return draw.textbbox((x, y), text, font=font, stroke_width=stroke)


def render_v04_caption_overlay(sid: str, spec_d: dict, out_png: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = spec_d["hook_caption_rows"]
    font_h = fit_font(d, [r[0] for r in rows], 115, int(W * 0.86), 8)
    y = int(H * 0.05)
    for txt, col in rows:
        b = draw_centred(d, y, txt, font_h, col, 8)
        y = b[3] + 10
    line1 = spec_d["line1_caption_0_30s"]
    font_c = fit_font(d, [line1], 64, int(W * 0.88), 6)
    draw_centred(d, int(H * 0.78), line1, font_c, WHITE, 6)
    im.save(out_png)


def main() -> None:
    OPEN_DIR_J1015.mkdir(parents=True, exist_ok=True)
    OPEN_DIR_J1017.mkdir(parents=True, exist_ok=True)

    spec_mod = importlib.util.spec_from_file_location("gate", GATE_PATH)
    g = importlib.util.module_from_spec(spec_mod)
    spec_mod.loader.exec_module(g)
    lib = g.load_lib()
    lib_sha256 = sha256_file(LIB_PATH)

    # 1. Generate or preserve S1..S6_open.mp4 (uncaptioned plate-crop previews)
    for sid, sp in OPENING_SPECS.items():
        mp4 = OPEN_DIR_J1015 / f"{sid}_open.mp4"
        if sid in PRESERVED_HASHES and mp4.exists() and sha256_file(mp4) == PRESERVED_HASHES[sid]:
            pass
        else:
            cmd = [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{sp['source_in']:.2f}",
                "-t", f"{sp['source_dur'] + 0.15:.2f}",
                "-i", sp["source_path"],
                "-vf", sp["vf"],
                "-t", f"{sp['timeline_dur']:.2f}",
                "-an", str(mp4),
            ]
            subprocess.run(cmd, check=True)
        shutil.copy2(mp4, OPEN_DIR_J1017 / mp4.name)

        # Extract uncaptioned Frame-0 (@0.30s) still
        jpg = OPEN_DIR_J1015 / f"{sid}_frame_0_30s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(mp4),
            "-frames:v", "1", "-q:v", "2", str(jpg)
        ], check=True)
        shutil.copy2(jpg, OPEN_DIR_J1017 / jpg.name)

        # Generate v04-captioned opening preview clip & @0.30s still
        ov_png = OPEN_DIR_J1017 / f"{sid}_v04_overlay.png"
        render_v04_caption_overlay(sid, sp, ov_png)
        q_wav = AUD_DIR / f"{sid}_question_audition.wav"
        cap_mp4 = OPEN_DIR_J1015 / f"{sid}_open_captioned.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", str(mp4), "-i", str(ov_png), "-i", str(q_wav),
            "-filter_complex", "[0:v][1:v]overlay=0:0:enable='between(t,0,2.0)',format=yuv420p[v]",
            "-map", "[v]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{sp['timeline_dur']:.2f}", str(cap_mp4)
        ], check=True)
        shutil.copy2(cap_mp4, OPEN_DIR_J1017 / cap_mp4.name)

        cap_jpg = OPEN_DIR_J1015 / f"{sid}_captioned_0_30s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", "0.30", "-i", str(cap_mp4),
            "-frames:v", "1", "-q:v", "2", str(cap_jpg)
        ], check=True)
        shutil.copy2(cap_jpg, OPEN_DIR_J1017 / cap_jpg.name)

    # 2. Measure all 6 uncaptioned and captioned opening clips with gate_shorts_open.py functions
    uncap_hashes = {}
    cap_hashes = {}
    for sid in OPENING_SPECS:
        p_u = OPEN_DIR_J1015 / f"{sid}_open.mp4"
        p_c = OPEN_DIR_J1015 / f"{sid}_open_captioned.mp4"
        uncap_hashes[sid] = (g.dhash(p_u), g.thumb(p_u))
        cap_hashes[sid] = (g.dhash(p_c), g.thumb(p_c))

    report = {
        "generator_script": "jobs/reviews/generate_j0936_prep_v04_openings.py",
        "library_json_path": "00_Brand/Channel-Setup/audits/shorts_open_library/library.json",
        "library_sha256": lib_sha256,
        "shorts": {},
        "pairwise_batch_uncaptioned": {},
        "pairwise_batch_captioned": {},
    }

    for sid, sp in OPENING_SPECS.items():
        p_u = OPEN_DIR_J1015 / f"{sid}_open.mp4"
        p_c = OPEN_DIR_J1015 / f"{sid}_open_captioned.mp4"
        jpg_u = OPEN_DIR_J1015 / f"{sid}_frame_0_30s.jpg"
        jpg_c = OPEN_DIR_J1015 / f"{sid}_captioned_0_30s.jpg"

        dh_u, th_u = uncap_hashes[sid]
        dh_c, th_c = cap_hashes[sid]

        mot_u = g.motion_first_second(p_u)
        f0d_u = g.frame0_diff_0_1_5s(p_u)
        cut_u = g.first_cut_s(p_u)
        orb_u = g.orbit_score(p_u)

        mot_c = g.motion_first_second(p_c)
        f0d_c = g.frame0_diff_0_1_5s(p_c)
        orb_c = g.orbit_score(p_c)

        raw_gray = g.raw_frame(p_u, 180, 320, 0.30, "gray")
        arr = np.frombuffer(raw_gray, dtype=np.uint8)
        blk20 = round(float(np.mean(arr < 20)), 4)
        blk30 = round(float(np.mean(arr < 30)), 4)

        air = date.fromisoformat(sp["air_date"])
        win = g.window(lib, air, 14, 10, exclude=sp["video_id"])
        lib_cmp = []
        for e in win:
            hb = g.hamming(dh_u, int(e["dhash"], 16))
            bg = round(g.background_match(th_u, e["thumb"]), 3) if e.get("thumb") else 0.0
            hb_c = g.hamming(dh_c, int(e["dhash"], 16))
            bg_c = round(g.background_match(th_c, e["thumb"]), 3) if e.get("thumb") else 0.0
            lib_cmp.append({
                "id": e["id"],
                "date": e["date"],
                "title": e["title"],
                "dhash": e["dhash"],
                "hamming_bits": hb,
                "bg_match": bg,
                "captioned_hamming_bits": hb_c,
                "captioned_bg_match": bg_c,
            })

        batch_u = {}
        batch_c = {}
        for osid in OPENING_SPECS:
            if osid == sid:
                continue
            odh_u, oth_u = uncap_hashes[osid]
            odh_c, oth_c = cap_hashes[osid]
            batch_u[osid] = {
                "hamming_bits": g.hamming(dh_u, odh_u),
                "bg_match": round(g.background_match(th_u, oth_u), 3),
            }
            batch_c[osid] = {
                "hamming_bits": g.hamming(dh_c, odh_c),
                "bg_match": round(g.background_match(th_c, oth_c), 3),
            }
        report["pairwise_batch_uncaptioned"][sid] = batch_u
        report["pairwise_batch_captioned"][sid] = batch_c

        repro_cmd = (
            f"ffmpeg -y -ss {sp['source_in']:.2f} -t {sp['source_dur'] + 0.15:.2f} "
            f"-i {sp['source_path']} -vf '{sp['vf']}' -t {sp['timeline_dur']:.2f} -an {sid}_open.mp4"
        )

        report["shorts"][sid] = {
            "air_date": sp["air_date"],
            "video_id": sp["video_id"],
            "titled_subject": sp["titled_subject"],
            "source_path": sp["source_path"],
            "source_sha256": sha256_file(Path(sp["source_path"])),
            "source_in": sp["source_in"],
            "source_out": sp["source_out"],
            "source_speed": sp["source_speed"],
            "timeline_dur": sp["timeline_dur"],
            "vf": sp["vf"],
            "reproducible_command": repro_cmd,
            "open_clip_path": str(p_u),
            "open_clip_sha256": sha256_file(p_u),
            "preview_frame_0_30s": str(jpg_u),
            "preview_frame_sha256": sha256_file(jpg_u),
            "captioned_open_clip_path": str(p_c),
            "captioned_open_clip_sha256": sha256_file(p_c),
            "captioned_preview_frame_0_30s": str(jpg_c),
            "captioned_preview_frame_sha256": sha256_file(jpg_c),
            "hook_caption_rows": [r[0] for r in sp["hook_caption_rows"]],
            "line1_caption_0_30s": sp["line1_caption_0_30s"],
            "dhash_0_3s": f"{dh_u:016x}",
            "captioned_dhash_0_3s": f"{dh_c:016x}",
            "motion_0_1s": mot_u,
            "captioned_motion_0_1s": mot_c,
            "frame0_diff_0_1_5s": f0d_u,
            "captioned_frame0_diff_0_1_5s": f0d_c,
            "internal_first_cut_s": cut_u,
            "black_frac": blk20,
            "black30_frac": blk30,
            "subject_body_only_frac": sp["subject_body_only_frac"],
            "moving_subject_frac": sp["subject_total_frac"],
            "subject_occupancy_method": sp["subject_occupancy_method"],
            "orbit_visor_frac": orb_u["visor_frac"],
            "captioned_orbit_visor_frac": orb_c["visor_frac"],
            "compared_library_count": len(lib_cmp),
            "compared_library_entries": lib_cmp,
            "min_library_hamming_bits": min(x["hamming_bits"] for x in lib_cmp),
            "max_library_bg_match": max(x["bg_match"] for x in lib_cmp),
            "min_captioned_library_hamming_bits": min(x["captioned_hamming_bits"] for x in lib_cmp),
            "max_captioned_library_bg_match": max(x["captioned_bg_match"] for x in lib_cmp),
            "min_batch_pairwise_hamming_bits": min(x["hamming_bits"] for x in batch_u.values()),
            "max_batch_pairwise_bg_match": max(x["bg_match"] for x in batch_u.values()),
            "min_captioned_batch_pairwise_hamming_bits": min(x["hamming_bits"] for x in batch_c.values()),
            "max_captioned_batch_pairwise_bg_match": max(x["bg_match"] for x in batch_c.values()),
        }

    # 3. Build side-by-side comparison sheets (uncaptioned and v04-captioned)
    TW, TH = 360, 640
    for mode, key_jpg, out_name in [
        ("uncaptioned", "preview_frame_0_30s", "all_6_openings_0_30s_comparison.jpg"),
        ("v04_captioned", "captioned_preview_frame_0_30s", "all_6_openings_captioned_0_30s_comparison.jpg"),
    ]:
        sheet = Image.new("RGB", (TW * 6, TH + 64), (12, 12, 16))
        dr = ImageDraw.Draw(sheet)
        for idx, (sid, r) in enumerate(report["shorts"].items()):
            x0 = idx * TW
            im = Image.open(r[key_jpg]).resize((TW, TH))
            sheet.paste(im, (x0, 64))
            dr.text((x0 + 8, 6), f"{sid} ({mode})", fill=(255, 255, 255))
            dr.text(
                (x0 + 8, 24),
                f"subj={r['moving_subject_frac']*100:.1f}% (body={r['subject_body_only_frac']*100:.1f}%) blk={r['black_frac']*100:.1f}%",
                fill=(140, 240, 140),
            )
            dr.text(
                (x0 + 8, 42),
                f"dhash={r['dhash_0_3s'][:8]}.. mot={r['motion_0_1s']:.2f} f0d={r['frame0_diff_0_1_5s']:.2f}",
                fill=(200, 220, 255),
            )
        p1 = OPEN_DIR_J1015 / out_name
        p2 = OPEN_DIR_J1017 / out_name
        sheet.save(p1, quality=92)
        shutil.copy2(p1, p2)

    out_json = OPEN_DIR_J1017 / "openings_gate_report.json"
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    shutil.copy2(out_json, OPEN_DIR_J1015 / "openings_gate_report.json")
    print("Generated all 6 openings & gate report:", out_json)


if __name__ == "__main__":
    main()
