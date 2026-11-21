#!/usr/bin/env python3
"""Each agent runs itself (J3265, Ben 21 Nov 2026).

The relay still walks chains, checks stalls and does Chief duties, and it stays the fallback.
Set AGENT_SELF_DISPATCH=0 to leave starting work to the relay only.

An agent's own timer (scripts/agent_timer.py, one launchd job each) checks its usage flag,
takes the best ready job through the existing claim, works it, and sleeps. One agent never
runs twice (a per-agent lease). The Mini also keeps a memory floor and a cap (AGENT_MINI_CAP,
default 3) on how many of its agents run at once.

Claim order stays deadline, then the film that airs soonest, then nearest, then urgent.
Skill (the kind that lists this agent first, plus Gemini's picture and video watches) only
breaks a remaining tie. With no agent named, every job shares one skill rank.

Finishing a pipeline stage queues the next stage's job (film and stage set) unless that job
already exists. A failed run retries once on the next model in the kind's chain; the second
failure files one repair job, releases the claim, and appends a line to the self-improvement
feed (J3257) for rsi.ingest_failure when that module is present.

Studio is one desk per channel window. The desk name is studio-<slug> from the channel
registry, the same name on every machine (each machine's locks are its own). ElevenLabs and
Flow stay one at a time. Kind assembly never takes a Studio desk.

Stage handoff is off until AGENT_STAGE_HANDOFF=1. It reads the channel's own stage list and
never queues a publishing stage or a stage whose owner is Ben. A handoff error cannot undo done.

Plists are not installed by this change. Each one cds to $STUDIO_CHECKOUT.
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
# Kind for a stage whose channel file does not name one. Keys are stage names, not channels.
STAGE_KIND = {
    "topic": "review", "script": "script", "sources": "facts", "facts": "facts",
    "vo": "vo", "shots": "review", "picture": "video", "edit": "assembly",
    "thumbs": "thumb", "thumbnails": "thumb", "package": "listing", "listing": "listing",
    "shorts_scripts": "script", "shorts_vo": "vo", "qa": "qa",
}
# Publishing, and the watch that stays Ben's. Never queued from a finished stage.
SKIP_STAGES = {"upload", "ben_ok", "scheduled"}


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


def _live_state(state) -> bool:
    import chief_relay
    if state is None:
        return True
    try:
        return pathlib.Path(state).resolve() == pathlib.Path(chief_relay.STATE).resolve()
    except OSError:
        return False


def relay_rows(at: dt.datetime, state=None) -> list:
    """Live relay slot leases. A test state is read from its own chief folder, not the machine's."""
    import chief_relay
    if _live_state(state):
        return list(chief_relay.current_executions(at))
    folder = pathlib.Path(state) / "chief"
    if not folder.is_dir():
        return []
    paths = sorted(folder.glob("execution-*.json"))
    if not paths and (folder / "execution.json").is_file():
        paths = [folder / "execution.json"]
    out = []
    for path in paths:
        try:
            row = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        exp = _stamp(row.get("expiresAt")) if isinstance(row, dict) else None
        if not exp or exp <= at or not _alive(row.get("pid")):
            continue
        out.append(row)
    return out


def relay_workers(at: dt.datetime, state=None) -> set:
    return {str(row.get("worker")) for row in relay_rows(at, state) if row.get("worker")}


def mini_running(at: dt.datetime, state=None) -> int:
    """Mini agents already running, whether a timer lease or a relay slot holds them. One agent counts once."""
    held = {agent for agent in MINI_AGENTS if lease_held(agent, at, state)}
    held |= {agent for agent in relay_workers(at, state) if agent in MINI_AGENTS}
    return len(held)


def memory_ok(free_mb=None) -> bool:
    """True when free memory is at or above AGENT_MEM_FLOOR_MB. The figure is the relay's own reading."""
    floor = int(os.environ.get("AGENT_MEM_FLOOR_MB", "1536"))
    if free_mb is None:
        import chief_relay
        free_mb = chief_relay.free_memory_bytes() // (1024 * 1024)
    return int(free_mb) >= floor


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
    if agent in relay_workers(at, state):
        return False, "relay"
    if agent in MINI_AGENTS:
        cap = int(os.environ.get("AGENT_MINI_CAP", "3"))
        if mini_running(at, state) >= cap:
            return False, "cap"
        if not memory_ok(free_mb):
            return False, "memory"
    return True, ""


def channel_of(job: dict) -> str:
    """The job's channel slug, from its repo or the registry. No channel is named here."""
    import channels
    repo = str(job.get("repo") or "").lower()
    if repo in channels.slugs():
        return repo
    return channels.of_job(job)


def desk_name(job: dict, host: str = "mini") -> str:
    """The one desk this job needs, or '' when it needs none (code and tooling included).

    Studio is one name per channel, studio-<slug>, taken from the registry. `host` does not
    change it: each machine keeps its own lock files, and the browser port stays in the channel file.
    """
    del host
    kind = job.get("kind") or ""
    if kind == "vo":
        return "elevenlabs"
    if kind in ("image", "video"):
        return "flow"
    if kind != "studio":
        return ""
    return "studio-" + channel_of(job)


def timer_desk_held(name: str, agent: str, at: dt.datetime, state=None) -> bool:
    """True when an agent timer holds this desk for someone else."""
    if not name:
        return False
    row = _read_holder(state_root(state) / "desks" / f"{name}.json", at)
    return bool(row and row.get("agent") != agent)


def desk_blocks(job: dict, agent: str, state, at: dt.datetime, host: str = "mini") -> bool:
    """True when this desk is held by a timer, a relay lock, or another relay slot."""
    name = desk_name(job, host)
    if not name:
        return False
    if timer_desk_held(name, agent, at, state):
        return True
    if _live_state(state):
        import chief_relay
        if chief_relay.desk_lock_held(name):
            return True
    for row in relay_rows(at, state):
        if row.get("desk") == name and row.get("worker") != agent:
            return True
    return False


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


def handoff_on() -> bool:
    """Off until the Chief has checked one film per channel (AGENT_STAGE_HANDOFF=1)."""
    return os.environ.get("AGENT_STAGE_HANDOFF", "0") == "1"


def next_stage(job: dict):
    """(stage, kind, needs, title) from this channel's own stage list, or None.

    The next key is the one after the job's stage. A publishing stage, a stage with no
    successor, and a stage owned by Ben are not queued.
    """
    if not job.get("film") or not job.get("stage"):
        return None
    import channels
    slug = channel_of(job)
    keys = channels.stage_keys(slug)
    stage = str(job.get("stage") or "")
    if stage not in keys:
        return None
    idx = keys.index(stage) + 1
    if idx >= len(keys):
        return None
    nxt = keys[idx]
    defs = {row["key"]: row for row in channels.stage_defs(slug)}
    row = defs.get(nxt) or {}
    if nxt in SKIP_STAGES or str(row.get("owner") or "").lower() == "ben":
        return None
    kind = str(row.get("kind") or STAGE_KIND.get(nxt) or "")
    if not kind or kind in ("studio", "chief"):
        return None
    label = str(row.get("label") or nxt)
    title = f"{label} for {job['film']}"
    return nxt, kind, "any", title


def queue_next(data: dict, job: dict, agent: str, at: dt.datetime):
    """Queue the channel's next stage once. None when the switch is off, or one already exists.

    Dedupe is film + stage + channel, whatever the kind. Default off: AGENT_STAGE_HANDOFF=1 to arm it.
    """
    if not handoff_on() or not job.get("film") or job.get("kind") == "chief" or job.get("needs") == "ben" or job.get("awaits_ben"):
        return None
    spec = next_stage(job)
    if not spec:
        return None
    stage, kind, needs, title = spec
    import channels
    slug = channel_of(job)
    if any(j.get("film") == job["film"] and j.get("stage") == stage and channel_of(j) == slug
           and j.get("status") in OPEN and j.get("id") != job.get("id")
           for j in data["jobs"]):
        return None
    import jobs
    body = (f"Queued when {job['id']} finished its stage. Film {job['film']}. "
            "£0. Ben's watch, money and publishing stay gated.")
    new = jobs.do_add(data, title=title, needs=needs, body=body, by=agent or "relay", at=at,
                      film=str(job["film"]), stage=stage, kind=kind, repo=slug or channels.default(),
                      action=title[:180])
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
        if nxt[0] == agent:
            jobs.log(job, at, agent, f"retry once in place on {nxt[1]}")
            return {"action": "retry", "agent": agent, "model": nxt[1]}
        # A different agent must claim the job itself. Running it inside this lease breaks its own jobs.py calls.
        if job.get("status") == "claimed" and job.get("by") == agent:
            jobs.do_release(job, agent, f"self_retry on {nxt[0]} {nxt[1]}", at)
        else:
            jobs.log(job, at, agent, f"self_retry on {nxt[0]} {nxt[1]}")
        return {"action": "released", "agent": nxt[0], "model": nxt[1]}
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
        if outcome.get("action") == "retry" and outcome.get("agent") == agent:
            code2, tail2, command2 = run(agent, job, outcome["model"])
            if code2 == 0:
                return {"started": True, "ok": True, "job": job["id"], "retried": True}
            outcome = fail_run(data, job, agent, outcome["model"], command2, tail2, at, feed)
        return {"started": True, "ok": False, "job": job["id"], **outcome}
    finally:
        if desk:
            release_desk(desk, agent, state)
        release_lease(agent, state)


def plist_label(agent: str) -> str:
    """Launchd label. The channel slug comes from the registry, not from a name written here."""
    import channels
    return "com." + channels.default() + ".agent." + agent


def plist_body(agent: str, minutes: int) -> str:
    label = plist_label(agent)
    command = (f'cd "$STUDIO_CHECKOUT" &amp;&amp; python3 scripts/agent_timer.py tick --agent {agent} '
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
        path = folder / (plist_label(agent) + ".plist")
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
        if err or not outcome or outcome.get("action") != "retry" or outcome.get("agent") != agent:
            return 0 if outcome and outcome.get("action") == "released" else 1
        code2, tail2, command2 = run(agent, claimed, outcome["model"])
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
