"""Read-only capacity reporting must distinguish launching, claiming and estimates."""
import datetime as dt
import unittest
from unittest.mock import patch
import subprocess

import chief_relay as relay
import macbook_worker as laptop

AT = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)


class Observation(unittest.TestCase):
    def test_lease_is_starting_until_canonical_claim_and_slot_is_unknown(self):
        lease = dict(job="J1843", worker="codex", expiresAt="2026-11-04T00:25Z")
        queue = {"jobs":[dict(id="J1843", status="open", eta_min=120,
                              remaining_action="verify implementation", progress={"step":1,"of":3})]}
        with patch.object(relay, "current_execution", return_value=lease), \
             patch.object(relay, "read_json", return_value=queue), \
             patch.object(relay.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "")):
            result = relay.capacity_observation(AT)
            self.assertEqual(result["active"][0]["phase"], "starting")
            self.assertEqual(result["active"][0]["action"], "verify implementation")
            self.assertEqual(result["active"][0]["recorded_task_estimate_minutes"], 120)
            self.assertIsNone(result["free_slot_at"])
            self.assertFalse(result["macbook_capacity_verified"])
            queue["jobs"][0]["status"] = "claimed"
            self.assertEqual(relay.capacity_observation(AT)["active"][0]["phase"], "running")

    def test_unavailable_heartbeat_does_not_imply_idle_capacity(self):
        with patch.object(relay, "current_execution", return_value=None), \
             patch.object(relay, "read_json", return_value={}), \
             patch.object(relay.subprocess, "run", side_effect=OSError):
            result = relay.capacity_observation(AT)
            self.assertIsNone(result["macbook_cached_observation"])
            self.assertEqual(result["availability"], "unknown")

    def test_laptop_heartbeat_has_observed_identity_without_invented_registration(self):
        with patch.object(laptop, "on_ac_power", return_value=True), \
             patch.object(laptop, "idle_minutes", return_value=22), \
             patch.object(laptop.platform, "node", return_value="actual-machine"):
            result = laptop.heartbeat_doc("idle", [], now=AT)
            self.assertEqual(result["host"], "macbook")
            self.assertEqual(result["observation"]["machine_name"], "actual-machine")
            self.assertIsNone(result["observation"]["registered_id"])
            self.assertIsNone(result["observation"]["auth_quota_ready"])
            self.assertEqual(result["observation"]["media_capabilities"], [])


if __name__ == "__main__":
    unittest.main()
