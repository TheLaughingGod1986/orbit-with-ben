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
        self.saved = (ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS, ks.WATCH_REGISTER, ks.WATCH_LOCAL_REGISTER, os.environ.pop("WATCH_UPLOAD_KEY", None))
        ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS = self.icloud, {"OWB": owb, "HOS": hos}, self.uploads
        ks.WATCH_REGISTER, ks.WATCH_LOCAL_REGISTER = root / "reg.json", root / "local_reg.json"
        self.saved_sign = (ks.WATCH_LINK_SECRET_FILE, os.environ.pop("WATCH_LINK_SECRET", None), ks.r2_ready)
        # Never upload from a test: on the Mini the main checkout's .env has real R2 keys (25 Oct: a run here
        # sent the 1-byte fixtures to R2 as owb-026-v04 etc.).
        ks.r2_ready = lambda *a, **k: False
        ks.WATCH_LINK_SECRET_FILE = root / "no_secret"

    def tearDown(self):
        ks.WATCH_LINK_SECRET_FILE, ks.r2_ready = self.saved_sign[0], self.saved_sign[2]
        if self.saved_sign[1] is not None:
            os.environ["WATCH_LINK_SECRET"] = self.saved_sign[1]
        ks.ICLOUD, ks.UAT_DIRS, ks.UPLOADS, ks.WATCH_REGISTER, ks.WATCH_LOCAL_REGISTER, key = self.saved
        if key is not None:
            os.environ["WATCH_UPLOAD_KEY"] = key
        self.tmp.cleanup()

    def links(self, owb_extra=None, briefs=None):
        owb = [{"film": "023"}, {"film": "025"}, {"film": "026"}, {"film": "028"}] + (owb_extra or [])
        return ks.watch_links({"films": [{"id": "006"}]}, owb, briefs or {})

    def test_same_film_version_distinct_cuts_and_aliases(self):
        names = [f"029_short_{slug}_v04_PHONE.mp4" for slug in
                 ("wed09_great_dimming", "fri11_opening_testA", "mon14_half_moon_daylight")]
        ids = [ks.watch_id("OWB", "029", "v04", n) for n in names]
        self.assertEqual(len(set(ids)), 3)
        for name, wid in zip(names, ids):
            self.assertEqual(ks.watch_id("OWB", "029", "v04", "nested/" + name), wid)
            self.assertLessEqual(len(wid), 64)

    def test_both_auto_upload_routes_distinguish_same_version_cuts(self):
        from unittest.mock import patch
        names = [f"029_short_{slug}_v04_PHONE.mp4" for slug in
                 ("wed09_great_dimming", "mon14_half_moon_daylight")]
        with patch.object(ks, "auto_upload", return_value=True) as upload:
            for name in names:
                pick = ks.UAT_DIRS["OWB"] / name
                pick.write_bytes(b"fixture")
                rel = "OWB UAT/" + name
                ks.stream_link("OWB", "029", pick, rel)
                ks.ask_watch({"channel": "OWB", "id": "J0961", "version": "v04", "file": rel})
            ids = [call.args[0] for call in upload.call_args_list]
        self.assertNotEqual(ids[0], ids[2])
        self.assertNotEqual(ids[1], ids[3])

    def test_newest_cut_phone_copy_in_files(self):
        w = self.links()["OWB:026"]
        self.assertEqual((w["label"], w["kind"]), ("Watch v04", "files"))
        self.assertTrue(w["url"].startswith("shareddocuments:///private/var/mobile/Library/Mobile%20Documents/com~apple~CloudDocs/OWB%20UAT/026_NearestStar_v04_PHONE.mp4"))

    def test_uploaded_cut_streams_instead_of_files(self):
        ks.WATCH_REGISTER.write_text(json.dumps({"files": {"OWB UAT/026_NearestStar_v04_PHONE.mp4": "owb-026-v04"}}))
        w = self.links()["OWB:026"]
        self.assertEqual((w["kind"], w["url"], w["label"]), ("stream", "https://studio-kanban.vercel.app/api/watch?v=owb-026-v04", "Watch v04"))

    def test_stream_link_is_signed_and_expires(self):
        # Ben, 25 Oct: Play opens the cut with no board code. Same HMAC as api/watch.js signWatch().
        import base64, hashlib, hmac
        (ks.WATCH_LINK_SECRET_FILE).write_text("test-secret\n")
        ks.WATCH_REGISTER.write_text(json.dumps({"files": {"OWB UAT/026_NearestStar_v04_PHONE.mp4": "owb-026-v04"}}))
        w = self.links()["OWB:026"]
        from urllib.parse import parse_qs, urlsplit
        q = {k: v[0] for k, v in parse_qs(urlsplit(w["url"]).query).items()}
        self.assertEqual(set(q), {"v", "e", "s"})
        self.assertNotIn("k=", w["url"])
        want = base64.urlsafe_b64encode(hmac.new(b"test-secret", f"owb-026-v04.{q['e']}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
        self.assertEqual(q["s"], want)
        url = ks.sign_watch_url("https://studio-kanban.vercel.app/api/watch?v=x", now=1_000_000_000, secret="k")
        e = int(parse_qs(urlsplit(url).query)["e"][0])
        self.assertTrue(12 * 3600 < e - 1_000_000_000 <= 15 * 3600)
        self.assertEqual(ks.sign_watch_url("https://youtu.be/abc", secret="k"), "https://youtu.be/abc")

    def test_explicit_stream_link_is_accepted(self):
        w = self.links(briefs={"OWB:026": {"watch": {"url": "https://studio-kanban.vercel.app/api/watch?v=x", "version": "v05"}}})["OWB:026"]
        self.assertEqual(w["kind"], "stream")

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
