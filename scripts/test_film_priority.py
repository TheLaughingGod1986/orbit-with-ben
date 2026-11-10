"""J2039: production links and deadline-first near-watch dispatch."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import jobs
import workflow_state as w
from workflow_board import load_tracker

AT = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)


def video(key, count, lane='progress', kind='long'):
    return {'key': key, 'type': kind, 'lane': lane,
            'production': {'milestones': [{'state': 'done'}] * count + [{'state': 'review'}]}}


def job(key, **extra):
    return {'id': key, 'status': 'open', 'needs': 'mini', 'title': 'work', **extra}


class FilmLinks(unittest.TestCase):
    def add(self, **kw):
        return jobs.do_add({'jobs': [], 'next_id': 1}, needs='mini', body='',
                           by='codex', at=AT, **kw)

    def test_named_film_requires_both_links(self):
        for title in ('123 edit', 'HOS 006 voice', 'Repair OWB:030', 'check hos 007'):
            with self.subTest(title=title), self.assertRaisesRegex(ValueError, '--film'):
                self.add(title=title)
        self.assertEqual(self.add(title='123 edit', film='123', stage='edit')['film'], '123')

    def test_production_kind_with_film_in_body_requires_links(self):
        for kind in ('script', 'facts', 'vo', 'image', 'chart', 'thumb', 'video', 'assembly', 'qa'):
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, '--film'):
                jobs.do_add({'jobs': [], 'next_id': 1}, title='Prepare delivery', needs='mini',
                            body='Use 02_Video-Projects/006_Gravity', by='claude', at=AT, kind=kind)

    def test_infrastructure_and_generated_backlog_are_exempt(self):
        self.add(title='Fix queue ordering', kind='assembly')
        for by in ('relay', 'refill', 'backlog'):
            jobs.do_add({'jobs': [], 'next_id': 1}, title='HOS 006 QA', needs='mini', body='', by=by, at=AT, kind='qa')
        self.add(title='Backlog: HOS 006 ideas', kind='script')

    def test_rejection_is_atomic_and_pair_validation_still_applies(self):
        data = {'jobs': [], 'next_id': 1}
        with self.assertRaises(ValueError):
            jobs.do_add(data, title='006 QA', needs='mini', body='', by='claude', at=AT)
        self.assertEqual(data, {'jobs': [], 'next_id': 1})
        with self.assertRaises(ValueError):
            self.add(title='tool', film='006')


class Priority(unittest.TestCase):
    def setUp(self):
        self.tracker = {'videos': [video('OWB:030', 8), video('HOS:008', 7), video('OWB:031', 6),
                                   video('HOS:030', 5), video('OWB:032', 9, 'ready'),
                                   video('OWB:033', 9, 'approved'), video('OWB:034', 9, 'done'),
                                   video('OWB:035:S:A', 9, kind='short')]}

    def test_top_three_only_and_uat_excluded(self):
        self.assertEqual(w.near_watch(self.tracker), ('OWB:030', 'HOS:008', 'OWB:031'))
        self.assertEqual(w.near_watch({}), ())
        for malformed in ([], {'videos': None}, {'videos': [video('OWB:036', 1) | {'production': 'bad'}]}):
            self.assertEqual(w.near_watch(malformed), ())

    def test_priority_over_urgent_focus_and_admin_but_not_deadlines(self):
        near = job('near', film='008', repo='hos')
        other = job('other', film='030', repo='hos', urgent=1)
        data = {'jobs': [other, near], 'focus': ['030'], 'tracker': self.tracker}
        choose = lambda j, workers: 'codex'
        self.assertEqual(w.select_dispatch(data, AT, 'chief', {'codex'}, choose)['job']['id'], 'near')
        other['due'] = '2026-11-05T00:00Z'
        self.assertEqual(w.select_dispatch(data, AT, 'chief', {'codex'}, choose)['job']['id'], 'other')
        near['after'] = 'missing'
        self.assertFalse(w.claimable(near, data['jobs'], AT, 'codex', 'chief'))

    def test_shared_job_and_inherited_deadline(self):
        near = job('near', taskKeys=['OWB:030'])
        prerequisite = job('before')
        downstream = job('after', after='before', due='2026-11-05T00:00Z')
        data = {'jobs': [near, prerequisite, downstream], 'tracker': self.tracker}
        self.assertEqual(w.select_dispatch(data, AT, 'chief', {'codex'}, lambda j, ws: 'codex')['job']['id'], 'before')

    def test_jobs_next_uses_same_board_and_does_not_persist_tracker(self):
        data = {'jobs': [job('first'), job('near', film='008', repo='hos')]}
        with patch('workflow_board.load_tracker', return_value=self.tracker):
            self.assertEqual(jobs.ordered(data, AT)[0]['id'], 'near')
        self.assertNotIn('tracker', data)

    def test_missing_or_invalid_board_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'board.json'
            self.assertEqual(load_tracker(path), {})
            for content in ('broken', '[]', '{"tracker":{"videos":null}}'):
                path.write_text(content)
                self.assertEqual(load_tracker(path), {})
            path.write_text(json.dumps({'tracker': self.tracker}))
            self.assertEqual(load_tracker(path), self.tracker)


class OldestFilmFirst(unittest.TestCase):
    """Ben, 8 Nov 2026 (option B): keep the WIP limit, but finish the oldest film's work before a newer one."""
    TRACKER = {'videos': [
        {'key': 'OWB:032', 'type': 'long', 'lane': 'progress', 'air': '2026-11-25'},
        {'key': 'OWB:034', 'type': 'long', 'lane': 'progress', 'air': '2026-12-13'},
        {'key': 'HOS:009', 'type': 'long', 'lane': 'progress', 'air': '2026-11-26'},
        {'key': 'OWB:024', 'type': 'long', 'lane': 'done', 'air': '2026-11-01'},
    ]}

    def test_air_dates_skip_finished_films(self):
        air = w.air_dates(self.TRACKER)
        self.assertEqual(set(air), {'OWB:032', 'OWB:034', 'HOS:009'})

    def test_the_film_that_airs_first_wins_even_when_its_job_is_newer(self):
        air = w.air_dates(self.TRACKER)
        older_film = job('J2', film='032', repo='owb', stage='edit', created_at='2026-11-08T10:00:00Z')
        newer_film = job('J1', film='034', repo='owb', stage='edit', created_at='2026-11-01T10:00:00Z')
        hos = job('J3', film='009', repo='hos', stage='edit', created_at='2026-11-01T10:00:00Z')
        ranked = sorted([newer_film, hos, older_film], key=lambda j: w.order(j, {}, (), AT, (), air))
        self.assertEqual([j['id'] for j in ranked], ['J2', 'J3', 'J1'])

    def test_a_deadline_still_beats_air_order_and_backlog_does_not_jump_the_line(self):
        air = w.air_dates(self.TRACKER)
        newer = job('J1', film='034', repo='owb', stage='edit')
        due = {'J1': dt.datetime(2026, 11, 5, tzinfo=dt.timezone.utc)}
        older = job('J2', film='032', repo='owb', stage='edit')
        self.assertEqual(min([older, newer], key=lambda j: w.order(j, due, (), AT, (), air))['id'], 'J1')
        backlog = job('J3', film='032', repo='owb', title='Backlog OWB: next Short', backlog='owb-shorts')
        self.assertEqual(min([backlog, newer], key=lambda j: w.order(j, {}, (), AT, (), air))['id'], 'J1')
