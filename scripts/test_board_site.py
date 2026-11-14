"""One address for clients; one route/header list for both hosts."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch
from board_site import board_request, site_url
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '05_Analytics/kanban/board_site'
class BoardSite(unittest.TestCase):
    def test_setting_and_override(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(site_url(), json.loads((ROOT / 'studio/board_site.json').read_text())['url'])
        with patch.dict(os.environ, {'BOARD_SITE_URL': 'https://board.example/'}):
            self.assertEqual(site_url(), 'https://board.example')
    def test_no_retired_board_address(self):
        retired = 'studio-kanban.' + 'vercel.app'
        names = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
        violations = []
        for name in names:
            if name.startswith(('_archive/', 'jobs/')):
                continue
            path = ROOT / name
            try:
                body = path.read_text()
            except (OSError, UnicodeError):
                continue
            if retired in body:
                violations.append(name)
        self.assertEqual(violations, [], 'Retired board address in tracked files')

    def test_explicit_watch_uses_configured_board(self):
        import kanban_snapshot as ks
        self.assertIsNotNone(ks.explicit_watch({'url': site_url() + '/api/watch?v=example'}))
        self.assertIsNone(ks.explicit_watch({'url': 'https://untrusted.example/api/watch?v=x'}))

    def test_client_identifies_itself(self):
        request = board_request(site_url() + '/api/checks')
        self.assertEqual(request.full_url, site_url() + '/api/checks')
        self.assertEqual(request.get_header('User-agent'), 'studio-kanban client')

    def test_host_rules(self):
        spec = importlib.util.spec_from_file_location('site_build', SITE / 'build.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            mod.build_host_config(out)
            self.assertIn('/*\n  X-Robots-Tag: noindex, nofollow\n', (out / '_headers').read_text())
            config = json.loads((SITE / 'vercel.json').read_text())
            for rule in config['redirects']:
                self.assertIn(f"{rule['source']} {rule['destination']} ", (out / '_redirects').read_text())
            self.assertNotIn('/tracker /tracker.html 200', (out / '_redirects').read_text())
            for rule in config['headers']:
                self.assertIn(rule['source'] + '\n', (out / '_headers').read_text())
            self.assertEqual(json.loads((out / '_routes.json').read_text())['include'], ['/api/*'])
            self.assertTrue((out / '_worker.js/index.js').exists())
            self.assertFalse((out / 'api').exists())
