"""One address for clients; one route/header list for both hosts."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from board_site import site_url
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '05_Analytics/kanban/board_site'
class BoardSite(unittest.TestCase):
    def test_setting_and_override(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(site_url(), json.loads((ROOT / 'studio/board_site.json').read_text())['url'])
        with patch.dict(os.environ, {'BOARD_SITE_URL': 'https://board.example/'}):
            self.assertEqual(site_url(), 'https://board.example')
    def test_host_rules(self):
        spec = importlib.util.spec_from_file_location('site_build', SITE / 'build.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            mod.build_host_config(out)
            config = json.loads((SITE / 'vercel.json').read_text())
            for rule in config['redirects']:
                self.assertIn(f"{rule['source']} {rule['destination']} ", (out / '_redirects').read_text())
            self.assertNotIn('/tracker /tracker.html 200', (out / '_redirects').read_text())
            for rule in config['headers']:
                self.assertIn(rule['source'] + '\n', (out / '_headers').read_text())
            self.assertEqual(json.loads((out / '_routes.json').read_text())['include'], ['/api/*'])
            self.assertTrue((out / '_worker.js/index.js').exists())
            self.assertFalse((out / 'api').exists())

    def test_no_retired_host_in_current_scripts_or_docs(self):
        retired = "studio-kanban" + ".vercel.app"
        offenders = []
        for name in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines():
            p = ROOT / name
            if name.startswith(("_archive/", "jobs/")) or not p.is_file():
                continue
            if p.suffix not in {".py", ".js", ".mjs", ".cjs", ".sh", ".md", ".mdc", ".json"}:
                continue
            try:
                if retired in p.read_text():
                    offenders.append(name)
            except UnicodeError:
                continue
        self.assertEqual(offenders, [], "Retired board address: " + ", ".join(offenders))

    def test_noindex_all_paths(self):
        config = json.loads((SITE / "vercel.json").read_text())
        self.assertTrue(any(rule["source"] == "/*" and
            {"key": "X-Robots-Tag", "value": "noindex, nofollow"} in rule["headers"]
            for rule in config["headers"]))
