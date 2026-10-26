#!/usr/bin/env python3
"""A Short swap's old copy must read back unscheduled (26 Oct 2026: Earth dM1OgGPAYvw and its swap OVLv9dxTcpE both
showed "Private, scheduled Mon 26 Oct 11:30" on the board, from the shared package folder's newest receipt)."""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board_check  # noqa: E402
import jobs  # noqa: E402
import video_tracker as vt  # noqa: E402

PKG = "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/lift_sudden_air/11_Upload-Package"


def receipt(folder: Path, name: str, vid: str, at: str) -> None:
    (folder / name).write_text(json.dumps({"ok": True, "dryRun": False, "upload": {
        "scheduledFor": at, "responseSummary": json.dumps({"id": vid, "privacyStatus": "private", "publishAt": at})}}))


class TrackerSwap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        pkg = root / PKG
        pkg.mkdir(parents=True)
        receipt(pkg, "PACKAGE_UPLOAD_RESULT_2026-10-15T18-16-01-695Z.json", "OLDOLDOLD01", "2026-10-26T11:30:00.000Z")
        receipt(pkg, "PACKAGE_UPLOAD_RESULT_2026-10-25T15-26-01-074Z.json", "NEWNEWNEW01", "2026-10-26T11:30:00.000Z")
        uploads = root / "00_Brand" / "Channel-Setup" / "social"
        uploads.mkdir(parents=True)
        (uploads / "UPLOADS.json").write_text(json.dumps({"videos": {
            "OLDOLDOLD01": {"packageDir": PKG, "kind": "short", "publishAt": None, "privacyStatus": "private",
                            "supersededBy": "NEWNEWNEW01", "unscheduledAt": "2026-10-25T15:27:00Z"},
            "NEWNEWNEW01": {"packageDir": PKG, "kind": "short", "publishAt": "2026-10-26T11:30:00.000Z",
                            "privacyStatus": "private"},
            "NOPUBLISH01": {"packageDir": PKG, "kind": "short", "privacyStatus": "private"},
        }}))
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_old_copy_keeps_its_null_publish_at(self):
        idx = vt.uploads_index(self.root)
        old = idx["OWB:027:S:OLDOLDOLD01"][0]
        self.assertEqual(old["publishAt"], "")
        self.assertEqual(old["supersededBy"], "NEWNEWNEW01")
        self.assertTrue(idx["OWB:027:S:NEWNEWNEW01"][0]["publishAt"].startswith("2026-10-26T11:30"))

    def test_receipt_fallback_only_reads_its_own_video(self):
        self.assertEqual(vt._receipt_privacy(self.root, PKG, "NOPUBLISH01"), ("", ""))
        self.assertEqual(vt._receipt_privacy(self.root, PKG, "OLDOLDOLD01")[0], "private")

    def test_board_shows_one_card_for_the_slot(self):
        idx = vt.uploads_index(self.root)
        out = vt.build_videos(hos={"films": []}, owb=[], briefs={}, jobs=[], checks={}, uploads=idx, public={},
                              titles={}, overrides={}, now=dt.datetime(2026, 10, 26, 8, 0, tzinfo=dt.timezone.utc))
        keys = [v["key"] for v in out["videos"] if ":S:" in v["key"]]
        self.assertIn("OWB:027:S:NEWNEWNEW01", keys)
        self.assertNotIn("OWB:027:S:OLDOLDOLD01", keys)
        self.assertEqual(board_check.duplicate_slots(out["videos"]), [])


class SlotCheck(unittest.TestCase):
    def card(self, vid):
        return {"key": f"OWB:027:S:{vid}", "type": "short", "parent": "OWB:027",
                "youtube": {"state": "scheduled", "videoId": vid, "publishAt": "2026-10-26T11:30:00.000Z"}}

    def test_two_scheduled_copies_is_a_problem(self):
        probs = board_check.duplicate_slots([self.card("a"), self.card("b"), {**self.card("c"), "key": "OWB:OK:J1"}])
        self.assertEqual(len(probs), 1)
        self.assertIn("2 Shorts scheduled for 2026-10-26T11:30Z", probs[0])


class SwapJobClose(unittest.TestCase):
    AT = dt.datetime(2026, 10, 26, 8, 0, tzinfo=dt.timezone.utc)
    JOB = {"id": "J0940", "title": "027 Short dM1OgGPAYvw: swap to earth_sudden_air_v05 (Private, Mon 26 Oct 11:30 London)"}

    def write(self, folder: Path, old: dict, new: dict, at: str = "2026-10-26T07:30:00.000Z"):
        (folder / "J0940.json").write_text(json.dumps({"at": at, "ok": True, "old": old, "new": new}))

    def test_non_swap_job_needs_nothing(self):
        self.assertEqual(jobs.swap_readback_problem({"id": "J1", "title": "OWB weekly audit"}, self.AT), "")

    def test_swap_without_readback_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIn("no read-back", jobs.swap_readback_problem(self.JOB, self.AT, Path(d)))

    def test_old_copy_still_scheduled_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(Path(d), {"id": "dM1OgGPAYvw", "privacyStatus": "private", "publishAt": "2026-10-26T11:30:00Z"},
                       {"id": "OVLv9dxTcpE", "privacyStatus": "private", "publishAt": "2026-10-26T11:30:00Z"})
            self.assertIn("must be private and unscheduled", jobs.swap_readback_problem(self.JOB, self.AT, Path(d)))

    def test_stale_readback_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(Path(d), {"id": "dM1OgGPAYvw", "privacyStatus": "private", "publishAt": None},
                       {"id": "OVLv9dxTcpE", "privacyStatus": "private", "publishAt": "2026-10-26T11:30:00Z"},
                       at="2026-10-25T15:30:00.000Z")
            self.assertIn("read both copies back again", jobs.swap_readback_problem(self.JOB, self.AT, Path(d)))

    def test_good_readback_passes(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(Path(d), {"id": "dM1OgGPAYvw", "privacyStatus": "private", "publishAt": None},
                       {"id": "OVLv9dxTcpE", "privacyStatus": "private", "publishAt": "2026-10-26T11:30:00Z"})
            self.assertEqual(jobs.swap_readback_problem(self.JOB, self.AT, Path(d)), "")


if __name__ == "__main__":
    unittest.main()
