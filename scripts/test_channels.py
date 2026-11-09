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


def _file(slug):
    """A channel's settings file as the loader found it."""
    return pathlib.Path(channels.get(slug)["_source"])


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
                c = json.loads(_file("owb" if slug == "sky" else slug).read_text())
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

    def test_each_channel_names_its_waiting_line(self):
        self.assertEqual((channels.wip_line("owb"), channels.wip_line("hos")), ("next", "next_hos"))

    def test_repo_path_prefers_env_then_existing_folder(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.dict("os.environ", {"HOS_REPO": ""}):
            (pathlib.Path(t) / "YouTube" / "history-of-science").mkdir(parents=True)
            self.assertEqual(channels.repo_path("hos", pathlib.Path(t)).name, "history-of-science")
        with mock.patch.dict("os.environ", {"HOS_REPO": "/x/hos"}):
            self.assertEqual(str(channels.repo_path("hos")), "/x/hos")


class OwnRepos(unittest.TestCase):
    """Phase 2: each channel's settings live in its own repo at studio/channel.json."""

    def test_home_channel_reads_its_own_studio_folder(self):
        self.assertEqual(_file("owb"), channels.ROOT / "studio" / "channel.json")

    def test_a_channels_checkout_wins_over_the_cached_copy(self):
        with tempfile.TemporaryDirectory() as t:
            repo = pathlib.Path(t) / "hos-checkout"
            (repo / "studio").mkdir(parents=True)
            c = json.loads((channels.DIR / "hos" / "channel.json").read_text())
            (repo / "studio" / "channel.json").write_text(json.dumps(dict(c, name="History of Science (own repo)")))
            channels._load.cache_clear()
            with mock.patch.dict("os.environ", {"HOS_REPO": str(repo)}):
                try:
                    self.assertEqual(channels.name("hos"), "History of Science (own repo)")
                    self.assertEqual(_file("hos"), repo / "studio" / "channel.json")
                finally:
                    channels._load.cache_clear()
        self.assertEqual(channels.name("hos"), "History of Science")  # cached copy again without the checkout

    def test_the_cached_copy_matches_the_channel_repo_when_it_is_here(self):
        entry = next(e for e in json.loads((channels.DIR / "channels.json").read_text())["channels"] if e["slug"] == "hos")
        co = channels._checkout(entry)
        if not co:
            self.skipTest("history-of-science is not checked out on this machine")
        self.assertEqual((co / "studio" / "channel.json").read_text(), (channels.DIR / "hos" / "channel.json").read_text(),
                         "run: python3 scripts/channels.py sync")


class Films(unittest.TestCase):
    def test_both_pipeline_kinds_give_the_same_rows(self):
        import channel_films
        with tempfile.TemporaryDirectory() as t:
            root = pathlib.Path(t)
            (root / "02_Video-Projects" / "033_X").mkdir(parents=True)
            (root / "02_Video-Projects" / "033_X" / "status.json").write_text(json.dumps(
                {"film": "033", "title": "X", "air": "2026-12-09T18:00", "stages": {"edit": {"state": "done"}}}))
            (root / "00_Brand" / "Channel-Setup").mkdir(parents=True)
            (root / "00_Brand" / "Channel-Setup" / "PIPELINE.json").write_text(json.dumps(
                {"films": [{"id": "011", "title": "Y", "air": "2026-12-10", "stages": {"edit": {"status": "doing"}}}]}))
            owb, hos = channel_films.films("owb", root), channel_films.films("hos", root)
        self.assertEqual((owb[0]["key"], owb[0]["air"], owb[0]["stages"]), ("OWB:033", "2026-12-09", {"edit": "done"}))
        self.assertEqual((hos[0]["key"], hos[0]["stages"]), ("HOS:011", {"edit": "doing"}))

    def test_picture_route_comes_from_the_channel(self):
        import routing
        hos = routing.job_chain({"kind": "video", "repo": "hos"})
        owb = routing.job_chain({"kind": "video", "repo": "owb"})
        self.assertTrue(all(not m.startswith("veo-") for _, m in hos))           # flow_only: no priced Vertex
        self.assertTrue(any(m.startswith("veo-") for _, m in owb))               # flow_first: Vertex behind Flow
        self.assertTrue(owb[0][1].startswith("flow-"))


class ThirdChannelOnTheBoard(unittest.TestCase):
    def test_a_channel_added_by_folder_gets_video_cards(self):
        import channel_films
        import video_tracker as vt
        base = channels._load()
        sky = dict(json.loads(_file("owb").read_text()), slug="sky", label="SKY",
                   name="Night Sky", short="Sky", home=False, order=3, title_match=r"\bSKY\b",
                   pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        row = {"key": "SKY:001", "id": "001", "title": "Orion", "air": "2026-12-01", "stages": {}, "raw": {}}
        with mock.patch.object(channels, "_load", lambda directory=None: base + (sky,)), \
                mock.patch.object(channel_films, "films", side_effect=lambda slug, root=None: [row] if slug == "sky" else []):
            channels.key_re.cache_clear()
            try:
                out = vt.build_from_docs({}, {}, {})
            finally:
                channels.key_re.cache_clear()
        cards = [v for v in out.get("videos", []) if v.get("key") == "SKY:001"]
        self.assertEqual([(c["channel"], c["title"], c["type"]) for c in cards], [("SKY", "Orion", "long")])


class NoNewChannelNames(unittest.TestCase):
    """Engine files already moved to channels.py must not grow new literal channel regexes."""
    MOVED = ("jobs.py", "kanban_snapshot.py", "progress24.py", "video_progress.py", "workflow_state.py",
             "workflow_handoffs.py", "channel_balance.py", "channel_films.py")

    def test_the_board_page_reads_channels_from_board_json(self):
        app = (HERE.parent / "05_Analytics" / "kanban" / "board_site" / "studio_app.js").read_text()
        self.assertIn("board.channels", app)
        self.assertNotRegex(app, r"'History of Science':'Orbit With Ben'|=== \"HOS\" \? \"hos\" : \"owb\"")
        self.assertNotIn('["ch", "OWB", "Orbit"]', app)

    def test_moved_files_use_the_loader(self):
        for name in self.MOVED:
            text = (HERE / name).read_text()
            self.assertIsNone(re.search(r"HOS\|OWB|OWB\|HOS", text), name)
            self.assertNotRegex(text, r'"HOS" if [^\n]*"hos"', name)


if __name__ == "__main__":
    unittest.main()
