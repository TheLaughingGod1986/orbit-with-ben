#!/usr/bin/env python3
"""026 Shorts: Scribe + timing on the LOCKED (untrimmed _raw) takes (J0064).

The v01 words.json were made from the trimmed/peak-limited files that Claude
superseded at lock (#99 5994626502). Picture must time to the LOCK files.

Usage:
  python3 _scribe_lock_v02.py [--media-root <checkout with the gitignored LOCK audio>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from _short_vo_pipeline_v01 import META, probe_dur, run_scribe, script_scribe_diff, silencedetect  # noqa: E402
from el_auth import load_token  # noqa: E402

LOCK_SHA = {
    "mon16_cant_see_nearest_star": "556a5f4a67fe96f76ecfeeb51dfb9831a10b2ff00e1f62695304ed55cd08dcee",
    "wed18_robot_reach_nearest_star": "e2cfe752e0627dffc7f62f13b1e3a9e9fe047b328914441e1bf3c8f30ee14909",
    "fri20_grapefruit_cherry": "35e3e07400a0ba4e9d922908acefde8608eba2f76c579c26b33e9a3eef3552ac",
}
HOLD_S = 2.0
SHORT_MIN, SHORT_MAX = 22.0, 27.0


def process(slug: str, media_root: Path, token: str, mode: str) -> dict:
    stem = META[slug]["stem"]
    rel = HERE.relative_to(REPO) / slug
    lock_mp3 = media_root / rel / f"{stem}_LOCK.mp3"
    lock_wav = media_root / rel / f"{stem}_LOCK.wav"
    out = HERE / slug
    sha = hashlib.sha256(lock_mp3.read_bytes()).hexdigest()
    if sha != LOCK_SHA[slug]:
        raise SystemExit(f"[{slug}] LOCK mp3 sha {sha} != locked {LOCK_SHA[slug]}")

    old = out / "words.json"
    keep = out / "words_v01_trimmed_superseded.json"
    if old.exists() and not keep.exists():
        shutil.copy2(old, keep)

    print(f"[{slug}] Scribe on LOCK mp3…", flush=True)
    data = run_scribe(token, mode, lock_mp3, out / "stt_lock")
    words = [w for w in (data.get("words") or []) if (w.get("type") or "word") == "word"]
    dur = probe_dur(lock_wav)
    payload = {
        "file": str((rel / f"{stem}_LOCK.mp3").as_posix()),
        "sha256": sha,
        "duration_s": round(dur, 3),
        "model": "elevenlabs_scribe_v2",
        "text": (data.get("text") or "").strip(),
        "words": [{"text": w.get("text"), "start": w.get("start"), "end": w.get("end")} for w in words],
    }
    old.write_text(json.dumps(payload, indent=2) + "\n")

    script = (out / f"{stem}.txt").read_text().strip()
    diff = script_scribe_diff(script, payload["text"])
    (out / "script_scribe_diff_lock.json").write_text(json.dumps(diff, indent=2) + "\n")

    first, last = words[0]["start"], words[-1]["end"]
    gaps = [round(b["start"] - a["end"], 3) for a, b in zip(words, words[1:])]
    sil = [(round(s, 3), round(e, 3)) for s, e in silencedetect(lock_wav)]
    total = round(dur + HOLD_S, 2)
    return {
        "slug": slug,
        "lock": payload["file"],
        "sha256_ok": True,
        "duration_s": round(dur, 3),
        "first_word_s": first,
        "last_word_end_s": last,
        "tail_after_last_word_s": round(dur - last, 3),
        "max_word_gap_s": max(gaps) if gaps else 0,
        "gaps_over_0_6s": [{"after": words[i]["text"], "at": words[i]["end"], "gap": g} for i, g in enumerate(gaps) if g > 0.6],
        "silences_-38dB": sil,
        "words": len(words),
        "match_rate_pct": diff["match_rate_pct"],
        "mismatches_number_spelling_only": diff["mismatches_are_number_spelling_only"],
        "mismatches": diff["mismatches"],
        "short_total_with_hold_s": total,
        "in_22_27s": SHORT_MIN <= total <= SHORT_MAX,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-root", type=Path, default=REPO)
    args = ap.parse_args()
    token, mode = load_token()
    rows = [process(s, args.media_root.resolve(), token, mode) for s in META]
    summary = {"job": "J0064", "created_at": datetime.now(timezone.utc).isoformat(), "hold_s": HOLD_S, "shorts": rows}
    (HERE / "SCRIBE_LOCK_v02.json").write_text(json.dumps(summary, indent=2) + "\n")
    for r in rows:
        print(f"{r['slug']}: dur {r['duration_s']}s, words {r['words']}, first {r['first_word_s']}, "
              f"last end {r['last_word_end_s']}, tail {r['tail_after_last_word_s']}, max gap {r['max_word_gap_s']}, "
              f"match {r['match_rate_pct']}% num-only={r['mismatches_number_spelling_only']}, "
              f"total+hold {r['short_total_with_hold_s']}s in22-27={r['in_22_27s']}")


if __name__ == "__main__":
    main()
