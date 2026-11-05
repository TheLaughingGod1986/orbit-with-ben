#!/usr/bin/env python3
"""Fail-closed capacity planning. Shadow only until exact-head rollout review.

This module does not launch, claim, reroute, approve or transfer jobs. Callers must
revalidate its proposal inside the canonical queue transaction before dispatch.
Host reports are observations from a registered worker, never inferred from UP.
"""
from __future__ import annotations

import hashlib
import math
import pathlib
import re

import workflow_state as workflow
import routing
import portable_transfer

SAFE_KINDS = {"assembly", "chart"}
DENIED_RESOURCES = {"browser", "generation", "publishing", "nas", "credentials"}


def fresh(report, at, max_age=300):
    if not isinstance(report, dict):
        return False
    stamp = workflow.timestamp(report.get("at"))
    end = workflow.timestamp(report.get("expiresAt"))
    return bool(stamp and end and 0 <= (at-stamp).total_seconds() <= max_age and at < end)


def live_leases(leases, at, local_host, process_alive):
    """Local leases require process proof; remote leases require fresh host proof.

    A timer never proves exit. Stale remote/unknown process evidence occupies
    capacity until its own host positively reconciles it. Remote PIDs are not
    probed locally. Malformed occupancy fails closed rather than disappearing.
    """
    result = []
    for lease in leases:
        start = workflow.timestamp(lease.get("startedAt"))
        end = workflow.timestamp(lease.get("expiresAt"))
        if not start or not end or end <= start or start > at or not lease.get("host"):
            raise ValueError("malformed process lease cannot establish spare capacity")
        uncertain = lease.get("recovery_required") is True
        if lease.get("host") == local_host:
            try:
                pid = int(lease.get("pid") or 0)
                if pid <= 0:
                    raise ValueError("missing process identity")
                alive = process_alive(pid)
                if alive is False and not lease.get("child_may_exist") and not uncertain:
                    continue  # Positive local exit proof for an unarmed supervisor.
                if alive is not True:
                    uncertain = True
            except (TypeError, ValueError, OSError, RuntimeError):
                uncertain = True
        elif not fresh(lease, at) or lease.get("process_validated") is not True:
            uncertain = True
        if not lease.get("job") or not lease.get("worker"):
            raise ValueError("unattributed process lease cannot establish spare capacity")
        result.append(dict(lease, overdue=at >= end, recovery_required=uncertain))
    return result


def host_problem(host, at):
    if not host.get("registered_id") or host.get("host") != host.get("registered_id"):
        return "host identity unregistered"
    if not fresh(host, at):
        return "host evidence stale or missing"
    if host.get("guard_reasons") or host.get("state") not in {"idle", "working"}:
        return "host guards: " + "; ".join(host.get("guard_reasons") or [host.get("state", "unknown")])
    idle = host.get("idle_minutes")
    if host.get("role") == "macbook" and (host.get("on_ac") is not True
            or type(idle) not in (int, float) or not math.isfinite(idle) or idle < 10):
        return "laptop on battery or in use"
    for key in ("free_gb", "min_free_gb", "load", "max_load", "memory_available_gb", "min_memory_gb"):
        value = host.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            return "measured resources missing"
    if host["free_gb"] < host["min_free_gb"] or host["load"] > host["max_load"] or host["memory_available_gb"] < host["min_memory_gb"]:
        return "measured resource guard"
    limit = host.get("configured_limit")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        return "configured capacity missing"
    if limit > 1 and (not host.get("capacity_review") or not host.get("installed_head")
                      or host.get("reviewed_head") != host.get("installed_head")):
        return "additional lane needs exact-head capacity review"
    return ""


def portable_problem(job, host, at):
    """No path inference: approved receipts identify each relative input by hash.

    Receipts prove host access to approved content, not film/KEEP approval. The
    worker must rehash locally immediately before execution; output receipts
    must be verified back on Mini before review or canonical stage completion.
    """
    contract = job.get("portable") or {}
    if (contract.get("version") != 1 or not contract.get("approved_by")
            or not contract.get("approval_ref") or job.get("kind") not in SAFE_KINDS
            or workflow.role_job(job) or workflow.is_review(job)):
        return "portable contract absent or unsupported work"
    if contract.get("no_spend") is not True or contract.get("no_publish") is not True:
        return "portable contract must prohibit spend and publishing"
    resources = contract.get("resources")
    if not isinstance(resources, list) or DENIED_RESOURCES.intersection(resources):
        return "Mini-only resource"
    if resources != ["cpu"]:
        return "unsupported portable resources"
    if not contract.get("output_receipts_required"):
        return "output hash receipts required"
    outputs = contract.get("outputs")
    if not isinstance(outputs, list):
        return "explicit portable output paths required"
    try:
        portable_transfer.manifest([{"path": name, "sha256": "0" * 64} for name in outputs])
    except (TypeError, ValueError):
        return "invalid portable output paths"
    inputs = contract.get("inputs")
    if not isinstance(inputs, list):
        return "explicit portable inputs required"
    receipts = host.get("input_receipts") or {}
    for item in inputs:
        if not isinstance(item, dict):
            return "malformed portable input"
        path = pathlib.PurePosixPath(item.get("path", ""))
        digest = item.get("sha256", "")
        if (not str(item.get("path", "")) or path.is_absolute() or ".." in path.parts
                or "\\" in str(path) or not re.fullmatch(r"[0-9a-f]{64}", digest)
                or not item.get("approval_ref")):
            return "invalid or unapproved portable input"
        receipt = receipts.get(str(path)) or {}
        if receipt.get("sha256") != digest or receipt.get("readable") is not True or not fresh(receipt, at):
            return "input hash/readability receipt missing: " + str(path)
    return ""


def verify_inputs(contract, root):
    """Local preflight: prohibit traversal and symlink escape; stream hashes."""
    root = pathlib.Path(root).resolve()
    for item in contract["inputs"]:
        relative = pathlib.PurePosixPath(item["path"])
        if relative.is_absolute() or ".." in relative.parts or "\\" in str(relative):
            raise ValueError("input path escapes checkout")
        path = (root / str(relative)).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("input path escapes checkout or is not a file")
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024*1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != item["sha256"]:
            raise ValueError("input hash mismatch: " + str(relative))


def unattributed_claims(data, hosts, leases, at):
    """A queue owner is not process/account proof, including legacy laptops.

    Keep even stalled claims occupied until canonical release or fresh,
    identity-bound process evidence accounts for them. A timer proves no exit.
    Canonical reservations carry their own durable account occupancy.
    """
    unknown = []
    for row in data.get("jobs", []):
        if row.get("status") != "claimed":
            continue
        reservation = row.get("dispatch_reservation") or {}
        if (reservation.get("phase") in {"claimed", "serial"} and reservation.get("account")
                and reservation.get("host")):
            continue
        matched = False
        for lease in leases:
            if lease.get("job") != row["id"] or not lease.get("account"):
                continue
            peer = next((h for h in hosts if h.get("host") == lease.get("host")), {})
            if (fresh(peer, at) and peer.get("registered_id") == peer.get("host")
                    and (row.get("by") != "macbook" or peer.get("role") == "macbook")):
                matched = True
                break
        if not matched:
            unknown.append(row["id"])
    return unknown


def propose(data, hosts, leases, accounts, at, chief, choose_worker):
    """Deadline-first shadow batch, using the existing workflow gates.

    Account capacity is shared across hosts. `ready` needs a fresh observed
    auth/quota result; a CLI installed/green heartbeat is insufficient. Each
    tentative pick occupies job, stage, worker, account and host in this batch.
    This is a proposal, never a queue claim or promise of a free slot.
    """
    if unattributed_claims(data, hosts, leases, at):
        return {"mode": "shadow", "proposals": [],
                "host_rejections": {h.get("host", "unknown"): "canonical claim occupancy unattributed"
                                    for h in hosts},
                "free_slot_at": None, "availability": "unknown"}
    rows = data.get("jobs", [])
    by_id = {j["id"]: j for j in rows}
    due = workflow.deadlines(rows)
    picked, rejected = [], {}
    busy_jobs = {x["job"] for x in leases}
    busy_workers = {x["worker"] for x in leases}
    busy_workers |= {j.get("by") for j in rows if j.get("status") == "claimed"
                     and not workflow.claim_is_stalled(j, at)}
    busy_stages = {(j.get("repo", "owb"), j.get("film"), j.get("stage")) for j in rows
                   if j.get("status") == "claimed" and j.get("film") and j.get("stage")}
    busy_stages |= {tuple(x["stage_key"]) for x in leases if x.get("stage_key")}
    ordered = sorted(rows, key=lambda j: workflow.order(j, due, data.get("focus") or (), at))
    for host in sorted(hosts, key=lambda h: h.get("role") == "macbook"):
        problem = host_problem(host, at)
        identity = host.get("host", "unknown")
        if any(x.get("host") == identity and x.get("recovery_required") for x in leases):
            rejected[identity] = "host execution recovery required"
            continue
        if problem:
            rejected[identity] = problem
            continue
        if host.get("role") == "macbook":
            minis = [h for h in hosts if h.get("role") == "mini"]
            if not minis or any(host_problem(h, at) or sum(x.get("host") == h["host"]
                    for x in [*leases, *picked]) < h["configured_limit"] for h in minis):
                rejected[identity] = "Mini capacity exhaustion not demonstrated"
                continue
        used = sum(x.get("host") == identity for x in leases)
        for _ in range(max(0, host["configured_limit"] - used)):
            candidates = []
            for job in ordered:
                stage = (job.get("repo", "owb"), job.get("film"), job.get("stage"))
                if (job.get("status") != "open" or job["id"] in busy_jobs
                        or (job.get("repo") == "hos" and job.get("film"))
                        or stage[1] and stage[2] and stage in busy_stages
                        or workflow.is_review(job) or workflow.role_job(job)):
                    continue  # Chief reviews remain in the canonical elected-Chief lane; HOS film stages fail closed.
                if workflow.external_hold(job, at) or workflow.dependency_problem(job, by_id):
                    continue
                laptop = host.get("role") == "macbook"
                if (job.get("execution_resources") != ["cpu"] or job.get("kind") not in SAFE_KINDS
                        or job.get("no_spend") is not True or job.get("no_publish") is not True):
                    continue
                if laptop and portable_problem(job, host, at):
                    continue
                eligible = set()
                for worker, report in (host.get("workers") or {}).items():
                    account = accounts.get(report.get("account")) or {}
                    limit = account.get("limit", 0)
                    account_used = sum(x.get("account") == report.get("account") for x in [*leases, *picked])
                    if any(not x.get("account") for x in leases):
                        continue  # Legacy leases cannot establish shared-account spare capacity.
                    if (worker in busy_workers or not fresh(report, at) or report.get("ready") is not True
                            or not report.get("auth_evidence")
                            or not routing.model_for(job, worker)
                            or routing.model_for(job, worker) not in (report.get("verified_models") or [])
                            or not fresh(account, at) or account.get("ready") is not True
                            or not account.get("quota_evidence")
                            or not isinstance(limit, int) or account_used >= limit):
                        continue
                    # Portability does not bypass original agent, capability or dependency gates.
                    can = workflow.MINI if not laptop else {"mini", "any", "macbook"}
                    caps = {worker: report.get("capabilities") or {}}
                    if workflow.claimable(job, rows, at, worker, chief, can=can, capabilities=caps):
                        eligible.add(worker)
                worker = choose_worker(job, eligible) if eligible else None
                if worker in eligible:
                    candidates.append((job, worker))
            if not candidates:
                break
            job, worker = candidates[0]
            pick = {"job":job["id"], "worker":worker, "host":identity,
                    "account":host["workers"][worker]["account"], "phase":"proposed",
                    "action":job.get("remaining_action", ""), "progress":job.get("progress"),
                    "recorded_task_estimate_minutes":job.get("eta_min"),
                    "free_slot_at":None, "availability":"unknown",
                    "stage_key":[job.get("repo", "owb"), job.get("film"), job.get("stage")]}
            picked.append(pick)
            busy_jobs.add(job["id"])
            busy_workers.add(worker)
            if job.get("film") and job.get("stage"):
                busy_stages.add(tuple(pick["stage_key"]))
    return {"mode":"shadow", "proposals":picked, "host_rejections":rejected,
            "free_slot_at":None, "availability":"unknown"}
