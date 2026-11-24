"""J3506: a board OK becomes durable delivery work, with visible overdue approvals."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import approved_deliver as ad
import chief_relay as cr
import video_tracker as vt
import jobs as J

NOW = dt.datetime(2026, 11, 24, 12, tzinfo=dt.timezone.utc)


def card(age=12, **over):
    at = (NOW - dt.timedelta(hours=age)).isoformat()
    return {"key": "OWB:ASK:J3400", "checkId": "OWB-J3400", "channel": "OWB", "number": "032",
            "type": "long", "title": "Titan", "lane": "approved", "version": "v03",
            "check": {"verdict": "ok", "at": at, "version": "v03", "handled": False},
            "approved": {"job": "J3400", "askJob": "J3400", "version": "v03", "state": "waiting", "okAt": at},
            "ask": {"job": "J3400", "file": "Titan_v03.mp4"}, **over}


def review():
    j = {"id": "J3400", "status": "done", "title": "Review Titan", "kind": "review", "repo": "owb", "history": []}
    J.do_awaits(j, "chief", NOW, what="Watch Titan", file="Titan_v03.mp4", version="v03",
                number="032", vtype="long")
    return j


class BoardOK(unittest.TestCase):
    def test_original_review_is_not_an_upload_and_threshold_is_exact(self):
        self.assertEqual(ad.delivery_jobs_for(card(), [review()]), [])
        self.assertFalse(ad.approval_alerts([card(11.99)], [review()], now=NOW))
        alert = ad.approval_alerts([card()], [review()], now=NOW)[0]
        self.assertEqual(alert['message'], 'Your OK on Titan is waiting for an upload job, 12 h')
        self.assertEqual(alert['href'], '#videos')
        unknown = card(check={}, approved={})
        self.assertIsNone(ad.waiting_approvals([unknown], [], now=NOW)[0]['ageHours'])
        self.assertFalse(ad.approval_alerts([unknown], [], now=NOW))

    def test_queue_receipt_is_durable_and_idempotent(self):
        v = card()
        data = {"next_id": 3507, "jobs": [review()]}
        listing = {"complete": True, "destination": "youtube", "title": "Titan"}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value=listing):
            actions = ad.plan_actions([v], data['jobs'], now=NOW, root=Path(d))
            self.assertEqual(actions[0]['op'], 'create')
            touched = ad.apply_actions(data, actions, agent='relay', at=NOW)
            upload = data['jobs'][-1]
            self.assertEqual(touched, [upload['id']])
            self.assertEqual(upload['needs'], 'mini')
            self.assertIn('Titan_v03.mp4', upload['body'])
            self.assertEqual(upload['approved_from']['okAt'], v['check']['at'])
            self.assertNotIn('awaits_ben', data['jobs'][0])
            again = ad.plan_actions([v], data['jobs'], now=NOW, root=Path(d))
            self.assertEqual(again[0]['op'], 'skip')
            self.assertFalse(ad.approval_alerts([v], data['jobs'], now=NOW))
            ticks = {v['checkId']: v['check']}
            self.assertTrue(vt.handled_checks(ticks, data['jobs'])[v['checkId']]['handled'])
            self.assertFalse(ticks[v['checkId']]['handled'])  # caller's raw tap preserved
            for replacement in ({'verdict': 'change'}, {'version': 'v04'}, {'at': NOW.isoformat()}):
                newer = {v['checkId']: {**v['check'], **replacement}}
                self.assertFalse(vt.handled_checks(newer, data['jobs'])[v['checkId']]['handled'])
            upload['status'] = 'cancelled'
            self.assertFalse(vt.handled_checks(ticks, data['jobs'])[v['checkId']]['handled'])

    def test_channel_and_short_identity_do_not_hide_missing_uploads(self):
        foreign = {'id': 'J9', 'status': 'open', 'repo': 'hos', 'title': 'Upload 032 v03', 'kind': 'studio'}
        self.assertFalse(ad.delivery_jobs_for(card(), [foreign]))
        short = card(type='short')
        sibling = {'id': 'J8', 'status': 'open', 'repo': 'owb', 'title': 'Upload 032 short v03',
                   'approved_from': {'card': 'OWB:ASK:Jother', 'number': '032', 'version': 'v03', 'channel': 'OWB', 'type': 'short'}}
        self.assertFalse(ad.delivery_jobs_for(short, [sibling]))

    def test_incomplete_listing_and_uploaded_cards_never_queue(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value={'complete': False}):
            self.assertEqual(ad.plan_actions([card()], [review()], now=NOW, root=Path(d))[0]['op'], 'wait')
        for youtube in ({'state': 'live', 'privacy': 'public'}, {'state': 'scheduled', 'publishAt': NOW.isoformat()}):
            self.assertFalse(ad.waiting_approvals([card(youtube=youtube)], [], now=NOW))

    def test_existing_upload_is_acknowledged_without_creating_a_second_job(self):
        v = card()
        upload = {'id': 'J3507', 'kind': 'studio', 'repo': 'owb', 'status': 'open',
                  'title': 'Upload OWB 032 v03', 'history': []}
        data = {'next_id': 3508, 'jobs': [review(), upload]}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value={'complete': True}):
            actions = ad.plan_actions([v], data['jobs'], now=NOW, root=Path(d))
            self.assertEqual(actions[0]['op'], 'acknowledge')
            ad.apply_actions(data, actions, agent='relay', at=NOW)
            self.assertEqual(len(data['jobs']), 2)
            self.assertEqual(upload['board_ok']['id'], v['checkId'])
            self.assertNotIn('awaits_ben', data['jobs'][0])

    def test_board_alert_payload_and_swap_guard(self):
        import ben_alerts
        with tempfile.TemporaryDirectory() as d:
            result = ben_alerts.evaluate(at=NOW, jobs=[], checks={}, videos=[card()], uploads={},
                                         state_file=Path(d)/'state.json', config_file=Path(d)/'config.json', deliver=False)
            self.assertEqual(result['board']['active'][0]['kind'], 'approval')
        self.assertTrue(ad.is_swap({'title': 'Swap Titan to v04'}))
        self.assertFalse(ad.is_swap({'title': 'Upload Titan', 'body': 'Do not swap a file onto an existing id.'}))

    def test_relay_inbox_contains_approvals_without_queue_duties(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'jobs').mkdir()
            (root/'jobs/queue.json').write_text(json.dumps({'jobs': [review()]}))
            board = root/'_desk/state/board/board.json'
            board.parent.mkdir(parents=True)
            board.write_text(json.dumps({'tracker': {'videos': [card(48)]}}))
            dest = root/'inbox.json'
            with mock.patch.object(cr, 'HOME', root), mock.patch.object(cr, 'STUDIO', root), mock.patch.object(cr, 'notify', return_value=True) as notify:
                cr.publish_chief_inbox([], 'chief', NOW, dest=dest)
                self.assertIn('48 h', notify.call_args[0][0])
                self.assertEqual(json.loads(dest.read_text())['approvals'][0]['key'], card()['key'])
                with mock.patch.object(ad, 'run', return_value={'touched': ['J3507']}) as run:
                    cr.approval_round(NOW, apply=True)
                    self.assertTrue(run.call_args.kwargs['git'])
                    self.assertEqual(run.call_args.kwargs['videos'][0]['key'], card()['key'])


if __name__ == '__main__':
    unittest.main()
