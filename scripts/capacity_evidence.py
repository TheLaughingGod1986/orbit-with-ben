"""Read-only local capacity evidence, disconnected from production dispatch.

Registration and probe receipts must come from an explicitly configured private
local directory. This is an OS-user trust boundary, not remote attestation.
Nothing here signs in, prompts a model, clears an outage, or authorizes rollout.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import platform
import re
import shutil
import stat
import subprocess

import dispatch_capacity as capacity
import workflow_state as workflow

MAX_DOCUMENT = 65536


def private_document(root, name):
    """Open through directory FDs; reject symlinks, permissive modes and devices."""
    if name not in {"registration.json", "probes.json"}:
        raise ValueError("unsupported evidence document")
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(directory)
        if info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError("evidence directory must be private and owned by this user")
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        with os.fdopen(fd, "rb") as source:
            info = os.fstat(source.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                    or info.st_mode & 0o077 or info.st_size > MAX_DOCUMENT):
                raise ValueError("evidence file must be a bounded private regular file")
            raw = source.read(MAX_DOCUMENT + 1)
            if len(raw) > MAX_DOCUMENT:
                raise ValueError("evidence file too large")
        doc = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
        if not isinstance(doc, dict):
            raise ValueError("evidence document must be an object")
        return doc
    finally:
        os.close(directory)


def command(argv):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=3)
    if result.returncode or result.stderr.strip():
        raise ValueError("local measurement unavailable")
    return result.stdout


def measure(root, *, run=command):
    """macOS measurements only; no auth/quota/media readiness is inferred.

    Memory uses free plus speculative pages, deliberately excluding inactive,
    compressed and purgeable totals rather than claiming all RAM is available.
    The hardware UUID is hashed immediately and never returned in clear text.
    """
    identity = run(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"])
    match = re.search(r'"IOPlatformUUID"\s*=\s*"([^"\n]+)"', identity)
    if not match:
        raise ValueError("machine fingerprint unavailable")
    vm = run(["vm_stat"])
    page = re.search(r"page size of (\d+) bytes", vm)
    free = re.search(r"Pages free:\s*(\d+)\.", vm)
    speculative = re.search(r"Pages speculative:\s*(\d+)\.", vm)
    if not page or not free or not speculative or int(page[1]) <= 0:
        raise ValueError("memory measurement unavailable")
    pm = run(["pmset", "-g", "batt"])
    idle = run(["ioreg", "-c", "IOHIDSystem", "-d", "4"])
    idle_match = re.search(r'"HIDIdleTime"\s*=\s*(\d+)', idle)
    return dict(machine_fingerprint=hashlib.sha256(match[1].encode()).hexdigest(),
                architecture=platform.machine(), free_gb=shutil.disk_usage(root).free / 1024**3,
                load=os.getloadavg()[0],
                memory_available_gb=(int(free[1])+int(speculative[1]))*int(page[1])/1024**3,
                memory_basis="free plus speculative pages",
                on_ac="AC Power" in pm,
                idle_minutes=int(idle_match[1])/1e9/60 if idle_match else None)


def positive(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def registered(config, measured, at):
    start, end = workflow.timestamp(config.get("at")), workflow.timestamp(config.get("expiresAt"))
    if (config.get("version") != 1 or not config.get("approved_by") or not config.get("approval_ref")
            or not start or not end or not start <= at < end
            or end-start > dt.timedelta(days=30)
            or config.get("machine_fingerprint") != measured.get("machine_fingerprint")
            or not re.fullmatch(r"[0-9a-f]{64}", str(config.get("machine_fingerprint", "")))
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", str(config.get("host", "")))
            or config.get("role") not in {"mini", "macbook"}
            or type(config.get("configured_limit")) is not int
            or not 1 <= config["configured_limit"] <= 8
            or any(not positive(config.get(k)) for k in ("min_free_gb", "max_load", "min_memory_gb"))):
        raise ValueError("current identity-bound host registration required")


def collect(root, *, at, installed_head, measurement=measure):
    """Collect again on EVERY transaction attempt and immediately before launch.

    Caller still owns queue/board leases and Chief election. Returned account
    IDs are explicit shared-pool aliases, not identities or tokens. Probe files
    are receipts from a trusted local producer, never self-reported heartbeats.
    Missing or malformed evidence raises; partial evidence cannot become ready.
    Remote transport/authentication and probe producers remain unimplemented.
    """
    config = private_document(root, "registration.json")
    measured = measurement(root)
    registered(config, measured, at)
    probes = private_document(root, "probes.json")
    if (not isinstance(probes.get("workers"), dict)
            or not isinstance(probes.get("accounts"), dict)
            or probes.get("host") != config["host"]
            or probes.get("machine_fingerprint") != config["machine_fingerprint"]
            or not capacity.fresh(probes, at)):
        raise ValueError("fresh local identity-bound probe receipts required")
    if not re.fullmatch(r"[0-9a-f]{40}", installed_head or ""):
        raise ValueError("installed Git head required")
    host = {k: measured.get(k) for k in ("free_gb", "load", "memory_available_gb", "memory_basis",
                                        "on_ac", "idle_minutes", "architecture")}
    host.update({k: config.get(k) for k in ("host", "role", "configured_limit", "min_free_gb",
        "max_load", "min_memory_gb", "capacity_review", "reviewed_head")})
    host.update(registered_id=config["host"], installed_head=installed_head, state="idle",
                at=at.isoformat(), expiresAt=(at+dt.timedelta(seconds=60)).isoformat(),
                guard_reasons=[], workers={}, input_receipts={})
    accounts = {}
    bindings = config.get("workers")
    limits = config.get("accounts")
    if not isinstance(bindings, dict) or not isinstance(limits, dict):
        raise ValueError("explicit worker/shared-account bindings required")
    for worker, binding in bindings.items():
        if worker not in {"codex", "cursor", "gemini"} or not isinstance(binding, dict):
            raise ValueError("unsupported worker binding")
        account_id = binding.get("account")
        limit = limits.get(account_id)
        models = binding.get("models")
        if (not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", str(account_id or ""))
                or type(limit) is not int or not 1 <= limit <= 8
                or not isinstance(models, list) or not models
                or any(not isinstance(m, str) or not m for m in models)):
            raise ValueError("bounded shared-account and model binding required")
        report = (probes.get("workers") or {}).get(worker) or {}
        account = (probes.get("accounts") or {}).get(account_id) or {}
        # A stale/rejected receipt remains unavailable, never auto-cleared when
        # a retry timer expires. Auth status alone cannot supply model success.
        if (not isinstance(report, dict) or not isinstance(account, dict)
                or not capacity.fresh(report, at) or report.get("account") != account_id
                or report.get("ready") is not True or not report.get("auth_evidence")
                or not capacity.fresh(account, at) or account.get("ready") is not True
                or not account.get("quota_evidence") or account.get("limit") != limit):
            continue
        verified = report.get("verified_models")
        if not isinstance(verified, list) or not verified or any(m not in models for m in verified):
            continue
        host["workers"][worker] = {k: report[k] for k in
            ("at", "expiresAt", "account", "ready", "auth_evidence", "verified_models")}
        # Media proof has its own timestamp/evidence and must be bound to this
        # host/worker; text execution success is never proof of listening.
        caps = report.get("capabilities") or {}
        if (isinstance(caps, dict) and capacity.fresh(caps, at) and caps.get("evidence")
                and caps.get("host") == config["host"] and caps.get("worker") == worker
                and isinstance(caps.get("available"), list)
                and all(isinstance(item, str) for item in caps["available"])
                and set(caps["available"]) <= {"audio_input", "moving_video_input"}):
            host["workers"][worker]["capabilities"] = {k:caps[k] for k in
                ("at", "expiresAt", "available", "evidence")}
        else:
            host["workers"][worker]["capabilities"] = {}
        accounts[account_id] = {k:account[k] for k in ("at", "expiresAt", "ready", "quota_evidence", "limit")}
    problem = capacity.host_problem(host, at)
    if problem:
        host["guard_reasons"] = [problem]
        host["state"] = "waiting"
    return host, accounts


def observation(root, *, at, installed_head, evidence_root=None):
    """Public-safe read-only outlook; never expose registration/probe contents.

    Host occupancy is separate process/queue evidence. Guard readiness must not
    be displayed as an idle host or a promised slot. Registration is never made
    automatically, and no missing readiness receipt is repaired by this reader.
    """
    try:
        measured = measure(root)
    except (OSError, ValueError, subprocess.SubprocessError):
        return dict(state="unverified", reason="local measurements unavailable",
                    dispatch_enabled=False, free_slot_at=None, availability="unknown")
    result = {k:measured.get(k) for k in ("architecture", "free_gb", "load",
        "memory_available_gb", "memory_basis", "on_ac", "idle_minutes")}
    result.update(state="unverified", machine_fingerprint_observed=bool(measured.get("machine_fingerprint")),
                  reason="private host registration and probe receipts not configured",
                  dispatch_enabled=False, free_slot_at=None, availability="unknown")
    if evidence_root is not None:
        try:
            host, accounts = collect(evidence_root, at=at, installed_head=installed_head,
                                     measurement=lambda _: measured)
            result.update(state="guards_rejected" if host["guard_reasons"] else "observed",
                          reason="host/account observations only; occupancy and launch review remain separate",
                          guard_reasons=host["guard_reasons"], registered_host=host["registered_id"],
                          ready_workers=sorted(host["workers"]), observed_shared_accounts=len(accounts))
        except (OSError, ValueError, TypeError):
            result["reason"] = "private registration or probe receipts rejected"
    return result


def installed_head(root):
    """Exact commit identity, distinct from the relay's truncated code digest."""
    try:
        head = command(["git", "-C", str(root), "rev-parse", "HEAD"]).strip()
        if not re.fullmatch(r"[0-9a-f]{40}", head):
            return ""
        dirty = command(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"])
        return "" if dirty.strip() else head
    except (OSError, ValueError, subprocess.SubprocessError):
        return ""
