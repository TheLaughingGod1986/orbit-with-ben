#!/usr/bin/env python3
"""Queue one daily all-channel 14-day gate sweep, deduplicated urgent Chief fixes, and Ben watch alerts.

No YouTube writes. Every registered channel's private scheduled Shorts and longs in the next 14 days
are re-checked with the current blocking gates (music_gate included). A FAIL on anything airing within
7 days queues an urgent Chief fix job, and raises Ben's alert (J3292 / urgent_alerts) ONLY when a
cut-level gate failed so his watch of a replacement cut will be needed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channels  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LONDON = ZoneInfo("Europe/London")
SNAPSHOT_MAX_AGE_S = 36 * 3600
URGENT_DAYS = 7
BOARD_SITE = "https://board.oppti.dev"


def queue_daily(data: dict, at: datetime) -> list[str]:
    """Queue one daily all-channel 14-day gate sweep per London day (deduplicated against incomplete sweeps)."""
    import jobs
    day = at.astimezone(LONDON).date().isoformat()
    existing = [j for j in data["jobs"] if j.get("scheduled_gate_sweep")]
    if any(j.get("scheduled_gate_sweep") == day or j.get("status") in ("open", "claimed", "blocked") for j in existing):
        return []
    j = jobs.do_add(
        data,
        title="Check every scheduled video in the next fourteen days",
        needs="mini",
        body=(
            "Run `python3 scripts/scheduled_gates.py --apply --git`. Re-run current blocking gates "
            "(music_gate, gate_shorts_open, picture_qa, sfx_kit, and channel-required gates) on every "
            "registered channel's scheduled Shorts and longs in the next 14 days. No uploads, schedule or "
            "privacy changes. Report missing inputs or stale snapshots as coverage failures; do not call them PASS."
        ),
        by="refill",
        at=at,
        kind="assembly",
        action="Run the all-channel fourteen-day scheduled-video gate sweep",
        due=(at + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%MZ"),
    )
    j["scheduled_gate_sweep"] = day
    j["plain"] = "Check that every video due in the next two weeks is ready to air"
    return [j["id"]]


def _watch_needed(row: dict) -> bool:
    """True only when a cut-level blocking gate failed (replacement cut will need Ben's watch)."""
    return bool(row.get("needs_watch"))


def _alert_state_path(root: Path) -> Path:
    base = Path(os.environ.get("BOARD_STATE", str(Path.home() / "_desk" / "state" / "board")))
    return base / "scheduled_gate_alerts.json"


def raise_ben_alert_if_needed(row: dict, fix_job: dict, at: datetime, *, root: Path = ROOT,
                              state_path: Path | None = None, deliver_fn=None) -> dict | None:
    """Raise Ben's alert ONLY when a failing video within 7 days will require Ben's watch of a replacement cut.

    Delegates delivery to J3292's `urgent_alerts.deliver` when present and the cut airs within 24 h (or watch
    deadline within 12 h), and records a deduplicated alert entry so the board banner / J3292 loop surfaces it
    without double-alerting. Coverage/missing-input/metadata failures never trigger Ben's alert.
    """
    if not _watch_needed(row):
        return None
    when = datetime.fromisoformat(row["publishAt"].replace("Z", "+00:00"))
    watch_due = min(when - timedelta(hours=1), when)
    ch = str(row.get("channel") or "").upper()
    title = row.get("title") or row["id"]
    gates = ", ".join(row.get("failed_gates") or []) or "blocking gate"
    eid = f"gate:{row['channel']}:{row['id']}:{row['publishAt']}"
    event = {
        "id": eid,
        "kind": "watch",
        "channel": row["channel"],
        "videoId": row["id"],
        "fixJob": fix_job.get("id", ""),
        "due": watch_due.isoformat(),
        "slot": when.isoformat(),
        "reminder": False,
        "message": (
            f"{ch} {title} ({row['id']}) failed {gates} ahead of "
            f"{when.astimezone(LONDON):%a %d %b %H:%M} London. A replacement cut will need your watch."
        ),
        "url": f"{BOARD_SITE}/#review",
    }
    fix_job["ben_alert_required"] = True
    fix_job["ben_alert"] = event

    # Only send an immediate direct alert when the watch window is urgent (airing within 24 h or watch due within 12 h).
    urgent_now = (when <= at + timedelta(hours=24)) or (watch_due <= at + timedelta(hours=12))
    path = state_path or _alert_state_path(root)
    try:
        state = json.loads(path.read_text()) if path.is_file() else {}
    except (OSError, ValueError):
        state = {}
    sent_map = state.setdefault("events", {})
    if eid in sent_map:
        return {**event, "delivered": False, "deduplicated": True}

    delivery = None
    if urgent_now:
        if deliver_fn is None:
            try:
                import urgent_alerts  # J3292 alert module when merged
                deliver_fn = urgent_alerts.deliver
            except ImportError:
                deliver_fn = None
        if deliver_fn is not None:
            delivery = deliver_fn(event, root)
        else:
            delivery = {"status": "queued_for_urgent_alerts", "reason": "urgent_alerts module not installed yet"}
    sent_map[eid] = {**event, "recordedAt": at.isoformat(), "urgentNow": urgent_now, "delivery": delivery}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2) + "\n")
        tmp.replace(path)
    except OSError:
        pass
    return {**event, "urgentNow": urgent_now, "delivery": delivery}


def queue_fixes(data: dict, findings: list[dict], at: datetime, *, root: Path = ROOT,
                trigger_alerts: bool = True, alert_state_path: Path | None = None,
                deliver_fn=None) -> list[str]:
    """Queue one urgent Chief fix job per failing video airing within 7 days, and alert Ben only if his watch will be needed."""
    import jobs
    added: list[str] = []
    for row in findings:
        if row.get("ok"):
            continue
        when = datetime.fromisoformat(row["publishAt"].replace("Z", "+00:00"))
        if not at <= when <= at + timedelta(days=URGENT_DAYS):
            continue
        key = f"{row['channel']}:{row['id']}"
        if any(j.get("scheduled_gate_fix") == key and j.get("status") in ("open", "claimed", "blocked") for j in data["jobs"]):
            continue
        needs_watch = _watch_needed(row)
        watch_note = (
            "A cut-level gate failed, so a replacement cut will need Ben's watch (use awaits_ben with the real watch deadline; urgent alert armed)."
            if needs_watch
            else "Coverage, metadata or package failure only — do NOT alert Ben unless a new finished cut becomes necessary."
        )
        j = jobs.do_add(
            data,
            title=f"Urgent scheduled-video gate fix: {row['channel']} {row['id']}",
            needs="any",
            kind="chief",
            repo=row["channel"],
            by="refill",
            at=at,
            due=min(when, at + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%MZ"),
            action="Resolve the scheduled video gate findings before it airs",
            body=(
                f"Airs {row['publishAt']}. Current blocking checks failed or could not run.\n"
                f"{row.get('output', '')}\n"
                f"Chief: assign the repair immediately. {watch_note} No automatic privacy or schedule change."
            ),
        )
        j["scheduled_gate_fix"] = key
        j["urgent"] = 0
        j["needs_ben_watch"] = needs_watch
        j["plain"] = "Fix a readiness problem on a video airing this week"
        if trigger_alerts and needs_watch:
            raise_ben_alert_if_needed(row, j, at, root=root, state_path=alert_state_path, deliver_fn=deliver_fn)
        added.append(j["id"])
    return added


def _uploads_files_for(slug: str) -> list[Path]:
    """Return every UPLOADS.json for `slug` (channel checkout plus studio social/<slug>/UPLOADS.json when present)."""
    files: list[Path] = []
    primary = channels.uploads_file(slug)
    if primary and primary.is_file():
        files.append(primary)
    default_uploads = channels.uploads_file(channels.default())
    studio_social = (default_uploads.parent / slug / "UPLOADS.json") if default_uploads else None
    if studio_social and studio_social.is_file() and studio_social.resolve() not in {p.resolve() for p in files}:
        files.append(studio_social)
    return files


def _load_upcoming_module():
    tools_rel = Path("00_Brand") / "Channel-Setup" / "tools" / "gate_upcoming.py"
    path = Path(__file__).resolve().parent.parent / tools_rel
    if not path.is_file():
        path = channels.studio_checkout() / tools_rel
    spec = importlib.util.spec_from_file_location("scheduled_upcoming", path)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    return gate


def sweep(now: datetime | None = None, *, days: int = 14) -> dict:
    """Check every registered channel's scheduled Shorts and longs in the next `days` days.

    Never aborts remaining channels if one channel has a missing or stale snapshot: all checkable
    channels are checked and their reports persisted, while coverage errors are returned explicitly.
    """
    now = now or datetime.now(timezone.utc)
    gate = _load_upcoming_module()
    findings: list[dict] = []
    channel_status: dict[str, dict] = {}
    errors: list[str] = []

    for slug in channels.slugs():
        cfg = channels.get(slug)
        repo = channels.checkout(slug) or channels.repo_path(slug)
        data = channels.analytics_dir(slug)
        snapshots = sorted((data / "snapshots").glob("*.json")) if (data / "snapshots").is_dir() else []
        upload_files = _uploads_files_for(slug)

        # Prelaunch / not-yet-live channel with neither snapshots nor upload register: cleanly skip.
        if (cfg.get("launch_state") == "prelaunch" or not upload_files) and not snapshots:
            channel_status[slug] = {"status": "skipped", "reason": "no snapshots or scheduled uploads (prelaunch)"}
            continue
        if not repo or not repo.is_dir() or not snapshots or not upload_files:
            msg = f"{slug}: missing checkout, snapshot or upload register; sweep incomplete"
            errors.append(msg)
            channel_status[slug] = {"status": "error", "error": msg}
            continue

        latest = snapshots[-1]
        try:
            snap_doc = json.loads(latest.read_text())
            taken_raw = snap_doc.get("takenAt") or f"{snap_doc.get('date') or latest.stem}T06:40:00Z"
            taken = datetime.fromisoformat(str(taken_raw).replace("Z", "+00:00"))
        except (OSError, ValueError) as exc:
            msg = f"{slug}: unreadable snapshot {latest.name} ({exc}); sweep incomplete"
            errors.append(msg)
            channel_status[slug] = {"status": "error", "error": msg}
            continue

        age_s = (now - taken).total_seconds() if taken.tzinfo else -1
        if not taken.tzinfo or not 0 <= age_s <= SNAPSHOT_MAX_AGE_S:
            msg = f"{slug}: snapshot {latest.name} older than 36 hours ({age_s / 3600:.1f}h); sweep incomplete"
            errors.append(msg)
            channel_status[slug] = {"status": "error", "error": msg}
            continue

        report = data / "UPCOMING_PUBLISHING_GATES.md"
        argv = [
            "--snapshot", str(latest),
            "--uploads", str(upload_files[0]),
            "--media-root", str(repo),
            "--out", str(report),
            "--days", str(days),
        ]
        for extra in upload_files[1:]:
            argv += ["--extra-uploads", str(extra)]
        try:
            result = gate.main(argv)
            if result:
                raise RuntimeError(f"gate_upcoming exited {result}")
            rows = [dict(r, channel=slug) for r in json.loads(report.with_suffix(".json").read_text())]
            findings.extend(rows)
            channel_status[slug] = {
                "status": "checked",
                "snapshot": latest.name,
                "report": str(report),
                "count": len(rows),
                "fails": sum(1 for r in rows if not r.get("ok")),
            }
        except Exception as exc:  # noqa: BLE001 — isolate channel failures so other channels still complete
            msg = f"{slug}: sweep failed ({exc})"
            errors.append(msg)
            channel_status[slug] = {"status": "error", "error": msg}

    return {"findings": findings, "channels": channel_status, "errors": errors}


def main(argv=None) -> int:
    import jobs
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--git", action="store_true")
    p.add_argument("--days", type=int, default=14)
    a = p.parse_args(argv)
    outcome = sweep(days=a.days)
    print(json.dumps(outcome, indent=2))
    if a.apply:
        at = jobs.now()
        findings = outcome["findings"]
        if a.git:
            _, err = jobs.with_git(
                lambda d: (queue_fixes(d, findings, at), None, []),
                "jobs: urgent scheduled-video gate findings",
            )
            if err:
                raise RuntimeError(err)
        else:
            data = jobs.load()
            queue_fixes(data, findings, at)
            jobs.save(data)
    if outcome["errors"]:
        for err in outcome["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
