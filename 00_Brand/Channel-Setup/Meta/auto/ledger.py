#!/usr/bin/env python3
"""Ledger of shorts already posted to Instagram / Facebook."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SETUP = Path(__file__).resolve().parents[1]
LEDGER = SETUP / "META_POSTED.json"
LONDON = ZoneInfo("Europe/London")
_SOCIAL = SETUP.parent / "social"
if str(_SOCIAL) not in sys.path:
    sys.path.insert(0, str(_SOCIAL))
import uniqueness  # noqa: E402


def load() -> dict:
    if not LEDGER.exists():
        return {"version": 1, "posted": {}}
    return json.loads(LEDGER.read_text())


def save(data: dict) -> None:
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")


def key_for(short: dict) -> str:
    vid = uniqueness.youtube_id(short)
    if vid:
        return f"yt:{vid}"
    slug = uniqueness.file_slug(short.get("file") or short.get("path") or "")
    if slug:
        return f"file:{slug}"
    title = uniqueness.normalize_title(short.get("title") or "")
    return f"title:{title}" if title else "file:unknown"


def is_posted(short: dict, *, platform: str | None = None) -> bool:
    """True if this Short — or a remake / same file / same title — is already mirrored."""
    data = load()
    return uniqueness.already_mirrored(short, data.get("posted") or {}, platform=platform)


def mark_posted(short: dict, result: dict | None = None) -> None:
    data = load()
    data.setdefault("posted", {})
    key = key_for(short)
    prev = data["posted"].get(key) or {}
    platforms = (result or {}).get("platforms") or {}
    entry = {
        **prev,
        "marked_at": datetime.now(LONDON).isoformat(),
        "title": short.get("title"),
        "file": short.get("file"),
        "youtube_id": short.get("video_id"),
        "youtube_url": short.get("url"),
        "project": short.get("_project"),
        "result_status": (result or {}).get("status"),
        "method": (result or {}).get("method"),
    }
    for plat, plat_result in platforms.items():
        entry[plat] = plat_result
    if (result or {}).get("status") == "seeded":
        entry["status"] = "seeded"
        entry["instagram"] = {"status": "seeded"}
        entry["facebook"] = {"status": "seeded"}
    data["posted"][key] = entry
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)


def needs_platform(short: dict, platform: str) -> bool:
    return not is_posted(short, platform=platform)
