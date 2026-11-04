"""Reservation consumption exercises real queue gates, with no launch or spend."""
import copy
import datetime as dt
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import capacity_reservations as reservations
import test_capacity_reservations as fixtures
from test_dispatch_capacity import T, host, job, portable


class Claims(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.Reservations()
        fixture.setUp()
        self.data, self.kw = fixture.data, fixture.kw
        reservations.reserve(self.data, **self.kw)
        self.evidence = {k: v for k, v in self.kw.items()
                         if k not in {"token", "host_id", "worker"}}
        self.addCleanup(patch.stopall)
        patch("chief_relay.current_execution", return_value=None).start()
        patch("chief_relay.worker_capabilities", return_value={}).start()

    def consume(self, **kw):
        return reservations.consume(self.data, token=self.kw["token"], host_id="mini",
                                    worker="codex", claimant="codex",
                                    **dict(self.evidence, **kw))

    def test_normal_claim_and_replay_are_idempotent_and_not_launch(self):
        result = self.consume()
        self.assertEqual((result["status"], result["by"]), ("claimed", "codex"))
        self.assertEqual(result["dispatch_reservation"]["phase"], "claimed")
        self.assertEqual(result["progress"]["step"], 0)
        before = copy.deepcopy(self.data)
        self.assertEqual(self.consume(), result)
        self.assertEqual(self.data, before)
        self.assertIn("not launched", result["history"][-1]["what"])

    def test_reserved_token_cannot_be_replayed_after_competing_claim(self):
        self.data["jobs"][0].update(status="claimed", by="other")
        with self.assertRaises(ValueError):
            reservations.reserve(self.data, **self.kw)

    def test_claim_replay_does_not_reset_board_stage_start(self):
        self.data["jobs"][0].update(film="028", stage="edit")
        self.consume()
        def transaction(apply, message):
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction), patch("jobs.board_claim") as board:
            value, error = reservations.consume_with_git(evidence=lambda:self.evidence,
                token=self.kw["token"], host_id="mini", worker="codex", claimant="codex")
        self.assertIsNone(error)
        self.assertEqual(value["by"], "codex")
        board.assert_not_called()

    def test_failed_revalidation_never_changes_original(self):
        for change in [dict(reviewed_head="wrong"), dict(at=T+dt.timedelta(minutes=2)),
                       dict(hosts=[host(on_ac=False, free_gb=0)])]:
            before = copy.deepcopy(self.data)
            with self.assertRaises(ValueError):
                self.consume(**change)
            self.assertEqual(self.data, before)

    def test_new_hold_dependency_or_capability_blocks_consumption(self):
        for field, value in [("hold", dict(type="input", condition="new input")),
                             ("after", "missing"), ("required_capabilities", ["audio_input"])]:
            with self.subTest(field=field):
                baseline = copy.deepcopy(self.data)
                self.data["jobs"][0][field] = value
                before = copy.deepcopy(self.data)
                with self.assertRaises(ValueError):
                    self.consume()
                self.assertEqual(self.data, before)
                self.data = baseline

    def test_busy_specialist_or_laptop_cannot_take_second_job(self):
        self.data["jobs"].append(job("J9999", status="claimed", by="codex"))
        with self.assertRaisesRegex(ValueError, "already holds"):
            self.consume()

    def test_new_higher_priority_job_requires_replan(self):
        self.data["jobs"].append(job("J9999", urgent=True, due=T.isoformat()))
        before = copy.deepcopy(self.data)
        with self.assertRaisesRegex(ValueError, "priority"):
            self.consume()
        self.assertEqual(self.data, before)

    def test_model_account_failure_and_stage_claim_rechecked(self):
        for change in [dict(accounts={}), dict(hosts=[host(workers={})]),
                       dict(stage_claims=[("owb", "028", "edit")])]:
            baseline = copy.deepcopy(self.data)
            self.data["jobs"][0].update(film="028", stage="edit")
            with self.assertRaises(ValueError):
                self.consume(**change)
            self.data = baseline

    def test_laptop_claim_retains_specialist_but_uses_macbook_owner(self):
        self.data = {"jobs": [job(portable=portable(), **{"for": "codex"})]}
        kw = dict(self.kw, host_id="macbook", hosts=[host(worker="gemini"), host("macbook")],
                  leases=[dict(job="busy-chief", worker="gemini", host="mini", account="gemini")])
        reservations.reserve(self.data, **kw)
        evidence = {k:v for k,v in kw.items() if k not in {"token", "host_id", "worker"}}
        result = reservations.consume(self.data, token=kw["token"], host_id="macbook",
                                      worker="codex", claimant="macbook", **evidence)
        self.assertEqual(result["by"], "macbook")
        self.assertEqual(result["for"], "codex")
        self.assertEqual(result["needs"], "mini")
        self.assertEqual(result["dispatch_reservation"]["worker"], "codex")
        self.assertEqual(result["progress"]["by"], "macbook")

    def test_laptop_use_changed_before_claim_is_rejected(self):
        self.data = {"jobs": [job(portable=portable())]}
        kw = dict(self.kw, host_id="macbook", hosts=[host(worker="gemini"), host("macbook")],
                  leases=[dict(job="busy-chief", worker="gemini", host="mini", account="gemini")])
        reservations.reserve(self.data, **kw)
        evidence = {k:v for k,v in kw.items() if k not in {"token", "host_id", "worker"}}
        evidence["hosts"][1]["idle_minutes"] = 0
        with self.assertRaises(ValueError):
            reservations.consume(self.data, token=kw["token"], host_id="macbook",
                                 worker="codex", claimant="macbook", **evidence)
        self.assertEqual(self.data["jobs"][0]["status"], "open")

    def test_hos_stage_needs_explicit_board_adapter(self):
        self.data["jobs"][0].update(repo="hos", film="007", stage="edit")
        with self.assertRaisesRegex(ValueError, "HOS board"):
            self.consume()
        # With an explicit HOS board transaction callback, consumption succeeds or rolls back on conflict.
        def transaction(apply, message):
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction):
            value, error = reservations.consume_with_git(
                evidence=lambda: self.evidence, token=self.kw["token"],
                host_id="mini", worker="codex", claimant="codex",
                hos_board_claim=lambda job_doc, by, at: "held by another",
            )
            self.assertIsNone(value)
            self.assertIn("HOS board stage held", error)
            self.assertEqual(self.data["jobs"][0]["status"], "open")
            value, error = reservations.consume_with_git(
                evidence=lambda: self.evidence, token=self.kw["token"],
                host_id="mini", worker="codex", claimant="codex",
                hos_board_claim=lambda job_doc, by, at: None,
            )
            self.assertIsNone(error)
            self.assertEqual(value["status"], "claimed")

    def test_transaction_board_conflict_preserves_reservation_and_queue(self):
        self.data["jobs"][0].update(film="028", stage="edit")
        before = copy.deepcopy(self.data)
        def transaction(apply, message):
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction), \
                patch("jobs.board_claim", return_value="another owner"):
            value, error = reservations.consume_with_git(evidence=lambda:self.evidence,
                token=self.kw["token"], host_id="mini", worker="codex", claimant="codex")
        self.assertIsNone(value)
        self.assertIn("board stage held", error)
        self.assertEqual(self.data, before)

    def test_real_board_claim_is_written_only_with_successful_queue_claim(self):
        import jobs
        import studio
        with tempfile.TemporaryDirectory() as temp:
            film = pathlib.Path(temp) / "028_Test"
            film.mkdir()
            path = film / "status.json"
            initial = dict(film="028", title="Test", claims=[], stages={"edit":{"state":"todo"}})
            path.write_text(json.dumps(initial))
            self.data["jobs"][0].update(film="028", stage="edit")
            def transaction(apply, message):
                value, error, touched = apply(self.data)
                self.assertEqual(touched, [path])
                return value, error
            with patch("jobs.with_git", side_effect=transaction), \
                    patch("studio.film_dir", return_value=film):
                value, error = reservations.consume_with_git(evidence=lambda:self.evidence,
                    token=self.kw["token"], host_id="mini", worker="codex", claimant="codex")
            self.assertIsNone(error)
            board = json.loads(path.read_text())
            self.assertEqual(board["claims"][0]["by"], value["by"])
            self.assertEqual(board["stages"]["edit"]["state"], "doing")
            self.assertEqual(value["status"], "claimed")

    def test_git_retry_rechecks_after_other_host_wins(self):
        calls = []
        def collect():
            calls.append(True)
            return self.evidence
        def transaction(apply, message):
            losing = copy.deepcopy(self.data)
            value, error, touched = apply(losing)
            self.assertIsNone(error)
            self.data["jobs"][0].update(status="claimed", by="other-host")
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction):
            value, error = reservations.consume_with_git(evidence=collect,
                token=self.kw["token"], host_id="mini", worker="codex", claimant="codex")
        self.assertIsNone(value)
        self.assertIn("another owner", error)
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.data["jobs"][0]["by"], "other-host")


if __name__ == "__main__":
    unittest.main()
