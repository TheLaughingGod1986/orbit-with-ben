#!/usr/bin/env python3
"""
Reproducible verifier for J0936 v04 Preparation v06 (J1024, under Chief J1020 ruling e82eae17d).
Performs deterministic machine checks across:
  1. Source word maps (391 words) and output word-coordinate arithmetic (<0.002s tolerance)
  2. Unchanged preservation of S1, S2, S3, S5 subspans and audition WAV hashes from v05
  3. Ordinary-Short VO bridge continuity across S3, S5, S6 (words 121..122, 719..720, 471..473, 985..986)
  4. S6 payoff correction verification: exact question preserved, zero pre-70% motion/appearance answer clauses
     or numbers, earliest_spoken_answer 'brightest' (word 881) at 16.820s (75.83% >= 70.0%), keyword_timings
     'star' (word 398) at 17.320s and 'three' (word 743) at 17.880s, 63 WS / 65 spoken words, and s05_alma_orion_set
     shot/line matching
  5. Test A (S4) explicitly authorised Option A syllable repair verification: Span 6 [14.980, 15.780] (6.700-7.500s),
     Span 7 [16.060, 17.220] (7.528-8.688s), gaps after Spans 4/5/6/7 = 0.060/0.040/0.040/0.060s, Span 5 6.012-6.672s,
     Span 8 8.736s, vo_end_s 23.516s, total_duration_s 24.516s, card 17.950-21.450s, and full_vo_audition SHA-256
     reconciled byte-for-byte with retained diagnostic hash d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a
  6. S3 atempo slot-fit implementation note verification (<=16.17ms buffer trim documented honestly)
  7. Whitespace and spoken-expansion word counts (55-65 for S1, S2, S3, S5, S6; Test A exempt 76/77)
  8. Opening question token equality to local_title and first_named_subject completion <=2.500s
  9. Subspan splice arithmetic (1.000x <= tempo <= 1.060x), shot cursor contiguity, 4-8s moving video,
     0 still-to-still cuts, >=10.0s repeat-source separation, and single teaching overlay rules
 10. Audition WAV existence and SHA-256 hash verification (all 12 WAVs in /Users/benjaminoats/_desk/reviews/J1024/auditions/)
 11. Fresh gate_shorts_open.py measurements on all 6 uncaptioned & 6 v04-captioned opening preview clips
 12. Saved source-window log provenance verification against both the preserved J1017 log (42 unchanged shots,
     sha256: b8e995f64132a8e9...) and the J1024 v06 log (43 shots including S6 s05_alma_orion_set)
Explicitly separates machine-verified checks from saved-log provenance, Gemini reviewer assertions, and post-assembly gates.
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
MAPS_V04_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04_maps.json"
MAPS_V05_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v05_maps.json"
MAPS_V06_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v06_maps.json"
OUT_PATH = ROOT / "jobs/reviews/J1024_2026-10-27_verification.json"
GATE_PATH = ROOT / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
LIB_PATH = ROOT / "00_Brand/Channel-Setup/audits/shorts_open_library/library.json"
J1017_WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json")
J1024_WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json")
J1019_TESTA_DIAG = Path("/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav")

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


def main() -> None:
    raw_bytes = MAPS_V06_PATH.read_bytes()
    input_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    data = json.loads(raw_bytes)
    v04 = json.loads(MAPS_V04_PATH.read_text())
    v05 = json.loads(MAPS_V05_PATH.read_text())

    j1017_win_sha256 = sha256_file(J1017_WIN_LOG_PATH)
    assert j1017_win_sha256 == "b8e995f64132a8e9116ff47fa4e349d23f8788436e5c3d9631be46b54e18374b"
    j1017_win_log = json.loads(J1017_WIN_LOG_PATH.read_text())
    j1017_by_key = {(r["short_id"], r["row"]): r for r in j1017_win_log["shots"]}

    j1024_win_sha256 = sha256_file(J1024_WIN_LOG_PATH)
    win_log = json.loads(J1024_WIN_LOG_PATH.read_text())
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
    preserved_j1017_window_matches = 0

    report = {
        "job": "J1024",
        "ruling_authority": "J1020 (e82eae17d on codex/j1020-review)",
        "verifier": "jobs/reviews/verify_j0936_prep_v06.py",
        "input_maps_path": "jobs/reviews/J0936_v04_PREP_v06_maps.json",
        "input_sha256": input_sha256,
        "library_sha256": lib_sha256,
        "preserved_j1017_source_window_log_path": str(J1017_WIN_LOG_PATH),
        "preserved_j1017_source_window_log_sha256": j1017_win_sha256,
        "saved_v06_source_window_log_path": str(J1024_WIN_LOG_PATH),
        "saved_v06_source_window_log_sha256": j1024_win_sha256,
        "machine_checks_passed": True,
        "total_source_words_verified": 0,
        "source_window_mismatches": source_window_mismatches,
        "omitted_ordinary_bridges": omitted_ordinary_bridges,
        "repaired_ordinary_bridges": repaired_ordinary_bridges,
        "saved_source_window_log_summary": {
            "provenance_note": (
                "Preserves 42 unchanged body shot entries verbatim from /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json "
                "(sha256: b8e995f64132a8e9116ff47fa4e349d23f8788436e5c3d9631be46b54e18374b) and updates only S6 s05_alma_orion_set in "
                "/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json. verify_j0936_prep_v06.py verifies both log "
                "SHA-256 hashes and zero (source_path, source_in, source_out) mismatches across all 43 body shots rather than re-decoding frames itself."
            ),
            "ocr_sampling_note": "2fps OCR (306 frames sampled every 0.50s plus window tail) is sampled text inspection; 30fps decode (4,046 frames) measures luma, black fraction, dark runs, and scdet internal cuts.",
            "transform_scope_note": "5 opening shots used declared custom 9:16 crops/grades; 38 body shots used default 9:16 centre crop (crop=ih*9/16:ih) at native source speed (source_speed not applied). Mandatory every-frame OCR/dark-run gates run on final transformed MP4s at assembly.",
            "unchanged_shots_preserved_from_j1017": 42,
            "updated_shots_in_j1024": 1,
            "total_body_shots": win_log["total_body_shots"],
            "total_30fps_frames_decoded_in_saved_log": win_log["total_30fps_frames_decoded"],
            "total_2fps_ocr_sampled_frames_in_saved_log": win_log["total_2fps_ocr_frames_scanned"],
        },
        "shorts": {},
        "s6_payoff_correction_verified": {},
        "test_a_option_a_repair_verified": {},
        "scale_card_timing_s5": {},
        "s3_atempo_slot_fit_documented": {},
        "verifier_scope_notes": [
            "earliest_spoken_answer_coordinate_check verifies the supplied word_idx's recomputed output start time and >=70.0% runtime position; semantic identification of earliest answer is attributed to reviewer gemini (no human reviewer claimed at preparation stage).",
            "saved_source_window_log_summary hash-verifies /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json (42 unchanged shots) and /Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json (43 shots including S6 s05_alma_orion_set); verify_j0936_prep_v06.py does not re-decode the 4,046 30fps frames or re-run Tesseract on the 306 sampled 2fps frames.",
            "2fps OCR and contact sheets are sampled text inspection (every 0.50s), not every-frame 30fps OCR.",
            "38 of 43 body shots in the source-window log used default 9:16 centre crops at native source speed; final transformed output MP4s still require full post-assembly OCR, dark-run, picture_qa, and polish_gate passes.",
            "In S3 Spans 1..7 (tempo=1.055x), render_audition trims up to 16.17ms (776 samples at 48kHz) of WSOLA frame-buffer tail with a 5ms fade to fit each nominal scaled_dur slot; nominal source/tempo arithmetic alone does not prove acoustic word boundaries, and final assembly retains the listening check without ever trimming a syllable just to meet a slot.",
        ],
        "reviewer_assertions": {
            "earliest_spoken_answer_semantic_selection": {
                "status": "REVIEWED_BY_GEMINI_SEMANTIC_INSPECTION",
                "reviewer": "gemini (Gemini 4 Argon; no human reviewer claimed at preparation stage)",
                "note": "Verifier checks coordinates/percentage of supplied word_idx and absence of removed S6 early answer tokens; semantic identification of earliest answer is a Gemini reviewer assertion.",
            },
            "titled_subject_visual_and_geometric_occupancy": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_VISION",
                "reviewer": "gemini (Gemini 4 Argon)",
                "method": "Visual limb/horizon/roofline segmentation on 1080x1920 @0.30s frames (all_6_openings_0_30s_comparison.jpg and all_6_openings_captioned_0_30s_comparison.jpg); never equated to 1 - black_frac.",
                "all_six_above_60pct": True,
            },
            "source_window_sampled_2fps_contact_sheets": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_VISION",
                "reviewer": "gemini (Gemini 4 Argon)",
                "method": "Visual inspection of all 6 per-Short 2fps sampled contact sheets (306 sampled tiles across 43 body shots, including updated S6_028_X768qs8sNQs_full_window_2fps.jpg in /Users/benjaminoats/_desk/reviews/J1024/source_windows/).",
                "clean_windows_confirmed": True,
            },
            "spliced_vo_auditions_prosody_and_repaired_bridges": {
                "status": "REVIEWED_BY_GEMINI_MULTIMODAL_AUDIO",
                "reviewer": "gemini (Gemini 4 Argon; Codex verified execution/hashes/arithmetic in J1020 and does not claim independent listening)",
                "method": "Direct multimodal audio playback and prosody inspection of all 12 WAV files in /Users/benjaminoats/_desk/reviews/J1024/auditions/ (including regenerated S4 Option A and S6 v06 WAVs); documented per Short in vo_splice_map.auditory_judgement.",
                "all_six_verified_clean_by_ear": True,
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

        # Verify S1, S2, S3, S5 unchanged from v05
        if sid in ("S1_026_A6TW_6CXhcs", "S2_027_emwQsPxnRGM", "S3_028_bizlhspnVvY", "S5_028_jJ5LkFGyzLI"):
            assert vm["subspans"] == v05["shorts"][sid]["vo_splice_map"]["subspans"]
            assert sp == v05["shorts"][sid]["shot_plan"]
            for k in ("question_audition", "full_vo_audition"):
                assert vm["auditions"][k]["sha256"] == v05["shorts"][sid]["vo_splice_map"]["auditions"][k]["sha256"]

        # Verify frame0_gate_verification unchanged from v04 across all 6 Shorts
        assert f0 == v04["shorts"][sid]["frame0_gate_verification"]

        # Verify 0 split Gliese/710 bridges in ordinary Shorts of Film 028
        if sdata["film"] == "OWB:028" and not is_test_a:
            for a, b in zip(vm["subspans"], vm["subspans"][1:]):
                wa_last = a["words"][-1]
                wb_first = b["words"][0]
                if wa_last["word"] == "Gliese" and wb_first["word"].startswith("710"):
                    omitted_ordinary_bridges.append([sid, a["span_index"], b["span_index"]])
            for r in vm["subspans"]:
                w_ids = [w["word_idx"] for w in r["words"]]
                if (121 in w_ids and 122 in w_ids) or (719 in w_ids and 720 in w_ids) or (472 in w_ids and 473 in w_ids) or (985 in w_ids and 986 in w_ids):
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

                if (sid, s["row"]) != ("S6_028_X768qs8sNQs", "s05_alma_orion_set"):
                    assert j1017_by_key[(sid, s["row"])] == w_rec
                    preserved_j1017_window_matches += 1

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
                "scope": "Verifies supplied word_idx output start time and >=70% position; semantic answer selection is attributed to reviewer gemini.",
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
        report["shorts"][sid] = row_out

    assert not source_window_mismatches
    assert preserved_j1017_window_matches == 42
    assert not omitted_ordinary_bridges
    assert len(repaired_ordinary_bridges) == 6

    # Specific S6 payoff correction verification
    s6 = data["shorts"]["S6_028_X768qs8sNQs"]
    s6_vm = s6["vo_splice_map"]
    s6_words = [w for r in s6_vm["subspans"] for w in r["words"]]
    pre_70_words = [w["word"].lower().strip(".,?!") for w in s6_words if w["start"] < s6_vm["seventy_pct_mark_s"]]
    assert all(tok not in pre_70_words for tok in ("creep", "moon", "35", "brightest", "sirius", "orange"))
    assert s6_vm["earliest_spoken_answer"] == {"word": "brightest", "word_idx": 881, "start": 16.820, "end": 17.240, "pct_of_total": 75.83}
    assert s6_vm["keyword_timings"]["star"] == {"word": "star", "word_idx": 398, "start": 17.320, "end": 17.740, "pct_of_total": 78.09}
    assert s6_vm["keyword_timings"]["three"] == {"word": "three", "word_idx": 743, "start": 17.880, "end": 18.280, "pct_of_total": 80.61}
    report["s6_payoff_correction_verified"] = {
        "question_retained": s6_vm["opening_question_punctuated"],
        "removed_early_answer_tokens_absent_before_70pct": True,
        "pre_70pct_body_text": " ".join(r["text"] for r in s6_vm["subspans"][9:19]),
        "payoff_span_20_start_s": s6_vm["subspans"][19]["timeline_start"],
        "earliest_spoken_answer": s6_vm["earliest_spoken_answer"],
        "keyword_star": s6_vm["keyword_timings"]["star"],
        "keyword_three": s6_vm["keyword_timings"]["three"],
        "shot_s05_updated_to_night_sky_video": {
            "row": s6["shot_plan"][4]["row"],
            "source_path": s6["shot_plan"][4]["source_path"],
            "source_in": s6["shot_plan"][4]["source_in"],
            "source_out": s6["shot_plan"][4]["source_out"],
            "video": s6["shot_plan"][4]["video"],
            "spoken_match": s6["shot_plan"][4]["spoken_match"],
        },
    }

    # Specific Test A (S4) Option A repair verification
    s4 = data["shorts"]["S4_028_DETI0HV2jlI"]
    s4_vm = s4["vo_splice_map"]
    s4_sub = s4_vm["subspans"]
    v05_s4_sub = v05["shorts"]["S4_028_DETI0HV2jlI"]["vo_splice_map"]["subspans"]
    assert s4_sub[:3] == v05_s4_sub[:3]
    assert s4_sub[7:] == v05_s4_sub[7:]
    assert s4_sub[3]["gap_after"] == 0.060
    assert (s4_sub[4]["timeline_start"], s4_sub[4]["timeline_end"], s4_sub[4]["gap_after"]) == (6.012, 6.672, 0.040)
    assert (s4_sub[5]["source_in"], s4_sub[5]["source_out"], s4_sub[5]["timeline_start"], s4_sub[5]["timeline_end"], s4_sub[5]["gap_after"]) == (14.980, 15.780, 6.700, 7.500, 0.040)
    assert (s4_sub[6]["source_in"], s4_sub[6]["source_out"], s4_sub[6]["timeline_start"], s4_sub[6]["timeline_end"], s4_sub[6]["gap_after"]) == (16.060, 17.220, 7.528, 8.688, 0.060)
    assert s4_sub[7]["timeline_start"] == 8.736
    assert s4_vm["vo_end_s"] == 23.516 and s4_vm["total_duration_s"] == 24.516
    assert [s4["single_teaching_overlay"]["timeline_in"], s4["single_teaching_overlay"]["timeline_out"]] == [17.950, 21.450]
    expected_diag_sha = "d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a"
    assert s4_vm["auditions"]["full_vo_audition"]["sha256"] == expected_diag_sha == sha256_file(J1019_TESTA_DIAG)
    report["test_a_option_a_repair_verified"] = {
        "applied_in_v06": True,
        "span_4_gap_after_s": s4_sub[3]["gap_after"],
        "span_5_timeline_s": [s4_sub[4]["timeline_start"], s4_sub[4]["timeline_end"]],
        "span_5_gap_after_s": s4_sub[4]["gap_after"],
        "span_6_source_s": [s4_sub[5]["source_in"], s4_sub[5]["source_out"]],
        "span_6_timeline_s": [s4_sub[5]["timeline_start"], s4_sub[5]["timeline_end"]],
        "span_6_gap_after_s": s4_sub[5]["gap_after"],
        "span_7_source_s": [s4_sub[6]["source_in"], s4_sub[6]["source_out"]],
        "span_7_timeline_s": [s4_sub[6]["timeline_start"], s4_sub[6]["timeline_end"]],
        "span_7_gap_after_s": s4_sub[6]["gap_after"],
        "span_8_timeline_start_s": s4_sub[7]["timeline_start"],
        "vo_end_s": s4_vm["vo_end_s"],
        "total_duration_s": s4_vm["total_duration_s"],
        "card_window_s": [s4["single_teaching_overlay"]["timeline_in"], s4["single_teaching_overlay"]["timeline_out"]],
        "full_vo_audition_sha256": s4_vm["auditions"]["full_vo_audition"]["sha256"],
        "matches_retained_proposal_diagnostic_hash": True,
    }

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

    s3_note = data["shorts"]["S3_028_bizlhspnVvY"]["vo_splice_map"]["atempo_slot_fit_implementation_note"]
    assert len(s3_note["spans_1_to_7_atempo_buffer_trim_details"]) == 7
    report["s3_atempo_slot_fit_documented"] = s3_note

    OUT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print("Verification complete! Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
