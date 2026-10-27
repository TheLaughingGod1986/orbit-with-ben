import copy, datetime as dt, json, pathlib, tempfile, unittest
from unittest.mock import patch
import jobs, workflow_state as w, chief_relay as cr, board_publish as bp
AT=dt.datetime(2026,10,27,1,tzinfo=dt.timezone.utc)
def row(i, **kw):
    return dict(id=i,title=i,status='open',needs='mini',history=[],created_at=AT.isoformat(),**kw)
def chooser(j,up):return 'codex' if 'codex' in up else next(iter(up),'')

class FinalAudit(unittest.TestCase):
    def test_empty_identity_cannot_claim_or_finish(self):
        j=row('X',kind='chief');data={'jobs':[j]}
        with patch.object(cr,'is_elected_chief',return_value=False):
            self.assertFalse(jobs.claimable(data,j,{'mini','any'},AT,''))
            with self.assertRaises(ValueError):jobs.do_next(data,'',{'mini'},AT)
        j.update(status='claimed',by='')
        with self.assertRaises(ValueError):jobs.do_done(j,'','no',AT)
        self.assertEqual(j['status'],'claimed')

    def test_former_chief_may_park_but_not_resume_finish_renew_or_progress(self):
        j={**row('X',kind='chief'),'status':'claimed','by':'codex','eta':(AT+dt.timedelta(hours=1)).isoformat()}
        with patch.object(cr,'is_elected_chief',return_value=False):
            for action in (lambda:jobs.do_next({'jobs':[j]},'codex',{'any'},AT),lambda:jobs.do_done(j,'codex','no',AT),lambda:jobs.do_renew(j,'codex',30,AT),lambda:jobs.do_progress(j,'codex',1,3,AT)):
                with self.assertRaises(ValueError):action()
            jobs.do_release(j,'codex','authority changed',AT)
        self.assertEqual(j['status'],'open')

    def test_peek_and_claim_resume_the_same_job_without_mutating_preview(self):
        held={**row('H'),'status':'claimed','by':'codex','eta':(AT+dt.timedelta(hours=1)).isoformat()}
        data={'jobs':[held,row('N',due=AT.isoformat())]};before=copy.deepcopy(data)
        preview=jobs.choose_next(data,'codex',{'mini'},AT)
        self.assertEqual(data,before)
        self.assertEqual(preview['id'],jobs.do_next(data,'codex',{'mini'},AT)['id'])

    def test_all_layers_share_grace_activity_and_live_lease(self):
        j={**row('H'),'status':'claimed','by':'codex','eta':(AT-dt.timedelta(minutes=20)).isoformat()}
        with patch.object(cr,'current_execution',return_value=None):
            self.assertFalse(jobs.stalled(j,AT));self.assertEqual(cr.stalled_claims({'jobs':[j]},AT),[])
            self.assertEqual(w.state(j,{'H':j},AT),'running')
            j['eta']=(AT-dt.timedelta(minutes=60)).isoformat()
            self.assertTrue(jobs.stalled(j,AT));self.assertEqual([x['id'] for x in cr.stalled_claims({'jobs':[j]},AT)],['H'])
        lease={'job':'H','expiresAt':(AT+dt.timedelta(minutes=10)).isoformat()}
        with patch.object(cr,'current_execution',return_value=lease):
            self.assertFalse(jobs.stalled(j,AT));self.assertEqual(cr.stalled_claims({'jobs':[j]},AT),[])
        self.assertEqual(w.snapshot({'jobs':[j]},AT,'codex',{'codex'},chooser,execution=lease)['counts']['running'],1)
        j['progress']={'at':AT.isoformat()}
        self.assertFalse(w.claim_is_stalled(j,AT))

    def test_dead_pid_or_expired_lease_does_not_claim_activity(self):
        with patch.object(cr,'read_json',return_value={'pid':123,'job':'H','expiresAt':(AT+dt.timedelta(minutes=2)).isoformat()}),patch.object(cr.os,'kill',side_effect=ProcessLookupError):
            self.assertIsNone(cr.current_execution(AT))

    def test_due_hold_creates_one_chief_check_and_keeps_work_blocked(self):
        j={**row('H'),'status':'blocked','result':'date gate; original approval retained'}
        data={'jobs':[j],'next_id':1};jobs.set_wait(j,'relay',AT,{'type':'test','condition':'Current title test has ended','check_at':(AT-dt.timedelta(hours=1)).isoformat()},'Start the next title test')
        jobs.reconcile_holds(data,AT)
        check=next(x for x in data['jobs'] if x.get('recheck_of'))
        self.assertEqual(check['due'],(AT+dt.timedelta(hours=1)).isoformat());self.assertEqual(check['kind'],'chief');self.assertEqual(j['status'],'blocked')
        self.assertEqual(j['result'],'date gate; original approval retained')
        before=copy.deepcopy(data);jobs.reconcile_holds(data,AT+dt.timedelta(minutes=2));self.assertEqual(data,before)
        self.assertFalse(jobs.claimable(data,j,{'mini'},AT,'codex'))
        with patch.object(cr,'is_elected_chief',return_value=False):
            with self.assertRaises(ValueError):jobs.do_reopen(j,'gemini','date alone is not evidence',AT)

    def test_ben_hold_never_queues_automatic_checks(self):
        j={**row('H',awaits_ben={'version':'v1'}),'status':'blocked','hold':{'condition':'Approval','check_at':AT.isoformat()}}
        data={'jobs':[j],'next_id':1};self.assertEqual(jobs.reconcile_holds(data,AT),[])

    def test_verification_retry_is_attributed_to_current_chief(self):
        j={**row('H'),'status':'blocked'}
        with patch.object(cr,'is_elected_chief',return_value=True):
            jobs.set_wait(j,'codex',AT,{'condition':'Test still running','check_at':(AT+dt.timedelta(hours=6)).isoformat()},recheck='CHECK')
        self.assertEqual(j['hold']['last_recheck'],'CHECK');self.assertEqual(j['hold']['checked_by'],'codex')
        self.assertEqual(j['status'],'blocked')

    def test_completed_dependency_requires_verification_not_blind_release(self):
        parent={**row('H',after='D'),'status':'blocked','result':'Waiting for finished QA'}
        done={**row('D'),'status':'done'};data={'jobs':[parent,done],'next_id':1}
        jobs.reconcile_holds(data,AT)
        self.assertEqual(parent['status'],'blocked');self.assertEqual(len([j for j in data['jobs'] if j.get('recheck_of')]),1)

    def test_cloud_chief_is_visible_without_becoming_a_cli_worker(self):
        role=row('ROLE',kind='chief',needs_override='x');role.pop('needs_override')
        snap=w.snapshot({'jobs':[role]},AT,'claude',{'codex'},chooser,include_chief=True)
        self.assertEqual((snap['next']['id'],snap['next']['worker'],snap['next']['mode']),('ROLE','claude','chief-inbox'))
        self.assertEqual(snap['counts']['queued'],1)
        self.assertIsNone(w.select_dispatch({'jobs':[role]},AT,'claude',{'codex'},chooser))

    def test_capability_mismatch_is_waiting_not_ready(self):
        cloud={**row('C'),'needs':'cloud'}
        snap=w.snapshot({'jobs':[cloud]},AT,'codex',{'codex'},chooser)
        self.assertEqual((snap['counts']['queued'],snap['counts']['waiting']),(0,1));self.assertIsNone(snap['next'])

    def test_metadata_is_atomic_and_preserves_newer_action(self):
        j={**row('H'),'remaining_action':'Latest worker action'};data={'jobs':[j]};before=copy.deepcopy(data)
        jobs.apply_metadata(data,[{'id':'H','remaining_action':'Older snapshot'}],'relay',AT)
        self.assertEqual(data,before)
        with self.assertRaises(ValueError):jobs.apply_metadata(data,[{'id':'H','remaining_action':'x','replace':True},{'id':'missing'}],'relay',AT)
        self.assertEqual(data,before)

    def test_version_change_yields_before_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(cr,'STATE',pathlib.Path(tmp)),patch.object(cr,'note_grok_posts'),patch.object(cr,'fetch_claude_beat'),patch.object(cr,'load_out',return_value={}),patch.object(cr,'self_heal',return_value=True),patch.object(cr,'escalate_stale'),patch.object(cr,'code_version',return_value='changed'),patch.object(cr,'run_cli') as cli:
            self.assertEqual(cr.run_locked(AT),0);cli.assert_not_called()
            self.assertEqual(json.loads(cr.d('runner.json').read_text())['state'],'restarting')

    def test_new_input_block_gets_a_bounded_automatic_recheck(self):
        j={**row('H'),'status':'claimed','by':'gemini'}
        jobs.do_block(j,'gemini','Required data not ready',AT)
        self.assertEqual(j['hold']['check_at'],(AT+dt.timedelta(hours=6)).isoformat())
        data={'jobs':[j],'next_id':1};jobs.reconcile_holds(data,AT+dt.timedelta(hours=7))
        self.assertEqual(len([x for x in data['jobs'] if x.get('recheck_of')]),1)

    def test_new_chief_review_is_immediate_and_ben_block_is_not_polled(self):
        review={**row('R'),'status':'claimed','by':'gemini'}
        jobs.do_block(review,'gemini','parked for Chief: exact hash review',AT)
        self.assertNotIn('hold',review)
        self.assertEqual(w.state(review,{'R':review},AT),'review')
        ben={**row('B'),'status':'claimed','by':'gemini'}
        jobs.do_block(ben,'gemini','needs Ben: sign-in',AT)
        data={'jobs':[ben],'next_id':1};self.assertEqual(jobs.reconcile_holds(data,AT+dt.timedelta(days=1)),[])

    def test_dependency_completion_checks_immediately_without_waiting_for_a_timer(self):
        child=row('C');j={**row('P',after='C'),'status':'claimed','by':'gemini'}
        jobs.do_block(j,'gemini','Waiting for the child check',AT)
        self.assertFalse(w.hold_due(j,{'C':child,'P':j},AT))
        child['status']='done'
        self.assertTrue(w.hold_due(j,{'C':child,'P':j},AT))
