import datetime as dt
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import subprocess

from execution_leases import Registry, process_identity, group_members

T = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)


class Leases(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.processes = {101: "start-A", 102: "start-B"}
        self.registry = Registry(self.tmp.name, "mini", 1, probe=self.processes.get,
                                 child_probe=self.processes.get)
        self.reservation = dict(host="mini", token="token-A", job="J1834", worker="codex",
            account="shared", phase="reserved", at=T.isoformat(),
            expiresAt=(T + dt.timedelta(minutes=2)).isoformat())

    def test_record_is_process_proof_not_queue_claim_or_slot_eta(self):
        row = self.registry.record(self.reservation, 101, T, 120)
        self.assertEqual(row["phase"], "starting")
        self.assertTrue(self.registry.observe(T)[0]["process_validated"])

    def test_duplicate_launch_and_second_slot_rejected(self):
        self.registry.record(self.reservation, 101, T, 120)
        self.assertEqual(self.registry.record(self.reservation, 101, T, 120)["pid"], 101)
        with self.assertRaises(ValueError):
            self.registry.record(self.reservation, 102, T, 120)
        with self.assertRaises(ValueError):
            self.registry.record(dict(self.reservation, token="token-B", job="J1841"), 102, T, 120)

    def test_dead_process_and_pid_reuse_release_capacity(self):
        for replacement in [None, "reused-PID-new-start"]:
            with self.subTest(replacement=replacement):
                self.processes[101] = "start-A"
                self.registry.record(self.reservation, 101, T, 120)
                self.processes[101] = replacement
                self.assertEqual(self.registry.observe(T), [])

    def test_expiry_and_unknown_process_fail_closed(self):
        with self.assertRaises(ValueError):
            self.registry.record(self.reservation, 999, T, 120)
        with self.assertRaises(ValueError):
            self.registry.record(self.reservation, 101, T + dt.timedelta(minutes=3), 120)
        self.registry.record(self.reservation, 101, T, 120)
        overdue = self.registry.observe(T + dt.timedelta(seconds=120))
        self.assertTrue(overdue[0]["overdue"])
        with self.assertRaises(ValueError):
            self.registry.record(dict(self.reservation, token="token-B", job="J1841",
                expiresAt=(T + dt.timedelta(minutes=5)).isoformat()), 102,
                T + dt.timedelta(seconds=120), 120)
        self.processes[101] = None
        self.assertEqual(self.registry.observe(T + dt.timedelta(seconds=120)), [])

    def test_finish_cannot_remove_another_supervisor(self):
        self.registry.record(self.reservation, 101, T, 120)
        with self.assertRaises(ValueError):
            self.registry.finish("token-A", 102)
        self.assertTrue(self.registry.finish("token-A", 101))
        self.assertFalse(self.registry.finish("token-A", 101))

    def test_dead_armed_supervisor_quarantines_possible_orphan(self):
        self.registry.record(self.reservation, 101, T, 120)
        with self.assertRaises(ValueError):
            self.registry.arm("token-A", 102)
        self.registry.arm("token-A", 101)
        self.processes[101] = None
        row = self.registry.observe(T + dt.timedelta(hours=1))[0]
        self.assertTrue(row["recovery_required"])
        self.assertFalse(row["process_validated"])
        with self.assertRaisesRegex(ValueError, "capacity"):
            self.registry.record(dict(self.reservation, token="new", job="J1841"), 102, T, 120)

    def test_corrupt_state_or_foreign_host_is_not_free_capacity(self):
        path = pathlib.Path(self.tmp.name) / "mini.json"
        path.write_text("broken")
        with self.assertRaises(ValueError):
            self.registry.observe(T)
        path.write_text(json.dumps([dict(host="remote")]))
        with self.assertRaises(ValueError):
            self.registry.observe(T)

    def test_real_local_process_identity_and_dead_pid(self):
        self.assertIsNotNone(process_identity(os.getpid()))
        self.assertIsNone(process_identity(-1))

    def test_malformed_row_and_denied_probe_never_disappear_as_free_capacity(self):
        row = self.registry.record(self.reservation, 101, T, 120)
        path = pathlib.Path(self.tmp.name) / "mini.json"
        for change in (dict(pid=None), dict(process_identity=""), dict(startedAt="bad"),
                       dict(startedAt=(T+dt.timedelta(minutes=1)).isoformat()), dict(token="")):
            path.write_text(json.dumps([dict(row, **change)]))
            with self.subTest(change=change):
                for method in (self.registry.observe, self.registry.reconcile):
                    before = path.read_bytes()
                    with self.assertRaises(ValueError):
                        method(T)
                    self.assertEqual(path.read_bytes(), before)
        path.write_text(json.dumps([row]))
        def denied(pid):
            raise PermissionError("denied")
        self.registry.probe = denied
        with self.assertRaises(PermissionError):
            self.registry.observe(T)
        self.assertEqual(self.registry.reconcile(T)[0]["phase"], "quarantined")
        self.assertEqual(len(json.loads(path.read_text())), 1)

    def orphan(self, child=201):
        self.registry.record(self.reservation, 101, T, 120)
        self.registry.arm("token-A", 101)
        self.processes[child] = "child-start"
        with patch("execution_leases.os.getpgid", return_value=child):
            self.registry.attach("token-A", 101, child)
        self.processes[101] = None

    def test_reconcile_kills_only_recorded_orphan_then_confirms_empty_group(self):
        self.orphan()
        groups = {201: [201, 202]}
        signals = []
        def kill(pid, sig):
            signals.append((pid, sig))
            groups[pid] = []
        result = self.registry.reconcile(T, members=lambda p:groups[p], kill_group=kill)
        self.assertEqual(result[0]["phase"], "orphan_recovered")
        self.assertEqual([p for p, _ in signals], [201])
        self.assertEqual(self.registry.observe(T), [])

    def test_reconcile_never_signals_live_even_overdue_supervisor(self):
        self.orphan()
        self.processes[101] = "start-A"
        def forbidden(*args):
            self.fail("live supervisor must not trigger orphan recovery")
        self.assertEqual(self.registry.reconcile(T+dt.timedelta(hours=1),
            members=forbidden, kill_group=forbidden), [])
        self.assertTrue(self.registry.observe(T+dt.timedelta(hours=1))[0]["overdue"])

    def test_reused_or_absent_child_with_surviving_group_stays_quarantined(self):
        self.orphan()
        for identity, members in (("reused-start", [201]), (None, [202])):
            with self.subTest(identity=identity):
                self.processes[201] = identity
                result = self.registry.reconcile(T, members=lambda p:members,
                    kill_group=lambda *a:self.fail("unproven group must not be signalled"))
                self.assertEqual(result[0]["phase"], "quarantined")
                self.assertTrue(self.registry.observe(T)[0]["recovery_required"])

    def test_empty_recorded_group_recovers_without_kill_or_queue_action(self):
        self.orphan()
        self.processes[201] = None
        result = self.registry.reconcile(T, members=lambda p:[],
            kill_group=lambda *a:self.fail("empty group must not be signalled"))
        self.assertEqual(result[0]["phase"], "orphan_recovered")
        self.assertEqual(self.registry.observe(T), [])

    def test_unknown_spawn_gap_remains_quarantined(self):
        self.registry.record(self.reservation, 101, T, 120)
        self.registry.arm("token-A", 101)
        self.processes[101] = None
        self.assertEqual(self.registry.reconcile(T)[0]["phase"], "quarantined")
        self.assertEqual(len(self.registry.observe(T)), 1)

    def test_failed_probe_or_unconfirmed_cleanup_stays_occupied(self):
        self.orphan()
        def denied(*args):
            raise PermissionError("denied")
        for members, kill in ((denied, lambda *a:None), (lambda p:[201], denied)):
            with self.subTest(members=members):
                self.assertEqual(self.registry.reconcile(T, members=members, kill_group=kill)[0]["phase"], "quarantined")
        ticks = iter([0, 0, 3])
        self.assertEqual(self.registry.reconcile(T, members=lambda p:[201],
            kill_group=lambda *a:None, monotonic=lambda:next(ticks), pause=lambda n:None)[0]["phase"], "quarantined")
        self.assertEqual(len(self.registry.observe(T)), 1)

    def test_attach_rejects_another_supervisor_and_non_session_child(self):
        self.registry.record(self.reservation, 101, T, 120)
        self.registry.arm("token-A", 101)
        self.processes[201] = "child"
        with patch("execution_leases.os.getpgid", return_value=201):
            with self.assertRaises(ValueError):
                self.registry.attach("token-A", 102, 201)
        with patch("execution_leases.os.getpgid", return_value=101):
            with self.assertRaises(ValueError):
                self.registry.attach("token-A", 101, 201)

    def test_probe_failures_are_not_exit_evidence(self):
        for result in (subprocess.CompletedProcess([], 1, "", "permission denied"),
                       subprocess.CompletedProcess([], 0, "", "")):
            with patch("execution_leases.subprocess.run", return_value=result):
                with self.assertRaises(RuntimeError):
                    process_identity(123)
        with patch("execution_leases.subprocess.run", side_effect=PermissionError):
            with self.assertRaises(RuntimeError):
                process_identity(123)
        with patch("execution_leases.subprocess.run", return_value=subprocess.CompletedProcess([], 1, "", "")):
            self.assertIsNone(process_identity(123))

    def test_group_probe_rejects_unavailable_or_malformed_tables_and_ignores_zombies(self):
        for status, output, error in ((1, "", "denied"), (0, "", ""), (0, "nonsense", "")):
            with patch("execution_leases.subprocess.run", return_value=subprocess.CompletedProcess([], status, output, error)):
                with self.assertRaises(RuntimeError):
                    group_members(201)
        with patch("execution_leases.subprocess.run", return_value=subprocess.CompletedProcess([], 0,
                   "201 201 S\n202 201 Z\n203 999 S\n", "")):
            self.assertEqual(group_members(201), [201])


if __name__ == "__main__":
    unittest.main()
