"""Pure studio activity, dependency and dispatch calculations. No disk/network access."""
from __future__ import annotations
import datetime as dt
import re
from zoneinfo import ZoneInfo

LIVE = {"open", "claimed", "blocked"}
MINI = {"mini", "gemini", "any"}

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
    nb = timestamp(j.get("not_before") or j.get("notBefore"))
    if nb and nb > at:
        return "Waiting for recorded date/reset: " + nb.isoformat()
    if j.get("status") == "blocked" and re.search(
        r"wait(?:s|ing)? .*?(?:public|reset|renewal)|date gate|reopen (?:when|on|after)|test.*(?:running|ends?)",
        j.get("result") or "", re.I):
        return j.get("result") or "Waiting for external input"
    return ""

def state(j, by_id, at, active_review=None):
    if j.get("status") not in LIVE:
        return j.get("status") or "unknown"
    if active_review and active_review.get("job") == j.get("id") and timestamp(active_review.get("expiresAt")) and timestamp(active_review["expiresAt"]) > at:
        return "running"
    if j.get("status") == "claimed":
        eta = timestamp(j.get("eta"))
        return "stalled" if eta and eta < at else "running"
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
    urgent = j.get("urgent")
    rank = urgent if isinstance(urgent, int) and not isinstance(urgent, bool) else 0
    created = timestamp(j.get("created_at") or j.get("addedAt") or next((h.get("at") for h in j.get("history", []) if h.get("at")), None))
    inf = float("inf")
    return (due.get(j["id"]).timestamp() if j["id"] in due else inf,
            1 if recently_released(j, at) else 0,
            0 if urgent else 1, rank if urgent else 0,
            1 if j.get("backlog") or re.search(r"^Backlog|weekly .*audit|QA sweep|listing check.*live", j.get("title", ""), re.I) else 0,
            0 if j.get("film") in focus and j.get("film") else 1,
            0 if j.get("film") else 1, 0 if (j.get("eta_min") or 120) <= 60 else 1,
            created.timestamp() if created else inf, j["id"])

def claimable(j, rows, at, agent, chief, can=MINI):
    by_id = {r["id"]: r for r in rows}
    if external_hold(j, at) or dependency_problem(j, by_id):
        return False
    if role_job(j):
        if agent != chief:
            return False
    elif j.get("needs") not in can or (j.get("for") and j.get("for") != agent):
        return False
    if j.get("status") not in ("open", "claimed"):
        return False
    if j.get("status") == "claimed" and state(j, by_id, at) != "stalled":
        return False
    return not j.get("after") or by_id.get(j["after"], {}).get("status") == "done"

def select_dispatch(data, at, chief, workers, choose_worker, review_ids=None, exclude=()):
    rows = data.get("jobs", [])
    by_id, due = {j["id"]: j for j in rows}, deadlines(rows)
    candidates = []
    # Resume existing ownership before selecting new work, matching jobs.py next (including overdue claims).
    for j in rows:
        if j["id"] not in exclude and j.get("by") in workers and j.get("status") == "claimed" and state(j, by_id, at) in {"running", "stalled"}:
            return {"job": j, "worker": j["by"], "mode": "job"}
    for j in rows:
        if j["id"] in exclude or external_hold(j, at) or dependency_problem(j, by_id):
            continue
        review = is_review(j)
        if review and state(j, by_id, at) != "review":
            continue
        if review:
            if chief not in workers or (review_ids is not None and j["id"] not in review_ids):
                continue
            worker = chief
        else:
            if role_job(j):
                worker = chief if chief in workers else None
            elif j.get("for"):
                worker = j["for"] if j["for"] in workers else None
            else:
                worker = choose_worker(j, workers)
            if not worker or not claimable(j, rows, at, worker, chief):
                continue
        candidates.append((order(j, due, data.get("focus") or (), at), {"job": j, "worker": worker, "mode": "review" if review else "job"}))
    return min(candidates, key=lambda p: p[0])[1] if candidates else None

def snapshot(data, at, chief, workers, choose_worker, active_review=None, review_ids=None):
    rows = data.get("jobs", [])
    by_id = {j["id"]: j for j in rows}
    states = {j["id"]: {"state": state(j, by_id, at, active_review), "reason": reason(j, by_id, at)} for j in rows if j.get("status") in LIVE}
    active = [{"id": j["id"], "title": j.get("title", ""), "worker": j.get("by"), "mode": "job", "progress": j.get("progress")} for j in rows if j.get("status") == "claimed" and states.get(j["id"], {}).get("state") == "running"]
    if active_review and states.get(active_review.get("job"), {}).get("state") == "running":
        active = [a for a in active if a["id"] != active_review["job"]]
        active.append({**active_review, "id": active_review["job"], "worker": active_review.get("agent"), "mode": "review"})
    pick = select_dispatch(data, at, chief, workers, choose_worker, review_ids, exclude=[a["id"] for a in active])
    counts = {k: sum(s["state"] == k for s in states.values()) for k in ("running", "queued", "review", "waiting", "stalled")}
    # Unavailable workers are waiting, not ready to run.
    for j in rows:
        if states.get(j["id"], {}).get("state") == "queued":
            worker = chief if role_job(j) else j.get("for") or choose_worker(j, workers)
            if worker not in workers:
                states[j["id"]] = {"state": "waiting", "reason": "Waiting for an available eligible worker"}
                counts["queued"] -= 1
                counts["waiting"] += 1
    return {"version": 1, "at": at.isoformat(), "active": active,
            "next": ({**pick["job"], "worker": pick["worker"], "mode": pick["mode"]} if pick else None),
            "states": states, "counts": counts}
