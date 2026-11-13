#!/usr/bin/env python3
"""channel_check.py (what a repo needs before the studio can drive it) and channel_new.py (start one)."""
import json
import pathlib
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import channel_check as cc  # noqa: E402
import channel_new as cn  # noqa: E402
import channels  # noqa: E402
import test_email_ratchet  # noqa: E402

REGISTERED = [{"slug": "one", "label": "ONE", "order": 1}, {"slug": "two", "label": "TWO", "order": 2}]


def good(**over):
    c = cn.settings("deep-sea", "SEA", "Deep Sea Stories")
    c.update(over)
    return c


class Settings(unittest.TestCase):
    def test_a_fresh_channel_has_no_problems(self):
        self.assertEqual(cc.settings_problems(good()), [])

    def test_every_registered_channel_passes(self):
        for c in channels.all_channels():
            self.assertEqual(cc.settings_problems(c), [], c["slug"])

    def test_stages_can_be_names_or_objects_with_weights_owners_and_kinds(self):
        # J2622: a channel that gives each stage its weight, who it goes to and the kind of job it is.
        full = [{"key": "script", "label": "Script", "weight": 60, "owner": "Grok", "kind": "script"},
                {"key": "ben_ok", "label": "Ben's OK", "weight": 40, "owner": "Ben"}]
        for stages in (["script", "edit"], full, [{"key": "script"}, {"key": "edit"}], ["script", {"key": "edit", "kind": "assembly"}]):
            self.assertEqual(cc.settings_problems(good(stages=stages)), [], stages)
        self.assertEqual(cc.settings_problems(good(stages="from pipeline")), [])

    def test_a_stage_list_that_cannot_be_read_is_named(self):
        bad = {
            "two stages have the same name": ["script", {"key": "script"}],
            "every stage has one and they add up to 100": [{"key": "a", "weight": 60}, {"key": "b"}],
            "they add up to 100": [{"key": "a", "weight": 60}, {"key": "b", "weight": 30}],
            "add up to 100 ": [{"key": "a", "weight": 100}, {"key": "b", "weight": 0}],
            "a stage's `kind` is the kind of job it is": [{"key": "a", "kind": ""}, {"key": "b"}],
            "names, or objects with a `key`": [{"label": "No key"}, "edit"],
        }
        for says, stages in bad.items():
            problems = cc.settings_problems(good(stages=stages))
            self.assertTrue(any(says.strip() in line for line in problems), (says, problems))

    def test_each_bad_field_is_named(self):
        cases = {
            "slug": {"slug": "Deep Sea"}, "label": {"label": "sea"}, "name": {"name": " "},
            "repo": {"repo": {"url": "", "checkouts": []}}, "title_match": {"title_match": "("},
            "wip": {"wip": {"limit": 0, "line": "next_x"}}, "stages": {"stages": []},
            "pipeline": {"pipeline": {"kind": "spreadsheet", "path": "x"}}, "uat_dir": {"uat_dir": {}},
            "picture_route": {"picture_route": "anything"},
            "shorts.planned_per_long": {"shorts": {"planned_per_long": -1}},
        }
        for field, change in cases.items():
            found = cc.settings_problems(good(**change))
            self.assertEqual(len(found), 1, field)
            self.assertTrue(found[0].startswith(field + ":"), found[0])

    def test_the_two_optional_settings_are_checked_when_given(self):
        self.assertEqual(cc.settings_problems(good(youtube={"handle": "@x", "studio_port": "9224"}, nas_folder="deep-sea")), [])
        self.assertEqual(cc.settings_problems(good(youtube={"handle": "@x"})), [])  # no Studio browser yet
        found = cc.settings_problems(good(youtube={"studio_port": 9224}))
        self.assertTrue(found and found[0].startswith("youtube.studio_port:"))
        found = cc.settings_problems(good(nas_folder="films/deep-sea"))
        self.assertTrue(found and found[0].startswith("nas_folder:"))

    def test_a_true_or_false_is_not_a_wip_limit(self):
        self.assertTrue(cc.settings_problems(good(wip={"limit": True, "line": "next_x"})))

    def test_not_an_object(self):
        self.assertEqual(len(cc.settings_problems(["slug"])), 1)

    def test_publishing_slots_and_the_tiktok_setting_are_checked_when_given(self):
        ok = {"long": ["Sun 18:00", "Wed 18:00"], "short": ["Mon 11:30"]}
        self.assertEqual(cc.settings_problems(good(cadence=ok, social={"tiktok": "buffer"})), [])
        self.assertEqual(cc.settings_problems(good(cadence={"long": ["Thu 18:00"]}, social={})), [])
        for bad in ({"long": [[6, 18, 0]]}, {"long": ["Sunday 18:00"]}, {"long": ["Sun 24:00"]}, {"long": ["Sun 18:60"]},
                    {"long": ["sun 18:00"]}, {"long": "Sun 18:00"}, {"long": []}, {}, {"live": ["Sun 18:00"]}, ["Sun 18:00"]):
            found = cc.settings_problems(good(cadence=bad))
            self.assertEqual(len(found), 1, bad)
            self.assertTrue(found[0].startswith("cadence:"), found[0])
        found = cc.settings_problems(good(social={"tiktok": "browser"}))
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith("social.tiktok:"))

    def test_a_desk_is_checked_when_given(self):
        # J2618: the relay's brief is built from this, so a wrong shape would reach every agent on the Mini.
        self.assertEqual(cc.settings_problems(good(desk={"tool": "00_Brand/Channel-Setup/tools/hos_desk.py", "number": 180})), [])
        self.assertEqual(cc.settings_problems(good()), [])                      # most channels have none
        for bad in ({}, {"tool": "tools/desk.py"}, {"number": 180}, {"tool": "tools/desk.sh", "number": 1},
                    {"tool": "/abs/desk.py", "number": 1}, {"tool": "~/desk.py", "number": 1}, {"tool": "../desk.py", "number": 1},
                    {"tool": "tools/desk.py", "number": 0}, {"tool": "tools/desk.py", "number": "180"},
                    {"tool": "tools/desk.py", "number": True}, "tools/desk.py", ["tools/desk.py", 180]):
            found = cc.settings_problems(good(desk=bad))
            self.assertEqual(len(found), 1, bad)
            self.assertTrue(found[0].startswith("desk:"), found[0])

    def test_the_slot_pattern_is_the_loaders(self):
        self.assertEqual(cc.SLOT.pattern, channels.SLOT.pattern)

    def test_the_address_pattern_is_the_email_ratchets(self):
        self.assertEqual(cc.ADDRESS.pattern, test_email_ratchet.ADDRESS.pattern)


class Checkout(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = cn.create(pathlib.Path(self.dir.name), "deep-sea", "SEA", "Deep Sea Stories", registered=REGISTERED)

    def settings(self, **change):
        file = self.root / "studio" / "channel.json"
        c = json.loads(file.read_text())
        c.update(change)
        file.write_text(json.dumps(c))

    def test_a_new_channel_passes_and_only_lacks_its_github_address_and_its_publishing_days(self):
        must, todo = cc.check(self.root)
        self.assertEqual(must, [])
        self.assertEqual(len(todo), 2)
        self.assertIn("repo.url is empty", todo[0])
        self.assertTrue(todo[1].startswith("cadence:"))   # its days are Ben's call; nothing is made up for it
        self.settings(cadence={"long": ["Fri 17:00"]})
        self.assertEqual(len(cc.check(self.root)[1]), 1)

    def test_no_settings_file(self):
        (self.root / "studio" / "channel.json").unlink()
        must, todo = cc.check(self.root)
        self.assertIn("studio/channel.json is missing", must[0])
        self.assertEqual(todo, [])

    def test_settings_that_are_not_json(self):
        (self.root / "studio" / "channel.json").write_text("{")
        self.assertIn("not valid JSON", cc.check(self.root)[0][0])

    def test_the_films_folder_must_be_there(self):
        self.settings(pipeline={"kind": "film_status", "path": "films/*/status.json"})
        self.assertEqual(cc.check(self.root)[0], ["pipeline: the folder films/ is not in the checkout"])

    def test_a_broken_film_status_file_is_named(self):
        film = self.root / "02_Video-Projects" / "001_First"
        film.mkdir()
        (film / "status.json").write_text("{")
        self.assertEqual(cc.check(self.root)[0], ["pipeline: 02_Video-Projects/001_First/status.json: not valid JSON"])
        (film / "status.json").write_text('{"film": "001"}')
        self.assertEqual(cc.check(self.root)[0], ["pipeline: 02_Video-Projects/001_First/status.json: no `stages`"])
        (film / "status.json").write_text('{"film": "001", "stages": {}}')
        self.assertEqual(cc.check(self.root)[0], [])

    def test_one_pipeline_file_works_but_is_on_the_to_do_list(self):
        self.settings(pipeline={"kind": "pipeline_json", "path": "PIPELINE.json"})
        self.assertEqual(cc.check(self.root)[0], ["pipeline: PIPELINE.json is not in the checkout"])
        (self.root / "PIPELINE.json").write_text('{"films": []}')
        must, todo = cc.check(self.root)
        self.assertEqual(must, [])
        self.assertTrue(any("one status file per film" in t for t in todo))
        (self.root / "PIPELINE.json").write_text('{"movies": []}')
        self.assertEqual(cc.check(self.root)[0], ["pipeline: PIPELINE.json has no `films` list"])

    def test_an_email_address_under_studio_is_refused(self):
        (self.root / "studio" / "notes.md").write_text("signed in as someone" + "@" + "gmail.com\n")
        must, _ = cc.check(self.root)
        self.assertEqual(len(must), 1)
        self.assertIn("studio/notes.md holds a personal email address", must[0])
        self.assertNotIn("someone", must[0])  # the address itself is never repeated

    def test_what_is_still_to_do(self):
        (self.root / "studio" / "RULES.md").unlink()
        (self.root / "STATUS.md").write_text("generated\n")
        (self.root / "studio-core").mkdir()
        self.settings(repo={"url": "https://github.com/x/deep-sea.git", "checkouts": ["deep-sea"]})
        must, todo = cc.check(self.root)
        self.assertEqual(must, [])
        self.assertEqual(len(todo), 4)
        self.assertTrue(todo[0].startswith("studio/RULES.md"))
        self.assertIn("STATUS.md", todo[1])
        self.assertTrue(todo[2].startswith("studio-core/"))
        self.assertTrue(todo[3].startswith("cadence:"))

    def test_this_repo_can_be_driven(self):
        # Orbit's own checkout: the studio's root today, a folder beside it once the two are apart.
        self.assertEqual(cc.check(channels.checkout(channels.default()))[0], [])

    def test_the_report_says_which(self):
        self.assertIn("cannot drive it yet", cc.report("x", ["a"], []))
        self.assertIn("Still to do", cc.report("x", [], ["b"]))
        self.assertIn("Nothing left to do", cc.report("x", [], []))


class NewChannel(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.parent = pathlib.Path(self.dir.name)

    def test_the_folder_it_makes(self):
        root = cn.create(self.parent, "deep-sea", "SEA", "Deep Sea Stories", handle="@DeepSea", wip=3, registered=REGISTERED)
        files = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
        self.assertEqual(files, [".gitignore", "00_Brand/README.md", "02_Video-Projects/README.md", "README.md",
                                 "studio/RULES.md", "studio/channel.json"])
        c = json.loads((root / "studio" / "channel.json").read_text())
        self.assertEqual((c["slug"], c["label"], c["name"], c["order"], c["home"]), ("deep-sea", "SEA", "Deep Sea Stories", 3, False))
        self.assertEqual(c["wip"], {"limit": 3, "line": "next_deep_sea"})
        self.assertEqual(c["youtube"], {"handle": "@DeepSea"})
        self.assertEqual(c["picture_route"], "flow_only")  # a new channel starts on the route that cannot bill
        self.assertEqual(c["shorts"], {"planned_per_long": 0})  # and with no places held for Shorts
        self.assertEqual(c["repo"], {"url": "", "env": "SEA_REPO", "checkouts": ["deep-sea"]})
        self.assertEqual(c["nas_folder"], "deep-sea")  # its NAS folder is its slug

    def test_the_templates_blanks_are_filled_in(self):
        root = cn.create(self.parent, "deep-sea", "SEA", "Deep Sea Stories", registered=REGISTERED)
        for path in root.rglob("*.md"):
            self.assertNotIn("{{", path.read_text(), path.name)
        self.assertIn("# Deep Sea Stories", (root / "README.md").read_text())
        self.assertIn("SEA:012", (root / "README.md").read_text())
        self.assertIn("studio-live/deep-sea/", (root / "README.md").read_text())

    def test_media_and_secrets_are_ignored_from_the_start(self):
        root = cn.create(self.parent, "deep-sea", "SEA", "Deep Sea Stories", registered=REGISTERED)
        ignore = (root / ".gitignore").read_text()
        for line in ("**/*.mp4", "**/*.wav", "**/*.png", ".env"):
            self.assertIn(line, ignore)

    def test_its_title_match_finds_its_own_jobs_only(self):
        import re
        c = cn.settings("deep-sea", "SEA", "Deep Sea Stories")
        self.assertTrue(re.search(c["title_match"], "SEA 004: script", re.I))
        self.assertTrue(re.search(c["title_match"], "deep sea stories weekly audit", re.I))
        self.assertFalse(re.search(c["title_match"], "research the seabed", re.I))

    def test_a_taken_slug_or_label_is_refused_and_nothing_is_made(self):
        for slug, label in (("one", "NEW"), ("fresh", "TWO")):
            with self.assertRaises(ValueError):
                cn.create(self.parent, slug, label, "Name", registered=REGISTERED)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_a_bad_slug_is_refused_and_nothing_is_made(self):
        with self.assertRaises(ValueError):
            cn.create(self.parent, "Deep Sea", "SEA", "Deep Sea Stories", registered=REGISTERED)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_an_existing_folder_is_never_written_over(self):
        (self.parent / "deep-sea").mkdir()
        (self.parent / "deep-sea" / "keep.txt").write_text("mine")
        with self.assertRaises(ValueError):
            cn.create(self.parent, "deep-sea", "SEA", "Deep Sea Stories", registered=REGISTERED)
        self.assertEqual((self.parent / "deep-sea" / "keep.txt").read_text(), "mine")

    def test_the_command(self):
        import contextlib
        import io
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = cn.main(["deep-sea", "--label", "SEA", "--name", "Deep Sea Stories", "--into", str(self.parent)])
        self.assertEqual(rc, 0)
        self.assertIn("the studio can drive it", out.getvalue())
        self.assertIn('{"slug": "deep-sea", "env": "SEA_REPO", "checkouts": ["deep-sea"]}', out.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as again:
            self.assertEqual(cn.main(["deep-sea", "--label", "SEA", "--name", "Deep Sea Stories", "--into", str(self.parent)]), 1)
        self.assertIn("not made", again.getvalue())


class HomeCheckout(unittest.TestCase):
    def test_the_home_channels_checkout_is_this_repo(self):
        home = channels.home()
        for slug in channels.slugs():
            if slug == home:
                self.assertEqual(channels.checkout(slug), HERE.parent)
            else:                     # every other channel, and every channel once none is home, is somewhere else
                self.assertNotEqual(channels.checkout(slug), HERE.parent)

    def test_a_channel_whose_repo_is_not_here_has_none(self):
        with tempfile.TemporaryDirectory() as d:
            import os
            other = next(c for c in channels.all_channels() if not c.get("home") and c["repo"].get("env"))
            old = os.environ.get(other["repo"]["env"])
            os.environ[other["repo"]["env"]] = d
            try:
                self.assertIsNone(channels.checkout(other["slug"]))
            finally:
                if old is None:
                    del os.environ[other["repo"]["env"]]
                else:
                    os.environ[other["repo"]["env"]] = old


if __name__ == "__main__":
    unittest.main()
