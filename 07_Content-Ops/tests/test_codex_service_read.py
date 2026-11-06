import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

spec = importlib.util.spec_from_file_location('service', Path(__file__).parents[1] / 'scripts/codex_service_read.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class ServiceBoundaryTests(unittest.TestCase):
    def args(self, operation='channel', channel='owb', **kw):
        return s.argparse.Namespace(channel=channel, operation=operation, video=None, network=None,
                                    start=None, end=None, dry_run=False) if not kw else self.override(self.args(operation, channel), kw)

    def override(self, args, kw):
        vars(args).update(kw)
        return args

    def test_invalid_inputs_fail_before_network(self):
        cases = [self.args(channel='other'), self.args('delete'), self.args('video'),
                 self.args('video', video='../secrets'), self.args('channel', video='abcdefghijk'),
                 self.args('buffer-status', video='abcdefghijk', network='tiktok'),
                 self.args('analytics', start='2026-02-30', end='2026-03-01'),
                 self.args('analytics', start='2026-11-02', end='2026-11-01'),
                 self.args('analytics', start='2026-01-01', end='9999-12-31')]
        with patch.object(s, 'request') as req:
            for args in cases:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    s.execute(args, {})
            req.assert_not_called()

    def test_cli_refuses_methods_urls_payloads_and_abbreviations(self):
        for extra in (['--url', 'https://example.com'], ['--method', 'DELETE'], ['--body', '{}'], ['--oper', 'channel']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                s.main(['--channel', 'owb', '--operation', 'channel', *extra])

    def test_dry_run_has_no_network_or_credential_read(self):
        with patch.object(s, 'request') as req, patch.object(s, 'settings') as cfg, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(s.main(['--channel', 'hos', '--operation', 'channel', '--dry-run']), 0)
        req.assert_not_called()
        cfg.assert_not_called()

    def test_existing_token_refresh_is_only_oauth_operation(self):
        cfg = {'GOOGLE_CLIENT_ID': 'fake-client', 'GOOGLE_CLIENT_SECRET': 'fake-secret',
               'YT_ANALYTICS_REFRESH_TOKEN_HOS': 'fake-refresh'}
        with patch.object(s, 'request', return_value={'access_token': 'fake-access'}) as req:
            self.assertEqual(s.token(cfg, 'hos'), 'fake-access')
            host, path, method, body, _ = req.call_args.args
            self.assertEqual((host, path, method), ('oauth2.googleapis.com', '/token', 'POST'))
            self.assertEqual(parse_qs(body)['grant_type'], ['refresh_token'])

    def test_wrong_login_refused_before_selected_read(self):
        with patch.object(s, 'token', return_value='fake'), patch.object(s, 'youtube_get', return_value={'items': [{'id': s.CHANNELS['hos']}]}) as get:
            with self.assertRaises(ValueError):
                s.execute(self.args(), {})
            self.assertEqual(get.call_count, 1)

    def test_video_cross_channel_and_missing_refused(self):
        mine = {'items': [{'id': s.CHANNELS['owb']}]}
        for videos in ({'items': []}, {'items': [{'id': 'abcdefghijk', 'snippet': {'channelId': s.CHANNELS['hos']}}]}):
            with patch.object(s, 'token', return_value='fake'), patch.object(s, 'youtube_get', side_effect=[mine, videos]):
                with self.assertRaises(ValueError):
                    s.execute(self.args('video', video='abcdefghijk'), {})

    def test_analytics_pins_channel_and_query(self):
        with patch.object(s, 'token', return_value='fake'), patch.object(s, 'youtube_get', return_value={'items': [{'id': s.CHANNELS['hos']}]}), patch.object(s, 'request', return_value={'rows': []}) as req:
            self.assertEqual(s.execute(self.args('analytics', 'hos', start='2026-10-01', end='2026-10-02'), {}), {'rows': []})
            host, path = req.call_args.args
            self.assertEqual(host, 'youtubeanalytics.googleapis.com')
            query = parse_qs(urlsplit(path).query)
            self.assertEqual(query['ids'], ['channel==' + s.CHANNELS['hos']])
            self.assertEqual(query['dimensions'], ['day'])

    def test_http_boundary_blocks_mutations_redirect_hosts_and_arbitrary_routes(self):
        with patch.object(s.http.client, 'HTTPSConnection') as conn:
            for host, path, method, body in [('example.com', '/', 'GET', None),
                     ('www.googleapis.com', '/youtube/v3/videos', 'DELETE', None),
                     ('www.googleapis.com', '/youtube/v3/videos', 'PUT', '{}'),
                     ('oauth2.googleapis.com', '/authorize', 'GET', None),
                     ('api.buffer.com', '/', 'POST', json.dumps({'query': 'mutation { deletePost }'}))]:
                with self.subTest(host=host, method=method), self.assertRaises(ValueError):
                    s.request(host, path, method, body)
            conn.assert_not_called()

    def test_registered_buffer_read_uses_only_profile_key_and_no_caller_post_id(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(s, 'ROOT', Path(tmp)):
            folder = Path(tmp) / s.SOCIAL / 'hos'
            folder.mkdir(parents=True)
            post_id = 'a' * 24
            (folder / 'BUFFER_POSTS.json').write_text(json.dumps({'videos': {'abcdefghijk': {'kind': 'short', 'channels': {'instagram': {'postId': post_id}}}}}))
            cfg = {'BUFFER_HOS_API_KEY': 'fake-hos', 'BUFFER_API_KEY': 'fake-owb'}
            with patch.object(s, 'request', return_value={'data': {'post': {'id': post_id, 'status': 'scheduled'}}}) as req:
                result = s.execute(self.args('buffer-status', 'hos', video='abcdefghijk', network='instagram'), cfg)
                self.assertEqual(result['status'], 'scheduled')
                host, path, method, body, headers = req.call_args.args
                self.assertEqual((host, path, method), ('api.buffer.com', '/', 'POST'))
                self.assertEqual(headers['Authorization'], 'Bearer fake-hos')
                self.assertEqual(json.loads(body), {'query': s.GET_POST, 'variables': {'input': {'id': post_id}}})

    def test_failure_output_never_prints_remote_or_token_values(self):
        output = io.StringIO()
        with patch.object(s, 'settings', side_effect=ValueError('FAKE_SECRET')), contextlib.redirect_stdout(output):
            self.assertEqual(s.main(['--channel', 'owb', '--operation', 'channel']), 1)
        self.assertNotIn('FAKE_SECRET', output.getvalue())

    def test_non200_does_not_follow_redirect_or_read_body(self):
        with patch.object(s.http.client, 'HTTPSConnection') as connection:
            connection.return_value.getresponse.return_value.status = 302
            with self.assertRaises(ValueError):
                s.request('www.googleapis.com', '/youtube/v3/channels?mine=true')
            connection.return_value.getresponse.return_value.read.assert_not_called()
            connection.return_value.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
