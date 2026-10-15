"""weekly_public_audit.py (studio core): the report from fake public pages, with no network and no ffmpeg."""
import json, pathlib, sys, tempfile, unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import weekly_public_audit as wpa  # noqa: E402


def snap(subs, longs, shorts):
    return {"subs": subs, "longs": [dict(id=i, title=t, views=v) for i, t, v in longs],
            "shorts": [dict(id=i, title=t, views=v) for i, t, v in shorts]}


class WeeklyAudit(unittest.TestCase):
    def run_week(self, prev, now):
        tmp = pathlib.Path(tempfile.mkdtemp())
        if prev:
            (tmp / "2026-10-05").mkdir()
            (tmp / "2026-10-05" / "PUBLIC_SNAPSHOT.json").write_text(json.dumps(dict(prev, captured="2026-10-05")))
        pages = {"videos": now["longs"], "shorts": now["shorts"]}
        with mock.patch.object(wpa, "WEEKLY", tmp), \
             mock.patch.object(wpa, "fetch", side_effect=lambda url: url.rsplit("/", 1)[1]), \
             mock.patch.object(wpa, "initial_data", side_effect=lambda html: html), \
             mock.patch.object(wpa, "parse_longs", side_effect=lambda d: pages["videos"]), \
             mock.patch.object(wpa, "parse_shorts", side_effect=lambda d: pages["shorts"]), \
             mock.patch.object(wpa, "subscribers", return_value=now["subs"]), \
             mock.patch.object(wpa.shutil, "which", return_value=None), \
             mock.patch.object(sys, "argv", ["weekly_public_audit.py", "--date", "2026-10-12"]):
            self.assertEqual(wpa.main(), 0)
        return (tmp / "2026-10-12" / "REPORT.md").read_text()

    def test_gain_is_like_for_like_and_returning_shorts_are_not_new(self):
        prev = snap(100, [("L1", "Why Mars Is Red", 1000)], [("S2", "b", 50), ("S3", "c", 40)])
        now = snap(110, [("L1", "Why Mars Is Red", 1200)], [("S1", "new", 30), ("S2", "b", 60), ("S9", "old one", 5)])
        r = self.run_week(prev, now)
        self.assertIn("| Subscribers | 110 | +10 |", r)
        self.assertIn("+40 (like for like)", r)          # S2 +10 and the new S1's 30; S9 only came back into view
        self.assertIn("Back in the newest-48 list (older, not new): `S9`", r)
        self.assertIn("| short | `S1` |", r)
        self.assertNotIn("| short | `S9` |", r)

    def test_hidden_subscriber_count_does_not_crash(self):
        r = self.run_week(snap(None, [], []), snap(None, [], [("S1", "a", 1)]))
        self.assertIn("| Subscribers | hidden | — |", r)

    def test_shared_four_word_title_formula_is_flagged(self):
        now = snap(5, [("L1", "Why Did Franklin Fly a Kite", 10), ("L2", "Why Did Franklin Fly to Paris", 3)], [])
        r = self.run_week(None, now)
        self.assertIn("Same title formula on 2 longs", r)

    def test_the_channel_profile_names_its_shorts_log(self):
        r = self.run_week(None, snap(5, [], []))
        self.assertIn(wpa.channel.SHORTS_LOG, r)


if __name__ == "__main__":
    unittest.main()
