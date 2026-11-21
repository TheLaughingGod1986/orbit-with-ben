"""Upload and daily sweeps must use current gates, not cached PASS labels."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
sys.path.insert(0, str(Path(__file__).resolve().parent))
import publishing_gates as g
import scheduled_gates as sg


class Publishing(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'studio').mkdir()
        (self.root / 'studio/channel.json').write_text('{}')
        self.video = self.root / 'short.mp4'
        self.video.write_bytes(b'cut')
        self.meta = self.video.with_name('short_meta.json')
        self.meta.write_text(json.dumps(dict(sha256=hashlib.sha256(b'cut').hexdigest(),
            publishing_gates={k:k for k in ['film', 'bed', 'cuts', 'vo', 'sfx']})))

    def check(self, fmt='short'):
        return g.evaluate(self.video, self.root, fmt, '2026-12-01', short_run=lambda c: (0, 'PASS'))

    def test_reused_bed_blocks_upload_even_with_recorded_pass(self):
        def run(c):
            return (1, 'FAIL reused: same bed (0.830)') if 'music_gate.py' in c[1] else (0, 'PASS')
        with patch.object(g, 'run', side_effect=run):
            result = self.check()
        self.assertFalse(result['ok'])
        self.assertIn('0.830', result['checks'][1]['output'])

    def test_gate_applied_waiver_passes_both_formats(self):
        with patch.object(g, 'run', return_value=(0, 'WAIVED reused: Chief waiver\nPASS')):
            for fmt in ['short', 'long']:
                self.assertTrue(self.check(fmt)['ok'])

    def test_missing_inputs_and_tool_errors_block(self):
        self.meta.write_text('{}')
        with patch.object(g, 'run', return_value=(2, 'unavailable')):
            self.assertFalse(self.check()['ok'])

    def test_changed_export_blocks_even_when_gates_pass(self):
        self.video.write_bytes(b'new cut')
        with patch.object(g, 'run', return_value=(0, 'PASS')):
            self.assertFalse(self.check()['ok'])

    def test_new_unknown_required_gate_cannot_silently_pass(self):
        (self.root / 'studio/channel.json').write_text('{"publishing_gates":{"required":["new_gate"]}}')
        with patch.object(g, 'run', return_value=(0, 'PASS')):
            self.assertFalse(self.check()['ok'])

    def test_daily_flags_failing_bed_ten_days_ahead(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('upcoming_test', g.ROOT / '00_Brand/Channel-Setup/tools/gate_upcoming.py')
        upcoming = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(upcoming)
        at = datetime.now(timezone.utc) + timedelta(days=10)
        (self.root / 'snap.json').write_text(json.dumps({'videos':[dict(id='short', format='short', privacy='private', publishAt=at.isoformat())]}))
        (self.root / 'uploads.json').write_text(json.dumps({'videos':{'short':{'file':'short.mp4'}}}))
        def run(c):
            return (1, 'FAIL reused: 0.830') if 'music_gate.py' in c[1] else (0, 'PASS')
        with patch.object(g, 'run', side_effect=run), patch.object(upcoming, 'run', return_value=(0, 'PASS')):
            upcoming.main(['--snapshot',str(self.root/'snap.json'),'--uploads',str(self.root/'uploads.json'),
                           '--media-root',str(self.root),'--out',str(self.root/'report.md')])
        rows = json.loads((self.root/'report.json').read_text())
        self.assertFalse(rows[0]['ok'])
        self.assertIn('0.830', rows[0]['output'])

    def test_only_near_term_fails_queue_one_chief_fix(self):
        now = datetime.now(timezone.utc)
        rows = [dict(channel='owb', id='near', ok=False, publishAt=(now+timedelta(days=6)).isoformat(),output='music FAIL'),
                dict(channel='hos', id='far', ok=False, publishAt=(now+timedelta(days=10)).isoformat(),output='music FAIL')]
        data = {'jobs': [], 'next': 1}
        import jobs
        def add(data, **kwargs):
            job = dict(kwargs,id='J-test',status='open')
            data['jobs'].append(job)
            return job
        with patch.object(jobs, 'do_add', side_effect=add):
            self.assertEqual(sg.queue_fixes(data, rows, now), ['J-test'])
            self.assertEqual(sg.queue_fixes(data, rows, now), [])
        self.assertEqual(data['jobs'][0]['kind'], 'chief')
        self.assertNotIn('awaits_ben', data['jobs'][0])

    def test_refill_daily_sweep_deduplicates(self):
        import jobs
        data = {'jobs':[]}
        now = datetime.now(timezone.utc)
        def add(data, **kwargs):
            job = dict(kwargs,id='J-test',status='open')
            data['jobs'].append(job)
            return job
        with patch.object(jobs, 'do_add', side_effect=add):
            self.assertEqual(sg.queue_daily(data, now), ['J-test'])
            self.assertEqual(sg.queue_daily(data, now+timedelta(days=1)), [])

if __name__ == '__main__':
    unittest.main()
