"""Cutover refusal runs before a stale engine can launch or commit work."""
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import engine_guard


class EngineGuard(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = pathlib.Path(tmp.name)
        self.marker = self.root / 'active.json'
        (self.root / 'channels').mkdir()
        self.registry = self.root / 'channels/channels.json'
        self.registry.write_text(json.dumps({'studio': {'github': 'test/old-engine'}}))

    def arm(self, repo='test/new-engine'):
        self.marker.write_text(json.dumps({'version': 1, 'github': repo}))

    def test_unarmed_layout_is_unchanged(self):
        self.assertIsNone(engine_guard.refusal(self.root, self.marker))

    def test_retired_repo_refused_even_with_new_checkout_environment(self):
        self.arm()
        with patch.dict('os.environ', {'STUDIO_REPO': '/new/studio'}):
            self.assertIsNotNone(engine_guard.refusal(self.root, self.marker))
        self.arm('test/old-engine')
        self.assertIsNone(engine_guard.refusal(self.root, self.marker))

    def test_malformed_marker_or_registry_fails_closed_without_echoing_contents(self):
        for value in ('not-json', '{}', '[]', '{"version":2,"github":"test/old-engine"}'):
            self.marker.write_text(value)
            self.assertIsNotNone(engine_guard.refusal(self.root, self.marker))
        self.arm()
        self.registry.write_text('private-content-not-to-print')
        why = engine_guard.refusal(self.root, self.marker)
        self.assertNotIn('private-content', why)
        self.registry.unlink()
        self.assertIsNotNone(engine_guard.refusal(self.root, self.marker))

    def test_cli_entrypoints_refuse_before_parsing_or_service_work(self):
        import jobs, studio, chief_relay, board_publish, macbook_worker, ai_spend, ai_spend_daily
        for module in (jobs, studio, chief_relay, board_publish, macbook_worker, ai_spend, ai_spend_daily):
            with self.subTest(module=module.__name__), \
                    patch.object(engine_guard, 'refusal', return_value='retired'):
                with self.assertRaisesRegex(SystemExit, 'retired'):
                    module.main(['--help'])

    def test_metadata_callback_and_git_never_run_in_retired_engine(self):
        import studio
        with patch.object(engine_guard, 'refusal', return_value='retired'), \
                patch.object(studio, 'git') as git:
            callback = unittest.mock.Mock()
            with self.assertRaisesRegex(SystemExit, 'retired'):
                studio.git_transaction(callback, 'must not commit')
            git.assert_not_called()
            callback.assert_not_called()

    def test_direct_ledger_writer_refuses_before_creating_files_or_running_git(self):
        import ai_spend
        target = self.root / 'absent' / 'ledger.jsonl'
        with patch.object(engine_guard, 'refusal', return_value='retired'), \
                patch.object(ai_spend, 'LEDGER', target), \
                patch.object(ai_spend.subprocess, 'run') as run:
            with self.assertRaisesRegex(SystemExit, 'retired'):
                ai_spend.append({'kind': 'record'}, True)
            self.assertFalse(target.parent.exists())
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
