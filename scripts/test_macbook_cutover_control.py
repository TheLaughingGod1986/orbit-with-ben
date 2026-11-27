"""Cross-machine protocol tests; process/service/Git/network adapter is mocked."""
import copy
import datetime as dt
import json
from pathlib import Path
import plistlib
import time
import unittest
from unittest.mock import patch
import macbook_cutover as m
import macbook_cutover_control as c
from test_macbook_cutover import FixtureBase

class Protocol(FixtureBase):
    def setUp(self):
        super().setUp()
        self.plan['authority_repo']='owner/old'; self.plan['thread']=1
        self.plan['production_sources']={'scripts/engine_guard.py':m.digest(b'guard')}
        for root in self.engines:
            (root/'scripts').mkdir()
            (root/'scripts/engine_guard.py').write_bytes(b'guard')
        self.path=self.root/'plan.json'
        # Match the real plan's digest and regenerate exact activation.
        self.plan.pop('plan_hash')
        self.path.write_bytes(m.canonical(self.plan)); self.path.chmod(0o600)
        self.sha=m.digest(self.path.read_bytes()); self.plan['plan_hash']=self.sha
        (self.root/'pause-identity.json').unlink(); self.pause.unlink()
        c.create_pause(self.plan,self.root)
        self.comment['body']=self.comment['body'].replace('a'*64,self.sha)
        self.activation=m.validate_activation(self.comment,self.plan,self.sha,time.time())
        m.private_write(self.root/'activation.json',m.canonical(self.activation))
        self.proposed=m.proposal(self.installed.read_bytes(),self.plan['engines'],self.plan['production_url'])
        self.installed.write_bytes(self.proposed)
        doc=plistlib.loads(self.proposed)
        self.loaded=('arguments = {\n'+'\n'.join(doc['ProgramArguments'])+'\n}\nenvironment = {\n'
            +'\n'.join(k+' => '+v for k,v in doc['EnvironmentVariables'].items())+'\n}\n').encode()
        Path(self.plan['marker']).write_bytes(m.canonical({'version':1,'github':self.plan['production_repo']}))
        m.private_write(self.root/'result.json',m.canonical({'status':'installed-paused'}))
        self.rows=[self.comment]; self.sent=[]; self.commands=[]
        self.io.comments=lambda p: self.rows[:]
        self.io.comment=lambda p,cid: next(x for x in self.rows if x['id']==cid)
        self.io.git=lambda root,*args: {'rev-parse':self.activation['commit'], 'branch':'main',
            'status':'', 'remote':self.plan['production_url']}[args[0]]
        self.io.run=lambda argv,**kwargs: self.commands.append(argv) or b''
        self.io.post=self.post
        # ANY accidental use of real adapters/process creation fails the test.
        self.addCleanup(patch.stopall)
        patch.object(m.subprocess,'run',side_effect=AssertionError('live process forbidden')).start()
        patch.object(m.subprocess,'Popen',side_effect=AssertionError('live process forbidden')).start()

    def post(self,plan,body):
        self.sent.append(body)
        self.rows.append(dict(self.comment,id=1000+len(self.sent),body=body,updated_at=self.comment['created_at']))

    def control(self,verb='RESUME',**overrides):
        row=dict(self.comment,id=77,body=f"[Chief] MACBOOK-{verb} coordinator={self.plan['job']} nonce={self.plan['nonce']} plan={self.sha} commit={self.activation['commit']} activation={self.activation['id']} activation-sha256={self.activation['hash']} chief=codex elected=confirmed global-freeze=confirmed")
        row.update(overrides)
        return row

    def tick(self): c.tick(self.path,self.sha,self.io)

    def test_success_waits_for_explicit_resume_and_releases_both_slot_pause(self):
        self.tick(); self.assertTrue(self.pause.exists())
        self.rows.append(self.control()); self.tick()
        self.assertFalse(self.pause.exists())
        self.assertTrue((self.root/'resumed.json').exists())
        result=json.loads(self.sent[-1].split('MACBOOK-RESULT ')[1])
        self.assertEqual((result['status'],result['chief'],result['request']),('resumed','codex',77))
        self.assertEqual(set(result),{'status','job','nonce','plan','commit','activation','activation_sha256','source_sha256','receipt_sha256','request','chief'})
        for body in self.sent:
            self.assertNotIn(str(self.root),body); self.assertNotIn('arguments',body)
        count=len(self.sent); self.tick(); self.tick()
        self.assertEqual(len(self.sent),count+1) # final base receipt once, then deduplicated
        self.assertEqual(self.commands,[]) # no worker kill/restart; normal launcher owns both slots

    def test_rejects_untrusted_stale_edited_mismatched_and_wrong_thread(self):
        bad=[{'author_association':'NONE'},{'user':{'type':'Bot'}},{'issue_url':'other'},
             {'updated_at':'changed'},{'created_at':'2020-01-01T00:00:00Z','updated_at':'2020-01-01T00:00:00Z'}]
        for delta in bad:
            with self.subTest(delta=delta):
                self.rows=[self.comment,self.control(**delta)]; self.tick(); self.assertTrue(self.pause.exists())
        for old,new in [(self.sha,'0'*64),(self.activation['commit'],'0'*40),('nonce=abc','nonce=wrong'),('activation=42','activation=43'),('elected=confirmed','elected=no')]:
            row=self.control(); row['body']=row['body'].replace(old,new)
            self.rows=[self.comment,row]; self.tick(); self.assertTrue(self.pause.exists())

    def test_delivery_failure_retains_pause_then_recovers(self):
        self.io.post=lambda p,b: (_ for _ in ()).throw(m.Refused('network'))
        self.rows.append(self.control())
        with self.assertRaises(m.Refused): self.tick()
        self.assertTrue(self.pause.exists())
        self.io.post=self.post; self.tick(); self.assertFalse(self.pause.exists())

    def test_ambiguous_post_is_read_back_without_duplicate(self):
        def ambiguous(p,b): self.post(p,b); raise m.Refused('ambiguous')
        self.io.post=ambiguous
        with self.assertRaises(m.Refused): self.tick()
        self.io.post=self.post; self.tick()
        self.assertEqual(len(self.sent),1); self.assertTrue(self.pause.exists())

    def test_empty_user_pause_is_never_owned(self):
        with self.assertRaises(FileExistsError): c.create_pause(self.plan,self.root)
        self.pause.write_bytes(b'')
        self.rows.append(self.control()); self.tick()
        self.assertTrue(self.pause.exists()); self.assertEqual(self.pause.read_bytes(),b'')
        self.assertIn('stopped-paused',self.sent[-1])

    def test_replaced_identical_pause_is_not_removed(self):
        token=self.pause.read_bytes(); self.pause.unlink(); self.pause.write_bytes(token)
        self.rows.append(self.control()); self.tick()
        self.assertTrue(self.pause.exists())

    def test_source_service_marker_production_head_drift(self):
        for which in ['source','service','marker','head','production']:
            with self.subTest(which=which):
                with patch.object(c,'verify_install',wraps=c.verify_install):
                    original=self.installed.read_bytes(); marker=Path(self.plan['marker']); old_marker=marker.read_bytes()
                    git=self.io.git; production=self.io.production
                    if which=='source': (self.engines[0]/'scripts/engine_guard.py').write_bytes(b'drift')
                    if which=='service': self.installed.write_bytes(b'drift')
                    if which=='marker': marker.write_bytes(b'{}')
                    if which=='head': self.io.git=lambda root,*a: 'drift' if a[0]=='rev-parse' else git(root,*a)
                    if which=='production': self.io.production=lambda *a: m.require(False,'production changed')
                    row=self.control(); row['id']=80+len(self.sent); self.rows=[self.comment,row]; self.tick()
                    self.assertTrue(self.pause.exists())
                    self.installed.write_bytes(original); marker.write_bytes(old_marker)
                    (self.engines[0]/'scripts/engine_guard.py').write_bytes(b'guard')
                    self.io.git=git; self.io.production=production

    def test_held_second_slot_lock_refuses_resume(self):
        with self.locks[1].open('r+') as f:
            m.fcntl.flock(f,m.fcntl.LOCK_EX|m.fcntl.LOCK_NB)
            self.rows.append(self.control()); self.tick()
            self.assertTrue(self.pause.exists())
            self.assertTrue(self.locks[1].exists())

    def test_expired_supervisor_after_switch_recovers_then_separate_resume(self):
        # No result was written before timeout. Service switched, marker missing.
        (self.root/'result.json').unlink(); Path(self.plan['marker']).unlink()
        with patch.object(c.time,'time',return_value=self.plan['deadline']+1):
            # Fresh command at recovery time, independently of expired install budget.
            now=dt.datetime.fromtimestamp(self.plan['deadline']+0.5,dt.timezone.utc).isoformat()
            self.rows.append(self.control('RECOVER',created_at=now,updated_at=now))
            self.tick(); self.assertTrue(self.pause.exists())
            self.assertTrue((self.root/'verified-install.json').exists())
            self.assertIn('expired-paused',self.sent[0])
            resume=self.control(created_at=now,updated_at=now); resume['id']=78
            self.rows.append(resume); self.tick(); self.assertFalse(self.pause.exists())

    def test_expired_before_activation_reports_without_install(self):
        (self.root/'activation.json').unlink(); (self.root/'result.json').unlink()
        with patch.object(c.time,'time',return_value=self.plan['deadline']+1): self.tick()
        self.assertIn('expired-paused',self.sent[0]); self.assertTrue(self.pause.exists())
        self.assertEqual(self.commands,[])

    def test_expired_without_activation_accepts_new_authority_without_install(self):
        (self.root/'activation.json').unlink(); (self.root/'result.json').unlink()
        now=dt.datetime.fromtimestamp(self.plan['deadline']+0.5,dt.timezone.utc).isoformat()
        fresh=dict(self.comment,id=43,created_at=now,updated_at=now)
        self.rows=[fresh]
        with patch.object(c.time,'time',return_value=self.plan['deadline']+1): self.tick()
        self.assertTrue((self.root/'activation.json').exists())
        self.assertTrue(self.pause.exists()); self.assertEqual(self.commands,[])
        self.assertIn('expired-paused',self.sent[-1])

    def test_failed_bootstrap_explicit_recovery_keeps_pause(self):
        def unloaded():
            if not self.commands: raise m.Refused('unloaded')
            return self.loaded
        self.io.loaded=unloaded
        self.rows.append(self.control('RECOVER')); self.tick()
        self.assertEqual(self.commands[0][1],'bootstrap'); self.assertTrue(self.pause.exists())
        self.assertIn('installed-paused',self.sent[-1])

    def test_no_automatic_restore_or_resume_on_failed_recovery(self):
        self.io.loaded=lambda: (_ for _ in ()).throw(m.Refused('unloaded'))
        self.rows.append(self.control('RECOVER')); self.tick()
        self.assertTrue(self.pause.exists()); self.assertIn('stopped-paused',self.sent[-1])
        count=len(self.commands); self.tick(); self.assertEqual(len(self.commands),count)
        self.assertTrue((self.root/'failure-77.json').exists())

    def test_resume_readback_mutation_is_refused(self):
        row=self.control(); self.rows.append(row)
        original=self.io.comment
        def changed(plan,cid):
            value=copy.deepcopy(original(plan,cid))
            if cid==77: value['updated_at']='changed'
            return value
        self.io.comment=changed
        with self.assertRaises(m.Refused): self.tick()
        self.assertTrue(self.pause.exists())

    def test_registration_is_independent_and_finite_process_no_keepalive(self):
        names = {'macbook_cutover.py', 'macbook_cutover_control.py', 'engine_guard.py',
            'macbook/render_worker_plist.py', 'macbook/' + m.render_worker_plist.TEMPLATE.name}
        self.plan['control_bundle'] = {name:m.digest(b'fixture') for name in names}
        for name in names:
            p = self.root/'control'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b'fixture')
        with patch.object(c,'read_plan',return_value=self.plan): c.arm(self.path,self.sha,self.plan,self.io)
        doc=plistlib.loads((self.root/'recovery.plist').read_bytes())
        self.assertEqual(doc['StartInterval'],180); self.assertNotIn('KeepAlive',doc)
        self.assertEqual([a[1] for a in self.commands],['bootstrap','print'])
        self.assertIn('tick',doc['ProgramArguments'])

    def test_timeout_before_replacement_can_finish_exact_new_service(self):
        original=(self.attempt/'original')
        # Original plist reconstructed from fixture; all service effects mocked.
        old=plistlib.loads(self.proposed)
        old['ProgramArguments']=['old']
        old['EnvironmentVariables'].pop('STUDIO_REPO'); old['EnvironmentVariables'].pop('STUDIO_GIT_URL')
        data=plistlib.dumps(old)
        self.plan['installed_hash']=m.digest(data)
        self.installed.write_bytes(data)
        self.loaded=('arguments = {\nold\n}\nenvironment = {\n'+
            '\n'.join(k+' => '+v for k,v in old['EnvironmentVariables'].items())+'\n}\n').encode()
        Path(self.plan['marker']).unlink()
        (self.root/'result.json').unlink()
        def replace(plan, proposed, attempt):
            self.installed.write_bytes(proposed)
            doc=plistlib.loads(proposed)
            self.loaded=('arguments = {\n'+'\n'.join(doc['ProgramArguments'])+'\n}\nenvironment = {\n'+
                '\n'.join(k+' => '+v for k,v in doc['EnvironmentVariables'].items())+'\n}\n').encode()
        self.io.replace=replace
        # Plan hash must remain exact; update only mocked original bytes to its
        # original hash (fixture's original plist serialization is identical).
        self.assertEqual(m.digest(data),json.loads(self.path.read_bytes())['installed_hash'])
        self.rows.append(self.control('RECOVER')); self.tick()
        self.assertTrue(self.pause.exists()); self.assertIn('installed-paused',self.sent[-1])
        self.assertTrue(Path(self.plan['marker']).exists())

    def test_lost_final_response_does_not_repeat_resume(self):
        self.rows.append(self.control())
        def lose(p,b):
            self.post(p,b)
            if '"status":"resumed"' in b: raise m.Refused('response lost')
        self.io.post=lose
        with self.assertRaises(m.Refused): self.tick()
        self.assertFalse(self.pause.exists())
        self.io.post=self.post; self.tick()
        self.assertFalse(self.pause.exists()); self.assertIn('resumed',self.sent[-1])

    def test_tick_has_real_wall_budget_not_launchd_timeout_assumption(self):
        with patch.object(c.sys,'argv',['control','tick','--plan',str(self.path),'--sha256',self.sha]), patch.object(c.subprocess,'run') as run:
            c.main()
            self.assertEqual(run.call_args.kwargs['timeout'],75)
            self.assertEqual(run.call_args.kwargs['stdin'],c.subprocess.DEVNULL)
            self.assertIn('tick-run',run.call_args.args[0])

    def test_changed_activation_preserves_remote_status_but_cannot_resume(self):
        self.comment['updated_at']='edited'
        row=self.control('STATUS'); row['updated_at']=row['created_at']
        self.rows.append(row); self.tick()
        self.assertTrue(self.pause.exists()); self.assertIn('stopped-paused',self.sent[-1])
        row=self.control(); row['id']=78; row['updated_at']=row['created_at']; self.rows.append(row); self.tick()
        self.assertTrue(self.pause.exists())

    def test_post_uses_structured_stdin_no_shell(self):
        io=m.System(); calls=[]
        io.run=lambda args,**kw: calls.append((args,kw))
        io.post(self.plan,'literal `text` $(never-execute)')
        self.assertEqual(calls[0][0][-2:],['--input','-'])
        self.assertEqual(json.loads(calls[0][1]['input'])['body'],'literal `text` $(never-execute)')

if __name__=='__main__': unittest.main()
