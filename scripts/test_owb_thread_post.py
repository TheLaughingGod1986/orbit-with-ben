"""A thread post must be a report, not what the shell made of one (11 Nov 2026).

A worker passed its report on the command line. The markdown backticks in it ran as commands, and 35 KB of
the Mini's environment, with a local session token, was posted on the public thread. These tests keep
`post` refusing that, and keep the briefs telling every worker to post from a file.
"""
import pathlib
import subprocess
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import owb_thread  # noqa: E402

ENV_DUMP = "\n".join(f"VAR_{i}=/some/value/{i}" for i in range(40))


class WhatPostRefuses(unittest.TestCase):
    def test_a_short_line_and_a_report_from_a_file_pass(self):
        self.assertIsNone(owb_thread.unsafe_post("[Claude] acting Chief: one line", from_file=False))
        report = "[MacBook] J2452 done.\n" + "A line of the report.\n" * 400
        self.assertGreater(len(report), owb_thread.INLINE_LIMIT)
        self.assertIsNone(owb_thread.unsafe_post(report, from_file=True))

    def test_a_long_report_on_the_command_line_is_refused(self):
        why = owb_thread.unsafe_post("x" * (owb_thread.INLINE_LIMIT + 1), from_file=False)
        self.assertIn("post -f", why)
        self.assertIsNone(owb_thread.unsafe_post("x" * owb_thread.INLINE_LIMIT, from_file=False))

    def test_an_environment_dump_is_refused_from_a_file_too(self):
        for from_file in (False, True):
            with self.subTest(from_file=from_file):
                why = owb_thread.unsafe_post("[Gemini] J2511 done.\n" + ENV_DUMP, from_file=from_file)
                self.assertIn("shell environment", why)

    def test_a_report_with_a_few_settings_in_it_is_not_a_dump(self):
        report = "[Codex] gates:\nPASS cut1=2.8s vo_onset=0.09s\nHOS_REPO=/x was set\nSTUDIO_SCRATCH=/y was set\n"
        self.assertIsNone(owb_thread.unsafe_post(report, from_file=True))

    def test_more_than_one_comment_holds_is_refused(self):
        self.assertIn("too long", owb_thread.unsafe_post("line\n" * 20000, from_file=True))

    def test_the_command_refuses_before_it_talks_to_github(self):
        run = subprocess.run([sys.executable, str(HERE / "owb_thread.py"), "post", ENV_DUMP],
                             capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Refused", run.stderr)
        self.assertIn("Nothing was posted", run.stderr)


class WhatTheBriefsSay(unittest.TestCase):
    def test_every_worker_is_told_to_post_from_a_file(self):
        for name in ("chief_relay.py", "macbook_worker.py"):
            with self.subTest(script=name):
                src = (HERE / name).read_text()
                self.assertIn("owb_thread.py post -f <file>", src)
                self.assertNotIn('owb_thread.py post "', src)

    def test_the_rule_book_says_so(self):
        self.assertIn("owb_thread.py post -f <file>", (HERE.parent / "AGENTS.md").read_text())


if __name__ == "__main__":
    unittest.main()
