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

class SpendRowsFromAPictureRun(unittest.TestCase):
    """11 Nov 2026. A picture run appends its spend rows to the tracked ledger in the shared checkout as it works.
    Those unsaved rows made every queue write on the Mini refuse for as long as a batch ran. A queue write now saves
    them first, and never leaves the file missing or half written, because the run reads it while it works."""

    LEDGER = '05_Analytics/ai_spend/ledger.jsonl'

    def setUp(self):
        self.case = MetadataGit()                     # its repositories and helpers, without its tests
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        for name in ('work', 'remote', 'git', 'remote_head', 'run_metadata'):
            setattr(self, name, getattr(self.case, name))
        self.ledger = self.work / self.LEDGER
        self.ledger.parent.mkdir(parents=True)
        self.ledger.write_text(self.row('flow:read:a', 100) + self.row('flow:spend:a', 100))
        self.git(self.work, 'add', '.')
        self.git(self.work, 'commit', '-qm', 'ledger')
        self.git(self.work, 'push', '-q', 'origin', 'main')

    @staticmethod
    def row(ident, n):
        return json.dumps({'id': ident, 'kind': 'spend', 'pool': 'flow', 'amount': n}) + '\n'

    def run_append(self, *rows):
        with self.ledger.open('a') as handle:
            handle.write(''.join(rows))

    def other_machine_appends(self, *rows):
        other = self.work.parent / 'other'
        subprocess.run(['git', 'clone', '-q', '-b', 'main', str(self.remote), str(other)], check=True)
        self.git(other, 'config', 'user.email', 'other@example.invalid')
        self.git(other, 'config', 'user.name', 'Other')
        with (other / self.LEDGER).open('a') as handle:
            handle.write(''.join(rows))
        self.git(other, 'commit', '-qam', 'ai_spend: a reading from another machine')
        self.git(other, 'push', '-q', 'origin', 'HEAD:main')

    def remote_ledger(self):
        return self.git(self.remote, 'show', 'main:' + self.LEDGER).splitlines()

    def ids(self, lines):
        return [json.loads(line)['id'] for line in lines]

    def test_unsaved_rows_are_saved_and_the_queue_write_goes_through(self):
        self.run_append(self.row('flow:read:b', 90), self.row('flow:spend:b', 100))
        self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.ids(self.remote_ledger()), ['flow:read:a', 'flow:spend:a', 'flow:read:b', 'flow:spend:b'])
        self.assertEqual(json.loads(self.git(self.remote, 'show', 'main:jobs/queue.json'))['next_id'], 2)
        self.assertEqual(self.git(self.work, 'status', '--porcelain'), '')
        subjects = self.git(self.remote, 'log', '--format=%s', '-2', 'main').splitlines()
        self.assertEqual(subjects[0], 'metadata')
        self.assertTrue(subjects[1].startswith('ai_spend: rows a picture run wrote'))
        # each commit holds only its own file
        self.assertEqual(self.git(self.remote, 'show', '--format=', '--name-only', 'main~1'), self.LEDGER)

    def test_both_sides_added_rows_none_is_lost_and_none_is_doubled(self):
        self.run_append(self.row('flow:read:b', 90), self.row('flow:spend:b', 100))
        self.other_machine_appends(self.row('codex:reading:1', 92), self.row('flow:read:b', 90))   # one row is the same receipt
        self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.ids(self.remote_ledger()),
                         ['flow:read:a', 'flow:spend:a', 'codex:reading:1', 'flow:read:b', 'flow:spend:b'])
        self.assertEqual(self.ledger.read_text().splitlines(), self.remote_ledger())
        self.assertEqual(self.git(self.work, 'status', '--porcelain'), '')

    def test_the_file_is_never_missing_or_half_written_while_it_is_settled(self):
        """The run stops on a ledger that is missing rows it wrote in a torn way; every write must be whole."""
        self.run_append(self.row('flow:read:b', 90))
        self.other_machine_appends(self.row('codex:reading:1', 92))
        seen = []
        real = studio._replace

        def watching(path, lines):
            real(path, lines)
            text = path.read_text()
            seen.append(text.endswith('\n') and all(json.loads(line) for line in text.splitlines()))
        with patch.object(studio, '_replace', watching):
            self.assertIsNone(self.run_metadata('jobs'))
        self.assertTrue(seen and all(seen))
        self.assertTrue(self.ledger.exists())
        self.assertEqual([p.name for p in self.ledger.parent.iterdir()], ['ledger.jsonl'])   # no temporary file left

    def test_a_row_the_run_adds_while_it_is_settled_is_kept(self):
        self.run_append(self.row('flow:read:b', 90))
        self.other_machine_appends(self.row('codex:reading:1', 92))
        real = studio._replace
        calls = []

        def run_writes_between(path, lines):
            real(path, lines)
            if not calls:                                # straight after the file was set to main's rows
                with path.open('a') as handle:
                    handle.write(self.row('flow:spend:c', 100))
            calls.append(1)
        with patch.object(studio, '_replace', run_writes_between):
            self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.ids(self.remote_ledger()), ['flow:read:a', 'flow:spend:a', 'codex:reading:1', 'flow:read:b', 'flow:spend:c'])

    def test_an_edited_or_cut_ledger_is_refused_and_left_alone(self):
        for text in (self.row('flow:read:a', 999) + self.row('flow:spend:a', 100), self.row('flow:read:a', 100)):
            with self.subTest(text=text[:30]):
                self.ledger.write_text(text)
                remote = self.remote_head()
                self.assertIn('settle it by hand', self.run_metadata('jobs'))
                self.assertEqual(self.remote_head(), remote)
                self.assertEqual(self.ledger.read_text(), text)

    def test_an_unfinished_last_line_or_an_unreadable_row_is_refused_and_left_alone(self):
        for tail, said in (('{"id": "flow:read:b", "le', 'unfinished'), ('not json\n', 'unreadable'), ('[1, 2]\n', 'unreadable')):
            with self.subTest(tail=tail):
                before = self.git(self.work, 'show', 'HEAD:' + self.LEDGER) + '\n'
                self.ledger.write_text(before + tail)
                remote = self.remote_head()
                self.assertIn(said, self.run_metadata('jobs'))
                self.assertEqual(self.remote_head(), remote)
                self.assertEqual(self.ledger.read_text(), before + tail)

    def test_any_other_unsaved_file_still_stops_the_write(self):
        self.run_append(self.row('flow:read:b', 90))
        (self.work / 'JOBS.md').write_text('someone was editing this\n')
        remote = self.remote_head()
        self.assertIn('clean working tree', self.run_metadata('jobs'))
        self.assertEqual(self.remote_head(), remote)
        self.assertIn('flow:read:b', self.ledger.read_text())

    def test_staged_ledger_changes_still_stop_the_write(self):
        self.run_append(self.row('flow:read:b', 90))
        self.git(self.work, 'add', self.LEDGER)
        self.assertIn('clean working tree', self.run_metadata('jobs'))

    def test_rows_already_on_main_leave_nothing_to_save(self):
        self.run_append(self.row('flow:read:b', 90))
        self.other_machine_appends(self.row('flow:read:b', 90))
        head = self.remote_head()
        self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.ids(self.remote_ledger()), ['flow:read:a', 'flow:spend:a', 'flow:read:b'])
        self.assertEqual(self.git(self.remote, 'rev-list', '--count', head + '..main'), '1')   # only the queue write

    def test_a_clean_checkout_behaves_as_before(self):
        head = self.remote_head()
        self.assertIsNone(self.run_metadata('jobs'))
        self.assertEqual(self.git(self.remote, 'rev-list', '--count', head + '..main'), '1')


if __name__ == '__main__':
    unittest.main()
