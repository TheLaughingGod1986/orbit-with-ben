"""Canonical capacity races, expiry and stage exclusion; no real dispatch."""
import copy
import datetime as dt
import unittest
from unittest.mock import patch

import capacity_reservations as reservations
import workflow_state as workflow
from test_dispatch_capacity import T, host, proof, job, portable, choose


class Reservations(unittest.TestCase):
    def setUp(self):
        self.data = {"jobs": [job()]}
        self.kw = dict(token="unique-reservation-0001", host_id="mini", worker="codex",
            hosts=[host()], leases=[], accounts={"shared": proof(ready=True, limit=1)},
            at=T, chief="codex", choose_worker=choose, installed_head="exact-head",
            reviewed_head="exact-head")

    def reserve(self, **kw):
        return reservations.reserve(self.data, **dict(self.kw, **kw))

    def test_free_lane_reserves_immediately_without_claim_or_launch(self):
        result = self.reserve()
        self.assertEqual(result["phase"], "reserved")
        self.assertEqual(self.data["jobs"][0]["status"], "open")
        self.assertNotIn("by", self.data["jobs"][0])
        self.assertIsNone(result["free_slot_at"])
        self.assertIn("not claimed or launched", self.data["jobs"][0]["history"][-1]["what"])

    def test_replayed_token_is_exactly_once(self):
        first = self.reserve()
        before = copy.deepcopy(self.data)
        self.assertEqual(self.reserve(), first)
        self.assertEqual(self.data, before)
        with self.assertRaisesRegex(ValueError, "identity"):
            self.reserve(host_id="macbook")

    def test_second_host_transaction_cannot_reserve_same_job(self):
        self.reserve()
        with self.assertRaisesRegex(ValueError, "no currently eligible"):
            self.reserve(token="second-reservation-0002", host_id="macbook",
                hosts=[host(), host("macbook")])

    def test_stage_cannot_be_reserved_twice_or_claimed_by_normal_next(self):
        self.data["jobs"] = [job(film="028", stage="edit"), job("J1841", film="028", stage="edit")]
        self.reserve()
        for row in self.data["jobs"]:
            self.assertFalse(workflow.claimable(row, self.data["jobs"], T, "gemini", "codex"))
        with self.assertRaisesRegex(ValueError, "no currently eligible"):
            self.reserve(token="second-reservation-0002")

    def test_existing_board_stage_claim_excludes_open_job(self):
        self.data["jobs"][0].update(film="028", stage="edit")
        with self.assertRaises(ValueError):
            self.reserve(stage_claims=[("owb", "028", "edit")])
        self.assertNotIn("dispatch_reservation", self.data["jobs"][0])

    def test_expired_reservation_releases_capacity_without_changing_hold(self):
        self.reserve()
        later = T + dt.timedelta(minutes=2)
        with self.assertRaisesRegex(ValueError, "expired"):
            self.reserve(at=later)
        self.assertTrue(workflow.claimable(self.data["jobs"][0], self.data["jobs"], later,
                                           "codex", "codex"))
        self.data["jobs"][0]["hold"] = dict(type="input", condition="actual external input")
        with self.assertRaises(ValueError):
            self.reserve(at=later, token="second-reservation-0002")
        self.assertEqual(self.data["jobs"][0]["hold"]["condition"], "actual external input")

    def test_expired_launch_window_never_frees_claimed_remote_account(self):
        self.reserve()
        held = self.data["jobs"][0]
        held.update(status="claimed", by="macbook", since=T.isoformat(),
                    eta=(T + dt.timedelta(minutes=25)).isoformat())
        held["dispatch_reservation"].update(phase="claimed", host="macbook", claimant="macbook")
        later = T + dt.timedelta(hours=2)
        self.assertIsNotNone(reservations.active(held, later))
        # Even a stale queue ETA is not remote process-exit evidence.
        self.assertFalse(workflow.claimable(held, [held], later, "gemini", "codex"))
        self.data["jobs"].append(job("J9999"))
        with self.assertRaisesRegex(ValueError, "no currently eligible"):
            self.reserve(token="another-reservation-0002", at=T+dt.timedelta(minutes=3))

    def test_busy_chief_reserves_independent_specialist_but_not_review(self):
        self.data["jobs"] += [job("J1841", kind="chief", needs="any")]
        result = self.reserve(worker="gemini", hosts=[host(worker="gemini", configured_limit=2,
            capacity_review="review", installed_head="abc", reviewed_head="abc")],
            leases=[dict(job="busy-chief", worker="codex", host="mini", account="codex")])
        self.assertEqual((result["job"], result["worker"]), ("J1834", "gemini"))
        self.assertNotIn("dispatch_reservation", self.data["jobs"][1])

    def test_busy_mini_portable_laptop_reserved_once(self):
        self.data["jobs"][0]["portable"] = portable()
        kw = dict(host_id="macbook", hosts=[host(worker="gemini"), host("macbook")],
            leases=[dict(job="busy-chief", worker="gemini", host="mini", account="gemini")])
        result = self.reserve(**kw)
        self.assertEqual(result["host"], "macbook")
        self.assertEqual(self.reserve(**kw), result)

    def test_rollback_checks_token_identity_and_cannot_release_actual_claim(self):
        self.reserve()
        args = dict(token=self.kw["token"], host_id="mini", worker="codex", at=T, reason="launch failed")
        with self.assertRaises(ValueError):
            reservations.cancel(self.data, **dict(args, worker="gemini"))
        self.data["jobs"][0]["status"] = "claimed"
        with self.assertRaises(ValueError):
            reservations.cancel(self.data, **args)
        self.data["jobs"][0]["status"] = "open"
        self.assertTrue(reservations.cancel(self.data, **args))
        self.assertFalse(reservations.cancel(self.data, **args))

    def test_head_review_and_media_guard_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exact-head"):
            self.reserve(reviewed_head="old-head")
        self.data["jobs"][0]["required_capabilities"] = ["audio_input"]
        with self.assertRaises(ValueError):
            self.reserve()

    def test_git_retry_recollects_evidence_and_uses_current_queue(self):
        attempts = []
        evidence = {k: v for k, v in self.kw.items() if k not in {"token", "host_id", "worker"}}
        def collect():
            attempts.append(True)
            return evidence
        def transaction(apply, message):
            # Simulate a lost push and replay onto another host's winning commit.
            losing = copy.deepcopy(self.data)
            value, error, touched = apply(losing)
            self.assertIsNone(error)
            self.assertEqual(touched, [])
            self.data["jobs"][0]["status"] = "claimed"
            self.data["jobs"][0]["by"] = "other"
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction):
            value, error = reservations.reserve_with_git(evidence=collect,
                token=self.kw["token"], host_id="mini", worker="codex")
        self.assertIsNone(value)
        self.assertIn("no currently eligible", error)
        self.assertEqual(len(attempts), 2)
        self.assertNotIn("dispatch_reservation", self.data["jobs"][0])


if __name__ == "__main__":
    unittest.main()
