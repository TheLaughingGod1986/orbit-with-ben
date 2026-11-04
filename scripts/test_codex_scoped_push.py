import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('gateway', Path(__file__).with_name('codex_scoped_push.py'))
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)

class ScopedPushTests(unittest.TestCase):
    def args(self, *extra):
        return ['--repo', 'owb', '--worktree', '/private/tmp/j2040-wt', '--branch', 'codex/check', *extra]

    @patch.object(gateway.subprocess, 'run')
    def test_exact_nonforcing_destination(self, run):
        run.side_effect = [SimpleNamespace(returncode=0), SimpleNamespace(returncode=1)]
        cmd, env = gateway.command(self.args('--dry-run'))
        self.assertEqual(cmd[-2:], [gateway.REPOS['owb'], 'HEAD:refs/heads/codex/check'])
        for flag in ['--no-force', '--no-mirror', '--no-follow-tags', '--recurse-submodules=no', '--dry-run']:
            self.assertIn(flag, cmd)
        self.assertFalse(any(k.startswith('GIT_') for k in env))

    def test_options_and_refspecs_rejected(self):
        cases = [self.args('--force'), self.args('--delete'), self.args('--repo', 'other'),
                 self.args('--branch', '+main'), self.args('--branch', ':main'),
                 self.args('--branch', 'main:other'), self.args('--branch', '--force')]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(SystemExit):
                gateway.command(args)

    @patch.object(gateway.subprocess, 'run')
    def test_url_rewrites_rejected(self, run):
        run.side_effect = [SimpleNamespace(returncode=0), SimpleNamespace(returncode=0)]
        with self.assertRaises(SystemExit):
            gateway.command(self.args())

if __name__ == '__main__':
    unittest.main()
