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
import jobs  # noqa: E402
import machines  # noqa: E402

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

    def test_skill_comes_before_urgent_and_due_work(self):
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}),
                     ("any", "Cut the pictures", {"kind": "assembly", "film": "041", "stage": "edit", "urgent": True}))
        self.assertEqual(jobs.do_next(data, "claude", {"cloud", "any"}, AT)["kind"], "script")
        data = queue(("mini", "Write the script", {"kind": "script", "film": "040", "stage": "script", "urgent": True}),
                     ("mini", "Cut the pictures", {"kind": "assembly", "film": "041", "stage": "edit"}))
        self.assertEqual(jobs.do_next(data, "cursor", {"mini"}, AT)["kind"], "assembly")
        data = queue(("mini", "Write the script", {"kind": "script", "film": "040", "stage": "script", "urgent": True}),
                     ("mini", "Watch the plates", {"kind": "image", "film": "041", "stage": "picture"}))
        self.assertEqual(jobs.do_next(data, "gemini", {"mini"}, AT)["kind"], "image")
        data = queue(("mini", "later cut", {"kind": "assembly", "film": "040", "stage": "edit"}),
                     ("mini", "due cut", {"kind": "assembly", "film": "041", "stage": "picture", "urgent": True}))
        self.assertEqual(jobs.do_next(data, "cursor", {"mini"}, AT)["title"], "due cut")

    def test_a_held_desk_blocks_only_its_own_window(self):
        self.assertTrue(auto.acquire_desk("studio-owb", "cursor", AT, self.state))
        owb = {"id": "J1", "kind": "studio", "repo": "owb", "status": "open", "needs": "mini"}
        hos = {"id": "J2", "kind": "studio", "repo": "hos", "status": "open", "needs": "mini"}
        code = {"id": "J3", "kind": "assembly", "status": "open", "needs": "mini", "film": "040", "stage": "edit"}
        self.assertTrue(auto.desk_blocks(owb, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(owb, "cursor", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(hos, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(code, "gemini", self.state, AT, "mini"))
        self.assertEqual(auto.desk_name(hos, "mini"), "studio-hos-mini")
        self.assertEqual(auto.desk_name(hos, "macbook"), "studio-hos-macbook")
        self.assertEqual(auto.desk_name({"kind": "studio", "repo": "ww2"}, "mini"), "studio-ww2")
        self.assertEqual(auto.desk_name({"kind": "vo"}, "mini"), "elevenlabs")
        self.assertEqual(auto.desk_name({"kind": "video"}, "mini"), "flow")
        self.assertTrue(auto.acquire_desk("flow", "cursor", AT, self.state))
        self.assertTrue(auto.desk_blocks({"kind": "image"}, "gemini", self.state, AT, "mini"))
        self.assertFalse(auto.desk_blocks(code, "gemini", self.state, AT, "mini"))
        data = queue(("mini", "Orbit end screen", {"kind": "studio", "repo": "owb"}),
                     ("mini", "History end screen", {"kind": "studio", "repo": "hos"}))
        taken = auto.claim_next(data, "gemini", AT, self.state)
        self.assertEqual(taken["repo"], "hos")

    def test_a_stage_handoff_queues_exactly_one_next_job(self):
        data = queue(("any", "Write the script", {"kind": "script", "film": "040", "stage": "script"}))
        job = jobs.do_next(data, "claude", {"any"}, AT)
        jobs.do_done(job, "claude", "locked", AT)
        nxt = auto.queue_next(data, job, "claude", AT)
        self.assertEqual((nxt["stage"], nxt["kind"], nxt["film"]), ("sources", "facts", "040"))
        self.assertIsNone(auto.queue_next(data, job, "claude", AT))
        self.assertEqual(sum(j.get("kind") == "facts" for j in data["jobs"]), 1)
        edit = jobs.do_add(data, title="Cut the pictures", needs="mini", body="", by="claude", at=AT,
                           film="040", stage="edit", kind="assembly")
        review = auto.queue_next(data, edit, "cursor", AT)
        self.assertEqual((review["stage"], review["kind"]), ("thumbs", "qa"))
        thumb = auto.queue_next(data, review, "claude", AT)
        self.assertEqual((thumb["stage"], thumb["kind"]), ("thumbs", "thumb"))
        self.assertIsNone(auto.queue_next(data, review, "claude", AT))
        with mock.patch.dict(os.environ, {"AGENT_SELF_DISPATCH": "0"}):
            other = jobs.do_add(data, title="Write another script", needs="any", body="", by="claude", at=AT,
                                film="042", stage="script", kind="script")
            self.assertIsNone(auto.queue_next(data, other, "claude", AT))
            self.assertEqual(auto.may_start("cursor", AT, self.state), (False, "relay-only"))

    def test_a_failed_run_retries_once_then_files_one_repair(self):
        data = queue(("mini", "Cut the pictures", {"kind": "assembly", "film": "040", "stage": "edit"}))
        job = jobs.do_next(data, "cursor", {"mini"}, AT)
        first = auto.fail_run(data, job, "cursor", "cursor-grok-4-7", "python3 scripts/build.py", "exit 1", AT, self.feed)
        self.assertEqual(first["action"], "retry")
        self.assertEqual(job["status"], "claimed")
        self.assertFalse(any(j.get("repair_of") for j in data["jobs"]))
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

    def test_a_tick_retries_once_and_the_board_lists_every_timer(self):
        data = queue(("mini", "Cut the pictures", {"kind": "assembly", "film": "040", "stage": "edit"}))
        calls = []

        def run(agent, job, model):
            calls.append((agent, model))
            return 1, "nope", "python3 scripts/build.py"

        out = auto.tick("cursor", AT, self.state, data, run, free_mb=8000, feed=self.feed)
        self.assertEqual(len(calls), 2)
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


if __name__ == "__main__":
    unittest.main()
