#!/usr/bin/env python3
"""Tests for scripts/channels.py, and the phase 1 rule: engine code asks channels.py instead of naming a channel
(docs/MULTI_CHANNEL_PLAN.md; Ben, 5 Nov 2026: "so we just plug in new channels")."""
import contextlib
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


def _here(slug):
    """Where a channel's content is on this machine: the studio's root while that channel is its home (today), its
    own checkout beside the studio once it is not (the layout the dry run of the move builds). The tests below that
    read real files ask here, so they hold in both."""
    return channels.checkout(slug)


class Loader(unittest.TestCase):
    def test_the_two_channels_in_order(self):
        self.assertEqual(channels.slugs(), ["owb", "hos"])
        self.assertIn(channels.home(), ("owb", None))       # None once the studio has a repo of its own
        self.assertEqual(channels.default(), "owb")         # ... and a job that names no channel is still Orbit's
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


class NoHomeChannel(unittest.TestCase):
    """J2621, 11 Nov 2026 (plan decision 1). Until now exactly one channel had to be the studio's home: its content
    lives in the studio's own root. That is optional now. With none, the studio's root holds no channel's content,
    every channel is read through its checkout, and the questions the engine asks still have an answer. These build
    that layout from made-up files, so they run the same today and after the move."""

    def apart(self, **section):
        """Today's channels with none of them home, and the registry's `studio` section as given."""
        base = tuple(dict(c, home=False) for c in channels._load())
        kept = {"prefix": "owb", "github": "someone/studio", "default_channel": "owb", **section}
        stack = contextlib.ExitStack()
        stack.enter_context(mock.patch.object(channels, "_load", lambda directory=None: base))
        stack.enter_context(mock.patch.object(channels, "_studio_section", lambda: kept))
        return stack

    def folder(self, tmp, homes):
        for slug in ("owb", "hos"):
            (pathlib.Path(tmp) / slug).mkdir()
            c = dict(json.loads(_file(slug).read_text()), home=slug in homes)
            (pathlib.Path(tmp) / slug / "channel.json").write_text(json.dumps(c))

    def test_no_channel_has_to_be_home_and_two_cannot_be(self):
        with tempfile.TemporaryDirectory() as t:
            self.folder(t, homes=())
            self.assertEqual([(c["slug"], bool(c.get("home"))) for c in channels._load(t)], [("owb", False), ("hos", False)])
        with tempfile.TemporaryDirectory() as t:
            self.folder(t, homes=("owb", "hos"))
            with self.assertRaisesRegex(ValueError, "at most one channel can be home"):
                channels._load(t)

    def test_the_registry_says_which_channel_is_home_not_the_channels_own_file(self):
        # A channel's settings file reads the same whichever studio it is plugged into. Here both files claim `home`
        # and the registry marks neither: neither is.
        with tempfile.TemporaryDirectory() as t:
            self.folder(t, homes=("owb", "hos"))
            (pathlib.Path(t) / "channels.json").write_text(json.dumps({"channels": [{"slug": "owb"}, {"slug": "hos"}]}))
            self.assertEqual([c["home"] for c in channels._load(t)], [False, False])

    def test_what_the_engine_asks_still_has_an_answer(self):
        with self.apart():
            self.assertIsNone(channels.home())
            self.assertIsNone(channels.studio_slug())
            self.assertEqual((channels.default(), channels.queue_key(), channels.home_label()), ("owb", "owb", "OWB"))
            self.assertEqual(channels.board_channel(), "owb")
            # a job's channel: its repo, then its title, then the default one, exactly as with a home channel
            self.assertEqual(channels.of_job({"repo": "hos", "title": "x"}), "hos")
            self.assertEqual(channels.of_job({"repo": "owb", "title": "HOS 013: Darwin"}), "hos")
            self.assertEqual(channels.of_job({"title": "033 shot list"}), "owb")
            self.assertEqual(channels.label_of_repo(None), "OWB")
            self.assertEqual((channels.studio_key(), channels.studio_name(), channels.studio_short()),
                             ("studio", "the studio", "studio"))
            self.assertEqual(channels.studio_github(), "someone/studio")
            self.assertEqual(channels.studio_repo(), {"url": "https://github.com/someone/studio.git", "env": "",
                                                      "checkouts": ["studio"]})
        with self.apart(name="Ben's studio", label="STUDIO", checkouts=["Studio"], env="STUDIO_REPO"):
            self.assertEqual((channels.studio_name(), channels.studio_short()), ("Ben's studio", "STUDIO"))
            with tempfile.TemporaryDirectory() as home, mock.patch.dict("os.environ", {"STUDIO_REPO": ""}):
                self.assertEqual(channels.studio_checkout(pathlib.Path(home)), pathlib.Path(home) / "YouTube" / "Studio")
            with mock.patch.dict("os.environ", {"STUDIO_REPO": "/elsewhere/s"}):
                self.assertEqual(channels.studio_checkout(), pathlib.Path("/elsewhere/s"))

    def test_the_default_channel_is_the_registrys_field_then_home_then_the_first(self):
        with self.apart(default_channel="hos"):
            self.assertEqual(channels.default(), "hos")
            self.assertEqual(channels.of_job({"title": "a job that names nothing"}), "hos")
        for missing in ({"default_channel": ""}, {"default_channel": "not-plugged-in"}):
            with self.apart(**missing):
                self.assertEqual(channels.default(), "owb")              # no home either: the first channel in order
        registry = json.loads((channels.DIR / "channels.json").read_text())
        self.assertEqual(registry["studio"]["default_channel"], "owb")   # the real registry names it
        if channels.home():
            self.assertEqual(channels.default(), channels.home())        # and until the move the two agree

    def test_every_channel_is_read_through_its_own_checkout(self):
        with tempfile.TemporaryDirectory() as t:
            where = {}
            for slug in ("owb", "hos"):
                where[slug] = pathlib.Path(t) / slug
                (where[slug] / "studio").mkdir(parents=True)
                (where[slug] / "studio" / "channel.json").write_text("{}")
            with self.apart(), mock.patch.object(channels, "repo_path", lambda slug, home_dir=None: where[slug]):
                for slug in ("owb", "hos"):
                    self.assertEqual(channels.checkout(slug), where[slug])            # never the studio's root
                    self.assertEqual(channels.analytics_dir(slug), where[slug] / "05_Analytics" / slug)
                    self.assertEqual(channels.uploads_file(slug),
                                     where[slug] / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json")
                self.assertEqual(channels.films_dir("owb"), where["owb"] / "02_Video-Projects")
                self.assertEqual(channels.of_path(where["hos"] / "anything"), "hos")
                self.assertEqual(channels.of_path(channels.ROOT / "scripts"), "owb")  # the studio's own files: the default
            # the studio's own records stay in the studio's root
            self.assertEqual(channels.studio_records("ai_spend", "ledger.jsonl"),
                             channels.ROOT / "05_Analytics" / "ai_spend" / "ledger.jsonl")


class OwnRepos(unittest.TestCase):
    """Phase 2: each channel's settings live in its own repo at studio/channel.json."""

    def test_a_channel_on_this_machine_is_read_from_its_own_studio_folder(self):
        self.assertEqual(_file("owb"), _here("owb") / "studio" / "channel.json")
        if channels.home():
            self.assertEqual(_here(channels.home()), channels.ROOT)   # the home channel's checkout is the studio's root

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

    def test_picture_route_takes_the_route_that_cannot_bill_when_channels_cannot_be_read(self):
        """10 Nov 2026: the fallback used to name a channel ('flow_only' for hos, else 'flow_first'). Not knowing the
        channel's route, a job must not be walked to priced Vertex."""
        import routing
        with mock.patch.object(channels, "slugs", side_effect=RuntimeError("channel file unreadable")):
            for repo in ("owb", "hos", "third"):
                self.assertEqual(routing._picture_route({"kind": "video", "repo": repo}), "flow_only")
                chain = routing.job_chain({"kind": "video", "repo": repo})
                self.assertTrue(chain and all(not m.startswith("veo-") for _, m in chain), repo)

    def test_a_bare_film_number_goes_to_the_jobs_own_channel_first_then_the_others(self):
        import progress24
        titles = {"OWB:031": "x", "HOS:009": "y", "OWB:009": "z"}
        self.assertEqual(progress24._bare_film_key("009", {"repo": "hos"}, titles), "HOS:009")
        self.assertEqual(progress24._bare_film_key("009", {"repo": "owb"}, titles), "OWB:009")
        self.assertEqual(progress24._bare_film_key("009", {}, titles), "OWB:009")                    # no repo: home first
        self.assertEqual(progress24._bare_film_key("031", {"repo": "hos"}, titles), "OWB:031")       # only the other has it
        self.assertEqual(progress24._bare_film_key("180", {"repo": "hos"}, titles), "")              # never invented
        self.assertEqual(progress24._bare_film_key("009", {"repo": "hos"}, None), "")

    def test_board_ticks_for_the_home_channel_are_read_by_its_label(self):
        import stage_sync
        oks = stage_sync.ben_oks({"OWB-024": {"verdict": "ok", "version": "v06", "at": "2026-10-22T09:17:55Z"},
                                  "HOS-007": {"verdict": "ok", "version": "v03", "at": "2026-10-25T10:00:00Z"},
                                  "OWB-025": {"verdict": "change", "at": "2026-10-23T10:00:00Z"}})
        self.assertEqual(list(oks), ["024"])
        self.assertIn("v06", oks["024"])

    def test_each_channels_numbers_and_uploads_register_are_asked_for_by_slug(self):
        # New engine code (the first-day check) asks here instead of writing a channel's folder into a path.
        # With a home channel every channel's numbers are a folder each in the studio's root; with none, each
        # channel keeps its own in its checkout.
        for slug in channels.slugs():
            base = channels.ROOT if channels.home() else _here(slug)
            self.assertEqual(channels.analytics_dir(slug), base / "05_Analytics" / slug)
            self.assertTrue((channels.analytics_dir(slug) / "snapshots").is_dir(), slug)
        own = channels.default()
        self.assertEqual(channels.uploads_file(own), _here(own) / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json")
        self.assertTrue(channels.uploads_file(own).is_file())

    def test_a_channel_whose_checkout_is_not_here_has_no_uploads_register(self):
        with mock.patch.object(channels, "checkout", return_value=None):
            self.assertIsNone(channels.uploads_file(channels.slugs()[-1]))

    def test_the_repair_script_covers_every_channels_checkout(self):
        import mini_repair
        self.assertEqual([p.name for p in mini_repair.REPOS],
                         [channels.repo_path(s, mini_repair.HOME).name for s in channels.slugs()])
        self.assertEqual(len(mini_repair.REPOS), len(channels.slugs()))


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


class TrackerAsksTheLoader(unittest.TestCase):
    """J2525: video_tracker.py names no channel. What it used to know by name it asks here."""

    def sky(self, **extra):
        base = channels._load()
        sky = dict(json.loads(_file("owb").read_text()), slug="sky", label="SKY", name="Night Sky", short="Sky",
                   home=False, order=3, title_match=r"\bSKY\b", repo={"env": "SKY_REPO", "checkouts": ["night-sky"]},
                   pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        sky.pop("shorts", None)
        sky.update(extra)
        return mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def test_the_label_for_a_repo_field(self):
        self.assertEqual(channels.label_of_repo("hos"), channels.label("hos"))
        self.assertEqual(channels.label_of_repo("HOS"), channels.label("hos"))
        for nothing in (None, "", "nowhere"):
            self.assertEqual(channels.label_of_repo(nothing), channels.home_label())
        # unlike of_job, a title is never read: a home-channel job that mentions the other channel stays the home's
        self.assertEqual(channels.label_of_repo(channels.home()), channels.home_label())

    def test_the_studio_slug_is_the_channel_whose_repo_carries_the_studio(self):
        # for code that must clone or pull the studio's repo (the MacBook worker): the home channel's while there is
        # one, the studio's own once there is not. Either way the loader gives its address.
        self.assertEqual(channels.studio_slug(), channels.home())
        self.assertEqual(channels.studio_repo()["url"], "https://github.com/" + channels.studio_github() + ".git")
        if channels.home():
            self.assertEqual(channels.studio_repo(), channels.get(channels.home())["repo"])
        with self.sky():
            self.assertEqual(channels.studio_slug(), channels.home())     # a third channel does not move it

    def test_planned_shorts_is_each_channels_own_setting(self):
        self.assertEqual((channels.planned_shorts("owb"), channels.planned_shorts("hos")), (2, 4))   # Ben, 7 Nov 2026
        with self.sky(shorts={"planned_per_long": 3}):
            self.assertEqual(channels.planned_shorts("sky"), 3)
            self.assertEqual(channels.planned_shorts("SKY"), 3)
        with self.sky():
            self.assertEqual(channels.planned_shorts("sky"), 0)       # names none, and has no cached copy

    def test_a_checkout_behind_main_takes_the_setting_from_the_cached_copy(self):
        # The Mini's checkout of a channel can sit on an old branch whose channel.json has no `shorts` yet. The board
        # must not lose that channel's planned Shorts for it.
        stale = tuple({k: v for k, v in c.items() if k != "shorts"} if c["slug"] == "hos" else c for c in channels._load())
        with mock.patch.object(channels, "_load", lambda directory=None: stale):
            self.assertEqual(channels.planned_shorts("hos"), 4)

    def test_a_third_channel_plans_its_own_shorts_from_its_own_document(self):
        import datetime as dt
        import video_tracker as vt
        doc = {"films": [{"id": "001", "title": "Orion", "air": "2027-01-10"}]}
        with self.sky(shorts={"planned_per_long": 3}):
            channels.key_re.cache_clear()
            try:
                out = vt.build_videos(briefs={}, jobs=[], checks={}, public={}, uploads={}, titles={}, overrides={},
                                      now=dt.datetime(2026, 11, 11, tzinfo=dt.timezone.utc), documents={"sky": doc})
                by_name = vt.build_videos(briefs={}, jobs=[], checks={}, public={}, uploads={}, titles={}, overrides={},
                                          now=dt.datetime(2026, 11, 11, tzinfo=dt.timezone.utc), sky=doc)
                with self.assertRaises(TypeError):
                    vt.build_videos(briefs={}, jobs=[], checks={}, nowhere=doc)
            finally:
                channels.key_re.cache_clear()
        cards = {v["key"]: v for v in out["videos"] if v["channel"] == "SKY"}
        self.assertEqual(sorted(cards), ["SKY:001", "SKY:001:S:planned-1", "SKY:001:S:planned-2", "SKY:001:S:planned-3"])
        self.assertEqual((cards["SKY:001"]["type"], cards["SKY:001"]["title"], cards["SKY:001"]["lane"]),
                         ("long", "Orion", "upcoming"))
        self.assertEqual([v["key"] for v in by_name["videos"]], [v["key"] for v in out["videos"]])

    def test_the_tracker_names_no_channel(self):
        import test_channel_ratchet as ratchet
        source = (pathlib.Path(channels.__file__).parent / "video_tracker.py").read_text()
        self.assertEqual((len(ratchet.channel_lines(source)), len(ratchet.home_lines(source))), (0, 0))


class ThirdChannelInTheForecasts(unittest.TestCase):
    """J2521: uat_outlook, video_progress and channel_balance take a made-up third channel from the registry."""

    def sky(self, **pipeline):
        base = channels._load()
        sky = dict(json.loads(_file("owb").read_text()), slug="sky", label="SKY", name="Night Sky", short="Sky",
                   home=False, order=3, title_match=r"\bSKY\b", stages=["script", "edit", "upload"], pipeline=pipeline,
                   repo={"env": "SKY_REPO", "checkouts": ["night-sky"]})
        return mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def repo(self, tmp, path, doc):
        import subprocess
        root = pathlib.Path(tmp)
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(json.dumps(doc))
        at = "2026-10-17T10:00:00Z"
        for args in (["init", "-q"], ["add", "."],
                     ["-c", "user.name=Test", "-c", "user.email=test@example.test", "commit", "-qm", "x"]):
            subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                           env={**__import__("os").environ, "GIT_AUTHOR_DATE": at, "GIT_COMMITTER_DATE": at})
        return root

    def test_the_loader_says_how_a_channel_keeps_its_films(self):
        self.assertEqual(channels.pipeline("owb")["kind"], "film_status")
        self.assertEqual(channels.pipeline("HOS")["kind"], "pipeline_json")
        with self.sky():
            self.assertEqual(channels.pipeline("sky"), {})

    def test_video_progress_reads_a_third_channels_past_by_its_pipeline_kind(self):
        import datetime as dt
        import video_progress as vp
        cutoff = dt.datetime(2026, 10, 18, tzinfo=dt.timezone.utc)
        with tempfile.TemporaryDirectory() as tmp, self.sky(kind="film_status", path="films/*/status.json"):
            root = self.repo(tmp, "films/001_Orion/status.json", {"film": "001", "stages": {"edit": {"state": "doing"}}})
            got = vp.historical_stages(root, "SKY", cutoff, {})
            self.assertEqual(got["films"]["SKY:001"]["stages"], {"edit": {"state": "doing"}})
            self.assertEqual([d["key"] for d in got["definitions"]], ["script", "edit", "upload"])
            self.assertAlmostEqual(got["definitions"][0]["weight"], 100 / 3)
        with tempfile.TemporaryDirectory() as tmp, self.sky(kind="pipeline_json", path="plan/PIPELINE.json"):
            root = self.repo(tmp, "plan/PIPELINE.json", {"stages": [{"key": "edit", "weight": 60}],
                                                         "films": [{"id": "002", "stages": {"edit": {"status": "done"}}}]})
            nowhere = pathlib.Path(tmp) / "absent"
            doc = vp.progress_document_all({"owb": nowhere, "hos": nowhere, "sky": root}, [], tmp,
                                           at=dt.datetime(2026, 10, 19, tzinfo=dt.timezone.utc))
            day = doc["periods"]["day"]["channels"]
            self.assertEqual(list(day), ["OWB", "HOS", "SKY"])
            self.assertEqual(day["SKY"]["films"]["SKY:002"]["stages"]["edit"]["status"], "done")
            self.assertEqual(day["SKY"]["definitions"], [{"key": "edit", "weight": 60}])
            self.assertFalse(day["OWB"]["available"])

    def test_uat_outlook_gives_a_third_channels_film_its_milestones(self):
        import datetime as dt
        import uat_outlook as uo
        now = dt.datetime(2026, 11, 2, 18, tzinfo=dt.timezone.utc)
        done = {key: {"state": "done"} for key in uo.PLAN}
        video = dict(key="SKY:001", channel="SKY", type="long", lane="progress")
        with self.sky(kind="pipeline_json", path="plan/PIPELINE.json"), \
                mock.patch.object(uo, "history_samples", return_value={}) as read:
            uo.attach_all([video], {"owb": [], "hos": {}, "sky": {"films": [{"id": "001", "stages": done}]}}, [], now)
            self.assertEqual(uo.film_records("SKY", {"films": [{"id": 7}]}), [("SKY:7", {"id": 7})])
        self.assertEqual(video["production"]["completed"], 9)
        self.assertIn(("plan/PIPELINE.json", "SKY"), [c.args[1:] for c in read.call_args_list])
        with self.sky(kind="film_status", path="films/*/status.json"):
            self.assertEqual(uo.film_records("sky", [{"film": "003"}]), [("SKY:003", {"film": "003"})])

    def test_channel_balance_takes_a_checkout_flag_for_each_channel_kept_elsewhere(self):
        import contextlib
        import io
        import channel_balance as cb
        import channel_films
        seen = {}
        with self.sky(kind="pipeline_json", path="plan/PIPELINE.json"), \
                mock.patch.dict(cb.NAMES, {"sky": "Night Sky"}), \
                mock.patch.object(channel_films, "films", side_effect=lambda slug, root=None: seen.update({slug: root}) or []), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cb.main(["--sky", "/tmp/sky", "--hos", "/tmp/h", "--today", "2026-10-09", "--json"]), 0)
            self.assertEqual(cb.priority([], [], T_BALANCE)["channels"].keys(), {"owb", "hos"})
        self.assertEqual(seen, {"owb": None, "hos": pathlib.Path("/tmp/h"), "sky": pathlib.Path("/tmp/sky")})
        self.assertEqual(set(json.loads(out.getvalue())["channels"]), {"owb", "hos", "sky"})


T_BALANCE = __import__("datetime").date(2026, 10, 9)


class StudioOwnRepo(unittest.TestCase):
    """What board_check.py asks instead of naming the repo that carries the board (J2522)."""

    def test_the_board_repo_and_its_github_name_come_from_the_home_channel(self):
        self.assertEqual(channels.studio_github(), "TheLaughingGod1986/orbit-with-ben")
        self.assertEqual(channels.home_label(), "OWB")
        repo = channels.studio_repo()             # the home channel's repo today, the studio's own after the move
        if repo["env"]:
            with mock.patch.dict("os.environ", {repo["env"]: "/somewhere/else"}):
                self.assertEqual(channels.studio_checkout(), pathlib.Path("/somewhere/else"))
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict("os.environ", {repo["env"] or "NO_SUCH_VARIABLE": ""}):
            self.assertEqual(channels.studio_checkout(pathlib.Path(tmp)), pathlib.Path(tmp) / "YouTube" / "orbit-with-ben")


class ThirdChannelInTheBoardCheck(unittest.TestCase):
    def test_a_third_pipeline_channel_gets_the_scheduled_read_back_check(self):
        import board_check
        base = channels._load()
        sky = dict(json.loads(_file("owb").read_text()), slug="sky", label="SKY", name="Night Sky", home=False,
                   order=3, title_match=r"\bSKY\b", pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        board = {"sky": {"films": [{"id": "001", "stages": {"scheduled": {"status": "done"}}}]},
                 "owb": {"films": [{"id": "002", "stages": {"scheduled": {"status": "done"}}}]},
                 "tracker": {"videos": [{"key": "SKY:001", "lane": "progress"}, {"key": "OWB:002", "lane": "progress"}]}}
        with mock.patch.object(channels, "_load", lambda directory=None: base + (sky,)):
            res = board_check.check([], board, site_status=lambda url, follow=True: 200, files={})
        self.assertEqual(res["problems"], ["SKY:001: scheduled in PIPELINE but the card is in progress; "
                                           "no YouTube read-back (add the long to SKY UPLOADS.json)"])


class NoHomeChannelInTheScripts(unittest.TestCase):
    """J2523: eight scripts stopped asking which channel this repo belongs to. They ask these instead."""

    def _with_sky(self):
        sky = dict(json.loads(_file("owb").read_text()), slug="sky", label="SKY", name="Night Sky", short="Sky",
                   home=False, order=3, title_match=r"\bSKY\b", uat_dir={"icloud": "SKY UAT"})
        base = channels._load()
        return mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def test_a_job_that_names_no_channel_gets_the_default_one(self):
        self.assertEqual(channels.default(), "owb")
        self.assertEqual(channels.queue_key(), "owb")   # where kanban_snapshot.py publishes the queue in board.json

    def test_the_studios_own_records_stay_where_they_were(self):
        root = HERE.parent
        self.assertEqual(channels.studio_records("ai_spend"), root / "05_Analytics" / "ai_spend")
        self.assertEqual(channels.studio_records("tests", "THUMB_LEDGER.json"),
                         root / "05_Analytics" / "tests" / "THUMB_LEDGER.json")
        import ai_spend
        import thumb_ledger
        self.assertEqual(ai_spend.LEDGER, root / "05_Analytics" / "ai_spend" / "ledger.jsonl")
        self.assertEqual(ai_spend.PLANS, root / "05_Analytics" / "ai_spend" / "plans.json")
        self.assertEqual(thumb_ledger.LEDGER, root / "05_Analytics" / "tests" / "THUMB_LEDGER.json")

    def test_a_path_belongs_to_the_channel_whose_checkout_holds_it(self):
        root = HERE.parent
        self.assertEqual(channels.of_path(root / "02_Video-Projects" / "033_X"), "owb")
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(channels.of_path(t), "owb")   # nobody's: the default channel
            sky_repo = pathlib.Path(t) / "night-sky"
            (sky_repo / "studio").mkdir(parents=True)
            (sky_repo / "studio" / "channel.json").write_text("{}")
            with self._with_sky(), mock.patch.object(
                    channels, "repo_path", lambda slug, home_dir=None: sky_repo if slug == "sky" else pathlib.Path(t) / "none"):
                self.assertEqual(channels.of_path(sky_repo / "02_Video-Projects" / "001_Orion"), "sky")
                self.assertEqual(channels.of_path(root / "02_Video-Projects"), "owb")

    def test_board_ticks_are_read_for_the_channel_asked_for(self):
        import stage_sync
        checks = {"OWB-024": {"verdict": "ok", "version": "v06", "at": "2026-10-22T09:17:55Z"},
                  "SKY-001": {"verdict": "ok", "version": "v02", "at": "2026-11-01T09:00:00Z"}}
        with self._with_sky():
            self.assertEqual(list(stage_sync.ben_oks(checks)), ["024"])
            self.assertEqual(stage_sync.ben_oks(checks, "sky"), {"001": "Ben OK v02 (2026-11-01)"})

    def test_a_bare_film_number_tries_the_jobs_own_channel_first(self):
        import progress24
        titles = {"OWB:001": "Moon", "SKY:001": "Orion", "SKY:002": "Lyra"}
        with self._with_sky():
            self.assertEqual(progress24._bare_film_key("001", {"repo": "sky"}, titles), "SKY:001")
            self.assertEqual(progress24._bare_film_key("001", {}, titles), "OWB:001")
            self.assertEqual(progress24._bare_film_key("002", {}, titles), "SKY:002")

    def test_the_queue_is_read_from_the_boards_queue_key(self):
        import progress24
        board = {channels.queue_key(): {"focus": ["OWB:033"], "jobs": [], "done": [{"id": "J1"}]}}
        self.assertEqual(progress24.board_focus(board), ["OWB:033"])
        self.assertEqual([j["id"] for j in progress24.jobs_done_all(board)], ["J1"])

    def test_the_voice_tools_are_found_in_a_channels_checkout(self):
        import ai_spend_daily
        self.assertEqual(ai_spend_daily.voice_tools(), HERE.parent / "04_Audio" / "tools")   # the studio's own copy
        with tempfile.TemporaryDirectory() as t:
            elsewhere = pathlib.Path(t) / "04_Audio" / "tools"
            elsewhere.mkdir(parents=True)
            (elsewhere / "el_auth.py").write_text("")
            with mock.patch.object(channels, "ROOT", pathlib.Path(t) / "bare-studio"), \
                    mock.patch.object(channels, "checkout", lambda slug: pathlib.Path(t)):
                self.assertEqual(ai_spend_daily.voice_tools(), elsewhere)     # ... else a channel's checkout
            with mock.patch.object(channels, "ROOT", pathlib.Path(t) / "bare-studio"), \
                    mock.patch.object(channels, "checkout", lambda slug: None):
                self.assertRaises(RuntimeError, ai_spend_daily.voice_tools)


class StudioRootHoldsNoChannelContent(unittest.TestCase):
    """J2619: jobs.py, workflow_state.py, workflow_handoffs.py, studio.py and routing.py take a film's folder and a
    job's channel from the loader, so they still work when the studio's own root holds no channel content."""

    def test_the_films_are_where_the_channel_is_checked_out(self):
        import studio
        root = _here("owb")           # the studio's root today; Orbit's own checkout once the two are apart
        self.assertEqual(channels.board_channel(), "owb")
        self.assertEqual(channels.films_dir("owb"), root / "02_Video-Projects")
        self.assertEqual(studio.FILMS, root / "02_Video-Projects")
        self.assertEqual(studio._board_name(), channels.name("owb"))

    def test_the_board_reads_films_from_the_channels_checkout_not_the_studios_root(self):
        import datetime as dt
        import jobs
        import studio
        import workflow_handoffs as handoffs
        with tempfile.TemporaryDirectory() as t:
            engine = pathlib.Path(t) / "studio-engine"          # the studio's own repo: scripts and jobs, no films
            (engine / "scripts").mkdir(parents=True)
            (engine / "jobs").mkdir()
            channel = pathlib.Path(t) / "channel-checkout"      # the channel's repo, somewhere else
            film = channel / "02_Video-Projects" / "033_Uranus"
            film.mkdir(parents=True)
            (film / "status.json").write_text(json.dumps(
                {"film": "033", "title": "Uranus", "air": "", "stages": {}, "claims": [], "next": ""}))
            self.assertFalse(any((engine / d).exists() for d in ("00_Brand", "02_Video-Projects", "05_Analytics")))
            with mock.patch.object(channels, "ROOT", engine), \
                    mock.patch.object(channels, "checkout", lambda slug: channel if slug == "owb" else None):
                films = studio._films()
                self.assertEqual(films, channel / "02_Video-Projects")
                with mock.patch.object(studio, "FILMS", films):
                    at = dt.datetime(2026, 11, 11, 15, 0, tzinfo=dt.timezone.utc)
                    job = {"id": "J1", "film": "033", "stage": "edit", "repo": "owb", "eta": "2026-11-11T16:00Z",
                           "title": "edit"}
                    self.assertTrue(jobs.on_board(job))
                    self.assertEqual(jobs.film_status_path(job), film / "status.json")
                    self.assertIsNone(jobs.board_claim(job, "cursor", at))
                    claims = json.loads((film / "status.json").read_text())["claims"]
                    self.assertEqual([(c["stage"], c["by"]) for c in claims], [("edit", "cursor")])
                    self.assertEqual([f for f, _ in handoffs.records(studio.FILMS)], ["033"])
                    self.assertIn("033", studio.render_md(studio.FILMS))

    def test_a_job_that_names_no_channel_is_still_the_default_channels(self):
        import jobs
        import routing
        import workflow_handoffs as handoffs
        self.assertTrue(jobs.on_board({"film": "033"}))                      # an old row with no repo
        self.assertFalse(jobs.on_board({"film": "013", "repo": "hos"}))      # keeps its films another way
        self.assertFalse(jobs.on_board({"film": "", "repo": "owb"}))
        self.assertEqual(routing._picture_route({}), routing._picture_route({"repo": channels.default()}))
        with tempfile.TemporaryDirectory() as t:
            wip = pathlib.Path(t) / "WIP.json"
            line = channels.wip_line(channels.board_channel())
            wip.write_text(json.dumps({line: ["OWB:041", "HOS:020"]}))
            self.assertEqual(handoffs.waiting_films(wip), {"041"})


class RuleFiles(unittest.TestCase):
    """J2577: the rule book is two files since J2527. Prompts ask here what to call them for a checkout."""

    def test_a_checkout_with_its_own_rules_is_told_both_files_in_order(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            self.assertEqual(channels.rule_files(root), ["AGENTS.md"])            # not split yet
            self.assertEqual(channels.rules_phrase(root), "AGENTS.md")
            (root / "studio").mkdir()
            (root / "studio" / "RULES.md").write_text("# rules\n")
            self.assertEqual(channels.rule_files(root), ["AGENTS.md", "studio/RULES.md"])
            self.assertEqual(channels.rules_phrase(str(root)), "AGENTS.md and then studio/RULES.md")
        self.assertEqual(channels.rule_files("/no/such/checkout"), ["AGENTS.md"])  # not on this machine

    def test_this_repo_has_both(self):
        self.assertTrue((channels.ROOT / "AGENTS.md").is_file())                # the studio's rules
        self.assertEqual(channels.rule_files(_here(channels.default())), ["AGENTS.md", "studio/RULES.md"])


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


class DeliveryAsksTheLoader(unittest.TestCase):
    """J2616: approved_deliver.py names no channel. The publishing slots and the TikTok rule it held by the two
    channels' names are each channel's own settings now."""

    def sky(self, **extra):
        base = channels._load()
        sky = {k: v for k, v in json.loads(_file("owb").read_text()).items() if k not in ("cadence", "social", "shorts")}
        sky.update(slug="sky", label="SKY", name="Night Sky", short="Sky", home=False, order=3, title_match=r"\bSKY\b",
                   repo={"env": "SKY_REPO", "checkouts": ["night-sky"]},
                   pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        sky.update(extra)
        return mock.patch.object(channels, "_load", lambda directory=None: base + (sky,))

    def test_the_locked_slots_are_the_ones_ben_set_on_7_nov_2026(self):
        # The table that was in approved_deliver.py until 11 Nov 2026, number for number: (weekday, hour, minute),
        # Mon=0 … Sun=6, London time, in the order they are filled. Changing a channel's days is Ben's call.
        self.assertEqual(channels.cadence("owb"), {"long": [(6, 18, 0), (2, 18, 0)],                        # Sun, Wed 18:00
                                                   "short": [(0, 11, 30), (2, 11, 30), (4, 11, 30), (5, 11, 30)]})  # Mon Wed Fri Sat
        self.assertEqual(channels.cadence("hos"), {"long": [(3, 18, 0)],                                    # Thu 18:00
                                                   "short": [(5, 11, 30), (4, 11, 30), (6, 11, 30), (1, 11, 30)]})  # Sat Fri Sun Tue
        self.assertEqual((channels.tiktok_by_buffer("owb"), channels.tiktok_by_buffer("hos")), (False, True))

    def test_a_third_channel_has_its_own_slots_or_none(self):
        with self.sky(cadence={"long": ["Fri 17:05"], "short": ["Tue 09:00", "Mon 23:59"]}, social={"tiktok": "buffer"}):
            self.assertEqual(channels.cadence("SKY"), {"long": [(4, 17, 5)], "short": [(1, 9, 0), (0, 23, 59)]})
            self.assertTrue(channels.tiktok_by_buffer("sky"))
        with self.sky(cadence={"long": ["Fri 17:05"]}, social={"tiktok": "browser"}):
            self.assertEqual(channels.cadence("sky"), {"long": [(4, 17, 5)], "short": []})
            self.assertFalse(channels.tiktok_by_buffer("sky"))
        with self.sky():
            self.assertEqual(channels.cadence("sky"), {})         # names none, and has no cached copy
            self.assertFalse(channels.tiktok_by_buffer("sky"))

    def test_a_slot_that_does_not_read_is_an_error_never_a_slot_quietly_dropped(self):
        for bad in ("Sunday 18:00", "Sun 6pm", "Sun 24:00", "sun 18:00", " Sun 18:00", [6, 18, 0], None):
            with self.sky(cadence={"long": ["Fri 17:00", bad]}):
                with self.assertRaises(ValueError, msg=repr(bad)):
                    channels.cadence("sky")

    def test_a_checkout_behind_main_takes_both_settings_from_the_cached_copy(self):
        # The same net as planned_shorts: a channel's checkout on an old branch has no `cadence` or `social` yet.
        # Its videos must not move to another channel's days for it.
        stale = tuple({k: v for k, v in c.items() if k not in ("cadence", "social")} if c["slug"] == "hos" else c
                      for c in channels._load())
        with mock.patch.object(channels, "_load", lambda directory=None: stale):
            self.assertEqual(channels.cadence("hos")["long"], [(3, 18, 0)])
            self.assertTrue(channels.tiktok_by_buffer("hos"))

    def test_a_channels_desk_comes_from_its_file_and_from_the_cached_copy_when_its_checkout_is_behind(self):
        # J2618: the relay's brief sends an agent to a channel's desk. On the Mini that channel's checkout can sit on
        # an old branch, with no `desk` in its file yet; the brief must not lose the desk for that.
        want = {"tool": "00_Brand/Channel-Setup/tools/hos_desk.py", "number": 180}
        self.assertEqual(channels.desk("hos"), want)
        self.assertEqual(channels.desk("owb"), {})
        stale = tuple({k: v for k, v in c.items() if k != "desk"} if c["slug"] == "hos" else c for c in channels._load())
        with mock.patch.object(channels, "_load", lambda directory=None: stale):
            self.assertEqual(channels.desk("hos"), want)
            self.assertEqual(channels.desk("owb"), {})

    def test_the_film_folder_can_be_asked_for_inside_another_copy_of_the_repo(self):
        self.assertEqual(channels.films_dir("owb", pathlib.Path("/elsewhere/o")), pathlib.Path("/elsewhere/o/02_Video-Projects"))
        self.assertEqual(channels.films_dir("owb"), _here("owb") / "02_Video-Projects")        # asked plainly: as before

    def test_the_delivery_tool_names_no_channel(self):
        import test_channel_ratchet as ratchet
        source = (pathlib.Path(channels.__file__).parent / "approved_deliver.py").read_text()
        self.assertEqual((len(ratchet.channel_lines(source)), len(ratchet.home_lines(source))), (0, 0))


class TheStudiosOwnName(unittest.TestCase):
    """J2620, 11 Nov 2026. Some names in the studio's code were never a channel's: the launchd labels, state files,
    log files and two environment variables carry the studio's own short name. They are read from the registry's
    `studio` section, so the studio's code spells no name and nothing on a machine is renamed."""

    def test_todays_names_are_the_ones_already_on_the_machines(self):
        self.assertEqual(channels.studio_prefix(), "owb")
        self.assertEqual(channels.studio_env("AGENT"), "OWB_AGENT")
        self.assertEqual(channels.studio_env("THREAD_PR"), "OWB_THREAD_PR")
        self.assertEqual(channels.studio_label("chief-relay"), "com.owb.chief-relay")

    def test_the_studios_own_launchd_jobs_are_shipped_under_that_label(self):
        root = pathlib.Path(channels.ROOT)
        for folder, job in (("scripts/mini", "chief-relay"), ("scripts/mini", "board-publish"),
                            ("scripts/macbook", "macbook-worker"), ("07_Content-Ops/launchd", "missed-runs"),
                            ("07_Content-Ops/launchd", "tab-janitor"), ("07_Content-Ops/launchd", "ai-spend-daily")):
            with self.subTest(job=job):
                self.assertTrue((root / folder / (channels.studio_label(job) + ".plist")).is_file())

    def test_the_name_comes_from_the_registry_and_nowhere_else(self):
        with tempfile.TemporaryDirectory() as t:
            (pathlib.Path(t) / "channels.json").write_text(json.dumps({"studio": {"prefix": "abc"}, "channels": []}))
            channels.studio_prefix.cache_clear()
            try:
                with mock.patch.object(channels, "DIR", pathlib.Path(t)):
                    self.assertEqual((channels.studio_prefix(), channels.studio_env("AGENT"), channels.studio_label("x")),
                                     ("abc", "ABC_AGENT", "com.abc.x"))
            finally:
                channels.studio_prefix.cache_clear()
        self.assertEqual(channels.studio_prefix(), "owb")

    def test_the_studios_repo_is_a_registry_field_and_agrees_with_the_home_channel_until_the_move(self):
        reg = json.loads((channels.DIR / "channels.json").read_text())["studio"]
        self.assertEqual(channels.studio_github(), reg["github"])
        if channels.home():
            self.assertEqual("https://github.com/" + reg["github"] + ".git", channels.get(channels.home())["repo"]["url"])

    def test_asking_for_the_studios_repo_needs_no_home_channel(self):
        with tempfile.TemporaryDirectory() as t:
            (pathlib.Path(t) / "channels.json").write_text(json.dumps(
                {"studio": {"prefix": "abc", "github": "someone/studio"}, "channels": []}))
            with mock.patch.object(channels, "DIR", pathlib.Path(t)), \
                    mock.patch.object(channels, "home", side_effect=AssertionError("asked which channel is home")):
                self.assertEqual(channels.studio_github(), "someone/studio")

    def test_a_registry_without_the_field_still_gives_the_home_channels_repo(self):
        with tempfile.TemporaryDirectory() as t:
            (pathlib.Path(t) / "channels.json").write_text(json.dumps({"studio": {"prefix": "abc"}, "channels": []}))
            with mock.patch.object(channels, "DIR", pathlib.Path(t)), \
                    mock.patch.object(channels, "home", return_value="x"), \
                    mock.patch.object(channels, "get", return_value={"repo": {"url": "https://github.com/a/b.git"}}):
                self.assertEqual(channels.studio_github(), "a/b")

    def test_the_small_scripts_spell_no_name(self):
        import test_channel_ratchet as ratchet
        counts = ratchet.counts()
        for name in ("studio_thread.py", "owb_thread.py", "missed_runs.py", "core_sync.py", "macbook_worker.py",
                     "nas_offload.py", "cdp_tabs.py", "routing.py", "uat_outlook.py"):
            with self.subTest(script=name):
                self.assertEqual(counts.get(name, 0), 0)


if __name__ == "__main__":
    unittest.main()
