"""gate_upcoming.py: which scheduled Shorts get gated, and the report it writes (7 Oct 2026)."""
import json, sys, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_upcoming as g  # noqa: E402

NOW = datetime(2026, 10, 7, 10, 0, tzinfo=timezone.utc)


def vid(i, fmt="short", privacy="private", at=None, title="T"):
    return {"id": i, "format": fmt, "privacy": privacy, "publishAt": at, "title": title}


class Upcoming(unittest.TestCase):
    def test_picks_scheduled_shorts_in_the_window_soonest_first(self):
        snap = {"videos": [
            vid("fri", at="2026-10-16T10:30:00Z"),
            vid("mon", at="2026-10-12T10:30:00Z"),
            vid("long", fmt="long", at="2026-10-11T17:00:00Z"),
            vid("live", privacy="public", at=None),
            vid("far", at="2026-11-30T10:30:00Z"),
            vid("past", at="2026-10-01T10:30:00Z"),
            vid("noschedule"),
        ]}
        rows = g.upcoming(snap, {"videos": {"mon": {"file": "m.mp4"}}}, NOW, 14)
        self.assertEqual([r["id"] for r in rows], ["mon", "fri"])
        self.assertEqual(rows[0]["air"], "2026-10-12")
        self.assertEqual(rows[0]["file"], "m.mp4")
        self.assertIsNone(rows[1]["file"])

    def test_falls_back_to_uploads_publish_time_and_skips_retired(self):
        snap = {"videos": [vid("a"), vid("b")]}
        uploads = {"videos": {"a": {"publishAt": "2026-10-09T10:30:00.000Z", "file": "a.mp4"},
                              "b": {"publishAt": "2026-10-09T10:30:00.000Z", "retired": True}}}
        self.assertEqual([r["id"] for r in g.upcoming(snap, uploads, NOW, 14)], ["a"])

    def test_london_date_crosses_midnight_in_summer_time(self):
        self.assertEqual(g.london_date("2026-10-11T23:30:00Z"), "2026-10-12")

    def test_report_flags_a_short_with_no_export(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "snap.json").write_text(json.dumps({"videos": [vid("x", at="2099-01-01T10:30:00Z")]}))
            (d / "up.json").write_text(json.dumps({"videos": {"x": {"file": "missing.mp4"}}}))
            g.datetime = type("D", (datetime,), {"now": staticmethod(lambda tz=None: datetime(2098, 12, 25, tzinfo=timezone.utc))})
            try:
                g.main(["--snapshot", str(d / "snap.json"), "--uploads", str(d / "up.json"), "--media-root", str(d), "--out", str(d / "out.md")])
            finally:
                g.datetime = datetime
            text = (d / "out.md").read_text()
            self.assertIn("NO FILE", text)
            self.assertIn("missing.mp4", text)


if __name__ == "__main__":
    unittest.main()
