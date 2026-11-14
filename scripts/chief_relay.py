#!/usr/bin/env python3
"""Chief relay: whoever is first in line and has credit acts as Chief of Staff on the Mac mini (Ben, 7 Oct 2026).

Ben: "If Grok Bot is down and out of credit, Cursor takes over. If Cursor and Grok Bot are down, Codex takes over,
and so on down a chain. The Chief of Staff is ultimately in charge." So the chain is, by default:

  chief (Grok Bot) -> claude -> codex (GPT) -> gemini (Antigravity `agy`)

The first agent in the chain that is up is the Chief. Nobody flips a switch by hand: Grok takes back over by itself
when it is active again, and a CLI that runs out of credit is skipped until its retry time, so the next one in line
takes the run.

How "up" is decided:
  chief   Grok Bot is a desktop app with no CLI; the relay can't start it, prompt it or see its credit. It counts as
          up when it has posted on the studio thread as plain "[Chief]" in the last 180 min (Cursor and Codex posts
          are tagged, and the relay's own lines are skipped), or has run `jobs.py ... --agent chief` in that time.
          Its app files are no use: they are a heartbeat written every minute while the app is open, credit or not.
          A `down` mark on Grok is cleared by either signal seen after the mark: Grok working again is proof it is back.
  codex, gemini (Cursor remains a specialist worker)
          up unless their CLI is missing or they are marked down. A run whose output says out of credit, over the
          usage limit, or signed out marks that agent down for CHIEF_RETRY_H hours (default 1), and the same run falls
          through to the next agent in line.

  python3 scripts/chief_relay.py status                         # the chain, who is Chief, and why
  python3 scripts/chief_relay.py run                            # launchd, every minute: one job by the acting Chief, when one is queued
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

`run` checks the Chief inbox every pass, alongside production in shared deadline order, round the clock. CLI Chiefs process up to
CHIEF_CHAIN_MAX duties/jobs (25-minute cap each); app/cloud Chiefs receive a durable inbox and yield if a delivered
duty makes no progress for CHIEF_DUTY_ACK_MIN (30 minutes; 150 for Claude's hourly cloud run, and only if its
inbox has not moved at all in that time) with no live claim. Per-job retries use CHIEF_REVIEW_MIN
(10 minutes), never the Chief heartbeat. A pause file or an existing run lock still prevents overlapping runs.
Every change of Chief is posted to the studio thread once.

State (on the Mini, never in git): ~/_desk/state/chief/  (heartbeat/<agent>, down/<agent>.json, current.json).
Mini heartbeat (Ben, 8 Oct): every `run` also pushes one small file, heartbeat.json {at, state, agent, note}, to the
branch `mini-heartbeat` as a single parentless commit (force-pushed, so main's history stays clean). The Kanban reads
it to tell "the Mini is busy on a long job" from "the Mini is asleep". CHIEF_HEARTBEAT=0 turns it off.
Log: stdout (launchd sends it to ~/Library/Logs/chief-relay.log).
Env (the defaults find the CLIs and the HOS checkout on Ben's Mini; set these only to override): CHIEF_CHAIN (orbit-with-ben, default "claude,chief,codex,gemini"), CHIEF_CHAIN_HOS (History of Science, default "chief,claude,codex,gemini"), CHIEF_HOURS (0-24: round the clock), CHIEF_CAP_S (1500), CHIEF_GROK_FRESH_MIN (180),
CHIEF_RETRY_H (1), CHIEF_CLAUDE_OUT_H (5), CURSOR_CLAUDE_MODEL (routing.py), CURSOR_AGENT_BIN / CURSOR_AGENT_FLAGS ("-p --force"), CODEX_BIN (Codex's flags are fixed in cli_spec; CODEX_FLAGS is ignored), AGY_BIN,
OWB_REPO, HOS_REPO, DESK_STATE, CHIEF_NOTIFY (command that posts a line; default owb_thread.py post).
"""
from __future__ import annotations

import argparse
import hashlib
import datetime as dt
import fcntl
import json
import os
import pathlib
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time

HOME = pathlib.Path.home()
STATE = pathlib.Path(os.environ.get("DESK_STATE", HOME / "_desk" / "state"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import workflow_state as workflow
import workflow_handoffs as handoffs
import routing  # noqa: E402  (AGENTS.md "Who does what": job kind -> worker and model)
import channels  # noqa: E402  (channels/*/channel.json: checkouts, labels)

# The checkout that carries the studio's own code, queue and thread, and the checkouts of the channels kept beside it.
# Which is which comes from the channel files (11 Nov 2026, J2618): this script names no channel.
STUDIO = channels.studio_checkout(HOME)


def code_version():
    root = pathlib.Path(__file__).resolve().parent
    return hashlib.sha256(b"\0".join((root/name).read_bytes() for name in ("chief_relay.py","workflow_state.py","workflow_handoffs.py","studio.py","jobs.py","routing.py",
        ))).hexdigest()[:16]

LOADED_VERSION = code_version()


def current_execution(at):
    value = read_json(d("execution.json")) or {}
    expires = workflow.timestamp(value.get("expiresAt"))
    if not expires or expires <= at:
        return None
    try:
        pid = int(value.get("pid") or 0)
        if pid <= 0:
            return None
        os.kill(pid,0)
    except (ValueError, TypeError, OSError):
        return None
    return value


def worker_capabilities():
    return read_json(d("capabilities.json")) or {}


def record_capabilities(agent, available, evidence, minutes, at, source="self"):
    """Record an observed tool capability, never infer it from agent availability.

    A worker's own session report can't test media and says "none", so it never narrows a fresh relay probe
    (scripts/capability_probe.py); it only adds what it shows itself (Claude, 5 Nov 2026)."""
    if agent not in chain() + list(routing.MINI_WORKERS) or not str(evidence).strip() or not 1 <= minutes <= 60:
        raise ValueError("Capability reports need a known agent, actual probe evidence and a 1–60 minute lifetime")
    names = [x.strip() for x in available.split(",") if x.strip()]
    if any(not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", x) for x in names):
        raise ValueError("Use capability identifiers such as audio_input, not prose")
    reports = worker_capabilities()
    old = reports.get(agent) or {}
    shown = dict(old.get("last_shown") or {})
    row = {"at":iso(at), "expiresAt":iso(at+dt.timedelta(minutes=minutes)),
           "available":sorted(set(names)), "evidence":str(evidence).strip(), "source":source}
    if source != "probe" and old.get("source") == "probe" and not workflow.capability_problem(
            {"required_capabilities": old.get("available") or ["_"]}, agent, at, reports):
        row = dict(old, available=sorted(set(old.get("available") or []) | set(names)),
                   evidence=f"{old.get('evidence')} | session: {str(evidence).strip()}"[:2000])
    for cap in set(names):
        shown[cap] = iso(at)
    if shown:
        row["last_shown"] = shown
    reports[agent] = row
    write_json(d("capabilities.json"), reports)


def refresh_probes(at):
    """Re-probe media input while a job needs it: when the last probe is missing or under 10 min from expiry, at most
    every 15 min per agent, so jobs needing audio go to a worker shown this hour to hear (Claude, 5 Nov 2026)."""
    if os.environ.get("CHIEF_PROBE", "1") != "1":
        return
    jobs = (read_json(STUDIO / "jobs" / "queue.json") or {}).get("jobs", [])
    if not any(j.get("required_capabilities") and j.get("status") not in ("done", "cancelled") for j in jobs):
        return
    import capability_probe
    tried = read_json(d("probe_attempts.json")) or {}
    for agent in capability_probe.RUNNERS:
        if not state_of(agent, at)[0]:
            continue
        rep = worker_capabilities().get(agent) or {}
        try:
            left = dt.datetime.fromisoformat(rep["expiresAt"].replace("Z", "+00:00")) - at
        except (KeyError, ValueError, AttributeError):
            left = dt.timedelta(0)
        last = tried.get(agent)
        if (rep.get("source") == "probe" and left > dt.timedelta(minutes=10)) or (
                last and at - dt.datetime.fromisoformat(last.replace("Z", "+00:00")) < dt.timedelta(minutes=15)):
            continue
        tried[agent] = iso(at)
        write_json(d("probe_attempts.json"), tried)
        try:
            available, evidence = capability_probe.probe(agent)
        except Exception as e:  # a probe that can't run proves nothing; leave the last report to expire
            log(f"capability probe of {agent} could not run: {e}")
            continue
        record_capabilities(agent, ",".join(available), evidence, 60, now(), source="probe")
        log(f"capability probe: {agent} has {', '.join(available) or 'no media input'} ({evidence[:300]})")


# Every other channel's checkout, by slug. A channel file can list more than one folder name for it (on Ben's Mini one
# is "History Of Science", Cursor, 7 Oct; the git-style name is the fallback): the first that exists is used.
OTHERS = {slug: channels.repo_path(slug, HOME) for slug in channels.slugs() if slug != channels.studio_slug()}


def add_dirs() -> str:
    """The folders an unattended CLI is allowed besides the studio checkout it starts in: every other channel's
    checkout, then the desk folder."""
    return " ".join(f"--add-dir {shlex.quote(str(path))}" for path in [*OTHERS.values(), STATE.parent])
# Ben, 21 Oct 2026: "build in a method where we identify dynamically if the acting chief is out and delegate a chief
# until the main one or next in command is back". Claude is a standing link (up while its hourly heartbeat is fresh),
# not only a dated override. Ben, 26 Oct 2026: Grok -> Claude -> Codex -> Gemini; Ben, 9 Nov 2026 (Claude now the
# bigger plan): Claude -> Grok -> Codex -> Gemini for orbit-with-ben. Cursor stays a worker.
# Ben, 11 Nov 2026, desk #180: the non-home channel keeps the 26 Oct chain (Grok first). The 9 Nov chain
# stays the home channel's. A status that names Claude on that channel's job means Grok is down.
DEFAULT_CHAIN = "claude,chief,codex,gemini"
SECOND_CHAIN = "chief,claude,codex,gemini"
NAMES = {"chief": "Grok Bot", "cursor": "Cursor", "codex": "Codex", "gemini": "Gemini", "claude": "Claude",
         "claudecode": "Claude Code"}

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
# The provider is briefly out of capacity for one model (Codex 5 Nov 2026 09:10Z: "ERROR: Selected model is at capacity.
# Please try a different model." benched Codex for an hour). Not an outage of the worker: flag that model for a few
# minutes, keep the worker up, and walk the job on.
CAPACITY_RE = re.compile(r"(?:model|server|service)[^\n]{0,40}\b(?:at|over) capacity|overloaded_error|"
                         r"(?:server|model) (?:is )?overloaded", re.I)


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> dt.datetime:
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return t if t.tzinfo else t.astimezone()  # a bare local time from Ben's --until


def _other_slugs() -> list:
    """Channels other than the one this repo belongs to. Today that is one channel."""
    home = channels.default()
    return [s for s in channels.slugs() if s != home]


def chain(repo: str | None = None) -> list:
    """The home channel uses CHIEF_CHAIN. Any other channel uses CHIEF_CHAIN_ plus its label
    (so the non-home channel's override is CHIEF_CHAIN_ and its label), else SECOND_CHAIN."""
    if repo and repo != channels.default():
        raw = os.environ.get("CHIEF_CHAIN_" + channels.label(repo), SECOND_CHAIN)
    else:
        raw = os.environ.get("CHIEF_CHAIN", DEFAULT_CHAIN)
    return [a.strip() for a in raw.split(",") if a.strip()]


def job_chain(job: dict | None) -> str | None:
    """The chain a job elects on. None keeps the home channel's chain."""
    if not job:
        return None
    try:
        slug = channels.of_job(job)
    except (OSError, ValueError, KeyError):
        slug = str(job.get("repo") or "")
    if slug and slug != channels.default():
        return slug
    return None


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


def mark_down(agent: str, reason: str, until, at: dt.datetime, kind: str = "") -> None:
    mark = {"since": iso(at), "until": iso(until) if until else None, "reason": reason}
    if kind:
        mark["kind"] = kind
    write_json(d("down", agent + ".json"), mark)


STALL_BASE_MIN, STALL_MAX_MIN = 30, 720


def stall_window(agent: str, at: dt.datetime) -> dt.timedelta:
    """How long a Chief that took its inbox but did not progress it stays down. Ben, 28 Oct 2026: "We know grok is
    down so why is the acting chief not taking over" - a flat 30 min let Grok be re-elected all evening without clearing
    a single decision. Each repeat within 24 h doubles it: 30 min, 1 h, 2 h ... up to 12 h."""
    log_path = d("stalls", agent + ".json")
    recent = [t for t in (read_json(log_path) or []) if at - parse(t) < dt.timedelta(hours=24)]
    minutes = min(STALL_BASE_MIN * 2 ** len(recent), STALL_MAX_MIN)
    write_json(log_path, recent + [iso(at)])
    return dt.timedelta(minutes=minutes)


def hard_flag(agent: str, at: dt.datetime) -> bool:
    """A credit_flags.json entry with "hard": true is Ben's own call that an agent is out (28 Oct 2026). Unlike a
    credit flag, a thread post does not clear it; only its out_until does."""
    flag = ((read_json(STUDIO / "scripts" / "credit_flags.json") or {}).get("flags") or {}).get(agent) or {}
    try:
        return bool(flag.get("hard")) and parse(flag["out_until"]) > at
    except (KeyError, ValueError, TypeError):
        return False


def mark_model_down(model: str, reason: str, until: dt.datetime, at: dt.datetime) -> None:
    """One model is out of credit while its worker's other models still run (routing.SEPARATE_POOLS: Claude-in-Cursor
    bills Cursor's "Other Models" pool, Cursor Auto its own; Ben, 14 Oct 2026)."""
    write_json(d("down_models", model + ".json"), {"since": iso(at), "until": iso(until), "reason": reason})


def load_out(at: dt.datetime) -> dict:
    """Out-of-credit flags in force this run: scripts/credit_flags.json (committed by Claude or Chief, with the known
    reset time) plus the relay's own model marks. Sets routing.OUT so every chain skips those lanes. {id: reason}."""
    flags = routing.read_flags(at, str(STUDIO / "scripts" / "credit_flags.json"))
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
    return routing.find_cli(env, name, HOME)


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
        flags = f"exec --approve-for-me -c sandbox_workspace_write.network_access=true {add_dirs()}"
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
        flags = os.environ.get("AGY_FLAGS", f"--dangerously-skip-permissions {add_dirs()}")
        cm = routing.cli_model(model) if routing.RUNS_ON.get(model) == "gemini" else ""
        if cm:
            flags = f"{flags} --model {shlex.quote(cm)}"
        flags = shlex.join([a for a in shlex.split(flags) if a != "-p"] + ["-p"])
    elif agent == "claudecode":
        # Claude Code as an ordinary Mini worker (Ben, 9 Nov 2026: Codex and Cursor out of credit; his Claude plan is
        # Max 20x). Unattended like agy (--dangerously-skip-permissions); -p last, straight before the prompt, because
        # --add-dir takes a list and would read a prompt after it as one more folder (macbook_worker, 5 Nov 2026).
        b = find_bin("CLAUDE_BIN", "claude")
        flags = os.environ.get("CLAUDE_CODE_FLAGS", f"--dangerously-skip-permissions {add_dirs()}")
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
# made "Grok Bot is Chief again" while Grok was out of credit. The stall watchdog's "[Chief] STALLED: 028 edit by
# gemini: ETA ... passed" did the same on 22 Oct 2026 23:46Z (relay: "Grok Bot is Chief again" at 23:53Z).
NOT_GROK = re.compile(r"\[(?:Cursor|Codex|Gemini|Claude|relay)\]|\b(?:Cursor|Codex|Gemini|Claude) covering|Chief relay:"
                      r"|watchdog|studio\.py stale|STALLED:|Generated by \[Claude Code\]", re.I)


def fetch_comments(since: dt.datetime) -> list:
    """Studio-thread comments updated since `since`, via the thread tool's own auth (GH_TOKEN or `gh auth token`)."""
    sys.path.insert(0, str(STUDIO / "scripts"))
    import studio_thread as thread  # noqa: E402
    # Only the repo's own accounts count (thread.trusted): the repo is public, so anyone can comment on the thread.
    return [c for c in thread.api("GET", f"/issues/{thread.PR}/comments?since={iso(since)}&per_page=100")
            if thread.trusted(c)]


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
    if agent == "claude":
        claude_beat_state(at)  # a newer heartbeat clears its old down mark before election
    mark = read_json(d("down", agent + ".json"))
    if mark:
        until = parse(mark["until"]) if mark.get("until") else None
        since = parse(mark["since"])
        beat = last_seen(agent)
        if until and at >= until:
            mark_up(agent)
        elif agent == "chief" and ((beat and beat > since) or (mark.get("kind") != "stalled"
                                                              and grok_post_age(at, after=since) is not None)):
            # Grok has worked since it was marked down: it's back. A stall (inbox taken, not progressed) clears only
            # when Grok runs jobs.py again; a post on the thread is talk, not progress.
            mark_up(agent)
        else:
            return False, f"marked down: {mark.get('reason') or 'no reason given'}" + (f" (retry after {mark['until']})" if until else "")
    flag = routing.read_flags(at, str(STUDIO / "scripts" / "credit_flags.json")).get(agent)
    if flag and (hard_flag(agent, at) or not (agent == "chief" and grok_post_age(at) is not None
                                             and grok_post_age(at) <= int(os.environ.get("CHIEF_GROK_FRESH_MIN", "180")))):
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
        out, why = claude_out(at, read_json(STUDIO / "jobs" / "queue.json") or {})
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
    o = read_json(STUDIO / "scripts" / "chief_override.json") or {}
    try:
        until = parse(o["until"])
    except (KeyError, ValueError, TypeError):
        return None
    return o if o.get("agent") and at < until else None


def acting(at: dt.datetime, repo: str | None = None):
    """The chain with each agent's state, and the first one that's up (or None). Ben's override (a Chief such as
    Claude, who isn't woken on the Mini) comes after Grok and ahead of the Mini CLIs. `repo="hos"` walks the
    History of Science chain (Grok first)."""
    order = chain(repo)
    rows = [(a,) + state_of(a, at) for a in order]
    first = next((a for a, up, _ in rows if up), None)
    o = override(at)
    if o and o.get("agent") in order:
        return rows, first   # already a link in the chain: its own up/down state decides
    if o and o.get("agent") == "claude" and first != "chief":
        out, why = claude_out(at, read_json(STUDIO / "jobs" / "queue.json") or {})
        if out:
            # Ben, 14 Oct 2026: while Claude is out of usage the next one down runs as Chief, and Claude takes it back
            # by itself when its heartbeat returns.
            return rows + [("claude", False, f"named Chief by Ben, but out of usage ({why})")], first
    if o and first != "chief":
        return rows + [(o["agent"], True, f"named Chief by Ben until {o['until']}")], o["agent"]
    return rows, first


def is_elected_chief(agent: str, at: dt.datetime, repo: str | None = None) -> bool:
    """Authority belongs to the elected role, never to a worker merely running a Chief's model.
    `repo="hos"` asks who is Chief for History of Science, which can differ from orbit-with-ben."""
    return bool(agent and acting(at, repo)[1] == agent)


def elected_for(agent: str, at: dt.datetime, job: dict | None) -> bool:
    """True when `agent` is the Chief for this job's channel.
    A home-channel job calls the two-argument check, so existing stand-ins keep working."""
    slug = job_chain(job)
    if not slug:
        return is_elected_chief(agent, at)
    return is_elected_chief(agent, at, slug)


def chief_fingerprint(job: dict) -> str:
    # Exclude relay escalation/heartbeats: those are not new work or a decision.
    fields = {k: job.get(k) for k in ("status", "result", "body", "progress", "after", "awaits_ben")}
    return hashlib.sha256(json.dumps(fields, sort_keys=True).encode()).hexdigest()


def chief_order(job: dict) -> tuple:
    def stamp(value, default=float("inf")):
        try:
            return parse(value).timestamp() if value else default
        except (TypeError, ValueError):
            return default
    approval = job.get("approved_from") or {}
    deadlines = [job.get("due"), approval.get("airs"), (job.get("awaits_was") or {}).get("due")]
    deadline = min(stamp(v) for v in deadlines)
    blocked = next((h.get("at") for h in reversed(job.get("history", []))
                    if str(h.get("what", "")).startswith("blocked")), job.get("created_at"))
    return (deadline, 0 if job.get("urgent") else 1, stamp(blocked), job.get("id", ""))


def pending_chief_reviews(at: dt.datetime) -> list:
    """All actionable role work, not just reviews. Never release a hold here."""
    data = read_json(STUDIO / "jobs" / "queue.json") or {}
    by_id = {j["id"]: j for j in data.get("jobs", [])}
    due = workflow.deadlines(data.get("jobs", []))
    capabilities = worker_capabilities()
    needs_cap = any(j.get("required_capabilities") for j in data.get("jobs", []))
    home_leader = acting(at)[1] if needs_cap else ""
    guests = _other_slugs()
    guest_leader = acting(at, guests[0])[1] if needs_cap and len(guests) == 1 else ""
    from workflow_board import load_tracker
    tracker = load_tracker()
    nearest, air = workflow.near_watch(tracker), workflow.air_dates(tracker)
    return sorted((j for j in data.get("jobs", [])
                   if not workflow.external_hold(j, at) and not workflow.dependency_problem(j, by_id)
                   and (j.get("capability_escalated") or not workflow.capability_problem(
                       j, guest_leader if job_chain(j) else home_leader, at, capabilities))
                   and (workflow.state(j, by_id, at) == "review" or (workflow.role_job(j) and workflow.state(j, by_id, at) == "queued"))),
                  key=lambda j: workflow.order(j, due, data.get("focus") or (), at, nearest, air))


def due_chief_reviews(items: list, agent: str, at: dt.datetime) -> list:
    attempts = (read_json(d("duties.json")) or {}).get("attempts", {})
    out = []
    for job in items:
        previous = attempts.get(job["id"], {})
        try:
            recent = at - parse(previous["at"]) < dt.timedelta(minutes=int(os.environ.get("CHIEF_REVIEW_MIN", "10")))
        except (KeyError, TypeError, ValueError):
            recent = False
        if recent and previous.get("agent") == agent and previous.get("fingerprint") == chief_fingerprint(job):
            continue
        out.append(job)
    return out


def record_chief_attempt(job: dict, agent: str, at: dt.datetime) -> None:
    state = read_json(d("duties.json")) or {}
    state.setdefault("attempts", {})[job["id"]] = {
        "at": iso(at), "agent": agent, "fingerprint": chief_fingerprint(job)}
    write_json(d("duties.json"), state)


def review_progress(agent: str, job: str, step: int, note: str, at: dt.datetime) -> None:
    active = read_json(d("active.json")) or {}
    slug = active.get("chain")
    elected = is_elected_chief(agent, at, slug) if slug else is_elected_chief(agent, at)
    if not elected or active.get("agent") != agent or active.get("job") != job or not active.get("expiresAt") or parse(active["expiresAt"]) <= at:
        raise ValueError("Only the elected Chief may update its active review")
    if not 0 <= step <= 3:
        raise ValueError("Review steps are 0-3: inputs checked, evidence reviewed, ruling recorded")
    if step < (active.get("progress") or {}).get("step", 0):
        raise ValueError("Review progress cannot move backwards")
    active["progress"] = {"step": step, "of": 3, "note": note, "at": iso(at)}
    write_json(d("active.json"), active)


def publish_chief_inbox(items: list, leader: str | None, at: dt.datetime, dest: pathlib.Path | None = None) -> None:
    """A durable inbox for app/cloud Chiefs too, with bounded repeated delivery.
    History of Science duties use a separate file when its Chief is not orbit-with-ben's."""
    dest = dest or d("inbox.json")
    previous = read_json(dest) or {}
    rows = [{"id": j["id"], "title": j.get("title", ""), "fingerprint": chief_fingerprint(j)} for j in items]
    same = previous.get("agent") == leader and previous.get("jobs") == rows
    since = previous.get("since") if same else iso(at)
    old_waits = previous.get("waiting", {}) if previous.get("agent") == leader else {}
    waiting = {row["id"]: {"fingerprint": row["fingerprint"],
                "since": old_waits.get(row["id"], {}).get("since", iso(at))
                if old_waits.get(row["id"], {}).get("fingerprint") == row["fingerprint"] else iso(at)}
               for row in rows}
    sent = previous.get("notified_at", "") if same else ""
    # When the Chief last moved its inbox: a duty left the list or its evidence changed. A Chief that is clearing
    # duties is not stalled, even while one it cannot settle yet keeps waiting (chief_delivery_overdue).
    progress = previous.get("progress_at", "") if same else iso(at)
    if previous.get("agent") != leader or not progress:
        progress = iso(at)
    if items and cloud_chief(leader):
        try:
            due = not sent or at - parse(sent) >= dt.timedelta(minutes=10)
        except ValueError:
            due = True
        if due and notify("Chief duties for " + NAMES.get(leader, leader) + ": " +
                          "; ".join(j["id"] + " " + j.get("title", "")[:120] for j in items) +
                          ". Resolve or delegate these before ordinary work; record each decision on its job."):
            sent = iso(at)
    write_json(dest, {"at": iso(at), "agent": leader, "since": since, "progress_at": progress,
                      "notified_at": sent, "jobs": rows, "waiting": waiting})


def chief_delivery_overdue(agent: str | None, at: dt.datetime, dest: pathlib.Path | None = None) -> bool:
    """An app/cloud Chief that leaves delivered duties untouched yields to the next Chief."""
    if not cloud_chief(agent):
        return False
    inbox = read_json(dest or d("inbox.json")) or {}
    if inbox.get("agent") != agent or not inbox.get("notified_at"):
        return False
    data = read_json(STUDIO / "jobs" / "queue.json") or {}
    # Never preempt a live Chief claim. Normal credit/error failover still applies.
    if any(j.get("status") == "claimed" and j.get("by") == agent
           and (not j.get("eta") or parse(j["eta"]) > at) for j in data.get("jobs", [])):
        return False
    # Claude's cloud Chief runs hourly at :50, so a 30-min window benched it every hour (5 Nov 2026: down until 22:13Z,
    # doubling each time). 75 min still benched it every night (9-10 Nov 2026: Chief flipped between Claude and Grok
    # Bot about every 40 min) because one duty it could not settle yet counted as a stall while it cleared the rest.
    # Now: two full runs plus margin, and only when the inbox has not moved at all in that time.
    limit = dt.timedelta(minutes=int(os.environ.get("CHIEF_DUTY_ACK_MIN", "30")) if agent != "claude"
                         else int(os.environ.get("CHIEF_DUTY_ACK_MIN_CLAUDE", "150")))
    try:
        if at - parse(inbox.get("progress_at") or inbox.get("since") or "") < limit:
            return False   # a duty was settled or re-parked inside the window: the Chief is working
    except (TypeError, ValueError):
        pass
    for item in inbox.get("waiting", {}).values():
        try:
            if at - parse(item["since"]) >= limit:
                return True
        except (KeyError, TypeError, ValueError):
            pass
    return False


WORKER_AUTHORITY = """You are a WORKER, not the elected Chief. No final OK or PASS, no merge, no change to AGENTS.md
or the Never list. Park protected calls with jobs.py block <id> --agent {agent} --reason "parked for Chief: ..." --git.
A model or task fallback does not grant Chief authority. Real money and Ben's watch of a finished cut stay with Ben; everything
else you can't decide goes to the Chief, never to Ben (AGENTS.md, 5 Nov 2026)."""
CHIEF_AUTHORITY = """You are the ELECTED ACTING CHIEF under Ben's order ({order}).
You may make the ordinary Chief decisions (reviews, PASS, merges and final OKs) within the existing channel rules.
Do not park a decision merely because Grok or Claude is unavailable. Check chief_relay.py status again before a
protected call; if a higher-priority Chief has returned, hand the decision back. Use your own agent id, never chief.
Money, public/irreversible actions, failed gates and the Never list remain subject to their existing rules. Ben only watches
finished cuts, spends real money and does his own logins (AGENTS.md, 5 Nov 2026): decide everything else yourself, including
private or internal copies (iCloud UAT, the board's watch store, checksum-verified NAS moves), which are not irreversible.
Never park a job for Ben's OK on anything else."""


def authority_prompt(agent: str, leader: str | None, repo: str | None = None) -> str:
    guest = bool(repo and repo != channels.default())
    order = ("11 Nov 2026: Grok -> Claude -> Codex -> Gemini" if guest
             else "26 Oct 2026, reordered 9 Nov 2026: Claude -> Grok -> Codex -> Gemini")
    return (CHIEF_AUTHORITY if agent == leader else WORKER_AUTHORITY).format(agent=agent, order=order)


def cloud_chief(who) -> bool:
    """A Chief that isn't a Mini CLI (Grok Bot, or Claude under Ben's override): the Mini CLIs are its workers."""
    return who is not None and who not in routing.MINI_WORKERS


# ---- the run ----

def brief_channels(agent: str, checkouts: dict | None = None) -> dict:
    """The parts of the brief that are about channels, each built from the channel files, so the brief names no
    channel itself (J2618, 11 Nov 2026). `checkouts` is {channel: its checkout} for every channel; by default the
    studio's own and the others', as the channel files give them.

    The checkout that carries the studio is step 1: the home channel's while a channel's repo carries the studio, the
    studio's own once it has one (then every channel is one of the others). Every other channel gets a step-2 line
    (2, 2b, 2c ...), its flag for the balance check and a note on its queue jobs. A channel with a desk (`desk` in
    its channel file: the desk tool's path and the desk's number) also gets the desk inbox, the desk-first rule and
    its way of reporting. For today's two channels the result reads exactly as the hand-written brief did (a test
    holds the old text against it)."""
    studio = channels.studio_slug()          # None once the studio has a repo of its own
    paths = dict(checkouts or {**({studio: STUDIO} if studio else {}), **OTHERS})
    studio_path = paths.get(studio, STUDIO)
    rules = {slug: channels.rules_phrase(path) for slug, path in paths.items()}
    others = [slug for slug in paths if slug != studio]
    desks = {slug: channels.desk(slug) for slug in others if channels.desk(slug)}
    label, tool = channels.label, lambda slug: pathlib.PurePosixPath(desks[slug]["tool"]).name
    steps, first, notes = [], [], []
    for i, slug in enumerate(others):
        line = f"2{'' if i == 0 else chr(ord('a') + i)}. {channels.name(slug)} ({paths[slug]}): git pull. Read its {rules[slug]}"
        if slug in desks:
            steps.append(line + f' ("The desk"). Run its desk inbox:\n     python3 {desks[slug]["tool"]} inbox --as {agent}   '
                                f"(run in the {label(slug)} checkout; there is no scripts/{tool(slug)})")
            first.append(f"   If it says {channels.name(slug)} first: take the single oldest {label(slug)} desk task you can do "
                         f"now, and go to step 4. Only if\n   there is none, fall through to the {channels.studio_short()} queue below.\n")
            notes.append(f'   Queue jobs marked `{slug}` (repo: {slug}, e.g. "{label(slug)} 007 Shorts VO") are NOT {label(slug)} '
                         f"desk tasks: they are normal queue jobs\n   that `jobs.py next` hands out like any other. Do them in "
                         f'the {label(slug)} checkout, following its {rules[slug]}. "{label(slug)} desk tasks"\n   means only '
                         f"desk #{desks[slug]['number']} messages that are not in the queue.\n")
        else:
            steps.append(line + ".")
            notes.append(f"   Queue jobs marked `{slug}` (repo: {slug}) are normal queue jobs that `jobs.py next` hands out like "
                         f"any other.\n   Do them in the {label(slug)} checkout, following its {rules[slug]}.\n")
    desk_labels = " or ".join(label(slug) for slug in desks)
    return {
        "studio_name": channels.studio_name(), "studio": studio_path,
        "studio_rules": channels.rules_phrase(studio_path), "studio_label": channels.studio_short(),
        "desk_ids": "".join(f", {tool(slug)} --as/--from" for slug in desks),
        "channel_steps": "\n".join(steps) or "2. No other channel is plugged in.",
        "balance_flags": " ".join(f'--{slug} "{paths[slug]}"' for slug in others),
        "desk_first": "".join(first), "queue_notes": "".join(notes),
        "film_example": f"{label(others[0] if others else channels.default())}:006",
        "desk_or": f"on the {desk_labels}\n   desk, or " if desks else "",
        "desk_claim": f", or the {desk_labels}\n   desk's own rule" if desks else "",
        "desk_reports": "".join(f"; {label(slug)} with  {tool(slug)} post --from {agent} --to claude ..." for slug in desks),
    }


def worker_only_steps() -> str:
    """What a worker that is not the Chief is told to skip and still do, in the sentence that goes into its brief."""
    others = list(OTHERS)
    desks = [slug for slug in others if channels.desk(slug)]
    skip = "the channel check" + (f" and the {' and '.join(channels.label(s) for s in desks)} desk inbox" if desks else "")
    if not others:
        return f"In step 3 skip {skip}: do only the job `jobs.py next` gives you. If it exits 10, stop without posting"
    return (f"In step 3 skip {skip}: do only the job "
            f"`jobs.py next` gives you, and that includes {' and '.join(f'`{s}`' for s in others)} queue jobs "
            f"({', '.join(f'repo: {s}' for s in others)}), which are normal "
            f"queue jobs, not desk tasks: do them in the {' or '.join(channels.label(s) for s in others)} checkout. "
            "If it exits 10, stop without posting")


PROMPT = """You are {name}, {role} on the Mac mini because {why}. You run unattended: do ONE job, then stop.
Your agent id is `{agent}` everywhere (jobs.py --agent, studio.py --by{desk_ids}).

0. If a git pull fails (no space left, or local files in the way), run  python3 scripts/mini_repair.py --apply
   (safe: caches, clean temp worktrees; blocking files are kept in ~/_desk/rescue, local edits stashed, local commits
   pushed to a rescue branch first) and pull again. Still under 20 GB free: move render scratch to the NAS by
   AGENTS.md "Render scratch" before anything else.
1. {studio_name} ({studio}): git pull. Read {studio_rules} (the rules, the Never list, "Stop and ask Ben", "Who does what",
   "Chief relay"). Run: python3 scripts/studio_thread.py read   and   python3 scripts/studio.py board
{channel_steps}
3. Follow the DISPATCH PRIORITY or CHIEF REVIEW PRIORITY below first, if supplied; otherwise, which channel first (Ben, 9 Oct: 4 videos a month on each channel; credits follow):
     python3 scripts/channel_balance.py {balance_flags}
{desk_first}{queue_notes}   The {studio_label} job queue (AGENTS.md "Job queue"):  python3 scripts/jobs.py next --agent {agent} --can mini,gemini,any --git
   If it prints a job, that job is yours: do it (step 4), then  jobs.py done|block|release <id> --agent {agent} ... --git.
   Ben watches % done on the board: split the job into n steps (replace a default_plan at step 0; otherwise keep its earlier n) and run
     python3 scripts/jobs.py progress <id> --agent {agent} --step <k> --of <n> --git
   with --action "<plain-English action still unfinished>"; update that action as the remaining work changes. Use k=0 when you start and again after each finished step (k = steps done), before you release or finish.
   During a long step, repeat the current k with an honest --note at least every 5 minutes; never increase k for elapsed time.
   As soon as you choose the video(s), include --films {film_example} (or {studio_label}:028,{studio_label}:029 for a shared job) on that progress
   command, and --note with the concrete outcome of each finished step. Keep the links on later progress updates.
   This connects the live job to the video's swim lane. A job parked for review is not an approved film stage.
   Inspect your actual input tools once at session start. Record demonstrated audio_input/moving_video_input only
   if this session can really perceive that medium (ffmpeg, ASR, a player window or a model name is not proof):
     python3 scripts/chief_relay.py capabilities --agent {agent} --available '<demonstrated identifiers, or empty>' --evidence '<actual tool/probe result>'
   If the assigned work cannot proceed because of an input capability, park it with a typed hold, not a generic
   six-hour input retry: jobs.py wait <id> --agent {agent} --type capability --requires audio_input
   --condition '<what input is unavailable and what was actually tested>' --check-at '<future UTC time>' --git.
   For a condition verification, update its original parent with --recheck <verification id> and finish the
   verification itself. Never claim to hear audio or review motion from text/stills/measurements.
   If it exits 10 (nothing waiting): pick the single oldest task for the Chief that isn't in the queue ({desk_or}a Claude message on #99 asking the Chief for something with no Chief reply yet).
   If nothing is waiting anywhere, stop without posting.
4. Do that one task, following that repo's AGENTS.md exactly: claim before work (studio.py claim --git{desk_claim}), commit only from a clean worktree (your own: `git worktree add --detach <dir> origin/main` or
   `-b <branch>`; never `git worktree add --force <dir> main`, which moves main under the shared checkout), never spend money or credit beyond the written rules, never
   upload, schedule, retitle or change privacy on YouTube unless the job brief or a Chief/Claude message for that task
   says to, never delete a video or anything on the NAS, and never print secrets. Chief owns AGENTS.md and the Never list
   (Ben, 9-10 Oct 2026): a job added by chief, a "[Chief]" OK, or a brief saying "Ben approved (relayed by Chief)" is
   full authorisation, including Never-list exceptions it names. Never ask Ben to re-post an OK on #99. If a step needs
   Ben (real money, a sign-in, something that can't be undone), say so in your report and stop.
   A job that needs `gemini` is a facts-and-numbers check: run it through Gemini with the `agy` CLI (AGENTS.md "Who does
   what"), claim it as {agent}/gemini, and commit Gemini's findings as the job says. You check Gemini's output is complete;
   you don't rewrite its findings or any spoken line.
5. Report: {studio_label} by writing the report to a file and posting it with  python3 scripts/studio_thread.py post -f <file>
   (start with "{name} covering"){desk_reports}  Say what you did,
   what's next, and what blocks you. Never put the report text on the command line: the shell runs any backtick
   or $(...) in it as a command and posts the output.
{authority}
{priority}
   Each job's kind selects its specialist worker. Acting-Chief authority is a separate role; a worker fallback does
   not inherit it merely because it runs Claude or GPT.
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
    argv = shlex.split(cmd) if cmd else [sys.executable, str(STUDIO / "scripts" / "studio_thread.py"), "post"]
    try:
        r = subprocess.run(argv + [text], cwd=str(STUDIO) if STUDIO.is_dir() else None, capture_output=True, text=True,
                           timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"notify failed: {e}")
        return False
    if r.returncode != 0:
        log(f"notify failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
        return False
    return True


MINIWORK = pathlib.Path(os.environ.get("MINIWORK", "/Volumes/MiniWork"))


SSD_PROBE_S = int(os.environ.get("CHIEF_SSD_PROBE_S", "5"))
SSD_PROBE_KEEP_S = int(os.environ.get("CHIEF_SSD_PROBE_KEEP_S", "600"))
_SSD_PROBE = "import os,sys; s=sys.argv[1]; print(os.stat(os.path.dirname(s)).st_dev if os.path.isdir(s) and os.access(s, os.W_OK) else '')"
_ssd_seen: dict = {}


def _ssd_dev(s: pathlib.Path) -> int | None:
    """The device id of the SSD's scratch folder, asked from a child process with a timeout (None: not there, not
    writable, or no answer). macOS can hold a process on a permission dialog for a removable volume, and nobody is at
    the Mini to click it: on 9 Nov 2026 this relay checked the SSD itself and went silent from 20:53Z (J2444/J2445
    record the block). A child that hangs is killed; the relay carries on with /private/tmp."""
    try:
        r = subprocess.run([sys.executable, "-c", _SSD_PROBE, str(s)], capture_output=True, text=True,
                           timeout=SSD_PROBE_S)
    except subprocess.TimeoutExpired:
        log(f"SSD check got no answer in {SSD_PROBE_S}s: macOS is probably waiting on a permission dialog "
            f"(give Python Full Disk Access on the Mini). Using /private/tmp.")
        return None
    except OSError:
        return None
    out = r.stdout.strip()
    return int(out) if r.returncode == 0 and out.isdigit() else None


def scratch_dir() -> pathlib.Path | None:
    """The Mini's working SSD (Ben, 9 Nov 2026: a 250 GB SanDisk, APFS "MiniWork") when it is mounted and writable.
    It must be its own volume: a /Volumes/MiniWork folder left on the internal disk after an unplug would fill the very
    disk this is meant to keep free. The answer is kept for SSD_PROBE_KEEP_S, so a blocked volume costs one short
    wait every ten minutes, not one per wake."""
    s = MINIWORK / "scratch"
    seen = _ssd_seen.get(str(s))
    if seen and time.monotonic() - seen[0] < SSD_PROBE_KEEP_S:
        return seen[1]
    try:
        dev, home_dev = _ssd_dev(s), os.stat(HOME).st_dev
    except OSError:
        dev, home_dev = None, None
    got = s if dev is not None and dev != home_dev else None
    _ssd_seen[str(s)] = (time.monotonic(), got)
    return got


def run_cli(agent: str, prompt: str, cap_s: int, model: str = "") -> tuple:
    """(exit code, tail of output). Exit 124 = killed at the cap. The whole process group is killed, so a CLI's
    child processes don't outlive the cap."""
    b, args = cli_spec(agent, model)
    # The exact command, minus the prompt, so a usage error (exit 2) can be matched to its flags. Flags hold no secrets.
    log(f"cmd: {b} {' '.join(shlex.quote(a) for a in args)} <prompt>" + (" (flags from the env)" if os.environ.get(
        {"cursor": "CURSOR_AGENT_FLAGS"}.get(agent, "")) else ""))
    # The thread tool tags its posts "[Chief] [Cursor]" from this variable. PATH: launchd's shell has no Homebrew or user bins, and doesn't
    # expand "~", so put the real dirs first; the woken agent then finds gh, agy, agent and codex itself.
    extra = [str(HOME / ".local" / "bin"), str(HOME / ".npm-global" / "bin"), "/opt/homebrew/bin", "/usr/local/bin"]
    env = dict(os.environ, PATH=os.pathsep.join(extra + [os.environ.get("PATH", "/usr/bin:/bin")]))
    env[channels.studio_env("AGENT")] = agent
    # Render scratch on the SSD when it is there (TMPDIR is what Python's tempfile, ffmpeg helpers and most CLIs use;
    # STUDIO_SCRATCH is the folder AGENTS.md tells agents to put worktrees, frames and part renders in).
    sd = scratch_dir()
    env.update(TMPDIR=f"{sd}/", STUDIO_SCRATCH=str(sd)) if sd else env.update(STUDIO_SCRATCH="/private/tmp")
    p = subprocess.Popen([b] + args + [prompt], cwd=str(STUDIO) if STUDIO.is_dir() else None, stdout=subprocess.PIPE,
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
        ok = notify(f"Chief relay: **Grok Bot is Chief again** ({states}). Cursor, Codex and Gemini keep running the job queue as workers; Chief owns reviews/decisions.")
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
    chain_rows = (read_json(d("chain.json")) or {}).get("rows") or []
    return {"at": iso(at), "state": state, "agent": agent, "note": note[:200], "host": "mac-mini", "chief": chief,
            "chain": chain_rows}


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
    waiting = parked_reviews(read_json(STUDIO / "jobs" / "queue.json") or {})
    if not waiting:
        return
    states = "; ".join(f"{NAMES.get(a, a)}: {why}" for a, up, why in rows)
    if notify(f"Chief relay: @TheLaughingGod1986 no Chief for {int((at - parse(spell['since'])).total_seconds() // 3600)} h "
              f"and {len(waiting)} review(s) waiting ({', '.join(j['id'] for j in waiting[:8])}). {states}. Workers keep "
              f"running the queue; nothing is lost. A top-up is your call."):
        write_json(p, dict(spell, alerted=iso(at)))


def push_heartbeat(at: dt.datetime, state: str, agent: str = "", note: str = "") -> None:
    """One parentless commit holding heartbeat.json, force-pushed to refs/heads/mini-heartbeat. Never raises."""
    if os.environ.get("CHIEF_HEARTBEAT", "1") == "0" or not (STUDIO / ".git").exists():
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
        git = ["git", "-C", str(STUDIO)]
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
    jobs = STUDIO / "scripts" / "jobs.py"
    if not jobs.exists():
        return True
    subprocess.run(["git", "-C", str(STUDIO), "pull", "-q", "--ff-only"], capture_output=True, timeout=120)
    try:
        r = subprocess.run([sys.executable, str(jobs), "next", "--agent", agent, "--can", "mini,gemini,any", "--peek"],
                           cwd=str(STUDIO), capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return True
    return r.returncode != 10


def addressed_to(agent: str) -> list:
    """Open jobs only this agent may claim (`jobs.py add --for <agent>`), e.g. Claude asking Codex for its own view."""
    q = read_json(STUDIO / "jobs" / "queue.json") or {}
    by_id = {j["id"]: j for j in q.get("jobs", [])}
    import jobs
    at = now()
    return [j["id"] for j in q.get("jobs", []) if j.get("for") == agent and j.get("status") == "open"
            and not workflow.external_hold(j, at)
            and (not j.get("after") or by_id.get(j["after"], {}).get("status") == "done")
            and (j.get("kind") != "chief" or elected_for(agent, at, j))]


def next_job(agent: str):
    """The queue job `agent` would get next (the one it holds, else the next claimable Mini job), or None."""
    try:
        import jobs  # noqa: E402  (jobs imports this module; by now it's loaded)
        data = jobs.load(STUDIO / "jobs" / "queue.json")
        at = jobs.now()
        return jobs.choose_next(data, agent, jobs.MINI_NEEDS, at)
    except Exception as e:  # an unreadable queue never stops a run: the worker just gets its default model
        log(f"routing: queue not readable ({e.__class__.__name__}); default worker and model")
        return None


# ---- Claude out of usage: its jobs go to Cursor on the Claude model (Ben, 11 Oct 2026 23:40) ----

def board_films() -> pathlib.Path:
    """The folder of film folders the stage board tracks: the board's channel, in that channel's own checkout."""
    slug = channels.board_channel()
    return channels.films_dir(slug, channels.repo_path(slug, HOME))


def claude_ledger_note(at: dt.datetime):
    """The newest Claude ledger note (ai_spend.py record --pool claude) from the last CHIEF_CLAUDE_OUT_H hours that says
    it hit a limit, or None."""
    hours = float(os.environ.get("CHIEF_CLAUDE_OUT_H", "5"))
    # the studio's own records folder, inside the studio checkout (the loader knows where that folder is)
    ledger = STUDIO / channels.studio_records("ai_spend", "ledger.jsonl").relative_to(channels.ROOT)
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
    url = os.environ.get("CHIEF_CLAUDE_BEAT_URL", f"https://raw.githubusercontent.com/{channels.studio_github()}/"
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
        subprocess.run(["git", "-C", str(STUDIO), "fetch", "-q", "origin",
                        f"+refs/heads/{CLAUDE_BEAT_BRANCH}:refs/remotes/origin/{CLAUDE_BEAT_BRANCH}"],
                       capture_output=True, timeout=60)
        r = subprocess.run(["git", "-C", str(STUDIO), "show", f"origin/{CLAUDE_BEAT_BRANCH}:heartbeat.json"],
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
        # A MacBook job stays on the MacBook (29 Oct 2026: J1194/J1195 were handed to Gemini on the Mini while
        # Claude was marked down, though they were never Claude's to run).
        if not routing.claude_owned(j) or j.get("kind") == "chief" or j.get("needs") in ("ben", "macbook"):
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


def stranded_jobs(data: dict, up: set, at=None) -> list:
    """Jobs the relay already handed to a worker (rerouted_from) that haven't started, whose worker is now down (out of
    usage): they walk on down their chain. Jobs Claude or Chief addressed by hand (no rerouted_from) wait for that
    agent, e.g. a second opinion from Codex."""
    capabilities = worker_capabilities()
    at = at or now()
    return [j for j in data.get("jobs", []) if j.get("rerouted_from") and j.get("status") == "open"
            and j.get("for") in routing.MINI_WORKERS
            and (j["for"] not in up or workflow.capability_problem(j,j["for"],at,capabilities)
                 or (j.get("model") and not routing.lane_ok(j["for"], j["model"])))]


def stalled_claims(data: dict, at: dt.datetime) -> list:
    """One 45-minute inactivity/ETA grace plus a validated active-run lease, shared with claims and the board."""
    execution = current_execution(at)
    return [j for j in data.get("jobs", []) if j.get("by") in routing.MINI_WORKERS
            and workflow.claim_is_stalled(j,at,execution)]


def jobs_py(*args):
    """Run `jobs.py <args> --git` in the engine checkout. The finished process, or None if it could not be run."""
    argv = [sys.executable, str(STUDIO / "scripts" / "jobs.py"), *args, "--git"]
    try:
        return subprocess.run(argv, cwd=str(STUDIO), capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"jobs.py {' '.join(args[:2])} failed: {e}")
        return None


def reroute(job: dict, to: str, model: str, note: str) -> bool:
    """`jobs.py reroute <id> --to <to> --model <model> --git` in the engine checkout. True when it went through."""
    r = jobs_py("reroute", job["id"], "--agent", "relay", "--to", to, "--note", note,
                *(["--model", model] if model and model in routing.MODELS else []))
    if r is None:
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
        argv = [sys.executable, str(STUDIO / "scripts" / "jobs.py"), "handback", j["id"], "--agent", "relay",
                "--note", "Claude is back online", "--git"]
        try:
            r = subprocess.run(argv, cwd=str(STUDIO), capture_output=True, text=True, timeout=180)
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
    data = read_json(STUDIO / "jobs" / "queue.json") or {}
    out, why = claude_out(at, data)
    if any(claude_blocked_on_limit(j) for j in data.get("jobs", [])) and not read_json(d("down", "claude.json")):
        retry_h = float(os.environ.get("CHIEF_RETRY_H", "3"))
        mark_down("claude", "a Claude job was blocked on a usage limit", at + dt.timedelta(hours=retry_h), at)
    if not out:
        hand_back_claude(data)
    capabilities = worker_capabilities()
    eligible = lambda j: {a for a in up if not workflow.capability_problem(j,a,at,capabilities)}
    moves = [(j, routing.next_lane(j, "claude", eligible(j)), f"Claude out of usage ({why})")
             for j in claude_jobs_to_reroute(data, at, out)]
    moves += [(j, routing.next_lane(j, j["for"], eligible(j), j.get("model") or ""), f"{NAMES.get(j['for'], j['for'])} is unavailable or lacks required input")
              for j in stranded_jobs(data, up, at)]
    moves += [(j, routing.next_lane(j, j["by"], eligible(j), j.get("model") or ""), f"{NAMES.get(j['by'], j['by'])} stopped answering on it (claim past its ETA)")
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
    if os.environ.get("CHIEF_REFILL", "1") == "0" or not (STUDIO / "scripts" / "refill.py").exists():
        return []
    try:
        r = subprocess.run([sys.executable, str(STUDIO / "scripts" / "refill.py"), "refill", "--git"], cwd=str(STUDIO),
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
        r = subprocess.run([sys.executable, str(STUDIO / "scripts" / "refill.py"), "escalate", "--git",
                            "--hours", os.environ.get("CHIEF_STALE_H", "2")], cwd=str(STUDIO),
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
    if (STUDIO / ".git").exists():
        try:
            pulled = subprocess.run(["git", "-C", str(STUDIO), "pull", "-q", "--ff-only"], capture_output=True,
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
        spec = importlib.util.spec_from_file_location("mini_repair", STUDIO / "scripts" / "mini_repair.py")
        if spec is None or not (STUDIO / "scripts" / "mini_repair.py").exists():
            spec = importlib.util.spec_from_file_location("mini_repair", pathlib.Path(__file__).with_name("mini_repair.py"))
        mr = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mr)
        rep = mr.repair(apply=True, repos=[r for r in (STUDIO, *OTHERS.values()) if (r / ".git").exists()],
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


def _pid_alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _offload_finished(at: dt.datetime) -> bool:
    """Report a background offload that has ended (its JSON report is in offload.out). True while one still runs."""
    st = read_json(d("offload.json")) or {}
    if not st.get("running"):
        return False
    if _pid_alive(st.get("pid")):
        return True
    try:
        txt = d("offload.out").read_text()
        rep = json.loads(txt[txt.index("{"):])
        no = _load_offload()
        line = no.summary(rep)
    except Exception as e:  # no report (killed, crashed): record it and let the next pass start again
        log(f"offload ended without a report: {e.__class__.__name__}: {str(e)[:200]}")
        write_json(d("offload.json"), {"at": st.get("at") or iso(at), "error": "ended without a report"})
        return False
    write_json(d("offload.json"), {"at": st.get("at") or iso(at), "before_mb": rep["before_mb"], "after_mb": rep["after_mb"],
                                   "moved": len(rep["moved"]), "kept": len(rep["kept"]), "nas": rep["nas"]})
    log(line)
    if rep["moved"] or rep["kept"] or rep["nas"] != "ok":
        notify(f"Chief relay: {line}")
    return False


def _offload_path() -> pathlib.Path:
    path = STUDIO / "scripts" / "nas_offload.py"
    return path if path.exists() else pathlib.Path(__file__).with_name("nas_offload.py")


def _load_offload():
    import importlib.util
    spec = importlib.util.spec_from_file_location("nas_offload", _offload_path())
    no = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(no)
    return no


def offload_scratch(at: dt.datetime) -> None:
    """Ben, 28 Oct 2026: "The external storage we can use our NAS for now". Under CHIEF_OFFLOAD_GB free (default 40),
    move render scratch untouched for CHIEF_OFFLOAD_AGE_H (default 24 h) from /private/tmp to the NAS with scripts/nas_offload.py (rsync, sha256 on
    both sides, the Mini copy goes only on a full match, never deletes on the NAS), at most every CHIEF_OFFLOAD_H
    hours, and say what moved on the thread. Never stops the relay.

    It runs as its own background process (Ben, 9 Nov 2026): run inside the relay, one slow copy to the NAS held the
    whole relay from 05:52 to past noon with no log line and no job started. The relay starts it, carries on, and a
    later pass reports it once it has ended. nas_offload.py's own lock keeps it to one at a time."""
    if sys.platform != "darwin" and not os.environ.get("CHIEF_OFFLOAD_ANY_OS"):
        return  # the Mini's /private/tmp and /Volumes/data only exist on macOS
    if _offload_finished(at):
        return  # still copying in the background
    # Ben, 9 Nov 2026 (disk at 3 GB): start at 40 GB free, not 20, and move scratch untouched for 24 h, not 48.
    target = float(os.environ.get("CHIEF_OFFLOAD_GB", "40"))
    age_h = os.environ.get("CHIEF_OFFLOAD_AGE_H", "24")
    try:
        free = shutil.disk_usage(str(HOME)).free // (1024 * 1024)
    except OSError:
        return
    if free >= target * 1024:
        return
    last = read_json(d("offload.json")) or {}
    if last.get("at") and at - parse(last["at"]) < dt.timedelta(hours=float(os.environ.get("CHIEF_OFFLOAD_H", "3"))):
        return
    try:
        d().mkdir(parents=True, exist_ok=True)
        with open(d("offload.out"), "w") as out:
            proc = subprocess.Popen([sys.executable, str(_offload_path()), "--apply", "--json", "--target-gb", str(target),
                                     "--min-age-h", age_h],
                                    stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                    start_new_session=True, cwd=str(HOME))
    except Exception as e:  # never let the offload stop the relay
        log(f"offload failed: {e.__class__.__name__}: {e}")
        write_json(d("offload.json"), {"at": iso(at), "error": str(e)[:300]})
        return
    write_json(d("offload.json"), {"at": iso(at), "running": True, "pid": proc.pid})
    log(f"offload: started in the background (pid {proc.pid}, {free:,} MB free)")


def weekly_caches(at: dt.datetime) -> None:
    """Ben, 9 Nov 2026 (disk at 3 GB): clear the caches that rebuild themselves (Homebrew, npm, pip, uv) once every
    CHIEF_CACHE_DAYS days (default 7), not only when the disk is nearly full. It runs as its own background process,
    like the NAS offload, so a slow `brew cleanup` never holds the relay. Checkouts and media are untouched."""
    if sys.platform != "darwin" and not os.environ.get("CHIEF_OFFLOAD_ANY_OS"):
        return
    last = read_json(d("caches.json")) or {}
    if last.get("at") and at - parse(last["at"]) < dt.timedelta(days=float(os.environ.get("CHIEF_CACHE_DAYS", "7"))):
        return
    path = STUDIO / "scripts" / "mini_repair.py"
    if not path.exists():
        path = pathlib.Path(__file__).with_name("mini_repair.py")
    try:
        d().mkdir(parents=True, exist_ok=True)
        with open(d("caches.out"), "w") as out:
            proc = subprocess.Popen([sys.executable, str(path), "--apply", "--caches-only", "--json"], stdout=out,
                                    stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True,
                                    cwd=str(HOME))
    except Exception as e:  # never let it stop the relay
        log(f"weekly cache clean failed to start: {e.__class__.__name__}: {e}")
        write_json(d("caches.json"), {"at": iso(at), "error": str(e)[:300]})
        return
    write_json(d("caches.json"), {"at": iso(at), "pid": proc.pid})
    log(f"weekly cache clean: started in the background (pid {proc.pid})")


def yield_monthly_for_dispatch(selection):
    """Called under the relay run lock, after the previous run_cli has returned."""
    if not selection or not selection.get("yield_monthly"):
        return True
    if current_execution(now()):
        log("immediate request waits: an execution lease is still active")
        return False
    import jobs
    def apply(current):
        try:
            released = jobs.yield_monthly_for_request(current, selection["job"]["id"], selection["yield_monthly"], now())
            return released, None, []
        except ValueError as error:
            return None, str(error), []
    released, error = jobs.with_git(apply, "jobs: yield monthly report at safe boundary for user claim request")
    if error:
        log("immediate request handoff requires replanning: " + error)
        return False
    log("immediate request " + selection["job"]["id"] + ": preserved and queued " + ", ".join(released or []))
    return True


STUCK_RUNS = 3  # runs in a row at the time cap, with no step finished, before a job is parked for the Chief


def capped_runs_in_a_row(job: dict, runs: list) -> int:
    """How many of this job's newest runs, in a row, were killed at the time cap since it last finished a step.

    10 Nov 2026: J2466 began its first step again in four 25-minute runs, and the Mini did nothing else for 90
    minutes. A run killed at the cap (exit 124) leaves the job claimed, and the relay resumes a claim before
    anything else, so nothing broke the loop. Only capped runs count: a worker that releases a job with a note has
    handed it back on purpose (a detached render it will check later), and that is not a loop. The count starts
    again when a step is finished, when the job is added or reopened, and when another worker takes it.
    """
    moved = None
    best = -1
    for h in job.get("history") or []:
        what, at = str(h.get("what") or ""), workflow.timestamp(h.get("at"))
        if not at:
            continue
        if what.startswith(("added", "reopened")):
            moved, best = at, -1
        step = re.match(r"step (\d+) of \d+ done", what)
        if step and int(step.group(1)) > best:
            if best >= 0 or int(step.group(1)) > 0:  # "step 0 of N" at the start of a run is not a finished step
                moved = at
            best = int(step.group(1))
    count, worker = 0, None
    for row in reversed([r for r in runs if r.get("job") == job.get("id")]):
        started = workflow.timestamp(row.get("at"))
        if row.get("exit") != 124 or not started or (worker and row.get("worker") != worker):
            break
        # History stamps are to the minute. A run that began in the same minute as the last step is not counted.
        if moved and started.replace(second=0, microsecond=0) <= moved:
            break
        worker = row.get("worker")
        count += 1
    return count


def stuck_runs(job: dict) -> int:
    try:
        lines = d("runs.jsonl").read_text().splitlines()[-400:]
    except OSError:
        return 0
    rows = []
    for line in lines:
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    return capped_runs_in_a_row(job, rows)


def park_stuck(job: dict, runs: int) -> bool:
    """`jobs.py stuck <id> --runs N --git` in the engine checkout. True when the job is now parked for the Chief."""
    r = jobs_py("stuck", job["id"], "--agent", "relay", "--runs", str(runs))
    if r is None:
        return False
    if r.returncode != 0:
        log(f"stuck: parking {job['id']} failed (exit {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}")
        return False
    return True


def recorded_task_outcome(job, who, started):
    """A worker that parked its task has not necessarily failed as an agent.

    Require a fresh canonical outcome by this run's owner; an old hold, CLI
    prose or launch signal cannot suppress a real worker failure.
    """
    if not job:
        return ""
    data = read_json(STUDIO / "jobs" / "queue.json") or {}
    current = next((j for j in data.get("jobs", []) if j.get("id") == job["id"]), None)
    if not current or current.get("by") != who or current.get("status") not in {"blocked", "done", "cancelled"}:
        return ""
    floor = started.replace(second=0, microsecond=0)  # canonical queue stamps have minute precision
    expected = {"blocked":"blocked:", "done":"done:", "cancelled":"cancelled"}[current["status"]]
    if any(h.get("by") == who and str(h.get("what") or "").startswith(expected)
           and workflow.timestamp(h.get("at")) and floor <= workflow.timestamp(h["at"]) <= now()
           for h in current.get("history", [])):
        return current["status"]
    return ""


def run_locked(at: dt.datetime) -> int:
    note_grok_posts(at)
    fetch_claude_beat(at)
    flags = load_out(at)
    if flags:
        log("out of credit: " + "; ".join(f"{k} ({v})" for k, v in sorted(flags.items())))
    healthy = self_heal(at)
    offload_scratch(at)  # also when the disk is too full to wake anyone: that is when the NAS helps most
    weekly_caches(at)
    if not healthy:
        log("disk still too full to run a worker: waiting for the next repair")
        return 0
    refresh_probes(at)
    if (STUDIO / "scripts" / "refill.py").exists():
        escalate_stale()
    cap = int(os.environ.get("CHIEF_CAP_S", "1500"))
    # A worker that says it's out of credit is retried after 1 h, not 3 (Ben, 14 Oct 2026: "no worker has credit. I
    # don't believe this"; a 429, or one model's pool read as the whole agent out for 3 h, left the Mini idle). A real
    # longer outage goes in scripts/credit_flags.json with its true reset time.
    retry_h = float(os.environ.get("CHIEF_RETRY_H", "1"))
    # Ben, 12 Oct 2026: the Mini never idles. When a job ends, the next ready job starts straight away in this same
    # run (no waiting for the next launchd tick); CHIEF_CHAIN_MAX bounds one run.
    # Already-attempted released tasks yield to others instead of ending the run.
    chain_max = int(os.environ.get("CHIEF_CHAIN_MAX", "12"))
    chained, last_ran = 0, None
    attempted = set()
    reviewed = set()
    while True:
        desired = code_version()
        write_json(d("runner.json"), {"pid":os.getpid(),"version":LOADED_VERSION,"desiredVersion":desired,"at":iso(now()),
                                     "state":"restarting" if desired != LOADED_VERSION else "ready"})
        if desired != LOADED_VERSION:
            log("runner update: safe boundary reached; yielding to a fresh launchd run")
            return 0
        queue = read_json(STUDIO / "jobs" / "queue.json") or {}
        by_id = {j["id"]:j for j in queue.get("jobs", [])}
        broken = any(j.get("status") in ("open","blocked") and workflow.dependency_problem(j,by_id)
                     and j.get("dependency_problem") != workflow.dependency_problem(j,by_id) for j in queue.get("jobs", []))
        check_due = any(workflow.hold_due(j,by_id,at) and not any(x.get("recheck_of") == j["id"] and x.get("status") in workflow.LIVE for x in queue.get("jobs", [])) for j in queue.get("jobs", []))
        stage_gaps = handoffs.findings(queue, list(handoffs.records(board_films())), at)
        missing_handoff = any(not any(j.get('handoff', {}).get('signature') == gap['signature'] and j.get('status') in workflow.LIVE for j in queue.get('jobs', [])) for gap in stage_gaps)
        if (broken or check_due or missing_handoff) and (STUDIO / "scripts" / "jobs.py").exists():
            result = subprocess.run([sys.executable,str(STUDIO / "scripts/jobs.py"),"reconcile","--agent","relay","--git"],capture_output=True,text=True,timeout=180)
            if result.returncode:
                log("queue reconciliation failed: " + (result.stderr or result.stdout)[-250:])
        # Re-read Claude's heartbeat each pass (at most every 5 min): a chain of worker jobs can hold this run for
        # hours, and on 15 Oct 2026 it kept reading the 04:04 beat until 06:03 after fresh beats at 05:49 and 05:51.
        fetch_claude_beat(now())
        rows, who = acting(at)
        leader = who
        guests = _other_slugs()
        guest = guests[0] if len(guests) == 1 else None
        guest_rows, guest_who = acting(at, guest) if guest else ([], None)
        handover(who, rows, at)
        alert_no_chief(who, rows, at)
        # The board shows who is Chief and who is out, and why (Ben, 21 Oct 2026).
        # `rows` stays the home chain. The other channel is stored under its slug.
        chain_state = {"at": iso(at), "rows": [{"agent": a, "up": up, "why": why[:120]} for a, up, why in rows]}
        if guest:
            chain_state[guest] = {"chief": guest_who,
                                  "rows": [{"agent": a, "up": up, "why": why[:120]} for a, up, why in guest_rows]}
        write_json(d("chain.json"), chain_state)
        log("chain: " + " | ".join(f"{a}={'UP' if up else 'down'} ({why})" for a, up, why in rows))
        if guest:
            log("guest chain: " + " | ".join(f"{a}={'UP' if up else 'down'} ({why})" for a, up, why in guest_rows)
                + f" chief={guest_who}")
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
        # One deadline-first selector ranks Chief duties and production together; named workers retain eligibility.
        chief_inbox = pending_chief_reviews(at)
        if guest and guest_who != leader:
            guest_inbox = [j for j in chief_inbox if job_chain(j)]
            chief_inbox = [j for j in chief_inbox if not job_chain(j)]
            publish_chief_inbox(guest_inbox, guest_who, at, dest=d("inbox-guest.json"))
        publish_chief_inbox(chief_inbox, leader, at)
        if guest and guest_who != leader and chief_delivery_overdue(guest_who, at, dest=d("inbox-guest.json")):
            mark_down(guest_who, "Guest-channel inbox delivered but not progressed within the acknowledgement window",
                      at + stall_window(guest_who, at), at, kind="stalled")
            log(f"Guest-channel duties: {guest_who} did not progress its inbox; electing the next Chief on that chain")
            continue
        if chief_delivery_overdue(leader, at):
            mark_down(leader, "Chief inbox delivered but not progressed within the acknowledgement window",
                      at + stall_window(leader, at), at, kind="stalled")
            log(f"Chief duties: {leader} did not progress its inbox; electing the next available Chief")
            continue
        chief_reviews = [j for j in due_chief_reviews(chief_inbox, leader, at)
                         if j["id"] not in reviewed] if leader in routing.MINI_WORKERS else []
        added = keep_busy()  # refill before selecting, so new ready work is seen in this pass
        if added:
            log(f"refill: added {' '.join(added)} from jobs/backlog.json")
        data = read_json(STUDIO / "jobs" / "queue.json") or {}
        from workflow_board import load_tracker
        data["tracker"] = load_tracker()
        selection = workflow.select_dispatch(data, at, leader, up, lambda j, workers: routing.preferred_worker(j, workers) or next(iter(sorted(workers)), ""),
                                             review_ids={j["id"] for j in chief_reviews}, execution=current_execution(at),
                                             exclude=attempted, capabilities=worker_capabilities())
        # An open/released job that already ran must not be rediscovered by the
        # legacy fallback below. Continue other eligible jobs in this same run.
        if not selection and attempted and data.get("jobs"):
            log("chain: no unattempted eligible jobs; held work and retries preserved")
            push_heartbeat(at, "idle", note="No unattempted eligible jobs; see queue holds and retry records")
            return 0
        if not yield_monthly_for_dispatch(selection):
            return 0
        review_due = bool(selection and selection["mode"] == "review")
        if selection:
            who = selection["worker"]
            if review_due:
                chief_reviews = [selection["job"]] + [j for j in chief_reviews if j["id"] != selection["job"]["id"]]
        addressed = bool(selection and who != leader)
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
        if who != leader:
            worker_only = True
        last_wake = last_seen(who)
        # Overnight (Ben, 7 Oct: carry on overnight) agents are woken for queued jobs only; the 2-hourly sweep for
        # thread/desk tasks runs in the day, so an empty night costs no credit.
        slo, shi = (int(x) for x in os.environ.get("CHIEF_SWEEP_HOURS", "8-22").split("-"))
        sweep = slo <= dt.datetime.now().hour < shi and (
            not last_wake or (at - last_wake) >= dt.timedelta(minutes=int(os.environ.get("CHIEF_SWEEP_MIN", "120"))))
        if worker_only:
            sweep = False
        reviews = chief_reviews if who == leader and not worker_only else []
        review_work = bool(reviews and review_due)
        if not queue_has_work(who) and not sweep and not review_work:
            ago = f"{int((at - last_wake).total_seconds() // 60)} min ago" if last_wake else "never"
            log(f"nothing queued for {who}; last woken {ago}: not waking it")
            push_heartbeat(at, "idle", who, "nothing queued")
            return 0
        names = [r[0] for r in rows]
        above = [f"{NAMES.get(a, a)} is {why}" for a, ok, why in rows[:names.index(who)]] if who in names else []
        why = "The shared queue selected your eligible task" if addressed else ("; ".join(above) or "it is first in line")
        if addressed and rerouted:
            why = (f"the job's earlier worker is out of usage, so the relay walked its fallback chain and handed it to "
                   f"you ({', '.join(rerouted)}; Ben, 11 Oct 2026). Take it with jobs.py next; do it as the primary "
                   f"would, and stop at the same protected calls")
        elif worker_only:
            why = (f"{NAMES.get(leader, leader) or 'No agent'} is Chief (reviews, PASS, merges, decisions, the board) and you are its WORKER for the Mini "
                   f"job queue. {worker_only_steps()}")
        model, job = "", None
        if selection:
            who = selection["worker"]
            job = None if review_work else selection["job"]
            model = routing.model_for({"kind": "chief"} if review_work else job, who)
        elif not addressed and who in routing.MINI_WORKERS:
            who, model, job = route_worker(who, up)
        if job and not review_work:
            capped = stuck_runs(job)
            if capped >= STUCK_RUNS and park_stuck(job, capped):
                log(f"stuck: {job['id']} parked for Chief: {capped} runs in a row hit the cap with no step finished")
                notify(f"Chief relay: {job['id']} is parked for the Chief. {capped} runs in a row hit the time cap "
                       "without finishing a step, so it was not started again. It needs splitting or a narrower next step.")
                attempted.add(job["id"])
                at = now()
                continue
        if chained and not review_work and (job is None or (last_ran and job.get("id") == last_ran)):
            log(f"chain: stop after {chained} job(s): " + ("next job is the one just run (released to retry later)"
                                                         if job else "no next job identified"))
            return 0
        priority = ("CHIEF REVIEW PRIORITY: before taking an ordinary job, review " + reviews[0]["id"] + ": "
                    + str(reviews[0].get("title") or "") + ". Read its body, result and history plus the evidence. "
                    "Keep the original work held until the decision is recorded. Resolve or delegate the next step; "
                    f"Report this review's own progress with python3 scripts/chief_relay.py review-progress --agent {who} --job {reviews[0]['id']} --step N --note 'outcome': "
                    "step 1 after checking inputs/approval, step 2 after reviewing evidence and choosing the ruling, "
                    "step 3 only after recording the ruling and follow-up. Do not reuse the worker's completed steps. "
                    "record the ruling and concrete follow-up on the queue job, including a dependency or retry date "
                    "for a real external wait. Do not just repeat parked-for-Chief or ask an absent Chief. "
                    f"For an open Chief job, use jobs.py next --id {reviews[0]['id']} --agent {who} --can mini,gemini,any --git to claim that exact job. "
                    "do not reopen unrelated date, credit or Ben-approval holds. Do this one review, then stop. "
                    "Other reviews waiting: " + ", ".join(j["id"] for j in reviews[1:])) if review_work else ""
        if selection and not review_work:
            priority = (f"DISPATCH PRIORITY: claim only {job['id']} with python3 scripts/jobs.py next --id {job['id']} --agent {who} --can mini,gemini,any --git. "
                        "This is the shared deadline-first selection. Do not substitute an inbox, audit or ordinary jobs.py next choice. "
                        "If it is no longer claimable, stop; the relay will replan from the current queue.")
        guest_job = job_chain(job) if job else None
        if guest_job:
            named = NAMES.get(guest_who, guest_who) or "No agent"
            label = channels.name(guest_job)
            if who == guest_who:
                why = (f"{named} is Chief for {label} "
                       "(Grok -> Claude -> Codex -> Gemini). "
                       "A relay line that names someone else on this channel's job means the first agent in its chain is down.")
            else:
                why = (f"{named} is Chief for {label} "
                       "(Grok -> Claude -> Codex -> Gemini). You are its WORKER for this channel's queue job. "
                       "If this line names anyone but Grok Bot, Grok is down. "
                       "In step 3 skip the channel check and the desk inbox: do only the job "
                       "`jobs.py next` gives you. If it exits 10, stop without posting")
        auth_leader = guest_who if guest_job else leader
        prompt = PROMPT.format(name=NAMES.get(who, who), agent=who, why=why,
                               authority=authority_prompt(who, auth_leader, guest_job),
                               priority=priority,
                               role="the elected acting Chief" if who == auth_leader else "a specialist worker",
                               **brief_channels(who))
        log(f"run: {who}{' on ' + model if model else ''}{' for ' + job['id'] if job else ''} (cap {cap}s)")
        push_heartbeat(at, "running", who, f"woke {NAMES.get(who, who)} for {job['id'] if job else 'one job'} (cap {cap // 60} min)")
        seen(who, at)
        started = now()
        if review_work:
            write_json(d("active.json"), {"job": reviews[0]["id"], "title": reviews[0].get("title", ""),
                       "agent": who, "startedAt": iso(started), "expiresAt": iso(started + dt.timedelta(seconds=cap + 60)),
                       "pid": os.getpid(), "kind": "chief-review", "chain": job_chain(reviews[0]),
                       "progress": {"step": 0, "of": 3, "at": iso(started), "note": "Review started"}})
        execution = {"job":reviews[0]["id"] if review_work else job.get("id") if job else "", "worker":who, "model":model,
                     "pid":os.getpid(),"host":"mini","machine_name":platform.node(),
                     "startedAt":iso(started),"expiresAt":iso(started + dt.timedelta(seconds=cap+60)),"version":LOADED_VERSION}
        write_json(d("execution.json"),execution)
        write_json(d("runner.json"),{"pid":os.getpid(),"version":LOADED_VERSION,"desiredVersion":code_version(),"at":iso(started),"state":"working","job":execution["job"]})
        try:
            code, tail = run_cli(who, prompt, cap, model)
        finally:
            d("execution.json").unlink(missing_ok=True)
            if review_work:
                d("active.json").unlink(missing_ok=True)
        said = credit_phrase(code, tail)
        usage = bool(said)
        log_run(at, reviews[0] if review_work else job, who, model, code, usage)
        if review_work and code in (0, 124) and not usage:
            record_chief_attempt(reviews[0], who, now())
            reviewed.add(reviews[0]["id"])
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
        if code not in (0, 124) and CAPACITY_RE.search(tail[-1500:]):
            mins = float(os.environ.get("CHIEF_CAPACITY_MIN", "15"))
            until = now() + dt.timedelta(minutes=mins)
            if bad_model:
                mark_model_down(bad_model, f"{NAMES.get(who, who)} on {routing.cli_model(bad_model)}: provider at capacity",
                                until, now())
                routing.OUT.add(bad_model)
                log(f"{who} on {bad_model}: provider at capacity; model flagged {mins:g} min, {who} stays up")
            else:  # its default model (Codex's is Sol too): a short pause, not the hour a real failure gets
                mark_down(who, "provider at capacity for its default model", until, now())
                log(f"{who}: provider at capacity on its default model; down {mins:g} min")
            if job:
                walk_on(job, who, bad_model, now())
            at = now()
            continue
        if code not in (0, 124):
            outcome = recorded_task_outcome(job, who, started)
            if outcome:
                log(f"chain: {job['id']} recorded {outcome}; exit {code} is task-local, not an agent outage")
                attempted.add(job["id"])
                chained += 1
                if chained >= chain_max:
                    return 0
                at = now()
                continue
            notify(f"Chief relay: {NAMES.get(who, who)}'s run failed (exit {code}). Log: ~/Library/Logs/chief-relay.log")
            # Don't wake it again every minute into the same failure (Gemini exit 2, 13-14 Oct: 88 posts in 20 h).
            # An addressed job waits the usual retry; a plain worker run waits CHIEF_FAIL_RETRY_H, so others take the queue.
            fail_h = retry_h if addressed else float(os.environ.get("CHIEF_FAIL_RETRY_H", "1"))
            mark_down(who, f"its {'run for an addressed job' if addressed else 'last run'} failed (exit {code})",
                      now() + dt.timedelta(hours=fail_h), now())
            if job:
                walk_on(job, who, model, now(), reason=f"run failed (exit {code})")
            if who == leader:
                at = now()  # a failed elected Chief yields to the next available Chief in this run
                continue
            at = now()
            continue  # a failed specialist must not strand work for healthy workers
        chained += 1
        last_ran = job.get("id") if job else None
        if job:
            current = read_json(STUDIO / "jobs" / "queue.json") or {}
            row = next((j for j in current.get("jobs", []) if j.get("id") == job["id"]), None)
            # Never abandon an unfinished claim. Its owner must resume or park
            # it; released/done/blocked tasks may yield to other work immediately.
            if row and row.get("status") != "claimed":
                attempted.add(job["id"])
        if chained >= chain_max or (not job and not review_work):
            return 0
        log(f"chain: {reviews[0]['id'] if review_work else last_ran} ended; checking remaining Chief duties and ready jobs ({chained}/{chain_max})")
        at = at + (now() - started)  # the run's own clock moved on by the job's length


def walk_on(job: dict, who: str, model: str, at: dt.datetime, reason="out of usage") -> None:
    """`who` ran out of usage on `job`: if the job is still open or held by `who`, hand it to the next worker up in its
    chain (so it isn't left claimed by a worker that can't finish it). If nobody further down is up, it waits."""
    data = read_json(STUDIO / "jobs" / "queue.json") or {}
    cur = next((j for j in data.get("jobs", []) if j.get("id") == job.get("id")), None)
    if not cur or not (cur.get("status") == "open" or (cur.get("status") == "claimed" and cur.get("by") == who)):
        return
    capabilities = worker_capabilities()
    eligible = {a for a in workers_up(at) if not workflow.capability_problem(cur,a,at,capabilities)}
    lane = routing.next_lane(cur, who, eligible, model)
    if not lane:
        log(f"chain: {cur['id']} waits: nobody after {who} in its chain is up")
        return
    if reroute(cur, lane[0], lane_model(lane), f"{NAMES.get(who, who)} {reason}; next in its chain: {lane[0]}"):
        log(f"chain: {cur['id']} rerouted from {who} to {lane[0]} on {lane[1]}")


def cmd_status(at: dt.datetime) -> int:
    flags = load_out(at)
    rows, who = acting(at)
    for a, up, why in rows:
        print(f"{'>' if a == who else ' '} {a:<7} {NAMES.get(a, a):<9} {'UP  ' if up else 'down'}  {why}")
    print(f"Chief: {NAMES.get(who, who) if who else 'nobody'}")
    guests = _other_slugs()
    if len(guests) == 1:
        grows, gwho = acting(at, guests[0])
        print(f"{channels.name(guests[0])} Chief: {NAMES.get(gwho, gwho) if gwho else 'nobody'} "
              "(Grok -> Claude -> Codex -> Gemini)")
        for a, up, why in grows:
            mark = ">" if a == gwho else " "
            print(f"  {mark} {a:<7} {NAMES.get(a, a):<9} {'UP  ' if up else 'down'}  {why}")
    runner = read_json(d("runner.json")) or {}
    print(f"Runner: {runner.get('version', 'not reported')} / installed {code_version()} ({runner.get('state', 'unknown')})")
    duties = pending_chief_reviews(at)
    print("Chief duties (deadline, urgency, age): " + (", ".join(j["id"] for j in duties) or "none"))
    for worker in routing.MINI_WORKERS:
        if worker not in [a for a, _, _ in rows]:
            up, why = state_of(worker, at)
            print(f"  {worker:<7} {NAMES[worker]:<9} {'UP  ' if up else 'down'}  {why} (specialist worker)")
    out, why = claude_out(at, read_json(STUDIO / "jobs" / "queue.json") or {})
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
    """Gemini is both the facts checker and the last Chief fallback. Show CLI presence and queued fact work."""
    b = find_bin("AGY_BIN", "agy")
    try:
        q = json.loads((STUDIO / "jobs" / "queue.json").read_text())["jobs"]
        waiting = sum(1 for j in q if j.get("needs") == "gemini" and j.get("status") in ("open", "claimed"))
        jobs = f"{waiting} gemini job{'s' if waiting != 1 else ''} waiting"
    except (OSError, ValueError, KeyError):
        jobs = "queue not found"
    return (f"Checker: Gemini ({'agy found' if b else 'agy NOT found on PATH'}); Chief fallback and facts checker; {jobs}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("run")
    cp = sub.add_parser("capabilities", help="record a fresh, actually demonstrated worker tool capability")
    cp.add_argument("--agent", required=True)
    cp.add_argument("--available", default="", help="comma-separated demonstrated capabilities; empty means none")
    cp.add_argument("--evidence", required=True, help="actual probe/result reference, never a model-name assumption")
    cp.add_argument("--minutes", type=int, default=30)
    rp = sub.add_parser("review-progress")
    rp.add_argument("--agent", required=True)
    rp.add_argument("--job", required=True)
    rp.add_argument("--step", required=True, type=int)
    rp.add_argument("--note", required=True)
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
    if a.cmd == "capabilities":
        record_capabilities(a.agent, a.available, a.evidence, a.minutes, at)
        return 0
    if a.cmd == "review-progress":
        review_progress(a.agent, a.job, a.step, a.note, at)
        return 0
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
