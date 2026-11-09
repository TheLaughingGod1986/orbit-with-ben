"""Local bare-remote regressions: metadata must never publish worker history."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jobs
import studio


class MetadataGit(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT, text=True).strip()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        self.remote = root / 'remote.git'
        self.work = root / 'work'
        subprocess.run(['git', 'init', '--bare', '-q', str(self.remote)], check=True)
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(self.work)], check=True)
        self.git(self.work, 'config', 'user.email', 'test@example.invalid')
        self.git(self.work, 'config', 'user.name', 'Test')
        self.films = self.work / '02_Video-Projects'
        self.path = self.films / '001_Test' / 'status.json'
        self.path.parent.mkdir(parents=True)
        studio.save(self.path, {'film': '001', 'title': 'Test', 'stages': {}, 'claims': [], 'next': ''})
        studio.write_status(self.films)
        self.queue = self.work / 'jobs' / 'queue.json'
        jobs.save({'next_id': 1, 'jobs': []}, self.queue)
        (self.work / 'JOBS.md').write_text('queue\n')
        self.git(self.work, 'add', '.')
        self.git(self.work, 'commit', '-qm', 'base')
        self.git(self.work, 'remote', 'add', 'origin', str(self.remote))
        self.git(self.work, 'push', '-q', 'origin', 'main')
        self.base = self.remote_head()
        for name, value in [('ROOT', self.work), ('FILMS', self.films)]:
            p = patch.object(studio, name, value)
            p.start()
            self.addCleanup(p.stop)
        for name, value in [('ROOT', self.work), ('QUEUE', self.queue), ('JOBS_MD', self.work / 'JOBS.md')]:
            p = patch.object(jobs, name, value)
            p.start()
            self.addCleanup(p.stop)

    def remote_head(self):
        return self.git(self.remote, 'rev-parse', 'main')

    def unrelated(self, root=None):
        root = root or self.work
        (root / 'implementation.py').write_text('unreviewed = True\n')
        self.git(root, 'add', 'implementation.py')
        self.git(root, 'commit', '-qm', 'unreviewed implementation')
        return self.git(root, 'rev-parse', 'HEAD')

    def run_metadata(self, kind):
        if kind == 'studio':
            return studio.with_git(self.path, lambda d: d.update(next='intended update'), 'metadata', self.films)
        def apply(d):
            d['next_id'] += 1
            return 'updated', None, []
        return jobs.with_git(apply, 'metadata')[1]

    def test_feature_detached_ahead_and_diverged_refuse_both_callers(self):
        for kind in ['jobs', 'studio']:
            for mode in ['feature', 'detached', 'ahead', 'diverged', 'worktree']:
                with self.subTest(kind=kind, mode=mode):
                    # Each case owns a fresh repo, avoiding resets even in tests.
                    case = MetadataGit()
                    case.setUp()
                    try:
                        if mode in ['feature', 'worktree']:
                            if mode == 'worktree':
                                wt = case.work.parent / 'feature-worktree'
                                case.git(case.work, 'worktree', 'add', '-qb', 'feature', str(wt))
                                studio.ROOT = wt
                                case.work = wt
                            else:
                                case.git(case.work, 'checkout', '-qb', 'feature')
                        elif mode == 'detached':
                            case.git(case.work, 'checkout', '-q', '--detach')
                        bad = case.unrelated()
                        if mode == 'diverged':
                            case.advance_remote()
                        remote = case.remote_head()
                        before = case.git(case.work, 'status', '--porcelain')
                        self.assertIsNotNone(case.run_metadata(kind))
                        self.assertEqual(case.remote_head(), remote)
                        self.assertEqual(case.git(case.work, 'rev-parse', 'HEAD'), bad)
                        self.assertEqual(case.git(case.work, 'status', '--porcelain'), before)
                        self.assertNotIn('implementation.py', case.git(case.remote, 'ls-tree', '-r', '--name-only', 'main'))
                    finally:
                        case.doCleanups()

    def advance_remote(self):
        other = self.work.parent / 'other'
        subprocess.run(['git', 'clone', '-q', '-b', 'main', str(self.remote), str(other)], check=True)
        self.git(other, 'config', 'user.email', 'other@example.invalid')
        self.git(other, 'config', 'user.name', 'Other')
        (other / 'concurrent.txt').write_text('concurrent update\n')
        queue = other / 'jobs' / 'queue.json'
        data = json.loads(queue.read_text())
        data['concurrent_marker'] = 'other agent'
        queue.write_text(json.dumps(data) + '\n')
        self.git(other, 'add', '.')
        self.git(other, 'commit', '-qm', 'concurrent')
        self.git(other, 'push', '-q', 'origin', 'main')

    def test_clean_main_and_behind_main_preserve_remote_updates(self):
        for kind in ['studio', 'jobs']:
            with self.subTest(kind=kind):
                if kind == 'jobs':
                    self.advance_remote()
                self.assertIsNone(self.run_metadata(kind))
                self.assertEqual(self.remote_head(), self.git(self.work, 'rev-parse', 'HEAD'))
                self.assertEqual(self.git(self.work, 'status', '--porcelain'), '')
        self.assertTrue((self.work / 'concurrent.txt').exists())
        self.assertEqual(json.loads(self.path.read_text())['next'], 'intended update')
        self.assertEqual(json.loads(self.queue.read_text())['next_id'], 2)
        self.assertEqual(json.loads(self.queue.read_text())['concurrent_marker'], 'other agent')

    def test_dirty_index_and_worktree_preserved(self):
        for staged in [False, True]:
            (self.work / 'private.txt').write_text('local work')
            if staged:
                self.git(self.work, 'add', 'private.txt')
            before = self.git(self.work, 'status', '--porcelain')
            for kind in ['jobs', 'studio']:
                self.assertIsNotNone(self.run_metadata(kind))
                self.assertEqual(self.remote_head(), self.base)
                self.assertEqual(self.git(self.work, 'status', '--porcelain'), before)

    def test_push_race_reapplies_on_new_main_keeping_both_updates(self):
        # 5 Nov 2026: a lost race used to leave main diverged and refuse every later write until reconciled by hand.
        original = studio.git
        raced = False
        def race(*args):
            nonlocal raced
            if args[0] == 'push' and not raced:
                raced = True
                self.advance_remote()
            return original(*args)
        with patch.object(studio, 'git', side_effect=race):
            self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.git(self.work, 'rev-parse', 'HEAD'), self.remote_head())
        data = json.loads(self.queue.read_text())
        self.assertEqual((data['next_id'], data['concurrent_marker']), (2, 'other agent'))
        self.assertEqual(self.git(self.work, 'rev-list', '--count', 'HEAD'),
                         str(int(self.git(self.work, 'rev-list', '--count', self.base)) + 2))  # theirs + ours, once

    def test_push_that_keeps_losing_fails_closed_and_preserves_the_commit(self):
        original = studio.git
        def reject(*args):
            if args[0] == 'push':
                return subprocess.CompletedProcess(args, 1, '', 'rejected')
            return original(*args)
        with patch.object(studio, 'git', side_effect=reject):
            self.assertIn('push rejected', self.run_metadata('jobs'))
        self.assertEqual(self.remote_head(), self.base)
        local = self.git(self.work, 'rev-parse', 'HEAD')
        self.assertNotEqual(local, self.base)
        self.assertIn('unpublished/diverged', self.run_metadata('jobs'))
        self.assertEqual(self.git(self.work, 'rev-parse', 'HEAD'), local)

if __name__ == '__main__':
    unittest.main()
