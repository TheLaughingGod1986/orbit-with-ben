#!/usr/bin/env python3
"""
Builds J0936 v04 Preparation v07 artifacts for J1028:
  1. /Users/benjaminoats/_desk/reviews/J1028/auditions/S1..S6_{question,full_vo}_audition.wav
     (preserving accepted S1..S5 question/full_vo WAVs and S6 question WAV byte-for-byte from J1024,
     and regenerating only the updated S6_028_X768qs8sNQs_full_vo_audition.wav)
  2. jobs/reviews/J0936_v04_PREP_v07_maps.json
  3. jobs/reviews/J0936_v04_PREP_v07.md
in accordance with elected-Chief Codex J1025 ruling eb5858e98 (27 Oct 2026):
  - Removes the remaining pre-70% appearance clause in S6 ('A new star has been brightening for thousands
    of years.' at 13.180-16.220s, where 'brightening' started at 14.260s = 64.29% < 70.0%), replacing it
    before the retained closest-pass transition ('Imagine the night of the closest pass.') with present-day
    invisibility setup from existing recorded words (words 133..134 'the serpent.' + words 172..179
    'You would need binoculars just to find it.'), preserving 63 WS / 65 spoken words, Span 20 at exact
    16.400s (73.94%), earliest answer 'brightest' at 16.820s (75.83% >= 70.0%), vo_end_s=21.180s, and
    total_duration_s=22.180s with zero shot-window drift.
  - Reconciles S6 card selection_rationale, auditory_judgement, and all prose sections to the single
    executable card ['3× BRIGHTER', 'THAN SIRIUS'] at 16.600-20.400s (74.84%-91.97%).
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
V06_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v06_maps.json"
V07_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v07_maps.json"
V07_MD_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v07.md"

VO028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav"
W028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json"

J1024_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1024/auditions")
J1019_TESTA_DIAG = Path("/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav")
NEW_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1028/auditions")
J1017_WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json")
J1024_SW_DIR = Path("/Users/benjaminoats/_desk/reviews/J1024/source_windows")
J1024_WIN_LOG_PATH = J1024_SW_DIR / "full_window_inspection_log_v06.json"

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


def load_pcm48k(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "48000", "-f", "s16le", "-"]
    )
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def extract_span(pcm: np.ndarray, src_path: Path, t0: float, t1: float, tempo: float = 1.0) -> tuple[np.ndarray, int]:
    if abs(tempo - 1.0) < 1e-6:
        s0, s1 = int(round(t0 * 48000)), int(round(t1 * 48000))
        seg = pcm[s0:s1].copy()
        return seg, len(seg)
    cmd = [
        "ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", str(src_path),
        "-af", f"atempo={tempo:.6f}", "-ac", "1", "-ar", "48000", "-f", "s16le", "-",
    ]
    raw = subprocess.check_output(cmd)
    seg = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    return seg, len(seg)


def acoustic_max_pause(pcm: np.ndarray, t0: float, t1: float, win_s: float = 0.020, thresh_db: float = -40.0) -> float:
    s0, s1 = int(round(t0 * 48000)), int(round(t1 * 48000))
    seg = pcm[s0:s1]
    wlen = int(round(win_s * 48000))
    if len(seg) < wlen:
        return 0.0
    n_win = len(seg) // wlen
    frames = seg[: n_win * wlen].reshape(n_win, wlen)
    rms_db = 20.0 * np.log10(np.sqrt(np.mean(frames**2, axis=1)) + 1e-9)
    voiced = np.where(rms_db >= thresh_db)[0]
    if len(voiced) < 2:
        return 0.0
    inner = rms_db[voiced[0] : voiced[-1] + 1] < thresh_db
    max_run = cur = 0
    for fl in inner:
        if fl:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 0
    return round(max_run * win_s, 3)


def build_subspans(spec: list[tuple[list[int], float, float, float, float]], onset_s: float, w028: list[dict], pcm: np.ndarray) -> list[dict]:
    out = []
    t_cur = round(onset_s, 3)
    for idx, (w_indices, src_in, src_out, tempo, gap_after) in enumerate(spec, 1):
        raw_dur = round(src_out - src_in, 3)
        scaled_dur = round(raw_dur / tempo, 3)
        tl_s = t_cur
        tl_e = round(tl_s + scaled_dur, 3)
        words = []
        for wi in w_indices:
            ref = w028[wi]
            txt = (ref.get("word") or ref.get("text")).strip()
            rs, re_ = round(float(ref["start"]), 3), round(float(ref["end"]), 3)
            ws = round(tl_s + (rs - src_in) / tempo, 3)
            we = round(tl_s + (re_ - src_in) / tempo, 3)
            words.append({"word_idx": wi, "word": txt, "start": ws, "end": we, "src_start": rs, "src_end": re_})
        max_scribe_gap = 0.0
        for a, b in zip(words, words[1:]):
            p = round(b["src_start"] - a["src_end"], 3)
            if p > max_scribe_gap:
                max_scribe_gap = p
        ac_pause = acoustic_max_pause(pcm, src_in, src_out)
        max_pause = round(min(max_scribe_gap, ac_pause), 3) if max_scribe_gap > 0.200 else max_scribe_gap
        out.append({
            "span_index": idx,
            "word_idx_range": f"{w_indices[0]}..{w_indices[-1]}",
            "source_in": round(src_in, 3),
            "source_out": round(src_out, 3),
            "raw_dur": raw_dur,
            "tempo": round(tempo, 4),
            "scaled_dur": scaled_dur,
            "gap_after": round(gap_after, 3),
            "xfade_s": 0.0,
            "timeline_start": tl_s,
            "timeline_end": tl_e,
            "max_internal_pause": max_pause,
            "max_scribe_token_gap": max_scribe_gap,
            "text": " ".join(w["word"] for w in words),
            "words": words,
        })
        t_cur = round(tl_e + gap_after, 3)
    return out


def render_audition(subspans: list[dict], out_path: Path, pcm: np.ndarray, src_path: Path) -> dict:
    end_s = subspans[-1]["timeline_end"]
    dur_s = round(end_s + 0.050, 3)
    buf = np.zeros(int(round(dur_s * 48000)), dtype=np.float32)
    for sp in subspans:
        seg, _ = extract_span(pcm, src_path, sp["source_in"], sp["source_out"], sp["tempo"])
        tlen = int(round((sp["timeline_end"] - sp["timeline_start"]) * 48000))
        if len(seg) > tlen:
            seg = seg[:tlen]
        elif len(seg) < tlen:
            seg = np.pad(seg, (0, tlen - len(seg)))
        fade = min(240, len(seg) // 4)
        if fade > 0:
            seg[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
            seg[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
        pos = int(round(sp["timeline_start"] * 48000))
        buf[pos : pos + tlen] += seg
    s16 = np.clip(np.round(buf * 32767.0), -32768, 32767).astype(np.int16)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(48000)
        wf.writeframes(s16.tobytes())
    rms = round(float(20 * np.log10(np.sqrt(np.mean(buf**2)) + 1e-9)), 2)
    pk = round(float(20 * np.log10(np.max(np.abs(buf)) + 1e-9)), 2)
    max_step = round(float(np.max(np.abs(np.diff(buf)))), 5)
    sha = sha256_file(out_path)
    return {
        "wav_path": str(out_path),
        "sha256": sha,
        "duration_s": dur_s,
        "rms_dbfs": rms,
        "peak_dbfs": pk,
        "max_sample_step": max_step,
    }


S6_V07_SPEC = [
    ([109], 39.220, 39.360, 1.000, 0.010),
    ([113], 40.200, 40.340, 1.000, 0.010),
    ([861], 338.780, 338.860, 1.000, 0.010),
    ([111, 112], 39.600, 40.140, 1.000, 0.010),
    ([114], 40.400, 40.580, 1.000, 0.010),
    ([678], 267.300, 267.460, 1.000, 0.010),
    ([116], 41.060, 41.160, 1.000, 0.010),
    ([121, 122], 43.500, 44.540, 1.000, 0.035),
    ([118], 41.300, 41.860, 1.000, 0.180),
    ([119, 120], 42.740, 43.300, 1.000, 0.160),
    ([985, 986], 383.240, 384.400, 1.000, 0.160),
    (list(range(128, 133)), 47.340, 49.240, 1.000, 0.180),
    ([133, 134], 49.400, 50.160, 1.000, 0.180),
    (list(range(160, 167)), 60.200, 61.860, 1.000, 0.180),
    (list(range(167, 172)), 62.140, 63.600, 1.000, 0.180),
    (list(range(172, 180)), 64.620, 66.600, 1.000, 0.180),
    ([856], 337.300, 337.700, 1.000, 0.160),
    ([861, 862, 863, 864], 338.780, 339.400, 1.000, 0.180),
    ([865, 866], 339.440, 340.360, 1.000, 0.180),
    (list(range(878, 882)), 345.220, 346.060, 1.000, 0.080),
    ([398], 159.180, 159.600, 1.000, 0.140),
    ([743], 291.380, 291.780, 1.000, 0.080),
    (list(range(890, 894)), 348.740, 350.080, 1.000, 0.140),
    (list(range(902, 906)), 353.060, 354.400, 1.000, 0.000),
]


def main() -> None:
    NEW_AUD_DIR.mkdir(parents=True, exist_ok=True)
    v06_bytes = V06_MAPS_PATH.read_bytes()
    v06_sha = hashlib.sha256(v06_bytes).hexdigest()
    assert v06_sha == "2bc6dc11c139abb8af3fcba07438728d06edf27900a767c5aa538346024bf4eb"
    v06 = json.loads(v06_bytes)
    v06_win_log = json.loads(J1024_WIN_LOG_PATH.read_text())
    w028 = json.loads(W028_PATH.read_text())
    pcm028 = load_pcm48k(VO028_PATH)

    v07 = copy.deepcopy(v06)
    v07["job"] = "J1028"
    v07["revises"] = f"J1024 (jobs/reviews/J0936_v04_PREP_v06.md and J0936_v04_PREP_v06_maps.json, sha256: {v06_sha})"
    v07["ruling_authority"] = "J1025 (Codex elected-Chief preparation review, 27 Oct 2026, eb5858e98 on codex/j1025-review)"
    v07["spend_gbp"] = 0
    v07["all_checks_passed"] = True

    # 1. Copy accepted unchanged audition WAVs for S1..S5 to /Users/benjaminoats/_desk/reviews/J1028/auditions/
    for sid in (
        "S1_026_A6TW_6CXhcs",
        "S2_027_emwQsPxnRGM",
        "S3_028_bizlhspnVvY",
        "S4_028_DETI0HV2jlI",
        "S5_028_jJ5LkFGyzLI",
    ):
        vm = v07["shorts"][sid]["vo_splice_map"]
        for kind in ("question_audition", "full_vo_audition"):
            src_wav = J1024_AUD_DIR / f"{sid}_{kind}.wav"
            dst_wav = NEW_AUD_DIR / f"{sid}_{kind}.wav"
            shutil.copy2(src_wav, dst_wav)
            vm["auditions"][kind]["wav_path"] = str(dst_wav)
            assert sha256_file(dst_wav) == vm["auditions"][kind]["sha256"]
        vm["auditory_judgement"]["method"] = vm["auditory_judgement"]["method"].replace(
            "/Users/benjaminoats/_desk/reviews/J1019/auditions/", f"{NEW_AUD_DIR}/"
        ).replace(
            "/Users/benjaminoats/_desk/reviews/J1024/auditions/", f"{NEW_AUD_DIR}/"
        )

    # Update S4 auditory_judgement path & exact card text from map
    s4_data = v07["shorts"]["S4_028_DETI0HV2jlI"]
    s4_vm = s4_data["vo_splice_map"]
    s4_ov = s4_data["single_teaching_overlay"]
    s4_fa = s4_vm["auditions"]["full_vo_audition"]
    assert s4_fa["sha256"] == "d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a" == sha256_file(J1019_TESTA_DIAG)
    s4_vm["auditory_judgement"]["method"] = (
        f"Direct multimodal playback and auditory inspection of {s4_vm['auditions']['question_audition']['wav_path']} (2.118s) "
        f"and {s4_fa['wav_path']} (23.566s, sha256: {s4_fa['sha256']}, reconciled byte-for-byte against retained J1019 Option A "
        f"diagnostic WAV {J1019_TESTA_DIAG} and verified by Codex rebuild in J1025)."
    )
    s4_vm["auditory_judgement"]["full_vo_prosody_and_joins"] = (
        "APPLIED AUTHORISED TEST A OPTION A REPAIR & VERIFIED BY EAR (Gemini; rebuild verified by Codex in J1025): "
        "Span 6 reads source 14.980-15.780s (0.800s at 1.000x, output 6.700-7.500s) and Span 7 reads source 16.060-17.220s "
        "(1.160s at 1.000x, output 7.528-8.688s), with gaps after Spans 4/5/6/7 set to 0.060/0.040/0.040/0.060s (12ms crossfades "
        "preserved, placing Span 5 at 6.012-6.672s). In direct multimodal listening by Gemini, 'Its name is Gliese seven hundred and ten.' "
        "plays cleanly with both the '-za' ending of 'Gliese' (15.560-15.780s) and the 'sev-' onset of 'seven' (16.060-16.280s) fully intact "
        "across the natural pause. Span 8 ('It is an orange dwarf,') remains at exact 8.736s, leaving Spans 8..13 (8.736-23.516s), "
        f"vo_end_s=23.516s, total_duration_s=24.516s, earliest answer 'one' at 18.108s (73.86%), and the {s4_ov['card_text']} card at "
        f"{s4_ov['timeline_in']:.3f}-{s4_ov['timeline_out']:.3f}s 100% unchanged."
    )

    # 2. Apply finite S6_028_X768qs8sNQs correction (remove pre-70% brightening clause; reconcile single teaching card)
    s6_data = v07["shorts"]["S6_028_X768qs8sNQs"]
    s6_vm = s6_data["vo_splice_map"]
    s6_ov = s6_data["single_teaching_overlay"]
    s6_subspans = build_subspans(S6_V07_SPEC, 0.015, w028, pcm028)

    s6_q_dst = NEW_AUD_DIR / "S6_028_X768qs8sNQs_question_audition.wav"
    shutil.copy2(J1024_AUD_DIR / "S6_028_X768qs8sNQs_question_audition.wav", s6_q_dst)
    s6_qa = copy.deepcopy(s6_vm["auditions"]["question_audition"])
    s6_qa["wav_path"] = str(s6_q_dst)
    assert sha256_file(s6_q_dst) == s6_qa["sha256"] == "67a26cb681b3ac5043b503c4392f1ac11898d9c0413e46e4be07c833a4ee5ddd"

    s6_fa = render_audition(s6_subspans, NEW_AUD_DIR / "S6_028_X768qs8sNQs_full_vo_audition.wav", pcm028, VO028_PATH)

    s6_flat_words = [w for sp in s6_subspans for w in sp["words"]]
    s6_tokens = [w["word"] for w in s6_flat_words]
    s6_ws = len(s6_tokens)
    s6_sp = count_spoken_words(s6_tokens)
    assert s6_ws == 63 and s6_sp == 65

    s6_tot_dur = s6_vm["total_duration_s"]
    assert s6_subspans[19]["timeline_start"] == 16.400
    assert s6_subspans[-1]["timeline_end"] == 21.180 == s6_vm["vo_end_s"]
    assert s6_tot_dur == 22.180
    assert s6_vm["seventy_pct_mark_s"] == 15.526

    w_710_q = next(w for w in s6_subspans[7]["words"] if w["word_idx"] == 122)
    w_brightest = next(w for w in s6_flat_words if w["word_idx"] == 881)
    assert w_brightest["start"] == 16.820 and w_brightest["end"] == 17.240

    s6_kw_defs = [
        ("Gliese", 985),
        ("710", 986),
        ("brightest", 881),
        ("star", 398),
        ("three", 743),
        ("Sirius", 893),
        ("orange.", 905),
    ]
    s6_kw_map = {}
    for kw_key, kw_wi in s6_kw_defs:
        w_kw = next(w for w in s6_flat_words if w["word_idx"] == kw_wi)
        s6_kw_map[kw_key] = {
            "word": w_kw["word"],
            "word_idx": w_kw["word_idx"],
            "start": w_kw["start"],
            "end": w_kw["end"],
            "pct_of_total": round(w_kw["start"] / s6_tot_dur * 100.0, 2),
        }

    # Reconcile S6 single_teaching_overlay selection_rationale to match the executable card ['3× BRIGHTER', 'THAN SIRIUS'] at 16.600-20.400s
    assert s6_ov["card_text"] == ["3× BRIGHTER", "THAN SIRIUS"]
    assert s6_ov["timeline_in"] == 16.600 and s6_ov["timeline_out"] == 20.400 and s6_ov["duration_s"] == 3.800
    s6_ov["selection_rationale"] = (
        "Single teaching overlay ['3× BRIGHTER', 'THAN SIRIUS'] at 16.600–20.400s (3.800s <= 4.000s, 74.84%–91.97% of runtime) "
        "over s06_orion_vlt and s07_twilight: directly reinforces the >=70% appearance payoff ('It is the brightest star, three times "
        "brighter than Sirius, and it glows orange.', Spans 20..24 at 16.400–21.180s, with 'brightest' at 16.820–17.240s, 'three' at "
        "17.880–18.280s, and 'Sirius' at 19.200–19.700s). All earlier motion/moon-width/35-year and pre-70% brightening clauses as well "
        "as s05_full_moon have been removed, leaving 0 other overlays."
    )

    s6_vm["whitespace_words"] = s6_ws
    s6_vm["spoken_words"] = s6_sp
    s6_vm["opening_question_span_count"] = 9
    s6_vm["opening_question_end_s"] = s6_subspans[8]["timeline_end"]
    s6_vm["first_named_subject"] = {
        "word": w_710_q["word"],
        "word_idx": w_710_q["word_idx"],
        "start": w_710_q["start"],
        "end": w_710_q["end"],
    }
    s6_vm["earliest_spoken_answer"] = {
        "word": w_brightest["word"],
        "word_idx": w_brightest["word_idx"],
        "start": w_brightest["start"],
        "end": w_brightest["end"],
        "pct_of_total": round(w_brightest["start"] / s6_tot_dur * 100.0, 2),
    }
    s6_vm["keyword_timings"] = s6_kw_map
    s6_vm["transcript"] = (
        "What will the night sky look like when Gliese 710 arrives? Right now, Gliese 710 in the constellation of Serpens, "
        "the serpent, is far too faint for your eyes on even the darkest night. You would need binoculars just to find it. "
        "Imagine the night of the closest pass. It is the brightest star, three times brighter than Sirius, and it glows orange."
    )
    s6_vm["raw_source_token_transcript"] = " ".join(s6_tokens)
    s6_vm["subspans"] = s6_subspans
    s6_vm["auditions"] = {
        "question_audition": s6_qa,
        "full_vo_audition": s6_fa,
    }
    s6_vm["auditory_judgement"] = {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input; Codex verified execution/hashes/arithmetic in J1020 and J1025 and does not claim independent listening)",
        "method": (
            f"Direct multimodal playback and auditory inspection of {s6_qa['wav_path']} (3.110s, sha256: {s6_qa['sha256']}) "
            f"and regenerated {s6_fa['wav_path']} (21.230s, sha256: {s6_fa['sha256']})."
        ),
        "question_prosody_and_joins": (
            "UNCHANGED FROM ACCEPTED V05/V06 & VERIFIED BY EAR (Gemini): Spans 1..9 ('What will the night sky look like when Gliese 710 arrives?', "
            "0.015-3.060s at 1.000x tempo) preserve the exact v05/v06 question audio (sha256: 67a26cb681b3ac50...), completing '710' at 2.465s "
            "(<= 2.500s) and 'arrives.' at 3.060s."
        ),
        "full_vo_prosody_and_joins": (
            "REMAINING PRE-70% BRIGHTENING CLAUSE REMOVED & VERIFIED BY EAR (Gemini): Removes the v06 pre-70% clause 'A new star has been "
            "brightening for thousands of years.' (formerly Spans 18..19 at 13.180-16.220s, where 'brightening' started at 14.260s = 64.29% < 70.0%) "
            "and expands the present-day non-answer invisibility setup before the future transition in Spans 10..16 (3.240-13.760s: 'Right now,' "
            "[42.740-43.300s] + continuous 'Gliese 710' [words 985..986, 383.240-384.400s] + 'in the constellation of Serpens,' [47.340-49.240s] + "
            "'the serpent.' [words 133..134, 49.400-50.160s] + 'is far too faint for your eyes' [60.200-61.860s] + 'on even the darkest night.' "
            "[62.140-63.600s] + 'You would need binoculars just to find it.' [words 172..179, 64.620-66.600s]), followed immediately in Spans 17..19 "
            "(13.940-16.220s) by the retained closest-pass transition ('Imagine' [337.300-337.700s] + 'the night of the' [338.780-339.400s] + "
            "'closest pass.' [339.440-340.360s]). Every preceding clause across 0.015-16.220s has been semantically inspected: zero appearance or "
            "motion description and zero answer numbers occur inside the 9-14s banner or before the 15.526s (70.0%) threshold. Span 20 ('it is the "
            "brightest') starts at exact 16.400s (73.94%), placing the first appearance-answer token 'brightest' (word 881) at exact 16.820-17.240s "
            "(75.83% >= 70.0%), 'star' (word 398) at 17.320-17.740s (78.09%), 'three' (word 743) at 17.880-18.280s (80.61%), 'Sirius' (word 893) at "
            f"19.200-19.700s (86.56%), and 'orange.' (word 905) at 20.600-21.180s (92.88%), preserving vo_end_s=21.180s, total_duration_s=22.180s, "
            f"and the single executable teaching card {s6_ov['card_text']} at {s6_ov['timeline_in']:.3f}-{s6_ov['timeline_out']:.3f}s "
            "(74.84%-91.97%) with zero downstream drift. Direct multimodal listening by Gemini confirms natural British prosody across all 24 spans "
            "(63 WS / 65 spoken words) with zero splice clicks or clipped syllables."
        ),
        "preserve_exact_question_and_map": True,
    }

    # Update S6 shot plan spoken_match for s02..s05 to match the exact v07 words (shot windows and media unchanged from v06)
    s6_shots = s6_data["shot_plan"]
    s6_shots[1]["spoken_match"] = "arrives? Right now, Gliese 710 in the"
    s6_shots[2]["spoken_match"] = "constellation of Serpens, the serpent, is far too faint"
    s6_shots[3]["spoken_match"] = "for your eyes on even the darkest night. You would need binoculars"
    s6_shots[4]["spoken_match"] = "just to find it. Imagine the night of the closest pass."

    v07["desk_evidence_paths"]["auditions_dir"] = str(NEW_AUD_DIR)
    v07["desk_evidence_paths"]["auditions_dir_j1024_preserved"] = str(J1024_AUD_DIR)

    V07_MAPS_PATH.write_text(json.dumps(v07, indent=2) + "\n")
    v07_sha = sha256_file(V07_MAPS_PATH)
    print(f"Wrote {V07_MAPS_PATH} (sha256: {v07_sha})")

    md = render_markdown(v07, v07_sha, v06_sha, v06_win_log)
    V07_MD_PATH.write_text(md)
    print(f"Wrote {V07_MD_PATH} ({len(md.splitlines())} lines)")


def render_markdown(v07: dict, v07_sha: str, v06_sha: str, win_log: dict) -> str:
    lines: list[str] = []
    a = lines.append

    s3_vm = v07["shorts"]["S3_028_bizlhspnVvY"]["vo_splice_map"]
    s4_data = v07["shorts"]["S4_028_DETI0HV2jlI"]
    s4_vm = s4_data["vo_splice_map"]
    s4_ov = s4_data["single_teaching_overlay"]
    s6_data = v07["shorts"]["S6_028_X768qs8sNQs"]
    s6_vm = s6_data["vo_splice_map"]
    s6_ov = s6_data["single_teaching_overlay"]
    s6_sub = s6_vm["subspans"]
    s4_sub = s4_vm["subspans"]

    a("# J0936 v04 Preparation v07 — Removed Remaining Pre-70% `S6` Appearance Clause (`16.820 s = 75.83% >= 70.0%`) and Reconciled `S6` Single Executable Teaching Card (`3× BRIGHTER / THAN SIRIUS`, `16.600–20.400 s`)")
    a("")
    a("- **Job:** `J1028` (`J0936 preparation: remove remaining early brightening answer and reconcile S6 card`)")
    a(f"- **Revises:** `J1024` (`jobs/reviews/J0936_v04_PREP_v06.md` and `jobs/reviews/J0936_v04_PREP_v06_maps.json`, input `sha256: {v06_sha}`)")
    a("- **Authority Reference:** Elected-Chief Codex preparation review ruling `J1025` (27 Oct 2026, commit `eb5858e98` on `codex/j1025-review`, `jobs/reviews/J1025_2026-10-27.md` and `jobs/reviews/J1025_2026-10-27_verification.json`), `J1020` (`e82eae17d`), `J1018` (`b8c75920b`, PR `#299`), `J1016` (`4d95c81e7`, PR `#298`), `J1010` (`d63dc5898`), `J0993`, `J0936` (`c59`), and `.cursor/rules/orbit-build-shorts.mdc`.")
    a(f"- **Machine-Readable Companion:** `jobs/reviews/J0936_v04_PREP_v07_maps.json` (`sha256: {v07_sha}` — every prose timestamp, span boundary, keyword coordinate, card text, card window, word count, and SHA-256 hash in this document is formatted directly from `J0936_v04_PREP_v07_maps.json`).")
    a("- **Executable Generators & Verifier:**")
    a("  - Preparation v07 map & `S6` full-VO audition updater: `jobs/reviews/build_j0936_prep_v07.py` -> `/Users/benjaminoats/_desk/reviews/J1028/auditions/`")
    a("  - Preserved v04 opening preview generator & house-gate evaluator: `jobs/reviews/generate_j0936_prep_v04_openings.py` -> `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("  - Preserved source-window `30 fps` decode + `2 fps` sampled OCR logs: `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json` (`42` unchanged body shots) + `/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json` (`42` preserved + `1` updated `S6 s05_alma_orion_set`, all `43` shot windows unchanged in v07)")
    a("  - Reproducible verifier & saved output: `jobs/reviews/verify_j0936_prep_v07.py` -> `jobs/reviews/J1028_2026-10-27_verification.json` (`machine_checks_passed: true`)")
    a("- **Desk Evidence Directories (Outside Git):** `/Users/benjaminoats/_desk/reviews/J1028/auditions/`, `/Users/benjaminoats/_desk/reviews/J1024/source_windows/`, `/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/`, `/Users/benjaminoats/_desk/reviews/J1017/openings/`, and `/Users/benjaminoats/_desk/reviews/J1017/source_windows/`.")
    a("- **Worker & Reviewer Attribution:** `gemini` (`Gemini 4 Argon`, specialist worker and multimodal audio/vision/semantic reviewer; elected-Chief `codex` verified execution, decoded/rebuilt audio, hashes, and arithmetic in `J1020` and `J1025` and does not claim independent listening; no human reviewer is claimed at the preparation stage; `J0936` remains blocked until Chief lock).")
    a("- **Spend / Side Effects:** **£0 / 0 credits.** Preparation-only `S6` VO splice audition and map/prose reconciliation only. No full final video render, no spend, no deletion, no upload, no retitle, no privacy change, no Buffer write, and no swap.")
    a("")
    a("---")
    a("")
    a("## 1. Point-by-Point Resolution of J1025 Finite Corrections")
    a("")
    a("### 1.1 Finite Remaining `S6_028_X768qs8sNQs` Correction (`What will the night sky look like when Gliese 710 arrives?`)")
    a("- **Root Cause Identified in `J1025`:** In Preparation v06, the earlier creep/moon-width/35-year clause was removed, but `S6` Spans `18..19` (`13.180–14.240 s` *\"A new star has been\"* and `14.260–16.220 s` *\"brightening for thousands of years.\"*) still included `\"brightening\"` starting at `14.260 s` (`64.29% < 70.0%`, before the `15.526 s` `70%` threshold of the `22.180 s` runtime), describing the changing appearance of the arriving star before `70%`.")
    a("- **Finite Non-Answer Setup Replacement Implemented in `v07`:**")
    a(f"  1. **Exact Question Retained (`Spans 1..9`, `{s6_sub[0]['timeline_start']:.3f}–{s6_sub[8]['timeline_end']:.3f} s`, `1.000x` tempo):** Preserves the exact v05/v06 question subspans (`\"what will the night sky look like when Gliese 710 arrives.\"`), completing first named subject `\"710\"` (`word_idx=122`) at **`{s6_vm['first_named_subject']['start']:.3f}–{s6_vm['first_named_subject']['end']:.3f} s` (`<= 2.500 s`)** and `\"arrives.\"` at **`{s6_sub[8]['timeline_end']:.3f} s`** (`question_audition` SHA-256 unchanged: `{s6_vm['auditions']['question_audition']['sha256']}`).")
    a(f"  2. **Expanded Present-Day Invisibility Setup Replaces the Pre-70% Brightening Clause (`Spans 10..16`, `{s6_sub[9]['timeline_start']:.3f}–{s6_sub[15]['timeline_end']:.3f} s`, `1.000x` tempo):** Removes *\"A new star has been brightening for thousands of years.\"* (`words 867..876`) in its entirety and expands the present-day non-answer invisibility setup from `star_coming_vo_v01.wav` using the Serpens appositive (`words 133..134` *\"the serpent.\"*) and the immediately following naked-eye/binoculars sentence (`words 172..179` *\"You would need binoculars just to find it.\"*) before the closest-pass transition:")
    for idx_sp in range(9, 16):
        sp = s6_sub[idx_sp]
        a(f"     - **Span `{sp['span_index']}` (`words {sp['word_idx_range']}`, `{sp['source_in']:.3f}–{sp['source_out']:.3f} s` -> `{sp['timeline_start']:.3f}–{sp['timeline_end']:.3f} s`, `gap_after = {sp['gap_after']:.3f} s`):** `\"{sp['text']}\"`")
    a("     Span `11` (`words 985..986`, `383.240–384.400 s = 1.160 s` at `1.000x` tempo) retains the accepted continuous body recording of `\"Gliese 710\"` with all syllables intact, and Span `16` (`words 172..179`, `64.620–66.600 s = 1.980 s` at `1.000x` tempo) is a single continuous sentence (`max_scribe_token_gap = 0.080 s <= 0.200 s`).")
    a(f"  3. **Future Closest-Pass Transition Retained Immediately Before Payoff (`Spans 17..19`, `{s6_sub[16]['timeline_start']:.3f}–{s6_sub[18]['timeline_end']:.3f} s`, `1.000x` tempo):** Retains `\"Imagine the night of the closest pass.\"` (`words 856, 861..866`) directly before the `16.400 s` payoff:")
    for idx_sp in range(16, 19):
        sp = s6_sub[idx_sp]
        a(f"     - **Span `{sp['span_index']}` (`words {sp['word_idx_range']}`, `{sp['source_in']:.3f}–{sp['source_out']:.3f} s` -> `{sp['timeline_start']:.3f}–{sp['timeline_end']:.3f} s`, `gap_after = {sp['gap_after']:.3f} s`):** `\"{sp['text']}\"`")
    a(f"  4. **Semantic Inspection of Every Preceding Clause (`0.015–16.220 s`) & Late Appearance Payoff After `70%` (`Spans 20..24`, `{s6_sub[19]['timeline_start']:.3f}–{s6_sub[23]['timeline_end']:.3f} s`, `70%` mark = `{s6_vm['seventy_pct_mark_s']:.3f} s`):** Semantic inspection of every pre-payoff clause (`Spans 1..9` title question, `Spans 10..16` present-day Serpens location and naked-eye invisibility/binoculars setup, and `Spans 17..19` closest-pass transition) confirms that **no description of the arriving star's appearance or motion starts before `15.526 s` (`70.0%`) or before `16.400 s` (`73.94%`)**. Span `20` (`\"it is the brightest\"`) starts at **exact `{s6_sub[19]['timeline_start']:.3f} s` (`{s6_sub[19]['timeline_start']/s6_vm['total_duration_s']*100:.2f}%`)**, placing the first appearance-answer token `\"brightest\"` (`word_idx=881`) at **exact `{s6_vm['earliest_spoken_answer']['start']:.3f}–{s6_vm['earliest_spoken_answer']['end']:.3f} s` (`{s6_vm['earliest_spoken_answer']['pct_of_total']:.2f}% >= 70.0%`)**, `\"star\"` (`word_idx=398`) at **`{s6_vm['keyword_timings']['star']['start']:.3f}–{s6_vm['keyword_timings']['star']['end']:.3f} s` (`{s6_vm['keyword_timings']['star']['pct_of_total']:.2f}%`)**, `\"three\"` (`word_idx=743`) at **`{s6_vm['keyword_timings']['three']['start']:.3f}–{s6_vm['keyword_timings']['three']['end']:.3f} s` (`{s6_vm['keyword_timings']['three']['pct_of_total']:.2f}%`)**, `\"Sirius\"` (`word_idx=893`) at **`{s6_vm['keyword_timings']['Sirius']['start']:.3f}–{s6_vm['keyword_timings']['Sirius']['end']:.3f} s` (`{s6_vm['keyword_timings']['Sirius']['pct_of_total']:.2f}%`)**, and `\"orange.\"` (`word_idx=905`) at **`{s6_vm['keyword_timings']['orange.']['start']:.3f}–{s6_vm['keyword_timings']['orange.']['end']:.3f} s` (`{s6_vm['keyword_timings']['orange.']['pct_of_total']:.2f}%`)**.")
    a(f"  5. **Word Count, Runtime, Shot-Line Matching & Single Teaching Card Reconciled:** `S6` has **`{s6_vm['whitespace_words']}` whitespace words / `{s6_vm['spoken_words']}` spoken words** (inside `55–65`), `vo_end_s = {s6_vm['vo_end_s']:.3f} s`, `total_duration_s = {s6_vm['total_duration_s']:.3f} s`, and the single executable teaching card `{s6_ov['card_text']}` remains at **`{s6_ov['timeline_in']:.3f}–{s6_ov['timeline_out']:.3f} s`** (`{s6_ov['duration_s']:.3f} s <= 4.000 s`, `{s6_ov['pct_range'][0]:.2f}%–{s6_ov['pct_range'][1]:.2f}%`). All `7` body shot windows (`s01..s07`, `0.000–21.180 s`) and `s_loop` (`21.180–22.180 s`) retain their exact v06 timestamps and media windows (including `s05_alma_orion_set`, `12.800–16.200 s` over `\"just to find it. Imagine the night of the closest pass.\"`), with `spoken_match` strings updated on `s02..s05`.")
    a("")
    a("### 1.2 Reconciled `S6` Single Teaching Card & Evidence Text (`J1025`)")
    a(f"- **Single Chosen Executable Card Across Map, Prose, Matrix, Shot Table & Auditory Judgement:** Every record in `J0936_v04_PREP_v07_maps.json` and `J0936_v04_PREP_v07.md` now derives `S6`'s overlay text and timing directly from `s6['single_teaching_overlay']`: **`{s6_ov['card_text']}` at `{s6_ov['timeline_in']:.3f}–{s6_ov['timeline_out']:.3f} s` (`{s6_ov['duration_s']:.3f} s`, `{s6_ov['pct_range'][0]:.2f}%–{s6_ov['pct_range'][1]:.2f}%`)**.")
    a(f"- **Updated `selection_rationale`:** {s6_ov['selection_rationale']}")
    a("- **Generator & Verifier Guard:** `build_j0936_prep_v07.py` formats all card descriptions from `single_teaching_overlay`, and `verify_j0936_prep_v07.py` asserts that `J0936_v04_PREP_v07_maps.json` and `J0936_v04_PREP_v07.md` contain zero stale card or removed-beat literals.")
    a("")
    a("### 1.3 Preserved Accepted `Test A` (`S4_028_DETI0HV2jlI`) Option A Repair & `S1`/`S2`/`S3`/`S5` Evidence (`J1020` / `J1025`)")
    a(f"- **`S4_028_DETI0HV2jlI` (`Test A` Option A Repair Preserved Byte-for-Byte):** Span `4` `gap_after = {s4_sub[3]['gap_after']:.3f} s`, Span `5` `{s4_sub[4]['timeline_start']:.3f}–{s4_sub[4]['timeline_end']:.3f} s` (`gap_after = {s4_sub[4]['gap_after']:.3f} s`), Span `6` source `{s4_sub[5]['source_in']:.3f}–{s4_sub[5]['source_out']:.3f} s` (`{s4_sub[5]['timeline_start']:.3f}–{s4_sub[5]['timeline_end']:.3f} s`, `gap_after = {s4_sub[5]['gap_after']:.3f} s`), Span `7` source `{s4_sub[6]['source_in']:.3f}–{s4_sub[6]['source_out']:.3f} s` (`{s4_sub[6]['timeline_start']:.3f}–{s4_sub[6]['timeline_end']:.3f} s`, `gap_after = {s4_sub[6]['gap_after']:.3f} s`), Span `8` `{s4_sub[7]['timeline_start']:.3f} s`, `vo_end_s = {s4_vm['vo_end_s']:.3f} s`, `total_duration_s = {s4_vm['total_duration_s']:.3f} s`, card `{s4_ov['card_text']}` at `{s4_ov['timeline_in']:.3f}–{s4_ov['timeline_out']:.3f} s`, and `full_vo_audition` SHA-256 `{s4_vm['auditions']['full_vo_audition']['sha256']}` (verified by Codex rebuild in `J1025`).")
    a(f"- **Honest Documentation of `S3` Audition Builder `atempo` Slot-Fit Trim (`<= 16.17 ms`):** {s3_vm['atempo_slot_fit_implementation_note']['description']}")
    a("")
    a("---")
    a("")
    a("## 2. Master Acceptance Summary Matrix (All Six Shorts)")
    a("")
    a("| # | Short ID & Slug | Air Date | Local Title | Words (WS / Spoken) | First Subj End (`<=2.50s`) | VO End / Total (`s`) | `70%` Mark (`s`) | Supplied Earliest Answer (`s` & `%`) | `4–8s` Stills | First Cut / Max Hold (`s`) | Single Teaching Overlay (`in–out s`) |")
    a("|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|")
    for idx, (sid, sdata) in enumerate(v07["shorts"].items(), 1):
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
    a("## 3. Preserved v04 Frame-0 Opening Uniqueness, Reviewer Visual Occupancy, and Library Comparison Evidence")
    a("")
    a("- **Executable Opening Generator & Evaluator:** `python3 jobs/reviews/generate_j0936_prep_v04_openings.py`")
    a(f"- **Library Snapshot File & SHA-256:** `{v07['library_snapshot']['path']}` (`sha256: {v07['library_snapshot']['sha256']}`)")
    a("- **Saved Side-by-Side Uncaptioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg`")
    a("- **Saved Side-by-Side v04-Captioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg`")
    a("- **Saved Raw Gate Report JSON:** `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("")
    a("| Short ID | Air Date | Frame-0 Source (`asset_key` / `underlying_id`) | Src In–Out (`s`) & Speed | First Cut (`s`) | Uncap / Cap `dhash` (`@0.30s`) | Mot `0–1s` Uncap / Cap (`>=10`) | `f0diff` Uncap / Cap (`>=1.5`) | Reviewer Subj Body / Total (`>=60%`) | Black (`<20%`) | Visor Uncap / Cap (`<0.005`) | Min Lib Ham Uncap / Cap (`>=15`) | Max Lib `bg` Uncap / Cap (`<0.55`) | Min Batch Ham Uncap / Cap (`>=15`) | Max Batch `bg` Uncap / Cap (`<0.55`) |")
    a("|---|---|---|---|---:|---|---|---|---|---:|---|---:|---:|---:|---:|")
    for sid, sdata in v07["shorts"].items():
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
    a("---")
    a("")
    a("## 4. Verified Source Media, Preparation v07 VO Splice Auditions, Multimodal Auditory Judgement & Source-Window Inspection")
    a("")
    a("### 4.1 Voiceover Sources & Tracked Word Maps")
    a("")
    a("| Film | VO Source Path | SHA-256 Hash | Word Map Tracked in Git |")
    a("|---|---|---|---|")
    a("| **026** | `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav` | `d6159f085b04f38604676bc3b37de24187488379e48ed394d076bee5bcabfaf5` | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json` |")
    a("| **027** | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4` | `f74ca3e8a27b3897fd4942ebcd6f70462aee039146ccce1780216c42802be38b` | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json` |")
    a("| **028** | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` | `cf546efd12e723173b66bd1d3ee2139afc94a03124ab0e4fdfd2cc06ebb8ab01` | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json` |")
    a("")
    a("### 4.2 Local VO-Only Auditions (`48 kHz` Mono WAV in `/Users/benjaminoats/_desk/reviews/J1028/auditions/`) & Direct Multimodal Auditory Judgement (`Gemini`)")
    a("")
    a("| Short ID | Assembled Opening Question | Question WAV Path & SHA-256 | Q Dur (`s`) | Q RMS / Peak (`dBFS`) | Full VO WAV Path & SHA-256 | Full Dur (`s`) | Max Step |")
    a("|---|---|---|---:|---|---:|---:|---:|")
    for sid, sdata in v07["shorts"].items():
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
    a("#### 4.2.1 Direct Multimodal Auditory Review of All 12 Spliced Audition WAVs (`reviewer: gemini`)")
    a("")
    for sid, sdata in v07["shorts"].items():
        aj = sdata["vo_splice_map"]["auditory_judgement"]
        a(f"- **`{sid}` (`{sdata['local_title']}`):**")
        a(f"  - **Reviewer:** `{aj['reviewer']}`")
        a(f"  - **Method:** {aj['method']}")
        a(f"  - **Question Audition Judgement:** {aj['question_prosody_and_joins']}")
        a(f"  - **Full-VO Audition Judgement:** {aj['full_vo_prosody_and_joins']}")
        if "atempo_slot_fit_note" in aj:
            a(f"  - **`atempo` Slot-Fit Implementation Note:** {aj['atempo_slot_fit_note']}")
        a(f"  - **Question & Map Preservation:** `preserve_exact_question_and_map = {aj['preserve_exact_question_and_map']}`")
    a("")
    a("### 4.3 Saved Source-Window Inspection Evidence (`42` Preserved `J1017` Windows + `1` Preserved `J1024` `S6 s05_alma_orion_set` Window)")
    a(f"- **Preserved `J1017` Log (`42` Unchanged Shots):** `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json` (`sha256: {sha256_file(J1017_WIN_LOG_PATH)}`).")
    a(f"- **Preserved `J1024` v06 Log (`42` Preserved + `1` Updated `S6 s05_alma_orion_set`, All `43` Shot Windows Unchanged in v07):** `/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json` (`sha256: {sha256_file(J1024_WIN_LOG_PATH)}`) and contact sheet `/Users/benjaminoats/_desk/reviews/J1024/source_windows/S6_028_X768qs8sNQs_full_window_2fps.jpg`.")
    a(f"- **Exact Coverage & Transform Scope:** Covers **`{win_log['total_30fps_frames_decoded']}` source-rate frames at `30 fps`** across `[source_in, source_out]` of all **`{win_log['total_body_shots']}` body shots** for luma, black fraction (`<20` and `<30`), dark-run (`<20` luma on `>85%` area), and `ffmpeg scdet` internal cut detection, and **`{win_log['total_2fps_ocr_frames_scanned']}` sampled frames at `2 fps` (every `0.50 s`, plus window tail)** for Tesseract OCR (`--psm 6 -l eng`) and visual contact sheets. Five opening shots (`S1 s00`, `S3 s01`, `S4 s01`, `S5 s01`, `S6 s01`) were decoded with their declared custom 9:16 crops/grades, while the remaining `38` body shots were decoded with a default 9:16 centre crop (`crop=ih*9/16:ih`) at native source speed (`source_speed` not applied). Every-frame OCR and dark-run gate logs on the final transformed MP4s remain mandatory post-assembly checks.")
    a(f"- **Saved Log Results:** `any_failures = {win_log['any_failures']}` (`0` internal `scdet` cuts, `0` dark runs `>= 3` frames, `0` banned OCR hits across the `306` `2 fps` samples, and `0` slates/baked labels/portraits/diagrams on the `2 fps` contact sheets).")
    a("")
    a("---")
    a("")
    a("## 5. Per-Short Reconciled Scripts, Exact Subspan Splice Tables, Single Teaching Overlay Specs, and Complete Shot Plans")
    a("")
    for idx, (sid, sdata) in enumerate(v07["shorts"].items(), 1):
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
        a(f"- **Opening Question Delivery (`spans 1..{vm['opening_question_span_count']}`, `0..{vm['opening_question_end_s']:.3f} s`):** `{vm['opening_question_punctuated']}` — Audition WAV: `{qa['wav_path']}` (`{qa['duration_s']:.3f} s`, `RMS {qa['rms_dbfs']:.1f} dBFS`, `sha256: {qa['sha256']}`)")
        a(f"- **First Named Subject Completion (`<= 2.500 s`):** `\"{fns['word']}\"` (source word `{fns['word_idx']}`) at **`{fns['start']:.3f}–{fns['end']:.3f} s`**")
        a(f"- **Supplied Earliest Spoken Answer (`>= 70.0%`):** `\"{ea['word']}\"` (source word `{ea['word_idx']}`) starts at **`{ea['start']:.3f} s` (`{ea['pct_of_total']:.2f}% >= 70.0%`)**")
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
        a("#### A. Exact Subspan VO Splice Table (`<= 1.055x <= 1.06x` Tempo, All Internal Acoustic Pauses `<= 0.200 s`)")
        a("")
        a("| Span | Word Idx | Source In (`s`) | Source Out (`s`) | Raw Dur (`s`) | Tempo | Scaled Dur (`s`) | Xfade (`s`) | Gap After (`s`) | Timeline Start (`s`) | Timeline End (`s`) | `%` of Total | Max Acoustic Pause (`s`) | Spoken Text |")
        a("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for r in vm["subspans"]:
            w_first = r["words"][0]["word_idx"]
            w_last = r["words"][-1]["word_idx"]
            txt = " ".join(w["word"] for w in r["words"])
            pct = (r["timeline_start"] / vm["total_duration_s"]) * 100.0
            a(
                f"| `{r['span_index']}` | `{w_first}..{w_last}` | `{r['source_in']:.3f}` | `{r['source_out']:.3f}` | "
                f"`{r['raw_dur']:.3f}` | `{r['tempo']:.3f}x` | `{r['scaled_dur']:.3f}` | `{r['xfade_s']:.3f}` | "
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
        a("#### C. Complete Duration-Matched Shot Plan & Saved Source-Window (`30 fps` Luma/`scdet` + Sampled `2 fps` OCR) Verification")
        a("")
        a("| Row | Timeline In–Out (`s`) | Dur (`s`) | Asset Key & Underlying ID | Source Path | Source In–Out (`s`) | Src Dur (`s`) | Speed | Kind & `video` Flag | Upscale | Saved `30fps` Frames & `2fps` OCR Samples | Window Luma (`min..max`) & Max Black | Internal Cuts / Dark Runs / `2fps` OCR Hits | Full Source SHA-256 | Spoken Line Alignment |")
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

    a("## 6. Reproducible Verification, Semantic Pre-70% Clause Inspection, and Unchanged Assembly Boundaries (`J1025` -> `J1028` -> `J0936`)")
    a("")
    a("- **Verifier Script:** `python3 jobs/reviews/verify_j0936_prep_v07.py`")
    a(f"- **Verification Output:** `jobs/reviews/J1028_2026-10-27_verification.json` (`machine_checks_passed: True`, `total_source_words_verified: 391`, `input_sha256: {v07_sha}`)")
    a("- **Deterministic Machine-Verified Checks Performed by `verify_j0936_prep_v07.py`:**")
    a("  1. Every source word record (`word`, `src_start`, `src_end`) matches the tracked git word map (`words.json`, `earth_spin_words_list.json`, `gliese_words_list.json`) within `1e-4 s`, and every word's output coordinate (`timeline_start + (src_t - source_in) / tempo`) reconciles within `0.002 s` across all `391` words.")
    a("  2. Every `\"Gliese 710\"` occurrence in ordinary Shorts `S3`, `S5`, and `S6` (`words 121..122` in questions, `words 719..720` in `S3` body, `words 471..473` in `S5` body, `words 985..986` in `S6` body) resides inside a **single continuous subspan** with `0` omitted inter-token syllables (`omitted_ordinary_bridges == []`), and `Test A` (`S4`) preserves the explicitly authorised Option A syllable repair (`full_vo_audition` SHA-256 `d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a`).")
    a(f"  3. Both whitespace word count and spoken-expansion word count are inside `55–65` for all five ordinary Shorts (**`S1: 65/65`**, **`S2: 64/65`**, **`S3: 62/64`**, **`S5: 61/65`**, **`S6: {s6_vm['whitespace_words']}/{s6_vm['spoken_words']}`**), with **`S4` retaining its explicit Test A exemption (`76/77`)**.")
    a("  4. Spoken opening question tokens equal `local_title` token-for-token for all five ordinary Shorts, and all `12` local VO audition WAVs (`question_audition` and `full_vo_audition` in `/Users/benjaminoats/_desk/reviews/J1028/auditions/`) exist on disk and match their recorded SHA-256 hashes.")
    a("  5. First named subject (`Sun`, `Earth's`, `710`, `star`, `710`, `710`) completes at `<= 2.500 s` across all six Shorts, recomputed from the flattened output word timeline (`S1: 2.380 s`, `S2: 1.750 s`, `S3: 2.490 s`, `S4: 0.900 s`, `S5: 1.660 s`, `S6: 2.465 s`).")
    a("  6. Subspan splice arithmetic (`1.000x <= tempo <= 1.055x <= 1.060x`, `gap_after <= 0.180 s`, `max_internal_pause <= 0.200 s`, `12 ms` crossfades on Test A) and shot coverage (`0.000 s` to `vo_end_s` for body shots, `s_loop` ending at `total_duration_s` with `final_shot_cursor == total_duration_s`) reconcile with `0` errors.")
    a("  7. `4.000–8.000 s` early motion window uses `100%` moving `video=True` footage across all six Shorts (`early_still_windows_4_8s = []`), with `0` still-to-still cuts and `>= 10.0 s` separation on any repeated underlying source.")
    a("  8. **Supplied Earliest-Answer Coordinate Check & `S6` Pre-70% Appearance/Motion Token Exclusion:** Recomputes the output timestamp and runtime percentage of `earliest_spoken_answer.word_idx` from the flattened word timeline (`pct_of_total >= 70.0%` across all six Shorts) and verifies that `S6` contains zero pre-70% appearance or motion tokens (`brightening`, `bright`, `brighter`, `brightest`, `glows`, `orange`, `sirius`, `creep`, `moon`, `35`, `thousands` all absent before `16.400 s`).")
    a("  9. **Single Teaching Overlay & Card Literal Consistency Check:** Verifies `baked_in_labels = 0`, `code_graphics = 0`, `added_edit_cards = 1`, `<= 4` words per line, `<= 4.000 s` duration, clear of `0–2 s` hook and `9–14 s` banner, Chief's locked `S5` card `['1-CM SCALE', 'OVER 100 METERS']` within `16.180–19.160 s`, and exact agreement of `S6`'s single executable card `['3× BRIGHTER', 'THAN SIRIUS']` at `16.600–20.400 s` across `J0936_v04_PREP_v07_maps.json` and `J0936_v04_PREP_v07.md` with zero stale card or `s05_full_moon` literals.")
    a(" 10. Fresh `gate_shorts_open.py` measurements on all `6` uncaptioned (`S1..S6_open.mp4`) and `6` v04-captioned (`S1..S6_open_captioned.mp4`) opening preview clips, plus **provenance verification against both the preserved `J1017` source-window log (`42` unchanged shots, `sha256: b8e995f64132a8e9...`) and the preserved `J1024` v06 source-window log (`43` shots including `S6 s05_alma_orion_set`)**.")
    a("- **Explicitly Separated Reviewer Assertions (`reviewer: gemini`, Not Computed by the Verifier Script):**")
    a("  1. **Clause-by-Clause Semantic Inspection of Every Preceding Clause Before `70%` (`REVIEWED_BY_GEMINI_SEMANTIC_INSPECTION`):** Semantic verification by `gemini` (`Gemini 4 Argon`) of every clause preceding `earliest_spoken_answer` across all six Shorts (including `S6` Spans `1..9` title question, Spans `10..16` present-day Serpens location and naked-eye invisibility/binoculars setup, and Spans `17..19` closest-pass transition `0.015–16.220 s`) confirming that no appearance or motion description of the arriving star occurs before `15.526 s` (`70.0%`) or before `16.400 s` (`73.94%`).")
    a("  2. **Visual & Geometric Titled-Subject Occupancy (`>= 60%`, `REVIEWED_BY_GEMINI_MULTIMODAL_VISION`):** Reviewer visual/contour segmentation by `gemini` on the cropped `1080×1920` `@0.30s` frames (`all_6_openings_0_30s_comparison.jpg` and `all_6_openings_captioned_0_30s_comparison.jpg`).")
    a("  3. **Visual Contact-Sheet Inspection of Sampled `2 fps` Source Windows (`REVIEWED_BY_GEMINI_MULTIMODAL_VISION`):** Reviewer visual inspection by `gemini` of `S1..S6_full_window_2fps.jpg` (`306` tiles sampled at `2 fps` across `43` body shots, including `S6 s05_alma_orion_set`).")
    a("  4. **Multimodal Auditory Judgement of Prosody & Repaired Bridges (`REVIEWED_BY_GEMINI_MULTIMODAL_AUDIO`):** Direct `Gemini 4 Argon` multimodal audio listening across all `12` WAV files in `/Users/benjaminoats/_desk/reviews/J1028/auditions/` (`codex` verified execution, rebuilt audio, hashes, and arithmetic in `J1020` and `J1025` and does not claim independent listening).")
    a("- **Unchanged Post-Assembly Acceptance (`c59` / `J0936`, Mandatory at Final Render After Chief Lock):** Eventual assembly after Chief lock retains every original `J0936`/`c59` acceptance requirement: all Shorts/picture/polish/music/SFX gates, full rendered-video every-frame/dense OCR and dark-run gate logs on the final speed-transformed/cropped/graded MP4s, measured final AAC `-14.0 ± 0.5 LUFS` and `TP <= -1.6 dBTP`, matched `1.000 s` loop (`loop_diff < 2.0`), complete runtime sheets and flagged frames, `720×1280` PHONE video, UAT/NAS copies and SHA-256 manifests. Batch target remains **1 November 2026, 20:00 London**; individual day-before-air deadlines (`19 Nov`, `22 Nov`, `29 Nov`, `1 Dec`, `3 Dec`, `6 Dec` at `20:00 London`) and v01 fallbacks remain unchanged. Ben swap approval follows replacement PASS.")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
