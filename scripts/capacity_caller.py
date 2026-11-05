"""Opt-in production bridge for the Mini relay and registered laptop worker.

Disabled unless OWB_CAPACITY_ENABLED=1 and an owner-private dispatch.json names
an exact reviewed installation and approved command. No registration, model
probe, mount, login, transport credential or approval is invented here. Mounted
filesystem handoff is the sole supported transport; missing access fails closed.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import subprocess
import sys
import json
import hashlib
import os
import pathlib

import capacity_evidence as evidence_tools
import capacity_supervisor
import dispatch_capacity
import execution_leases
import portable_transfer
import routing
import workflow_state


def production_tick(*, role, owb_root, hos_root=None, environ=None, serial_only=False, _serial_lock_held=False, admission=None):
    """Run capacity transactions in their own reviewed, preprovisioned checkout.

    A busy serial relay may call this without touching its Git index. The
    configured checkout is locked for the entire attempt. We never create or
    switch a worktree during dispatch, and never share its index with a worker.
    A fresh local occupancy receipt permits selection; canonical admission
    then binds the actual serial job/worker/account before launch.
    """
    env = os.environ if environ is None else environ
    if env.get("OWB_CAPACITY_ENABLED") != "1":
        return None
    try:
        root = pathlib.Path(env["OWB_CAPACITY_ROOT"])
        config = evidence_tools.private_document(root, "dispatch.json")
        checkout = pathlib.Path(config["queue_root"]).resolve(strict=True)
        if checkout == pathlib.Path(owb_root).resolve() or not (checkout / ".git").exists():
            raise ValueError("dedicated queue checkout required")
        if (config.get("role") != role or config.get("enabled") is not True
                or not config.get("approved_by") or not config.get("approval_ref")
                or (not serial_only and not dispatch_capacity.fresh(config, dt.datetime.now(dt.timezone.utc)))):
            raise ValueError("fresh rollout approval required")
        # Reuse the bounded supervisor's policy: no indefinite worker run.
        cap = config.get("cap_seconds", 1200)
        if type(cap) is not int or not 1 <= cap <= 1200:
            raise ValueError("production attempt requires a 1–1200 second cap")
        lock_context = (contextlib.nullcontext() if _serial_lock_held
                        else (root / "caller.lock").open("a"))
        with lock_context as lock:
            try:
                if lock is not None:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return {"state": "capacity_busy"}
            evidence_tools.reviewed_installation(checkout, config.get("reviewed_head"))
            argv = [sys.executable, str(checkout / "scripts/capacity_caller.py"), role]
            if serial_only:
                argv.append("--serial-only")
            if admission is not None:
                argv.extend(["--admit", json.dumps(admission)])
            if hos_root is not None:
                argv.append(str(hos_root))
            # Wrapper timeout exceeds the CPU cap to permit canonical Git
            # cleanup. Do not kill a supervisor at the worker timeout: it must
            # reap its group before freeing capacity.
            child = subprocess.run(argv, cwd=checkout, env=dict(env), capture_output=True,
                                   text=True, timeout=cap + 240)
            if child.returncode:
                raise RuntimeError("isolated capacity process failed; inspect private journal")
            result = json.loads(child.stdout)
            if not isinstance(result, dict) or not result.get("state"):
                raise ValueError("isolated caller returned malformed receipt")
            return result
    except Exception as error:
        return {"state": "capacity_rejected", "reason": type(error).__name__,
                "availability": "unknown", "free_slot_at": None}


@contextlib.contextmanager
def serial_preflight(*, owb_root, hos_root=None, environ=None, role="mini"):
    """Keep local launch exclusion through canonical account admission.

    Releasing the lock immediately after a local observation would let a busy
    tick launch between that observation and the serial execution lease.
    """
    env = os.environ if environ is None else environ
    if env.get("OWB_CAPACITY_ENABLED") != "1":
        yield None
        return
    lock = None
    try:
        root = pathlib.Path(env["OWB_CAPACITY_ROOT"])
        # Validate ownership/mode before opening any evidence-directory file.
        evidence_tools.private_document(root, "dispatch.json")
        lock = (root / "caller.lock").open("a")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (KeyError, OSError, ValueError):
        if lock is not None:
            lock.close()
        yield {"state": "capacity_rejected", "serial_safe": False}
        return
    try:
        yield production_tick(role=role, owb_root=owb_root, hos_root=hos_root,
                              environ=env, serial_only=True, _serial_lock_held=True)
    finally:
        lock.close()


def attempt(*, role, owb_root, hos_root=None, legacy_lease=None, chief=None,
            laptop_guard=None, environ=None, clock=None, serial_only=False, admission=None):
    """Return None only when disabled/no candidate; otherwise consume this tick.

    A failed enabled attempt never falls through to a second serial launch.
    Canonical reserve/consume/release and per-token launch seals live in the
    existing adapters. Success captures outputs for review, never marks done.
    Exceptions are reported by type only; private commands/paths stay private.
    """
    env = os.environ if environ is None else environ
    if env.get("OWB_CAPACITY_ENABLED") != "1":
        return None
    try:
        result = _attempt(role=role, owb_root=pathlib.Path(owb_root), hos_root=hos_root,
                        legacy_lease=legacy_lease, chief=chief, laptop_guard=laptop_guard,
                        evidence_root=pathlib.Path(env["OWB_CAPACITY_ROOT"]),
                        clock=clock or (lambda: dt.datetime.now(dt.timezone.utc)), serial_only=serial_only, admission=admission)
        # The relay log intentionally omits paths; retain the complete handoff
        # in the same owner-private directory so the next run can find returns.
        _journal(pathlib.Path(env["OWB_CAPACITY_ROOT"]), result)
        return result
    except Exception as error:
        result = {"state": "capacity_rejected", "reason": type(error).__name__,
                  "availability": "unknown", "free_slot_at": None}
        try:
            _journal(pathlib.Path(env["OWB_CAPACITY_ROOT"]), result)
        except (KeyError, OSError, ValueError, TypeError):
            # Never let failed private evidence access become serial fallback.
            pass
        return result


def _journal(root, result):
    config = evidence_tools.private_document(root, "dispatch.json")
    key = hashlib.sha256(str(config.get("token", "")).encode()).hexdigest()
    directory = root / "attempts"
    directory.mkdir(mode=0o700, exist_ok=True)
    # Never overwrite a prior successful handoff. Repeated observations may
    # have their own immutable record; they cannot replace a return receipt.
    import tempfile
    fd, path = tempfile.mkstemp(prefix=key + "-", suffix=".json", dir=directory)
    with os.fdopen(fd, "w") as out:
        json.dump(result, out)
        out.flush()
        os.fsync(out.fileno())


def _attempt(*, role, owb_root, hos_root, legacy_lease, chief, laptop_guard,
             evidence_root, clock, serial_only=False, admission=None):
    import jobs
    config = evidence_tools.private_document(evidence_root, "dispatch.json")
    if (config.get("enabled") is not True or config.get("role") != role
            or not config.get("approved_by") or not config.get("approval_ref")
            or (not serial_only and not dispatch_capacity.fresh(config, clock()))):
        raise ValueError("fresh explicit rollout approval required")
    reviewed = config.get("reviewed_head")
    head = evidence_tools.reviewed_installation(owb_root, reviewed)
    if config.get("mode") == "receive" and not serial_only:
        if role != "mini":
            raise ValueError("only Mini receives returned work for review")
        job = jobs.find(jobs.load(), config["job"])
        return_bundle = pathlib.Path(config["return_bundle"])
        with portable_transfer.open_regular(return_bundle.parent,
                return_bundle.name + ".receipt.json") as source:
            raw = source.read(evidence_tools.MAX_DOCUMENT + 1)
        if len(raw) > evidence_tools.MAX_DOCUMENT:
            raise ValueError("return receipt exceeds size limit")
        receipt = json.loads(raw)
        if not isinstance(receipt, dict):
            raise ValueError("return receipt must be an object")
        received = portable_transfer.consume_return(
            job, reservation=config["token"], host=config["source_host"],
            return_bundle=config["return_bundle"], receipt=receipt,
            review_parent=config["review_parent"], at=clock(),
            max_bytes=config["max_bytes"], max_files=config["max_files"])
        return dict(state="capacity_returned_for_review", **received)
    job_id = config.get("job")
    argv = config.get("argv")
    if not serial_only and (not job_id or not isinstance(argv, list) or not argv):
        raise ValueError("approved job-bound command required")
    # A private request is scoped to one job and one attempt. A replay retains
    # the token and is stopped by canonical ownership/immutable launch seals.
    token = config.get("token")
    if not serial_only and (not isinstance(token, str) or not token.strip()):
        raise ValueError("stable request token required")
    initial_host, _ = evidence_tools.collect(evidence_root, at=clock(), installed_head=head)
    if initial_host.get("role") != role:
        raise ValueError("registered host role differs from production caller")
    host_id = initial_host["host"]
    registry = execution_leases.Registry(evidence_root / "leases", host_id,
                                         initial_host["configured_limit"])
    receipt = None
    bundle = None
    budget = config.get("max_bytes", 0)
    files = config.get("max_files", 0)
    job = jobs.find(jobs.load(), job_id) if not serial_only else None
    if not serial_only and not job:
        raise ValueError("approved request job missing")
    if role == "macbook" and not serial_only:
        # Source/staging/return roots must already be mounted and readable on
        # this host. We never create a mount or guess a Mini/NAS path.
        if laptop_guard is None or laptop_guard():
            raise ValueError("laptop mains/idle guards rejected staging")
        bundle, receipt = portable_transfer.stage_outbound(
            job, reservation=token, host=host_id, source_root=config["source_root"],
            staging_parent=config["staging_parent"], at=clock(),
            max_bytes=budget, max_files=files)
    cwd = bundle if bundle is not None else owb_root

    def observe():
        # Recollect identity, resources, account/model/capability probes and
        # board/process leases on EVERY canonical Git retry.
        kwargs = {}
        if serial_only or role == "macbook" or (evidence_root / "peer.json").exists():
            peer = evidence_tools.private_document(evidence_root, "peer.json")
            if (not dispatch_capacity.fresh(peer, clock())
                    or peer.get("transport_approval_ref") != config.get("transport_approval_ref")
                    or not peer.get("transport_approval_ref")):
                raise ValueError("fresh approved peer evidence transport required")
            kwargs = dict(remote_hosts=peer.get("hosts", []),
                          remote_leases=peer.get("leases", []))
            peer_role = "mini" if role == "macbook" else "macbook"
            if len(kwargs["remote_hosts"]) != 1 or kwargs["remote_hosts"][0].get("role") != peer_role:
                raise ValueError("observed peer occupancy required")
        observed = evidence_tools.transaction_evidence(
            evidence_root, lease_root=registry.root, owb_root=owb_root,
            hos_root=hos_root, reviewed_head=reviewed,
            chief=chief() if callable(chief) else chief,
            choose_worker=lambda j, workers: routing.preferred_worker(j, workers),
            legacy_lease=legacy_lease, clock=clock, **kwargs)
        if receipt is not None:
            local = next(h for h in observed["hosts"] if h["host"] == host_id)
            local["input_receipts"] = portable_transfer.input_receipts_map(
                receipt, job["portable"], bundle, job=job_id, reservation=token,
                host=host_id, at=clock(), max_bytes=budget)
        return observed

    observed = observe()
    data = jobs.load()
    if serial_only:
        import capacity_reservations
        # A known busy peer is not local occupancy. This is only a gate to
        # candidate selection: every enabled serial launch still needs a fresh
        # canonical admission for its actual job/model/account below.
        local = next(h for h in observed["hosts"] if h["host"] == host_id)
        clear = (not dispatch_capacity.host_problem(local, observed["at"])
                 and not any(x.get("host") == host_id or not x.get("account")
                             or x.get("recovery_required") for x in observed["leases"])
                 and all(dispatch_capacity.fresh(h, observed["at"])
                         and h.get("registered_id") == h.get("host") for h in observed["hosts"])
                 and not any((a := capacity_reservations.active(j, observed["at"]))
                             and a.get("host") == host_id for j in data.get("jobs", []))
                 and not dispatch_capacity.unattributed_claims(
                     data, observed["hosts"], observed["leases"], observed["at"]))
        if admission is not None:
            import serial_admission
            def apply(current):
                try:
                    return serial_admission.reserve(current, host_id=host_id,
                        request=admission, observed=observe()), None, []
                except (ValueError, OSError) as error:
                    return None, str(error), []
            value, error = jobs.with_git(apply, "jobs: admit accounted serial execution")
            if error or value is None:
                return {"state": "capacity_rejected", "serial_safe": False}
            return {"state": "capacity_waiting", "serial_safe": True, "admission": value}
        return {"state": "capacity_waiting", "serial_safe": clear,
                "availability": "unknown", "free_slot_at": None}
    plan = dispatch_capacity.propose(data, **{k: observed[k] for k in
        ("hosts", "leases", "accounts", "at", "chief", "choose_worker")})
    pick = next((p for p in plan["proposals"] if p["host"] == host_id), None)
    if pick is None:
        return {"state": "capacity_waiting", "availability": "unknown", "free_slot_at": None}
    if pick["job"] != job_id:
        raise ValueError("approved command differs from current deadline-first selection")
    worker = pick["worker"]
    claimant = "macbook" if role == "macbook" else worker

    def read_claim():
        return jobs.find(jobs.load(), job_id) or {}

    def guard(claim):
        if evidence_tools.private_document(evidence_root, "dispatch.json") != config:
            return False
        if role == "macbook" and (laptop_guard is None or laptop_guard()):
            return False
        # Do not recheck the two-minute launch window during execution. The
        # supervisor checks ownership separately; resource/account proofs must
        # remain fresh and the installed code must remain reviewed.
        try:
            current = observe()
            local = next(h for h in current["hosts"] if h["host"] == host_id)
            report = local["workers"].get(worker, {})
            return (not dispatch_capacity.host_problem(local, current["at"])
                    and not workflow_state.capability_problem(job, worker, current["at"],
                        {worker: report.get("capabilities") or {}})
                    and report.get("ready") is True
                    and report.get("account") == pick["account"]
                    and routing.model_for(job, worker) in report.get("verified_models", [])
                    and current["accounts"].get(pick["account"], {}).get("ready") is True)
        except (OSError, ValueError, TypeError):
            return False

    outcome = capacity_supervisor.dispatch_claimed(
        evidence=observe, registry=registry, token=token, host_id=host_id,
        worker=worker, claimant=claimant, read_claim=read_claim, guard=guard,
        installed_head=head, reviewed_head=reviewed, argv=argv, cwd=cwd,
        log_path=config["log_path"], cap_seconds=config.get("cap_seconds", 1200),
        rollout_enabled=True, rollout_approval_ref=config["approval_ref"],
        portable_receipt=receipt, max_portable_bytes=budget, expected_job=job_id,
        clock=clock)
    result = dict(state="capacity_exited", job=job_id, outcome=outcome,
                  job_completed=False, stage_approved=False)
    if receipt is not None:
        returned, output = portable_transfer.stage_return(
            job, reservation=token, host=host_id, work_root=bundle,
            return_parent=config["return_parent"], at=clock(),
            max_bytes=budget, max_files=files)
        # Persist return receipt beside the unique bundle for Mini's receiving
        # caller. This is never a job completion or film approval signal.
        receipt_path = returned.with_suffix(".receipt.json")
        fd = os.open(receipt_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w") as out:
            json.dump(output, out)
            out.flush()
            os.fsync(out.fileno())
        result.update(return_bundle=str(returned), receipt_path=str(receipt_path))
    return result


if __name__ == "__main__":
    import chief_relay
    admission = None
    if "--admit" in sys.argv:
        i = sys.argv.index("--admit")
        admission = json.loads(sys.argv[i + 1])
        del sys.argv[i:i + 2]
    serial_only = "--serial-only" in sys.argv
    if serial_only:
        sys.argv.remove("--serial-only")
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in {"mini", "macbook"}:
        raise SystemExit(2)
    role = sys.argv[1]
    laptop_guard = None
    if role == "macbook":
        import macbook_worker
        laptop_guard = macbook_worker.guards
    result = attempt(role=role, owb_root=pathlib.Path(__file__).resolve().parents[1],
        hos_root=sys.argv[2] if len(sys.argv) == 3 else None,
        legacy_lease=chief_relay.current_execution if role == "mini" else None,
        chief=lambda: chief_relay.acting(chief_relay.now())[1], laptop_guard=laptop_guard,
        serial_only=serial_only, admission=admission)
    print(json.dumps(result))
