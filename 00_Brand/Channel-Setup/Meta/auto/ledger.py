#!/usr/bin/env python3
"""Ledger of shorts already posted to Instagram / Facebook."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SETUP = Path(__file__).resolve().parents[1]
LEDGER = SETUP / "META_POSTED.json"
LONDON = ZoneInfo("Europe/London")


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


def is_posted(short: dict, *, platform: str | None = None) -> bool:
    """
    platform=None → True only when both enabled targets are done
    (or a single 'meta' umbrella mark exists from seeding).
    """
    data = load()
    entry = data.get("posted", {}).get(key_for(short))
    if not entry:
        return False
    # "posted" is the status written by the Aug 2026 socials sync and by
    # successful CDP confirms. Omitting it made the 5-minute watcher keep
    # re-opening Meta Reels composer for shorts that were already live.
    done = {"ok", "skipped", "seeded", "disabled", "scheduled", "posted"}
    if platform:
        if entry.get("status") == "seeded":
            return True
        plat = entry.get(platform)
        return bool(plat) and plat.get("status") in done
    # Umbrella seed
    if entry.get("status") == "seeded":
        return True
    ig = entry.get("instagram")
    fb = entry.get("facebook")
    # If either platform recorded ok/skipped intentionally, treat as done for that side
    ig_done = bool(ig) and ig.get("status") in done
    fb_done = bool(fb) and fb.get("status") in done
    # Complete when both sides have a terminal status
    return ig_done and fb_done


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
