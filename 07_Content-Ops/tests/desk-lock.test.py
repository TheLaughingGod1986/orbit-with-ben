"""Offline lock regression checks: python3 tests/desk-lock.test.py."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

OPS = Path(__file__).resolve().parents[1]
LOCK = OPS / 'scripts/desk-lock.sh'


class DeskLockTests(unittest.TestCase):
    def test_writers_and_cleanup(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            holder = subprocess.Popen(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'sleep', '60'],
                env=env, stdout=subprocess.DEVNULL,
            )
            try:
                for _ in range(200):
                    if (directory / 'owner.txt').exists():
                        break
                    time.sleep(.01)
                self.assertTrue((directory / 'owner.txt').exists())
                for name in ['youtube-package-upload', 'buffer-mirror', 'retitle-videos',
                             'update-pinned-comment', 'set-synthetic-disclosure',
                             'update-shorts-listings']:
                    with self.subTest(writer=name):
                        result = subprocess.run(
                            ['node', '--import', 'tsx', f'scripts/{name}.ts'],
                            cwd=OPS, env=env, capture_output=True, text=True, timeout=10,
                        )
                        self.assertEqual(result.returncode, 75, result.stderr)
            finally:
                holder.terminate()
                holder.wait(timeout=10)
            self.assertFalse(directory.exists())
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'bash', '-c', 'exit 23'],
                env=env, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 23)
            self.assertFalse(directory.exists())
            # No arguments hits usage offline, verifying nested lock inheritance.
            result = subprocess.run(
                ['node', '--import', 'tsx', 'scripts/buffer-mirror.ts'],
                cwd=OPS, env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('Usage:', result.stderr)
            self.assertFalse(directory.exists())
            # A competing creator may not have written metadata yet.
            directory.mkdir()
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'true'],
                env=env, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 75)
            self.assertTrue(directory.exists())


if __name__ == '__main__':
    unittest.main()
