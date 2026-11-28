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
        self.assertEqual(alert['href'], '#v=OWB%3AASK%3AJ3400')  # opens that video's own page (24 Nov 2026)
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

    def test_incomplete_listing_waits_only_for_delivery_work_and_uploaded_cards_never_queue(self):
        upload = {'id': 'J3507', 'kind': 'studio', 'repo': 'owb', 'status': 'open', 'title': 'Upload OWB 032 v03',
                  'history': []}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value={'complete': False}):
            self.assertEqual(ad.plan_actions([card()], [review(), upload], now=NOW, root=Path(d))[0]['op'], 'wait')
        for youtube in ({'state': 'live', 'privacy': 'public'}, {'state': 'scheduled', 'publishAt': NOW.isoformat()}):
            self.assertFalse(ad.waiting_approvals([card(youtube=youtube)], [], now=NOW))

    def test_ok_with_no_package_queues_one_job_that_packages_then_uploads(self):
        # 26 Nov 2026: Ben OK'd the Franklin and Titan Shorts at 09:15; neither had a listing package and nothing was asked
        # to make one, so the relay waited and the board said "waiting for an upload job, 12 h" for both.
        at = (NOW - dt.timedelta(hours=1)).isoformat()
        short = card(key='HOS:ASK:J3763', checkId='HOS-J3763', channel='HOS', number='008 Short s04', type='short',
                     title='Why Did Franklin Never Patent the Lightning Rod?', version='v01',
                     check={'verdict': 'ok', 'at': at, 'version': 'v01', 'handled': False},
                     approved={'job': 'J3763', 'askJob': 'J3763', 'version': 'v01', 'okAt': at},
                     ask={'job': 'J3763', 'file': 'hos_008_s04_no_patent_v01.mp4'})
        # Its long airs Thu 26 Nov 18:00, so the Short's slot comes after that, never before.
        long = {'key': 'HOS:008', 'channel': 'HOS', 'number': '008', 'type': 'long', 'lane': 'done',
                'youtube': {'state': 'scheduled', 'videoId': 'YqCWYlv_LCY', 'publishAt': '2026-11-26T18:00:00Z'}}
        ask = {'id': 'J3763', 'status': 'blocked', 'kind': 'assembly', 'repo': 'hos', 'history': [],
               'title': 'Backlog HOS: next search-titled Short cut from a locked long'}
        J.do_awaits(ask, 'chief', NOW, what='Watch HOS 008 Short s04', file='hos_008_s04_no_patent_v01.mp4',
                    version='v01', number='008 Short s04', vtype='short', title=short['title'])
        data = {'next_id': 3820, 'jobs': [ask]}
        missing = {'complete': False, 'missing': ['title', 'thumbnail', 'description', 'tags'], 'destination': 'youtube'}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value=missing), \
                mock.patch.object(ad, 'taken_cadence_days', return_value=set()):
            actions = ad.plan_actions([short, long], data['jobs'], now=NOW, root=Path(d))
            self.assertEqual([a['op'] for a in actions], ['create'])
            a = actions[0]
            self.assertTrue(a['title'].startswith('Package and upload HOS 008 Short s04'), a['title'])
            self.assertEqual(a['airs'], '2026-11-27T11:30Z')  # Fri, the first HOS Short slot after the long
            self.assertIn('title, thumbnail, description, tags', a['body'])
            self.assertIn('Keep the title Ben OK\'d: "Why Did Franklin Never Patent the Lightning Rod?"', a['body'])
            self.assertIn('Related video is the long', a['body'])
            ad.apply_actions(data, actions, agent='relay', at=NOW)
            job = data['jobs'][-1]
            self.assertEqual((job['repo'], job['needs'], job['approved_from']['card']), ('hos', 'mini', 'HOS:ASK:J3763'))
            self.assertEqual(job['remaining_action'], 'Build the listing package, then upload to YouTube Studio as Private')
            self.assertNotIn('awaits_ben', ask)  # Ben has answered
            self.assertEqual(ad.delivery_jobs_for(short, data['jobs']), [job])
            self.assertEqual(ad.approval_alerts([short], data['jobs'], now=NOW + dt.timedelta(hours=24)), [])
            again = ad.plan_actions([short, long], data['jobs'], now=NOW, root=Path(d))
            self.assertEqual(again[0]['op'], 'wait')  # the package job is the delivery work now; no second one
            ad.apply_actions(data, again, agent='relay', at=NOW)
            self.assertEqual(len(data['jobs']), 2)
            # A long that is not on YouTube yet: the job is queued all the same and told to wait for it.
            unscheduled = dict(long, youtube=None)
            first = ad.plan_actions([short, unscheduled], [ask], now=NOW, root=Path(d))[0]
            self.assertIn("Its long (HOS:008) is not on YouTube yet", first['body'])

    def test_the_watch_job_that_built_the_upload_package_is_not_the_upload(self):
        # 27 Nov 2026: Ben OK'd FOH 004 on 26 Nov; J3430 ("edit, captions, three thumbnails and upload package, to Ben's
        # watch") was done before his OK and counted as the upload, so nothing queued one and no alert fired.
        at = (NOW - dt.timedelta(hours=26)).isoformat()
        film = card(key='WW2:004', checkId='WW2-004', channel='WW2', number='004', type='long', title='Mark 14 Torpedo',
                    version='v04', check={'verdict': 'ok', 'at': at, 'version': 'v04', 'handled': False},
                    approved={'job': 'J3430', 'askJob': 'J3430', 'version': 'v04', 'okAt': at, 'airs': '2026-12-01T17:00Z'},
                    ask={'job': 'J3430', 'file': 'ww2_004_v04.mp4'})
        watch = {'id': 'J3430', 'status': 'done', 'kind': 'assembly', 'stage': 'edit', 'film': 'WW2:004', 'repo': 'ww2',
                 'title': "WW2 film 004: edit, captions, three thumbnails and upload package, to Ben's watch",
                 'result': 'v04 in WW2 UAT; package ready', 'history': []}
        self.assertEqual(ad.delivery_jobs_for(film, [watch]), [])
        self.assertEqual(len(ad.approval_alerts([film], [watch], now=NOW)), 1)
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value={'complete': False}), \
                mock.patch.object(ad, 'taken_cadence_days', return_value=set()):
            a = ad.plan_actions([film], [watch], now=NOW, root=Path(d))[0]
        self.assertEqual((a['op'], a['airs']), ('create', '2026-12-01T17:00Z'))
        self.assertTrue(a['title'].startswith('Package and upload WW2 004 long v04'), a['title'])
        # A held ask job that will reopen to upload, or one whose result reads an upload back, still counts.
        held = dict(watch, status='blocked', title='WW2 004: upload v04 Private after Ben OKs it')
        self.assertEqual(ad.delivery_jobs_for(film, [held]), [held])
        uploaded = dict(watch, title='WW2 004: upload v04 Private', result='Uploaded Private, publishAt 2026-12-01T17:00Z, read back')
        self.assertEqual(ad.delivery_jobs_for(film, [uploaded]), [uploaded])
        # Its Short's upload and an unrelated job that mentions 004 in its brief aren't the film's upload either.
        short_upload = {'id': 'J3753', 'status': 'done', 'kind': 'studio', 'stage': 'upload', 'film': 'WW2:004', 'repo': 'ww2',
                        'title': 'WW2 004-S1: upload Ben-approved Mark 14 Torpedo depth Short v01',
                        'approved_from': {'card': 'WW2:004-S1', 'number': '004-S1', 'type': 'short', 'channel': 'WW2', 'version': 'v01'}}
        setup = {'id': 'J3254', 'status': 'done', 'kind': 'studio', 'repo': 'ww2',
                 'title': 'Field Order History: set up its upload path', 'body': 'films 004 and 005; pilot 2 v04'}
        self.assertEqual(ad.delivery_jobs_for(film, [short_upload, setup]), [])
        self.assertTrue(ad.UPLOAD_WORD_RE.search('Upload WW2 004 Private'))
        self.assertFalse(ad.UPLOAD_WORD_RE.search('three thumbnails and upload package'))

    def test_a_passed_card_already_on_youtube_is_done_not_waiting(self):
        # 27 Nov 2026: pilot 2 (live since 24 Nov) and HOS's Franklin Shorts A and C (uploaded 24 Nov, in the HOS register,
        # their times in SHORTS_RELEASE.json) sat in Passed as "Waiting for the Chief to queue the upload".
        live = {'key': 'WW2:002', 'lane': 'approved', 'type': 'long', 'approved': {'state': 'waiting'},
                'youtube': {'state': 'live', 'videoId': 'qfc6EBStOfo', 'privacy': 'public'}}
        short_a = {'key': 'HOS:ASK:J2699', 'lane': 'approved', 'type': 'short', 'approved': {'state': 'waiting'},
                   'ask': {'file': 'HOS UAT/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4'}, 'youtube': None}
        swap = {'key': 'OWB:029', 'lane': 'approved', 'type': 'long', 'approved': {'state': 'working'},
                'youtube': {'state': 'live', 'videoId': 'k2kEaA7ICjc'}}   # a job still running may be a swap: stays
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            social = root / '00_Brand/Channel-Setup/social/hos'
            social.mkdir(parents=True)
            (social / 'UPLOADS.json').write_text(json.dumps({'videos': {'__UtUYdEUwg': {
                'kind': 'short', 'file': '/Volumes/data/HOS/008/10_Shorts/hos_008_short_A_v04.mp4'}}}))
            rel = root / '02_Video-Projects/008_Lightning-Franklin/10_Shorts'
            rel.mkdir(parents=True)
            (rel / 'SHORTS_RELEASE.json').write_text(json.dumps({'shorts': [{'id': '__UtUYdEUwg', 'airDate': '2026-11-27T11:30:00Z'}]}))
            files = vt.upload_files(root)
        self.assertEqual(files['id']['__UtUYdEUwg']['publishAt'], '2026-11-27T11:30:00Z')
        videos = [live, short_a, swap]
        vt.settle_on_youtube(videos, files, NOW)
        self.assertEqual((live['lane'], live['waitingOn']), ('done', 'YouTube'))
        self.assertNotIn('approved', live)
        self.assertEqual((short_a['lane'], short_a['youtube']['videoId']), ('done', '__UtUYdEUwg'))
        self.assertEqual(swap['lane'], 'approved')

    def test_a_finished_delivery_job_never_gets_a_second_upload(self):
        done = {'id': 'J3507', 'kind': 'studio', 'repo': 'owb', 'status': 'done', 'title': 'Upload OWB 032 v03',
                'history': []}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ad.lp, 'for_video', return_value={'complete': True}):
            actions = ad.plan_actions([card()], [review(), done], now=NOW, root=Path(d))
        self.assertEqual(actions, [{'op': 'skip', 'key': 'OWB:ASK:J3400', 'job': 'J3507',
                                    'reason': 'Delivered by J3507; waiting for YouTube to read it back'}])

    def test_listing_and_booked_shorts_come_from_the_cards_own_channel(self):
        with tempfile.TemporaryDirectory() as d:
            root, hos = Path(d) / 'studio', Path(d) / 'hos'
            release = hos / '02_Video-Projects/008_Lightning-Franklin/10_Shorts/SHORTS_RELEASE.json'
            release.parent.mkdir(parents=True)
            release.write_text(json.dumps({'shorts': [{'id': '__UtUYdEUwg', 'airDate': '2026-11-27T11:30:00Z'},
                                                      {'id': '', 'airDate': '2026-11-30T11:30:00Z'}]}))
            with mock.patch.object(ad.channels, 'checkout', side_effect=lambda s: hos if s == 'hos' else None):
                self.assertEqual(ad.listing_root('owb', root), root)
                self.assertEqual(ad.listing_root('hos', root), hos)  # never Orbit's own film 008
                self.assertEqual(ad.listing_root('ww2', root), ad.NO_CHECKOUT)
                # Franklin Short A was booked only in HOS's own release file (26 Nov 2026).
                self.assertEqual(ad.taken_cadence_days([], 'HOS', 'short', NOW.date(), root=root), {'2026-11-27'})
                self.assertEqual(ad.taken_cadence_days([], 'HOS', 'long', NOW.date(), root=root), set())

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

    def test_listing_upload_finished_swap_and_listed_cards_count_as_delivery(self):
        # 24 Nov 2026: Ben saw nine "waiting for an upload job" alerts; most had one.
        uranus = card(key='OWB:OK:J2895', type='short', number='033', approved={'job': 'J2895', 'version': 'v02', 'okAt': card()['check']['at']})
        listing = {'id': 'J2895', 'status': 'blocked', 'kind': 'listing', 'repo': 'owb',
                   'title': 'Upload the Uranus Short about landing on an ice giant (v02) Private, slot Sat 19 Dec 11:30'}
        self.assertEqual(ad.waiting_approvals([uranus], [listing], now=NOW), [])
        muons = card(key='OWB:OK:J2881', type='short', approved={'job': 'J2881', 'version': 'v05', 'okAt': card()['check']['at']})
        swap = {'id': 'J2881', 'status': 'done', 'kind': 'listing', 'repo': 'owb',
                'title': 'Swap the Muons Short rvug71d7Dqk (Sat 21 Nov) to the full-screen cut Ben OK\'d, v05'}
        self.assertEqual(ad.waiting_approvals([muons], [swap], now=NOW), [])
        short_a = card(key='HOS:ASK:J2699', channel='HOS', type='short', number='008', approved={'job': 'J2699', 'version': 'v04', 'okAt': card()['check']['at']})
        review = {'id': 'J2699', 'status': 'done', 'kind': 'edit', 'repo': 'hos', 'title': 'HOS 008 Short A v04: private final-watch handoff'}
        self.assertEqual(len(ad.waiting_approvals([short_a], [review], now=NOW)), 1)  # a watch handoff is not an upload
        bundle = {'id': 'J3500', 'status': 'open', 'kind': 'studio', 'repo': 'hos', 'film': '008', 'stage': 'upload',
                  'title': 'HOS 008 Franklin: package and schedule', 'delivers': ['HOS:008', 'HOS:ASK:J2699', 'HOS:ASK:J2984']}
        self.assertEqual(ad.waiting_approvals([short_a], [review, bundle], now=NOW), [])
        self.assertEqual(ad.approval_alerts([short_a], [review], now=NOW)[0]['href'], '#v=HOS%3AASK%3AJ2699')

    def test_upload_that_names_the_asks_own_card_counts_as_delivery(self):
        # 25 Nov 2026: J3542 asked Ben about card WW2:001-S1; no such card existed, so the board keyed it WW2:ASK:J3542.
        # J3646 uploaded it (delivers ['WW2:001-S1']) and the banner still said "waiting for an upload job, 17 h".
        ask = {"what": "Watch the Mulberry Short", "file": "mulberry_short_v02.mp4", "version": "v02",
               "airs": "2026-11-26T12:00Z", "card": "WW2:001-S1", "channel": "WW2", "number": "001-S1",
               "type": "short", "id": "J3542", "job": "J3542", "jobStatus": "done", "title": "Mulberry Short"}
        short = vt.ask_card(ask)
        self.assertEqual((short["key"], short["aliases"]), ("WW2:ASK:J3542", ["WW2:001-S1"]))
        short.update(lane="approved", readyFor="", approved={"job": "J3542", "askJob": "J3542", "version": "v02",
                                                "okAt": (NOW - dt.timedelta(hours=17)).isoformat()})
        build = {"id": "J3542", "status": "done", "kind": "assembly", "repo": "ww2", "title": "One test Short"}
        self.assertEqual(len(ad.approval_alerts([short], [build], now=NOW)), 1)
        upload = {"id": "J3646", "status": "done", "kind": "studio", "stage": "upload", "repo": "ww2",
                  "title": "WW2 001-S1: upload Ben-approved Mulberry Short v02", "delivers": ["WW2:001-S1"]}
        self.assertEqual(ad.delivery_jobs_for(short, [build, upload]), [upload])
        self.assertEqual(ad.approval_alerts([short], [build, upload], now=NOW), [])
        # approved_from naming the ask's card settles that card too, rather than adding a second one.
        videos = [vt.ask_card(ask)]
        entry = {**{k: ask[k] for k in ("what", "file", "version", "airs", "card", "title", "number", "type", "channel")},
                 "askJob": "J3542", "id": "J3646", "job": "J3646", "jobStatus": "done", "okAt": "",
                 "result": "Uploaded as NoQQqrW2meM (Private, scheduled Thu 26 Nov 2026 12:00 London)"}
        vt.add_approved(videos, [entry], {}, NOW, files={})
        self.assertEqual([(v["key"], v["lane"]) for v in videos], [("WW2:ASK:J3542", "done")])

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
