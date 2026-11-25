"""Unit tests for scripts/market_track.py (J3650 Market Intelligence)."""
from __future__ import annotations

import datetime as dt
import io
import json
import pathlib
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import market_track as mt  # noqa: E402


def _make_png(color: tuple[int, int, int], size: tuple[int, int] = (320, 180), fg_box: bool = False) -> bytes:
    img = Image.new("RGB", size, color)
    if fg_box:
        for x in range(60, 260):
            for y in range(25, 155):
                img.putpixel((x, y), (245, 220, 40))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class BreakoutMathsTests(unittest.TestCase):
    def test_parse_iso_duration_and_format_classification(self):
        self.assertEqual(mt.parse_iso_duration("PT4M1S"), 241)
        self.assertEqual(mt.parse_iso_duration("PT4M"), 240)
        self.assertEqual(mt.parse_iso_duration("PT58S"), 58)
        self.assertEqual(mt.parse_iso_duration("PT1H2M3S"), 3723)
        self.assertEqual(mt.classify_format(241), "long")
        self.assertEqual(mt.classify_format(240), "short")
        self.assertEqual(mt.classify_format(55), "short")

    def test_channel_long_median_uses_last_20_longs_only(self):
        videos = []
        # 25 longs: newest 20 have views 1000..20000 (step 1000 -> median 10500), oldest 5 have 999999
        for i in range(25):
            views = (i + 1) * 1000 if i < 20 else 999_999
            day = 25 - i
            videos.append({
                "duration_s": 600,
                "views": views,
                "published_at": f"2026-11-{day:02d}T12:00:00Z",
            })
        # Add Shorts that must be ignored for the long median
        for i in range(5):
            videos.append({
                "duration_s": 45,
                "views": 5_000_000,
                "published_at": f"2026-11-26T0{i}:00:00Z",
            })
        self.assertEqual(mt.channel_long_median(videos, limit=20), 10500.0)

    def test_breakout_3x_at_24h(self):
        ch = {"id": "UC1", "title": "WW2 Eng", "niche": "ww2", "tier": "benchmark", "subscribers": 80_000, "median_long_views": 10_000}
        vid = {"video_id": "v1", "title": "Pearl Harbor: How 21 Winches Righted a Battleship", "duration_s": 1200, "views": 35_000, "likes": 1_800, "published_at": "2026-11-24T00:00:00Z"}
        snaps = {"24h": {"at": "2026-11-25T00:00:00Z", "age_hours": 24.0, "views": 32_000}}
        res = mt.evaluate_breakout(vid, ch, age_hours=26.0, snapshots=snaps)
        self.assertTrue(res["is_breakout"])
        self.assertIn("3x_median_24h", res["breakout_reasons"])
        self.assertEqual(res["format"], "long")
        self.assertEqual(res["multiple"], 3.5)

    def test_breakout_100k_within_72h_on_small_channel(self):
        ch = {"id": "UC2", "title": "Tiny Eng", "niche": "ww2", "tier": "rising", "subscribers": 1_410, "median_long_views": 60_000}
        vid = {"video_id": "v2", "title": "B-29 Pressurised Cabin: Why Engines Caught Fire", "duration_s": 900, "views": 115_000, "likes": 4_200, "published_at": "2026-11-23T00:00:00Z"}
        res = mt.evaluate_breakout(vid, ch, age_hours=48.0, snapshots={})
        self.assertTrue(res["is_breakout"])
        self.assertIn("100k_72h_small", res["breakout_reasons"])

    def test_non_breakout_under_threshold(self):
        ch = {"id": "UC3", "title": "Big Space", "niche": "owb", "tier": "benchmark", "subscribers": 250_000, "median_long_views": 100_000}
        vid = {"video_id": "v3", "title": "Europa Ocean Explained", "duration_s": 800, "views": 150_000, "likes": 6_000, "published_at": "2026-11-24T00:00:00Z"}
        res = mt.evaluate_breakout(vid, ch, age_hours=24.0, snapshots={"24h": {"views": 150_000}})
        self.assertFalse(res["is_breakout"])

    def test_snapshot_buckets(self):
        self.assertEqual(mt.snapshot_bucket(6.0), "6h")
        self.assertEqual(mt.snapshot_bucket(24.0), "24h")
        self.assertEqual(mt.snapshot_bucket(72.0), "72h")
        self.assertIsNone(mt.snapshot_bucket(1.0))
        self.assertIsNone(mt.snapshot_bucket(120.0))


class FarmFilterTests(unittest.TestCase):
    def test_drops_low_like_ratio_farm(self):
        vid = {"video_id": "f1", "title": "USS Enterprise Repair Story", "views": 100_000, "likes": 900}
        farm, reason = mt.is_farm_video(vid)
        self.assertTrue(farm)
        self.assertTrue(reason.startswith("low_like_ratio:"))

    def test_drops_templated_what_x_said_when_title(self):
        for title in (
            "What German Generals Said When They Saw the Sherman Tank",
            "What Happened When British Mechanics Opened a U-Boat Engine",
            "When Japanese Pilots Saw the P-51 Over Tokyo",
            "What Stunned Soviet Tankers Inside a Captured Tiger",
        ):
            farm, reason = mt.is_farm_video({"title": title, "views": 50_000, "likes": 2_500})
            self.assertTrue(farm, f"expected farm flag on: {title}")
            self.assertEqual(reason, "templated_title")

    def test_farm_never_marked_as_breakout(self):
        ch = {"id": "UCf", "title": "Slop Channel", "niche": "ww2", "tier": "rising", "subscribers": 5_000, "median_long_views": 1_000}
        vid = {"video_id": "f2", "title": "What German Officers Said When They Saw American Rations", "duration_s": 1200, "views": 150_000, "likes": 1_000}
        res = mt.evaluate_breakout(vid, ch, age_hours=24.0)
        self.assertTrue(res["is_farm"])
        self.assertFalse(res["is_breakout"])
        self.assertEqual(res["breakout_reasons"], [])

    def test_keeps_legitimate_high_engagement_video(self):
        farm, _ = mt.is_farm_video({"title": "How the US Raised Pearl Harbor's Sunken Battleships", "views": 100_000, "likes": 4_500})
        self.assertFalse(farm)


class QuotaGuardTests(unittest.TestCase):
    def test_enforces_1500_daily_cap_and_forbids_daily_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            qpath = pathlib.Path(tmp) / "quota.json"
            q = mt.QuotaGuard(daily_cap=1500, allow_search=False, state_path=qpath, today="2026-11-25")
            with self.assertRaises(mt.QuotaError):
                q.consume("search.list", 100)
            q.consume("playlistItems.list", 90)
            q.consume("videos.list", 45)
            q.save()

            # Reloading the same UTC day continues counting against the 1,500 cap.
            q2 = mt.QuotaGuard(daily_cap=1500, allow_search=False, state_path=qpath, today="2026-11-25")
            self.assertEqual(q2.used, 135)
            with self.assertRaises(mt.QuotaError):
                q2.consume("videos.list", 1400)
            self.assertEqual(q2.used, 135)

    def test_caps_daily_limit_even_if_caller_requests_higher(self):
        q = mt.QuotaGuard(daily_cap=5000, allow_search=False, today="2026-11-25")
        self.assertEqual(q.daily_cap, 1500)


class RollupAndTaggingTests(unittest.TestCase):
    def test_snapshot_rollup_folds_old_days_into_weekly_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            daily_dir = pathlib.Path(tmp) / "daily"
            weekly_dir = pathlib.Path(tmp) / "weekly"
            daily_dir.mkdir()
            # Two old days in ISO week 2026-W44 and one recent day kept untouched
            old1 = {"date": "2026-10-27", "quota": {"used": 120}, "breakouts": [{"video_id": "a1", "format": "long", "views": 40_000, "multiple": 4.0}], "farms": [{"video_id": "fm1"}]}
            old2 = {"date": "2026-10-28", "quota": {"used": 130}, "breakouts": [{"video_id": "a1", "format": "long", "views": 65_000, "multiple": 6.5}, {"video_id": "a2", "format": "short", "views": 120_000, "multiple": 5.0}], "farms": []}
            recent = {"date": "2026-11-24", "quota": {"used": 110}, "breakouts": [], "farms": []}
            (daily_dir / "2026-10-27.json").write_text(json.dumps(old1))
            (daily_dir / "2026-10-28.json").write_text(json.dumps(old2))
            (daily_dir / "2026-11-24.json").write_text(json.dumps(recent))

            written = mt.rollup_daily_snapshots(daily_dir=daily_dir, weekly_dir=weekly_dir, today=dt.date(2026, 11, 25), keep_days=14)
            self.assertEqual(len(written), 1)
            self.assertFalse((daily_dir / "2026-10-27.json").exists())
            self.assertFalse((daily_dir / "2026-10-28.json").exists())
            self.assertTrue((daily_dir / "2026-11-24.json").exists())

            rolled = json.loads(written[0].read_text())
            self.assertEqual(rolled["days"], ["2026-10-27", "2026-10-28"])
            self.assertEqual(rolled["quota_units_total"], 250)
            self.assertEqual(rolled["breakout_count"], 2)
            self.assertEqual(rolled["farm_count"], 1)
            # Deduplicated a1 keeps highest views and sorts long before short
            self.assertEqual(rolled["breakouts"][0]["video_id"], "a1")
            self.assertEqual(rolled["breakouts"][0]["views"], 65_000)
            self.assertEqual(rolled["breakouts"][1]["video_id"], "a2")

    def test_title_and_thumbnail_tagging_and_weekly_report(self):
        tt1 = mt.tag_title("Pearl Harbor: How 21 Winches Raised a Battleship", "ww2")
        self.assertTrue(tt1["starts_with_searched_name"])
        self.assertFalse(tt1["how_why_opener"])
        self.assertTrue(tt1["has_number"])
        self.assertEqual(tt1["word_count"], 8)

        tt2 = mt.tag_title("Why Did Saturn's Rings Appear 100 Million Years Ago?", "owb")
        self.assertTrue(tt2["how_why_opener"])
        self.assertTrue(tt2["has_number"])
        self.assertTrue(tt2["is_question"])

        raw_img = _make_png((20, 30, 50), fg_box=True)
        th = mt.tag_thumbnail(
            "https://i.ytimg.com/vi/abc/hqdefault.jpg",
            vision_fn=lambda b, u: {"main_subject": "battleship hull", "words_on_thumb": 2, "has_face": False},
            fetcher=lambda u: raw_img,
        )
        self.assertTrue(th["vision_tagged"])
        self.assertEqual(th["main_subject"], "battleship hull")
        self.assertEqual(th["words_on_thumb"], 2)
        self.assertFalse(th["has_face"])
        self.assertIsNotNone(th["frame_fill_pct_168px"])
        self.assertGreater(th["frame_fill_pct_168px"], 25.0)

        with tempfile.TemporaryDirectory() as tmp:
            out_md = pathlib.Path(tmp) / "2026-11-25.md"
            sample = [{
                "video_id": "abc", "niche": "ww2", "format": "long", "title": "Pearl Harbor: How 21 Winches Raised a Battleship",
                "channel_title": "Test Eng", "channel_subscribers": 1410, "channel_tier": "rising",
                "views": 180000, "views_per_hour": 5000.0, "multiple": 12.0, "age_hours": 36.0,
                "title_tags": tt1, "thumb_tags": th, "angle": mt.suggest_angle({"niche": "ww2", "format": "long", "title": "Pearl Harbor: How 21 Winches Raised a Battleship"}),
            }]
            mt.write_weekly_report(sample, out_md, "2026-11-25", mt.summarize_patterns(sample))
            txt = out_md.read_text()
            self.assertIn("The angle we could take:", txt)
            self.assertIn("Pearl Harbor", txt)

    def test_monthly_discovery_enforces_40_credit_cap(self):
        wl = {"channels": [{"id": "UC1", "title": "Ch1", "niche": "ww2", "video_count": 10}]}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                mt.monthly_discovery_plan(wl, out_dir=pathlib.Path(tmp), month_str="2026-12", credit_budget=45)
            doc = mt.monthly_discovery_plan(wl, out_dir=pathlib.Path(tmp), month_str="2026-12", credit_budget=40)
            self.assertEqual(doc["credit_budget"], 40)
            self.assertTrue(doc["never_buy_credits"])
            self.assertTrue((pathlib.Path(tmp) / "2026-12.md").is_file())

    def test_board_publish_reads_market_board_json(self):
        import board_publish as bp
        self.assertIn("/05_Analytics/market/board.json", bp.STUDIO_SPARSE)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            p = root / "05_Analytics" / "market" / "board.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"schemaVersion": 1, "watchlistTotal": 88, "breakouts": []}))
            board: dict = {}
            orig_wt = bp.wt
            try:
                bp.wt = lambda slug=None: root
                bp.add_market(board)
            finally:
                bp.wt = orig_wt
            self.assertEqual(board["market"]["watchlistTotal"], 88)


if __name__ == "__main__":
    unittest.main()
