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
        import jobs, studio, chief_relay, board_publish, macbook_worker, ai_spend, ai_spend_daily, thumb_ledger, launch_check
        for module in (jobs, studio, chief_relay, board_publish, macbook_worker, ai_spend, ai_spend_daily, thumb_ledger, launch_check):
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

    def test_retired_thumbnail_writer_preserves_existing_ledger(self):
        import thumb_ledger
        target = self.root / 'thumb.json'
        target.write_text('{"tests": []}\n')
        original = target.read_bytes()
        with patch.object(engine_guard, 'refusal', return_value='retired'):
            with self.assertRaisesRegex(SystemExit, 'retired'):
                thumb_ledger.save({'tests': [{'id': 'changed'}]}, target)
        self.assertEqual(target.read_bytes(), original)

    def test_retired_launch_writer_never_resolves_or_creates_record(self):
        import launch_check
        with patch.object(engine_guard, 'refusal', return_value='retired'), \
                patch.object(launch_check, 'record_path') as path:
            with self.assertRaisesRegex(SystemExit, 'retired'):
                launch_check.save_record('fixture', {'id': 'example'})
            path.assert_not_called()

    def test_unarmed_imported_writers_keep_existing_behavior(self):
        import thumb_ledger, launch_check
        target = self.root / 'thumb.json'
        record = self.root / 'new' / 'launch.json'
        with patch.object(engine_guard, 'refusal', return_value=None), \
                patch.object(launch_check, 'record_path', return_value=record):
            thumb_ledger.save({'tests': []}, target)
            self.assertEqual(launch_check.save_record('fixture', {'id': 'example'}), record)
        self.assertEqual(json.loads(target.read_text()), {'tests': []})
        self.assertEqual(json.loads(record.read_text()), {'id': 'example'})


if __name__ == '__main__':
    unittest.main()
