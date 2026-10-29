#!/usr/bin/env python3
"""MacBook worker lane: the MacBook Pro takes queued `needs macbook` jobs when Ben isn't using it
(Ben, 28 Oct 2026: "yes" to a MacBook worker lane over Tailscale with power and idle guards).

launchd runs this every 15 minutes (scripts/macbook/com.owb.macbook-worker.plist, installed by
scripts/macbook/setup_macbook.sh). Each run does at most one job, and only when ALL of these hold:
  - it is inside its hours: round the clock by default (Ben, 28 Oct 2026: "let's use the MacBook Pro 24 seven");
    MACBOOK_HOURS=night limits it to weeknights 21:00-09:00 and all weekend, London (the run must also end by 09:00);
  - no pause file (~/_desk/state/macbook-worker.pause), and no other run of this script in progress;
  - the MacBook is on mains power (never drains the battery);
  - nobody has touched the keyboard or trackpad for MACBOOK_IDLE_MIN minutes (default 10);
  - at least MACBOOK_MIN_FREE_GB free on the disk (default 15).
Then it pulls both checkouts, claims the oldest `macbook` job with
  jobs.py next --agent macbook --can macbook --git
and wakes the agent CLI (MACBOOK_AGENT, default codex) on it under `caffeinate -i`, which keeps the Mac awake for
that one run only (nothing global changes; sleep settings are untouched). The run is killed at MACBOOK_CAP_S seconds
(default 1500); a job still claimed afterwards is released with a note so the next run (or another worker) picks
it up. After a Codex run it records the Codex usage limits (pool codex: the same account as the Mini) for the board.

The `macbook` lane is separate: the Mini's workers never take these jobs and this worker never takes Mini jobs
(Studio sign-ins, the NAS rules and the HOS desk all live on the Mini). The Chief routes a job here with
`jobs.py add --needs macbook ...`: local renders, ffmpeg batches and low-stakes text on the local Ollama model.

  python3 scripts/macbook_worker.py check     # which guard would stop a run now (claims nothing)
  python3 scripts/macbook_worker.py run       # what launchd calls
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

HOME = pathlib.Path.home()
OWB = pathlib.Path(os.environ.get("OWB_REPO", HOME / "YouTube" / "orbit-with-ben"))
HOS = pathlib.Path(os.environ.get("HOS_REPO", HOME / "YouTube" / "History Of Science"))
WORKER_DIR = HOME / "_desk" / "worker"  # the clones setup_macbook.sh made for the worker itself
STATE = HOME / "_desk" / "state"
AGENT_ID = "macbook"

PROMPT = """You are the MacBook worker for Ben's YouTube studio, running unattended on Ben's MacBook Pro while he is
away from it. Your agent id is `macbook` everywhere (jobs.py --agent macbook). Do ONE job, then stop.

The job is already claimed for you: {job}
1. Orbit With Ben ({owb}) is pulled. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben") and then
     python3 scripts/jobs.py show {job}
   For a HOS job, work in the HOS checkout ({hos}) and follow its AGENTS.md.
2. Do the job exactly as its brief says. Report progress as you go:
     python3 scripts/jobs.py progress {job} --agent macbook --step <k> --of <n> --action "<what is left>" --git
3. Commit your work on a branch named macbook/<job id>, push it (git push -u origin <branch>), and open a PR to main
   with gh; say the PR number in the result. Then switch every checkout you touched back to main
   (git checkout main): a checkout left on a branch stops the MacBook taking any further job, and Ben's own
   History of Science folder must always be left on main.
4. Finish with  jobs.py done {job} --agent macbook --result "..." --git  (or block / release with a reason).
5. Report on the studio thread:  python3 scripts/owb_thread.py post "[MacBook] ..."

This is Ben's own laptop, not the Mini:
- never spend money or credit beyond the written rules, never sign in to anything, never print secrets;
- never upload, schedule or change anything on YouTube, and never delete anything on the NAS;
- the local model at http://127.0.0.1:11434 (Ollama, model {model}) is for low-stakes text only: metadata drafts,
  caption cleanup, gate summaries. Never scripts, facts or anything spoken;
- keep files inside the two checkouts and ~/_desk; leave nothing running when you stop.
Your run is killed at {cap_min} minutes: if the job will take longer, stop at a clean point, release it with a note,
and stop.
"""


def log(msg: str) -> None:
    print(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def sh(cmd: list, cwd=None, timeout: int = 300) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return subprocess.CompletedProcess(cmd, 1, "", f"{e.__class__.__name__}: {e}")


def on_ac_power(pmset_out: str | None = None) -> bool:
    out = pmset_out if pmset_out is not None else sh(["pmset", "-g", "batt"]).stdout
    return "AC Power" in out


def idle_minutes(ioreg_out: str | None = None) -> float:
    """Minutes since the last keyboard/trackpad input (IOHIDSystem HIDIdleTime, nanoseconds)."""
    out = ioreg_out if ioreg_out is not None else sh(["ioreg", "-c", "IOHIDSystem", "-d", "4"]).stdout
    m = re.search(r'"HIDIdleTime"\s*=\s*(\d+)', out)
    return int(m.group(1)) / 1e9 / 60 if m else 0.0


def in_hours(t: dt.datetime) -> bool:
    """Round the clock unless MACBOOK_HOURS=night (Ben, 28 Oct 2026, evening: "let's use the MacBook Pro 24 seven";
    the idle and mains-power guards still keep it off while he is using it). The night window is his earlier rule:
    "work at night time from say 9 PM till 9 AM, and also ... the weekend, Saturday and Sunday": London time, all of
    Sat and Sun and 21:00-09:00 on weekday nights. MACBOOK_START_H / MACBOOK_END_H change that window."""
    if os.environ.get("MACBOOK_HOURS", "always") != "night":
        return True
    from zoneinfo import ZoneInfo
    lt = t.astimezone(ZoneInfo("Europe/London"))
    if lt.weekday() >= 5:
        return True
    start, end = int(os.environ.get("MACBOOK_START_H", "21")), int(os.environ.get("MACBOOK_END_H", "9"))
    return lt.hour >= start or lt.hour < end


def guards(pmset_out=None, ioreg_out=None, free_gb=None, now=None) -> list[str]:
    """Reasons not to run now; empty means go."""
    why = []
    now = now or dt.datetime.now(dt.timezone.utc)
    cap = dt.timedelta(seconds=int(os.environ.get("MACBOOK_CAP_S", "1500")))
    if not (in_hours(now) and in_hours(now + cap)):
        # A run must also finish inside the window, so nothing is still going at 9 AM on a workday.
        why.append("outside its hours (MACBOOK_HOURS=night: weeknights 21:00-09:00 and weekends, London)")
    if (STATE / "macbook-worker.pause").exists():
        why.append("paused (rm ~/_desk/state/macbook-worker.pause to resume)")
    if not on_ac_power(pmset_out):
        why.append("on battery")
    need = float(os.environ.get("MACBOOK_IDLE_MIN", "10"))
    idle = idle_minutes(ioreg_out)
    if idle < need:
        why.append(f"in use ({idle:.0f} min idle, needs {need:.0f})")
    free = free_gb if free_gb is not None else shutil.disk_usage(str(HOME)).free / 1024 ** 3
    floor = float(os.environ.get("MACBOOK_MIN_FREE_GB", "15"))
    if free < floor:
        why.append(f"disk low ({free:.0f} GB free, needs {floor:.0f})")
    return why


def agent_cmd(agent: str, prompt: str) -> list | None:
    """The agent CLI's one-shot form, as the Mini runs it (scripts/chief_relay.py cli_spec)."""
    if agent == "codex":
        b = os.environ.get("CODEX_BIN") or shutil.which("codex")
        return [b, "exec", "--approve-for-me", "-c", "sandbox_workspace_write.network_access=true",
                "--add-dir", str(HOS), "--add-dir", str(HOME / "_desk"), prompt] if b else None
    if agent == "claude":
        b = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
        return [b, "-p", "--permission-mode", "acceptEdits", "--add-dir", str(HOS), "--add-dir", str(HOME / "_desk"),
                prompt] if b else None
    return None


def run_capped(cmd: list, cwd, cap_s: int) -> int:
    """Run in its own process group and kill the whole group at the cap, so no agent or render outlives the run."""
    import signal
    p = subprocess.Popen(cmd, cwd=cwd, start_new_session=True)
    try:
        return p.wait(timeout=cap_s)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        try:
            p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
        return 124


def claimed_job(out: str) -> str:
    m = re.search(r"^(J\d{4,})\b", out, re.M)
    return m.group(1) if m else ""


def still_mine(job: str) -> bool:
    r = sh([sys.executable, "scripts/jobs.py", "show", job], cwd=OWB)
    first = (r.stdout.splitlines() or [""])[0]
    return "claimed" in first and AGENT_ID in first


def record_usage(now: dt.datetime | None = None, every_h: float = 3.0) -> bool:
    """After a run, record the Codex usage limits for the board's AI & credits page (pool codex, shared with the Mini),
    at most every few hours so the ledger isn't one line per job. A failed read records nothing."""
    now = now or dt.datetime.now(dt.timezone.utc)
    stamp = STATE / "macbook-usage.last"
    try:
        if now.timestamp() - float(stamp.read_text().strip()) < every_h * 3600:
            return False
    except (OSError, ValueError):
        pass
    # Same ChatGPT account as the Mini (benoats@gmail.com, one shared weekly limit): one pool, read from either machine.
    r = sh([sys.executable, "scripts/ai_spend_daily.py", "--pools", "codex", "--codex-pool", "codex",
            "--by", AGENT_ID, "--git"], cwd=OWB, timeout=180)
    log(f"usage reading: {(r.stdout or r.stderr).strip()[-200:]}")
    if r.returncode == 0:
        stamp.write_text(str(now.timestamp()))
    return r.returncode == 0


def heartbeat_doc(state: str, why: list, job: str = "", now: dt.datetime | None = None) -> dict:
    now = now or dt.datetime.now(dt.timezone.utc)
    return {"at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "host": "macbook", "state": state, "why": why, "job": job}


def push_heartbeat(state: str, why: list, job: str = "") -> None:
    """One parentless commit holding heartbeat.json, force-pushed to refs/heads/macbook-heartbeat, every run (as the
    Mini's relay does on mini-heartbeat). Ben, 28 Oct 2026, after five hours with no MacBook job and no way to see
    why: the hub's Agents tab reads it ("waiting: on battery", "working on J1122"). Never raises."""
    body = json.dumps(heartbeat_doc(state, why, job)) + "\n"
    git = ["git", "-C", str(OWB)]
    try:
        blob = subprocess.run(git + ["hash-object", "-w", "--stdin"], input=body, capture_output=True, text=True,
                              timeout=30, check=True).stdout.strip()
        tree = subprocess.run(git + ["mktree"], input=f"100644 blob {blob}\theartbeat.json\n", capture_output=True,
                              text=True, timeout=30, check=True).stdout.strip()
        commit = subprocess.run(git + ["commit-tree", tree, "-m", f"macbook heartbeat {state}"], capture_output=True,
                                text=True, timeout=30, check=True).stdout.strip()
        subprocess.run(git + ["push", "-q", "-f", "origin", f"{commit}:refs/heads/macbook-heartbeat"],
                       capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"heartbeat not pushed: {e}")


def pull_main() -> str:
    """Pull both checkouts; '' when fine, else why not. Runs before the guards so fixes reach a MacBook that keeps
    waiting (it used to pull only after the guards passed, so one stuck guard kept it on old code)."""
    for repo in (OWB, HOS):
        if (repo / ".git").exists():
            branch = sh(["git", "-C", str(repo), "branch", "--show-current"]).stdout.strip()
            # A job may leave the worker's own clone on its work branch (J1194, 29 Oct 2026: the MacBook then
            # refused every later job). Its own clone goes back to main by itself when clean; Ben's checkouts never.
            if branch != "main" and repo.resolve().is_relative_to(WORKER_DIR.resolve()) \
                    and not sh(["git", "-C", str(repo), "status", "--porcelain"]).stdout.strip():
                if sh(["git", "-C", str(repo), "checkout", "-q", "main"]).returncode == 0:
                    log(f"{repo.name}: back on main from '{branch}'")
                    branch = "main"
            if branch != "main":
                return f"{repo} is on '{branch or 'detached'}', not main (re-run setup_macbook.sh)"
            r = sh(["git", "-C", str(repo), "pull", "-q", "--ff-only"], timeout=180)
            if r.returncode:
                return f"pull failed in {repo.name}: {(r.stderr or r.stdout).strip()[-200:]}"
    return ""


def run() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / "macbook-worker.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("another run is still going")
        return 0
    problem = pull_main()
    if problem:
        log(problem)
        push_heartbeat("error", [problem])
        return 1
    why = guards()
    if why:
        log("not now: " + "; ".join(why))
        push_heartbeat("waiting", why)
        return 0
    r = sh([sys.executable, "scripts/jobs.py", "next", "--agent", AGENT_ID, "--can", "macbook", "--git"], cwd=OWB)
    if r.returncode == 10:
        log("no macbook job waiting")
        push_heartbeat("idle", ["no MacBook job waiting"])
        return 0
    job = claimed_job(r.stdout)
    if r.returncode or not job:
        log(f"claim failed: {(r.stderr or r.stdout).strip()[-300:]}")
        push_heartbeat("error", [f"claim failed: {(r.stderr or r.stdout).strip()[-120:]}"])
        return 1
    push_heartbeat("working", [], job)
    agent = os.environ.get("MACBOOK_AGENT", "codex")
    cap = int(os.environ.get("MACBOOK_CAP_S", "1500"))
    prompt = PROMPT.format(job=job, owb=OWB, hos=HOS, model=os.environ.get("OLLAMA_MODEL", "qwen3:14b"),
                           cap_min=cap // 60)
    cmd = agent_cmd(agent, prompt)
    if not cmd:
        sh([sys.executable, "scripts/jobs.py", "release", job, "--agent", AGENT_ID, "--note",
            f"MacBook worker: the {agent} CLI isn't installed", "--git"], cwd=OWB)
        log(f"{agent} CLI not found: released {job}")
        return 1
    log(f"{job}: waking {agent} (cap {cap // 60} min)")
    code = run_capped(["caffeinate", "-i", *cmd] if shutil.which("caffeinate") else cmd, OWB, cap)
    sh(["git", "-C", str(OWB), "pull", "-q", "--ff-only"], timeout=180)
    if still_mine(job):
        sh([sys.executable, "scripts/jobs.py", "release", job, "--agent", AGENT_ID, "--note",
            f"MacBook worker run ended (exit {code}) with the job still open; picked up again next run", "--git"],
           cwd=OWB)
        log(f"{job}: released after exit {code}")
    else:
        log(f"{job}: finished (exit {code})")
    if agent == "codex":
        record_usage()
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "check"])
    a = ap.parse_args(argv)
    if a.cmd == "check":
        why = guards()
        print("would run now" if not why else "would wait: " + "; ".join(why))
        return 0
    return run()


if __name__ == "__main__":
    sys.exit(main())
