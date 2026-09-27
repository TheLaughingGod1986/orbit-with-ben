#!/usr/bin/env python3
"""Ledger of shorts already posted/scheduled on TikTok (keyed by YouTube video_id or file)."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SETUP = Path(__file__).resolve().parents[1]
LEDGER = SETUP / "TIKTOK_POSTED.json"
LONDON = ZoneInfo("Europe/London")
_SOCIAL = SETUP.parent / "social"
if str(_SOCIAL) not in sys.path:
    sys.path.insert(0, str(_SOCIAL))
import uniqueness  # noqa: E402

# YouTube video_id → TikTok schedule slot (pre-scheduled / already on Studio).
# Auto-poster must NOT Post-now these — Studio already has them queued.
# Only Studio-confirmed entries until re-queue verifies.
YT_SCHEDULED_COVER = {
    "1HuV8o3gOss": {"tt_id": "aliens-01", "when": "2026-08-01T17:00:00+01:00"},
    "dPMJQp2gMNc": {"tt_id": "aliens-02", "when": "2026-08-02T12:30:00+01:00"},
    "rFJoOdQAc9c": {"tt_id": "aliens-03", "when": "2026-08-03T12:30:00+01:00"},
}


def load() -> dict:
    if not LEDGER.exists():
        return {"version": 1, "posted": {}}
    return json.loads(LEDGER.read_text())


def save(data: dict) -> None:
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")


def key_for(short: dict) -> str:
    vid = (short.get("video_id") or "").strip()
    if vid:
        return f"yt:{vid}"
    file = short.get("file") or short.get("path") or ""
    return f"file:{Path(file).name}"


def _entry_covers(short: dict, entry: dict) -> bool:
    """True if a ledger entry already covers this short (scheduled or posted)."""
    if not isinstance(entry, dict):
        return False
    status = str(entry.get("status") or entry.get("result_status") or "").lower()
    if status in {
        "scheduled",
        "scheduled_covered",
        "live",
        "ok",
        "seeded",
        "posted",
    }:
        return True
    # Older entries may only have marked_at / result_status
    if entry.get("marked_at") or entry.get("when"):
        return True
    return False


def is_posted(short: dict) -> bool:
    """True when TikTok already has this short (live OR pre-scheduled).

    Also treats remakes / same file / same title as already mirrored.
    """
    data = load()
    posted = data.get("posted", {})
    if uniqueness.already_mirrored(short, posted):
        return True
    key = key_for(short)
    if key in posted and _entry_covers(short, posted[key]):
        return True

    vid = (short.get("video_id") or "").strip()
    if vid and vid in YT_SCHEDULED_COVER:
        # Covered by the intentional pre-schedule batch unless explicitly forced
        cover = YT_SCHEDULED_COVER[vid]
        tt_key = f"tt:{cover['tt_id']}"
        if tt_key in posted and _entry_covers(short, posted[tt_key]):
            return True
        # Even without tt: row, known cover map means do not auto Post-now
        if data.get("mode") == "scheduled" or any(
            str(k).startswith("tt:") for k in posted
        ):
            return True

    # Match by youtube_id field inside any entry
    if vid:
        for entry in posted.values():
            if not isinstance(entry, dict):
                continue
            if entry.get("youtube_id") == vid and _entry_covers(short, entry):
                return True

    # Match by filename
    fname = Path(short.get("file") or short.get("_abs_file") or "").name
    if fname:
        file_key = f"file:{fname}"
        if file_key in posted and _entry_covers(short, posted[file_key]):
            return True
        for entry in posted.values():
            if not isinstance(entry, dict):
                continue
            ef = Path(str(entry.get("file") or "")).name
            if ef and ef == fname and _entry_covers(short, entry):
                return True
    return False


def mark_posted(short: dict, result: dict | None = None) -> None:
    data = load()
    data.setdefault("posted", {})
    data["posted"][key_for(short)] = {
        "marked_at": datetime.now(LONDON).isoformat(),
        "title": short.get("title"),
        "file": short.get("file") or short.get("_abs_file"),
        "youtube_id": short.get("video_id"),
        "youtube_url": short.get("url"),
        "project": short.get("_project"),
        "result_status": (result or {}).get("status"),
        "status": (result or {}).get("status") or "posted",
    }
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)


def mark_scheduled_cover(
    *,
    youtube_id: str,
    tt_id: str,
    when: str,
    file: str | None = None,
) -> None:
    """Record that a YouTube short is already covered by a TikTok schedule."""
    data = load()
    data.setdefault("posted", {})
    data["posted"][f"yt:{youtube_id}"] = {
        "marked_at": datetime.now(LONDON).isoformat(),
        "status": "scheduled_covered",
        "result_status": "scheduled_covered",
        "tt_id": tt_id,
        "when": when,
        "youtube_id": youtube_id,
        "file": file,
    }
    data["posted"][f"tt:{tt_id}"] = {
        "when": when,
        "status": "scheduled",
        "youtube_id": youtube_id,
        "file": file,
    }
    data["mode"] = "scheduled"
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)


def seed_scheduled_covers() -> int:
    """Ensure every YT id in the pre-schedule map is ledger-covered."""
    n = 0
    data = load()
    data.setdefault("posted", {})
    for yid, meta in YT_SCHEDULED_COVER.items():
        key = f"yt:{yid}"
        tt_key = f"tt:{meta['tt_id']}"
        if key not in data["posted"]:
            data["posted"][key] = {
                "marked_at": datetime.now(LONDON).isoformat(),
                "status": "scheduled_covered",
                "result_status": "scheduled_covered",
                "tt_id": meta["tt_id"],
                "when": meta["when"],
                "youtube_id": yid,
            }
            n += 1
        if tt_key not in data["posted"]:
            data["posted"][tt_key] = {
                "when": meta["when"],
                "status": "scheduled",
                "youtube_id": yid,
            }
            n += 1
        else:
            # Keep youtube_id linked on existing tt rows
            entry = data["posted"][tt_key]
            if isinstance(entry, dict) and not entry.get("youtube_id"):
                entry["youtube_id"] = yid
    data["mode"] = "scheduled"
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)
    return n


def record_failure(short: dict, reason: str) -> None:
    """Track consecutive auto-post failures for backoff."""
    data = load()
    fails = data.setdefault("failures", {})
    key = key_for(short)
    row = fails.get(key) or {"count": 0}
    row["count"] = int(row.get("count") or 0) + 1
    row["last_reason"] = reason
    row["last_at"] = datetime.now(LONDON).isoformat()
    fails[key] = row
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)


def clear_failure(short: dict) -> None:
    data = load()
    fails = data.get("failures") or {}
    key = key_for(short)
    if key in fails:
        del fails[key]
        data["failures"] = fails
        data["updated_at"] = datetime.now(LONDON).isoformat()
        save(data)


def should_skip_for_backoff(short: dict, *, max_fails: int = 3) -> str | None:
    """Return reason to skip if too many recent failures (e.g. check limit)."""
    data = load()
    row = (data.get("failures") or {}).get(key_for(short)) or {}
    count = int(row.get("count") or 0)
    reason = str(row.get("last_reason") or "")
    if count >= max_fails:
        return f"backoff after {count} fails ({reason})"
    if "check_limit" in reason and count >= 1:
        return f"content_check_limit ({reason})"
    return None
