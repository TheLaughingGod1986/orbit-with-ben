#!/usr/bin/env python3
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_progress as vp

UTC = dt.timezone.utc


class HistoricalStages(unittest.TestCase):
    def run_git(self, root, *args, env=None):
        return subprocess.check_output(['git', '-C', str(root), *args], env=env, stderr=subprocess.DEVNULL).decode().strip()

    def commit(self, root, at):
        self.run_git(root, 'add', '.')
        return self.run_git(root, '-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '-qm', at,
                            env={**os.environ, 'GIT_AUTHOR_DATE': at, 'GIT_COMMITTER_DATE': at}) or self.run_git(root, 'rev-parse', 'HEAD')

    def test_baseline_uses_tree_before_cutoff_and_reads_paths_with_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.run_git(root, 'init', '-q')
            p = root / '02_Video-Projects/024_Light Speed/status.json'; p.parent.mkdir(parents=True)
            p.write_text(json.dumps({'film': '024', 'stages': {'edit': {'state': 'todo'}}}))
            before = self.commit(root, '2026-10-17T10:00:00Z')
            p.write_text(json.dumps({'film': '024', 'stages': {'edit': {'state': 'done'}}}))
            self.commit(root, '2026-10-19T10:00:00Z')
            cache = {}; cutoff = dt.datetime(2026, 10, 18, tzinfo=UTC)
            baseline = vp.historical_stages(root, 'OWB', cutoff, cache)
            self.assertTrue(baseline['available'])
            self.assertEqual(baseline['commit'], before)
            self.assertEqual(baseline['films']['OWB:024']['stages']['edit']['state'], 'todo')
            with patch.object(vp, 'documents_at', side_effect=AssertionError('Cached commit reread')):
                self.assertEqual(vp.historical_stages(root, 'OWB', cutoff, cache), baseline)
            self.assertFalse(vp.historical_stages(root, 'OWB', dt.datetime(2026, 10, 16, tzinfo=UTC), {})['available'])

    def test_hos_keeps_historical_weights_and_fractional_stage_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); self.run_git(root, 'init', '-q')
            p=root/'00_Brand/Channel-Setup/PIPELINE.json';p.parent.mkdir(parents=True)
            p.write_text(json.dumps({'stages':[{'key':'picture','weight':35}], 'films':[{'id':'006','stages':{'picture':{'status':'doing','progress':0.4}}}]}))
            self.commit(root,'2026-10-17T10:00:00Z')
            d=vp.historical_stages(root,'HOS',dt.datetime(2026,10,18,tzinfo=UTC),{})
            self.assertEqual(d['films']['HOS:006']['stages']['picture']['progress'],0.4)
            self.assertEqual(d['definitions'],[{'key':'picture','weight':35}])

    def test_missing_history_and_invalid_json_are_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(vp.historical_stages(Path(tmp),'HOS',dt.datetime.now(UTC),{})['available'])
            root=Path(tmp);self.run_git(root,'init','-q')
            p=root/'00_Brand/Channel-Setup/PIPELINE.json';p.parent.mkdir(parents=True);p.write_text('{bad')
            self.commit(root,'2026-10-17T10:00:00Z')
            self.assertFalse(vp.historical_stages(root,'HOS',dt.datetime.now(UTC),{})['available'])


class RecordedWork(unittest.TestCase):
    def test_unique_work_excludes_reminders_and_keeps_review_distinct_from_done(self):
        jobs=[{'id':'J1','status':'blocked','taskKeys':['HOS:006'],'history':[
            {'at':'2026-10-20T01:00Z','what':'claimed'}, {'at':'2026-10-20T02:00Z','what':'step 4 of 4 done: draft saved'},
            {'at':'2026-10-20T03:00Z','what':'claimed'}, {'at':'2026-10-20T04:00Z','what':'escalated to Chief'}]},
            {'id':'J2','status':'blocked','history':[{'at':'2026-10-20T03:00Z','what':'escalated to Chief'}]},
            {'id':'J3','status':'done','history':[{'at':'2026-10-20T04:00Z','what':'done: published data'}]},
            {'id':'J4','status':'claimed','history':[{'at':'2026-10-21T04:00Z','what':'claimed'}]}]
        rows=vp.work_since(jobs,dt.datetime(2026,10,20,tzinfo=UTC),dt.datetime(2026,10,20,12,tzinfo=UTC))
        self.assertEqual([r['id'] for r in rows],['J1','J3'])
        self.assertFalse(rows[0]['done']);self.assertTrue(rows[1]['done'])
        self.assertEqual(rows[0]['workedAt'],'2026-10-20T03:00:00Z')

    def test_explicit_target_takes_precedence_and_generic_numbers_do_not_create_links(self):
        self.assertEqual(vp.job_targets({'title':'HOS 007 script','taskKeys':['HOS:006']}),['HOS:006'])
        self.assertEqual(vp.job_targets({'title':'Channel check','result':'95 points; 19 videos'}),[])
        self.assertEqual(vp.job_targets({'title':'HOS script','result':'HOS 006 updated'}),['HOS:006'])


if __name__ == '__main__':
    unittest.main()
