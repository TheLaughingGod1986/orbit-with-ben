#!/usr/bin/env python3
"""Unit tests for scripts/retention_autopsy.py and launch_check.py 48 h / 7 d autopsy wiring (J3256)."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import launch_check as lc  # noqa: E402
import retention_autopsy as ra  # noqa: E402

UTC = dt.timezone.utc


def t(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text).replace(tzinfo=UTC)


class RsiScoringTests(unittest.TestCase):
    def test_rsi_bounds_and_arrows(self):
        self.assertEqual(ra.rsi(100, 100), 50)
        self.assertEqual(ra.rsi_arrow(50), "→")
        self.assertEqual(ra.rsi(300, 100), 75)
        self.assertEqual(ra.rsi_arrow(75), "↑↑")
        self.assertEqual(ra.rsi(150, 100), 60)
        self.assertEqual(ra.rsi_arrow(60), "↑")
        self.assertEqual(ra.rsi(50, 100), 33)
        self.assertEqual(ra.rsi_arrow(33), "↓")
        self.assertEqual(ra.rsi(10, 100), 9)
        self.assertEqual(ra.rsi_arrow(9), "↓↓")
        self.assertEqual(ra.rsi(0, 100), 0)
        self.assertIsNone(ra.rsi(None, 100))
        self.assertIsNone(ra.rsi(10, 0))
        self.assertIsNone(ra.rsi(10, None))

    def test_one_line_summary_contains_all_six_metrics(self):
        scores = ra.score_metrics(
            {"impressions": 500, "ctr": 4.0, "views": 20, "avg_pct": 35.0, "r30": 60.0, "subs_per_1k": 10.0},
            {"values": {"impressions": 500, "ctr": 4.0, "views": 20, "avg_pct": 35.0, "r30": 60.0, "subs_per_1k": 10.0}},
            ra.niche_benchmark("owb", "48h"),
        )
        line = ra.rsi_summary_line(scores)
        for label in ("Showings", "CTR", "Views", "Avg%", "0:30", "Subs/1k"):
            self.assertIn(label, line)
        self.assertIn("50→", line)


class SteepestDropsTests(unittest.TestCase):
    def test_three_non_overlapping_drops_have_valid_40s_windows(self):
        # 500 s video: 100 points every 5 s, with steep drops around 10 s, 50 s, and 200 s
        curve = [{"at": i / 100.0, "watching": 0.90} for i in range(1, 101)]
        for i in range(2, 100):
            curve[i]["watching"] = 0.60   # -30 pp at 10-15 s
        for i in range(10, 100):
            curve[i]["watching"] = 0.45   # -15 pp at 50-55 s
        for i in range(40, 100):
            curve[i]["watching"] = 0.30   # -15 pp at 200-205 s
        drops = ra.steepest_drops(curve, 500.0)
        self.assertEqual(len(drops), 3)
        for d in drops:
            self.assertFalse(d["proxy"])
            self.assertLess(d["watch_start_s"], d["watch_end_s"])
            self.assertGreaterEqual(d["watch_end_s"] - d["watch_start_s"], 39.0)
            self.assertLessEqual(d["watch_end_s"], 500.0)
        self.assertEqual(drops[0]["delta_pp"], -30.0)

    def test_suppressed_curve_returns_proxy_windows(self):
        drops = ra.steepest_drops([], 495.0, avg_view_seconds=60.0)
        self.assertEqual(len(drops), 3)
        self.assertTrue(all(d["proxy"] for d in drops))
        self.assertEqual((drops[0]["watch_start_s"], drops[0]["watch_end_s"]), (0.0, 40.0))
        self.assertEqual((drops[2]["watch_start_s"], drops[2]["watch_end_s"]), (455.0, 495.0))


class FunnelDiagnosisTests(unittest.TestCase):
    def test_strict_priority_order(self):
        ch_base = {"values": {"impressions": 500}}
        # 1. Low showings wins first
        d1 = ra.diagnose_funnel("owb", "48h", {"impressions": 20, "ctr": 1.0, "avg_pct": 10.0, "r30": 20.0}, ch_base, [], 500.0)
        self.assertEqual(d1["primary"]["step"], 1)
        # 2. Good showings + low CTR -> packaging
        d2 = ra.diagnose_funnel("owb", "48h", {"impressions": 800, "ctr": 1.2, "avg_pct": 15.0, "r30": 30.0}, ch_base, [], 500.0)
        self.assertEqual(d2["primary"]["step"], 2)
        # 3. Good showings + good CTR + weak 0:30 -> hook
        d3 = ra.diagnose_funnel("owb", "48h", {"impressions": 800, "ctr": 4.2, "avg_pct": 20.0, "r30": 32.0}, ch_base, [], 500.0)
        self.assertEqual(d3["primary"]["step"], 3)
        # 4. Good showings/CTR/hook + mid-film cliff -> pacing/picture
        mid = [{"proxy": False, "drop_start_s": 120.0, "delta_pp": -12.0}]
        d4 = ra.diagnose_funnel("owb", "48h", {"impressions": 800, "ctr": 4.2, "avg_pct": 22.0, "r30": 65.0}, ch_base, mid, 500.0)
        self.assertEqual(d4["primary"]["step"], 4)
        # 5. Everything healthy except weak end -> end screen/handoff
        d5 = ra.diagnose_funnel("owb", "48h", {"impressions": 800, "ctr": 4.2, "avg_pct": 42.0, "r30": 68.0}, ch_base, [], 500.0, end_retention=6.0)
        self.assertEqual(d5["primary"]["step"], 5)


class AutopsyQueueWiringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        names = {"owb": "Orbit With Ben", "hos": "History of Science", "ww2": "Field Order History"}
        for name, fake in (
            ("slugs", lambda: ["owb", "hos", "ww2"]),
            ("name", names.get),
            ("label", str.upper),
            ("studio_port", lambda slug: "9223"),
            ("analytics_dir", lambda slug: self.root / "05_Analytics" / slug),
            ("uploads_file", lambda slug: self.root / "uploads" / f"{slug}.json"),
        ):
            p = mock.patch.object(lc.channels, name, fake)
            p.start()
            self.addCleanup(p.stop)

    def _snap(self, slug: str, taken: str, videos: list):
        folder = self.root / "05_Analytics" / slug / "snapshots"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{taken[:10]}.json").write_text(json.dumps({"date": taken[:10], "takenAt": taken, "videos": videos}))

    def test_queues_48h_and_7d_autopsies_across_all_three_channels_and_chains_after_read(self):
        self._snap("owb", "2026-11-22T06:40:00Z", [{
            "id": "owbLong1", "title": "Orbit Long", "format": "long", "privacy": "public",
            "publishedAt": "2026-11-20T06:00:00Z", "seconds": 500, "views": 25,
        }])
        self._snap("hos", "2026-11-22T06:40:00Z", [{
            "id": "hosShort1", "title": "HOS Short", "format": "short", "privacy": "public",
            "publishedAt": "2026-11-20T06:00:00Z", "seconds": 18, "views": 200,
        }])
        self._snap("ww2", "2026-11-22T06:40:00Z", [{
            "id": "ww2Long1", "title": "Mulberry Harbours", "format": "long", "privacy": "public",
            "publishedAt": "2026-11-20T06:00:00Z", "seconds": 1500, "views": 90,
        }])

        # Pre-existing WW2 48h Studio read job still open
        data = {
            "next_id": 10,
            "jobs": [{
                "id": "J0009", "status": "open", "repo": "ww2",
                "title": "Field Order History analytics read ww2Long1 48h",
            }],
        }
        now_48h = t("2026-11-22T07:00:00Z")
        added = lc.queue_due(data, now_48h)
        autopsies = [j for j in data["jobs"] if j.get("autopsy")]
        self.assertEqual({j["autopsy"] for j in autopsies}, {"owbLong1@48h", "ww2Long1@48h"})
        # Never queues Shorts for retention autopsy
        self.assertFalse(any("hosShort1" in (j.get("autopsy") or "") for j in autopsies))
        # WW2 48h autopsy chains strictly after the open WW2 48h analytics read job
        ww2_job = next(j for j in autopsies if j["autopsy"] == "ww2Long1@48h")
        self.assertEqual(ww2_job["after"], "J0009")
        self.assertEqual(ww2_job["required_capabilities"], ["audio_input", "moving_video_input"])
        self.assertEqual(ww2_job["model"], "gemini-argon")
        # OWB 48h autopsy chains after the 48h first-day check job just created by queue_due
        owb_check = next(j for j in data["jobs"] if j.get("launch") == "owbLong1@48")
        owb_auto = next(j for j in autopsies if j["autopsy"] == "owbLong1@48h")
        self.assertEqual(owb_auto["after"], owb_check["id"])
        # Running again queues nothing duplicate
        self.assertEqual(lc.queue_autopsies(data, now_48h + dt.timedelta(minutes=10)), [])

        # At 7 days (168 h), 7d autopsies become due; if a report file already exists, it is skipped
        p_existing = lc.autopsy_path("owb", "owbLong1", "7d")
        p_existing.parent.mkdir(parents=True, exist_ok=True)
        p_existing.write_text("# already done\n")
        added_7d = lc.queue_autopsies(data, t("2026-11-27T07:00:00Z"))
        self.assertEqual(len(added_7d), 1)
        new_7d = next(j for j in data["jobs"] if j["id"] == added_7d[0])
        self.assertEqual(new_7d["autopsy"], "ww2Long1@7d")
        self.assertEqual(new_7d["repo"], "ww2")
        self.assertGreaterEqual(len(added), 2)


if __name__ == "__main__":
    unittest.main()
