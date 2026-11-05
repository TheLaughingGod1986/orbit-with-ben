#!/usr/bin/env python3
"""Queue forecast for the board (Ben, 5 Nov 2026: "I need information in the workflow board that it's waiting for this
particular agent to be free, number 4 in the queue or something like that ... a time and schedule that it will be free").

board_publish.py calls `section(queue, mini_hb, macbook_hb, at)` on every publish. It walks the ready jobs in the
queue's own order and hands each one to whichever agent that can take it is free soonest, like the relay does. For
every queued job the board then shows who it is waiting for, its place in that agent's line and roughly when it starts;
for every agent, what it is on now and when it is free.

It is an estimate: how long a job takes is each agent's pace over the last 24 h (jobs finished per hour). Reads only; never
fails the publish.
"""
import datetime as dt
import re
import json
import pathlib

import jobs
import routing
import workflow_state as workflow

DEFAULT_MIN, MIN_MIN, MAX_MIN = 45, 10, 150
PACE = dt.timedelta(hours=24)
CLOUD_EVERY = 60          # Claude's cloud run is hourly at :50
MACBOOK_FRESH = dt.timedelta(minutes=40)
CAN = {"cursor": {"mini", "any"}, "codex": {"mini", "any"}, "gemini": {"mini", "any", "gemini"},
       "macbook": {"macbook", "any"}, "claude": {"cloud", "any"}}
MACHINE = {"cursor": "mini", "codex": "mini", "gemini": "mini", "macbook": "macbook", "claude": "cloud"}
MAX_FORECAST = 80         # jobs; beyond that the times mean nothing


def _t(s):
    try:
        t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def _iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def durations(queue: dict, at: dt.datetime) -> dict:
    """{agent: minutes per job} from its real pace: the last 24 h divided by the jobs it finished in them, clamped.
    (Claim-to-done times read far too short: a job is claimed again on every run, so only its last stretch shows.)"""
    done = {}
    for j in queue.get("jobs") or []:
        if j.get("status") != "done":
            continue
        for h in reversed(j.get("history") or []):
            if str(h.get("what", "")).startswith("done"):
                when = _t(h.get("at"))
                if when and at - when <= PACE:
                    done[str(h.get("by") or "")] = done.get(str(h.get("by") or ""), 0) + 1
                break
    return {a: max(MIN_MIN, min(MAX_MIN, PACE.total_seconds() / 60 / n)) for a, n in done.items() if n}


def _flags() -> dict:
    try:
        return json.loads((pathlib.Path(__file__).resolve().parent / "credit_flags.json").read_text()).get("flags") or {}
    except (OSError, ValueError, AttributeError):
        return {}


def agents_up(mini_hb: dict | None, macbook_hb: dict | None, at: dt.datetime) -> dict:
    """{agent: why it is down or ''}: the Mini's own chain, the MacBook's heartbeat, and Claude's hourly run."""
    out = {}
    flags = _flags()
    rows = {r.get("agent"): r for r in (mini_hb or {}).get("chain") or [] if isinstance(r, dict)}
    for a in routing.MINI_WORKERS:
        r = rows.get(a)
        why = "" if r and r.get("up") else str((r or {}).get("why") or "")
        flag = (flags.get(a) or {}) if not (r and r.get("up")) else {}
        if not why and flag.get("out_until") and (_t(flag["out_until"]) or at) > at:
            why = f"out of credit until {flag['out_until']}" + (f" ({flag.get('reason')})" if flag.get("reason") else "")
        out[a] = (why or ("" if r and r.get("up") else "not in the Mini's chain"))[:120]
    seen = _t((macbook_hb or {}).get("at"))
    why = (macbook_hb or {}).get("why") or []
    why = "; ".join(why) if isinstance(why, list) else str(why)
    # A MacBook waiting on its guards (in use, on battery) takes no job now: say so rather than promise a start.
    out["macbook"] = ("no MacBook heartbeat in 40 min" if not (seen and at - seen <= MACBOOK_FRESH) else
                      why[:120] if (macbook_hb or {}).get("state") == "waiting" and why else "")
    # Cloud Claude: down when the relay has it down (e.g. a missed Chief inbox), else up.
    r = rows.get("claude")
    out["claude"] = str(r.get("why") or "marked down by the relay")[:120] if r and not r.get("up") else ""
    return out


def _who_can(job: dict, up: dict) -> list:
    need, only = job.get("needs") or "any", job.get("for") or ""
    names = [a for a in CAN if need in CAN[a] and not up.get(a)]
    if only:
        names = [a for a in names if a == only]
    return names


def _next_cloud_run(t: dt.datetime) -> dt.datetime:
    nxt = t.replace(minute=50, second=0, microsecond=0)
    return nxt if nxt >= t else nxt + dt.timedelta(minutes=CLOUD_EVERY)


def section(queue: dict, mini_hb: dict | None, macbook_hb: dict | None, at: dt.datetime) -> dict:
    up = agents_up(mini_hb, macbook_hb, at)
    took = durations(queue, at)
    est = {a: dt.timedelta(minutes=took.get(a, DEFAULT_MIN)) for a in CAN}
    lanes = {a: {"agent": a, "machine": MACHINE[a], "up": not up[a], "why": up[a], "now": "", "freeAt": _iso(at),
                 "queued": 0, "minutesPerJob": round(est[a].total_seconds() / 60)} for a in CAN}
    free = {a: at for a in CAN}
    for j in queue.get("jobs") or []:
        a = str(j.get("by") or "")
        if j.get("status") != "claimed" or a not in lanes:
            continue
        since = _t(j.get("since")) or at
        lease = _t(j.get("eta"))
        # A claim usually ends well before its lease: expect the agent's usual time, never sooner than 10 min from now.
        end = max(at + dt.timedelta(minutes=MIN_MIN), min(since + est[a], lease or since + est[a]))
        free[a] = max(free[a], end)
        lanes[a]["now"] = j.get("id") or ""
    # The Mini's own heartbeat names the job it just woke a worker for, before that claim reaches the queue.
    woke = re.match(r"woke (\w+) for (J\d+)", str((mini_hb or {}).get("note") or ""))
    hb_at = _t((mini_hb or {}).get("at"))
    if woke and (mini_hb or {}).get("state") == "running" and hb_at and at - hb_at <= dt.timedelta(minutes=26):
        a = woke.group(1).lower()
        if a in lanes and not lanes[a]["now"]:
            lanes[a]["now"] = woke.group(2)
            free[a] = max(free[a], hb_at + est[a], at + dt.timedelta(minutes=MIN_MIN))
    if (macbook_hb or {}).get("job"):
        lanes["macbook"]["now"] = lanes["macbook"]["now"] or str(macbook_hb["job"])
        free["macbook"] = max(free["macbook"], at + dt.timedelta(minutes=MIN_MIN))
    free["claude"] = max(free["claude"], _next_cloud_run(at))
    for a in lanes:
        lanes[a]["freeAt"] = _iso(free[a])  # when its current job should end (or now)
    forecast, nobody = {}, {}
    import chief_relay
    caps = chief_relay.worker_capabilities()
    for j in jobs.ordered(queue, at):
        if len(forecast) >= MAX_FORECAST:
            break
        if j.get("status") != "open":
            continue
        names = [a for a in _who_can(j, up) if jobs.claimable(queue, j, CAN[a], at, a)]
        if not names:
            if not workflow.external_hold(j, at) and not (j.get("after") and
                                                           (jobs.find(queue, j["after"]) or {}).get("status") != "done"):
                only = j.get("for") or ""
                cap = next((workflow.capability_problem(j, a, at, caps) for a in _who_can(j, up)
                            if workflow.capability_problem(j, a, at, caps)), "")
                nobody[j["id"]] = cap[:140] if cap else ( (f"waiting for {only}: {up[only]}" if only in up and up[only] else
                                   f"waiting for {only}" if only else
                                   f"no agent that takes '{j.get('needs') or 'any'}' jobs is up"))
            continue
        a = min(names, key=lambda n: (free[n], names.index(n)))
        lanes[a]["queued"] += 1
        start = free[a] if a != "claude" else _next_cloud_run(free[a])
        forecast[j["id"]] = {"agent": a, "pos": lanes[a]["queued"], "startAt": _iso(start)}
        free[a] = start + est[a]
    for a in lanes:
        lanes[a]["clearAt"] = _iso(free[a])  # when its whole line should be done
    return {"at": _iso(at), "agents": list(lanes.values()), "jobs": forecast, "noAgent": nobody,
            "note": "Estimate from each agent's pace over the last 24 h."}
