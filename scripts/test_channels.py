#!/usr/bin/env python3
"""Tests for scripts/channels.py, and the phase 1 rule: engine code asks channels.py instead of naming a channel
(docs/MULTI_CHANNEL_PLAN.md; Ben, 5 Nov 2026: "so we just plug in new channels")."""
import json
import pathlib
import re
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import channels  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


class Loader(unittest.TestCase):
    def test_the_two_channels_in_order(self):
        self.assertEqual(channels.slugs(), ["owb", "hos"])
        self.assertEqual(channels.home(), "owb")
        self.assertEqual((channels.label("hos"), channels.name("owb")), ("HOS", "Orbit With Ben"))

    def test_a_jobs_channel_comes_from_repo_then_title_then_home(self):
        self.assertEqual(channels.of_job({"repo": "hos", "title": "x"}), "hos")
        self.assertEqual(channels.of_job({"repo": "owb", "title": "HOS 013: Darwin"}), "hos")  # as before
        self.assertEqual(channels.of_job({"title": "History of Science Shorts gap"}), "hos")
        self.assertEqual(channels.of_job({"title": "033 shot list"}), "owb")
        self.assertEqual(channels.label_of_job({"repo": "hos"}), "HOS")

    def test_film_keys_in_any_spelling(self):
        self.assertEqual(channels.film_keys("OWB 033 and hos-013, HOS:010"), {"OWB:033", "HOS:013", "HOS:010"})
        self.assertTrue(channels.strict_key_re().fullmatch("HOS:013"))
        self.assertFalse(channels.strict_key_re().fullmatch("ABC:013"))

    def test_a_third_channel_plugs_in_by_folder(self):
        with tempfile.TemporaryDirectory() as t:
            for slug in ("owb", "hos", "sky"):
                (pathlib.Path(t) / slug).mkdir()
                c = json.loads((channels.DIR / ("owb" if slug == "sky" else slug) / "channel.json").read_text())
                if slug == "sky":
                    c.update(slug="sky", label="SKY", name="Night Sky", home=False, order=3, title_match=r"\bSKY\b")
                (pathlib.Path(t) / slug / "channel.json").write_text(json.dumps(c))
            loaded = channels._load(t)
            with mock.patch.object(channels, "_load", lambda directory=t: loaded):
                channels.key_re.cache_clear()
                try:
                    self.assertEqual(channels.slugs(), ["owb", "hos", "sky"])
                    self.assertEqual(channels.of_job({"title": "SKY 001 Orion"}), "sky")
                    self.assertEqual(channels.film_keys("SKY 001"), {"SKY:001"})
                finally:
                    channels.key_re.cache_clear()

    def test_repo_path_prefers_env_then_existing_folder(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.dict("os.environ", {"HOS_REPO": ""}):
            (pathlib.Path(t) / "YouTube" / "history-of-science").mkdir(parents=True)
            self.assertEqual(channels.repo_path("hos", pathlib.Path(t)).name, "history-of-science")
        with mock.patch.dict("os.environ", {"HOS_REPO": "/x/hos"}):
            self.assertEqual(str(channels.repo_path("hos")), "/x/hos")


class NoNewChannelNames(unittest.TestCase):
    """Engine files already moved to channels.py must not grow new literal channel regexes."""
    MOVED = ("jobs.py", "kanban_snapshot.py", "progress24.py", "video_progress.py", "workflow_state.py")

    def test_moved_files_use_the_loader(self):
        for name in self.MOVED:
            text = (HERE / name).read_text()
            self.assertIsNone(re.search(r"HOS\|OWB|OWB\|HOS", text), name)
            self.assertNotRegex(text, r'"HOS" if [^\n]*"hos"', name)


if __name__ == "__main__":
    unittest.main()
