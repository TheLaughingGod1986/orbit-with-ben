"""No live service/process/Git operations: the whole adapter is fake."""
import copy
import datetime as dt
import json
import os
from pathlib import Path
import plistlib
import tempfile
import time
import unittest
from unittest.mock import patch
import macbook_cutover as m

class FixtureBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.installed = self.root / 'installed'
        self.installed.write_bytes(plistlib.dumps({'Label': m.LABEL, 'ProgramArguments': ['old'],
             'EnvironmentVariables': {'MACBOOK_IDLE_MIN': '10', 'MACBOOK_SLOTS': '2', 'OWB_REPO': 'content-one'},
             'RunAtLoad': False, 'StartInterval': 180, 'Nice': 10}))
        self.loaded = b'arguments = {\n old\n}\nenvironment = {\n MACBOOK_IDLE_MIN => 10\n}\n'
        self.pause = self.root / 'pause'; self.pause.touch()
        self.locks = [self.root / 'lock1', self.root / 'lock2']
        for p in self.locks: p.touch()
        self.engines = [self.root / 'engine1', self.root / 'engine2']
        self.old = [self.root / 'old1', self.root / 'old2']
        for root in self.engines + self.old:
            (root / 'channels').mkdir(parents=True)
            (root / 'channels/channels.json').write_text(json.dumps({'studio': {'github': 'owner/studio' if root in self.engines else 'owner/old'}}))
        self.plan = {'job': 'J3999', 'nonce': 'abc', 'created': time.time()-10, 'deadline': time.time()+300,
            'plan_hash': 'a'*64, 'owners': [{'pid': 987001, 'pgid': 987001, 'start': 'old'},
                                         {'pid': 987002, 'pgid': 987002, 'start': 'old'}],
            'locks': list(map(str,self.locks)), 'engines': list(map(str,self.engines)),
            'old_engines': list(map(str,self.old)), 'installed': str(self.installed),
            'installed_hash': m.digest(self.installed.read_bytes()), 'sources': {str(self.installed): m.digest(self.installed.read_bytes())},
            'loaded_hash': m.digest(m.canonical(m.loaded_settings(self.loaded.decode()))),
            'pause': str(self.pause), 'marker': str(self.root/'marker'), 'cancel': str(self.root/'cancel'),
            'production_repo': 'owner/studio', 'production_url': 'https://github.com/owner/studio.git',
            'issue_url': 'https://api.github.com/repos/owner/old/issues/1'}
        self.plan['proposal_hash'] = m.digest(m.proposal(self.installed.read_bytes(), self.plan['engines'],self.plan['production_url']))
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        self.comment = {'id': 42, 'author_association': 'OWNER', 'user': {'type': 'User'},
            'issue_url': self.plan['issue_url'], 'created_at': now, 'updated_at': now,
            'body': '[Chief] MACBOOK-CUTOVER J3892 coordinator=J3999 abc '+ 'a'*64 +' chief=codex commit='+ 'b'*40 +' queue='+ 'c'*64 +' global-freeze=confirmed'}
        self.activation = m.validate_activation(self.comment,self.plan,self.plan['plan_hash'],time.time())
        outer = self
        class Fake:
            def __init__(self): self.calls=[]; self.rows=[]; self.jobs=[{'id':'J3999','status':'done'}]; self.race=None
            def queue(self,p): return self.jobs
            def processes(self): return self.rows
            def loaded(self): return outer.loaded
            def comment(self,p,cid): return outer.comment
            def comments(self,p): return [outer.comment]
            def production(self,p,a): self.calls.append('production')
            def update_engine(self,*args):
                self.calls.append('engine')
                if self.race: self.race()
            def replace(self,*args): self.calls.append('replace'); return b'new loaded'
        self.io=Fake()
        self.attempt=self.root/'attempt'; self.attempt.mkdir(mode=0o700)

    def execute(self): m.execute(self.plan,self.io,self.activation,self.attempt)

class Fixture(FixtureBase):
    def test_success_retains_pause_private_backups_and_guard(self):
        self.execute()
        self.assertTrue(self.pause.exists())
        self.assertTrue((self.attempt/'success.json').exists())
        self.assertEqual((self.attempt/'installed.plist').read_bytes(),self.installed.read_bytes())
        self.assertEqual((self.attempt/'installed.plist').stat().st_mode & 0o777,0o600)
        self.assertEqual(self.io.calls.count('engine'),2)
        self.assertEqual(self.io.calls.count('replace'),1)

    def test_proposal_preserves_all_other_properties_and_policy(self):
        old=plistlib.loads(self.installed.read_bytes()); new=plistlib.loads(m.proposal(self.installed.read_bytes(),self.plan['engines'],self.plan['production_url']))
        for key in old:
            if key not in {'ProgramArguments','EnvironmentVariables'}: self.assertEqual(old[key],new[key])
        for key,value in old['EnvironmentVariables'].items(): self.assertEqual(new['EnvironmentVariables'][key],value)

    def test_activation_refusals(self):
        for key,value in [('author_association','NONE'),('updated_at','2026-01-01T00:00:00Z'),('issue_url','wrong'),('body',self.comment['body']+'\n')]:
            c=copy.deepcopy(self.comment); c[key]=value
            with self.subTest(key=key),self.assertRaises(m.Refused): m.validate_activation(c,self.plan,self.plan['plan_hash'],time.time())
        c=copy.deepcopy(self.comment); c['user']['type']='Bot'
        with self.assertRaises(m.Refused): m.validate_activation(c,self.plan,self.plan['plan_hash'],time.time())
        with self.assertRaises(m.Refused): m.validate_activation(self.comment,self.plan,self.plan['plan_hash'],time.time()+4000)

    def test_terminal_queue_alone_is_insufficient(self):
        self.io.rows=[{'pid':987001,'pgid':7,'start':'reused','command':'unrelated'}]
        with self.assertRaisesRegex(m.Refused,'PID'): self.execute()
        self.assertNotIn('replace',self.io.calls)

    def test_group_survives_owner(self):
        self.io.rows=[{'pid':987004,'pgid':987001,'start':'child','command':'python worker'}]
        with self.assertRaisesRegex(m.Refused,'group'): self.execute()

    def test_detached_agent_blocks(self):
        self.io.rows=[{'pid':1234,'pgid':1234,'start':'child','command':'/bin/codex run'}]
        with self.assertRaisesRegex(m.Refused,'child'): self.execute()

    def test_claim_blocks(self):
        self.io.jobs.append({'id':'J4000','status':'claimed','by':'macbook'})
        with self.assertRaisesRegex(m.Refused,'claim'): self.execute()

    def test_nonterminal_blocks(self):
        self.io.jobs[0]['status']='blocked'
        with self.assertRaisesRegex(m.Refused,'terminal'): self.execute()

    def test_held_lock_is_preserved(self):
        with open(self.locks[1],'r+') as f:
            m.fcntl.flock(f,m.fcntl.LOCK_EX|m.fcntl.LOCK_NB)
            with self.assertRaisesRegex(m.Refused,'lock held'): self.execute()
        self.assertTrue(self.locks[1].exists())

    def test_source_change_blocks(self):
        self.installed.write_bytes(b'changed')
        with self.assertRaisesRegex(m.Refused,'source hash'): self.execute()

    def test_loaded_change_blocks(self):
        self.loaded=self.loaded.replace(b'10',b'11')
        with self.assertRaisesRegex(m.Refused,'loaded'): self.execute()

    def test_proposal_change_blocks(self):
        self.plan['proposal_hash']='0'*64
        with self.assertRaisesRegex(m.Refused,'proposal'): self.execute()

    def test_pause_required(self):
        self.pause.unlink()
        with self.assertRaisesRegex(m.Refused,'pause'): self.execute()

    def test_race_is_rechecked_before_replacement(self):
        self.io.race=lambda: self.io.jobs.append({'id':'J4000','status':'claimed','by':'macbook-2'})
        with self.assertRaisesRegex(m.Refused,'claim'): self.execute()
        self.assertNotIn('replace',self.io.calls)
        self.assertTrue((self.attempt/'installed.plist').exists())

    def test_edited_comment_race_blocks(self):
        self.io.race=lambda: self.comment.update(updated_at='changed')
        with self.assertRaisesRegex(m.Refused,'edited'): self.execute()
        self.assertNotIn('replace',self.io.calls)

    def test_cancel_race_blocks(self):
        self.io.race=lambda: Path(self.plan['cancel']).touch()
        with self.assertRaisesRegex(m.Refused,'cancelled'): self.execute()

    def test_deadline_race_blocks(self):
        self.io.race=lambda: self.plan.update(deadline=0)
        with self.assertRaisesRegex(m.Refused,'deadline'): self.execute()

    def test_partial_replacement_does_not_resume_or_restore_stale_service(self):
        def failed(*args): self.io.calls.append('bootout'); raise m.Refused('bootstrap failed')
        self.io.replace=failed
        with self.assertRaisesRegex(m.Refused,'bootstrap failed'): self.execute()
        self.assertTrue((self.attempt/'replacement-started').exists())
        self.assertTrue((self.attempt/'installed.plist').exists())
        self.assertTrue(self.pause.exists())
        self.assertFalse(Path(self.plan['marker']).exists())

    def test_no_live_adapter_used_by_dry_run(self):
        with patch.object(m.subprocess,'run',side_effect=AssertionError('real subprocess forbidden')),patch.object(m.subprocess,'Popen',side_effect=AssertionError('real child forbidden')):
            self.execute()

    def test_missing_lock_refuses_without_creating_it(self):
        self.locks[0].unlink()
        with self.assertRaisesRegex(m.Refused,'missing'): self.execute()
        self.assertFalse(self.locks[0].exists())


class ProductionBoundaries(FixtureBase):
    def test_new_loaded_settings_exact(self):
        data=m.proposal(self.installed.read_bytes(),self.plan['engines'],self.plan['production_url'])
        doc=plistlib.loads(data)
        text='arguments = {\n'+'\n'.join(doc['ProgramArguments'])+'\n}\nenvironment = {\n'+'\n'.join(k+' => '+v for k,v in doc['EnvironmentVariables'].items())+'\n}\n'
        m.loaded_matches(text,data)
        with self.assertRaisesRegex(m.Refused,'arguments'): m.loaded_matches(text.replace('/bin/zsh','/bin/bash'),data)
        with self.assertRaisesRegex(m.Refused,'environment'): m.loaded_matches(text.replace('MACBOOK_SLOTS => 2','MACBOOK_SLOTS => 3'),data)

    def test_production_main_and_freshness(self):
        io=m.System()
        def api(path):
            if '/git/ref/' in path: return {'object':{'sha':self.activation['commit']}}
            if '/git/commits/' in path: return {'committer':{'date':dt.datetime.now(dt.timezone.utc).isoformat()}}
            return {'private': True}
        io.api=api
        io.production(self.plan,self.activation)
        self.plan['created']=time.time()+60
        with self.assertRaisesRegex(m.Refused,'stale'): io.production(self.plan,self.activation)
        self.plan['created']=0
        io.api=lambda p: {'private':False}
        with self.assertRaisesRegex(m.Refused,'private'): io.production(self.plan,self.activation)

    def test_git_preserves_rehearsal_ref_without_reset(self):
        io=m.System(); commands=[]
        root=self.engines[0]
        self.plan['staged_heads']={str(root):'d'*40}
        self.plan['production_sources']={'scripts/macbook_worker.py':m.digest(b'worker')}
        queue=m.canonical({'jobs':[{'id':'J3999','status':'done'}]})
        self.activation['queue']=m.digest(queue)
        def git(root,*args):
            commands.append(args)
            if args[:2]==('status','--porcelain'): return ''
            if args==('rev-parse','HEAD'): return 'd'*40
            if args==('branch','--show-current'): return 'main'
            if args==('remote','get-url','origin'): return self.plan['production_url']
            if args==('rev-parse','FETCH_HEAD'): return self.activation['commit']
            if args[0]=='show': return json.dumps({'studio':{'github':'owner/studio'}})
            return ''
        io.git=git; io.processes=lambda: []
        io.run=lambda argv: queue if argv[-1].endswith('jobs/queue.json') else b'worker'
        io.update_engine(root,self.plan,self.activation,'preserved-rehearsal')
        self.assertIn(('branch','-m','main','preserved-rehearsal'),commands)
        self.assertIn(('switch','-c','main',self.activation['commit']),commands)
        self.assertFalse(any('reset' in cmd or '--force' in cmd for cmd in commands))
        self.activation['queue']='0'*64
        commands.clear()
        with self.assertRaisesRegex(m.Refused,'queue'): io.update_engine(root,self.plan,self.activation,'backup')
        self.assertFalse(any(cmd[0]=='switch' for cmd in commands))

    def test_detached_node_agent_blocks(self):
        self.io.rows=[{'pid':1234,'pgid':1234,'start':'child','command':'node /tool/codex/bin/codex.js run'}]
        with self.assertRaisesRegex(m.Refused,'child'): self.execute()

    def test_marker_preexists_blocks(self):
        Path(self.plan['marker']).write_text('{}')
        with self.assertRaisesRegex(m.Refused,'marker'): self.execute()

    def test_existing_backup_never_overwritten(self):
        (self.attempt/'installed.plist').write_bytes(b'keep')
        with self.assertRaises(FileExistsError): self.execute()
        self.assertEqual((self.attempt/'installed.plist').read_bytes(),b'keep')
        self.assertNotIn('replace',self.io.calls)

    def test_new_supervisor_is_detached_with_private_log(self):
        path=self.root/'plan.json'
        helper=str(Path(m.__file__).resolve())
        self.plan['sources'][helper]=m.digest(Path(helper).read_bytes())
        path.write_bytes(m.canonical(self.plan)); path.chmod(0o600); self.root.chmod(0o700)
        with patch.object(m.subprocess,'Popen') as popen,patch.object(m.sys,'argv',['helper','launch','--plan',str(path),'--sha256',m.digest(path.read_bytes())]),patch('builtins.print'):
            popen.return_value.pid=777
            m.main()
            self.assertTrue(popen.call_args.kwargs['start_new_session'])
            self.assertEqual(popen.call_args.kwargs['stdin'],m.subprocess.DEVNULL)
            self.assertEqual((self.root/'supervisor.log').stat().st_mode & 0o777,0o600)
        with patch.object(m.subprocess,'Popen',side_effect=AssertionError('must not relaunch')),patch.object(m.sys,'argv',['helper','launch','--plan',str(path),'--sha256',m.digest(path.read_bytes())]):
            with self.assertRaises(FileExistsError): m.main()

class AdapterBoundaries(FixtureBase):
    def test_large_queue_uses_raw_api(self):
        io=m.System(); calls=[]
        def run(args):
            calls.append(args)
            return json.dumps({'jobs':[{'id':'J3999','status':'done'}]}).encode()
        io.run=run
        self.plan['authority_repo']='owner/old'
        self.assertEqual(io.queue(self.plan)[0]['id'],'J3999')
        self.assertIn('Accept: application/vnd.github.raw+json',calls[0])

    def test_replace_only_targets_worker_and_preserves_proposal(self):
        io=m.System(); calls=[]
        proposed=m.proposal(self.installed.read_bytes(),self.plan['engines'],self.plan['production_url'])
        doc=plistlib.loads(proposed)
        after='arguments = {\n'+'\n'.join(doc['ProgramArguments'])+'\n}\nenvironment = {\n'+'\n'.join(k+' => '+v for k,v in doc['EnvironmentVariables'].items())+'\n}\n'
        def run(args): calls.append(args); return b''
        io.run=run; io.loaded=lambda: after.encode()
        io.replace(self.plan,proposed,'fixture')
        self.assertEqual(self.installed.read_bytes(),proposed)
        self.assertEqual([c[1] for c in calls],['bootout','bootstrap'])
        self.assertTrue(calls[0][-1].endswith('/'+m.LABEL))
        self.assertEqual(calls[1][-1],str(self.installed))
        self.assertTrue(self.pause.exists())

    def test_command_budget_reduces_timeout_and_refuses_expiry(self):
        io=m.System(deadline=time.time()+5)
        with patch.object(m.subprocess,'run') as run:
            run.return_value.returncode=0; run.return_value.stdout=b'ok'
            self.assertEqual(io.run(['fake']),b'ok')
            self.assertLessEqual(run.call_args.kwargs['timeout'],5)
            io.deadline=0.1
            with self.assertRaisesRegex(m.Refused,'deadline'): io.run(['fake'])

class PreparationBoundaries(FixtureBase):
    def test_private_preparation_pins_and_preserves_originals_without_commands(self):
        plan=copy.deepcopy(self.plan)
        home=self.root/'home'; state=home/'_desk/state'; state.mkdir(parents=True)
        plan['engines']=[str(home/'_desk/worker/studio'),str(home/'_desk/worker/slot2/studio')]
        plan['locks']=[str(state/'macbook-worker.lock'),str(state/'macbook-worker-2.lock')]
        plan['pause']=str(state/'macbook-worker.pause'); plan['marker']=str(state/'active-studio.json')
        plan['installed']=str(home/'Library/LaunchAgents'/ (m.LABEL+'.plist'))
        installed=Path(plan['installed']); installed.parent.mkdir(parents=True); installed.write_bytes(self.installed.read_bytes())
        plan['old_engines']=[str(home/'_desk/worker/orbit-with-ben'),str(home/'_desk/worker/slot2/orbit-with-ben')]
        plan['authority_repo']='owner/old'; plan['thread']=1
        plan['staged_heads']={root:'d'*40 for root in plan['engines']}
        plan['production_sources']={name:m.digest(b'approved') for name in ['scripts/macbook_worker.py','scripts/engine_guard.py']}
        plan['owner_pids']=[987001,987002]
        self.io.rows=[{'pid':pid,'pgid':pid,'start':'old','command':'coordinator'} for pid in plan['owner_pids']]
        doc=plistlib.loads(installed.read_bytes())
        loaded='arguments = {\n'+'\n'.join(doc['ProgramArguments'])+'\n}\nenvironment = {\n'+'\n'.join(k+' => '+v for k,v in doc['EnvironmentVariables'].items())+'\n}\n'
        self.io.loaded=lambda: loaded.encode()
        self.io.git=lambda root,*args: '' if args[0]=='status' else 'd'*40
        paths=[installed,Path(m.__file__).resolve(),Path(m.__file__).resolve().with_name('engine_guard.py')]
        for root in plan['old_engines']:
            for name in ['macbook_worker.py','engine_guard.py']:
                path=Path(root)/'scripts'/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(b'old source'); paths.append(path)
        plan['sources']={str(path):m.digest(path.read_bytes()) for path in paths}
        plan['loaded_hash']=m.digest(m.canonical(m.loaded_settings(loaded)))
        plan['proposal_hash']=m.digest(m.proposal(installed.read_bytes(),plan['engines'],plan['production_url']))
        config=state/'config.json'; config.write_bytes(m.canonical(plan)); config.chmod(0o600)
        output=state/'handoff'
        with patch.object(m.Path,'home',return_value=home),patch.object(m.subprocess,'run',side_effect=AssertionError('real command forbidden')):
            result=m.prepare(config,output,self.io)
        self.assertEqual(result,m.digest((output/'plan.json').read_bytes()))
        self.assertEqual((output/'installed-original.plist').read_bytes(),installed.read_bytes())
        self.assertTrue((output/'original-metadata.json').is_file())
        self.assertFalse(Path(plan['pause']).exists())
        self.assertFalse(Path(plan['marker']).exists())
        self.assertEqual((output/'plan.json').stat().st_mode & 0o777,0o600)

if __name__=='__main__': unittest.main()
