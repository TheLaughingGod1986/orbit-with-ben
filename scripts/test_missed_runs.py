#!/usr/bin/env python3
"""Tests for missed_runs.py (pure logic; no git or network)."""
import datetime as dt, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import missed_runs as m
from unittest.mock import patch
import engine_guard

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 4, 12, 0, tzinfo=UTC)


def fresh():
    return {"tracker": NOW - dt.timedelta(hours=5), "buffer": NOW - dt.timedelta(hours=5),
            "claude": NOW - dt.timedelta(minutes=20), "mini": NOW - dt.timedelta(minutes=2)}


class Retirement(unittest.TestCase):
    def test_retired_monitor_refuses_before_fetch_read_or_post(self):
        with patch.object(engine_guard, 'refusal', return_value='retired'), \
                patch.object(m, 'last_seen') as seen, \
                patch.object(m.subprocess, 'run') as run:
            with self.assertRaisesRegex(SystemExit, 'retired'):
                m.main(['--post'])
            seen.assert_not_called()
            run.assert_not_called()


class Misses(unittest.TestCase):
    def test_all_fresh(self):
        self.assertEqual(m.misses(NOW, fresh()), [])

    def test_buffer_silent_two_days(self):
        s = fresh(); s["buffer"] = NOW - dt.timedelta(hours=50)
        self.assertEqual([x[0] for x in m.misses(NOW, s)], ["buffer"])

    def test_claude_down_three_days(self):
        s = fresh(); s["claude"] = NOW - dt.timedelta(days=3)
        self.assertEqual([x[0] for x in m.misses(NOW, s)], ["claude"])

    def test_claude_one_missed_hour_is_fine(self):
        s = fresh(); s["claude"] = NOW - dt.timedelta(minutes=80)
        self.assertEqual(m.misses(NOW, s), [])

    def test_no_record(self):
        s = fresh(); s["tracker"] = None
        miss = m.misses(NOW, s)
        self.assertEqual(miss[0][0], "tracker")
        self.assertIn("no record", m.line(*miss[0]))

    def test_line_has_marker_and_fix(self):
        l = m.line("buffer", 50.0, 26)
        self.assertTrue(l.startswith("[alarm buffer]"))
        self.assertIn("50.0 h", l)
        self.assertIn("dev.orbit.buffer-check", l)

    def test_dedupe(self):
        self.assertTrue(m.already_posted("buffer", NOW, ["x", "[alarm buffer] buffer missed: ..."]))
        self.assertFalse(m.already_posted("claude", NOW, ["[alarm buffer] buffer missed"]))


class TheRelaysFixLine(unittest.TestCase):
    def test_it_names_the_launchd_job_that_is_on_the_mini(self):
        # J2620, 11 Nov 2026: the label's prefix comes from the registry; the line reads as it always did.
        self.assertEqual(m.CHECKS["mini"]["fix"],
                         "the Mini relay is not beating: check com.owb.chief-relay and scripts/mini_repair.py")



class DetachedRecords(unittest.TestCase):
    def checks(self, root):
        with patch.object(m.channels, 'studio_slug', return_value=None), \
                patch.object(m.channels, 'slugs', return_value=['science', 'history']), \
                patch.object(m.channels, 'checkout', side_effect=lambda slug: root / slug):
            return m.configured_checks()

    def test_resident_preserves_existing_alarms(self):
        with patch.object(m.channels, 'studio_slug', return_value='resident'):
            self.assertEqual(m.configured_checks(), m.CHECKS)

    def test_each_channel_has_independent_alarm_and_snapshot_scope(self):
        from pathlib import Path
        checks = self.checks(Path('/scratch'))
        seen = {key: NOW for key in checks}
        seen['tracker-history'] = NOW - dt.timedelta(hours=27)
        missed = m.misses(NOW, seen, checks)
        self.assertEqual([x[0] for x in missed], ['tracker-history'])
        self.assertIn('[alarm tracker-history]', m.line(*missed[0], checks=checks))
        self.assertEqual(checks['tracker-history']['paths'], ('05_Analytics/history/snapshots',))
        self.assertEqual(checks['tracker']['paths'], ('05_Analytics/dashboard',))

    def test_missing_checkout_never_falls_back_to_engine(self):
        with patch.object(m, 'git') as git:
            self.assertIsNone(m.last_seen({'kind': 'commit', 'root': None}))
            git.assert_not_called()

    def test_failed_fetch_does_not_use_stale_remote_tracking_ref(self):
        with patch.object(m, 'git', return_value=None) as git:
            self.assertIsNone(m.last_seen({'kind': 'commit', 'grep': '^Channel tracker'}))
            self.assertEqual(git.call_count, 1)

    def test_git_timeout_and_nonzero_are_unavailable_without_diagnostics(self):
        import subprocess
        with patch.object(m.subprocess, 'run', side_effect=subprocess.TimeoutExpired('git', 30)):
            self.assertIsNone(m.git('fetch'))
        with patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, 'sensitive', 'sensitive')):
            self.assertIsNone(m.git('fetch'))

    def test_real_git_subject_and_scope_do_not_count_reports_as_snapshots(self):
        import subprocess, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.run(['git', '-C', str(root), *args], check=True,
                                      capture_output=True, text=True).stdout.strip()
            git('init', '-q')
            def commit(path, subject):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(subject)
                git('add', '.')
                git('-c', 'user.name=Test', '-c', 'user.email=test', 'commit', '-qm', subject)
                git('update-ref', 'refs/remotes/origin/main', 'HEAD')
            check = dict(self.checks(root)['tracker-science'], root=root)
            commit('05_Analytics/science/REPORT.md', 'Channel tracker: daily analytics records')
            self.assertIsNone(m.last_seen(check, fetch=False))
            commit('05_Analytics/science/snapshots/today.json', 'unrelated manual change')
            self.assertIsNone(m.last_seen(check, fetch=False))
            commit('05_Analytics/science/snapshots/today.json', 'Channel tracker: daily analytics records')
            self.assertIsNotNone(m.last_seen(check, fetch=False))
            other = dict(self.checks(root)['tracker-history'], root=root)
            self.assertIsNone(m.last_seen(other, fetch=False))
            commit('05_Analytics/history/snapshots/today.json', 'Channel tracker 2026-11-20')
            self.assertIsNotNone(m.last_seen(other, fetch=False))


if __name__ == "__main__":
    unittest.main(verbosity=1)
