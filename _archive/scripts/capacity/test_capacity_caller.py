"""Production caller integration with canonical in-memory transactions and real CPU children."""
import copy
import subprocess
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

import capacity_caller as caller
import chief_relay
import macbook_worker
from test_dispatch_capacity import T, host, proof, job, portable, choose


class Caller(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.config = dict(enabled=True, role="mini", approved_by="claude",
            approval_ref="fixture-only", reviewed_head="reviewed", job="J1834",
            token="caller-integration-0001", at=T.isoformat(),
            expiresAt=(T+dt.timedelta(minutes=5)).isoformat(),
            argv=[sys.executable, "-c", "print('cpu fixture')"],
            cap_seconds=2, log_path=str(self.root / "run.log"))
        self.data = {"jobs": [job()]}
        self.config["transport_approval_ref"] = "mounted-fixture"
        self.ev = dict(hosts=[host()], leases=[], accounts={"shared":proof(ready=True, limit=1)},
                       at=T, chief="claude", choose_worker=choose,
                       installed_head="reviewed", reviewed_head="reviewed")
        self.guard = lambda: []

    def call(self, dispatch=None, serial_only=False, admission=None):
        def document(root, name):
            if name == "dispatch.json":
                return copy.deepcopy(self.config)
            if name == "peer.json":
                return dict(at=T.isoformat(), expiresAt=(T+dt.timedelta(minutes=5)).isoformat(),
                    transport_approval_ref="mounted-fixture", hosts=[next((h for h in self.ev["hosts"] if h["role"] != self.config["role"]),
                        host("macbook" if self.config["role"] == "mini" else "mini"))],
                    leases=self.ev["leases"])
            raise ValueError(name)
        def transaction(apply, message):
            return apply(self.data)[:2]
        with patch("capacity_evidence.private_document", side_effect=document), \
             patch("capacity_evidence.reviewed_installation", return_value="reviewed"), \
             patch("capacity_evidence.collect", side_effect=lambda *a, **k:(copy.deepcopy(self.ev["hosts"][-1]), self.ev["accounts"])), \
             patch("capacity_evidence.transaction_evidence", side_effect=lambda *a, **k:copy.deepcopy(self.ev)), \
             patch("jobs.load", side_effect=lambda:self.data), \
             patch("jobs.with_git", side_effect=transaction), \
             patch("chief_relay.current_execution", return_value=None), \
             patch("chief_relay.worker_capabilities", return_value={}):
            return caller.attempt(role=self.config["role"], owb_root=self.root,
                laptop_guard=self.guard, chief="claude", clock=lambda:T,
                environ={"OWB_CAPACITY_ENABLED":"1", "OWB_CAPACITY_ROOT":str(self.root)},
                serial_only=serial_only, admission=admission)

    def laptop(self):
        self.config.update(role="macbook", source_root=str(self.root),
            staging_parent=str(self.root), return_parent=str(self.root),
            max_bytes=1000, max_files=2, transport_approval_ref="mounted-fixture",
            argv=[sys.executable,"-c","from pathlib import Path; Path('result.txt').write_text('fixture')"])
        contract = portable()
        contract["outputs"] = ["result.txt"]
        self.data["jobs"][0]["portable"] = contract
        self.ev["hosts"] = [host(worker="gemini"), host("macbook")]
        self.ev["leases"] = [dict(job="busy-mini", worker="gemini", host="mini", account="other")]

    def test_serial_empty_observation_permits_canonical_dispatch_without_cpu_launch(self):
        self.data["jobs"][0]["kind"] = "chief"
        result = self.call(serial_only=True)
        self.assertTrue(result["serial_safe"])
        self.assertFalse((self.root / "run.log").exists())
        self.assertNotIn("dispatch_reservation", self.data["jobs"][0])

    def test_stale_cpu_request_does_not_starve_fresh_empty_serial_dispatch(self):
        self.config["at"] = (T-dt.timedelta(hours=1)).isoformat()
        self.config["expiresAt"] = (T-dt.timedelta(minutes=55)).isoformat()
        self.config.pop("job")
        self.config.pop("argv")
        self.config.pop("token")
        self.assertTrue(self.call(serial_only=True)["serial_safe"])
        self.assertEqual(self.call()["state"], "capacity_rejected")

    def test_mini_only_serial_needs_no_macbook_peer_file(self):
        # J2197, 5 Nov 2026: with no peer.json on a Mini-only rollout every serial tick was rejected.
        self.data["jobs"][0]["kind"] = "chief"
        self.assertFalse((self.root / "peer.json").exists())
        self.assertTrue(self.call(serial_only=True)["serial_safe"])

    def test_serial_occupied_or_uncertain_observation_never_falls_through(self):
        for lease in (dict(job="busy", worker="gemini", host="mini", account="other"),
                      dict(job="unknown", worker="unknown", host="mini", recovery_required=True)):
            self.ev["leases"] = [lease]
            self.assertFalse(self.call(serial_only=True)["serial_safe"])
        self.ev["leases"] = []
        self.data["jobs"].append(job("J9999", status="claimed", by="macbook"))
        self.assertFalse(self.call(serial_only=True)["serial_safe"])

    def test_serial_launch_lock_remains_held_until_lease_publication(self):
        import fcntl
        cfg = dict(self.config)
        with patch("capacity_evidence.private_document", return_value=cfg), \
             patch("capacity_caller.production_tick", return_value={"state":"capacity_waiting", "serial_safe":True}):
            with caller.serial_preflight(owb_root=self.root,
                    environ={"OWB_CAPACITY_ENABLED":"1", "OWB_CAPACITY_ROOT":str(self.root)}):
                with (self.root / "caller.lock").open("a") as competing:
                    with self.assertRaises(BlockingIOError):
                        fcntl.flock(competing, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with (self.root / "caller.lock").open("a") as competing:
                fcntl.flock(competing, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def run_laptop(self, receipt, ordinary=None):
        from contextlib import contextmanager
        @contextmanager
        def observed(**kwargs):
            self.assertEqual(kwargs["role"], "macbook")
            yield receipt
        with patch.object(macbook_worker, "pull_main", return_value=""), \
             patch.object(macbook_worker, "guards", return_value=[]), \
             patch.object(macbook_worker, "push_heartbeat"), \
             patch.object(macbook_worker, "capacity_tick", return_value={"state":"capacity_waiting"}) as tick, \
             patch("capacity_caller.serial_preflight", side_effect=observed), \
             patch.object(macbook_worker, "sh", return_value=subprocess.CompletedProcess([],10,"","")) as claim:
            self.assertEqual(macbook_worker.run_one(), "idle" if receipt and receipt.get("serial_safe") else "waiting")
            return claim.call_count, tick.call_count

    def test_laptop_empty_no_candidate_continues_canonical_queue(self):
        self.assertEqual(self.run_laptop({"state":"capacity_waiting", "serial_safe":True}), (1,0))

    def test_laptop_uncertain_and_occupied_receipts_never_claim_ordinary(self):
        for receipt in ({"state":"capacity_rejected"}, {"state":"capacity_busy"},
                        {"state":"capacity_waiting", "serial_safe":False}):
            claims, _ = self.run_laptop(receipt)
            self.assertEqual(claims, 0)

    def test_laptop_stale_request_uses_fresh_occupancy_and_holds_exclusion_through_claim(self):
        import fcntl
        self.config["role"] = "macbook"
        self.config["at"] = (T-dt.timedelta(hours=1)).isoformat()
        self.config["expiresAt"] = (T-dt.timedelta(minutes=55)).isoformat()
        self.ev["hosts"] = [host(), host("macbook")]
        self.ev["leases"] = []
        self.config["transport_approval_ref"] = "mounted-fixture"
        self.assertTrue(self.call(serial_only=True)["serial_safe"])
        def competing_claim(*args, **kwargs):
            with (self.root / "caller.lock").open("a") as competing:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(competing, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return subprocess.CompletedProcess([],10,"","")
        env = {"OWB_CAPACITY_ENABLED":"1", "OWB_CAPACITY_ROOT":str(self.root)}
        with patch.dict(__import__("os").environ, env), \
             patch("capacity_evidence.private_document", return_value=self.config), \
             patch("capacity_caller.production_tick", return_value={"state":"capacity_waiting", "serial_safe":True,
                 "admission": {"job": "J1834", "worker": "codex", "model": "gpt-6.1-sol"}}), \
             patch("serial_admission.finish"), \
             patch.object(macbook_worker, "pull_main", return_value=""), \
             patch.object(macbook_worker, "guards", return_value=[]), \
             patch.object(macbook_worker, "push_heartbeat"), \
             patch.object(macbook_worker, "sh", side_effect=competing_claim):
            self.assertEqual(macbook_worker.run_one(), "idle")
        with (self.root / "caller.lock").open("a") as competing:
            fcntl.flock(competing, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def ordinary_fixture(self, role="macbook"):
        self.laptop()
        self.data["jobs"][0]["status"] = "done"
        self.data["jobs"].append(job("J9998", kind="review", needs="any"))
        self.ev["hosts"][-1]["workers"]["codex"]["verified_models"].append("gpt-6-astra")
        if role == "mini":
            self.config["role"] = "mini"
            self.ev["hosts"] = [host("macbook", worker="gemini"), host()]
            self.ev["leases"][0]["host"] = "macbook"
            self.ev["hosts"][-1]["workers"]["codex"]["verified_models"].append("gpt-6-astra")
        return dict(job="J9998", worker="codex", model="gpt-6-astra")

    def admit(self, request=None):
        with patch.object(macbook_worker, "installed", return_value=["codex"]), \
             patch.object(macbook_worker, "usable", return_value=["codex"]):
            return self.call(serial_only=True, admission=request or {})

    def test_busy_independent_peer_real_receipt_reaches_ordinary_laptop(self):
        self.ordinary_fixture()
        receipt = self.call(serial_only=True)
        self.assertTrue(receipt["serial_safe"], receipt)
        admitted = self.admit()
        self.assertEqual(admitted["admission"]["job"], "J9998", admitted)
        from contextlib import contextmanager
        @contextmanager
        def preflight(**kw):
            yield receipt
        with patch("capacity_caller.serial_preflight", side_effect=preflight), \
             patch("capacity_caller.production_tick", return_value=admitted), \
             patch.object(macbook_worker, "pull_main", return_value=""), \
             patch.object(macbook_worker, "guards", return_value=[]), \
             patch.object(macbook_worker, "run_ordinary", return_value="ran") as ordinary, \
             patch("serial_admission.finish") as finish:
            self.assertEqual(macbook_worker.run_one(), "ran")
            ordinary.assert_called_once_with(admitted)
            finish.assert_called_once_with(admitted)

    def test_serial_selected_shared_pool_at_limit_rejected(self):
        self.ordinary_fixture()
        self.ev["leases"][0]["account"] = "shared"
        self.assertNotIn("admission", self.admit())
        self.assertNotIn("dispatch_reservation", self.data["jobs"][-1])

    def test_serial_local_or_uncertain_occupancy_rejected(self):
        for variant in ({"host": "macbook"}, {"recovery_required": True}, {"account": ""}):
            self.ordinary_fixture()
            self.ev["leases"][0].update(variant)
            self.assertNotIn("admission", self.admit())

    def test_serial_stale_or_missing_peer_proof_rejected(self):
        self.ordinary_fixture()
        self.ev["hosts"][0]["at"] = (T-dt.timedelta(hours=1)).isoformat()
        self.assertFalse(self.call(serial_only=True)["serial_safe"])
        self.assertNotIn("admission", self.admit())
        self.config["transport_approval_ref"] = "unapproved"
        self.assertEqual(self.call(serial_only=True)["state"], "capacity_rejected")

    def test_serial_cross_host_competing_admission_and_positive_exit(self):
        self.ordinary_fixture()
        admitted = self.admit()
        self.assertIn("admission", admitted)
        # A second host's fresh snapshot sees the canonical reservation, even
        # before any process lease or ordinary claim has been published.
        self.config["role"] = "mini"
        self.ev["hosts"] = [host("macbook"), host()]
        self.ev["leases"] = []
        request = dict(job="J9998", worker="codex", model="gpt-6-astra")
        self.ev["hosts"][-1]["workers"]["codex"]["verified_models"].append("gpt-6-astra")
        self.assertNotIn("admission", self.admit(request))
        import serial_admission
        def transaction(apply, message):
            return apply(self.data)[:2]
        with patch("jobs.with_git", side_effect=transaction):
            serial_admission.finish(admitted)
        self.assertIn("admission", self.admit(request))

    def test_serial_admission_is_consumed_only_by_its_canonical_owner(self):
        self.ordinary_fixture()
        admitted = self.admit()
        import jobs
        self.assertIsNotNone(jobs.do_next(self.data, "macbook", {"macbook", "any"}, T, job_id="J9998"))
        self.assertEqual(self.data["jobs"][-1]["by"], "macbook")
        self.assertEqual(self.data["jobs"][-1]["dispatch_reservation"], admitted["admission"])
        self.assertEqual(self.admit({"validate": admitted["admission"]})["admission"], admitted["admission"])
        self.ev["accounts"]["shared"]["ready"] = False
        self.assertNotIn("admission", self.admit({"validate": admitted["admission"]}))
        self.assertIsNone(jobs.do_next(self.data, "gemini", {"mini", "any"}, T, job_id="J9998"))

    def test_serial_git_retry_reobserves_competing_account_occupancy(self):
        self.ordinary_fixture()
        observed = []
        import serial_admission
        real = serial_admission.reserve
        def retry(data, **kw):
            observed.append(1)
            # Competing reservation committed before this retry is visible to
            # the actual admission function, and cannot be ignored as remote.
            data["jobs"][0]["dispatch_reservation"] = dict(phase="serial", host="mini",
                account="shared", worker="gemini", claimant="gemini", token="other-token")
            return real(data, **kw)
        with patch("serial_admission.reserve", side_effect=retry):
            self.assertNotIn("admission", self.admit())
        self.assertEqual(len(observed), 1)

    def test_launch_revalidation_preserves_own_owb_board_claim_only(self):
        self.ordinary_fixture()
        self.data["jobs"][-1].update(film="032", stage="script")
        admitted = self.admit()
        self.assertIn("admission", admitted)
        row = self.data["jobs"][-1]
        row.update(status="claimed", by="macbook")
        self.ev["stage_claims"] = [("owb", "032", "script")]
        board = {"claims": [dict(stage="script", by="macbook", note="J9998 fixture",
            at=T.isoformat(), eta=(T+dt.timedelta(minutes=10)).isoformat())]}
        with patch("studio.load", return_value=board), patch("jobs.film_status_path", return_value=self.root):
            self.assertIn("admission", self.admit({"validate": admitted["admission"]}))
            board["claims"][0]["by"] = "gemini"
            self.assertNotIn("admission", self.admit({"validate": admitted["admission"]}))

    def test_uncertain_group_exit_retains_canonical_admission(self):
        self.ordinary_fixture()
        admitted = self.admit()
        import serial_admission
        with patch("execution_leases.group_members", return_value=[42]):
            with self.assertRaises(RuntimeError):
                serial_admission.confirm_group_exit(42)
        self.assertEqual(self.data["jobs"][-1]["dispatch_reservation"], admitted["admission"])
        with patch("execution_leases.group_members", side_effect=RuntimeError("probe unavailable")):
            with self.assertRaises(RuntimeError):
                serial_admission.confirm_group_exit(42)

    def test_mini_serial_rejects_changed_ordinary_deadline_selection(self):
        request = self.ordinary_fixture(role="mini")
        self.data["jobs"].append(job("J0001", needs="any", urgent=True))
        self.assertNotIn("admission", self.admit(request))

    def test_symmetric_mini_serial_busy_independent_peer(self):
        request = self.ordinary_fixture(role="mini")
        self.assertTrue(self.call(serial_only=True)["serial_safe"])
        self.assertIn("admission", self.admit(request))

    def test_disabled_bridge_never_reads_private_config_or_mutates_queue(self):
        with patch("capacity_evidence.private_document") as read:
            self.assertIsNone(caller.attempt(role="mini",owb_root=self.root,environ={}))
            read.assert_not_called()

    def test_real_cpu_success_claims_but_never_completes(self):
        result = self.call()
        self.assertEqual(result["state"], "capacity_exited")
        self.assertEqual(self.data["jobs"][0]["status"], "claimed")
        self.assertFalse(result["job_completed"])
        self.assertEqual((self.root / "run.log").read_text(), "cpu fixture\n")

    def test_launch_failure_releases_canonical_claim_and_reservation(self):
        self.config["argv"] = [str(self.root / "missing")]
        self.assertEqual(self.call()["state"], "capacity_rejected")
        self.assertEqual(self.data["jobs"][0]["status"], "open")
        self.assertNotIn("dispatch_reservation", self.data["jobs"][0])

    def test_different_selected_job_cannot_run_approved_command(self):
        self.config["job"] = "J9999"
        self.data["jobs"].append(job("J9999"))
        self.assertEqual(self.call()["state"], "capacity_rejected")
        self.assertFalse((self.root / "run.log").exists())
        self.assertTrue(all(j["status"] == "open" for j in self.data["jobs"]))

    def test_laptop_receives_approved_bundle_and_returns_hash_receipt(self):
        self.laptop()
        result = self.call()
        self.assertEqual(result["state"], "capacity_exited", result)
        output = json.loads(pathlib.Path(result["receipt_path"]).read_text())
        self.assertEqual(output["direction"], "output")
        self.assertEqual(output["files"][0]["path"], "result.txt")
        self.assertEqual(self.data["jobs"][0]["by"], "macbook")
        self.assertFalse(result["stage_approved"])

    def test_mini_consumes_laptop_return_from_mounted_path_without_approval(self):
        self.laptop()
        sent = self.call()
        self.assertEqual(sent["state"], "capacity_exited")
        # Simulated receiving host sees the mounted return folder, but hashes
        # its bytes itself. This is a filesystem fixture, not real-host proof.
        self.config.update(mode="receive", role="mini", source_host="macbook",
                           return_bundle=sent["return_bundle"], review_parent=str(self.root))
        received = self.call()
        self.assertEqual(received["state"], "capacity_returned_for_review", received)
        self.assertEqual((pathlib.Path(received["review_bundle"]) / "result.txt").read_text(), "fixture")
        self.assertFalse(received["stage_approved"])
        pathlib.Path(sent["return_bundle"], "result.txt").write_text("changed")
        self.assertEqual(self.call()["state"], "capacity_rejected")

    def test_laptop_guard_change_after_claim_releases_without_launch(self):
        self.laptop()
        calls = []
        def guard():
            calls.append(1)
            return ["in use"] if len(calls) >= 3 else []
        self.guard = guard
        result = self.call()
        self.assertEqual(result["state"], "capacity_rejected")
        self.assertEqual(self.data["jobs"][0]["status"], "open")
        self.assertNotIn("dispatch_reservation", self.data["jobs"][0])
        self.assertFalse((self.root / "run.log").exists())

    def test_offline_or_unavailable_host_does_not_fall_through_to_serial(self):
        self.ev["hosts"][0]["workers"] = {}
        result = self.call()
        self.assertEqual(result["state"], "capacity_waiting")
        self.assertEqual(self.data["jobs"][0]["status"], "open")

    def test_production_uses_separate_locked_reviewed_checkout(self):
        checkout = self.root / "queue"
        checkout.mkdir()
        (checkout / ".git").write_text("gitdir: fixture")
        cfg = dict(self.config, queue_root=str(checkout),
                   at=dt.datetime.now(dt.timezone.utc).isoformat(),
                   expiresAt=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)).isoformat())
        env = {"OWB_CAPACITY_ENABLED":"1", "OWB_CAPACITY_ROOT":str(self.root)}
        with patch("capacity_evidence.private_document", return_value=cfg), \
             patch("capacity_evidence.reviewed_installation", return_value="reviewed") as reviewed, \
             patch("capacity_caller.subprocess.run", return_value=subprocess.CompletedProcess(
                 [], 0, '{"state":"capacity_exited"}', '')) as launch:
            result = caller.production_tick(role="mini", owb_root=self.root, environ=env)
            self.assertEqual(result["state"], "capacity_exited")
            self.assertEqual(launch.call_args.kwargs["cwd"], checkout.resolve())
            self.assertIn(str(checkout.resolve() / "scripts/capacity_caller.py"), launch.call_args.args[0])
            reviewed.assert_called_once_with(checkout.resolve(), "reviewed")
            cfg["queue_root"] = str(self.root)
            self.assertEqual(caller.production_tick(role="mini", owb_root=self.root,
                              environ=env)["state"], "capacity_rejected")
            self.assertEqual(launch.call_count, 1)

    def test_production_wrapper_failure_is_not_serial_fallback_or_secret_echo(self):
        checkout = self.root / "queue"
        checkout.mkdir()
        (checkout / ".git").write_text("gitdir: fixture")
        cfg = dict(self.config, queue_root=str(checkout),
                   at=dt.datetime.now(dt.timezone.utc).isoformat(),
                   expiresAt=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)).isoformat())
        with patch("capacity_evidence.private_document", return_value=cfg), \
             patch("capacity_evidence.reviewed_installation", return_value="reviewed"), \
             patch("capacity_caller.subprocess.run", return_value=subprocess.CompletedProcess(
                 [], 1, "private diagnostic", "private credential")):
            result = caller.production_tick(role="mini", owb_root=self.root,
                environ={"OWB_CAPACITY_ENABLED":"1", "OWB_CAPACITY_ROOT":str(self.root)})
            self.assertEqual(result["state"], "capacity_rejected")
            self.assertNotIn("private", json.dumps(result))

    def test_production_entrypoints_supply_real_role_and_guard_adapters(self):
        with patch("capacity_caller.production_tick", return_value={"state":"fixture"}) as attempt:
            self.assertEqual(chief_relay.capacity_tick(), {"state":"fixture"})
            self.assertEqual(attempt.call_args.kwargs["role"], "mini")
            macbook_worker.capacity_tick()
            self.assertEqual(attempt.call_args.kwargs["role"], "macbook")


if __name__ == "__main__":
    unittest.main()
