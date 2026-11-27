#!/usr/bin/env python3
"""064 Every Planet Explained — Companion Short 1 (Test A Opening Short) v03 Repair Builder (J3922).

Repairs the critical missing-narration defect found in v02 (J3918 / PR #1400, Chief FIX ruling on J3918):
- Root cause in v02: `_build_064_short01_testA_v02.py` placed `-ss` after `-i` before `afade=t=out`,
  fading nonzero-source-offset segments S2/S3/S4 to silence (±1 LSB PCM dither at -90.31 dBFS) before
  output-seeking.
- Fix in v03: Slice locked VO via `atrim=start=...:end=...,asetpts=PTS-STARTPTS` strictly before
  `afade=t=in` / `afade=t=out`, rebuild all 4 complete 71-word narration segments, normalize VO,
  re-duck score bed, re-level house SFX, remix and AAC-calibrate.
- Video reuse: Stream-copies verified `v02` video track (`-c:v copy`) unchanged and proves both
  encoded bitstream (`streamhash`) and decoded-frame (`framemd5`) equivalence across all 738 frames.
  Per Chief ruling on J3918, this reuse is strictly for audio repair, NOT a visual/motion PASS.
- Regression proof: Compares output speech coverage against locked source intervals on all segments
  (explicitly covering nonzero-source-offset segments, genuine pauses, and -90.31 dBFS PCM dither),
  proving old `v02` FAILS and repaired `v03` PASSES; also verifies all 71 words via fresh local
  `faster-whisper` ASR decoded directly from final muxed `v03.mp4` and `v03_vo.wav`.
- Immutability & zero spend: £0 cash, 0 ElevenLabs chars, 0 Flow/Vertex credits; preserves `v01` and
  `v02` NAS masters, stems, and manifests untouched. Zero upload, schedule, privacy, or Buffer changes.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
NAS_ROOT = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
NAS_FILM = NAS_ROOT / "064_Every-Planet-Explained-In-10-Minutes"
NAS_SHORTS = NAS_FILM / "10_Shorts"
NAS_SUB_OUT = NAS_SHORTS / "short01_testA_opening" / "06_Final-Exports"

MASTER_V03 = NAS_FILM / "09_Final-Export" / "064_every_planet_explained_master_v03.mp4"
EXPECTED_MASTER_SHA256 = "d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a"
VO_WAV = NAS_FILM / "02_Voiceover" / "every_planet_explained_vo_v01.wav"
EXPECTED_VO_SHA256 = "4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa"
STT_JSON = NAS_FILM / "02_Voiceover" / "stt" / "every_planet_explained_vo_v01" / "stt_raw.json"
BED_MP3 = NAS_FILM / "05_Music" / "every_planet_score_bed_v01.mp3"
EXPECTED_BED_SHA256 = "3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6"
KIT_DIR = NAS_FILM / "06_Sound-Effects" / "kit_v01"

V01_NAS_MP4 = NAS_SUB_OUT / "064_short01_testA_opening_v01.mp4"
EXPECTED_V01_SHA256 = "b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6"
V02_NAS_MP4 = NAS_SUB_OUT / "064_short01_testA_opening_v02.mp4"
EXPECTED_V02_SHA256 = "8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968"
V02_NAS_VO = NAS_SUB_OUT / "064_short01_testA_opening_v02_vo.wav"
V02_NAS_COVER = NAS_SUB_OUT / "064_short01_testA_opening_v02_cover.jpg"
EXPECTED_V02_COVER_SHA256 = "0e5b993776582f461091268acec11f8c4a34c8a320428605898ae7b884a3054e"
V02_META_GIT = HERE / "06_Final-Exports" / "064_short01_testA_opening_v02_meta.json"
V02_SUMMARY_GIT = HERE / "06_Final-Exports" / "064_short01_testA_opening_v02_summary.json"
V02_CUTS_GIT = HERE / "06_Final-Exports" / "064_short01_testA_opening_v02_cuts.json"
V02_POOL_GIT = HERE / "06_Final-Exports" / "064_short01_testA_opening_v02_pool.json"

SCRATCH_BASE = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch"))
WORK = SCRATCH_BASE / "J3922_064_short01_v03"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "scripts"))
import gate_shorts_open as gso  # noqa: E402
import orbit_cfr_delivery as cfr  # noqa: E402
import sfx_kit  # noqa: E402

W, H, FPS = 1080, 1920, 24
SR = 48000
TOTAL_FRAMES = 738
TOTAL_S = TOTAL_FRAMES / FPS  # 30.750 s exact at 24 fps CFR

STEM = "064_short01_testA_opening_v03"
SHORT_SLUG = "short01_testA_opening"
SHORT_TITLE = "Why Does Water Ice Survive 430°C Heat on Mercury?"
ALT_TITLE = "How Does Mercury Hide Water Ice at 430°C?"
AIR_DATE = "2026-12-28"  # Unchanged non-colliding Mon/Wed/Fri/Sat candidate slot; NOT scheduled
LONG_TITLE = "Every Planet Explained in 12 Minutes (Mercury to Neptune)"

HOOK_END = 2.10
TITLE_IN, TITLE_OUT = 9.00, 14.00
TEACH_IN, TEACH_OUT = 23.75, 27.70
TEACH_TEXT = "1965 · GIUSEPPE COLOMBO"
END_CARD_IN = 714 / FPS  # 29.750 s exact

# Verbatim S1-S4 from locked every_planet_explained_vo_v01.wav (71 spoken words)
VO_SEGMENTS = [
    (0.060, 6.600),   # S1: "On Mercury, the sun's closest planet, why does water ice survive 430-degree heat?"
    (7.560, 11.050),  # S2: "The ice hides in polar craters that never see sunlight."
    (11.890, 25.140), # S3: "At 58 million km out, sunlight shines up to 7x brighter than on Earth, yet ... -180 °C."
    (26.280, 32.600), # S4: "In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery."
]
VO_LEAD_S = 0.000
VO_GAPS = [0.060, 0.080, 0.020]

# PCM 16-bit ±1 LSB dither reference: 20*log10(1/32768) = -90.309 dBFS
PCM16_LSB_DBFS = round(20.0 * math.log10(1.0 / 32768.0), 2)


def run(cmd: list) -> None:
    sp.run([str(c) for c in cmd], check=True)


def run_gate(cmd: list) -> sp.CompletedProcess:
    return sp.run([str(x) for x in cmd], capture_output=True, text=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        sr = w.getframerate()
        sw = w.getsampwidth()
        ch = w.getnchannels()
        assert sr == SR and sw == 2, f"Unexpected WAV format in {p}: sr={sr}, sw={sw}, ch={ch}"
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        if ch == 1:
            return np.stack([a, a], axis=-1)
        assert ch == 2, f"Unsupported channel count {ch} in {p}"
        return a.reshape(-1, 2)


def write_wav(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    z = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if z.any():
        idx = np.arange(z.sum())
        pcm[z, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[z, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def silence(n: int) -> np.ndarray:
    return np.zeros((max(0, n), 2), dtype=np.float32)


def rms_dbfs(x: np.ndarray) -> float:
    if x.size == 0:
        return -120.0
    val = float(np.sqrt(np.mean(np.square(x, dtype=np.float64))))
    return round(20.0 * math.log10(max(val, 1e-6)), 2)


def peak_abs(x: np.ndarray) -> float:
    if x.size == 0:
        return 0.0
    return round(float(np.max(np.abs(x))), 6)


def build_voice_plan() -> tuple[list[dict], list[dict], float]:
    stt = json.loads(STT_JSON.read_text())
    raw_words = [w for w in stt["words"] if w.get("text", "").strip()]
    slices = []
    words = []
    local = VO_LEAD_S
    for si, (a, b) in enumerate(VO_SEGMENTS):
        dur_s = round(b - a, 3)
        seg_words = []
        for w in raw_words:
            if w["end"] <= a + 0.005 or w["start"] >= b - 0.005:
                continue
            s = round(w["start"] - a + local, 3)
            e = round(min(b, w["end"]) - a + local, 3)
            txt = w["text"].strip()
            if txt.lower() == "kilometers":
                txt = "kilometres"
            entry = {
                "text": txt,
                "w": txt,
                "s": s,
                "e": e,
                "start": s,
                "end": e,
                "seg_idx": si,
                "src_start": round(float(w["start"]), 3),
                "src_end": round(float(min(b, w["end"])), 3),
            }
            words.append(entry)
            seg_words.append(entry)
        slices.append({
            "seg_idx": si,
            "a": a,
            "b": b,
            "dur": dur_s,
            "local": round(local, 3),
            "local_end": round(local + dur_s, 3),
            "nonzero_source_offset": a > 0.0,
            "word_count": len(seg_words),
        })
        local = round(local + dur_s, 3)
        if si < len(VO_GAPS):
            local = round(local + VO_GAPS[si], 3)
    return slices, words, words[-1]["e"]


def srt_chunks_full(words: list[dict], vo_end: float) -> list[dict]:
    """Full spoken-word SRT cues covering 100% of VO, preserving commas/full stops/question marks."""
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["e"] + 0.35, vo_end)
        text = " ".join(x["w"] for x in c)
        if end - start >= 0.12:
            out.append({"text": text, "s": round(start, 3), "e": round(min(end, vo_end), 3)})
    return out


def write_srt(caps: list[dict], dst: Path) -> None:
    def fmt(t: float) -> str:
        ms = int(round(t * 1000))
        hh, rem = divmod(ms, 3600_000)
        mm, rem = divmod(rem, 60_000)
        ss, mmm = divmod(rem, 1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d},{mmm:03d}"

    lines = []
    for idx, c in enumerate(caps, 1):
        lines.append(f"{idx}\n{fmt(c['s'])} --> {fmt(c['e'])}\n{c['text']}\n")
    dst.write_text("\n".join(lines))


def check_vo_speech_coverage(
    src_vo_wav: Path,
    out_vo_wav: Path,
    slices: list[dict],
    words: list[dict],
    label: str,
) -> dict:
    """Meaningful speech-coverage regression check against locked source intervals.

    Detects unexpected dropouts on all segments (especially nonzero-source-offset segments),
    while cleanly allowing genuine pauses in the locked source and accounting for ±1 LSB PCM
    dither (-90.31 dBFS).
    """
    src = read_wav(src_vo_wav)
    out = read_wav(out_vo_wav)
    win_n = int(round(0.200 * SR))  # 200 ms windows
    edge_n = int(round(0.020 * SR))  # skip 20 ms fade edges
    src_active_thresh_db = -45.0
    out_active_thresh_db = -45.0
    dropout_src_thresh_db = -40.0
    dropout_out_thresh_db = -60.0

    segments_report = []
    failures = []

    for sl in slices:
        si = sl["seg_idx"]
        a, b, local = sl["a"], sl["b"], sl["local"]
        s0, s1 = int(round(a * SR)), int(round(b * SR))
        seg_n = s1 - s0
        o0 = int(round(local * SR))
        o1 = min(len(out), o0 + seg_n)
        src_seg = src[s0:s1]
        out_seg = out[o0:o1]
        if len(out_seg) < len(src_seg):
            out_seg = np.pad(out_seg, ((0, len(src_seg) - len(out_seg)), (0, 0)))

        src_seg_db = rms_dbfs(src_seg)
        out_seg_db = rms_dbfs(out_seg)
        out_seg_peak = peak_abs(out_seg)

        # 200 ms window comparison (excluding 20 ms fade edges)
        src_wins = []
        out_wins = []
        win_starts = []
        pos = edge_n
        while pos + win_n <= seg_n - edge_n:
            src_wins.append(rms_dbfs(src_seg[pos:pos + win_n]))
            out_wins.append(rms_dbfs(out_seg[pos:pos + win_n]))
            win_starts.append(round(local + pos / SR, 3))
            pos += win_n

        src_w = np.array(src_wins, dtype=np.float64)
        out_w = np.array(out_wins, dtype=np.float64)
        src_active_mask = src_w > src_active_thresh_db
        src_pause_mask = ~src_active_mask
        n_src_active = int(src_active_mask.sum())
        n_src_pauses = int(src_pause_mask.sum())
        n_out_active_on_src = int((src_active_mask & (out_w > out_active_thresh_db)).sum())
        coverage_ratio = round(n_out_active_on_src / max(1, n_src_active), 4)

        # Median active-window gain offset (normalizes loudnorm gain difference without masking dropouts)
        if n_src_active > 0 and n_out_active_on_src > 0:
            both_active = src_active_mask & (out_w > out_active_thresh_db)
            gain_offset_db = float(np.median(out_w[both_active] - src_w[both_active]))
        else:
            gain_offset_db = 0.0

        dropout_windows = []
        for idx_w in range(len(src_wins)):
            sw_db, ow_db = src_wins[idx_w], out_wins[idx_w]
            if sw_db > dropout_src_thresh_db:
                rel_drop = (ow_db - gain_offset_db) - sw_db
                if ow_db < dropout_out_thresh_db or rel_drop < -20.0:
                    dropout_windows.append({
                        "t_local_s": win_starts[idx_w],
                        "src_db": sw_db,
                        "out_db": ow_db,
                        "rel_drop_db": round(rel_drop, 2),
                    })

        # Envelope Pearson correlation (clipped at -75 dBFS so PCM dither floor doesn't dominate)
        sc = np.clip(src_w, -75.0, 0.0)
        oc = np.clip(out_w, -75.0, 0.0)
        if np.std(sc) > 1e-6 and np.std(oc) > 1e-6:
            env_corr = round(float(np.corrcoef(sc, oc)[0, 1]), 4)
        else:
            env_corr = 0.0

        # Word-interval check against locked source words
        seg_words = [w for w in words if w["seg_idx"] == si]
        missing_words = []
        active_src_words = 0
        for w in seg_words:
            ws0 = int(round(w["src_start"] * SR))
            ws1 = max(ws0 + 1, int(round(w["src_end"] * SR)))
            wo0 = int(round(w["s"] * SR))
            wo1 = max(wo0 + 1, min(len(out), int(round(w["e"] * SR))))
            w_src_db = rms_dbfs(src[ws0:ws1])
            w_out_db = rms_dbfs(out[wo0:wo1])
            if w_src_db > -42.0:
                active_src_words += 1
                if w_out_db < -50.0:
                    missing_words.append({
                        "word": w["w"],
                        "t_local_s": w["s"],
                        "src_db": w_src_db,
                        "out_db": w_out_db,
                    })

        seg_ok = (
            n_src_active > 0
            and coverage_ratio >= 0.98
            and len(dropout_windows) == 0
            and len(missing_words) == 0
            and env_corr >= 0.90
            and out_seg_db > -30.0
        )
        if not seg_ok:
            failures.append(
                f"S{si + 1} (src {a:.3f}-{b:.3f}s -> local {local:.3f}-{local + sl['dur']:.3f}s): "
                f"coverage={coverage_ratio:.1%}, dropouts={len(dropout_windows)}, "
                f"missing_words={len(missing_words)}/{active_src_words}, corr={env_corr:.4f}, out_rms={out_seg_db} dBFS"
            )

        segments_report.append({
            "segment": f"S{si + 1}",
            "nonzero_source_offset": sl["nonzero_source_offset"],
            "src_start_s": a,
            "src_end_s": b,
            "local_start_s": local,
            "local_end_s": round(local + sl["dur"], 3),
            "src_rms_dbfs": src_seg_db,
            "out_rms_dbfs": out_seg_db,
            "out_peak": out_seg_peak,
            "windows_total": len(src_wins),
            "src_active_windows": n_src_active,
            "src_genuine_pause_windows": n_src_pauses,
            "out_active_on_src_active": n_out_active_on_src,
            "speech_coverage_ratio": coverage_ratio,
            "unexpected_dropout_count": len(dropout_windows),
            "unexpected_dropouts_sample": dropout_windows[:6],
            "active_source_words": active_src_words,
            "missing_word_count": len(missing_words),
            "missing_words_sample": missing_words[:10],
            "envelope_corr": env_corr,
            "passed": seg_ok,
        })

    # 1-second RMS table across entire 31 s file (for clear report evidence)
    per_sec = []
    n_secs = int(math.ceil(len(out) / SR))
    for sec in range(n_secs):
        chunk = out[sec * SR:min(len(out), (sec + 1) * SR)]
        per_sec.append({
            "sec": sec,
            "rms_dbfs": rms_dbfs(chunk),
            "peak": peak_abs(chunk),
        })

    return {
        "label": label,
        "out_vo_wav": str(out_vo_wav),
        "src_vo_wav": str(src_vo_wav),
        "pcm16_1lsb_dither_dbfs": PCM16_LSB_DBFS,
        "passed": len(failures) == 0,
        "failures": failures,
        "segments": segments_report,
        "per_second_rms": per_sec,
    }


def build_audio(work: Path, slices: list[dict], total: float) -> dict:
    parts = []
    cursor = 0.0
    for i, sl in enumerate(slices):
        gap_n = int(round((sl["local"] - cursor) * SR))
        if gap_n > 0:
            parts.append(silence(gap_n))
        seg = sl["b"] - sl["a"]
        target_n = int(round(seg * SR))
        p = work / f"vo_{i}.wav"
        # FIXED: atrim + asetpts=PTS-STARTPTS strictly BEFORE afade so nonzero-offset slices keep 100% speech
        af = (
            f"atrim=start={sl['a']:.3f}:end={sl['b']:.3f},"
            f"asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d=0.008,"
            f"afade=t=out:st={max(0.0, seg - 0.008):.3f}:d=0.008"
        )
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(VO_WAV),
            "-af", af,
            "-ar", str(SR), "-ac", "2", str(p),
        ])
        seg_arr = read_wav(p)
        if abs(len(seg_arr) - target_n) > 8:
            raise RuntimeError(f"Segment {i} length mismatch: got {len(seg_arr)} samples vs expected {target_n}")
        if len(seg_arr) < target_n:
            seg_arr = np.concatenate([seg_arr, silence(target_n - len(seg_arr))], axis=0)
        seg_arr = seg_arr[:target_n]
        parts.append(seg_arr)
        cursor = sl["local"] + seg

    vo = np.concatenate(parts, axis=0)
    n = int(round(total * SR))
    if len(vo) < n:
        vo = np.concatenate([vo, silence(n - len(vo))], axis=0)
    vo = vo[:n]
    raw = work / "stem_vo_raw.wav"
    write_wav(vo, raw)

    vo_wav = work / "stem_vo.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(vo_wav),
    ])
    vo_norm = read_wav(vo_wav)[:n]
    if len(vo_norm) < n:
        vo_norm = np.pad(vo_norm, ((0, n - len(vo_norm)), (0, 0)))
    write_wav(vo_norm, vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)

    bed_raw = work / "stem_bed_raw.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "0.0", "-t", f"{total:.3f}",
        "-i", str(BED_MP3),
        "-af", f"afade=t=in:d=0.10,afade=t=out:st={total - 0.30:.3f}:d=0.30",
        "-ar", str(SR), "-ac", "2", str(bed_raw),
    ])
    bed = read_wav(bed_raw)[:n]
    if len(bed) < n:
        bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))
    _, bi0 = sfx_kit.ebur128(bed_raw)
    bed *= 10 ** (((vo_i - 16.0) - bi0) / 20)
    bed_wav = work / "stem_bed.wav"
    write_wav(bed, bed_wav)
    T = np.arange(n) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k = int(0.35 * SR)
    for _ in range(10):
        bm, _bi = sfx_kit.ebur128(bed_wav)
        m = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:m])
        delta = vo_m_arr[:m] - bm_arr
        short = np.where(speaking[:m], np.clip(12.5 - delta, 0, None), 0)
        pause = np.where(~speaking[:m], np.clip(bm_arr - (vo_i - 12.5), 0, None), 0)
        need = np.maximum(short, pause)
        if not (delta[speaking[:m]] < 10.5).any() and not (bm_arr[~speaking[:m]] > vo_i - 11).any():
            break
        held = np.array([need[max(0, idx - 3):min(m, idx + 4)].max() for idx in range(m)])
        duck[:m] = np.minimum(duck[:m] + held, 20)
        env = np.convolve(np.interp(T, grid, duck, left=0, right=0), np.ones(k) / k, mode="same")
        write_wav(bed * (10 ** (-env / 20))[:, None], bed_wav)

    hits = [
        ("whoosh", 0.00, -6.0),
        ("rumble", 0.20, -10.5),
        ("tick", TITLE_IN, -8.5),
        ("tick", 14.08, -8.5),
        ("tick", 20.04, -8.5),
        ("tick", TEACH_IN, -8.5),
    ]
    sfx = np.zeros((n, 2), dtype=np.float32)
    kit = {
        "whoosh": KIT_DIR / "sfx_owb_whoosh_soft_v01.wav",
        "tick": KIT_DIR / "sfx_owb_tick_ui_v01.wav",
        "rumble": KIT_DIR / "sfx_owb_rumble_low_v01.wav",
    }
    for kind, at, gain in hits:
        sample = read_wav(kit[kind]) * (10 ** (gain / 20))
        i0 = int(round(at * SR))
        i1 = min(n, i0 + len(sample))
        if i1 > i0:
            sfx[i0:i1] += sample[:i1 - i0]
    sfx_wav = work / "stem_sfx.wav"
    write_wav(sfx, sfx_wav)
    _sm, si = sfx_kit.ebur128(sfx_wav)
    if si > vo_i - 22:
        sfx *= 10 ** ((vo_i - 22 - si) / 20)
        write_wav(sfx, sfx_wav)
    for _ in range(8):
        sm, _si = sfx_kit.ebur128(sfx_wav)
        m = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:m])
        over = np.where(~speaking[:m], sm_arr - (vo_i - 8), 0)
        under = np.where(speaking[:m], 12.5 - (vo_m_arr[:m] - sm_arr), 0)
        worst = max(float(over.max()), float(under.max()))
        if worst <= 0:
            break
        sfx *= 10 ** (-(worst + 1) / 20)
        write_wav(sfx, sfx_wav)

    mix_raw = work / "mix_raw.wav"
    write_wav(read_wav(vo_wav)[:n] + read_wav(bed_wav)[:n] + sfx[:n], mix_raw)
    mix = work / "mix.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(mix_raw),
        "-af", "loudnorm=I=-14:TP=-2.2:LRA=11",
        "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(mix),
    ])
    _, mix_i = sfx_kit.ebur128(mix)
    _, bed_i = sfx_kit.ebur128(bed_wav)
    _, sfx_i = sfx_kit.ebur128(sfx_wav)
    return {
        "vo_lufs": round(vo_i, 2),
        "bed_lufs": round(bed_i, 2),
        "sfx_lufs": round(sfx_i, 2),
        "mix_lufs": round(mix_i, 2),
    }


def calibrate_aac_wav(work: Path, src_wav: Path, total: float) -> tuple[Path, float, float]:
    gain_db = 0.0
    limit_db = -2.25
    cal_wav = work / "mix_cal.wav"
    test_m4a = work / "mix_cal_test.m4a"
    i_lufs, tp = -14.0, -2.0
    for it in range(8):
        af = (
            f"aresample=192000,volume={gain_db:.3f}dB,"
            f"alimiter=limit={limit_db:.2f}dB:level=disabled:attack=5:release=50,"
            "aresample=48000"
        )
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(src_wav),
            "-af", af, "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(cal_wav),
        ])
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(cal_wav),
            "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-t", f"{total:.3f}", str(test_m4a),
        ])
        m_i, m_tp = gso.aac_loudness(test_m4a)
        if m_i is not None and m_tp is not None:
            i_lufs, tp = m_i, m_tp
        print(f"  aac cal iter {it}: gain={gain_db:+.2f}dB limit={limit_db:.2f}dB -> I={i_lufs:.2f} LUFS, TP={tp:.2f} dBTP", flush=True)
        if -14.15 <= i_lufs <= -13.85 and tp <= -1.85:
            break
        gain_db += (-14.0 - i_lufs)
        if tp > -1.85:
            limit_db -= max(0.15, tp - (-2.0))
    return cal_wav, round(i_lufs, 2), round(tp, 2)


def verify_video_stream_equivalence(v02_mp4: Path, v03_mp4: Path) -> dict:
    """Verify exact video stream equivalence (encoded streamhash + decoded framemd5 across all 738 frames)."""
    sh_v02 = sp.check_output([
        "ffmpeg", "-v", "error", "-i", str(v02_mp4), "-map", "0:v:0", "-c", "copy", "-f", "streamhash", "-"
    ], text=True).strip()
    sh_v03 = sp.check_output([
        "ffmpeg", "-v", "error", "-i", str(v03_mp4), "-map", "0:v:0", "-c", "copy", "-f", "streamhash", "-"
    ], text=True).strip()
    if sh_v02 != sh_v03:
        raise RuntimeError(f"Encoded video streamhash mismatch: v02={sh_v02} vs v03={sh_v03}")

    fm_v02 = sp.check_output([
        "ffmpeg", "-v", "error", "-i", str(v02_mp4), "-map", "0:v:0", "-f", "framemd5", "-"
    ], text=True)
    fm_v03 = sp.check_output([
        "ffmpeg", "-v", "error", "-i", str(v03_mp4), "-map", "0:v:0", "-f", "framemd5", "-"
    ], text=True)
    frames_v02 = [ln for ln in fm_v02.splitlines() if ln and not ln.startswith("#")]
    frames_v03 = [ln for ln in fm_v03.splitlines() if ln and not ln.startswith("#")]
    if len(frames_v02) != TOTAL_FRAMES or frames_v02 != frames_v03:
        raise RuntimeError(
            f"Decoded video framemd5 mismatch: v02={len(frames_v02)} frames vs v03={len(frames_v03)} frames"
        )
    framemd5_sha = hashlib.sha256("\n".join(frames_v03).encode("utf-8")).hexdigest()
    return {
        "stream_copy_verified": True,
        "encoded_streamhash": sh_v03,
        "decoded_frames_count": len(frames_v03),
        "decoded_framemd5_sha256": framemd5_sha,
        "note": "Video stream reused unchanged from v02 strictly for audio repair per Chief ruling on J3918; NOT a visual/motion PASS.",
    }


def _norm_tokens(text: str) -> list[str]:
    """Normalize English/British/numeric ASR text to comparable lowercase word tokens."""
    t = text.lower().replace("’", "'").replace("—", " ").replace("–", " ").replace("-", " ")
    t = t.replace("°c", " degrees celsius").replace("°", " degrees ")
    t = re.sub(r"\b430\b", "four hundred and thirty", t)
    t = re.sub(r"\b58\b", "fifty eight", t)
    t = re.sub(r"\b180\b", "one hundred and eighty", t)
    t = re.sub(r"\b1965\b", "nineteen sixty five", t)
    t = re.sub(r"\b7\b", "seven", t)
    t = re.sub(r"\bkilometers\b", "kilometres", t)
    t = re.sub(r"\bcolumbus\b", "colombo", t)
    t = re.sub(r"[^a-z0-9'\s]", " ", t)
    return [tok for tok in t.split() if tok]


def verify_asr_speech(
    work: Path,
    v03_mp4: Path,
    v03_vo_wav: Path,
    v02_mp4: Path,
    expected_words: list[dict],
) -> dict:
    """Decode audio freshly from v03.mp4, v03_vo.wav, and v02.mp4 and run local faster-whisper ASR."""
    from faster_whisper import WhisperModel  # type: ignore
    from difflib import SequenceMatcher

    model = WhisperModel("small.en", device="cpu", compute_type="int8", local_files_only=True)
    expected_text = " ".join(w["w"] for w in expected_words)
    exp_tokens = _norm_tokens(expected_text)

    def run_one(media_path: Path, tag: str) -> dict:
        dec_wav = work / f"asr_decoded_{tag}.wav"
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(media_path),
            "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dec_wav),
        ])
        with wave.open(str(dec_wav)) as wf:
            assert wf.getframerate() == 16000 and wf.getnchannels() == 1 and wf.getsampwidth() == 2
            audio_np = np.frombuffer(wf.readframes(wf.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        segs_iter, info = model.transcribe(
            audio_np,
            language="en",
            beam_size=5,
            word_timestamps=True,
            vad_filter=False,
        )
        segs = list(segs_iter)
        asr_words = []
        for seg in segs:
            for w in (seg.words or []):
                asr_words.append({
                    "word": w.word.strip(),
                    "start": round(float(w.start), 3),
                    "end": round(float(w.end), 3),
                    "prob": round(float(w.probability), 3),
                })
        full_text = " ".join(s.text.strip() for s in segs).strip()
        got_tokens = _norm_tokens(full_text)
        sm = SequenceMatcher(None, exp_tokens, got_tokens)
        matched = sum(b.size for b in sm.get_matching_blocks())
        ratio = round(matched / max(1, len(exp_tokens)), 4)
        missing = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op in ("delete", "replace"):
                missing.append({
                    "op": op,
                    "expected": exp_tokens[i1:i2],
                    "got": got_tokens[j1:j2],
                })
        return {
            "source": str(media_path),
            "decoded_wav_sha256": sha256(dec_wav),
            "duration_s": round(float(info.duration), 3),
            "transcript": full_text,
            "asr_word_count": len(asr_words),
            "expected_normalized_tokens": len(exp_tokens),
            "matched_normalized_tokens": matched,
            "token_recall": ratio,
            "diffs": missing,
            "first_word_start_s": asr_words[0]["start"] if asr_words else None,
            "last_word_end_s": asr_words[-1]["end"] if asr_words else None,
            "words": asr_words,
        }

    res_v03_mp4 = run_one(v03_mp4, "v03_mp4")
    res_v03_vo = run_one(v03_vo_wav, "v03_vo")
    res_v02_mp4 = run_one(v02_mp4, "v02_mp4")

    if res_v03_mp4["token_recall"] < 0.95 or res_v03_vo["token_recall"] < 0.95:
        raise RuntimeError(
            f"Fresh ASR verification failed on v03: mp4_recall={res_v03_mp4['token_recall']}, "
            f"vo_recall={res_v03_vo['token_recall']}, diffs={res_v03_mp4['diffs']}"
        )
    if res_v02_mp4["token_recall"] >= 0.50:
        raise RuntimeError(f"Expected old v02.mp4 ASR to fail, got recall={res_v02_mp4['token_recall']}")

    return {
        "model": "faster-whisper small.en (local_files_only=True, int8 CPU)",
        "expected_word_count": len(expected_words),
        "expected_text": expected_text,
        "v03_mp4": res_v03_mp4,
        "v03_vo_wav": res_v03_vo,
        "v02_mp4_contrast": {
            "transcript": res_v02_mp4["transcript"],
            "asr_word_count": res_v02_mp4["asr_word_count"],
            "token_recall": res_v02_mp4["token_recall"],
            "last_word_end_s": res_v02_mp4["last_word_end_s"],
        },
        "note": "Automated fresh-decode ASR verification only; actual human/capable-agent listening is delegated to dependent QA job J3923.",
    }


def canonical_13_other_mp3_beds() -> list[Path]:
    beds = []
    for p in sorted(NAS_ROOT.glob("*/05_Music/*.mp3")):
        if p.name.startswith("._"):
            continue
        if "064_" in str(p):
            continue
        beds.append(p)
    return beds


def copy_verified(src: Path, dst: Path) -> None:
    if dst.exists():
        raise SystemExit(f"Refusing to overwrite existing NAS file: {dst}")
    shutil.copy2(src, dst)
    if sha256(src) != sha256(dst):
        raise SystemExit(f"SHA-256 mismatch copying {src} -> {dst}")


def main() -> None:
    if (NAS_SUB_OUT / f"{STEM}.mp4").exists() or (NAS_SHORTS / f"{STEM}.mp4").exists():
        raise SystemExit(f"Target {STEM}.mp4 already exists on NAS; bump version.")

    # Verify all locked inputs and preserved prior versions BEFORE building
    for path, expected, label in (
        (VO_WAV, EXPECTED_VO_SHA256, "Locked VO WAV"),
        (BED_MP3, EXPECTED_BED_SHA256, "Locked Score Bed MP3"),
        (MASTER_V03, EXPECTED_MASTER_SHA256, "Locked Parent Master v03"),
        (V01_NAS_MP4, EXPECTED_V01_SHA256, "Preserved Short v01 MP4"),
        (V02_NAS_MP4, EXPECTED_V02_SHA256, "Preserved Short v02 MP4"),
        (V02_NAS_COVER, EXPECTED_V02_COVER_SHA256, "Preserved Short v02 Cover"),
    ):
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"{label} SHA-256 mismatch: {actual} != {expected}")
    print("Verified all 6 locked/preserved input SHA-256 hashes.", flush=True)

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    OUT_WORK = WORK / "exports"
    OUT_WORK.mkdir(parents=True)

    slices, words, last_word_end = build_voice_plan()
    joined = " ".join(w["w"] for w in words)
    assert len(words) == 71, f"Expected 71 spoken words, got {len(words)}"
    print(f"Voice plan: {len(words)} words across {len(slices)} segments | VO: {words[0]['s']:.3f}-{last_word_end:.3f} s", flush=True)

    cuts_meta = json.loads(V02_CUTS_GIT.read_text())
    pool_meta = json.loads(V02_POOL_GIT.read_text())
    v02_meta = json.loads(V02_META_GIT.read_text())
    v02_summary = json.loads(V02_SUMMARY_GIT.read_text())

    # Verify zero split words across all 11 cut boundaries
    for cut in cuts_meta[:-1]:
        cut_t = float(cut["timeline_out"])
        for w in words:
            if w["s"] + 0.005 < cut_t < w["e"] - 0.005:
                raise SystemExit(f"Cut at {cut_t:.3f}s ({cut['row']}) splits word {w['w']!r}")
    print(f"Verified 0 spoken words split across all {len(cuts_meta) - 1} cut boundaries.", flush=True)

    # 1. Build fixed audio (all 4 segments restored via atrim+asetpts before afade)
    aud = build_audio(WORK, slices, TOTAL_S)
    cal_wav, aac_i, aac_tp = calibrate_aac_wav(WORK, WORK / "mix.wav", TOTAL_S)
    aud["aac_lufs"] = aac_i
    aud["aac_tp_dbtp"] = aac_tp
    print("Audio levels:", json.dumps(aud), flush=True)

    # 2. Regression assertion: PROVE old v02 FAILS and repaired v03 PASSES
    reg_v02 = check_vo_speech_coverage(VO_WAV, V02_NAS_VO, slices, words, label="v02_broken")
    reg_v03 = check_vo_speech_coverage(VO_WAV, WORK / "stem_vo.wav", slices, words, label="v03_repaired")
    print(f"Regression check v02 passed={reg_v02['passed']} (expected False); failures={len(reg_v02['failures'])}", flush=True)
    for f_line in reg_v02["failures"]:
        print(f"  [v02 EXPECTED FAIL] {f_line}", flush=True)
    print(f"Regression check v03 passed={reg_v03['passed']} (expected True); failures={len(reg_v03['failures'])}", flush=True)
    if reg_v02["passed"]:
        raise SystemExit("REGRESSION TEST INVALID: old v02 VO stem unexpectedly passed coverage check!")
    if not reg_v03["passed"]:
        raise SystemExit(f"REPAIRED v03 VO stem failed speech coverage check: {reg_v03['failures']}")

    # 3. Mux v03 reusing v02 video stream (-c:v copy) with repaired calibrated AAC audio
    final_mp4 = OUT_WORK / f"{STEM}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(V02_NAS_MP4),
        "-i", str(cal_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2",
        "-movflags", "+faststart",
        "-t", f"{TOTAL_S:.3f}",
        str(final_mp4),
    ])

    # 4. Verify video stream equivalence & playback health
    vid_equiv = verify_video_stream_equivalence(V02_NAS_MP4, final_mp4)
    print("Video stream equivalence verified:", json.dumps(vid_equiv), flush=True)
    health_local = cfr.assess_playback_health(cfr.probe_json(final_mp4))
    if not health_local.get("ok"):
        raise SystemExit(f"Playback health failed on local v03: {json.dumps(health_local, indent=2)}")

    # 5. Freshly decoded speech ASR verification (all 71 words) on v03.mp4 & v03_vo.wav (+ v02 contrast)
    vo_stem_out = OUT_WORK / f"{STEM}_vo.wav"
    sfx_stem_out = OUT_WORK / f"{STEM}_sfx.wav"
    bed_stem_out = OUT_WORK / f"{STEM}_bed.wav"
    shutil.copy2(WORK / "stem_vo.wav", vo_stem_out)
    shutil.copy2(WORK / "stem_sfx.wav", sfx_stem_out)
    shutil.copy2(WORK / "stem_bed.wav", bed_stem_out)

    asr_report = verify_asr_speech(WORK, final_mp4, vo_stem_out, V02_NAS_MP4, words)
    print(
        f"Fresh ASR check PASS: v03.mp4 recall={asr_report['v03_mp4']['token_recall']} "
        f"({asr_report['v03_mp4']['matched_normalized_tokens']}/{asr_report['v03_mp4']['expected_normalized_tokens']}), "
        f"v03_vo recall={asr_report['v03_vo_wav']['token_recall']}, "
        f"v02 contrast recall={asr_report['v02_mp4_contrast']['token_recall']}",
        flush=True,
    )

    # 6. Write sidecars, stills, contact sheet
    words_clean = [{k: w[k] for k in ("text", "w", "s", "e", "start", "end")} for w in words]
    words_path = OUT_WORK / f"{STEM}_words.json"
    transcript_path = OUT_WORK / f"{STEM}_transcript.txt"
    srt_path = OUT_WORK / f"{STEM}_en-GB.srt"
    cuts_path = OUT_WORK / f"{STEM}_cuts.json"
    pool_path = OUT_WORK / f"{STEM}_pool.json"
    meta_path = OUT_WORK / f"{STEM}_meta.json"
    reg_path = OUT_WORK / f"{STEM}_vo_coverage_regression.json"
    asr_path = OUT_WORK / f"{STEM}_asr_verify.json"

    words_path.write_text(json.dumps(words_clean, indent=2) + "\n")
    transcript_path.write_text(joined + "\n")
    write_srt(srt_chunks_full(words_clean, last_word_end), srt_path)
    cuts_path.write_text(json.dumps(cuts_meta, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_meta, indent=2) + "\n")
    reg_path.write_text(json.dumps({"v02_broken": reg_v02, "v03_repaired": reg_v03}, indent=2) + "\n")
    asr_path.write_text(json.dumps(asr_report, indent=2) + "\n")

    frame0_jpg = OUT_WORK / f"{STEM}_frame0.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.00", "-i", str(final_mp4), "-frames:v", "1", "-q:v", "2", str(frame0_jpg)])
    cover_jpg = OUT_WORK / f"{STEM}_cover.jpg"
    shutil.copy2(V02_NAS_COVER, cover_jpg)
    assert sha256(cover_jpg) == EXPECTED_V02_COVER_SHA256

    # 12-shot midpoint inspection contact sheet from v03.mp4
    shot_tiles = []
    for idx, cut in enumerate(cuts_meta):
        mid_t = round((float(cut["timeline_in"]) + float(cut["timeline_out"])) / 2.0, 2)
        raw_t = sp.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{mid_t:.2f}", "-i", str(final_mp4),
            "-frames:v", "1", "-vf", "scale=360:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        im_t = Image.frombytes("RGB", (360, 640), raw_t)
        d_t = ImageDraw.Draw(im_t)
        d_t.rectangle((0, 0, 360, 32), fill=(0, 0, 0))
        d_t.text((8, 8), f"{idx + 1:02d} {cut['row']} ({mid_t:.1f}s)", fill=(255, 255, 255))
        shot_tiles.append(im_t)
    cols_s = 4
    rows_s = (len(shot_tiles) + cols_s - 1) // cols_s
    sheet_12 = Image.new("RGB", (360 * cols_s, 640 * rows_s), (18, 22, 30))
    for idx, im_t in enumerate(shot_tiles):
        sheet_12.paste(im_t, ((idx % cols_s) * 360, (idx // cols_s) * 640))
    sheet_12_path = OUT_WORK / f"{STEM}_review_12shots.jpg"
    sheet_12.save(sheet_12_path, quality=92)

    meta_obj = {
        "slug": SHORT_SLUG,
        "stem": STEM,
        "title": SHORT_TITLE,
        "alt_title": ALT_TITLE,
        "air_date": AIR_DATE,
        "test_a": True,
        "relatedVideoId": None,
        "parent_long_film": "OWB:064",
        "parent_long_title": LONG_TITLE,
        "parent_master_v03_sha256": EXPECTED_MASTER_SHA256,
        "repaired_from_v02_sha256": EXPECTED_V02_SHA256,
        "video_stream_equivalence": vid_equiv,
        "spoken": joined,
        "vo_onset_s": words_clean[0]["s"],
        "last_word_end_s": last_word_end,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "hook": v02_meta["hook"],
        "hook_caption": v02_meta["hook_caption"],
        "title_banner": v02_meta["title_banner"],
        "teach_overlay": v02_meta["teach_overlay"],
        "end_card": v02_meta["end_card"],
        "words_file": str(words_path),
        "vo": str(vo_stem_out),
        "audio": aud,
    }
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    # 7. Run all 7 gates + canonical 13-bed MP3 music gate locally first
    g_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK])
    g_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", final_mp4, "--air-date", AIR_DATE, "--sheet-dir", OUT_WORK, "--json"])
    (OUT_WORK / f"{STEM}_gate.txt").write_text((g_txt.stdout or "") + (g_txt.stderr or ""))
    (OUT_WORK / f"{STEM}_gate.json").write_text(g_json.stdout or g_json.stderr)
    print(g_txt.stdout, end="", flush=True)

    tp_f0 = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", frame0_jpg, "--out", OUT_WORK / f"{STEM}_frame0_preview.jpg", "--score"])
    tp_cov = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py", "short", cover_jpg, "--out", OUT_WORK / f"{STEM}_cover_preview.jpg", "--score"])
    (OUT_WORK / f"{STEM}_thumb_score.txt").write_text((tp_f0.stdout or "") + (tp_cov.stdout or ""))
    print(tp_f0.stdout, end="", flush=True)
    print(tp_cov.stdout, end="", flush=True)

    sfx_res = run_gate([
        sys.executable, REPO / "scripts/sfx_kit.py", "level",
        "--vo", vo_stem_out, "--sfx", sfx_stem_out, "--bed", bed_stem_out,
        "--minutes", f"{TOTAL_S / 60:.3f}",
        "--out", OUT_WORK / f"{STEM}_sfx_level.json",
    ])
    (OUT_WORK / f"{STEM}_sfx.txt").write_text((sfx_res.stdout or "") + (sfx_res.stderr or ""))
    print(sfx_res.stdout, end="", flush=True)

    mg_res = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", final_mp4,
        "--out", OUT_WORK / f"{STEM}_music_gate.json",
    ])
    (OUT_WORK / f"{STEM}_music_gate.txt").write_text((mg_res.stdout or "") + (mg_res.stderr or ""))
    print(mg_res.stdout, end="", flush=True)

    other_beds = canonical_13_other_mp3_beds()
    assert len(other_beds) == 13, f"Expected 13 other canonical MP3 beds on NAS, found {len(other_beds)}: {other_beds}"
    mg_canon = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", final_mp4,
        "--others", *other_beds,
        "--out", OUT_WORK / f"{STEM}_music_gate_canonical_mp3.json",
    ])
    (OUT_WORK / f"{STEM}_music_gate_canonical_mp3.txt").write_text((mg_canon.stdout or "") + (mg_canon.stderr or ""))
    print("CANONICAL 13-BED MP3:", mg_canon.stdout, end="", flush=True)

    pg_res = run_gate([
        sys.executable, REPO / "scripts/polish_gate.py", final_mp4,
        "--cuts", cuts_path,
        "--out", OUT_WORK / f"{STEM}_polish_gate.json",
    ])
    (OUT_WORK / f"{STEM}_polish_gate.txt").write_text((pg_res.stdout or "") + (pg_res.stderr or ""))
    print(pg_res.stdout, end="", flush=True)

    pqa_dir = OUT_WORK / f"{STEM}_picture_qa"
    pqa_res = run_gate([
        sys.executable, REPO / "scripts/picture_qa.py", final_mp4,
        "--cuts", cuts_path, "--pool", pool_path, "--out-dir", pqa_dir,
    ])
    (OUT_WORK / f"{STEM}_picture_qa.txt").write_text((pqa_res.stdout or "") + (pqa_res.stderr or ""))
    print(pqa_res.stdout, end="", flush=True)

    gates = {
        "gate_shorts_open_rc": g_txt.returncode,
        "thumb_preview_frame0_rc": tp_f0.returncode,
        "thumb_preview_cover_rc": tp_cov.returncode,
        "sfx_level_rc": sfx_res.returncode,
        "music_gate_rc": mg_res.returncode,
        "music_gate_canonical_13mp3_rc": mg_canon.returncode,
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
        "playback_health_ok": bool(health_local.get("ok")),
    }
    print("LOCAL GATES:", json.dumps(gates, indent=2), flush=True)
    if any(v != 0 for k, v in gates.items() if k.endswith("_rc")) or not gates["playback_health_ok"]:
        raise SystemExit(1)

    # Update meta_obj paths to canonical NAS paths before checksum-copying to NAS
    nas_vo_future = NAS_SUB_OUT / f"{STEM}_vo.wav"
    nas_words_future = NAS_SUB_OUT / f"{STEM}_words.json"
    meta_obj["words_file"] = str(nas_words_future)
    meta_obj["vo"] = str(nas_vo_future)
    meta_path.write_text(json.dumps(meta_obj, indent=2) + "\n")

    cover_info = dict(v02_summary["cover"])
    cover_info["file"] = str(NAS_SUB_OUT / f"{STEM}_cover.jpg")

    open_sheet_path = OUT_WORK / f"{STEM}_open_sheet.jpg"
    summary = {
        "stem": STEM,
        "mp4_path": str(NAS_SUB_OUT / f"{STEM}.mp4"),
        "mp4_sha256": sha256(final_mp4),
        "vo_stem_sha256": sha256(vo_stem_out),
        "bed_stem_sha256": sha256(bed_stem_out),
        "sfx_stem_sha256": sha256(sfx_stem_out),
        "srt_sha256": sha256(srt_path),
        "frame0_jpg_sha256": sha256(frame0_jpg),
        "cover_jpg_sha256": sha256(cover_jpg),
        "open_sheet_sha256": sha256(open_sheet_path),
        "review_12shots_sha256": sha256(sheet_12_path),
        "master_v03_sha256": EXPECTED_MASTER_SHA256,
        "locked_vo_sha256": EXPECTED_VO_SHA256,
        "locked_bed_sha256": EXPECTED_BED_SHA256,
        "preserved_v01_mp4_sha256": EXPECTED_V01_SHA256,
        "preserved_v02_mp4_sha256": EXPECTED_V02_SHA256,
        "video_stream_equivalence": vid_equiv,
        "duration_s": TOTAL_S,
        "fps": FPS,
        "frames": TOTAL_FRAMES,
        "words_count": len(words_clean),
        "vo_onset_s": words_clean[0]["s"],
        "s01_s02_breath_s": round(words_clean[16]["s"] - words_clean[15]["e"], 3),
        "last_word_end_s": last_word_end,
        "tail_gap_s": round(TOTAL_S - last_word_end, 3),
        "cut1_s": v02_summary["cut1_s"],
        "cut2_s": v02_summary["cut2_s"],
        "max_shot_s": v02_summary["max_shot_s"],
        "audio": aud,
        "vo_coverage_regression": {
            "v02_broken_passed": reg_v02["passed"],
            "v03_repaired_passed": reg_v03["passed"],
            "v03_segments": [
                {
                    "segment": s["segment"],
                    "src_start_s": s["src_start_s"],
                    "out_rms_dbfs": s["out_rms_dbfs"],
                    "speech_coverage_ratio": s["speech_coverage_ratio"],
                    "unexpected_dropout_count": s["unexpected_dropout_count"],
                    "missing_word_count": s["missing_word_count"],
                    "envelope_corr": s["envelope_corr"],
                }
                for s in reg_v03["segments"]
            ],
        },
        "asr_verify": {
            "model": asr_report["model"],
            "v03_mp4_token_recall": asr_report["v03_mp4"]["token_recall"],
            "v03_mp4_matched": f"{asr_report['v03_mp4']['matched_normalized_tokens']}/{asr_report['v03_mp4']['expected_normalized_tokens']}",
            "v03_vo_token_recall": asr_report["v03_vo_wav"]["token_recall"],
            "v02_contrast_token_recall": asr_report["v02_mp4_contrast"]["token_recall"],
        },
        "hook": v02_summary["hook"],
        "title": v02_summary["title"],
        "teach": v02_summary["teach"],
        "end_card": v02_summary["end_card"],
        "cover": cover_info,
        "gates": gates,
    }
    summary_path = OUT_WORK / f"{STEM}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    # 8. Checksum-copy all verified v03 outputs to NAS_SUB_OUT (preserving v01/v02 untouched)
    NAS_SUB_OUT.mkdir(parents=True, exist_ok=True)
    for item in sorted(OUT_WORK.iterdir()):
        if item.is_dir():
            dst_dir = NAS_SUB_OUT / item.name
            dst_dir.mkdir(parents=True, exist_ok=True)
            for sub in sorted(item.iterdir()):
                if sub.is_file():
                    copy_verified(sub, dst_dir / sub.name)
        elif item.is_file():
            copy_verified(item, NAS_SUB_OUT / item.name)

    # 9. Re-run canonical NAS gates directly on NAS v03 master & stems so all reports record NAS paths
    nas_mp4 = NAS_SUB_OUT / f"{STEM}.mp4"
    nas_vo = NAS_SUB_OUT / f"{STEM}_vo.wav"
    nas_sfx = NAS_SUB_OUT / f"{STEM}_sfx.wav"
    nas_bed = NAS_SUB_OUT / f"{STEM}_bed.wav"
    nas_cuts = NAS_SUB_OUT / f"{STEM}_cuts.json"
    nas_pool = NAS_SUB_OUT / f"{STEM}_pool.json"

    g_nas_txt = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", nas_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT])
    g_nas_json = run_gate([sys.executable, REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", nas_mp4, "--air-date", AIR_DATE, "--sheet-dir", NAS_SUB_OUT, "--json"])
    if g_nas_txt.returncode != 0:
        raise SystemExit(f"NAS gate_shorts_open failed: {g_nas_txt.stdout}\n{g_nas_txt.stderr}")
    (NAS_SUB_OUT / f"{STEM}_gate.txt").write_text((g_nas_txt.stdout or "") + (g_nas_txt.stderr or ""))
    (NAS_SUB_OUT / f"{STEM}_gate.json").write_text(g_nas_json.stdout or g_nas_json.stderr)

    sfx_nas = run_gate([
        sys.executable, REPO / "scripts/sfx_kit.py", "level",
        "--vo", nas_vo, "--sfx", nas_sfx, "--bed", nas_bed,
        "--minutes", f"{TOTAL_S / 60:.3f}",
        "--out", NAS_SUB_OUT / f"{STEM}_sfx_level.json",
    ])
    if sfx_nas.returncode != 0:
        raise SystemExit(f"NAS sfx_kit level failed: {sfx_nas.stdout}\n{sfx_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_sfx.txt").write_text((sfx_nas.stdout or "") + (sfx_nas.stderr or ""))

    mg_nas = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", nas_mp4,
        "--out", NAS_SUB_OUT / f"{STEM}_music_gate.json",
    ])
    if mg_nas.returncode != 0:
        raise SystemExit(f"NAS music_gate failed: {mg_nas.stdout}\n{mg_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_music_gate.txt").write_text((mg_nas.stdout or "") + (mg_nas.stderr or ""))

    mg_nas_canon = run_gate([
        sys.executable, REPO / "scripts/music_gate.py", NAS_FILM,
        "--bed", BED_MP3, "--video", nas_mp4,
        "--others", *other_beds,
        "--out", NAS_SUB_OUT / f"{STEM}_music_gate_canonical_mp3.json",
    ])
    if mg_nas_canon.returncode != 0:
        raise SystemExit(f"NAS canonical 13-bed music_gate failed: {mg_nas_canon.stdout}\n{mg_nas_canon.stderr}")
    (NAS_SUB_OUT / f"{STEM}_music_gate_canonical_mp3.txt").write_text((mg_nas_canon.stdout or "") + (mg_nas_canon.stderr or ""))

    pg_nas = run_gate([
        sys.executable, REPO / "scripts/polish_gate.py", nas_mp4,
        "--cuts", nas_cuts, "--out", NAS_SUB_OUT / f"{STEM}_polish_gate.json",
    ])
    if pg_nas.returncode != 0:
        raise SystemExit(f"NAS polish_gate failed: {pg_nas.stdout}\n{pg_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_polish_gate.txt").write_text((pg_nas.stdout or "") + (pg_nas.stderr or ""))

    pqa_nas = run_gate([
        sys.executable, REPO / "scripts/picture_qa.py", nas_mp4,
        "--cuts", nas_cuts, "--pool", nas_pool, "--out-dir", NAS_SUB_OUT / f"{STEM}_picture_qa",
    ])
    if pqa_nas.returncode != 0:
        raise SystemExit(f"NAS picture_qa failed: {pqa_nas.stdout}\n{pqa_nas.stderr}")
    (NAS_SUB_OUT / f"{STEM}_picture_qa.txt").write_text((pqa_nas.stdout or "") + (pqa_nas.stderr or ""))

    health_nas = cfr.assess_playback_health(cfr.probe_json(nas_mp4))
    if not health_nas.get("ok"):
        raise SystemExit(f"NAS playback health failed: {json.dumps(health_nas, indent=2)}")
    (NAS_SUB_OUT / f"{STEM}_playback_health.json").write_text(json.dumps(health_nas, indent=2) + "\n")

    # Refresh summary with updated NAS open_sheet hash and playback health
    summary["open_sheet_sha256"] = sha256(NAS_SUB_OUT / f"{STEM}_open_sheet.jpg")
    summary["playback_health"] = health_nas
    (NAS_SUB_OUT / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    # 10. Mirror key v03 exports into NAS 10_Shorts/ root with SHA-256 verification
    for name in (
        f"{STEM}.mp4",
        f"{STEM}_frame0.jpg",
        f"{STEM}_cover.jpg",
        f"{STEM}_frame0_preview.jpg",
        f"{STEM}_cover_preview.jpg",
        f"{STEM}_open_sheet.jpg",
        f"{STEM}_review_12shots.jpg",
        f"{STEM}_meta.json",
        f"{STEM}_words.json",
        f"{STEM}_transcript.txt",
        f"{STEM}_cuts.json",
        f"{STEM}_pool.json",
        f"{STEM}_gate.txt",
        f"{STEM}_gate.json",
        f"{STEM}_summary.json",
        f"{STEM}_vo_coverage_regression.json",
        f"{STEM}_asr_verify.json",
    ):
        copy_verified(NAS_SUB_OUT / name, NAS_SHORTS / name)

    # 11. Re-verify preserved v01 and v02 NAS files remain bit-for-bit untouched
    assert sha256(V01_NAS_MP4) == EXPECTED_V01_SHA256, "v01.mp4 hash changed!"
    assert sha256(V02_NAS_MP4) == EXPECTED_V02_SHA256, "v02.mp4 hash changed!"
    print(f"NAS v03 verified by SHA-256: {nas_mp4} ({summary['mp4_sha256']})", flush=True)
    print("Confirmed preserved v01 and v02 NAS masters untouched.", flush=True)


if __name__ == "__main__":
    main()
