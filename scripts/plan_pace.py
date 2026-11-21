#!/usr/bin/env python3
"""Use-it-all pacing for flat plans, and hard caps for pay-per-use (J3266, Ben 21 Nov 2026).

Flat plans cost the same used or not, so each one is aimed at landing near 100% at its reset.
Pay-per-use (a call that can bill the card) stays stopped until Ben sets a monthly cap.

  python3 scripts/plan_pace.py report     # project every plan; ElevenLabs first-run detail
  python3 scripts/plan_pace.py refresh    # write the local pace file the queue reads

The queue reads that file (or a test override). With neither, ordering and claims are unchanged.
A test file on the stack also leaves the queue alone, so a pace file on this machine cannot
change another test's order.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_spend  # noqa: E402
import routing  # noqa: E402

LONDON = ZoneInfo("Europe/London")
ROOT = Path(__file__).resolve().parents[1]
CAPS_FILE = ai_spend.DIR / "pay_per_use_caps.json"
STATE_FILE = Path.home() / "_desk" / "state" / "plan_pace.json"
WINDOW_DAYS = 7
LEFTOVER_PCT = 90.0
EARLY_DAYS = 3.0
DUE_SOON_DAYS = 7
SCHEDULE_DAYS = 28
# November Option 1 VO jobs keep 11,000 credits back (HOS fixes plus a margin). A raise
# that would spend into that reserve does not go ahead.
ELEVENLABS_RESERVE = 11000
WW2_MUSIC_UNTIL = datetime(2026, 12, 1, tzinfo=timezone.utc)
PROPOSAL = (
    "Ben: pay-per-use caps are unset, so nothing new bills the card — "
    "send one monthly £ cap each for Google video/image (Veo), Vercel, and overage if you want any."
)

# Flat plans. Flow is the included picture allowance on Google AI Ultra. vidIQ has no reader yet.
FLAT = ("claude", "cursor", "codex", "gemini", "flow", "elevenlabs", "vidiq")
WEEKLY = {"claude", "cursor", "codex", "gemini"}
NAMES = {
    "claude": "Claude",
    "cursor": "Cursor",
    "codex": "Codex",
    "gemini": "Google AI / Gemini",
    "flow": "Google Flow",
    "elevenlabs": "ElevenLabs",
    "vidiq": "vidIQ",
}
# What a queued job spends first. Tool pools have no other model (no second voice; Flow before Vertex).
KIND_POOL = {
    "script": "claude", "review": "claude", "qa": "claude", "listing": "claude",
    "facts": "gemini",
    "vo": "elevenlabs",
    "image": "flow", "video": "flow",
    "chart": "codex", "thumb": "codex",
    "assembly": "cursor", "studio": "cursor",
}
TOOL_POOLS = {"elevenlabs", "flow"}
MODEL_POOL = {
    "claude-opus-5-5": "claude",
    "cursor-claude-opus-5-5": "claude",
    "mini-claude-opus-5-5": "claude",
    "gpt-6-astra": "codex",
    "gpt-6.1-sol": "codex",
    "cursor-grok-4-7": "cursor",
    "cursor-auto": "cursor",
    "grok": "cursor",
    "gemini-argon": "gemini",
    "gemini-agy": "gemini",
    "eleven_v3": "elevenlabs",
    "scribe_v2": "elevenlabs",
    "flow-veo-3.1": "flow",
    "flow-nano-banana-2": "flow",
    "veo-3.1-fast-generate-001": "vertex",
    "veo-3.1-generate-001": "vertex",
    "gemini-omni-flash-preview": "vertex",
    "gemini-2.5-flash-image": "vertex",
}
PAY_PER_USE = ("vertex", "vercel", "overage")
PAY_LABELS = {
    "vertex": "Google video and image API (Veo and stills once they bill the card)",
    "vercel": "Vercel usage",
    "overage": "Plan overage",
}

_override = None
_override_on = False
_from_test = None
_cache: dict | None = None
_cache_at: datetime | None = None


def use(state: dict | None) -> None:
    """Tests pin a pace judgment. None still counts as pinned, so the live file stays out."""
    global _override, _override_on
    _override, _override_on = state, True


def clear() -> None:
    global _override, _override_on
    _override, _override_on = None, False


def _testing() -> bool:
    global _from_test
    if _from_test is not None:
        return _from_test
    _from_test = any("/test_" in fr.filename or fr.filename.endswith("_test.py")
                     for fr in traceback.extract_stack())
    return _from_test


def _parse(ts) -> datetime | None:
    return ai_spend._parse_iso(str(ts or ""))


def _day_label(when: datetime) -> str:
    local = when.astimezone(LONDON)
    return f"{local.day} {local.strftime('%b')}"


def _stamp(value) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return _parse(value)


def live() -> dict | None:
    """The judgment the queue should apply: the stored pace file, re-read at most every 10 minutes.

    Queue sorting and claim checks call this for every job, so it never recomputes the pace or reads ElevenLabs:
    refill's `refresh_if_stale` keeps the file current. A missing, unreadable or stale (36 h) file, and every test
    process, change nothing."""
    if _override_on:
        return _override
    if _testing():
        return None
    global _cache, _cache_at
    now = datetime.now(timezone.utc)
    if _cache_at and (now - _cache_at).total_seconds() < 600:
        return _cache
    try:
        state = json.loads(STATE_FILE.read_text())
    except (OSError, ValueError):
        state = None
    written = _parse((state or {}).get("at")) if isinstance(state, dict) else None
    if not state or not written or (now - written).total_seconds() > 36 * 3600:
        state = None
    _cache, _cache_at = state, now
    return state


_index: tuple | None = None


def index(rows: list | None) -> dict | None:
    """Jobs by id, built once per queue list rather than once per job that is sorted."""
    global _index
    if not rows:
        return None
    if _index and _index[0] is rows and _index[1] == len(rows):
        return _index[2]
    built = {r["id"]: r for r in rows if isinstance(r, dict) and "id" in r}
    _index = (rows, len(rows), built)
    return built


_dates: tuple | None = None


def _deadlines_and_air(rows: list | None) -> tuple[dict, dict]:
    """Deadlines and air dates for `blocks`, worked out once a minute per queue list instead of on every claim check
    (the air dates read the tracker files)."""
    global _dates
    now = datetime.now(timezone.utc)
    if _dates and _dates[0] is rows and _dates[1] == len(rows or ()) and (now - _dates[2]).total_seconds() < 60:
        return _dates[3], _dates[4]
    due, air = {}, {}
    try:
        import workflow_state
        if rows:
            due = workflow_state.deadlines(rows)
        if not _testing():
            from workflow_board import load_tracker
            air = workflow_state.air_dates(load_tracker())
    except Exception:
        pass
    _dates = (rows, len(rows or ()), now, due, air)
    return due, air


def load_caps() -> dict:
    try:
        raw = json.loads(CAPS_FILE.read_text())
    except (OSError, ValueError):
        raw = {}
    caps = raw.get("caps") if isinstance(raw, dict) else {}
    out = {}
    for key in PAY_PER_USE:
        spec = (caps or {}).get(key) or {}
        cap = spec.get("capGbp") if isinstance(spec, dict) else None
        out[key] = {"label": PAY_LABELS[key], "capGbp": cap if isinstance(cap, (int, float)) else None}
    return out


def allow(service: str, spent: float | None = None, caps: dict | None = None) -> dict:
    """Whether one more pay-per-use call may run. Unset cap: stop. At the cap: stop. Halfway: warn."""
    spec = (caps if caps is not None else load_caps()).get(service) or {}
    cap = spec.get("capGbp") if isinstance(spec, dict) else None
    amount = 0.0 if spent is None else float(spent)
    if cap is None:
        return {"ok": False, "stop": True, "warning": False,
                "reason": "cap unset; no new pay-per-use spend"}
    cap = float(cap)
    if amount >= cap:
        return {"ok": False, "stop": True, "warning": True, "reason": "at the cap"}
    if cap and amount >= cap / 2:
        return {"ok": True, "stop": False, "warning": True, "reason": "halfway to the cap"}
    return {"ok": True, "stop": False, "warning": False, "reason": "under the cap"}


def _used(row: dict, unit: str) -> tuple[float, float] | None:
    if row.get("left") is None:
        return None
    left = float(row["left"])
    if unit == "%":
        total = float(row["total"]) if row.get("total") else 100.0
        return max(0.0, total - left), total
    if row.get("total") is None:
        return None
    total = float(row["total"])
    return max(0.0, total - left), total


def _points(rows: list[dict], pool: str, unit: str, at: datetime) -> list[tuple]:
    """Balance readings. A credit total is kept from the last reading that named one, so a later
    'left' without a total still counts."""
    carried = None
    pts = []
    ordered = sorted(rows, key=lambda r: r.get("at") or "")
    for row in ordered:
        if row.get("pool") != pool or row.get("kind") != "record":
            continue
        when = _parse(row.get("at"))
        if not when or when > at:
            continue
        if row.get("total"):
            carried = float(row["total"])
        elif unit != "%" and carried and row.get("left") is not None:
            row = dict(row, total=carried)
        used = _used(row, unit)
        if not used:
            continue
        pts.append((when, used[0], used[1], row))
    return pts


def _rate(pts: list[tuple], at: datetime, allowance: float, reset: datetime | None = None,
          weekly: bool = False) -> float | None:
    """Use per day across the last 7 days, after the last refill in that window.

    A weekly plan that has reset inside the week often has a single reading since. That reading
    is measured from zero at the start of the window (reset minus 7 days), which is the rate
    the current allowance is actually being spent at.
    """
    if allowance <= 0 or not pts:
        return None
    start = at - timedelta(days=WINDOW_DAYS)
    window = [p for p in pts if p[0] >= start]
    if len(window) < 2 and len(pts) >= 2 and (at - pts[-2][0]) <= timedelta(days=WINDOW_DAYS + 1):
        window = pts[-2:]
    cut = 0
    for i in range(1, len(window)):
        if window[i - 1][1] - window[i][1] > allowance * 0.3:
            cut = i
    window = window[cut:]
    if len(window) >= 2:
        days = (window[-1][0] - window[0][0]).total_seconds() / 86400
        if days >= 0.25:
            return (window[-1][1] - window[0][1]) / days
    if weekly and reset is not None:
        opened = reset - timedelta(days=7)
        latest = pts[-1]
        if opened <= latest[0] <= at:
            days = (latest[0] - opened).total_seconds() / 86400
            if days >= 0.25:
                return latest[1] / days
    return None


def _note_reset(note: str, at: datetime) -> datetime | None:
    """The weekly reset, not an earlier 5-hour 'resets 13:12Z' in the same note."""
    weekly = re.search(r"weekly[^;\n]{0,120}?resets?\s+(?:on\s+|at\s+)?([^;\n]+)", note or "", re.I)
    if weekly:
        found = ai_spend._weekly_reset("weekly resets " + weekly.group(1).strip().rstrip("."), at)
        if found:
            return found
    return ai_spend._weekly_reset(note or "", at)


def _reset(pool: str, latest: dict | None, plans: dict, at: datetime) -> datetime | None:
    if pool in WEEKLY and latest:
        when = _parse(latest.get("at"))
        found = _note_reset(latest.get("note") or "", when) if when else None
        if found and found > at:
            return found
    for sub in plans.get("subscriptions") or []:
        if pool not in (sub.get("pools") or []):
            continue
        window = (sub.get("allowanceWindows") or {}).get(pool) or {}
        end = _parse(window.get("end")) if window.get("verified") else None
        if end and end > at:
            return end
        renews = sub.get("renews") or ""
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", renews):
            day = datetime.fromisoformat(renews + "T00:00:00+00:00")
            if day > at:
                return day
    return None


def _project(pool: str, rows: list[dict], plans: dict, at: datetime) -> dict:
    unit = ai_spend.POOLS.get(pool, "credits")
    name = NAMES[pool]
    if pool == "vidiq":
        return {"id": pool, "name": name, "flat": True, "state": "unknown", "line": "no reading yet",
                "unit": "credits"}
    pts = _points(rows, pool, unit, at)
    if not pts:
        return {"id": pool, "name": name, "flat": True, "state": "unknown", "line": "no reading yet",
                "unit": unit}
    when, used, allowance, row = pts[-1]
    left = float(row["left"])
    reset = _reset(pool, row, plans, at)
    rate = _rate(pts, at, allowance, reset, weekly=pool in WEEKLY)
    base = {"id": pool, "name": name, "flat": True, "unit": unit, "left": left, "total": allowance,
            "used": round(used, 2), "usedPct": round(used / allowance * 100, 1) if allowance else None,
            "ratePerDay": None if rate is None else round(rate, 2), "readAt": row.get("at"),
            "reset": reset.isoformat().replace("+00:00", "Z") if reset else ""}
    if pool == "elevenlabs":
        base["reserve"] = ELEVENLABS_RESERVE
        base["spare"] = round(left - ELEVENLABS_RESERVE, 2)
    if reset is None or rate is None:
        base.update(state="unknown", line="not enough of the last 7 days to project")
        return base
    days = (reset - at).total_seconds() / 86400
    if days <= 0:
        base.update(state="unknown", line="reset already passed; awaiting a new reading")
        return base
    burn = max(rate, 0.0)
    projected = used + burn * days
    pct = projected / allowance * 100 if allowance else 0
    if burn > 0 and used < allowance:
        days_to_full = (allowance - used) / burn
    elif used >= allowance:
        days_to_full = 0.0
    else:
        days_to_full = float("inf")
    hit = at + timedelta(days=days_to_full) if days_to_full < 1e8 else None
    shown = int(round(min(100, max(0, pct))))
    if days_to_full + 1e-9 < days - EARLY_DAYS:
        when_full = hit or at
        base.update(state="early_out", projectedPct=shown, hit=when_full.isoformat().replace("+00:00", "Z"),
                    line=f"on track to use 100% by {_day_label(when_full)}")
    elif pct < LEFTOVER_PCT:
        base.update(state="leftovers", projectedPct=shown, line=f"on track to use {shown}% by {_day_label(reset)}")
    else:
        base.update(state="on_track", projectedPct=shown, line=f"on track to use {shown}% by {_day_label(reset)}")
    return base


def _month_spend(rows: list[dict], pool: str, at: datetime) -> float:
    month = at.astimezone(timezone.utc).strftime("%Y-%m")
    return round(sum(float(r.get("amount") or 0) for r in rows
                     if r.get("kind") == "spend" and r.get("pool") == pool and str(r.get("at", "")).startswith(month)), 2)


def _caps_view(rows: list[dict], at: datetime, caps: dict) -> list[dict]:
    out = []
    for key in PAY_PER_USE:
        spent = _month_spend(rows, key, at) if key == "vertex" else 0.0
        decision = allow(key, spent, caps)
        cap = (caps.get(key) or {}).get("capGbp")
        if cap is None:
            line = f"{PAY_LABELS[key]}: cap unset · no new pay-per-use spend · £{spent:.2f} spent this month"
        else:
            line = f"{PAY_LABELS[key]}: £{spent:.2f} of £{float(cap):.2f} cap"
            if decision["warning"] and decision["ok"]:
                line += " · halfway warning"
            if decision["stop"]:
                line += " · stopped"
        out.append({"service": key, "label": PAY_LABELS[key], "capGbp": cap, "spentGbp": spent,
                    "line": line, "stop": decision["stop"], "warning": decision["warning"]})
    return out


def compute(at: datetime | None = None, rows: list[dict] | None = None, plans: dict | None = None,
            caps: dict | None = None) -> dict:
    at = at or datetime.now(timezone.utc)
    if rows is None:
        rows = ai_spend.load()
    if plans is None:
        plans = json.loads(ai_spend.PLANS.read_text()) if ai_spend.PLANS.exists() else {}
    if caps is None:
        caps = load_caps()
    flagged = []
    try:
        flagged = sorted(routing.read_flags(at))
    except Exception:
        flagged = []
    plans_out = {pool: _project(pool, rows, plans, at) for pool in FLAT}
    return {"at": at.isoformat().replace("+00:00", "Z"), "plans": plans_out,
            "caps": _caps_view(rows, at, caps), "proposal": PROPOSAL, "flags": flagged}


def for_board(rows: list[dict] | None = None, built: dict | None = None, at: datetime | None = None) -> dict:
    """The slice the AI & credits tab reads. `built` is accepted so a caller can pass the spend doc."""
    del built
    state = compute(at, rows)
    return {"at": state["at"], "proposal": state["proposal"], "plans": state["plans"], "caps": state["caps"]}


def _film_keys(job: dict) -> set[str]:
    import channels
    keys = set()
    film = job.get("film") or ""
    if isinstance(film, str) and film.strip():
        keys.add(film)
        if re.fullmatch(r"\d{3}", film):
            slug = job.get("repo") if job.get("repo") in channels.slugs() else channels.default()
            keys.add(channels.label(slug) + ":" + film)
    for key in job.get("taskKeys") or []:
        if isinstance(key, str):
            keys.add(key)
    return keys


def _soon(job: dict, at: datetime, days: int, due: dict | None, air: dict | None) -> bool:
    limit = at + timedelta(days=days)
    stamps = []
    if due and job.get("id") in due:
        stamps.append(due[job["id"]])
    stamps.append(_stamp(job.get("due")))
    rec = job.get("approved_from") or {}
    if isinstance(rec, dict):
        stamps.append(_stamp(rec.get("airs") or rec.get("due")))
    elif isinstance(rec, list):
        for item in rec:
            if isinstance(item, dict):
                stamps.append(_stamp(item.get("airs") or item.get("due")))
    if air:
        for key in _film_keys(job):
            if key in air:
                stamps.append(air[key])
    return any(stamp and at <= stamp <= limit for stamp in stamps)


def ready(job: dict, by_id: dict | None) -> bool:
    if job.get("status") != "open":
        return False
    if job.get("hold") or job.get("awaits_ben") or job.get("needs") == "ben":
        return False
    parent = job.get("after")
    if parent:
        if not by_id or (by_id.get(parent) or {}).get("status") != "done":
            return False
    return True


def approved(job: dict, at: datetime, due: dict | None, air: dict | None) -> bool:
    """Already queued on a film, or dated inside the next four weeks. Backlog is not approved."""
    if job.get("backlog"):
        return False
    if _soon(job, at, SCHEDULE_DAYS, due, air):
        return True
    return bool(job.get("kind") in KIND_POOL and (job.get("film") or job.get("taskKeys")))


def service_block(job: dict, at: datetime) -> str:
    """November Option 1: ElevenLabs narration only. No music for WW2 before December."""
    if at >= WW2_MUSIC_UNTIL:
        return ""
    blob = " ".join(str(job.get(k) or "") for k in ("title", "body", "plain", "repo", "film"))
    if not re.search(r"\bww2\b", blob, re.I):
        return ""
    # Narration briefs mention the music ban in the same paragraph. The ban is the music job, not the narration.
    if re.search(r"narrat", blob, re.I) and job.get("kind") == "vo":
        return ""
    if re.search(r"\bmusic\b|\bscore\b", blob, re.I):
        return "no ElevenLabs music for WW2 in November"
    return ""


def estimate_credits(job: dict) -> int:
    """What this job would spend. A '~9,500 credits' figure is the cost; a balance in the brief is not."""
    text = " ".join(str(job.get(k) or "") for k in ("title", "body", "plain"))
    approx = re.findall(r"(?:~|about\s+)(\d{1,3}(?:,\d{3})+|\d{3,6})\s*credits", text, re.I)
    if approx:
        return int(approx[-1].replace(",", ""))
    if job.get("kind") != "vo":
        return 0
    if re.search(r"narrat|chapter|\blong\b", text, re.I):
        return 9500
    return 1500


def budget_ok(job: dict, plan: dict) -> bool:
    if plan.get("id") != "elevenlabs" and KIND_POOL.get(job.get("kind")) != "elevenlabs":
        return True
    spare = plan.get("spare")
    if spare is None:
        return False
    return estimate_credits(job) <= float(spare)


def low_priority(job: dict, at: datetime, due: dict | None, air: dict | None) -> bool:
    if job.get("urgent"):
        return False
    if _soon(job, at, DUE_SOON_DAYS, due, air):
        return False
    return True


def _plan(state: dict | None, pool: str | None) -> dict | None:
    if not state or not pool:
        return None
    return (state.get("plans") or {}).get(pool)


def is_raised(job: dict, at: datetime, due: dict | None = None, air: dict | None = None,
              by_id: dict | None = None, state: dict | None = None) -> bool:
    state = live() if state is None else state
    plan = _plan(state, KIND_POOL.get(job.get("kind")))
    if not plan or plan.get("state") != "leftovers":
        return False
    if not ready(job, by_id) or not approved(job, at, due, air):
        return False
    if (KIND_POOL.get(job.get("kind")) == "elevenlabs" or job.get("kind") == "vo") and service_block(job, at):
        return False
    return budget_ok(job, plan)


def is_held(job: dict, at: datetime, due: dict | None = None, air: dict | None = None,
            state: dict | None = None) -> bool:
    """Low-priority work on a plan that runs out early. Urgent and due-soon stay."""
    state = live() if state is None else state
    plan = _plan(state, KIND_POOL.get(job.get("kind")))
    if not plan or plan.get("state") != "early_out":
        return False
    if job.get("status") not in ("open", "claimed"):
        return False
    return low_priority(job, at, due, air)


def model_for(job: dict, agent: str) -> str:
    named = job.get("model") or ""
    if named and routing.RUNS_ON.get(named) == agent:
        return named
    chain = routing.CHAINS.get(job.get("kind") or "")
    if not chain:
        return ""
    for who, model in chain[1]:
        if who == agent:
            return model
    return ""


def agent_pool(job: dict, agent: str) -> str:
    kind_pool = KIND_POOL.get(job.get("kind"))
    if kind_pool in TOOL_POOLS:
        return kind_pool
    return MODEL_POOL.get(model_for(job, agent), "") or (kind_pool or "")


def blocks(job: dict, agent: str, at: datetime, rows: list | None = None, state: dict | None = None) -> bool:
    """True when this agent would spend a plan that must be kept for urgent and due-soon work."""
    state = live() if state is None else state
    if not state:
        return False
    pool = agent_pool(job, agent)
    plan = _plan(state, pool)
    if not plan or plan.get("state") != "early_out":
        return False
    if job.get("status") not in ("open", "claimed"):
        return False
    due, air = _deadlines_and_air(rows)
    if not low_priority(job, at, due, air):
        return False
    # Reaching here means this agent's own pool is the one running out early.
    # A fallback on a healthy pool returned above, when its plan state was not early_out.
    return True


def raised_ids(jobs: list[dict], state: dict, at: datetime, due: dict | None = None, air: dict | None = None) -> list[str]:
    by_id = {j["id"]: j for j in jobs}
    return [j["id"] for j in jobs if is_raised(j, at, due, air, by_id, state)]


def held_ids(jobs: list[dict], state: dict, at: datetime, due: dict | None = None, air: dict | None = None) -> list[str]:
    return [j["id"] for j in jobs if is_held(j, at, due, air, state)]


def refresh(at: datetime | None = None) -> dict:
    """Recompute and store the pace file. Once a London day is enough; the caller may repeat."""
    at = at or datetime.now(timezone.utc)
    if _testing() and not _override_on:
        return {}
    state = compute(at, ai_spend.load() + _live_elevenlabs(at))
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n")
    except OSError:
        pass
    global _cache, _cache_at
    _cache, _cache_at = state, at
    return state


def refresh_if_stale(at: datetime | None = None, max_age_h: float = 1.0) -> dict | None:
    """Refill's call: recompute only when the stored pace file is missing or older than `max_age_h`."""
    at = at or datetime.now(timezone.utc)
    try:
        written = _parse(json.loads(STATE_FILE.read_text()).get("at"))
    except (OSError, ValueError, AttributeError):
        written = None
    if written and (at - written).total_seconds() < max_age_h * 3600:
        return None
    return refresh(at)


def _live_elevenlabs(at: datetime) -> list[dict]:
    """The shared ElevenLabs account, read now. A Codex log on this machine is a different seat, so it is not mixed in."""
    try:
        import ai_spend_daily
        el = ai_spend_daily.read_elevenlabs()
    except (Exception, SystemExit):  # el_auth exits when this machine has no ElevenLabs key
        return []
    if el.get("left") is None or el.get("total") is None:
        return []
    return [{"at": at.isoformat().replace("+00:00", "Z"), "kind": "record", "pool": "elevenlabs",
             "left": el["left"], "total": el["total"], "note": el.get("note") or "", "by": "plan-pace"}]


def report_text(at: datetime | None = None) -> str:
    at = at or datetime.now(timezone.utc)
    rows = ai_spend.load()
    fresh = _live_elevenlabs(at)
    state = compute(at, rows + fresh)
    lines = ["Flat-plan pace (last 7 days projected to the reset):"]
    for pool in FLAT:
        plan = state["plans"][pool]
        left = ""
        if plan.get("left") is not None and plan.get("total") is not None:
            if plan.get("unit") == "%":
                left = f" — {plan['usedPct']}% used, {plan['left']}% left"
            else:
                left = f" — {int(plan['left']):,} left of {int(plan['total']):,}"
        lines.append(f"- {plan['name']}: {plan['line']}{left}")
    lines.append("Pay-per-use:")
    lines.extend(f"- {cap['line']}" for cap in state["caps"])
    lines.append(state["proposal"])
    el = state["plans"]["elevenlabs"]

    def _whole(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    lines.append(
        f"ElevenLabs first run: {_whole(el.get('left'))} left of {_whole(el.get('total'))}, "
        f"reserve {_whole(el.get('reserve'))}, spare above reserve {_whole(el.get('spare'))}. {el.get('line')}."
    )
    try:
        import jobs as jobs_mod
        queued = jobs_mod.load().get("jobs") or []
        import workflow_state
        due = workflow_state.deadlines(queued)
        air = {}
        try:
            from workflow_board import load_tracker
            air = workflow_state.air_dates(load_tracker())
        except Exception:
            air = {}
        raised = raised_ids(queued, state, at, due, air)
        held = held_ids(queued, state, at, due, air)
        lines.append(f"Raised ({len(raised)}, approved ready work on a plan heading under 90%): "
                     + (", ".join(raised[:25]) or "none")
                     + (" …" if len(raised) > 25 else ""))
        lines.append(f"Held ({len(held)}, low priority kept off a plan that hits zero early; "
                     "a later model in that kind's chain can still take them): "
                     + (", ".join(held[:25]) or "none")
                     + (" …" if len(held) > 25 else ""))
    except Exception as exc:
        lines.append(f"Queue not read: {exc.__class__.__name__}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["report", "refresh"])
    args = ap.parse_args(argv)
    if args.cmd == "refresh":
        state = refresh()
        el = (state.get("plans") or {}).get("elevenlabs") or {}
        print(el.get("line") or "pace refreshed")
        return 0
    print(report_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
