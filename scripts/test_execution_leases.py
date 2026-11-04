import datetime as dt
import json
import os
import pathlib
import tempfile
import unittest

from execution_leases import Registry, process_identity

T = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)


class Leases(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.processes = {101: "start-A", 102: "start-B"}
        self.registry = Registry(self.tmp.name, "mini", 1, probe=self.processes.get)
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


if __name__ == "__main__":
    unittest.main()
