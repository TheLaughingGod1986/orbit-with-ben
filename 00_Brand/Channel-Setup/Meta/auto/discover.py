#!/usr/bin/env python3
"""Discover Orbit shorts that are live on YouTube and not yet on Meta."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from _sib import load

ledger = load("ledger")
caption = load("caption")
_SETUP = AUTO.parent
_SOCIAL = _SETUP.parent / "social"
if str(_SOCIAL) not in sys.path:
    sys.path.insert(0, str(_SOCIAL))
import uniqueness  # noqa: E402

REPO = AUTO.parents[3]
PROJECTS = REPO / "02_Video-Projects"
LONDON = ZoneInfo("Europe/London")
SCHEDULE_GRACE_MIN = 2


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=LONDON)
        return dt
    except Exception:
        return None


def is_live(short: dict, *, now: datetime | None = None) -> bool:
    """True when the short should be mirrored to Meta (IG + FB Page).

    Future ``schedule_iso`` always wins over a stale ``visibility: public`` /
    ``published_now`` flag — YouTube can still be Scheduled while the index
    says public. Matches TikTok ``discover.is_live``.
    """
    now = now or datetime.now(LONDON)
    sched = _parse_iso(short.get("schedule_iso"))
    if sched and now < sched + timedelta(minutes=SCHEDULE_GRACE_MIN):
        return False
    vis = str(short.get("visibility", "")).lower()
    # Past schedule_iso on a still-"scheduled" row is not a licence to upload
    # (deleted IDs / stale indexes). Wait until the index says public.
    if vis == "scheduled" and short.get("published_now") is not True:
        return False
    if short.get("published_now") is True and not sched:
        return True
    if vis == "public":
        return True
    if vis in {"public", ""} and sched and now >= sched + timedelta(minutes=SCHEDULE_GRACE_MIN):
        if short.get("video_id") or short.get("url"):
            return True
    return False


def resolve_file(project_root: Path, short: dict) -> Path | None:
    rel = short.get("file")
    if not rel:
        return None
    path = project_root / rel
    if path.exists():
        return path
    alt = project_root / "10_Shorts" / Path(rel).name
    if alt.exists():
        return alt
    exports = project_root / "10_Shorts" / "06_Final-Exports" / Path(rel).name
    if exports.exists():
        return exports
    return path if path.exists() else None


def iter_index_shorts() -> list[dict]:
    out: list[dict] = []
    for index in sorted(PROJECTS.glob("*/10_Shorts/SHORTS_UPLOAD_INDEX.json")):
        project_root = index.parents[1]
        try:
            data = json.loads(index.read_text())
        except Exception:
            continue
        for short in data.get("shorts") or []:
            item = dict(short)
            # Normalize Studio index field names
            if not item.get("video_id") and item.get("youtube_video_id"):
                item["video_id"] = item["youtube_video_id"]
            if item.get("video_id") and not item.get("url"):
                item["url"] = f"https://youtu.be/{item['video_id']}"
            # Normalize Studio index field names
            if not item.get("video_id") and item.get("youtube_video_id"):
                item["video_id"] = item["youtube_video_id"]
            if item.get("video_id") and not item.get("url"):
                item["url"] = f"https://youtu.be/{item['video_id']}"
            item["_project"] = project_root.name
            item["_project_root"] = str(project_root)
            item["_index"] = str(index)
            path = resolve_file(project_root, short)
            item["_abs_file"] = str(path) if path else None
            item["_ledger_key"] = ledger.key_for(short)
            item["_caption"] = caption.meta_caption(item)
            item["_needle"] = caption.confirm_needle(item, item["_caption"])
            item["_live"] = is_live(item)
            item["_posted"] = ledger.is_posted(item)
            out.append(item)
    return out


def pending_live_shorts() -> list[dict]:
    pending = []
    for s in iter_index_shorts():
        if not s["_live"]:
            continue
        if s["_posted"]:
            continue
        if not s.get("_abs_file") or not Path(s["_abs_file"]).exists():
            continue
        pending.append(s)
    posted = ledger.load().get("posted") or {}
    unique = uniqueness.first_unique(pending, posted)
    return unique[:1]
