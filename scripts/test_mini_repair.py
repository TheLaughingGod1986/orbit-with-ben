#!/usr/bin/env python3
"""Tests for scripts/mini_repair.py on throwaway git repos: a stuck shared checkout gets back to origin/main and
nothing local is lost (Ben, 14 Oct 2026)."""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mini_repair as mr  # noqa: E402


def sh(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}: {r.stderr}")
    return r.stdout.strip()


class Repos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = pathlib.Path(self.tmp.name)
        self.home = t / "home"
        self.home.mkdir()
        self._home = mr.HOME
        mr.HOME = self.home
        env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        os.environ.update(env)
        self.origin = t / "origin.git"
        sh(t, "init", "-q", "--bare", "-b", "main", str(self.origin))
        seed = t / "seed"
        sh(t, "clone", "-q", str(self.origin), str(seed))
        (seed / "a.txt").write_text("one\n")
        sh(seed, "add", "-A")
        sh(seed, "commit", "-qm", "one")
        sh(seed, "push", "-q", "origin", "HEAD:main")
        self.mini = t / "mini"
        sh(t, "clone", "-q", str(self.origin), str(self.mini))
        # main moves on: a new QA record (the kind that blocked the Mini's pull) and an edit
        (seed / "qa").mkdir()
        (seed / "qa" / "report_v04.json").write_text('{"upstream": true}\n')
        (seed / "a.txt").write_text("two\n")
        sh(seed, "add", "-A")
        sh(seed, "commit", "-qm", "two")
        sh(seed, "push", "-q", "origin", "HEAD:main")
        self.seed = seed

    def tearDown(self):
        mr.HOME = self._home
        self.tmp.cleanup()

    def test_untracked_file_that_blocks_the_pull_moves_to_rescue(self):
        (self.mini / "qa").mkdir()
        (self.mini / "qa" / "report_v04.json").write_text('{"local": true}\n')
        (self.mini / "notes.txt").write_text("unrelated local file\n")
        self.assertNotEqual(subprocess.run(["git", "pull", "-q", "--ff-only"], cwd=self.mini, capture_output=True).returncode, 0)
        dry = mr.unblock(self.mini, False, "2026-10-14")
        self.assertIn("would move 1 untracked file(s)", " ".join(dry["actions"]))
        self.assertTrue((self.mini / "qa" / "report_v04.json").read_text().startswith('{"local"'))   # dry run touched nothing
        res = mr.unblock(self.mini, True, "2026-10-14")
        self.assertTrue(res["ok"], res)
        self.assertEqual((self.mini / "a.txt").read_text(), "two\n")
        kept = self.home / "_desk" / "rescue" / "2026-10-14" / "mini" / "qa" / "report_v04.json"
        self.assertEqual(kept.read_text(), '{"local": true}\n')
        self.assertTrue((self.mini / "notes.txt").exists())   # untracked files that don't block stay put

    def test_tracked_edit_is_stashed_not_lost(self):
        (self.mini / "a.txt").write_text("local edit\n")
        res = mr.unblock(self.mini, True, "2026-10-14")
        self.assertTrue(res["ok"], res)
        self.assertEqual((self.mini / "a.txt").read_text(), "two\n")
        self.assertIn("mini_repair 2026-10-14", sh(self.mini, "stash", "list"))
        self.assertIn("local edit", sh(self.mini, "stash", "show", "-p"))

    def test_divergent_commits_go_to_a_rescue_branch_first(self):
        (self.mini / "b.txt").write_text("local commit\n")
        sh(self.mini, "add", "-A")
        sh(self.mini, "commit", "-qm", "local only")
        local = sh(self.mini, "rev-parse", "HEAD")
        res = mr.unblock(self.mini, True, "2026-10-14")
        self.assertTrue(res["ok"], res)
        self.assertEqual(sh(self.mini, "rev-parse", "HEAD"), sh(self.mini, "rev-parse", "origin/main"))
        self.assertEqual(sh(self.origin, "rev-parse", "refs/heads/rescue/mini-2026-10-14-mini"), local)

    def test_clean_checkout_just_fast_forwards(self):
        res = mr.unblock(self.mini, True, "2026-10-14")
        self.assertTrue(res["ok"])
        self.assertIn("fast-forwarded", " ".join(res["actions"]))
        self.assertTrue(mr.unblock(self.mini, True, "2026-10-14")["ok"])

    def test_not_on_main_is_left_alone(self):
        sh(self.mini, "switch", "-qc", "work")
        res = mr.unblock(self.mini, True, "2026-10-14")
        self.assertFalse(res["ok"])
        self.assertIn("left alone", res["actions"][0])

    def test_temp_worktrees_go_only_when_clean_and_pushed(self):
        sh(self.mini, "fetch", "-q", "origin")
        tmp = pathlib.Path(tempfile.mkdtemp(dir="/tmp"))
        clean, dirty, unpushed = tmp / "clean", tmp / "dirty", tmp / "unpushed"
        sh(self.mini, "worktree", "add", "-q", "--detach", str(clean), "origin/main")
        sh(self.mini, "worktree", "add", "-q", "--detach", str(dirty), "origin/main")
        (dirty / "a.txt").write_text("work in progress\n")
        sh(self.mini, "worktree", "add", "-q", "--detach", str(unpushed), "origin/main")
        (unpushed / "c.txt").write_text("c\n")
        sh(unpushed, "add", "-A")
        sh(unpushed, "commit", "-qm", "not pushed")
        try:
            got = {pathlib.Path(w["path"]).name: mr.removable(self.mini, w) for w in mr.worktrees(self.mini)}
            self.assertEqual(got["clean"], (True, "clean, everything pushed"))
            self.assertEqual(got["dirty"][0], False)
            self.assertEqual(got["unpushed"], (False, "has commits that aren't on origin"))
            rep = mr.repair(True, repos=[self.mini], do_caches=False, scan=False)
            self.assertFalse(clean.exists())
            self.assertTrue(dirty.exists() and unpushed.exists())
            self.assertTrue(rep["checkouts"][0]["ok"])
        finally:
            subprocess.run(["rm", "-rf", str(tmp)])


if __name__ == "__main__":
    unittest.main()
