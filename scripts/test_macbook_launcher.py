"""Exercise the actual launch command with fake git/python, never live services."""
import importlib.util
import os
import pathlib
import plistlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import macbook_worker as worker

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("renderer", HERE / "macbook/render_worker_plist.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


@unittest.skipUnless(shutil.which("zsh"), "launcher requires zsh")
class Launcher(unittest.TestCase):
    def exercise(self, existing=False, failed_clone=False, separate=True):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            channel = root / "channel"
            engine = root / ('studio & $(touch INJECTED)' if separate else "channel")
            url = "https://example.invalid/engine.git"
            doc = plistlib.loads(renderer.render(root, engine, url, channel, root / "second channel", "model"))
            self.assertEqual(doc["EnvironmentVariables"]["OWB_REPO"], str(channel))
            self.assertEqual(doc["EnvironmentVariables"]["STUDIO_REPO"], str(engine))
            if existing:
                (engine / "scripts").mkdir(parents=True)
                (engine / "scripts/macbook_worker.py").touch()
            bins = root / "bin"
            bins.mkdir()
            for name, body in {
                "git": 'printf "git:%s\\n" "$*" >> "$PROBE_LOG"\nexit "${CLONE_RC:-0}"',
                "python3": 'printf "python:%s\\n" "$*" >> "$PROBE_LOG"',
            }.items():
                path = bins / name
                path.write_text("#!/bin/sh\n" + body + "\n")
                path.chmod(0o755)
            log = root / "calls"
            env = dict(os.environ, **doc["EnvironmentVariables"])
            env.update(PATH=str(bins) + ":/usr/bin:/bin", PROBE_LOG=str(log), CLONE_RC="1" if failed_clone else "0")
            # Omit login startup files so a user's PATH cannot replace the fakes.
            result = subprocess.run(["zsh", "-c", doc["ProgramArguments"][-1]], env=env, cwd=root, capture_output=True)
            calls = log.read_text()
            self.assertFalse((root / "INJECTED").exists())
            self.assertEqual("git:" in calls, not existing)
            if not existing:
                self.assertIn("--branch main", calls)
                self.assertIn(url, calls)
            self.assertEqual("python:" in calls, not failed_clone)
            if not failed_clone:
                self.assertIn(str(engine / "scripts/macbook_worker.py") + " run", calls)
            self.assertEqual(result.returncode, 1 if failed_clone else 0)

    def test_existing_engine_uses_no_clone(self):
        self.exercise(existing=True)

    def test_missing_engine_clones_the_engine_not_channel(self):
        self.exercise()

    def test_clone_failure_does_not_start_worker(self):
        self.exercise(failed_clone=True)

    def test_before_split_engine_can_still_be_channel(self):
        self.exercise(separate=False)


class SeparateEngineSlots(unittest.TestCase):
    def test_slot_two_overrides_inherited_slot_one_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            spawned = mock.Mock()
            with mock.patch.object(worker, "HOME", root), \
                    mock.patch.object(worker, "WORKER_DIR", root / "worker"), \
                    mock.patch.object(worker, "SLOT", 1), mock.patch.object(worker, "SLOTS", 2), \
                    mock.patch.object(worker.channels, "studio_repo", return_value={
                        "env": "STUDIO_REPO", "url": "https://example.invalid/studio.git"}), \
                    mock.patch.dict(os.environ, {"STUDIO_REPO": str(root / "worker/studio")}):
                self.assertEqual(worker.start_other_slots(popen=spawned, system="Darwin"), [2])
            env = spawned.call_args.kwargs["env"]
            self.assertEqual(env["MACBOOK_SLOT"], "2")
            self.assertEqual(env["STUDIO_REPO"], str(root / "worker/slot2/studio"))


if __name__ == "__main__":
    unittest.main()
