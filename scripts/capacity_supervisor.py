"""Bounded local execution adapter; deliberately has no CLI/production caller.

The caller must supply a freshly reread canonical claim and trusted local guard
checks. This is process lifecycle control, not a sandbox, queue completion,
cross-host transport, approval, or permission to enable capacity dispatch.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import signal
import subprocess
import time

import dispatch_capacity as capacity
import workflow_state as workflow


def utcnow():
    return dt.datetime.now(dt.timezone.utc)


def validate_claim(claim, registry, installed_head, reviewed_head, at):
    receipt = claim.get("dispatch_reservation") or {}
    if (not installed_head or installed_head != reviewed_head
            or receipt.get("head") != installed_head
            or claim.get("status") != "claimed" or receipt.get("phase") != "claimed"
            or receipt.get("host") != registry.host
            or receipt.get("job") != claim.get("id")
            or receipt.get("claimant") != claim.get("by")
            or not receipt.get("worker") or not receipt.get("account")
            or not receipt.get("token")):
        raise ValueError("matching canonical claim and exact-head review required")
    # Claim acknowledgements may be replayed by Git, but cannot extend the
    # original two-minute launch window or silently resurrect stale work.
    start, end = workflow.timestamp(receipt.get("at")), workflow.timestamp(receipt.get("expiresAt"))
    if not start or not end or not start <= at < end:
        raise ValueError("claim launch window expired")
    if (claim.get("execution_resources") != ["cpu"] or claim.get("kind") not in capacity.SAFE_KINDS
            or claim.get("no_spend") is not True or claim.get("no_publish") is not True
            or workflow.role_job(claim) or workflow.is_review(claim)):
        raise ValueError("only explicitly scoped independent CPU work may launch")
    return receipt


def _stop_group(child):
    """Kill the whole session, including descendants after the leader exits."""
    try:
        os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    child.wait(timeout=5)


def run(*, registry, read_claim, guard, installed_head, reviewed_head, argv,
        cwd, log_path, cap_seconds, preflight, clock=utcnow):
    """Run one caller-approved command in a bounded supervised process group.

    read_claim()/guard() must use trusted current state, not a cached proposal.
    guard is repeated after preflight/lease acquisition and while executing;
    laptop callers must include mains/idle checks there. preflight performs
    consuming-host input rehashing. No shell or detached-child escape is allowed
    by contract; arbitrary subprocesses are NOT sandboxed by this adapter.
    The returned receipt never marks a queue job done or approves its outputs.
    """
    if (not isinstance(argv, (list, tuple)) or not argv
            or any(not isinstance(a, str) or not a or "\0" in a for a in argv)
            or not pathlib.Path(argv[0]).is_absolute()
            or type(cap_seconds) is not int or not 1 <= cap_seconds <= 1500):
        raise ValueError("explicit absolute executable and 1–1500 second cap required")
    cwd = pathlib.Path(cwd).resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError("working directory missing")
    claim = read_claim()
    receipt = validate_claim(claim, registry, installed_head, reviewed_head, clock())
    if guard(claim) is not True:
        raise ValueError("local execution guards rejected launch")
    preflight(claim, cwd)
    # Recover only locally proven orphan groups before seeking capacity.
    # Unknown spawn gaps/probe failures remain occupied and block record().
    recovery = registry.reconcile(clock())
    # Refuse even same-PID replay: a Git claim acknowledgement is not permission
    # to start another copy. Registry lock arbitrates simultaneous supervisors.
    registry.record(dict(receipt, phase="reserved"), os.getpid(), clock(), cap_seconds,
                    exclusive=True)
    child = None
    started = time.monotonic()
    outcome = dict(job=claim["id"], token=receipt["token"], host=registry.host,
                   worker=receipt["worker"], account=receipt["account"], head=installed_head,
                   phase="not_started", startedAt=clock().isoformat(), exit_code=None,
                   recovery=recovery)
    try:
        latest = read_claim()
        current = validate_claim(latest, registry, installed_head, reviewed_head, clock())
        if current != receipt or guard(latest) is not True:
            raise ValueError("claim or host guards changed before launch")
        # Exclusive log creation preserves prior executions and makes output
        # capture explicit without leaking command output into relay logs.
        with pathlib.Path(log_path).open("xb") as log:
            # Keep a durable launch-attempt seal after the live lease ends.
            # Otherwise replaying the still-claimed canonical receipt could
            # launch a second copy after a successful exit or launch failure.
            seals = registry.root / (registry.host + "-launches")
            seals.mkdir(exist_ok=True)
            key = hashlib.sha256(receipt["token"].encode()).hexdigest()
            with (seals / (key + ".json")).open("x") as seal:
                json.dump(dict(job=claim["id"], token=receipt["token"],
                               at=clock().isoformat(), head=installed_head), seal)
                seal.flush()
                os.fsync(seal.fileno())
            registry.arm(receipt["token"], os.getpid())
            child = subprocess.Popen(list(argv), cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                                     stdin=subprocess.DEVNULL, start_new_session=True)
            # A very short child may already have exited. The finally block
            # still reaps its group; only running leaders need a recovery ID.
            if child.poll() is None:
                try:
                    registry.attach(receipt["token"], os.getpid(), child.pid)
                except (ValueError, ProcessLookupError):
                    if child.poll() is None:
                        raise
            outcome["phase"] = "running"
            while child.poll() is None:
                if time.monotonic() - started >= cap_seconds:
                    outcome["phase"] = "timed_out"
                    break
                # Observe cancellation/ownership and guards without extending
                # the launch-window timestamp once the child is running.
                latest = read_claim()
                if (latest.get("status") != "claimed" or latest.get("by") != claim["by"]
                        or latest.get("dispatch_reservation") != receipt
                        or guard(latest) is not True):
                    outcome["phase"] = "guard_stopped"
                    break
                time.sleep(min(0.2, max(0, cap_seconds - (time.monotonic() - started))))
            if outcome["phase"] == "running":
                outcome["phase"] = "exited"
    finally:
        # Always reap child group BEFORE freeing capacity. If cleanup fails the
        # lease stays occupied; another supervisor cannot assume a free slot.
        if child is not None:
            _stop_group(child)
            outcome["exit_code"] = child.returncode
        registry.finish(receipt["token"], os.getpid())
    outcome["finishedAt"] = clock().isoformat()
    return outcome
