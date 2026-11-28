"""Offline lock regression checks: python3 tests/desk-lock.test.py."""
import os
import json
import shutil
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

OPS = Path(__file__).resolve().parents[1]
REPO = OPS.parent
LOCK = OPS / 'scripts/desk-lock.sh'
BUFFER_CHECK = OPS / 'launchd/buffer-check.sh'

# The writer CLIs import their own packages (googleapis and others), so they only run where `npm ci` has been run in
# this checkout. A worker's checkout has no node_modules: there the writers test is skipped, not failed (7 Nov code
# audit, row F-05b: seven failures in the MacBook worker's checkouts). CI runs it after npm ci.
HAS_DEPS = (OPS / 'node_modules' / 'tsx').exists()


def prepare_timer_repo(repo):
    (repo/'scripts').mkdir(exist_ok=True)
    shutil.copy2(REPO/'scripts/engine_guard.py', repo/'scripts/engine_guard.py')
    (repo/'00_Brand/Channel-Setup/social').mkdir(parents=True)
    (repo/'07_Content-Ops/.env').write_text('')


class DeskLockTests(unittest.TestCase):
    def test_direct_buffer_refuses_retired_engine_before_lock_and_root_probe_is_read_only(self):
        with tempfile.TemporaryDirectory(prefix='buffer-identity-') as root:
            base = Path(root)
            env = {**os.environ, 'HOME': root, 'DESK_LOCK_ROOT': str(base/'locks')}
            command = ['node', '--import', 'tsx', 'scripts/buffer-mirror.ts']
            probe = subprocess.run(command + ['record-root'], cwd=OPS, env=env,
                                   capture_output=True, text=True, timeout=15)
            self.assertEqual(probe.returncode, 0, probe.stderr)
            self.assertTrue(Path(probe.stdout.strip()).is_absolute())
            self.assertFalse((base/'locks').exists())
            marker = base/'_desk/state/active-studio.json'
            marker.parent.mkdir(parents=True)
            marker.write_text(json.dumps({'version': 1, 'github': 'fixture/other-engine'}))
            for operation in ('check', 'record-root'):
                result = subprocess.run(command + [operation], cwd=OPS, env=env,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('engine identity guard failed', result.stderr)
                self.assertFalse((base/'locks').exists())

    def test_detached_cli_resolves_records_without_credentials_or_lock(self):
        with tempfile.TemporaryDirectory(prefix='buffer-detached-') as root:
            base = Path(root)
            engine, channel = base/'engine', base/'channel'
            ops = engine/'07_Content-Ops'
            ops.mkdir(parents=True)
            for name in ('scripts', 'src'):
                shutil.copytree(OPS/name, ops/name)
            shutil.copy2(OPS/'tsconfig.json', ops/'tsconfig.json')
            (ops/'node_modules').symlink_to(OPS/'node_modules', target_is_directory=True)
            (engine/'scripts').mkdir()
            shutil.copy2(REPO/'scripts/engine_guard.py', engine/'scripts/engine_guard.py')
            (engine/'channels/owb').mkdir(parents=True)
            (engine/'channels/channels.json').write_text(json.dumps({
                'studio': {'github': 'fixture/studio'},
                'channels': [{'slug': 'owb', 'env': 'TEST_RECORDS'}]}))
            (engine/'channels/owb/channel.json').write_text(json.dumps({'repo': {'env': 'TEST_RECORDS'}}))
            (channel/'studio').mkdir(parents=True)
            (channel/'studio/channel.json').write_text(json.dumps({'slug': 'owb'}))
            env = {**os.environ, 'HOME': root, 'TEST_RECORDS': str(channel),
                   'DESK_LOCK_ROOT': str(base/'locks')}
            cmd = ['node', '--import', 'tsx', 'scripts/buffer-mirror.ts', 'record-root']
            result = subprocess.run(cmd, cwd=ops, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), str(channel))
            self.assertFalse((base/'locks').exists())
            self.assertFalse((engine/'00_Brand').exists())
            del env['TEST_RECORDS']
            result = subprocess.run(cmd, cwd=ops, env=env, capture_output=True, text=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('absolute TEST_RECORDS', result.stderr)
            self.assertFalse((base/'locks').exists())

    def test_daily_wrapper_reaches_both_locked_clis_without_self_deadlock(self):
        with tempfile.TemporaryDirectory(prefix='buffer-daily-success-') as root:
            repo = Path(root)/'repo'
            ops = repo/'07_Content-Ops'
            (ops/'scripts').mkdir(parents=True)
            prepare_timer_repo(repo)
            (ops/'node_modules').symlink_to(OPS/'node_modules',target_is_directory=True)
            calls = Path(root)/'calls'
            fixture = "import fs from 'node:fs';\nimport {ensureDeskLock} from " + repr(str(OPS/'scripts/with-desk-lock.ts')) + ";\nif(process.argv[2]==='record-root'){console.log(process.env.ORBIT_REPO);process.exit(0)}\nensureDeskLock();\nfs.appendFileSync(process.env.RUN_LOG!,process.argv.includes('hos')?'hos\\n':'owb\\n');\n"
            (ops/'scripts/buffer-mirror.ts').write_text(fixture)
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'checkout','-qb','offline-test'],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture',
                            'commit','-q','--allow-empty','-m','fixture'],check=True)
            env={**os.environ,'ORBIT_REPO':str(repo),'STUDIO_REPO':str(repo),'DESK_LOCK_ROOT':str(Path(root)/'locks'),'RUN_LOG':str(calls)}
            result=subprocess.run(['bash',str(BUFFER_CHECK)],env=env,capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual(calls.read_text().splitlines(),['owb','hos'])
            self.assertFalse((Path(root)/'locks/youtube-buffer.lock').exists())

    def test_npx_tsx_cli_owns_one_real_lock_without_outer_wrapper(self):
        with tempfile.TemporaryDirectory(prefix='buffer-npx-lock-') as root:
            fixture = Path(root) / 'entry.ts'
            ready, release = Path(root) / 'ready', Path(root) / 'release'
            fixture.write_text("import fs from 'node:fs';\nimport {ensureDeskLock} from " + repr(str(OPS / 'scripts/with-desk-lock.ts')) + ";\nensureDeskLock();\nfs.writeFileSync(process.env.READY_FILE!, 'locked');\nif(process.env.HOLD==='1'){const t=setInterval(()=>{if(fs.existsSync(process.env.RELEASE_FILE!))clearInterval(t)},25)}else{process.exitCode=23}\n")
            env = {**os.environ, 'DESK_LOCK_ROOT':root, 'READY_FILE':str(ready), 'RELEASE_FILE':str(release)}
            command = ['npx','--no-install','tsx',str(fixture)]
            holder = subprocess.Popen(command,cwd=OPS,env={**env,'HOLD':'1'},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            try:
                for _ in range(300):
                    if ready.exists(): break
                    time.sleep(.02)
                self.assertTrue(ready.exists(),'npx/tsx command must enter its real operation lock')
                result=subprocess.run(command,cwd=OPS,env=env,capture_output=True,timeout=15)
                self.assertEqual(result.returncode,75,'another live writer must remain excluded')
            finally:
                release.touch();holder.wait(timeout=15)
            self.assertFalse((Path(root)/'youtube-buffer.lock').exists())
            result=subprocess.run(command,cwd=OPS,env=env,capture_output=True,timeout=15)
            self.assertEqual(result.returncode,23,result.stderr)
            self.assertFalse((Path(root)/'youtube-buffer.lock').exists())

    def test_writers_and_cleanup(self):
        if not HAS_DEPS:
            self.skipTest('07_Content-Ops/node_modules is missing here (run npm ci); CI runs this test')
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            holder = subprocess.Popen(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'sleep', '60'],
                env=env, stdout=subprocess.DEVNULL,
            )
            try:
                for _ in range(200):
                    if (directory / 'owner.txt').exists():
                        break
                    time.sleep(.01)
                self.assertTrue((directory / 'owner.txt').exists())
                for name in ['youtube-package-upload', 'buffer-mirror', 'retitle-videos',
                             'update-pinned-comment', 'set-synthetic-disclosure',
                             'update-shorts-listings']:
                    with self.subTest(writer=name):
                        result = subprocess.run(
                            ['node', '--import', 'tsx', f'scripts/{name}.ts'],
                            cwd=OPS, env=env, capture_output=True, text=True, timeout=10,
                        )
                        self.assertEqual(result.returncode, 75, result.stderr)
            finally:
                holder.terminate()
                holder.wait(timeout=10)
            self.assertFalse(directory.exists())
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'bash', '-c', 'exit 23'],
                env=env, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 23)
            self.assertFalse(directory.exists())
            # No arguments hits usage offline, verifying nested lock inheritance.
            result = subprocess.run(
                ['node', '--import', 'tsx', 'scripts/buffer-mirror.ts'],
                cwd=OPS, env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('Usage:', result.stderr)
            self.assertFalse(directory.exists())
            # A competing creator may not have written metadata yet.
            directory.mkdir()
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'true'],
                env=env, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 75)
            self.assertTrue(directory.exists())

    def test_stale_reclaim_when_pid_dead_and_owner_older_than_5m(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            directory.mkdir()
            owner = directory / 'owner.txt'
            # Use a pid that is almost certainly dead and not ours.
            owner.write_text('pid=1\nuser=test\nstarted_at=1970-01-01T00:00:00+0000\n')
            # Make owner.txt older than 5 minutes.
            old = time.time() - 301
            os.utime(owner, (old, old))
            # If pid 1 is alive (init/launchd), pick another dead pid.
            if subprocess.call(['kill', '-0', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                owner.write_text('pid=2147483646\nuser=test\nstarted_at=1970-01-01T00:00:00+0000\n')
                os.utime(owner, (old, old))
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'bash', '-c', 'exit 42'],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 42, result.stderr)
            self.assertFalse(directory.exists())

    def test_fresh_dead_owner_is_not_reclaimed(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            env = {**os.environ, 'DESK_LOCK_ROOT': root}
            directory = Path(root) / 'youtube-buffer.lock'
            directory.mkdir()
            owner = directory / 'owner.txt'
            owner.write_text('pid=2147483646\nuser=test\nstarted_at=recent\n')
            # Fresh mtime (<5m): fail closed even though pid is dead.
            result = subprocess.run(
                ['bash', str(LOCK), 'youtube-buffer', '--', 'true'],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 75, result.stderr)
            self.assertTrue(directory.exists())

    def test_buffer_check_notifies_on_second_consecutive_75(self):
        with tempfile.TemporaryDirectory(prefix='owb-lock-') as root:
            bin_dir = Path(root) / 'bin'
            bin_dir.mkdir()
            notify_log = Path(root) / 'notify.log'
            osascript = bin_dir / 'osascript'
            osascript.write_text(
                '#!/bin/bash\necho "$@" >> "$NOTIFY_LOG"\n'
            )
            osascript.chmod(0o755)
            # Test the daily supervisor's repeated-75 policy independently of credentials.
            # Real competing holders and the actual npx/tsx chain are exercised above.
            npx = bin_dir / 'npx'
            npx.write_text('#!/bin/sh\ncase "$*" in *record-root*) echo "$ORBIT_REPO"; exit 0;; esac\nexit 75\n')
            npx.chmod(0o755)
            repo = Path(root) / 'repo'
            (repo/'07_Content-Ops').mkdir(parents=True)
            prepare_timer_repo(repo)
            subprocess.run(['git','init','-q',str(repo)],check=True)
            subprocess.run(['git','-C',str(repo),'checkout','-qb','offline-test'],check=True)
            subprocess.run(['git','-C',str(repo),'-c','user.name=Fixture','-c','user.email=fixture',
                            'commit','-q','--allow-empty','-m','fixture'],check=True)
            env = {
                **os.environ,
                'DESK_LOCK_ROOT': root,
                'ORBIT_REPO': str(repo),
                'STUDIO_REPO': str(repo),
                'PATH': f'{bin_dir}:{os.environ.get("PATH", "")}',
                'NOTIFY_LOG': str(notify_log),
            }
            first = subprocess.run(['bash', str(BUFFER_CHECK)], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(first.returncode, 75, first.stderr + first.stdout)
            self.assertFalse(notify_log.exists(), 'first 75 must stay quiet')
            second = subprocess.run(['bash', str(BUFFER_CHECK)], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(second.returncode, 75, second.stderr + second.stdout)
            self.assertTrue(notify_log.exists(), 'second consecutive 75 must notify')
            self.assertIn('twice in a row', notify_log.read_text())


if __name__ == '__main__':
    unittest.main()
