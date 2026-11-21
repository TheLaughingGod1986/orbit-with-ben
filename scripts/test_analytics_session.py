"""Offline preflight, serialization and routing tests for detached analytics."""
from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import analytics_session as module
from analytics_worktree import RecordError

VERIFY_SOURCE = module.verify_source


class Sessions(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.engine = self.root / 'engine'
        self.engine.mkdir()
        (self.engine / 'jobs').mkdir()
        (self.engine / 'jobs/queue.json').write_text('{"jobs": []}')
        (self.engine / 'channels').mkdir()
        (self.engine / 'channels/channels.json').write_text(json.dumps({'studio': {'github': 'owner/studio'}}))
        self.sources = {}
        for slug in ('owb', 'hos', 'ww2'):
            source = self.root / slug
            (source / 'studio').mkdir(parents=True)
            (source / 'studio/channel.json').write_text(json.dumps({'slug': slug}))
            history = source / '05_Analytics' / slug / 'snapshots'
            history.mkdir(parents=True)
            (history / 'before.json').write_text('{}')
            self.sources[slug] = source
        self.stack.enter_context(patch.object(module, 'refusal', return_value=None))
        self.stack.enter_context(patch.object(module.channels, 'ROOT', self.engine))
        self.stack.enter_context(patch.object(module.channels, 'studio_slug', return_value=None))
        self.stack.enter_context(patch.object(module.channels, 'studio_checkout', return_value=self.engine))
        self.stack.enter_context(patch.object(module.channels, 'studio_github', return_value='owner/studio'))
        self.stack.enter_context(patch.object(module.channels, 'studio_repo', return_value={'url': 'https://github.com/owner/studio.git', 'env': 'STUDIO_REPO'}))
        self.stack.enter_context(patch.object(module.channels, 'slugs', return_value=list(self.sources)))
        self.stack.enter_context(patch.object(module.channels, 'checkout', side_effect=self.sources.get))
        self.stack.enter_context(patch.object(module.channels, 'get', side_effect=lambda s: {'repo': {'url': f'https://github.com/owner/{s}.git', 'env': f'{s.upper()}_REPO'}}))
        self.verify = self.stack.enter_context(patch.object(module, 'verify_source'))
        self.session = module.Session(self.root / 'scratch')

    def test_preflight_binds_records_but_keeps_queue_in_engine(self):
        self.session.preflight()
        self.assertEqual(set(self.session.records), {'studio', *self.sources})
        env = self.session.environment({'CREDENTIAL_FILE': '/local/credential-file'})
        self.assertEqual(env['CREDENTIAL_FILE'], '/local/credential-file')
        self.assertEqual(env['FIELD_ORDER_QUEUE_REPO'], str(self.engine))
        self.assertEqual(env['HOS_REPO'], str(self.root / 'scratch/hos'))
        self.assertEqual(self.session.sources['hos'], self.sources['hos'])
        self.assertFalse((self.root / 'scratch').exists())
        self.assertEqual(self.verify.call_count, 5)

    def test_missing_history_refuses_before_worktree_operations(self):
        (self.sources['hos'] / '05_Analytics/hos/snapshots/before.json').unlink()
        with patch.object(module.Records, 'prepare') as prepare:
            with self.assertRaisesRegex(RecordError, 'Stage existing'):
                self.session.prepare()
            prepare.assert_not_called()

    def test_wrong_manifest_refuses(self):
        (self.sources['hos'] / 'studio/channel.json').write_text('{"slug":"owb"}')
        with self.assertRaisesRegex(RecordError, 'identity mismatch'):
            self.session.preflight()

    def test_resident_and_retired_engine_refuse(self):
        with patch.object(module.channels, 'studio_slug', return_value='owb'):
            with self.assertRaises(RecordError):
                self.session.preflight()
        with patch.object(module, 'refusal', return_value='retired'):
            with self.assertRaises(RecordError):
                self.session.preflight()
        self.verify.assert_not_called()

    def test_shared_queue_registry_must_match(self):
        (self.engine / 'channels/channels.json').write_text('{"studio":{"github":"owner/retired"}}')
        with self.assertRaisesRegex(RecordError, 'queue engine identity'):
            self.session.preflight()

    def test_scratch_cannot_be_inside_source(self):
        with self.assertRaisesRegex(RecordError, 'scratch must be outside'):
            module.Session(self.sources['owb'] / 'scratch').preflight()

    def test_environment_aliases_refused(self):
        with patch.object(module.channels, 'get', return_value={'repo': {'url': 'https://github.com/owner/owb.git', 'env': 'STUDIO_REPO'}}):
            with self.assertRaisesRegex(RecordError, 'unique checkout'):
                self.session.preflight()

    def test_actual_detached_history_checked_after_prepare(self):
        with patch.object(module.Records, 'prepare'):
            with self.assertRaisesRegex(RecordError, 'manifest unavailable'):
                self.session.prepare()

    def test_lock_covers_prepare_body_and_publish_and_releases_on_error(self):
        lock = self.root / 'locks/test.lock'
        with patch.object(module.Session, 'prepare') as prepare:
            with module.locked_session(self.root / 'first', lock):
                with self.assertRaisesRegex(RecordError, 'already running'):
                    with module.locked_session(self.root / 'second', lock):
                        self.fail('second writer entered')
            self.assertEqual(prepare.call_count, 1)
            with self.assertRaisesRegex(RuntimeError, 'body failed'):
                with module.locked_session(self.root / 'second', lock):
                    raise RuntimeError('body failed')
            with module.locked_session(self.root / 'third', lock):
                pass
            self.assertEqual(prepare.call_count, 3)

    def test_publish_attempts_other_repositories_after_one_failure(self):
        self.session.records = {'studio': Mock(), 'owb': Mock(), 'hos': Mock()}
        self.session.records['owb'].publish.side_effect = RecordError('push failed')
        self.assertEqual(self.session.publish('daily'), ['owb'])
        for record in self.session.records.values():
            record.publish.assert_called_once_with('daily')

    def test_registry_controls_record_ownership_without_channel_name_rules(self):
        from analytics_worktree import scopes
        with patch.object(module.channels, 'slugs', return_value=['science', 'space']), \
             patch.object(module.channels, 'get', side_effect=lambda s: {'analytics': {'open_gate_library': s == 'space'}}):
            self.assertEqual(scopes('science'), ('05_Analytics/science',))
            self.assertEqual(scopes('space'), ('05_Analytics/space',
                '00_Brand/Channel-Setup/audits/shorts_open_library/library.json'))
            with self.assertRaises(RecordError):
                scopes('unregistered')

    def test_repository_identity_is_exact_and_never_echoes_invalid_url(self):
        self.assertEqual(module.repository_id('git@github.com:Owner/studio.git'), 'owner/studio')
        self.assertEqual(module.repository_id('https://github.com/Owner/studio'), 'owner/studio')
        for bad in ('https://other.example/owner/studio', 'https://private-value' + chr(64) + 'github.com/owner/studio', '/tmp/local'):
            with self.assertRaises(RecordError) as raised:
                module.repository_id(bad)
            self.assertNotIn(bad, str(raised.exception))
        def git(repo, *args):
            return Mock(stdout=str(repo) if args[0] == 'rev-parse' else 'https://github.com/owner/wrong.git')
        with patch.object(module.Records, 'git', side_effect=git):
            with self.assertRaisesRegex(RecordError, 'does not match registry'):
                VERIFY_SOURCE(self.engine, 'https://github.com/owner/studio.git')


if __name__ == '__main__':
    unittest.main()
