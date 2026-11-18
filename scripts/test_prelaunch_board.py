"""J3007: embedded channels participate in reviews before a YouTube connection exists."""
import datetime as dt
import json
import tempfile
from pathlib import Path
import unittest
from unittest import mock
import channels
import channel_cards
import channel_films
import kanban_snapshot as ks
import board_publish as bp
import approved_deliver as ad
import video_tracker as vt
import test_board_benauth as auth


class Prelaunch(unittest.TestCase):
    def setUp(self):
        # Exercise the supported embedded/prelaunch layout independently of the live channel's move.
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        channel = dict(channels.get('ww2'), local='channels/ww2', launch_state='prelaunch',
                       youtube={'handle': '@FieldOrderHistory'},
                       repo={'url': '', 'env': 'WW2_REPO', 'checkouts': ['ww2']})
        base = tuple(channel if c['slug'] == 'ww2' else c for c in channels._load())
        self.enterContext(mock.patch.object(channels, 'ROOT', root))
        original_load = channels._load
        self.enterContext(mock.patch.object(channels, '_load',
            side_effect=lambda *args: original_load(*args) if args else base))
        folder = root / 'channels/ww2'
        (folder / 'studio').mkdir(parents=True)
        (folder / 'studio/channel.json').write_text(json.dumps(channel))
        for number in range(1, 11):
            film = folder / '02_Video-Projects' / f'{number:03d}_Fixture'
            film.mkdir(parents=True)
            (film / 'status.json').write_text(json.dumps({
                'film': f'{number:03d}', 'title': f'Fixture {number}',
                'stages': {'topic': {'state': 'done'}}, 'claims': []}))

    def test_embedded_channel_has_real_films_and_no_remote_repository(self):
        root = channels.ROOT / 'channels/ww2'
        self.assertEqual(channels.checkout('ww2'), root)
        self.assertEqual(channels.of_path(root / '02_Video-Projects'), 'ww2')
        self.assertEqual(channels.get('ww2')['repo']['url'], '')
        self.assertEqual(len(channel_films.films('ww2')), 10)
        doc = ks.read_documents({'ww2': root})['ww2']
        board = vt.build_from_docs({'ww2': {'films': doc}})
        films = [v for v in board['videos'] if v['channel'] == 'WW2']
        self.assertEqual(len(films), 10)
        self.assertTrue(any(v['key'] == 'WW2:001' for v in films))
        card = next(c for c in channel_cards.cards() if c['slug'] == 'ww2')
        self.assertEqual(card['status'], 'Getting ready: YouTube not connected yet')
        self.assertTrue(card['prelaunch'])
        self.assertFalse(card['repo'])

    def test_local_channel_cannot_escape_the_studio(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'channels'
            base.mkdir()
            for local in ('../outside', '/outside'):
                (base / 'channels.json').write_text(json.dumps({'channels': [{'slug': 'bad', 'local': local}]}))
                with self.assertRaisesRegex(ValueError, 'inside the studio'):
                    channels._load(str(base))

    def test_publisher_uses_embedded_folder_in_fresh_studio_copy(self):
        self.assertEqual(bp.wt('ww2'), bp.wt() / 'channels/ww2')
        calls = []
        with mock.patch.object(bp, 'worktree', side_effect=lambda *a: calls.append(a)), mock.patch.object(bp.subprocess, 'run'), mock.patch.object(bp.pathlib.Path, 'mkdir'):
            bp.build(Path('/tmp/nonexistent-j3007-docs'))
        self.assertNotIn(channels.repo_path('ww2'), [c[0] for c in calls])
        self.assertIn(str(bp.wt('ww2')), bp.snapshot_command(Path('/tmp/out')))

    def test_approved_cut_waits_before_listing_or_delivery(self):
        film = {'key': 'WW2:001', 'channel': 'WW2', 'number': '001', 'lane': 'approved', 'type': 'long'}
        with mock.patch.object(ad.lp, 'for_video', side_effect=AssertionError('must not plan delivery')):
            actions = ad.plan_actions([film], [], now=dt.datetime.now(dt.timezone.utc))
        self.assertEqual(actions, [{'op': 'wait', 'key': 'WW2:001', 'reason': 'Approved; waiting for YouTube connection'}])

    def test_authenticated_tick_round_trip_reaches_mini_tracker(self):
        runner = auth.OpenTapsNode()
        doc = {'film': 'WW2:001', 'version': 'v01', 'verdict': 'ok', 'at': '2026-11-18T06:00:00Z'}
        result = runner.run_handler({'id': 'WW2-001', 'doc': doc}, {'cookie': 'studio_ben=' + runner.node_session()})
        self.assertEqual(result['status'], 200)
        self.assertTrue(result['posted'][0].startswith('[Ben] OK WW2 001 v01'))
        stored = json.loads(result['patched'][0].split('```json\n')[1].split('\n```')[0])['checks']
        film = json.loads(next((channels.checkout('ww2') / '02_Video-Projects').glob('001*/status.json')).read_text())
        ask = {'id': 'J3999', 'job': 'J3999', 'channel': 'WW2', 'card': 'WW2:001', 'version': 'v01', 'watch': {'url': 'https://board.example/api/watch?test=1'}}
        board = vt.build_from_docs({'ww2': {'films': [film]}, 'briefs': {'asks': [ask]}}, checks=stored)
        card = next(v for v in board['videos'] if v['key'] == 'WW2:001')
        self.assertEqual(card['lane'], 'approved')
        self.assertEqual(card['waitingOn'], 'YouTube connection')
        actions = ad.plan_actions([card], [])
        self.assertEqual(actions[0]['op'], 'wait')
        denied = runner.run_handler({'id': 'WW2-001', 'doc': doc})
        self.assertEqual(denied['status'], 401)
        change = dict(doc, verdict='change', fixes=[{'text': 'Fix the map'}])
        changed = runner.run_handler({'id': 'WW2-001', 'doc': change}, {'cookie': 'studio_ben=' + runner.node_session()})
        self.assertIn('[Ben] changes WW2 001', changed['posted'][0])
