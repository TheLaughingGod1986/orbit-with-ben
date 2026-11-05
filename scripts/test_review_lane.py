#!/usr/bin/env python3
"""Tests for scripts/review_lane.py (rule H, Ben 5 Nov 2026)."""
import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import review_lane as rl  # noqa: E402
import workflow_state as w  # noqa: E402

AT = dt.datetime(2026, 11, 5, 1, 0, tzinfo=dt.timezone.utc)


def job(i, **k):
    return {"id": i, "title": k.pop("title", i), "status": k.pop("status", "open"), "needs": "mini", "history": [], **k}


class ReviewLane(unittest.TestCase):
    def test_parked_film_work_gets_a_linked_review_and_leaves_the_chief_queue(self):
        p = job("J1", status="blocked", kind="thumb", film="031", stage="thumbs", result="parked for Chief: review three concepts")
        data = {"jobs": [p], "next_id": 10}
        self.assertTrue(w.is_review(p))
        moved = rl.apply(data, AT)
        r = data["jobs"][-1]
        self.assertEqual((r["kind"], r["review_of"], r["film"]), ("review", "J1", "031"))
        self.assertFalse(w.is_review(p))
        self.assertIn(r["id"], p["result"])
        self.assertEqual(moved, [("J1", r["id"])])
        self.assertEqual(rl.apply(data, AT), [])  # idempotent

    def test_chief_review_and_condition_checks_are_rekinded(self):
        data = {"jobs": [job("J2", kind="chief", title="Chief: verify condition for J9", recheck_of="J9"),
                         job("J3", kind="chief", title="Chief: review recipe", status="blocked")], "next_id": 10}
        rl.apply(data, AT)
        self.assertEqual([j["kind"] for j in data["jobs"]], ["review", "review"])
        self.assertEqual(data["jobs"][0]["title"], "verify condition for J9")
        self.assertEqual(data["jobs"][1]["status"], "open")
        self.assertFalse(any(w.role_job(j) for j in data["jobs"]))

    def test_the_chiefs_own_calls_stay(self):
        keep = [job("A", kind="chief", title="Chief: review PR437 and turn on parallel Mini dispatch"),
                job("B", status="blocked", kind="assembly", result="parked for Chief: review and merge PR488 head x"),
                job("C", status="blocked", kind="video", film="009", result="parked for Chief: spend £4 on Vertex"),
                job("D", kind="chief", title="Chief: review OWB 2026-10 monthly improvement report"),
                job("E", status="blocked", kind="studio", result="parked for Chief: publish schedule change"),
                job("F", kind="chief", title="Chief: resolve 033 topic orphan-review", handoff={"film": "033"})]
        data = {"jobs": keep, "next_id": 10}
        self.assertEqual(rl.apply(data, AT), [])
        self.assertEqual(len(data["jobs"]), 6)

    def test_no_second_review_when_a_ruling_job_already_names_it(self):
        data = {"jobs": [job("J5", status="blocked", kind="vo", film="033", result="parked for Chief: rule on take"),
                         job("J6", kind="review", title="033: ruling on J5 VO transcript")], "next_id": 10}
        self.assertEqual(rl.apply(data, AT), [])


if __name__ == "__main__":
    unittest.main()
