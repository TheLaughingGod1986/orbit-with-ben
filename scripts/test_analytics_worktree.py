#!/usr/bin/env python3
"""Real local Git remotes; no production records or network access."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from analytics_worktree import Records, RecordError


class RecordWorktrees(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # Neutral identifiers only; do not copy machine account configuration.
        self.env = patch.dict(os.environ, {
            'GIT_AUTHOR_NAME': 'Studio tests', 'GIT_COMMITTER_NAME': 'Studio tests',
            'GIT_AUTHOR_EMAIL': 'studio-test', 'GIT_COMMITTER_EMAIL': 'studio-test',
            'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1',
        })
        self.env.start()
        self.addCleanup(self.env.stop)
        self.remote = self.root / 'remote.git'
        self.git(self.root, 'init', '--bare', str(self.remote))
        self.source = self.root / 'source'
        self.git(self.root, 'clone', str(self.remote), str(self.source))
        self.git(self.source, 'checkout', '-b', 'main')
        for name in ('05_Analytics/owb/snapshots/base.json', '05_Analytics/hos/snapshots/base.json',
                     '05_Analytics/ww2/snapshots/base.json', '05_Analytics/dashboard/index.html', 'code.py'):
            self.write(self.source, name, 'base\n')
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-m', 'seed')
        self.git(self.source, 'push', 'origin', 'main')
        self.records = Records(self.source, self.root / 'records', 'owb')
        self.records.prepare()

    def git(self, repo, *args):
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def write(self, repo, name, content):
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def remote_text(self, name):
        return self.git(self.remote, 'show', f'main:{name}')

    def test_channel_records_publish_without_shared_checkout_edits(self):
        self.write(self.source, 'code.py', 'someone else is editing\n')
        self.write(self.records.worktree, '05_Analytics/owb/snapshots/today.json', 'today\n')
        self.records.publish('today')
        self.assertEqual(self.remote_text('05_Analytics/owb/snapshots/today.json'), 'today')
        self.assertEqual(self.remote_text('code.py'), 'base')
        self.assertEqual((self.source / 'code.py').read_text(), 'someone else is editing\n')

    def test_failed_push_is_retried_on_next_run_even_without_new_changes(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        self.write(self.records.worktree, '05_Analytics/owb/REPORT.md', 'retained\n')
        with self.assertRaisesRegex(RecordError, 'push failed'):
            self.records.publish('today', attempts=1)
        pending = self.git(self.records.worktree, 'rev-parse', 'HEAD')
        self.assertEqual(self.git(self.records.worktree, 'status', '--porcelain'), '')
        hook.unlink()
        self.records.prepare()
        self.records.publish('retry')
        self.assertEqual(self.git(self.remote, 'rev-parse', 'main'), pending)
        self.assertEqual(self.remote_text('05_Analytics/owb/REPORT.md'), 'retained')

    def test_rebase_conflict_preserves_local_commit_and_remote(self):
        self.write(self.records.worktree, '05_Analytics/owb/snapshots/base.json', 'local\n')
        self.records.save('local')
        local = self.git(self.records.worktree, 'rev-parse', 'HEAD')
        self.write(self.source, '05_Analytics/owb/snapshots/base.json', 'remote\n')
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-m', 'remote')
        self.git(self.source, 'push', 'origin', 'main')
        with self.assertRaisesRegex(RecordError, 'conflicted'):
            self.records.publish('retry')
        self.assertEqual(self.git(self.records.worktree, 'rev-parse', 'HEAD'), local)
        self.assertEqual(self.remote_text('05_Analytics/owb/snapshots/base.json'), 'remote')
        self.records.verify()  # no abandoned rebase state

    def test_other_channel_or_code_changes_refuse_before_staging(self):
        for name in ('05_Analytics/hos/REPORT.md', 'code.py'):
            with self.subTest(name=name):
                self.write(self.records.worktree, name, 'foreign\n')
                with self.assertRaisesRegex(RecordError, 'Unrelated changes'):
                    self.records.publish('must refuse')
                self.assertEqual(self.git(self.records.worktree, 'diff', '--cached', '--name-only'), '')
                if name == 'code.py':
                    self.git(self.records.worktree, 'restore', name)
                else:
                    (self.records.worktree / name).unlink()

    def test_foreign_pending_commit_is_not_pushed(self):
        self.write(self.records.worktree, 'code.py', 'foreign\n')
        self.git(self.records.worktree, 'add', '.')
        self.git(self.records.worktree, 'commit', '-m', 'foreign')
        with self.assertRaisesRegex(RecordError, 'Unrelated pending commit'):
            self.records.prepare()
        self.assertEqual(self.remote_text('code.py'), 'base')

    def test_foreign_add_then_delete_history_cannot_hide_in_net_diff(self):
        name = 'foreign.txt'
        self.write(self.records.worktree, name, 'foreign\n')
        self.git(self.records.worktree, 'add', name)
        self.git(self.records.worktree, 'commit', '-m', 'foreign add')
        self.git(self.records.worktree, 'rm', name)
        self.git(self.records.worktree, 'commit', '-m', 'foreign remove')
        self.assertEqual(self.git(self.records.worktree, 'diff', 'origin/main', '--name-only'), '')
        with self.assertRaisesRegex(RecordError, 'Unrelated pending commit'):
            self.records.publish('must refuse')

    def test_staged_foreign_rename_is_refused(self):
        self.git(self.records.worktree, 'mv', 'code.py', '05_Analytics/owb/moved.py')
        with self.assertRaisesRegex(RecordError, 'Unrelated changes'):
            self.records.publish('must refuse')
        self.assertEqual(self.remote_text('code.py'), 'base')

    def test_dirty_records_survive_prepare(self):
        self.write(self.records.worktree, '05_Analytics/owb/REPORT.md', 'recovered\n')
        self.records.prepare()
        self.assertEqual(self.git(self.records.worktree, 'status', '--porcelain'), '')
        self.records.publish('later')
        self.assertEqual(self.remote_text('05_Analytics/owb/REPORT.md'), 'recovered')

    def test_cannot_reuse_shared_checkout_or_another_repository(self):
        with self.assertRaises(RecordError):
            Records(self.source, self.source, 'owb')
        other = self.root / 'other'
        self.git(self.root, 'clone', '--branch', 'main', str(self.remote), str(other))
        self.git(other, 'checkout', '--detach')
        with self.assertRaisesRegex(RecordError, 'another repository'):
            Records(self.source, other, 'owb').prepare()

    def test_each_owner_has_only_its_own_scope(self):
        for owner in ('hos', 'ww2', 'studio'):
            with self.subTest(owner=owner):
                records = Records(self.source, self.root / owner, owner)
                records.prepare()
                name = '05_Analytics/dashboard/index.html' if owner == 'studio' else f'05_Analytics/{owner}/REPORT.md'
                self.write(records.worktree, name, owner)
                records.publish(owner)
                self.assertEqual(self.remote_text(name), owner)
                self.assertFalse(records.allowed('05_Analytics/owb/REPORT.md'))

    def test_retired_engine_refuses_before_worktree_creation_or_publish(self):
        records = Records(self.source, self.root / 'never-created', 'hos')
        with patch('analytics_worktree.refusal', return_value='retired'):
            with self.assertRaisesRegex(RecordError, 'retired'):
                records.prepare()
            with self.assertRaisesRegex(RecordError, 'retired'):
                self.records.publish('must refuse')
        self.assertFalse(records.worktree.exists())

    def test_unrelated_upstream_changes_are_preserved(self):
        self.write(self.source, 'code.py', 'upstream code\n')
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-m', 'upstream')
        self.git(self.source, 'push', 'origin', 'main')
        self.write(self.records.worktree, '05_Analytics/owb/REPORT.md', 'new report\n')
        self.records.publish('report')
        self.assertEqual(self.remote_text('code.py'), 'upstream code')
        self.assertEqual(self.remote_text('05_Analytics/owb/REPORT.md'), 'new report')

    def test_symlink_scope_is_refused(self):
        (self.records.worktree / '05_Analytics/owb').rename(self.root / 'saved')
        (self.records.worktree / '05_Analytics/owb').symlink_to(self.root / 'saved', target_is_directory=True)
        with self.assertRaisesRegex(RecordError, 'symlink'):
            self.records.save('must refuse')


if __name__ == '__main__':
    unittest.main()
