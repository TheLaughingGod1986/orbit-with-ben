#!/usr/bin/env python3
import copy, hashlib, json, subprocess, wave
from pathlib import Path
import numpy as np

ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
OUT_ROOT = Path("/Users/benjaminoats/_desk/renders/J1100-v07")
NAS_OPENINGS = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-31/reviews_J1017/openings")

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()

# --- 1. S2 preparation ---
s2_key = "S2_027_emwQsPxnRGM"
s2_dir = OUT_ROOT / s2_key
s2_dir.mkdir(parents=True, exist_ok=True)
s2_prep = json.loads(Path("/Users/benjaminoats/_desk/renders/J1100-S2-raw03/S2_027_emwQsPxnRGM/locked_preparation.json").read_text())
s2_v = s2_prep["vo_splice_map"]
s2_pickup_path = ROOT / "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/J1100_s2_open_pickup_v01.wav"
s2_clause_path = s2_dir / "S2_because_swings_continuous.wav"
s2_body_path = Path(s2_v["vo_source_path"])

sp0_words = [
    {"word_idx": 1, "word": "Why", "src_start": 0.10, "src_end": 0.24},
    {"word_idx": 2, "word": "do", "src_start": 0.30, "src_end": 0.36},
    {"word_idx": 3, "word": "you", "src_start": 0.42, "src_end": 0.48},
    {"word_idx": 4, "word": "weigh", "src_start": 0.54, "src_end": 0.74},
    {"word_idx": 5, "word": "less", "src_start": 0.80, "src_end": 1.12},
    {"word_idx": 6, "word": "at", "src_start": 1.26, "src_end": 1.38},
    {"word_idx": 7, "word": "Earth's", "src_start": 1.44, "src_end": 1.66},
    {"word_idx": 8, "word": "equator?", "src_start": 1.70, "src_end": 2.28},
]
sp1_words = [
    {"word_idx": 9, "word": "You", "src_start": 2.72, "src_end": 2.80},
    {"word_idx": 10, "word": "weigh", "src_start": 2.84, "src_end": 2.98},
    {"word_idx": 11, "word": "about", "src_start": 3.08, "src_end": 3.36},
    {"word_idx": 12, "word": "half", "src_start": 3.44, "src_end": 3.70},
    {"word_idx": 13, "word": "a", "src_start": 3.76, "src_end": 3.82},
    {"word_idx": 14, "word": "percent", "src_start": 3.86, "src_end": 4.34},
    {"word_idx": 15, "word": "less", "src_start": 4.40, "src_end": 4.66},
    {"word_idx": 16, "word": "there.", "src_start": 4.74, "src_end": 4.92},
]
sp_clause_words = [
    {"word_idx": 351, "word": "Because", "src_start": 0.04, "src_end": 0.22},
    {"word_idx": 352, "word": "the", "src_start": 0.22, "src_end": 0.34},
    {"word_idx": 353, "word": "ground", "src_start": 0.34, "src_end": 0.56},
    {"word_idx": 354, "word": "at", "src_start": 0.56, "src_end": 0.76},
    {"word_idx": 355, "word": "the", "src_start": 0.76, "src_end": 0.86},
    {"word_idx": 356, "word": "equator", "src_start": 0.86, "src_end": 1.42},
    {"word_idx": 357, "word": "swings", "src_start": 1.49, "src_end": 1.86},
    {"word_idx": 358, "word": "round", "src_start": 1.90, "src_end": 2.12},
    {"word_idx": 359, "word": "so", "src_start": 2.22, "src_end": 2.42},
    {"word_idx": 360, "word": "fast,", "src_start": 2.48, "src_end": 2.96},
]

new_s2_spans = [
    {
        "span_index": 1,
        "source_wav": str(s2_pickup_path),
        "source_in": 0.06,
        "source_out": 2.40,
        "raw_dur": 2.34,
        "tempo": 1.0,
        "scaled_dur": 2.34,
        "gap_after": 0.65,
        "text": "Why do you weigh less at Earth's equator?",
        "words": sp0_words,
    },
    {
        "span_index": 2,
        "source_wav": str(s2_pickup_path),
        "source_in": 2.66,
        "source_out": 5.04,
        "raw_dur": 2.38,
        "tempo": 1.0,
        "scaled_dur": 2.38,
        "gap_after": 0.56,
        "text": "You weigh about half a percent less there.",
        "words": sp1_words,
    },
]
for sp in copy.deepcopy(s2_v["subspans"][10:19]):
    sp["source_wav"] = str(s2_body_path)
    if sp["words"][0]["word"] == "the" and sp["source_in"] == 4.04:
        sp["words"][0]["word"] = "The"
    if sp["words"][0]["word"] == "it" and sp["source_in"] == 10.92:
        sp["words"][0]["word"] = "It"
    if sp["words"][-1]["word"] == "airliner,":
        sp["words"][-1]["word"] = "airliner."
    new_s2_spans.append(sp)
new_s2_spans[-1]["gap_after"] = 0.28
new_s2_spans.append({
    "span_index": 12,
    "source_wav": str(s2_clause_path),
    "source_in": 0.00,
    "source_out": 2.96,
    "raw_dur": 2.96,
    "tempo": 1.0,
    "scaled_dur": 2.96,
    "gap_after": 0.26,
    "text": "Because the ground at the equator swings round so fast,",
    "words": sp_clause_words,
})
sp_last = copy.deepcopy(s2_v["subspans"][23])
sp_last["source_wav"] = str(s2_body_path)
new_s2_spans.append(sp_last)

now = 0.02
for idx, sp in enumerate(new_s2_spans):
    sp["span_index"] = idx + 1
    a, b = sp["source_in"], sp["source_out"]
    sp["timeline_start"] = round(now, 3)
    sp["timeline_end"] = round(now + (b - a), 3)
    for w in sp["words"]:
        w["start"] = round(now + w["src_start"] - a, 3)
        w["end"] = round(now + w["src_end"] - a, 3)
    now += (b - a) + sp.get("gap_after", 0.0)

s2_vo_wav = s2_dir / "S2_027_emwQsPxnRGM_v07_vo.wav"
s2_v["subspans"] = new_s2_spans
s2_v["vo_end_s"] = round(now, 3)
s2_v["total_duration_s"] = round(now + 1.0, 3)
s2_v["auditions"]["full_vo_audition"] = {"wav_path": str(s2_vo_wav), "sha256": sha(s2_vo_wav)}
s2_prep["hook_tokens"] = ["0.5%", "LIGHTER", "EQUATOR"]
(s2_dir / "locked_preparation.json").write_text(json.dumps(s2_prep, indent=2) + "\n")
(s2_dir / "locked_shots.json").write_text(json.dumps(s2_prep["shot_plan"], indent=2) + "\n")

# --- 2. S5 preparation ---
s5_key = "S5_028_jJ5LkFGyzLI"
s5_dir = OUT_ROOT / s5_key
s5_dir.mkdir(parents=True, exist_ok=True)
s5_prep = json.loads(Path("/Users/benjaminoats/_desk/renders/J1100-attempt03/S5_028_jJ5LkFGyzLI/locked_preparation.json").read_text())
s5_v = s5_prep["vo_splice_map"]
s5_pickup_path = ROOT / "02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/J1100_s5_open_pickup_v01.wav"
s5_body_path = ROOT / s5_v["vo_source_path"]

s5_sp0_words = [
    {"word_idx": 1, "word": "How", "src_start": 0.10, "src_end": 0.22},
    {"word_idx": 2, "word": "close", "src_start": 0.34, "src_end": 0.74},
    {"word_idx": 3, "word": "will", "src_start": 0.84, "src_end": 0.98},
    {"word_idx": 4, "word": "Gliese", "src_start": 1.08, "src_end": 1.42},
    {"word_idx": 5, "word": "710", "src_start": 2.00, "src_end": 2.54},
    {"word_idx": 6, "word": "come", "src_start": 2.84, "src_end": 3.16},
    {"word_idx": 7, "word": "to", "src_start": 3.26, "src_end": 3.36},
    {"word_idx": 8, "word": "the", "src_start": 3.40, "src_end": 3.46},
    {"word_idx": 9, "word": "Sun?", "src_start": 3.58, "src_end": 3.88},
]
s5_sp1_words = [
    {"word_idx": 487, "word": "The", "src_start": 196.08, "src_end": 196.16},
    {"word_idx": 488, "word": "star", "src_start": 196.24, "src_end": 196.46},
]
new_s5_spans = [
    {
        "span_index": 1,
        "source_wav": str(s5_pickup_path),
        "source_in": 0.06,
        "source_out": 3.90,
        "raw_dur": 3.84,
        "tempo": 1.0,
        "scaled_dur": 3.84,
        "gap_after": 0.24,
        "text": "How close will Gliese 710 come to the Sun?",
        "words": s5_sp0_words,
    },
    {
        "span_index": 2,
        "source_wav": str(s5_body_path),
        "source_in": 196.06,
        "source_out": 196.46,
        "raw_dur": 0.40,
        "tempo": 1.0,
        "scaled_dur": 0.40,
        "gap_after": 0.11,
        "text": "The star",
        "words": s5_sp1_words,
    },
]
for sp in copy.deepcopy(s5_v["subspans"][7:]):
    sp["source_wav"] = str(s5_body_path)
    new_s5_spans.append(sp)

now = 0.02
for idx, sp in enumerate(new_s5_spans):
    sp["span_index"] = idx + 1
    a, b = sp["source_in"], sp["source_out"]
    sp["timeline_start"] = round(now, 3)
    sp["timeline_end"] = round(now + (b - a), 3)
    for w in sp["words"]:
        w["start"] = round(now + w["src_start"] - a, 3)
        w["end"] = round(now + w["src_end"] - a, 3)
    now += (b - a) + sp.get("gap_after", 0.0)

delta_s5 = round(now - s5_v["vo_end_s"], 3)
s5_vo_wav = s5_dir / "S5_028_jJ5LkFGyzLI_v07_vo.wav"
s5_v["subspans"] = new_s5_spans
s5_v["vo_end_s"] = round(now, 3)
s5_v["total_duration_s"] = round(now + 1.0, 3)
s5_v["seventy_pct_mark_s"] = round(s5_v["total_duration_s"] * 0.7, 3)
s5_v["auditions"]["full_vo_audition"] = {"wav_path": str(s5_vo_wav), "sha256": sha(s5_vo_wav)}

for i, row in enumerate(s5_prep["shot_plan"]):
    if i > 1:
        row["timeline_in"] = round(row["timeline_in"] + delta_s5, 3)
    if i >= 1:
        row["timeline_out"] = round(row["timeline_out"] + delta_s5, 3)
    row["timeline_dur"] = round(row["timeline_out"] - row["timeline_in"], 3)
s5_prep["shot_plan"][1]["source_dur"] = s5_prep["shot_plan"][1]["timeline_dur"]
s5_prep["shot_plan"][1]["source_out"] = round(s5_prep["shot_plan"][1]["source_in"] + s5_prep["shot_plan"][1]["source_dur"], 3)
card = s5_prep["single_teaching_overlay"]
card["timeline_in"] = round(card["timeline_in"] + delta_s5, 3)
card["timeline_out"] = round(card["timeline_out"] + delta_s5, 3)
s5_prep["hook_tokens"] = ["HOW", "CLOSE", "SUN"]
(s5_dir / "locked_preparation.json").write_text(json.dumps(s5_prep, indent=2) + "\n")
(s5_dir / "locked_shots.json").write_text(json.dumps(s5_prep["shot_plan"], indent=2) + "\n")

# --- 3. S6 preparation ---
s6_key = "S6_028_X768qs8sNQs"
s6_dir = OUT_ROOT / s6_key
s6_dir.mkdir(parents=True, exist_ok=True)
s6_prep = json.loads(Path("/Users/benjaminoats/_desk/renders/J1100-S6-raw02/S6_028_X768qs8sNQs/locked_preparation.json").read_text())
s6_prep["hook_tokens"] = ["BRIGHTER", "THAN", "SIRIUS"]
(s6_dir / "locked_preparation.json").write_text(json.dumps(s6_prep, indent=2) + "\n")
(s6_dir / "locked_shots.json").write_text(json.dumps(s6_prep["shot_plan"], indent=2) + "\n")

for k, prep in [(s2_key, s2_prep), (s5_key, s5_prep), (s6_key, s6_prep)]:
    words = [w for sp in prep["vo_splice_map"]["subspans"] for w in sp["words"]]
    cuts = [r["timeline_out"] for r in prep["shot_plan"][:-1]]
    clipped = []
    for c in cuts:
        for w in words:
            if w["start"] + 0.02 < c < w["end"] - 0.02:
                clipped.append((c, w["word"], w["start"], w["end"]))
    print(f"{k}: vo_end={prep['vo_splice_map']['vo_end_s']}s total={prep['vo_splice_map']['total_duration_s']}s words={len(words)} clipped_cuts={clipped}")
