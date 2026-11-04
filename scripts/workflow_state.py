"""Pure studio activity, dependency and dispatch calculations. No disk/network access."""
from __future__ import annotations
import datetime as dt
import re
from zoneinfo import ZoneInfo

LIVE = {"open", "claimed", "blocked"}
MINI = {"mini", "gemini", "any"}
STALL_GRACE = dt.timedelta(minutes=45)

def capability_names(value):
    if not value:
        return []
    names = value.split(",") if isinstance(value, str) else value or []
    if not isinstance(names, list) or any(not isinstance(n, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", n.strip()) for n in names):
        raise ValueError("Capabilities must be identifiers such as audio_input")
    return sorted({n.strip() for n in names})

def capability_problem(j, agent, at, capabilities=None):
    """Online is not proof of media input. Explicit requirements fail closed.

    Reports are local, per worker and short lived; neither a model name nor a
    heartbeat supplies a capability. Jobs without requirements keep their rules.
    """
    required = j.get("required_capabilities") or []
    if not required:
        return ""
    report = (capabilities or {}).get(agent) or {}
    checked, expires = timestamp(report.get("at")), timestamp(report.get("expiresAt"))
    fresh = checked and expires and checked <= at < expires and expires-checked <= dt.timedelta(hours=1) and report.get("evidence")
    available = (report.get("available") or []) if fresh else []
    missing = sorted(set(required) - set(available))
    return "Waiting for verified capability: " + ", ".join(missing) if missing else ""

def timestamp(value):
    if not value:
        return None
    try:
        t = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return t.replace(tzinfo=ZoneInfo("Europe/London")) if t.tzinfo is None else t
    except (ValueError, TypeError):
        return None

def normalize_due(value):
    if not str(value or "").strip():
        return ""
    t = timestamp(value)
    if t is None:
        raise ValueError("--due must be an ISO date/time or YYYY-MM-DD HH:MM London")
    return t.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def role_job(j):
    return j.get("kind") == "chief" or j.get("for") == "chief"

def dependency_problem(j, by_id):
    path, cur = [j["id"]], j
    while cur.get("after"):
        parent = cur["after"]
        if parent in path:
            return {"kind": "cycle", "ids": sorted(path[path.index(parent):])}
        path.append(parent)
        if parent not in by_id:
            return {"kind": "missing", "ids": [parent]}
        cur = by_id[parent]
        if cur.get("status") == "done":
            return None
        if cur.get("status") == "cancelled":
            return {"kind": "cancelled", "ids": [parent]}
    return None

def is_review(j):
    return j.get("status") == "blocked" and bool(re.search(
        r"parked for (?:the )?chief|await(?:s|ing)? (?:the )?chief|needs? (?:the )?chief",
        j.get("result") or "", re.I))

def external_hold(j, at):
    if j.get("needs") == "ben" or j.get("awaits_ben"):
        return "Waiting for Ben"
    hold = j.get("hold") or {}
    if hold:
        return hold.get("condition") or "Waiting for condition verification"
    nb = timestamp(j.get("not_before") or j.get("notBefore"))
    if nb and nb > at:
        return "Waiting for recorded date/reset: " + nb.isoformat()
    if j.get("status") == "blocked" and re.search(
        r"wait(?:s|ing)? .*?(?:public|reset|renewal)|date gate|reopen (?:when|on|after)|test.*(?:running|ends?)",
        j.get("result") or "", re.I):
        return j.get("result") or "Waiting for external input"
    return ""

def claim_is_stalled(j, at, execution=None):
    if j.get("status") != "claimed":
        return False
    if execution and execution.get("job") == j.get("id"):
        until = timestamp(execution.get("expiresAt"))
        if until and until > at:
            return False
    stamps = [timestamp(j.get("eta")), timestamp((j.get("progress") or {}).get("at"))]
    latest = max((t for t in stamps if t), default=None)
    return bool(latest and at > latest + STALL_GRACE)

def hold_due(j, by_id, at):
    """A due hold requests verification; it never grants permission to release the work."""
    if j.get("status") != "blocked" or j.get("needs") == "ben" or j.get("awaits_ben") or (j.get("hold") or {}).get("type") == "ben":
        return False
    hold = j.get("hold") or {}
    check = timestamp(hold.get("check_at"))
    if hold.get("type") == "dependency" and not hold.get("last_recheck"):
        if j.get("after") and by_id.get(j["after"],{}).get("status") == "done":
            return True
        # Legacy holds may name their predecessor only in prose. Their recorded check must still run.
        # Verification can repair the graph; it never releases the held production job automatically.
    if check:
        return check <= at
    return bool(j.get("after") and by_id.get(j["after"], {}).get("status") == "done" and not external_hold(j, at))

def starting_execution(j, at, execution=None):
    """Caller supplies a process-validated execution lease, not a heartbeat."""
    if not execution or j.get("status") != "open" or execution.get("job") != j.get("id"):
        return False
    start, end = timestamp(execution.get("startedAt")), timestamp(execution.get("expiresAt"))
    return bool(execution.get("worker") and start and end and start <= at < end)

def state(j, by_id, at, active_review=None, execution=None):
    if j.get("status") not in LIVE:
        return j.get("status") or "unknown"
    if active_review and active_review.get("job") == j.get("id") and timestamp(active_review.get("expiresAt")) and timestamp(active_review["expiresAt"]) > at:
        return "running"
    if external_hold(j,at) or dependency_problem(j,by_id):
        return "waiting"
    if j.get("status") == "open" and starting_execution(j, at, execution):
        if j.get("after") and by_id.get(j["after"], {}).get("status") != "done":
            return "waiting"
        return "starting"
    if j.get("status") == "claimed":
        return "stalled" if claim_is_stalled(j, at, execution) else "running"
    if external_hold(j, at) or dependency_problem(j, by_id):
        return "waiting"
    if is_review(j):
        return "waiting" if j.get("after") and by_id.get(j["after"], {}).get("status") != "done" else "review"
    if j.get("status") == "blocked":
        return "waiting"
    if j.get("after") and by_id.get(j["after"], {}).get("status") != "done":
        return "waiting"
    return "queued"

def reason(j, by_id, at):
    problem = dependency_problem(j, by_id)
    if problem:
        return "Dependency " + problem["kind"] + ": " + ", ".join(problem["ids"]) + "; awaiting Chief resolution"
    if j.get("status") == "blocked":
        return j.get("result") or "Waiting for input"
    held = external_hold(j, at)
    if held:
        return held
    if j.get("after") and by_id.get(j["after"], {}).get("status") != "done":
        return "Waiting for " + j["after"]
    return ""

def deadlines(rows):
    out = {}
    for j in rows:
        if j.get("status") not in LIVE:
            continue
        records = []
        for field in ("approved_from", "awaits_was"):
            value = j.get(field) or {}
            records.extend(value if isinstance(value, list) else [value])
        stamps = [timestamp(j.get("due"))]
        for rec in records:
            if isinstance(rec, dict):
                stamps.extend([timestamp(rec.get("due")), timestamp(rec.get("airs"))])
        valid = [t for t in stamps if t]
        if valid:
            out[j["id"]] = min(valid)
    # A prerequisite inherits the earliest deadline it unblocks. Bounded even for cycles.
    for _ in range(len(rows)):
        changed = False
        for j in rows:
            parent, due = j.get("after"), out.get(j["id"])
            if j.get("status") not in LIVE:
                continue
            if parent and due and (parent not in out or due < out[parent]):
                out[parent] = due
                changed = True
        if not changed:
            break
    return out

def recently_released(j, at):
    last = (j.get("history") or [])[-1:]
    stamp = timestamp(last[0].get("at")) if last else None
    return bool(last and str(last[0].get("what", "")).startswith("released") and stamp
                and at - stamp < dt.timedelta(minutes=30))

def order(j, due, focus=(), at=None):
    at = at or dt.datetime.now(dt.timezone.utc)
    film = j.get("film") or (j.get("handoff") or {}).get("film")
    urgent = j.get("urgent")
    rank = urgent if isinstance(urgent, int) and not isinstance(urgent, bool) else 0
    created = timestamp(j.get("created_at") or j.get("addedAt") or next((h.get("at") for h in j.get("history", []) if h.get("at")), None))
    inf = float("inf")
    # Synthetic one-hour verification deadlines must not outrank actual work.
    # A check for a parent with a real production deadline retains that deadline.
    verification = j.get("recheck_of") if j.get("due_kind") == "condition-verification" else ""
    background = bool(verification and verification not in due)
    deadline = due.get(verification) if verification else due.get(j["id"])
    return (1 if recently_released(j, at) else 0, 1 if background else 0,
            deadline.timestamp() if deadline else inf,
            0 if urgent else 1, rank if urgent else 0,
            1 if j.get("backlog") or re.search(r"^Backlog|weekly .*audit|QA sweep|listing check.*live", j.get("title", ""), re.I) else 0,
            0 if film in focus and film else 1,
            0 if film else 1, 0 if (j.get("eta_min") or 120) <= 60 else 1,
            created.timestamp() if created else inf, j["id"])

def claimable(j, rows, at, agent, chief, can=MINI, execution=None, capabilities=None):
    if not str(agent or "").strip():
        return False
    # Capacity reservations precede launch. Ordinary `next` cannot consume one:
    # the future launcher must verify its token/host/inputs inside the same queue
    # transaction before handing it to the existing claim and stage machinery.
    def reserved(row):
        value = row.get("dispatch_reservation") or {}
        start, end = timestamp(value.get("at")), timestamp(value.get("expiresAt"))
        return bool(start and end and start <= at < end)
    if reserved(j):
        return False
    stage = (j.get("repo", "owb"), j.get("film"), j.get("stage"))
    if stage[1] and stage[2] and any(
            r.get("id") != j.get("id") and reserved(r)
            and (r.get("repo", "owb"), r.get("film"), r.get("stage")) == stage for r in rows):
        return False
    by_id = {r["id"]: r for r in rows}
    if external_hold(j, at) or dependency_problem(j, by_id) or capability_problem(j, agent, at, capabilities):
        return False
    if role_job(j):
        if not chief or agent != chief:
            return False
    elif j.get("needs") not in can or (j.get("for") and j.get("for") != agent):
        return False
    if j.get("status") not in ("open", "claimed"):
        return False
    if starting_execution(j, at, execution) and execution.get("worker") != agent:
        return False
    if j.get("status") == "claimed" and state(j, by_id, at, execution=execution) != "stalled":
        return False
    return not j.get("after") or by_id.get(j["after"], {}).get("status") == "done"

def yieldable_monthly_claim(j):
    return (j.get("status") == "claimed" and j.get("needs") == "mini" and j.get("kind") == "review"
            and str(j.get("backlog", "")).startswith("monthly-improvement-") and not j.get("film") and not j.get("stage")
            and not j.get("hold") and not j.get("awaits_ben"))

def immediate_dispatch(rows, at, chief, workers, actors, choose_worker, exclude=(), execution=None, focus=(), capabilities=None):
    """Honor explicit user claim requests at a safe dispatch boundary.

    Never interrupt an execution lease or give a worker a second claimed job.
    A green worker is eligible here only through the existing routing/claim gates.
    """
    if execution and timestamp(execution.get("expiresAt")) and timestamp(execution["expiresAt"]) > at:
        return None
    owned = [j for j in rows if j.get("status") == "claimed" and j.get("by") in actors]
    # Only unmapped monthly analysis can yield automatically; media/stage claims keep ownership.
    if any(not yieldable_monthly_claim(j) for j in owned):
        return None
    occupied = {j.get("by") for j in rows if j.get("status") == "claimed"}
    free = set(actors) - occupied
    by_id, due = {j["id"]: j for j in rows}, deadlines(rows)
    picks = []
    for j in rows:
        requested = timestamp(j.get("due"))
        if (j["id"] in exclude or j.get("status") != "open" or not j.get("urgent")
                or j.get("due_kind") != "user-immediate-claim" or not requested or requested > at):
            continue
        if external_hold(j, at) or dependency_problem(j, by_id):
            continue
        if role_job(j):
            worker = chief if chief in free and claimable(j, rows, at, chief, chief, execution=execution, capabilities=capabilities) else None
        else:
            eligible = {a for a in free & set(workers) if claimable(j, rows, at, a, chief, execution=execution, capabilities=capabilities)}
            worker = choose_worker(j, eligible) if eligible else None
            if worker not in eligible:
                worker = None
        if worker:
            mode = "chief-inbox" if worker == chief and chief not in workers else "job"
            picks.append((order(j, due, focus, at), {"job":j, "worker":worker, "mode":mode,
                "yield_monthly":[{"id":old["id"], "by":old.get("by")} for old in owned]}))
    return min(picks, key=lambda x:x[0])[1] if picks else None

def select_dispatch(data, at, chief, workers, choose_worker, review_ids=None, exclude=(), execution=None, include_chief=False, capabilities=None):
    actors = set(workers) | ({chief} if chief and include_chief else set())
    rows = data.get("jobs", [])
    by_id, due = {j["id"]: j for j in rows}, deadlines(rows)
    candidates = []
    requested = immediate_dispatch(rows, at, chief, workers, actors, choose_worker, exclude, execution, data.get("focus") or (), capabilities)
    if requested:
        return requested
    # Ordinary deadlines retain resume-first behavior; explicit user requests above only use free workers.
    for j in rows:
        if j["id"] not in exclude and j.get("by") in actors and j.get("status") == "claimed" and state(j, by_id, at, execution=execution) in {"running","stalled"} and (not role_job(j) or j.get("by") == chief) and not external_hold(j,at) and not dependency_problem(j,by_id) and not capability_problem(j,j.get("by"),at,capabilities):
            return {"job": j, "worker": j["by"], "mode": "job"}
    occupied = {j.get("by") for j in rows if j.get("status") == "claimed"}
    free = set(workers) - occupied
    for j in rows:
        if j["id"] in exclude or external_hold(j, at) or dependency_problem(j, by_id):
            continue
        review = is_review(j)
        if review and state(j, by_id, at) != "review":
            continue
        if review:
            if chief not in actors or chief in occupied or (review_ids is not None and j["id"] not in review_ids):
                continue
            worker = chief
            if capability_problem(j, worker, at, capabilities):
                continue
        else:
            if role_job(j):
                worker = chief if chief in actors and chief not in occupied else None
            elif j.get("for"):
                worker = j["for"] if j["for"] in free else None
            else:
                eligible = {a for a in free if claimable(j, rows, at, a, chief, execution=execution, capabilities=capabilities)}
                worker = choose_worker(j, eligible) if eligible else None
                if worker not in eligible:
                    worker = None
            if not worker or not claimable(j, rows, at, worker, chief, execution=execution, capabilities=capabilities):
                continue
        candidates.append((order(j, due, data.get("focus") or (), at), {"job": j, "worker": worker, "mode": "chief-inbox" if worker == chief and chief not in workers else "review" if review else "job"}))
    return min(candidates, key=lambda p: p[0])[1] if candidates else None

def snapshot(data, at, chief, workers, choose_worker, active_review=None, review_ids=None, execution=None, include_chief=False, capabilities=None):
    actors = set(workers) | ({chief} if chief and include_chief else set())
    rows = data.get("jobs", [])
    by_id = {j["id"]: j for j in rows}
    states = {j["id"]: {"state": state(j, by_id, at, active_review, execution), "reason": reason(j, by_id, at)} for j in rows if j.get("status") in LIVE}
    active = [{"id": j["id"], "title": j.get("title", ""), "worker": j.get("by"), "mode": "job", "progress": j.get("progress")} for j in rows if j.get("status") == "claimed" and states.get(j["id"], {}).get("state") == "running"]
    for j in rows:
        if states.get(j["id"], {}).get("state") == "starting":
            states[j["id"]]["reason"] = "Worker launched; task claim pending"
            active.append({"id":j["id"], "title":j.get("title", ""), "worker":execution["worker"],
                           "mode":"starting", "phase":"starting", "startedAt":execution["startedAt"],
                           "expiresAt":execution["expiresAt"]})
    if active_review and states.get(active_review.get("job"), {}).get("state") == "running":
        active = [a for a in active if a["id"] != active_review["job"]]
        active.append({**active_review, "id": active_review["job"], "worker": active_review.get("agent"), "mode": "review"})
    pick = select_dispatch(data, at, chief, workers, choose_worker, review_ids, exclude=[a["id"] for a in active], execution=execution, include_chief=include_chief, capabilities=capabilities)
    counts = {k: sum(s["state"] == k for s in states.values()) for k in ("running", "starting", "queued", "review", "waiting", "stalled")}
    # Unavailable workers are waiting, not ready to run.
    for j in rows:
        if states.get(j["id"], {}).get("state") == "queued":
            eligible = {a for a in actors if claimable(j, rows, at, a, chief, execution=execution, capabilities=capabilities)}
            if not eligible:
                required = j.get("required_capabilities") or []
                why = "Waiting for an available eligible worker"
                if required:
                    why += " with verified capability: " + ", ".join(required)
                states[j["id"]] = {"state": "waiting", "reason": why}
                counts["queued"] -= 1
                counts["waiting"] += 1
    return {"version": 1, "at": at.isoformat(), "active": active,
            "next": ({**pick["job"], "worker": pick["worker"], "mode": pick["mode"]} if pick else None),
            "states": states, "counts": counts}
