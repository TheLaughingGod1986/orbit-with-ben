"""Private local evidence boundary tests; no model, remote or paid calls."""
import copy
import datetime as dt
import hashlib
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import capacity_evidence as evidence
import dispatch_capacity as capacity
from test_dispatch_capacity import T, proof, job, choose

HEAD = "a" * 40
FINGERPRINT = hashlib.sha256(b"test-machine").hexdigest()


class Evidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.root.chmod(0o700)
        self.config = dict(version=1, at=T.isoformat(), expiresAt=(T+dt.timedelta(days=1)).isoformat(),
            host="registered-mini", role="mini", machine_fingerprint=FINGERPRINT,
            approved_by="codex", approval_ref="review-only", configured_limit=1,
            min_free_gb=20, min_memory_gb=2, max_load=4,
            workers={"codex":dict(account="codex-shared", models=["gpt-6.1-sol"])},
            accounts={"codex-shared":1})
        self.probes = proof(host="registered-mini", machine_fingerprint=FINGERPRINT,
            workers={"codex":proof(ready=True, account="codex-shared")},
            accounts={"codex-shared":proof(ready=True, limit=1)})
        self.probes["workers"]["codex"]["verified_models"] = ["gpt-6.1-sol"]
        self.measured = dict(machine_fingerprint=FINGERPRINT, architecture="arm64", free_gb=30,
            load=1, memory_available_gb=8, memory_basis="free plus speculative pages",
            on_ac=True, idle_minutes=20)
        self.write()

    def write(self):
        for name, doc in [("registration.json", self.config), ("probes.json", self.probes)]:
            path = self.root/name
            path.write_text(json.dumps(doc))
            path.chmod(0o600)

    def collect(self):
        return evidence.collect(self.root, at=T, installed_head=HEAD,
                                measurement=lambda _:copy.deepcopy(self.measured))

    def plan(self, candidate=None):
        host, accounts = self.collect()
        return capacity.propose({"jobs":[candidate or job()]}, [host], [], accounts, T, "codex", choose)

    def test_fresh_bound_evidence_composes_with_planner_without_claim(self):
        host, accounts = self.collect()
        self.assertEqual(host["registered_id"], "registered-mini")
        self.assertEqual(host["installed_head"], HEAD)
        self.assertEqual(host["workers"]["codex"]["account"], "codex-shared")
        self.assertEqual(accounts["codex-shared"]["limit"], 1)
        self.assertEqual(self.plan()["proposals"][0]["phase"], "proposed")

    def test_missing_registration_is_not_inferred_from_measurement(self):
        (self.root/"registration.json").unlink()
        with self.assertRaises(OSError):
            self.collect()

    def test_wrong_machine_expired_or_unapproved_registration_rejected(self):
        original = copy.deepcopy(self.config)
        for changes in [dict(machine_fingerprint="b"*64), dict(approval_ref=""),
                        dict(expiresAt=T.isoformat()), dict(configured_limit=True),
                        dict(expiresAt=(T+dt.timedelta(days=31)).isoformat())]:
            self.config = dict(original, **changes)
            self.write()
            with self.assertRaises(ValueError):
                self.collect()

    def test_private_modes_and_symlinks_rejected(self):
        path = self.root/"probes.json"
        path.chmod(0o644)
        with self.assertRaises(ValueError):
            self.collect()
        path.chmod(0o600)
        saved = self.root/"saved.json"
        path.rename(saved)
        path.symlink_to(saved)
        with self.assertRaises(OSError):
            self.collect()
        path.unlink()
        saved.rename(path)
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            self.collect()

    def test_directory_symlink_is_not_trusted(self):
        link = self.root/"alias"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(OSError):
            evidence.private_document(link, "probes.json")

    def test_oversized_nonfinite_array_or_device_document_rejected(self):
        path = self.root/"probes.json"
        for raw in ['x'*(evidence.MAX_DOCUMENT+1), '{"limit": NaN}', '[]']:
            path.write_text(raw)
            with self.assertRaises(ValueError):
                self.collect()
        path.unlink()
        os.mkfifo(path, 0o600)
        with self.assertRaises(ValueError):
            self.collect()

    def test_stale_wrong_host_or_wrong_machine_probes_rejected(self):
        original = copy.deepcopy(self.probes)
        for changes in [dict(at=(T-dt.timedelta(minutes=6)).isoformat()),
                        dict(host="another"), dict(machine_fingerprint="b"*64)]:
            self.probes = dict(original, **changes)
            self.write()
            with self.assertRaises(ValueError):
                self.collect()

    def test_status_login_alone_unknown_quota_outage_and_expired_probe_stay_unavailable(self):
        baseline = copy.deepcopy(self.probes)
        for target, changes in [("worker", dict(verified_models=[])), ("worker", dict(ready=False)),
            ("worker", dict(auth_evidence="")), ("worker", dict(account="other")),
            ("worker", dict(expiresAt=T.isoformat())), ("account", dict(ready=False)),
            ("account", dict(limit=2)), ("account", dict(quota_evidence=""))]:
            self.probes = copy.deepcopy(baseline)
            value = self.probes["workers"]["codex"] if target == "worker" else self.probes["accounts"]["codex-shared"]
            value.update(changes)
            self.write()
            self.assertEqual(self.plan()["proposals"], [])

    def test_unbound_model_is_not_verified_fallback(self):
        self.probes["workers"]["codex"]["verified_models"] = ["unregistered-model"]
        self.write()
        self.assertEqual(self.plan()["proposals"], [])

    def test_shared_pool_limit_cannot_be_relabeled_by_worker_receipt(self):
        self.probes["workers"]["codex"]["account"] = "laptop-codex-new-quota"
        self.write()
        self.assertEqual(self.collect()[1], {})

    def test_media_proof_requires_own_fresh_host_worker_binding(self):
        caps = proof(available=["audio_input"], evidence="actual listening probe",
                     host="registered-mini", worker="codex")
        self.probes["workers"]["codex"]["capabilities"] = caps
        self.write()
        self.assertEqual(len(self.plan(job(required_capabilities=["audio_input"]))["proposals"]), 1)
        for changes in [dict(host="laptop"), dict(worker="gemini"), dict(evidence=""),
                        dict(at=(T-dt.timedelta(minutes=6)).isoformat())]:
            self.probes["workers"]["codex"]["capabilities"] = dict(caps, **changes)
            self.write()
            self.assertEqual(self.plan(job(required_capabilities=["audio_input"]))["proposals"], [])

    def test_resource_loss_and_unreviewed_lane_remain_excluded(self):
        for key, value in [("free_gb", 1), ("load", 100), ("memory_available_gb", None)]:
            saved = self.measured[key]
            self.measured[key] = value
            self.assertEqual(self.plan()["proposals"], [])
            self.measured[key] = saved
        self.config["configured_limit"] = 2
        self.write()
        self.assertEqual(self.plan()["proposals"], [])

    def test_laptop_rechecks_mains_and_idle_at_each_collection(self):
        self.config["role"] = "macbook"
        self.write()
        self.assertEqual(self.collect()[0]["guard_reasons"], [])
        self.measured["on_ac"] = False
        self.assertTrue(self.collect()[0]["guard_reasons"])
        self.measured["on_ac"] = True
        self.measured["idle_minutes"] = None
        self.assertTrue(self.collect()[0]["guard_reasons"])

    def test_malformed_receipt_containers_never_become_ready(self):
        baseline = copy.deepcopy(self.probes)
        for field in ("workers", "accounts"):
            self.probes = dict(baseline, **{field: ["invalid"]})
            self.write()
            with self.assertRaises(ValueError):
                self.collect()
        self.probes = copy.deepcopy(baseline)
        self.probes["workers"]["codex"] = ["invalid"]
        self.write()
        self.assertEqual(self.plan()["proposals"], [])
        self.assertFalse(capacity.fresh(["invalid"], T))

    def test_receipt_secrets_and_extra_fields_are_not_returned(self):
        self.probes["token"] = "NEVER-RETURN"
        self.probes["workers"]["codex"]["token"] = "NEVER-RETURN"
        self.write()
        self.assertNotIn("NEVER-RETURN", json.dumps(self.collect()))

    def test_read_only_observation_does_not_invent_registration_or_slot(self):
        with patch.object(evidence, "measure", return_value=self.measured):
            result = evidence.observation(self.root, at=T, installed_head=HEAD)
            self.assertEqual(result["state"], "unverified")
            self.assertFalse(result["dispatch_enabled"])
            self.assertIsNone(result["free_slot_at"])
            self.assertNotIn(FINGERPRINT, json.dumps(result))
            result = evidence.observation(self.root, at=T, installed_head=HEAD, evidence_root=self.root)
            self.assertEqual(result["ready_workers"], ["codex"])
            self.assertFalse(result["dispatch_enabled"])
            self.assertNotIn("auth_evidence", json.dumps(result))
            self.measured["free_gb"] = 0
            result = evidence.observation(self.root, at=T, installed_head=HEAD, evidence_root=self.root)
            self.assertEqual(result["state"], "guards_rejected")

    def test_failed_observation_and_invalid_private_receipt_remain_unknown(self):
        with patch.object(evidence, "measure", side_effect=ValueError):
            result = evidence.observation(self.root, at=T, installed_head=HEAD)
            self.assertEqual(result["availability"], "unknown")
        with patch.object(evidence, "measure", return_value=self.measured):
            result = evidence.observation(self.root, at=T, installed_head=HEAD, evidence_root=self.root/"missing")
            self.assertEqual(result["state"], "unverified")
            self.assertNotIn(str(self.root), json.dumps(result))

    def test_exact_commit_identity_never_uses_runner_digest(self):
        with patch.object(evidence, "command", side_effect=[HEAD+"\n", ""]):
            self.assertEqual(evidence.installed_head(self.root), HEAD)
        with patch.object(evidence, "command", side_effect=[HEAD+"\n", " M scripts/chief_relay.py"]):
            self.assertEqual(evidence.installed_head(self.root), "")
        with patch.object(evidence, "command", return_value="short-digest"):
            self.assertEqual(evidence.installed_head(self.root), "")
        with patch.object(evidence, "command", side_effect=ValueError):
            self.assertEqual(evidence.installed_head(self.root), "")

    def test_macos_measurement_hashes_identity_and_uses_conservative_memory(self):
        def run(argv):
            return {'IOPlatformExpertDevice':'"IOPlatformUUID" = "raw-machine-id"',
                    'vm_stat':'Mach Virtual Memory Statistics: (page size of 16384 bytes)\nPages free: 10.\nPages speculative: 20.\nPages inactive: 999999.',
                    'batt':"Now drawing from 'AC Power'", 'IOHIDSystem':'"HIDIdleTime" = 1200000000000'}[argv[-1]]
        # IOHIDSystem is followed by -d 4 in the production probe.
        def probe(argv):
            return run(["IOHIDSystem"] if "IOHIDSystem" in argv else argv)
        result = evidence.measure(self.root, run=probe)
        self.assertEqual(result["memory_available_gb"], 30*16384/1024**3)
        self.assertEqual(result["idle_minutes"], 20)
        self.assertNotIn("raw-machine-id", json.dumps(result))
        with self.assertRaises(ValueError):
            evidence.measure(self.root, run=lambda _:"")

    def test_produce_probes_enforces_outage_chronology_and_shared_account_taint(self):
        self.config["workers"]["cursor"] = dict(account="codex-shared", models=["cursor-auto"])
        self.write()
        verified_workers = {
            "codex": dict(at=T.isoformat(), ready=True, account="codex-shared",
                          auth_evidence="verified execution J1900", verified_models=["gpt-6.1-sol"]),
            "cursor": dict(at=T.isoformat(), ready=True, account="codex-shared",
                           auth_evidence="verified execution J1901", verified_models=["cursor-auto"]),
        }
        verified_accounts = {
            "codex-shared": dict(at=T.isoformat(), ready=True, limit=1,
                                 quota_evidence="verified subscription quota"),
        }
        doc = evidence.produce_probes(
            self.root, at=T, verified_workers=verified_workers,
            verified_accounts=verified_accounts,
            measurement=lambda _: copy.deepcopy(self.measured),
        )
        self.assertTrue(doc["workers"]["codex"]["ready"])
        self.assertTrue(doc["accounts"]["codex-shared"]["ready"])
        self.assertEqual(len(self.plan()["proposals"]), 1)

        # Outage at T (even with expired retryAt) blocks readiness until a newer execution succeeds.
        outages = {
            "codex": dict(at=T.isoformat(), retryAt=(T - dt.timedelta(minutes=5)).isoformat(),
                          auth_required=True)
        }
        evidence.produce_probes(
            self.root, at=T, verified_workers=verified_workers,
            verified_accounts=verified_accounts, outages=outages,
            measurement=lambda _: copy.deepcopy(self.measured),
        )
        host_doc, _ = self.collect()
        self.assertNotIn("codex", host_doc["workers"])
        self.assertIn("cursor", host_doc["workers"])

        # Shared-account quota failure on cursor taints codex-shared for codex too.
        outages = {"cursor": dict(at=T.isoformat(), out_of_usage=True)}
        evidence.produce_probes(
            self.root, at=T, verified_workers=verified_workers,
            verified_accounts=verified_accounts, outages=outages,
            measurement=lambda _: copy.deepcopy(self.measured),
        )
        host_doc, accounts_doc = self.collect()
        self.assertEqual(host_doc["workers"], {})
        self.assertEqual(accounts_doc, {})

    def test_produce_probes_rejects_login_only_and_secret_strings(self):
        verified_workers = {
            "codex": dict(at=T.isoformat(), ready=True, login_only=True, account="codex-shared",
                          auth_evidence="Login successful!", verified_models=["gpt-6.1-sol"]),
        }
        verified_accounts = {
            "codex-shared": dict(at=T.isoformat(), ready=True, limit=1,
                                 quota_evidence="verified quota"),
        }
        evidence.produce_probes(
            self.root, at=T, verified_workers=verified_workers,
            verified_accounts=verified_accounts,
            measurement=lambda _: copy.deepcopy(self.measured),
        )
        self.assertEqual(self.plan()["proposals"], [])

        verified_workers["codex"]["login_only"] = False
        for secret in ["Bearer abcdef123456", "user@example.com", "sk-1234567890abcdef", "token=xyz"]:
            verified_workers["codex"]["auth_evidence"] = secret
            with self.assertRaisesRegex(ValueError, "secret"):
                evidence.produce_probes(
                    self.root, at=T, verified_workers=verified_workers,
                    verified_accounts=verified_accounts,
                    measurement=lambda _: copy.deepcopy(self.measured),
                )

    def serial_written_by_relay(self):
        from contextlib import contextmanager
        import chief_relay as cr
        from test_chief_relay import Relay
        harness = Relay()
        harness.setUp()
        self.addCleanup(harness.tearDown)
        emitted = []
        @contextmanager
        def empty(**kwargs):
            yield None
        def run_cli(*args):
            emitted.append(cr.read_json(cr.d("execution.json")))
            return 0, "fixture completed"
        selected = dict(mode="worker", worker="codex", job=job("J1841"))
        original_collect = evidence.collect
        with patch.dict(os.environ, {"OWB_CAPACITY_ENABLED":"1",
                    "OWB_CAPACITY_ROOT":str(self.root), "CHIEF_CHAIN_MAX":"1"}), \
             patch("capacity_caller.serial_preflight", side_effect=empty), \
             patch("capacity_caller.production_tick", return_value={"state":"capacity_waiting",
                 "admission": {"job": "J1841"}}), \
             patch("serial_admission.finish"), \
             patch.object(cr.workflow, "select_dispatch", return_value=selected), \
             patch.object(cr, "queue_has_work", return_value=True), \
             patch.object(cr, "run_cli", side_effect=run_cli), \
             patch.object(cr, "now", return_value=T), \
             patch.object(cr, "offload_scratch"), \
             patch.object(cr, "fetch_claude_beat"), \
             patch.object(evidence, "reviewed_installation", return_value=HEAD), \
             patch.object(evidence, "collect", side_effect=lambda *a, **kw:original_collect(
                 self.root, at=T, installed_head=HEAD, measurement=lambda _:self.measured)):
            cr.cmd_run(T)
        self.assertEqual(len(emitted), 1)
        return emitted[0]

    def test_real_serial_writer_through_transaction_and_reservation(self):
        import capacity_reservations
        # A Chief's Codex execution and an independent Gemini specialist.
        self.config.update(configured_limit=2, capacity_review="fixture", reviewed_head=HEAD)
        self.config["workers"]["gemini"] = dict(account="gemini-pool", models=["gemini-agy"])
        self.config["accounts"]["gemini-pool"] = 1
        self.probes["workers"]["gemini"] = proof(ready=True, account="gemini-pool",)
        self.probes["workers"]["gemini"]["verified_models"] = ["gemini-agy"]
        self.probes["accounts"]["gemini-pool"] = proof(ready=True, limit=1)
        self.write()
        (self.root / "dispatch.json").write_text('{}')
        (self.root / "dispatch.json").chmod(0o600)
        serial = self.serial_written_by_relay()
        self.assertEqual(serial["account"], "codex-shared")
        self.assertEqual(serial["model"], "gpt-6.1-sol")
        (self.root / "02_Video-Projects").mkdir()
        def observe(alive=True, lease=serial):
            with patch.object(evidence, "reviewed_installation", return_value=HEAD):
                return evidence.transaction_evidence(self.root, lease_root=self.root / "leases",
                    owb_root=self.root, reviewed_head=HEAD, chief="codex", choose_worker=choose,
                    legacy_lease=lease, clock=lambda:T, measurement=lambda _:self.measured,
                    process_alive=lambda pid:alive)
        tx = observe()
        data = {"jobs":[job()]}
        reservation = capacity_reservations.reserve(data, **tx, token="serial-integration-token",
            host_id="registered-mini", worker="gemini")
        self.assertEqual(reservation["worker"], "gemini")
        import capacity_supervisor
        import execution_leases
        import sys
        capacity_reservations.consume(data, token="serial-integration-token",
            host_id="registered-mini", worker="gemini", claimant="gemini", **tx)
        result = capacity_supervisor.run(
            registry=execution_leases.Registry(self.root / "leases", "registered-mini", 2),
            read_claim=lambda:data["jobs"][0], guard=lambda claim:True,
            installed_head=HEAD, reviewed_head=HEAD,
            argv=[sys.executable, "-c", "print('independent specialist')"],
            cwd=self.root, log_path=self.root / "specialist.log", cap_seconds=2,
            preflight=lambda claim, cwd:None, clock=lambda:T)
        self.assertEqual((self.root / "specialist.log").read_text(), "independent specialist\n")
        self.assertEqual(data["jobs"][0]["status"], "claimed")
        # The same account cannot become spare by using the other host.
        self.config["workers"]["gemini"]["account"] = "codex-shared"
        self.probes["workers"]["gemini"]["account"] = "codex-shared"
        self.write()
        tx = observe()
        self.assertEqual(capacity.propose({"jobs":[job()]}, **{k:tx[k] for k in
            ("hosts", "leases", "accounts", "at", "chief", "choose_worker")})["proposals"], [])
        tx = observe(alive=False)
        self.assertTrue(capacity.propose({"jobs":[job()]}, **{k:tx[k] for k in
            ("hosts", "leases", "accounts", "at", "chief", "choose_worker")})["proposals"])
        for change in (dict(account="wrong"), dict(model="unverified"),
                       dict(account_identity={}), dict(host="other")):
            bad = observe(lease=dict(serial, **change))
            self.assertEqual(bad["leases"][0]["account"], "")

    def test_transaction_evidence_combines_boards_and_legacy_lease(self):
        owb = self.root / "owb"
        hos = self.root / "hos"
        (owb / "02_Video-Projects" / "028_Test").mkdir(parents=True)
        (hos / "02_Video-Projects" / "007_Hos").mkdir(parents=True)
        (owb / "02_Video-Projects" / "028_Test" / "status.json").write_text(json.dumps(dict(
            film="028", claims=[dict(stage="edit", by="codex", at=T.isoformat(),
                                     eta=(T + dt.timedelta(minutes=20)).isoformat(), note="live")],
            stages={},
        )))
        (hos / "02_Video-Projects" / "007_Hos" / "status.json").write_text(json.dumps(dict(
            film="007", claims=[], stages={"vo": {"state": "doing"}},
        )))
        with patch.object(evidence, "installed_head", return_value=HEAD):
            tx = evidence.transaction_evidence(
                self.root, lease_root=self.root / "leases", owb_root=owb, hos_root=hos,
                reviewed_head=HEAD, chief="codex", choose_worker=choose,
                legacy_lease=dict(job="J1843", worker="codex", host="registered-mini", pid=101,
                                  startedAt=T.isoformat(), expiresAt=(T + dt.timedelta(minutes=10)).isoformat()),
                clock=lambda: T, measurement=lambda _: copy.deepcopy(self.measured),
                process_alive=lambda pid: True,
            )
        self.assertEqual(tx["stage_claims"], [("hos", "007", "vo"), ("owb", "028", "edit")])
        self.assertEqual(len(tx["leases"]), 1)
        self.assertEqual(tx["leases"][0]["account"], "")
        # Legacy lease without account attribution prevents spare shared-account proposals.
        plan = capacity.propose({"jobs": [job("J1900")]}, tx["hosts"], tx["leases"],
                                tx["accounts"], T, "codex", choose)
        self.assertEqual(plan["proposals"], [])


class ReviewBinding(unittest.TestCase):
    """Chief, 5 Nov 2026 (J2197): only capacity/dispatch/relay/queue code is bound to the reviewed commit."""

    def test_unrelated_changes_keep_the_review_but_bound_code_does_not(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True, text=True).stdout.strip()
            git("init", "-q"); git("config", "user.email", "t@x"); git("config", "user.name", "t")
            (repo / "scripts").mkdir(); (repo / "scripts" / "jobs.py").write_text("v1\n"); (repo / "AGENTS.md").write_text("a\n")
            git("add", "."); git("commit", "-qm", "reviewed"); reviewed = git("rev-parse", "HEAD")
            (repo / "AGENTS.md").write_text("b\n"); (repo / "scripts" / "queue_eta.py").write_text("x\n")
            git("add", "."); git("commit", "-qm", "unrelated")
            self.assertEqual(evidence.reviewed_installation(repo, reviewed), reviewed)
            (repo / "scripts" / "jobs.py").write_text("v2\n"); git("commit", "-qam", "bound")
            with self.assertRaises(ValueError):
                evidence.reviewed_installation(repo, reviewed)


if __name__ == "__main__":
    unittest.main()
