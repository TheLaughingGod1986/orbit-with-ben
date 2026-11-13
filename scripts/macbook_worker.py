#!/usr/bin/env python3
"""MacBook worker lane: the MacBook Pro takes queued `needs macbook` jobs when Ben isn't using it
(Ben, 28 Oct 2026: "yes" to a MacBook worker lane over Tailscale with power and idle guards).

launchd runs this every 3 minutes (scripts/macbook/com.owb.macbook-worker.plist, installed by
scripts/macbook/setup_macbook.sh; 180 s from 6 Nov 2026 so a free MacBook notices waiting work quickly).
Each run keeps taking jobs back to back for up to MACBOOK_LOOP_MIN (13) minutes
(Ben, 5 Nov 2026), and takes each one only when ALL of these hold:
  - it is inside its hours: round the clock by default (Ben, 28 Oct 2026: "let's use the MacBook Pro 24 seven");
    MACBOOK_HOURS=night limits it to weeknights 21:00-09:00 and all weekend, London (the run must also end by 09:00);
  - no pause file (~/_desk/state/macbook-worker.pause), and no other run of this script in progress;
  - the MacBook is on mains power (never drains the battery);
  - nobody has touched the keyboard or trackpad for MACBOOK_IDLE_MIN minutes (default 10) for slot 2; slot 1 also
    runs while Ben is using the Mac, at background priority (Ben, 9 Nov 2026; MACBOOK_BUSY_OK=0 turns that off);
  - at least MACBOOK_MIN_FREE_GB free on the disk (default 15).
Then it pulls both checkouts, claims the oldest `macbook` job with
  jobs.py next --agent macbook --can macbook --git
and wakes an agent CLI on it under `caffeinate -i`: the first lane in the job's routing chain whose CLI is installed
here (Codex, Gemini `agy`, Claude Code, Cursor `agent`; Ben, 4 Nov 2026: "get all the agents working on the MacBook
Pro"; MACBOOK_AGENTS limits the set, MACBOOK_AGENT pins one), which keeps the Mac awake for
that one run only (nothing global changes; sleep settings are untouched). The run is killed at MACBOOK_CAP_S seconds
(default 1500); a job still claimed afterwards is released with a note so the next run (or another worker) picks
it up, unless the run ended cleanly and pushed its work branch: that job is parked for the Chief, so nobody starts
the same work again. After a Codex run it records the Codex usage limits (pool codex: the same account as the Mini)
for the board.

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
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import time
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import channels  # noqa: E402  which channels there are, their repos, names and Studio ports

HOME = pathlib.Path.home()
WORKER_DIR = HOME / "_desk" / "worker"  # the clones setup_macbook.sh made for the worker itself
# Two jobs at once on the MacBook Pro (Ben, 5 Nov 2026: "could that maybe handle two tasks in parallel ... two on the
# MacBook Pro and one on the Mac Mini"). launchd starts slot 1; slot 1 starts the other slots (MACBOOK_SLOTS, default
# 2) as their own processes. Each slot has its own clones, lock, agent id (macbook, macbook-2) and heartbeat branch,
# so the two never share a checkout or a claim.
SLOT = max(1, int(os.environ.get("MACBOOK_SLOT", "1") or 1))
SLOTS = max(1, int(os.environ.get("MACBOOK_SLOTS", "2") or 1))


def _repo_name(url: str) -> str:
    return str(url or "").rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")


def clone_name(slug: str) -> str:
    """The folder name of the worker's own clone of a channel's repo: the repo's name on GitHub. A channel whose
    file gives no URL yet gets its slug, and is never cloned from here."""
    return _repo_name(channels.get(slug)["repo"].get("url")) or channels.get(slug)["slug"]


def other_slugs() -> list[str]:
    """Every channel but the one whose repo carries the studio, in the registry's order."""
    return [s for s in channels.slugs() if s != channels.studio_slug()]


def own_checkout(env: str, name: str) -> pathlib.Path:
    """The worker's own clone, never one of Ben's folders (5 Nov 2026: a HOS job left Ben's own History of Science
    folder on 'macbook/J2170' and the worker stopped). An env path is used only if it is inside WORKER_DIR."""
    given = os.environ.get(env)
    if given:
        p = pathlib.Path(given)
        try:
            if p.resolve().is_relative_to(WORKER_DIR.resolve()):
                return p
        except (OSError, ValueError):
            pass
    return slot_dir(SLOT) / name


def slot_dir(n: int) -> pathlib.Path:
    return WORKER_DIR if n == 1 else WORKER_DIR / f"slot{n}"


def slot_name(n: int, base: str) -> str:
    return base if n == 1 else f"{base}-{n}"


def channel_clone(slug: str) -> pathlib.Path:
    return own_checkout(channels.get(slug)["repo"].get("env") or "", clone_name(slug))


def studio_clone() -> pathlib.Path:
    """The worker's own clone of the repo that carries the studio: a channel's repo while one does, the studio's own
    once it has one. The loader says which (`channels.studio_repo()`); the folder is named after the repo."""
    repo = channels.studio_repo()
    return own_checkout(repo.get("env") or "", _repo_name(repo.get("url")) or channels.studio_key())


# The clone that carries the studio (the queue, these scripts), and the clone of every other channel. Which repos
# those are comes from the channel files; nothing here names one.
STUDIO = studio_clone()
OTHERS = [channel_clone(s) for s in other_slugs()]
URLS = {clone_name(s): channels.get(s)["repo"]["url"] for s in channels.slugs() if channels.get(s)["repo"].get("url")}
if channels.studio_repo().get("url"):    # the studio's own repo, once it is not also a channel's
    URLS.setdefault(_repo_name(channels.studio_repo()["url"]), channels.studio_repo()["url"])
STATE = HOME / "_desk" / "state"
AGENT_ID = slot_name(SLOT, "macbook")
HEARTBEAT_REF = slot_name(SLOT, "macbook-heartbeat")

PROMPT = """You are the MacBook worker for Ben's YouTube studio, running unattended on Ben's MacBook Pro while he is
away from it. Your agent id is `{agent}` everywhere (jobs.py --agent {agent}). Do ONE job, then stop.
Another MacBook slot may be working on a different job at the same time, in its own checkouts: stay in yours.

The job is already claimed for you: {job}
1. {studio_name} ({studio}) is pulled. Read {studio_rules} (the rules, the Never list, "Stop and ask Ben") and then
     python3 scripts/jobs.py show {job}
{other_checkouts}
2. Do the job exactly as its brief says. Report progress as you go:
     python3 scripts/jobs.py progress {job} --agent {agent} --step <k> --of <n> --action "<what is left>" --git
3. Commit your work on a branch named macbook/<job id>, push it (git push -u origin <branch>), and open a PR to main
   with gh; say the PR number in the result. Never merge, approve or close a PR, and never push to main: merges are
   the Chief's (AGENTS.md), so a brief that says "merge" stops at the open PR and says so. Then switch every checkout you touched back to main
   (git checkout main): a checkout left on a branch stops the MacBook taking any further job, and Ben's own
   {bens_folders} must always be left on main.
4. Finish with  jobs.py done {job} --agent {agent} --result "..." --git  (or block / release with a reason).
5. Report on the studio thread: write the report to a file, starting "[MacBook] ...", and post it with
   python3 scripts/studio_thread.py post -f <file>   Never put the report text on the command line: the shell runs
   any backtick or $(...) in it as a command and posts the output.

This is Ben's own laptop, not the Mini:
- never spend money or credit beyond the written rules, never sign in to anything, never print secrets;
- never upload a video, change a video's privacy or schedule, or delete a video; never delete anything on the NAS;
- change something on YouTube only when this job is a YouTube Studio job the Chief routed to this Mac (Ben, 9 Nov
  2026: he signed both channels into Studio here for these). Then do exactly what the brief names, in the Studio
  window on CDP port {studio_ports}, check the channel name first, and touch
  nothing else on YouTube;
- the local model at http://127.0.0.1:11434 (Ollama, model {model}) is for low-stakes text only: metadata drafts,
  caption cleanup, gate summaries. Never scripts, facts or anything spoken;
{file_rule}
- leave nothing running when you stop.
Your run is killed at {cap_min} minutes: if the job will take longer, stop at a clean point, release it with a note,
and stop.
"""


def film_store() -> pathlib.Path | None:
    """The shared working-film store on the NAS, when this Mac has it mounted.

    AGENTS.md "Film folders on the NAS" (Ben, 7 Nov 2026): both machines read and write a film's folder there. Until
    11 Nov the brief said "keep files inside the checkouts and ~/_desk", so a run was refused the copy of a source
    image into its own film's folder (J2452) and a finished film had no allowed way off this Mac (J2568)."""
    import jobs
    try:
        return jobs.STUDIO_LIVE_ROOT if jobs.STUDIO_LIVE_ROOT.is_dir() else None
    except OSError:
        return None


def file_rule(count: str, store: pathlib.Path | None) -> str:
    """Where this run may put files. The NAS rules ride along, because the store is the only copy of a lot of work."""
    if not store:
        return (f"- keep files inside the {count} checkouts and ~/_desk. The shared working-film store on the NAS is not\n"
                "  mounted on this Mac right now, so do not try to reach it: keep finished files in ~/_desk and put each\n"
                "  one's SHA-256 in your report;")
    return (f"- keep files inside the {count} checkouts, ~/_desk and the shared working-film store on the NAS\n"
            f"  ({store}; AGENTS.md \"Film folders on the NAS\": both machines read and write a film's folder there).\n"
            "  On the NAS you add to a film's own folder and nothing else: never delete or move a file that is already\n"
            "  there, never replace a finished media file (a new version gets a new name), never write outside that\n"
            "  store (the archive beside it is not yours), and check each copy with SHA-256. More than a handful of\n"
            "  files waits for the 01:00-06:00 window, unless it is a finished master's copy;")


def prompt_channels() -> dict:
    """The parts of the brief that depend on which channels there are: built from the channel files, so the brief
    reads the same for the channels of today and needs no edit for the next one."""
    others = list(zip(other_slugs(), OTHERS))
    names = [channels.name(s) for s, _ in others]
    ports = [(channels.studio_port(s), channels.name(s)) for s in channels.slugs() if channels.studio_port(s)]
    count = 1 + len(others)
    return {
        "studio_name": channels.studio_name(),
        "studio": STUDIO,
        "other_checkouts": "\n".join(
            f"   For a {channels.label(s)} job, work in the {channels.label(s)} checkout ({path}) and follow its "
            f"{channels.rules_phrase(path)}."
            for s, path in others),
        "studio_rules": channels.rules_phrase(STUDIO),
        "bens_folders": " and ".join(names) + (" folder" if len(names) < 2 else " folders"),
        "studio_ports": " or ".join(f"{port} ({name})" for port, name in ports),
        "checkout_count": {1: "one", 2: "two", 3: "three", 4: "four"}.get(count, str(count)),
        "file_rule": file_rule({1: "one", 2: "two", 3: "three", 4: "four"}.get(count, str(count)), film_store()),
    }


def brief(job: str, model: str, cap_min: int) -> str:
    """The brief the agent CLI gets for one claimed job."""
    return PROMPT.format(job=job, agent=AGENT_ID, model=model, cap_min=cap_min, **prompt_channels())


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


def guards(pmset_out=None, ioreg_out=None, free_gb=None, now=None, load=None) -> list[str]:
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
    # Ben, 9 Nov 2026: "I want the MacBook Pro to be picking up as many jobs as the Mac Mini". On mains, slot 1 also works
    # while he is using the Mac, at background priority (taskpolicy -b, see busy_cmd); slot 2 still waits for idle.
    # MACBOOK_BUSY_OK=0 brings back the old rule (no job at all while he is at the keys).
    busy_ok = SLOT == 1 and os.environ.get("MACBOOK_BUSY_OK", "1") != "0"
    if idle < need and not busy_ok:
        why.append(f"in use ({idle:.0f} min idle, needs {need:.0f})")
    free = free_gb if free_gb is not None else shutil.disk_usage(str(HOME)).free / 1024 ** 3
    floor = float(os.environ.get("MACBOOK_MIN_FREE_GB", "15"))
    if free < floor:
        why.append(f"disk low ({free:.0f} GB free, needs {floor:.0f})")
    if SLOT > 1:
        # A second job only while the machine has room: the first slot's job always comes first.
        load, cpus = os.getloadavg()[0] if load is None else load, os.cpu_count() or 8
        if load > cpus * float(os.environ.get("MACBOOK_SLOT_LOAD", "0.6")):
            why.append(f"busy (load {load:.1f} on {cpus} cores): slot {SLOT} waits")
    return why


AGENTS = ("codex", "gemini", "claude", "cursor")  # Ben, 4 Nov 2026: "get all the agents working on the MacBook Pro"
BINS = {"codex": ("CODEX_BIN", "codex"), "gemini": ("AGY_BIN", "agy"), "claude": ("CLAUDE_BIN", "claude"),
        "cursor": ("CURSOR_AGENT_BIN", "agent")}


def find_bin(agent: str):
    """launchd's PATH misses npm-global and ~/.local: look in the usual install places too (as chief_relay.find_bin)."""
    env, name = BINS[agent]
    import routing
    return routing.find_cli(env, name, HOME)


def installed(names=None) -> list:
    """The agent CLIs this MacBook runs, in MACBOOK_AGENTS order (default all four), that are actually installed."""
    want = [a.strip() for a in (names or os.environ.get("MACBOOK_AGENTS", ",".join(AGENTS))).split(",") if a.strip()]
    return [a for a in want if a in BINS and find_bin(a)]


DOWN = STATE / "macbook-agent-down.json"


def down_agents(now: dt.datetime | None = None) -> dict:
    """{agent: until} for agent CLIs whose last run here failed, while the pause lasts (MACBOOK_FAIL_H, default 2 h)."""
    now = now or dt.datetime.now(dt.timezone.utc)
    try:
        marks = json.loads(DOWN.read_text())
    except (OSError, ValueError):
        return {}
    out = {}
    for a, until in (marks or {}).items():
        try:
            if dt.datetime.fromisoformat(str(until).replace("Z", "+00:00")) > now:
                out[a] = until
        except ValueError:
            pass
    return out


def mark_down(agent: str, now: dt.datetime | None = None) -> str:
    """A failed run pauses that CLI here, so the job's next run goes to the next lane in its chain instead of
    failing the same way every 15 minutes."""
    now = now or dt.datetime.now(dt.timezone.utc)
    until = (now + dt.timedelta(hours=float(os.environ.get("MACBOOK_FAIL_H", "2")))).strftime("%Y-%m-%dT%H:%M:%SZ")
    marks = down_agents(now)
    marks[agent] = until
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        DOWN.write_text(json.dumps(marks) + "\n")
    except OSError:
        pass
    return until


def failed_run(code: int, seconds: float, still_open: bool) -> bool:
    """Pause the CLI after this run? A non-zero exit (not the 124 cap), or a clean exit inside 2 minutes that left
    its job open: an agent out of usage prints a notice and exits 0 (9 Nov 2026: claude claimed and released J2421
    every minute for an hour)."""
    if code not in (0, 124):
        return True
    return code == 0 and still_open and seconds < float(os.environ.get("MACBOOK_QUICK_EXIT_S", "120"))


def usable(have: list, now: dt.datetime | None = None) -> list:
    down = down_agents(now)
    return [a for a in have if a not in down]


# Agents that can drive the signed-in Studio windows here with nobody at the keys, best first. Claude Code is not one:
# its unattended allowlist (CLAUDE_ALLOWED_TOOLS) covers tests and PRs only, so it cannot reach the browser, and on
# 10 Nov 2026 it handed J2460 and J2461 straight back. The free Codex model goes last: it failed J0135 on 9 Nov.
STUDIO_AGENTS = ("gemini", "cursor", "codex")


def studio_agents(have: list) -> list:
    return [a for a in STUDIO_AGENTS if a in have]


def is_studio_job(job: dict) -> bool:
    """A job done in the Studio browser here: any `kind: studio` job, or a `needs mini` job this MacBook was offered
    as Studio-only (jobs.macbook_studio_ok)."""
    if job.get("kind") == "studio":
        return True
    if job.get("needs") != "mini":
        return False
    try:
        import jobs
        return jobs.macbook_studio_ok(job, f"{job.get('title') or ''} {job.get('body') or ''}")
    except Exception:  # noqa: BLE001
        return job.get("kind") == "studio"


def pick_agent(job: dict, have: list) -> tuple:
    """(agent, model) for this job on this MacBook: the first lane in the job's routing chain (scripts/routing.py,
    AGENTS.md "Who does what") whose CLI is installed here and has credit; else the first installed CLI with its
    default model; ("", "") when nothing is installed. MACBOOK_AGENT pins one agent (the old single-agent setting)."""
    import routing
    pin = os.environ.get("MACBOOK_AGENT", "")
    if pin:
        return (pin, routing.model_for(job, pin)) if pin in have else ("", "")
    if is_studio_job(job):
        can = studio_agents(have)
        return (can[0], routing.model_for(job, can[0])) if can else ("", "")
    # A job addressed to one agent (a Mini job the MacBook took over) runs that agent's CLI. `claudecode` is the Mini's
    # Claude Code worker (9 Nov 2026): here it is the MacBook's own Claude Code.
    addressed = {"claudecode": "claude"}.get(job.get("for") or "", job.get("for"))
    if addressed in have:
        return addressed, routing.model_for(job, addressed)
    for a, m in routing.job_chain(job):
        if a == "claudecode":  # the Mini's Claude Code lane = this MacBook's Claude Code
            a, m = "claude", ("claude-opus-5-5" if m == "mini-claude-opus-5-5" else m)
        if a in have and routing.lane_ok(a, m):
            return a, (m if routing.RUNS_ON.get(m) == a else "")
    return (have[0], "") if have else ("", "")


# Commands an unattended Claude run may use without a prompt (Ben, 9 Nov 2026: "Yes please"). J2427 was released about 40
# times on 9 Nov because `python3 -m unittest` and `gh pr create` asked for approval with nobody there. Tests, the repo's
# own checks and opening a PR only; merges stay with the Chief (no `gh pr merge` here).
# `git fetch` was added on 10 Nov 2026 (Ben: "Yes, do a git fetch"): J2495 came straight back because the run could not
# fetch the pull-request heads it had to read. Fetch only reads from GitHub; it changes no branch and no file.
CLAUDE_ALLOWED_TOOLS = (
    "Bash(git fetch:*)",
    "Bash(python3 -m unittest:*)",
    "Bash(python3 scripts/test_kanban_snapshot.py:*)",
    "Bash(node scripts/test_studio_app.cjs:*)",
    "Bash(python3 scripts/core_sync.py check:*)",
    "Bash(python3 scripts/sync_rules.py:*)",
    "Bash(git push:*)",
    "Bash(gh pr create:*)",
    "Bash(gh pr view:*)",
    "Bash(gh pr checks:*)",
    "Bash(gh pr list:*)",
)


# Refused outright, whatever a brief says: no run waits for an approval that cannot come, and none can be talked into
# it (J2600, from the draft #666 of 9 Nov 2026). Merging, approving and closing a PR are the Chief's, main is pushed to
# only by the queue's own Python (`jobs.py ... --git`, which is not a shell `git push`), and a forced push rewrites
# what a reviewer has already read. These match by how the command starts, so they stop the usual forms; the brief's
# own line is what forbids the rest.
CLAUDE_DENIED_TOOLS = (
    "Bash(gh pr merge:*)",
    "Bash(gh pr review:*)",
    "Bash(gh pr close:*)",
    "Bash(gh pr ready:*)",
    "Bash(gh api:*)",
    "Bash(git push origin main:*)",
    "Bash(git push -u origin main:*)",
    "Bash(git push --force:*)",
    "Bash(git push -f:*)",
    "Bash(git push --force-with-lease:*)",
)


def agent_cmd(agent: str, prompt: str, model: str = "") -> list | None:
    """The agent CLI's one-shot form, as the Mini runs it (scripts/chief_relay.py cli_spec)."""
    b = find_bin(agent) if agent in BINS else None
    if not b:
        return None
    dirs = [x for path in OTHERS for x in ("--add-dir", str(path))] + ["--add-dir", str(HOME / "_desk")]
    store = film_store()
    if store:  # the brief allows it, so the agent's own sandbox has to as well
        dirs += ["--add-dir", str(store)]
    if agent == "codex":
        m = ["-m", model] if model.startswith("gpt-") else []
        return [b, "exec", *m, "--approve-for-me", "-c", "sandbox_workspace_write.network_access=true", *dirs, prompt]
    if agent == "claude":
        # The prompt goes straight after -p: --add-dir takes a list, so a prompt after it was read as one more folder
        # ("Input must be provided ... when using --print", 5 Nov 2026: every MacBook job given to Claude failed).
        return [b, "-p", prompt, "--permission-mode", "acceptEdits", "--allowedTools", ",".join(CLAUDE_ALLOWED_TOOLS),
                "--disallowedTools", ",".join(CLAUDE_DENIED_TOOLS), *dirs]
    import routing
    cm = routing.cli_model(model) if model and routing.RUNS_ON.get(model) == agent else ""
    if agent == "gemini":  # Antigravity agy: -p must come last, straight before the prompt (chief_relay note, 14 Oct)
        return [b, "--dangerously-skip-permissions", *dirs, *(["--model", cm] if cm else []), "-p", prompt]
    if agent == "cursor":
        return [b, "-p", "--force", *(["--model", cm] if cm else []), prompt]
    return None


def job_record(job_id: str) -> dict:
    try:
        return next((j for j in json.loads((STUDIO / "jobs" / "queue.json").read_text()).get("jobs", [])
                     if j.get("id") == job_id), {})
    except (OSError, ValueError):
        return {}


def busy_cmd(cmd: list, idle_min: float | None = None) -> list:
    """While Ben is using the Mac, run the job at macOS background priority (taskpolicy -b: lowest CPU, disk and
    network priority), so his apps always come first. Idle: unchanged."""
    need = float(os.environ.get("MACBOOK_IDLE_MIN", "10"))
    idle = idle_minutes() if idle_min is None else idle_min
    if idle < need and shutil.which("taskpolicy"):
        return ["taskpolicy", "-b", *cmd]
    return cmd


def run_capped(cmd: list, cwd, cap_s: int) -> int:
    """Run in its own process group and kill the whole group at the cap, so no agent or render outlives the run."""
    import signal
    p = subprocess.Popen(cmd, cwd=cwd, start_new_session=True)
    try:
        code = p.wait(timeout=cap_s)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGTERM)
        try:
            p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
        code = 124
    return code


def claimed_job(out: str) -> str:
    m = re.search(r"^(J\d{4,})\b", out, re.M)
    return m.group(1) if m else ""


def still_mine(job: str) -> bool:
    r = sh([sys.executable, "scripts/jobs.py", "show", job], cwd=STUDIO)
    first = (r.stdout.splitlines() or [""])[0]
    return "claimed" in first and AGENT_ID in first


def work_branch(job: str) -> str:
    """The branch the brief tells every run to push its work on."""
    return f"macbook/{job}"


def branch_heads(job: str) -> dict:
    """What GitHub holds on this job's work branch, per clone: {clone: commit}. Read before and after a run, so a
    branch this run pushed is told apart from one an earlier run left there (a long job keeps one across many runs).
    A clone that cannot be asked is left out, which reads as "nothing pushed"."""
    heads = {}
    for repo in (STUDIO, *OTHERS):
        if not (repo / ".git").exists():
            continue
        r = sh(["git", "-C", str(repo), "ls-remote", "--heads", "origin", work_branch(job)], timeout=60)
        sha = (r.stdout.split() or [""])[0] if r.returncode == 0 else ""
        if sha:
            heads[repo] = sha
    return heads


def open_pr(repo: pathlib.Path, branch: str) -> str:
    """The open pull request for `branch`, as its address; '' when gh is missing, fails or finds none."""
    if not shutil.which("gh"):
        return ""
    r = sh(["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "url", "--limit", "1"], cwd=repo, timeout=60)
    try:
        return str(json.loads(r.stdout or "[]")[0].get("url") or "") if r.returncode == 0 else ""
    except (ValueError, LookupError, AttributeError, TypeError):
        return ""


def pushed_work(job: str, before: dict) -> dict:
    """The work this run pushed and nobody has merged: {'repo', 'branch', 'ahead', 'pr'}, or {} for none. It counts
    only when the branch's head on GitHub moved during the run and is ahead of main there."""
    branch = work_branch(job)
    for repo, sha in branch_heads(job).items():
        if before.get(repo) == sha:
            continue
        git = ["git", "-C", str(repo)]
        r = sh(git + ["fetch", "-q", "origin", MAIN_REF, f"+refs/heads/{branch}:refs/remotes/origin/{branch}"], timeout=180)
        if r.returncode == 0:
            r = sh(git + ["rev-list", "--count", f"refs/remotes/origin/main..{sha}"])
        count = r.stdout.strip() if r.returncode == 0 else ""
        if count.isdigit() and int(count):
            return {"repo": repo.name, "branch": branch, "ahead": int(count), "pr": open_pr(repo, branch)}
    return {}


def park_reason(agent: str, pushed: dict) -> str:
    """What the Chief reads on a job parked by park(). It starts "parked for Chief", which is what puts the job on
    the Chief's review list; it carries no timed wait, because a wait would take it off that list until it fell due."""
    return (f"parked for Chief: the MacBook run on {agent} ended (exit 0) with its work pushed and the job still open. "
            f"Branch {pushed['branch']} in {pushed['repo']} is {pushed['ahead']} commit(s) ahead of main; "
            + (f"pull request {pushed['pr']}" if pushed.get("pr") else "no open pull request was found for it")
            + ". Review and merge it and close the job, or reopen the job with a note.")


def park(job: str, agent: str, pushed: dict) -> bool:
    """Park a job whose run pushed its branch and stopped without closing it (11 Nov 2026: the run opened its pull
    request and ended with the job open; it was handed back, and two minutes later the other slot began the same work
    again and opened a second pull request). The brief already tells the agent to park; this is the net under it."""
    r = sh([sys.executable, "scripts/jobs.py", "block", job, "--agent", AGENT_ID, "--reason", park_reason(agent, pushed),
            "--git"], cwd=STUDIO)
    return r.returncode == 0


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
    # Same ChatGPT account as the Mini (Ben's personal account, one shared weekly limit): one pool, read from either machine.
    # --strict: this caller asked for one pool, so an unread one must not look like a recorded one (J2564).
    r = sh([sys.executable, "scripts/ai_spend_daily.py", "--pools", "codex", "--codex-pool", "codex",
            "--by", AGENT_ID, "--git", "--strict"], cwd=STUDIO, timeout=180)
    log(f"usage reading: {(r.stdout or r.stderr).strip()[-200:]}")
    if r.returncode == 0:
        stamp.write_text(str(now.timestamp()))
    return r.returncode == 0


def machine_mark() -> str:
    """Twelve hex characters that tell this machine from another without naming it. The heartbeat is on a public
    branch, and a device's network name never goes into a tracked file (AGENTS.md "Never"). Until 11 Nov 2026 the
    heartbeat carried the name itself."""
    return hashlib.sha256(platform.node().encode()).hexdigest()[:12]


def host_observation():
    """Measured host identity/resources; no implied auth, quota or media capability.

    A generic `host=macbook` is retained for old board readers. The machine's mark
    must be matched against an independently approved registration before use.
    Missing memory/capability evidence deliberately cannot unlock another lane.
    """
    return {"machine": machine_mark(), "architecture": platform.machine(),
            "on_ac": on_ac_power(), "idle_minutes": idle_minutes(),
            "free_gb": shutil.disk_usage(str(HOME)).free / 1024**3,
            "load": os.getloadavg()[0], "cpu_count": os.cpu_count(),
            "registered_id": None, "memory_available_gb": None,
            "auth_quota_ready": None, "media_capabilities": []}


def heartbeat_doc(state: str, why: list, job: str = "", now: dt.datetime | None = None) -> dict:
    now = now or dt.datetime.now(dt.timezone.utc)
    return {"at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "host": "macbook", "slot": SLOT, "agent": AGENT_ID,
            "state": state, "why": why, "job": job,
            "observation": host_observation(),
            "agents": installed(), "paused": down_agents(now)}


def push_heartbeat(state: str, why: list, job: str = "") -> None:
    """One parentless commit holding heartbeat.json, force-pushed to refs/heads/macbook-heartbeat, every run (as the
    Mini's relay does on mini-heartbeat). Ben, 28 Oct 2026, after five hours with no MacBook job and no way to see
    why: the hub's Agents tab reads it ("waiting: on battery", "working on J1122"). Never raises."""
    body = json.dumps(heartbeat_doc(state, why, job)) + "\n"
    git = ["git", "-C", str(STUDIO)]
    try:
        blob = subprocess.run(git + ["hash-object", "-w", "--stdin"], input=body, capture_output=True, text=True,
                              timeout=30, check=True).stdout.strip()
        tree = subprocess.run(git + ["mktree"], input=f"100644 blob {blob}\theartbeat.json\n", capture_output=True,
                              text=True, timeout=30, check=True).stdout.strip()
        commit = subprocess.run(git + ["commit-tree", tree, "-m", f"macbook heartbeat {state}"], capture_output=True,
                                text=True, timeout=30, check=True).stdout.strip()
        subprocess.run(git + ["push", "-q", "-f", "origin", f"{commit}:refs/heads/{HEARTBEAT_REF}"],
                       capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        log(f"heartbeat not pushed: {e}")


MAIN_REF = "+refs/heads/main:refs/remotes/origin/main"


def ff_main(repo: pathlib.Path, own: bool = True) -> subprocess.CompletedProcess:
    """Bring `repo`'s main up to GitHub's, fast-forward only. In the worker's own clone this names the exact ref both
    ways (fetch refs/heads/main into refs/remotes/origin/main, then merge that), so nothing depends on the clone's
    branch or remote settings: on 8 and 10 Nov 2026 slot 2's `git pull origin main` died with "Cannot fast-forward to
    multiple branches". One of Ben's own checkouts keeps the plain pull."""
    git = ["git", "-C", str(repo)]
    if not own:
        return sh(git + ["pull", "-q", "--ff-only", "origin", "main"], timeout=180)
    r = sh(git + ["fetch", "-q", "origin", MAIN_REF], timeout=180)
    if r.returncode:
        return r
    return sh(git + ["merge", "-q", "--ff-only", "refs/remotes/origin/main"], timeout=120)


def pull_main() -> str:
    """Pull both checkouts; '' when fine, else why not. Runs before the guards so fixes reach a MacBook that keeps
    waiting (it used to pull only after the guards passed, so one stuck guard kept it on old code)."""
    for repo in (STUDIO, *OTHERS):
        if not (repo / ".git").exists() and repo.name in URLS:
            # First run after the switch to the worker's own clones: make it (media stays out: LFS is skipped).
            repo.parent.mkdir(parents=True, exist_ok=True)
            env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
            try:
                r = subprocess.run(["git", "clone", "-q", "--depth", "50", URLS[repo.name], str(repo)],
                                   capture_output=True, text=True, timeout=900, env=env)
            except (OSError, subprocess.SubprocessError) as e:
                return f"clone of {repo.name} failed: {e}"
            if r.returncode:
                return f"clone of {repo.name} failed: {(r.stderr or r.stdout).strip()[-200:]}"
            log(f"made the worker's own clone {repo}")
        if (repo / ".git").exists():
            branch = sh(["git", "-C", str(repo), "branch", "--show-current"]).stdout.strip()
            # A job may leave the worker's own clone on its work branch (J1194, 29 Oct 2026: the MacBook then
            # refused every later job). Its own clone goes back to main by itself when clean; Ben's checkouts never.
            own = repo.resolve().is_relative_to(WORKER_DIR.resolve())
            if own:
                # 10 Nov 2026, slot 1: a git killed mid-commit left .git/index.lock in a clone that was only behind
                # GitHub, not ahead of it. The lock was cleared only on the diverged path, so every run failed its
                # pull with "Another git process seems to be running" and the slot sat in error.
                clear_stale_index_lock(repo)
            if own and sh(["git", "-C", str(repo), "status", "--porcelain"]).stdout.strip():
                # Left dirty on a job branch (5 Nov 2026: J2165 left macbook/J2165 dirty and every later run errored),
                # or dirty on main itself (8 Nov 2026: `jobs.py next --git` needs a clean tree, so both slots errored
                # on every claim). Its own clone only: keep the work in a named stash, never discard it.
                stamp = time.strftime("%Y%m%dT%H%MZ", time.gmtime())
                if sh(["git", "-C", str(repo), "stash", "push", "-u", "-q", "-m",
                       f"macbook-worker autostash {branch} {stamp}"]).returncode == 0:
                    log(f"{repo.name}: saved unfinished work on '{branch}' as stash 'macbook-worker autostash {branch} {stamp}'")
            if branch != "main" and own \
                    and not sh(["git", "-C", str(repo), "status", "--porcelain"]).stdout.strip():
                if sh(["git", "-C", str(repo), "checkout", "-q", "main"]).returncode == 0:
                    log(f"{repo.name}: back on main from '{branch}'")
                    branch = "main"
            if branch != "main":
                return f"{repo} is on '{branch or 'detached'}', not main (re-run setup_macbook.sh)"
            # Name origin main: a clone whose branch.main.merge holds more than one entry fails a bare pull with
            # "Cannot fast-forward to multiple branches" (8 Nov 2026, slot 2).
            r = ff_main(repo, own)
            if r.returncode and own and rescue_diverged(repo):
                r = ff_main(repo, own)
            if r.returncode:
                if own and RESCUE_WHY:
                    return f"pull failed in {repo.name}: {RESCUE_WHY}"
                return f"pull failed in {repo.name}: {(r.stderr or r.stdout).strip()[-200:]}"
            if own:
                # A pull can succeed while main is still ahead of GitHub (a queue write whose push lost a race keeps
                # its local commit). Every --git claim then refuses "main has unpublished/diverged commits" (9 Nov
                # 2026, slot 1). Keep those commits on a rescue branch and put main back on origin/main.
                rescue_diverged(repo)
    return ""


STALE_LOCK_S = 600
RESCUE_WHY = ""   # why the last rescue_diverged could not finish; pull_main adds it to the heartbeat's reason


def clear_stale_index_lock(repo: pathlib.Path, now: float | None = None) -> bool:
    """A git killed mid-write (the run cap kills the whole process group) leaves .git/index.lock behind, and every
    later reset, checkout and stash in that clone then fails. In the worker's own clone a lock untouched for
    STALE_LOCK_S is moved aside, never deleted (no git step here holds the index for ten minutes). True when moved."""
    lock = repo / ".git" / "index.lock"
    try:
        if not lock.exists() or (now or time.time()) - lock.stat().st_mtime < STALE_LOCK_S:
            return False
        lock.rename(lock.with_name("index.lock.stale-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())))
    except OSError:
        return False
    log(f"{repo.name}: moved a stale .git/index.lock aside")
    return True


def rescue_diverged(repo: pathlib.Path) -> bool:
    """The worker's own clone has main commits GitHub doesn't (5 Nov 2026 21:36: 'pull failed ... git merge --no-ff',
    and slot 1 stopped). Keep them on a pushed branch macbook-worker/rescue-<time>, then put main back on origin/main.
    Its own clone only (the caller checks); nothing is discarded. True when main was moved.
    10 Nov 2026: slot 2 sat in error for an hour with one unpushed queue write. Each run pushed another rescue branch
    for the same commit and main never moved, and nothing said why. Now a commit already on a rescue branch is not
    branched again, a stale index.lock is moved aside first, and a reset that fails says so (RESCUE_WHY)."""
    global RESCUE_WHY
    RESCUE_WHY = ""
    git = ["git", "-C", str(repo)]
    if sh(git + ["fetch", "-q", "origin", MAIN_REF], timeout=180).returncode:   # the exact ref: origin/main is never stale
        RESCUE_WHY = "could not fetch origin main"
        return False
    ahead = sh(git + ["rev-list", "--count", "origin/main..main"]).stdout.strip()
    if not ahead or ahead == "0":
        return False
    stamp = time.strftime("%Y%m%dT%H%MZ", time.gmtime())
    clear_stale_index_lock(repo)
    if sh(git + ["status", "--porcelain"]).stdout.strip():
        sh(git + ["stash", "push", "-u", "-q", "-m", f"macbook-worker autostash main {stamp}"])
    kept = sh(git + ["branch", "--list", "macbook-worker/rescue-*", "--contains", "main",
                     "--format", "%(refname:short)"]).stdout.split()
    branch = kept[0] if kept else f"macbook-worker/rescue-{stamp}"
    if not kept:
        if sh(git + ["branch", branch, "main"]).returncode:
            RESCUE_WHY = f"could not make branch {branch}"
            return False
        sh(git + ["push", "-q", "origin", branch], timeout=120)
    r = sh(git + ["reset", "-q", "--hard", "origin/main"])
    if r.returncode:
        RESCUE_WHY = f"main has {ahead} commit(s) GitHub doesn't (kept on {branch}) and git reset failed: " \
                     f"{(r.stderr or r.stdout).strip()[-160:]}"
        log(f"{repo.name}: {RESCUE_WHY}")
        return False
    log(f"{repo.name}: main had {ahead} commit(s) GitHub doesn't; kept on {branch} (pushed), main reset to origin/main")
    return True


def run_one() -> str:
    """One job: 'ran' after a job (finished or released), else 'idle', 'waiting' or 'error'."""
    problem = pull_main()
    if problem:
        log(problem)
        push_heartbeat("error", [problem])
        return "error"
    why = guards()
    if why:
        log("not now: " + "; ".join(why))
        push_heartbeat("waiting", why)
        return "waiting"
    return run_ordinary()


# Each channel's Studio browser: the Mini's ports and profiles (start_cdp_browsers.sh), named in the channel files.
CDP_PORTS = tuple(p for p in (channels.studio_port(s) for s in channels.slugs()) if p)


def cdp_ports_up(ports=CDP_PORTS) -> list:
    """The CDP ports whose Chrome answers here (Ben, 9 Nov 2026: signed into Studio on the MacBook). jobs.py offers a
    Studio job to the MacBook only while its channel's browser is up."""
    import urllib.request
    up = []
    for p in ports:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{p}/json/version", timeout=2) as r:
                if r.status == 200:
                    up.append(p)
        except Exception:
            pass
    return up


def run_ordinary() -> str:
    """Claim the next MacBook job and run it on the first installed agent in its chain."""
    args = [sys.executable, "scripts/jobs.py", "next", "--agent", AGENT_ID, "--can", "macbook,any", "--git"]
    # Read by jobs.macbook_studio_ok in the claim below. Empty when no agent here can drive the browser unattended, so
    # a Studio job is never claimed just to be handed back.
    os.environ["MACBOOK_CDP"] = ",".join(cdp_ports_up()) if studio_agents(usable(installed())) else ""
    r = sh(args, cwd=STUDIO)  # any: rule H reviews
    if r.returncode == 10:
        log("no macbook job waiting")
        push_heartbeat("idle", ["no MacBook job waiting"])
        return "idle"
    job = claimed_job(r.stdout)
    if r.returncode or not job:
        log(f"claim failed: {(r.stderr or r.stdout).strip()[-300:]}")
        push_heartbeat("error", [f"claim failed: {(r.stderr or r.stdout).strip()[-120:]}"])
        return "error"
    push_heartbeat("working", [], job)
    have = usable(installed())
    try:  # the same out-of-credit flags the Mini's relay honours (scripts/credit_flags.json)
        import routing
        routing.OUT = set(routing.read_flags(path=str(STUDIO / "scripts" / "credit_flags.json")))
    except Exception:  # noqa: BLE001
        pass
    agent, model = pick_agent(job_record(job), have)
    cap = int(os.environ.get("MACBOOK_CAP_S", "1500"))
    prompt = brief(job, os.environ.get("OLLAMA_MODEL", "qwen3:14b"), cap // 60)
    cmd = agent_cmd(agent, prompt, model) if agent else None
    if not cmd:
        sh([sys.executable, "scripts/jobs.py", "release", job, "--agent", AGENT_ID, "--note",
            f"MacBook worker: no agent CLI installed for this job (installed: {', '.join(have) or 'none'})", "--git"],
           cwd=STUDIO)
        log(f"no CLI for {job} (installed: {have}): released")
        return "error"
    log(f"{job}: waking {agent}{' on ' + model if model else ''} (cap {cap // 60} min)")
    before = branch_heads(job)
    started = time.monotonic()
    code = run_capped(busy_cmd(["caffeinate", "-i", *cmd] if shutil.which("caffeinate") else cmd), STUDIO, cap)
    seconds = time.monotonic() - started
    ff_main(STUDIO, STUDIO.resolve().is_relative_to(WORKER_DIR.resolve()))
    paused = ""
    open_now = still_mine(job)
    # A clean exit that pushed its branch but left the job open is finished work waiting for the Chief, not a job to
    # hand back. A failed run, a run that hit the cap and a run that pushed nothing are released as before.
    pushed = pushed_work(job, before) if open_now and code == 0 else {}
    if not pushed and failed_run(code, seconds, open_now):  # 124 = hit the cap: slow, not broken
        paused = mark_down(agent)
    if pushed and park(job, agent, pushed):
        log(f"{job}: parked for the Chief ({pushed['branch']} pushed, job left open)")
        push_heartbeat("idle", [f"last run: {job} on {agent} pushed its work; parked for the Chief"])
    elif open_now:
        note = f"MacBook worker run on {agent} ended (exit {code}) with the job still open; picked up again next run"
        if paused:
            note += f"; {agent} paused on the MacBook until {paused}, so the next run uses the next agent in the chain"
        sh([sys.executable, "scripts/jobs.py", "release", job, "--agent", AGENT_ID, "--note", note, "--git"], cwd=STUDIO)
        log(f"{job}: released after exit {code}")
        push_heartbeat("idle", [f"last run: {job} on {agent} failed (exit {code})"
                                + (f"; {agent} paused until {paused}" if paused else "")])
    else:
        log(f"{job}: finished (exit {code})")
        push_heartbeat("idle", [f"last run: {job} on {agent} finished"])
    if agent == "codex":
        record_usage()
    return "ran"




def start_other_slots(popen=None, system=None) -> list:
    """Slot 1 starts slots 2..SLOTS, each in its own process group with its own log; a slot still running from an
    earlier tick holds its lock and the new copy exits at once."""
    if SLOT != 1 or SLOTS < 2 or (system or platform.system()) != "Darwin":  # the MacBook only: never from a test or another host
        return []
    popen = popen or subprocess.Popen
    started = []
    logs = HOME / "Library" / "Logs"
    for n in range(2, SLOTS + 1):
        clones = {channels.get(s)["repo"]["env"]: str(slot_dir(n) / clone_name(s))
                  for s in channels.slugs() if channels.get(s)["repo"].get("env")}
        env = dict(os.environ, MACBOOK_SLOT=str(n), **clones)
        try:
            logs.mkdir(parents=True, exist_ok=True)
            with open(logs / f"{channels.studio_prefix()}-macbook-worker-{n}.log", "a") as out:   # the child keeps its own handle
                popen([sys.executable, str(pathlib.Path(__file__).resolve()), "run"], env=env, stdout=out,
                      stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
            started.append(n)
        except OSError as e:
            log(f"slot {n} not started: {e}")
    return started


def leave_the_board_to_the_mini() -> None:
    """One publisher for the board (J2541, 10 Nov 2026). jobs.py starts board_publish.py after every queue change on
    any machine with ~/_desk/state/chief, and the MacBook has that folder, so both slots force-pushed board-data all
    day beside the Mini (197 pushes on 10 Nov; one was rejected because another publish landed mid-push). With
    BOARD_PUBLISH=0 in the worker's own environment, its jobs.py calls, the agents it wakes and slot 2 all skip the
    hook. The Mini publishes within a minute of any push to main, so nothing is lost."""
    os.environ["BOARD_PUBLISH"] = "0"


def run() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    leave_the_board_to_the_mini()
    start_other_slots()
    # The lock file is closed, and the lock freed, when the run returns (J2463: it used to be left open).
    with open(STATE / f"{slot_name(SLOT, 'macbook-worker')}.lock", "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            log("another run is still going")
            return 0
        return _take_jobs()


def _take_jobs() -> int:
    # Keep taking jobs back to back (Ben, 5 Nov 2026: "why are agents taking so long between jobs"): launchd starts a
    # run every 15 min, and the run keeps going while there is work and the guards hold, up to MACBOOK_LOOP_MIN.
    # The lock stops a second run, so a long job simply carries the lane into the next tick.
    started = dt.datetime.now(dt.timezone.utc)
    budget = dt.timedelta(minutes=float(os.environ.get("MACBOOK_LOOP_MIN", "13")))
    jobs_run = 0
    while True:
        status = run_one()
        if status != "ran":
            return 1 if status == "error" and not jobs_run else 0
        jobs_run += 1
        if dt.datetime.now(dt.timezone.utc) - started >= budget:
            log(f"loop budget used after {jobs_run} job(s); the next tick carries on")
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
