"""Probe prepared Mini launchers without touching launchd or any live engine."""
import importlib.util
import os
import pathlib
import plistlib
import subprocess
import sys
import tempfile
import unittest

TOOL = pathlib.Path(__file__).parent / 'mini' / 'render_service_plist.py'
spec = importlib.util.spec_from_file_location('mini_plist', TOOL)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class MiniServicePlist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.engine = self.root / 'engine $(touch INJECTED) & space'
        (self.engine / 'scripts').mkdir(parents=True)
        for script, _ in renderer.SERVICES.values():
            (self.engine / 'scripts' / script).write_text(
                'import os, sys\nprint(os.environ["STUDIO_REPO"])\nprint(sys.argv[1])\n')
        self.channels = {'OWB_REPO': str(self.root / 'channel one'),
                         'HOS_REPO': str(self.root / 'channel two'),
                         'WW2_REPO': str(self.root / 'channel three')}
        self.source = {'Label': 'com.owb.chief-relay', 'Program': '/old/runner',
                       'ProgramArguments': ['old'], 'StartInterval': 60, 'RunAtLoad': True,
                       'StandardOutPath': '/unchanged/log', 'Nice': 10,
                       'EnvironmentVariables': {'PATH': '/old/path', 'DESK_STATE': '/shared/state',
                                                'STUDIO_SCRATCH': '/existing/scratch'}}

    def render(self, source=None):
        return plistlib.loads(renderer.render(source or self.source, self.engine, sys.executable, self.channels))

    def test_both_launchers_execute_exact_staged_engine_without_shell_expansion(self):
        for label, (_, arg) in renderer.SERVICES.items():
            with self.subTest(label=label):
                source = dict(self.source, Label=label)
                doc = self.render(source)
                env = dict(os.environ, **doc['EnvironmentVariables'])
                out = subprocess.run(doc['ProgramArguments'], cwd=doc['WorkingDirectory'], env=env,
                                     check=True, capture_output=True, text=True)
                self.assertEqual(out.stdout.splitlines(), [str(self.engine), arg])
                self.assertFalse((self.engine / 'INJECTED').exists())
                self.assertNotIn('Program', doc)
                self.assertEqual(source['Program'], '/old/runner')

    def test_preserves_service_settings_and_channel_paths(self):
        doc = self.render()
        for key in ('StartInterval', 'RunAtLoad', 'StandardOutPath', 'Nice'):
            self.assertEqual(doc[key], self.source[key])
        for key, value in {**self.source['EnvironmentVariables'], **self.channels}.items():
            self.assertEqual(doc['EnvironmentVariables'][key], value)

    def test_rejects_unrelated_service(self):
        with self.assertRaises(ValueError):
            self.render(dict(self.source, Label='unrelated'))

    def test_rejects_relative_paths(self):
        with self.assertRaises(ValueError):
            renderer.render(self.source, 'relative', sys.executable, self.channels)
        with self.assertRaises(ValueError):
            renderer.render(self.source, self.engine, sys.executable, {'OWB_REPO': 'relative'})

    def test_rejects_missing_engine(self):
        with self.assertRaises(ValueError):
            renderer.render(self.source, self.root / 'missing', sys.executable, self.channels)

    def test_cli_writes_private_file_and_refuses_overwrite(self):
        source = self.root / 'installed.plist'
        source.write_bytes(plistlib.dumps(self.source))
        out = self.root / 'proposed.plist'
        args = [sys.executable, str(TOOL), '--source', str(source), '--engine', str(self.engine),
                '--python', sys.executable, '--out', str(out)]
        for name, key in [('owb', 'OWB_REPO'), ('hos', 'HOS_REPO'), ('ww2', 'WW2_REPO')]:
            args += ['--' + name, self.channels[key]]
        subprocess.run(args, check=True, capture_output=True)
        self.assertEqual(out.stat().st_mode & 0o777, 0o600)
        before = out.read_bytes()
        again = subprocess.run(args, capture_output=True)
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual(out.read_bytes(), before)
        self.assertEqual(plistlib.loads(source.read_bytes()), self.source)


if __name__ == '__main__':
    unittest.main()
