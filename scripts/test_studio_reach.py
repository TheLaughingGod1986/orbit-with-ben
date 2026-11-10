#!/usr/bin/env python3
"""Pure tests for the monthly Studio Reach archive. No Chrome."""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import studio_reach as reach


LONG = {
    "cards": [
        {"keyMetricCardData": {"keyMetricTabs": [
            {"primaryContent": {"metric": "VIDEO_THUMBNAIL_IMPRESSIONS", "total": 381}},
            {"primaryContent": {"metric": "VIDEO_THUMBNAIL_IMPRESSIONS_VTR", "total": 3.94}},
        ]}},
        {"screenConfig": {"timePeriod": {"dateIdRange": {"inclusiveStart": 20261001, "exclusiveEnd": 20261101}}}},
    ]
}

SHORT = {
    "cards": [
        {"stackedBarCardData": {"overviewCardData": {
            "values": [70.83],
            "cardData": {"metricColumns": [{"metric": {"type": "SHORTS_FEED_IMPRESSIONS_VTR"}}]},
        }}},
        {"elsewhere": {"inclusiveStart": 20261001, "exclusiveEnd": 20261101}},
    ]
}


class Window(unittest.TestCase):
    def test_october_ids_are_the_closed_month(self):
        start, end = reach.month_bounds(2026, 10)
        self.assertEqual((start, end), (dt.date(2026, 10, 1), dt.date(2026, 10, 31)))
        self.assertEqual(reach.window_ids(start, end), (20261001, 20261101))
        self.assertTrue(reach.is_closed_month(start, end))

    def test_november_to_date_stays_open(self):
        start, end = dt.date(2026, 11, 1), dt.date(2026, 11, 5)
        self.assertEqual(reach.window_ids(start, end), (20261101, 20261106))
        self.assertFalse(reach.is_closed_month(start, end))

    def test_morning_archives_only_on_the_first(self):
        self.assertEqual(reach.morning_plan(dt.date(2026, 11, 5)), {"archive": False, "scrape_month": None})
        self.assertEqual(
            reach.morning_plan(dt.date(2026, 12, 1)),
            {"archive": True, "scrape_month": (2026, 11)},
        )


class Extract(unittest.TestCase):
    def test_long_impressions_and_ctr(self):
        self.assertEqual(reach.long_row(LONG), {"format": "long", "impressions": 381, "impressionsCtr": 3.94})
        self.assertEqual(reach.response_window(LONG), (20261001, 20261101))

    def test_short_stayed_comes_from_the_selected_window_bar(self):
        self.assertEqual(reach.short_row(SHORT), {"format": "short", "stayedToWatch": 70.83})

    def test_percent_text_is_a_number(self):
        payload = {"primaryContent": {"metric": "VIDEO_THUMBNAIL_IMPRESSIONS_VTR", "total": "3.2%"}}
        self.assertEqual(reach.key_metric_totals(payload)["VIDEO_THUMBNAIL_IMPRESSIONS_VTR"], 3.2)


class Files(unittest.TestCase):
    def test_archive_is_immutable_and_only_on_the_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "05_Analytics" / "hos"
            folder.mkdir(parents=True)
            (folder / "studio_ctr.json").write_text('{"readAt":"2026-12-01T07:00:00Z"}\n')
            self.assertEqual(reach.archive_studio_ctr(root, "hos", dt.date(2026, 11, 5)), "skipped")
            self.assertEqual(reach.archive_studio_ctr(root, "hos", dt.date(2026, 12, 1)), "written")
            dest = folder / "studio_ctr_2026-12-01.json"
            dest.write_text("original\n")
            self.assertEqual(reach.write_immutable(dest, b"changed\n"), "kept")
            self.assertEqual(dest.read_text(), "original\n")

    def test_closed_month_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "studio_reach_monthly_2026-10.json"
            self.assertEqual(reach.write_reach(path, {"closed": True, "videos": {"a": 1}}), "written")
            self.assertEqual(reach.write_reach(path, {"closed": True, "videos": {"a": 2}}), "kept")
            self.assertEqual(json.loads(path.read_text())["videos"]["a"], 1)

    def test_open_month_can_be_closed_later(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "studio_reach_monthly_2026-11.json"
            self.assertEqual(reach.write_reach(path, {"closed": False, "videos": {}}), "written")
            self.assertEqual(reach.write_reach(path, {"closed": True, "videos": {"b": 1}}), "written")
            self.assertTrue(json.loads(path.read_text())["closed"])


class ChannelsFromTheirOwnFiles(unittest.TestCase):
    """J2533: the reach port and the YouTube id come from each channel's studio/channel.json through channels.py."""

    def sky(self, **youtube):
        from unittest import mock
        base = reach.registry._load()
        sky = dict(base[0], slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3,
                   youtube=youtube)
        return mock.patch.object(reach.registry, "_load", lambda directory=None: base + (sky,))

    def test_the_two_real_channels_read_as_the_old_table_did(self):
        self.assertEqual(reach.reach_channels(), {
            "hos": {"port": 9460, "channel_id": "UCXp7HkBIl1LgaznXuZHJyRg"},
            "owb": {"port": 9223, "channel_id": "UC_esArsDKd3GJvOkeO0DUog"},
        })
        self.assertEqual(list(reach.reach_channels()), ["hos", "owb"])
        self.assertEqual(reach.selected_channels("both"), ["hos", "owb"])
        self.assertEqual(reach.selected_channels("hos"), ["hos"])

    def test_a_made_up_third_channel_is_read_from_its_file(self):
        with self.sky(id="UCsky0000000000000000000", reach_port="9555", studio_port="9224"):
            self.assertEqual(reach.reach_channels()["sky"], {"port": 9555, "channel_id": "UCsky0000000000000000000"})
            self.assertEqual(reach.selected_channels("both"), ["hos", "owb", "sky"])
            self.assertEqual(reach.selected_channels("sky"), ["sky"])
            self.assertEqual(reach.channel_dir(Path("/x"), "sky"), Path("/x/05_Analytics/sky"))

    def test_a_channel_missing_the_port_or_the_id_is_not_read(self):
        for youtube in ({"id": "UCsky0000000000000000000"}, {"reach_port": "9555"}, {}):
            with self.sky(**youtube):
                self.assertEqual(list(reach.reach_channels()), ["hos", "owb"])
                with self.assertRaises(SystemExit):
                    reach.selected_channels("sky")
                with self.assertRaises(SystemExit):
                    reach.channel_dir(Path("/x"), "sky")


if __name__ == "__main__":
    unittest.main()
