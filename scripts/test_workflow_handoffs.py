import copy
import datetime as dt
import pathlib
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).parent))
import jobs
import workflow_handoffs as h
import workflow_state as w
AT=dt.datetime(2026,11,3,12,tzinfo=dt.timezone.utc)

class Handoffs(unittest.TestCase):
    def setUp(self):
        self.data={'next_id':1,'jobs':[],'focus':['031']}
        self.films=[('031',{'stages':{'vo':{'state':'review','lock':'v02a','ref':'h32'}},'claims':[]})]
    def test_orphan_review_creates_one_durable_chief_repair_and_never_changes_stage(self):
        before=copy.deepcopy(self.films)
        ids=h.reconcile(self.data,self.films,AT,jobs.do_add)
        self.assertEqual(len(ids),1)
        task=self.data['jobs'][0]
        self.assertEqual((task['kind'],task['needs']),('chief','mini'))
        self.assertFalse(jobs.on_board(task))
        self.assertEqual(self.films,before)
        self.assertEqual(h.reconcile(self.data,self.films,AT,jobs.do_add),[])
        self.assertIsNone(w.select_dispatch(self.data,AT,None,{'cursor'},lambda j,ws:'cursor'))
        self.assertEqual(w.select_dispatch(self.data,AT,'codex',{'codex'},lambda j,ws:'codex')['job']['id'],ids[0])
    def test_existing_review_correction_or_hold_is_not_duplicated(self):
        for state in ['open','claimed','blocked']:
            self.data['jobs']=[{'id':'J9','film':'031','stage':'vo','status':state}]
            self.assertEqual(h.findings(self.data,self.films,AT),[])
    def test_hos_number_collision_cannot_hide_owb_gap(self):
        self.data['jobs']=[{'id':'J9','film':'031','stage':'vo','repo':'hos','status':'open'}]
        self.assertEqual(len(h.findings(self.data,self.films,AT)),1)
    def test_live_stage_claim_waits_but_expired_claim_recovers(self):
        rec=self.films[0][1];rec['claims']=[{'stage':'vo','eta':(AT+dt.timedelta(minutes=5)).isoformat()}]
        self.assertEqual(h.findings(self.data,self.films,AT),[])
        self.assertEqual(len(h.findings(self.data,self.films,AT+dt.timedelta(minutes=6))),1)
    def test_stranded_doing_and_blocked_are_recovered(self):
        for state in ['doing','blocked']:
            self.films[0][1]['stages']['vo']['state']=state
            self.assertEqual(h.findings(self.data,self.films,AT)[0]['kind'],'orphan-'+state)
    def test_focus_continuation_without_bulk_backlog_generation(self):
        self.films[0][1]['stages']['vo']['state']='done'
        self.assertEqual(h.findings(self.data,self.films,AT)[0]['kind'],'missing-next-step')
        self.data['focus']=[]
        self.assertEqual(h.findings(self.data,self.films,AT),[])
    def test_published_history_not_reopened(self):
        self.films[0][1]['stages']['upload']={'state':'done'}
        self.assertEqual(h.findings(self.data,self.films,AT),[])
    def test_repair_cannot_finish_with_same_unresolved_gap(self):
        h.reconcile(self.data,self.films,AT,jobs.do_add);task=self.data['jobs'][0]
        with self.assertRaises(ValueError):h.check_completion(task,self.data,self.films,AT)
        self.data['jobs'].append({'id':'J2','film':'031','stage':'vo','status':'open'})
        h.check_completion(task,self.data,self.films,AT)
    def test_cancelled_or_completed_repair_does_not_silence_remaining_gap(self):
        for state in ['done','cancelled']:
            self.data['jobs']=[]
            h.reconcile(self.data,self.films,AT,jobs.do_add)
            self.data['jobs'][0]['status']=state
            self.assertEqual(len(h.reconcile(self.data,self.films,AT,jobs.do_add)),1)
    def test_finished_focus_stage_needs_successor_before_repair_closes(self):
        h.reconcile(self.data,self.films,AT,jobs.do_add);task=self.data['jobs'][0]
        self.films[0][1]['stages']['vo']['state']='done'
        h.check_completion(task,self.data,self.films,AT) # stage approval task resolved
        self.assertEqual(h.findings(self.data,self.films,AT)[0]['kind'],'missing-next-step')
    def test_bad_file_is_reported_not_silently_skipped(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            p=pathlib.Path(root)/'031_Test';p.mkdir();(p/'status.json').write_text('{')
            self.assertEqual(h.findings(self.data,list(h.records(root)),AT)[0]['kind'],'invalid-record')


class RecheckBackoff(unittest.TestCase):
    """Ben, 4 Nov 2026: hourly re-checks of the same held jobs crowded out video work."""
    def held(self):
        return {'id':'J1','title':'held job','status':'blocked','hold':{'type':'input','condition':'x','check_at':(AT-dt.timedelta(minutes=5)).isoformat()}}
    def check(self,i,hours_ago):
        t=(AT-dt.timedelta(hours=hours_ago)).strftime('%Y-%m-%dT%H:%MZ')
        return {'id':'V%d'%i,'status':'done','recheck_of':'J1','history':[{'at':t,'by':'codex','what':'done: still unmet'}]}
    def test_first_check_is_not_delayed(self):
        data={'jobs':[self.held()],'next_id':10}
        self.assertEqual(len(jobs.reconcile_holds(data,AT)),2)
    def test_waits_double_after_each_unchanged_check(self):
        # 1 check 30 min ago -> wait 1 h: no new task
        data={'jobs':[self.held(),self.check(1,0.5)],'next_id':10}
        self.assertEqual(jobs.reconcile_holds(data,AT),[])
        # 3 checks, last 3 h ago -> wait 4 h: no new task
        data={'jobs':[self.held(),self.check(1,9),self.check(2,6),self.check(3,3)],'next_id':10}
        self.assertEqual(jobs.reconcile_holds(data,AT),[])
        # 3 checks, last 5 h ago -> due
        data={'jobs':[self.held(),self.check(1,11),self.check(2,8),self.check(3,5)],'next_id':10}
        self.assertEqual(len(jobs.reconcile_holds(data,AT)),2)
    def test_wait_caps_at_24h(self):
        checks=[self.check(i,26+i) for i in range(1,8)]+[self.check(9,25)]
        data={'jobs':[self.held()]+checks,'next_id':20}
        self.assertEqual(len(jobs.reconcile_holds(data,AT)),2)
    def test_finished_predecessor_skips_the_wait(self):
        parent=self.held();parent['after']='J0'
        pre={'id':'J0','title':'pre','status':'done','history':[{'at':(AT-dt.timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%MZ'),'by':'codex','what':'done'}]}
        data={'jobs':[parent,pre,self.check(1,0.5)],'next_id':10}
        self.assertEqual(len(jobs.reconcile_holds(data,AT)),2)

if __name__=='__main__':unittest.main()

class ChiefCompletion(unittest.TestCase):
    def test_explicit_chief_ruling_is_required_and_survives_release(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root, patch.object(jobs.studio,'FILMS',pathlib.Path(root)):
            p=pathlib.Path(root)/'031_Test';p.mkdir()
            record={'stages':{'vo':{'state':'review'}},'claims':[]}
            jobs.studio.save(p/'status.json',record)
            task={'id':'J1','film':'031','stage':'vo','kind':'chief','eta':(AT+dt.timedelta(hours=1)).isoformat(),'title':'voice review'}
            self.assertIsNone(jobs.board_claim(task,'codex',AT))
            with self.assertRaises(ValueError):jobs.check_board_completion(task,'evidence')
            record=jobs.studio.load(p/'status.json');record['stages']['vo']['state']='done';jobs.studio.save(p/'status.json',record)
            with self.assertRaises(ValueError):jobs.check_board_completion(task,'')
            jobs.check_board_completion(task,'approval-evidence')
            jobs.board_release(task,'codex','review','approval-evidence')
            result=jobs.studio.load(p/'status.json')
            self.assertEqual(result['stages']['vo']['state'],'done')
            self.assertEqual(result['stages']['vo']['ref'],'approval-evidence')
            self.assertEqual(result['claims'],[])

class Timestamps(unittest.TestCase):
    def test_producer_formats_are_accepted_in_claims_and_ordering(self):
        for value in ['2026-11-03T12:00Z','2026-11-03T12:00:00Z','2026-11-03T12:00:00+00:00','2026-11-03T13:00:00+01:00']:
            self.assertEqual(jobs.studio.parse(value),AT)
        self.assertEqual(jobs.studio.parse('2026-11-03T12:00:00.500Z').microsecond,500000)
        with self.assertRaises(ValueError):jobs.studio.parse('invalid')
    def test_repair_inherits_focus_priority_without_claiming_stage(self):
        data={'next_id':1,'jobs':[],'focus':['031']}
        films=[('031',{'stages':{'vo':{'state':'review'}}})]
        h.reconcile(data,films,AT,jobs.do_add)
        repair=data['jobs'][0]
        other={'id':'J9','film':'032','created_at':'2026-10-01T12:00Z'}
        self.assertLess(w.order(repair,{},['031'],AT),w.order(other,{},['031'],AT))
        self.assertNotIn('due',repair) # never manufacture a production deadline

class LegacyDependencyHolds(unittest.TestCase):
    def test_overdue_dependency_without_after_still_requests_verification(self):
        job={'id':'J1213','title':'HOS008 edit','status':'blocked','hold':{'type':'dependency','condition':'Wait for J1218 repairs','check_at':'2026-10-30T15:00:00Z'}}
        self.assertTrue(w.hold_due(job,{'J1213':job},AT))
        data={'jobs':[job],'next_id':2000}
        ids=jobs.reconcile_holds(data,AT)
        self.assertEqual(len(ids),2)
        self.assertEqual(job['status'],'blocked')
        self.assertEqual(data['jobs'][-1]['recheck_of'],'J1213')
        self.assertEqual(jobs.reconcile_holds(data,AT),[])
    def test_future_dependency_check_does_not_release_work(self):
        job={'id':'J1','status':'blocked','hold':{'type':'dependency','check_at':(AT+dt.timedelta(hours=1)).isoformat()}}
        self.assertFalse(w.hold_due(job,{'J1':job},AT))
