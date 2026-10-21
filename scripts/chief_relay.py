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

Fallback chains (Ben, 11 Oct 2026 23:40: "if Claude Code is out of usage you can use a Claude model in Cursor"; 23:47:
"remember we also have Gemini and Codex"). Each job kind has a chain in routing.CHAINS, e.g. a Claude job:
Claude Code -> Cursor on the Claude model (`agent --model claude-opus-5-5`) -> Gemini (`agy -p`) -> Codex gpt-6-astra;
code and graphics start at Codex. Every `run` walks them:
  - Claude counts as out of usage when it is marked down (`chief_relay.py down claude --reason "usage limit" --until
    ...`), a Claude ledger note in the last CHIEF_CLAUDE_OUT_H hours (default 5) says it hit a limit (`ai_spend.py
    record --pool claude --note "hit the 5-hour limit"`), or Claude blocked a queue job with a usage/limit reason
    (that also marks it down for CHIEF_RETRY_H). Its waiting jobs then go to the next worker up in their chain with
    `jobs.py reroute`, addressed to that worker, so the same run wakes it instead of leaving the job parked.
  - A Cursor, Codex or Gemini run that ends in a usage/limit/sign-in error marks that worker down and the job goes to
    the next worker up in its chain in the same run; a rerouted job whose worker has since run out walks on.
  - Each run is logged with the worker and model that actually ran it: "ran: J0300 by cursor on claude-opus-5-5
    (lane 2 of 4)" here, and a line in ~/_desk/state/chief/runs.jsonl.

`run` does nothing while Grok is Chief (Grok drives itself), outside CHIEF_HOURS (default: never), while
~/_desk/state/chief-relay.pause exists, or while a previous run holds the lock. Otherwise it wakes the acting
CLI Chief for ONE job (25-minute cap), then exits. Every change of Chief is posted to the studio thread once.

State (on the Mini, never in git): ~/_desk/state/chief/  (heartbeat/<agent>, down/<agent>.json, current.json).
Mini heartbeat (Ben, 8 Oct): every `run` also pushes one small file, heartbeat.json {at, state, agent, note}, to the
branch `mini-heartbeat` as a single parentless commit (force-pushed, so main's history stays clean). The Kanban reads
it to tell "the Mini is busy on a long job" from "the Mini is asleep". CHIEF_HEARTBEAT=0 turns it off.
Log: stdout (launchd sends it to ~/Library/Logs/chief-relay.log).
Env (the defaults find the CLIs and the HOS checkout on Ben's Mini; set these only to override): CHIEF_CHAIN (default "chief,claude,cursor,codex"), CHIEF_HOURS (0-24: round the clock), CHIEF_CAP_S (1500), CHIEF_GROK_FRESH_MIN (180),
CHIEF_RETRY_H (1), CHIEF_CLAUDE_OUT_H (5), CURSOR_CLAUDE_MODEL (routing.py), CURSOR_AGENT_BIN / CURSOR_AGENT_FLAGS ("-p --force"), CODEX_BIN (Codex's flags are fixed in cli_spec; CODEX_FLAGS is ignored), AGY_BIN,
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
import time

HOME = pathlib.Path.home()
STATE = pathlib.Path(os.environ.get("DESK_STATE", HOME / "_desk" / "state"))
OWB = pathlib.Path(os.environ.get("OWB_REPO", HOME / "YouTube" / "orbit-with-ben"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import routing  # noqa: E402  (AGENTS.md "Who does what": job kind -> worker and model)


def first_dir(*cands) -> pathlib.Path:
    return next((c for c in cands if c.is_dir()), cands[0])


# On Ben's Mini the HOS checkout is "History Of Science" (Cursor, 7 Oct); keep the git-style name as a fallback.
HOS = pathlib.Path(os.environ.get("HOS_REPO") or first_dir(HOME / "YouTube" / "History Of Science",
                                                            HOME / "YouTube" / "history-of-science"))
# Ben, 21 Oct 2026: "build in a method where we identify dynamically if the acting chief is out and delegate a chief
# until the main one or next in command is back". Claude is a standing link (up while its hourly heartbeat is fresh),
# not only a dated override, so Grok going quiet hands Chief to Claude before the Mini CLIs.
DEFAULT_CHAIN = "chief,claude,cursor,codex"
NAMES = {"chief": "Grok Bot", "cursor": "Cursor", "codex": "Codex", "gemini": "Gemini", "claude": "Claude"}

# What an out-of-credit, over-limit or signed-out CLI says. Only read when the run failed or printed almost nothing,
# so a job that merely talks about a YouTube quota doesn't count.
CREDIT_RE = re.compile(
    r"out of (?:credit|credits|tokens)|insufficient (?:credit|credits|balance|quota)|usage limit|rate[- ]limit|"
    r"quota (?:exceeded|exhausted)|exceeded your (?:current )?quota|payment required|billing|upgrade (?:your|to) |"
    r"limit (?:reached|exceeded)|hit your .*limit|not logged in|log ?in required|please (?:log|sign) ?in|"
    r"unauthori[sz]ed|authentication (?:failed|required)|\b402\b|\b429\b",
    re.I)

# What Claude (Claude Code or a cloud session) says when it is out of usage: the CLI phrases above, plus the way agents
# write it in a note or a block reason ("hit the 5-hour limit", "Claude Code out of usage", "weekly limit").
CLAUDE_LIMIT_RE = re.compile(CREDIT_RE.pattern + r"|out of usage|\bhit (?:the|its|my|our|a) .*limit|"
                             r"(?:5-hour|five-hour|weekly|session|usage) (?:limit|cap)|usage (?:cap|exhausted)", re.I)


# A CLI saying one model's pool is spent, not the whole agent (Cursor Ultra: "hit your usage limit for Opus ... Switch
# to a different model").
MODEL_LIMIT_RE = re.compile(r"usage limit for \w|switch to a different model", re.I)
# A CLI that doesn't know the model it was given (a renamed or mistyped id): flag that model, keep the worker up.
UNKNOWN_MODEL_RE = re.compile(r"(?:unknown|invalid|unsupported|unrecognized|unrecognised) model|model\b[^\n]{0,60}"
                              r"(?:not found|not available|does not exist|isn't available|is not supported)", re.I)


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


def mark_model_down(model: str, reason: str, until: dt.datetime, at: dt.datetime) -> None:
    """One model is out of credit while its worker's other models still run (routing.SEPARATE_POOLS: Claude-in-Cursor
    bills Cursor's "Other Models" pool, Cursor Auto its own; Ben, 14 Oct 2026)."""
    write_json(d("down_models", model + ".json"), {"since": iso(at), "until": iso(until), "reason": reason})


def load_out(at: dt.datetime) -> dict:
    """Out-of-credit flags in force this run: scripts/credit_flags.json (committed by Claude or Chief, with the known
    reset time) plus the relay's own model marks. Sets routing.OUT so every chain skips those lanes. {id: reason}."""
    flags = routing.read_flags(at, str(OWB / "scripts" / "credit_flags.json"))
    for p in sorted(d("down_models").glob("*.json")) if d("down_models").is_dir() else []:
        m = read_json(p) or {}
        try:
            until = parse(m["until"])
        except (KeyError, ValueError, TypeError):
            until = at
        if until > at:
            flags.setdefault(p.stem, f"{m.get('reason') or 'out of credit'} (until {m['until']})")
        else:
            p.unlink(missing_ok=True)
    routing.OUT = set(flags)
    return flags


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


def cursor_default_out(at: dt.datetime):
    """The mark left when Cursor's own default model (Opus on the Mini) ran out, while it lasts; else None."""
    m = read_json(d("cursor_default_out.json")) or {}
    try:
        return m if m.get("until") and at < parse(m["until"]) else None
    except (ValueError, TypeError):
        return None


def cli_spec(agent: str, model: str = ""):
    """(binary, args) for a CLI agent, or None if it isn't installed. `model` (from scripts/routing.py, AGENTS.md "Who
    does what") is passed to Codex as `-m`. Cursor stays on its own Auto setting unless the model is one it runs by
    name: cursor-claude-opus-5-5 (a Claude job while Claude Code is out of usage) adds `--model claude-opus-5-5`."""
    if agent == "cursor":
        b = find_bin("CURSOR_AGENT_BIN", "agent")
        flags = os.environ.get("CURSOR_AGENT_FLAGS", "-p --force")
        cm = routing.cli_model(model) if routing.RUNS_ON.get(model) == "cursor" else ""
        if not cm and model != "cursor-auto":
            # Ben, 15 Oct 2026: "Cursor doesn't always have to be on Auto, it could be on Grok 4.7". A job with no
            # Cursor model of its own runs on Grok 4.7; on Auto when Grok is flagged, or when Cursor's default model
            # hit its pool limit ("You've hit your usage limit for Opus ... Switch to a different model", 03:40Z).
            if cursor_default_out(now()) or not routing.lane_ok("cursor", "cursor-grok-4-7"):
                cm = os.environ.get("CURSOR_FALLBACK_MODEL", "auto")
            else:
                cm = routing.cli_model("cursor-grok-4-7")
        if cm:
            flags = f"{flags} --model {shlex.quote(cm)}"
    elif agent == "codex":
        b = find_bin("CODEX_BIN", "codex")
        # exec = one prompt, no chat window; --approve-for-me = workspace-write sandbox with approvals auto-reviewed;
        # network and the extra dirs let it pull/push and use the HOS desk, like Cursor. Codex 0.160 has no
        # --full-auto, and rejects -s together with --approve-for-me (exit 2, 8 Oct). Check `codex exec --help` after
        # a Codex update.
        # The flags live here only: a stale CODEX_FLAGS left by an old `launchctl setenv` overrode this default for
        # three runs on 8 Oct (all exit 2), so the env is ignored and only noted in the log.
        if os.environ.get("CODEX_FLAGS"):
            log("CODEX_FLAGS is set in the environment and ignored; the flags come from cli_spec()")
        flags = (f"exec --approve-for-me -c sandbox_workspace_write.network_access=true "
                 f"--add-dir {shlex.quote(str(HOS))} --add-dir {shlex.quote(str(STATE.parent))}")
        if model.startswith("gpt-"):
            flags = flags.replace("exec ", f"exec -m {shlex.quote(model)} ", 1)
    elif agent == "gemini":
        # Gemini via Antigravity `agy` (Ben, 11 Oct 23:47: "remember we also have Gemini and Codex"): a stand-in in the
        # job chains (routing.CHAINS) when Cursor or Codex are out. -p = one prompt, print, exit (as in `agy -p` fact
        # checks since 8 Oct); --dangerously-skip-permissions is agy's unattended mode, like Cursor's --force.
        # `-p` takes the next argument as the prompt, so it goes last, straight before the prompt run_cli appends.
        # With `-p` first, agy read --dangerously-skip-permissions as its prompt and exited 2 on every wake (Cursor,
        # #99 6136609471; 88 "run failed" posts 13-14 Oct).
        b = find_bin("AGY_BIN", "agy")
        flags = os.environ.get("AGY_FLAGS", f"--dangerously-skip-permissions --add-dir {shlex.quote(str(HOS))} "
                                            f"--add-dir {shlex.quote(str(STATE.parent))}")
        cm = routing.cli_model(model) if routing.RUNS_ON.get(model) == "gemini" else ""
        if cm:
            flags = f"{flags} --model {shlex.quote(cm)}"
        flags = shlex.join([a for a in shlex.split(flags) if a != "-p"] + ["-p"])
    else:
        return None
    return (b, shlex.split(flags)) if b else None


# Grok Bot is an app with no CLI, and its own files can't tell working from idle: dune-reliability/sessions holds a
# process heartbeat the app rewrites every minute while it's open, credit or not (Cursor, #99 6040044537). What Grok
# does when it works is post on the studio thread as plain "[Chief]". Cursor and Codex posts carry "[Cursor]" /
# "[Codex]" or "... covering", and the relay's own lines say "Chief relay:", so those don't count. Gemini's and Claude's
# posts don't either (14 Oct 2026: "[Chief] Gemini covering — J0236 ..." read as Grok, so the relay announced "Grok Bot
# is Chief again" while Grok was out of credit, ending Ben's Claude-as-Chief order early).
# "[relay]" too: the relay's own "[Chief] [relay] @Chief stale reviews" post was read as Grok on 15 Oct 2026 01:01Z and
# made "Grok Bot is Chief again" while Grok was out of credit.
NOT_GROK = re.compile(r"\[(?:Cursor|Codex|Gemini|Claude|relay)\]|\b(?:Cursor|Codex|Gemini|Claude) covering|Chief relay:"
                      r"|watchdog|studio\.py stale|Generated by \[Claude Code\]", re.I)


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
    # The thread was read, so the window's posts are all here: a remembered time inside the window that isn't among
    # them was a misread (a worker post taken for Grok's) and is dropped; an older one just ages out.
    cutoff = at - dt.timedelta(minutes=fresh)
    old = prev.get("last_post") if prev.get("last_post") and parse(prev["last_post"]) < cutoff else None
    last = max(times + ([old] if old else []), default=None)
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
    flag = routing.read_flags(at, str(OWB / "scripts" / "credit_flags.json")).get(agent)
    if flag and not (agent == "chief" and grok_post_age(at) is not None
                     and grok_post_age(at) <= int(os.environ.get("CHIEF_GROK_FRESH_MIN", "180"))):
        return False, f"flagged out of credit: {flag}"   # Grok posting again proves it's back, flag or not
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
    if agent == "claude":
        out, why = claude_out(at, read_json(OWB / "jobs" / "queue.json") or {})
        if out:
            return False, why
        beat = ((read_json(d("claude_beat.json")) or {}).get("beat") or {}).get("at")
        if not beat:
            return False, "no heartbeat yet"
        return True, f"heartbeat {int((at - parse(beat)).total_seconds() // 60)} min ago"
    if agent in routing.MINI_WORKERS:
        return (True, "ready") if cli_spec(agent) else (False, "CLI not installed")
    return False, "unknown agent"


def override(at: dt.datetime):
    """Ben's standing order naming a Chief outside the Mini chain (scripts/chief_override.json), while it holds:
    {"agent": "claude", "until": ISO, "reason": ...}. Ben, 14 Oct 2026: "Grokbot is out of credits until Friday, so you
    should be taking over as the main agent to run this as chief." Grok posting on the thread again ends it early."""
    o = read_json(OWB / "scripts" / "chief_override.json") or {}
    try:
        until = parse(o["until"])
    except (KeyError, ValueError, TypeError):
        return None
    return o if o.get("agent") and at < until else None


def acting(at: dt.datetime):
    """The chain with each agent's state, and the first one that's up (or None). Ben's override (a Chief such as
    Claude, who isn't woken on the Mini) comes after Grok and ahead of the Mini CLIs."""
    rows = [(a,) + state_of(a, at) for a in chain()]
    first = next((a for a, up, _ in rows if up), None)
    o = override(at)
    if o and o.get("agent") in chain():
        return rows, first   # already a link in the chain: its own up/down state decides
    if o and o.get("agent") == "claude" and first != "chief":
        out, why = claude_out(at, read_json(OWB / "jobs" / "queue.json") or {})
        if out:
            # Ben, 14 Oct 2026: while Claude is out of usage the next one down runs as Chief, and Claude takes it back
            # by itself when its heartbeat returns.
            return rows + [("claude", False, f"named Chief by Ben, but out of usage ({why})")], first
    if o and first != "chief":
        return rows + [(o["agent"], True, f"named Chief by Ben until {o['until']}")], o["agent"]
    return rows, first


def cloud_chief(who) -> bool:
    """A Chief that isn't a Mini CLI (Grok Bot, or Claude under Ben's override): the Mini CLIs are its workers."""
    return who is not None and who not in routing.MINI_WORKERS


# ---- the run ----

PROMPT = """You are {name}, acting as Chief of Staff on the Mac mini because {why}. You run unattended: do ONE job, then stop.
Your agent id is `{agent}` everywhere (jobs.py --agent, studio.py --by, hos_desk.py --as/--from).

0. If a git pull fails (no space left, or local files in the way), run  python3 scripts/mini_repair.py --apply
   (safe: caches, clean temp worktrees; blocking files are kept in ~/_desk/rescue, local edits stashed, local commits
   pushed to a rescue branch first) and pull again. Still under 20 GB free: move render scratch to the NAS by
   AGENTS.md "Render scratch" before anything else.
1. Orbit With Ben ({owb}): git pull. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben", "Who does what",
   "Chief relay"). Run: python3 scripts/owb_thread.py read   and   python3 scripts/studio.py board
2. History of Science ({hos}): git pull. Read its AGENTS.md ("The desk"). Run its desk inbox:
     python3 00_Brand/Channel-Setup/tools/hos_desk.py inbox --as {agent}   (run in the HOS checkout; there is no scripts/hos_desk.py)
3. Which channel first (Ben, 9 Oct: 4 videos a month on each channel; credits follow):
     python3 scripts/channel_balance.py --hos "{hos}"
   If it says History of Science first: take the single oldest HOS desk task you can do now, and go to step 4. Only if
   there is none, fall through to the OWB queue below.
   Queue jobs marked `hos` (repo: hos, e.g. "HOS 007 Shorts VO") are NOT HOS desk tasks: they are normal queue jobs
   that `jobs.py next` hands out like any other. Do them in the HOS checkout, following its AGENTS.md. "HOS desk tasks"
   means only desk #180 messages that are not in the queue.
   The OWB job queue (AGENTS.md "Job queue"):  python3 scripts/jobs.py next --agent {agent} --can mini,gemini,any --git
   If it prints a job, that job is yours: do it (step 4), then  jobs.py done|block|release <id> --agent {agent} ... --git.
   Ben watches % done on the board: split the job into n steps (keep n from any earlier `progress` on it) and run
     python3 scripts/jobs.py progress <id> --agent {agent} --step <k> --of <n> --git
   with k=0 when you start and again after each finished step (k = steps done), before you release or finish.
   As soon as you choose the video(s), include --films HOS:006 (or OWB:028,OWB:029 for a shared job) on that progress
   command, and --note with the concrete outcome of each finished step. Keep the links on later progress updates.
   This connects the live job to the video's swim lane. A job parked for review is not an approved film stage.
   If it exits 10 (nothing waiting): pick the single oldest task for the Chief that isn't in the queue (on the HOS
   desk, or a Claude message on #99 asking the Chief for something with no Chief reply yet).
   If nothing is waiting anywhere, stop without posting.
4. Do that one task, following that repo's AGENTS.md exactly: claim before work (studio.py claim --git, or the HOS
   desk's own rule), commit only from a clean worktree, never spend money or credit beyond the written rules, never
   upload, schedule, retitle or change privacy on YouTube unless the job brief or a Chief/Claude message for that task
   says to, never delete a video or anything on the NAS, and never print secrets. Chief owns AGENTS.md and the Never list
   (Ben, 9-10 Oct 2026): a job added by chief, a "[Chief]" OK, or a brief saying "Ben approved (relayed by Chief)" is
   full authorisation, including Never-list exceptions it names. Never ask Ben to re-post an OK on #99. If a step needs
   Ben (real money, a sign-in, something that can't be undone), say so in your report and stop.
   A job that needs `gemini` is a facts-and-numbers check: run it through Gemini with the `agy` CLI (AGENTS.md "Who does
   what"), claim it as {agent}/gemini, and commit Gemini's findings as the job says. You check Gemini's output is complete;
   you don't rewrite its findings or any spoken line.
5. Report: OWB with  python3 scripts/owb_thread.py post "..."  (start with "{name} covering"); HOS with
   hos_desk.py post --from {agent} --to claude ...  Say what you did, what's next, and what blocks you.
You are a stand-in for Grok Bot (the Chief): never make a protected call yourself. No final OK or PASS, no merge, no
   change to AGENTS.md or the Never list, no spend past the written rules, nothing irreversible. Park it for Chief with
   jobs.py block <id> --agent {agent} --reason "parked for Chief: <what needs deciding>" --git  and say so in your report.
   Each job's `kind` says which model does it best (AGENTS.md "Who does what"); do your part and leave the rest as a job.
   A job rerouted to you while Claude Code is out of usage (model cursor-claude-opus-5-5: you are running on Claude) is
   yours to do in full, as Claude would; Claude's own protected calls (final OK, PASS, merge) still park for Chief.
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


def run_cli(agent: str, prompt: str, cap_s: int, model: str = "") -> tuple:
    """(exit code, tail of output). Exit 124 = killed at the cap. The whole process group is killed, so a CLI's
    child processes don't outlive the cap."""
    b, args = cli_spec(agent, model)
    # The exact command, minus the prompt, so a usage error (exit 2) can be matched to its flags. Flags hold no secrets.
    log(f"cmd: {b} {' '.join(shlex.quote(a) for a in args)} <prompt>" + (" (flags from the env)" if os.environ.get(
        {"cursor": "CURSOR_AGENT_FLAGS"}.get(agent, "")) else ""))
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


def credit_phrase(code: int, tail: str) -> str:
    """The out-of-credit / signed-out phrase a CLI ended its run with, or "". Only the last CHIEF_CREDIT_TAIL (800)
    characters count: that's where a CLI prints its own error. A run that did real work and quoted a YouTube 429, a
    Buffer "unauthorized" or an ai_spend "billing" line further up is not the agent being out (Ben, 15 Oct 2026: Cursor
    and Codex were marked out overnight while both had credit, and only Gemini ran)."""
    if code == 124:
        return ""  # it was working when the cap hit
    end = tail.strip()[-int(os.environ.get("CHIEF_CREDIT_TAIL", "800")):]
    m = CREDIT_RE.search(end)
    if not m or (code == 0 and len(tail.strip()) >= 600):
        return ""
    line = next((l for l in end.splitlines() if m.group(0) in l), m.group(0))
    return line.strip()[:160]


def out_of_credit(code: int, tail: str) -> bool:
    return bool(credit_phrase(code, tail))


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
        ok = notify(f"Chief relay: **Grok Bot is Chief again** ({states}). Cursor and Codex keep running the job queue as workers; Chief owns reviews/decisions.")
    elif new not in chain():
        o = override(at) or {}
        ok = notify(f"Chief relay: **{NAMES.get(new, new)} is acting Chief** until {o.get('until', '?')} "
                    f"({o.get('reason') or 'Ben named it'}). Cursor, Codex and Gemini run the job queue as workers on "
                    f"whatever model has credit; reviews, PASS, merges and final OKs go to {NAMES.get(new, new)} on "
                    f"this thread. Grok Bot takes back over by itself once it posts again.")
    else:
        later = [NAMES.get(a, a) for a in chain()[chain().index(new) + 1:]]
        workers = (f"Cursor, Codex and Gemini run the job queue as workers; reviews, PASS, merges and final OKs go to "
                   f"{NAMES.get(new, new)} on this thread. ") if cloud_chief(new) else ""
        ok = notify(f"Chief relay: **{NAMES.get(new, new)} is acting Chief** ({states}). {workers}"
                    f"{'Next in line: ' + ', '.join(later) + '. ' if later else ''}"
                    f"Whoever is higher in line takes back over by itself once it is back.")
    if ok:
        write_json(d("current.json"), {"agent": new, "since": iso(at)})


def heartbeat_doc(at: dt.datetime, state: str, agent: str = "", note: str = "") -> dict:
    """What the Kanban shows about the Mini: when the relay last ran and what it found (idle, running, busy, paused),
    and who the acting Chief is (Claude's hourly run reads it to know whether the Chief work is its own)."""
    chief = (read_json(d("current.json")) or {}).get("agent") or ""
    return {"at": iso(at), "state": state, "agent": agent, "note": note[:200], "host": "mac-mini", "chief": chief}


def parked_reviews(data: dict) -> list:
    return [j for j in data.get("jobs", []) if j.get("status") == "blocked"
            and "parked for chief" in (j.get("result") or "").lower()]


def alert_no_chief(who, rows, at: dt.datetime) -> None:
    """Ben, 21 Oct 2026: when every Chief is out, the queue keeps running but reviews wait. After CHIEF_ALERT_H (3) hours
    with no Chief and reviews parked, tell Ben once per spell (daytime only, CHIEF_ALERT_HOURS 7-22), naming who is out
    and why. Clears when a Chief is back."""
    p = d("no_chief.json")
    if who is not None:
        if p.exists():
            p.unlink(missing_ok=True)
        return
    spell = read_json(p) or {}
    if not spell.get("since"):
        write_json(p, {"since": iso(at)})
        return
    if spell.get("alerted") or at - parse(spell["since"]) < dt.timedelta(hours=float(os.environ.get("CHIEF_ALERT_H", "3"))):
        return
    lo, hi = (int(x) for x in os.environ.get("CHIEF_ALERT_HOURS", "7-22").split("-"))
    if not lo <= dt.datetime.now().hour < hi:
        return
    waiting = parked_reviews(read_json(OWB / "jobs" / "queue.json") or {})
    if not waiting:
        return
    states = "; ".join(f"{NAMES.get(a, a)}: {why}" for a, up, why in rows)
    if notify(f"Chief relay: @TheLaughingGod1986 no Chief for {int((at - parse(spell['since'])).total_seconds() // 3600)} h "
              f"and {len(waiting)} review(s) waiting ({', '.join(j['id'] for j in waiting[:8])}). {states}. Workers keep "
              f"running the queue; nothing is lost. A top-up is your call."):
        write_json(p, dict(spell, alerted=iso(at)))


def push_heartbeat(at: dt.datetime, state: str, agent: str = "", note: str = "") -> None:
    """One parentless commit holding heartbeat.json, force-pushed to refs/heads/mini-heartbeat. Never raises."""
    if os.environ.get("CHIEF_HEARTBEAT", "1") == "0" or not (OWB / ".git").exists():
        return
    # The relay ticks every minute (Ben, 12 Oct: next job within a minute): don't re-push the same idle/busy state
    # more than once per CHIEF_HB_REPEAT_MIN (10) minutes.
    if state in ("idle", "busy"):
        mark = d("heartbeat.last")
        try:
            prev_state, prev_at = mark.read_text().split()
            if prev_state == state and (at - parse(prev_at)) < dt.timedelta(
                    minutes=int(os.environ.get("CHIEF_HB_REPEAT_MIN", "10"))):
                return
        except (OSError, ValueError):
            pass
        try:
            mark.parent.mkdir(parents=True, exist_ok=True)
            mark.write_text(f"{state} {iso(at)}\n")
        except OSError:
            pass
    else:
        try:
            d("heartbeat.last").unlink()
        except OSError:
            pass
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
    """Is a Mini job waiting for this agent (jobs.py next --peek)? The relay runs every minute and chains jobs back to back (Ben,
    12 Oct: the Mini never idles), but only wakes a CLI when there's work, plus a sweep every 2 h for
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


def next_job(agent: str):
    """The queue job `agent` would get next (the one it holds, else the next claimable Mini job), or None."""
    try:
        import jobs  # noqa: E402  (jobs imports this module; by now it's loaded)
        data = jobs.load(OWB / "jobs" / "queue.json")
        at = jobs.now()
        held = next((j for j in data["jobs"] if j.get("by") == agent and j.get("status") == "claimed"), None)
        if held:
            return held
        return next((j for j in sorted(data["jobs"], key=lambda j: jobs.order(j, data.get("focus") or ()))
                     if jobs.claimable(data, j, jobs.MINI_NEEDS, at, agent)), None)
    except Exception as e:  # an unreadable queue never stops a run: the worker just gets its default model
        log(f"routing: queue not readable ({e.__class__.__name__}); default worker and model")
        return None


# ---- Claude out of usage: its jobs go to Cursor on the Claude model (Ben, 11 Oct 2026 23:40) ----

def claude_ledger_note(at: dt.datetime):
    """The newest Claude ledger note (ai_spend.py record --pool claude) from the last CHIEF_CLAUDE_OUT_H hours that says
    it hit a limit, or None."""
    hours = float(os.environ.get("CHIEF_CLAUDE_OUT_H", "5"))
    ledger = OWB / "05_Analytics" / "ai_spend" / "ledger.jsonl"
    try:
        rows = [json.loads(l) for l in ledger.read_text().splitlines() if l.strip()]
    except (OSError, ValueError):
        return None
    hits = [r for r in rows if r.get("pool") == "claude" and CLAUDE_LIMIT_RE.search(r.get("note") or "")
            and r.get("at") and at - parse(r["at"]) <= dt.timedelta(hours=hours) and parse(r["at"]) <= at]
    return max(hits, key=lambda r: r["at"]) if hits else None


def claude_blocked_on_limit(job: dict) -> bool:
    """Claude parked this job because it ran out of usage: blocked, the last block was by Claude, and the reason reads
    like a usage/limit error."""
    if job.get("status") != "blocked":
        return False
    blocks = [h for h in job.get("history", []) if str(h.get("what", "")).startswith("blocked")]
    by = blocks[-1].get("by") if blocks else ""
    return by == "claude" and bool(CLAUDE_LIMIT_RE.search(job.get("result") or (blocks[-1].get("what") if blocks else "")))


CLAUDE_BEAT_BRANCH = "claude-heartbeat"


def raw_claude_beat():
    """heartbeat.json straight from GitHub's raw file host (the repo is public), or None."""
    url = os.environ.get("CHIEF_CLAUDE_BEAT_URL", "https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/"
                         f"{CLAUDE_BEAT_BRANCH}/heartbeat.json")
    if not url:
        return None
    try:
        import urllib.request
        with urllib.request.urlopen(f"{url}?t={int(time.time())}", timeout=20) as r:
            return json.loads(r.read().decode())
    except Exception as e:   # no network, 404, bad JSON: the git read decides
        log(f"claude beat: raw read failed: {e.__class__.__name__}")
        return None


def fetch_claude_beat(at: dt.datetime):
    """Claude's heartbeat (Ben, 14 Oct 2026: "if ever an agent like yourself is down, out of usage for a few hours ...
    switch to the next model down, and when it's back, switch back automatically"). Every Claude run (the hourly studio
    run, any working session) pushes heartbeat.json to the claude-heartbeat branch with scripts/claude_beat.py. A Claude
    that is out of usage can't say so, so its silence is the signal. Fetched at most every CHIEF_CLAUDE_BEAT_FETCH_MIN
    (5) minutes; the last good read is cached in state."""
    st = read_json(d("claude_beat.json")) or {}
    every = int(os.environ.get("CHIEF_CLAUDE_BEAT_FETCH_MIN", "5"))
    if st.get("fetched") and at - parse(st["fetched"]) < dt.timedelta(minutes=every):
        return st.get("beat")
    beat = st.get("beat")
    try:
        subprocess.run(["git", "-C", str(OWB), "fetch", "-q", "origin",
                        f"+refs/heads/{CLAUDE_BEAT_BRANCH}:refs/remotes/origin/{CLAUDE_BEAT_BRANCH}"],
                       capture_output=True, timeout=60)
        r = subprocess.run(["git", "-C", str(OWB), "show", f"origin/{CLAUDE_BEAT_BRANCH}:heartbeat.json"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            beat = json.loads(r.stdout)
        else:
            log(f"claude beat: git read failed: {(r.stderr or '').strip()[-200:]}")
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        log(f"claude beat: git fetch failed: {e.__class__.__name__}")
    # A second road to the same file (15 Oct 2026 03:40Z: the Mini still read the 01:51 beat after a 03:31 one was
    # pushed). The newest of the two wins.
    raw = raw_claude_beat()
    if raw and raw.get("at") and (not beat or str(raw["at"]) > str(beat.get("at", ""))):
        beat = raw
    write_json(d("claude_beat.json"), {"fetched": iso(at), "beat": beat})
    return beat


def claude_beat_state(at: dt.datetime):
    """(out, why) from Claude's heartbeat alone, or None when there is no heartbeat yet (then the other signs decide).
    Out when the last beat is older than CHIEF_CLAUDE_STALE_MIN (90: one missed hourly run and a half; it was 150 until
    Ben, 15 Oct 2026: "when your usage ran out, work stopped again") or Claude said it's out.
    A fresh beat after a down mark clears the mark: Claude is back, and its work comes back to it."""
    beat = (read_json(d("claude_beat.json")) or {}).get("beat")
    if not beat or not beat.get("at"):
        return None
    try:
        bat = parse(beat["at"])
    except (ValueError, TypeError):
        return None
    if beat.get("out"):
        until = parse(beat["until"]) if beat.get("until") else bat + dt.timedelta(hours=5)
        if at < until:
            return True, f"Claude said it's out of usage until {iso(until)}" + (f": {beat['reason']}" if beat.get("reason") else "")
        bat = until   # past its reset: the stale clock starts there, so a Claude that doesn't come back still counts out
    mark = read_json(d("down", "claude.json"))
    if mark and not beat.get("out") and parse(mark["since"]) < bat:
        mark_up("claude")
        log(f"claude: heartbeat {beat['at']} is newer than its down mark: Claude is back")
    age = int((at - bat).total_seconds() // 60)
    if age > int(os.environ.get("CHIEF_CLAUDE_STALE_MIN", "90")):
        return True, f"no Claude run for {age} min (heartbeat {beat['at']})"
    return None


def claude_out(at: dt.datetime, data=None) -> tuple:
    """(out, why): is Claude (Claude Code / its cloud sessions) out of usage right now?"""
    hb = claude_beat_state(at)
    if hb:
        return hb
    mark = read_json(d("down", "claude.json"))
    if mark:
        until = parse(mark["until"]) if mark.get("until") else None
        if until and at >= until:
            mark_up("claude")
        else:
            return True, f"marked down: {mark.get('reason') or 'out of usage'}"
    note = claude_ledger_note(at)
    if note:
        return True, f"ledger note {note['at']}: {note.get('note')}"
    for j in (data or {}).get("jobs", []):
        if claude_blocked_on_limit(j):
            return True, f"{j['id']} blocked by Claude: {j.get('result') or 'usage limit'}"
    return False, "no usage-limit sign"


def claude_jobs_to_reroute(data: dict, at: dt.datetime, out: bool) -> list:
    """Claude-owned jobs that should go to a stand-in now: any Claude job Claude blocked on a usage/limit error, and,
    while Claude is out, its waiting ones too (open, or claimed by Claude). Never a Chief call or a Ben job, never one
    addressed to another agent, never twice (a job already rerouted walks on only via stranded_jobs / walk_on)."""
    picked = []
    for j in data.get("jobs", []):
        if not routing.claude_owned(j) or j.get("kind") == "chief" or j.get("needs") == "ben":
            continue
        if j.get("rerouted_from") or (j.get("for") and j["for"] != "claude"):
            continue
        if claude_blocked_on_limit(j) or (out and (j.get("status") == "open" or (
                j.get("status") == "claimed" and j.get("by") == "claude"))):
            picked.append(j)
    return picked


def workers_up(at: dt.datetime) -> set:
    """The Mini workers (cursor, codex, gemini) that are up: CLI installed and not marked down."""
    return {a for a in routing.MINI_WORKERS if state_of(a, at)[0]}


def stranded_jobs(data: dict, up: set) -> list:
    """Jobs the relay already handed to a worker (rerouted_from) that haven't started, whose worker is now down (out of
    usage): they walk on down their chain. Jobs Claude or Chief addressed by hand (no rerouted_from) wait for that
    agent, e.g. a second opinion from Codex."""
    return [j for j in data.get("jobs", []) if j.get("rerouted_from") and j.get("status") == "open"
            and j.get("for") in routing.MINI_WORKERS
            and (j["for"] not in up or (j.get("model") and not routing.lane_ok(j["for"], j["model"])))]


def stalled_claims(data: dict, at: dt.datetime) -> list:
    """Jobs a Mini worker claimed and then went quiet on (15 Oct 2026: Gemini held J0258 for 3 h past its ETA, so the
    board showed it running and nobody took it over). A claim over CHIEF_STALL_MIN (45) min past its ETA is dead: a
    worker run is capped at 25 min. Chief-kind jobs and jobs held by Claude or Chief are left alone."""
    lim = dt.timedelta(minutes=float(os.environ.get("CHIEF_STALL_MIN", "45")))
    out = []
    for j in data.get("jobs", []):
        if j.get("status") != "claimed" or j.get("by") not in routing.MINI_WORKERS or j.get("kind") == "chief":
            continue
        try:
            eta = dt.datetime.strptime(j.get("eta", ""), "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue
        if at - eta > lim:
            out.append(j)
    return out


def reroute(job: dict, to: str, model: str, note: str) -> bool:
    """`jobs.py reroute <id> --to <to> --model <model> --git` in the OWB checkout. True when it went through."""
    argv = [sys.executable, str(OWB / "scripts" / "jobs.py"), "reroute", job["id"], "--agent", "relay", "--to", to,
            "--note", note, "--git"] + (["--model", model] if model and model in routing.MODELS else [])
    try:
        r = subprocess.run(argv, cwd=str(OWB), capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"reroute {job['id']} failed: {e}")
        return False
    if r.returncode != 0:
        log(f"reroute {job['id']} failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
        return False
    return True


def hand_back_claude(data: dict) -> list:
    """Claude is back (Ben, 14 Oct 2026: "when you're back online, it switches back to you"): every Claude job that was
    walked down the chain while Claude was out and that no stand-in has started yet (still open) goes back to Claude."""
    back = []
    for j in data.get("jobs", []):
        rf = j.get("rerouted_from") or {}
        if j.get("status") != "open" or rf.get("needs") != "cloud" or rf.get("for", "") not in ("", "claude"):
            continue
        argv = [sys.executable, str(OWB / "scripts" / "jobs.py"), "handback", j["id"], "--agent", "relay",
                "--note", "Claude is back online", "--git"]
        try:
            r = subprocess.run(argv, cwd=str(OWB), capture_output=True, text=True, timeout=180)
        except (OSError, subprocess.SubprocessError) as e:
            log(f"handback {j['id']} failed: {e}")
            continue
        if r.returncode == 0:
            back.append(j["id"])
        else:
            log(f"handback {j['id']} failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
    if back:
        log(f"claude: handed back {', '.join(back)}")
        notify(f"Chief relay: **Claude is back**: handed back {', '.join(back)} (not started by a stand-in).")
    return back


def lane_model(lane) -> str:
    """The model to pin on a rerouted job: the lane's model when that worker runs it by name, else none."""
    return lane[1] if routing.RUNS_ON.get(lane[1]) == lane[0] else ""


def reroute_work(at: dt.datetime) -> list:
    """Walk the fallback chains (routing.CHAINS; Ben, 11 Oct 23:40 and 23:47). If Claude is out of usage, each waiting
    Claude job goes to the next worker up in its chain (Cursor on the Claude model, then Gemini, then Codex). A job
    already handed to a worker that has since run out walks on to the next one. Returns the ids moved; each is addressed
    to its new worker, so this same run wakes it. Called once per pass, before a worker is picked."""
    up = workers_up(at)
    data = read_json(OWB / "jobs" / "queue.json") or {}
    out, why = claude_out(at, data)
    if any(claude_blocked_on_limit(j) for j in data.get("jobs", [])) and not read_json(d("down", "claude.json")):
        retry_h = float(os.environ.get("CHIEF_RETRY_H", "3"))
        mark_down("claude", "a Claude job was blocked on a usage limit", at + dt.timedelta(hours=retry_h), at)
    if not out:
        hand_back_claude(data)
    moves = [(j, routing.next_lane(j, "claude", up), f"Claude out of usage ({why})")
             for j in claude_jobs_to_reroute(data, at, out)]
    moves += [(j, routing.next_lane(j, j["for"], up, j.get("model") or ""), f"{NAMES.get(j['for'], j['for'])} is down too")
              for j in stranded_jobs(data, up)]
    moves += [(j, routing.next_lane(j, j["by"], up, j.get("model") or ""), f"{NAMES.get(j['by'], j['by'])} stopped answering on it (claim past its ETA)")
              for j in stalled_claims(data, at)]
    moved = []
    for j, lane, reason in moves:
        if not lane:
            log(f"chain: {j['id']} waits: no worker left in its chain is up")
            continue
        to, model = lane
        if reroute(j, to, lane_model(lane), f"{reason}; next in its chain: {to} on {routing.cli_model(model) or 'its default'}"):
            log(f"chain: {j['id']} rerouted to {to} on {model} ({reason})")
            moved.append(f"{j['id']} -> {NAMES.get(to, to)}" + (f" on {routing.cli_model(model)}" if routing.cli_model(model) else ""))
    if moved:
        notify(f"Chief relay: walked the fallback chain: {'; '.join(moved)}. "
               + (f"Claude is out of usage ({why}); it gets the next one after its reset." if out else ""))
    return moved


def route_worker(who: str, up: set) -> tuple:
    """(worker, model) for the next job (AGENTS.md "Who does what", Ben 11 Oct 2026): the first worker in the job's
    chain that is up wakes for it (a chart job wakes Codex on gpt-6-astra; with Codex out, Cursor; then Gemini). The
    next job of that kind goes back to the primary once it's up (failover, then hand back)."""
    job = next_job(who)
    if job and not job.get("for"):
        pref = routing.preferred_worker(job, up)
        if pref and pref != who:
            log(f"routing: {job['id']} ({job.get('kind') or job.get('model')}) goes to {pref}, first up in its chain")
            who = pref
            job = next_job(who) or job
    return who, (routing.model_for(job, who) if job else ""), job


def log_run(at: dt.datetime, job, who: str, model: str, code: int, usage: bool) -> None:
    """Which worker actually ran which job, on which model (Ben, 11 Oct 23:47): one line in the log and in
    ~/_desk/state/chief/runs.jsonl (the board and Chief read it)."""
    jid = (job or {}).get("id", "")
    ch = routing.job_chain(job) if job else []
    lane = next((i for i, (a, m) in enumerate(ch, 1) if a == who and (not model or m == model)), 0)
    row = {"at": iso(at), "job": jid, "kind": (job or {}).get("kind", ""), "worker": who, "model": model,
           "cli_model": routing.cli_model(model) if model else "", "lane": lane, "of": len(ch), "exit": code,
           "out_of_usage": usage}
    log(f"ran: {jid or '(sweep)'} by {who}" + (f" on {row['cli_model'] or model}" if model else "")
        + (f" (lane {lane} of {len(ch)})" if lane else "") + f", exit {code}" + (", out of usage" if usage else ""))
    p = d("runs.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row) + "\n")


def keep_busy() -> list:
    """Ben, 12 Oct 2026: the Mini never idles. Top the queue up from the standing backlog (scripts/refill.py) so at
    least 3 Mini jobs are ready. False/empty if nothing was added or the refill couldn't run."""
    if os.environ.get("CHIEF_REFILL", "1") == "0" or not (OWB / "scripts" / "refill.py").exists():
        return []
    try:
        r = subprocess.run([sys.executable, str(OWB / "scripts" / "refill.py"), "refill", "--git"], cwd=str(OWB),
                           capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"refill failed: {e}")
        return []
    added = [x for x in r.stdout.split() if x.startswith("J")]
    if r.returncode != 0:
        log(f"refill failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
    return added


def escalate_stale() -> None:
    """A review parked for Chief past CHIEF_STALE_H hours (default 2) is posted once on #99 for the Chief. Parking
    holds only that job; every other job keeps running."""
    try:
        r = subprocess.run([sys.executable, str(OWB / "scripts" / "refill.py"), "escalate", "--git",
                            "--hours", os.environ.get("CHIEF_STALE_H", "2")], cwd=str(OWB),
                           capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"escalate failed: {e}")
        return
    lines = [x for x in r.stdout.splitlines() if x.strip()]
    if lines:
        notify("[relay] @Chief stale reviews (parked over " + os.environ.get("CHIEF_STALE_H", "2") + " h): "
               + "; ".join(lines))


def self_heal(at: dt.datetime) -> bool:
    """Ben, 14 Oct 2026: "It just seems to have ground to a halt." On 13-14 Oct the Mini had ~110 MB free and local
    files blocked the shared checkouts' pull, so every wake stopped at `git pull` and this relay (run from that
    checkout) never got its own fixes. Each run: if the disk is under CHIEF_MIN_FREE_MB or the OWB pull fails, run
    scripts/mini_repair.py's safe steps (caches, clean temp worktrees, blocking files kept in ~/_desk/rescue, local
    edits stashed, local commits pushed to a rescue branch first), at most every CHIEF_HEAL_MIN minutes, and say what
    it did on the thread. Returns False when the disk is still too full to run anything (wakes would only fail)."""
    min_mb = int(os.environ.get("CHIEF_MIN_FREE_MB", "2048"))
    hard_mb = int(os.environ.get("CHIEF_HARD_MIN_FREE_MB", "300"))
    try:
        free = shutil.disk_usage(str(HOME)).free // (1024 * 1024)
    except OSError:
        free = min_mb
    pulled = True
    if (OWB / ".git").exists():
        try:
            pulled = subprocess.run(["git", "-C", str(OWB), "pull", "-q", "--ff-only"], capture_output=True,
                                    timeout=120).returncode == 0
        except (OSError, subprocess.SubprocessError):
            pulled = False
    if pulled and free >= min_mb:
        return True
    last = read_json(d("heal.json")) or {}
    gap = dt.timedelta(minutes=int(os.environ.get("CHIEF_HEAL_MIN", "30")))
    if last.get("at") and at - parse(last["at"]) < gap:
        return free >= hard_mb
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("mini_repair", OWB / "scripts" / "mini_repair.py")
        if spec is None or not (OWB / "scripts" / "mini_repair.py").exists():
            spec = importlib.util.spec_from_file_location("mini_repair", pathlib.Path(__file__).with_name("mini_repair.py"))
        mr = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mr)
        rep = mr.repair(apply=True, repos=[r for r in (OWB, HOS) if (r / ".git").exists()],
                        do_caches=free < min_mb, scan=free < min_mb)
    except Exception as e:  # never let the repair stop the relay
        log(f"heal failed: {e.__class__.__name__}: {e}")
        write_json(d("heal.json"), {"at": iso(at), "error": str(e)[:300]})
        return free >= hard_mb
    write_json(d("heal.json"), {"at": iso(at), "before_mb": rep["before_mb"], "after_mb": rep["after_mb"]})
    acts = [f"{pathlib.Path(c['repo']).name}: {'; '.join(c['actions'])}" for c in rep["checkouts"]
            if c["actions"] and c["actions"] != ["already at origin/main"]]
    gone = [w for w in rep["worktrees"] if ": remove (" in w]
    log(f"heal: {rep['before_mb']} MB -> {rep['after_mb']} MB free; {'; '.join(acts) or 'checkouts fine'}; "
        f"{len(gone)} temp worktree(s) removed")
    if acts or gone or rep["after_mb"] - rep["before_mb"] > 100 or rep["after_mb"] < min_mb:
        big = "; ".join(x.strip() for x in rep["biggest"][:4])
        notify(f"Chief relay: repaired the Mini (scripts/mini_repair.py): {rep['before_mb']:,} MB -> "
               f"{rep['after_mb']:,} MB free. {' '.join(acts) or 'Checkouts pull cleanly.'}"
               + (f" {len(gone)} clean temp worktree(s) removed." if gone else "")
               + (f" Still under {min_mb // 1024} GB free: move the version-before-last render scratch to the NAS "
                  f"(AGENTS.md 'Render scratch'). Biggest: {big}" if rep["after_mb"] < min_mb else ""))
    if rep["after_mb"] < hard_mb:
        push_heartbeat(at, "disk-full", note=f"{rep['after_mb']} MB free after repair; render scratch must move to the NAS")
        return False
    return True


def run_locked(at: dt.datetime) -> int:
    note_grok_posts(at)
    fetch_claude_beat(at)
    flags = load_out(at)
    if flags:
        log("out of credit: " + "; ".join(f"{k} ({v})" for k, v in sorted(flags.items())))
    if not self_heal(at):
        log("disk still too full to run a worker: waiting for the next repair")
        return 0
    if (OWB / "scripts" / "refill.py").exists():
        escalate_stale()
    cap = int(os.environ.get("CHIEF_CAP_S", "1500"))
    # A worker that says it's out of credit is retried after 1 h, not 3 (Ben, 14 Oct 2026: "no worker has credit. I
    # don't believe this"; a 429, or one model's pool read as the whole agent out for 3 h, left the Mini idle). A real
    # longer outage goes in scripts/credit_flags.json with its true reset time.
    retry_h = float(os.environ.get("CHIEF_RETRY_H", "1"))
    # Ben, 12 Oct 2026: the Mini never idles. When a job ends, the next ready job starts straight away in this same
    # run (no waiting for the next launchd tick); CHIEF_CHAIN_MAX bounds one run, and a job that comes straight back
    # open (released to retry later) ends the chain so it isn't re-run in a tight loop.
    chain_max = int(os.environ.get("CHIEF_CHAIN_MAX", "12"))
    chained, last_ran = 0, None
    while True:
        # Re-read Claude's heartbeat each pass (at most every 5 min): a chain of worker jobs can hold this run for
        # hours, and on 15 Oct 2026 it kept reading the 04:04 beat until 06:03 after fresh beats at 05:49 and 05:51.
        fetch_claude_beat(now())
        rows, who = acting(at)
        handover(who, rows, at)
        alert_no_chief(who, rows, at)
        log("chain: " + " | ".join(f"{a}={'UP' if up else 'down'} ({why})" for a, up, why in rows))
        up = workers_up(at)
        worker_only = False
        if who is None:
            if not up:
                log("nobody up: nothing to run")
                push_heartbeat(at, "no-chief", note="nobody in the chain is up")
                return 0
            # Grok, Cursor and Codex all down but Gemini up (Ben, 11 Oct 23:47): it runs queued jobs, no Chief work.
            who, worker_only = next(a for a in routing.MINI_WORKERS if a in up), True
        # Fallback chains (Ben, 11 Oct 23:40 / 23:47): Claude's jobs when it's out of usage, and jobs whose worker ran
        # out, go to the next worker up in their chain, addressed to it, so the loop below wakes it in this same run.
        rerouted = reroute_work(at)
        # A job addressed to one agent wakes that agent if it's up, ahead of the acting Chief: otherwise only the first
        # agent in the chain ever runs, and a second opinion from Codex would never happen.
        addressed = False
        for a in routing.MINI_WORKERS:
            if a in up and a != who and addressed_to(a):
                addressed = True
                log(f"{a} has a job addressed to it ({', '.join(addressed_to(a))}): waking it first")
                who = a
                break
        chief_name = NAMES.get(who, who) if cloud_chief(who) else ""
        if cloud_chief(who):
            # Grok Bot (9 Oct 2026, studio owner), or Claude under Ben's override (14 Oct): the Chief does reviews,
            # PASS, merges, decisions and the board; the Mini CLIs stay the WORKERS for queued jobs. So wake the first
            # worker that's up (Cursor, Codex, then Gemini) for one queued job (no thread/desk sweep).
            who = next((a for a in routing.MINI_WORKERS if a in up), None)
            if who is None:
                log(f"{chief_name} is Chief and no worker is up: nothing to run")
                push_heartbeat(at, "no-worker", note=f"{chief_name} is Chief; no Mini worker has credit")
                return 0
            worker_only = True
        if who == "gemini":
            worker_only = True  # Gemini is never acting Chief: it only takes queued jobs
        last_wake = last_seen(who)
        # Overnight (Ben, 7 Oct: carry on overnight) agents are woken for queued jobs only; the 2-hourly sweep for
        # thread/desk tasks runs in the day, so an empty night costs no credit.
        slo, shi = (int(x) for x in os.environ.get("CHIEF_SWEEP_HOURS", "8-22").split("-"))
        sweep = slo <= dt.datetime.now().hour < shi and (
            not last_wake or (at - last_wake) >= dt.timedelta(minutes=int(os.environ.get("CHIEF_SWEEP_MIN", "120"))))
        if worker_only:
            sweep = False
        added = keep_busy()  # every pass, not only when dry: keeps >=3 Mini jobs ready (Ben, 12 Oct 14:36)
        if added:
            log(f"refill: added {' '.join(added)} from jobs/backlog.json")
        if not queue_has_work(who) and not sweep:
            ago = f"{int((at - last_wake).total_seconds() // 60)} min ago" if last_wake else "never"
            log(f"nothing queued for {who}; last woken {ago}: not waking it")
            push_heartbeat(at, "idle", who, "nothing queued")
            return 0
        names = [r[0] for r in rows]
        above = [f"{NAMES.get(a, a)} is {why}" for a, ok, why in rows[:names.index(who)]] if who in names else []
        why = "Claude addressed a job to you by name" if addressed else ("; ".join(above) or "it is first in line")
        if addressed and rerouted:
            why = (f"the job's earlier worker is out of usage, so the relay walked its fallback chain and handed it to "
                   f"you ({', '.join(rerouted)}; Ben, 11 Oct 2026). Take it with jobs.py next; do it as the primary "
                   f"would, and stop at the same protected calls")
        elif worker_only:
            why = (f"{chief_name or 'Grok Bot'} is Chief (reviews, PASS, merges, decisions, the board) and you are its WORKER for the Mini "
                   "job queue. In step 3 skip the channel check and the HOS desk inbox: do only the job "
                   "`jobs.py next` gives you, and that includes `hos` queue jobs (repo: hos), which are normal "
                   "queue jobs, not desk tasks: do them in the HOS checkout. If it exits 10, stop without posting")
        model, job = "", None
        if not addressed and who in routing.MINI_WORKERS:
            who, model, job = route_worker(who, up)
        elif addressed:
            job = next_job(who)  # the addressed job comes first in jobs.order: run it on its own model
            model = routing.model_for(job, who) if job else ""
        if chained and (job is None or (last_ran and job.get("id") == last_ran)):
            log(f"chain: stop after {chained} job(s): " + ("next job is the one just run (released to retry later)"
                                                         if job else "no next job identified"))
            return 0
        prompt = PROMPT.format(name=NAMES.get(who, who), agent=who, why=why,
                               owb=OWB, hos=HOS)
        log(f"run: {who}{' on ' + model if model else ''}{' for ' + job['id'] if job else ''} (cap {cap}s)")
        push_heartbeat(at, "running", who, f"woke {NAMES.get(who, who)} for {job['id'] if job else 'one job'} (cap {cap // 60} min)")
        seen(who, at)
        started = now()
        code, tail = run_cli(who, prompt, cap, model)
        said = credit_phrase(code, tail)
        usage = bool(said)
        log_run(at, job, who, model, code, usage)
        if usage:
            until = now() + dt.timedelta(hours=retry_h)
            on_auto = who == "cursor" and model not in routing.SEPARATE_POOLS and bool(cursor_default_out(now()))
            if who == "cursor" and MODEL_LIMIT_RE.search(said) and model not in routing.SEPARATE_POOLS and not on_auto:
                # Only the model Cursor defaults to is out (its Opus pool), not Cursor: run it on Auto for the
                # mark's length and keep it up (Ben, 15 Oct 2026: Cursor was benched overnight with credit left).
                write_json(d("cursor_default_out.json"), {"since": iso(now()), "until": iso(until), "said": said})
                log(f"cursor: its default model is out ({said}); Cursor runs on Auto until {iso(until)}")
                at = now()
                continue   # the same job, on Auto, in this same run
            elif model in routing.SEPARATE_POOLS:
                # Only this model's pool is empty (Claude-in-Cursor): flag the model, keep the worker up for its other
                # models, and move the job on down its chain (Ben, 14 Oct 2026: run 24/7 on whoever has credit).
                mark_model_down(model, f"{NAMES.get(who, who)} on {routing.cli_model(model)} said out of credit", until, now())
                routing.OUT.add(model)
                log(f"{who} on {model} looks out of credit: that model is flagged until {iso(until)}; {who} stays up")
            else:
                mark_down(who, f"out of usage, credit or signed out (its last run ended: \"{said}\")", until, now())
                log(f"{who} looks out of usage or signed out: down until {iso(until)}; walking the job's chain")
            if job:
                walk_on(job, who, model, now())
            at = now()
            continue
        bad_model = (model or ("cursor-grok-4-7" if who == "cursor" and not cursor_default_out(now()) else ""))
        if code not in (0, 124) and bad_model and UNKNOWN_MODEL_RE.search(tail[-1500:]):
            # The worker doesn't know that model id (Ben, 15 Oct 2026: best-fit models per job). Flag the model for a
            # day, keep the worker up, and walk the job on so a wrong id never stops the queue.
            mark_model_down(bad_model, f"{NAMES.get(who, who)} didn't recognise model {routing.cli_model(bad_model)}",
                            now() + dt.timedelta(hours=24), now())
            routing.OUT.add(bad_model)
            notify(f"Chief relay: {NAMES.get(who, who)} doesn't know model `{routing.cli_model(bad_model)}`; flagged "
                   f"for 24 h and the job walks on. Fix the id in scripts/routing.py (`agent --list-models` / codex / agy).")
            if job:
                walk_on(job, who, bad_model, now())
            at = now()
            continue
        if code not in (0, 124):
            notify(f"Chief relay: {NAMES.get(who, who)}'s run failed (exit {code}). Log: ~/Library/Logs/chief-relay.log")
            # Don't wake it again every minute into the same failure (Gemini exit 2, 13-14 Oct: 88 posts in 20 h).
            # An addressed job waits the usual retry; a plain worker run waits CHIEF_FAIL_RETRY_H, so others take the queue.
            fail_h = retry_h if addressed else float(os.environ.get("CHIEF_FAIL_RETRY_H", "1"))
            mark_down(who, f"its {'run for an addressed job' if addressed else 'last run'} failed (exit {code})",
                      now() + dt.timedelta(hours=fail_h), now())
            return 0
        chained += 1
        last_ran = job.get("id") if job else None
        if chained >= chain_max or not job:
            return 0
        log(f"chain: {last_ran} ended; starting the next ready job now ({chained}/{chain_max})")
        at = at + (now() - started)  # the run's own clock moved on by the job's length


def walk_on(job: dict, who: str, model: str, at: dt.datetime) -> None:
    """`who` ran out of usage on `job`: if the job is still open or held by `who`, hand it to the next worker up in its
    chain (so it isn't left claimed by a worker that can't finish it). If nobody further down is up, it waits."""
    data = read_json(OWB / "jobs" / "queue.json") or {}
    cur = next((j for j in data.get("jobs", []) if j.get("id") == job.get("id")), None)
    if not cur or not (cur.get("status") == "open" or (cur.get("status") == "claimed" and cur.get("by") == who)):
        return
    lane = routing.next_lane(cur, who, workers_up(at), model)
    if not lane:
        log(f"chain: {cur['id']} waits: nobody after {who} in its chain is up")
        return
    if reroute(cur, lane[0], lane_model(lane), f"{NAMES.get(who, who)} out of usage; next in its chain: {lane[0]}"):
        log(f"chain: {cur['id']} rerouted from {who} to {lane[0]} on {lane[1]}")


def cmd_status(at: dt.datetime) -> int:
    flags = load_out(at)
    rows, who = acting(at)
    for a, up, why in rows:
        print(f"{'>' if a == who else ' '} {a:<7} {NAMES.get(a, a):<9} {'UP  ' if up else 'down'}  {why}")
    print(f"Chief: {NAMES.get(who, who) if who else 'nobody'}")
    g_up, g_why = state_of("gemini", at)
    print(f"  {'gemini':<7} {'Gemini':<9} {'UP  ' if g_up else 'down'}  {g_why} (worker only, never Chief)")
    out, why = claude_out(at, read_json(OWB / "jobs" / "queue.json") or {})
    print(f"Claude: {'OUT of usage (' + why + '); its jobs walk their chain: Cursor on ' + routing.CURSOR_CLAUDE_MODEL + ', Gemini, Codex' if out else 'up (' + why + ')'}")
    print(gemini_line())
    for k, v in sorted(flags.items()):
        print(f"Out of credit: {k}: {v}")
    try:
        print(f"Disk: {shutil.disk_usage(str(HOME)).free // (1024 * 1024):,} MB free")
    except OSError:
        pass
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
