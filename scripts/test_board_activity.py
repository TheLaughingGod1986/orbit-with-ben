"""Execute the simple board's actual JavaScript against progress and blocker regressions."""
import shutil
import subprocess
import unittest
from pathlib import Path


class TrackerActivity(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'node is required for browser logic checks')
    def test_tracker_activity(self):
        result = subprocess.run(['node', str(Path(__file__).with_name('test_tracker_activity.cjs'))],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
