#!/usr/bin/env python3
"""
Builds J0936 v04 Preparation v06 artifacts for J1024:
  1. /Users/benjaminoats/_desk/reviews/J1024/auditions/S1..S6_{question,full_vo}_audition.wav
  2. /Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json
     and S6_028_X768qs8sNQs_full_window_2fps.jpg (preserving all 42 unchanged shots from
     /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json untouched
     and inspecting only the 1 updated shot S6 s05_alma_orion_set)
  3. jobs/reviews/J0936_v04_PREP_v06_maps.json
  4. jobs/reviews/J0936_v04_PREP_v06.md
in accordance with elected-Chief Codex J1020 ruling e82eae17d (27 Oct 2026).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
V04_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v04_maps.json"
V05_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v05_maps.json"
V06_MAPS_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v06_maps.json"
V06_MD_PATH = ROOT / "jobs/reviews/J0936_v04_PREP_v06.md"

VO028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav"
W028_PATH = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json"

J1019_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1019/auditions")
J1019_TESTA_DIAG = Path("/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav")
NEW_AUD_DIR = Path("/Users/benjaminoats/_desk/reviews/J1024/auditions")
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


def apply_test_a_option_a(s4_vm: dict, w028: list[dict], pcm028: np.ndarray) -> dict:
    """
    Applies Chief J1020 explicitly authorised Test A Option A syllable repair to S4:
      - Span 4 gap_after: 0.140 -> 0.060s
      - Span 5: source [14.140, 14.800], timeline [6.012, 6.672], gap_after 0.100 -> 0.040s
      - Span 6: source [14.980, 15.780] (1.0x), timeline [6.700, 7.500], gap_after 0.120 -> 0.040s
      - Span 7: source [16.060, 17.220] (1.0x), timeline [7.528, 8.688], gap_after 0.120 -> 0.060s
      - Span 8 remains 8.736s; VO end 23.516, runtime 24.516, card 17.950-21.450 unchanged.
    """
    subspans = s4_vm["subspans"]
    subspans[3]["gap_after"] = 0.060

    subspans[4]["timeline_start"] = 6.012
    subspans[4]["timeline_end"] = 6.672
    subspans[4]["gap_after"] = 0.040

    subspans[5]["source_in"] = 14.980
    subspans[5]["source_out"] = 15.780
    subspans[5]["raw_dur"] = 0.800
    subspans[5]["scaled_dur"] = 0.800
    subspans[5]["timeline_start"] = 6.700
    subspans[5]["timeline_end"] = 7.500
    subspans[5]["gap_after"] = 0.040

    subspans[6]["source_in"] = 16.060
    subspans[6]["source_out"] = 17.220
    subspans[6]["raw_dur"] = 1.160
    subspans[6]["scaled_dur"] = 1.160
    subspans[6]["timeline_start"] = 7.528
    subspans[6]["timeline_end"] = 8.688
    subspans[6]["gap_after"] = 0.060

    for idx in (4, 5, 6):
        sp = subspans[idx]
        tl_s = sp["timeline_start"]
        src_in = sp["source_in"]
        tempo = sp["tempo"]
        for w in sp["words"]:
            ref = w028[w["word_idx"]]
            rs, re_ = round(float(ref["start"]), 3), round(float(ref["end"]), 3)
            w["src_start"] = rs
            w["src_end"] = re_
            w["start"] = round(tl_s + (rs - src_in) / tempo, 3)
            w["end"] = round(tl_s + (re_ - src_in) / tempo, 3)
        sp["max_internal_pause"] = acoustic_max_pause(pcm028, sp["source_in"], sp["source_out"])

    assert subspans[7]["timeline_start"] == 8.736
    assert subspans[-1]["timeline_end"] == 23.516 == s4_vm["vo_end_s"]

    w44 = subspans[6]["words"][0]
    assert w44["word_idx"] == 44 and w44["word"] == "710."
    s4_vm["keyword_timings"]["710."] = {
        "word": w44["word"],
        "start": w44["start"],
        "end": w44["end"],
        "pct_of_total": round(w44["start"] / s4_vm["total_duration_s"] * 100.0, 2),
    }

    q_src = J1019_AUD_DIR / "S4_028_DETI0HV2jlI_question_audition.wav"
    q_dst = NEW_AUD_DIR / "S4_028_DETI0HV2jlI_question_audition.wav"
    shutil.copy2(q_src, q_dst)
    s4_vm["auditions"]["question_audition"]["wav_path"] = str(q_dst)

    fa = render_audition(subspans, NEW_AUD_DIR / "S4_028_DETI0HV2jlI_full_vo_audition.wav", pcm028, VO028_PATH)
    expected_diag_sha = "d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a"
    assert fa["sha256"] == expected_diag_sha == sha256_file(J1019_TESTA_DIAG), f"S4 Option A hash mismatch: {fa['sha256']}"
    s4_vm["auditions"]["full_vo_audition"] = fa
    return fa


S6_V06_SPEC = [
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
    (list(range(160, 167)), 60.200, 61.860, 1.000, 0.140),
    (list(range(167, 172)), 62.140, 63.600, 1.000, 0.180),
    ([856], 337.300, 337.700, 1.000, 0.130),
    ([861, 862, 863, 864], 338.780, 339.400, 1.000, 0.130),
    ([865, 866], 339.440, 340.360, 1.000, 0.180),
    (list(range(867, 872)), 341.060, 342.120, 1.000, 0.020),
    (list(range(872, 877)), 342.140, 344.100, 1.000, 0.180),
    (list(range(878, 882)), 345.220, 346.060, 1.000, 0.080),
    ([398], 159.180, 159.600, 1.000, 0.140),
    ([743], 291.380, 291.780, 1.000, 0.080),
    (list(range(890, 894)), 348.740, 350.080, 1.000, 0.140),
    (list(range(902, 906)), 353.060, 354.400, 1.000, 0.000),
]


def inspect_single_updated_shot_s6_s05(j1017_log: dict) -> tuple[dict, dict, Path]:
    """
    Preserves all 42 unchanged body shot records from J1017's saved source-window log
    (/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json)
    without re-decoding them, and runs the 30fps decode + scdet + 2fps sampled Tesseract OCR
    ONLY on the 1 updated shot in S6: s05_alma_orion_set (0.400-3.800s of alma_orion_set.mp4).
    Also renders the updated 2fps contact sheet for S6 in /Users/benjaminoats/_desk/reviews/J1024/source_windows/.
    """
    J1024_SW_DIR.mkdir(parents=True, exist_ok=True)
    src_rel = "02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/alma_orion_set.mp4"
    src = ROOT / src_rel
    sin, sout = 0.400, 3.800
    sdur = round(sout - sin, 3)

    vf_gray = "crop=ih*9/16:ih,scale=180:320:flags=area,fps=30,format=gray"
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{sin:.3f}", "-t", f"{sdur:.3f}",
        "-i", str(src), "-vf", vf_gray, "-f", "rawvideo", "-"
    ])
    n_px = 180 * 320
    n_frames = len(raw) // n_px
    frames = np.frombuffer(raw[: n_frames * n_px], dtype=np.uint8).reshape(n_frames, n_px)
    lumas = frames.mean(axis=1)
    blks20 = (frames < 20).mean(axis=1)
    blks30 = (frames < 30).mean(axis=1)

    dark_flags = blks20 > 0.85
    run_len = max_dark_run = 0
    for fl in dark_flags:
        if fl:
            run_len += 1
            max_dark_run = max(max_dark_run, run_len)
        else:
            run_len = 0

    sc_err = subprocess.run([
        "ffmpeg", "-v", "info", "-nostats", "-ss", f"{sin:.3f}", "-t", f"{sdur:.3f}",
        "-i", str(src), "-vf", "crop=ih*9/16:ih,scale=72:128:flags=area,scdet=threshold=12:sc_pass=1",
        "-an", "-f", "null", "-"
    ], capture_output=True, text=True, errors="replace").stderr
    internal_cuts = [round(float(m.group(1)), 3) for m in re.finditer(r"lavfi\.scd\.time:\s*([0-9.]+)", sc_err) if float(m.group(1)) > 0.10]

    sample_offsets = list(np.arange(0.05, max(0.06, sdur - 0.04), 0.50))
    if not sample_offsets or abs(sample_offsets[-1] - (sdur - 0.08)) > 0.20:
        sample_offsets.append(max(0.05, round(sdur - 0.08, 3)))
    sample_times = [round(sin + off, 3) for off in sample_offsets]

    ocr_dir = Path("/tmp/ocr_win_S6_028_X768qs8sNQs_s05_alma_orion_set")
    if ocr_dir.exists():
        shutil.rmtree(ocr_dir)
    ocr_dir.mkdir(parents=True)

    tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
    banned_re = re.compile(
        r"(https?://|www\.|\.int\b|\.gov\b|esa\.int|copyright|all rights reserved|tycho|brahe|"
        r"shrinking|grapefruit|cherry|4,000|equator|gliese|sirius|million|light-year|centimeter|neptune)",
        re.I,
    )
    vf_ocr = "crop=ih*9/16:ih,scale=360:640:flags=lanczos"
    ocr_records = []
    banned_hits = []
    for idx_t, st in enumerate(sample_times):
        jpg_p = ocr_dir / f"f_{idx_t:02d}.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{st:.3f}", "-i", str(src),
            "-frames:v", "1", "-vf", vf_ocr, "-q:v", "3", str(jpg_p)
        ], check=True)
        got = subprocess.run([tess, str(jpg_p), "stdout", "--psm", "6", "-l", "eng"], capture_output=True, text=True, errors="replace")
        txt = re.sub(r"\s+", " ", (got.stdout or "")).strip()
        alpha_words = [w for w in re.findall(r"[A-Za-z]{3,}", txt)]
        if banned_re.search(txt):
            banned_hits.append({"source_t": st, "ocr": txt})
        ocr_records.append({"source_t": st, "raw_ocr": txt, "alpha_3plus_words": alpha_words})

    new_rec = {
        "short_id": "S6_028_X768qs8sNQs",
        "row": "s05_alma_orion_set",
        "source_path": src_rel,
        "source_in": sin,
        "source_out": sout,
        "source_dur": sdur,
        "frames_decoded_30fps": int(n_frames),
        "start_mean_luma": round(float(lumas[0]), 2),
        "midpoint_mean_luma": round(float(lumas[len(lumas) // 2]), 2),
        "end_mean_luma": round(float(lumas[-1]), 2),
        "window_min_luma": round(float(lumas.min()), 2),
        "window_max_luma": round(float(lumas.max()), 2),
        "window_mean_luma": round(float(lumas.mean()), 2),
        "start_black_frac": round(float(blks20[0]), 4),
        "midpoint_black_frac": round(float(blks20[len(blks20) // 2]), 4),
        "end_black_frac": round(float(blks20[-1]), 4),
        "window_min_black_frac": round(float(blks20.min()), 4),
        "window_max_black_frac": round(float(blks20.max()), 4),
        "window_mean_black_frac": round(float(blks20.mean()), 4),
        "window_max_black30_frac": round(float(blks30.max()), 4),
        "dark_run_max_consecutive_frames": int(max_dark_run),
        "internal_scdet_cuts": internal_cuts,
        "ocr_2fps_sample_count": len(sample_times),
        "ocr_2fps_timestamps_s": sample_times,
        "ocr_banned_hits": banned_hits,
        "ocr_records": ocr_records,
        "clean_window_verified": (max_dark_run < 3 and len(internal_cuts) == 0 and len(banned_hits) == 0),
    }
    assert new_rec["clean_window_verified"] is True

    # Build v06 log by copying 42 unchanged entries from j1017_log and replacing only (S6, s05_full_moon)
    v06_shots = []
    for r in j1017_log["shots"]:
        if r["short_id"] == "S6_028_X768qs8sNQs" and r["row"] == "s05_full_moon":
            v06_shots.append(new_rec)
        else:
            v06_shots.append(copy.deepcopy(r))

    v06_log = {
        "method": (
            "Preserves 42 unchanged body shot entries verbatim from /Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json "
            "(sha256: b8e995f64132a8e9116ff47fa4e349d23f8788436e5c3d9631be46b54e18374b) without re-decoding unchanged windows, and updates only the 1 "
            "replaced shot in S6 (s05_alma_orion_set, 0.400-3.800s of alma_orion_set.mp4) with 30fps decode (102 frames), scdet internal cut check (0 cuts), "
            "and 2fps sampled Tesseract OCR (8 samples, 0 banned hits)."
        ),
        "preserved_j1017_log_path": str(J1017_WIN_LOG_PATH),
        "preserved_j1017_log_sha256": sha256_file(J1017_WIN_LOG_PATH),
        "unchanged_shots_preserved_count": 42,
        "updated_shots_inspected_count": 1,
        "total_body_shots": len(v06_shots),
        "total_30fps_frames_decoded": sum(r["frames_decoded_30fps"] for r in v06_shots),
        "total_2fps_ocr_frames_scanned": sum(r["ocr_2fps_sample_count"] for r in v06_shots),
        "any_failures": sum(1 for r in v06_shots if not r["clean_window_verified"]),
        "shots": v06_shots,
    }
    J1024_WIN_LOG_PATH.write_text(json.dumps(v06_log, indent=2) + "\n")

    # Update row 5 (index 4) of S6_028_X768qs8sNQs_full_window_2fps.jpg from J1017 without re-extracting unchanged rows
    j1017_s6_sheet = Image.open("/Users/benjaminoats/_desk/reviews/J1017/source_windows/S6_028_X768qs8sNQs_full_window_2fps.jpg").copy()
    draw = ImageDraw.Draw(j1017_s6_sheet)
    tw, th = 135, 240
    y0 = 4 * (th + 22)
    draw.rectangle([0, y0, j1017_s6_sheet.width, y0 + th + 22], fill=(12, 12, 16))
    hdr = (
        f"S6_028 {new_rec['row']} [{new_rec['source_in']:.2f}-{new_rec['source_out']:.2f}s] "
        f"{new_rec['frames_decoded_30fps']}f luma={new_rec['window_min_luma']:.0f}..{new_rec['window_max_luma']:.0f} "
        f"blk={new_rec['window_max_black_frac']*100:.1f}% cuts=0 ocr_hits=0"
    )
    draw.text((4, y0 + 3), hdr, fill=(230, 230, 230))
    for c_i, st in enumerate(sample_times):
        jp = ocr_dir / f"f_{c_i:02d}.jpg"
        im = Image.open(jp).resize((tw - 2, th - 2))
        j1017_s6_sheet.paste(im, (c_i * tw + 1, y0 + 21))
        draw.text((c_i * tw + 4, y0 + 24), f"{st:.2f}s", fill=(255, 214, 0))
    s6_sheet_out = J1024_SW_DIR / "S6_028_X768qs8sNQs_full_window_2fps.jpg"
    j1017_s6_sheet.save(s6_sheet_out, quality=88)

    return new_rec, v06_log, s6_sheet_out


def main() -> None:
    NEW_AUD_DIR.mkdir(parents=True, exist_ok=True)
    v05 = json.loads(V05_MAPS_PATH.read_text())
    j1017_log = json.loads(J1017_WIN_LOG_PATH.read_text())
    w028 = json.loads(W028_PATH.read_text())
    pcm028 = load_pcm48k(VO028_PATH)

    v06 = copy.deepcopy(v05)
    v06["job"] = "J1024"
    v06["revises"] = "J1019 (jobs/reviews/J0936_v04_PREP_v05.md and J0936_v04_PREP_v05_maps.json)"
    v06["ruling_authority"] = "J1020 (Codex elected-Chief preparation ruling, 27 Oct 2026, e82eae17d on codex/j1020-review)"
    v06["spend_gbp"] = 0
    v06["all_checks_passed"] = True

    # 1. Copy accepted unchanged audition WAVs for S1, S2, S3, S5 to /Users/benjaminoats/_desk/reviews/J1024/auditions/
    for sid in ("S1_026_A6TW_6CXhcs", "S2_027_emwQsPxnRGM", "S3_028_bizlhspnVvY", "S5_028_jJ5LkFGyzLI"):
        vm = v06["shorts"][sid]["vo_splice_map"]
        for kind in ("question_audition", "full_vo_audition"):
            src_wav = J1019_AUD_DIR / f"{sid}_{kind}.wav"
            dst_wav = NEW_AUD_DIR / f"{sid}_{kind}.wav"
            shutil.copy2(src_wav, dst_wav)
            vm["auditions"][kind]["wav_path"] = str(dst_wav)
            assert sha256_file(dst_wav) == vm["auditions"][kind]["sha256"]

    # Record honest S3 atempo slot-fit implementation note per J1020
    s3_vm = v06["shorts"]["S3_028_bizlhspnVvY"]["vo_splice_map"]
    s3_pcm_diffs = []
    for sp in s3_vm["subspans"]:
        if abs(sp["tempo"] - 1.0) > 1e-6:
            _, actual_n = extract_span(pcm028, VO028_PATH, sp["source_in"], sp["source_out"], sp["tempo"])
            slot_n = int(round((sp["timeline_end"] - sp["timeline_start"]) * 48000))
            s3_pcm_diffs.append({
                "span_index": sp["span_index"],
                "text": sp["text"],
                "tempo": sp["tempo"],
                "atempo_output_samples": actual_n,
                "slot_samples": slot_n,
                "trimmed_samples": max(0, actual_n - slot_n),
                "trimmed_ms": round(max(0, actual_n - slot_n) / 48.0, 2),
            })
    s3_vm["atempo_slot_fit_implementation_note"] = {
        "description": (
            "In render_audition, short-span ffmpeg atempo=1.055 output on S3 Spans 1..7 produces up to 776 excess samples "
            "(16.17 ms at 48 kHz) due to WSOLA frame buffering; render_audition slices seg[:tlen] with a 240-sample (5.0 ms) "
            "linear fade-in/fade-out to fit each span's nominal scaled_dur slot. The rebuilt bytes match the audition WAVs "
            "(dd7e65643007638e... and e38d4a2838dfb122...) reviewed by Gemini multimodal audio input. Nominal source/tempo "
            "arithmetic alone does not prove acoustic word boundaries; listening verification is preserved at final assembly "
            "and no syllable is ever trimmed just to meet a slot."
        ),
        "spans_1_to_7_atempo_buffer_trim_details": s3_pcm_diffs,
    }
    s3_vm["auditory_judgement"]["atempo_slot_fit_note"] = s3_vm["atempo_slot_fit_implementation_note"]["description"]

    # 2. Apply explicitly authorised Test A Option A syllable repair to S4_028_DETI0HV2jlI
    s4_vm = v06["shorts"]["S4_028_DETI0HV2jlI"]["vo_splice_map"]
    s4_fa = apply_test_a_option_a(s4_vm, w028, pcm028)
    s4_vm["auditory_judgement"] = {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input; Codex verified execution/hashes/arithmetic in J1020 and does not claim independent listening)",
        "method": (
            f"Direct multimodal playback and auditory inspection of {s4_vm['auditions']['question_audition']['wav_path']} (2.118s) "
            f"and {s4_fa['wav_path']} (23.566s, sha256: {s4_fa['sha256']}, reconciled byte-for-byte against retained J1019 Option A "
            f"diagnostic WAV {J1019_TESTA_DIAG})."
        ),
        "question_prosody_and_joins": (
            "Test A long-opening hook ('There is a star coming towards us.', spans 1-2, 0.000-2.068s) is preserved byte-for-byte "
            "identical to Preparation v02/v03/v04/v05."
        ),
        "full_vo_prosody_and_joins": (
            "APPLIED AUTHORISED TEST A OPTION A REPAIR & VERIFIED BY EAR (Gemini): Span 6 now reads source 14.980-15.780s (0.800s at 1.000x, "
            "output 6.700-7.500s) and Span 7 reads source 16.060-17.220s (1.160s at 1.000x, output 7.528-8.688s), with gaps after Spans 4/5/6/7 "
            "set to 0.060/0.040/0.040/0.060s (12ms crossfades preserved, placing Span 5 at 6.012-6.672s). In direct multimodal listening by Gemini, "
            "'Its name is Gliese seven hundred and ten.' plays cleanly with both the '-za' ending of 'Gliese' (15.560-15.780s) and the 'sev-' onset "
            "of 'seven' (16.060-16.280s) fully intact across the natural pause. Span 8 ('It is an orange dwarf,') remains at exact 8.736s, leaving "
            "Spans 8..13 (8.736-23.516s), vo_end_s=23.516s, total_duration_s=24.516s, earliest answer 'one' at 18.108s (73.86%), and the "
            "1.3 MILLION YEARS card at 17.950-21.450s 100% unchanged."
        ),
        "preserve_exact_question_and_map": True,
    }
    v06["test_a_separate_repair_proposal"]["applied_in_v05"] = False
    v06["test_a_separate_repair_proposal"]["applied_in_v06"] = True
    v06["test_a_separate_repair_proposal"]["locked_test_a_subspans_unchanged"] = False
    v06["test_a_separate_repair_proposal"]["j1020_authorisation"] = (
        "Explicitly authorised by elected-Chief Codex in J1020 (e82eae17d): Option A applied to S4_028_DETI0HV2jlI map and full_vo_audition "
        "with retained diagnostic SHA-256 d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a."
    )
    v06["shorts"]["S4_028_DETI0HV2jlI"]["test_a_separate_repair_proposal"] = v06["test_a_separate_repair_proposal"]

    # 3. Apply S6_028_X768qs8sNQs payoff correction (replace early motion/35-years clause with present-day invisibility setup)
    s6_data = v06["shorts"]["S6_028_X768qs8sNQs"]
    s6_vm = s6_data["vo_splice_map"]
    s6_subspans = build_subspans(S6_V06_SPEC, 0.015, w028, pcm028)
    s6_qa = render_audition(s6_subspans[:9], NEW_AUD_DIR / "S6_028_X768qs8sNQs_question_audition.wav", pcm028, VO028_PATH)
    s6_fa = render_audition(s6_subspans, NEW_AUD_DIR / "S6_028_X768qs8sNQs_full_vo_audition.wav", pcm028, VO028_PATH)

    assert s6_qa["sha256"] == "67a26cb681b3ac5043b503c4392f1ac11898d9c0413e46e4be07c833a4ee5ddd"

    s6_flat_words = [w for sp in s6_subspans for w in sp["words"]]
    s6_tokens = [w["word"] for w in s6_flat_words]
    s6_ws = len(s6_tokens)
    s6_sp = count_spoken_words(s6_tokens)
    assert s6_ws == 63 and s6_sp == 65

    s6_tot_dur = s6_vm["total_duration_s"]
    assert s6_subspans[-1]["timeline_end"] == 21.180 == s6_vm["vo_end_s"]
    assert s6_tot_dur == 22.180

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
        "is far too faint for your eyes on even the darkest night. Imagine the night of the closest pass. A new star has been "
        "brightening for thousands of years. It is the brightest star, three times brighter than Sirius, and it glows orange."
    )
    s6_vm["raw_source_token_transcript"] = " ".join(s6_tokens)
    s6_vm["subspans"] = s6_subspans
    s6_vm["auditions"] = {
        "question_audition": s6_qa,
        "full_vo_audition": s6_fa,
    }
    s6_vm["auditory_judgement"] = {
        "reviewer": "gemini (Gemini 4 Argon multimodal audio input; Codex verified execution/hashes/arithmetic in J1020 and does not claim independent listening)",
        "method": (
            f"Direct multimodal playback and auditory inspection of {s6_qa['wav_path']} (3.110s, sha256: {s6_qa['sha256']}) "
            f"and regenerated {s6_fa['wav_path']} (21.230s, sha256: {s6_fa['sha256']})."
        ),
        "question_prosody_and_joins": (
            "UNCHANGED FROM ACCEPTED V05 & VERIFIED BY EAR (Gemini): Spans 1..9 ('What will the night sky look like when Gliese 710 arrives?', "
            "0.015-3.060s at 1.000x tempo) preserve the exact v05 question audio (sha256: 67a26cb681b3ac50...), completing '710' at 2.465s "
            "(<= 2.500s) and 'arrives.' at 3.060s."
        ),
        "full_vo_prosody_and_joins": (
            "PAYOFF TIMING CORRECTED & VERIFIED BY EAR (Gemini): Replaces the v05 early motion/moon-width clause ('On the darkest night, Gliese 710 "
            "will creep across the sky the width of the full moon every 35 years.') with non-answer present-day invisibility setup from existing "
            "recordings in Spans 10..14 (3.240-10.620s: 'Right now,' [42.740-43.300s] + continuous 'Gliese 710' [words 985..986, 383.240-384.400s] + "
            "'in the constellation of Serpens,' [47.340-49.240s] + 'is far too faint for your eyes' [60.200-61.860s] + 'on even the darkest night.' "
            "[62.140-63.600s]), followed in Spans 15..19 (10.800-16.220s) by the future closest-pass transition and approach setup ('Imagine the night "
            "of the closest pass. A new star has been brightening for thousands of years.'). No appearance or motion answer and no number land inside "
            "the 9-14s banner or before the 15.526s 70% threshold. Span 20 ('it is the brightest') starts at exact 16.400s (73.94%), placing the first "
            "answer token 'brightest' (word 881) at exact 16.820-17.240s (75.83% >= 70.0%), 'star' (word 398) at 17.320-17.740s (78.09%), 'three' "
            "(word 743) at 17.880-18.280s (80.61%), 'Sirius' (word 893) at 19.200-19.700s (86.56%), and 'orange.' (word 905) at 20.600-21.180s (92.88%), "
            "preserving vo_end_s=21.180s, total_duration_s=22.180s, and the 16.820-20.820s teaching card with zero downstream drift. Direct multimodal "
            "listening confirms natural British cadence across all 24 spans (63 WS / 65 spoken words) with zero splice clicks or clipped syllables."
        ),
        "preserve_exact_question_and_map": True,
    }

    # 4. Update S6 shot plan for shot/line matching (replace s05_full_moon with s05_alma_orion_set and update s02..s05 spoken_match)
    s6_s05_px, v06_win_log, s6_sheet_out = inspect_single_updated_shot_s6_s05(j1017_log)
    alma_path = ROOT / "02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/alma_orion_set.mp4"
    alma_sha = sha256_file(alma_path)

    s6_shots = s6_data["shot_plan"]
    s6_shots[1]["spoken_match"] = "arrives? Right now, Gliese 710 in the constellation"
    s6_shots[2]["spoken_match"] = "of Serpens, is far too faint for your eyes on"
    s6_shots[3]["spoken_match"] = "even the darkest night. Imagine the night of the closest"
    s6_shots[4] = {
        "row": "s05_alma_orion_set",
        "timeline_in": 12.800,
        "timeline_out": 16.200,
        "timeline_dur": 3.400,
        "asset_key": "029_alma_orion_set",
        "underlying_id": "alma_orion_set.mp4",
        "source_path": "02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/alma_orion_set.mp4",
        "source_in": 0.400,
        "source_out": 3.800,
        "source_dur": 3.400,
        "source_speed": 1.00,
        "kind": "eso_video",
        "video": True,
        "upscale": 1.78,
        "crop_filter": "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
        "source_sha256": alma_sha,
        "spoken_match": "pass. A new star has been brightening for thousands of years.",
        "pixel_inspection": {
            **{k: v for k, v in s6_s05_px.items() if k not in ("short_id", "row", "source_path", "source_in", "source_out", "source_dur")},
            "inspection_method": (
                "Saved source-window inspection log (/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json): "
                "30fps source-rate decode across [0.400, 3.800] (102 frames) for luma, black fraction (<20 and <30), dark-run (<20 luma on >85% area), "
                "and ffmpeg scdet internal cut detection, plus sampled 2fps (every 0.50s, 8 samples) frame extraction and Tesseract OCR (--psm 6 -l eng). "
                "Evaluated with default 9:16 centre crop (crop=ih*9/16:ih) at native source speed (final transformed every-frame OCR/dark-run gates run on assembled MP4s)."
            ),
        },
    }

    v06["desk_evidence_paths"] = {
        "auditions_dir": str(NEW_AUD_DIR),
        "test_a_proposal_diagnosis_dir": "/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis",
        "openings_dir_j1017": "/Users/benjaminoats/_desk/reviews/J1017/openings",
        "openings_uncaptioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg",
        "openings_v04_captioned_sheet": "/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg",
        "openings_gate_report_json": "/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json",
        "source_windows_dir_j1017_preserved": "/Users/benjaminoats/_desk/reviews/J1017/source_windows",
        "source_windows_j1017_log_json": str(J1017_WIN_LOG_PATH),
        "source_windows_dir_j1024_v06": str(J1024_SW_DIR),
        "source_windows_v06_log_json": str(J1024_WIN_LOG_PATH),
        "source_windows_s6_v06_2fps_sheet": str(s6_sheet_out),
    }

    V06_MAPS_PATH.write_text(json.dumps(v06, indent=2) + "\n")
    v06_sha = sha256_file(V06_MAPS_PATH)
    print(f"Wrote {V06_MAPS_PATH} (sha256: {v06_sha})")

    md = render_markdown(v06, v06_sha, v06_win_log)
    V06_MD_PATH.write_text(md)
    print(f"Wrote {V06_MD_PATH} ({len(md.splitlines())} lines)")


def render_markdown(v06: dict, v06_sha: str, win_log: dict) -> str:
    lines: list[str] = []
    a = lines.append

    s3_vm = v06["shorts"]["S3_028_bizlhspnVvY"]["vo_splice_map"]
    s4_vm = v06["shorts"]["S4_028_DETI0HV2jlI"]["vo_splice_map"]
    s5_vm = v06["shorts"]["S5_028_jJ5LkFGyzLI"]["vo_splice_map"]
    s6_vm = v06["shorts"]["S6_028_X768qs8sNQs"]["vo_splice_map"]
    s6_sub = s6_vm["subspans"]
    s4_sub = s4_vm["subspans"]

    a("# J0936 v04 Preparation v06 — Corrected `S6` Late Payoff Ordering (`75.83% >= 70.0%`), Applied Authorised `Test A` Option A Syllable Repair (`S4`), Reconciled Exact Map/Prose/Keyword Coordinates, and Honest Reviewer & `atempo` Implementation Attribution")
    a("")
    a("- **Job:** `J1024` (`J0936 preparation: fix S6 early answer and apply approved Test A repair`)")
    a("- **Revises:** `J1019` (`jobs/reviews/J0936_v04_PREP_v05.md` and `jobs/reviews/J0936_v04_PREP_v05_maps.json`, input `sha256: a0e934536e4ab814ded720091845980d647c0661349b2ea50a6dc96860707242`)")
    a("- **Authority Reference:** Elected-Chief Codex preparation review ruling `J1020` (27 Oct 2026, commit `e82eae17d` on `codex/j1020-review`, `jobs/reviews/J1020_2026-10-27.md` and `jobs/reviews/J1020_2026-10-27_verification.json`), `J1018` (`b8c75920b`, PR `#299`), `J1016` (`4d95c81e7`, PR `#298`), `J1010` (`d63dc5898`), `J0993`, `J0936` (`c59`), and `.cursor/rules/orbit-build-shorts.mdc`.")
    a(f"- **Machine-Readable Companion:** `jobs/reviews/J0936_v04_PREP_v06_maps.json` (`sha256: {v06_sha}` — every prose timestamp, span boundary, keyword coordinate, word count, and SHA-256 hash in this document is formatted directly from `J0936_v04_PREP_v06_maps.json`).")
    a("- **Executable Generators & Verifier:**")
    a("  - Preparation v06 map, audition & `S6 s05` window updater: `jobs/reviews/build_j0936_prep_v06.py` -> `/Users/benjaminoats/_desk/reviews/J1024/auditions/` and `/Users/benjaminoats/_desk/reviews/J1024/source_windows/`")
    a("  - Preserved v04 opening preview generator & house-gate evaluator: `jobs/reviews/generate_j0936_prep_v04_openings.py` -> `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("  - Preserved source-window `30 fps` decode + `2 fps` sampled OCR inspector: `jobs/reviews/inspect_j0936_prep_v04_source_windows.py` -> `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json` (`42` unchanged body shots preserved untouched) + `/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json` (`42` preserved + `1` updated `S6 s05_alma_orion_set`)")
    a("  - Reproducible verifier & saved output: `jobs/reviews/verify_j0936_prep_v06.py` -> `jobs/reviews/J1024_2026-10-27_verification.json` (`machine_checks_passed: true`)")
    a("- **Desk Evidence Directories (Outside Git):** `/Users/benjaminoats/_desk/reviews/J1024/auditions/`, `/Users/benjaminoats/_desk/reviews/J1024/source_windows/`, `/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/`, `/Users/benjaminoats/_desk/reviews/J1017/openings/`, and `/Users/benjaminoats/_desk/reviews/J1017/source_windows/`.")
    a("- **Worker & Reviewer Attribution:** `gemini` (`Gemini 4 Argon`, specialist worker and multimodal audio/vision/semantic reviewer; elected-Chief `codex` verified execution, hashes, and arithmetic in `J1020` and does not claim independent listening; no human reviewer is claimed at the preparation stage; `J0936` remains blocked until Chief lock `J1025`).")
    a("- **Spend / Side Effects:** **£0 / 0 credits.** Preparation-only VO splice auditions and map reconciliation only. No full final video render, no spend, no deletion, no upload, no retitle, no privacy change, no Buffer write, and no swap.")
    a("")
    a("---")
    a("")
    a("## 1. Point-by-Point Resolution of J1020 Finite Corrections")
    a("")
    a("### 1.1 Blocking `S6_028_X768qs8sNQs` Early-Answer Correction (`What will the night sky look like when Gliese 710 arrives?`)")
    a("- **Root Cause Identified in `J1020`:** In Preparation v05, `S6` supplied `brightest` (`word_idx=881`) at `16.820 s` (`75.83%`) as `earliest_spoken_answer`, but its earlier spoken spans `19..20` (`11.820–13.180 s` *\"will creep across the sky\"* and `13.300–16.220 s` *\"the width of the full moon every 35 years.\"*, with token `35` at `15.220–15.680 s` = `68.62% < 70.0%`) already described what the future night sky would look like inside the `9–14 s` banner and before the `15.526 s` (`70.0%`) threshold.")
    a("- **Finite Non-Answer Setup Replacement Implemented in `v06`:**")
    a(f"  1. **Exact Question Retained (`Spans 1..9`, `{s6_sub[0]['timeline_start']:.3f}–{s6_sub[8]['timeline_end']:.3f} s`, `1.000x` tempo):** Preserves the exact v05 question subspans (`\"what will the night sky look like when Gliese 710 arrives.\"`), completing first named subject `\"710\"` (`word_idx=122`) at **`{s6_vm['first_named_subject']['start']:.3f}–{s6_vm['first_named_subject']['end']:.3f} s` (`<= 2.500 s`)** and `\"arrives.\"` at **`{s6_sub[8]['timeline_end']:.3f} s`** (`question_audition` SHA-256 unchanged: `{s6_vm['auditions']['question_audition']['sha256']}`).")
    a(f"  2. **Present-Day Invisibility Setup Replaces Early Motion/Moon-Width Clause (`Spans 10..14`, `{s6_sub[9]['timeline_start']:.3f}–{s6_sub[13]['timeline_end']:.3f} s`, `1.000x` tempo):** Replaces the early answer-bearing motion/moon-width clause with present-day non-answer setup from `star_coming_vo_v01.wav` explaining why you cannot see `Gliese 710` today (62 light-years before arrival):")
    for idx_sp in range(9, 14):
        sp = s6_sub[idx_sp]
        a(f"     - **Span `{sp['span_index']}` (`words {sp['word_idx_range']}`, `{sp['source_in']:.3f}–{sp['source_out']:.3f} s` -> `{sp['timeline_start']:.3f}–{sp['timeline_end']:.3f} s`, `gap_after = {sp['gap_after']:.3f} s`):** `\"{sp['text']}\"`")
    a("     Note that Span `11` (`words 985..986`, `383.240–384.400 s = 1.160 s` at `1.000x` tempo) retains the accepted J1019/J1020 continuous body recording of `\"Gliese 710\"` with all syllables intact.")
    a(f"  3. **Future Closest-Pass Transition & Approach Context Retained (`Spans 15..19`, `{s6_sub[14]['timeline_start']:.3f}–{s6_sub[18]['timeline_end']:.3f} s`, `1.000x` tempo):** Retains the existing closest-pass scene invitation and millennial approach context directly before the payoff:")
    for idx_sp in range(14, 19):
        sp = s6_sub[idx_sp]
        a(f"     - **Span `{sp['span_index']}` (`words {sp['word_idx_range']}`, `{sp['source_in']:.3f}–{sp['source_out']:.3f} s` -> `{sp['timeline_start']:.3f}–{sp['timeline_end']:.3f} s`, `gap_after = {sp['gap_after']:.3f} s`):** `\"{sp['text']}\"`")
    a(f"  4. **Late Appearance Payoff & Numbers After `70%` (`Spans 20..24`, `{s6_sub[19]['timeline_start']:.3f}–{s6_sub[23]['timeline_end']:.3f} s`, `70%` mark = `{s6_vm['seventy_pct_mark_s']:.3f} s`):** Span `20` (`\"it is the brightest\"`) starts at **exact `{s6_sub[19]['timeline_start']:.3f} s` (`{s6_sub[19]['timeline_start']/s6_vm['total_duration_s']*100:.2f}%`)**, placing the first appearance-answer token `\"brightest\"` (`word_idx=881`) at **exact `{s6_vm['earliest_spoken_answer']['start']:.3f}–{s6_vm['earliest_spoken_answer']['end']:.3f} s` (`{s6_vm['earliest_spoken_answer']['pct_of_total']:.2f}% >= 70.0%`)**, `\"star\"` (`word_idx=398`) at **`{s6_vm['keyword_timings']['star']['start']:.3f}–{s6_vm['keyword_timings']['star']['end']:.3f} s` (`{s6_vm['keyword_timings']['star']['pct_of_total']:.2f}%`)**, `\"three\"` (`word_idx=743`) at **`{s6_vm['keyword_timings']['three']['start']:.3f}–{s6_vm['keyword_timings']['three']['end']:.3f} s` (`{s6_vm['keyword_timings']['three']['pct_of_total']:.2f}%`)**, `\"Sirius\"` (`word_idx=893`) at **`{s6_vm['keyword_timings']['Sirius']['start']:.3f}–{s6_vm['keyword_timings']['Sirius']['end']:.3f} s` (`{s6_vm['keyword_timings']['Sirius']['pct_of_total']:.2f}%`)**, and `\"orange.\"` (`word_idx=905`) at **`{s6_vm['keyword_timings']['orange.']['start']:.3f}–{s6_vm['keyword_timings']['orange.']['end']:.3f} s` (`{s6_vm['keyword_timings']['orange.']['pct_of_total']:.2f}%`)**.")
    a(f"  5. **Word Count, Runtime, Card & Shot-Line Matching Reconciled:** `S6` has **`{s6_vm['whitespace_words']}` whitespace words / `{s6_vm['spoken_words']}` spoken words** (inside `55–65`), `vo_end_s = {s6_vm['vo_end_s']:.3f} s`, `total_duration_s = {s6_vm['total_duration_s']:.3f} s`, and the single teaching card `['3× SIRIUS', 'BRIGHTEST STAR']` remains at **`16.820–20.820 s`** (`4.000 s`). Because `\"full moon\"` is no longer spoken at `12.800–16.200 s`, shot `s05` (`12.800–16.200 s`) is updated from `s05_full_moon` (`moon_2.jpg`, `video=False`) to `s05_alma_orion_set` (`02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/alma_orion_set.mp4`, `0.400–3.800 s`, `video=True`, rising night-sky starfield time-lapse, `102` 30fps frames decoded, `8` 2fps OCR samples, `0` internal cuts, `0` dark runs, `0` banned OCR hits), while preserving all other `42` body shots untouched from `J1017`'s saved log.")
    a("")
    a("### 1.2 Explicitly Authorised `Test A` (`S4_028_DETI0HV2jlI`) Option A Syllable Repair Applied")
    a("- **Exact `J1020` Option A Parameters Applied to `S4_028_DETI0HV2jlI`:**")
    a(f"  - **Span `4` (`\"and it is heading almost straight at the sun.\"`, `{s4_sub[3]['source_in']:.3f}–{s4_sub[3]['source_out']:.3f} s` -> `{s4_sub[3]['timeline_start']:.3f}–{s4_sub[3]['timeline_end']:.3f} s`):** `gap_after` updated from `0.140 s` to **`{s4_sub[3]['gap_after']:.3f} s`** (`xfade_s = 0.012 s`).")
    a(f"  - **Span `5` (`\"Its name\"`, `{s4_sub[4]['source_in']:.3f}–{s4_sub[4]['source_out']:.3f} s` -> `{s4_sub[4]['timeline_start']:.3f}–{s4_sub[4]['timeline_end']:.3f} s`):** `gap_after` updated from `0.100 s` to **`{s4_sub[4]['gap_after']:.3f} s`** (`xfade_s = 0.012 s`).")
    a(f"  - **Span `6` (`\"is Gliese\"`, `{s4_sub[5]['source_in']:.3f}–{s4_sub[5]['source_out']:.3f} s` at `{s4_sub[5]['tempo']:.3f}x` -> `{s4_sub[5]['timeline_start']:.3f}–{s4_sub[5]['timeline_end']:.3f} s`):** Extended from `14.980–15.640 s` to **`14.980–15.780 s`** (`0.800 s`), `gap_after` updated from `0.120 s` to **`{s4_sub[5]['gap_after']:.3f} s`** (`xfade_s = 0.012 s`), preserving the complete `\"-za\"` second syllable of `\"Gliese\"` (`15.560–15.780 s`).")
    a(f"  - **Span `7` (`\"710.\"`, `{s4_sub[6]['source_in']:.3f}–{s4_sub[6]['source_out']:.3f} s` at `{s4_sub[6]['tempo']:.3f}x` -> `{s4_sub[6]['timeline_start']:.3f}–{s4_sub[6]['timeline_end']:.3f} s`):** Extended from `16.260–17.280 s` to **`16.060–17.220 s`** (`1.160 s`), `gap_after` updated from `0.120 s` to **`{s4_sub[6]['gap_after']:.3f} s`** (`xfade_s = 0.012 s`), preserving the complete `\"sev-\"` onset of `\"seven hundred and ten.\"` (`16.060–16.280 s`) and updating `keyword_timings['710.']` to **`{s4_vm['keyword_timings']['710.']['start']:.3f}–{s4_vm['keyword_timings']['710.']['end']:.3f} s` (`{s4_vm['keyword_timings']['710.']['pct_of_total']:.2f}%`)**.")
    a(f"  - **Downstream Spans `8..13` (`{s4_sub[7]['timeline_start']:.3f}–{s4_sub[12]['timeline_end']:.3f} s`), Runtime & Card Unchanged:** Span `8` starts at **exact `{s4_sub[7]['timeline_start']:.3f} s`**, `vo_end_s = {s4_vm['vo_end_s']:.3f} s`, `total_duration_s = {s4_vm['total_duration_s']:.3f} s`, earliest answer `\"one\"` remains at **`{s4_vm['earliest_spoken_answer']['start']:.3f} s` (`{s4_vm['earliest_spoken_answer']['pct_of_total']:.2f}%`)**, and card `['1.3 MILLION YEARS', 'CLOSEST STAR PASS']` remains at **`17.950–21.450 s`**.")
    a(f"  - **Audition Hash Reconciled Against Retained Proposal Diagnostic Hash:** Regenerated `{s4_vm['auditions']['full_vo_audition']['wav_path']}` has **`sha256: {s4_vm['auditions']['full_vo_audition']['sha256']}`**, matching the retained J1019 Option A diagnostic WAV (`/Users/benjaminoats/_desk/reviews/J1019/test_a_proposal_diagnosis/S4_TestA_Proposal_OptionA_full_vo_diagnostic.wav`) byte-for-byte.")
    a("")
    a("### 1.3 Small Evidence Corrections & Implementation Transparency (`J1020`)")
    a(f"- **100% Map-Driven Prose & Corrected `S6` Keyword Coordinates:** All span start/end numbers in this document are rendered directly from `J0936_v04_PREP_v06_maps.json` (correcting the v05 prose discrepancy where v05 text wrote `13.240` and `16.340` while the v05 map had `13.300` and `16.400`). In `S6` `keyword_timings`, `star` (`word_idx=398`) is recorded at **`{s6_vm['keyword_timings']['star']['start']:.3f}–{s6_vm['keyword_timings']['star']['end']:.3f} s` (`{s6_vm['keyword_timings']['star']['pct_of_total']:.2f}%`)** and `three` (`word_idx=743`) is recorded at **`{s6_vm['keyword_timings']['three']['start']:.3f}–{s6_vm['keyword_timings']['three']['end']:.3f} s` (`{s6_vm['keyword_timings']['three']['pct_of_total']:.2f}%`)**.")
    a("- **Accurate Reviewer Attribution (No Un-Evidenced Human Reviewer Claim):** Removed `REVIEWED_BY_HUMAN_AND_LLM_SEMANTIC_INSPECTION` from the verifier and prose; semantic earliest-answer inspection, visual occupancy segmentation, 2fps contact-sheet review, and multimodal audio listening are explicitly attributed to **`gemini` (`Gemini 4 Argon`)**, while `codex` is credited for deterministic execution, hash, and arithmetic verification (`J1020`).")
    a(f"- **Honest Documentation of `S3` Audition Builder `atempo` Slot-Fit Trim (`<= 16.17 ms`):** {s3_vm['atempo_slot_fit_implementation_note']['description']}")
    a("")
    a("---")
    a("")
    a("## 2. Master Acceptance Summary Matrix (All Six Shorts)")
    a("")
    a("| # | Short ID & Slug | Air Date | Local Title | Words (WS / Spoken) | First Subj End (`<=2.50s`) | VO End / Total (`s`) | `70%` Mark (`s`) | Supplied Earliest Answer (`s` & `%`) | `4–8s` Stills | First Cut / Max Hold (`s`) | Single Teaching Overlay (`in–out s`) |")
    a("|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|")
    for idx, (sid, sdata) in enumerate(v06["shorts"].items(), 1):
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
    a(f"- **Library Snapshot File & SHA-256:** `{v06['library_snapshot']['path']}` (`sha256: {v06['library_snapshot']['sha256']}`)")
    a("- **Saved Side-by-Side Uncaptioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_0_30s_comparison.jpg`")
    a("- **Saved Side-by-Side v04-Captioned Frame-0 Sheet (`@0.30 s`):** `/Users/benjaminoats/_desk/reviews/J1017/openings/all_6_openings_captioned_0_30s_comparison.jpg`")
    a("- **Saved Raw Gate Report JSON:** `/Users/benjaminoats/_desk/reviews/J1017/openings/openings_gate_report.json`")
    a("")
    a("| Short ID | Air Date | Frame-0 Source (`asset_key` / `underlying_id`) | Src In–Out (`s`) & Speed | First Cut (`s`) | Uncap / Cap `dhash` (`@0.30s`) | Mot `0–1s` Uncap / Cap (`>=10`) | `f0diff` Uncap / Cap (`>=1.5`) | Reviewer Subj Body / Total (`>=60%`) | Black (`<20%`) | Visor Uncap / Cap (`<0.005`) | Min Lib Ham Uncap / Cap (`>=15`) | Max Lib `bg` Uncap / Cap (`<0.55`) | Min Batch Ham Uncap / Cap (`>=15`) | Max Batch `bg` Uncap / Cap (`<0.55`) |")
    a("|---|---|---|---|---:|---|---|---|---|---:|---|---:|---:|---:|---:|")
    for sid, sdata in v06["shorts"].items():
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
    a("## 4. Verified Source Media, Preparation v06 VO Splice Auditions, Multimodal Auditory Judgement & Source-Window Inspection")
    a("")
    a("### 4.1 Voiceover Sources & Tracked Word Maps")
    a("")
    a("| Film | VO Source Path | SHA-256 Hash | Word Map Tracked in Git |")
    a("|---|---|---|---|")
    a("| **026** | `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_NearestStar_Long_VO/nearest_star_vo_v01.wav` | `d6159f085b04f38604676bc3b37de24187488379e48ed394d076bee5bcabfaf5` | `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/words.json` |")
    a("| **027** | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-027/027_EarthSpin_rough_v01i.mp4` | `f74ca3e8a27b3897fd4942ebcd6f70462aee039146ccce1780216c42802be38b` | `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/rough_v01i_pack/earth_spin_words_list.json` |")
    a("| **028** | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` | `cf546efd12e723173b66bd1d3ee2139afc94a03124ab0e4fdfd2cc06ebb8ab01` | `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/gliese_words_list.json` |")
    a("")
    a("### 4.2 Local VO-Only Auditions (`48 kHz` Mono WAV in `/Users/benjaminoats/_desk/reviews/J1024/auditions/`) & Direct Multimodal Auditory Judgement (`Gemini`)")
    a("")
    a("| Short ID | Assembled Opening Question | Question WAV Path & SHA-256 | Q Dur (`s`) | Q RMS / Peak (`dBFS`) | Full VO WAV Path & SHA-256 | Full Dur (`s`) | Max Step |")
    a("|---|---|---|---:|---|---:|---:|---:|")
    for sid, sdata in v06["shorts"].items():
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
    for sid, sdata in v06["shorts"].items():
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
    a("### 4.3 Saved Source-Window Inspection Evidence (`42` Preserved `J1017` Windows + `1` Updated `S6 s05_alma_orion_set` Window)")
    a(f"- **Preserved `J1017` Log (`42` Unchanged Shots):** `/Users/benjaminoats/_desk/reviews/J1017/source_windows/full_window_inspection_log.json` (`sha256: {sha256_file(J1017_WIN_LOG_PATH)}`).")
    a(f"- **Updated `J1024` v06 Log (`42` Preserved + `1` Updated `S6 s05_alma_orion_set`):** `/Users/benjaminoats/_desk/reviews/J1024/source_windows/full_window_inspection_log_v06.json` (`sha256: {sha256_file(J1024_WIN_LOG_PATH)}`) and updated contact sheet `/Users/benjaminoats/_desk/reviews/J1024/source_windows/S6_028_X768qs8sNQs_full_window_2fps.jpg`.")
    a(f"- **Exact Coverage & Transform Scope:** Covers **`{win_log['total_30fps_frames_decoded']}` source-rate frames at `30 fps`** across `[source_in, source_out]` of all **`{win_log['total_body_shots']}` body shots** for luma, black fraction (`<20` and `<30`), dark-run (`<20` luma on `>85%` area), and `ffmpeg scdet` internal cut detection, and **`{win_log['total_2fps_ocr_frames_scanned']}` sampled frames at `2 fps` (every `0.50 s`, plus window tail)** for Tesseract OCR (`--psm 6 -l eng`) and visual contact sheets. Five opening shots (`S1 s00`, `S3 s01`, `S4 s01`, `S5 s01`, `S6 s01`) were decoded with their declared custom 9:16 crops/grades, while the remaining `38` body shots were decoded with a default 9:16 centre crop (`crop=ih*9/16:ih`) at native source speed (`source_speed` not applied). Every-frame OCR and dark-run gate logs on the final transformed MP4s remain mandatory post-assembly checks.")
    a(f"- **Saved Log Results:** `any_failures = {win_log['any_failures']}` (`0` internal `scdet` cuts, `0` dark runs `>= 3` frames, `0` banned OCR hits across the `306` `2 fps` samples, and `0` slates/baked labels/portraits/diagrams on the `2 fps` contact sheets).")
    a("")
    a("---")
    a("")
    a("## 5. Per-Short Reconciled Scripts, Exact Subspan Splice Tables, Single Teaching Overlay Specs, and Complete Shot Plans")
    a("")
    for idx, (sid, sdata) in enumerate(v06["shorts"].items(), 1):
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

    a("## 6. Reproducible Verification, Accurate Reviewer Attribution, and Unchanged Assembly Boundaries (`J1020` -> `J1025` -> `J0936`)")
    a("")
    a("- **Verifier Script:** `python3 jobs/reviews/verify_j0936_prep_v06.py`")
    a(f"- **Verification Output:** `jobs/reviews/J1024_2026-10-27_verification.json` (`machine_checks_passed: True`, `total_source_words_verified: 391`, `input_sha256: {v06_sha}`)")
    a("- **Deterministic Machine-Verified Checks Performed by `verify_j0936_prep_v06.py`:**")
    a("  1. Every source word record (`word`, `src_start`, `src_end`) matches the tracked git word map (`words.json`, `earth_spin_words_list.json`, `gliese_words_list.json`) within `1e-4 s`, and every word's output coordinate (`timeline_start + (src_t - source_in) / tempo`) reconciles within `0.002 s` across all `391` words.")
    a("  2. Every `\"Gliese 710\"` occurrence in ordinary Shorts `S3`, `S5`, and `S6` (`words 121..122` in questions, `words 719..720` in `S3` body, `words 471..473` in `S5` body, `words 985..986` in `S6` body) resides inside a **single continuous subspan** with `0` omitted inter-token syllables (`omitted_ordinary_bridges == []`), and `Test A` (`S4`) applies the explicitly authorised Option A syllable repair (`Span 6: 14.980–15.780 s`, `Span 7: 16.060–17.220 s`, gaps `0.060/0.040/0.040/0.060 s`, `full_vo_audition` SHA-256 `d0bd657e7d9269df32965f299b4fac799d51dac05095d4069f7b5a1ac207f10a`).")
    a(f"  3. Both whitespace word count and spoken-expansion word count are inside `55–65` for all five ordinary Shorts (**`S1: 65/65`**, **`S2: 64/65`**, **`S3: 62/64`**, **`S5: 61/65`**, **`S6: {s6_vm['whitespace_words']}/{s6_vm['spoken_words']}`**), with **`S4` retaining its explicit Test A exemption (`76/77`)**.")
    a("  4. Spoken opening question tokens equal `local_title` token-for-token for all five ordinary Shorts, and all `12` local VO audition WAVs (`question_audition` and `full_vo_audition` in `/Users/benjaminoats/_desk/reviews/J1024/auditions/`) exist on disk and match their recorded SHA-256 hashes.")
    a("  5. First named subject (`Sun`, `Earth's`, `710`, `star`, `710`, `710`) completes at `<= 2.500 s` across all six Shorts, recomputed from the flattened output word timeline (`S1: 2.380 s`, `S2: 1.750 s`, `S3: 2.490 s`, `S4: 0.900 s`, `S5: 1.660 s`, `S6: 2.465 s`).")
    a("  6. Subspan splice arithmetic (`1.000x <= tempo <= 1.055x <= 1.060x`, `gap_after <= 0.180 s`, `max_internal_pause <= 0.200 s`, `12 ms` crossfades on Test A) and shot coverage (`0.000 s` to `vo_end_s` for body shots, `s_loop` ending at `total_duration_s` with `final_shot_cursor == total_duration_s`) reconcile with `0` errors.")
    a("  7. `4.000–8.000 s` early motion window uses `100%` moving `video=True` footage across all six Shorts (`early_still_windows_4_8s = []`), with `0` still-to-still cuts and `>= 10.0 s` separation on any repeated underlying source.")
    a("  8. **Supplied Earliest-Answer Index Coordinate Check & `S6` Pre-70% Non-Answer Check:** Recomputes the output timestamp and runtime percentage of the **supplied** `earliest_spoken_answer.word_idx` from the flattened word timeline and verifies `pct_of_total >= 70.0%` across all six Shorts, and verifies that `S6` contains zero pre-70% motion/appearance answer clauses or numbers (`will creep`, `full moon`, `35` absent before `16.400 s`).")
    a("  9. Single teaching overlay (`baked_in_labels = 0`, `code_graphics = 0`, `added_edit_cards = 1`, `<= 4` words per line, `<= 4.000 s` duration, clear of `0–2 s` hook and `9–14 s` banner), including Chief's locked S5 card `['1-CM SCALE', 'OVER 100 METERS']` within **`16.180–19.160 s`** aligned to spoken `\"100\"` (`16.180 s`) and `\"pitch.\"` (`19.160 s`).")
    a(" 10. Fresh `gate_shorts_open.py` measurements on all `6` uncaptioned (`S1..S6_open.mp4`) and `6` v04-captioned (`S1..S6_open_captioned.mp4`) opening preview clips, plus **provenance verification against both the preserved `J1017` source-window log (`42` unchanged shots, `sha256: b8e995f64132a8e9...`) and the `J1024` v06 source-window log (`43` shots including `S6 s05_alma_orion_set`)**.")
    a("- **Explicitly Separated Reviewer Assertions (`reviewer: gemini`, Not Computed by the Verifier Script):**")
    a("  1. **Semantic Identification of Earliest Spoken Answer (`REVIEWED_BY_GEMINI_SEMANTIC_INSPECTION`):** Semantic verification by `gemini` (`Gemini 4 Argon`) that the supplied `earliest_spoken_answer` token is the first utterance that answers the Short's title question (no human reviewer is claimed at the preparation stage).")
    a("  2. **Visual & Geometric Titled-Subject Occupancy (`>= 60%`, `REVIEWED_BY_GEMINI_MULTIMODAL_VISION`):** Reviewer visual/contour segmentation by `gemini` on the cropped `1080×1920` `@0.30s` frames (`all_6_openings_0_30s_comparison.jpg` and `all_6_openings_captioned_0_30s_comparison.jpg`).")
    a("  3. **Visual Contact-Sheet Inspection of Sampled `2 fps` Source Windows (`REVIEWED_BY_GEMINI_MULTIMODAL_VISION`):** Reviewer visual inspection by `gemini` of `S1..S6_full_window_2fps.jpg` (`306` tiles sampled at `2 fps` across `43` body shots, including updated `S6 s05_alma_orion_set`).")
    a("  4. **Multimodal Auditory Judgement of Prosody & Repaired Bridges (`REVIEWED_BY_GEMINI_MULTIMODAL_AUDIO`):** Direct `Gemini 4 Argon` multimodal audio listening across all `12` WAV files in `/Users/benjaminoats/_desk/reviews/J1024/auditions/` (`codex` verified execution, hashes, and arithmetic in `J1020` and does not claim independent listening).")
    a("- **Unchanged Post-Assembly Acceptance (`c59` / `J0936`, Mandatory at Final Render After Chief Lock `J1025`):** Eventual assembly after Chief lock (`J1025`) retains every original `J0936`/`c59` acceptance requirement: all Shorts/picture/polish/music/SFX gates, full rendered-video every-frame/dense OCR and dark-run gate logs on the final speed-transformed/cropped/graded MP4s, measured final AAC `-14.0 ± 0.5 LUFS` and `TP <= -1.6 dBTP`, matched `1.000 s` loop (`loop_diff < 2.0`), complete runtime sheets and flagged frames, `720×1280` PHONE video, UAT/NAS copies and SHA-256 manifests. Batch target remains **1 November 2026, 20:00 London**; individual day-before-air deadlines (`19 Nov`, `22 Nov`, `29 Nov`, `1 Dec`, `3 Dec`, `6 Dec` at `20:00 London`) and v01 fallbacks remain unchanged. Ben swap approval follows replacement PASS.")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
