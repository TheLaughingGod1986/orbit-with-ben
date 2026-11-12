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
import studio_thread  # noqa: E402

ENV_DUMP = "\n".join(f"VAR_{i}=/some/value/{i}" for i in range(40))


class WhatPostRefuses(unittest.TestCase):
    def test_a_short_line_and_a_report_from_a_file_pass(self):
        self.assertIsNone(studio_thread.unsafe_post("[Claude] acting Chief: one line", from_file=False))
        report = "[MacBook] J2452 done.\n" + "A line of the report.\n" * 400
        self.assertGreater(len(report), studio_thread.INLINE_LIMIT)
        self.assertIsNone(studio_thread.unsafe_post(report, from_file=True))

    def test_a_long_report_on_the_command_line_is_refused(self):
        why = studio_thread.unsafe_post("x" * (studio_thread.INLINE_LIMIT + 1), from_file=False)
        self.assertIn("post -f", why)
        self.assertIsNone(studio_thread.unsafe_post("x" * studio_thread.INLINE_LIMIT, from_file=False))

    def test_an_environment_dump_is_refused_from_a_file_too(self):
        for from_file in (False, True):
            with self.subTest(from_file=from_file):
                why = studio_thread.unsafe_post("[Gemini] J2511 done.\n" + ENV_DUMP, from_file=from_file)
                self.assertIn("shell environment", why)

    def test_a_report_with_a_few_settings_in_it_is_not_a_dump(self):
        report = "[Codex] gates:\nPASS cut1=2.8s vo_onset=0.09s\nHOS_REPO=/x was set\nSTUDIO_SCRATCH=/y was set\n"
        self.assertIsNone(studio_thread.unsafe_post(report, from_file=True))

    def test_more_than_one_comment_holds_is_refused(self):
        self.assertIn("too long", studio_thread.unsafe_post("line\n" * 20000, from_file=True))

    def test_the_command_refuses_before_it_talks_to_github(self):
        for name in ("studio_thread.py", "owb_thread.py"):          # the tool, and the same tool under its old name
            with self.subTest(command=name):
                run = subprocess.run([sys.executable, str(HERE / name), "post", ENV_DUMP],
                                     capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
                self.assertNotEqual(run.returncode, 0)
                self.assertIn("Refused", run.stderr)
                self.assertIn("Nothing was posted", run.stderr)


class TheOldNameIsTheSameTool(unittest.TestCase):
    """11 Nov 2026 (J2620): the tool moved to studio_thread.py so the studio's code names no channel. AGENTS.md, the
    relay's briefs and jobs already in the queue still say owb_thread.py, and they must keep working unchanged."""

    def test_importing_the_old_name_gives_the_very_same_module(self):
        import owb_thread
        self.assertIs(owb_thread, studio_thread)

    def test_the_old_command_takes_the_same_arguments(self):
        for name in ("studio_thread.py", "owb_thread.py"):
            with self.subTest(command=name):
                run = subprocess.run([sys.executable, str(HERE / name), "post", "--help"], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertIn("--re", run.stdout)
                self.assertIn("-f", run.stdout)

    def test_the_names_it_runs_under_are_todays(self):
        # Nothing on the Mini or the MacBook is renamed by reading these from the registry.
        self.assertEqual(studio_thread.REPO, "TheLaughingGod1986/orbit-with-ben")
        self.assertTrue(studio_thread.STATE.endswith("/.owb_thread_state"))
        src = (HERE / "studio_thread.py").read_text()
        self.assertIn('channels.studio_env("THREAD_PR")', src)
        self.assertIn('channels.studio_env("AGENT")', src)

    def test_a_post_is_still_signed_with_the_agent_the_relay_woke(self):
        import channels
        self.assertEqual(channels.studio_env("AGENT"), "OWB_AGENT")
        self.assertEqual(channels.studio_env("THREAD_PR"), "OWB_THREAD_PR")


class WhatTheBriefsSay(unittest.TestCase):
    # The tool is scripts/studio_thread.py; scripts/owb_thread.py is the same tool under its old name. A brief may
    # name either, and neither may be shown posting text from the command line.
    def test_every_worker_is_told_to_post_from_a_file(self):
        for name in ("chief_relay.py", "macbook_worker.py"):
            with self.subTest(script=name):
                src = (HERE / name).read_text()
                self.assertRegex(src, r"(?:owb|studio)_thread\.py post -f <file>")
                self.assertNotRegex(src, r'(?:owb|studio)_thread\.py post "')

    def test_every_name_a_brief_gives_the_tool_is_one_an_unattended_claude_run_may_use(self):
        # 11 Nov 2026: the MacBook brief began to say studio_thread.py while the project's pre-approved commands
        # named only owb_thread.py. An unattended Claude run would have stopped to ask, with nobody there to answer.
        import json
        import re
        allowed = json.loads((HERE.parent / ".claude" / "settings.json").read_text())["permissions"]["allow"]
        named = set()
        for name in ("chief_relay.py", "macbook_worker.py"):
            named |= set(re.findall(r"python3 scripts/(\w+_thread\.py) (?:post|read)", (HERE / name).read_text()))
        self.assertIn("studio_thread.py", named)
        for tool in sorted(named | {"owb_thread.py", "studio_thread.py"}):
            with self.subTest(tool=tool):
                self.assertIn(f"Bash(python3 scripts/{tool}:*)", allowed)

    def test_the_rule_book_says_so(self):
        self.assertIn("owb_thread.py post -f <file>", (HERE.parent / "AGENTS.md").read_text())


if __name__ == "__main__":
    unittest.main()
