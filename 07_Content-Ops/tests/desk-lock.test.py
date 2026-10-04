"""Offline lock regression checks: python3 tests/desk-lock.test.py."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

OPS = Path(__file__).resolve().parents[1]
REPO = OPS.parent
LOCK = OPS / 'scripts/desk-lock.sh'
BUFFER_CHECK = OPS / 'launchd/buffer-check.sh'


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

    def test_stale_reclaim_when_pid_dead_and_owner_older_than_5m(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            directory.mkdir()
            owner = directory / 'owner.txt'
            # Use a pid that is almost certainly dead and not ours.
            owner.write_text('pid=1\nuser=test\nstarted_at=1970-01-01T00:00:00+0000\n')
            # Make owner.txt older than 5 minutes.
            old = time.time() - 301
            os.utime(owner, (old, old))
            # If pid 1 is alive (init/launchd), pick another dead pid.
            if subprocess.call(['kill', '-0', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                owner.write_text('pid=2147483646\nuser=test\nstarted_at=1970-01-01T00:00:00+0000\n')
                os.utime(owner, (old, old))
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'bash', '-c', 'exit 42'],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 42, result.stderr)
            self.assertFalse(directory.exists())

    def test_fresh_dead_owner_is_not_reclaimed(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            directory.mkdir()
            owner = directory / 'owner.txt'
            owner.write_text('pid=2147483646\nuser=test\nstarted_at=recent\n')
            # Fresh mtime (<5m): fail closed even though pid is dead.
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'true'],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 75, result.stderr)
            self.assertTrue(directory.exists())

    def test_buffer_check_notifies_on_second_consecutive_75(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            bin_dir = Path(root) / 'bin'
            bin_dir.mkdir()
            notify_log = Path(root) / 'notify.log'
            osascript = bin_dir / 'osascript'
            osascript.write_text(
                '#!/bin/bash\necho "$@" >> "$NOTIFY_LOG"\n'
            )
            osascript.chmod(0o755)
            # Hold the lock so buffer-check's desk-lock wrapper exits 75.
            directory = Path(root) / 'youtube-buffer.lock'
            directory.mkdir()
            (directory / 'owner.txt').write_text(f'pid={os.getpid()}\nuser=test\n')
            env = {
                **os.environ,
                'DESK_LOCK_ROOT': root,
                'ORBIT_REPO': str(REPO),
                'PATH': f'{bin_dir}:{os.environ.get("PATH", "")}',
                'NOTIFY_LOG': str(notify_log),
            }
            first = subprocess.run(['bash', str(BUFFER_CHECK)], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(first.returncode, 75, first.stderr + first.stdout)
            self.assertFalse(notify_log.exists(), 'first 75 must stay quiet')
            second = subprocess.run(['bash', str(BUFFER_CHECK)], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(second.returncode, 75, second.stderr + second.stdout)
            self.assertTrue(notify_log.exists(), 'second consecutive 75 must notify')
            self.assertIn('twice in a row', notify_log.read_text())


if __name__ == '__main__':
    unittest.main()
