import contextlib
import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('r2', Path(__file__).parents[1] / 'scripts/codex_r2_upload.py')
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)


class R2BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.root = root
        self.patch = patch.multiple(r2, ROOT=root, HOS=root / 'hos')
        self.patch.start()
        self.addCleanup(self.patch.stop)
        (root / r2.SOCIAL).mkdir(parents=True)
        (root / '07_Content-Ops').mkdir()
        self.media = root / 'video.mp4'
        self.media.write_bytes(b'\x00\x00\x00\x18ftypisom' + b'x' * 100)
        self.record({'kind': 'short', 'file': 'video.mp4'})
        self.cfg = {'R2_ACCOUNT_ID': 'a' * 32, 'R2_ACCESS_KEY_ID': 'fake-id',
                    'R2_SECRET_ACCESS_KEY': 'fake-secret', 'R2_PUBLIC_URL': 'https://pub-test.r2.dev'}
        self.env()

    def record(self, entry):
        (self.root / r2.SOCIAL / 'UPLOADS.json').write_text(json.dumps({'videos': {'abcdefghijk': entry}}))

    def env(self, **overrides):
        (self.root / '07_Content-Ops/.env').write_text('\n'.join(k + '=' + v for k, v in (self.cfg | overrides).items()))

    def args(self, *extra):
        return ['--channel', 'owb', '--video', 'abcdefghijk', '--role', 'media', *extra]

    def test_registered_media_scoped_key(self):
        file, key = r2.asset('owb', 'abcdefghijk', 'media')
        self.assertEqual(file, self.media)
        self.assertRegex(key, r'^social/abcdefghijk-[a-f0-9]{32}\.mp4$')

    def test_path_traversal_and_unregistered_files_refused(self):
        for raw in ('../../etc/passwd', '/etc/passwd', 'absent.mp4'):
            self.record({'kind': 'short', 'file': raw})
            with self.assertRaises(ValueError):
                r2.asset('owb', 'abcdefghijk', 'media')

    def test_secrets_renamed_as_media_refused(self):
        self.media.write_text('a secret pretending to be an mp4')
        with self.assertRaises(ValueError):
            r2.asset('owb', 'abcdefghijk', 'media')

    def test_cross_channel_long_and_bad_ids_refused(self):
        for channel, video, role in [('other', 'abcdefghijk', 'media'), ('owb', '../anything', 'media'),
                                     ('hos', 'abcdefghijk', 'thumb'), ('owb', 'abcdefghijk', 'delete')]:
            with self.assertRaises((ValueError, OSError)):
                r2.asset(channel, video, role)
        self.record({'kind': 'long', 'file': 'video.mp4'})
        with self.assertRaises(ValueError):
            r2.asset('owb', 'abcdefghijk', 'media')

    def test_bucket_and_public_host_overrides_refused(self):
        for overrides in ({'R2_BUCKET': 'elsewhere'}, {'R2_ACCOUNT_ID': 'attacker.com'},
                          {'R2_PUBLIC_URL': 'https://example.com'}, {'R2_PUBLIC_URL': 'https://pub-test.r2.dev/other'}):
            self.env(**overrides)
            with self.assertRaises(ValueError):
                r2.settings()

    def test_inherited_environment_has_no_effect(self):
        with patch.dict('os.environ', {'R2_ACCOUNT_ID': 'attacker', 'R2_BUCKET': 'attacker'}):
            self.assertEqual(r2.settings(), self.cfg)

    def test_signature_pins_destination_method_and_no_overwrite(self):
        host, uri, headers = r2.signature(self.cfg, 'social/abcdefghijk-abc.mp4', '0' * 64,
                                          dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc))
        self.assertEqual(host, 'a' * 32 + '.r2.cloudflarestorage.com')
        self.assertEqual(uri, '/owb-media/social/abcdefghijk-abc.mp4')
        self.assertEqual(headers['if-none-match'], '*')
        self.assertIn('if-none-match', headers['Authorization'])
        self.assertNotIn('fake-secret', str(headers))
        # Independently cross-checked against installed aws4fetch 1.0.20 with
        # the same fixed datetime and fake credentials; no network involved.
        self.assertTrue(headers['Authorization'].endswith(
            'Signature=4614c36e165ae68d4656e7189a7cae21823566cef86cfbf306e8084e35c97322'))

    @patch.object(r2.http.client, 'HTTPSConnection')
    def test_dry_run_sends_nothing(self, connection):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(r2.main(self.args('--dry-run')), 0)
        connection.assert_not_called()

    @patch.object(r2.http.client, 'HTTPSConnection')
    def test_only_conditional_put_is_sent(self, connection):
        connection.return_value.getresponse.return_value.status = 200
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(r2.main(self.args()), 0)
        method, uri = connection.return_value.request.call_args.args
        self.assertEqual(method, 'PUT')
        self.assertTrue(uri.startswith('/owb-media/social/'))
        headers = connection.return_value.request.call_args.kwargs['headers']
        self.assertEqual(headers['if-none-match'], '*')
        self.assertEqual(int(headers['Content-Length']), self.media.stat().st_size)
        connection.return_value.close.assert_called_once()

    def test_extra_options_rejected(self):
        for extra in ('--delete', '--bucket', '--url', '--method', '--file'):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                r2.main(self.args(extra, 'anything'))


if __name__ == '__main__':
    unittest.main()
