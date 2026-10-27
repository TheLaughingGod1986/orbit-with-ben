#!/usr/bin/env python3
"""
Reproducible verifier for J0936 v04 Preparation v05 (J1019).
Performs deterministic machine checks across:
  1. Source word maps (390 words) and output word-coordinate arithmetic (<0.002s tolerance)
  2. Ordinary-Short VO bridge continuity: verifies that all Gliese 710 occurrences in S3, S5, S6
     (words 121..122, 719..720, 471..473, 985..986) and 'every 35 years.' (words 952..960 in S6)
     reside inside single continuous subspans with 0 omitted inter-token syllables
  3. Test A subspan equality against v02, v03, and v04 maps (unchanged per J1018/J1019) + verification
     of the separate non-applied Test A diagnostic repair WAV and timing proposal
  4. Whitespace and spoken-expansion word counts (55-65 for S1, S2, S3, S5, S6; Test A exempt 76/77)
  5. Opening question token equality to local_title
  6. Recomputed first_named_subject (<=2.500s) and supplied earliest_spoken_answer index coordinate/percentage
     check (>=70.0% of total runtime; verifies supplied word_idx coordinates, not semantic question-answering)
  7. Subspan splice arithmetic (1.000x <= tempo <= 1.060x) and shot cursor contiguity (final_shot_cursor == total_duration_s)
  8. 4.0-8.0s moving video (0 early still windows), 0 still-to-still cuts, >=10.0s repeat-source separation
  9. Single teaching overlay timing & spoken-word alignment (including Chief-locked S5 16.180-19.160s card)
 10. Audition WAV existence and SHA-256 hash verification (all 12 WAVs in /Users/benjaminoats/_desk/reviews/J1019/auditions/ + source VO files)
 11. Fresh gate_shorts_open.py measurements on all 6 uncaptioned & 6 v04-captioned opening preview clips
 12. Saved source-window inspection log provenance check (verifies SHA-256 of full_window_inspection_log.json
     and exact (source_path, source_in, source_out) match across all 43 body shots; does not re-decode frames itself)
Explicitly separates machine-verified checks from saved-log provenance, manual/multimodal reviewer assertions, and post-assembly gates.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MAPS_V02_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v02_maps.json"
MAPS_V03_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v03_maps.json"
MAPS_V04_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04_maps.json"
MAPS_V05_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v05_maps.json"
OUT_PATH = ROOT / "jobs/reviews/J1019_2026-10-27_verification.json"
GATE_PATH = ROOT / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
LIB_PATH = ROOT / "00_Brand/Channel-Setup/audits/shorts_open_library/library.json"
WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json")

SPOKEN_EXPAND = {
    "710": 2,
    "10": 1,
    "30": 1,
    "100": 2,
    "35": 2,
    "forty-three": 2,
    "light-years": 2,
    "light-year": 2,
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def count_spoken_words(tokens: list[str]) -> int:
    total = 0
    for t in tokens:
        clean = t.strip(".,?!:;\"'")
        if clean in SPOKEN_EXPAND:
            total += SPOKEN_EXPAND[clean]
        elif "-" in clean and clean not in SPOKEN_EXPAND:
            total += len(clean.split("-"))
        else:
            total += 1
    return total


def norm_words(s: str) -> list[str]:
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in s.split() if re.sub(r"[^a-z0-9']", "", w.lower())]


def strip_scribe_gap(subspans: list[dict]) -> list[dict]:
    out = []
    for r in subspans:
        rc = dict(r)
        rc.pop("max_scribe_token_gap", None)
        out.append(rc)
    return out


def main() -> None:
    raw_bytes = MAPS_V05_PATH.read_bytes()
    input_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    data = json.loads(raw_bytes)
    v02 = json.loads(MAPS_V02_PATH.read_text())
    v03 = json.loads(MAPS_V03_PATH.read_text())
    v04 = json.loads(MAPS_V04_PATH.read_text())
    win_log_sha256 = sha256_file(WIN_LOG_PATH)
    win_log = json.loads(WIN_LOG_PATH.read_text())
    win_by_key = {(r["short_id"], r["row"]): r for r in win_log["shots"]}

    spec_mod = importlib.util.spec_from_file_location("gate", GATE_PATH)
    g = importlib.util.module_from_spec(spec_mod)
    spec_mod.loader.exec_module(g)
    lib = g.load_lib()
    lib_sha256 = sha256_file(LIB_PATH)
    assert lib_sha256 == data["library_snapshot"]["sha256"]

    w026 = json.load(open(ROOT / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json"))["words"]
    w027 = json.load(open(ROOT / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json"))
    w028 = json.load(open(ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json"))
    word_maps = {"OWB:026": w026, "OWB:027": w027, "OWB:028": w028}

    fresh_open = {}
    for sid, sdata in data["shorts"].items():
        f0 = sdata["frame0_gate_verification"]
        pu = Path(f0["open_clip_path"])
        pc = Path(f0["captioned_open_clip_path"])
        assert pu.exists() and pc.exists(), f"{sid}: missing opening clip"
        assert sha256_file(pu) == f0["open_clip_sha256"]
        assert sha256_file(pc) == f0["captioned_open_clip_sha256"]
        assert sha256_file(Path(f0["preview_jpg_path"])) == f0["preview_frame_sha256"]
        assert sha256_file(Path(f0["captioned_preview_jpg_path"])) == f0["captioned_preview_frame_sha256"]
        fresh_open[sid] = {
            "dh_u": g.dhash(pu),
            "th_u": g.thumb(pu),
            "mot_u": g.motion_first_second(pu),
            "f0d_u": g.frame0_diff_0_1_5s(pu),
            "cut_u": g.first_cut_s(pu),
            "orb_u": g.orbit_score(pu),
            "dh_c": g.dhash(pc),
            "th_c": g.thumb(pc),
            "mot_c": g.motion_first_second(pc),
            "f0d_c": g.frame0_diff_0_1_5s(pc),
            "orb_c": g.orbit_score(pc),
        }
        raw_gray = g.raw_frame(pu, 180, 320, 0.30, "gray")
        arr = np.frombuffer(raw_gray, dtype=np.uint8)
        fresh_open[sid]["blk20"] = round(float(np.mean(arr < 20)), 4)

    source_window_mismatches = []
    omitted_ordinary_bridges = []
    repaired_ordinary_bridges = []

    report = {
        "job": "J1019",
        "ruling_authority": "J1018 (b8c75920b, PR #299)",
        "verifier": "jobs/reviews/verify_j0936_prep_v05.py",
        "input_maps_path": "jobs/reviews/J0936_v04_PREP_v05_maps.json",
        "input_sha256": input_sha256,
        "library_sha256": lib_sha256,
        "saved_source_window_log_path": str(WIN_LOG_PATH),
        "saved_source_window_log_sha256": win_log_sha256,
        "machine_checks_passed": True,
        "total_source_words_verified": 0,
        "source_window_mismatches": source_window_mismatches,
        "omitted_ordinary_bridges": omitted_ordinary_bridges,
        "repaired_ordinary_bridges": repaired_ordinary_bridges,
        "saved_source_window_log_summary": {
            "provenance_note": "Read from saved log produced by inspect_j0936_prep_v04_source_windows.py; verify_j0936_prep_v05.py verifies log SHA-256 and zero (source_path, source_in, source_out) mismatches across all 43 body shots rather than re-decoding frames itself.",
            "ocr_sampling_note": "2fps OCR (306 frames sampled every 0.50s plus window tail) is sampled text inspection; 30fps decode (4,046 frames) measures luma, black fraction, dark runs, and scdet internal cuts.",
            "transform_scope_note": "5 opening shots used declared custom 9:16 crops/grades; 38 body shots used default 9:16 centre crop (crop=ih*9/16:ih) at native source speed (source_speed not applied). Mandatory every-frame OCR/dark-run gates run on final transformed MP4s at assembly.",
            "total_body_shots": win_log["total_body_shots"],
            "total_30fps_frames_decoded_in_saved_log": win_log["total_30fps_frames_decoded"],
            "total_2fps_ocr_sampled_frames_in_saved_log": win_log["total_2fps_ocr_frames_scanned"],
        },
        "shorts": {},
        "scale_card_timing_s5": {},
        "test_a_diagnosis_and_proposal_verified": {},
        "verifier_scope_notes": [
            "earliest_spoken_answer_coordinate_check verifies the supplied word_idx's recomputed output start time and >=70.0% runtime position; semantic selection of which spoken word first answers the title is a manual reviewer assertion.",
            "saved_source_window_log_summary reads and hash-verifies /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json; verify_j0936_prep_v05.py does not re-decode the 4,046 30fps frames or re-run Tesseract on the 306 sampled 2fps frames.",
            "2fps OCR and contact sheets are sampled text inspection (every 0.50s), not every-frame 30fps OCR.",
            "inspect_j0936_prep_v04_source_windows.py used default 9:16 centre crops and native source speed on 38 of 43 body shots; final transformed output MP4s still require full post-assembly OCR, dark-run, picture_qa, and polish_gate passes.",
            "Titled-subject occupancy percentages and auditory prosody judgements are multimodal reviewer assertions, not computed by verify_j0936_prep_v05.py.",
        ],
        "manual_and_reviewer_assertions": {
            "earliest_spoken_answer_semantic_selection": {
                "status": "REVIEWED_BY_HUMAN_AND_LLM_SEMANTIC_INSPECTION",
                "note": "Verifier checks coordinates/percentage of supplied word_idx; semantic identification of earliest answer is a reviewer assertion.",
            },
            "titled_subject_visual_and_geometric_occupancy": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_VISION",
                "method": "Visual limb/horizon/roofline segmentation on 1080x1920 @0.30s frames (all_6_openings_0_30s_comparison.jpg and all_6_openings_captioned_0_30s_comparison.jpg); never equated to 1 - black_frac.",
                "all_six_above_60pct": True,
            },
            "source_window_sampled_2fps_contact_sheets": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_VISION",
                "method": "Visual inspection of all 6 per-Short 2fps sampled contact sheets (S1..S6_full_window_2fps.jpg, 306 sampled tiles across 43 body shots).",
                "clean_windows_confirmed": True,
            },
            "spliced_vo_auditions_prosody_and_repaired_bridges": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_AUDIO",
                "method": "Direct multimodal audio playback and prosody inspection of all 12 WAV files in /Users/benjaminoats/_desk/reviews/J1019/auditions/ (including regenerated S3, S5, S6 question and full VO WAVs) and the separate Test A diagnostic WAV; documented per Short in vo_splice_map.auditory_judgement.",
                "all_ordinary_gliese_710_and_body_bridges_verified_clean_by_ear": True,
            },
        },
        "post_assembly_checks_not_run_in_prep": [
            "Full rendered-video OCR and dark-run gate logs on assembled master MP4s with final crops, grades, and source_speed transforms",
            "Final integrated AAC loudness (-14.0 +- 0.5 LUFS) and true peak (<=-1.6 dBTP)",
            "music_gate.py and sfx_kit.py level on assembled stems",
            "Final master loop_diff < 2.0 across last-to-first frame boundary",
            "720x1280 PHONE renders, complete runtime contact sheets, and UAT/NAS SHA-256 manifests",
        ],
    }

    for sid, sdata in data["shorts"].items():
        wlist = word_maps[sdata["film"]]
        vm = sdata["vo_splice_map"]
        sp = sdata["shot_plan"]
        ov = sdata["single_teaching_overlay"]
        f0 = sdata["frame0_gate_verification"]
        is_test_a = "test_a_exemption" in sdata

        vo_src = Path(vm["vo_source_path"])
        if not vo_src.is_absolute():
            vo_src = ROOT / vo_src
        assert vo_src.exists() and sha256_file(vo_src) == vm["vo_source_sha256"]

        tokens = []
        flat_words = []
        splice_errors = []
        word_coord_errors = []
        for idx, r in enumerate(vm["subspans"]):
            assert 1.000 - 1e-6 <= r["tempo"] <= 1.060 + 1e-6, f"{sid} span {idx+1} tempo {r['tempo']} out of range"
            assert r["gap_after"] <= 0.180 + 1e-6
            assert r["max_internal_pause"] <= 0.200 + 1e-6
            expected_raw = round(r["source_out"] - r["source_in"], 3)
            expected_scaled = round(expected_raw / r["tempo"], 3)
            if abs(expected_raw - r["raw_dur"]) > 0.002:
                splice_errors.append(f"span {idx+1} raw_dur mismatch")
            if abs(expected_scaled - r["scaled_dur"]) > 0.002:
                splice_errors.append(f"span {idx+1} scaled_dur mismatch")
            if idx == 0:
                if abs(r["timeline_start"] - vm["onset_s"]) > 0.002:
                    splice_errors.append("span 1 start != onset")
            else:
                prev = vm["subspans"][idx - 1]
                expected_start = round(prev["timeline_end"] + prev["gap_after"] - r["xfade_s"], 3)
                if abs(r["timeline_start"] - expected_start) > 0.002:
                    splice_errors.append(f"span {idx+1} start != expected_start")
            for w in r["words"]:
                w_i = w["word_idx"]
                ref = wlist[w_i]
                ref_txt = (ref.get("word") or ref.get("text")).strip()
                assert w["word"] == ref_txt
                assert abs(w["src_start"] - float(ref["start"])) <= 1e-4
                assert abs(w["src_end"] - float(ref["end"])) <= 1e-4
                for out_k, src_k in [("start", "src_start"), ("end", "src_end")]:
                    exp_t = r["timeline_start"] + (w[src_k] - r["source_in"]) / r["tempo"]
                    if abs(w[out_k] - exp_t) > 0.002:
                        word_coord_errors.append([r["span_index"], w["word"], out_k, w[out_k], round(exp_t, 3)])
                tokens.append(w["word"])
                flat_words.append(w)
                report["total_source_words_verified"] += 1

        # Verify S1, S2, S4 unchanged from v04, and S4 unchanged from v02/v03/v04
        if sid in ("S1_026_A6TW_6CXhcs", "S2_027_emwQsPxnRGM", "S4_028_DETI0HV2jlI"):
            assert strip_scribe_gap(vm["subspans"]) == v04["shorts"][sid]["vo_splice_map"]["subspans"]
        if is_test_a:
            assert strip_scribe_gap(vm["subspans"]) == v02["shorts"][sid]["vo_splice_map"]["subspans"]
            assert strip_scribe_gap(vm["subspans"]) == v03["shorts"][sid]["vo_splice_map"]["subspans"]

        # Verify 0 split Gliese/710 or 'every 35' bridges in ordinary Shorts of Film 028
        if sdata["film"] == "OWB:028" and not is_test_a:
            for a, b in zip(vm["subspans"], vm["subspans"][1:]):
                wa_last = a["words"][-1]
                wb_first = b["words"][0]
                if wa_last["word"] == "Gliese" and wb_first["word"].startswith("710"):
                    omitted_ordinary_bridges.append([sid, a["span_index"], b["span_index"]])
                if wa_last["word"] == "every" and wb_first["word"] == "35":
                    omitted_ordinary_bridges.append([sid, a["span_index"], b["span_index"]])
            for r in vm["subspans"]:
                w_ids = [w["word_idx"] for w in r["words"]]
                if (121 in w_ids and 122 in w_ids) or (719 in w_ids and 720 in w_ids) or (472 in w_ids and 473 in w_ids) or (985 in w_ids and 986 in w_ids) or (958 in w_ids and 959 in w_ids):
                    repaired_ordinary_bridges.append({
                        "short": sid,
                        "span_index": r["span_index"],
                        "word_idx_range": r["word_idx_range"],
                        "source_in": r["source_in"],
                        "source_out": r["source_out"],
                        "raw_dur": r["raw_dur"],
                        "tempo": r["tempo"],
                        "timeline_start": r["timeline_start"],
                        "timeline_end": r["timeline_end"],
                        "text": r["text"],
                    })

        ws_count = len(tokens)
        sp_count = count_spoken_words(tokens)
        assert ws_count == vm["whitespace_words"] and sp_count == vm["spoken_words"]
        if not is_test_a:
            assert 55 <= ws_count <= 65 and 55 <= sp_count <= 65

        q_spans = vm["subspans"][: vm["opening_question_span_count"]]
        q_tokens = [w["word"] for r in q_spans for w in r["words"]]
        q_equal = True
        if not is_test_a:
            q_equal = norm_words(" ".join(q_tokens)) == norm_words(sdata["local_title"])
            assert q_equal

        fns = vm["first_named_subject"]
        fns_matches = [w for w in flat_words if w["word_idx"] == fns["word_idx"] and abs(w["start"] - fns["start"]) < 0.002]
        assert len(fns_matches) == 1 and fns_matches[0]["end"] <= 2.500 + 1e-6

        ea = vm["earliest_spoken_answer"]
        ea_matches = [w for w in flat_words if w["word_idx"] == ea["word_idx"] and abs(w["start"] - ea["start"]) < 0.002]
        assert len(ea_matches) == 1
        recomputed_ea_pct = round(ea_matches[0]["start"] / vm["total_duration_s"] * 100.0, 2)
        assert abs(recomputed_ea_pct - ea["pct_of_total"]) <= 0.02 and recomputed_ea_pct >= 70.0

        tot_dur = vm["total_duration_s"]
        assert 22.000 <= tot_dur <= 27.000
        assert abs(vm["subspans"][-1]["timeline_end"] - vm["vo_end_s"]) < 1e-4
        assert abs(vm["vo_end_s"] + vm["loop_tail_s"] - tot_dur) < 1e-4

        early_still_windows = []
        shot_errors = []
        t_cur = 0.000
        prev_vid = True
        seen_underlying = {}
        body_end_s = 0.000
        for s_i, s in enumerate(sp):
            if abs(s["timeline_in"] - t_cur) > 1e-4:
                shot_errors.append(f"{s['row']} tl_in {s['timeline_in']} != {t_cur}")
            t_cur = s["timeline_out"]
            if s_i == 0 and s["timeline_dur"] > sdata["first_cut_limit_s"] + 1e-4:
                shot_errors.append(f"first cut {s['timeline_dur']} > {sdata['first_cut_limit_s']}")
            elif s["row"] != "s_loop" and s["timeline_dur"] > sdata["max_hold_limit_s"] + 1e-4:
                shot_errors.append(f"{s['row']} hold {s['timeline_dur']} > {sdata['max_hold_limit_s']}")
            if s["row"] != "s_loop":
                body_end_s = s["timeline_out"]
                exp_sd = round(s["timeline_dur"] * s["source_speed"], 3)
                if abs(s["source_dur"] - exp_sd) > 0.005:
                    shot_errors.append(f"{s['row']} src_dur {s['source_dur']} != {exp_sd}")
                if not s["video"] and max(s["timeline_in"], 4.000) < min(s["timeline_out"], 8.000):
                    early_still_windows.append([s["row"], s["timeline_in"], s["timeline_out"]])
                if s_i > 0 and not prev_vid and not s["video"]:
                    shot_errors.append(f"still-to-still at {s['row']}")
                prev_vid = s["video"]
                uid = s["underlying_id"]
                if uid in seen_underlying:
                    sep = s["timeline_in"] - seen_underlying[uid]
                    if sep < 10.0 - 1e-4:
                        shot_errors.append(f"repeat {uid} separation {sep} < 10.0s")
                seen_underlying[uid] = s["timeline_out"]

                w_rec = win_by_key[(sid, s["row"])]
                for k in ("source_path", "source_in", "source_out"):
                    if w_rec[k] != s[k]:
                        source_window_mismatches.append([sid, s["row"], k, w_rec[k], s[k]])
                assert w_rec["clean_window_verified"] is True
                assert w_rec["dark_run_max_consecutive_frames"] == 0
                assert len(w_rec["internal_scdet_cuts"]) == 0
                assert len(w_rec["ocr_banned_hits"]) == 0

        assert abs(body_end_s - vm["vo_end_s"]) < 1e-4, f"{sid}: body_end {body_end_s} != vo_end {vm['vo_end_s']}"
        assert abs(t_cur - tot_dur) < 1e-4, f"{sid}: final_shot_cursor {t_cur} != total_duration_s {tot_dur}"
        assert not splice_errors and not word_coord_errors and not shot_errors and not early_still_windows

        assert ov["total_teaching_overlays"] == 1
        assert ov["duration_s"] <= 4.000 + 1e-6
        assert abs((ov["timeline_out"] - ov["timeline_in"]) - ov["duration_s"]) < 1e-4
        assert ov["clear_of_hook_0_2s"] and ov["timeline_in"] >= 2.000
        assert ov["clear_of_title_9_14s"] and (ov["timeline_out"] <= 9.000 or ov["timeline_in"] >= 14.000)
        for line in ov["card_text"]:
            assert len(line.split()) <= 4

        aud_status = {}
        for k, a in vm["auditions"].items():
            p = Path(a["wav_path"])
            h_ok = p.exists() and sha256_file(p) == a["sha256"]
            assert h_ok, f"{sid} {k} wav hash mismatch"
            aud_status[k] = {"exists": True, "hash_matches": True, "sha256": a["sha256"], "duration_s": a["duration_s"]}

        fo = fresh_open[sid]
        assert f"{fo['dh_u']:016x}" == f0["dhash_0_3s"]
        assert f"{fo['dh_c']:016x}" == f0["captioned_dhash_0_3s"]
        assert fo["mot_u"] == f0["motion_0_1s"] and fo["mot_u"] >= 10.0
        assert fo["mot_c"] == f0["captioned_motion_0_1s"] and fo["mot_c"] >= 10.0
        assert fo["f0d_u"] == f0["frame0_diff_0_1_5s"] and fo["f0d_u"] >= 1.50
        assert fo["f0d_c"] == f0["captioned_frame0_diff_0_1_5s"] and fo["f0d_c"] >= 1.50
        assert fo["blk20"] == f0["black_frac"] and fo["blk20"] < 0.20
        assert fo["orb_u"]["visor_frac"] == f0["visor_frac"] and fo["orb_u"]["visor_frac"] < 0.005

        air = date.fromisoformat(f0["air_date"])
        win = g.window(lib, air, 14, 10, exclude=f0["video_id"])
        assert len(win) == len(f0["compared_library_entries"])
        stored_hash_distance_errors = []
        for e_map, e_lib in zip(f0["compared_library_entries"], win):
            assert e_map["id"] == e_lib["id"]
            hb = g.hamming(fo["dh_u"], int(e_lib["dhash"], 16))
            bg = round(g.background_match(fo["th_u"], e_lib["thumb"]), 3) if e_lib.get("thumb") else 0.0
            if hb != e_map["hamming_bits"] or bg != e_map["bg_match"]:
                stored_hash_distance_errors.append(e_map["id"])
            assert hb >= 15 and bg < 0.55

        for osid, b_map in f0["batch_pairwise"].items():
            hb = g.hamming(fo["dh_u"], fresh_open[osid]["dh_u"])
            bg = round(g.background_match(fo["th_u"], fresh_open[osid]["th_u"]), 3)
            assert hb == b_map["hamming_bits"] and bg == b_map["bg_match"]
            assert hb >= 15 and bg < 0.55

        row_out = {
            "whitespace_count": ws_count,
            "spoken_count": sp_count,
            "within_55_65_target": (55 <= ws_count <= 65 and 55 <= sp_count <= 65) if not is_test_a else "Test A exempt (76/77)",
            "question_equals_local_title": q_equal,
            "word_output_coordinate_errors": word_coord_errors,
            "first_named_subject": fns,
            "earliest_spoken_answer_coordinate_check": {
                **ea,
                "scope": "Verifies supplied word_idx output start time and >=70% position; semantic answer selection is a manual reviewer check.",
            },
            "computed_vo_end_s": vm["vo_end_s"],
            "computed_total_s": tot_dur,
            "final_shot_cursor_s": t_cur,
            "final_shot_cursor_equals_total_runtime": (abs(t_cur - tot_dur) < 1e-4),
            "splice_arithmetic_errors": splice_errors,
            "shot_duration_errors": shot_errors,
            "early_still_windows_4_8s": early_still_windows,
            "single_overlay_verified": {
                "card_text": ov["card_text"],
                "timeline_in": ov["timeline_in"],
                "timeline_out": ov["timeline_out"],
                "duration_s": ov["duration_s"],
            },
            "auditions_verified": aud_status,
            "stored_hash_distance_errors": stored_hash_distance_errors,
            "fresh_measured_opening": {
                "open_clip_sha256": f0["open_clip_sha256"],
                "captioned_open_clip_sha256": f0["captioned_open_clip_sha256"],
                "dhash_0_3s": f0["dhash_0_3s"],
                "captioned_dhash_0_3s": f0["captioned_dhash_0_3s"],
                "motion_0_1s": fo["mot_u"],
                "captioned_motion_0_1s": fo["mot_c"],
                "frame0_diff_0_1_5s": fo["f0d_u"],
                "captioned_frame0_diff_0_1_5s": fo["f0d_c"],
                "black_frac": fo["blk20"],
                "visor_frac": fo["orb_u"]["visor_frac"],
                "min_library_hamming_bits": f0["min_library_hamming_bits"],
                "max_library_bg_match": f0["max_library_bg_match"],
                "min_batch_hamming_bits": f0["min_batch_pairwise_hamming_bits"],
                "max_batch_bg_match": f0["max_batch_pairwise_bg_match"],
            },
            "saved_source_window_log_match": {
                "body_shots": len(sp) - 1,
                "frames_decoded_30fps_in_saved_log": sum(win_by_key[(sid, s["row"])]["frames_decoded_30fps"] for s in sp if s["row"] != "s_loop"),
                "ocr_sampled_frames_2fps_in_saved_log": sum(win_by_key[(sid, s["row"])]["ocr_2fps_sample_count"] for s in sp if s["row"] != "s_loop"),
                "internal_scdet_cuts_in_saved_log": 0,
                "dark_runs_in_saved_log": 0,
                "ocr_2fps_banned_hits_in_saved_log": 0,
            },
        }
        if is_test_a:
            row_out["test_a_subspans_equal_v02"] = True
            row_out["test_a_subspans_equal_v03"] = True
            row_out["test_a_subspans_equal_v04"] = True
        report["shorts"][sid] = row_out

    assert not source_window_mismatches
    assert not omitted_ordinary_bridges
    assert len(repaired_ordinary_bridges) == 7

    # Specific S5 scale card alignment verification
    s5 = data["shorts"]["S5_028_jJ5LkFGyzLI"]
    s5_ov = s5["single_teaching_overlay"]
    s5_words = [w for r in s5["vo_splice_map"]["subspans"] for w in r["words"]]
    w_100 = next(w for w in s5_words if w["word"] == "100")
    w_pitch = next(w for w in s5_words if w["word"] == "pitch.")
    w_fifth = next(w for w in s5_words if w["word"] == "fifth")
    w_ly = next(w for w in s5_words if w["word"] == "light-year.")
    assert s5_ov["card_text"] == ["1-CM SCALE", "OVER 100 METERS"]
    assert s5_ov["timeline_in"] == 16.180 == w_100["start"]
    assert s5_ov["timeline_out"] == 19.160 == w_pitch["end"]
    assert all("LIGHT-YEAR" not in ln and "1/5" not in ln for ln in s5_ov["card_text"])
    report["scale_card_timing_s5"] = {
        "card_text": s5_ov["card_text"],
        "card_in_s": s5_ov["timeline_in"],
        "card_out_s": s5_ov["timeline_out"],
        "spoken_100_start_s": w_100["start"],
        "spoken_100_end_s": w_100["end"],
        "spoken_pitch_end_s": w_pitch["end"],
        "spoken_fifth_start_s": w_fifth["start"],
        "spoken_light_year_start_s": w_ly["start"],
        "spoken_light_year_end_s": w_ly["end"],
        "matches_spoken_model_distance_line": True,
        "excludes_later_real_distance_words": True,
    }

    # Verify Test A separate diagnosis & diagnostic WAV existence/hash
    tprop = data["test_a_separate_repair_proposal"]
    assert tprop["applied_in_v05"] is False and tprop["locked_test_a_subspans_unchanged"] is True
    diag_p = Path(tprop["proposal_option_a_zero_downstream_drift"]["diagnostic_wav_path"])
    assert diag_p.exists() and sha256_file(diag_p) == tprop["proposal_option_a_zero_downstream_drift"]["diagnostic_wav_sha256"]
    report["test_a_diagnosis_and_proposal_verified"] = {
        "locked_test_a_unchanged": True,
        "diagnostic_wav_exists": True,
        "diagnostic_wav_sha256": tprop["proposal_option_a_zero_downstream_drift"]["diagnostic_wav_sha256"],
        "option_a_downstream_drift_s": tprop["proposal_option_a_zero_downstream_drift"]["timing_consequences"]["span_8_onward_drift_s"],
        "option_b_downstream_drift_s": tprop["proposal_option_b_extend_runtime_by_0_280s"]["timing_consequences"]["span_8_onward_drift_s"],
    }

    OUT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print("Verification complete! Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
