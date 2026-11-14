"""Publisher/browser parity, missed updates and bounded idle transfer (J2798)."""
import copy
import json
import random
import subprocess
import unittest
from pathlib import Path
import board_publish as bp

SITE = Path(__file__).resolve().parents[1] / '05_Analytics/kanban/board_site'


def browser_apply(old, ops):
    code = 'global.window={};\n' + (SITE / 'board_updates.js').read_text() + '\nconst input=JSON.parse(require("fs").readFileSync(0,"utf8")); console.log(JSON.stringify(window.__applyBoardEdits(input.old,input.ops)));'
    result = subprocess.run(['node', '-e', code], input=json.dumps({'old': old, 'ops': ops}), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


class Updates(unittest.TestCase):
    def test_job_removal_insertion_reorder_and_nested_changes_match_full_board(self):
        old = {'owb': {'jobs': [{'id': 'J1', 'status': 'open'}, {'id': 'J2', 'status': 'claimed'}, {'id': 'J3', 'status': 'open'}]}, 'tracker': {'videos': [{'key': 'OWB:032', 'lane': 'progress'}]}, 'obsolete': True}
        new = {'owb': {'jobs': [{'id': 'J3', 'status': 'done'}, {'id': 'J2', 'status': 'open'}, {'id': 'J4', 'status': 'claimed'}]}, 'tracker': {'videos': [{'key': 'OWB:032', 'lane': 'uat'}]}, 'checks': {}}
        self.assertEqual(browser_apply(old, bp.board_diff(old, new)), new)

    def test_random_list_edits_match_full_board(self):
        rng = random.Random(2798)
        old = {'jobs': [{'id': str(i), 'value': i} for i in range(30)]}
        for _ in range(12):
            new = copy.deepcopy(old)
            rng.shuffle(new['jobs'])
            new['jobs'] = new['jobs'][:rng.randrange(10, 30)]
            new['jobs'].insert(3, {'id': 'new', 'value': rng.randrange(100)})
            new['jobs'][0]['value'] = -1
            self.assertEqual(browser_apply(old, bp.board_diff(old, new)), new)

    def test_ten_minute_idle_history_stays_under_16kb_and_replays_exactly(self):
        old = {'films': [{'id': '032', 'title': 'Titan'}], 'jobs': [{'id': 'J1', 'status': 'claimed'}], 'heartbeat': '0'}
        original, history = copy.deepcopy(old), None
        for minute in range(1, 11):
            new = {**old, 'heartbeat': str(minute)}
            history = bp.updates_payload(new, old, history, 'tracker unchanged')
            old = new
        self.assertLessEqual(len(json.dumps(history, ensure_ascii=False, separators=(',', ':')).encode()), 16000)
        ops = [op for edit in history['edits'] for op in edit['ops']]
        self.assertEqual(browser_apply(original, ops), new)

    def test_oversized_change_evicts_history_for_safe_full_reload(self):
        old = {'films': []}
        new = {'films': [{'id': '032', 'text': 'x' * 20000}]}
        history = bp.updates_payload(new, old, None, '')
        self.assertEqual(history['edits'], [])
        self.assertEqual(history['revision'], bp.digest(new))

    def test_live_sized_per_film_stamps_do_not_evict_history(self):
        old = {'tracker': {'videos': [{'key': str(i), 'production': {'asOf': 'old'}} for i in range(312)]}}
        new = copy.deepcopy(old)
        for film in new['tracker']['videos']:
            film['production']['asOf'] = 'new'
        history = bp.updates_payload(new, old, None, '')
        self.assertTrue(history['edits'])
        self.assertLess(len(json.dumps(history).encode()), 3000)
        self.assertEqual(browser_apply(old, history['edits'][0]['ops']), new)

    def test_compaction_preserves_order_around_splices(self):
        old = {'rows': [{'id': str(i), 'stamp': 'old'} for i in range(12)]}
        new = {'rows': [{'id': str(i), 'stamp': 'new'} for i in [0, 1, 8, 9, 2, 3, 7]]}
        self.assertEqual(browser_apply(old, bp.compact_edits(bp.board_diff(old, new))), new)

    def test_tree_keeps_legacy_files_and_adds_updates(self):
        tree = bp.tree_listing('board', 'no-deploy', 'sub', 'tracker', 'updates')
        self.assertIn('board\tboard.json', tree)
        self.assertIn('updates\tupdates.json', tree)

if __name__ == '__main__':
    unittest.main()
