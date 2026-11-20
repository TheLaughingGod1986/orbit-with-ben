"""Exercise the timer with separate code/record repos and no network or credentials."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class BufferTimerLayout(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.engine = self.base / 'engine with spaces'
        self.records = self.base / 'records with spaces'
        self.bin = self.base / 'bin'
        self.trace = self.base / 'trace.jsonl'
        for folder in (self.engine / 'scripts', self.engine / 'channels',
                       self.engine / '07_Content-Ops/launchd', self.records / '07_Content-Ops',
                       self.records / '00_Brand/Channel-Setup/social', self.bin, self.base / 'home'):
            folder.mkdir(parents=True)
        shutil.copy2(SOURCE / 'scripts/engine_guard.py', self.engine / 'scripts/engine_guard.py')
        self.script = self.engine / '07_Content-Ops/launchd/buffer-check.sh'
        shutil.copy2(SOURCE / self.script.relative_to(self.engine), self.script)
        (self.records / '07_Content-Ops/.env').write_text('# empty fixture\n')
        for tool in ('git', 'npx', 'osascript'):
            file = self.bin / tool
            file.write_text('#!' + sys.executable + '''
import json, os, sys
from pathlib import Path
name=Path(sys.argv[0]).name
args=sys.argv[1:]
with open(os.environ['TRACE'], 'a') as out:
    out.write(json.dumps({'tool':name,'args':args,'cwd':os.getcwd()})+'\\n')
if name == 'npx':
    if 'record-root' in args:
        print(os.environ['RECORDS'])
        sys.exit(int(os.environ.get('ROOT_EXIT', '0')))
    sys.exit(int(os.environ.get('CHECK_EXIT', '0')))
if name == 'git':
    if 'rev-parse' in args: print('main')
    if 'status' in args: print(' M 00_Brand/Channel-Setup/social/BUFFER_POSTS.json')
''')
            file.chmod(0o755)
        (self.bin / 'python3').symlink_to(sys.executable)
        self.env = dict(os.environ, HOME=str(self.base / 'home'), PATH=f'{self.bin}:/usr/bin:/bin',
                        STUDIO_REPO=str(self.engine), ORBIT_REPO='/stale/legacy/path',
                        RECORDS=str(self.records), TRACE=str(self.trace))
        self.env.pop('BUFFER_ENV_FILE', None)
        self.env.pop('DESK_LOCK_ROOT', None)

    def run_timer(self):
        result = subprocess.run(['bash', str(self.script)], env=self.env, capture_output=True, text=True, timeout=10)
        rows = [json.loads(line) for line in self.trace.read_text().splitlines()]
        return result, rows

    def test_detached_code_credentials_and_record_commit_use_their_own_roots(self):
        result, rows = self.run_timer()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [r for r in rows if r['tool'] == 'npx']
        self.assertEqual(len(calls), 3)
        for call in calls:
            self.assertEqual(call['cwd'], str(self.engine / '07_Content-Ops'))
        for call in calls[1:]:
            self.assertIn('--env-file=' + str(self.records / '07_Content-Ops/.env'), call['args'])
        self.assertEqual(calls[-1]['args'][-2:], ['--channel', 'hos'])
        writes = [r for r in rows if r['tool'] == 'git' and any(x in r['args'] for x in ['add','commit','push'])]
        self.assertEqual(len(writes), 3)
        for row in writes:
            self.assertEqual(row['args'][:2], ['-C', str(self.records)])

    def test_missing_record_root_or_credentials_never_calls_check_or_commits(self):
        for invalid in ('relative', str(self.base / 'missing')):
            self.env['RECORDS'] = invalid
            result, rows = self.run_timer()
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(any('check' in r['args'] or 'commit' in r['args'] for r in rows))
            self.trace.unlink()
        self.env['RECORDS'] = str(self.records)
        (self.records / '07_Content-Ops/.env').unlink()
        result, rows = self.run_timer()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any('check' in r['args'] for r in rows))

    def test_lock_contention_does_not_run_second_profile_or_commit(self):
        self.env['CHECK_EXIT'] = '75'
        result, rows = self.run_timer()
        self.assertEqual(result.returncode, 75)
        self.assertEqual(sum('check' in r['args'] for r in rows), 1)
        self.assertFalse(any('commit' in r['args'] for r in rows))


if __name__ == '__main__':
    unittest.main()
