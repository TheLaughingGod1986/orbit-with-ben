"""capability_probe: fresh known clips, graded answers, shell tools fail the probe; relay keeps a fresh probe."""
import datetime as dt
import json
import pathlib
import random
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import capability_probe as cp  # noqa: E402
import chief_relay as cr  # noqa: E402

T0 = dt.datetime(2026, 11, 5, 10, 0, tzinfo=dt.timezone.utc)
MEDIA = shutil.which("say") and shutil.which("ffmpeg")


def oracle(truth, tools=("read_file",), deaf=False, blind=False):
    """A fake worker that 'perceives' by being told the truth the probe stored."""
    def run(prompt, schema, cwd):
        if "transcript" in schema["properties"]:
            return ({"heard": not deaf, "transcript": "" if deaf else truth["phrase"]}, set(tools))
        if blind:
            return ({"watched": True, "direction": "left_to_right", "colours_in_order": ["red", "green", "blue"]}, set(tools))
        return ({"watched": True, "direction": truth["direction"], "colours_in_order": truth["order"]}, set(tools))
    return run


@unittest.skipUnless(MEDIA, "needs macOS say and ffmpeg")
class Probe(unittest.TestCase):
    def setUp(self):
        self.truth = {}
        self.mk_a, self.mk_v = cp.make_audio, cp.make_video

        def make_audio(d, rng):
            path, phrase = self.mk_a(d, rng)
            self.truth["phrase"] = phrase
            return path, phrase

        def make_video(d, rng):
            path, direction, order = self.mk_v(d, rng)
            self.truth.update(direction=direction, order=order)
            return path, direction, order
        cp.make_audio, cp.make_video = make_audio, make_video

    def tearDown(self):
        cp.make_audio, cp.make_video = self.mk_a, self.mk_v

    def test_a_worker_that_hears_and_watches_passes_both(self):
        available, evidence = cp.probe("gemini", oracle(self.truth), random.Random(1))
        self.assertEqual(available, ["audio_input", "moving_video_input"])
        self.assertIn("audio PASS", evidence)

    def test_a_wrong_motion_answer_fails_video_only(self):
        # 5 Nov 2026: agy heard the VO word for word but said a left-to-right square moved diagonally.
        rng = random.Random(7)
        available, evidence = cp.probe("gemini", oracle(self.truth, blind=True), rng)
        self.assertIn("audio_input", available)
        if (self.truth["direction"], self.truth["order"]) != ("left_to_right", ["red", "green", "blue"]):
            self.assertNotIn("moving_video_input", available)
            self.assertIn("video FAIL", evidence)

    def test_a_shell_tool_is_not_perception(self):
        available, evidence = cp.probe("gemini", oracle(self.truth, tools=("read_file", "run_command")), random.Random(2))
        self.assertEqual(available, [])
        self.assertIn("run_command", evidence)

    def test_not_hearing_fails_audio(self):
        available, _ = cp.probe("gemini", oracle(self.truth, deaf=True), random.Random(3))
        self.assertNotIn("audio_input", available)


class Grading(unittest.TestCase):
    def test_audio_match_ignores_case_and_punctuation(self):
        self.assertGreater(cp.audio_score("The violet kettle counted forty pebbles.", "the Violet kettle, counted forty pebbles"), 0.99)
        self.assertLess(cp.audio_score("The violet kettle counted forty pebbles.", "A quiet lantern beside the canal"), cp.AUDIO_PASS)
        self.assertLess(cp.audio_score("The violet kettle counted forty pebbles.", ""), cp.AUDIO_PASS)
        # 5 Nov 2026 live: agy really heard this one, with two slips
        self.assertGreaterEqual(cp.audio_score("The woollen teapot buried twelve pebbles beside the copper windmill.",
                                               "The woolen teapot buried twelve pebbles beside the copper wheel."), cp.AUDIO_PASS)


class RelayKeepsAFreshProbe(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.old = cr.STATE
        cr.STATE = self.tmp / "state"
        cr.d().mkdir(parents=True)

    def tearDown(self):
        cr.STATE = self.old
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_a_session_saying_none_does_not_wipe_a_fresh_probe(self):
        cr.record_capabilities("gemini", "audio_input", "probe: heard the clip", 60, T0, source="probe")
        cr.record_capabilities("gemini", "", "session start: no media probed", 30, T0 + dt.timedelta(minutes=5))
        rep = json.loads(cr.d("capabilities.json").read_text())["gemini"]
        self.assertEqual(rep["available"], ["audio_input"])
        self.assertEqual(rep["source"], "probe")
        self.assertIn("session start", rep["evidence"])

    def test_after_the_probe_expires_a_session_report_stands_and_keeps_last_shown(self):
        cr.record_capabilities("gemini", "audio_input", "probe: heard the clip", 60, T0, source="probe")
        cr.record_capabilities("gemini", "", "session start: none", 30, T0 + dt.timedelta(minutes=61))
        rep = json.loads(cr.d("capabilities.json").read_text())["gemini"]
        self.assertEqual(rep["available"], [])
        self.assertEqual(rep["last_shown"]["audio_input"], cr.iso(T0))


class RunnersCoverEveryMiniWorker(unittest.TestCase):
    def test_every_mini_worker_has_a_runner(self):
        import routing
        self.assertEqual(set(cp.RUNNERS), set(routing.MINI_WORKERS))

    def test_cursor_codex_and_claude_runners_parse_structured_replies_and_flag_shell_tools(self):
        from unittest.mock import MagicMock, patch
        cur_lines = "\n".join([
            json.dumps({"type": "tool_call", "tool_call": {"readToolCall": {}, "shellToolCall": {}, "toolCallId": "1"}}),
            json.dumps({"type": "result", "is_error": False, "result": '{"heard": true, "transcript": "hello"}'}),
        ])
        with patch.object(cp.subprocess, "run", return_value=MagicMock(returncode=0, stdout=cur_lines, stderr="")):
            ans, tools = cp.cursor_runner("p", cp.AUDIO_SCHEMA, "/tmp")
        self.assertEqual(ans, {"heard": True, "transcript": "hello"})
        self.assertEqual(tools, {"readToolCall", "shellToolCall"})
        self.assertEqual(set(tools) - cp.FILE_TOOLS, {"shellToolCall"})

        cl_lines = "\n".join([
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Read", "input": {}},
                {"type": "tool_use", "name": "StructuredOutput", "input": {"watched": False, "direction": "none", "colours_in_order": []}},
            ]}}),
            json.dumps({"type": "result", "is_error": False, "structured_output": {"watched": False, "direction": "none", "colours_in_order": []}}),
        ])
        with patch.object(cp.subprocess, "run", return_value=MagicMock(returncode=0, stdout=cl_lines, stderr="")):
            ans, tools = cp.claude_runner("p", cp.VIDEO_SCHEMA, "/tmp")
        self.assertEqual(ans["watched"], False)
        self.assertEqual(set(tools) - cp.FILE_TOOLS, set())

        cx_lines = "\n".join([
            json.dumps({"type": "item.completed", "item": {"type": "command_execution"}}),
            json.dumps({"type": "error", "message": "You hit your usage limit"}),
        ])
        with patch.object(cp.subprocess, "run", return_value=MagicMock(returncode=1, stdout=cx_lines, stderr="")):
            ans, tools = cp.codex_runner("p", cp.AUDIO_SCHEMA, "/tmp")
        self.assertIn("usage limit", ans["_error"])
        self.assertEqual(set(tools) - cp.FILE_TOOLS, {"command_execution"})


if __name__ == "__main__":
    unittest.main()
