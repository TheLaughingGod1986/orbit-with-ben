#!/usr/bin/env python3
"""Music gate: every film has its own music, at a pace that fits it (Ben, 8 Oct 2026, after 023, 024 and 025 all
shipped to his watch on the same `jupiter-music.mp3`).

  python3 scripts/music_gate.py <film dir> --bed <bed.mp3> [--video <cut.mp4>] [--others <dir or file> ...] [--out <json>]

  own       FAIL the bed isn't in this film's 05_Music folder, or has no plan JSON next to it (the generator writes one).
  brief     FAIL the plan's prompt has no "Pace:" line (a BPM range Claude set from the script's narration and arc), or
            doesn't name what it must not sound like ("NOT ..."): Claude writes this prompt with the shot list.
  reused    FAIL the bed sounds like another film's bed or any track under --others (default: every other film's
            05_Music, plus OWB UAT when it exists), even trimmed, offset or re-encoded. Similarity is the best mean
            cosine of 1 s band-energy frames over time offsets: the same track scores about 1, different music well
            under 0.5. FAIL at 0.8 or more.
  length    FAIL (with --video) the bed is shorter than the cut: music runs the whole film, never looped or silent.
  pace      WARN the bed's measured tempo is well outside the brief's BPM range (ambient beds have weak beats, so this
            only asks Claude to listen).
Exit 1 on any FAIL. Fit itself is judged by ear: Claude's review, then Ben's watch."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess as sp
import sys
from pathlib import Path

import numpy as np

SR = 8000
BANDS = 24
SIM_FAIL = 0.8
MAX_SECONDS = 300  # compare the first 5 minutes; a reused bed matches long before that
REPO = Path(__file__).resolve().parent.parent
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
AUDIO = (".mp3", ".wav", ".m4a", ".aac", ".flac")


def decode(path: Path, seconds: float | None = MAX_SECONDS) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-t", str(seconds)] if seconds else []) + \
          ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(sp.run(cmd, capture_output=True, check=True).stdout, np.float32)


def duration(path: Path) -> float:
    return float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                 text=True).strip())


def frames(x: np.ndarray) -> np.ndarray:
    """1 s frames of log band energy (60 Hz-3.8 kHz), each band centred over time, each frame unit length."""
    n = len(x) // SR
    if n < 4:
        return np.zeros((0, BANDS), np.float32)
    spec = np.abs(np.fft.rfft(x[:n * SR].reshape(n, SR) * np.hanning(SR), axis=1)) ** 2
    edges = np.geomspace(60, 3800, BANDS + 1).astype(int)
    e = np.log1p(np.stack([spec[:, a:b].sum(1) for a, b in zip(edges[:-1], edges[1:])], 1))
    e -= e.mean(0)
    return e / (np.linalg.norm(e, axis=1, keepdims=True) + 1e-9)


def similarity(a: np.ndarray, b: np.ndarray, min_overlap: int = 20) -> float:
    """Best mean cosine between aligned frames over every time offset with at least min_overlap seconds in common."""
    if len(a) < min_overlap or len(b) < min_overlap:
        return 0.0
    m = a @ b.T  # cosine of every frame pair
    best = 0.0
    for lag in range(-(len(a) - min_overlap), len(b) - min_overlap + 1):
        d = np.diagonal(m, offset=lag)
        if len(d) >= min_overlap:
            best = max(best, float(d.mean()))
    return best


def tempo(x: np.ndarray) -> float | None:
    """Rough BPM from the autocorrelation of onset strength (50 ms hops); None when there is no clear beat."""
    hop = SR // 20
    n = len(x) // hop
    if n < 200:
        return None
    env = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))
    onset = np.maximum(np.diff(np.log1p(env * 100)), 0)
    onset -= onset.mean()
    ac = np.correlate(onset, onset, "full")[len(onset) - 1:]
    lo, hi = int(20 * 60 / 180), int(20 * 60 / 40)  # 180..40 BPM
    k = lo + int(np.argmax(ac[lo:hi]))
    return round(60 * 20 / k, 1) if ac[k] > 0.1 * ac[0] else None


def others_default(film_dir: Path) -> list[Path]:
    out = [p for p in (REPO / "02_Video-Projects").glob("*/05_Music/*") if p.suffix.lower() in AUDIO
           and film_dir.resolve() not in p.resolve().parents]
    if UAT.is_dir():
        out += [p for p in UAT.glob("*") if p.suffix.lower() in AUDIO]
    return out


def judge(film_dir: Path, bed: Path, video: Path | None = None, others: list[Path] | None = None) -> dict:
    fails, warns = [], []
    music_dir = film_dir / "05_Music"
    if bed.resolve().parent != music_dir.resolve():
        fails.append(f"own: the bed is {bed}, not in this film's 05_Music")
    plan_path = bed.with_name(bed.stem + "_plan.json")
    plan = json.loads(plan_path.read_text()) if plan_path.exists() else None
    if plan is None:
        fails.append(f"own: no plan next to the bed ({plan_path.name})")
    prompt = (plan or {}).get("prompt", "")
    pace = re.search(r"Pace:\s*(\d{2,3})\s*[-–]\s*(\d{2,3})\s*BPM", prompt, re.I)
    if plan is not None and not pace:
        fails.append("brief: the prompt has no 'Pace: NN-NN BPM' line")
    if plan is not None and not re.search(r"\bNOT\b", prompt):
        fails.append("brief: the prompt doesn't say what it must not sound like (NOT ...)")
    x = decode(bed)
    fa = frames(x)
    digest = hashlib.sha256(bed.read_bytes()).hexdigest()
    matches = []
    for o in (others if others is not None else others_default(film_dir)):
        if o.resolve() == bed.resolve():
            continue
        try:
            same = hashlib.sha256(o.read_bytes()).hexdigest() == digest
            s = 1.0 if same else similarity(fa, frames(decode(o)))
        except (OSError, sp.CalledProcessError) as e:
            # An iCloud placeholder that isn't downloaded reads as "Resource deadlock avoided" (Errno 11) on the Mini.
            warns.append(f"reused: couldn't read {o.name} to compare ({e.__class__.__name__}); download it or pass --others")
            continue
        if s >= SIM_FAIL:
            matches.append(dict(file=str(o), similarity=round(s, 3)))
    if matches:
        fails.append("reused: sounds like " + ", ".join(f"{Path(m['file']).name} ({m['similarity']})" for m in matches))
    bed_s = duration(bed)
    if video:
        cut_s = duration(video)
        if bed_s + 0.5 < cut_s:
            fails.append(f"length: the bed is {bed_s:.1f} s, the cut {cut_s:.1f} s")
    bpm = tempo(decode(bed, 120))
    if pace and bpm:
        lo, hi = int(pace.group(1)), int(pace.group(2))
        # A beat tracker often lands on half or double time, so only flag a tempo no octave of which fits.
        if not any(lo * 0.85 <= bpm * f <= hi * 1.15 for f in (0.5, 1, 2)):
            warns.append(f"pace: measured about {bpm} BPM against the brief's {lo}-{hi}; Claude listens")
    return dict(verdict="FAIL" if fails else "PASS", bed=str(bed), seconds=round(bed_s, 1), bpm=bpm,
                brief_pace=pace.group(0) if pace else None, fail=fails, warn=warns, matches=matches,
                rules=dict(similarity_fail=SIM_FAIL, compared_seconds=MAX_SECONDS))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("film_dir", type=Path)
    ap.add_argument("--bed", type=Path, required=True)
    ap.add_argument("--video", type=Path)
    ap.add_argument("--others", type=Path, nargs="*", help="files or folders to compare against (default: other films + OWB UAT)")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    others = None
    if a.others is not None:
        others = []
        for o in a.others:
            others += [p for p in o.rglob("*") if p.suffix.lower() in AUDIO] if o.is_dir() else [o]
    res = judge(a.film_dir, a.bed, a.video, others)
    if a.out:
        a.out.write_text(json.dumps(res, indent=2))
    for f in res["fail"]:
        print("FAIL", f)
    for w in res["warn"]:
        print("WARN", w)
    print(f"music gate {res['verdict']}: {Path(res['bed']).name}, {res['seconds']} s, about {res['bpm']} BPM, brief {res['brief_pace']}")
    return 1 if res["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
