#!/usr/bin/env python3
"""Studio job queue: any agent that is up can do any job it is able to, whoever was meant to (7 Oct 2026).

Jobs used to be addressed to an agent by name in prose on the studio thread ("Chief, please ..."). When that agent
was down (Grok Bot out of credit), its jobs sat. Here a job says what it NEEDS, not who does it, and whichever agent
is alive and able claims it. The thread stays for discussion and reports; this queue is the work list.

  needs   mini    the Mac mini: media, ffmpeg, picture, edit, YouTube/Studio, launchd (Grok Bot or Cursor)
          gemini  a facts-and-numbers check run through Gemini (Antigravity `agy`) on the Mini
          cloud   a Claude cloud session: reviews, scripts, shot lists, code, the tracker
          ben     only Ben: money, a sign-in, a decision
          any     whoever is free
  kind    what sort of job it is (scripts/routing.py, AGENTS.md "Who does what", Ben 11 Oct 2026): script, facts,
          review, vo, image, chart, thumb, video, assembly, qa, listing, studio, chief. The relay wakes the worker whose
          model does that kind best (chart -> Codex on gpt-6-astra) and passes the model; --model overrides it.

  python3 scripts/jobs.py add --needs mini --title "Sun 022 first cut" --body-file brief.md --film 022 --stage edit \\
          --ref 6036709461 --by claude --git
  python3 scripts/jobs.py next --agent cursor --can mini,gemini,any --git      # claims the oldest job it can do
  python3 scripts/jobs.py done J0003 --agent cursor --result "cut v01 at OWB UAT/..." --ref 1a2b3c4 --git
  python3 scripts/jobs.py block J0003 --agent cursor --reason "needs Ben: Vertex credit" --git
  python3 scripts/jobs.py release J0003 --agent cursor --note "stopping point; rows 1-40 done" --git
  python3 scripts/jobs.py renew J0003 --agent cursor --eta 120 --git           # still working: push the ETA out
  python3 scripts/jobs.py progress J0003 --agent cursor --step 3 --of 8 --git   # finished step 3 of 8 (the board's % done)
  python3 scripts/jobs.py wait J0003 --condition "Verify renewed credit" --check-at "2026-10-30T00:05Z" --type credits --agent cursor --git
  python3 scripts/jobs.py list [--all]                                          # open and claimed jobs (JOBS.md too)
  python3 scripts/jobs.py approved J0945 --from J0924 --ok-at "2026-10-25 14:10" --ref 6398691247 --agent chief --git
          # Ben OK'd the cut J0924 asked about; J0945 delivers it: board lane "Approved, on its way" until it's on YouTube
  python3 scripts/jobs.py reroute J0003 --agent relay --to cursor --model cursor-claude-opus-5-5 --note "Claude out of usage" --git
          # Claude Code out of usage (Ben, 11 Oct 23:40): hand a Claude job to Cursor on the Claude model

`next` exits 10 when no claim is available, and `next --peek` makes the identical choice without mutation.
Recorded deadlines and inherited prerequisite deadlines go first; urgency, production, focus, short jobs and age
break ties. A claim is stalled only after 45 minutes beyond its ETA/latest activity with no validated active-run
lease. All queue, relay and board calculations use that policy. `--after` waits for a completed prerequisite.
A structured condition hold schedules a Chief verification task, never an automatic release or fixed production
start. The elected Chief records evidence before reopening, or records a future check with `wait --recheck`.
Ben approvals remain explicit. `--action` records the actual unfinished action shown on the board; update it with
`progress --action` as work advances. A job with --film/--stage also claims that
stage on the studio board in the same commit (and releases it on done/release/block), so the board and the queue
always agree. Mutating commands take --git: pull, write, commit only the queue files (+ the film's status.json and
STATUS.md), push, and retry if another agent raced the push.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chief_relay  # noqa: E402
import routing  # noqa: E402
import workflow_state as workflow
import studio  # noqa: E402

ROOT = studio.ROOT
QUEUE = ROOT / "jobs" / "queue.json"
JOBS_MD = ROOT / "JOBS.md"
NEEDS = ["mini", "gemini", "cloud", "ben", "any"]
EX_NONE = 10
DEFAULT_ETA = 120
QUICK_MIN = 60
LONDON = ZoneInfo("Europe/London")


def now():
    return studio.now()


def load(path: pathlib.Path = QUEUE) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"next_id": 1, "jobs": []}


def save(data: dict, path: pathlib.Path = QUEUE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def find(data: dict, jid: str) -> dict | None:
    return next((j for j in data["jobs"] if j["id"] == jid.upper()), None)


def stalled(job: dict, at: dt.datetime) -> bool:
    return workflow.claim_is_stalled(job, at, chief_relay.current_execution(at))


def log(job: dict, at: dt.datetime, agent: str, what: str) -> None:
    job.setdefault("history", []).append({"at": studio.iso(at), "by": agent, "what": what})


def parse_not_before(text: str) -> str:
    """"YYYY-MM-DD HH:MM" in London time -> the queue's UTC stamp ("2026-10-12T08:00Z"); "" clears it."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        local = dt.datetime.strptime(text, "%Y-%m-%d %H:%M").replace(tzinfo=LONDON)
    except ValueError:
        raise ValueError(f'--not-before must be "YYYY-MM-DD HH:MM" (London time), not {text!r}')
    return studio.iso(local.astimezone(dt.timezone.utc))


def london_hm(stamp: str) -> str:
    """UTC queue stamp -> "HH:MM" London (with the date when it isn't today in London)."""
    t = studio.parse(stamp).astimezone(LONDON)
    return t.strftime("%H:%M") if t.date() == now().astimezone(LONDON).date() else t.strftime("%a %d %b %H:%M")



def do_add(data: dict, *, title: str, needs: str, body: str, by: str, at: dt.datetime, ref: str = "", film: str = "",
           stage: str = "", after: str = "", repo: str = "owb", eta_min: int = DEFAULT_ETA, for_agent: str = "",
           kind: str = "", model: str = "", not_before: str = "", reset: str = "", due: str = "", action: str = "") -> dict:
    if needs not in NEEDS:
        raise ValueError(f"needs must be one of {', '.join(NEEDS)}")
    if kind and kind not in routing.KINDS:
        raise ValueError(f"kind must be one of {', '.join(routing.KINDS)}")
    if model and model not in routing.MODELS:
        raise ValueError(f"model must be a configured one: {', '.join(routing.MODELS)}")
    if bool(film) != bool(stage):
        raise ValueError("--film and --stage go together")
    if stage and stage not in studio.STAGES:
        raise ValueError(f"stage must be one of {', '.join(studio.STAGES)}")
    if after and not find(data, after):
        raise ValueError(f"--after {after}: no such job")
    if not_before:
        raise ValueError("Use a structured hold with jobs.py wait --condition ... --check-at ...; ready work has no fixed start time")
    nb = ""
    due = workflow.normalize_due(due)
    if len(action.strip()) > 180:
        raise ValueError("--action must fit 180 characters")
    job = {"id": f"J{data['next_id']:04d}", "title": title, "needs": needs, "repo": repo, "body": body, "ref": ref,
           "film": film, "stage": stage, "after": after.upper() if after else "", "eta_min": eta_min,
           "status": "open", "by": "", "since": "", "eta": "", "created_by": by, "created_at": studio.iso(at),
           "result": "", "history": []}
    job["remaining_action"] = action.strip() or title.strip()[:180]
    if due:
        job["due"] = due
    if for_agent:
        job["for"] = for_agent
    if kind:
        job["kind"] = kind
    if model:
        job["model"] = model
    if nb:
        job["not_before"] = nb
        job["reset"] = reset.strip()
    log(job, at, by, "added" + (f" for {for_agent}" if for_agent else ""))
    data["next_id"] += 1
    data["jobs"].append(job)
    return job


def film_named(title: str) -> bool:
    """A title that starts with a film number or names one with its channel (OWB 027, HOS 006)."""
    return bool(re.match(r"\s*0\d\d\b", title) or re.search(r"\b(?:OWB|HOS)[ :]*0\d\d\b", title))


def claimable(data: dict, job: dict, can: set[str], at: dt.datetime, agent: str = "") -> bool:
    chief = agent if workflow.role_job(job) and chief_relay.is_elected_chief(agent, at) else ""
    return workflow.claimable(job, data["jobs"], at, agent, chief, can, chief_relay.current_execution(at))


def ordered(data: dict, at: dt.datetime | None = None) -> list:
    due = workflow.deadlines(data["jobs"])
    return sorted(data["jobs"], key=lambda j: workflow.order(j, due, data.get("focus") or (), at))


def set_wait(job, agent, at, hold, action="", recheck=""):
    if not str(agent or "").strip():
        raise ValueError("A non-empty --agent is required")
    if job.get("status") == "claimed":
        _mine(job,agent)
        do_block(job,agent,"Waiting for: " + str(hold.get("condition") or ""),at)
    if job.get("status") != "blocked":
        raise ValueError("A hold can only be recorded on a claimed or blocked job")
    if agent != "relay" and job.get("by") != agent and not chief_relay.is_elected_chief(agent,at):
        raise ValueError("Only the holder or elected Chief may update this hold")
    condition = str(hold.get("condition") or "").strip()
    check = workflow.normalize_due(hold.get("check_at"))
    if not condition or not check:
        raise ValueError("A hold needs --condition and --check-at")
    value = {"type":hold.get("type") or "input","condition":condition,"check_at":check}
    if recheck:
        if workflow.timestamp(check) <= at:
            raise ValueError("A verification retry needs a future --check-at")
        if not chief_relay.is_elected_chief(agent,at):
            raise ValueError("Only the elected Chief may record a condition check")
        value.update(last_recheck=recheck,checked_at=at.isoformat(),checked_by=agent)
    job["hold"] = value
    if action:
        job["remaining_action"] = str(action).strip()
    log(job,at,agent,"condition recorded; next verification " + check)


def apply_metadata(data, entries, agent, at):
    if agent != "relay" and not chief_relay.is_elected_chief(agent,at):
        raise ValueError("Workflow metadata requires relay maintenance or the elected Chief")
    # Validate on a copy first: a bad entry cannot partially change the queue.
    import copy
    planned = copy.deepcopy(data)
    for entry in entries:
        j = find(planned,entry.get("id", ""))
        if not j:
            raise ValueError("Unknown metadata job: " + str(entry.get("id")))
        if j["status"] not in workflow.LIVE:
            continue  # concurrent completions retain their final record
        action = str(entry.get("remaining_action") or "").strip()
        if len(action) > 180:
            raise ValueError("remaining_action must fit 180 characters")
        if action and (not j.get("remaining_action") or entry.get("replace")):
            j["remaining_action"] = action
            log(j,at,agent,"remaining action: " + action)
        if entry.get("hold") and j["status"] == "blocked" and not j.get("hold"):
            set_wait(j,agent,at,entry["hold"])
    data.clear(); data.update(planned)


def reconcile_holds(data, at):
    by_id = {j["id"]:j for j in data["jobs"]}
    due = workflow.deadlines(data["jobs"])
    changed = []
    for parent in list(data["jobs"]):
        if parent.get("recheck_of") or not workflow.hold_due(parent,by_id,at):
            continue
        pending = next((j for j in data["jobs"] if j.get("recheck_of") == parent["id"] and j.get("status") in workflow.LIVE),None)
        if pending:
            continue
        condition = (parent.get("hold") or {}).get("condition") or "Required predecessor is complete; verify remaining gates and approvals"
        task = do_add(data,title="Chief: verify condition for " + parent["id"],needs="any",kind="chief",by="relay",at=at,
            body="Verify the waiting condition for " + parent["id"] + ": " + condition +
            ". Read the original job, latest result, evidence and approval history. This is a verification task, not permission to upload, spend or change a schedule. "
            "If the condition is proven satisfied, and all original gates/Ben approvals remain valid, reopen the original job with an evidence note. "
            "Otherwise keep it blocked and run jobs.py wait " + parent["id"] + " --agent <your elected id> --condition '<actual unmet condition>' --check-at '<next sensible UTC time>' --type input --recheck RECHECK_ID. "
            "Use this task's actual id for RECHECK_ID. Then finish this verification task. Never infer test completion, public status or restored credits from a date alone. "
            "If you cannot verify, record why and follow the original recorded retry date, or retry in six hours when none is specified. Update --action with the actual unfinished action if needed.")
        task["recheck_of"] = parent["id"]
        task["remaining_action"] = ("Verify readiness: " + (parent.get("remaining_action") or parent["title"]))[:180]
        target = at + dt.timedelta(hours=1)
        if parent["id"] in due:
            target = min(target,due[parent["id"]])
        task["due"] = target.isoformat()
        task["due_kind"] = "condition-verification"
        parent.setdefault("hold",{"type":"dependency","condition":condition})["check_at"] = (at+dt.timedelta(hours=1)).isoformat()
        parent["hold"]["recheck_task"] = task["id"]
        log(parent,at,"relay","condition verification queued: " + task["id"])
        changed += [parent["id"],task["id"]]
    return changed


def reconcile_dependencies(data: dict, at: dt.datetime) -> list:
    by_id = {j["id"]: j for j in data["jobs"]}
    changed = []
    for j in list(data["jobs"]):
        if j.get("status") not in ("open", "blocked") or j.get("dependency_resolution"):
            continue
        problem = workflow.dependency_problem(j, by_id)
        if not problem:
            continue
        key = problem["kind"] + ":" + ",".join(problem["ids"])
        explanation = workflow.reason(j, by_id, at)
        if j.get("dependency_problem") != problem:
            j.update(status="blocked", result=explanation, dependency_problem=problem, eta="")
            log(j, at, "relay", "blocked: " + explanation)
            changed.append(j["id"])
        if not any(x.get("dependency_resolution") == key and x.get("status") in workflow.LIVE for x in data["jobs"]):
            task = do_add(data, title="Chief: resolve " + key, needs="any", kind="chief", by="relay", at=at,
                          body="Resolve dependency problem " + key + ". Inspect affected jobs and their existing approvals. Record an explicit replacement dependency, repair or cancellation decision; never bypass a hold. Do not upload or change media as part of this task.")
            task["dependency_resolution"] = key
            changed.append(task["id"])
    return changed


MINI_NEEDS = {"mini", "gemini", "any"}


def can_any_mini_claim(data, job, at):
    chief = chief_relay.acting(at)[1] if workflow.role_job(job) else ""
    actors = [chief] if workflow.role_job(job) else [job["for"]] if job.get("for") else routing.MINI_WORKERS
    return any(actor and workflow.claimable(job,data["jobs"],at,actor,chief,MINI_NEEDS,chief_relay.current_execution(at)) for actor in actors)


def do_watch(data: dict, at: dt.datetime, quiet_h: float = 3) -> dict:
    """What Claude's 2-hourly check alerts Ben about (read only):
    quiet  Mini work is waiting or stalled, nothing holds a live Mini claim, and no agent but Claude has touched the
           queue for quiet_h hours: the Mini, the relay or every Chief in the chain is down.
    ben    jobs only Ben can do (needs ben, open) and jobs blocked on him, with when each started waiting."""
    def mini_able(j):
        return can_any_mini_claim(data,j,at)
    waiting = [j["id"] for j in data["jobs"] if j["needs"] in MINI_NEEDS and mini_able(j)]
    live = [j["id"] for j in data["jobs"] if j["status"] == "claimed" and not stalled(j, at) and j["needs"] in MINI_NEEDS]
    stamps = [studio.parse(h["at"]) for j in data["jobs"] for h in j.get("history", []) if h.get("by") not in ("claude", "")]
    last = max(stamps) if stamps else None
    quiet = bool(waiting) and not live and (last is None or at - last > dt.timedelta(hours=quiet_h))
    ben = []
    for j in data["jobs"]:
        if (j["needs"] == "ben" and j["status"] in ("open", "claimed")) or j["status"] == "blocked":
            since = j["history"][-1]["at"] if j.get("history") else ""
            ben.append({"id": j["id"], "title": j["title"], "status": j["status"], "since": since,
                        "why": (j.get("result") if j["status"] == "blocked" else "") or j.get("body", "")[:200]})
    return {"quiet": quiet, "last_mini_activity": studio.iso(last) if last else None, "waiting_mini": waiting,
            "live_claims": live, "ben": ben}


def urgent_rank(job: dict) -> int:
    """Urgent jobs run in the order they were named (Grok Bot, 9 Oct: `urgent J0085 J0096 J0089` = that order). The
    rank is stored in "urgent" (1 = first); an older plain `true` counts as rank 0, then id order."""
    u = job.get("urgent")
    return u if isinstance(u, int) and not isinstance(u, bool) else 0


def do_urgent(data: dict, found: list[dict], off: bool = False) -> list[str]:
    """Mark jobs urgent in the order named, after any other urgent jobs (a named one that was already urgent moves to
    its named place); --off clears them. Returns the urgent ids in run order."""
    for j in found:
        if off:
            j.pop("urgent", None)
    if not off:
        named = [j["id"] for j in found]
        rest = [j for j in sorted(data["jobs"], key=lambda j: (urgent_rank(j), j["id"]))
                if j.get("urgent") and j["id"] not in named and j["status"] in ("open", "claimed", "blocked")]
        for k, j in enumerate(rest + found, 1):
            j["urgent"] = k
    live = (j for j in data["jobs"] if j.get("urgent") and j["status"] in ("open", "claimed", "blocked"))
    return [j["id"] for j in sorted(live, key=lambda j: (urgent_rank(j), j["id"]))]


RETRY_COOL_MIN = 30


def recently_released(job: dict, at: dt.datetime | None = None) -> bool:
    """Its last event is a release less than RETRY_COOL_MIN ago (a poll like the Flow balance read): it goes behind
    every other ready job so it isn't re-run back to back, but it is still claimable if nothing else is ready."""
    return workflow.recently_released(job, at or now())


def order(job: dict, focus=()) -> tuple:
    return workflow.order(job, workflow.deadlines([job]), focus)


def require_chief(job, agent, at):
    if not str(agent or "").strip():
        raise ValueError("A non-empty --agent is required")
    if workflow.role_job(job) and not chief_relay.is_elected_chief(agent, at):
        raise ValueError("Chief authority changed: only the currently elected Chief may resume or complete this job; release or park it")


def choose_next(data, agent, can, at, job_id=""):
    if not str(agent or "").strip():
        raise ValueError("A non-empty --agent is required")
    held = next((j for j in data["jobs"] if j.get("by") == agent and j["status"] == "claimed"), None)
    if held:
        require_chief(held, agent, at)
        if workflow.external_hold(held,at):
            return None
        return held if not job_id or held["id"] == job_id else None
    return next((j for j in ordered(data, at) if (not job_id or j["id"] == job_id) and claimable(data,j,can,at,agent)), None)


def do_next(data: dict, agent: str, can: set[str], at: dt.datetime, eta_min: int | None = None, job_id: str = "") -> dict | None:
    job = choose_next(data,agent,can,at,job_id)
    if not job:
        return job
    # A claim always has an explicit baseline. This records no completed work;
    # workers replace the default plan before reporting their first milestone.
    if not job.get("progress"):
        job["progress"] = {"step": 0, "of": 3, "at": studio.iso(at), "by": agent,
                           "default_plan": True, "note": "Starting: check the brief, complete the work, verify the result"}
    if job.get("by") == agent and job["status"] == "claimed":
        return job
    took, prev = stalled(job, at), job.get("by", "")
    job.update(status="claimed", by=agent, since=studio.iso(at), eta=studio.iso(at + dt.timedelta(minutes=eta_min or job.get("eta_min") or DEFAULT_ETA)))
    log(job, at, agent, f"claimed (took over a stalled claim by {prev})" if took else "claimed")
    return job


def _mine(job: dict, agent: str) -> None:
    if not str(agent or "").strip():
        raise ValueError("A non-empty --agent is required")
    if job["status"] != "claimed" or job.get("by") != agent:
        raise ValueError(f"{job['id']} is {job['status']}" + (f" by {job['by']}" if job.get("by") else "") + f", not claimed by {agent}")


SWAP_RE = re.compile(r"\b([A-Za-z0-9_-]{11}):\s*swap to\b", re.I)
READBACKS = pathlib.Path(__file__).resolve().parents[1] / "jobs" / "readbacks"


def swap_old_id(job: dict) -> str:
    """The old copy a swap job replaces, from its title ("... Short dM1OgGPAYvw: swap to v05 ..."), else ""."""
    m = SWAP_RE.search(job.get("title") or "")
    return m.group(1) if m else ""


def swap_readback_problem(job: dict, at: dt.datetime, folder: pathlib.Path | None = None) -> str:
    """Why a swap job can't close yet, or "". Its old copy must read back from YouTube as Private with no publishAt,
    and the new copy Private + scheduled, in jobs/readbacks/<id>.json written by
    07_Content-Ops/scripts/verify-swap.ts within the last 2 hours (26 Oct 2026: four swaps closed as "unscheduled"
    while the board still showed both copies scheduled for one slot)."""
    old = swap_old_id(job)
    if not old:
        return ""
    path = (folder or READBACKS) / f"{job['id']}.json"
    try:
        rb = json.loads(path.read_text())
    except (OSError, ValueError):
        return (f"swap job: no read-back at jobs/readbacks/{job['id']}.json; run "
                f"`npx tsx --env-file=.env scripts/verify-swap.ts --job {job['id']} --old {old} --new <new id>` in 07_Content-Ops")
    o, n = rb.get("old") or {}, rb.get("new") or {}
    if o.get("id") != old:
        return f"swap job: read-back is for old copy {o.get('id') or '?'}, not {old}"
    if o.get("privacyStatus") != "private" or o.get("publishAt"):
        return f"swap job: old copy {old} reads {o.get('privacyStatus')} publishAt {o.get('publishAt')}; it must be private and unscheduled"
    if n.get("privacyStatus") != "private" or not n.get("publishAt"):
        return f"swap job: new copy {n.get('id')} reads {n.get('privacyStatus')} publishAt {n.get('publishAt')}; it must be private and scheduled"
    try:
        when = dt.datetime.fromisoformat(str(rb.get("at") or "").replace("Z", "+00:00"))
    except ValueError:
        return "swap job: read-back has no time"
    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    if at - when > dt.timedelta(hours=2):
        return f"swap job: read-back is from {rb.get('at')}; read both copies back again"
    return ""


def do_done(job: dict, agent: str, result: str, at: dt.datetime, ref: str = "") -> None:
    _mine(job, agent)
    require_chief(job, agent, at)
    problem = swap_readback_problem(job, at)
    if problem:
        raise ValueError(f"{job['id']}: {problem}")
    job.update(status="done", result=result, eta="")
    if ref:
        job["done_ref"] = ref
    log(job, at, agent, "done: " + result)


def do_block(job: dict, agent: str, reason: str, at: dt.datetime) -> None:
    _mine(job, agent)
    job.update(status="blocked", result=reason, eta="")
    if not workflow.is_review(job) and not job.get("hold"):
        is_ben = bool(job.get("awaits_ben") or job.get("needs") == "ben" or re.search(r"(?:needs?|waiting for) Ben\b",reason,re.I))
        job["hold"] = {"type":"ben" if is_ben else "dependency" if job.get("after") and not re.search(r"public|credit|reset|renewal|date gate",reason,re.I) else "input","condition":reason,"check_at":(at+dt.timedelta(hours=6)).isoformat()}
    log(job, at, agent, "blocked: " + reason)


def do_release(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    _mine(job, agent)
    job.update(status="open", by="", since="", eta="")
    log(job, at, agent, "released" + (": " + note if note else ""))


def do_renew(job: dict, agent: str, eta_min: int, at: dt.datetime) -> None:
    _mine(job, agent)
    require_chief(job, agent, at)
    job["eta"] = studio.iso(at + dt.timedelta(minutes=eta_min))
    log(job, at, agent, f"renewed to {job['eta']}")


def do_progress(job: dict, agent: str, step: int, of: int, at: dt.datetime, note: str = "", films: str | None = None, action: str | None = None) -> None:
    """Ben, 11 Oct 22:09: the board says "Working on X, 20% done, finished in about 30 min". A worker reports each
    finished step: `progress J0130 --step 3 --of 8` = 3 of 8 steps done. The page turns it into % done and an ETA from
    the pace so far. Kept across a release (the next run carries on from it); cleared when the job is reopened.
    Allowed on a job the agent holds, or an open one it released between steps."""
    require_chief(job, agent, at)
    if of < 1 or step < 0 or step > of:
        raise ValueError(f"--step {step} --of {of}: need 0 <= step <= of and of >= 1")
    if job["status"] == "claimed" and job.get("by") != agent:
        raise ValueError(f"{job['id']} is claimed by {job['by']}, not {agent}")
    if job["status"] not in ("claimed", "open"):
        raise ValueError(f"{job['id']} is {job['status']}; progress is for a job in hand")
    if action is not None and (not action.strip() or len(action.strip()) > 180):
        raise ValueError("--action needs a plain remaining action of 1-180 characters")
    if films is not None:
        keys = list(dict.fromkeys(x.strip().upper() for x in films.split(",") if x.strip()))
        if not keys or any(not re.fullmatch(r"(?:HOS|OWB):\d{3}", x) for x in keys):
            raise ValueError("--films needs channel-qualified video ids, e.g. HOS:006 or OWB:028,OWB:029")
        job["taskKeys"] = keys
    if action is not None:
        job["remaining_action"] = action.strip()
    job["progress"] = {"step": step, "of": of, "at": studio.iso(at), "by": agent}
    if note:
        job["progress"]["note"] = note[:120]
    log(job, at, agent, f"step {step} of {of} done" + (": " + note if note else ""))


def do_reopen(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    require_chief(job,agent,at)
    if job["status"] not in ("blocked", "done", "cancelled"):
        raise ValueError(f"{job['id']} is {job['status']}; only blocked, done or cancelled jobs reopen")
    if job.get("hold") and not chief_relay.is_elected_chief(agent, at):
        raise ValueError("Only the elected Chief may release a verified hold")
    if job.get("hold") and not str(note or "").strip():
        raise ValueError("Reopening a hold requires current verification evidence in --note")
    job.pop("hold", None)
    job.update(status="open", by="", since="", eta="", result="")
    job.pop("progress", None)
    log(job, at, agent, "reopened" + (": " + note if note else ""))


def do_reroute(job: dict, agent: str, to: str, model: str, note: str, at: dt.datetime) -> None:
    """Hand a job to another worker on a given model (Ben, 11 Oct 2026 23:40: "if Claude Code is out of usage you can
    use a Claude model in Cursor"). The job becomes an open Mini job only `to` may claim, carrying `model`; what it was
    before is kept in rerouted_from. An open, blocked, or claimed job (the holder's claim ends) can be rerouted."""
    if job["status"] in ("done", "cancelled"):
        raise ValueError(f"{job['id']} is {job['status']}; nothing to reroute")
    if model and model not in routing.MODELS:
        raise ValueError(f"model must be a configured one: {', '.join(routing.MODELS)}")
    if model and routing.RUNS_ON.get(model) != to:
        raise ValueError(f"{model} doesn't run on {to}")
    if job.get("kind") == "chief" and not chief_relay.is_elected_chief(to, at):
        raise ValueError(f"{job['id']} is a Chief call; only the elected Chief may take it")
    job.setdefault("rerouted_from", {"needs": job["needs"], "for": job.get("for", ""), "model": job.get("model", ""),
                                     "status": job["status"], "by": job.get("by", "")})
    job.update(status="open", by="", since="", eta="", needs="mini", **{"for": to})
    if job.get("result") and job["rerouted_from"].get("status") == "blocked":
        job["result"] = ""
    if model:
        job["model"] = model
    log(job, at, agent, f"rerouted to {to}" + (f" on {model}" if model else "") + (": " + note if note else ""))


def do_handback(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    """Undo a reroute once the original agent is back (Ben, 14 Oct 2026: "when you're back online, it switches back
    to you"): only a job no stand-in has started (still open) goes back to what it was before."""
    rf = job.get("rerouted_from")
    if not rf:
        raise ValueError(f"{job['id']} was never rerouted")
    if job["status"] != "open":
        raise ValueError(f"{job['id']} is {job['status']}; a stand-in has it, so it stays")
    job.update(needs=rf.get("needs") or job["needs"], status="open", by="", since="", eta="")
    for k in ("for", "model"):
        if rf.get(k):
            job[k] = rf[k]
        else:
            job.pop(k, None)
    job.pop("rerouted_from", None)
    log(job, at, agent, "handed back" + (": " + note if note else ""))


def do_awaits(job: dict, agent: str, at: dt.datetime, *, what: str = "", file: str = "", version: str = "", due: str = "",
              airs: str = "", if_not: str = "", card: str = "", title: str = "", number: str = "", vtype: str = "",
              add: bool = False, clear: bool = False) -> None:
    """Mark a job as waiting on Ben (Ben, 25 Oct 2026: every cut he has to OK shows on the board, with Play and its
    deadline). `awaits_ben` is the one signal the Studio Kanban builds Ready for OK cards from (video_tracker.py
    ask_entries); scripts/board_check.py checks every entry reached the published board. --add appends another cut to
    the same job (J0937 holds three Shorts); --clear removes the signal (Ben answered, or the hold was dropped)."""
    if clear:
        # Keep what was asked (awaits_was), so `jobs.py approved <follow-on> --from <this job>` can still link it.
        if job.get("awaits_ben"):
            job["awaits_was"] = job.pop("awaits_ben")
        log(job, at, agent, "no longer waits on Ben")
        return
    if not what or not file:
        raise ValueError("awaits needs --what (what Ben is OKing) and --file (the cut to play)")
    entry = {"what": what, "file": file}
    for k, v in (("version", version), ("due", parse_not_before(due) if due else ""), ("airs", parse_not_before(airs) if airs else ""),
                 ("ifNot", if_not), ("card", card), ("title", title), ("number", number), ("type", vtype)):
        if v:
            entry[k] = v
    cur = job.get("awaits_ben")
    cur = cur if isinstance(cur, list) else ([cur] if isinstance(cur, dict) else [])
    job["awaits_ben"] = (cur + [entry]) if add else [entry]
    if len(job["awaits_ben"]) == 1:
        job["awaits_ben"] = job["awaits_ben"][0]
    log(job, at, agent, f"waits on Ben: {what}" + (f" (by {due} London)" if due else ""))


APPROVED_FIELDS = ("what", "file", "version", "airs", "card", "title", "number", "type", "channel")


def do_approved(job: dict, src: dict, agent: str, at: dt.datetime, *, entry: int = 0, ok_at: str = "", ref: str = "",
                over: dict | None = None) -> None:
    """Ben OK'd a cut; `job` is the follow-on that delivers it (the swap, package or upload). Sets job["approved_from"]
    (Ben, 25 Oct 2026 14:13: "Ones I approve ... need to know they're still in the pipeline"): the Studio Kanban shows
    the job in "Approved, on its way" with its status until it's done and the upload reads back Private + scheduled
    (video_tracker.approved_entries). `src` is the job that asked Ben (its awaits_ben, or awaits_was once cleared); it
    is `job` itself when the held job just reopens (J0940). Asking it clears src's awaits_ben: Ben has answered."""
    raw = src.get("awaits_ben") or src.get("awaits_was") or {}
    items = [x for x in (raw if isinstance(raw, list) else [raw]) if isinstance(x, dict)]
    if entry:
        if not 1 <= entry <= len(items):
            raise ValueError(f"{src['id']} has {len(items)} awaits entr{'y' if len(items) == 1 else 'ies'}; --entry {entry} is out of range")
        base = items[entry - 1]
    elif len(items) > 1:
        raise ValueError(f"{src['id']} asked Ben about {len(items)} cuts; say which with --entry N")
    else:
        base = items[0] if items else {}
    rec = {k: str(base.get(k) or "") for k in APPROVED_FIELDS if base.get(k)}
    for k, v in (over or {}).items():
        if v:
            rec[k] = parse_not_before(v) if k == "airs" else v
    if not rec.get("what") and not rec.get("title"):
        raise ValueError(f"nothing to say what Ben approved: {src['id']} has no awaits entry; give --what (and --version, --airs)")
    rec["channel"] = (rec.get("channel") or ("HOS" if (src.get("repo") or job.get("repo")) == "hos" else "OWB")).upper()
    rec.setdefault("number", str(src.get("film") or job.get("film") or ""))
    rec["job"] = src["id"]
    if len(items) > 1 and entry:
        rec["askId"] = f"{src['id']}.{entry}"  # video_tracker.ask_entries' id for that cut (its Play link is reused)
    rec["okAt"] = parse_not_before(ok_at) if ok_at else studio.iso(at)
    if ref:
        rec["okRef"] = ref
    job["approved_from"] = rec
    if src.get("awaits_ben"):
        if len(items) > 1 and entry:
            rest = [x for i, x in enumerate(items, 1) if i != entry]
            src["awaits_ben"] = rest[0] if len(rest) == 1 else rest
        else:
            src["awaits_was"] = src.pop("awaits_ben")
        log(src, at, agent, "no longer waits on Ben" + (f" (entry {entry})" if entry else "") + f": OK'd, delivered by {job['id']}")
    log(job, at, agent, f"approved by Ben: {rec.get('what') or rec.get('title')}" + (f" {rec['version']}" if rec.get("version") else "")
        + (f" (asked in {src['id']})" if src is not job else ""))


def do_cancel(job: dict, agent: str, note: str, at: dt.datetime) -> None:
    require_chief(job,agent,at)
    if job["status"] == "done":
        raise ValueError(f"{job['id']} is already done")
    job.update(status="cancelled", by="", eta="")
    log(job, at, agent, "cancelled" + (": " + note if note else ""))


# ----------------------------------------------------------------------------- board link (film/stage claims)
def on_board(job: dict) -> bool:
    """Only OWB jobs have a film folder on this repo's studio board; HOS films live in the HOS checkout."""
    return bool(job.get("film")) and job.get("repo", "owb") != "hos"


def board_claim(job: dict, agent: str, at: dt.datetime) -> str | None:
    if not on_board(job):
        return None
    path = studio.film_dir(studio.FILMS, job["film"]) / "status.json"
    d = studio.load(path)
    mins = max(1, int((studio.parse(job["eta"]) - at).total_seconds() // 60))
    err = studio.do_claim(d, job["stage"], agent, mins, f"{job['id']} {job['title']}", at)
    if err:
        return err
    studio.save(path, d)
    return None


def board_release(job: dict, agent: str, state: str, ref: str = "") -> None:
    if not on_board(job):
        return
    path = studio.film_dir(studio.FILMS, job["film"]) / "status.json"
    d = studio.load(path)
    if any(c["stage"] == job["stage"] and c["by"] == agent for c in d.get("claims", [])):
        studio.do_release(d, job["stage"], agent, state, ref)
        studio.save(path, d)


# ----------------------------------------------------------------------------- JOBS.md
def render(data: dict, at: dt.datetime) -> str:
    L = ["# Studio job queue", "", "Generated by `python3 scripts/jobs.py` from `jobs/queue.json`. Don't edit by hand.",
         "Any agent able to do a job may claim it: `jobs.py next --agent <you> --can <what you can do>`.", ""]
    if data.get("focus"):
        L += [f"**Focus film: {', '.join(data['focus'])}.** Its jobs go first (Ben, 8 Oct: one film at a time).", ""]
    urgent = [j["id"] for j in sorted(data["jobs"], key=lambda j: (urgent_rank(j), j["id"]))
              if j.get("urgent") and j["status"] in ("open", "claimed", "blocked")]
    if urgent:
        L += [f"**Urgent, in this order: {', '.join(urgent)}.** After recorded deadlines, before other ready work.", ""]
    L += [
         "| Job | Needs | Status | Who | ETA (UTC) | Title | Ref |", "|---|---|---|---|---|---|---|"]
    live = [j for j in data["jobs"] if j["status"] in ("open", "claimed", "blocked")]
    for j in sorted(live, key=lambda j: j["id"]):
        st = "**stalled**" if stalled(j, at) else j["status"] + (f" (after {j['after']})" if j.get("after") and j["status"] == "open" else "")
        film = f"{j['film']} {j['stage']} · " if j.get("film") else ""
        film += f"for {j['for']} · " if j.get("for") else ""
        film += f"{j['kind']} · " if j.get("kind") else ""
        film += f"`{j['model']}` · " if j.get("model") else ""
        L.append(f"| {j['id']} | {j['needs']} | {st} | {j.get('by') or '–'} | {j.get('eta') or '–'} | {film}{j['title']} | {j.get('ref') or ''} |")
    if not live:
        L.append("| – | | nothing waiting | | | | |")
    done = [j for j in data["jobs"] if j["status"] in ("done", "cancelled")][-10:]
    if done:
        L += ["", "Recently finished:", ""] + [f"- {j['id']} {j['status']}: {j['title']} ({j.get('result') or ''})" for j in reversed(done)]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- git transaction
def with_git(apply, message: str, tries: int = 3):
    """Pull, apply, commit only the queue files and any touched film board files, push; retry on a push race."""
    for _ in range(tries):
        if studio.git("pull", "-q", "--rebase", "--autostash", "origin", "main").returncode != 0:
            return None, "git pull failed; resolve the working tree first"
        data = load()
        before = json.dumps(data, sort_keys=True)
        out, err, touched = apply(data)
        if err:
            return None, err
        if json.dumps(data, sort_keys=True) == before and not touched:
            return out, None  # nothing changed (e.g. `next` with nothing waiting): no commit, no push
        save(data)
        JOBS_MD.write_text(render(data, now()))
        paths = [str(QUEUE), str(JOBS_MD)]
        if touched:
            studio.write_status(studio.FILMS)
            paths += [str(p) for p in touched] + [str(studio.status_path(studio.FILMS))]
        studio.git("add", *paths)
        if studio.git("commit", "-q", "-m", message, "--", *paths).returncode != 0:
            return None, "git commit failed"
        if studio.git("push", "-q", "origin", "HEAD:main").returncode == 0:
            return out, None
        studio.git("reset", "-q", "HEAD~1")
        studio.git("checkout", "-q", "--", *paths)
    return None, "push kept racing; try again"


def film_status_path(job: dict):
    return studio.film_dir(studio.FILMS, job["film"]) / "status.json" if on_board(job) else None


def show(job: dict) -> str:
    who = (f" by {job['by']}" if job.get("by") else "") + (f" until {job['eta']}" if job.get("eta") else "")
    lines = [f"{job['id']} [{job['needs']}] {job['status']}{who}",
             f"title: {job['title']}"]
    if job.get("film"):
        lines.append(f"board: {job['film']} {job['stage']}")
    if job.get("kind") or job.get("model"):
        r = routing.KINDS.get(job.get("kind") or "")
        fb = routing.fallbacks(job["kind"]) if r else []
        lines.append(f"kind: {job.get('kind') or '-'}" + (f" (primary {r[1][0]} {r[1][1]}" + (
            ", then " + " -> ".join(f"{a} {m}" for a, m in fb) + ")" if fb else ", no stand-in)") if r else "")
                     + (f"; model: {job['model']}" if job.get("model") else ""))
    if job.get("not_before"):
        lines.append(f"not before: {studio.parse(job['not_before']).astimezone(LONDON):%Y-%m-%d %H:%M} London ({job['not_before']})")
    if job.get("ref"):
        lines.append(f"ref: {job['ref']}")
    if job.get("body"):
        lines += ["", job["body"]]
    return "\n".join(lines)


def heartbeat(agent: str) -> None:
    """On the Mini, tell the Chief relay this agent is alive (chief_relay.py: Grok Bot counts as up while it runs jobs.py).
    A no-op anywhere without ~/_desk/state, e.g. cloud sessions."""
    if agent and chief_relay.STATE.is_dir():
        try:
            chief_relay.seen(agent)
        except OSError:
            pass


def publish_board() -> None:
    """Rebuild the Studio Kanban's data in the background (scripts/board_publish.py, Ben 9 Oct: the board updates
    whenever a job moves). Fire-and-forget: it never blocks the job or changes its exit code. Off with BOARD_PUBLISH=0,
    and a no-op anywhere without ~/_desk/state (cloud sessions, CI)."""
    script = ROOT / "scripts" / "board_publish.py"
    if os.environ.get("BOARD_PUBLISH", "1") == "0" or not chief_relay.STATE.is_dir() or not script.exists():
        return
    try:
        subprocess.Popen([sys.executable, str(script), "--quiet"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True, cwd=str(ROOT))
    except OSError:
        pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--needs", required=True, choices=NEEDS)
    a.add_argument("--body", default="")
    a.add_argument("--body-file", type=pathlib.Path)
    a.add_argument("--ref", default="")
    a.add_argument("--film", default="")
    a.add_argument("--stage", default="")
    a.add_argument("--after", default="")
    a.add_argument("--repo", default="owb", choices=["owb", "hos"])
    a.add_argument("--eta", type=int, default=DEFAULT_ETA, help="minutes a claim lasts before it counts as stalled")
    a.add_argument("--by", required=True)
    a.add_argument("--for", dest="for_agent", default="", help="only this agent may claim it, e.g. codex; the relay wakes it")
    a.add_argument("--kind", default="", choices=[""] + list(routing.KINDS), help="job type; routes it (AGENTS.md 'Who does what')")
    a.add_argument("--model", default="", choices=[""] + list(routing.MODELS), help="override the kind's model")
    a.add_argument("--action", default="", help="plain-English action still unfinished")
    a.add_argument("--due", default="", help="deadline, ISO or YYYY-MM-DD HH:MM London; does not defer start")
    a.add_argument("--not-before", default="", help="deprecated: use a structured wait condition and check-at")
    a.add_argument("--reset", default="", help="deprecated compatibility argument")
    a.add_argument("--approved-from", dest="approved_from", default="",
                   help="this job delivers a cut Ben OK'd that job asked about (awaits_ben), e.g. J0924; see `approved`")
    a.add_argument("--entry", type=int, default=0, help="with --approved-from: which cut, when it asked about several")
    rc = sub.add_parser("reconcile", help="block broken dependencies and queue deduplicated Chief resolutions")
    rc.add_argument("--agent", default="relay")
    due = sub.add_parser("due", help="set or clear a deadline without changing eligibility")
    due.add_argument("id")
    due.add_argument("--due", required=True)
    due.add_argument("--agent", required=True)
    md = sub.add_parser("metadata", help="set explicit remaining actions and structured holds without releasing work")
    md.add_argument("--file", type=pathlib.Path, required=True)
    md.add_argument("--agent", required=True)
    wt = sub.add_parser("wait", help="record a condition and verification time; never auto-release a hold")
    wt.add_argument("id")
    wt.add_argument("--agent", required=True)
    wt.add_argument("--condition", required=True)
    wt.add_argument("--check-at", required=True)
    wt.add_argument("--type", dest="hold_type", default="input", choices=["input","public","credits","test","dependency","date","ben"])
    wt.add_argument("--action", default="")
    wt.add_argument("--recheck", default="", help="verification task whose condition check this records")
    n = sub.add_parser("next")
    n.add_argument("--agent", required=True)
    n.add_argument("--can", required=True, help="comma list from: " + ",".join(NEEDS))
    n.add_argument("--eta", type=int, default=None)
    n.add_argument("--id", default="", help="claim only this actionable job; preserve role, hold and existing-claim checks")
    n.add_argument("--peek", action="store_true", help="show what you would get, claim nothing")
    for name in ("done", "block", "release", "renew", "reopen", "cancel", "show", "progress", "reroute", "handback"):
        p = sub.add_parser(name)
        p.add_argument("id")
        p.add_argument("--agent", default="")
        p.add_argument("--result", default="")
        p.add_argument("--reason", default="")
        p.add_argument("--note", default="")
        p.add_argument("--ref", default="")
        p.add_argument("--eta", type=int, default=DEFAULT_ETA)
        if name == "progress":
            p.add_argument("--step", type=int, required=True, help="steps finished so far (0 at the start)")
            p.add_argument("--of", type=int, required=True, help="steps in the whole job")
            p.add_argument("--action", default=None, help="plain-English action still unfinished; update when the remaining work changes")
            p.add_argument("--films", default=None, help="video(s) this job advances, e.g. HOS:006 or OWB:028,OWB:029")
        if name == "reroute":
            p.add_argument("--to", required=True, choices=list(routing.MINI_WORKERS), help="the Mini worker that takes it")
            p.add_argument("--model", default="", choices=[""] + list(routing.MODELS), help="model it runs on there")
    aw = sub.add_parser("awaits", help="mark a job as waiting on Ben's OK/watch: a Ready for OK card with Play + deadline")
    aw.add_argument("id")
    aw.add_argument("--agent", default="")
    aw.add_argument("--what", default="", help="what Ben is OKing, in plain words, e.g. 'swap the 027 Short to v05'")
    aw.add_argument("--file", default="", help="the cut to play: iCloud path from CloudDocs ('OWB UAT/...mp4'), or absolute")
    aw.add_argument("--version", default="", help="the cut's version, e.g. v05 (Ben's tick is matched on it)")
    aw.add_argument("--due", default="", help='"YYYY-MM-DD HH:MM" London: Ben\'s OK is needed by then')
    aw.add_argument("--airs", default="", help='"YYYY-MM-DD HH:MM" London: when it airs, if scheduled')
    aw.add_argument("--if-not", dest="if_not", default="", help="what happens with no OK by the deadline")
    aw.add_argument("--card", default="", help="an existing board card to move, e.g. HOS:007 (longs); else a new card")
    aw.add_argument("--title", default="", help="card title (new cards)")
    aw.add_argument("--number", default="", help="film number or S2 etc. shown on the card")
    aw.add_argument("--type", dest="vtype", default="", choices=["", "long", "short"])
    aw.add_argument("--add", action="store_true", help="add another cut to this job's list instead of replacing it")
    aw.add_argument("--clear", action="store_true", help="the job no longer waits on Ben")
    aw.add_argument("--ok", action="store_true", help="with --clear: Ben OK'd it and this job now delivers it (as `approved`); "
                    "the default when the job is still open/claimed/blocked")
    aw.add_argument("--dropped", action="store_true", help="with --clear: the hold was dropped (no OK), so nothing goes to "
                    "the board's Approved, on its way lane")
    ap_ = sub.add_parser("approved", help="Ben OK'd a cut: this job delivers it (board lane \"Approved, on its way\")")
    ap_.add_argument("id", help="the follow-on job (swap / package / upload), e.g. J0945")
    ap_.add_argument("--from", dest="from_job", default="", help="the job that asked Ben (awaits_ben), e.g. J0924; default: this job")
    ap_.add_argument("--entry", type=int, default=0, help="which cut, when that job asked about several (1-based)")
    ap_.add_argument("--ok-at", dest="ok_at", default="", help='"YYYY-MM-DD HH:MM" London: when Ben OK\'d (default now)')
    ap_.add_argument("--ref", default="", help="where Ben said it (comment id)")
    ap_.add_argument("--agent", default="")
    for f_ in ("what", "file", "version", "airs", "card", "title", "number"):
        ap_.add_argument(f"--{f_}", default="", help="override / fill in the approved cut's " + f_)
    ap_.add_argument("--type", dest="vtype", default="", choices=["", "long", "short"])
    w = sub.add_parser("watch", help="JSON for Claude's 2-hourly check: is the Mini quiet, what waits on Ben")
    w.add_argument("--quiet-hours", type=float, default=3)
    fo = sub.add_parser("focus", help="the film(s) every agent works on first, e.g. `focus 025`; no films clears it")
    fo.add_argument("films", nargs="*")
    fo.add_argument("--by", default="claude")
    ur = sub.add_parser("urgent", help="put job(s) ahead of everything, even the focus film, in the order named, after any "
                        "other urgent jobs, e.g. `urgent J0085 J0096`; --off undoes it")
    ur.add_argument("ids", nargs="+")
    ur.add_argument("--off", action="store_true")
    ur.add_argument("--by", default="claude")
    lst = sub.add_parser("list")
    lst.add_argument("--all", action="store_true")
    for p in sub.choices.values():
        p.add_argument("--git", action="store_true")
    args = ap.parse_args(argv)
    at = now()
    heartbeat(getattr(args, "agent", ""))

    if args.cmd == "list":
        data = load()
        for j in data["jobs"]:
            if args.all or j["status"] in ("open", "claimed", "blocked"):
                print(f"{j['id']} [{j['needs']}] {'stalled' if stalled(j, at) else j['status']}"
                      f"{' by ' + j['by'] if j.get('by') else ''}  {j['title']}")
        return 0
    if args.cmd == "watch":
        print(json.dumps(do_watch(load(), at, args.quiet_hours), indent=2))
        return 0
    if args.cmd == "show":
        job = find(load(), args.id)
        if not job:
            sys.exit(f"jobs: no {args.id}")
        print(show(job))
        return 0

    def apply(data):
        touched = []
        try:
            if args.cmd == "metadata":
                apply_metadata(data, json.loads(args.file.read_text()), args.agent, at)
                return {"id":"metadata","title":"Workflow metadata","needs":"any","status":"done","result":"metadata updated","history":[]},None,touched
            if args.cmd == "reconcile":
                changes = reconcile_dependencies(data, at) + reconcile_holds(data, at)
                return {"id": "reconcile", "title": "Dependency reconciliation", "needs": "any", "status": "done", "result": ", ".join(changes), "history": []}, None, touched
            if args.cmd == "add":
                body = args.body_file.read_text() if args.body_file else args.body
                if not args.film and film_named(args.title):
                    print(f"jobs: warning: '{args.title[:60]}' names a film but has no --film/--stage, so the board "
                          "won't move that film's stage when it's done (J0814)", file=sys.stderr)
                job = do_add(data, title=args.title, needs=args.needs, body=body, by=args.by, at=at, ref=args.ref,
                             film=args.film, stage=args.stage, after=args.after, repo=args.repo, eta_min=args.eta,
                             for_agent=args.for_agent, kind=args.kind, model=args.model, not_before=args.not_before, reset=args.reset, due=args.due, action=args.action)
                if args.approved_from:
                    src = find(data, args.approved_from)
                    if not src:
                        return None, f"no {args.approved_from}", touched
                    do_approved(job, src, args.by, at, entry=args.entry, ref=args.ref)
                return job, None, touched
            if args.cmd == "focus":
                data["focus"] = [f.strip() for f in args.films if f.strip()]
                return {"id": "focus", "focus": data["focus"]}, None, touched
            if args.cmd == "urgent":
                found = [find(data, i) for i in args.ids]
                if not all(found):
                    return None, "no " + ", ".join(i for i, j in zip(args.ids, found) if not j), touched
                return {"id": "urgent", "urgent": do_urgent(data, found, args.off)}, None, touched
            if args.cmd == "next":
                can = {c.strip() for c in args.can.split(",") if c.strip()}
                if args.peek:
                    job = choose_next(data,args.agent,can,at,args.id)
                    return job, None, touched
                job = do_next(data, args.agent, can, at, args.eta, args.id)
                if job and on_board(job) and job["history"][-1]["what"].startswith("claimed"):
                    err = board_claim(job, args.agent, at)
                    if err:
                        do_release(job, args.agent, f"board stage held: {err}", at)
                        return None, f"{job['id']}: the board stage is held ({err}); left open", touched
                    touched.append(film_status_path(job))
                return job, None, touched
            job = find(data, args.id)
            if not job:
                return None, f"no {args.id}", touched
            if args.cmd == "due":
                job["due"] = workflow.normalize_due(args.due)
                log(job, at, args.agent, "deadline: " + (job["due"] or "cleared"))
            elif args.cmd == "done":
                if job.get("recheck_of"):
                    parent = find(data,job["recheck_of"])
                    if parent and parent.get("status") == "blocked" and (parent.get("hold") or {}).get("last_recheck") != job["id"]:
                        raise ValueError("Record the condition result on the held job with wait --recheck " + job["id"] + ", or reopen it with evidence, before closing this check")
                do_done(job, args.agent, args.result or "done", at, args.ref)
                board_release(job, args.agent, "review", args.ref)
            elif args.cmd == "block":
                do_block(job, args.agent, args.reason or args.result, at)
                board_release(job, args.agent, "blocked")
            elif args.cmd == "release":
                do_release(job, args.agent, args.note, at)
                board_release(job, args.agent, "doing")
            elif args.cmd == "renew":
                do_renew(job, args.agent, args.eta, at)
                if on_board(job):
                    board_claim(job, args.agent, at)
            elif args.cmd == "progress":
                do_progress(job, args.agent, args.step, args.of, at, args.note, args.films, args.action)
                return job, None, touched  # the film's board stage doesn't change
            elif args.cmd == "reopen":
                do_reopen(job, args.agent or "claude", args.note, at)
            elif args.cmd == "wait":
                if args.recheck and (find(data,args.recheck) or {}).get("recheck_of") != job["id"]:
                    raise ValueError("--recheck must identify this job's Chief verification task")
                set_wait(job, args.agent, at, {"type":args.hold_type,"condition":args.condition,"check_at":args.check_at}, args.action, args.recheck)
            elif args.cmd == "awaits" and args.clear and not args.dropped and job.get("awaits_ben") and (
                    args.ok or job["status"] in ("open", "claimed", "blocked")):
                # Clearing a held job that goes on = Ben OK'd it (Ben, 25 Oct 14:13): it shows in "Approved, on its
                # way" until it's on YouTube. A job that asked about several cuts needs `approved --entry N`.
                raw = job["awaits_ben"]
                if isinstance(raw, list) and len(raw) > 1:
                    return None, (f"{job['id']} asked Ben about {len(raw)} cuts: use `jobs.py approved {job['id']} --entry N`"
                                  " for the one he OK'd, or --dropped"), touched
                do_approved(job, job, args.agent or "chief", at)
            elif args.cmd == "awaits":
                do_awaits(job, args.agent or "chief", at, what=args.what, file=args.file, version=args.version, due=args.due,
                          airs=args.airs, if_not=args.if_not, card=args.card, title=args.title, number=args.number,
                          vtype=args.vtype, add=args.add, clear=args.clear)
            elif args.cmd == "approved":
                src = find(data, args.from_job) if args.from_job else job
                if not src:
                    return None, f"no {args.from_job}", touched
                do_approved(job, src, args.agent or "chief", at, entry=args.entry, ok_at=args.ok_at, ref=args.ref,
                            over={"what": args.what, "file": args.file, "version": args.version, "airs": args.airs,
                                  "card": args.card, "title": args.title, "number": args.number, "type": args.vtype})
            elif args.cmd == "cancel":
                do_cancel(job, args.agent or "claude", args.note, at)
            elif args.cmd == "handback":
                do_handback(job, args.agent or "relay", args.note, at)
            elif args.cmd == "reroute":
                held = job.get("by") if job["status"] == "claimed" else ""
                do_reroute(job, args.agent or "relay", args.to, args.model, args.note, at)
                if held:
                    board_release(job, held, "doing")
            if on_board(job):
                touched.append(film_status_path(job))
            return job, None, touched
        except ValueError as e:
            return None, str(e), touched

    if args.git and not (args.cmd == "next" and args.peek):
        who = getattr(args, "agent", "") or getattr(args, "by", "")
        what = " ".join(x for x in ("jobs:", args.cmd, " ".join(getattr(args, "ids", [])) or getattr(args, "id", "") or (args.title if args.cmd == "add" else ""), "by", who) if x)
        job, err = with_git(apply, what)
    else:
        data = load()
        job, err, touched = apply(data)
        if not err and not (args.cmd == "next" and args.peek):
            save(data)
            JOBS_MD.write_text(render(data, at))
            if touched:  # the film's status.json was written by board_claim / board_release
                studio.write_status(studio.FILMS)
    if err:
        print(f"jobs: {err}", file=sys.stderr)
        return 1
    if job and not (args.cmd == "next" and args.peek):
        publish_board()
    if args.cmd == "next" and not job:
        print("jobs: nothing waiting for you")
        return EX_NONE
    if args.cmd == "focus":
        print("focus: " + (", ".join(job["focus"]) or "none"))
        return 0
    if args.cmd == "urgent":
        print("urgent: " + (", ".join(job["urgent"]) or "none"))
        return 0
    print(job.get("result") or "no dependency changes" if args.cmd in ("reconcile","metadata") else show(job) if job else "ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
