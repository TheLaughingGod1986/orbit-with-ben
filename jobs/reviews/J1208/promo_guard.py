"""J1208 no-network budget guard. No generation entry point.

Evidence must come from credential-safe live reads, never from this module's
defaults. Reserve under the existing vertex desk-lock before any billable call.
Unknown historic spend blocks rather than becoming zero. Existing ai_spend
readers ignore the new reserve/reconcile events; completed spend remains a
normal spend row. This deliberately does not modify shared studio core.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

PROJECT = "gen-lang-client-0538779324"
ACCOUNT = "billingAccounts/0124D1-E6EFD6-40F6DA"
MODEL = "veo-3.1-fast-generate-001"
REGION = "us-central1"
LOCK_ROOT = Path.home() / "_desk/locks"


class Stop(ValueError):
    pass


def money(value):
    try:
        d = Decimal(str(value))
    except Exception as exc:
        raise Stop("invalid money") from exc
    if not d.is_finite() or d < 0:
        raise Stop("invalid money")
    return d


def stamp(value):
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if d.utcoffset() is None:
            raise ValueError()
        return d
    except Exception as exc:
        raise Stop("invalid timestamp") from exc


def digest(rows):
    """SHA256 of canonical parsed rows, NOT sha256sum of raw ledger bytes."""
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


def check_lock():
    held = Path(os.environ.get("DESK_LOCK_HELD_DIR", "/nonexistent"))
    if held.resolve() != (LOCK_ROOT / "vertex.lock").resolve():
        raise Stop("canonical vertex desk-lock required")
    try:
        owner = dict(line.split("=", 1) for line in (held / "owner.txt").read_text().splitlines() if "=" in line)
        pid = int(owner["pid"])
        if pid not in (os.getpid(), os.getppid()):
            raise Stop("vertex lock belongs to another process")
        os.kill(pid, 0)
    except (OSError, KeyError, ValueError) as exc:
        raise Stop("live owned vertex desk-lock required") from exc


def read_rows(f):
    f.seek(0)
    raw = f.read()
    if raw and not raw.endswith("\n"):
        raise Stop("ledger incomplete trailing line; preserve and repair before append")
    try:
        rows = [json.loads(x) for x in raw.splitlines() if x.strip()]
        if any(not isinstance(r, dict) for r in rows):
            raise ValueError()
        return rows
    except (ValueError, TypeError) as exc:
        raise Stop("ledger malformed; preserve and repair before append") from exc


def assess(e, rows, now=None):
    try:
        return _assess(e, rows, now)
    except Stop:
        raise
    except (KeyError, TypeError, ValueError, ArithmeticError, AttributeError) as exc:
        raise Stop("malformed evidence or ledger") from exc


def _assess(e, rows, now=None):
    """Return a budget only; evidence is not permission or source approval.

    pending_since is an authoritative usage/billing reconciliation cutoff, NOT
    the time of the latest balance read. Without it billing lag is unbounded.
    """
    now = now or datetime.now(timezone.utc)
    for key in ("credits", "link", "service", "price", "usage"):
        age = (now - stamp(e[key]["at"])).total_seconds()
        if not 0 <= age <= 300:
            raise Stop(f"{key} evidence stale or in future")
    if e["link"].get("project") != PROJECT or e["link"].get("account") != ACCOUNT or e["link"].get("enabled") is not True:
        raise Stop("billing linkage unverified")
    s = e["service"]
    if (s.get("project"), s.get("model"), s.get("region"), s.get("served")) != (PROJECT, MODEL, REGION, True):
        raise Stop("served model/region unverified")
    c = e["credits"]
    if c.get("account") != ACCOUNT or c.get("vertex_eligible") is not True:
        raise Stop("promo entitlement unverified")
    active = [r for r in c["rows"] if r["status"] == "Available" and r["type"] == "CREDIT_TYPE_MONTHLY"]
    if not active:
        raise Stop("no available monthly credit")
    ids = [r["id"] for r in active]
    if len(set(ids)) != len(ids):
        raise Stop("duplicate credit row")
    available = sum((money(r["remaining_gbp"]) for r in active), Decimal(0))
    p = e["price"]
    if (p.get("model"), p.get("region"), p.get("resolution"), p.get("audio"), p.get("currency"), p.get("unit")) != (MODEL, REGION, "1080p", False, "GBP", "second"):
        raise Stop("price does not match request")
    if not p.get("source_url", "").startswith("https://cloud.google.com/") or not p.get("sku"):
        raise Stop("current regional GBP SKU evidence missing")
    rate, margin = money(p["per_second"]), money(p["margin"])
    if rate <= 0 or margin < Decimal("0.10"):
        raise Stop("positive price and >=10% currency margin required")
    per_take = (rate * (1 + margin) * 8).quantize(Decimal("0.01"), rounding=ROUND_CEILING)
    if per_take * 2 > 4:
        raise Stop("full scope exceeds GBP4")
    # Exact forward source recipe: tail 0..1.15, opening 1.15..3.85.
    for subject in ("s5", "s6"):
        recipe = e["duration"][subject]
        if recipe != {"source_seconds": 8, "preroll": [0, 1.15], "opening": [1.15, 3.85], "reverse": False, "speed": 1}:
            raise Stop("duration/forward-loop recipe not verified")
    cutoff = stamp(e["usage"]["pending_since"])
    if cutoff > min(stamp(e["usage"]["at"]), stamp(e["credits"]["at"])):
        raise Stop("usage cutoff newer than balance/usage snapshot")
    if e["usage"].get("all_projects_checked") is not True or not e["usage"].get("source"):
        raise Stop("pending spend coverage unverified")
    pending = money(e["usage"]["unlogged_upper_bound_gbp"])
    reservations = {}
    reconciled = set()
    seen_takes = set()
    started = set()
    for r in rows:
        if r.get("pool") != "vertex":
            continue
        kind = r.get("kind")
        if kind == "reserve":
            rid = r["reservation_id"]
            if rid in reservations:
                raise Stop("duplicate reservation id")
            reservations[rid] = r
            if r.get("job") == "J1208":
                if r.get("take") not in ("s5", "s6") or r["take"] in seen_takes:
                    raise Stop("duplicate or unscoped take")
                if rid != f"J1208:{r['take']}":
                    raise Stop("reservation id does not match take")
                seen_takes.add(r["take"])
        elif kind == "take_started":
            rid = r.get("reservation_id")
            if rid not in reservations or rid in started:
                raise Stop("duplicate or unreserved submission")
            started.add(rid)
        elif kind == "spend":
            rid = r.get("reservation_id")
            if r.get("job") == "J1208" and not rid:
                raise Stop("J1208 spend lacks reservation")
            if rid:
                if rid not in reservations or rid in reconciled or rid not in started:
                    raise Stop("unmatched or duplicate reconciliation")
                if money(r["amount"]) > money(reservations[rid]["amount"]):
                    raise Stop("spend exceeded reservation")
                reconciled.add(rid)
            # J1208 stays conservatively deducted even after a fresh balance
            # read: never infer settlement of our own unknown failed request.
            if rid or stamp(r["at"]) >= cutoff:
                amount = money(r["amount"])
                if amount == 0 and not (r.get("verified_zero_cost") is True and r.get("cost_source")):
                    raise Stop("unpriced pending spend requires upper bound")
                pending += amount
        elif kind != "record":
            raise Stop(f"unknown vertex ledger kind: {kind!r}")
    for rid, r in reservations.items():
        if rid not in reconciled:
            pending += money(r["amount"])
    remaining = 2 - len(seen_takes)
    full_remaining = per_take * remaining
    # Reserve both subjects before either call. Existing reservations remain in
    # pending even across fresh balance reads until explicitly reconciled.
    if available - pending - full_remaining < 1:
        raise Stop("GBP1 reserve would be breached")
    committed = sum((money(r["amount"]) for r in reservations.values() if r.get("job") == "J1208"), Decimal(0))
    if committed + full_remaining > 4:
        raise Stop("cumulative scope exceeds GBP4")
    return {"available_gbp": str(available), "pending_gbp": str(pending), "per_take_gbp": str(per_take), "remaining_takes": [x for x in ("s5", "s6") if x not in seen_takes], "ledger_sha256": digest(rows)}


def reserve(ledger: Path, evidence: dict, now=None):
    """Atomically reserve the entire remaining scope in the existing ledger.

    Caller must hold desk-lock vertex. This function never submits a request.
    A reservation consumes its take even if the process crashes or call fails.
    """
    check_lock()
    now = now or datetime.now(timezone.utc)
    with open_ledger(ledger) as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        rows = read_rows(f)
        result = assess(evidence, rows, now)
        if evidence.get("ledger_sha256") != result["ledger_sha256"]:
            raise Stop("ledger changed since pending-spend review")
        if not result["remaining_takes"]:
            raise Stop("scope already reserved; inspect submission journal, never resubmit")
        appended = []
        for take in result["remaining_takes"]:
            row = {"at": now.isoformat(), "kind": "reserve", "pool": "vertex", "amount": float(result["per_take_gbp"]), "film": "OWB:030", "job": "J1208", "take": take, "reservation_id": f"J1208:{take}", "by": "codex"}
            appended.append(row)
        f.write("".join(json.dumps(row) + "\n" for row in appended))
        f.flush()
        os.fsync(f.fileno())
    return {"reserved_takes": result["remaining_takes"], "ledger_sha256": digest(rows + appended), "submission_authorized": False}


def begin_take(ledger: Path, evidence: dict, take: str, now=None):
    """Consume one reserved take BEFORE submission. Crash means no retry.

    The caller must keep the desk lock until reconciliation. Returned identity
    is for a single call only; it is not an idempotency token for API retries.
    Fresh evidence is mandatory for both takes, including the second.
    """
    check_lock()
    now = now or datetime.now(timezone.utc)
    rid = f"J1208:{take}"
    with open_ledger(ledger) as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        rows = read_rows(f)
        result = assess(evidence, rows, now)
        if evidence.get("ledger_sha256") != digest(rows):
            raise Stop("ledger changed since pending-spend review")
        r = next((r for r in rows if r.get("kind") == "reserve" and r.get("reservation_id") == rid), None)
        if r is None or any(r.get("kind") == "take_started" and r.get("reservation_id") == rid for r in rows):
            raise Stop("unreserved or already attempted take; zero retries")
        if money(result["per_take_gbp"]) > money(r["amount"]):
            raise Stop("fresh estimate exceeds reserved bound")
        row = {**r, "kind": "take_started", "at": now.isoformat()}
        f.write(json.dumps(row) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return rid


def reconcile(ledger: Path, reservation_id: str, amount, now=None):
    """Write exactly one normal spend line; unknown failures retain full bound."""
    now = now or datetime.now(timezone.utc)
    check_lock()
    with open_ledger(ledger) as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        rows = read_rows(f)
        matches = [r for r in rows if r.get("kind") == "reserve" and r.get("reservation_id") == reservation_id]
        if len(matches) != 1 or any(r.get("kind") == "spend" and r.get("reservation_id") == reservation_id for r in rows):
            raise Stop("missing reservation or already reconciled")
        r = matches[0]
        if sum(r.get("kind") == "take_started" and r.get("reservation_id") == reservation_id for r in rows) != 1:
            raise Stop("take has not been consumed by submission journal")
        value = money(r["amount"] if amount is None else amount)
        if value <= 0:
            raise Stop("verified spend must be positive; None retains full bound")
        overrun = value > money(r["amount"])
        row = {**r, "kind": "spend", "amount": float(value), "at": now.isoformat(), "what": "J1208 one take; conservative estimate" if amount is None else "J1208 verified cost"}
        if overrun:
            row["budget_overrun"] = True
        f.write(json.dumps(row) + "\n")
        f.flush()
        os.fsync(f.fileno())
    if overrun:
        raise Stop("cost exceeded reserved ceiling; recorded actual cost, stop scope")
    return row


def open_ledger(ledger):
    try:
        return ledger.open("r+")
    except OSError as exc:
        raise Stop("existing writable ledger required") from exc
