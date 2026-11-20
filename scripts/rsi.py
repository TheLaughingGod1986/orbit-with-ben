#!/usr/bin/env python3
"""Recursive self-improvement (RSI) loop for every registered channel (J3257, Ben 20 Nov 2026).

Studio-wide and driven by `scripts/channels.py` — never written per channel. Every registered channel gets
its own experiment entries, autopsy-to-hypothesis candidates, weekly improvement cycle, and dashboard row
automatically with no code change.

Commands:
    python3 scripts/rsi.py validate
    python3 scripts/rsi.py ingest-autopsies [--channel SLUG] [--apply]
    python3 scripts/rsi.py start <EXP_ID> [--readout YYYY-MM-DD] [--days 14]
    python3 scripts/rsi.py record <EXP_ID> --result pass|fail|inconclusive --sample N --evidence "..." [--changelog "..."]
    python3 scripts/rsi.py cycle --channel SLUG [--as-of YYYY-MM-DD]
    python3 scripts/rsi.py board
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
from zoneinfo import ZoneInfo

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import channels  # noqa: E402
import studio  # noqa: E402

LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc

MAX_LIVE_PER_CHANNEL = 3
DEFAULT_EXTEND_DAYS = 14
VALID_STATUSES = ("candidate", "running", "decided", "dropped")
VALID_RESULTS = ("pending", "pass", "fail", "inconclusive")
VALID_TEST_TYPES = ("test_and_compare", "next_n_films", "format_test", "style_test", "readout")
REQUIRED_FIELDS = (
    "id",
    "channel",
    "status",
    "result",
    "hypothesis",
    "change",
    "applies_to",
    "metric",
    "expected_effect",
    "readout_date",
    "evidence",
    "min_sample",
)

# Guardrails (item 6): areas the automated loop may NEVER change on its own.
# Any proposal touching these must go to Ben in one line instead of auto-starting or promoting.
PROTECTED_PATTERNS = (
    ("ben_gate", re.compile(r"\b(ben'?s?\s+(final\s+)?(gate|ok|watch|uat)|bypass\s+uat|skip\s+ben|auto[- ]?publish\s+without\s+ben)\b", re.I)),
    ("never_list", re.compile(r"\b(never[- ]?list|delete\s+(a\s+)?video|premiere\s+a\s+long|lift\s+tiktok\s+pause|direct\s+tiktok)\b", re.I)),
    ("money", re.compile(r"\b(buy\s+credits?|top[- ]?up|upgrade\s+plan|paid\s+overage|spend\s+past|billing|raise\s+budget|subscription\s+upgrade)\b", re.I)),
    ("channel_direction", re.compile(r"\b(rule\s*34\s+item\s*7|channel\s+direction|pivot\s+niche|change\s+channel\s+plan|lift\s+long\s+pause|override\s+ben'?s?\s+plan)\b", re.I)),
)


class RsiError(ValueError):
    """Validation or guardrail failure in the experiment register."""


def register_path() -> pathlib.Path:
    return channels.studio_records("EXPERIMENTS.json")


def ops_latest_path() -> pathlib.Path:
    return channels.studio_records("ops_loop", "latest.json")


def _today(now: dt.datetime | None = None) -> dt.date:
    return (now or dt.datetime.now(UTC)).astimezone(LONDON).date()


def _parse_date(value: str) -> dt.date | None:
    if not value:
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)):
        raise RsiError(f"bad ISO date {value!r} (expected YYYY-MM-DD)")
    return dt.date.fromisoformat(value)


def _date_label(value: str) -> str:
    if not value:
        return "No date yet"
    try:
        d = dt.date.fromisoformat(value[:10])
    except ValueError:
        return value
    return f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"


def _short_date(value: str) -> str:
    if not value:
        return ""
    try:
        d = dt.date.fromisoformat(value[:10])
    except ValueError:
        return value
    return f"{d.day} {d.strftime('%b')}"


def check_guardrails(exp: dict) -> list[str]:
    """Return list of guardrail categories violated by an experiment's text or scope."""
    if exp.get("ben_approved"):
        return []
    blob = " ".join(
        str(exp.get(k) or "")
        for k in ("hypothesis", "change", "expected_effect", "guardrail_scope", "revert_plan")
    )
    hits = [name for name, pat in PROTECTED_PATTERNS if pat.search(blob)]
    if exp.get("needs_ben"):
        hits.append("needs_ben")
    return sorted(set(hits))


def load_register(path: pathlib.Path | None = None) -> dict:
    p = path or register_path()
    if not p.is_file():
        return {
            "schema_version": 1,
            "max_live_per_channel": MAX_LIVE_PER_CHANNEL,
            "updated_at": "",
            "experiments": [],
        }
    return json.loads(p.read_text())


def save_register(doc: dict, path: pathlib.Path | None = None, now: dt.datetime | None = None) -> pathlib.Path:
    p = path or register_path()
    doc["updated_at"] = studio.iso(now or dt.datetime.now(UTC))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2) + "\n")
    return p


def validate_register(doc: dict, valid_slugs: list[str] | None = None) -> list[str]:
    """Validate register structure, channel slugs, <=3 live cap per channel, guardrails, and min_sample."""
    errors: list[str] = []
    if not isinstance(doc, dict) or not isinstance(doc.get("experiments"), list):
        return ["EXPERIMENTS.json must be an object with an 'experiments' list"]
    cap = int(doc.get("max_live_per_channel") or MAX_LIVE_PER_CHANNEL)
    if cap > MAX_LIVE_PER_CHANNEL:
        errors.append(f"max_live_per_channel {cap} exceeds studio cap {MAX_LIVE_PER_CHANNEL}")
    known = set(valid_slugs if valid_slugs is not None else channels.slugs())
    seen_ids: set[str] = set()
    live_counts: dict[str, int] = {}

    for idx, exp in enumerate(doc["experiments"]):
        if not isinstance(exp, dict):
            errors.append(f"experiments[{idx}] is not an object")
            continue
        eid = str(exp.get("id") or f"#{idx}")
        if eid in seen_ids:
            errors.append(f"duplicate experiment id {eid}")
        seen_ids.add(eid)
        for field in REQUIRED_FIELDS:
            if field not in exp:
                errors.append(f"{eid}: missing required field {field!r}")
        ch = str(exp.get("channel") or "")
        if ch not in known:
            errors.append(f"{eid}: unknown channel {ch!r} (registered: {sorted(known)})")
        status = str(exp.get("status") or "")
        if status not in VALID_STATUSES:
            errors.append(f"{eid}: invalid status {status!r}")
        result = str(exp.get("result") or "")
        if result not in VALID_RESULTS:
            errors.append(f"{eid}: invalid result {result!r}")
        if status == "decided" and result == "pending":
            errors.append(f"{eid}: decided experiment cannot have result 'pending'")
        if exp.get("readout_date"):
            try:
                _parse_date(str(exp["readout_date"]))
            except RsiError as exc:
                errors.append(f"{eid}: {exc}")
        elif status == "running":
            errors.append(f"{eid}: running experiment must declare a readout_date")
        min_sample = exp.get("min_sample")
        if not isinstance(min_sample, int) or isinstance(min_sample, bool) or min_sample < 1:
            errors.append(f"{eid}: min_sample must be a positive integer")
        if status == "decided" and result == "pass":
            obs = exp.get("sample_observed")
            if not isinstance(obs, int) or isinstance(obs, bool) or obs < (min_sample or 1):
                errors.append(f"{eid}: passed rule has sample_observed={obs!r} below min_sample={min_sample!r}")
            if not str(exp.get("evidence") or "").strip():
                errors.append(f"{eid}: passed rule must carry evidence")
            if not str(exp.get("revert_plan") or "").strip():
                errors.append(f"{eid}: passed rule must carry a revert_plan")
        if status == "running":
            live_counts[ch] = live_counts.get(ch, 0) + 1
            violations = check_guardrails(exp)
            if violations:
                errors.append(f"{eid}: running experiment violates guardrails {violations} without ben_approved")
        if status == "decided" and result == "pass":
            violations = check_guardrails(exp)
            if violations:
                errors.append(f"{eid}: promoted rule violates guardrails {violations} without ben_approved")

    for ch, count in sorted(live_counts.items()):
        if count > cap:
            errors.append(f"channel {ch!r} has {count} running experiments (max {cap})")
    return errors


# ---- Channel readiness (analytics sign-in + first 48h read) ------------------------------------------------------

def channel_autopsies(slug: str) -> list[pathlib.Path]:
    folder = channels.analytics_dir(slug) / "autopsy"
    return sorted(folder.glob("*.md")) if folder.is_dir() else []


def channel_cycle_ready(slug: str, register_doc: dict | None = None) -> bool:
    """True once this channel has a 48h launch read, an autopsy, a public-video snapshot, or a running experiment.

    A brand-new channel before analytics sign-in and its first 48h read returns False, so its weekly improvement
    cycle stays quiet until real data arrives, then starts automatically with no code change.
    """
    if register_doc:
        if any(e.get("channel") == slug and e.get("status") == "running" for e in register_doc.get("experiments") or []):
            return True
    if channel_autopsies(slug):
        return True
    adir = channels.analytics_dir(slug)
    launch_dir = adir / "launch"
    if launch_dir.is_dir():
        for path in launch_dir.glob("*.json"):
            try:
                rec = json.loads(path.read_text())
            except (OSError, ValueError):
                continue
            for r in rec.get("readings") or []:
                if isinstance(r, dict) and (r.get("hours") or 0) >= 48:
                    return True
    snap_dir = adir / "snapshots"
    if snap_dir.is_dir():
        for path in reversed(sorted(snap_dir.glob("*.json"))):
            try:
                snap = json.loads(path.read_text())
            except (OSError, ValueError):
                continue
            videos = snap.get("videos") or []
            if any(isinstance(v, dict) and v.get("privacy") == "public" for v in videos):
                return True
    return False


# ---- Autopsy -> Hypothesis candidate extraction (J3256 -> J3257) -------------------------------------------------

_FIX_LINE = re.compile(
    r"^\s*(?:[-*]|\d+[.)])\s*(?:\*\*)?(?:fix\s*\d*\s*)?"
    r"(?:\((this video|live video|packaging|next film|next \d+ (?:films?|longs?|shorts?)|production)\)|"
    r"\[(this video|live video|packaging|next film|next \d+ (?:films?|longs?|shorts?)|production)\])"
    r"\s*:?\s*(?:\*\*)?\s*(.+)$",
    re.I,
)
_TARGET_RE = re.compile(r"\b(?:next\s+(\d+)\s+(films?|longs?|shorts?))\b", re.I)
_PCT_RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*(?:to|->|→)\s*(\d+(?:\.\d+)?)\s*%", re.I)


def _infer_metric(text: str, scope: str) -> str:
    low = text.lower()
    if any(k in low for k in ("0:30", "first 30", "first 5", "first 10", "first 15", "hook", "opening")):
        return "0:30 retention (%)"
    if any(k in low for k in ("ctr", "click-through", "click through", "thumbnail", "title", "packaging")):
        return "impressions CTR (%)"
    if any(k in low for k in ("end screen", "handoff", "next video", "ending", "outro")):
        return "end-screen click rate (%)"
    if any(k in low for k in ("stayed", "swipe", "frame 0")):
        return "stayed-to-watch (%)"
    if any(k in low for k in ("search", "impression", "showing", "topic", "keyword")):
        return "14-day impressions"
    if scope == "test_and_compare":
        return "impressions CTR (%) / Test & Compare watch-time share"
    return "average % viewed"


def _infer_expected(text: str, metric: str) -> str:
    m = _PCT_RANGE_RE.search(text)
    if m:
        return f"raise {metric} from {m.group(1)}% to {m.group(2)}%"
    if "ctr" in metric.lower():
        return "beat live control in Test & Compare (or +1.0 pp CTR)"
    if "0:30" in metric.lower():
        return "raise 0:30 retention by +10 pp vs channel median"
    if "impressions" in metric.lower():
        return "raise 14-day impressions >= 2x channel median"
    return f"lift {metric} by +5 pp vs channel median"


def parse_autopsy(slug: str, path: pathlib.Path) -> list[dict]:
    """Parse a J3256 autopsy markdown file into candidate experiment records."""
    text = path.read_text()
    stem = path.stem  # <video_id>_<48h|7d>
    m = re.match(r"^(.+?)_(48h|7d)$", stem, re.I)
    video_id = m.group(1) if m else stem
    window = m.group(2).lower() if m else "48h"
    ch_label = channels.label(slug)

    fixes: list[tuple[str, str]] = []
    in_fixes = False
    for raw in text.splitlines():
        line = raw.strip()
        if re.match(r"^#{1,3}\s+.*fix", line, re.I):
            in_fixes = True
            continue
        if in_fixes and re.match(r"^#{1,3}\s+", line):
            in_fixes = False
        fm = _FIX_LINE.match(line)
        if fm:
            tag = (fm.group(1) or fm.group(2) or "").strip().lower()
            body = fm.group(3).strip()
            fixes.append((tag, body))
        elif in_fixes and re.match(r"^(?:[-*]|\d+[.)])\s+\S", line):
            body = re.sub(r"^(?:[-*]|\d+[.)])\s+", "", line).strip()
            tag = "this video" if re.search(r"\b(this video|live video|test & compare|thumbnail|retitle|description|end screen)\b", body, re.I) else "next film"
            fixes.append((tag, body))

    candidates: list[dict] = []
    for idx, (tag, body) in enumerate(fixes[:3], 1):
        is_live = any(k in tag for k in ("this video", "live", "packaging"))
        test_type = "test_and_compare" if is_live else "next_n_films"
        metric = _infer_metric(body, test_type)
        expected = _infer_expected(body, metric)
        nm = _TARGET_RE.search(body)
        if is_live:
            applies_to = [video_id]
            min_sample = 500
            sample_unit = "impressions"
            hypothesis = f"On {video_id}, {body} (tested via Test & Compare) will {expected}."
            revert_plan = f"Keep control arm on {video_id} in Studio Test & Compare if variant loses."
        else:
            n_films = int(nm.group(1)) if nm else 4
            unit = nm.group(2).lower() if nm else "longs"
            applies_to = [f"next {n_films} {ch_label} {unit}"]
            min_sample = n_films
            sample_unit = unit
            hypothesis = f"{body} will {expected} over the next {n_films} {unit}."
            revert_plan = f"Revert template/rule change in {slug} repo and restore previous generator prompt."

        sig = hashlib.sha1(f"{slug}|{path.name}|{body.lower()}".encode("utf-8")).hexdigest()[:6].upper()
        cand = {
            "id": f"EXP-{ch_label}-AUTO-{sig}",
            "channel": slug,
            "status": "candidate",
            "result": "pending",
            "hypothesis": hypothesis,
            "change": body,
            "applies_to": applies_to,
            "test_type": test_type,
            "metric": metric,
            "expected_effect": expected,
            "min_sample": min_sample,
            "sample_unit": sample_unit,
            "sample_observed": 0,
            "readout_date": "",
            "started_at": "",
            "extended_once": False,
            "source": f"autopsy:{slug}/{path.name}",
            "evidence": f"Proposed from {window} retention autopsy {path.name} (fix #{idx}).",
            "revert_plan": revert_plan,
            "guardrail_scope": "packaging" if is_live else "production",
            "decided_at": "",
            "changelog": "",
        }
        violations = check_guardrails(cand)
        if violations:
            cand["needs_ben"] = f"Guardrail hit ({', '.join(violations)}): review '{body}' in one line before testing."
        candidates.append(cand)
    return candidates


def ingest_autopsies(doc: dict, slugs: list[str] | None = None) -> list[dict]:
    """Scan every registered channel's autopsy folder and append new deduplicated candidates."""
    existing_ids = {e.get("id") for e in doc.get("experiments") or []}
    existing_keys = {
        (e.get("channel"), str(e.get("source") or ""), str(e.get("change") or "").strip().lower())
        for e in doc.get("experiments") or []
    }
    added: list[dict] = []
    for slug in (slugs if slugs is not None else channels.slugs()):
        for path in channel_autopsies(slug):
            for cand in parse_autopsy(slug, path):
                key = (cand["channel"], cand["source"], cand["change"].strip().lower())
                if cand["id"] in existing_ids or key in existing_keys:
                    continue
                doc.setdefault("experiments", []).append(cand)
                existing_ids.add(cand["id"])
                existing_keys.add(key)
                added.append(cand)
    return added


# ---- Lifecycle operations: start, record, weekly cycle brief -----------------------------------------------------

def start_experiment(
    doc: dict,
    exp_id: str,
    readout_date: str | None = None,
    days: int = 14,
    now: dt.datetime | None = None,
) -> dict:
    """Promote a candidate experiment to running, enforcing the <=3 live cap and guardrails."""
    cap = int(doc.get("max_live_per_channel") or MAX_LIVE_PER_CHANNEL)
    exp = next((e for e in doc.get("experiments") or [] if e.get("id") == exp_id), None)
    if not exp:
        raise RsiError(f"unknown experiment {exp_id!r}")
    if exp.get("status") != "candidate":
        raise RsiError(f"{exp_id} has status {exp.get('status')!r}, expected 'candidate'")
    violations = check_guardrails(exp)
    if violations:
        raise RsiError(f"{exp_id} blocked by guardrails {violations}; escalate to Ben in one line")
    ch = exp["channel"]
    live = [e for e in doc.get("experiments") or [] if e.get("channel") == ch and e.get("status") == "running"]
    if len(live) >= cap:
        raise RsiError(f"channel {ch!r} already has {len(live)}/{cap} running experiments")
    today = _today(now)
    rdate = readout_date or (today + dt.timedelta(days=days)).isoformat()
    _parse_date(rdate)
    exp["status"] = "running"
    exp["result"] = "pending"
    exp["started_at"] = today.isoformat()
    exp["readout_date"] = rdate
    return exp


def record_readout(
    doc: dict,
    exp_id: str,
    result: str,
    sample: int,
    evidence: str,
    changelog: str = "",
    extend_days: int = DEFAULT_EXTEND_DAYS,
    now: dt.datetime | None = None,
) -> dict:
    """Record a readout for a running experiment.

    - PASS: requires sample >= min_sample, evidence, revert_plan, and zero guardrail violations.
    - FAIL: marks decided/fail and records why it is reverted.
    - INCONCLUSIVE: extends readout_date once; a second inconclusive readout drops the experiment.
    """
    if result not in ("pass", "fail", "inconclusive"):
        raise RsiError(f"invalid readout result {result!r}")
    exp = next((e for e in doc.get("experiments") or [] if e.get("id") == exp_id), None)
    if not exp:
        raise RsiError(f"unknown experiment {exp_id!r}")
    if exp.get("status") != "running":
        raise RsiError(f"{exp_id} is {exp.get('status')!r}, not 'running'")
    if not str(evidence or "").strip():
        raise RsiError(f"{exp_id}: readout requires concrete evidence")
    today = _today(now)
    exp["sample_observed"] = int(sample)
    exp["evidence"] = evidence.strip()
    if changelog:
        exp["changelog"] = changelog.strip()

    if result == "pass":
        min_sample = int(exp.get("min_sample") or 1)
        if sample < min_sample:
            raise RsiError(
                f"{exp_id}: cannot PASS on sample={sample} < min_sample={min_sample}; record 'inconclusive' instead"
            )
        violations = check_guardrails(exp)
        if violations:
            raise RsiError(f"{exp_id}: cannot auto-promote rule touching guardrails {violations}; ask Ben in one line")
        exp["status"] = "decided"
        exp["result"] = "pass"
        exp["decided_at"] = today.isoformat()
    elif result == "fail":
        exp["status"] = "decided"
        exp["result"] = "fail"
        exp["decided_at"] = today.isoformat()
    else:  # inconclusive
        if not exp.get("extended_once"):
            base = _parse_date(str(exp.get("readout_date") or "")) or today
            new_date = max(base, today) + dt.timedelta(days=extend_days)
            exp["extended_once"] = True
            exp["result"] = "inconclusive"
            exp["readout_date"] = new_date.isoformat()
            exp["status"] = "running"
        else:
            exp["status"] = "dropped"
            exp["result"] = "inconclusive"
            exp["decided_at"] = today.isoformat()
    return exp


def cycle_plan(doc: dict, slug: str, as_of: dt.date | None = None) -> dict:
    """Compute what a channel's weekly improvement cycle needs to do right now."""
    ch = channels.get(slug)
    today = as_of or _today()
    cap = int(doc.get("max_live_per_channel") or MAX_LIVE_PER_CHANNEL)
    exps = [e for e in doc.get("experiments") or [] if e.get("channel") == slug]
    running = [e for e in exps if e.get("status") == "running"]
    due = [
        e for e in running
        if e.get("readout_date") and (_parse_date(str(e["readout_date"])) or today) <= today
    ]
    candidates = [e for e in exps if e.get("status") == "candidate" and not check_guardrails(e)]
    ben_escalations = [e for e in exps if e.get("status") == "candidate" and check_guardrails(e)]
    slots_open = max(0, cap - len(running))
    co = channels.checkout(slug)
    return {
        "channel": slug,
        "label": ch["label"],
        "name": ch["name"],
        "ready": channel_cycle_ready(slug, doc),
        "as_of": today.isoformat(),
        "repo_checkout": str(co) if co else str(channels.repo_path(slug)),
        "rules_file": channels.CHANNEL_RULES,
        "cap": cap,
        "running": running,
        "due_readouts": due,
        "slots_open": slots_open,
        "startable_candidates": candidates[:slots_open],
        "all_candidates": candidates,
        "ben_escalations": ben_escalations,
        "autopsies": [str(p) for p in channel_autopsies(slug)],
    }


# ---- Dashboard block: 'What the studio is learning' --------------------------------------------------------------

def _outcome_label(exp: dict) -> str:
    status = exp.get("status")
    result = exp.get("result")
    if status == "decided" and result == "pass":
        return "Kept"
    if status == "decided" and result == "fail":
        return "Reverted"
    if status == "dropped":
        return "Dropped"
    if status == "running" and exp.get("extended_once") and result == "inconclusive":
        return "Extended"
    return "Pending"


def board_section(
    experiments_doc: dict | None,
    ops_doc: dict | None,
    updated_at: str,
    previous: dict | None = None,
    now: dt.datetime | None = None,
) -> dict:
    """Build board['learning'] for the 'What the studio is learning' dashboard card.

    Iterates over `channels.all_channels()` so every registered channel (including newly added ones)
    automatically gets a row with zero code change. Keeps `updatedAt` stable on quiet publishes.
    """
    now = now or dt.datetime.now(UTC)
    today = _today(now)
    week_ago = today - dt.timedelta(days=7)
    doc = experiments_doc or {}
    exps = [e for e in (doc.get("experiments") or []) if isinstance(e, dict)]
    cap = int(doc.get("max_live_per_channel") or MAX_LIVE_PER_CHANNEL)

    channel_rows = []
    name_by_slug = {}
    for ch in channels.all_channels():
        slug = ch["slug"]
        name_by_slug[slug] = ch["name"]
        ch_exps = [e for e in exps if e.get("channel") == slug]
        running = [e for e in ch_exps if e.get("status") == "running"]
        running.sort(key=lambda e: (str(e.get("readout_date") or "9999-99-99"), str(e.get("id") or "")))
        candidates = [e for e in ch_exps if e.get("status") == "candidate"]
        ready = channel_cycle_ready(slug, doc)
        channel_rows.append({
            "slug": slug,
            "label": ch["label"],
            "name": ch["name"],
            "runningCount": len(running),
            "cap": cap,
            "candidateCount": len(candidates),
            "autopsyCount": len(channel_autopsies(slug)),
            "cycleReady": ready,
            "cycleNote": "" if ready else "Starts after analytics sign-in and first 48-hour read",
            "running": [
                {
                    "id": str(e.get("id") or ""),
                    "summary": str(e.get("change") or e.get("hypothesis") or ""),
                    "hypothesis": str(e.get("hypothesis") or ""),
                    "metric": str(e.get("metric") or ""),
                    "readoutDate": str(e.get("readout_date") or ""),
                    "readoutLabel": _date_label(str(e.get("readout_date") or "")),
                    "extended": bool(e.get("extended_once")),
                }
                for e in running
            ],
        })

    recent_results = []
    for e in exps:
        if e.get("status") not in ("decided", "dropped"):
            continue
        dec = str(e.get("decided_at") or "")
        try:
            d = dt.date.fromisoformat(dec[:10]) if dec else None
        except ValueError:
            d = None
        if d and d < week_ago:
            continue
        recent_results.append({
            "id": str(e.get("id") or ""),
            "channel": str(e.get("channel") or ""),
            "channelName": name_by_slug.get(str(e.get("channel") or ""), str(e.get("channel") or "")),
            "outcome": _outcome_label(e),
            "result": str(e.get("result") or ""),
            "summary": str(e.get("changelog") or e.get("change") or e.get("hypothesis") or ""),
            "evidence": str(e.get("evidence") or ""),
            "decidedAt": dec,
            "decidedLabel": _short_date(dec),
        })
    recent_results.sort(key=lambda r: (r["decidedAt"], r["id"]), reverse=True)

    ops = ops_doc if isinstance(ops_doc, dict) else {}
    bn = ops.get("bottleneck") if isinstance(ops.get("bottleneck"), dict) else {}
    prev_cmp = ops.get("previous_comparison") if isinstance(ops.get("previous_comparison"), dict) else {}
    ops_block = {
        "bottleneck": str(bn.get("title") or "No weekly ops measurement yet"),
        "summary": str(bn.get("summary") or "Run the weekly ops loop to name the studio's biggest bottleneck."),
        "proposedFix": str(bn.get("proposed_fix") or ""),
        "previousVerdict": str(prev_cmp.get("plain") or ""),
        "measuredAt": str(ops.get("measured_at") or ""),
        "measuredLabel": _short_date(str(ops.get("measured_at") or "")),
        "metricsLine": str(ops.get("metrics_line") or ""),
    }

    body = {
        "title": "What the studio is learning",
        "cap": cap,
        "runningTotal": sum(r["runningCount"] for r in channel_rows),
        "channels": channel_rows,
        "recentResults": recent_results,
        "ops": ops_block,
    }
    prev = previous or {}
    prev_body = {k: v for k, v in prev.items() if k != "updatedAt"}
    if prev_body == body and prev.get("updatedAt"):
        body["updatedAt"] = prev["updatedAt"]
    else:
        body["updatedAt"] = updated_at
    return body


# ---- CLI ---------------------------------------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="Validate 05_Analytics/EXPERIMENTS.json")

    p_ing = sub.add_parser("ingest-autopsies", help="Turn J3256 autopsies into candidate experiments")
    p_ing.add_argument("--channel", default="")
    p_ing.add_argument("--apply", action="store_true")

    p_st = sub.add_parser("start", help="Start a candidate experiment")
    p_st.add_argument("id")
    p_st.add_argument("--readout", default="")
    p_st.add_argument("--days", type=int, default=14)

    p_rec = sub.add_parser("record", help="Record an experiment readout")
    p_rec.add_argument("id")
    p_rec.add_argument("--result", required=True, choices=["pass", "fail", "inconclusive"])
    p_rec.add_argument("--sample", required=True, type=int)
    p_rec.add_argument("--evidence", required=True)
    p_rec.add_argument("--changelog", default="")

    p_cyc = sub.add_parser("cycle", help="Print weekly improvement cycle brief for a channel")
    p_cyc.add_argument("--channel", required=True)
    p_cyc.add_argument("--as-of", default="")

    sub.add_parser("board", help="Print the 'What the studio is learning' dashboard block as JSON")

    a = ap.parse_args(argv)
    doc = load_register()

    if a.cmd == "validate":
        errs = validate_register(doc)
        if errs:
            for e in errs:
                print(f"FAIL: {e}", file=sys.stderr)
            return 1
        by_ch = {s: sum(1 for e in doc["experiments"] if e.get("channel") == s and e.get("status") == "running")
                 for s in channels.slugs()}
        print(f"OK: {len(doc['experiments'])} experiments valid; live per channel: {by_ch}")
        return 0

    if a.cmd == "ingest-autopsies":
        slugs = [a.channel] if a.channel else None
        added = ingest_autopsies(doc, slugs)
        if a.apply and added:
            save_register(doc)
        print(f"{'Added' if a.apply else 'Found'} {len(added)} candidate experiment(s) from autopsies.")
        for c in added:
            print(f"  {c['id']} [{c['channel']}] ({c['test_type']}): {c['change']}")
        return 0

    if a.cmd == "start":
        try:
            exp = start_experiment(doc, a.id, readout_date=a.readout or None, days=a.days)
        except RsiError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        save_register(doc)
        print(f"Started {exp['id']} [{exp['channel']}]; readout {exp['readout_date']}")
        return 0

    if a.cmd == "record":
        try:
            exp = record_readout(doc, a.id, a.result, a.sample, a.evidence, a.changelog)
        except RsiError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        save_register(doc)
        print(f"Recorded {exp['id']}: status={exp['status']} result={exp['result']} readout={exp.get('readout_date')}")
        return 0

    if a.cmd == "cycle":
        as_of = _parse_date(a.as_of) if a.as_of else None
        plan = cycle_plan(doc, a.channel, as_of=as_of)
        print(json.dumps(plan, indent=2))
        return 0

    if a.cmd == "board":
        ops = None
        op = ops_latest_path()
        if op.is_file():
            try:
                ops = json.loads(op.read_text())
            except ValueError:
                ops = None
        block = board_section(doc, ops, studio.iso(dt.datetime.now(UTC)))
        print(json.dumps(block, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
