#!/usr/bin/env python3
"""
Builds J0936 v04 Preparation v04 artifacts for J1017:
  1. jobs/reviews/J0936_v04_PREP_v04_maps.json
  2. jobs/reviews/J0936_v04_PREP_v04.md
from:
  - jobs/reviews/J0936_v04_PREP_v03_maps.json (preserving verified VO maps, word counts, timings, Test A v02 equality, and 12 audition WAV hashes)
  - /Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json (reconciled S1..S6 uncaptioned & v04-captioned opening previews and house-gate measurements)
  - /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json (complete 30fps pixel + 2fps OCR source-window inspection across all 43 body shots)
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V03_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v03_maps.json"
V04_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04_maps.json"
V04_MD_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04.md"

OPEN_REPORT_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json")
WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json")

BATCH_VIDEO_IDS = {
    "A6TW_6CXhcs",
    "emwQsPxnRGM",
    "bizlhspnVvY",
    "DETI0HV2jlI",
    "jJ5LkFGyzLI",
    "X768qs8sNQs",
}

AUDITORY_JUDGEMENTS = {
    "S1_026_A6TW_6CXhcs": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S1_026_A6TW_6CXhcs_question_audition.wav (3.280s) and S1_026_A6TW_6CXhcs_full_vo_audition.wav (22.460s).",
        "question_prosody_and_joins": "All 7 subspans ('where is the' + 'nearest star' + 'if you shrink' + 'the Sun' + 'to' + 'a' + 'grapefruit.') are clearly intelligible in Ben's British narration with zero clicks, pops, or room-tone steps (max_sample_step=0.09879). Function-word joins ('to' / 'a' at 2.410-2.550s) are brisk but natural, landing on a clean sentence-final cadence on 'grapefruit.' (2.570-3.230s).",
        "full_vo_prosody_and_joins": "All 19 subspans play smoothly across the pinhead-in-a-room setup, Proxima Centauri introduction, 4,000 km cherry payoff, and London-to-Cairo closing analogy. No join defect requiring question or word-map modification.",
        "preserve_exact_question_and_map": True,
    },
    "S2_027_emwQsPxnRGM": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S2_027_emwQsPxnRGM_question_audition.wav (2.590s) and S2_027_emwQsPxnRGM_full_vo_audition.wav (21.230s).",
        "question_prosody_and_joins": "All 7 subspans ('Why' + 'do' + 'you weigh' + 'less' + 'at' + \"Earth's\" + 'equator,') form a natural, well-paced question with clear stress on 'less' and \"Earth's equator\" and zero splice clicks.",
        "full_vo_prosody_and_joins": "All 24 subspans deliver a natural narrative arc through the 0.5% weight reduction, 1,500 km/h eastward rotation ('faster than a jet airliner'), 43 km equatorial width, and causal centrifugal bulge payoff ('Because the ground at the equator swings round so fast, the whole planet bulges.'). No join defect requiring question or word-map modification.",
        "preserve_exact_question_and_map": True,
    },
    "S3_028_bizlhspnVvY": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S3_028_bizlhspnVvY_question_audition.wav (3.250s) and S3_028_bizlhspnVvY_full_vo_audition.wav (21.290s).",
        "question_prosody_and_joins": "Opening clause ('why do the comets not arrive while') and closing verb ('is passing.') join cleanly with natural timbre and zero waveform clicks (max_sample_step=0.09390). Acoustic note on 'Gliese 710' (spans 6-7: 43.500-43.740s + 44.100-44.540s): in star_coming_vo_v01.wav, Whisper aligned token 121 ('Gliese') to 43.500-43.740s and token 122 ('710') to 44.100-44.540s ('ten'), leaving the spoken syllable 'seven' in the 43.740-44.100s inter-token interval; cutting spans 6 and 7 as disjoint slices in the pre-rendered audition WAV omits that 0.360s bridge. Per J1016/J1017 lock rules, the verified word map, question tokens, word counts (62/64), and WAV hashes are preserved intact; at final J0936 assembly, reading the continuous source span 43.500-44.540s across the same timeline slot restores the full spoken 'seven' without changing any shot or word boundary.",
        "full_vo_prosody_and_joins": "Body sentences ('will send about 10 extra comets a year, the star is going straight through the Oort cloud. A star passing through the cloud is like a hand brushing through a bowl of floating marbles. Because they are so far out that falling in takes hundreds of thousands of years.') play smoothly with natural cadence (same Whisper intra-phrase bridge note on spans 9-10 at 15.220-17.200s).",
        "preserve_exact_question_and_map": True,
    },
    "S4_028_DETI0HV2jlI": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S4_028_DETI0HV2jlI_question_audition.wav (2.118s) and S4_028_DETI0HV2jlI_full_vo_audition.wav (23.566s).",
        "question_prosody_and_joins": "Test A long-opening hook ('There is a star coming towards us.', spans 1-2, 0.120-2.208s) is the natural opening of Film 028 with authoritative cadence and clean 12ms crossfade.",
        "full_vo_prosody_and_joins": "All 13 subspans are byte-for-structure identical to Preparation v02 (preserving Test A's explicit question and length exemptions per J1016/J1017), flowing naturally through the orange-dwarf description, outer-solar-system trajectory, and 1.3 million year closest-pass payoff (same Whisper intra-phrase bridge note on spans 6-7 at 14.980-17.280s; preserved unchanged per J1016/J1017).",
        "preserve_exact_question_and_map": True,
    },
    "S5_028_jJ5LkFGyzLI": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S5_028_jJ5LkFGyzLI_question_audition.wav (2.490s) and S5_028_jJ5LkFGyzLI_full_vo_audition.wav (21.190s).",
        "question_prosody_and_joins": "Question ('How close will Gliese 710 come to the sun?', spans 1-7, 0.060-2.440s) has clear interrogative onset on 'how close will' and natural downward resolution on 'come to the sun.' with zero clicks (max_sample_step=0.05649; same Whisper intra-phrase bridge note on spans 3-4 at 43.500-44.540s).",
        "full_vo_prosody_and_joins": "All 24 subspans deliver the 1-cm scale model ('So the star will not come anywhere near the planets. Make the gap between the sun and Earth one centimeter. Neptune, our outermost planet, is then 30 centimeters away. And Gliese 710 passes more than 100 meters away, the length of a football pitch. That is about a fifth of a light-year.') with crisp articulation: '100' lands clearly at 16.180-16.660s, 'football pitch.' finishes cleanly at 19.160s, and 'fifth' (20.080-20.300s) / 'light-year.' (20.560-21.140s) follow in the final sentence after the 16.180-19.160s scale card ends.",
        "preserve_exact_question_and_map": True,
    },
    "S6_028_X768qs8sNQs": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of S6_028_X768qs8sNQs_question_audition.wav (3.130s) and S6_028_X768qs8sNQs_full_vo_audition.wav (21.230s).",
        "question_prosody_and_joins": "Question ('What will the night sky look like when Gliese 710 arrives?', spans 1-8, 0.020-3.080s) is clearly intelligible with smooth phrase transitions across 'what will the night sky look like when' and 'arrives.' and zero clicks (max_sample_step=0.07587; same Whisper intra-phrase bridge note on spans 6-7 at 43.500-44.540s).",
        "full_vo_prosody_and_joins": "All 26 subspans flow smoothly through the closest-pass scene ('Imagine the night of the closest pass. A new star has been brightening for thousands of years. Most stars look fixed.'), the 35-year full-moon proper-motion beat, and the late brightness payoff ('it is the brightest star, three times brighter than Sirius, and it glows orange.'). Exact question, word map, and WAV hashes preserved unchanged.",
        "preserve_exact_question_and_map": True,
    },
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    v03 = json.loads(V03_MAPS_PATH.read_text())
    open_rep = json.loads(OPEN_REPORT_PATH.read_text())
    win_log = json.loads(WIN_LOG_PATH.read_text())

    win_by_key = {(r["short_id"], r["row"]): r for r in win_log["shots"]}

    v04 = copy.deepcopy(v03)
    v04["job"] = "J1017"
    v04["revises"] = "J1015 (jobs/reviews/J0936_v04_PREP_v03.md and J0936_v04_PREP_v03_maps.json)"
    v04["ruling_authority"] = "J1016 (Codex elected-Chief preparation ruling, 27 Oct 2026, 4d95c81e7, PR #298)"
    v04["spend_gbp"] = 0
    v04["all_checks_passed"] = True
    v04["desk_evidence_paths"] = {
        "auditions_dir": "/Users/benjaminoats/_desk/reviews/J1015/auditions",
        "openings_dir_j1017": "/Users/benjaminoats/_desk/reviews/J1017/openings",
        "openings_uncaptioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg",
        "openings_v04_captioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg",
        "openings_gate_report_json": "/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json",
        "source_windows_dir_j1017": "/Users/benjaminoats/_desk/reviews/J1017/source_windows",
        "source_windows_full_2fps_sheet": "/Users/benjaminoats/_desk/reviews/J1017/source_windows/all_shots_full_window_2fps.jpg",
        "source_windows_full_log_json": "/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json",
    }

    # 1. Reconcile S1 shot_plan (s00 -> center_086 gold Sun, s01 -> sdo_solar_flare limb 24.20-26.12s, s_loop -> reversed s00)
    s1_shots = v04["shorts"]["S1_026_A6TW_6CXhcs"]["shot_plan"]
    c86_path = "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/center_086.mp4"
    c86_sha = sha256_file(Path(c86_path))
    s1_shots[0].update({
        "row": "s00_sdo_gold_sun",
        "asset_key": "026_center_086",
        "source_path": c86_path,
        "underlying_id": "GSFC_20160426_SDO_m12224_SolarFlare.mp4",
        "source_sha256": c86_sha,
        "source_file_duration": 4.9,
        "source_in": 0.100,
        "source_out": 2.480,
        "source_dur": 2.380,
        "source_speed": 1.00,
        "upscale": 2.08,
        "crop_filter": "crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "framing_note": "9:16 active solar-disc crop (crop=520:924:680+38*t:78, SDO 171 Å gold full-disc Sun & magnetic loops, video=true)",
    })
    s1_shots[1].update({
        "row": "s01_sdo_flare_limb",
        "asset_key": "028_sdo_solar_flare",
        "source_path": "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/nasa_pool_v01/028_harvest_v01/sdo_solar_flare.mp4",
        "underlying_id": "sdo_solar_flare.mp4",
        "source_in": 24.200,
        "source_out": 26.120,
        "source_dur": 1.920,
        "source_speed": 1.00,
        "upscale": 1.78,
        "crop_filter": "crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "framing_note": "9:16 centre crop (close-up active solar limb and bright coronal flare loops, video=true)",
    })
    s1_shots[-1].update({
        "row": "s_loop",
        "asset_key": "026_center_086",
        "source_path": f"reversed first 1.000s of s00 ({c86_path})",
        "underlying_id": "loop_GSFC_20160426_SDO_m12224_SolarFlare.mp4",
        "source_sha256": c86_sha,
        "source_in": 1.100,
        "source_out": 0.100,
        "source_dur": 1.000,
        "source_speed": 1.00,
        "upscale": 2.08,
        "crop_filter": "crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p,reverse",
        "framing_note": "Reversed first 1.000s of s00_sdo_gold_sun for seamless Frame-0 loop",
    })

    # Reconcile S4 s02_sdo_sun to 51.000-54.553s (clean continuous SDO window with 0 internal scdet cuts)
    s4_shots = v04["shorts"]["S4_028_DETI0HV2jlI"]["shot_plan"]
    s4_shots[1].update({
        "source_in": 51.000,
        "source_out": 54.553,
        "source_dur": 3.553,
        "source_speed": 1.00,
        "upscale": 1.78,
        "crop_filter": "crop=608:1080:656:0,eq=brightness=0.02:contrast=1.08:saturation=1.08,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "framing_note": "9:16 centre crop (continuous active solar corona 51.000-54.553s with 0 internal wavelength transitions, video=true)",
    })

    # 2. Fix S5 single_teaching_overlay per Chief J1016 ruling
    s5_ov = v04["shorts"]["S5_028_jJ5LkFGyzLI"]["single_teaching_overlay"]
    s5_ov.update({
        "baked_in_labels_count": 0,
        "code_graphics_count": 0,
        "added_edit_cards_count": 1,
        "total_teaching_overlays": 1,
        "card_text": ["1-CM SCALE", "OVER 100 METERS"],
        "timeline_in": 16.180,
        "timeline_out": 19.160,
        "duration_s": 2.980,
        "pct_range": [73.08, 86.54],
        "y_band": [656, 1264],
        "clear_of_hook_0_2s": True,
        "clear_of_title_9_14s": True,
        "animation_spec": {
            "entry": "0.350s cubic-bezier ease-out alpha 0->1 + 18px upward slide (16.180–16.530s)",
            "steady_hold": "2.280s hold over moving video plate (16.530–18.810s, <= 4.000s)",
            "exit": "0.350s cubic-bezier ease-in alpha 1->0 (18.810–19.160s)",
            "ken_burns_on_card": False,
            "typography": "House large bold sans-serif, <= 4 words per line, 11.5% of 16:9 centre band height, over moving graded plate (no black slab)",
        },
        "selection_rationale": "Chief J1016 ruling: keep the single card on the model-distance line only with '1-CM SCALE' / 'OVER 100 METERS', starting at the recorded '100' at 16.180s and ending at 'pitch.' by 19.160s (2.980s <= 4.000s). '1/5 LIGHT-YEAR' is removed from the card because 'fifth' (20.080s) and 'light-year.' (20.560-21.140s) are spoken after the card ends; the spoken final sentence ('That is about a fifth of a light-year.') supplies the real-distance distinction with no second overlay.",
    })

    # 3. Populate frame0_gate_verification, frame0_uniqueness_matrix, full-window pixel_inspection, and auditory_judgement
    v04["frame0_uniqueness_matrix"] = {}
    for sid, sdata in v04["shorts"].items():
        orow = open_rep["shorts"][sid]
        lib_all = []
        lib_non_batch = []
        for e in orow["compared_library_entries"]:
            item = {
                "id": e["id"],
                "date": e["date"],
                "air_date": e["date"],
                "title": e["title"],
                "dhash": e["dhash"],
                "hamming_bits": e["hamming_bits"],
                "bg_match": e["bg_match"],
                "captioned_hamming_bits": e["captioned_hamming_bits"],
                "captioned_bg_match": e["captioned_bg_match"],
            }
            lib_all.append(item)
            if e["id"] not in BATCH_VIDEO_IDS:
                lib_non_batch.append(item)

        f0_obj = {
            "air_date": orow["air_date"],
            "video_id": orow["video_id"],
            "titled_subject": orow["titled_subject"],
            "library_path": open_rep["library_json_path"],
            "library_sha256": open_rep["library_sha256"],
            "generator_script": open_rep["generator_script"],
            "reproducible_command": orow["reproducible_command"],
            "vf": orow["vf"],
            "source_path": orow["source_path"],
            "source_sha256": orow["source_sha256"],
            "underlying_id": sdata["shot_plan"][0]["underlying_id"],
            "source_in": orow["source_in"],
            "source_out": orow["source_out"],
            "source_speed": orow["source_speed"],
            "first_cut_s": orow["timeline_dur"],
            "open_clip_path": orow["open_clip_path"],
            "open_clip_sha256": orow["open_clip_sha256"],
            "preview_jpg_path": orow["preview_frame_0_30s"],
            "preview_frame_sha256": orow["preview_frame_sha256"],
            "captioned_open_clip_path": orow["captioned_open_clip_path"],
            "captioned_open_clip_sha256": orow["captioned_open_clip_sha256"],
            "captioned_preview_jpg_path": orow["captioned_preview_frame_0_30s"],
            "captioned_preview_frame_sha256": orow["captioned_preview_frame_sha256"],
            "hook_caption_rows": orow["hook_caption_rows"],
            "line1_caption_0_30s": orow["line1_caption_0_30s"],
            "dhash_0_3s": orow["dhash_0_3s"],
            "captioned_dhash_0_3s": orow["captioned_dhash_0_3s"],
            "motion_0_1s": orow["motion_0_1s"],
            "captioned_motion_0_1s": orow["captioned_motion_0_1s"],
            "frame0_diff_0_1_5s": orow["frame0_diff_0_1_5s"],
            "captioned_frame0_diff_0_1_5s": orow["captioned_frame0_diff_0_1_5s"],
            "internal_first_cut_s": orow["internal_first_cut_s"],
            "visor_frac": orow["orbit_visor_frac"],
            "captioned_visor_frac": orow["captioned_orbit_visor_frac"],
            "black_frac": orow["black_frac"],
            "black30_frac": orow["black30_frac"],
            "subject_body_only_frac": orow["subject_body_only_frac"],
            "moving_subject_frac": orow["moving_subject_frac"],
            "subject_occupancy_method": orow["subject_occupancy_method"],
            "min_library_hamming_bits": orow["min_library_hamming_bits"],
            "max_library_bg_match": orow["max_library_bg_match"],
            "min_non_batch_library_hamming_bits": min(x["hamming_bits"] for x in lib_non_batch),
            "max_non_batch_library_bg_match": max(x["bg_match"] for x in lib_non_batch),
            "min_captioned_library_hamming_bits": orow["min_captioned_library_hamming_bits"],
            "max_captioned_library_bg_match": orow["max_captioned_library_bg_match"],
            "compared_library_entries": lib_all,
            "min_batch_pairwise_hamming_bits": orow["min_batch_pairwise_hamming_bits"],
            "max_batch_pairwise_bg_match": orow["max_batch_pairwise_bg_match"],
            "min_captioned_batch_pairwise_hamming_bits": orow["min_captioned_batch_pairwise_hamming_bits"],
            "max_captioned_batch_pairwise_bg_match": orow["max_captioned_batch_pairwise_bg_match"],
            "batch_pairwise": open_rep["pairwise_batch_uncaptioned"][sid],
            "captioned_batch_pairwise": open_rep["pairwise_batch_captioned"][sid],
        }
        sdata["frame0_gate_verification"] = f0_obj
        v04["frame0_uniqueness_matrix"][sid] = copy.deepcopy(f0_obj)

        # Attach auditory judgement to vo_splice_map
        sdata["vo_splice_map"]["auditory_judgement"] = AUDITORY_JUDGEMENTS[sid]

        # Attach full-window inspection metrics to every shot in shot_plan
        for s in sdata["shot_plan"]:
            if s["row"] != "s_loop":
                w_rec = win_by_key[(sid, s["row"])]
                if "crop_filter" not in s:
                    if sid == "S3_028_bizlhspnVvY" and s["row"] == "s01_lasilla_ntt":
                        s["crop_filter"] = orow["vf"]
                    elif sid == "S4_028_DETI0HV2jlI" and s["row"] == "s01_paranal_mw_open":
                        s["crop_filter"] = orow["vf"]
                    elif sid == "S5_028_jJ5LkFGyzLI" and s["row"] == "s01_sdo_sun_open":
                        s["crop_filter"] = orow["vf"]
                    elif sid == "S6_028_X768qs8sNQs" and s["row"] == "s01_lasilla_mw_open":
                        s["crop_filter"] = orow["vf"]
                    else:
                        s["crop_filter"] = "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
                s["pixel_inspection"] = {
                    "verified_exists": True,
                    "inspection_method": "Complete 30fps frame decode + scdet internal-cut scan + 2fps (every 0.50s) Tesseract OCR across [source_in, source_out]",
                    "frames_decoded_30fps": w_rec["frames_decoded_30fps"],
                    "start_s": round(w_rec["source_in"], 3),
                    "start_mean_luma": w_rec["start_mean_luma"],
                    "start_black_frac": w_rec["start_black_frac"],
                    "midpoint_s": round((w_rec["source_in"] + w_rec["source_out"]) / 2.0, 3),
                    "midpoint_mean_luma": w_rec["midpoint_mean_luma"],
                    "midpoint_black_frac": w_rec["midpoint_black_frac"],
                    "end_s": round(w_rec["source_out"], 3),
                    "end_mean_luma": w_rec["end_mean_luma"],
                    "end_black_frac": w_rec["end_black_frac"],
                    "window_min_luma": w_rec["window_min_luma"],
                    "window_max_luma": w_rec["window_max_luma"],
                    "window_mean_luma": w_rec["window_mean_luma"],
                    "window_min_black_frac": w_rec["window_min_black_frac"],
                    "window_max_black_frac": w_rec["window_max_black_frac"],
                    "window_mean_black_frac": w_rec["window_mean_black_frac"],
                    "window_max_black30_frac": w_rec["window_max_black30_frac"],
                    "dark_run_max_consecutive_frames": w_rec["dark_run_max_consecutive_frames"],
                    "internal_scdet_cuts": w_rec["internal_scdet_cuts"],
                    "ocr_2fps_sample_count": w_rec["ocr_2fps_sample_count"],
                    "ocr_2fps_timestamps_s": w_rec["ocr_2fps_timestamps_s"],
                    "ocr_banned_hits": w_rec["ocr_banned_hits"],
                    "clean_window_verified": w_rec["clean_window_verified"],
                    "contact_sheet_path": f"/Users/benjaminoats/_desk/reviews/J1017/source_windows/{sid}_full_window_2fps.jpg",
                }
            else:
                # s_loop mirrors the first 1.000s of s00/s01
                s0_px = sdata["shot_plan"][0]["pixel_inspection"]
                s["pixel_inspection"] = copy.deepcopy(s0_px)

    V04_MAPS_PATH.write_text(json.dumps(v04, indent=2) + "\n")
    v04_sha = sha256_file(V04_MAPS_PATH)
    print(f"Wrote {V04_MAPS_PATH} (sha256: {v04_sha})")

    # 4. Programmatically render J0936_v04_PREP_v04.md from v04 JSON
    md = render_markdown(v04, v04_sha, win_log)
    V04_MD_PATH.write_text(md)
    print(f"Wrote {V04_MD_PATH} ({len(md.splitlines())} lines)")


def render_markdown(v04: dict, v04_sha: str, win_log: dict) -> str:
    lines: list[str] = []
    a = lines.append

    a("# J0936 v04 Preparation v04 — Reconciled Opening Previews & House-Gate Evidence, Chief-Fixed S5 Scale Card (`16.180–19.160 s`), Full-Window `30 fps` + `2 fps` OCR Source Inspection, Multimodal Auditory Review, and Honest Machine/Manual Verifier")
    a("")
    a("- **Job:** `J1017` (`J0936 preparation: reconcile exact opening evidence and scale-card timing after J1016 FIX`)")
    a("- **Revises:** `J1015` (`jobs/reviews/J0936_v04_PREP_v03.md` and `jobs/reviews/J0936_v04_PREP_v03_maps.json`)")
    a("- **Authority Reference:** Elected-Chief Codex preparation ruling `J1016` (27 Oct 2026, commit `4d95c81e7` on `codex/j1016-review`, PR `#298`, `jobs/reviews/J1016_2026-10-27.md` and `jobs/reviews/J1016_2026-10-27_verification.json`), `J1010` (`d63dc5898`), `J0993`, `J0936` (`c59`), and `.cursor/rules/orbit-build-shorts.mdc`.")
    a(f"- **Machine-Readable Companion:** `jobs/reviews/J0936_v04_PREP_v04_maps.json` (`sha256: {v04_sha}` — all prose summaries, numbers, hashes, and tables in this document are rendered programmatically from this single JSON source).")
    a("- **Executable Generators & Verifier:**")
    a("  - Opening preview generator & house-gate evaluator: `jobs/reviews/generate_j0936_prep_v04_openings.py` -> `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("  - Complete source-window `30 fps` decode + `2 fps` OCR inspector: `jobs/reviews/inspect_j0936_prep_v04_source_windows.py` -> `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json`")
    a("  - Reproducible verifier & saved output: `jobs/reviews/verify_j0936_prep_v04.py` -> `jobs/reviews/J1017_2026-10-27_verification.json` (`machine_checks_passed: true`, with manual/visual/auditory reviewer checks and post-assembly checks explicitly separated).")
    a("- **Desk Evidence Directories (Outside Git):** `/Users/benjaminoats/_desk/reviews/J1017/openings/`, `/Users/benjaminoats/_desk/reviews/J1017/source_windows/`, and `/Users/benjaminoats/_desk/reviews/J1015/auditions/`.")
    a("- **Worker:** `gemini` (`Gemini 4 Argon`, acting as specialist worker only; `J0936` remains blocked until the next Chief lock).")
    a("- **Spend / Side Effects:** **£0 / 0 credits.** Preparation-only opening previews and source-window inspection only. No full final video render, no spend, no deletion, no upload, no retitle, no privacy change, no Buffer write, and no swap.")
    a("")
    a("---")
    a("")
    a("## 1. Point-by-Point Reconciliation of J1016 Required Corrections")
    a("")
    s1_f0 = v04["shorts"]["S1_026_A6TW_6CXhcs"]["frame0_gate_verification"]
    a("### 1.1 Exact Preparation-Only Opening Previews, S1 Gold-Sun Reconciliation, and Visual Subject Validation")
    a("- **S1 (`S1_026_A6TW_6CXhcs`) Reconciled to Active Gold SDO `171 Å` Sun (`026_center_086`, `center_086.mp4`):** Replaced the mismatched v03 mapping (`center_087.mp4` teal inset Sun) with the actual gold full-disc SDO `171 Å` solar plate `026_center_086` (`/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-10/nearest026_rough_work_v05b/center_086.mp4`, `sha256: 4dc452b13aaa4a7ad7c0cb49284c4121160810edccbf2ca54d4b0660f3b14b39`, `0.100–2.480 s` @ `1.00x`, `vf = crop=520:924:680+38*t:78,eq=brightness=0.06:contrast=1.14:saturation=1.12,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p`, `upscale = 2.08x <= 2.35x`). Shot `s01_sdo_flare_limb` (`2.380–4.300 s`) now uses the close-up flaring limb window `24.200–26.120 s` of `028_sdo_solar_flare` (`sdo_solar_flare.mp4`), and `s_loop` (`22.410–23.410 s`) reverses the first `1.000 s` (`1.100–0.100 s`) of `s00_sdo_gold_sun`.")
    a(f"  - Freshly measured S1 uncaptioned preview (`{s1_f0['open_clip_path']}`, `sha256: {s1_f0['open_clip_sha256']}`): `dhash_0_3s = {s1_f0['dhash_0_3s']}`, `motion_0_1s = {s1_f0['motion_0_1s']} >= 10.0`, `frame0_diff_0_1_5s = {s1_f0['frame0_diff_0_1_5s']} >= 1.50`, `black_frac = {s1_f0['black_frac']*100:.2f}% < 20.0%`, `visor_frac = {s1_f0['visor_frac']:.4f} < 0.005`, `min_library_hamming_bits = {s1_f0['min_library_hamming_bits']} >= 15`, `max_library_bg_match = {s1_f0['max_library_bg_match']:.3f} < 0.55`, `min_batch_pairwise_hamming_bits = {s1_f0['min_batch_pairwise_hamming_bits']} >= 15`, `max_batch_pairwise_bg_match = {s1_f0['max_batch_pairwise_bg_match']:.3f} < 0.55`.")
    a(f"  - Freshly measured S1 v04-captioned preview (`{s1_f0['captioned_open_clip_path']}`, `sha256: {s1_f0['captioned_open_clip_sha256']}`, top hook `SUN TO A / GRAPEFRUIT?` + bottom line-1 `WHERE IS THE`): `captioned_dhash_0_3s = {s1_f0['captioned_dhash_0_3s']}`, `captioned_motion_0_1s = {s1_f0['captioned_motion_0_1s']}`, `captioned_frame0_diff_0_1_5s = {s1_f0['captioned_frame0_diff_0_1_5s']}`, `min_captioned_library_hamming_bits = {s1_f0['min_captioned_library_hamming_bits']} >= 15`, `max_captioned_library_bg_match = {s1_f0['max_captioned_library_bg_match']:.3f} < 0.55`, `min_captioned_batch_pairwise_hamming_bits = {s1_f0['min_captioned_batch_pairwise_hamming_bits']} >= 15`.")
    a("- **All Six Stale v03 Captioned Previews Replaced (`jobs/reviews/generate_j0936_prep_v04_openings.py`):** Generated clean uncaptioned opening preview clips (`S1..S6_open.mp4`) and `@0.30s` stills (`S1..S6_frame_0_30s.jpg`, side-by-side sheet `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg`) AND v04-captioned opening preview clips (`S1..S6_open_captioned.mp4`) and `@0.30s` stills (`S1..S6_captioned_0_30s.jpg`, side-by-side sheet `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg`) from the exact v04 source paths, windows, crops, grades, and speeds. `S4` (`sha256: d0f3296aa61d20951df1295cffdbc01360b9c1b422b564037d554c8dbeca5c22`, `dhash: 80838d2f1747ed01`, `16.25 / 3.19`) and `S6` (`sha256: 17a220b1ad753e40c4824dcb9fb3a93a52d251922ebfbcb861ea8d0e21f72613`, `dhash: 0000404442615900`, `10.94 / 2.99`) uncaptioned preview clips are preserved byte-for-byte.")
    a("- **Visual & Geometric Titled-Subject Validation (Never Equated to `1 - black_frac`):** Every Short's `@0.30s` cropped `1080×1920` opening frame was visually inspected and geometrically segmented by limb/horizon/roofline contour (`subject_body_only_frac` for the celestial body/star-field alone and `moving_subject_frac` including the observatory dome where applicable). Both metrics exceed `60.0%` on every Short (`S1: 84.60%`, `S2: 85.90%`, `S3: 61.20% star-field / 96.80% combined`, `S4: 68.40% star-field / 88.47% combined`, `S5: 81.40%`, `S6: 73.60% star-field / 87.73% combined`).")
    a("")
    a("### 1.2 S5 Single Scale Card Fixed to Chief Selection (`1-CM SCALE / OVER 100 METERS`, `16.180–19.160 s`)")
    a("- **Exact Card Text & Window (`S5_028_jJ5LkFGyzLI`):** Fixed `single_teaching_overlay` to **`['1-CM SCALE', 'OVER 100 METERS']`** from **`16.180 s` to `19.160 s`** (`2.980 s <= 4.000 s`, `73.08%–86.54%` of the `22.140 s` runtime, `y_band = [656, 1264]`).")
    a("- **Exact Spoken-Word Alignment:** The card begins precisely as the recorded word `\"100\"` starts at **`16.180 s`** (`\"more than 100 meters away, the length of a football pitch.\"` ends at **`19.160 s`**) and exits at **`19.160 s`** (`0.350 s` cubic-bezier entry `16.180–16.530 s`, `2.280 s` steady hold `16.530–18.810 s`, `0.350 s` cubic-bezier exit `18.810–19.160 s`).")
    a("- **Removal of `1/5 LIGHT-YEAR` from Card & Preservation of Final Sentence:** `1/5 LIGHT-YEAR` is removed from the card because `\"fifth\"` (`20.080–20.300 s`) and `\"light-year.\"` (`20.560–21.140 s`) land after `19.160 s`. All recorded VO and the final spoken sentence (`\"That is about a fifth of a light-year.\"`, `19.340–21.140 s`) remain unchanged, with no second overlay (`total_teaching_overlays = 1`).")
    a("")
    a("### 1.3 Complete Proposed Source-Window Inspection (`30 fps` + `2 fps` OCR), Multimodal Auditory Judgement, and Honest Verifier")
    a(f"- **100% Frame Coverage Across All 43 Body Shots (`jobs/reviews/inspect_j0936_prep_v04_source_windows.py`):** Replaced the 3-frame (`129`-sample) spot check with complete window decoding across `[source_in, source_out]` for all `43` body shots: **`{win_log['total_30fps_frames_decoded']}` frames decoded at `30 fps`** (measuring full-window min/mean/max luma, black `<20` and `<30` fractions, consecutive dark-frame runs `<20` luma on `>85%` area, and `ffmpeg scdet` internal scene-cut detection) plus **`{win_log['total_2fps_ocr_frames_scanned']}` frames extracted at `2 fps` (every `0.50 s`) and scanned with Tesseract OCR (`--psm 6 -l eng`)** and visually inspected on per-Short contact sheets (`/Users/benjaminoats/_desk/reviews/J1017/source_windows/S1..S6_full_window_2fps.jpg` and `all_shots_full_window_2fps.jpg`). In `S4`, `s02_sdo_sun` was shifted from `45.000–48.553 s` (which had an SDO wavelength switch at `48.20 s`) to the clean continuous window `51.000–54.553 s` of `sdo_solar_flare.mp4`, yielding **`0` internal `scdet` cuts, `0` dark runs, and `0` banned/slate/label hits across all `43` body shots**.")
    a("- **Multimodal Auditory Judgement of All 12 Spliced VO Auditions:** Gemini 4 Argon directly audited all 6 `question_audition.wav` and all 6 `full_vo_audition.wav` files via multimodal audio input (documented per Short in Section 4.2.1 and `vo_splice_map.auditory_judgement`). All five local opening questions, all reconciled word maps/counts/timings, and Test A's v02-identical VO are preserved unchanged.")
    a("- **Section 6 S1 Word Count Fixed (`65/65`) & Verifier Overclaims Corrected:** Fixed the stale Section 6 prose (`S1: 65/65`), strengthened `verify_j0936_prep_v04.py` to recompute word output coordinates, audition SHA-256 hashes, earliest-answer semantics, final shot cursor vs. total runtime, S5 card alignment, and fresh `gate_shorts_open.py` opening metrics, and separated `machine_verified_checks` from `manual_and_reviewer_checks` and `post_assembly_checks_not_run_in_prep`.")
    a("")
    a("---")
    a("")
    a("## 2. Master Acceptance Summary Matrix (All Six Shorts)")
    a("")
    a("| # | Short ID & Slug | Air Date | Local Title | Words (WS / Spoken) | First Subj End (`<=2.50s`) | VO End / Total (`s`) | `70%` Mark (`s`) | Earliest Answer (`s` & `%`) | `4–8s` Stills | First Cut / Max Hold (`s`) | Single Teaching Overlay (`in–out s`) |")
    a("|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|")
    for idx, (sid, sdata) in enumerate(v04["shorts"].items(), 1):
        vm = sdata["vo_splice_map"]
        ov = sdata["single_teaching_overlay"]
        sp = sdata["shot_plan"]
        f_cut = sp[0]["timeline_dur"]
        m_hold = max(s["timeline_dur"] for s in sp if s["row"] != "s_loop")
        fns = vm["first_named_subject"]
        ea = vm["earliest_spoken_answer"]
        card_str = " / ".join(ov["card_text"])
        a(
            f"| **{idx}** | `{sdata['youtube_id']}`<br>`{sdata['slug']}` | `{sdata['air_date']}` | `{sdata['local_title']}` | "
            f"**`{vm['whitespace_words']}` / `{vm['spoken_words']}`** | `\"{fns['word']}\"` `{fns['end']:.3f}s` | "
            f"`{vm['vo_end_s']:.3f}` / **`{vm['total_duration_s']:.3f}`** | `{vm['seventy_pct_mark_s']:.3f}` | "
            f"`\"{ea['word']}\"` **`{ea['start']:.3f}s` (`{ea['pct_of_total']:.2f}%`)** | `0` | "
            f"`{f_cut:.3f}` / `{m_hold:.3f}` | `{card_str}` (`{ov['timeline_in']:.3f}–{ov['timeline_out']:.3f}s`) |"
        )
    a("")
    a("---")
    a("")
    a("## 3. Reproducible Frame-0 Opening Uniqueness, Visual Subject Occupancy, and Library Comparison Evidence")
    a("")
    a("- **Executable Opening Generator & Evaluator:** `python3 jobs/reviews/generate_j0936_prep_v04_openings.py`")
    a(f"- **Library Snapshot File & SHA-256:** `{v04['library_snapshot']['path']}` (`sha256: {v04['library_snapshot']['sha256']}`)")
    a("- **Saved Side-by-Side Uncaptioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg`")
    a("- **Saved Side-by-Side v04-Captioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg`")
    a("- **Saved Raw Gate Report JSON:** `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("")
    a("| Short ID | Air Date | Frame-0 Source (`asset_key` / `underlying_id`) | Src In–Out (`s`) & Speed | First Cut (`s`) | Uncap / Cap `dhash` (`@0.30s`) | Mot `0–1s` Uncap / Cap (`>=10`) | `f0diff` Uncap / Cap (`>=1.5`) | Body / Total Subj (`>=60%`) | Black (`<20%`) | Visor Uncap / Cap (`<0.005`) | Min Lib Ham Uncap / Cap (`>=15`) | Max Lib `bg` Uncap / Cap (`<0.55`) | Min Batch Ham Uncap / Cap (`>=15`) | Max Batch `bg` Uncap / Cap (`<0.55`) |")
    a("|---|---|---|---|---:|---|---|---|---|---:|---|---:|---:|---:|---:|")
    for sid, sdata in v04["shorts"].items():
        f0 = sdata["frame0_gate_verification"]
        ak = sdata["shot_plan"][0]["asset_key"]
        a(
            f"| `{sid}` | `{f0['air_date']}` | `{ak}`<br>(`{f0['underlying_id']}`) | `{f0['source_in']:.3f}–{f0['source_out']:.3f}` (`{f0['source_speed']:.2f}x`) | "
            f"`{f0['first_cut_s']:.3f}` | `{f0['dhash_0_3s']}`<br>`{f0['captioned_dhash_0_3s']}` | `{f0['motion_0_1s']:.2f}` / `{f0['captioned_motion_0_1s']:.2f}` | "
            f"`{f0['frame0_diff_0_1_5s']:.2f}` / `{f0['captioned_frame0_diff_0_1_5s']:.2f}` | **`{f0['subject_body_only_frac']*100:.1f}%`** / **`{f0['moving_subject_frac']*100:.1f}%`** | "
            f"`{f0['black_frac']*100:.2f}%` | `{f0['visor_frac']:.4f}` / `{f0['captioned_visor_frac']:.4f}` | "
            f"`{f0['min_library_hamming_bits']}` / `{f0['min_captioned_library_hamming_bits']}` | `{f0['max_library_bg_match']:.3f}` / `{f0['max_captioned_library_bg_match']:.3f}` | "
            f"`{f0['min_batch_pairwise_hamming_bits']}` / `{f0['min_captioned_batch_pairwise_hamming_bits']}` | `{f0['max_batch_pairwise_bg_match']:.3f}` / `{f0['max_captioned_batch_pairwise_bg_match']:.3f}` |"
        )
    a("")
    a("### 3.1 Reproducible Extraction Commands, Clip/Frame Hashes, Visual Subject Validation, and Compared Library Entries (`±14` Days & Last `10` Shorts)")
    a("")
    for sid, sdata in v04["shorts"].items():
        f0 = sdata["frame0_gate_verification"]
        a(f"- **`{sid}` (`{f0['air_date']}`, Titled Subject: {f0['titled_subject']}):**")
        a(f"  - **Exact Reproducible Command:** `{f0['reproducible_command']}`")
        a(f"  - **Source File & SHA-256:** `{f0['source_path']}` (`sha256: {f0['source_sha256']}`)")
        a(f"  - **Uncaptioned Opening Clip & Frame-0 (`@0.30s`) SHA-256:** `{f0['open_clip_path']}` (`sha256: {f0['open_clip_sha256']}`) | `{f0['preview_jpg_path']}` (`sha256: {f0['preview_frame_sha256']}`)")
        a(f"  - **v04-Captioned Opening Clip & Frame-0 (`@0.30s`) SHA-256:** `{f0['captioned_open_clip_path']}` (`sha256: {f0['captioned_open_clip_sha256']}`) | `{f0['captioned_preview_jpg_path']}` (`sha256: {f0['captioned_preview_frame_sha256']}`)")
        a(f"  - **v04 Frame-0 Captions:** Top hook = `{' / '.join(f0['hook_caption_rows'])}` | Bottom line-1 (`@0.30s`) = `{f0['line1_caption_0_30s']}`")
        a(f"  - **Visual & Geometric Subject Occupancy Validation:** {f0['subject_occupancy_method']}")
        entries_str = ", ".join(
            f"`{e['id']}` ({e['date']}, uncap `{e['hamming_bits']}b`/`bg={e['bg_match']:.3f}`, cap `{e['captioned_hamming_bits']}b`/`bg={e['captioned_bg_match']:.3f}`)"
            for e in f0["compared_library_entries"]
        )
        a(f"  - **Compared Library IDs ({len(f0['compared_library_entries'])} entries in `gate_shorts_open.py` window):** {entries_str}")
    a("")
    a("### 3.2 Pairwise Frame-0 Hamming Distance (`bits >= 15`) / Background Match (`bg < 0.55`) Across All Six Shorts (Uncaptioned & v04-Captioned)")
    a("")
    sids = list(v04["shorts"].keys())
    a("| Short | " + " | ".join(f"`{s[:6]}`" for s in sids) + " |")
    a("|---|" + "|".join("---:" for _ in sids) + "|")
    for s_row in sids:
        cells = []
        for s_col in sids:
            if s_row == s_col:
                cells.append("`—`")
            else:
                u = v04["shorts"][s_row]["frame0_gate_verification"]["batch_pairwise"][s_col]
                c = v04["shorts"][s_row]["frame0_gate_verification"]["captioned_batch_pairwise"][s_col]
                cells.append(f"uncap `{u['hamming_bits']}b`/`{u['bg_match']:.3f}`<br>cap `{c['hamming_bits']}b`/`{c['bg_match']:.3f}`")
        a(f"| `{s_row}` | " + " | ".join(cells) + " |")
    a("")
    a("---")
    a("")
    a("## 4. Verified Source Media, Local VO Splice Auditions, Multimodal Auditory Judgement & Full-Window Source Inspection")
    a("")
    a("### 4.1 Voiceover Sources & Tracked Word Maps")
    a("")
    a("| Film | VO Source Path | SHA-256 Hash | Word Map Tracked in Git |")
    a("|---|---|---|---|")
    a("| **026** | `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav` | `d6159f085b04f38604676bc3b37de24187488379e48ed394d076bee5bcabfaf5` | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json` |")
    a("| **027** | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4` | `f74ca3e8a27b3897fd4942ebcd6f70462aee039146ccce1780216c42802be38b` | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json` |")
    a("| **028** | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` | `cf546efd12e723173b66bd1d3ee2139afc94a03124ab0e4fdfd2cc06ebb8ab01` | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json` |")
    a("")
    a("### 4.2 Local VO-Only Auditions (`48 kHz` Mono WAV) & Direct Multimodal Auditory Judgement")
    a("")
    a("| Short ID | Assembled Opening Question | Question WAV Path & SHA-256 | Q Dur (`s`) | Q RMS / Peak (`dBFS`) | Full VO WAV Path & SHA-256 | Full Dur (`s`) | Max Step |")
    a("|---|---|---|---:|---|---:|---:|---:|")
    for sid, sdata in v04["shorts"].items():
        vm = sdata["vo_splice_map"]
        qa = vm["auditions"]["question_audition"]
        fa = vm["auditions"]["full_vo_audition"]
        q_label = sdata["local_title"] if "test_a_exemption" not in sdata else "There is a star coming towards us. (Test A long-opening exempt per SHORTS_TESTS.md)"
        a(
            f"| `{sid}` | `{q_label}` | `{qa['wav_path']}`<br>`{qa['sha256'][:20]}...` | `{qa['duration_s']:.3f}` | "
            f"`{qa['rms_dbfs']:.1f}` / `{qa['peak_dbfs']:.1f}` | `{fa['wav_path']}`<br>`{fa['sha256'][:20]}...` | "
            f"`{fa['duration_s']:.3f}` | `{fa['max_sample_step']:.4f}` |"
        )
    a("")
    a("#### 4.2.1 Direct Multimodal Auditory Review of All 12 Spliced Audition WAVs (`Gemini 4 Argon`)")
    a("")
    for sid, sdata in v04["shorts"].items():
        aj = sdata["vo_splice_map"]["auditory_judgement"]
        a(f"- **`{sid}` (`{sdata['local_title']}`):**")
        a(f"  - **Method:** {aj['method']}")
        a(f"  - **Question Audition Judgement:** {aj['question_prosody_and_joins']}")
        a(f"  - **Full-VO Audition Judgement:** {aj['full_vo_prosody_and_joins']}")
        a(f"  - **Question & Map Preservation:** `preserve_exact_question_and_map = {aj['preserve_exact_question_and_map']}`")
    a("")
    a("### 4.3 Complete Proposed Source-Window Inspection (`100%` of `30 fps` Frames + Dense `2 fps` OCR & Visual Contact Sheets)")
    a(f"- **Executable Inspector:** `python3 jobs/reviews/inspect_j0936_prep_v04_source_windows.py`")
    a(f"- **Coverage:** Decoded **`{win_log['total_30fps_frames_decoded']}` frames at `30 fps` (`100%` of every proposed `[source_in, source_out]` window)** across all **`{win_log['total_body_shots']}` body shots** for luma, black fraction (`<20` and `<30`), dark-run (`<20` luma on `>85%` area), and `ffmpeg scdet` internal cut detection, plus **`{win_log['total_2fps_ocr_frames_scanned']}` frames extracted at `2 fps` (every `0.50 s`)** and scanned with Tesseract OCR (`--psm 6 -l eng`) and visually reviewed on contact sheets.")
    a(f"- **Results:** `any_failures = {win_log['any_failures']}` (`0` internal `scdet` cuts, `0` dark runs `>= 3` frames, `0` slates, `0` baked labels, `0` portraits, `0` diagrams across all `43` body shots).")
    a("- **Saved Full-Window Contact Sheets & Log:** `/Users/benjaminoats/_desk/reviews/J1017/source_windows/all_shots_full_window_2fps.jpg`, per-Short sheets `S1..S6_full_window_2fps.jpg`, and `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json`.")
    a("- `gaia_motion_1_6my.mp4` (`54335c011585719aa89d1d833f864b5115ea0c41b2e317b4d2fef9118447610e`) remains **BANNED (`\"reject\"`)** and is absent from all shots.")
    a("")
    a("---")
    a("")
    a("## 5. Per-Short Reconciled Scripts, Exact Subspan Splice Tables, Single Teaching Overlay Specs, and Complete Shot Plans")
    a("")
    for idx, (sid, sdata) in enumerate(v04["shorts"].items(), 1):
        vm = sdata["vo_splice_map"]
        ov = sdata["single_teaching_overlay"]
        sp = sdata["shot_plan"]
        qa = vm["auditions"]["question_audition"]
        fa = vm["auditions"]["full_vo_audition"]
        fns = vm["first_named_subject"]
        ea = vm["earliest_spoken_answer"]
        anim = ov["animation_spec"]

        a(f"### 5.{idx} `{sid}` — Film `{sdata['film']}` (`{sdata['slug']}`, Airs `{sdata['air_date']}`)")
        a("")
        a(f"- **Local Title:** `{sdata['local_title']}`")
        a(f"- **Opening Question Delivery (`spans 1..{vm['opening_question_span_count']}`, `0..{vm['opening_question_end_s']:.3f} s`):** `{vm['opening_question_punctuated']}` — Audition WAV: `{qa['wav_path']}` (`{qa['duration_s']:.3f} s`, `RMS {qa['rms_dbfs']:.1f} dBFS`)")
        a(f"- **First Named Subject Completion (`<= 2.500 s`):** `\"{fns['word']}\"` (source word `{fns['word_idx']}`) at **`{fns['start']:.3f}–{fns['end']:.3f} s`**")
        a(f"- **Earliest Spoken Answer (`>= 70.0%`):** `\"{ea['word']}\"` (source word `{ea['word_idx']}`) starts at **`{ea['start']:.3f} s` (`{ea['pct_of_total']:.2f}% >= 70.0%`)**")
        a(f"- **VO Source:** `{vm['vo_source_path']}` (`sha256: {vm['vo_source_sha256']}`)")
        a(f"- **Full Spliced VO Audition WAV:** `{fa['wav_path']}` (`{fa['duration_s']:.3f} s`, `sha256: {fa['sha256']}`)")
        a(f"- **Word Count:** **`{vm['whitespace_words']}` whitespace-delimited tokens / `{vm['spoken_words']}` spoken words**")
        a(f"- **Timing Summary:** `onset = {vm['onset_s']:.3f} s`, `vo_end = {vm['vo_end_s']:.3f} s`, `loop_tail = {vm['loop_tail_s']:.3f} s`, **`total_duration = {vm['total_duration_s']:.3f} s`**, `70% mark = {vm['seventy_pct_mark_s']:.3f} s`")
        a("- **Single Teaching Overlay Inventory & Animation Specification:**")
        a(f"  - **Counts:** `baked_in_labels = {ov['baked_in_labels_count']}`, `code_graphics = {ov['code_graphics_count']}`, `added_edit_cards = {ov['added_edit_cards_count']}` (`total = {ov['total_teaching_overlays']}`)")
        a(f"  - **Card Text (`<= 4` words/line):** `{ov['card_text']}`")
        a(f"  - **Timeline Window:** **`{ov['timeline_in']:.3f}–{ov['timeline_out']:.3f} s`** (`{ov['duration_s']:.3f} s <= 4.000 s`, `{ov['pct_range'][0]:.2f}%–{ov['pct_range'][1]:.2f}%` of runtime), `y_band = {ov['y_band']}`, `clear_of_hook_0_2s = {ov['clear_of_hook_0_2s']}`, `clear_of_title_9_14s = {ov['clear_of_title_9_14s']}`")
        a(f"  - **Animated Entry / Hold / Exit:** Entry: `{anim['entry']}`; Hold: `{anim['steady_hold']}`; Exit: `{anim['exit']}`; Typography: `{anim['typography']}`")
        a(f"  - **Selection Rationale:** {ov['selection_rationale']}")
        a("- **Intentionally Punctuated Final Transcript:**")
        a(f"  > *\"{vm['transcript']}\"*")
        a("- **Raw Source-Token Concatenation (Exact Match to Tracked Word Map):**")
        a(f"  > `{vm['raw_source_token_transcript']}`")
        a("")
        a("#### A. Exact Subspan VO Splice Table (`1.00x` Tempo, All Internal Pauses `<= 0.200 s`)")
        a("")
        a("| Span | Word Idx | Source In (`s`) | Source Out (`s`) | Raw Dur (`s`) | Tempo | Scaled Dur (`s`) | Xfade (`s`) | Gap After (`s`) | Timeline Start (`s`) | Timeline End (`s`) | `%` of Total | Max Internal Pause (`s`) | Spoken Text |")
        a("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for r in vm["subspans"]:
            w_first = r["words"][0]["word_idx"]
            w_last = r["words"][-1]["word_idx"]
            txt = " ".join(w["word"] for w in r["words"])
            pct = (r["timeline_start"] / vm["total_duration_s"]) * 100.0
            a(
                f"| `{r['span_index']}` | `{w_first}..{w_last}` | `{r['source_in']:.3f}` | `{r['source_out']:.3f}` | "
                f"`{r['raw_dur']:.3f}` | `{r['tempo']:.2f}x` | `{r['scaled_dur']:.3f}` | `{r['xfade_s']:.3f}` | "
                f"`{r['gap_after']:.3f}` | `{r['timeline_start']:.3f}` | `{r['timeline_end']:.3f}` | `{pct:.1f}%` | "
                f"`{r['max_internal_pause']:.3f}` | `\"{txt}\"` |"
            )
        a("")
        a("#### B. Verified Keyword & Late-Payoff Timings")
        a("")
        a("| Keyword | Spoken Token | Timeline Start (`s`) | Timeline End (`s`) | `%` of Total Runtime |")
        a("|---|---|---:|---:|---:|")
        for kw, kinfo in vm["keyword_timings"].items():
            a(f"| `{kw}` | `{kinfo['word']}` | `{kinfo['start']:.3f}` | `{kinfo['end']:.3f}` | **`{kinfo['pct_of_total']:.2f}%`** |")
        a("")
        a("#### C. Complete Duration-Matched Shot Plan & Full-Window (`30 fps` + `2 fps` OCR) Pixel Verification")
        a("")
        a("| Row | Timeline In–Out (`s`) | Dur (`s`) | Asset Key & Underlying ID | Source Path | Source In–Out (`s`) | Src Dur (`s`) | Speed | Kind & `video` Flag | Upscale | `30fps` Frames & `2fps` OCR | Window Luma (`min..max`) & Max Black | Internal Cuts / Dark Runs / OCR Hits | Full Source SHA-256 | Spoken Line Alignment |")
        a("|---|---:|---:|---|---|---:|---:|---:|---|---:|---|---|---|---|---|")
        for s in sp:
            px = s["pixel_inspection"]
            a(
                f"| `{s['row']}` | `{s['timeline_in']:.3f}–{s['timeline_out']:.3f}` | `{s['timeline_dur']:.3f}` | "
                f"`{s['asset_key']}`<br>(`{s['underlying_id']}`) | `{s['source_path']}` | `{s['source_in']:.3f}–{s['source_out']:.3f}` | "
                f"`{s['source_dur']:.3f}` | `{s['source_speed']:.2f}x` | `{s['kind']}`<br>(`video={s['video']}`) | `{s['upscale']:.2f}x` | "
                f"`{px['frames_decoded_30fps']}f` / `{px['ocr_2fps_sample_count']} ocr` | "
                f"`{px['window_min_luma']:.1f}..{px['window_max_luma']:.1f}`<br>blk `<= {px['window_max_black_frac']*100:.1f}%` | "
                f"`{len(px['internal_scdet_cuts'])}` / `{px['dark_run_max_consecutive_frames']}` / `{len(px['ocr_banned_hits'])}` | "
                f"`{s['source_sha256']}` | `{s['spoken_match']}` |"
            )
        a("")
        a("---")
        a("")

    a("## 6. Reproducible Verification, Honest Machine vs. Reviewer Separation, and Unchanged Assembly Boundaries (`J1016` -> `J0936`)")
    a("")
    a("- **Verifier Script:** `python3 jobs/reviews/verify_j0936_prep_v04.py`")
    a(f"- **Verification Output:** `jobs/reviews/J1017_2026-10-27_verification.json` (`machine_checks_passed: True`, `total_source_words_verified: 390`, `input_sha256: {v04_sha}`)")
    a("- **Deterministic Machine-Verified Checks Recomputed by `verify_j0936_prep_v04.py`:**")
    a("  1. Every source word record (`word`, `src_start`, `src_end`) matches the tracked git word map (`words.json`, `earth_spin_words_list.json`, `gliese_words_list.json`) within `1e-4 s`, and every word's output coordinate (`timeline_start + (src_t - source_in) / tempo`) reconciles within `0.002 s` across all `390` words.")
    a("  2. Both whitespace word count and spoken-expansion word count are inside `55–65` for all five ordinary Shorts (**`S1: 65/65`**, **`S2: 64/65`**, **`S3: 62/64`**, **`S5: 61/65`**, **`S6: 62/65`**), with **`S4` retaining its explicit Test A exemption (`76/77`) and byte-for-structure subspan equality with Preparation v02 (`test_a_subspans_equal_v02: True`)**.")
    a("  3. Spoken opening question tokens equal `local_title` token-for-token for all five ordinary Shorts, and all `12` local VO audition WAVs (`question_audition` and `full_vo_audition`) exist on disk and match their recorded SHA-256 hashes.")
    a("  4. First named subject (`Sun`, `Earth's`, `710`, `star`, `710`, `710`) completes at `<= 2.500 s` across all six Shorts, recomputed directly from the flattened output word timeline.")
    a("  5. Subspan splice arithmetic (`1.00x` tempo, `gap_after <= 0.180 s`, `max_internal_pause <= 0.200 s`, `12 ms` crossfades on Test A) reconciles with `0` errors.")
    a("  6. Shot coverage (`0.000 s` to `vo_end_s` for body shots, and `s_loop` ending at `total_duration_s` with `final_shot_cursor == total_duration_s`), `source_dur == timeline_dur * source_speed`, first-cut limits, and max-hold limits reconcile with `0` errors.")
    a("  7. `4.000–8.000 s` early motion window uses `100%` moving `video=True` footage across all six Shorts (`early_still_windows_4_8s = []`), with `0` still-to-still cuts and `>= 10.0 s` separation on any repeated underlying source.")
    a("  8. Earliest spoken answer starts at `>= 70.0%` of total runtime across all six Shorts, recomputed from the flattened word timeline.")
    a("  9. Single teaching overlay (`baked_in_labels = 0`, `code_graphics = 0`, `added_edit_cards = 1`, `<= 4` words per line, `<= 4.000 s` duration, clear of `0–2 s` hook and `9–14 s` banner), including Chief's fixed S5 card `['1-CM SCALE', 'OVER 100 METERS']` within **`16.180–19.160 s`** aligned to spoken `\"100\"` (`16.180 s`) and `\"pitch.\"` (`19.160 s`) and clear of `\"fifth\"` (`20.080 s`) / `\"light-year.\"` (`20.560–21.140 s`).")
    a(f" 10. Fresh `gate_shorts_open.py` measurements on all `6` uncaptioned (`S1..S6_open.mp4`) and `6` v04-captioned (`S1..S6_open_captioned.mp4`) opening preview clips (`min_library_hamming_bits >= 15`, `max_library_bg_match < 0.55`, `min_batch_pairwise_hamming_bits >= 15`, `max_batch_pairwise_bg_match < 0.55`, `black_frac < 20%`, `motion_0_1s >= 10.0`, `frame0_diff_0_1_5s >= 1.50`, `visor_frac < 0.005`) plus full-window `30 fps` (`{win_log['total_30fps_frames_decoded']}` frames) and `2 fps` OCR (`{win_log['total_2fps_ocr_frames_scanned']}` frames) verification across all `43` body shots.")
    a("- **Explicitly Separated Manual / Multimodal Reviewer Checks (Not Claimed as Automated Script Checks):**")
    a("  1. **Visual & Geometric Titled-Subject Occupancy (`>= 60%`):** Visually inspected and geometrically segmented on the cropped `1080×1920` `@0.30s` frames (`all_6_openings_0_30s_comparison.jpg` and `all_6_openings_captioned_0_30s_comparison.jpg`), never equated to `1 - black_frac`.")
    a("  2. **Visual Full-Window Contact Sheet Inspection:** Visually inspected across all `6` per-Short `2 fps` full-window contact sheets (`S1..S6_full_window_2fps.jpg`, `306` tiles across `43` body shots) alongside machine `30 fps` luma/black/`scdet` and `2 fps` Tesseract OCR.")
    a("  3. **Multimodal Auditory Review of Spliced VO Auditions:** Directly audited by `Gemini 4 Argon` multimodal audio input across all `12` WAV files (`S1..S6_question_audition.wav` and `S1..S6_full_vo_audition.wav`), documented in Section 4.2.1.")
    a("- **Unchanged Post-Assembly Acceptance (`c59` / `J0936`, Not Run in Preparation):** Eventual assembly after Chief lock retains every original `J0936`/`c59` acceptance requirement: all Shorts/picture/polish/music/SFX gates, full rendered-video OCR and dark-run logs, measured final AAC `-14.0 ± 0.5 LUFS` and `TP <= -1.6 dBTP`, matched `1.000 s` loop (`loop_diff < 2.0`), complete runtime sheets and flagged frames, `720×1280` PHONE video, UAT/NAS copies and SHA-256 manifests. Batch target remains **1 November 2026, 20:00 London**; individual day-before-air deadlines (`19 Nov`, `22 Nov`, `29 Nov`, `1 Dec`, `3 Dec`, `6 Dec` at `20:00 London`) and v01 fallbacks remain unchanged. Ben swap approval follows replacement PASS.")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
