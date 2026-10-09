#!/usr/bin/env python3
"""Tests for the Studio Kanban watch links (kanban_snapshot.watch_links): Ben's cut opens on his phone."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kanban_snapshot as ks  # noqa: E402


class WatchLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.icloud, self.uploads = root / "CloudDocs", root / "UPLOADS.json"
        owb, hos = self.icloud / "OWB UAT", self.icloud / "HOS UAT"
        owb.mkdir(parents=True)
        for n in ("026_NearestStar_rough_v04.mp4", "026_NearestStar_v04_PHONE.mp4", "026_NearestStar_rough_v03.mp4",
                  "025_MarsRobot_full_rough_v03f.mp4", "023_Venus_full_rough_v05d.mp4", "023_Venus_v05c_PHONE.mp4"):
            (owb / n).write_bytes(b"x")
        (hos / "006_Trees" / "10_Shorts").mkdir(parents=True)
        (hos / "006_Trees" / "hos_006_part02_rough_v02.mp4").write_bytes(b"x")
        (hos / "006_Trees" / "10_Shorts" / "hos_006_s01_v09.mp4").write_bytes(b"x")
        self.uploads.write_text(json.dumps({"videos": {"Js6EQJ8qDi8": {"kind": "long",
            "packageDir": "02_Video-Projects/025_Mars/11_Upload-Package", "file": "x/025_MarsRobot_full_rough_v03f.mp4"}}}))
        self.saved = (ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS)
        ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS = self.icloud, {"OWB": owb, "HOS": hos}, self.uploads

    def tearDown(self):
        ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS = self.saved
        self.tmp.cleanup()

    def links(self, owb_extra=None, briefs=None):
        owb = [{"film": "023"}, {"film": "025"}, {"film": "026"}, {"film": "028"}] + (owb_extra or [])
        return ks.watch_links({"films": [{"id": "006"}]}, owb, briefs or {})

    def test_newest_cut_phone_copy_in_files(self):
        w = self.links()["OWB:026"]
        self.assertEqual((w["label"], w["kind"]), ("Watch v04", "files"))
        self.assertTrue(w["url"].startswith("shareddocuments:///private/var/mobile/Library/Mobile%20Documents/com~apple~CloudDocs/OWB%20UAT/026_NearestStar_v04_PHONE.mp4"))

    def test_newer_version_beats_older_phone_copy(self):
        self.assertEqual(self.links()["OWB:023"]["version"], "v05d")

    def test_uploaded_video_wins_when_it_is_the_newest_cut(self):
        w = self.links()["OWB:025"]
        self.assertEqual((w["kind"], w["url"]), ("youtube", "https://youtu.be/Js6EQJ8qDi8"))

    def test_newer_uat_cut_beats_the_upload(self):
        (ks.UAT_DIRS["OWB"] / "025_MarsRobot_full_rough_v04.mp4").write_bytes(b"x")
        self.assertEqual(self.links()["OWB:025"]["kind"], "files")

    def test_hos_long_not_shorts(self):
        self.assertEqual(self.links()["HOS:006"]["version"], "v02")

    def test_explicit_link_wins_and_bad_ones_are_ignored(self):
        w = self.links(briefs={"OWB:026": {"watch": {"url": "https://www.icloud.com/iclouddrive/abc", "version": "v05"}}})["OWB:026"]
        self.assertEqual((w["kind"], w["label"]), ("icloud", "Watch v05"))
        w = self.links(briefs={"OWB:026": {"watch": {"url": "javascript:alert(1)"}}})["OWB:026"]
        self.assertEqual(w["kind"], "files")

    def test_nothing_to_watch_no_link(self):
        self.assertNotIn("OWB:028", self.links())


if __name__ == "__main__":
    unittest.main()
