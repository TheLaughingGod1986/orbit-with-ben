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
            if (job.get("status") != "open" or old.get("phase") != "reserved"
                    or not active(job, at) or old.get("host") != host_id
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


def cancel_with_git(*, token, host_id, worker, reason, clock=None):
    """Roll back an unclaimed reservation through the canonical queue transaction."""
    import jobs

    def apply(data):
        try:
            at = clock() if clock else dt.datetime.now(dt.timezone.utc)
            removed = cancel(data, token=token, host_id=host_id, worker=worker,
                             at=at, reason=reason)
            return removed, None, []
        except (ValueError, OSError) as error:
            return None, str(error), []

    return jobs.with_git(apply, "jobs: cancel unclaimed capacity reservation")


def consume(data, *, token, host_id, worker, claimant, eta_min=25, **evidence):
    """Revalidate a reservation and produce a canonical claim, never a launch.

    Mutate only after all queue/evidence checks pass. Laptop claims use macbook
    as their queue owner while retaining the specialist identity for routing,
    account and capability validation. HOS film stages need their own board
    transaction adapter and are deliberately excluded until that exists.
    """
    import jobs

    at = evidence["at"]
    rows = data.get("jobs", [])
    matches = [j for j in rows if (j.get("dispatch_reservation") or {}).get("token") == token]
    if len(matches) != 1:
        raise ValueError("one matching canonical reservation required")
    original = matches[0]
    old = original["dispatch_reservation"]
    if (old.get("host") != host_id or old.get("worker") != worker
            or old.get("head") != evidence.get("installed_head")
            or evidence.get("reviewed_head") != evidence.get("installed_head")):
        raise ValueError("claim identity or exact-head review changed")
    host = next((h for h in evidence["hosts"] if h.get("host") == host_id), {})
    expected = "macbook" if host.get("role") == "macbook" else worker
    if claimant != expected:
        raise ValueError("queue claimant does not match registered host role")
    if original.get("status") == "claimed":
        if old.get("phase") != "claimed" or original.get("by") != claimant:
            raise ValueError("reservation already consumed by another owner")
        return copy.deepcopy(original)  # Git retry acknowledgement, never launch permission.
    if old.get("phase") != "reserved" or not active(original, at):
        raise ValueError("reservation expired or no longer reserved")
    if type(eta_min) is not int or not 1 <= eta_min <= 25:
        raise ValueError("bounded claim estimate required")
    if original.get("repo") == "hos" and original.get("film"):
        raise ValueError("HOS film claim needs a supported HOS board transaction")
    if any(j.get("status") == "claimed" and j.get("by") in {worker, claimant}
           for j in rows if j is not original):
        raise ValueError("worker or laptop already holds a canonical claim")

    candidate = copy.deepcopy(data)
    selected = next(j for j in candidate["jobs"] if j["id"] == original["id"])
    del selected["dispatch_reservation"]
    # Recompute deadline order, stage/account occupancy, power/idle/resource,
    # model/capability and portable-input proof after removing only OUR token.
    refreshed = reserve(candidate, token=token, host_id=host_id, worker=worker, **evidence)
    if refreshed["job"] != original["id"] or refreshed["account"] != old.get("account"):
        raise ValueError("reservation priority or account changed; replan")
    del selected["dispatch_reservation"]
    # Use the normal queue claim operation under the specialist identity. This
    # also checks the installed relay's current capabilities; host proof cannot
    # silently override a missing local input capability.
    claimed = jobs.do_next(candidate, worker, workflow.MINI | {"macbook"}, at,
                           eta_min=eta_min, job_id=original["id"])
    if not claimed or claimed["id"] != original["id"]:
        raise ValueError("normal queue claim gates rejected reservation")
    if claimant != worker:
        claimed["by"] = claimant
        if claimed.get("progress", {}).get("default_plan"):
            claimed["progress"]["by"] = claimant
        claimed["history"][-1]["by"] = claimant
    claimed["dispatch_reservation"] = dict(old, phase="claimed", claimant=claimant,
                                              claimedAt=at.isoformat())
    claimed.setdefault("history", []).append(dict(at=at.isoformat(), by=claimant,
        what="capacity claim on " + host_id + " using " + worker + "; not launched"))
    original.clear()
    original.update(claimed)
    return copy.deepcopy(original)


def consume_with_git(*, evidence, token, host_id, worker, claimant, eta_min=25):
    """Queue and OWB board claim through the existing compare-and-push retry.

    No CLI or production caller is enabled. Every retry recollects evidence.
    HOS film stages fail closed in consume() until a cross-repo board adapter
    exists. If an OWB push attempt is rejected or fails after writing the local
    film status.json, rollback restores the pre-attempt file before the next
    retry recollects board_stage_claims or before returning.
    A returned claim still needs a bounded supervisor and local input rehash.
    """
    import jobs

    board_snapshots = {}

    def rollback_board():
        for path, (before_bytes, after_bytes) in list(board_snapshots.items()):
            try:
                if path.exists() and path.read_bytes() == after_bytes:
                    if before_bytes is None:
                        path.unlink(missing_ok=True)
                    else:
                        path.write_bytes(before_bytes)
            finally:
                board_snapshots.pop(path, None)

    def apply(data):
        rollback_board()
        before = copy.deepcopy(data)
        try:
            observed = evidence()
            previous = next((j for j in data.get("jobs", [])
                             if (j.get("dispatch_reservation") or {}).get("token") == token), {})
            already_claimed = previous.get("status") == "claimed"
            value = consume(data, token=token, host_id=host_id, worker=worker,
                            claimant=claimant, eta_min=eta_min, **observed)
            touched = []
            if jobs.on_board(value) and not already_claimed:
                path = jobs.film_status_path(value)
                before_bytes = path.read_bytes() if path and path.exists() else None
                error = jobs.board_claim(value, claimant, observed["at"])
                if error:
                    raise ValueError("board stage held: " + error)
                if path is not None and path.exists():
                    board_snapshots[path] = (before_bytes, path.read_bytes())
                touched.append(path)
            return value, None, touched
        except (ValueError, OSError) as error:
            rollback_board()
            data.clear()
            data.update(before)
            return None, str(error), []

    value, error = jobs.with_git(apply, "jobs: consume measured capacity reservation (not a launch)")
    if error or value is None:
        rollback_board()
    return value, error


def release_failed_with_git(*, token, host_id, worker, claimant, reason, clear, clock=None):
    """Release only this failed dispatch after the local supervisor proves it clear.

    `clear` must reread local leases on EVERY Git retry. An uncertain child or
    quarantine retains the canonical claim. A new owner/token or a completed job
    is never modified. OWB board changes roll back on rejected push attempts;
    HOS film stages remain excluded. Failed output is never marked approved.
    """
    import jobs

    if not str(reason).strip():
        raise ValueError("failed dispatch release requires a reason")
    snapshots = {}

    def rollback():
        for path, (before, after) in list(snapshots.items()):
            if path.exists() and path.read_bytes() == after:
                path.write_bytes(before)
            snapshots.pop(path, None)

    def apply(data):
        rollback()
        before = copy.deepcopy(data)
        try:
            matches = [j for j in data.get("jobs", [])
                       if (j.get("dispatch_reservation") or {}).get("token") == token]
            if not matches:
                return False, None, []  # already reconciled, never find by job ID alone
            if len(matches) != 1:
                raise ValueError("ambiguous failed dispatch token")
            job = matches[0]
            receipt = job["dispatch_reservation"]
            if (job.get("status") != "claimed" or job.get("by") != claimant
                    or receipt.get("phase") != "claimed"
                    or receipt.get("host") != host_id or receipt.get("worker") != worker
                    or receipt.get("claimant") != claimant):
                raise ValueError("failed dispatch claim changed; reconciliation required")
            if job.get("repo") == "hos" and job.get("film"):
                raise ValueError("HOS film release requires supported board transaction")
            if clear() is not True:
                raise ValueError("local execution cleanup unverified; claim retained")
            touched = []
            if jobs.on_board(job):
                path = jobs.film_status_path(job)
                original = path.read_bytes()
                jobs.board_release(job, claimant, "todo")
                snapshots[path] = (original, path.read_bytes())
                touched.append(path)
            at = clock() if clock else dt.datetime.now(dt.timezone.utc)
            jobs.do_release(job, claimant, "failed capacity dispatch: " + reason, at)
            del job["dispatch_reservation"]
            return True, None, touched
        except (ValueError, OSError) as error:
            rollback()
            data.clear()
            data.update(before)
            return None, str(error), []

    try:
        value, error = jobs.with_git(apply, "jobs: reconcile failed capacity dispatch")
    except BaseException:
        rollback()
        raise
    if error or value is None:
        rollback()
    return value, error
