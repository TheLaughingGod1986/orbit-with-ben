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

    def test_a_missing_ffprobe_reads_not_checked_not_fail(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "x.mp4").write_bytes(b"fake")
            (d / "snap.json").write_text(json.dumps({"videos": [vid("x", at="2099-01-01T10:30:00Z")]}))
            (d / "up.json").write_text(json.dumps({"videos": {"x": {"file": "x.mp4"}}}))
            g.datetime = type("D", (datetime,), {"now": staticmethod(lambda tz=None: datetime(2098, 12, 25, tzinfo=timezone.utc))})
            old_which = g.shutil.which
            g.shutil.which = lambda name: None
            try:
                g.main(["--snapshot", str(d / "snap.json"), "--uploads", str(d / "up.json"), "--media-root", str(d), "--out", str(d / "out.md")])
            finally:
                g.datetime = datetime
                g.shutil.which = old_which
            text = (d / "out.md").read_text()
            self.assertIn("NOT CHECKED", text)
            self.assertIn("ffprobe, ffmpeg not on PATH", text)
            self.assertNotIn("FAIL", text)


class Waivers(unittest.TestCase):
    OUT = ("FAIL  bd_v04.mp4  dur=26.9s  visor=0.0048\n"
           "   FAIL  Orbit in frame at 0 s (visor 0.0048 \u2265 0.003) \u2014 picture-first lock\n"
           "   warn  picture barely changes in the first second (motion 0.8 < 10)\n")

    def test_reads_only_the_indented_fail_reasons(self):
        self.assertEqual(g.fail_lines(self.OUT), ["Orbit in frame at 0 s (visor 0.0048 \u2265 0.003) \u2014 picture-first lock"])

    def test_a_recorded_waiver_covers_the_exact_fail_only(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "bd_v04.mp4"
            f.write_bytes(b"")
            fail = g.fail_lines(self.OUT)[0]
            (Path(d) / "bd_v04_gate.json").write_text(json.dumps([{"waivers": [{"fail": fail, "waived_by": "Claude 5979615078"}]}]))
            self.assertEqual(g.waived(f, [fail])[0]["waived_by"], "Claude 5979615078")
            self.assertIsNone(g.waived(f, [fail.replace("0.0048", "0.0061")]))  # a new cut: the old waiver no longer counts
            self.assertIsNone(g.waived(f, [fail, "Short runs 41 s"]))           # every FAIL must be covered
            self.assertIsNone(g.waived(Path(d) / "other.mp4", [fail]))            # no sidecar, no waiver


if __name__ == "__main__":
    unittest.main()
