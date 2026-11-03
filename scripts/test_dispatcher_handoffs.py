"""Dispatcher regressions: useful work survives retry, capability and worker failures."""
import copy
import datetime as dt
import json
import pathlib
import re
import tempfile
import unittest
from unittest.mock import patch
from contextlib import ExitStack
import chief_relay as cr
import jobs
import workflow_state as w

AT = dt.datetime(2026, 11, 3, 19, 30, tzinfo=dt.timezone.utc)
def row(i, **kw):
    return dict(id=i, title=i, status='open', needs='mini', created_at=AT.isoformat(), history=[], **kw)
def choose(j, up):
    return 'codex' if 'codex' in up else next(iter(sorted(up)), '')
def report(*available, at=AT):
    return {'at':at.isoformat(), 'expiresAt':(at+dt.timedelta(minutes=30)).isoformat(),
            'available':list(available), 'evidence':'Observed local input-tool probe, fixture'}

class Capabilities(unittest.TestCase):
    def test_online_worker_without_input_cannot_claim_or_displace_useful_job(self):
        media=row('MEDIA', kind='qa', required_capabilities=['audio_input'])
        work=row('WORK', kind='assembly')
        caps={'codex':report(), 'gemini':report()}
        data={'jobs':[media,work]}
        pick=w.select_dispatch(data,AT,'codex',{'codex','gemini'},choose,capabilities=caps)
        self.assertEqual(pick['job']['id'],'WORK')
        snap=w.snapshot(data,AT,'codex',{'codex','gemini'},choose,capabilities=caps)
        self.assertEqual(snap['states']['MEDIA']['state'],'waiting')
        self.assertIn('audio_input',snap['states']['MEDIA']['reason'])
        self.assertEqual(snap['counts']['queued'],1)
        with patch.object(cr,'worker_capabilities',return_value=caps):
            self.assertIsNone(jobs.choose_next({'jobs':[media]},'codex',{'mini'},AT,'MEDIA'))

    def test_eligible_fallback_is_chosen_before_routing_not_after_first_worker_fails(self):
        media=row('MEDIA', required_capabilities=['audio_input'])
        caps={'codex':report(), 'gemini':report('audio_input')}
        pick=w.select_dispatch({'jobs':[media]},AT,'codex',{'codex','gemini'},choose,capabilities=caps)
        self.assertEqual(pick['worker'],'gemini')
        immediate={**media,'urgent':1,'due':AT.isoformat(),'due_kind':'user-immediate-claim'}
        self.assertEqual(w.select_dispatch({'jobs':[immediate]},AT,'codex',{'codex','gemini'},choose,capabilities=caps)['worker'],'gemini')

    def test_expired_future_long_lived_or_evidenceless_report_cannot_enable_review(self):
        j=row('MEDIA', required_capabilities=['audio_input'])
        for r in [report('audio_input',at=AT-dt.timedelta(hours=1)), report('audio_input',at=AT+dt.timedelta(minutes=1)),
                  {**report('audio_input'),'expiresAt':(AT+dt.timedelta(days=1)).isoformat()},
                  {**report('audio_input'),'evidence':''}]:
            self.assertFalse(w.claimable(j,[j],AT,'gemini','codex',capabilities={'gemini':r}))

    def test_chief_authority_does_not_fallback_to_a_capable_non_chief(self):
        j=row('CHIEF',kind='chief',required_capabilities=['audio_input'])
        caps={'codex':report(),'gemini':report('audio_input')}
        self.assertIsNone(w.select_dispatch({'jobs':[j]},AT,'codex',{'codex','gemini'},choose,capabilities=caps))
        caps['codex']=report('audio_input')
        self.assertEqual(w.select_dispatch({'jobs':[j]},AT,'codex',{'codex','gemini'},choose,capabilities=caps)['worker'],'codex')

    def test_capability_hold_creates_one_gated_recheck_without_releasing_parent(self):
        parent={**row('PARENT'),'status':'blocked','by':'codex'}
        with patch.object(cr,'is_elected_chief',return_value=True):
            jobs.set_wait(parent,'codex',AT,{'type':'capability','condition':'Actual audio input unavailable',
                'requires':['audio_input'],'check_at':AT.isoformat()})
        data={'jobs':[parent],'next_id':1}
        jobs.reconcile_holds(data,AT)
        check=data['jobs'][1]
        self.assertEqual(check['required_capabilities'],['audio_input'])
        self.assertIsNone(w.select_dispatch(data,AT,'codex',{'codex'},choose))
        self.assertEqual(parent['status'],'blocked')
        self.assertEqual(w.select_dispatch(data,AT,'codex',{'codex'},choose,capabilities={'codex':report('audio_input')})['job']['id'],check['id'])
        before=copy.deepcopy(data);jobs.reconcile_holds(data,AT+dt.timedelta(hours=2))
        self.assertEqual(before,data)

    def test_pending_legacy_check_gains_requirement_when_parent_hold_is_typed(self):
        parent={**row('PARENT'),'status':'blocked','hold':{'type':'capability','requires':['audio_input'],
            'condition':'No listening input','check_at':(AT+dt.timedelta(hours=6)).isoformat()}}
        check=row('CHECK',kind='chief',recheck_of='PARENT')
        data={'jobs':[parent,check],'next_id':10}
        self.assertEqual(jobs.reconcile_holds(data,AT),['CHECK'])
        self.assertEqual(check['required_capabilities'],['audio_input'])
        self.assertEqual(len(data['jobs']),2)

    def test_stranded_rerouted_worker_uses_a_capable_fallback_without_changing_named_tasks(self):
        routed=row('R',kind='assembly',required_capabilities=['audio_input'],rerouted_from={'for':'claude'},**{'for':'codex'})
        named=row('N',kind='assembly',required_capabilities=['audio_input'],**{'for':'codex'})
        caps={'codex':report(),'gemini':report('audio_input')}
        with patch.object(cr,'worker_capabilities',return_value=caps):
            self.assertEqual(cr.stranded_jobs({'jobs':[routed,named]},{'codex','gemini'},AT),[routed])
            with patch.object(cr,'workers_up',return_value={'codex','gemini'}),patch.object(cr,'read_json',return_value={'jobs':[routed]}),\
                 patch.object(cr,'reroute',return_value=True) as reroute:
                cr.walk_on(routed,'codex','',AT)
                self.assertEqual(reroute.call_args.args[1],'gemini')

    def test_publisher_and_direct_claim_agree_on_capability_wait_and_recovery(self):
        import board_publish as bp
        media=row('MEDIA',required_capabilities=['audio_input'])
        board={'models':{'chief':{'agent':'codex'},'chiefChain':[{'agent':'codex','up':True},{'agent':'gemini','up':True}]}}
        with tempfile.TemporaryDirectory() as tmp:
            q=pathlib.Path(tmp)/'queue.json';q.write_text(json.dumps({'jobs':[media]}))
            with patch.object(cr,'worker_capabilities',return_value={}),patch.object(cr,'current_execution',return_value=None):
                self.assertIsNone(bp.dispatch_snapshot(board,AT,q)['next'])
                self.assertIsNone(jobs.choose_next({'jobs':[media]},'codex',{'mini'},AT))
            with patch.object(cr,'worker_capabilities',return_value={'gemini':report('audio_input')}),patch.object(cr,'current_execution',return_value=None):
                self.assertEqual(bp.dispatch_snapshot(board,AT,q)['next']['worker'],'gemini')
                self.assertEqual(jobs.choose_next({'jobs':[media]},'gemini',{'mini'},AT)['id'],'MEDIA')

    def test_bad_requirement_is_rejected_before_add_or_hold_mutates(self):
        data={'jobs':[],'next_id':1};before=copy.deepcopy(data)
        with self.assertRaises(ValueError):jobs.do_add(data,title='x',needs='mini',body='',by='codex',at=AT,requires=['not a tool'])
        self.assertEqual(data,before)
        j={**row('P'),'status':'claimed','by':'codex'};before=copy.deepcopy(j)
        with self.assertRaises(ValueError):jobs.set_wait(j,'codex',AT,{'type':'capability','check_at':AT.isoformat(),'condition':'No tools'})
        self.assertEqual(j,before)

    def test_capability_report_is_bounded_and_can_record_no_input(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(cr,'STATE',pathlib.Path(tmp)):
            cr.record_capabilities('codex','','actual observed lack of audio-input tool',30,AT)
            self.assertEqual(cr.worker_capabilities()['codex']['available'],[])
            for minutes in [0,61]:
                with self.assertRaises(ValueError):cr.record_capabilities('codex','audio_input','probe',minutes,AT)

class Priority(unittest.TestCase):
    def test_released_overdue_job_yields_to_other_work(self):
        retry=row('RETRY',due='2026-10-01T00:00Z')
        retry['history']=[{'at':AT.isoformat(),'what':'released: missing input, retry later'}]
        work=row('WORK')
        self.assertEqual(w.select_dispatch({'jobs':[retry,work]},AT,'codex',{'codex'},choose)['job']['id'],'WORK')

    def test_synthetic_check_deadline_does_not_outrank_real_production(self):
        parent={**row('P'),'status':'blocked','hold':{'condition':'Not ready'}}
        check=row('CHECK',kind='chief',recheck_of='P',due_kind='condition-verification',due='2026-10-01T00:00Z')
        work=row('WORK',kind='assembly')
        data={'jobs':[parent,check,work]}
        self.assertEqual(w.select_dispatch(data,AT,'codex',{'codex'},choose)['job']['id'],'WORK')
        parent['due']='2026-11-03T19:35Z'
        self.assertEqual(w.select_dispatch(data,AT,'codex',{'codex'},choose)['job']['id'],'CHECK')

class RelayContinuation(unittest.TestCase):
    def exercise(self, failure=False, leave_claim=False, recover_failure=False):
        with tempfile.TemporaryDirectory() as tmp,ExitStack() as stack:
            root=pathlib.Path(tmp);(root/'jobs').mkdir();q=root/'jobs/queue.json'
            data={'jobs':[row('RETRY',kind='assembly',due='2026-10-01T00:00Z'),row('WORK',kind='assembly')]}
            q.write_text(json.dumps(data));ran=[]
            for name,value in [('OWB',root),('STATE',root/'state')]:stack.enter_context(patch.object(cr,name,value))
            for name in ['note_grok_posts','fetch_claude_beat','handover','alert_no_chief','publish_chief_inbox','push_heartbeat','notify','offload_scratch']:
                stack.enter_context(patch.object(cr,name))
            for name,value in [('load_out',{}),('self_heal',True),('reroute_work',[]),('pending_chief_reviews',[]),
                ('chief_delivery_overdue',False),('keep_busy',[]),('queue_has_work',True)]:
                stack.enter_context(patch.object(cr,name,return_value=value))
            stack.enter_context(patch.object(cr.handoffs,'findings',return_value=[]))
            stack.enter_context(patch.object(cr,'now',return_value=AT))
            stack.enter_context(patch.object(cr,'acting',return_value=([('gemini',True,'fixture')],'gemini')))
            available={'codex','gemini'}
            stack.enter_context(patch.object(cr,'workers_up',side_effect=lambda at:set(available)))
            stack.enter_context(patch.object(cr,'mark_down',side_effect=lambda who,*a,**kw:available.discard(who)))
            def reroute(job,to,model,note):
                d=json.loads(q.read_text());j=next(j for j in d['jobs'] if j['id']==job['id'])
                jobs.do_reroute(j,'relay',to,model,note,AT)
                q.write_text(json.dumps(d));return True
            stack.enter_context(patch.object(cr,'reroute',side_effect=reroute))
            def run(who,prompt,cap,model):
                selected=re.search(r'DISPATCH PRIORITY: claim only (\w+)',prompt).group(1)
                ran.append((selected,who));d=json.loads(q.read_text());j=next(j for j in d['jobs'] if j['id']==selected)
                if recover_failure and selected=='RETRY':
                    if who=='codex':j.update(status='claimed',by=who,progress={'step':1,'of':4,'at':AT.isoformat()})
                    else:j['status']='done'
                elif selected=='RETRY':
                    if leave_claim:j.update(status='claimed',by=who,eta=(AT+dt.timedelta(minutes=30)).isoformat())
                    elif failure:
                        j.update(status='blocked',by=who,hold={'condition':'task failure; preserve original scope'})
                        j['history'].append({'at':AT.isoformat(),'by':who,'what':'blocked: task-local approval/input hold'})
                    else:j['history'].append({'at':AT.isoformat(),'what':'released: retry later'})
                else:j['status']='done'
                q.write_text(json.dumps(d))
                return (2,'local fixture failed') if (failure and selected=='RETRY') or (recover_failure and selected=='RETRY' and who=='codex') else (0,'done')
            stack.enter_context(patch.object(cr,'run_cli',side_effect=run))
            self.assertEqual(cr.run_locked(AT),0)
            return ran,json.loads(q.read_text())

    def test_released_job_does_not_stop_other_work_or_run_again_in_same_pass(self):
        ran,data=self.exercise()
        self.assertEqual([i for i,_ in ran],['RETRY','WORK'])
        self.assertEqual(data['jobs'][0]['status'],'open')

    def test_recorded_task_hold_does_not_bench_a_healthy_worker(self):
        ran,data=self.exercise(failure=True)
        self.assertEqual(ran,[('RETRY','codex'),('WORK','codex')])
        self.assertEqual(data['jobs'][0]['status'],'blocked')

    def test_unfinished_claim_remains_owned_and_is_not_abandoned(self):
        ran,data=self.exercise(leave_claim=True)
        self.assertEqual(len(ran),1)
        self.assertEqual(data['jobs'][0]['status'],'claimed')
        self.assertEqual(data['jobs'][1]['status'],'open')

    def test_failed_claim_is_handed_to_backup_immediately_with_progress_preserved(self):
        ran,data=self.exercise(recover_failure=True)
        self.assertEqual(ran,[('RETRY','codex'),('RETRY','gemini'),('WORK','gemini')])
        self.assertEqual(data['jobs'][0]['status'],'done')
        self.assertEqual(data['jobs'][0]['progress']['step'],1)

    def test_old_or_different_owner_hold_cannot_hide_current_worker_failure(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(cr,'OWB',pathlib.Path(tmp)):
            q=pathlib.Path(tmp)/'jobs/queue.json';q.parent.mkdir()
            for by,stamp in [('gemini',AT),('codex',AT-dt.timedelta(hours=1)),('codex',AT+dt.timedelta(hours=1))]:
                j={**row('R'),'status':'blocked','by':by,'history':[{'by':by,'at':stamp.isoformat(),'what':'blocked: old hold'}]}
                q.write_text(json.dumps({'jobs':[j]}))
                with patch.object(cr,'now',return_value=AT):
                    self.assertEqual(cr.recorded_task_outcome(j,'codex',AT),'')

if __name__=='__main__':unittest.main()
