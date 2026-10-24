#!/usr/bin/env python3
"""Tests for the five-lane per-video Studio tracker (Ben, 24 Oct 2026)."""
from __future__ import annotations

import json
import sys
import unittest
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_tracker as vt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
HOS_PIPE = Path("/tmp/hos-sparse/00_Brand/Channel-Setup/PIPELINE.json")


def live_fixture():
    if not HOS_PIPE.exists():
        raise unittest.SkipTest("HOS PIPELINE not at /tmp/hos-sparse (sparse-fetch it for integration checks)")
    from kanban_snapshot import release_record
    hos = json.loads(HOS_PIPE.read_text())
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    for film in owb:
        rec = release_record(str(film.get("film", "")))
        if rec:
            film["release"] = rec
    briefs = json.loads((ROOT / "05_Analytics" / "kanban" / "film_briefs.json").read_text())["films"]
    jobs = json.loads((ROOT / "jobs" / "queue.json").read_text())["jobs"]
    try:
        with urllib.request.urlopen("https://studio-kanban.vercel.app/api/checks", timeout=15) as r:
            checks = json.loads(r.read().decode()).get("checks") or {}
    except Exception as e:
        raise unittest.SkipTest(f"checks API unavailable: {e}")
    return vt.build_videos(hos=hos, owb=owb, briefs=briefs, jobs=jobs, checks=checks,
                           now=datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc))


class ParseNotes(unittest.TestCase):
    def test_timecoded_list(self):
        notes = vt.parse_change_notes(
            "HOS 007 Vaccine: Ben's 3 changes\n"
            "(1) 0:38: the wooden figures look like they fall through the shelf.\n"
            "(2) 2:40: it should be a scratch, not a needle.\n"
            "(3) 4:22: arm artefact when the doctor places it.\n"
        )
        self.assertEqual([n["t"] for n in notes], ["0:38", "2:40", "4:22"])
        self.assertIn("shelf", notes[0]["text"])


class LaneRules(unittest.TestCase):
    def test_change_check_wins_over_open_fix_job(self):
        lane = vt.derive_lane(
            youtube=None,
            check={"verdict": "change", "fixes": [{"t": "0:38", "text": "shelf"}], "handled": False},
            jobs=[{"id": "J1", "status": "open", "title": "HOS 007 Vaccine: Ben's 3 changes on master v03"}],
            brief={"you": "Rewatch v03"},
        )
        self.assertEqual(lane, "changes")

    def test_ben_ok_with_release_jobs_is_progress(self):
        lane = vt.derive_lane(
            youtube=None,
            check={"verdict": "ok", "handled": False},
            jobs=[{"id": "J1", "status": "open", "title": "029 Betelgeuse: Private upload"}],
            brief={"you": "Rewatch v03b"},
        )
        self.assertEqual(lane, "progress")

    def test_scheduled_upload_is_done(self):
        lane = vt.derive_lane(
            youtube={"videoId": "F-jImX5h7ws", "state": "scheduled", "publishAt": "2026-11-29T18:00:00Z"},
            check={"verdict": "ok", "handled": False},
            jobs=[{"id": "J1", "status": "blocked", "title": "Studio finish"}],
            brief={},
        )
        self.assertEqual(lane, "done")

    def test_stuck_flag_when_ok_and_no_job(self):
        flags = vt.flags_for(
            key="OWB:029", lane="ready",
            check={"verdict": "ok", "handled": False},
            jobs=[], brief={"you": "Rewatch"},
            now=datetime(2026, 10, 24, tzinfo=timezone.utc),
        )
        self.assertTrue(any(f["kind"] == "stuck" for f in flags))


class LiveMapping(unittest.TestCase):
    """Real queue + checks as of the 24 Oct rebuild brief."""

    @classmethod
    def setUpClass(cls):
        cls.doc = live_fixture()
        cls.by = {v["key"]: v for v in cls.doc["videos"]}

    def test_vaccine_in_changes_with_three_notes(self):
        v = self.by["HOS:007"]
        self.assertEqual(v["lane"], "changes")
        self.assertGreaterEqual(len(v["notes"]), 3)
        times = {n["t"] for n in v["notes"]}
        self.assertTrue({"0:38", "2:40", "4:22"} <= times)

    def test_willow_in_changes(self):
        self.assertEqual(self.by["HOS:006"]["lane"], "changes")
        self.assertGreaterEqual(len(self.by["HOS:006"]["notes"]), 3)

    def test_gliese_done_private_scheduled_london(self):
        v = self.by["OWB:028"]
        self.assertEqual(v["lane"], "done")
        self.assertEqual(v["youtube"]["videoId"], "F-jImX5h7ws")
        self.assertIn("29 Nov", v["youtube"]["publishAtLondon"])
        self.assertIn("18:00", v["youtube"]["publishAtLondon"])

    def test_betelgeuse_flagged(self):
        v = self.by["OWB:029"]
        self.assertTrue(v["flags"], msg=v)
        kinds = {f["kind"] for f in v["flags"]}
        self.assertTrue(kinds & {"stale", "stuck", "deadline"})


if __name__ == "__main__":
    unittest.main()
