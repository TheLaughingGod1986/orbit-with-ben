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

spec = importlib.util.spec_from_file_location('defaults', Path(__file__).parents[1] / 'scripts/codex_youtube_defaults.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class DefaultsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'social').mkdir()
        (self.root / 'social/UPLOADS.json').write_text(json.dumps({'videos': {'abcdefghijk': {'kind': 'short'}}}))
        self.args = argparse.Namespace(channel='owb', video='abcdefghijk', apply=False)
        self.video = {'id': self.args.video, 'etag': 'version-one',
                      'snippet': {'channelId': s.CHANNELS['owb'], 'title': 'Untouched'},
                      'status': {'privacyStatus': 'private', 'uploadStatus': 'processed', 'license': 'youtube',
                                 'embeddable': False, 'publicStatsViewable': False, 'madeForKids': False,
                                 'publishAt': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)).isoformat(),
                                 'selfDeclaredMadeForKids': True, 'containsSyntheticMedia': False}}
        self.reader = SimpleNamespace(SOCIAL=Path('social'), request=lambda *_: {'access_token': 'fake-only'}, youtube_get=self.get)
        self.cfg = {'GOOGLE_CLIENT_ID': 'fake', 'GOOGLE_CLIENT_SECRET': 'fake', 'YOUTUBE_REFRESH_TOKEN': 'fake'}
        self.root_patch = patch.object(s, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def get(self, access, endpoint, params):
        if endpoint == 'channels':
            return {'items': [{'id': s.CHANNELS[self.args.channel]}]}
        return {'items': [copy.deepcopy(self.video)]}

    def test_plan_no_write(self):
        with patch.object(s, 'update') as update:
            result = s.run(self.args, self.reader, self.cfg)
        self.assertTrue(result['change'])
        update.assert_not_called()
        self.assertEqual(self.video['snippet']['title'], 'Untouched')

    def test_preserves_every_writable_field(self):
        body = s.body_for(self.video, 'owb', self.args.video)
        self.assertEqual(set(body), {'id', 'status'})
        self.assertEqual(set(body['status']), s.MUTABLE)
        for field in s.MUTABLE - {'selfDeclaredMadeForKids', 'containsSyntheticMedia'}:
            self.assertEqual(body['status'][field], self.video['status'][field])
        self.assertIs(body['status']['selfDeclaredMadeForKids'], False)
        self.assertIs(body['status']['containsSyntheticMedia'], True)

    def test_rejects_public_unscheduled_unprocessed_and_unknown(self):
        for fields in ({'privacyStatus': 'public'}, {'privacyStatus': 'unlisted'}, {'uploadStatus': 'uploaded'},
                       {'publishAt': None}, {'publishAt': '2000-01-01T00:00:00Z'},
                       {'publishAt': '2099-01-01T00:00:00'}, {'futureWritableField': True},
                       {'embeddable': None}, {'license': 'other'}):
            video = copy.deepcopy(self.video)
            video['status'].update(fields)
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                s.body_for(video, 'owb', self.args.video)

    def test_ownership_version_and_id_required(self):
        for key, value in [('id', 'other123456'), ('etag', ''), ('snippet', {'channelId': s.CHANNELS['hos']})]:
            video = {**self.video, key: value}
            with self.subTest(key=key), self.assertRaises(ValueError):
                s.body_for(video, 'owb', self.args.video)

    def test_unregistered_no_network(self):
        self.args.video = 'notregister'
        self.reader.request = unittest.mock.Mock()
        with self.assertRaises(KeyError):
            s.run(self.args, self.reader, self.cfg)
        self.reader.request.assert_not_called()

    def test_foreign_writer_no_video_or_write(self):
        self.reader.youtube_get = unittest.mock.Mock(return_value={'items': [{'id': s.CHANNELS['hos']}]})
        with patch.object(s, 'update') as update, self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)
        update.assert_not_called()
        self.assertEqual(self.reader.youtube_get.call_count, 1)

    def test_apply_rechecks_and_reads_back(self):
        self.args.apply = True
        def update(access, body, etag):
            self.assertEqual(etag, 'version-one')
            self.video['status'].update(body['status'])
            self.video['etag'] = 'version-two'
            return copy.deepcopy(self.video)
        with patch.object(s, 'update', side_effect=update) as call:
            result = s.run(self.args, self.reader, self.cfg)
        self.assertTrue(result['apply'])
        self.assertEqual(call.call_count, 1)
        self.assertIs(self.video['status']['selfDeclaredMadeForKids'], False)

    def test_idempotent_no_write(self):
        self.args.apply = True
        self.video['status'].update(selfDeclaredMadeForKids=False, containsSyntheticMedia=True)
        with patch.object(s, 'update') as update:
            self.assertFalse(s.run(self.args, self.reader, self.cfg)['change'])
        update.assert_not_called()

    def test_concurrent_change_blocks_write(self):
        self.args.apply = True
        calls = 0
        def get(*args):
            nonlocal calls
            calls += 1
            if calls == 3:
                self.video['etag'] = 'concurrent'
            return self.get(*args)
        self.reader.youtube_get = get
        with patch.object(s, 'update') as update, self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)
        update.assert_not_called()

    def test_response_mismatch_stops(self):
        self.args.apply = True
        with patch.object(s, 'update', return_value={'id': 'wrong'}), self.assertRaises(ValueError):
            s.run(self.args, self.reader, self.cfg)

    def test_cli_rejects_arbitrary_payloads(self):
        for extra in (['--privacy', 'public'], ['--publish-at', '2099-01-01'], ['--body', '{}'],
                      ['--url', 'https://example.com'], ['--delete'], ['--app']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                s.main(['--channel', 'owb', '--video', self.args.video, *extra])

    def test_transport_fixed_route_no_redirect_or_raw_error(self):
        with patch.object(s.http.client, 'HTTPSConnection') as conn:
            conn.return_value.getresponse.return_value.status = 302
            with self.assertRaises(ValueError):
                s.update('fake', {}, 'etag')
            conn.assert_called_once_with('www.googleapis.com', timeout=30)
            conn.return_value.getresponse.return_value.read.assert_not_called()
            self.assertEqual(conn.return_value.request.call_args.args[:2], ('PUT', '/youtube/v3/videos?part=status'))
            self.assertEqual(conn.return_value.request.call_args.args[3]['If-Match'], 'etag')

    def test_dependency_change_blocks_import(self):
        file = self.root / 'changed.py'
        file.write_text('raise RuntimeError("must not execute")')
        with self.assertRaises(ValueError):
            s.dependency(file, 'wrong', 'changed')

    def test_redacted_failure(self):
        with patch.object(s, 'dependency', side_effect=ValueError('secret')), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(s.main(['--channel', 'owb', '--video', self.args.video]), 1)
        self.assertNotIn('secret', out.getvalue())


if __name__ == '__main__':
    unittest.main()
