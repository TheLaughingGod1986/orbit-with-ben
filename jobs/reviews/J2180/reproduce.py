"""Run against PR512 checkout: python3 reproduce.py /path/to/checkout.

Assertions describe required fail-closed behavior; both fail at be2c980ffa.
Uses only synthetic files from the PR's fixture, no studio media or credit.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv.pop(1)) / 'scripts'))
from test_terminal_loop import TerminalLoop
import terminal_loop
import picture_qa


class ReviewRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TerminalLoop.setUpClass()

    @classmethod
    def tearDownClass(cls):
        TerminalLoop.tearDownClass()

    def recipe(self):
        return TerminalLoop().setup_recipe()

    def test_missing_body_source_must_fail_identity_verification(self):
        cuts, declaration = self.recipe()
        cuts[1]['source'] = str(TerminalLoop.root / 'missing-body.mp4')
        result = terminal_loop.validate(cuts, declaration)
        rows = picture_qa.source_checks(cuts, {}, result)
        print('MISSING BODY:', result['status'], 'failures=', [r['fail'] for r in rows])
        self.assertTrue(rows[1]['fail'], 'Absent source must not receive a verified unique identity')

    def test_missing_video_offset_must_not_disable_whole_run_checks(self):
        cuts, declaration = self.recipe()
        cuts[1]['source'] = str(TerminalLoop.src)
        cuts[1]['framing'].pop('offset')
        result = terminal_loop.validate(cuts, declaration)
        rows = picture_qa.source_checks(cuts, {}, result)
        print('MISSING OFFSET:', result['status'], 'failures=', [r['fail'] for r in rows])
        self.assertTrue(any(r['fail'] for r in rows),
                        'Explicit video body missing offset must fail, not turn the 24s run into a still')


if __name__ == '__main__':
    unittest.main(verbosity=2)
