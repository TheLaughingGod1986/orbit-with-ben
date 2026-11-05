#!/usr/bin/env python3
"""Tests for progress24.py."""
import datetime as dt, json, os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import progress24 as p

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 4, 13, 0, tzinfo=UTC)


def ms(n_done, awaiting=False):
    return [{"id": f"m{i}", "state": "done" if i < n_done else "todo", "awaitingApproval": awaiting and i == n_done - 1}
            for i in range(9)]


def board(videos, done=()):
    return {"tracker": {"videos": [{"key": k, "title": t, "production": {"milestones": m}} for k, t, m in videos]},
            "owb": {"done": list(done)}}


class Counts(unittest.TestCase):
    def test_counts_and_awaiting_approval(self):
        b = board([("OWB:030", "Thirty", ms(5)), ("HOS:008", "Franklin", ms(4, awaiting=True)), ("OWB:099", "None", [])])
        self.assertEqual(p.video_counts(b), {"OWB:030": [5, "Thirty"], "HOS:008": [3, "Franklin"]})


class History(unittest.TestCase):
    def test_samples_every_30_min_and_drops_after_48h(self):
        h = [{"at": "2026-11-02T10:00Z", "counts": {}}, {"at": "2026-11-04T12:45Z", "counts": {}}]
        h = p.record(h, NOW, {"A": [1, "a"]})
        self.assertEqual([x["at"] for x in h], ["2026-11-04T12:45Z"])     # 50 h old dropped; 15 min too soon
        h = p.record(h, NOW + dt.timedelta(minutes=20), {"A": [2, "a"]})
        self.assertEqual(len(h), 2)

    def test_baseline_nearest_24h(self):
        h = [{"at": "2026-11-03T11:00Z"}, {"at": "2026-11-03T12:30Z"}, {"at": "2026-11-03T14:00Z"}]
        self.assertEqual(p.baseline(h, NOW)["at"], "2026-11-03T12:30Z")
        self.assertEqual(p.baseline([{"at": "2026-11-04T09:00Z"}], NOW)["at"], "2026-11-04T09:00Z")


class Summary(unittest.TestCase):
    def test_moved_jobs_and_films(self):
        hist = [{"at": "2026-11-03T12:30Z", "counts": {"OWB:030": 5, "HOS:008": 4, "OWB:032": 1}}]
        counts = {"OWB:030": [7, "Thirty"], "HOS:008": [4, "Franklin"], "OWB:032": [3, "Thirty-two"], "OWB:040": [1, "New"]}
        done = [{"id": "J1", "by": "codex", "film": "OWB:030", "title": "030 picture pass", "at": "2026-11-04T10:00Z"},
                {"id": "J2", "by": "codex", "title": "032 script review", "repo": "owb", "at": "2026-11-04T09:00Z"},
                {"id": "J3", "by": "gemini", "title": "Daily Studio read", "at": "2026-11-04T07:00Z"}]
        s = p.summarise(hist, NOW, counts, done)
        self.assertEqual(s["jobsDone"], 3)
        self.assertEqual(s["byAgent"], {"codex": 2, "gemini": 1})
        self.assertEqual(s["milestones"], 4)
        self.assertEqual([(m["key"], m["from"], m["to"]) for m in s["moved"]], [("OWB:030", 56, 78), ("OWB:032", 11, 33)])
        self.assertEqual({f["film"] for f in s["films"]}, {"OWB:030", "OWB:032"})
        self.assertEqual(s["otherJobs"], 1)
        self.assertEqual(s["videoJobs"], 2)
        self.assertEqual(s["hours"], 24.5)

    def test_jobs_done_window(self):
        b = board([], done=[{"id": "J1", "at": "2026-11-04T10:00Z"}, {"id": "J2", "at": "2026-11-03T10:00Z"},
                            {"id": "J1", "at": "2026-11-04T10:00Z"}])
        self.assertEqual([j["id"] for j in p.jobs_done(b, NOW)], ["J1"])

    def test_section_writes_history_and_survives_bad_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "h.json"; f.write_text("not json")
            s = p.section(f, board([("OWB:030", "T", ms(2))]), NOW)
            self.assertEqual(s["jobsDone"], 0)
            self.assertEqual(json.loads(f.read_text())[0]["counts"], {"OWB:030": 2})

    def test_schema_correction_is_not_new_production_and_preserves_history(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'h.json'
            old = {'at': '2026-11-03T13:00Z', 'counts': {'HOS:009': 3}}
            f.write_text(json.dumps([old]))
            b = board([('HOS:009', 'Moon', ms(4))], done=[{'id': 'Jreal', 'at': '2026-11-04T12:00Z'}])
            b['tracker']['videos'][0]['production']['milestoneSchema'] = 'studio-nine-stages-hos-aliases-v2'
            s = p.section(f, b, NOW)
            self.assertEqual((s['milestones'], s['moved'], s['hours'], s['jobsDone']), (0, [], 0, 1))
            self.assertEqual(json.loads(f.read_text())[0], old, 'old history is retained unmodified')
            # An actual later completion on the same basis still counts.
            b['tracker']['videos'][0]['production']['milestones'] = ms(5)
            s = p.section(f, b, NOW + dt.timedelta(minutes=31))
            self.assertEqual(s['milestones'], 1)
            self.assertEqual((s['moved'][0]['from'], s['moved'][0]['to']), (44, 56))

    def test_legacy_producer_does_not_compare_against_new_schema_on_rollback(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'h.json'
            f.write_text(json.dumps([{'at': '2026-11-03T13:00Z', 'counts': {'HOS:009': 4}, 'basis': 'v2'}]))
            s = p.section(f, board([('HOS:009', 'Moon', ms(3))]), NOW)
            self.assertEqual((s['milestones'], s['moved'], s['hours']), (0, [], 0))


if __name__ == "__main__":
    unittest.main(verbosity=1)
