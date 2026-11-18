"""J2803 owned-bed validation. Reads studio-live music. Writes only this folder.

Records paths, hashes, prompts and labels before any similarity call. Then scores
the current production frames and the isolated J2795 candidate on the same pairs.
Does not edit scripts/music_gate.py, does not download audio, and does not spend.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import candidate  # noqa: E402
import music_gate as mg  # noqa: E402
import windows  # noqa: E402

HERE = Path(__file__).resolve().parent
OWB = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
HOS = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects")
BAR = mg.SIM_FAIL

# Labels below are checked against each plan's own prompt before measuring.
# A missing token drops that source out of the acceptance set rather than
# inventing a style from the audio.
SOURCES = [
    {
        "id": "hos009-wonder",
        "work": "HOS:009",
        "styles_expected": ["chamber", "drone"],
        "stationary": True,
        "positives": True,
        "audio": HOS / "009_The-Falling-Moon-Gravity/05_Music/hos_009_wonder_v01.mp3",
        "plan": HOS / "009_The-Falling-Moon-Gravity/05_Music/hos_009_wonder_v01_plan.json",
    },
    {
        "id": "hos006-trees",
        "work": "HOS:006",
        "styles_expected": ["chamber"],
        "stationary": False,
        "positives": True,
        "audio": HOS / "006_Trees-Are-Made-Of-Air/05_Music/trees006_score_bed_v01.mp3",
        "plan": HOS / "006_Trees-Are-Made-Of-Air/05_Music/trees006_score_bed_v01_plan.json",
    },
    {
        "id": "owb028-gliese",
        "work": "OWB:028",
        "styles_expected": ["ambient"],
        "stationary": False,
        "positives": True,
        "audio": OWB / "028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03.mp3",
        "plan": OWB / "028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03_plan.json",
    },
    {
        "id": "owb029-betelgeuse",
        "work": "OWB:029",
        "styles_expected": ["ambient"],
        "stationary": False,
        "positives": True,
        "audio": OWB / "029_Is-Betelgeuse-About-To-Explode/05_Music/betelgeuse_score_bed_v01.mp3",
        "plan": OWB / "029_Is-Betelgeuse-About-To-Explode/05_Music/betelgeuse_score_bed_v01_plan.json",
    },
    {
        "id": "owb031-magnetic",
        "work": "OWB:031",
        "styles_expected": ["drone"],
        "stationary": False,
        "positives": True,
        "audio": OWB / "031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.mp3",
        "plan": OWB / "031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01_plan.json",
        "note": "The plan names a geomagnetic drone in one chapter and a rhythmic pulse in others. Not a stationary-bed control.",
    },
    {
        "id": "hos009-teach",
        "work": "HOS:009",
        "styles_expected": ["chamber"],
        "stationary": False,
        "positives": False,
        "audio": HOS / "009_The-Falling-Moon-Gravity/05_Music/hos_009_teach_v01.mp3",
        "plan": HOS / "009_The-Falling-Moon-Gravity/05_Music/hos_009_teach_v01_plan.json",
        "note": "Second cue of the same HOS 009 score. Not an independent negative.",
    },
    {
        "id": "owb026-nearest",
        "work": "OWB:026",
        "styles_expected": [],
        "stationary": False,
        "positives": False,
        "audio": OWB / "026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.mp3",
        "plan": OWB / "026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full_plan.json",
        "note": "Own plan does not have to say ambient. Kept only for the written J01 reuse note.",
    },
    {
        "id": "owb-j01-linking",
        "work": "OWB:J01",
        "styles_expected": ["drone"],
        "stationary": False,
        "positives": False,
        "audio": OWB / "J01_Journey-To-Every-World/05_Music/j01_journey_linking_bed_v01.wav",
        "plan": OWB / "J01_Journey-To-Every-World/05_Music/j01_journey_linking_bed_v01_plan.json",
        "note": "Plan says this drone is reused from the owned 026 nearest-star stem. Not an independent negative.",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_plan(path: Path) -> dict:
    data = json.loads(path.read_text())
    prompt = data.get("prompt") or ""
    if not prompt and data.get("takes"):
        prompt = data["takes"][0].get("prompt") or ""
    keep = {
        "prompt": prompt,
        "source": data.get("source"),
        "job": data.get("job"),
        "song_id": data.get("song_id"),
        "model_id": data.get("model_id"),
        "sha256_recorded_in_plan": data.get("sha256"),
        "duration_s_recorded_in_plan": data.get("duration_s"),
        "created_at": data.get("created_at"),
        "cue": data.get("cue"),
        "film": data.get("film"),
        "bed": data.get("bed") or data.get("audio_file"),
    }
    return keep


def style_tokens(prompt: str) -> list[str]:
    low = prompt.lower()
    return [w for w in ("ambient", "chamber", "drone", "stationary") if w in low]


def record_sources() -> list[dict]:
    rows = []
    for spec in SOURCES:
        audio, plan = spec["audio"], spec["plan"]
        if not audio.is_file() or not plan.is_file():
            raise SystemExit(f"missing owned file: {audio} or {plan}")
        meta = load_plan(plan)
        prompt = meta["prompt"]
        found = style_tokens(prompt)
        missing = [w for w in spec["styles_expected"] if w not in found]
        stationary_ok = bool(spec["stationary"]) and "drone" in found and "no drum beat" in prompt.lower()
        rows.append({
            "id": spec["id"],
            "work": spec["work"],
            "audio": str(audio),
            "plan": str(plan),
            "bytes": audio.stat().st_size,
            "sha256": sha256_file(audio),
            "plan_sha256": sha256_file(plan),
            "styles_found_in_own_prompt": found,
            "styles_expected": spec["styles_expected"],
            "label_ok": not missing,
            "missing_style_tokens": missing,
            "stationary_label_ok": stationary_ok,
            "use_for_positives": bool(spec["positives"]) and not missing,
            "note": spec.get("note", ""),
            "plan_fields": meta,
            "independence": (
                "Separate film, separate plan prompt, and a recorded source or song id when the plan has one. "
                "A different hash is recorded and is not itself the independence claim."
            ),
        })
    return rows


def write_corpus(sources: list[dict]) -> dict:
    corpus = {
        "job": "J2803",
        "measured": False,
        "threshold": BAR,
        "compare_cap_seconds": mg.MAX_SECONDS,
        "frame_seconds": 1,
        "gate_sha256": hashlib.sha256(Path(mg.__file__).read_bytes()).hexdigest(),
        "candidate_sha256": hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
        "protocol": {
            "positives": [
                "trim the first 0.37 s",
                "gain -12 dB",
                "linear fade-in 0.8 s and fade-out 1.2 s",
                "re-encode to 64 kbps mp3 and decode back",
                "combined: 0.37 s trim, -12 dB, both fades, then 64 kbps mp3",
            ],
            "negatives": "Every pair of sources whose work ids differ, whose own prompts do not say one reuses the other, and whose style tokens matched.",
            "not_independent": [
                "HOS 009 wonder with HOS 009 teach: two cues of one score",
                "J01 linking bed with OWB 026: the J01 plan says it is reused from the 026 stem",
            ],
            "no_listening": "Styles come from the written plan prompt. This run does not claim to hear the beds.",
        },
        "sources": sources,
    }
    (HERE / "CORPUS.json").write_text(json.dumps(corpus, indent=2) + "\n")
    print("CORPUS_WRITTEN", HERE / "CORPUS.json", flush=True)
    return corpus


def fade(x: np.ndarray, fade_in: float, fade_out: float) -> np.ndarray:
    y = np.array(x, copy=True)
    n_in = min(len(y), int(fade_in * mg.SR))
    n_out = min(len(y), int(fade_out * mg.SR))
    if n_in > 1:
        y[:n_in] *= np.linspace(0, 1, n_in, dtype=np.float32)
    if n_out > 1:
        y[-n_out:] *= np.linspace(1, 0, n_out, dtype=np.float32)
    return y


def to_mp3_pcm(x: np.ndarray, tmp: Path) -> np.ndarray:
    path = tmp / "take.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(mg.SR), "-ac", "1", "-i", "-", "-b:a", "64k", str(path)],
        input=np.ascontiguousarray(x, dtype=np.float32).tobytes(),
        check=True,
    )
    return mg.decode(path)


def variants(x: np.ndarray, tmp: Path) -> list[tuple[str, np.ndarray]]:
    trimmed = x[int(0.37 * mg.SR) :]
    gained = x * np.float32(10 ** (-12 / 20))
    faded = fade(x, 0.8, 1.2)
    lossy = to_mp3_pcm(x, tmp)
    combined = to_mp3_pcm(fade(trimmed, 0.8, 1.2) * np.float32(10 ** (-12 / 20)), tmp)
    return [
        ("trim_0_37s", trimmed),
        ("gain_minus12db", gained),
        ("fade_in_0_8s_out_1_2s", faded),
        ("mp3_64k", lossy),
        ("combined_trim_gain_fade_mp3", combined),
    ]


def both(a_pcm: np.ndarray, b_pcm: np.ndarray) -> dict:
    prod = windows.match_report(mg.frames(a_pcm), mg.frames(b_pcm))
    prop = windows.match_report(candidate.frames(a_pcm), candidate.frames(b_pcm))
    return {"production": prod, "candidate": prop}


def main() -> None:
    sources = record_sources()
    corpus = write_corpus(sources)
    by_id = {row["id"]: row for row in sources}
    decoded = {}
    print("DECODING", flush=True)
    for row in sources:
        decoded[row["id"]] = mg.decode(Path(row["audio"]))
        print("decoded", row["id"], round(len(decoded[row["id"]]) / mg.SR, 2), flush=True)

    positives = []
    with tempfile.TemporaryDirectory(prefix="j2803-") as tmpdir:
        tmp = Path(tmpdir)
        for row in sources:
            if not row["use_for_positives"]:
                continue
            original = decoded[row["id"]]
            for name, audio in variants(original, tmp):
                scores = both(original, audio)
                positives.append({
                    "id": f"{row['id']}__{name}",
                    "source": row["id"],
                    "work": row["work"],
                    "transform": name,
                    "styles": row["styles_found_in_own_prompt"],
                    "stationary": row["stationary_label_ok"],
                    "sha256_variant_pcm": hashlib.sha256(np.ascontiguousarray(audio, dtype=np.float32).tobytes()).hexdigest(),
                    **scores,
                })
                print(
                    "positive",
                    positives[-1]["id"],
                    "prod", round(scores["production"]["score"], 3),
                    "cand", round(scores["candidate"]["score"], 3),
                    flush=True,
                )

    def cites_reuse(a: dict, b: dict) -> str:
        text = (a["plan_fields"]["prompt"] + " " + b["plan_fields"]["prompt"]).lower()
        if "reused from" in text:
            return "a plan says the bed is reused from another owned stem"
        return ""

    negatives = []
    unresolved = []
    ids = [row["id"] for row in sources]
    for i, left_id in enumerate(ids):
        for right_id in ids[i + 1 :]:
            left, right = by_id[left_id], by_id[right_id]
            reason = ""
            if left["work"] == right["work"]:
                reason = "same film or score"
            elif not left["label_ok"] or not right["label_ok"]:
                reason = "a style token expected from the brief is missing in that plan"
            else:
                reason = cites_reuse(left, right)
            scores = both(decoded[left_id], decoded[right_id])
            item = {
                "id": f"{left_id}__vs__{right_id}",
                "left": left_id,
                "right": right_id,
                "works": [left["work"], right["work"]],
                **scores,
            }
            if reason:
                item["why_unresolved"] = reason
                unresolved.append(item)
            else:
                negatives.append(item)
            kind = "unresolved" if reason else "negative"
            print(kind, item["id"], "prod", round(scores["production"]["score"], 3), "cand", round(scores["candidate"]["score"], 3), flush=True)

    def fails(rows, feature, want_high, stationary_only=False):
        out = []
        for row in rows:
            if stationary_only and not row.get("stationary"):
                continue
            score = row[feature]["score"]
            bad = score < BAR if want_high else score >= BAR
            if bad:
                out.append({"id": row["id"], "feature": feature, "score": score, "bar": BAR, "want": ">=" if want_high else "<"})
        return out

    candidate_positive_fails = fails(positives, "candidate", True)
    candidate_negative_fails = fails(negatives, "candidate", False)
    stationary_fails = fails(positives, "candidate", True, stationary_only=True)
    production_positive_fails = fails(positives, "production", True)
    production_negative_fails = fails(negatives, "production", False)
    bar_met = not candidate_positive_fails and not candidate_negative_fails and not stationary_fails
    result = {
        "job": "J2803",
        "not_a_gate_pass": True,
        "production_script_unchanged": True,
        "threshold": BAR,
        "compare_cap_seconds": mg.MAX_SECONDS,
        "corpus_sha256": hashlib.sha256((HERE / "CORPUS.json").read_bytes()).hexdigest(),
        "gate_sha256": corpus["gate_sha256"],
        "candidate_sha256": corpus["candidate_sha256"],
        "validation_bar_met": bar_met,
        "counts": {
            "positives": len(positives),
            "independent_negatives": len(negatives),
            "unresolved_pairs": len(unresolved),
            "stationary_positives": sum(1 for row in positives if row["stationary"]),
        },
        "failures": {
            "candidate_positives_below_0_8": candidate_positive_fails,
            "candidate_independent_negatives_at_or_above_0_8": candidate_negative_fails,
            "candidate_stationary_positives_below_0_8": stationary_fails,
            "production_positives_below_0_8_context_only": production_positive_fails,
            "production_independent_negatives_at_or_above_0_8_context_only": production_negative_fails,
        },
        "positives": positives,
        "independent_negatives": negatives,
        "unresolved_pairs": unresolved,
        "regression_context": "regression_j2795_77.json holds all 77 J2795 comparison scores and match windows. Those prototype figures are not production results.",
    }
    (HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print("VALIDATION_BAR", "MET" if bar_met else "NOT_MET", flush=True)
    print("FAILURES", json.dumps(result["failures"]), flush=True)


if __name__ == "__main__":
    main()
