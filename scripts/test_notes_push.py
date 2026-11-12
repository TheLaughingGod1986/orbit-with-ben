#!/usr/bin/env python3
"""notes_push.py: the checks a board-notes push must pass, and a push that never overwrites someone else's notes."""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import types
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import notes_push as np  # noqa: E402


def note(**over):
    base = {"updated": "2026-11-10T10:00Z", "mood": "good", "line": "l", "done": "d", "holdup": "h",
            "steps": [{"who": "Mini", "what": "build", "job": "J1"}]}
    base.update(over)
    return base


def text(films):
    return np.canonical({"films": films})


class Problems(unittest.TestCase):
    def test_a_good_file_has_none(self):
        self.assertEqual(np.problems(text({"OWB:032": note()})), [])

    def test_broken_json(self):
        self.assertIn("not valid JSON", np.problems("{")[0])

    def test_other_formatting_is_refused(self):
        compact = json.dumps({"films": {"OWB:032": note()}})
        self.assertIn("board's form", np.problems(compact)[0])

    def test_no_films(self):
        self.assertIn("no 'films'", np.problems(np.canonical({"films": {}}))[0])

    def test_missing_field_names_the_film_and_the_field(self):
        bad = note()
        del bad["holdup"]
        self.assertEqual(np.problems(text({"OWB:032": bad})), ["OWB:032: missing holdup"])

    def test_unknown_mood(self):
        self.assertIn("mood 'happy'", np.problems(text({"OWB:032": note(mood="happy")}))[0])

    def test_step_must_say_when(self):
        found = np.problems(text({"OWB:032": note(steps=[{"who": "Mini", "what": "build"}])}))
        self.assertEqual(len(found), 1)
        self.assertIn("step 1 (build)", found[0])

    def test_step_needs_who_unless_its_kind_is_routed(self):
        step = {"kind": "review", "what": "review", "when": "today"}
        self.assertTrue(np.problems(text({"OWB:032": note(steps=[step])})))
        self.assertEqual(np.problems(text({"OWB:032": note(steps=[step])}), routed=("review",)), [])

    def test_the_real_file_passes(self):
        sys.path.insert(0, str(HERE))
        import kanban_snapshot
        self.assertEqual(np.problems(np.NOTES.read_text(), routed=tuple(kanban_snapshot.routing_doc())), [])


class WhichTests(unittest.TestCase):
    def test_found_by_what_they_read_not_by_a_list(self):
        with tempfile.TemporaryDirectory() as d:
            folder = pathlib.Path(d)
            (folder / "test_kanban_snapshot.py").write_text("pass\n")
            (folder / "test_reads.py").write_text("x = 'film_briefs.json'\n")
            (folder / "test_loads.py").write_text("ks.load_briefs()\n")
            (folder / "test_other.py").write_text("pass\n")
            for name in np.SKIP:
                (folder / name).write_text("film_briefs\n")
            names = [p.name for p in np.tests_that_read_notes(folder)]
        self.assertEqual(names, ["test_kanban_snapshot.py", "test_loads.py", "test_reads.py"])

    def test_the_snapshot_test_is_in_the_real_list(self):
        self.assertIn("test_kanban_snapshot.py", [p.name for p in np.tests_that_read_notes()])

    def test_failures_are_named(self):
        def runner(cmd, **kw):
            return types.SimpleNamespace(returncode=int("bad" in cmd[1]), stderr="boom", stdout="")
        with contextlib.redirect_stderr(io.StringIO()):
            failed = np.run_tests([pathlib.Path("test_ok.py"), pathlib.Path("test_bad.py")], runner=runner)
        self.assertEqual(failed, ["test_bad.py"])


class FakeStudio:
    """Stands in for studio.py: a notes file with a HEAD version, and a transaction that may move main first."""

    def __init__(self, notes, head, arrives=None, fail=None):
        self.notes, self.head, self.arrives, self.fail = notes, head, arrives, fail
        self.committed = None

    def git(self, *args):
        if args[0] == "status":
            return types.SimpleNamespace(returncode=0, stdout=" M notes\n" if self.notes.read_text() != self.head else "")
        if args[0] == "show":
            return types.SimpleNamespace(returncode=0, stdout=self.head)
        if args[0] == "checkout":
            self.notes.write_text(self.head)
            return types.SimpleNamespace(returncode=0, stdout="")
        raise AssertionError(args)

    def git_transaction(self, write, message):
        if self.fail:
            return None, self.fail
        if self.arrives is not None:  # someone else's notes landed on main before ours
            self.notes.write_text(self.arrives)
        out, err, paths = write()
        if err:
            return out, err
        self.committed = self.notes.read_text()
        return out, None


class Push(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.tmp = pathlib.Path(self.dir.name) / "film_briefs.json"

    def push(self, studio):
        # the temp file is outside the repo; point ROOT at its folder so push() can name it
        orig, np.ROOT = np.ROOT, self.tmp.parent
        try:
            return np.push("notes: test", studio=studio, notes=self.tmp)
        finally:
            np.ROOT = orig

    def test_nothing_changed_nothing_pushed(self):
        self.tmp.write_text("old")
        s = FakeStudio(self.tmp, head="old")
        self.assertIsNone(self.push(s))
        self.assertIsNone(s.committed)

    def test_an_edit_is_committed(self):
        self.tmp.write_text("new")
        s = FakeStudio(self.tmp, head="old")
        self.assertIsNone(self.push(s))
        self.assertEqual(s.committed, "new")

    def test_someone_elses_notes_are_never_overwritten(self):
        self.tmp.write_text("mine")
        s = FakeStudio(self.tmp, head="old", arrives="theirs")
        err = self.push(s)
        self.assertIn("changed on main", err)
        self.assertIsNone(s.committed)
        self.assertEqual(self.tmp.read_text(), "mine")  # the edit is handed back, not lost

    def test_a_refused_transaction_hands_the_edit_back(self):
        self.tmp.write_text("mine")
        s = FakeStudio(self.tmp, head="old", fail="metadata --git requires clean main; worker branch unchanged")
        self.assertIn("clean main", self.push(s))
        self.assertEqual(self.tmp.read_text(), "mine")


if __name__ == "__main__":
    unittest.main()
