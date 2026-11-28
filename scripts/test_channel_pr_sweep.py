"""channel_pr_sweep: the Chief's batch merge of channel PRs (25 Nov 2026 traps: duplicated Shorts, stitched scripts)."""
import json
import pathlib
import subprocess
import tempfile
import unittest

import channel_pr_sweep as sw

M = sw.MISSING


def run(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)


class Merge3(unittest.TestCase):
    def test_records_merge_by_id_and_newer_side_wins_a_clash(self):
        base = {"shorts": [{"id": "S1", "state": "queued"}], "title": "Old"}
        ours = {"shorts": [{"id": "S1", "state": "queued"}, {"id": "S2", "state": "queued"}], "title": "Ours"}
        theirs = {"shorts": [{"id": "S1", "state": "built", "version": "v01"}], "title": "Theirs"}
        out = sw.merge3(base, ours, theirs, theirs_newer=True)
        self.assertEqual(out["shorts"], [{"id": "S1", "state": "built", "version": "v01"}, {"id": "S2", "state": "queued"}])
        self.assertEqual(out["title"], "Theirs")
        self.assertEqual(sw.merge3(base, ours, theirs, theirs_newer=False)["title"], "Ours")
        self.assertEqual(sw.duplicate_ids(out), [])

    def test_plain_lists_union_and_additions_kept(self):
        self.assertEqual(sw.merge3(M, ["a"], ["b", "a"]), ["a", "b"])
        self.assertEqual(sw.merge3({}, {"x": 1}, {"y": 2}), {"x": 1, "y": 2})
        self.assertEqual(sw.duplicate_ids({"s": [{"id": "A"}, {"id": "A"}]}), ["A"])


class Sweep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.origin, self.repo = root / "origin.git", root / "work"
        run(root, "init", "-q", "--bare", "-b", "main", str(self.origin))
        run(root, "clone", "-q", str(self.origin), str(self.repo))
        for k, v in (("user.name", "t"), ("user.email", "t@example.invalid")):
            run(self.repo, "config", k, v)
        self.status = self.repo / "film" / "status.json"
        self.status.parent.mkdir()
        self.write({"title": "Film", "shorts": [{"id": "S1", "state": "queued"}, {"id": "S2", "state": "queued"}]})
        (self.repo / "film" / "SCRIPT.md").write_text("v00\n")
        self.commit("main", "base")
        run(self.repo, "push", "-q", "origin", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, doc):
        self.status.write_text(json.dumps(doc, indent=2) + "\n")

    def commit(self, branch, msg):
        run(self.repo, "add", "-A")
        run(self.repo, "commit", "-q", "-m", msg)

    def branch(self, name, edit):
        run(self.repo, "checkout", "-q", "-B", name, "origin/main")
        edit()
        self.commit(name, name)
        run(self.repo, "push", "-q", "origin", name)
        run(self.repo, "checkout", "-q", "main")

    def test_two_prs_on_one_record_and_one_script_merge_cleanly_and_push(self):
        def a():
            self.write({"title": "Film", "shorts": [{"id": "S1", "state": "built", "version": "v01"}, {"id": "S2", "state": "queued"}]})
            (self.repo / "film" / "SCRIPT.md").write_text("v01 draft\n")

        def b():
            self.write({"title": "Film", "shorts": [{"id": "S1", "state": "queued"}, {"id": "S2", "state": "built", "version": "v01"}]})
            (self.repo / "film" / "SCRIPT.md").write_text("v02 locked\n")
        self.branch("w/a", a)
        self.branch("w/b", b)
        res = sw.sweep(self.repo, [(1, "w/a"), (2, "w/b")], push=True, log=lambda *_: None)
        self.assertEqual((res["merged"], res["problems"], res["pushed"]), ([1, 2], [], True))
        doc = json.loads(self.status.read_text())
        self.assertEqual([(s["id"], s["state"]) for s in doc["shorts"]], [("S1", "built"), ("S2", "built")])
        self.assertEqual((self.repo / "film" / "SCRIPT.md").read_text(), "v02 locked\n")  # newer PR, not both
        self.assertIn("Merge pull request #2", subprocess.run(["git", "-C", str(self.origin), "log", "-1", "--format=%s", "main"],
                                                              capture_output=True, text=True).stdout)

    def test_rules_change_is_skipped_unless_allowed(self):
        def r():
            (self.repo / "studio").mkdir(exist_ok=True)
            (self.repo / "studio" / "RULES.md").write_text("new rule\n")
        self.branch("w/r", r)
        res = sw.sweep(self.repo, [(3, "w/r")], log=lambda *_: None)
        self.assertEqual(res["merged"], [])
        self.assertIn("studio/RULES.md", res["skipped"][0][1])
        self.assertEqual(sw.sweep(self.repo, [(3, "w/r")], allow_rules=True, log=lambda *_: None)["merged"], [3])

    def test_refuses_a_dirty_checkout(self):
        (self.repo / "stray.txt").write_text("x")
        with self.assertRaises(RuntimeError):
            sw.sweep(self.repo, [(1, "w/a")], log=lambda *_: None)


if __name__ == "__main__":
    unittest.main()
