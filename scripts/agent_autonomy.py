#!/usr/bin/env python3
"""Each agent runs itself (J3265, Ben 21 Nov 2026).

The relay still walks chains, checks stalls and does Chief duties, and it stays the fallback.
Set AGENT_SELF_DISPATCH=0 to leave starting work to the relay only.

An agent's own timer (scripts/agent_timer.py, one launchd job each) checks its usage flag,
takes the best ready job through the existing claim, works it, and sleeps. One agent never
runs twice (a per-agent lease). The Mini also keeps a memory floor and a cap (AGENT_MINI_CAP,
default 3) on how many of its agents run at once.

Claim order, when the agent is named: jobs whose kind lists that agent first in routing.py,
then the existing urgent and due-soon order. Gemini also prefers picture and video watches.

Finishing a pipeline stage queues the next stage's job (film and stage set) unless that job
already exists. A failed run retries once on the next model in the kind's chain; the second
failure files one repair job, releases the claim, and appends a line to the self-improvement
feed (J3257) for rsi.ingest_failure when that module is present.

Studio windows are one desk each: 9223 Orbit, 9224 Field Order History, 9460 History of
Science on the Mini. 9222 is the Flow browser on the Mini and History of Science Studio on
the MacBook. ElevenLabs and Flow stay one at a time. Kind assembly never takes a Studio desk.
"""
import datetime as dt
import json
import os
import pathlib
import subprocess
import threading

import routing

ROOT = pathlib.Path(__file__).resolve().parents[1]
# (agent, every minutes, label). Intervals are 10–15 min and already staggered.
TIMERS = (
    ("cursor", 10, "Cursor"),
    ("gemini", 11, "Gemini"),
    ("claudecode", 12, "Claude Code"),
    ("codex", 13, "Codex"),
    ("macbook", 14, "MacBook"),
    ("macbook-2", 15, "MacBook 2"),
)
MINI_AGENTS = ("cursor", "gemini", "claudecode", "codex")
# Gemini watches pictures and video (J3265) even though Cursor runs the tool first.
GEMINI_WATCH = {"image", "video"}
OPEN = ("open", "claimed", "blocked", "done")
_LOCK = threading.Lock()
# stage finished → (next stage, kind, needs, title). QA is a kind on the thumbs stage
# because the board stages have no separate QA column. Upload is never queued here.
HANDOFF = {
    "script": ("sources", "facts", "any", "Check the spoken facts for {film}"),
    "vo": ("shots", "review", "any", "Write the shot list for {film}"),
    "picture": ("edit", "assembly", "mini", "Cut the pictures for {film}"),
    "edit": ("thumbs", "qa", "any", "Review the cut of {film}"),
}
QA_NEXT = ("thumbs", "thumb", "mini", "Design the thumbnail for {film}")


def enabled() -> bool:
    """False rolls dispatch back to the relay (AGENT_SELF_DISPATCH=0)."""
    return os.environ.get("AGENT_SELF_DISPATCH", "1") != "0"


def host_of(agent: str) -> str:
    return "macbook" if str(agent or "").startswith("macbook") else "mini"


def lanes(agent: str) -> set:
    if str(agent or "").startswith("macbook"):
        return {"macbook", "any"}
    if agent == "claude":
        return {"cloud", "any"}
    return {"mini", "gemini", "any"}


def skill_rank(job: dict, agent: str) -> int:
    """0 when this agent should prefer the job, else 1. Jobs with no kind stay 1."""
    kind = job.get("kind") or ""
    if not agent or kind not in routing.CHAINS:
        return 1
    primary = routing.CHAINS[kind][1][0][0]
    if primary == agent:
        return 0
    if agent == "gemini" and kind in GEMINI_WATCH:
        return 0
    return 1


def state_root(state=None) -> pathlib.Path:
    if state is not None:
        return pathlib.Path(state)
    import chief_relay
    return pathlib.Path(chief_relay.STATE)


def _alive(pid) -> bool:
    try:
        pid = int(pid or 0)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _stamp(value):
    try:
        when = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    return when


def _read_holder(path: pathlib.Path, at: dt.datetime):
    try:
        row = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(row, dict):
        return None
    exp = _stamp(row.get("expiresAt"))
    if not exp or exp <= at or not _alive(row.get("pid")):
        return None
    return row


def _write_holder(path: pathlib.Path, agent: str, at: dt.datetime, minutes: int = 25) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "agent": agent, "pid": os.getpid(), "at": at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expiresAt": (at + dt.timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }, indent=2) + "\n")


def lease_held(agent: str, at: dt.datetime, state=None) -> bool:
    row = _read_holder(state_root(state) / "agent-leases" / f"{agent}.json", at)
    return bool(row)


def acquire_lease(agent: str, at: dt.datetime, state=None, minutes: int = 25) -> bool:
    """One live process per agent. The same pid may refresh its own lease."""
    path = state_root(state) / "agent-leases" / f"{agent}.json"
    row = _read_holder(path, at)
    if row and int(row.get("pid") or 0) != os.getpid():
        return False
    _write_holder(path, agent, at, minutes)
    return True


def release_lease(agent: str, state=None) -> None:
    path = state_root(state) / "agent-leases" / f"{agent}.json"
    try:
        row = json.loads(path.read_text())
    except (OSError, ValueError):
        return
    if int(row.get("pid") or 0) == os.getpid():
        path.unlink(missing_ok=True)


def mini_running(at: dt.datetime, state=None) -> int:
    return sum(1 for agent in MINI_AGENTS if lease_held(agent, at, state))


def memory_ok(free_mb=None) -> bool:
    """True when free memory is at or above AGENT_MEM_FLOOR_MB. Unknown memory does not block."""
    floor = int(os.environ.get("AGENT_MEM_FLOOR_MB", "1536"))
    if free_mb is None:
        raw = os.environ.get("AGENT_FREE_MB")
        if raw:
            try:
                free_mb = int(raw)
            except ValueError:
                return True
        else:
            return True
    return free_mb >= floor


def usage_blocked(agent: str, at: dt.datetime | None = None) -> bool:
    if agent in routing.OUT:
        return True
    return agent in routing.read_flags(at)


def may_start(agent: str, at: dt.datetime, state=None, free_mb=None) -> tuple:
    """(ok, reason). Reason is empty when the timer may claim."""
    if not enabled():
        return False, "relay-only"
    if usage_blocked(agent, at):
        return False, "usage"
    if lease_held(agent, at, state):
        return False, "already running"
    if agent in MINI_AGENTS:
        cap = int(os.environ.get("AGENT_MINI_CAP", "3"))
        if mini_running(at, state) >= cap:
            return False, "cap"
        if not memory_ok(free_mb):
            return False, "memory"
    return True, ""


def channel_of(job: dict) -> str:
    repo = str(job.get("repo") or "").lower()
    if repo in ("hos", "ww2", "owb"):
        return repo
    return "owb"


def desk_name(job: dict, host: str = "mini") -> str:
    """The one desk this job needs, or '' when it needs none (code and tooling included)."""
    kind = job.get("kind") or ""
    if kind == "vo":
        return "elevenlabs"
    if kind in ("image", "video"):
        return "flow"
    if kind != "studio":
        return ""
    channel = channel_of(job)
    if channel == "ww2":
        return "studio-ww2"          # 9224 Field Order History
    if channel == "hos":
        return "studio-hos-macbook" if host == "macbook" else "studio-hos-mini"  # 9222 / 9460
    return "studio-owb"              # 9223 Orbit


def desk_blocks(job: dict, agent: str, state, at: dt.datetime, host: str = "mini") -> bool:
    name = desk_name(job, host)
    if not name:
        return False
    row = _read_holder(state_root(state) / "desks" / f"{name}.json", at)
    return bool(row and row.get("agent") != agent)


def acquire_desk(name: str, agent: str, at: dt.datetime, state=None, minutes: int = 25) -> bool:
    if not name:
        return True
    path = state_root(state) / "desks" / f"{name}.json"
    row = _read_holder(path, at)
    if row and row.get("agent") != agent:
        return False
    _write_holder(path, agent, at, minutes)
    return True


def release_desk(name: str, agent: str, state=None) -> None:
    if not name:
        return
    path = state_root(state) / "desks" / f"{name}.json"
    try:
        row = json.loads(path.read_text())
    except (OSError, ValueError):
        return
    if row.get("agent") == agent and int(row.get("pid") or 0) == os.getpid():
        path.unlink(missing_ok=True)


def record_wake(agent: str, at: dt.datetime, state=None, job: str = "", status: str = "") -> None:
    path = state_root(state) / "agent-timers" / f"{agent}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "agent": agent, "at": at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "job": job, "status": status,
    }, indent=2) + "\n")


def timer_rows(at: dt.datetime | None = None, state=None) -> list:
    """Every agent's interval, last wake and current job, for the Machines panel."""
    root = state_root(state) / "agent-timers"
    rows = []
    for agent, minutes, label in TIMERS:
        beat = {}
        try:
            beat = json.loads((root / f"{agent}.json").read_text())
        except (OSError, ValueError):
            beat = {}
        rows.append({"agent": agent, "label": label, "everyMin": minutes,
                     "at": beat.get("at") or "", "job": beat.get("job") or "",
                     "status": beat.get("status") or ""})
    return rows


def peek(data: dict, agent: str, at: dt.datetime, state=None) -> dict | None:
    """The job this agent would claim, without claiming it."""
    import jobs
    can = lanes(agent)
    host = host_of(agent)
    held = next((j for j in data["jobs"] if j.get("by") == agent and j.get("status") == "claimed"), None)
    if held:
        return held
    for cand in jobs.ordered(data, at, agent):
        if jobs.claimable(data, cand, can, at, agent) and not desk_blocks(cand, agent, state, at, host):
            return cand
    return None


def claim_next(data: dict, agent: str, at: dt.datetime, state=None) -> dict | None:
    """Claim under one process lock so two agents in this process never take the same job."""
    import jobs
    can = lanes(agent)
    host = host_of(agent)
    with _LOCK:
        held = next((j for j in data["jobs"] if j.get("by") == agent and j.get("status") == "claimed"), None)
        if held:
            return held
        for cand in jobs.ordered(data, at, agent):
            if not jobs.claimable(data, cand, can, at, agent):
                continue
            if desk_blocks(cand, agent, state, at, host):
                continue
            return jobs.do_next(data, agent, can, at, job_id=cand["id"])
        return None


def next_spec(job: dict):
    if (job.get("kind") or "") == "qa":
        return QA_NEXT
    return HANDOFF.get(job.get("stage") or "")


def queue_next(data: dict, job: dict, agent: str, at: dt.datetime):
    """Queue the next pipeline stage once. None when there is nothing to queue or one already exists."""
    if not enabled() or not job.get("film") or job.get("kind") == "chief" or job.get("needs") == "ben" or job.get("awaits_ben"):
        return None
    spec = next_spec(job)
    if not spec:
        return None
    stage, kind, needs, title = spec
    if stage == "upload":
        return None
    title = title.format(film=job["film"])
    import channels
    repo = job.get("repo") or channels.default()
    if any(j.get("film") == job["film"] and j.get("stage") == stage and j.get("kind") == kind
           and (j.get("repo") or channels.default()) == repo and j.get("status") in OPEN and j.get("id") != job.get("id")
           for j in data["jobs"]):
        return None
    import jobs
    body = (f"Queued when {job['id']} finished its stage. Film {job['film']}. "
            "£0. Ben's watch, money and publishing stay gated.")
    new = jobs.do_add(data, title=title, needs=needs, body=body, by=agent or "relay", at=at,
                      film=str(job["film"]), stage=stage, kind=kind, repo=repo, action=title[:180])
    new["handoff_from"] = job["id"]
    jobs.log(job, at, agent or "relay", f"queued {new['id']} for {stage}")
    return new


def note_failure(record: dict, path: pathlib.Path) -> None:
    """One JSON line on the self-improvement feed. rsi.ingest_failure picks it up when present."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    try:
        import rsi
    except ImportError:
        return
    ingest = getattr(rsi, "ingest_failure", None)
    if ingest:
        ingest(record)


def fail_run(data: dict, job: dict, agent: str, model: str, command: str, tail: str, at: dt.datetime, feed: pathlib.Path | None = None) -> dict:
    """First failure: retry once on the next model. Second failure: one repair job, then release."""
    import jobs
    command = jobs.scrub(command or "")[:300]
    tail = jobs.scrub(tail or "")[-1500:]
    rec = job.get("self_retry") or {}
    count = int(rec.get("count") or 0)
    nxt = routing.next_lane(job, after_agent=agent, after_model=model or "")
    if count < 1 and nxt:
        job["self_retry"] = {"count": 1, "from": agent, "model": model or "", "to": nxt[0], "to_model": nxt[1],
                             "command": command, "tail": tail[-400:]}
        jobs.log(job, at, agent, f"retry once on {nxt[0]} {nxt[1]}")
        return {"action": "retry", "agent": nxt[0], "model": nxt[1]}
    existing = next((j for j in data["jobs"] if j.get("repair_of") == job.get("id") and j.get("status") in ("open", "claimed", "blocked")), None)
    if existing:
        return {"action": "repair", "job": existing["id"], "duplicate": True}
    kind = "assembly" if job.get("film") and job.get("stage") else "review"
    title = "Fix a failed run and try it again"
    body = f"Failed job: {job.get('id')}\nCommand: {command}\n\nError tail:\n{tail}\n\n£0."
    extra = {"film": job["film"], "stage": job["stage"]} if job.get("film") and job.get("stage") else {}
    repair = jobs.do_add(data, title=title, needs="any", body=body, by=agent, at=at, kind=kind,
                         action=title, **extra)
    repair["repair_of"] = job["id"]
    feed = feed or (state_root(None) / "rsi" / "failure_feed.jsonl")
    note_failure({"at": at.strftime("%Y-%m-%dT%H:%M:%SZ"), "job": job.get("id"), "agent": agent,
                  "model": model or "", "command": command, "tail": tail[-800:], "repair": repair["id"]}, feed)
    if job.get("status") == "claimed" and job.get("by") == agent:
        jobs.do_release(job, agent, f"failed twice; repair {repair['id']} filed", at)
    return {"action": "repair", "job": repair["id"]}


def tick(agent: str, at: dt.datetime, state, data: dict, run, free_mb=None, feed: pathlib.Path | None = None) -> dict:
    """One in-process heartbeat. `run(agent, job, model)` returns (code, tail, command)."""
    ok, why = may_start(agent, at, state, free_mb)
    if not ok:
        record_wake(agent, at, state, status=why)
        return {"started": False, "reason": why}
    if not acquire_lease(agent, at, state):
        record_wake(agent, at, state, status="already running")
        return {"started": False, "reason": "already running"}
    desk = ""
    try:
        job = claim_next(data, agent, at, state)
        if not job:
            record_wake(agent, at, state, status="idle")
            return {"started": False, "reason": "nothing waiting"}
        desk = desk_name(job, host_of(agent))
        if desk and not acquire_desk(desk, agent, at, state):
            import jobs
            jobs.do_release(job, agent, f"desk {desk} is held", at)
            record_wake(agent, at, state, status="desk")
            return {"started": False, "reason": f"desk {desk}"}
        record_wake(agent, at, state, job=job["id"], status="working")
        model = routing.model_for(job, agent)
        code, tail, command = run(agent, job, model)
        if code == 0:
            return {"started": True, "ok": True, "job": job["id"]}
        outcome = fail_run(data, job, agent, model, command, tail, at, feed)
        if outcome.get("action") == "retry":
            code2, tail2, command2 = run(outcome["agent"], job, outcome["model"])
            if code2 == 0:
                return {"started": True, "ok": True, "job": job["id"], "retried": True}
            outcome = fail_run(data, job, agent, outcome["model"], command2, tail2, at, feed)
        return {"started": True, "ok": False, "job": job["id"], **outcome}
    finally:
        if desk:
            release_desk(desk, agent, state)
        release_lease(agent, state)


def plist_body(agent: str, minutes: int) -> str:
    label = f"com.owb.agent.{agent}"
    repo = '"$HOME/_desk/worker/orbit-with-ben"' if agent.startswith("macbook") else '"$HOME/YouTube/orbit-with-ben"'
    command = (f'cd {repo} &amp;&amp; python3 scripts/agent_timer.py tick --agent {agent} '
               f'>> "$HOME/Library/Logs/agent-timer-{agent}.log" 2>&gt;&amp;1')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>{command}</string>
  </array>
  <key>StartInterval</key>
  <integer>{minutes * 60}</integer>
  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
"""


def write_plists(folder: pathlib.Path) -> list:
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for agent, minutes, _label in TIMERS:
        path = folder / f"com.owb.agent.{agent}.plist"
        path.write_text(plist_body(agent, minutes))
        paths.append(path)
    return paths


def default_run(agent: str, job: dict, model: str = ""):
    """One bounded CLI run. MacBook slots use the MacBook worker's single pass."""
    if str(agent).startswith("macbook"):
        import macbook_worker
        macbook_worker.AGENT_ID = agent
        outcome = macbook_worker.run_one()
        return (0 if outcome in ("ran", "idle", "waiting") else 1), outcome, f"macbook_worker.run_one {agent}"
    import chief_relay
    cap = int(os.environ.get("CHIEF_CAP_S", "1500"))
    prompt = (f"Your agent id is {agent}. Job {job['id']} is already claimed by you. "
              "Do that job only, report progress, then finish or release it. "
              "£0 beyond the written rules. Do not upload, delete, or change a video's privacy or schedule.")
    code, tail = chief_relay.run_cli(agent, prompt, cap, model or "")
    return code, tail, f"agent timer {agent} {model} {job.get('id')}"


def live_tick(agent: str, run=None, root: pathlib.Path | None = None) -> int:
    """One heartbeat on a machine whose checkout is on main (the Mini, or a MacBook worker)."""
    import jobs
    run = run or default_run
    root = root or ROOT
    at = jobs.now()
    state = state_root(None)
    if not enabled():
        record_wake(agent, at, state, status="relay-only")
        return 0
    ok, why = may_start(agent, at, state)
    if not ok:
        record_wake(agent, at, state, status=why)
        return 0
    if not acquire_lease(agent, at, state):
        record_wake(agent, at, state, status="already running")
        return 0
    if str(agent).startswith("macbook"):
        # The MacBook worker already claims one job, runs it and releases it. The lease stops a second slot.
        try:
            import macbook_worker
            macbook_worker.AGENT_ID = agent
            outcome = macbook_worker.run_one()
            record_wake(agent, at, state, status=outcome)
            return 0 if outcome != "error" else 1
        finally:
            release_lease(agent, state)
    desk = ""
    try:
        claimed = None
        for _ in range(4):
            data = jobs.load()
            cand = peek(data, agent, at, state)
            if not cand:
                record_wake(agent, at, state, status="idle")
                return 0
            if cand.get("by") == agent and cand.get("status") == "claimed":
                claimed = cand
                break
            import sys
            proc = subprocess.run([sys.executable, str(root / "scripts/jobs.py"),
                                   "next", "--id", cand["id"], "--agent", agent,
                                   "--can", ",".join(sorted(lanes(agent))), "--git"],
                                  cwd=str(root), capture_output=True, text=True)
            if proc.returncode == 0:
                data = jobs.load()
                claimed = jobs.find(data, cand["id"])
                if claimed and claimed.get("by") == agent:
                    break
            claimed = None
        if not claimed:
            record_wake(agent, at, state, status="idle")
            return 0
        desk = desk_name(claimed, host_of(agent))
        if desk and not acquire_desk(desk, agent, at, state):
            import sys
            subprocess.run([sys.executable, str(root / "scripts/jobs.py"), "release", claimed["id"],
                            "--agent", agent, "--note", f"desk {desk} is held", "--git"], cwd=str(root))
            record_wake(agent, at, state, status="desk")
            return 0
        record_wake(agent, at, state, job=claimed["id"], status="working")
        model = routing.model_for(claimed, agent)
        code, tail, command = run(agent, claimed, model)
        if code == 0:
            return 0

        def apply(data):
            job = jobs.find(data, claimed["id"])
            if not job:
                return None, "missing job", []
            return fail_run(data, job, agent, model, command, tail, jobs.now(), state_root(state) / "rsi" / "failure_feed.jsonl"), None, []

        outcome, err = jobs.with_git(apply, f"jobs: {agent} timer failure {claimed['id']}")
        if err or not outcome or outcome.get("action") != "retry":
            return 1
        code2, tail2, command2 = run(outcome["agent"], claimed, outcome["model"])
        if code2 == 0:
            return 0

        def apply_again(data):
            job = jobs.find(data, claimed["id"])
            if not job:
                return None, "missing job", []
            return fail_run(data, job, agent, outcome["model"], command2, tail2, jobs.now(),
                            state_root(state) / "rsi" / "failure_feed.jsonl"), None, []

        jobs.with_git(apply_again, f"jobs: {agent} timer repair {claimed['id']}")
        return 1
    finally:
        if desk:
            release_desk(desk, agent, state)
        release_lease(agent, state)
