"""Retired daily timers must stop before Git, APIs, or the watchdog run."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class TimerGuard(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'engine'
        self.home = self.base / 'home'
        self.bin = self.base / 'bin'
        for folder in (self.root / 'scripts', self.root / 'channels',
                       self.root / '07_Content-Ops/launchd', self.home / '_desk/state', self.bin):
            folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / 'scripts/engine_guard.py', self.root / 'scripts/engine_guard.py')
        (self.root / 'channels/channels.json').write_text(json.dumps({'studio': {'github': 'test/old'}}))
        self.marker = self.home / '_desk/state/active-studio.json'
        self.trace = self.base / 'side-effects'
        for command in ('git', 'npx', 'perl', 'osascript', 'mkdir', 'ln'):
            executable = self.bin / command
            executable.write_text('#!/bin/sh\nprintf "%s\\n" "$0" >> "$TRACE"\nexit 91\n')
            executable.chmod(0o755)
        (self.bin / 'python3').symlink_to(sys.executable)
        self.env = dict(os.environ, HOME=str(self.home), PATH=f'{self.bin}:/usr/bin:/bin',
                        TRACE=str(self.trace), STUDIO_REPO=str(self.root), ORBIT_REPO=str(self.root))

    def run_timer(self, name, sourced=False):
        script = self.root / '07_Content-Ops/launchd' / name
        shutil.copy2(SOURCE / '07_Content-Ops/launchd' / name, script)
        args = ['bash', '-c', 'source "$1"; main', 'test', str(script)] if sourced else ['bash', str(script)]
        return subprocess.run(args, env=self.env, capture_output=True, text=True, timeout=10)

    def test_retired_and_malformed_markers_refuse_before_any_external_work(self):
        for marker in (json.dumps({'version': 1, 'github': 'test/new'}), 'not-json'):
            self.marker.write_text(marker)
            for name in ('buffer-check.sh', 'analytics-snapshot.sh'):
                for sourced in (False, True):
                    with self.subTest(name=name, marker=marker, sourced=sourced):
                        result = self.run_timer(name, sourced)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn('engine', result.stderr.lower())
                        self.assertNotIn('not-json', result.stderr)
                        self.assertFalse(self.trace.exists(), result.stdout + result.stderr)

    def test_guard_cli_allows_unarmed_and_matching_identity(self):
        for armed in (False, True):
            if armed:
                self.marker.write_text(json.dumps({'version': 1, 'github': 'test/old'}))
            result = subprocess.run([sys.executable, str(self.root / 'scripts/engine_guard.py')],
                                    env=self.env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout + result.stderr, '')

    def test_active_wrapper_cannot_select_a_retired_runtime(self):
        self.marker.write_text(json.dumps({'version': 1, 'github': 'test/old'}))
        retired = self.base / 'retired'
        (retired / 'scripts').mkdir(parents=True)
        (retired / 'channels').mkdir()
        shutil.copy2(SOURCE / 'scripts/engine_guard.py', retired / 'scripts/engine_guard.py')
        (retired / 'channels/channels.json').write_text(json.dumps({'studio': {'github': 'test/retired'}}))
        self.env['ORBIT_REPO'] = str(retired)
        self.env['STUDIO_REPO'] = str(retired)
        for name in ('buffer-check.sh', 'analytics-snapshot.sh'):
            result = self.run_timer(name, sourced=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('retired', result.stderr)
            self.assertFalse(self.trace.exists(), result.stdout + result.stderr)

    def test_missing_guard_fails_closed_before_work(self):
        (self.root / 'scripts/engine_guard.py').unlink()
        for name in ('buffer-check.sh', 'analytics-snapshot.sh'):
            result = self.run_timer(name)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.trace.exists(), result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
