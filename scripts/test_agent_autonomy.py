#!/usr/bin/env python3
"""J3265: an agent's own timer, skill pick, one next stage, one retry then one repair, desks per window."""
import datetime as dt
import json
import os
import pathlib
import plistlib
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import agent_autonomy as auto  # noqa: E402
import channels  # noqa: E402
import jobs  # noqa: E402
import machines  # noqa: E402
import routing  # noqa: E402
import workflow_state as workflow  # noqa: E402

AT = dt.datetime(2026, 11, 21, 1, 30, tzinfo=dt.timezone.utc)


def queue(*specs):
    data = {"next_id": 1, "jobs": []}
    for needs, title, extra in specs:
        extra = dict(extra)
        urgent = extra.pop("urgent", None)
        job = jobs.do_add(data, title=title, needs=needs, body="", by="claude", at=AT, **extra)
        if urgent:
            job["urgent"] = urgent
    return data


class Autonomy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = pathlib.Path(self.tmp.name)
        self.feed = self.state / "feed.jsonl"
        self.tracker = mock.patch("workflow_board.load_tracker", return_value={})
        self.tracker.start()

    def tearDown(self):
        self.tracker.stop()
        self.tmp.cleanup()

    def test_two_agents_never_claim_the_same_job(self):
        data = queue(("mini", "cut the picture", {"kind": "assembly", "film": "040", "stage": "picture"}),
                     ("mini", "check the facts", {"kind": "facts", "film": "041", "stage": "sources"}))
        got = {}

        def take(agent):
            got[agent] = auto.claim_next(data, agent, AT, self.state)

        threads = [threading.Thread(target=take, args=(agent,)) for agent in ("cursor", "gemini")]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual({got["cursor"]["id"], got["gemini"]["id"]}, {"J0001", "J0002"})
        self.assertEqual(got["cursor"]["by"], "cursor")
        self.assertEqual(got["gemini"]["by"], "gemini")
        alone = queue(("mini", "only one", {}))
        first = auto.claim_next(alone, "cursor", AT, self.state)
        second = auto.claim_next(alone, "gemini", AT, self.state)
        self.assertEqual(first["id"], "J0001")
        self.assertIsNone(second)

    def test_an_agent_never_runs_twice(self):
        self.assertTrue(auto.acquire_lease("cursor", AT, self.state))
        self.assertTrue(auto.lease_held("cursor", AT, self.state))
        self.assertFalse(auto.lease_held("gemini", AT, self.state))
        data = queue(("mini", "cut the picture", {"kind": "assembly", "film": "040", "stage": "picture"}))
        out = auto.tick("cursor", AT, self.state, data, lambda *_: (0, "", ""), feed=self.feed)
        self.assertEqual(out["reason"], "already running")
        self.assertEqual(data["jobs"][0]["status"], "open")
        self.assertTrue(auto.acquire_lease("cursor", AT, self.state))  # the same process may refresh
        auto.release_lease("cursor", self.state)
        self.assertFalse(auto.lease_held("cursor", AT, self.state))

    def test_the_mini_cap_and_memory_floor_hold_further_agents(self):
        for agent in ("cursor", "gemini", "claudecode"):
            self.assertTrue(auto.acquire_lease(agent, AT, self.state))
        self.assertEqual(auto.may_start("codex", AT, self.state, free_mb=8000), (False, "cap"))
        ok, why = auto.may_start("macbook", AT, self.state, free_mb=8000)
        self.assertTrue(ok, why)
        empty = pathlib.Path(self.tmp.name) / "other"
        self.assertEqual(auto.may_start("cursor", AT, empty, free_mb=100), (False, "memory"))
        self.assertEqual(auto.may_start("cursor", AT, empty, free_mb=4000)[0], True)

    def test_skill_only_breaks_ties_after_deadline_air_nearest_and_urgent(self):
        # Urgent still beats a skill match. Claude's kind is script; the urgent cut wins.
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}),
                     ("any", "Cut the pictures", {"kind": "assembly", "film": "041", "stage": "edit", "urgent": True}))
        self.assertEqual(jobs.do_next(data, "claude", {"cloud", "any"}, AT)["kind"], "assembly")
        # The same urgency: skill then prefers the kind that lists this agent first.
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}),
                     ("any", "Cut the pictures", {"kind": "assembly", "film": "041", "stage": "edit"}))
        self.assertEqual(jobs.do_next(data, "claude", {"cloud", "any"}, AT)["kind"], "script")
        data = queue(("mini", "Write the script", {"kind": "script", "film": "040", "stage": "script"}),
                     ("mini", "Cut the pictures", {"kind": "assembly", "film": "041", "stage": "edit"}))
        self.assertEqual(jobs.do_next(data, "cursor", {"mini"}, AT)["kind"], "assembly")
        data = queue(("mini", "Write the script", {"kind": "script", "film": "040", "stage": "script"}),
                     ("mini", "Watch the plates", {"kind": "image", "film": "041", "stage": "picture"}))
        self.assertEqual(jobs.do_next(data, "gemini", {"mini"}, AT)["kind"], "image")
        # Two jobs of the same kind: urgent still wins, skill does not reorder them.
        data = queue(("mini", "later cut", {"kind": "assembly", "film": "040", "stage": "edit"}),
                     ("mini", "due cut", {"kind": "assembly", "film": "041", "stage": "picture", "urgent": True}))
        self.assertEqual(jobs.do_next(data, "cursor", {"mini"}, AT)["title"], "due cut")
        script = {"id": "J1", "kind": "script", "film": "040", "stage": "script", "status": "open", "history": []}
        cut = {"id": "J2", "kind": "assembly", "film": "041", "stage": "edit", "status": "open", "history": []}
        soon, later = AT, AT + dt.timedelta(days=14)
        air = {"041": soon, "040": later}
        self.assertLess(workflow.order(cut, {}, (), AT, (), air, agent="claude"),
                        workflow.order(script, {}, (), AT, (), air, agent="claude"))
        due = {"J2": soon}
        self.assertLess(workflow.order(cut, due, (), AT, (), None, agent="claude"),
                        workflow.order(script, due, (), AT, (), None, agent="claude"))
        self.assertLess(workflow.order(cut, {}, (), AT, ("041",), None, agent="claude"),
                        workflow.order(script, {}, (), AT, ("041",), None, agent="claude"))
        # No agent: every job shares one skill rank, so air order is unchanged.
        self.assertLess(workflow.order(cut, {}, (), AT, (), air),
                        workflow.order(script, {}, (), AT, (), air))

    def test_a_held_desk_blocks_only_its_own_window(self):
        home = {"id": "J1", "kind": "studio", "repo": channels.default(), "status": "open", "needs": "mini"}
        other = next(slug for slug in channels.slugs() if slug != channels.default())
        guest = {"id": "J2", "kind": "studio", "repo": other, "status": "open", "needs": "mini"}
        code = {"id": "J3", "kind": "assembly", "status": "open", "needs": "mini", "film": "040", "stage": "edit"}
        home_desk = auto.desk_name(home, "mini")
        guest_desk = auto.desk_name(guest, "macbook")
        self.assertEqual(home_desk, "studio-" + channels.default())
        self.assertEqual(guest_desk, "studio-" + other)
        self.assertEqual(auto.desk_name(guest, "mini"), guest_desk)  # the name does not change with the machine
        self.assertTrue(auto.acquire_desk(home_desk, "cursor", AT, self.state))
        self.assertTrue(auto.desk_blocks(home, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(home, "cursor", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(guest, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(code, "gemini", self.state, AT, "mini"))
        self.assertEqual(auto.desk_name({"kind": "vo"}, "mini"), "elevenlabs")
        self.assertEqual(auto.desk_name({"kind": "video"}, "mini"), "flow")
        self.assertTrue(auto.acquire_desk("flow", "cursor", AT, self.state))
        self.assertTrue(auto.desk_blocks({"kind": "image"}, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(code, "gemini", self.state, AT, "mini"))
        data = queue(("mini", "End screen on the home channel", {"kind": "studio", "repo": channels.default()}),
                     ("mini", "End screen on the other channel", {"kind": "studio", "repo": other}))
        taken = auto.claim_next(data, "gemini", AT, self.state)
        self.assertEqual(taken["repo"], other)

    def test_a_relay_slot_and_a_timer_see_each_others_desk(self):
        chief = self.state / "chief"
        chief.mkdir()
        (chief / "execution-1.json").write_text(json.dumps({
            "worker": "cursor", "desk": "flow", "pid": os.getpid(), "slot": 1,
            "expiresAt": (AT + dt.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }))
        self.assertTrue(auto.desk_blocks({"kind": "image"}, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks({"kind": "assembly", "film": "040", "stage": "edit"}, "gemini", self.state, AT, "mini"))
        self.assertTrue(auto.acquire_desk("elevenlabs", "gemini", AT, self.state))
        self.assertTrue(auto.timer_desk_held("elevenlabs", "cursor", AT, self.state))
        self.assertFalse(auto.timer_desk_held("elevenlabs", "gemini", AT, self.state))

    def test_a_stage_handoff_queues_exactly_one_next_job_from_the_channel(self):
        os.environ.pop("AGENT_STAGE_HANDOFF", None)
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}))
        job = jobs.do_next(data, "claude", {"any"}, AT)
        jobs.do_done(job, "claude", "locked", AT)
        self.assertIsNone(auto.queue_next(data, job, "claude", AT))  # default off
        with mock.patch.dict(os.environ, {"AGENT_STAGE_HANDOFF": "1"}):
            nxt = auto.queue_next(data, job, "claude", AT)
            self.assertEqual((nxt["stage"], nxt["kind"], nxt["film"]), ("sources", "facts", "040"))
            # A different kind on the same film and stage is still the one next job.
            jobs.do_add(data, title="Already checking", needs="any", body="", by="claude", at=AT,
                        film="041", stage="sources", kind="review")
            other_script = jobs.do_add(data, title="Write the other script", needs="any", body="", by="claude", at=AT,
                                       film="041", stage="script", kind="script")
            self.assertIsNone(auto.queue_next(data, other_script, "claude", AT))
            self.assertIsNone(auto.queue_next(data, job, "claude", AT))
            guest = next(slug for slug in channels.slugs() if channels.stage_keys(slug)[:3] != channels.stage_keys(channels.default())[:3])
            keys = channels.stage_keys(guest)
            guest_job = jobs.do_add(data, title="Write the guest script", needs="any", body="", by="claude", at=AT,
                                    film="011", stage="script", kind="script", repo=guest)
            followed = auto.queue_next(data, guest_job, "claude", AT)
            self.assertEqual(followed["stage"], keys[keys.index("script") + 1])
            self.assertEqual(followed["repo"], guest)
            self.assertIsNone(auto.queue_next(data, guest_job, "claude", AT))
        with mock.patch.dict(os.environ, {"AGENT_SELF_DISPATCH": "0"}):
            self.assertEqual(auto.may_start("cursor", AT, self.state), (False, "relay-only"))

    def test_a_handoff_error_never_blocks_done(self):
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}))
        job = jobs.do_next(data, "claude", {"any"}, AT)
        jobs.do_done(job, "claude", "locked", AT)
        with mock.patch.object(auto, "queue_next", side_effect=RuntimeError("stage list missing")):
            self.assertIsNone(jobs.after_done(data, job, "claude", AT))
        self.assertEqual(job["status"], "done")
        self.assertTrue(any("stage handoff failed" in h.get("what", "") for h in job["history"]))

    def test_a_failed_run_retries_in_place_or_releases_then_files_one_repair(self):
        data = queue(("mini", "Cut the pictures", {"kind": "assembly", "film": "040", "stage": "edit"}))
        job = jobs.do_next(data, "cursor", {"mini"}, AT)
        with mock.patch.object(routing, "next_lane", return_value=("cursor", "cursor-auto")):
            first = auto.fail_run(data, job, "cursor", "cursor-grok-4-7", "python3 scripts/build.py", "exit 1", AT, self.feed)
        self.assertEqual(first, {"action": "retry", "agent": "cursor", "model": "cursor-auto"})
        self.assertEqual(job["status"], "claimed")
        self.assertFalse(any(j.get("repair_of") for j in data["jobs"]))
        with mock.patch.object(routing, "next_lane", return_value=("codex", "gpt-6.1-sol")):
            second = auto.fail_run(data, job, "cursor", first["model"], "python3 scripts/build.py", "exit 1 again", AT, self.feed)
        self.assertEqual(second["action"], "repair")
        self.assertEqual(job["status"], "open")
        repairs = [j for j in data["jobs"] if j.get("repair_of") == job["id"]]
        self.assertEqual(len(repairs), 1)
        self.assertIn("python3 scripts/build.py", repairs[0]["body"])
        self.assertIn("exit 1 again", repairs[0]["body"])
        third = auto.fail_run(data, job, "cursor", first["model"], "python3 scripts/build.py", "exit 1 again", AT, self.feed)
        self.assertEqual(third["job"], second["job"])
        self.assertEqual(sum(1 for j in data["jobs"] if j.get("repair_of")), 1)
        lines = self.feed.read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["repair"], second["job"])
        # A different agent is not run inside this lease: the job is released with self_retry recorded.
        data = queue(("mini", "Record the line", {"kind": "vo", "film": "040", "stage": "vo"}))
        voiced = jobs.do_next(data, "cursor", {"mini"}, AT)
        with mock.patch.object(routing, "next_lane", return_value=("codex", "eleven_v3")):
            released = auto.fail_run(data, voiced, "cursor", "eleven_v3", "python3 vo_take.py", "exit 1", AT, self.feed)
        self.assertEqual(released["action"], "released")
        self.assertEqual(released["agent"], "codex")
        self.assertEqual(voiced["status"], "open")
        self.assertEqual(voiced["self_retry"]["count"], 1)
        self.assertFalse(any(j.get("repair_of") for j in data["jobs"]))
        with mock.patch.object(routing, "next_lane", return_value=("gemini", "eleven_v3")):
            repair = auto.fail_run(data, voiced, "codex", "eleven_v3", "python3 vo_take.py", "exit 1 again", AT, self.feed)
        self.assertEqual(repair["action"], "repair")
        self.assertEqual(sum(1 for j in data["jobs"] if j.get("repair_of") == voiced["id"]), 1)

    def test_a_tick_retries_once_and_the_board_lists_every_timer(self):
        data = queue(("mini", "Cut the pictures", {"kind": "assembly", "film": "040", "stage": "edit"}))
        calls = []

        def run(agent, job, model):
            calls.append((agent, model))
            return 1, "nope", "python3 scripts/build.py"

        with mock.patch.object(routing, "next_lane", side_effect=[("cursor", "cursor-auto"), ("codex", "gpt-6.1-sol")]):
            out = auto.tick("cursor", AT, self.state, data, run, free_mb=8000, feed=self.feed)
        self.assertEqual(calls, [("cursor", "cursor-grok-4-7"), ("cursor", "cursor-auto")])
        self.assertEqual(out["action"], "repair")
        self.assertFalse(out["ok"])
        self.assertFalse(auto.lease_held("cursor", AT, self.state))
        rows = {row["agent"]: row for row in auto.timer_rows(AT, self.state)}
        self.assertEqual(set(rows), {agent for agent, _, _ in auto.TIMERS})
        self.assertEqual(rows["cursor"]["job"], "J0001")
        self.assertEqual(rows["gemini"]["everyMin"], 11)
        shown = machines.section({"jobs": []}, None, None, AT, agent_timers=auto.timer_rows(AT, self.state))
        self.assertEqual(len(shown["timers"]), 6)

    def test_timers_are_staggered_and_plists_name_each_agent(self):
        folder = self.state / "plists"
        paths = auto.write_plists(folder)
        self.assertEqual(len(paths), 6)
        intervals = []
        for path in paths:
            text = path.read_text()
            self.assertNotIn("@", text)
            agent = path.name[len("com.owb.agent."):-len(".plist")]
            self.assertIn(f"--agent {agent}", text)
            doc = plistlib.loads(text.encode())
            self.assertEqual(doc["Label"], f"com.owb.agent.{agent}")
            self.assertIn(f"--agent {agent}", doc["ProgramArguments"][2])
            intervals.append(doc["StartInterval"])
        self.assertEqual(intervals, [600, 660, 720, 780, 840, 900])
        self.assertTrue(all('cd "$STUDIO_CHECKOUT"' in path.read_text() for path in paths))

    def test_the_relay_and_the_memory_floor_hold_a_timer(self):
        chief = self.state / "chief"
        chief.mkdir()
        (chief / "execution-0.json").write_text(json.dumps({
            "worker": "cursor", "pid": os.getpid(), "slot": 0, "job": "J9",
            "expiresAt": (AT + dt.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }))
        (chief / "execution-1.json").write_text(json.dumps({
            "worker": "gemini", "pid": os.getpid(), "slot": 1, "job": "J8",
            "expiresAt": (AT + dt.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }))
        self.assertEqual(auto.may_start("cursor", AT, self.state, free_mb=8000), (False, "relay"))
        self.assertTrue(auto.acquire_lease("claudecode", AT, self.state))
        self.assertEqual(auto.may_start("codex", AT, self.state, free_mb=8000), (False, "cap"))
        self.assertEqual(auto.mini_running(AT, self.state), 3)  # two relay slots and one timer, cursor not twice
        import chief_relay
        quiet = pathlib.Path(self.tmp.name) / "quiet"
        with mock.patch.object(chief_relay, "free_memory_bytes", return_value=100 * 1024 * 1024):
            self.assertEqual(auto.may_start("cursor", AT, quiet), (False, "memory"))
        with mock.patch.object(chief_relay, "free_memory_bytes", return_value=4000 * 1024 * 1024):
            ok, why = auto.may_start("cursor", AT, quiet)
        self.assertTrue(ok, why)


if __name__ == "__main__":
    unittest.main()
