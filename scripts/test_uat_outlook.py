import unittest
from datetime import datetime, timedelta, timezone
from uat_outlook import PLAN, attach, forecast, learn_documents

NOW = datetime(2026, 11, 2, 18, tzinfo=timezone.utc)


class OutlookTests(unittest.TestCase):
    def setUp(self):
        self.video = dict(key='OWB:999', channel='OWB', type='long', lane='progress')
        self.stages = {key: dict(state='done') for key in PLAN}
        self.samples = {('OWB', 'long', key): [(10, 'OWB:001'), (20, 'OWB:002'), (30, 'OWB:003')] for key in PLAN}

    def run_forecast(self, jobs=()):
        return forecast(self.video, self.stages, list(jobs), self.samples, NOW)

    def test_final_stage_estimate_excludes_upload_and_watch(self):
        self.stages['qa'] = dict(state='doing', since=(NOW-timedelta(minutes=5)).isoformat())
        result = self.run_forecast([dict(id='qa', stage='qa', status='claimed', by='chief')])
        self.assertEqual(result['completed'], 8)
        self.assertEqual(result['eta']['state'], 'estimated')
        self.assertEqual(result['eta']['lowerMinutes'], 15)
        self.assertEqual(result['eta']['upperMinutes'], 25)
        self.assertEqual(result['eta']['confidence'], 'low')
        self.assertEqual(result['eta']['criticalPath'], ['qa'])

    def test_parallel_branches_take_max_not_sum(self):
        for stage in ('vo', 'picture', 'edit', 'thumbs', 'qa'):
            self.stages[stage] = dict(state='doing', since=NOW.isoformat())
        result = self.run_forecast([dict(id=k, stage=k, status='claimed', by=k) for k in ('vo', 'picture', 'edit', 'thumbs', 'qa')])
        # Picture -> edit -> QA is three stages, not five serial stages.
        self.assertEqual(result['eta']['lowerMinutes'], 60)
        self.assertEqual(result['eta']['upperMinutes'], 90)

    def test_block_queue_manual_dependency_and_unmapped_work(self):
        for job, message in [
            (dict(status='blocked', hold={'condition': 'credit reset'}), 'credit reset'),
            (dict(status='open'), 'queue start'),
            (dict(status='claimed', title='Flow generation'), 'manual Flow'),
            (dict(status='claimed', after='Joutside'), 'dependency Joutside'),
            (dict(status='claimed', stage='admin'), 'not mapped'),
        ]:
            job = dict(id='J1', stage='qa', **job) if 'stage' not in job else dict(id='J1', **job)
            e = self.run_forecast([job])['eta']
            self.assertEqual(e['state'], 'unavailable')
            self.assertIn(message, ' '.join(e['reasons']))
            self.assertNotIn('lowerMinutes', e)

    def test_insufficient_history_overrun_and_missing_start(self):
        self.stages['qa'] = dict(state='doing')
        self.assertIn('start not recorded', ' '.join(self.run_forecast()['eta']['reasons']))
        self.stages['qa']['since'] = (NOW-timedelta(hours=2)).isoformat()
        self.assertIn('longer than historical', ' '.join(self.run_forecast()['eta']['reasons']))
        self.samples.clear()
        self.assertIn('fewer than 3', ' '.join(self.run_forecast()['eta']['reasons']))

    def test_ready_review_changes_and_completed_handoffs(self):
        self.video.update(lane='ready', readyFor='Ben')
        self.assertEqual(self.run_forecast()['eta']['state'], 'ready')
        self.video.update(lane='changes')
        self.assertEqual(self.run_forecast()['eta']['state'], 'unavailable')
        self.video.update(lane='approved')
        self.assertEqual(self.run_forecast()['eta']['state'], 'complete')

    def test_real_transitions_unknown_baseline_and_rework(self):
        key = 'OWB:001'
        def snap(minutes, state):
            return NOW+timedelta(minutes=minutes), {key: {'edit': {'state': state}}}
        self.assertEqual(learn_documents([snap(0, 'doing'), snap(10, 'done')], 'OWB'), {})
        samples = learn_documents([snap(0, 'todo'), snap(1, 'doing'), snap(11, 'done'),
                                   snap(12, 'doing'), snap(17, 'done')], 'OWB')
        self.assertEqual(samples[('OWB', 'long', 'edit')], [(15, key)])

    def test_complete_milestones_without_handoff_are_not_ready(self):
        e = self.run_forecast()['eta']
        self.assertEqual(e['state'], 'unavailable')
        self.assertIn('handoff not confirmed', ' '.join(e['reasons']))

    def test_history_batch_reads_real_git_boundaries(self):
        import json
        import os
        from pathlib import Path
        import subprocess
        import tempfile
        from uat_outlook import history_samples
        with tempfile.TemporaryDirectory() as directory:
            def git(*args, at=None):
                env = dict(os.environ)
                if at:
                    env.update(GIT_AUTHOR_DATE=at, GIT_COMMITTER_DATE=at)
                return subprocess.run(['git', '-C', directory, *args], env=env, capture_output=True, check=True)
            git('init')
            git('config', 'user.name', 'Test')
            git('config', 'user.email', 'test@example.com')
            for i, state in enumerate(('todo', 'doing', 'done')):
                Path(directory, 'status.json').write_text(json.dumps(dict(film='001', stages=dict(edit=dict(state=state)))))
                git('add', 'status.json')
                git('commit', '-m', state, at=f'2026-11-01T12:{i*10:02}:00Z')
            self.assertEqual(history_samples(directory, 'status.json', 'OWB')[('OWB', 'long', 'edit')], [(10, 'OWB:001')])
            self.assertEqual(history_samples(directory, 'missing.json', 'OWB'), {})

    def test_approval_wait_duplicate_jobs_and_original_note(self):
        from uat_outlook import milestone_rows, select_current
        original = 'J1191 complete (parked for Chief picture PASS): all 101/101 Flow v03 rows minted and KEEP'
        self.stages['picture'] = dict(state='done', note=original)
        job = dict(id='J1191', stage='picture', status='blocked', by='chief', hold={'type':'approval', 'condition':'Chief picture PASS'})
        rows = milestone_rows(self.stages, [job, job])
        picture = next(r for r in rows if r['id']=='picture')
        self.assertEqual(picture['state'], 'done', 'source state never rewritten')
        self.assertEqual(picture['displayState'], 'review')
        self.assertEqual(picture['summary'], '101/101 Flow shots generated')
        self.assertEqual(picture['source']['note'], original)
        self.assertEqual(len(picture['jobs']), 1)
        self.assertEqual(select_current(rows), ['picture'])
        result = self.run_forecast([job, job])
        self.assertEqual(result['completed'], 8)
        self.assertEqual(result['eta']['state'], 'unavailable')

    def test_partial_stage_estimate_is_not_full_uat(self):
        self.stages['picture'] = dict(state='doing', since=NOW.isoformat())
        self.stages['qa'] = dict(state='unknown')
        self.samples.pop(('OWB','long','qa'))
        result = self.run_forecast([dict(id='J1', stage='picture', status='claimed', by='cursor')])
        self.assertEqual(result['eta']['state'], 'unavailable')
        self.assertEqual(result['partialEstimates'][0]['stage'], 'picture')
        self.assertNotIn('lowerMinutes', result['eta'])

    def test_format_channel_and_variability_are_not_pooled(self):
        self.stages['qa'] = dict(state='doing', since=NOW.isoformat())
        self.video['type'] = 'short'
        self.assertEqual(self.run_forecast()['eta']['state'], 'unavailable')
        self.video.update(type='long', channel='HOS')
        self.assertEqual(self.run_forecast()['eta']['state'], 'unavailable')
        self.video['channel'] = 'OWB'
        self.samples[('OWB','long','qa')] = [(10 if i<7 else 1000, 'OWB:'+str(i)) for i in range(12)]
        result = self.run_forecast([dict(id='qa',stage='qa',status='claimed',by='chief')])
        self.assertEqual(result['eta']['confidence'], 'low')

    def test_review_does_not_invent_a_chief_assignment(self):
        from uat_outlook import milestone_rows
        rows = milestone_rows({'vo':{'state':'review','note':'Recording ready for checking'}}, [])
        voice = next(r for r in rows if r['id']=='vo')
        self.assertEqual(voice['owner'], '')
        self.assertEqual(voice['reviewer'], '')
        self.assertTrue(voice['awaitingApproval'])

    def test_current_film_cannot_train_its_own_eta(self):
        self.samples[('OWB', 'long', 'qa')][0] = (10, 'OWB:999')
        self.stages['qa'] = dict(state='doing', since=NOW.isoformat())
        self.assertEqual(self.run_forecast()['eta']['state'], 'unavailable')

    def test_short_never_inherits_parent_stage_completion(self):
        from unittest.mock import patch
        video = dict(self.video, key='OWB:999:S:x', type='short')
        with patch('uat_outlook.history_samples', return_value={}):
            attach([video], {}, [dict(film='999', stages=self.stages)], [], NOW)
        self.assertEqual(video['production']['completed'], 0)
        self.assertEqual(video['production']['eta']['state'], 'unavailable')

    def test_mixed_cut_keeps_project_history_without_borrowing_completion_or_eta(self):
        import copy
        from unittest.mock import patch
        stages={k:dict(state='done' if k not in ('edit','qa') else 'blocked' if k=='edit' else 'unknown') for k in PLAN}
        stages['edit']['note']='AR cohort: replacement input remains blocked; original cut is separate'
        original=copy.deepcopy(stages)
        for corrected in [False,True]:
            video=dict(self.video,cutFormatCorrected=corrected,type='short' if corrected else 'long',watch={'file':'original.mp4'})
            with patch('uat_outlook.history_samples',return_value={}):
                attach([video],{},[dict(film='999',stages=stages)],[],NOW)
            p=video['production']
            self.assertEqual(p['scope'],'unconfirmed_cut')
            self.assertEqual(p['projectHistory']['completed'],7)
            self.assertEqual(p['completed'],0)
            self.assertEqual(p['eta']['state'],'unavailable')
            self.assertNotIn('lowerMinutes',p['eta'])
            self.assertEqual(stages,original)

    def test_unambiguous_long_retains_milestone_completion(self):
        from unittest.mock import patch
        video=dict(self.video)
        with patch('uat_outlook.history_samples',return_value={}):
            attach([video],{},[dict(film='999',stages=self.stages)],[],NOW)
        self.assertNotIn('scope',video['production'])
        self.assertEqual(video['production']['completed'],9)

    def test_exact_cut_mapping_can_restore_short_progress_but_wrong_version_cannot(self):
        from unittest.mock import patch
        for version, expected in [('v13a',9),('v12',0)]:
            video=dict(self.video,type='short',version='v13a',cutFormatCorrected=True)
            source=dict(film='999',stages=self.stages,milestoneScope=dict(type='cut',format='short',version=version))
            with patch('uat_outlook.history_samples',return_value={}):
                attach([video],{},[source],[],NOW)
            self.assertEqual(video['production']['completed'],expected)
            self.assertEqual(video['production']['scope'],'cut' if expected else 'unconfirmed_cut')

    def test_same_worker_parallel_capacity_unavailable(self):
        jobs = [dict(id=k, stage=k, status='claimed', by='cursor') for k in ('picture', 'vo')]
        self.assertIn('Shared worker', ' '.join(self.run_forecast(jobs)['eta']['reasons']))


class RecordedHosSchemaTests(unittest.TestCase):
    def test_hos_records_map_without_completing_unrecorded_stages(self):
        import copy
        stages = {'topic': {'status': 'done'}, 'script': {'status': 'done'},
                  'facts': {'status': 'done'}, 'vo': {'status': 'done'},
                  'picture': {'status': 'doing', 'steps': [70, 90], 'steps_unit': 'board rows rendered'},
                  'thumbnails': {'status': 'todo'}, 'package': {'status': 'done'}}
        before = copy.deepcopy(stages)
        video = dict(key='HOS:009', channel='HOS', type='long', lane='progress')
        result = forecast(video, stages, [], {}, NOW)
        rows = {r['id']: r for r in result['milestones']}
        self.assertEqual(result['completed'], 4)
        self.assertEqual(rows['thumbs']['state'], 'todo')
        self.assertEqual(rows['shots']['state'], 'unknown')
        self.assertEqual(rows['qa']['state'], 'unknown')
        self.assertEqual(rows['picture']['summary'], '70/90 picture rows recorded')
        self.assertEqual(rows['picture']['displayState'], 'doing')
        self.assertEqual(stages, before)

    def test_canonical_unknown_and_pending_approval_win_over_alias_done(self):
        from uat_outlook import milestone_rows
        for canonical in ({'state': 'unknown'}, {}, {'state': 'done', 'approval': {'status': 'pending'}}):
            with self.subTest(canonical=canonical):
                rows = milestone_rows({'sources': canonical, 'facts': {'status': 'done'}}, [])
                source = next(r for r in rows if r['id'] == 'sources')
                self.assertNotIn(source['displayState'], ('done', 'passed', 'skip'))

    def test_approval_pending_on_hos_fact_record_remains_incomplete(self):
        from uat_outlook import milestone_rows
        rows = milestone_rows({'facts': {'status': 'done', 'approval': {'status': 'pending'}}}, [])
        source = next(r for r in rows if r['id'] == 'sources')
        self.assertEqual(source['displayState'], 'review')

    def test_alias_stage_job_preserves_approval_hold(self):
        from uat_outlook import milestone_rows
        rows = milestone_rows({'facts': {'status': 'done'}},
                              [{'id': 'Jfacts', 'stage': 'facts', 'status': 'blocked', 'hold': {'type': 'chief'}}])
        source = next(r for r in rows if r['id'] == 'sources')
        self.assertEqual(source['displayState'], 'review')
        self.assertEqual(source['jobs'][0]['id'], 'Jfacts')

    def test_invalid_or_non_row_step_counts_do_not_become_picture_counts(self):
        from uat_outlook import milestone_rows
        for steps, unit in [([91, 90], 'rows'), ([-1, 90], 'rows'), ([True, 90], 'rows'),
                            ([70, 0], 'rows'), (['70', 90], 'rows'), ([2, 3], 'agent tasks'), ([70], 'rows')]:
            with self.subTest(steps=steps, unit=unit):
                rows = milestone_rows({'picture': {'status': 'doing', 'steps': steps, 'steps_unit': unit}}, [])
                self.assertEqual(next(r for r in rows if r['id'] == 'picture')['summary'], '')

    def test_hos_fact_timing_uses_same_recorded_alias(self):
        history = [(NOW + timedelta(minutes=i), {'HOS:001': {'facts': {'status': state}}})
                   for i, state in [(0, 'todo'), (10, 'doing'), (30, 'done')]]
        samples = learn_documents(history, 'HOS')
        self.assertEqual(samples[('HOS', 'long', 'sources')], [(20, 'HOS:001')])


if __name__ == '__main__':
    unittest.main()
