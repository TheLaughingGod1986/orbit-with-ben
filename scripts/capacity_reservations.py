"""Canonical queue reservations for the capacity rollout (not a launcher).

The caller supplies observed, registered host/account evidence on every Git
transaction attempt. Reservations live on existing jobs, never a second queue.
No production caller is enabled until launch/receipt integration is reviewed.
"""
from __future__ import annotations

import copy
import datetime as dt
import re

import dispatch_capacity as capacity
import workflow_state as workflow


def active(job, at):
    value = job.get("dispatch_reservation") or {}
    start = workflow.timestamp(value.get("at"))
    end = workflow.timestamp(value.get("expiresAt"))
    return value if start and end and start <= at < end else None


def stage_key(job):
    return (job.get("repo", "owb"), job.get("film"), job.get("stage"))


def reserve(data, *, token, host_id, worker, hosts, leases, accounts, at,
            chief, choose_worker, installed_head, reviewed_head, stage_claims=()):
    """Recompute and reserve one proposal INSIDE jobs.with_git's retry callback.

    Replaying a successful token is idempotent. Competing transaction retries
    see the first reservation as occupied host/account/job/stage capacity.
    stage_claims must be reread from the studio board on each transaction try.
    A reservation is neither a queue claim, launch, KEEP nor stage approval.
    """
    if (not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", token)
            or not installed_head or reviewed_head != installed_head):
        raise ValueError("reservation needs a unique token and exact-head review")
    rows = data.get("jobs", [])
    for job in rows:
        old = job.get("dispatch_reservation") or {}
        if old.get("token") == token:
            if (not active(job, at) or old.get("host") != host_id
                    or old.get("worker") != worker or old.get("head") != installed_head):
                raise ValueError("reservation replay expired or changed identity/head")
            return copy.deepcopy(old)
    occupied = list(leases)
    for job in rows:
        reservation = active(job, at)
        if reservation:
            occupied.append(dict(reservation, job=job["id"], stage_key=list(stage_key(job))))
    # Existing film claims also exclude an otherwise open job on that stage.
    candidate = copy.deepcopy(data)
    held = {tuple(key) for key in stage_claims}
    for job in candidate.get("jobs", []):
        if job.get("film") and job.get("stage") and stage_key(job) in held:
            job["status"] = "blocked"
    plan = capacity.propose(candidate, hosts, occupied, accounts, at, chief, choose_worker)
    pick = next((p for p in plan["proposals"]
                 if p["host"] == host_id and p["worker"] == worker), None)
    if not pick:
        raise ValueError("no currently eligible capacity proposal for this host/worker")
    job = next(j for j in rows if j["id"] == pick["job"])
    value = dict(pick, token=token, head=installed_head, phase="reserved",
                 at=at.isoformat(), expiresAt=(at + dt.timedelta(minutes=2)).isoformat())
    job["dispatch_reservation"] = value
    job.setdefault("history", []).append(dict(at=at.isoformat(), by=worker,
        what="capacity reserved on " + host_id + "; not claimed or launched"))
    return copy.deepcopy(value)


def cancel(data, *, token, host_id, worker, at, reason):
    """Rollback only the matching reservation; never release an actual claim."""
    if not str(reason).strip():
        raise ValueError("reservation rollback needs a reason")
    for job in data.get("jobs", []):
        value = job.get("dispatch_reservation") or {}
        if value.get("token") != token:
            continue
        if value.get("host") != host_id or value.get("worker") != worker:
            raise ValueError("reservation rollback identity mismatch")
        if job.get("status") != "open":
            raise ValueError("actual claim/outcome requires its normal queue operation")
        del job["dispatch_reservation"]
        job.setdefault("history", []).append(dict(at=at.isoformat(), by=worker,
            what="capacity reservation cancelled: " + reason))
        return True
    return False


def reserve_with_git(*, evidence, token, host_id, worker):
    """Durable compare-and-push via the existing queue transaction.

    evidence() must collect fresh registration, guards, process leases, quotas,
    elected Chief, exact-head review and board stage claims for EACH retry.
    Deliberately no CLI, default config or production invocation yet.
    """
    import jobs

    def apply(data):
        try:
            value = reserve(data, token=token, host_id=host_id, worker=worker, **evidence())
            return value, None, []
        except (ValueError, OSError) as error:
            return None, str(error), []

    return jobs.with_git(apply, "jobs: reserve measured capacity (not a launch)")
