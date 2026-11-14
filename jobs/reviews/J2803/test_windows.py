"""Focused regressions for the unmatched production feature and the proposed window report.

Does not run the owned-bed corpus and does not change a production verdict.
"""
import hashlib
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import candidate  # noqa: E402
import music_gate as mg  # noqa: E402
import windows  # noqa: E402

CANDIDATE_SHA = "7c5a915cc2e55911c7d080cc05eac418d770298e5e0d6e64b746f6087ecfba54"
GATE_SHA = "62b5159f95598eaca5256b30ba66144812bad97dc86fd0c9de4618e4a1dd5385"


def tone(seconds, seed):
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * mg.SR)) / mg.SR
    y = np.zeros(len(t), np.float32)
    step = 3 * mg.SR
    for i in range(0, len(t) // step):
        sl = slice(i * step, (i + 1) * step)
        f = 110 * 2 ** (int(rng.integers(0, 24)) / 12)
        u = t[sl] - i * 3
        y[sl] = np.sin(2 * np.pi * f * u).astype(np.float32) * np.exp(-0.2 * u).astype(np.float32)
    return y


class WindowReport(unittest.TestCase):
    def test_proposal_files_match_the_isolated_candidate_and_production_gate(self):
        self.assertEqual(hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(), CANDIDATE_SHA)
        self.assertEqual(hashlib.sha256(Path(mg.__file__).read_bytes()).hexdigest(), GATE_SHA)

    def test_integer_offset_windows_and_score_agree_with_production_similarity(self):
        y = tone(80, 17)
        a = candidate.frames(y)
        b = candidate.frames(y[17 * mg.SR :])
        report = windows.match_report(a, b)
        self.assertAlmostEqual(report["score"], mg.similarity(a, b), places=5)
        self.assertGreaterEqual(report["score"], mg.SIM_FAIL)
        self.assertEqual(report["lag_seconds"], -17)
        self.assertEqual(report["window_a_seconds"][0], 17)
        self.assertEqual(report["window_b_seconds"][0], 0)
        self.assertEqual(report["overlap_seconds"], report["window_a_seconds"][1] - report["window_a_seconds"][0])
        self.assertEqual(report["overlap_seconds"], report["window_b_seconds"][1] - report["window_b_seconds"][0])
        self.assertAlmostEqual(report["score"], max(0.0, report["raw_best_mean"]), places=5)

    def test_identical_window_is_the_whole_overlap(self):
        y = tone(40, 3)
        a = candidate.frames(y)
        report = windows.match_report(a, a)
        self.assertEqual(report["lag_seconds"], 0)
        self.assertEqual(report["window_a_seconds"], report["window_b_seconds"])
        self.assertGreaterEqual(report["score"], mg.SIM_FAIL)

    def test_fractional_trim_and_gain_stay_above_the_threshold(self):
        y = tone(90, 11)
        a = candidate.frames(y)
        shifted = y[int(0.37 * mg.SR) :] * 10 ** (-12 / 20)
        report = windows.match_report(a, candidate.frames(shifted))
        self.assertGreaterEqual(report["score"], mg.SIM_FAIL)
        self.assertIsNotNone(report["window_a_seconds"])
        self.assertIsNotNone(report["window_b_seconds"])

    def test_shared_envelope_still_fools_production_and_not_the_candidate(self):
        rng = np.random.default_rng(2795)
        t = np.arange(120 * mg.SR) / mg.SR
        envelope = (0.01 + 0.49 * (t / 120) ** 2).astype(np.float32)
        left = (rng.standard_normal(len(t)).astype(np.float32) * envelope)
        right = (rng.standard_normal(len(t)).astype(np.float32) * envelope)
        prod = windows.match_report(mg.frames(left), mg.frames(right))
        prop = windows.match_report(candidate.frames(left), candidate.frames(right))
        self.assertGreaterEqual(prod["score"], mg.SIM_FAIL)
        self.assertLess(prop["score"], mg.SIM_FAIL)


if __name__ == "__main__":
    unittest.main()
