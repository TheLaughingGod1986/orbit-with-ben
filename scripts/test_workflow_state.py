import datetime as dt
import copy
import unittest
import workflow_state as w
import jobs

NOW=dt.datetime(2026,10,26,22,tzinfo=dt.timezone.utc)

def job(id, **kw):
    return dict(id=id,status='open',needs='mini',title=id,history=[],created_at='2026-10-26T08:00Z',**kw)

def choose(j,up):
    return 'gemini' if 'gemini' in up else next(iter(up),'')

class Workflow(unittest.TestCase):
    def test_shared_video_job_retains_production_priority(self):
        repair = job('J1471', taskKeys=['OWB:030'])
        repair['created_at'] = '2026-10-25T08:00Z'
        draft = job('J1785', film='044', kind='chief')
        data = {'jobs': [draft, repair]}
        pick = w.select_dispatch(data, NOW, 'codex', {'codex', 'gemini'}, choose)
        self.assertEqual(pick['job']['id'], 'J1471')

    def test_shared_video_focus_matches_any_recorded_video(self):
        shared = job('J2', taskKeys=['OWB:029', 'HOS:008'])
        other = job('J1', film='044')
        data = {'jobs': [other, shared], 'focus': ['HOS:008']}
        self.assertEqual(w.select_dispatch(data, NOW, 'codex', {'codex', 'gemini'}, choose)['job']['id'], 'J2')
        # Actual deadlines and prerequisites still outrank focus.
        other['due'] = '2026-10-27T11:30Z'
        self.assertEqual(w.select_dispatch(data, NOW, 'codex', {'codex', 'gemini'}, choose)['job']['id'], 'J1')

    def test_malformed_video_links_do_not_create_production_priority(self):
        for value in (None, 'OWB:030', [None, '', '   ', 3, 'not-a-video'], {'OWB:030': True}):
            with self.subTest(value=value):
                unlinked = job('J1', taskKeys=value)
                video = job('J2', film='030')
                data = {'jobs': [unlinked, video]}
                self.assertEqual(w.select_dispatch(data, NOW, 'codex', {'codex', 'gemini'}, choose)['job']['id'], 'J2')

    def test_deadline_inheritance_beats_named_audit_and_chief_review(self):
        correction=job('J1')
        upload=job('J2',after='J1',approved_from={'airs':'2026-10-27T11:30Z'})
        audit=job('J0',**{'for':'gemini','backlog':'audit'})
        review={**job('J3'),'status':'blocked','result':'parked for Chief: audit'}
        data={'jobs':[audit,review,upload,correction]}
        self.assertEqual(w.deadlines(data['jobs'])['J1'],w.timestamp('2026-10-27T11:30Z'))
        pick=w.select_dispatch(data,NOW,'codex',{'codex','gemini'},choose)
        self.assertEqual(pick['job']['id'],'J1')
        # A Chief decision that is the prerequisite inherits exactly the same deadline.
        correction.update(status='blocked',result='parked for Chief: technical decision')
        pick=w.select_dispatch(data,NOW,'codex',{'codex','gemini'},choose)
        self.assertEqual((pick['job']['id'],pick['worker'],pick['mode']),('J1','codex','review'))

    def test_role_authority_and_worker_availability(self):
        chief=job('J1',kind='chief',needs_override='x');chief.pop('needs_override')
        self.assertFalse(w.claimable(chief,[chief],NOW,'gemini','codex'))
        named=job('J2',**{'for':'gemini'})
        data={'jobs':[named]}
        self.assertIsNone(w.select_dispatch(data,NOW,'codex',{'codex'},choose))
        snap=w.snapshot(data,NOW,'codex',{'codex'},choose)
        self.assertEqual((snap['counts']['queued'],snap['counts']['waiting']),(0,1))

    def test_review_counts_once_and_preserves_production_hold(self):
        j={**job('J1'),'status':'blocked','result':'parked for Chief: verify','progress':{'step':5,'of':5}}
        active={'job':'J1','agent':'codex','expiresAt':'2026-10-26T22:20Z','progress':{'step':1,'of':3}}
        data={'jobs':[j,job('J2')]}; before=copy.deepcopy(data)
        snap=w.snapshot(data,NOW,'codex',{'codex','gemini'},choose,active)
        self.assertEqual((snap['counts']['running'],snap['counts']['review']),(1,0))
        self.assertEqual(snap['active'][0]['progress'],{'step':1,'of':3})
        self.assertEqual(snap['next']['id'],'J2')
        self.assertEqual(data,before,'snapshot is read only')
        expired=w.snapshot(data,NOW+dt.timedelta(hours=1),'codex',{'codex'},choose,active)
        self.assertEqual(expired['counts']['running'],0)

    def test_production_and_review_active_ids_are_unique(self):
        j={**job('J1'),'status':'claimed','by':'codex','eta':'2026-10-26T23:00Z'}
        active={'job':'J1','agent':'codex','expiresAt':'2026-10-26T22:20Z','progress':{'step':0,'of':3}}
        snap=w.snapshot({'jobs':[j]},NOW,'codex',{'codex'},choose,active)
        self.assertEqual(len(snap['active']),1)
        self.assertEqual(snap['counts']['running'],1)

    def test_dependency_missing_cancelled_cycles_and_reconcile_idempotence(self):
        rows=[job('J1',after='MISSING'),job('J2',after='J3'),job('J3',after='J2'),job('J4',after='J5'),{**job('J5'),'status':'cancelled'}]
        data={'jobs':rows,'next_id':6}
        self.assertEqual(w.dependency_problem(rows[0],{j['id']:j for j in rows})['kind'],'missing')
        for j in rows[:4]:self.assertFalse(w.claimable(j,rows,NOW,'codex','codex'))
        jobs.reconcile_dependencies(data,NOW)
        resolutions=[j for j in data['jobs'] if j.get('dependency_resolution')]
        self.assertEqual(len(resolutions),3)
        self.assertEqual(len({j['dependency_resolution'] for j in resolutions}),3)
        before=copy.deepcopy(data)
        jobs.reconcile_dependencies(data,NOW+dt.timedelta(minutes=1))
        self.assertEqual(data,before)
        self.assertTrue(all(j['status']=='blocked' for j in rows[:4]))

    def test_ben_date_credit_and_unmet_input_holds_preserved(self):
        rows=[job('J1',awaits_ben={'version':'v1'}),job('J2',not_before='2026-10-28T00:00Z'),
              {**job('J3'),'status':'blocked','result':'parked for Chief: wait for credit reset'},job('J4',after='J3')]
        self.assertIsNone(w.select_dispatch({'jobs':rows},NOW,'codex',{'codex','gemini'},choose))

    def test_current_claim_not_preempted_by_new_deadline(self):
        active={**job('J1'),'status':'claimed','by':'gemini','eta':'2026-10-26T23:00Z'}
        newer=job('J2',due='2026-10-26T22:01Z')
        self.assertEqual(w.select_dispatch({'jobs':[newer,active]},NOW,'codex',{'codex','gemini'},choose)['job']['id'],'J1')

    def test_due_validation_and_dst(self):
        self.assertEqual(w.normalize_due('2026-10-26 10:30'),'2026-10-26T10:30:00Z')
        self.assertEqual(w.normalize_due('2026-10-24 10:30'),'2026-10-24T09:30:00Z')
        with self.assertRaises(ValueError):w.normalize_due('tomorrow-ish')

    def test_released_poll_yields_but_remains_claimable(self):
        poll=job('J1'); poll['history']=[{'at':NOW.isoformat(),'what':'released: retry later'}]
        other=job('J2')
        data={'jobs':[poll,other]}
        self.assertEqual(w.select_dispatch(data,NOW,'codex',{'codex'},choose)['job']['id'],'J2')
        self.assertEqual(jobs.do_next(copy.deepcopy(data),'codex',{'mini'},NOW)['id'],'J2')
        self.assertEqual(w.select_dispatch({'jobs':[poll]},NOW,'codex',{'codex'},choose)['job']['id'],'J1')

    def test_finished_consumer_does_not_propagate_old_deadline(self):
        parent=job('J1')
        old={**job('J2',after='J1',due='2026-10-01T00:00Z'),'status':'cancelled'}
        self.assertNotIn('J1',w.deadlines([parent,old]))

    def test_publisher_next_is_exact_dispatch_choice(self):
        import board_publish as bp
        import json, tempfile
        from pathlib import Path
        data={'jobs':[job('J1',due='2026-10-27T10:30Z'),job('J2',**{'for':'gemini','backlog':'audit'})]}
        board={'models':{'chief':{'agent':'codex'},'chiefChain':[{'agent':'codex','up':True},{'agent':'gemini','up':True}], 'models':[]}}
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'queue.json';path.write_text(json.dumps(data))
            snap=bp.dispatch_snapshot(board,NOW,path)
        import routing
        chooser=lambda j,up:routing.preferred_worker(j,up) or next(iter(sorted(up)),'')
        dispatch=w.select_dispatch(data,NOW,'codex',{'codex','gemini'},chooser)
        self.assertEqual((snap['next']['id'],snap['next']['worker'],snap['next']['mode']),
                         (dispatch['job']['id'],dispatch['worker'],dispatch['mode']))
        self.assertEqual(jobs.do_next(copy.deepcopy(data),dispatch['worker'],{'mini','gemini','any'},NOW)['id'],snap['next']['id'])

    def test_add_due_validation_happens_before_mutation(self):
        data={'jobs':[],'next_id':1}
        with self.assertRaises(ValueError):
            jobs.do_add(data,title='x',needs='mini',body='',by='codex',at=NOW,due='bad')
        self.assertEqual(data,{'jobs':[],'next_id':1})
        j=jobs.do_add(data,title='x',needs='mini',body='',by='codex',at=NOW,due='2026-10-27 10:30')
        self.assertEqual(j['due'],'2026-10-27T10:30:00Z')

    def test_done_dependency_is_a_satisfied_boundary(self):
        rows=[job('J1',after='J2'),{**job('J2',after='J3'),'status':'done'},{**job('J3'),'status':'cancelled'}]
        self.assertIsNone(w.dependency_problem(rows[0],{j['id']:j for j in rows}))
        self.assertTrue(w.claimable(rows[0],rows,NOW,'codex','codex'))

    def test_chief_review_waits_for_its_correction(self):
        upload={**job('J1',after='J2',due='2026-10-27T10:30Z'),'status':'blocked','result':'parked for Chief: correction queued'}
        fix=job('J2')
        snap=w.snapshot({'jobs':[upload,fix]},NOW,'codex',{'codex'},choose)
        self.assertEqual(snap['states']['J1']['state'],'waiting')
        self.assertEqual(snap['next']['id'],'J2')

    def test_overdue_claim_is_resumed_before_claiming_a_different_job(self):
        held={**job('J1'),'status':'claimed','by':'gemini','eta':'2026-10-26T21:00Z'}
        data={'jobs':[held,job('J2',due='2026-10-26T22:01Z')]}
        pick=w.select_dispatch(data,NOW,'codex',{'gemini'},choose)
        self.assertEqual(pick['job']['id'],jobs.do_next(copy.deepcopy(data),'gemini',{'mini'},NOW)['id'])

    def test_multi_cut_approval_deadlines_are_supported(self):
        j=job('J1',awaits_was=[{'due':'2026-10-27T10:30Z'},{'due':'2026-10-28T10:30Z'}])
        self.assertEqual(w.deadlines([j])['J1'],w.timestamp('2026-10-27T10:30Z'))

class StartupVisibility(unittest.TestCase):
    def lease(self):
        return {'job':'J1','worker':'codex','startedAt':(NOW-dt.timedelta(minutes=1)).isoformat(),'expiresAt':(NOW+dt.timedelta(minutes=20)).isoformat()}
    def test_live_launch_before_claim_is_starting_not_idle_or_completed_work(self):
        j=job('J1');data={'jobs':[j,job('J2')]};lease=self.lease()
        snap=w.snapshot(data,NOW,'codex',{'codex','gemini'},choose,execution=lease)
        self.assertEqual(snap['states']['J1']['state'],'starting')
        self.assertEqual(snap['active'][0]['worker'],'codex')
        self.assertEqual(snap['active'][0]['phase'],'starting')
        self.assertNotIn('progress',snap['active'][0])
        self.assertEqual((snap['counts']['starting'],snap['counts']['running']),(1,0))
        self.assertEqual(snap['next']['id'],'J2')
        self.assertEqual(j['status'],'open')
        self.assertTrue(w.claimable(j,data['jobs'],NOW,'codex','codex',execution=lease))
        self.assertFalse(w.claimable(j,data['jobs'],NOW,'gemini','codex',execution=lease))
    def test_expired_future_and_unrelated_leases_never_show_work(self):
        j=job('J1')
        for fields in [{'expiresAt':NOW.isoformat()},{'startedAt':(NOW+dt.timedelta(minutes=1)).isoformat()},{'job':'other'},{'worker':''}]:
            self.assertNotEqual(w.state(j,{'J1':j},NOW,execution={**self.lease(),**fields}),'starting')
        self.assertEqual(w.state(j,{'J1':j},NOW),'queued')
    def test_hold_and_unfinished_dependency_win_over_startup(self):
        j=job('J1',hold={'condition':'Input missing'})
        self.assertEqual(w.state(j,{'J1':j},NOW,execution=self.lease()),'waiting')
        j.pop('hold');j['after']='J2';other=job('J2')
        self.assertEqual(w.state(j,{'J1':j,'J2':other},NOW,execution=self.lease()),'waiting')
    def test_claim_and_completion_end_the_startup_phase(self):
        j={**job('J1'),'status':'claimed','by':'codex','eta':NOW.isoformat()}
        snap=w.snapshot({'jobs':[j]},NOW,'codex',{'codex'},choose,execution=self.lease())
        self.assertEqual((snap['counts']['starting'],snap['counts']['running']),(0,1))
        j['status']='done'
        self.assertEqual(w.snapshot({'jobs':[j]},NOW,'codex',{'codex'},choose,execution=self.lease())['active'],[])


class ImmediateUserDispatch(unittest.TestCase):
    def fixture(self):
        held=job('J1859',status_override='x');held.pop('status_override')
        held.update(status='claimed',by='gemini',eta='2026-10-26T23:00Z',kind='review',backlog='monthly-improvement-owb',progress={'step':2,'of':4})
        request=job('J1870',urgent=3,due=NOW.isoformat(),due_kind='user-immediate-claim')
        older=job('Jcheck',kind='chief',due='2026-10-25T09:00Z')
        return {'jobs':[held,request,older]}
    def pick(self,data,**kwargs):
        return w.select_dispatch(data,NOW,'codex',{'codex','gemini'},choose,**kwargs)
    def test_request_uses_free_worker_at_boundary_without_changing_claims(self):
        data=self.fixture();before=copy.deepcopy(data);p=self.pick(data)
        self.assertEqual((p['job']['id'],p['worker']),('J1870','codex'))
        self.assertEqual(data,before)
        # The actual selected worker's normal exact-ID claim must agree with dispatch.
        self.assertEqual(jobs.choose_next(data,'codex',w.MINI,NOW,'J1870')['id'],'J1870')
    def test_valid_execution_is_never_preempted(self):
        data=self.fixture();e={'job':'J1859','worker':'gemini','expiresAt':(NOW+dt.timedelta(minutes=10)).isoformat()}
        self.assertEqual(self.pick(data,execution=e)['job']['id'],'J1859')
        e['expiresAt']=(NOW-dt.timedelta(seconds=1)).isoformat()
        self.assertEqual(self.pick(data,execution=e)['job']['id'],'J1870')
    def test_ordinary_urgency_and_future_requests_do_not_override_resume(self):
        for changes in [{'due_kind':'production'}, {'urgent':False}, {'due':(NOW+dt.timedelta(hours=1)).isoformat()}]:
            data=self.fixture();data['jobs'][1].update(changes)
            self.assertEqual(self.pick(data)['job']['id'],'J1859')
    def test_holds_dependencies_named_workers_and_exclusions_remain_enforced(self):
        for changes in [{'hold':{'condition':'Needs approval'}}, {'after':'missing'}, {'after':'J1859'}, {'needs':'ben'}, {'for':'gemini'}]:
            data=self.fixture();data['jobs'][1].update(changes)
            self.assertEqual(self.pick(data)['job']['id'],'J1859')
        self.assertEqual(self.pick(self.fixture(),exclude=['J1870'])['job']['id'],'J1859')
    def test_no_worker_gets_a_second_claim_or_an_ineligible_routing_fallback(self):
        data=self.fixture();data['jobs'].append({**job('Jheld'),'status':'claimed','by':'codex','eta':'2026-10-26T23:00Z'})
        self.assertEqual(self.pick(data)['job']['id'],'J1859')
        data=self.fixture()
        p=w.select_dispatch(data,NOW,'codex',{'codex','gemini'},lambda j,up:'gemini')
        self.assertEqual(p['job']['id'],'J1859')
    def test_chief_requests_use_only_elected_chief(self):
        data=self.fixture();data['jobs'][1]['kind']='chief'
        self.assertEqual(self.pick(data)['worker'],'codex')
        data['jobs'][0]['by']='codex'
        self.assertNotEqual(self.pick(data)['job']['id'],'J1870')

    def test_media_or_nonmonthly_claim_cannot_be_yielded(self):
        for patch in [{'film':'027','stage':'edit'},{'kind':'assembly'},{'backlog':'ordinary-review'}]:
            data=self.fixture();data['jobs'][0].update(patch)
            self.assertEqual(self.pick(data)['job']['id'],'J1859')
    def test_safe_yield_preserves_steps_and_next_exact_claim_is_real(self):
        data=self.fixture();pick=self.pick(data)
        result=jobs.yield_monthly_for_request(data,'J1870',pick['yield_monthly'],NOW)
        self.assertEqual(result,['J1859'])
        self.assertEqual(data['jobs'][0]['progress'],{'step':2,'of':4})
        self.assertEqual(data['jobs'][0]['status'],'open')
        self.assertEqual(data['jobs'][0]['history'][-1]['by'],'relay')
        claimed=jobs.do_next(data,'codex',w.MINI,NOW,job_id='J1870')
        self.assertEqual(claimed['id'],'J1870')
        snap=w.snapshot(data,NOW,'codex',{'codex','gemini'},choose)
        self.assertEqual([x['id'] for x in snap['active']],['J1870'],'yielded report is queued, never a fake second running job')
    def test_yield_races_are_atomic_and_preserve_holds(self):
        for patch in [{'hold':{'condition':'wait for approval'}},{'status':'claimed','by':'gemini'},{'after':'missing'}]:
            data=self.fixture();pick=self.pick(data);data['jobs'][1].update(patch);before=copy.deepcopy(data)
            with self.assertRaises(ValueError):jobs.yield_monthly_for_request(data,'J1870',pick['yield_monthly'],NOW)
            self.assertEqual(data,before)
        data=self.fixture();pick=self.pick(data);data['jobs'][0]['by']='codex';before=copy.deepcopy(data)
        with self.assertRaises(ValueError):jobs.yield_monthly_for_request(data,'J1870',pick['yield_monthly'],NOW)
        self.assertEqual(data,before)

    def test_relay_wont_touch_queue_while_execution_is_live(self):
        import chief_relay as relay
        from unittest.mock import patch
        data=self.fixture();pick=self.pick(data)
        with patch.object(relay,'current_execution',return_value={'job':'J1859'}), patch.object(jobs,'with_git') as transaction, patch.object(relay,'log'):
            self.assertFalse(relay.yield_monthly_for_dispatch(pick));transaction.assert_not_called()
    def test_relay_commits_yield_before_allowing_dispatch_and_stops_on_race(self):
        import chief_relay as relay
        from unittest.mock import patch
        data=self.fixture();pick=self.pick(data)
        def transact(apply,message):
            out,error,touched=apply(data);return out,error
        with patch.object(relay,'current_execution',return_value=None), patch.object(relay,'now',return_value=NOW), patch.object(relay,'log'), patch.object(jobs,'with_git',side_effect=transact):
            self.assertTrue(relay.yield_monthly_for_dispatch(pick))
            self.assertEqual(data['jobs'][0]['status'],'open')
        data=self.fixture();pick=self.pick(data);data['jobs'][1]['hold']={'condition':'Needs approval'}
        with patch.object(relay,'current_execution',return_value=None), patch.object(relay,'now',return_value=NOW), patch.object(relay,'log'), patch.object(jobs,'with_git',side_effect=transact):
            self.assertFalse(relay.yield_monthly_for_dispatch(pick))
            self.assertEqual(data['jobs'][0]['status'],'claimed')
