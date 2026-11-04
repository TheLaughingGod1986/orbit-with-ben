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
jobs.load = lambda: json.loads(jobs.QUEUE.read_text())
jobs.save = lambda data: jobs.QUEUE.write_text(json.dumps(data, indent=2) + "\n")
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


if __name__ == "__main__":
    unittest.main()
