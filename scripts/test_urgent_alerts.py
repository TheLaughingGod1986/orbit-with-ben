import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from urgent_alerts import evaluate, update, deliver

NOW = dt.datetime(2026, 11, 21, 8, tzinfo=dt.timezone.utc)
SITE = 'https://board.oppti.dev'


def card(channel='OWB'):
    return {'key': channel + ':S:test', 'channel': channel, 'title': 'Muons Short',
            'youtube': {'state': 'scheduled', 'videoId': 'old', 'publishAt': (NOW + dt.timedelta(hours=4)).isoformat()}}


def board(v):
    return {'tracker': {'videos': [v]}}


class Alerts(unittest.TestCase):
    def test_pull_unschedule_replace_once_and_one_reminder_each_channel(self):
        for channel in ('OWB', 'HOS', 'FOH'):
            for change in ({'state': 'uploaded', 'publishAt': ''}, {'publishAt': (NOW + dt.timedelta(days=2)).isoformat()}, {'videoId': 'new'}):
                with self.subTest(channel=channel, change=change):
                    v, state = card(channel), {}
                    self.assertEqual(evaluate(board(v), [], state, NOW, SITE)[1], [])
                    v['youtube'].update(change)
                    banners, sent = evaluate(board(v), [], state, NOW, SITE)
                    self.assertEqual(len(sent), 1)
                    self.assertIn('London', sent[0]['message'])
                    self.assertFalse(evaluate(board(v), [], state, NOW + dt.timedelta(hours=1), SITE)[1])
                    self.assertTrue(evaluate(board(v), [], state, NOW + dt.timedelta(hours=2), SITE)[1][0]['reminder'])
                    self.assertFalse(evaluate(board(v), [], state, NOW + dt.timedelta(hours=3), SITE)[1])
                    self.assertFalse(evaluate(board(v), [], state, NOW + dt.timedelta(hours=5), SITE)[0])

    def test_watch_once_repeat_and_done_or_resolved_stops(self):
        for finished in ('done', 'resolved'):
            v, state = card(), {}
            v['ask'] = {'job': 'J1', 'version': 'v06', 'due': (NOW + dt.timedelta(hours=10)).isoformat()}
            jobs = [{'id': 'J1', 'status': 'blocked'}]
            self.assertEqual(len(evaluate(board(v), jobs, state, NOW, SITE)[1]), 1)
            # Restart retains deduplication.
            state = json.loads(json.dumps(state))
            self.assertFalse(evaluate(board(v), jobs, state, NOW + dt.timedelta(hours=4), SITE)[1])
            self.assertEqual(len(evaluate(board(v), jobs, state, NOW + dt.timedelta(hours=5), SITE)[1]), 1)
            self.assertFalse(evaluate(board(v), jobs, state, NOW + dt.timedelta(hours=6), SITE)[1])
            if finished == 'done':
                jobs[0]['status'] = 'done'
            else:
                v.pop('ask')
            self.assertEqual(evaluate(board(v), jobs, state, NOW + dt.timedelta(hours=7), SITE), ([], []))

    def test_boundaries_unknown_missing_and_normal_publication(self):
        v, state = card(), {}
        v['youtube']['publishAt'] = (NOW + dt.timedelta(hours=25)).isoformat()
        evaluate(board(v), [], state, NOW, SITE)
        v['youtube']['state'] = 'uploaded'
        self.assertFalse(evaluate(board(v), [], state, NOW, SITE)[1])
        v, state = card(), {}
        evaluate(board(v), [], state, NOW, SITE)
        self.assertFalse(evaluate({'tracker': {'videos': []}}, [], state, NOW, SITE)[1])
        v['youtube']['state'] = 'live'
        self.assertFalse(evaluate(board(v), [], state, NOW, SITE)[1])
        v['ask'] = {'job': 'J1', 'due': (NOW + dt.timedelta(hours=13)).isoformat()}
        self.assertFalse(evaluate(board(v), [{'id': 'J1', 'status': 'open'}], {}, NOW, SITE)[1])

    def test_restored_schedule_clears_and_does_not_realert_same_event(self):
        v, state = card(), {}
        original = copy.deepcopy(v)
        evaluate(board(v), [], state, NOW, SITE)
        v['youtube']['publishAt'] = ''
        evaluate(board(v), [], state, NOW, SITE)
        self.assertFalse(evaluate(board(original), [], state, NOW + dt.timedelta(hours=1), SITE)[0])
        self.assertFalse(evaluate(board(v), [], state, NOW + dt.timedelta(hours=1), SITE)[1])

    def test_dry_run_no_send_or_state_write_and_reserve_before_delivery(self):
        v = card()
        v['ask'] = {'job': 'J1', 'due': (NOW + dt.timedelta(hours=4)).isoformat()}
        jobs = [{'id': 'J1', 'status': 'open'}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'state.json'
            with patch('urgent_alerts.deliver') as send:
                update(board(v), jobs, path, NOW, SITE, Path(tmp), dry_run=True)
                self.assertFalse(path.exists())
                send.assert_not_called()
                def reserved(*args):
                    self.assertEqual(next(iter(json.loads(path.read_text())['events'].values()))['sent'], 1)
                    return {'phone': 'unconfirmed'}
                send.side_effect = reserved
                update(board(v), jobs, path, NOW, SITE, Path(tmp))
                update(board(v), jobs, path, NOW, SITE, Path(tmp))
                self.assertEqual(send.call_count, 1)

    def test_done_before_halfway_cancels_reminder(self):
        v, state = card(), {}
        v['ask'] = {'job': 'J1', 'due': (NOW + dt.timedelta(hours=4)).isoformat()}
        jobs = [{'id': 'J1', 'status': 'open'}]
        evaluate(board(v), jobs, state, NOW, SITE)
        jobs[0]['status'] = 'done'
        self.assertEqual(evaluate(board(v), jobs, state, NOW + dt.timedelta(hours=2), SITE), ([], []))

    def test_no_phone_setup_and_thread_uses_file(self):
        event = {'message': 'Muons needs your watch.', 'url': SITE + '/#review', 'reminder': False}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'jobs').mkdir()
            with patch.dict('os.environ', {}, clear=True), patch('urgent_alerts.urllib.request.urlopen') as phone:
                with patch('urgent_alerts.subprocess.run') as post:
                    post.return_value.returncode = 0
                    def check_file(argv, **kwargs):
                        self.assertEqual(argv[-2], '-f')
                        self.assertIn('Muons needs your watch.', Path(argv[-1]).read_text())
                        return type('Result', (), {'returncode': 0})()
                    post.side_effect = check_file
                    self.assertEqual(deliver(event, root)['thread'], 'posted')
                    phone.assert_not_called()
                    self.assertEqual(list((root / 'jobs').iterdir()), [])

    def test_banner_in_all_built_pages(self):
        import importlib.util
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location('build', root / '05_Analytics/kanban/board_site/build.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            mod.build_studio(out)
            mod.build_ai(out)
            mod.build_tracker(out)
            for name in ('index.html', 'ai.html', 'tracker.html'):
                self.assertIn("banner.id = 'urgent-studio-alerts'", (out / name).read_text())


if __name__ == '__main__':
    unittest.main()
