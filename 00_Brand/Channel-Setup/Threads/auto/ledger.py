#!/usr/bin/env python3
"""Ledger of shorts already posted to Threads."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SETUP = Path(__file__).resolve().parents[1]
LEDGER = SETUP / "THREADS_POSTED.json"
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


def is_posted(short: dict) -> bool:
    data = load()
    return uniqueness.already_mirrored(short, data.get("posted") or {}, platform="threads")


def mark_posted(short: dict, result: dict | None = None) -> None:
    data = load()
    data.setdefault("posted", {})
    key = key_for(short)
    prev = data["posted"].get(key) or {}
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
        "status": (result or {}).get("status"),
    }
    threads_payload = {
        "status": (result or {}).get("status"),
        "method": (result or {}).get("method"),
        "url": (result or {}).get("url"),
        "permalink": (result or {}).get("permalink"),
    }
    if (result or {}).get("status") == "seeded":
        entry["status"] = "seeded"
        threads_payload["status"] = "seeded"
    entry["threads"] = threads_payload
    data["posted"][key] = entry
    data["updated_at"] = datetime.now(LONDON).isoformat()
    save(data)
