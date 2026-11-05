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
        # HOS film stages fail closed across propose/reserve/consume/consume_with_git
        # so an OWB Git push rejection can never leave a cross-repo HOS stage claimed.
        fresh = {"jobs": [job(repo="hos", film="007", stage="edit")]}
        with self.assertRaisesRegex(ValueError, "no currently eligible"):
            reservations.reserve(fresh, **self.kw)
        self.assertNotIn("dispatch_reservation", fresh["jobs"][0])

        self.data["jobs"][0].update(repo="hos", film="007", stage="edit")
        before = copy.deepcopy(self.data)
        with self.assertRaisesRegex(ValueError, "HOS board"):
            self.consume()
        self.assertEqual(self.data, before)

        attempts = []
        def collect():
            attempts.append(True)
            return self.evidence
        def transaction(apply, message):
            losing = copy.deepcopy(self.data)
            value, error, touched = apply(losing)
            if error:
                return None, error
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction):
            value, error = reservations.consume_with_git(
                evidence=collect, token=self.kw["token"],
                host_id="mini", worker="codex", claimant="codex",
            )
        self.assertIsNone(value)
        self.assertIn("HOS board", error)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(self.data["jobs"][0]["status"], "open")

    def test_owb_board_claim_push_race_rolls_back_before_retry_and_on_rejection(self):
        import capacity_evidence
        import studio
        with tempfile.TemporaryDirectory() as temp:
            films_root = pathlib.Path(temp) / "02_Video-Projects"
            film = films_root / "028_Test"
            film.mkdir(parents=True)
            path = film / "status.json"
            initial = dict(film="028", title="Test", claims=[], stages={"edit": {"state": "todo"}})
            path.write_text(json.dumps(initial))
            self.data["jobs"][0].update(film="028", stage="edit")

            # 1) Push rejection followed by eligible retry: attempt 1 writes status.json,
            # push fails, retry rolls back status.json before refreshing stage_claims
            # and succeeds cleanly on attempt 2.
            attempts = []
            def collect_live():
                attempts.append(True)
                claims = capacity_evidence.board_stage_claims(films_root, "owb", T)
                return dict(self.evidence, stage_claims=claims)

            def push_race_then_succeed(apply, message):
                losing = copy.deepcopy(self.data)
                value1, err1, touched1 = apply(losing)
                self.assertIsNone(err1)
                self.assertEqual(touched1, [path])
                # Before retry 2 runs, status.json on disk was written by attempt 1.
                self.assertEqual(json.loads(path.read_text())["claims"][0]["by"], "codex")
                # Simulate rejected push without external git checkout: apply() itself
                # must roll back its uncommitted status.json write before collect_live().
                value2, err2, touched2 = apply(self.data)
                return value2, err2

            with patch("jobs.with_git", side_effect=push_race_then_succeed), \
                    patch("studio.FILMS", films_root), \
                    patch("studio.film_dir", return_value=film):
                value, error = reservations.consume_with_git(
                    evidence=collect_live, token=self.kw["token"],
                    host_id="mini", worker="codex", claimant="codex"
                )
            self.assertIsNone(error)
            self.assertEqual(len(attempts), 2)
            self.assertEqual(value["status"], "claimed")
            board = json.loads(path.read_text())
            self.assertEqual(board["claims"][0]["by"], "codex")
            self.assertEqual(board["stages"]["edit"]["state"], "doing")

            # 2) Push rejection followed by rejected retry (e.g. higher-priority job arrives):
            # canonical queue stays open AND status.json is rolled back to unclaimed.
            path.write_text(json.dumps(initial))
            self.setUp()
            self.data["jobs"][0].update(film="028", stage="edit")
            attempts.clear()

            def push_race_then_reject(apply, message):
                losing = copy.deepcopy(self.data)
                value1, err1, touched1 = apply(losing)
                self.assertIsNone(err1)
                self.assertEqual(json.loads(path.read_text())["claims"][0]["by"], "codex")
                # Competing push adds an urgent higher-priority job before retry 2.
                self.data["jobs"].append(job("J9999", urgent=True, due=T.isoformat()))
                value2, err2, _ = apply(self.data)
                return value2, err2

            with patch("jobs.with_git", side_effect=push_race_then_reject), \
                    patch("studio.FILMS", films_root), \
                    patch("studio.film_dir", return_value=film):
                value, error = reservations.consume_with_git(
                    evidence=collect_live, token=self.kw["token"],
                    host_id="mini", worker="codex", claimant="codex"
                )
            self.assertIsNone(value)
            self.assertIn("priority", error)
            self.assertEqual(self.data["jobs"][0]["status"], "open")
            board_after = json.loads(path.read_text())
            self.assertEqual(board_after["claims"], [])
            self.assertEqual(board_after["stages"]["edit"]["state"], "todo")

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

    def test_failed_release_checks_exact_claim_and_current_local_cleanup(self):
        self.consume()
        original = copy.deepcopy(self.data)
        def transaction(apply, message):
            return apply(self.data)[:2]
        kw = dict(token=self.kw["token"], host_id="mini", worker="codex", claimant="codex",
                  reason="FileNotFoundError", clock=lambda:T)
        with patch("jobs.with_git", side_effect=transaction):
            value, error = reservations.release_failed_with_git(**kw, clear=lambda:False)
            self.assertIsNone(value)
            self.assertIn("cleanup unverified", error)
            self.assertEqual(self.data, original)
            value, error = reservations.release_failed_with_git(**dict(kw, claimant="gemini"), clear=lambda:True)
            self.assertIsNone(value)
            self.assertEqual(self.data, original)
            value, error = reservations.release_failed_with_git(**kw, clear=lambda:True)
            self.assertTrue(value)
            self.assertIsNone(error)
            self.assertEqual(self.data["jobs"][0]["status"], "open")
            self.assertNotIn("dispatch_reservation", self.data["jobs"][0])
            # Replay cannot release some later owner's claim by matching job ID.
            self.data["jobs"][0].update(status="claimed", by="gemini")
            value, error = reservations.release_failed_with_git(**kw, clear=lambda:True)
            self.assertFalse(value)
            self.assertEqual(self.data["jobs"][0]["by"], "gemini")

    def test_failed_release_rolls_back_board_on_rejected_push_and_rechecks_cleanup(self):
        import studio
        with tempfile.TemporaryDirectory() as temp:
            films = pathlib.Path(temp) / "02_Video-Projects"
            film = films / "028_Test"
            film.mkdir(parents=True)
            path = film / "status.json"
            path.write_text(json.dumps(dict(film="028", title="Test", claims=[],
                                           stages={"edit":{"state":"todo"}})))
            self.data["jobs"][0].update(film="028", stage="edit")
            self.consume()
            with patch("studio.FILMS", films):
                import jobs
                self.assertIsNone(jobs.board_claim(self.data["jobs"][0], "codex", T))
                before = path.read_bytes()
                clear_calls = []
                def clear():
                    clear_calls.append(True)
                    return len(clear_calls) == 1  # uncertainty appears before retry
                def race(apply, message):
                    losing = copy.deepcopy(self.data)
                    value, error, touched = apply(losing)
                    self.assertIsNone(error)
                    self.assertEqual(json.loads(path.read_text())["claims"], [])
                    return apply(self.data)[:2]
                with patch("jobs.with_git", side_effect=race):
                    value, error = reservations.release_failed_with_git(
                        token=self.kw["token"], host_id="mini", worker="codex", claimant="codex",
                        reason="ValueError", clear=clear, clock=lambda:T)
                self.assertIsNone(value)
                self.assertIn("cleanup unverified", error)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual(self.data["jobs"][0]["status"], "claimed")
                self.assertEqual(len(clear_calls), 2)

                # A later confirmed-clear retry releases the queue and board,
                # without pretending any failed output is reviewed or done.
                with patch("jobs.with_git", side_effect=lambda apply, message:apply(self.data)[:2]):
                    value, error = reservations.release_failed_with_git(
                        token=self.kw["token"], host_id="mini", worker="codex", claimant="codex",
                        reason="ValueError", clear=lambda:True, clock=lambda:T)
                self.assertTrue(value)
                self.assertIsNone(error)
                board = json.loads(path.read_text())
                self.assertEqual(board["claims"], [])
                self.assertEqual(board["stages"]["edit"]["state"], "todo")


if __name__ == "__main__":
    unittest.main()
