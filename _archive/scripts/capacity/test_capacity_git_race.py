"""Two local clones race real Git pushes; never contact production remotes."""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

from test_dispatch_capacity import job

# Each process uses the real jobs.with_git retry implementation in a disposable
# clone. File barriers force both first attempts to plan from the same head.
RUNNER = r'''
import json, pathlib, subprocess, sys, time
sys.path.insert(0, sys.argv[1])
import jobs, studio
import capacity_reservations as reservations
from test_dispatch_capacity import T, host, proof, choose
root, sync, identity = map(pathlib.Path, sys.argv[2:5])
worker = "codex" if identity.name == "hostA" else "gemini"
name = identity.name
jobs.ROOT = studio.ROOT = root
jobs.QUEUE = root / "jobs/queue.json"
jobs.JOBS_MD = root / "JOBS.md"
jobs.load = lambda path=None: json.loads((path or jobs.QUEUE).read_text())
jobs.save = lambda data, path=None: (path or jobs.QUEUE).write_text(json.dumps(data, indent=2) + "\n")
count = 0
def evidence():
    global count
    count += 1
    if count == 1:
        (sync / name).touch()
        until = time.monotonic() + 10
        while len(list(sync.iterdir())) < 2:
            if time.monotonic() > until:
                raise RuntimeError("race barrier timeout")
            time.sleep(.01)
    return dict(hosts=[host(name, worker=worker, role="mini")], leases=[],
                accounts={"shared":proof(ready=True, limit=2)}, at=T,
                chief="codex", choose_worker=choose, installed_head="reviewed",
                reviewed_head="reviewed")
value, error = reservations.reserve_with_git(evidence=evidence,
    token="reservation-token-" + name, host_id=name, worker=worker)
print(json.dumps(dict(value=value, error=error, attempts=count)))
'''


REVIEW_IDENTITY_RUNNER = r'''
import sys, tempfile, pathlib, subprocess, json
sys.path.insert(0, sys.argv[1])
import jobs, studio, capacity_evidence, capacity_reservations as reservations
from test_dispatch_capacity import T, host, proof, choose, job
from unittest.mock import patch
with tempfile.TemporaryDirectory() as tmp:
    root=pathlib.Path(tmp); repo=root/'repo'; remote=root/'remote.git'
    def git(*args,cwd=None):
        return subprocess.run(['git',*map(str,args)],cwd=cwd,capture_output=True,text=True,check=True).stdout.strip()
    git('init','--bare',remote); git('init','-b','main',repo)
    git('config','user.name','Local test',cwd=repo);git('config','user.email','test@example.invalid',cwd=repo)
    (repo/'jobs').mkdir();(repo/'jobs/queue.json').write_text(json.dumps({'jobs':[job()]}));(repo/'JOBS.md').write_text('fixture\n')
    git('add','.',cwd=repo);git('commit','-m','fixture',cwd=repo);git('remote','add','origin',remote,cwd=repo);git('push','origin','main',cwd=repo)
    reviewed=capacity_evidence.installed_head(repo)
    jobs.ROOT=studio.ROOT=repo;jobs.QUEUE=repo/'jobs/queue.json';jobs.JOBS_MD=repo/'JOBS.md'
    jobs.load=lambda path=None:json.loads((path or jobs.QUEUE).read_text())
    jobs.save=lambda data,path=None:(path or jobs.QUEUE).write_text(json.dumps(data,indent=2)+"\n")
    def evidence():
        return dict(hosts=[host()],leases=[],accounts={'shared':proof(ready=True,limit=1)},at=T,chief='codex',choose_worker=choose,installed_head=capacity_evidence.reviewed_installation(repo,reviewed),reviewed_head=reviewed)
    with patch('chief_relay.current_execution',return_value=None),patch('chief_relay.worker_capabilities',return_value={}):
        result,error=reservations.reserve_with_git(evidence=evidence,token='head-drift-probe-0001',host_id='mini',worker='codex')
        assert result and error is None,(result,error)
        changed=capacity_evidence.installed_head(repo)!=reviewed
        claim,error=reservations.consume_with_git(evidence=evidence,token='head-drift-probe-0001',host_id='mini',worker='codex',claimant='codex')
        assert changed and claim and claim['status']=='claimed' and error is None,(claim,error)
        # Include the board/queue release transaction in the same real-Git cycle.
        released,error=reservations.release_failed_with_git(token='head-drift-probe-0001',host_id='mini',worker='codex',claimant='codex',reason='fixture launch rejected',clear=lambda:True,clock=lambda:T)
        assert released and error is None,(released,error)
        assert jobs.load()['jobs'][0]['status']=='open'
        assert capacity_evidence.reviewed_installation(repo,reviewed)==reviewed
        # Uncommitted tracked state and later source changes both invalidate review.
        (repo/'JOBS.md').write_text('dirty operational state')
        try:
            capacity_evidence.reviewed_installation(repo,reviewed)
            raise AssertionError('dirty installation accepted')
        except ValueError:
            pass
        git('checkout','--','JOBS.md',cwd=repo)
        (repo/'scripts').mkdir();(repo/'scripts/capacity_caller.py').write_text('changed code')
        git('add','.',cwd=repo);git('commit','-m','unreviewed code',cwd=repo)
        try:
            capacity_evidence.reviewed_installation(repo,reviewed)
            raise AssertionError('changed source accepted')
        except ValueError:
            pass
        print(json.dumps({'reserve_claim_release':True,'source_and_dirty_rejected':True}))

'''

class GitRace(unittest.TestCase):
    def test_two_hosts_cannot_reserve_same_job_or_stage(self):
        for same_stage in (False, True):
            with self.subTest(same_stage=same_stage), tempfile.TemporaryDirectory() as temp:
                root = pathlib.Path(temp)
                remote, seed = root / "remote.git", root / "seed"
                def git(*args, cwd=None):
                    return subprocess.run(["git", *map(str,args)], cwd=cwd,
                        capture_output=True, text=True, check=True)
                git("init", "--bare", remote)
                git("init", "-b", "main", seed)
                git("config", "user.email", "test@example.invalid", cwd=seed)
                git("config", "user.name", "Capacity test", cwd=seed)
                (seed / "jobs").mkdir()
                rows = [job(film="028", stage="edit")] if same_stage else [job()]
                if same_stage:
                    rows.append(job("J1841", film="028", stage="edit"))
                (seed / "jobs/queue.json").write_text(json.dumps(dict(jobs=rows)))
                (seed / "JOBS.md").write_text("fixture queue\n")
                git("add", ".", cwd=seed)
                git("commit", "-m", "fixture", cwd=seed)
                git("remote", "add", "origin", remote, cwd=seed)
                git("push", "origin", "main", cwd=seed)
                sync = root / "barrier"
                sync.mkdir()
                processes = []
                for name in ("hostA", "hostB"):
                    clone = root / name
                    git("clone", "--branch", "main", remote, clone)
                    git("config", "user.email", "test@example.invalid", cwd=clone)
                    git("config", "user.name", "Capacity test", cwd=clone)
                    processes.append(subprocess.Popen([sys.executable, "-c", RUNNER,
                        str(pathlib.Path(__file__).parent.resolve()), str(clone), str(sync), name],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                        env=dict(os.environ, GIT_TERMINAL_PROMPT="0")))
                outcomes = []
                try:
                    for process in processes:
                        out, err = process.communicate(timeout=25)
                        self.assertEqual(process.returncode, 0, err)
                        outcomes.append(json.loads(out))
                finally:
                    for process in processes:
                        if process.poll() is None:
                            process.kill()
                            process.communicate()
                self.assertEqual(sum(v["value"] is not None for v in outcomes), 1, outcomes)
                self.assertEqual(sorted(v["attempts"] for v in outcomes), [1,2], outcomes)
                data = json.loads(git("show", "main:jobs/queue.json", cwd=remote).stdout)
                reserved = [j for j in data["jobs"] if j.get("dispatch_reservation")]
                self.assertEqual(len(reserved), 1)
                self.assertTrue(all(j["status"] == "open" for j in data["jobs"]))
                self.assertEqual(reserved[0]["dispatch_reservation"]["phase"], "reserved")

    def test_consume_board_claim_push_race_rolls_back_and_succeeds_on_retry(self):
        consume_runner = r'''
import json, pathlib, sys, time
sys.path.insert(0, sys.argv[1])
import jobs, studio
import capacity_evidence
import capacity_reservations as reservations
from test_dispatch_capacity import T, host, proof, choose
root, sync = map(pathlib.Path, sys.argv[2:4])
jobs.ROOT = studio.ROOT = root
studio.FILMS = root / "02_Video-Projects"
jobs.QUEUE = root / "jobs/queue.json"
jobs.JOBS_MD = root / "JOBS.md"
jobs.load = lambda path=None: json.loads((path or jobs.QUEUE).read_text())
jobs.save = lambda data, path=None: (path or jobs.QUEUE).write_text(json.dumps(data, indent=2) + "\n")
count = 0
def evidence():
    global count
    count += 1
    claims = capacity_evidence.board_stage_claims(studio.FILMS, "owb", T)
    if count == 1:
        (sync / "ready").touch()
        until = time.monotonic() + 10
        while not (sync / "competing_pushed").exists():
            if time.monotonic() > until:
                raise RuntimeError("consume race barrier timeout")
            time.sleep(.01)
    return dict(hosts=[host("mini", worker="codex", role="mini"),
                            host("peer", role="mini", workers={})],
                leases=[dict(job="J9999", worker="gemini", host="peer", account="other")],
                accounts={"shared": proof(ready=True, limit=1)}, at=T,
                chief="codex", choose_worker=choose, installed_head="reviewed",
                reviewed_head="reviewed", stage_claims=claims)
value, error = reservations.consume_with_git(
    evidence=evidence, token="reservation-token-consume-race",
    host_id="mini", worker="codex", claimant="codex"
)
print(json.dumps(dict(value=value, error=error, attempts=count)))
'''
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            remote, seed = root / "remote.git", root / "seed"
            def git(*args, cwd=None):
                return subprocess.run(["git", *map(str, args)], cwd=cwd,
                    capture_output=True, text=True, check=True)
            git("init", "--bare", remote)
            git("init", "-b", "main", seed)
            git("config", "user.email", "test@example.invalid", cwd=seed)
            git("config", "user.name", "Capacity test", cwd=seed)
            (seed / "jobs").mkdir()
            film_dir = seed / "02_Video-Projects/028_Test-Film"
            film_dir.mkdir(parents=True)
            (film_dir / "status.json").write_text(json.dumps(dict(
                film="028", title="Test Film", claims=[],
                stages={"edit": {"state": "todo"}}
            ), indent=2) + "\n")
            (seed / "STATUS.md").write_text("fixture status\n")
            row = job(film="028", stage="edit")
            row["dispatch_reservation"] = dict(
                job=row["id"], worker="codex", host="mini", account="shared",
                phase="reserved", token="reservation-token-consume-race",
                head="reviewed", at="2026-11-04T00:00:00+00:00",
                expiresAt="2026-11-04T00:02:00+00:00",
                stage_key=["owb", "028", "edit"]
            )
            other = job("J9999", status="claimed", by="gemini")
            (seed / "jobs/queue.json").write_text(json.dumps(dict(jobs=[row, other]), indent=2) + "\n")
            (seed / "JOBS.md").write_text("fixture queue\n")
            git("add", ".", cwd=seed)
            git("commit", "-m", "fixture", cwd=seed)
            git("remote", "add", "origin", remote, cwd=seed)
            git("push", "origin", "main", cwd=seed)

            sync = root / "barrier"
            sync.mkdir()
            clone_a = root / "cloneA"
            clone_b = root / "cloneB"
            for clone in (clone_a, clone_b):
                git("clone", "--branch", "main", remote, clone)
                git("config", "user.email", "test@example.invalid", cwd=clone)
                git("config", "user.name", "Capacity test", cwd=clone)

            proc = subprocess.Popen(
                [sys.executable, "-c", consume_runner,
                 str(pathlib.Path(__file__).parent.resolve()), str(clone_a), str(sync)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                env=dict(os.environ, GIT_TERMINAL_PROMPT="0")
            )
            try:
                until = os.times().elapsed + 10
                while not (sync / "ready").exists():
                    if os.times().elapsed > until:
                        raise RuntimeError("waiting for cloneA attempt 1 timed out")
                # Push an unrelated queue update from cloneB so cloneA's first push fails.
                q_b = json.loads((clone_b / "jobs/queue.json").read_text())
                q_b["jobs"][1]["remaining_action"] = "Updated from cloneB"
                (clone_b / "jobs/queue.json").write_text(json.dumps(q_b, indent=2) + "\n")
                git("add", "jobs/queue.json", cwd=clone_b)
                git("commit", "-m", "competing unrelated update", cwd=clone_b)
                git("push", "origin", "main", cwd=clone_b)
                (sync / "competing_pushed").touch()

                out, err = proc.communicate(timeout=25)
                self.assertEqual(proc.returncode, 0, err)
                outcome = json.loads(out)
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.communicate()

            self.assertIsNone(outcome["error"], outcome)
            self.assertEqual(outcome["attempts"], 2, outcome)
            self.assertEqual(outcome["value"]["status"], "claimed")
            remote_q = json.loads(git("show", "main:jobs/queue.json", cwd=remote).stdout)
            self.assertEqual(remote_q["jobs"][0]["status"], "claimed")
            self.assertEqual(remote_q["jobs"][0]["by"], "codex")
            self.assertEqual(remote_q["jobs"][1]["remaining_action"], "Updated from cloneB")
            remote_board = json.loads(git(
                "show", "main:02_Video-Projects/028_Test-Film/status.json", cwd=remote
            ).stdout)
            self.assertEqual(len(remote_board["claims"]), 1)
            self.assertEqual(remote_board["claims"][0]["by"], "codex")
            self.assertEqual(remote_board["stages"]["edit"]["state"], "doing")

    def test_review_identity_survives_real_queue_commits_but_rejects_source_change(self):
        runner = REVIEW_IDENTITY_RUNNER
        result = subprocess.run([sys.executable, "-c", runner,
                                 str(pathlib.Path(__file__).parent.resolve())],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout),
                         {"reserve_claim_release":True,"source_and_dirty_rejected":True})


if __name__ == "__main__":
    unittest.main()
