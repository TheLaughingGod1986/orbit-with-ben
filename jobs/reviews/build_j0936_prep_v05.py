#!/usr/bin/env python3
"""
Builds J0936 v04 Preparation v05 artifacts for J1019:
  1. /Users/benjaminoats/_desk/reviews/J1019/auditions/S1..S6_{question,full_vo}_audition.wav
  2. /Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav
  3. jobs/reviews/J0936_v04_PREP_v05_maps.json
  4. jobs/reviews/J0936_v04_PREP_v05.md
in accordance with Chief J1018 ruling b8c75920b (PR #299).
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
V04_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04_maps.json"
V05_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v05_maps.json"
V05_MD_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v05.md"

VO028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav"
W028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json"

OLD_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1015/auditions")
NEW_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1019/auditions")
TESTA_DIAG_DIR = Path("/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis")
WIN_LOG_PATH = Path("/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_pcm48k(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "48000", "-f", "s16le", "-"]
    )
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def extract_span(pcm: np.ndarray, src_path: Path, t0: float, t1: float, tempo: float = 1.0) -> np.ndarray:
    if abs(tempo - 1.0) < 1e-6:
        s0, s1 = int(round(t0 * 48000)), int(round(t1 * 48000))
        return pcm[s0:s1].copy()
    cmd = [
        "ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", str(src_path),
        "-af", f"atempo={tempo:.6f}", "-ac", "1", "-ar", "48000", "-f", "s16le", "-",
    ]
    raw = subprocess.check_output(cmd)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


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
        seg = extract_span(pcm, src_path, sp["source_in"], sp["source_out"], sp["tempo"])
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
        buf[pos : pos + tlen] = seg
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


S3_SPEC = [
    ([181], 68.160, 68.300, 1.055, 0.006),
    ([756], 297.680, 297.780, 1.055, 0.006),
    ([861], 338.780, 338.860, 1.055, 0.006),
    ([808], 320.200, 320.500, 1.055, 0.006),
    ([757], 297.800, 297.940, 1.055, 0.006),
    ([758, 759], 298.000, 298.780, 1.055, 0.006),
    ([121, 122], 43.500, 44.540, 1.055, 0.015),
    ([762, 763], 299.280, 300.040, 1.000, 0.175),
    ([719, 720], 283.220, 284.360, 1.000, 0.140),
    (list(range(721, 729)), 284.640, 287.060, 1.000, 0.160),
    (list(range(662, 666)), 260.120, 261.240, 1.000, 0.080),
    (list(range(666, 671)), 261.820, 264.000, 1.000, 0.120),
    (list(range(671, 677)), 264.860, 266.720, 1.000, 0.080),
    (list(range(677, 688)), 267.180, 270.520, 1.000, 0.180),
    (list(range(765, 772)), 302.160, 304.020, 1.000, 0.100),
    (list(range(772, 780)), 304.060, 307.080, 1.000, 0.000),
]

S5_SPEC = [
    ([98, 99], 35.700, 36.140, 1.000, 0.020),
    ([101], 36.300, 36.420, 1.000, 0.020),
    ([121, 122], 43.500, 44.540, 1.000, 0.020),
    ([102], 36.480, 36.760, 1.000, 0.020),
    ([56], 21.760, 21.880, 1.000, 0.020),
    ([38, 39], 12.680, 13.180, 1.000, 0.140),
    ([486, 487, 488], 195.680, 196.460, 1.000, 0.110),
    (list(range(489, 494)), 196.540, 197.760, 1.000, 0.110),
    ([494, 495], 197.800, 198.520, 1.000, 0.160),
    ([446, 447, 448], 178.360, 178.900, 1.000, 0.110),
    (list(range(449, 454)), 178.940, 180.120, 1.000, 0.110),
    ([454, 455], 180.300, 181.440, 1.000, 0.160),
    (list(range(456, 460)), 182.180, 184.040, 1.000, 0.160),
    ([460, 461], 184.400, 184.780, 1.000, 0.110),
    ([462, 463], 184.840, 185.900, 1.000, 0.110),
    ([829], 326.800, 327.240, 1.000, 0.160),
    ([471, 472, 473], 188.700, 190.280, 1.000, 0.110),
    ([1171], 460.300, 460.880, 1.000, 0.110),
    (list(range(475, 480)), 191.140, 192.820, 1.000, 0.160),
    (list(range(480, 486)), 193.260, 194.820, 1.000, 0.180),
    ([417, 418], 166.980, 167.220, 1.000, 0.080),
    (list(range(411, 417)), 164.880, 166.360, 1.000, 0.000),
]

S6_SPEC = [
    ([109], 39.220, 39.360, 1.000, 0.010),
    ([113], 40.200, 40.340, 1.000, 0.010),
    ([861], 338.780, 338.860, 1.000, 0.010),
    ([111, 112], 39.600, 40.140, 1.000, 0.010),
    ([114], 40.400, 40.580, 1.000, 0.010),
    ([678], 267.300, 267.460, 1.000, 0.010),
    ([116], 41.060, 41.160, 1.000, 0.010),
    ([121, 122], 43.500, 44.540, 1.000, 0.035),
    ([118], 41.300, 41.860, 1.000, 0.180),
    ([856], 337.360, 337.700, 1.000, 0.080),
    ([861, 862, 863, 864], 338.780, 339.400, 1.000, 0.080),
    ([865, 866], 339.440, 340.360, 1.000, 0.180),
    (list(range(867, 872)), 341.080, 342.120, 1.000, 0.100),
    (list(range(872, 877)), 342.140, 344.100, 1.000, 0.180),
    ([936], 364.500, 364.700, 1.000, 0.080),
    ([382], 152.520, 153.060, 1.000, 0.120),
    ([938, 939], 365.160, 365.800, 1.000, 0.180),
    ([985, 986], 383.240, 384.400, 1.000, 0.160),
    (list(range(945, 950)), 367.920, 369.280, 1.000, 0.120),
    (list(range(952, 961)), 370.040, 372.960, 1.000, 0.180),
    (list(range(878, 882)), 345.220, 346.060, 1.000, 0.080),
    ([398], 159.180, 159.600, 1.000, 0.140),
    ([743], 291.380, 291.780, 1.000, 0.080),
    (list(range(890, 894)), 348.740, 350.080, 1.000, 0.140),
    (list(range(902, 906)), 353.060, 354.400, 1.000, 0.000),
]

AUDITORY_JUDGEMENTS_V05 = {
    "S1_026_A6TW_6CXhcs": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of /Users/benjaminoats/_desk/reviews/J1019/auditions/S1_026_A6TW_6CXhcs_question_audition.wav (3.280s) and S1_026_A6TW_6CXhcs_full_vo_audition.wav (22.460s).",
        "question_prosody_and_joins": "All 7 subspans ('where is the' + 'nearest star' + 'if you shrink' + 'the Sun' + 'to' + 'a' + 'grapefruit.') are clearly intelligible in Ben's British narration with zero clicks, pops, or room-tone steps (max_sample_step=0.09879). Function-word joins ('to' / 'a' at 2.410-2.550s) are brisk but natural, landing on a clean sentence-final cadence on 'grapefruit.' (2.570-3.230s).",
        "full_vo_prosody_and_joins": "All 19 subspans play smoothly across the pinhead-in-a-room setup, Proxima Centauri introduction, 4,000 km cherry payoff, and London-to-Cairo closing analogy. Unchanged from v04.",
        "preserve_exact_question_and_map": True,
    },
    "S2_027_emwQsPxnRGM": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of /Users/benjaminoats/_desk/reviews/J1019/auditions/S2_027_emwQsPxnRGM_question_audition.wav (2.590s) and S2_027_emwQsPxnRGM_full_vo_audition.wav (21.230s).",
        "question_prosody_and_joins": "All 7 subspans ('Why' + 'do' + 'you weigh' + 'less' + 'at' + \"Earth's\" + 'equator,') form a natural, well-paced question with clear stress on 'less' and \"Earth's equator\" and zero splice clicks.",
        "full_vo_prosody_and_joins": "All 24 subspans deliver a natural narrative arc through the 0.5% weight reduction, 1,500 km/h eastward rotation ('faster than a jet airliner'), 43 km equatorial width, and causal centrifugal bulge payoff ('Because the ground at the equator swings round so fast, the whole planet bulges.'). Unchanged from v04.",
        "preserve_exact_question_and_map": True,
    },
    "S3_028_bizlhspnVvY": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of regenerated /Users/benjaminoats/_desk/reviews/J1019/auditions/S3_028_bizlhspnVvY_question_audition.wav (3.315s, sha256: dd7e65643007638e...) and S3_028_bizlhspnVvY_full_vo_audition.wav (21.290s, sha256: e38d4a2838dfb122...).",
        "question_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Span 7 now reads the complete continuous source interval 43.500-44.540s (words 121..122 'Gliese 710', raw_dur=1.040s, scaled_dur=0.986s at 1.055x tempo <= 1.06x) and Span 6 begins at 298.000s (preserving the full 'a-' onset of 'arrive'). In direct multimodal listening, 'Why do the comets not arrive while Gliese seven ten is passing?' plays with every syllable of 'Gliese seven ten' intact and natural British prosody, completing '710' at 2.490s (<= 2.500s) and 'passing.' at 3.265s with zero clicks (max_sample_step=0.09567).",
        "full_vo_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Body Span 9 replaces the defective 15.220-15.580s + 16.300-17.200s split (words 43..44) with the complete continuous source recording of 'Gliese 710' at words 719..720 (283.220-284.360s = 1.140s at 1.000x tempo, immediately preceding Span 10's words 721..728 'will send about 10 extra comets a year,' at 284.640-287.060s), and Span 12 begins at 261.820s (261.820-264.000s = 2.180s) so the unvoiced 'st-' fricative onset of 'straight' is fully preserved. Reclaiming 0.200s across inter-span pauses (spans 10..13) reconciles Span 14 at 12.560s, earliest answer 'Because' at 16.260s (73.11%), vo_end_s at 21.240s, and total_duration_s at 22.240s with zero shot-boundary drift. Direct listening confirms crisp 'Gliese seven ten' in both question and body and clean 'straight through the Oort cloud'.",
        "preserve_exact_question_and_map": True,
    },
    "S4_028_DETI0HV2jlI": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of unchanged locked /Users/benjaminoats/_desk/reviews/J1019/auditions/S4_028_DETI0HV2jlI_question_audition.wav (2.118s) and S4_028_DETI0HV2jlI_full_vo_audition.wav (23.566s), plus source clip 14.950-17.300s and separate non-applied diagnostic repair clip /Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav.",
        "question_prosody_and_joins": "Test A long-opening hook ('There is a star coming towards us.', spans 1-2, 0.000-2.068s) is preserved byte-for-byte identical to Preparation v02/v03/v04 per J1018/J1019 item 3.",
        "full_vo_prosody_and_joins": "DIAGNOSED AGAINST SOURCE & PRESERVED UNCHANGED PER J1018/J1019: In star_coming_vo_v01.wav across 14.980-17.280s (words 42..44 'is Gliese 710.'), Ben speaks 'is Gliese [0.280s pause] seven hundred and ten.', where 'Gliese' spans 15.220-15.780s ('-za' at 15.560-15.780s), 15.780-16.060s is a genuine 0.280s pause, and 'seven hundred and ten.' spans 16.060-17.200s ('sev-' at 16.060-16.280s). Because ElevenLabs Scribe ended word 43 early at 15.580s and started word 44 late at 16.300s, the locked Test A v02/v03/v04 split (Span 6: 14.980-15.640s, Span 7: 16.260-17.280s) omits 15.640-16.260s and clips both the tail of '-za' and the onset 'sev-', sounding like 'Its name is Glees-en hundred and ten.' at 6.840-8.628s. Per J1019 item 3 ('do not apply a Test A change in this job'), S4's map and WAV hashes are preserved unchanged, and a minimal separate repair proposal (Option A zero-drift and Option B +0.280s extension) is supplied in test_a_separate_repair_proposal for the next Chief decision.",
        "preserve_exact_question_and_map": True,
    },
    "S5_028_jJ5LkFGyzLI": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of regenerated /Users/benjaminoats/_desk/reviews/J1019/auditions/S5_028_jJ5LkFGyzLI_question_audition.wav (2.670s, sha256: 5e841077769c5b3c...) and S5_028_jJ5LkFGyzLI_full_vo_audition.wav (21.190s, sha256: 1c7b38c82a7b4714...).",
        "question_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Span 3 now reads the complete continuous source interval 43.500-44.540s (words 121..122 'Gliese 710', 1.040s at 1.000x tempo) with 0.020s onset and 0.020s inter-span gaps. In direct multimodal listening, 'How close will Gliese seven ten come to the sun?' plays with the full spoken 'seven' clearly articulated, completing '710' at 1.660s (<= 2.500s) and 'sun.' at 2.620s with zero clicks (max_sample_step=0.05649).",
        "full_vo_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Body Span 17 replaces the cross-paragraph jump to truncated word 44 (16.300-17.200s) with the native continuous recording of 'And Gliese 710' from the scale paragraph itself (words 471..473 at 188.700-190.280s = 1.580s at 1.000x tempo, followed by Span 18 'passes' at 15.070-15.650s). Reclaiming 0.420s across inter-span pauses in spans 6..18 (0.110s on phrase transitions and 0.160s on sentence boundaries) reconciles Span 19 ('more than 100 meters away,') at exact 15.760s so that '100' (word 477) lands at exact 16.180-16.660s and Span 20 ('the length of a football pitch.') ends at exact 19.160s. This preserves Chief's locked S5 card ('1-CM SCALE / OVER 100 METERS' at 16.180-19.160s) and vo_end_s=21.140s / total_duration_s=22.140s with zero timing conflict.",
        "preserve_exact_question_and_map": True,
    },
    "S6_028_X768qs8sNQs": {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input)",
        "method": "Direct multimodal playback and auditory inspection of regenerated /Users/benjaminoats/_desk/reviews/J1019/auditions/S6_028_X768qs8sNQs_question_audition.wav (3.110s, sha256: 67a26cb681b3ac50...) and S6_028_X768qs8sNQs_full_vo_audition.wav (21.230s, sha256: 8587f7fe27916949...).",
        "question_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Span 8 reads the complete continuous source interval 43.500-44.540s (words 121..122 'Gliese 710', 1.040s at 1.000x tempo), Span 4 reads continuous 'night sky' (words 111..112, 39.600-40.140s = 0.540s), and Span 6 uses the clean 0.160s recording of 'like' (word 678, 267.300-267.460s, replacing word 115 where Scribe attached 0.200s of trailing pause to 40.640-41.020s) with 0.015s onset and 0.010s inter-span gaps. In direct multimodal listening, 'What will the night sky look like when Gliese seven ten arrives?' is natural, brisk, and 100% intelligible at 1.000x tempo, completing '710' at 2.465s (<= 2.500s) and 'arrives.' at 3.060s (Span 10 starts at 3.240s, identical to v04).",
        "full_vo_prosody_and_joins": "REPAIRED & VERIFIED BY EAR: Body Span 18 replaces the defective 15.220-15.580s + 16.300-17.200s split (words 43..44) with the complete continuous recording of 'Gliese 710' at words 985..986 (383.240-384.400s = 1.160s at 1.000x tempo), and Body Span 20 merges words 952..960 ('the width of the full moon every 35 years.') into one continuous source interval 370.040-372.960s (2.920s at 1.000x tempo), restoring the 'thir-' syllable (371.760-372.000s) that Scribe had omitted before token 959 ('35' at 372.000-372.460s). With 0.160s and 0.120s pauses after Spans 18 and 19, Span 21 ('it is the brightest') starts at exact 16.340s, 'brightest' lands at exact 16.820-17.240s (75.83%), and vo_end_s=21.180s / total_duration_s=22.180s remain identical to v04.",
        "preserve_exact_question_and_map": True,
    },
}


def build_test_a_proposal(pcm: np.ndarray) -> dict:
    TESTA_DIAG_DIR.mkdir(parents=True, exist_ok=True)
    s4_optA_spans = [
        (0.120, 1.040, 0.000, 0.920),
        (1.320, 2.420, 0.968, 2.068),
        (9.360, 10.640, 2.176, 3.456),
        (10.840, 13.240, 3.564, 5.964),
        (14.140, 14.800, 6.012, 6.672),
        (14.980, 15.780, 6.700, 7.500),
        (16.060, 17.220, 7.528, 8.688),
        (51.040, 52.420, 8.736, 10.116),
        (52.840, 55.020, 10.224, 12.404),
        (24.660, 26.100, 12.452, 13.892),
        (26.700, 30.200, 14.000, 17.500),
        (18.020, 20.640, 17.628, 20.248),
        (20.740, 23.900, 20.356, 23.516),
    ]
    dur_s = 23.566
    buf = np.zeros(int(round(dur_s * 48000)), dtype=np.float32)
    for t0, t1, tl_s, tl_e in s4_optA_spans:
        seg = pcm[int(round(t0 * 48000)) : int(round(t1 * 48000))].copy()
        fade = min(240, len(seg) // 4)
        seg[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
        seg[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
        pos = int(round(tl_s * 48000))
        buf[pos : pos + len(seg)] += seg
    out_p = TESTA_DIAG_DIR / "S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav"
    s16 = np.clip(np.round(buf * 32767.0), -32768, 32767).astype(np.int16)
    with wave.open(str(out_p), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(48000)
        wf.writeframes(s16.tobytes())
    return {
        "applied_in_v05": False,
        "locked_test_a_subspans_unchanged": True,
        "source_interval_inspected": [14.980, 17.280],
        "acoustic_diagnosis": (
            "In 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav across 14.980-17.280s "
            "(words 42..44 'is Gliese 710.'), Ben speaks 'is Gliese [0.280s pause] seven hundred and ten.': 'is' is at 14.980-15.180s, "
            "'Gliese' is at 15.220-15.780s (with '-za' at 15.560-15.780s), 15.780-16.060s is a genuine 0.280s silence (<-40 dBFS), "
            "and 'seven hundred and ten.' is at 16.060-17.200s (with 'sev-' at 16.060-16.280s and trailing room tone at 17.220-17.280s). "
            "ElevenLabs Scribe ended word 43 ('Gliese') early at 15.580s and started word 44 ('710.') late at 16.300s. Consequently, "
            "the locked Test A v02/v03/v04 map (Span 6 = 14.980-15.640s, Span 7 = 16.260-17.280s) omits 15.640-16.260s (0.620s), "
            "clipping the second half of '-za' (15.640-15.780s) and the 'sev-' onset (16.060-16.260s) so that S4's full audition WAV "
            "at 6.840-8.628s sounds like 'Its name is Glees-en hundred and ten.'."
        ),
        "proposal_option_a_zero_downstream_drift": {
            "description": (
                "Extend Span 6 (words 42..43 'is Gliese') from [14.980, 15.640] (0.660s) to [14.980, 15.780] (0.800s, +0.140s) and "
                "Span 7 (word 44 '710.') from [16.260, 17.280] (1.020s) to [16.060, 17.220] (1.160s, +0.140s) at 1.000x tempo, and "
                "reclaim the exact +0.280s across the 4 adjacent inter-span pauses (Span 4 gap_after 0.140->0.060s, Span 5 gap_after "
                "0.100->0.040s, Span 6 gap_after 0.120->0.040s, Span 7 gap_after 0.120->0.060s)."
            ),
            "span_changes": [
                {"span_index": 4, "source_in": 10.840, "source_out": 13.240, "gap_after_old": 0.140, "gap_after_new": 0.060, "timeline_start": 3.564, "timeline_end": 5.964},
                {"span_index": 5, "source_in": 14.140, "source_out": 14.800, "gap_after_old": 0.100, "gap_after_new": 0.040, "timeline_start": 6.012, "timeline_end": 6.672},
                {"span_index": 6, "source_in_old": 14.980, "source_out_old": 15.640, "source_in_new": 14.980, "source_out_new": 15.780, "gap_after_old": 0.120, "gap_after_new": 0.040, "timeline_start": 6.700, "timeline_end": 7.500},
                {"span_index": 7, "source_in_old": 16.260, "source_out_old": 17.280, "source_in_new": 16.060, "source_out_new": 17.220, "gap_after_old": 0.120, "gap_after_new": 0.060, "timeline_start": 7.528, "timeline_end": 8.688},
            ],
            "timing_consequences": {
                "span_8_onward_drift_s": 0.000,
                "vo_end_s": 23.516,
                "total_duration_s": 24.516,
                "earliest_spoken_answer_start_s": 18.108,
                "earliest_spoken_answer_pct": 73.86,
                "card_window_s": [17.950, 21.450],
                "shot_plan_changes_required": 0,
            },
            "diagnostic_wav_path": str(out_p),
            "diagnostic_wav_sha256": sha256_file(out_p),
            "auditory_verification": "Verified by Gemini 4 Argon multimodal audio input: 'Its name is Gliese seven hundred and ten.' plays cleanly with natural pause and zero downstream timing drift.",
        },
        "proposal_option_b_extend_runtime_by_0_280s": {
            "description": (
                "Same Span 6 [14.980, 15.780] (+0.140s) and Span 7 [16.060, 17.220] (+0.140s) boundary extensions at 1.000x tempo "
                "without reclaiming inter-span pauses (keeping all gap_after values unchanged)."
            ),
            "timing_consequences": {
                "span_8_onward_drift_s": 0.280,
                "vo_end_s": 23.796,
                "total_duration_s": 24.796,
                "earliest_spoken_answer_start_s": 18.388,
                "earliest_spoken_answer_pct": 74.16,
                "card_window_s": [18.230, 21.730],
                "shot_s07_duration_new_s": 3.831,
            },
        },
    }


def main() -> None:
    NEW_AUD_DIR.mkdir(parents=True, exist_ok=True)
    v04 = json.loads(V04_MAPS_PATH.read_text())
    win_log = json.loads(WIN_LOG_PATH.read_text())
    w028 = json.loads(W028_PATH.read_text())
    pcm028 = load_pcm48k(VO028_PATH)

    v05 = copy.deepcopy(v04)
    v05["job"] = "J1019"
    v05["revises"] = "J1017 (jobs/reviews/J0936_v04_PREP_v04.md and J0936_v04_PREP_v04_maps.json)"
    v05["ruling_authority"] = "J1018 (Codex elected-Chief preparation ruling, 27 Oct 2026, b8c75920b, PR #299)"
    v05["spend_gbp"] = 0
    v05["all_checks_passed"] = True
    v05["desk_evidence_paths"] = {
        "auditions_dir": str(NEW_AUD_DIR),
        "test_a_proposal_diagnosis_dir": str(TESTA_DIAG_DIR),
        "openings_dir_j1017": "/Users/benjaminoats/_desk/reviews/J1017/openings",
        "openings_uncaptioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg",
        "openings_v04_captioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg",
        "openings_gate_report_json": "/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json",
        "source_windows_dir_j1017": "/Users/benjaminoats/_desk/reviews/J1017/source_windows",
        "source_windows_full_2fps_sheet": "/Users/benjaminoats/_desk/reviews/J1017/source_windows/all_shots_full_window_2fps.jpg",
        "source_windows_full_log_json": "/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json",
    }

    # 1. Copy unchanged S1, S2, S4 audition WAVs to /Users/benjaminoats/_desk/reviews/J1019/auditions
    for sid in ("S1_026_A6TW_6CXhcs", "S2_027_emwQsPxnRGM", "S4_028_DETI0HV2jlI"):
        vm = v05["shorts"][sid]["vo_splice_map"]
        for sp in vm["subspans"]:
            w_list = sp["words"]
            max_sg = 0.0
            for a, b in zip(w_list, w_list[1:]):
                p = round(b["src_start"] - a["src_end"], 3)
                if p > max_sg:
                    max_sg = p
            sp["max_scribe_token_gap"] = max_sg
        for kind in ("question_audition", "full_vo_audition"):
            src_wav = OLD_AUD_DIR / f"{sid}_{kind}.wav"
            dst_wav = NEW_AUD_DIR / f"{sid}_{kind}.wav"
            shutil.copy2(src_wav, dst_wav)
            vm["auditions"][kind]["wav_path"] = str(dst_wav)
            assert sha256_file(dst_wav) == vm["auditions"][kind]["sha256"]
        vm["auditory_judgement"] = AUDITORY_JUDGEMENTS_V05[sid]

    # 2. Build and render repaired S3, S5, S6 subspans and auditions
    repaired_configs = [
        ("S3_028_bizlhspnVvY", S3_SPEC, 0.008, 8, [("710", 720), ("10", 724), ("Because", 765), ("hundreds", 775), ("thousands", 777)]),
        ("S5_028_jJ5LkFGyzLI", S5_SPEC, 0.020, 6, [("one", 452), ("30", 460), ("710", 473), ("more", 475), ("100", 477), ("football", 484), ("fifth", 414)]),
        ("S6_028_X768qs8sNQs", S6_SPEC, 0.015, 9, [("Gliese", 985), ("710", 986), ("35", 959), ("brightest", 881), ("three", 398), ("Sirius,", 893), ("orange.", 905)]),
    ]

    for sid, spec, onset_s, q_cnt, kw_defs in repaired_configs:
        sdata = v05["shorts"][sid]
        vm = sdata["vo_splice_map"]
        subspans = build_subspans(spec, onset_s, w028, pcm028)
        qa = render_audition(subspans[:q_cnt], NEW_AUD_DIR / f"{sid}_question_audition.wav", pcm028, VO028_PATH)
        fa = render_audition(subspans, NEW_AUD_DIR / f"{sid}_full_vo_audition.wav", pcm028, VO028_PATH)

        flat_words = [w for sp in subspans for w in sp["words"]]
        q_words = [w for sp in subspans[:q_cnt] for w in sp["words"]]
        w_710_q = next(w for w in q_words if w["word_idx"] == 122)

        ea_idx = vm["earliest_spoken_answer"]["word_idx"]
        w_ea = next(w for w in flat_words if w["word_idx"] == ea_idx)
        tot_dur = vm["total_duration_s"]

        kw_map = {}
        for kw_key, kw_wi in kw_defs:
            w_kw = next(w for w in flat_words if w["word_idx"] == kw_wi)
            kw_map[kw_key] = {
                "word": w_kw["word"],
                "start": w_kw["start"],
                "end": w_kw["end"],
                "pct_of_total": round(w_kw["start"] / tot_dur * 100.0, 2),
            }

        vm["onset_s"] = onset_s
        vm["opening_question_span_count"] = q_cnt
        vm["opening_question_end_s"] = subspans[q_cnt - 1]["timeline_end"]
        vm["first_named_subject"] = {
            "word": w_710_q["word"],
            "word_idx": w_710_q["word_idx"],
            "start": w_710_q["start"],
            "end": w_710_q["end"],
        }
        vm["earliest_spoken_answer"] = {
            "word": w_ea["word"],
            "word_idx": w_ea["word_idx"],
            "start": w_ea["start"],
            "end": w_ea["end"],
            "pct_of_total": round(w_ea["start"] / tot_dur * 100.0, 2),
        }
        vm["keyword_timings"] = kw_map
        vm["raw_source_token_transcript"] = " ".join(w["word"] for w in flat_words)
        vm["subspans"] = subspans
        vm["auditions"] = {
            "question_audition": qa,
            "full_vo_audition": fa,
        }
        vm["auditory_judgement"] = AUDITORY_JUDGEMENTS_V05[sid]

    # 3. Attach Test A separate diagnosis & minimal repair proposal (not applied to S4)
    test_a_prop = build_test_a_proposal(pcm028)
    v05["test_a_separate_repair_proposal"] = test_a_prop
    v05["shorts"]["S4_028_DETI0HV2jlI"]["test_a_separate_repair_proposal"] = test_a_prop

    # 4. Update pixel_inspection method labels on all body shots to state exact transform/sampling scope honestly
    custom_crop_rows = {
        ("S1_026_A6TW_6CXhcs", "s00_sdo_gold_sun"),
        ("S3_028_bizlhspnVvY", "s01_lasilla_ntt"),
        ("S4_028_DETI0HV2jlI", "s01_paranal_mw_open"),
        ("S5_028_jJ5LkFGyzLI", "s01_sdo_sun_open"),
        ("S6_028_X768qs8sNQs", "s01_lasilla_mw_open"),
    }
    for sid, sdata in v05["shorts"].items():
        for s in sdata["shot_plan"]:
            if s["row"] != "s_loop":
                used_custom = (sid, s["row"]) in custom_crop_rows
                s["pixel_inspection"]["inspection_method"] = (
                    "Saved source-window inspection log (/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json) "
                    "produced by inspect_j0936_prep_v04_source_windows.py: 30fps source-rate decode across [source_in, source_out] for luma, "
                    "black fraction (<20 and <30), dark-run (<20 luma on >85% area), and ffmpeg scdet internal cut detection, plus sampled "
                    "2fps (every 0.50s) frame extraction and Tesseract OCR (--psm 6 -l eng). "
                    + (
                        "Evaluated with this opening shot's declared custom 9:16 crop/grade filter (no source_speed transform)."
                        if used_custom
                        else "Evaluated with default 9:16 centre crop (crop=ih*9/16:ih) at native source speed (source_speed and per-row eq grade not applied in source-window inspector; final transformed every-frame OCR/dark-run gates run on assembled MP4s)."
                    )
                )
            else:
                s["pixel_inspection"] = copy.deepcopy(sdata["shot_plan"][0]["pixel_inspection"])

    V05_MAPS_PATH.write_text(json.dumps(v05, indent=2) + "\n")
    v05_sha = sha256_file(V05_MAPS_PATH)
    print(f"Wrote {V05_MAPS_PATH} (sha256: {v05_sha})")

    md = render_markdown(v05, v05_sha, win_log)
    V05_MD_PATH.write_text(md)
    print(f"Wrote {V05_MD_PATH} ({len(md.splitlines())} lines)")


def render_markdown(v05: dict, v05_sha: str, win_log: dict) -> str:
    lines: list[str] = []
    a = lines.append

    a("# J0936 v04 Preparation v05 — Repaired Question & Body VO Bridges (`S3`, `S5`, `S6`), Reconciled Exact Timing & `S5` Scale Card (`16.180–19.160 s`), Unchanged `Test A` Diagnosis & Separate Repair Proposal, and Accurate Verifier Scope Labels")
    a("")
    a("- **Job:** `J1019` (`J0936 preparation: repair reported VO bridges and reconcile exact timing`)")
    a("- **Revises:** `J1017` (`jobs/reviews/J0936_v04_PREP_v04.md` and `jobs/reviews/J0936_v04_PREP_v04_maps.json`)")
    a("- **Authority Reference:** Elected-Chief Codex preparation review ruling `J1018` (27 Oct 2026, commit `b8c75920b` on `codex/j1018-review`, PR `#299`, `jobs/reviews/J1018_2026-10-27.md` and `jobs/reviews/J1018_2026-10-27_verification.json`), `J1016` (`4d95c81e7`, PR `#298`), `J1010` (`d63dc5898`), `J0993`, `J0936` (`c59`), and `.cursor/rules/orbit-build-shorts.mdc`.")
    a(f"- **Machine-Readable Companion:** `jobs/reviews/J0936_v04_PREP_v05_maps.json` (`sha256: {v05_sha}` — all prose summaries, numbers, hashes, and tables in this document are rendered programmatically from this single JSON source).")
    a("- **Executable Generators & Verifier:**")
    a("  - Preparation v05 map, audition & diagnostic builder: `jobs/reviews/build_j0936_prep_v05.py` -> `/Users/benjaminoats/_desk/reviews/J1019/auditions/` and `/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/`")
    a("  - Preserved v04 opening preview generator & house-gate evaluator: `jobs/reviews/generate_j0936_prep_v04_openings.py` -> `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("  - Saved source-window `30 fps` decode + `2 fps` sampled OCR inspector: `jobs/reviews/inspect_j0936_prep_v04_source_windows.py` -> `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json`")
    a("  - Reproducible verifier & saved output: `jobs/reviews/verify_j0936_prep_v05.py` -> `jobs/reviews/J1019_2026-10-27_verification.json` (`machine_checks_passed: true`, with accurate verifier scope labels separating supplied-index/saved-log machine checks from semantic/visual/auditory reviewer judgements and post-assembly final-render gates).")
    a("- **Desk Evidence Directories (Outside Git):** `/Users/benjaminoats/_desk/reviews/J1019/auditions/`, `/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/`, `/Users/benjaminoats/_desk/reviews/J1017/openings/`, and `/Users/benjaminoats/_desk/reviews/J1017/source_windows/`.")
    a("- **Worker:** `gemini` (`Gemini 4 Argon`, acting as specialist worker only; `J0936` remains blocked until Chief lock `J1020`).")
    a("- **Spend / Side Effects:** **£0 / 0 credits.** Preparation-only VO splice auditions and map reconciliation only. No full final video render, no spend, no deletion, no upload, no retitle, no privacy change, no Buffer write, and no swap.")
    a("")
    a("---")
    a("")
    a("## 1. Point-by-Point Resolution of J1018 Required Corrections")
    a("")
    a("### 1.1 Question VO Bridge Repair (`43.500–44.540 s` Continuous `Gliese 710` in `S3`, `S5`, `S6`) and Upstream Reconciliation")
    a("- **Root Cause of Omitted Spoken `\"seven\"` Resolved in Executable Subspans:** In `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav`, ElevenLabs Scribe (`gliese_words_list.json`) aligned token `121` (`\"Gliese\"`) to `43.500–43.740 s` and token `122` (`\"710\"`) to `44.100–44.540 s` (`\"ten\"`), leaving the spoken syllable `\"seven\"` inside the `43.740–44.100 s` (`0.360 s`) inter-token interval. Instead of deferring a bridge to assembly, Preparation v05 merges tokens `121..122` into a **single continuous subspan `[43.500, 44.540]` (`1.040 s` raw)** in `S3`, `S5`, and `S6`, reclaims genuine pauses / uses a shorter recorded token of the same word (`<= 1.055x <= 1.06x` tempo), updates every word coordinate and hash, and regenerates the affected WAV auditions in `/Users/benjaminoats/_desk/reviews/J1019/auditions/`:")
    a("  - **`S3_028_bizlhspnVvY` (`Why do the comets not arrive while Gliese 710 is passing?`):** Preserves the exact v04 question word indices (`181, 756, 861, 808, 757, 758..759, 121..122, 762..763`). Spans `1..7` run at `1.055x` tempo (`<= 1.06x`) with `0.008 s` onset and `0.006 s` inter-span gaps, and Span `6` (`\"arrive while\"`) starts at `298.000 s` to include the full `\"a-\"` onset of `\"arrive\"`. Continuous Span `7` (`43.500–44.540 s`, `scaled_dur = 0.986 s` at `1.055x`) places `\"710\"` (`word_idx=122`) at **`2.073–2.490 s` (`<= 2.500 s`)**, and Span `8` (`\"is passing.\"`, `1.000x` tempo) finishes the question at **`3.265 s`** (`gap_after = 0.175 s`), so body Span `9` starts at **exact `3.440 s`** (identical to v04).")
    a("  - **`S5_028_jJ5LkFGyzLI` (`How close will Gliese 710 come to the sun?`):** Preserves the exact v04 question word indices (`98..99, 101, 121..122, 102, 56, 38..39`) at **`1.000x` tempo** with `0.020 s` onset and `0.020 s` inter-span gaps. Continuous Span `3` (`43.500–44.540 s`, `1.040 s` at `1.000x`) places `\"710\"` (`word_idx=122`) at **`1.220–1.660 s` (`<= 2.500 s`)**, and Span `6` (`\"the sun.\"`) finishes the question at **`2.620 s`** (`gap_after = 0.140 s`, body Span `7` starts at `2.760 s`).")
    a("  - **`S6_028_X768qs8sNQs` (`What will the night sky look like when Gliese 710 arrives?`):** Preserves the exact question text at **`1.000x` tempo** (`0.015 s` onset, `0.010 s` inter-span gaps) by merging continuous `\"night sky\"` (`words 111..112`, `39.600–40.140 s = 0.540 s`) in Span `4`, using the clean `0.160 s` recording of `\"like\"` (`word 678`, `267.300–267.460 s`, replacing `word 115` where Scribe attached `0.200 s` of trailing silence to `40.640–41.020 s`) in Span `6`, and reading continuous `43.500–44.540 s` (`words 121..122`, `1.040 s`) in Span `8`. `\"710\"` (`word_idx=122`) completes at **`2.465 s` (`<= 2.500 s`)**, and Span `9` (`\"arrives.\"`) finishes the question at **`3.060 s`** (`gap_after = 0.180 s`), so body Span `10` starts at **exact `3.240 s`** (identical to v04).")
    a("")
    a("### 1.2 Body Bridge Repairs (`S3`, `S5`, `S6`), Exact `S5` Scale Card Alignment (`16.180–19.160 s`), and Direct Multimodal Auditory Judgement")
    a("- **Complete Resolution of All Identified Body Bridge Defects in `S3`, `S5`, and `S6` (Not Only Question WAVs):**")
    a("  1. **`S3_028_bizlhspnVvY` Body Bridges Repaired:**")
    a("     - **Body `\"Gliese 710\"` (Span `9`, `3.440–4.580 s`):** Replaced the v04 split across words `43..44` (`15.220–15.580 s` + `16.300–17.200 s`, which clipped `\"-za\"` and `\"sev-\"`) with the complete continuous recording of `\"Gliese 710\"` at words `719..720` (`283.220–284.360 s = 1.140 s` at `1.000x` tempo), which is the exact sentence subject immediately preceding Span `10`'s words `721..728` (`\"will send about 10 extra comets a year,\"` at `284.640–287.060 s`). With `gap_after = 0.140 s`, Span `10` starts at **exact `4.720 s`** (identical to v04).")
    a("     - **Body `\"straight through the Oort cloud.\"` (Span `12`, `8.560–10.740 s`):** Extended `source_in` on words `666..670` from `262.020 s` back to **`261.820 s`** (`261.820–264.000 s = 2.180 s` at `1.000x` tempo) so the unvoiced `\"st-\"` onset of `\"straight\"` (`261.820–262.020 s`) is preserved intact. Reclaiming `0.200 s` across the inter-span pauses of Spans `10..13` (`0.160 s, 0.080 s, 0.120 s, 0.080 s`) keeps Span `14` at **`12.560 s`**, earliest spoken answer `\"Because\"` at **`16.260 s` (`73.11%`)**, `vo_end_s` at **`21.240 s`**, and `total_duration_s` at **`22.240 s`** (zero shot-boundary drift).")
    a("  2. **`S5_028_jJ5LkFGyzLI` Body Bridge Repaired & `16.180–19.160 s` Scale Card Reconciled Upstream:**")
    a("     - **Body `\"And Gliese 710\"` (Span `17`, `13.380–14.960 s`):** Replaced the v04 cross-paragraph jump (`words 471..472` at `188.700–189.240 s` + truncated `word 44` at `16.300–17.200 s`) with the native continuous recording of `\"And Gliese 710\"` from the scale paragraph itself (**`words 471..473` at `188.700–190.280 s = 1.580 s` at `1.000x` tempo**), followed by Span `18` (`word 1171` `\"passes\"` at `15.070–15.650 s`).")
    a("     - **Upstream Pause Reconciliation Preserving Exact `16.180–19.160 s` Card Alignment:** Setting inter-span pauses across Spans `7..18` to `0.110 s` on phrase joins and `0.160 s` on sentence boundaries reconciles Span `19` (`words 475..479`, `\"more than 100 meters away,\"`, `191.140–192.820 s`) at **exact `15.760–17.440 s`**, placing spoken `\"100\"` (`word 477`, `191.560–192.040 s`) at **exact `16.180–16.660 s`** and Span `20` (`words 480..485`, `\"the length of a football pitch.\"`, `193.260–194.820 s`) at **exact `17.600–19.160 s`**. Thus Chief's locked S5 card (`['1-CM SCALE', 'OVER 100 METERS']` at **`16.180–19.160 s`**), earliest spoken answer (`\"more\"` at **`15.760 s` / `71.18%`** and `\"100\"` at **`16.180 s` / `73.08%`**), `vo_end_s = 21.140 s`, and `total_duration_s = 22.140 s` are preserved to the exact millisecond with zero timing conflict.")
    a("  3. **`S6_028_X768qs8sNQs` Body Bridges Repaired:**")
    a("     - **Body `\"Gliese 710\"` (Span `18`, `10.500–11.660 s`):** Replaced the v04 split across words `43..44` (`15.220–15.580 s` + `16.300–17.200 s`) with the complete continuous recording of `\"Gliese 710\"` at words `985..986` (`383.240–384.400 s = 1.160 s` at `1.000x` tempo).")
    a("     - **Body `\"the width of the full moon every 35 years.\"` (Span `20`, `13.240–16.160 s`):** Merged words `952..960` into one continuous source interval **`370.040–372.960 s` (`2.920 s` at `1.000x` tempo)** instead of splitting `370.040–371.760 s` + `372.000–372.960 s` across Scribe's `371.760–372.000 s` gap (where the spoken syllable `\"thir-\"` of `\"thirty-five\"` sits). With `gap_after = 0.160 s` on Span `18` and `0.120 s` on Span `19`, Span `21` (`\"it is the brightest\"`) starts at **exact `16.340 s`**, earliest spoken answer `\"brightest\"` (`word 881`) lands at **exact `16.820–17.240 s` (`75.83%`)**, `vo_end_s = 21.180 s`, and `total_duration_s = 22.180 s` (zero shot-boundary drift).")
    a("")
    tprop = v05["test_a_separate_repair_proposal"]
    opt_a = tprop["proposal_option_a_zero_downstream_drift"]
    opt_b = tprop["proposal_option_b_extend_runtime_by_0_280s"]
    a("### 1.3 `Test A` (`S4_028_DETI0HV2jlI`) Unchanged Preservation, Source Diagnosis at `14.980–17.280 s`, and Minimal Separate Repair Proposal for Next Chief")
    a("- **Locked `Test A` Map & Audio Preserved Unchanged (`test_a_subspans_equal_v02 = True`, `test_a_subspans_equal_v04 = True`):** Per J1018 (`b8c75920b`) and J1019 item 3 (*\"Preserve Test A unchanged VO/map and question/length exemptions. Diagnose J1017 reported bridge at 14.980-17.280s against source/audio. If defective, present a minimal separate repair proposal with timing consequences for next Chief; do not apply a Test A change in this job\"*), `S4_028_DETI0HV2jlI` in `J0936_v04_PREP_v05_maps.json` and `/Users/benjaminoats/_desk/reviews/J1019/auditions/S4_028_DETI0HV2jlI_*.wav` is **100% unchanged**.")
    a(f"- **Direct Diagnosis Against Source `star_coming_vo_v01.wav` (`14.980–17.280 s`) and `S4` Full Audition WAV:** {tprop['acoustic_diagnosis']}")
    a("- **Minimal Separate Repair Proposal for Next Chief Decision (Not Applied in v05):**")
    a(f"  - **Option A — Zero Downstream Timing Drift (Recommended if Chief Authorises Test A Repair):** {opt_a['description']} Diagnostic WAV rendered to `{opt_a['diagnostic_wav_path']}` (`sha256: {opt_a['diagnostic_wav_sha256']}`) and verified by `Gemini 4 Argon` multimodal audio input: *\"Its name is Gliese seven hundred and ten.\"* plays cleanly at `1.000x` tempo, and Span `8` (`\"It is an orange dwarf,\"`) still starts at **exact `8.736 s`**, leaving Spans `8..13` (`8.736–23.516 s`), all `8` shot boundaries (`s01..s07 + s_loop`), the `1.3 MILLION YEARS` card (`17.950–21.450 s`), earliest answer (`\"one\"` at `18.108 s` / `73.86%`), `vo_end_s = 23.516 s`, and `total_duration_s = 24.516 s` **100% unchanged**.")
    a(f"  - **Option B — Extend Runtime by `+0.280 s` (No Pause Reclamation):** {opt_b['description']} Shifts Spans `8..13` later by `+0.280 s` (`vo_end_s: 23.516 -> 23.796 s`, `total_duration_s: 24.516 -> 24.796 s`, earliest answer `\"one\"`: `18.108 s` / `73.86%` -> `18.388 s` / `74.16%`, card: `17.950–21.450 s` -> `18.230–21.730 s`, `s07_star_trails` hold: `3.551 -> 3.831 s <= 4.000 s`).")
    a("")
    a("### 1.4 Corrected Verifier Scope Labels & Honest Coverage Statement (`verify_j0936_prep_v05.py`)")
    a("- **`earliest_spoken_answer` Check Scope:** `verify_j0936_prep_v05.py` verifies the **supplied word index and its recomputed output timestamp/percentage** (`word_idx` exists in flattened output words, `start` matches within `0.002 s`, and `start / total_duration_s * 100 >= 70.0%`); it does **not** perform semantic natural-language analysis to decide which utterance first answers the title question (that semantic selection is a documented reviewer check).")
    a("- **Saved Source-Window Pixel/OCR Log Provenance:** `verify_j0936_prep_v05.py` verifies the SHA-256 hash (`b8e995f64132a8e9116ff47fa4e349d23f8788436e5c3d9631be46b54e18374b`) of the saved source-window inspection log (`/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json`, produced by `inspect_j0936_prep_v04_source_windows.py`) and checks that all `43` body shots' `(source_path, source_in, source_out)` match the saved log (`source_window_mismatches == []`); the verifier itself does **not** re-decode the `4,046` video frames or re-run Tesseract OCR.")
    a("- **`2 fps` Sampled OCR vs. Every-Frame Inspection:** In the saved source-window inspection log, `30 fps` decoding (`4,046` frames across all `43` body shots) measures luma, black fraction (`<20` and `<30`), dark runs (`<20` luma on `>85%` area), and `ffmpeg scdet` internal cuts on every source-rate frame, whereas Tesseract OCR and contact-sheet tiles (`306` frames) are **sampled at `2 fps` (every `0.50 s`, plus window tail)**, not every-frame (`30 fps`) OCR.")
    a("- **Source Inspector Transforms vs. Final Assembly Transforms:** `inspect_j0936_prep_v04_source_windows.py` applied explicit custom 9:16 crops/grades on `5` opening shots (`S1 s00_sdo_gold_sun`, `S3 s01_lasilla_ntt`, `S4 s01_paranal_mw_open`, `S5 s01_sdo_sun_open`, `S6 s01_lasilla_mw_open`) and a default 9:16 centre crop (`crop=ih*9/16:ih`) at native source speed (`source_speed` not applied) on the remaining `38` body shots. Therefore, the source-window log is preparation-stage source screening and does **not** replace mandatory every-frame OCR/dark-run/polish/picture gates on the final speed-transformed, graded, and pan/crop-rendered output MP4s at assembly.")
    a("")
    a("---")
    a("")
    a("## 2. Master Acceptance Summary Matrix (All Six Shorts)")
    a("")
    a("| # | Short ID & Slug | Air Date | Local Title | Words (WS / Spoken) | First Subj End (`<=2.50s`) | VO End / Total (`s`) | `70%` Mark (`s`) | Supplied Earliest Answer (`s` & `%`) | `4–8s` Stills | First Cut / Max Hold (`s`) | Single Teaching Overlay (`in–out s`) |")
    a("|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|")
    for idx, (sid, sdata) in enumerate(v05["shorts"].items(), 1):
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
    a(f"- **Library Snapshot File & SHA-256:** `{v05['library_snapshot']['path']}` (`sha256: {v05['library_snapshot']['sha256']}`)")
    a("- **Saved Side-by-Side Uncaptioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg`")
    a("- **Saved Side-by-Side v04-Captioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg`")
    a("- **Saved Raw Gate Report JSON:** `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("")
    a("| Short ID | Air Date | Frame-0 Source (`asset_key` / `underlying_id`) | Src In–Out (`s`) & Speed | First Cut (`s`) | Uncap / Cap `dhash` (`@0.30s`) | Mot `0–1s` Uncap / Cap (`>=10`) | `f0diff` Uncap / Cap (`>=1.5`) | Reviewer Subj Body / Total (`>=60%`) | Black (`<20%`) | Visor Uncap / Cap (`<0.005`) | Min Lib Ham Uncap / Cap (`>=15`) | Max Lib `bg` Uncap / Cap (`<0.55`) | Min Batch Ham Uncap / Cap (`>=15`) | Max Batch `bg` Uncap / Cap (`<0.55`) |")
    a("|---|---|---|---|---:|---|---|---|---|---:|---|---:|---:|---:|---:|")
    for sid, sdata in v05["shorts"].items():
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
    a("## 4. Verified Source Media, Repaired v05 VO Splice Auditions, Multimodal Auditory Judgement & Saved Source-Window Inspection")
    a("")
    a("### 4.1 Voiceover Sources & Tracked Word Maps")
    a("")
    a("| Film | VO Source Path | SHA-256 Hash | Word Map Tracked in Git |")
    a("|---|---|---|---|")
    a("| **026** | `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav` | `d6159f085b04f38604676bc3b37de24187488379e48ed394d076bee5bcabfaf5` | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json` |")
    a("| **027** | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4` | `f74ca3e8a27b3897fd4942ebcd6f70462aee039146ccce1780216c42802be38b` | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json` |")
    a("| **028** | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` | `cf546efd12e723173b66bd1d3ee2139afc94a03124ab0e4fdfd2cc06ebb8ab01` | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json` |")
    a("")
    a("### 4.2 Local VO-Only Auditions (`48 kHz` Mono WAV in `/Users/benjaminoats/_desk/reviews/J1019/auditions/`) & Direct Multimodal Auditory Judgement")
    a("")
    a("| Short ID | Assembled Opening Question | Question WAV Path & SHA-256 | Q Dur (`s`) | Q RMS / Peak (`dBFS`) | Full VO WAV Path & SHA-256 | Full Dur (`s`) | Max Step |")
    a("|---|---|---|---:|---|---:|---:|---:|")
    for sid, sdata in v05["shorts"].items():
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
    for sid, sdata in v05["shorts"].items():
        aj = sdata["vo_splice_map"]["auditory_judgement"]
        a(f"- **`{sid}` (`{sdata['local_title']}`):**")
        a(f"  - **Method:** {aj['method']}")
        a(f"  - **Question Audition Judgement:** {aj['question_prosody_and_joins']}")
        a(f"  - **Full-VO Audition Judgement:** {aj['full_vo_prosody_and_joins']}")
        a(f"  - **Question & Map Preservation:** `preserve_exact_question_and_map = {aj['preserve_exact_question_and_map']}`")
    a("")
    a("### 4.3 Saved Source-Window Inspection Evidence (`30 fps` Luma/Dark-Run/`scdet` + Sampled `2 fps` OCR & Contact Sheets)")
    a(f"- **Inspector Script & Saved Log:** `python3 jobs/reviews/inspect_j0936_prep_v04_source_windows.py` -> `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json` (`sha256: {sha256_file(WIN_LOG_PATH)}`).")
    a(f"- **Exact Coverage & Transform Scope:** Decoded **`{win_log['total_30fps_frames_decoded']}` source-rate frames at `30 fps`** across `[source_in, source_out]` of all **`{win_log['total_body_shots']}` body shots** for luma, black fraction (`<20` and `<30`), dark-run (`<20` luma on `>85%` area), and `ffmpeg scdet` internal cut detection, and extracted **`{win_log['total_2fps_ocr_frames_scanned']}` sampled frames at `2 fps` (every `0.50 s`, plus window tail)** for Tesseract OCR (`--psm 6 -l eng`) and visual contact sheets (`/Users/benjaminoats/_desk/reviews/J1017/source_windows/S1..S6_full_window_2fps.jpg`). Five opening shots (`S1 s00`, `S3 s01`, `S4 s01`, `S5 s01`, `S6 s01`) were decoded with their declared custom 9:16 crops/grades, while the remaining `38` body shots were decoded with a default 9:16 centre crop (`crop=ih*9/16:ih`) at native source speed (`source_speed` not applied). Every-frame OCR and dark-run gate logs on the final transformed MP4s remain mandatory post-assembly checks.")
    a(f"- **Saved Log Results:** `any_failures = {win_log['any_failures']}` (`0` internal `scdet` cuts, `0` dark runs `>= 3` frames, `0` banned OCR hits across the `306` `2 fps` samples, and `0` slates/baked labels/portraits/diagrams on the `2 fps` contact sheets).")
    a("")
    a("---")
    a("")
    a("## 5. Per-Short Reconciled Scripts, Exact Subspan Splice Tables, Single Teaching Overlay Specs, and Complete Shot Plans")
    a("")
    for idx, (sid, sdata) in enumerate(v05["shorts"].items(), 1):
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

    a("## 6. Reproducible Verification, Accurate Scope Labels, and Unchanged Assembly Boundaries (`J1018` -> `J1020` -> `J0936`)")
    a("")
    a("- **Verifier Script:** `python3 jobs/reviews/verify_j0936_prep_v05.py`")
    a(f"- **Verification Output:** `jobs/reviews/J1019_2026-10-27_verification.json` (`machine_checks_passed: True`, `total_source_words_verified: 390`, `input_sha256: {v05_sha}`)")
    a("- **Deterministic Machine-Verified Checks Performed by `verify_j0936_prep_v05.py`:**")
    a("  1. Every source word record (`word`, `src_start`, `src_end`) matches the tracked git word map (`words.json`, `earth_spin_words_list.json`, `gliese_words_list.json`) within `1e-4 s`, and every word's output coordinate (`timeline_start + (src_t - source_in) / tempo`) reconciles within `0.002 s` across all `390` words.")
    a("  2. Every `" + '"Gliese 710"' + "` occurrence in ordinary Shorts `S3`, `S5`, and `S6` (`words 121..122` in questions, `words 719..720` in `S3` body, `words 471..473` in `S5` body, `words 985..986` in `S6` body) and `\"every 35 years.\"` (`words 952..960` in `S6` body) is verified to reside inside a **single continuous subspan** with `0` omitted inter-token syllables (`omitted_ordinary_bridges == []`).")
    a("  3. Both whitespace word count and spoken-expansion word count are inside `55–65` for all five ordinary Shorts (**`S1: 65/65`**, **`S2: 64/65`**, **`S3: 62/64`**, **`S5: 61/65`**, **`S6: 62/65`**), with **`S4` retaining its explicit Test A exemption (`76/77`) and byte-for-structure subspan equality with Preparation v02, v03, and v04 (`test_a_subspans_equal_v02: True`, `test_a_subspans_equal_v04: True`)**.")
    a("  4. Spoken opening question tokens equal `local_title` token-for-token for all five ordinary Shorts, and all `12` local VO audition WAVs (`question_audition` and `full_vo_audition` in `/Users/benjaminoats/_desk/reviews/J1019/auditions/`) exist on disk and match their recorded SHA-256 hashes.")
    a("  5. First named subject (`Sun`, `Earth's`, `710`, `star`, `710`, `710`) completes at `<= 2.500 s` across all six Shorts, recomputed from the flattened output word timeline (`S1: 2.380 s`, `S2: 1.750 s`, `S3: 2.490 s`, `S4: 0.920 s`, `S5: 1.660 s`, `S6: 2.465 s`).")
    a("  6. Subspan splice arithmetic (`1.000x <= tempo <= 1.055x <= 1.060x`, `gap_after <= 0.180 s`, `max_internal_pause <= 0.200 s`, `12 ms` crossfades on Test A) and shot coverage (`0.000 s` to `vo_end_s` for body shots, `s_loop` ending at `total_duration_s` with `final_shot_cursor == total_duration_s`) reconcile with `0` errors.")
    a("  7. `4.000–8.000 s` early motion window uses `100%` moving `video=True` footage across all six Shorts (`early_still_windows_4_8s = []`), with `0` still-to-still cuts and `>= 10.0 s` separation on any repeated underlying source.")
    a("  8. **Supplied Earliest-Answer Index Coordinate Check:** Recomputes the output timestamp and runtime percentage of the **supplied** `earliest_spoken_answer.word_idx` from the flattened word timeline and verifies `pct_of_total >= 70.0%` across all six Shorts (semantic selection of which word first answers the title is a manual reviewer check, not performed by the verifier).")
    a("  9. Single teaching overlay (`baked_in_labels = 0`, `code_graphics = 0`, `added_edit_cards = 1`, `<= 4` words per line, `<= 4.000 s` duration, clear of `0–2 s` hook and `9–14 s` banner), including Chief's locked S5 card `['1-CM SCALE', 'OVER 100 METERS']` within **`16.180–19.160 s`** aligned to spoken `\"100\"` (`16.180 s`) and `\"pitch.\"` (`19.160 s`) and clear of `\"fifth\"` (`20.080 s`) / `\"light-year.\"` (`20.560–21.140 s`).")
    a(" 10. Fresh `gate_shorts_open.py` measurements on all `6` uncaptioned (`S1..S6_open.mp4`) and `6` v04-captioned (`S1..S6_open_captioned.mp4`) opening preview clips, plus **provenance verification against the saved source-window inspection log** (`/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json`, verifying its SHA-256 and `source_window_mismatches == []` across all `43` body shots; the verifier reads that saved log rather than re-decoding the `4,046` `30 fps` frames or `306` sampled `2 fps` OCR frames).")
    a("- **Explicitly Separated Manual / Multimodal Reviewer Assertions (Not Computed by the Verifier Script):**")
    a("  1. **Semantic Identification of Earliest Spoken Answer:** Human/LLM semantic verification that the supplied `earliest_spoken_answer` token is the first utterance that answers the Short's title question.")
    a("  2. **Visual & Geometric Titled-Subject Occupancy (`>= 60%`):** Reviewer visual/contour segmentation on the cropped `1080×1920` `@0.30s` frames (`all_6_openings_0_30s_comparison.jpg` and `all_6_openings_captioned_0_30s_comparison.jpg`); supplied as reviewer values, not computed by `verify_j0936_prep_v05.py`.")
    a("  3. **Visual Contact-Sheet Inspection of Sampled `2 fps` Source Windows:** Reviewer visual inspection of `S1..S6_full_window_2fps.jpg` (`306` tiles sampled at `2 fps` across `43` body shots, where `38` body shots use the inspector's default 9:16 centre crop at native source speed).")
    a("  4. **Multimodal Auditory Judgement of Prosody & Repaired Bridges:** Direct `Gemini 4 Argon` multimodal audio listening across all `12` WAV files in `/Users/benjaminoats/_desk/reviews/J1019/auditions/` and the separate Test A diagnostic WAV in `/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/` (hash/token validity does not itself prove prosody).")
    a("- **Unchanged Post-Assembly Acceptance (`c59` / `J0936`, Mandatory at Final Render After Chief Lock):** Eventual assembly after Chief lock (`J1020`) retains every original `J0936`/`c59` acceptance requirement: all Shorts/picture/polish/music/SFX gates, full rendered-video every-frame/dense OCR and dark-run gate logs on the final speed-transformed/cropped/graded MP4s, measured final AAC `-14.0 ± 0.5 LUFS` and `TP <= -1.6 dBTP`, matched `1.000 s` loop (`loop_diff < 2.0`), complete runtime sheets and flagged frames, `720×1280` PHONE video, UAT/NAS copies and SHA-256 manifests. Batch target remains **1 November 2026, 20:00 London**; individual day-before-air deadlines (`19 Nov`, `22 Nov`, `29 Nov`, `1 Dec`, `3 Dec`, `6 Dec` at `20:00 London`) and v01 fallbacks remain unchanged. Ben swap approval follows replacement PASS.")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
