"""Ben, 26 Oct: Grok -> Claude -> Codex -> Gemini, with real role authority and recovery."""
import contextlib
import datetime as dt
import io
import json
import os
from pathlib import Path
import unittest
from unittest import mock

import test_chief_relay as fixture
import chief_relay as cr
import jobs
import board_publish as bp

T0, MIN = fixture.T0, fixture.MIN


class ChiefSuccession(unittest.TestCase):
    fake = fixture.Relay.fake
    ran = fixture.Relay.ran
    beat = fixture.Relay.beat
    chief = fixture.Relay.chief
    routed_queue = fixture.Relay.routed_queue

    def setUp(self):
        fixture.Relay.setUp(self)
        self.addCleanup(fixture.Relay.tearDown, self)
        os.environ.pop('CHIEF_CHAIN', None)
        patch = mock.patch.object(cr, 'now', return_value=T0)
        patch.start()
        self.addCleanup(patch.stop)

    def queue(self, rows):
        self.routed_queue(json.dumps({'next_id': 100, 'jobs': rows}))

    def test_default_order_and_each_successor(self):
        self.assertEqual(cr.chain(), ['chief', 'claude', 'codex', 'gemini'])
        self.assertEqual(self.chief(), 'codex')
        self.beat(T0 - 5 * MIN)
        self.assertEqual(self.chief(), 'claude')
        cr.seen('chief', T0)
        self.assertEqual(self.chief(), 'chief')
        cr.mark_down('chief', 'credit exhausted', None, T0)
        self.assertEqual(self.chief(), 'claude')
        self.beat(T0 - 100 * MIN)
        self.assertEqual(self.chief(), 'codex')
        cr.mark_down('codex', 'usage limit', T0 + 60 * MIN, T0)
        self.assertEqual(self.chief(), 'gemini')
        self.assertTrue(cr.state_of('cursor', T0)[0])  # available Cursor does not enter succession

    def test_recovery_hands_back_in_priority_order_without_manual_switches(self):
        cr.mark_down('codex', 'usage limit', T0 + 60 * MIN, T0)
        self.assertEqual(self.chief(), 'gemini')
        self.assertEqual(self.chief(T0 + 61 * MIN), 'codex')
        self.beat(T0 + 60 * MIN)
        self.assertEqual(self.chief(T0 + 62 * MIN), 'claude')
        cr.seen('chief', T0 + 63 * MIN)
        self.assertEqual(self.chief(T0 + 64 * MIN), 'chief')

    def test_a_new_claude_heartbeat_clears_its_old_down_mark_before_election(self):
        cr.mark_down('claude','usage limit',T0+120*MIN,T0-10*MIN)
        self.assertEqual(self.chief(),'codex')
        self.beat(T0-1*MIN)
        self.assertEqual(self.chief(),'claude')
        self.assertFalse(cr.d('down','claude.json').exists())

    def test_missing_codex_cli_uses_gemini_and_all_chiefs_out_does_not_elect_cursor(self):
        os.environ['CODEX_BIN'] = str(self.tmp / 'missing')
        os.environ['PATH'] = str(self.tmp / 'empty')
        self.assertEqual(self.chief(), 'gemini')
        cr.mark_down('gemini', 'usage limit', None, T0)
        self.assertIsNone(self.chief())
        self.assertTrue(cr.state_of('cursor', T0)[0])

    def test_gemini_can_review_when_codex_hits_usage_limit_in_the_same_run(self):
        self.queue([{'id':'J10','title':'Chief review of a finished pack','status':'blocked','needs':'any',
                     'result':'parked for Chief: inspect the rendered evidence','history':[]}])
        calls=[]
        def run(agent,prompt,cap,model):
            calls.append((agent,prompt,model))
            return (1,'Error: usage limit exceeded') if agent=='codex' else (0,'review recorded')
        with mock.patch.object(cr,'run_cli',side_effect=run), mock.patch.object(cr,'reroute_work',return_value=[]):
            cr.cmd_run(T0)
        self.assertEqual([c[0] for c in calls], ['codex','gemini'])
        self.assertIn('ELECTED ACTING CHIEF', calls[1][1])
        self.assertIn('CHIEF REVIEW PRIORITY', calls[1][1])
        self.assertIn('J10',calls[1][1])
        self.assertEqual(calls[1][2],'gemini-argon')
        self.assertEqual(self.chief(),'gemini')

    def test_generic_failure_of_the_elected_chief_also_yields_in_the_same_run(self):
        calls=[]
        def run(agent,prompt,cap,model):
            calls.append(agent)
            return (2,'unexpected CLI failure') if agent=='codex' else (0,'done')
        with mock.patch.object(cr,'run_cli',side_effect=run), mock.patch.object(cr,'reroute_work',return_value=[]):
            cr.cmd_run(T0)
        self.assertEqual(calls,['codex','gemini'])

    def test_a_specialist_worker_does_not_receive_chief_authority(self):
        self.queue([{'id':'J10','title':'Independent Cursor opinion','status':'open','needs':'any','for':'cursor','history':[]}])
        calls=[]
        with mock.patch.object(cr,'run_cli',side_effect=lambda agent,prompt,cap,model: (calls.append((agent,prompt)) or (0,'done'))):
            cr.cmd_run(T0)
        self.assertEqual(calls[0][0],'cursor')
        self.assertIn('You are a WORKER, not the elected Chief',calls[0][1])
        self.assertNotIn('You are the ELECTED ACTING CHIEF',calls[0][1])

    def test_unready_addressed_work_cannot_displace_a_ready_chief_review(self):
        self.queue([{'id':'J1','status':'blocked','needs':'any','result':'wait for input'},
                    {'id':'J2','status':'open','needs':'any','for':'gemini','after':'J1'},
                    {'id':'J3','status':'blocked','needs':'any','title':'Review result','result':'parked for Chief: ready'}])
        self.assertEqual(cr.addressed_to('gemini'),[])
        calls=[]
        with mock.patch.object(cr,'run_cli',side_effect=lambda agent,prompt,cap,model:(calls.append((agent,prompt)) or (0,'done'))), mock.patch.object(cr,'reroute_work',return_value=[]):
            cr.cmd_run(T0)
        self.assertEqual(calls[0][0],'codex')
        self.assertIn('CHIEF REVIEW PRIORITY: before taking an ordinary job, review J3',calls[0][1])

    def test_date_credit_and_ben_holds_are_not_reopened_as_reviews(self):
        self.queue([{'id':'J1','status':'blocked','needs':'any','result':'parked for Chief: waits for long public; reopen when public'},
                    {'id':'J2','status':'blocked','needs':'any','result':'parked for Chief: wait for credit reset'},
                    {'id':'J3','status':'blocked','needs':'ben','result':'parked for Chief: sign in'},
                    {'id':'J4','status':'blocked','needs':'any','awaits_ben':{'version':'v1'},'result':'parked for Chief: watch'},
                    {'id':'J5','status':'blocked','needs':'any','result':'parked for Chief: audio gate FAIL; decide correction'}])
        self.assertEqual([j['id'] for j in cr.pending_chief_reviews(T0)],['J5'])

    def test_only_elected_chief_can_claim_role_jobs_and_dependencies_still_hold(self):
        j={'id':'J1','title':'Merge reviewed change','kind':'chief','status':'open','needs':'cloud','for':'chief','history':[]}
        data={'jobs':[j]}
        self.assertTrue(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'codex'))
        self.assertFalse(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'cursor'))
        self.assertFalse(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'gemini'))
        cr.mark_down('codex','usage limit',None,T0)
        self.assertTrue(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'gemini'))
        j['needs']='ben'
        self.assertFalse(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'gemini'))
        j.update(needs='cloud',after='J0')
        data['jobs'].append({'id':'J0','status':'blocked'})
        self.assertFalse(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'gemini'))
        data['jobs'][-1]['status']='done'
        self.assertTrue(jobs.claimable(data,j,jobs.MINI_NEEDS,T0,'gemini'))

    def test_a_claimed_chief_job_hands_to_gemini_without_waiting_for_its_eta(self):
        j={'id':'J1','title':'Review','kind':'chief','status':'claimed','needs':'cloud','for':'chief','by':'codex',
           'history':[],'eta':'2026-10-07T14:00Z'}
        cr.mark_down('codex','usage limit',None,T0)
        jobs.do_reroute(j,'relay','gemini','gemini-argon','Chief failover',T0)
        self.assertEqual((j['status'],j['for']),('open','gemini'))
        self.assertTrue(jobs.claimable({'jobs':[j]},j,jobs.MINI_NEEDS,T0,'gemini'))
        with self.assertRaises(ValueError):jobs.do_reroute(j,'relay','cursor','','not Chief',T0)

    def test_status_does_not_call_gemini_worker_only(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):cr.cmd_status(T0)
        self.assertIn('gemini',out.getvalue())
        self.assertNotIn('never Chief',out.getvalue())
        self.assertIn('Chief fallback and facts checker',out.getvalue())

    def test_fresh_relay_status_beats_old_expired_usage_and_names_gemini(self):
        p=self.tmp/'board-chief';p.mkdir()
        (p/'chain.json').write_text(json.dumps({'at':cr.iso(T0),'rows':[{'agent':'codex','up':True,'why':'ready'}]}))
        (p/'runs.jsonl').write_text(json.dumps({'at':cr.iso(T0-120*MIN),'worker':'codex','out_of_usage':True})+'\n')
        (p/'current.json').write_text(json.dumps({'agent':'gemini','since':cr.iso(T0)}))
        result=bp.models_status(T0,state=p,flags_file=self.tmp/'absent.json')
        self.assertEqual(next(m for m in result['models'] if m['id']=='codex')['status'],'green')
        self.assertEqual(result['chief']['name'],'Gemini')
        self.assertEqual(result['chiefChain'][0]['name'],'Codex')
