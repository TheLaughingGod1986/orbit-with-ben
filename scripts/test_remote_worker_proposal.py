import hashlib
import importlib.util
from pathlib import Path
import shlex
import unittest

spec = importlib.util.spec_from_file_location('proposal', Path(__file__).parent / 'mini/prepare_remote_worker.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SOURCE = b'''#!/bin/bash
set -euo pipefail
# Local authentication setup must remain byte-identical.
AGENT=/local/agent
exec /usr/bin/caffeinate -dims \\
  "$AGENT" worker \\
  --computer-use \\
  --name "existing-worker" \\
  --idle-release-timeout 0 \\
  --data-dir "/local/identity" \\
  --worker-dir "/old channel" \\
  --worker-dir "/unrelated" \\
  start --verbose
'''

class Proposal(unittest.TestCase):
    def setUp(self):
        self.roots = dict(zip(m.ROOTS, ('/new engine', '/old channel', '/hos', '/ww2')))

    def render(self, source=SOURCE):
        return m.render(source, hashlib.sha256(source).hexdigest(), self.roots)

    def test_preserves_identity_auth_and_existing_access(self):
        result = self.render().decode()
        before, after = result.split('exec /usr/bin/caffeinate')
        self.assertTrue(before.startswith(SOURCE.decode().split('exec /usr/bin/caffeinate')[0]))
        args = shlex.split(after.replace('\\\n', ''))
        dirs = [args[i+1] for i, a in enumerate(args) if a == '--worker-dir']
        self.assertEqual(dirs, ['/old channel', '/unrelated', '/new engine'])
        self.assertEqual(args[args.index('--name')+1], 'existing-worker')
        self.assertEqual(args[args.index('--data-dir')+1], '/local/identity')
        for key in m.ROOTS:
            self.assertIn('export ' + key + '=', before)

    def test_refuses_changed_source(self):
        with self.assertRaises(ValueError):
            m.render(SOURCE, '0'*64, self.roots)

    def test_shell_metacharacters_are_literal(self):
        self.roots['STUDIO_REPO'] = "/engine/$(touch BAD)' space"
        output = self.render().decode()
        line = next(l for l in output.splitlines() if l.startswith('export STUDIO_REPO='))
        self.assertEqual(shlex.split(line)[1], 'STUDIO_REPO=' + self.roots['STUDIO_REPO'])

    def test_refuses_unknown_options(self):
        with self.assertRaises(ValueError):
            self.render(SOURCE.replace(b'--name', b'--pool'))

    def test_refuses_relative_multiline_or_missing_roots(self):
        for value in ('relative', '/bad\ncommand', '/bad\rcommand'):
            self.roots['STUDIO_REPO'] = value
            with self.assertRaises(ValueError): self.render()
        self.roots.pop('WW2_REPO')
        with self.assertRaises(ValueError): self.render()

    def test_refuses_duplicate_engine_and_unreviewed_tail(self):
        self.roots['STUDIO_REPO'] = '/old channel'
        with self.assertRaises(ValueError): self.render()
        self.roots['STUDIO_REPO'] = '/new engine'
        with self.assertRaises(ValueError): self.render(SOURCE + b'echo unexpected\n')

if __name__ == '__main__': unittest.main()
