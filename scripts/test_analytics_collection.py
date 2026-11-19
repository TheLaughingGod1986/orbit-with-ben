"""Offline collection flow: fake collectors, real timeout process groups."""
from contextlib import ExitStack, contextmanager
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

import analytics_collection as module
from analytics_worktree import RecordError


class Collection(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.session = Mock()
        self.session.sources = {s: self.root / 'sources' / s for s in ('studio', 'space', 'science')}
        self.session.records = {s: Mock(worktree=self.root / 'records' / s) for s in self.session.sources}
        for record in self.session.records.values():
            (record.worktree / '07_Content-Ops').mkdir(parents=True)
        runner = self.session.sources['studio'] / '07_Content-Ops/node_modules/tsx/dist/cli.mjs'
        runner.parent.mkdir(parents=True)
        runner.write_text('// fixture')
        self.credentials = self.root / 'credentials'
        self.credentials.write_text('')
        self.session.environment.return_value = {'SPACE_REPO': str(self.session.records['space'].worktree),
            'SCIENCE_REPO': str(self.session.records['science'].worktree),
            'FIELD_ORDER_QUEUE_REPO': str(self.session.sources['studio']),
            'GOOGLE_CLIENT_SECRET': 'stale', 'YT_ANALYTICS_REFRESH_TOKEN_SPACE': 'stale',
            'YT_CHANNEL_ID_SPACE': 'stale', 'PATH': os.environ['PATH']}
        self.session.publish.return_value = []
        self.commands = []
        self.stack.enter_context(patch.object(module.channels, 'studio_repo', return_value={'env': 'STUDIO_REPO'}))
        self.stack.enter_context(patch.object(module.channels, 'get', side_effect=lambda s: {'repo': {'env': s.upper() + '_REPO'}}))

    def run_fake(self, command):
        self.commands.append(command)
        return 0

    def test_full_sequence_and_distinct_data_queue_publisher_environments(self):
        def auxiliary(session, env):
            self.assertEqual(len(self.commands), 2)
            self.assertIs(session, self.session)
            self.assertEqual(env['FIELD_ORDER_QUEUE_REPO'], str(self.session.sources['studio']))
            return []
        self.assertEqual(module.collect(self.session, self.credentials, auxiliary, self.run_fake), [])
        self.assertEqual([c.name for c in self.commands], ['snapshot:space', 'snapshot:science', 'report', 'board'])
        for c in self.commands[:-1]:
            self.assertEqual(c.cwd, self.session.records['studio'].worktree / '07_Content-Ops')
            self.assertEqual(c.env['SPACE_REPO'], str(self.session.records['space'].worktree))
            self.assertNotIn('GOOGLE_CLIENT_SECRET', c.env)
            self.assertNotIn('YT_CHANNEL_ID_SPACE', c.env)
            self.assertNotIn('YT_ANALYTICS_REFRESH_TOKEN_SPACE', c.env)
            self.assertIn(f'--env-file={self.credentials}', c.args)
        self.assertEqual(self.commands[-1].env['SPACE_REPO'], str(self.session.sources['space']))
        self.session.publish.assert_called_once()

    def test_collector_gate_report_and_push_failures_do_not_suppress_other_owners(self):
        self.session.publish.return_value = ['science']
        def fail(command):
            self.commands.append(command)
            return 124 if command.name in ('snapshot:space', 'report', 'board') else 0
        result = module.collect(self.session, self.credentials, lambda *_: ['gate:space'], fail)
        self.assertEqual(result, ['snapshot:space', 'gate:space', 'report', 'publish:science', 'board'])
        self.assertIn('snapshot:science', [c.name for c in self.commands])

    def test_retry_publication_runs_even_without_new_collector_changes(self):
        module.collect(self.session, self.credentials, lambda *_: [], self.run_fake, board=False)
        module.collect(self.session, self.credentials, lambda *_: [], self.run_fake, board=False)
        self.assertEqual(self.session.publish.call_count, 2)
        self.assertNotIn('board', [c.name for c in self.commands])

    def test_invalid_credential_or_missing_gate_phase_refuses_before_commands(self):
        for credential in (Path('relative'), self.root / 'absent'):
            with self.assertRaises(RecordError):
                module.collect(self.session, credential, lambda *_: [], self.run_fake)
        with self.assertRaises(RecordError):
            module.collect(self.session, self.credentials, None, self.run_fake)
        credential = self.session.records['space'].worktree / '.env'
        credential.write_text('')
        with self.assertRaises(RecordError):
            module.collect(self.session, credential, lambda *_: [], self.run_fake)
        self.assertEqual(self.commands, [])
        self.session.publish.assert_not_called()

    def test_dependency_directory_is_never_overwritten(self):
        (self.session.records['studio'].worktree / '07_Content-Ops/node_modules').mkdir()
        with self.assertRaisesRegex(RecordError, 'unexpected dependency'):
            module.collect(self.session, self.credentials, lambda *_: [], self.run_fake)
        self.assertEqual(self.commands, [])

    def test_lock_wraps_all_work_and_releases_on_exception(self):
        state = []
        @contextmanager
        def locked(*_):
            state.append('locked')
            try:
                yield self.session
            finally:
                state.append('unlocked')
        def collect(*args, **kwargs):
            self.assertEqual(state, ['locked'])
            raise RecordError('auxiliary failed')
        with patch.object(module, 'locked_session', locked), patch.object(module, 'collect', collect):
            with self.assertRaises(RecordError):
                module.collection_session(self.root, self.credentials, lambda *_: [])
        self.assertEqual(state, ['locked', 'unlocked'])

    def test_fake_executable_writes_only_selected_record_destinations(self):
        fakebin = self.root / 'bin'
        fakebin.mkdir()
        fake = fakebin / 'node'
        fake.write_text('#!' + sys.executable + '\n' + """import os,pathlib,sys
args = sys.argv[1:]
if '--channel' in args:
    slug = args[args.index('--channel') + 1]
    root = pathlib.Path(os.environ[slug.upper() + '_REPO'])
    target = root / '05_Analytics' / slug / 'snapshots' / 'fake.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('{}')
else:
    root = pathlib.Path.cwd().parent
    target = root / '05_Analytics/dashboard/data.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('{}')
""")
        fake.chmod(0o755)
        self.session.environment.return_value['PATH'] = str(fakebin) + os.pathsep + os.environ['PATH']
        result = module.collect(self.session, self.credentials, lambda *_: [], board=False)
        self.assertEqual(result, [])
        for slug in ('space', 'science'):
            self.assertTrue((self.session.records[slug].worktree / '05_Analytics' / slug / 'snapshots/fake.json').is_file())
            self.assertFalse((self.session.sources[slug] / '05_Analytics').exists())
        engine = self.session.records['studio'].worktree
        self.assertTrue((engine / '05_Analytics/dashboard/data.json').is_file())
        self.assertFalse((engine / '05_Analytics/space').exists())
        self.assertFalse((engine / '05_Analytics/science').exists())

    def test_timeout_kills_child_group_not_only_parent(self):
        # A surviving child would create this file after its parent was killed.
        marker = self.root / 'orphan'
        child = 'import time,pathlib; time.sleep(1); pathlib.Path(' + repr(str(marker)) + ').write_text("alive")'
        parent = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",' + repr(child) + ']); time.sleep(30)'
        command = module.Command('timeout', (sys.executable, '-c', parent), self.root, dict(os.environ), 0.2)
        self.assertEqual(module.execute(command), 124)
        time.sleep(1.1)
        self.assertFalse(marker.exists())

    def test_runner_preserves_exit_code_and_handles_missing_executable(self):
        command = module.Command('exit', (sys.executable, '-c', 'raise SystemExit(7)'), self.root, dict(os.environ), 5)
        self.assertEqual(module.execute(command), 7)
        command = module.Command('missing', (str(self.root / 'missing'),), self.root, dict(os.environ), 5)
        self.assertEqual(module.execute(command), 127)


if __name__ == '__main__':
    unittest.main()
