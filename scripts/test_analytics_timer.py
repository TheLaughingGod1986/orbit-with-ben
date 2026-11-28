"""Timer wiring and fallback probes, without live APIs or service changes."""
import argparse
from contextlib import ExitStack
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import analytics_timer as module
from analytics_worktree import RecordError


class Timer(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.args = argparse.Namespace(records=self.root / 'records', credentials=self.root / 'local.env',
            cache=self.root / 'cache', safe_cache=self.root / 'safe', gate_timeout=123, no_board=True)
        self.stack.enter_context(patch.object(module, 'refusal', return_value=None))
        self.stack.enter_context(patch.object(module.channels, 'studio_slug', return_value=None))

    def test_real_cache_probe_and_fallback_leave_no_probe_files(self):
        blocked = self.root / 'blocked'
        blocked.write_text('file')
        selected = module.pick_cache(blocked / 'cache', self.args.safe_cache)
        self.assertEqual(selected, self.args.safe_cache)
        self.assertEqual(list(selected.iterdir()), [])
        self.assertEqual(module.pick_cache(self.args.cache, selected), self.args.cache)

    def test_timed_out_cache_uses_fallback_and_both_fail_closed(self):
        run = Mock(side_effect=[124, 0])
        self.assertEqual(module.pick_cache(self.args.cache, self.args.safe_cache, run), self.args.safe_cache)
        self.assertEqual([c.args[0].timeout for c in run.call_args_list], [5, 5])
        with self.assertRaises(RecordError):
            module.pick_cache(self.args.cache, self.args.safe_cache, Mock(return_value=124))
        with self.assertRaises(RecordError):
            module.pick_cache(Path('relative'), self.args.safe_cache)

    def test_worker_connects_required_auxiliary_and_serialized_collection(self):
        callback = object()
        with patch.object(module, 'auxiliary', return_value=callback) as auxiliary, \
                patch.object(module, 'collection_session', return_value=[]) as collect:
            self.assertEqual(module.worker(self.args), 0)
            auxiliary.assert_called_once_with(self.args.credentials, self.args.cache,
                'field-order-dispatch.ts', gate_timeout=123)
            collect.assert_called_once_with(self.args.records, self.args.credentials, callback, board=False)
            collect.return_value = ['publish:science']
            self.assertEqual(module.worker(self.args), 1)

    def test_retired_and_resident_engine_never_probe_or_collect(self):
        with patch.object(module, 'pick_cache') as probe, patch.object(module, 'collection_session') as collect:
            for name, value in [('refusal', 'retired')]:
                with patch.object(module, name, return_value=value):
                    with self.assertRaises(RecordError):
                        module.worker(self.args)
            with patch.object(module.channels, 'studio_slug', return_value='space'):
                with self.assertRaises(RecordError):
                    module.worker(self.args)
            probe.assert_not_called()
            collect.assert_not_called()

    def test_supervisor_bounds_whole_worker_and_preserves_status(self):
        argv = ['--records', str(self.args.records), '--credentials', str(self.args.credentials),
                '--cache', str(self.args.cache), '--safe-cache', str(self.args.safe_cache)]
        with patch.object(module, 'execute', return_value=124) as execute:
            self.assertEqual(module.main(argv), 124)
            command = execute.call_args.args[0]
            self.assertEqual(command.timeout, 2700)
            self.assertEqual(command.args[-1], '--worker')
        with patch.object(module, 'worker', side_effect=RuntimeError('sensitive diagnostic')):
            self.assertEqual(module.main([*argv, '--worker']), 1)

    def test_shell_passes_paths_literally_and_missing_credentials_refuse(self):
        source = Path(__file__).resolve().parents[1] / '07_Content-Ops/launchd/analytics-detached.sh'
        engine = self.root / 'engine space'
        target = engine / '07_Content-Ops/launchd/analytics-detached.sh'
        target.parent.mkdir(parents=True)
        shutil.copy2(source, target)
        (engine / 'scripts').mkdir()
        (engine / 'scripts/analytics_timer.py').write_text(
            'import json,sys\nprint(json.dumps(sys.argv[1:]))\nraise SystemExit(7)\n')
        env = dict(os.environ)
        env.pop('ANALYTICS_CREDENTIAL_FILE', None)
        r = subprocess.run(['bash', str(target)], env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        env.update(ANALYTICS_CREDENTIAL_FILE=str(self.root / '$(touch INJECTED).env'),
                   STUDIO_PYTHON=sys.executable, ANALYTICS_SAFE_DIR=str(self.root / 'internal space'),
                   BOARD_PUBLISH='0')
        r = subprocess.run(['bash', str(target)], env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 7, r.stderr)
        import json
        args = json.loads(r.stdout)
        self.assertEqual(args[args.index('--credentials') + 1], env['ANALYTICS_CREDENTIAL_FILE'])
        self.assertEqual(args[args.index('--records') + 1], str(self.root / 'internal space/records'))
        self.assertIn('--no-board', args)
        self.assertFalse((engine / 'INJECTED').exists())


if __name__ == '__main__':
    unittest.main()
