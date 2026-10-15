"""core_sync.py: shared files stay identical in both repos; a one-repo edit fails the check."""
import json, pathlib, sys, tempfile, unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import core_sync as cs  # noqa: E402


class CoreSync(unittest.TestCase):
    def setUp(self):
        self.a = pathlib.Path(tempfile.mkdtemp())
        (self.a / "lib").mkdir()
        (self.a / "lib" / "x.ts").write_text("export const x = 1;\n")
        self.data = {"files": {"lib/x.ts": cs.sha(self.a / "lib" / "x.ts")}}

    def test_matching_file_passes(self):
        self.assertEqual(cs.problems(self.a, self.data), [])

    def test_edit_in_one_repo_is_drift(self):
        (self.a / "lib" / "x.ts").write_text("export const x = 2;\n")
        self.assertEqual(cs.problems(self.a, self.data), ["changed  lib/x.ts"])

    def test_missing_file_is_drift(self):
        (self.a / "lib" / "x.ts").unlink()
        self.assertEqual(cs.problems(self.a, self.data), ["missing  lib/x.ts"])

    def test_this_repo_matches_its_lock(self):
        self.assertEqual(cs.problems(cs.ROOT, cs.load()), [])

    def test_channel_rules_are_never_core(self):
        never = ("AGENTS.md", "THUMBNAIL_AND_TITLE_RULES.md", "STUDIO_PLAYBOOK.md", "HOS_STRATEGY.md",
                 "FAMILIAR_DANGER_STRATEGY.md", "CHANNEL_META.json", "hos-contract")
        for rel in cs.load()["files"]:
            self.assertFalse(any(n in rel for n in never), rel)


if __name__ == "__main__":
    unittest.main()
