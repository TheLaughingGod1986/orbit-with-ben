"""capability_probe: fresh known clips, graded answers, shell tools fail the probe; relay keeps a fresh probe."""
import datetime as dt
import json
import pathlib
import random
import shutil
import tempfile
import unittest

import capability_probe as cp
import chief_relay as cr

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

    def test_after_the_probe_expires_a_session_report_stands(self):
        cr.record_capabilities("gemini", "audio_input", "probe: heard the clip", 60, T0, source="probe")
        cr.record_capabilities("gemini", "", "session start: none", 30, T0 + dt.timedelta(minutes=61))
        self.assertEqual(json.loads(cr.d("capabilities.json").read_text())["gemini"]["available"], [])


if __name__ == "__main__":
    unittest.main()
