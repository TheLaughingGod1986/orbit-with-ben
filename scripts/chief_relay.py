#!/usr/bin/env python3
"""Chief relay: whoever is first in line and has credit acts as Chief of Staff on the Mac mini (Ben, 7 Oct 2026).

Ben: "If Grok Bot is down and out of credit, Cursor takes over. If Cursor and Grok Bot are down, Codex takes over,
and so on down a chain. The Chief of Staff is ultimately in charge." So the chain is, by default:

  chief (Grok Bot)  ->  cursor (Cursor `agent` CLI)  ->  codex (Codex CLI)

The first agent in the chain that is up is the Chief. Nobody flips a switch by hand: Grok takes back over by itself
when it is active again, and a CLI that runs out of credit is skipped until its retry time, so the next one in line
takes the run.

How "up" is decided:
  chief   Grok Bot is a desktop app with no CLI; the relay can't start it, prompt it or see its credit. It counts as
          up when it has posted on the studio thread as plain "[Chief]" in the last 180 min (Cursor and Codex posts
          are tagged, and the relay's own lines are skipped), or has run `jobs.py ... --agent chief` in that time.
          Its app files are no use: they are a heartbeat written every minute while the app is open, credit or not.
          A `down` mark on Grok is cleared by either signal seen after the mark: Grok working again is proof it is back.
  cursor, codex
          up unless their CLI is missing or they are marked down. A run whose output says out of credit, over the
          usage limit, or signed out marks that agent down for --retry hours (default 3), and the same run falls
          through to the next agent in line.

  python3 scripts/chief_relay.py status                         # the chain, who is Chief, and why
  python3 scripts/chief_relay.py run                            # launchd, every 10 min: one job by the acting Chief, when one is queued
  python3 scripts/chief_relay.py seen chief                     # heartbeat (jobs.py does this for you)
  python3 scripts/chief_relay.py down chief --reason "out of credit" [--until 2026-10-12T09:00]
  python3 scripts/chief_relay.py up cursor                      # clear a down mark

`run` does nothing while Grok is Chief (Grok drives itself), outside CHIEF_HOURS (default: never), while
~/_desk/state/chief-relay.pause exists, or while a previous run holds the lock. Otherwise it wakes the acting
CLI Chief for ONE job (25-minute cap), then exits. Every change of Chief is posted to the studio thread once.

State (on the Mini, never in git): ~/_desk/state/chief/  (heartbeat/<agent>, down/<agent>.json, current.json).
Mini heartbeat (Ben, 8 Oct): every `run` also pushes one small file, heartbeat.json {at, state, agent, note}, to the
branch `mini-heartbeat` as a single parentless commit (force-pushed, so main's history stays clean). The Kanban reads
it to tell "the Mini is busy on a long job" from "the Mini is asleep". CHIEF_HEARTBEAT=0 turns it off.
Log: stdout (launchd sends it to ~/Library/Logs/chief-relay.log).
Env (the defaults find the CLIs and the HOS checkout on Ben's Mini; set these only to override): CHIEF_CHAIN (default "chief,cursor,codex"), CHIEF_HOURS (0-24: round the clock), CHIEF_CAP_S (1500), CHIEF_GROK_FRESH_MIN (180),
CHIEF_RETRY_H (3), CURSOR_AGENT_BIN / CURSOR_AGENT_FLAGS ("-p --force"), CODEX_BIN / CODEX_FLAGS (see cli_spec), AGY_BIN,
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
def first_dir(*cands) -> pathlib.Path:
    return next((c for c in cands if c.is_dir()), cands[0])


# On Ben's Mini the HOS checkout is "History Of Science" (Cursor, 7 Oct); keep the git-style name as a fallback.
HOS = pathlib.Path(os.environ.get("HOS_REPO") or first_dir(HOME / "YouTube" / "History Of Science",
                                                            HOME / "YouTube" / "history-of-science"))
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


def find_bin(env: str, name: str):
    """launchd's `zsh -lc` doesn't read .zshrc, so npm-global and ~/.local CLIs aren't on PATH there: look in the
    usual install places too."""
    cands = [os.environ.get(env), shutil.which(name)] + [str(HOME / d / name) for d in (".npm-global/bin", ".local/bin")] \
        + [f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}"]
    return next((c for c in cands if c and os.access(c, os.X_OK)), None)


def cli_spec(agent: str):
    """(binary, args) for a CLI agent, or None if it isn't installed."""
    if agent == "cursor":
        b = find_bin("CURSOR_AGENT_BIN", "agent")
        flags = os.environ.get("CURSOR_AGENT_FLAGS", "-p --force")
    elif agent == "codex":
        b = find_bin("CODEX_BIN", "codex")
        # exec = one prompt, no chat window; a workspace-write sandbox on the OWB checkout, commands approved without
        # asking; network and the extra dirs let it pull/push and use the HOS desk, like Cursor. Codex 0.160 has no
        # --full-auto (Cursor checked on the Mini, 7 Oct). Check `codex exec --help` after a Codex update.
        flags = os.environ.get("CODEX_FLAGS", f"exec -s workspace-write --approve-for-me "
                                              f"-c sandbox_workspace_write.network_access=true "
                                              f"--add-dir {shlex.quote(str(HOS))} --add-dir {shlex.quote(str(STATE.parent))}")
    else:
        return None
    return (b, shlex.split(flags)) if b else None


# Grok Bot is an app with no CLI, and its own files can't tell working from idle: dune-reliability/sessions holds a
# process heartbeat the app rewrites every minute while it's open, credit or not (Cursor, #99 6040044537). What Grok
# does when it works is post on the studio thread as plain "[Chief]". Cursor and Codex posts carry "[Cursor]" /
# "[Codex]" or "... covering", and the relay's own lines say "Chief relay:", so those don't count.
NOT_GROK = re.compile(r"\[(?:Cursor|Codex)\]|\b(?:Cursor|Codex) covering|Chief relay:|watchdog|studio\.py stale", re.I)


def fetch_comments(since: dt.datetime) -> list:
    """Studio-thread comments updated since `since`, via owb_thread.py's own auth (GH_TOKEN or `gh auth token`)."""
    sys.path.insert(0, str(OWB / "scripts"))
    import owb_thread  # noqa: E402
    return owb_thread.api("GET", f"/issues/{owb_thread.PR}/comments?since={iso(since)}&per_page=100")


def note_grok_posts(at: dt.datetime) -> None:
    """Once per relay run: the time of Grok's newest own post on the thread. If the thread can't be read, the last
    known time stays."""
    fresh = int(os.environ.get("CHIEF_GROK_FRESH_MIN", "180"))
    prev = read_json(d("grok_thread.json")) or {}
    try:
        posts = fetch_comments(at - dt.timedelta(minutes=fresh))
    except Exception as e:  # network, auth: keep what we knew
        log(f"grok check: thread not readable ({e.__class__.__name__}); keeping the last known post time")
        return
    times = [c["created_at"] for c in posts
             if c.get("body", "").lstrip().startswith("[Chief]") and not NOT_GROK.search(c["body"][:400])]
    last = max(times + ([prev["last_post"]] if prev.get("last_post") else []), default=None)
    write_json(d("grok_thread.json"), {"checked": iso(at), "last_post": last})


def grok_post_age(at: dt.datetime, after=None):
    """Minutes since Grok's newest own thread post (as of the last relay run), or None; only posts after `after`."""
    last = (read_json(d("grok_thread.json")) or {}).get("last_post")
    if not last or (after and parse(last) <= after):
        return None
    return int((at - parse(last)).total_seconds() // 60)


def state_of(agent: str, at: dt.datetime) -> tuple:
    """(up, why) for one agent in the chain."""
    mark = read_json(d("down", agent + ".json"))
    if mark:
        until = parse(mark["until"]) if mark.get("until") else None
        since = parse(mark["since"])
        beat = last_seen(agent)
        if until and at >= until:
            mark_up(agent)
        elif agent == "chief" and ((beat and beat > since) or grok_post_age(at, after=since) is not None):
            mark_up(agent)  # Grok has worked since it was marked down: it's back
        else:
            return False, f"marked down: {mark.get('reason') or 'no reason given'}" + (f" (retry after {mark['until']})" if until else "")
    if agent == "chief":
        fresh = int(os.environ.get("CHIEF_GROK_FRESH_MIN", "180"))
        beat = last_seen(agent)
        if beat and int((at - beat).total_seconds() // 60) <= fresh:
            return True, f"ran jobs.py {int((at - beat).total_seconds() // 60)} min ago"
        age = grok_post_age(at)
        if age is not None and age <= fresh:
            return True, f"posted on the thread {age} min ago"
        return False, "no Grok post on the thread in the last {} h".format(fresh // 60) + (
            f"; last jobs.py run {int((at - beat).total_seconds() // 3600)} h ago" if beat else "")
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
   anything on the NAS, and never print secrets. If a step needs Ben (money, a sign-in, a decision), say so in your
   report and stop.
   A job that needs `gemini` is a facts-and-numbers check: run it through Gemini with the `agy` CLI (AGENTS.md "Who does
   what"), claim it as {agent}/gemini, and commit Gemini's findings as the job says. You check Gemini's output is complete;
   you don't rewrite its findings or any spoken line.
5. Report: OWB with  python3 scripts/owb_thread.py post "..."  (start with "{name} covering"); HOS with
   hos_desk.py post --from {agent} --to claude ...  Say what you did, what's next, and what blocks you.
Your run is killed at 25 minutes. Anything that takes longer (a full render, a big download, a batch of picture jobs):
start it detached so it outlives you, e.g.
   tmux new -d -s <job>-render "cd <dir> && <command> > ~/_desk/logs/<job>-render.log 2>&1; echo $? > ~/_desk/logs/<job>-render.done"
then release the job with a note naming the tmux session, the log and the .done file. The next run checks that file:
missing means still running (leave it, take a quick job meanwhile); present means read the exit code and the log, and
carry on. Never start a second copy of a render that is still running.
Otherwise, if a job will take longer than about 20 minutes, stop at a clean point, release your claim with a note,
report, and stop.
"""


def log(msg: str) -> None:
    print(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def notify(text: str) -> bool:
    """Post one line on the studio thread. False (and the reason in the log) if it didn't go out, e.g. no GitHub token
    in launchd's environment."""
    cmd = os.environ.get("CHIEF_NOTIFY")
    argv = shlex.split(cmd) if cmd else [sys.executable, str(OWB / "scripts" / "owb_thread.py"), "post"]
    try:
        r = subprocess.run(argv + [text], cwd=str(OWB) if OWB.is_dir() else None, capture_output=True, text=True,
                           timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"notify failed: {e}")
        return False
    if r.returncode != 0:
        log(f"notify failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
        return False
    return True


def run_cli(agent: str, prompt: str, cap_s: int) -> tuple:
    """(exit code, tail of output). Exit 124 = killed at the cap. The whole process group is killed, so a CLI's
    child processes don't outlive the cap."""
    b, args = cli_spec(agent)
    # owb_thread.py tags its posts "[Chief] [Cursor]". PATH: launchd's shell has no Homebrew or user bins, and doesn't
    # expand "~", so put the real dirs first; the woken agent then finds gh, agy, agent and codex itself.
    extra = [str(HOME / ".local" / "bin"), str(HOME / ".npm-global" / "bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    env = dict(os.environ, OWB_AGENT=agent, PATH=os.pathsep.join(extra + [os.environ.get("PATH", "/usr/bin:/bin")]))
    p = subprocess.Popen([b] + args + [prompt], cwd=str(OWB) if OWB.is_dir() else None, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True, env=env)
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
    """Post one line on the thread when the Chief changes, then record it. If the post fails, nothing is recorded, so
    the next run tries again (the 7 Oct first run made Cursor Chief but its post never reached the thread)."""
    cur = read_json(d("current.json")) or {}
    if "agent" in cur and cur["agent"] == new:
        return
    states = "; ".join(f"{NAMES.get(a, a)}: {why}" for a, up, why in rows)
    if new is None:
        ok = notify(f"Chief relay: **nobody can act as Chief** ({states}). Mini jobs wait until one is back. "
                    f"Ben: top-ups stay your call.")
    elif new == "chief":
        ok = notify(f"Chief relay: **Grok Bot is Chief again** ({states}). Cursor and Codex stand down.")
    else:
        later = [NAMES.get(a, a) for a in chain()[chain().index(new) + 1:]]
        ok = notify(f"Chief relay: **{NAMES.get(new, new)} is acting Chief** ({states}). "
                    f"{'Next in line: ' + ', '.join(later) + '. ' if later else ''}"
                    f"Grok Bot takes back over by itself once it posts on the thread again.")
    if ok:
        write_json(d("current.json"), {"agent": new, "since": iso(at)})


def heartbeat_doc(at: dt.datetime, state: str, agent: str = "", note: str = "") -> dict:
    """What the Kanban shows about the Mini: when the relay last ran and what it found (idle, running, busy, paused)."""
    return {"at": iso(at), "state": state, "agent": agent, "note": note[:200], "host": "mac-mini"}


def push_heartbeat(at: dt.datetime, state: str, agent: str = "", note: str = "") -> None:
    """One parentless commit holding heartbeat.json, force-pushed to refs/heads/mini-heartbeat. Never raises."""
    if os.environ.get("CHIEF_HEARTBEAT", "1") == "0" or not (OWB / ".git").exists():
        return
    body = json.dumps(heartbeat_doc(at, state, agent, note)) + "\n"
    try:
        git = ["git", "-C", str(OWB)]
        blob = subprocess.run(git + ["hash-object", "-w", "--stdin"], input=body, capture_output=True, text=True,
                              timeout=30, check=True).stdout.strip()
        tree = subprocess.run(git + ["mktree"], input=f"100644 blob {blob}\theartbeat.json\n", capture_output=True,
                              text=True, timeout=30, check=True).stdout.strip()
        commit = subprocess.run(git + ["commit-tree", tree, "-m", f"mini heartbeat {iso(at)} {state}"],
                                capture_output=True, text=True, timeout=30, check=True).stdout.strip()
        subprocess.run(git + ["push", "-q", "-f", "origin", f"{commit}:refs/heads/mini-heartbeat"],
                       capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"heartbeat not pushed: {e}")


def cmd_run(at: dt.datetime) -> int:
    if (STATE / "chief-relay.pause").exists():
        log("skip: paused")
        push_heartbeat(at, "paused", note="chief-relay.pause is set")
        return 0
    lo, hi = (int(x) for x in os.environ.get("CHIEF_HOURS", "0-24").split("-"))
    h = dt.datetime.now().hour
    if not lo <= h < hi:
        log(f"skip: outside {lo}-{hi}")
        return 0
    d().mkdir(parents=True, exist_ok=True)
    with open(d("run.lock"), "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            log("skip: previous run still working")
            push_heartbeat(at, "busy", note="the previous run is still working")
            return 0
        return run_locked(at)


def queue_has_work(agent: str) -> bool:
    """Is a Mini job waiting for this agent (jobs.py next --peek)? The relay runs every 10 min (Ben, 7 Oct: one job per
    30 min left the Mini idle most of the time), but only wakes a CLI when there's work, plus a sweep every 2 h for
    thread/desk tasks outside the queue. If the queue can't be read, it wakes the agent anyway."""
    jobs = OWB / "scripts" / "jobs.py"
    if not jobs.exists():
        return True
    subprocess.run(["git", "-C", str(OWB), "pull", "-q", "--ff-only"], capture_output=True, timeout=120)
    try:
        r = subprocess.run([sys.executable, str(jobs), "next", "--agent", agent, "--can", "mini,gemini,any", "--peek"],
                           cwd=str(OWB), capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return True
    return r.returncode != 10


def addressed_to(agent: str) -> list:
    """Open jobs only this agent may claim (`jobs.py add --for <agent>`), e.g. Claude asking Codex for its own view."""
    q = read_json(OWB / "jobs" / "queue.json") or {}
    return [j["id"] for j in q.get("jobs", []) if j.get("for") == agent and j.get("status") == "open"]


def run_locked(at: dt.datetime) -> int:
    note_grok_posts(at)
    cap = int(os.environ.get("CHIEF_CAP_S", "1500"))
    retry_h = float(os.environ.get("CHIEF_RETRY_H", "3"))
    while True:
        rows, who = acting(at)
        handover(who, rows, at)
        log("chain: " + " | ".join(f"{a}={'UP' if up else 'down'} ({why})" for a, up, why in rows))
        if who is None:
            log("nobody up: nothing to run")
            push_heartbeat(at, "no-chief", note="nobody in the chain is up")
            return 0
        # A job addressed to one agent wakes that agent if it's up, ahead of the acting Chief: otherwise only the first
        # agent in the chain ever runs, and a second opinion from Codex would never happen.
        addressed = False
        for a, up, _ in rows:
            if up and a in ("cursor", "codex") and a != who and addressed_to(a):
                addressed = True
                log(f"{a} has a job addressed to it ({', '.join(addressed_to(a))}): waking it first")
                who = a
                break
        if who == "chief":
            log("Grok Bot is Chief: nothing to do")
            return 0
        last_wake = last_seen(who)
        # Overnight (Ben, 7 Oct: carry on overnight) agents are woken for queued jobs only; the 2-hourly sweep for
        # thread/desk tasks runs in the day, so an empty night costs no credit.
        slo, shi = (int(x) for x in os.environ.get("CHIEF_SWEEP_HOURS", "8-22").split("-"))
        sweep = slo <= dt.datetime.now().hour < shi and (
            not last_wake or (at - last_wake) >= dt.timedelta(minutes=int(os.environ.get("CHIEF_SWEEP_MIN", "120"))))
        if not queue_has_work(who) and not sweep:
            log(f"nothing queued for {who}; last woken {int((at - last_wake).total_seconds() // 60)} min ago: not waking it")
            push_heartbeat(at, "idle", who, "nothing queued")
            return 0
        above = [f"{NAMES.get(a, a)} is {why}" for a, up, why in rows[:[r[0] for r in rows].index(who)]]
        why = "Claude addressed a job to you by name" if addressed else ("; ".join(above) or "it is first in line")
        prompt = PROMPT.format(name=NAMES.get(who, who), agent=who, why=why,
                               owb=OWB, hos=HOS)
        log(f"run: {who} (cap {cap}s)")
        push_heartbeat(at, "running", who, f"woke {NAMES.get(who, who)} for one job (cap {cap // 60} min)")
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
    print(gemini_line())
    return 0


def gemini_line() -> str:
    """Gemini is the facts-and-numbers checker, not in the Chief chain: it can't run the Mini, so the acting Chief runs
    it (`agy`) for every job that needs gemini. Show whether it's installed and how much is waiting for it."""
    b = find_bin("AGY_BIN", "agy")
    try:
        q = json.loads((OWB / "jobs" / "queue.json").read_text())["jobs"]
        waiting = sum(1 for j in q if j.get("needs") == "gemini" and j.get("status") in ("open", "claimed"))
        jobs = f"{waiting} gemini job{'s' if waiting != 1 else ''} waiting"
    except (OSError, ValueError, KeyError):
        jobs = "queue not found"
    return (f"Checker: Gemini ({'agy found' if b else 'agy NOT found on PATH'}); run by the acting Chief; {jobs}")


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
