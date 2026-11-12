"""Exercise the CLI on narrated cards without weakening breath or end holds."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / '00_Brand/Channel-Setup/tools/clip_check.py'


class NarratedCards(unittest.TestCase):
    def run_check(self, breath=.6, end=7., card_text='Next discovery.', prior_text='First result.'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            words = [dict(word=w, start=s, end=e) for w, s, e in
                     [('First', 0., .8), ('result.', 1., 2.),
                      ('Next', 3., 3.8), ('discovery.', 4., 5.)]]
            (root/'words.json').write_text(json.dumps({'words': words}))
            with (root/'cuts.csv').open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['row', 'source', 'vo_in', 'vo_out', 'vo_text'])
                writer.writerow(['1', 'picture', 0., 2.+breath, prior_text])
                writer.writerow(['2', 'CARD', 2.+breath, 5.2, card_text])
                writer.writerow(['3', 'picture', 5.2, end, ''])
            proc = subprocess.run([sys.executable, str(CHECKER), str(root/'cuts.csv'),
                                   '--words', str(root/'words.json'), '--json'],
                                  capture_output=True, text=True)
            return proc.returncode, json.loads(proc.stdout)

    def test_narrated_card_uses_preceding_sentence(self):
        code, result = self.run_check()
        self.assertEqual(code, 0, result)
        self.assertTrue(result['passed'])
        self.assertEqual(result['errors'], [])

    def test_insufficient_breath_still_fails(self):
        code, result = self.run_check(breath=.2)
        self.assertEqual(code, 1)
        self.assertTrue(any('breath before card 0.20s' in x for x in result['errors']))

    def test_card_narration_still_counts_for_end_hold(self):
        code, result = self.run_check(end=6.)
        self.assertEqual(code, 1)
        self.assertTrue(any('end hold only 1.00s' in x for x in result['errors']))

    def test_long_breath_remains_warning(self):
        code, result = self.run_check(breath=1.)
        self.assertEqual(code, 0, result)
        self.assertTrue(any('breath before card 1.00s' in x for x in result['warnings']))

    def test_unfinished_sentence_still_fails(self):
        code, result = self.run_check(prior_text='First result')
        self.assertEqual(code, 1)
        self.assertTrue(any('CARD before VO sentence finishes' in x for x in result['errors']))

    def test_silent_card_still_passes(self):
        code, result = self.run_check(card_text='')
        self.assertEqual(code, 0, result)


if __name__ == '__main__':
    unittest.main()
