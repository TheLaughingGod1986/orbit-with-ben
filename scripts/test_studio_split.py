#!/usr/bin/env python3
"""The dry run of the move (scripts/studio_split.py; Ben, 10 Nov 2026: "How can we get this project moving and
finished?"). It must place every file, count what the ratchet counts, never print a key, and change nothing real."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channels  # noqa: E402
import studio_split as split  # noqa: E402

ROOT = split.ROOT


class Routes(unittest.TestCase):
    def test_every_tracked_file_has_a_place(self):
        placed = split.plan(split.tracked(ROOT), channels.slugs(), split.resident(ROOT))
        self.assertEqual(placed["unrouted"], [])
        self.assertGreater(len(placed[split.STUDIO]), 500)

    def test_the_engine_the_queue_and_the_board_go_to_the_studio(self):
        slugs = ["aaa", "bbb"]
        for path in ("scripts/jobs.py", "jobs/queue.json", "JOBS.md", "channels/channels.json", "AGENTS.md",
                     ".github/workflows/rules-check.yml", "05_Analytics/kanban/board_site/build.py",
                     "05_Analytics/ai_spend/ledger.jsonl", "04_Audio/tools/vo_take.py", "07_Content-Ops/package.json"):
            self.assertEqual(split.route(path, slugs)[0], split.STUDIO, path)

    def test_a_channels_numbers_go_to_that_channel_and_content_stays_with_the_resident(self):
        slugs = ["aaa", "bbb"]
        self.assertEqual(split.route("05_Analytics/bbb/snapshots/2026-11-10.json", slugs)[0], "bbb")
        self.assertEqual(split.route("05_Analytics/ccc/x.json", slugs)[0], split.STUDIO)   # not a channel: the studio's
        for path in ("02_Video-Projects/001_X/status.json", "00_Brand/logo.png", "studio/channel.json", "_archive/x.md"):
            self.assertEqual(split.route(path, slugs)[0], split.HOME_CHANNEL, path)
        self.assertEqual(split.route("STATUS.md", slugs)[0], split.BUILT)
        self.assertIsNone(split.route("somewhere/new.txt", slugs))

    def test_a_file_both_need_is_in_both_and_shared_tools_are_not_split(self):
        placed = split.plan([".gitignore", "scripts/a.py", "02_Video-Projects/001_X/s.json"], ["aaa"], "aaa")
        self.assertIn(".gitignore", placed[split.STUDIO])
        self.assertIn(".gitignore", placed["aaa"])
        files, in_studio = set(split.tracked(ROOT)), set(split.plan(split.tracked(ROOT), channels.slugs(), split.resident(ROOT))[split.STUDIO])
        self.assertEqual([f for f in split.shared_tools(ROOT) if f in files and f not in in_studio], [])

    def test_with_no_home_channel_a_channels_file_has_no_place_in_the_studio(self):
        # The studio already in a repo of its own: channel content found there is listed, not filed under a channel.
        placed = split.plan([".gitignore", "scripts/a.py", "02_Video-Projects/001_X/s.json", "05_Analytics/aaa/x.json"], ["aaa"], None)
        self.assertEqual(placed[split.STUDIO], [".gitignore", "scripts/a.py"])
        self.assertEqual(placed["unrouted"], ["02_Video-Projects/001_X/s.json"])
        self.assertEqual(placed["aaa"], ["05_Analytics/aaa/x.json"])

    def test_the_script_names_no_channel_and_asks_for_no_home(self):
        import test_channel_ratchet as ratchet
        self.assertEqual(ratchet.counts().get("studio_split.py", 0), 0)
        self.assertEqual(ratchet.home_counts().get("studio_split.py", 0), 0)


class Gates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return name

    def test_a_key_is_named_by_file_and_never_printed(self):
        secret = "s" + "k-" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4"
        files = [self.write("scripts/tool.py", f'TOKEN = "{secret}"\n'), self.write("scripts/clean.py", "x = 1\n"),
                 self.write("docs/risk-and-task-notes-for-the-studio.md", "a disk-usage-report-of-2026-10-31-for-the-mini\n")]
        found = split.key_findings(self.root, files)
        self.assertEqual(found, ["scripts/tool.py: 1 key-shaped string"])
        self.assertNotIn(secret, "\n".join(found))

    def test_a_real_env_file_counts_and_an_example_does_not(self):
        files = [self.write("a/.env", "PROJECT=x\n"), self.write("a/.env.example", "KEY=\n"), self.write("b/.env.local", "A=1\n")]
        self.assertEqual(split.key_findings(self.root, files),
                         ["a/.env: a .env file that is not an example", "b/.env.local: a .env file that is not an example"])

    def test_a_web_apps_public_id_is_not_a_key(self):
        public = "AI" + "za" + "SyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q"
        files = [self.write("old/tool.py", f"key='firebase:authUser:{public}:[DEFAULT]'\n"),
                 self.write("old/real.py", f'API_KEY = "{public}"\n')]
        self.assertEqual(split.key_findings(self.root, files), ["old/real.py: 1 key-shaped string"])

    def test_every_key_shape_gets_past_the_quick_filter(self):
        # J2538: key_findings only runs the key patterns on a file that holds one of _KEY_PREFIXES. So every shape
        # must always carry one of them, or a key of that shape would be passed over unseen. A new shape needs a
        # sample here, and its fixed text in _KEY_PREFIXES.
        import re
        fill = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4"
        samples = (
            "s" + "k-" + fill[:28],
            "AI" + "za" + fill[:35],
            "gh" + "p_" + fill[:36],
            "github" + "_pat_" + fill[:40],
            "xo" + "xb-" + fill[:24],
            "-----BEGIN RSA PRIVATE " + "KEY-----",
            "ya" + "29." + fill[:32],
        )
        self.assertEqual(len(samples), len(split._KEY_SHAPES), "a key shape has no sample in this test")
        for n, ((shape, _word), sample) in enumerate(zip(split._KEY_SHAPES, samples)):
            with self.subTest(shape=n):
                self.assertTrue(re.fullmatch(shape, sample), "the sample is not of this shape")
                # The fixed text is in the pattern itself, outside any group, class or repeat: every match has it.
                plain = shape.replace("\\", "")
                held = [p for p in split._KEY_PREFIXES if p in plain]
                self.assertTrue(held, "no quick-filter string is part of this shape")
                self.assertTrue(any(
                    plain[:plain.index(p)].count("(") == plain[:plain.index(p)].count(")")
                    and plain[:plain.index(p)].count("[") == plain[:plain.index(p)].count("]")
                    and plain[plain.index(p) + len(p):][:1] not in ("?", "*", "{", "|")
                    and "|" not in plain[:plain.index(p)]
                    for p in held), "the quick-filter string is optional in this shape")
                self.assertTrue(any(p in sample for p in split._KEY_PREFIXES))
                name = self.write(f"scripts/shape_{n}.py", f'# notes\nVALUE = "{sample}"\n')
                self.assertEqual(split.key_findings(self.root, [name]), [f"{name}: 1 key-shaped string"])

    def test_addresses_are_counted_by_file(self):
        who = "someone" + "@" + "gmail.com"
        files = [self.write("jobs/a.md", f"sent from {who} and again {who}\n"), self.write("jobs/b.md", "the studio account\n")]
        found = split.address_files(self.root, files)
        self.assertEqual(found, ["jobs/a.md: 2 places"])
        self.assertNotIn(who, "\n".join(found))

    def test_failing_tests_are_grouped_by_file(self):
        out = ("ERROR: test_one (test_alpha.Thing.test_one)\n----\nFAIL: test_two (scripts.test_alpha.Thing.test_two)\n"
               "FAIL: test_three (test_beta.Other.test_three)\nOK: nothing\n")
        self.assertEqual(split.failing_tests(out), {"test_alpha.py": ["test_one", "test_two"], "test_beta.py": ["test_three"]})


class History(unittest.TestCase):
    def res(self, day, left, tests="run"):
        return {"at": f"{day}T05:00Z", "left": left, "commit": "abc", "counts": {}, "tests": tests}

    def test_one_line_a_day_and_the_streak_counts_passes_in_a_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "deep" / "history.jsonl"
            self.assertEqual(split.streak(log), 0)
            split.record(log, self.res("2026-11-10", 318))
            split.record(log, self.res("2026-11-11", 0))
            split.record(log, self.res("2026-11-12", 4))
            split.record(log, self.res("2026-11-12", 0))          # a later run the same day replaces that day's line
            split.record(log, self.res("2026-11-13", 0))
            rows = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual([r["day"] for r in rows], ["2026-11-10", "2026-11-11", "2026-11-12", "2026-11-13"])
            self.assertEqual(split.streak(log, dt.date(2026, 11, 13)), 3)
            self.assertEqual(split.streak(log, dt.date(2026, 11, 14)), 3)   # today not run yet: yesterday still counts
            self.assertEqual(split.streak(log, dt.date(2026, 11, 15)), 0)   # a missed day ends it
            split.record(log, self.res("2026-11-14", 0, tests="not run"))   # a pass without its tests is not a pass
            self.assertEqual(split.streak(log, dt.date(2026, 11, 14)), 0)


class WholeRun(unittest.TestCase):
    def test_it_agrees_with_the_ratchet_and_changes_nothing_real(self):
        import test_channel_ratchet as ratchet
        if split.resident(ROOT) is None:
            # Run inside the layout the dry run builds: no channel's content is here, so there is nothing to rehearse.
            with self.assertRaises(SystemExit) as stop:
                split.check(ROOT, tests=False)
            self.assertIn("already moved", str(stop.exception))
            return
        before = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True, text=True).stdout
        res = split.check(ROOT, tests=False)
        after = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True, text=True).stdout
        self.assertEqual(before, after)
        self.assertEqual(res["counts"]["names"], sum(ratchet.counts().values()))
        self.assertEqual(res["counts"]["home"], sum(ratchet.home_counts().values()))
        self.assertEqual(res["left"], sum(res["counts"].values()))
        self.assertEqual([g["key"] for g in res["groups"]], [k for k, _ in split.GROUPS])
        self.assertEqual(res["counts"]["unrouted"], 0)
        self.assertEqual(res["counts"]["keys"], 0, [g for g in res["groups"] if g["key"] == "keys"])
        text = split.report(res)
        self.assertIn(f"{res['left']} thing", text)
        one = split.report(dict(res, left=1))
        self.assertIn("1 thing still stops the move.", one)                 # one thing stops; two things stop
        self.assertIn("2 things still stop the move.", split.report(dict(res, left=2)))
        self.assertNotRegex(text, r"[A-Za-z0-9._%+-]+@(gmail|googlemail)\.com")

    def test_a_pass_says_so(self):
        res = {"at": "2026-11-20T05:00Z", "commit": "abc", "clean": True, "left": 0, "counts": {}, "groups": [],
               "tests": "run", "layout": {"studio": 10}}
        self.assertIn("PASS. Nothing stops the move.", split.report(res))

    def test_the_daily_run_records_itself_through_the_clean_main_transaction(self):
        import studio
        res = {"at": "2026-11-11T05:00Z", "commit": "abc", "clean": True, "left": 3, "counts": {"names": 3},
               "groups": [], "tests": "run", "layout": {}}
        with tempfile.TemporaryDirectory() as t:
            out, hist = Path(t) / "r" / "latest.json", Path(t) / "r" / "history.jsonl"
            seen = {}

            def transaction(write, message, tries=3):
                seen["message"] = message
                seen["paths"] = write()[2]
                return None, None
            with mock.patch.object(studio, "git_transaction", transaction):
                self.assertIsNone(split.save(res, out, hist, git=True))
            self.assertEqual(seen["message"], "dry run of the move: 3 left on 2026-11-11")
            self.assertEqual(seen["paths"], [out.resolve(), hist.resolve()])
            self.assertEqual(json.loads(out.read_text())["left"], 3)
            self.assertEqual(json.loads(hist.read_text())["day"], "2026-11-11")
            # a refusal (not on a clean main) comes back as words and nothing is claimed as recorded
            with mock.patch.object(studio, "git_transaction", lambda w, m, tries=3: (None, "requires clean main")):
                self.assertEqual(split.save(res, out, hist, git=True), "requires clean main")
            self.assertIn("nothing to commit", split.save(res, git=True))
            # without --git it only writes the files
            plain = Path(t) / "plain.jsonl"
            self.assertIsNone(split.save(res, None, plain))
            self.assertTrue(plain.is_file())

    def test_nothing_to_rehearse_once_no_channel_lives_here(self):
        with mock.patch.object(split, "resident", lambda root: None):
            self.assertRaises(SystemExit, split.check, ROOT, None, False)


class Isolation(unittest.TestCase):
    """Placing a channel's numbers into a linked checkout must write the scratch copy only (J2738)."""

    def test_placing_a_channels_numbers_does_not_write_through_to_its_checkout(self):
        home, slug = "owb", "hos"
        rels = {
            "file": "05_Analytics/hos/sample.json",
            "nested": "05_Analytics/hos/nested/inner.json",
            "dangling": "05_Analytics/hos/dangling.json",
            "source_link": "05_Analytics/hos/via_link.json",
            "same_target": "05_Analytics/hos/same_target.json",
        }
        original = b"ORIGINAL CHANNEL DATA\n"
        studio = b"STUDIO COPY\n"
        nested_original = b"ORIGINAL NESTED\n"
        nested_studio = b"STUDIO NESTED\n"
        link_body = b"LINK BODY\n"
        same_original = b"ORIGINAL SAME TARGET\n"

        def seal(path: Path) -> None:
            if path.is_symlink():
                return
            if path.is_dir():
                for child in list(path.iterdir()):
                    seal(child)
                path.chmod(0o555)
            else:
                path.chmod(0o444)

        def unseal(path: Path) -> None:
            if path.is_symlink() or not path.exists():
                return
            if path.is_dir():
                path.chmod(0o755)
                for child in list(path.iterdir()):
                    unseal(child)
            else:
                path.chmod(0o644)

        def digest(path: Path) -> str:
            return hashlib.sha256(path.read_bytes()).hexdigest()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real, source, scratch = root / "real", root / "source", root / "scratch"
            nested_store = root / "nested_store"
            body = root / "link_body"
            missing = root / "missing" / "dangling.json"
            nested_store.mkdir()
            (nested_store / "inner.json").write_bytes(nested_original)
            body.write_bytes(link_body)
            for rel, data in (("file", original), ("source_link", original), ("same_target", same_original)):
                path = real / rels[rel]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (real / "05_Analytics/hos/nested").symlink_to(nested_store, target_is_directory=True)
            (real / rels["dangling"]).symlink_to(missing)
            (real / "05_Analytics/hos/untouched.json").write_bytes(b"LEAVE THIS\n")
            for rel, data in (("file", studio), ("nested", nested_studio), ("dangling", b"STUDIO DANGLING\n")):
                path = source / rels[rel]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (source / rels["source_link"]).symlink_to(body)
            (source / rels["same_target"]).symlink_to(real / rels["same_target"])
            before = {name: digest(real / rels[name]) for name in ("file", "source_link", "same_target")}
            before["nested"] = digest(nested_store / "inner.json")
            before["link_body"] = digest(body)
            sealed = [real, nested_store, body]
            for path in sealed:
                seal(path)
            try:
                placed = {split.STUDIO: [], home: [], slug: list(rels.values())}
                folder = split.build(scratch, source, placed, home, {slug: real})[slug]
                scratch_file = folder / rels["file"]
                scratch_nested = folder / rels["nested"]
                scratch_dangling = folder / rels["dangling"]
                scratch_link = folder / rels["source_link"]
                scratch_same = folder / rels["same_target"]
                self.assertFalse(scratch_file.is_symlink())
                self.assertFalse(scratch_nested.is_symlink())
                self.assertFalse(scratch_dangling.is_symlink())
                self.assertEqual(scratch_file.read_bytes(), studio)
                self.assertEqual(scratch_nested.read_bytes(), nested_studio)
                self.assertEqual(scratch_dangling.read_bytes(), b"STUDIO DANGLING\n")
                self.assertNotEqual(scratch_file.resolve(), (real / rels["file"]).resolve())
                self.assertNotEqual(scratch_nested.resolve(), (nested_store / "inner.json").resolve())
                self.assertTrue(scratch_file.resolve().is_relative_to(scratch.resolve()))
                self.assertTrue(scratch_nested.resolve().is_relative_to(scratch.resolve()))
                self.assertTrue(scratch_dangling.resolve().is_relative_to(scratch.resolve()))
                self.assertFalse(missing.exists())
                self.assertTrue(scratch_link.is_symlink())
                self.assertEqual(os.readlink(scratch_link), os.readlink(source / rels["source_link"]))
                self.assertNotEqual(scratch_link.resolve(), (real / rels["source_link"]).resolve())
                self.assertTrue(scratch_same.is_symlink())
                self.assertEqual(scratch_same.resolve(), (real / rels["same_target"]).resolve())
                self.assertTrue((folder / "05_Analytics/hos/untouched.json").is_symlink())
                self.assertEqual(stat.S_IMODE((real / rels["file"]).stat().st_mode), 0o444)
                self.assertEqual(stat.S_IMODE((nested_store / "inner.json").stat().st_mode), 0o444)
                # A second place, after the scratch file is real, still writes the scratch copy.
                (source / rels["file"]).write_bytes(b"STUDIO COPY 2\n")
                (source / rels["nested"]).write_bytes(b"STUDIO NESTED 2\n")
                for rel in (rels["file"], rels["nested"], rels["dangling"], rels["source_link"], rels["same_target"]):
                    split._own_folder((folder / rel).parent, folder)
                    split._place(source / rel, folder / rel)
                self.assertEqual((folder / rels["file"]).read_bytes(), b"STUDIO COPY 2\n")
                self.assertEqual((folder / rels["nested"]).read_bytes(), b"STUDIO NESTED 2\n")
                self.assertFalse((folder / rels["file"]).is_symlink())
                self.assertFalse((folder / rels["nested"]).is_symlink())
                self.assertFalse(missing.exists())
                self.assertEqual(os.readlink(folder / rels["source_link"]), os.readlink(source / rels["source_link"]))
            finally:
                for path in sealed:
                    unseal(path)
            self.assertEqual(digest(real / rels["file"]), before["file"])
            self.assertEqual((real / rels["file"]).read_bytes(), original)
            self.assertEqual(digest(real / rels["source_link"]), before["source_link"])
            self.assertEqual((real / rels["source_link"]).read_bytes(), original)
            self.assertEqual(digest(real / rels["same_target"]), before["same_target"])
            self.assertEqual((real / rels["same_target"]).read_bytes(), same_original)
            self.assertEqual(digest(nested_store / "inner.json"), before["nested"])
            self.assertEqual((nested_store / "inner.json").read_bytes(), nested_original)
            self.assertEqual(digest(body), before["link_body"])
            self.assertEqual((real / "05_Analytics/hos/untouched.json").read_bytes(), b"LEAVE THIS\n")
            self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
