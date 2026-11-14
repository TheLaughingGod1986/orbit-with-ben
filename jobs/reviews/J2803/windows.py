"""PROPOSAL ONLY. Not wired into scripts/music_gate.py and not a gate result.

Matched-window report for one pairwise comparison. Frames are one second, which
is the production hop, so lag and both windows are whole seconds on that grid.
A fractional-second edit can therefore land on lag 0 or lag 1. The score is the
same number scripts/music_gate.py similarity returns for these frames, including
its floor at 0 when every alignment mean is negative.
"""
from __future__ import annotations

import numpy as np

import music_gate as mg


def match_report(a: np.ndarray, b: np.ndarray, min_overlap: int = 20) -> dict:
    if len(a) < min_overlap or len(b) < min_overlap:
        return {
            "score": 0.0,
            "raw_best_mean": None,
            "lag_seconds": None,
            "overlap_seconds": 0,
            "window_a_seconds": None,
            "window_b_seconds": None,
            "frame_seconds": 1,
        }
    m = a @ b.T
    best = None
    for lag in range(-(len(a) - min_overlap), len(b) - min_overlap + 1):
        d = np.diagonal(m, offset=lag)
        if len(d) < min_overlap:
            continue
        raw = float(d.mean())
        if best is None or raw > best[0]:
            best = (raw, int(lag), int(len(d)))
    raw, lag, n = best
    official = float(mg.similarity(a, b, min_overlap))
    a0 = max(0, -lag)
    b0 = max(0, lag)
    return {
        "score": official,
        "raw_best_mean": raw,
        "lag_seconds": lag,
        "overlap_seconds": n,
        "window_a_seconds": [a0, a0 + n],
        "window_b_seconds": [b0, b0 + n],
        "frame_seconds": 1,
    }
