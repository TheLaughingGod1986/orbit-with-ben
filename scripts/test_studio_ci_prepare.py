import hashlib
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import studio_ci_prepare as ci


class Prepare(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = pathlib.Path(self.tmp.name) / 'staged'
        # This is a pre-cutover renderer. Its input fixture must stay pre-cutover
        # even when this test runs inside the already-adapted studio export.
        self.root = pathlib.Path(self.tmp.name) / 'source'
        def put(rel, text):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        put('channels/channels.json', json.dumps({
            'studio': {'default_channel': 'sample', 'github': 'owner/channel'},
            'channels': [{'slug': 'sample', 'home': True}]}))
        put('studio/channel.json', json.dumps({'repo': {
            'url': 'https://github.com/owner/channel.git', 'env': 'SAMPLE_REPO'}}))
        common = "name: Check\non:\n  pull_request:\n    paths: ['**', '!jobs/**']\njobs:\n  check:\n    steps:\n      - uses: actions/setup-python@v5\n"
        put('.github/workflows/rules-check.yml', common +
            "      - if: steps.scope.outputs.rules == 'true'\n        run: python3 scripts/studio.py status --check\n" +
            "      - run: python3 scripts/sync_rules.py --check\n")
        put('.github/workflows/notes-check.yml', common)
        put('.github/workflows/core-check.yml', "if: github.repository == 'owner/channel'\n")
        put('.github/workflows/content-ops.yml', 'steps: [npm ci, npm run typecheck, npm run lint, npm test]\n')
        put('studio-core/CORE_FILES.json', json.dumps({'files': {
            '.github/workflows/core-check.yml': 'old-hash', 'unchanged.py': 'retained-hash'}}))
        self.sha = 'a' * 40

    def test_stages_without_changing_live_templates(self):
        paths = [self.root / '.github/workflows' / n for n in ci.WORKFLOWS]
        before = [p.read_bytes() for p in paths]
        self.assertEqual(ci.prepare(self.root, self.out, self.sha, 'owner/engine'), 5)
        self.assertEqual([p.read_bytes() for p in paths], before)
        for name in ('rules-check.yml', 'notes-check.yml'):
            text = (self.out / '.github/workflows' / name).read_text()
            self.assertIn('ref: ' + self.sha, text)
            self.assertIn('persist-credentials: false', text)
            self.assertIn('${{ github.workspace }}/.ci-channels/default', text)
        rules = (self.out / '.github/workflows/rules-check.yml').read_text()
        self.assertNotIn('run: python3 scripts/studio.py status --check', rules)
        self.assertIn('run: python3 scripts/sync_rules.py --check', rules)
        self.assertIn('!jobs/**', rules)
        self.assertIn("github.repository == 'owner/engine'", (self.out / '.github/workflows/core-check.yml').read_text())
        self.assertEqual((self.out / '.github/workflows/content-ops.yml').read_bytes(), before[3])
        lock = json.loads((self.out / 'studio-core/CORE_FILES.json').read_text())
        old = json.loads((self.root / 'studio-core/CORE_FILES.json').read_text())
        for path, digest in lock['files'].items():
            expected = hashlib.sha256((self.out / path).read_bytes()).hexdigest() if (self.out / path).is_file() else old['files'][path]
            self.assertEqual(digest, expected)

    def test_refuses_existing_output(self):
        self.out.mkdir()
        marker = self.out / 'keep'
        marker.write_text('keep')
        with self.assertRaises(FileExistsError):
            ci.prepare(self.root, self.out, self.sha, 'owner/engine')
        self.assertEqual(marker.read_text(), 'keep')

    def test_rejects_unpinned_ref_and_invalid_repo_before_writing(self):
        for sha, repo in [('main', 'owner/engine'), (self.sha, 'owner/engine\ninjected')]:
            with self.assertRaises(ValueError):
                ci.prepare(self.root, self.out, sha, repo)
            self.assertFalse(self.out.exists())

    def test_changed_template_fails_closed(self):
        original = pathlib.Path.read_text
        def read(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            return text.replace('python3 scripts/studio.py status --check', 'different command') if path.name == 'rules-check.yml' else text
        with patch.object(pathlib.Path, 'read_text', read), self.assertRaises(ValueError):
            ci.prepare(self.root, self.out, self.sha, 'owner/engine')
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
