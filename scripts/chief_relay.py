#!/usr/bin/env python3
"""Chief relay: whoever is first in line and has credit acts as Chief of Staff on the Mac mini (Ben, 7 Oct 2026).

Ben: "If Grok Bot is down and out of credit, Cursor takes over. If Cursor and Grok Bot are down, Codex takes over,
and so on down a chain. The Chief of Staff is ultimately in charge." So the chain is, by default:

  chief (Grok Bot)  ->  cursor (Cursor `agent` CLI)  ->  codex (Codex CLI)

The first agent in the chain that is up is the Chief. Nobody flips a switch by hand: Grok takes back over by itself
when it is active again, and a CLI that runs out of credit is skipped until its retry time, so the next one in line
takes the run.

How "up" is decided:
  chief   Grok Bot is a desktop app; the relay can't start it or see its credit. It counts as up while its heartbeat
          is fresh (default 180 min). The heartbeat is touched every time Grok runs `jobs.py ... --agent chief`
          (every session and loop starts with `jobs.py next`), or `chief_relay.py seen chief`. A `down` mark on Grok
          is cleared by any later heartbeat: Grok working again is proof it is back.
  cursor, codex
          up unless their CLI is missing or they are marked down. A run whose output says out of credit, over the
          usage limit, or signed out marks that agent down for --retry hours (default 3), and the same run falls
          through to the next agent in line.

  python3 scripts/chief_relay.py status                         # the chain, who is Chief, and why
  python3 scripts/chief_relay.py run                            # launchd, every 30 min: one job by the acting Chief
  python3 scripts/chief_relay.py seen chief                     # heartbeat (jobs.py does this for you)
  python3 scripts/chief_relay.py down chief --reason "out of credit" [--until 2026-10-12T09:00]
  python3 scripts/chief_relay.py up cursor                      # clear a down mark

`run` does nothing while Grok is Chief (Grok drives itself), outside 08:00-22:00 local, while
~/_desk/state/chief-relay.pause exists, or while a previous run holds the lock. Otherwise it wakes the acting
CLI Chief for ONE job (25-minute cap), then exits. Every change of Chief is posted to the studio thread once.

State (on the Mini, never in git): ~/_desk/state/chief/  (heartbeat/<agent>, down/<agent>.json, current.json).
Log: stdout (launchd sends it to ~/Library/Logs/chief-relay.log).
Env: CHIEF_CHAIN (default "chief,cursor,codex"), CHIEF_HOURS (8-22), CHIEF_CAP_S (1500), CHIEF_GROK_FRESH_MIN (180),
CHIEF_RETRY_H (3), CURSOR_AGENT_BIN / CURSOR_AGENT_FLAGS ("-p --force"), CODEX_BIN / CODEX_FLAGS (see CLI below),
OWB_REPO, HOS_REPO, DESK_STATE, CHIEF_NOTIFY (command that posts a line; default owb_thread.py post).
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import pathlib
import re
import shlex
import shutil
import signal
import subprocess
import sys

HOME = pathlib.Path.home()
STATE = pathlib.Path(os.environ.get("DESK_STATE", HOME / "_desk" / "state"))
OWB = pathlib.Path(os.environ.get("OWB_REPO", HOME / "YouTube" / "orbit-with-ben"))
HOS = pathlib.Path(os.environ.get("HOS_REPO", HOME / "YouTube" / "history-of-science"))
DEFAULT_CHAIN = "chief,cursor,codex"
NAMES = {"chief": "Grok Bot", "cursor": "Cursor", "codex": "Codex"}

# What an out-of-credit, over-limit or signed-out CLI says. Only read when the run failed or printed almost nothing,
# so a job that merely talks about a YouTube quota doesn't count.
CREDIT_RE = re.compile(
    r"out of (?:credit|credits|tokens)|insufficient (?:credit|credits|balance|quota)|usage limit|rate[- ]limit|"
    r"quota (?:exceeded|exhausted)|exceeded your (?:current )?quota|payment required|billing|upgrade (?:your|to) |"
    r"limit (?:reached|exceeded)|hit your .*limit|not logged in|log ?in required|please (?:log|sign) ?in|"
    r"unauthori[sz]ed|authentication (?:failed|required)|\b402\b|\b429\b",
    re.I)


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> dt.datetime:
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return t if t.tzinfo else t.astimezone()  # a bare local time from Ben's --until


def chain() -> list:
    return [a.strip() for a in os.environ.get("CHIEF_CHAIN", DEFAULT_CHAIN).split(",") if a.strip()]


def d(*parts) -> pathlib.Path:
    return STATE.joinpath("chief", *parts)


def read_json(p: pathlib.Path):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def write_json(p: pathlib.Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(p)


# ---- heartbeat and down marks ----

def seen(agent: str, at: dt.datetime | None = None) -> None:
    p = d("heartbeat", agent)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(iso(at or now()) + "\n")


def last_seen(agent: str):
    try:
        return parse(d("heartbeat", agent).read_text().strip())
    except (OSError, ValueError):
        return None


def mark_down(agent: str, reason: str, until, at: dt.datetime) -> None:
    write_json(d("down", agent + ".json"), {"since": iso(at), "until": iso(until) if until else None, "reason": reason})


def mark_up(agent: str) -> None:
    try:
        d("down", agent + ".json").unlink()
    except OSError:
        pass


def cli_spec(agent: str):
    """(binary, args) for a CLI agent, or None if it isn't installed."""
    if agent == "cursor":
        b = os.environ.get("CURSOR_AGENT_BIN") or shutil.which("agent") or str(HOME / ".local" / "bin" / "agent")
        flags = os.environ.get("CURSOR_AGENT_FLAGS", "-p --force")
    elif agent == "codex":
        b = os.environ.get("CODEX_BIN") or shutil.which("codex") or "/opt/homebrew/bin/codex"
        # exec = one prompt, no chat window. --full-auto = run commands without asking, inside a sandbox that may
        # write to the OWB checkout; the extra dirs and network let it pull/push and use the HOS desk, like Cursor.
        flags = os.environ.get("CODEX_FLAGS", f"exec --full-auto -c sandbox_workspace_write.network_access=true "
                                              f"--add-dir {shlex.quote(str(HOS))} --add-dir {shlex.quote(str(STATE.parent))}")
    else:
        return None
    return (b, shlex.split(flags)) if os.access(b, os.X_OK) else None


def state_of(agent: str, at: dt.datetime) -> tuple:
    """(up, why) for one agent in the chain."""
    mark = read_json(d("down", agent + ".json"))
    if mark:
        until = parse(mark["until"]) if mark.get("until") else None
        beat = last_seen(agent)
        if until and at >= until:
            mark_up(agent)
        elif agent == "chief" and beat and beat > parse(mark["since"]):
            mark_up(agent)  # Grok has run jobs.py since it was marked down: it's back
        else:
            return False, f"marked down: {mark.get('reason') or 'no reason given'}" + (f" (retry after {mark['until']})" if until else "")
    if agent == "chief":
        fresh = int(os.environ.get("CHIEF_GROK_FRESH_MIN", "180"))
        beat = last_seen(agent)
        if not beat:
            return False, "no heartbeat yet (it hasn't run jobs.py on this Mini)"
        age = int((at - beat).total_seconds() // 60)
        return (True, f"active {age} min ago") if age <= fresh else (False, f"quiet for {age // 60} h {age % 60} min")
    if agent in ("cursor", "codex"):
        return (True, "ready") if cli_spec(agent) else (False, "CLI not installed")
    return False, "unknown agent"


def acting(at: dt.datetime):
    """The chain with each agent's state, and the first one that's up (or None)."""
    rows = [(a,) + state_of(a, at) for a in chain()]
    return rows, next((a for a, up, _ in rows if up), None)


# ---- the run ----

PROMPT = """You are {name}, acting as Chief of Staff on the Mac mini because {why}. You run unattended: do ONE job, then stop.
Your agent id is `{agent}` everywhere (jobs.py --agent, studio.py --by, hos_desk.py --as/--from).

1. Orbit With Ben ({owb}): git pull. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben", "Who does what",
   "Chief relay"). Run: python3 scripts/owb_thread.py read   and   python3 scripts/studio.py board
2. History of Science ({hos}): git pull. Read its AGENTS.md ("The desk"). Run its desk inbox: hos_desk.py inbox --as {agent}
3. First the job queue (AGENTS.md "Job queue"):  python3 scripts/jobs.py next --agent {agent} --can mini,gemini,any --git
   If it prints a job, that job is yours: do it (step 4), then  jobs.py done|block|release <id> --agent {agent} ... --git.
   Only if it exits 10 (nothing waiting): pick the single oldest task for the Chief that isn't in the queue (on the HOS
   desk, or a Claude message on #99 asking the Chief for something with no Chief reply yet).
   If nothing is waiting anywhere, stop without posting.
4. Do that one task, following that repo's AGENTS.md exactly: claim before work (studio.py claim --git, or the HOS
   desk's own rule), commit only from a clean worktree, never spend money or credit beyond the written rules, never
   upload, schedule, retitle or change privacy on YouTube unless Claude's message for that task says to, never delete
   anything on the NAS, and never print secrets. You drive Gemini (`agy`) for fact checks, as the Chief does. If a step
   needs Ben (money, a sign-in, a decision), say so in your report and stop.
5. Report: OWB with  python3 scripts/owb_thread.py post "..."  (start with "{name} covering"); HOS with
   hos_desk.py post --from {agent} --to claude ...  Say what you did, what's next, and what blocks you.
If a job will take longer than about 20 minutes, do a clean stopping point, release or renew your claim, report, and stop.
"""


def log(msg: str) -> None:
    print(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def notify(text: str) -> None:
    cmd = os.environ.get("CHIEF_NOTIFY")
    argv = shlex.split(cmd) if cmd else [sys.executable, str(OWB / "scripts" / "owb_thread.py"), "post"]
    try:
        subprocess.run(argv + [text], cwd=str(OWB) if OWB.is_dir() else None, capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"notify failed: {e}")


def run_cli(agent: str, prompt: str, cap_s: int) -> tuple:
    """(exit code, tail of output). Exit 124 = killed at the cap. The whole process group is killed, so a CLI's
    child processes don't outlive the cap."""
    b, args = cli_spec(agent)
    p = subprocess.Popen([b] + args + [prompt], cwd=str(OWB) if OWB.is_dir() else None, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=cap_s)
        code = p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        try:
            out, _ = p.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            out, _ = p.communicate()
        code = 124
    out = out or ""
    sys.stdout.write(out[-20000:])
    return code, out[-4000:]


def out_of_credit(code: int, tail: str) -> bool:
    if code == 124:
        return False  # it was working when the cap hit
    return bool(CREDIT_RE.search(tail)) and (code != 0 or len(tail.strip()) < 600)


def handover(new, rows, at: dt.datetime) -> None:
    """Record who is Chief; post one line on the thread when it changes."""
    cur = read_json(d("current.json")) or {}
    if "agent" in cur and cur["agent"] == new:
        return
    write_json(d("current.json"), {"agent": new, "since": iso(at)})
    states = "; ".join(f"{NAMES.get(a, a)}: {why}" for a, up, why in rows)
    if new is None:
        notify(f"Chief relay: **nobody can act as Chief** ({states}). Mini jobs wait until one is back. "
               f"Ben: top-ups stay your call.")
    elif new == "chief":
        notify(f"Chief relay: **Grok Bot is Chief again** ({states}). Cursor and Codex stand down.")
    else:
        later = [NAMES.get(a, a) for a in chain()[chain().index(new) + 1:]]
        notify(f"Chief relay: **{NAMES.get(new, new)} is acting Chief** ({states}). "
               f"{'Next in line: ' + ', '.join(later) + '. ' if later else ''}"
               f"Grok Bot takes back over by itself once it runs jobs.py again.")


def cmd_run(at: dt.datetime) -> int:
    if (STATE / "chief-relay.pause").exists():
        log("skip: paused")
        return 0
    lo, hi = (int(x) for x in os.environ.get("CHIEF_HOURS", "8-22").split("-"))
    h = dt.datetime.now().hour
    if not lo <= h < hi:
        log(f"skip: outside {lo}-{hi}")
        return 0
    d().mkdir(parents=True, exist_ok=True)
    lock = open(d("run.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("skip: previous run still working")
        return 0
    cap = int(os.environ.get("CHIEF_CAP_S", "1500"))
    retry_h = float(os.environ.get("CHIEF_RETRY_H", "3"))
    while True:
        rows, who = acting(at)
        handover(who, rows, at)
        log("chain: " + " | ".join(f"{a}={'UP' if up else 'down'} ({why})" for a, up, why in rows))
        if who is None:
            log("nobody up: nothing to run")
            return 0
        if who == "chief":
            log("Grok Bot is Chief: nothing to do")
            return 0
        above = [f"{NAMES.get(a, a)} is {why}" for a, up, why in rows[:[r[0] for r in rows].index(who)]]
        prompt = PROMPT.format(name=NAMES.get(who, who), agent=who, why="; ".join(above) or "it is first in line",
                               owb=OWB, hos=HOS)
        log(f"run: {who} (cap {cap}s)")
        seen(who, at)
        code, tail = run_cli(who, prompt, cap)
        log(f"done: {who} exit {code}")
        if out_of_credit(code, tail):
            until = now() + dt.timedelta(hours=retry_h)
            mark_down(who, "out of credit or signed out (its last run said so)", until, now())
            log(f"{who} looks out of credit or signed out: down until {iso(until)}; trying the next in line")
            at = now()
            continue
        if code not in (0, 124):
            notify(f"Chief relay: {NAMES.get(who, who)}'s run failed (exit {code}). Log: ~/Library/Logs/chief-relay.log")
        return 0


def cmd_status(at: dt.datetime) -> int:
    rows, who = acting(at)
    for a, up, why in rows:
        print(f"{'>' if a == who else ' '} {a:<7} {NAMES.get(a, a):<9} {'UP  ' if up else 'down'}  {why}")
    print(f"Chief: {NAMES.get(who, who) if who else 'nobody'}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("run")
    s = sub.add_parser("seen")
    s.add_argument("agent")
    dn = sub.add_parser("down")
    dn.add_argument("agent")
    dn.add_argument("--reason", default="")
    dn.add_argument("--until", default="", help="ISO time; local if no zone. Omit: until `up` (or, for Grok, its next heartbeat)")
    u = sub.add_parser("up")
    u.add_argument("agent")
    a = ap.parse_args(argv)
    at = now()
    if a.cmd == "status":
        return cmd_status(at)
    if a.cmd == "run":
        return cmd_run(at)
    if a.cmd == "seen":
        seen(a.agent, at)
    elif a.cmd == "down":
        mark_down(a.agent, a.reason, parse(a.until) if a.until else None, at)
    elif a.cmd == "up":
        mark_up(a.agent)
    return cmd_status(at)


if __name__ == "__main__":
    sys.exit(main())
