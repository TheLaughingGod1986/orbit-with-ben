"""J3357: soft pin outage recovery and one alarm per observed idle spell."""
import datetime as dt
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chief_relay as cr
import machines

AT = dt.datetime(2026, 11, 22, 12, tzinfo=dt.timezone.utc)


class Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        for name, value in (("STATE", root / "state"), ("STUDIO", root / "repo")):
            patch = mock.patch.object(cr, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        cr.STATE.mkdir()
        self.job = {"id": "J1", "status": "open", "for": "codex", "kind": "chart", "needs": "any"}
        self.data = {"jobs": [self.job]}
        cr.write_json(cr.STUDIO / "jobs/queue.json", self.data)
        patch = mock.patch.object(cr, "worker_capabilities", return_value={})
        patch.start()
        self.addCleanup(patch.stop)

    def down(self, since=AT, until=None):
        cr.write_json(cr.d("down/codex.json"), {"since": cr.iso(since), "until": cr.iso(until or AT + dt.timedelta(days=1)), "reason": "weekly usage limit"})

    def recover(self, at=AT):
        return cr.recover_pinned_jobs(self.data, at, {"cursor", "gemini"}, {})

    def test_soft_pin_opens_after_two_hours(self):
        self.down()
        self.assertEqual(self.recover(), [])
        self.assertEqual(self.recover(AT + dt.timedelta(minutes=119)), [])
        moves = self.recover(AT + dt.timedelta(hours=2))
        self.assertEqual(moves[0][0]["id"], "J1")
        self.assertEqual(moves[0][1][0], "cursor")
        with mock.patch.object(cr, "workers_up", return_value={"cursor", "gemini"}), mock.patch.object(cr, "claude_out", return_value=(False, "")), mock.patch.object(cr, "hand_back_claude"), mock.patch.object(cr, "stalled_claims", return_value=[]), mock.patch.object(cr, "reroute", return_value=True) as reroute, mock.patch.object(cr, "notify"), mock.patch.object(cr, "log"):
            cr.reroute_work(AT + dt.timedelta(hours=2))
            self.assertTrue(reroute.call_args.kwargs["open_claim"])
            self.assertIn("weekly usage limit", reroute.call_args.args[3])

    def test_pin_reopens_even_when_other_lanes_are_temporarily_down(self):
        self.down(AT - dt.timedelta(hours=3))
        moves = cr.recover_pinned_jobs(self.data, AT, set(), {})
        self.assertEqual(moves[0][1][0], "cursor")

    def test_hard_pin_stays_and_is_listed(self):
        self.down(AT - dt.timedelta(hours=3))
        self.job["pin_hard"] = True
        self.assertEqual(self.recover(), [])
        self.assertIn("J1", cr.read_json(cr.d("hard-pins.json"))["jobs"][0])
        self.job["rerouted_from"] = {"for": "claude"}
        self.assertEqual(cr.stranded_jobs(self.data, {"cursor"}, AT), [])

    def test_reset_after_deadline_opens_early(self):
        self.down()
        self.job["due"] = cr.iso(AT + dt.timedelta(hours=1))
        self.assertEqual(len(self.recover()), 1)

    def test_holds_dependencies_and_chief_pins_are_preserved(self):
        self.down(AT - dt.timedelta(hours=3))
        for field, value in (("hold", {"condition": "wait for credit"}), ("after", "missing"), ("kind", "chief"), ("cloud_only", True)):
            with self.subTest(field=field):
                before = dict(self.job)
                self.job[field] = value
                self.assertEqual(self.recover(), [])
                self.job.clear()
                self.job.update(before)

    def test_credit_flag_without_since_uses_durable_observation(self):
        cr.write_json(cr.STUDIO / "scripts/credit_flags.json", {"flags": {"codex": {"out_until": cr.iso(AT + dt.timedelta(days=1)), "reason": "limit"}}})
        self.assertEqual(self.recover(), [])
        self.assertEqual(len(self.recover(AT + dt.timedelta(hours=2))), 1)
        cr.write_json(cr.STUDIO / "scripts/credit_flags.json", {"flags": {}})
        self.assertEqual(self.recover(AT + dt.timedelta(hours=3)), [])
        self.assertEqual(cr.read_json(cr.d("pinned-outages.json")), {})

    def test_claudecode_honors_claude_usage_flag(self):
        self.job.update({"for": "claudecode", "kind": "assembly"})
        cr.write_json(cr.STUDIO / "scripts/credit_flags.json", {"flags": {"claude": {"out_until": cr.iso(AT + dt.timedelta(days=1)), "reason": "usage"}}})
        self.assertEqual(self.recover(), [])
        self.assertTrue(self.recover(AT + dt.timedelta(hours=2)))

    def test_idle_alarm_once_per_spell_and_board_payload(self):
        self.down()
        with mock.patch.object(cr, "current_executions", return_value=[]) as running, mock.patch.object(cr, "workers_up", return_value={"cursor"}), mock.patch.object(cr, "notify", return_value=True) as post, mock.patch.object(cr, "log"):
            cr.check_idle_alarm(AT)
            cr.check_idle_alarm(AT + dt.timedelta(minutes=29))
            post.assert_not_called()
            cr.check_idle_alarm(AT + dt.timedelta(minutes=30))
            cr.check_idle_alarm(AT + dt.timedelta(minutes=40))
            post.assert_called_once()
            self.assertIn("J1: pinned to codex", post.call_args.args[0])
            hb = cr.heartbeat_doc(AT, "idle")
            mini = machines.section(self.data, hb, None, AT)["machines"][0]
            self.assertIn("J1", mini["idleAlarm"]["message"])
            running.return_value = [{"job": "J2"}]
            cr.check_idle_alarm(AT + dt.timedelta(minutes=41))
            self.assertEqual(cr.read_json(cr.d("idle-alarm.json")), {})
            running.return_value = []
            cr.check_idle_alarm(AT + dt.timedelta(minutes=42))
            cr.check_idle_alarm(AT + dt.timedelta(minutes=72))
            self.assertEqual(post.call_count, 2)

    def test_no_open_work_clears_alarm(self):
        cr.write_json(cr.d("idle-alarm.json"), {"since": cr.iso(AT), "message": "old"})
        cr.write_json(cr.STUDIO / "jobs/queue.json", {"jobs": []})
        with mock.patch.object(cr, "current_executions", return_value=[]):
            cr.check_idle_alarm(AT)
        self.assertEqual(cr.read_json(cr.d("idle-alarm.json")), {})


if __name__ == "__main__":
    unittest.main()
