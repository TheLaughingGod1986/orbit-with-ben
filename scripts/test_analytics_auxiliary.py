"""Offline gate/dispatch integration; no production queue or remote calls."""
from contextlib import ExitStack
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import analytics_auxiliary as module
from analytics_worktree import RecordError


class Auxiliary(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.session = Mock()
        self.session.records = {s: Mock(worktree=self.root / 'records' / s)
                                for s in ('studio', 'space', 'science')}
        self.session.sources = {s: self.root / 'sources' / s for s in self.session.records}
        self.credentials = self.root / 'credentials'
        self.cache = self.root / 'cache'
        self.env = {'FIELD_ORDER_QUEUE_REPO': str(self.root / 'shared-queue')}
        self.commands = []
        self.stack.enter_context(patch.object(module.channels, 'get',
            side_effect=lambda s: {'analytics': {'open_gate_library': s == 'space'}}))
        self.data = self.session.records['space'].worktree / '05_Analytics/space'
        snapshot = self.data / 'snapshots/2026-11-20.json'
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text('{"videos": []}')
        uploads = self.session.records['space'].worktree / '00_Brand/Channel-Setup/social/UPLOADS.json'
        uploads.parent.mkdir(parents=True)
        uploads.write_text('{"videos": {}}')

    def run_fake(self, command):
        self.commands.append(command)
        return 0

    def phase(self, runner=None):
        return module.auxiliary(self.credentials, self.cache, 'field-order-dispatch.ts',
                                runner or self.run_fake, day='2026-11-20')

    def test_records_media_credentials_cache_and_queue_are_separate(self):
        self.assertEqual(self.phase()(self.session, self.env), [])
        self.assertEqual([c.name for c in self.commands], ['dispatch', 'gate:space'])
        dispatch, gate = self.commands
        self.assertIn(f'--env-file={self.credentials}', dispatch.args)
        self.assertEqual(dispatch.env['FIELD_ORDER_QUEUE_REPO'], str(self.root / 'shared-queue'))
        for flag, expected in (('--record', self.session.records['space'].worktree),
                               ('--media-root', self.session.sources['space']),
                               ('--cache', self.cache), ('--out', self.data / 'UPCOMING_SHORTS_GATE.md')):
            self.assertEqual(gate.args[gate.args.index(flag) + 1], str(expected))
        self.assertEqual((dispatch.timeout, gate.timeout), (180, 600))
        self.assertNotIn('--stage', gate.args)

    def test_dispatch_failure_does_not_suppress_gate_and_gate_timeout_is_reported(self):
        def fail(command):
            self.commands.append(command)
            return 124
        self.assertEqual(self.phase(fail)(self.session, self.env), ['dispatch', 'gate:space'])
        self.assertEqual(len(self.commands), 2)

    def test_missing_today_does_not_substitute_yesterday(self):
        (self.data / 'snapshots/2026-11-20.json').rename(self.data / 'snapshots/2026-11-19.json')
        self.assertEqual(self.phase()(self.session, self.env), ['gate-input:space'])
        self.assertEqual([c.name for c in self.commands], ['dispatch'])

    def test_bad_paths_script_and_limits_fail_before_work(self):
        for args in ((Path('relative'), self.cache, 'dispatch.ts', 600),
                     (self.credentials, Path('relative'), 'dispatch.ts', 600),
                     (self.credentials, self.cache, '../other.ts', 600),
                     (self.credentials, self.cache, 'dispatch.ts', 0)):
            with self.assertRaises(RecordError):
                module.auxiliary(*args[:3], gate_timeout=args[3])
        self.assertEqual(self.commands, [])

    def test_real_adapter_empty_report_in_bounded_subprocess(self):
        # Exercise the actual command, not a mocked gate, with a channel-specific
        # profile. The engine code lives here; record destinations stay temporary.
        import json
        engine = Path(__file__).resolve().parent.parent
        source = self.session.sources['space']
        record = self.session.records['space'].worktree
        for root in (source, record):
            (root / 'studio').mkdir(parents=True, exist_ok=True)
            (root / 'studio/channel.json').write_text(json.dumps({'slug': 'space', 'analytics': {'open_gate_library': True}}))
        profile = source / '00_Brand/Channel-Setup/tools/channel_profile.py'
        profile.parent.mkdir(parents=True)
        profile.write_text("NAME='Fixture'\nSLUG='fixture'\nROBOT_FRAME0_CHECK=False\n")
        self.session.records['studio'].worktree = engine
        def execute(command):
            if command.name == 'dispatch':
                return 0
            import os
            command.env.update(os.environ)
            return module.execute(command)
        self.assertEqual(self.phase(execute)(self.session, self.env), [])
        self.assertIn('No scheduled Shorts', (self.data / 'UPCOMING_SHORTS_GATE.md').read_text())
        self.assertFalse((source / '05_Analytics').exists())


if __name__ == '__main__':
    unittest.main()
