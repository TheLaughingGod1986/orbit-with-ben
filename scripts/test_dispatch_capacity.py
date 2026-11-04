"""Capacity regressions use synthetic evidence; never launch or spend."""
import copy
import datetime as dt
import hashlib
import pathlib
import tempfile
import unittest

import dispatch_capacity as capacity

T = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)
STAMP = T.isoformat()
END = (T+dt.timedelta(minutes=5)).isoformat()


def proof(**kw):
    return dict(at=STAMP, expiresAt=END, auth_evidence="noninteractive status probe",
                quota_evidence="current account quota observation",
                verified_models=["gpt-6.1-sol", "gemini-agy", "cursor-grok-4-7"], **kw)


def host(name="mini", worker="codex", **kw):
    value = proof(host=name, registered_id=name, role=name, state="idle", guard_reasons=[],
                  free_gb=30, min_free_gb=20, load=1, max_load=4,
                  memory_available_gb=8, min_memory_gb=2, configured_limit=1,
                  workers={worker:proof(ready=True, account="shared", capabilities={})})
    if name == "macbook":
        value.update(on_ac=True, idle_minutes=20)
    value.update(kw)
    return value


def job(id="J1834", **kw):
    value = dict(id=id, status="open", needs="mini", kind="assembly", title=id,
                 remaining_action="build approved CPU output", after=None, execution_resources=["cpu"],
                 no_spend=True, no_publish=True)
    value.update(kw)
    return value


def portable():
    return dict(version=1, approved_by="codex", approval_ref="scope-123", no_spend=True,
                no_publish=True, resources=["cpu"], inputs=[], output_receipts_required=True)


def choose(j, eligible):
    return next((w for w in ["codex", "gemini", "cursor"] if w in eligible), None)


class Capacity(unittest.TestCase):
    def plan(self, jobs=None, hosts=None, leases=None, accounts=None):
        return capacity.propose({"jobs":jobs or [job()]}, hosts or [host()], leases or [],
                                accounts if accounts is not None else {"shared":proof(ready=True, limit=1)},
                                T, "codex", choose)

    def test_free_lane_proposes_immediately_without_claiming(self):
        original = [job()]
        before = copy.deepcopy(original)
        result = self.plan(jobs=original)
        self.assertEqual(result["proposals"][0]["job"], "J1834")
        self.assertEqual(result["proposals"][0]["phase"], "proposed")
        self.assertEqual(original, before)
        self.assertIsNone(result["free_slot_at"])

    def test_busy_chief_does_not_block_an_independent_specialist(self):
        lease = dict(job="J1841", worker="codex", host="mini", account="shared")
        self.assertEqual(self.plan(hosts=[host(worker="gemini", configured_limit=2,
            capacity_review="review", installed_head="abc", reviewed_head="abc")], leases=[lease],
            accounts={"shared":proof(ready=True, limit=2)})["proposals"][0]["worker"], "gemini")

    def test_busy_mini_proposes_portable_on_laptop_once(self):
        lease = dict(job="J1841", worker="gemini", host="mini", account="gemini")
        result = self.plan(jobs=[job(portable=portable())], hosts=[host(worker="gemini"), host("macbook")], leases=[lease])
        self.assertEqual(len(result["proposals"]), 1)
        self.assertEqual(result["proposals"][0]["host"], "macbook")

    def test_shared_codex_account_cannot_be_reset_by_changing_host(self):
        self.assertEqual(self.plan(hosts=[host("macbook")], jobs=[job(portable=portable())],
            leases=[dict(job="J1841", worker="other", host="mini", account="shared")])["proposals"], [])

    def test_unknown_legacy_account_is_not_spare_capacity(self):
        self.assertEqual(self.plan(leases=[dict(job="J1841", worker="other", host="other")])["proposals"], [])

    def test_laptop_battery_in_use_offline_unregistered_and_low_resources(self):
        variants = [dict(on_ac=False), dict(idle_minutes=2), dict(state="offline"),
                    dict(registered_id=""), dict(free_gb=2), dict(load=9),
                    dict(memory_available_gb=0), dict(load=float("nan")),
                    dict(at=(T-dt.timedelta(minutes=6)).isoformat())]
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(self.plan(hosts=[host("macbook", **variant)], jobs=[job(portable=portable())])["proposals"], [])

    def test_idle_mini_does_not_send_work_to_laptop(self):
        # No portable overflow while a real Mini lane remains available.
        unavailable = host(workers={})
        result = self.plan(jobs=[job(portable=portable())], hosts=[unavailable, host("macbook")])
        self.assertEqual(result["proposals"], [])
        self.assertIn("exhaustion", result["host_rejections"]["macbook"])

    def test_missing_model_probe_cannot_become_fallback(self):
        workers = {"codex":proof(ready=True, account="shared")}
        workers["codex"]["verified_models"] = []
        self.assertEqual(self.plan(hosts=[host(workers=workers)])["proposals"], [])

    def test_ready_boolean_without_probe_is_insufficient(self):
        workers = {"codex":proof(ready=True, account="shared")}
        workers["codex"]["auth_evidence"] = ""
        self.assertEqual(self.plan(hosts=[host(workers=workers)])["proposals"], [])
        account = proof(ready=True, limit=1)
        account["quota_evidence"] = ""
        self.assertEqual(self.plan(accounts={"shared":account})["proposals"], [])

    def test_second_lane_needs_exact_head_review(self):
        for changes in ({}, {"capacity_review":"x", "reviewed_head":"old", "installed_head":"new"}):
            self.assertEqual(self.plan(hosts=[host(configured_limit=2, **changes)])["proposals"], [])

    def test_no_duplicate_job_or_stage_across_hosts(self):
        first = job(film="030", stage="picture")
        second = job("J1841", film="030", stage="picture", portable=portable())
        result = self.plan(jobs=[first, second], hosts=[host(), host("macbook", worker="gemini")],
                           accounts={"shared":proof(ready=True, limit=2)})
        self.assertEqual(len(result["proposals"]), 1)

    def test_existing_claimed_stage_is_preserved(self):
        claimed = job("J1841", status="claimed", by="codex", film="030", stage="picture")
        self.assertEqual(self.plan(jobs=[claimed, job(film="030", stage="picture")])["proposals"], [])

    def test_model_outage_walks_only_capable_fallback(self):
        workers = {"codex":proof(ready=False, account="shared"), "gemini":proof(ready=True, account="shared")}
        self.assertEqual(self.plan(hosts=[host(workers=workers)])["proposals"][0]["worker"], "gemini")
        self.assertEqual(self.plan(hosts=[host(workers=workers)], jobs=[job(required_capabilities=["moving_video_input"])])["proposals"], [])
        workers["gemini"]["capabilities"] = proof(available=["moving_video_input"], evidence="actual video probe")
        self.assertEqual(self.plan(hosts=[host(workers=workers)], jobs=[job(required_capabilities=["moving_video_input"])])["proposals"][0]["worker"], "gemini")

    def test_unknown_or_stale_auth_and_quota_are_not_ready(self):
        for account in ({}, proof(ready=False, limit=1), dict(at="2026-11-01T00:00Z", expiresAt=END, ready=True, limit=1)):
            self.assertEqual(self.plan(accounts={"shared":account})["proposals"], [])

    def test_chief_decision_and_delivered_review_are_not_overflow(self):
        for candidate in (job(kind="chief"), job(status="blocked", reason="parked for Chief: review J1834 delivery")):
            self.assertEqual(self.plan(jobs=[candidate])["proposals"], [])

    def test_ben_dependency_and_capability_holds_are_preserved(self):
        for candidate in (job(awaits_ben={"what":"finished cut"}), job(after="Jmissing"),
                          job(required_capabilities=["audio_input"])):
            with self.subTest(candidate=candidate):
                self.assertEqual(self.plan(jobs=[candidate])["proposals"], [])

    def test_future_display_check_is_not_added_as_a_start_delay(self):
        # An open ready task stays ready; real structured holds are still workflow-owned.
        self.assertEqual(len(self.plan(jobs=[job(check_at="2026-12-01T00:00Z")])["proposals"]), 1)

    def test_unscoped_or_single_writer_work_is_not_parallel(self):
        for candidate in (job(execution_resources=["browser"]), job(kind="video"), job(no_spend=False), job(no_publish=False)):
            self.assertEqual(self.plan(jobs=[candidate])["proposals"], [])

    def test_portable_contract_rejects_missing_inputs_and_unsupported_work(self):
        for changes in ({"resources":["nas"]}, {"inputs":None}, {"output_receipts_required":False},
                        {"approval_ref":""}):
            contract = dict(portable(), **changes)
            self.assertTrue(capacity.portable_problem(job(portable=contract), host("macbook"), T))

    def test_portable_hash_receipts_are_fresh_and_exact(self):
        contract = portable()
        contract["inputs"] = [dict(path="assets/approved.txt", sha256="a"*64, approval_ref="KEEP")]
        candidate = job(portable=contract)
        laptop = host("macbook")
        self.assertTrue(capacity.portable_problem(candidate, laptop, T))
        laptop["input_receipts"] = {"assets/approved.txt":proof(sha256="a"*64, readable=True)}
        self.assertEqual(capacity.portable_problem(candidate, laptop, T), "")
        contract["inputs"][0]["path"] = "/Volumes/data/private"
        self.assertTrue(capacity.portable_problem(candidate, laptop, T))

    def test_local_input_verification_rejects_changed_bytes_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root/"ok").write_bytes(b"approved")
            contract = dict(inputs=[dict(path="ok", sha256=hashlib.sha256(b"approved").hexdigest())])
            capacity.verify_inputs(contract, root)
            (root/"ok").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                capacity.verify_inputs(contract, root)
            (root/"escape").symlink_to(root.parent)
            contract["inputs"][0]["path"] = "escape/anything"
            with self.assertRaises((ValueError, FileNotFoundError)):
                capacity.verify_inputs(contract, root)

    def test_dead_expired_and_remote_pid_leases(self):
        base = dict(job="J1841", worker="codex", host="mini", pid=100, startedAt=STAMP, expiresAt=END)
        self.assertEqual(capacity.live_leases([base], T, "mini", lambda p:False), [])
        self.assertEqual(len(capacity.live_leases([base], T, "mini", lambda p:True)), 1)
        self.assertEqual(capacity.live_leases([dict(base, expiresAt=STAMP)], T, "mini", lambda p:True), [])
        remote = dict(base, host="macbook", at=STAMP, process_validated=True)
        self.assertEqual(len(capacity.live_leases([remote], T, "mini", lambda p:False)), 1)
        self.assertEqual(capacity.live_leases([dict(remote, at="2026-11-01T00:00Z")], T, "mini", lambda p:True), [])


if __name__ == "__main__":
    unittest.main()
