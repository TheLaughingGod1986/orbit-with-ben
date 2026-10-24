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


class RealYouTubeState(unittest.TestCase):
    """Board must match YouTube (Ben, 24 Oct 23:23): public read wins, old films and Shorts get real titles."""
    NOW = datetime(2026, 10, 24, 22, 0, tzinfo=timezone.utc)
    PUBLIC = {
        "GHZDsiH7L7A": {"channel": "HOS", "title": "What's Really Inside an Atom?", "format": "long", "publishedAt": "2026-10-15T17:00:00Z"},
        "_C92tIJCk8A": {"channel": "HOS", "title": "How Did We Discover Germs?", "format": "long", "publishedAt": "2026-09-03T17:00:00Z"},
        "h8HGfyShEHI": {"channel": "OWB", "title": "Is the Sun Getting Brighter?", "format": "long", "publishedAt": "2026-10-18T17:00:00Z"},
        "LCZRHUyTiq0": {"channel": "HOS", "title": "What Are Cathode Rays?", "format": "short", "publishedAt": "2026-10-23T10:30:00Z"},
    }

    def build(self, **kw):
        args = dict(
            hos={"films": [{"id": "004", "title": "What's Really Inside an Atom?", "air": "2026-10-15"}]},
            owb=[{"film": "022", "title": "Is the Sun Getting Brighter?", "air": "2026-10-18"},
                 {"film": "031", "title": "", "air": ""}],
            briefs={}, jobs=[], checks={}, now=self.NOW, public=self.PUBLIC,
            titles={"031": "What Happens When Earths Magnetic Field Flips"},
            uploads={"OWB:022": [{"videoId": "h8HGfyShEHI", "privacyStatus": "private", "publishAt": "2026-10-18T17:00:00Z"}]},
            overrides={"youtube": {"HOS:001": "_C92tIJCk8A"}},
        )
        args.update(kw)
        return {v["key"]: v for v in vt.build_videos(**args)["videos"]}

    def test_scheduled_that_aired_is_public_done(self):
        v = self.build()["OWB:022"]
        self.assertEqual((v["lane"], v["youtube"]["state"]), ("done", "live"))
        self.assertTrue(v["line"].startswith("Public on YouTube since"))

    def test_title_match_moves_aired_hos_long_to_done(self):
        v = self.build()["HOS:004"]
        self.assertEqual((v["lane"], v["youtube"]["videoId"]), ("done", "GHZDsiH7L7A"))

    def test_forced_id_adds_missing_old_film(self):
        v = self.build()["HOS:001"]
        self.assertEqual((v["lane"], v["title"], v["number"]), ("done", "How Did We Discover Germs?", "001"))

    def test_untitled_film_gets_folder_title(self):
        self.assertEqual(self.build()["OWB:031"]["title"], "What Happens When Earths Magnetic Field Flips")

    def test_public_short_without_record_gets_one_card(self):
        by = self.build()
        shorts = [v for v in by.values() if v["shortId"] == "LCZRHUyTiq0"]
        self.assertEqual(len(shorts), 1)
        self.assertEqual(shorts[0]["title"], "What Are Cathode Rays?")

    def test_ready_needs_a_playable_cut(self):
        by = self.build(
            hos={"films": [{"id": "009", "title": "Why Doesn't the Moon Fall to Earth?", "air": "2026-11-26"},
                           {"id": "006", "title": "Willow", "air": "2026-11-05"}]},
            briefs={"HOS:009": {"you": "Your final OK on Sun 22 Nov.", "youShort": "your final OK Sun 22 Nov", "youWhen": "2026-11-22"},
                    "HOS:006": {"you": "Watch v06 and OK it."}},
            watch={"HOS:006": {"url": "https://studio-kanban.vercel.app/api/watch?v=hos-006-v06", "version": "v06"}},
            jobs=[{"id": "J0862", "status": "blocked", "title": "HOS 009 + 010: Shorts voiceover from the v02 Shorts scripts, park for Chief", "taskKeys": ["HOS:009"]}],
            overrides={"jobFilms": {"J0862": ["HOS:009"]}},
        )
        self.assertEqual(by["HOS:009"]["lane"], "progress")
        self.assertTrue(by["HOS:009"]["line"].startswith("No cut to watch yet"))
        self.assertEqual(by["HOS:009"]["version"], "")  # v02 was the Shorts scripts, not a cut
        self.assertEqual((by["HOS:006"]["lane"], by["HOS:006"]["version"]), ("ready", "v06"))

    def test_short_slug_titles_are_clean(self):
        self.assertEqual(vt.clean_short_slug("friday_2026-10-16_last_star"), "Last star")
        self.assertEqual(vt.clean_short_slug("mon30_comets"), "Comets")
        self.assertEqual(vt.short_title_from_path({"file": "x/10_Shorts/wednesday_neutron_cover/a.mp4"}), "Neutron")


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
