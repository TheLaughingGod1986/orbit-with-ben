import argparse
import contextlib
import copy
import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('reschedule', Path(__file__).parents[1] / 'scripts/codex_buffer_reschedule.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / 'social'
        self.folder.mkdir()
        self.video = 'abcdefghijk'
        self.post_id = 'a' * 24
        self.due = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).isoformat()
        self.old = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)).isoformat()
        self.entry = {'kind': 'short', 'mode': 'customScheduled', 'dueAt': self.old,
                      'channels': {'instagram': {'postId': self.post_id}}}
        self.save()
        self.args = argparse.Namespace(channel='owb', video=self.video, apply=False)
        self.status = {'privacyStatus': 'private', 'publishAt': self.due}
        self.reader = SimpleNamespace(ROOT=self.root, SOCIAL=Path('social'), execute=lambda *_: {'items': [{'status': self.status}]})
        self.cfg = {'BUFFER_API_KEY': 'fake-only'}
        self.post = {'id': self.post_id, 'channelId': s.CHANNELS['owb']['instagram'], 'status': 'scheduled', 'dueAt': self.old}

    def save(self):
        (self.folder / 'BUFFER_POSTS.json').write_text(json.dumps({'videos': {self.video: self.entry}}))
        (self.folder / 'UPLOADS.json').write_text(json.dumps({'videos': {self.video: {'kind': 'short'}}}))

    def call(self, key, query, payload):
        if query == s.GET:
            return {'post': copy.deepcopy(self.post)}
        self.post['dueAt'] = payload['dueAt']
        return {'editPost': {'__typename': 'PostActionSuccess', 'post': copy.deepcopy(self.post)}}

    def test_default_plan_does_not_mutate_or_write(self):
        before = (self.folder / 'BUFFER_POSTS.json').read_bytes()
        with patch.object(s, 'buffer_call', side_effect=self.call) as call:
            result = s.run(self.args, self.reader, self.cfg)
        self.assertTrue(result['posts'][0]['change'])
        self.assertEqual([c.args[1] for c in call.call_args_list], [s.GET])
        self.assertEqual((self.folder / 'BUFFER_POSTS.json').read_bytes(), before)

    def test_apply_pins_only_id_mode_due_and_records(self):
        self.args.apply = True
        with patch.object(s, 'buffer_call', side_effect=self.call) as call:
            s.run(self.args, self.reader, self.cfg)
        edits = [c.args[2] for c in call.call_args_list if c.args[1] == s.EDIT]
        self.assertEqual(edits, [{'id': self.post_id, 'mode': 'customScheduled', 'dueAt': self.due}])
        entry = json.loads((self.folder / 'BUFFER_POSTS.json').read_text())['videos'][self.video]
        self.assertEqual(entry['dueAt'], self.due)
        self.assertEqual(entry['channels']['instagram']['dueAt'], self.due)

    def test_matching_schedule_is_idempotent(self):
        self.post['dueAt'] = self.due
        self.args.apply = True
        with patch.object(s, 'buffer_call', side_effect=self.call) as call:
            s.run(self.args, self.reader, self.cfg)
        self.assertEqual([c.args[1] for c in call.call_args_list], [s.GET])

    def test_wrong_channel_status_or_id_never_edits(self):
        for field, value in [('channelId', s.CHANNELS['hos']['instagram']), ('status', 'sent'), ('status', 'draft'), ('id', 'b' * 24)]:
            post = {**self.post, field: value}
            with self.subTest(field=field, value=value), patch.object(s, 'buffer_call', return_value={'post': post}) as call:
                self.args.apply = True
                with self.assertRaises(ValueError):
                    s.run(self.args, self.reader, self.cfg)
                self.assertTrue(all(c.args[1] == s.GET for c in call.call_args_list))

    def test_unscheduled_public_imminent_and_distant_youtube_refused(self):
        for status in [{'privacyStatus': 'public', 'publishAt': self.due}, {'privacyStatus': 'private'},
                       {'privacyStatus': 'private', 'publishAt': '2020-01-01T00:00:00Z'},
                       {'privacyStatus': 'private', 'publishAt': '9999-01-01T00:00:00Z'}]:
            self.status = status
            with patch.object(s, 'buffer_call') as call, self.assertRaises((ValueError, KeyError)):
                s.run(self.args, self.reader, self.cfg)
            call.assert_not_called()

    def test_recheck_blocks_changed_youtube_before_edit(self):
        self.args.apply = True
        count = 0
        def read(*_):
            nonlocal count
            count += 1
            return {'items': [{'status': self.status if count == 1 else {'privacyStatus': 'public'}}]}
        self.reader.execute = read
        with patch.object(s, 'buffer_call', side_effect=self.call) as call, self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)
        self.assertTrue(all(c.args[1] == s.GET for c in call.call_args_list))

    def test_all_post_ownership_checked_before_first_edit(self):
        self.entry['channels']['tiktok'] = {'postId': 'b' * 24}
        self.save()
        self.args.apply = True
        with patch.object(s, 'buffer_call', side_effect=self.call) as call, self.assertRaises(KeyError):
            s.run(self.args, self.reader, self.cfg)
        self.assertTrue(all(c.args[1] == s.GET for c in call.call_args_list))

    def test_lock_fails_closed_and_releases_own_lock(self):
        lock = self.root / 'locks/test.lock'
        with patch.object(s, 'LOCK', lock):
            with s.desk_lock():
                self.assertTrue((lock / 'owner.txt').exists())
                with self.assertRaises(FileExistsError):
                    with s.desk_lock():
                        self.fail('must not enter')
            self.assertFalse(lock.exists())

    def test_transport_refuses_unapproved_graphql_and_payload_before_network(self):
        cases = [('mutation deletePost', {}), (s.EDIT, {'id': self.post_id, 'mode': 'shareNow', 'dueAt': self.due}),
                 (s.EDIT, {'id': self.post_id, 'mode': 'customScheduled', 'dueAt': self.due, 'text': 'injected'}),
                 (s.GET, {'id': '../wrong'})]
        with patch.object(s.http.client, 'HTTPSConnection') as conn:
            for query, payload in cases:
                with self.subTest(query=query), self.assertRaises(ValueError):
                    s.buffer_call('fake', query, payload)
        conn.assert_not_called()

    def test_cli_refuses_arbitrary_inputs(self):
        for extra in (['--url', 'https://example.com'], ['--post-id', self.post_id], ['--due-at', self.due],
                      ['--body', '{}'], ['--delete'], ['--app']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                s.main(['--channel', 'owb', '--video', self.video, *extra])

    def test_partial_failure_retains_confirmed_receipt(self):
        self.entry['channels']['facebook'] = {'postId': 'b' * 24}
        self.save()
        self.args.apply = True
        def call(key, query, payload):
            if payload['id'] == self.post_id:
                return self.call(key, query, payload)
            other = {**self.post, 'id': 'b' * 24, 'channelId': s.CHANNELS['owb']['facebook'], 'dueAt': self.old}
            if query == s.EDIT:
                return {'editPost': {'__typename': 'MutationError'}}
            return {'post': other}
        with patch.object(s, 'buffer_call', side_effect=call), self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)
        entry = json.loads((self.folder / 'BUFFER_POSTS.json').read_text())['videos'][self.video]
        self.assertEqual(entry['dueAt'], self.old)
        self.assertEqual(entry['channels']['instagram']['dueAt'], self.due)
        self.assertNotIn('dueAt', entry['channels']['facebook'])

    def test_hos_long_refused_before_network(self):
        hos = self.folder / 'hos'
        hos.mkdir()
        (hos / 'BUFFER_POSTS.json').write_text(json.dumps({'videos': {self.video: {**self.entry, 'kind': 'long'}}}))
        (hos / 'UPLOADS.json').write_text(json.dumps({'videos': {self.video: {'kind': 'long'}}}))
        self.args.channel = 'hos'
        with patch.object(s, 'buffer_call') as call, self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)
        call.assert_not_called()

    def test_transport_redirect_not_followed_or_body_printed(self):
        with patch.object(s.http.client, 'HTTPSConnection') as conn:
            conn.return_value.getresponse.return_value.status = 302
            with self.assertRaises(ValueError):
                s.buffer_call('fake', s.GET, {'id': self.post_id})
            conn.assert_called_once_with('api.buffer.com', timeout=30)
            conn.return_value.getresponse.return_value.read.assert_not_called()
            conn.return_value.close.assert_called_once()

    def test_naive_and_missing_dates_refused(self):
        for value in (None, '', '2026-11-07T12:00:00'):
            with self.assertRaises(ValueError):
                s.instant(value)

    def test_dependency_hash_change_refused_before_import(self):
        with patch.object(s, 'READ', self.folder / 'UPLOADS.json'), self.assertRaises(ValueError):
            s.read_gateway()

    def test_remote_secret_errors_are_not_printed(self):
        with patch.object(s, 'read_gateway', side_effect=ValueError('FAKE_SECRET')), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(s.main(['--channel', 'owb', '--video', self.video]), 1)
        self.assertNotIn('FAKE_SECRET', out.getvalue())


if __name__ == '__main__':
    unittest.main()
